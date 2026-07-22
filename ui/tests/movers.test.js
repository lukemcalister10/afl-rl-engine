/* UI — unit tests for the MOVERS view's pure logic (integrity, LINEAGE anchoring, sort, filters).
   Run:  node ui/tests/movers.test.js      (exit 0 = all pass, exit 1 = a failure)
   Exercises the EXACT dual-target functions the browser runs (ui/app/movers.js core). Validates the
   committed PRODUCTION bundle (ui/data/movers.js — ships EMPTY) and the R15-R19 SCRATCH EVIDENCE bundle
   (session_2026-07-20/live_scoring_catchup/movers_bundle_scratch.js). Browser-integration + styling +
   player-link + screenshot evidence is produced by ui/tools/movers_ui_check.mjs (headless Chromium). */
var M = require("../app/movers.js");
var core = M.core;
var fs = require("fs"), path = require("path");

var fails = 0, n = 0;
function ok(cond, label) { n++; if (cond) console.log("  [PASS] " + label); else { fails++; console.log("  [FAIL] " + label); } }
function eq(got, want, label) { ok(JSON.stringify(got) === JSON.stringify(want), label + "  (got " + JSON.stringify(got) + ")"); }

function mkReport(over) {
  var base = {
    kind: "weekly_movers_report", submitted_round: 16, previous_round: 15,
    board_md5_before: "b15", board_md5_after: "b16",
    source_store_md5_before: "s15", source_store_md5_after: "s16",
    release_identity: { release_version: "candidate:270a2c5f", as_of_round: 16 },
    integrity: { players_unique: true, coverage_full: true, board_after_matches_committed: true },
    views: { played_count: 3, dnp_count: 1 },
    players: [
      { key: "a", name: "A", affl_team: "X", pos: "Mid", played: true, dnp: false, score: 120, cur_value: 900, prev_value: 800, value_change: 100, value_change_pct: 12.5, cur_rank: 1, prev_rank: 3, rank_change: 2, prev_pos_rank: 2, cur_pos_rank: 1, pos_rank_change: 1 },
      { key: "b", name: "B", affl_team: "Y", pos: "Ruck", played: true, dnp: false, score: 0, cur_value: 500, prev_value: 560, value_change: -60, value_change_pct: -10.7, cur_rank: 4, prev_rank: 2, rank_change: -2, prev_pos_rank: 1, cur_pos_rank: 2, pos_rank_change: -1 },
      { key: "c", name: "C", affl_team: "X", pos: "Mid", played: true, dnp: false, score: 70, cur_value: 700, prev_value: 700, value_change: 0, value_change_pct: 0, cur_rank: 2, prev_rank: 1, rank_change: -1, prev_pos_rank: 1, cur_pos_rank: 2, pos_rank_change: -1 },
      { key: "d", name: "D", affl_team: "Y", pos: "Fwd", played: false, dnp: true, score: null, cur_value: 650, prev_value: 640, value_change: 10, value_change_pct: 1.6, cur_rank: 3, prev_rank: 5, rank_change: 2, prev_pos_rank: 3, cur_pos_rank: 2, pos_rank_change: 1 },
    ],
  };
  return Object.assign(base, over || {});
}

/* The FIXED release-baseline identity (immutable across weekly rounds; balanced_board_md5 is the fixed
   present-lens baseline anchor, not a final full-board hash). */
var FIX = { release_version: "v2.11-present-lens-baseline", balanced_board_md5: "06d8af60", engine_head: "40f43772",
            rl_model: "a5fd3d7d", fv: "de4c7ec3", config: "c2d233ae", register: "652d83e8" };
function mkRel(rn, board, store, over) {
  return Object.assign({}, FIX, { board: board, store: store, as_of_round: rn }, over || {});
}
function mkApp(rn, board, store, relOver) { return { board: board, store: store, release: mkRel(rn, board, store, relOver) }; }

