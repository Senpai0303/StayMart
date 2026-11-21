/**
 * Milestone 2 Challenger 2: Adversarial Logic & Fallback Stress Test Suite
 * Evaluates:
 * 1. StayMartAccommodationStats edge cases:
 *    - 0 total rooms, 0 available rooms, negative rent, astronomical rent,
 *    - null/undefined properties, missing amenities array
 * 2. RecommerceVisuals edge cases:
 *    - 0 price, null category, missing description, retail price lower than listing price
 * 3. Savings Calculator edge cases:
 *    - Slider at minimum (₹5,000), slider at maximum (₹25,000)
 *    - Rapid mode switching between Accommodation and Gear packages
 * 4. Dual-Engine Charts & Fallback stress:
 *    - Chart.js CDN blocked / offline fallback to responsive SVG
 *    - SVG chart viewBox & responsive container scaling
 *    - Interactive SVG filter switching without Chart.js
 * 5. Headless Chrome Playwright verification with simulated offline CDN & Detail Pages
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const { chromium } = require('C:/Users/divya/AppData/Local/Programs/Python/Python312/Lib/site-packages/playwright/driver/package');

const BASE_DIR = path.resolve(__dirname, '..');
const FRONTEND_DIR = path.join(BASE_DIR, 'frontend');
const STATS_PATH = path.join(FRONTEND_DIR, 'js', 'stats.js');
const CHARTS_PATH = path.join(FRONTEND_DIR, 'js', 'charts.js');
const UTILS_PATH = path.join(FRONTEND_DIR, 'js', 'utils.js');

const statsCode = fs.readFileSync(STATS_PATH, 'utf8');
const chartsCode = fs.readFileSync(CHARTS_PATH, 'utf8');

const testReport = {
  timestamp: new Date().toISOString(),
  suites: [],
  passedCount: 0,
  failedCount: 0,
  totalCount: 0,
  findings: []
};

function recordTest(suiteName, testName, passed, details) {
  testReport.totalCount++;
  if (passed) {
    testReport.passedCount++;
  } else {
    testReport.failedCount++;
    testReport.findings.push({ suite: suiteName, test: testName, details });
  }
  const statusStr = passed ? '[PASS]' : '[FAIL]';
  console.log(`  ${statusStr} ${testName}`);
  if (details && !passed) {
    console.log(`         Details: ${JSON.stringify(details)}`);
  }
}

// -----------------------------------------------------------------------------
// SUITE 1: StayMartAccommodationStats Edge Cases
// -----------------------------------------------------------------------------
console.log('\n===============================================================');
console.log('SUITE 1: StayMartAccommodationStats Adversarial Edge Cases');
console.log('===============================================================');

function createStatsContext() {
  const context = {
    window: {},
    document: {
      querySelectorAll: () => [],
      getElementById: () => null,
      querySelector: () => null,
      addEventListener: () => {}
    },
    performance: { now: () => Date.now() },
    requestAnimationFrame: (cb) => setTimeout(cb, 16),
    console: console,
    Math: Math,
    Number: Number,
    parseInt: parseInt,
    parseFloat: parseFloat,
    String: String,
    Object: Object
  };
  context.window = context;
  vm.createContext(context);
  vm.runInContext(statsCode, context);
  return context;
}

const statsCtx = createStatsContext();
const stats = statsCtx.window.StayMartAccommodationStats;

// Test 1.1: 0 Total Rooms
try {
  const res = stats.getOccupancy({ totalRooms: 0, availableRooms: 0 });
  const passed = res.total === 1 && !isNaN(res.rate) && res.status === 'FULL';
  recordTest('StayMartAccommodationStats', 'Edge Case: 0 Total Rooms (clamped to 1, no NaN rate)', passed, res);
} catch (err) {
  recordTest('StayMartAccommodationStats', 'Edge Case: 0 Total Rooms', false, err.message);
}

// Test 1.2: 0 Available Rooms (100% Full)
try {
  const res = stats.getOccupancy({ totalRooms: 6, availableRooms: 0 });
  const passed = res.total === 6 && res.available === 0 && res.occupied === 6 && res.rate === 100 && res.status === 'FULL' && res.badgeText === 'Fully Occupied';
  recordTest('StayMartAccommodationStats', 'Edge Case: 0 Available Rooms (100% Full -> FULL status, rate 100)', passed, res);
} catch (err) {
  recordTest('StayMartAccommodationStats', 'Edge Case: 0 Available Rooms', false, err.message);
}

// Test 1.3: Negative Rent
try {
  const savings = stats.getSavings({ pricePerMonth: -6000, area: 'Clement Town', type: 'PG' });
  const trend = stats.getPriceTrend({ pricePerMonth: -6000, area: 'Clement Town', type: 'PG' });
  const passed = !isNaN(savings.diff) && !isNaN(savings.annualTotal) && !isNaN(trend.needlePct) && trend.needlePct >= 4 && trend.needlePct <= 96;
  recordTest('StayMartAccommodationStats', 'Edge Case: Negative Rent (-₹6,000 -> needle clamped [4..96], no NaN)', passed, { savings, trend });
} catch (err) {
  recordTest('StayMartAccommodationStats', 'Edge Case: Negative Rent', false, err.message);
}

// Test 1.4: Astronomical Rent (₹1,00,000+)
try {
  const savings = stats.getSavings({ pricePerMonth: 150000, area: 'Rajpur Road', type: 'FLAT' });
  const trend = stats.getPriceTrend({ pricePerMonth: 150000, area: 'Rajpur Road', type: 'FLAT' });
  const passed = !isNaN(savings.diff) && trend.needlePct === 96 && trend.verdictClass === 'premium' && trend.verdictBadge.includes('Premium');
  recordTest('StayMartAccommodationStats', 'Edge Case: Astronomical Rent (₹1,50,000 -> clamped needle 96, premium class)', passed, { savings, trend });
} catch (err) {
  recordTest('StayMartAccommodationStats', 'Edge Case: Astronomical Rent', false, err.message);
}

// Test 1.5: Null/Undefined Property & Empty Object Handling
try {
  let nullOccupancyThrew = false;
  let undefinedSavingsThrew = false;
  try {
    stats.getOccupancy(null);
  } catch (e) {
    nullOccupancyThrew = (e.name === 'TypeError' || (e instanceof TypeError));
  }
  try {
    stats.getSavings(undefined);
  } catch (e) {
    undefinedSavingsThrew = (e.name === 'TypeError' || (e instanceof TypeError));
  }
  const emptyOccupancy = stats.getOccupancy({});
  const emptySavings = stats.getSavings({});
  const emptyTrend = stats.getPriceTrend({});
  const emptyEngagement = stats.getEngagement(null);
  const emptySafe = !isNaN(emptyOccupancy.total) && !isNaN(emptySavings.brokerage) && !isNaN(emptyTrend.needlePct) && emptyEngagement.viewsThisWeek > 0;
  
  recordTest('StayMartAccommodationStats', 'Edge Case: Null/Undefined Property & Empty Object Handling', emptySafe && nullOccupancyThrew && undefinedSavingsThrew, {
    emptyOccupancy,
    emptySavings,
    emptyTrend,
    emptyEngagement,
    nullOccupancyThrew,
    undefinedSavingsThrew
  });
} catch (err) {
  recordTest('StayMartAccommodationStats', 'Edge Case: Null/Undefined Property Handling', false, err.message);
}

// Test 1.6: Missing Amenities Array
try {
  const res = stats.getOccupancy({ totalRooms: 4, availableRooms: 2, amenities: null });
  const passed = res.total === 4 && res.available === 2;
  recordTest('StayMartAccommodationStats', 'Edge Case: Missing Amenities Array (null / undefined does not affect stats)', passed, res);
} catch (err) {
  recordTest('StayMartAccommodationStats', 'Edge Case: Missing Amenities Array', false, err.message);
}

// -----------------------------------------------------------------------------
// SUITE 2: RecommerceVisuals Deterministic Analytics Edge Cases
// -----------------------------------------------------------------------------
console.log('\n===============================================================');
console.log('SUITE 2: RecommerceVisuals Adversarial Edge Cases');
console.log('===============================================================');

const recommerce = statsCtx.window.RecommerceVisuals;

// Test 2.1: 0 Price
try {
  const res = recommerce.getAnalytics({ id: 101, title: 'Old Study Table', price: 0 });
  const passed = res.price === 1 && res.retailPrice >= res.price && !isNaN(res.savingsPercent) && res.savingsPercent >= 15;
  recordTest('RecommerceVisuals', 'Edge Case: 0 Price (clamped to 1, valid retail, valid savings, no NaN)', passed, res);
} catch (err) {
  recordTest('RecommerceVisuals', 'Edge Case: 0 Price', false, err.message);
}

// Test 2.2: Null Category
try {
  const res = recommerce.getAnalytics({ id: 102, title: 'Engineering Drafting Tool', price: 800, category: null });
  const passed = res.categoryMedian === 4500 && res.categoryName === 'Others' && !isNaN(res.retailPrice);
  recordTest('RecommerceVisuals', 'Edge Case: Null Category (falls back gracefully to Others category median 4500)', passed, res);
} catch (err) {
  recordTest('RecommerceVisuals', 'Edge Case: Null Category', false, err.message);
}

// Test 2.3: Missing Description & Missing Title
try {
  const res = recommerce.getAnalytics({ id: 103, price: 1500 });
  const passed = res.price === 1500 && res.retailPrice > 1500 && res.condScore > 0 && res.campusAffiliation.length > 0;
  recordTest('RecommerceVisuals', 'Edge Case: Missing Description & Title (defaults safely without errors)', passed, res);
} catch (err) {
  recordTest('RecommerceVisuals', 'Edge Case: Missing Description & Title', false, err.message);
}

// Test 2.4: Retail Price Lower Than Listing Price Handling
try {
  const res1 = recommerce.getAnalytics({ id: 104, title: 'Custom Desktop PC', price: 65000, condition: 'NEW' });
  const res2 = recommerce.getAnalytics({ id: 105, title: 'Item at 999999', price: 999999, condition: 'NEW' });
  const passed = res1.retailPrice > res1.price && res1.savingsAmount > 0 && res2.retailPrice > res2.price && res2.savingsAmount > 0;
  recordTest('RecommerceVisuals', 'Edge Case: Retail Price Lower Than Listing Price (enforces retailPrice > price margin)', passed, {
    item1: { price: res1.price, retail: res1.retailPrice, savings: res1.savingsAmount },
    item2: { price: res2.price, retail: res2.retailPrice, savings: res2.savingsAmount }
  });
} catch (err) {
  recordTest('RecommerceVisuals', 'Edge Case: Retail Price Lower Than Listing Price', false, err.message);
}

// -----------------------------------------------------------------------------
// SUITE 3: Interactive Savings Calculator Edge Cases
// -----------------------------------------------------------------------------
console.log('\n===============================================================');
console.log('SUITE 3: Interactive Dual-Mode Calculator Edge Cases');
console.log('===============================================================');

class MockClassList {
  constructor(initial = []) {
    this.classes = new Set(initial);
  }
  add(cls) { this.classes.add(cls); }
  remove(cls) { this.classes.delete(cls); }
  toggle(cls, force) {
    if (force !== undefined) {
      if (force) this.classes.add(cls); else this.classes.delete(cls);
      return force;
    }
    if (this.classes.has(cls)) { this.classes.delete(cls); return false; }
    this.classes.add(cls); return true;
  }
  contains(cls) { return this.classes.has(cls); }
}

function createCalculatorDomContext() {
  const domState = {
    calcRentSlider: { value: '9000' },
    calcRentDisplay: { textContent: '' },
    calcIncludeMeals: { checked: true },
    calcIncludeUtilities: { checked: true },
    calcAccTotalSavings: { textContent: '' },
    cbBrokerageVal: { textContent: '' },
    cbUtilityVal: { textContent: '' },
    cbMealRow: { style: { display: '' } },
    cbMealVal: { textContent: '' },
    cbBrokerCost: { textContent: '' },
    cbStaymartCost: { textContent: '' },
    cbSavingsBar: { style: { width: '' } },
    calcAccCta: { href: '' },
    calcModeAccBtn: { classList: new MockClassList(['active']), setAttribute: () => {}, removeAttribute: () => {} },
    calcModeGearBtn: { classList: new MockClassList(), setAttribute: () => {}, removeAttribute: () => {} },
    calcPaneAccommodation: { classList: new MockClassList(['active']), style: { display: 'block' } },
    calcPaneGear: { classList: new MockClassList(), style: { display: 'none' } },
    calcGearRetail: { textContent: '' },
    calcGearSenior: { textContent: '' },
    calcGearSavings: { textContent: '' },
    calcGearPercent: { textContent: '' },
    calcGearCo2: { textContent: '' },
    calcGearCta: { href: '' }
  };

  const context = {
    window: {},
    document: {
      getElementById: (id) => domState[id] || null,
      querySelectorAll: () => [],
      querySelector: () => null,
      addEventListener: () => {}
    },
    performance: { now: () => Date.now() },
    requestAnimationFrame: (cb) => setTimeout(cb, 16),
    console: console,
    Math: Math,
    Number: Number,
    parseInt: parseInt,
    parseFloat: parseFloat,
    String: String,
    Object: Object
  };
  context.window = context;
  vm.createContext(context);
  vm.runInContext(statsCode, context);
  return { context, domState };
}

const calcEnv = createCalculatorDomContext();

// Test 3.1: Slider at Minimum (₹5,000)
try {
  calcEnv.domState.calcRentSlider.value = '5000';
  calcEnv.context.updateAccommodationCalc();
  const savingsText = calcEnv.domState.calcAccTotalSavings.textContent;
  const brokerageText = calcEnv.domState.cbBrokerageVal.textContent;
  const staymartCost = calcEnv.domState.cbStaymartCost.textContent;
  const brokerCost = calcEnv.domState.cbBrokerCost.textContent;
  const ctaHref = calcEnv.domState.calcAccCta.href;
  const passed = savingsText.includes('17,000') && brokerageText.includes('5,000') && ctaHref.includes('maxPrice=5000');
  recordTest('Calculator', 'Edge Case: Slider at Minimum ₹5,000 (Brokerage ₹5k, Bundle ₹17k, CTA param maxPrice=5000)', passed, {
    savingsText, brokerageText, staymartCost, brokerCost, ctaHref
  });
} catch (err) {
  recordTest('Calculator', 'Edge Case: Slider at Minimum ₹5,000', false, err.message);
}

// Test 3.2: Slider at Maximum (₹25,000)
try {
  calcEnv.domState.calcRentSlider.value = '25000';
  calcEnv.context.updateAccommodationCalc();
  const savingsText = calcEnv.domState.calcAccTotalSavings.textContent;
  const brokerageText = calcEnv.domState.cbBrokerageVal.textContent;
  const staymartCost = calcEnv.domState.cbStaymartCost.textContent;
  const brokerCost = calcEnv.domState.cbBrokerCost.textContent;
  const ctaHref = calcEnv.domState.calcAccCta.href;
  const passed = savingsText.includes('37,000') && brokerageText.includes('25,000') && ctaHref.includes('maxPrice=25000');
  recordTest('Calculator', 'Edge Case: Slider at Maximum ₹25,000 (Brokerage ₹25k, Bundle ₹37k, CTA param maxPrice=25000)', passed, {
    savingsText, brokerageText, staymartCost, brokerCost, ctaHref
  });
} catch (err) {
  recordTest('Calculator', 'Edge Case: Slider at Maximum ₹25,000', false, err.message);
}

// Test 3.3: Rapid Mode Switching between Accommodation and Gear packages
try {
  let modeSwitchSuccess = true;
  for (let i = 0; i < 50; i++) {
    const targetMode = i % 2 === 0 ? 'gear' : 'accommodation';
    calcEnv.context.switchCalcMode(targetMode);
    if (targetMode === 'gear') {
      if (calcEnv.domState.calcPaneGear.style.display !== 'block' || calcEnv.domState.calcPaneAccommodation.style.display !== 'none') {
        modeSwitchSuccess = false;
        break;
      }
    } else {
      if (calcEnv.domState.calcPaneAccommodation.style.display !== 'block' || calcEnv.domState.calcPaneGear.style.display !== 'none') {
        modeSwitchSuccess = false;
        break;
      }
    }
  }
  recordTest('Calculator', 'Edge Case: 50x Rapid Mode Switching (maintains active pane display & sync without leaks)', modeSwitchSuccess);
} catch (err) {
  recordTest('Calculator', 'Edge Case: Rapid Mode Switching', false, err.message);
}

// -----------------------------------------------------------------------------
// SUITE 4: Dual-Engine Creative Visual Charts & Fallbacks
// -----------------------------------------------------------------------------
console.log('\n===============================================================');
console.log('SUITE 4: Dual-Engine Charts & Offline SVG Fallback');
console.log('===============================================================');

function createChartsDomContext() {
  const domContainers = {
    accChartContainer: { innerHTML: '' },
    gearChartContainer: { innerHTML: '' }
  };

  const context = {
    window: {},
    document: {
      getElementById: (id) => domContainers[id] || null,
      querySelectorAll: () => [],
      addEventListener: () => {}
    },
    console: console,
    Math: Math,
    Number: Number,
    parseInt: parseInt,
    parseFloat: parseFloat,
    String: String,
    Object: Object
  };
  context.window = context;
  vm.createContext(context);
  vm.runInContext(chartsCode, context);
  return { context, domContainers };
}

const chartsEnv = createChartsDomContext();

// Test 4.1: Offline / Blocked CDN Triggering Zero-Dependency SVG
try {
  chartsEnv.context.initPublicCharts();
  const rentSvg = chartsEnv.domContainers.accChartContainer.innerHTML;
  const gearSvg = chartsEnv.domContainers.gearChartContainer.innerHTML;
  const hasRentSvg = rentSvg.includes('<svg') && rentSvg.includes('viewBox="0 0 560 260"') && rentSvg.includes('preserveAspectRatio="xMidYMid meet"');
  const hasGearSvg = gearSvg.includes('<svg') && gearSvg.includes('viewBox="0 0 560 260"') && gearSvg.includes('preserveAspectRatio="xMidYMid meet"');
  const passed = hasRentSvg && hasGearSvg;
  recordTest('DualEngineCharts', 'Offline Fallback: Zero-Dependency Responsive SVG rendered cleanly with viewBox="0 0 560 260"', passed, {
    rentSvgLength: rentSvg.length,
    gearSvgLength: gearSvg.length
  });
} catch (err) {
  recordTest('DualEngineCharts', 'Offline Fallback: SVG Rendering', false, err.message);
}

// Test 4.2: Interactive SVG Filter Switching Without Chart.js
try {
  // Test PG only filter
  chartsEnv.context.filterRentChart('pg');
  const pgOnlySvg = chartsEnv.domContainers.accChartContainer.innerHTML;
  const hasPgData = pgOnlySvg.includes('<title>PG with Food:');
  const hasSingleData = pgOnlySvg.includes('<title>Single Room:');
  const hasFlatData = pgOnlySvg.includes('<title>Shared Flat:');

  // Test Flat only filter
  chartsEnv.context.filterRentChart('flat');
  const flatOnlySvg = chartsEnv.domContainers.accChartContainer.innerHTML;
  const hasFlatOnlyData = flatOnlySvg.includes('<title>Shared Flat:');
  const hasFlatNoPg = !flatOnlySvg.includes('<title>PG with Food:');
  const hasFlatNoSingle = !flatOnlySvg.includes('<title>Single Room:');

  // Test Volume view toggle on recommerce chart
  chartsEnv.context.toggleRecommerceView('volume');
  const volumeSvg = chartsEnv.domContainers.gearChartContainer.innerHTML;
  const hasVolumeBars = volumeSvg.includes('Semester Trade Volume (Ads)') && volumeSvg.includes('Volume: 420 ads');

  const passed = hasPgData && !hasSingleData && !hasFlatData && hasFlatOnlyData && hasFlatNoPg && hasFlatNoSingle && hasVolumeBars;
  recordTest('DualEngineCharts', 'Interactive Filter Toggling in SVG Fallback Mode (correctly isolates dataset bars)', passed, {
    pgFilterCorrect: hasPgData && !hasSingleData && !hasFlatData,
    flatFilterCorrect: hasFlatOnlyData && hasFlatNoPg && hasFlatNoSingle,
    volumeToggleCorrect: hasVolumeBars
  });
} catch (err) {
  recordTest('DualEngineCharts', 'Interactive Filter Toggling in SVG', false, err.message);
}

// -----------------------------------------------------------------------------
// SUITE 5: Real Headless Chrome (Playwright) Offline CDN Simulation & Detail Pages
// -----------------------------------------------------------------------------
async function runPlaywrightStress() {
  console.log('\n===============================================================');
  console.log('SUITE 5: Playwright Headless Chrome Offline CDN Simulation');
  console.log('===============================================================');

  let browser;
  try {
    browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();

    const consoleErrors = [];
    page.on('console', msg => {
      // Ignore network errors caused by external CDNs/fonts
      if (msg.type() === 'error' && !msg.text().includes('net::ERR_')) {
        consoleErrors.push(msg.text());
      }
    });
    page.on('pageerror', err => {
      consoleErrors.push(err.message);
    });

    // Mock API requests for StayMart backend
    await page.route('**', async route => {
      const url = route.request().url();
      if (url.includes('cdn.jsdelivr.net') || url.includes('chartjs')) {
        return route.abort();
      }
      if (url.includes('/api/properties/1')) {
        return route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            success: true,
            data: {
              id: 1,
              title: 'Shivalik Valley PG & Student Hostels',
              type: 'PG',
              pricePerMonth: 8500,
              totalRooms: 12,
              availableRooms: 3,
              isAvailable: true,
              area: 'Clement Town',
              address: 'Bell Road, Clement Town, Dehradun',
              genderPreference: 'BOYS',
              amenities: ['WiFi', 'Power Backup', 'Meals Included', 'RO Water'],
              location: { id: 1, city: 'Dehradun', state: 'Uttarakhand' },
              postedBy: { id: 5, name: 'Vikram Joshi', phone: '9876543210' },
              images: []
            }
          })
        });
      }
      if (url.includes('/api/products/1')) {
        return route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            success: true,
            data: {
              id: 1,
              title: 'Casio Scientific Calculator fx-991EX Classwiz',
              description: 'Barely used for 1 semester in 1st year mechanical engineering.',
              price: 950,
              condition: 'LIKE_NEW',
              listingType: 'SELL',
              isAvailable: true,
              area: 'Prem Nagar',
              category: { id: 10, name: 'Books & Stationery' },
              location: { id: 1, city: 'Dehradun' },
              postedBy: { id: 8, name: 'Ananya Sharma' },
              images: [],
              viewsCount: 45
            }
          })
        });
      }
      if (url.includes('/api/')) {
        return route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({ success: true, data: [] })
        });
      }
      return route.continue();
    });

    const indexPath = 'file:///' + path.join(FRONTEND_DIR, 'index.html').replace(/\\/g, '/');

    // 1. Test 375px mobile viewport with blocked Chart.js CDN
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto(indexPath, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(600);

    const svgRentCount = await page.$$eval('#accChartContainer svg', svgs => svgs.length);
    const svgGearCount = await page.$$eval('#gearChartContainer svg', svgs => svgs.length);
    const svgRentBox = await page.$eval('#accChartContainer svg', el => {
      const rect = el.getBoundingClientRect();
      return { width: rect.width, height: rect.height };
    });

    const isSvgRenderedMobile = svgRentCount === 1 && svgGearCount === 1 && svgRentBox.width > 0;
    recordTest('PlaywrightBrowser', 'Mobile 375px: SVG fallback renders cleanly when Chart.js CDN is blocked', isSvgRenderedMobile, {
      svgRentCount, svgGearCount, svgRentBox
    });

    // 2. Test SVG responsive resize from 375px to 1280px desktop
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.waitForTimeout(300);

    const svgRentBoxDesktop = await page.$eval('#accChartContainer svg', el => {
      const rect = el.getBoundingClientRect();
      return { width: rect.width, height: rect.height };
    });

    const isSvgResized = svgRentBoxDesktop.width > svgRentBox.width;
    recordTest('PlaywrightBrowser', 'Desktop 1280px: SVG chart expands responsively with viewport width', isSvgResized, {
      mobileWidth: svgRentBox.width,
      desktopWidth: svgRentBoxDesktop.width
    });

    // 3. Test interactive UI clicking under blocked CDN
    await page.click('#calcModeGearBtn');
    await page.waitForTimeout(100);
    const gearPaneVisible = await page.$eval('#calcPaneGear', el => window.getComputedStyle(el).display !== 'none');

    const filterBtn = await page.$('#accChartFilter .chart-pill:nth-child(2)');
    if (filterBtn) {
      await filterBtn.click();
      await page.waitForTimeout(100);
    }
    const svgAfterFilter = await page.$eval('#accChartContainer', el => el.innerHTML);
    const filterExecuted = svgAfterFilter.includes('<svg') && gearPaneVisible;

    recordTest('PlaywrightBrowser', 'In-browser interaction: Mode toggling & SVG filter clicks function with 0 console crashes', filterExecuted && consoleErrors.length === 0, {
      consoleErrors
    });

    // 4. Test property-detail.html with blocked CDN
    const propPath = 'file:///' + path.join(FRONTEND_DIR, 'property-detail.html').replace(/\\/g, '/') + '?id=1';
    await page.goto(propPath, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(600);
    const propOccWidget = await page.$('.detail-occupancy-widget');
    const propTrendGrid = await page.$('.trend-benchmark-grid');
    const propSavingsCard = await page.$('.student-savings-card');
    recordTest('PlaywrightBrowser', 'property-detail.html: Occupancy (.detail-occupancy-widget) & Rent Trends render cleanly', propOccWidget !== null && propTrendGrid !== null && propSavingsCard !== null && consoleErrors.length === 0);

    // 5. Test product-detail.html with blocked CDN
    const prodPath = 'file:///' + path.join(FRONTEND_DIR, 'product-detail.html').replace(/\\/g, '/') + '?id=1';
    await page.goto(prodPath, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(600);
    const prodSavingsCard = await page.$('.student-savings-card');
    const prodConditionCard = await page.$('.condition-inspection-card');
    const prodPriceWidget = await page.$('.price-trend-widget');
    recordTest('PlaywrightBrowser', 'product-detail.html: Condition inspection & student savings render cleanly', prodSavingsCard !== null && prodConditionCard !== null && prodPriceWidget !== null && consoleErrors.length === 0);

    await browser.close();
  } catch (err) {
    recordTest('PlaywrightBrowser', 'Playwright Headless Chrome Verification', false, err.message);
    if (browser) await browser.close();
  }

  // ---------------------------------------------------------------------------
  // Summary & Report Generation
  // ---------------------------------------------------------------------------
  console.log('\n===============================================================');
  console.log('EMPIRICAL ADVERSARIAL STRESS TEST SUMMARY');
  console.log('===============================================================');
  console.log(`Total Stress Tests Executed: ${testReport.totalCount}`);
  console.log(`Passed: ${testReport.passedCount}`);
  console.log(`Failed: ${testReport.failedCount}`);
  const verdict = testReport.failedCount === 0 ? 'APPROVE' : 'REQUEST_CHANGES';
  console.log(`VERDICT: ${verdict}`);

  fs.writeFileSync(
    path.join(__dirname, 'm2_stress_results.json'),
    JSON.stringify(testReport, null, 2),
    'utf8'
  );
}

runPlaywrightStress();
