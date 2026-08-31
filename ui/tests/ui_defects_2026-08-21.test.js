/* THE 2026-08-21 UI ACT — the four defect fixes, the lens re-disable, the from/to scope, the v0
   feature and the three new board filters, exercised against the EXACT shipped app files.

   Run:  node ui/tests/ui_defects_2026-08-21.test.js      (exit 0 = all pass, exit 1 = a failure)

   Every assertion here is about BEHAVIOUR, not about this month's numbers. Where a figure is
   unavoidable it is read from the shipped bundle at run time rather than pinned, so a board move
   cannot red this suite for a reason that is not a defect (the "assert the relationship, not this
   month's number" rule the register keeps re-teaching). The one exception is deliberate and named:
   the v0 sidecar's board/store pin MUST be compared to the loaded board, because refusing a stale
   mirror is the behaviour under test. */
var fs = require("fs"), path = require("path"), vm = require("vm");

var fails = 0, n = 0;
function check(cond, label, extra) {
  n++;
  if (cond) { console.log("  [PASS] " + label); }
  else { fails++; console.log("  [FAIL] " + label + (extra ? "  " + extra : "")); }
}
function section(t) { console.log("\n" + t + "\n  " + "-".repeat(72)); }

var UI = path.join(__dirname, "..");
function appSrc(name) { return fs.readFileSync(path.join(UI, "app", name), "utf8"); }
function dataSrc(rel) { return fs.readFileSync(path.join(UI, rel), "utf8"); }
function exists(rel) { return fs.existsSync(path.join(UI, rel)); }

/* A browser-like context where `window` IS the global (the release-seam suite's pattern). */
function makeCtx() {
  var sandbox = { console: console, Math: Math, JSON: JSON, Object: Object, Array: Array,
                  String: String, Number: Number, isFinite: isFinite };
  sandbox.window = sandbox;
  sandbox.document = {
    readyState: "loading",
    addEventListener: function () {},
    getElementById: function () { return null; },
    createElement: function (tag) {
      return { tagName: tag, className: "", style: {}, title: "", disabled: false,
               innerHTML: "", textContent: "",
               classList: { add: function () {}, contains: function () { return false; } },
               appendChild: function () {}, addEventListener: function () {},
               setAttribute: function () {}, querySelector: function () { return null; } };
    },
  };
  vm.createContext(sandbox);
  return sandbox;
}
function load(ctx, name) { vm.runInContext(appSrc(name), ctx, { filename: name }); }
function loadData(ctx, rel) { vm.runInContext(dataSrc(rel), ctx, { filename: rel }); }

console.log("UI ACT 2026-08-21 — defect fixes · lens re-disable · from/to scope · v0 · board filters");

/* =============== (a) MOVERS: played:null MUST NOT RENDER AS DNP ================================ */
section("(a) movers — participation is tri-state, never a truthiness test");
(function () {
  var movers = require(path.join(UI, "app", "movers.js"));
  var core = movers.core;

  check(typeof core.participation === "function", "core exposes the single tri-state resolver");
  check(core.participation({ played: true }) === "played", "played:true -> played");
  check(core.participation({ played: false, dnp: true }) === "dnp", "played:false -> dnp");
  check(core.participation({ played: null, dnp: null }) === "unrecorded",
    "played:null -> UNRECORDED, not DNP", "got " + core.participation({ played: null, dnp: null }));
  check(core.participation({}) === "unrecorded", "an absent field -> unrecorded");

  // the synthetic from/to path must emit the ABSENT sentinel, not a false
  var bundle = {
    points: [{ id: "A", label: "A" }, { id: "B", label: "B" }],
    values: {
      k1: { name: "One", club: "C", pos: "Mid", byPoint: { A: { v: 100, rank: 2 }, B: { v: 150, rank: 1 } } },
      k2: { name: "Two", club: "C", pos: "Mid", byPoint: { A: { v: 120, rank: 1 }, B: { v: 90, rank: 2 } } },
    },
    reports: {},
  };
  var rep = core.compare(bundle, "A", "B");
  check(rep.synthetic === true, "an unstored pair yields a synthetic report");
  check(rep.players.length === 2, "both rows are present");
  check(rep.players.every(function (p) { return p.played === null && p.dnp === null; }),
    "every synthetic row carries played:null AND dnp:null (the ABSENT sentinel, not false)");
  check(rep.players.every(function (p) { return core.participation(p) === "unrecorded"; }),
    "so NOT ONE synthetic row resolves to DNP — the Phase-0 bug, closed");

  // the filter is the same tri-state, so the two cannot drift
  var mixed = [{ key: "p", played: true }, { key: "d", played: false }, { key: "u", played: null }];
  check(core.filter(mixed, { status: "played" }).map(function (p) { return p.key; }).join() === "p",
    "status=played selects only the proven played row");
  check(core.filter(mixed, { status: "dnp" }).map(function (p) { return p.key; }).join() === "d",
    "status=dnp selects ONLY the proven DNP row — an unrecorded row is not swept in",
    "got " + JSON.stringify(core.filter(mixed, { status: "dnp" }).map(function (p) { return p.key; })));
  check(core.filter(mixed, { status: "unrecorded" }).map(function (p) { return p.key; }).join() === "u",
    "status=unrecorded selects only the unrecorded row");

  // the renderer must not carry a two-branch truthiness test any more
  var src = appSrc("movers.js");
  check(src.indexOf("(p.played\n") < 0 && src.indexOf("p.played\n              ? '<span") < 0,
    "the renderer no longer branches on p.played truthiness");
  check(src.indexOf("core.participation(p)") > 0, "the renderer resolves through the shared tri-state");
})();

