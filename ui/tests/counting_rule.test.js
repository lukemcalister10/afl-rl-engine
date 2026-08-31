/* UI v1.3.1 — unit tests for THE OWNER'S POSITIONAL COUNTING RULE, COLLAPSE-FIRST (items 196(2), 216).
   Run:  node ui/tests/counting_rule.test.js      (exit 0 = all pass, exit 1 = a failure)
   Exercises the EXACT function the browser runs (ui/app/counting.js is dual-target). */
var C = require("../app/counting.js");
var fs = require("fs"), path = require("path");

var fails = 0, n = 0;
function approx(a, b) { return Math.abs(a - b) < 1e-9; }
function eqWeights(got, want, label) {
  n++;
  var keys = {};
  Object.keys(got).forEach(function (k) { keys[k] = 1; });
  Object.keys(want).forEach(function (k) { keys[k] = 1; });
  var ok = Object.keys(keys).every(function (k) { return approx(got[k] || 0, want[k] || 0); });
  report(ok, label, JSON.stringify(want), JSON.stringify(got));
}
function eqArr(got, want, label) {
  n++;
  var ok = got.length === want.length && got.every(function (v, i) { return v === want[i]; });
  report(ok, label, JSON.stringify(want), JSON.stringify(got));
}
function assert(cond, label, want, got) { n++; report(!!cond, label, want, got); }
function report(ok, label, want, got) {
  if (ok) { console.log("  [PASS] " + label); }
  else { fails++; console.log("  [FAIL] " + label + "  want=" + want + " got=" + got); }
}
function sum(o) { return Object.keys(o).reduce(function (s, k) { return s + o[k]; }, 0); }

console.log("COUNTING-RULE TESTS (items 196(2), 216 — collapse-first)\n  " + "-".repeat(60));

// --- THE COLLAPSE (item 216): K absorbs its same-flank G, applied first ------------------------
eqArr(C.collapse(["SF", "KPF"]), ["KPF"],
  "collapse: K-FWD absorbs G-FWD -> plain KPF");
eqArr(C.collapse(["SD", "KPD"]), ["KPD"],
  "collapse: K-DEF absorbs G-DEF -> plain KPD");
eqArr(C.collapse(["SF", "KPF", "MID"]), ["KPF", "MID"],
  "collapse: {G-FWD,K-FWD,MID} -> {K-FWD,MID} (Langford pattern)");
eqArr(C.collapse(["SD", "KPD", "KPF", "SF"]), ["KPD", "KPF"],
  "collapse: four-way swingman -> DPP {K-DEF,K-FWD}");
eqArr(C.collapse(["RUCK", "KPF", "SF"]), ["RUCK", "KPF"],
  "collapse: {RUCK,K-FWD,G-FWD} -> DPP {RUC,K-FWD} (ruck swingman)");
eqArr(C.collapse(["SF"]), ["SF"],
  "collapse: a bare G-FWD (no K) is UNTOUCHED — G stands alone");
eqArr(C.collapse(["KPD", "SF"]), ["KPD", "SF"],
  "collapse: cross-flank K-DEF + G-FWD do NOT collapse (different flanks)");

// --- the owner's verbatim cases, applied AFTER collapse ----------------------------------------
eqWeights(C.positionWeights(["SF"]), { SF: 1 },
  "single position (non-mid) -> 1.0 to that position");
eqWeights(C.positionWeights(["MID"]), { MID: 1 },
  "single position (MID-only) -> 1.0 to MID");
eqWeights(C.positionWeights(["KPD", "KPF"]), { KPD: 0.5, KPF: 0.5 },
  "DPP, no mid -> 0.5 to each (Matt Whitlock, corrected pure-key)");
eqWeights(C.positionWeights(["MID", "SF"]), { SF: 1, MID: 0 },
  "DPP-mid EXCEPTION -> non-mid counts 1, MID counts 0");
eqWeights(C.positionWeights(["SF", "MID"]), { SF: 1, MID: 0 },
  "DPP-mid EXCEPTION (mid listed second) -> non-mid 1, MID 0");

// --- one case per COLLAPSED pattern (the item-4 required set) ----------------------------------
eqWeights(C.positionWeights(["RUCK", "KPF", "SF"]), { RUCK: 0.5, KPF: 0.5 },
  "RUCK/K-FWD swingman: collapse then DPP -> RUC 0.5, K-FWD 0.5");
eqWeights(C.positionWeights(["SD", "KPD", "KPF", "SF"]), { KPD: 0.5, KPF: 0.5 },
  "four-way swingman: collapse then DPP -> K-DEF 0.5, K-FWD 0.5");
