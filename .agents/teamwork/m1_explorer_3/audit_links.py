import glob
import os
import re

real_html_files = set()
for root, dirs, files in os.walk('frontend'):
    for f in files:
        if f.endswith('.html'):
            rel = os.path.relpath(os.path.join(root, f), 'frontend').replace('\\', '/')
            real_html_files.add(rel)
            real_html_files.add(f)

print('Real HTML files:', sorted(list(real_html_files)))

all_files = glob.glob('frontend/**/*.js', recursive=True) + glob.glob('frontend/**/*.html', recursive=True)
pattern = re.compile(r"""['"`]([^'"`\n]+\.html(?:[?#][^'"`\n]*)?)['"`]""")

broken_refs = []
all_refs = []
for fp in all_files:
    with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    for m in pattern.finditer(content):
        raw_url = m.group(1)
        url = raw_url.split('?')[0].split('#')[0]
        if url.startswith('http://') or url.startswith('https://'):
            continue
        cleaned = url.replace('${depthPrefix()}', '').replace('${DASH_ROOT}', '')
        base = os.path.basename(cleaned)
        all_refs.append((fp, raw_url, base))
        if base and base not in real_html_files:
            broken_refs.append((fp, raw_url, base))

print(f'\nTotal HTML references examined: {len(all_refs)}')
print(f'Total broken references: {len(broken_refs)}')
for fp, url, base in broken_refs:
    print(f'  {fp}: ref="{url}" -> basename "{base}" NOT FOUND')
