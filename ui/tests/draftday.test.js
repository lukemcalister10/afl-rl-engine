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

var s1 = core.select(FIX, ST, { pick: 10, spread: 0, pos: null, minSeasons: 4 });
eq(s1.set.map(function (r) { return r.k; }), ["a", "b"], "an exact pick selects only that ordinal");
eq([s1.lo, s1.hi], [10, 10], "and reports the ordinal window it actually used");

var s2 = core.select(FIX, ST, { pick: 11, spread: 2, pos: null, minSeasons: 4 });
eq(s2.set.map(function (r) { return r.k; }), ["a", "b", "c"], "a neighbourhood widens the window");
eq(s2.young.map(function (r) { return r.k; }), ["d", "e"],
   "and the still-running classes inside that window are HELD OUT, not dropped");
ok(s2.set.length + s2.young.length ===
   FIX.filter(function (r) { return r.p >= 9 && r.p <= 13; }).length,
   "the two halves account for EVERY row in the window — the selection partitions, it never loses one");

var s3 = core.select(FIX, ST, { pick: 11, spread: 2, pos: null, minSeasons: 0 });
eq(s3.set.map(function (r) { return r.k; }), ["a", "b", "c", "d", "e"],
   "with every class in, the young rows join the set rather than appearing twice");
ok(s3.young.length === 0, "and nothing is held out, so the two modes cannot double-count");

var s4 = core.select(FIX, ST, { pick: 30, spread: 5, pos: "RUCK", minSeasons: 4 });
eq(s4.set.map(function (r) { return r.k; }), ["f"], "a position filter keys on the DRAFTED position");
var s5 = core.select(FIX, ST, { pick: 30, spread: 0, pos: "MID", minSeasons: 4 });
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
  /* EVERY SELECTION, LESS EXACTLY THE OWNER'S DECLARED EXCLUSIONS AND NOTHING ELSE. The bare
     equality this replaces was the stronger statement and would be the better test if the record
     were unfiltered — but it is filtered now, by an owner ruling, and a test loosened to `<=` would
     stop catching the thing it exists to catch. So the arithmetic is exact and the MISSING KEYS ARE
     NAMED: the shortfall must be the declared list, member for member. A survivor filter that crept
     in later would drop somebody who is not on that list, and this fails by name. */
  var declared = ((st.bustExcluded || []).map(function (e) { return e.key; })).sort();
  ok(ndStore.length - declared.length === rows.length,
     "the record holds EVERY national-draft selection in the store less the " + declared.length +
     " the owner struck out, and no others  (" + ndStore.length + " in the store, " +
     declared.length + " excluded, " + rows.length + " shipped)");
  var shipped = {};
  rows.forEach(function (r) { shipped[r.k] = 1; });
  var missing = ndStore.filter(function (r) { return !shipped[r.key]; })
                       .map(function (r) { return r.key; }).sort();
  ok(JSON.stringify(missing) === JSON.stringify(declared),
     "and the men who are missing are EXACTLY the men the ruling names — nobody has been quietly " +
     "filtered out alongside them", missing.join(", ") || "(none)");
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
  var shipped = core.select(rows, st, { pick: 1, spread: 0, pos: null, minSeasons: 4 });
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

/* ================================================================================================
   7. THE VALUE FRAME AND THE MIDFIELD YARDSTICK — the half that turns a table into a decision

   The board reads every cell in ONE currency: the midfielder pick it is worth. That conversion is
   what makes "a key forward at pick 5" and "a key defender at pick 5" comparable at all, so the
   properties below are the ones the whole surface rests on.
   ================================================================================================ */
console.log("\n  the BAKED bars (rl_model REPL / PEAK) and the midfield yardstick");

/* THE BARS ARE THE MODEL'S, NOT THIS PAGE'S — the property this block exists to pin.
   rl_model.py:824 carries REPL per position (v3.3, rl_replacement_derive.py, owner dial on KPF
   2026-07-04) and PEAK beside it. They have been baked for months and every surface measures
   against them.

   THIS SUITE PREVIOUSLY ASSERTED A FRAME THIS APP DERIVED FOR ITSELF, and that is what it was
   wrong to do. Twice: first off the best-23 slot law (a roster-shape rule, not a replacement
   level), then off the passmark. Both disagreed with the baked bar and the SF row — a derived 57.7
   against 70.9 — was enough to invert the small-forward reading on the board. What is asserted now
   is that NOTHING is derived: the bars arrive from the board, and a board that does not publish
   them yields no frame at all rather than a substitute. */

/* THE BAR IN USE IS REPL_BAR — the literal LESS the uniform drop the pricing core applies. The raw
   REPL is not what a player is measured against: dist_redesign.py:35-39 lowers every position by
   RL_REPL_DROP (3 in the declared config) and _merged_recover.py:495 applies it. Measuring against
   the literal would sit this page three points above every real bar, at every position, in the
   same direction — a small number and not a small error. */
var BOARD = { REPL: { MID: 80.1, KPF: 66.8 }, REPL_DROP: 3,
              REPL_BAR: { MID: 77.1, KPF: 63.8 }, PEAK: { MID: 92, KPF: 72 } };

ok(core.replOf(BOARD, "MID") === 77.1,
   "the bar is REPL_BAR — the literal 80.1 LESS the 3-point drop the pricing core applies");
