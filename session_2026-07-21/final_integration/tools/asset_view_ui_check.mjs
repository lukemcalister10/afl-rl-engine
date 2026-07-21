/* Visible future-draft asset-view UI check (final integration 2026-07-21).
   Drives the real Matchday UI (Chromium) and asserts, at the +1 and +2 lenses and at desktop + mobile
   widths: the asset ladder renders exactly 64 visible national-draft placeholders + 2 labelled residual
   aggregates; the current (now) lens shows ZERO asset rows (player-only ladder); pick rows carry no
   player card link; no document-width overflow. Writes evidence + screenshots.

   Run: PLAYWRIGHT_CORE=<abs> CHROME_BIN=<abs> node session_2026-07-21/final_integration/tools/asset_view_ui_check.mjs */
import fs from 'fs';
import { execSync } from 'child_process';
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_CORE || 'playwright-core');
const URL = 'file:///home/user/afl-rl-engine/ui/index.html';
const OUT = '/home/user/afl-rl-engine/session_2026-07-21/final_integration/evidence';
fs.mkdirSync(OUT, { recursive: true });
function chromePath() {
  if (process.env.CHROME_BIN && fs.existsSync(process.env.CHROME_BIN)) return process.env.CHROME_BIN;
  const g = execSync("ls -d /opt/pw-browsers/chromium-*/chrome-linux/chrome 2>/dev/null | head -1").toString().trim();
  if (g) return g; throw new Error('no Chromium');
}
const R = []; let fails = 0;
function ck(name, ok, detail = '') { R.push({ name, ok: !!ok, detail }); if (!ok) fails++;
  console.log((ok ? '  PASS ' : '  FAIL ') + name + (detail ? '  -- ' + detail : '')); }

// set the working tier + a given lens, then re-render the board view
async function setLens(page, lens) {
  await page.evaluate((l) => {
    MD.state.tier = 'working'; MD.state.lens = l;
    const holder = document.querySelector('#view') || document.body;
    MD.board.render(holder);
  }, lens);
}
async function assetInfo(page) {
  return await page.evaluate(() => {
    const sec = document.querySelector('.assetladder');
    if (!sec) return { present: false, visible: 0, residual: 0, links: 0, firstLabel: null, lastLabel: null };
    const rows = [...sec.querySelectorAll('.pickrow')];
    const vis = rows.filter(r => /Draft Pick \d+/.test(r.querySelector('.nm').textContent));
    const res = rows.filter(r => /aggregate/i.test(r.textContent) || /Entrant aggregate/.test(r.textContent));
    return { present: true, total: rows.length, visible: vis.length, residual: res.length,
             firstLabel: rows[0] ? rows[0].querySelector('.nm').textContent.replace(/Draft asset|Entrant aggregate/, '').trim() : null,
             lastVisible: vis.length ? vis[vis.length - 1].querySelector('.nm').textContent.replace('Draft asset', '').trim() : null };
  });
}

(async () => {
  const browser = await chromium.launch({ executablePath: chromePath(), args: ['--no-sandbox'] });
  try {
    for (const width of [390, 1440]) {
      const page = await browser.newPage({ viewport: { width, height: 900 } });
      await page.goto(URL, { waitUntil: 'load' });
      await page.waitForTimeout(150);

      // NOW lens (2): player-only ladder, zero asset rows
      await setLens(page, 2);
      const now = await assetInfo(page);
      ck(`${width}px · now-lens: no asset ladder (player-only)`, !now.present, 'present=' + now.present);
      const nowOverflow = await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth);
      ck(`${width}px · now-lens: no document overflow`, nowOverflow);

      // +1 lens (3): 64 visible 2027 picks + 2 residual aggregates
      await setLens(page, 3);
      const p1 = await assetInfo(page);
      ck(`${width}px · +1 asset ladder present`, p1.present);
      ck(`${width}px · +1 exactly 64 visible 2027 picks`, p1.visible === 64, 'visible=' + p1.visible);
      ck(`${width}px · +1 exactly 2 residual aggregates`, p1.residual === 2, 'residual=' + p1.residual);
      ck(`${width}px · +1 first row = "2027 Draft Pick 1"`, /2027 Draft Pick 1\b/.test(p1.firstLabel || ''), p1.firstLabel);
      ck(`${width}px · +1 last visible = "2027 Draft Pick 64"`, /2027 Draft Pick 64\b/.test(p1.lastVisible || ''), p1.lastVisible);
      const p1Overflow = await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth);
      ck(`${width}px · +1 no document overflow`, p1Overflow);
      // pick rows must not link to a player card (no data-key / click target to a player)
      const noCardLink = await page.evaluate(() => {
        const rows = [...document.querySelectorAll('.assetladder .pickrow')];
        return rows.every(r => r.getAttribute('data-asset') && !r.querySelector('.slug'));
      });
      ck(`${width}px · +1 pick rows carry asset id, no player identity`, noCardLink);
      await page.screenshot({ path: `${OUT}/asset_view_2027_${width}.png` });

      // +2 lens (4): 64 visible 2028 picks + 2 residual
      await setLens(page, 4);
      const p2 = await assetInfo(page);
      ck(`${width}px · +2 exactly 64 visible 2028 picks`, p2.visible === 64, 'visible=' + p2.visible);
      ck(`${width}px · +2 exactly 2 residual aggregates`, p2.residual === 2, 'residual=' + p2.residual);
      ck(`${width}px · +2 first row = "2028 Draft Pick 1"`, /2028 Draft Pick 1\b/.test(p2.firstLabel || ''), p2.firstLabel);
      const p2Overflow = await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth);
      ck(`${width}px · +2 no document overflow`, p2Overflow);
      await page.screenshot({ path: `${OUT}/asset_view_2028_${width}.png` });
      await page.close();
    }
  } finally { await browser.close(); }
  fs.writeFileSync(`${OUT}/asset_view_ui_check.json`, JSON.stringify({ ok: fails === 0, fails, checks: R }, null, 2));
  console.log(`\n${R.length - fails}/${R.length} asset-view UI assertions passed`);
  process.exit(fails ? 1 : 0);
})();
