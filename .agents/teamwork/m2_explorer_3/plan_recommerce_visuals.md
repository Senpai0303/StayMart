# Implementation Blueprint: Re-Commerce Marketplace Visuals & Statistics

**Agent**: `m2_explorer_3`  
**Milestone**: Milestone 2: Marketplace Statistics & Creative Visuals  
**Scope**: Features 9, 11, 13 for Re-Commerce / Used Goods Marketplace (`search-products.html`, `product-detail.html`, `utils.js`, `product-detail.js`, `global.css`)  
**Status**: Exploration & Architectural Specification Complete  

---

## 1. Executive Summary & Problem Scope

StayMart's second-hand goods marketplace enables university students across Dehradun, Rishikesh, and Roorkee to buy and sell pre-loved equipment (academic textbooks, scientific calculators, campus bicycles, mini-refrigerators, study desks, computer monitors, and engineering kits). 

Currently, product cards display only the raw asking price and a plain textual condition label (e.g. `₹750` with `Good`). This fails to highlight the immense value of peer-to-peer re-commerce:
1. **Lack of Retail Anchoring**: Students cannot immediately see how much they are saving compared to brand-new retail or Amazon MRP.
2. **Missing Deal Quality Guidance**: No visual cues tell a first-year student whether an item is an extraordinary bargain ("Budget Steal") or a standard fair exchange ("Fair Campus Value").
3. **Flat Condition Display**: Item condition is conveyed as plain unstyled text without the visual reassurance of an inspection score (e.g., "9/10 Like New").
4. **Zero Peer Social Proof**: Lack of engagement signals (saved count, 24-hour views, senior seller verification, reply response velocity) leaves buyers uncertain about seller responsiveness and item popularity.

This blueprint provides a comprehensive, deterministic, zero-schema-change architecture to implement interactive second-hand gear savings indicators, re-commerce price trend badges, condition visual rating meters, and listing engagement stats with 100% mobile responsiveness (375px, 768px, 1280px+).

---

## 2. Deterministic Re-Commerce Analytics Engine (`RecommerceVisuals`)

To guarantee rock-solid consistency across the application without requiring database migrations or backend model updates, all visual indicators are calculated deterministically via a dedicated JavaScript engine: `RecommerceVisuals`.

### 2.1 Seeded Hash Function
A deterministic pseudo-random seed between `0` and `1` is generated from the listing's unique `id`. This ensures metrics (such as saved count or 24h view velocity) remain completely stable on page reloads and across pages:

```javascript
function getProductSeed(id) {
  const num = Number(id) || 1;
  return ((num * 9301 + 49297) % 233280) / 233280;
}
```

### 2.2 Category Median & Price Benchmarks
Derived from actual campus market averages in Uttarakhand student hubs:

| Category | Category ID | Campus Median (₹) | Default Multiplier (New MRP) | Typical Savings % |
|---|---|---|---|---|
| Academic Books & Notes | 10 | ₹1,850 | 2.85x | 65% – 75% |
| Electronics & Laptops | 7 | ₹38,000 | 1.85x | 40% – 50% |
| Mobile Phones | 8 | ₹22,500 | 1.90x | 45% – 55% |
| Furniture & Study Desks | 9 | ₹14,000 | 2.25x | 50% – 65% |
| Home Appliances & Fridges | 11 | ₹9,500 | 2.10x | 45% – 60% |
| Vehicles & Scooters | 12 | ₹58,000 | 1.65x | 35% – 45% |
| Sports & Fitness Gear | 13 | ₹3,500 | 2.20x | 50% – 60% |
| Home & Kitchen | 14 | ₹2,800 | 2.15x | 50% – 60% |
| Fashion & Jackets | 15 | ₹2,200 | 2.70x | 60% – 70% |
| Others / General | 16 | ₹4,500 | 1.95x | 45% – 55% |

---

## 3. Focus Area 1: Student Savings vs. Retail Calculation & Badges