/* =============== the FROM/TO SCOPE — LIFTED (owner word 2026-08-28) ============================ */
section("(3) from/to — scope lifted; defaults to the LATEST round's single-model report");
(function () {
  var movers = require(path.join(UI, "app", "movers.js"));
  var core = movers.core;

  check(!core.SCOPE && !core.scopedPoints,
    "the R22 -> R23 scope is retired outright, not left dormant");

  var live = null;
  try {
    var ctx = makeCtx();
    loadData(ctx, path.join("data", "movers.js"));
    live = ctx.window.__MATCHDAY_MOVERS__;
  } catch (e) { /* bundle absent -> the shipped-bundle assertions below are skipped, loudly */ }

  if (!live) {
    check(false, "the shipped movers bundle loads (needed for the default-pair assertions)");
  } else {
    // RESTATED 2026-08-29 (THE WALK-FORWARD RETROSPECTIVE). Until the retrospective landed, the best
    // available single-model default was the latest STORED round report's own pair. It is no longer:
    // a stored report is priced under the model that was live that week, and R24's was finalised
    // before ORDER 45/46/47/48 and before the ORDER 49 blend, so it is a superseded model's answer —
    // and its `previous_round` is the last out-of-round column, not R23. The owner asked for "round
    // 23 to 24, under the current model". That is now literally available: the newest consecutive
    // RETRO pair, one model on both ends, one round of football between them, terminating on a
    // re-pricing that reproduces the live board exactly. It is synthetic in construction and single-
    // model in meaning, which is the property the original assertion was actually protecting.
    var dp = core.defaultPair(live);
    var lastRound = Number(live.rounds[live.rounds.length - 1]);
    var pts = core.points(live), byId = {};
    pts.forEach(function (p) { byId[String(p.id)] = p; });
    var pf = byId[String((dp || {}).from)], pt = byId[String((dp || {}).to)];
    check(pf && pt && pf.kind === "retro" && pt.kind === "retro" &&
          Number(pt.after_round) === lastRound && Number(pf.after_round) === lastRound - 1,
      "defaultPair is the newest consecutive RETRO pair — R" + (lastRound - 1) + " to R" + lastRound +
      ", both ends under the current model", JSON.stringify(dp));
    var rep = core.compare(live, dp.from, dp.to);
    check(rep && String(rep.submitted_round) === String(dp.to) && rep.player_count > 0,
      "…and it resolves to a comparison over the whole priced population");
    // NOT a loss of the facts: a one-round retro pair IS that round, so played/DNP/score are read
    // from the round's own stored report. Football does not depend on which engine priced it.
    var stored24 = (live.reports || {})[String(lastRound)] || {};
    check(rep.views.played_count === (stored24.views || {}).played_count &&
          rep.views.dnp_count === (stored24.views || {}).dnp_count &&
          rep.players.every(function (p) { return p.played !== null; }),
      "…and it keeps the round's participation facts (played " + rep.views.played_count +
      " / DNP " + rep.views.dnp_count + ") — the chips, the scores and both filters survive the change");
    // NON-VACUITY: a range that is NOT one round of football still says the facts are unknown.
    var multi = core.compare(live, "retro-r14", "retro-r24");
    check(multi.synthetic && multi.views.played_count === null &&
          multi.players.every(function (p) { return p.played === null && p.score === null; }),
      "a multi-round retro range has NO single participation fact and says so (not recorded)");
    check(core.spansModelChange(live, dp.from, dp.to).length === 0,
      "…and the default pair crosses NO model change (never a cross-model featured view)");
    // the machinery is intact: any stored pair still compares
    var wide = core.compare(live, "20", "23");
    check(wide && wide.players && wide.players.length > 0,
      "core.compare still answers for any stored pair — the selector is fully open again");
  }

  var src = appSrc("movers.js");
  check(src.indexOf("retrospective") > 0 || src.indexOf("RETROSPECTIVE") > 0,
    "the retrospective (walk-forward) ask stays recorded in the code while the engine act is in flight");
})();

/* =============== (b) TRADE: the ceiling clamp ================================================== */
section("(b) trade — describePick has a ceiling as well as a floor");
(function () {
  var ctx = makeCtx();
  load(ctx, "config.js");
  load(ctx, "format.js");
  // a minimal seam carrying only what the translator reads
  ctx.MD.seam = { working: { pvc: {}, players: [], stamp: {} }, indexed: function () { return { byKey: {} }; } };
  ctx.MD.dispVal = function (p) { return p ? p.v : null; };
  ctx.MD.state = { tier: "working", trade: { give: [], get: [] } };
  ctx.MD.anchors = {};
  load(ctx, "trade.js");
  var d = ctx.MD.trade.describePick;
  check(typeof d === "function", "trade exposes describePick for exercise");

  // THE SHIPPED CURVE, not a synthetic one — the translator's job is to describe the amounts the
  // owner's own PVC can and cannot price, so the fixture is that PVC.
  var bc = makeCtx();
  loadData(bc, path.join("data", "board_view_working.js"));
  var pvc = (bc.window.__MATCHDAY_WORKING__ || {}).pvc || {};
  check(pvc["1"] != null && pvc["64"] != null, "the shipped board carries the PVC the translator reads");
  ctx.MD.seam.working.pvc = pvc;
  var r1 = 0; for (var j = 1; j <= 18; j++) r1 += pvc[String(j)];

  check(d(pvc["1"]) === "a top-1 pick", "an amount AT pick 1 still reads as a top-1 pick", d(pvc["1"]));
  check(d(pvc["1"] - 1).indexOf("top-1") >= 0, "an amount just under pick 1 still reads as a top-1 pick",
    d(pvc["1"] - 1));
  check(d(pvc["2"]) === "a top-2 pick", "pick 2 reads as a top-2 pick", d(pvc["2"]));
  check(d(1) === "a pool pick", "the FLOOR clamp is untouched", d(1));

  // THE DEFECT, verbatim: the blind reviewer saw −11,376 SCAR described as "roughly a top-1 pick"
  // while pick 1 = 3,000. That is the case this clamp exists for.
  var big = 11376;
  check(d(big).indexOf("top-1") < 0, "11,376 no longer reads as 'a top-1 pick'", d(big));
  check(d(big).indexOf("more than pick 1") === 0,
    "it reads as MORE THAN pick 1 — the curve has no ordinal that can carry it", d(big));
  check(/[0-9.]+× pick 1/.test(d(big)), "and it states the size as a multiple of pick 1", d(big));
  check(big > pvc["1"] && big < r1,
    "…and 11,376 really sits above pick 1 (" + pvc["1"] + ") and below a whole first round (" + r1 + "), " +
    "so 'more than pick 1' is the honest rung");

  // above a whole first round -> the second rung
  var huge = r1 + 1;
  check(d(huge).indexOf("first round") > 0,
    "an amount above the whole first round says so", d(huge));
  check(d(huge).indexOf("top-1") < 0, "…and never names a pick", d(huge));

  // an incomplete curve must not fabricate a round total
  ctx.MD.seam.working.pvc = { "1": 3000, "64": 100 };
  check(d(9000).indexOf("more than pick 1") === 0,
    "with an incomplete curve the round rung is SKIPPED, not guessed", d(9000));
})();