eqWeights(C.positionWeights(["SF", "KPF", "MID"]), { KPF: 1, MID: 0 },
  "Langford (K-FWD/MID after collapse): DPP-mid exception -> K-FWD 1, MID 0");
eqWeights(C.positionWeights(["SD", "SF"]), { SD: 0.5, SF: 0.5 },
  "corrected pure-general (Flanders/Baker/Langdon): DPP -> G-DEF 0.5, G-FWD 0.5");

// --- invariants -------------------------------------------------------------------------------
assert(approx(sum(C.positionWeights(["KPD", "KPF"])), 1), "weights sum to 1.0 (DPP)", "1", "see");
assert(approx(sum(C.positionWeights(["MID", "SF"])), 1), "weights sum to 1.0 (DPP-mid)", "1", "see");
assert(approx(sum(C.positionWeights(["RUCK", "KPF", "SF"])), 1), "weights sum to 1.0 (collapsed swingman)", "1", "see");
assert(Object.keys(C.positionWeights([])).length === 0, "no position -> empty (unattributed)", "{}", "see");
eqWeights(C.positionWeights(["SF", "SF"]), { SF: 1 },
  "duplicate token collapses -> 1.0 (no double count)");

// --- OBITUARY guard: a genuine 3+ post-collapse set is an INVARIANT VIOLATION (throws) ---------
(function () {
  n++;
  var threw = false;
  try { C.positionWeights(["KPD", "KPF", "MID"]); } catch (e) { threw = true; }
  report(threw, "3+ effective positions after collapse THROWS (equal-split generalisation is dead)",
    "throw", threw ? "threw" : "no throw");
})();

// --- value-conservation over a synthetic mixed roster -----------------------------------------
(function () {
  var roster = [
    { codes: ["MID"], v: 8000 },
    { codes: ["KPD", "KPF"], v: 6000 },
    { codes: ["MID", "SD"], v: 4000 },
    { codes: ["RUCK", "KPF", "SF"], v: 900 },
    { codes: ["SD", "KPD", "KPF", "SF"], v: 1200 },
  ];
  var bucket = {}, total = 0;
  roster.forEach(function (r) { C.accumulate(bucket, r.codes, r.v); total += r.v; });
  assert(approx(sum(bucket), total),
    "roster: Sigma positional value == Sigma player value (conservation)", String(total), String(sum(bucket)));
})();

// --- THE <=2 ASSERTION over the REAL shipped map (item 216(3)) ---------------------------------
// A committed test FAILS if any ranked player carries 3+ effective positions after the collapse.
(function () {
  var src = fs.readFileSync(path.join(__dirname, "..", "app", "positions_data.js"), "utf8");
  var obj = JSON.parse(src.slice(src.indexOf("{"), src.lastIndexOf("}") + 1));
  var byKey = obj.byKey || {};
  var offenders = [];
  Object.keys(byKey).forEach(function (k) {
    var eff = C.collapse(byKey[k]);
    if (eff.length > 2) offenders.push(k + " -> " + eff.join(","));
    C.positionWeights(byKey[k]);   // must never throw on real data (the invariant holds)
  });
  assert(offenders.length === 0,
    "SHIPPED map: NO player exceeds 2 effective positions after collapse (" +
      Object.keys(byKey).length + " players checked)",
    "0 offenders", offenders.length ? offenders.slice(0, 8).join(" | ") : "0 offenders");
})();

/* ================================================================================================
   THE POSITION MAP'S REAL INVARIANT: IT COVERS THE ROSTER, EXACTLY.

   ui/app/positions_data.js carries a stamp naming a BOARD md5 (`f2df6e0a` at the time of writing,
   against a working bundle of `c8c2f2b6`), and nothing checks it. That stamp is the wrong pin and
   the mismatch is not the defect it looks like: the map is VALUES-FREE — a player key to position
   codes, off the owner's locations CSV — so it does not depend on the board at all. A price move
   cannot stale it. What CAN stale it is the ROSTER changing, and that is what is asserted here.

   The reader is already honest about a miss. ui/app/pocket.js accumulates an uncovered player's
   value into an `unlisted` bucket and renders it as an alarm-coloured "Unlisted" row with its share
   of the club — so a gap shows on screen rather than vanishing. That is a better guard than a board
   md5 would have been, and it is why this file was never in the same class as the v0 sidecar or the
   picks bundle, both of which shipped silently wrong.

   What was missing is this: a gap should go RED IN A SUITE, not wait for somebody to notice a row.
   Set equality both ways, so a player who joins the league and a player who leaves both fail — and
   the failure names them, because "the map is stale" is not an actionable sentence and
   "these three keys are on the board and not in the map" is. */
