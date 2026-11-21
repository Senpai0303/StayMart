import os
import re

seed_path = 'database/03_seed_listings.sql'
update_path = 'database/04_update_realistic_media.sql'

with open(seed_path, 'r', encoding='utf-8') as f:
    seed_content = f.read()

# 1. Room Images (accurate room & hostel bedding images)
room_lines = """INSERT INTO rooms (property_id, room_number, type, price, capacity, floor_number, is_available, images) VALUES
(1, 'A-101', 'SINGLE', 6500.00, 1, 1, TRUE, '["https://images.unsplash.com/photo-1598928506311-c55ded91a20c?auto=format&fit=crop&w=800&q=80"]'),
(1, 'A-102', 'DOUBLE', 5000.00, 2, 1, TRUE, '["https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?auto=format&fit=crop&w=800&q=80"]'),
(1, 'B-201', 'TRIPLE', 4200.00, 3, 2, FALSE, '["https://images.unsplash.com/photo-1555854877-bab0e564b8d5?auto=format&fit=crop&w=800&q=80"]'),
(2, 'G-01',  'SINGLE', 8500.00, 1, 0, TRUE, '["https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=800&q=80"]'),
(2, 'G-02',  'DOUBLE', 6500.00, 2, 0, TRUE, '["https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=800&q=80"]'),
(3, 'H-101', 'DOUBLE', 7000.00, 2, 1, TRUE, '["https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?auto=format&fit=crop&w=800&q=80"]'),
(3, 'H-102', 'TRIPLE', 5500.00, 3, 1, TRUE, '["https://images.unsplash.com/photo-1555854877-bab0e564b8d5?auto=format&fit=crop&w=800&q=80"]'),
(3, 'D-01',  'DORMITORY', 4000.00, 6, 0, TRUE, '["https://images.unsplash.com/photo-1512918728675-ed5a9ecdebfd?auto=format&fit=crop&w=800&q=80"]');"""

seed_content = re.sub(
    r"INSERT INTO rooms[^(]+\([^;]+;",
    room_lines,
    seed_content,
    flags=re.DOTALL
)

# 2. Accurate product images map for products 1-24:
product_images = {
    1: '["https://images.unsplash.com/photo-1593642632823-8f785ba67e45?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?auto=format&fit=crop&w=800&q=80"]',
    2: '["https://images.unsplash.com/photo-1603302576837-37561b2e2302?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=800&q=80"]',
    3: '["https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?auto=format&fit=crop&w=800&q=80"]',
    4: '["https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1502920917128-1aa500764cbd?auto=format&fit=crop&w=800&q=80"]',
    5: '["https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1592750475338-74b7b21085ab?auto=format&fit=crop&w=800&q=80"]',
    6: '["https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1580910051074-3eb694886505?auto=format&fit=crop&w=800&q=80"]',
    7: '["https://images.unsplash.com/photo-1598327105666-5b89351aff97?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1565849904461-04a58ad377e0?auto=format&fit=crop&w=800&q=80"]',
    8: '["https://images.unsplash.com/photo-1567581935884-3349723552ca?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1511707171634-5f897ff02560?auto=format&fit=crop&w=800&q=80"]',
    9: '["https://images.unsplash.com/photo-1617806118233-18e1de247200?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1530018607912-eff2daa1bac4?auto=format&fit=crop&w=800&q=80"]',
    10: '["https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1540518614846-7ede433c4ef7?auto=format&fit=crop&w=800&q=80"]',
    11: '["https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?auto=format&fit=crop&w=800&q=80"]',
    12: '["https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1532012164546-f432f2e3777f?auto=format&fit=crop&w=800&q=80"]',
    13: '["https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&w=800&q=80"]',
    14: '["https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1610557892470-55d9e80c0bce?auto=format&fit=crop&w=800&q=80"]',
    15: '["https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1584568694244-14fbdf83bd30?auto=format&fit=crop&w=800&q=80"]',
    16: '["https://images.unsplash.com/photo-1621905252507-b35492cc74b4?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1585338107529-13afc5f02586?auto=format&fit=crop&w=800&q=80"]',
    17: '["https://images.unsplash.com/photo-1570222094114-d054a817e56b?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=800&q=80"]',
    18: '["https://images.unsplash.com/photo-1558981403-c5f9899a28bc?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1568772585407-9361f9bf3a87?auto=format&fit=crop&w=800&q=80"]',
    19: '["https://images.unsplash.com/photo-1558981806-ec527fa84c39?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1558981359-219d6364c9c8?auto=format&fit=crop&w=800&q=80"]',
    20: '["https://images.unsplash.com/photo-1568772585407-9361f9bf3a87?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1609630875171-b1321377ee65?auto=format&fit=crop&w=800&q=80"]',
    21: '["https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1613918108466-292b78a8ef95?auto=format&fit=crop&w=800&q=80"]',
    22: '["https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1531415074968-036ba1b575da?auto=format&fit=crop&w=800&q=80"]',
    23: '["https://images.unsplash.com/photo-1576995853123-5a10305d93c0?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1551028719-00167b16eac5?auto=format&fit=crop&w=800&q=80"]',
    24: '["https://images.unsplash.com/photo-1595428774223-ef52624120d2?auto=format&fit=crop&w=800&q=80","https://images.unsplash.com/photo-1558997519-83ea9252def8?auto=format&fit=crop&w=800&q=80"]'
}

