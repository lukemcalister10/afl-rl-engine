/* UI — unit tests for the PICK VALUE view's pure logic (ui/app/pickvalue.js core).
   Run:  node ui/tests/pickvalue.test.js      (exit 0 = all pass, exit 1 = a failure)

   TWO HALVES, ON THE ui/tests/movers.test.js PATTERN:
     · SYNTHETIC — small hand-built fixtures that pin the LAWS: what parses, what fails closed, what
       is never rendered, what a sample count is allowed to claim.
     · SHIPPED — the same functions run against the committed production artifacts
       (ui/data/board_view_working.js `pvc` and ui/data_aux/v0.js `byKey`), asserting the structural
       facts the view's honesty rests on.

   EVERY ASSERT IS A RELATIONSHIP, NEVER A PINNED FIGURE. Not one line below says "pick 1 is 3,000"
   or "there are 272 filled cells": both are true of today's bake and false of the next one, and a
   test that fails on a legitimate re-bake teaches the next reader to delete it. What is asserted
   instead is the shape the view is allowed to draw — every rendered pick lies inside the curve's
   ruled domain; a printed sample size equals the observations actually behind it; a cell the data
   has nothing for stays empty; the counts partition the input exactly. Those hold on every bake or
   the view is lying, which is the only kind of failure worth waking somebody for. */

var fs = require("fs");
var path = require("path");
var PV = require("../app/pickvalue.js");
var core = PV.core;
var counting = require("../app/counting.js");

var fails = 0, n = 0;
function ok(cond, label) {
  n++;
  if (cond) console.log("  [PASS] " + label);
  else { fails++; console.log("  [FAIL] " + label); }
}
function eq(got, want, label) {
  ok(JSON.stringify(got) === JSON.stringify(want), label + "  (got " + JSON.stringify(got) + ")");
}

/* Load a `window.__NAME__ = {...};` generated bundle under node without a DOM. The view never does
   this — it reads the globals the page already loaded — but a test that validated a re-typed copy of
   the data would be validating the copy. */
function loadBundle(rel, globalName) {
  var p = path.join(__dirname, "..", rel);
  if (!fs.existsSync(p)) return null;
  var src = fs.readFileSync(p, "utf8");
  var sandbox = { window: {} };
  new Function("window", src)(sandbox.window);
  return sandbox.window[globalName] || null;
}

console.log("PICK VALUE VIEW TESTS\n  " + "-".repeat(70));

/* ================================================================================================
   1. parseSlot — the slot key is re-checked, never trusted
   ================================================================================================ */
console.log("\n  slot key (POSITION|AGE|PICK)");

eq(core.parseSlot("KPF|18|1"), { pos: "KPF", age: 18, pick: 1 }, "a well-formed slot parses to its three fields");
eq(core.parseSlot("MID|21|64"), { pos: "MID", age: 21, pick: 64 }, "the last ordinal in the ruled domain parses");
ok(core.parseSlot("MID|18") === null, "two fields is not a slot");
ok(core.parseSlot("MID|18|5|X") === null, "four fields is not a slot");
ok(core.parseSlot("|18|5") === null, "an empty position is not a slot");
ok(core.parseSlot("MID|x|5") === null, "a non-numeric age is not a slot");
ok(core.parseSlot("MID|18|x") === null, "a non-numeric pick is not a slot");
ok(core.parseSlot("MID|0|5") === null, "a zero draft age is not a slot");
ok(core.parseSlot(null) === null, "a null slot is not a slot");
ok(core.parseSlot(undefined) === null, "an absent slot is not a slot");
ok(core.parseSlot(5) === null, "a non-string slot is not a slot");
/* THE DOMAIN LAW, asserted at the parser so it cannot be forgotten downstream. */
ok(core.parseSlot("MID|18|0") === null, "pick 0 is outside the curve's domain and does not parse");
ok(core.parseSlot("MID|18|" + (core.CURVE_MAX + 1)) === null,
   "pick " + (core.CURVE_MAX + 1) + " is the POOL, not an ordinal, and does not parse as a pick");
