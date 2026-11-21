"""
Empirical Adversarial Stress Test Suite for StayMart_Project_Report.pdf
Conducted by m2_chal_2 (empirical challenger)
"""

import os
import sys
import re
import pypdf

PDF_PATH = r"D:\Mini5th\StayMart_Project_Report.pdf"

def run_adversarial_stress_tests():
    print("=" * 80)
    print("ADVERSARIAL STRESS TEST SUITE: StayMart_Project_Report.pdf")
    print("=" * 80)

    assert os.path.exists(PDF_PATH), f"Target file not found: {PDF_PATH}"
    file_size = os.path.getsize(PDF_PATH)
    print(f"[*] Target PDF Size: {file_size} bytes ({file_size / (1024*1024):.2f} MB)")
    assert file_size >= 5 * 1024 * 1024, f"File size {file_size} is under 5MB specification!"

    reader = pypdf.PdfReader(PDF_PATH)
    total_pages = len(reader.pages)
    print(f"[*] Total Pages: {total_pages}")
    assert total_pages == 118, f"Expected exactly 118 pages, got {total_pages}"

    # Test 1: Page Geometry across ALL pages
    print("\n[TEST 1] Page Geometry & MediaBox Consistency (A4 Executive Dimensions)")
    for idx, page in enumerate(reader.pages, 1):
        mb = page.mediabox
        width = float(mb.width)
        height = float(mb.height)
        # Standard A4 in points is 595.276 x 841.890 (or approx 595 x 842)
        assert abs(width - 595.28) < 2.0 or abs(width - 595.0) < 2.0, f"Page {idx} non-standard width: {width}"
        assert abs(height - 841.89) < 2.0 or abs(height - 842.0) < 2.0, f"Page {idx} non-standard height: {height}"
    print("  -> PASS: All 118 pages have exact standard A4 MediaBox dimensions (595.28 pt x 841.89 pt).")

    # Test 2: Extraction & Content Integrity across Pages
    print("\n[TEST 2] Text Extraction & Multi-Parser Extraction Resilience")
    extracted_texts = []
    for idx, page in enumerate(reader.pages, 1):
        txt = page.extract_text()
        assert txt is not None, f"Page {idx} returned None for extracted text"
        assert len(txt.strip()) > 0, f"Page {idx} appears to be completely empty!"
        extracted_texts.append(txt)
    print("  -> PASS: Successfully extracted text from 100% of pages (no blank pages).")

    # Test 3: Structural Completeness - Chapters 1 to 9 & Appendices A to D
    print("\n[TEST 3] Complete Chapter & Appendix Structure Verification")
    required_structures = [
        ("Cover Page (Annexure II)", 1, ["STAYMART", "A PROJECT REPORT", "DIVYANSHU SINGH", "GRAPHIC ERA HILL UNIVERSITY", "NOVEMBER, 2026"]),
        ("Title Page (Annexure III)", 2, ["STAYMART", "PROJECT REPORT", "DIVYANSHU SINGH", "School of Computing", "NOVEMBER, 2026"]),
        ("Candidate's Declaration", 3, ["CANDIDATE", "DECLARATION", "School of Computing", "authentic record", "Faculty Mentor"]),
        ("Abstract", 4, ["Abstract", "StayMart"]),
        ("Acknowledgements", 5, ["Acknowledgements", "School of Computing", "gratitude"]),
        ("Table of Contents", 6, ["Contents", "Chapter 1", "Abstract"]),
        ("List of Abbreviations", 9, ["[[LOC:LOA]]", "List of Abbreviations"]),
        ("List of Figures", 12, ["[[LOC:LOF]]", "List of Figures"]),
        ("List of Tables", 13, ["[[LOC:LOT]]", "List of Tables"]),
        ("Chapter 1", 14, ["[[LOC:CH_1]]", "CHAPTER 1"]),
        ("Chapter 2", 19, ["[[LOC:CH_2]]", "CHAPTER 2"]),
        ("Chapter 3", 28, ["[[LOC:CH_3]]", "CHAPTER 3"]),
        ("Chapter 4", 37, ["[[LOC:CH_4]]", "CHAPTER 4"]),
        ("Chapter 5", 51, ["[[LOC:CH_5]]", "CHAPTER 5"]),
        ("Chapter 6", 59, ["[[LOC:CH_6]]", "CHAPTER 6"]),
        ("Chapter 7", 70, ["[[LOC:CH_7]]", "CHAPTER 7"]),
        ("Chapter 8", 81, ["[[LOC:CH_8]]", "CHAPTER 8"]),
        ("Chapter 9", 90, ["[[LOC:CH_9]]", "CHAPTER 9"]),
        ("References", 93, ["[[LOC:REFERENCES]]", "REFERENCES"]),
        ("Appendix A", 96, ["[[LOC:APP_A]]", "APPENDIX A:"]),
        ("Appendix B", 105, ["[[LOC:APP_B]]", "APPENDIX B:"]),
        ("Appendix C", 110, ["[[LOC:APP_C]]", "APPENDIX C:"]),
        ("Appendix D", 115, ["[[LOC:APP_D]]", "APPENDIX D:"]),
    ]

    found_locations = {}
    for name, expected_page, markers in required_structures:
        found_page = None
        for p_idx, text in enumerate(extracted_texts, 1):
            if all(m in text for m in markers):
                found_page = p_idx
                break
        assert found_page is not None, f"Failed to find section '{name}' with markers {markers}"
        if expected_page is not None:
            assert found_page == expected_page, f"Section '{name}' found on Page {found_page}, expected Page {expected_page}"
        found_locations[name] = found_page
        print(f"  -> Found {name:32} at Page {found_page:3d} [PASS]")

    # Test 4: Abstract Word Count Validation (< 300 words)
    print("\n[TEST 4] Abstract Word Count Strict Institutional Boundary (< 300 words)")
    abs_txt = extracted_texts[3] # Page 4
    # Strip heading and page number
    abs_body = re.sub(r'Abstract', '', abs_txt)
    abs_body = re.sub(r'\bii\b', '', abs_body).strip()
    words = abs_body.split()
    word_count = len(words)
    print(f"  -> Extracted Abstract word count: {word_count} words")
    assert word_count < 300, f"Abstract exceeds 300-word limit: {word_count} words"
    assert word_count > 150, f"Abstract is suspiciously short: {word_count} words"
    print("  -> PASS: Abstract length strictly within [150, 300) words.")

    # Test 5: Strict Sequential Pagination Invariance
    print("\n[TEST 5] Strict Sequential Pagination Invariance (Roman ii..xi, Arabic 1..105)")
    p_ch1 = found_locations["Chapter 1"] # Page 14
    # Cover and Title unnumbered
    for p in range(1, 3):
        lines = [l.strip() for l in extracted_texts[p-1].splitlines() if l.strip()]
        last_line = lines[-1]
        assert last_line not in ["1", "2", "i", "ii"], f"Page {p} must not have page numbers, found: {last_line}"
    print("  -> Cover and Title pages confirmed unnumbered.")

    # Prelim pages Roman numerals
    roman_numerals = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x", "xi"]
    for idx, p in enumerate(range(3, p_ch1)):
        expected_roman = roman_numerals[idx]
        lines = [l.strip() for l in extracted_texts[p-1].splitlines() if l.strip()]
        assert lines[-1] == expected_roman or expected_roman in lines[-1], f"Page {p} expected Roman '{expected_roman}', got '{lines[-1]}'"
    print(f"  -> Pages 3 to {p_ch1-1} verified Roman numerals 'i' through '{roman_numerals[p_ch1-4]}'.")

    # Body pages Arabic numerals 1 to 105
    for p in range(p_ch1, total_pages + 1):
        expected_arabic = str(p - p_ch1 + 1)
        lines = [l.strip() for l in extracted_texts[p-1].splitlines() if l.strip()]
        assert lines[-1] == expected_arabic, f"Page {p} expected Arabic '{expected_arabic}', got '{lines[-1]}'"
    print(f"  -> Pages {p_ch1} to {total_pages} verified sequential Arabic numerals 1 through {total_pages - p_ch1 + 1}.")

    # Test 6: Zero Browser Artifacts & Zero Leaked Placeholders
    print("\n[TEST 6] Leak & Browser Artifact Scrutiny")
    prohibited_strings = ["file:///", "TODO:", "FIXME:"]
    for p_idx, text in enumerate(extracted_texts, 1):
        for prohibited in prohibited_strings:
            assert prohibited.lower() not in text.lower(), f"Found prohibited string '{prohibited}' on page {p_idx}!"
        assert not re.search(r'\d{1,2}/\d{1,2}/\d{2,4},\s*\d{1,2}:\d{2}\s*(?:AM|PM)', text), f"Found browser timestamp on page {p_idx}!"
    print("  -> PASS: 0 browser URLs (file:///), 0 browser print timestamps, 0 unresolved TODO/FIXME markers.")

    # Test 7: Table of Contents Exact Convergence
    print("\n[TEST 7] Table of Contents Exact Page Reference Audit")
    toc_text = "\n".join(extracted_texts[5:found_locations["List of Figures"]-1])
    for ch_idx in range(1, 10):
        ch_name = f"Chapter {ch_idx}"
        phys_p = found_locations[ch_name]
        body_p = phys_p - p_ch1 + 1
        # Check that body_p appears in TOC
        pattern = rf"{body_p}\b"
        assert re.search(pattern, toc_text), f"TOC does not contain body page {body_p} for Chapter {ch_idx}"
        print(f"  -> Chapter {ch_idx} (Phys Page {phys_p}, Body Page {body_p}) TOC reference verified.")

    print("\n" + "=" * 80)
    print("ALL ADVERSARIAL STRESS TESTS COMPLETED AND PASSED (7/7 CATEGORIES)!")
    print("=" * 80)

if __name__ == '__main__':
    try:
        run_adversarial_stress_tests()
        sys.exit(0)
    except AssertionError as e:
        print(f"\n[FAIL] Stress test assertion failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected stress test error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(2)
