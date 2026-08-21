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

  /* ================= PER-LEVER ATTRIBUTION — THE WATERFALL, LIT ==================================
     The panel waited for `levers:[{label,delta}]`. The export has shipped `levers` on 804/804 rows
     since the v2.9 attribution sidecar landed (rl_export.py `player_rec` → `export_attribution.json`),
     but as a DICT keyed by dial code — {L1,L4,L2,L3,L5} — not the array of {label,delta} this card was
     written against. So the most-designed panel in the app displayed "awaiting the export field" while
     the field was there. This reads the shipped shape.

     THE CODE → OWNER-WORD MAP IS NOT INVENTED HERE. It is read off the certified chain that produced
     the sidecar — session_2026-07-13/v2_9_refit_cert/scripts/gen_gattr_chain.sh runs the six stage
     boards by toggling exactly these five env dials in exactly this order, and
     session_2026-07-21/final_integration/tools/config_inventory.py names each one "v2.9 L1…L5":
       L1 = RL_PVCADOPT      — the adopted pick-value curve (entry pick capital re-priced)
       L4 = RL_MSD_POOL_EXCL — mid-season-draft rows excluded from the training pool
       L2 = RL_DIAL14        — the balance-lens weight, dial 14 (owner-ruled D5, "14 for now")
       L3 = RL_AGE           — the s(age) age-shape refit
       L5 = RL_L5_PICKLESS   — pickless (SSP) re-entry pick capital
     A code the map does not know prints its own code, never a guessed word.

     ORDER IS FIXED, NOT SORTED BY SIZE. DESIGN_DIRECTION §5 asks for "largest |Δ| first", but the
     register's own reading of this decomposition forbids it: G-ATTR "separable" means PATH-ADDITIVE —
     "the decomposition is sequential along the fixed order L1→L4→L2→L3→L5; a different order would
     split the same 9,650 differently. Future seats must not read per-lever numbers as order-free."
     Re-ordering the bars would invite exactly that misreading, so they render in the chain's order,
     with the order stated on the panel. A lever that contributed nothing prints as a zero line and is
     never omitted (absence is a finding, §5).

     THE RESIDUAL IS THE POINT. §5: "The waterfall's end figure must equal the displayed value — if the
     export's lever deltas don't sum, the panel shows the residual as an explicit 'unattributed' bar in
     alarm red. An unreviewable move should look broken, because it is." Measured on the shipped board
     today the residual is large on 802 of 804 rows (median 150, p90 586, max 2,272), because the
     sidecar is frozen at its certification era (its own `source` names engine 2030e5df / store
     b0c39d78) while the board has moved several engine eras since. That is a real finding about the
     data, not a rendering choice, and the panel states it in words under the bars rather than hiding
     it behind a tidy total. */
  const LEVER_ORDER = ["L1", "L4", "L2", "L3", "L5"];
  const LEVER_LABEL = {
    L1: { word: "Pick-curve adoption",
          tip: "L1 · RL_PVCADOPT — the adopted pick-value curve: what his entry pick capital is worth under the ruled curve." },
    L4: { word: "Mid-season-draft pool",
          tip: "L4 · RL_MSD_POOL_EXCL — mid-season-draft rows held out of the training pool." },
    L2: { word: "Balance-lens weight",
          tip: "L2 · RL_DIAL14 — the balance lens set to dial 14 (owner-ruled D5, “14 for now”)." },
    L3: { word: "Age shape",
          tip: "L3 · RL_AGE — the s(age) age-shape refit." },
    L5: { word: "Pickless re-entry",
          tip: "L5 · RL_L5_PICKLESS — pickless (SSP) re-entry pick capital. Inert on a board with no active pickless entrant; certified at +0, reproduced not contradicted." },
  };

  /* One waterfall row: label · zero-centred bar · signed mono figure. `scale` is the largest |Δ| on
     the panel, so the bars are comparable to each other and to the residual. */
  function wfRow(label, tip, delta, scale, extraCls) {
    const pct = (scale > 0 && delta) ? Math.max(2, Math.min(50, Math.abs(delta) / scale * 50)) : 0;
    const resid = extraCls === "resid";
    const barCls = resid ? "resid" : (delta > 0 ? "up" : delta < 0 ? "dn" : "");
    const figCls = resid ? "resid" : (delta ? fmt.cls(delta) : "zero");
    // DIRECTION IS INLINE, COLOUR IS THE CLASS. The stylesheet's .bar.up/.bar.dn carry both anchor and
    // colour, and .bar.resid carries alarm + a right-hand anchor; a red residual that FELL must still
    // grow leftwards, so the anchor is set here and the class is left to say what colour it is.
    const side = delta < 0 ? "right:50%;left:auto" : "left:50%;right:auto";
    return '<span class="lbl" title="' + fmt.esc(tip) + '">' + fmt.esc(label) + "</span>" +
      '<span class="track"><span class="zline"></span>' +
        (pct ? '<span class="bar ' + barCls + '" style="' + side + ';width:' + pct.toFixed(1) + '%"></span>' : "") +
      "</span>" +
      '<span class="fig ' + figCls + '">' + fmt.signed(delta) + "</span>";
  }

  function leverBlock(p) {
    const lv = p.levers;
    if (!lv || typeof lv !== "object") {
      return '<div class="awaiting"><b>Per-lever attribution</b> — this row carries no <span class="num">' +
        "levers</span> block, so no waterfall is drawn. Nothing is inferred in its place; the export " +
        "ships the field null for a row the attribution sidecar does not cover.</div>";
    }
    // every code the row carries, chain order first, then any code the map does not know (never dropped)
    const codes = LEVER_ORDER.filter(function (c) {
      return Object.prototype.hasOwnProperty.call(lv, c);
    }).concat(Object.keys(lv).filter(function (c) { return LEVER_ORDER.indexOf(c) < 0; }));
    if (!codes.length) {
      return '<div class="awaiting"><b>Per-lever attribution</b> — the <span class="num">levers</span> ' +
        "block on this row is empty. No bar is drawn from an empty block.</div>";
    }
    const sum = codes.reduce(function (s, c) { return s + (Number(lv[c]) || 0); }, 0);
    const from = p.vPrev;
    const to = MD.dispVal(p);
    const move = (from == null || to == null) ? null : (to - from);
    const residual = (move == null) ? null : (move - sum);
    const scale = Math.max.apply(null, codes.map(function (c) { return Math.abs(Number(lv[c]) || 0); })
      .concat([Math.abs(residual || 0), 1]));

    let rows = "";
    if (from != null) {
      rows += '<span class="totals">Last accepted bake</span><span></span>' +
        '<span class="totals" style="text-align:right"><b>' + fmt.n(from) + "</b></span>" +
        '<span class="rowline"></span>';
    }
    codes.forEach(function (c) {
      const meta = LEVER_LABEL[c] || { word: c, tip: c + " — no owner-facing name is on the record for this dial code; the code is shown rather than a guessed word." };
      rows += wfRow(meta.word, meta.tip, Number(lv[c]) || 0, scale);
    });
    if (residual != null) {
      rows += wfRow("Unattributed residual",
        "The part of this player's move the certified lever split does not account for. It is shown, " +
        "not absorbed: the waterfall's end figure must equal the displayed value.",
        residual, scale, "resid");
    }
    rows += '<span class="rowline"></span>' +
      '<span class="totals">Lands at</span><span></span>' +
      '<span class="totals" style="text-align:right"><b>' + fmt.n(to) + "</b></span>";

    let note = '<div class="note"><b>Order is the chain’s, not the size’s.</b> The split is ' +
      "path-additive along the certified order L1 → L4 → L2 → L3 → L5; a different " +
      "order would divide the same move differently, so these are not order-free per-lever facts. " +
      "A lever that contributed nothing prints as a zero line rather than being dropped.</div>";
    if (residual != null && from != null && Math.abs(residual) > Math.max(1, Math.abs(move) * 0.02)) {
      note += '<div class="awaiting"><b>The residual is real, and it is data, not rendering.</b> ' +
        "The lever deltas sum to <span class=\"num\">" + fmt.signed(sum) + "</span> but this player has " +
        "moved <span class=\"num\">" + fmt.signed(move) + "</span> since that bake, leaving " +
        "<span class=\"num\">" + fmt.signed(residual) + "</span> unattributed. The attribution sidecar " +
        "is frozen at its certification era and the board has advanced since, so everything the board " +
        "did after that certification lands here. An unreviewable move looks broken because it is.</div>";
    }
    return '<div class="wf">' + rows + "</div>" + note;
  }

  function waterfall(p) {
    // The owner-override line item (when present), then the per-lever waterfall. The grammar (green
    // right / red left, signed mono, residual in alarm red) is the CSS the panel was always built on.
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
    html += leverBlock(p);
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

  /* ================= v0 — THE ENTRY PRICE, AND WHAT HE IS WORTH AGAINST IT ========================
     Owner-commissioned 2026-08-21, and scoped by him in one line: "v0 of 3200, live rating of 4000,
     would mean +800 / 1.25x". Four figures — entry price · live rating · absolute gap · ratio — and a
     line saying WHICH entry price it is, because the two populations arrive at it differently and
     conflating them would be the quiet kind of wrong.

     NO RANK. See the note at the top of ui/app/v0.js: v0 is a slot value shared by every same-(future
     position, draft age, pick) player, so a rank over it would manufacture an order the model does not
     have. The card states the sharing in words instead, once, where it is cheapest to say honestly. */
  function v0Section(p) {
    const r = MD.v0.of(p);
    if (r.refused) {
      return '<div class="reserved"><b>Entry price not shown.</b> ' + fmt.esc(r.why) +
        " Nothing is shown in its place.</div>";
    }
    if (!r.has) {
      // an explicit, reasoned absence — the em-dash carries its why, never a bare dash
      return '<div class="statrow">' +
        '<div><div class="k">Entry price (v0)</div><div class="v num" title="' + fmt.esc(r.why || "") +
          '">—</div></div>' +
        '<div><div class="k">Live rating</div><div class="v volt num">' + fmt.n(r.live) + "</div></div>" +
        "</div>" +
        '<div class="note"><b>No entry price is recoverable for this player.</b> ' + fmt.esc(r.why || "") +
        " The em-dash is the finding, not a formatting choice — no anchor is invented to fill it.</div>";
    }
    const dCls = fmt.cls(r.delta);
    const rCls = r.ratio == null ? "na" : (r.ratio > 1 ? "up" : r.ratio < 1 ? "dn" : "flat");
    const shared = r.origin === "pick-slot"
      ? "<b>This figure is his draft slot's, not his own.</b> Every player who entered at the same " +
        "future position, draft age and pick number carries it to the dollar — measured on this board, " +
        "the eight pick-5 mids all sit at 2,218. It is what the model paid for the slot; the gap and " +
        "the ratio beside it are what he has done with it."
      : r.origin === "entry-anchor"
        ? "<b>He entered through the pool, so his entry price is his division's signed level</b> " +
          "(#326 entry anchors), not a pick slot. Same object — the price the model put on him the " +
          "moment he came in — arrived at the way the ruling says it must be for a pool entrant."
        : "";
    return '<div class="statrow">' +
        '<div><div class="k">Entry price (v0)</div><div class="v num" title="' +
          fmt.esc(MD.v0.originTip(r.origin)) + '">' + fmt.n(r.v0) +
          '<small> ' + fmt.esc(MD.v0.originWord(r.origin)) + "</small></div></div>" +
        '<div><div class="k">Live rating</div><div class="v volt num">' + fmt.n(r.live) + "</div></div>" +
        '<div><div class="k">vs entry</div><div class="v ' + dCls + ' num" title="' +
          fmt.esc("Live rating minus entry price. A difference of two given figures — nothing is re-valued.") +
          '">' + fmt.signed(r.delta) + "</div></div>" +
        '<div><div class="k">ratio</div><div class="v ' + rCls + ' num" title="' +
          fmt.esc("Live rating divided by entry price. 1.25x = worth a quarter more than he came in at.") +
          '">' + fmt.esc(MD.v0.ratioText(r.ratio)) + "</div></div>" +
      "</div>" +
      (shared ? '<div class="note">' + shared + "</div>" : "");
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
        '<h2 class="sec"><span>Worth now vs worth at entry</span><span class="meta">v0 · absolute · ratio</span></h2>' +
        v0Section(p) +
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
       · movement vs the previous round — CORRECTED 2026-08-21. What stood here said "the public bundle
         has always carried `dRound` … it now shows the real figure." It does not, and it never did.
         Measured on both shipped bundles: `dRound` 0/804 and `dRoundRank` 0/804, no production writer
         anywhere in engine/, tools/ or ui/tools/, and the key is absent from rl_export.py
         `player_rec()`'s row schema. This stat therefore prints "not published" — the honest state —
         and the movement the owner actually has lives on the Movers tab and in the weekly-history
         table further down this same card, both of which are real records. The claim above was a
         comment that outlived its truth and it drove a bridge in board.js on the same false premise;
         both are removed rather than left to be believed again.

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

    // item 18: round movement, read from `dRound` verbatim. Unfed on every row today (see the note
    // above) -> "not published", with the reason and the place the real record lives on hover.
    const dTxt = p.dRound == null ? "<small>not published</small>" : fmt.signed(p.dRound);
    const dCls = p.dRound == null ? "na" : fmt.cls(p.dRound);
    const dTitle = p.dRound == null
      ? "Previous-round movement is not published on this board — the dRound export field has no " +
        "writer, so nothing is invented here. His actual per-round record is the weekly history table " +
        "below, and the Movers tab."
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
