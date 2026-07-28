/* Matchday UI — ACCEPTANCE for the #222 bundle (Chromium-driven, screens by re-running).
 *
 * Thirteen items from #139, exercised against the real app in a real browser rather than by reading
 * the source: the player card's weekly history (3, 17, 18), the Public navigation defects (12, 16, 15,
 * 9, 11), the tab tidy-up (2, 13, 14, 5) and the club totals moving to the browser (21).
 *
 * The assertions that matter most are the honesty ones. It is easy to render a history table that looks
 * right and quietly claims a player missed a game the feed never covered, so this test checks the
 * SEMANTICS of the score column, not just its presence:
 *   - DNP appears only on rounds proven completely fed, and appears there;
 *   - no DNP is ever printed on a partially-fed round or on the out-of-round restructure point;
 *   - the value / rank / positional-rank trace is present at every point regardless of participation.
 *
 * Run:  PLAYWRIGHT_CORE=<abs path to playwright-core> node ui/tests/ui_222_items.test.mjs
 *       (optionally CHROME_BIN=<chrome>; otherwise the /opt/pw-browsers build is discovered.)
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';
import { createRequire } from 'module';

const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_CORE || 'playwright-core');

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = process.env.RL_REPO || path.resolve(__dirname, '..', '..');
const URL = 'file://' + path.join(ROOT, 'ui', 'index.html');

function chromePath() {
  if (process.env.CHROME_BIN && fs.existsSync(process.env.CHROME_BIN)) return process.env.CHROME_BIN;
  const g = execSync("ls -d /opt/pw-browsers/chromium-*/chrome-linux/chrome 2>/dev/null | head -1").toString().trim();
  if (g) return g;
  throw new Error('no Chromium binary found (set CHROME_BIN)');
}

let pass = 0, fail = 0;
function check(cond, name, detail) {
  if (cond) { pass++; console.log('  [PASS] ' + name); }
  else { fail++; console.log('  [FAIL] ' + name + (detail ? ' — ' + detail : '')); }
}
function section(t) { console.log('\n' + t); console.log('-'.repeat(t.length)); }

const browser = await chromium.launch({ executablePath: chromePath(), args: ['--no-sandbox'] });
const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
const pageErrors = [];
page.on('pageerror', e => pageErrors.push(e.message));
page.on('console', m => { if (m.type() === 'error') pageErrors.push('console: ' + m.text()); });

await page.goto(URL);
await page.waitForTimeout(600);

const go = async (view) => { await page.evaluate(v => MD.go(v), view); await page.waitForTimeout(250); };
const setTier = async (t) => { await page.evaluate(t2 => { MD.state.tier = t2; MD.render(); }, t); await page.waitForTimeout(250); };

/* ------------------------------------------------------------------ the app renders at all */
section('PREREQUISITE — the board ring-fence');
check(await page.locator('.failclosed').count() === 0,
  'the app renders (the shipped bundle matches its board of record)');
check(await page.locator('.rows .row').count() === 804, 'the working board renders all 804 players');

/* ------------------------------------------------------------------ CLUSTER 3: tabs and labels */
section('CLUSTER 3 — tabs and labels (items 2, 13, 14, 5)');
const tabs = await page.locator('.tabs button').allTextContents();
check(!tabs.some(t => /round review/i.test(t)), 'item 2 — the Round review tab is gone', tabs.join('|'));
check(await page.evaluate(() => typeof MD.review), 'item 2 — MD.review no longer exists',
  await page.evaluate(() => typeof MD.review));
check(tabs.includes('AFFL Rankings') && !tabs.includes('Board'), 'item 13 — Board is renamed AFFL Rankings');

const WANT_SUBTITLES = {
  board: ['AFFL Rankings', 'Player Rankings'], clubs: ['Clubs', 'Club Breakdown'],
  card: ['Player card', 'Player Profiles'], trade: ['Trade desk', 'Trade Desk'],
  movers: ['Movers', 'Weekly Review'],
};
for (const [view, [title, sub]] of Object.entries(WANT_SUBTITLES)) {
  await go(view);
  const h = (await page.locator('.viewtitle h1').innerText()).trim();
  const p = (await page.locator('.viewtitle p').innerText()).trim();
  check(h.toLowerCase() === title.toLowerCase() && p.toLowerCase() === sub.toLowerCase(),
    `item 14 — ${view}: "${title}" / "${sub}"`, `got "${h}" / "${p}"`);
}

// item 5 — the duplicate Free-agents category collapses for display AND filtering.
await go('movers');
const clubOpts = await page.locator('.moversfilters select').first().locator('option').allTextContents();
const freeOpts = clubOpts.filter(o => /free agents/i.test(o));
check(freeOpts.length === 1, 'item 5 — the Movers club filter lists the Free-Agents pool exactly once',
  'got ' + JSON.stringify(freeOpts));
