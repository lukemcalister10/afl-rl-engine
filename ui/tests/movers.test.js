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

/* A minimal coherent two-round bundle: baseline board B0; R15 (B0->B1), R16 (B1->B2). */
function mkBundle(over) {
  function rep(rn, bb, ba, sb, sa) {
    return { kind: "weekly_movers_report", submitted_round: rn, previous_round: rn - 1,
             board_md5_before: bb, board_md5_after: ba, source_store_md5_before: sb, source_store_md5_after: sa,
             release_identity: { release_version: "candidate:B0" }, board: ba,
             integrity: { players_unique: true, coverage_full: true, board_after_matches_committed: true },
             views: { played_count: 1, dnp_count: 0 }, player_count: 1,
             players: [{ key: "a", name: "A", played: true, dnp: false, cur_value: 100, value_change: 1, rank_change: 0, pos_rank_change: 0 }] };
  }
  var b = {
    kind: "matchday_movers_bundle", rounds: [15, 16],
    baseline: { as_of_round: 14, board: "B0", store: "S0" },
    reports: { "15": rep(15, "B0", "B1", "S0", "S1"), "16": rep(16, "B1", "B2", "S1", "S2") },
    integrity: { board_chain_ok: true, baseline_anchor_ok: true, rounds: [15, 16] },
  };
  return Object.assign(b, over || {});
}

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

// ---- LINEAGE anchoring (directive E) --------------------------------------------------------
// empty bundle -> honest empty state (NOT an alarm), ok:true
var emptyBundle = { kind: "matchday_movers_bundle", rounds: [], reports: {}, baseline: { as_of_round: 14, board: "B0" }, integrity: { board_chain_ok: true, baseline_anchor_ok: true } };
var linEmpty = core.lineage(emptyBundle, { board: "B0" });
eq([linEmpty.ok, linEmpty.state], [true, "empty"], "empty bundle -> honest empty state (not an alarm)");
// coherent bundle, latest report board == loaded app board -> ok
eq([core.lineage(mkBundle(), { board: "B2" }).ok, core.lineage(mkBundle(), { board: "B2" }).state], [true, "ok"], "coherent bundle anchored to the loaded app passes lineage");
// a SCRATCH bundle beginning at the superseded board 270a2c5f must FAIL CLOSED vs the RC baseline 06d8af60
var scratch = mkBundle({ baseline: { as_of_round: 14, board: "270a2c5f", store: "S0" } });
scratch.reports["15"].board_md5_before = "270a2c5f"; // begins at the superseded board
var linRC = core.lineage(scratch, { board: "06d8af60" });  // loaded app is on the RC baseline lineage
ok(!linRC.ok && linRC.state === "mismatch", "scratch bundle (begins 270a2c5f) fails closed vs RC baseline 06d8af60");
// baseline-anchor break: first report's board_before != bundle baseline board
var badBase = mkBundle(); badBase.reports["15"].board_md5_before = "ZZZ";
ok(!core.lineage(badBase, { board: "B2" }).ok, "baseline-anchor break fails closed");
// board-chain break between rounds
var chainBreak = mkBundle(); chainBreak.reports["16"].board_md5_before = "XXX";
ok(!core.lineage(chainBreak, { board: "B2" }).ok, "board-identity chain break fails closed");
// store-chain break between rounds
var storeBreak = mkBundle(); storeBreak.reports["16"].source_store_md5_before = "XXX";
ok(!core.lineage(storeBreak, { board: "B2" }).ok, "store-identity chain break fails closed");
// latest finalized report must match the loaded app board
ok(!core.lineage(mkBundle(), { board: "SOME_OTHER_BOARD" }).ok, "latest report not matching the loaded app fails closed");
// non-sequential rounds
var gap = mkBundle(); gap.reports["16"].previous_round = 14;
ok(!core.lineage(gap, { board: "B2" }).ok, "non-sequential previous_round fails closed");

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
  eq(core.lineage(prod, { board: prod.baseline.board }).state, "empty", "production bundle renders the honest EMPTY state");
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
  // lineage passes against ITS OWN baseline app (the last committed scratch board)
  var lastRep = sb.reports[String(sb.rounds[sb.rounds.length - 1])];
  ok(core.lineage(sb, { board: lastRep.board_md5_after }).ok, "scratch bundle is self-coherent against its own last board");
  var allGood = true, dnpSeen = false;
  sb.rounds.forEach(function (r) {
    var rep = sb.reports[String(r)];
    var ig = core.integrity(rep, sb);
    if (!ig.ok) { allGood = false; console.log("    round " + r + " integrity: " + ig.why); }
    var keys = {}; rep.players.forEach(function (p) { keys[p.key] = (keys[p.key] || 0) + 1; if (p.dnp) dnpSeen = true; });
    if (Object.keys(keys).length !== rep.players.length) allGood = false;
    if (rep.release_identity && rep.release_identity.tag === "v2.10") allGood = false;  // no hardcoded tag
  });
  ok(allGood, "every scratch round report passes integrity + unique coverage + no hardcoded v2.10 tag");
  ok(dnpSeen, "scratch reports represent DNP players");
} else {
  console.log("  [skip] scratch evidence bundle not present (run generate_movers_bundle.py)");
}

console.log("  " + "-".repeat(60));
if (fails) { console.log("MOVERS TESTS: " + fails + " FAIL / " + n); process.exit(1); }
console.log("MOVERS TESTS: ALL " + n + " PASS");
