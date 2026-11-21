import os
import re

PATTERNS = [
    r'\bTODO\b',
    r'\bFIXME\b',
    r'\bTBD\b',
    r'\bXXX\b',
    r'lorem\s+ipsum',
    r'insert\s+here',
    r'coming\s+soon',
    r'\[insert',
    r'<insert',
    r'your\s+name\s+here',
    r'as\s+an\s+ai',
    r'language\s+model',
    r'chatgpt',
    r'openai',
    r'claude',
    r'certainly,?\s+here',
    r'here\s+is\s+the\s+(?:chapter|report|document)',
    r'in\s+this\s+section,?\s+we\s+will\s+insert'
]

compiled_patterns = [re.compile(p, re.IGNORECASE) for p in PATTERNS]

directories_and_files = [
    r"d:\Mini5th\report\main.tex",
    r"d:\Mini5th\report\references.bib",
]

for d in [r"d:\Mini5th\report\chapters", r"d:\Mini5th\report\appendices"]:
    for f in os.listdir(d):
        if f.endswith('.tex'):
            directories_and_files.append(os.path.join(d, f))

print(f"Scanning {len(directories_and_files)} files for AI traces, stubs, and placeholders...\n")

issues_found = []

for file_path in directories_and_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    file_issues = 0
    for line_idx, line in enumerate(lines, 1):
        for pattern in compiled_patterns:
            matches = pattern.findall(line)
            if matches:
                # Check context to see if it's a false positive or actual stub/AI trace
                issues_found.append((file_path, line_idx, line.strip(), matches))
                file_issues += 1
    if file_issues == 0:
        print(f"[CLEAN] {os.path.basename(file_path)}: 0 stubs or AI artifacts ({len(lines)} lines)")
    else:
        print(f"[FLAG]  {os.path.basename(file_path)}: {file_issues} potential matches found")

print("\n--- Summary of Matches ---")
if not issues_found:
    print("ZERO AI TRACES OR PLACEHOLDER STUBS FOUND!")
else:
    for f, l, content, m in issues_found:
        print(f"File: {os.path.basename(f)} Line {l}: match={m} -> {content[:80]}")
