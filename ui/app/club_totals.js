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
   (ui/tools/ingest_inputs.py build_clubs). ui/tests/club_totals_parity.test.js proves the two agree
   club-for-club and metric-for-metric on the live board — see the selector's own note below for the law
   it implements and why the greedy it replaced could not implement it. */
window.MD = window.MD || {};

MD.clubTotals = (function () {
  const SLOTS = [["KPD", 2], ["SD", 4], ["MID", 5], ["SF", 4], ["KPF", 2], ["RUCK", 1]];
  const BENCH = 5;
  const TARGET = 23;   // slots(18) + BENCH(5); the backfill fills to THIS, not to BENCH
  /* The Free-Agents pool is not a club: it is never ranked and never enters a league denominator
     (item 191). Matched on the CANONICAL key, so both authored spellings fold into the one pool. */
  const FREE_LC = "free agents";

  function isFree(canonName) {
    return String(canonName || "").toLowerCase() === FREE_LC;
  }

  /* ---------------------------------------------------------------- BEST-23: the value-maximal legal 23
     THE LAW (#271 Addendum 19, owner words 2026-07-30): "Best 23 should be the best possible 23 a team
     can fill based on their players eligible positions. Optimised, DPP can help." Metric, owner-corrected
     in the same exchange: ABSOLUTE BOARD VALUE `v`. Slots are drawn from the store's ELIGIBILITIES column,
     with DPP players assignable to EITHER eligible slot — an optimisation, explicitly not a first-fit.

     WHAT THIS REPLACED, and why it had to be replaced rather than patched. The old selector filled slots
     greedily by `posCode`, which is `grp` — the modelling/trajectory axis, one code per player. That axis
     cannot see DPP at all, so clubs showed positional shortfalls they do not have: Adelaide 3 MID-grouped
     against 5 MID slots while holding TEN dual-eligible covers (Rozee SD,MID v=2930 foremost); Hawthorn 4
     against 5 with SIX (Graham SF,MID v=1727; Nairn; Edwards). Both are fully legal in eligibility terms —
     the shortfall was an AXIS ARTIFACT, which is why "count the shortfall honestly" was rejected: it would
     have displayed false information. The adoption-day fix was a declared STOPGAP (a top-up that backfilled
     unfilled slots so no club lost a place); this is the ruled law that retires it.

     WHY AN ASSIGNMENT AND NOT A GREEDY. A greedy over eligibility is still wrong, not merely imprecise: it
     can spend a dual-eligible player on a slot that a single-eligible player could have filled, and strand
     the slot only that player could have covered. Getting it right means solving the assignment, so this is
     an exact MIN-COST MAX-FLOW: source -> each slot type (capacity = its slot count) and -> a bench node
     (capacity 5); slot -> every player eligible for it; bench -> every player; player -> sink at cost -v.
     A flow of 23 saturates the source, so it is exactly 18 legally-assigned players plus 5 bench, and
     minimising cost maximises the summed board value. Optimal, not approximate.

     PARITY IS BY TRANSLITERATION. This function, ingest_inputs.py `best23_of`, and the oracle inside
     club_totals_parity.test.js are the SAME algorithm written three times, deliberately line-for-line:
     same node numbering, same edge insertion order, same Bellman-Ford relaxation order, same
     strict-improvement rule. That is what makes the selection itself — not just its total — reproducible
     across languages, which matters because two different legal 23s can sum to the same number.

     BENCH IS UNRESTRICTED, so which 18 of the 23 are "slot" and which 5 are "bench" is not unique (a
     player can often swap between a bench place and a slot he is eligible for). The chosen SET is unique
     under this algorithm; the partition is not, so no slot assignment is exposed — publishing an arbitrary
     one would be inventing a fact.

     Returns {total, keys} with `keys` in roster order (descending v). If eligibility genuinely cannot fill
     the 18 slots the flow stops short and the club carries fewer than 23 — reported honestly, never
     topped up. */
  function best23Of(roster) {
    const n = roster.length;
    const SRC = 0;                          // 1..SLOTS.length are the slot nodes
    const BENCH_NODE = 1 + SLOTS.length;
    const P0 = BENCH_NODE + 1;              // P0 + j is player j
    const SINK = P0 + n;
    const N = SINK + 1;

    const eFrom = [], eTo = [], eCap = [], eCost = [];
    function addEdge(u, v, c, w) {
      eFrom.push(u); eTo.push(v); eCap.push(c); eCost.push(w);      // forward
      eFrom.push(v); eTo.push(u); eCap.push(0); eCost.push(-w);     // residual
    }
    for (let i = 0; i < SLOTS.length; i++) addEdge(SRC, 1 + i, SLOTS[i][1], 0);
    addEdge(SRC, BENCH_NODE, BENCH, 0);
    for (let j = 0; j < n; j++) {
      const el = roster[j].elig || [];
      for (let i = 0; i < SLOTS.length; i++) {
        if (el.indexOf(SLOTS[i][0]) >= 0) addEdge(1 + i, P0 + j, 1, 0);
      }
    }
    for (let j = 0; j < n; j++) addEdge(BENCH_NODE, P0 + j, 1, 0);
    const sinkEdge = [];
    for (let j = 0; j < n; j++) { sinkEdge.push(eCap.length); addEdge(P0 + j, SINK, 1, -(roster[j].v || 0)); }

    const E = eCap.length;
    const INF = Infinity;
    let flow = 0;
    while (flow < TARGET) {
      // Bellman-Ford over the residual graph. Edges are relaxed in INSERTION order and only on strict
      // improvement, so the predecessor tree — and therefore the augmenting path — is deterministic.
      const dist = new Array(N).fill(INF), prev = new Array(N).fill(-1);
      dist[SRC] = 0;
      for (let pass = 0; pass < N; pass++) {
        let changed = false;
        for (let e = 0; e < E; e++) {
          if (eCap[e] <= 0) continue;
          const u = eFrom[e];
          if (dist[u] === INF) continue;
          const nd = dist[u] + eCost[e];
          if (nd < dist[eTo[e]]) { dist[eTo[e]] = nd; prev[eTo[e]] = e; changed = true; }
        }
        if (!changed) break;
      }
      if (dist[SINK] === INF) break;        // eligibility cannot fill another place — stop honestly
      // every player->sink edge has capacity 1, so the bottleneck is always exactly one unit
      for (let v = SINK; v !== SRC; v = eFrom[prev[v]]) {
        const e = prev[v];
        eCap[e] -= 1;
        eCap[e ^ 1] += 1;                   // forward/residual are inserted as pairs, so XOR 1 is the twin
      }
      flow += 1;
    }

    let total = 0;
    const keys = [];
    for (let j = 0; j < n; j++) {
      if (eCap[sinkEdge[j]] === 0) { total += (roster[j].v || 0); keys.push(roster[j].key); }
    }
    return { total: total, keys: keys };
  }

  /* ------------------------------------------------------------------- THE PICKS PIN (v827, 2026-08-21)
     THE #232 MIRROR LAW, ONE CARRIER ALONG. `ui/data/club_valuation.js` is a GENERATED bundle stamped
     with the board + store it was generated from, and until tonight this module honoured whatever
     bundle was present — `halted = !!(cv && cv.halt)`, with no comparison of that stamp against the
     board the app is loaded on. That is exactly the hole #232 left in the ownership sidecar and #283
     closed with `MD.ownership.pin()`: a mirror that does not name the identity it was generated from
     cannot be told apart from a stale one, and one that names it and is never asked is no better.

     MEASURED, NOT HYPOTHETICAL. On 2026-08-21 the shipped bundle carried board a05fe951 / R22 while
     the tree stood on b3e8da99 / R23. The pocket and club pages showed R22-board pick VALUES with
     nothing refusing and nothing flagged — a silent wrong number, which is the one outcome the owner's
     word that night forbids: "It is essential that the UI displays the correct player locations and
     pick locations."

     WHY IT REFUSES RATHER THAN DEGRADES, unlike the ownership mirror. A refused ownership mirror falls
     back to the board's own store-derived `affl_team`, which since #283 is the same field — a degraded
     display, never a wrong club. There is no such fallback for a pick's price: it is the engine's
     canonical PVC evaluated over a band, and the browser cannot re-derive it from the board (that is
     this module's founding argument, above). So a stale bundle's picks go to the HALTED path — Picks
     and Overall read `n/a`, never 0 and never a stale figure — with a reason naming BOTH identities.

     Same shape and same field names as `MD.ownership.pin()`: `{ok, why}`, checked against the working
     bundle's stamp, comparing store first and then board. */
  function pin() {
    const cv = MD.seam.clubBundle;
    const st = (cv && cv.stamp) || {};
    const w = ((MD.seam && MD.seam.working) || {}).stamp || {};
    if (!cv) return { ok: false, why: "the picks bundle is absent" };
    if (cv.halt) {
      return { ok: false, why: (cv.halt.reason || "the ingest refused to write a picks bundle") };
    }
    if (!st.store || !st.board) {
      return { ok: false, why: "the picks bundle carries no board/store stamp, so it cannot be authenticated" };
    }
    if (w.store && st.store !== w.store) {
      return { ok: false, why: "the picks bundle was generated from store " + String(st.store).slice(0, 8)
                              + " but the app is loaded on store " + String(w.store).slice(0, 8) };
    }
    if (w.board && st.board !== w.board) {
      return { ok: false, why: "the picks bundle was generated from board " + String(st.board).slice(0, 8)
                              + " but the app is loaded on board " + String(w.board).slice(0, 8) };
    }
    return { ok: true, why: null };
  }

  let _cache = null;

  function compute() {
    if (_cache) return _cache;
    const w = MD.seam.working;
    if (!w || !(w.players || []).length) return null;

    const cv = MD.seam.clubBundle;            // the ingest bundle — picks only; totals no longer read
    /* The pin decides, not the presence of the bundle. An unauthenticated bundle is treated exactly as
       an ingest halt is: no picks are read from it at all. */
    const pn = pin();
    const halted = !pn.ok;
    const picksByTeam = (!halted && cv && cv.picksByTeam) || {};

    /* roster by canonical AFFL club, board order preserved so the value sort ties break exactly as the
       ingest's does. Pick assets are ring-fenced out — a draft asset is not a player. */
    const rosterBy = {};
    (w.players || []).forEach(function (p) {
      if (MD.isPickAsset(p)) return;
      const t = MD.canonClub(MD.ownership.clubOf(p));   // #232: sidecar overrides, store falls back
      if (!t || isFree(t)) return;
      (rosterBy[t] = rosterBy[t] || []).push(p);
    });

    const clubs = Object.keys(rosterBy).sort().map(function (team) {
      const roster = rosterBy[team].slice().sort(function (a, b) { return b.v - a.v; });
      const totalPlayer = roster.reduce(function (s, p) { return s + p.v; }, 0);
      const sumN = function (n) { return roster.slice(0, n).reduce(function (s, p) { return s + p.v; }, 0); };

      // Best-23 — the ruled value-maximal legal 23 (see best23Of's note); identical to the ingest's.
      const sel = best23Of(roster);
      const best23 = sel.total, best23Keys = sel.keys;

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
      /* PROVENANCE, NOT A CLOCK. This read `generated: cv.stamp.generated` — the bundle's wall-clock
         timestamp — until v827 dropped that field so the bundle could be byte-proved and become a
         landing carrier. A timestamp never answered the question a reader has anyway ("is this the
         tree I am looking at?"); the identity fields do, and they are the same ones `pin()` checks. */
      picksSource: halted ? { halted: true, reason: pn.why, pinOk: false }
                          : { board: (cv.stamp || {}).board, store: (cv.stamp || {}).store,
                              engine: (cv.stamp || {}).engine, asOfRound: (cv.stamp || {}).asOfRound,
                              tag: (cv.stamp || {}).tag,
                              pvcCurveMd5: (cv.stamp || {}).pvcCurveMd5,
                              pvcCurveFileMd5: (cv.stamp || {}).pvcCurveFileMd5,
                              mult2027: (cv.stamp || {}).mult2027, nPicks: (cv.stamp || {}).nPicks,
                              pinOk: true, absent: false },
      picksAvailable: !halted,
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

  return { compute: compute, byTeam: byTeam, rankOf: rankOf, isFree: isFree, pin: pin,
           SLOTS: SLOTS, BENCH: BENCH };
})();
