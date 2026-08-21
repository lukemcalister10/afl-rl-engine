/* #139 item 21 — MD.clubTotals must reproduce the ingest's own arithmetic exactly.
 *
 * Club totals moved from a baked file (ui/data/club_valuation.js) to a browser computation
 * (ui/app/club_totals.js). The risk in that move is silent divergence: the browser could compute
 * something *plausible* that is not what ui/tools/ingest_inputs.py build_clubs() would have produced,
 * and nothing would say so — the baked file's own numbers cannot be the oracle, because they are stale
 * (generated against board fa172ac1; the board is now 8a38cca4).
 *
 * So the oracle is the ALGORITHM, not the artifact: this test re-implements build_clubs() from
 * ingest_inputs.py line-for-line here in the test file, runs it over the SAME live board bundle the UI
 * reads, and asserts the two agree club-for-club and metric-for-metric. Best-23 is the part that could
 * plausibly drift (a value-maximal positional SELECTION, not a sum), so its chosen KEYS are compared as
 * an ordered list, not just its total — two different selections can sum to the same number.
 *
 * #274 item 2 — what Best-23 now is: the ruled value-maximal legal 23 (#271 Addendum 19), selected from
 * the store's ELIGIBILITIES column with DPP players assignable to either eligible slot, solved as an
 * exact assignment rather than a greedy. Three copies of that algorithm exist ON PURPOSE and must move
 * together: ui/app/club_totals.js (what the browser runs), ui/tools/ingest_inputs.py (the live ingest),
 * and the transcription below (this oracle). The ruled OUTCOMES are asserted too, each against a method
 * that shares no code with the selector: slot legality by independent bipartite matching, and optimality
 * against the top-23 upper bound.
 *
 * NON-VACUITY: the test mutates a player's value and asserts the two implementations still agree on the
 * changed board (so it is reading the board, not a constant); asserts a deliberately wrong selector
 * FAILS the comparison (so the comparison can fail at all); and asserts that the obvious wrong answer —
 * the top 23 by raw value — is genuinely illegal for most clubs, so the legality check is discriminating.
 *
 * Run: node ui/tests/club_totals_parity.test.js
 */
"use strict";
const fs = require("fs");
const vm = require("vm");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
let pass = 0, fail = 0;
function check(cond, name, detail) {
  if (cond) { pass++; console.log("  [PASS] " + name); }
  else { fail++; console.log("  [FAIL] " + name + (detail ? " — " + detail : "")); }
}

/* ---------------------------------------------------------------- load the UI in a browser-ish ctx */
function loadUI(mutate) {
  const ctx = { console };
  ctx.window = ctx; ctx.globalThis = ctx;
  vm.createContext(ctx);
  const files = [
    "ui/data/board_view_working.js",
    "ui/data/board_view_public.js",
    "ui/data/club_valuation.js",
    "ui/data/ownership.js",        // #232 live-lane sidecar — club_totals now resolves through it
    "ui/app/positions_data.js",
    "ui/app/config.js",
    "ui/app/format.js",
    "ui/app/counting.js",
    "ui/app/seam.js",
    "ui/app/ownership.js",
    "ui/app/club_totals.js",
  ];
  files.forEach(function (f) {
    vm.runInContext(fs.readFileSync(path.join(ROOT, f), "utf8"), ctx, { filename: f });
  });
  if (mutate) mutate(ctx);
  return ctx;
}

/* ------------------------------------------------- the ORACLE: ingest_inputs.py build_clubs(), in JS
   Transcribed from ui/tools/ingest_inputs.py (SLOTS / BENCH / FREE_AGENTS and the selector body). If the
   ingest changes, this transcription must change with it — that is the point of a parity test.
   #274 item 2: the greedy body became `best23_of`, the ruled value-maximal legal 23 over the store's
   ELIGIBILITIES column (#271 Addendum 19). Transcribed here line-for-line, same as before. */