/* =============== (b2) TRADE SEARCH — items 5, 6 and 7 (owner word 2026-08-31) ================== */
section("(b2) trade — the desk search: length (5), 'pick xx' (6), and future years (7)");
(function () {
  /* THE SHIPPED FILES, WIRED AS THE PAGE WIRES THEM (index.html order): the board bundle, the picks
     ledger, then config/format/seam/club_totals under the trade desk. The search is the one thing
     standing between what the owner types and what the desk offers him, so it is exercised against the
     real curve and the real ledger — a synthetic fixture would prove only that a fixture agrees with
     itself. matchItems reads no DOM, exactly as describePick above does not. */
  var ctx = makeCtx();
  loadData(ctx, path.join("data", "board_view_working.js"));
  loadData(ctx, path.join("data", "club_valuation.js"));
  load(ctx, "config.js");
  load(ctx, "format.js");
  load(ctx, "seam.js");
  load(ctx, "club_totals.js");
  load(ctx, "trade.js");

  var T = ctx.MD.trade, W = ctx.window.__MATCHDAY_WORKING__ || {}, CV = ctx.window.__CLUB_VALUATION__ || {};
  var pvc = W.pvc || {}, base = (W.stamp || {}).baseYear;
  check(typeof T.matchItems === "function" && typeof T.pickYears === "function",
    "the desk exposes its search for exercise (no DOM read anywhere in it)");
  check(ctx.MD.seam.clubHalt() === null,
    "…and the shipped picks ledger authenticates against this board, so the future-year path is LIVE",
    JSON.stringify(ctx.MD.seam.clubHalt()));

  // the ledger, read here independently of the desk: "year|ordinal" -> the ruled, year-weighted value
  var ledger = {}, years = {};
  Object.keys(CV.picksByTeam || {}).forEach(function (team) {
    (CV.picksByTeam[team] || []).forEach(function (p) {
      if (p.low !== p.high) return;                 // a band is not an ordinal
      ledger[p.year + "|" + p.low] = p.value;
      if (p.low >= 1 && p.low <= 64) years[p.year] = 1;
    });
  });
  var issued = Object.keys(years).map(Number).sort(function (a, b) { return a - b; });
  check(issued.length > 1, "the shipped ledger issues more than one draft year (" + issued.join("/") + ")");

  /* ---- item 7: FUTURE PICKS ARE SEARCHABLE, AT THE RULED PRICE ------------------------------- */
  check(T.pickYears().join() === issued.join(),
    "the desk offers exactly the years the ledger prices, base year first",
    T.pickYears().join() + " vs " + issued.join());
  check(T.pickYears()[0] === base, "…and the first of them is the BOARD's base year, not a literal", String(base));

  var rows62 = T.matchItems("62").filter(function (r) { return r.t === "pick" && !r.pool; });
  check(rows62.length === issued.length,
    "searching an ordinal answers with that pick in EVERY issued year", JSON.stringify(rows62.map(function (r) { return r.year; })));
  check(rows62.every(function (r) { return r.n === 62; }), "…and every one of them is that ordinal");
  check(rows62.every(function (r) { return r.year === base ? r.val === pvc["62"] : r.val === ledger[r.year + "|62"]; }),
    "…each priced by the SOURCE THAT OWNS THAT YEAR — base year off the PVC, later years off the " +
    "ledger's already-ruled value (2027 = (1/3 own + 2/3 round avg) x 0.9, 2028 = round avg x 0.8). " +
    "The desk re-derives no year rule; it could not honestly, the Ladder projection is in no bundle here",
    JSON.stringify(rows62.map(function (r) { return r.year + ":" + r.val; })));
  // NON-VACUITY: a later year really is a different price, so the assertion above is not comparing
  // one number with itself.
  check(rows62.some(function (r) { return r.year !== base && r.val !== pvc["62"]; }),
    "…and a future year's figure genuinely differs from the base year's",
    JSON.stringify(rows62.map(function (r) { return r.year + ":" + r.val; })));

  var pinned = T.matchItems("62 2027");
  check(pinned.length === 1 && pinned[0].n === 62 && pinned[0].year === 2027,
    "naming the year narrows to that one pick", JSON.stringify(pinned));
  check(!pinned.some(function (r) { return r.pool; }),
    "…and a year-pinned query is given NO pool item — the pool level is a base-year committed figure");

  /* THE POOL IS STILL THE POOL. Law 4: there is no ordinal 65, so a number past the curve resolves to
     the pool and never to a phantom ordinal — in any year. The ledger carries round-5 rows at 0, which
     is a ledger convention and not a pick price; reading them would put a 0-SCAR "Pick 70" on the desk. */
  var past = T.matchItems("70");
  check(past.length === 1 && past[0].pool === true,
    "a number past the curve's end is THE POOL, not a phantom ordinal", JSON.stringify(past));
  check(ledger["2026|70"] === 0 && ledger["2027|70"] === 0,
    "…and the ledger really does carry those rows (at 0), so the desk is declining them, not missing them");
  var allPickRows = [];
  ["", "5", "62", "pick", "2027", "2028", "70", "pool"].forEach(function (q) {
    T.matchItems(q).forEach(function (r) { if (r.t === "pick" && !r.pool) allPickRows.push(r); });
  });
  check(allPickRows.length > 0 && allPickRows.every(function (r) { return r.n >= 1 && r.n <= 64; }),
    "NO query offers an ordinal outside 1-64, in any year (" + allPickRows.length + " pick rows scanned)");
  check(allPickRows.every(function (r) { return typeof r.val === "number" && isFinite(r.val) && r.val > 0; }),
    "…and the desk offers no pick it cannot price — every offered row carries a real figure");

  /* ---- item 6: "PICK XX" FINDS THE PICK, AND "PICK" LISTS PICKS ------------------------------ */
  var asWords = T.matchItems("pick 62"), asDigits = T.matchItems("62");
  check(JSON.stringify(asWords) === JSON.stringify(asDigits),
    "'pick 62' and '62' are the SAME query — the phrasing cannot change the answer");
  check(T.matchItems("pick 62 2028").length === 1 && T.matchItems("pick 62 2028")[0].year === 2028,
    "'pick 62 2028' reads all three parts");
  var bare = T.matchItems("pick").filter(function (r) { return r.t === "pick"; });
  check(bare.length > 0, "'pick' on its own LISTS picks (it used to return two Picketts and no pick)");
  // and it must not have eaten the name search on the way past
  var pk = T.matchItems("pickett");
  check(pk.length > 0 && pk.every(function (r) { return r.t === "player"; }),
    "'pickett' is still a NAME search — the keyword is stripped, 'ett' is not digits, the parse declines",
    JSON.stringify(pk.map(function (r) { return r.label; })));
  check(T.matchItems("pool").length === 1 && T.matchItems("pool")[0].pool === true,
    "'pool' still names the pool item");
  check(T.matchItems("pick pool").length === 1 && T.matchItems("pick pool")[0].pool === true,
    "…and so does 'pick pool', which is what a pool pick is actually called");
  check(T.matchItems("2029")[0] && T.matchItems("2029")[0].pool === true,
    "a four-digit number that is NOT an issued year stays a number, so it resolves to the pool",
    JSON.stringify(T.matchItems("2029")));

  /* ---- item 5: THE LIST IS AS LONG AS THE MATCHES, AND NOT TRUNCATED SHORTER ----------------- */
  check(typeof T.MIN_ROWS === "number" && T.MIN_ROWS >= 5,
    "the desk publishes the owner's floor (" + T.MIN_ROWS + " rows) rather than a number retyped here");
  // THE DEFECT, verbatim: "currently it's only 2 items come up in the search". That was Pick 62 + the
  // pool, because one ordinal in one year is all the desk could match.
  check(T.matchItems("62").length === issued.length + 1,
    "the owner's own case ('62') is now one row per issued year plus the pool, not two rows",
    String(T.matchItems("62").length));
  check(T.matchItems("62").length > 2, "…which is strictly more than the two he counted");
  // the OTHER half of the shortness: a prefix query used to stop at six rows, silently dropping picks
  var five = T.matchItems("5"), ords5 = {};
  five.forEach(function (r) { if (r.t === "pick" && !r.pool) ords5[r.n] = 1; });
  check(five.length >= T.MIN_ROWS,
    "a query with matches to spare clears the floor ('5' -> " + five.length + " rows)");
  check(Object.keys(ords5).length >= 6 && ords5[5] && ords5[50],
    "…and the ordinal breadth of the old scan survives (exact match first, then the prefix run)",
    Object.keys(ords5).join(","));
  check(five[0] && five[0].n === 5, "the EXACT ordinal leads the list — typing '5' means pick 5, not pick 50");
  // a floor is not a pad: a query with fewer true matches returns fewer rows, inventing nothing
  check(T.matchItems("62 2027").length === 1,
    "…but the floor pads nothing — a query with one true match returns one row");

  /* THE YEAR ON A CHIP IS THE BOARD'S, not a string typed into the view — asserted by MOVING the base
     year rather than by grepping for the retired "2026 ND" literal (a text search cannot tell a live
     literal from the comment that records its retirement). The same move proves the ledger guard: with
     the desk's base year shifted, the ledger's base-year rows no longer agree with the PVC ordinal-for-
     ordinal, so it is no longer evidence that the ledger's other years are in these units — and NO
     future year is offered, rather than a row the desk cannot honestly compare. */
  var moved = makeCtx();
  loadData(moved, path.join("data", "board_view_working.js"));
  moved.window.__MATCHDAY_WORKING__.stamp.baseYear = base + 1;
  loadData(moved, path.join("data", "club_valuation.js"));
  load(moved, "config.js"); load(moved, "format.js"); load(moved, "seam.js");
  load(moved, "club_totals.js"); load(moved, "trade.js");
  check(moved.MD.trade.pickYears()[0] === base + 1,
    "move the bundle's base year and the desk's first year moves with it — no year is written into the view",
    JSON.stringify(moved.MD.trade.pickYears()));
  check(moved.MD.trade.pickYears().length === 1,
    "…and with the ledger no longer agreeing with the PVC on the base year, NO future year is offered",
    JSON.stringify(moved.MD.trade.pickYears()));
  check(moved.MD.trade.matchItems("5").filter(function (r) { return r.t === "pick" && !r.pool; })
        .every(function (r) { return r.year === base + 1; }),
    "…so every pick the moved desk offers wears the moved year");
})();

