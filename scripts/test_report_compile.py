import subprocess
import pypdf
import os

TEMP_TEST_HTML = r"D:\Mini5th\report\compiled\test_report.html"
TEMP_TEST_PDF = r"D:\Mini5th\report\compiled\test_report.pdf"

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def test_compile(html_content):
    with open(TEMP_TEST_HTML, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    temp_user_dir = r"C:\Users\divya\AppData\Local\Temp\chrome_test_profile"
    cmd = [
        CHROME,
        "--headless",
        "--no-sandbox",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--user-data-dir={temp_user_dir}",
        f"--print-to-pdf={TEMP_TEST_PDF}",
        f"file:///{TEMP_TEST_HTML.replace(os.sep, '/')}"
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    reader = pypdf.PdfReader(TEMP_TEST_PDF)
    print(f"Test PDF compiled: {len(reader.pages)} pages")
    return len(reader.pages)

if __name__ == '__main__':
    import sys
    sys.path.insert(0, 'scripts')
    import compile_report_pdf
    doc = compile_report_pdf.build_html_document(page_map=None)
    test_compile(doc)