ok(core.replBarIsEffective(BOARD) === true, "…and the page can tell that it is the effective bar");
ok(core.replOf({ REPL: { MID: 80.1 } }, "MID") === 80.1 &&
   core.replBarIsEffective({ REPL: { MID: 80.1 } }) === false,
   "a bundle predating REPL_BAR falls back to the literal AND reports that it is not effective, so " +
   "the page says so rather than implying the drop was applied");
ok(core.replOf(BOARD, "RUCK") === null,
   "a position the board does not publish a bar for reads null — never a stand-in number");
ok(core.replOf({}, "MID") === null && core.replOf(null, "MID") === null,
   "no board, no bar — and no throw");

/* VOR counts BUSTS AT ZERO, which is what makes it an expectation rather than a highlight reel: a
   position producing one star and nine nothings must score below one producing ten useful players,
   or the board would recommend lottery tickets. */
/* A fixture player: one real season at `v`, played in position `at` (defaulting to his drafted
   position). `s` is what frame() measures — (average, position played) per season. */
function pk(v, key, at) {
  var r = row({ k: key || ("x" + v + (at || "")), p: 10, y: 2010, g: 100, dl: 1, pk: v });
  r.s = (v == null) ? [] : [[v, at || "MID"]];
  return r;
}
var oneStar = [pk(160), pk(null, "a"), pk(null, "b"), pk(null, "c"), pk(null, "d")];
var allOk = [pk(95), pk(95, "o2"), pk(95, "o3"), pk(95, "o4"), pk(95, "o5")];
var fStar = core.frame(oneStar, BOARD, "MID"), fOk = core.frame(allOk, BOARD, "MID");
ok(Math.abs(fStar.vor - 16.58) < 1e-9 && Math.abs(fOk.vor - 17.9) < 1e-9,
   "VOR averages over EVERY selection with busts at zero, against the EFFECTIVE bar of 77.1",
   fStar.vor.toFixed(2) + " vs " + fOk.vor.toFixed(2));
ok(fStar.startable === 0.2 && fOk.startable === 1,
   "…so a one-star-in-five position is barely startable while a five-useful one always is",
   fStar.startable + " vs " + fOk.startable);

/* ===================== THE OWNER'S BAR RULE, IN HIS OWN TWO EXAMPLES =========================
   2026-08-31, verbatim: "A player drafted as a mid who then switched to SF mid career and scored
   95 over a 67 bar is +28, and that's credited to the midfield role he was drafted to. A player
   drafted as a KPF who switched to a mid mid career and scores 75 that season over a 77 bar
   doesn't contribute much even though the KPF bar is lower than his average."

   The bar is the position he PLAYED. The credit is the position he was DRAFTED as. These two cases
   are the whole rule, and the second is the one that catches a naive implementation: measured
   against his drafted KPF bar he would look eleven points clear; measured against the bar for the
   job he actually did, he is below it. */
var SIXBAR = { REPL_BAR: { MID: 77.1, SF: 67.9, KPF: 63.8, SD: 75.3, KPD: 65.4, RUCK: 75.5 },
               REPL_DROP: 3, REPL: { MID: 80.1, SF: 70.9, KPF: 66.8, SD: 78.3, KPD: 68.4, RUCK: 78.5 } };

var midPlayedFwd = core.frame([pk(95, "m1", "SF")], SIXBAR, "MID");
ok(Math.abs(midPlayedFwd.vor - 27.1) < 1e-9,
   "his case 1 — a MID-drafted player scoring 95 while playing SF is measured against SF's 67.9, " +
   "not MID's 77.1, and the +27.1 is credited to the MIDFIELD row",
   midPlayedFwd.vor.toFixed(1));
ok(midPlayedFwd.startable === 1, "…and he clears the bar he was actually playing against");

var kpfPlayedMid = core.frame([pk(75, "k1", "MID")], SIXBAR, "KPF");
ok(kpfPlayedMid.vor === 0 && kpfPlayedMid.startable === 0,
   "his case 2 — a KPF-drafted player scoring 75 while playing MID is BELOW MID's 77.1 and " +
   "contributes nothing, even though his own drafted KPF bar of 63.8 sits well under his average",
   kpfPlayedMid.vor + " / " + kpfPlayedMid.startable);
/* The naive implementation, stated so the difference is on the record rather than implied. */
var naive = 75 - SIXBAR.REPL_BAR.KPF;
ok(naive > 11 && kpfPlayedMid.vor === 0,
   "…where measuring him against his DRAFTED bar would have scored him +" + naive.toFixed(1) +
   " — the exact error the ruling exists to prevent");

/* A DUAL SEASON TAKES THE LOWER BAR — the engine's own collapse for a dual declaration
   (rl_model.py:85, min by REPL, "the LOWER REPL = more valuable for him"). */
ok(core.seasonBar(SIXBAR, "SF/MID") === 67.9, "a dual season takes the LOWER of the two bars (SF over MID)");
ok(core.seasonBar(SIXBAR, "KPF/RUCK") === 63.8, "…and again where the tall side is the cheaper one");
ok(core.seasonBar(SIXBAR, "MID") === 77.1, "a single-position season is just its own bar");
ok(core.seasonBar(SIXBAR, "NOPE") === null && core.seasonBar(SIXBAR, "") === null,
   "an unresolvable position yields NO bar, and the season is skipped rather than measured against " +
   "the drafted position's — missing evidence is not evidence of nothing");

/* cross-position seasons are COUNTED, so a row can say how much of it rests on the rule at all. */
var mixed = core.frame([pk(95, "a1", "SF"), pk(90, "a2", "MID")], SIXBAR, "MID");
ok(mixed.nCross === 1 && mixed.nMeasured === 2,
   "the frame reports how many careers included a season outside the drafted position",
   mixed.nCross + " of " + mixed.nMeasured);

