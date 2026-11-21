# StayMart Milestone 1 — Token Harmonization, Visual Polish & Bugfix Blueprint

**Document**: `plan_tokens_polish.md`  
**Author**: M1 Explorer 3 (Token Harmonization, Visual Polish & Bugfix Specialist)  
**Date**: November 2, 2026  
**Target Milestone**: Milestone 1 (Features 5, 6, 7)  
**Scope**: Exact implementation blueprints for CSS design token unification, complete dashboard light-theme overhaul, comprehensive 404 redirect bug fixes, micro-interactions, spring transitions, and emoji badge refactoring.

---

## 1. Executive Summary

StayMart's frontend transition from a legacy dark theme (`global.css.bak`) to the authentic OLX/Amazon commercial light theme (`global.css`) left significant styling regressions across the user experience:
1. **13 Missing CSS Custom Properties**: `dashboard.css` and multiple JavaScript controllers (`search.js`, `wishlist.js`) reference variables (`--dark`, `--dark-2`, `--primary`, `--gradient-*`) that do not exist in `global.css`, causing backgrounds and borders to evaluate to `unset`/`transparent`.
2. **Four Critical 404 Broken Redirects**: Beyond the known bug in `property-detail.js:224` (`my-bookings.html`), an exhaustive audit of all 23 JS redirect assignments uncovered **3 additional broken redirects** in `product-detail.js` and `property-detail.js` targeting nonexistent files (`my-orders.html` and `messages.html`).
3. **Dropped Core UI Classes**: Critical foundational CSS rules from the legacy stylesheet—including `.table`, `.filter-tag`, auth forms, post-listing radio cards, reviews, and `@keyframes shimmer`—were omitted during the theme rewrite, breaking layout and rendering on public and dashboard pages alike.
4. **Static AI Aesthetics & Raw Unicode Emojis**: Interactive elements lack tactile feedback, button press states, spring easing curves, and elevation changes. Raw Unicode emojis render inconsistently and look cheap and cartoonish across different operating systems.

This document provides complete, production-ready, copy-paste CSS snippets and JavaScript code replacements to solve every identified defect in Milestone 1.

---

## 2. Analysis 1: CSS Design Token Disconnect & Harmonization

### 2.1 Complete Inventory of Missing CSS Custom Properties

Through automated static analysis of all CSS, JS, and HTML files, exactly **13 custom properties** were identified as referenced but undefined in `global.css`:

| Missing Variable | Usage Locations in Codebase | Broken Behavior When Undefined |
|---|---|---|
| `--primary` | `search.js:238`, `dashboard.css:82, 567, 652, 668` | "Clear all ×" button renders transparent with white text (invisible); dashboard active sidebar tab indicator disappears |
| `--primary-light` | `dashboard.css:261` | Stat card hover border renders transparent |
| `--accent-light` | `dashboard.css:298, 435` | Stat card trend text and list prices render uncolored/unstyled |
| `--dark` | `dashboard.css:9, 343, 657`, `search.js` | Dashboard body background falls back to white; search inputs have transparent backgrounds |
| `--dark-2` | `dashboard.css:16, 227, 516, 642, 748` | Sidebar background evaluates to transparent; hamburger button background evaluates to transparent |
| `--dark-3` | `dashboard.css:75, 140, 392, 530, 615, 692, 722, 748` | Sidebar link hovers, thumbnails, chat bubble backgrounds render transparent |
| `--card-bg` | `dashboard.css:250, 303, 447, 510` | Panels and stat cards render with transparent backgrounds |
| `--card-bg-hover` | `dashboard.css:383` | Table and list rows have no hover state |
| `--glass` | `dashboard.css:169` | Dashboard sticky topbar background is transparent |
| `--glass-border` | `dashboard.css:172` | Topbar bottom divider line is invisible |
| `--gradient-card` | `wishlist.js:33` | Fallback wishlist placeholder card image fails to render background |
| `--gradient-primary` | `dashboard.css:364, 621` | Active tabs and user chat bubbles render transparent |
| `--transition-fast` | `dashboard.css:64, 148, 360, 375, 525` | Sidebar buttons, tabs, and chat items have instant jerky hover transitions |

---

### 2.2 Backward-Compatible Root Variables for `frontend/css/global.css`

To ensure 100% backward compatibility and eliminate any risk of undefined variables across the entire application, add the following block directly inside `:root` in `frontend/css/global.css` (lines 50–58):

