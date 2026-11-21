# StayMart Mobile-First Navigation, Drawers & Action Bars Implementation Plan

**Specialist**: M1 Explorer 2 (Navigation, Drawers & Action Bars Specialist)  
**Date**: November 2, 2026  
**Target File**: `d:\Mini5th\.agents\teamwork\m1_explorer_2\plan_navigation.md`  
**Milestone**: Milestone 1 (Frontend Mobile-First Overhaul & Visual Polish — Features 2, 3, 4)  
**Status**: Production-Ready Architectural & Implementation Blueprint (Read-Only Investigation)

---

## Executive Summary

StayMart's frontend is a vanilla HTML5, CSS3, and ES6+ Multi-Page Application (MPA). While desktop browsing is functional, the mobile experience (< 768px, specifically 375px iPhone viewports) suffers from critical usability breakdowns:
1. **Desktop Navbar Overcrowding**: Row 1 contains brand logo (~120px) + nav links (~240px) + nav actions (~250px) = >610px of content. On a 375px mobile viewport, these wrap into 3 disorganized rows or cause horizontal viewport overflow.
2. **Missing Navigation Drawer**: Public users on mobile lack a consolidated menu for browsing student categories, campus hubs, user space links, and authentication controls.
3. **Absence of Mobile Bottom Navigation**: Users must scroll back to the top to switch between accommodations, marketplace, messages, and account.
4. **Desktop Filter Sidebar Grid Lock**: In `search-properties.html` and `search-products.html`, an inline `style="grid-template-columns:260px 1fr"` overrides responsive media queries, breaking 375px screens. Furthermore, filters stack directly above listings, forcing users to scroll past 25+ inputs before seeing a single card.
5. **Detail Page Action Card Buried**: On `property-detail.html` and `product-detail.html`, `<aside class="sidebar-sticky">` drops below the entire main column (including gallery, facilities, 1,200px+ reviews, and similar listings). Mobile students cannot view the price or access the "Book Now" / "Buy Now" button without scrolling to the page footer.

This document delivers an **exact, zero-dependency, production-ready specification** for Features 2, 3, and 4, complete with HTML markup, CSS styling rules, lightweight ES6 handlers, and integration blueprints.

---

## 1. Feature 2A: Public Navbar Overhaul (375px Overflow-Proof Header)

### 1.1 Problem Analysis & Viewport Budgeting
On a 375px mobile viewport:
- Usable width with 12px outer padding = **351px**.
- **Current Desktop Header Demand**:
  - Logo: 120px
  - Location Selector: 150px
  - Nav Links (🏠 Accommodations, 🛒 Buy & Sell): 230px
  - Nav Actions (Messages 38px + Wishlist 38px + Avatar 38px + "+ SELL" 105px): 219px
  - Total Row 1 demand: **719px** (Over 200% of available mobile width).
- **Target Mobile Header Budget (Single Fixed Row at 60px Height)**:
  - Left group: Hamburger button (40px) + Logo (~110px) = 150px
  - Right group: Search Toggle (38px) + Messages/Wishlist badge (38px) + Avatar / Quick Action (36px) = 112px
  - Middle gap / flex space: 89px
  - **Total: 351px**. Fits cleanly within 375px with zero wrapping, zero overflow, and zero height jitter.

---

### 1.2 Unified Navbar HTML Structure

Replace the fragmented navbar headers across all public pages (`index.html`, `search-properties.html`, `search-products.html`, `property-detail.html`, `product-detail.html`, `post-property.html`, `post-product.html`) with this unified semantic structure:

```html
<!-- Unified Sticky Commercial Navbar -->
<header class="navbar" id="siteNavbar">
  <div class="navbar-inner">
    <!-- Left Section: Mobile Hamburger Toggle + Brand Mark -->
    <div class="nav-left">
      <button class="nav-mobile-toggle" id="mobileMenuToggle" aria-label="Open mobile menu" onclick="openMobileDrawer()">
        <span class="hamburger-bar"></span>
        <span class="hamburger-bar"></span>
        <span class="hamburger-bar"></span>
      </button>

      <a href="index.html" class="logo">
        <span class="logo-stay">Stay</span><span class="logo-mart">Mart</span>
        <span class="logo-badge">UK</span>
      </a>
    </div>

    <!-- Center Section: Desktop Location Selector + Desktop Search Bar -->
    <div class="nav-center">
      <!-- Location Selector Dropdown (Desktop Only) -->
      <div class="nav-location" id="navLocationBtn" onclick="toggleLocationDropdown(event)">
        <span class="loc-pin">📍</span>
        <div class="loc-text">
          <span class="loc-label">Location</span>
          <span class="loc-val" id="selectedCityLabel">Dehradun</span>
        </div>
        <span class="loc-arrow">▼</span>
        <div class="loc-dropdown" id="navLocDropdown">
          <div class="loc-dropdown-title">Popular Campus Hubs</div>
          <div class="loc-item active" onclick="selectCity('Dehradun')">📍 Dehradun (All Areas)</div>
          <div class="loc-item" onclick="selectCity('Clement Town')">🎓 Clement Town (Graphic Era)</div>
          <div class="loc-item" onclick="selectCity('Premnagar')">🎓 Premnagar / Bidholi (UPES)</div>
          <div class="loc-item" onclick="selectCity('Rajpur Road')">🎓 Rajpur Road / DIT</div>
          <div class="loc-item" onclick="selectCity('Rishikesh')">🏔️ Rishikesh</div>
          <div class="loc-item" onclick="selectCity('Roorkee')">🏛️ Roorkee (IIT)</div>
        </div>
      </div>

      <!-- Unified Amazon/OLX Desktop Search Bar -->
      <form class="nav-search-bar" id="desktopNavSearch" onsubmit="handleNavSearch(event)">
        <div class="search-cat-picker">
          <select id="navCatSelect" aria-label="Select search category">
            <option value="all">All</option>
            <option value="properties">Accommodations</option>
            <option value="products">Buy & Sell</option>
          </select>
        </div>
        <input id="navSearchInput" type="text" placeholder="Find PGs, flats, laptops, books, cycles..." autocomplete="off"/>
        <button type="submit" class="nav-search-btn" title="Search listings">🔍</button>
      </form>
    </div>

    <!-- Right Section: Desktop Links + Quick Actions / Auth -->
    <div class="nav-right">
      <!-- Desktop Navigation Links -->
      <nav class="nav-links">
        <a href="search-properties.html" class="nav-link-item" data-page="properties">🏠 Accommodations</a>
        <a href="search-products.html" class="nav-link-item" data-page="products">🛒 Buy & Sell</a>
      </nav>

      <!-- Mobile Search Toggle Button (Visible only on < 768px) -->
      <button class="nav-icon-btn mobile-search-trigger" id="mobileSearchTrigger" aria-label="Search" onclick="toggleMobileSearch()">
        🔍
      </button>

      <!-- Auth Actions Container (Populated dynamically by Auth.updateNavbar()) -->
      <div class="nav-actions" id="navActions">
        <!-- Logged out: [Login] [+ SELL] -->
        <!-- Logged in: [Chat] [Wishlist] [Avatar dropdown] [+ SELL] -->
      </div>
    </div>
  </div>

  <!-- Expandable Mobile Search Sub-Bar (Slides down on < 768px when 🔍 is tapped) -->
  <div class="mobile-search-drawer" id="mobileSearchDrawer">
    <form class="mobile-search-form" onsubmit="handleNavSearch(event)">
      <div class="mobile-search-inner">
        <span class="search-lens">🔍</span>
        <input id="mobileSearchInput" type="text" placeholder="Search PGs, rooms, laptops, books..." autocomplete="off"/>
        <button type="button" class="search-clear-btn" id="mobileSearchClear" onclick="clearMobileSearch()">✕</button>
        <button type="submit" class="search-go-btn">Go</button>
      </div>
    </form>
  </div>
</header>
```

