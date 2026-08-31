/* Matchday UI — THE TWO UNIVERSES. One definition, read by the card and the movers tab alike.

   THE OWNER'S RULING, 2026-08-31, verbatim:

     "comparing R14 to FW1 should simply be 'Bontempelli was rated 3213 in R14, and 3717 in FW1, so
      up 504 in that comparison' - that simple. Model changes happened between, but the R14 I want to
      appear is the R14 that is under the 'current model'... It's two universes - it's the ones purely
      under the current model (default) - and then all, including model changes, as the all-in one."

   WHY THIS FILE EXISTS RATHER THAN THE LOGIC LIVING IN BOTH VIEWS. The card and the movers tab must
   agree about which points belong to which universe, or the same player reads two different histories
   on two tabs. Mirrored pairs drift; this estate refuses them everywhere else and refuses one here.

   THE CURRENT-MODEL UNIVERSE is the retrospective series (each round re-priced under the live model)
   plus every stored point that no model change has landed AFTER. Both halves are needed and neither
   is arbitrary:

     * the retro series covers the rounds whose stored boards were produced under a superseded model;
     * a stored point with no model change after it WAS produced under the live model, so re-pricing
       it would be a no-op — and asserting that is cheap: measured 2026-08-31, retro-r24 and the
       stored board immediately before FW1 agree on all 804 players, 0 differ. That is what lets FW1
       join the series with no seam and no second pricing pass.

   IT IS COMPUTED, NEVER LISTED. A hardcoded set of ids would be wrong the first time anything lands.
   `model_changes` is the source, and it now correctly excludes football (round_movers.football_column),
   so a finals week does not evict itself and the rounds after it from their own universe.

   THE ALL-IN UNIVERSE is the record as the app actually served it: stored points only — the rounds
   and the out-of-round columns — with no retro re-pricings interleaved. That is the existing
   behaviour and it is unchanged. */
/* Loadable BOTH ways, like ui/app/movers.js: the browser gets `MD.universe`, a node test gets the
   module export. `window.MD = {}` makes a global in a browser and does not in node, so the module
   is written against a local alias rather than assuming one exists. */
(function (root) {
  "use strict";
  var MD = (typeof window !== "undefined") ? (window.MD = window.MD || {}) : (root.MD = root.MD || {});

  MD.universe = (function () {
  const KEY = "md.universe.mode";
  const CURRENT = "current";      // default: one model throughout
  const ALL = "all";              // the record, model changes included

  /* localStorage can throw outright in some embeddings, not merely return null, so every read and
     write is wrapped and the default survives. A preference that cannot be stored is a preference
     that resets — never a page that fails to render. */
  function mode() {
    try {
      const v = (typeof window !== "undefined" && window.localStorage)
        ? window.localStorage.getItem(KEY) : _memMode;
      return v === ALL ? ALL : CURRENT;
    } catch (e) { return CURRENT; }
  }
  function setMode(m) {
    _memMode = (m === ALL ? ALL : CURRENT);
    try {
      if (typeof window !== "undefined" && window.localStorage) window.localStorage.setItem(KEY, _memMode);
    } catch (e) { /* a preference that cannot be stored still applies for this page load */ }
  }

  let _memMode = CURRENT;   // the in-page fallback when storage is unavailable or throws

  function bundle() {
    return (typeof window !== "undefined" && window.__MATCHDAY_MOVERS__) || null;
  }

  /* The ids of every point a model change landed ON. `model_changes[].between[1]` is the point the
     move arrived at, which is the point that is NOT under the model that preceded it. */
  function modelChangeIds(b) {
    const out = {};
    ((b || {}).model_changes || []).forEach(function (mc) {
      const to = mc && mc.between && mc.between[1];
      if (to) out[String(to)] = true;
    });
    return out;
  }

  /* The index, in the bundle's stored-point order, of the LAST model change. Everything after it was
     produced under the live model. -1 when no model change has ever landed. */
  function lastModelChangeIndex(b) {
    const pts = ((b || {}).points || []).filter(function (p) { return p.kind !== "retro"; });
    const mc = modelChangeIds(b);
    let last = -1;
    for (let i = 0; i < pts.length; i++) if (mc[String(pts[i].id)]) last = i;
    return last;
  }

  /* THE UNIVERSE, as an ordered point list ready for a selector or a history table. */
  function points(b) {
    b = b || bundle();
    const all = ((b || {}).points || []);
    if (mode() === ALL) return all.filter(function (p) { return p.kind !== "retro"; });

    const stored = all.filter(function (p) { return p.kind !== "retro"; });
    const cut = lastModelChangeIndex(b);
    // Everything after the last model change is already the live model's answer.
    const live = cut < 0 ? stored : stored.slice(cut + 1);
    const retro = all.filter(function (p) { return p.kind === "retro"; });
    // Retro first (they cover the older rounds), then the live tail. A retro point and a stored point
    // for the SAME round would double the history, so a retro round that the live tail also carries
    // is dropped — the stored one is the board the app served and wins.
    const liveRounds = {};
    live.forEach(function (p) { if (p.after_round != null) liveRounds[String(p.after_round)] = true; });
    const keptRetro = retro.filter(function (p) {
      return !(p.kind === "retro" && p.after_round != null && liveRounds[String(p.after_round)] &&
               live.some(function (q) { return q.kind === "round" &&
                                        String(q.after_round) === String(p.after_round); }));
    });
    return keptRetro.concat(live);
  }

  /* Is this point in the CURRENT-MODEL universe? Used by the card to filter its own series without
     re-deriving the rule. */
  function inCurrent(b, id) {
    return points(b).some(function (p) { return String(p.id) === String(id); });
  }

  return { CURRENT: CURRENT, ALL: ALL, mode: mode, setMode: setMode,
             points: points, inCurrent: inCurrent,
             modelChangeIds: modelChangeIds, lastModelChangeIndex: lastModelChangeIndex };
  })();

  if (typeof module !== "undefined" && module.exports) module.exports = MD.universe;
})(this);
