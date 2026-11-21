# Milestone 1 Viewport & Layout Adversarial Challenge Report

## 1. Observation

### Test Execution Command & Environment
- **Automation Engine**: Google Chrome (v131.0.6778.205) headless via Playwright Core driver running on Node.js v22.14.0.
- **Verification Runner Script**: `d:\Mini5th\scripts\run_viewport_tests.js`
- **Output JSON Log**: `d:\Mini5th\scripts\viewport_test_results.json`
- **Execution Command**:
  ```powershell
  node scripts/run_viewport_tests.js
  ```

### Empirical Observations

#### Observation 1: High-Severity CSS Cascade Defect Hiding Mobile Hamburger Menu
In headless Chrome at 375px viewport (and 320px, 414px) on all five public pages (`frontend/index.html`, `frontend/search-properties.html`, `frontend/search-products.html`, `frontend/property-detail.html`, `frontend/product-detail.html`), `#mobileMenuToggle` has:
```json
{
  "id": "mobileMenuToggle",
  "exists": true,
  "display": "none",
  "visibility": "visible",
  "rect": { "x": 0, "y": 0, "width": 0, "height": 0 }
}
```
Direct tool observation from Playwright element click:
```
elementHandle.click: Timeout 30000ms exceeded.
Call log:
  - attempting click action
  - waiting for element to be visible, enabled and stable
    - element is not visible
```
Exact code lines in `frontend/css/global.css`:
- Line 1380 inside `@media (max-width: 768px)`:
  ```css
  .nav-mobile-toggle {
    display: flex;
  }
  ```
- Line 2126 OUTSIDE media query, placed 746 lines later in `frontend/css/global.css`:
  ```css
  .nav-mobile-toggle {
    display: none;
    width: 40px;
    height: 40px;
    ...
  }
  ```
- Because both rules share identical class selector specificity (`.nav-mobile-toggle`), CSS cascade source order dictates that line 2126 overrides line 1380, causing `#mobileMenuToggle` to have computed style `display: none` on mobile viewports.

#### Observation 2: Mobile Search Trigger Button Also Hidden
At 375px viewport on all five pages, `#mobileSearchTrigger` has computed style `display: "none"`.
Exact code lines in `frontend/css/global.css`:
- Line 1402 inside `@media (max-width: 768px)`:
  ```css
  .mobile-search-trigger {
    display: inline-flex;
    ...
  }
  ```
- Line 2155 OUTSIDE media query, placed 753 lines later in `frontend/css/global.css`:
  ```css
  .mobile-search-trigger {
    display: none;
  }
  ```
- Line 2155 unconditionally overrides line 1402 on all viewports.

#### Observation 3: Desktop Search Bar Form Crush & Overflow in Mobile Header
In `frontend/css/global.css`, lines 1395–1400:
```css
  .nav-center,
  .nav-links,
  .nav-location,
  .nav-actions .btn-olx-sell {
    display: none !important;
  }
```
The desktop form `<form class="nav-search-bar">` is a direct child of `.navbar-inner` (not inside `.nav-center`), so it remains rendered on mobile viewports alongside the brand logo. At 375px viewport:
```json
{
  "tag": "form",
  "className": "nav-search-bar",
  "display": "flex",
  "scrollWidth": 145,
  "clientWidth": 141,
  "overflowDelta": 4
}
```
The child elements (`<select id="navCatSelect">`, `<input id="navSearchInput">`, `<button class="nav-search-btn">`) are squeezed into 141px and internally overflow.

#### Observation 4: Adversarial Narrow Mobile (320px) Body Overflow on Homepage
On `frontend/index.html` at 320px viewport:
- `document.documentElement.scrollWidth`: 320px (clipped by `html { overflow-x: hidden }`)
- `document.body.scrollWidth`: 338px
- `document.body.clientWidth`: 320px
- Protruding elements: `<section class="hero">` (scrollWidth=338, clientWidth=320) and `.container` (scrollWidth=338, clientWidth=320).

#### Observation 5: Validated Passing Features
1. **Zero Inline Grid**: All HTML files in `frontend/` scan 0 occurrences of inline `grid-template-columns: 260px` or any inline `grid-template-columns`.
2. **CSS Token Completeness**: 54 unique CSS custom properties defined in `:root`. All `var(--...)` usages in `frontend/css/global.css` and `frontend/css/dashboard.css` resolve to defined tokens (0 undefined / missing tokens).
3. **Broken Redirects Elimination**: 0 occurrences of `my-bookings.html`, `my-orders.html`, or `messages.html` across all frontend HTML and JS files.
4. **Document Horizontal Overflow**:
   - `search-properties.html`: 0px horizontal overflow across 320px, 375px, 414px, 768px, 1280px, 1920px.
   - `search-products.html`: 0px horizontal overflow across 320px, 375px, 414px, 768px, 1280px, 1920px.
   - `property-detail.html`: 0px horizontal overflow across 320px, 375px, 414px, 768px, 1280px, 1920px.
   - `product-detail.html`: 0px horizontal overflow across 320px, 375px, 414px, 768px, 1280px, 1920px.
   - `index.html`: 0px horizontal overflow at 375px, 768px, 1280px.
