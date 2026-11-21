import asyncio
import os
from playwright.async_api import async_playwright

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PAGES = [
    "frontend/index.html",
    "frontend/search-properties.html",
    "frontend/search-products.html",
    "frontend/property-detail.html",
    "frontend/product-detail.html"
]
VIEWPORTS = [
    {"name": "mobile", "width": 375, "height": 667},
    {"name": "tablet", "width": 768, "height": 1024},
    {"name": "desktop", "width": 1280, "height": 800}
]

async def check():
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        all_passed = True
        for page_file in PAGES:
            abs_url = "file:///" + os.path.abspath(page_file).replace("\\", "/")
            print(f"\n--- Checking {page_file} ---")
            for vp in VIEWPORTS:
                page = await browser.new_page(viewport={"width": vp["width"], "height": vp["height"]})
                await page.goto(abs_url)
                await page.wait_for_timeout(300)
                
                # Check horizontal overflow
                overflow = await page.evaluate("""
                    () => {
                        const docWidth = document.documentElement.clientWidth;
                        const scrollWidth = document.documentElement.scrollWidth;
                        const bodyScrollWidth = document.body.scrollWidth;
                        const elements = Array.from(document.querySelectorAll('*'));
                        const overflowing = [];
                        for (const el of elements) {
                            const rect = el.getBoundingClientRect();
                            if (rect.right > docWidth + 1) { // 1px margin of error
                                overflowing.push({
                                    tag: el.tagName,
                                    id: el.id,
                                    class: el.className,
                                    right: Math.round(rect.right),
                                    docWidth
                                });
                            }
                        }
                        return {
                            hasScrollbar: scrollWidth > docWidth || bodyScrollWidth > docWidth,
                            docWidth,
                            scrollWidth,
                            bodyScrollWidth,
                            overflowingElementsCount: overflowing.length,
                            sampleOverflowing: overflowing.slice(0, 3)
                        };
                    }
                """)
                passed = not overflow["hasScrollbar"]
                status = "PASS" if passed else "FAIL"
                print(f"[{status}] {vp['name']} ({vp['width']}x{vp['height']}): clientWidth={overflow['docWidth']}, scrollWidth={overflow['scrollWidth']}, bodyScrollWidth={overflow['bodyScrollWidth']}, overflowingEls={overflow['overflowingElementsCount']}")
                if not passed:
                    print(f"       Details: {overflow['sampleOverflowing']}")
                    all_passed = False
                await page.close()
        await browser.close()
        return all_passed

if __name__ == "__main__":
    passed = asyncio.run(check())
    print("\nOVERALL PLAYWRIGHT OVERFLOW TEST RESULT:", "SUCCESS (ZERO OVERFLOW)" if passed else "FAILED")
    exit(0 if passed else 1)