/* A minimal coherent two-round bundle: baseline board B0/store S0; R15 (B0->B1), R16 (B1->B2). */
function mkBundle(over) {
  function rep(rn, bb, ba, sb, sa) {
    return { kind: "weekly_movers_report", submitted_round: rn, previous_round: rn - 1,
             board_md5_before: bb, board_md5_after: ba, source_store_md5_before: sb, source_store_md5_after: sa,
             release_identity: mkRel(rn, ba, sa),
             integrity: { players_unique: true, coverage_full: true, board_after_matches_committed: true },
             views: { played_count: 1, dnp_count: 0 }, player_count: 1,
             players: [{ key: "a", name: "A", played: true, dnp: false, cur_value: 100, value_change: 1, rank_change: 0, pos_rank_change: 0 }] };
  }
  var b = {
    kind: "matchday_movers_bundle", rounds: [15, 16],
    baseline: { as_of_round: 14, board: "B0", store: "S0", release_identity: mkRel(14, "B0", "S0") },
    reports: { "15": rep(15, "B0", "B1", "S0", "S1"), "16": rep(16, "B1", "B2", "S1", "S2") },
    integrity: { board_chain_ok: true, baseline_anchor_ok: true, rounds: [15, 16] },
  };
  return Object.assign(b, over || {});
}
var APP = mkApp(16, "B2", "S2");   // loaded app: current board B2, store S2, on the release lineage

console.log("MOVERS-VIEW TESTS\n  " + "-".repeat(60));

// integrity: valid passes; each failure mode fail-closes
ok(core.integrity(mkReport(), { integrity: { board_chain_ok: true } }).ok, "valid report passes integrity");
ok(!core.integrity(null).ok, "null report fails closed");
ok(!core.integrity(mkReport({ board_md5_after: null })).ok, "missing committed board id fails closed");
ok(!core.integrity(mkReport({ release_identity: null })).ok, "missing release identity fails closed");
ok(!core.integrity(mkReport({ integrity: { board_after_matches_committed: false } })).ok, "board mismatch fails closed");
ok(!core.integrity(mkReport(), { integrity: { board_chain_ok: false } }).ok, "broken board chain fails closed");
var dup = mkReport(); dup.players = dup.players.concat([dup.players[0]]);
ok(!core.integrity(dup).ok, "duplicate player rows fail closed");

