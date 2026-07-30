/* Matchday UI — AFFL OWNERSHIP, THE LIVE LANE (#232, REDESIGNED BY #283).

   WHY THIS EXISTS.  Ownership affects no player's value — `affl_team` appears nowhere in the valuation
   path — so reflecting a trade has no business costing an engine run.  The owner edits
   `docs/inputs/AFFL_Player_Locations.csv`, runs `ui/tools/ingest_inputs.py`, and reloads.

   THE RULE (owner ruling 2026-07-30, #283): THE STORE IS THE SINGLE SOURCE; THIS SIDECAR IS A
   GENERATED MIRROR.  The ingest couriers the owner's CSV into the store's `affl_team` and then rebuilds
   `ui/data/ownership.js` FROM THE STORE in the same command.  The sidecar is never independently
   authoritative — it cannot "override" anything, because it is downstream of the same field the clubs
   parity oracle reads.  That is the whole point: reader and oracle are provably the same source and
   cannot disagree.

   WHAT REPLACED THE OLD RULE, AND WHY.  #232 shipped the inverse — "the sidecar OVERRIDES; the store's
   affl_team remains the fallback" — on the premise that ownership was presentation data read nowhere in
   a checked computation.  That premise died when club totals became a checked surface: the UI resolved
   clubs through this sidecar while the parity oracle read the store, and the two agreed only by the
   coincidence that no override existed.  The moment the owner's 2026-07-29 CSV was ingested, 18 of 804
   players moved and the parity suite went red.  See ui/screenshots/issue_274/02_item2_FINDING_ownership.md.

   HAND-EDITING IS BARRED, AND ENFORCED HERE.  A hand-edited or stale sidecar is refused by the pin check
   in `active()` below, not merely discouraged by a comment.  #232 gated this file on presence, halt and
   non-emptiness ONLY — never on its board/store pin — which is exactly why a pre-adoption sidecar
   (expectedBoard 8a38cca4, store e3aaba77) was being HONOURED rather than ignored while the app ran on a
   later board.  A mirror that does not name the identity it was generated from is not a mirror.

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

  /* THE PIN CHECK (#283, acceptance 4 — the hand-edit bar made real).
     A generated mirror must name the identity it was generated FROM, and that identity must be the one
     the app is loaded at. This compares the sidecar's stamped board + store against the working bundle's
     — the check #232 never had. A stale sidecar (generated before the current adoption), a hand-edited
     one, or one lifted from another tree fails here and the app falls back to the board's own
     store-derived `affl_team` instead of honouring it.

     Fail CLOSED but not silently: `status()` reports pinOk / pinWhy so the surface can say so. */
  function pin() {
    const st = (side && side.stamp) || {};
    const w = ((MD.seam && MD.seam.working) || {}).stamp || {};
    if (!st.store || !st.board) {
      return { ok: false, why: "the sidecar carries no board/store pin, so it cannot be authenticated" };
    }
    if (w.store && st.store !== w.store) {
      return { ok: false, why: "sidecar was generated from store " + String(st.store).slice(0, 8)
                              + " but the app is loaded on store " + String(w.store).slice(0, 8) };
    }
    if (w.board && st.board !== w.board) {
      return { ok: false, why: "sidecar was generated from board " + String(st.board).slice(0, 8)
                              + " but the app is loaded on board " + String(w.board).slice(0, 8) };
    }
    return { ok: true, why: null };
  }

  /* ACTIVE means "this mirror is authenticated and usable". Absent, halted, empty, or failing the pin
     check -> not active, and every row reads the board's own store-derived `affl_team`. Since #283 the
     two are the same field, so an inactive mirror is a degraded display, never a wrong club. */
  function active() {
    return present() && !halted() && Object.keys(side.byKey).length > 0 && pin().ok;
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
    const pn = pin();
    return {
      present: present(),
      active: active(),
      halted: halted(),
      haltReason: halted() ? (side.halt.reason || "ingest refused") : null,
      /* #283: the mirror carries no wall clock — it is a pure function of the store, so its
         provenance is the store identity it was generated from, and that is what makes
         "regenerate and byte-compare" a real check rather than one that can never be an equality. */
      generatedFromStore: st.generatedFromStore || null,
      source: st.source || null,
      nAuthored: st.nAuthored || 0,
      /* #283: the mirror is downstream of the store, so a divergence from it is structurally
         impossible. This stays 0 by construction and is reported as the invariant it now is. */
      nOverriding: (side && side.overriding && side.overriding.length) || 0,
      pinOk: pn.ok,
      pinWhy: pn.why,
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
    pin: pin,
    REFUSED_LABEL: REFUSED_LABEL,
    _norm: norm,
  };
})();