/* =============== (c) dRound — the dead assertions and the bridge are gone ====================== */
section("(c) dRound — the false comments and the bridge they justified are removed");
(function () {
  var board = appSrc("board.js"), card = appSrc("card.js"), config = appSrc("config.js");

  /* RESTATED 2026-08-28 (owner redesign): board.js and card.js were rewritten clean, so the
     retraction comments this block used to look for went with the file they annotated. What must
     stay true is the MECHANISM: no dRound bridge, and the one movement column reads the weekly
     report of record (Round Δ) with the card taking the board's own figure. */
  check(board.indexOf("w.dRound") < 0,
    "the name->key dRound bridge is DELETED, not left returning null");
  check(board.indexOf("__MATCHDAY_MOVERS__") > 0,
    "the board's one movement column reads the weekly report of record (Round Δ)");
  check(card.indexOf("MD.board.roundDeltas()") > 0,
    "the card's Round Δ is the board's own figure — one source, not a second computation");

  // the default Δ basis must be one the board actually carries
  var ctx = makeCtx();
  load(ctx, "config.js");
  check(ctx.MD.config.DELTA_BASE_DEFAULT === "bake",
    "DELTA_BASE_DEFAULT is the populated basis", ctx.MD.config.DELTA_BASE_DEFAULT);

  // and the claim must be true of the SHIPPED bundle, measured not assumed
  var w = null;
  try { var c2 = makeCtx(); loadData(c2, path.join("data", "board_view_working.js")); w = c2.window.__MATCHDAY_WORKING__; }
  catch (e) { /* reported below */ }
  if (!w) { check(false, "the shipped working bundle loads (needed to measure the basis)"); }
  else {
    var nD = w.players.filter(function (p) { return p.dRound != null; }).length;
    var nV = w.players.filter(function (p) { return p.vPrev != null; }).length;
    check(nV > 0, "vPrev IS carried on the shipped board (" + nV + " of " + w.players.length + ")");
    // this is the finding, asserted as a relationship: the default basis must be a fed one.
    var fed = ctx.MD.config.DELTA_BASE_DEFAULT === "bake" ? nV : nD;
    check(fed > 0, "the DEFAULT Δ basis is fed on the shipped board — no column of dashes by default",
      "dRound " + nD + " / vPrev " + nV + " of " + w.players.length);
  }
})();