const SLOTS = [["KPD", 2], ["SD", 4], ["MID", 5], ["SF", 4], ["KPF", 2], ["RUCK", 1]];
const BENCH = 5;
const TARGET = 23;   // the 18 positional slots + BENCH(5)
const FREE_AGENTS = "Free Agents";

/* Transcribed from ingest_inputs.py best23_of(). `broken` is the non-vacuity lever: it flips the sign of
   the value on the player->sink edge, so the flow selects the CHEAPEST legal 23 instead of the dearest —
   still a legal 23, so it proves the comparison catches a wrong SELECTION and not merely a crash. */
function oracleBest23(roster, broken) {
  const n = roster.length;
  const SRC = 0;
  const BENCH_NODE = 1 + SLOTS.length;
  const P0 = BENCH_NODE + 1;
  const SINK = P0 + n;
  const N = SINK + 1;

  const eFrom = [], eTo = [], eCap = [], eCost = [];
  function addEdge(u, v, c, w) {
    eFrom.push(u); eTo.push(v); eCap.push(c); eCost.push(w);
    eFrom.push(v); eTo.push(u); eCap.push(0); eCost.push(-w);
  }
  for (let i = 0; i < SLOTS.length; i++) addEdge(SRC, 1 + i, SLOTS[i][1], 0);
  addEdge(SRC, BENCH_NODE, BENCH, 0);
  for (let j = 0; j < n; j++) {
    const el = roster[j].elig || [];
    for (let i = 0; i < SLOTS.length; i++) {
      if (el.indexOf(SLOTS[i][0]) >= 0) addEdge(1 + i, P0 + j, 1, 0);
    }
  }
  for (let j = 0; j < n; j++) addEdge(BENCH_NODE, P0 + j, 1, 0);
  const sinkEdge = [];
  for (let j = 0; j < n; j++) {
    sinkEdge.push(eCap.length);
    addEdge(P0 + j, SINK, 1, (broken ? 1 : -1) * (roster[j].v || 0));
  }

  const E = eCap.length;
  const INF = Infinity;
  let flow = 0;
  while (flow < TARGET) {
    const dist = new Array(N).fill(INF), prev = new Array(N).fill(-1);
    dist[SRC] = 0;
    for (let pass = 0; pass < N; pass++) {
      let changed = false;
      for (let e = 0; e < E; e++) {
        if (eCap[e] <= 0) continue;
        const u = eFrom[e];
        if (dist[u] === INF) continue;
        const nd = dist[u] + eCost[e];
        if (nd < dist[eTo[e]]) { dist[eTo[e]] = nd; prev[eTo[e]] = e; changed = true; }
      }
      if (!changed) break;
    }
    if (dist[SINK] === INF) break;
    for (let v = SINK; v !== SRC; v = eFrom[prev[v]]) {
      const e = prev[v];
      eCap[e] -= 1;
      eCap[e ^ 1] += 1;
    }
    flow += 1;
  }

  let total = 0;
  const keys = [];
  for (let j = 0; j < n; j++) {
    if (eCap[sinkEdge[j]] === 0) { total += (roster[j].v || 0); keys.push(roster[j].key); }
  }
  return { total: total, keys: keys };
}

function oracleClubs(players, picksByTeam, opts) {
  opts = opts || {};
  const rosterBy = {};
  players.forEach(function (p) {
    const t = p.affl_team;
    if (!t || t === FREE_AGENTS) return;
    (rosterBy[t] = rosterBy[t] || []).push(p);
  });
  return Object.keys(rosterBy).map(function (team) {
    const roster = rosterBy[team].slice().sort(function (a, b) { return b.v - a.v; });
    const totalPlayer = roster.reduce(function (s, p) { return s + p.v; }, 0);
    const top5 = roster.slice(0, 5).reduce(function (s, p) { return s + p.v; }, 0);
    const top10 = roster.slice(0, 10).reduce(function (s, p) { return s + p.v; }, 0);
    const sel = oracleBest23(roster, !!opts.broken);
    const best23 = sel.total, best23Keys = sel.keys;
    const tp = picksByTeam[team] || [];
    const totalPicks = tp.reduce(function (s, p) { return s + p.value; }, 0);
    return {
      team: team, overall: totalPlayer + totalPicks, totalPlayer: totalPlayer, totalPicks: totalPicks,
      top5: top5, top10: top10, best23: best23, nonBest23: totalPlayer - best23,
      nRoster: roster.length, nPicks: tp.length, best23Keys: best23Keys,
    };
  });
}

