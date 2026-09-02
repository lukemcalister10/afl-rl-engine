/* Matchday UI — THE PLAYER'S WEEKLY HISTORY (#139 item 3).

   Reads the movers bundle (ui/data/movers.js), which the page already loads. That bundle carries, for
   all 804 players at all eight points, the value / rank / positional-rank trace (`values[key].byPoint`),
   the ordered points with their labels and kinds (`points`), the out-of-round model changes
   (`model_changes`), and each committed round's per-player score (`reports[r].players[].score`).

   ============================ THE THING THAT MAKES THIS CARD HONEST ============================

   THE TWO COLUMNS HAVE DIFFERENT POPULATIONS, and treating them alike produces a card that states
   football facts the data does not support.

   1 · THE VALUATION TRACE IS COMPLETE. All 804 players carry a value, a rank and a positional rank at
       every one of the eight points — verified, zero gaps. A player who did not play still moves,
       because everyone else did. So the trace is NEVER gated on participation and carries no caveat.

   2 · SCORE COVERAGE IS NOT UNIFORM, and 804 is the wrong denominator to judge it by. 804 is the whole
       tracked league; a round only selects about 414 (18 sides). Measured on this bundle:

         point                  scored   AFL clubs represented   smallest side
         14                     none     —                       —                (no score map at all)
         15                     318      16 of 18                1                PARTIAL FEED
         16                     319      17 of 18                1                PARTIAL FEED
         17                     410      18 of 18                21               complete
         18                     406      18 of 18                21               complete
         19                     405      18 of 18                21               complete
         20                     410      18 of 18                20               complete
         post-r19-redesign-1    none     —                       —                not a round

       In R15 and R16 the early catch-up feeds were partial: whole clubs are missing and two more are
       represented by a single player. A player absent from those maps DID NOT NECESSARILY MISS THE
       GAME — the feed did not carry him. In R17-R20 every club is present at full-side strength, so
       absence there really does mean he did not play.

       Therefore: show the score where it exists; leave it BLANK where it does not; and print "DNP" ONLY
       for a round proven complete. Never print DNP for a round whose data was never collected.

       The bundle's own per-player `dnp` flag is deliberately NOT used. It is set true for every player
       without a score, which in R15 marks 486 players as "did not play" in a round that recorded 318 of
       ~414 — exactly the false football claim this module exists to prevent.

   3 · `post-r19-redesign-1` IS NOT A ROUND. It is the ITEM 411 D1/D2 restructure. It shows as value and
       rank movement labelled a model change, has no score cell, and can never carry a played indicator.

   COMPLETENESS IS DERIVED, NOT HARDCODED. The round list above is what today's bundle measures, not a
   constant in the code: coverage() recomputes it from the bundle and the board every load. A future
   round with a full feed lights up on its own; a future partial feed stays blank without a code change.
   The threshold sits in the empty gap between a broken feed (smallest side 1-2) and a real one
   (smallest side 20+), and it fails SAFE — an unrecognised shape yields "not recorded", never a DNP. */
window.MD = window.MD || {};

