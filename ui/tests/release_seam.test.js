/* v2.11 UI/RELEASE-SEAM — UI-side proof (exercises the EXACT shipped app files).
   Run:  node ui/tests/release_seam.test.js      (exit 0 = all pass, exit 1 = a failure)

   Loads the real ui/app/config.js, ui/app/seam.js and ui/app/main.js into a browser-like sandbox
   (window === global) and asserts:
     - the masthead release/round labels come from the stamp metadata contract (releaseVersion /
       asOfRound), and render a NEUTRAL unknown — never "v2.10" / "Round 17" — when metadata is absent;
     - the UI ring-fence (seam.js) still REFUSES a board whose md5 head != the expected board id. */
var fs = require("fs"), path = require("path"), vm = require("vm");

var fails = 0, n = 0;
function check(cond, label, extra) {
  n++;
  if (cond) { console.log("  [PASS] " + label); }
  else { fails++; console.log("  [FAIL] " + label + (extra ? "  " + extra : "")); }
}

function appSrc(name) { return fs.readFileSync(path.join(__dirname, "..", "app", name), "utf8"); }

/* A minimal browser-like context where `window` IS the global object, so both `window.MD = …`
   and bare `MD` resolve to the same namespace (exactly as in the browser). document.readyState is
   "loading" so main.js registers its listener but does NOT auto-render (no real DOM here). */
function makeCtx(globals) {
  var sandbox = { console: console };
  Object.keys(globals || {}).forEach(function (k) { sandbox[k] = globals[k]; });
  sandbox.window = sandbox;
  sandbox.document = {
    readyState: "loading",
    addEventListener: function () {},
    getElementById: function () { return null; },
  };
  vm.createContext(sandbox);
  return sandbox;
}
function load(ctx, name) { vm.runInContext(appSrc(name), ctx, { filename: name }); }

console.log("v2.11 UI/RELEASE-SEAM — UI proof (real config.js / seam.js / main.js)\n  " + "-".repeat(66));

// ================= no hardcoded round/version label survives in any UI display file ============
(function () {
  // "Round 17 ·" and a hardcoded "v2.10" masthead/strip literal must be gone from the display sites.
  ["main.js", "board.js"].forEach(function (name) {
    var src = appSrc(name);
    check(src.indexOf("Round 17 ") < 0, name + ": no hardcoded 'Round 17' display literal");
  });
})();

// ================= release / round labels (metadata contract, main.js) =========================
(function () {
  var ctx = makeCtx();
  load(ctx, "config.js");
  load(ctx, "main.js");
  var rel = ctx.MD.releaseLabel, rnd = ctx.MD.roundLabel;

  check(typeof rel === "function" && typeof rnd === "function",
    "main.js exposes MD.releaseLabel / MD.roundLabel");

  // present -> shows the boot-manifest values verbatim
  check(rel({ releaseVersion: "v2.11" }) === "v2.11", "releaseLabel shows the contract version verbatim",
    "got " + rel({ releaseVersion: "v2.11" }));
  check(rnd({ asOfRound: 14 }) === "Round 14", "roundLabel shows the contract round verbatim",
    "got " + rnd({ asOfRound: 14 }));

  // absent -> NEUTRAL unknown, and specifically never the old hardcoded labels
  var relMissing = [rel({}), rel({ releaseVersion: null }), rel({ releaseVersion: "" })];
  var rndMissing = [rnd({}), rnd({ asOfRound: null }), rnd({ asOfRound: "" })];
  check(relMissing.every(function (s) { return s === "unversioned"; }),
    "releaseLabel: missing version -> neutral 'unversioned'", JSON.stringify(relMissing));
  check(rndMissing.every(function (s) { return s === "Round —"; }),
    "roundLabel: missing round -> neutral 'Round —'", JSON.stringify(rndMissing));
  check(relMissing.every(function (s) { return s !== "v2.10"; }),
    "releaseLabel: missing version is NEVER 'v2.10'");
  check(rndMissing.every(function (s) { return s.indexOf("17") < 0; }),
    "roundLabel: missing round is NEVER 'Round 17'");
})();

