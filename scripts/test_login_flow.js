const { chromium } = require('C:/Users/divya/AppData/Local/Programs/Python/Python312/Lib/site-packages/playwright/driver/package');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  page.on('console', msg => console.log('BROWSER LOG:', msg.type(), msg.text()));
  page.on('response', resp => {
    if (resp.url().includes('/api/')) {
      console.log('API RESPONSE:', resp.status(), resp.url());
    }
  });
  
  const targetUrl = 'https://constitutional-republican-consulting-heavily.trycloudflare.com/login.html';
  console.log('Navigating to:', targetUrl);
  await page.goto(targetUrl, { waitUntil: 'networkidle' });
  
  console.log('Filling login credentials...');
  await page.fill('#email', 'admin@staymart.com');
  await page.fill('#password', 'Admin@123');
  
  console.log('Clicking Login button...');
  await page.click('#submitBtn');
  
  await page.waitForTimeout(3000);
  
  const currentUrl = page.url();
  console.log('Final Page URL:', currentUrl);
  
  const token = await page.evaluate(() => localStorage.getItem('staymart_token'));
  console.log('Stored Token:', token ? token.slice(0, 30) + '...' : 'NONE');
  
  await browser.close();
  if (token && currentUrl.includes('dashboard.html')) {
    console.log('SUCCESS: Browser admin login verified perfectly!');
  }
})();