MD.history = (function () {
  /* A round counts as completely fed when EVERY AFL club on the board appears in its score map, and
     none of them appears at less than a full side's worth of tracked players. The observed complete
     rounds sit at 20-25 per club; the observed partial ones drop to 1-2 and lose whole clubs. */
  const MIN_SIDE = 15;

  function bundle() { return (typeof window !== "undefined" && window.__MATCHDAY_MOVERS__) || null; }

  let _cov = null;

  /* per-round: the score map (key -> score) and whether the round's feed is complete. */
  function coverage() {
    if (_cov) return _cov;
    const b = bundle();
    const out = { rounds: {}, clubsOnBoard: 0, minSide: MIN_SIDE };
    if (!b) { _cov = out; return out; }

    const byKey = ((MD.seam && MD.seam.indexed) ? MD.seam.indexed().byKey : {}) || {};
    const boardClubs = {};
    Object.keys(byKey).forEach(function (k) {
      const c = byKey[k] && byKey[k].afl_club;
      if (c) boardClubs[c] = 1;
    });
    out.clubsOnBoard = Object.keys(boardClubs).length;

    (b.rounds || []).forEach(function (rd) {
      const rep = (b.reports || {})[String(rd)];
      if (!rep) return;
      const scores = {}, perClub = {};
      let n = 0;
      (rep.players || []).forEach(function (p) {
        if (p.score == null) return;
        scores[p.key] = p.score; n++;
        const c = byKey[p.key] && byKey[p.key].afl_club;
        if (c) perClub[c] = (perClub[c] || 0) + 1;
      });
      const clubs = Object.keys(perClub);
      let smallest = null;
      clubs.forEach(function (c) { if (smallest === null || perClub[c] < smallest) smallest = perClub[c]; });
      const complete = out.clubsOnBoard > 0 &&
                       clubs.length === out.clubsOnBoard &&
                       smallest !== null && smallest >= MIN_SIDE;
      out.rounds[String(rd)] = {
        scores: scores, scored: n, clubs: clubs.length, smallestSide: smallest, complete: complete,
      };
    });
    _cov = out;
    return out;
  }

  /* the ordered points, each already resolved for rendering. */
  function points() {
    const b = bundle();
    if (!b || !(b.points || []).length) return [];
    const changes = {};
    (b.model_changes || []).forEach(function (mc) {
      const to = mc.between && mc.between[1];
      if (to) changes[String(to)] = mc;
    });
    // The card is the RECORD: what this player's value did on the boards the app actually served.
    // Retro points are the current model's re-pricing of old rounds — a second world, offered in the
    // movers selector where a comparison names its own two endpoints. Interleaving them here would
    // double every card's history and read as movement that never happened.
    /* THE UNIVERSE DECIDES, NOT THIS FUNCTION (owner ruling 2026-08-31). The card used to be the
       stored record only, and the comment below still explains why retro points were excluded from
       it: interleaving both would double every history. That reasoning is intact — what changed is
       that the two are now offered as ALTERNATIVES rather than one being dropped. MD.universe owns
       the choice so the card and the movers tab cannot disagree about which world is on screen. */
    /* A RETRO POINT'S DISPLAY NAME. A numbered round reads "Round 14" rather than the emitter's
       "R14 · current model", because the card already says re-priced everywhere it matters and the
       axis has no room. But A FINALS WEEK IS NAMED, NOT NUMBERED — "Round 25" is a round that
       appears on no fixture, and the card printed exactly that until 2026-09-02. The emitter has
       already named the week, so the name is TAKEN FROM THE POINT rather than kept in a second
       finals table here that could drift out of step with it. */
    function retroLabel(pt) {
      var name = String(pt.label || "").split(" · ")[0];
      if (!name || /^R\d+$/.test(name)) return "Round " + pt.after_round;
      return name;
    }
    return MD.universe.points(b).map(function (pt) {
      /* A RETRO POINT IS A ROUND. It is that round's football re-priced under the current model, so
         it has a score map, a DNP truth and a coverage record — all keyed on the ROUND, not on the
         retro point's own id. Treating it as "not a round" would print "no football was played at
         this point" against a round of football, which is the opposite of true. `roundKey` is what
         the score and coverage lookups join on; it is the point's own id for a stored round and the
         round number for a retro one. */
      const isRetro = pt.kind === "retro";
      const isRound = pt.kind === "round" || isRetro;
      return {
        id: String(pt.id),
        roundKey: isRetro ? String(pt.after_round) : String(pt.id),
        label: isRetro ? retroLabel(pt) : pt.label,
        isRound: isRound,
        isRetro: isRetro,
        modelChange: changes[String(pt.id)] || null,
      };
    });
  }

  /* SCORE CELL STATE for one player at one point. This is the whole honesty contract in one function.
       "score"        — a real score, shown
       "dnp"          — proven complete round, no score: he did not play
       "unrecorded"   — the feed did not carry him (or carried no one); NOT a football claim
       "not-a-round"  — the restructure point; no score exists or ever will  */
  function scoreCell(key, pt) {
    if (!pt.isRound) {
      return { state: "not-a-round", score: null,
               why: "Not a round — " + (pt.label || "a model change") + ". No football was played at this point." };
    }
    const cov = coverage().rounds[pt.roundKey || pt.id];
    if (!cov) {
      return { state: "unrecorded", score: null,
               why: "No scores were recorded for " + (pt.label || "this round") + " — the round carries no score map at all." };
    }
    const s = cov.scores[key];
    if (s != null) return { state: "score", score: s, why: null };
    if (cov.complete) {
      return { state: "dnp", score: null,
               why: "Did not play. " + (pt.label || "This round") + " is completely fed — all " + cov.clubs +
                    " clubs, smallest side " + cov.smallestSide + " — so an absent player did not play." };
    }
    return { state: "unrecorded", score: null,
             why: "Not recorded. " + (pt.label || "This round") + "'s feed was partial — " + cov.scored +
                  " players across " + cov.clubs + " of " + coverage().clubsOnBoard +
                  " clubs (smallest side " + cov.smallestSide + "). His absence here means the feed did not " +
                  "carry him, NOT that he missed the game." };
  }

  /* the full per-player series: one entry per point, with movement against the previous point.
     The value/rank/pos-rank trace is complete for every player, so it is never gated on participation. */
  function series(key) {
    const b = bundle();
    if (!b) return null;
    const rec = (b.values || {})[key];
    if (!rec) return null;
    const pts = points();
    if (!pts.length) return null;
    let prev = null;
    return pts.map(function (pt) {
      const at = (rec.byPoint || {})[pt.id] || {};
      const row = {
        id: pt.id, roundKey: pt.roundKey, label: pt.label, isRound: pt.isRound,
        isRetro: !!pt.isRetro, modelChange: pt.modelChange,
        v: at.v == null ? null : at.v,
        rank: at.rank == null ? null : at.rank,
        posRank: at.pos_rank == null ? null : at.pos_rank,
        dv: null, dRank: null, dPosRank: null,
        score: scoreCell(key, pt),
      };
      if (prev) {
        if (row.v != null && prev.v != null) row.dv = row.v - prev.v;
        // a rank IMPROVES as the number falls, so the signed movement is prev - now.
        if (row.rank != null && prev.rank != null) row.dRank = prev.rank - row.rank;
        if (row.posRank != null && prev.posRank != null) row.dPosRank = prev.posRank - row.posRank;
      }
      prev = row;
      return row;
    });
  }

  /* how many of the tracked players the trace covers, for the card's own footnote. */
  function traceSize() {
    const b = bundle();
    return b && b.values ? Object.keys(b.values).length : 0;
  }

  return { coverage: coverage, points: points, series: series, scoreCell: scoreCell,
           traceSize: traceSize, MIN_SIDE: MIN_SIDE };
})();
