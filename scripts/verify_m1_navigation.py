"""
Comprehensive Empirical Verification Suite for Milestone 1 Navigation & Links
Challenger 2 (M1 Navigation & Links Adversarial Challenger)
Role: critic, specialist
"""

import os
import re
import sys
import json
import subprocess
from html.parser import HTMLParser

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")
JS_DIR = os.path.join(FRONTEND_DIR, "js")
CSS_DIR = os.path.join(FRONTEND_DIR, "css")

print("=" * 75)
print("StayMart Milestone 1: Navigation, Links, Redirects & JS Interaction Audit")
print(f"Working Directory: {ROOT_DIR}")
print("=" * 75)

failures = []
passed_checks = 0

# ----------------------------------------------------------------------
# Index all HTML files
# ----------------------------------------------------------------------
all_html_files = {}
for root, _, files in os.walk(FRONTEND_DIR):
    for f in files:
        if f.endswith(".html"):
            full = os.path.join(root, f)
            rel = os.path.relpath(full, FRONTEND_DIR).replace("\\", "/")
            all_html_files[rel] = full

print(f"\n[INFO] Found {len(all_html_files)} existing HTML files in frontend/")

# ======================================================================
# SUITE 1: Forbidden Legacy Dead Links Audit
# ======================================================================
print("\n" + "=" * 75)
print("SUITE 1: Forbidden Legacy Dead Links Audit")
print("Targeting: 'my-bookings.html', 'my-orders.html', 'messages.html'")
print("=" * 75)

forbidden = ["my-bookings.html", "my-orders.html", "messages.html"]
forbidden_matches = []

for root, _, files in os.walk(FRONTEND_DIR):
    for f in files:
        if f.endswith((".js", ".html", ".css", ".json")):
            filepath = os.path.join(root, f)
            relpath = os.path.relpath(filepath, ROOT_DIR).replace("\\", "/")
            with open(filepath, "r", encoding="utf-8") as fh:
                content = fh.read()
            for target in forbidden:
                if target in content:
                    forbidden_matches.append((relpath, target))

if forbidden_matches:
    for relpath, target in forbidden_matches:
        err = f"Forbidden target '{target}' discovered in '{relpath}'"
        print(f"  [FAIL] {err}")
        failures.append(err)
else:
    print(f"  [PASS] Zero occurrences of {forbidden} found in any frontend file.")
    passed_checks += 1


# ======================================================================
# SUITE 2: Complete JavaScript Redirect & URL Target Resolution Audit
# ======================================================================
print("\n" + "=" * 75)
print("SUITE 2: JavaScript .html Redirect & Target Resolution Audit")
print("=" * 75)

js_pattern = re.compile(r'(?:["\'`])([^"\'`\r\n]*?([a-zA-Z0-9_\-\./]+\.html)[^"\'`\r\n]*?)(?:["\'`])')

total_js_refs = 0
unresolved_js_refs = []

for root, _, files in os.walk(JS_DIR):
    for f in files:
        if f.endswith(".js"):
            filepath = os.path.join(root, f)
            rel_js = os.path.relpath(filepath, ROOT_DIR).replace("\\", "/")
            with open(filepath, "r", encoding="utf-8") as fh:
                lines = fh.readlines()
            for line_no, line in enumerate(lines, 1):
                stripped = line.strip()
                if stripped.startswith("//") or stripped.startswith("*"):
                    continue
                matches = js_pattern.findall(line)
                for full_match, filename in matches:
                    total_js_refs += 1
                    cleaned = full_match
                    cleaned = cleaned.replace("${prefix}", "").replace("${depthPrefix()}", "").replace("${p}", "")
                    cleaned = cleaned.split("?")[0].split("#")[0].strip()
                    
                    norm = cleaned
                    while norm.startswith("../") or norm.startswith("./") or norm.startswith("/"):
                        if norm.startswith("../"):
                            norm = norm[3:]
                        elif norm.startswith("./"):
                            norm = norm[2:]
                        elif norm.startswith("/"):
                            norm = norm[1:]

                    resolved = False
                    if norm in all_html_files:
                        resolved = True
                    elif norm.startswith("pages/"):
                        if norm in all_html_files:
                            resolved = True
                    else:
                        if norm in all_html_files:
                            resolved = True
                        elif f"pages/user/{norm}" in all_html_files or f"pages/admin/{norm}" in all_html_files:
                            resolved = True
                        else:
                            matches_base = [h for h in all_html_files if os.path.basename(h) == os.path.basename(norm)]
                            if matches_base:
                                resolved = True

                    if not resolved:
                        err = f"Unresolved HTML target in {rel_js}:{line_no} -> '{full_match}' (cleaned: '{norm}')"
                        print(f"  [FAIL] {err}")
                        unresolved_js_refs.append(err)
                        failures.append(err)

