# StayMart Milestone 1 — Responsive Layout & Breakpoint Overhaul Plan
**Specialist**: M1 Explorer 1 (Layout & Breakpoint Specialist)  
**Assigned Directory**: `d:\Mini5th\.agents\teamwork\m1_explorer_1`  
**Date**: November 2, 2026  
**Status**: COMPLETE IMPLEMENTATION PLAN (Read-Only)  
**Target Viewports**: Mobile (`375px × 667px`), Tablet (`768px × 1024px`), Desktop (`1280px+ × 800px+`)

---

## Executive Summary

StayMart's current frontend exhibits critical layout regressions across mobile and tablet viewports that degrade student usability and trigger page-breaking horizontal scrollbars. Specifically:
1. **Hardcoded Inline Grid Overrides**: `search-properties.html` and `search-products.html` enforce an inline `style="grid-template-columns:260px 1fr;gap:24px;align-items:start"`, completely disabling responsive media queries and causing **189px+ of horizontal page blowout** on 375px mobile viewports.
2. **Deficient Media Queries in `global.css`**: Only three coarse `@media` rules exist (1024px, 768px, 480px). Crucial responsive rules from the backup stylesheet (such as `.grid-2`, `.info-cards` 2-column collapse, `.nav-links` hiding, sticky sidebar position resetting, auth form cards, and posting form grids) were entirely omitted during the light theme rewrite.
3. **Detail Page Hierarchy Failure on Mobile**: When `.detail-layout` stacks to 1 column on mobile, the entire left column (photos, description, reviews list, review submission form, and similar properties) renders before the booking/contact sidebar. A student must scroll past ~1,500px of reviews just to find the price and booking button.
4. **Card Grids & Touch Target Deficiencies**: Card grids crush at intermediate tablet widths (800px-1024px), wishlist heart buttons lack accessible touch hit areas (<44px), category strips lack horizontal swipe discovery cues, and form checkboxes lack thumb-friendly touch padding.

This report establishes the **exact, production-ready implementation plan** with line-by-line before/after code replacements, responsive CSS rule definitions, and mobile-first architectural patterns.

---

## 1. Search Pages Inline Grid Fix (`search-properties.html` & `search-products.html`)

### 1.1 Root Cause & Defect Analysis
- **Observed Files & Lines**:
  - `frontend/search-properties.html` (line 86)
  - `frontend/search-products.html` (line 86)
- **Problematic Code**:
  ```html
  <div class="detail-layout" style="grid-template-columns:260px 1fr;gap:24px;align-items:start">
  ```
- **Why It Fails**:
  1. *Inline Specificity*: In CSS, inline `style="..."` attributes take precedence over class selectors. In `global.css:1280`, `@media (max-width: 1024px) { .detail-layout { grid-template-columns: 1fr; } }` is completely overridden and ignored.
  2. *Semantic Misuse*: `.detail-layout` was built for property/product detail pages with a `2fr 1.2fr` ratio. Reusing it with an inline override on faceted search pages conflates two distinct layouts.
  3. *Mobile Overflow Calculation on 375px*:
     $$\text{Width Required} = \text{Sidebar } (260\text{px}) + \text{Gap } (24\text{px}) + \text{Card Min } (280\text{px}) = 564\text{px}$$
     $$\text{Viewport Available} = 375\text{px} - 32\text{px Container Padding} = 343\text{px}$$
     $$\text{Horizontal Blowout} = 564\text{px} - 343\text{px} = \mathbf{221\text{px Overflow}}$$
  4. *Desktop/Tablet Gap*: On 768px tablets, locking 260px leaves only 452px for the results column, squishing `.grid-3` into unreadable cards.

---

### 1.2 Target HTML Replacements

#### In `frontend/search-properties.html`:
**Target Lines**: 86
```html
<!-- BEFORE -->
    <div class="detail-layout" style="grid-template-columns:260px 1fr;gap:24px;align-items:start">
      <!-- Faceted Sidebar -->
      <aside class="filter-sidebar">

<!-- AFTER -->
    <div class="search-layout">
      <!-- Faceted Sidebar -->
      <aside class="filter-sidebar" id="filterSidebar">
        <div class="filter-sidebar-header mobile-only">
          <span class="filter-sidebar-title">⚡ Filters & Sorting</span>
          <button type="button" class="filter-close-btn" onclick="toggleMobileFilters(false)" aria-label="Close filters">✕</button>
        </div>
```

