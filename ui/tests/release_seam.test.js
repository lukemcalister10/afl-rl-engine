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
  // config.js pins the expected board id; the fence compares the working stamp's md5 head to it.
  var cfgCtx = makeCtx();
  load(cfgCtx, "config.js");
  var WANT = cfgCtx.MD.config.EXPECTED_BOARD;
  var TAIL = "deadbeefdeadbeefdeadbeef";
  check(/^[0-9a-f]{8}$/.test(WANT), "config.EXPECTED_BOARD is an 8-hex board pin", "got " + WANT);

  function fence(working) {
    var ctx = makeCtx({ __MATCHDAY_WORKING__: working });
    load(ctx, "config.js");
    load(ctx, "seam.js");
    return ctx.MD.seam.ringFence();
  }

  // ring-fence authenticates the INSTALLED WORKING BOARD only: board_md5 (|| srcmd5 alias)
  check(fence({ stamp: { board_md5: WANT + TAIL } }).ok === true,
    "ring-fence ACCEPTS a bundle keyed by board_md5");
  check(fence({ stamp: { srcmd5: WANT + TAIL } }).ok === true,
    "ring-fence ACCEPTS a legacy bundle keyed only by the srcmd5 alias");
  // the ring-fence uses BOARD identity only — a matching store/balanced but wrong board is refused
  var wrongBoard = fence({ stamp: { board_md5: "0badc0de" + TAIL, store_md5: WANT + TAIL,
    balanced_board_md5: WANT + TAIL } });
  check(wrongBoard.ok === false && wrongBoard.got === "0badc0de" && wrongBoard.want === WANT,
    "ring-fence keys on board identity ONLY (store/balanced do not authenticate it)", JSON.stringify(wrongBoard));

  var bad = fence({ stamp: { board_md5: "0badc0de" + TAIL } });
  check(bad.ok === false && bad.why === "board id mismatch",
    "ring-fence REFUSES a mismatched board (fail-closed)", JSON.stringify(bad));
  check(bad.got === "0badc0de" && bad.want === WANT,
    "ring-fence reports got/want for the fail-closed screen");

  check(fence(null).ok === false, "ring-fence REFUSES a missing working bundle");
})();

// ==== retrospective seam (board.js) — real F2 contract: store_md5 AND balanced_board_md5 ==========
(function () {
  var TAIL = "deadbeefdeadbeefdeadbeef";
  var STORE = "968de0c7", BAL = "06d8af60";       // the real F2 stamp values (heads)
  function board(working, retro) {
    var ctx = makeCtx({
      MD: { fmt: {}, seam: { working: working }, state: {}, config: {} },
      __MATCHDAY_RETRO__: retro,
    });
    load(ctx, "board.js");
    return ctx.MD.board;
  }
  // working stamp AFTER a bake set balanced_board_md5; store_md5 is the verified store.
  var wBaked = { stamp: { board_md5: "aaaa1111" + TAIL, store_md5: STORE + TAIL, balanced_board_md5: BAL + TAIL } };
  // working stamp on THIS prep branch: balanced not set yet.
  var wPrep = { stamp: { board_md5: "aaaa1111" + TAIL, store_md5: STORE + TAIL, balanced_board_md5: null } };
  var goodEntry = { stamp: { store_md5: STORE, balanced_board_md5: BAL } };  // F2-shaped (8-hex heads)

  check(typeof board(wBaked, null).retroFor === "function",
    "board.js exposes retroFor (the exact retro identity check)");

  // both F2 identities present + matching -> ok
  check(board(wBaked, { "-1": goodEntry }).retroFor(1).state === "ok",
    "retro ACCEPTS an F2 stamp with matching store_md5 AND balanced_board_md5");

  // wrong store identity -> mismatch, names store_md5
  var mStore = board(wBaked, { "-1": { stamp: { store_md5: "ffff9999", balanced_board_md5: BAL } } }).retroFor(1);
  check(mStore.state === "mismatch" && mStore.field === "store_md5" && mStore.got === "ffff9999" && mStore.want === STORE,
    "retro REFUSES a wrong store_md5 and names the field", JSON.stringify(mStore));

  // wrong balanced-board identity -> mismatch, names balanced_board_md5
  var mBal = board(wBaked, { "-1": { stamp: { store_md5: STORE, balanced_board_md5: "ffff9999" } } }).retroFor(1);
  check(mBal.state === "mismatch" && mBal.field === "balanced_board_md5" && mBal.got === "ffff9999" && mBal.want === BAL,
    "retro REFUSES a wrong balanced_board_md5 and names the field", JSON.stringify(mBal));

  // balanced_board_md5 not set yet (prep) -> pending, never ok, even with a fully-matching store
  check(board(wPrep, { "-1": goodEntry }).retroFor(1).state === "pending",
    "retro stays PENDING while balanced_board_md5 is unset (no premature ok)");

  // no retro bundle -> pending (empty-state safe)
  check(board(wBaked, null).retroFor(1).state === "pending",
    "retro with no bundle stays empty-state 'pending'");

  // no hardcoded identity fallbacks anywhere in board.js
  check(appSrc("board.js").indexOf("968de0c7") < 0 && appSrc("board.js").indexOf("06d8af60") < 0,
    "board.js retro check hardcodes neither 968de0c7 nor 06d8af60");
})();

console.log("  " + "-".repeat(66));
console.log("  " + (n - fails) + "/" + n + " passed" + (fails ? "  (" + fails + " FAILED)" : ""));
process.exit(fails ? 1 : 0);
