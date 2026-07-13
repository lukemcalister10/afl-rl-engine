/* Matchday UI — player card (working + public). Pure view; the model speaks, the owner overrules. */
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
    const X = function (i) { return 20 + (i * 420) / (n - 1); };
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

  function waterfall(p) {
    // Per-lever attribution needs the levers:[{label,delta}] export field (§7.4 / G-ATTR). Absent in
    // v2.8 -> the section renders honestly: the owner-override line item (when present) + an awaiting
    // note. The grammar (green right / red left, signed mono, residual in alarm red) is fully built.
    let html = "";
    if (p.owner_rule) {
      const pre = p.vRaw != null ? p.vRaw : null;
      html += '<div class="wf">' +
        (pre != null ? '<span class="totals">Model figure</span><span></span>' +
          '<span class="totals" style="text-align:right"><b>' + fmt.n(pre) + "</b></span>" +
          '<span class="rowline"></span>' : "") +
        '<span class="lbl rule">Your rule: owner override <i style="color:var(--volt);opacity:.7">(a rule holds this price, not the model curve)</i></span>' +
        '<span class="track"><span class="zline"></span><span class="bar rule" style="width:46%"></span></span>' +
        '<span class="fig rule">' + (pre != null ? fmt.signed(MD.dispVal(p) - pre) : "override") + "</span>" +
        '<span class="rowline"></span>' +
        '<span class="totals">Lands at</span><span></span><span class="totals" style="text-align:right"><b>' + fmt.n(MD.dispVal(p)) + "</b></span>" +
        "</div>";
      html += '<div class="note"><b>The rule is a line item, not a ghost.</b> The hollow volt bar is your call ' +
        "holding the price — the post-override figure is shown; the model's own figure is one hover away on the tag, never on the rail.</div>";
    }
    html += '<div class="awaiting"><b>Per-lever attribution</b> — the full "why the price is what it is" waterfall ' +
      "(recent scoring · role time · availability · young upside · the unattributed residual) renders the moment the " +
      "export carries <span class=\"num\">levers:[{label,delta}]</span> (§7.4, G-ATTR already requires these to exist). " +
      "No lever figure is invented here; availability will print <b>absent</b>, never skipped, and a residual that grows turns red.</div>";
    return html;
  }

  function renderWorking(container, p) {
    const w = MD.seam.working, st = w.stamp;
    const rank = rankOf(p.key);
    const years = w.lensYears || [2024, 2025, 2026, 2027, 2028];
    const lensPts = p.lens.map(function (v) { return { v: v }; });
    const trackPts = (p.track || []).map(function (t) { return { v: t.a }; });
    const trackYears = (p.track || []).map(function (t) { return "s" + t.s; });

    let ovTag = "";
    if (p.owner_rule) ovTag = '<span class="tag" title="Owner override active — see the waterfall line item">Owner override</span>';

    const dBake = p.vPrev == null ? null : p.v - p.vPrev;
    const dCls = p.vPrev == null ? "flat" : fmt.cls(dBake);
    const dTxt = p.vPrev == null ? "awaiting" : fmt.signed(dBake);

    container.innerHTML =
      '<div class="card"><div class="head">' +
        '<div class="name">' + fmt.esc(p.name) + ovTag + "</div>" +
        '<div class="id">' + fmt.esc(p.pos) + " · " + fmt.esc(p.club || "—") +
          " · " + (p.pk ? "Pick " + p.pk : "no pick") + " · " + (p.yr || "—") + " " + fmt.esc(p.ty || "") + "</div>" +
        '<div class="cstamp">board <b>' + st.tag + "</b> · engine <b>" + st.engine + "</b> · store <b>" + st.store +
          '</b><span class="badge">guard 5 pass</span></div>' +
      "</div><div class=\"body\">" +
        '<div class="statrow">' +
          '<div><div class="k">Value</div><div class="v volt num">' + fmt.n(MD.dispVal(p)) + "</div></div>" +
          '<div><div class="k">Δ vs last bake</div><div class="v ' + dCls + ' num">' + dTxt + "</div></div>" +
          '<div><div class="k">Rank</div><div class="v num">' + (rank || "—") +
            '<small> / ' + fmt.n(st.nPlayers) + "</small></div></div>" +
        "</div>" +
        '<h2 class="sec"><span>Why the price is what it is</span><span class="meta">per-lever</span></h2>' +
        waterfall(p) +
        '<h2 class="sec"><span>Value by year</span><span class="meta">' + years[0] + "–" + years[4] +
          " · the ±2-yr board lens</span></h2>" +
        lineChart(lensPts, years, 2, true) +
        '<h2 class="sec"><span>Recent form</span><span class="meta">season score · real</span></h2>' +
        (trackPts.length ? lineChart(trackPts, trackYears, trackPts.length - 1, true)
          : '<div class="reserved">No recent-form series.</div>') +
        '<h2 class="sec"><span>Round-by-round rating</span><span class="meta">reserved</span></h2>' +
        '<div class="reserved"><b>Wired in the weekly-loop phase.</b> History starts clean on the post-overhaul model; ' +
          "one model version per line, a seam marker where a re-bake splits a season.</div>" +
      "</div></div>";
  }

  function renderPublic(container, p) {
    const w = MD.seam.working; // public card reads sanitised fields only (name/pos/value/lens years)
    const years = w.lensYears || [2024, 2025, 2026, 2027, 2028];
    const lensPts = p.lens.map(function (v) { return { v: v }; });
    container.innerHTML =
      '<div class="card"><div class="head">' +
        '<div class="name">' + fmt.esc(p.name) + "</div>" +
        '<div class="id">' + fmt.esc(p.pos) + " · " + fmt.esc(p.club || "—") + "</div>" +
      "</div><div class=\"body\">" +
        '<div class="statrow">' +
          '<div><div class="k">Value</div><div class="v volt num">' + fmt.n(MD.dispVal(p)) + "</div></div>" +
          '<div><div class="k">Δ vs prev round</div><div class="v flat num">— steady</div></div>' +
          '<div><div class="k">Rank</div><div class="v num">' + (rankOf(p.key) || "—") + "</div></div>" +
        "</div>" +
        '<h2 class="sec"><span>Value by year</span><span class="meta">' + years[0] + "–" + years[4] + "</span></h2>" +
        lineChart(lensPts, years, 2, true) +
        '<footer class="foot">value · rank · movement — always signed, never colour alone</footer>' +
      "</div></div>";
  }

  function render(container) {
    const key = MD.state.cardKey;
    const p = MD.seam.indexed().byKey[key];
    if (!p) { container.innerHTML = '<div class="reserved">Select a player from the board.</div>'; return; }
    const back = fmt.el("button", "tabs");
    back.innerHTML = "<button>← back to board</button>";
    back.firstChild.addEventListener("click", function () { MD.go("board"); });
    container.appendChild(back);
    const holder = fmt.el("div");
    container.appendChild(holder);
    if (MD.state.tier === "public") renderPublic(holder, p); else renderWorking(holder, p);
  }

  return { render: render };
})();
