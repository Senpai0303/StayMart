"""
scripts/bump_cache_busters.py
Bumps all static asset version queries in frontend/*.html to ?v=4.1.0
to immediately force browser cache invalidation.
"""

import os
import re

FRONTEND_DIR = "frontend"
count = 0

for root, dirs, files in os.walk(FRONTEND_DIR):
    for f in files:
        if f.endswith(".html"):
            path = os.path.join(root, f)
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()
            
            # Replace any ?v=x.y.z with ?v=4.1.0
            new_content = re.sub(r'(\.(?:css|js))\?v=[0-9.]+', r'\1?v=4.1.0', content)
            
            if new_content != content:
                with open(path, "w", encoding="utf-8") as file:
                    file.write(new_content)
                count += 1
                print(f"Bumped cache busters in {path}")

print(f"Total HTML files updated: {count}")