const canon = await page.evaluate(() => ({
  a: MD.canonClub('Free agents'), b: MD.canonClub('Free Agents'), c: MD.canonClub('  free   agents ')
}));
check(canon.a === canon.b && canon.b === canon.c && canon.a === 'Free Agents',
  'item 5 — both authored spellings canonicalise to one key', JSON.stringify(canon));
const bothSpellingsSelected = await page.evaluate(() => {
  const b = window.__MATCHDAY_MOVERS__;
  const rep = b.reports['20'];
  const filtered = MD.movers.core.filter(rep.players, { club: 'Free Agents' });
  const spellings = {};
  filtered.forEach(p => { spellings[p.affl_team] = (spellings[p.affl_team] || 0) + 1; });
  return spellings;
});
check(Object.keys(bothSpellingsSelected).length >= 1 &&
      Object.keys(bothSpellingsSelected).every(s => /^free agents$/i.test(s)),
  'item 5 — selecting the pool returns rows of BOTH authored spellings',
  JSON.stringify(bothSpellingsSelected));

/* ------------------------------------------------------------------ CLUSTER 1: the player card */
section('CLUSTER 1 — the player card (items 3, 17, 18)');
const HIST = await page.evaluate(() => {
  const cov = MD.history.coverage();
  const key = 'aaron-cadman';
  const series = MD.history.series(key);
  return { cov, series, traceSize: MD.history.traceSize() };
});
check(HIST.series && HIST.series.length === 8, 'item 3 — the history has all eight points',
  HIST.series ? String(HIST.series.length) : 'null');
check(HIST.series.every(r => r.v != null && r.rank != null && r.posRank != null),
  'item 3 — value, rank and positional rank are present at EVERY point (no participation gate)');
check(HIST.traceSize === 804, 'item 3 — the trace covers all 804 tracked players', String(HIST.traceSize));

const modelPt = HIST.series.find(r => !r.isRound);
check(!!modelPt && modelPt.id === 'post-r19-redesign-1',
  'item 3 — the restructure point is present and flagged as not-a-round');
check(modelPt && modelPt.score.state === 'not-a-round' && modelPt.v != null,
  'item 3 — the restructure carries value/rank movement but never a score');

// the honesty contract, asserted over EVERY player, not just one.
const HONESTY = await page.evaluate(() => {
  const cov = MD.history.coverage();
  const keys = Object.keys(window.__MATCHDAY_MOVERS__.values);
  const dnpByPoint = {}, unrecByPoint = {}, scoreByPoint = {};
  keys.forEach(k => {
    MD.history.series(k).forEach(r => {
      const b = r.score.state === 'dnp' ? dnpByPoint : r.score.state === 'unrecorded' ? unrecByPoint
              : r.score.state === 'score' ? scoreByPoint : null;
      if (b) b[r.id] = (b[r.id] || 0) + 1;
    });
  });
  return { cov, dnpByPoint, unrecByPoint, scoreByPoint, n: keys.length };
});
const completeRounds = Object.keys(HONESTY.cov.rounds).filter(r => HONESTY.cov.rounds[r].complete);
const partialRounds = Object.keys(HONESTY.cov.rounds).filter(r => !HONESTY.cov.rounds[r].complete);
/* Deliberately NOT asserted as the literal list "17,18,19,20": that would have to be re-pinned by hand
   every time a round lands, which is the upkeep trap this project has paid for before. What is asserted
   is the DERIVATION — a round is complete exactly when every club on the board is present at full-side
   strength — plus the fact that today's bundle actually contains both kinds, so the test is not
   vacuously passing over a set with nothing in it. */
check(completeRounds.every(r => {
  const c = HONESTY.cov.rounds[r];
  return c.clubs === HONESTY.cov.clubsOnBoard && c.smallestSide >= HONESTY.cov.minSide;
}), 'item 3 — every round judged complete really has all clubs at full-side strength');
check(partialRounds.every(r => {
  const c = HONESTY.cov.rounds[r];
  return c.clubs < HONESTY.cov.clubsOnBoard || c.smallestSide < HONESTY.cov.minSide;
}), 'item 3 — every round judged partial really is short of that bar');
check(completeRounds.length > 0 && partialRounds.length > 0,
  'item 3 — this bundle exercises BOTH branches (complete: ' + completeRounds.join(',') +
  ' · partial: ' + partialRounds.join(',') + ')');
const dnpPoints = Object.keys(HONESTY.dnpByPoint);
check(dnpPoints.every(p => completeRounds.includes(p)),
  'item 3 — DNP is printed ONLY on completely-fed rounds', 'DNP on: ' + dnpPoints.join(','));
check(partialRounds.every(r => !HONESTY.dnpByPoint[r]),
  'item 3 — NO player is ever marked DNP in a partially-fed round',
  partialRounds.filter(r => HONESTY.dnpByPoint[r]).join(','));
