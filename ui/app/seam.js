/* Matchday UI — the DATA SEAM. Pure view: computes NO price (SSI / DESIGN_DIRECTION §7 doctrine).
   Loads the stamped, tiered board bundles and FAIL-CLOSES if the working board's md5 head disagrees
   with the expected board id — the UI analogue of Guard 5 (an unauthenticated/unexpected board must
   look broken, because it is). */
window.MD = window.MD || {};

MD.seam = (function () {
  const working = window.__MATCHDAY_WORKING__ || null;
  const pub = window.__MATCHDAY_PUBLIC__ || null;

  function ringFence() {
    if (!working || !working.stamp) return { ok: false, why: "working board bundle missing" };
    const head = String(working.stamp.srcmd5 || "").slice(0, 8);
    const want = MD.config.EXPECTED_BOARD;
    if (head !== want) {
      return { ok: false, why: "board id mismatch", got: head, want: want };
    }
    return { ok: true };
  }

  /* index players by key + precompute board rank (by current value, descending). */
  function indexed() {
    const players = (working.players || []).slice();
    const byKey = {};
    players.forEach(function (p) { byKey[p.key] = p; });
    return { players: players, byKey: byKey };
  }

  return {
    working: working,
    public: pub,
    ringFence: ringFence,
    indexed: indexed,
  };
})();

/* The DISPLAYED current value of a player (v2.9 bake, owner-ruled 2026-07-13): an owner override
   substitutes the overridden display figure (ov.dispv) WHEREVER the board shows his value, and ordering
   follows the display. MECHANICS stay on the engine value `v` (Δ-vs-bake, lens, attribution, all guards).
   Non-overridden rows and the public tier (no `ov` by design) fall back to `v`. */
MD.dispVal = function (p) {
  return (p && p.ov && p.ov.dispv != null) ? p.ov.dispv : (p ? p.v : null);
};

/* shared UI state */
MD.state = {
  view: "board",                       // board | card | trade | review
  tier: "working",                     // working | public
  lens: MD.config.LENS_DEFAULT,        // 0..4  (index 2 == now)
  deltaBase: MD.config.DELTA_BASE_DEFAULT, // bake | round
  slugs: false,                        // debug affordance (working only)
  cardKey: null,                       // selected player for the card view
  trade: { give: [], get: [] },        // trade-desk baskets (keys / pick refs)
};
