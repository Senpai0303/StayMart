"""
scripts/add_cache_busters_all.py
Adds ?v=4.1.0 to all css/js links in frontend/pages/**/*.html
and inserts meta no-cache headers if not present.
"""

import os
import re

PAGES_DIR = "frontend/pages"
count = 0

for root, dirs, files in os.walk(PAGES_DIR):
    for f in files:
        if f.endswith(".html"):
            path = os.path.join(root, f)
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()
            
            # Replace ../../css/global.css with ../../css/global.css?v=4.1.0
            content = re.sub(r'href="(\.\./\.\./css/[^"]+?\.css)(\?v=[0-9.]+)?(")', r'href="\1?v=4.1.0\3', content)
            # Replace js scripts
            content = re.sub(r'src="(\.\./\.\./js/[^"]+?\.js)(\?v=[0-9.]+)?(")', r'src="\1?v=4.1.0\3', content)
            
            # Add meta no-cache if missing
            if 'http-equiv="Cache-Control"' not in content:
                meta_tags = """  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate"/>\n  <meta http-equiv="Pragma" content="no-cache"/>\n  <meta http-equiv="Expires" content="0"/>\n"""
                content = content.replace("<head>\n", f"<head>\n{meta_tags}")
            
            with open(path, "w", encoding="utf-8") as file:
                file.write(content)
            count += 1
            print(f"Updated cache busters in {path}")

print(f"Total admin/user pages updated: {count}")

