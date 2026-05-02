# """
# Run this once to fix all product images:
#     python fix_images.py
# """
# import sqlite3, os

# DB = os.path.join(os.path.dirname(__file__), 'instance', 'ecommerce.db')

# # Product name keyword → working image URL
# IMAGE_MAP = [
#     # Electronics
#     ("iphone",          "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=500&q=80"),
#     ("samsung galaxy",  "https://images.unsplash.com/photo-1610945264803-c22b62831f8a?w=500&q=80"),
#     ("sony wh",         "https://images.unsplash.com/photo-1578319439584-104c94d37305?w=500&q=80"),
#     ("macbook",         "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500&q=80"),
#     ("ipad",            "https://images.unsplash.com/photo-1561154464-82e9adf32764?w=500&q=80"),
#     ("dell xps",        "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500&q=80"),
#     ("jbl",             "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=500&q=80"),
#     ("logitech",        "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=500&q=80"),
#     # Fashion
#     ("nike",            "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&q=80"),
#     ("adidas",          "https://images.unsplash.com/photo-1518002054494-3a6f94352e9d?w=500&q=80"),
#     ("levi",            "https://images.unsplash.com/photo-1542272454315-4c01d7abdf4a?w=500&q=80"),
#     ("ray-ban",         "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=500&q=80"),
#     ("hoodie",          "https://images.unsplash.com/photo-1556821840-3a63f15732ce?w=500&q=80"),
#     ("fossil",          "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&q=80"),
#     # Home & Kitchen
#     ("instant pot",     "https://images.unsplash.com/photo-1585515320310-259814833e62?w=500&q=80"),
#     ("philips",         "https://images.unsplash.com/photo-1585515320310-259814833e62?w=500&q=80"),
#     ("dyson",           "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=500&q=80"),
#     ("ikea",            "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=500&q=80"),
#     # Books
#     ("atomic habits",   "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=500&q=80"),
#     ("psychology",      "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=500&q=80"),
#     ("deep work",       "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=500&q=80"),
#     # Sports
#     ("yonex",           "https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?w=500&q=80"),
#     ("yoga mat",        "https://images.unsplash.com/photo-1601925228239-03f1e7c5d15b?w=500&q=80"),
#     ("fitbit",          "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=500&q=80"),
# ]

# # Fallback images per category if no name match
# CATEGORY_FALLBACK = {
#     "Electronics":    "https://images.unsplash.com/photo-1468495244123-6c6c332eeece?w=500&q=80",
#     "Fashion":        "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=500&q=80",
#     "Home & Kitchen": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=500&q=80",
#     "Books":          "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=500&q=80",
#     "Sports":         "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=500&q=80",
# }

# def fix_images():
#     if not os.path.exists(DB):
#         print("ERROR: Database not found. Run  python app.py  first.")
#         return

#     conn = sqlite3.connect(DB)
#     conn.row_factory = sqlite3.Row
#     products = conn.execute("SELECT id, name, category FROM product").fetchall()

#     updated = 0
#     for p in products:
#         name_lower = p['name'].lower()
#         new_url = None

#         # Try name match first
#         for keyword, url in IMAGE_MAP:
#             if keyword.lower() in name_lower:
#                 new_url = url
#                 break

#         # Fallback to category image
#         if not new_url:
#             new_url = CATEGORY_FALLBACK.get(p['category'],
#                 "https://images.unsplash.com/photo-1472851294608-062f824d29cc?w=500&q=80")

#         conn.execute("UPDATE product SET image_url=? WHERE id=?", (new_url, p['id']))
#         print(f"  ✓ [{p['id']:>3}] {p['name'][:45]:<45} → image set")
#         updated += 1

#     conn.commit()
#     conn.close()
#     print(f"\n✅ Done! {updated} product images updated.")
#     print("   Restart app.py and refresh browser to see images.")

# if __name__ == '__main__':
#     fix_images()













import sqlite3, os

DB = os.path.join(os.path.dirname(__file__), 'instance', 'ecommerce.db')

