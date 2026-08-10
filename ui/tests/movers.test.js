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
  };
  return Object.assign(b, over || {});
}
var APP = mkApp(16, "B2", "S2");   // loaded app: current board B2, store S2, on the release lineage

console.log("MOVERS-VIEW TESTS\n  " + "-".repeat(60));

// integrity: valid passes; each failure mode fail-closes
ok(core.integrity(mkReport()).ok, "valid report passes integrity");
ok(!core.integrity(null).ok, "null report fails closed");
ok(!core.integrity(mkReport({ board_md5_after: null })).ok, "missing committed board id fails closed");
ok(!core.integrity(mkReport({ release_identity: null })).ok, "missing release identity fails closed");
ok(!core.integrity(mkReport({ integrity: { board_after_matches_committed: false } })).ok, "board mismatch fails closed");
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
ok(core.lineage(mkBundle(), mkApp(16, "B2", "SXX")).ok, "same newest board, differing store: displayed (transition is no longer a gate)");
// same board/store, WRONG release_version
ok(core.lineage(mkBundle(), mkApp(16, "B2", "S2", { release_version: "v9.9" })).ok, "differing release_version: displayed (enforcement removed)");
// WRONG engine / fv / config / register
ok(core.lineage(mkBundle(), mkApp(16, "B2", "S2", { engine_head: "deadbeef" })).ok, "differing engine_head: displayed (enforcement removed)");
ok(core.lineage(mkBundle(), mkApp(16, "B2", "S2", { fv: "deadbeef" })).ok, "differing fv: displayed (enforcement removed)");
ok(core.lineage(mkBundle(), mkApp(16, "B2", "S2", { config: "deadbeef" })).ok, "differing config: displayed (enforcement removed)");
ok(core.lineage(mkBundle(), mkApp(16, "B2", "S2", { register: "deadbeef" })).ok, "differing register: displayed (enforcement removed)");
// THE ONE ASSERT that replaced all of the above — non-vacuity, both directions:
ok(!core.lineage(mkBundle(), mkApp(16, "BXX", "S2")).ok, "ONE ASSERT: newest stored point != loaded board fails closed");
ok(core.lineage(mkBundle(), mkApp(16, "B2", "S2")).ok, "ONE ASSERT: newest stored point == loaded board passes");
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
ok(core.lineage(chainBreak, APP).ok, "a board-identity discontinuity is DISPLAYED, not rejected (chain removed 2026-07-28)");
var storeBreak = mkBundle(); storeBreak.reports["16"].source_store_md5_before = "XXX";
ok(core.lineage(storeBreak, APP).ok, "a store-identity discontinuity is DISPLAYED, not rejected (chain removed 2026-07-28)");
// latest report board / store must equal the loaded current board / store
ok(!core.lineage(mkBundle(), mkApp(16, "OTHER_BOARD", "S2")).ok, "latest report board != loaded current board fails closed");
// as_of_round coherence
var badAsof = mkBundle(); badAsof.reports["16"].release_identity.as_of_round = 14;
ok(!core.lineage(badAsof, APP).ok, "incoherent as_of_round fails closed");
// non-sequential rounds
var gap = mkBundle(); gap.reports["16"].previous_round = 14;
ok(core.lineage(gap, APP).ok, "non-sequential points are DISPLAYED — from/to needs no consecutive series");

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

  // POSITIVE — the populated production bundle carries exactly R15-R22
  eq(prod.rounds, [15, 16, 17, 18, 19, 20, 21, 22], "production ui/data/movers.js carries R15-R22");
  ok(prod.reports && Object.keys(prod.reports).length === 8, "production bundle carries eight reports (one per round)");
  // the complete historical board/store chain (baseline R14 -> R15 -> ... -> R19) is exact + continuous
  var chainOk = true, prevB = prod.baseline.board, prevS = prod.baseline.store;
  [15, 16, 17, 18, 19].forEach(function (r) {
    var rep = prod.reports[String(r)];
    if (rep.board_md5_before !== prevB || rep.source_store_md5_before !== prevS) chainOk = false;
    prevB = rep.board_md5_after; prevS = rep.source_store_md5_after;
  });
  ok(chainOk, "complete historical board/store chain R14->R19 is exact + continuous");
  // the latest report terminates at the R19 materialised store of the recovery. f37d9716 was the
  // ACCEPTED store when these reports were materialised; ITEM 411 D1 landed 2026-07-27 and the accepted
  // store is now c120cfd5. The historical reports are immutable, so this terminus is unchanged history
  // and the literal stays as the drift sentinel.
  ok(prod.reports["19"].source_store_md5_after === "f37d9716648cfe4382b8c6a24c4f064f",
     "latest report terminates at the R19 recovery-materialised store f37d9716 (history; superseded as the accepted store by ITEM 411 D1 c120cfd5)");
  // the transition is the owner-approved bridge and its content digest matches the restored reports
  ok(trans.kind === "movers_release_transition" && trans.owner_approved === true,
     "transition record is an owner-approved movers_release_transition");
  eq(trans.applies_to.historical_reports_digest, core.reportsDigest(prod, [15, 16, 17, 18, 19]),
     "transition digest matches the restored R15-R19 reports byte-for-byte (content anchor)");

  // POSITIVE — the bundle displays under the current app. The transition is NO LONGER A GATE
  // (owner word 2026-07-28): it is read by the producer to LABEL model-change ranges, and the record
  // itself is untouched and still owner-approved. It is passed here only to prove it is ignored.
  //
  // RESTATED at #274 item 1 (owner word 2026-07-30, amending #271 A22's acceptance test). This
  // asserted `[true, "ok"]`, written when the bundle's newest report was generated under the loaded
  // release. Post-adoption the history predates the live release, so `lineage()` reports `bridged` —
  // ok:true, the tab displays, which is the whole of what the 2026-07-28 law requires. `bridged` is
  // the honest state, not a defect: it says "this bundle's history was made under an earlier release
  // and is shown under the current one," which is exactly true.
  //
  // MEASURED, so the expectation is set on fact rather than hope (#271 A22 note 4 asked for this):
  // at its writing the state did NOT self-resolve, because `lineage()` compared the bundle's frozen
  // LINEAGE anchor (06d8af60) against the loaded app's balanced_board_md5, which fell through to the
  // current board-ARTIFACT hash (4939d740) — apples to oranges, the three-way balanced_board_md5 item
  // DOCKETED TO HYGIENE by #271 A17.
  // RESOLVED 2026-08-06 (seam ruling, R21 apply): the R21 finalization now emits a `release` block in
  // the board stamp (manifest_source: expected_boot + release_lineage), so curApp.balanced_board_md5
  // carries the immutable present-lens anchor 06d8af60 — release_lineage.json declares it CONSTANT
  // across weekly rounds — and lineage() compares like with like. The state is honestly `ok`: same
  // present-lens lineage end to end. Era boundaries still surface via the owner-approved
  // model_changes entries below, so nothing provenance-bearing is hidden. #271 A17 closed.
  // RESTATED 2026-08-10 (#334 DOB courier landing, board 6e724cca -> a672ed3a): the expected state is
  // `bridged` again, and that is the honest reading, not a weakening. `ok` is the DIRECT-lineage branch,
  // which requires the latest ROUND REPORT's terminal board to equal the loaded board. This act moved the
  // board OUTSIDE a round, so R22's report keeps its own frozen terminal board (6e724cca — a later act
  // never rewrites an earlier report's identity, #271 A15/A16) while the app serves a672ed3a. That is
  // exactly the situation this file's own note above describes: "this bundle's history was made under an
  // earlier release and is shown under the current one, which is exactly true." The out-of-round column
  // `dob-courier-10-8` carries the live board, so THE ONE ASSERT (newest stored point == loaded board)
  // still passes — which is why the state is `bridged` and not `mismatch`. Nothing is loosened: the two
  // non-vacuity assertions immediately below still prove `bridged` discriminates (a foreign board fails
  // closed, and the same bundle loaded at its own terminal identity still reads `ok`).
  eq([core.lineage(prod, curApp, trans).ok, core.lineage(prod, curApp, trans).state], [true, "bridged"],
     "bundle displays under the current app, bridged — history made under an earlier release, shown under the current one (the board moved outside a round)");
  // NON-VACUITY for the restated assertion, both directions. `bridged` is a state this check can
  // FAIL to reach: a bundle on a foreign lineage does not get bridged, it fails closed as a mismatch.
  var appForeign = clone(curApp); appForeign.board = "ffffffffffffffffffffffffffffffff";
  eq([core.lineage(prod, appForeign, trans).ok, core.lineage(prod, appForeign, trans).state],
     [false, "mismatch"],
     "NON-VACUITY: a bundle whose newest point is not the loaded board is refused, not bridged");
  // and "ok" is still REACHABLE — proving `bridged` discriminates rather than being whatever this
  // function now returns for everything. Loaded at the bundle's OWN terminal identity, the same
  // bundle takes the direct branch and reads "ok".
  var lastR = prod.reports[String(prod.rounds[prod.rounds.length - 1])];
  var relOwn = lastR.release_identity;
  var appOwn = { board: lastR.board_md5_after, store: lastR.source_store_md5_after,
                 balanced_board_md5: relOwn.balanced_board_md5, release_version: relOwn.release_version,
                 release: relOwn };
  eq([core.lineage(prod, appOwn, trans).ok, core.lineage(prod, appOwn, trans).state], [true, "ok"],
     "NON-VACUITY: loaded at the bundle's own terminal identity the SAME bundle reads ok — bridged is a discriminating state");
  // THE HYGIENE ITEM (#271 A17) — RETIRED 2026-08-06, exactly as its own comment instructed ("if
  // this ever starts failing, the hygiene item has been resolved and the assertion above should be
  // revisited"). It started failing at the R21 apply: the stamp's new `release` block carries the
  // lineage anchor, the anchors now AGREE, and the disagreement this assertion kept loud no longer
  // exists. The inverted assertion below pins the resolved state so a regression re-opens loudly.
  ok(prod.baseline.release_identity.balanced_board_md5 === curApp.balanced_board_md5,
     "RESOLVED (#271 A17, 2026-08-06): bundle baseline anchor " +
     String(prod.baseline.release_identity.balanced_board_md5).slice(0, 8) +
     " now agrees with the loaded app's " + String(curApp.balanced_board_md5).slice(0, 8) +
     " — the reason the state is ok, not bridged");
  ok(core.lineage(prod, curApp, null).ok, "the same bundle WITHOUT a transition also displays (gate removed)");
  // the app has ADVANCED PAST the transition destination — that record now describes a historical
  // boundary (R19 -> the restructure board fa172ac1), not the current release.
  ok(!core.matchAppToDest(trans.destination, curApp).ok,
     "app has advanced past the transition destination — the record is history, not the current release");
  ok(trans.destination.board === "fa172ac1c90ab84e5044d3e9907c5819",
     "transition destination is the restructure board — the boundary the tab labels");

  // THE MODEL-CHANGE LABEL replaced the gate: the boundary is declared in the bundle, not enforced.
  //
  // RESTATED at #274 item 1 (ERA SUCCESSION). This asserted EXACTLY ONE boundary, which was true when
  // the ITEM 408 restructure was the only out-of-round board move in the system's life. Adoption made
  // a second one — the 30/7 rederivation column — so a fixed count of 1 is now a stale expectation
  // rather than a property worth holding. What IS worth holding, and is asserted instead: EVERY
  // out-of-round boundary is anchored to an owner-approved record. That is the property era succession
  // exists to deliver, and it grows correctly with the register instead of pinning a number.
  var mc = prod.model_changes || [];
  // BUMPED 2026-08-10 (#334 DOB courier landing): a fourth out-of-round boundary, `dob-courier-10-8` —
  // the 302 birthdates plus the owner-authorised v0surf re-cut, board 6e724cca -> a672ed3a. Exactly the
  // growth the note above predicted ("it grows correctly with the register instead of pinning a number").
  // The durable property — EVERY boundary anchored to an owner-approved record — is asserted below and
  // covers the new entry too; this line only counts.
  ok(mc.length === 4, "four out-of-round boundaries are declared (the restructure, the 30/7 rederivation, the 6/8 adoption, the 10/8 DOB courier)  (got " + mc.length + ")");
  ok(mc[0].between[0] === "19" && mc[0].between[1] === "post-r19-redesign-1" &&
     mc[0].owner_approved_record === true,
     "model change declared between R19 and the restructure point, anchored to the owner-approved record");
  ok(mc[1].between[0] === "20" && mc[1].between[1] === "rederivation-30-7" &&
     mc[1].owner_approved_record === true,
     "model change declared between R20 and the 30/7 rederivation, anchored to the owner-approved record");
  ok(mc[2].between[0] === "rederivation-30-7" && mc[2].between[1] === "redesign-adoption-6-8" &&
     mc[2].owner_approved_record === true &&
     String(mc[2].owner_ruling_id) === "ADOPTION_2026-08-06_review_era",
     "model change declared between the 30/7 rederivation and the 6/8 adoption, anchored to the owner-approved adoption record");
  // The 30/7 boundary names the ruling that approved it. Until #274 this read `false`/null — the
  // declared plumbing lag of #271 A22 item 3, cleared by reading the whole register.
  eq(mc[1].owner_ruling_id, ["ITEM_271_Addendum_17"],
     "the 30/7 boundary carries its own owner ruling id (A22's known-false flag is cleared)");
  // and EVERY boundary is approved — the property, stated once over all of them.
  ok(mc.every(function (c) { return c.owner_approved_record === true && c.owner_ruling_id; }),
     "EVERY declared out-of-round boundary is anchored to an owner-approved record");
  ok(core.spansModelChange(prod, "19", "20").length === 1, "a range spanning the restructure is LABELLED");
  ok(core.spansModelChange(prod, "post-r19-redesign-1", "20").length === 0, "a range inside one model is not");

  // WHAT STILL FAILS CLOSED — the one assert, both directions (non-vacuity).
  ok(core.lineage(prod, curApp, trans).ok, "ONE ASSERT: newest stored point == loaded board passes");
  var appW = clone(curApp); appW.board = "ffffffffffffffffffffffffffffffff";
  ok(!core.lineage(prod, appW, trans).ok, "ONE ASSERT: newest stored point != loaded board fails closed");

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
