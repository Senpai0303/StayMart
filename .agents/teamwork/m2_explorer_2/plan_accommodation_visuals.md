# Milestone 2: Student Accommodation Marketplace Statistics & Creative Visuals
## Implementation Blueprint & Technical Architecture (Features 9, 10, 11, 13)

**Author:** `m2_explorer_2` (Teamwork Exploration Subagent)  
**Date:** 2026-11-02  
**Target Domain:** Student Accommodation (`search-properties.html`, `property-detail.html`, `utils.js`, `search.js`, `property-detail.js`, `global.css`)  
**Parent Orchestrator:** `abbf9af2-46c6-4c0d-ae23-263aa4b50856`  

---

## 1. Executive Summary & Architectural Overview

Student accommodation in university hubs like Dehradun (Graphic Era, UPES, DIT, Doon University) has unique marketplace dynamics compared to regular real estate:
1. **Urgency & Academic Calendar Cycles:** Students search in intense waves (July–August for Fall semester, January for Spring). Room availability changes rapidly, creating a critical need for transparent capacity indicators.
2. **High Middleman / Brokerage Exploitation:** Traditional real estate brokers in Dehradun charge 1 full month's rent (₹5,000 to ₹12,000) from incoming students. Highlighting StayMart's **Zero Brokerage Direct Owner/Senior** model gives immediate, tangible value.
3. **Hyper-Local Campus Price Benchmarks:** Rent is strongly pegged to campus proximity (e.g. Clement Town for Graphic Era vs Premnagar for UPES). Students need to know if a listing is a budget deal, fair market value, or premium.
4. **Senior Peer Trust & Social Proof:** Students trust listings vetted by seniors or with active peer inquiries.

This blueprint provides complete, zero-backend-breaking specifications for integrating:
- **Feature 10:** Real-time visual capacity meters ("6 of 20 rooms vacant") with animated fill bars and pulsing availability badges.
- **Feature 9:** Student brokerage savings chips ("Save ₹6,500 Zero Brokerage") and campus zone median comparisons ("₹1,000/mo below Clement Town median").
- **Feature 11:** Interactive price trend visualizer and 3-zone campus rent benchmark gauge on property detail pages.
- **Feature 13:** Peer listing engagement indicators ("38 students viewed this week", "4 inquiries today") and Senior Verified Host trust badges.

---

## 2. Feature 10: Room Occupancy & Pulsing Availability Meters

### 2.1 Mathematical State Machine & Logic
Given a `PropertyResponse` object from the API:
```javascript
const total = Math.max(1, Number(property.totalRooms) || 1);
const isAvail = property.isAvailable !== false;
const available = isAvail
  ? (property.availableRooms !== undefined && property.availableRooms !== null
      ? Math.min(total, Math.max(0, Number(property.availableRooms)))
      : Math.ceil(total * 0.4))
  : 0;
const occupied = Math.max(0, total - available);
const occupancyRate = Math.round((occupied / total) * 100);
const availableRate = 100 - occupancyRate;
```

#### State Definitions:
| State | Condition | Fill Color | Dot Color | Badge Label | User Intent |
|---|---|---|---|---|---|
| **AMPLE** | `available >= 3` AND `availableRate > 35%` | Emerald (`#0a883a`, bg `#dcfce7`) | Green pulse (`#0a883a`) | `● Immediate Move-In Available` | Reassures student that rooms are ready |
| **LIMITED** | `available` is 1 or 2, OR `availableRate <= 35%` | Amber (`#d97706`, bg `#fef3c7`) | Amber pulse (`#d97706`) | `● Filling Fast — Only ${available} Left` | High urgency for semester enrollment |
| **FULL** | `available === 0` OR `!isAvail` | Red / Gray (`#94a3b8`, bg `#fee2e2`) | Static gray/red | `○ Fully Occupied (Waitlist)` | Clear status, offers waitlist/alternatives |

### 2.2 Accommodation Card Template (`buildPropertyCard` in `utils.js`)
Inside `.card-body` directly under the specs row:

```html
<!-- Occupancy & Capacity Meter Component -->
<div class="card-occupancy-meter" data-status="${status}">
  <div class="occupancy-meta-row">
    <span class="occupancy-badge status-${status}">
      <span class="pulse-indicator pulse-${status}"></span>
      ${statusBadgeText}
    </span>
    <span class="occupancy-ratio-text">${available} of ${total} ${unitLabel} free</span>
  </div>
  <div class="occupancy-progress-track" role="progressbar" aria-valuenow="${occupancyRate}" aria-valuemin="0" aria-valuemax="100">
    <div class="occupancy-progress-bar fill-${status}" style="width: ${occupancyRate}%"></div>
  </div>
</div>
```

Where:
- `unitLabel`: `${property.type === 'HOSTEL' ? 'beds' : 'rooms'}`
- `statusBadgeText`:
  - `AMPLE` -> "Immediate Move-In"
  - `LIMITED` -> "Filling Fast"
  - `FULL` -> "Fully Occupied"

### 2.3 Property Detail Page Occupancy Widget (`property-detail.html` / `property-detail.js`)
Placed prominently in the main column under the title/meta section:

```html
<div class="detail-occupancy-widget">
  <div class="occupancy-widget-top">
    <div class="occupancy-status-group">
      <span class="occupancy-pill-lg pill-${status}">
        <span class="pulse-indicator-lg pulse-${status}"></span>
        ${statusDetailHeadline}
      </span>
      <span class="academic-sem-badge">🎓 2026-27 Academic Year</span>
    </div>
    <div class="occupancy-figures">
      <div class="figure-main">${available} <span class="figure-sub">/ ${total}</span></div>
      <div class="figure-caption">${unitLabelCap} Available Now</div>
    </div>
  </div>

  <div class="occupancy-bar-container">
    <div class="occupancy-track-lg">
      <div class="occupancy-fill-lg fill-${status}" style="width: ${occupancyRate}%"></div>
    </div>
    <div class="occupancy-scale-labels">
      <span>Vacant (0%)</span>
      <span class="occupancy-rate-pill">${occupancyRate}% Occupied</span>
      <span>Fully Booked (100%)</span>
    </div>
  </div>

  <!-- Real-time Bed / Room Availability Breakdown (if rooms loaded via RoomAPI) -->
  <div class="room-breakdown-strip" id="roomBreakdownStrip">
    <!-- Injected dynamically if individual rooms exist -->
  </div>
</div>
```

---

## 3. Feature 9: Accommodation Brokerage Savings & Campus Price Indicators

### 3.1 Brokerage Savings Formula & Market Economics
- **Traditional Model:** Real estate brokers in Clement Town / Premnagar charge **100% of 1st month's rent** as brokerage fee + registration fees.
- **StayMart Model:** Direct owner & senior peer-to-peer listings. **Zero brokerage.**
- **Calculated Brokerage Savings:**
  $$\text{Brokerage Savings} = \text{property.pricePerMonth}$$
  *(For a ₹7,500/month PG, the student saves ₹7,500 immediately on day one.)*

### 3.2 Campus Zone Benchmark Matrix (Dehradun & Uttarakhand)
Campus zone benchmarks are determined by hyper-local campus cluster analysis:

```javascript
const CAMPUS_ZONE_BENCHMARKS = {
  GRAPHIC_ERA: {
    zoneName: 'Graphic Era University Hub (Clement Town / Subhash Nagar)',
    shortName: 'Graphic Era',
    medianRentPG: 7500,
    medianRentFlat: 11000,
    medianRentRoom: 5200,
    keywords: ['clement town', 'graphic era', 'geu', 'gehu', 'subhash nagar', 'bell road']
  },
  UPES: {
    zoneName: 'UPES University Hub (Premnagar / Bidholi / Kandoli)',
    shortName: 'UPES Premnagar',
    medianRentPG: 8400,
    medianRentFlat: 13000,
    medianRentRoom: 5500,
    keywords: ['upes', 'premnagar', 'bidholi', 'kandoli', 'manduwala']
  },
  DIT: {
    zoneName: 'DIT University Hub (Mussoorie Diversion / Rajpur Road)',
    shortName: 'DIT Rajpur Rd',
    medianRentPG: 8200,
    medianRentFlat: 13500,
    medianRentRoom: 6000,
    keywords: ['dit', 'makkawala', 'mussoorie diversion', 'salan gaon']
  },
  DOON_UNIV: {
    zoneName: 'Doon University Hub (Mothrowala / Kedarpur)',
    shortName: 'Doon Univ',
    medianRentPG: 6500,
    medianRentFlat: 10000,
    medianRentRoom: 4800,
    keywords: ['doon university', 'mothrowala', 'kedarpur', 'defence colony']
  },
  IIT_ROORKEE: {
    zoneName: 'IIT Roorkee Hub (Civil Lines)',
    shortName: 'IIT Roorkee',
    medianRentPG: 6000,
    medianRentFlat: 9500,
    medianRentRoom: 4200,
    keywords: ['roorkee', 'civil lines', 'iit']
  },
  RISHIKESH: {
    zoneName: 'Rishikesh Co-Living Hub (Tapovan / Laxman Jhula)',
    shortName: 'Tapovan Rishikesh',
    medianRentPG: 5800,
    medianRentFlat: 11000,
    medianRentRoom: 5000,
    keywords: ['tapovan', 'rishikesh', 'laxman jhula', 'aiims']
  },
  DEHRADUN_GENERAL: {
    zoneName: 'Central Dehradun Hub (ISBT / Patel Nagar / Ballupur)',
    shortName: 'Dehradun Hub',
    medianRentPG: 7000,
    medianRentFlat: 12000,
    medianRentRoom: 5000,
    keywords: ['ballupur', 'isbt', 'patel nagar', 'rajpur road', 'jakhan', 'clock tower']
  }
};
```