/* ================== THE STAR LINE — the owner's ruled figure, and the bust count ==============
   His reasoning, 2026-08-31, and it is why the line is needed at all: value over replacement
   already carries magnitude continuously — "a great, say, 110 ppg mid, contributes 6x more to the
   retrospective value of their pick than an 85 mid does (if the bar was 80) as 30 is 6x 5". What a
   MEAN destroys is the shape. "What we probably don't get from that is bust % and bar clear % - we
   just get averaged results."

   His lines: 105 mid, 105 ruck, 97 SD, 92 SF, 85 KPD and KPF. A DECLARATION, not a derivation —
   published from docs/inputs/OWNER_STAR_SEASONS.json and read, never inferred. */
var STARBOARD = {
  REPL_BAR: { MID: 77.1, SF: 67.9, KPF: 63.8, SD: 75.3, KPD: 65.4, RUCK: 75.5 }, REPL_DROP: 3,
  REPL: { MID: 80.1, SF: 70.9, KPF: 66.8, SD: 78.3, KPD: 68.4, RUCK: 78.5 },
  STAR_BAR: { MID: 105, RUCK: 105, SD: 97, SF: 92, KPD: 85, KPF: 85 },
};
ok(core.starOf(STARBOARD, "MID") === 105 && core.starOf(STARBOARD, "KPF") === 85,
   "the star line is READ off the board, per position");
ok(core.starOf({}, "MID") === null, "no declaration, no star line");

/* THE OWNER'S POSITION RULE APPLIES TO THE CEILING EXACTLY AS IT DOES TO THE FLOOR: "a player who
   changes positions is measured against that season's bar, and if they clear it, it credits their
   original draft position for the success." */
var midStarredAsFwd = core.frame([pk(95, "s1", "SF")], STARBOARD, "MID");
ok(midStarredAsFwd.star === 1,
   "a MID-drafted player scoring 95 while playing SF STARS — 95 clears SF's line of 92 — and the " +
   "star is credited to the MIDFIELD row, not to the forwards");
var midNotStar = core.frame([pk(95, "s2", "MID")], STARBOARD, "MID");
ok(midNotStar.star === 0,
   "…while the same 95 played as a midfielder is NOT a star, because MID's line is 105. The same " +
   "score is a star in one role and ordinary in another, which is the entire point of per-position lines");

/* one star season is enough — a career is starred by its best year, not its average */
var oneGoodYear = core.frame([{ k: "g", p: 10, y: 2010, dp: "MID", g: 100,
                                s: [[70, "MID"], [108, "MID"], [72, "MID"]] }], STARBOARD, "MID");
ok(oneGoodYear.star === 1 && oneGoodYear.vor > 0,
   "one star season is enough — a career is starred by its best year, not by its mean");

/* BUST is "never produced a measurable season", NOT "never cleared the bar" — the latter is just
   the complement of the clear rate and would say nothing the clear rate does not. */
var mixedBust = core.frame([pk(95, "b1", "MID"), pk(null, "b2"), pk(50, "b3", "MID")], STARBOARD, "MID");
ok(Math.abs(mixedBust.bust - 1 / 3) < 1e-9,
   "bust is the share who never produced a measurable season — one of three here",
   mixedBust.bust.toFixed(3));
ok(mixedBust.startable === 1 / 3 && mixedBust.bust === 1 / 3,
   "…and it is NOT the complement of the clear rate: the 50-scorer played and did not clear, so he " +
   "is neither a bust nor a clear", mixedBust.startable + " / " + mixedBust.bust);

/* a dual season takes the LOWER star line, matching the lower floor — one job, one story */
ok(core.seasonStar(STARBOARD, "SF/MID") === 92 && core.seasonBar(STARBOARD, "SF/MID") === 67.9,
   "a dual season takes the LOWER star line as well as the lower floor, so both describe one job");

/* with no declaration the board draws NO star column rather than a default */
var noStar = core.frame([pk(95, "n1", "MID")], { REPL_BAR: { MID: 77.1 } }, "MID");
ok(noStar.star === null && noStar.bust === 0,
   "with no star line declared the frame reports null — the column disappears, it does not default");

ok(core.frame([pk(95)], { REPL: {}, REPL_BAR: {} }, "MID") === null,
   "no baked bar, no frame — the page shows nothing rather than measuring against something invented");
ok(core.frame([], BOARD, "MID") === null, "and no careers, no frame");

var atRepl = core.frame([pk(77.1, "atbar", "MID")], BOARD, "MID");
ok(atRepl.vor === 0 && atRepl.startable === 1,
   "a player exactly at the bar counts as startable and adds ZERO value over it",
   atRepl.vor + " / " + atRepl.startable);

/* THE YARDSTICK. Nearest match, and honest at both ends rather than clamping in silence. */
var CURVE = [{ p: 1, vor: 20 }, { p: 10, vor: 15 }, { p: 30, vor: 8 }, { p: 60, vor: 3 }];
eq(core.midEquivalent(CURVE, 15), { p: 10, beyond: null, vor: 15 },
   "a value on the curve reads its own pick");
ok(core.midEquivalent(CURVE, 14).p === 10, "and a value between two picks reads the nearer one");
ok(core.midEquivalent(CURVE, 25).beyond === "above",
   "a value richer than the best midfielder says it is ABOVE the scale, not 'mid 0'");