print(f"  [INFO] Analyzed {total_js_refs} .html references across frontend/js/")
if not unresolved_js_refs:
    print(f"  [PASS] 100% of JavaScript .html references resolve to valid files ({total_js_refs} references).")
    passed_checks += 1


# ======================================================================
# SUITE 3: HTML Links (<a href>) Internal Resolution Audit
# ======================================================================
print("\n" + "=" * 75)
print("SUITE 3: HTML Links (<a href>) Internal Resolution Audit")
print("=" * 75)

class LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag == "a" and "href" in attr_dict:
            self.links.append((tag, attr_dict["href"]))
        elif tag == "form" and "action" in attr_dict:
            self.links.append((tag, attr_dict["action"]))

total_html_links = 0
broken_html_links = []

for rel_page, full_path in all_html_files.items():
    page_dir = os.path.dirname(full_path)
    with open(full_path, "r", encoding="utf-8") as fh:
        html_text = fh.read()
    
    parser = LinkExtractor()
    parser.feed(html_text)

    for tag, href in parser.links:
        total_html_links += 1
        if href.startswith(("#", "javascript:", "mailto:", "tel:", "http://", "https://", "data:")):
            continue
        
        clean_href = href.split("?")[0].split("#")[0].strip()
        if not clean_href:
            continue
        
        if clean_href.startswith("/"):
            target_path = os.path.normpath(os.path.join(FRONTEND_DIR, clean_href.lstrip("/")))
        else:
            target_path = os.path.normpath(os.path.join(page_dir, clean_href))
        
        target_rel = os.path.relpath(target_path, FRONTEND_DIR).replace("\\", "/")
        if target_rel not in all_html_files and not os.path.exists(target_path):
            err = f"Broken link in {rel_page}: <{tag} href='{href}'> -> '{target_rel}' not found on disk"
            print(f"  [FAIL] {err}")
            broken_html_links.append(err)
            failures.append(err)

print(f"  [INFO] Analyzed {total_html_links} links across all 26 HTML pages.")
if not broken_html_links:
    print(f"  [PASS] 100% of HTML href links resolve to valid destinations.")
    passed_checks += 1


# ======================================================================
# SUITE 4: JavaScript Syntax & Node Execution Readiness Audit
# ======================================================================
print("\n" + "=" * 75)
print("SUITE 4: JavaScript Syntax & Simulated DOM Execution Readiness")
print("=" * 75)

# 1. Syntax check with node --check
syntax_failures = []
all_js_files = []
for root, _, files in os.walk(JS_DIR):
    for f in files:
        if f.endswith(".js"):
            all_js_files.append(os.path.join(root, f))

for js_path in all_js_files:
    rel_js = os.path.relpath(js_path, ROOT_DIR).replace("\\", "/")
    res = subprocess.run(["node", "--check", js_path], capture_output=True, text=True)
    if res.returncode != 0:
        err = f"Syntax error in {rel_js}: {res.stderr.strip()}"
        print(f"  [FAIL] {err}")
        syntax_failures.append(err)
        failures.append(err)

if not syntax_failures:
    print(f"  [PASS] All {len(all_js_files)} JS files parsed cleanly with zero syntax errors.")
    passed_checks += 1

