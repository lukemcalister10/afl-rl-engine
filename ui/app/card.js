/* Matchday UI — player card. Pure view; the model speaks, the owner overrules.

   REDESIGNED 2026-08-28 ON THE OWNER'S WORD: the card shows the player — his price, his round
   move, his rank, his entry price, his form, his history — and none of the machinery that made
   them. Provenance stamps, the per-lever waterfall, the forward +1/+2 projections (ruled off) and
   every explanatory essay are gone from this surface; what still needs saying for maintenance
   lives in ui/MAINTAINER.md. History is ONE LINE PER EVENT: rounds as themselves, model changes
   as "Model change (ID)" — the ledger behind each ID is documentation, not screen furniture. */
window.MD = window.MD || {};

MD.card = (function () {
  const fmt = MD.fmt;

  function rankOf(key) {
    const players = (MD.seam.working.players || []).slice().sort(function (a, b) { return b.v - a.v; });
    for (let i = 0; i < players.length; i++) if (players[i].key === key) return i + 1;
    return null;
  }

  /* polyline over an array of {x,y} in a 460x120 viewbox, volt line, marked "now" point. */
  function lineChart(points, years, nowIdx, labelYears) {
    const vals = points.map(function (p) { return p.v; }).filter(function (v) { return v != null; });
    if (!vals.length) return '<div class="reserved">No trajectory data.</div>';
    const min = Math.min.apply(null, vals), max = Math.max.apply(null, vals);
    const span = max - min || 1;
    const n = points.length;
    const X = function (i) { return 20 + (i * 420) / (n - 1 || 1); };
    const Y = function (v) { return 100 - ((v - min) / span) * 80; };
    let poly = "", dots = "", labels = "";
    points.forEach(function (p, i) {
      if (p.v == null) return;
      poly += (poly ? " " : "") + X(i).toFixed(0) + "," + Y(p.v).toFixed(0);
      if (i === nowIdx) {
        dots += '<circle cx="' + X(i).toFixed(0) + '" cy="' + Y(p.v).toFixed(0) + '" r="4" fill="#f2f5f9"/>' +
          '<text x="' + X(i).toFixed(0) + '" y="' + (Y(p.v) - 10).toFixed(0) + '" fill="#f2f5f9" font-size="10" ' +
          'text-anchor="middle" font-family="monospace">' + years[i] + "</text>";
      }
    });
    if (labelYears) {
      years.forEach(function (yr, i) {
        if (i === nowIdx) return;
        labels += '<text x="' + X(i).toFixed(0) + '" y="114" fill="#525c6d" font-size="10" ' +
          'text-anchor="middle" font-family="monospace">' + yr + "</text>";
      });
    }
    return '<div class="chart"><svg viewBox="0 0 460 120">' +
      '<polyline points="' + poly + '" fill="none" stroke="#c8f04a" stroke-width="2"/>' +
      dots + labels + "</svg></div>";
  }

  /* ================== OWNER ITEM 3 (2026-08-31): THE WEEKLY VALUE GRAPH ==================
     His word: "recent form" comes off the card and a graph of the player's value each week since
     R14 goes on, with the x and y axes labelled.

     IT READS `MD.history.series`, IT DOES NOT DERIVE. That function already owns three things this
     chart must not re-decide and could easily get wrong on its own:
       · WHICH UNIVERSE IS ON SCREEN. Current-model-only or all-in, per the Config tab. The card and
         the movers tab share that choice through MD.universe precisely so they cannot disagree, and
         a chart that walked the bundle itself would be the third opinion.
       · WHAT EACH POINT IS. A round, a retro re-pricing of a round, a finals week, a model change.
       · THAT THE TRACE IS COMPLETE. Every player carries a value at every point — a player who did
         not play still moves, because everyone else did — so this line NEVER has participation gaps
         and needs no "did not play" handling. Score coverage is the patchy column; value is not.

     THE AXES ARE LABELLED BECAUSE HE ASKED, AND THE Y AXIS IS NOT ZERO-BASED. A keeper board's
     weekly movement is a few per cent of a four-figure price; anchoring the axis at zero would draw
     every player as the same flat line. The axis therefore spans the player's own range with a
     margin, and SAYS SO on the axis title, so nobody reads a steep line as a collapse. */

  /* the x tick for one point: short enough to sit under a dense axis, still unambiguous. */
  function shortPointLabel(r) {
    if (r.isRound) {
      const m = /(\d+)\s*$/.exec(String(r.label || ""));
      return m ? m[1] : String(r.label || r.id);
    }
    const fin = finalsName(r.id);
    if (fin) return fin.replace(/[^A-Z0-9]/g, "");     // "Finals Week 1" -> "FW1"
    return mcId(r.modelChange);
  }
  function longPointLabel(r) {
    if (r.isRound) return (r.label || String(r.id)) + (r.isRetro ? " (re-priced under the current model)" : "");
    return finalsName(r.id) || ("Model change " + mcId(r.modelChange));
  }

  /* a human y-axis: 4-ish ticks on a round step covering [lo,hi], never a step of zero. */
  function niceTicks(lo, hi, want) {
    const span = (hi - lo) || 1;
    const raw = span / Math.max(1, want);
    const mag = Math.pow(10, Math.floor(Math.log(raw) / Math.LN10));
    const norm = raw / mag;
    const step = (norm <= 1 ? 1 : norm <= 2 ? 2 : norm <= 5 ? 5 : 10) * mag;
    const out = [];
    for (let t = Math.ceil(lo / step) * step; t <= hi + step * 0.001; t += step) out.push(Math.round(t));
    return out.length >= 2 ? out : [Math.round(lo), Math.round(hi)];
  }

  const WCHART = { w: 640, h: 260, l: 58, r: 14, t: 16, b: 52 };

  function weeklyValueChart(key) {
    const rows = (MD.history.series(key) || []).filter(function (r) { return r.v != null; });
    if (rows.length < 2) {
      return '<div class="reserved">Not enough weekly points to draw a line' +
             (rows.length === 1 ? " — this player carries a value at one point only." : ".") + "</div>";
    }
    const vals = rows.map(function (r) { return r.v; });
    let lo = Math.min.apply(null, vals), hi = Math.max.apply(null, vals);
    const pad = ((hi - lo) || Math.max(1, hi * 0.02)) * 0.18;
    lo -= pad; hi += pad;
    const ticks = niceTicks(lo, hi, 4);
    lo = Math.min(lo, ticks[0]); hi = Math.max(hi, ticks[ticks.length - 1]);

    const g = WCHART;
    const iw = g.w - g.l - g.r, ih = g.h - g.t - g.b;
    const X = function (i) { return g.l + (rows.length === 1 ? iw / 2 : (i * iw) / (rows.length - 1)); };
    const Y = function (v) { return g.t + ih - ((v - lo) / ((hi - lo) || 1)) * ih; };

    // grid + y labels
    let grid = "", ylab = "";
    ticks.forEach(function (t) {
      const y = Y(t).toFixed(1);
      grid += '<line x1="' + g.l + '" x2="' + (g.w - g.r) + '" y1="' + y + '" y2="' + y + '" class="wcg"/>';
      ylab += '<text x="' + (g.l - 8) + '" y="' + y + '" class="wcy">' + fmt.n(t) + "</text>";
    });

    /* X LABELS THIN THEMSELVES rather than overlapping. With a long season the ticks would collide,
       so every nth is drawn — but the FIRST and the LAST are always drawn whatever n works out to,
       because "since when" and "as at when" are the two readings the axis exists to give. */
    const every = Math.max(1, Math.ceil(rows.length / 12));
    let xlab = "", poly = "", dots = "";
    rows.forEach(function (r, i) {
      const x = X(i), y = Y(r.v);
      poly += (poly ? " " : "") + x.toFixed(1) + "," + y.toFixed(1);
      const last = i === rows.length - 1;
      if (i % every === 0 || last || i === 0) {
        xlab += '<text x="' + x.toFixed(1) + '" y="' + (g.t + ih + 16) + '" class="wcx' +
          (r.isRound ? "" : " ev") + '">' + fmt.esc(shortPointLabel(r)) + "</text>";
      }
      // A NON-ROUND POINT IS MARKED DIFFERENTLY because it is not a week of football: a finals week
      // and a model change both land as their own column, and a hollow marker says "this step was
      // not a normal round" without needing a legend nobody reads.
      dots += '<circle cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" r="' + (last ? 4.5 : 3) +
        '" class="wcd' + (last ? " now" : "") + (r.isRound ? "" : " ev") + '">' +
        "<title>" + fmt.esc(longPointLabel(r)) + ": " + fmt.n(r.v) +
        (r.dv == null ? "" : " (" + fmt.signed(r.dv) + ")") + "</title></circle>";
    });

    const first = rows[0], last = rows[rows.length - 1];
    const net = last.v - first.v;

    return '<div class="wchart"><svg viewBox="0 0 ' + g.w + " " + g.h + '" preserveAspectRatio="xMidYMid meet">' +
      grid +
      '<line x1="' + g.l + '" x2="' + g.l + '" y1="' + g.t + '" y2="' + (g.t + ih) + '" class="wca"/>' +
      '<line x1="' + g.l + '" x2="' + (g.w - g.r) + '" y1="' + (g.t + ih) + '" y2="' + (g.t + ih) + '" class="wca"/>' +
      '<polyline points="' + poly + '" class="wcl"/>' + dots + ylab + xlab +
      // the axis TITLES — the half of his ask that a bare tick row does not satisfy
      '<text x="' + (g.l + iw / 2) + '" y="' + (g.h - 8) + '" class="wcat">ROUND</text>' +
      '<text transform="translate(14,' + (g.t + ih / 2) + ') rotate(-90)" class="wcat">VALUE</text>' +
      "</svg>" +
      '<div class="wcfoot"><span>' + fmt.esc(longPointLabel(first)) + " <b>" + fmt.n(first.v) +
        "</b></span><span>" + fmt.esc(longPointLabel(last)) + " <b>" + fmt.n(last.v) + "</b></span>" +
        '<span class="' + fmt.cls(net) + '">net ' + fmt.signed(net) + "</span>" +
        '<span class="axnote">Vertical axis spans this player\u2019s own range, not zero.</span></div>' +
      "</div>";
  }

  /* the section's own subtitle — "Round 14 - Finals Week 1" — READ off the series rather than
     written as "since Round 14". The series begins where the bundle begins; the day it begins
     somewhere else this heading follows it, and a hardcoded "since Round 14" would quietly lie. */
  function weeklySpan(key) {
    const rows = (MD.history.series(key) || []).filter(function (r) { return r.v != null; });
    if (!rows.length) return "";
    if (rows.length === 1) return longPointLabel(rows[0]);
    return longPointLabel(rows[0]) + " \u2013 " + longPointLabel(rows[rows.length - 1]);
  }

  function movePill(d) {
    if (d == null) return '<span class="hm na">—</span>';
    return '<span class="hm ' + fmt.cls(d) + '">' + fmt.signed(d) + "</span>";
  }

  function scoreTd(cell) {
    if (cell.state === "score") {
      return '<td class="num hsc">' + fmt.n(cell.score) + "</td>";
    }
    if (cell.state === "dnp") {
      return '<td class="num hsc"><span class="dnp" title="' + fmt.esc(cell.why) + '">DNP</span></td>';
    }
    return '<td class="num hsc"><span class="unrec" title="' + fmt.esc(cell.why) + '">—</span></td>';
  }

  /* ONE LINE PER EVENT (owner word 2026-08-28). A round is its round label; a model change is
     "Model change (ID)" and nothing else — the ID indexes the maintainer ledger. */
  let _mcIds = null;
  function mcId(mc) {
    // Sequential IDs in the bundle's own order: MC-1, MC-2, ... The ledger mapping each ID to its
    // full record is maintainer documentation (ui/MAINTAINER.md), not screen furniture.
    if (!_mcIds) {
      _mcIds = {};
      const list = ((window.__MATCHDAY_MOVERS__ || {}).model_changes) || [];
      list.forEach(function (c, i) {
        _mcIds[JSON.stringify(c.between || i)] = "MC-" + (i + 1);
      });
    }
    return (mc && _mcIds[JSON.stringify(mc.between)]) || "MC";
  }
  /* A FINALS WEEK IS FOOTBALL, NOT A MODEL CHANGE — the browser's copy of
     round_movers.FINALS_COLUMN_PREFIXES, keyed on the column id the act declares. It lands as a
     store edit, so it arrives here as a non-round row and fell through to "Model change (MC-N)":
     unfindable, and a claim about the model that is false about a week of scores. */
  const FINALS_COLUMNS = { "fw1-": "Finals Week 1", "fw2-": "Finals Week 2",
                           "sf-": "Semi-Final", "pf-": "Preliminary Final", "gf-": "Grand Final" };
  function finalsName(id) {
    const s = String(id || "");
    const hit = Object.keys(FINALS_COLUMNS).filter(function (k) { return s.indexOf(k) === 0; })[0];
    return hit ? FINALS_COLUMNS[hit] : null;
  }
  function eventLabel(r) {
    if (r.isRound) return fmt.esc(r.label || r.id);
    const fin = finalsName(r.id);
    if (fin) return '<span class="finalsev">' + fmt.esc(fin) + "</span>";
    return 'Model change <span class="mcid">(' + fmt.esc(mcId(r.modelChange)) + ")</span>";
  }

  function historySection(p) {
    const rows = MD.history.series(p.key);
    if (!rows || !rows.length) {
      return '<div class="reserved">No weekly history for this player.</div>';
    }
    let body = "";
    rows.forEach(function (r) {
      body +=
        '<tr class="' + (r.isRound ? "" : "hmodel") + '">' +
          '<td class="hpt">' + eventLabel(r) + "</td>" +
          '<td class="num">' + fmt.n(r.v) + "</td>" +
          '<td class="num">' + movePill(r.dv) + "</td>" +
          '<td class="num">' + (r.rank == null ? "—" : r.rank) + "</td>" +
          '<td class="num">' + movePill(r.dRank) + "</td>" +
          '<td class="num">' + (r.posRank == null ? "—" : r.posRank) + "</td>" +
          '<td class="num">' + movePill(r.dPosRank) + "</td>" +
          scoreTd(r.score) +
        "</tr>";
    });
    return '<div class="histwrap"><table class="histtbl">' +
      "<thead><tr>" +
        "<th></th>" +
        '<th class="num">Value</th><th class="num">Δ</th>' +
        '<th class="num">Rank</th><th class="num">Δ</th>' +
        '<th class="num">Pos rank</th><th class="num">Δ</th>' +
        '<th class="num">Score</th>' +
      "</tr></thead><tbody>" + body + "</tbody></table></div>";
  }

  /* Entry price — the four figures, nothing else. */
  function v0Section(p) {
    const r = MD.v0.of(p);
    const live = r.live != null ? r.live : MD.dispVal(p);
    if (r.refused || !r.has) {
      return '<div class="statrow">' +
        '<div><div class="k">Entry price</div><div class="v num" title="' + fmt.esc(r.why || "") + '">—</div></div>' +
        '<div><div class="k">Now</div><div class="v volt num">' + fmt.n(live) + "</div></div>" +
        "</div>";
    }
    const dCls = fmt.cls(r.delta);
    const rCls = r.ratio == null ? "na" : (r.ratio > 1 ? "up" : r.ratio < 1 ? "dn" : "flat");
    return '<div class="statrow">' +
        '<div><div class="k">Entry price</div><div class="v num">' + fmt.n(r.v0) + "</div></div>" +
        '<div><div class="k">Now</div><div class="v volt num">' + fmt.n(r.live) + "</div></div>" +
        '<div><div class="k">vs entry</div><div class="v ' + dCls + ' num">' + fmt.signed(r.delta) + "</div></div>" +
        '<div><div class="k">ratio</div><div class="v ' + rCls + ' num">' + fmt.esc(MD.v0.ratioText(r.ratio)) + "</div></div>" +
      "</div>";
  }

  function render(container) {
    const key = MD.state.cardKey;
    const p = MD.seam.indexed().byKey[key];
    if (!p) { container.innerHTML = '<div class="reserved">Select a player from the board.</div>'; return; }

    const w = MD.seam.working, st = w.stamp || {};
    const rank = rankOf(p.key);

    // ROUND CHANGE — the same figure as the board column (the latest weekly report of record).
    const rd = MD.board.roundDeltas();
    const rr = rd && rd[p.key];
    const dTxt = (rr && rr.d != null) ? fmt.signed(rr.d) : "—";
    const dCls = (rr && rr.d != null) ? fmt.cls(rr.d) : "na";
    const dTitle = (rr && rr.d != null) ? ("Round " + rd._round + " vs Round " + rd._prev) : "no weekly report";

    // The trajectory the card charts is the REAL one: backward re-values and now. The forward
    // +1/+2 projections are ruled off and render nowhere (owner word 2026-08-28).
    const years = (w.lensYears || [2024, 2025, 2026]).slice(0, 3);
    const lensPts = (p.lens || []).slice(0, 3).map(function (v) { return { v: v }; });

    let ovTag = "";
    if (p.owner_rule) ovTag = '<span class="tag" title="Your rule holds this price.">Owner rule</span>';

    container.innerHTML =
      '<div class="card"><div class="head">' +
        '<div class="name">' + fmt.esc(p.name) + ovTag + "</div>" +
        '<div class="id">' + fmt.esc(p.pos) +
          " · " + (p.pk ? "Pick " + p.pk : "no pick") + " · " + (p.yr || "—") + " " + fmt.esc(p.ty || "") + "</div>" +
        '<div class="clubs"><span><b>AFL</b> ' + fmt.esc(p.afl_club || p.club || "—") + "</span>" +
          '<span><b>AFFL</b> ' + fmt.esc(MD.ownership.labelOf(p)) + "</span></div>" +
      "</div><div class=\"body\">" +
        '<div class="statrow">' +
          '<div><div class="k">Value</div><div class="v volt num">' + fmt.n(MD.dispVal(p)) + "</div></div>" +
          '<div><div class="k">Round Δ</div><div class="v ' + dCls + ' num" title="' + fmt.esc(dTitle) + '">' + dTxt + "</div></div>" +
          '<div><div class="k">Rank</div><div class="v num">' + (rank || "—") +
            '<small> / ' + fmt.n(st.nPlayers || (w.players || []).length) + "</small></div></div>" +
        "</div>" +
        '<h2 class="sec"><span>Entry price</span></h2>' +
        v0Section(p) +
        '<h2 class="sec"><span>Value by year</span><span class="meta">' + years[0] + "–" + years[years.length - 1] + "</span></h2>" +
        lineChart(lensPts, years, years.length - 1, true) +
        // OWNER ITEM 3 (2026-08-31): the season-score "Recent form" line is replaced by the weekly
        // value graph. The scores it drew are not lost — they remain, per round, in the Score
        // column of the weekly history table directly below, where each one carries its own
        // played / did-not-play / not-recorded truth instead of being smoothed into a line.
        '<h2 class="sec"><span>Weekly value</span><span class="meta">' +
          fmt.esc(weeklySpan(p.key)) + "</span></h2>" +
        weeklyValueChart(p.key) +
        '<h2 class="sec"><span>Weekly history</span></h2>' +
        historySection(p) +
      "</div></div>";
  }

  return { render: render };
})();
