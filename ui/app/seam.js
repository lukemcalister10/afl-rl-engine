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
    // The BOARD OF RECORD, and NOT a hand-typed constant (see config.js — the pin that used to live
    // there killed the app on 2026-07-28). extract_board_view.py copies data/expected_boot.json 'board'
    // into the stamp verbatim, so this is the manifest's own answer travelling with the bundle. `head`
    // is computed from the board artifact's bytes; `want` is declared by the manifest — a bundle whose
    // contents don't match what the manifest says it is still fails closed.
    const want = String(working.stamp.board || "").slice(0, 8);
    // A bundle carrying NO board of record cannot be authenticated, so it does not get the benefit of
    // the doubt. Fail closed — an unauthenticated board must look broken, because it is. (Without this
    // an unstamped bundle would compare "" !== "" and sail through as ok.)
    if (!/^[0-9a-f]{8}$/.test(want)) {
      return { ok: false, why: "board of record missing from bundle stamp", got: head, want: want };
    }
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

  /* THE ONE CHOKE POINT FOR THE PICKS OVERLAY (v827, 2026-08-21). `clubHalt()` used to mean only "the
     ingest wrote a halted bundle". It now ALSO means "the bundle present is not this tree's" —
     `MD.clubTotals.pin()`, the #232 mirror law applied to the picks bundle (see the note at that
     function). Both are the same fact to every reader here: the picks on file cannot be shown.

     WHY THE REFUSAL IS CENTRALISED RATHER THAN LEFT IN THE CLUBS PAGE. The stale bundle found on
     2026-08-21 was read by THREE surfaces — the clubs table, the pocket profile, and the board's
     picks-included overlay (club headers, the club banner, the held-picks panel). Guarding only the
     reader that computes totals would have left the board still printing R22 pick values under a
     "picks included" button that looked perfectly healthy. So the seam refuses, once, and every
     consumer inherits it: the overlay button disables with the reason on hover, exactly as it does on
     an ingest halt, and `picksFor` yields nothing for anyone who asks anyway.

     `MD.clubTotals` loads AFTER this module (index.html), which is why the pin is consulted lazily at
     call time and why its absence is not treated as a refusal — a context that loads the seam without
     the reader has no picks surface to protect. */
  function clubPin() {
    return (MD.clubTotals && MD.clubTotals.pin) ? MD.clubTotals.pin() : { ok: true, why: null };
  }
  function clubHalt() {
    if (clubBundle && clubBundle.halt) return clubBundle.halt;
    const pn = clubPin();
    return pn.ok ? null : { reason: pn.why, pinRefused: true };
  }
  function picksFor(afflTeamLong) {
    if (!clubBundle || !clubBundle.picksByTeam) return [];
    // FAIL CLOSED on a bundle that is not this tree's. A stale pick price is a wrong number wearing
    // the look of a right one, and there is no fallback the browser could compute in its place.
    if (!clubPin().ok) return [];
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

/* THE SAME RULING, REACHABLE BY KEY (owner word 2026-09-01). `MD.dispVal` needs a board ROW, which is
   fine for every surface that holds one. The movers page does not: it reads historical values out of
   movers.js `byPoint`, keyed by player, with no board row in hand — which is why it showed Brodie at his
   pre-override 117 at every point, stored and retro alike, while board, card, draft day and v0 all showed
   58. Owner ruling: "Display 58 for Brodie."

   ONE SOURCE STILL. This reads the factor off the SAME `ov` block `MD.dispVal` substitutes, so the
   override lives in exactly one place (data/owner_overrides.json -> owner_overrides.apply_to_board ->
   the board row's `ov`) and a future row, or a changed factor, reaches both accessors with no edit here.
   Returns 1 for every non-overridden player and whenever the board is not loaded, so callers can
   multiply unconditionally. */
MD.ovFactor = function (key) {
  var idx = null;
  try { idx = MD.seam && MD.seam.indexed && MD.seam.indexed(); } catch (e) { return 1; }
  var row = idx && idx.byKey ? idx.byKey[key] : null;
  var f = row && row.ov ? row.ov.factor : null;
  return (typeof f === "number" && f > 0) ? f : 1;
};

/* PYTHON'S ROUNDING, NOT JAVASCRIPT'S, and the difference is visible on the one player this exists for.
   owner_overrides.py computes `dispv = int(round(v * factor))`, and Python 3 rounds a .5 tie to EVEN:
   round(58.5) = 58. `Math.round(58.5)` is 59. Brodie is 117 x 0.5 = 58.5 exactly, so using Math.round
   here would print 59 on the movers page against 58 on his card — the very inconsistency this ruling
   closes, reintroduced one decimal further down. */
MD.ovRound = function (x) {
  var f = Math.floor(x), d = x - f;
  if (d > 0.5) return f + 1;
  if (d < 0.5) return f;
  return (f % 2 === 0) ? f : f + 1;
};

/* THE LENS GATE (owner word 2026-08-21; ruling register v46 — see MD.config.LENS_DISABLED).
   A disabled lens must be UNREACHABLE, not merely unclicked: the board's filter state is snapshotted
   and restored by the universal Back, and MD.state is a plain object any future caller can set. So the
   test lives here, beside the state it guards, and the board clamps through it at render — a restored
   snapshot, a stale value or a future caller cannot put a ruled-wrong lens on screen. */
MD.lensDisabled = function (i) {
  return ((MD.config && MD.config.LENS_DISABLED) || []).indexOf(i) !== -1;
};
MD.lensClamp = function (i) {
  return MD.lensDisabled(i) ? MD.config.LENS_DEFAULT : i;
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
