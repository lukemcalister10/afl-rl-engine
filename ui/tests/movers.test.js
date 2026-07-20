/* UI — unit tests for the MOVERS view's pure logic (integrity, deterministic sort, filters, views).
   Run:  node ui/tests/movers.test.js      (exit 0 = all pass, exit 1 = a failure)
   Exercises the EXACT dual-target functions the browser runs (ui/app/movers.js core). Also validates
   the committed movers bundle (ui/data/movers.js) if present. Browser-integration + styling + player-
   link + screenshot evidence is produced by ui/tools/movers_ui_check.mjs (headless Chromium). */
var M = require("../app/movers.js");
var core = M.core;
var fs = require("fs"), path = require("path");

var fails = 0, n = 0;
function ok(cond, label) { n++; if (cond) console.log("  [PASS] " + label); else { fails++; console.log("  [FAIL] " + label); } }
function eq(got, want, label) { ok(JSON.stringify(got) === JSON.stringify(want), label + "  (got " + JSON.stringify(got) + ")"); }

function mkReport(over) {
  var base = {
    kind: "weekly_movers_report", submitted_round: 16, previous_round: 15,
    board_md5_before: "b15", board_md5_after: "b16", release_identity: { tag: "v2.10" },
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

// ---- committed bundle (if generated) --------------------------------------------------------
var bundlePath = path.join(__dirname, "..", "data", "movers.js");
if (fs.existsSync(bundlePath)) {
  var txt = fs.readFileSync(bundlePath, "utf8");
  var obj = JSON.parse(txt.slice(txt.indexOf("{"), txt.lastIndexOf("}") + 1));
  eq(obj.rounds, [15, 16, 17, 18, 19], "committed bundle carries R15-R19");
  ok(obj.integrity.board_chain_ok, "committed bundle board-identity chain coherent");
  var allGood = true, dnpSeen = false;
  obj.rounds.forEach(function (r) {
    var rep = obj.reports[String(r)];
    var ig = core.integrity(rep, obj);
    if (!ig.ok) { allGood = false; console.log("    round " + r + " integrity: " + ig.why); }
    var keys = {}; rep.players.forEach(function (p) { keys[p.key] = (keys[p.key] || 0) + 1; if (p.dnp) dnpSeen = true; });
    if (Object.keys(keys).length !== rep.players.length) allGood = false;   // unique coverage
  });
  ok(allGood, "every committed round report passes integrity + unique player coverage");
  ok(dnpSeen, "committed reports represent DNP players");
} else {
  console.log("  [skip] committed ui/data/movers.js not present (run generate_movers_bundle.py)");
}

console.log("  " + "-".repeat(60));
if (fails) { console.log("MOVERS TESTS: " + fails + " FAIL / " + n); process.exit(1); }
console.log("MOVERS TESTS: ALL " + n + " PASS");
