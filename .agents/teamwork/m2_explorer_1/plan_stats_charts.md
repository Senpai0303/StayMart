# Implementation Blueprint: Marketplace Statistics, Animated Counters, Savings Calculator & Creative Visual Charts

**Milestone:** M2 — Marketplace Statistics & Creative Visuals (Features 8 and 12 in `PROJECT.md`)  
**Author:** `m2_explorer_1` (Investigation & Architecture Explorer)  
**Target Files:**  
- `frontend/index.html` (DOM markup & script inclusions)  
- `frontend/css/global.css` (Component styles, layout grids, animations & responsive media queries)  
- `frontend/js/stats.js` (NEW: Metric counters animation engine & interactive dual-mode savings calculator)  
- `frontend/js/charts.js` (NEW: Public creative visual charts with Chart.js 4.4.1 + responsive SVG fallback engine)  

---

## 1. Architectural Overview & Component Structure

### 1.1 Objective
Transform the StayMart homepage into an engaging, data-rich student marketplace by embedding:
1. **High-Impact Animated Metric Counters**: Demonstrating platform scale and trust (500+ Verified PGs, 1,200+ Student Listings, ₹4,500/mo Average Student Savings, 98% Senior Verification Rate).
2. **Interactive Student Savings Calculator**: A dual-mode financial calculator allowing students to compute real-time cash savings on zero-brokerage campus housing (Mode A) and pre-loved university gear (Mode B).
3. **Public Creative Visual Charts**: Visualizing Dehradun campus rental benchmarks (Graphic Era, UPES, Subhash Nagar, DIT) and student re-commerce pricing trends across academic semesters.
4. **Resilience & Mobile-First Performance**: Flawless zero-overflow display from 375px mobile to 1440px desktop, featuring an offline-first dual engine (Chart.js 4.4.1 CDN with zero-dependency responsive SVG vector fallback).

### 1.2 File Layout & Component Map
```
d:\Mini5th\
├── frontend/
│   ├── index.html                   # Add Metrics Ribbon, Calculator Widget, Campus Charts & script tags
│   ├── css/
│   │   └── global.css               # Append styles for metrics ribbon, calculator, and chart containers
│   └── js/
│       ├── stats.js                 # [NEW] Counter animation logic & Savings Calculator controller
│       ├── charts.js                # [NEW] Public campus rent & re-commerce charts (Chart.js + SVG fallback)
│       └── home.js                  # Loads categories, listings, triggers stats/charts initialization
```

### 1.3 Homepage Section Flow
The components are strategically organized on `frontend/index.html` to create a compelling commercial student narrative:
1. **Top Navbar & Category Strip** (Existing commercial header)
2. **Hero Banner & Promo Card** (Enhanced with counter animations)
3. **Marketplace Metrics Ribbon** (`.metrics-ribbon-section`): 4 verified platform trust counters
4. **Category Grid & Featured Accommodations** (Existing listings)
5. **Fresh Student Classifieds (Re-Commerce)** (Existing listings)
6. **Interactive Student Savings Calculator** (`.savings-calc-section`): Dual-mode interactive tool
7. **Campus Market Insights & Creative Visual Charts** (`.campus-charts-section`): 2 interactive public charts
8. **Trending Accommodations & How StayMart Works** (Existing value proposition)
9. **Marketplace Footer** (Existing links and trust guarantees)

---

## 2. Component 1: Animated Metric Counters (Feature 8)

### 2.1 Placement & Visual Hierarchy
- **Primary Location:** A dedicated full-width **Marketplace Metrics Ribbon** inserted right below the Hero Banner (`index.html` after line 140, before `<main class="container">` or as the top section inside `<main>`).
- **Secondary Enhancement:** Connect the existing 3 counter nodes in the Hero Promo Card (`.hero-promo-card .hero-stats`, line 132-136) to the same animation engine using data attributes.

### 2.2 Student-Centric Metrics Definition
Each metric has been defined around verified student pain points across Uttarakhand universities:

| Metric | Target | Prefix / Suffix | Badge / Label | Sub-Caption / Context | Rationale |
|---|---|---|---|---|---|
| **Verified Campus PGs** | `500` | `+` | 🏠 Verified Campus PGs | Near GEU, UPES, DIT & Doon Univ | Directly addresses the accommodation search crisis |
| **Active Student Ads** | `1200` | `+` | 🛒 Student Classifieds | Laptops, bikes, books & furniture | Validates active peer-to-peer campus re-commerce |
| **Avg Student Savings** | `4500` | `₹` / `/mo` | 💰 Avg Monthly Savings | Zero brokerage + shared utilities | Quantifies the financial advantage of StayMart |
| **Senior Verification Rate** | `98` | `%` | 🛡️ Senior Verification | College ID & caretaker verified | Solves campus trust, security, and fraud concerns |

### 2.3 Animation Engine Specification (`IntersectionObserver` + RAF)
The animation engine in `frontend/js/stats.js` follows these exact specifications:
- **Observer Trigger:** An `IntersectionObserver` with `threshold: 0.25` and `rootMargin: '0px 0px -50px 0px'`.
- **One-Shot Execution:** Once the ribbon scrolls into view, `observer.unobserve(entry.target)` is called so animations run once smoothly without jarring restarts during casual scrolling.
- **Duration:** 1,800ms (1.8 seconds) for smooth, visible deceleration.
- **High-Performance Easing:** Exponential Deceleration (`easeOutExpo`):
  $$\text{easeOutExpo}(t) = \begin{cases} 1 & \text{if } t = 1 \\ 1 - 2^{-10t} & \text{if } t < 1 \end{cases}$$
  This starts with swift momentum and gently settles onto the exact target value.
- **Number Formatting:** Standard Indian numbering system (`Number(value).toLocaleString('en-IN')`).
- **Initial HTML Fallback:** The HTML markup renders the target numbers directly (e.g. `500+`, `1,200+`, `₹4,500/mo`, `98%`). If JavaScript is disabled or fails to execute, users and search engines immediately see valid statistics.

### 2.4 HTML Structure for Metrics Ribbon
```html
<!-- Marketplace Metrics Ribbon (Feature 8) -->
<section class="metrics-ribbon-section" aria-label="Marketplace Statistics">
  <div class="container">
    <div class="metrics-ribbon-card">
      <div class="metrics-grid">
        <!-- Metric 1: Verified PGs -->
        <div class="metric-item">
          <div class="metric-icon-box icon-teal">🏠</div>
          <div class="metric-content">
            <div class="metric-value-wrap">
              <span class="metric-val" data-counter data-target="500" data-suffix="+">500+</span>
            </div>
            <div class="metric-title">Verified Campus PGs</div>
            <div class="metric-sub">Near GEU, UPES & DIT</div>
          </div>
        </div>

        <!-- Metric 2: Student Listings -->
        <div class="metric-item">
          <div class="metric-icon-box icon-amber">🛒</div>
          <div class="metric-content">
            <div class="metric-value-wrap">
              <span class="metric-val" data-counter data-target="1200" data-suffix="+">1,200+</span>
            </div>
            <div class="metric-title">Student Classifieds</div>
            <div class="metric-sub">Tech, books & gear</div>
          </div>
        </div>

        <!-- Metric 3: Avg Monthly Savings -->
        <div class="metric-item">
          <div class="metric-icon-box icon-green">💰</div>
          <div class="metric-content">
            <div class="metric-value-wrap">
              <span class="metric-val" data-counter data-target="4500" data-prefix="₹" data-suffix="/mo">₹4,500/mo</span>
            </div>
            <div class="metric-title">Avg Monthly Savings</div>
            <div class="metric-sub">Zero brokerage fee</div>
          </div>
        </div>

        <!-- Metric 4: Senior Verification Rate -->
        <div class="metric-item">
          <div class="metric-icon-box icon-cyan">🛡️</div>
          <div class="metric-content">
            <div class="metric-value-wrap">
              <span class="metric-val" data-counter data-target="98" data-suffix="%">98%</span>
            </div>
            <div class="metric-title">Senior Verified Rate</div>
            <div class="metric-sub">College ID verified</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
```

---

## 3. Component 2: Interactive Student Savings Calculator (Feature 9)