(function () {
  var src = fs.readFileSync(path.join(__dirname, "..", "app", "positions_data.js"), "utf8");
  var map = JSON.parse(src.slice(src.indexOf("{"), src.lastIndexOf("}") + 1));
  var bsrc = fs.readFileSync(path.join(__dirname, "..", "data", "board_view_working.js"), "utf8");
  var board = JSON.parse(bsrc.slice(bsrc.indexOf("{"), bsrc.lastIndexOf("}") + 1));
  var mapKeys = map.byKey || {};
  var boardKeys = {};
  (board.players || []).forEach(function (p) { boardKeys[p.key] = 1; });
  var missing = Object.keys(boardKeys).filter(function (k) { return !mapKeys[k]; });
  var extra = Object.keys(mapKeys).filter(function (k) { return !boardKeys[k]; });
  assert(missing.length === 0,
    "SHIPPED map: every board player has position codes (" + Object.keys(boardKeys).length +
      " on the board) — an uncovered player's value falls into pocket.js's alarm-coloured " +
      "\"Unlisted\" row, which is honest but should never have to fire",
    "0 uncovered", missing.length ? missing.slice(0, 8).join(", ") : "0 uncovered");
  assert(extra.length === 0,
    "SHIPPED map: and it carries NOBODY who is not on the board — a departed player left in it is " +
      "the same staleness in the other direction, and nothing on screen would show it",
    "0 stragglers", extra.length ? extra.slice(0, 8).join(", ") : "0 stragglers");
  assert(map.stamp && map.stamp.n === Object.keys(mapKeys).length,
    "SHIPPED map: its stamp's own count is the number of players it actually carries",
    String(Object.keys(mapKeys).length), String(map.stamp && map.stamp.n));

  /* ---- THE STAMP NAMES ITS REAL DEPENDENCIES, AND THIS SIDE RECOMPUTES THEM -------------------
     The stamp used to name a BOARD, which this map does not depend on: it is values-free, so a
     price move or a round advance moves the board md5 and leaves every position code where it was.
     It now names the two things that CAN stale it — the roster (the board's player-key set) and the
     owner's CSV — and both are recomputed here from the same raw bytes the writer used.

     Recomputed in node rather than trusted, and deliberately NOT by re-implementing the CSV's name
     join: the signature is over the key SET and the CSV's md5, both of which two languages can
     agree on exactly. A normalisation implemented twice is a normalisation that disagrees
     eventually. ui/tools/positions_identity.py carries the definition and the reasoning. */
  var crypto = require("crypto");
  var st = map.stamp || {};
  var sig = crypto.createHash("sha256");
  sig.update(st.rosterSigVersion + "\u001e", "utf8");
  Object.keys(boardKeys).sort().forEach(function (k) { sig.update(k + "\u001e", "utf8"); });
  assert(st.rosterSig === sig.digest("hex"),
    "SHIPPED map: its stamped ROSTER signature is the board's own player-key set, recomputed here " +
      "— so a player joining or leaving the league stales it loudly instead of silently",
    "recomputed match", String(st.rosterSig).slice(0, 12));

  var csvPath = path.join(__dirname, "..", "..", "docs", "inputs", "AFFL_Player_Locations.csv");
  assert(st.locationsCsvMd5 === crypto.createHash("md5").update(fs.readFileSync(csvPath)).digest("hex"),
    "SHIPPED map: and its stamped CSV md5 is the owner's locations file as committed — a re-cut CSV " +
      "changes the codes with no board movement at all, so it is the other real dependency",
    "recomputed match", String(st.locationsCsvMd5).slice(0, 12));

  assert(st.board === undefined && st.expectedBoard === undefined,
    "SHIPPED map: the stamp no longer claims a BOARD — that was the wrong dependency, and the " +
      "obvious 'fix' for the mismatch it produced (a board pin in the reader) would have taken the " +
      "pocket panel dark on every landing",
    "no board keys", JSON.stringify(Object.keys(st).filter(function (k) { return /board/i.test(k); })));
  assert(/PROVENANCE ONLY/.test(st._builtAgainstBoard_note || ""),
    "SHIPPED map: the board it was built against is retained but LABELLED as provenance, not a " +
      "dependency, so nobody checks it by mistake", "labelled", st._builtAgainstBoard_note || "(absent)");
})();

console.log("  " + "-".repeat(60));
console.log("  " + (n - fails) + "/" + n + " passed" + (fails ? "  (" + fails + " FAILED)" : ""));
process.exit(fails ? 1 : 0);
