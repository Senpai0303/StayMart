import glob
import re

with open('frontend/css/global.css', 'r', encoding='utf-8') as f:
    glob_classes = set(re.findall(r'\.([a-zA-Z0-9_-]+)', f.read()))

with open('frontend/css/dashboard.css', 'r', encoding='utf-8') as f:
    dash_classes = set(re.findall(r'\.([a-zA-Z0-9_-]+)', f.read()))

all_css_classes = glob_classes | dash_classes

html_and_js = glob.glob('frontend/**/*.html', recursive=True) + glob.glob('frontend/**/*.js', recursive=True)
used_classes = set()
class_pattern = re.compile(r"""class=['"]([^'"]+)['"]""")

for fp in html_and_js:
    with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    for m in class_pattern.finditer(content):
        for c in m.group(1).split():
            if '$' not in c and '{' not in c and '<' not in c and not c.startswith('.'):
                used_classes.add(c)

missing_classes = used_classes - all_css_classes
print(f'Total HTML/JS classes found: {len(used_classes)}')
print(f'Total missing classes in CSS: {len(missing_classes)}')
for c in sorted(list(missing_classes)):
    print('  missing class:', c)
