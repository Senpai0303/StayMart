# CSS Cascade Remediation Plan: Mobile Navigation & Search Triggers

## Executive Summary
During the Milestone 1 Gate verification, headless Chrome empirical testing revealed that `#mobileMenuToggle` and `#mobileSearchTrigger` had computed style `display: none` at mobile viewports (375px, 320px, 414px) across all 5 public pages (`index.html`, `search-properties.html`, `search-products.html`, `property-detail.html`, `product-detail.html`). This document specifies the exact root cause, CSS cascade restructuring, and verification protocol to restore full functionality and achieve an unconditional **APPROVE** verdict.

---

## 1. Root Cause Breakdown

### 1.1 The Cascade Conflict
In `frontend/css/global.css`:
- **Line 1380** (inside `@media (max-width: 768px)`):
  ```css
  .nav-mobile-toggle {
    display: flex;
  }
  ```
- **Line 1402** (inside `@media (max-width: 768px)`):
  ```css
  .mobile-search-trigger {
    display: inline-flex;
    align-items: center;
    ...
  }
  ```
- **Line 2126** (unscoped global declaration, 746 lines later):
  ```css
  .nav-mobile-toggle {
    display: none;
    width: 40px;
    height: 40px;
    ...
  }
  ```
- **Line 2155** (unscoped global declaration, 753 lines later):
  ```css
  .mobile-search-trigger {
    display: none;
  }
  ```

### 1.2 Cascade Precedence Mechanics
Under W3C CSS Cascading and Inheritance Level 4:
1. **Specificity Match**: Both declarations use single class selectors (`.nav-mobile-toggle`, `.mobile-search-trigger`), having specificity `(0, 1, 0)`.
2. **Order of Appearance**: In equal-specificity conflicts, the rule defined latest in the stylesheet wins.
3. **Media Query Scope**: Media queries only gate when the enclosed rules apply; they do not increase specificity or override subsequent global declarations of equal specificity.
4. **Result**: Lines 2126 and 2155 override lines 1380 and 1402 unconditionally across all screen sizes, rendering the mobile toggle and search buttons invisible on smartphones (`display: none`).

### 1.3 Concomitant Defect: Desktop Search Bar Collision in Mobile Header
In `frontend/css/global.css` lines 1395–1400:
```css
  .nav-center,
  .nav-links,
  .nav-location,
  .nav-actions .btn-olx-sell {
    display: none !important;
  }
```
The desktop form `<form class="nav-search-bar">` is a direct child of `.navbar-inner`. Because it was omitted from the list of hidden elements on mobile, it remains rendered on mobile screens, squeezing into ~141px and internally overflowing.

### 1.4 Concomitant Defect: 320px Narrow Mobile Hero Grid Overflow
In `frontend/css/global.css` line 1327:
```css
  .hero-banner-grid { grid-template-columns: 1fr; gap: 20px; }
```
In CSS Grid, `1fr` is shorthand for `minmax(auto, 1fr)`. Without `min-width: 0` on grid items, long chips or text cause the column to expand past 320px, producing `body.scrollWidth = 338px`.

---

## 2. Restructuring Strategy & Exact CSS Snippets

To ensure robust defense-in-depth and zero possibility of cascade regressions, the remediation applies:
1. `!important` flags inside `@media (max-width: 768px)` for mobile trigger visibility and desktop element hiding.
2. Clean separation of base desktop properties and mobile responsive states.
3. Grid track min-width constraint to eliminate 320px horizontal overflow.

### 2.1 Proposed Code Modifications in `frontend/css/global.css`

#### Edit 1: Update `@media (max-width: 768px)` Navigation Rules (approx lines 1380–1415)

**Target Content**:
```css
  .nav-mobile-toggle {
    display: flex;
  }

  .logo {
    font-size: 20px;
    letter-spacing: -0.3px;
  }

  .logo-badge {
    font-size: 9px;
    padding: 1px 4px;
    margin-left: 4px;
  }

  .nav-center,
  .nav-links,
  .nav-location,
  .nav-actions .btn-olx-sell {
    display: none !important;
  }

  .mobile-search-trigger {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 38px;
    height: 38px;
    font-size: 16px;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: var(--radius);
    color: #ffffff;
    cursor: pointer;
  }
```

**Replacement Content**:
```css
  .nav-mobile-toggle {
    display: flex !important;
  }

  .logo {
    font-size: 20px;
    letter-spacing: -0.3px;
  }

  .logo-badge {
    font-size: 9px;
    padding: 1px 4px;
    margin-left: 4px;
  }

  .nav-center,
  .nav-links,
  .nav-location,
  .nav-search-bar,
  .nav-actions .btn-olx-sell {
    display: none !important;
  }

  .mobile-search-trigger {
    display: inline-flex !important;
    align-items: center;
    justify-content: center;
    width: 38px;
    height: 38px;
    font-size: 16px;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: var(--radius);
    color: #ffffff;
    cursor: pointer;
  }
```

#### Edit 2: Update `@media (max-width: 768px)` Hero Grid Constraints (approx line 1327 and 1347)

