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

/* RESTATED 2026-08-28 (owner redesign): the app ships ONE fully transparent tier — the public
   renderer and the tier toggle are retired, so `setTier` went with them. Item substance that
   survives (form, pick, rank denominator, navigation, totals) is asserted against THE app. */
const go = async (view) => { await page.evaluate(v => MD.go(v), view); await page.waitForTimeout(250); };

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
/* RESTATED 2026-08-28: since #283 the club filter matches each player's LIVE club (the ownership
   store is the single source of ownership), not the report row's stored affl_team — a row's stored
   spelling can be any club the player has since left. What remains item 5's to assert: the
   selection is exactly the live-store Free-Agents pool, canonicalised, and non-empty. */
const poolSel = await page.evaluate(() => {
  const rep = window.__MATCHDAY_MOVERS__.reports['20'];
  const live = (p) => (MD.ownership ? MD.ownership.clubOf(p) : (p ? p.affl_team : null));
  const want = rep.players.filter(p => (MD.canonClub(live(p)) || '—') === 'Free Agents');
  const got = MD.movers.core.filter(rep.players, { club: 'Free Agents' });
  return { n: got.length, wantN: want.length };
});
check(poolSel.n > 0 && poolSel.n === poolSel.wantN,
  'item 5 — selecting the pool returns exactly the live-store Free-Agents rows',
  JSON.stringify(poolSel));

/* ------------------------------------------------------------------ CLUSTER 1: the player card */
section('CLUSTER 1 — the player card (items 3, 17, 18)');

/* TWO UNIVERSES, AND THIS CLUSTER IS ABOUT THE RECORD (owner ruling 2026-08-31). The card now
   DEFAULTS to the current-model universe — the retrospective series plus everything since the last
   model change — because the owner asked for "the player's progression over the rounds since 14
   under the live model". Every assertion below is about the ALL-IN universe: the stored record as
   the app served it, model changes and all. So the mode is set explicitly rather than assumed, which
   is the honest form either way — a test that silently depended on the default was going to break
   the first time the default moved, and did.
   The DEFAULT is asserted straight after this block, so neither universe is left unexercised. */
const DEFAULT_UNIVERSE = await page.evaluate(() => MD.universe.mode());
const DEFAULT_SERIES = await page.evaluate(() => MD.history.series('aaron-cadman').map(r => String(r.id)));
await page.evaluate(() => MD.universe.setMode(MD.universe.ALL));

const HIST = await page.evaluate(() => {
  const cov = MD.history.coverage();
  const key = 'aaron-cadman';
  const series = MD.history.series(key);
  return { cov, series, traceSize: MD.history.traceSize() };
});
/* RESTATED at #274 item 1. This read `=== 8` and was written when the R19 restructure was the only
   out-of-round column. The 30/7 rederivation adoption added a ninth point, so the literal was stale the
   moment adoption landed — it did not surface until #274 cleared the movers red that was SHADOWING
   Final Integration steps 14-22. Measured at HEAD before the fix: the identical three failures, so this
   is adoption-created and inherited, not caused by the era-succession work.
   The literal stays a literal ON PURPOSE — it is the drift sentinel that made adoption's new column
   visible at all. It moves by one every time a landed change adds a column, and that edit is the
   point. */
/* Sentinel RE-PINNED 2026-08-29: the ORDER 49 landing added its model-change column (MC-15,
   order49-avail-blend-28-8), 25 → 26. The literal stays a literal — it is the drift sentinel,
   and it moves by hand every time a landed change adds a column. */
// A HARD-PINNED COUNT, and it moves whenever an out-of-round act lands — it was 26 until the
// 30/8 store correction added its column. That is what this pin is FOR: a point count that changed
// without anyone noticing would mean the card had silently gained or lost an event. Restate it in
// the same commit as the act that moved it, and never to make a red go away.
// RESTATED 2026-08-31: FINALS WEEK 1 landed (fw1-finals-week-1-30-8), 27 -> 28. The sentinel did
// its job and caught it — late, because the FW1 act should have restated it in its own commit and
// did not. The count moving for a landed act is the sentinel working; it moving unexplained is the
// thing it exists to catch.
// RESTATED 2026-09-01: THE BUST EXCLUSION landed (bust-exclusion-live-fit-1-9), 28 -> 29 — McCartin
// and Boyd struck from the live pick-value fit, board c8c2f2b6 -> b005096b. Caught late again, and
// for the same reason: the act's own commit did not restate it, because the landing's gate set does
// not run this file. That is the gap, not the count.
check(HIST.series && HIST.series.length === 29, 'item 3 — the history has all 29 points',
  HIST.series ? String(HIST.series.length) : 'null');