/* ------------------------------------------------------------------------------------ the compare */
const METRICS = ["overall", "totalPlayer", "totalPicks", "top5", "top10", "best23", "nonBest23",
                 "nRoster", "nPicks"];

function diffs(uiClubs, oracle) {
  const byTeam = {};
  oracle.forEach(function (c) { byTeam[c.team] = c; });
  const out = [];
  uiClubs.forEach(function (u) {
    const o = byTeam[u.team];
    if (!o) { out.push(u.team + ": missing from oracle"); return; }
    METRICS.forEach(function (m) {
      if (u[m] !== o[m]) out.push(u.team + "." + m + ": ui " + u[m] + " vs oracle " + o[m]);
    });
    if (u.best23Keys.join("|") !== o.best23Keys.join("|")) {
      out.push(u.team + ".best23Keys: selection differs");
    }
  });
  return out;
}

console.log("CLUB TOTALS PARITY — MD.clubTotals vs ingest_inputs.py build_clubs()");
console.log("-".repeat(72));

const ctx = loadUI();
const ui = ctx.MD.clubTotals.compute();
const board = ctx.window.__MATCHDAY_WORKING__;
const cvBundle = ctx.window.__CLUB_VALUATION__;
const oracle = oracleClubs(board.players, cvBundle.picksByTeam || {});

check(!!ui && ui.clubs.length === 16, "MD.clubTotals returns the 16 ranked AFFL clubs",
  ui ? "got " + ui.clubs.length : "null");
check(oracle.length === 16, "oracle builds 16 clubs", "got " + oracle.length);

const d = diffs(ui.clubs, oracle);
check(d.length === 0, "every club agrees on every metric AND on the Best-23 selection",
  d.slice(0, 6).join(" · "));

/* the Free-Agents pool is a pool, not a club — never ranked, on either spelling (item 191 / #139 item 5) */
check(!ui.clubs.some(function (c) { return /^free agents$/i.test(c.team); }),
  "the Free-Agents pool is not ranked as a club");

/* Best-23 is 23 players, and is a subset of the roster */
const b23ok = ui.clubs.every(function (c) {
  return c.best23Keys.length === Math.min(23, c.nRoster) &&
         new Set(c.best23Keys).size === c.best23Keys.length;
});
check(b23ok, "Best-23 selects exactly 23 distinct players per club");

/* ------------------------------------------------------------------ #274 item 2: the RULED behaviour
   The selection must be SLOT-LEGAL: 18 of the chosen 23 must be assignable, one per slot, each to a slot
   he is eligible for. Verified by an INDEPENDENT method — augmenting-path bipartite matching over the 18
   slot instances — so it shares no code with the min-cost-flow selector it is checking. A selector that
   returned the top 23 by value and ignored eligibility would pass the count check above and fail here. */
