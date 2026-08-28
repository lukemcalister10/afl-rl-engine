/* #283 — OWNERSHIP SINGLE SOURCE: the browser-side acceptance proofs.
 *
 * WHAT IS AT RISK.  Before #283 the UI resolved a player's club through ui/data/ownership.js while the
 * clubs parity oracle read the store's `affl_team`. Two sources behind one fact. They agreed only by the
 * coincidence that no override existed; the moment the owner's 2026-07-29 CSV was ingested, 18 of 804
 * players moved and parity went red (ui/screenshots/issue_274/02_item2_FINDING_ownership.md).
 *
 * Under the owner ruling of 2026-07-30 the STORE is the single source and ownership.js is a GENERATED
 * MIRROR rebuilt FROM it. This file proves that is true of the SHIPPED bundles, and — the part that
 * matters — that the proof can FAIL. A same-source check that cannot go red is worth nothing: that is
 * exactly the state #232 was in for months.
 *
 * EVERY ASSERTION HERE IS PROVEN BOTH DIRECTIONS. The clean population passes; a population differing
 * only in the injected divergence fails. A check that never sees its own failing case cannot distinguish
 * "correct" from "always true".
 *
 * Run: node ui/tests/ownership_single_source.test.js
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

const FILES = [
  "ui/data/board_view_working.js",
  "ui/data/board_view_public.js",
  "ui/data/club_valuation.js",
  "ui/data/ownership.js",
  "ui/app/positions_data.js",
  "ui/app/config.js",
  "ui/app/format.js",
  "ui/app/counting.js",
  "ui/app/seam.js",
  "ui/app/ownership.js",
  "ui/app/club_totals.js",
];

/* `mutate(ctx, runIn)` runs after the DATA bundles load but before the APP modules, so a test can
   reshape what the modules will read. Top-level rebinding must go through runIn — a host-side
   assignment does not propagate into the VM's global, and a test written that way silently exercises
   the un-mutated path and passes for the wrong reason. */
function loadUI(mutate) {
  const ctx = { console };
  ctx.window = ctx; ctx.globalThis = ctx;
  vm.createContext(ctx);
  const runIn = function (src) { return vm.runInContext(src, ctx, { filename: "test-mutation" }); };
  FILES.forEach(function (f) {
    if (f === "ui/app/config.js" && mutate) mutate(ctx, runIn);
    vm.runInContext(fs.readFileSync(path.join(ROOT, f), "utf8"), ctx, { filename: f });
  });
  return ctx;
}

console.log("\n#283 — ownership single source (browser side)");
console.log("-".repeat(72));

// ---------------------------------------------------------------- the shipped state
const clean = loadUI();
const W = clean.__MATCHDAY_WORKING__;
const OWN = clean.__OWNERSHIP__;
const nBoard = W.players.length;

check(OWN.stamp.sourceOfTruth === "store",
  "the mirror declares the store as its source of truth");

check(!!OWN.stamp.generatedFromStore && OWN.stamp.generatedFromStore.length === 32,
  "the mirror names in full the store it was generated from (deterministic provenance, no wall clock)");

check(OWN.stamp.generated === undefined,
  "the mirror carries NO wall-clock stamp — otherwise 'regenerate and byte-compare' could never be an equality");

// V2 (a) — reader and oracle are the same field on the shipped bundles.
const disagree = W.players.filter(function (p) {
  return p.key && OWN.byKey[p.key] !== undefined && OWN.byKey[p.key] !== p.affl_team;
});
check(disagree.length === 0,
  "READER == ORACLE on all " + nBoard + " board players (the mirror is the board's own affl_team)",
  disagree.slice(0, 3).map(function (p) { return p.name; }).join(", "));

check(OWN.stamp.nOverriding === 0 && (OWN.overriding || []).length === 0,
  "nOverriding is 0 BY CONSTRUCTION — a mirror cannot override the field it is generated from");