ok(core.parseSlot("MID|18|999") === null, "a pick far past the curve does not parse");

/* ================================================================================================
   2. curve — the all-in column, and the pool that is never a pick
   ================================================================================================ */
console.log("\n  the all-in curve");

function mkPvc(over) {
  var p = {};
  for (var i = 1; i <= core.CURVE_MAX; i++) p[String(i)] = 1000 - i;   // shape only; no figure is asserted
  p[core.POOL_KEY] = 5;
  return Object.assign(p, over || {});
}

ok(!core.curve(null).ok, "a missing pvc fails closed");
ok(!core.curve(undefined).ok, "an undefined pvc fails closed");
ok(!core.curve({}).ok, "an empty pvc fails closed");
ok(core.curve(null).why && /pvc|curve/i.test(core.curve(null).why),
   "the failure names the artifact that is absent, rather than failing silently");
var poolOnly = {}; poolOnly[core.POOL_KEY] = 5;
ok(!core.curve(poolOnly).ok, "a pvc carrying ONLY the pool prices no pick and fails closed");
ok(core.curve(poolOnly).ordinals.length === 0, "...and offers no ordinal to render");

var full = core.curve(mkPvc());
ok(full.ok, "a complete curve is accepted");
eq(full.ordinals.length, core.CURVE_MAX, "a complete curve yields exactly one row per ruled ordinal");
ok(full.ordinals.every(function (o) { return o.n >= 1 && o.n <= core.CURVE_MAX; }),
   "RELATIONSHIP: every ordinal offered lies inside the ruled 1–" + core.CURVE_MAX + " domain");
ok(!full.ordinals.some(function (o) { return String(o.n) === core.POOL_KEY; }),
   "RELATIONSHIP: index " + core.POOL_KEY + " is NEVER offered as a pick ordinal");
ok(full.pool === 5, "the pool level is read, separately from the curve");

var holed = mkPvc(); delete holed["7"]; delete holed["40"];
var hc = core.curve(holed);
eq(hc.missing, [7, 40], "an unpriced ordinal is REPORTED as missing");
ok(!hc.ordinals.some(function (o) { return o.n === 7 || o.n === 40; }),
   "RELATIONSHIP: an unpriced ordinal is omitted, never interpolated from its neighbours");
eq(hc.ordinals.length, core.CURVE_MAX - 2, "...and the table is two rows shorter, not two guesses longer");

var noPool = mkPvc(); delete noPool[core.POOL_KEY];
ok(core.curve(noPool).ok && core.curve(noPool).pool === null,
   "a curve with no pool level still prices picks, and reports no pool rather than inventing one");

/* ================================================================================================
   3. index — the counts must account for every row handed in
   ================================================================================================ */
console.log("\n  indexing entry prices");

var ENTRIES = [
  { key: "a", slot: "MID|18|1", v0: 3400, origin: "pick-slot" },
  { key: "b", slot: "MID|18|1", v0: 3400, origin: "pick-slot" },   // same triple, same value
  { key: "c", slot: "MID|19|1", v0: 3100, origin: "pick-slot" },   // same (pos,pick), OTHER age
  { key: "d", slot: "KPF|18|1", v0: 2100, origin: "pick-slot" },
  { key: "e", slot: "MID|18|5", v0: 2200, origin: "pick-slot" },
  { key: "f", slot: null, v0: 258, origin: "entry-anchor" },       // a pool entrant: no ordinal
  { key: "g", slot: null, v0: null, origin: "unrecoverable" },     // no entry price at all
  { key: "h", slot: "MID|18|99", v0: 10, origin: "pick-slot" },    // outside the domain
  { key: "i", slot: "garbage", v0: 10, origin: "pick-slot" },      // unreadable
];
var IDX = core.index(ENTRIES);