const SLOT_INSTANCES = SLOTS.reduce(function (acc, s) {
  for (let i = 0; i < s[1]; i++) acc.push(s[0]);
  return acc;
}, []);
function legalFillCount(keys, byKey) {
  const owner = {};                        // slot instance index -> player key, via augmenting paths
  function aug(si, seen) {
    for (let i = 0; i < keys.length; i++) {
      const k = keys[i];
      if (seen[k]) continue;
      if (((byKey[k] || {}).elig || []).indexOf(SLOT_INSTANCES[si]) < 0) continue;
      seen[k] = 1;
      if (owner[k] === undefined || aug(owner[k], seen)) { owner[k] = si; return true; }
    }
    return false;
  }
  let filled = 0;
  for (let si = 0; si < SLOT_INSTANCES.length; si++) if (aug(si, {})) filled++;
  return filled;
}
const uiByKey = {};
ctx.window.__MATCHDAY_WORKING__.players.forEach(function (p) { uiByKey[p.key] = p; });
const illegal = ui.clubs.filter(function (c) {
  return legalFillCount(c.best23Keys, uiByKey) !== SLOT_INSTANCES.length;
}).map(function (c) { return c.team; });
check(illegal.length === 0,
  "every club's Best-23 legally fills all 18 positional slots from the ELIGIBILITIES column",
  illegal.join(", "));

/* NON-VACUITY for that check, both directions: the top 23 by raw value — the obvious wrong answer — is
   NOT slot-legal for every club, so the assertion above is discriminating rather than always true. */
const rosterByTeam = {};
ctx.window.__MATCHDAY_WORKING__.players.forEach(function (p) {
  if (ctx.MD.isPickAsset(p)) return;
  const t = ctx.MD.canonClub(ctx.MD.ownership.clubOf(p));
  if (!t || /^free agents$/i.test(t)) return;
  (rosterByTeam[t] = rosterByTeam[t] || []).push(p);
});
const naiveIllegal = Object.keys(rosterByTeam).filter(function (t) {
  const top23 = rosterByTeam[t].slice().sort(function (a, b) { return b.v - a.v; }).slice(0, 23);
  return legalFillCount(top23.map(function (p) { return p.key; }), uiByKey) !== SLOT_INSTANCES.length;
});
check(naiveIllegal.length > 0,
  "NON-VACUITY: taking the top 23 by raw value is NOT slot-legal for every club, so legality is a real constraint  (" +
  naiveIllegal.length + " of " + Object.keys(rosterByTeam).length + " clubs would be illegal)");

/* OPTIMALITY, against an oracle that shares no code with the selector: the plain top 23 by value is an
   upper bound on any legal 23, so wherever that set is ALREADY legal the optimum must equal its sum —
   and no club may ever exceed it. This is what separates "optimised" from "a better greedy". */
let boundClubs = 0, boundMatched = 0, exceeded = [];
ui.clubs.forEach(function (c) {
  const top23 = rosterByTeam[c.team].slice().sort(function (a, b) { return b.v - a.v; }).slice(0, 23);
  const ub = top23.reduce(function (s, p) { return s + p.v; }, 0);
  if (c.best23 > ub) exceeded.push(c.team);
  if (legalFillCount(top23.map(function (p) { return p.key; }), uiByKey) === SLOT_INSTANCES.length) {
    boundClubs++;
    if (c.best23 === ub) boundMatched++;
  }
});
check(exceeded.length === 0, "no club's Best-23 exceeds the top-23 upper bound", exceeded.join(", "));
check(boundClubs > 0 && boundMatched === boundClubs,
  "where the top-23 is already legal, Best-23 equals that provable optimum  (" +
  boundMatched + " of " + boundClubs + " such clubs)");

/* THE TWO MEASURED AXIS-ARTIFACT CASES (#271 A19) resolve. Under `posCode` — the modelling axis, which
   cannot see DPP — Adelaide could fill only 16 of 18 slots and Hawthorn 17; both now fill 18 from the
   eligibility axis. Asserted by NAME because these two clubs are the ruling's own evidence. */