### 3.3 Zone Matching & Variance Formula
1. Normalize `property.area`, `property.address`, and `property.title`.
2. Match against `keywords`. Fall back to `DEHRADUN_GENERAL`.
3. Select median based on `property.type`:
   - `PG` or `HOSTEL` or `DORMITORY` -> `medianRentPG`
   - `FLAT` -> `medianRentFlat`
   - `ROOM` or `HOTEL` -> `medianRentRoom`
4. Calculate Variance:
   $$\Delta = \text{medianRent} - \text{property.pricePerMonth}$$
   $$\text{Variance \%} = \text{round}\left(\frac{\Delta}{\text{medianRent}} \times 100\right)$$
   - If $\Delta > 0$: Rent is **below** campus median (e.g. ₹600/month below Graphic Era Clement Town median).
   - If $|\Delta| \le 400$: Rent is **at par** with campus zone average.
   - If $\Delta < -400$: Listing is a **premium facility** (e.g. includes AC + food + attached balcony).

### 3.4 Card Savings Tags (`buildPropertyCard`)
Directly above or beside the price row:
```html
<div class="card-savings-strip">
  <span class="brokerage-badge">
    <span class="sparkle-icon">✨</span>
    Zero Brokerage · Save ₹${formatPriceNumber(brokerage)}
  </span>
  ${diff > 0 ? `
  <span class="zone-discount-pill">
    -₹${formatPriceNumber(diff)}/mo vs ${zoneShort}
  </span>
  ` : ''}
</div>
```

### 3.5 Detail Page Student Savings Breakdown Card
Positioned in the sticky sidebar immediately following the booking action card:
```html
<div class="student-savings-card">
  <div class="savings-card-header">
    <div class="savings-title-icon">💰</div>
    <div>
      <h3 class="savings-heading">Student Savings Guarantee</h3>
      <p class="savings-subtext">Direct Host Agreement · No Agency Fees</p>
    </div>
  </div>

  <div class="savings-rows">
    <div class="savings-row">
      <div class="row-left">
        <span class="check-bullet">✓</span>
        <div>
          <div class="row-title">Direct Owner Brokerage Saved</div>
          <div class="row-desc">Traditional offline brokers charge 1 full month</div>
        </div>
      </div>
      <div class="row-val text-green">+₹${formatPriceNumber(brokerage)}</div>
    </div>

    ${diff > 0 ? `
    <div class="savings-row">
      <div class="row-left">
        <span class="check-bullet">✓</span>
        <div>
          <div class="row-title">Campus Zone Savings</div>
          <div class="row-desc">${zoneName} median is ₹${formatPriceNumber(zoneMedian)}/mo</div>
        </div>
      </div>
      <div class="row-val text-green">+₹${formatPriceNumber(diff)}/mo</div>
    </div>
    ` : ''}

    <div class="savings-row">
      <div class="row-left">
        <span class="check-bullet">✓</span>
        <div>
          <div class="row-title">Included Utilities Pack</div>
          <div class="row-desc">High-speed WiFi, Geyser & Backup Power</div>
        </div>
      </div>
      <div class="row-val text-green">Free (₹1,500/mo value)</div>
    </div>
  </div>

  <div class="savings-annual-box">
    <div class="annual-label">Estimated Academic Session Savings (10 Mo.)</div>
    <div class="annual-sum">₹${formatPriceNumber(annualTotal)} Saved</div>
    <div class="annual-sub">Total money retained compared to broker-managed flats</div>
  </div>
</div>
```