// ---- FULL release-lineage anchoring (directive D; owner ruling on balanced_board_md5) --------
// coherent populated bundle against the loaded release -> ok
eq([core.lineage(mkBundle(), APP).ok, core.lineage(mkBundle(), APP).state], [true, "ok"], "coherent bundle passes full-identity lineage");
// EMPTY coherent bundle -> honest empty state (validated vs the loaded app first)
var emptyOk = { kind: "matchday_movers_bundle", rounds: [], reports: {}, baseline: { as_of_round: 14, board: "B0", store: "S0", release_identity: mkRel(14, "B0", "S0") }, integrity: {} };
eq([core.lineage(emptyOk, mkApp(14, "B0", "S0")).ok, core.lineage(emptyOk, mkApp(14, "B0", "S0")).state], [true, "empty"], "empty bundle on the loaded lineage -> honest empty state");
// EMPTY bundle on the WRONG lineage fails closed (empty 270a2c5f bundle vs a DIFFERENT baseline board)
var emptyDf = { kind: "matchday_movers_bundle", rounds: [], reports: {}, baseline: { as_of_round: 14, board: "270a2c5f", store: "968de0c7", release_identity: mkRel(14, "270a2c5f", "968de0c7") }, integrity: {} };
var eMis = core.lineage(emptyDf, mkApp(14, "06d8af60", "otherstore"));
ok(!eMis.ok && eMis.state === "mismatch", "empty 270a2c5f bundle vs a different baseline board fails closed (not empty state)");
// same board, WRONG store (current-store mismatch)
ok(!core.lineage(mkBundle(), mkApp(16, "B2", "SXX")).ok, "same board but wrong current store fails closed");
// same board/store, WRONG release_version
ok(!core.lineage(mkBundle(), mkApp(16, "B2", "S2", { release_version: "v9.9" })).ok, "same board/store but wrong release_version fails closed");
// WRONG engine / fv / config / register
ok(!core.lineage(mkBundle(), mkApp(16, "B2", "S2", { engine_head: "deadbeef" })).ok, "wrong engine_head fails closed");
ok(!core.lineage(mkBundle(), mkApp(16, "B2", "S2", { fv: "deadbeef" })).ok, "wrong fv fails closed");
ok(!core.lineage(mkBundle(), mkApp(16, "B2", "S2", { config: "deadbeef" })).ok, "wrong config fails closed");
ok(!core.lineage(mkBundle(), mkApp(16, "B2", "S2", { register: "deadbeef" })).ok, "wrong register fails closed");
// a report carrying a DIFFERENT balanced_board_md5 than the fixed baseline
var badBB = mkBundle(); badBB.reports["16"].release_identity.balanced_board_md5 = "ffffffff";
ok(!core.lineage(badBB, APP).ok, "a report with a different balanced_board_md5 fails closed");
// baseline board / store anchor breaks
var badBase = mkBundle(); badBase.reports["15"].board_md5_before = "ZZZ";
ok(!core.lineage(badBase, APP).ok, "baseline board-anchor break fails closed");
var badBaseS = mkBundle(); badBaseS.reports["15"].source_store_md5_before = "ZZZ";
ok(!core.lineage(badBaseS, APP).ok, "baseline store-anchor break fails closed");
// board / store chain breaks
var chainBreak = mkBundle(); chainBreak.reports["16"].board_md5_before = "XXX";
ok(!core.lineage(chainBreak, APP).ok, "board-identity chain break fails closed");
var storeBreak = mkBundle(); storeBreak.reports["16"].source_store_md5_before = "XXX";
ok(!core.lineage(storeBreak, APP).ok, "store-identity chain break fails closed");
// latest report board / store must equal the loaded current board / store
ok(!core.lineage(mkBundle(), mkApp(16, "OTHER_BOARD", "S2")).ok, "latest report board != loaded current board fails closed");
// as_of_round coherence
var badAsof = mkBundle(); badAsof.reports["16"].release_identity.as_of_round = 14;
ok(!core.lineage(badAsof, APP).ok, "incoherent as_of_round fails closed");
// non-sequential rounds
var gap = mkBundle(); gap.reports["16"].previous_round = 14;
ok(!core.lineage(gap, APP).ok, "non-sequential previous_round fails closed");

// deterministic sort + tie-break (primary field, then cur_value desc, then key asc)
eq(core.viewRows(mkReport(), "value_risers", {}).map(function (p) { return p.key; }), ["a", "d", "c", "b"], "value risers order");
eq(core.viewRows(mkReport(), "value_fallers", {}).map(function (p) { return p.key; }), ["b", "c", "d", "a"], "value fallers order");
// rank risers: a(+2) and d(+2) tie -> cur_value desc a(900)>d(650); then c(-1); then b(-2)
eq(core.viewRows(mkReport(), "rank_risers", {}).map(function (p) { return p.key; }), ["a", "d", "c", "b"], "rank risers deterministic tie-break (a before d)");

// filters
eq(core.filter(mkReport().players, { club: "X" }).map(function (p) { return p.key; }), ["a", "c"], "club filter");
eq(core.filter(mkReport().players, { pos: "Mid" }).map(function (p) { return p.key; }), ["a", "c"], "position filter");
eq(core.filter(mkReport().players, { status: "dnp" }).map(function (p) { return p.key; }), ["d"], "DNP filter keeps DNP player");
eq(core.filter(mkReport().players, { status: "played" }).map(function (p) { return p.key; }), ["a", "b", "c"], "played filter");

// DNP players remain in the complete view (not omitted)
ok(core.viewRows(mkReport(), "all", {}).some(function (p) { return p.key === "d" && p.dnp; }), "DNP player present in the complete table");
// a listed score of 0 is a played score (not DNP)
ok(mkReport().players.find(function (p) { return p.key === "b"; }).played === true, "listed score of 0 is PLAYED");

// summary headline movers
var s = core.summary(mkReport());
eq([s.value_increase.key, s.value_decrease.key, s.rank_improve.key, s.rank_decline.key], ["a", "b", "a", "b"], "summary headline movers");

function readBundle(p) { var t = fs.readFileSync(p, "utf8"); return JSON.parse(t.slice(t.indexOf("{"), t.lastIndexOf("}") + 1)); }