["Adelaide Crows", "Hawthorn Hawks"].forEach(function (team) {
  const c = ui.clubs.find(function (x) { return x.team === team; });
  const grpFilled = SLOT_INSTANCES.reduce(function (acc, code) {
    const p = rosterByTeam[team].slice().sort(function (a, b) { return b.v - a.v; })
      .find(function (q) { return q.posCode === code && !acc.used[q.key]; });
    if (p) { acc.used[p.key] = 1; acc.n++; }
    return acc;
  }, { used: {}, n: 0 }).n;
  check(!!c && grpFilled < SLOT_INSTANCES.length &&
        legalFillCount(c.best23Keys, uiByKey) === SLOT_INSTANCES.length,
    "axis artifact resolved for " + team + " — the modelling axis fills " + grpFilled +
    "/18, the eligibility axis fills 18/18");
});

/* the identities the baked file asserted about itself must still hold on the live computation */
const idOk = ui.clubs.every(function (c) {
  return c.overall === c.totalPlayer + c.totalPicks && c.totalPlayer === c.best23 + c.nonBest23;
});
check(idOk, "overall == player + picks, and player == best23 + nonBest23");

/* -------------------------------------------------------------------------------- NON-VACUITY (1)
   Move a real player's value and re-run BOTH sides: they must still agree, and the club's total must
   actually change. Proves the UI reads the board rather than echoing a constant. */
const mutCtx = loadUI(function (c) {
  const pl = c.window.__MATCHDAY_WORKING__.players;
  const target = pl.find(function (p) { return p.affl_team && p.affl_team !== FREE_AGENTS; });
  target.v = target.v + 100000;                     // large enough to reorder his club's roster
});
const mutUI = mutCtx.MD.clubTotals.compute();
const mutOracle = oracleClubs(mutCtx.window.__MATCHDAY_WORKING__.players, cvBundle.picksByTeam || {});
const mutDiffs = diffs(mutUI.clubs, mutOracle);
check(mutDiffs.length === 0, "they still agree after a player's value is moved",
  mutDiffs.slice(0, 4).join(" · "));
const movedTotals = JSON.stringify(mutUI.clubs.map(function (c) { return c.totalPlayer; }));
const baseTotals = JSON.stringify(ui.clubs.map(function (c) { return c.totalPlayer; }));
check(movedTotals !== baseTotals, "moving a player's value CHANGES the computed totals (not a constant)");

/* -------------------------------------------------------------------------------- NON-VACUITY (2)
   A deliberately broken greedy must FAIL the comparison — proves the comparison can fail. */
const brokenDiffs = diffs(ui.clubs, oracleClubs(board.players, cvBundle.picksByTeam || {}, { broken: true }));
check(brokenDiffs.length > 0, "a deliberately wrong Best-23 greedy is REJECTED (the check can fail)");

/* ------------------------------------------------------ the baked totals must not be consulted at all
   This assertion used to read `stale.length > 0` — "the baked club_valuation.js totals ARE stale against
   the live board". That was true when written and is a FACT ABOUT A MOMENT, not an invariant: it holds
   only while nobody re-runs the ingest, and it failed the moment #232 regenerated the bundle against the
   current board. A guard that goes red when you correctly refresh an input is guarding the wrong thing.

   The durable property it was reaching for is that the browser does not READ those baked totals. So
   assert that directly: corrupt every baked club total and require the computation to be unmoved. This
   cannot pass vacuously — if MD.clubTotals ever consulted the baked block again, the corruption would
   show up immediately. It is also strictly stronger than the staleness check, which could only ever
   observe that two numbers happened to differ. */
const corrupted = loadUI(function (c) {
  (c.window.__CLUB_VALUATION__.clubs || []).forEach(function (cl) {
    cl.totalPlayer = -1; cl.top5 = -1; cl.top10 = -1;
    cl.best23 = -1; cl.nonBest23 = -1; cl.overall = -1; cl.nRoster = -1;
  });
});
const corruptedUI = corrupted.MD.clubTotals.compute();
const unmoved = JSON.stringify(corruptedUI.clubs.map(function (c) {
  return [c.team, c.totalPlayer, c.top5, c.top10, c.best23, c.nonBest23, c.nRoster];
}));
const original = JSON.stringify(ui.clubs.map(function (c) {
  return [c.team, c.totalPlayer, c.top5, c.top10, c.best23, c.nonBest23, c.nRoster];
}));
check(unmoved === original,
  "corrupting every baked club total in club_valuation.js changes NOTHING — the browser computes the "
  + "player side from the board and never reads the baked block");