check(HIST.series.every(r => r.v != null && r.rank != null && r.posRank != null),
  'item 3 — value, rank and positional rank are present at EVERY point (no participation gate)');
check(HIST.traceSize === 804, 'item 3 — the trace covers all 804 tracked players', String(HIST.traceSize));

const modelPts = HIST.series.filter(r => !r.isRound);
const modelPt = modelPts[0];
check(!!modelPt && modelPt.id === 'post-r19-redesign-1',
  'item 3 — the restructure point is present and flagged as not-a-round');
check(modelPt && modelPt.score.state === 'not-a-round' && modelPt.v != null,
  'item 3 — the restructure carries value/rank movement but never a score');
/* #274 item 1 — the adoption column is a point in its own right, and it must behave like one rather
   than merely be tolerated by a loosened count. Named explicitly so a missing or mislabelled column
   fails here instead of passing as "some non-round point". */
/* RESTATED 2026-08-28: fourteen model changes have landed, so the two-name literal became a
   derivation — the out-of-round columns must be EXACTLY the bundle's model_changes, in order.
   (The bundle list is the same one the card's MC-N ids index; see ui/MAINTAINER.md.) */
/* AMENDED 2026-08-31: the derivation read `model_changes` as the list of out-of-round columns,
   because until FW1 those were the same set — every board move outside a round was a model change.
   A finals week is a board move outside a round that changes NO model, so it is a column and is
   deliberately not a model change (round_movers.football_column). The card must still show EVERY
   non-round point in bundle order; the expectation is now derived from the bundle's own points,
   which is the set the card renders, rather than from a list that no longer means the same thing. */
const wantOorIds = await page.evaluate(() =>
  ((window.__MATCHDAY_MOVERS__.points || []).filter(p => p.kind === "out_of_round")).map(p => String(p.id)));
check(modelPts.map(r => String(r.id)).join(',') === wantOorIds.join(',') && wantOorIds.length >= 2,
  'item 3 — every out-of-round column is present, in bundle order, flagged not-a-round',
  modelPts.map(r => r.id).join(',') + ' vs ' + wantOorIds.join(','));
check(modelPts.every(r => r.score.state === 'not-a-round' && r.v != null),
  'item 3 — every out-of-round column carries value/rank movement but never a score');

// the honesty contract, asserted over EVERY player, not just one.
const HONESTY = await page.evaluate(() => {
  const cov = MD.history.coverage();
  const keys = Object.keys(window.__MATCHDAY_MOVERS__.values);
  const dnpByPoint = {}, unrecByPoint = {}, scoreByPoint = {};
  keys.forEach(k => {
    MD.history.series(k).forEach(r => {
      const b = r.score.state === 'dnp' ? dnpByPoint : r.score.state === 'unrecorded' ? unrecByPoint
              : r.score.state === 'score' ? scoreByPoint : null;
      /* KEYED ON THE ROUND, NOT THE POINT ID (2026-08-31). A retro point is round N's football
         re-priced, so its coverage, its DNP truth and its score all belong to round N — its own id
         is "retro-r21" and coverage is keyed "21". Joining on the point id would report DNP against
         a round it cannot find and call a correct card wrong. `roundKey` is what history.js itself
         joins on, so the test asks the same question the view does. */
      const rk = r.roundKey || (String(r.id).indexOf("retro-r") === 0 ? String(r.id).slice(7) : String(r.id));
      if (b) b[rk] = (b[rk] || 0) + 1;
    });
  });
  return { cov, dnpByPoint, unrecByPoint, scoreByPoint, n: keys.length };
});
/* THE DEFAULT, asserted on its own terms: one model throughout, no model change inside it, and it
   reaches from R14 to the newest stored point — which is the whole of what the owner asked for. */
const MC_IDS = await page.evaluate(() =>
  ((window.__MATCHDAY_MOVERS__.model_changes) || []).map(c => String(c.between[1])));
check(DEFAULT_UNIVERSE === 'current', 'item 3 — the card DEFAULTS to the current-model universe',
  DEFAULT_UNIVERSE);