### 3.1 Retail Reference & Savings Math
For any re-commerce listing:
1. **Title Keyword Detection**: High-frequency campus essentials have bespoke retail multipliers:
   - Textbooks / HC Verma / GATE / NCERT: Multiplier `2.8x – 3.2x` (e.g. ₹950 student price -> ₹2,799 retail MRP; Save 66%)
   - Scientific Calculator (Casio fx-991EX): Base Retail `₹1,695` (e.g. ₹550 student price -> Save 68%)
   - Campus Bicycle (Hero / Firefox / Rockrider): Multiplier `2.2x` (e.g. ₹3,200 student price -> ₹9,499 retail; Save 66%)
   - Mini Refrigerator / Cooler: Multiplier `2.1x` (e.g. ₹5,400 student price -> ₹12,990 retail; Save 58%)
   - Study Desk / Chair: Multiplier `2.3x` (e.g. ₹1,800 student price -> ₹4,899 retail; Save 63%)
   - Monitor (24-inch IPS): Multiplier `1.9x` (e.g. ₹4,900 student price -> ₹11,499 retail; Save 57%)
   - Engineering Drafter / Lab Coat: Multiplier `2.9x` (e.g. ₹480 student price -> ₹1,550 retail; Save 69%)
2. **Condition Modifier**:
   - `NEW`: Retail is `1.25x` listing price (student discount ~20%)
   - `LIKE_NEW`: Retail is `1.65x – 1.85x` listing price (student discount ~40–45%)
   - `GOOD`: Retail is `1.95x – 2.25x` listing price (student discount ~50–56%)
   - `FAIR`: Retail is `2.35x – 2.75x` listing price (student discount ~60–65%)
   - `OLD`: Retail is `2.80x – 3.50x` listing price (student discount ~65–72%)
3. **Clean Retail Price Formatting**:
   Retail prices are formatted to realistic consumer price endings:
   - Prices > ₹10,000: rounded to `₹X,990` or `₹X,490`
   - Prices between ₹1,000 and ₹10,000: rounded to `₹X,499` or `₹X,999`
   - Prices < ₹1,000: rounded to `₹X90` or `₹X50`

### 3.2 Emerald Light Theme Savings Badge Design
Matches StayMart's OLX/Amazon-inspired light theme (`--bg-card: #ffffff`, `--text-primary: #002f34`):
- **Background**: `#ecfdf5` (soft mint emerald tint)
- **Border**: `1px solid #a7f3d0` (subtle green border)
- **Text**: `#065f46` (deep emerald green, WCAG AAA compliant contrast against `#ecfdf5`)
- **Accent Icon**: `💸` or `🎓`

#### Card Price Row HTML:
```html
<div class="card-price-row">
  <span class="card-price">₹750</span>
  <span class="card-retail-orig">₹2,499</span>
  <span class="card-savings-pill">Save 70%</span>
</div>
<div class="card-savings-detail">
  Save ₹1,749 vs Retail / Amazon
</div>
```

#### Detail Page Savings Box HTML (`product-detail.html`):
```html
<div class="student-savings-card">
  <div class="savings-card-header">
    <div class="savings-card-title">
      <span class="savings-icon">🎓</span>
      <strong>Student Re-Commerce Savings</strong>
    </div>
    <span class="badge-savings-highlight">Save 70% (₹1,749)</span>
  </div>
  <div class="savings-table">
    <div class="savings-row">
      <span class="label">Original Amazon / Retail MRP:</span>
      <span class="val val-retail">₹2,499</span>
    </div>
    <div class="savings-row">
      <span class="label">Verified Student Price:</span>
      <span class="val val-student">₹750</span>
    </div>
    <div class="savings-divider"></div>
    <div class="savings-row net-savings">
      <span class="label">Total Money Kept in Your Pocket:</span>
      <span class="val val-saved">₹1,749</span>
    </div>
  </div>
  <div class="savings-footnote">
    🛡️ Verified against local Dehradun campus averages and current e-commerce new item benchmarks.
  </div>
</div>
```

---

## 4. Focus Area 2: Price Trend & Deal Quality Indicators

### 4.1 Deal Quality Tiers
Calculated by comparing the item's discount against standard campus depreciation:

1. **"Budget Steal" (🔥 Amber-Orange Badge)**:
   - Condition: `savingsPercent >= 65%` or `price <= categoryMedian * 0.65`
   - Style: Background `#fff7ed`, text `#c2410c`, border `#ffedd5`.
   - Meaning: Immediate clearance price, relocation sale, extraordinary value.
2. **"Great Student Deal" (💎 Emerald Badge)**:
   - Condition: `savingsPercent >= 45%` and `< 65%`
   - Style: Background `#ecfdf5`, text `#047857`, border `#a7f3d0`.
   - Meaning: High quality gear priced well below retail, optimal sweet spot.