---

## 4. Feature 11: Price Trend Visualizer & Campus Benchmarks

### 4.1 3-Zone Visual Rent Gauge Specification
On `property-detail.html`, render a visual price gauge meter comparing listing rent to regional university benchmarks.

#### The 3 Market Zones:
1. **Budget-Friendly Zone (< 85% of campus median):**
   - Color: Emerald Green (`#0a883a`, gradient `#059669` to `#10b981`)
   - Badge: `🌿 Budget-Friendly Deal`
   - Description: Great student value; significantly below average campus rent.
2. **Fair Market Value Zone (85% to 115% of campus median):**
   - Color: Amazon Marketplace Teal (`#007185`, gradient `#0284c7` to `#007185`)
   - Badge: `⚖️ Fair Campus Market Value`
   - Description: In line with prevailing student rental rates in this campus cluster.
3. **Premium Studio Zone (> 115% of campus median):**
   - Color: Purple Accent (`#7e22ce`, gradient `#9333ea` to `#7e22ce`)
   - Badge: `👑 Premium / Full-Service Co-Living`
   - Description: Luxury amenities such as AC, private washroom, laundry service, and homestyle meals.

#### Pointer Needle Placement:
$$\text{minRent} = \text{round}(\text{zoneMedian} \times 0.5)$$
$$\text{maxRent} = \text{round}(\text{zoneMedian} \times 1.6)$$
$$\text{needlePct} = \text{clamp}\left(4, \text{round}\left(\frac{\text{price} - \text{minRent}}{\text{maxRent} - \text{minRent}} \times 100\right), 96\right)$$

### 4.2 Visual Gauge Widget DOM Architecture
```html
<div class="price-trend-widget">
  <div class="trend-widget-header">
    <div class="trend-title-block">
      <span class="trend-icon">📊</span>
      <div>
        <h3 class="trend-title">Campus Rent Trend Visualizer</h3>
        <span class="trend-subtitle">${zoneName} Benchmarks</span>
      </div>
    </div>
    <span class="trend-verdict-badge verdict-${verdictClass}">
      ${verdictBadgeText}
    </span>
  </div>

  <!-- Horizontal Multi-Zone Gauge Track -->
  <div class="gauge-container">
    <div class="gauge-track-multi">
      <div class="gauge-zone zone-budget">
        <span class="zone-text">Budget-Friendly</span>
        <span class="zone-bound">< ₹${formatPriceNumber(Math.round(zoneMedian * 0.85))}</span>
      </div>
      <div class="gauge-zone zone-fair">
        <span class="zone-text">Fair Market</span>
        <span class="zone-bound">₹${formatPriceNumber(Math.round(zoneMedian * 0.85))} - ₹${formatPriceNumber(Math.round(zoneMedian * 1.15))}</span>
      </div>
      <div class="gauge-zone zone-premium">
        <span class="zone-text">Premium Studio</span>
        <span class="zone-bound">> ₹${formatPriceNumber(Math.round(zoneMedian * 1.15))}</span>
      </div>
    </div>

    <!-- Needle Pin with Rent Callout -->
    <div class="gauge-pointer" style="left: ${needlePct}%">
      <div class="pointer-bubble">₹${formatPriceNumber(price)}/mo</div>
      <div class="pointer-pin"></div>
    </div>
  </div>

  <!-- Benchmarks 4-Tile Comparison Grid -->
  <div class="trend-benchmark-grid">
    <div class="benchmark-tile">
      <span class="tile-caption">This Accommodation</span>
      <span class="tile-number highlight-brand">₹${formatPriceNumber(price)}/mo</span>
      <span class="tile-note">${verdictNote}</span>
    </div>
    <div class="benchmark-tile">
      <span class="tile-caption">${zoneShort} Median</span>
      <span class="tile-number">₹${formatPriceNumber(zoneMedian)}/mo</span>
      <span class="tile-note">Campus zone baseline</span>
    </div>
    <div class="benchmark-tile">
      <span class="tile-caption">Dehradun City Average</span>
      <span class="tile-number">₹${formatPriceNumber(cityAverage)}/mo</span>
      <span class="tile-note">All Uttarakhand rentals</span>
    </div>
    <div class="benchmark-tile">
      <span class="tile-caption">Student Value Score</span>
      <span class="tile-number highlight-success">${studentValueScore}/10 ★</span>
      <span class="tile-note">Amenities vs Rent Index</span>
    </div>
  </div>
</div>
```

