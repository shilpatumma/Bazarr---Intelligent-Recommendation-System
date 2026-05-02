"""
add_products.py — Add 25 products per category (125 total)
Run once: python add_products.py
"""
import sqlite3, os

DB = os.path.join(os.path.dirname(__file__), 'instance', 'ecommerce.db')

def add_products():
    conn = sqlite3.connect(DB)
    
    # Check existing count
    existing = conn.execute("SELECT COUNT(*) FROM product").fetchone()[0]
    print(f"Existing products: {existing}")

    # All 125 products — 25 per category
    # Format: (name, description, price, original_price, category, brand, image_url, stock, rating, reviews, featured)
    products = [

        # ══════════════════════════════════════════════════════════
        # ELECTRONICS — 25 products
        # ══════════════════════════════════════════════════════════
        # Main devices
        ("Apple iPhone 15 Pro","Latest iPhone with A17 Pro chip, titanium design, and 48MP camera system.",99999,109999,"Electronics","Apple","https://images.unsplash.com/photo-1695048132575-5d1c1f57e1ad?w=400",100,4.8,2341,1),
        ("Samsung Galaxy S24 Ultra","Galaxy AI, 200MP camera, S Pen included. The ultimate Android flagship.",84999,94999,"Electronics","Samsung","https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=400",100,4.7,1876,1),
        ("OnePlus 12 5G","Snapdragon 8 Gen 3, 50MP Hasselblad camera, 100W SUPERVOOC charging.",64999,69999,"Electronics","OnePlus","https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=400",120,4.6,987,0),
        ("MacBook Air M3","Supercharged by M3 chip. Thin, light, with all-day battery life.",114900,119900,"Electronics","Apple","https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?w=400",50,4.9,987,1),
        ("Dell XPS 15 Laptop","15.6-inch OLED display, Intel Core i9, 32GB RAM, RTX 4070.",149999,169999,"Electronics","Dell","https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=400",40,4.6,432,0),
        ("Lenovo IdeaPad Slim 5","Intel Core i7, 16GB RAM, 512GB SSD, 15.6-inch FHD display.",62999,72999,"Electronics","Lenovo","https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=400",80,4.4,765,0),
        ("iPad Pro 12.9 inch","M4 chip, Liquid Retina XDR display, works with Apple Pencil Pro.",99900,109900,"Electronics","Apple","https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400",80,4.7,654,0),
        ("Samsung 65-inch QLED TV","4K QLED, Quantum HDR, 120Hz, built-in Alexa.",89999,109999,"Electronics","Samsung","https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=400",30,4.7,543,1),

        # Laptop Accessories
        ("Apple USB-C 67W Charger","Original MagSafe fast charger, compatible with MacBook Air/Pro.",4999,5999,"Electronics","Apple","https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=400",300,4.8,3210,0),
        ("Dell Laptop Bag 15.6 inch","Water-resistant laptop bag, multiple compartments, padded sleeve.",2499,3499,"Electronics","Dell","https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400",250,4.5,1876,0),
        ("Laptop Sleeve MacBook 14 inch","Neoprene sleeve, shockproof, fits MacBook 13-14 inch, slim profile.",1299,1999,"Electronics","Inateck","https://images.unsplash.com/photo-1491553895911-0055eca6402d?w=400",400,4.4,2134,0),
        ("USB-C Hub 7-in-1","Multiport adapter: HDMI 4K, 3x USB 3.0, SD card, USB-C PD 100W.",3499,4999,"Electronics","Anker","https://images.unsplash.com/photo-1625895197185-efcec01cffe0?w=400",200,4.6,1543,0),
        ("Laptop Stand Aluminium","Adjustable aluminium stand, ergonomic angle, compatible with all laptops.",2999,3999,"Electronics","Twelve South","https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400",180,4.7,987,0),
        ("Anker PowerBank 20000mAh","20000mAh power bank, 65W PD, dual USB-A + USB-C ports.",3999,5499,"Electronics","Anker","https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=400",300,4.7,4532,0),

        # Phone Accessories
        ("iPhone 15 Pro Silicone Case","Official Apple silicone case, MagSafe compatible, all colors.",3999,4499,"Electronics","Apple","https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=400",500,4.5,5678,0),
        ("Samsung Galaxy S24 Case","Official Samsung clear case, military-grade drop protection.",2499,2999,"Electronics","Samsung","https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=400",500,4.4,2341,0),
        ("Tempered Glass Screen Protector","9H hardness, 99% clarity, anti-fingerprint, fits iPhone 15 Pro.",499,799,"Electronics","Belkin","https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=400",800,4.3,8765,0),
        ("Anker Wireless Charger Pad","15W fast wireless charger, compatible with iPhone/Samsung/AirPods.",1999,2999,"Electronics","Anker","https://images.unsplash.com/photo-1591370874773-6702e8f12fd8?w=400",400,4.5,3456,0),

        # Audio & Input
        ("Sony WH-1000XM5 Headphones","Industry-leading noise canceling headphones with 30hr battery life.",24999,29999,"Electronics","Sony","https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400",100,4.9,4521,1),
        ("Apple AirPods Pro 2nd Gen","Active noise cancellation, Adaptive Audio, H2 chip, MagSafe charging.",24999,27999,"Electronics","Apple","https://images.unsplash.com/photo-1639747280804-dd2d6b3d88ac?w=400",150,4.8,6789,1),
        ("JBL Flip 6 Speaker","Portable Bluetooth speaker with 12 hours playtime, IP67 waterproof.",7999,9999,"Electronics","JBL","https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400",200,4.5,2134,0),
        ("Logitech MX Master 3S","Advanced wireless mouse, 8K DPI sensor, quiet click buttons.",8999,10999,"Electronics","Logitech","https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=400",150,4.8,3210,0),
        ("Logitech MX Keys Keyboard","Advanced wireless keyboard, backlit, multi-device, scissor switches.",9999,12999,"Electronics","Logitech","https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400",120,4.7,2109,0),
        ("Samsung T7 Portable SSD","1TB portable SSD, USB 3.2 Gen 2, 1050MB/s read, fingerprint lock.",8999,11999,"Electronics","Samsung","https://images.unsplash.com/photo-1597149305323-4fd6a91f1d8e?w=400",100,4.8,3456,0),
        ("Logitech C920 HD Webcam","1080p HD webcam, autofocus, built-in mic, plug and play.",6999,8999,"Electronics","Logitech","https://images.unsplash.com/photo-1587826080692-f439cd0b70da?w=400",150,4.6,1987,0),


        # ══════════════════════════════════════════════════════════
        # FASHION — 25 products
        # ══════════════════════════════════════════════════════════
        # Shoes
        ("Nike Air Max 270","Men's lifestyle shoe with the biggest Air unit yet for all-day comfort.",9999,12999,"Fashion","Nike","https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",200,4.6,5432,1),
        ("Adidas Ultraboost 23","Running shoes with BOOST midsole and Primeknit+ upper.",14999,17999,"Fashion","Adidas","https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400",150,4.7,2876,0),
        ("Nike Revolution 7","Lightweight running shoes, foam midsole, breathable mesh upper.",4999,6499,"Fashion","Nike","https://images.unsplash.com/photo-1607522370275-f14206abe5d3?w=400",300,4.4,4321,0),
        ("Puma RS-X","Bold chunky sneakers with retro running DNA, cushioned sole.",7999,9999,"Fashion","Puma","https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400",180,4.3,1876,0),
        ("Adidas Samba OG","Classic leather sneakers, suede overlays, timeless street style.",8999,10999,"Fashion","Adidas","https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",150,4.7,3456,0),

        # Bottoms
        ("Levis 501 Original Jeans","The original straight fit. 100% cotton denim, timeless style.",3999,4999,"Fashion","Levi's","https://images.unsplash.com/photo-1542272454315-4c01d7abdf4a?w=400",300,4.4,8765,0),
        ("Nike Dri-FIT Track Pants","Sweat-wicking fabric, tapered fit, zip pockets, athletic wear.",3499,4499,"Fashion","Nike","https://images.unsplash.com/photo-1584370848010-d7fe6bc767ec?w=400",250,4.5,2345,0),
        ("Zara Straight Chinos","Slim straight chinos, cotton blend, multiple colors available.",2999,3999,"Fashion","Zara","https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=400",300,4.2,1234,0),

        # Tops & Outerwear
        ("H&M Oversized Hoodie","Relaxed fit hoodie in soft cotton blend, perfect for casual wear.",1799,2299,"Fashion","H&M","https://images.unsplash.com/photo-1556821840-3a63f15732ce?w=400",400,4.2,3456,0),
        ("Nike Dri-FIT T-Shirt","Moisture-wicking performance tee, lightweight, athletic fit.",1299,1799,"Fashion","Nike","https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400",500,4.5,6789,0),
        ("Adidas Tiro Track Jacket","Slim fit training jacket, moisture-absorbing AEROREADY fabric.",4999,6499,"Fashion","Adidas","https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=400",200,4.4,1987,0),
        ("Levis Trucker Jacket","Classic denim jacket, rigid denim, chest pockets, timeless cut.",5999,7499,"Fashion","Levi's","https://images.unsplash.com/photo-1551537482-f2075a1d41f2?w=400",150,4.5,2109,0),
        ("Zara Formal Blazer","Slim-fit blazer, soft structure, notch lapel, two-button closure.",4999,6999,"Fashion","Zara","https://images.unsplash.com/photo-1593030761757-71fae45fa0e7?w=400",120,4.3,876,0),

        # Accessories
        ("Ray-Ban Aviator Sunglasses","Classic pilot frame, 100% UV protection, gold metal frame.",6999,8999,"Fashion","Ray-Ban","https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400",100,4.6,1234,0),
        ("Ray-Ban Wayfarer","Iconic acetate frame, polarized lenses, UV400 protection.",7499,9499,"Fashion","Ray-Ban","https://images.unsplash.com/photo-1577803645773-f96470509666?w=400",100,4.6,987,0),
        ("Fossil Gen 6 Smartwatch","Wear OS, heart rate monitor, GPS, 3-day battery.",19999,24999,"Fashion","Fossil","https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400",80,4.3,876,0),
        ("Casio G-Shock GA-2100","Carbon core guard, shock/water resistant, analog-digital, 200M WR.",8999,10999,"Fashion","Casio","https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400",120,4.7,2345,0),
        ("Nike Sports Cap","Dri-FIT technology, adjustable strap, embroidered Swoosh logo.",1299,1699,"Fashion","Nike","https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=400",400,4.3,4567,0),
        ("Adidas Backpack","25L capacity, padded laptop sleeve, water-resistant, 3-Stripes.",3499,4499,"Fashion","Adidas","https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400",200,4.5,2134,0),
        ("Nike Crew Socks 3-Pack","Cushioned crew socks, moisture-wicking, arch support, 3 pairs.",799,999,"Fashion","Nike","https://images.unsplash.com/photo-1586350977771-b3b0abd50c82?w=400",800,4.4,8901,0),
        ("Puma Sports Bag","25L gym bag, ventilated shoe compartment, water-resistant.",2499,3199,"Fashion","Puma","https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400",200,4.4,1543,0),
        ("H&M Cotton T-Shirt 2-Pack","Essential crew-neck tees, 100% cotton, slim fit, pack of 2.",999,1299,"Fashion","H&M","https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400",600,4.1,5678,0),
        ("Wildcraft Trekking Shoes","Waterproof hiking shoes, grip sole, ankle support, lightweight.",5999,7999,"Fashion","Wildcraft","https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",150,4.4,987,0),


        # ══════════════════════════════════════════════════════════
        # HOME & KITCHEN — 25 products
        # ══════════════════════════════════════════════════════════
        ("Instant Pot Duo 7-in-1","Electric pressure cooker, slow cooker, rice cooker, steamer.",6999,8999,"Home & Kitchen","Instant Pot","https://images.unsplash.com/photo-1585515320310-259814833e62?w=400",150,4.8,12453,1),
        ("Philips Air Fryer XXL","5.5L family-size air fryer. Cooks with 90% less fat.",12999,15999,"Home & Kitchen","Philips","https://images.unsplash.com/photo-1639831114716-1b2d55e7e6c1?w=400",100,4.6,5678,0),
        ("Dyson V15 Detect Vacuum","Laser-powered vacuum, intelligent auto-mode. 60min battery.",52900,59900,"Home & Kitchen","Dyson","https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400",50,4.7,987,0),
        ("IKEA MALM Bed Frame","Queen size bed frame with storage boxes. White finish.",18999,22999,"Home & Kitchen","IKEA","https://images.unsplash.com/photo-1505693314120-0d443867891c?w=400",60,4.3,2341,0),
        ("Philips Hand Blender","700W hand blender, turbo function, stainless steel blending shaft.",2499,3499,"Home & Kitchen","Philips","https://images.unsplash.com/photo-1585515320310-259814833e62?w=400",200,4.5,3456,0),
        ("Bosch Electric Kettle","1.5L electric kettle, 2400W, stainless steel, auto shut-off.",2999,3999,"Home & Kitchen","Bosch","https://images.unsplash.com/photo-1544378730-8b5104b18790?w=400",300,4.6,4567,0),
        ("Prestige Non-Stick Cookware Set","5-piece non-stick set: kadai, tawa, pans, glass lids.",3999,5499,"Home & Kitchen","Prestige","https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400",200,4.4,6789,0),
        ("Milton Thermosteel Flask 1L","1L double-walled stainless steel flask, 24hr hot/cold.",999,1499,"Home & Kitchen","Milton","https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400",500,4.6,8901,0),
        ("Cello Water Bottle Set","1L BPA-free water bottle, leak-proof, pack of 3.",599,899,"Home & Kitchen","Cello","https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400",600,4.3,5678,0),
        ("IKEA KALLAX Shelf Unit","4x2 shelf unit, white, 147x77cm, holds books, boxes, baskets.",8999,10999,"Home & Kitchen","IKEA","https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400",80,4.5,3456,0),
        ("Amazon Echo Dot 5th Gen","Smart speaker with Alexa, improved bass, motion detection.",4999,5999,"Home & Kitchen","Amazon","https://images.unsplash.com/photo-1543512214-318c7553f230?w=400",200,4.4,12345,1),
        ("Phillips LED Bulb 12W Pack","12W LED bulb, 6500K cool white, 1400 lumens, pack of 6.",799,1199,"Home & Kitchen","Philips","https://images.unsplash.com/photo-1532298229144-0ec0c57515c7?w=400",500,4.5,7890,0),
        ("Duroflex Dream Single Mattress","5-inch single mattress, high-resilience foam, medium-firm.",8999,11999,"Home & Kitchen","Duroflex","https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=400",60,4.5,2345,0),
        ("Bombay Dyeing Bedsheet Set","Double bedsheet with 2 pillow covers, 180TC cotton, printed.",1499,2199,"Home & Kitchen","Bombay Dyeing","https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=400",300,4.2,4567,0),
        ("Solimo Pillow Set of 2","Microfiber fill, soft and supportive, washable cover, pack of 2.",999,1499,"Home & Kitchen","Solimo","https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=400",400,4.3,3456,0),
        ("WeatherTech Shower Curtain","180x200cm, waterproof PEVA, anti-mold, 12 hooks included.",799,1299,"Home & Kitchen","Spaces","https://images.unsplash.com/photo-1552321554-5fefe8c9ef14?w=400",300,4.1,2345,0),
        ("Usha Table Fan 400mm","400mm sweep, 55W, 3 speed settings, powerful airflow.",2999,3999,"Home & Kitchen","Usha","https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=400",150,4.4,3456,0),
        ("Wipro Smart LED Strip","5m RGB LED strip, app control, music sync, waterproof IP65.",1299,1999,"Home & Kitchen","Wipro","https://images.unsplash.com/photo-1636466497217-26a8cbeaf0aa?w=400",300,4.3,5678,0),
        ("Hafele Kitchen Knife Set","5-piece stainless steel knife set with wooden block, sharp edge.",3499,4999,"Home & Kitchen","Hafele","https://images.unsplash.com/photo-1593618998160-e34014e67546?w=400",200,4.5,1987,0),
        ("Tupperware Lunch Box Set","3-container lunch box set, microwave-safe, leak-proof lid.",1499,2199,"Home & Kitchen","Tupperware","https://images.unsplash.com/photo-1564951434112-64d74cc2a2d7?w=400",400,4.6,6789,0),
        ("Pigeon Mini Induction Cooktop","1800W induction, feather touch, 7 pre-set menus, auto-shutoff.",2499,3499,"Home & Kitchen","Pigeon","https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400",200,4.4,4567,0),
        ("Godrej Washing Machine 7kg","7kg front load, inverter motor, 15 wash programs, steam wash.",28999,34999,"Home & Kitchen","Godrej","https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400",40,4.4,1234,1),
        ("Havells Stand Fan 400mm","400mm high-speed stand fan, 3 speed, timer, remote control.",4999,6499,"Home & Kitchen","Havells","https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=400",100,4.5,2109,0),
        ("Kuber Industries Storage Box","Stackable storage box set of 4, 30L each, lids, for wardrobe.",1999,2799,"Home & Kitchen","Kuber","https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400",300,4.2,3456,0),
        ("Hettich Tool Organizer","Wall-mounted tool organizer with hooks, for kitchen/garage.",1299,1799,"Home & Kitchen","Hettich","https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400",200,4.3,1234,0),


        # ══════════════════════════════════════════════════════════
        # BOOKS — 25 products
        # ══════════════════════════════════════════════════════════
        ("Atomic Habits - James Clear","Tiny changes, remarkable results. Build good habits.",399,599,"Books","Penguin","https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400",500,4.9,45678,1),
        ("The Psychology of Money","Timeless lessons on wealth, greed, and happiness.",349,499,"Books","Jaico","https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400",400,4.8,23456,0),
        ("Deep Work - Cal Newport","Rules for focused success in a distracted world.",299,449,"Books","Piatkus","https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=400",300,4.7,12345,0),
        ("Rich Dad Poor Dad","What the rich teach their kids about money that the poor don't.",349,499,"Books","Manjul","https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400",500,4.7,56789,1),
        ("Think and Grow Rich","Napoleon Hill's classic principles of personal achievement.",249,349,"Books","Fingerprint","https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400",400,4.6,34567,0),
        ("The Alchemist - Paulo Coelho","A magical fable about following your dream.",199,299,"Books","HarperCollins","https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400",600,4.8,67890,1),
        ("Zero to One - Peter Thiel","Notes on startups and how to build the future.",399,549,"Books","Crown","https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=400",300,4.6,12098,0),
        ("The Lean Startup","How today's entrepreneurs use continuous innovation.",349,499,"Books","Crown","https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400",250,4.5,9876,0),
        ("Sapiens - Yuval Noah Harari","A brief history of humankind.",499,649,"Books","Vintage","https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400",400,4.8,45678,1),
        ("The 4-Hour Workweek","Escape 9-5, live anywhere, and join the new rich.",399,549,"Books","Harmony","https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=400",300,4.4,23456,0),
        ("Ikigai - Japanese secret","The Japanese secret to a long and happy life.",249,349,"Books","Penguin","https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400",500,4.7,34567,0),
        ("Start with Why - Simon Sinek","How great leaders inspire everyone to take action.",349,499,"Books","Portfolio","https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400",350,4.6,18765,0),
        ("Mindset - Carol Dweck","The new psychology of success.",299,449,"Books","Random House","https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=400",300,4.6,15432,0),
        ("The Subtle Art of Not Giving a F*ck","A counterintuitive approach to living a good life.",349,499,"Books","HarperOne","https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400",450,4.5,34567,0),
        ("Can't Hurt Me - David Goggins","Master your mind and defy the odds.",449,599,"Books","Lioncrest","https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400",300,4.7,23456,0),
        ("How to Win Friends","Dale Carnegie's timeless classic on human relations.",199,299,"Books","Pocket Books","https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=400",600,4.6,56789,0),
        ("The Power of Now - Eckhart Tolle","A guide to spiritual enlightenment.",299,399,"Books","New World","https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400",400,4.5,23456,0),
        ("Good to Great - Jim Collins","Why some companies make the leap and others don't.",449,599,"Books","Harper Business","https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400",200,4.6,9876,0),
        ("The 7 Habits of Highly Effective People","Powerful lessons in personal change by Covey.",349,499,"Books","Free Press","https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=400",400,4.7,45678,0),
        ("Thinking Fast and Slow","How the two systems that drive the way we think work.",499,699,"Books","Farrar","https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400",300,4.7,23456,0),
        ("The 48 Laws of Power","Robert Greene's bestselling guide to power dynamics.",449,599,"Books","Penguin","https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400",250,4.5,18765,0),
        ("Essentialism - Greg McKeown","The disciplined pursuit of less.",349,499,"Books","Crown","https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=400",300,4.6,12345,0),
        ("The Art of War - Sun Tzu","Ancient Chinese military treatise, timeless strategy.",149,249,"Books","Fingerprint","https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400",600,4.5,34567,0),
        ("Built to Last - Jim Collins","Successful habits of visionary companies.",399,549,"Books","Harper Business","https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400",200,4.5,8765,0),
        ("Never Split the Difference","Negotiating as if your life depended on it, by Chris Voss.",399,549,"Books","Harper Business","https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=400",300,4.8,12345,0),


        # ══════════════════════════════════════════════════════════
        # SPORTS — 25 products
        # ══════════════════════════════════════════════════════════
        ("Yonex Badminton Racket","Professional grade racket, carbon graphite, lightweight 85g.",4999,6499,"Sports","Yonex","https://images.unsplash.com/photo-1613041720571-56d87aa2f9b1?w=400",120,4.6,1876,1),
        ("Decathlon Yoga Mat","Non-slip yoga mat, 5mm thick, 183x61cm, carry strap.",999,1499,"Sports","Decathlon","https://images.unsplash.com/photo-1601925228239-03f1e7c5d15b?w=400",300,4.5,6543,0),
        ("Fitbit Charge 6","Advanced fitness tracker, ECG app, built-in GPS, 7-day battery.",14999,17999,"Sports","Fitbit","https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=400",90,4.4,2109,0),
        ("Yonex Badminton Shuttlecocks","Feather shuttlecocks, pack of 6, for tournament play.",1299,1699,"Sports","Yonex","https://images.unsplash.com/photo-1613041720571-56d87aa2f9b1?w=400",400,4.5,3456,0),
        ("Decathlon Badminton Net","Regulation-size net, steel cable, easy setup, bag included.",2499,3499,"Sports","Decathlon","https://images.unsplash.com/photo-1613041720571-56d87aa2f9b1?w=400",150,4.4,987,0),
        ("Nivia Football Size 5","FIFA-approved, 32-panel, waterproof PU, match quality.",1499,1999,"Sports","Nivia","https://images.unsplash.com/photo-1575361204480-aadea25e6e68?w=400",300,4.5,4567,0),
        ("Cosco Cricket Bat Full Size","English willow, full size, Grade 1, rubber grip, 1.2kg.",3999,5499,"Sports","Cosco","https://images.unsplash.com/photo-1540747913346-19212a4b423d?w=400",150,4.4,1234,0),
        ("SG Cricket Helmet","ABS shell, steel grill, foam padding, adjustable, all sizes.",2499,3499,"Sports","SG","https://images.unsplash.com/photo-1540747913346-19212a4b423d?w=400",120,4.5,876,0),
        ("Nivia Cricket Batting Gloves","Full finger gloves, PVC back, sheepskin palm, pair.",1299,1799,"Sports","Nivia","https://images.unsplash.com/photo-1540747913346-19212a4b423d?w=400",200,4.3,1543,0),
        ("Cosco Cricket Kit Bag","Kit bag, wheels, 3 compartments, waterproof.",3499,4499,"Sports","Cosco","https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400",150,4.4,987,0),
        ("Decathlon Resistance Bands Set","Set of 5 resistance bands, 5-50 lbs, latex, carry bag.",999,1499,"Sports","Decathlon","https://images.unsplash.com/photo-1601925228239-03f1e7c5d15b?w=400",400,4.6,5678,0),
        ("Boldfit Skipping Rope","PVC cable, steel ball bearings, adjustable length.",499,799,"Sports","Boldfit","https://images.unsplash.com/photo-1601925228239-03f1e7c5d15b?w=400",600,4.4,8901,0),
        ("Domyos Dumbbell Set 10kg","2x5kg cast iron dumbbells, rubber grip, hex shape.",3999,5499,"Sports","Domyos","https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400",200,4.6,3456,0),
        ("Decathlon Swimming Goggles","Anti-fog, UV protection, silicone seal, adjustable strap.",799,1299,"Sports","Decathlon","https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=400",300,4.4,2345,0),
        ("Arena Swim Cap Silicone","Hydrodynamic silicone cap, unisex, multiple colors.",399,599,"Sports","Arena","https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=400",400,4.3,1987,0),
        ("Decathlon Cycling Helmet","Road cycling helmet, 18 vents, adjustable retention, 260g.",2999,3999,"Sports","Decathlon","https://images.unsplash.com/photo-1502904550040-7534597429ae?w=400",150,4.5,1234,0),
        ("Garmin Forerunner 255","GPS running watch, HRV status, training readiness, 14-day battery.",28999,32999,"Sports","Garmin","https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=400",60,4.7,987,1),
        ("Wildcraft 40L Trekking Backpack","40L hiking backpack, rain cover, hip belt, multiple pockets.",3999,5499,"Sports","Wildcraft","https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400",150,4.5,2109,0),
        ("Domyos Gym Gloves","Neoprene training gloves, palm padding, wrist support, unisex.",799,1299,"Sports","Domyos","https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400",400,4.4,4567,0),
        ("Nike Training Water Bottle","24oz squeeze bottle, flip-top lid, BPA-free.",999,1499,"Sports","Nike","https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400",500,4.5,5678,0),
        ("Boldfit Yoga Block Set","Set of 2 EVA foam yoga blocks, high density, non-slip.",699,999,"Sports","Boldfit","https://images.unsplash.com/photo-1601925228239-03f1e7c5d15b?w=400",400,4.5,3456,0),
        ("Nivia Basketball Size 7","Official size 7, rubber, deep channel, indoor/outdoor.",1499,1999,"Sports","Nivia","https://images.unsplash.com/photo-1575361204480-aadea25e6e68?w=400",200,4.4,1987,0),
        ("Stag Table Tennis Paddle","7-ply blade, 1.5mm rubber, ITTF approved, carry case.",1999,2799,"Sports","Stag","https://images.unsplash.com/photo-1575361204480-aadea25e6e68?w=400",150,4.5,876,0),
        ("Decathlon Foam Roller","High-density foam roller 45cm, muscle recovery, full body.",1299,1799,"Sports","Decathlon","https://images.unsplash.com/photo-1601925228239-03f1e7c5d15b?w=400",300,4.6,3456,0),
        ("Reebok Crossfit Shoes","Lightweight, flexible, grip sole, ideal for cross-training.",7999,9999,"Sports","Reebok","https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",150,4.5,1234,0),
    ]

    # Remove duplicates by name — only insert if name doesnt exist
    inserted = 0
    skipped = 0
    for p in products:
        name = p[0]
        exists = conn.execute("SELECT id FROM product WHERE name=?", (name,)).fetchone()
        if not exists:
            conn.execute(
                "INSERT INTO product (name,description,price,original_price,category,brand,image_url,stock,rating,reviews_count,is_featured) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                p
            )
            inserted += 1
        else:
            skipped += 1

    conn.commit()

    total = conn.execute("SELECT COUNT(*) FROM product").fetchone()[0]
    print(f"\n✅ Done!")
    print(f"   Inserted : {inserted} new products")
    print(f"   Skipped  : {skipped} (already existed)")
    print(f"   Total now: {total} products")

    # Show category breakdown
    print("\n📊 Products per category:")
    cats = conn.execute("SELECT category, COUNT(*) as c FROM product GROUP BY category ORDER BY category").fetchall()
    for cat in cats:
        print(f"   {cat[0]:<20} {cat[1]} products")

    conn.close()


if __name__ == "__main__":
    if not os.path.exists(DB):
        print("ERROR: Run python app.py first to create the database.")
    else:
        add_products()