// ================= ring-fence (seam.js) — UI refuses a mismatched board =========================
(function () {
  /* WHY THIS BLOCK LOOKS THE WAY IT DOES. Until 2026-07-28 it opened with
         var WANT = cfgCtx.MD.config.EXPECTED_BOARD;
     and built every fixture from that pin. So when the pin pointed at the wrong board, the fixtures
     pointed at the wrong board too, the fence agreed with itself, and this file reported 23/23 green
     for the entire outage it existed to catch — while ringFence() was rejecting the real shipped board
     and every tab in the app rendered the fail-closed panel. A test that draws its expectation from the
     thing under test cannot fail.

     Both identities below now come from OUTSIDE the app's own configuration — from the generated
     bundle, never from config.js — and the fixtures are fixed literals that no pin can drag along.
     A disagreement between the bundle's two identities, or a fence that stops keying on them, is
     now a red. */
  var TAIL = "deadbeefdeadbeefdeadbeef";
  var GOOD = "aaaa1111";
  var WRONG = "0badc0de";

  /* SCOPE OF THIS FILE — it asserts what the FENCE authenticates, and nothing about release state.
     The fence compares the bundle's computed board_md5 against the board of record the bundle itself
     carries in stamp.board. That relationship must hold for WHATEVER IS STAGED — a held bundle, an
     adopted one, a candidate mid-baseline — so this file stays green through all of them.

     Bundle-versus-MANIFEST is a different question with a different lifetime: it is only true at
     adoption. #217 moved data/expected_boot.json to the new board and deliberately held the UI
     bundles until the owner adopts, so asserting it here would paint this suite permanently red for
     the whole baseline effort — a guard that always fails, which is the shape this job exists to
     remove. That comparison lives in ui/tests/adoption_gate.test.js and runs at the adoption step. */
  var bundleSrc = fs.readFileSync(
    path.join(__dirname, "..", "data", "board_view_working.js"), "utf8");
  var SHIPPED = JSON.parse(bundleSrc.slice(bundleSrc.indexOf("{"), bundleSrc.lastIndexOf("}") + 1));
  var shippedMd5 = String(SHIPPED.stamp.board_md5 || SHIPPED.stamp.srcmd5 || "").slice(0, 8);
  var shippedRecord = String(SHIPPED.stamp.board || "").slice(0, 8);
  check(/^[0-9a-f]{8}$/.test(shippedMd5) && /^[0-9a-f]{8}$/.test(shippedRecord),
    "shipped bundle carries both a board_md5 and a board of record",
    "md5 " + shippedMd5 + " / board " + shippedRecord);
  check(shippedRecord === shippedMd5,
    "shipped bundle's stamp.board matches its own board_md5 (what ringFence authenticates)",
    "board " + shippedRecord + " vs md5 " + shippedMd5);

  // ---- the retired pin must not come back ----------------------------------------------------------
  var cfgCtx = makeCtx();
  load(cfgCtx, "config.js");
  check(cfgCtx.MD.config.EXPECTED_BOARD === undefined,
    "config.js carries NO hand-typed EXPECTED_BOARD pin (retired, issue #231)",
    "got " + JSON.stringify(cfgCtx.MD.config.EXPECTED_BOARD));
  check(appSrc("seam.js").indexOf("EXPECTED_BOARD") < 0,
    "seam.js reads no EXPECTED_BOARD constant");

  function fence(working) {
    var ctx = makeCtx({ __MATCHDAY_WORKING__: working });
    load(ctx, "config.js");
    load(ctx, "seam.js");
    return ctx.MD.seam.ringFence();
  }

  // ring-fence authenticates the INSTALLED WORKING BOARD only: board_md5 (|| srcmd5 alias)
  check(fence({ stamp: { board: GOOD + TAIL, board_md5: GOOD + TAIL } }).ok === true,
    "ring-fence ACCEPTS a bundle keyed by board_md5");
  check(fence({ stamp: { board: GOOD + TAIL, srcmd5: GOOD + TAIL } }).ok === true,
    "ring-fence ACCEPTS a legacy bundle keyed only by the srcmd5 alias");

  // the ring-fence uses BOARD identity only — a matching store/balanced but wrong board is refused
  var wrongBoard = fence({ stamp: { board: GOOD + TAIL, board_md5: WRONG + TAIL,
    store_md5: GOOD + TAIL, balanced_board_md5: GOOD + TAIL } });
  check(wrongBoard.ok === false && wrongBoard.got === WRONG && wrongBoard.want === GOOD,
    "ring-fence keys on board identity ONLY (store/balanced do not authenticate it)", JSON.stringify(wrongBoard));

  var bad = fence({ stamp: { board: GOOD + TAIL, board_md5: WRONG + TAIL } });
  check(bad.ok === false && bad.why === "board id mismatch",
    "ring-fence REFUSES a board that disagrees with the board of record (fail-closed)", JSON.stringify(bad));
  check(bad.got === WRONG && bad.want === GOOD,
    "ring-fence reports got/want for the fail-closed screen");

  // the fence's expectation TRACKS THE BUNDLE'S board of record — it is not a constant anywhere.
  // Feed a bundle declaring a different board of record and `want` must move with it.
  var moved = fence({ stamp: { board: WRONG + TAIL, board_md5: GOOD + TAIL } });
  check(moved.ok === false && moved.want === WRONG && moved.got === GOOD,
    "ring-fence's expectation comes from the bundle's board of record, not a pin", JSON.stringify(moved));

  // a bundle with NO board of record cannot be authenticated -> fail closed, never a silent pass
  var unstamped = fence({ stamp: { board_md5: GOOD + TAIL } });
  check(unstamped.ok === false && unstamped.why === "board of record missing from bundle stamp",
    "ring-fence REFUSES a bundle carrying no board of record", JSON.stringify(unstamped));
  var emptyBoth = fence({ stamp: {} });
  check(emptyBoth.ok === false,
    "ring-fence REFUSES a stamp with neither identity (no ''===''  silent pass)", JSON.stringify(emptyBoth));

  check(fence(null).ok === false, "ring-fence REFUSES a missing working bundle");

  // ---- THE REAL SHIPPED BUNDLE, through the real fence ---------------------------------------------
  // Exercises the actual generated artifact rather than a fixture: this is the assertion whose failure
  // means the app is dead on main.
  check(fence(SHIPPED).ok === true,
    "the REAL shipped bundle passes the ring-fence (the app renders)", JSON.stringify(fence(SHIPPED)));
})();

