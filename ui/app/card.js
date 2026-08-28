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
  function eventLabel(r) {
    if (r.isRound) return fmt.esc(r.label || r.id);
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
    const trackPts = (p.track || []).map(function (t) { return { v: t.a }; });
    const trackYears = (p.track || []).map(function (t) { return "s" + t.s; });

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
        '<h2 class="sec"><span>Recent form</span><span class="meta">season score</span></h2>' +
        (trackPts.length ? lineChart(trackPts, trackYears, trackPts.length - 1, true)
          : '<div class="reserved">No recent-form series.</div>') +
        '<h2 class="sec"><span>Weekly history</span></h2>' +
        historySection(p) +
      "</div></div>";
  }

  return { render: render };
})();
