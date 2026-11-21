import subprocess
import json
import os

NEW_PRODUCTS = [
    (25, 2, 11, 'Symphony Diet 3D 30i Personal Tower Air Cooler (Honeycomb / 4 Castor Wheels)',
     '30-litre compact tower air cooler with 3D honeycomb cooling pads, low power consumption (145W) that runs smoothly on student PG inverters. Easy to move between study desk and bed on smooth castor wheels. Graduating senior passing out.',
     3200.00, 'SELL', 'GOOD', 'Symphony', 3, 'ISBT',
     '["https://images.unsplash.com/photo-1585338107529-13afc5f02586?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1610557892470-55d9e80c0bce?auto=format&fit=crop&w=800&q=80"]',
     'APPROVED', True, 85),

    (26, 2, 11, 'Prestige PIC 20 1200W Induction Cooktop + Stainless Steel Tea & Maggi Pan',
     'Essential for student hostel & PG rooms where gas cylinders are prohibited. Push-button Indian menu options (Milk, Boil, Curry, Dosa). Includes stainless steel saucepan with handle for midnight Maggi, tea, and boiling eggs.',
     1400.00, 'SELL', 'LIKE_NEW', 'Prestige', 3, 'Clement Town',
     '["https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=800&q=80"]',
     'APPROVED', True, 60),

    (27, 2, 11, 'Whirlpool 190L 4-Star Single Door Direct Cool Refrigerator (Silver Mirror)',
     'Single door compact refrigerator used by 2 roommates near Graphic Era. 4-star energy rating adds negligible cost to shared electricity. Ice maker freezer, vegetable crisper box, and silent reciprocating compressor.',
     7200.00, 'SELL', 'GOOD', 'Whirlpool', 3, 'Clement Town',
     '["https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1584568694244-14fbdf83bd30?auto=format&fit=crop&w=800&q=80"]',
     'APPROVED', True, 115),

    (28, 3, 9, 'Wakefit Orthopedic Single Bed Mattress (72x36x5 inch) + Quilted Washable Cover',
     '72x36x5 inch high-density orthopedic memory foam mattress for single student PG cots. Excellent spine support for long study hours. Clean, spotless with breathable zipper cover. Purchased 9 months ago.',
     2800.00, 'SELL', 'LIKE_NEW', 'Wakefit', 1, 'Rajpur Road',
     '["https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1540518614846-7ede433c4ef7?auto=format&fit=crop&w=800&q=80"]',
     'APPROVED', True, 92),

    (29, 3, 9, 'Nilkamal Mid-Back Ergonomic Computer Study Chair (Breathable Mesh / Black)',
     'Ergonomic swivel desk chair with pneumatic height adjustment, lumbar support cushion, and 360-degree smooth nylon wheels. Ideal for study tables, coding projects, and online lectures.',
     2100.00, 'SELL', 'GOOD', 'Nilkamal', 1, 'Rajpur Road',
     '["https://images.unsplash.com/photo-1580481077195-c9a75d5e236b?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1505797149-43b0069ec26b?auto=format&fit=crop&w=800&q=80"]',
     'APPROVED', True, 74),

    (30, 3, 11, 'Bajaj Flashy 1000W Radiant Room Heater for Dehradun Winters',
     'Instant infrared quartz heating element with safety tip-over switch and stainless steel heat reflector. Warms student study rooms in 5 minutes during chilly Dehradun and Mussoorie winter mornings.',
     850.00, 'SELL', 'LIKE_NEW', 'Bajaj', 1, 'Rajpur Road',
     '["https://images.unsplash.com/photo-1621905252507-b35492cc74b4?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=800&q=80"]',
     'APPROVED', True, 110),

    (31, 4, 7, 'HP Pavilion 14 Lightweight Student Laptop (Core i5 11th Gen / 16GB / 512GB SSD)',
     '14-inch Full HD IPS anti-glare display, Intel Core i5 1135G7, 16GB dual-channel DDR4 RAM, 512GB NVMe SSD, backlit keyboard, Bang & Olufsen audio. 6 hours genuine battery life. Perfect for BCA/CSE coding, Java, and projects.',
     34000.00, 'SELL', 'GOOD', 'HP', 6, 'Ballupur',
     '["https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1603302576837-37561b2e2302?auto=format&fit=crop&w=800&q=80"]',
     'APPROVED', True, 210),

    (32, 4, 7, 'Sony WH-CH520 Wireless Bluetooth Headphones (50-Hr Battery for Late Night Study)',
     'Lightweight on-ear headphones with 50-hour playback, DSEE sound enhancement, dual device multipoint connection, and built-in mic for viva and Zoom classes. 3-minute quick charge provides 1.5 hours listening.',
     2900.00, 'SELL', 'LIKE_NEW', 'Sony', 6, 'Ballupur',
     '["https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1583394838336-acd977736f90?auto=format&fit=crop&w=800&q=80"]',
     'APPROVED', True, 88),

    (33, 4, 7, 'Casio FX-991CW Advanced Scientific Calculator (Classwiz / High-Res Natural Display)',
     'High-resolution natural textbook 4-gradation display with spreadsheet, matrix calculation (4x4), equation solver, and numerical integration. Mandatory for engineering math, statistics, and university exams.',
     1100.00, 'SELL', 'LIKE_NEW', 'Casio', 6, 'Ballupur',
     '["https://images.unsplash.com/photo-1594980596870-8aa52a78d8cd?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1611117775350-ac3950990985?auto=format&fit=crop&w=800&q=80"]',
     'APPROVED', True, 65),

    (34, 5, 12, 'Firefox Target 21-Speed Hardtail Mountain Bicycle with Disc Brakes & Mudguards',
     'Sturdy steel hardtail mountain bike with 21-speed Shimano Tourney gearing, front zoom suspension fork, and mechanical disc brakes. Saves daily auto fare to Graphic Era / UPES. Includes bottle holder and cable lock.',
     6500.00, 'SELL', 'GOOD', 'Firefox', 4, 'Patel Nagar',
     '["https://images.unsplash.com/photo-1485965120184-e220f721d03e?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1507035895480-2b3156c31fc8?auto=format&fit=crop&w=800&q=80"]',
     'APPROVED', True, 185),

    (35, 5, 10, 'HC Verma Concepts of Physics (Part 1 & 2) + Irodov General Physics Problems',
     'HC Verma Part 1 & Part 2 in neat condition with clean problem margins, paired with IE Irodov Problems in General Physics. Proven question bank for 1st year engineering physics and competitive exams.',
     750.00, 'SELL', 'GOOD', 'Bharati Bhawan', 4, 'Patel Nagar',
     '["https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1532012164546-f432f2e3777f?auto=format&fit=crop&w=800&q=80"]',
     'APPROVED', True, 45),

    (36, 5, 16, 'Spacious 4-Shelf Collapsible Fabric Wardrobe with Steel Frame (Grey Dustproof Cover)',
     'Heavy-duty powder-coated iron pipes with plastic connectors and water-resistant non-woven fabric zipped cover. 4 storage shelves for folded clothes and center hanging rod. Folds compact into a box for easy moving.',
     900.00, 'SELL', 'GOOD', 'Caddy', 4, 'Patel Nagar',
     '["https://images.unsplash.com/photo-1595428774223-ef52624120d2?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1558997519-83ea9252def8?auto=format&fit=crop&w=800&q=80"]',
     'APPROVED', True, 80)
]

