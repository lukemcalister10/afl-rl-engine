/* Matchday UI — RESPONSIVE LAYOUT acceptance (Chromium-driven). Replaces the weak generic
   "board renders" assertion with real layout assertions at phone/tablet/desktop widths.

   Run:  NODE_PATH=<dir-with-playwright-core> node ui/tests/responsive_layout.test.mjs
         (the repo has no package.json; this browser test uses playwright-core + the pre-installed
          Chromium at $CHROME_BIN or the /opt/pw-browsers chromium build. exit 0 = all pass.)

   Viewport widths tested: 320, 360, 390, 430, 720, 1440.
   At every width it asserts:
     - document.documentElement.scrollWidth <= window.innerWidth  (no horizontal document overflow);
     - the first five player names have usable width and render in <= 2 text lines (never char-by-char);
     - every navigation destination is reachable (hit-testable) and not clipped by an overflow region;
     - rank, player name, club and value are visible in the first five rows;
     - the Club-valuation and held-pick views render without HALT (and without document overflow).
   1440 additionally documents that the desktop layout is preserved. */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';
import { createRequire } from 'module';

// playwright-core is not a repo dependency (the repo has no package.json). Resolve it via CJS require
// from $PLAYWRIGHT_CORE (an absolute path to the module) when provided, else the bare specifier
// (works when playwright-core is installed / on NODE_PATH).
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_CORE || 'playwright-core');

// Repo-relative paths (portable across the local workspace + the CI runner). Prefer RL_REPO (the
// workflow sets it to the checkout root); else derive from this file's location: tests -> ui -> repo root.
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = process.env.RL_REPO || path.resolve(__dirname, '..', '..');
const URL = 'file://' + path.join(ROOT, 'ui', 'index.html');
const OUT = path.join(ROOT, 'session_2026-07-20', 'ui_release_seam', 'evidence');
fs.mkdirSync(OUT, { recursive: true });

function chromePath() {
  if (process.env.CHROME_BIN && fs.existsSync(process.env.CHROME_BIN)) return process.env.CHROME_BIN;
  const g = execSync("ls -d /opt/pw-browsers/chromium-*/chrome-linux/chrome 2>/dev/null | head -1").toString().trim();
  if (g) return g;
  throw new Error('no Chromium binary found (set CHROME_BIN)');
}

const WIDTHS = [320, 360, 390, 430, 720, 1440];
const results = [];
let fails = 0;
function assert(width, name, ok, detail = '') {
  results.push({ width, name, ok: !!ok, detail });
  if (!ok) fails++;
  console.log(`    [${ok ? 'PASS' : 'FAIL'}] ${width}px · ${name}${detail ? '  (' + detail + ')' : ''}`);
}

async function clickByText(page, sel, text) {
  for (const e of await page.$$(sel)) {
    const t = ((await e.innerText().catch(() => '')) || '').trim().toLowerCase();
    if (t === text.toLowerCase()) { await e.click(); return true; }
  }
  return false;
}

// In-page layout probe for the board view — returns everything measured in the browser.
const PROBE = () => {
  const lh = (el) => {
    const cs = getComputedStyle(el);
    let v = parseFloat(cs.lineHeight);
    if (!isFinite(v)) v = parseFloat(cs.fontSize) * 1.2;
    return v;
  };
  const inView = (r) => r.width > 0 && r.height > 0 &&
    r.left >= -0.5 && r.right <= window.innerWidth + 0.5 && r.top >= -0.5 && r.bottom <= window.innerHeight + 0.5;
  // names
  const nms = [...document.querySelectorAll('.rows .row.working .nm')].slice(0, 5);
  const names = nms.map((el) => {
    const r = el.getBoundingClientRect();
    return { text: (el.textContent || '').trim(), width: Math.round(r.width),
             lines: Math.round(el.scrollHeight / lh(el)) };
  });
  // first-5 rows: rank/name/club/value present + visible
  const rows = [...document.querySelectorAll('.rows .row.working')].slice(0, 5).map((row) => {
    const g = (s) => row.querySelector(s);
    const vis = (el) => !!el && el.offsetParent !== null && el.getBoundingClientRect().width > 0 && (el.textContent || '').trim() !== '';
    return { rank: vis(g('.rank')), name: vis(g('.nm')), club: vis(g('.club .affl')),
             val: vis(g('.val')), pill: !!g('.pill') };
  });
  // nav: every destination reachable (hit-testable at its centre) and within the viewport
  const tabsBox = document.querySelector('.tabs');
  const navEls = [...document.querySelectorAll('.tabs button'), ...document.querySelectorAll('.tier button')];
  const nav = navEls.map((el) => {
    const r = el.getBoundingClientRect();
    const cx = r.left + r.width / 2, cy = r.top + r.height / 2;
    const hit = document.elementFromPoint(cx, cy);
    return { text: (el.textContent || '').trim(), inView: inView(r),
             hittable: !!hit && (hit === el || el.contains(hit) || (hit.closest && hit.closest('.tabs,.tier') === el.closest('.tabs,.tier') && el.contains(hit))) };
  });
  const tabsCS = tabsBox ? getComputedStyle(tabsBox) : null;
  const tabsClips = !!tabsBox && (tabsCS.overflowX === 'hidden' || tabsCS.overflowX === 'clip') &&
    tabsBox.scrollWidth > tabsBox.clientWidth + 1;
  return {
    scrollWidth: document.documentElement.scrollWidth, innerWidth: window.innerWidth,
    names, rows, nav, tabsClips,
  };
};