---

### 1.3 Navbar CSS Specification (Add to `frontend/css/global.css`)

```css
/* ==========================================================================
   Mobile-First Responsive Commercial Header
   ========================================================================== */
.navbar {
  position: sticky;
  top: 0;
  z-index: 1000;
  background: var(--header-bg);
  color: var(--header-text);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.18);
  height: 64px;
  display: flex;
  align-items: center;
  transition: all 0.25s ease;
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
  height: 100%;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}

.nav-center {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
  max-width: 680px;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

/* Hamburger Button */
.nav-mobile-toggle {
  display: none; /* Desktop default */
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
  transition: var(--transition);
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

/* Mobile Search Trigger Icon */
.mobile-search-trigger {
  display: none;
}

/* Expandable Mobile Search Drawer */
.mobile-search-drawer {
  display: none;
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: var(--header-bg);
  padding: 10px 16px 14px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.22);
  transform: translateY(-8px);
  opacity: 0;
  pointer-events: none;
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.25s ease;
  z-index: 998;
}

.mobile-search-drawer.open {
  transform: translateY(0);
  opacity: 1;
  pointer-events: auto;
}

.mobile-search-inner {
  display: flex;
  align-items: center;
  background: #ffffff;
  border-radius: var(--radius);
  padding: 2px 6px 2px 12px;
  border: 2px solid transparent;
  transition: border-color 0.2s ease;
}

.mobile-search-inner:focus-within {
  border-color: var(--amazon-amber);
}

.mobile-search-inner .search-lens {
  font-size: 15px;
  color: var(--text-muted);
  margin-right: 8px;
}

.mobile-search-inner input {
  flex: 1;
  height: 40px;
  border: none;
  outline: none;
  font-size: 14px;
  color: var(--text-primary);
  background: transparent;
}

.search-clear-btn {
  background: none;
  border: none;
  font-size: 16px;
  color: #94a3b8;
  cursor: pointer;
  padding: 4px 8px;
  display: none;
}

.search-go-btn {
  background: var(--amazon-amber);
  color: #0f1111;
  font-weight: 700;
  font-size: 13px;
  border: none;
  padding: 7px 14px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  margin-left: 4px;
}

/* ==========================================================================
   Header Mobile Breakpoints (< 768px & 375px)
   ========================================================================== */
@media (max-width: 768px) {
  .navbar {
    height: 58px;
  }

  .navbar-inner {
    padding: 0 12px;
    gap: 8px;
  }

  .nav-mobile-toggle {
    display: flex;
  }

  .logo {
    font-size: 21px;
    letter-spacing: -0.3px;
  }

  .logo-badge {
    font-size: 9px;
    padding: 1px 4px;
  }

  /* Hide crowded desktop elements */
  .nav-center,
  .nav-links,
  .nav-location,
  .nav-actions .btn-olx-sell {
    display: none !important;
  }

  /* Show mobile search trigger icon */
  .mobile-search-trigger {
    display: flex;
    width: 38px;
    height: 38px;
  }

  .mobile-search-drawer {
    display: block;
  }

  .nav-right {
    gap: 8px;
  }

  .nav-icon-btn {
    width: 36px;
    height: 36px;
    font-size: 15px;
  }

  .avatar {
    width: 34px;
    height: 34px;
    font-size: 13px;
  }
}
```

---

## 2. Feature 2B: Mobile Navigation Drawer (Slide-Out Off-Canvas Menu)

### 2.1 Component Blueprint
The mobile navigation drawer provides a single slide-out surface housing:
1. **Student Auth / Profile Banner**: Shows avatar, user name, university/student role, and city when authenticated; or friendly onboarding invite with Login/Sign Up buttons when guest.
2. **Post Quick CTAs**: High-visibility dual cards to post accommodation (PG/hostel/room) or list a marketplace product.
3. **Core Browsing Links**: Accommodations, Marketplace, Student Deals.
4. **Campus Hub Quick-Filter Pills**: Graphic Era, UPES, DIT, Roorkee, Rishikesh.
5. **Authenticated Student Space**: Dashboard, Bookings, Orders, Listings, Requests, Saved Wishlist, Chat.
6. **Drawer Footer**: Logout action & platform verification badge.

---

### 2.2 Complete Drawer HTML Structure (Add directly before `</body>` in public pages)

```html
<!-- Mobile Navigation Drawer & Backdrop -->
<div class="mobile-drawer-overlay" id="mobileDrawerOverlay" onclick="closeMobileDrawer()"></div>

<aside class="mobile-drawer" id="mobileDrawer" aria-label="Mobile Navigation">
  <!-- Drawer Header -->
  <div class="drawer-header">
    <div class="drawer-user-card" id="drawerUserCard">
      <!-- Injected by Auth.updateNavbar() -->
      <div class="drawer-user-avatar">👤</div>
      <div class="drawer-user-meta">
        <div class="drawer-user-name">Welcome, Student!</div>
        <div class="drawer-user-role">Dehradun & Uttarakhand Hub</div>
      </div>
    </div>
    <button class="drawer-close-btn" onclick="closeMobileDrawer()" aria-label="Close menu">✕</button>
  </div>

  <!-- Drawer Body (Scrollable) -->
  <div class="drawer-body">
    <!-- Quick Post CTAs -->
    <div class="drawer-post-cards">
      <a href="post-property.html" class="drawer-post-card card-property">
        <span class="post-card-icon">🏠</span>
        <div class="post-card-text">
          <strong>List a PG / Room</strong>
          <small>Zero Brokerage · Free</small>
        </div>
      </a>
      <a href="post-product.html" class="drawer-post-card card-product">
        <span class="post-card-icon">🏷️</span>
        <div class="post-card-text">
          <strong>Sell Pre-Loved Gear</strong>
          <small>Tech, Cycles, Books</small>
        </div>
      </a>
    </div>

    <!-- Core Public Exploration -->
    <div class="drawer-group-title">Browse Marketplace</div>
    <nav class="drawer-links">
      <a href="index.html" class="drawer-link"><span class="link-icon">🏠</span> Home</a>
      <a href="search-properties.html" class="drawer-link"><span class="link-icon">🛏️</span> Student Accommodations & PGs</a>
      <a href="search-products.html" class="drawer-link"><span class="link-icon">🛒</span> Student Buy & Sell Re-Commerce</a>
      <a href="search-properties.html?type=PG" class="drawer-link sub-link"><span>•</span> Paying Guest (PGs)</a>
      <a href="search-properties.html?type=FLAT" class="drawer-link sub-link"><span>•</span> Shared Rental Flats</a>
      <a href="search-products.html?category=Electronics" class="drawer-link sub-link"><span>•</span> Laptops & Computer Gear</a>
      <a href="search-products.html?category=Books" class="drawer-link sub-link"><span>•</span> Tech & GATE Textbooks</a>
    </nav>

    <!-- Campus Hub Filter Pills -->
    <div class="drawer-group-title">Campus Hubs</div>
    <div class="drawer-campus-grid">
      <a href="search-properties.html?q=Graphic+Era" class="drawer-campus-chip">🎓 Graphic Era (GEU)</a>
      <a href="search-properties.html?q=UPES" class="drawer-campus-chip">🎓 UPES Dehradun</a>
      <a href="search-properties.html?q=DIT" class="drawer-campus-chip">🎓 DIT University</a>
      <a href="search-properties.html?q=Roorkee" class="drawer-campus-chip">🏛️ IIT Roorkee</a>
      <a href="search-properties.html?city=Rishikesh" class="drawer-campus-chip">🏔️ Rishikesh</a>
    </div>

    <!-- Student Dashboard Links (Dynamic Auth Injected) -->
    <div id="drawerAccountSection" style="display:none">
      <div class="drawer-group-title">My Student Space</div>
      <nav class="drawer-links" id="drawerAccountLinks">
        <!-- Injected via Auth.updateNavbar() -->
      </nav>
    </div>
  </div>

  <!-- Drawer Footer -->
  <div class="drawer-footer" id="drawerFooter">
    <!-- Injected: Logout button or Login link -->
  </div>
</aside>
```

