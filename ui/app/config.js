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

  /* FREE-HIT VALUE — the ruled constant behind the "over free" lens (#274 item 3).

     THE RULING (#270 FHV definitional ruling, owner word 2026-07-29: "Yes, option A"): free-hit value is
     defined on the EXPECTATION view, as a SINGLE constant, working value ≈190. The survivor-conditioned
     readings were rejected as definitions — 250 is the listed survivors' median and 528 (`pool_value`) is
     cleared by 8% of entrants ever, and the study measured the survivor overstatement at 2–3× on means.
     No per-access-position schedule: order within a window carries no usable signal (pooled rho ≈ −0.15).

     THE INTEGER, with its denominators, fixed by this consumer as the ruling requires. The study's basis:
     mature-cohort mean 193 (2015–23 entries, n=200, busts and departed counted at 0) and all-years mean
     178 (n=389). 190 is taken because it is the constant the ruling itself carries as its working value,
     and because each alternative has a defect the study names: 193's n=200 excludes in-flight recent
     entrants, and 178's n=389 is cohort-age dominated (the study's own presentation guard). It also keeps
     this consumer consistent with #276's phantom, which takes "the ruled FHV (≈190)" at its fire.

     A LENS, NEVER A STORED FIGURE. `v − FHV` is computed at render, every time, and written nowhere: no
     bundle field, no baked file, no re-pin. That is deliberate — a stored derived figure is exactly the
     staleness that took the club totals out (see ui/app/club_totals.js). Changing this one number moves
     the column and the below-free flag together and touches nothing else.

     The per-window schedule (MSD ~352 / SSP ~277 / OTHER ~97) is the recorded upgrade path and is one
     owner word away; nothing here blocks it. */
  FHV: 190,

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