IMAGE_MAP = [
    ("iphone",          "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=500&q=80"),
    ("samsung galaxy",  "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=500&q=80"),
    ("sony wh",         "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&q=80"),
    ("macbook",         "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500&q=80"),
    ("ipad",            "https://images.unsplash.com/photo-1561154464-82e9adf32764?w=500&q=80"),
    ("dell xps",        "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500&q=80"),
    ("jbl",             "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=500&q=80"),
    ("logitech",        "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=500&q=80"),
    ("nike",            "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&q=80"),
    ("adidas",          "https://images.unsplash.com/photo-1508609349937-5ec4ae374ebf?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8YWRpZGFzJTIwdWx0cmFib29zdCUyMDIzfGVufDB8fDB8fHww"),
    ("levi",            "https://images.unsplash.com/photo-1542272454315-4c01d7abdf4a?w=500&q=80"),
    ("ray-ban",         "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=500&q=80"),
    ("hoodie",          "https://images.unsplash.com/photo-1565608726736-3f280c8f7bb1?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjB8fGhvb2RpZSUyMG92ZXJzaXplZHxlbnwwfHwwfHx8MA%3D%3D"),
    ("fossil",          "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&q=80"),
    ("instant pot",     "https://m.media-amazon.com/images/I/71znyBH3HeL._AC_UY327_FMwebp_QL65_.jpg"),
    ("philips",         "https://media.istockphoto.com/id/2204596709/photo/woman-cooking-healthy-food-in-the-modern-air-fryer.jpg?s=612x612&w=0&k=20&c=RoAFEcR3l1lKVDp6UT2ZLIrEv4dpVSJeKzT2Lzqj2Wg="),
    ("dyson",           "https://m.media-amazon.com/images/I/41Rvda0M1wL._AC_UY327_FMwebp_QL65_.jpg"),
    ("ikea",            "https://m.media-amazon.com/images/I/61tu79uUb+L._AC_UL480_FMwebp_QL65_.jpg"),
    ("atomic habits",   "https://m.media-amazon.com/images/I/619vrpstWlL._SY385_.jpg"),
    ("psychology",      "https://images.unsplash.com/photo-1592496431122-2349e0fbc666?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8VGhlJTIwUHN5Y2hvbG9neSUyMG9mJTIwTW9uZXl8ZW58MHx8MHx8fDA%3D"),
    ("deep work",       "https://images.unsplash.com/photo-1711185895262-f14ad4d4eeac?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8RGVlcCUyMFdvcmslMjAtJTIwQ2FsJTIwTmV3cG9ydHxlbnwwfHwwfHx8MA%3D%3D"),
    ("yonex",           "https://images.unsplash.com/photo-1734459553318-1cde555f3c17?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8WW9uZXglMjBCYWRtaW50b24lMjBSYWNrZXR8ZW58MHx8MHx8fDA%3D"),
    ("yoga mat",        "https://m.media-amazon.com/images/I/71mInNZP1UL._SX679_.jpg"),
    ("fitbit",          "https://plus.unsplash.com/premium_photo-1711043989409-2b24e127d61f?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8Rml0Yml0JTIwQ2hhcmdlJTIwNnxlbnwwfHwwfHx8MA%3D%3D"),
]

CATEGORY_FALLBACK = {
    "Electronics":    "https://images.unsplash.com/photo-1468495244123-6c6c332eeece?w=500&q=80",
    "Fashion":        "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=500&q=80",
    "Home & Kitchen": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=500&q=80",
    "Books":          "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=500&q=80",
    "Sports":         "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=500&q=80",
}

def fix_images():
    if not os.path.exists(DB):
        print("ERROR: Database not found. Run  python app.py  first.")
        return

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    products = conn.execute("SELECT id, name, category FROM product").fetchall()

    updated = 0
    for p in products:
        name_lower = p['name'].lower()
        new_url = None

        for keyword, url in IMAGE_MAP:
            if keyword.lower() in name_lower:
                new_url = url
                break

        if not new_url:
            new_url = CATEGORY_FALLBACK.get(p['category'],
                "https://images.unsplash.com/photo-1472851294608-062f824d29cc?w=500&q=80")

        conn.execute("UPDATE product SET image_url=? WHERE id=?", (new_url, p['id']))
        print(f"  ✓ [{p['id']:>3}] {p['name'][:45]:<45} → image set")
        updated += 1

    conn.commit()
    conn.close()
    print(f"\n✅ Done! {updated} product images updated.")
    print("   Restart app.py and refresh browser to see images.")

if __name__ == '__main__':
    fix_images()