eq(IDX.nUsed, 5, "only the rows that resolve to a numbered pick inside the domain are used");
eq(IDX.nNotPickSlot, 1, "a pool entrant is counted as not-a-pick-slot, not as missing data");
eq(IDX.nNoEntryPrice, 1, "a row with no recoverable entry price is counted");
eq(IDX.nBadSlot, 2, "an unreadable slot and an out-of-domain pick are counted as dropped");
ok(IDX.nUsed + IDX.nNotPickSlot + IDX.nNoEntryPrice + IDX.nBadSlot === ENTRIES.length,
   "RELATIONSHIP: the four counts PARTITION the input — every row handed in is accounted for exactly once");

eq(IDX.positions, ["KPF", "MID"], "the positions offered are exactly those the data carries");
eq(IDX.ages, [18, 19], "the draft ages offered are exactly those the data carries");
eq(IDX.modalAge, 18, "the default draft age is DERIVED as the modal one, not typed in");
eq(core.index([]).modalAge, null, "no data means no default age is claimed");
eq(core.index(null).nUsed, 0, "a null entry list indexes to nothing rather than throwing");
/* determinism: a tie must not depend on key order */
var tie = core.index([
  { key: "x", slot: "MID|21|3", v0: 1 }, { key: "y", slot: "MID|19|4", v0: 1 },
]);
eq(tie.modalAge, 19, "a tie on observation count breaks to the YOUNGER age, so the default is deterministic");

/* ================================================================================================
   4. cell — a printed sample may never overstate its evidence
   ================================================================================================ */
console.log("\n  grid cells");

var c18 = core.cell(IDX, "MID", 1, 18);
eq(c18.n, 2, "a cell's n is the count of observations actually used");
ok(!c18.aggregated && c18.lo === c18.hi && c18.v0 === c18.lo,
   "RELATIONSHIP: agreeing observations are not aggregated — lo === v0 === hi");
eq(c18.ages, [18], "RELATIONSHIP: a fixed-age cell contains ONLY that age's observations");

var cAll = core.cell(IDX, "MID", 1, null);
eq(cAll.n, 3, "pooling ages uses every observation at that (position, pick)");
ok(cAll.aggregated, "...and is marked aggregated when the pooled values disagree");
ok(cAll.lo < cAll.v0 && cAll.v0 < cAll.hi,
   "RELATIONSHIP: an aggregated cell's mean lies strictly inside the real range it reports");
eq(cAll.ages, [18, 19], "an aggregated cell reports every draft age it pooled");

ok(core.cell(IDX, "MID", 2, 18) === null,
   "RELATIONSHIP: a pick with no observation yields NOTHING, even though picks 1 and 5 have values");
ok(core.cell(IDX, "MID", 1, 22) === null, "a draft age the data does not carry yields nothing");
ok(core.cell(IDX, "RUCK", 1, 18) === null, "a position the data does not carry yields nothing");
ok(core.cell(IDX, null, 1, 18) === null, "no position selected yields no cell");
ok(core.cell(null, "MID", 1, 18) === null, "no index yields no cell");

ok(core.cell(IDX, "KPF", 1, 18).thin === true,
   "a cell resting on " + core.THIN_MAX + " or fewer careers is flagged thin");
ok(core.cell(IDX, "MID", 1, null).thin === (3 <= core.THIN_MAX),
   "RELATIONSHIP: thin is exactly n <= THIN_MAX, computed from the same n that is printed");

/* THE CENTRAL HONESTY ASSERT, stated as a relationship over the whole synthetic grid: for every
   (position, pick, age) the view could render, the n it would print equals the number of entries
   that actually match. A cell can never claim a sample it does not have. */
(function () {
  var bad = 0, checked = 0;
  IDX.positions.forEach(function (pos) {
    IDX.ages.concat([null]).forEach(function (age) {
      for (var pk = 1; pk <= core.CURVE_MAX; pk++) {
        var c = core.cell(IDX, pos, pk, age);
        var truth = ENTRIES.filter(function (e) {
          var s = core.parseSlot(e.slot);
          return s && e.v0 != null && s.pos === pos && s.pick === pk && (age == null || s.age === age);
        });
        checked++;
        if (truth.length === 0) { if (c !== null) bad++; continue; }
        if (!c || c.n !== truth.length) bad++;
      }
    });
  });
  ok(bad === 0, "RELATIONSHIP: over all " + checked + " synthetic (position, pick, age) cells, no cell " +
     "claims a sample it does not have and no empty cell materialises a value");
})();