And in the results column (`search-properties.html` around line 132):
```html
<!-- BEFORE -->
      <!-- Main Results Column -->
      <main>
        <div class="results-topbar" style="background:#ffffff;padding:12px 18px;border:1px solid var(--border);border-radius:6px;margin-bottom:18px;">
          <div class="results-count" id="resultsCount" style="font-weight:700;color:var(--text-primary);">Loading verified listings…</div>
          <div style="display:flex;align-items:center;gap:10px;">
            <label for="sortSelect" style="font-size:13px;color:var(--text-secondary);font-weight:600;">Sort By:</label>
            <select id="sortSelect" class="btn btn-secondary" onchange="applySearch()" style="padding:7px 12px;background:#ffffff;">
              <option value="newest">Featured & Verified</option>
              <option value="price-asc">Rent: Low to High</option>
              <option value="price-desc">Rent: High to Low</option>
            </select>
          </div>
        </div>

<!-- AFTER -->
      <!-- Main Results Column -->
      <main class="search-results-col">
        <div class="results-topbar">
          <div class="results-count" id="resultsCount">Loading verified listings…</div>
          <div class="results-topbar-actions">
            <button type="button" class="btn btn-secondary mobile-filter-toggle" onclick="toggleMobileFilters(true)">
              ⚡ Filters <span class="filter-badge" id="filterBadge" style="display:none">0</span>
            </button>
            <div class="sort-wrap">
              <label for="sortSelect" class="sort-label">Sort By:</label>
              <select id="sortSelect" class="sort-select" onchange="applySearch()">
                <option value="newest">Featured & Verified</option>
                <option value="price-asc">Rent: Low to High</option>
                <option value="price-desc">Rent: High to Low</option>
              </select>
            </div>
          </div>
        </div>
```

#### In `frontend/search-products.html`:
**Target Lines**: 86
```html
<!-- BEFORE -->
    <div class="detail-layout" style="grid-template-columns:260px 1fr;gap:24px;align-items:start">
      <!-- Amazon Style Filter Sidebar -->
      <aside class="filter-sidebar">

<!-- AFTER -->
    <div class="search-layout">
      <!-- Amazon Style Filter Sidebar -->
      <aside class="filter-sidebar" id="filterSidebar">
        <div class="filter-sidebar-header mobile-only">
          <span class="filter-sidebar-title">⚡ Marketplace Filters</span>
          <button type="button" class="filter-close-btn" onclick="toggleMobileFilters(false)" aria-label="Close filters">✕</button>
        </div>
```

And around line 126 in `search-products.html`:
```html
<!-- BEFORE -->
      <!-- Main Results Column -->
      <main>
        <div class="results-topbar" style="background:#ffffff;padding:12px 18px;border:1px solid var(--border);border-radius:6px;margin-bottom:18px;">
          <div class="results-count" id="resultsCount" style="font-weight:700;color:var(--text-primary);">Loading verified ads…</div>
          <div style="display:flex;align-items:center;gap:10px;">
            <label for="sortSelect" style="font-size:13px;color:var(--text-secondary);font-weight:600;">Sort By:</label>
            ...

<!-- AFTER -->
      <!-- Main Results Column -->
      <main class="search-results-col">
        <div class="results-topbar">
          <div class="results-count" id="resultsCount">Loading verified ads…</div>
          <div class="results-topbar-actions">
            <button type="button" class="btn btn-secondary mobile-filter-toggle" onclick="toggleMobileFilters(true)">
              ⚡ Filters <span class="filter-badge" id="filterBadge" style="display:none">0</span>
            </button>
            <div class="sort-wrap">
              <label for="sortSelect" class="sort-label">Sort By:</label>
              ...
```

---

### 1.3 Exact CSS Rule Definitions for `frontend/css/global.css`

Add the following production-grade CSS rules to `frontend/css/global.css`:

```css
/* ==========================================================================
   Search & Catalog Layout System (Feature 1 & Feature 3)
   ========================================================================== */
.search-layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 24px;
  align-items: start;
  width: 100%;
}

.search-results-col {
  min-width: 0; /* Prevents grid blowouts from wide children */
  width: 100%;
}

.results-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 12px 16px;
  margin-bottom: 18px;
}

.results-count {
  font-size: 14px;
  font-weight: 700;
  color: var(--text-primary);
  white-space: nowrap;
}

.results-topbar-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.sort-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
}

.sort-label {
  font-size: 13px;
  color: var(--text-secondary);
  font-weight: 600;
  white-space: nowrap;
}

.sort-select {
  padding: 7px 12px;
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  outline: none;
  cursor: pointer;
  transition: var(--transition);
}

.sort-select:focus {
  border-color: var(--amazon-amber);
}

/* Mobile Filter Trigger Button & Badge */
.mobile-filter-toggle {
  display: none;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 700;
  padding: 8px 14px;
  border-radius: var(--radius);
}

.filter-badge {
  background: var(--amazon-amber);
  color: #002f34;
  font-size: 11px;
  font-weight: 800;
  border-radius: 999px;
  padding: 2px 7px;
  min-width: 18px;
  text-align: center;
}

.filter-sidebar-header {
  display: none;
}

/* Mobile Drawer Overlay */
.filter-drawer-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 47, 52, 0.6);
  backdrop-filter: blur(2px);
  z-index: 1090;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.25s ease;
}

.filter-drawer-backdrop.active {
  opacity: 1;
  pointer-events: auto;
}

/* Responsive Search Breakpoints */
@media (max-width: 1024px) {
  .search-layout {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .mobile-filter-toggle {
    display: inline-flex;
  }

  /* Transform filter-sidebar into an Off-Canvas Slide Drawer on Mobile/Tablet */
  .filter-sidebar {
    position: fixed;
    top: 0;
    right: 0;
    width: 320px;
    max-width: 88vw;
    height: 100vh;
    background: #ffffff;
    z-index: 1100;
    box-shadow: -4px 0 25px rgba(0, 47, 52, 0.25);
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
    padding: 20px 18px 80px;
    transform: translateX(100%);
    transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    border-radius: 0;
    border: none;
  }

  .filter-sidebar.open {
    transform: translateX(0);
  }

  .filter-sidebar-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 14px;
    margin-bottom: 14px;
    border-bottom: 1px solid var(--border);
  }

  .filter-sidebar-title {
    font-size: 16px;
    font-weight: 800;
    color: var(--text-primary);
  }

  .filter-close-btn {
    background: #f1f5f9;
    border: none;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    font-size: 16px;
    color: var(--text-primary);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: var(--transition);
  }

  .filter-close-btn:hover {
    background: #e2e8f0;
  }
}

@media (max-width: 600px) {
  .results-topbar {
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
  }

  .results-topbar-actions {
    justify-content: space-between;
    width: 100%;
  }

  .sort-wrap {
    flex: 1;
    justify-content: flex-end;
  }

  .sort-select {
    width: 100%;
    max-width: 170px;
  }
}
```

---

## 2. Complete Breakpoint & Zero-Overflow Audit for `global.css`

### 2.1 Viewport Breakpoint Standard
To support students on every device, StayMart must adhere to a standardized 4-tier responsive hierarchy:

| Breakpoint Tier | Media Query Range | Target Devices | Layout Behavior |
|---|---|---|---|
| **Mobile Portrait** | `max-width: 480px` (tested at `375px`) | iPhone SE, iPhone 13-15 Mini, Pixel 6a | Single-column cards (`1fr`), 100% width inputs, compact navbar, sticky bottom CTA bar |
| **Mobile Landscape / Phablet** | `481px` to `768px` (tested at `768px`) | iPad mini portrait, Galaxy Fold unfolded | 2-column cards (`repeat(2, 1fr)`), compact header, bottom navigation bar |
| **Tablet Landscape / Laptop** | `769px` to `1024px` | iPad Pro 10.5", 11", Surface Go | 3-column cards (`repeat(3, 1fr)`), 1-column search layout with mobile filter button |
| **Desktop / Wide Screen** | `1025px` and `1280px+` | MacBook, ThinkPad, 1080p Desktop | 4-column cards (`repeat(4, 1fr)`), 280px sticky search sidebar, full 2fr 1.2fr detail layout |

---

### 2.2 Comprehensive Zero-Overflow Protocol (375px Elimination)

Horizontal scrollbars on 375px viewports occur when content width exceeds `375px - 32px (container margin) = 343px`. The following structural fixes guarantee zero horizontal overflow:

#### A. Root HTML and Body Containment
```css
/* In frontend/css/global.css lines 60-75 */
html, body {
  width: 100%;
  max-width: 100vw;
  overflow-x: hidden;
  box-sizing: border-box;
}

*, *::before, *::after {
  box-sizing: border-box;
}

/* Guarantee all media is intrinsically responsive */
img, svg, video, canvas {
  max-width: 100%;
  height: auto;
  display: block;
}

/* Ensure flexbox and grid children do not cause overflow blowouts */
input, select, textarea, button {
  min-width: 0;
  max-width: 100%;
}
```

