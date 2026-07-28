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
    // Authenticate the INSTALLED WORKING BOARD only — `board_md5` (not the store, not the balanced
    // reference). `srcmd5` is the temporary identical alias read for un-regenerated bundles.
    const head = String(working.stamp.board_md5 || working.stamp.srcmd5 || "").slice(0, 8);
    const want = MD.config.EXPECTED_BOARD;
    if (head !== want) {
      return { ok: false, why: "board id mismatch", got: head, want: want };
    }
    return { ok: true };
  }

  /* index players by key + precompute board rank (by current value, descending). */
  function indexed() {
    const players = (working.players || []).slice();
    const byKey = {}, byName = {}, nameDupes = {};
    players.forEach(function (p) {
      byKey[p.key] = p;
      // #139 item 16: the public bundle is a sanitised view of the SAME 804 players but carries no
      // `key`, so a public row joins to its profile by display name. Ambiguous names are recorded and
      // deliberately NOT joined — opening the wrong player's card is worse than opening none. Measured
      // on store e3aaba77: zero display names are shared by two or more of the 804 active players.
      if (p.name == null) return;
      if (Object.prototype.hasOwnProperty.call(byName, p.name)) { nameDupes[p.name] = 1; }
      else { byName[p.name] = p.key; }
    });
    Object.keys(nameDupes).forEach(function (n) { delete byName[n]; });
    return { players: players, byKey: byKey, byName: byName, nameDupes: Object.keys(nameDupes) };
  }

  /* club-valuation overlay (item 178(2)/(3)): the picks + per-club summary emitted by the deterministic
     VALIDATE-OR-HALT ingest (ui/tools/ingest_inputs.py).  Null if the bundle is absent; carries `.halt`
     (a {reason, verdicts}) when the ingest refused — the overlay features fail-closed to that message
     while the board itself still renders. */
  /* #139 item 21 (owner ruling 2026-07-28): this bundle is now read for its PICKS ONLY. Its baked
     per-club totals are no longer a source of truth anywhere in the UI — they are recomputed live from
     the board by MD.clubTotals, because a baked sum goes stale on every board move and twice did.
     Deliberately exposed as `clubBundle`, not `club`: the old name read like "the club data", and any
     code reaching for it now has to say that it wants the raw ingest bundle. */
  const clubBundle = window.__CLUB_VALUATION__ || null;
  function clubHalt() { return clubBundle && clubBundle.halt ? clubBundle.halt : null; }
  function picksFor(afflTeamLong) {
    if (!clubBundle || !clubBundle.picksByTeam) return [];
    // canonical join key — the picks ledger and the board must agree on one spelling per club.
    const t = MD.canonClub(afflTeamLong);
    return clubBundle.picksByTeam[t] || clubBundle.picksByTeam[afflTeamLong] || [];
  }

  return {
    working: working,
    public: pub,
    clubBundle: clubBundle,
    clubHalt: clubHalt,
    picksFor: picksFor,
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
  view: "board",                       // board | clubs | card | trade | movers  (#139 item 2: review retired)
  tier: "working",                     // working | public
  nav: [],                             // #139 item 15: universal-Back location stack (see main.js)
  lens: MD.config.LENS_DEFAULT,        // 0..4  (index 2 == now)
  deltaBase: MD.config.DELTA_BASE_DEFAULT, // bake | round
  slugs: false,                        // debug affordance (working only)
  cardKey: null,                       // selected player for the card view
  trade: { give: [], get: [] },        // trade-desk baskets (keys / pick refs)
};