/* ================================================================================================
   5. rows / coverage — what actually reaches the table
   ================================================================================================ */
console.log("\n  rendered rows");

var RS = core.rows(full, IDX, "MID", 18);
eq(RS.length, core.CURVE_MAX, "one row per priced ordinal");
ok(RS.every(function (r) { return r.n >= 1 && r.n <= core.CURVE_MAX; }),
   "RELATIONSHIP: every rendered pick is within the curve's domain");
ok(!RS.some(function (r) { return String(r.n) === core.POOL_KEY; }),
   "RELATIONSHIP: the pool index is never rendered as a pick row");
ok(RS.every(function (r) { return r.cell || r.delta === null; }),
   "RELATIONSHIP: no cell means NO delta — never a delta against a stood-in zero");
ok(RS.every(function (r) { return !r.cell || r.delta === r.cell.v0 - r.allIn; }),
   "RELATIONSHIP: the delta is exactly (position v0 − all-in), a difference of two given figures");
ok(RS.every(function (r) { return !r.cell || r.ratio === r.cell.v0 / r.allIn; }),
   "RELATIONSHIP: the ratio is exactly (position v0 / all-in)");
ok(RS.every(function (r) { return r.round === Math.ceil(r.n / core.ROUND_SIZE); }),
   "RELATIONSHIP: the round label follows the ruled " + core.ROUND_SIZE + "-pick round size");

var RS0 = core.rows(full, IDX, null, 18);
ok(RS0.every(function (r) { return r.cell === null && r.delta === null && r.ratio === null; }),
   "with no position selected the table is the all-in column alone");
ok(RS0.every(function (r) { return typeof r.allIn === "number"; }),
   "...and the all-in column is still fully populated");

var RSholed = core.rows(hc, IDX, "MID", 18);
ok(!RSholed.some(function (r) { return r.n === 7 || r.n === 40; }),
   "RELATIONSHIP: an ordinal the curve cannot price produces no row at all");

var COV = core.coverage(RS);
eq(COV.filled + COV.absent, COV.total, "RELATIONSHIP: coverage partitions the rows into filled and absent");
eq(COV.total, RS.length, "coverage counts exactly the rows drawn");
eq(COV.observations, RS.reduce(function (s, r) { return s + (r.cell ? r.cell.n : 0); }, 0),
   "RELATIONSHIP: the stated career count is the sum of the cells' own n, so the sentence cannot drift from the table");
ok(COV.thin <= COV.filled && COV.aggregated <= COV.filled,
   "RELATIONSHIP: thin and aggregated cells are subsets of the filled ones");
eq(core.coverage(RS0).filled, 0, "the all-in-only table claims no positional coverage");

/* ================================================================================================
   6. THE SHIPPED ARTIFACTS — the structural facts the view's honesty rests on
   ================================================================================================ */
console.log("\n  shipped artifacts");

var W = loadBundle("data/board_view_working.js", "__MATCHDAY_WORKING__");
var V = loadBundle("data_aux/v0.js", "__V0__");