// the fixture, DERIVED (shrink review S1 form, 2026-08-28): the six sentinel players' clubs are
// read from the CURRENT authored CSV — the single source this suite exists to prove — instead of
// a frozen 2026-07-29 snapshot, which went stale the first time the owner traded one of them
// again (Ed Langdon, 2026-08-28). The property is unchanged: authored sheet == board == mirror,
// three ways, including the name-twin row (sam-butler-1 is the BOARD row for the authored 'Sam
// Butler'; his storeless twin sam-butler must NOT receive the write).
const SENTINELS = {
  "beau-mccreery": "Beau McCreery",
  "lachie-neale": "Lachie Neale",
  "jack-sinclair": "Jack Sinclair",
  "ed-langdon": "Ed Langdon",
  "brennan-cox": "Brennan Cox",
  "sam-butler-1": "Sam Butler",
};
const csvText = fs.readFileSync(path.join(__dirname, "..", "..", "docs", "inputs", "AFFL_Player_Locations.csv"), "utf8");
const sheetClub = {};
csvText.split(/\r?\n/).slice(1).forEach(function (ln) {
  if (!ln.trim()) return;
  const m = ln.match(/^("[^"]*"|[^,]*),("[^"]*"|[^,]*),/);
  if (m) sheetClub[m[1].replace(/"/g, "")] = m[2].replace(/"/g, "");
});
const FIXTURE = {};
Object.keys(SENTINELS).forEach(function (k) { FIXTURE[k] = sheetClub[SENTINELS[k]]; });
const byKey = {};
W.players.forEach(function (p) { if (p.key) byKey[p.key] = p; });
const fixtureOk = Object.keys(FIXTURE).every(function (k) {
  return FIXTURE[k] && byKey[k] && byKey[k].affl_team === FIXTURE[k] && OWN.byKey[k] === FIXTURE[k];
});
check(fixtureOk, "the authored sheet's clubs for the six sentinels are on the board AND in the mirror (DERIVED from the CSV; incl. the name-twin sam-butler-1)");

// V6 — the two free-agent spellings must not fork a bucket
const buckets = {};
W.players.forEach(function (p) { if (p.affl_team) buckets[p.affl_team] = 1; });
const names = Object.keys(buckets).sort();
check(names.length === 17,
  "16 clubs + Free Agents = 17 buckets — the store's two free-agent spellings do not fork",
  names.join(" | "));
check(names.filter(function (n) { return n.toLowerCase() === "free agents"; }).length === 1,
  "exactly ONE free-agent bucket after display canonicalisation");

// ---------------------------------------------------------------- NON-VACUITY
// V2 (b) — inject divergence into the MIRROR only; the same-source check must go red.
const divergedMirror = loadUI(function (ctx) {
  const k = Object.keys(ctx.__OWNERSHIP__.byKey)[0];
  ctx.__OWNERSHIP__.byKey[k] = "Hawthorn Hawks__INJECTED";
});
const dm = divergedMirror.__MATCHDAY_WORKING__.players.filter(function (p) {
  return p.key && divergedMirror.__OWNERSHIP__.byKey[p.key] !== undefined
      && divergedMirror.__OWNERSHIP__.byKey[p.key] !== p.affl_team;
});
check(dm.length === 1,
  "NON-VACUITY: divergence injected into the MIRROR is detected (the check can go red)");

// V2 (c) — inject divergence into the BOARD only; same check, other direction.
const divergedBoard = loadUI(function (ctx) {
  ctx.__MATCHDAY_WORKING__.players[0].affl_team = "Hawthorn Hawks__INJECTED";
});
const db = divergedBoard.__MATCHDAY_WORKING__.players.filter(function (p) {
  return p.key && divergedBoard.__OWNERSHIP__.byKey[p.key] !== undefined
      && divergedBoard.__OWNERSHIP__.byKey[p.key] !== p.affl_team;
});
check(db.length === 1,
  "NON-VACUITY: divergence injected into the BOARD is detected (proven the other direction too)");

// ---------------------------------------------------------------- V3, the hand-edit bar
check(clean.MD.ownership.pin().ok === true && clean.MD.ownership.status().active === true,
  "the shipped mirror passes the pin check and is ACTIVE");

const wrongStore = loadUI(function (ctx) {
  ctx.__OWNERSHIP__.stamp.store = "deadbeef";
});
check(wrongStore.MD.ownership.pin().ok === false,
  "a mirror stamped with the WRONG STORE is refused by the pin check");
check(wrongStore.MD.ownership.status().active === false,
  "...and is therefore NOT ACTIVE — a stale sidecar can no longer be honoured (the #232 hole)");
check(/store/.test(String(wrongStore.MD.ownership.status().pinWhy || "")),
  "...and the refusal NAMES the store mismatch rather than failing silently",
  String(wrongStore.MD.ownership.status().pinWhy));

const wrongBoard = loadUI(function (ctx) {
  ctx.__OWNERSHIP__.stamp.board = "8a38cca44f53152090cb3df3f78bd47e";   // the PRE-ADOPTION board
});
check(wrongBoard.MD.ownership.pin().ok === false && wrongBoard.MD.ownership.status().active === false,
  "a mirror stamped with the PRE-ADOPTION board (8a38cca4) is refused — the exact stale state #232 honoured");

const noPin = loadUI(function (ctx) {
  delete ctx.__OWNERSHIP__.stamp.store;
  delete ctx.__OWNERSHIP__.stamp.board;
});
check(noPin.MD.ownership.pin().ok === false && noPin.MD.ownership.status().active === false,
  "a mirror carrying NO pin at all is refused — it cannot be authenticated");

// A refused mirror must DEGRADE, never mislead: rows fall back to the board's own store-derived field,
// which since #283 is the same fact the mirror carried.
const refusedResolve = wrongStore.MD.ownership.resolve(wrongStore.__MATCHDAY_WORKING__.players[0]);
check(refusedResolve.club === wrongStore.__MATCHDAY_WORKING__.players[0].affl_team
      && refusedResolve.refused === false,
  "a refused mirror degrades to the board's store-derived club — a degraded display, never a wrong club");

console.log("-".repeat(72));
console.log(pass + "/" + (pass + fail) + " passed");
process.exit(fail ? 1 : 0);
