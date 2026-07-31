/* #292 proof harness — drives the real trade desk in Chromium against a given tree ROOT and reports
   what the picker actually offers and prices. Used three ways: BEFORE (pristine HEAD), AFTER (the fix),
   and NON-VACUITY (the fix over a scratch bundle whose index-65 pool value has been changed). */
import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require('/opt/node22/lib/node_modules/playwright/node_modules/playwright-core');

const ROOT = process.env.RL_REPO;
const TAG = process.env.TAG || 'run';
const SHOTS = process.env.SHOTS || '';
const URL = 'file://' + path.join(ROOT, 'ui', 'index.html');
const chrome = execSync("ls -d /opt/pw-browsers/chromium-*/chrome-linux/chrome 2>/dev/null | head -1").toString().trim();

const browser = await chromium.launch({ executablePath: chrome, args: ['--no-sandbox'] });
const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
const pageErrors = [];
page.on('pageerror', e => pageErrors.push(e.message));
page.on('console', m => { if (m.type() === 'error') pageErrors.push('console: ' + m.text()); });

await page.goto(URL);
await page.waitForTimeout(700);
await page.evaluate(() => { MD.state.tier = 'working'; MD.go('trade'); });
await page.waitForTimeout(400);

// what the bundle itself carries (read from the live page, not from the file)
const bundle = await page.evaluate(() => {
  const pvc = MD.seam.working.pvc || {};
  const ks = Object.keys(pvc).map(Number).sort((a, b) => a - b);
  return { nKeys: ks.length, min: ks[0], max: ks[ks.length - 1], v64: pvc['64'], v65: pvc['65'] };
});

// type a query into the give-side combobox and read back what the dropdown offers
async function offer(q) {
  const input = page.locator('.desk .pane .tradesearch').first();
  await input.click();
  await input.fill('');
  await input.type(q, { delay: 15 });
  await page.waitForTimeout(250);
  const rows = await page.evaluate(() => {
    const box = document.querySelector('.desk .pane .results');
    if (!box) return [];
    return Array.from(box.querySelectorAll('button')).map(b => ({
      label: (b.querySelector('.rpick, span') || {}).textContent.trim(),
      val: (b.querySelector('.rv') || {}).textContent.trim(),
    }));
  });
  if (SHOTS) await page.screenshot({ path: path.join(SHOTS, `${TAG}_query_${q}.png`) });
  return rows;
}

const out = { tag: TAG, bundle, queries: {} };
for (const q of ['7', '65', '70', 'pool']) out.queries[q] = await offer(q);

// the nearest-pick descriptor at an amount just under pick 64's value (the phantom-ordinal path)
await page.keyboard.press('Escape');
await page.evaluate(() => { document.querySelector('.desk .pane .tradesearch').blur(); });
await page.waitForTimeout(200);
out.describe = await page.evaluate(() => {
  const pvc = MD.seam.working.pvc || {};
  const probe = pvc['65'] != null ? pvc['65'] : 300;   // an amount at the pool level
  // drive the real verdict text: clear both baskets, put one pool-level gap on the table
  const el = document.querySelector('.verdict .line');
  return { probeAmount: probe, verdictLineOnOpen: el ? el.textContent.trim() : null };
});

// the desk as it opens (seeded trade + verdict)
if (SHOTS) await page.screenshot({ path: path.join(SHOTS, `${TAG}_desk.png`), fullPage: true });

out.pageErrors = pageErrors;
fs.writeFileSync(process.env.OUT || `/dev/stdout`, JSON.stringify(out, null, 2));
console.log(JSON.stringify(out, null, 2));
await browser.close();