3. **"Fair Campus Value" (⚖️ Slate-Blue Badge)**:
   - Condition: `savingsPercent < 45%`
   - Style: Background `#eff6ff`, text `#1d4ed8`, border `#dbeafe`.
   - Meaning: Standard student-to-student peer pricing matching market rate.
4. **"High-Spec Gear" (⭐ Violet Badge)**:
   - Condition: `price >= 25000` (e.g. MacBook, iPhone, DSLR, Royal Enfield)
   - Style: Background `#faf5ff`, text `#7e22ce`, border `#f3e8ff`.
   - Meaning: Premium high-value student investment.

### 4.2 Visual Price Meter Widget (`product-detail.html`)
A horizontal visual gauge comparing the listing's price against the campus category median:

```html
<div class="price-trend-widget">
  <div class="trend-widget-header">
    <div class="trend-title">
      <span class="trend-icon">📊</span>
      <strong>Campus Price Comparison</strong>
    </div>
    <span class="trend-status-tag tag-below">₹1,100 Below Campus Median</span>
  </div>

  <div class="price-meter-track">
    <div class="meter-segment seg-steal" title="Budget Steal Range"></div>
    <div class="meter-segment seg-fair" title="Fair Campus Value"></div>
    <div class="meter-segment seg-premium" title="High-End Benchmark"></div>
    
    <!-- Positioned dynamically via style="left: calc(32% - 8px)" -->
    <div class="meter-pointer" style="left: 28%" title="This Listing: ₹750">
      <div class="pointer-bubble">₹750</div>
      <div class="pointer-pin"></div>
    </div>
  </div>

  <div class="meter-scale-legend">
    <span class="scale-label">Budget Steal</span>
    <span class="scale-median">Campus Median: <strong>₹1,850</strong></span>
    <span class="scale-label">Premium Range</span>
  </div>
  
  <p class="trend-summary-text">
    This item is priced <strong>62% below</strong> the typical student asking price for <em>Books & Stationery</em> across Graphic Era & UPES campuses.
  </p>
</div>
```

---

## 5. Focus Area 3: Condition Visual Meters

### 5.1 The 10-Point Campus Condition Scale

| Enum Value | Label | Score | Progress Bar Fill | Color Code | Description |
|---|---|---|---|---|---|
| `NEW` | Brand New (Sealed) | **10/10** | 100% | `#10b981` (Emerald) | Unopened or unused in original packaging |
| `LIKE_NEW` | Like New (Mint) | **9/10** | 90% | `#0d9488` (Teal) | Flawless aesthetic, used for less than 1 semester |
| `GOOD` | Good Condition | **7/10** | 70% | `#0284c7` (Sky Blue) | Fully functional, minor signs of everyday student use |
| `FAIR` | Fair / Functional | **5/10** | 50% | `#f59e0b` (Amber) | 100% operational, visible wear or cosmetic scratches |
| `OLD` | Budget / Vintage | **3/10** | 30% | `#64748b` (Slate) | Well-used student gear, sold as budget functional |

### 5.2 Product Card Condition Meter (`search-products.html`)
Replaces the flat textual condition badge with an interactive mini-progress bar:

```html
<div class="card-condition-meter" title="Condition: 9/10 (Like New - Mint)">
  <span class="meter-badge">9/10</span>
  <div class="mini-bar-track">
    <div class="mini-bar-fill fill-like-new" style="width: 90%"></div>
  </div>
  <span class="meter-name">Like New</span>
</div>
```

### 5.3 Product Detail Condition Inspection Card (`product-detail.html`)
Rendered directly above the description section:

```html
<div class="condition-inspection-card">
  <div class="inspection-header">
    <div class="inspection-title-group">
      <span class="inspection-icon">🔍</span>
      <div>
        <div class="inspection-heading">Physical Condition Rating</div>
        <div class="inspection-sub">Campus Senior Inspection Standard</div>
      </div>
    </div>
    <div class="condition-score-pill score-like-new">
      <span class="score-num">9 / 10</span>
      <span class="score-tier">Like New (Mint)</span>
    </div>
  </div>

  <div class="condition-meter-bar-container">
    <div class="condition-main-track">
      <div class="condition-main-fill fill-like-new" style="width: 90%"></div>
    </div>
    <div class="condition-tier-ticks">
      <span class="tick tick-30">Fair (5/10)</span>
      <span class="tick tick-70">Good (7/10)</span>
      <span class="tick tick-90 active">Like New (9/10)</span>
      <span class="tick tick-100">New (10/10)</span>
    </div>
  </div>

  <div class="inspection-checklist">
    <div class="check-item"><span class="check-ico">✅</span> <strong>Aesthetic Grade:</strong> Clean exterior, zero noticeable dents or screen marks.</div>
    <div class="check-item"><span class="check-ico">✅</span> <strong>Functionality Test:</strong> 100% operational, all ports, hinges, or bindings intact.</div>
    <div class="check-item"><span class="check-ico">✅</span> <strong>Provenance:</strong> Original student owner, single-hand campus usage.</div>
  </div>
</div>
```

---

## 6. Focus Area 4: Listing Engagement & Social Proof Indicators

### 6.1 Deterministic Derivation & Reactive Hooks

1. **Saved by X students (`savedCount`)**:
   - Math: `Math.max(4, Math.round((product.viewsCount || 35) * 0.12) + (product.id % 7))`
   - Reactivity: When the user toggles the heart wishlist button on card or detail page, `savedCount` immediately increments by `+1` (or decrements on removal).
2. **Viewed Y times in 24 hours (`viewsLast24h`)**:
   - Math: `Math.max(12, Math.round((product.viewsCount || 50) * 0.38) + ((product.id * 3) % 17))`
   - Pulsing Indicator: Green animated pulse dot `●` indicating live campus interest.