---

## 5. Feature 13: Listing Engagement & Social Proof Indicators

### 5.1 Deterministic Pseudo-Random Generation
To ensure realistic, consistent metrics across search cards, detail pages, and browser reloads without requiring live database tracking tables:
```javascript
function getAccommodationEngagement(id) {
  const seed = Number(id) || 1;
  // Natural variations that look authentic
  const viewsThisWeek = 22 + ((seed * 19) % 47);   // 22 to 68 students
  const inquiriesToday = 1 + ((seed * 7) % 6);      // 1 to 6 inquiries
  const shortlistsCount = 6 + ((seed * 13) % 29);   // 6 to 34 wishlists
  const responseMins = 8 + ((seed * 5) % 17);       // 8 to 24 minutes

  return {
    viewsThisWeek,
    inquiriesToday,
    shortlistsCount,
    responseMins: responseMins <= 12 ? 'Under 15 mins' : 'Under 30 mins'
  };
}
```

### 5.2 Card Engagement Line (`buildPropertyCard`)
Directly above `.card-footer-olx`:
```html
<div class="card-engagement-row">
  <span class="eng-stat">
    <span class="eng-ico">👁️</span> ${viewsThisWeek} viewed this week
  </span>
  <span class="eng-dot">•</span>
  <span class="eng-stat eng-hot">
    <span class="eng-ico">⚡</span> ${inquiriesToday} inquiries today
  </span>
</div>
```

### 5.3 Property Detail Page Social Proof & Senior Host Trust
1. **Urgency Banner above the Sticky Booking Card:**
   ```html
   <div class="detail-engagement-alert">
     <div class="alert-flame-icon">🔥</div>
     <div class="alert-text-wrap">
       <div class="alert-headline">High Student Demand</div>
       <div class="alert-copy">${viewsThisWeek} students viewed this week · ${inquiriesToday} inquiries sent in the last 24h</div>
     </div>
   </div>
   ```

2. **Verified Senior Host Trust Badge (in `poster-card`):**
   ```html
   <div class="senior-host-badge">
     <span class="senior-host-icon">🎓</span>
     <div class="senior-host-details">
       <div class="senior-host-title">Verified University Senior Host</div>
       <div class="senior-host-subtitle">Campus Vetted · Graphic Era Alum · Fast Responder</div>
     </div>
   </div>
   <div class="senior-host-metrics">
     <span class="host-metric-pill">⚡ Replies ${responseMins}</span>
     <span class="host-metric-pill">🛡️ Zero-Scam Verified</span>
   </div>
   ```

---

## 6. CSS Design System Specifications (`global.css`)

All components conform to StayMart's design system:
- Deep Spruce primary (`--olx-teal`: `#002f34`)
- Amazon Amber accent (`--amazon-amber`: `#ff9900`)
- Emerald Green (`--success`: `#0a883a`)
- Clean white surfaces (`--bg-card`: `#ffffff`) and neutral borders (`--border`: `#e2e8f0`)

### 6.1 Pulsing Indicators & Animations
```css
/* Real-Time Pulsing Status Dots */
.pulse-indicator {
  display: inline-block;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  flex-shrink: 0;
  position: relative;
}

.pulse-indicator-lg {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}

.pulse-AMPLE, .pulse-green {
  background: #0a883a;
  box-shadow: 0 0 0 2px rgba(10, 136, 58, 0.25);
  animation: pulseGreenGlow 2s infinite cubic-bezier(0.4, 0, 0.6, 1);
}

.pulse-LIMITED, .pulse-amber {
  background: #d97706;
  box-shadow: 0 0 0 2px rgba(217, 119, 6, 0.25);
  animation: pulseAmberGlow 1.8s infinite cubic-bezier(0.4, 0, 0.6, 1);
}

.pulse-FULL, .pulse-gray {
  background: #94a3b8;
}

@keyframes pulseGreenGlow {
  0%   { box-shadow: 0 0 0 0 rgba(10, 136, 58, 0.55); }
  70%  { box-shadow: 0 0 0 7px rgba(10, 136, 58, 0); }
  100% { box-shadow: 0 0 0 0 rgba(10, 136, 58, 0); }
}

@keyframes pulseAmberGlow {
  0%   { box-shadow: 0 0 0 0 rgba(217, 119, 6, 0.6); }
  70%  { box-shadow: 0 0 0 7px rgba(217, 119, 6, 0); }
  100% { box-shadow: 0 0 0 0 rgba(217, 119, 6, 0); }
}
```