5. **Interactive Controls Functionality**:
   - Filter drawer sheet opens cleanly on click (`.mobile-filter-toggle` -> `.filter-sidebar.open`, scrollWidth=375px, clientWidth=375px).
   - Sticky bottom action bar on detail pages renders with `position: fixed; bottom: 0px` on mobile (< 768px) and `display: none` on desktop (1280px).
   - Bottom booking and order sheets trigger and open with zero layout overflow.
   - Post chooser sheet modal triggers and opens with zero layout overflow.

---

## 2. Logic Chain

1. **Pre-condition**: Requirement R1 and Feature 2 ("Mobile Navigation Overhaul") require a functional mobile header and slide-out hamburger drawer for mobile viewports (< 768px).
2. **Cascade Breakdown**:
   - At line 1380 of `global.css`, `.nav-mobile-toggle` is styled with `display: flex` inside `@media (max-width: 768px)`.
   - However, at line 2126 of `global.css`, a second definition `.nav-mobile-toggle` with `display: none` is declared in global scope (unscoped by any media query).
   - Under standard CSS cascade specificity rules (W3C CSS Cascading and Inheritance Level 4), when two declarations have equal specificity, the later declaration wins.
   - Therefore, on a 375px mobile screen, the browser computes `display: none` for `#mobileMenuToggle`.
3. **User Impact**: Because the button has `width: 0`, `height: 0`, and `display: none`, a student browsing on a smartphone cannot see or tap the hamburger icon. The slide-out navigation drawer `#mobileDrawer` cannot be opened via normal user interaction.
4. **Secondary Impact**: The exact same cascade bug affects `.mobile-search-trigger` (line 1402 vs line 2155), preventing users from triggering mobile search. Furthermore, `.nav-search-bar` is not hidden on mobile, leaving a crushed search bar in the header.
5. **Conclusion from Chain**: Milestone 1 cannot be approved in its current state because the core mobile navigation requirement (Feature 2) is rendered inoperative by this stylesheet bug.

---

## 3. Caveats

- Backend Java APIs and unit tests were not affected; all 13 backend unit tests continue to pass with exit code 0.
- When invoked programmatically via JavaScript (`window.openMobileDrawer()`), the drawer element transitions smoothly and causes no horizontal overflow. The bug is strictly located in the CSS cascade rules governing the header triggers.
- The 320px narrow mobile overflow on `index.html` is masked on desktop browsers by `overflow-x: hidden` on `<html>`, but on physical iOS WebKit devices it can cause rubber-banding if child widths exceed viewport width.

---

## 4. Conclusion

### Explicit Verdict: **REJECT**

Milestone 1 is **REJECTED** due to a blocking defect in Feature 2 (Mobile Navigation Overhaul).

### Required Corrective Actions for Worker:
1. In `frontend/css/global.css`:
   - Either wrap lines 2126–2157 inside `@media (min-width: 769px) { ... }`, or move the base desktop definitions (`display: none`) before the `@media (max-width: 768px)` breakpoint, or increase the specificity / add `display: flex !important;` inside `@media (max-width: 768px)`.
   - Ensure `#mobileMenuToggle` computes to `display: flex` and `#mobileSearchTrigger` computes to `display: inline-flex` on all screens `<= 768px`.
2. In `frontend/css/global.css` line 1395:
   - Add `.navbar .nav-search-bar` to `display: none !important;` under `@media (max-width: 768px)` so that the desktop search bar does not crowd the 58px mobile header.
3. In `frontend/css/global.css`:
   - Ensure `.hero` container on `index.html` has `max-width: 100%` and `box-sizing: border-box` to avoid the 338px scrollWidth anomaly on 320px viewports.

---

## 5. Verification Method

To independently reproduce and verify this finding:

1. **Execute Headless Chrome Layout & Visibility Stress Harness**:
   ```powershell
   node scripts/run_viewport_tests.js
   ```
   *Expected Output*:
   ```
   [PAGE: index.html] at 375px:
     mobileMenuToggle: display='none' (EXPECTED: 'flex')
     mobileSearchTrigger: display='none' (EXPECTED: 'inline-flex')
   OVERALL VERDICT: REJECT
   ```

2. **Direct Single-Command Playwright Check**:
   ```powershell
   node -e '
   const { chromium } = require("C:/Users/divya/AppData/Local/Programs/Python/Python312/Lib/site-packages/playwright/driver/package");
   (async () => {
     const browser = await chromium.launch({ channel: "chrome", headless: true });
     const page = await browser.newPage({ viewport: { width: 375, height: 667 } });
     await page.goto("file:///d:/Mini5th/frontend/index.html");
     const display = await page.evaluate(() => window.getComputedStyle(document.getElementById("mobileMenuToggle")).display);
     console.log("Computed display of #mobileMenuToggle at 375px:", display);
     await browser.close();
   })();
   '
   ```
   *Expected Output*: `Computed display of #mobileMenuToggle at 375px: none` (Confirming bug).
