"""
apriori.py — Apriori Recommendation Engine (no external ML libraries needed)
============================================================
How it works:
  1. We have transactions (orders) — each order has multiple products
  2. Apriori finds frequent itemsets: "mobile + charger bought together often"
  3. It generates association rules: IF mobile → THEN charger (confidence 80%)
  4. Rules are stored in DB table: association_rules
  5. Product detail page shows "Frequently Bought Together"

Run once to train:
    python apriori.py

Then it auto-runs when new orders come in (called from app.py).
"""

import sqlite3
import os
from itertools import combinations
from collections import defaultdict

DB = os.path.join(os.path.dirname(__file__), 'instance', 'ecommerce.db')


# ── STEP 1: CREATE TABLES ─────────────────────────────────────────────────────

def create_tables(conn):
    conn.executescript('''
        -- Synthetic transactions for training (manually defined product pairs)
        CREATE TABLE IF NOT EXISTS transactions (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            tx_id     INTEGER NOT NULL,
            product_id INTEGER NOT NULL
        );

        -- Mined association rules
        CREATE TABLE IF NOT EXISTS association_rules (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            antecedent_id INTEGER NOT NULL,   -- IF this product...
            consequent_id INTEGER NOT NULL,   -- THEN recommend this
            support       REAL NOT NULL,      -- how often both appear together
            confidence    REAL NOT NULL,      -- P(consequent | antecedent)
            lift          REAL NOT NULL,      -- confidence / P(consequent)
            UNIQUE(antecedent_id, consequent_id)
        );
    ''')
    conn.commit()


# ── STEP 2: SEED SYNTHETIC TRANSACTIONS ───────────────────────────────────────

