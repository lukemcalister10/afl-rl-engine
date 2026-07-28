/* Matchday UI — configuration. UI-side only; no values, no recomputation. */
window.MD = window.MD || {};

MD.config = {
  /* EXPECTED_BOARD IS GONE — retired 2026-07-28 by owner word (issue #231), and nothing replaces it here.

     It was a hand-typed copy of the shipped board id, and on 2026-07-28 it killed the app. R20's board
     reached main at fef7f69; this constant did not follow; ringFence() rejected the shipped board and
     EVERY tab rendered the fail-closed panel. One board move was enough. It was corrected hours later at
     6d8f910, but the shape was the defect, not the lapse: a value a human has to retype whenever
     something moves will eventually not be retyped.

     The ring-fence keeps its job and loses that failure mode. It now reads the BOARD OF RECORD out of the
     working bundle's own stamp (`stamp.board`), which extract_board_view.py copies verbatim from
     data/expected_boot.json 'board' and asserts against the artifact md5 at generation time. Two values
     with different provenance — one computed from the board's bytes, one declared by the manifest — and
     neither of them typed by hand. See ringFence() in seam.js.

     What authenticates staleness is ui/tests/release_seam.test.js, which reads data/expected_boot.json
     directly: the browser cannot open the manifest from file://, but the test can, so drift between the
     shipped bundle and the board of record is caught in the repo rather than in the user's face.

     DO NOT reintroduce a board id in this file. */

  /* Q-DELTA-BASE (owner-worded 2026-07-12): the toggle is BUILT; default = (a) last accepted bake NOW.
     "default flips to (b) previous-round AT GO-LIVE" — ship the flip as THIS ONE LINE, not a rebuild. */
  DELTA_BASE_DEFAULT: "round", // "bake" (a) today · flip to "round" (b) at go-live.

  /* ±1/2-yr board lens (completion-path requirement). Index 2 == now (BASE_YEAR).
     Maps to lens = [vM2, vM1, v, vP1, vP2] = ev @ 2024/2025/2026/2027/2028 (rl_export.py:66). */
  LENS_DEFAULT: 2,
  LENS_LABELS: ["−2 yr", "−1 yr", "Now", "+1 yr", "+2 yr"],

  /* item 178(1) CLUB-NAME WRAP FIX (owner-worded 2026-07-16): a DISPLAY-NAME MAP for exactly the three
     owner-named AFFL clubs whose full nicknames break two lines. DISPLAY-ONLY — the long name stays the
     join key everywhere (bundle affl_team, the picks-Owner join, the club-filter value); only the
     rendered string is shortened. Any club not in this map renders verbatim. */
  CLUB_DISPLAY: {
    "North Melbourne Kangaroos": "North Melbourne",
    "Collingwood Magpies": "Collingwood",
    "Port Adelaide Power": "Port Adelaide",
  },
};

/* ANCHOR MANIFEST — the owner's acceptance reads (documented, owner-worded). Working tier only.
   key · direction text · status: "met" (filled pin) | "watch" (hollow pin, not-yet/directional).
   Where the board makes the read verifiable it is cross-checked in code (see MD.anchorStatus). */
MD.anchors = {
  "marcus-bontempelli": { read: "up ≥10%", status: "met" },
  "sam-darcy":          { read: "lifts (runway)", status: "watch" },
  "jeremy-cameron":     { read: "up", status: "met" },
  "max-gawn":           { read: "clearly above Kieren Briggs", status: "met", vs: "kieren-briggs" },
  "willem-duursma":     { read: "runway credit lands", status: "watch" },
  "stephen-coniglio":   { read: "fades", status: "met" },
};

/* Verifiable anchors get their pin lit from the real board, not from the manifest's stored guess.
   Gawn>Briggs is checkable today; the rest fall back to the documented ruling status. */
MD.anchorStatus = function (key, byKey) {
  const a = MD.anchors[key];
  if (!a) return null;
  if (a.vs && byKey[key] && byKey[a.vs]) {
    return { read: a.read, status: byKey[key].v > byKey[a.vs].v ? "met" : "watch", verified: true };
  }
  return { read: a.read, status: a.status, verified: false };
};
