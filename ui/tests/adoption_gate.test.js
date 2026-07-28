/* ADOPTION GATE — the shipped UI bundles against the board of record.
   Run:  node ui/tests/adoption_gate.test.js        (exit 0 = adopted and consistent, 1 = not)

   THIS IS NOT A PER-RUN TEST, AND IT IS EXPECTED TO BE RED FOR MOST OF A BUILD.

   `data/expected_boot.json` 'board' moves when the engine lands a new board. The UI bundles in
   ui/data/ move when someone regenerates them with ui/tools/extract_board_view.py. Those are two
   different moments on purpose: #217 moved the manifest to the new board and deliberately HELD the
   UI bundles until the owner adopts, so that the app keeps rendering the last adopted board while
   the baseline effort is in flight.

   So "bundle == manifest" is not an invariant. It is a RELEASE CONDITION that becomes true at the
   adoption step, and asserting it on every run would paint the suite permanently red for the whole
   baseline — a guard that always fails, which is exactly the shape issue #231 existed to remove.
   ui/tests/release_seam.test.js therefore asserts only what holds whatever is staged: the bundle's
   stamp.board matches its own board_md5, which is what ringFence() authenticates.

   Run THIS file at adoption, when the answer is supposed to be yes. A red here before adoption is
   information, not a defect: it tells you how far the UI is behind the engine. */
var fs = require("fs"), path = require("path");

var fails = 0, n = 0;
function check(cond, label, extra) {
  n++;
  if (cond) { console.log("  [PASS] " + label); }
  else { fails++; console.log("  [FAIL] " + label + (extra ? "  " + extra : "")); }
}

var REPO = path.join(__dirname, "..", "..");

function head(s) { return String(s || "").slice(0, 8); }

/* The board of record. Read from the manifest directly — this file is the one place that is
   allowed to, because it is the one check whose whole question is "has the UI caught up?". */
var BOOT = JSON.parse(fs.readFileSync(path.join(REPO, "data", "expected_boot.json"), "utf8"));
var RECORD = head(BOOT.board);

/* The shipped bundle, read as a generated artifact (window.__X__ = {...};). */
function bundle(name) {
  var src = fs.readFileSync(path.join(REPO, "ui", "data", name), "utf8");
  return JSON.parse(src.slice(src.indexOf("{"), src.lastIndexOf("}") + 1));
}

console.log("ADOPTION GATE — shipped UI bundles vs the board of record\n  " + "-".repeat(66));
console.log("  board of record (data/expected_boot.json) : " + RECORD);

check(/^[0-9a-f]{8}$/.test(RECORD),
  "board of record is an 8-hex id in data/expected_boot.json", "got " + RECORD);

var W = bundle("board_view_working.js");
var wMd5 = head(W.stamp.board_md5 || W.stamp.srcmd5);
var wRecord = head(W.stamp.board);
console.log("  shipped working bundle board_md5         : " + wMd5);

/* Internal consistency first — if this is red the bundle is corrupt, not merely behind, and the
   staleness answer below would be meaningless. */
check(wRecord === wMd5,
  "working bundle is internally consistent (stamp.board == board_md5)",
  "board " + wRecord + " vs md5 " + wMd5);

/* The adoption question itself. */
check(wMd5 === RECORD,
  "working bundle IS the board of record (adoption complete)",
  "bundle " + wMd5 + " vs manifest " + RECORD +
    " — the UI is holding an earlier board; regenerate via ui/tools/extract_board_view.py to adopt");

console.log("  " + "-".repeat(66));
if (fails) {
  console.log("  " + (n - fails) + "/" + n + " passed  (" + fails + " FAILED)");
  console.log("  NOT ADOPTED — this is the expected state while a board change is in flight.");
} else {
  console.log("  " + n + "/" + n + " passed — the shipped UI is the board of record.");
}
process.exit(fails ? 1 : 0);