ok(core.midEquivalent(CURVE, 1).beyond === "below",
   "and one poorer than the deepest says it is BELOW it, rather than being clamped in silence");
ok(core.midEquivalent([], 10) === null && core.midEquivalent(CURVE, null) === null,
   "no curve or no value yields no equivalence");

/* the careers selector the board's cells are cut with — the window is a control, never a smoothing */
var VST = { seasonNow: 2026, maturitySeasons: 4 };
var WROWS = [row({ k: "m1", p: 10, y: 2010, g: 50, pk: 90 }),
             row({ k: "m2", p: 18, y: 2010, g: 50, pk: 90 }),
             row({ k: "m3", p: 10, y: 2025, g: 0 }),
             row({ k: "f1", p: 10, y: 2010, g: 50, pk: 90, dp: "KPF" })];
ok(core.careers(WROWS, VST, "MID", 10, 0, 4).length === 1, "a zero-width window is exactly the ordinal");
ok(core.careers(WROWS, VST, "MID", 10, 8, 4).length === 2, "…and widening it pools the neighbours");
ok(core.careers(WROWS, VST, "MID", 10, 8, 4).every(function (r) { return r.dp === "MID"; }),
   "…and never crosses positions");
ok(core.careers(WROWS, VST, "MID", 10, 8, 0).length === 3,
   "with every class in, the still-running rows join the window too");

