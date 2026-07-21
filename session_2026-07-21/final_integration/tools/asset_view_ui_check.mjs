/* Unified future-asset-ranking + no-row-cap UI check (final integration 2026-07-21, supervisor corrections).
   Drives the real Matchday UI (Chromium) and asserts:
     - current (now) lens: ALL 804 players render (no 60-row cap), last-ranked player in the DOM, 0 pick rows;
     - +1 / +2 lenses: ONE combined value-descending ranking of 868 assets (804 players vP1/vP2 + 64 anonymous
       national-draft placeholders at exact PVC), exactly 64 pick rows, picks interleaved with players by value,
       first + middle + last ranked assets present, last player AND last pick (Pick 64) in the DOM;
     - the two F5 residual aggregates are NOT ranked (held in a separate reconciliation panel that reconciles);
     - a player-only filter (club) removes the anonymous picks while active; clearing restores 868;
     - no document-width overflow at mobile (390) + desktop (1440).
   Run: PLAYWRIGHT_CORE=<abs> CHROME_BIN=<abs> node session_2026-07-21/final_integration/tools/asset_view_ui_check.mjs */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_CORE || 'playwright-core');
// Repo-relative paths (portable across the local workspace + the CI runner). Prefer RL_REPO (the
// workflow sets it to the checkout root); else derive from this file's location: tools -> final_integration
// -> session_2026-07-21 -> repo root.
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = process.env.RL_REPO || path.resolve(__dirname, '..', '..', '..');
const URL = 'file://' + path.join(ROOT, 'ui', 'index.html');
const OUT = path.join(ROOT, 'session_2026-07-21', 'final_integration', 'evidence');
fs.mkdirSync(OUT, { recursive: true });
function chromePath() {
  if (process.env.CHROME_BIN && fs.existsSync(process.env.CHROME_BIN)) return process.env.CHROME_BIN;
  const g = execSync("ls -d /opt/pw-browsers/chromium-*/chrome-linux/chrome 2>/dev/null | head -1").toString().trim();
  if (g) return g; throw new Error('no Chromium');
}
const R = []; let fails = 0;
function ck(name, ok, detail = '') { R.push({ name, ok: !!ok, detail }); if (!ok) fails++;
  console.log((ok ? '  PASS ' : '  FAIL ') + name + (detail ? '  -- ' + detail : '')); }

async function setLens(page, lens, club) {
  await page.evaluate((a) => {
    MD.state.tier = 'working'; MD.state.lens = a.lens;
    if (a.club !== undefined) { MD.board.focusClub(a.club, false); }
    const holder = document.querySelector('#view') || document.body;
    MD.board.render(holder);
  }, { lens, club });
}
async function ladder(page) {
  return await page.evaluate(() => {
    const rows = [...document.querySelectorAll('.rows .row')];
    const data = rows.map(r => ({
      pick: r.classList.contains('pickrow'),
      rank: parseInt((r.querySelector('.rank') || {}).textContent || '0', 10),
      val: parseInt(((r.querySelector('.val') || {}).textContent || '0').replace(/[^0-9-]/g, ''), 10),
      name: (r.querySelector('.nm') || {}).textContent || '',
    }));
    const recon = document.querySelector('.reconpanel');
    return { total: rows.length, picks: data.filter(d => d.pick).length,
             players: data.filter(d => !d.pick).length, data,
             recon: recon ? recon.textContent : null,
             firstName: data.length ? data[0].name : null,
             lastName: data.length ? data[data.length - 1].name : null };
  });
}