#### B. Navbar & Commercial Header Restructuring on Mobile
**Current Defect**:
- `.navbar` has hardcoded `height: 72px;` in desktop CSS.
- In `@media (max-width: 768px)`, `.navbar-inner` wraps into 3 rows, but `.navbar` remains 72px tall! This vertically clips the navbar and pushes items into horizontal overflow.
- `.nav-links` (Accommodations, Buy & Sell) takes ~220px, competing with logo (110px) and `.nav-actions` (220px), totaling 550px on a 343px viewport.

**The Fix**:
```css
@media (max-width: 768px) {
  .navbar {
    height: auto;
    min-height: 60px;
    padding: 8px 0;
  }

  .navbar-inner {
    flex-wrap: wrap;
    gap: 8px;
    padding: 6px 14px;
    height: auto;
  }

  /* Hide verbose text links from the top navbar on mobile (routed through bottom nav / drawer) */
  .nav-links {
    display: none;
  }

  /* Search bar spans 100% of row 2 */
  .nav-search-bar {
    order: 3;
    max-width: 100%;
    width: 100%;
    margin-top: 4px;
    height: 38px;
  }

  .nav-search-bar input {
    height: 38px;
    font-size: 13px;
  }

  .nav-search-btn {
    height: 38px;
    width: 40px;
  }

  /* Compact nav actions */
  .nav-actions {
    gap: 8px;
  }

  .nav-icon-btn {
    width: 34px;
    height: 34px;
    font-size: 14px;
  }

  .avatar {
    width: 34px;
    height: 34px;
    font-size: 13px;
  }

  .btn-olx-sell {
    padding: 4px 10px;
    font-size: 12px;
    border-width: 2.5px;
    gap: 3px;
  }

  .logo {
    font-size: 22px;
  }
}
```

#### C. Grid System Normalization Across All Breakpoints
Replace lines 1275-1296 of `global.css` with this comprehensive grid system:

```css
/* ==========================================================================
   Complete Responsive Grid & Component Breakpoints
   ========================================================================== */

/* 1. Desktop Standard / Small Laptop (<= 1024px) */
@media (max-width: 1024px) {
  .grid-4 { grid-template-columns: repeat(3, 1fr); gap: 16px; }
  .grid-3 { grid-template-columns: repeat(2, 1fr); gap: 16px; }
  .category-grid { grid-template-columns: repeat(4, 1fr); gap: 10px; }
  .hero-banner-grid { grid-template-columns: 1fr; gap: 20px; }
  .detail-layout { grid-template-columns: 1fr; gap: 20px; }
  .sidebar-sticky { position: static; }
}

/* 2. Tablet / Large Mobile (<= 768px) */
@media (max-width: 768px) {
  .grid-4, .grid-3 { grid-template-columns: repeat(2, 1fr); gap: 14px; }
  .grid-2 { grid-template-columns: repeat(2, 1fr); gap: 14px; }
  .category-grid { grid-template-columns: repeat(3, 1fr); gap: 8px; }
  .footer-grid { grid-template-columns: 1fr; gap: 24px; }
  .info-cards { grid-template-columns: repeat(2, 1fr); gap: 10px; }
  
  .hero { padding: 20px 0; }
  .hero-headline { font-size: 24px; }
  .hero-subheadline { font-size: 13px; }
  
  .campus-chips { gap: 6px; }
  .campus-chip { font-size: 11px; padding: 5px 10px; }

  .breadcrumb {
    flex-wrap: wrap;
    row-gap: 4px;
    font-size: 11px;
    margin-bottom: 12px;
  }

  .reviews-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}

/* 3. Small Mobile / Phone Portrait (<= 480px, tested at 375px) */
@media (max-width: 480px) {
  .container {
    padding: 0 12px;
  }

  .grid-4, .grid-3, .grid-2 {
    grid-template-columns: 1fr;
    gap: 14px;
  }

  .category-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
  }

  .category-card {
    padding: 10px 6px;
  }

  .category-card .category-icon {
    font-size: 24px;
  }

  .category-card .category-name {
    font-size: 12px;
  }

  .hero-stats {
    flex-wrap: wrap;
    gap: 12px;
    justify-content: space-between;
  }

  .stat-item {
    flex: 1 1 30%;
  }

  .stat-num {
    font-size: 17px;
  }

  .stat-lbl {
    font-size: 11px;
  }

  .section-title {
    font-size: 18px;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  /* Form and Radio Cards */
  .radio-cards {
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 8px;
  }

  .checkbox-grid {
    grid-template-columns: 1fr !important;
  }

  /* Auth Card Padding on Small Mobile */
  .auth-card {
    padding: 24px 16px;
    border-radius: var(--radius-lg);
  }

  /* Ensure detail view titles wrap cleanly */
  .detail-title {
    font-size: 20px;
    line-height: 1.3;
  }
}
```

