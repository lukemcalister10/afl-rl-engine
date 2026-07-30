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

  /* ======================= #139 item 3 — THE WEEKLY HISTORY =======================================
     Replaces the "reserved · wired in the weekly-loop phase" placeholder with the real per-round record.

     TWO COLUMNS, TWO POPULATIONS. The value / rank / positional-rank trace is COMPLETE — every one of
     the tracked players carries all three at all eight points — so it is rendered unconditionally and
     carries no participation caveat. The score column is NOT uniformly covered, so its cell is resolved
     by MD.history.scoreCell(), which distinguishes "he did not play" (only ever claimed for a round
     proven completely fed) from "the feed did not carry him". See ui/app/history.js for the contract
     and the measurements behind it. Nothing here invents a football fact. */

  function movePill(d, invertColour) {
    if (d == null) return '<span class="hm na">—</span>';
    // rank movement is already signed so that positive == improved; colour follows the same sign.
    return '<span class="hm ' + fmt.cls(d) + '">' + fmt.signed(d) + "</span>";
  }

  function scoreTd(cell) {
    if (cell.state === "score") {
      return '<td class="num hsc">' + fmt.n(cell.score) + "</td>";
    }
    if (cell.state === "dnp") {
      return '<td class="num hsc"><span class="dnp" title="' + fmt.esc(cell.why) + '">DNP</span></td>';
    }
    // "unrecorded" and "not-a-round" both render as a blank with the reason on hover. Neither ever
    // says anything about whether the player took the field.
    return '<td class="num hsc"><span class="unrec" title="' + fmt.esc(cell.why) + '">—</span></td>';
  }

  /* The "model change" tooltip, per point. It used to be one hard-coded sentence naming the ITEM 411
     restructure, written when that was the only out-of-round column in the system's life. The 30/7
     rederivation added a second one, so the fixed text began telling the owner that the 30/7 column was
     the ITEM 411 restructure — a wrong statement on a live surface. It now names the change the row
     actually is, from the bundle's own model_changes entry (#274 item 1; display only — no value,
     ordering or selection behaviour changes). */
  function modelChangeWhy(r) {
    const mc = r.modelChange || null;
    const name = (mc && mc.label) || r.label || r.id || "a model change";
    let why = "A model change, not a week of football: " + name + ". Value and rank move here because " +
              "the model changed, not because anyone played.";
    if (mc && mc.owner_approved_record) {
      const ids = [].concat(mc.owner_ruling_id || []).filter(Boolean);
      why += " This change is on the record as owner-approved" + (ids.length ? " (" + ids.join(", ") + ")" : "") + ".";
    }
    return why;
  }

  function historySection(p) {
    const rows = MD.history.series(p.key);
    if (!rows || !rows.length) {
      return '<div class="reserved"><b>No weekly history for this player.</b> The movers bundle carries no ' +
        "trace under his key; nothing is inferred in its place.</div>";
    }
    const cov = MD.history.coverage();
    const complete = [], partial = [];
    Object.keys(cov.rounds).sort(function (a, b) { return a - b; }).forEach(function (r) {
      (cov.rounds[r].complete ? complete : partial).push("R" + r);
    });

    let body = "";
    rows.forEach(function (r) {
      const isChange = !r.isRound;
      body +=
        '<tr class="' + (isChange ? "hmodel" : "") + '">' +
          '<td class="hpt">' + fmt.esc(r.label || r.id) +
            (isChange ? '<span class="mctag" title="' + fmt.esc(modelChangeWhy(r)) +
              '">model change</span>' : "") + "</td>" +
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
        "<th>Point</th>" +
        '<th class="num">Value</th><th class="num">Δ</th>' +
        '<th class="num">Rank</th><th class="num">Δ</th>' +
        '<th class="num">Pos rank</th><th class="num">Δ</th>' +
        '<th class="num">Score</th>' +
      "</tr></thead><tbody>" + body + "</tbody></table></div>" +
      '<div class="histnote">' +
        "<b>Value, rank and positional rank are complete.</b> All " + fmt.n(MD.history.traceSize()) +
        " tracked players carry all three at every one of the " + rows.length +
        " points, whether or not they played — a player who sat out still moves, because everyone else " +
        "did. Rank movement is shown so that <b>positive means improved</b> (a rank of 99 → 63 reads ▲ +36)." +
        "<br><b>Score coverage is not uniform, so a blank score never means \"did not play\".</b> " +
        (complete.length
          ? "A completely-fed round — every one of the " + cov.clubsOnBoard + " clubs present at full-side " +
            "strength — is the only place an absence can mean he missed the game, and only there is <b>DNP</b> " +
            "printed: " + complete.join(", ") + ". "
          : "No round in this bundle is completely fed, so <b>no played/DNP indicator is shown anywhere</b>. ") +
        (partial.length
          ? "In " + partial.join(", ") + " the early catch-up feed was partial — whole clubs are missing — so " +
            "an absence there means the feed did not carry him and the cell is left blank. "
          : "") +
        "Round 14 is the baseline the trace starts from and carries no score map at all. Hover any blank " +
        "cell for its reason." +
      "</div>";
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
        '<div class="id">' + fmt.esc(p.pos) +
          " · " + (p.pk ? "Pick " + p.pk : "no pick") + " · " + (p.yr || "—") + " " + fmt.esc(p.ty || "") + "</div>" +
        // item 1: both clubs, labelled, on the card head.
        '<div class="clubs"><span><b>AFL</b> ' + fmt.esc(p.afl_club || p.club || "—") + "</span>" +
          '<span title="' + fmt.esc(MD.ownership.titleOf(p)) + '"><b>AFFL</b> ' +
            fmt.esc(MD.ownership.labelOf(p)) + "</span></div>" +
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
        '<h2 class="sec"><span>Weekly history</span><span class="meta">value · rank · positional rank · score</span></h2>' +
        historySection(p) +
      "</div></div>";
  }

  /* ============ #139 items 17 and 18 — PUBLIC / WORKING PARITY ====================================
     The public card renders from the same player record as the working one; the difference has always
     been which fields it chose to print. So this is a decision about each field, not a build.

     CLOSED (general player facts, with no reason to withhold them):
       · draft pick, draft year and entry type — item 18 names the pick explicitly.
       · rank WITH ITS DENOMINATOR ("136 of 804") — item 18 names it; a bare rank cannot be read.
       · Recent form — item 17. The section already existed and was simply never exposed here.
       · the weekly history — item 3's table, the same one the working card shows.
       · movement vs the previous round — the public bundle has always carried `dRound`, yet this card
         printed a hardcoded "— steady" for every player no matter how far he had actually moved. That
         was not a withheld field, it was a wrong one; it now shows the real figure.

     LEFT HIDDEN, DELIBERATELY — each by decision and named in the hand-back, none merely by default:
       · the board / engine / store identity stamp and the "guard 5 pass" badge — build provenance, not
         a fact about the player.
       · the owner-override tag, the override line item in the waterfall, and the model's pre-override
         figure (`vRaw`) — this is the owner's own pricing decision on a named player. Genuinely private.
       · the per-lever attribution panel — model internals, and today an "awaiting the export field"
         notice rather than a player fact.
       · the debug slug (`p.key`) and the Δ-vs-last-bake base — an internal handle and an internal bake
         concept. The public tier gets Δ vs previous round, which is the one that means something. */
  function renderPublic(container, p) {
    const w = MD.seam.working, st = w.stamp || {};
    const years = w.lensYears || [2024, 2025, 2026, 2027, 2028];
    const lensPts = p.lens.map(function (v) { return { v: v }; });
    const trackPts = (p.track || []).map(function (t) { return { v: t.a }; });
    const trackYears = (p.track || []).map(function (t) { return "s" + t.s; });
    const rank = rankOf(p.key);
    const denom = st.nPlayers != null ? st.nPlayers : (w.players || []).length;

    // item 18: real round movement, from the same `dRound` the public board row already uses.
    const dTxt = p.dRound == null ? "—" : fmt.signed(p.dRound);
    const dCls = p.dRound == null ? "na" : fmt.cls(p.dRound);
    const dTitle = p.dRound == null
      ? "No previous-round movement is published for this player; nothing is invented."
      : "Movement vs the previous round.";

    container.innerHTML =
      '<div class="card"><div class="head">' +
        '<div class="name">' + fmt.esc(p.name) + "</div>" +
        // item 18: draft pick · year · entry type, as the working card shows them.
        '<div class="id">' + fmt.esc(p.pos) +
          " · " + (p.pk ? "Pick " + p.pk : "no pick") + " · " + (p.yr || "—") + " " + fmt.esc(p.ty || "") + "</div>" +
        '<div class="clubs"><span><b>AFL</b> ' + fmt.esc(p.afl_club || p.club || "—") + "</span>" +
          '<span title="' + fmt.esc(MD.ownership.titleOf(p)) + '"><b>AFFL</b> ' +
            fmt.esc(MD.ownership.labelOf(p)) + "</span></div>" +
      "</div><div class=\"body\">" +
        '<div class="statrow">' +
          '<div><div class="k">Value</div><div class="v volt num">' + fmt.n(MD.dispVal(p)) + "</div></div>" +
          '<div><div class="k">Δ vs prev round</div><div class="v ' + dCls + ' num" title="' +
            fmt.esc(dTitle) + '">' + dTxt + "</div></div>" +
          // item 18: the rank carries its denominator.
          '<div><div class="k">Rank</div><div class="v num">' + (rank || "—") +
            '<small> of ' + fmt.n(denom) + "</small></div></div>" +
        "</div>" +
        '<h2 class="sec"><span>Value by year</span><span class="meta">' + years[0] + "–" + years[4] + "</span></h2>" +
        lineChart(lensPts, years, 2, true) +
        // item 17: Recent form, exposed on the public tier.
        '<h2 class="sec"><span>Recent form</span><span class="meta">season score · real</span></h2>' +
        (trackPts.length ? lineChart(trackPts, trackYears, trackPts.length - 1, true)
          : '<div class="reserved">No recent-form series.</div>') +
        // item 3: the same weekly history the working card shows.
        '<h2 class="sec"><span>Weekly history</span><span class="meta">value · rank · positional rank · score</span></h2>' +
        historySection(p) +
        '<footer class="foot">value · rank · movement — always signed, never colour alone</footer>' +
      "</div></div>";
  }

  function render(container) {
    const key = MD.state.cardKey;
    const p = MD.seam.indexed().byKey[key];
    if (!p) { container.innerHTML = '<div class="reserved">Select a player from the board.</div>'; return; }
    /* #139 item 15: the card's own "← back to board" button is GONE. It was the reason Back was
       player-card-specific and always went to the board — so club → player → Back landed on the
       all-player list, and player → club had no Back at all. The universal Back now lives in the app
       chrome (main.js) and returns to the actual previous page, board filters and all. */
    const holder = fmt.el("div");
    container.appendChild(holder);
    if (MD.state.tier === "public") renderPublic(holder, p); else renderWorking(holder, p);
  }

  return { render: render };
})();