check(ui.clubs.length > 0 && ui.clubs.some(function (c) { return c.totalPlayer > 0; }),
  "…and the computation is non-empty, so that assertion is not passing over an empty club list",
  ui.clubs.length + " clubs");

/* ============================================================ THE PICKS PIN — v827, both directions
 * ui/data/club_valuation.js is the PICK-LOCATIONS bundle and it carries the board + store it was
 * generated from. Until 2026-08-21 nothing compared that stamp with the board the app is loaded on:
 * `halted = !!(cv && cv.halt)` honoured whatever bundle was present. It was found that night carrying
 * board a05fe951 / R22 while the tree stood on b3e8da99 / R23, and the pocket and club pages showed
 * R22-board pick VALUES with nothing refusing and nothing flagged.
 *
 * `MD.clubTotals.pin()` is the #232 mirror law applied to this bundle — the same shape
 * `MD.ownership.pin()` uses. These cases assert BOTH directions, because a guard proved in one
 * direction is a guard that might simply always refuse (or always pass):
 *
 *   MATCHING   the live bundle authenticates, picks render, and the figures are real (non-zero).
 *   MISMATCHED store, board, and a stamp-less bundle each REFUSE, each with a reason naming the two
 *              identities, and every pick figure goes to the unavailable path rather than to 0 or to
 *              a stale number — on the clubs reader AND on the seam every other surface reads.
 */
console.log("");
console.log("THE PICKS PIN (v827) — a bundle that is not this tree's must REFUSE, not whisper");
console.log("-".repeat(72));

const liveBoard = String(board.stamp.board);
const liveStore = String(board.stamp.store);

/* ---- DIRECTION 1: the matching stamp renders --------------------------------------------------- */
check(ctx.MD.clubTotals.pin().ok === true,
  "MATCHING STAMP: the shipped bundle authenticates against the loaded board + store",
  JSON.stringify(ctx.MD.clubTotals.pin()));
check(ui.picksAvailable === true, "MATCHING STAMP: picks are AVAILABLE");
check((ui.picksSource || {}).board === liveBoard && (ui.picksSource || {}).store === liveStore,
  "MATCHING STAMP: picksSource carries the bundle's IDENTITY fields (board + store), not a wall clock");
check((ui.picksSource || {}).generated === undefined,
  "MATCHING STAMP: picksSource carries NO `generated` timestamp — the field was dropped so the bundle "
  + "could be byte-proved and become a landing carrier (writer 6)");
check(ctx.MD.seam.clubHalt() === null, "MATCHING STAMP: the seam reports no halt");
const someTeam = ui.clubs.find(function (c) { return c.nPicks > 0; });
check(!!someTeam && someTeam.totalPicks > 0 && ctx.MD.seam.picksFor(someTeam.team).length > 0,
  "MATCHING STAMP: real pick figures reach the readers (non-vacuity — this is not a guard that "
  + "always refuses)", someTeam ? someTeam.team + " " + someTeam.totalPicks : "no club holds picks");

/* ---- DIRECTION 2: a mismatched stamp refuses ---------------------------------------------------- */
function refusedCtx(mutateStamp) {
  return loadUI(function (c) { mutateStamp(c.window.__CLUB_VALUATION__.stamp); });
}
const STALE_BOARD = "a05fe951dead0000dead0000dead0000";   // the identity actually found stale, 2026-08-21
const STALE_STORE = "cc02567f";