IMAGE_FIXES = {
    # Product 14: LG washing machine -> real washing machine images
    14: '["https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1610557892470-55d9e80c0bce?auto=format&fit=crop&w=800&q=80"]',
    # Product 16: Havells AC -> real split AC
    16: '["https://images.unsplash.com/photo-1585338107529-13afc5f02586?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1621905252507-b35492cc74b4?auto=format&fit=crop&w=800&q=80"]',
    # Product 17: Mixer grinder -> real mixer grinder / kitchen
    17: '["https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=800&q=80"]',
    # Product 20: Pulsar 150 motorbike -> real motorcycle images
    20: '["https://images.unsplash.com/photo-1558981403-c5f9899a28bc?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1568772585407-9361f9bf3a87?auto=format&fit=crop&w=800&q=80"]',
    # Product 22: Cricket kit -> real cricket equipment
    22: '["https://images.unsplash.com/photo-1531415074968-036ba1b575da?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1624526267942-ab0ff8a3e972?auto=format&fit=crop&w=800&q=80"]'
}

def update_database():
    print("Connecting to staymart-mysql Docker container...")
    
    # Apply Image Fixes
    for pid, img_json in IMAGE_FIXES.items():
        escaped_json = img_json.replace('"', '\\"')
        sql = f"USE staymart; UPDATE products SET images='{escaped_json}' WHERE id={pid};"
        cmd = ['docker', 'exec', '-i', 'staymart-mysql', 'mysql', '-uroot', '-proot', '-e', sql]
        subprocess.run(cmd, check=True)
        print(f"Fixed images for Product #{pid}")
        
    # Insert New Products
    for p in NEW_PRODUCTS:
        pid, posted_by, cat_id, title, desc, price, p_type, cond, brand, loc_id, area, img_json, status, is_avail, views = p
        escaped_title = title.replace("'", "\\'")
        escaped_desc = desc.replace("'", "\\'")
        escaped_brand = f"'{brand}'" if brand else "NULL"
        escaped_json = img_json.replace('"', '\\"')
        
        sql = f"""USE staymart;
INSERT INTO products (id, posted_by, category_id, title, description, price, listing_type, `condition`, brand, location_id, area, images, status, is_available, views_count, created_at)
VALUES ({pid}, {posted_by}, {cat_id}, '{escaped_title}', '{escaped_desc}', {price}, '{p_type}', '{cond}', {escaped_brand}, {loc_id}, '{area}', '{escaped_json}', '{status}', {1 if is_avail else 0}, {views}, NOW())
ON DUPLICATE KEY UPDATE 
title='{escaped_title}', description='{escaped_desc}', price={price}, images='{escaped_json}';
"""
        cmd = ['docker', 'exec', '-i', 'staymart-mysql', 'mysql', '-uroot', '-proot', '-e', sql]
        subprocess.run(cmd, check=True)
        print(f"Added/Updated Product #{pid}: {title[:40]}...")

    print("\nDatabase update completed successfully!")

if __name__ == '__main__':
    update_database()
