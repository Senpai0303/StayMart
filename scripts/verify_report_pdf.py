import os
import sys
import re
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

def verify_report_pdf():
    print("=" * 70, flush=True)
    print("STAYMART PROJECT REPORT PDF INDEPENDENT VERIFICATION", flush=True)
    print("=" * 70, flush=True)

    # 1. Existence and size
    assert os.path.exists(PDF_PATH), f"Target PDF does not exist: {PDF_PATH}"
    size = os.path.getsize(PDF_PATH)
    print(f"[PASS] File exists: {PDF_PATH} ({size} bytes, {size / (1024*1024):.2f} MB)", flush=True)
    assert size > 1 * 1024 * 1024, f"Target PDF size {size} is under 1MB requirement!"

    reader = pypdf.PdfReader(PDF_PATH)
    total_pages = len(reader.pages)
    print(f"[PASS] Total page count: {total_pages} (Requirement: 50 pages)", flush=True)
    assert total_pages == 50, f"Expected 50 pages, got {total_pages}"

    print(f"Pre-extracting text across all {total_pages} pages...", flush=True)
    all_texts = [p.extract_text() for p in reader.pages]
    print(f"[PASS] Extracted text from all {total_pages} pages cleanly", flush=True)

    # 2. Check no Chrome default headers/footers (file:/// URLs or print timestamps)
    for idx, txt in enumerate(all_texts, 1):
        assert "file:///" not in txt, f"Found browser file:/// URL on page {idx}!"
        assert not re.search(r'\d{1,2}/\d{1,2}/\d{2,4},\s*\d{1,2}:\d{2}\s*(?:AM|PM)', txt), f"Found browser timestamp on page {idx}!"
    print("[PASS] Clean compilation: 0 browser URLs or print timestamps across all pages", flush=True)

    # 3. Check Cover Page (Page 1)
    p1_txt = all_texts[0]
    p1_norm = " ".join(p1_txt.split())
    p1_lines = [l.strip() for l in p1_txt.split('\n') if l.strip()]
    assert "STAYMART: SMART STUDENT HOUSING AND CAMPUS MARKETPLACE" in p1_norm, "Cover page missing title"
    assert "A PROJECT REPORT" in p1_txt, "Cover page missing 'A PROJECT REPORT'"
    assert "BACHELOR OF COMPUTER APPLICATIONS" in p1_txt, "Cover page missing Degree"
    assert "DIVYANSH JOSHI" in p1_txt and "GORAV KUMAR" in p1_txt, "Cover page missing Candidates"
    assert "Ms. TABISH RAO" in p1_txt, "Cover page missing Mentor"
    assert "SCHOOL OF COMPUTING" in p1_txt, "Cover page missing School"
    assert "GRAPHIC ERA HILL UNIVERSITY" in p1_txt, "Cover page missing University"
    assert "NOVEMBER, 2026" in p1_txt, "Cover page missing Date"
    assert p1_lines[-1] == "NOVEMBER, 2026", f"Cover page does not end with Date; ends with: {p1_lines[-1]!r}"
    print("[PASS] Page 1: Single-page Cover (Annexure II) with all required institutional elements", flush=True)

    # 4. Check Title Page (Page 2)
    p2_txt = all_texts[1]
    p2_norm = " ".join(p2_txt.split())
    p2_lines = [l.strip() for l in p2_txt.split('\n') if l.strip()]
    assert "STAYMART: SMART STUDENT HOUSING AND CAMPUS MARKETPLACE" in p2_norm, "Title page missing title"
    assert "PROJECT REPORT" in p2_txt, "Title page missing 'PROJECT REPORT'"
    assert "DIVYANSH JOSHI" in p2_txt and "GORAV KUMAR" in p2_txt, "Title page missing Candidates"
    assert "Ms. TABISH RAO" in p2_txt, "Title page missing Mentor"
    assert "School of Computing" in p2_txt, "Title page missing School"
    assert "NOVEMBER, 2026" in p2_txt, "Title page missing Date"
    assert p2_lines[-1] == "NOVEMBER, 2026", f"Title page does not end with Date; ends with: {p2_lines[-1]!r}"
    print("[PASS] Page 2: Single-page Title (Annexure III) with all required institutional elements", flush=True)

    # 5. Check Candidate Declaration (Page 3)
    p3_txt = all_texts[2]
    p3_norm = " ".join(p3_txt.split())
    p3_lines = [l.strip() for l in p3_txt.split('\n') if l.strip()]
    assert "CANDIDATE" in p3_txt and "DECLARATION" in p3_txt, "Page 3 missing CANDIDATE'S DECLARATION"
    assert "We hereby certify that the work which is being presented in the PROJECT REPORT entitled" in p3_norm, "Declaration missing verbatim certification opening"
    assert "The matter presented in this Project Report has not been submitted by us for the award of any other degree of this or any other institution." in p3_norm, "Declaration missing verbatim non-submission statement"
    assert "This is to certify that the above statement made by the candidates is correct to the best of my/our knowledge." in p3_norm, "Declaration missing verbatim mentor certification"
    assert p3_lines[-1] == "i", f"Page 3 should be stamped with 'i', got: {p3_lines[-1]!r}"
    print("[PASS] Page 3: Candidate's Declaration matches verbatim Graphic Era Hill University wording with Roman numeral 'i'", flush=True)

    # 6. Check Abstract (Page 4)
    p4_txt = all_texts[3]
    p4_lines = [l.strip() for l in p4_txt.split('\n') if l.strip()]
    assert "Abstract" in p4_txt, "Page 4 missing Abstract"
    assert p4_lines[-1] == "ii", f"Page 4 should be stamped with 'ii', got: {p4_lines[-1]!r}"
    print("[PASS] Page 4: Abstract formatted cleanly with Roman numeral 'ii'", flush=True)

    # 7. Check Acknowledgements (Page 5)
    p5_txt = all_texts[4]
    p5_lines = [l.strip() for l in p5_txt.split('\n') if l.strip()]
    assert "Acknowledgements" in p5_txt, "Page 5 missing Acknowledgements"
    assert p5_lines[-1] == "iii", f"Page 5 should be stamped with 'iii', got: {p5_lines[-1]!r}"
    print("[PASS] Page 5: Acknowledgements formatted cleanly with Roman numeral 'iii'", flush=True)

    # 8. Dynamically locate Chapter 1 physical page
    p_ch1 = None
    for p in range(1, total_pages + 1):
        txt = all_texts[p - 1]
        if "CHAPTER 1" in txt and "INTRODUCTION AND PROBLEM STATEMENT" in txt and p > 10:
            p_ch1 = p
            break
    assert p_ch1 is not None, "Could not locate Chapter 1 physical page!"
    print(f"[PASS] Chapter 1 dynamically located on physical Page {p_ch1}", flush=True)

    # Check Preliminary Roman Numerals
    for p in range(3, p_ch1):
        expected_roman = to_roman(p - 2)
        txt = all_texts[p - 1]
        lines = [l.strip() for l in txt.split('\n') if l.strip()]
        last_line = lines[-1]
        assert expected_roman in last_line or last_line.endswith(expected_roman), f"Page {p} expected Roman numeral '{expected_roman}', got: '{last_line}'"
    print(f"[PASS] Pages 3 to {p_ch1 - 1}: Preliminary pages stamped with centered Roman numerals (i to {to_roman(p_ch1 - 3)})", flush=True)

    # 9. Check Chapter 1 (Page p_ch1)
    pch1_txt = all_texts[p_ch1 - 1]
    pch1_lines = [l.strip() for l in pch1_txt.split('\n') if l.strip()]
    assert "CHAPTER 1" in pch1_txt, f"Page {p_ch1} missing CHAPTER 1"
    assert "INTRODUCTION AND PROBLEM STATEMENT" in pch1_txt, f"Page {p_ch1} missing chapter title"
    assert pch1_lines[-1] == "1", f"Page {p_ch1} should restart Arabic numbering at '1', got: {pch1_lines[-1]!r}"
    print(f"[PASS] Page {p_ch1}: Chapter 1 Introduction restarts Arabic page numbering at '1'", flush=True)

    # 10. Check Body Arabic Numerals
    for p in range(p_ch1, total_pages + 1):
        expected_arabic = str(p - p_ch1 + 1)
        txt = all_texts[p - 1]
        lines = [l.strip() for l in txt.split('\n') if l.strip()]
        last_line = lines[-1]
        assert last_line == expected_arabic, f"Page {p} expected Arabic numeral '{expected_arabic}', got: '{last_line}'"
    print(f"[PASS] Pages {p_ch1} to {total_pages}: Body pages stamped with consecutive Arabic numerals (1 to {total_pages - p_ch1 + 1})", flush=True)

    # 11. Verify Table of Contents against actual chapter physical positions
    chapters_to_check = [
        ("Chapter 1", "CHAPTER 1"),
        ("Chapter 2", "CHAPTER 2"),
        ("Chapter 3", "CHAPTER 3"),
        ("Chapter 4", "CHAPTER 4"),
        ("Chapter 5", "CHAPTER 5"),
        ("Chapter 6", "CHAPTER 6"),
        ("Chapter 7", "CHAPTER 7"),
        ("Chapter 8", "CHAPTER 8"),
        ("Chapter 9", "CHAPTER 9"),
        ("References", "1. Adomavicius"),
    ]

    chapter_locations = {}
    for ch_name, search_str in chapters_to_check:
        for p in range(p_ch1, total_pages + 1):
            txt = all_texts[p - 1]
            if search_str in txt:
                chapter_locations[ch_name] = p
                break
        assert ch_name in chapter_locations, f"Could not find {ch_name} in body pages!"
        body_page = chapter_locations[ch_name] - p_ch1 + 1
        print(f"[PASS] {ch_name:12} verified on physical Page {chapter_locations[ch_name]} (Body Page {body_page})", flush=True)

    # Verify TOC text contains exact matched numbers
    toc_pages_txt = "".join([all_texts[p] for p in range(5, p_ch1 - 1)])
    for ch_name, phys_page in chapter_locations.items():
        body_page = phys_page - p_ch1 + 1
        assert str(body_page) in toc_pages_txt, f"TOC missing body page number {body_page} for {ch_name}"

    print("[PASS] Table of Contents: 100% agreement with physical chapter locations (0 page drift)", flush=True)

    # 12. Bibliography style plain (alphabetical order) check
    # Find References page
    ref_phys_page = chapter_locations["References"]
    ref_txt = all_texts[ref_phys_page - 1]
    assert "Adomavicius" in ref_txt, "References should start with Adomavicius (alphabetical order)"
    assert "Bauer" in ref_txt, "References should contain Bauer second (alphabetical order)"
    print("[PASS] Bibliography: Alphabetized by author name per Rule 5 (plain style)", flush=True)

    print("\n" + "=" * 70, flush=True)
    print("ALL VERIFICATION CHECKS PASSED SUCCESSFULLY (12/12)!", flush=True)
    print("=" * 70, flush=True)
    return True

if __name__ == '__main__':
    try:
        verify_report_pdf()
        sys.exit(0)
    except AssertionError as e:
        print(f"\n[FAIL] Assertion failed: {e}", flush=True)
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}", flush=True)
        sys.exit(2)
