#!/usr/bin/env python3
"""
scripts/inject_cache_busters.py
Injects cache-busting query strings and anti-caching HTTP-EQUIV headers
into all frontend HTML files to ensure browsers never serve stale cached assets.
"""

import glob
import re

META_TAGS = """  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate"/>
  <meta http-equiv="Pragma" content="no-cache"/>
  <meta http-equiv="Expires" content="0"/>"""

def update_html_files():
    html_files = sorted(glob.glob("frontend/*.html"))
    for path in html_files:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # Update CSS links: css/xyz.css -> css/xyz.css?v=3.5.0
        content = re.sub(
            r'href=["\'](css/[^"\']+\.css)(?:\?[^"\']*)?["\']',
            r'href="\1?v=3.5.0"',
            content
        )

        # Update JS links: js/xyz.js -> js/xyz.js?v=3.5.0
        content = re.sub(
            r'src=["\'](js/[^"\']+\.js)(?:\?[^"\']*)?["\']',
            r'src="\1?v=3.5.0"',
            content
        )

        # Add Cache-Control meta tags if not already present
        if 'http-equiv="Cache-Control"' not in content:
            content = re.sub(
                r'(<meta\s+name=["\']viewport["\'][^>]*>)',
                r'\1\n' + META_TAGS,
                content,
                count=1
            )

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[OK] Injected cache-busters into {path}")

if __name__ == "__main__":
    update_html_files()