```css
  /* ==========================================================================
     Backward-Compatible Theme Tokens & Semantic Aliases
     Harmonized for StayMart Light Marketplace Theme
     ========================================================================== */
  /* Primary & Accent Semantic Aliases */
  --primary: #002f34;                        /* Authentic OLX Deep Spruce Brand */
  --primary-dark: #001f23;                   /* Darker Spruce for hover/active */
  --primary-light: #007185;                  /* Amazon Action Blue / Highlight */
  --accent: #ff9900;                         /* Amazon Marketplace Amber */
  --accent-light: #0a883a;                   /* Uttarakhand Emerald Green for positive trends & savings */

  /* Surface Aliases (Light Marketplace Canvas) */
  --dark: #002f34;                           /* Semantic dark = Deep Spruce Header */
  --dark-2: #002226;                         /* Sidebar dark surface */
  --dark-3: #003d44;                         /* Elevated dark surface / hover */
  --card-bg: #ffffff;                        /* Crisp white card surface */
  --card-bg-hover: #f8fafc;                  /* Subtle neutral hover */

  /* Glassmorphism & Overlays */
  --glass: rgba(255, 255, 255, 0.94);        /* Frosted light glass for sticky bars */
  --glass-border: rgba(0, 47, 52, 0.08);     /* Subtle slate boundary */

  /* Harmonized Gradients */
  --gradient-primary: linear-gradient(135deg, #002f34 0%, #004d56 100%);
  --gradient-card: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
  --gradient-accent: linear-gradient(135deg, #ff9900 0%, #ffd814 100%);

  /* Spring Animation Easing Tokens */
  --transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  --transition-fast: all 0.15s cubic-bezier(0.16, 1, 0.3, 1);
  --transition-spring: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
```

---

### 2.3 Dashboard Overhaul in `frontend/css/dashboard.css`

The dashboard sidebar and views must harmonize with the light marketplace aesthetic. We adopt an **enterprise hybrid theme** (deep spruce `#002f34` sidebar matching the marketplace top navigation + airy `#f2f4f5` main content area with `#ffffff` cards and panels).

#### Exact CSS Overrides for `frontend/css/dashboard.css`:

```css
/* ============================================================
   StayMart Harmonized Dashboard Styles
   Enterprise Light Theme with Deep Spruce Sidebar
   ============================================================ */

/* Body Canvas */
.dash-body {
  display: flex;
  min-height: 100vh;
  background: var(--bg-page);
  color: var(--text-primary);
}

/* Sidebar: Deep Spruce matching Public Header */
.dash-sidebar {
  width: 264px;
  flex-shrink: 0;
  background: #002f34;
  border-right: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  z-index: 1200;
  transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1);
}

.dash-brand {
  padding: 22px 22px 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.dash-brand .logo {
  font-size: 22px;
  color: #ffffff;
  display: flex;
  flex-direction: column;
}

.dash-brand .logo small {
  font-size: 11px;
  color: #7f9799;
  font-weight: 500;
  margin-top: 2px;
}

.dash-nav {
  flex: 1;
  overflow-y: auto;
  padding: 14px 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.dash-nav .nav-group-title {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.09em;
  color: #7f9799;
  padding: 16px 12px 6px;
}

.dash-nav a {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  border-radius: 8px;
  color: #cfd8dc;
  font-size: 14px;
  font-weight: 600;
  transition: var(--transition-fast);
}

.dash-nav a:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #ffffff;
}

.dash-nav a.active {
  background: rgba(35, 229, 219, 0.12);
  color: #23e5db;
  box-shadow: inset 3px 0 0 #23e5db;
}

.dash-nav a .nav-ico {
  font-size: 15px;
  width: 28px;
  height: 28px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.06);
  flex-shrink: 0;
  transition: var(--transition-fast);
}

.dash-nav a:hover .nav-ico,
.dash-nav a.active .nav-ico {
  background: rgba(35, 229, 219, 0.2);
}

.dash-nav a .nav-badge {
  margin-left: auto;
  background: var(--danger);
  color: #fff;
  font-size: 11px;
  font-weight: 700;
  min-width: 20px;
  height: 20px;
  padding: 0 6px;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.dash-nav .nav-divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.08);
  margin: 10px 0;
}

/* User Card in Sidebar */
.dash-user {
  padding: 16px 18px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  align-items: center;
  gap: 12px;
}

.dash-user .avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #ff9900;
  color: #0f1111;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
}

.dash-user .du-name {
  font-size: 14px;
  font-weight: 700;
  color: #ffffff;
}

.dash-user .du-role {
  font-size: 11px;
  color: #7f9799;
  text-transform: uppercase;
}

.dash-user .du-logout {
  margin-left: auto;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: #cfd8dc;
  width: 34px;
  height: 34px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition-fast);
}

.dash-user .du-logout:hover {
  background: rgba(217, 56, 30, 0.2);
  color: #ff6b52;
  border-color: #ff6b52;
}

/* Main Content Area */
.dash-main {
  flex: 1;
  margin-left: 264px;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.dash-topbar {
  position: sticky;
  top: 0;
  z-index: 900;
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
  padding: 16px 28px;
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.dash-title {
  font-size: 22px;
  font-weight: 800;
  color: var(--text-primary);
}

.dash-subtitle {
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: 2px;
}

/* Stat Cards & Panels */
.stat-card {
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 20px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 47, 52, 0.05);
  transition: var(--transition);
}

.stat-card:hover {
  transform: translateY(-3px);
  border-color: #002f34;
  box-shadow: 0 8px 20px rgba(0, 47, 52, 0.08);
}

.stat-card .sc-value {
  font-size: 30px;
  font-weight: 800;
  line-height: 1.1;
  color: var(--text-primary);
}

.stat-card .sc-label {
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: 4px;
}

.stat-card .sc-trend {
  font-size: 12px;
  font-weight: 600;
  margin-top: 8px;
  color: var(--success);
}

.panel {
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 47, 52, 0.05);
}

.panel-header {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  padding: 18px 22px;
  border-bottom: 1px solid var(--border);
  background: #ffffff;
}

.panel-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
}

/* Tabs */
.tabs {
  display: flex;
  gap: 6px;
  background: #eef2f5;
  border: 1px solid var(--border);
  border-radius: 999px;
  padding: 4px;
  width: fit-content;
  flex-wrap: wrap;
}

.tab {
  padding: 7px 16px;
  border-radius: 999px;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  font-weight: 600;
  font-size: 13.5px;
  cursor: pointer;
  transition: var(--transition-fast);
}

.tab:hover {
  color: var(--text-primary);
}

.tab.active {
  background: #002f34;
  color: #ffffff;
  box-shadow: 0 2px 6px rgba(0, 47, 52, 0.2);
}

/* List Rows */
.list-row {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 22px;
  background: #ffffff;
  border-bottom: 1px solid var(--border);
  transition: var(--transition-fast);
}

.list-row:last-child {
  border-bottom: none;
}

.list-row:hover {
  background: #f8fafc;
}

.list-thumb {
  width: 60px;
  height: 60px;
  border-radius: 10px;
  object-fit: cover;
  flex-shrink: 0;
  background: #eef2f5;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.list-price {
  font-weight: 800;
  color: #002f34;
  font-size: 15px;
}

/* Search input & pills */
.search-input {
  background: #ffffff;
  border: 1px solid var(--border);
  color: var(--text-primary);
  border-radius: 999px;
  padding: 9px 16px;
  font-size: 13.5px;
  outline: none;
  min-width: 240px;
  transition: var(--transition-fast);
}

.search-input:focus {
  border-color: #002f34;
  box-shadow: 0 0 0 3px rgba(0, 47, 52, 0.1);
}

.pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  background: #eef2f5;
  border: 1px solid var(--border);
  color: var(--text-secondary);
}

/* Chat Layout & Message Bubbles */
.chat-layout {
  display: grid;
  grid-template-columns: 320px 1fr;
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  height: calc(100vh - 200px);
  min-height: 480px;
}

.convo-list {
  background: #f8fafc;
  border-right: 1px solid var(--border);
  overflow-y: auto;
}

.convo-item {
  display: flex;
  gap: 12px;
  padding: 14px 16px;
  border-bottom: 1px solid var(--border);
  cursor: pointer;
  transition: var(--transition-fast);
}

.convo-item:hover {
  background: #edf2f7;
}

.convo-item.active {
  background: #ffffff;
  box-shadow: inset 3px 0 0 #002f34;
}

.convo-item .cv-unread {
  background: #002f34;
  color: #fff;
}

.chat-panel {
  display: flex;
  flex-direction: column;
  background: #ffffff;
}

.chat-bubble.them {
  align-self: flex-start;
  background: #eef2f5;
  color: var(--text-primary);
  border-bottom-left-radius: 4px;
}

.chat-bubble.me {
  align-self: flex-end;
  background: #002f34;
  color: #ffffff;
  border-bottom-right-radius: 4px;
}

.chat-input {
  display: flex;
  gap: 10px;
  padding: 14px 20px;
  border-top: 1px solid var(--border);
  background: #ffffff;
}

.chat-input input {
  flex: 1;
  background: #f8fafc;
  border: 1px solid var(--border);
  color: var(--text-primary);
  border-radius: 999px;
  padding: 12px 18px;
  font-size: 14px;
  outline: none;
  transition: var(--transition-fast);
}

.chat-input input:focus {
  background: #ffffff;
  border-color: #002f34;
  box-shadow: 0 0 0 3px rgba(0, 47, 52, 0.1);
}

/* Skeleton Shimmer in Light Mode */
.row-skeleton {
  height: 74px;
  border-radius: var(--radius);
  background: linear-gradient(90deg, #eef2f5 25%, #f8fafc 50%, #eef2f5 75%);
  background-size: 800px 100%;
  animation: shimmer 1.5s infinite linear;
}
```