def seed_transactions(conn):
    """
    Create realistic 'bought together' transaction data.
    Maps product names to IDs and builds transaction baskets.
    """
    existing = conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
    if existing > 0:
        print(f"  Transactions already seeded ({existing} rows). Skipping.")
        return

    # Fetch all products
    products = conn.execute("SELECT id, name, category FROM product").fetchall()
    if not products:
        print("  No products found. Run app.py first to seed products.")
        return

    # Build lookup: lowercase name keyword → product_id
    name_to_id = {}
    for p in products:
        name_to_id[p['name'].lower()] = p['id']

    # Build lookup by category
    cat_to_ids = defaultdict(list)
    for p in products:
        cat_to_ids[p['category']].append(p['id'])

    def find_id(keyword):
        """Find product ID by keyword in name"""
        for name, pid in name_to_id.items():
            if keyword.lower() in name:
                return pid
        return None

    # ── DEFINE TRANSACTION BASKETS ────────────────────────────────────────────
    # Format: list of (keyword1, keyword2, ...) — products bought together
    basket_templates = [

        # ── LAPTOP BUNDLES (most important for realistic recommendations)
        ("macbook air",    "laptop sleeve macbook"),       # laptop + sleeve/cover
        ("macbook air",    "usb-c 67w charger"),           # macbook + charger
        ("macbook air",    "usb-c hub"),           # macbook + hub
        ("macbook air",    "logitech mx master"),  # macbook + mouse
        ("macbook air",    "mx keys keyboard"),             # macbook + keyboard
        ("macbook air",    "laptop stand"),        # macbook + stand
        ("macbook air",    "sony wh"),             # macbook + headphones
        ("macbook air",    "airpods pro"),             # macbook + airpods
        ("macbook air",    "samsung t7"),          # macbook + SSD
        ("macbook air",    "logitech c920"),       # macbook + webcam

        ("dell xps",       "dell laptop bag"),          # dell laptop + bag
        ("dell xps",       "usb-c hub"),           # dell + hub
        ("dell xps",       "logitech mx master"),  # dell + mouse
        ("dell xps",       "mx keys keyboard"),             # dell + keyboard
        ("dell xps",       "laptop stand"),        # dell + stand
        ("dell xps",       "sony wh"),             # dell + headphones
        ("dell xps",       "samsung t7"),          # dell + SSD
        ("dell xps",       "logitech c920"),       # dell + webcam
        ("dell xps",       "anker powerbank"),           # dell + powerbank

        ("lenovo ideapad", "dell laptop bag"),          # lenovo + bag
        ("lenovo ideapad", "usb-c hub"),           # lenovo + hub
        ("lenovo ideapad", "logitech mx master"),  # lenovo + mouse
        ("lenovo ideapad", "mx keys keyboard"),             # lenovo + keyboard
        ("lenovo ideapad", "sony wh"),             # lenovo + headphones
        ("lenovo ideapad", "laptop stand"),        # lenovo + stand

        # ── PHONE BUNDLES
        ("iphone 15 pro",  "iphone 15 pro silicone"),       # iPhone + case
        ("iphone 15 pro",  "tempered glass"),      # iPhone + screen protector
        ("iphone 15 pro",  "anker wireless charger"),    # iPhone + wireless charger
        ("iphone 15 pro",  "anker powerbank"),           # iPhone + powerbank
        ("iphone 15 pro",  "airpods pro"),             # iPhone + AirPods
        ("iphone 15 pro",  "sony wh"),             # iPhone + headphones
        ("iphone 15 pro",  "usb-c 67w charger"),           # iPhone + charger

        ("samsung galaxy s24 ultra", "samsung galaxy s24 case"), # Samsung + case
        ("samsung galaxy s24 ultra", "tempered glass"),          # Samsung + glass
        ("samsung galaxy s24 ultra", "anker wireless charger"),        # Samsung + charger
        ("samsung galaxy s24 ultra", "anker powerbank"),               # Samsung + powerbank
        ("samsung galaxy s24 ultra", "sony wh"),                 # Samsung + headphones
        ("samsung galaxy s24 ultra", "airpods pro"),             # Samsung + buds

        ("oneplus 12",     "tempered glass"),      # OnePlus + glass
        ("oneplus 12",     "anker powerbank"),           # OnePlus + powerbank
        ("oneplus 12",     "anker wireless charger"),    # OnePlus + charger

        # ── TABLET BUNDLES
        ("ipad pro",       "usb-c hub"),        # iPad + pencil
        ("ipad pro",       "laptop sleeve macbook"),       # iPad + sleeve
        ("ipad pro",       "usb-c hub"),           # iPad + hub
        ("ipad pro",       "macbook air"),             # iPad + MacBook (Apple ecosystem)
        ("ipad pro",       "airpods pro"),             # iPad + AirPods
        ("ipad pro",       "anker wireless charger"),    # iPad + charger

        # ── AUDIO BUNDLES
        ("sony wh-1000xm5","jbl flip 6"),            # headphones + speaker
        ("airpods pro",    "anker wireless charger"),    # AirPods + charger
        ("airpods pro",    "iphone 15 pro"),           # AirPods + iPhone

        # ── DESK SETUP BUNDLE (very common)
        ("logitech mx master 3s", "logitech mx keys"),         # mouse + keyboard combo
        ("logitech mx master 3s", "laptop stand"),    # mouse + stand
        ("logitech mx keys",      "laptop stand"),    # keyboard + stand
        ("logitech c920",         "logitech mx keys"),         # webcam + keyboard (work from home)
        ("logitech c920",         "logitech mx master"), # webcam + mouse

        # ── FASHION COMBINATIONS
        ("nike air max",   "nike dri-fit t-shirt"),   # shoes + tshirt
        ("nike air max",   "nike dri-fit track"),       # shoes + track pants
        ("nike air max",   "nike crew socks"),  # shoes + socks
        ("nike air max 270","adidas backpack"),  # shoes + bag
        ("adidas ultraboost 23","nike crew socks"),# running shoes + socks
        ("adidas ultraboost 23","nike dri-fit t-shirt"), # running shoes + tshirt
        ("adidas ultraboost 23","adidas backpack"),# running shoes + bag
        ("levi's 501 original", "nike air max"),     # jeans + shoes
        ("levi's 501 original", "ray-ban aviator"),  # jeans + sunglasses
        ("levi's 501 original", "h&m oversized hoodie"),    # jeans + hoodie
        ("levis 501 original", "nike air max"),     # same combination
        ("ray-ban aviator", "fossil gen 6"),     # sunglasses + watch
        ("ray-ban aviator", "casio g-shock"),    # sunglasses + watch
        ("fossil gen 6",    "woodland leather"), # smartwatch + belt
        ("h&m oversized hoodie", "nike dri-fit t-shirt"),   # hoodie + tshirt
        ("adidas tiro track",   "adidas ultraboost"),# jacket + shoes
        ("nike dri-fit t-shirt","nike dri-fit track"),       # tshirt + pants
        ("adidas backpack",     "wildcraft trekking"),# bag + trekking shoes
        ("zara formal blazer",  "woodland leather"), # blazer + belt
        ("puma sports bag",     "reebok crossfit"),  # sports bag + shoes

        # ── HOME & KITCHEN COMBINATIONS
        ("instant pot",     "prestige non-stick"),  # pressure cooker + pans
        ("instant pot",     "philips air fryer"),   # combo kitchen appliances
        ("instant pot",     "hafele kitchen knife"),      # pressure cooker + knives
        ("philips air fryer xxl","philips hand blender"),# air fryer + blender
        ("philips air fryer xxl","hafele kitchen knife"),     # air fryer + knives
        ("dyson v15 detect","wipro smart led"),     # vacuum + smart lights
        ("dyson v15 detect","amazon echo dot"),         # vacuum + smart home
        ("ikea malm bed",   "duroflex dream"),            # bed frame + mattress
        ("ikea malm bed",   "bombay dyeing bedsheet"),       # bed frame + bedsheet
        ("ikea malm bed",   "solimo pillow"),       # bed frame + pillows
        ("duroflex dream",  "bombay dyeing bedsheet"),       # mattress + bedsheet
        ("bombay dyeing bedsheet","solimo pillow"),       # bedsheet + pillows
        ("ikea kallax",     "kuber industries storage"),    # shelf + storage boxes
        ("amazon echo dot", "wipro smart led"),     # smart speaker + smart lights
        ("pigeon mini induction","prestige non-stick"),  # induction + pans
        ("bosch electric kettle","hafele kitchen knife"),      # kettle + knives
        ("tupperware lunch box","milton thermosteel"),       # lunch box + flask
        ("godrej washing machine","dyson v15 detect"),           # washing machine + vacuum
        ("havells stand fan","wipro smart led"),     # fan + LED lights

        # ── BOOKS COMBINATIONS (readers buy series/similar)
        ("atomic habits",   "psychology of money"),
        ("atomic habits",   "deep work"),
        ("atomic habits",   "essentialism"),
        ("atomic habits",   "mindset"),
        ("psychology of money", "rich dad poor dad"),
        ("psychology of money", "think and grow rich"),
        ("deep work",       "zero to one"),
        ("deep work",       "4-hour workweek"),
        ("rich dad",        "think and grow rich"),
        ("rich dad",        "psychology of money"),
        ("the alchemist",   "power of now"),
        ("the alchemist",   "ikigai"),
        ("zero to one",     "lean startup"),
        ("zero to one",     "good to great"),
        ("lean startup",    "start with why"),
        ("sapiens",         "thinking fast"),
        ("can't hurt me",   "atomic habits"),
        ("how to win",      "start with why"),
        ("7 habits",        "how to win"),
        ("48 laws",         "art of war"),
        ("never split",     "how to win"),
        ("built to last",   "good to great"),

        # ── SPORTS COMBINATIONS (very realistic)
        ("yonex badminton racket","yonex badminton shuttlecock"),  # racket + shuttlecocks
        ("yonex badminton racket","decathlon badminton net"),      # racket + net
        ("yonex badminton racket","fitbit charge"),      # sports + tracker
        ("decathlon yoga mat","boldfit yoga block"), # yoga mat + blocks
        ("decathlon yoga mat","decathlon resistance"),# yoga mat + bands
        ("decathlon yoga mat","fitbit charge"),      # yoga + tracker
        ("decathlon yoga mat","boldfit skipping rope"),   # yoga mat + rope
        ("fitbit charge",    "garmin forerunner"),  # fitness trackers
        ("fitbit charge",   "nike training water"),# tracker + bottle
        ("fitbit charge",   "domyos gym gloves"),  # tracker + gym gloves
        ("cosco cricket bat","sg cricket helmet"),  # bat + helmet
        ("cosco cricket bat","nivia cricket batting"),       # bat + gloves
        ("cosco cricket bat","cosco cricket kit bag"),      # bat + kit bag
        ("sg cricket helmet","nivia cricket batting"),       # helmet + gloves
        ("nivia football",   "reebok crossfit shoes"),    # football + shoes
        ("domyos dumbbell",  "domyos gym gloves"),  # dumbbells + gloves
        ("domyos dumbbell",  "boldfit skipping rope"),   # dumbbells + rope
        ("domyos dumbbell", "nike training water"),# dumbbells + water bottle
        ("decathlon swimming goggles","arena swim cap"),     # goggles + cap
        ("garmin forerunner","nike training water"),# GPS watch + bottle
        ("wildcraft trekking shoes","wildcraft 40l trekking"),      # trekking shoes + backpack
        ("decathlon foam roller","decathlon resistance bands"),# foam roller + bands
        ("decathlon cycling helmet","garmin forerunner"),  # cycling helmet + GPS
        ("stag table tennis paddle","nivia football"),     # multi-sport buyer

        # ── CROSS-CATEGORY (Electronics + Sports/Others)
        ("fitbit charge 6",  "sony wh"),         # fitness + audio
        ("garmin forerunner","sony wh"),          # GPS watch + headphones
        ("garmin forerunner","wildcraft 40l"),    # GPS + backpack
        ("sony wh-1000xm5", "decathlon yoga mat"),  # headphones at gym
        ("airpods pro",      "decathlon yoga mat"),  # AirPods + yoga
        ("amazon echo dot",  "phillips led bulb"),     # smart home
        ("deep work - cal",  "macbook air"),         # productivity books + laptop
        ("atomic habits",    "fitbit charge"),   # habits + fitness
        ("atomic habits",    "garmin forerunner"),          # habits + fitness tracker

        # ── TRIPLE COMBOS (highest lift)
        ("macbook air",      "logitech mx master", "logitech mx keys"),
        ("macbook air",      "laptop sleeve macbook", "usb-c hub"),
        ("macbook air",      "sony wh",        "laptop stand"),
        ("iphone 15 pro",    "iphone 15 pro silicone", "tempered glass"),
        ("iphone 15 pro",    "airpods pro",    "anker wireless charger"),
        ("dell xps",         "logitech mx master", "dell laptop bag"),
        ("ikea malm",       "duroflex",           "bombay dyeing"),
        ("yonex badminton racket","yonex badminton shuttlecock","decathlon badminton net"),
        ("cosco cricket bat","sg cricket helmet","nivia cricket batting"),
        ("atomic habits",   "psychology of money","deep work"),
        ("levi's 501 original", "nike air max", "ray-ban aviator"),
        ("domyos dumbbell",  "domyos gym gloves", "boldfit skipping rope"),
        ("decathlon yoga mat","boldfit yoga block","decathlon resistance bands"),
    ]

    # Expand templates → actual product IDs
    transactions = []
    tx_id = 1

    for template in basket_templates:
        ids = [find_id(kw) for kw in template]
        ids = [i for i in ids if i is not None]  # remove not-found
        if len(ids) >= 2:
            # Repeat each pattern multiple times to boost support
            repeats = 12  # each pattern appears 12 times in data
            for _ in range(repeats):
                for pid in ids:
                    transactions.append((tx_id, pid))
                tx_id += 1

    # Also add real order data if exists
    real_orders = conn.execute("""
        SELECT order_id, product_id FROM order_item
    """).fetchall()
    for row in real_orders:
        transactions.append((row['order_id'] + 10000, row['product_id']))

    if not transactions:
        print("  No valid transactions could be built (check product names).")
        return

    conn.executemany(
        "INSERT INTO transactions (tx_id, product_id) VALUES (?,?)",
        transactions
    )
    conn.commit()
    print(f"  Seeded {len(transactions)} transaction rows across {tx_id-1} baskets.")


