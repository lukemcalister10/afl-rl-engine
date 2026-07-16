/* Matchday UI v1.3.1 — THE OWNER'S POSITIONAL COUNTING RULE, COLLAPSE-FIRST (items 196(2), 216).
   Display-only: it distributes a player's already-computed board value across the positions listed
   in the owner's AFFL_Player_Locations.csv `Position/s` cell; it computes NO value.

   THE COLLAPSE RULE (item 216, owner-worded, applied FIRST):
     a K-FWD listing ABSORBS a G-FWD listing; a K-DEF listing ABSORBS a G-DEF listing.  The general
     (G) token is slot ELIGIBILITY, never a second position (not a DPP).  So {G-FWD,K-FWD} is a plain
     KEY_FWD; {G-DEF,K-DEF} a plain KEY_DEF; {G-FWD,K-FWD,MID} collapses to {K-FWD,MID}; a four-way
     {G-DEF,K-DEF,K-FWD,G-FWD} collapses to the DPP {K-DEF,K-FWD}.  After the collapse (and the item-2
     CSV corrections) NO ranked player carries 3+ effective positions — asserted by the committed test.

   Owner rule (verbatim-in-substance), applied AFTER the collapse, unchanged:
     - each player counts 1 to his position;
     - a DPP (dual) player counts 0.5 to EACH;
     - EXCEPT DPP midfielders — the non-mid position counts 1 and the midfield component counts 0.

   The per-player weights sum to 1.0, so a club's positional totals sum to its PLAYER value.  MID
   collects value ONLY from MID-only players; any non-mid eligibility gives MID a 0 share.

   OBITUARY — the equal-split 3-4-position generalisation.
     v1.3 carried a generalisation here: when the CSV listed a player at 3-4 positions, his value was
     split equally across his non-mid positions (1/3 or 1/4 each), the only value-conserving reading
     of "0.5 to each" once "each" exceeded two.  The COLLAPSE rule (item 216) removed its reason to
     exist: the 3-4-position listings were all K-implies-G artefacts, and collapsing the G tokens
     leaves every ranked player at <=2 effective positions.  The generalisation is therefore DEAD CODE
     and is DELETED (not disabled).  A post-collapse count of 3+ is now an INVARIANT VIOLATION, thrown
     below and asserted by ui/tests/counting_rule.test.js — it can no longer occur on real data. */
(function (root) {
  "use strict";

  // the 6 canonical position rows (board posCode vocab, Best-23 order).
  var POSITIONS = ["KEY_DEF", "GEN_DEF", "MID", "GEN_FWD", "KEY_FWD", "RUC"];
  var LABELS = {
    KEY_DEF: "Key Def", GEN_DEF: "Gen Def", MID: "Mid",
    GEN_FWD: "Gen Fwd", KEY_FWD: "Key Fwd", RUC: "Ruck",
  };

  /* THE COLLAPSE (item 216), applied first: dedup, then K absorbs its same-flank G.
     Returns the effective posCodes in input order (empty [] only if none listed). */
  function collapse(codes) {
    var seen = {}, uniq = [];
    (codes || []).forEach(function (c) { if (c && !seen[c]) { seen[c] = 1; uniq.push(c); } });
    var set = {};
    uniq.forEach(function (c) { set[c] = 1; });
    if (set.KEY_FWD) delete set.GEN_FWD;   // K-FWD absorbs G-FWD (G is eligibility, not a DPP)
    if (set.KEY_DEF) delete set.GEN_DEF;   // K-DEF absorbs G-DEF
    return uniq.filter(function (c) { return set[c]; });
  }

  /* codes: array of canonical posCodes for one player (from his Position/s cell).
     returns {posCode: weight} summing to 1.0 (empty {} only if he has no listed position). */
  function positionWeights(codes) {
    var eff = collapse(codes);
    if (eff.length === 0) return {};
    if (eff.length === 1) {
      var o1 = {}; o1[eff[0]] = 1.0; return o1;
    }
    if (eff.length > 2) {
      // INVARIANT VIOLATION — see the OBITUARY above.  Post-collapse this cannot happen on real data.
      throw new Error("counting: " + eff.length + " effective positions after collapse (" +
        eff.join(",") + ") — the <=2 collapse invariant (item 216) is broken");
    }
    // exactly 2 — the owner's DPP rule, unchanged.
    var nonMid = eff.filter(function (c) { return c !== "MID"; });
    if (nonMid.length === 0) { return { MID: 1.0 }; }        // degenerate all-MID (not reachable via CSV)
    if (nonMid.length === 1) { var o2 = {}; o2[nonMid[0]] = 1.0; return o2; }  // DPP-mid: non-mid 1, MID 0
    var out = {};                                            // DPP, no mid: 0.5 to each
    nonMid.forEach(function (c) { out[c] = 0.5; });
    return out;
  }

  /* accumulate one player's value onto a per-position bucket, in place. */
  function accumulate(bucket, codes, value) {
    var wts = positionWeights(codes);
    Object.keys(wts).forEach(function (pos) {
      bucket[pos] = (bucket[pos] || 0) + wts[pos] * value;
    });
    return bucket;
  }

  var api = {
    POSITIONS: POSITIONS,
    LABELS: LABELS,
    collapse: collapse,
    positionWeights: positionWeights,
    accumulate: accumulate,
  };

  // browser (window.MD.counting) + node (module.exports) — same source, so the tests exercise the
  // exact function the UI runs.
  if (typeof module !== "undefined" && module.exports) { module.exports = api; }
  root.MD = root.MD || {};
  root.MD.counting = api;
})(typeof window !== "undefined" ? window : globalThis);