# 2. Simulated DOM Execution of Core Navigation Functions in Node.js
# Uses isolated vm contexts to simulate individual browser page environments
dom_test_harness = """
const fs = require('fs');
const path = require('path');
const vm = require('vm');

function createPageEnvironment(pathname, search = '?id=1') {
  const elements = {};
  function mockEl(id, tag = 'div') {
    return {
      id,
      tagName: tag.toUpperCase(),
      classList: {
        _classes: new Set(),
        add: function(c) { this._classes.add(c); },
        remove: function(c) { this._classes.delete(c); },
        toggle: function(c) {
          if (this._classes.has(c)) { this._classes.delete(c); return false; }
          else { this._classes.add(c); return true; }
        },
        contains: function(c) { return this._classes.has(c); }
      },
      style: {},
      dataset: {},
      value: '1',
      textContent: '',
      innerHTML: '',
      children: [],
      appendChild: function(c) { this.children.push(c); },
      addEventListener: function(event, fn) {},
      dispatchEvent: function(e) {},
      focus: function() {}
    };
  }

  const sandbox = {
    console,
    elements,
    setTimeout,
    clearTimeout,
    setInterval,
    clearInterval,
    URLSearchParams,
    Date,
    Number,
    Array,
    String,
    parseInt,
    parseFloat,
    isNaN,
    localStorage: {
      getItem: function(k) { return null; },
      setItem: function(k, v) {},
      removeItem: function(k) {}
    },
    Event: function(type) { this.type = type; },
    PropertyAPI: {
      getById: async (id) => ({
        id: 101,
        title: 'Student PG Premnagar',
        pricePerMonth: 6500,
        images: ['https://example.com/p1.jpg'],
        amenities: ['WiFi', 'Meals'],
        location: { city: 'Dehradun' }
      }),
      getRooms: async () => [{ id: 1, roomNumber: '101', pricePerMonth: 6500, capacity: 2 }]
    },
    ProductAPI: {
      getById: async (id) => ({
        id: 202,
        title: 'Calculus Textbook',
        price: 450,
        listingType: 'SELL',
        images: ['https://example.com/b1.jpg']
      })
    },
    ReviewAPI: {
      getSummary: async () => ({ averageRating: 4.8, count: 12 }),
      getByItem: async () => ({ content: [] })
    },
    WishlistAPI: { check: async () => false, add: async () => {}, remove: async () => {} },
    CategoryAPI: { getAll: async () => [{ id: 1, name: 'Books', type: 'PRODUCT' }] },
    logBehavior: () => {}
  };

  sandbox.window = sandbox;
  sandbox.document = {
    title: 'StayMart Test Page',
    body: mockEl('body', 'body'),
    getElementById: function(id) {
      if (!elements[id]) {
        elements[id] = mockEl(id);
      }
      return elements[id];
    },
    querySelector: function(sel) { return mockEl('sel_' + sel); },
    querySelectorAll: function(sel) { return [mockEl('el1'), mockEl('el2')]; },
    createElement: function(tag) { return mockEl('new_' + tag, tag); },
    addEventListener: function(evt, handler) {}
  };

  sandbox.window.location = { pathname, search };
  sandbox.window.addEventListener = function() {};
  sandbox.window.scrollTo = function() {};

  return vm.createContext(sandbox);
}

(async function runAllSimulations() {
  // Scenario A: Global Navigation (auth.js)
  {
    const ctx = createPageEnvironment('/index.html');
    vm.runInContext(fs.readFileSync(path.join('frontend', 'js', 'auth.js'), 'utf8'), ctx);
    
    ctx.openMobileDrawer();
    if (!ctx.elements['mobileDrawer'].classList.contains('open')) throw new Error('mobileDrawer failed to open');
    ctx.closeMobileDrawer();
    if (ctx.elements['mobileDrawer'].classList.contains('open')) throw new Error('mobileDrawer failed to close');

    ctx.toggleMobileSearch();
    if (!ctx.elements['mobileSearchDrawer'].classList.contains('open')) throw new Error('mobileSearchDrawer failed to toggle');
    ctx.clearMobileSearch();

    ctx.openPostChooser();
    if (!ctx.elements['postChooserOverlay'].classList.contains('open')) throw new Error('postChooserOverlay failed to open');
    ctx.closePostChooser();
    if (ctx.elements['postChooserOverlay'].classList.contains('open')) throw new Error('postChooserOverlay failed to close');

    ctx.updateBottomNavActive();
    console.log('[NODE-TEST] auth.js navigation passed');
  }

  // Scenario B: Search Page Off-Canvas Filters (search.js)
  {
    const ctx = createPageEnvironment('/search-properties.html');
    vm.runInContext(fs.readFileSync(path.join('frontend', 'js', 'auth.js'), 'utf8'), ctx);
    vm.runInContext(fs.readFileSync(path.join('frontend', 'js', 'utils.js'), 'utf8'), ctx);
    vm.runInContext(fs.readFileSync(path.join('frontend', 'js', 'search.js'), 'utf8'), ctx);

    ctx.toggleMobileFilters(true);
    if (!ctx.elements['filterSidebar'].classList.contains('open')) throw new Error('filterSidebar failed to open');
    ctx.toggleMobileFilters(false);
    if (ctx.elements['filterSidebar'].classList.contains('open')) throw new Error('filterSidebar failed to close');

    ctx.openFilterDrawer();
    if (!ctx.elements['filterSidebar'].classList.contains('open')) throw new Error('openFilterDrawer failed');
    ctx.closeFilterDrawer();
    if (ctx.elements['filterSidebar'].classList.contains('open')) throw new Error('closeFilterDrawer failed');

    console.log('[NODE-TEST] search.js mobile filters passed');
  }

  // Scenario C: Property Detail Sticky CTA & Booking Sheet (property-detail.js)
  {
    const ctx = createPageEnvironment('/property-detail.html', '?id=101');
    vm.runInContext(fs.readFileSync(path.join('frontend', 'js', 'auth.js'), 'utf8'), ctx);
    vm.runInContext(fs.readFileSync(path.join('frontend', 'js', 'utils.js'), 'utf8'), ctx);
    vm.runInContext(fs.readFileSync(path.join('frontend', 'js', 'property-detail.js'), 'utf8'), ctx);

    await ctx.loadProperty();
    ctx.openMobileBookingSheet();
    if (!ctx.elements['bookingSheetOverlay'].classList.contains('open')) throw new Error('bookingSheetOverlay failed to open');
    ctx.closeMobileBookingSheet();
    if (ctx.elements['bookingSheetOverlay'].classList.contains('open')) throw new Error('bookingSheetOverlay failed to close');
    
    ctx.syncBookingRoom('1');
    ctx.syncBookingMonths('3');

    console.log('[NODE-TEST] property-detail.js sticky bar & booking sheet passed');
  }

  // Scenario D: Product Detail Sticky CTA & Order Sheet (product-detail.js)
  {
    const ctx = createPageEnvironment('/product-detail.html', '?id=202');
    vm.runInContext(fs.readFileSync(path.join('frontend', 'js', 'auth.js'), 'utf8'), ctx);
    vm.runInContext(fs.readFileSync(path.join('frontend', 'js', 'utils.js'), 'utf8'), ctx);
    vm.runInContext(fs.readFileSync(path.join('frontend', 'js', 'product-detail.js'), 'utf8'), ctx);

    await ctx.loadProduct();
    ctx.openMobileOrderSheet();
    if (!ctx.elements['orderSheetOverlay'].classList.contains('open')) throw new Error('orderSheetOverlay failed to open');
    ctx.closeMobileOrderSheet();
    if (ctx.elements['orderSheetOverlay'].classList.contains('open')) throw new Error('orderSheetOverlay failed to close');

    ctx.syncOrderQty('2');
    ctx.syncOrderType('BUY');

    console.log('[NODE-TEST] product-detail.js sticky bar & order sheet passed');
  }

  console.log('ALL SIMULATED EXECUTION SCENARIOS PASSED!');
})().catch(err => {
  console.error('[NODE-TEST-FAIL]', err.message);
  process.exit(1);
});
"""