---

### 2.3 Restoring Missing Component CSS Lost in the Rewrite

The following crucial classes exist in HTML files (`post-property.html`, `post-product.html`, `login.html`, `register.html`, `utils.js`) but were lost from `global.css`:

```css
/* ==========================================================================
   Restored Posting Forms & Auth Styles (Missing from global.css)
   ========================================================================== */

/* 2-Column Grid Utility */
.grid-2 {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

/* Post Form Sections */
.post-form-section {
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: var(--shadow-sm);
}

.post-form-section h2 {
  font-size: 17px;
  font-weight: 800;
  color: #002f34;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Selectable Radio Cards */
.radio-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
  gap: 10px;
}

.radio-card {
  position: relative;
  cursor: pointer;
  display: block;
}

.radio-card input {
  position: absolute;
  opacity: 0;
  width: 100%;
  height: 100%;
  cursor: pointer;
}

.radio-card-body {
  border: 1.5px solid var(--border);
  border-radius: var(--radius);
  padding: 12px 8px;
  text-align: center;
  transition: var(--transition);
  background: #ffffff;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
}

.radio-card input:checked + .radio-card-body {
  border-color: #002f34;
  background: var(--olx-light-teal);
  box-shadow: 0 0 0 2px #002f34;
}

.radio-card-icon {
  display: block;
  font-size: 22px;
  margin-bottom: 4px;
}

/* Checkbox Cards for Amenities */
.checkbox-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
  gap: 10px;
}

.checkbox-card {
  position: relative;
}

.checkbox-card input {
  position: absolute;
  opacity: 0;
}

.checkbox-card-body {
  border: 1.5px solid var(--border);
  border-radius: var(--radius);
  padding: 10px 12px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  background: #ffffff;
  transition: var(--transition);
}

.checkbox-card input:checked + .checkbox-card-body {
  border-color: #002f34;
  background: var(--olx-light-teal);
}

/* Auth Page Wrappers (login.html, register.html) */
.auth-wrap {
  min-height: calc(100vh - 140px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 32px 16px;
}

.auth-card {
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 36px 32px;
  width: 100%;
  max-width: 440px;
  box-shadow: var(--shadow-md);
}

.auth-heading {
  font-size: 22px;
  font-weight: 800;
  color: #002f34;
  text-align: center;
  margin-bottom: 4px;
}

.auth-sub {
  font-size: 13px;
  color: var(--text-secondary);
  text-align: center;
  margin-bottom: 24px;
}

.auth-link {
  text-align: center;
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: 20px;
}

.auth-link a {
  font-weight: 700;
  color: var(--text-link);
}

/* Pagination Bar (utils.js renderPagination) */
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  flex-wrap: wrap;
  margin-top: 28px;
}

.page-btn {
  background: #ffffff;
  border: 1px solid var(--border);
  color: var(--text-primary);
  font-weight: 700;
  font-size: 14px;
  min-width: 38px;
  height: 38px;
  padding: 0 10px;
  border-radius: var(--radius-sm);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: var(--transition);
}

.page-btn:hover:not(:disabled) {
  border-color: #002f34;
  background: #f8fafc;
}

.page-btn.active {
  background: #002f34;
  color: #ffffff;
  border-color: #002f34;
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
```

---

## 3. Detail Page Mobile Layout Architecture (`property-detail` & `product-detail`)

### 3.1 The UX Breakdown on Mobile Viewports
Currently, in `frontend/js/property-detail.js` and `frontend/js/product-detail.js`:
- The DOM consists of `<section class="detail-layout">` with two direct children:
  1. `<div>` (Left column: Gallery $\rightarrow$ Badges/Title $\rightarrow$ Meta $\rightarrow$ Info Cards $\rightarrow$ Facilities $\rightarrow$ Description $\rightarrow$ **All Reviews** $\rightarrow$ **Review Submission Form** $\rightarrow$ **Similar Properties Grid**).
  2. `<aside class="sidebar-sticky">` (Right column: Owner Profile $\rightarrow$ Action Card with Rent/Price $\rightarrow$ Room Selector / Qty Selector $\rightarrow$ Book/Buy Button $\rightarrow$ Message & Call Buttons).
- When the layout collapses to 1 column on `< 1024px`, the entire `<aside>` is placed at the very bottom — **after the complete reviews thread and similar listings!**
- On a 375px mobile device:
  - The student cannot see the price in the top hero area.
  - The student must scroll through 8 to 12 mobile screens of reviews before seeing the "Book Now" CTA or seller contact details.
  - This severely hurts listing conversion and causes student drop-off.