---

### 2.3 Mobile Drawer CSS (Add to `frontend/css/global.css`)

```css
/* ==========================================================================
   Mobile Navigation Drawer & Overlay
   ========================================================================== */
.mobile-drawer-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 47, 52, 0.65);
  backdrop-filter: blur(4px);
  z-index: 1200;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.28s cubic-bezier(0.4, 0, 0.2, 1);
}

.mobile-drawer-overlay.open {
  opacity: 1;
  pointer-events: auto;
}

.mobile-drawer {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  width: min(320px, 86vw);
  background: #ffffff;
  z-index: 1210;
  display: flex;
  flex-direction: column;
  transform: translateX(-100%);
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 10px 0 30px rgba(0, 47, 52, 0.25);
}

.mobile-drawer.open {
  transform: translateX(0);
}

/* Drawer Header */
.drawer-header {
  padding: 16px 18px;
  background: var(--header-bg);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-shrink: 0;
}

.drawer-user-card {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.drawer-user-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.15);
  border: 2px solid var(--amazon-amber);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 16px;
  overflow: hidden;
  flex-shrink: 0;
}

.drawer-user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.drawer-user-meta {
  min-width: 0;
}

.drawer-user-name {
  font-size: 15px;
  font-weight: 700;
  color: #ffffff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.drawer-user-role {
  font-size: 11px;
  color: var(--olx-cyan);
  font-weight: 600;
}

.drawer-close-btn {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: #ffffff;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: var(--transition);
  flex-shrink: 0;
}

.drawer-close-btn:hover {
  background: rgba(255, 255, 255, 0.22);
}

/* Drawer Body */
.drawer-body {
  flex: 1;
  overflow-y: auto;
  padding: 16px 14px;
  -webkit-overflow-scrolling: touch;
}

.drawer-post-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-bottom: 20px;
}

.drawer-post-card {
  background: #f8fafc;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 10px 12px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  text-decoration: none !important;
  color: var(--text-primary);
  transition: var(--transition);
}

.drawer-post-card.card-property {
  border-left: 3px solid #007185;
}

.drawer-post-card.card-product {
  border-left: 3px solid var(--amazon-amber);
}

.drawer-post-card:active {
  transform: scale(0.97);
  background: #f1f5f9;
}

.post-card-icon {
  font-size: 20px;
}

.post-card-text strong {
  display: block;
  font-size: 12px;
  line-height: 1.2;
}

.post-card-text small {
  font-size: 10px;
  color: var(--text-muted);
}

.drawer-group-title {
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-muted);
  margin: 18px 8px 8px;
}

.drawer-links {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.drawer-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  border-radius: var(--radius);
  text-decoration: none !important;
  transition: var(--transition);
}

.drawer-link:hover, .drawer-link:active {
  background: var(--olx-light-teal);
  color: var(--olx-teal);
}

.drawer-link.sub-link {
  padding-left: 36px;
  font-size: 13px;
  color: var(--text-secondary);
  font-weight: 500;
}

.drawer-campus-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  padding: 4px 6px 12px;
}

.drawer-campus-chip {
  font-size: 11px;
  font-weight: 600;
  background: #f1f5f9;
  border: 1px solid var(--border);
  color: var(--text-secondary);
  padding: 4px 10px;
  border-radius: var(--radius-full);
  text-decoration: none !important;
  transition: var(--transition);
}

.drawer-campus-chip:active {
  background: var(--olx-teal);
  color: #ffffff;
}

/* Drawer Footer */
.drawer-footer {
  padding: 14px 18px;
  border-top: 1px solid var(--border);
  background: #f8fafc;
  flex-shrink: 0;
}
```

---

## 3. Feature 2C: Mobile Bottom Navigation Bar (Sticky App Bar)

### 3.1 Ergonomics & Safe Area Architecture
On smartphones, users operate with one hand in the bottom thumb zone. A sticky bottom bar provides instant 1-tap switching between core tasks:
- **Tab 1: Explore** (`search-properties.html` — Accommodations, PGs, Hostels)
- **Tab 2: Marketplace** (`search-products.html` — Classifieds, Laptops, Books)
- **Center Button (+): Post** (Prominent raised button that opens the Post Chooser sheet)
- **Tab 4: Chats** (`pages/user/chat.html` — In-app student chat with unread indicator)
- **Tab 5: Account** (`pages/user/dashboard.html` or `login.html`)

---

### 3.2 Mobile Bottom Navigation HTML

