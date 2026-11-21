import os
import re

html_files = set()
for root, _, files in os.walk('frontend'):
    for f in files:
        if f.endswith('.html'):
            rel = os.path.relpath(os.path.join(root, f), 'frontend').replace('\\', '/')
            html_files.add(rel)

print(f"Total HTML files found: {len(html_files)}")

broken = []
for root, _, files in os.walk('frontend'):
    for f in files:
        if f.endswith(('.html', '.js')):
            full = os.path.join(root, f)
            text = open(full, encoding='utf-8', errors='ignore').read()
            # match strings ending with .html
            pattern = re.compile(r"""['"`]([a-zA-Z0-9_\-\.\/]+\.html)""")
            for m in pattern.finditer(text):
                ref = m.group(1)
                if ref.startswith(('http', '//', 'mailto:')):
                    continue
                s_dir = os.path.dirname(os.path.relpath(full, 'frontend')).replace('\\', '/')
                # Handle leading /
                if ref.startswith('/'):
                    target = os.path.normpath(ref.lstrip('/')).replace('\\', '/')
                else:
                    target = os.path.normpath(os.path.join(s_dir, ref)).replace('\\', '/')
                
                # If target is not in html_files, might be dynamic prefix like ${prefix}login.html
                if target not in html_files:
                    # check if basename exists in html_files
                    basename = os.path.basename(ref)
                    matching = [h for h in html_files if os.path.basename(h) == basename]
                    broken.append((os.path.relpath(full, 'frontend').replace('\\', '/'), ref, target, tuple(matching)))

print(f"Potential unresolved links: {len(broken)}")
for src, ref, target, matching in sorted(set(broken)):
    print(f"File: {src} -> Ref: '{ref}' -> Target: '{target}' (Matches: {matching})")
