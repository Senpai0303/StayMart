/**
 * Adversarial Viewport & Layout Empirical Test Runner
 * Evaluates Mobile (375px), Tablet (768px), Desktop (1280px),
 * plus adversarial 320px, 414px, and 1920px viewports.
 * Uses headless Google Chrome via Playwright core driver.
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

const VIEWPORTS = [
  { name: 'Adversarial Narrow (iPhone SE 1st gen)', width: 320, height: 568 },
  { name: 'Mobile Standard (iPhone SE / 12 mini)', width: 375, height: 667 },
  { name: 'Mobile Large (iPhone Pro Max / Pixel)', width: 414, height: 896 },
  { name: 'Tablet Standard (iPad portrait)', width: 768, height: 1024 },
  { name: 'Desktop Standard (HD laptop)', width: 1280, height: 800 },
  { name: 'Desktop Widescreen (Full HD)', width: 1920, height: 1080 }
];

const results = {
  timestamp: new Date().toISOString(),
  staticChecks: {
    inlineGridStyles: [],
    cssTokens: { totalDefined: 0, missingInGlobal: [], missingInDashboard: [] },
    brokenRedirects: []
  },
  viewportChecks: [],
  mobileComponentVisibility: [],
  interactionChecks: [],
  defectsIdentified: []
};

// ---------------------------------------------------------------------------
// 1. Static Verification
// ---------------------------------------------------------------------------
console.log('===============================================================');
console.log('1. RUNNING STATIC VERIFICATIONS');
console.log('===============================================================');

// A. Check for inline grid-template-columns in all HTML files
function scanHtmlForInlineGrid(dir) {
  const files = fs.readdirSync(dir);
  for (const f of files) {
    const full = path.join(dir, f);
    if (fs.statSync(full).isDirectory()) {
      scanHtmlForInlineGrid(full);
    } else if (f.endsWith('.html')) {
      const content = fs.readFileSync(full, 'utf8');
      const matches = content.match(/style\s*=\s*["'][^"']*grid-template-columns[^"']*["']/gi);
      if (matches) {
        results.staticChecks.inlineGridStyles.push({ file: path.relative(BASE_DIR, full), matches });
      }
      if (content.includes('grid-template-columns:260px') || content.includes('grid-template-columns: 260px')) {
        results.staticChecks.inlineGridStyles.push({ file: path.relative(BASE_DIR, full), error: 'hardcoded 260px grid found' });
      }
    }
  }
}
scanHtmlForInlineGrid(FRONTEND_DIR);
console.log(`[PASS/FAIL] Inline grid-template-columns violations: ${results.staticChecks.inlineGridStyles.length}`);

// B. Check CSS token resolution
const globalCssPath = path.join(FRONTEND_DIR, 'css', 'global.css');
const dashCssPath = path.join(FRONTEND_DIR, 'css', 'dashboard.css');
const globalCss = fs.readFileSync(globalCssPath, 'utf8');
const dashCss = fs.readFileSync(dashCssPath, 'utf8');

const definedTokens = new Set();
const defRegex = /(--[a-zA-Z0-9-_]+)\s*:/g;
let m;
while ((m = defRegex.exec(globalCss)) !== null) definedTokens.add(m[1]);
const globalTokenCount = definedTokens.size;
while ((m = defRegex.exec(dashCss)) !== null) definedTokens.add(m[1]);
results.staticChecks.cssTokens.totalDefined = definedTokens.size;

function findMissingTokens(css, file) {
  const varRegex = /var\(\s*(--[a-zA-Z0-9-_]+)[^)]*\)/g;
  const missing = [];
  let match;
  while ((match = varRegex.exec(css)) !== null) {
    const token = match[1];
    if (!definedTokens.has(token)) {
      missing.push({ file, token });
    }
  }
  return missing;
}
results.staticChecks.cssTokens.missingInGlobal = findMissingTokens(globalCss, 'global.css');
results.staticChecks.cssTokens.missingInDashboard = findMissingTokens(dashCss, 'dashboard.css');
console.log(`[PASS/FAIL] Total unique CSS tokens defined: ${results.staticChecks.cssTokens.totalDefined}`);
console.log(`[PASS/FAIL] Undefined tokens in global.css: ${results.staticChecks.cssTokens.missingInGlobal.length}`);
console.log(`[PASS/FAIL] Undefined tokens in dashboard.css: ${results.staticChecks.cssTokens.missingInDashboard.length}`);

// C. Check for broken 404 redirects in all frontend JS and HTML
const badUrls = ['my-bookings.html', 'my-orders.html', 'messages.html'];
function scanForBadUrls(dir) {
  const files = fs.readdirSync(dir);
  for (const f of files) {
    const full = path.join(dir, f);
    if (fs.statSync(full).isDirectory()) {
      scanForBadUrls(full);
    } else if (f.endsWith('.js') || f.endsWith('.html')) {
      const content = fs.readFileSync(full, 'utf8');
      for (const bad of badUrls) {
        if (content.includes(bad)) {
          results.staticChecks.brokenRedirects.push({ file: path.relative(BASE_DIR, full), url: bad });
        }
      }
    }
  }
}
scanForBadUrls(FRONTEND_DIR);
console.log(`[PASS/FAIL] Broken 404 redirect references found: ${results.staticChecks.brokenRedirects.length}`);

// ---------------------------------------------------------------------------
// 2. Dynamic Headless Chrome Layout & Viewport Verification
// ---------------------------------------------------------------------------
console.log('\n===============================================================');
console.log('2. RUNNING DYNAMIC HEADLESS CHROME VIEWPORT TESTS');
console.log('===============================================================');

(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });

  for (const pageName of TARGET_PAGES) {
    const pageUrl = 'file:///' + path.join(FRONTEND_DIR, pageName).replace(/\\/g, '/');
    console.log(`\nTesting Page: ${pageName}`);

    for (const vp of VIEWPORTS) {
      const context = await browser.newContext({
        viewport: { width: vp.width, height: vp.height },
        deviceScaleFactor: 1
      });
      const page = await context.newPage();

      try {
        await page.goto(pageUrl, { waitUntil: 'domcontentloaded' });
        await new Promise(r => setTimeout(r, 250));

        const evaluation = await page.evaluate((vpWidth) => {
          const docEl = document.documentElement;
          const body = document.body;

          const docScrollWidth = docEl.scrollWidth;
          const docClientWidth = docEl.clientWidth;
          const bodyScrollWidth = body ? body.scrollWidth : 0;
          const bodyClientWidth = body ? body.clientWidth : 0;

          // Check for horizontal overflow
          const hasDocOverflow = docScrollWidth > docClientWidth;
          const hasBodyOverflow = bodyScrollWidth > bodyClientWidth;
          const overflowsViewport = docScrollWidth > vpWidth;

          // Scan DOM elements that have internal overflow
          const internalOverflowElements = [];
          const allElements = document.querySelectorAll('*');
          for (const el of allElements) {
            const tag = el.tagName.toLowerCase();
            if (['script', 'style', 'head', 'meta', 'link', 'path', 'defs'].includes(tag)) continue;

            const computed = window.getComputedStyle(el);
            if (computed.display === 'none' || computed.visibility === 'hidden' || parseFloat(computed.opacity) === 0) {
              continue;
            }

            const isScrollContainer = computed.overflowX === 'auto' || computed.overflowX === 'scroll';
            if (!isScrollContainer && el.scrollWidth > el.clientWidth + 1 && el.clientWidth > 0) {
              internalOverflowElements.push({
                tag,
                id: el.id,
                className: el.className,
                scrollWidth: el.scrollWidth,
                clientWidth: el.clientWidth,
                overflowDelta: el.scrollWidth - el.clientWidth
              });
            }
          }

          return {
            docScrollWidth,
            docClientWidth,
            bodyScrollWidth,
            bodyClientWidth,
            hasDocOverflow,
            hasBodyOverflow,
            overflowsViewport,
            internalOverflowElementsCount: internalOverflowElements.length,
            internalOverflowElements: internalOverflowElements.slice(0, 3)
          };
        }, vp.width);

        const status = (!evaluation.hasDocOverflow && !evaluation.hasBodyOverflow && !evaluation.overflowsViewport)
          ? 'PASS' : 'FAIL';

        console.log(`  [${vp.name} (${vp.width}x${vp.height})] -> ${status} | doc: ${evaluation.docScrollWidth}px/${evaluation.docClientWidth}px | body: ${evaluation.bodyScrollWidth}px/${evaluation.bodyClientWidth}px`);
        if (evaluation.internalOverflowElementsCount > 0) {
          for (const item of evaluation.internalOverflowElements) {
            console.log(`    ⚠ Internal overflow: <${item.tag} id="${item.id}" class="${item.className}"> (scrollWidth=${item.scrollWidth}, clientWidth=${item.clientWidth})`);
          }
        }

        results.viewportChecks.push({
          page: pageName,
          viewport: vp.name,
          width: vp.width,
          height: vp.height,
          status,
          evaluation
        });

      } catch (err) {
        console.error(`  Error testing ${pageName} at ${vp.width}x${vp.height}:`, err.message);
        results.viewportChecks.push({
          page: pageName,
          viewport: vp.name,
          width: vp.width,
          height: vp.height,
          status: 'ERROR',
          error: err.message
        });
      } finally {
        await context.close();
      }
    }
  }

  // ---------------------------------------------------------------------------
  // 3. Mobile Component Visibility & Cascade Defect Verification (375px)
  // ---------------------------------------------------------------------------
  console.log('\n===============================================================');
  console.log('3. RUNNING MOBILE COMPONENT VISIBILITY AUDIT (375px)');
  console.log('===============================================================');

  for (const pageName of TARGET_PAGES) {
    const pageUrl = 'file:///' + path.join(FRONTEND_DIR, pageName).replace(/\\/g, '/');
    const context = await browser.newContext({ viewport: { width: 375, height: 667 } });
    const page = await context.newPage();
    await page.goto(pageUrl, { waitUntil: 'domcontentloaded' });
    await new Promise(r => setTimeout(r, 200));

    const visibility = await page.evaluate(() => {
      const getComp = (id) => {
        const el = document.getElementById(id);
        if (!el) return { exists: false };
        const cs = window.getComputedStyle(el);
        return {
          exists: true,
          display: cs.display,
          visibility: cs.visibility,
          opacity: cs.opacity,
          rect: { width: el.offsetWidth, height: el.offsetHeight }
        };
      };
      return {
        mobileMenuToggle: getComp('mobileMenuToggle'),
        mobileSearchTrigger: getComp('mobileSearchTrigger'),
        mobileSearchDrawer: getComp('mobileSearchDrawer'),
        mobileBottomNav: getComp('mobileBottomNav'),
        postChooserOverlay: getComp('postChooserOverlay'),
        mobileDetailCtaBar: getComp('mobileDetailCtaBar')
      };
    });

    console.log(`[PAGE: ${pageName}] at 375px:`);
    console.log(`  mobileMenuToggle: display='${visibility.mobileMenuToggle.display}' (EXPECTED: 'flex')`);
    console.log(`  mobileSearchTrigger: display='${visibility.mobileSearchTrigger.display}' (EXPECTED: 'inline-flex')`);
    console.log(`  mobileBottomNav: display='${visibility.mobileBottomNav.display}'`);

    const hasToggleBug = visibility.mobileMenuToggle.exists && visibility.mobileMenuToggle.display === 'none';
    const hasSearchTriggerBug = visibility.mobileSearchTrigger.exists && visibility.mobileSearchTrigger.display === 'none';

    results.mobileComponentVisibility.push({
      page: pageName,
      visibility,
      hasToggleBug,
      hasSearchTriggerBug
    });

    if (hasToggleBug) {
      results.defectsIdentified.push({
        severity: 'HIGH',
        component: 'mobileMenuToggle',
        page: pageName,
        issue: 'Hamburger menu button has computed display: none at 375px viewport due to CSS cascade conflict in global.css (line 2126 overrides line 1380).'
      });
    }

    await context.close();
  }

  // ---------------------------------------------------------------------------
  // 4. Interactive State Stress-Testing
  // ---------------------------------------------------------------------------
  console.log('\n===============================================================');
  console.log('4. RUNNING INTERACTIVE MODAL & DRAWER STRESS TESTS (375px)');
  console.log('===============================================================');

  // Test A: Mobile Drawer Opening via JavaScript API (since toggle button is hidden)
  {
    const context = await browser.newContext({ viewport: { width: 375, height: 667 } });
    const page = await context.newPage();
    await page.goto('file:///' + path.join(FRONTEND_DIR, 'index.html').replace(/\\/g, '/'), { waitUntil: 'domcontentloaded' });
    
    const drawerRes = await page.evaluate(() => {
      if (typeof openMobileDrawer === 'function') {
        openMobileDrawer();
        const drawer = document.getElementById('mobileDrawer');
        return {
          opened: drawer ? drawer.classList.contains('open') : false,
          scrollWidth: document.documentElement.scrollWidth,
          clientWidth: document.documentElement.clientWidth
        };
      }
      return { error: 'openMobileDrawer not found' };
    });
    console.log('[INTERACTION] Mobile Drawer Programmatic Open:', drawerRes);
    results.interactionChecks.push({ test: 'openMobileDrawer', result: drawerRes });
    await context.close();
  }

  // Test B: Mobile Filter Sheet on search-properties.html
  {
    const context = await browser.newContext({ viewport: { width: 375, height: 667 } });
    const page = await context.newPage();
    await page.goto('file:///' + path.join(FRONTEND_DIR, 'search-properties.html').replace(/\\/g, '/'), { waitUntil: 'domcontentloaded' });
    const filterBtn = page.locator('.mobile-filter-toggle');
    if (await filterBtn.count() > 0) {
      await filterBtn.click();
      await new Promise(r => setTimeout(r, 300));
      const filterRes = await page.evaluate(() => {
        const sidebar = document.getElementById('filterSidebar');
        return {
          opened: sidebar ? sidebar.classList.contains('open') : false,
          scrollWidth: document.documentElement.scrollWidth,
          clientWidth: document.documentElement.clientWidth
        };
      });
      console.log('[INTERACTION] Filter Drawer Click on search-properties:', filterRes);
      results.interactionChecks.push({ test: 'Filter Drawer Click', result: filterRes });
    }
    await context.close();
  }

  // Test C: Post Chooser Modal on index.html
  {
    const context = await browser.newContext({ viewport: { width: 375, height: 667 } });
    const page = await context.newPage();
    await page.goto('file:///' + path.join(FRONTEND_DIR, 'index.html').replace(/\\/g, '/'), { waitUntil: 'domcontentloaded' });
    const postBtn = page.locator('.bottom-nav-post-btn');
    if (await postBtn.count() > 0) {
      await postBtn.click();
      await new Promise(r => setTimeout(r, 300));
      const postRes = await page.evaluate(() => {
        const overlay = document.getElementById('postChooserOverlay');
        return {
          opened: overlay ? overlay.classList.contains('open') : false,
          scrollWidth: document.documentElement.scrollWidth,
          clientWidth: document.documentElement.clientWidth
        };
      });
      console.log('[INTERACTION] Post Chooser Modal Click:', postRes);
      results.interactionChecks.push({ test: 'Post Chooser Modal Click', result: postRes });
    }
    await context.close();
  }

  // Test D: Sticky CTA Booking Sheet on property-detail.html
  {
    const context = await browser.newContext({ viewport: { width: 375, height: 667 } });
    const page = await context.newPage();
    await page.goto('file:///' + path.join(FRONTEND_DIR, 'property-detail.html').replace(/\\/g, '/'), { waitUntil: 'domcontentloaded' });
    const bookBtn = page.locator('#mobileCtaBookBtn');
    if (await bookBtn.count() > 0) {
      await bookBtn.click();
      await new Promise(r => setTimeout(r, 300));
      const bookRes = await page.evaluate(() => {
        const sheet = document.getElementById('bookingSheetOverlay');
        return {
          opened: sheet ? sheet.classList.contains('open') : false,
          scrollWidth: document.documentElement.scrollWidth,
          clientWidth: document.documentElement.clientWidth
        };
      });
      console.log('[INTERACTION] Booking Sheet Modal Click on property-detail:', bookRes);
      results.interactionChecks.push({ test: 'Booking Sheet Modal Click', result: bookRes });
    }
    await context.close();
  }

  // Test E: Sticky CTA Order Sheet on product-detail.html
  {
    const context = await browser.newContext({ viewport: { width: 375, height: 667 } });
    const page = await context.newPage();
    await page.goto('file:///' + path.join(FRONTEND_DIR, 'product-detail.html').replace(/\\/g, '/'), { waitUntil: 'domcontentloaded' });
    const buyBtn = page.locator('#mobileCtaBuyBtn');
    if (await buyBtn.count() > 0) {
      await buyBtn.click();
      await new Promise(r => setTimeout(r, 300));
      const buyRes = await page.evaluate(() => {
        const sheet = document.getElementById('orderSheetOverlay');
        return {
          opened: sheet ? sheet.classList.contains('open') : false,
          scrollWidth: document.documentElement.scrollWidth,
          clientWidth: document.documentElement.clientWidth
        };
      });
      console.log('[INTERACTION] Order Sheet Modal Click on product-detail:', buyRes);
      results.interactionChecks.push({ test: 'Order Sheet Modal Click', result: buyRes });
    }
    await context.close();
  }

  await browser.close();

  // ---------------------------------------------------------------------------
  // 5. Final Assessment & Verdict
  // ---------------------------------------------------------------------------
  console.log('\n===============================================================');
  console.log('5. FINAL VERDICT COMPUTATION');
  console.log('===============================================================');

  const viewportFailures = results.viewportChecks.filter(c => c.status === 'FAIL');
  console.log(`Total Viewport Tests: ${results.viewportChecks.length} | Failures: ${viewportFailures.length}`);
  console.log(`Defects Identified: ${results.defectsIdentified.length}`);

  const verdict = (results.defectsIdentified.length === 0 && viewportFailures.length === 0) ? 'APPROVE' : 'REJECT';
  results.verdict = verdict;

  console.log(`\nOVERALL VERDICT: ${verdict}`);
  if (verdict === 'REJECT') {
    console.log('\nREASONS FOR REJECTION:');
    results.defectsIdentified.forEach((d, idx) => {
      console.log(`${idx + 1}. [${d.severity}] ${d.component} on ${d.page}: ${d.issue}`);
    });
  }

  fs.writeFileSync(
    path.join(BASE_DIR, 'scripts', 'viewport_test_results.json'),
    JSON.stringify(results, null, 2)
  );
  console.log('\nResults saved to scripts/viewport_test_results.json');
})();