// ---- PRODUCTION bundle ships EMPTY (directive A) --------------------------------------------
var prodPath = path.join(__dirname, "..", "data", "movers.js");
if (fs.existsSync(prodPath)) {
  var prod = readBundle(prodPath);
  eq(prod.rounds, [], "production ui/data/movers.js ships EMPTY (no finalized rounds)");
  ok(prod.reports && Object.keys(prod.reports).length === 0, "production bundle carries no reports");
  ok(prod.baseline && typeof prod.baseline.board === "string", "production bundle carries a release-baseline block");
  ok(prod.baseline.release_identity && prod.baseline.release_identity.balanced_board_md5 === "06d8af60b679a12db07c064c60c065f9",
     "production baseline carries the fixed present-lens baseline balanced_board_md5 (06d8af60)");
  // honest empty state when the loaded app matches the baseline; fail-closed when it does not
  var pApp = { board: prod.baseline.board, store: prod.baseline.store, release: prod.baseline.release_identity };
  eq(core.lineage(prod, pApp).state, "empty", "production bundle renders the honest EMPTY state on its lineage");
  eq(core.lineage(prod, { board: "06d8af60b679a12db07c064c60c065f9", store: "x", release: null }).state, "mismatch",
     "production empty bundle fails closed when loaded against a different board");
} else {
  console.log("  [skip] production ui/data/movers.js not present");
}

// ---- SCRATCH EVIDENCE bundle (R15-R19) — preserved under the session proof path -------------
var scratchPath = path.join(__dirname, "..", "..", "session_2026-07-20", "live_scoring_catchup", "movers_bundle_scratch.js");
if (fs.existsSync(scratchPath)) {
  var sb = readBundle(scratchPath);
  eq(sb.rounds, [15, 16, 17, 18, 19], "scratch evidence bundle carries R15-R19");
  ok(sb.integrity.board_chain_ok, "scratch evidence board-identity chain coherent");
  ok(sb.integrity.baseline_anchor_ok, "scratch evidence anchors to its own baseline board");
  // full-identity lineage passes against ITS OWN loaded app (the last committed scratch board/store/release)
  var lastRep = sb.reports[String(sb.rounds[sb.rounds.length - 1])];
  var sApp = { board: lastRep.board_md5_after, store: lastRep.source_store_md5_after, release: lastRep.release_identity };
  ok(core.lineage(sb, sApp).ok, "scratch bundle passes full-identity lineage against its own last board/store/release");
  // the PERMANENT balanced_board_md5 is identical across every scratch round (never per-round board)
  ok(sb.rounds.every(function (r) { return (sb.reports[String(r)].release_identity || {}).balanced_board_md5 === "06d8af60b679a12db07c064c60c065f9"; }),
     "every scratch report carries the same fixed balanced_board_md5 (06d8af60)");
  var allGood = true, dnpSeen = false;
  sb.rounds.forEach(function (r) {
    var rep = sb.reports[String(r)];
    var ig = core.integrity(rep, sb);
    if (!ig.ok) { allGood = false; console.log("    round " + r + " integrity: " + ig.why); }
    var keys = {}; rep.players.forEach(function (p) { keys[p.key] = (keys[p.key] || 0) + 1; if (p.dnp) dnpSeen = true; });
    if (Object.keys(keys).length !== rep.players.length) allGood = false;
    if (rep.release_identity && rep.release_identity.tag === "v2.10") allGood = false;  // no hardcoded tag
    if (rep.release_identity && rep.release_identity.balanced_board_md5 === rep.board_md5_after) allGood = false;  // never synthesized
  });
  ok(allGood, "every scratch round report: integrity + unique coverage + no v2.10 tag + balanced not synthesized");
  ok(dnpSeen, "scratch reports represent DNP players");
} else {
  console.log("  [skip] scratch evidence bundle not present (run generate_movers_bundle.py)");
}

console.log("  " + "-".repeat(60));
if (fails) { console.log("MOVERS TESTS: " + fails + " FAIL / " + n); process.exit(1); }
console.log("MOVERS TESTS: ALL " + n + " PASS");
