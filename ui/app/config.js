/* Matchday UI — configuration. UI-side only; no values, no recomputation. */
window.MD = window.MD || {};

MD.config = {
  /* Ring-fence: the UI refuses to render any board whose md5 head != this expected board id
     (md5(rl_app_data.json) == the pinned board id; the UI analogue of Guard 5, fail-closed).
     Moved 9ecbe0fa -> de4baef9 (ID-primary migration 2026-07-12) -> 81e48293 (v2.9 BAKE 2026-07-13:
     L7 numéraire re-base + adopted-curve repoint + Brodie owner override) -> 3dc19fbb (ITEM 20 store-
     identity job 2026-07-13: afl_club import + club-display repoint + bramble +1; display-only board
     move, engine ev() unchanged). The UI board pin tracks the shipped board, same as
     data/expected_boot.json 'board'; the refreshed board_view bundles carry srcmd5 3dc19fbb. */
  EXPECTED_BOARD: "3dc19fbb",

  /* Q-DELTA-BASE (owner-worded 2026-07-12): the toggle is BUILT; default = (a) last accepted bake NOW.
     "default flips to (b) previous-round AT GO-LIVE" — ship the flip as THIS ONE LINE, not a rebuild. */
  DELTA_BASE_DEFAULT: "bake", // "bake" (a) today · flip to "round" (b) at go-live.

  /* ±1/2-yr board lens (completion-path requirement). Index 2 == now (BASE_YEAR).
     Maps to lens = [vM2, vM1, v, vP1, vP2] = ev @ 2024/2025/2026/2027/2028 (rl_export.py:66). */
  LENS_DEFAULT: 2,
  LENS_LABELS: ["−2 yr", "−1 yr", "Now", "+1 yr", "+2 yr"],
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