check(DEFAULT_SERIES.length > 0 && DEFAULT_SERIES.every(id => !MC_IDS.includes(id)),
  'item 3 — the default series contains NO model change',
  DEFAULT_SERIES.filter(id => MC_IDS.includes(id)).join(',') || 'none');
check(DEFAULT_SERIES[0] === 'retro-r14',
  'item 3 — the default series starts at R14 under the current model', DEFAULT_SERIES[0]);
check(DEFAULT_SERIES.length < HIST.series.length,
  'item 3 — the default is a STRICT subset of the all-in record (' + DEFAULT_SERIES.length +
  ' vs ' + HIST.series.length + ') — the switch is not vacuous');

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
/* RESTATED 2026-08-28: one line per event (owner word) — the row count equals the series, model
   rows carry the bare "Model change (MC-N)" id, and the coverage-caveat essay (.histnote) is
   retired to ui/MAINTAINER.md. */
check(await page.locator('.histtbl tbody tr').count() === HIST.series.length,
  'item 3 — one row per point, no more and no fewer');
/* AMENDED 2026-08-31, on the owner's word ("FW1 doesn't even appear in the movers list?"). Every
   non-round row used to be "Model change (MC-N)". A finals week now carries its own name, so the
   MC-N chips cover the MODEL-CHANGE rows only and the football rows are asserted separately —
   NOT loosened: both halves must account for every non-round row, so a row that is neither still
   fails, and a model change that lost its id still fails. */
const mcidTexts = await page.locator('.histtbl .mcid').allTextContents();
const finalsTexts = await page.locator('.histtbl .finalsev').allTextContents();
const nFootball = await page.evaluate(() =>
  ((window.__MATCHDAY_MOVERS__.points || [])
    .filter(p => p.kind === "out_of_round" &&
                 ["fw1-", "fw2-", "sf-", "pf-", "gf-"].some(k => String(p.id).indexOf(k) === 0))).length);
check(mcidTexts.length + finalsTexts.length === modelPts.length
      && mcidTexts.length === modelPts.length - nFootball
      && mcidTexts.every(t => /^\(MC-\d+\)$/.test(t.trim()))
      && finalsTexts.length === nFootball
      && finalsTexts.every(t => /Final|Finals Week/.test(t.trim())),
  'item 3 — every model-change row is ONE line "Model change (MC-N)", every football row is its week name, and together they account for every non-round row',
  JSON.stringify(mcidTexts.slice(0, 4)));
check(await page.locator('.reserved:has-text("weekly-loop phase")').count() === 0,
  'item 3 — the "reserved · wired in the weekly-loop phase" placeholder is gone');
check(await page.locator('.histnote').count() === 0,
  'item 3 — the coverage-caveat essay is off the card (maintainer doc, not screen furniture)');

/* items 17 + 18 — the substance survives on THE card (one transparent tier) */
const cardText = await page.locator('.card').innerText();
/* AMENDED 2026-08-31 ON THE OWNER'S WORD (item 3 of his UI list): "recent form" comes OFF the card
   and a weekly value graph since R14 goes on, x and y axes labelled. The old assertion here was
   `/recent form/i` — it encoded the section he has now retired, so it is replaced by the assertion
   the new requirement earns, NOT deleted and not weakened:
     · the retired section must actually be gone (a rename that left both would pass a mere
       "graph exists" check),
     · the graph must draw a real line with one point per point in the series — not an empty frame,
     · BOTH axis titles must render, because "labelled axes" was half of what he asked for.
   The season scores the old line drew are not lost: they remain per-round in the history table's
   Score column, where each carries its own played / DNP / not-recorded truth. */
check(!/recent form/i.test(cardText), 'item 3 (2026-08-31) — the "Recent form" season-score line is retired from the card');
check(/weekly value/i.test(cardText) && await page.locator('.wchart svg .wcl').count() === 1,
  'item 3 (2026-08-31) — the weekly value graph replaces it and draws a line');
const wcPts = await page.evaluate(() => {
  const poly = document.querySelector('.wchart .wcl');
  return poly ? poly.getAttribute('points').trim().split(/\s+/).length : 0;
});
const wcSeries = await page.evaluate(() =>
  (MD.history.series(MD.state.cardKey) || []).filter(r => r.v != null).length);
check(wcPts === wcSeries && wcPts >= 2,
  'item 3 (2026-08-31) — the line carries one vertex per point in MD.history.series, no more and no fewer',
  wcPts + ' vs ' + wcSeries);
