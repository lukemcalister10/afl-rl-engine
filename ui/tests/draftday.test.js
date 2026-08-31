/* UI — unit tests for DRAFT DAY (ui/app/draftday.js core + ui/tools/gen_draft_outcomes.py output).
   Run:  node ui/tests/draftday.test.js      (exit 0 = all pass, exit 1 = a failure)

   TWO HALVES, ON THE ui/tests/pickvalue.test.js PATTERN:
     · SYNTHETIC — hand-built fixtures that pin the LAWS: what is excluded and why, what a
       denominator covers, what a quantile means, what the pin refuses.
     · SHIPPED — the same functions run against the committed record (ui/data_aux/draft_outcomes.js),
       asserting the structural facts the page's honesty rests on, and re-deriving from the raw
       store the two claims the page makes about its own population.

   EVERY ASSERT IS A RELATIONSHIP, NEVER A PINNED FIGURE. Nothing below says "232 never played" or
   "the maturity line is 4": both are true of today's store and neither is a law. What is asserted
   is the shape the page is allowed to draw — the selection partitions its input exactly, no rate
   is a percentage of a different denominator, the emitted maturity threshold follows from the
   emitted evidence, the record's own counts match a recount off the store, and a record that does
   not belong to the loaded board is refused. Those hold on every store or the page is lying. */

var fs = require("fs");
var path = require("path");
var DD = require("../app/draftday.js");
var core = DD.core;

var fails = 0, n = 0;
function ok(cond, label) {
  n++;
  if (cond) console.log("  [PASS] " + label);
  else { fails++; console.log("  [FAIL] " + label); }
}
function eq(got, want, label) {
  ok(JSON.stringify(got) === JSON.stringify(want), label + "  (got " + JSON.stringify(got) + ")");
}

function loadBundle(rel, globalName) {
  var p = path.join(__dirname, "..", rel);
  if (!fs.existsSync(p)) return null;
  var src = fs.readFileSync(p, "utf8");
  var sandbox = { window: {} };
  new Function("window", src)(sandbox.window);
  return sandbox.window[globalName] || null;
}

console.log("DRAFT DAY TESTS\n  " + "-".repeat(70));

/* ================================================================================================
   1. THE MATURITY RULE — a young player is not a failed one, and the line is derived
   ================================================================================================ */
console.log("\n  the maturity rule");

var ST = { seasonNow: 2026, maturitySeasons: 4 };
ok(core.classAge(ST, 2020) === 6, "a class drafted in 2020 has had six seasons by 2026");
ok(core.isMature(ST, 2022) === true, "a class with exactly the threshold's worth of seasons counts");
ok(core.isMature(ST, 2023) === false, "a class one season short does not");
ok(core.isMature(ST, 2025) === false, "last year's class is not judged at all");

/* The threshold is a function of the evidence, not a constant. Re-derived from a lag table here so
   a bundle whose stamp does not follow from its own table cannot pass unnoticed. */
var LAGS = [{ lag: 1, n: 600, cum: 0.60 }, { lag: 2, n: 280, cum: 0.88 },
            { lag: 3, n: 90, cum: 0.97 }, { lag: 4, n: 25, cum: 0.995 }];
ok(core.maturityFromLags(LAGS) === 4, "the threshold is the first lag reaching 99% of eventual debutants");
ok(core.maturityFromLags(LAGS, 0.85) === 2, "a different coverage bar moves the threshold, so it is genuinely derived");
ok(core.maturityFromLags([]) === 0, "no evidence yields no invented threshold");

/* ================================================================================================
   2. THE SELECTION — it partitions, it never drops
   ================================================================================================ */
console.log("\n  selection and the partition law");

function row(o) {
  return { k: o.k, n: o.k, p: o.p, y: o.y, dp: o.dp || "MID", g: o.g == null ? 0 : o.g,
           dl: o.dl == null ? null : o.dl, pk: o.pk == null ? null : o.pk, c: null, fp: "MID",
           ly: null, py: null, ret: false };
}
var FIX = [
  row({ k: "a", p: 10, y: 2010, g: 200, dl: 1, pk: 100 }),
  row({ k: "b", p: 10, y: 2015, g: 0 }),
  row({ k: "c", p: 11, y: 2016, g: 60, dl: 2, pk: 80 }),
  row({ k: "d", p: 12, y: 2024, g: 4, dl: 1 }),           // still-running class
  row({ k: "e", p: 12, y: 2025, g: 0 }),                  // still-running class, no debut
  row({ k: "f", p: 30, y: 2012, g: 120, dl: 1, pk: 90, dp: "RUCK" }),
];

