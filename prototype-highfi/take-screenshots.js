'use strict';
const { chromium } = require('/home/muzaffar/.npm/_npx/e41f203b7505f1fb/node_modules/playwright');
const path = require('path');

const OUT_DIR = path.join(__dirname, '..', 'build', 'cw2-screenshots');

async function main() {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 420, height: 820 } });
  await page.setViewportSize({ width: 420, height: 820 });

  await page.goto('http://localhost:4100');
  await page.waitForTimeout(300);
  await page.screenshot({ path: path.join(OUT_DIR, '01-login.png') });

  await page.fill('#loginName', 'Aziz');
  await page.selectOption('#loginRole', 'worker');
  await page.click('#loginForm button[type=submit]');
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(OUT_DIR, '02-dashboard.png') });

  await page.locator('#housesList button', { hasText: 'Open' }).first().click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(OUT_DIR, '03-batch-worker-403.png') });

  await page.click('#logoutBtn');
  await page.waitForTimeout(300);
  await page.fill('#loginName', 'Director');
  await page.selectOption('#loginRole', 'director');
  await page.click('#loginForm button[type=submit]');
  await page.waitForTimeout(500);
  await page.locator('#housesList button', { hasText: 'Open' }).first().click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(OUT_DIR, '04-batch-director-profit.png') });

  await page.selectOption('#saleBuyerType', 'bazaar');
  await page.fill('#saleKg', '1200');
  await page.fill('#saleTrustedKg', '1140');
  await page.fill('#saleRate', '26000');
  await page.click('#saleForm button[type=submit]');
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(OUT_DIR, '05-sale-mismatch-flagged.png'), fullPage: true });

  await browser.close();
  console.log('Screenshots saved to', OUT_DIR);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