# ── STEP 3: APRIORI ALGORITHM ─────────────────────────────────────────────────

def apriori(transactions_list, min_support=0.01, min_confidence=0.3, min_lift=1.0):
    """
    Pure Python Apriori implementation.

    Args:
        transactions_list : list of sets, e.g. [{1,3,5}, {2,3}, ...]
        min_support       : minimum support threshold (0–1)
        min_confidence    : minimum confidence threshold (0–1)
        min_lift          : minimum lift threshold

    Returns:
        rules : list of (antecedent, consequent, support, confidence, lift)
    """
    n_transactions = len(transactions_list)
    if n_transactions == 0:
        return []

    # ── Count item frequencies ────────────────────────────────────────────────
    item_count = defaultdict(int)
    for tx in transactions_list:
        for item in tx:
            item_count[item] += 1

    # ── Frequent 1-itemsets ───────────────────────────────────────────────────
    freq_items = {
        frozenset([item]): count / n_transactions
        for item, count in item_count.items()
        if count / n_transactions >= min_support
    }

    if not freq_items:
        return []

    all_freq = dict(freq_items)
    current_freq = freq_items

    # ── Generate larger frequent itemsets ────────────────────────────────────
    k = 2
    while current_freq:
        # Get unique items from current frequent sets
        items = sorted(set(item for itemset in current_freq for item in itemset))
        candidates = {}

        # Generate candidate k-itemsets from (k-1)-itemsets
        for combo in combinations(items, k):
            candidate = frozenset(combo)
            # Pruning: all (k-1) subsets must be frequent
            all_subsets_frequent = all(
                frozenset(sub) in all_freq
                for sub in combinations(combo, k - 1)
            )
            if not all_subsets_frequent:
                continue
            # Count support
            count = sum(1 for tx in transactions_list if candidate.issubset(tx))
            support = count / n_transactions
            if support >= min_support:
                candidates[candidate] = support

        all_freq.update(candidates)
        current_freq = candidates
        k += 1
        if k > 4:  # limit to 4-itemsets max for performance
            break

    # ── Generate association rules ────────────────────────────────────────────
    rules = []
    for itemset, itemset_support in all_freq.items():
        if len(itemset) < 2:
            continue
        for size in range(1, len(itemset)):
            for antecedent in combinations(itemset, size):
                antecedent = frozenset(antecedent)
                consequent = itemset - antecedent
                if not consequent:
                    continue

                ant_support = all_freq.get(antecedent, 0)
                if ant_support == 0:
                    continue

                confidence = itemset_support / ant_support
                cons_support = all_freq.get(consequent, 0)
                lift = confidence / cons_support if cons_support > 0 else 0

                if confidence >= min_confidence and lift >= min_lift:
                    # Only store single-item consequents for simplicity
                    if len(consequent) == 1:
                        rules.append((
                            list(antecedent)[0] if len(antecedent) == 1 else tuple(sorted(antecedent)),
                            list(consequent)[0],
                            round(itemset_support, 4),
                            round(confidence, 4),
                            round(lift, 4)
                        ))

    return rules


