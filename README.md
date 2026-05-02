# 🛒 ShopBlack — Full-Stack Flask E-Commerce

A complete Amazon/Flipkart-style e-commerce app built with Flask, SQLite, and Bootstrap.

---

## 🚀 Quick Start (VS Code)

### 1. Install Dependencies
```bash
cd ecommerce
pip install -r requirements.txt
```

### 2. Run the App
```bash
python app.py
```

### 3. Open in Browser
```
http://localhost:5000
```

The database is auto-created and seeded with 24 products on first run.

---

## ✅ Features

| Feature | Status |
|---|---|
| User Signup / Login | ✅ |
| Product Listing with Filters | ✅ |
| Product Detail Page | ✅ |
| Search with Suggestions | ✅ |
| Add to Cart | ✅ |
| Wishlist | ✅ |
| Checkout with Address | ✅ |
| Multiple Payment Methods | ✅ |
| Order Placement | ✅ |
| Order History | ✅ |
| Order Detail View | ✅ |
| User Profile Edit | ✅ |
| Recommended Products | ✅ |
| Responsive Design | ✅ |
| Category Browsing | ✅ |
| Sort & Filter | ✅ |
| Pagination | ✅ |

---

## 📁 Project Structure

```
ecommerce/
├── app.py                  # Main Flask app (models + routes)
├── requirements.txt
├── instance/
│   └── ecommerce.db        # SQLite DB (auto-created)
└── templates/
    ├── base.html           # Layout + navbar
    ├── index.html          # Homepage
    ├── products.html       # Product listing
    ├── product_detail.html # Product page
    ├── cart.html           # Shopping cart
    ├── checkout.html       # Checkout
    ├── order_success.html  # Order confirmation
    ├── orders.html         # Order history
    ├── order_detail.html   # Order details
    ├── wishlist.html       # Wishlist
    ├── login.html          # Login
    ├── signup.html         # Signup
    └── profile.html        # User profile
```

---

## 📊 Real Datasets (Free)

To expand the product catalog, use these real datasets:

### 1. Amazon Product Dataset (Kaggle)
- URL: https://www.kaggle.com/datasets/promptcloud/amazon-india-product-dataset-2020
- Format: CSV with product name, price, category, image URL, ratings
- How to use: Import with pandas, insert into Product model

### 2. Flipkart Product Dataset
- URL: https://www.kaggle.com/datasets/PromptCloudHQ/flipkart-products
- Format: CSV with ~20,000 products

### 3. BigBasket Products Dataset
- URL: https://www.kaggle.com/datasets/mkechinov/ecommerce-purchase-history-from-electronics-store
- Format: Electronics purchase data

### 4. Open Food Facts (for grocery)
- URL: https://world.openfoodfacts.org/data
- Format: CSV/JSON with 3M+ food products

### Import Script Example:
```python
import pandas as pd
from app import app, db, Product

df = pd.read_csv('amazon_products.csv')
with app.app_context():
    for _, row in df.iterrows():
        p = Product(
            name=row['product_name'],
            price=float(row['discounted_price'].replace('₹','').replace(',','')),
            original_price=float(row['actual_price'].replace('₹','').replace(',','')),
            category=row['category'].split('|')[0],
            brand=row.get('brand', 'Unknown'),
            image_url=row.get('img_link', ''),
            description=row.get('about_product', ''),
            rating=float(row.get('rating', 4.0)),
            reviews_count=int(row.get('rating_count', 0))
        )
        db.session.add(p)
    db.session.commit()
    print("Import complete!")
```

---

## 🎨 Tech Stack

- **Backend:** Flask 3.0, SQLAlchemy, Werkzeug
- **Frontend:** Bootstrap 5.3, Bootstrap Icons, Bebas Neue + DM Sans fonts
- **Database:** SQLite (can upgrade to PostgreSQL/MySQL)
- **Theme:** Black & White editorial design

---

## 🔧 Upgrade to PostgreSQL

```python
# In app.py, replace:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
# With:
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/shopblack'
```

Add `psycopg2-binary` to requirements.txt.