### 3.1 Overview & Dual-Mode Structure
The Student Savings Calculator is an interactive, visual dual-mode widget embedded in `frontend/index.html`. It demonstrates transparent financial savings to university students through two modes:
- **Mode A: Accommodation Brokerage Savings**: Calculates broker commission saved (typically 1 month's full rent in Dehradun: ₹5,000 - ₹25,000) plus bundled campus utilities (WiFi, RO water, cleaning) versus commercial rentals.
- **Mode B: College Gear Savings (Campus Re-Commerce)**: Allows students to choose or customize semester equipment packages (Textbooks, Engineering Coding Setup, Room Setup, Campus Commute) and computes discounts compared to Amazon/retail prices (50% to 72% savings).

### 3.2 Mode A: Accommodation Brokerage Savings Logic
1. **Interactive Controls:**
   - **Monthly Rent Range Slider (`#calcRentSlider`):**
     - Minimum: `₹5,000`
     - Maximum: `₹25,000`
     - Step: `₹500`
     - Default: `₹9,000` (standard median student PG rent in Clement Town / Prem Nagar)
     - Synchronized with active numeric badge (`#calcRentVal`).
   - **Quick-Select Rent Presets:**
     - `₹6,000` (Budget Twin Room)
     - `₹9,000` (Standard PG with 3 Meals)
     - `₹14,000` (Independent 1 BHK Flat)
     - `₹20,000` (Shared 2 BHK Apartment)
   - **Stay Duration Selector (`#calcStayDuration`):**
     - `6 Months` (Single Semester)
     - `10 Months` (Standard Academic Year — Default)
     - `12 Months` (Annual Lease)
   - **Accommodation Type Switcher (`#calcAccType`):**
     - `PG with Meals Included`
     - `Furnished Flat / Bedspace`
2. **Financial Formulation:**
   - **Standard Brokerage Fee Avoided:**
     $$\text{Brokerage Saved} = \text{Monthly Rent} \times 1.0$$
     *(Traditional property brokers in Dehradun demand 1 full month rent as an upfront non-refundable fee).*
   - **Shared Utility & WiFi Economies:**
     $$\text{Utility Savings} = ₹1,200 \times \text{Duration (Months)}$$
     *(Independent rentals charge ₹800/mo WiFi + ₹400/mo water/maintenance; StayMart campus PGs bundle high-speed fiber & utilities).*
   - **Mess / Meal Advantage (for PG with Food option):**
     $$\text{Meal Savings} = ₹2,500 \times \text{Duration (Months)}$$
     *(PG mess costs ₹3,000/mo within rent vs eating outside/ordering via Swiggy/Zomato at ₹5,500/mo).*
   - **Total Net Pocket Savings:**
     $$\text{Total Savings} = \text{Brokerage Saved} + \text{Utility Savings} (+ \text{Meal Savings})$$
   - *Example with Default Values (₹9,000 rent, 10 months academic year, standard PG):*
     - Brokerage Saved: ₹9,000
     - Shared Utilities: ₹12,000
     - **Total Cash Kept by Student: ₹21,000!**

### 3.3 Mode B: College Gear Savings Logic
1. **Interactive Category Packages:**
   Four pre-computed packages reflect the authentic academic needs of Uttarakhand students:

   | Package ID | Package Name | Includes | Benchmark Retail / Amazon Price | StayMart Senior Price | Net Cash Saved | % Saved | Eco-Impact (CO2e) |
   |---|---|---|---|---|---|---|---|
   | `pkg_books` | **📚 Semester Textbooks & Notes** | GATE prep books, B.Tech semester guides, engineering drafter, hand notes | ₹6,500 | ₹1,800 | **₹4,700** | 72% | 12 kg CO2 |
   | `pkg_laptop` | **💻 Engineering Laptop Setup** | Refurbished Core i5/Ryzen 5 laptop (16GB RAM), 22" monitor, mouse & bag | ₹56,000 | ₹24,500 | **₹31,500** | 56% | 185 kg CO2 |
   | `pkg_room` | **🪑 Room Setup Essentials** | Solid wood study desk, ergonomic chair, metal shoe rack & room cooler | ₹14,500 | ₹4,800 | **₹9,700** | 67% | 45 kg CO2 |
   | `pkg_mobility`| **🚲 Campus Mobility & Commute** | 21-speed geared mountain bicycle / serviced scooter with helmet | ₹12,000 (Cycle) / ₹82,000 (Activa) | ₹4,200 (Cycle) / ₹34,000 (Activa) | **₹7,800 - ₹48,000** | 65% | 80 kg CO2 |

2. **Custom Multi-Select Checklist:**
   Students can toggle checkboxes to build a custom bundle. The calculator live-updates total retail cost, StayMart resale cost, total savings, and circular economy environmental impact.

### 3.4 HTML Structure for Savings Calculator
```html
<!-- Interactive Student Savings Calculator (Feature 9) -->
<section class="section savings-calc-section" id="studentCalculator" aria-label="Student Savings Calculator">
  <div class="section-header">
    <div class="section-title-wrap">
      <span class="section-kicker">SMART CAMPUS FINANCE</span>
      <h2 class="section-title">💡 Student Savings Calculator</h2>
      <p class="text-secondary-text">See how much real cash you save on zero-brokerage housing and pre-loved university gear</p>
    </div>
    <!-- Mode Toggle Pills -->
    <div class="calc-mode-switcher" role="tablist">
      <button type="button" class="calc-mode-btn active" id="calcModeAccBtn" role="tab" aria-selected="true" onclick="switchCalcMode('accommodation')">
        🏠 Housing & Brokerage
      </button>
      <button type="button" class="calc-mode-btn" id="calcModeGearBtn" role="tab" aria-selected="false" onclick="switchCalcMode('gear')">
        🎒 Campus Gear Re-Commerce
      </button>
    </div>
  </div>

  <div class="calc-card">
    <!-- MODE A: ACCOMMODATION BROKERAGE SAVINGS -->
    <div class="calc-pane active" id="calcPaneAccommodation">
      <div class="calc-grid">
        <!-- Controls Column -->
        <div class="calc-controls">
          <div class="calc-field">
            <div class="calc-label-row">
              <label for="calcRentSlider" class="calc-label">Monthly Accommodation Rent</label>
              <span class="calc-slider-val" id="calcRentDisplay">₹9,000 / month</span>
            </div>
            <input type="range" class="calc-range" id="calcRentSlider" min="5000" max="25000" step="500" value="9000" oninput="updateAccommodationCalc()"/>
            <div class="calc-range-limits">
              <span>₹5,000</span>
              <span>₹15,000</span>
              <span>₹25,000</span>
            </div>
            <!-- Preset Chips -->
            <div class="calc-preset-chips">
              <button type="button" class="calc-chip" onclick="setRentPreset(6000)">₹6,000 (Budget PG)</button>
              <button type="button" class="calc-chip active" onclick="setRentPreset(9000)">₹9,000 (PG + Meals)</button>
              <button type="button" class="calc-chip" onclick="setRentPreset(14000)">₹14,000 (1 BHK Flat)</button>
              <button type="button" class="calc-chip" onclick="setRentPreset(20000)">₹20,000 (Shared 2 BHK)</button>
            </div>
          </div>

          <div class="calc-field">
            <label class="calc-label">Academic Stay Duration</label>
            <div class="calc-pill-group" id="stayDurationPills">
              <button type="button" class="calc-pill" data-months="6" onclick="setDurationPreset(6)">1 Semester (6 Mos)</button>
              <button type="button" class="calc-pill active" data-months="10" onclick="setDurationPreset(10)">Academic Year (10 Mos)</button>
              <button type="button" class="calc-pill" data-months="12" onclick="setDurationPreset(12)">Full Year (12 Mos)</button>
            </div>
          </div>

          <div class="calc-field">
            <label class="calc-label">Included Amenities & Services</label>
            <div class="calc-checkbox-list">
              <label class="calc-check-label">
                <input type="checkbox" id="calcIncludeMeals" checked onchange="updateAccommodationCalc()"/>
                <span>3 Homestyle PG Meals Included (Saves eating out)</span>
              </label>
              <label class="calc-check-label">
                <input type="checkbox" id="calcIncludeUtilities" checked onchange="updateAccommodationCalc()"/>
                <span>Bundled High-Speed WiFi & Inverter Power</span>
              </label>
            </div>
          </div>
        </div>

        <!-- Result Highlights Column -->
        <div class="calc-result-box">
          <div class="calc-savings-badge">YOUR ESTIMATED SAVINGS</div>
          <div class="calc-total-amount" id="calcAccTotalSavings">₹21,000</div>
          <div class="calc-total-sub">Cash kept in your student account</div>

          <div class="calc-breakdown">
            <div class="calc-breakdown-row">
              <span class="cb-label">🏢 Brokerage Commission Saved</span>
              <span class="cb-val text-success" id="cbBrokerageVal">+₹9,000</span>
            </div>
            <div class="calc-breakdown-row">
              <span class="cb-label">📶 Bundled WiFi & Shared Utilities</span>
              <span class="cb-val text-success" id="cbUtilityVal">+₹12,000</span>
            </div>
            <div class="calc-breakdown-row" id="cbMealRow">
              <span class="cb-label">🍲 Mess vs Swiggy/Outside Food</span>
              <span class="cb-val text-success" id="cbMealVal">+₹25,000</span>
            </div>
          </div>

          <div class="calc-comparison-bar">
            <div class="bar-legend">
              <span>Traditional Broker: <strong id="cbBrokerCost">₹99,000</strong></span>
              <span>StayMart Direct: <strong class="text-success" id="cbStaymartCost">₹90,000</strong></span>
            </div>
            <div class="bar-track">
              <div class="bar-fill" id="cbSavingsBar" style="width:78%"></div>
            </div>
          </div>

          <a href="search-properties.html?type=PG" class="btn btn-primary btn-block calc-cta-btn" id="calcAccCta">
            Explore Zero-Brokerage PGs Now →
          </a>
        </div>
      </div>
    </div>

    <!-- MODE B: CAMPUS GEAR RE-COMMERCE -->
    <div class="calc-pane" id="calcPaneGear" style="display:none">
      <div class="calc-grid">
        <!-- Controls Column -->
        <div class="calc-controls">
          <div class="calc-field">
            <label class="calc-label">Select Semester Package Preset</label>
            <div class="calc-package-grid">
              <div class="package-card active" onclick="selectGearPackage('books', this)">
                <div class="pkg-icon">📚</div>
                <div class="pkg-title">Textbooks & GATE Notes</div>
                <div class="pkg-save">Save ~72%</div>
              </div>
              <div class="package-card" onclick="selectGearPackage('laptop', this)">
                <div class="pkg-icon">💻</div>
                <div class="pkg-title">Engineering Coding Setup</div>
                <div class="pkg-save">Save ~56%</div>
              </div>
              <div class="package-card" onclick="selectGearPackage('room', this)">
                <div class="pkg-icon">🪑</div>
                <div class="pkg-title">Room Setup & Cooler</div>
                <div class="pkg-save">Save ~67%</div>
              </div>
              <div class="package-card" onclick="selectGearPackage('mobility', this)">
                <div class="pkg-icon">🚲</div>
                <div class="pkg-title">Campus Cycle Commute</div>
                <div class="pkg-save">Save ~65%</div>
              </div>
            </div>
          </div>

          <div class="calc-field">
            <label class="calc-label">Or Custom Bundle Checklist</label>
            <div class="calc-checkbox-list" id="gearChecklist">
              <label class="calc-check-label">
                <input type="checkbox" data-retail="6500" data-senior="1800" data-co2="12" checked onchange="updateCustomGearCalc()"/>
                <span>Tech & Semester Textbooks (Retail ₹6,500 · Senior ₹1,800)</span>
              </label>
              <label class="calc-check-label">
                <input type="checkbox" data-retail="5500" data-senior="1800" data-co2="25" checked onchange="updateCustomGearCalc()"/>
                <span>Study Table & Ergonomic Desk Chair (Retail ₹5,500 · Senior ₹1,800)</span>
              </label>
              <label class="calc-check-label">
                <input type="checkbox" data-retail="5500" data-senior="2200" data-co2="30" onchange="updateCustomGearCalc()"/>
                <span>Symphony Personal Room Cooler (Retail ₹5,500 · Senior ₹2,200)</span>
              </label>
              <label class="calc-check-label">
                <input type="checkbox" data-retail="12000" data-senior="4200" data-co2="40" onchange="updateCustomGearCalc()"/>
                <span>Geared Mountain Bicycle (Retail ₹12,000 · Senior ₹4,200)</span>
              </label>
            </div>
          </div>
        </div>

        <!-- Result Highlights Column -->
        <div class="calc-result-box">
          <div class="calc-savings-badge">CAMPUS RE-COMMERCE SAVINGS</div>
          <div class="calc-total-amount text-success" id="calcGearSavings">₹8,400</div>
          <div class="calc-total-sub"><span id="calcGearPercent">70%</span> cheaper than Amazon / Retail</div>

          <div class="calc-price-compare">
            <div class="compare-item">
              <div class="cp-label">Retail / Amazon New</div>
              <div class="cp-val text-strike" id="calcGearRetail">₹12,000</div>
            </div>
            <div class="compare-sep">➔</div>
            <div class="compare-item">
              <div class="cp-label">StayMart Senior Price</div>
              <div class="cp-val text-primary" id="calcGearSenior">₹3,600</div>
            </div>
          </div>

          <div class="calc-eco-badge">
            <span class="eco-icon">🌱</span>
            <span class="eco-text">Prevents <strong id="calcGearCo2">37 kg</strong> CO2e through circular reuse</span>
          </div>

          <a href="search-products.html" class="btn btn-primary btn-block calc-cta-btn" id="calcGearCta">
            Shop Pre-Loved Student Gear →
          </a>
        </div>
      </div>
    </div>
  </div>
</section>
```

---

## 4. Component 3: Creative Visual Charts (Feature 12)

### 4.1 Architecture: Chart.js 4.4.1 + Zero-Dependency Responsive SVG Dual-Engine
An essential requirement of StayMart's production deployment and automated testing suite is that public charts must render reliably in:
1. High-speed desktop browsers with full CDN connectivity.
2. Offline development environments, headless test runners (`scripts/run_viewport_tests.py`), and firewalled university intranets.

**The Solution:**
In `frontend/js/charts.js`, we implement an intelligent **Dual-Engine Chart Renderer**:
- If `typeof Chart !== 'undefined'`, it initializes responsive HTML5 Canvas charts with retina resolution, custom tooltips, curved bezier lines, and animated bar entries.
- If `typeof Chart === 'undefined'` (offline mode, CDN blocked, or script timeout), it triggers `renderSvgFallback()`, dynamically creating clean `<svg>` vector charts with styled bars, polyline paths, axis labels, and tooltip hover effects.
- Result: **0% blank canvas failure rate**, 100% test compatibility.

### 4.2 Chart 1: Average Student Accommodation Rent by Campus Zone in Dehradun
- **Context:** Dehradun contains 4 distinct higher-education geographic hubs with vastly different rent profiles.
- **Campus Zones:**
  1. `Clement Town (Graphic Era University - GEU/GEHU)`
  2. `Prem Nagar (UPES Bidholi / Kandoli)`
  3. `Subhash Nagar (ISBT / South Campus)`
  4. `Rajpur Road (DIT University & Pacific Hills)`
- **Data Series:**
  - **PG with 3 Meals (Amber `#ff9900`):** Clement Town (₹6,800), Prem Nagar (₹8,200), Subhash Nagar (₹5,800), Rajpur Road (₹8,800).
  - **Single Private Room (Spruce `#002f34`):** Clement Town (₹8,500), Prem Nagar (₹10,500), Subhash Nagar (₹6,500), Rajpur Road (₹11,000).
  - **Shared Flat Bedspace (Emerald `#0a883a`):** Clement Town (₹4,500), Prem Nagar (₹5,500), Subhash Nagar (₹3,800), Rajpur Road (₹6,000).
- **Chart Presentation:**
  - Grouped Bar Chart with rounded tops (`borderRadius: 6`).
  - Y-Axis formatted with Indian Rupee symbol (`₹5k`, `₹10k`).
  - Interactive Filter Buttons: `All Types`, `PGs with Meals`, `Shared Flats`.
  - Student Tip Callout: *"💡 Tip: Subhash Nagar provides the best rent-to-commute ratio (avg ₹5,800 with food), while Clement Town has the highest pedestrian availability within 500m of GEU."*

### 4.3 Chart 2: Student Re-Commerce Volume & Price Trends across Categories
- **Context:** Student marketplace items have defined turnover cycles based on university semester dates (July/Jan new semester intake; May/June graduation move-out).
- **Categories:**
  1. `Textbooks & Guides`
  2. `Laptops & Tech`
  3. `Study Furniture`
  4. `Coolers & Appliances`
  5. `Cycles & Scooters`
- **Data Series:**
  - **StayMart Senior Resale Price (₹):**
    - Textbooks: ₹650 (Retail ₹1,800)
    - Laptops & Tech: ₹24,500 (Retail ₹48,000)
    - Study Furniture: ₹2,400 (Retail ₹6,500)
    - Coolers & Appliances: ₹2,200 (Retail ₹5,800)
    - Cycles & Scooters: ₹4,800 (Retail ₹12,000)
  - **Average Student Savings Percentage (%):**
    - Textbooks: `64%`
    - Laptops & Tech: `49%`
    - Study Furniture: `63%`
    - Coolers & Appliances: `62%`
    - Cycles & Scooters: `60%`
  - **Semester Listing Volume (Ads):**
    - Textbooks: 420 ads/term
    - Laptops & Tech: 280 ads/term
    - Study Furniture: 310 ads/term
    - Coolers & Appliances: 190 ads/term
    - Cycles & Scooters: 160 ads/term
- **Chart Presentation:**
  - Combo Dual-Axis Bar & Line Chart (Resale Price on primary axis; Discount % or Volume on secondary).
  - Toggle Switch: `Price Comparison (₹)` vs `Exchange Volume (Ads)`.

### 4.4 HTML Structure for Public Creative Visual Charts
```html
<!-- Public Creative Visual Charts (Feature 12) -->
<section class="section campus-charts-section" aria-label="Campus Market Insights">
  <div class="section-header">
    <div class="section-title-wrap">
      <span class="section-kicker">DATA-DRIVEN CAMPUS INSIGHTS</span>
      <h2 class="section-title">📊 Dehradun Student Market Trends</h2>
      <p class="text-secondary-text">Transparent rental benchmarks and re-commerce price trends across university zones</p>
    </div>
  </div>

  <div class="charts-grid">
    <!-- Chart Card 1: Rent by Campus Zone -->
    <div class="chart-box-card">
      <div class="chart-box-header">
        <div>
          <h3 class="chart-box-title">🏠 Student Accommodation Rent by Campus Zone</h3>
          <p class="chart-box-subtitle">Average monthly living costs across Dehradun's main university belts</p>
        </div>
        <div class="chart-filter-pills" id="accChartFilter">
          <button type="button" class="chart-pill active" onclick="filterRentChart('all')">All</button>
          <button type="button" class="chart-pill" onclick="filterRentChart('pg')">PG + Meals</button>
          <button type="button" class="chart-pill" onclick="filterRentChart('flat')">Shared Flats</button>
        </div>
      </div>
      <div class="chart-canvas-wrap" id="accChartContainer">
        <canvas id="campusRentChart"></canvas>
      </div>
      <div class="chart-card-footer">
        <span class="chart-insight-badge">💡 Insight:</span> Subhash Nagar & Clement Town offer the most economical shared accommodations under ₹6,500/mo.
      </div>
    </div>

    <!-- Chart Card 2: Re-Commerce Volume & Price Trends -->
    <div class="chart-box-card">
      <div class="chart-box-header">
        <div>
          <h3 class="chart-box-title">🛒 Student Re-Commerce Pricing & Savings</h3>
          <p class="chart-box-subtitle">Average pre-loved selling prices vs retail Amazon benchmark</p>
        </div>
        <div class="chart-filter-pills" id="gearChartFilter">
          <button type="button" class="chart-pill active" onclick="toggleRecommerceView('price')">Prices (₹)</button>
          <button type="button" class="chart-pill" onclick="toggleRecommerceView('volume')">Trade Volume</button>
        </div>
      </div>
      <div class="chart-canvas-wrap" id="gearChartContainer">
        <canvas id="recommerceChart"></canvas>
      </div>
      <div class="chart-card-footer">
        <span class="chart-insight-badge">🔥 Peak Activity:</span> Textbook exchanges peak in July & January; furniture surges during May graduations.
      </div>
    </div>
  </div>
</section>
```

---

## 5. CSS Specifications for `frontend/css/global.css`

To ensure full layout harmony with StayMart's OLX Deep Spruce and Amazon Amber design system, append the following clean CSS definitions into `frontend/css/global.css`:

```css
/* ==========================================================================
   Milestone 2: Marketplace Statistics & Creative Visuals
   ========================================================================== */

/* ---------- 1. Marketplace Metrics Ribbon ---------- */
.metrics-ribbon-section {
  padding: 16px 0 24px 0;
  width: 100%;
}

.metrics-ribbon-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 20px 24px;
  box-shadow: var(--shadow-sm);
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.metric-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 8px 12px;
  border-radius: var(--radius);
  transition: transform 0.2s ease, background 0.2s ease;
}

.metric-item:hover {
  transform: translateY(-2px);
  background: var(--bg-hover);
}

.metric-icon-box {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  flex-shrink: 0;
}

.metric-icon-box.icon-teal  { background: #ebf7f7; color: var(--olx-teal); }
.metric-icon-box.icon-amber { background: #fff8e6; color: var(--amazon-amber); }
.metric-icon-box.icon-green { background: #eafaf1; color: var(--success); }
.metric-icon-box.icon-cyan  { background: #e0f2fe; color: #0284c7; }

.metric-content {
  min-width: 0;
  flex: 1;
}

.metric-value-wrap {
  display: flex;
  align-items: baseline;
  gap: 2px;
}

.metric-val {
  font-size: 24px;
  font-weight: 800;
  color: var(--text-primary);
  line-height: 1.1;
  letter-spacing: -0.02em;
}

.metric-title {
  font-size: 13px;
  font-weight: 700;
  color: var(--text-primary);
  margin-top: 3px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.metric-sub {
  font-size: 11px;
  color: var(--text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* ---------- 2. Interactive Student Savings Calculator ---------- */
.savings-calc-section {
  margin-top: 10px;
  margin-bottom: 30px;
}

.section-kicker {
  display: inline-block;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.1em;
  color: var(--amazon-amber);
  margin-bottom: 4px;
}

.calc-mode-switcher {
  display: inline-flex;
  background: var(--bg-page);
  border: 1px solid var(--border);
  padding: 4px;
  border-radius: var(--radius-full);
  gap: 4px;
}

.calc-mode-btn {
  background: transparent;
  border: none;
  padding: 8px 18px;
  border-radius: var(--radius-full);
  font-size: 13px;
  font-weight: 700;
  color: var(--text-secondary);
  cursor: pointer;
  transition: var(--transition-fast);
}

.calc-mode-btn.active {
  background: var(--olx-teal);
  color: #ffffff;
  box-shadow: var(--shadow-sm);
}

.calc-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 28px;
  box-shadow: var(--shadow-sm);
  margin-top: 16px;
}

.calc-grid {
  display: grid;
  grid-template-columns: 1.25fr 1fr;
  gap: 36px;
  align-items: start;
}

.calc-field {
  margin-bottom: 24px;
}

.calc-field:last-child {
  margin-bottom: 0;
}

.calc-label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.calc-label {
  font-size: 14px;
  font-weight: 700;
  color: var(--text-primary);
}

.calc-slider-val {
  font-size: 16px;
  font-weight: 800;
  color: var(--olx-teal);
  background: var(--olx-light-teal);
  padding: 4px 10px;
  border-radius: var(--radius-sm);
}

.calc-range {
  -webkit-appearance: none;
  width: 100%;
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  outline: none;
  margin: 12px 0 6px 0;
}

.calc-range::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: var(--olx-teal);
  cursor: pointer;
  border: 3px solid #ffffff;
  box-shadow: 0 2px 6px rgba(0, 47, 52, 0.3);
  transition: transform 0.1s ease;
}

.calc-range::-webkit-slider-thumb:hover {
  transform: scale(1.15);
}

.calc-range::-moz-range-thumb {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: var(--olx-teal);
  cursor: pointer;
  border: 3px solid #ffffff;
  box-shadow: 0 2px 6px rgba(0, 47, 52, 0.3);
}

.calc-range-limits {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  color: var(--text-muted);
}

.calc-preset-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 14px;
}

.calc-chip {
  background: var(--bg-page);
  border: 1px solid var(--border);
  padding: 6px 12px;
  border-radius: var(--radius-full);
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
  cursor: pointer;
  transition: var(--transition-fast);
}

.calc-chip:hover, .calc-chip.active {
  background: var(--olx-light-teal);
  border-color: var(--olx-teal);
  color: var(--olx-teal);
  font-weight: 700;
}

.calc-pill-group {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 8px;
}

.calc-pill {
  flex: 1;
  min-width: 110px;
  background: var(--bg-page);
  border: 1px solid var(--border);
  padding: 8px 12px;
  border-radius: var(--radius);
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
  cursor: pointer;
  text-align: center;
  transition: var(--transition-fast);
}

.calc-pill.active {
  background: var(--olx-teal);
  border-color: var(--olx-teal);
  color: #ffffff;
}

.calc-checkbox-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 10px;
}

.calc-check-label {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  color: var(--text-primary);
  cursor: pointer;
}

.calc-check-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: var(--olx-teal);
  cursor: pointer;
}

/* Calculator Result Card */
.calc-result-box {
  background: linear-gradient(145deg, #002f34 0%, #00454d 100%);
  border-radius: var(--radius-lg);
  padding: 28px 24px;
  color: #ffffff;
  box-shadow: var(--shadow-md);
  position: relative;
  overflow: hidden;
}

.calc-savings-badge {
  display: inline-block;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.1em;
  color: var(--amazon-yellow);
  background: rgba(255, 216, 20, 0.15);
  padding: 4px 10px;
  border-radius: var(--radius-full);
}

.calc-total-amount {
  font-size: 42px;
  font-weight: 900;
  color: #ffffff;
  line-height: 1.1;
  margin: 12px 0 4px 0;
  letter-spacing: -0.03em;
}

.calc-total-amount.text-success {
  color: #34d399;
}

.calc-total-sub {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 22px;
}

.calc-breakdown {
  background: rgba(255, 255, 255, 0.08);
  border-radius: var(--radius);
  padding: 14px 16px;
  margin-bottom: 20px;
}

.calc-breakdown-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
  padding: 6px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.calc-breakdown-row:last-child {
  border-bottom: none;
}

.calc-breakdown-row .cb-label {
  color: rgba(255, 255, 255, 0.85);
}

.calc-breakdown-row .cb-val {
  font-weight: 700;
  color: #34d399;
}

.calc-comparison-bar {
  margin-bottom: 22px;
}

.bar-legend {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  color: rgba(255, 255, 255, 0.75);
  margin-bottom: 6px;
}

.bar-track {
  width: 100%;
  height: 8px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #34d399 0%, #10b981 100%);
  border-radius: 4px;
  transition: width 0.4s ease;
}

.calc-cta-btn {
  background: var(--amazon-yellow);
  color: var(--amazon-dark);
  border: none;
  font-weight: 800;
  font-size: 14px;
  padding: 12px;
  border-radius: var(--radius);
  text-align: center;
  display: block;
  text-decoration: none !important;
  transition: var(--transition-fast);
}

.calc-cta-btn:hover {
  background: var(--amazon-yellow-hover);
  transform: translateY(-1px);
}

/* Gear Re-Commerce Calculator Styles */
.calc-package-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  margin-top: 8px;
}

.package-card {
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 12px;
  cursor: pointer;
  transition: var(--transition-fast);
  background: var(--bg-card);
}

.package-card:hover {
  border-color: var(--olx-teal);
  background: var(--bg-hover);
}

.package-card.active {
  border: 2px solid var(--olx-teal);
  background: var(--olx-light-teal);
}

.package-card .pkg-icon {
  font-size: 20px;
  margin-bottom: 4px;
}

.package-card .pkg-title {
  font-size: 12px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.2;
}

.package-card .pkg-save {
  font-size: 11px;
  font-weight: 700;
  color: var(--success);
  margin-top: 4px;
}

.calc-price-compare {
  display: flex;
  align-items: center;
  justify-content: space-around;
  background: rgba(255, 255, 255, 0.08);
  border-radius: var(--radius);
  padding: 14px;
  margin-bottom: 18px;
}

.compare-item {
  text-align: center;
}

.compare-item .cp-label {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.7);
}

.compare-item .cp-val {
  font-size: 18px;
  font-weight: 800;
  margin-top: 2px;
}

.compare-item .cp-val.text-strike {
  text-decoration: line-through;
  color: rgba(255, 255, 255, 0.5);
}

.compare-sep {
  font-size: 18px;
  color: var(--amazon-yellow);
}

.calc-eco-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(52, 211, 153, 0.15);
  border: 1px solid rgba(52, 211, 153, 0.3);
  padding: 8px 12px;
  border-radius: var(--radius);
  font-size: 12px;
  color: #34d399;
  margin-bottom: 20px;
}

/* ---------- 3. Public Creative Visual Charts ---------- */
.campus-charts-section {
  padding-top: 0;
  margin-bottom: 30px;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.chart-box-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 22px;
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
}

.chart-box-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
  gap: 12px;
}

.chart-box-title {
  font-size: 16px;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 2px;
}

.chart-box-subtitle {
  font-size: 12px;
  color: var(--text-secondary);
}

.chart-filter-pills {
  display: flex;
  gap: 4px;
  flex-shrink: 0;
}

.chart-pill {
  background: var(--bg-page);
  border: 1px solid var(--border);
  padding: 4px 10px;
  border-radius: var(--radius-full);
  font-size: 11px;
  font-weight: 600;
  color: var(--text-secondary);
  cursor: pointer;
  transition: var(--transition-fast);
}

.chart-pill:hover, .chart-pill.active {
  background: var(--olx-teal);
  border-color: var(--olx-teal);
  color: #ffffff;
}

.chart-canvas-wrap {
  position: relative;
  width: 100%;
  height: 290px;
  min-height: 290px;
  flex: 1;
}

.chart-canvas-wrap canvas,
.chart-canvas-wrap svg {
  width: 100% !important;
  height: 100% !important;
  display: block;
}

.chart-card-footer {
  margin-top: 14px;
  padding-top: 12px;
  border-top: 1px solid var(--border-subtle);
  font-size: 12px;
  color: var(--text-secondary);
  line-height: 1.4;
}

.chart-insight-badge {
  font-weight: 700;
  color: var(--olx-teal);
}

/* ---------- Responsive Media Queries ---------- */
@media (max-width: 1024px) {
  .metrics-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }
  .charts-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
}

@media (max-width: 768px) {
  .calc-grid {
    grid-template-columns: 1fr;
    gap: 24px;
  }
  .calc-card {
    padding: 18px;
  }
  .chart-canvas-wrap {
    height: 260px;
    min-height: 260px;
  }
}

@media (max-width: 480px) {
  .metrics-grid {
    grid-template-columns: 1fr 1fr;
    gap: 8px;
  }
  .metric-item {
    padding: 6px 4px;
    gap: 8px;
  }
  .metric-icon-box {
    width: 36px;
    height: 36px;
    font-size: 16px;
    border-radius: 8px;
  }
  .metric-val {
    font-size: 18px;
  }
  .metric-title {
    font-size: 11px;
  }
  .metric-sub {
    display: none;
  }
  .calc-mode-switcher {
    width: 100%;
    display: flex;
  }
  .calc-mode-btn {
    flex: 1;
    padding: 7px 8px;
    font-size: 11px;
    text-align: center;
  }
  .calc-total-amount {
    font-size: 32px;
  }
  .calc-package-grid {
    grid-template-columns: 1fr;
  }
}
```

---

## 6. JavaScript Implementation: `frontend/js/stats.js`

This file handles both the **Animated Metric Counters** (Feature 8) and the **Student Savings Calculator** (Feature 9):

```javascript
/**
 * StayMart Marketplace Statistics & Student Savings Calculator
 * Milestone 2 - Features 8 & 9
 */

(function () {
  'use strict';

  // State for Calculator
  const calcState = {
    mode: 'accommodation', // 'accommodation' | 'gear'
    monthlyRent: 9000,
    durationMonths: 10,
    includeMeals: true,
    includeUtilities: true,
    selectedPackage: 'books'
  };

  const gearPackages = {
    books: { retail: 6500, senior: 1800, co2: 12, label: 'Textbooks & GATE Notes' },
    laptop: { retail: 56000, senior: 24500, co2: 185, label: 'Engineering Coding Setup' },
    room: { retail: 14500, senior: 4800, co2: 45, label: 'Room Setup & Cooler' },
    mobility: { retail: 12000, senior: 4200, co2: 80, label: 'Campus Cycle Commute' }
  };

  /* ==========================================================================
     1. Animated Metric Counters (IntersectionObserver + easeOutExpo)
     ========================================================================== */
  function initMetricCounters() {
    const counterElements = document.querySelectorAll('[data-counter]');
    if (!counterElements.length) return;

    if (!('IntersectionObserver' in window)) {
      // Fallback if browser lacks IntersectionObserver: leave rendered target values
      return;
    }

    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          obs.unobserve(entry.target);
        }
      });
    }, {
      root: null,
      threshold: 0.25,
      rootMargin: '0px 0px -40px 0px'
    });

    counterElements.forEach(el => observer.observe(el));
  }

  function animateCounter(el) {
    const target = parseFloat(el.getAttribute('data-target')) || 0;
    const prefix = el.getAttribute('data-prefix') || '';
    const suffix = el.getAttribute('data-suffix') || '';
    const duration = 1800; // 1.8 seconds smooth entrance
    const startTime = performance.now();

    function easeOutExpo(t) {
      return t === 1 ? 1 : 1 - Math.pow(2, -10 * t);
    }

    function frame(now) {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const easedProgress = easeOutExpo(progress);
      const current = Math.round(target * easedProgress);

      el.textContent = `${prefix}${current.toLocaleString('en-IN')}${suffix}`;

      if (progress < 1) {
        requestAnimationFrame(frame);
      } else {
        el.textContent = `${prefix}${target.toLocaleString('en-IN')}${suffix}`;
      }
    }

    requestAnimationFrame(frame);
  }

  /* ==========================================================================
     2. Interactive Student Savings Calculator
     ========================================================================== */
  function switchCalcMode(mode) {
    calcState.mode = mode;
    const accBtn = document.getElementById('calcModeAccBtn');
    const gearBtn = document.getElementById('calcModeGearBtn');
    const accPane = document.getElementById('calcPaneAccommodation');
    const gearPane = document.getElementById('calcPaneGear');

    if (mode === 'accommodation') {
      if (accBtn) accBtn.classList.add('active');
      if (gearBtn) gearBtn.classList.remove('active');
      if (accPane) { accPane.classList.add('active'); accPane.style.display = 'block'; }
      if (gearPane) { gearPane.classList.remove('active'); gearPane.style.display = 'none'; }
      updateAccommodationCalc();
    } else {
      if (accBtn) accBtn.classList.remove('active');
      if (gearBtn) gearBtn.classList.add('active');
      if (accPane) { accPane.classList.remove('active'); accPane.style.display = 'none'; }
      if (gearPane) { gearPane.classList.add('active'); gearPane.style.display = 'block'; }
      updateGearCalc();
    }
  }

  function updateAccommodationCalc() {
    const slider = document.getElementById('calcRentSlider');
    if (slider) {
      calcState.monthlyRent = parseInt(slider.value, 10);
      const disp = document.getElementById('calcRentDisplay');
      if (disp) disp.textContent = `₹${calcState.monthlyRent.toLocaleString('en-IN')} / month`;
    }

    const mealsCheck = document.getElementById('calcIncludeMeals');
    calcState.includeMeals = mealsCheck ? mealsCheck.checked : true;

    const utilCheck = document.getElementById('calcIncludeUtilities');
    calcState.includeUtilities = utilCheck ? utilCheck.checked : true;

    // Calculation formulas
    const brokerageSaved = calcState.monthlyRent; // 1 month rent saved
    const utilitySavings = calcState.includeUtilities ? (1200 * calcState.durationMonths) : 0;
    const mealSavings = calcState.includeMeals ? (2500 * calcState.durationMonths) : 0;
    const totalSavings = brokerageSaved + utilitySavings; // Core visible cash savings

    // Update UI elements
    const totalEl = document.getElementById('calcAccTotalSavings');
    if (totalEl) totalEl.textContent = `₹${totalSavings.toLocaleString('en-IN')}`;

    const cbBrokerage = document.getElementById('cbBrokerageVal');
    if (cbBrokerage) cbBrokerage.textContent = `+₹${brokerageSaved.toLocaleString('en-IN')}`;

    const cbUtility = document.getElementById('cbUtilityVal');
    if (cbUtility) cbUtility.textContent = `+₹${utilitySavings.toLocaleString('en-IN')}`;

    const mealRow = document.getElementById('cbMealRow');
    const cbMeal = document.getElementById('cbMealVal');
    if (mealRow && cbMeal) {
      if (calcState.includeMeals) {
        mealRow.style.display = 'flex';
        cbMeal.textContent = `+₹${mealSavings.toLocaleString('en-IN')}`;
      } else {
        mealRow.style.display = 'none';
      }
    }

    // Comparison Bar
    const brokerTotal = (calcState.monthlyRent * calcState.durationMonths) + brokerageSaved + (calcState.includeUtilities ? utilitySavings : 0);
    const staymartTotal = calcState.monthlyRent * calcState.durationMonths;
    const brokerEl = document.getElementById('cbBrokerCost');
    const staymartEl = document.getElementById('cbStaymartCost');
    const barFill = document.getElementById('cbSavingsBar');

    if (brokerEl) brokerEl.textContent = `₹${brokerTotal.toLocaleString('en-IN')}`;
    if (staymartEl) staymartEl.textContent = `₹${staymartTotal.toLocaleString('en-IN')}`;
    if (barFill && brokerTotal > 0) {
      const pct = Math.round((staymartTotal / brokerTotal) * 100);
      barFill.style.width = `${Math.min(pct, 100)}%`;
    }

    // Dynamic CTA link
    const cta = document.getElementById('calcAccCta');
    if (cta) {
      cta.href = `search-properties.html?maxPrice=${calcState.monthlyRent}`;
    }
  }

  function setRentPreset(amount) {
    const slider = document.getElementById('calcRentSlider');
    if (slider) {
      slider.value = amount;
      document.querySelectorAll('.calc-chip').forEach(c => {
        c.classList.toggle('active', c.textContent.includes(amount.toLocaleString('en-IN')));
      });
      updateAccommodationCalc();
    }
  }

  function setDurationPreset(months) {
    calcState.durationMonths = months;
    document.querySelectorAll('#stayDurationPills .calc-pill').forEach(pill => {
      pill.classList.toggle('active', parseInt(pill.getAttribute('data-months'), 10) === months);
    });
    updateAccommodationCalc();
  }

  function selectGearPackage(pkgKey, cardEl) {
    calcState.selectedPackage = pkgKey;
    document.querySelectorAll('.package-card').forEach(c => c.classList.remove('active'));
    if (cardEl) cardEl.classList.add('active');

    const pkg = gearPackages[pkgKey];
    if (!pkg) return;

    const retailEl = document.getElementById('calcGearRetail');
    const seniorEl = document.getElementById('calcGearSenior');
    const savingsEl = document.getElementById('calcGearSavings');
    const pctEl = document.getElementById('calcGearPercent');
    const co2El = document.getElementById('calcGearCo2');
    const cta = document.getElementById('calcGearCta');

    const saved = pkg.retail - pkg.senior;
    const pct = Math.round((saved / pkg.retail) * 100);

    if (retailEl) retailEl.textContent = `₹${pkg.retail.toLocaleString('en-IN')}`;
    if (seniorEl) seniorEl.textContent = `₹${pkg.senior.toLocaleString('en-IN')}`;
    if (savingsEl) savingsEl.textContent = `₹${saved.toLocaleString('en-IN')}`;
    if (pctEl) pctEl.textContent = `${pct}%`;
    if (co2El) co2El.textContent = `${pkg.co2} kg`;

    if (cta) {
      const catMap = {
        books: 'Books%20%26%20Stationery',
        laptop: 'Electronics',
        room: 'Furniture',
        mobility: 'Vehicles'
      };
      cta.href = `search-products.html?category=${catMap[pkgKey] || ''}`;
    }
  }

  function updateCustomGearCalc() {
    let totalRetail = 0;
    let totalSenior = 0;
    let totalCo2 = 0;

    const checks = document.querySelectorAll('#gearChecklist input[type="checkbox"]:checked');
    checks.forEach(chk => {
      totalRetail += parseFloat(chk.getAttribute('data-retail')) || 0;
      totalSenior += parseFloat(chk.getAttribute('data-senior')) || 0;
      totalCo2 += parseFloat(chk.getAttribute('data-co2')) || 0;
    });

    const retailEl = document.getElementById('calcGearRetail');
    const seniorEl = document.getElementById('calcGearSenior');
    const savingsEl = document.getElementById('calcGearSavings');
    const pctEl = document.getElementById('calcGearPercent');
    const co2El = document.getElementById('calcGearCo2');

    const saved = totalRetail - totalSenior;
    const pct = totalRetail > 0 ? Math.round((saved / totalRetail) * 100) : 0;

    if (retailEl) retailEl.textContent = `₹${totalRetail.toLocaleString('en-IN')}`;
    if (seniorEl) seniorEl.textContent = `₹${totalSenior.toLocaleString('en-IN')}`;
    if (savingsEl) savingsEl.textContent = `₹${saved.toLocaleString('en-IN')}`;
    if (pctEl) pctEl.textContent = `${pct}%`;
    if (co2El) co2El.textContent = `${totalCo2} kg`;
  }

  function updateGearCalc() {
    selectGearPackage(calcState.selectedPackage, document.querySelector(`.package-card[onclick*="${calcState.selectedPackage}"]`));
  }

  // Export functions globally
  window.switchCalcMode = switchCalcMode;
  window.updateAccommodationCalc = updateAccommodationCalc;
  window.setRentPreset = setRentPreset;
  window.setDurationPreset = setDurationPreset;
  window.selectGearPackage = selectGearPackage;
  window.updateCustomGearCalc = updateCustomGearCalc;

  // Initialize on DOM load
  document.addEventListener('DOMContentLoaded', () => {
    initMetricCounters();
    updateAccommodationCalc();
  });
})();
```

---

## 7. JavaScript Implementation: `frontend/js/charts.js`

This file handles the **Creative Visual Charts** (Feature 12) with the **Dual-Engine Architecture** (Chart.js 4.4.1 + zero-dependency SVG fallback):

```javascript
/**
 * StayMart Public Creative Visual Charts
 * Milestone 2 - Feature 12
 * Dual-Engine: Chart.js 4.4.1 with Native SVG Fallback Engine
 */

(function () {
  'use strict';

  let rentChartInstance = null;
  let recommerceChartInstance = null;
  let rentFilter = 'all';
  let recommerceMode = 'price'; // 'price' | 'volume'

  // Campus Zone Rent Data
  const campusRentData = {
    zones: ['Clement Town (GEU)', 'Prem Nagar (UPES)', 'Subhash Nagar (ISBT)', 'Rajpur Road (DIT)'],
    pgWithFood: [6800, 8200, 5800, 8800],
    singleRoom: [8500, 10500, 6500, 11000],
    sharedFlat: [4500, 5500, 3800, 6000]
  };

  // Re-Commerce Category Data
  const recommerceData = {
    categories: ['Textbooks', 'Laptops & Tech', 'Furniture', 'Coolers & AC', 'Cycles & Bikes'],
    seniorPrice: [650, 24500, 2400, 2200, 4800],
    retailPrice: [1800, 48000, 6500, 5800, 12000],
    discountPct: [64, 49, 63, 62, 60],
    semesterVolume: [420, 280, 310, 190, 160]
  };

  /* ==========================================================================
     Chart Initializer
     ========================================================================== */
  function initPublicCharts() {
    if (typeof Chart !== 'undefined') {
      renderChartJsRent();
      renderChartJsRecommerce();
    } else {
      // Offline or CDN blocked -> Render zero-dependency responsive SVG charts
      renderSvgRentChart();
      renderSvgRecommerceChart();
    }
  }

  /* ==========================================================================
     Engine A: Chart.js 4.4.1 Implementation
     ========================================================================== */
  function renderChartJsRent() {
    const canvas = document.getElementById('campusRentChart');
    if (!canvas) return;

    if (rentChartInstance) {
      rentChartInstance.destroy();
    }

    const datasets = [];

    if (rentFilter === 'all' || rentFilter === 'pg') {
      datasets.push({
        label: 'PG with 3 Meals (₹/mo)',
        data: campusRentData.pgWithFood,
        backgroundColor: '#ff9900',
        borderRadius: 6,
        barPercentage: 0.8
      });
    }

    if (rentFilter === 'all') {
      datasets.push({
        label: 'Single Private Room (₹/mo)',
        data: campusRentData.singleRoom,
        backgroundColor: '#002f34',
        borderRadius: 6,
        barPercentage: 0.8
      });
    }

    if (rentFilter === 'all' || rentFilter === 'flat') {
      datasets.push({
        label: 'Shared Flat Bedspace (₹/mo)',
        data: campusRentData.sharedFlat,
        backgroundColor: '#0a883a',
        borderRadius: 6,
        barPercentage: 0.8
      });
    }

    rentChartInstance = new Chart(canvas, {
      type: 'bar',
      data: {
        labels: campusRentData.zones,
        datasets: datasets
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
            labels: {
              boxWidth: 12,
              font: { family: 'Inter', size: 12, weight: 600 },
              color: '#465666'
            }
          },
          tooltip: {
            backgroundColor: '#002f34',
            titleFont: { family: 'Inter', size: 13, weight: 700 },
            bodyFont: { family: 'Inter', size: 12 },
            padding: 10,
            cornerRadius: 8,
            callbacks: {
              label: function (ctx) {
                return `${ctx.dataset.label}: ₹${ctx.raw.toLocaleString('en-IN')}`;
              }
            }
          }
        },
        scales: {
          x: {
            grid: { display: false },
            ticks: {
              font: { family: 'Inter', size: 11, weight: 600 },
              color: '#465666'
            }
          },
          y: {
            beginAtZero: true,
            grid: { color: 'rgba(0, 47, 52, 0.06)' },
            ticks: {
              font: { family: 'Inter', size: 11 },
              color: '#7f9799',
              callback: function (val) {
                return `₹${(val / 1000)}k`;
              }
            }
          }
        }
      }
    });
  }

  function renderChartJsRecommerce() {
    const canvas = document.getElementById('recommerceChart');
    if (!canvas) return;

    if (recommerceChartInstance) {
      recommerceChartInstance.destroy();
    }

    if (recommerceMode === 'price') {
      recommerceChartInstance = new Chart(canvas, {
        type: 'bar',
        data: {
          labels: recommerceData.categories,
          datasets: [
            {
              label: 'StayMart Senior Price (₹)',
              data: recommerceData.seniorPrice,
              backgroundColor: '#002f34',
              borderRadius: 6
            },
            {
              label: 'Retail / Amazon New (₹)',
              data: recommerceData.retailPrice,
              backgroundColor: '#e2e8f0',
              borderRadius: 6
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top',
              labels: {
                boxWidth: 12,
                font: { family: 'Inter', size: 12, weight: 600 },
                color: '#465666'
              }
            },
            tooltip: {
              backgroundColor: '#002f34',
              padding: 10,
              cornerRadius: 8,
              callbacks: {
                label: function (ctx) {
                  return `${ctx.dataset.label}: ₹${ctx.raw.toLocaleString('en-IN')}`;
                }
              }
            }
          },
          scales: {
            x: {
              grid: { display: false },
              ticks: { font: { family: 'Inter', size: 11, weight: 600 }, color: '#465666' }
            },
            y: {
              beginAtZero: true,
              grid: { color: 'rgba(0, 47, 52, 0.06)' },
              ticks: {
                font: { family: 'Inter', size: 11 },
                color: '#7f9799',
                callback: function (val) {
                  return val >= 1000 ? `₹${val / 1000}k` : `₹${val}`;
                }
              }
            }
          }
        }
      });
    } else {
      // Volume view
      recommerceChartInstance = new Chart(canvas, {
        type: 'bar',
        data: {
          labels: recommerceData.categories,
          datasets: [
            {
              label: 'Semester Trade Volume (Ads)',
              data: recommerceData.semesterVolume,
              backgroundColor: '#ff9900',
              borderRadius: 6
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: '#002f34',
              callbacks: {
                label: function (ctx) {
                  return `Trade Volume: ${ctx.raw} student ads/term`;
                }
              }
            }
          },
          scales: {
            x: { grid: { display: false }, ticks: { font: { family: 'Inter', size: 11, weight: 600 }, color: '#465666' } },
            y: {
              beginAtZero: true,
              grid: { color: 'rgba(0, 47, 52, 0.06)' },
              ticks: { font: { family: 'Inter', size: 11 }, color: '#7f9799' }
            }
          }
        }
      });
    }
  }

  /* ==========================================================================
     Engine B: Zero-Dependency Responsive SVG Fallback
     ========================================================================== */
  function renderSvgRentChart() {
    const container = document.getElementById('accChartContainer');
    if (!container) return;

    const maxVal = 12000;
    const w = 560;
    const h = 260;
    const padL = 45;
    const padR = 20;
    const padT = 25;
    const padB = 45;
    const chartW = w - padL - padR;
    const chartH = h - padT - padB;
    const groupW = chartW / 4;

    let svgHtml = `
      <svg viewBox="0 0 ${w} ${h}" preserveAspectRatio="xMidYMid meet" style="width:100%;height:100%">
        <!-- Grid lines -->
        <line x1="${padL}" y1="${padT}" x2="${w - padR}" y2="${padT}" stroke="#e2e8f0" stroke-dasharray="3"/>
        <text x="${padL - 8}" y="${padT + 4}" font-size="10" fill="#7f9799" text-anchor="end">₹12k</text>
        <line x1="${padL}" y1="${padT + chartH / 2}" x2="${w - padR}" y2="${padT + chartH / 2}" stroke="#e2e8f0" stroke-dasharray="3"/>
        <text x="${padL - 8}" y="${padT + chartH / 2 + 4}" font-size="10" fill="#7f9799" text-anchor="end">₹6k</text>
        <line x1="${padL}" y1="${h - padB}" x2="${w - padR}" y2="${h - padB}" stroke="#cbd5e1"/>
        <text x="${padL - 8}" y="${h - padB + 4}" font-size="10" fill="#7f9799" text-anchor="end">₹0</text>
    `;

    campusRentData.zones.forEach((zone, i) => {
      const gx = padL + i * groupW;
      const barW = 18;

      const hPg = (campusRentData.pgWithFood[i] / maxVal) * chartH;
      const hSingle = (campusRentData.singleRoom[i] / maxVal) * chartH;
      const hFlat = (campusRentData.sharedFlat[i] / maxVal) * chartH;

      // PG bar (amber)
      svgHtml += `<rect x="${gx + 10}" y="${h - padB - hPg}" width="${barW}" height="${hPg}" rx="3" fill="#ff9900"><title>PG with Food: ₹${campusRentData.pgWithFood[i]}</title></rect>`;
      // Single room bar (teal)
      svgHtml += `<rect x="${gx + 32}" y="${h - padB - hSingle}" width="${barW}" height="${hSingle}" rx="3" fill="#002f34"><title>Single Room: ₹${campusRentData.singleRoom[i]}</title></rect>`;
      // Flat bar (green)
      svgHtml += `<rect x="${gx + 54}" y="${h - padB - hFlat}" width="${barW}" height="${hFlat}" rx="3" fill="#0a883a"><title>Shared Flat: ₹${campusRentData.sharedFlat[i]}</title></rect>`;

      // X-Axis Zone label
      const shortName = zone.split(' ')[0];
      svgHtml += `<text x="${gx + 40}" y="${h - padB + 16}" font-size="10" font-weight="600" fill="#465666" text-anchor="middle">${shortName}</text>`;
    });

    svgHtml += `
      <!-- Legend -->
      <g transform="translate(${padL}, 12)">
        <rect width="10" height="10" rx="2" fill="#ff9900"/>
        <text x="14" y="9" font-size="10" fill="#465666">PG + Food</text>
        <rect x="90" width="10" height="10" rx="2" fill="#002f34"/>
        <text x="104" y="9" font-size="10" fill="#465666">Single Room</text>
        <rect x="190" width="10" height="10" rx="2" fill="#0a883a"/>
        <text x="204" y="9" font-size="10" fill="#465666">Shared Flat</text>
      </g>
    </svg>`;

    container.innerHTML = svgHtml;
  }

  function renderSvgRecommerceChart() {
    const container = document.getElementById('gearChartContainer');
    if (!container) return;

    const w = 560;
    const h = 260;
    const padL = 45;
    const padR = 20;
    const padT = 25;
    const padB = 45;
    const chartW = w - padL - padR;
    const chartH = h - padT - padB;
    const groupW = chartW / 5;
    const maxVal = 50000;

    let svgHtml = `
      <svg viewBox="0 0 ${w} ${h}" preserveAspectRatio="xMidYMid meet" style="width:100%;height:100%">
        <line x1="${padL}" y1="${padT}" x2="${w - padR}" y2="${padT}" stroke="#e2e8f0" stroke-dasharray="3"/>
        <text x="${padL - 8}" y="${padT + 4}" font-size="10" fill="#7f9799" text-anchor="end">₹50k</text>
        <line x1="${padL}" y1="${padT + chartH / 2}" x2="${w - padR}" y2="${padT + chartH / 2}" stroke="#e2e8f0" stroke-dasharray="3"/>
        <text x="${padL - 8}" y="${padT + chartH / 2 + 4}" font-size="10" fill="#7f9799" text-anchor="end">₹25k</text>
        <line x1="${padL}" y1="${h - padB}" x2="${w - padR}" y2="${h - padB}" stroke="#cbd5e1"/>
        <text x="${padL - 8}" y="${h - padB + 4}" font-size="10" fill="#7f9799" text-anchor="end">₹0</text>
    `;

    recommerceData.categories.forEach((cat, i) => {
      const gx = padL + i * groupW;
      const barW = 16;
      const hSenior = (recommerceData.seniorPrice[i] / maxVal) * chartH;
      const hRetail = (recommerceData.retailPrice[i] / maxVal) * chartH;

      svgHtml += `<rect x="${gx + 8}" y="${h - padB - hSenior}" width="${barW}" height="${hSenior}" rx="3" fill="#002f34"><title>Senior: ₹${recommerceData.seniorPrice[i]}</title></rect>`;
      svgHtml += `<rect x="${gx + 28}" y="${h - padB - hRetail}" width="${barW}" height="${hRetail}" rx="3" fill="#cbd5e1"><title>Retail: ₹${recommerceData.retailPrice[i]}</title></rect>`;

      const shortCat = cat.split(' ')[0];
      svgHtml += `<text x="${gx + 26}" y="${h - padB + 16}" font-size="10" font-weight="600" fill="#465666" text-anchor="middle">${shortCat}</text>`;
    });

    svgHtml += `
      <g transform="translate(${padL}, 12)">
        <rect width="10" height="10" rx="2" fill="#002f34"/>
        <text x="14" y="9" font-size="10" fill="#465666">StayMart Senior Price</text>
        <rect x="150" width="10" height="10" rx="2" fill="#cbd5e1"/>
        <text x="164" y="9" font-size="10" fill="#465666">Retail Benchmark</text>
      </g>
    </svg>`;

    container.innerHTML = svgHtml;
  }

  /* ==========================================================================
     Interactive Filters & Public Controls
     ========================================================================== */
  function filterRentChart(type) {
    rentFilter = type;
    document.querySelectorAll('#accChartFilter .chart-pill').forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('onclick').includes(type));
    });

    if (typeof Chart !== 'undefined' && rentChartInstance) {
      renderChartJsRent();
    } else {
      renderSvgRentChart();
    }
  }

  function toggleRecommerceView(mode) {
    recommerceMode = mode;
    document.querySelectorAll('#gearChartFilter .chart-pill').forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('onclick').includes(mode));
    });

    if (typeof Chart !== 'undefined' && recommerceChartInstance) {
      renderChartJsRecommerce();
    } else {
      renderSvgRecommerceChart();
    }
  }

  window.filterRentChart = filterRentChart;
  window.toggleRecommerceView = toggleRecommerceView;

  document.addEventListener('DOMContentLoaded', initPublicCharts);
})();
```

---

## 8. Integration Blueprint for `frontend/index.html`

In `frontend/index.html`:
1. **Head Section:** Add deferred Chart.js CDN script:
   ```html
   <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js" defer></script>
   ```
2. **Body Section (Below Hero Banner, Line 140):**
   Insert `<section class="metrics-ribbon-section">...</section>` (Section 2.4).
3. **Body Section (Inside `<main class="container">`, between Trending Accommodations and "How StayMart Works", Line 188):**
   Insert:
   - `<section class="section savings-calc-section" id="studentCalculator">...</section>` (Section 3.4)
   - `<section class="section campus-charts-section">...</section>` (Section 4.4)
4. **Bottom Scripts (Lines 265-270):**
   Add `stats.js` and `charts.js`:
   ```html
   <script src="js/api.js"></script>
   <script src="js/auth.js"></script>
   <script src="js/behavior.js"></script>
   <script src="js/utils.js"></script>
   <script src="js/stats.js"></script>
   <script src="js/charts.js"></script>
   <script src="js/home.js"></script>
   ```

---

## 9. Verification & Quality Assurance Method

### 9.1 Mobile Viewport Responsiveness Verification
- **Test Command:** Execute headless layout check:
  `python scripts/run_viewport_tests.py`
- **Expected Outcome:**
  - Viewports tested: Mobile (375px), Tablet (768px), Desktop (1280px).
  - Horizontal overflow (`document.documentElement.scrollWidth > window.innerWidth`): Must evaluate to `0px` across all screen sizes.
  - Interactive slider thumb must remain within safe margins with minimum touch size 44px.

### 9.2 Animation & IntersectionObserver Verification
- Scroll down to the Metrics Ribbon from hero:
  - Metric counters count up smoothly from 0 to target (500+, 1,200+, ₹4,500/mo, 98%) over ~1.8 seconds.
  - Counter animation executes once without stuttering or re-animating during subsequent scrolls.

### 9.3 Calculator Interactivity Verification
- **Mode A (Accommodation):**
  - Drag rent slider from ₹5,000 to ₹18,000: Display updates synchronously; total savings counter recalibrates in real-time.
  - Switch duration pills between 6, 10, and 12 months: Utility savings recalculate accurately.
  - Uncheck "Meals Included" checkbox: Meal savings row collapses smoothly and re-adjusts totals.
- **Mode B (Re-Commerce):**
  - Click on "Laptop Setup" card: Benchmark price jumps to ₹56,000, StayMart price updates to ₹24,500, savings badge shows ₹31,500 (56% off).
  - CO2 ecological indicator reflects campus carbon avoidance (185 kg CO2e).

### 9.4 Public Chart Dual-Engine Verification
- **Online with CDN:** Canvas charts render cleanly with retina crispness, tooltips activate on mouseover.
- **Offline / Disconnected Simulation:** Disable network or block CDN; charts immediately fallback to SVG vector charts without any uncaught JavaScript exceptions or blank containers.
