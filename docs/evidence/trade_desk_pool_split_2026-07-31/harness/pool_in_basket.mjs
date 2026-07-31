/* #292 — select the pool item and prove the BASKET render path: the row chip names the pool, the row
   prices at the artifact value, the total moves by exactly that value, and the stored item carries no
   ordinal `n` at all (so nothing downstream can read one off it). */
import path from 'path';
import { execSync } from 'child_process';
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require('/opt/node22/lib/node_modules/playwright/node_modules/playwright-core');

const ROOT = process.env.RL_REPO;
const SHOTS = process.env.SHOTS;
const chrome = execSync("ls -d /opt/pw-browsers/chromium-*/chrome-linux/chrome 2>/dev/null | head -1").toString().trim();
const browser = await chromium.launch({ executablePath: chrome, args: ['--no-sandbox'] });
const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
const errs = []; page.on('pageerror', e => errs.push(e.message));
page.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });

await page.goto('file://' + path.join(ROOT, 'ui', 'index.html'));
await page.waitForTimeout(700);
await page.evaluate(() => { MD.state.tier = 'working'; MD.go('trade'); });
await page.waitForTimeout(400);

const totalBefore = await page.locator('.desk .pane').first().locator('.ttotal .tfig').innerText();

const input = page.locator('.desk .pane .tradesearch').first();
await input.click(); await input.type('70', { delay: 20 });
await page.waitForTimeout(250);
await page.locator('.desk .pane .results button').first().click();   // mousedown handler fires
await page.waitForTimeout(350);

const after = await page.evaluate(() => {
  const give = MD.state.trade.give;
  const it = give[give.length - 1];
  const rows = Array.from(document.querySelectorAll('.desk .pane')).shift()
    .querySelectorAll('.trow');
  const last = rows[rows.length - 1];
  return {
    storedItem: it,
    storedKeys: Object.keys(it),
    hasOrdinalN: Object.prototype.hasOwnProperty.call(it, 'n'),
    rowText: last.innerText.replace(/\s+/g, ' ').trim(),
    total: document.querySelector('.desk .pane .ttotal .tfig').innerText,
  };
});
await page.screenshot({ path: path.join(SHOTS, 'after_pool_in_basket.png'), fullPage: true });

console.log(JSON.stringify({ totalBefore, ...after, pageErrors: errs }, null, 2));
await browser.close();