/* =============== (d) the attribution waterfall ================================================= */
section("(d) attribution — the waterfall reads the SHIPPED {L1..L5} shape");
(function () {
  /* RESTATED 2026-08-28 (owner redesign): the waterfall panel is OFF the card — "Why the price is
     what it is" is process, not product. The DATA survives on the shipped board (asserted below);
     only the screen furniture is gone, and it must be ALL gone, not half-rendered. */
  var card = appSrc("card.js");
  check(card.indexOf("leverBlock") < 0 && card.indexOf("Why the price is") < 0,
    "the waterfall panel is retired from the card (owner word 2026-08-28)");
  check(card.indexOf("RL_PVCADOPT") < 0 && card.indexOf("RL_DIAL14") < 0,
    "…and no dial-map fragment survives on the surface");
  check(card.indexOf("resid") < 0, "…and no residual bar either — the removal is whole");

  // the shipped board must actually carry the shape the card now reads
  var w = null;
  try { var c = makeCtx(); loadData(c, path.join("data", "board_view_working.js")); w = c.window.__MATCHDAY_WORKING__; }
  catch (e) { /* reported below */ }
  if (!w) { check(false, "the shipped working bundle loads (needed to check the lever shape)"); }
  else {
    var withLev = w.players.filter(function (p) { return p.levers && typeof p.levers === "object"; });
    check(withLev.length > 0, "the export carries `levers` on the shipped board (" + withLev.length +
      " of " + w.players.length + ")");
    check(!Array.isArray(withLev[0].levers), "…as a DICT, which is the shape the card now reads");
    check(Object.keys(withLev[0].levers).every(function (k) { return /^L[0-9]+$/.test(k); }),
      "…keyed by dial code", JSON.stringify(withLev[0].levers));
  }
})();

/* =============== (2) the +1/+2 lenses are OFF ================================================== */
section("(2) the +1/+2 projection lenses are re-disabled and unreachable");
(function () {
  var ctx = makeCtx();
  load(ctx, "config.js");
  ctx.MD.fmt = { esc: function (s) { return String(s); } };
  load(ctx, "seam.js");

  var dis = ctx.MD.config.LENS_DISABLED;
  check(Array.isArray(dis) && dis.indexOf(3) >= 0 && dis.indexOf(4) >= 0,
    "+1 (3) and +2 (4) are declared disabled", JSON.stringify(dis));
  check(dis.indexOf(0) < 0 && dis.indexOf(1) < 0 && dis.indexOf(2) < 0,
    "-2, -1 and Now are NOT disabled — only the ruled-wrong forward lenses");
  check(typeof ctx.MD.config.LENS_DISABLED_NOTE === "string" &&
    ctx.MD.config.LENS_DISABLED_NOTE.indexOf("rebuild") > 0,
    "the short on-screen note names the rebuild", ctx.MD.config.LENS_DISABLED_NOTE);
  check(ctx.MD.lensDisabled(3) && ctx.MD.lensDisabled(4), "the gate reports both forward lenses off");
  check(!ctx.MD.lensDisabled(2), "…and reports Now on");
  check(ctx.MD.lensClamp(3) === ctx.MD.config.LENS_DEFAULT && ctx.MD.lensClamp(4) === ctx.MD.config.LENS_DEFAULT,
    "a disabled lens CLAMPS to the default — it cannot become the active lens");
  check(ctx.MD.lensClamp(0) === 0 && ctx.MD.lensClamp(1) === 1,
    "…and the backward lenses pass through untouched");
  check(!ctx.MD.lensDisabled(ctx.MD.config.LENS_DEFAULT), "the default lens is never a disabled one");

  /* RESTATED 2026-08-28 (owner redesign): the board no longer has a lens control AT ALL — a
     retired picker cannot smuggle a disabled lens in, and the card truncates the lens series to
     the three backward entries, so +1/+2 render nowhere. */
  var board = appSrc("board.js");
  check(board.indexOf("lensClamp") < 0 && board.indexOf("s.lens") < 0,
    "the board carries NO lens control — the picker is retired with the forward lenses");
  check(/\.slice\(0, 3\)/.test(appSrc("card.js")),
    "the card truncates the lens series to the three backward entries — +1/+2 render nowhere");
})();