const axisTitles = (await page.locator('.wchart .wcat').allTextContents()).map(t => t.trim()).sort();
check(JSON.stringify(axisTitles) === JSON.stringify(['ROUND', 'VALUE']),
  'item 3 (2026-08-31) — both axes are labelled (his ask), not just ticked',
  JSON.stringify(axisTitles));
check(/pick\s*\d+/i.test(cardText), 'item 18 — the card shows the draft pick');
check(/\/\s*804/.test(cardText), 'item 18 — the card shows rank WITH its denominator');
check(!/guard 5|board <b>|engine <b>/i.test(cardText), 'item 18 — no build provenance on the card');
check(!/per-lever|why the price/i.test(cardText), 'item 18 — no attribution panel on the card');
const steady = await page.locator('.statrow').first().innerText();
check(!/—\s*steady/i.test(steady), 'item 18 — the hardcoded "— steady" movement is gone');

/* ---------------------------------------------------- OWNER ITEM 11 (2026-08-31): "vs Pick 1"
   His word: the "vs top" bar becomes "vs Pick 1", carrying a ratio to two decimals rendered ON the
   bar and legible against it. Four things are worth asserting and one is worth NOT asserting:
     · the column is renamed (a ratio under a heading that still says "vs top" is a contradiction);
     · every board row carries a ratio, and each is exactly 2dp — the format IS the requirement;
     · the ratio is the row's value over PICK 1 off the loaded board's own curve, checked against
       the bundle rather than against 3000, so a re-anchored curve moves the expectation with it;
     · the label flips to the inside of the fill on long bars, which is what keeps it readable
       against the bright warm end instead of vanishing into it.
   NOT asserted: that the fill is anchored to pick 1. It deliberately is not — it stays on the
   0..top-of-board track so the column still ranks the page, and the dashed tick is what ties the
   two readings together. */
section('OWNER ITEM 11 (2026-08-31) — the value line reads vs Pick 1');
await go('board');
check((await page.locator('.rowhead.working .h').allTextContents()).some(t => /vs pick 1/i.test(t)),
  'item 11 — the column heading is "vs Pick 1", not "vs top"');
const p1 = await page.evaluate(() => MD.pick1());
check(typeof p1 === 'number' && p1 > 0,
  'item 11 — pick 1 is READ off the loaded board curve (pvc), not hardcoded', String(p1));
const ratioCheck = await page.evaluate(() => {
  const rows = [...document.querySelectorAll('.rows .row.working')];
  const out = { n: 0, bad2dp: 0, wrong: 0, inside: 0, outside: 0, ticks: 0, floored: 0 };
  const p1 = MD.pick1();
  rows.forEach(r => {
    const lab = r.querySelector('.vline .vratio');
    if (!lab) return;
    out.n++;
    const txt = lab.textContent.trim();
    /* "<0.01x" is the floor form: at the foot of the board a single-digit value against a pick 1 in
       the thousands rounds to 0.00, and printing that would say a player is worth nothing. Both
       forms are accepted HERE, and the two are pinned to their own cases just below, so accepting
       the floor cannot be used to smuggle a wrong number through. */
    if (!/^(\d+\.\d{2}|<0\.01)\u00d7$/.test(txt)) out.bad2dp++;
    const val = Number(r.querySelector('.val').textContent.replace(/[^0-9.-]/g, ''));
    const rr = val / p1;
    const want = (rr > 0 && rr < 0.005) ? '<0.01' : rr.toFixed(2);
    if (txt.replace('\u00d7', '') !== want) out.wrong++;
    if (txt.indexOf('<') === 0) out.floored++;
    if (lab.classList.contains('in')) out.inside++; else out.outside++;
    if (r.querySelector('.vline .vp1')) out.ticks++;
  });
  return out;
});
check(ratioCheck.n === 804 && ratioCheck.bad2dp === 0,
  'item 11 — every board row carries a ratio, and every one of them is to two decimals',
  JSON.stringify(ratioCheck));
check(ratioCheck.wrong === 0,
  'item 11 — each ratio is that row\'s own value divided by pick 1 off the curve', JSON.stringify(ratioCheck));
check(ratioCheck.inside > 0 && ratioCheck.outside > 0,
  'item 11 — the label sits inside the fill on long bars and outside it on short ones, so it is legible on both',
  JSON.stringify(ratioCheck));