var s1 = core.select(FIX, ST, { pick: 10, spread: 0, pos: null, mature: true });
eq(s1.set.map(function (r) { return r.k; }), ["a", "b"], "an exact pick selects only that ordinal");
eq([s1.lo, s1.hi], [10, 10], "and reports the ordinal window it actually used");

var s2 = core.select(FIX, ST, { pick: 11, spread: 2, pos: null, mature: true });
eq(s2.set.map(function (r) { return r.k; }), ["a", "b", "c"], "a neighbourhood widens the window");
eq(s2.young.map(function (r) { return r.k; }), ["d", "e"],
   "and the still-running classes inside that window are HELD OUT, not dropped");
ok(s2.set.length + s2.young.length ===
   FIX.filter(function (r) { return r.p >= 9 && r.p <= 13; }).length,
   "the two halves account for EVERY row in the window — the selection partitions, it never loses one");

var s3 = core.select(FIX, ST, { pick: 11, spread: 2, pos: null, mature: false });
eq(s3.set.map(function (r) { return r.k; }), ["a", "b", "c", "d", "e"],
   "with every class in, the young rows join the set rather than appearing twice");
ok(s3.young.length === 0, "and nothing is held out, so the two modes cannot double-count");

var s4 = core.select(FIX, ST, { pick: 30, spread: 5, pos: "RUCK", mature: true });
eq(s4.set.map(function (r) { return r.k; }), ["f"], "a position filter keys on the DRAFTED position");
var s5 = core.select(FIX, ST, { pick: 30, spread: 0, pos: "MID", mature: true });
ok(s5.set.length === 0 && s5.young.length === 0,
   "a filter with no matching career yields an EMPTY set — nothing is pooled in to fill it");

/* ================================================================================================
   3. THE RATES — one denominator, printed, and no threshold anywhere
   ================================================================================================ */
console.log("\n  the rates, and what they are rates OF");

var R = core.rates(s2.set, {});
ok(R.n === 3, "n is the size of the set the figures were computed on");
ok(R.never + R.played === R.n, "never-played and played PARTITION the set exactly");
ok(R.never === 1 && R.played === 2, "…and each side is the count it claims");
ok(R.g50 === 2 && R.g100 === 1, "the games milestones are counts over that same n, not over the players who played");
ok(R.nPeak === 2, "the best-season figure reports how many rows carry one, because not every career does");
ok(R.nLive === 0 && R.liveMed === null,
   "with no board values injected there is no survivorship figure at all — it is an argument, not a hidden read");

var Rlive = core.rates(s2.set, { a: 3000, c: 1000 });
ok(Rlive.nLive === 2 && Rlive.liveMed === 2000,
   "when board values ARE injected only the joined rows count, and the median is over those");
ok(Rlive.n === R.n, "…and injecting them does not change the denominator of any other figure");

/* the quantile is the ordinary linear interpolation, pinned so a later 'tidy-up' cannot quietly
   change what "median" and "quartile" mean on a page that prints both. */
ok(core.quantile([], 0.5) === null, "an empty set has no quantile, and does not return 0");
ok(core.quantile([5], 0.5) === 5, "one observation is its own median");
ok(core.quantile([1, 2, 3, 4], 0.5) === 2.5, "an even count interpolates between the middle two");
ok(core.quantile([1, 2, 3, 4], 0.25) === 1.75, "and the quartiles interpolate the same way");
ok(core.quantile([1, 2, 3], 0) === 1 && core.quantile([1, 2, 3], 1) === 3, "the ends are the ends");

/* NO VERDICTS. The page reports distributions because a "hit" needs a threshold and no ruling
   defines one. This asserts the absence, in the source, so a future edit that adds a hit rate has
   to delete a test that says why it must not. */