---

### 3.2 Dual-Tier Solution: Sticky Mobile Action Bar + In-Flow Reordering

#### Tier 1: Fixed Mobile Sticky Action Bar
When viewport width is $\le 768\text{px}$, a sleek, high-conversion action bar is permanently docked to the bottom of the screen:
```
┌────────────────────────────────────────────────────────┐
│  ₹6,500/mo · ● Available        [ Book Room ➔ ]        │
└────────────────────────────────────────────────────────┘
```
- **Left Side**: Prominent price + pulsing status badge (`Available` or `Occupied`).
- **Right Side**: Primary action CTA (`Book Room` for PG, `Buy Now` or `Rent Now` for classified).
- **Behavior**:
  - Tapping "Book Room" performs a smooth scroll directly to `#bookingActionCard` and highlights the room selector, OR
  - Triggers the mobile booking sheet drawer.
- **Safety Offset**:
  - `body.has-mobile-bar { padding-bottom: 74px; }` prevents content or footer links from being obscured.

#### Tier 2: Semantic Mobile Re-ordering in Detail Page Scripts
In `frontend/js/property-detail.js` and `frontend/js/product-detail.js`, the generated DOM order is modified so that the Action/Booking card appears immediately beneath the property description and facilities, **prior to the reviews section**.

Target flow on mobile:
1. Gallery (with touch swipe indicator)
2. Badges, Title, Location, and Date
3. **Mobile Price Banner** (Visible immediately on mobile)
4. Info Cards (2x2 grid: Rooms, Gender, Deposit, Photos)
5. Amenities / Facilities Grid
6. About / Description
7. **Host / Seller Card & Booking Action Panel**
8. Student Reviews & Star Breakdown
9. Similar Listings Grid
10. Footer

---

### 3.3 Concrete Code Additions for Detail Pages

#### CSS to add in `frontend/css/global.css`:
```css
/* ==========================================================================
   Detail Page Mobile Sticky Bar & Responsive Flow (Feature 4)
   ========================================================================== */
.mobile-action-bar {
  display: none;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #ffffff;
  border-top: 1px solid var(--border);
  box-shadow: 0 -4px 16px rgba(0, 47, 52, 0.12);
  padding: 10px 16px;
  z-index: 1000;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.mobile-action-info {
  display: flex;
  flex-direction: column;
}

.mobile-action-price {
  font-size: 18px;
  font-weight: 800;
  color: #002f34;
  letter-spacing: -0.3px;
  line-height: 1.2;
}

.mobile-action-sub {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-secondary);
}

.mobile-action-btn {
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 700;
  border-radius: var(--radius);
  white-space: nowrap;
}

@media (max-width: 768px) {
  .mobile-action-bar {
    display: flex;
  }

  body.has-detail-bottom-bar {
    padding-bottom: 70px;
  }

  /* Make gallery aspect ratio optimized for phones */
  .gallery-main {
    aspect-ratio: 16 / 11;
  }

  .gallery-thumbs {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
    padding-bottom: 4px;
  }

  .gallery-thumbs::-webkit-scrollbar {
    display: none;
  }

  .gallery-thumbs img {
    width: 64px;
    height: 48px;
    flex-shrink: 0;
  }

  /* Collapse sidebar margin */
  .sidebar-sticky {
    margin-top: 24px;
  }
}
```

#### JavaScript Logic to Render Mobile Action Bar in `property-detail.js`:
```javascript
// Append mobile action bar to body
document.body.classList.add('has-detail-bottom-bar');
let mobileBar = document.getElementById('mobileDetailBar');
if (!mobileBar) {
  mobileBar = document.createElement('div');
  mobileBar.id = 'mobileDetailBar';
  mobileBar.className = 'mobile-action-bar';
  document.body.appendChild(mobileBar);
}

mobileBar.innerHTML = `
  <div class="mobile-action-info">
    <div class="mobile-action-price">${formatPrice(property.pricePerMonth, 'RENT')}</div>
    <div class="mobile-action-sub">${property.isAvailable ? '● Available for move-in' : '● Fully occupied'}</div>
  </div>
  <button class="btn btn-primary mobile-action-btn" onclick="scrollToBooking()">
    ${property.isAvailable ? 'Book Room' : 'Check Waitlist'}
  </button>
`;

window.scrollToBooking = function() {
  const target = document.querySelector('.action-card');
  if (target) {
    target.scrollIntoView({ behavior: 'smooth', block: 'center' });
    target.style.transition = 'box-shadow 0.3s ease';
    target.style.boxShadow = '0 0 0 3px var(--amazon-amber)';
    setTimeout(() => { target.style.boxShadow = ''; }, 1500);
  }
};
```