check(ratioCheck.ticks === 804,
  'item 11 — the pick-1 tick is drawn on every bar, which is what makes "past the line = worth more than pick 1" readable',
  String(ratioCheck.ticks));
/* The floor is asserted to be IN USE, not merely tolerated. It was found on the rendered page: the
   foot of the board printed a column of "0.00x" against players who are not worth zero. If a future
   change removes the floor this goes red rather than silently restoring the false reading. */
check(ratioCheck.floored > 0 && (await page.evaluate(() =>
  [...document.querySelectorAll('.rows .row.working .vline .vratio')]
    .filter(l => l.textContent.trim() === '0.00\u00d7').length)) === 0,
  'item 11 — a ratio too small for two decimals reads "<0.01x", and NO row prints the false "0.00x"',
  ratioCheck.floored + ' floored');

/* ------------------------------------------------- OWNER ITEM 10 (2026-08-31): the figure face
   "Something that looks a little cleaner and less mechanical" on the value rating numbers. He was
   shown two and chose the system sans. The thing worth pinning is not which family name won — that
   is taste and he can change it — but the PROPERTY the change had to preserve to be allowed at all:
   monospace was carrying the column alignment, and dropping it without tabular figures would have
   left every column of numbers ragged. So the assertions are: the figures are no longer monospaced,
   they ask for tabular lining figures, and two values with the same digit count actually MEASURE the
   same width on the rendered page — which is the alignment itself, not a proxy for it. */
section('OWNER ITEM 10 (2026-08-31) — the value figures are set in the figure face, still tabular');
await go('board');
const figFace = await page.evaluate(() => {
  const el = document.querySelector('.rows .row.working .val');
  const cs = getComputedStyle(el);
  return { family: cs.fontFamily, variant: cs.fontVariantNumeric };
});
check(!/mono/i.test(figFace.family),
  'item 10 — the board value is no longer set in the monospace stack', figFace.family);
check(/tabular-nums/.test(figFace.variant),
  'item 10 — it asks for tabular figures, which is what kept the column aligned without the monospace',
  figFace.variant);
const widths = await page.evaluate(() => {
  const by = {};
  [...document.querySelectorAll('.rows .row.working .val')].forEach(el => {
    const d = el.textContent.replace(/[^0-9]/g, '').length;
    (by[d] = by[d] || []).push(Math.round(el.getBoundingClientRect().width * 100) / 100);
  });
  // the widest digit-count bucket that has more than one member is the one worth measuring
  const k = Object.keys(by).filter(k => by[k].length > 1).sort((a, b) => by[b].length - by[a].length)[0];
  return { digits: k, n: by[k].length, distinct: [...new Set(by[k])].length };
});
check(widths.distinct === 1 && widths.n > 50,
  'item 10 — every value with the same digit count renders at the SAME width, so the column is still a column',
  JSON.stringify(widths));
/* And the separation the token exists for: an IDENTIFIER is still monospaced. If a later sweep
   swapped --mono wholesale this goes red, which is the point — the change was to the figures. */
const idFace = await page.evaluate(() =>
  getComputedStyle(document.querySelector('.rows .row.working .club .afl')).fontFamily);
check(/mono/i.test(idFace),
  'item 10 — identifiers (the AFL club line) keep the monospace: the swap was scoped to values, not to everything',
  idFace);

/* ------------------------------------------------------------------ CLUSTER 2: navigation */
section('CLUSTER 2 — navigation (items 12, 16, 15, 9, 11)');
await go('board');
const bRows = page.locator('.rows .row.working');
check(await bRows.count() === 804, 'the board renders all rows');
const bRowText = await bRows.first().innerText();
check(/\n/.test(bRowText) && (await page.locator('.rows .row.working .club').count()) === 804,
  'item 9 — every row carries the AFFL/AFL club');

// item 16 — a player row opens that player's profile.
await bRows.nth(3).click();
await page.waitForTimeout(300);
const viewAfterPlayerClick = await page.evaluate(() => MD.state.view);
const keyAfterPlayerClick = await page.evaluate(() => MD.state.cardKey);
check(viewAfterPlayerClick === 'card' && !!keyAfterPlayerClick,
  'item 16 — clicking a player opens that player\'s profile',
  viewAfterPlayerClick + '/' + keyAfterPlayerClick);