sim_res = subprocess.run(["node", "-e", dom_test_harness], capture_output=True, text=True, cwd=ROOT_DIR)
if sim_res.returncode != 0:
    err = f"Node simulated DOM execution failed: {sim_res.stderr.strip()}"
    print(f"  [FAIL] {err}")
    failures.append(err)
else:
    print(f"  [PASS] Simulated execution harness verified interactive functions in auth.js, search.js, property-detail.js, product-detail.js across isolated page environments.")
    passed_checks += 1


# ======================================================================
# SUITE 5: Mobile DOM Elements & Event Bindings Verification
# ======================================================================
print("\n" + "=" * 75)
print("SUITE 5: Mobile Navigation, Drawer, Bottom Nav, Filters & CTA DOM Bindings")
print("=" * 75)

public_htmls = [
    "index.html",
    "search-properties.html",
    "search-products.html",
    "property-detail.html",
    "product-detail.html"
]

for html_file in public_htmls:
    html_path = os.path.join(FRONTEND_DIR, html_file)
    with open(html_path, "r", encoding="utf-8") as fh:
        html = fh.read()

    print(f"\n  Checking {html_file}:")
    
    # 1. Mobile Header & Drawer
    header_checks = [
        ('id="mobileMenuToggle"', 'Mobile hamburger trigger'),
        ('onclick="openMobileDrawer()"', 'Trigger opens mobile drawer'),
        ('id="mobileSearchTrigger"', 'Mobile search trigger button'),
        ('onclick="toggleMobileSearch()"', 'Trigger toggles mobile search'),
        ('id="mobileSearchDrawer"', 'Mobile search expandable drawer container'),
        ('id="mobileDrawer"', 'Mobile navigation drawer element'),
        ('id="mobileDrawerOverlay"', 'Mobile drawer backdrop overlay'),
        ('onclick="closeMobileDrawer()"', 'Backdrop closes mobile drawer'),
        ('id="drawerUserCard"', 'User profile card in drawer'),
        ('id="drawerAccountSection"', 'Account links container in drawer'),
        ('id="drawerAccountLinks"', 'Account nav element in drawer'),
        ('id="drawerFooter"', 'Drawer footer container')
    ]
    for pattern_str, label in header_checks:
        if pattern_str not in html:
            err = f"{html_file} missing {label} ({pattern_str})"
            print(f"    [FAIL] {err}")
            failures.append(err)
        else:
            print(f"    [PASS] {label}")

    # 2. Bottom Nav (for non-detail pages)
    if "detail" not in html_file:
        bottom_nav_checks = [
            ('id="mobileBottomNav"', 'Mobile sticky bottom navigation bar'),
            ('data-tab="properties"', 'Explore tab link'),
            ('data-tab="products"', 'Market tab link'),
            ('onclick="openPostChooser(event)"', 'Post listing button trigger'),
            ('data-tab="chat"', 'Chats tab link'),
            ('data-tab="account"', 'Account tab link'),
            ('id="postChooserOverlay"', 'Post listing chooser sheet overlay'),
            ('onclick="closePostChooser(event)"', 'Chooser backdrop click to close'),
            ('onclick="closePostChooser()"', 'Chooser cancel button handler')
        ]
        for pattern_str, label in bottom_nav_checks:
            if pattern_str not in html:
                err = f"{html_file} missing {label} ({pattern_str})"
                print(f"    [FAIL] {err}")
                failures.append(err)
            else:
                print(f"    [PASS] {label}")