// In-page probe for the club view — renders without HALT + no document overflow.
const CLUB_PROBE = () => {
  const halted = !!document.querySelector('.cintro .halt') ||
    /HALTED|refuses|STALE-CURVE/i.test(document.body.innerText);
  const clubRows = document.querySelectorAll('.ctable tbody tr').length;
  return { halted, clubRows, scrollWidth: document.documentElement.scrollWidth, innerWidth: window.innerWidth };
};

const browser = await chromium.launch({ executablePath: chromePath(),
  args: ['--no-sandbox', '--disable-gpu', '--allow-file-access-from-files', '--hide-scrollbars'] });

console.log('=== RESPONSIVE LAYOUT ACCEPTANCE ===');
for (const width of WIDTHS) {
  const isMobile = width < 1440;
  const ctx = await browser.newContext({ viewport: { width, height: 844 }, deviceScaleFactor: 2 });
  const page = await ctx.newPage();
  await page.goto(URL, { waitUntil: 'networkidle' });
  await page.waitForTimeout(500);

  // integrity: never the fail-closed screen
  const alarm = await page.evaluate(() => /fail-?closed|board rejected/i.test(document.body.innerText));
  assert(width, 'no fail-closed / integrity alarm', !alarm);

  const m = await page.evaluate(PROBE);

  // (a) no horizontal document overflow
  assert(width, 'scrollWidth <= innerWidth', m.scrollWidth <= m.innerWidth,
    `scrollWidth=${m.scrollWidth} innerWidth=${m.innerWidth}`);

  // (b) first five names: usable width + <= 2 lines + not char-by-char
  const named = m.names.length >= 5;
  assert(width, 'first five player names present', named, `${m.names.length} names`);
  const usable = m.names.every((n) => n.width >= 50);
  const twoLines = m.names.every((n) => n.lines <= 2 && n.lines >= 1);
  assert(width, 'names usable width (>=50px, not one-char column)', usable,
    m.names.map((n) => `${n.text.split('\n')[0].slice(0, 10)}:${n.width}px`).join(' '));
  assert(width, 'names render in <= 2 text lines (never char-by-char)', twoLines,
    m.names.map((n) => `${n.lines}L`).join(' '));

  // (c) nav reachable + not clipped
  const navReach = m.nav.length >= 5 && m.nav.every((x) => x.inView && x.hittable);
  assert(width, 'every nav destination reachable + in viewport', navReach,
    m.nav.map((x) => `${x.text.slice(0, 6)}${x.inView && x.hittable ? '✓' : '✗'}`).join(' '));
  assert(width, 'nav strip not clipped behind inaccessible overflow', !m.tabsClips);

  // (d) rank/name/club/value visible in first five rows
  const fields = m.rows.length >= 5 && m.rows.every((r) => r.rank && r.name && r.club && r.val);
  assert(width, 'rank+name+club+value visible in first five rows', fields,
    m.rows.map((r) => `[${r.rank ? 'r' : '-'}${r.name ? 'n' : '-'}${r.club ? 'c' : '-'}${r.val ? 'v' : '-'}${r.pill ? 'm' : ' '}]`).join(''));

  // screenshots at 390 + 720 (board + navigation)
  if (width === 390 || width === 720) {
    await page.screenshot({ path: `${OUT}/board_${width}_fixed.png`, fullPage: false });
  }

  // (e) Club-valuation view renders without HALT (+ no document overflow)
  await clickByText(page, '.controls .tabs button, button', 'Clubs');
  await page.waitForTimeout(400);
  const cm = await page.evaluate(CLUB_PROBE);
  assert(width, 'club valuation renders without HALT', !cm.halted && cm.clubRows === 16,
    `halted=${cm.halted} rows=${cm.clubRows}`);
  assert(width, 'club view: scrollWidth <= innerWidth', cm.scrollWidth <= cm.innerWidth,
    `scrollWidth=${cm.scrollWidth} innerWidth=${cm.innerWidth}`);
  if (width === 390) await page.screenshot({ path: `${OUT}/clubs_${width}_fixed.png`, fullPage: false });

  // (f) held-pick view: focus a club onto the board (picks included), renders without HALT
  const opened = await clickByText(page, '.ctable td.club a.copen, a.copen', 'open ›');
  await page.waitForTimeout(400);
  const hp = await page.evaluate(() => ({
    picks: /Σ\s*PICKS|picks included/i.test(document.body.innerText) || document.querySelector('.strip') != null,
    board: document.querySelectorAll('.rows .row').length > 0,
    scrollWidth: document.documentElement.scrollWidth, innerWidth: window.innerWidth,
  }));
  assert(width, 'held-pick view renders (club focused on board)', opened && hp.board && hp.picks);
  assert(width, 'held-pick view: scrollWidth <= innerWidth', hp.scrollWidth <= hp.innerWidth,
    `scrollWidth=${hp.scrollWidth} innerWidth=${hp.innerWidth}`);
  if (width === 390) await page.screenshot({ path: `${OUT}/heldpicks_${width}_fixed.png`, fullPage: false });

  await ctx.close();
}

await browser.close();
fs.writeFileSync(`${OUT}/responsive_assertions.json`, JSON.stringify(results, null, 2));
const byWidth = {};
for (const r of results) { byWidth[r.width] = byWidth[r.width] || { p: 0, f: 0 }; r.ok ? byWidth[r.width].p++ : byWidth[r.width].f++; }
console.log('\n  per-width: ' + WIDTHS.map((w) => `${w}:${byWidth[w].p}/${byWidth[w].p + byWidth[w].f}`).join('  '));
console.log(`  ${results.length - fails}/${results.length} responsive assertions passed`);
process.exit(fails ? 1 : 0);
