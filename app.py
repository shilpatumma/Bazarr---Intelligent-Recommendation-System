from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, g
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from apriori import get_recommendations, get_cart_recommendations
import json, os, csv
import sqlite3, os
from email_service import send_welcome_email, send_login_alert_email, send_order_confirmation_email

app = Flask(__name__)
# Use env variable in production, fallback for local dev

app.secret_key = os.environ.get('SECRET_KEY', 'shopblack-secret-key-2025')
# In production (Render), use /tmp for writable storage
if os.environ.get('RENDER'):
    DATABASE = '/tmp/ecommerce.db'
else:
    DATABASE = os.path.join(os.path.dirname(__file__), 'instance', 'ecommerce.db')
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
if os.environ.get('RENDER'):
    UPLOAD_FOLDER = '/tmp/profile_pics'
else:
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'profile_pics')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db: db.close()

def query(sql, args=(), one=False):
    cur = get_db().execute(sql, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv

def execute(sql, args=()):
    db = get_db()
    cur = db.execute(sql, args)
    db.commit()
    return cur.lastrowid

def init_db():
    db = sqlite3.connect(DATABASE)
    db.executescript('''
        CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, password TEXT NOT NULL, phone TEXT DEFAULT '', address TEXT DEFAULT '', profile_pic TEXT DEFAULT '', created_at TEXT DEFAULT (datetime('now')));
        CREATE TABLE IF NOT EXISTS product (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, description TEXT, price REAL NOT NULL, original_price REAL, category TEXT, brand TEXT, image_url TEXT, stock INTEGER DEFAULT 100, rating REAL DEFAULT 4.0, reviews_count INTEGER DEFAULT 0, is_featured INTEGER DEFAULT 0);
        CREATE TABLE IF NOT EXISTS cart_item (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, product_id INTEGER NOT NULL, quantity INTEGER DEFAULT 1);
        CREATE TABLE IF NOT EXISTS "order" (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, total_amount REAL NOT NULL, status TEXT DEFAULT 'Pending', payment_method TEXT, shipping_address TEXT, created_at TEXT DEFAULT (datetime('now')));
        CREATE TABLE IF NOT EXISTS order_item (id INTEGER PRIMARY KEY AUTOINCREMENT, order_id INTEGER NOT NULL, product_id INTEGER NOT NULL, quantity INTEGER NOT NULL, price REAL NOT NULL);
        CREATE TABLE IF NOT EXISTS wishlist (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, product_id INTEGER NOT NULL);
    ''')
    # Migration: add profile_pic if column missing in existing DB
    try:
        db.execute("ALTER TABLE user ADD COLUMN profile_pic TEXT DEFAULT ''")
        db.commit()
    except: pass
    count = db.execute("SELECT COUNT(*) FROM product").fetchone()[0]
    if count == 0:
        products = [
            ("Apple iPhone 15 Pro","Latest iPhone with A17 Pro chip, titanium design, and 48MP camera system.",99999,109999,"Electronics","Apple","https://images.unsplash.com/photo-1695048132575-5d1c1f57e1ad?w=400",100,4.8,2341,1),
            ("Samsung Galaxy S24 Ultra","Galaxy AI, 200MP camera, S Pen included. The ultimate Android flagship.",84999,94999,"Electronics","Samsung","https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=400",100,4.7,1876,1),
            ("Sony WH-1000XM5 Headphones","Industry-leading noise canceling headphones with 30hr battery life.",24999,29999,"Electronics","Sony","https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400",100,4.9,4521,1),
            ("MacBook Air M3","Supercharged by M3 chip. Thin, light, with all-day battery life.",114900,119900,"Electronics","Apple","https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?w=400",50,4.9,987,1),
            ("iPad Pro 12.9 inch","M4 chip, Liquid Retina XDR display, works with Apple Pencil Pro.",99900,109900,"Electronics","Apple","https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400",80,4.7,654,0),
            ("Dell XPS 15 Laptop","15.6-inch OLED display, Intel Core i9, 32GB RAM, RTX 4070.",149999,169999,"Electronics","Dell","https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=400",40,4.6,432,0),
            ("JBL Flip 6 Speaker","Portable Bluetooth speaker with 12 hours playtime, IP67 waterproof.",7999,9999,"Electronics","JBL","https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400",200,4.5,2134,0),
            ("Logitech MX Master 3S","Advanced wireless mouse, 8K DPI sensor, quiet click buttons.",8999,10999,"Electronics","Logitech","https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=400",150,4.8,3210,0),
            ("Nike Air Max 270","Men's lifestyle shoe with the biggest Air unit yet for all-day comfort.",9999,12999,"Fashion","Nike","https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",200,4.6,5432,1),
            ("Adidas Ultraboost 23","Running shoes with BOOST midsole and Primeknit+ upper for ultimate comfort.",14999,17999,"Fashion","Adidas","https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400",150,4.7,2876,0),
            ("Levi's 501 Original Jeans","The original straight fit. 100% cotton denim, timeless style.",3999,4999,"Fashion","Levi's","https://images.unsplash.com/photo-1542272454315-4c01d7abdf4a?w=400",300,4.4,8765,0),
            ("Ray-Ban Aviator Sunglasses","Classic pilot frame, 100% UV protection, gold metal frame.",6999,8999,"Fashion","Ray-Ban","https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400",100,4.6,1234,0),
            ("H&M Oversized Hoodie","Relaxed fit hoodie in soft cotton blend, perfect for casual wear.",1799,2299,"Fashion","H&M","https://images.unsplash.com/photo-1556821840-3a63f15732ce?w=400",400,4.2,3456,0),
            ("Fossil Gen 6 Smartwatch","Wear OS by Google smartwatch, heart rate monitor, GPS.",19999,24999,"Fashion","Fossil","https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400",80,4.3,876,0),
            ("Instant Pot Duo 7-in-1","Electric pressure cooker, slow cooker, rice cooker, steamer, and more.",6999,8999,"Home & Kitchen","Instant Pot","https://images.unsplash.com/photo-1585515320310-259814833e62?w=400",150,4.8,12453,1),
            ("Philips Air Fryer XXL","5.5L family-size air fryer. Cooks with 90% less fat.",12999,15999,"Home & Kitchen","Philips","https://images.unsplash.com/photo-1639831114716-1b2d55e7e6c1?w=400",100,4.6,5678,0),
            ("Dyson V15 Detect Vacuum","Laser-powered vacuum with intelligent auto-mode. 60min battery.",52900,59900,"Home & Kitchen","Dyson","https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400",50,4.7,987,0),
            ("IKEA MALM Bed Frame","Queen size bed frame with storage boxes. White finish.",18999,22999,"Home & Kitchen","IKEA","https://images.unsplash.com/photo-1505693314120-0d443867891c?w=400",60,4.3,2341,0),
            ("Atomic Habits - James Clear","Tiny changes, remarkable results. Build good habits and break bad ones.",399,599,"Books","Penguin","https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400",500,4.9,45678,1),
            ("The Psychology of Money","Timeless lessons on wealth, greed, and happiness by Morgan Housel.",349,499,"Books","Jaico","https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400",400,4.8,23456,0),
            ("Deep Work - Cal Newport","Rules for focused success in a distracted world.",299,449,"Books","Piatkus","https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=400",300,4.7,12345,0),
            ("Yonex Badminton Racket","Professional grade racket, carbon graphite, lightweight at 85g.",4999,6499,"Sports","Yonex","https://images.unsplash.com/photo-1613041720571-56d87aa2f9b1?w=400",120,4.6,1876,1),
            ("Decathlon Yoga Mat","Non-slip yoga mat, 5mm thick, 183x61cm, includes carry strap.",999,1499,"Sports","Decathlon","https://images.unsplash.com/photo-1601925228239-03f1e7c5d15b?w=400",300,4.5,6543,0),
            ("Fitbit Charge 6","Advanced fitness tracker, ECG app, built-in GPS, 7-day battery.",14999,17999,"Sports","Fitbit","https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=400",90,4.4,2109,0),
        ]
        db.executemany("INSERT INTO product (name,description,price,original_price,category,brand,image_url,stock,rating,reviews_count,is_featured) VALUES (?,?,?,?,?,?,?,?,?,?,?)", products)
        db.commit()
        print(f"Seeded {len(products)} products")
    db.close()

@app.context_processor
def inject_counts():
    cart_count = 0; wishlist_count = 0
    if session.get('user_id'):
        r = query("SELECT COUNT(*) as c FROM cart_item WHERE user_id=?", (session['user_id'],), one=True)
        cart_count = r['c'] if r else 0
        r2 = query("SELECT COUNT(*) as c FROM wishlist WHERE user_id=?", (session['user_id'],), one=True)
        wishlist_count = r2['c'] if r2 else 0
    return dict(cart_count=cart_count, wishlist_count=wishlist_count)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']; password = request.form['password']
        user = query("SELECT * FROM user WHERE email=?", (email,), one=True)
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']; session['user_name'] = user['name']
            # Send login alert email
            login_time = datetime.now().strftime('%d %b %Y at %I:%M %p')
            send_login_alert_email(user['email'], user['name'], login_time)
            flash('Welcome back, ' + user['name'] + '!', 'success')
            return redirect(url_for('index'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']; email = request.form['email']
        password = request.form['password']; phone = request.form.get('phone','')
        if query("SELECT id FROM user WHERE email=?", (email,), one=True):
            flash('Email already registered.', 'danger'); return redirect(url_for('signup'))
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        uid = execute("INSERT INTO user (name,email,password,phone,created_at) VALUES (?,?,?,?,?)", (name, email, generate_password_hash(password), phone, now))
        session['user_id'] = uid; session['user_name'] = name
        # Send welcome email (runs in background, won't slow down signup)
        joined = datetime.now().strftime('%d %b %Y')
        send_welcome_email(email, name, uid, joined)
        flash('Account created! Welcome, ' + name + '! Check your email 📧', 'success')
        return redirect(url_for('index'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear(); flash('Logged out successfully.', 'info'); return redirect(url_for('index'))

@app.route('/')
def index():
    featured = query("SELECT * FROM product WHERE is_featured=1 LIMIT 8")
    categories = [r['category'] for r in query("SELECT DISTINCT category FROM product")]
    new_arrivals = query("SELECT * FROM product ORDER BY id DESC LIMIT 8")
    best_sellers = query("SELECT * FROM product ORDER BY rating DESC LIMIT 8")
    return render_template('index.html', featured=featured, categories=categories, new_arrivals=new_arrivals, best_sellers=best_sellers)

@app.route('/products')
def products():
    page = request.args.get('page', 1, type=int); per_page = 12
    category = request.args.get('category',''); brand = request.args.get('brand','')
    search = request.args.get('search',''); sort = request.args.get('sort','default')
    min_price = request.args.get('min_price', 0, type=float); max_price = request.args.get('max_price', 9999999, type=float)
    conditions = ["price >= ?","price <= ?"]; params = [min_price, max_price]
    if category: conditions.append("category = ?"); params.append(category)
    if brand: conditions.append("brand = ?"); params.append(brand)
    if search: conditions.append("name LIKE ?"); params.append(f'%{search}%')
    where = " AND ".join(conditions)
    order_map = {'price_asc':'price ASC','price_desc':'price DESC','rating':'rating DESC','newest':'id DESC'}
    order_sql = order_map.get(sort, 'id ASC')
    total = query(f"SELECT COUNT(*) as c FROM product WHERE {where}", params, one=True)['c']
    offset = (page-1)*per_page
    items = query(f"SELECT * FROM product WHERE {where} ORDER BY {order_sql} LIMIT ? OFFSET ?", params+[per_page, offset])
    pages = (total+per_page-1)//per_page
    categories = [r['category'] for r in query("SELECT DISTINCT category FROM product")]
    # Show only brands that belong to selected category — if no category, show all
    if category:
        brands = [r['brand'] for r in query("SELECT DISTINCT brand FROM product WHERE category=? ORDER BY brand", (category,))]
    else:
        brands = [r['brand'] for r in query("SELECT DISTINCT brand FROM product ORDER BY brand")]
    class Pag:
        def __init__(self):
            self.page=page; self.pages=pages; self.total=total; self.items=items
            self.has_prev=page>1; self.has_next=page<pages; self.prev_num=page-1; self.next_num=page+1
        def iter_pages(self, left_edge=2, right_edge=2, left_current=2, right_current=2):
            last=0
            for num in range(1, pages+1):
                if num<=left_edge or (page-left_current-1<num<page+right_current) or num>pages-right_edge:
                    if last+1!=num: yield None
                    yield num; last=num
    return render_template('products.html', products=items, pagination=Pag(), categories=categories, brands=brands, current_category=category, current_brand=brand, search=search, sort=sort)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = query("SELECT * FROM product WHERE id=?", (product_id,), one=True)
    if not product: return redirect(url_for('products'))
    related = query("SELECT * FROM product WHERE category=? AND id!=? LIMIT 4", (product['category'], product_id))
    in_wishlist = False
    if session.get('user_id'):
        in_wishlist = query("SELECT id FROM wishlist WHERE user_id=? AND product_id=?", (session['user_id'], product_id), one=True) is not None
    # Apriori recommendations
    frequently_bought = get_recommendations(product_id, top_n=4, db_path=DATABASE)
    return render_template('product_detail.html', product=product, related=related,
                           in_wishlist=in_wishlist, frequently_bought=frequently_bought)

@app.route('/category/<category_name>')
def category(category_name):
    return redirect(url_for('products', category=category_name))

@app.route('/cart')
def cart():
    if 'user_id' not in session: flash('Please login to view cart.','warning'); return redirect(url_for('login'))
    items = query("SELECT ci.id, ci.quantity, p.id as product_id, p.name, p.price, p.original_price, p.brand, p.category, p.image_url FROM cart_item ci JOIN product p ON ci.product_id=p.id WHERE ci.user_id=?", (session['user_id'],))
    subtotal = sum(i['price']*i['quantity'] for i in items)
    shipping = 0 if subtotal>999 else 99
    # Apriori cart recommendations
    cart_product_ids = [i['product_id'] for i in items]
    cart_recommendations = get_cart_recommendations(cart_product_ids, top_n=4, db_path=DATABASE)
    return render_template('cart.html', items=items, subtotal=subtotal, shipping=shipping,
                           total=subtotal+shipping, cart_recommendations=cart_recommendations)

@app.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'user_id' not in session: return jsonify({'status':'error','message':'Please login first'})
    qty = int(request.form.get('quantity',1))
    existing = query("SELECT id,quantity FROM cart_item WHERE user_id=? AND product_id=?", (session['user_id'], product_id), one=True)
    if existing: execute("UPDATE cart_item SET quantity=? WHERE id=?", (existing['quantity']+qty, existing['id']))
    else: execute("INSERT INTO cart_item (user_id,product_id,quantity) VALUES (?,?,?)", (session['user_id'], product_id, qty))
    count = query("SELECT COUNT(*) as c FROM cart_item WHERE user_id=?", (session['user_id'],), one=True)['c']
    return jsonify({'status':'success','message':'Added to cart!','count':count})

@app.route('/cart/update/<int:item_id>', methods=['POST'])
def update_cart(item_id):
    if 'user_id' not in session: return redirect(url_for('login'))
    qty = int(request.form.get('quantity',1))
    if qty<=0: execute("DELETE FROM cart_item WHERE id=?", (item_id,))
    else: execute("UPDATE cart_item SET quantity=? WHERE id=?", (qty, item_id))
    return redirect(url_for('cart'))

@app.route('/cart/remove/<int:item_id>')
def remove_from_cart(item_id):
    if 'user_id' not in session: return redirect(url_for('login'))
    execute("DELETE FROM cart_item WHERE id=?", (item_id,))
    flash('Item removed.','info'); return redirect(url_for('cart'))

@app.route('/wishlist')
def wishlist():
    if 'user_id' not in session: flash('Please login.','warning'); return redirect(url_for('login'))
    items = query("SELECT w.id, p.id as product_id, p.name, p.price, p.original_price, p.brand, p.image_url, p.rating, p.reviews_count FROM wishlist w JOIN product p ON w.product_id=p.id WHERE w.user_id=?", (session['user_id'],))
    return render_template('wishlist.html', items=items)

@app.route('/wishlist/toggle/<int:product_id>', methods=['POST'])
def toggle_wishlist(product_id):
    if 'user_id' not in session: return jsonify({'status':'error','message':'Please login first'})
    existing = query("SELECT id FROM wishlist WHERE user_id=? AND product_id=?", (session['user_id'], product_id), one=True)
    if existing:
        execute("DELETE FROM wishlist WHERE id=?", (existing['id'],))
        return jsonify({'status':'removed','message':'Removed from wishlist'})
    execute("INSERT INTO wishlist (user_id,product_id) VALUES (?,?)", (session['user_id'], product_id))
    return jsonify({'status':'added','message':'Added to wishlist'})

@app.route('/checkout', methods=['GET','POST'])
def checkout():
    if 'user_id' not in session: flash('Please login.','warning'); return redirect(url_for('login'))
    items = query("SELECT ci.id, ci.quantity, p.id as product_id, p.name, p.price, p.original_price, p.brand, p.image_url FROM cart_item ci JOIN product p ON ci.product_id=p.id WHERE ci.user_id=?", (session['user_id'],))
    if not items: flash('Cart is empty.','warning'); return redirect(url_for('cart'))
    subtotal = sum(i['price']*i['quantity'] for i in items)
    shipping = 0 if subtotal>999 else 99; total = subtotal+shipping
    user = query("SELECT * FROM user WHERE id=?", (session['user_id'],), one=True)
    if not user:
        session.clear(); flash('Session expired. Please login again.','warning'); return redirect(url_for('login'))
    if request.method == 'POST':
        address = request.form.get('address',''); payment = request.form.get('payment_method','COD')
        oid = execute('INSERT INTO "order" (user_id,total_amount,payment_method,shipping_address) VALUES (?,?,?,?)', (session['user_id'], total, payment, address))
        for item in items:
            execute("INSERT INTO order_item (order_id,product_id,quantity,price) VALUES (?,?,?,?)", (oid, item['product_id'], item['quantity'], item['price']))
        execute("DELETE FROM cart_item WHERE user_id=?", (session['user_id'],))
        # Send order confirmation email
        email_items = [{'name': i['name'], 'qty': i['quantity'], 'price': i['price'] * i['quantity']} for i in items]
        send_order_confirmation_email(user['email'], user['name'], oid, email_items, total, address)
        flash('Order placed! 🎉 Check your email for confirmation.','success')
        return redirect(url_for('order_success', order_id=oid))
    return render_template('checkout.html', items=items, subtotal=subtotal, shipping=shipping, total=total, user=user)

@app.route('/order/success/<int:order_id>')
def order_success(order_id):
    order = query('SELECT * FROM "order" WHERE id=?', (order_id,), one=True)
    return render_template('order_success.html', order=order)

@app.route('/orders')
def orders():
    if 'user_id' not in session: return redirect(url_for('login'))
    user_orders = query('SELECT * FROM "order" WHERE user_id=? ORDER BY created_at DESC', (session['user_id'],))
    orders_with_items = []
    for o in user_orders:
        its = query("SELECT oi.*, p.name, p.image_url, p.brand FROM order_item oi JOIN product p ON oi.product_id=p.id WHERE oi.order_id=?", (o['id'],))
        orders_with_items.append({'order':o,'items':its})
    return render_template('orders.html', orders_with_items=orders_with_items)

@app.route('/order/<int:order_id>')
def order_detail(order_id):
    order = query('SELECT * FROM "order" WHERE id=?', (order_id,), one=True)
    items = query("SELECT oi.*, p.name, p.image_url, p.brand FROM order_item oi JOIN product p ON oi.product_id=p.id WHERE oi.order_id=?", (order_id,))
    return render_template('order_detail.html', order=order, items=items)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/profile', methods=['GET','POST'])
def profile():
    if 'user_id' not in session: return redirect(url_for('login'))
    user = query("SELECT * FROM user WHERE id=?", (session['user_id'],), one=True)
    if not user:
        session.clear()
        flash('Session expired. Please login again.', 'warning')
        return redirect(url_for('login'))
    order_count = query('SELECT COUNT(*) as c FROM "order" WHERE user_id=?', (session['user_id'],), one=True)['c']
    if request.method == 'POST':
        name    = request.form.get('name', user['name'])
        phone   = request.form.get('phone', '')
        address = request.form.get('address', '')
        profile_pic = user['profile_pic'] or ''

        # Handle profile picture upload
        file = request.files.get('profile_pic')
        if file and file.filename and allowed_file(file.filename):
            try:
                # Make sure folder exists on THIS machine
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                ext = file.filename.rsplit('.', 1)[1].lower()
                filename = f"user_{session['user_id']}.{ext}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                profile_pic = filename
                flash('Profile picture updated!', 'success')
            except Exception as e:
                flash(f'Image upload failed: {str(e)}', 'danger')
        elif file and file.filename and not allowed_file(file.filename):
            flash('Invalid file type. Use JPG, PNG, GIF or WEBP.', 'danger')

        try:
            execute("UPDATE user SET name=?,phone=?,address=?,profile_pic=? WHERE id=?",
                    (name, phone, address, profile_pic, session['user_id']))
            session['user_name'] = name
            flash('Profile updated successfully!', 'success')
        except Exception as e:
            # profile_pic column might be missing — run migration
            try:
                get_db().execute("ALTER TABLE user ADD COLUMN profile_pic TEXT DEFAULT ''")
                get_db().commit()
                execute("UPDATE user SET name=?,phone=?,address=?,profile_pic=? WHERE id=?",
                        (name, phone, address, profile_pic, session['user_id']))
                session['user_name'] = name
                flash('Profile updated successfully!', 'success')
            except Exception as e2:
                flash(f'Update failed: {str(e2)}', 'danger')
        return redirect(url_for('profile'))
    return render_template('profile.html', user=user, order_count=order_count)

@app.route('/profile/pic/<filename>')
def profile_pic(filename):
    from flask import send_from_directory
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/search')
def search():
    return redirect(url_for('products', search=request.args.get('q','')))

@app.route('/api/search-suggestions')
def search_suggestions():
    q = request.args.get('q','')
    if len(q)<2: return jsonify([])
    results = query("SELECT id, name, price, image_url FROM product WHERE name LIKE ? LIMIT 5", (f'%{q}%',))
    return jsonify([{'id':r['id'],'name':r['name'],'price':r['price'],'image':r['image_url']} for r in results])

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)