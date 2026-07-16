/* UI v1.3 — unit tests for THE OWNER'S POSITIONAL COUNTING RULE (item 196(2)).
   Run:  node ui/tests/counting_rule.test.js      (exit 0 = all pass, exit 1 = a failure)
   Exercises the EXACT function the browser runs (ui/app/counting.js is dual-target). */
var C = require("../app/counting.js");

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
function assert(cond, label, want, got) { n++; report(!!cond, label, want, got); }
function report(ok, label, want, got) {
  if (ok) { console.log("  [PASS] " + label); }
  else { fails++; console.log("  [FAIL] " + label + "  want=" + want + " got=" + got); }
}
function sum(o) { return Object.keys(o).reduce(function (s, k) { return s + o[k]; }, 0); }

console.log("COUNTING-RULE TESTS (item 196(2))\n  " + "-".repeat(60));

// --- the owner's three verbatim cases ---------------------------------------------------------
eqWeights(C.positionWeights(["GEN_FWD"]), { GEN_FWD: 1 },
  "single position (non-mid) -> 1.0 to that position");
eqWeights(C.positionWeights(["MID"]), { MID: 1 },
  "single position (MID-only) -> 1.0 to MID");
eqWeights(C.positionWeights(["GEN_FWD", "KEY_FWD"]), { GEN_FWD: 0.5, KEY_FWD: 0.5 },
  "DPP, no mid -> 0.5 to each");
eqWeights(C.positionWeights(["MID", "GEN_FWD"]), { GEN_FWD: 1, MID: 0 },
  "DPP-mid EXCEPTION -> non-mid counts 1, MID counts 0");
eqWeights(C.positionWeights(["GEN_FWD", "MID"]), { GEN_FWD: 1, MID: 0 },
  "DPP-mid EXCEPTION (mid listed second) -> non-mid 1, MID 0");

// --- the value-conserving generalisation to 3-4 listed positions ------------------------------
eqWeights(C.positionWeights(["RUC", "GEN_FWD", "KEY_FWD"]), { RUC: 1 / 3, GEN_FWD: 1 / 3, KEY_FWD: 1 / 3 },
  "3 positions, no mid -> 1/3 to each");
eqWeights(C.positionWeights(["MID", "GEN_FWD", "GEN_DEF"]), { GEN_FWD: 0.5, GEN_DEF: 0.5, MID: 0 },
  "3 positions WITH mid -> 0.5 to each non-mid, MID 0");
eqWeights(C.positionWeights(["GEN_DEF", "KEY_DEF", "KEY_FWD", "GEN_FWD"]),
  { GEN_DEF: 0.25, KEY_DEF: 0.25, KEY_FWD: 0.25, GEN_FWD: 0.25 },
  "4 positions, no mid -> 1/4 to each");
eqWeights(C.positionWeights(["MID", "GEN_FWD", "KEY_FWD", "GEN_DEF"]),
  { GEN_FWD: 1 / 3, KEY_FWD: 1 / 3, GEN_DEF: 1 / 3, MID: 0 },
  "4 positions WITH mid -> 1/3 to each non-mid, MID 0");

// --- invariants -------------------------------------------------------------------------------
assert(approx(sum(C.positionWeights(["GEN_FWD", "KEY_FWD"])), 1), "weights sum to 1.0 (DPP)", "1", "see");
assert(approx(sum(C.positionWeights(["MID", "GEN_FWD"])), 1), "weights sum to 1.0 (DPP-mid)", "1", "see");
assert(approx(sum(C.positionWeights(["RUC", "GEN_FWD", "KEY_FWD"])), 1), "weights sum to 1.0 (3-pos)", "1", "see");
assert(Object.keys(C.positionWeights([])).length === 0, "no position -> empty (unattributed)", "{}", "see");
// dup tokens must not inflate weight
eqWeights(C.positionWeights(["GEN_FWD", "GEN_FWD"]), { GEN_FWD: 1 },
  "duplicate token collapses -> 1.0 (no double count)");

// --- value-conservation property over a synthetic mixed roster --------------------------------
(function () {
  var roster = [
    { codes: ["MID"], v: 8000 },
    { codes: ["GEN_FWD", "KEY_FWD"], v: 6000 },
    { codes: ["MID", "GEN_DEF"], v: 4000 },
    { codes: ["RUC", "GEN_FWD", "KEY_FWD"], v: 900 },
    { codes: ["GEN_DEF", "KEY_DEF", "KEY_FWD", "GEN_FWD"], v: 1200 },
  ];
  var bucket = {};
  var total = 0;
  roster.forEach(function (r) { C.accumulate(bucket, r.codes, r.v); total += r.v; });
  var distributed = sum(bucket);
  assert(approx(distributed, total),
    "roster: Sigma positional value == Sigma player value (conservation)", String(total), String(distributed));
})();

console.log("  " + "-".repeat(60));
console.log("  " + (n - fails) + "/" + n + " passed" + (fails ? "  (" + fails + " FAILED)" : ""));
process.exit(fails ? 1 : 0);