// item 12 — a club opened from the Clubs page lands on THAT club, not the all-player list.
await go('clubs');
await page.locator('.ctable tbody tr .copen').first().click();
await page.waitForTimeout(350);
const afterClubOpen = await page.evaluate(() => ({
  view: MD.state.view, filter: MD.board.snapshot().clubFilter,
  rows: document.querySelectorAll('.rows .row').length,
  summary: document.querySelectorAll('.clubsummary').length,
  picksPanel: document.querySelectorAll('.pickspanel').length,
}));
check(afterClubOpen.view === 'board' && !!afterClubOpen.filter,
  'item 12 — opening a club routes to the board WITH the club filter set');
check(afterClubOpen.rows > 0 && afterClubOpen.rows < 804,
  'item 12 — the board shows that club only, not the all-player list',
  'rows=' + afterClubOpen.rows);
check(afterClubOpen.picksPanel === 1,
  'owner fix 2026-08-28 — a focused club shows its PICKS at the bottom of its board');
check(afterClubOpen.summary === 1, 'item 11 — the club page opens with the club profile summary');

/* RESTATED 2026-08-28: the metric labels are the owner's — "Rating" (the 56-asset club rating)
   and "Depth" (was Non-Best-23) — and ranks read plain "rank N". */
const summaryText = await page.locator('.clubsummary').innerText();
check(/rating/i.test(summaryText) && /best-23/i.test(summaryText) && /top-5/i.test(summaryText) &&
      /depth/i.test(summaryText) && /rank \d+/i.test(summaryText),
  'item 11 — the summary carries the comparison-page metrics, each with its rank');
check((await page.locator('.clubsummary')).first() !== null &&
      await page.evaluate(() => {
        const s = document.querySelector('.clubsummary'), r = document.querySelector('.rows .row');
        return !!(s && r) && (s.compareDocumentPosition(r) & Node.DOCUMENT_POSITION_FOLLOWING) !== 0;
      }),
  'item 11 — the summary appears BEFORE the player list');

// item 15 — universal Back: club -> player -> back lands on the club page again.
const clubBefore = await page.evaluate(() => MD.board.snapshot().clubFilter);
await page.locator('.rows .row.working').first().click();
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
  /* INDEPENDENCE FROM THE BAKED BLOCK, proven by perturbation rather than by staleness.
     This used to assert `differsFromBaked === 16` — i.e. that the baked totals were WRONG for every
     club, which was true only because ui/data/club_valuation.js had not been regenerated since before
     the adoption. That made the check a hostage to a stale file: #283 regenerates the bundle as part of
     making the store the single source of ownership, the baked totals became correct, and the
     assertion inverted through no change in the behaviour it was meant to guard. A test that passes
     only while something else is broken is not guarding anything.
     The property actually wanted is INDEPENDENCE: the browser computes the player side from the board
     and never reads the baked block. So corrupt every baked total in place and recompute — the answer
     must not move. (club_totals_parity.test.js proves the same property head-on; this is its in-page
     counterpart, and it stays true whether the bundle is fresh or stale.) */
  const beforePerturb = ct.clubs.map(c => c.totalPlayer);
  (window.__CLUB_VALUATION__.clubs || []).forEach(c => { c.totalPlayer = -999999; c.overall = -999999; });
  const afterPerturb = MD.clubTotals.compute().clubs.map(c => c.totalPlayer);
  return {
    n: ct.clubs.length,
    matchesLiveBoard: ct.clubs.every(c => Math.abs(c.totalPlayer - live[c.team]) < 0.5),
    independentOfBaked: beforePerturb.length === afterPerturb.length
      && beforePerturb.every((v, i) => v === afterPerturb[i]),
    bakedWasReadable: Object.keys(baked).length === 16,
    picksKept: ct.clubs.every(c => c.totalPicks > 0),
    /* RESTATED 2026-08-28: `overall` is now the owner's 56-asset rating, so the conservation
       identity is rating == (players − material excluded) + (picks − material cut) + phantom. */
    identities: ct.clubs.every(c => {
      const f = c.rating56 || {};
      const conserve = (c.totalPlayer - f.materialExcludedPlayers)
        + (c.totalPicks - f.materialExcludedPicks) + f.phantomAdded;
      return Math.abs(c.overall - conserve) < 0.5 && c.totalPlayer === c.best23 + c.nonBest23;
    }),
    boardPin: ct.playerSource.board.slice(0, 8),
    stampPin: (MD.seam.working.stamp.board_md5 || '').slice(0, 8),
  };
});
check(totals.n === 16, 'item 21 — 16 clubs computed', String(totals.n));
check(totals.matchesLiveBoard, 'item 21 — every club total equals the sum of its players ON THE LIVE BOARD');
check(totals.bakedWasReadable,
  'item 21 — the baked block IS present and readable for all 16 clubs (so independence is a real test, '
  + 'not one passing over an absent file)');
