/* Matchday UI — v0, THE ENTRY PRICE (owner-commissioned 2026-08-21).

   WHAT HE ASKED FOR, IN HIS WORDS
   -------------------------------
     "One I'd like to definitely add is displaying a player's v0 and their ranking now change
      (absolute and relative) vs that"
   and, correcting the scope the same session:
     "v0 of 3200, live rating of 4000, would mean +800 / 1.25x"

   So: HIS ENTRY PRICE, HIS LIVE RATING, THE GAP, AND THE RATIO. An eyeball of how much he is worth
   against what the model paid for him on the day he came in. Nothing more.

   NO RANKING. THIS IS DELIBERATE AND IT IS THE OWNER'S OWN CORRECTION.
   v0 is a SLOT value, not a player value — docs/ENGINE_PRIMER.md:170: "the surface's slot value —
   identical for every same-(pos, age, pick) player. It is a MODEL BELIEF, not that player's outcome."
   Measured on the shipped sidecar: all eight pick-5 mids of draft age 18 carry v0 2,218 to the dollar.
   A rank over that field would put two thirds of the board into shared blocks and "rank change vs v0"
   for a player inside a block would be an artifact of whatever broke the tie — the register's standing
   posture calls that displaying false information. The value half has none of that problem, so the
   value half is what ships.

   EVERY PLAYER HAS ONE, INCLUDING POOL ENTRANTS (owner, 2026-08-21):
     "Pool entrants do have a v0 though? The moment they are drafted, they have a value. So isn't
      that their v0?"
   Yes. The sidecar carries `origin` per row so this module can say WHICH entry price it is showing:
     · pick-slot    — the frozen year-zero pick surface. Shared by every same-(future position, draft
                      age, pick) player, by construction, and the card says so in words.
     · entry-anchor — a pool entrant's signed division level (#326 entry anchors), in engine-value
                      currency. His entry price, simply not a pick slot.
     · unrecoverable — no entry price could be recovered. Renders an em-dash WITH ITS REASON. Never a
                      fabricated anchor, and never silently omitted.

   THE MIRROR LAW, ENFORCED HERE AND NOT MERELY DOCUMENTED (ui/app/ownership.js:25 — "A mirror that
   does not name the identity it was generated from is not a mirror"). The bundle names the board md5
   and store md5 it was generated from; this module compares both against the board the app is loaded
   on and REFUSES when either disagrees. The failure mode this prevents is the concrete one #232 hit:
   a sidecar generated before an adoption being honoured while the app runs on a later board. v0 is a
   draft-time constant, so it goes stale slowly — which makes it MORE likely to be trusted while wrong,
   not less. Fail closed, and say which identity broke.

   BOTH TIERS AS OF 2026-08-21 — THE RULING CAME IN. What stood here said "WORKING TIER ONLY, PENDING
   AN OWNER WORD": the two-tier law makes the public bundle leak-proof BY CONSTRUCTION, so what rides
   it is a ruling and never a default, and v0 — a model belief about a DRAFT SLOT, shared to the dollar
   by every same-(future position, draft age, pick) player — was arguably public-safe but was his call.
   He made it, verbatim: "v0 goes on the public board, yes." The pending note is retracted here rather
   than left standing beside a shipped feature, because a comment that outlives its truth is the exact
   failure this file's own dRound neighbour was written to record.

   WHAT SHIPPED IS A DATA CHANGE, NOT A BRIDGE. THIS MODULE'S SCOPE IS UNCHANGED: it still answers on
   KEYED (working) rows only, and it still refuses an unkeyed row — a name bridge from a public row to
   a keyed sidecar would have been a second, weaker identity path, and the public bundle carries no key
   to bridge FROM by design. Instead the sidecar is joined to the public rows AT GENERATION TIME, in
   ui/tools/extract_board_view.py, where the keys legitimately exist; the public bundle carries the
   ANSWER per row (`v0` + `v0_origin`) and NO new identifier. ui/app/card.js renderPublic reads those
   two fields and calls ratioText / originWord / originTip below, so the arithmetic and the vocabulary
   have one home across both tiers. The mirror law is enforced at the join too: a sidecar whose stamped
   board/store is not the one the bundle is generated from is refused whole, and every row then carries
   the honest absent state (`v0: null`, origin "unrecoverable") rather than a stale figure.

   PURE VIEW. Computes no price. Reads one generated bundle and does arithmetic on two given figures. */
window.MD = window.MD || {};

