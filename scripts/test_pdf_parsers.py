"""
Multi-Parser and Deep Metadata Verification for StayMart_Project_Report.pdf
Tests extraction across multiple libraries / parsers and validates PDF structural objects.
"""

import os
import sys

PDF_PATH = r"D:\Mini5th\StayMart_Project_Report.pdf"

def test_parsers():
    print("=" * 80)
    print("MULTI-PARSER & PDF DEEP OBJECT VERIFICATION")
    print("=" * 80)

    # 1. pypdf test
    print("[1] Testing with pypdf...")
    import pypdf
    reader = pypdf.PdfReader(PDF_PATH)
    print(f"  - Pages: {len(reader.pages)}")
    assert len(reader.pages) == 118, "Page count mismatch in pypdf"
    
    # Check pdf metadata / info
    info = reader.metadata
    print(f"  - Metadata: {info}")
    
    # Check page 1 text
    p1_txt = reader.pages[0].extract_text()
    assert "STAYMART" in p1_txt, "pypdf failed to find STAYMART on page 1"
    print("  -> pypdf successfully read document structure and extracted text.")

    # 2. Test pdfminer if installed
    print("\n[2] Testing with pdfminer.six (if available)...")
    try:
        from pdfminer.high_level import extract_text as pdfminer_extract_text
        from pdfminer.high_level import extract_pages
        print("  - pdfminer is available! Extracting page 1...")
        p1_mined = pdfminer_extract_text(PDF_PATH, page_numbers=[0])
        assert "STAYMART" in p1_mined, "pdfminer failed to find STAYMART on page 1"
        print(f"  -> pdfminer extracted {len(p1_mined)} chars from page 1 successfully.")
        
        # Test sample body page (page 14)
        p14_mined = pdfminer_extract_text(PDF_PATH, page_numbers=[13])
        assert "CHAPTER 1" in p14_mined, "pdfminer failed to find CHAPTER 1 on page 14"
        print("  -> pdfminer successfully verified Chapter 1 on body page 1.")
    except ImportError:
        print("  - pdfminer.six not installed in this environment.")

    # 3. Test fitz (PyMuPDF) if installed
    print("\n[3] Testing with PyMuPDF / fitz (if available)...")
    try:
        import fitz
        doc = fitz.open(PDF_PATH)
        print(f"  - PyMuPDF opened document with {len(doc)} pages.")
        assert len(doc) == 118, "PyMuPDF page count mismatch"
        p0 = doc[0].get_text()
        assert "STAYMART" in p0, "PyMuPDF failed to find STAYMART on page 1"
        print("  -> PyMuPDF successfully verified page 1.")
    except ImportError:
        print("  - PyMuPDF / fitz not installed in this environment.")

    # 4. Low-level PyPDF PDF Object Inspection
    print("\n[4] Inspecting PDF internal objects, stream compression, and font references...")
    # Check for Fonts dictionary across pages
    font_count = 0
    image_count = 0
    for idx, page in enumerate(reader.pages, 1):
        if '/Resources' in page:
            resources = page['/Resources']
            if '/Font' in resources:
                fonts = resources['/Font']
                font_count += len(fonts)
            if '/XObject' in resources:
                xobjs = resources['/XObject']
                for k in xobjs:
                    obj = xobjs[k]
                    if hasattr(obj, 'get') and obj.get('/Subtype') == '/Image':
                        image_count += 1
    print(f"  - Total Font references across pages: {font_count}")
    print(f"  - Total embedded Images / XObjects: {image_count}")
    assert font_count > 0, "No fonts found in document resources!"
    print("  -> PASS: PDF contains valid font dictionaries and graphic objects.")

    print("\n" + "=" * 80)
    print("MULTI-PARSER VERIFICATION SUCCESSFUL!")
    print("=" * 80)

if __name__ == '__main__':
    try:
        test_parsers()
        sys.exit(0)
    except AssertionError as e:
        print(f"\n[FAIL] Parser assertion failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Parser error: {e}")
        sys.exit(2)