# Update products section in 03_seed_listings.sql
lines = seed_content.splitlines()
new_lines = []
curr_prod_id = None

for line in lines:
    m = re.match(r"^\s*\((\d+),\s*\d+,\s*\d+,", line)
    if m:
        curr_prod_id = int(m.group(1))

    if curr_prod_id is not None and curr_prod_id in product_images:
        if line.strip().startswith("'[") and (("picsum" in line) or ("unsplash" in line)):
            prefix = line[:line.find("'[")]
            suffix = line[line.rfind("]'") + 2:]
            line = prefix + "'" + product_images[curr_prod_id] + "'" + suffix
            curr_prod_id = None

    new_lines.append(line)

new_seed = '\n'.join(new_lines) + '\n'

with open(seed_path, 'w', encoding='utf-8') as f:
    f.write(new_seed)

print("Updated 03_seed_listings.sql successfully")

# 3. Also generate clean 04_update_realistic_media.sql
update_sql = "-- StayMart: Production realistic media updates for all listings\nUSE staymart;\n\n-- 1. Properties\n"
for prop_id in range(1, 13):
    # properties already have correct URLs, let's keep them explicit
    pass

# Read property URLs from 03_seed_listings.sql to keep 04 in perfect sync
property_images = {}
for m in re.finditer(r"\((\d+),\s*\d+,\s*'[^']+',[\s\S]*?'(\[\"[^\"]+unsplash[^\']+\])'", new_seed):
    p_id = int(m.group(1))
    if p_id <= 12 and p_id not in property_images:
        property_images[p_id] = m.group(2)

update_sql = "-- StayMart: Synchronized Realistic Media for All Listings\nUSE staymart;\n\n-- 1. Properties\n"
for p_id in sorted(property_images.keys()):
    update_sql += f"UPDATE properties SET images = '{property_images[p_id]}' WHERE id = {p_id};\n"

update_sql += "\n-- 2. Rooms\n"
room_tuples = [
    (1, 'A-101', '["https://images.unsplash.com/photo-1598928506311-c55ded91a20c?auto=format&fit=crop&w=800&q=80"]'),
    (1, 'A-102', '["https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?auto=format&fit=crop&w=800&q=80"]'),
    (1, 'B-201', '["https://images.unsplash.com/photo-1555854877-bab0e564b8d5?auto=format&fit=crop&w=800&q=80"]'),
    (2, 'G-01',  '["https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=800&q=80"]'),
    (2, 'G-02',  '["https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=800&q=80"]'),
    (3, 'H-101', '["https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?auto=format&fit=crop&w=800&q=80"]'),
    (3, 'H-102', '["https://images.unsplash.com/photo-1555854877-bab0e564b8d5?auto=format&fit=crop&w=800&q=80"]'),
    (3, 'D-01',  '["https://images.unsplash.com/photo-1512918728675-ed5a9ecdebfd?auto=format&fit=crop&w=800&q=80"]'),
]
for p_id, r_num, imgs in room_tuples:
    update_sql += f"UPDATE rooms SET images = '{imgs}' WHERE property_id = {p_id} AND room_number = '{r_num}';\n"

update_sql += "\n-- 3. Products\n"
for prod_id, imgs in sorted(product_images.items()):
    update_sql += f"UPDATE products SET images = '{imgs}' WHERE id = {prod_id};\n"

with open(update_path, 'w', encoding='utf-8') as f:
    f.write(update_sql)

print("Updated 04_update_realistic_media.sql successfully")