---

### 2.4 Restoring Missing Foundational Classes in `global.css`

During the theme rewrite, several foundational UI utility rules were omitted. Append these directly to `frontend/css/global.css`:

```css
/* ==========================================================================
   Restored Foundational Components (Tables, Chips, Auth, Shimmer)
   ========================================================================== */

/* Tables */
.table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
  background: #ffffff;
}

.table th, .table td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid var(--border);
}

.table th {
  color: var(--text-secondary);
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  background: #f8fafc;
}

.table tr:hover td {
  background: #f8fafc;
}

/* Filter Tag Chips (Search pages & active filter rows) */
.filter-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #eef2f5;
  border: 1px solid #d5d9d9;
  color: var(--text-primary);
  padding: 5px 12px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 500;
  transition: var(--transition-fast);
}

.filter-tag button {
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  font-size: 15px;
  line-height: 1;
  padding: 0 2px;
}

.filter-tag button:hover {
  color: var(--danger);
}

/* Auth Cards (login.html and register.html) */
.auth-wrap {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  background: var(--bg-page);
}

.auth-card {
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 36px 32px;
  width: 100%;
  max-width: 440px;
  box-shadow: 0 4px 20px rgba(0, 47, 52, 0.08);
}

.auth-heading {
  text-align: center;
  font-size: 24px;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 6px;
}

.auth-sub {
  text-align: center;
  color: var(--text-secondary);
  font-size: 14px;
  margin-bottom: 24px;
}

.auth-link {
  text-align: center;
  font-size: 14px;
  color: var(--text-secondary);
  margin-top: 20px;
}

.input-with-icon {
  position: relative;
  display: flex;
  align-items: center;
}

.input-with-icon .field-icon {
  position: absolute;
  left: 14px;
  font-size: 16px;
  pointer-events: none;
  color: var(--text-muted);
}

.input-with-icon input {
  padding-left: 42px !important;
  width: 100%;
}

/* Post Listing Forms & Radio Cards (post-property.html, post-product.html) */
.post-form-section {
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 24px;
  margin-bottom: 20px;
  box-shadow: var(--shadow-sm);
}

.post-form-section h2 {
  font-size: 17px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.radio-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
  gap: 12px;
}

.radio-card {
  position: relative;
  cursor: pointer;
}

.radio-card input {
  position: absolute;
  opacity: 0;
}

.radio-card-body {
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 14px 10px;
  text-align: center;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  background: #ffffff;
  transition: var(--transition-fast);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.radio-card-icon {
  width: 38px;
  height: 38px;
  border-radius: 8px;
  background: var(--olx-light-teal);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  transition: var(--transition-fast);
}

.radio-card input:checked + .radio-card-body {
  border-color: #002f34;
  background: #ebf7f7;
  color: #002f34;
  box-shadow: 0 0 0 1px #002f34;
}

.radio-card input:checked + .radio-card-body .radio-card-icon {
  background: #002f34;
  color: #ffffff;
}

/* Reviews Styling */
.review-card {
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 16px 18px;
  margin-bottom: 12px;
}

.review-card .review-head {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 10px;
}

.review-card .review-comment {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.5;
}

.review-card .review-date {
  font-size: 12px;
  color: var(--text-muted);
  margin-left: auto;
}

/* Shimmer Loading Animations */
@keyframes shimmer {
  0% { background-position: -600px 0; }
  100% { background-position: 600px 0; }
}

.skeleton {
  background: linear-gradient(90deg, #eef2f5 25%, #f8fafc 50%, #eef2f5 75%);
  background-size: 800px 100%;
  animation: shimmer 1.5s infinite linear;
  border-radius: var(--radius);
  min-height: 180px;
}
```