```html
<!-- Mobile Sticky Bottom Navigation Bar (App Bar) -->
<nav class="mobile-bottom-nav" id="mobileBottomNav" aria-label="Mobile Navigation">
  <!-- Tab 1: Explore Properties -->
  <a href="search-properties.html" class="bottom-nav-item" data-tab="properties">
    <span class="nav-icon">🏠</span>
    <span class="nav-label">Explore</span>
  </a>

  <!-- Tab 2: Buy & Sell Marketplace -->
  <a href="search-products.html" class="bottom-nav-item" data-tab="products">
    <span class="nav-icon">🛒</span>
    <span class="nav-label">Market</span>
  </a>

  <!-- Center Floating Action Button: Post Listing -->
  <div class="bottom-nav-post-wrap">
    <button class="bottom-nav-post-btn" onclick="openPostChooser(event)" aria-label="Post a listing">
      <span class="post-plus">+</span>
    </button>
    <span class="nav-label">Post</span>
  </div>

  <!-- Tab 4: Messages / Chat -->
  <a href="pages/user/chat.html" class="bottom-nav-item" data-tab="chat" id="bottomTabChat">
    <span class="nav-icon">
      💬
      <span class="nav-badge-dot" id="chatUnreadDot" style="display:none"></span>
    </span>
    <span class="nav-label">Chats</span>
  </a>

  <!-- Tab 5: Account / Dashboard -->
  <a href="pages/user/dashboard.html" class="bottom-nav-item" data-tab="account" id="bottomTabAccount">
    <span class="nav-icon">👤</span>
    <span class="nav-label">Account</span>
  </a>
</nav>

<!-- Post Chooser Modal Sheet (Triggers on center + tap) -->
<div class="post-chooser-overlay" id="postChooserOverlay" onclick="closePostChooser(event)">
  <div class="post-chooser-sheet" onclick="event.stopPropagation()">
    <div class="sheet-drag-handle"></div>
    <div class="sheet-title">What would you like to list?</div>
    <p class="sheet-desc">Reach 8,000+ local students across Dehradun, Rishikesh & Roorkee</p>
    
    <div class="chooser-card-list">
      <a href="post-property.html" class="chooser-card-item">
        <div class="chooser-icon-box" style="background:#e0f2fe;color:#0284c7">🏠</div>
        <div class="chooser-text">
          <div class="chooser-head">List an Accommodation</div>
          <div class="chooser-info">Post a PG room, student hostel, shared flat, or 1 BHK</div>
        </div>
        <span class="chooser-chevron">›</span>
      </a>

      <a href="post-product.html" class="chooser-card-item">
        <div class="chooser-icon-box" style="background:#fef3c7;color:#d97706">📦</div>
        <div class="chooser-text">
          <div class="chooser-head">Sell or Rent a Product</div>
          <div class="chooser-info">Laptops, study tables, bicycles, books, electronics</div>
        </div>
        <span class="chooser-chevron">›</span>
      </a>
    </div>

    <button type="button" class="btn btn-secondary btn-block mt-8" onclick="closePostChooser()">Cancel</button>
  </div>
</div>
```

---

### 3.3 Bottom Navigation CSS (Add to `frontend/css/global.css`)

```css
/* ==========================================================================
   Mobile Bottom Navigation Bar
   ========================================================================== */
.mobile-bottom-nav {
  display: none; /* Hidden on desktop */
}

@media (max-width: 768px) {
  body {
    padding-bottom: calc(62px + env(safe-area-inset-bottom, 0px)) !important;
  }

  .mobile-bottom-nav {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    align-items: center;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    height: 58px;
    background: rgba(255, 255, 255, 0.98);
    backdrop-filter: blur(12px);
    border-top: 1px solid var(--border);
    box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.08);
    z-index: 1000;
    padding-bottom: env(safe-area-inset-bottom, 0px);
  }

  .bottom-nav-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-decoration: none !important;
    color: #64748b;
    gap: 2px;
    height: 100%;
    transition: var(--transition);
  }

  .bottom-nav-item:active {
    transform: scale(0.92);
  }

  .bottom-nav-item.active {
    color: var(--olx-teal);
    font-weight: 700;
  }

  .bottom-nav-item .nav-icon {
    font-size: 19px;
    line-height: 1;
    position: relative;
    display: inline-block;
  }

  .bottom-nav-item .nav-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: -0.2px;
  }

  /* Center Floating Action Button */
  .bottom-nav-post-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-top: -14px;
    gap: 2px;
  }

  .bottom-nav-post-btn {
    width: 46px;
    height: 46px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--amazon-amber), #ffb834);
    color: #0f1111;
    border: 3px solid #ffffff;
    box-shadow: 0 4px 12px rgba(255, 153, 0, 0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: transform 0.15s ease;
    padding: 0;
  }

  .bottom-nav-post-btn:active {
    transform: scale(0.9);
  }

  .bottom-nav-post-btn .post-plus {
    font-size: 24px;
    font-weight: 900;
    line-height: 1;
  }

  .bottom-nav-post-wrap .nav-label {
    font-size: 10px;
    font-weight: 700;
    color: var(--text-primary);
  }

  .nav-badge-dot {
    position: absolute;
    top: -2px;
    right: -4px;
    width: 8px;
    height: 8px;
    background: var(--danger);
    border-radius: 50%;
    border: 1.5px solid #ffffff;
  }

  /* Post Chooser Bottom Sheet */
  .post-chooser-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 47, 52, 0.65);
    backdrop-filter: blur(4px);
    z-index: 1250;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.25s ease;
    display: flex;
    align-items: flex-end;
  }

  .post-chooser-overlay.open {
    opacity: 1;
    pointer-events: auto;
  }

  .post-chooser-sheet {
    width: 100%;
    background: #ffffff;
    border-radius: 20px 20px 0 0;
    padding: 14px 20px 24px;
    transform: translateY(100%);
    transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    box-shadow: 0 -10px 25px rgba(0, 47, 52, 0.2);
  }

  .post-chooser-overlay.open .post-chooser-sheet {
    transform: translateY(0);
  }

  .sheet-drag-handle {
    width: 38px;
    height: 4px;
    background: #cbd5e1;
    border-radius: 2px;
    margin: 0 auto 14px;
  }

  .sheet-title {
    font-size: 18px;
    font-weight: 800;
    color: var(--text-primary);
    text-align: center;
  }

  .sheet-desc {
    font-size: 13px;
    color: var(--text-secondary);
    text-align: center;
    margin-bottom: 18px;
  }

  .chooser-card-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 16px;
  }

  .chooser-card-item {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 12px 14px;
    background: #f8fafc;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    text-decoration: none !important;
    color: var(--text-primary);
    transition: var(--transition);
  }

  .chooser-card-item:active {
    background: #f1f5f9;
  }

  .chooser-icon-box {
    width: 44px;
    height: 44px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    flex-shrink: 0;
  }

  .chooser-text {
    flex: 1;
    min-width: 0;
  }

  .chooser-head {
    font-weight: 700;
    font-size: 14px;
  }

  .chooser-info {
    font-size: 12px;
    color: var(--text-secondary);
  }

  .chooser-chevron {
    font-size: 20px;
    color: var(--text-muted);
  }
}
```

---

## 4. Feature 3: Mobile Filter Drawer / Bottom Sheet on Search Pages

### 4.1 Diagnosis of Current Defect
In `frontend/search-properties.html` and `frontend/search-products.html`:
```html
<!-- Line 86 in search-properties.html and search-products.html -->
<div class="detail-layout" style="grid-template-columns:260px 1fr;gap:24px;align-items:start">
```
- **Why it breaks**:
  1. The inline `style="grid-template-columns:260px 1fr"` overrides the media query `.detail-layout { grid-template-columns: 1fr; }` in `global.css`.
  2. On 375px mobile, `260px + 24px + 1fr` forces horizontal page scrollbar (~550px total width).
  3. When forced to 1 column, the filter sidebar with 25+ checkboxes and inputs takes up 1,200px of vertical space before showing any listing cards.

---

### 4.2 Architectural Solution

1. **HTML Modification**:
   Replace line 86 with clean class `.search-layout` (remove inline style attribute completely):
   ```html
   <div class="search-layout">
   ```
