/**
 * Comprehensive Independent Verification Suite by Milestone 2 Reviewer 1
 * Stress-testing:
 * - Feature 8: Animated Metric Counters
 * - Feature 9: Dual-Mode Interactive Student Savings Calculator
 * - Feature 12: Public Creative Visual Charts & Dual-Engine Fallback
 * - Design System & Viewport Conformance
 * - Integrity Audit
 */

const fs = require('fs');
const path = require('path');
const { chromium } = require('C:/Users/divya/AppData/Local/Programs/Python/Python312/Lib/site-packages/playwright/driver/package');

const BASE_DIR = path.resolve(__dirname, '..');
const FRONTEND_DIR = path.join(BASE_DIR, 'frontend');

async function runReviewerVerification() {
  console.log('===============================================================');
  console.log('REVIEWER 1 (M2): RIGOROUS INDEPENDENT VERIFICATION SUITE');
  console.log('===============================================================');

  const report = {
    feature8Counters: { status: 'PENDING', checks: [] },
    feature9Calculator: { status: 'PENDING', checks: [] },
    feature12Charts: { status: 'PENDING', checks: [] },
    responsiveBreakpoints: { status: 'PENDING', checks: [] },
    integrityAudit: { status: 'PENDING', checks: [] }
  };

  const browser = await chromium.launch({ channel: 'chrome', headless: true });

  try {
    // -------------------------------------------------------------------------
    // TEST 1: Feature 8 - Animated Metric Counters in Headless Chrome
    // -------------------------------------------------------------------------
    console.log('\n--- 1. Testing Feature 8: Animated Metric Counters ---');
    const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
    await page.goto('file:///' + path.join(FRONTEND_DIR, 'index.html').replace(/\\/g, '/'), { waitUntil: 'load' });

    // Wait for IntersectionObserver and animation frames (1.8s duration)
    await page.evaluate(() => {
      // Scroll to trigger IntersectionObserver
      const ribbon = document.querySelector('.metrics-ribbon-section');
      if (ribbon) ribbon.scrollIntoView();
    });
    await new Promise(r => setTimeout(r, 2200));

    const counterResults = await page.evaluate(() => {
      const counters = document.querySelectorAll('[data-counter]');
      const details = [];
      counters.forEach(c => {
        details.push({
          target: c.getAttribute('data-target'),
          prefix: c.getAttribute('data-prefix') || '',
          suffix: c.getAttribute('data-suffix') || '',
          text: c.textContent.trim()
        });
      });
      return details;
    });

    console.log(`Found ${counterResults.length} counter elements:`);
    let allCountersPassed = true;
    counterResults.forEach((cr, idx) => {
      console.log(`  Counter ${idx + 1}: target="${cr.target}", prefix="${cr.prefix}", suffix="${cr.suffix}" -> Rendered Text: "${cr.text}"`);
      // Target text should end with suffix and start with prefix
      const expectedEnd = cr.suffix;
      const expectedStart = cr.prefix;
      const hasPrefix = cr.text.startsWith(expectedStart);
      const hasSuffix = cr.text.endsWith(expectedEnd);
      const isNumeric = /\d+/.test(cr.text);
      const valid = hasPrefix && hasSuffix && isNumeric;
      report.feature8Counters.checks.push({
        counter: idx + 1,
        target: cr.target,
        text: cr.text,
        valid
      });
      if (!valid) allCountersPassed = false;
    });
    report.feature8Counters.status = allCountersPassed ? 'PASS' : 'FAIL';
    console.log(`Feature 8 Verdict: ${report.feature8Counters.status}`);

    // -------------------------------------------------------------------------
    // TEST 2: Feature 9 - Dual-Mode Student Savings Calculator
    // -------------------------------------------------------------------------
    console.log('\n--- 2. Testing Feature 9: Dual-Mode Interactive Calculator ---');
    const calcChecks = await page.evaluate(() => {
      const results = [];

      // A. Check initial accommodation state
      const initialTotal = document.getElementById('calcAccTotalSavings').textContent.trim();
      const initialRent = document.getElementById('calcRentDisplay').textContent.trim();
      const initialCta = document.getElementById('calcAccCta').getAttribute('href');
      results.push({ test: 'Initial Accommodation State', initialTotal, initialRent, initialCta, pass: initialTotal === '₹21,000' && initialRent.includes('9,000') });

      // B. Change Rent Slider to 15,000
      const slider = document.getElementById('calcRentSlider');
      slider.value = 15000;
      window.updateAccommodationCalc();
      const updatedTotal15k = document.getElementById('calcAccTotalSavings').textContent.trim();
      const updatedRent15k = document.getElementById('calcRentDisplay').textContent.trim();
      const updatedCta15k = document.getElementById('calcAccCta').getAttribute('href');
      // Brokerage: 15,000. Utilities (10 mos): 12,000. Total = 27,000
      results.push({ test: 'Slider to 15k', updatedTotal15k, updatedRent15k, updatedCta15k, pass: updatedTotal15k === '₹27,000' && updatedCta15k.includes('maxPrice=15000') });

      // C. Preset Rent Chip to 6,000
      window.setRentPreset(6000);
      const chipTotal6k = document.getElementById('calcAccTotalSavings').textContent.trim();
      // Brokerage: 6,000. Utilities (10 mos): 12,000. Total = 18,000
      results.push({ test: 'Preset Chip to 6k', chipTotal6k, pass: chipTotal6k === '₹18,000' });

      // D. Duration Preset to 1 Semester (6 months)
      window.setDurationPreset(6);
      const durTotal6m = document.getElementById('calcAccTotalSavings').textContent.trim();
      // Brokerage: 6,000. Utilities (6 mos): 1,200 * 6 = 7,200. Total = 13,200
      results.push({ test: 'Duration to 6 months', durTotal6m, pass: durTotal6m === '₹13,200' });

      // E. Uncheck Utilities
      const utilCheck = document.getElementById('calcIncludeUtilities');
      utilCheck.checked = false;
      window.updateAccommodationCalc();
      const noUtilTotal = document.getElementById('calcAccTotalSavings').textContent.trim();
      // Brokerage: 6,000. Utilities: 0. Total = 6,000
      results.push({ test: 'Uncheck Utilities', noUtilTotal, pass: noUtilTotal === '₹6,000' });

      // F. Switch to Gear Mode
      window.switchCalcMode('gear');
      const gearPaneVisible = window.getComputedStyle(document.getElementById('calcPaneGear')).display !== 'none';
      const accPaneHidden = window.getComputedStyle(document.getElementById('calcPaneAccommodation')).display === 'none';
      const initialGearPkgRetail = document.getElementById('calcGearRetail').textContent.trim();
      const initialGearPkgSenior = document.getElementById('calcGearSenior').textContent.trim();
      const initialGearSavings = document.getElementById('calcGearSavings').textContent.trim();
      results.push({ test: 'Switch to Gear Mode', gearPaneVisible, accPaneHidden, initialGearPkgRetail, initialGearPkgSenior, initialGearSavings, pass: gearPaneVisible && accPaneHidden });

      // G. Select Laptop Gear Package
      window.selectGearPackage('laptop');
      const laptopRetail = document.getElementById('calcGearRetail').textContent.trim();
      const laptopSenior = document.getElementById('calcGearSenior').textContent.trim();
      const laptopSavings = document.getElementById('calcGearSavings').textContent.trim();
      const laptopCo2 = document.getElementById('calcGearCo2').textContent.trim();
      // Laptop: retail 56,000, senior 24,500, saved 31,500, co2 185
      results.push({ test: 'Select Laptop Package', laptopRetail, laptopSenior, laptopSavings, laptopCo2, pass: laptopRetail === '₹56,000' && laptopSenior === '₹24,500' && laptopSavings === '₹31,500' });

      // H. Select Mobility Package
      window.selectGearPackage('mobility');
      const cycleRetail = document.getElementById('calcGearRetail').textContent.trim();
      const cycleSenior = document.getElementById('calcGearSenior').textContent.trim();
      const cycleSavings = document.getElementById('calcGearSavings').textContent.trim();
      // Mobility: retail 12,000, senior 4,200, saved 7,800
      results.push({ test: 'Select Mobility Package', cycleRetail, cycleSenior, cycleSavings, pass: cycleRetail === '₹12,000' && cycleSenior === '₹4,200' && cycleSavings === '₹7,800' });

      // I. Custom Checklist Test
      const checks = document.querySelectorAll('#gearChecklist input[type="checkbox"]');
      checks[0].checked = true; // 6500 / 1800 / 12
      checks[1].checked = false;
      checks[2].checked = true; // 5500 / 2200 / 30
      checks[3].checked = false;
      window.updateCustomGearCalc();
      // Retail: 6500 + 5500 = 12,000. Senior: 1800 + 2200 = 4,000. Saved = 8,000. Co2 = 42
      const customRetail = document.getElementById('calcGearRetail').textContent.trim();
      const customSenior = document.getElementById('calcGearSenior').textContent.trim();
      const customSavings = document.getElementById('calcGearSavings').textContent.trim();
      const customCo2 = document.getElementById('calcGearCo2').textContent.trim();
      results.push({ test: 'Custom Checklist', customRetail, customSenior, customSavings, customCo2, pass: customRetail === '₹12,000' && customSenior === '₹4,000' && customSavings === '₹8,000' && customCo2 === '42 kg' });

      return results;
    });

    let allCalcPassed = true;
    calcChecks.forEach(cc => {
      console.log(`  ${cc.test} -> ${cc.pass ? 'PASS' : 'FAIL'}`, cc);
      report.feature9Calculator.checks.push(cc);
      if (!cc.pass) allCalcPassed = false;
    });
    report.feature9Calculator.status = allCalcPassed ? 'PASS' : 'FAIL';
    console.log(`Feature 9 Verdict: ${report.feature9Calculator.status}`);

    // -------------------------------------------------------------------------
    // TEST 3: Feature 12 - Public Creative Visual Charts & Fallback
    // -------------------------------------------------------------------------
    console.log('\n--- 3. Testing Feature 12: Creative Visual Charts & Dual-Engine Fallback ---');

    // Test A: Normal online execution (Chart.js or SVG fallback)
    const chartRenderStatus = await page.evaluate(() => {
      const rentContainer = document.getElementById('accChartContainer');
      const gearContainer = document.getElementById('gearChartContainer');
      const hasRentCanvas = !!rentContainer.querySelector('canvas');
      const hasRentSvg = !!rentContainer.querySelector('svg');
      const hasGearCanvas = !!gearContainer.querySelector('canvas');
      const hasGearSvg = !!gearContainer.querySelector('svg');
      return { hasRentCanvas, hasRentSvg, hasGearCanvas, hasGearSvg };
    });
    console.log('  Live Chart Render Status:', chartRenderStatus);

    // Test B: Filter interaction
    const filterResults = await page.evaluate(() => {
      window.filterRentChart('pg');
      const pgActive = document.querySelector('#accChartFilter .chart-pill.active').textContent.trim();
      window.filterRentChart('all');
      const allActive = document.querySelector('#accChartFilter .chart-pill.active').textContent.trim();
      window.toggleRecommerceView('volume');
      const volActive = document.querySelector('#gearChartFilter .chart-pill.active').textContent.trim();
      window.toggleRecommerceView('price');
      const priceActive = document.querySelector('#gearChartFilter .chart-pill.active').textContent.trim();
      return { pgActive, allActive, volActive, priceActive };
    });
    console.log('  Filter & Mode Switching Results:', filterResults);

    // Test C: Strict Offline / Blocked CDN Simulation (Adversarial Fallback Test)
    console.log('  Running Strict Zero-CDN Offline Fallback Simulation...');
    const offlineContext = await browser.newContext({ offline: true });
    const offlinePage = await offlineContext.newPage();
    // In offline mode, file:// local files still load, but external CDNs (jsdelivr) will fail!
    await offlinePage.goto('file:///' + path.join(FRONTEND_DIR, 'index.html').replace(/\\/g, '/'), { waitUntil: 'domcontentloaded' });
    await new Promise(r => setTimeout(r, 500));

    const fallbackCheck = await offlinePage.evaluate(() => {
      const rentContainer = document.getElementById('accChartContainer');
      const gearContainer = document.getElementById('gearChartContainer');
      const rentSvg = rentContainer ? rentContainer.querySelector('svg') : null;
      const gearSvg = gearContainer ? gearContainer.querySelector('svg') : null;

      let rentRects = 0;
      let rentTexts = 0;
      if (rentSvg) {
        rentRects = rentSvg.querySelectorAll('rect').length;
        rentTexts = rentSvg.querySelectorAll('text').length;
      }

      let gearRects = 0;
      let gearTexts = 0;
      if (gearSvg) {
        gearRects = gearSvg.querySelectorAll('rect').length;
        gearTexts = gearSvg.querySelectorAll('text').length;
      }

      // Test filtering on offline SVG charts
      window.filterRentChart('pg');
      const svgFilteredRects = rentSvg ? rentSvg.querySelectorAll('rect').length : 0;
      window.filterRentChart('all');

      window.toggleRecommerceView('volume');
      const svgVolRects = gearSvg ? gearSvg.querySelectorAll('rect').length : 0;

      return {
        hasRentSvg: !!rentSvg,
        hasGearSvg: !!gearSvg,
        rentRects,
        rentTexts,
        gearRects,
        gearTexts,
        svgFilteredRects,
        svgVolRects
      };
    });

    console.log('  Fallback Offline Verification:', fallbackCheck);
    const fallbackPassed = fallbackCheck.hasRentSvg && fallbackCheck.hasGearSvg && fallbackCheck.rentRects > 0 && fallbackCheck.gearRects > 0;
    report.feature12Charts.checks.push({
      test: 'Offline CDN Blocked SVG Fallback',
      fallbackCheck,
      pass: fallbackPassed
    });
    report.feature12Charts.status = fallbackPassed ? 'PASS' : 'FAIL';
    console.log(`Feature 12 Verdict: ${report.feature12Charts.status}`);
    await offlineContext.close();

    // -------------------------------------------------------------------------
    // TEST 4: Viewport Conformance across 320px, 375px, 768px, 1280px
    // -------------------------------------------------------------------------
    console.log('\n--- 4. Testing Responsive Viewport Conformance ---');
    const viewports = [320, 375, 768, 1280];
    let allVpPassed = true;

    for (const width of viewports) {
      const vpContext = await browser.newContext({ viewport: { width, height: 800 } });
      const vpPage = await vpContext.newPage();
      await vpPage.goto('file:///' + path.join(FRONTEND_DIR, 'index.html').replace(/\\/g, '/'), { waitUntil: 'load' });
      await new Promise(r => setTimeout(r, 400));

      const vpMetrics = await vpPage.evaluate((w) => {
        const docEl = document.documentElement;
        const body = document.body;
        const ribbon = document.querySelector('.metrics-ribbon-section');
        const calc = document.querySelector('.savings-calc-section');
        const charts = document.querySelector('.campus-charts-section');

        return {
          viewport: w,
          docScrollWidth: docEl.scrollWidth,
          docClientWidth: docEl.clientWidth,
          bodyScrollWidth: body ? body.scrollWidth : 0,
          bodyClientWidth: body ? body.clientWidth : 0,
          ribbonScrollWidth: ribbon ? ribbon.scrollWidth : 0,
          ribbonClientWidth: ribbon ? ribbon.clientWidth : 0,
          calcScrollWidth: calc ? calc.scrollWidth : 0,
          calcClientWidth: calc ? calc.clientWidth : 0,
          chartsScrollWidth: charts ? charts.scrollWidth : 0,
          chartsClientWidth: charts ? charts.clientWidth : 0,
          hasOverflow: docEl.scrollWidth > w || (body && body.scrollWidth > w)
        };
      }, width);

      console.log(`  Viewport ${width}px -> ${vpMetrics.hasOverflow ? 'OVERFLOW FAIL' : 'PASS'} (Doc: ${vpMetrics.docScrollWidth}px / Body: ${vpMetrics.bodyScrollWidth}px)`);
      report.responsiveBreakpoints.checks.push(vpMetrics);
      if (vpMetrics.hasOverflow) allVpPassed = false;
      await vpContext.close();
    }
    report.responsiveBreakpoints.status = allVpPassed ? 'PASS' : 'FAIL';
    console.log(`Responsive Conformance Verdict: ${report.responsiveBreakpoints.status}`);

    // -------------------------------------------------------------------------
    // TEST 5: Integrity Audit
    // -------------------------------------------------------------------------
    console.log('\n--- 5. Rigorous Integrity Audit ---');
    const integrityFindings = [];

    // Check for dummy or bypass implementations
    const statsCode = fs.readFileSync(path.join(FRONTEND_DIR, 'js', 'stats.js'), 'utf8');
    const chartsCode = fs.readFileSync(path.join(FRONTEND_DIR, 'js', 'charts.js'), 'utf8');

    // 1. Check if stats.js has real calculations or hardcoded mock returns
    const hasEaseOut = statsCode.includes('easeOutExpo') && statsCode.includes('Math.pow(2, -10 * t)');
    const hasRealRentCalc = statsCode.includes('brokerageSaved') && statsCode.includes('utilitySavings');
    const hasStayMartStats = statsCode.includes('StayMartAccommodationStats') && statsCode.includes('matchCampusZone');
    const hasRecommerceStats = statsCode.includes('RecommerceVisuals') && statsCode.includes('RECOMMERCE_CATEGORY_MEDIANS');

    if (!hasEaseOut) integrityFindings.push('Feature 8 missing real easing formula');
    if (!hasRealRentCalc) integrityFindings.push('Feature 9 missing financial calculation formulas');
    if (!hasStayMartStats) integrityFindings.push('Feature 10/11 missing StayMartAccommodationStats engine');
    if (!hasRecommerceStats) integrityFindings.push('Feature 11/13 missing RecommerceVisuals engine');

    // 2. Check if charts.js has real SVG math or fake placeholders
    const hasSvgMath = chartsCode.includes('viewBox') && chartsCode.includes('hPg') && chartsCode.includes('recommerceMode');
    if (!hasSvgMath) integrityFindings.push('Feature 12 missing genuine SVG coordinate calculations');

    // 3. Scan for "test-only" shortcut bypasses
    if (statsCode.includes('__test_mock__') || chartsCode.includes('__test_mock__')) {
      integrityFindings.push('Found fake test-only bypass hooks');
    }

    report.integrityAudit.findings = integrityFindings;
    report.integrityAudit.status = integrityFindings.length === 0 ? 'PASS' : 'INTEGRITY_VIOLATION';
    console.log(`Integrity Audit Verdict: ${report.integrityAudit.status}`, integrityFindings);

  } finally {
    await browser.close();
  }

  // Save report
  fs.writeFileSync(
    path.join(__dirname, 'reviewer_verification_results.json'),
    JSON.stringify(report, null, 2)
  );

  console.log('\n===============================================================');
  console.log('INDEPENDENT VERIFICATION RUN COMPLETE');
  console.log('===============================================================');
}

runReviewerVerification().catch(err => {
  console.error('Reviewer verification error:', err);
  process.exit(1);
});
