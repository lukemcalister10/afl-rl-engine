/* Matchday UI — configuration. UI-side only; no values, no recomputation. */
window.MD = window.MD || {};

MD.config = {
  /* Ring-fence: the UI refuses to render any board whose md5 head != this expected board id
     (md5(rl_app_data.json) == the pinned board id; the UI analogue of Guard 5, fail-closed).
     Moved 9ecbe0fa -> de4baef9 (ID-primary migration 2026-07-12) -> 81e48293 (v2.9 BAKE 2026-07-13:
     L7 numéraire re-base + adopted-curve repoint + Brodie owner override) -> 3dc19fbb (ITEM 20 store-
     identity job 2026-07-13: afl_club import + club-display repoint + bramble +1; display-only board
     move, engine ev() unchanged). The UI board pin tracks the shipped board, same as
     data/expected_boot.json 'board'; the refreshed board_view bundles carry srcmd5 3dc19fbb. Moved
     3dc19fbb -> 790136a3 (v2.10 CAPTAINCY BAKE, tag d14efaef: the L-CAPTAIN ruled captain curve lifts the
     guns + load-time re-normalisation; display-only for the UI — no value is computed here). The pin moves
     with the tagged board, per the v1.1 base rule: bundles regenerate via extract_board_view.py from the tag.
     Moved 790136a3 -> 06d8af60 (v2.11-rc1 RELEASE CANDIDATE, release/v2.11-rc1: the installed balanced board
     of record data/expected_boot.json 'board' = full md5 06d8af60b679a12db07c064c60c065f9, RL_LEGE=0 RL_LEGF=0
     RL_PVC2=1 on engine cc626d7d/904722cd, store 968de0c7; display-only for the UI — no value is computed here.
     The seam authenticates working.stamp.board_md5[:8] == this id). */
  EXPECTED_BOARD: "06d8af60",

  /* Q-DELTA-BASE (owner-worded 2026-07-12): the toggle is BUILT; default = (a) last accepted bake NOW.
     "default flips to (b) previous-round AT GO-LIVE" — ship the flip as THIS ONE LINE, not a rebuild. */
  DELTA_BASE_DEFAULT: "bake", // "bake" (a) today · flip to "round" (b) at go-live.

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
