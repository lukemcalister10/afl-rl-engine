/* Matchday UI — PER-CLUB TOTALS, COMPUTED IN THE BROWSER (#139 item 21; owner ruling 2026-07-28).

   WHY THIS EXISTS. `ui/data/club_valuation.js` baked each club's totals into a generated file. A baked
   sum has to be remembered on every board move, and it was forgotten twice: the file was last generated
   2026-07-27 against board fa172ac1 / store c120cfd5 / round 19, and the board has moved twice since —
   the ITEM 411 restructure and then round 20 (board 8a38cca4, store e3aaba77). Every one of the 16
   clubs' player totals was wrong, by between +1 and +1,853.

   Item 21 framed the choice as "integrate the refresh into finalisation, or restrict operation to the
   wrapper". The owner ruled neither: compute the totals in the browser and stop baking the sum. This is
   CURRENT_STATE Part A applied to the case that produced it — do not fix the symptom of a thing that
   should not exist. A browser sums a club's players instantly and cannot go stale, because it reads the
   board the page is already showing.

   WHAT IS COMPUTED HERE vs WHAT IS STILL READ FROM THE INGEST.

     computed live from the board bundle  — totalPlayer, top5, top10, best23, nonBest23, nRoster
     read from ui/data/club_valuation.js  — picksByTeam / totalPicks

   The picks side is NOT a re-summable total and is deliberately left alone: a pick's value is the
   engine's canonical PVC evaluated over a band (`{band:"#9-11", low:9, high:11, value:1598}`), which the
   browser cannot re-derive from the board — it needs the curve. It is also not board-dependent, so it
   did not go stale when the board moved; only the player side did. `overall` = the live player total +
   the ingest's pick total, so it is as fresh as its two parts.

   PURE VIEW. This computes no price. Every figure is a sum, a top-N or a selection over the stamped
   board's own `v` — the same field the ingest used, so the two are directly comparable. No store byte,
   no board byte.

   BEST-23 is a positional SELECTION, not a sum, so it is reproduced here EXACTLY as the ingest does it
   (ui/tools/ingest_inputs.py build_clubs): roster sorted by board value descending, greedy fill of
   2 KEY_DEF · 4 GEN_DEF · 5 MID · 4 GEN_FWD · 2 KEY_FWD · 1 RUC taking the highest-valued unused player
   for each slot, then the 5 best remaining as bench. Identical algorithm, identical input, identical
   tie-breaking (both sorts are stable over the same bundle order). ui/tests/club_totals_parity.test.js
   proves the two agree club-for-club and metric-for-metric on the live board. */
window.MD = window.MD || {};

MD.clubTotals = (function () {
  const SLOTS = [["KEY_DEF", 2], ["GEN_DEF", 4], ["MID", 5], ["GEN_FWD", 4], ["KEY_FWD", 2], ["RUC", 1]];
  const BENCH = 5;
  /* The Free-Agents pool is not a club: it is never ranked and never enters a league denominator
     (item 191). Matched on the CANONICAL key, so both authored spellings fold into the one pool. */
  const FREE_LC = "free agents";

  function isFree(canonName) {
    return String(canonName || "").toLowerCase() === FREE_LC;
  }

  let _cache = null;

  function compute() {
    if (_cache) return _cache;
    const w = MD.seam.working;
    if (!w || !(w.players || []).length) return null;

    const cv = MD.seam.clubBundle;            // the ingest bundle — picks only; totals no longer read
    const halted = !!(cv && cv.halt);
    const picksByTeam = (!halted && cv && cv.picksByTeam) || {};

    /* roster by canonical AFFL club, board order preserved so the value sort ties break exactly as the
       ingest's does. Pick assets are ring-fenced out — a draft asset is not a player. */
    const rosterBy = {};
    (w.players || []).forEach(function (p) {
      if (MD.isPickAsset(p)) return;
      const t = MD.canonClub(p.affl_team);
      if (!t || isFree(t)) return;
      (rosterBy[t] = rosterBy[t] || []).push(p);
    });

    const clubs = Object.keys(rosterBy).sort().map(function (team) {
      const roster = rosterBy[team].slice().sort(function (a, b) { return b.v - a.v; });
      const totalPlayer = roster.reduce(function (s, p) { return s + p.v; }, 0);
      const sumN = function (n) { return roster.slice(0, n).reduce(function (s, p) { return s + p.v; }, 0); };

      // Best-23 — the ingest's exact greedy (see the header note).
      const used = {}, best23Keys = [];
      let best23 = 0;
      SLOTS.forEach(function (slot) {
        roster.filter(function (p) { return p.posCode === slot[0] && !used[p.key]; })
          .slice(0, slot[1])
          .forEach(function (p) { used[p.key] = 1; best23 += p.v; best23Keys.push(p.key); });
      });
      roster.filter(function (p) { return !used[p.key]; }).slice(0, BENCH)
        .forEach(function (p) { used[p.key] = 1; best23 += p.v; best23Keys.push(p.key); });

      const myPicks = picksByTeam[team] || [];
      const totalPicks = myPicks.reduce(function (s, p) { return s + p.value; }, 0);

      return {
        team: team,
        display: (MD.config.CLUB_DISPLAY && MD.config.CLUB_DISPLAY[team]) || team,
        overall: totalPlayer + totalPicks,
        totalPlayer: totalPlayer,
        totalPicks: totalPicks,
        top5: sumN(5), top10: sumN(10),
        best23: best23, nonBest23: totalPlayer - best23,
        nRoster: roster.length, nPicks: myPicks.length,
        best23Keys: best23Keys,
      };
    });

    clubs.sort(function (a, b) { return b.overall - a.overall; });

    const st = (w.stamp || {});
    _cache = {
      clubs: clubs,
      /* Provenance, stated separately for the two sides — they no longer share one stamp, and a single
         combined identity would be the false-success signal this change exists to remove. */
      playerSource: { board: st.board_md5 || st.srcmd5, store: st.store_md5, asOfRound: st.asOfRound,
                      tag: st.tag, live: true },
      picksSource: halted ? { halted: true, reason: (cv.halt || {}).reason }
                          : (cv ? { generated: (cv.stamp || {}).generated, pvcCurveMd5: (cv.stamp || {}).pvcCurveMd5,
                                    mult2027: (cv.stamp || {}).mult2027, nPicks: (cv.stamp || {}).nPicks,
                                    absent: false }
                                : { absent: true }),
      picksAvailable: !halted && !!cv,
    };
    return _cache;
  }

  function byTeam(teamLong) {
    const a = compute();
    if (!a) return null;
    const t = MD.canonClub(teamLong);
    for (let i = 0; i < a.clubs.length; i++) if (a.clubs[i].team === t) return a.clubs[i];
    return null;
  }

  /* rank among the ranked clubs by a metric (1-based); null when the club is not ranked. */
  function rankOf(teamLong, key) {
    const a = compute();
    if (!a) return null;
    const t = MD.canonClub(teamLong);
    const order = a.clubs.slice().sort(function (x, y) { return y[key || "overall"] - x[key || "overall"]; });
    for (let i = 0; i < order.length; i++) if (order[i].team === t) return i + 1;
    return null;
  }

  return { compute: compute, byTeam: byTeam, rankOf: rankOf, isFree: isFree, SLOTS: SLOTS, BENCH: BENCH };
})();
