import re

with open('database/04_update_realistic_media.sql', 'r', encoding='utf-8') as f:
    sql = f.read()

with open('database/03_seed_listings.sql', 'r', encoding='utf-8') as f:
    seed = f.read()

for line in sql.splitlines():
    m = re.match(r"UPDATE (properties|products) SET images = '([^']+)' WHERE id = (\d+);", line.strip())
    if m:
        table, new_img, item_id = m.groups()
        # Find picsum pattern
        # Replace the picsum array in 03_seed_listings
        seed = re.sub(
            r"(\(\s*" + item_id + r",\s*[\s\S]*?)'\[\"https://picsum\.photos[^']+\]'([\s\S]*?)",
            lambda match: match.group(1) + "'" + new_img + "'" + match.group(2),
            seed,
            count=1
        )

with open('database/03_seed_listings.sql', 'w', encoding='utf-8') as f:
    f.write(seed)

print("Updated 03_seed_listings.sql successfully")