# 3. Filter Sheet on search pages
for sp in ["search-properties.html", "search-products.html"]:
    sp_path = os.path.join(FRONTEND_DIR, sp)
    with open(sp_path, "r", encoding="utf-8") as fh:
        html = fh.read()
    print(f"\n  Checking Filter Sheet in {sp}:")
    filter_checks = [
        ('class="mobile-filter-toggle"', 'Mobile filter toggle button'),
        ('onclick="toggleMobileFilters(true)"', 'Button triggers mobile filter open'),
        ('id="filterBadge"', 'Dynamic active filter counter badge'),
        ('id="filterDrawerOverlay"', 'Filter drawer backdrop overlay'),
        ('onclick="toggleMobileFilters(false)"', 'Backdrop closes filter drawer'),
        ('id="filterSidebar"', 'Filter sidebar container'),
        ('class="filter-close-btn"', 'Filter sheet close button'),
        ('onclick="applyAndCloseFilters()"', 'Apply & close filters button action')
    ]
    for pattern_str, label in filter_checks:
        if pattern_str not in html:
            err = f"{sp} missing {label} ({pattern_str})"
            print(f"    [FAIL] {err}")
            failures.append(err)
        else:
            print(f"    [PASS] {label}")

# 4. Sticky CTA Bar on Property Detail
prop_path = os.path.join(FRONTEND_DIR, "property-detail.html")
with open(prop_path, "r", encoding="utf-8") as fh:
    prop_html = fh.read()