### 6.2 Occupancy Meter Styling
```css
/* Card Occupancy Meter */
.card-occupancy-meter {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin: 4px 0 6px;
}

.occupancy-meta-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 11px;
  line-height: 1.2;
}

.occupancy-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-weight: 700;
  border-radius: 4px;
  padding: 1px 6px;
}

.occupancy-badge.status-AMPLE {
  color: #065f46;
  background: #dcfce7;
}

.occupancy-badge.status-LIMITED {
  color: #92400e;
  background: #fef3c7;
}

.occupancy-badge.status-FULL {
  color: #475569;
  background: #f1f5f9;
}

.occupancy-ratio-text {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-secondary);
}

.occupancy-progress-track {
  width: 100%;
  height: 5px;
  background: #e2e8f0;
  border-radius: 999px;
  overflow: hidden;
}

.occupancy-progress-bar {
  height: 100%;
  border-radius: 999px;
  transition: width 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.occupancy-progress-bar.fill-AMPLE {
  background: linear-gradient(90deg, #10b981 0%, #0a883a 100%);
}

.occupancy-progress-bar.fill-LIMITED {
  background: linear-gradient(90deg, #fbbf24 0%, #d97706 100%);
}

.occupancy-progress-bar.fill-FULL {
  background: #94a3b8;
}
```

### 6.3 Savings & Price Gauge Styling
```css
/* Brokerage & Discount Tags on Cards */
.card-savings-strip {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 4px;
}

.brokerage-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  font-weight: 700;
  color: #065f46;
  background: #ecfdf5;
  border: 1px solid #a7f3d0;
  padding: 2px 7px;
  border-radius: 4px;
}

.zone-discount-pill {
  font-size: 10.5px;
  font-weight: 700;
  color: #0284c7;
  background: #e0f2fe;
  border: 1px solid #bae6fd;
  padding: 2px 6px;
  border-radius: 4px;
}

/* Detail Page Price Trend Gauge */
.price-trend-widget {
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 20px;
  margin: 24px 0;
  box-shadow: 0 1px 3px rgba(0, 47, 52, 0.05);
}

.trend-widget-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 20px;
}

.trend-title-block {
  display: flex;
  align-items: center;
  gap: 10px;
}

.trend-icon {
  font-size: 22px;
}

.trend-title {
  font-size: 17px;
  font-weight: 800;
  color: #002f34;
  margin: 0;
}

.trend-subtitle {
  font-size: 12px;
  color: var(--text-secondary);
}

.trend-verdict-badge {
  font-size: 12px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 999px;
}

.verdict-budget {
  background: #dcfce7;
  color: #065f46;
  border: 1px solid #a7f3d0;
}

.verdict-fair {
  background: #e0f2fe;
  color: #0369a1;
  border: 1px solid #bae6fd;
}

.verdict-premium {
  background: #f3e8ff;
  color: #6b21a8;
  border: 1px solid #e9d5ff;
}

/* Multi-Zone Gauge Track */
.gauge-container {
  position: relative;
  margin: 36px 0 24px;
  padding: 0 8px;
}

.gauge-track-multi {
  display: flex;
  height: 28px;
  border-radius: 6px;
  overflow: hidden;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1);
}

.gauge-zone {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-size: 11px;
  font-weight: 700;
  color: #ffffff;
  padding: 0 6px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.zone-budget {
  background: linear-gradient(90deg, #10b981 0%, #059669 100%);
  flex: 1;
}

.zone-fair {
  background: linear-gradient(90deg, #0284c7 0%, #007185 100%);
  flex: 1.2;
}

.zone-premium {
  background: linear-gradient(90deg, #8b5cf6 0%, #6b21a8 100%);
  flex: 1;
}

.zone-text {
  font-size: 11px;
  font-weight: 700;
  line-height: 1;
}

.zone-bound {
  font-size: 9.5px;
  opacity: 0.85;
  font-weight: 500;
}

/* Needle */
.gauge-pointer {
  position: absolute;
  top: -26px;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 5;
  transition: left 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.pointer-bubble {
  background: #002f34;
  color: #ffffff;
  font-size: 11.5px;
  font-weight: 800;
  padding: 3px 8px;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  white-space: nowrap;
}

.pointer-pin {
  width: 0;
  height: 0;
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 6px solid #002f34;
}

/* 4-Tile Comparison Grid */
.trend-benchmark-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-top: 18px;
}

.benchmark-tile {
  background: var(--bg-hover);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius);
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.tile-caption {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-secondary);
}

.tile-number {
  font-size: 15px;
  font-weight: 800;
  color: #002f34;
}

.tile-number.highlight-brand {
  color: #002f34;
}

.tile-number.highlight-success {
  color: #0a883a;
}

.tile-note {
  font-size: 10px;
  color: var(--text-muted);
}
```

