import pypdf

reader = pypdf.PdfReader(r"D:\Mini5th\report\compiled\test_report.pdf")
print(f"Total pages: {len(reader.pages)}")

ch_starts = {}
for i, p in enumerate(reader.pages):
    txt = p.extract_text()
    for c in range(1, 10):
        if f"CHAPTER {c}" in txt and c not in ch_starts:
            ch_starts[c] = i + 1
    if "1. Adomavicius" in txt and "Ref" not in ch_starts:
        ch_starts["Ref"] = i + 1

for c in range(1, 10):
    next_start = ch_starts.get(c + 1, ch_starts.get("Ref", len(reader.pages) + 1))
    cur_start = ch_starts.get(c, 0)
    length = next_start - cur_start
    print(f"Chapter {c}: Page {cur_start} to {next_start - 1} ({length} pages)")

print(f"References: Page {ch_starts.get('Ref')}")