if (!W || !V) {
  ok(false, "the shipped bundles load (ui/data/board_view_working.js, ui/data_aux/v0.js)");
} else {
  var SC = core.curve(W.pvc);
  ok(SC.ok, "the shipped board publishes a usable pick-value curve");
  eq(SC.missing, [], "RELATIONSHIP: the shipped curve prices every ordinal in the ruled domain (no holes to explain)");
  ok(SC.ordinals.every(function (o) { return o.n >= 1 && o.n <= core.CURVE_MAX; }),
     "RELATIONSHIP: every shipped ordinal lies inside the ruled domain");
  ok(SC.pool !== null, "the shipped curve carries a pool level");
  /* The pool is NOT the continuation of the curve — asserting it is genuinely a different object,
     which is why rendering it as a 65th pick would be a fabrication and not a rounding. */
  var lastV = SC.ordinals[SC.ordinals.length - 1].v;
  ok(SC.pool !== lastV, "RELATIONSHIP: the pool level is a distinct object from pick " + core.CURVE_MAX +
     "'s value, not a continuation of the curve");

  /* Build the shipped entry rows the way the view does — one per keyed row of the sidecar. */
  var shipped = Object.keys(V.byKey).map(function (k) {
    var r = V.byKey[k];
    return { key: k, slot: r.slot == null ? null : r.slot, v0: r.v0, origin: r.origin };
  });
  var SIDX = core.index(shipped);

  ok(SIDX.nUsed + SIDX.nNotPickSlot + SIDX.nNoEntryPrice + SIDX.nBadSlot === shipped.length,
     "RELATIONSHIP: every shipped sidecar row is accounted for exactly once across the four counts");
  eq(SIDX.nBadSlot, 0,
     "RELATIONSHIP: no shipped pick-slot row has a slot key this view cannot read — the format is as verified");

  /* Every row the sidecar calls a pick-slot must carry a readable slot, and every row it does NOT
     call a pick-slot must carry none. If that ever inverts, the view would be silently placing pool
     entrants on the pick axis (or dropping real picks), and no other assert here would catch it. */
  (function () {
    var wrong = shipped.filter(function (e) {
      var isPickSlot = e.origin === "pick-slot";
      var parses = core.parseSlot(e.slot) !== null;
      return isPickSlot !== parses;
    });
    ok(wrong.length === 0,
       "RELATIONSHIP: origin 'pick-slot' and a readable slot key agree on every shipped row (" +
       wrong.length + " disagreements)");
  })();

  /* THE TRIPLE INVARIANT — the fact that justifies the whole "single draft age aggregates nothing"
     design. If the surface ever carried two values for one (position, age, pick), the default view
     would be quietly averaging while telling the reader it was not. */
  (function () {
    var seen = {}, viol = 0;
    shipped.forEach(function (e) {
      var s = core.parseSlot(e.slot);
      if (!s || e.v0 == null) return;
      var k = s.pos + "|" + s.age + "|" + s.pick;
      if (seen[k] === undefined) seen[k] = e.v0;
      else if (seen[k] !== e.v0) viol++;
    });
    ok(viol === 0, "RELATIONSHIP: on the shipped surface each (position, draft age, pick) carries exactly " +
       "ONE entry price (" + Object.keys(seen).length + " triples, " + viol + " violations)");
  })();

  /* ...and therefore, through the actual rendering path: at a fixed draft age NOTHING is aggregated.
     Asserted through core.rows so it is the drawn table being checked, not a parallel derivation. */
  (function () {
    var aggAtFixedAge = 0, drawn = 0, outOfDomain = 0, overclaim = 0;
    SIDX.positions.forEach(function (pos) {
      SIDX.ages.forEach(function (age) {
        core.rows(SC, SIDX, pos, age).forEach(function (r) {
          drawn++;
          if (!(r.n >= 1 && r.n <= core.CURVE_MAX)) outOfDomain++;
          if (!r.cell) return;
          if (r.cell.aggregated) aggAtFixedAge++;
          /* no cell may claim a sample larger than the sidecar rows that match it */
          var truth = shipped.filter(function (e) {
            var s = core.parseSlot(e.slot);
            return s && e.v0 != null && s.pos === pos && s.age === age && s.pick === r.n;
          }).length;
          if (r.cell.n !== truth) overclaim++;
        });
      });
    });
    ok(outOfDomain === 0, "RELATIONSHIP: across every shipped position × draft age, all " + drawn +
       " rendered picks lie inside the curve's domain");
    ok(aggAtFixedAge === 0,
       "RELATIONSHIP: at a fixed draft age the shipped data aggregates NOTHING — every cell is the surface's own value");
    ok(overclaim === 0,
       "RELATIONSHIP: on shipped data no cell claims a sample it does not have (" + overclaim + " overclaims)");
  })();

  /* Pooling ages is the ONLY mode that aggregates, and it must not lose or duplicate observations:
     the all-ages cells of one position must hold exactly that position's readable pick-slot rows. */
  (function () {
    var bad = [];
    SIDX.positions.forEach(function (pos) {
      var got = 0;
      for (var pk = 1; pk <= core.CURVE_MAX; pk++) {
        var c = core.cell(SIDX, pos, pk, null);
        if (c) got += c.n;
      }
      var want = shipped.filter(function (e) {
        var s = core.parseSlot(e.slot);
        return s && e.v0 != null && s.pos === pos;
      }).length;
      if (got !== want) bad.push(pos + " " + got + "!=" + want);
    });
    ok(bad.length === 0, "RELATIONSHIP: pooling every draft age conserves the observations exactly — " +
       "no row counted twice, none dropped (" + bad.join(", ") + ")");
  })();

  /* An aggregated cell must always report a range that CONTAINS its mean and is genuinely wider than
     a point — otherwise the ≈ marker would be appearing on cells that averaged nothing. */
  (function () {
    var bad = 0, agg = 0;
    SIDX.positions.forEach(function (pos) {
      for (var pk = 1; pk <= core.CURVE_MAX; pk++) {
        var c = core.cell(SIDX, pos, pk, null);
        if (!c || !c.aggregated) continue;
        agg++;
        if (!(c.lo < c.hi && c.lo <= c.v0 && c.v0 <= c.hi && c.n >= 2)) bad++;
      }
    });
    ok(bad === 0, "RELATIONSHIP: every ≈ cell on shipped data reports a real, non-degenerate range " +
       "containing its mean (" + agg + " such cells, " + bad + " malformed)");
  })();

  /* The sparsity the page reports must be the sparsity of the table it drew — and it must be real
     sparsity, not a rendering accident: absent cells exist, and they are absent because no career
     stands behind them. */
  (function () {
    var anyAbsent = 0, mismatched = 0;
    SIDX.positions.forEach(function (pos) {
      var rs = core.rows(SC, SIDX, pos, null);
      var cov = core.coverage(rs);
      if (cov.filled + cov.absent !== cov.total) mismatched++;
      if (cov.observations !== rs.reduce(function (s, r) { return s + (r.cell ? r.cell.n : 0); }, 0)) mismatched++;
      anyAbsent += cov.absent;
    });
    ok(mismatched === 0, "RELATIONSHIP: the coverage sentence reconciles to the drawn rows for every shipped position");
    ok(anyAbsent > 0, "RELATIONSHIP: the shipped grid IS sparse — there are genuinely absent cells to show as absent");
  })();

  /* The positions the selector will offer are the board's own vocabulary. A code the sidecar carried
     that counting.js had never heard of would still render (by design), but it would mean the two
     halves of the estate had drifted, and the owner should be told. */
  (function () {
    var known = {};
    counting.POSITIONS.forEach(function (p) { known[p] = 1; });
    var unknown = SIDX.positions.filter(function (p) { return !known[p]; });
    ok(unknown.length === 0, "RELATIONSHIP: every entry position on the shipped surface is in the board's " +
       "own position vocabulary (ui/app/counting.js) — unknown: [" + unknown.join(", ") + "]");
  })();

  /* The draft age is an opaque label read off the slot, so the only thing to assert about it is that
     it is a usable label: present, positive, and that the derived default is one the data carries. */
  ok(SIDX.ages.length > 0 && SIDX.ages.every(function (a) { return a > 0; }),
     "the shipped surface carries usable draft-age labels");
  ok(SIDX.ageCount[SIDX.modalAge] > 0,
     "RELATIONSHIP: the DERIVED default draft age is one the shipped data actually carries");
  ok(SIDX.ages.every(function (a) { return SIDX.ageCount[a] <= SIDX.ageCount[SIDX.modalAge]; }),
     "RELATIONSHIP: the derived default is the modal draft age, by observation count");
}

console.log("\n  " + "-".repeat(70));
if (fails) { console.log("PICK VALUE TESTS: " + fails + " of " + n + " FAILED"); process.exit(1); }
console.log("PICK VALUE TESTS: ALL " + n + " PASS");