// ==== retro seam RETIRED; Round Δ is the one movement column (owner redesign 2026-08-28) =========
(function () {
  /* The retrospective bake-delta seam ("delta vs bake", retroFor, __MATCHDAY_RETRO__) was ruled OFF
     the product: the board's single movement figure is ROUND Δ — this round vs the previous round,
     from the latest weekly report of record. These checks pin the retirement (no half-removed
     machinery) and the replacement's exact data path. */
  function board(movers) {
    var ctx = makeCtx({
      MD: { fmt: {}, seam: { working: { stamp: {}, players: [] } }, state: {}, config: {} },
      __MATCHDAY_MOVERS__: movers,
    });
    load(ctx, "board.js");
    return ctx.MD.board;
  }

  // the retired machinery is GONE, not dormant
  check(typeof board(null).retroFor === "undefined",
    "retroFor is retired — board.js no longer exposes the bake-delta seam");
  check(appSrc("board.js").indexOf("__MATCHDAY_RETRO__") < 0,
    "board.js no longer reads the retro bundle at all");
  ["board.js", "card.js"].forEach(function (name) {
    var src = appSrc(name);
    check(src.indexOf("delta vs bake") < 0 && src.indexOf("over free") < 0,
      name + ": no 'delta vs bake' / 'over free' display text survives");
  });

  // the replacement: Round Δ from the LATEST weekly report of record
  var movers = {
    rounds: [22, 23],
    reports: {
      "22": { current_round: 22, previous_round: 21,
              players: [{ key: "p1", value_change: 999, prev_value: 1, cur_value: 1000 }] },
      "23": { current_round: 23, previous_round: 22,
              players: [{ key: "p1", value_change: -40, prev_value: 540, cur_value: 500 },
                        { key: "p2", value_change: 25, prev_value: 100, cur_value: 125 }] },
    },
  };
  var b = board(movers);
  check(typeof b.roundDeltas === "function", "board.js exposes roundDeltas (the Round Δ source)");
  var rd = b.roundDeltas();
  check(rd && rd._round === 23 && rd._prev === 22,
    "Round Δ is the LATEST report's round pair (23 vs 22), not an older report", JSON.stringify(rd && { r: rd._round, p: rd._prev }));
  check(rd && rd.p1 && rd.p1.d === -40 && rd.p1.prev === 540 && rd.p1.cur === 500,
    "Round Δ carries the report's own value_change/prev/cur per player", JSON.stringify(rd && rd.p1));
  check(rd && rd.p2 && rd.p2.d === 25, "every player in the report is covered");

  // empty-state safe: no movers bundle -> null, never a throw or an invented zero
  check(board(null).roundDeltas() === null,
    "no weekly report -> roundDeltas is null (renders '—', never an invented 0)");

  // no hardcoded identity fallbacks anywhere in board.js
  check(appSrc("board.js").indexOf("968de0c7") < 0 && appSrc("board.js").indexOf("06d8af60") < 0,
    "board.js hardcodes neither 968de0c7 nor 06d8af60");
})();

console.log("  " + "-".repeat(66));
console.log("  " + (n - fails) + "/" + n + " passed" + (fails ? "  (" + fails + " FAILED)" : ""));
process.exit(fails ? 1 : 0);