2. **Add Mobile Filter Trigger Button in `results-topbar`**:
   ```html
   <div class="results-topbar">
     <div class="results-count" id="resultsCount">Loading verified listings…</div>
     <div class="results-controls">
       <!-- Mobile Filter Drawer Trigger -->
       <button class="btn-filter-trigger" id="mobileFilterBtn" onclick="openFilterDrawer()">
         <span class="filter-icon">⚡</span> Filters
         <span class="filter-badge" id="filterCountBadge" style="display:none">0</span>
       </button>

       <label for="sortSelect" class="sort-label">Sort:</label>
       <select id="sortSelect" class="btn btn-secondary sort-select" onchange="applySearch()">
         <option value="newest">Featured</option>
         <option value="price-asc">Price: Low to High</option>
         <option value="price-desc">Price: High to Low</option>
       </select>
     </div>
   </div>
   ```
3. **Filter Sidebar Responsive Modal Container**:
   Wrap the existing `<aside class="filter-sidebar">` so it has a mobile drawer header, scrollable body, and sticky action footer:
   ```html
   <!-- Mobile Filter Backdrop -->
   <div class="filter-drawer-overlay" id="filterDrawerOverlay" onclick="closeFilterDrawer()"></div>

   <aside class="filter-sidebar" id="filterSidebar">
     <!-- Mobile Drawer Header -->
     <div class="filter-drawer-header">
       <div class="filter-drawer-title">⚡ Refine & Filter</div>
       <button type="button" class="filter-drawer-close" onclick="closeFilterDrawer()" aria-label="Close filters">✕</button>
     </div>

     <!-- Scrollable Filter Content -->
     <div class="filter-drawer-body">
       <!-- Existing property or product filter groups remain untouched here -->
     </div>

     <!-- Mobile Drawer Sticky Action Footer -->
     <div class="filter-drawer-footer">
       <button type="button" class="btn btn-secondary btn-reset-filters" onclick="resetFilters()">Reset All</button>
       <button type="button" class="btn btn-primary btn-apply-filters" onclick="applyAndCloseFilters()">Show Results</button>
     </div>
   </aside>
   ```

---

### 4.3 Filter Drawer CSS (Add to `frontend/css/global.css`)

```css
/* ==========================================================================
   Responsive Search Layout & Mobile Filter Drawer
   ========================================================================== */
.search-layout {
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: 24px;
  align-items: start;
}

.filter-drawer-overlay,
.filter-drawer-header,
.filter-drawer-footer,
.btn-filter-trigger {
  display: none;
}

/* On Desktop: filter sidebar styling */
.filter-sidebar {
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 18px;
  box-shadow: var(--shadow-sm);
  position: sticky;
  top: 80px;
}

/* ==========================================================================
   Mobile/Tablet Filter Bottom Sheet (< 1024px)
   ========================================================================== */
@media (max-width: 1023px) {
  .search-layout {
    display: block;
  }

  .btn-filter-trigger {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--olx-light-teal);
    color: var(--olx-teal);
    border: 1.5px solid var(--olx-teal);
    border-radius: var(--radius);
    padding: 6px 12px;
    font-size: 13px;
    font-weight: 700;
    cursor: pointer;
    transition: var(--transition);
  }

  .btn-filter-trigger:active {
    background: var(--olx-teal);
    color: #ffffff;
  }

  .filter-badge {
    background: var(--amazon-amber);
    color: #0f1111;
    font-size: 10px;
    font-weight: 800;
    padding: 1px 6px;
    border-radius: var(--radius-full);
  }

  .results-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    flex-wrap: wrap;
    padding: 10px 14px;
  }

  .results-controls {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .sort-label {
    display: none;
  }

  /* Filter Backdrop */
  .filter-drawer-overlay {
    display: block;
    position: fixed;
    inset: 0;
    background: rgba(0, 47, 52, 0.65);
    backdrop-filter: blur(4px);
    z-index: 1250;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.25s ease;
  }

  .filter-drawer-overlay.open {
    opacity: 1;
    pointer-events: auto;
  }

  /* Transform Sidebar into Bottom Sheet */
  .filter-sidebar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    top: auto;
    max-height: 82vh;
    background: #ffffff;
    border-radius: 18px 18px 0 0;
    border: none;
    box-shadow: 0 -10px 30px rgba(0, 47, 52, 0.25);
    z-index: 1260;
    display: flex;
    flex-direction: column;
    padding: 0;
    transform: translateY(100%);
    transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  }

  .filter-sidebar.open {
    transform: translateY(0);
  }

  .filter-drawer-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 20px;
    border-bottom: 1px solid var(--border);
    flex-shrink: 0;
  }

  .filter-drawer-title {
    font-size: 16px;
    font-weight: 800;
    color: var(--text-primary);
  }

  .filter-drawer-close {
    background: #f1f5f9;
    border: none;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    font-size: 15px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .filter-drawer-body {
    flex: 1;
    overflow-y: auto;
    padding: 14px 20px;
    -webkit-overflow-scrolling: touch;
  }

  .filter-drawer-footer {
    display: flex;
    gap: 12px;
    padding: 12px 20px;
    border-top: 1px solid var(--border);
    background: #ffffff;
    flex-shrink: 0;
    padding-bottom: calc(12px + env(safe-area-inset-bottom, 0px));
  }

  .btn-reset-filters {
    flex: 1;
    padding: 10px;
    font-size: 13px;
  }

  .btn-apply-filters {
    flex: 2;
    padding: 10px;
    font-size: 14px;
    font-weight: 800;
  }
}
```

---

## 5. Feature 4: Sticky Bottom CTA Bar on Detail Pages (`property-detail.html` & `product-detail.html`)

### 5.1 Diagnosis of Current Defect
In `property-detail.js` and `product-detail.js`, the booking and order controls are placed inside:
```html
<aside class="sidebar-sticky">
  <div class="action-card">...</div>
</aside>
```
On mobile screens (`< 768px`), `.detail-layout` stacks into a single column. The sidebar falls to the bottom of the document:
1. Gallery & Badges
2. Info Cards (Deposit, Room counts, Preferred gender)
3. Facilities Grid (WiFi, Meals, Geyser)
4. Description & Address
5. **Full Student Reviews List** (Average 800px - 1,400px of vertical height)
6. Similar Listings Grid
7. Finally, `<aside class="sidebar-sticky">` at the very bottom!

A mobile student wanting to book a room or contact a seller must scroll through 1,500px of reviews just to reach the action button!

---

### 5.2 Architectural Solution: Floating Mobile Action Bar + Instant Booking Sheet

1. **Fixed Floating Action Bar**:
   Rendered at the bottom of the viewport on screens `< 768px`:
   - Left side: High-contrast price (`₹6,500/mo` or `₹24,500`) + availability badge (`● Available`).
   - Right side: Quick "💬 Chat" icon + prominent primary action button (`Book Now` or `Buy Now`).
2. **Instant Booking Sheet**:
   Tapping "Book Now" on mobile slides up a lightweight bottom sheet containing the room selector, month selector, total calculation, and "Confirm Booking" button, without requiring the user to scroll to the bottom.

