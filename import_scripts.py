import csv, re, sqlite3, os, sys
 
DB = os.path.join(os.path.dirname(__file__), 'instance', 'ecommerce.db')
 
 
def clean_price(val):
    """Remove ₹ and commas, return float or None"""
    if not val:
        return None
    cleaned = re.sub(r'[₹,\s]', '', str(val))
    try:
        return float(cleaned)
    except ValueError:
        return None
 
 
def clean_rating(val):
    try:
        r = float(str(val).strip())
        return min(max(r, 0), 5)
    except:
        return 4.0
 
 
def clean_count(val):
    try:
        return int(re.sub(r'[,\s]', '', str(val)))
    except:
        return 0
 
 
def extract_category(cat_str):
    """'Computers&Accessories|Peripherals|Cables' → 'Electronics'"""
    if not cat_str:
        return 'General'
    first = cat_str.split('|')[0].strip()
    mapping = {
        'Computers': 'Electronics', 'Electronics': 'Electronics',
        'Home': 'Home & Kitchen', 'Kitchen': 'Home & Kitchen',
        'Office': 'Home & Kitchen', 'Toys': 'Sports',
        'Sports': 'Sports', 'Books': 'Books',
        'Clothing': 'Fashion', 'Shoes': 'Fashion', 'Fashion': 'Fashion',
        'Health': 'Sports', 'Beauty': 'Fashion',
        'Car': 'Electronics', 'Musical': 'Electronics',
    }
    for key, mapped in mapping.items():
        if key.lower() in first.lower():
            return mapped
    return first[:50]  # Use raw if no mapping found
 
 
def import_amazon(csv_file='amazon.csv'):
    if not os.path.exists(csv_file):
        print(f"ERROR: File '{csv_file}' not found.")
        print("Download from: https://www.kaggle.com/datasets/karkavelrajaj/amazon-sales-dataset")
        sys.exit(1)
 
    conn = sqlite3.connect(DB)
    inserted = 0
    skipped = 0
 
    with open(csv_file, encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('product_name', '').strip()
            if not name:
                skipped += 1
                continue
 
            price = clean_price(row.get('discounted_price', ''))
            orig_price = clean_price(row.get('actual_price', ''))
            if not price:
                skipped += 1
                continue
 
            category = extract_category(row.get('category', ''))
            description = row.get('about_product', '')[:500]
            rating = clean_rating(row.get('rating', 4.0))
            reviews_count = clean_count(row.get('rating_count', 0))
            image_url = row.get('img_link', '').strip()
 
            # Extract brand from product name (first word usually)
            brand = name.split()[0] if name else 'Unknown'
 
            conn.execute(
                """INSERT INTO product
                   (name, description, price, original_price, category, brand,
                    image_url, stock, rating, reviews_count, is_featured)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                (name[:200], description, price, orig_price, category, brand[:100],
                 image_url[:500], 100, rating, reviews_count, 0)
            )
            inserted += 1
 
    conn.commit()
    conn.close()
    print(f"✅ Amazon import done: {inserted} products added, {skipped} skipped.")
 