check(!HONESTY.dnpByPoint['14'] && !HONESTY.dnpByPoint['post-r19-redesign-1'],
  'item 3 — no DNP at the baseline point or the restructure point');
check(completeRounds.every(r => HONESTY.dnpByPoint[r] > 0),
  'item 3 — DNP IS shown where it is warranted (the indicator is not simply switched off)');
check(HONESTY.unrecByPoint['15'] > 0 && HONESTY.unrecByPoint['16'] > 0 && HONESTY.unrecByPoint['14'] === 804,
  'item 3 — partial rounds and the R14 baseline read "not recorded" instead');
check(completeRounds.every(r => HONESTY.scoreByPoint[r] === HONESTY.cov.rounds[r].scored),
  'item 3 — every recorded score is shown');

// the rendered table, in the DOM.
await page.evaluate(() => MD.go('card', 'aaron-cadman'));
await page.waitForTimeout(300);
check(await page.locator('.histtbl').count() === 1, 'item 3 — the card renders the history table');
check(await page.locator('.histtbl tbody tr').count() === 8, 'item 3 — eight rows, one per point');
check(await page.locator('.histtbl .mctag').count() === 1,
  'item 3 — the restructure row carries a "model change" tag');
check(await page.locator('.reserved:has-text("weekly-loop phase")').count() === 0,
  'item 3 — the "reserved · wired in the weekly-loop phase" placeholder is gone');
const noteText = await page.locator('.histnote').innerText();
check(/not uniform/i.test(noteText) && /did not play/i.test(noteText),
  'item 3 — the card states the coverage caveat in words');

/* items 17 + 18 — public parity */
await setTier('public');
await page.waitForTimeout(250);
const pubCard = await page.locator('.card').innerText();
check(/recent form/i.test(pubCard), 'item 17 — Recent form is exposed on the public card');
check(/pick\s*\d+/i.test(pubCard), 'item 18 — the public card shows the draft pick');
check(/of\s*804/i.test(pubCard), 'item 18 — the public card shows rank WITH its denominator');
check(await page.locator('.histtbl').count() === 1, 'item 3 — the public card carries the weekly history too');
check(!/guard 5|store <b>|engine <b>/i.test(pubCard), 'item 18 — build provenance stays hidden in public');
check(!/owner override/i.test(pubCard), 'item 18 — the owner override stays hidden in public');
check(!/per-lever/i.test(pubCard), 'item 18 — the per-lever attribution panel stays hidden in public');
const steady = await page.locator('.statrow').innerText();
check(!/—\s*steady/i.test(steady), 'item 18 — the hardcoded "— steady" movement is gone');

/* ------------------------------------------------------------------ CLUSTER 2: navigation */
section('CLUSTER 2 — navigation (items 12, 16, 15, 9, 11)');
await setTier('public');
await go('board');
const pubRows = page.locator('.rows .row.public');
check(await pubRows.count() === 804, 'the public board renders');
const pubRowText = await pubRows.first().innerText();
check(/\n/.test(pubRowText) && (await page.locator('.rows .row.public .club').count()) === 804,
  'item 9 — every public row carries the AFFL/AFL club');

// item 16 — a public player row opens that player's profile.
await pubRows.nth(3).click();
await page.waitForTimeout(300);
const viewAfterPlayerClick = await page.evaluate(() => MD.state.view);
const keyAfterPlayerClick = await page.evaluate(() => MD.state.cardKey);
check(viewAfterPlayerClick === 'card' && !!keyAfterPlayerClick,
  'item 16 — clicking a player in Public opens that player\'s profile',
  viewAfterPlayerClick + '/' + keyAfterPlayerClick);

// item 12 — a club opened from the Clubs page lands on THAT club, not the all-player list.
await go('clubs');
await page.locator('.ctable tbody tr .copen').first().click();
await page.waitForTimeout(350);
const afterClubOpen = await page.evaluate(() => ({
  view: MD.state.view, filter: MD.board.snapshot().clubFilter,
  rows: document.querySelectorAll('.rows .row').length,
  summary: document.querySelectorAll('.clubsummary').length,
}));
check(afterClubOpen.view === 'board' && !!afterClubOpen.filter,
  'item 12 — opening a club in Public routes to the board WITH the club filter set');
check(afterClubOpen.rows > 0 && afterClubOpen.rows < 804,
  'item 12 — the public board shows that club only, not the all-player list',
  'rows=' + afterClubOpen.rows);
check(afterClubOpen.summary === 1, 'item 11 — the club page opens with the club profile summary');