---

### 5.3 Detail Page Sticky CTA HTML Blueprint

```html
<!-- Mobile Floating Action Bar (Visible only on < 768px) -->
<div class="mobile-detail-cta-bar" id="mobileDetailCtaBar">
  <div class="cta-price-group">
    <div class="cta-price-val" id="mobileCtaPrice">₹ —</div>
    <div class="cta-status-badge" id="mobileCtaBadge">● Available</div>
  </div>

  <div class="cta-btn-group">
    <button type="button" class="cta-icon-action" id="mobileCtaChatBtn" onclick="contactOwner()" title="Chat with owner">
      💬
    </button>
    <button type="button" class="btn btn-primary cta-primary-btn" id="mobileCtaPrimaryBtn" onclick="openMobileBookingSheet()">
      Book Now
    </button>
  </div>
</div>

<!-- Mobile Quick Booking Sheet (Opens when Book Now is tapped on mobile) -->
<div class="booking-sheet-overlay" id="bookingSheetOverlay" onclick="closeMobileBookingSheet()">
  <div class="booking-sheet" onclick="event.stopPropagation()">
    <div class="sheet-drag-handle"></div>
    <div class="booking-sheet-header">
      <div class="sheet-title" id="bookingSheetTitle">Book Accommodation</div>
      <button type="button" class="sheet-close" onclick="closeMobileBookingSheet()">✕</button>
    </div>

    <div class="booking-sheet-body" id="bookingSheetBody">
      <!-- Mirror of the room selector and duration inputs for mobile -->
      <div class="input-group">
        <label for="mobileRoomSelect">Select Room</label>
        <select id="mobileRoomSelect" onchange="syncBookingRoom(this.value)">
          <option value="">Any available room</option>
        </select>
      </div>

      <div class="input-group">
        <label for="mobileMonthsSelect">Stay Duration (Months)</label>
        <select id="mobileMonthsSelect" onchange="syncBookingMonths(this.value)">
          <option value="1">1 month</option>
          <option value="2">2 months</option>
          <option value="3">3 months</option>
          <option value="4">4 months</option>
          <option value="6" selected>6 months (Semester)</option>
          <option value="8">8 months</option>
          <option value="9">9 months (Academic Year)</option>
          <option value="12">12 months</option>
        </select>
      </div>

      <div class="input-group">
        <label for="mobileBookingMessage">Message to Owner (Optional)</label>
        <textarea id="mobileBookingMessage" rows="2" placeholder="e.g. 2nd year GEU student, moving in next week" maxlength="300"></textarea>
      </div>

      <div class="total-display">
        <span class="total-label">Total Estimated Rent</span>
        <span class="total-value" id="mobileTotalRent">₹ —</span>
      </div>

      <button type="button" class="btn btn-primary btn-block btn-lg" onclick="executeMobileBooking()">
        Confirm Booking Request
      </button>

      <p class="sheet-safety-note">🛡️ Zero broker fee. Payments are made directly to the owner after room inspection.</p>
    </div>
  </div>
</div>
```

---

### 5.4 Sticky CTA CSS (Add to `frontend/css/global.css`)

```css
/* ==========================================================================
   Mobile Sticky Action Bar & Booking Sheet on Detail Pages
   ========================================================================== */
.mobile-detail-cta-bar,
.booking-sheet-overlay {
  display: none;
}

@media (max-width: 768px) {
  /* Prevent content hiding behind the sticky bar */
  body.detail-page {
    padding-bottom: calc(76px + env(safe-area-inset-bottom, 0px)) !important;
  }

  .mobile-detail-cta-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    height: 68px;
    background: rgba(255, 255, 255, 0.98);
    backdrop-filter: blur(12px);
    border-top: 1px solid var(--border);
    box-shadow: 0 -4px 18px rgba(0, 47, 52, 0.12);
    z-index: 1050;
    padding: 0 16px;
    padding-bottom: env(safe-area-inset-bottom, 0px);
  }

  .cta-price-group {
    display: flex;
    flex-direction: column;
    min-width: 0;
  }

  .cta-price-val {
    font-size: 19px;
    font-weight: 900;
    color: var(--text-primary);
    line-height: 1.1;
  }

  .cta-status-badge {
    font-size: 11px;
    font-weight: 700;
    color: var(--success);
    margin-top: 2px;
  }

  .cta-btn-group {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .cta-icon-action {
    width: 44px;
    height: 44px;
    border-radius: var(--radius);
    background: #f1f5f9;
    border: 1px solid var(--border);
    font-size: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: var(--transition);
  }

  .cta-icon-action:active {
    background: #e2e8f0;
    transform: scale(0.95);
  }

  .cta-primary-btn {
    padding: 11px 22px;
    font-size: 15px;
    font-weight: 800;
    border-radius: var(--radius);
    box-shadow: 0 2px 8px rgba(255, 153, 0, 0.3);
  }

  .cta-primary-btn:active {
    transform: scale(0.96);
  }

  /* Booking Sheet Overlay */
  .booking-sheet-overlay {
    display: flex;
    align-items: flex-end;
    position: fixed;
    inset: 0;
    background: rgba(0, 47, 52, 0.65);
    backdrop-filter: blur(4px);
    z-index: 1300;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.25s ease;
  }

  .booking-sheet-overlay.open {
    opacity: 1;
    pointer-events: auto;
  }

  .booking-sheet {
    width: 100%;
    max-height: 85vh;
    background: #ffffff;
    border-radius: 20px 20px 0 0;
    padding: 14px 20px 24px;
    transform: translateY(100%);
    transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    display: flex;
    flex-direction: column;
    box-shadow: 0 -10px 30px rgba(0, 47, 52, 0.25);
  }

  .booking-sheet-overlay.open .booking-sheet {
    transform: translateY(0);
  }

  .booking-sheet-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 14px;
  }

  .sheet-close {
    background: #f1f5f9;
    border: none;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    font-size: 15px;
    cursor: pointer;
  }

  .booking-sheet-body {
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
  }

  .sheet-safety-note {
    font-size: 11px;
    color: var(--text-muted);
    text-align: center;
    margin-top: 12px;
    line-height: 1.4;
  }
}
```

---

## 6. Lightweight JavaScript Handlers & Integration Blueprint

### 6.1 Centralized Navigation Manager (`frontend/js/navigation.js`)
Create a zero-dependency module `frontend/js/navigation.js` loaded on all pages:

```javascript
/**
 * StayMart Mobile Navigation & Interactive Drawer Handlers
 */

// Drawer Controls
function openMobileDrawer() {
  const drawer = document.getElementById('mobileDrawer');
  const overlay = document.getElementById('mobileDrawerOverlay');
  if (drawer && overlay) {
    drawer.classList.add('open');
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
}

function closeMobileDrawer() {
  const drawer = document.getElementById('mobileDrawer');
  const overlay = document.getElementById('mobileDrawerOverlay');
  if (drawer && overlay) {
    drawer.classList.remove('open');
    overlay.classList.remove('open');
    document.body.style.overflow = '';
  }
}

// Mobile Expandable Search
function toggleMobileSearch() {
  const drawer = document.getElementById('mobileSearchDrawer');
  const input = document.getElementById('mobileSearchInput');
  if (!drawer) return;
  const isOpen = drawer.classList.toggle('open');
  if (isOpen && input) {
    setTimeout(() => input.focus(), 150);
  }
}

function clearMobileSearch() {
  const input = document.getElementById('mobileSearchInput');
  const clearBtn = document.getElementById('mobileSearchClear');
  if (input) {
    input.value = '';
    input.focus();
  }
  if (clearBtn) clearBtn.style.display = 'none';
}

// Post Chooser Modal
function openPostChooser(event) {
  if (event) event.preventDefault();
  const overlay = document.getElementById('postChooserOverlay');
  if (overlay) {
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
}

function closePostChooser(event) {
  const overlay = document.getElementById('postChooserOverlay');
  if (overlay) {
    overlay.classList.remove('open');
    document.body.style.overflow = '';
  }
}

// Mobile Filter Drawer (Search Pages)
function openFilterDrawer() {
  const sidebar = document.getElementById('filterSidebar');
  const overlay = document.getElementById('filterDrawerOverlay');
  if (sidebar && overlay) {
    sidebar.classList.add('open');
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
}

function closeFilterDrawer() {
  const sidebar = document.getElementById('filterSidebar');
  const overlay = document.getElementById('filterDrawerOverlay');
  if (sidebar && overlay) {
    sidebar.classList.remove('open');
    overlay.classList.remove('open');
    document.body.style.overflow = '';
  }
}

function applyAndCloseFilters() {
  if (typeof applySearch === 'function') {
    applySearch();
  }
  closeFilterDrawer();
}

// Mobile Booking Bottom Sheet (Detail Pages)
function openMobileBookingSheet() {
  const overlay = document.getElementById('bookingSheetOverlay');
  if (overlay) {
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
}

function closeMobileBookingSheet() {
  const overlay = document.getElementById('bookingSheetOverlay');
  if (overlay) {
    overlay.classList.remove('open');
    document.body.style.overflow = '';
  }
}

// Active Bottom Navigation Highlight
function updateBottomNavActive() {
  const currentPath = window.location.pathname.toLowerCase();
  const items = document.querySelectorAll('.bottom-nav-item');
  items.forEach(item => {
    const tab = item.dataset.tab;
    let isActive = false;
    if (tab === 'properties' && (currentPath.includes('search-properties') || currentPath.includes('property-detail'))) {
      isActive = true;
    } else if (tab === 'products' && (currentPath.includes('search-products') || currentPath.includes('product-detail'))) {
      isActive = true;
    } else if (tab === 'chat' && currentPath.includes('chat.html')) {
      isActive = true;
    } else if (tab === 'account' && (currentPath.includes('dashboard') || currentPath.includes('profile') || currentPath.includes('bookings') || currentPath.includes('orders'))) {
      isActive = true;
    }
    if (isActive) item.classList.add('active');
    else item.classList.remove('active');
  });
}

// Escape key listener for all drawers and overlays
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeMobileDrawer();
    closePostChooser();
    closeFilterDrawer();
    closeMobileBookingSheet();
  }
});

// Initialize on DOM Ready
document.addEventListener('DOMContentLoaded', () => {
  updateBottomNavActive();
  
  // Real-time clear button visibility on mobile search
  const mobileInput = document.getElementById('mobileSearchInput');
  const clearBtn = document.getElementById('mobileSearchClear');
  if (mobileInput && clearBtn) {
    mobileInput.addEventListener('input', () => {
      clearBtn.style.display = mobileInput.value.length ? 'block' : 'none';
    });
  }
});
```

---

### 6.2 Updating `Auth.updateNavbar()` in `frontend/js/auth.js`
When `Auth.updateNavbar()` executes, it should populate both the desktop `.nav-actions` and the new `#drawerUserCard`, `#drawerAccountSection`, and `#drawerFooter`.

#### Before / After in `frontend/js/auth.js`:
```javascript
// Extend Auth.updateNavbar() to sync with mobile drawer and bottom nav:
updateNavbar() {
  const navActions = document.querySelector('.navbar .nav-actions');
  const drawerUserCard = document.getElementById('drawerUserCard');
  const drawerAccountSection = document.getElementById('drawerAccountSection');
  const drawerAccountLinks = document.getElementById('drawerAccountLinks');
  const drawerFooter = document.getElementById('drawerFooter');
  const prefix = depthPrefix();

  if (this.isLoggedIn() && this.user) {
    const user = this.user;
    
    // 1. Desktop Nav Actions
    if (navActions) {
      navActions.innerHTML = `
        <a href="${prefix}pages/user/chat.html" class="nav-icon-btn" title="Messages">💬</a>
        <a href="${prefix}pages/user/wishlist.html" class="nav-icon-btn" title="Saved Wishlist">❤️</a>
        <div class="avatar-menu">
          <div class="avatar" onclick="toggleDropdown(event)">
            ${user.profilePic ? `<img src="${user.profilePic}" alt=""/>` : (user.name ? user.name[0].toUpperCase() : 'U')}
          </div>
          <div class="dropdown" id="profileDropdown">
            <div class="dropdown-header">
              <div class="dropdown-name">${escapeHtml(user.name || 'User')}</div>
              <div class="dropdown-mail">${escapeHtml(user.email || '')}</div>
            </div>
            <a href="${prefix}pages/user/dashboard.html"><span>📊</span> Dashboard</a>
            <a href="${prefix}pages/user/profile.html"><span>👤</span> My Profile</a>
            <a href="${prefix}pages/user/my-listings.html"><span>🏠</span> My Listings</a>
            <a href="${prefix}pages/user/bookings.html"><span>📅</span> My Bookings</a>
            <a href="${prefix}pages/user/orders.html"><span>📦</span> My Orders</a>
            <a href="${prefix}pages/user/requests-received.html"><span>📨</span> Requests</a>
            <a href="${prefix}pages/user/wishlist.html"><span>❤️</span> Wishlist</a>
            <a href="${prefix}pages/user/chat.html"><span>💬</span> Messages</a>
            ${this.isAdmin() ? '<div class="dropdown-divider"></div><a href="' + prefix + 'pages/admin/dashboard.html"><span>🛡️</span> Admin Dashboard</a>' : ''}
            <div class="dropdown-divider"></div>
            <button onclick="handleLogout()"><span>🚪</span> Logout</button>
          </div>
        </div>
        <a href="${prefix}post-product.html" class="btn-olx-sell">
          <span class="sell-plus">+</span> SELL
        </a>
      `;
    }

    // 2. Mobile Drawer User Card
    if (drawerUserCard) {
      drawerUserCard.innerHTML = `
        <div class="drawer-user-avatar">
          ${user.profilePic ? `<img src="${user.profilePic}" alt=""/>` : (user.name ? user.name[0].toUpperCase() : 'U')}
        </div>
        <div class="drawer-user-meta">
          <div class="drawer-user-name">${escapeHtml(user.name || 'User')}</div>
          <div class="drawer-user-role">🎓 Verified Student · ${escapeHtml(user.city || 'Dehradun')}</div>
        </div>
      `;
    }

    // 3. Mobile Drawer Account Links
    if (drawerAccountSection && drawerAccountLinks) {
      drawerAccountSection.style.display = 'block';
      drawerAccountLinks.innerHTML = `
        <a href="${prefix}pages/user/dashboard.html" class="drawer-link"><span class="link-icon">📊</span> My Dashboard</a>
        <a href="${prefix}pages/user/bookings.html" class="drawer-link"><span class="link-icon">📅</span> My Bookings</a>
        <a href="${prefix}pages/user/orders.html" class="drawer-link"><span class="link-icon">📦</span> My Orders</a>
        <a href="${prefix}pages/user/my-listings.html" class="drawer-link"><span class="link-icon">🏷️</span> My Listings</a>
        <a href="${prefix}pages/user/requests-received.html" class="drawer-link"><span class="link-icon">📨</span> Incoming Requests</a>
        <a href="${prefix}pages/user/wishlist.html" class="drawer-link"><span class="link-icon">❤️</span> Saved Wishlist</a>
        <a href="${prefix}pages/user/chat.html" class="drawer-link"><span class="link-icon">💬</span> Direct Messages</a>
        <a href="${prefix}pages/user/profile.html" class="drawer-link"><span class="link-icon">⚙️</span> Profile & Settings</a>
        ${this.isAdmin() ? `<a href="${prefix}pages/admin/dashboard.html" class="drawer-link"><span class="link-icon">🛡️</span> Admin Console</a>` : ''}
      `;
    }

    // 4. Mobile Drawer Footer
    if (drawerFooter) {
      drawerFooter.innerHTML = `
        <button class="btn btn-secondary btn-block" onclick="handleLogout()" style="color:var(--danger)">
          <span>🚪</span> Log Out
        </button>
      `;
    }

  } else {
    // Logged Out (Guest State)
    if (navActions) {
      navActions.innerHTML = `
        <a href="${prefix}login.html" class="nav-login-link">Login</a>
        <a href="${prefix}login.html" class="btn-olx-sell">
          <span class="sell-plus">+</span> SELL
        </a>
      `;
    }

    if (drawerUserCard) {
      drawerUserCard.innerHTML = `
        <div class="drawer-user-avatar">👤</div>
        <div class="drawer-user-meta">
          <div class="drawer-user-name">Welcome, Student!</div>
          <div class="drawer-user-role">Zero Brokerage Uttarakhand Hub</div>
        </div>
      `;
    }

    if (drawerAccountSection) {
      drawerAccountSection.style.display = 'none';
    }

    if (drawerFooter) {
      drawerFooter.innerHTML = `
        <div style="display:flex;gap:10px;">
          <a href="${prefix}login.html" class="btn btn-primary" style="flex:1">Log In</a>
          <a href="${prefix}register.html" class="btn btn-secondary" style="flex:1">Sign Up</a>
        </div>
      `;
    }
  }
}
```

