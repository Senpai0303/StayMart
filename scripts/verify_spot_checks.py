import os
import sys
import pypdf

PDF_PATH = r"D:\Mini5th\StayMart_Project_Report.pdf"

def main():
    reader = pypdf.PdfReader(PDF_PATH)
    total_pages = len(reader.pages)
    print(f"Total Pages in PDF: {total_pages}")
    
    # Locate Chapter 1
    p_ch1 = None
    for p in range(1, total_pages + 1):
        txt = reader.pages[p - 1].extract_text() or ""
        if "CHAPTER 1" in txt and "INTRODUCTION" in txt and p > 10:
            p_ch1 = p
            break
    print(f"Physical page for Chapter 1: {p_ch1}")
    assert p_ch1 == 14, f"Expected p_ch1 == 14, got {p_ch1}"

    # We will test entries across 3 categories: TOC, LOF, LOT
    test_cases = [
        # --- Category 1: TOC Chapters and Preliminary ---
        {"cat": "TOC", "name": "Abstract", "listed_page": "ii", "expected_phys": 4, "search": "Abstract"},
        {"cat": "TOC", "name": "Acknowledgements", "listed_page": "iii", "expected_phys": 5, "search": "Acknowledgements"},
        {"cat": "TOC", "name": "Contents", "listed_page": "iv", "expected_phys": 6, "search": "Contents"},
        {"cat": "TOC", "name": "List of Abbreviations", "listed_page": "vii", "expected_phys": 9, "search": "List of Abbreviations"},
        {"cat": "TOC", "name": "List of Figures", "listed_page": "x", "expected_phys": 12, "search": "List of Figures"},
        {"cat": "TOC", "name": "List of Tables", "listed_page": "xi", "expected_phys": 13, "search": "List of Tables"},
        {"cat": "TOC", "name": "Chapter 1 Introduction", "listed_page": "1", "expected_phys": 14, "search": "CHAPTER 1"},
        {"cat": "TOC", "name": "Chapter 2 Literature Review", "listed_page": "6", "expected_phys": 19, "search": "CHAPTER 2"},
        {"cat": "TOC", "name": "Chapter 3 System Requirements", "listed_page": "15", "expected_phys": 28, "search": "CHAPTER 3"},
        {"cat": "TOC", "name": "Chapter 4 Database Design", "listed_page": "24", "expected_phys": 37, "search": "CHAPTER 4"},
        {"cat": "TOC", "name": "Chapter 5 Backend & ML", "listed_page": "38", "expected_phys": 51, "search": "CHAPTER 5"},
        {"cat": "TOC", "name": "Chapter 6 Frontend UI/UX", "listed_page": "46", "expected_phys": 59, "search": "CHAPTER 6"},
        {"cat": "TOC", "name": "Chapter 7 Verification & Testing", "listed_page": "57", "expected_phys": 70, "search": "CHAPTER 7"},
        {"cat": "TOC", "name": "Chapter 8 Deployment & Cloud", "listed_page": "68", "expected_phys": 81, "search": "CHAPTER 8"},
        {"cat": "TOC", "name": "Chapter 9 Conclusion", "listed_page": "77", "expected_phys": 90, "search": "CHAPTER 9"},
        {"cat": "TOC", "name": "References", "listed_page": "80", "expected_phys": 93, "search": "References"},
        {"cat": "TOC", "name": "Appendix A: Backend Code", "listed_page": "83", "expected_phys": 96, "search": "APPENDIX A:"},
        {"cat": "TOC", "name": "Appendix B: Frontend Code", "listed_page": "92", "expected_phys": 105, "search": "APPENDIX B:"},
        {"cat": "TOC", "name": "Appendix C: SQL Schema", "listed_page": "97", "expected_phys": 110, "search": "APPENDIX C:"},
        {"cat": "TOC", "name": "Appendix D: API Catalog", "listed_page": "102", "expected_phys": 115, "search": "APPENDIX D:"},

        # --- Category 2: List of Figures ---
        {"cat": "LOF", "name": "Fig 1.1 High-Level Distributed Framework", "listed_page": "4", "expected_phys": 17, "search": "Figure 1.1"},
        {"cat": "LOF", "name": "Fig 2.1 Microservice Deployment Topology", "listed_page": "12", "expected_phys": 25, "search": "Figure 2.1"},
        {"cat": "LOF", "name": "Fig 3.1 DFD Level 0 Context Diagram", "listed_page": "15", "expected_phys": 28, "search": "Figure 3.1"},
        {"cat": "LOF", "name": "Fig 3.2 UML Sequence Diagram Booking", "listed_page": "19", "expected_phys": 32, "search": "Figure 3.2"},
        {"cat": "LOF", "name": "Fig 4.1 ER Diagram", "listed_page": "25", "expected_phys": 38, "search": "Figure 4.1"},
        {"cat": "LOF", "name": "Fig 5.1 Swagger UI OpenAPI 3.0", "listed_page": "39", "expected_phys": 52, "search": "Figure 5.1"},
        {"cat": "LOF", "name": "Fig 6.1 StayMart Public Landing Page", "listed_page": "47", "expected_phys": 60, "search": "Figure 6.1"},
        {"cat": "LOF", "name": "Fig 6.2 Faceted Search Portals", "listed_page": "53", "expected_phys": 66, "search": "Figure 6.2"},
        {"cat": "LOF", "name": "Fig 6.4 Personalized User Dashboard", "listed_page": "54", "expected_phys": 67, "search": "Figure 6.4"},
        {"cat": "LOF", "name": "Fig 6.6 Administrative Analytics Console", "listed_page": "56", "expected_phys": 69, "search": "Figure 6.6"},
        {"cat": "LOF", "name": "Fig 7.1 Accommodation Search", "listed_page": "64", "expected_phys": 77, "search": "Figure 7.1"},
        {"cat": "LOF", "name": "Fig 7.4 Peer-to-Peer Chat", "listed_page": "66", "expected_phys": 79, "search": "Figure 7.4"},
        {"cat": "LOF", "name": "Fig 8.1 Production Cloud Hosting Topology", "listed_page": "68", "expected_phys": 81, "search": "Figure 8.1"},

        # --- Category 3: List of Tables ---
        {"cat": "LOT", "name": "Table 2.1 Comparative Feature Matrix", "listed_page": "8", "expected_phys": 21, "search": "Table 2.1"},
        {"cat": "LOT", "name": "Table 3.1 Functional Requirements Spec", "listed_page": "17", "expected_phys": 30, "search": "Table 3.1"},
        {"cat": "LOT", "name": "Table 3.2 Operational Specifications", "listed_page": "22", "expected_phys": 35, "search": "Table 3.2"},
        {"cat": "LOT", "name": "Table 4.1 Data Dictionary users", "listed_page": "26", "expected_phys": 39, "search": "Table 4.1"},
        {"cat": "LOT", "name": "Table 4.4 Data Dictionary properties", "listed_page": "29", "expected_phys": 42, "search": "Table 4.4"},
        {"cat": "LOT", "name": "Table 4.6 Data Dictionary products", "listed_page": "33", "expected_phys": 46, "search": "Table 4.6"},
        {"cat": "LOT", "name": "Table 7.1 Software Test Execution Record", "listed_page": "59", "expected_phys": 72, "search": "Table 7.1"},
    ]

    passed = 0
    failed = 0

    print("\n" + "=" * 80)
    print(f"{'CAT':5} | {'ENTRY NAME':38} | {'LISTED':6} | {'PHYS':4} | {'STATUS':6} | {'EVIDENCE'}")
    print("=" * 80)

    for item in test_cases:
        expected_p = item["expected_phys"]
        actual_txt = reader.pages[expected_p - 1].extract_text() or ""
        lines = [l.strip() for l in actual_txt.splitlines() if l.strip()]
        stamped_num = lines[-1] if lines else ""
        
        # Check if search string is in text of that page
        found = item["search"].lower() in actual_txt.lower()

        # If not found on exact expected page, search neighboring pages (+-1) to detect drift
        drift = 0
        if not found:
            for d in [-1, 1, -2, 2]:
                np = expected_p + d
                if 1 <= np <= total_pages:
                    ntxt = reader.pages[np - 1].extract_text() or ""
                    if item["search"].lower() in ntxt.lower():
                        drift = d
                        break

        if found and stamped_num == item["listed_page"]:
            status = "PASS"
            passed += 1
            evidence = f"Found '{item['search']}', Stamped: '{stamped_num}'"
        else:
            status = "FAIL"
            failed += 1
            if not found:
                if drift != 0:
                    evidence = f"NOT on P{expected_p}! Found drifted by {drift:+d} on P{expected_p+drift}"
                else:
                    evidence = f"NOT found on P{expected_p} or neighbors!"
            else:
                evidence = f"Found '{item['search']}' but Stamped '{stamped_num}' != Listed '{item['listed_page']}'"

        print(f"{item['cat']:5} | {item['name'][:38]:38} | {item['listed_page']:6} | P{expected_p:<3} | {status:6} | {evidence}")

    print("=" * 80)
    print(f"RESULTS: {passed} PASSED, {failed} FAILED (Total: {len(test_cases)})")

    if failed == 0:
        print("\n[CONCLUSION] 100% PERFECT CONVERGENCE: Every single TOC, LOF, and LOT entry aligns with exact physical page and stamped page number!")
        sys.exit(0)
    else:
        print(f"\n[CONCLUSION] DRIFT DETECTED: {failed} entries misaligned.")
        sys.exit(1)

if __name__ == '__main__':
    main()
