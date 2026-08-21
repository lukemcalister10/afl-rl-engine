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
     "default flips to (b) previous-round AT GO-LIVE" — ship the flip as THIS ONE LINE, not a rebuild.

     FLIPPED BACK TO "bake", 2026-08-21, ON A MEASUREMENT AND NOT A PREFERENCE. The go-live flip to
     "round" was made on the belief that `dRound` would be populated by then. It is not, and never has
     been: 0 of 804 rows carry `dRound` (or `dRoundRank`) on BOTH shipped bundles, and no production
     writer exists — the exported row schema in engine/rl_after/rl_export.py `player_rec()` has never
     contained the key. So the default basis was rendering a column of dashes on every row of the
     owner's primary surface, which is the UI review's "dead columns ship by default" finding arriving
     through a one-line default. `vPrev` IS populated 804/804, so "bake" is the basis that has a number.

     This changes NO value and NO ordering — it selects which of two given figures the Δ column
     subtracts. The toggle keeps both options; the unfed one is disabled AT RENDER by measuring the
     loaded board (see board.js `basisFed`), so the day a dRound writer lands the button lights itself
     and this line can flip again with the same one-line edit the ruling always intended. */
  DELTA_BASE_DEFAULT: "bake", // (a) last accepted bake — the basis the board actually carries today.

  /* ±1/2-yr board lens (completion-path requirement). Index 2 == now (BASE_YEAR).
     Maps to lens = [vM2, vM1, v, vP1, vP2] = ev @ 2024/2025/2026/2027/2028 (rl_export.py:66). */
  LENS_DEFAULT: 2,
  LENS_LABELS: ["−2 yr", "−1 yr", "Now", "+1 yr", "+2 yr"],

  /* ===== THE +1/+2 PROJECTION LENSES ARE OFF (LENS-PROJECTION law, register v46) ==================
     RE-IMPOSED 2026-08-21 ON THE OWNER'S WORD. His words this session:

       "I don't currently use the +1/2 projections... I'd like to, if they genuinely work."

     THE RULING BEHIND IT (register v46, owner word 2026-07-13, "B, clearly") found the forward lenses
     wrong — the owner independently re-observed it as "the +1/+2 lenses are broken — everyone is
     losing value" — and the mitigation of record was explicit: "The UI meanwhile DISABLES the +1/+2
     toggle (tooltip: lands next chapter) so ruled-wrong numbers are never shown."

     THE MITIGATION LAPSED, AND THAT IS WHY THIS CONSTANT EXISTS RATHER THAN A COMMENT. A later
     ratification carried a binding expiry ("the deferral dies at the NEXT ROUND ADVANCE — from the R20
     bake onward the forward/projection view must regenerate with the live board"), the expiry passed,
     and the REBUILD never shipped — no register entry records the LENS PROJECTION build delivering,
     and none records the toggle being deliberately re-enabled on the strength of a fix. board.js
     carried a comment saying the lenses were "RE-ENABLED … the projection law (R103.3) has landed";
     the rebuild it cites is still queued, so a ruled-wrong number was one click from the board.

     WHAT THIS DOES: the two forward buttons are disabled and carry the note; a lens index in this list
     can never become the active lens (board.js clamps it at render, so a restored snapshot or a stale
     bookmark cannot smuggle one back in); the −2/−1/Now lenses are untouched, being real backward
     re-values and the live board.

     WHAT THIS DOES NOT DO: it does not attempt the rebuild. That is engine-side, rides the merged
     PVC+FLEX chapter, and stays queued. LIFTING THIS IS ONE LINE — empty the list — and it should be
     lifted only on the owner's word after the rebuild lands, never because the column looks empty. */
  LENS_DISABLED: [3, 4],
  LENS_DISABLED_NOTE: "+1/+2 under rebuild per ruling",
  LENS_DISABLED_WHY:
    "The +1/+2 projection lenses are OFF. The owner ruled these numbers wrong (register v46, " +
    "2026-07-13) and the rebuild has not shipped, so the forward view is withheld rather than " +
    "shown wrong. It returns when the LENS PROJECTION rebuild lands and the owner says so.",

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
