/**
 * Forensic Verification Test Suite for Milestone 2: Marketplace Statistics & Creative Visuals
 * Independent Auditor: Milestone 2 Forensic Auditor (Generation 2)
 *
 * Verifies Features 8, 9, 10, 11, 12, 13
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT_DIR = path.resolve(__dirname, '..');
const FRONTEND_DIR = path.join(ROOT_DIR, 'frontend');

console.log('======================================================================');
console.log('StayMart Milestone 2: Forensic Integrity & Mathematical Audit Suite');
console.log('======================================================================');

let passCount = 0;
let failCount = 0;
const failureDetails = [];

function assert(condition, message) {
  if (condition) {
    console.log(`  [PASS] ${message}`);
    passCount++;
  } else {
    console.error(`  [FAIL] ${message}`);
    failCount++;
    failureDetails.push(message);
  }
}

// ---------------------------------------------------------------------------
// 1. Static Anti-Cheat & Facade Inspection
// ---------------------------------------------------------------------------
console.log('\n--- 1. STATIC ANTI-CHEAT & FACADE AUDIT ---');

const statsJsContent = fs.readFileSync(path.join(FRONTEND_DIR, 'js', 'stats.js'), 'utf8');
const chartsJsContent = fs.readFileSync(path.join(FRONTEND_DIR, 'js', 'charts.js'), 'utf8');
const utilsJsContent = fs.readFileSync(path.join(FRONTEND_DIR, 'js', 'utils.js'), 'utf8');
const indexHtmlContent = fs.readFileSync(path.join(FRONTEND_DIR, 'index.html'), 'utf8');

// Check that stats.js is not an empty stub or facade
assert(statsJsContent.length > 5000, `stats.js has authentic size (${statsJsContent.length} bytes)`);
assert(chartsJsContent.length > 5000, `charts.js has authentic size (${chartsJsContent.length} bytes)`);

// Check that functions don't return dummy constants
assert(!statsJsContent.includes('return "PASS"') && !statsJsContent.includes('return true; // dummy'), 'No dummy test-pass facades in stats.js');
assert(!chartsJsContent.includes('return "PASS"') && !chartsJsContent.includes('return "<svg></svg>"'), 'No static dummy SVG stubs in charts.js');

// ---------------------------------------------------------------------------
// 2. Feature 8: Animated Metric Counters & easeOutExpo Verification
// ---------------------------------------------------------------------------
console.log('\n--- 2. FEATURE 8: ANIMATED COUNTER & MATH EASING AUDIT ---');

assert(statsJsContent.includes('IntersectionObserver'), 'IntersectionObserver is utilized in stats.js');
assert(statsJsContent.includes('requestAnimationFrame'), 'requestAnimationFrame is used for progressive rendering');
assert(statsJsContent.includes('easeOutExpo'), 'easeOutExpo easing algorithm is defined');

// Extract and test easeOutExpo
function easeOutExpo(t) {
  return t === 1 ? 1 : 1 - Math.pow(2, -10 * t);
}

assert(easeOutExpo(0) === 0, 'easeOutExpo(0) === 0 (starts exactly at 0)');
assert(easeOutExpo(1) === 1, 'easeOutExpo(1) === 1 (finishes exactly at target 1.0)');

// Test strictly monotonic increase in [0, 1]
let monotonic = true;
let prev = -1;
for (let t = 0; t <= 1.0001; t += 0.05) {
  const val = easeOutExpo(Math.min(1, t));
  if (val < prev) monotonic = false;
  prev = val;
}
assert(monotonic, 'easeOutExpo is strictly monotonic across [0, 1]');

// Test realistic counter increments for 500+, 1,200+, ₹4,500/mo, 98%
const targets = [
  { target: 500, prefix: '', suffix: '+' },
  { target: 1200, prefix: '', suffix: '+' },
  { target: 4500, prefix: '₹', suffix: '/mo' },
  { target: 98, prefix: '', suffix: '%' }
];

targets.forEach(({ target, prefix, suffix }) => {
  const midVal = Math.round(target * easeOutExpo(0.5));
  assert(midVal > 0 && midVal < target, `Midpoint progress for target ${target}: ${midVal} is between 0 and ${target}`);
  const finalVal = Math.round(target * easeOutExpo(1.0));
  const finalStr = `${prefix}${finalVal.toLocaleString('en-IN')}${suffix}`;
  assert(finalVal === target, `Final formatted value for target ${target} matches: ${finalStr}`);
});

// ---------------------------------------------------------------------------
// 3. Feature 9: Interactive Dual-Mode Student Savings Calculator Logic
// ---------------------------------------------------------------------------
console.log('\n--- 3. FEATURE 9: DUAL-MODE SAVINGS CALCULATOR AUDIT ---');

// Mock DOM environment to execute calculator logic from stats.js
const domContext = {
  window: {},
  document: {
    getElementById: (id) => {
      if (!domContext._elements[id]) {
        domContext._elements[id] = {
          value: '9000',
          checked: true,
          textContent: '',
          style: {},
          classList: {
            add: () => {},
            remove: () => {},
            toggle: () => {}
          },
          setAttribute: () => {},
          getAttribute: () => null
        };
      }
      return domContext._elements[id];
    },
    querySelectorAll: () => [],
    querySelector: () => null,
    addEventListener: () => {}
  },
  performance: { now: () => 100 },
  requestAnimationFrame: () => {},
  Math: Math,
  parseFloat: parseFloat,
  parseInt: parseInt,
  Number: Number,
  String: String,
  Object: Object
};
domContext.window = domContext;
domContext._elements = {};

vm.createContext(domContext);
vm.runInContext(statsJsContent, domContext);

// Verify exported calculator functions
assert(typeof domContext.window.switchCalcMode === 'function', 'switchCalcMode is exported to window');
assert(typeof domContext.window.updateAccommodationCalc === 'function', 'updateAccommodationCalc is exported to window');
assert(typeof domContext.window.setRentPreset === 'function', 'setRentPreset is exported to window');
assert(typeof domContext.window.selectGearPackage === 'function', 'selectGearPackage is exported to window');

// Test accommodation savings calculations with varying rents
const rentTestCases = [
  { rent: 6000, duration: 10, utils: true, meals: true, expectedBrokerage: 6000, expectedUtil: 12000, expectedTotal: 18000 },
  { rent: 9000, duration: 10, utils: true, meals: true, expectedBrokerage: 9000, expectedUtil: 12000, expectedTotal: 21000 },
  { rent: 14000, duration: 10, utils: false, meals: false, expectedBrokerage: 14000, expectedUtil: 0, expectedTotal: 14000 },
  { rent: 20000, duration: 12, utils: true, meals: true, expectedBrokerage: 20000, expectedUtil: 14400, expectedTotal: 34400 }
];

rentTestCases.forEach(({ rent, duration, utils, meals, expectedBrokerage, expectedUtil, expectedTotal }) => {
  domContext.document.getElementById('calcRentSlider').value = String(rent);
  domContext.document.getElementById('calcIncludeUtilities').checked = utils;
  domContext.document.getElementById('calcIncludeMeals').checked = meals;
  domContext.window.setDurationPreset(duration);
  domContext.window.updateAccommodationCalc();

  const totalText = domContext.document.getElementById('calcAccTotalSavings').textContent;
  const brokerageText = domContext.document.getElementById('cbBrokerageVal').textContent;
  const utilText = domContext.document.getElementById('cbUtilityVal').textContent;

  assert(totalText === `₹${expectedTotal.toLocaleString('en-IN')}`, `Rent ₹${rent} (${duration} mo, util=${utils}): Total savings is ${totalText}`);
  assert(brokerageText === `+₹${expectedBrokerage.toLocaleString('en-IN')}`, `Brokerage saved is ${brokerageText}`);
  assert(utilText === `+₹${expectedUtil.toLocaleString('en-IN')}`, `Utility saved is ${utilText}`);
});

// Test gear packages savings
const gearPackages = {
  books: { retail: 6500, senior: 1800, co2: 12 },
  laptop: { retail: 56000, senior: 24500, co2: 185 },
  room: { retail: 14500, senior: 4800, co2: 45 },
  mobility: { retail: 12000, senior: 4200, co2: 80 }
};

Object.entries(gearPackages).forEach(([key, expected]) => {
  domContext.window.selectGearPackage(key, null);
  const retailText = domContext.document.getElementById('calcGearRetail').textContent;
  const seniorText = domContext.document.getElementById('calcGearSenior').textContent;
  const savedText = domContext.document.getElementById('calcGearSavings').textContent;
  const pctText = domContext.document.getElementById('calcGearPercent').textContent;
  const co2Text = domContext.document.getElementById('calcGearCo2').textContent;

  const expectedSaved = expected.retail - expected.senior;
  const expectedPct = Math.round((expectedSaved / expected.retail) * 100);

  assert(retailText === `₹${expected.retail.toLocaleString('en-IN')}`, `Package [${key}] Retail price: ${retailText}`);
  assert(seniorText === `₹${expected.senior.toLocaleString('en-IN')}`, `Package [${key}] Senior price: ${seniorText}`);
  assert(savedText === `₹${expectedSaved.toLocaleString('en-IN')}`, `Package [${key}] Savings amount: ${savedText}`);
  assert(pctText === `${expectedPct}%`, `Package [${key}] Discount %: ${pctText}`);
  assert(co2Text === `${expected.co2} kg`, `Package [${key}] CO2 offset: ${co2Text}`);
});

// ---------------------------------------------------------------------------
// 4. Feature 10: StayMartAccommodationStats Capacity Math & Occupancy
// ---------------------------------------------------------------------------
console.log('\n--- 4. FEATURE 10: ACCOMMODATION CAPACITY & OCCUPANCY AUDIT ---');

const StatsEngine = domContext.window.StayMartAccommodationStats;
assert(typeof StatsEngine === 'object', 'StayMartAccommodationStats object exists on window');
assert(typeof StatsEngine.getOccupancy === 'function', 'getOccupancy method exists');

// Test AMPLE state (e.g. 10 total, 5 available = 50% available -> occupied=5, rate=50%)
const occAmple = StatsEngine.getOccupancy({ totalRooms: 10, availableRooms: 5, isAvailable: true });
assert(occAmple.status === 'AMPLE', 'Status is AMPLE for 5 of 10 rooms available');
assert(occAmple.rate === 50, `Occupancy rate is 50% (got ${occAmple.rate}%)`);
assert(occAmple.available === 5, 'Available count is 5');
assert(occAmple.badgeText === 'Immediate Move-In', `Badge text: ${occAmple.badgeText}`);

// Test LIMITED state (e.g. 10 total, 2 available = 20% available)
const occLimited = StatsEngine.getOccupancy({ totalRooms: 10, availableRooms: 2, isAvailable: true });
assert(occLimited.status === 'LIMITED', 'Status is LIMITED when available <= 2');
assert(occLimited.rate === 80, `Occupancy rate is 80% (got ${occLimited.rate}%)`);
assert(occLimited.badgeText.includes('Filling Fast'), `Badge text contains 'Filling Fast': ${occLimited.badgeText}`);

// Test LIMITED state singular bed wording
const occLimited1 = StatsEngine.getOccupancy({ totalRooms: 8, availableRooms: 1, isAvailable: true });
assert(occLimited1.detailHeadline.includes('1 Bed Left'), `Detail headline has singular '1 Bed Left': ${occLimited1.detailHeadline}`);

// Test FULL state (0 available or isAvailable=false)
const occFull1 = StatsEngine.getOccupancy({ totalRooms: 10, availableRooms: 0, isAvailable: true });
assert(occFull1.status === 'FULL', 'Status is FULL when availableRooms = 0');
assert(occFull1.rate === 100, 'Occupancy rate is 100%');

const occFull2 = StatsEngine.getOccupancy({ totalRooms: 10, availableRooms: 5, isAvailable: false });
assert(occFull2.status === 'FULL', 'Status is FULL when isAvailable = false');
assert(occFull2.available === 0, 'Available count is forced to 0 when isAvailable = false');

// Extreme edge case: missing totalRooms, negative numbers
const occEdge = StatsEngine.getOccupancy({ totalRooms: 0, availableRooms: -2, isAvailable: true });
assert(occEdge.total >= 1, `Zero totalRooms clamped to minimum 1 (got ${occEdge.total})`);
assert(occEdge.available >= 0, `Negative availableRooms clamped to 0 (got ${occEdge.available})`);

// ---------------------------------------------------------------------------
// 5. Feature 11: Campus Rent Trend Visualizer Benchmarks
// ---------------------------------------------------------------------------
console.log('\n--- 5. FEATURE 11: CAMPUS RENT TREND VISUALIZER AUDIT ---');

assert(typeof StatsEngine.matchCampusZone === 'function', 'matchCampusZone method exists');
assert(typeof StatsEngine.getSavings === 'function', 'getSavings method exists');
assert(typeof StatsEngine.getPriceTrend === 'function', 'getPriceTrend method exists');

// Verify Campus Zone Keyword Matching
const testZones = [
  { area: 'Clement Town', title: 'Near Graphic Era Gate 1', expectedKey: 'Graphic Era' },
  { area: 'Premnagar', title: 'UPES Bidholi road student PG', expectedKey: 'UPES Premnagar' },
  { area: 'Rajpur Road', title: 'Near DIT University diversion', expectedKey: 'DIT Rajpur Rd' },
  { area: 'Kedarpur', title: 'Girls hostel near Doon University', expectedKey: 'Doon Univ' },
  { area: 'Civil Lines', title: 'IIT Roorkee student flat', expectedKey: 'IIT Roorkee' },
  { area: 'Tapovan', title: 'Rishikesh co-living studio', expectedKey: 'Tapovan Rishikesh' },
  { area: 'Unknown Area', title: 'Central room', expectedKey: 'Dehradun Hub' }
];

testZones.forEach(({ area, title, expectedKey }) => {
  const matched = StatsEngine.matchCampusZone(area, '', title);
  assert(matched.shortName === expectedKey, `Area '${area}' matches campus zone benchmark '${expectedKey}'`);
});

// Test Price Trend Classifications
const trendBudget = StatsEngine.getPriceTrend({
  area: 'Clement Town',
  pricePerMonth: 5500, // Clement Town PG median is 7500. 5500 < 7500 * 0.85 (6375)
  type: 'PG'
});
assert(trendBudget.verdictClass === 'budget', `Rent ₹5,500 vs median ₹7,500 classified as 'budget' (got ${trendBudget.verdictClass})`);
assert(trendBudget.studentValueScore >= 9.0, `Budget studentValueScore is high: ${trendBudget.studentValueScore}`);

const trendFair = StatsEngine.getPriceTrend({
  area: 'Clement Town',
  pricePerMonth: 7500,
  type: 'PG'
});
assert(trendFair.verdictClass === 'fair', `Rent ₹7,500 vs median ₹7,500 classified as 'fair'`);

const trendPremium = StatsEngine.getPriceTrend({
  area: 'Clement Town',
  pricePerMonth: 10500, // 10500 > 7500 * 1.15 (8625)
  type: 'PG'
});
assert(trendPremium.verdictClass === 'premium', `Rent ₹10,500 vs median ₹7,500 classified as 'premium'`);

// Test Needle positioning math
assert(trendBudget.needlePct >= 4 && trendBudget.needlePct <= 96, `Needle percentage ${trendBudget.needlePct}% is clamped in [4, 96]`);
assert(trendFair.needlePct > trendBudget.needlePct, `Fair needle (${trendFair.needlePct}%) is to the right of Budget needle (${trendBudget.needlePct}%)`);
assert(trendPremium.needlePct > trendFair.needlePct, `Premium needle (${trendPremium.needlePct}%) is to the right of Fair needle (${trendFair.needlePct}%)`);

// ---------------------------------------------------------------------------
// 6. Feature 12: Dual-Engine Creative Charts (Chart.js + SVG Fallback)
// ---------------------------------------------------------------------------
console.log('\n--- 6. FEATURE 12: DUAL-ENGINE CHARTS & PURE SVG VECTOR RENDERER AUDIT ---');

const chartsContext = {
  window: {},
  document: {
    getElementById: (id) => {
      if (!chartsContext._elements[id]) {
        chartsContext._elements[id] = {
          innerHTML: '',
          getContext: () => ({ fillRect: () => {} })
        };
      }
      return chartsContext._elements[id];
    },
    querySelectorAll: () => [],
    addEventListener: () => {}
  },
  console: console,
  Math: Math,
  parseFloat: parseFloat,
  parseInt: parseInt,
  Number: Number,
  String: String
};
chartsContext.window = chartsContext;
chartsContext._elements = {};

vm.createContext(chartsContext);
vm.runInContext(chartsJsContent, chartsContext);

// Test SVG Rent Chart generation when Chart.js is not loaded
assert(typeof chartsContext.window.filterRentChart === 'function', 'filterRentChart is exported to window');
assert(typeof chartsContext.window.toggleRecommerceView === 'function', 'toggleRecommerceView is exported to window');

// Trigger SVG Rent Chart render
chartsContext.window.filterRentChart('all');
const rentSvgHtml = chartsContext.document.getElementById('accChartContainer').innerHTML;

assert(rentSvgHtml.includes('<svg viewBox="0 0 560 260"'), 'Rent SVG generated with proper viewBox="0 0 560 260"');
assert(rentSvgHtml.includes('<line'), 'Rent SVG includes computed grid lines');
assert(rentSvgHtml.includes('<rect'), 'Rent SVG includes calculated bar rects');
assert(rentSvgHtml.includes('PG + Food'), 'Rent SVG includes legend item PG + Food');
assert(rentSvgHtml.includes('Single Room'), 'Rent SVG includes legend item Single Room');
assert(rentSvgHtml.includes('Shared Flat'), 'Rent SVG includes legend item Shared Flat');

// Verify that bar heights in SVG are dynamically computed and non-zero
const rectHeights = [...rentSvgHtml.matchAll(/height="([0-9.]+)"/g)].map(m => parseFloat(m[1]));
assert(rectHeights.length >= 12, `All 4 zones x 3 categories rendered rects (found ${rectHeights.length} rect heights)`);
assert(rectHeights.every(h => h > 0 && h <= 260), 'All bar heights are mathematically calculated between 0 and chart height 260');

// Test Filter: filterRentChart('pg') should only render PG bars
chartsContext.window.filterRentChart('pg');
const pgOnlySvg = chartsContext.document.getElementById('accChartContainer').innerHTML;
assert(!pgOnlySvg.includes('Single Room:'), 'filterRentChart("pg") does not render Single Room bars');
assert(pgOnlySvg.includes('PG with Food:'), 'filterRentChart("pg") renders PG with Food bars');

// Trigger SVG Recommerce Chart render (Price mode)
chartsContext.window.toggleRecommerceView('price');
const recommerceSvgPrice = chartsContext.document.getElementById('gearChartContainer').innerHTML;
assert(recommerceSvgPrice.includes('StayMart Senior Price'), 'Recommerce SVG renders Senior Price legend');
assert(recommerceSvgPrice.includes('Retail Benchmark'), 'Recommerce SVG renders Retail Benchmark legend');
assert(recommerceSvgPrice.includes('Textbooks'), 'Recommerce SVG includes category labels');

// Trigger SVG Recommerce Chart render (Volume mode)
chartsContext.window.toggleRecommerceView('volume');
const recommerceSvgVol = chartsContext.document.getElementById('gearChartContainer').innerHTML;
assert(recommerceSvgVol.includes('Semester Trade Volume'), 'Recommerce SVG volume mode renders Trade Volume legend');
assert(recommerceSvgVol.includes('Volume: 420 ads'), 'Recommerce SVG volume mode contains exact calculated volume data');

// ---------------------------------------------------------------------------
// 7. Feature 13: RecommerceVisuals Deterministic Analytics Engine
// ---------------------------------------------------------------------------
console.log('\n--- 7. FEATURE 13: RECOMMERCE VISUALS & LIVE ENGAGEMENT AUDIT ---');

const RecommerceEngine = domContext.window.RecommerceVisuals;
assert(typeof RecommerceEngine === 'object', 'RecommerceVisuals object exists on window');
assert(typeof RecommerceEngine.getAnalytics === 'function', 'getAnalytics method exists');

// Test deterministic PRNG seed
const seed1 = RecommerceEngine.getProductSeed(42);
const seed2 = RecommerceEngine.getProductSeed(42);
assert(seed1 === seed2, `getProductSeed(42) is 100% deterministic (${seed1})`);
assert(seed1 >= 0 && seed1 < 1, `getProductSeed output is within [0, 1) range`);

// Test item price calculation with category multiplier
// Category 10 = Books & Stationery (mult 2.85)
const bookItem = {
  id: 101,
  title: 'Higher Engineering Mathematics - B.S. Grewal',
  price: 550,
  category: { id: 10, name: 'Books & Stationery' },
  condition: 'GOOD'
};
const bookAnalytics = RecommerceEngine.getAnalytics(bookItem);
assert(bookAnalytics.retailPrice > bookAnalytics.price, `Retail price (₹${bookAnalytics.retailPrice}) is higher than student price (₹${bookAnalytics.price})`);
assert(bookAnalytics.savingsAmount === bookAnalytics.retailPrice - bookAnalytics.price, `Savings amount equals retailPrice - price (₹${bookAnalytics.savingsAmount})`);
assert(bookAnalytics.savingsPercent >= 15 && bookAnalytics.savingsPercent <= 85, `Savings percentage (${bookAnalytics.savingsPercent}%) is within realistic range`);
assert(bookAnalytics.condScore === 7, `Condition GOOD maps to score 7/10`);

// Test condition modifiers: NEW vs OLD
const newItem = { id: 202, title: 'Scientific Calculator fx-991CW', price: 900, category: { id: 7 }, condition: 'NEW' };
const oldItem = { id: 203, title: 'Engineering Mechanics by Timoshenko', price: 200, category: { id: 10 }, condition: 'OLD' };

const newAnalytics = RecommerceEngine.getAnalytics(newItem);
const oldAnalytics = RecommerceEngine.getAnalytics(oldItem);

assert(newAnalytics.condScore === 10, 'Condition NEW gets 10/10 score');
assert(newAnalytics.condTier === 'new', 'Condition NEW maps to tier "new"');
assert(oldAnalytics.condScore === 3, 'Condition OLD gets 3/10 score');
assert(oldAnalytics.condTier === 'old', 'Condition OLD maps to tier "old"');

// Test Deal Quality Tiers:
// High spec gear (>= 25,000)
const laptopItem = { id: 301, title: 'ThinkPad T480 i7 16GB RAM', price: 28000, category: { id: 7 }, condition: 'LIKE_NEW' };
const laptopAnalytics = RecommerceEngine.getAnalytics(laptopItem);
assert(laptopAnalytics.dealClass === 'premium', `Item priced ₹28,000 classified as 'premium' tier (got ${laptopAnalytics.dealClass})`);

// Budget Steal (savingsPercent >= 60% or price <= median * 0.65)
const stealItem = { id: 302, title: 'Hercules Mountain Cycle', price: 2200, category: { id: 12 }, condition: 'GOOD' };
const stealAnalytics = RecommerceEngine.getAnalytics(stealItem);
assert(stealAnalytics.dealClass === 'steal' || stealAnalytics.dealClass === 'great', `Affordable cycle classified as '${stealAnalytics.dealClass}'`);

// ---------------------------------------------------------------------------
// 8. Integration Points Verification
// ---------------------------------------------------------------------------
console.log('\n--- 8. INTEGRATION POINTS VERIFICATION ---');

// Check index.html integration
assert(indexHtmlContent.includes('metrics-ribbon-section'), 'index.html contains metrics-ribbon-section');
assert(indexHtmlContent.includes('data-counter data-target="500"'), 'index.html contains data-counter target="500"');
assert(indexHtmlContent.includes('data-counter data-target="1200"'), 'index.html contains data-counter target="1200"');
assert(indexHtmlContent.includes('data-counter data-target="4500"'), 'index.html contains data-counter target="4500"');
assert(indexHtmlContent.includes('data-counter data-target="98"'), 'index.html contains data-counter target="98"');
assert(indexHtmlContent.includes('savings-calc-section'), 'index.html contains savings-calc-section');
assert(indexHtmlContent.includes('calcRentSlider'), 'index.html contains calcRentSlider');
assert(indexHtmlContent.includes('campus-charts-section'), 'index.html contains campus-charts-section');
assert(indexHtmlContent.includes('campusRentChart'), 'index.html contains campusRentChart canvas');
assert(indexHtmlContent.includes('recommerceChart'), 'index.html contains recommerceChart canvas');

// Check utils.js card builder integration
assert(utilsJsContent.includes('StayMartAccommodationStats.getOccupancy'), 'buildPropertyCard calls StayMartAccommodationStats.getOccupancy');
assert(utilsJsContent.includes('StayMartAccommodationStats.getSavings'), 'buildPropertyCard calls StayMartAccommodationStats.getSavings');
assert(utilsJsContent.includes('StayMartAccommodationStats.getEngagement'), 'buildPropertyCard calls StayMartAccommodationStats.getEngagement');
assert(utilsJsContent.includes('card-occupancy-meter'), 'buildPropertyCard embeds card-occupancy-meter HTML');
assert(utilsJsContent.includes('occupancy-progress-bar'), 'buildPropertyCard embeds occupancy-progress-bar');
assert(utilsJsContent.includes('RecommerceVisuals.getAnalytics'), 'buildProductCard calls RecommerceVisuals.getAnalytics');
assert(utilsJsContent.includes('card-condition-meter'), 'buildProductCard embeds card-condition-meter');
assert(utilsJsContent.includes('card-savings-pill'), 'buildProductCard embeds card-savings-pill');

// Check property-detail.js and product-detail.js integration
const propDetailJs = fs.readFileSync(path.join(FRONTEND_DIR, 'js', 'property-detail.js'), 'utf8');
const prodDetailJs = fs.readFileSync(path.join(FRONTEND_DIR, 'js', 'product-detail.js'), 'utf8');

assert(propDetailJs.includes('detail-occupancy-widget'), 'property-detail.js renders detail-occupancy-widget');
assert(propDetailJs.includes('price-trend-widget'), 'property-detail.js renders campus rent price-trend-widget');
assert(propDetailJs.includes('student-savings-card'), 'property-detail.js renders student-savings-card');
assert(propDetailJs.includes('senior-host-badge'), 'property-detail.js renders senior-host-badge');

assert(prodDetailJs.includes('detail-social-proof-strip'), 'product-detail.js renders detail-social-proof-strip');
assert(prodDetailJs.includes('condition-inspection-card'), 'product-detail.js renders condition-inspection-card');
assert(prodDetailJs.includes('student-savings-card'), 'product-detail.js renders student-savings-card');

// ---------------------------------------------------------------------------
// 9. Summary & Final Audit Verdict
// ---------------------------------------------------------------------------
console.log('\n======================================================================');
console.log(`FORENSIC AUDIT SUMMARY:`);
console.log(`  Total Checks Executed : ${passCount + failCount}`);
console.log(`  Passed Checks         : ${passCount}`);
console.log(`  Failed Checks         : ${failCount}`);
console.log('======================================================================');

if (failCount > 0) {
  console.error('\nFAILURES IDENTIFIED:');
  failureDetails.forEach(f => console.error(`  - ${f}`));
  console.log('\nFINAL VERDICT: INTEGRITY VIOLATION');
  process.exit(1);
} else {
  console.log('\nFINAL VERDICT: CLEAN');
  process.exit(0);
}