/* =============== (4) v0 — the sidecar, the pin, and the arithmetic ============================= */
section("(4) v0 — entry price, live rating, absolute and ratio; no ranking");
(function () {
  check(exists(path.join("tools", "gen_v0_sidecar.py")), "the generator exists at ui/tools/gen_v0_sidecar.py");
  var haveSidecar = exists(path.join("data_aux", "v0.js"));
  check(haveSidecar, "the sidecar is generated at ui/data_aux/v0.js (NOT under ui/data/, the landing's carriers)");
  if (!haveSidecar) return;

  var ctx = makeCtx();
  load(ctx, "config.js");
  load(ctx, "format.js");
  loadData(ctx, path.join("data", "board_view_working.js"));
  loadData(ctx, path.join("data_aux", "v0.js"));
  var W = ctx.window.__MATCHDAY_WORKING__, V = ctx.window.__V0__;
  ctx.MD.seam = { working: W, public: null, indexed: function () { return { byKey: {} }; } };
  ctx.MD.dispVal = function (p) { return (p && p.ov && p.ov.dispv != null) ? p.ov.dispv : (p ? p.v : null); };
  load(ctx, "v0.js");
  var v0 = ctx.MD.v0;

  check(V.stamp && V.stamp.board && V.stamp.store,
    "the bundle NAMES the board and store it was generated from");
  check(v0.pin().ok, "…and that identity is the one the app is loaded on (the pin passes)", v0.pin().why || "");
  check(v0.active(), "so the sidecar is ACTIVE");
  check(V.stamp.nRows === W.players.length,
    "every active board player has a row", V.stamp.nRows + " vs " + W.players.length);
  check(V.stamp.nAbsent === 0,
    "and none is unrecoverable on this board", "nAbsent=" + V.stamp.nAbsent);
  check(V.stamp.nEntryAnchor > 0,
    "POOL ENTRANTS CARRY A v0 — the owner's correction, honoured: " + V.stamp.nEntryAnchor +
    " rows are priced off their signed entry anchor, not dashed");
  check(V.stamp.nPickSlot + V.stamp.nEntryAnchor + V.stamp.nAbsent === V.stamp.nRows,
    "the three origins partition the roster exactly");

  // the owner's own worked example, as arithmetic
  var probe = { key: null, v: 4000 };
  var real = W.players.filter(function (p) { return V.byKey[p.key] && V.byKey[p.key].v0; })[0];
  var r = v0.of(real);
  check(r.has && r.v0 > 0 && r.live != null, "a real row resolves to a v0 and a live rating");
  check(r.delta === r.live - r.v0, "the absolute is live − v0, a difference of two given figures");
  check(Math.abs(r.ratio - r.live / r.v0) < 1e-9, "the ratio is live ÷ v0");
  check(v0.ratioText(1.25) === "1.25x", "the ratio prints in the owner's own notation", v0.ratioText(1.25));

  // THE TIE STRUCTURE IS THE FEATURE, NOT A BUG — every pick-5 mid of one draft age shares a v0
  var bySlot = {};
  Object.keys(V.byKey).forEach(function (k) {
    var rec = V.byKey[k];
    if (rec.slot) { (bySlot[rec.slot] = bySlot[rec.slot] || []).push(rec.v0); }
  });
  var shared = Object.keys(bySlot).filter(function (s) { return bySlot[s].length > 1; });
  check(shared.length > 0, "the surface really does share slots (" + shared.length + " shared slots)");
  check(shared.every(function (s) {
    return bySlot[s].every(function (v) { return v === bySlot[s][0]; });
  }), "and EVERY player in a shared slot carries the identical v0 — the primer's law, held");
  var p5 = Object.keys(bySlot).filter(function (s) { return /^MID\|\d+\|5$/.test(s); });
  check(p5.length > 0 && p5.every(function (s) {
    return bySlot[s].every(function (v) { return v === bySlot[s][0]; });
  }), "spot-check: the pick-5 mids share one v0", p5.map(function (s) {
    return s + "=" + bySlot[s][0] + " x" + bySlot[s].length;
  }).join(" "));

  // NO RANKING ANYWHERE
  var v0src = appSrc("v0.js"), cardsrc = appSrc("card.js");
  check(v0src.indexOf("NO RANKING") > 0, "the module states the no-ranking rule");
  check(!/rank/i.test(v0src.replace(/[\s\S]*?NO RANK[\s\S]*?\n\n/, "").split("function status")[0]) ||
        v0src.indexOf("v0Rank") < 0, "no v0 rank is computed anywhere in the module");
  check(cardsrc.indexOf("v0Rank") < 0 && cardsrc.indexOf("entry rank") < 0,
    "and the card ships no entry rank");

  // the pin FAILS CLOSED on a moved board
  var ctx2 = makeCtx();
  load(ctx2, "config.js"); load(ctx2, "format.js");
  loadData(ctx2, path.join("data_aux", "v0.js"));
  ctx2.MD.seam = { working: { stamp: { board_md5: "deadbeefdeadbeef", store_md5: V.stamp.store }, players: [] } };
  ctx2.MD.dispVal = function (p) { return p ? p.v : null; };
  load(ctx2, "v0.js");
  check(!ctx2.MD.v0.pin().ok, "a sidecar generated from another board is REFUSED");
  check((ctx2.MD.v0.pin().why || "").indexOf("board") >= 0,
    "…and the refusal names which identity broke", ctx2.MD.v0.pin().why);
  var refused = ctx2.MD.v0.of({ key: real.key, v: 1 });
  check(refused.refused && refused.v0 == null,
    "a refused row yields NO figure — there is no fallback source for an entry price");
})();

