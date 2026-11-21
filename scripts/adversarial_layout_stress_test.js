/**
 * Milestone 2 Challenger Adversarial Layout & Responsiveness Stress Test Harness
 * Evaluates 8 Viewports: 320px, 360px, 375px, 414px, 768px, 1024px, 1280px, 1920px.
 * Deeply validates:
 *  1. Zero horizontal overflow across all pages and viewports (docScrollWidth <= vpWidth, bodyScrollWidth <= vpWidth).
 *  2. DOM bounding rects & wrapping of Milestone 2 components:
 *     - .metrics-ribbon-section
 *     - .savings-calc-section (sliders, chips, mode switcher, dynamic calculation states)
 *     - .campus-charts-section (SVG / canvas scaling, responsive filters)
 *     - Search & listing card badges (.brokerage-badge, .card-occupancy-meter, .card-condition-meter)
 *     - Detail page visualizers & widgets (#propertyOccupancyWidget, #campusRentVisualizer, #productPriceMeter, etc.)
 */

const fs = require('fs');
const path = require('path');
const { chromium } = require('C:/Users/divya/AppData/Local/Programs/Python/Python312/Lib/site-packages/playwright/driver/package');

const BASE_DIR = path.resolve(__dirname, '..');
const FRONTEND_DIR = path.join(BASE_DIR, 'frontend');

const TARGET_PAGES = [
  'index.html',
  'search-properties.html',
  'search-products.html',
  'property-detail.html',
  'product-detail.html'
];

const ADVERSARIAL_VIEWPORTS = [
  { name: 'Adversarial Narrow (iPhone SE 1st gen / tiny Android)', width: 320, height: 568 },
  { name: 'Android Standard Narrow (Samsung Galaxy S / A-series)', width: 360, height: 640 },
  { name: 'Mobile Standard (iPhone SE 2/3 / iPhone 12/13 mini)', width: 375, height: 667 },
  { name: 'Mobile Large (iPhone 11/12/13/14 Pro Max / Pixel XL)', width: 414, height: 896 },
  { name: 'Tablet Portrait (iPad 9.7 / 10.2)', width: 768, height: 1024 },
  { name: 'Tablet Landscape / Small Laptop (iPad Pro / Netbook)', width: 1024, height: 768 },
  { name: 'Desktop Standard (HD 13-15" Laptop)', width: 1280, height: 800 },
  { name: 'Desktop Widescreen (Full HD 1080p Monitor)', width: 1920, height: 1080 }
];

const report = {
  timestamp: new Date().toISOString(),
  testRunId: 'm2-challenger-1-stress',
  summary: {
    totalViewportChecks: 0,
    passedViewportChecks: 0,
    failedViewportChecks: 0,
    componentChecks: {
      metricsRibbon: { total: 0, passed: 0, failed: 0 },
      savingsCalc: { total: 0, passed: 0, failed: 0 },
      campusCharts: { total: 0, passed: 0, failed: 0 },
      cardBadges: { total: 0, passed: 0, failed: 0 },
      detailWidgets: { total: 0, passed: 0, failed: 0 }
    },
    interactiveStressChecks: { total: 0, passed: 0, failed: 0 }
  },
  failures: [],
  viewportDetails: [],
  interactiveDetails: []
};

function recordFailure(category, details) {
  report.failures.push({ category, details });
  console.error(`  [FAILURE] [${category}]: ${JSON.stringify(details)}`);
}