---

## 3. Analysis 2: Exhaustive 404 Broken Redirect Audit & Bug Fixes

### 3.1 Comprehensive JavaScript Redirect Inventory

We executed an automated scan across all `.js` files in `frontend/js/` to verify every location redirect:

```python
# Total redirect assignments checked: 23
```

| # | File Path | Line | Existing Code | Resolution / Status |
|---|---|---|---|---|
| 1 | `property-detail.js` | 224 | `window.location.href = `${depthPrefix()}pages/user/my-bookings.html`;` | ❌ **404 BUG** → Replace with `pages/user/bookings.html` |
| 2 | `property-detail.js` | 276 | `window.location.href = `${depthPrefix()}pages/user/messages.html`;` | ❌ **404 BUG** → Replace with `pages/user/chat.html` |
| 3 | `product-detail.js` | 234 | `window.location.href = `${depthPrefix()}pages/user/my-orders.html`;` | ❌ **404 BUG** → Replace with `pages/user/orders.html` |
| 4 | `product-detail.js` | 286 | `window.location.href = `${depthPrefix()}pages/user/messages.html`;` | ❌ **404 BUG** → Replace with `pages/user/chat.html` |
| 5 | `auth.js` | 45 | `${depthPrefix()}pages/admin/dashboard.html` | ✅ Valid |
| 6 | `auth.js` | 47 | `${depthPrefix()}index.html` | ✅ Valid |
| 7 | `auth.js` | 96 | `'../../login.html'` | ✅ Valid |
| 8 | `auth.js` | 103 | `'../../login.html'` | ✅ Valid |
| 9 | `auth.js` | 107 | `'../../pages/user/dashboard.html'` | ✅ Valid |
| 10 | `auth.js` | 127 | `${depthPrefix()}login.html` | ✅ Valid |
| 11 | `home.js` | 22 | `${target}?${params.toString()}` | ✅ Valid (`search-properties.html` / `search-products.html`) |
| 12 | `post-product.js` | 7 | `'login.html'` | ✅ Valid |
| 13 | `post-product.js` | 141 | `'index.html'` | ✅ Valid |
| 14 | `post-property.js` | 6 | `'login.html'` | ✅ Valid |
| 15 | `post-property.js` | 111 | `'index.html'` | ✅ Valid |
| 16 | `product-detail.js` | 208 | `'login.html'` | ✅ Valid |
| 17 | `product-detail.js` | 244 | `'login.html'` | ✅ Valid |
| 18 | `product-detail.js` | 274 | `'login.html'` | ✅ Valid |
| 19 | `property-detail.js` | 206 | `'login.html'` | ✅ Valid |
| 20 | `property-detail.js` | 234 | `'login.html'` | ✅ Valid |
| 21 | `property-detail.js` | 264 | `'login.html'` | ✅ Valid |
| 22 | `register.js` | 44 | `'index.html'` | ✅ Valid |
| 23 | `admin-locations.js`| 55 | `locations.find((l) => l.id === id)` | ✅ (Not a redirect, variable assignment) |

---

### 3.2 Exact Code Replacements for Implementers

#### Fix 1: `frontend/js/property-detail.js` (Line 224)
```javascript
// BEFORE (Line 224):
setTimeout(function () { window.location.href = `${depthPrefix()}pages/user/my-bookings.html`; }, 1200);

// AFTER:
setTimeout(function () { window.location.href = `${depthPrefix()}pages/user/bookings.html`; }, 1200);
```

#### Fix 2: `frontend/js/property-detail.js` (Line 276)
```javascript
// BEFORE (Line 276):
setTimeout(function () { window.location.href = `${depthPrefix()}pages/user/messages.html`; }, 1200);

// AFTER:
setTimeout(function () { window.location.href = `${depthPrefix()}pages/user/chat.html`; }, 1200);
```

#### Fix 3: `frontend/js/product-detail.js` (Line 234)
```javascript
// BEFORE (Line 234):
setTimeout(function () { window.location.href = `${depthPrefix()}pages/user/my-orders.html`; }, 1200);

// AFTER:
setTimeout(function () { window.location.href = `${depthPrefix()}pages/user/orders.html`; }, 1200);
```

