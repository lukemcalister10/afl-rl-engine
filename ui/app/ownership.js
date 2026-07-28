/* Matchday UI — AFFL OWNERSHIP, THE LIVE LANE (#232).

   WHY THIS EXISTS.  Ownership lived inside the store as `affl_team`, so reflecting a trade meant editing
   the authored store and running the whole pipeline.  Trades happen daily in this league, so they simply
   did not get reflected.  Ownership affects no player's value — `affl_team` appears nowhere in the
   valuation path — so it has no business costing an engine run.  `ui/data/ownership.js` is written by
   `ui/tools/ingest_inputs.py` straight from the owner's sheet; the browser reads it here.

   THE RULE: THE SIDECAR OVERRIDES, THE STORE FALLS BACK.  A player the sheet names takes the sidecar's
   club; a player it does not name keeps the board's `affl_team`.  So the sidecar may be partial and fill
   in over time, and nothing has to be deleted from the store — retiring that field is an owner act.

   POSITIONS ARE NOT HERE.  They feed valuation, so they ride the batched lane: engine run, board move,
   one history column.  If positions ever appear in this file, the live lane has become an engine trigger
   and the whole design is undone.

   THE PUBLIC TIER IS WHY THIS IS NOT A ONE-LINER.  The working bundle keys every player; the public
   bundle carries the same 804 players with NO key at all, joining only by display name.  So a public row
   has to be bridged name -> key before we can tell whether an override applies to it.  Today all 804
   names are distinct on store e3aaba77 — but that is DATA, not a guarantee.  If a name is ambiguous or
   matches nothing, we cannot establish which player the row is, and therefore cannot know whether the
   sheet moved him.  In that case this module REFUSES: it returns no club and reports the row, rather
   than resolving to one candidate or quietly showing the store value as though it were current.
   Silently showing the store value is precisely the failure this job exists to prevent — the same player
   in his new club on one tab and his old club on another, with nothing saying so. */
window.MD = window.MD || {};

MD.ownership = (function () {
  const side = window.__OWNERSHIP__ || null;

  function halted() { return !!(side && side.halt); }
  function present() { return !!(side && side.byKey); }
  /* ACTIVE means "this sidecar can override something". An absent or halted sidecar is not active, and
     with nothing to override there is no divergence to refuse over — every row falls back to the store,
     which is exactly the pre-#232 behaviour. */
  function active() {
    return present() && !halted() && Object.keys(side.byKey).length > 0;
  }

  /* Same normalisation as the ingest's nkey(): collapse whitespace, casefold. It resolves the five
     case-only surname variants without guessing, and keeps the two Max Kings distinct. */
  function norm(s) {
    return String(s == null ? "" : s).trim().replace(/\s+/g, " ").toLowerCase();
  }

  let _bridge = null, _ambiguous = null;

  /* name -> key, built from the WORKING bundle because it is the only population carrying both. Any
     name held by more than one player is DELETED from the index and recorded — an ambiguous name must
     resolve to nothing, never to whichever player was seen first (hazard 13: identity by key, never by
     substring or by first match). */
  function buildBridge() {
    const m = {}, dup = {};
    const w = MD.seam && MD.seam.working;
    ((w && w.players) || []).forEach(function (p) {
      if (!p || !p.key || p.name == null) return;
      const n = norm(p.name);
      if (Object.prototype.hasOwnProperty.call(m, n)) dup[n] = 1;
      else m[n] = p.key;
    });
    Object.keys(dup).forEach(function (n) { delete m[n]; });
    _bridge = m; _ambiguous = dup;
  }

  function bridge() { if (_bridge === null) buildBridge(); return _bridge; }
  function ambiguous() { if (_bridge === null) buildBridge(); return _ambiguous; }

  /* Resolve one row's AFFL club.
       -> { club: <string|null>, refused: <bool>, why: <string|undefined>, overridden: <bool> }
     `club: null, refused: false` simply means "no club" (a pick asset, or a row the board never gave
     one).  `refused: true` means "identity could not be established" — the caller must not fall back. */
  function resolve(p) {
    if (!p) return { club: null, refused: false, overridden: false };
    if (MD.isPickAsset && MD.isPickAsset(p)) {
      return { club: null, refused: false, overridden: false };   // an asset is not a player
    }
    const store = (p.affl_team == null) ? null : p.affl_team;

    if (!active()) return { club: store, refused: false, overridden: false };

    // keyed row (working board, movers): join directly, no bridge, no ambiguity.
    if (p.key) {
      const o = side.byKey[p.key];
      return (o == null)
        ? { club: store, refused: false, overridden: false }
        : { club: o, refused: false, overridden: o !== store };
    }

    // unkeyed row (public bundle): bridge by name, FAIL CLOSED.
    if (p.name != null) {
      const n = norm(p.name);
      const key = bridge()[n];
      if (!key) {
        return {
          club: null, refused: true, overridden: false,
          why: ambiguous()[n]
            ? "display name is shared by more than one player, so the row cannot be identified"
            : "display name matches no player in the working board, so the row cannot be identified",
        };
      }
      const o = side.byKey[key];
      return (o == null)
        ? { club: store, refused: false, overridden: false }
        : { club: o, refused: false, overridden: o !== store };
    }

    // No key and no name: nothing to identify it by. Refuse rather than trust the store.
    return { club: null, refused: true, overridden: false,
             why: "row carries neither a key nor a name, so the player cannot be identified" };
  }

  /* The club to USE for membership: filters, aggregation, dropdowns. Null on refusal, so a row whose
     identity is unknown drops out of every club total rather than being counted into the wrong one. */
  function clubOf(p) {
    const r = resolve(p);
    return r.refused ? null : r.club;
  }

  /* The string to DISPLAY. A refusal is visible, never a silent "—". */
  const REFUSED_LABEL = "⚠ unverified";
  function labelOf(p) {
    const r = resolve(p);
    if (r.refused) return REFUSED_LABEL;
    return (MD.fmt && MD.fmt.club) ? MD.fmt.club(r.club) : (r.club || "—");
  }
  function titleOf(p) {
    const r = resolve(p);
    return r.refused
      ? ("AFFL ownership not shown: " + r.why + ". The sidecar is live, so the board's stored club "
         + "cannot be assumed current for this row.")
      : "AFFL club";
  }

  /* Every public row the bridge cannot identify. Computed over the whole public bundle so the count is
     the real one rather than whatever happened to render. Empty when the sidecar is not active. */
  function publicRefusals() {
    if (!active()) return [];
    const pub = MD.seam && MD.seam.public;
    const b = bridge();
    return ((pub && pub.players) || [])
      .filter(function (p) { return p && p.name != null && !b[norm(p.name)]; })
      .map(function (p) { return p.name; });
  }

  function status() {
    const st = (side && side.stamp) || {};
    const refusals = publicRefusals();
    return {
      present: present(),
      active: active(),
      halted: halted(),
      haltReason: halted() ? (side.halt.reason || "ingest refused") : null,
      generated: st.generated || null,
      source: st.source || null,
      nAuthored: st.nAuthored || 0,
      nOverriding: (side && side.overriding && side.overriding.length) || 0,
      publicRefusals: refusals,
      nPublicRefused: refusals.length,
    };
  }

  return {
    resolve: resolve,
    clubOf: clubOf,
    labelOf: labelOf,
    titleOf: titleOf,
    publicRefusals: publicRefusals,
    status: status,
    REFUSED_LABEL: REFUSED_LABEL,
    _norm: norm,
  };
})();