(async () => {
  console.log('======================================================================');
  console.log('STAYMART MILESTONE 2: EMPIRICAL ADVERSARIAL LAYOUT STRESS TEST HARNESS');
  console.log('======================================================================');
  console.log(`Testing 8 Viewports across ${TARGET_PAGES.length} Core Pages`);
  console.log('Viewports: 320px, 360px, 375px, 414px, 768px, 1024px, 1280px, 1920px\n');

  const browser = await chromium.launch({ channel: 'chrome', headless: true });

  // =========================================================================
  // SUITE 1: ADVERSARIAL VIEWPORT HORIZONTAL OVERFLOW & WRAPPING MATRIX
  // =========================================================================
  console.log('----------------------------------------------------------------------');
  console.log('SUITE 1: VIEWPORT HORIZONTAL OVERFLOW & PAGE INTEGRITY MATRIX');
  console.log('----------------------------------------------------------------------');

  for (const pageName of TARGET_PAGES) {
    const pageUrl = 'file:///' + path.join(FRONTEND_DIR, pageName).replace(/\\/g, '/');
    console.log(`\nPage: ${pageName}`);

    for (const vp of ADVERSARIAL_VIEWPORTS) {
      report.summary.totalViewportChecks++;
      const context = await browser.newContext({
        viewport: { width: vp.width, height: vp.height },
        deviceScaleFactor: 1
      });
      const page = await context.newPage();

      try {
        await page.goto(pageUrl, { waitUntil: 'domcontentloaded' });
        await new Promise(r => setTimeout(r, 250)); // allow charts/counters to mount

        const evaluation = await page.evaluate((viewportWidth) => {
          const docEl = document.documentElement;
          const body = document.body;

          const docScrollWidth = docEl.scrollWidth;
          const docClientWidth = docEl.clientWidth;
          const bodyScrollWidth = body ? body.scrollWidth : 0;
          const bodyClientWidth = body ? body.clientWidth : 0;

          // Check if root or body causes horizontal scrollbar
          const docOverflow = docScrollWidth > viewportWidth;
          const bodyOverflow = bodyScrollWidth > viewportWidth;
          const clientMismatch = docScrollWidth > docClientWidth || (body && bodyScrollWidth > bodyClientWidth);

          // Find offending elements in normal document flow that exceed viewport bounds and are NOT clipped
          const overflowingElements = [];
          const allEls = document.querySelectorAll('*');
          for (const el of allEls) {
            const tag = el.tagName.toLowerCase();
            if (['script', 'style', 'head', 'meta', 'link', 'svg', 'path', 'defs', 'clippath'].includes(tag)) continue;

            const cs = window.getComputedStyle(el);
            if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) === 0) continue;

            // Ignore elements inside intentional horizontal scrollers or off-canvas sheets/drawers
            const isScrollContainer = cs.overflowX === 'auto' || cs.overflowX === 'scroll';
            const insideScrollable = el.closest('.h-scroll, .category-strip, .category-strip-inner, .search-filters-scroll');
            const insideOffCanvas = el.closest('.mobile-drawer, .filter-sidebar, .booking-sheet-overlay, .order-sheet-overlay, .post-chooser-overlay, .modal-overlay');

            if (isScrollContainer || insideScrollable || insideOffCanvas) continue;

            const rect = el.getBoundingClientRect();
            // Check unclipped right bleed in normal document flow
            if (rect.right > viewportWidth + 2 && rect.width > 0 && cs.position !== 'fixed' && cs.position !== 'absolute') {
              overflowingElements.push({
                tag,
                id: el.id,
                className: el.className,
                rectRight: Math.round(rect.right),
                rectWidth: Math.round(rect.width),
                scrollWidth: el.scrollWidth,
                clientWidth: el.clientWidth,
                reason: 'Right boundary bleed beyond viewport in normal flow'
              });
            }

            // Check non-scroll container with unclipped internal scrollWidth
            if (el.scrollWidth > el.clientWidth + 2 && el.clientWidth > 0 && rect.width > 0 && cs.overflowX === 'visible') {
              if (!['text', 'tspan', 'canvas', 'svg', 'select'].includes(tag)) {
                overflowingElements.push({
                  tag,
                  id: el.id,
                  className: el.className,
                  scrollWidth: el.scrollWidth,
                  clientWidth: el.clientWidth,
                  delta: el.scrollWidth - el.clientWidth,
                  reason: 'Visible overflow with scrollWidth > clientWidth'
                });
              }
            }
          }

          return {
            docScrollWidth,
            docClientWidth,
            bodyScrollWidth,
            bodyClientWidth,
            docOverflow,
            bodyOverflow,
            clientMismatch,
            hasAnyOverflow: docOverflow || bodyOverflow || clientMismatch,
            overflowingElementsCount: overflowingElements.length,
            overflowingElements: overflowingElements.slice(0, 5)
          };
        }, vp.width);

        const passed = !evaluation.hasAnyOverflow && evaluation.overflowingElementsCount === 0;

        if (passed) {
          report.summary.passedViewportChecks++;
          console.log(`  [PASS] ${vp.name.padEnd(52)} | doc: ${evaluation.docScrollWidth}px/${evaluation.docClientWidth}px | body: ${evaluation.bodyScrollWidth}px/${evaluation.bodyClientWidth}px`);
        } else {
          report.summary.failedViewportChecks++;
          console.error(`  [FAIL] ${vp.name.padEnd(52)} | doc: ${evaluation.docScrollWidth}px/${evaluation.docClientWidth}px | body: ${evaluation.bodyScrollWidth}px/${evaluation.bodyClientWidth}px`);
          recordFailure('HorizontalOverflow', {
            page: pageName,
            viewport: vp.name,
            width: vp.width,
            evaluation
          });
        }

        report.viewportDetails.push({
          page: pageName,
          viewport: vp.name,
          width: vp.width,
          height: vp.height,
          passed,
          evaluation
        });

      } catch (err) {
        report.summary.failedViewportChecks++;
        recordFailure('PageLoadError', { page: pageName, viewport: vp.name, error: err.message });
      } finally {
        await context.close();
      }
    }
  }

  // =========================================================================
  // SUITE 2: DEEP DOM LAYOUT INSPECTION OF MILESTONE 2 COMPONENTS ON INDEX.HTML
  // =========================================================================
  console.log('\n----------------------------------------------------------------------');
  console.log('SUITE 2: DEEP DOM COMPONENT BOUNDING BOX & RESPONSIVENESS (INDEX.HTML)');
  console.log('----------------------------------------------------------------------');

  const componentViewports = [
    { name: '320px Narrow', width: 320, height: 568 },
    { name: '360px Android', width: 360, height: 640 },
    { name: '375px Standard', width: 375, height: 667 },
    { name: '414px Large', width: 414, height: 896 },
    { name: '768px Tablet', width: 768, height: 1024 },
    { name: '1024px Netbook', width: 1024, height: 768 },
    { name: '1280px Desktop', width: 1280, height: 800 },
    { name: '1920px Wide', width: 1920, height: 1080 }
  ];

  for (const cvp of componentViewports) {
    const context = await browser.newContext({ viewport: { width: cvp.width, height: cvp.height } });
    const page = await context.newPage();
    const indexUrl = 'file:///' + path.join(FRONTEND_DIR, 'index.html').replace(/\\/g, '/');
    await page.goto(indexUrl, { waitUntil: 'domcontentloaded' });
    await new Promise(r => setTimeout(r, 350));

    // A. Metrics Ribbon Section
    report.summary.componentChecks.metricsRibbon.total++;
    const metricsResult = await page.evaluate((vpWidth) => {
      const section = document.querySelector('.metrics-ribbon-section');
      const card = document.querySelector('.metrics-ribbon-card');
      const grid = document.querySelector('.metrics-grid');
      const items = Array.from(document.querySelectorAll('.metric-item'));

      if (!section || !card || !grid || items.length === 0) {
        return { exists: false, error: 'Metrics ribbon elements missing' };
      }

      const secRect = section.getBoundingClientRect();
      const cardRect = card.getBoundingClientRect();

      const itemsValid = items.every(item => {
        const r = item.getBoundingClientRect();
        return r.width > 0 && r.height > 0 && r.right <= vpWidth + 2;
      });

      const csGrid = window.getComputedStyle(grid);
      const cols = csGrid.gridTemplateColumns.split(' ').length;

      return {
        exists: true,
        secWidth: Math.round(secRect.width),
        cardWidth: Math.round(cardRect.width),
        cardRight: Math.round(cardRect.right),
        columnsCount: cols,
        itemCount: items.length,
        itemsValid,
        fitsViewport: cardRect.right <= vpWidth + 1 && cardRect.width <= vpWidth
      };
    }, cvp.width);

    if (metricsResult.exists && metricsResult.fitsViewport && metricsResult.itemsValid) {
      report.summary.componentChecks.metricsRibbon.passed++;
      console.log(`  [PASS] [.metrics-ribbon-section] @ ${cvp.name}: ${metricsResult.columnsCount} cols, cardWidth=${metricsResult.cardWidth}px (fits <= ${cvp.width}px)`);
    } else {
      report.summary.componentChecks.metricsRibbon.failed++;
      recordFailure('MetricsRibbonDefect', { viewport: cvp.name, metricsResult });
    }

    // B. Savings Calculator Section
    report.summary.componentChecks.savingsCalc.total++;
    const calcResult = await page.evaluate((vpWidth) => {
      const sec = document.querySelector('.savings-calc-section');
      const card = document.querySelector('.calc-card');
      const slider = document.getElementById('calcRentSlider');
      const chips = Array.from(document.querySelectorAll('.calc-chip'));
      const resultBox = document.querySelector('.calc-result-box');
      const totalAmount = document.getElementById('calcAccTotalSavings');

      if (!sec || !card || !slider || !resultBox || !totalAmount) {
        return { exists: false, error: 'Calculator components missing' };
      }

      const cardRect = card.getBoundingClientRect();
      const sliderRect = slider.getBoundingClientRect();
      const resRect = resultBox.getBoundingClientRect();
      const amountRect = totalAmount.getBoundingClientRect();

      const chipsWithinBounds = chips.every(c => {
        const cr = c.getBoundingClientRect();
        return cr.right <= vpWidth + 2;
      });

      return {
        exists: true,
        cardWidth: Math.round(cardRect.width),
        cardFits: cardRect.right <= vpWidth + 1,
        sliderWidth: Math.round(sliderRect.width),
        sliderFits: sliderRect.right <= vpWidth + 1,
        chipsWithinBounds,
        totalAmountText: totalAmount.innerText.trim(),
        totalAmountFits: amountRect.right <= vpWidth + 1,
        resBoxFits: resRect.right <= vpWidth + 1
      };
    }, cvp.width);

    if (calcResult.exists && calcResult.cardFits && calcResult.sliderFits && calcResult.chipsWithinBounds && calcResult.totalAmountFits) {
      report.summary.componentChecks.savingsCalc.passed++;
      console.log(`  [PASS] [.savings-calc-section] @ ${cvp.name}: slider=${calcResult.sliderWidth}px, amount='${calcResult.totalAmountText}', within bounds`);
    } else {
      report.summary.componentChecks.savingsCalc.failed++;
      recordFailure('SavingsCalcDefect', { viewport: cvp.name, calcResult });
    }

    // C. Campus Charts Section (SVG / Canvas scaling)
    report.summary.componentChecks.campusCharts.total++;
    const chartResult = await page.evaluate((vpWidth) => {
      const sec = document.querySelector('.campus-charts-section');
      const grid = document.querySelector('.charts-grid');
      const rentContainer = document.getElementById('accChartContainer');
      const gearContainer = document.getElementById('gearChartContainer');
      const svgElements = Array.from(sec.querySelectorAll('svg'));

      if (!sec || !grid || !rentContainer || !gearContainer) {
        return { exists: false, error: 'Charts section components missing' };
      }

      const gridRect = grid.getBoundingClientRect();
      const rentRect = rentContainer.getBoundingClientRect();
      const gearRect = gearContainer.getBoundingClientRect();

      const gridFits = gridRect.right <= vpWidth + 1;
      const rentFits = rentRect.right <= vpWidth + 1;
      const gearFits = gearRect.right <= vpWidth + 1;

      let svgsValid = true;
      for (const svg of svgElements) {
        const sr = svg.getBoundingClientRect();
        if (sr.right > vpWidth + 2) svgsValid = false;
      }

      const csGrid = window.getComputedStyle(grid);
      const cols = csGrid.gridTemplateColumns.split(' ').length;

      return {
        exists: true,
        cols,
        gridFits,
        rentContainerWidth: Math.round(rentRect.width),
        rentFits,
        gearContainerWidth: Math.round(gearRect.width),
        gearFits,
        svgsCount: svgElements.length,
        svgsValid
      };
    }, cvp.width);

    if (chartResult.exists && chartResult.gridFits && chartResult.rentFits && chartResult.gearFits && chartResult.svgsValid) {
      report.summary.componentChecks.campusCharts.passed++;
      console.log(`  [PASS] [.campus-charts-section] @ ${cvp.name}: ${chartResult.cols} col(s), rentWrap=${chartResult.rentContainerWidth}px, gearWrap=${chartResult.gearContainerWidth}px, svg/canvas valid`);
    } else {
      report.summary.componentChecks.campusCharts.failed++;
      recordFailure('CampusChartsDefect', { viewport: cvp.name, chartResult });
    }

    await context.close();
  }

  // =========================================================================
  // SUITE 3: INTERACTIVE STRESS TESTING (SLIDERS, CHIPS, MODE SWITCHES, CHARTS)
  // =========================================================================
  console.log('\n----------------------------------------------------------------------');
  console.log('SUITE 3: INTERACTIVE CALCULATOR & CHART FILTER STRESS TESTING');
  console.log('----------------------------------------------------------------------');

  const interactiveViewports = [
    { name: 'Adversarial 320px', width: 320, height: 568 },
    { name: 'Standard 375px', width: 375, height: 667 }
  ];

  for (const ivp of interactiveViewports) {
    const context = await browser.newContext({ viewport: { width: ivp.width, height: ivp.height } });
    const page = await context.newPage();
    const indexUrl = 'file:///' + path.join(FRONTEND_DIR, 'index.html').replace(/\\/g, '/');
    await page.goto(indexUrl, { waitUntil: 'domcontentloaded' });
    await new Promise(r => setTimeout(r, 200));

    console.log(`\nInteractive Tests @ Viewport: ${ivp.name} (${ivp.width}x${ivp.height})`);

    // Step A: Rent slider dynamic bounds & calculation test
    report.summary.interactiveStressChecks.total++;
    const sliderTest = await page.evaluate((vpWidth) => {
      const slider = document.getElementById('calcRentSlider');
      const display = document.getElementById('calcRentDisplay');
      const totalAmount = document.getElementById('calcAccTotalSavings');

      // Test Min: ₹5,000
      slider.value = 5000;
      slider.dispatchEvent(new Event('input', { bubbles: true }));
      const minDisplay = display.innerText;
      const minTotal = totalAmount.innerText;
      const docW1 = document.documentElement.scrollWidth;

      // Test Max: ₹25,000
      slider.value = 25000;
      slider.dispatchEvent(new Event('input', { bubbles: true }));
      const maxDisplay = display.innerText;
      const maxTotal = totalAmount.innerText;
      const docW2 = document.documentElement.scrollWidth;

      // Test Mid: ₹14,500
      slider.value = 14500;
      slider.dispatchEvent(new Event('input', { bubbles: true }));
      const midDisplay = display.innerText;
      const midTotal = totalAmount.innerText;
      const docW3 = document.documentElement.scrollWidth;

      return {
        minDisplay,
        minTotal,
        maxDisplay,
        maxTotal,
        midDisplay,
        midTotal,
        noOverflow: docW1 <= vpWidth && docW2 <= vpWidth && docW3 <= vpWidth,
        docWidths: [docW1, docW2, docW3]
      };
    }, ivp.width);

    if (sliderTest.noOverflow && sliderTest.minTotal !== sliderTest.maxTotal) {
      report.summary.interactiveStressChecks.passed++;
      console.log(`  [PASS] Rent Slider Dynamic Stress: min(${sliderTest.minDisplay} -> ${sliderTest.minTotal}) max(${sliderTest.maxDisplay} -> ${sliderTest.maxTotal}) 0 overflow`);
    } else {
      report.summary.interactiveStressChecks.failed++;
      recordFailure('SliderStressDefect', { viewport: ivp.name, sliderTest });
    }

    // Step B: Preset Chips Interaction Stress
    report.summary.interactiveStressChecks.total++;
    const chipTest = await page.evaluate((vpWidth) => {
      const chips = Array.from(document.querySelectorAll('.calc-chip'));
      const results = [];
      for (const chip of chips) {
        chip.click();
        const display = document.getElementById('calcRentDisplay').innerText;
        const total = document.getElementById('calcAccTotalSavings').innerText;
        const scrollW = document.documentElement.scrollWidth;
        results.push({ text: chip.innerText, display, total, scrollW });
      }
      const allFit = results.every(r => r.scrollW <= vpWidth);
      return { results, allFit };
    }, ivp.width);

    if (chipTest.allFit) {
      report.summary.interactiveStressChecks.passed++;
      console.log(`  [PASS] Preset Chips Click Stress: ${chipTest.results.length} chips triggered, zero overflow`);
    } else {
      report.summary.interactiveStressChecks.failed++;
      recordFailure('ChipStressDefect', { viewport: ivp.name, chipTest });
    }

    // Step C: Mode Switching to Gear Re-Commerce and Back
    report.summary.interactiveStressChecks.total++;
    const modeSwitchTest = await page.evaluate((vpWidth) => {
      const gearBtn = document.getElementById('calcModeGearBtn');
      const accBtn = document.getElementById('calcModeAccBtn');
      const paneGear = document.getElementById('calcPaneGear');
      const paneAcc = document.getElementById('calcPaneAccommodation');

      // Switch to Gear
      gearBtn.click();
      const gearVisible = paneGear && window.getComputedStyle(paneGear).display !== 'none';
      const accHidden = paneAcc && window.getComputedStyle(paneAcc).display === 'none';
      const docWGear = document.documentElement.scrollWidth;

      // Click each package card in gear mode
      const pkgs = Array.from(document.querySelectorAll('.package-card'));
      for (const p of pkgs) {
        p.click();
      }
      const docWPkgs = document.documentElement.scrollWidth;

      // Switch back to Acc
      accBtn.click();
      const accRestored = paneAcc && window.getComputedStyle(paneAcc).display !== 'none';
      const docWRestored = document.documentElement.scrollWidth;

      return {
        gearVisible,
        accHidden,
        accRestored,
        noOverflow: docWGear <= vpWidth && docWPkgs <= vpWidth && docWRestored <= vpWidth,
        docWidths: { docWGear, docWPkgs, docWRestored }
      };
    }, ivp.width);

    if (modeSwitchTest.gearVisible && modeSwitchTest.accRestored && modeSwitchTest.noOverflow) {
      report.summary.interactiveStressChecks.passed++;
      console.log(`  [PASS] Mode Switcher (Acc <-> Gear Re-Commerce): clean transitions, 0 overflow`);
    } else {
      report.summary.interactiveStressChecks.failed++;
      recordFailure('ModeSwitchDefect', { viewport: ivp.name, modeSwitchTest });
    }

    // Step D: Public Chart Filter Pill Interactions
    report.summary.interactiveStressChecks.total++;
    const chartFilterTest = await page.evaluate(async (vpWidth) => {
      const rentPills = Array.from(document.querySelectorAll('#accChartFilter .chart-pill'));
      const gearPills = Array.from(document.querySelectorAll('#gearChartFilter .chart-pill'));

      for (const p of rentPills) {
        p.click();
      }

      for (const p of gearPills) {
        p.click();
      }

      const docW = document.documentElement.scrollWidth;
      const bodyW = document.body.scrollWidth;

      return {
        rentPillsTested: rentPills.length,
        gearPillsTested: gearPills.length,
        docW,
        bodyW,
        noOverflow: docW <= vpWidth && bodyW <= vpWidth
      };
    }, ivp.width);

    if (chartFilterTest.noOverflow) {
      report.summary.interactiveStressChecks.passed++;
      console.log(`  [PASS] Chart Filter Pills Interaction (${chartFilterTest.rentPillsTested + chartFilterTest.gearPillsTested} buttons clicked): 0 overflow`);
    } else {
      report.summary.interactiveStressChecks.failed++;
      recordFailure('ChartFilterDefect', { viewport: ivp.name, chartFilterTest });
    }

    await context.close();
  }

  // =========================================================================
  // SUITE 4: SEARCH PAGE CARD GRIDS & BADGE WRAPPING STRESS TEST
  // =========================================================================
  console.log('\n----------------------------------------------------------------------');
  console.log('SUITE 4: SEARCH CARD BADGE WRAPPING & GRID STRESS (PROPERTIES & PRODUCTS)');
  console.log('----------------------------------------------------------------------');

  const searchPages = ['search-properties.html', 'search-products.html'];
  const searchTestViewports = [
    { name: '320px Narrow', width: 320, height: 568 },
    { name: '375px Standard', width: 375, height: 667 },
    { name: '768px Tablet', width: 768, height: 1024 },
    { name: '1280px Desktop', width: 1280, height: 800 }
  ];

  for (const pageName of searchPages) {
    const pageUrl = 'file:///' + path.join(FRONTEND_DIR, pageName).replace(/\\/g, '/');

    for (const svp of searchTestViewports) {
      report.summary.componentChecks.cardBadges.total++;
      const context = await browser.newContext({ viewport: { width: svp.width, height: svp.height } });
      const page = await context.newPage();
      await page.goto(pageUrl, { waitUntil: 'domcontentloaded' });
      await new Promise(r => setTimeout(r, 300));

      const cardStress = await page.evaluate((opts) => {
        const { vpWidth } = opts;
        const cards = Array.from(document.querySelectorAll('.card'));
        const docW = document.documentElement.scrollWidth;

        let badgesWithinCard = true;
        let meterWithinCard = true;
        let cardFitsColumn = true;

        for (const c of cards) {
          const cr = c.getBoundingClientRect();
          if (cr.right > vpWidth + 2) cardFitsColumn = false;

          const badges = Array.from(c.querySelectorAll('.brokerage-badge, .zone-discount-pill, .card-savings-pill, .deal-chip'));
          for (const b of badges) {
            const br = b.getBoundingClientRect();
            if (br.right > cr.right + 2) badgesWithinCard = false;
          }

          const meters = Array.from(c.querySelectorAll('.card-occupancy-meter, .card-condition-meter'));
          for (const m of meters) {
            const mr = m.getBoundingClientRect();
            if (mr.right > cr.right + 2) meterWithinCard = false;
          }
        }

        return {
          cardCount: cards.length,
          docW,
          noDocOverflow: docW <= vpWidth,
          cardFitsColumn,
          badgesWithinCard,
          meterWithinCard
        };
      }, { vpWidth: svp.width, pageName });

      if (cardStress.noDocOverflow && cardStress.cardFitsColumn && cardStress.badgesWithinCard && cardStress.meterWithinCard) {
        report.summary.componentChecks.cardBadges.passed++;
        console.log(`  [PASS] [${pageName}] @ ${svp.name}: ${cardStress.cardCount} cards tested, all badges & meters within column bounds`);
      } else {
        report.summary.componentChecks.cardBadges.failed++;
        recordFailure('SearchCardBadgeDefect', { page: pageName, viewport: svp.name, cardStress });
      }

      await context.close();
    }
  }

  // =========================================================================
  // SUITE 5: DETAIL PAGE WIDGETS & VISUALIZERS STRESS TEST
  // =========================================================================
  console.log('\n----------------------------------------------------------------------');
  console.log('SUITE 5: DETAIL PAGES NEW VISUAL COMPONENTS & GAUGES STRESS TEST');
  console.log('----------------------------------------------------------------------');

  const detailViewports = [
    { name: '320px Narrow', width: 320, height: 568 },
    { name: '375px Standard', width: 375, height: 667 },
    { name: '768px Tablet', width: 768, height: 1024 },
    { name: '1280px Desktop', width: 1280, height: 800 }
  ];

  // A. property-detail.html widgets
  for (const dvp of detailViewports) {
    report.summary.componentChecks.detailWidgets.total++;
    const context = await browser.newContext({ viewport: { width: dvp.width, height: dvp.height } });
    const page = await context.newPage();
    const propUrl = 'file:///' + path.join(FRONTEND_DIR, 'property-detail.html').replace(/\\/g, '/');
    await page.goto(propUrl, { waitUntil: 'domcontentloaded' });
    await new Promise(r => setTimeout(r, 250));

    const propWidgetTest = await page.evaluate((vpWidth) => {
      const occWidget = document.getElementById('propertyOccupancyWidget');
      const rentVis = document.getElementById('campusRentVisualizer');
      const savCard = document.getElementById('propertySavingsCard');
      const ctaBar = document.getElementById('mobileDetailCtaBar');

      const docW = document.documentElement.scrollWidth;

      const occFits = occWidget ? occWidget.getBoundingClientRect().right <= vpWidth + 2 : true;
      const rentFits = rentVis ? rentVis.getBoundingClientRect().right <= vpWidth + 2 : true;
      const savFits = savCard ? savCard.getBoundingClientRect().right <= vpWidth + 2 : true;
      const ctaFits = ctaBar ? ctaBar.getBoundingClientRect().right <= vpWidth + 2 : true;

      return {
        docW,
        noDocOverflow: docW <= vpWidth,
        occFits,
        rentFits,
        savFits,
        ctaFits
      };
    }, dvp.width);

    if (propWidgetTest.noDocOverflow && propWidgetTest.occFits && propWidgetTest.rentFits && propWidgetTest.savFits && propWidgetTest.ctaFits) {
      report.summary.componentChecks.detailWidgets.passed++;
      console.log(`  [PASS] [property-detail.html] @ ${dvp.name}: Occupancy, Rent Gauge & Savings Card fit viewport <= ${dvp.width}px`);
    } else {
      report.summary.componentChecks.detailWidgets.failed++;
      recordFailure('PropertyDetailWidgetDefect', { viewport: dvp.name, propWidgetTest });
    }

    await context.close();
  }

  // B. product-detail.html widgets
  for (const dvp of detailViewports) {
    report.summary.componentChecks.detailWidgets.total++;
    const context = await browser.newContext({ viewport: { width: dvp.width, height: dvp.height } });
    const page = await context.newPage();
    const prodUrl = 'file:///' + path.join(FRONTEND_DIR, 'product-detail.html').replace(/\\/g, '/');
    await page.goto(prodUrl, { waitUntil: 'domcontentloaded' });
    await new Promise(r => setTimeout(r, 250));

    const prodWidgetTest = await page.evaluate((vpWidth) => {
      const proof = document.getElementById('productSocialProofRibbon');
      const savingsBox = document.getElementById('productSavingsBox');
      const priceMeter = document.getElementById('productPriceMeter');
      const condCard = document.getElementById('productConditionCard');
      const ctaBar = document.getElementById('mobileDetailCtaBar');

      const docW = document.documentElement.scrollWidth;

      const proofFits = proof ? proof.getBoundingClientRect().right <= vpWidth + 2 : true;
      const savFits = savingsBox ? savingsBox.getBoundingClientRect().right <= vpWidth + 2 : true;
      const meterFits = priceMeter ? priceMeter.getBoundingClientRect().right <= vpWidth + 2 : true;
      const condFits = condCard ? condCard.getBoundingClientRect().right <= vpWidth + 2 : true;
      const ctaFits = ctaBar ? ctaBar.getBoundingClientRect().right <= vpWidth + 2 : true;

      return {
        docW,
        noDocOverflow: docW <= vpWidth,
        proofFits,
        savFits,
        meterFits,
        condFits,
        ctaFits
      };
    }, dvp.width);

    if (prodWidgetTest.noDocOverflow && prodWidgetTest.proofFits && prodWidgetTest.savFits && prodWidgetTest.meterFits && prodWidgetTest.condFits && prodWidgetTest.ctaFits) {
      report.summary.componentChecks.detailWidgets.passed++;
      console.log(`  [PASS] [product-detail.html] @ ${dvp.name}: Social Proof, Savings Table, Price Meter & Condition Card fit <= ${dvp.width}px`);
    } else {
      report.summary.componentChecks.detailWidgets.failed++;
      recordFailure('ProductDetailWidgetDefect', { viewport: dvp.name, prodWidgetTest });
    }

    await context.close();
  }

  await browser.close();

  // =========================================================================
  // FINAL EVALUATION & SUMMARY
  // =========================================================================
  console.log('\n======================================================================');
  console.log('EMPIRICAL ADVERSARIAL STRESS TEST SUMMARY');
  console.log('======================================================================');
  console.log(`Total Viewport Matrix Checks:    ${report.summary.totalViewportChecks} | Passed: ${report.summary.passedViewportChecks} | Failed: ${report.summary.failedViewportChecks}`);
  console.log(`Metrics Ribbon Component Checks:  ${report.summary.componentChecks.metricsRibbon.total} | Passed: ${report.summary.componentChecks.metricsRibbon.passed} | Failed: ${report.summary.componentChecks.metricsRibbon.failed}`);
  console.log(`Savings Calculator Checks:        ${report.summary.componentChecks.savingsCalc.total} | Passed: ${report.summary.componentChecks.savingsCalc.passed} | Failed: ${report.summary.componentChecks.savingsCalc.failed}`);
  console.log(`Campus Visual Charts Checks:      ${report.summary.componentChecks.campusCharts.total} | Passed: ${report.summary.componentChecks.campusCharts.passed} | Failed: ${report.summary.componentChecks.campusCharts.failed}`);
  console.log(`Card Badges & Column Checks:      ${report.summary.componentChecks.cardBadges.total} | Passed: ${report.summary.componentChecks.cardBadges.passed} | Failed: ${report.summary.componentChecks.cardBadges.failed}`);
  console.log(`Detail Widgets & Gauges Checks:   ${report.summary.componentChecks.detailWidgets.total} | Passed: ${report.summary.componentChecks.detailWidgets.passed} | Failed: ${report.summary.componentChecks.detailWidgets.failed}`);
  console.log(`Interactive Stress Tests:         ${report.summary.interactiveStressChecks.total} | Passed: ${report.summary.interactiveStressChecks.passed} | Failed: ${report.summary.interactiveStressChecks.failed}`);
  console.log(`Total Defects / Failures Found:   ${report.failures.length}`);

  const verdict = (report.failures.length === 0 && report.summary.failedViewportChecks === 0) ? 'APPROVE' : 'REQUEST_CHANGES';
  report.verdict = verdict;

  console.log(`\nOVERALL ADVERSARIAL VERDICT: ${verdict}`);

  const outputPath = path.join(BASE_DIR, 'scripts', 'adversarial_stress_results.json');
  fs.writeFileSync(outputPath, JSON.stringify(report, null, 2));
  console.log(`Detailed test results written to: ${outputPath}`);

  process.exit(verdict === 'APPROVE' ? 0 : 1);
})();