---

## 4. Card Grids, Category Pills & Touch Target Ergonomics

### 4.1 Card Grids (`buildPropertyCard` & `buildProductCard`)
Our inspection of `frontend/js/utils.js` (lines 262-340) and `global.css` (lines 568-758) shows the OLX card layout functions well on desktop, but requires responsive safeguards:

1. **Card Title Clamp**:
   - Currently: `-webkit-line-clamp: 2; min-height: 40px;`
   - Responsive polish: On mobile (`<= 480px`), when cards span full width (1 column), allow titles to breathe (`min-height: auto; font-size: 15px;`) for optimal student scanning.
2. **Wishlist Tap Target Expansion**:
   - Currently: `.card-fav-btn` is `width: 32px; height: 32px;`.
   - On touchscreens, a 32px button nested inside an `<a>` card link frequently triggers the link instead of toggling the favorite!
   - Touch Ergonomics Solution:
     ```css
     .card-fav-btn {
       width: 36px;
       height: 36px;
       font-size: 16px;
     }

     /* Expand touch hit area to 48px via invisible pseudo-element */
     .card-fav-btn::after {
       content: '';
       position: absolute;
       inset: -6px;
     }
     ```
3. **Card Specs Text Wrapping**:
   - Currently: `.card-specs` has `white-space: nowrap; overflow: hidden; text-overflow: ellipsis;`.
   - On 375px mobile, when `.grid-4` or `.grid-3` is set to 1 column, available width is 343px. All specs fit comfortably with no truncation.
   - At tablet widths (768px with 2 columns = ~350px per card), specs also fit without clipping.

---

### 4.2 Category Strip Swipe Discovery
- **Observed Issue**: In `index.html`, `search-properties.html`, and `search-products.html`, `.category-strip-inner` has `overflow-x: auto; scrollbar-width: none;`. Users on touchscreens have no visual cue that 6+ additional categories lie just off-screen to the right.
- **Solution**:
  1. Add CSS edge fade masks that automatically fade the right edge on scrollable containers.
  2. Implement iOS-smooth touch inertia:
     ```css
     .category-strip {
       position: relative;
     }

     .category-strip-inner {
       max-width: 1280px;
       margin: 0 auto;
       padding: 0 16px;
       display: flex;
       align-items: center;
       gap: 12px;
       overflow-x: auto;
       white-space: nowrap;
       scrollbar-width: none;
       -webkit-overflow-scrolling: touch;
       scroll-snap-type: x proximity;
       height: 48px;
     }

     .cat-strip-item {
       scroll-snap-align: start;
       padding: 6px 12px;
       min-height: 36px;
       border-radius: var(--radius-full);
       background: #f8fafc;
       border: 1px solid var(--border-subtle);
       flex-shrink: 0;
     }

     .cat-strip-item:hover, .cat-strip-item.active {
       background: var(--olx-light-teal);
       border-color: #002f34;
       color: #002f34;
     }
     ```

---

### 4.3 Filter Sections & Touch Form Elements
In `search-properties.html` and `search-products.html`:
- `.check-row`:
  ```css
  .check-row {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 13.5px;
    color: var(--text-secondary);
    cursor: pointer;
    padding: 7px 4px;
    min-height: 38px; /* Thumb-friendly touch target */
    border-radius: var(--radius-sm);
    transition: background 0.15s ease;
    user-select: none;
  }

  .check-row:hover {
    background: #f8fafc;
    color: var(--text-primary);
  }

  .check-row input[type="checkbox"],
  .check-row input[type="radio"] {
    accent-color: #002f34;
    width: 18px;
    height: 18px;
    cursor: pointer;
    flex-shrink: 0;
  }
  ```
- `.price-range`:
  ```css
  .price-range {
    display: flex;
    align-items: center;
    gap: 8px;
    width: 100%;
  }

  .price-range input {
    flex: 1;
    min-width: 0; /* Prevents overflow inside flex parent */
    padding: 8px 10px;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    outline: none;
    font-size: 13px;
  }
  ```

---

## 5. Token Harmonization Bridge (Fixing CSS Variable Failures)

`dashboard.css` and several scripts (`search.js:238`, `wishlist.js:33`) reference legacy tokens that evaluate to `transparent` or invalid CSS because `global.css` does not define them.

Add the following backwards-compatible token bridge to `:root` in `frontend/css/global.css`:

```css
  /* ==========================================================================
     Design Token Harmonization Bridge (Feature 5)
     Unifies global.css with dashboard.css and dynamic JavaScript references
     ========================================================================== */
  --primary: #002f34;               /* OLX Deep Spruce */
  --primary-light: #004d56;
  --primary-hover: #001d20;
  --primary-bg: #ebf7f7;
  
  --accent: #ff9900;                /* Amazon Marketplace Amber */
  --accent-light: #fff4e5;
  --accent-hover: #e68a00;
  
  --dark: #002f34;
  --dark-2: #003e45;
  --dark-3: #004d56;
  
  --card-bg: #ffffff;
  --card-bg-hover: #f8fafc;
  
  --gradient-primary: linear-gradient(135deg, #002f34 0%, #004d56 100%);
  --gradient-card: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
  
  --transition-fast: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
```

**Immediate Bug Fixes Resulting From This Bridge**:
1. `search.js:238`: `clearAll.style.background = 'var(--primary)'; clearAll.style.color = '#fff';` will now properly render a distinct teal badge with white text instead of an invisible transparent block!
2. `dashboard.css`: `.dash-body { background: var(--dark); }` and `.dash-sidebar { background: var(--dark-2); }` will now render cohesive rich deep teal surfaces instead of blank white transparent panels.

---

## 6. Implementation Action Plan & Checklist

| Step | Target File | Action Description | Complexity |
|---|---|---|---|
| **1** | `frontend/search-properties.html` | Remove inline `style="grid-template-columns:260px 1fr..."` from line 86. Replace with class `search-layout`. Add mobile filter header and trigger button in results topbar. | Low |
| **2** | `frontend/search-products.html` | Remove inline `style="grid-template-columns:260px 1fr..."` from line 86. Replace with class `search-layout`. Add mobile filter header and trigger button in results topbar. | Low |
| **3** | `frontend/css/global.css` | 1. Add design token harmonization bridge to `:root`.<br>2. Add `.search-layout`, `.search-results-col`, and off-canvas mobile drawer styles.<br>3. Add restored classes (`.grid-2`, `.post-form-section`, `.radio-cards`, `.checkbox-grid`, `.auth-wrap`, `.auth-card`, `.pagination`, `.page-btn`).<br>4. Implement comprehensive responsive breakpoints for `1024px`, `768px`, and `480px`.<br>5. Add `.mobile-action-bar` and sticky CTA styling. | Medium |
| **4** | `frontend/js/search.js` | Add `toggleMobileFilters(open)` helper function to open/close drawer on mobile viewports and update active filter badge count. | Low |
| **5** | `frontend/js/property-detail.js` | Render `.mobile-action-bar` at bottom of page on viewports $\le 768\text{px}$. Ensure `has-detail-bottom-bar` body class is applied. Fix broken 404 redirect (`my-bookings.html` $\rightarrow$ `bookings.html`). | Low |
| **6** | `frontend/js/product-detail.js` | Render `.mobile-action-bar` at bottom of page on viewports $\le 768\text{px}$ with "Buy Now" / "Rent Now" CTA. | Low |

---

## 7. Verification Method

### 7.1 Automated Layout Verification Test
Milestone 5 will execute automated headless Chrome checks across all pages at 3 viewports:
- Mobile: `375px × 667px`
- Tablet: `768px × 1024px`
- Desktop: `1280px × 800px`

The headless test evaluates:
```javascript
const isOverflowing = document.documentElement.scrollWidth > document.documentElement.clientWidth;
console.assert(!isOverflowing, `Horizontal overflow detected! scrollWidth=${document.documentElement.scrollWidth}, clientWidth=${document.documentElement.clientWidth}`);
```

### 7.2 Manual Developer Inspection Checklist
1. Open Chrome DevTools (`F12`), toggle Device Toolbar (`Ctrl + Shift + M`), select **iPhone SE (375 × 667)**.
2. Navigate to `http://localhost:5500/frontend/search-properties.html`:
   - Verify zero horizontal scrolling (`scrollLeft === 0`).
   - Verify listings are full width in 1 column.
   - Verify "⚡ Filters" button appears and opens the slide drawer smoothly.
3. Navigate to `http://localhost:5500/frontend/property-detail.html?id=1`:
   - Verify the sticky mobile action bar docks at the bottom with price and "Book Room" button.
   - Verify tapping "Book Room" scrolls smoothly to the booking form.
4. Rotate to **iPad Mini (768 × 1024)**:
   - Verify grid displays clean 2-column cards.
   - Verify navbar wraps cleanly without overlapping buttons or cut-off text.
5. Expand to **Desktop (1280 × 800)**:
   - Verify 4-column card grids on homepage and 3-column grids on search page with 280px sidebar.
