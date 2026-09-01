/* Matchday UI — DRAFT DAY (owner UI item 13, "the draft-day translator").

   THE QUESTION THIS PAGE ANSWERS
   ------------------------------
   You are holding pick 34. What has pick 34 actually become?

   That is a different question from the one the Pick Value tab answers. Pick Value says what a pick
   is WORTH — the adopted curve, and the entry price the surface pays by position. This page says
   what a pick has HISTORICALLY PRODUCED — games, debuts, best seasons, and how often nothing at all.
   A price and an outcome are not the same object and this page never mixes them: it reads the
   outcome record and, separately, joins the live board so the men who are still tracked show what
   they are worth today, with the count of how many survived to be joined printed beside it.

   WHY THE BASE RATES ARE REAL — AND THE ONE REASON THEY USUALLY ARE NOT
   --------------------------------------------------------------------
   Tools like this are normally built on a list of players who made it, which makes every pick look
   like a good pick. The record behind this page is a COMPLETE draft class list: 2003 onward, from
   pick 1, with 23 observations at nearly every ordinal, and 232 of the 1570 selections never played
   a senior game. The generator re-proves that count on every run and carries it in the stamp, and
   this page PRINTS IT, because a reader is entitled to check the one assumption everything else
   rests on rather than take it on faith.

   A YOUNG PLAYER IS NOT A FAILED ONE
   ----------------------------------
   A 2025 draftee who has not played is nineteen. Counting him as a bust would poison every recent
   class — 2025 currently reads 44.8% "never played" against a mature-class norm near 12%. So the
   classes are split, and the boundary is MEASURED, not chosen: among classes with time to settle,
   99% of eventual debutants had debuted within four completed seasons, so four is the DEBUT line.
   It is not the line this board runs on — see TWO DIFFERENT QUESTIONS below — because a peak takes
   far longer to arrive than a debut; the default is eleven seasons, where 93% of first-star seasons
   have landed. The younger classes are not hidden — they are reported on their own line, with how
   many have already debuted — but they are kept out of the rates. The debut threshold comes off the
   bundle (`stamp.maturitySeasons`) with the table it was measured from; the peak threshold is
   measured in this file, from the same kind of evidence, because it needs the star lines.

   AND THE OLD END IS CUT TOO. The class of 2003 is excluded outright (YR_LO), not for being
   unsettled but because the store holds no 2004 seasons: its year one is unobservable. The house's
   own pick-value harness (session_2026-07-30/item279/panel/harness_pvc.py) draws the same floor.
   There is no era adjustment at either end and none is wanted: SuperCoach assigns a fixed 3,300
   points a match, so averages are comparable across seasons by construction (ENGINE_PRIMER 4.10).

   THE PAGE PASSES NO JUDGEMENT
   ----------------------------
   There is no hit rate here, and no bust flag. A "hit" needs a threshold, a threshold is a ruling,
   and no such ruling exists — so this reports distributions (median and quartiles) and lets the
   owner put his own line through them. The one CURRENCY figure on the panel is the pick's own price
   off the adopted curve, which is a price and not a return; the survivorship-shaped reading (what
   these men are worth today) appears only per player, in the roll, where it cannot be mistaken for
   a rate. See the note on priceOf below for the tile that was built and then removed.

   THIN SAMPLES ARE MARKED, NOT SMOOTHED. One ordinal is 23 careers at most, and fewer once the
   still-running classes come out. The neighbourhood control widens the set on purpose and SAYS which
   ordinals it pooled; nothing is ever interpolated, and a set at or under the thin bar wears a dot.

   PURE VIEW. It computes no price and derives no valuation. */
