const { chromium } = require('C:/Users/divya/AppData/Local/Programs/Python/Python312/Lib/site-packages/playwright/driver/package');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  page.on('console', msg => console.log('BROWSER LOG:', msg.type(), msg.text()));
  page.on('pageerror', err => console.log('BROWSER UNCAUGHT:', err.message));
  page.on('requestfailed', req => console.log('REQ FAILED:', req.url(), req.failure()?.errorText));
  page.on('response', resp => {
    if (resp.url().includes('/api/')) {
      console.log('API RESPONSE:', resp.status(), resp.url());
    }
  });
  
  const targetUrl = 'https://constitutional-republican-consulting-heavily.trycloudflare.com/register.html';
  console.log('Navigating to:', targetUrl);
  await page.goto(targetUrl, { waitUntil: 'networkidle' });
  
  const testId = Date.now() % 10000;
  console.log('Filling fields with testId:', testId);
  await page.fill('#name', 'Test Student ' + testId);
  await page.fill('#email', 'student_' + testId + '@gehu.ac.in');
  await page.fill('#phone', '9876543210');
  await page.selectOption('#city', 'Dehradun');
  await page.fill('#password', 'StudentPass@123');
  await page.fill('#confirmPassword', 'StudentPass@123');
  
  console.log('Clicking Create Account button...');
  await page.click('#submitBtn');
  
  await page.waitForTimeout(3000);
  
  const toastText = await page.evaluate(() => {
    const el = document.getElementById('toast') || document.querySelector('.toast-container') || document.querySelector('.toast');
    return el ? el.innerText : 'NO TOAST';
  });
  console.log('Toast Result:', toastText);
  
  const currentUrl = page.url();
  console.log('Final Page URL:', currentUrl);
  
  const token = await page.evaluate(() => localStorage.getItem('staymart_token'));
  console.log('Local Storage Token:', token ? token.slice(0, 30) + '...' : 'NONE');
  
  await browser.close();
})();
