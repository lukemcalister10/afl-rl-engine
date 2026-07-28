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
 * plausibly drift (a greedy positional selection, not a sum), so its chosen KEYS are compared as an
 * ordered list, not just its total — two different selections can sum to the same number.
 *
 * NON-VACUITY: the test also mutates a player's value and asserts the two implementations still agree
 * on the changed board (so it is reading the board, not a constant), and asserts a deliberately broken
 * greedy FAILS the comparison (so the comparison can fail at all).
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
    "ui/app/positions_data.js",
    "ui/app/config.js",
    "ui/app/format.js",
    "ui/app/counting.js",
    "ui/app/seam.js",
    "ui/app/club_totals.js",
  ];
  files.forEach(function (f) {
    vm.runInContext(fs.readFileSync(path.join(ROOT, f), "utf8"), ctx, { filename: f });
  });
  if (mutate) mutate(ctx);
  return ctx;
}

/* ------------------------------------------------- the ORACLE: ingest_inputs.py build_clubs(), in JS
   Transcribed from ui/tools/ingest_inputs.py (SLOTS / BENCH / FREE_AGENTS and the greedy body). If the
   ingest changes, this transcription must change with it — that is the point of a parity test. */
const SLOTS = [["KEY_DEF", 2], ["GEN_DEF", 4], ["MID", 5], ["GEN_FWD", 4], ["KEY_FWD", 2], ["RUC", 1]];
const BENCH = 5;
const FREE_AGENTS = "Free Agents";

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
    const used = {}, best23Keys = [];
    let best23 = 0;
    SLOTS.forEach(function (slot) {
      let picked = roster.filter(function (p) { return p.posCode === slot[0] && !used[p.key]; });
      // non-vacuity lever: a deliberately WRONG greedy (take the cheapest for each slot).
      if (opts.broken) picked = picked.slice().reverse();
      picked.slice(0, slot[1]).forEach(function (p) {
        used[p.key] = 1; best23 += p.v; best23Keys.push(p.key);
      });
    });
    roster.filter(function (p) { return !used[p.key]; }).slice(0, BENCH).forEach(function (p) {
      used[p.key] = 1; best23 += p.v; best23Keys.push(p.key);
    });
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

/* -------------------------------------------------------------------- the staleness this replaced */
const baked = cvBundle.clubs || [];
const bakedByTeam = {};
baked.forEach(function (c) { bakedByTeam[c.team] = c; });
const stale = ui.clubs.filter(function (c) {
  const b = bakedByTeam[c.team];
  return b && b.totalPlayer !== c.totalPlayer;
});
check(stale.length > 0,
  "the baked club_valuation.js totals ARE stale against the live board (" + stale.length +
  "/16 clubs differ) — the reason this computation moved to the browser");

console.log("-".repeat(72));
console.log((fail ? "FAIL " : "") + pass + "/" + (pass + fail) + " passed");
process.exit(fail ? 1 : 0);
