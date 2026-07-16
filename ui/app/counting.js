/* Matchday UI v1.3 — THE OWNER'S POSITIONAL COUNTING RULE (item 196(2)), as a PURE function.
   Display-only: it distributes a player's already-computed board value across the positions listed
   in the owner's AFFL_Player_Locations.csv `Position/s` cell; it computes NO value.

   Owner rule (verbatim-in-substance):
     - each player counts 1 to his position;
     - a DPP (dual) player counts 0.5 to EACH;
     - EXCEPT DPP midfielders — the non-mid position counts 1 and the midfield component counts 0.

   ONE rule reproduces all three verbatim cases and is forced by value conservation (the per-player
   weights MUST sum to 1.0 so the club's positional totals sum to its PLAYER value):

     MID collects value ONLY from MID-only players.  A player with any non-mid eligibility splits his
     full value EQUALLY across his non-mid positions; his MID share is 0.

   Generalisation to the 33 ranked players the CSV lists at 3-4 positions (owner worded it for <=2):
   equal split is the only value-conserving reading of "to each" (0.5 x 3 = 1.5 > 1 is impossible),
   and the mid-exception's rationale — credit the specialist position, not the catch-all MID — is
   unchanged.  This generalisation is flagged in the RETURN and in the panel footnote.  No case here
   contradicts the three the owner gave. */
(function (root) {
  "use strict";

  // the 6 canonical position rows (board posCode vocab, Best-23 order).
  var POSITIONS = ["KEY_DEF", "GEN_DEF", "MID", "GEN_FWD", "KEY_FWD", "RUC"];
  var LABELS = {
    KEY_DEF: "Key Def", GEN_DEF: "Gen Def", MID: "Mid",
    GEN_FWD: "Gen Fwd", KEY_FWD: "Key Fwd", RUC: "Ruck",
  };

  /* codes: array of canonical posCodes for one player (from his Position/s cell).
     returns {posCode: weight} summing to 1.0 (empty {} only if he has no listed position). */
  function positionWeights(codes) {
    var seen = {}, uniq = [];
    (codes || []).forEach(function (c) { if (c && !seen[c]) { seen[c] = 1; uniq.push(c); } });
    if (uniq.length === 0) return {};
    if (uniq.length === 1) {
      var o1 = {}; o1[uniq[0]] = 1.0; return o1;
    }
    var nonMid = uniq.filter(function (c) { return c !== "MID"; });
    if (nonMid.length === 0) { return { MID: 1.0 }; }   // degenerate all-MID multi-token
    var w = 1.0 / nonMid.length, out = {};
    nonMid.forEach(function (c) { out[c] = w; });        // MID share left implicitly 0
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
    positionWeights: positionWeights,
    accumulate: accumulate,
  };

  // browser (window.MD.counting) + node (module.exports) — same source, so the tests exercise the
  // exact function the UI runs.
  if (typeof module !== "undefined" && module.exports) { module.exports = api; }
  root.MD = root.MD || {};
  root.MD.counting = api;
})(typeof window !== "undefined" ? window : globalThis);