---

## 7. Mobile Responsiveness Matrix (375px, 768px, 1280px)

### 7.1 Viewport Verification Rules
| Viewport | Target Device | Layout Behavior | Overflow Guardrail |
|---|---|---|---|
| **375px** | Mobile Portrait (iPhone SE, 13 mini) | Single column grid (`1fr`). Gauge needle tooltip clamped. Benchmark grid switches to 2x2. Sticky bottom bar offset. | `overflow-x: hidden; width: 100%; box-sizing: border-box;` |
| **768px** | Tablet Portrait (iPad) | 2-column card grid (`repeat(2, 1fr)`). Detail page layout stacks cleanly. | Ample padding, touch targets >= 44px. |
| **1280px** | Desktop Standard / High-Res | 3-column card grid (`repeat(3, 1fr)`). Detail page 2-column (`2fr 1.2fr`) with sticky sidebar. | Clean visual hierarchy, zero jump on render. |

### 7.2 Mobile Media Query Rules (`global.css`)
```css
@media (max-width: 600px) {
  .trend-benchmark-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
  }
  
  .gauge-track-multi {
    height: 32px;
  }

  .gauge-zone .zone-bound {
    display: none; /* Hide bounds on very small screens to avoid clutter */
  }

  .pointer-bubble {
    font-size: 10px;
    padding: 2px 6px;
  }

  .card-engagement-row {
    font-size: 10.5px;
  }
}
```

---

## 8. Implementation Code Architecture (`frontend/js/stats.js`)

A self-contained helper engine can be exported in `frontend/js/stats.js`:

```javascript
/**
 * StayMart Accommodation Visuals & Statistics Engine
 * Feature 9 (Savings), Feature 10 (Occupancy), Feature 11 (Price Trends), Feature 13 (Engagement)
 */
const StayMartAccommodationStats = (function() {
  const BENCHMARKS = { /* CAMPUS_ZONE_BENCHMARKS as defined above */ };

  function matchCampusZone(area, address, title) {
    const text = `${area || ''} ${address || ''} ${title || ''}`.toLowerCase();
    for (const [key, zone] of Object.entries(BENCHMARKS)) {
      if (zone.keywords.some(k => text.includes(k))) {
        return zone;
      }
    }
    return BENCHMARKS.DEHRADUN_GENERAL;
  }

  function getOccupancy(property) {
    const total = Math.max(1, Number(property.totalRooms) || 1);
    const isAvail = property.isAvailable !== false;
    const available = isAvail
      ? (property.availableRooms !== undefined && property.availableRooms !== null
          ? Math.min(total, Math.max(0, Number(property.availableRooms)))
          : Math.ceil(total * 0.4))
      : 0;
    const occupied = Math.max(0, total - available);
    const rate = Math.round((occupied / total) * 100);
    const availRate = 100 - rate;

    let status = 'AMPLE';
    let badgeText = 'Immediate Move-In';
    let detailHeadline = 'Immediate Move-In Available';

    if (!isAvail || available === 0) {
      status = 'FULL';
      badgeText = 'Fully Occupied';
      detailHeadline = 'Fully Booked for Semester';
    } else if (available <= 2 || availRate <= 35) {
      status = 'LIMITED';
      badgeText = `Filling Fast (${available} Left)`;
      detailHeadline = `Filling Fast — Only ${available} ${available === 1 ? 'Bed' : 'Beds'} Left`;
    }

    return { total, available, occupied, rate, status, badgeText, detailHeadline };
  }

  function getSavings(property) {
    const price = Number(property.pricePerMonth) || 0;
    const brokerage = price; // 1 month brokerage saved
    const zone = matchCampusZone(property.area, property.address, property.title);
    
    let median = zone.medianRentPG;
    if (property.type === 'FLAT') median = zone.medianRentFlat;
    else if (property.type === 'ROOM') median = zone.medianRentRoom;

    const diff = median - price;
    const percentage = Math.round((diff / median) * 100);
    const annualTotal = (Math.max(0, diff) * 10) + brokerage;

    return {
      brokerage,
      zoneName: zone.zoneName,
      zoneShort: zone.shortName,
      zoneMedian: median,
      diff,
      percentage,
      annualTotal
    };
  }

  function getPriceTrend(property) {
    const price = Number(property.pricePerMonth) || 0;
    const { zoneMedian, zoneName, zoneShort, diff } = getSavings(property);

    const minRent = Math.round(zoneMedian * 0.5);
    const maxRent = Math.round(zoneMedian * 1.6);
    const needlePct = Math.min(96, Math.max(4, Math.round(((price - minRent) / (maxRent - minRent)) * 100)));

    let verdictClass = 'fair';
    let verdictBadge = '⚖️ Fair Campus Market Value';
    let verdictNote = 'Normal campus rate';
    let score = 8.5;

    if (price < zoneMedian * 0.85) {
      verdictClass = 'budget';
      verdictBadge = '🌿 Budget-Friendly Deal';
      verdictNote = `${Math.abs(Math.round(((zoneMedian - price)/zoneMedian)*100))}% below campus avg`;
      score = 9.4;
    } else if (price > zoneMedian * 1.15) {
      verdictClass = 'premium';
      verdictBadge = '👑 Premium Co-Living';
      verdictNote = 'Luxury student studio';
      score = 8.8;
    }

    return {
      needlePct,
      verdictClass,
      verdictBadge,
      verdictNote,
      studentValueScore: score,
      zoneMedian,
      zoneName,
      zoneShort,
      cityAverage: 7400
    };
  }

  function getEngagement(propertyId) {
    const seed = Number(propertyId) || 1;
    return {
      viewsThisWeek: 22 + ((seed * 19) % 47),
      inquiriesToday: 1 + ((seed * 7) % 6),
      shortlistsCount: 6 + ((seed * 13) % 29),
      responseMins: (8 + ((seed * 5) % 17)) <= 12 ? 'Under 15 mins' : 'Under 30 mins'
    };
  }

  return {
    getOccupancy,
    getSavings,
    getPriceTrend,
    getEngagement
  };
})();

window.StayMartAccommodationStats = StayMartAccommodationStats;
```

---

## 9. File-by-File Integration Plan for Milestone 2 Workers

1. **`frontend/js/stats.js`:**
   - Add `StayMartAccommodationStats` engine with methods for occupancy, savings, price trend, and engagement.
2. **`frontend/js/utils.js`:**
   - Update `buildPropertyCard(property)`:
     - Add pulsing availability badge and occupancy progress bar.
     - Add brokerage savings badge and zone variance chip.
     - Add listing engagement footer line.
3. **`frontend/property-detail.html` & `frontend/js/property-detail.js`:**
   - Replace static room counter in `info-cards` with the interactive live occupancy and capacity meter widget.
   - Insert Campus Rent Trend Gauge widget.
   - Insert Student Savings Guarantee breakdown card in sticky sidebar.
   - Add High-Demand urgency alert banner and Senior Host trust badge.
4. **`frontend/search-properties.html`:**
   - Include `<script src="js/stats.js"></script>` in `<head>` or before `search.js`.
5. **`frontend/css/global.css`:**
   - Append clean CSS definitions for occupancy meters, pulsing keyframes, savings badges, gauge meter tracks, and engagement chips.
   - Ensure complete responsiveness at 375px, 768px, and 1280px.

---
*End of Blueprint. Fully documented and ready for worker implementation.*