# ── STEP 4: TRAIN AND STORE RULES ─────────────────────────────────────────────

def train_and_store(conn, min_support=0.01, min_confidence=0.25, min_lift=1.0):
    """Run Apriori on transactions table and save rules to association_rules."""

    # Load transactions from DB
    rows = conn.execute(
        "SELECT tx_id, product_id FROM transactions ORDER BY tx_id"
    ).fetchall()

    if not rows:
        print("  No transactions found to train on.")
        return 0

    # Group into baskets
    baskets = defaultdict(set)
    for row in rows:
        baskets[row['tx_id']].add(row['product_id'])

    transactions_list = list(baskets.values())
    print(f"  Training on {len(transactions_list)} transactions, {len(set(r['product_id'] for r in rows))} unique products...")

    # Run Apriori
    rules = apriori(transactions_list,
                    min_support=min_support,
                    min_confidence=min_confidence,
                    min_lift=min_lift)

    if not rules:
        print("  No rules found. Try lowering thresholds.")
        return 0

    # Clear old rules and insert new ones
    conn.execute("DELETE FROM association_rules")

    inserted = 0
    for rule in rules:
        ant, cons, support, confidence, lift = rule
        # Only store simple single-item antecedent rules
        if isinstance(ant, (int, float)):
            try:
                conn.execute(
                    """INSERT OR REPLACE INTO association_rules
                       (antecedent_id, consequent_id, support, confidence, lift)
                       VALUES (?,?,?,?,?)""",
                    (int(ant), int(cons), support, confidence, lift)
                )
                inserted += 1
            except Exception:
                pass

    conn.commit()
    print(f"  Stored {inserted} association rules.")
    return inserted