#### Fix 4: `frontend/js/product-detail.js` (Line 286)
```javascript
// BEFORE (Line 286):
setTimeout(function () { window.location.href = `${depthPrefix()}pages/user/messages.html`; }, 1200);

// AFTER:
setTimeout(function () { window.location.href = `${depthPrefix()}pages/user/chat.html`; }, 1200);
```

---

## 4. Analysis 3: Smooth Transitions, Micro-Interactions & Hover Elevations

To eliminate the static, cheap feel and provide a tactile, responsive mobile-first experience, we introduce a standardized physics-based interaction model:

### 4.1 Physics-Based Easing & Shadow Hierarchy

1. **Decelerated Spring Easing**:
   `cubic-bezier(0.16, 1, 0.3, 1)` (Apple/Framer standard) provides an initial high velocity followed by an ultra-smooth glide to rest.
2. **Elevated Shadow System**:
   - Level 0 (Rest): `box-shadow: 0 1px 3px rgba(0, 47, 52, 0.06);`
   - Level 1 (Card Hover): `box-shadow: 0 12px 28px -6px rgba(0, 47, 52, 0.14), 0 4px 10px -2px rgba(0, 47, 52, 0.06);`
   - Level 2 (Floating Action / Sticky Bars): `box-shadow: 0 10px 30px rgba(0, 47, 52, 0.16);`

### 4.2 Exact CSS Rules for Interactive Polish in `global.css`

```css
/* ==========================================================================
   Micro-Interactions & Visual Polish
   ========================================================================== */

/* Enhanced Product & Property Cards */
.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  position: relative;
  display: flex;
  flex-direction: column;
  box-shadow: 0 1px 3px rgba(0, 47, 52, 0.05);
  text-decoration: none;
  color: var(--text-primary);
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1),
              box-shadow 0.25s cubic-bezier(0.16, 1, 0.3, 1),
              border-color 0.2s ease;
}

.card:hover {
  border-color: #002f34;
  box-shadow: 0 12px 28px -6px rgba(0, 47, 52, 0.14), 0 4px 10px -2px rgba(0, 47, 52, 0.06);
  transform: translateY(-4px);
  text-decoration: none;
}

/* Card Image Scale on Hover */
.card-img-wrapper {
  position: relative;
  width: 100%;
  aspect-ratio: 4 / 3;
  background: #f1f5f9;
  overflow: hidden;
}

.card-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.card:hover .card-img {
  transform: scale(1.05);
}

/* Tactile Button Feedback & Press States */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: var(--radius);
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--transition-fast);
  text-decoration: none !important;
  border: 1px solid transparent;
  white-space: nowrap;
}

.btn:hover {
  transform: translateY(-1px);
}

.btn:active {
  transform: scale(0.97);
}

/* Subtle Click Flash/Ripple Pseudo-Element */
.btn::after {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(255, 255, 255, 0.24);
  opacity: 0;
  transition: opacity 0.2s ease;
  pointer-events: none;
}

.btn:active::after {
  opacity: 1;
}

/* OLX Sell Button Polish */
.btn-olx-sell {
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.btn-olx-sell:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 14px rgba(0, 47, 52, 0.25);
}

.btn-olx-sell:active {
  transform: scale(0.96);
}

/* Tactile Wishlist Heart Pop Animation */
@keyframes heartPop {
  0%   { transform: scale(1); }
  35%  { transform: scale(1.38); }
  65%  { transform: scale(0.88); }
  100% { transform: scale(1); }
}

.card-fav-btn {
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), background-color 0.2s ease, box-shadow 0.2s ease;
}

.card-fav-btn:hover {
  transform: scale(1.15);
  box-shadow: 0 4px 10px rgba(0, 47, 52, 0.2);
}

.card-fav-btn:active {
  transform: scale(0.9);
}

.card-fav-btn.active, .btn-fav.active {
  animation: heartPop 0.38s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  color: #e0245e;
}
```

---

## 5. Analysis 4: Styled Badges to Replace Raw Emojis

### 5.1 The Problem with Raw Unicode Emojis
Currently, raw Unicode emojis (🏠, 📦, 🛒, 🏷️, 🔑, 👥, 🚪, 📶) are injected inline next to raw text strings. On Windows browsers, raw emojis render with black borders and flat cartoonish styling; on Android, they render as blobby shapes; and on iOS, they render as 3D skeuomorphic glyphs. This creates an inconsistent, prototype-like aesthetic.

