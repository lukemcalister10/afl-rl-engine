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

/* =============== (b2) TRADE SEARCH — items 5, 6 and 7, AS THE OWNER CORRECTED THEM ============= */
section("(b2) trade — future picks are club + year + round, never an ordinal (owner correction 2026-08-31)");
(function () {
  /* THE SHIPPED FILES, WIRED AS THE PAGE WIRES THEM (index.html order): the board bundle, the picks
     ledger, then config/format/seam/club_totals under the trade desk. The search is the one thing
     standing between what the owner types and what the desk offers him, and the namer is the one thing
     between what he clicked and what the chip reads, so both are exercised against the real curve and
     the real ledger — a synthetic fixture would prove only that a fixture agrees with itself. Neither
     reads the DOM, exactly as describePick above does not.

     THE OWNER'S CORRECTION, which is what this block is now about: "2027 pick 62 isn't pick 62. It's a
     fourth round pick. 2027 and 2028 picks don't have numbers. They exist as concepts — Hawthorn's
     future 1st round pick — we don't know what pick that will be yet. … You'd search for Hawthorn 2027
     4th — or 4th round 27 Hawthorn etc." Every assertion here is a RELATIONSHIP against the shipped
     ledger, never this month's figure. */
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
  check(typeof T.matchItems === "function" && typeof T.pickYears === "function" &&
        typeof T.pickRounds === "function" && typeof T.pickName === "function",
    "the desk exposes its search AND its namer for exercise (no DOM read anywhere in either)");
  check(ctx.MD.seam.clubHalt() === null,
    "…and the shipped picks ledger authenticates against this board, so the future-pick path is LIVE",
    JSON.stringify(ctx.MD.seam.clubHalt()));

  /* THE LEDGER, READ HERE INDEPENDENTLY OF THE DESK. A pick asset's identity is (origin club, year,
     round); `value` is the ruled, year-weighted price; `low`/`high` is the PROJECTED BAND, which is a
     pricing input and must never surface as a name. */
  var rows = [], priced = [], byId = {};
  Object.keys(CV.picksByTeam || {}).forEach(function (team) {
    (CV.picksByTeam[team] || []).forEach(function (p) {
      if (!p || !p.origin || !(p.year > 0) || !(p.round > 0)) return;
      rows.push(p);
      if (typeof p.value === "number" && p.value > 0) {
        priced.push(p);
        byId[p.origin + "|" + p.year + "|" + p.round] = p;
      }
    });
  });
  function uniq(a) { var s = {}; a.forEach(function (x) { s[x] = 1; });
                     return Object.keys(s).map(Number).sort(function (x, y) { return x - y; }); }
  var issued = uniq(priced.map(function (p) { return p.year; }));
  var ledgerRounds = uniq(priced.map(function (p) { return p.round; }));
  var futureYears = issued.filter(function (y) { return y !== base; });
  check(rows.length > 0 && issued.length > 1 && ledgerRounds.length > 1 && futureYears.length > 0,
    "the shipped ledger prices more than one year (" + issued.join("/") + ") over more than one round (" +
    ledgerRounds.join("/") + ") — so nothing below is vacuous");

  // the desk's own spelling of a round, rebuilt here from the ledger's round number alone
  function ord(n) {
    var t = n % 100, u = n % 10;
    return n + ((t >= 11 && t <= 13) ? "th" : u === 1 ? "st" : u === 2 ? "nd" : u === 3 ? "rd" : "th");
  }
  function picksIn(q) { return T.matchItems(q).filter(function (r) { return r.t === "pick" && !r.pool; }); }
  function futureIn(q) { return picksIn(q).filter(function (r) { return r.year !== base; }); }
  function idOf(r) { return r.club + "|" + r.year + "|" + r.round; }

  /* ---- THE YEARS AND ROUNDS OFFERED ARE THE YEARS AND ROUNDS THE LEDGER PRICES ---------------- */
  check(T.pickYears().join() === issued.join(),
    "the years the desk offers ARE the years the ledger prices, base year first",
    T.pickYears().join() + " vs " + issued.join());
  check(T.pickYears()[0] === base, "…and the first of them is the BOARD's base year, not a literal", String(base));
  check(T.pickRounds().join() === ledgerRounds.join(),
    "the rounds the desk offers ARE the rounds the ledger PRICES", T.pickRounds().join() + " vs " + ledgerRounds.join());

  /* ---- REQUIREMENT 3: THE ROUND-5 ROWS ARE A LEDGER CONVENTION, NOT AN ASSET ------------------ */
  var zeroRounds = uniq(rows.filter(function (p) { return p.value === 0; }).map(function (p) { return p.round; }));
  check(zeroRounds.length > 0,
    "the ledger really does carry a whole round at value 0 (round " + zeroRounds.join("/") + ") in every year — " +
    "a ledger convention recording that the round exists, not a price");
  check(zeroRounds.every(function (r) { return T.pickRounds().indexOf(r) === -1; }),
    "…and NOT ONE of those rounds is offered as a pickable asset, in any year — the desk declines them, " +
    "it is not merely missing them", T.pickRounds().join());
  check(zeroRounds.every(function (r) {
    return ["", "hawthorn ", "hawthorn 2027 "].every(function (pre) {
      return T.matchItems(pre + ord(r)).filter(function (x) { return x.t === "pick"; }).length === 0;
    });
  }), "…and asking for one by name offers nothing rather than a 0-SCAR row — the round is not even " +
      "search vocabulary", JSON.stringify(zeroRounds.map(function (r) { return ord(r); })));

  /* ---- THE CORRECTION: NO LATER YEAR CARRIES AN ORDINAL, ANYWHERE ---------------------------- */
  var probes = ["", "5", "62", "27", "pick", "2026", "2027", "2028", "1st", "4th round 27 hawthorn",
                "hawthorn", "hawthorn 2027", "2027 1st", "70", "pool", "north melbourne 2028 2nd"];
  var allPicks = [], allFuture = [];
  probes.forEach(function (q) {
    picksIn(q).forEach(function (r) { allPicks.push(r); if (r.year !== base) allFuture.push(r); });
  });
  check(allFuture.length > 0, "the probe battery reaches the future assets at all (" + allFuture.length + " rows)");
  check(allFuture.every(function (r) { return r.n == null; }),
    "NOT ONE offered later-year pick carries an ordinal — a 2027 pick has no number, so the desk gives it none");
  check(allFuture.every(function (r) { return !/pick\s*\d/i.test(String(r.label)) && String(r.label).indexOf("#") < 0; }),
    "…and not one of their names says 'Pick 62' or '#62' — the owner's exact complaint, closed",
    JSON.stringify(allFuture.slice(0, 3).map(function (r) { return r.label; })));
  check(allPicks.filter(function (r) { return r.year === base; }).every(function (r) { return r.n >= 1 && r.n <= 64; }),
    "…while a BASE-YEAR pick still is its number, 1-64 and nothing else — that year is unchanged");

  /* THE BAND IS A PRICING INPUT AND IS NEVER SURFACED. The ledger's 2027 row for the asset the owner
     called "2027 pick 62" carries low=high=62; the desk must name it by its ROUND. Tested over every
     future row the battery reached, against that row's own band. */
  var banded = allFuture.filter(function (r) { return byId[idOf(r)] && byId[idOf(r)].low != null; });
  check(banded.length > 0, "the future rows the desk offers do have a projected band in the ledger (" +
    banded.length + " rows) — so the assertion below has something to catch");
  check(banded.every(function (r) {
    var b = byId[idOf(r)], lab = String(r.label);
    // the round token is trimmed off first — "…2027 1st" legitimately carries the round's own digit,
    // and the year legitimately carries four of them; what must not appear is the BAND.
    var head = lab.slice(0, lab.length - ord(r.round).length);
    return !new RegExp("(^|[^0-9])" + b.low + "([^0-9]|$)").test(head);
  }), "…and NOT ONE name contains its projected band — the band prices the pick, it does not name it",
     JSON.stringify(banded.slice(0, 2).map(function (r) { return r.label + " <- band #" + byId[idOf(r)].low; })));
  check(banded.every(function (r) { return String(r.label).indexOf(ord(byId[idOf(r)].round)) > 0; }),
    "…each is named by its ROUND instead ('… 2027 4th')");

  /* ---- REQUIREMENT 1: THE DISPLAY FORM IS CLUB + YEAR + ROUND -------------------------------- */
  check(allFuture.every(function (r) {
    var b = byId[idOf(r)];
    return b && r.label === (b.originDisplay || b.origin) + " " + r.year + " " + ord(r.round);
  }), "every future pick reads as its club, its year and its round — and the club spelling is the " +
      "LEDGER's own display name, not a second spelling rule invented in the view",
      JSON.stringify(allFuture.slice(0, 2).map(function (r) { return r.label; })));
  // the DROPDOWN row and the BASKET chip must be one namer, or a pick loses its ordinal on one surface
  // and keeps it on the other — which is exactly how this defect got in.
  check(allFuture.every(function (r) {
    return T.pickName({ t: "pick", club: r.club, year: r.year, round: r.round }) === r.label;
  }), "…and the basket chip is the SAME namer the dropdown row used — one name per asset, not two");
  check(T.pickName({ t: "pick", n: 24, year: base }) === "Pick 24" &&
        T.pickName({ t: "pick", pool: true, year: base }) === "Pool pick",
    "…while a base-year pick still names itself by number and the pool still names itself the pool",
    T.pickName({ t: "pick", n: 24, year: base }));
  /* THE RETIRED FORM CANNOT BE RESURRECTED BY A HAND-SET BASKET. The search cannot build one and no
     basket is persisted, but a later-year ordinal is not an asset, so the namer refuses to spell it. */
  check(futureYears.every(function (y) { return T.pickName({ t: "pick", n: 62, year: y }) !== "Pick 62"; }),
    "a later-year ordinal gets NO name at all — 'Pick 62 · 2027 ND' cannot be put back on the desk by " +
    "hand", futureYears.map(function (y) { return y + ":" + T.pickName({ t: "pick", n: 62, year: y }); }).join(" "));

  /* ---- REQUIREMENT 2: CLUB, YEAR AND ROUND IN ANY ORDER, TOLERANT OF SHORTHAND --------------- */
  var target = futureIn("hawthorn 2027 4th");
  check(target.length === 1 && target[0].year === 2027 && target[0].round === 4 &&
        /hawthorn/i.test(target[0].club),
    "the owner's own phrasing — 'Hawthorn 2027 4th' — lands on exactly that one asset",
    JSON.stringify(target.map(function (r) { return r.label; })));
  var forms = ["hawthorn 2027 4th", "4th round 27 hawthorn", "2027 4th hawthorn", "hawthorn 4th 2027",
               "hawthorn r4 27", "hawthorn fourth 2027", "round 4 hawthorn 2027", "hawthorn's 2027 4th",
               "pick hawthorn 2027 4th"];
  check(forms.every(function (q) { return futureIn(q).map(idOf).join() === target.map(idOf).join(); }),
    "…and so does every reordering and shorthand of it — club/year/round in any order, '27' for 2027, " +
    "'4th'/'fourth'/'r4'/'round 4' for the round",
    forms.filter(function (q) { return futureIn(q).map(idOf).join() !== target.map(idOf).join(); }).join(" | "));

  // each named part NARROWS; an unnamed part matches everything.
  check(futureIn("hawthorn 2027").length === ledgerRounds.filter(function (r) {
      return zeroRounds.indexOf(r) === -1; }).length,
    "'hawthorn 2027' is the club's whole priced 2027 holding — one row per priced round",
    JSON.stringify(futureIn("hawthorn 2027").map(function (r) { return r.label; })));
  check(futureIn("hawthorn 2027").every(function (r) { return r.year === 2027 && /hawthorn/i.test(r.club); }),
    "…and every row of it is that club in that year");
  var r1s = futureIn("2027 1st");
  check(r1s.length > 1 && r1s.every(function (r) { return r.year === 2027 && r.round === 1; }),
    "'2027 1st' is every club's 2027 first — the club is the part left unnamed", String(r1s.length));
  check(uniq(r1s.map(function (r) { return r.club.length; })).length >= 1 &&
        Object.keys(r1s.reduce(function (s, r) { s[r.club] = 1; return s; }, {})).length === r1s.length,
    "…one row per club, no club listed twice");

  // PARTIAL CLUB NAMES WORK LIKE THE PLAYER SEARCH — a substring, not a whole-name match.
  check(futureIn("hawth 2027 4th").map(idOf).join() === target.map(idOf).join(),
    "a partial club name resolves exactly as a partial player name does (substring)");
  var mel = futureIn("melbourne 2028 1st");
  check(mel.length > 1 && mel.every(function (r) { return /melbourne/i.test(r.club); }),
    "…and a substring that names two clubs answers with both, rather than picking one",
    JSON.stringify(mel.map(function (r) { return r.club; })));

  /* ---- THE PRICES ARE THE LEDGER'S OWN. The desk computes nothing. -------------------------- */
  check(allFuture.every(function (r) { return byId[idOf(r)] && r.val === byId[idOf(r)].value; }),
    "every future pick is offered at the LEDGER's own year-weighted value — the desk re-derives no " +
    "price (2027 = (1/3 own + 2/3 round avg) x 0.9, 2028 = round avg x 0.8, enforced in the ingest)");
  check(allPicks.every(function (r) { return typeof r.val === "number" && isFinite(r.val) && r.val > 0; }),
    "…and the desk offers no asset it cannot price — every offered row carries a real figure");
  check(picksIn("12").every(function (r) { return r.year === base && r.val === pvc[String(r.n)]; }),
    "…while a base-year pick is still priced straight off the shipped PVC, this desk's founding source");

  /* ---- THE OWNER'S YEAR RULE, VISIBLE IN THE ROWS THE DESK OFFERS --------------------------- */
  /* "2028 picks are all worth the same for each round — it's too far away to use 2026 finishing
     positions to value them. 2027 is close enough you can infer some value from how the teams went
     this year, but not the full value of the pick." Asserted as the SHAPE of the pricing, never as a
     figure: the furthest year is flat within a round, the nearer one is not. */
  var far = futureYears[futureYears.length - 1], near = futureYears[0];
  function spread(y, r) {
    return Object.keys(priced.filter(function (p) { return p.year === y && p.round === r; })
      .reduce(function (s, p) { s[p.value] = 1; return s; }, {})).length;
  }
  var offeredRounds = T.pickRounds();
  check(offeredRounds.every(function (r) { return spread(far, r) === 1; }),
    "the FURTHEST year prices every pick in a round identically — the owner's rule, measured " +
    "(" + far + ": " + offeredRounds.map(function (r) { return "r" + r + "=" + spread(far, r); }).join(" ") + ")");
  check(offeredRounds.some(function (r) { return spread(near, r) > 1; }),
    "…and the NEARER year does not, so this year's finishing positions still move it " +
    "(" + near + ": " + offeredRounds.map(function (r) { return "r" + r + "=" + spread(near, r); }).join(" ") + ")");
  // ONE PRICE IS NOT ONE ASSET. Two clubs' furthest-year firsts cost the same and are still two rows.
  var flat = futureIn(far + " 1st");
  check(flat.length > 1 && uniq(flat.map(function (r) { return r.val; })).length === 1,
    "two clubs' " + far + " firsts really do carry one price…", JSON.stringify(uniq(flat.map(function (r) { return r.val; }))));
  check(Object.keys(flat.reduce(function (s, r) { s[r.club] = 1; return s; }, {})).length === flat.length,
    "…and they are STILL one row per club — equal prices are never folded into one asset");

  /* ---- THE POOL IS UNTOUCHED (law 4) -------------------------------------------------------- */
  check(T.matchItems("70").length === 1 && T.matchItems("70")[0].pool === true,
    "a number past the curve's end is THE POOL, not a phantom ordinal", JSON.stringify(T.matchItems("70")));
  check(T.matchItems("1000").length === 1 && T.matchItems("1000")[0].pool === true,
    "…and so is a number far past it");
  check(T.matchItems("pool").length === 1 && T.matchItems("pool")[0].pool === true,
    "'pool' still names the pool item");
  check(T.matchItems("pick pool").length === 1 && T.matchItems("pick pool")[0].pool === true,
    "…and so does 'pick pool', which is what a pool pick is actually called");
  check(T.matchItems("2029")[0] && T.matchItems("2029")[0].pool === true,
    "a four-digit number that is NOT an issued year stays a number, so it resolves to the pool",
    JSON.stringify(T.matchItems("2029")));
  check(!futureIn("2027 1st").some(function (r) { return r.pool; }) &&
        !T.matchItems("2027 1st").some(function (r) { return r.pool; }),
    "…and a later-year query is given NO pool item — the pool level is a base-year committed figure");

  /* THE ONE GENUINE AMBIGUITY, resolved by context and never by preference: "27" is both the owner's
     shorthand for 2027 and the ordinal pick 27, which this desk has answered since it opened. */
  var bare27 = picksIn("27");
  check(bare27.length === 1 && bare27[0].n === 27 && bare27[0].year === base,
    "bare '27' KEEPS its established meaning — ordinal pick 27 of the base year", JSON.stringify(bare27));
  check(futureIn("hawthorn 27").length > 0 &&
        futureIn("hawthorn 27").every(function (r) { return r.year === 2027; }),
    "…but '27' beside a club is the year, because nothing else it could be is on offer");

  /* ---- item 6: "PICK XX" FINDS THE PICK, AND "PICK" LISTS PICKS ------------------------------ */
  var asWords = T.matchItems("pick 62"), asDigits = T.matchItems("62");
  check(JSON.stringify(asWords) === JSON.stringify(asDigits),
    "'pick 62' and '62' are the SAME query — the phrasing cannot change the answer");
  var bare = T.matchItems("pick").filter(function (r) { return r.t === "pick"; });
  check(bare.length > 0, "'pick' on its own LISTS picks (it used to return two Picketts and no pick)");
  var pk = T.matchItems("pickett");
  check(pk.length > 0 && pk.every(function (r) { return r.t === "player"; }),
    "'pickett' is still a NAME search — the keyword is stripped, 'ett' names no club and is not digits, " +
    "so the parse declines the query", JSON.stringify(pk.map(function (r) { return r.label; })));
  var nobody = T.matchItems("zzz 2027 1st");
  check(nobody.length === 0,
    "a word that names no club declines the WHOLE query rather than half-answering it", JSON.stringify(nobody));
  check(T.matchItems("hawthorn 2027 62").length === 0,
    "…and so does a query that mixes the two asset languages: a later year has no ordinal to mix in");

  /* ---- item 5: THE LIST IS AS LONG AS THE MATCHES, AND NOT TRUNCATED SHORTER ----------------- */
  check(typeof T.MIN_ROWS === "number" && T.MIN_ROWS >= 5,
    "the desk publishes the owner's floor (" + T.MIN_ROWS + " rows) rather than a number retyped here");
  var five = T.matchItems("5"), ords5 = {};
  five.forEach(function (r) { if (r.t === "pick" && !r.pool) ords5[r.n] = 1; });
  check(five.length >= T.MIN_ROWS,
    "a query with matches to spare clears the floor ('5' -> " + five.length + " rows)");
  check(Object.keys(ords5).length >= 6 && ords5[5] && ords5[50],
    "…and the ordinal breadth of the old scan survives (exact match first, then the prefix run)",
    Object.keys(ords5).join(","));
  check(five[0] && five[0].n === 5, "the EXACT ordinal leads the list — typing '5' means pick 5, not pick 50");
  check(T.matchItems("hawthorn").length >= T.MIN_ROWS,
    "a bare club clears the floor too — the club's whole holding, every year", String(T.matchItems("hawthorn").length));
  /* A FLOOR IS NOT A PAD, and the owner's correction narrowed one query on purpose: "62" is Pick 62 and
     the pool again, because under his own ruling there is no 2027 pick 62 to be a third row. Nothing is
     invented to reach five. This is recorded as behaviour, not smuggled past. */
  check(T.matchItems("62").length === 2 && T.matchItems("62")[1].pool === true,
    "'62' is the base-year pick and the pool — a bare ordinal has no later-year sibling any more, and " +
    "the floor pads nothing to hide that", JSON.stringify(T.matchItems("62").map(function (r) { return r.label; })));
  check(T.matchItems("hawthorn 2027 4th").length === 1,
    "…and a query with exactly one true match returns exactly one row");

  /* THE YEAR ON A CHIP IS THE BOARD'S, not a string typed into the view — asserted by MOVING the base
     year rather than by grepping for the retired "2026 ND" literal (a text search cannot tell a live
     literal from the comment that records its retirement). The same move proves the ledger guard: with
     the desk's base year shifted, the ledger's base-year rows no longer agree with the PVC ordinal-for-
     ordinal, so it is no longer evidence that the ledger's other years are in these units — and NO
     future asset is offered, rather than a row the desk cannot honestly compare. */
  var moved = makeCtx();
  loadData(moved, path.join("data", "board_view_working.js"));
  moved.window.__MATCHDAY_WORKING__.stamp.baseYear = base + 1;
  loadData(moved, path.join("data", "club_valuation.js"));
  load(moved, "config.js"); load(moved, "format.js"); load(moved, "seam.js");
  load(moved, "club_totals.js"); load(moved, "trade.js");
  check(moved.MD.trade.pickYears()[0] === base + 1,
    "move the bundle's base year and the desk's first year moves with it — no year is written into the view",
    JSON.stringify(moved.MD.trade.pickYears()));
  check(moved.MD.trade.pickYears().length === 1 && moved.MD.trade.pickRounds().length === 0,
    "…and with the ledger no longer agreeing with the PVC on the base year, NO later year and NO round " +
    "is offered", JSON.stringify(moved.MD.trade.pickYears()) + " / " + JSON.stringify(moved.MD.trade.pickRounds()));
  check(moved.MD.trade.matchItems("hawthorn 2027 1st").every(function (r) { return r.t === "player"; }),
    "…so the club search itself goes quiet rather than pricing a ledger it cannot vouch for");
  check(moved.MD.trade.matchItems("5").filter(function (r) { return r.t === "pick" && !r.pool; })
        .every(function (r) { return r.year === base + 1; }),
    "…while every pick the moved desk still offers wears the moved year");
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
