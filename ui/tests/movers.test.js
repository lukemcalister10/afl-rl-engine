/* UI — unit tests for the MOVERS view's pure logic (integrity, LINEAGE anchoring, sort, filters).
   Run:  node ui/tests/movers.test.js      (exit 0 = all pass, exit 1 = a failure)
   Exercises the EXACT dual-target functions the browser runs (ui/app/movers.js core). Validates the
   committed PRODUCTION bundle (ui/data/movers.js — the owner-authorised R15-R19 history, ITEM 408 Items
   6-7 Option A, bridged to the current accepted release by the owner-approved fail-closed provenance
   transition ui/data/movers_transition.js) and the R15-R19 SCRATCH EVIDENCE bundle
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
function clone(o) { return JSON.parse(JSON.stringify(o)); }

// ---- PRODUCTION bundle: owner-authorised R15-R19 history + fail-closed provenance transition ------
// ITEM 408 Items 6-7, Option A (owner ruling): the authorised R15-R19 recovery is GENUINE production
// Movers history — retained, NOT reset to empty — and displayed under the current accepted release via
// a SEPARATELY-DECLARED, owner-approved provenance transition. Positive + negative controls below.
var prodPath = path.join(__dirname, "..", "data", "movers.js");
var transPath = path.join(__dirname, "..", "data", "movers_transition.js");
var workingPath = path.join(__dirname, "..", "data", "board_view_working.js");
if (fs.existsSync(prodPath) && fs.existsSync(transPath) && fs.existsSync(workingPath)) {
  var prod = readBundle(prodPath);
  var trans = readBundle(transPath);
  var stamp = readBundle(workingPath).stamp;
  // the loaded current application identity, exactly as ui/app/movers.js appIdentity() derives it
  var rel = stamp.release || null;
  var curApp = {
    board: (rel && rel.board) || stamp.srcmd5 || stamp.board,
    store: (rel && rel.store) || stamp.store_md5 || stamp.store,
    balanced_board_md5: (rel && rel.balanced_board_md5) || stamp.balanced_board_md5,
    release_version: (rel && rel.release_version) || stamp.releaseVersion || stamp.tag,
    engine_head: (rel && rel.engine_head) || stamp.engine,
    register: (rel && rel.register) || stamp.register,
    as_of_round: (rel && rel.as_of_round != null) ? rel.as_of_round : stamp.asOfRound,
    release: rel,
  };

  // POSITIVE — the populated production bundle carries exactly R15-R19
  eq(prod.rounds, [15, 16, 17, 18, 19], "production ui/data/movers.js carries exactly R15-R19 (owner-authorised history)");
  ok(prod.reports && Object.keys(prod.reports).length === 5, "production bundle carries five reports (one per round)");
  // the complete historical board/store chain (baseline R14 -> R15 -> ... -> R19) is exact + continuous
  var chainOk = true, prevB = prod.baseline.board, prevS = prod.baseline.store;
  [15, 16, 17, 18, 19].forEach(function (r) {
    var rep = prod.reports[String(r)];
    if (rep.board_md5_before !== prevB || rep.source_store_md5_before !== prevS) chainOk = false;
    prevB = rep.board_md5_after; prevS = rep.source_store_md5_after;
  });
  ok(chainOk, "complete historical board/store chain R14->R19 is exact + continuous");
  // the latest report terminates at the accepted R19 materialised store of the recovery
  ok(prod.reports["19"].source_store_md5_after === "f37d9716648cfe4382b8c6a24c4f064f",
     "latest report terminates at the accepted R19 store f37d9716 (recovery materialisation)");
  // the transition is the owner-approved bridge and its content digest matches the restored reports
  ok(trans.kind === "movers_release_transition" && trans.owner_approved === true,
     "transition record is an owner-approved movers_release_transition");
  eq(trans.applies_to.historical_reports_digest, core.reportsDigest(prod, [15, 16, 17, 18, 19]),
     "transition digest matches the restored R15-R19 reports byte-for-byte (content anchor)");

  // POSITIVE — the owner-approved transition permits the exact historical lineage under the current app
  eq([core.lineage(prod, curApp, trans).ok, core.lineage(prod, curApp, trans).state], [true, "bridged"],
     "owner-approved transition bridges R15-R19 to the current accepted release (state=bridged)");
  // the current application identity EQUALS the transition destination
  ok(core.matchAppToDest(trans.destination, curApp).ok, "current application identity == transition destination");

  // NEGATIVE CONTROLS — each fails closed
  ok(!core.lineage(prod, curApp, null).ok, "the same bundle WITHOUT the transition fails closed");
  var tSrc = clone(trans); tSrc.source.balanced_board_md5 = "ffffffffffffffffffffffffffffffff";
  ok(!core.lineage(prod, curApp, tSrc).ok, "wrong transition SOURCE fails closed");
  var tDst = clone(trans); tDst.destination.board = "ffffffffffffffffffffffffffffffff";
  ok(!core.lineage(prod, curApp, tDst).ok, "wrong transition DESTINATION fails closed");
  var tRev = clone(trans); var sw = tRev.source; tRev.source = tRev.destination; tRev.destination = sw;
  ok(!core.lineage(prod, curApp, tRev).ok, "REVERSED transition (source<->destination) fails closed");
  var tNo = clone(trans); tNo.owner_approved = false;
  ok(!core.lineage(prod, curApp, tNo).ok, "a transition that is not owner-approved fails closed");
  var bId = clone(prod); bId.reports["18"].release_identity.engine_head = "deadbeefdeadbeefdeadbeefdeadbeef";
  ok(!core.lineage(bId, curApp, trans).ok, "a modified historical report IDENTITY fails closed");
  var bPl = clone(prod); bPl.reports["17"].players[3].value_change += 1;
  ok(!core.lineage(bPl, curApp, trans).ok, "modified player MOVEMENT data fails closed (content digest)");
  var bCh = clone(prod); bCh.reports["17"].board_md5_before = "deadbeef";
  ok(!core.lineage(bCh, curApp, trans).ok, "a modified board/store CHAIN fails closed");
  var bUn = clone(prod);
  [15, 16, 17, 18, 19].forEach(function (r) { bUn.reports[String(r)].release_identity.balanced_board_md5 = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"; });
  bUn.baseline.release_identity.balanced_board_md5 = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
  ok(!core.lineage(bUn, curApp, trans).ok, "an UNRELATED release lineage fails closed (transition cannot authorise it)");
  var appW = clone(curApp); appW.board = "ffffffffffffffffffffffffffffffff";
  ok(!core.lineage(prod, appW, trans).ok, "current application board != transition destination fails closed");

  // FUTURE APPEND — a next-round report appends under the then-current governing identity WITHOUT
  // altering R15-R19 (the historical content digest is unchanged; the future report carries destination).
  var digestBefore = core.reportsDigest(prod, [15, 16, 17, 18, 19]);
  var appended = clone(prod);
  var last19 = appended.reports["19"];
  appended.reports["20"] = {
    kind: "weekly_movers_report", submitted_round: 20, previous_round: 19,
    board_md5_before: last19.board_md5_after, board_md5_after: "20b0ard00000000000000000000000000",
    source_store_md5_before: last19.source_store_md5_after, source_store_md5_after: "20st0re00000000000000000000000000",
    release_identity: clone(trans.destination), players: [], views: {}, player_count: 0,
  };
  appended.rounds = [15, 16, 17, 18, 19, 20];
  eq(core.reportsDigest(appended, [15, 16, 17, 18, 19]), digestBefore,
     "future report append preserves all R15-R19 reports byte-for-byte (historical digest unchanged)");
  ok(appended.reports["20"].release_identity.release_version === trans.destination.release_version,
     "the appended future report carries the then-current governing identity (destination)");

  // NO score application: the movers module is pure view/lineage logic (no score-apply surface at all).
  eq(Object.keys(M).sort(), ["core", "makeView"], "movers module exports only pure view logic (applies NO scores)");
} else {
  console.log("  [skip] production movers bundle / transition / working board not present");
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