# ── STEP 5: GET RECOMMENDATIONS ───────────────────────────────────────────────

def get_recommendations(product_id, top_n=4, db_path=DB):
    """
    Given a product_id, return top N recommended products.
    Used in app.py product detail page.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    # Get rules where this product is the antecedent
    rules = conn.execute("""
        SELECT ar.consequent_id, ar.confidence, ar.lift, ar.support,
               p.id, p.name, p.price, p.original_price, p.image_url,
               p.brand, p.category, p.rating, p.reviews_count
        FROM association_rules ar
        JOIN product p ON ar.consequent_id = p.id
        WHERE ar.antecedent_id = ?
          AND ar.consequent_id != ?
        ORDER BY ar.lift DESC, ar.confidence DESC
        LIMIT ?
    """, (product_id, product_id, top_n)).fetchall()

    conn.close()
    return rules


def get_cart_recommendations(product_ids, top_n=4, db_path=DB):
    """
    Given a list of product_ids (cart), return recommendations
    excluding products already in cart.
    """
    if not product_ids:
        return []

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    placeholders = ','.join('?' * len(product_ids))
    rules = conn.execute(f"""
        SELECT ar.consequent_id, MAX(ar.confidence) as confidence,
               MAX(ar.lift) as lift,
               p.id, p.name, p.price, p.original_price,
               p.image_url, p.brand, p.category, p.rating
        FROM association_rules ar
        JOIN product p ON ar.consequent_id = p.id
        WHERE ar.antecedent_id IN ({placeholders})
          AND ar.consequent_id NOT IN ({placeholders})
        GROUP BY ar.consequent_id
        ORDER BY lift DESC, confidence DESC
        LIMIT ?
    """, product_ids + product_ids + [top_n]).fetchall()

    conn.close()
    return rules


# ── MAIN: RUN TRAINING ────────────────────────────────────────────────────────

def run_training():
    if not os.path.exists(DB):
        print("ERROR: Database not found. Run  python app.py  first.")
        return

    print("\n🔄 Apriori Recommendation Engine — Training")
    print("=" * 50)

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    print("\n[1/3] Creating tables...")
    create_tables(conn)

    print("\n[2/3] Seeding transaction data...")
    seed_transactions(conn)

    print("\n[3/3] Running Apriori algorithm...")
    count = train_and_store(conn, min_support=0.005, min_confidence=0.12, min_lift=1.5)

    # Show sample rules
    if count > 0:
        print("\n📊 Sample Association Rules Found:")
        print(f"  {'Antecedent':<35} {'Consequent':<35} {'Conf':>6} {'Lift':>6}")
        print(f"  {'-'*85}")
        sample = conn.execute("""
            SELECT p1.name as ant_name, p2.name as cons_name,
                   ar.confidence, ar.lift
            FROM association_rules ar
            JOIN product p1 ON ar.antecedent_id = p1.id
            JOIN product p2 ON ar.consequent_id = p2.id
            ORDER BY ar.lift DESC
            LIMIT 15
        """).fetchall()
        for r in sample:
            print(f"  {r['ant_name'][:33]:<35} {r['cons_name'][:33]:<35} {r['confidence']:>6.2f} {r['lift']:>6.2f}")

    conn.close()
    print(f"\n✅ Training complete! {count} rules ready.")
    print("   Restart app.py to see 'Frequently Bought Together' on product pages.\n")


if __name__ == '__main__':
    run_training()