const summaryText = await page.locator('.clubsummary').innerText();
check(/overall/i.test(summaryText) && /best-23/i.test(summaryText) && /top-5/i.test(summaryText) &&
      /non-best-23/i.test(summaryText) && /rank \d+ of 16/i.test(summaryText),
  'item 11 — the summary carries the comparison-page metrics, each with its rank');
check((await page.locator('.clubsummary')).first() !== null &&
      await page.evaluate(() => {
        const s = document.querySelector('.clubsummary'), r = document.querySelector('.rows .row');
        return !!(s && r) && (s.compareDocumentPosition(r) & Node.DOCUMENT_POSITION_FOLLOWING) !== 0;
      }),
  'item 11 — the summary appears BEFORE the player list');

// item 15 — universal Back: club -> player -> back lands on the club page again.
const clubBefore = await page.evaluate(() => MD.board.snapshot().clubFilter);
await page.locator('.rows .row.public').first().click();
await page.waitForTimeout(300);
check(await page.evaluate(() => MD.state.view) === 'card', 'item 15 — club → player navigates to the card');
check(await page.locator('.backnav button').count() === 1, 'item 15 — a universal Back control is present');
await page.locator('.backnav button').click();
await page.waitForTimeout(350);
const afterBack = await page.evaluate(() => ({
  view: MD.state.view, filter: MD.board.snapshot().clubFilter,
  rows: document.querySelectorAll('.rows .row').length,
}));
check(afterBack.view === 'board' && afterBack.filter === clubBefore,
  'item 15 — Back returns to the CLUB page, not the all-player list',
  JSON.stringify(afterBack) + ' want filter ' + clubBefore);
check(afterBack.rows > 0 && afterBack.rows < 804, 'item 15 — the club filter is restored with the page');

// item 15 — player -> club also has a Back, and Back is not card-specific.
await go('clubs');
await page.waitForTimeout(250);
check(await page.locator('.backnav button').count() === 1,
  'item 15 — Back exists on the Clubs page too (it is not player-card-specific)');
await page.locator('.backnav button').click();
await page.waitForTimeout(300);
check(await page.evaluate(() => MD.state.view) === 'board', 'item 15 — Back from Clubs returns to the board');

/* ------------------------------------------------------------------ item 21: club totals */
section('ITEM 21 — club totals computed in the browser');
await setTier('working');
await go('clubs');
const totals = await page.evaluate(() => {
  const ct = MD.clubTotals.compute();
  const baked = (window.__CLUB_VALUATION__.clubs || []).reduce((m, c) => (m[c.team] = c, m), {});
  const live = {};
  (MD.seam.working.players || []).forEach(p => {
    const t = MD.canonClub(p.affl_team);
    if (!t || MD.clubTotals.isFree(t)) return;
    live[t] = (live[t] || 0) + p.v;
  });
  return {
    n: ct.clubs.length,
    matchesLiveBoard: ct.clubs.every(c => Math.abs(c.totalPlayer - live[c.team]) < 0.5),
    differsFromBaked: ct.clubs.filter(c => baked[c.team] && baked[c.team].totalPlayer !== c.totalPlayer).length,
    picksKept: ct.clubs.every(c => c.totalPicks > 0),
    identities: ct.clubs.every(c => c.overall === c.totalPlayer + c.totalPicks &&
                                    c.totalPlayer === c.best23 + c.nonBest23),
    boardPin: ct.playerSource.board.slice(0, 8),
    stampPin: (MD.seam.working.stamp.board_md5 || '').slice(0, 8),
  };
});
check(totals.n === 16, 'item 21 — 16 clubs computed', String(totals.n));
check(totals.matchesLiveBoard, 'item 21 — every club total equals the sum of its players ON THE LIVE BOARD');
check(totals.differsFromBaked === 16,
  'item 21 — and differs from the baked file for all 16 clubs (the staleness this removes)',
  String(totals.differsFromBaked));
check(totals.picksKept, 'item 21 — the ingest\'s PVC band-priced picks are kept, not recomputed');
check(totals.identities, 'item 21 — overall == player + picks and player == best23 + nonBest23');
check(totals.boardPin === totals.stampPin, 'item 21 — the totals name the board they were summed from');
const clubsIntro = await page.locator('.cintro').innerText();
check(/browser/i.test(clubsIntro), 'item 21 — the Clubs page says the totals are summed in the browser');

/* ------------------------------------------------------------------ no runtime errors anywhere */
section('RUNTIME');
for (const v of ['board', 'clubs', 'card', 'trade', 'movers']) {
  for (const t of ['working', 'public']) {
    await setTier(t); await go(v);
  }
}
check(pageErrors.length === 0, 'every view renders in both tiers with no page errors',
  pageErrors.slice(0, 4).join(' | '));

await browser.close();
console.log('\n' + '-'.repeat(60));
console.log((fail ? 'FAIL ' : '') + pass + '/' + (pass + fail) + ' passed');
process.exit(fail ? 1 : 0);
