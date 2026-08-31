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
   99% of eventual debutants had debuted within four completed seasons, so four is the line. The
   younger classes are not hidden — they are reported on their own line, with how many have already
   debuted — but they are kept out of the rates. The threshold comes off the bundle
   (`stamp.maturitySeasons`) with the table it was measured from; it is not a constant in this file.

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
  var THIN_MAX = 8;

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
    function isMature(stamp, y) { return classAge(stamp, y) >= (stamp.maturitySeasons || 0); }

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
        if (state.mature && !isMature(stamp, r.y)) young.push(r);
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

    return { classAge: classAge, isMature: isMature, maturityFromLags: maturityFromLags,
             select: select, quantile: quantile, rates: rates, pinOf: pinOf,
             priceRange: priceRange, THIN_MAX: THIN_MAX };
  })();

  function makeView(MD) {
  var fmt = MD.fmt;

  var state = { pick: 1, spread: 0, pos: null, mature: true, roll: false };

  function bundle() {
    return (typeof window !== "undefined" && window.__DRAFT_OUTCOMES__) || null;
  }

  function pin() {
    var b = bundle();
    return core.pinOf(b && b.stamp, MD.seam.working.stamp);
  }

  function rows() { var b = bundle(); return (b && b.rows) || []; }
  function stamp() { var b = bundle(); return (b && b.stamp) || {}; }
  function isMature(y) { return core.isMature(stamp(), y); }
  function select() { return core.select(rows(), stamp(), state); }
  var quantile = core.quantile;

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

  function controls(container) {
    var bar = fmt.el("div", "strip ddstrip");
    var ords = ordinals();

    bar.appendChild(fmt.el("span", "lbl", "Pick"));
    var sel = document.createElement("select");
    sel.className = "boardsel";
    sel.innerHTML = ords.map(function (n) {
      return '<option value="' + n + '"' + (n === state.pick ? " selected" : "") + ">" + n + "</option>";
    }).join("");
    sel.addEventListener("change", function () {
      state.pick = parseInt(sel.value, 10); render(container);
    });
    bar.appendChild(sel);

    var step = function (d) {
      var b = fmt.el("button", "ddstep", d < 0 ? "‹" : "›");
      b.title = (d < 0 ? "Previous" : "Next") + " pick";
      b.addEventListener("click", function () {
        var i = ords.indexOf(state.pick) + d;
        if (i >= 0 && i < ords.length) { state.pick = ords[i]; render(container); }
      });
      return b;
    };
    bar.appendChild(step(-1));
    bar.appendChild(step(1));
    bar.appendChild(fmt.el("span", "spacer"));

    bar.appendChild(seg("Neighbourhood",
      [[0, "this pick"], [2, "±2"], [5, "±5"]], state.spread,
      function (v) { state.spread = v; render(container); }));

    var positions = {};
    rows().forEach(function (r) { if (r.dp) positions[r.dp] = 1; });
    var posOpts = [[null, "all"]].concat(Object.keys(positions).sort().map(function (p) { return [p, p]; }));
    bar.appendChild(seg("Drafted as", posOpts, state.pos,
      function (v) { state.pos = v; render(container); }));

    bar.appendChild(seg("Classes",
      [[true, "settled only"], [false, "every class"]], state.mature,
      function (v) { state.mature = v; render(container); }));

    container.appendChild(bar);
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
    if (sel.young.length) {
      var debuted = sel.young.filter(function (r) { return r.g > 0; }).length;
      parts.push("<b>" + fmt.n(sel.young.length) + " selection" + (sel.young.length === 1 ? "" : "s") +
        " from classes still running are excluded</b> from every figure above — " +
        fmt.n(debuted) + " of them " + (debuted === 1 ? "has" : "have") + " already debuted. A class " +
        "counts once it has had <b>" + st.maturitySeasons + " completed seasons</b>, and that line " +
        "is measured rather than chosen: " + pct(
          Math.round(1000 * (((st.debutLagTable || []).filter(function (t) {
            return t.lag === st.maturitySeasons; })[0] || {}).cum || 0)) / 10, 100) +
        " of the " + fmt.n(st.debutLagN) + " eventual debutants in the settled classes had debuted " +
        "by then. Switch to <b>every class</b> to fold them in.");
    } else if (!state.mature) {
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

  function halt(page, head, why) {
    var d = fmt.el("div", "reserved");
    d.innerHTML = "<b>" + head + "</b> " + why;
    page.appendChild(d);
  }

  function render(container) {
    container.innerHTML = "";
    /* Wears the clubs page's class as well as its own, the same way ui/app/pickvalue.js does: the
       stylesheet is visual law and a view may not amend it, so the intro / halt / table vocabulary
       is BORROWED rather than a second unstyled one being invented for the same three things. */
    var page = fmt.el("div", "clubspage draftpage");
    container.appendChild(page);

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
      "since " + stamp().classFrom + ", complete classes from pick 1, so the men who never played " +
      "are in the count. The Pick value tab carries the price; this one carries the outcome.";
    page.appendChild(intro);

    controls(page);

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
    more.addEventListener("click", function () { state.roll = !state.roll; render(container); });
    page.appendChild(more);
    if (state.roll) page.appendChild(roll(sel.set));
  }

  return { render: render, pin: pin, select: select, rates: rates, isMature: isMature,
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