---

## 7. Concrete File Modification Inventory

The table below catalogs every file requiring modifications, the exact lines affected, and the rationale:

| File Path | Lines Affected | Nature of Modification |
|---|---|---|
| `frontend/css/global.css` | 108–132, 1283–1290 + new sections | Add 375px overflow-proof navbar styles, mobile drawer, bottom nav, filter sheet, and sticky CTA rules. |
| `frontend/js/navigation.js` | New file (120 lines) | Global event listeners for drawer, bottom sheet, search toggle, and active tab states. |
| `frontend/js/auth.js` | 50–93 (`updateNavbar`) | Synchronize user state with mobile drawer header, account links, and bottom nav. |
| `frontend/index.html` | 11–64 (Navbar) & before `</body>` | Upgrade navbar markup; embed mobile drawer and bottom navigation components. |
| `frontend/search-properties.html` | 11–32 (Nav), 86 (Grid fix), 128 (Filter wrap) | Remove inline `grid-template-columns:260px 1fr`, attach mobile filter sheet and bottom nav. |
| `frontend/search-products.html` | 11–32 (Nav), 86 (Grid fix), 122 (Filter wrap) | Remove inline `grid-template-columns:260px 1fr`, attach mobile filter sheet and bottom nav. |
| `frontend/property-detail.html` | 11–31 (Nav), 53 (Detail root), bottom | Include mobile drawer, bottom nav, and sticky action bar markup. |
| `frontend/product-detail.html` | 11–30 (Nav), 52 (Detail root), bottom | Include mobile drawer, bottom nav, and sticky action bar markup. |
| `frontend/post-property.html` | 11–24 (Navbar), bottom | Standardize navbar markup; embed mobile drawer and bottom navigation. |
| `frontend/post-product.html` | 11–24 (Navbar), bottom | Standardize navbar markup; embed mobile drawer and bottom navigation. |
| `frontend/js/property-detail.js` | 48–160 (`renderDetail`) | Populate `#mobileCtaPrice`, `#mobileCtaBadge`, and wire mobile booking sheet. Correct line 224 redirect to `bookings.html`. |
| `frontend/js/product-detail.js` | 48–166 (`renderDetail`) | Populate `#mobileCtaPrice`, wire mobile order button. Correct line 234 redirect to `orders.html`. |

---

## 8. Verification & Acceptance Testing Protocol

To independently verify the implementation, execute the following verification steps:

### 8.1 Automated Viewport Overflow Verification
Execute automated headless Chrome checks across standard viewports (375px, 768px, 1280px):
```javascript
// Test logic for zero horizontal overflow:
const isOverflowing = await page.evaluate(() => {
  return document.documentElement.scrollWidth > document.documentElement.clientWidth;
});
expect(isOverflowing).toBe(false);
```

### 8.2 Functional Mobile Interaction Checks (375px Viewport)
1. **Navbar Overflow Test**: Load `index.html` at 375px × 667px. Verify that navbar height is <= 60px, `.nav-mobile-toggle` is visible, and no horizontal scrollbar exists.
2. **Drawer Toggle Test**: Click `#mobileMenuToggle`. Verify `#mobileDrawer` slides into view (`transform: translateX(0)`), `#mobileDrawerOverlay` becomes opaque, and body scroll is locked. Click overlay or ✕ button; verify drawer closes and scroll restores.
3. **Search Drawer Test**: Click `#mobileSearchTrigger` (🔍). Verify `#mobileSearchDrawer` expands with input focused. Type "Graphic Era" and submit; verify redirection to `search-properties.html?q=Graphic%20Era`.
4. **Bottom Nav Test**: Verify bottom navigation is fixed at viewport bottom. Verify active tab styling reflects current route. Tap (+) button; verify `#postChooserOverlay` opens with accommodation and product options.
5. **Search Filter Drawer Test**: Load `search-properties.html` at 375px. Verify results grid renders immediately without 25+ filters above it. Tap `⚡ Filters & Sort`; verify filter sheet slides up from bottom. Select "PG" and tap "Show Results"; verify drawer closes and filtered results update.
6. **Sticky Action Bar Test**: Load `property-detail.html?id=1` at 375px. Verify floating bottom action bar displays rent (e.g. `₹6,500/mo`) and "Book Now" button immediately upon load. Tap "Book Now"; verify booking bottom sheet opens without scrolling through reviews.