/* =============== (4b) v0 ON THE PUBLIC TIER — the owner's word, same day ======================= */
section("(4b) v0 on the public tier — joined at generation time, and NO key added to do it");
(function () {
  var ctx = makeCtx();
  loadData(ctx, path.join("data", "board_view_working.js"));
  loadData(ctx, path.join("data", "board_view_public.js"));
  loadData(ctx, path.join("data_aux", "v0.js"));
  var W = ctx.window.__MATCHDAY_WORKING__, P = ctx.window.__MATCHDAY_PUBLIC__, V = ctx.window.__V0__;

  /* THE LAW FIRST. The public bundle is leak-proof BY CONSTRUCTION — no key, no id, no internals — and
     the whole point of doing this join in the generator is that shipping the entry price did not cost
     that. So the first assertion is not about v0 at all: it is that nothing was added to make v0
     possible. */
  var forbidden = ["key", "posCode", "slot", "ov", "levers", "vRaw", "owner_rule", "lti_reg", "cat", "pk"];
  var leaked = forbidden.filter(function (k) {
    return P.players.some(function (r) { return Object.prototype.hasOwnProperty.call(r, k); });
  });
  check(!leaked.length, "the public row still carries NO key and no internals — the join added a FACT, not an identifier",
    "leaked " + JSON.stringify(leaked));

  check(P.players.length === W.players.length, "the public bundle still carries every player",
    P.players.length + " vs " + W.players.length);
  check(P.players.every(function (r) { return "v0" in r && "v0_origin" in r; }),
    "every public row carries the entry price AND which entry price it is");

  var st = (P.stamp && P.stamp.v0) || {};
  check(st.joined === true, "the public stamp records that the join was MADE, so a reader is never left inferring it",
    JSON.stringify(st));
  var priced = P.players.filter(function (r) { return r.v0 != null; });
  check(st.nPriced === priced.length && st.nPriced + st.nAbsent === P.players.length,
    "…and its counts are the measured ones, partitioning the published rows",
    JSON.stringify({ nPriced: st.nPriced, nAbsent: st.nAbsent, measured: priced.length, rows: P.players.length }));

  /* THE JOIN IS FAITHFUL. Every published figure must be the SIDECAR's own figure for that player —
     the generator holds the keys, so this is the one place the join can be checked against them. */
  var keyByName = {};
  W.players.forEach(function (p) { if (p.name != null) keyByName[p.name] = p.key; });
  var wrong = P.players.filter(function (r) {
    var rec = V.byKey[keyByName[r.name]];
    return !rec || rec.v0 !== r.v0 || (rec.origin || "unrecoverable") !== r.v0_origin;
  });
  check(!wrong.length, "EVERY published entry price is the sidecar's own figure and origin for that player — the join invents nothing",
    wrong.length + " row(s) differ, first: " + JSON.stringify(wrong[0] || null));

  check(P.players.every(function (r) { return r.v0 === null ? r.v0_origin === "unrecoverable" : r.v0 > 0; }),
    "an unrecoverable entry price is NULL with its origin named — never 0, never silently omitted");

  /* RESTATED 2026-08-28 (owner redesign): the app now ships ONE fully transparent tier, so the
     public-card renderer is gone. The public BUNDLE keeps its leak-proof v0 join (asserted above,
     unchanged); on the card, the entry price renders through MD.v0 — one vocabulary, no copy. */
  var cardsrc = appSrc("card.js");
  check(cardsrc.indexOf("renderPublic") < 0 && cardsrc.indexOf("v0SectionPublic") < 0,
    "the public-tier card renderer is retired — one transparent tier");
  check(cardsrc.indexOf("v0Section(p)") > 0, "the card renders the entry-price section");
  check(cardsrc.indexOf("MD.v0.of(") > 0 && cardsrc.indexOf("MD.v0.ratioText") > 0,
    "the entry price and ratio notation are MD.v0's, not a second copy");

  /* THE COMMENT MUST NOT OUTLIVE ITS TRUTH — the module said "pending an owner word" and the word came.
     As with dRound above, the header QUOTES the retracted note in order to retract it, so what is
     asserted is that the correction is stated and that status() no longer reports a pending decision. */
  var v0src = appSrc("v0.js");
  check(v0src.indexOf("v0 goes on the public board, yes") > 0,
    "ui/app/v0.js records the owner's word verbatim, where the pending note used to stand");
  var c2 = makeCtx();
  load(c2, "config.js"); load(c2, "format.js");
  loadData(c2, path.join("data", "board_view_working.js"));
  loadData(c2, path.join("data_aux", "v0.js"));
  c2.MD.seam = { working: c2.window.__MATCHDAY_WORKING__, public: null, indexed: function () { return { byKey: {} }; } };
  c2.MD.dispVal = function (p) { return p ? p.v : null; };
  load(c2, "v0.js");
  var tier = String(c2.MD.v0.status().publicTier || "");
  check(!/pending/i.test(tier), "status() no longer reports the public tier as a pending decision", tier);
  check(tier.indexOf("2026-08-21") > 0, "…it names the word it ships on", tier);
})();