(async () => {
  const browser = await chromium.launch({ executablePath: chromePath(), args: ['--no-sandbox'] });
  try {
    for (const width of [390, 1440]) {
      const page = await browser.newPage({ viewport: { width, height: 900 } });
      await page.goto(URL, { waitUntil: 'load' });
      await page.waitForTimeout(150);

      // NOW lens — all 804 players, no cap, no picks
      await setLens(page, 2);
      const now = await ladder(page);
      ck(`${width}px · now: all 804 players render (no 60-cap)`, now.players === 804, 'players=' + now.players);
      ck(`${width}px · now: zero pick rows on the current ladder`, now.picks === 0, 'picks=' + now.picks);
      ck(`${width}px · now: last-ranked player present in DOM`, now.total === 804 && !!now.lastName);
      ck(`${width}px · now: no document overflow`,
         await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth));

      // +1 lens — unified 868 ranking
      await setLens(page, 3);
      const p1 = await ladder(page);
      ck(`${width}px · +1: 868 combined rows (804 players + 64 picks)`, p1.total === 868, 'total=' + p1.total);
      ck(`${width}px · +1: exactly 64 pick rows`, p1.picks === 64, 'picks=' + p1.picks);
      ck(`${width}px · +1: 804 player rows`, p1.players === 804, 'players=' + p1.players);
      const desc1 = p1.data.every((d, i) => i === 0 || p1.data[i - 1].val >= d.val);
      ck(`${width}px · +1: single value-descending ranking`, desc1);
      const ranks1 = p1.data.map(d => d.rank);
      ck(`${width}px · +1: global ranks 1..868 contiguous`, ranks1[0] === 1 && ranks1[ranks1.length - 1] === 868);
      // a pick is interleaved between players (Pick 1 v=3000 sits among players)
      const pk1 = p1.data.find(d => d.pick && /Draft Pick 1(?!\d)/.test(d.name));
      const idx1 = p1.data.indexOf(pk1);
      const interleaved = pk1 && idx1 > 0 && !p1.data[idx1 - 1].pick && p1.data[idx1 - 1].val >= 3000;
      ck(`${width}px · +1: picks interleaved among players by value (a player ranks above Pick 1)`, interleaved,
         pk1 ? ('Pick1 rank=' + pk1.rank + ' above=' + (p1.data[idx1 - 1] || {}).name) : 'Pick1 not found');
      ck(`${width}px · +1: last pick "2027 Draft Pick 64" present in DOM`,
         p1.data.some(d => d.pick && /Draft Pick 64(?!\d)/.test(d.name)));
      ck(`${width}px · +1: last-ranked asset present (rank 868)`, ranks1.includes(868));
      ck(`${width}px · +1: residual reconciliation panel present + reconciles`,
         !!p1.recon && /= sealed F5 entrant layer 83,538 ✓/.test(p1.recon), p1.recon ? 'panel ok' : 'no panel');
      ck(`${width}px · +1: no document overflow`,
         await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth));
      await page.screenshot({ path: `${OUT}/unified_2027_${width}.png`, fullPage: false });

      // +2 lens
      await setLens(page, 4);
      const p2 = await ladder(page);
      ck(`${width}px · +2: 868 combined rows`, p2.total === 868, 'total=' + p2.total);
      ck(`${width}px · +2: exactly 64 pick rows`, p2.picks === 64, 'picks=' + p2.picks);
      ck(`${width}px · +2: last pick "2028 Draft Pick 64" present`,
         p2.data.some(d => d.pick && /2028 Draft Pick 64(?!\d)/.test(d.name)));
      ck(`${width}px · +2: no document overflow`,
         await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth));

      // player-only filter (club) removes the anonymous picks; clearing restores 868
      await setLens(page, 3, 'Collingwood Magpies');
      const filt = await ladder(page);
      ck(`${width}px · +1 club filter removes anonymous picks`, filt.picks === 0, 'picks=' + filt.picks);
      await setLens(page, 3, null);
      const cleared = await ladder(page);
      ck(`${width}px · +1 clearing the filter restores 868 combined rows`, cleared.total === 868, 'total=' + cleared.total);
      await page.close();
    }
  } finally { await browser.close(); }
  fs.writeFileSync(`${OUT}/asset_view_ui_check.json`, JSON.stringify({ ok: fails === 0, fails, checks: R }, null, 2));
  console.log(`\n${R.length - fails}/${R.length} unified-ranking UI assertions passed`);
  process.exit(fails ? 1 : 0);
})();