var SRC = fs.readFileSync(path.join(__dirname, "..", "app", "draftday.js"), "utf8");
var CODE = SRC.replace(/\/\*[\s\S]*?\*\//g, "").replace(/^\s*\/\/.*$/gm, "");
ok(!/hitRate|bustRate|isHit|isBust|grade/i.test(CODE),
   "no hit rate, bust flag or grade is computed anywhere in the view — a threshold is a ruling, and none exists");

/* ================================================================================================
   4. THE PIN — a record that does not belong to this board is refused
   ================================================================================================ */
console.log("\n  the pin (a mirror that does not name its identity is not a mirror)");

var FULL = "415929d3c9d561cc58bef00ae63432b2", OTHER = "0123456789abcdef0123456789abcdef";
ok(core.pinOf({ store: FULL }, { store_md5: FULL }).ok === true, "the same store passes");
ok(core.pinOf({ store: FULL }, { store_md5: OTHER }).ok === false, "a different store is refused");
ok(/regenerate with/.test(core.pinOf({ store: FULL }, { store_md5: OTHER }).why),
   "…and the refusal says what to do about it, naming both stores");
ok(core.pinOf({ store: FULL }, { store: FULL.slice(0, 8) }).ok === true,
   "the board's eight-character abbreviation is accepted as a prefix of the full digest");
ok(core.pinOf({ store: FULL }, { store: OTHER.slice(0, 8) }).ok === false,
   "…but only when it actually is one");
ok(core.pinOf(null, { store_md5: FULL }).ok === false, "an absent record is refused, not treated as empty");
ok(core.pinOf({}, { store_md5: FULL }).ok === false,
   "a record that names NO store is refused — it cannot be told apart from a stale one");

/* ================================================================================================
   5. THE PRICE SIDE — read off the curve, never invented
   ================================================================================================ */
console.log("\n  the price, read off the adopted curve");

var PVC = { "1": 3000, "2": 2600, "3": 2300, "64": 177, "65": 150 };
eq(core.priceRange(PVC, 1, 1), { lo: 3000, hi: 3000, n: 1 }, "one ordinal reads that ordinal");
eq(core.priceRange(PVC, 1, 3), { lo: 2300, hi: 3000, n: 3 }, "a window reads the range across it");
ok(core.priceRange(PVC, 100, 105) === null, "ordinals the curve does not carry yield NOTHING, never an extrapolation");
eq(core.priceRange(PVC, 2, 10), { lo: 2300, hi: 2600, n: 2 },
   "a partly-covered window reports only the ordinals that exist, and says how many they were");
ok(core.priceRange(null, 1, 5) === null, "no curve, no price");

/* ================================================================================================
   6. THE SHIPPED RECORD — its own claims, re-derived from the store
   ================================================================================================ */
console.log("\n  the shipped record (ui/data_aux/draft_outcomes.js)");

var B = loadBundle("data_aux/draft_outcomes.js", "__DRAFT_OUTCOMES__");
ok(!!B, "the record is committed and loads");

if (B) {
  var rows = B.rows, st = B.stamp;
  ok(rows.length === st.nRows, "the stamp's row count is the number of rows it ships");
  ok(rows.every(function (r) { return r.k && r.p > 0 && r.y > 0; }),
     "every row carries a key, an ordinal and a class — there are no half-rows");
  ok(rows.every(function (r) { return r.g > 0 ? r.dl != null : r.dl === null; }),
     "a debut lag exists exactly when the player played, and never otherwise");
  ok(rows.every(function (r) { return r.dl === null || r.dl >= 0; }),
     "no career begins before its own draft");
  ok(rows.filter(function (r) { return r.g === 0; }).length === st.nNeverPlayed,
     "the stamp's never-played count is the number of gameless rows it actually ships");

  /* THE ONE CLAIM EVERYTHING ELSE RESTS ON: the population is not survivor-filtered. Re-derived
     here from the RAW STORE rather than from the bundle, so the bundle cannot vouch for itself. */
  var storePath = path.join(__dirname, "..", "..", "engine", "rl_after", "rl_model_data.json");
  var store = JSON.parse(fs.readFileSync(storePath, "utf8"));
  var ndStore = store.filter(function (r) { return r.draft_stream === "ND" && r.stream_pick && r.stream_year; });
  ok(ndStore.length === rows.length,
     "the record holds EVERY national-draft selection in the store, not a filtered subset  (" +
     ndStore.length + " in the store, " + rows.length + " shipped)");
  /* THE RECOUNT SUMS THE SEASON ROWS, NOT THE TOP-LEVEL `games` FIELD, and that distinction is the
     defect this suite found. The scalar is a snapshot that stops being maintained once a player has
     a live season: every one of the store's players WITHOUT a 2026 season has games == the sum of
     his seasons, and most of those WITH one do not. Six men read games == 0 while their own season
     rows recorded football this year, which made "never played" false about players who had played.
     So the season rows are the record and the scalar is the copy — asserted both ways below, so
     neither the bundle nor this recount can drift onto the wrong one silently. */
  function careerGames(r) {
    return (r.scoring || []).reduce(function (a, s) { return a + (s.games || 0); }, 0);
  }
  var neverStore = ndStore.filter(function (r) { return careerGames(r) === 0; }).length;
  ok(neverStore === st.nNeverPlayed,
     "and the never-played count matches a recount off the store's SEASON ROWS  (" + neverStore + ")");
  var byStoreKey = {};
  ndStore.forEach(function (r) { byStoreKey[r.key] = r; });
  ok(rows.every(function (r) { return r.g === careerGames(byStoreKey[r.k]); }),
     "every shipped career-games figure is the sum of that player's own seasons");
  var scalarDisagrees = ndStore.filter(function (r) { return (r.games || 0) !== careerGames(r); }).length;
  ok(scalarDisagrees > 0,
     "the store's top-level `games` scalar DOES still disagree with the season rows for " +
     scalarDisagrees + " players — this test exists because reading it instead was the bug, and it " +
     "goes red if a future store makes the two agree, at which point this comment is what to read");
  ok(st.nNeverPlayed > 0,
     "busts ARE in the population — without this every rate on the page is survivorship fiction");

  /* the maturity threshold the bundle publishes must follow from the table it publishes with it. */
  ok(core.maturityFromLags(st.debutLagTable) === st.maturitySeasons,
     "the stamped maturity threshold is re-derivable from the stamped lag table  (" +
     st.maturitySeasons + " seasons)");
  var lastCum = st.debutLagTable[st.debutLagTable.length - 1].cum;
  ok(lastCum >= 0.99 && st.debutLagTable.every(function (t, i, a) {
       return i === 0 || t.cum >= a[i - 1].cum; }),
     "the lag table is a cumulative distribution: non-decreasing, and it reaches the bar");
  ok(st.debutLagN === st.debutLagTable.reduce(function (a, t) { return a + t.n; }, 0),
     "its own n is the sum of its buckets");

  /* class coverage: complete classes from pick 1 is what lets a base rate mean anything. */
  var byClass = {};
  rows.forEach(function (r) { (byClass[r.y] = byClass[r.y] || []).push(r.p); });
  ok(Object.keys(byClass).length === st.nClasses, "the stamp's class count is the number of classes present");
  ok(Object.keys(byClass).every(function (y) { return Math.min.apply(null, byClass[y]) === 1; }),
     "EVERY class starts at pick 1 — no class is a top-of-the-draft-only sample");
  ok(Object.keys(byClass).every(function (y) {
       var ps = byClass[y].slice().sort(function (a, b) { return a - b; });
       return ps.every(function (p, i) { return i === 0 || p > ps[i - 1]; });
     }), "and no ordinal is duplicated inside a class");

  /* the shipped record, driven through the same selection the page uses */
  var shipped = core.select(rows, st, { pick: 1, spread: 0, pos: null, mature: true });
  ok(shipped.set.length + shipped.young.length ===
     rows.filter(function (r) { return r.p === 1; }).length,
     "on the shipped record too, the selection partitions pick 1 exactly");
  ok(shipped.young.every(function (r) { return !core.isMature(st, r.y); }),
     "everything held out is held out for being young, and for no other reason");
  var SR = core.rates(shipped.set, {});
  ok(SR.never + SR.played === SR.n && SR.g100 <= SR.played && SR.g50 <= SR.played,
     "and its rates are coherent: the milestones cannot exceed the men who played");
  ok(SR.nPeak <= SR.played,
     "nor can more careers carry a best season than played a game");
}

console.log("\n  " + "-".repeat(70));
console.log(fails ? "DRAFT DAY TESTS: " + fails + " FAILED of " + n
                  : "DRAFT DAY TESTS: ALL " + n + " PASS");
process.exit(fails ? 1 : 0);