check(totals.independentOfBaked,
  'item 21 — and the computation is INDEPENDENT of it: corrupting every baked total changes nothing '
  + '(the staleness this removes)');
check(totals.picksKept, 'item 21 — the ingest\'s PVC band-priced picks are kept, not recomputed');
check(totals.identities, 'item 21 — overall == player + picks and player == best23 + nonBest23');
check(totals.boardPin === totals.stampPin, 'item 21 — the totals name the board they were summed from');
check(await page.locator('.cintro').count() === 0,
  'owner word 2026-08-28 — the Clubs-page intro essay is retired (methodology lives in ui/MAINTAINER.md)');

/* ------------------------------------- the ONE movement column (owner redesign 2026-08-28) */
section('REDESIGN — Round Δ is the one movement column; over-free is retired');
await go('board');
const RD = await page.evaluate(() => {
  const rows = Array.from(document.querySelectorAll('.row.working'));
  const rd = MD.board.roundDeltas();
  const rep = (() => {
    const mv = window.__MATCHDAY_MOVERS__;
    return mv.reports[String(mv.rounds[mv.rounds.length - 1])];
  })();
  const byKey = {}; rep.players.forEach(r => { byKey[r.key] = r; });
  // the pill text must be the report's own value_change for that player, on every row it renders
  const agree = (MD.seam.working.players || []).every(p => {
    const r = rd && rd[p.key];
    return !r || r.d === byKey[p.key].value_change;
  });
  return {
    rows: rows.length,
    ofreeCells: document.querySelectorAll('.ofree').length,
    pills: rows.filter(r => r.querySelector('.pill')).length,
    round: rd && rd._round, prev: rd && rd._prev,
    repRound: rep.submitted_round != null ? rep.submitted_round : rep.current_round,
    // the pill names the football pair: the round vs the previous stored ROUND — the model changes
    // between them are their own history lines, never smeared into this figure's label.
    prevRound: (() => {
      const mv = window.__MATCHDAY_MOVERS__;
      const cur = rep.submitted_round != null ? rep.submitted_round : rep.current_round;
      const lower = mv.rounds.map(Number).filter(n => !isNaN(n) && n < Number(cur));
      return lower.length ? Math.max(...lower) : rep.previous_round;
    })(),
    agree,
  };
});
check(RD.ofreeCells === 0, 'the over-free column is retired — no .ofree cell renders anywhere');
check(RD.pills === RD.rows && RD.rows > 0,
  'every board row carries the Round Δ cell', RD.pills + '/' + RD.rows);
check(RD.round === RD.repRound && RD.prev === RD.prevRound,
  'Round Δ is the LATEST report\'s round vs the previous stored round', RD.round + ' vs ' + RD.prev);
check(RD.agree, 'every rendered delta is the report\'s own value_change — computed nowhere else');

/* ------------------------------------------------------------------ no runtime errors anywhere */
section('RUNTIME');
/* DRIVEN OFF MD.TABS, not a hand-kept list. The list here used to be five names and had already
   fallen behind the app twice — Pick value and Config both shipped without ever being visited by
   this check, and Draft day would have been the third. A new tab now gets its runtime check by
   existing, which is the only way this assertion stays true of the app rather than of 2026. */
const ALL_VIEWS = await page.evaluate(() => (MD.TABS || []).map(t => t[0]));
check(ALL_VIEWS.length >= 5, 'the tab list is readable, so this loop covers the whole app',
  ALL_VIEWS.join(','));
for (const v of ALL_VIEWS) {
  await go(v);
}
check(pageErrors.length === 0, 'every view renders with no page errors',
  pageErrors.slice(0, 4).join(' | '));

await browser.close();
console.log('\n' + '-'.repeat(60));
console.log((fail ? 'FAIL ' : '') + pass + '/' + (pass + fail) + ' passed');
process.exit(fail ? 1 : 0);