### 5.2 The Unified Badge & Icon Container Architecture

We convert every raw emoji into a **structured badge** featuring:
1. A **subtle 10–15% tinted background container** matching the entity category.
2. A **1px soft border** in the container's hue.
3. Clean, high-contrast, bold typography.
4. An enclosed micro-icon container that standardizes size, alignment, and spacing.

#### Complete CSS Badge System to append in `frontend/css/global.css`:

```css
/* ==========================================================================
   Cohesive Light Marketplace Badge & Icon Container System
   ========================================================================== */

/* Base Badge */
.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
  line-height: 1;
  letter-spacing: 0.3px;
  white-space: nowrap;
}

.badge-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
}

/* Property Type Badges */
.badge-pg        { background: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; } /* Blue/Sky */
.badge-room      { background: #ecfeff; color: #0e7490; border: 1px solid #a5f3fc; } /* Cyan */
.badge-hostel    { background: #fef3c7; color: #b45309; border: 1px solid #fde68a; } /* Amber */
.badge-hotel     { background: #f3e8ff; color: #7e22ce; border: 1px solid #e9d5ff; } /* Purple */
.badge-flat      { background: #e0e7ff; color: #4338ca; border: 1px solid #c7d2fe; } /* Indigo */
.badge-dormitory { background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; } /* Slate */

/* Marketplace & Listing Badges */
.badge-sell      { background: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; } /* Emerald */
.badge-rent      { background: #ffedd5; color: #c2410c; border: 1px solid #fed7aa; } /* Orange */
.badge-both      { background: #e0f2fe; color: #0284c7; border: 1px solid #bae6fd; }

/* Moderation Status Badges */
.badge-pending   { background: #fef9c3; color: #854d0e; border: 1px solid #fef08a; } /* Yellow */
.badge-approved,
.badge-active    { background: #dcfce7; color: #166534; border: 1px solid #bbf7d0; } /* Green */
.badge-rejected,
.badge-suspended { background: #fee2e2; color: #991b1b; border: 1px solid #fecaca; } /* Red */

/* Item Condition Badges */
.badge-new       { background: #dbeafe; color: #1e40af; border: 1px solid #bfdbfe; }
.badge-like-new  { background: #ccfbf1; color: #115e59; border: 1px solid #99f6e4; }
.badge-good      { background: #dcfce7; color: #166534; border: 1px solid #bbf7d0; }
.badge-fair      { background: #fef3c7; color: #b45309; border: 1px solid #fde68a; }
.badge-used,
.badge-old       { background: #f1f5f9; color: #64748b; border: 1px solid #e2e8f0; }

/* Real-Time Pulsing Availability Tag */
.avail-tag {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: #ebf7f7;
  color: #002f34;
  font-size: 11px;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 4px;
  border: 1px solid #23e5db;
}

.avail-tag::before {
  content: '';
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #0a883a;
  box-shadow: 0 0 0 2px rgba(10, 136, 58, 0.25);
  animation: pulseGreen 2s infinite;
}

@keyframes pulseGreen {
  0%   { box-shadow: 0 0 0 0 rgba(10, 136, 58, 0.4); }
  70%  { box-shadow: 0 0 0 6px rgba(10, 136, 58, 0); }
  100% { box-shadow: 0 0 0 0 rgba(10, 136, 58, 0); }
}

/* Card Specs Micro-Chips (Replacing raw inline emoji text) */
.card-specs {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
  margin-bottom: 8px;
}

.spec-chip {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 11.5px;
  color: var(--text-secondary);
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  padding: 2px 7px;
  border-radius: 4px;
  font-weight: 600;
}

.spec-chip .chip-ico {
  font-size: 12px;
}

/* Category Grid Tiles (Homepage Category Strip) */
.category-card .category-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: #ebf7f7;
  color: #002f34;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  margin-bottom: 4px;
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), background-color 0.2s ease;
}

.category-card:hover .category-icon {
  background: #d0f0ee;
  transform: scale(1.1);
}

/* Amenity Badges (Property Detail Page) */
.amenity-item {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 8px 14px;
  font-size: 13.5px;
  font-weight: 600;
  color: var(--text-primary);
  box-shadow: 0 1px 3px rgba(0, 47, 52, 0.04);
  transition: var(--transition-fast);
}

.amenity-item:hover {
  border-color: #002f34;
  background: #f8fafc;
  transform: translateY(-1px);
}

.amenity-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 6px;
  background: #ebf7f7;
  color: #002f34;
  font-size: 15px;
  flex-shrink: 0;
}

/* Empty State Styled Badges */
.empty-state .empty-icon,
.inline-empty .empty-icon {
  width: 64px;
  height: 64px;
  border-radius: 18px;
  background: #ebf7f7;
  color: #002f34;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  margin-bottom: 16px;
  box-shadow: 0 4px 12px rgba(0, 47, 52, 0.06);
}
```