[["store", function (st) { st.store = STALE_STORE; }, STALE_STORE, liveStore],
 ["board", function (st) { st.board = STALE_BOARD; }, STALE_BOARD, liveBoard],
].forEach(function (caseDef) {
  const what = caseDef[0], mutate = caseDef[1], wrong = caseDef[2], right = caseDef[3];
  const c = refusedCtx(mutate);
  const pn = c.MD.clubTotals.pin();
  const t = c.MD.clubTotals.compute();
  check(pn.ok === false, "MISMATCHED " + what.toUpperCase() + ": the bundle is REFUSED");
  check(typeof pn.why === "string"
        && pn.why.indexOf(String(wrong).slice(0, 8)) >= 0
        && pn.why.indexOf(String(right).slice(0, 8)) >= 0,
    "MISMATCHED " + what.toUpperCase() + ": the reason NAMES BOTH identities — the one the bundle was "
    + "generated from and the one the app is loaded on", pn.why);
  check(t.picksAvailable === false && (t.picksSource || {}).halted === true,
    "MISMATCHED " + what.toUpperCase() + ": picks go to the HALTED/unavailable path");
  check((t.picksSource || {}).reason === pn.why,
    "MISMATCHED " + what.toUpperCase() + ": the surface is handed the SAME reason (clubs.js prints it "
    + "instead of 'the club-valuation bundle is absent')");
  check(t.clubs.every(function (cl) { return cl.totalPicks === 0 && cl.nPicks === 0; }),
    "MISMATCHED " + what.toUpperCase() + ": no stale pick value survives into any club total "
    + "(the readers show n/a, never 0-as-a-figure — clubs.js / pocket.js / board.js)");
  const h = c.MD.seam.clubHalt();
  check(!!h && h.reason === pn.why && h.pinRefused === true,
    "MISMATCHED " + what.toUpperCase() + ": the SEAM refuses too, so the board's picks-included overlay "
    + "disables with the reason on hover");
  check(c.MD.seam.picksFor(someTeam.team).length === 0,
    "MISMATCHED " + what.toUpperCase() + ": MD.seam.picksFor yields nothing — the held-picks panel and "
    + "the club headers cannot print a stale price");
  /* NON-VACUITY for this whole block: the PLAYER side is untouched by the refusal, so the cases above
     are not passing because the computation collapsed. */
  check(t.clubs.length === 16
        && JSON.stringify(t.clubs.map(function (x) { return [x.team, x.totalPlayer]; }).sort())
           === JSON.stringify(ui.clubs.map(function (x) { return [x.team, x.totalPlayer]; }).sort()),
    "MISMATCHED " + what.toUpperCase() + ": the player side is UNAFFECTED — 16 clubs, every player "
    + "total identical (the refusal is scoped to the picks, not a collapse)");
});

/* a bundle carrying no pin at all cannot be authenticated — the same fail-closed rule the ownership
   mirror applies, and the reason #232's presence-only gate was not a guard. */
const noPin = refusedCtx(function (st) { delete st.board; delete st.store; });
check(noPin.MD.clubTotals.pin().ok === false
      && /no board\/store stamp/.test(noPin.MD.clubTotals.pin().why || ""),
  "A BUNDLE WITH NO board/store STAMP is refused — it cannot be told apart from a stale one",
  noPin.MD.clubTotals.pin().why);

/* the ingest's own halt still reaches the reader, and still by its own reason. */
const ingestHalted = loadUI(function (c) {
  c.window.__CLUB_VALUATION__.halt = { reason: "SELF-TEST: the ingest refused" };
});
check(ingestHalted.MD.clubTotals.pin().ok === false
      && ingestHalted.MD.clubTotals.compute().picksSource.reason === "SELF-TEST: the ingest refused",
  "AN INGEST HALT still refuses, and still carries the ingest's OWN reason (the pin did not swallow it)");

console.log("-".repeat(72));
console.log((fail ? "FAIL " : "") + pass + "/" + (pass + fail) + " passed");
process.exit(fail ? 1 : 0);