/* ---- THE SHIPPED BARS: the board publishes them, and NOTHING derives them --------------------- */
(function () {
  var bsrc = fs.readFileSync(path.join(__dirname, "..", "data", "board_view_working.js"), "utf8");
  var bd = JSON.parse(bsrc.slice(bsrc.indexOf("{"), bsrc.lastIndexOf("}") + 1));
  var POS6 = ["MID", "RUCK", "SF", "KPF", "SD", "KPD"];
  ok(bd.REPL && bd.PEAK, "the shipped bundle publishes the baked REPL and PEAK");
  ok(POS6.every(function (p) { return typeof bd.REPL[p] === "number" && bd.REPL[p] > 0; }),
     "…for all six positions", JSON.stringify(bd.REPL));

  /* THE DROP COMES FROM THE DECLARED CONFIG, NOT A CODE DEFAULT. data/model_config.json is the
     manifest this board was built under (pinned by the release contract's config_sha256);
     dist_redesign's literal '3' is only what an unset environment gives you. Reading the default
     would be right today for the wrong reason and wrong the first time a board moves the dial. */
  var cfgPath = path.join(__dirname, "..", "..", "data", "model_config.json");
  var cfg = JSON.parse(fs.readFileSync(cfgPath, "utf8"));
  var declaredDrop = parseFloat((cfg.vars || {}).RL_REPL_DROP);
  ok(!isNaN(declaredDrop),
     "the declared model config publishes RL_REPL_DROP under `vars`", String(declaredDrop));
  ok(bd.REPL_DROP === declaredDrop,
     "the bundle's drop IS the declared one — not the code default, not a typed 3",
     bd.REPL_DROP + " vs " + declaredDrop);
  ok(POS6.every(function (p) { return Math.abs(bd.REPL_BAR[p] - (bd.REPL[p] - declaredDrop)) < 1e-9; }),
     "and REPL_BAR is exactly REPL minus that drop at every position",
     JSON.stringify(bd.REPL_BAR));
  ok(POS6.every(function (p) { return core.replOf(bd, p) === bd.REPL_BAR[p]; }),
     "…and the page measures against REPL_BAR, never the raw literal");
  /* AGAINST THE ENGINE ITSELF, not against a copy. If rl_model's REPL is ever re-derived, this
     goes red until the board is rebuilt and republished — which is the whole point of not holding
     a second copy anywhere. */
  var eng = fs.readFileSync(path.join(__dirname, "..", "..", "engine", "rl_after", "rl_model.py"), "utf8");
  var m = /^REPL=\{([^}]*)\}/m.exec(eng);
  ok(!!m, "rl_model.py declares REPL as a literal this test can read");
  if (m) {
    var engRepl = {};
    m[1].split(",").forEach(function (kv) {
      var pr = kv.split(":");
      engRepl[pr[0].replace(/['"\s]/g, "")] = parseFloat(pr[1]);
    });
    ok(POS6.every(function (p) { return Math.abs(engRepl[p] - bd.REPL[p]) < 1e-9; }),
       "and the SHIPPED bars are byte-equal to the engine's own REPL — the app holds no second copy",
       JSON.stringify(engRepl));
  }
  /* A CORRECTION I OWE THE RECORD. This block previously asserted that PEAK sits BELOW REPL at two
     positions and concluded PEAK could not be a ceiling. That comparison was against the RAW
     LITERAL. Against the bar the engine actually prices with — REPL_BAR, the literal less the
     3-point drop — PEAK is above at EVERY position:

         MID  bar 77.1  PEAK 92     RUCK bar 75.5  PEAK 92
         SD   bar 75.3  PEAK 78     SF   bar 67.9  PEAK 70
         KPD  bar 65.4  PEAK 70     KPF  bar 63.8  PEAK 72

     So the "ceiling below the floor" finding was an artefact of my own wrong bar, and it is
     asserted the right way round here instead. PEAK is a reference peak level per position — the
     denominator of the elite ramp at rl_model.py:1170, `elite = clamp((lp/PEAK[g] - 0.97)/0.30)`
     — and it lives in params.json beside PEAK_AGE as part of the age-curve machinery.

     It is STILL not used as a star bar on this page, but for a different and better reason: at SF
     the elite onset (0.97 x 70 = 67.9) is EXACTLY the replacement bar (67.9), and at SD it is 0.4
     above it. For two of six positions "elite" would begin at the floor. Pending an owner ruling,
     no ceiling is drawn. */
  var barOf = function (p) { return bd.REPL_BAR ? bd.REPL_BAR[p] : bd.REPL[p]; };
  ok(POS6.every(function (p) { return bd.PEAK[p] > barOf(p); }),
     "PEAK sits ABOVE the EFFECTIVE bar at every position — the earlier 'ceiling below the floor' " +
     "reading compared it against the raw literal and was wrong",
     POS6.map(function (p) { return p + " " + barOf(p) + "/" + bd.PEAK[p]; }).join(" "));
  var degenerate = POS6.filter(function (p) { return 0.97 * bd.PEAK[p] - barOf(p) < 1; });
  ok(degenerate.length > 0,
     "…but the elite onset (0.97 x PEAK, rl_model.py:1170) collapses onto the bar at " +
     degenerate.join(", ") + ", which is why no star line is drawn from it without a ruling");

  /* THE SHIPPED STAR LINE IS THE OWNER'S DECLARED ONE, byte-for-byte — no default, no rounding,
     no second copy in the app. If the declaration moves, this goes red until the bundle is
     republished, which is the only way a ruled constant stays ruled. */
  var starPath = path.join(__dirname, "..", "..", "docs", "inputs", "OWNER_STAR_SEASONS.json");
  ok(fs.existsSync(starPath), "the owner's star declaration is committed");
  if (fs.existsSync(starPath)) {
    var starDoc = JSON.parse(fs.readFileSync(starPath, "utf8"));
    ok(!!starDoc.owner_word,
       "…and it carries his own words, so a ruled constant cannot be told apart from a guess");
    ok(POS6.every(function (p) { return bd.STAR_BAR[p] === starDoc.star[p]; }),
       "…and the bundle publishes exactly those figures", JSON.stringify(bd.STAR_BAR));
    ok(POS6.every(function (p) { return bd.STAR_BAR[p] > barOf(p); }),
       "every star line sits above its own replacement bar — unlike PEAK, which does not");
  }

  if (B) {
    var shippedCurve = core.midCurve(B.rows, B.stamp, bd, 8, 4);
    ok(shippedCurve.length > 50,
       "the shipped record supports a midfield yardstick across the curve", shippedCurve.length + " ordinals");
    ok(shippedCurve.every(function (c, i, a) { return i === 0 || a[i - 1].vor >= c.vor - 3; }),
       "…and it descends with the ordinal (within noise) — a yardstick that rose late is not a ruler");
    var priced = POS6.filter(function (pos) {
      var f = core.frame(core.careers(B.rows, B.stamp, pos, 10, 8, 4), bd, pos);
      return f && core.midEquivalent(shippedCurve, f.vor);
    });
    ok(priced.length === 6, "all six positions price against the yardstick at pick 10", priced.join(","));
  }
})();

/* THE GENERATOR HOLDS NO BAR EITHER. The outcome record emits career facts only; the moment it
   starts publishing a replacement level again, this goes red. */
(function () {
  var gen = fs.readFileSync(path.join(__dirname, "..", "tools", "gen_draft_outcomes.py"), "utf8");
  var code = gen.replace(/"""[\s\S]*?"""/g, "").replace(/^\s*#.*$/gm, "");
  ok(!/STARTING_SLOTS|STAR_RANK|_repl_levels|_star_bar/.test(code),
     "the outcome generator derives NO replacement level and NO star bar — it emits career facts " +
     "only, and the measuring happens where the baked bars live");
  ok(B && B.stamp.repl === undefined && B.stamp.starBar === undefined,
     "…and the shipped record carries no such field either");
})();

/* ================================================================================================
   8. TWO QUESTIONS, TWO THRESHOLDS — the defect this suite exists to prevent recurring

   The bundle's `maturitySeasons` (4) was derived for ONE question: has he debuted. 99% of eventual
   debutants have by then. It was then reused to gate the PEAK questions, and that was wrong —
   measured on this record, only 31% of first-star seasons have arrived by four seasons, 91% by
   eleven. The cost was not academic: star rate read 15.3% against a fully-run 17.0%, the error was
   three times worse at picks 41-64 than at 1-10 (late picks develop slowly), and it INVERTED the
   headline — rucks lead midfielders on star rate at four seasons, midfielders lead at twelve.

   So the peak threshold is derived separately, from first-star lags rather than debut lags, and
   `careers` now takes an explicit minimum instead of a boolean that silently meant four.
   ================================================================================================ */
console.log("\n  the peak threshold — a debut rule must never gate a peak question again");

var RUNSTAMP = { seasonNow: 2026, maturitySeasons: 4 };
ok(core.hasRun(RUNSTAMP, 2015, 11) === true, "a class with eleven seasons has had a full run");
ok(core.hasRun(RUNSTAMP, 2016, 11) === false, "…and one with ten has not");
ok(core.hasRun(RUNSTAMP, 2025, 0) === true, "a minimum of zero admits every class");

/* the threshold is DERIVED from first-star lags, and it moves with the coverage asked for */
var STARROWS = [];
for (var q = 0; q < 20; q++) {
  // ten careers starring at +4, ten at +10 — so 50% coverage lands at 4 and 100% at 10
  STARROWS.push({ k: "e" + q, p: 10, y: 2005, dp: "MID",
                  s: [[110, "MID", 2005 + (q < 10 ? 4 : 10)]] });
}
var d90 = core.developedFromRows(STARROWS, RUNSTAMP, { STAR_BAR: { MID: 105 } }, 0.9, core.seasonStar);
var d50 = core.developedFromRows(STARROWS, RUNSTAMP, { STAR_BAR: { MID: 105 } }, 0.5, core.seasonStar);
ok(d90.lag === 10 && d50.lag === 4,
   "the threshold is the lag by which the asked-for share of first-star seasons has landed — 90% " +
   "needs ten seasons here, 50% needs four", d50.lag + " / " + d90.lag);
ok(d90.n === 20, "…measured over the careers that actually starred", String(d90.n));
ok(core.developedFromRows([], RUNSTAMP, { STAR_BAR: {} }, 0.9, core.seasonStar) === null,
   "no star seasons to measure yields NO threshold — the page falls back and says so rather than " +
   "inventing a number");
/* classes without a long run may not TEACH the threshold, or the measurement is contaminated by
   the very immaturity it exists to detect. */
var YOUNG = [{ k: "y", p: 10, y: 2024, dp: "MID", s: [[110, "MID", 2025]] }];
ok(core.developedFromRows(YOUNG, RUNSTAMP, { STAR_BAR: { MID: 105 } }, 0.9, core.seasonStar) === null,
   "and a class too young to have finished cannot teach the threshold it would bias");

/* THE DEFECT ITSELF, on the shipped record: the two thresholds must differ, and the peak one must
   be the longer. If a future store makes them equal this goes red and the reasoning gets re-read. */
if (B) {
  var bsrc2 = fs.readFileSync(path.join(__dirname, "..", "data", "board_view_working.js"), "utf8");
  var bd2 = JSON.parse(bsrc2.slice(bsrc2.indexOf("{"), bsrc2.lastIndexOf("}") + 1));
  var dev = core.developedFromRows(B.rows, B.stamp, bd2, 0.9, core.seasonStar);
  ok(dev && dev.lag > B.stamp.maturitySeasons,
     "on the shipped record the PEAK threshold (" + (dev && dev.lag) + " seasons) is longer than " +
     "the DEBUT threshold (" + B.stamp.maturitySeasons + ") — a peak takes longer to arrive than a " +
     "debut, and gating one with the other is the defect this block prevents");

  /* and the bias is real and directional: measured on the shipped record, the loose population
     understates late picks more than early ones. Asserted as a RELATIONSHIP, not a figure. */
  function starRate(minSeasons, lo, hi) {
    var set = (B.rows || []).filter(function (r) {
      return r.p >= lo && r.p <= hi && core.hasRun(B.stamp, r.y, minSeasons) && bd2.REPL_BAR[r.dp];
    });
    var f = null, tot = 0, n = 0;
    ["MID", "RUCK", "SF", "KPF", "SD", "KPD"].forEach(function (pos) {
      var sub = set.filter(function (r) { return r.dp === pos; });
      if (!sub.length) return;
      f = core.frame(sub, bd2, pos);
      tot += f.star * sub.length; n += sub.length;
    });
    return n ? tot / n : 0;
  }
  var lateLoose = starRate(B.stamp.maturitySeasons, 41, 64), lateRun = starRate(dev.lag, 41, 64);
  var earlyLoose = starRate(B.stamp.maturitySeasons, 1, 10), earlyRun = starRate(dev.lag, 1, 10);
  ok(lateRun > lateLoose && earlyRun > earlyLoose,
     "the loose population understates the star rate at BOTH ends of the draft",
     (100 * lateLoose).toFixed(1) + "->" + (100 * lateRun).toFixed(1) + " late, " +
     (100 * earlyLoose).toFixed(1) + "->" + (100 * earlyRun).toFixed(1) + " early");
  ok((lateRun - lateLoose) / lateLoose > (earlyRun - earlyLoose) / earlyLoose,
     "…and it understates LATE picks proportionally more than early ones, which is why the default " +
     "is the fully-run population: the bias runs in the direction of the trade-down decision");
}

/* ================================================================================================
   9. THE HOUSE'S OWN PARAMETERS — pinned against their source, not retyped

   The owner asked whether this work had looked at what the estate already derived, or invented its
   own. It had invented its own. The ruled pick curve's evidence panel carries a declared basis for
   nearly every choice this page had made independently:

       session_2026-07-30/item279/panel/harness_pvc.py
         YR_LO       = 2004   the class floor — the store's earliest season is 2005, so the 2003
                              class has no observable year one and every lag measured on it is late
         QUAL_GAMES  = 6      the establishment threshold, and never_established() is the estate's
                              own bust definition — the one the curve was TAUGHT with
         MIN_STRATUM = 20     the size below which a cell is not a stratum worth reading

   Measured cost of having chosen instead of looked: a 10-game establishment bar called 32.4% of
   selections busts where the house's 6-game bar calls 23.7% — nine points on a headline figure.

   These assertions READ THE HOUSE FILE. If the estate moves a parameter, this suite goes red and
   the board is brought back into line, instead of the two drifting apart in silence.
   ================================================================================================ */
console.log("\n  the house's ruled parameters, read from their source");
(function () {
  var hp = path.join(__dirname, "..", "..", "session_2026-07-30", "item279", "panel", "harness_pvc.py");
  if (!fs.existsSync(hp)) {
    ok(true, "the #279 evidence panel is not in this checkout — the house parameters cannot be pinned here");
    return;
  }
  var src = fs.readFileSync(hp, "utf8");
  function decl(name) {
    var m = new RegExp("^" + name + "\\s*=\\s*(\\d+)", "m").exec(src);
    return m ? parseInt(m[1], 10) : null;
  }
  var YR_LO = decl("YR_LO"), QUAL = decl("QUAL_GAMES"), STRAT = decl("MIN_STRATUM");
  ok(YR_LO === 2004, "the house declares YR_LO = 2004 (the 2003 class has no observable year one)", String(YR_LO));
  ok(QUAL === 6, "the house declares QUAL_GAMES = 6 as its establishment threshold", String(QUAL));
  ok(STRAT === 20, "the house declares MIN_STRATUM = 20", String(STRAT));

  /* and the page must be USING them, not merely aware of them */
  ok(core.THIN_MAX === STRAT,
     "the board's thin-sample bar IS the house's minimum stratum, not a number this page picked",
     core.THIN_MAX + " vs " + STRAT);

  var gen = fs.readFileSync(path.join(__dirname, "..", "tools", "gen_draft_outcomes.py"), "utf8");
  var m = /^REAL_SEASON_GAMES = (\d+)/m.exec(gen);
  ok(m && parseInt(m[1], 10) === QUAL,
     "the record's establishment threshold IS the house's QUAL_GAMES, so a season counts here " +
     "exactly when it counts for the curve that taught the prices",
     m && m[1]);

  var app = fs.readFileSync(path.join(__dirname, "..", "app", "draftday.js"), "utf8");
  var y = /var YR_LO = (\d+);/.exec(app);
  ok(y && parseInt(y[1], 10) === YR_LO,
     "and the board's class floor IS the house's YR_LO", y && y[1]);
})();

/* THE RULED BUST EXCLUSION — NOW APPLIED, ON THE OWNER'S WORD.
   ENGINE_PRIMER §4.5 has carried it for months: "Paddy McCartin and Tom Boyd (pick-1 KPF busts,
   force majeure) are excluded by owner ruling; every player in their drafts slides up one pick."
   Nothing ever applied it — measured 2026-09-01, no store row carried `_pvc_exclude` and both men
   sat in this record at pick 1 unslid. Owner, on being shown that: "McCartin and Boyd should be
   excluded from everything. It's as if they weren't picked ... For your draft day analytics, they
   didn't happen."

   THE LIST IS DECLARED ONCE, in engine/rl_after/rl_model.py, and read from there by the generator.
   These assertions read the ENGINE'S declaration too, so a test that agreed with a stale local copy
   is not possible: if the curve's exclusion list moves, this test moves with it or fails. */
(function () {
  var declPath = path.join(__dirname, "..", "..", "docs", "inputs", "OWNER_BUST_EXCLUSION.json");
  var decl = null;
  try { decl = JSON.parse(fs.readFileSync(declPath, "utf8")); } catch (e) { decl = null; }
  ok(!!decl, "the owner's exclusion declaration exists at docs/inputs/OWNER_BUST_EXCLUSION.json");
  var keys = ((decl || {}).exclude || []).map(function (e) { return e.key; }).sort();
  ok(keys.length === 2 && keys.indexOf("thomas-boyd") >= 0 && keys.indexOf("paddy-mccartin") >= 0,
     "and it names the two force-majeure pick-1 KPF busts of ENGINE_PRIMER §4.5", keys.join(", "));

  var gen = fs.readFileSync(path.join(__dirname, "..", "tools", "gen_draft_outcomes.py"), "utf8");
  ok(/OWNER_BUST_EXCLUSION/.test(gen) && !/'paddy-mccartin'/.test(gen),
     "the generator READS that declaration and keeps no copy of its own — one source, so the list " +
     "cannot be changed in one place and honoured in another");

  /* WHERE THE RULING IS ALREADY APPLIED, ASSERTED SO IT CANNOT QUIETLY STOP BEING TRUE.
     The v0 pick surface's shipped lane (#306, RL_V0_LENS default '1') does not fit over the roster —
     it fits over a declared basis that inherits "McCartin/Boyd exclusions and one-pick slides as the
     committed matrix carries them". This was reported wrongly once, by reading the A/B control lane
     (RL_V0_LENS=0, the pre-#306 free fit) as if it shipped. The assertion below is the check that
     should have been run then: it reads the basis and asserts BOTH the absence and the slide. */
  var basis = null;
  try {
    basis = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "..", "docs", "evidence",
      "exec_306_zlaarm", "basis", "structural_basis_279.json"), "utf8"));
  } catch (e) { basis = null; }
  ok(!!basis, "the v0 lens basis artifact is present — it is what teaches the shipped v0 surface");
  if (basis) {
    var bk = {};
    basis.rows.forEach(function (r) { bk[r.key] = r; });
    keys.forEach(function (k) {
      ok(!bk[k], "  " + k + " is absent from the v0 lens basis, so the v0 KPF surface does not learn " +
         "from him", basis.rows.length + " rows");
    });
    /* AND THE SLIDE IS IN THE BASIS TOO, which is the half that proves it is the ruling being applied
       rather than two rows happening to be missing. Josh Kelly was the second name called in 2013 and
       Petracca the second in 2014; with the first struck out, both are pick 1 in the basis. */
    [["joshua-kelly", 1], ["christian-petracca", 1], ["marcus-bontempelli", 3]].forEach(function (t) {
      ok(bk[t[0]] && bk[t[0]].pick === t[1],
         "  " + t[0] + " sits at pick " + t[1] + " in the v0 basis — the same one-pick slide this " +
         "board applies", bk[t[0]] && bk[t[0]].pick);
    });
  }

  /* AND THE LAST HOLE, NOW CLOSED (landed 2026-09-01 on the owner's word). rl_model.py had read
     `_pvc_exclude` for months with nothing setting it; the live v3.4 fit was the only place on the
     estate where the ruling was not applied. It now sets the flag, and the engine's list must be the
     SAME LIST as the owner's declaration — the two live in different files for a reason (rl_model.py
     is md5-pinned and carries the value path; the JSON is the owner's word), so this binds them. */
  var eng = fs.readFileSync(path.join(__dirname, "..", "..", "engine", "rl_after", "rl_model.py"), "utf8");
  var m = /^BUST_EXCLUDE_KEYS\s*=\s*\(([^)]*)\)/m.exec(eng);
  ok(!!m, "the engine declares BUST_EXCLUDE_KEYS — the live pick-value fit applies the ruling");
  var engKeys = m ? (m[1].match(/'([^']+)'/g) || []).map(function (q) { return q.slice(1, -1); }).sort() : [];
  ok(JSON.stringify(engKeys) === JSON.stringify(keys),
     "and the engine's list is EXACTLY the owner's declaration — one ruling, two files, bound here so " +
     "they cannot drift", engKeys.join(", ") + "  vs  " + keys.join(", "));
  ok(/for _p in _bx: _p\['_pvc_exclude'\]=True/.test(eng),
     "  and it actually SETS the flag rather than only naming the men — the defect being closed was a " +
     "flag nothing set");
  ok(/BUST_EXCLUDE_APPLIED\s*=/.test(eng),
     "  and RECORDS what it set the flag on, so this test can read the engine's own answer rather " +
     "than re-deriving it (the re-implemented-assertion class)");
  ok(/if _bx and len\(_bx\)!=len\(BUST_EXCLUDE_KEYS\)/.test(eng),
     "  and HALTS on a PARTIAL exclusion — one man's draft sliding and the other's not is incoherent " +
     "under any store — while allowing zero, which is what a legacy scratch store legitimately is");

  /* THE LIVE-STORE ASSERTION, WHICH IS THE ONE THAT MATTERS. The engine deliberately does NOT halt
     when a store carries neither man: the first cut did, and it made the engine unable to load
     against the R15 proof's legacy R14 scratch, which a landing gate caught within the hour. So the
     "it must actually apply on the board we ship" half is asserted HERE, over the live store, where
     a scratch fixture cannot reach it. Both men must be in the cohort the curve builders read:
     first-time national/rookie selections, 2003-2021, in a position group the engine knows. */
  var storeRows = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "..", "engine", "rl_after",
    "rl_model_data.json"), "utf8"));
  var GRPOK = { MID: 1, SF: 1, KPF: 1, SD: 1, KPD: 1, RUCK: 1 };
  keys.forEach(function (k) {
    var row = storeRows.filter(function (r) { return r.key === k; })[0];
    ok(!!row, "  the live store carries " + k);
    ok(row && row.year >= 2003 && row.year <= 2021 && GRPOK[row.drafted_position],
       "  and he is inside the cohort the curve builders read, so the engine's flag reaches him",
       row && (row.year + " " + row.drafted_position));
  });

  if (!B) return;
  keys.forEach(function (k) {
    ok(B.rows.filter(function (r) { return r.k === k; }).length === 0,
       "  " + k + " is gone from the record entirely — not zeroed, not flagged: not picked", "0 rows");
  });

  /* AND THE SLIDE, which is the half that is easy to forget. Striking a man out WITHOUT sliding
     leaves a hole at pick 1 of his class and quietly shrinks that ordinal's denominator — a
     different distortion, not the removal of one. Every ordinal must still carry one observation
     per class it existed in. */
  var st = B.stamp || {};
  ok(Array.isArray(st.bustExcluded) && st.bustExcluded.length === 2,
     "the bundle DECLARES who was struck out and from where",
     (st.bustExcluded || []).map(function (e) { return e.name + " " + e.year + " #" + e.pick; }).join(", "));
  ok(st.bustSlid > 0, "and how many selections slid up to close the holes", st.bustSlid);

  var byYear = {};
  B.rows.forEach(function (r) { (byYear[r.y] = byYear[r.y] || []).push(r.p); });
  (st.bustExcluded || []).forEach(function (e) {
    var picks = (byYear[e.year] || []).slice().sort(function (a, b) { return a - b; });
    ok(picks[0] === 1, "  the " + e.year + " class still starts at pick 1 — no hole where " +
       e.name + " stood", "first pick " + picks[0]);
    var dup = picks.filter(function (p, i) { return i && p === picks[i - 1]; });
    ok(dup.length === 0, "  and the " + e.year + " slide collided with nothing", dup.join(","));
  });

  var counts = {};
  B.rows.forEach(function (r) { counts[r.p] = (counts[r.p] || 0) + 1; });
  var nClasses = st.nClasses;
  ok(counts[1] === nClasses && counts[2] === nClasses,
     "picks 1 and 2 still carry one observation per class — the slide closed the holes rather than " +
     "shrinking the denominators", counts[1] + ", " + counts[2] + " of " + nClasses);
})();

console.log("\n  " + "-".repeat(70));
console.log(fails ? "DRAFT DAY TESTS: " + fails + " FAILED of " + n
                  : "DRAFT DAY TESTS: ALL " + n + " PASS");
process.exit(fails ? 1 : 0);
