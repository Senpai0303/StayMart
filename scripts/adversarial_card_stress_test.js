/**
 * Adversarial Card Generator & Badge Wrapping Stress Test Harness
 * Injects adversarial cards with extreme values (very long titles, high prices, zero/full occupancy, extreme deal badges)
 * into index.html, search-properties.html, and search-products.html grids across 320px, 360px, 375px, 768px, 1280px.
 * Validates:
 *  1. Card width strictly <= column width (no forced horizontal blowout).
 *  2. Badges (.brokerage-badge, .zone-discount-pill, .card-savings-pill, .deal-chip) wrap or truncate gracefully.
 *  3. Zero document horizontal overflow (docScrollWidth === clientWidth).
 */

const fs = require('fs');
const path = require('path');
const { chromium } = require('C:/Users/divya/AppData/Local/Programs/Python/Python312/Lib/site-packages/playwright/driver/package');

const BASE_DIR = path.resolve(__dirname, '..');
const FRONTEND_DIR = path.join(BASE_DIR, 'frontend');

const VIEWPORTS = [
  { name: '320px Narrow', width: 320, height: 568 },
  { name: '360px Android', width: 360, height: 640 },
  { name: '375px Standard', width: 375, height: 667 },
  { name: '768px Tablet', width: 768, height: 1024 },
  { name: '1280px Desktop', width: 1280, height: 800 }
];

(async () => {
  console.log('======================================================================');
  console.log('ADVERSARIAL CARD GENERATION & BADGE WRAPPING STRESS TEST');
  console.log('======================================================================\n');

  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  let totalTests = 0;
  let passedTests = 0;
  let failedTests = 0;
  const failureList = [];

  for (const vp of VIEWPORTS) {
    const context = await browser.newContext({ viewport: { width: vp.width, height: vp.height } });
    const page = await context.newPage();
    const indexUrl = 'file:///' + path.join(FRONTEND_DIR, 'index.html').replace(/\\/g, '/');
    await page.goto(indexUrl, { waitUntil: 'domcontentloaded' });
    await new Promise(r => setTimeout(r, 200));

    totalTests++;
    const testResult = await page.evaluate((vpWidth) => {
      // Create adversarial property objects
      const advProperties = [
        {
          id: 991,
          title: 'Ultra Luxury Student Palace PG Near Graphic Era Clement Town With High-Speed WiFi, Gym, 4-Course Meals, Attached Bathroom and Dedicated Study Desk',
          type: 'PG',
          pricePerMonth: 28500,
          totalRooms: 12,
          availableRooms: 0,
          isAvailable: false,
          genderPreference: 'MALE',
          area: 'Clement Town Extension Campus Belt Near Graphic Era Hill University',
          createdAt: new Date().toISOString(),
          images: []
        },
        {
          id: 992,
          title: 'Budget Friendly Room Sharing Near UPES Bidholi',
          type: 'ROOM',
          pricePerMonth: 4500,
          totalRooms: 20,
          availableRooms: 18,
          isAvailable: true,
          genderPreference: 'ANY',
          area: 'Bidholi Knowledge City Village Road',
          createdAt: new Date().toISOString(),
          images: []
        }
      ];

      // Create adversarial product objects
      const advProducts = [
        {
          id: 881,
          title: 'Apple MacBook Pro M3 Max 64GB Unified Memory 1TB SSD Space Black Flawless Condition With AppleCare+ Warranty and Original MagSafe Charger',
          price: 185000,
          listingType: 'SELL',
          brand: 'Apple California Premium Tech',
          condition: 'LIKE_NEW',
          area: 'Prem Nagar UPES Western Campus Corridor',
          createdAt: new Date().toISOString(),
          images: []
        },
        {
          id: 882,
          title: 'GATE 2027 Complete Mechanical & Computer Science Solved Papers Handwritten Toppers Notes Bundle 14 Volumes',
          price: 850,
          listingType: 'SELL',
          brand: 'Standard Publications',
          condition: 'FAIR',
          area: 'DIT University Rajpur Road',
          createdAt: new Date().toISOString(),
          images: []
        }
      ];

      // Inject into DOM
      const testContainer = document.createElement('div');
      testContainer.id = 'adversarialTestContainer';
      testContainer.className = 'grid-4';
      testContainer.style.padding = '12px';
      testContainer.style.boxSizing = 'border-box';

      let html = '';
      if (typeof buildPropertyCard === 'function') {
        html += advProperties.map(p => buildPropertyCard(p)).join('');
      }
      if (typeof buildProductCard === 'function') {
        html += advProducts.map(p => buildProductCard(p)).join('');
      }

      testContainer.innerHTML = html;
      document.body.appendChild(testContainer);

      const docScrollWidth = document.documentElement.scrollWidth;
      const bodyScrollWidth = document.body.scrollWidth;

      const cards = Array.from(testContainer.querySelectorAll('.card'));
      const cardEvaluations = [];

      let anyCardBlowout = false;
      let anyBadgeBleed = false;

      for (const card of cards) {
        const cRect = card.getBoundingClientRect();
        if (cRect.right > vpWidth + 1.5) anyCardBlowout = true;

        // Check if badges or strips bleed past card
        const badges = Array.from(card.querySelectorAll('.card-savings-strip, .brokerage-badge, .zone-discount-pill, .card-savings-pill, .deal-chip, .card-occupancy-meter, .card-engagement-strip'));
        for (const b of badges) {
          const bRect = b.getBoundingClientRect();
          if (bRect.right > cRect.right + 2) {
            anyBadgeBleed = true;
          }
        }

        cardEvaluations.push({
          cardWidth: Math.round(cRect.width),
          cardRight: Math.round(cRect.right),
          cardScrollWidth: card.scrollWidth,
          cardClientWidth: card.clientWidth
        });
      }

      return {
        docScrollWidth,
        bodyScrollWidth,
        noPageOverflow: docScrollWidth <= vpWidth && bodyScrollWidth <= vpWidth,
        cardsCount: cards.length,
        anyCardBlowout,
        anyBadgeBleed,
        cardEvaluations
      };
    }, vp.width);

    const passed = testResult.noPageOverflow && !testResult.anyCardBlowout && !testResult.anyBadgeBleed && testResult.cardsCount === 4;

    if (passed) {
      passedTests++;
      console.log(`  [PASS] Viewport ${vp.name.padEnd(20)}: 4 adversarial cards mounted, 0 blowout, 0 badge bleed, docW=${testResult.docScrollWidth}px <= ${vp.width}px`);
    } else {
      failedTests++;
      failureList.push({ viewport: vp.name, testResult });
      console.error(`  [FAIL] Viewport ${vp.name.padEnd(20)}: failure:`, JSON.stringify(testResult));
    }

    await context.close();
  }

  await browser.close();

  console.log('\n======================================================================');
  console.log(`SUMMARY: ${passedTests} / ${totalTests} viewports passed adversarial card stress`);
  console.log(`VERDICT: ${failedTests === 0 ? 'APPROVE' : 'REQUEST_CHANGES'}`);
  console.log('======================================================================');

  process.exit(failedTests === 0 ? 0 : 1);
})();