MD.v0 = (function () {
  const side = (typeof window !== "undefined" && window.__V0__) || null;

  function present() { return !!(side && side.byKey); }

  /* THE PIN CHECK — the same shape ownership.js uses, against the same two identities. */
  function pin() {
    const st = (side && side.stamp) || {};
    const w = ((MD.seam && MD.seam.working) || {}).stamp || {};
    if (!present()) {
      return { ok: false, why: "no v0 sidecar is loaded (ui/data_aux/v0.js)" };
    }
    if (!st.board || !st.store) {
      return { ok: false, why: "the v0 sidecar carries no board/store pin, so it cannot be authenticated" };
    }
    const wBoard = w.board_md5 || w.board || w.srcmd5;
    const wStore = w.store_md5 || w.store;
    if (wStore && String(st.store).slice(0, 8) !== String(wStore).slice(0, 8)) {
      return { ok: false, why: "the v0 sidecar was generated from store " + String(st.store).slice(0, 8) +
                              " but the app is loaded on store " + String(wStore).slice(0, 8) +
                              " — regenerate with ui/tools/gen_v0_sidecar.py" };
    }
    if (wBoard && String(st.board).slice(0, 8) !== String(wBoard).slice(0, 8)) {
      return { ok: false, why: "the v0 sidecar was generated from board " + String(st.board).slice(0, 8) +
                              " but the app is loaded on board " + String(wBoard).slice(0, 8) +
                              " — regenerate with ui/tools/gen_v0_sidecar.py" };
    }
    return { ok: true, why: null };
  }

  function active() {
    return present() && Object.keys(side.byKey).length > 0 && pin().ok;
  }

  /* Resolve one row.
       -> { has: bool, v0: number|null, origin: string|null, slot: string|null,
            live: number|null, delta: number|null, ratio: number|null,
            refused: bool, why: string|null }
     `refused` means "the sidecar could not be trusted for this row" — a failed pin, an unkeyed
     (public) row, or a pick asset. The caller must render the refusal, never a fallback figure: there
     is no second source for v0 and inventing one is the whole thing this module exists to prevent. */
  function of(p) {
    const none = { has: false, v0: null, origin: null, slot: null, live: null,
                   delta: null, ratio: null, refused: false, why: null };
    if (!p) return none;
    if (MD.isPickAsset && MD.isPickAsset(p)) {
      return Object.assign({}, none, { refused: true, why: "a draft asset is not a player and has no entry price" });
    }
    const pn = pin();
    if (!pn.ok) return Object.assign({}, none, { refused: true, why: pn.why });
    if (!p.key) {
      return Object.assign({}, none, { refused: true,
        why: "this row carries no player key, so it cannot be joined to the v0 sidecar" });
    }
    const rec = side.byKey[p.key];
    if (!rec) {
      return Object.assign({}, none, { refused: true,
        why: "the v0 sidecar carries no row under this player's key" });
    }
    const live = MD.dispVal ? MD.dispVal(p) : p.v;
    if (rec.v0 == null) {
      return { has: false, v0: null, origin: rec.origin || "unrecoverable", slot: rec.slot || null,
               live: live, delta: null, ratio: null, refused: false,
               why: "no entry price could be recovered for this player, so none is shown" };
    }
    const delta = (live == null) ? null : (live - rec.v0);
    const ratio = (live == null || !rec.v0) ? null : (live / rec.v0);
    return { has: true, v0: rec.v0, origin: rec.origin || null, slot: rec.slot || null,
             live: live, delta: delta, ratio: ratio, refused: false, why: null };
  }

  /* "1.25x" / "0.78x" — two decimals, the owner's own notation from his worked example. */
  function ratioText(r) {
    if (r == null || !isFinite(r)) return "—";
    return (Math.round(r * 100) / 100).toFixed(2) + "x";
  }

  const ORIGIN_WORD = {
    "pick-slot": "draft-slot price",
    "entry-anchor": "pool entry level",
    "unrecoverable": "no entry price recoverable",
  };
  const ORIGIN_TIP = {
    "pick-slot":
      "His entry price off the frozen year-zero pick surface — what the model paid for that draft " +
      "slot. Every player entering at the same future position, draft age and pick number carries " +
      "this same figure: it is a belief about the slot, not a prediction about him.",
    "entry-anchor":
      "His entry price as a POOL entrant — his intake division's signed level (#326 entry anchors), " +
      "in board currency. Pool entrants are priced off their division rather than a pick slot, so " +
      "this is the same object as a drafted player's v0 arrived at the honest way for him.",
    "unrecoverable":
      "No entry price could be recovered for this player, so none is shown. Nothing is invented in " +
      "its place.",
  };
  function originWord(o) { return ORIGIN_WORD[o] || (o || "—"); }
  function originTip(o) { return ORIGIN_TIP[o] || "Entry price provenance is not recorded for this row."; }

  function status() {
    const st = (side && side.stamp) || {};
    const pn = pin();
    return {
      present: present(),
      active: active(),
      pinOk: pn.ok,
      pinWhy: pn.why,
      board: st.board || null,
      store: st.store || null,
      generator: st.generator || null,
      source: st.source || null,
      nRows: st.nRows || 0,
      nPickSlot: st.nPickSlot || 0,
      nEntryAnchor: st.nEntryAnchor || 0,
      nAbsent: st.nAbsent || 0,
      /* The public tier is a ruling, not a default — and the ruling is IN (owner, 2026-08-21: "v0
         goes on the public board, yes"). Reported as the shipped state so a status reader is never
         told a decision is outstanding when it has been made and acted on. The public tier does not
         read THIS module's sidecar: it renders from the per-row `v0` / `v0_origin` fields joined into
         ui/data/board_view_public.js by ui/tools/extract_board_view.py (see the header note). */
      publicTier: "shipped on the owner's word of 2026-08-21 — the public card renders v0 from the "
                + "public bundle's own per-row fields, joined at generation time (no key is added)",
    };
  }

  return {
    of: of,
    pin: pin,
    active: active,
    status: status,
    ratioText: ratioText,
    originWord: originWord,
    originTip: originTip,
  };
})();