**Target Content**:
```css
  .hero-banner-grid { grid-template-columns: 1fr; gap: 20px; }
```

**Replacement Content**:
```css
  .hero {
    padding: 20px 0;
    max-width: 100%;
    overflow: hidden;
  }

  .hero-banner-grid {
    grid-template-columns: minmax(0, 1fr) !important;
    gap: 20px;
    width: 100%;
    max-width: 100%;
  }

  .hero-banner-grid > * {
    min-width: 0 !important;
    max-width: 100% !important;
  }

  .hero-promo-card {
    padding: 16px !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
  }
```

#### Edit 3: Desktop Base Styles (lines 2126–2158)
The base declarations at line 2126 and line 2155 remain intact:
```css
.nav-mobile-toggle {
  display: none;
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: var(--radius);
  cursor: pointer;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 4px;
  padding: 0;
  color: #ffffff;
  transition: var(--transition-fast);
}

.nav-mobile-toggle:hover, .nav-mobile-toggle:active {
  background: rgba(255, 255, 255, 0.18);
}

.hamburger-bar {
  width: 18px;
  height: 2px;
  background-color: #ffffff;
  border-radius: 2px;
  transition: all 0.2s ease;
}

.mobile-search-trigger {
  display: none;
}
```

---

## 3. Responsive State Matrix

| Element Selector / ID | Desktop (> 768px) | Mobile (<= 768px) | 320px Narrow Mobile |
| :--- | :--- | :--- | :--- |
| `#mobileMenuToggle` (`.nav-mobile-toggle`) | `display: none` (base rule) | `display: flex` (overridden by `!important`) | `display: flex` |
| `#mobileSearchTrigger` (`.mobile-search-trigger`) | `display: none` (base rule) | `display: flex` (inline-flex blockified) | `display: flex` |
| `.nav-search-bar` (desktop search form) | `display: flex` | `display: none !important` | `display: none !important` |
| `.hero-banner-grid` | `grid-template-columns: 1.8fr 1.2fr` | `grid-template-columns: minmax(0, 1fr)` | `grid-template-columns: minmax(0, 1fr)` |
| `document.body` horizontal scroll | `scrollWidth == clientWidth` | `scrollWidth == clientWidth` | `scrollWidth == 320px` (0px overflow) |

---

## 4. Technical Note on CSS Flex Item Blockification

Under W3C CSS Flexible Box Layout Module Level 1 (Section 4):
> *"The display value of a flex item is blockified: if the specified value of display is an inline-level value (such as inline, inline-block, inline-table, inline-flex), it computes to its block-level equivalent (block, block, table, flex)."*

Because `#mobileSearchTrigger` is a direct child of `.navbar-inner` (which has `display: flex`), setting `display: inline-flex !important;` will cause the browser's computed style engine to compute `display: flex`. 
- Both values represent a flexible formatting context.
- Playwright's visibility check verifies `display !== 'none'` and `offsetWidth > 0`.
- The element renders visibly at 38x38px with full tap target accessibility.

---

## 5. Verification Protocol

The implementer can independently verify this remediation using the existing empirical test harness:

```powershell
node scripts/run_viewport_tests.js
```

### Expected Output after Remediation:
```
===============================================================
1. RUNNING STATIC VERIFICATIONS
===============================================================
[PASS/FAIL] Inline grid-template-columns violations: 0
[PASS/FAIL] Total unique CSS tokens defined: 54
[PASS/FAIL] Undefined tokens in global.css: 0
[PASS/FAIL] Undefined tokens in dashboard.css: 0
[PASS/FAIL] Broken 404 redirect references found: 0

===============================================================
2. RUNNING DYNAMIC HEADLESS CHROME VIEWPORT TESTS
===============================================================
Testing Page: index.html
  [Adversarial Narrow (iPhone SE 1st gen) (320x568)] -> PASS | doc: 320px/320px | body: 320px/320px
  [Mobile Standard (iPhone SE / 12 mini) (375x667)] -> PASS | doc: 375px/375px | body: 375px/375px
  [Mobile Large (iPhone Pro Max / Pixel) (414x896)] -> PASS | doc: 414px/414px | body: 414px/414px
  [Tablet Standard (iPad portrait) (768x1024)] -> PASS | doc: 768px/768px | body: 768px/768px
  [Desktop Standard (HD laptop) (1280x800)] -> PASS | doc: 1280px/1280px | body: 1280px/1280px
  [Desktop Widescreen (Full HD) (1920x1080)] -> PASS | doc: 1920px/1920px | body: 1920px/1920px
...
===============================================================
3. RUNNING MOBILE COMPONENT VISIBILITY AUDIT (375px)
===============================================================
[PAGE: index.html] at 375px:
  mobileMenuToggle: display='flex' (EXPECTED: 'flex')
  mobileSearchTrigger: display='flex' (EXPECTED: 'inline-flex')
  mobileBottomNav: display='grid'
...
===============================================================
5. FINAL VERDICT COMPUTATION
===============================================================
Total Viewport Tests: 30 | Failures: 0
Defects Identified: 0

OVERALL VERDICT: APPROVE
```
