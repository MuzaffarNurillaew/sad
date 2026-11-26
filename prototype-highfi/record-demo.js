'use strict';
// One-off script to record the <=1 minute CW2 screencast. Not part of the
// prototype itself - run manually, not referenced by server.js.
const { chromium } = require('/home/muzaffar/.npm/_npx/e41f203b7505f1fb/node_modules/playwright');
const path = require('path');
const fs = require('fs');

const VIDEO_DIR = path.join(__dirname, '..', 'build', 'cw2-video');
const marks = [];
let t0;
function mark(label) {
  const t = (Date.now() - t0) / 1000;
  marks.push({ t, label });
  console.log(t.toFixed(2) + 's', label);
}

async function main() {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 420, height: 820 },
    recordVideo: { dir: VIDEO_DIR, size: { width: 420, height: 820 } },
  });
  const page = await context.newPage();
  t0 = Date.now();

  await page.goto('http://localhost:4100');
  await page.waitForTimeout(1200);
  mark('Logging in as a Worker (Aziz)');

  // 1. Log in as a worker.
  await page.fill('#loginName', 'Aziz');
  await page.selectOption('#loginRole', 'worker');
  await page.click('#loginForm button[type=submit]');
  await page.waitForTimeout(1500);
  mark('Worker dashboard: House 1 / House 2 and their active batches');

  // 2. Open the active batch - mortality log + 403 financial panel.
  await page.locator('#housesList button', { hasText: 'Open' }).first().click();
  await page.waitForTimeout(2600);
  mark('Logging a chick death (FR-01)');

  await page.fill('#mortalityNote', 'found near feeder, House 1');
  await page.click('#mortalityForm button[type=submit]');
  await page.waitForTimeout(2800);
  mark('Logging out, logging back in as the Director');

  // 3. Log out, log back in as the director.
  await page.click('#logoutBtn');
  await page.waitForTimeout(900);
  await page.fill('#loginName', 'Director');
  await page.selectOption('#loginRole', 'director');
  await page.click('#loginForm button[type=submit]');
  await page.waitForTimeout(1200);
  mark('Director dashboard, opening the same batch');

  // 4. Open the same batch - profit panel now visible.
  await page.locator('#housesList button', { hasText: 'Open' }).first().click();
  await page.waitForTimeout(3200);
  mark('Recording a bazaar sale: 1200kg reported vs 1140kg trusted-rep weighing');

  // 5. Record a bazaar sale with a mismatched trusted-rep weighing.
  await page.selectOption('#saleBuyerType', 'bazaar');
  await page.fill('#saleKg', '1200');
  await page.fill('#saleTrustedKg', '1140');
  await page.fill('#saleRate', '26000');
  await page.click('#saleForm button[type=submit]');
  await page.waitForTimeout(3600);
  mark('End');

  await context.close();
  await browser.close();

  fs.writeFileSync(path.join(VIDEO_DIR, 'marks.json'), JSON.stringify(marks, null, 2));
  console.log('Recorded to', VIDEO_DIR);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
