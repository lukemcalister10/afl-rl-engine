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

/* =============== the FROM/TO SCOPE ============================================================= */
section("(3) from/to — scoped to the R22 → R23 boundary, machinery intact");
(function () {
  var movers = require(path.join(UI, "app", "movers.js"));
  var core = movers.core;

  check(core.SCOPE && String(core.SCOPE.from) === "22" && String(core.SCOPE.to) === "23",
    "the scope is declared as R22 -> R23", JSON.stringify(core.SCOPE));

  var live = null;
  try {
    var ctx = makeCtx();
    loadData(ctx, path.join("data", "movers.js"));
    live = ctx.window.__MATCHDAY_MOVERS__;
  } catch (e) { /* bundle absent -> the shipped-bundle assertions below are skipped, loudly */ }

  if (!live) {
    check(false, "the shipped movers bundle loads (needed for the scope assertions)");
  } else {
    var all = core.points(live), scoped = core.scopedPoints(live);
    check(scoped.length === 2, "the shipped bundle can honour the scope", "got " + scoped.length);
    check(scoped.map(function (p) { return String(p.id); }).join(",") === "22,23",
      "and it resolves to exactly [22, 23] in from->to order",
      scoped.map(function (p) { return p.id; }).join(","));
    check(all.length > scoped.length,
      "the scope really narrows the selector (" + scoped.length + " of " + all.length + " stored points)");
    // the machinery is NOT removed: any pair still compares
    var wide = core.compare(live, "20", "23");
    check(wide && wide.players && wide.players.length > 0,
      "core.compare still answers for an out-of-scope pair — the scope is display, not capability");
  }

  var src = appSrc("movers.js");
  check(src.indexOf("retrospective") > 0 && src.indexOf("QUEUED post-model-confidence") > 0,
    "the future retrospective-view ask is recorded in the code, not built");
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

/* =============== (c) dRound — the dead assertions and the bridge are gone ====================== */
section("(c) dRound — the false comments and the bridge they justified are removed");
(function () {
  var board = appSrc("board.js"), card = appSrc("card.js"), config = appSrc("config.js");

  /* NOTE ON THESE ASSERTIONS: both files now QUOTE the retracted claim in order to retract it, so
     asserting the absence of the old sentence would fail on the correction itself. What must be true
     is that the MECHANISM is gone and the CORRECTION is stated. That is what is checked. */
  check(board.indexOf("w.dRound") < 0,
    "the name->key dRound bridge is DELETED, not left returning null");
  check(board.indexOf("REMOVED") > 0 && board.indexOf("premise was never true") > 0,
    "board.js records that the premise was false, so the bridge is not rebuilt from the same belief");
  check(board.indexOf("no writer") > 0, "board.js names the real cause (no writer) where the field is read");
  check(card.indexOf("CORRECTED 2026-08-21") > 0 && card.indexOf("It does not, and it never did") > 0,
    "card.js retracts the claim in place rather than leaving it to be believed again");
  check(card.indexOf("not published") > 0, "…and the public card prints the honest state");

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
  var card = appSrc("card.js");
  check(card.indexOf("renders the moment the") < 0, "the 'awaiting the export field' notice is gone");
  // the header quotes the old shape in order to explain the mismatch; what must be gone is the WAIT.
  check(card.indexOf("G-ATTR already requires these to exist") < 0,
    "the card no longer tells the owner the field is missing");
  check(card.indexOf("leverBlock(p)") > 0, "the panel now renders the shipped block");
  ["L1", "L2", "L3", "L4", "L5"].forEach(function (c) {
    check(new RegExp("\\b" + c + ":\\s*\\{").test(card), "the label map names " + c);
  });
  check(card.indexOf("RL_PVCADOPT") > 0 && card.indexOf("RL_DIAL14") > 0 && card.indexOf("RL_AGE") > 0,
    "and it names the env dials the certified chain toggled — the map is sourced, not invented");
  check(card.indexOf("path-additive") > 0 || card.indexOf("chain’s") > 0,
    "the fixed-order caveat (G-ATTR is path-additive) is stated on the panel");
  check(card.indexOf("resid") > 0, "the unattributed residual has its own bar");

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

  var board = appSrc("board.js");
  check(board.indexOf("forward-lens toggle is RE-ENABLED") < 0,
    "the stale 'RE-ENABLED' comment that licensed this is gone");
  check(board.indexOf("MD.lensClamp(s.lens)") > 0, "the board clamps at render, so a restored snapshot cannot smuggle one in");
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
  var snap = B.snapshot();
  check("cohortFilter" in snap && "ageFilter" in snap && "eligFilter" in snap && "v0Col" in snap,
    "the snapshot carries the new filters and the column lens, so Back restores the board you were on",
    JSON.stringify(Object.keys(snap)));
  B.restore({ cohortFilter: "2024", ageFilter: "b:-20", eligFilter: "KPF", v0Col: true });
  var snap2 = B.snapshot();
  check(snap2.cohortFilter === "2024" && snap2.ageFilter === "b:-20" && snap2.eligFilter === "KPF" &&
        snap2.v0Col === true, "…and restore round-trips them", JSON.stringify(snap2));
  B.restore({ cohortFilter: null, ageFilter: null, eligFilter: null, v0Col: false });
})();

console.log("\n  " + "-".repeat(72));
console.log(fails ? ("UI ACT 2026-08-21: " + fails + " FAIL / " + n)
                  : ("UI ACT 2026-08-21: ALL " + n + " PASS"));
process.exit(fails ? 1 : 0);