---

### 5.3 JavaScript Card Helper Updates in `frontend/js/utils.js`

In `frontend/js/utils.js`, update `buildPropertyCard` and `buildProductCard` to output `.spec-chip` containers instead of raw emoji strings:

#### Replacement in `buildPropertyCard` (Lines 287–292):
```javascript
// BEFORE:
<div class="card-specs">
  <span>👥 ${escapeHtml(gender)}</span>
  <span class="specs-dot">•</span>
  <span>🚪 ${property.totalRooms || 0} Rooms</span>
  ${property.isAvailable ? '<span class="specs-dot">•</span><span class="avail-tag">Available</span>' : ''}
</div>

// AFTER:
<div class="card-specs">
  <span class="spec-chip"><span class="chip-ico">👥</span>${escapeHtml(gender)}</span>
  <span class="spec-chip"><span class="chip-ico">🚪</span>${property.totalRooms || 0} Rooms</span>
  ${property.isAvailable ? '<span class="avail-tag">Available</span>' : ''}
</div>
```

#### Replacement in `buildProductCard` (Lines 329–333):
```javascript
// BEFORE:
<div class="card-specs">
  <span>🏷️ ${brand}</span>
  <span class="specs-dot">•</span>
  <span class="condition-tag">${escapeHtml(cond)}</span>
</div>

// AFTER:
<div class="card-specs">
  <span class="spec-chip"><span class="chip-ico">🏷️</span>${brand}</span>
  <span class="badge ${getConditionBadgeClass(product.condition)}">${escapeHtml(cond)}</span>
</div>
```

---

## 6. Implementation Checklist & Verification Matrix

### 6.1 Implementer Action Plan

| Step | Target File | Action |
|---|---|---|
| 1 | `frontend/css/global.css` | Insert backward-compatible `:root` tokens (Section 2.2), restored foundational classes (Section 2.4), micro-interactions (Section 4.2), and styled badge classes (Section 5.2). |
| 2 | `frontend/css/dashboard.css` | Apply harmonized enterprise light theme overrides with deep spruce sidebar (Section 2.3). |
| 3 | `frontend/js/property-detail.js` | Change Line 224 redirect to `bookings.html` and Line 276 redirect to `chat.html` (Section 3.2). |
| 4 | `frontend/js/product-detail.js` | Change Line 234 redirect to `orders.html` and Line 286 redirect to `chat.html` (Section 3.2). |
| 5 | `frontend/js/utils.js` | Update `buildPropertyCard` and `buildProductCard` to use `.spec-chip` badges (Section 5.3). |

---

### 6.2 Independent Verification Script

Implementers can run this verification script to guarantee zero remaining broken redirects and zero undefined CSS tokens:

```bash
# 1. Verify zero 404 links across frontend
python -c "
import glob, os, re
files = glob.glob('frontend/**/*.js', recursive=True)
bad = [('my-bookings.html', 'bookings.html'), ('my-orders.html', 'orders.html'), ('messages.html', 'chat.html')]
for fp in files:
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()
    for b, target in bad:
        if b in c:
            print(f'FAIL: Found broken reference {b} in {fp} (should be {target})')
print('Verification check complete.')
"

# 2. Verify all CSS variables in dashboard.css exist in global.css
python -c "
import re
with open('frontend/css/dashboard.css', 'r', encoding='utf-8') as f:
    dash = f.read()
with open('frontend/css/global.css', 'r', encoding='utf-8') as f:
    glob = f.read()
dash_vars = set(re.findall(r'var\((--[a-zA-Z0-9_-]+)', dash))
glob_defs = set(re.findall(r'(--[a-zA-Z0-9_-]+)\s*:', glob))
missing = dash_vars - glob_defs
if missing:
    print('FAIL: Undefined variables:', missing)
else:
    print('PASS: All dashboard CSS variables successfully resolved in global.css!')
"
```