(function (root) {
  "use strict";

  /* A set resting on this many careers or fewer is marked. Same marker and same intent as the Pick
     Value page's dot: it does not hide the figure, it warns what the figure is standing on. */
  /* THE MINIMUM STRATUM, TAKEN FROM THE HOUSE. This was 8 — chosen here, in ignorance. The ruled
     curve's evidence panel declares MIN_STRATUM = 20 (session_2026-07-30/item279/panel/
     harness_pvc.py:27), which is the size below which the estate does not treat a cell as a
     stratum worth reading. Raising 8 to 20 marks a great many more cells on this board, and that
     is the point: they were always thin and the old bar said otherwise. */
  var THIN_MAX = 20;

  /* ============================== THE PURE CORE ==============================================
     Every selection and every rate on this page is computed HERE, off arguments, with no globals
     read and no DOM touched — the same split ui/app/pickvalue.js uses, and for the same reason:
     the honesty properties (what is excluded, what the denominator is, what a quantile means) are
     the things worth testing, and a function that reaches for `window` can only be tested through
     a browser. ui/tests/draftday.test.js drives this object directly, against both hand-built
     fixtures and the shipped record. */
  var core = (function () {
    /* A class is mature when it has had `maturitySeasons` COMPLETED seasons since its draft. The
       draft happens after the season it is named for, so class Y's first playing season is Y+1 and
       seasonNow - Y is exactly the number of seasons it has had. */
    function classAge(stamp, y) { return (stamp.seasonNow || 0) - y; }

    /* HOW LONG A CLASS HAS HAD, AGAINST AN EXPLICIT MINIMUM. This used to be `isMature`, a boolean
       that silently meant "four seasons" — the bundle's debut threshold — and that silence is what
       let a debut rule gate the PEAK questions for a day. The minimum is now always passed in, so
       every caller has to say which question it is asking. 0 means every class. */
    function hasRun(stamp, y, minSeasons) {
      return classAge(stamp, y) >= (minSeasons || 0);
    }
    // kept for the maturity-rule tests and any caller genuinely asking the DEBUT question
    function isMature(stamp, y) { return hasRun(stamp, y, stamp.maturitySeasons || 0); }

    /* ================= TWO DIFFERENT QUESTIONS SETTLE AT TWO DIFFERENT TIMES ==================
       The bundle's `maturitySeasons` (4) was derived for ONE question — has he debuted — and 99% of
       eventual debutants have by then. It was then reused to gate the PEAK questions (value over
       the bar, star rate), and that was wrong. Measured on classes with a full run: only 31% of
       first-star seasons have arrived by four seasons. 45% by five, 60% by six, 93% by ten.

       WHAT IT COST, measured: star rate 15.3% on the 4-season population against 17.0% on a
       fully-run one, and the error is not uniform — picks 41-64 read 7.4% against 9.7% (a third
       understated) while picks 1-10 read 42.5% against 45.0%. Late picks develop slower, so the
       immature classes penalise exactly the picks the board is used to judge. It also FLIPPED the
       headline: rucks lead midfielders on star rate at four seasons, midfielders lead rucks at
       twelve.

       So the peak questions get their own threshold, derived the same way and from the same kind of
       evidence — the lag by which most first-star seasons have landed. It is computed here rather
       than in the generator because it needs the STAR LINES, which live on the board; the generator
       still holds no bar. */
    function developedFromRows(rows, stamp, board, want, seasonStarFn) {
      var need = (want == null) ? 0.9 : want;
      var lags = {}, total = 0;
      (rows || []).forEach(function (r) {
        /* Only classes with a long run may TEACH the threshold, or the measurement is contaminated
           by the very immaturity it exists to detect. Ten seasons is the same discipline the debut
           lag uses (seven there), scaled to a question that takes longer to answer. */
        if ((stamp.seasonNow || 0) - r.y < 14) return;
        var first = null;
        (r.s || []).forEach(function (sn) {
          var sb = seasonStarFn(board, sn[1]);
          if (sb == null || sn[0] < sb || sn[2] == null) return;
          var lag = sn[2] - r.y;                       // SEASONS SINCE THE DRAFT, exactly
          if (first === null || lag < first) first = lag;
        });
        if (first === null) return;
        lags[first] = (lags[first] || 0) + 1;
        total++;
      });
      if (!total) return null;
      /* THE LAG IS THE THRESHOLD, WITH NO +1. A star arriving four seasons after the draft happened
         when that class was four seasons old, so admitting it needs classAge >= 4. The +1 that
         stood here was carried over from an earlier version that counted seasons of FOOTBALL rather
         than seasons since the draft, where it was right; once the lag became exact it made the
         threshold a year too strict and cost a whole draft class of evidence for nothing. */
      var cum = 0, keys = Object.keys(lags).map(Number).sort(function (a, b) { return a - b; });
      for (var i = 0; i < keys.length; i++) {
        cum += lags[keys[i]];
        if (cum / total >= need) return { lag: keys[i], n: total, cum: cum / total };
      }
      return { lag: keys[keys.length - 1], n: total, cum: 1 };
    }

    /* THE MATURITY THRESHOLD, RE-DERIVED FROM THE TABLE THE BUNDLE SHIPS. The generator computes it
       and the bundle carries it; this recomputes it from the bundle's own evidence, so a stamp
       whose threshold does not follow from its own lag table is caught rather than believed. */
    function maturityFromLags(table, want) {
      var need = (want == null) ? 0.99 : want;
      for (var i = 0; i < (table || []).length; i++) {
        if (table[i].cum >= need) return table[i].lag;
      }
      return (table && table.length) ? table[table.length - 1].lag : 0;
    }

    /* THE SELECTION, AND THE PARTITION THAT MAKES IT HONEST. Every row inside the ordinal window
       lands in exactly one of `set` and `young` — nothing is dropped silently, so the page can say
       how many were held out and why instead of quietly shrinking its own denominator. */
    function select(rows, stamp, state) {
      var lo = state.pick - state.spread, hi = state.pick + state.spread;
      var picked = [], young = [];
      (rows || []).forEach(function (r) {
        if (r.p < lo || r.p > hi) return;
        if (state.pos && r.dp !== state.pos) return;
        if (state.yrLo && r.y < state.yrLo) return;      // the class floor: 2003 has no year one
        if (!hasRun(stamp, r.y, state.minSeasons)) young.push(r);
        else picked.push(r);
      });
      return { set: picked, young: young, lo: Math.max(lo, 1), hi: hi };
    }

    function quantile(sorted, q) {
      if (!sorted.length) return null;
      var i = (sorted.length - 1) * q, lo = Math.floor(i), hi = Math.ceil(i);
      return sorted[lo] + (sorted[hi] - sorted[lo]) * (i - lo);
    }

    /* The base rates. Every one is a count over the SAME denominator, which is printed beside it,
       so no figure on this page is a percentage of something the reader has to guess at. `values`
       is injected — the live board value per key, or an empty map — so the core never reaches for
       the board and the one survivorship-shaped figure can be tested with and without one. */
    function rates(set, values) {
      var vals = values || {};
      var n = set.length;
      var games = set.map(function (r) { return r.g; }).sort(function (a, b) { return a - b; });
      var peaks = set.filter(function (r) { return r.pk != null; })
                     .map(function (r) { return r.pk; }).sort(function (a, b) { return a - b; });
      var played = set.filter(function (r) { return r.g > 0; });
      var live = [];
      set.forEach(function (r) { if (vals[r.k] != null) live.push(vals[r.k]); });
      live.sort(function (a, b) { return a - b; });
      return {
        n: n,
        never: n - played.length,
        played: played.length,
        g50: set.filter(function (r) { return r.g >= 50; }).length,
        g100: set.filter(function (r) { return r.g >= 100; }).length,
        g200: set.filter(function (r) { return r.g >= 200; }).length,
        gamesMed: quantile(games, 0.5),
        gamesQ1: quantile(games, 0.25),
        gamesQ3: quantile(games, 0.75),
        nPeak: peaks.length,
        peakMed: quantile(peaks, 0.5),
        peakQ1: quantile(peaks, 0.25),
        peakQ3: quantile(peaks, 0.75),
        nLive: live.length,
        liveMed: quantile(live, 0.5),
      };
    }

    /* THE PIN, as a pure predicate over the two stamps. The record is generated from a store; the
       app runs on a board generated from a store. If those are not the same store, the careers on
       screen are not the careers behind the live board, and the page refuses rather than showing a
       near-miss. Same law as MD.v0 and MD.ownership — a mirror that does not name the identity it
       was generated from is not a mirror — and it is CHECKED rather than assumed, because the
       defect this session opened with was exactly a sidecar nobody re-checked.

       `store_md5` first and `store` only as a fallback: the board stamp carries both and the second
       is an eight-character abbreviation of the first, so the full digest is what gets compared
       whenever the bundle publishes it (the order ui/app/v0.js:79 reads them in). Where only the
       abbreviation exists, one must be a prefix of the other — a weaker check, and the only one the
       data supports; it is never silently presented as equality. */
    function pinOf(bundleStamp, boardStamp) {
      if (!bundleStamp) {
        return { ok: false, why: "the draft outcome record (ui/data_aux/draft_outcomes.js) is not loaded" };
      }
      if (!bundleStamp.store) {
        return { ok: false, why: "the draft outcome record names no store, so it cannot be checked against the loaded board" };
      }
      var want = (boardStamp || {}).store_md5 || (boardStamp || {}).store;
      var got = String(bundleStamp.store);
      if (want) {
        want = String(want);
        if (got.indexOf(want) !== 0 && want.indexOf(got) !== 0) {
          return { ok: false, why: "the draft outcome record was generated from store " + got.slice(0, 8) +
                                   ", but the loaded board is on store " + want.slice(0, 8) +
                                   " — regenerate with ui/tools/gen_draft_outcomes.py" };
        }
      }
      return { ok: true };
    }

    /* The adopted curve's price across an ordinal range — the ONE currency figure on the panel, and
       a price rather than a return, so it cannot be mistaken for what these careers paid back. */
    function priceRange(pvc, lo, hi) {
      if (!pvc) return null;
      var vals = [];
      for (var n = lo; n <= hi; n++) {
        var v = pvc[String(n)];
        if (typeof v === "number") vals.push(v);
      }
      if (!vals.length) return null;
      return { lo: Math.min.apply(null, vals), hi: Math.max.apply(null, vals), n: vals.length };
    }

    /* ============================ THE VALUE FRAME ==============================================
       Everything below converts a (position, pick) into ONE currency: THE MIDFIELDER PICK IT IS
       WORTH. That is the whole point of the board — "a key forward at pick 5 is worth a midfielder
       at pick 17" is a sentence you can act on at the clock; "expected peak 75.3" is not.

       THREE FIGURES PER CELL, and each answers a different question:

         VOR      — expected value OVER REPLACEMENT. Mean of max(0, best season - replacement) over
                    EVERY selection at that position and pick neighbourhood, busts included at zero.
                    That is what makes it an expectation and not a highlight reel: a position that
                    produces one star and nine nothings scores far below one that produces ten
                    useful players, which is the correct ordering for a keeper draft.
         STARTABLE— the share who ever reach a season at or above replacement. The floor.
         STAR     — the share who ever reach a difference-maker season, on the league-wide bar. The
                    ceiling.

       A position can be strong on one and weak on another and that is the finding, not a defect:
       key defenders are startable astonishingly deep and almost never stars; midfielders own the
       stars. Showing all three is what stops the board being read as one number.

       REPLACEMENT IS NOT CHOSEN. It comes off the owner's own ruled starting slots (5 mids, 1 ruck,
       ... per club) times the counted club count, measured on the current season — so the 80th-best
       midfielder and the 16th-best ruck ARE, by the league's own definition, the last men holding a
       slot. The generator publishes it with the pool behind it. */

    /* The careers behind one (position, pick) cell. `half` widens the neighbourhood because a single
       ordinal is at most one career per class; it is a control on the page, never a hidden smoothing,
       and every cell reports the n it stands on. */
    function careers(rows, stamp, pos, pick, half, minSeasons, yrLo) {
      var lo = pick - half, hi = pick + half;
      return (rows || []).filter(function (r) {
        if (r.dp !== pos || r.p < lo || r.p > hi) return false;
        if (yrLo && r.y < yrLo) return false;
        return hasRun(stamp, r.y, minSeasons);
      });
    }

    /* THE REPLACEMENT BAR IS THE MODEL'S OWN, READ OFF THE BOARD. rl_model.py:824 —
       REPL = {MID 80.1, SD 78.3, RUCK 78.5, KPD 68.4, SF 70.9, KPF 66.8}, v3.3 derived by
       rl_replacement_derive.py with the owner's 2026-07-04 dial on KPF. It has been baked into this
       model for months and it is what every other surface measures against.

       THIS FUNCTION USED TO READ A LEVEL THIS APP DERIVED FOR ITSELF, and that was the defect. The
       first version came off the best-23 slot law, which is a roster-shape rule and not a
       replacement level; when told not to derive, the second version reached for the passmark, which
       was still this seat choosing. Both disagreed with the baked bar, worst at SF — a derived 57.7
       against 70.9 — and that single row was enough to invert the small-forward reading on the
       board. `frame` is now handed the number the engine prices against, and the frame refuses when
       the board does not publish one rather than substituting anything. */
    function replOf(board, pos) {
      /* REPL_BAR, NOT REPL. The raw literal is not the bar a player is measured against: the pricing
         core lowers every one of them by a uniform dial before use (RL_REPL_DROP = 3 in the declared
         config; dist_redesign.py:35-39, applied at _merged_recover.py:495). So the live bars are
         MID 77.1, SD 75.3, RUCK 75.5, KPD 65.4, SF 67.9, KPF 63.8 — three points below the literal
         at every position.

         Reading REPL would sit this whole board three points above every real bar. It is a small
         number and it is not a small error: it shifts every "clears the bar" share and every value
         over replacement on the page, in the same direction, at once.

         The fallback to REPL is deliberate and narrow: a bundle published before REPL_BAR existed
         carries only the literal, and showing it is better than showing nothing — but it is the
         literal, and `replBarIsEffective` below lets the page say so rather than imply otherwise. */
      var b = (board || {}).REPL_BAR;
      var v = (b && b[pos] != null) ? b[pos] : ((board || {}).REPL || {})[pos];
      return typeof v === "number" ? v : null;
    }

    /* whether the bar in use is the one the engine prices against, or the un-dropped literal. */
    function replBarIsEffective(board) {
      return !!((board || {}).REPL_BAR) && typeof (board || {}).REPL_DROP === "number";
    }

    /* THERE IS NO "STAR" FIGURE ON THIS PAGE, AND THAT IS A DECISION.
       The board publishes PEAK beside REPL and it is tempting to read it as a star bar. It is not
       the same kind of object: SF's PEAK is 70 against a REPL of 70.9, and SD's 78 against 78.3 —
       a "star" bar BELOW the replacement bar at two positions, which no ceiling can be. Reading it
       that way would have been the third bar this page invented for itself in a day.
       So the page measures against the ONE baked bar that is a replacement bar, and reports no
       ceiling at all. If a star line is wanted it needs a baked constant that is one; until such a
       constant is named, an absent figure is the honest one. */

    /* the three figures for one set of careers, against that position's own replacement level. */
    /* THE SEASON'S BAR IS THE POSITION HE PLAYED, THE CREDIT IS THE POSITION HE WAS DRAFTED AS.
       The owner's ruling, 2026-08-31, verbatim:

         "A player drafted as a mid who then switched to SF mid career and scored 95 over a 67 bar
          is +28, and that's credited to the midfield role he was drafted to. A player drafted as a
          KPF who switched to a mid mid career and scores 75 that season over a 77 bar doesn't
          contribute much even though the KPF bar is lower than his average."

       Two axes, two jobs. What you buy on draft day is the midfield selection, so the MIDFIELD row
       owns the outcome. But what the outcome IS depends on the job he actually did — a mid playing
       forward is measured as a forward. Measuring everyone against his drafted bar for life would
       have scored that KPF-turned-mid as eleven points clear of a 63.8 bar instead of below a 77.1
       one, and one in five settled selections changes position.

       A DUAL SEASON ("SF/MID", "KPF/RUCK") TAKES THE LOWER BAR, which is the engine's own rule for a
       dual declaration — rl_model.py:85, `min(es, key=lambda g: REPL[g])`, "the LOWER REPL = more
       valuable for him". Not a choice made here; the collapse the model already performs. */
    /* THE STAR LINE per position — the owner's ruled figure, published from
       docs/inputs/OWNER_STAR_SEASONS.json. Returns null when no line is declared, and the board
       then draws no star column at all rather than inventing one. */
    function starOf(board, pos) {
      var v = ((board || {}).STAR_BAR || {})[pos];
      return typeof v === "number" ? v : null;
    }

    function seasonBar(board, seasonPos) {
      var codes = String(seasonPos || "").split("/");
      var best = null;
      for (var i = 0; i < codes.length; i++) {
        var v = replOf(board, codes[i].trim());
        if (v != null && (best === null || v < best)) best = v;   // LOWER bar, the engine's rule
      }
      return best;
    }

    /* THE STAR LINE FOR A SEASON, collapsed the same way the floor is: a dual season takes the
       LOWER line, because it takes the lower floor and the two must describe the same job. Reading
       the higher star line against the lower floor would make a dual season simultaneously the
       easiest to clear and the hardest to star in, which is not one position's story. */
    function seasonStar(board, seasonPos) {
      var codes = String(seasonPos || "").split("/");
      var best = null;
      for (var i = 0; i < codes.length; i++) {
        var v = starOf(board, codes[i].trim());
        if (v != null && (best === null || v < best)) best = v;
      }
      return best;
    }

    function frame(set, board, pos) {
      var repl = replOf(board, pos);
      if (!set.length || repl == null) return null;
      var vor = 0, nStart = 0, nMeasured = 0, nCross = 0, nStar = 0, nBust = 0;
      var hasStar = !!(board || {}).STAR_BAR;
      set.forEach(function (r) {
        /* A player's value is his BEST season's excess over THAT SEASON'S bar. Best-season is the
           unchanged semantic; which bar applies is what the ruling changed. A season the board
           publishes no bar for is skipped rather than measured against the drafted position's — an
           unresolvable position is missing evidence, not evidence of nothing. */
        var seasons = r.s || [];
        var bestExcess = null, measured = false, crossed = false, starred = false;
        for (var i = 0; i < seasons.length; i++) {
          var bar = seasonBar(board, seasons[i][1]);
          if (bar == null) continue;
          measured = true;
          if (seasons[i][1] !== pos) crossed = true;
          var e = seasons[i][0] - bar;
          if (bestExcess === null || e > bestExcess) bestExcess = e;
          /* A STAR SEASON IS ONE CLEARING THE LINE FOR THE POSITION HE PLAYED — and the credit
             lands on the row of the position he was DRAFTED as. Exactly the owner's rule for the
             floor, applied to the ceiling: "a player who changes positions is measured against that
             season's bar, and if they clear it, it credits their original draft position for the
             success." One star season is enough; a career is starred by its best year, not its
             average, which is the point of having the line at all. */
          var sb = seasonStar(board, seasons[i][1]);
          if (sb != null && seasons[i][0] >= sb) starred = true;
        }
        if (measured) nMeasured++;
        if (crossed) nCross++;
        if (starred) nStar++;
        /* BUST = never produced a measurable season at all. Deliberately NOT "never cleared the
           bar", which is just the complement of the clear rate and would say nothing new. This is
           the harder failure the owner asked to see: the pick that returned no football worth
           measuring. It is a share of EVERY selection, busts included in the denominator, which is
           the whole reason this record carries the men who never played. */
        if (!measured) nBust++;
        /* A player with NO measurable season still counts in the denominator at zero — he is a
           selection that returned nothing, and dropping him would turn every rate into a survivor
           rate. That is the whole reason this record carries the men who never played. */
        if (bestExcess != null && bestExcess > 0) vor += bestExcess;
        if (bestExcess != null && bestExcess >= 0) nStart++;
      });
      return { n: set.length, vor: vor / set.length,
               startable: nStart / set.length, repl: repl,
               star: hasStar ? nStar / set.length : null,
               starBar: starOf(board, pos),
               bust: nBust / set.length,
               nMeasured: nMeasured, nCross: nCross };
    }

    /* THE MIDFIELD YARDSTICK. The midfielder curve is the ruler every other cell is read against, so
       it is built once over every ordinal and then searched for the pick whose VOR is nearest.

       WHY A MIDFIELDER AND NOT A DOLLAR. The pick-value curve prices a pick; it does not know what
       you will do with it. On the clock the question is never "is this worth 530 points", it is
       "would I rather have this key forward or a midfielder later" — and the midfielder is the only
       position deep and star-rich enough to be a stable ruler across the whole board. */
    function midCurve(rows, stamp, board, half, minSeasons, yrLo) {
      var out = [];
      for (var p = 1; p <= 64; p++) {
        var f = frame(careers(rows, stamp, "MID", p, half, minSeasons, yrLo), board, "MID");
        if (f && f.n) out.push({ p: p, vor: f.vor, n: f.n });
      }
      return out;
    }

    /* the midfielder pick whose VOR is closest to `v`. Returns null past the ruler's own range
       rather than extrapolating: a cell worth more than a pick-1 midfielder has no answer on this
       scale and must say so, not print "mid 0". */
    function midEquivalent(curve, v) {
      if (!curve.length || v == null) return null;
      var best = null;
      curve.forEach(function (c) {
        var d = Math.abs(c.vor - v);
        if (best === null || d < best.d) best = { p: c.p, d: d, vor: c.vor };
      });
      if (!best) return null;
      var top = curve[0], tail = curve[curve.length - 1];
      // OFF THE SCALE, both ends, said rather than clamped silently.
      if (v > top.vor) return { p: top.p, beyond: "above", vor: best.vor };
      if (v < tail.vor) return { p: tail.p, beyond: "below", vor: best.vor };
      return { p: best.p, beyond: null, vor: best.vor };
    }

    return { classAge: classAge, isMature: isMature, maturityFromLags: maturityFromLags,
             select: select, quantile: quantile, rates: rates, pinOf: pinOf, hasRun: hasRun,
             priceRange: priceRange, THIN_MAX: THIN_MAX,
             careers: careers, replOf: replOf, replBarIsEffective: replBarIsEffective,
             seasonBar: seasonBar, seasonStar: seasonStar, starOf: starOf, frame: frame,
             developedFromRows: developedFromRows,
             midCurve: midCurve, midEquivalent: midEquivalent };
  })();

  function makeView(MD) {
  var fmt = MD.fmt;

  /* minSeasons DEFAULTS TO null AND IS RESOLVED AT FIRST RENDER to the DEVELOPED threshold — the
     one derived for the peak questions, not the debut one. See classFilter() for why the default is
     the strict population despite costing sample. */
  var state = { pick: 1, spread: 0, pos: null, minSeasons: null, roll: false,
                half: 8, view: "board",
                a: { pos: "KPF", pick: 5 }, b: { pos: "KPD", pick: 5 } };

  /* THE SIX POSITIONS, IN THE OWNER'S OWN ORDER AND HIS OWN WORDS. The store's codes are terse
     modelling labels; these are what the positions are called when you are talking about a draft. */
  var POS_ORDER = ["MID", "RUCK", "SF", "KPF", "SD", "KPD"];
  var POS_LABEL = { MID: "MIDFIELDER", RUCK: "RUCK", SF: "GEN / SMALL FWD",
                    KPF: "KEY FORWARD", SD: "GEN / REBOUND DEF", KPD: "KEY DEFENDER" };
  var POS_SHORT = { MID: "MID", RUCK: "RUC", SF: "G FWD", KPF: "K FWD", SD: "G DEF", KPD: "K DEF" };

  /* The columns of the board. Dense early where the curve is steep and every ordinal matters,
     sparse late where it is flat — the same spacing the owner's own board used, and the reason it
     fits on one screen without a scroll. */
  /* THE COLUMNS ARE POINT PICKS, NOT THE HOUSE'S BANDS. harness_pvc.py strata the draft into
     RANGES = [(1,10),(11,20),(21,30),(31,45),(46,64)] and that is right for FITTING a curve, where
     the question is "how does this stretch of the draft behave". It is the wrong shape for draft
     day, where the question is "I hold pick 15" — a band that runs 11-20 answers a pick 11 and a
     pick 20 with the same number, and those are not the same pick. So the columns are picks, each
     read over a +/-8 window (adjustable), and thinness is marked rather than hidden by widening. */
  var BOARD_PICKS = [1, 3, 6, 10, 15, 21, 30, 42, 58];

  function bundle() {
    return (typeof window !== "undefined" && window.__DRAFT_OUTCOMES__) || null;
  }

  function pin() {
    var b = bundle();
    return core.pinOf(b && b.stamp, MD.seam.working.stamp);
  }

  function rows() { var b = bundle(); return (b && b.rows) || []; }
  function stamp() { var b = bundle(); return (b && b.stamp) || {}; }
  /* THE BOARD, for its baked position constants (REPL / PEAK). The outcome record carries careers;
     the board carries what a career is measured against. Two sources, two jobs, and the split is
     the whole point — this page must never hold a bar of its own. */
  function board() { return (MD.seam && MD.seam.working) || {}; }

  /* THE CLASS FLOOR, AND WHY IT IS 2004 AND NOT 2003.
     The store's earliest recorded season is 2005, so the 2003 class has NO observable year one —
     every one of its debut lags reads a year late and every "how long did this take" measured on it
     is wrong. The owner caught this; the house had already ruled it, and the ruled curve's own
     evidence panel carries the same floor:

         session_2026-07-30/item279/panel/harness_pvc.py:31   YR_LO = 2004

     Measured on the debut lags, including 2003 moved the derived debut threshold from 5 to 4 across
     a 0.05% margin — a knife-edge answer resting on a class whose first year cannot be seen. */
  var YR_LO = 2004;
  function inWindow(r) {
    return r.y >= YR_LO && core.hasRun(stamp(), r.y, state.minSeasons);
  }
  function inRun(y) { return core.hasRun(stamp(), y, state.minSeasons); }
  /* The detail panel below the board reads the SAME window the board's cells do, so a cell you
     clicked and the careers listed under it cannot disagree about which men they are. */
  function select() {
    return core.select(rows(), stamp(),
      { pick: state.pick, spread: state.half, pos: state.pos, minSeasons: state.minSeasons,
        yrLo: YR_LO });
  }
  var quantile = core.quantile;

  /* THE PEAK-MATURITY THRESHOLD, derived once per load from the record's own first-star lags and
     the board's star lines. Memoised because it walks every row and the controls re-render often. */
  var _dev = null;
  function developedThreshold() {
    if (_dev) return _dev;
    /* DERIVED ON THE SAME WINDOW THE BOARD READS. The threshold measures how long careers take;
       measuring it on a class whose first year is unobservable makes every one of its lags a year
       long. Including 2003 gave 10 seasons, excluding it gives 11 — and the board would then have
       been filtered on one number while its own evidence supported another. */
    var r = core.developedFromRows(rows().filter(function (x) { return x.y >= YR_LO; }),
                                   stamp(), board(), 0.9, core.seasonStar);
    /* No star lines, or no fully-run class to measure — fall back to the debut threshold and say so
       rather than inventing a number. */
    _dev = r || { lag: stamp().maturitySeasons || 4, n: 0, cum: null, fallback: true };
    return _dev;
  }

  function ordinals() {
    var seen = {};
    rows().forEach(function (r) { seen[r.p] = 1; });
    return Object.keys(seen).map(Number).sort(function (a, b) { return a - b; });
  }

  /* the live board value per key, which is the ONLY thing the core needs from the board. Passing a
     map in keeps the rate arithmetic testable without a board and makes the survivorship-shaped
     column an argument rather than a hidden dependency. */
  function liveValues(set) {
    var byKey = ((MD.seam && MD.seam.indexed) ? MD.seam.indexed().byKey : {}) || {};
    var out = {};
    set.forEach(function (r) {
      var p = byKey[r.k];
      if (p) out[r.k] = MD.dispVal ? MD.dispVal(p) : p.v;
    });
    return out;
  }

  function rates(set) { return core.rates(set, liveValues(set)); }

  /* THE PRICE SIDE, read off the board's own published curve — the bridge between this page and the
     Pick value tab.

     A "what are these men worth today" tile was built here first and then TAKEN OUT, which is worth
     recording so that it is not rebuilt. It read 1,680 at pick 1 against 1,480 at picks 32-36 —
     nearly identical, and for a reason with nothing to do with the draft: the board is a keeper
     league of CURRENT players, so a pick-1 selection from 2006 is a 38-year-old who is not on it
     and a 2010 one is a veteran priced as a veteran. The figure measured how recently a man was
     drafted, not how good his pick was. It was labelled "survivors only" and carried its count, and
     it was still going to be read as a return on the pick. A label does not repair a comparison
     that invites the wrong reading. The per-player "Now" column in the roll below carries the same
     numbers where they read as one man's career rather than as a rate. */
  function priceOf(lo, hi) {
    return core.priceRange((MD.seam.working && MD.seam.working.pvc) || null, lo, hi);
  }

  function pct(a, b) { return b ? (100 * a / b).toFixed(0) + "%" : "—"; }
  function num(v, dp) { return v == null ? "—" : (dp ? v.toFixed(dp) : Math.round(v)); }

  // ---------------------------------------------------------------- controls
  function seg(label, opts, current, onPick) {
    var wrap = fmt.el("div", "ddseg");
    wrap.appendChild(fmt.el("span", "lbl", label));
    var box = fmt.el("div", "seg");
    opts.forEach(function (o) {
      var b = fmt.el("button", o[0] === current ? "on" : "", o[1]);
      b.addEventListener("click", function () { onPick(o[0]); });
      box.appendChild(b);
    });
    wrap.appendChild(box);
    return wrap;
  }

  /* EVERY CONTROL IN THIS BAR CHANGES THE BOARD. That is the whole rule, and it was broken: the
     pick selector and the "Drafted as" filter sat here, looking exactly like the two that do, and
     changed nothing above the fold — the position filter only ever cut the detail table hundreds of
     pixels below. On draft day you would click RUCK, watch the grid not move, and stop trusting the
     page. They now live WITH the detail panel they drive, and this bar holds only what it says it
     holds. */
  function controls(container) {
    var bar = fmt.el("div", "strip ddstrip");

    /* THE NEIGHBOURHOOD IS ONE CONTROL FOR THE WHOLE PAGE. A single ordinal carries at most one
       career per class, so every cell on the board pools a window around its pick — and the width
       of that window is the single biggest lever on how noisy the grid looks. It is a control the
       owner turns, not a constant buried in the code, and every cell reports the n it landed on. */
    bar.appendChild(seg("Pool",
      [[4, "±4"], [8, "±8"], [12, "±12"]], state.half,
      function (v) { state.half = v; renderAll(); }));

    /* THREE POPULATIONS, THREE QUESTIONS, AND THE DEFAULT IS THE STRICT ONE.

       FULLY RUN — classes with enough seasons for their PEAKS to have landed. The threshold is
         derived here from the record's own first-star lags (see core.developedFromRows); on this
         store it is 11 seasons, at which 91% of first-star seasons have arrived.
       SETTLED — the bundle's debut threshold, 4 seasons, at which 99% of eventual DEBUTS have
         happened. Right for "did he ever play", wrong for "was he any good": measured, star rate
         reads 15.3% on this population against 17.0% on a fully-run one, and the error is worst
         exactly where the board is most used — picks 41-64 read 7.4% against 9.7%, a third
         understated, because late picks develop slowly. It also flips the headline: rucks lead
         midfielders on star rate at four seasons, midfielders lead at twelve.
       EVERY CLASS — everything, including this year's teenagers.

       THE DEFAULT IS FULLY RUN, and it is a trade rather than a free win: it costs 44% of the
       sample (840 selections against 1,509 from 2004 on) and confines the evidence to the classes
       of 2004-2015. What it does NOT cost is comparability across eras — SuperCoach assigns a fixed
       3,300 points a match, so a 2006 average and a 2024 average are the same unit by construction
       and no era normalisation is applied anywhere in this model. The trade is taken because a
       board that systematically understates late picks is actively misleading on the trade-down
       decision, while a thinner board is merely less certain — and thinness is marked on every cell
       it affects, where bias is invisible. Both other populations are one click away and the page
       says what each costs. */
    var dev = developedThreshold();
    bar.appendChild(seg("Classes",
      [[dev.lag, "fully run"], [stamp().maturitySeasons || 4, "settled"], [0, "every class"]],
      state.minSeasons,
      function (v) { state.minSeasons = v; renderAll(); }));

    /* THE POPULATION ON SCREEN, NAMED. Which classes are in, how many selections that is, and what
       the threshold rests on — because "fully run" is a word and the reader is entitled to the
       number behind it. */
    var inSet = rows().filter(inWindow);
    var note = fmt.el("span", "ddpop");
    var newest = stamp().seasonNow - state.minSeasons;
    note.innerHTML = fmt.n(inSet.length) + " selections" +
      (state.minSeasons ? ", classes " + YR_LO + "–" + newest : ", classes from " + YR_LO) +
      (state.minSeasons === dev.lag && !dev.fallback
        ? ' <span class="why">— ' + dev.lag + " seasons, where " + Math.round(dev.cum * 100) +
          "% of first-star seasons have landed</span>"
        : state.minSeasons === (stamp().maturitySeasons || 4)
          ? ' <span class="why warn">— the DEBUT threshold: peaks have not landed, late picks read low</span>'
          : state.minSeasons === 0
            ? ' <span class="why warn">— includes classes still running; their peaks are ahead of them</span>'
            : "");
    bar.appendChild(note);

    container.appendChild(bar);
  }

  // =============================================== THE BOARD (positions x picks, one currency) ===
  /* Every cell reads "mid N" — the midfielder pick this position at this pick is worth — with the
     expected value over replacement and the startable share beneath it. One currency across the
     whole grid is what turns six separate outcome tables into a decision you can take at the clock.

     THE TIERS ARE DERIVED FROM THE YARDSTICK ITSELF, not from the raw figures: a cell is elite when
     it is worth a top-5 midfielder, strong at a first-rounder, useful mid-board, filler past that.
     A STEAL is the one tier that is not about level at all — it is about the GAP between what the
     cell is worth and what the pick costs you. A ruck at pick 30 worth a top-10 midfielder is the
     same quality as a mid-teens pick and costs a thirty. That gap is the edge, and it is the only
     thing on this page that tells you to do something rather than telling you what happened. */
  var TIERS = [
    { key: "elite",  label: "Elite — top of your board",   at: 5 },
    { key: "strong", label: "Strong — first-round keeper",  at: 15 },
    { key: "useful", label: "Useful — mid-board",           at: 30 },
    { key: "filler", label: "Filler — late / punt",         at: 999 },
  ];
  function tierOf(equivPick) {
    for (var i = 0; i < TIERS.length; i++) if (equivPick <= TIERS[i].at) return TIERS[i].key;
    return "filler";
  }
  /* A steal needs the cell to be worth MATERIALLY more than the pick costs, and needs enough
     careers behind it to mean anything — a thin cell drifting high is noise, not an edge. */
  var STEAL_RATIO = 0.6, STEAL_FROM_PICK = 10;
  function isSteal(equivPick, pick, n) {
    return n > THIN_MAX && pick >= STEAL_FROM_PICK && equivPick <= pick * STEAL_RATIO;
  }

  function boardCell(pos, pick, curve) {
    /* careers() takes the OUTCOME RECORD's stamp (it needs seasonNow / maturitySeasons to decide
       which classes have settled); frame() takes the BOARD (it needs the baked REPL bar). Two
       different objects for two different jobs, and getting them the wrong way round is silent —
       careers returns nothing and every cell reads n=0, which is exactly what happened here. */
    var set = core.careers(rows(), stamp(), pos, pick, state.half, state.minSeasons, YR_LO);
    var f = core.frame(set, board(), pos);
    if (!f) return { empty: true, n: set.length };
    var eq = core.midEquivalent(curve, f.vor);
    if (!eq) return { empty: true, n: f.n };
    return { n: f.n, vor: f.vor, startable: f.startable, star: f.star, bust: f.bust,
             starBar: f.starBar, repl: f.repl,
             equiv: eq.p, beyond: eq.beyond, thin: f.n <= THIN_MAX,
             tier: tierOf(eq.p), steal: isSteal(eq.p, pick, f.n) };
  }

  function boardSection(page, curve) {
    var wrap = fmt.el("div", "ddboard");
    var head = fmt.el("div", "ddbhead");
    /* THE HEADER NAMES THE BAR, because a "value over replacement" figure means nothing until the
       reader knows whose replacement level it is. It is the model's own — rl_model REPL, baked and
       unchanged for months — and each position is measured against its own, which is why a key
       forward and a midfielder can be compared at all. */
    var bars = POS_ORDER.map(function (p) {
      var v = core.replOf(board(), p);
      return v == null ? null : POS_SHORT[p] + " " + v.toFixed(1);
    }).filter(Boolean).join(" · ");
    head.innerHTML = '<h2>The full board</h2><p>Each cell is <b>the midfielder pick it is worth</b>' +
      ' — then <b>expected value over the bar</b>, the share who ever <b>clear</b> it, and the ' +
      'share who produce a <b>star season</b>. The value already carries how great: a 110 ' +
      'midfielder over a 77 bar is worth six times an 85 one. The two rates carry what an average ' +
      'hides — how often a pick returns nothing, and how often it returns someone great. ' +
      '<span class="thin">●</span> marks a thin sample; hover a cell for its bust rate.</p>' +
      (bars ? '<p class="bars">Bars: ' + bars +
        (core.replBarIsEffective(board())
          ? '  <span class="drop">— the literal REPL less the ' + board().REPL_DROP +
            '-point drop the pricing core applies (RL_REPL_DROP)</span>'
          : '  <span class="drop warn">— the RAW literal. This bundle publishes no REPL_BAR, so the ' +
            'drop the pricing core applies is NOT reflected and every figure below sits above the ' +
            'real bar.</span>') + '</p>' : "");
    wrap.appendChild(head);

    var tbl = fmt.el("table", "ddgrid");
    var thead = fmt.el("thead");
    var hr = fmt.el("tr");
    hr.appendChild(fmt.el("th", "corner", ""));
    BOARD_PICKS.forEach(function (p) {
      var th = fmt.el("th", "", "Pick " + p);
      th.addEventListener("click", function () { state.pick = p; renderAll(); });
      th.title = "Show the careers behind pick " + p + " below.";
      hr.appendChild(th);
    });
    thead.appendChild(hr);
    tbl.appendChild(thead);

    var tb = fmt.el("tbody");
    POS_ORDER.forEach(function (pos) {
      var tr = fmt.el("tr");
      var repl = core.replOf(stamp(), pos);
      var rh = fmt.el("th", "rowh");
      rh.innerHTML = "<b>" + fmt.esc(POS_LABEL[pos]) + "</b>" +
        (repl == null ? "" : '<span>repl ' + repl.toFixed(0) + "</span>");
      rh.title = "Replacement level " + (repl == null ? "unavailable" : repl.toFixed(1)) +
        " — the last man holding a starting slot at this position across the league.";
      tr.appendChild(rh);
      BOARD_PICKS.forEach(function (p) {
        var c = boardCell(pos, p, curve);
        var td = fmt.el("td", "ddcell " + (c.empty ? "empty" : c.tier + (c.steal ? " steal" : "")));
        if (c.empty) {
          td.innerHTML = '<span class="none">n=' + c.n + "</span>";
          td.title = "Too few careers at " + POS_LABEL[pos] + " near pick " + p +
            " to read anything — nothing is interpolated in its place.";
        } else {
          td.innerHTML = '<span class="eq">' + (c.beyond === "above" ? "&gt;" : c.beyond === "below" ? "&lt;" : "") +
            "mid " + c.equiv + (c.thin ? ' <span class="thin">●</span>' : "") + "</span>" +
            /* THREE NUMBERS, THREE QUESTIONS. The VOR is the magnitude and already carries
               "great" continuously — a 110 mid over a 77 bar is worth six times an 85 one. What a
               mean cannot tell you is the SHAPE, so the two rates sit beside it: how often this
               cell clears the bar at all, and how often it produces a star. +12 could be one star
               and four failures or five useful players, and on draft day those are opposite
               propositions. */
            '<span class="sub">' + c.vor.toFixed(1) + " · " + Math.round(c.startable * 100) + "%" +
              (c.star == null ? "" : ' · <b class="st">' + Math.round(c.star * 100) + "%</b>") +
            "</span>";
          td.title = POS_LABEL[pos] + " at pick " + p + ": worth a midfielder at pick " + c.equiv +
            ". Expected value over replacement " + c.vor.toFixed(1) +
            " (bar " + c.repl.toFixed(1) + "); " +
            Math.round(c.startable * 100) + "% ever clear it" +
            (c.star == null ? "" : ", " + Math.round(c.star * 100) + "% produce a STAR season (" +
              c.starBar + "+)") +
            ", " + Math.round(c.bust * 100) + "% never played a measurable season. " +
            c.n + " careers" +
            (c.thin ? " — a thin sample." : ".") +
            (c.steal ? " STEAL: worth far more than the pick costs." : "");
          td.addEventListener("click", function () {
            state.pick = p; state.pos = pos; state.view = "board"; renderAll();
          });
        }
        tr.appendChild(td);
      });
      tb.appendChild(tr);
    });
    tbl.appendChild(tb);
    var scroll = fmt.el("div", "tablewrap");
    scroll.appendChild(tbl);
    wrap.appendChild(scroll);

    var leg = fmt.el("div", "ddlegend");
    leg.innerHTML = TIERS.map(function (t) {
      return '<span class="lg ' + t.key + '"><i></i>' + fmt.esc(t.label) + "</span>";
    }).join("") + '<span class="lg steal"><i></i>Scarcity steal — worth far more than the pick costs</span>';
    wrap.appendChild(leg);
    page.appendChild(wrap);
  }

  // =========================================================== THE COMPARATOR (A against B) ======
  /* Two hypotheticals, side by side, in the midfield currency, with a verdict that names the pick
     at which they break even. This is the question actually asked on the clock — "this key forward
     here, or a key defender?" — and the currency is what lets two different positions be compared
     at all. */
  function sideCard(which) {
    var side = state[which];
    var curve = core.midCurve(rows(), stamp(), board(), state.half, state.minSeasons, YR_LO);
    var f = core.frame(core.careers(rows(), stamp(), side.pos, side.pick, state.half, state.minSeasons, YR_LO),
                       board(), side.pos);
    var el = fmt.el("div", "ddside");
    var h = '<div class="k">Option ' + which.toUpperCase() + "</div>" +
            '<div class="lbl">Position the AFL drafted him as</div><div class="posgrid">';
    POS_ORDER.forEach(function (p) {
      h += '<button data-pos="' + p + '" class="' + (p === side.pos ? "on" : "") + '">' +
           fmt.esc(POS_SHORT[p]) + "</button>";
    });
    h += "</div>" +
      '<div class="lbl">Real national-draft pick</div>' +
      '<div class="pickrow2"><span class="num pk">' + side.pick + "</span>" +
      '<input type="range" min="1" max="64" value="' + side.pick + '"></div>';
    if (!f) {
      h += '<div class="verdictline none">No settled careers at ' + fmt.esc(POS_LABEL[side.pos]) +
           " near pick " + side.pick + " — nothing is estimated in its place.</div>";
    } else {
      var eq = core.midEquivalent(curve, f.vor);
      h += '<div class="tierchip ' + tierOf(eq.p) + '">' +
           fmt.esc(TIERS.filter(function (t) { return t.key === tierOf(eq.p); })[0].label.split(" —")[0]) +
           "</div>" +
           '<div class="lbl">' + fmt.esc(POS_LABEL[side.pos]) + " at pick " + side.pick + "</div>" +
           '<div class="worth">worth <b>a midfielder at pick ' + eq.p + "</b></div>" +
           '<div class="trio"><span><i>exp. VOR</i>' + f.vor.toFixed(1) + "</span>" +
           "<span><i>clears bar</i>" + Math.round(f.startable * 100) + "%</span>" +
           (f.star == null ? "" :
             "<span><i>star " + f.starBar + "+</i>" + Math.round(f.star * 100) + "%</span>") +
           "<span><i>bust</i>" + Math.round(f.bust * 100) + "%</span>" +
           '<span><i>careers</i>' + f.n + (f.n <= THIN_MAX ? " ●" : "") + "</span></div>";
    }
    el.innerHTML = h;
    el.querySelectorAll(".posgrid button").forEach(function (b) {
      b.addEventListener("click", function () { side.pos = b.getAttribute("data-pos"); renderAll(); });
    });
    var rng = el.querySelector("input[type=range]");
    if (rng) rng.addEventListener("input", function () { side.pick = parseInt(rng.value, 10); renderAll(); });
    return el;
  }

  /* THE VERDICT: at what pick does B match A? Not a winner declaration — a break-even, because the
     two options are almost never far apart and the honest answer is where the line sits. */
  function verdict() {
    var curve = core.midCurve(rows(), stamp(), board(), state.half, state.minSeasons, YR_LO);
    var fa = core.frame(core.careers(rows(), stamp(), state.a.pos, state.a.pick, state.half, state.minSeasons, YR_LO), board(), state.a.pos);
    var fb = core.frame(core.careers(rows(), stamp(), state.b.pos, state.b.pick, state.half, state.minSeasons, YR_LO), board(), state.b.pos);
    var el = fmt.el("div", "ddverdict");
    if (!fa || !fb) {
      el.innerHTML = "<b>No verdict.</b> One side has no settled careers to read, and a comparison " +
        "against nothing is not a comparison.";
      return el;
    }
    /* Walk B's own position down the ordinals for the pick whose value matches A. That is the
       sentence worth printing: "a key forward at 5 is worth a key defender at 7." */
    var bestP = null, bestD = null;
    for (var p = 1; p <= 64; p++) {
      var f = core.frame(core.careers(rows(), stamp(), state.b.pos, p, state.half, state.minSeasons, YR_LO), board(), state.b.pos);
      if (!f) continue;
      var d = Math.abs(f.vor - fa.vor);
      if (bestD === null || d < bestD) { bestD = d; bestP = p; }
    }
    var ea = core.midEquivalent(curve, fa.vor), eb = core.midEquivalent(curve, fb.vor);
    /* THE GAP IS TAKEN OFF THE FIGURES ON SCREEN, not off the full-precision ones behind them. The
       two cards print VOR to one decimal; subtracting the unrounded values gave 1.5 under a pair
       reading 16.3 and 14.7, which is a page doing arithmetic the reader can see is wrong. Round
       first, then subtract — the visible numbers are the ones that have to add up. */
    var va = Math.round(fa.vor * 10) / 10, vb = Math.round(fb.vor * 10) / 10;
    var gap = vb - va;
    var near = Math.abs(gap) < 1.0;
    el.innerHTML = "<div class=\"k\">Verdict</div>" +
      "<div class=\"say\">A <b>" + fmt.esc(POS_LABEL[state.a.pos].toLowerCase()) + " at pick " +
      state.a.pick + "</b> is worth a <b>" + fmt.esc(POS_LABEL[state.b.pos].toLowerCase()) +
      " at pick " + (bestP == null ? "—" : bestP) + "</b>.</div>" +
      "<div class=\"why\">" +
      (near
        ? "<b>Line ball.</b> Your " + fmt.esc(POS_LABEL[state.b.pos].toLowerCase()) + " at pick " +
          state.b.pick + " is right around that break-even — split it on roster need, development " +
          "timing and floor (lean higher-floor if you are contending)."
        : "<b>" + (gap > 0 ? "Option B" : "Option A") + " is ahead</b> by " + Math.abs(gap).toFixed(1) +
          " of expected value over replacement at the picks you have set.") +
      "</div>" +
      "<div class=\"yard\">Against the midfield yardstick — A ≈ mid " + (ea ? ea.p : "—") +
      " · B ≈ mid " + (eb ? eb.p : "—") + "</div>";
    return el;
  }

  function comparatorSection(page) {
    var wrap = fmt.el("div", "ddcompare");
    var h = fmt.el("div", "ddbhead");
    h.innerHTML = "<h2>This or that</h2><p>Two options in one currency, with the pick at which they " +
      "break even.</p>";
    wrap.appendChild(h);
    var pair = fmt.el("div", "ddpair");
    pair.appendChild(sideCard("a"));
    pair.appendChild(sideCard("b"));
    wrap.appendChild(pair);
    wrap.appendChild(verdict());
    page.appendChild(wrap);
  }

  // ================================================== THE FINDINGS (derived, never written) =====
  /* EVERY SENTENCE BELOW IS COMPUTED FROM THE BOARD ABOVE, ON EVERY LOAD. None is a paragraph
     somebody typed once and left to go stale — which is the failure mode of every "insights" panel
     ever shipped. If the data changes, these change; if a finding stops being true, it stops being
     printed rather than sitting there being wrong.

     Each one carries the figures it rests on, so it can be checked against the grid rather than
     believed. */

  /* THE CLIFF IS THE LAST CROSSING, NOT THE FIRST. A first-dip definition looked right and was
     wrong the moment it met a noisy row: ruck dips under a coin-flip at pick 15, climbs back to 55%
     at pick 30, and the card printed "ruck ~16" beside a steal card recommending a ruck at 40. Both
     were computed correctly and together they were nonsense.
     A cliff is a place you do not come back from, so this walks BACKWARDS and returns the pick from
     which the position never again clears the bar. A row that stays above it all the way has no
     cliff and says nothing rather than inventing one at 64. */
  function startableCliff(pos) {
    var cliff = null;
    for (var p = 64; p >= 1; p--) {
      var f = core.frame(core.careers(rows(), stamp(), pos, p, state.half, state.minSeasons, YR_LO), board(), pos);
      if (!f || f.n <= THIN_MAX) continue;
      if (f.startable < 0.5) cliff = p; else break;
    }
    return cliff;
  }

  /* the biggest gap between what a cell is worth and what the pick costs — the single best steal. */
  function bestSteal(curve) {
    var best = null;
    POS_ORDER.forEach(function (pos) {
      for (var p = 8; p <= 58; p++) {
        var f = core.frame(core.careers(rows(), stamp(), pos, p, state.half, state.minSeasons, YR_LO), board(), pos);
        if (!f || f.n <= THIN_MAX) continue;
        var eq = core.midEquivalent(curve, f.vor);
        if (!eq) continue;
        var gain = p - eq.p;
        if (best === null || gain > best.gain) best = { pos: pos, pick: p, equiv: eq.p, gain: gain, n: f.n };
      }
    });
    return best;
  }

  /* WHICH POSITIONS CLEAR THEIR OWN BAR, over the whole settled population.

     This replaced a "star conversion" card that measured against a bar this page had no business
     owning. Each position is now measured against ITS OWN BAKED REPLACEMENT BAR — MID 80.1, KPF
     66.8, and so on — so the reading is not "who scores most" but "who, relative to what the model
     demands of that position, actually delivers". That is the comparison the draft presents,
     because the pick costs the same whoever you take with it. */
  function clearRates() {
    var out = [];
    POS_ORDER.forEach(function (pos) {
      var set = (rows() || []).filter(function (r) {
        return r.dp === pos && r.p <= 64 && inWindow(r);
      });
      var f = core.frame(set, board(), pos);
      if (f && f.n) out.push({ pos: pos, startable: f.startable, n: f.n, repl: f.repl,
                               star: f.star, starBar: f.starBar, bust: f.bust });
    });
    return out.sort(function (a, b) { return b.startable - a.startable; });
  }

  /* A DEPTH CLAIM NEEDS MORE THAN A CELL. THIN_MAX is the right bar for marking one cell with a dot;
     it is far too permissive for a sentence like "you can wait on this position until pick 58",
     which is a claim about a whole tail. The first cut used it and said RUCK holds to pick 64 — off
     15 careers in a window whose neighbour, two picks earlier and on a different 19, read as worth
     LESS than a pick-64 midfielder. One good late ruck was carrying the entire finding.

     So a depth claim requires a real sample AND a RUN: the position must clear the bar at three
     consecutive ordinals, so a single lucky window cannot produce a recommendation. */
  var DEPTH_MIN_N = 25, DEPTH_RUN = 3;
  function holdsUntil(pos, midBar, curve) {
    var last = null, run = 0;
    for (var p = 1; p <= 64; p++) {
      var f = core.frame(core.careers(rows(), stamp(), pos, p, state.half, state.minSeasons, YR_LO), board(), pos);
      var eq = f ? core.midEquivalent(curve, f.vor) : null;
      // A cell off the bottom of the yardstick is not "worth a mid 64" — it is worth less than the
      // ruler can express, and counting it would let a worthless row claim depth it does not have.
      var holds = !!(f && f.n >= DEPTH_MIN_N && eq && !eq.beyond && eq.p <= midBar);
      run = holds ? run + 1 : 0;
      if (run >= DEPTH_RUN) last = p;
    }
    return last;
  }

  function findingsSection(page, curve) {
    var wrap = fmt.el("div", "ddfindings");
    var h = fmt.el("div", "ddbhead");
    h.innerHTML = "<h2>What the board says</h2><p>Every line here is computed from the grid above on " +
      "this load — none is a paragraph anybody typed. A finding that stops being true stops being " +
      "printed.</p>";
    wrap.appendChild(h);

    var cards = fmt.el("div", "ddcards");
    function card(title, html, cls) {
      var c = fmt.el("div", "ddcard " + (cls || ""));
      c.innerHTML = "<h3>" + title + "</h3><p>" + html + "</p>";
      cards.appendChild(c);
    }

    // 1. the single best steal on the board
    var st = bestSteal(curve);
    if (st && st.gain > 4) {
      card("The steal", "A <b>" + fmt.esc(POS_LABEL[st.pos].toLowerCase()) + "</b> at <b>pick " +
        st.pick + "</b> is worth a midfielder at <b>pick " + st.equiv + "</b> — " + st.gain +
        " ordinals of value the pick does not cost you, and the widest such gap anywhere on the " +
        "board (" + st.n + " careers).", "steal");
    }

    // 2. the shape a mean hides: floor, ceiling and failure, side by side
    /* The three are deliberately reported TOGETHER, because separately each one misleads. Key
       defenders clear their bar more often than anyone and star least — a high floor and no
       ceiling. Midfielders clear it about as often and star at twice the rate. Reading either
       column alone would recommend the wrong position. */
    var cr = clearRates();
    if (cr.length >= 3) {
      var byStar = cr.slice().sort(function (a, b) { return (b.star || 0) - (a.star || 0); });
      var byFloor = cr.slice().sort(function (a, b) { return b.startable - a.startable; });
      var byBust = cr.slice().sort(function (a, b) { return a.bust - b.bust; });
      var say = "";
      if (byStar[0].star != null) {
        say += "<b>Ceiling:</b> " + byStar.slice(0, 2).map(function (x) {
          return fmt.esc(POS_LABEL[x.pos].toLowerCase()) + "s <b>" + Math.round(x.star * 100) +
                 "%</b> produce a star season (" + x.starBar + "+)"; }).join(", ") +
          " against " + fmt.esc(POS_LABEL[byStar[byStar.length - 1].pos].toLowerCase()) + "s " +
          Math.round(byStar[byStar.length - 1].star * 100) + "%. ";
      }
      say += "<b>Floor:</b> " + fmt.esc(POS_LABEL[byFloor[0].pos].toLowerCase()) + "s clear their " +
        "bar most often (" + Math.round(byFloor[0].startable * 100) + "%). " +
        "<b>Failure:</b> " + fmt.esc(POS_LABEL[byBust[0].pos].toLowerCase()) + "s bust least (" +
        Math.round(byBust[0].bust * 100) + "% never played a measurable season) and " +
        fmt.esc(POS_LABEL[byBust[byBust.length - 1].pos].toLowerCase()) + "s most (" +
        Math.round(byBust[byBust.length - 1].bust * 100) + "%). " +
        "Each is measured against its OWN bars, and a position can lead one column and trail another " +
        "— which is the whole reason all three are here.";
      card("Floor, ceiling and failure", say, "star");
    }

    // 3. the startable cliff, per position, ordered
    var cliffs = POS_ORDER.map(function (p) { return { pos: p, at: startableCliff(p) }; })
                          .filter(function (c) { return c.at != null; })
                          .sort(function (a, b) { return a.at - b.at; });
    if (cliffs.length >= 3) {
      card("Mind the startable cliff",
        "The pick where a position drops below a coin-flip to produce even a starter: " +
        cliffs.map(function (c) { return fmt.esc(POS_LABEL[c.pos].toLowerCase()) + " <b>~" + c.at + "</b>"; })
              .join(", ") + ". Take the early ones <b>early or not at all</b>; you can comfortably " +
        "<b>wait</b> on the late ones.");
    }

    // 4. how deep the midfield holds
    var midHold = holdsUntil("MID", 20, curve);
    if (midHold) {
      card("Ride mids deep",
        "A midfielder is still worth a top-20 midfielder's return as deep as <b>pick " + midHold +
        "</b>. They hold value longest and own the stars — which is why the yardstick is a " +
        "midfielder and not a dollar.");
    }

    // 5. tall vs small forward, decided by the data rather than asserted
    var cross = null;
    for (var p = 1; p <= 64; p++) {
      var fs = core.frame(core.careers(rows(), stamp(), "SF", p, state.half, state.minSeasons, YR_LO), board(), "SF");
      var fk = core.frame(core.careers(rows(), stamp(), "KPF", p, state.half, state.minSeasons, YR_LO), board(), "KPF");
      if (!fs || !fk || fs.n <= THIN_MAX || fk.n <= THIN_MAX) continue;
      if (fs.vor > fk.vor) cross = p;
    }
    if (cross) {
      /* "down to ~64" is a silly way to say "everywhere", and the first cut printed exactly that.
         When the crossing runs to the end of the curve the finding is stronger, not weaker, and it
         should read that way. */
      card("Take the small forward over the tall",
        "A small or general forward out-returns a key forward " +
        (cross >= 58 ? "<b>at every pick on the board</b>" : "at every pick down to <b>~" + cross + "</b>") +
        ". Same shape of upside, fewer busts, and it costs you less to find out.");
    }

    // 6. where you can punt — EVERY position that holds, not one fragile winner
    /* Named as a set rather than a single deepest position on purpose: the top two are usually
       within a few ordinals of each other, and picking one by a margin the sample cannot support
       would turn a robust finding into a coin toss dressed as advice. */
    var deep = POS_ORDER.map(function (pos) { return { pos: pos, at: holdsUntil(pos, 40, curve) }; })
                        .filter(function (d) { return d.at && d.at >= 45; })
                        .sort(function (a, b) { return b.at - a.at; });
    if (deep.length) {
      card("Where you can punt",
        deep.map(function (d) {
          return "<b>" + fmt.esc(POS_LABEL[d.pos].toLowerCase()) + "</b> to <b>pick " + d.at + "</b>";
        }).join(", ") + " — still worth a top-40 midfielder that deep. These are the positions you " +
        "can leave until late without losing much, so spend your early picks elsewhere.");
    }

    wrap.appendChild(cards);
    page.appendChild(wrap);
  }

  // ---------------------------------------------------------------- the panels
  function statPanel(rs, sel) {
    var panel = fmt.el("div", "ddstats");
    var thin = rs.n <= THIN_MAX;

    function cell(k, v, sub, cls) {
      var d = fmt.el("div", "ddstat" + (cls ? " " + cls : ""));
      d.innerHTML = '<div class="k">' + k + "</div>" +
                    '<div class="v num">' + v + "</div>" +
                    (sub ? '<div class="s">' + sub + "</div>" : "");
      return d;
    }

    panel.appendChild(cell("Careers in this set", fmt.n(rs.n) + (thin ? ' <span class="thin" title="' +
      THIN_MAX + ' careers or fewer — read this set as an indication, not a rate.">●</span>' : ""),
      sel.lo === sel.hi ? ("pick " + sel.lo) : ("picks " + sel.lo + "–" + sel.hi)));
    panel.appendChild(cell("Never played", pct(rs.never, rs.n), fmt.n(rs.never) + " of " + fmt.n(rs.n),
      rs.never ? "bad" : ""));
    panel.appendChild(cell("Reached 100 games", pct(rs.g100, rs.n), fmt.n(rs.g100) + " of " + fmt.n(rs.n)));
    panel.appendChild(cell("Median career", num(rs.gamesMed) + " <small>games</small>",
      "quartiles " + num(rs.gamesQ1) + "–" + num(rs.gamesQ3)));
    panel.appendChild(cell("Median best season", num(rs.peakMed, 1),
      rs.nPeak ? ("quartiles " + num(rs.peakQ1, 1) + "–" + num(rs.peakQ3, 1) +
                  " · " + fmt.n(rs.nPeak) + " reached one") : "none reached one"));
    var pr = priceOf(sel.lo, sel.hi);
    panel.appendChild(cell("Priced at",
      pr == null ? "—" : (pr.lo === pr.hi ? fmt.n(pr.lo) : fmt.n(pr.lo) + "–" + fmt.n(pr.hi)),
      pr == null ? "the board publishes no pick-value curve"
                 : (sel.lo === sel.hi ? "the adopted curve, this pick"
                                      : "the adopted curve across these " + pr.n + " picks"),
      "price"));
    return panel;
  }

  /* The honesty block. Three separate statements, each of which a reader would otherwise have to
     take on trust: what population these rates came from, what was excluded and why, and what the
     one survivorship-shaped figure above actually covers. */
  function notes(rs, sel) {
    var st = stamp();
    var el = fmt.el("div", "note");
    var parts = [];
    parts.push("<b>Complete draft classes, not a list of players who made it.</b> The record holds " +
      fmt.n(st.nRows) + " national-draft selections across " + st.nClasses + " classes (" +
      st.classFrom + "–" + st.classTo + "), of which <b>" + fmt.n(st.nNeverPlayed) + "</b> (" +
      pct(st.nNeverPlayed, st.nRows) + ") never played a senior game. Busts are in the population, " +
      "which is the only basis on which the rates above mean anything.");

    /* THE OWNER'S EXCLUSION, ON THE PAGE'S OWN FACE. Two men were struck out of the record by a
       ruling, and a board that silently omits two pick-1 selections while claiming to hold every one
       of them is lying by omission — the more so because they are the two whose absence most flatters
       the number above. So it is named, with who and from where. */
    var bx = st.bustExcluded || [];
    if (bx.length) {
      parts.push("<b>" + bx.map(function (e) { return e.name; }).join(" and ") + " are struck out " +
        "of this record by owner ruling</b> — " +
        bx.map(function (e) { return e.year + " pick " + e.pick; }).join(" and ") +
        ", careers ended by force majeure rather than by failing. They are not zeroed or flagged: " +
        "they did not happen, and the " + fmt.n(st.bustSlid) + " selections behind them slid up one " +
        "to close the holes, so no ordinal lost an observation. The pick curve that sets the prices " +
        "struck out the same two men and slid the same " + fmt.n(st.bustSlid) + " — checked row for " +
        "row — so this page and the Pick value tab agree about who was picked where. It flatters " +
        "the top of the key-forward column and nothing else.");
    }

    /* THE CLASS FLOOR, NAMED SEPARATELY FROM THE YOUNG END. The 2003 class is not held out for
       being unsettled — it is held out because its first season is unobservable: the store carries
       zero 2004 seasons for it, so every 2003 man's year one is missing rather than bad. The
       house's own pick-value harness sets the same floor (YR_LO = 2004). */
    var nFloor = (rows() || []).filter(function (r) {
      return r.y < YR_LO && r.p >= sel.lo && r.p <= sel.hi && (!state.pos || r.dp === state.pos);
    }).length;
    if (nFloor) {
      parts.push("<b>The " + (YR_LO - 1) + " class is out of every figure above</b> (" +
        fmt.n(nFloor) + " selection" + (nFloor === 1 ? "" : "s") + " in this window) — the record " +
        "holds no " + YR_LO + " seasons for it, so its year one cannot be observed rather than " +
        "merely being poor. The pick-value harness draws the same line.");
    }

    if (sel.young.length) {
      var debuted = sel.young.filter(function (r) { return r.g > 0; }).length;
      var devT = developedThreshold();
      var onDev = (state.minSeasons === devT.lag && !devT.fallback);
      parts.push("<b>" + fmt.n(sel.young.length) + " selection" + (sel.young.length === 1 ? "" : "s") +
        " from classes still running are excluded</b> from every figure above — " +
        fmt.n(debuted) + " of them " + (debuted === 1 ? "has" : "have") + " already debuted. A class " +
        "counts once it has had <b>" + state.minSeasons + " completed seasons</b>, and that line " +
        "is measured rather than chosen: " + (onDev
          ? Math.round(devT.cum * 100) + "% of first-star seasons in fully-run classes have landed " +
            "by then, which is the question this board asks"
          : pct(Math.round(1000 * (((st.debutLagTable || []).filter(function (t) {
              return t.lag === state.minSeasons; })[0] || {}).cum || 0)) / 10, 100) +
            " of the " + fmt.n(st.debutLagN) + " eventual debutants in the settled classes had " +
            "debuted by then — a DEBUT line, which settles years before a peak does") +
        ". Switch to <b>every class</b> to fold them in.");
    } else if (!state.minSeasons) {
      parts.push("<b>Every class is in, including the ones still running.</b> A player from a recent " +
        "class who has not debuted is counted here as never having played, which is true today and " +
        "may not be true in two years. Switch to <b>settled only</b> for rates that are not " +
        "depressed by youth.");
    }
    parts.push("<b>The price is a price and the rest are outcomes</b> — “Priced at” is what the " +
      "adopted curve pays for this pick today, not what these careers returned. In the roll below, " +
      "<b>Now</b> is a live board value and only " + fmt.n(rs.nLive) + " of " + fmt.n(rs.n) +
      " are still tracked to carry one; read it as one man's career, never as a rate for the pick.");
    parts.push("<b>Best season</b> means a season of " + st.realSeasonGames + " games or more; " +
      "a five-match cameo is not a career peak. There is no “hit” line on this page: a " +
      "threshold is a ruling, so the spread is shown and you draw your own.");
    el.innerHTML = parts.join(" ");
    return el;
  }

  function roll(set) {
    var byKey = ((MD.seam && MD.seam.indexed) ? MD.seam.indexed().byKey : {}) || {};
    var sorted = set.slice().sort(function (a, b) { return (b.g - a.g) || (a.y - b.y); });
    var body = "";
    sorted.forEach(function (r) {
      var p = byKey[r.k];
      var live = p ? fmt.n(MD.dispVal ? MD.dispVal(p) : p.v) : "—";
      body += "<tr" + (r.g === 0 ? ' class="never"' : "") + ">" +
        "<td>" + fmt.esc(r.n) + "</td>" +
        '<td class="num">' + r.y + "</td>" +
        '<td class="num">#' + r.p + "</td>" +
        "<td>" + fmt.esc(r.dp || "—") + "</td>" +
        "<td>" + fmt.esc(r.c || "—") + "</td>" +
        '<td class="num">' + fmt.n(r.g) + "</td>" +
        '<td class="num">' + (r.dl == null ? '<span class="never">never</span>' : "+" + r.dl) + "</td>" +
        '<td class="num">' + (r.pk == null ? "—" : r.pk.toFixed(1)) + "</td>" +
        '<td class="num">' + live + "</td>" +
      "</tr>";
    });
    var wrap = fmt.el("div", "tablewrap");
    wrap.innerHTML = '<table class="ctable ddroll"><thead><tr>' +
      "<th>Player</th><th class=\"num\">Class</th><th class=\"num\">Pick</th><th>Drafted as</th>" +
      "<th>AFL club</th><th class=\"num\">Games</th><th class=\"num\" title=\"Seasons after the draft " +
      "before he first played.\">Debut</th><th class=\"num\" title=\"Best average in a season of " +
      (stamp().realSeasonGames || 10) + " games or more.\">Best season</th>" +
      "<th class=\"num\" title=\"His value on today's board, if he is still tracked.\">Now</th>" +
      "</tr></thead><tbody>" + body + "</tbody></table>";
    return wrap;
  }

  /* the detail panel's own controls, rendered WITH it so their scope is obvious from where they are */
  function detailControls(container) {
    var bar = fmt.el("div", "strip ddstrip dddetail");
    var ords = ordinals();
    bar.appendChild(fmt.el("span", "lbl", "Pick"));
    var sel = document.createElement("select");
    sel.className = "boardsel";
    sel.innerHTML = ords.map(function (n) {
      return '<option value="' + n + '"' + (n === state.pick ? " selected" : "") + ">" + n + "</option>";
    }).join("");
    sel.addEventListener("change", function () { state.pick = parseInt(sel.value, 10); renderAll(); });
    bar.appendChild(sel);
    var step = function (d) {
      var b = fmt.el("button", "ddstep", d < 0 ? "‹" : "›");
      b.title = (d < 0 ? "Previous" : "Next") + " pick";
      b.addEventListener("click", function () {
        var i = ords.indexOf(state.pick) + d;
        if (i >= 0 && i < ords.length) { state.pick = ords[i]; renderAll(); }
      });
      return b;
    };
    bar.appendChild(step(-1));
    bar.appendChild(step(1));
    bar.appendChild(fmt.el("span", "spacer"));
    var positions = {};
    rows().forEach(function (r) { if (r.dp) positions[r.dp] = 1; });
    var posOpts = [[null, "all"]].concat(Object.keys(positions).sort().map(function (p) { return [p, p]; }));
    bar.appendChild(seg("Drafted as", posOpts, state.pos,
      function (v) { state.pos = v; renderAll(); }));
    container.appendChild(bar);
  }

  function halt(page, head, why) {
    var d = fmt.el("div", "reserved");
    d.innerHTML = "<b>" + head + "</b> " + why;
    page.appendChild(d);
  }

  function render(container) {
    _container = container;
    container.innerHTML = "";
    /* Wears the clubs page's class as well as its own, the same way ui/app/pickvalue.js does: the
       stylesheet is visual law and a view may not amend it, so the intro / halt / table vocabulary
       is BORROWED rather than a second unstyled one being invented for the same three things. */
    var page = fmt.el("div", "clubspage draftpage");
    container.appendChild(page);

    if (state.minSeasons == null) state.minSeasons = developedThreshold().lag;

    var pn = pin();
    if (!pn.ok) {
      halt(page, "Draft outcomes unavailable —", fmt.esc(pn.why) +
        ". Nothing is shown rather than base rates computed off a record that does not belong to " +
        "this board.");
      return;
    }

    var intro = fmt.el("div", "cintro");
    intro.innerHTML =
      "What a pick has <b>become</b> — not what it is worth. Every national-draft selection " +
      "from the class of " + YR_LO + " on, complete classes from pick 1, so the men who never " +
      "played are in the count. The Pick value tab carries the price; this one carries the outcome.";
    page.appendChild(intro);

    controls(page);

    /* THE MIDFIELD YARDSTICK IS BUILT ONCE PER RENDER and handed to everything that needs it. It is
       64 frames over the whole population; rebuilding it inside each of the 54 board cells would be
       the same work 54 times, and the page would stutter on every control change. */
    var curve = core.midCurve(rows(), stamp(), board(), state.half, state.minSeasons, YR_LO);
    if (!curve.length) {
      halt(page, "No midfield yardstick.", "The record carries no settled midfield careers, so " +
        "there is no ruler to price the other positions against and no board is drawn.");
      return;
    }

    boardSection(page, curve);
    findingsSection(page, curve);
    comparatorSection(page);

    var detail = fmt.el("div", "ddbhead");
    detail.innerHTML = "<h2>The careers behind a pick</h2><p>Click a cell above, or use the " +
      "selector, to see who this rests on. Nothing on this page is interpolated — every figure " +
      "stands on named careers.</p>";
    page.appendChild(detail);
    detailControls(page);

    var sel = select();
    if (!sel.set.length) {
      halt(page, "No settled careers in this set.", "Widen the neighbourhood, clear the position " +
        "filter, or switch to every class. Nothing is pooled in silently to fill the gap.");
      if (sel.young.length) page.appendChild(roll(sel.young));
      return;
    }
    var rs = rates(sel.set);
    page.appendChild(statPanel(rs, sel));
    page.appendChild(notes(rs, sel));

    var more = fmt.el("button", "ddmore",
      (state.roll ? "Hide" : "Show") + " the " + fmt.n(sel.set.length) + " careers behind these figures");
    more.addEventListener("click", function () { state.roll = !state.roll; renderAll(); });
    page.appendChild(more);
    if (state.roll) page.appendChild(roll(sel.set));
  }

  /* One re-entry point for every control on the page. The container is remembered from the last
     real render so a nested handler does not have to carry it, and a control that fires before the
     first render is a no-op rather than a throw. */
  var _container = null;
  function renderAll() { if (_container) render(_container); }

  return { render: render, pin: pin, select: select, rates: rates, inRun: inRun,
           bundle: bundle, stamp: stamp, state: state, core: core, THIN_MAX: THIN_MAX };
  }

  /* ---- registration: browser (window.MD) + node (module.exports for tests) -------------------- */
  if (typeof window !== "undefined") {
    window.MD = window.MD || {};
    // Deferred exactly as ui/app/pickvalue.js defers: script order guarantees MD.fmt, but a view
    // that assumes it and is wrong renders a blank tab instead of an error, which is the worst of
    // both outcomes.
    window.MD.draftday = (window.MD.fmt) ? makeView(window.MD) : {
      render: function (h) { window.MD.draftday = makeView(window.MD); window.MD.draftday.render(h); },
      core: core,
    };
  }
  if (typeof module !== "undefined" && module.exports) {
    module.exports = { core: core, makeView: makeView };
  }
})(this);