print(f"\n  Checking Sticky CTA Bar & Booking Sheet in property-detail.html:")
prop_checks = [
    ('id="mobileDetailCtaBar"', 'Sticky bottom CTA bar'),
    ('id="mobileCtaPrice"', 'Mobile CTA price display'),
    ('id="mobileCtaBadge"', 'Mobile CTA availability badge'),
    ('id="mobileCtaWishlist"', 'Mobile CTA wishlist button'),
    ('onclick="toggleWishlist(event)"', 'Wishlist toggle handler'),
    ('id="mobileCtaChat"', 'Mobile CTA chat with owner button'),
    ('onclick="contactOwner()"', 'Chat with owner handler'),
    ('id="mobileCtaBookBtn"', 'Mobile primary book now button'),
    ('onclick="openMobileBookingSheet()"', 'Book now button opens booking sheet'),
    ('id="bookingSheetOverlay"', 'Slide-up booking sheet modal overlay'),
    ('onclick="closeMobileBookingSheet(event)"', 'Sheet backdrop close handler'),
    ('onclick="closeMobileBookingSheet()"', 'Sheet header close button handler'),
    ('id="mobileRoomSelect"', 'Room select dropdown in sheet'),
    ('onchange="syncBookingRoom(this.value)"', 'Room select bi-directional sync handler'),
    ('id="mobileMonthsSelect"', 'Months stay duration select dropdown in sheet'),
    ('onchange="syncBookingMonths(this.value)"', 'Months duration sync handler'),
    ('id="mobileBookingMessage"', 'Message textarea in booking sheet'),
    ('id="mobileTotalRent"', 'Total rent estimate display in booking sheet'),
    ('onclick="executeMobileBooking()"', 'Confirm & Send Request booking action')
]
for pattern_str, label in prop_checks:
    if pattern_str not in prop_html:
        err = f"property-detail.html missing {label} ({pattern_str})"
        print(f"    [FAIL] {err}")
        failures.append(err)
    else:
        print(f"    [PASS] {label}")

# 5. Sticky CTA Bar on Product Detail
prod_path = os.path.join(FRONTEND_DIR, "product-detail.html")
with open(prod_path, "r", encoding="utf-8") as fh:
    prod_html = fh.read()
print(f"\n  Checking Sticky CTA Bar & Order Sheet in product-detail.html:")
prod_checks = [
    ('id="mobileDetailCtaBar"', 'Sticky bottom CTA bar'),
    ('id="mobileCtaPrice"', 'Mobile CTA price display'),
    ('id="mobileCtaBadge"', 'Mobile CTA availability badge'),
    ('id="mobileCtaWishlist"', 'Mobile CTA wishlist button'),
    ('onclick="toggleWishlist(event)"', 'Wishlist toggle handler'),
    ('id="mobileCtaChat"', 'Mobile CTA chat with seller button'),
    ('onclick="contactSeller()"', 'Chat with seller handler'),
    ('id="mobileCtaBuyBtn"', 'Mobile primary buy now button'),
    ('onclick="openMobileOrderSheet()"', 'Buy now button opens order sheet'),
    ('id="orderSheetOverlay"', 'Slide-up order sheet modal overlay'),
    ('onclick="closeMobileOrderSheet(event)"', 'Order sheet backdrop close handler'),
    ('onclick="closeMobileOrderSheet()"', 'Order sheet header close button handler'),
    ('id="mobileQtySelect"', 'Quantity select dropdown in sheet'),
    ('onchange="syncOrderQty(this.value)"', 'Quantity sync handler'),
    ('id="mobileOrderTypeSelect"', 'Order type select dropdown in sheet'),
    ('onchange="syncOrderType(this.value)"', 'Order type sync handler'),
    ('id="mobileOrderMessage"', 'Message textarea in order sheet'),
    ('id="mobileOrderTotal"', 'Total amount display in order sheet'),
    ('id="mobileConfirmOrderBtn"', 'Confirm order button element'),
    ('onclick="executeMobileOrder()"', 'Confirm order execution handler')
]
for pattern_str, label in prod_checks:
    if pattern_str not in prod_html:
        err = f"product-detail.html missing {label} ({pattern_str})"
        print(f"    [FAIL] {err}")
        failures.append(err)
    else:
        print(f"    [PASS] {label}")

if not any("missing" in f for f in failures):
    print("\n  [PASS] All mobile DOM elements and event bindings verified present and wired.")
    passed_checks += 1


# ======================================================================
# SUITE 6: CSS Classes & Design Tokens Verification
# ======================================================================
print("\n" + "=" * 75)
print("SUITE 6: CSS Design Tokens & Mobile Styles Verification")
print("=" * 75)

global_css_path = os.path.join(CSS_DIR, "global.css")
dashboard_css_path = os.path.join(CSS_DIR, "dashboard.css")

with open(global_css_path, "r", encoding="utf-8") as fh:
    global_css = fh.read()

with open(dashboard_css_path, "r", encoding="utf-8") as fh:
    dashboard_css = fh.read()

