import os

css_content = """/* ==========================================================================
   StayMart - Authentic OLX & Amazon-Inspired Marketplace Theme
   Designed for Dehradun & Uttarakhand Classifieds & Student Rentals
   ========================================================================== */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root {
  /* Brand Palette: OLX Deep Teal + Amazon Amber Accent */
  --header-bg: #002f34;            /* Iconic OLX Deep Spruce */
  --header-text: #ffffff;
  --header-hover: #23e5db;
  
  --amazon-amber: #ff9900;          /* Amazon Marketplace Orange */
  --amazon-yellow: #ffd814;         /* Amazon Primary Button */
  --amazon-yellow-hover: #f7ca00;
  --amazon-dark: #0f1111;
  
  --olx-teal: #002f34;
  --olx-cyan: #23e5db;
  --olx-light-teal: #ebf7f7;
  
  /* Modern Commercial Neutral Surfaces (Clean Light Theme) */
  --bg-page: #f2f4f5;              /* The authentic OLX light neutral canvas */
  --bg-card: #ffffff;
  --bg-hover: #f8fafc;
  --bg-subtle: #f8fafc;
  
  /* Text & Typography */
  --text-primary: #002f34;          /* High contrast, ultra-readable */
  --text-secondary: #465666;        /* Subtitles & metadata */
  --text-muted: #7f9799;            /* Dates & fine print */
  --text-link: #007185;             /* Amazon-style hyperlink blue */
  
  /* Borders & Dividers */
  --border: #e2e8f0;
  --border-subtle: #ebedf0;
  --border-focus: #002f34;
  
  /* Status & Accents */
  --success: #0a883a;
  --danger: #d9381e;
  --warning: #f59e0b;
  --info: #007185;
  
  /* Elevation & Shadows */
  --shadow-sm: 0 1px 3px rgba(0, 47, 52, 0.08);
  --shadow-md: 0 4px 12px rgba(0, 47, 52, 0.1);
  --shadow-lg: 0 10px 25px rgba(0, 47, 52, 0.14);
  
  /* Layout Dimensions */
  --radius-sm: 4px;
  --radius: 6px;
  --radius-lg: 10px;
  --radius-full: 999px;
  --font: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Base Styles */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  background-color: var(--bg-page);
  color: var(--text-primary);
  font-family: var(--font);
  font-size: 15px;
  line-height: 1.5;
  min-height: 100vh;
  -webkit-font-smoothing: antialiased;
}

a {
  color: var(--text-link);
  text-decoration: none;
  transition: var(--transition);
}

a:hover {
  color: #c7511f;
  text-decoration: underline;
}

img {
  max-width: 100%;
  height: auto;
  display: block;
}

input, select, textarea, button {
  font-family: var(--font);
  font-size: 14px;
}

.container {
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 16px;
}

/* ==========================================================================
   Top Header (Amazon / OLX Commercial Style)
   ========================================================================== */
.navbar {
  position: sticky;
  top: 0;
  z-index: 1000;
  background: var(--header-bg);
  color: var(--header-text);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  height: 72px;
  display: flex;
  align-items: center;
}

.navbar-inner {
  max-width: 1280px;
  width: 100%;
  margin: 0 auto;
  padding: 0 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

/* Logo */
.logo {
  display: flex;
  align-items: center;
  gap: 2px;
  font-size: 26px;
  font-weight: 900;
  color: #ffffff;
  letter-spacing: -0.5px;
  text-decoration: none;
  flex-shrink: 0;
}

.logo:hover {
  text-decoration: none;
}

.logo-stay {
  color: #ffffff;
}

.logo-mart {
  color: var(--amazon-amber);
  position: relative;
}

.logo-badge {
  font-size: 10px;
  font-weight: 700;
  background: #ffce32;
  color: #002f34;
  padding: 2px 6px;
  border-radius: 4px;
  margin-left: 6px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.logo small {
  display: block;
  font-size: 10px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.7);
  letter-spacing: 0.5px;
  margin-top: 1px;
}

/* OLX Location Selector Dropdown */
.nav-location {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #ffffff;
  color: var(--text-primary);
  border: 2px solid #002f34;
  border-radius: var(--radius);
  padding: 6px 12px;
  cursor: pointer;
  position: relative;
  font-size: 13px;
  font-weight: 600;
  flex-shrink: 0;
  min-width: 150px;
  user-select: none;
}

.nav-location .loc-pin {
  font-size: 16px;
}

.nav-location .loc-text {
  display: flex;
  flex-direction: column;
  line-height: 1.1;
}

.nav-location .loc-label {
  font-size: 10px;
  text-transform: uppercase;
  color: var(--text-muted);
}

.nav-location .loc-val {
  font-weight: 700;
  color: var(--text-primary);
}

.nav-location .loc-arrow {
  margin-left: auto;
  font-size: 10px;
  color: var(--text-secondary);
}

.loc-dropdown {
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow-lg);
  min-width: 220px;
  display: none;
  z-index: 1050;
  padding: 6px 0;
}

.loc-dropdown.open {
  display: block;
}

.loc-dropdown-title {
  padding: 8px 14px;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--text-muted);
  border-bottom: 1px solid var(--border-subtle);
}

.loc-item {
  padding: 8px 14px;
  font-size: 13px;
  color: var(--text-primary);
  cursor: pointer;
  transition: var(--transition);
}

.loc-item:hover, .loc-item.active {
  background: var(--olx-light-teal);
  color: var(--olx-teal);
  font-weight: 600;
}

/* Amazon-Style Unified Search Bar */
.nav-search-bar {
  display: flex;
  align-items: center;
  flex: 1;
  max-width: 580px;
  background: #ffffff;
  border-radius: var(--radius);
  overflow: hidden;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
  border: 2px solid transparent;
  transition: var(--transition);
}

.nav-search-bar:focus-within {
  border-color: var(--amazon-amber);
  box-shadow: 0 0 0 2px rgba(255, 153, 0, 0.25);
}

.search-cat-picker {
  background: #f3f4f6;
  border-right: 1px solid #d1d5db;
  height: 42px;
  display: flex;
  align-items: center;
}

.search-cat-picker select {
  border: none;
  background: transparent;
  padding: 0 10px;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
  cursor: pointer;
  outline: none;
  height: 100%;
}

.nav-search-bar input {
  flex: 1;
  border: none;
  padding: 10px 14px;
  font-size: 14px;
  color: var(--text-primary);
  outline: none;
  height: 42px;
}

.nav-search-bar input::placeholder {
  color: #9ca3af;
}

.nav-search-btn {
  background: var(--amazon-amber);
  border: none;
  width: 46px;
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #0f1111;
  transition: var(--transition);
}

.nav-search-btn:hover {
  background: #f38f00;
}

/* Navigation Links */
.nav-links {
  display: flex;
  align-items: center;
  gap: 18px;
}

.nav-links a {
  color: #ffffff;
  font-weight: 600;
  font-size: 14px;
  text-decoration: none;
  padding: 6px 10px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  gap: 6px;
}

.nav-links a:hover, .nav-links a.active {
  background: rgba(255, 255, 255, 0.12);
  color: var(--amazon-amber);
  text-decoration: none;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* The Signature OLX "+ SELL" Button */
.btn-olx-sell {
  background: #ffffff;
  color: #002f34 !important;
  font-weight: 800;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 6px 20px;
  border-radius: var(--radius-full);
  border: 4px solid;
  border-color: #23e5db #ffce32 #3a77ff #23e5db; /* Authentic OLX Multi-color Border */
  display: inline-flex;
  align-items: center;
  gap: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.18);
  transition: all 0.2s ease;
  cursor: pointer;
  text-decoration: none !important;
  white-space: nowrap;
}

.btn-olx-sell:hover {
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);
  background: #fcfcfc;
}

.btn-olx-sell .sell-plus {
  font-size: 18px;
  line-height: 1;
}

/* Sub-Header Horizontal Category Strip (Amazon / OLX style) */
.category-strip {
  background: #ffffff;
  border-bottom: 1px solid var(--border);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.category-strip-inner {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 16px;
  display: flex;
  align-items: center;
  gap: 16px;
  overflow-x: auto;
  white-space: nowrap;
  scrollbar-width: none;
  height: 44px;
}

.category-strip-inner::-webkit-scrollbar {
  display: none;
}

.cat-strip-item {
  color: var(--text-primary);
  font-size: 13px;
  font-weight: 600;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 8px;
  border-radius: var(--radius-sm);
  transition: var(--transition);
}

.cat-strip-item:hover {
  color: #007185;
  background: #f1f5f9;
  text-decoration: none;
}

.cat-strip-item.cat-all {
  font-weight: 800;
  color: var(--header-bg);
}

.cat-strip-item.cat-deals {
  color: #c7511f;
  font-weight: 700;
}

/* ==========================================================================
   Hero & Promotion Banner (Authentic Marketplace Style)
   ========================================================================== */
.hero {
  background: linear-gradient(180deg, #ffffff 0%, #f7f9fa 100%);
  border-bottom: 1px solid var(--border);
  padding: 32px 0 28px;
}

.hero-banner-grid {
  display: grid;
  grid-template-columns: 1.8fr 1.2fr;
  gap: 24px;
  align-items: center;
}

.hero-headline {
  font-size: 32px;
  font-weight: 800;
  color: var(--text-primary);
  line-height: 1.25;
  letter-spacing: -0.5px;
}

.hero-headline span.highlight {
  color: #007185;
  border-bottom: 3px solid var(--amazon-amber);
}

.hero-subheadline {
  font-size: 15px;
  color: var(--text-secondary);
  margin-top: 10px;
  line-height: 1.6;
}

.campus-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 18px;
}

.campus-chip {
  background: #ffffff;
  border: 1px solid var(--border);
  color: var(--text-primary);
  font-size: 12px;
  font-weight: 600;
  padding: 6px 12px;
  border-radius: var(--radius-full);
  display: inline-flex;
  align-items: center;
  gap: 6px;
  text-decoration: none;
  transition: var(--transition);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
}

.campus-chip:hover {
  border-color: var(--header-bg);
  color: var(--header-bg);
  background: var(--olx-light-teal);
  text-decoration: none;
}

.hero-promo-card {
  background: #ffffff;
  border: 2px dashed #002f34;
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--shadow-sm);
  text-align: center;
}

.hero-promo-card h3 {
  font-size: 18px;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.hero-promo-card p {
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 16px;
}

.hero-stats {
  display: flex;
  justify-content: space-around;
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid var(--border-subtle);
}

.stat-item {
  text-align: center;
}

.stat-num {
  font-size: 20px;
  font-weight: 800;
  color: var(--text-primary);
}

.stat-lbl {
  font-size: 12px;
  color: var(--text-muted);
}

/* ==========================================================================
   Product & Property Cards (Authentic OLX India Style)
   ========================================================================== */
.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 6px;
  overflow: hidden;
  transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
  position: relative;
  display: flex;
  flex-direction: column;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  text-decoration: none;
  color: var(--text-primary);
}

.card:hover {
  border-color: #002f34;
  box-shadow: 0 4px 16px rgba(0, 47, 52, 0.14);
  transform: translateY(-3px);
  text-decoration: none;
}

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
  transition: transform 0.3s ease;
}

.card:hover .card-img {
  transform: scale(1.04);
}

/* Card Top Badges & Wishlist Button */
.card-badge-top {
  position: absolute;
  top: 10px;
  left: 10px;
  z-index: 2;
  font-size: 11px;
  font-weight: 800;
  padding: 3px 8px;
  border-radius: 4px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.badge-featured {
  background: #ffce32;
  color: #002f34;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
}

.badge-verified {
  background: #002f34;
  color: #ffffff;
}

.card-fav-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 2;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #002f34;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.12);
  transition: var(--transition);
}

.card-fav-btn:hover {
  transform: scale(1.1);
  color: #e11d48;
}

.card-fav-btn.active {
  color: #e11d48;
  fill: #e11d48;
}

/* Card Body (OLX Layout: Price First -> Title -> Specs -> Location/Date) */
.card-body {
  padding: 12px 14px 14px;
  display: flex;
  flex-direction: column;
  flex: 1;
  gap: 6px;
}

.card-price-row {
  display: flex;
  align-items: baseline;
  gap: 6px;
}

.card-price {
  font-size: 20px;
  font-weight: 800;
  color: #002f34;
  letter-spacing: -0.3px;
}

.card-price .price-type {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
}

.card-title {
  font-size: 14px;
  font-weight: 600;
  color: #002f34;
  line-height: 1.4;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  min-height: 40px;
}

.card-specs {
  font-size: 12px;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 6px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.specs-dot {
  color: #cbd5e1;
}

.condition-tag {
  background: #f1f5f9;
  padding: 1px 6px;
  border-radius: 3px;
  font-weight: 600;
  color: var(--text-secondary);
}

.avail-tag {
  color: #0a883a;
  font-weight: 700;
}

/* Card Bottom Line (Location + Time Ago - Exactly like OLX) */
.card-footer-olx {
  margin-top: auto;
  padding-top: 8px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 11px;
  color: var(--text-muted);
  border-top: 1px solid var(--border-subtle);
}

.card-loc {
  display: flex;
  align-items: center;
  gap: 4px;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 60%;
}

.card-date {
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* ==========================================================================
   Grids & Layout Containers
   ========================================================================== */
.section {
  padding: 32px 0;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  border-bottom: 2px solid var(--border);
  padding-bottom: 10px;
}

.section-title {
  font-size: 22px;
  font-weight: 800;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-link {
  font-size: 13px;
  font-weight: 700;
  color: #007185;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.section-link:hover {
  color: #c7511f;
}

.grid-4 {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
}

.grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}

.h-scroll {
  display: grid;
  grid-auto-flow: column;
  grid-auto-columns: minmax(260px, 1fr);
  gap: 16px;
  overflow-x: auto;
  padding-bottom: 12px;
  scrollbar-width: thin;
}

/* Category Grid on Homepage */
.category-grid {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 12px;
}

.category-card {
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 14px 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 8px;
  text-decoration: none;
  color: var(--text-primary);
  transition: var(--transition);
  box-shadow: var(--shadow-sm);
}

.category-card:hover {
  border-color: #002f34;
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
  text-decoration: none;
}

.category-icon {
  font-size: 28px;
}

.category-name {
  font-size: 12px;
  font-weight: 700;
  line-height: 1.2;
}

/* ==========================================================================
   Buttons & Interactive Elements
   ========================================================================== */
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
  transition: var(--transition);
  text-decoration: none !important;
  border: 1px solid transparent;
  white-space: nowrap;
}

.btn-primary {
  background: var(--amazon-yellow);
  border-color: #fcd200;
  color: var(--amazon-dark) !important;
}

.btn-primary:hover {
  background: var(--amazon-yellow-hover);
  border-color: #f2c200;
  box-shadow: 0 2px 5px rgba(213, 217, 217, 0.5);
}

.btn-secondary {
  background: #ffffff;
  border-color: #d5d9d9;
  color: var(--text-primary) !important;
  box-shadow: 0 2px 5px rgba(213, 217, 217, 0.5);
}

.btn-secondary:hover {
  background: #f7fafa;
  border-color: #002f34;
}

.btn-teal {
  background: var(--header-bg);
  color: #ffffff !important;
}

.btn-teal:hover {
  background: #001f23;
  color: #ffffff !important;
}

.btn-block {
  width: 100%;
}

.btn-sm {
  padding: 6px 14px;
  font-size: 13px;
}

/* ==========================================================================
   Search & Filter Sidebar (Amazon Faceted Navigation)
   ========================================================================== */
.filter-sidebar {
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 18px;
  box-shadow: var(--shadow-sm);
}

.filter-group {
  padding: 14px 0;
  border-bottom: 1px solid var(--border-subtle);
}

.filter-group:first-child {
  padding-top: 0;
}

.filter-group-title {
  font-size: 14px;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 10px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.check-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--text-secondary);
  cursor: pointer;
  margin-bottom: 6px;
  user-select: none;
}

.check-row:hover {
  color: var(--text-primary);
}

.check-row input[type=\"checkbox\"],
.check-row input[type=\"radio\"] {
  accent-color: #002f34;
  width: 16px;
  height: 16px;
}

.price-range {
  display: flex;
  align-items: center;
  gap: 8px;
}

.price-range input {
  width: 100%;
  padding: 8px 10px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  outline: none;
}

.price-range input:focus {
  border-color: #002f34;
}

.results-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 10px 16px;
}

.results-count {
  font-size: 14px;
  font-weight: 700;
  color: var(--text-primary);
}

/* ==========================================================================
   Product & Property Detail View (Amazon & OLX Hybrid)
   ========================================================================== */
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--text-muted);
  margin-bottom: 16px;
}

.breadcrumb a {
  color: var(--text-link);
}

.breadcrumb .sep {
  color: #94a3b8;
}

.detail-layout {
  display: grid;
  grid-template-columns: 2fr 1.2fr;
  gap: 28px;
  align-items: start;
}

.detail-main-card {
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 24px;
  box-shadow: var(--shadow-sm);
}

.gallery-main {
  width: 100%;
  aspect-ratio: 16 / 10;
  background: #f8fafc;
  border-radius: var(--radius);
  overflow: hidden;
  border: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.gallery-main img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  background: #ffffff;
}

.gallery-thumbs {
  display: flex;
  gap: 10px;
  margin-top: 12px;
  overflow-x: auto;
}

.gallery-thumbs img {
  width: 72px;
  height: 72px;
  object-fit: cover;
  border-radius: var(--radius);
  border: 2px solid var(--border);
  cursor: pointer;
  transition: var(--transition);
}

.gallery-thumbs img.active, .gallery-thumbs img:hover {
  border-color: #002f34;
}

.detail-title {
  font-size: 24px;
  font-weight: 800;
  color: #002f34;
  margin: 20px 0 10px;
  line-height: 1.3;
}

.detail-meta-bar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 12px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border-subtle);
  font-size: 13px;
  color: var(--text-secondary);
}

.detail-meta-bar .badge {
  font-size: 12px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 4px;
}

/* Sidebar Price & Seller Cards (OLX Style) */
.sidebar-box {
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
  box-shadow: var(--shadow-sm);
  margin-bottom: 18px;
}

.price-box-amount {
  font-size: 32px;
  font-weight: 900;
  color: #002f34;
  margin-bottom: 4px;
}

.price-box-sub {
  font-size: 13px;
  color: var(--text-muted);
  margin-bottom: 18px;
}

.seller-profile-box {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 16px;
}

.seller-avatar {
  width: 54px;
  height: 54px;
  border-radius: 50%;
  background: #002f34;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  font-weight: 800;
}

.seller-info h4 {
  font-size: 16px;
  font-weight: 800;
  color: #002f34;
}

.seller-info p {
  font-size: 12px;
  color: var(--text-muted);
}

.seller-verified-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  font-weight: 700;
  color: #0a883a;
  margin-top: 2px;
}

.safety-tips-box {
  background: #fffbeb;
  border: 1px solid #fef3c7;
  border-radius: var(--radius);
  padding: 16px;
  font-size: 12px;
  color: #92400e;
  line-height: 1.6;
}

.safety-tips-box h5 {
  font-size: 13px;
  font-weight: 800;
  color: #b45309;
  margin-bottom: 6px;
}

/* ==========================================================================
   Footer
   ========================================================================== */
.footer {
  background: #002f34;
  color: #ffffff;
  margin-top: 48px;
  padding: 48px 0 24px;
  border-top: 4px solid var(--amazon-amber);
}

.footer-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 36px;
  padding-bottom: 36px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.footer h4 {
  font-size: 15px;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 16px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.footer-links {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.footer-links a {
  color: rgba(255, 255, 255, 0.75);
  font-size: 13px;
  text-decoration: none;
}

.footer-links a:hover {
  color: var(--amazon-amber);
  text-decoration: underline;
}

.footer-bottom {
  text-align: center;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
  margin-top: 24px;
}

/* Toasts & Modals */
.toast-container {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.toast {
  background: #002f34;
  color: #ffffff;
  padding: 12px 20px;
  border-radius: var(--radius);
  font-size: 14px;
  font-weight: 600;
  box-shadow: var(--shadow-lg);
  opacity: 0;
  transform: translateY(10px);
  transition: all 0.3s ease;
}

.toast.show {
  opacity: 1;
  transform: translateY(0);
}

.toast-success { border-left: 4px solid #10b981; }
.toast-error { border-left: 4px solid #ef4444; }

/* Responsive */
@media (max-width: 1024px) {
  .grid-4 { grid-template-columns: repeat(3, 1fr); }
  .category-grid { grid-template-columns: repeat(4, 1fr); }
  .hero-banner-grid { grid-template-columns: 1fr; }
  .detail-layout { grid-template-columns: 1fr; }
}

@media (max-width: 768px) {
  .grid-4, .grid-3 { grid-template-columns: repeat(2, 1fr); }
  .category-grid { grid-template-columns: repeat(3, 1fr); }
  .navbar-inner { flex-wrap: wrap; height: auto; padding: 12px 16px; }
  .nav-search-bar { order: 3; max-width: 100%; width: 100%; margin-top: 10px; }
  .nav-location { display: none; }
  .footer-grid { grid-template-columns: 1fr; }
}

@media (max-width: 480px) {
  .grid-4, .grid-3 { grid-template-columns: 1fr; }
  .category-grid { grid-template-columns: repeat(2, 1fr); }
}
"""

with open("frontend/css/global.css", "w", encoding="utf-8") as f:
    f.write(css_content)

print("Updated frontend/css/global.css with authentic OLX + Amazon theme!")

