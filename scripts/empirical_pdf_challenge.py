import os
import sys
import re
import json
import pypdf

PDF_PATH = r"D:\Mini5th\StayMart_Project_Report.pdf"

def to_roman(n):
    val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syb = ["m", "cm", "d", "cd", "c", "xc", "l", "xl", "x", "ix", "v", "iv", "i"]
    roman_num = ""
    i = 0
    while n > 0:
        for _ in range(n // val[i]):
            roman_num += syb[i]
            n -= val[i]
        i += 1
    return roman_num

def run_adversarial_challenge():
    print("=" * 75)
    print("EMPIRICAL ADVERSARIAL CHALLENGER AUDIT: StayMart_Project_Report.pdf")
    print("=" * 75)

    results = {
        "pdf_path": PDF_PATH,
        "file_exists": False,
        "file_size_bytes": 0,
        "file_size_mb": 0.0,
        "total_pages": 0,
        "browser_stamp_violations": [],
        "cover_page_valid": False,
        "title_page_valid": False,
        "declaration_page_valid": False,
        "preliminary_roman_pages": [],
        "chapter1_arabic_valid": False,
        "arabic_sequence_valid": True,
        "arabic_sequence_mismatches": [],
        "toc_spot_checks": [],
        "lof_spot_checks": [],
        "lot_spot_checks": [],
        "verdict": "FAIL"
    }

    # 1. Existence and size
    if not os.path.exists(PDF_PATH):
        print(f"[FAIL] PDF does not exist at {PDF_PATH}")
        return results

    results["file_exists"] = True
    size = os.path.getsize(PDF_PATH)
    results["file_size_bytes"] = size
    results["file_size_mb"] = round(size / (1024 * 1024), 2)
    print(f"File Size: {results['file_size_mb']} MB ({size} bytes) - Target > 1.0 MB")
    assert size > 1024 * 1024, f"File size {size} is <= 1MB!"

    reader = pypdf.PdfReader(PDF_PATH)
    total_pages = len(reader.pages)
    results["total_pages"] = total_pages
    print(f"Total Pages: {total_pages}")
    assert total_pages >= 100, f"Total pages {total_pages} is < 100!"

    pages_text = []
    for idx, page in enumerate(reader.pages):
        txt = page.extract_text() or ""
        pages_text.append(txt)

    # 2. Check for forbidden browser headers/footers across every single page
    print("\n--- TEST 1: Scanning for forbidden browser stamps (file:/// URLs or dates) ---")
    date_patterns = [
        re.compile(r'file:///', re.IGNORECASE),
        re.compile(r'11/3/26'),
        re.compile(r'11/03/26'),
        re.compile(r'11/3/2026'),
        re.compile(r'11/03/2026'),
        re.compile(r'localhost:\d+'),
        re.compile(r'127\.0\.0\.1:\d+'),
        re.compile(r'\d{1,2}/\d{1,2}/\d{2,4},\s*\d{1,2}:\d{2}\s*(?:AM|PM)', re.IGNORECASE)
    ]

    for p_num in range(1, total_pages + 1):
        txt = pages_text[p_num - 1]
        for pattern in date_patterns:
            matches = pattern.findall(txt)
            if matches:
                # Discard false positives if it's within the institutional date "NOVEMBER, 2026"
                results["browser_stamp_violations"].append({
                    "page": p_num,
                    "pattern": pattern.pattern,
                    "matches": matches
                })

    if results["browser_stamp_violations"]:
        print(f"[FAIL] Found browser stamp violations: {results['browser_stamp_violations']}")
    else:
        print("[PASS] 0 forbidden browser stamps or file:/// URLs found across all 118 pages.")

    # 3. Verify Cover Page (page 1) fits on one page and does NOT spill onto page 2
    print("\n--- TEST 2: Inspecting Cover Page (Page 1) and Title Page (Page 2) ---")
    p1_txt = pages_text[0]
    p1_lines = [l.strip() for l in p1_txt.splitlines() if l.strip()]
    p2_txt = pages_text[1]
    p2_lines = [l.strip() for l in p2_txt.splitlines() if l.strip()]
    p3_txt = pages_text[2]
    p3_lines = [l.strip() for l in p3_txt.splitlines() if l.strip()]

    print(f"Page 1 first 2 lines: {p1_lines[:2]}")
    print(f"Page 1 last 2 lines: {p1_lines[-2:]}")
    print(f"Page 2 first 2 lines: {p2_lines[:2]}")
    print(f"Page 2 last 2 lines: {p2_lines[-2:]}")
    print(f"Page 3 first 2 lines: {p3_lines[:2]}")

    # Check Cover Page elements
    assert "STAYMART: AN INTELLIGENT ACCOMMODATION" in p1_txt, "Cover missing title"
    assert "A PROJECT REPORT" in p1_txt, "Cover missing 'A PROJECT REPORT'"
    assert "GRAPHIC ERA HILL UNIVERSITY" in p1_txt, "Cover missing university"
    assert "NOVEMBER, 2026" in p1_txt, "Cover missing date"
    assert p1_lines[-1] == "NOVEMBER, 2026", f"Cover page ends with {p1_lines[-1]!r}, expected 'NOVEMBER, 2026'"
    results["cover_page_valid"] = True
    print("[PASS] Cover Page (Page 1) contains all required elements and cleanly terminates with 'NOVEMBER, 2026'.")

    # Check Title Page elements
    assert "STAYMART: AN INTELLIGENT ACCOMMODATION" in p2_txt, "Title missing title"
    assert "PROJECT REPORT" in p2_txt, "Title missing 'PROJECT REPORT'"
    assert "DIVYANSHU SINGH" in p2_txt, "Title missing candidate"
    assert "GRAPHIC ERA HILL UNIVERSITY" in p2_txt, "Title missing university"
    assert "NOVEMBER, 2026" in p2_txt, "Title missing date"
    assert p2_lines[-1] == "NOVEMBER, 2026", f"Title page ends with {p2_lines[-1]!r}, expected 'NOVEMBER, 2026'"
    results["title_page_valid"] = True
    print("[PASS] Title Page (Page 2) begins independently, contains all required institutional elements, and ends with 'NOVEMBER, 2026'.")

    # Check Page 3 is Candidate's Declaration
    assert "CANDIDATE" in p3_txt and "DECLARATION" in p3_txt, "Page 3 is not Candidate's Declaration!"
    assert p3_lines[-1] == "i", f"Page 3 does not end with Roman numeral 'i', ends with {p3_lines[-1]!r}"
    results["declaration_page_valid"] = True
    print("[PASS] Page 3 is Candidate's Declaration with Roman numeral 'i' - confirms Cover & Title are strictly 1 page each.")

    # 4. Check Preliminary Roman Numerals and find Chapter 1
    print("\n--- TEST 3: Preliminary Roman Numerals and Chapter 1 Transition ---")
    p_ch1 = None
    for p in range(1, total_pages + 1):
        txt = pages_text[p - 1]
        if "CHAPTER 1" in txt and "INTRODUCTION AND PROBLEM STATEMENT" in txt and p > 10:
            p_ch1 = p
            break
    print(f"Chapter 1 physical page: {p_ch1}")
    assert p_ch1 is not None, "Failed to find Chapter 1 physical page"

    roman_failures = []
    for p in range(3, p_ch1):
        expected_roman = to_roman(p - 2)
        txt = pages_text[p - 1]
        lines = [l.strip() for l in txt.splitlines() if l.strip()]
        last_line = lines[-1] if lines else ""
        if last_line != expected_roman:
            roman_failures.append((p, expected_roman, last_line))
        results["preliminary_roman_pages"].append({
            "page": p,
            "expected": expected_roman,
            "actual": last_line,
            "match": last_line == expected_roman
        })

    if roman_failures:
        print(f"[FAIL] Roman numeral mismatches in preliminary pages: {roman_failures}")
    else:
        print(f"[PASS] All preliminary pages (Pages 3 to {p_ch1 - 1}) have exact lowercase Roman numerals (i to {to_roman(p_ch1 - 3)}).")

    # 5. Check Chapter 1 and Body Arabic Numerals
    print("\n--- TEST 4: Arabic Numerals Sequence ---")
    pch1_lines = [l.strip() for l in pages_text[p_ch1 - 1].splitlines() if l.strip()]
    if pch1_lines[-1] == "1":
        results["chapter1_arabic_valid"] = True
        print(f"[PASS] Chapter 1 (physical Page {p_ch1}) restarts numbering at Arabic '1'.")
    else:
        print(f"[FAIL] Chapter 1 (physical Page {p_ch1}) ends with '{pch1_lines[-1]}', expected '1'")

    for p in range(p_ch1, total_pages + 1):
        expected_arabic = str(p - p_ch1 + 1)
        txt = pages_text[p - 1]
        lines = [l.strip() for l in txt.splitlines() if l.strip()]
        last_line = lines[-1] if lines else ""
        if last_line != expected_arabic:
            results["arabic_sequence_valid"] = False
            results["arabic_sequence_mismatches"].append({
                "page": p,
                "expected": expected_arabic,
                "actual": last_line
            })

    if results["arabic_sequence_valid"]:
        print(f"[PASS] All body pages ({p_ch1} to {total_pages}) strictly follow Arabic numbering 1 to {total_pages - p_ch1 + 1}.")
    else:
        print(f"[FAIL] Arabic sequence mismatches: {results['arabic_sequence_mismatches'][:5]}")

    # 6. Spot-Check TOC, LOF, and LOT entries
    print("\n--- TEST 5: Spot-Checking TOC, LOF, and LOT Entries against Physical Pages ---")
    
    # Locate TOC, LOF, LOT pages
    toc_pages = []
    lof_pages = []
    lot_pages = []
    for p in range(3, p_ch1):
        txt = pages_text[p - 1]
        if "TABLE OF CONTENTS" in txt:
            toc_pages.append(p)
        if "LIST OF FIGURES" in txt:
            lof_pages.append(p)
        if "LIST OF TABLES" in txt:
            lot_pages.append(p)

    print(f"TOC Pages: {toc_pages}")
    print(f"LOF Pages: {lof_pages}")
    print(f"LOT Pages: {lot_pages}")

    # Print raw text of TOC, LOF, LOT for detailed analysis
    print("\n--- DUMPING TOC TEXT ---")
    for tp in toc_pages:
        print(f"--- Page {tp} ---")
        print(pages_text[tp - 1][:800])

    print("\n--- DUMPING LOF TEXT ---")
    for lp in lof_pages:
        print(f"--- Page {lp} ---")
        print(pages_text[lp - 1][:800])

    print("\n--- DUMPING LOT TEXT ---")
    for ltp in lot_pages:
        print(f"--- Page {ltp} ---")
        print(pages_text[ltp - 1][:800])

    return results

if __name__ == '__main__':
    res = run_adversarial_challenge()