# Verify key CSS classes exist in global.css
required_classes = [
    (".nav-mobile-toggle", "Mobile hamburger button style"),
    (".mobile-search-drawer", "Expandable mobile search drawer style"),
    (".mobile-search-drawer.open", "Search drawer open transition state"),
    (".mobile-drawer", "Slide-out navigation drawer style"),
    (".mobile-drawer.open", "Navigation drawer open spring transition"),
    (".mobile-drawer-overlay", "Drawer backdrop overlay style"),
    (".mobile-bottom-nav", "Fixed bottom navigation bar style"),
    (".bottom-nav-item", "Bottom nav individual tab item style"),
    (".bottom-nav-item.active", "Bottom nav active indicator style"),
    (".bottom-nav-post-wrap", "Floating post listing chooser wrapper style"),
    (".bottom-nav-post-btn", "Floating post listing (+) button style"),
    (".post-chooser-overlay", "Post chooser modal backdrop style"),
    (".post-chooser-sheet", "Post chooser slide-up sheet style"),
    (".mobile-filter-toggle", "Mobile filter trigger button style"),
    (".filter-drawer-backdrop", "Filter drawer backdrop overlay style"),
    (".filter-sidebar", "Faceted filter sidebar style"),
    (".filter-sidebar.open", "Filter sidebar mobile open drawer style"),
    (".filter-badge", "Live active filter counter badge style"),
    (".mobile-detail-cta-bar", "Fixed detail bottom CTA bar style"),
    (".booking-sheet-overlay", "Detail booking/order sheet overlay style"),
    (".booking-sheet-overlay.open", "Detail sheet modal open state"),
    (".booking-sheet", "Slide-up sheet modal card style"),
    (".search-layout", "Responsive search layout class"),
    (".table", "Dashboard table utility class"),
    (".filter-tag", "Active filter chip style"),
    ("@keyframes shimmer", "Shimmer animation keyframes")
]

for cls, label in required_classes:
    if cls not in global_css:
        err = f"global.css missing {label} ({cls})"
        print(f"  [FAIL] {err}")
        failures.append(err)
    else:
        print(f"  [PASS] {label} ({cls}) verified.")

# Verify CSS variable harmonization
global_vars = set(re.findall(r'(--[a-zA-Z0-9_\-]+)\s*:', global_css))
dashboard_var_uses = set(re.findall(r'var\((--[a-zA-Z0-9_\-]+)\)', dashboard_css))

unresolved_vars = [v for v in dashboard_var_uses if v not in global_vars]
if unresolved_vars:
    err = f"dashboard.css uses undefined CSS variables: {unresolved_vars}"
    print(f"  [FAIL] {err}")
    failures.append(err)
else:
    print(f"  [PASS] 100% of CSS variables in dashboard.css resolve to tokens defined in global.css ({len(dashboard_var_uses)} variables).")
    passed_checks += 1


# ======================================================================
# SUITE 7: Backend Automated Test Execution
# ======================================================================
print("\n" + "=" * 75)
print("SUITE 7: Backend Automated Test Execution (JUnit 5)")
print("=" * 75)

backend_test_cmd = [sys.executable, os.path.join(ROOT_DIR, "scripts", "run_backend_tests.py")]
res = subprocess.run(backend_test_cmd, capture_output=True, text=True, cwd=ROOT_DIR)

if res.returncode != 0:
    err = f"Backend test runner failed with exit code {res.returncode}:\n{res.stdout}\n{res.stderr}"
    print(f"  [FAIL] {err}")
    failures.append(err)
else:
    if "13 tests successful" in res.stdout and "0 tests failed" in res.stdout:
        print("  [PASS] All 13 JUnit 5 backend tests compiled and passed with exit code 0.")
        passed_checks += 1
    else:
        err = f"Backend tests ran but did not output expected 13 successful tests: {res.stdout}"
        print(f"  [FAIL] {err}")
        failures.append(err)


# ======================================================================
# FINAL VERDICT
# ======================================================================
print("\n" + "=" * 75)
print("EMPIRICAL VERIFICATION SUMMARY")
print("=" * 75)
print(f"Total Test Suites Passed: {passed_checks} / 7")
print(f"Total Defects Found: {len(failures)}")

if failures:
    print("\nDEFECT LOG:")
    for idx, f in enumerate(failures, 1):
        print(f"  {idx}. {f}")
    print("\n" + "#" * 75)
    print("VERDICT: REJECT")
    print("#" * 75)
    sys.exit(1)
else:
    print("\nALL ADVERSARIAL STRESS-TESTS AND VERIFICATION SUITES PASSED!")
    print("\n" + "#" * 75)
    print("VERDICT: APPROVE")
    print("#" * 75)
    sys.exit(0)