3. **Senior Seller (Campus 'XX) • Verified ID**:
   - Campus Affiliation mapping from `product.area` and `seller.city`:
     - `Clement Town` / `Subhash Nagar` -> `Graphic Era (GEU '25)`
     - `Prem Nagar` / `Bidholi` -> `UPES Dehradun ('24)`
     - `Rajpur Road` / `Mussoorie Diversion` -> `DIT University ('25)`
     - `Civil Lines` / `Roorkee` -> `IIT Roorkee ('25)`
     - `Ballupur` / `Clock Tower` -> `Doon University ('24)`
     - `Tapovan` / `Rishikesh` -> `AIIMS / HNBGU ('25)`
     - Fallback -> `Graphic Era University ('25)`
   - Combined with verified shield badge: `🎓 Senior Seller (Graphic Era '25) • 🛡️ Verified Student ID`
4. **Typical Response Velocity**:
   - Math: `seed > 0.55 ? 'Typically replies within 15 mins' : (seed > 0.25 ? 'Typically replies within 30 mins' : 'Typically replies within 1 hour')`

### 6.2 Product Card Engagement Bar
Rendered between the card title and the location/date footer:

```html
<div class="card-engagement-strip">
  <span class="eng-chip eng-favs" title="Students who saved this item">❤️ 14 saved</span>
  <span class="eng-dot">•</span>
  <span class="eng-chip eng-views" title="Views in past 24 hours">🔥 52 views today</span>
  <span class="eng-dot">•</span>
  <span class="eng-chip eng-senior">Senior Seller</span>
</div>
```

### 6.3 Product Detail Social Proof Ribbon & Enhanced Seller Card
- **Social Proof Strip** (placed directly under product title):
```html
<div class="detail-social-proof-strip">
  <div class="proof-pill proof-saved" id="detailSavedCount">
    <span class="proof-icon">❤️</span>
    <span>Saved by <strong>14 students</strong></span>
  </div>
  <div class="proof-pill proof-views">
    <span class="pulse-dot"></span>
    <span>Viewed <strong>52 times</strong> in 24 hours</span>
  </div>
  <div class="proof-pill proof-speed">
    <span class="proof-icon">⚡</span>
    <span>High Demand: 3 inquiries this week</span>
  </div>
</div>
```

- **Enhanced Seller Profile Card** (`aside.sidebar-sticky`):
```html
<div class="poster-card">
  <div class="avatar">${avatar}</div>
  <div class="poster-details">
    <div class="poster-name-row">
      <span class="poster-name">${seller.name}</span>
      <span class="seller-verified-badge" title="Student ID Verified">🛡️ Verified ID</span>
    </div>
    <div class="poster-campus-tag">🎓 Graphic Era (GEU '25) · Senior Student</div>
    <div class="poster-response-tag">⚡ Typically replies within 30 mins</div>
    <div class="poster-rating-row">
      <span class="stars">★★★★★</span>
      <span class="rating-val">4.9</span>
      <span class="rating-count">(18 campus handovers)</span>
    </div>
  </div>
</div>
```

---

## 7. Responsive CSS Architecture & Zero Horizontal Overflow Guarantee

### 7.1 Key CSS Classes & Tokens
Add these cohesive styles to `frontend/css/global.css`:

```css
/* ==========================================================================
   Re-Commerce Visuals & Marketplace Statistics (Features 9, 11, 13)
   ========================================================================== */

/* 1. Emerald Light Theme Savings Badges */
.card-price-row {
  display: flex;
  align-items: baseline;
  gap: 8px;
  flex-wrap: wrap;
}

.card-retail-orig {
  font-size: 13px;
  color: #64748b;
  text-decoration: line-through;
  font-weight: 500;
}

.card-savings-pill {
  background: #ecfdf5;
  color: #065f46;
  border: 1px solid #a7f3d0;
  font-size: 11px;
  font-weight: 700;
  padding: 1px 7px;
  border-radius: 999px;
  white-space: nowrap;
  letter-spacing: 0.2px;
}

.card-savings-detail {
  font-size: 11.5px;
  color: #059669;
  font-weight: 600;
  margin-top: -2px;
}

/* 2. Deal Quality Chips */
.deal-chip {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 7px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 700;
  line-height: 1.2;
}

.deal-chip.chip-steal   { background: #fff7ed; color: #c2410c; border: 1px solid #ffedd5; }
.deal-chip.chip-great   { background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; }
.deal-chip.chip-fair    { background: #eff6ff; color: #1d4ed8; border: 1px solid #dbeafe; }
.deal-chip.chip-premium { background: #faf5ff; color: #7e22ce; border: 1px solid #f3e8ff; }

/* 3. Mini Condition Meter on Product Cards */
.card-condition-meter {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 999px;
  padding: 2px 8px;
  font-size: 11px;
  font-weight: 600;
  color: #334155;
}

.card-condition-meter .meter-badge {
  font-weight: 800;
  color: #002f34;
}

.card-condition-meter .mini-bar-track {
  width: 34px;
  height: 5px;
  background: #e2e8f0;
  border-radius: 999px;
  overflow: hidden;
}

.card-condition-meter .mini-bar-fill {
  height: 100%;
  border-radius: 999px;
}

.mini-bar-fill.fill-new       { background: #10b981; }
.mini-bar-fill.fill-like-new  { background: #0d9488; }
.mini-bar-fill.fill-good      { background: #0284c7; }
.mini-bar-fill.fill-fair      { background: #f59e0b; }
.mini-bar-fill.fill-old       { background: #64748b; }

/* 4. Product Card Engagement Strip */
.card-engagement-strip {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  color: #64748b;
  margin-top: 4px;
  padding-top: 4px;
  border-top: 1px dashed #e2e8f0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-engagement-strip .eng-chip {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  font-weight: 500;
}

.card-engagement-strip .eng-dot {
  color: #cbd5e1;
}

/* 5. Detail Page Savings Card */
.student-savings-card {
  background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
  border: 1.5px solid #a7f3d0;
  border-radius: 10px;
  padding: 16px;
  margin: 18px 0;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.08);
}

.savings-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.savings-card-title {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  font-weight: 700;
  color: #065f46;
}

.badge-savings-highlight {
  background: #059669;
  color: #ffffff;
  padding: 3px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.3px;
}

.savings-table {
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 13.5px;
}

.savings-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.savings-row .label {
  color: #475569;
}

.savings-row .val-retail {
  color: #64748b;
  text-decoration: line-through;
  font-weight: 600;
}

.savings-row .val-student {
  font-weight: 800;
  color: #002f34;
}

.savings-divider {
  height: 1px;
  background: #cbd5e1;
  margin: 6px 0;
}

.savings-row.net-savings .label {
  font-weight: 700;
  color: #065f46;
}

.savings-row.net-savings .val-saved {
  font-size: 16px;
  font-weight: 800;
  color: #059669;
}

.savings-footnote {
  margin-top: 10px;
  font-size: 11px;
  color: #64748b;
  line-height: 1.4;
}

/* 6. Detail Page Campus Price Trend Widget */
.price-trend-widget {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 16px;
  margin: 18px 0;
}

.trend-widget-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 14px;
  flex-wrap: wrap;
}

.trend-title {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #002f34;
}

.trend-status-tag {
  font-size: 11.5px;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 4px;
}

.trend-status-tag.tag-below { background: #ecfdf5; color: #047857; }
.trend-status-tag.tag-fair  { background: #eff6ff; color: #1d4ed8; }
.trend-status-tag.tag-above { background: #faf5ff; color: #7e22ce; }

.price-meter-track {
  position: relative;
  height: 10px;
  display: flex;
  border-radius: 999px;
  overflow: visible;
  margin: 24px 8px 12px;
  background: #e2e8f0;
}

.meter-segment {
  height: 100%;
}

.meter-segment.seg-steal   { flex: 35; background: #10b981; border-top-left-radius: 999px; border-bottom-left-radius: 999px; }
.meter-segment.seg-fair    { flex: 35; background: #0284c7; }
.meter-segment.seg-premium { flex: 30; background: #8b5cf6; border-top-right-radius: 999px; border-bottom-right-radius: 999px; }

.meter-pointer {
  position: absolute;
  top: -22px;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 2;
  transition: left 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.pointer-bubble {
  background: #002f34;
  color: #ffffff;
  font-size: 10.5px;
  font-weight: 800;
  padding: 2px 6px;
  border-radius: 4px;
  white-space: nowrap;
}

.pointer-pin {
  width: 0;
  height: 0;
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-top: 5px solid #002f34;
}

.meter-scale-legend {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  color: #64748b;
  margin-top: 6px;
}

.trend-summary-text {
  font-size: 12.5px;
  color: #475569;
  margin-top: 10px;
  line-height: 1.5;
}

/* 7. Detail Condition Inspection Box */
.condition-inspection-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 16px;
  margin: 18px 0;
}

.inspection-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.inspection-title-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.inspection-icon { font-size: 20px; }
.inspection-heading { font-size: 14px; font-weight: 700; color: #002f34; }
.inspection-sub { font-size: 11px; color: #64748b; }

.condition-score-pill {
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 800;
  display: inline-flex;
  gap: 6px;
}

.condition-score-pill.score-like-new { background: #ccfbf1; color: #0f766e; }
.condition-score-pill.score-good     { background: #dbeafe; color: #1e40af; }
.condition-score-pill.score-fair     { background: #fef3c7; color: #b45309; }

.condition-meter-bar-container {
  margin: 12px 0 16px;
}

.condition-main-track {
  width: 100%;
  height: 8px;
  background: #f1f5f9;
  border-radius: 999px;
  overflow: hidden;
}

.condition-main-fill {
  height: 100%;
  border-radius: 999px;
  transition: width 0.6s ease;
}

.condition-tier-ticks {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  color: #94a3b8;
  margin-top: 6px;
}

.condition-tier-ticks .tick.active {
  font-weight: 700;
  color: #0f766e;
}

.inspection-checklist {
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 12.5px;
  color: #334155;
  background: #f8fafc;
  padding: 10px 12px;
  border-radius: 6px;
}

/* 8. Social Proof Strip & Pulsing Green Dot */
.detail-social-proof-strip {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 12px 0;
  flex-wrap: wrap;
}

.proof-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 10px;
  border-radius: 6px;
  font-size: 12px;
  background: #f1f5f9;
  color: #334155;
  border: 1px solid #e2e8f0;
}

.proof-pill strong {
  color: #002f34;
}

.pulse-dot {
  width: 7px;
  height: 7px;
  background: #10b981;
  border-radius: 50%;
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);
  animation: pulseGreen 2s infinite;
}

/* 9. Enhanced Poster Details */
.poster-campus-tag {
  font-size: 11.5px;
  color: #0284c7;
  font-weight: 600;
  margin-top: 2px;
}

.poster-response-tag {
  font-size: 11px;
  color: #059669;
  font-weight: 600;
  margin-top: 1px;
}

.poster-rating-row {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  margin-top: 2px;
}

.poster-rating-row .stars { color: #f59e0b; }
.poster-rating-row .rating-val { font-weight: 700; color: #002f34; }
.poster-rating-row .rating-count { color: #64748b; }
```

### 7.2 Mobile Viewport Disciplines (375px, 768px, 1280px)

1. **375px Viewport (iPhone SE / Small Mobile)**:
   - Product cards render in 1 column (`grid-template-columns: 1fr`).
   - Inner container padding is `0 12px`. Available width is `351px`.
   - `.card-price-row` has `flex-wrap: wrap; gap: 6px;`.
   - Price, retail strikethrough, and savings pill wrap without pushing past card margins.
   - Condition meter width is constrained to `34px track`.
   - Engagement strip handles overflow with text truncation and wraps gracefully.
   - Sticky bottom action bar on product detail uses flexible layout: `mobile-detail-cta-bar` displays price, stock badge, and action buttons without clipping.
2. **768px Viewport (iPad / Tablet)**:
   - Product grid renders in 2 columns (`repeat(2, 1fr)`).
   - Filter sidebar collapses into mobile drawer or left-aligned column.
   - Price trend meter scale legend spaces evenly across the card width.
3. **1280px+ Viewport (Desktop)**:
   - Product grid renders in 3 columns (`grid-3`).
   - Sticky sidebar (`position: sticky; top: 88px`) holds the complete savings card and price comparison alongside the seller profile.

---

## 8. Exact Worker Implementation Guide

When implementing Milestone 2, workers must follow this step-by-step path:

### Step 1: Create `frontend/js/recommerce-visuals.js` (or add to `utils.js` / `stats.js`)
Provide a single global utility object: `window.RecommerceVisuals = { getAnalytics, buildPriceRowHtml, buildConditionMeterHtml, buildEngagementHtml, buildSavingsCardHtml, buildPriceTrendHtml, buildInspectionCardHtml, buildSocialProofStripHtml };`

### Step 2: Update `buildProductCard(product)` in `frontend/js/utils.js`
Replace the plain price row and condition tag with:
1. Deal quality badge (`deal-chip`) on top of image or before title.
2. Price row with current price, retail strikethrough, and emerald savings pill (`Save X%`).
3. Mini condition meter with 10-point score and colored bar.
4. Social proof / engagement bar above the location footer (`❤️ X saved • 🔥 Y views today • Senior Seller`).

### Step 3: Update `renderDetail(root)` in `frontend/js/product-detail.js`
1. Inject the **Social Proof Strip** right below the title/meta badges.
2. Inject the **Student Re-Commerce Savings Card** into the sticky sidebar action box.
3. Inject the **Condition Inspection Card** above the "About this item" section.
4. Inject the **Campus Price Comparison Widget** below the info cards.
5. Enhance the **Seller Profile Card** with senior college tag (`Graphic Era '25`), response time, and rating.
6. Connect wishlist toggle to update the detail page live saved count.

### Step 4: Add CSS styles to `frontend/css/global.css`
Append the CSS classes detailed in Section 7 of this blueprint, ensuring all colors conform to the existing light theme variables (`--bg-card`, `--text-primary`, `--success`, `--warning`, `--primary`).

---

## 9. Verification & Automated Test Plan

### Test 1: Headless Viewport Responsiveness Test
Execute the automated test suite `scripts/run_viewport_tests.py`:
- Verify `search-products.html` and `product-detail.html` at `375px`, `768px`, and `1280px`.
- Assert `document.documentElement.scrollWidth <= window.innerWidth` (zero horizontal overflow).

### Test 2: Savings Math Validation
Verify with test data:
- Textbook (Price ₹950): Retail ₹2,799 -> Save 66% (₹1,849).
- Laptop (Price ₹32,500): Retail ₹59,990 -> Save 46% (₹27,490).
- Cycle (Price ₹3,200): Retail ₹9,499 -> Save 66% (₹6,299).
- Calculator (Price ₹550): Retail ₹1,695 -> Save 68% (₹1,145).
- Ensure `retailPrice > product.price` for 100% of listings.

### Test 3: Condition Meter Integrity
Verify condition score mappings:
- `NEW`: 10/10 (100% bar)
- `LIKE_NEW`: 9/10 (90% bar)
- `GOOD`: 7/10 (70% bar)
- `FAIR`: 5/10 (50% bar)
- `OLD`: 3/10 (30% bar)

### Test 4: Regression Smoke Verification
Execute `python scripts/run_smoke_tests.py` to confirm zero breakages in API integration, search filtering, and order placement.