/* =============== (5) the three new board filters =============================================== */
section("(5) board filters — cohort year · age · live eligibility");
(function () {
  var ctx = makeCtx();
  load(ctx, "config.js");
  load(ctx, "format.js");
  loadData(ctx, path.join("data", "board_view_working.js"));
  var W = ctx.window.__MATCHDAY_WORKING__;
  ctx.MD.seam = { working: W, public: null, clubHalt: function () { return null; },
                  picksFor: function () { return []; }, indexed: function () { return { byKey: {}, byName: {} }; } };
  ctx.MD.dispVal = function (p) { return p ? p.v : null; };
  ctx.MD.state = { lens: 2, tier: "working", deltaBase: "bake", slugs: false };
  ctx.MD.anchors = {}; ctx.MD.anchorStatus = function () { return null; };
  ctx.MD.ownership = { clubOf: function (p) { return p.affl_team; }, labelOf: function () { return ""; },
                       titleOf: function () { return ""; } };
  ctx.MD.v0 = { status: function () { return { active: false }; }, of: function () { return { refused: true, why: "x" }; },
                originWord: function () { return ""; }, originTip: function () { return ""; },
                ratioText: function () { return ""; } };
  ctx.MD.clubTotals = { compute: function () { return null; }, byTeam: function () { return null; },
                        rankOf: function () { return null; } };
  ctx.MD.pocket = { has: function () { return false; }, attach: function () {} };
  ctx.MD.history = { series: function () { return []; } };
  load(ctx, "seam.js");
  load(ctx, "board.js");
  var B = ctx.MD.board;

  // ---- the cohort clock, exactly as the owner stated it
  check(typeof B.cohortYear === "function", "the board exposes the cohort clock");
  check(B.cohortYear({ ty: "ND", yr: 2024 }) === 2024, "a 2024 ND entrant is in the 2024 cohort");
  check(B.cohortYear({ ty: "RD", yr: 2024 }) === 2024, "a 2024 RD entrant is in the 2024 cohort");
  check(B.cohortYear({ ty: "SSP", yr: 2024 }) === 2024, "a 2024 SSP entrant is in the 2024 cohort");
  check(B.cohortYear({ ty: "MSD", yr: 2025 }) === 2024,
    "AND a 2025 MSD selection is in the 2024 cohort — the owner's stated grouping",
    "got " + B.cohortYear({ ty: "MSD", yr: 2025 }));
  check(B.cohortYear({ ty: "MSD", yr: 2024 }) === 2023, "…so a 2024 MSD belongs to the 2023 cohort");
  check(B.cohortYear({ ty: "ND", yr: null }) === null, "a row without a draft year has no cohort");

  // and the rule is derivable from the shipped bundle, not just asserted
  var msd = W.players.filter(function (p) { return p.ty === "MSD"; });
  var nd = W.players.filter(function (p) { return p.ty === "ND"; });
  check(msd.length > 0 && nd.length > 0, "the shipped board carries both MSD and ND rows",
    "MSD " + msd.length + " / ND " + nd.length);
  var c24 = W.players.filter(function (p) { return B.cohortYear(p) === 2024; });
  var c24msd = c24.filter(function (p) { return p.ty === "MSD"; });
  check(c24.length > 0, "the 2024 cohort is non-empty on the shipped board (" + c24.length + " players)");
  check(c24msd.every(function (p) { return p.yr === 2025; }),
    "every MSD row inside the 2024 cohort carries draft year 2025 — the clock rule, on real rows",
    c24msd.length + " MSD rows");

  // ---- age
  check(B.ageMatches({ age: 22 }, null) === true, "a null age filter matches everything");
  check(B.ageMatches({ age: 22 }, "22") === true, "an exact age matches");
  check(B.ageMatches({ age: 23 }, "22") === false, "…and only that age");
  check(B.ageMatches({ age: 19 }, "b:-20") === true, "the 20-and-under band matches 19");
  check(B.ageMatches({ age: 21 }, "b:-20") === false, "…and not 21");
  check(B.ageMatches({ age: 34 }, "b:29-") === true, "the 29-and-over band matches 34");
  check(B.ageMatches({ age: null }, "22") === false,
    "a row with NO age drops out while an age filter is on, rather than being bucketed");
  check(B.AGE_BANDS.length === 4 && B.AGE_BANDS.every(function (b) { return b.lo <= b.hi; }),
    "the bands are well-formed and cover the range in order");

  // ---- live eligibility
  check(B.eligMatches({ elig: ["MID"] }, null) === true, "a null eligibility filter matches everything");
  check(B.eligMatches({ elig: ["KPF", "MID"] }, "KPF") === true, "a dual player matches his KPF eligibility");
  check(B.eligMatches({ elig: ["KPF", "MID"] }, "MID") === true, "…AND his MID eligibility");
  check(B.eligMatches({ elig: ["SD"] }, "KPF") === false, "a player without the eligibility does not match");
  check(B.eligMatches({ elig: [] }, "KPF") === false, "an empty eligibility set matches nothing");
  check(B.eligMatches({}, "KPF") === false, "…and so does an absent one");

  // the shipped bundle really carries the column, and it really is a superset of the modelling axis
  var withElig = W.players.filter(function (p) { return (p.elig || []).length; });
  check(withElig.length === W.players.length,
    "every shipped row carries an eligibility set", withElig.length + " of " + W.players.length);
  var duals = W.players.filter(function (p) { return (p.elig || []).length > 1; });
  check(duals.length > 0, "and the board really has dual-eligible players (" + duals.length + ") — " +
    "the case the modelling Position axis cannot answer");
  var kpfElig = W.players.filter(function (p) { return B.eligMatches(p, "KPF"); });
  var kpfPos = W.players.filter(function (p) { return p.posCode === "KPF"; });
  check(kpfElig.length >= kpfPos.length,
    "\"eligible to play KPF now\" is a superset of \"modelled as KPF\"",
    kpfElig.length + " eligible vs " + kpfPos.length + " modelled");

  // ---- the filters ride the universal Back
  /* RESTATED 2026-08-28 (owner redesign): the column-lens toggle (v0Col) is retired with the rest
     of the board controls — the columns are fixed. The five surviving filters still ride Back. */
  var snap = B.snapshot();
  check("clubFilter" in snap && "posFilter" in snap &&
        "cohortFilter" in snap && "ageFilter" in snap && "eligFilter" in snap,
    "the snapshot carries all five surviving filters, so Back restores the board you were on",
    JSON.stringify(Object.keys(snap)));
  B.restore({ cohortFilter: "2024", ageFilter: "b:-20", eligFilter: "KPF" });
  var snap2 = B.snapshot();
  check(snap2.cohortFilter === "2024" && snap2.ageFilter === "b:-20" && snap2.eligFilter === "KPF",
    "…and restore round-trips them", JSON.stringify(snap2));
  B.restore({ cohortFilter: null, ageFilter: null, eligFilter: null });
})();

console.log("\n  " + "-".repeat(72));
console.log(fails ? ("UI ACT 2026-08-21: " + fails + " FAIL / " + n)
                  : ("UI ACT 2026-08-21: ALL " + n + " PASS"));
process.exit(fails ? 1 : 0);
