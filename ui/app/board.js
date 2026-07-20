/* Matchday UI — board view (working + public tiers). Pure view; no re-valuation. */
window.MD = window.MD || {};

MD.board = (function () {
  const fmt = MD.fmt;
  let onlyReads = false;
  // item 2 (team-context lens v1): filter the board to one AFFL club, and/or group by AFFL club with
  // per-club ΣSCAR totals. Display-only aggregation (a sum of given board figures, never a re-valuation).
  // The standalone AFFL club ranking PAGE is owner-deferred (2026-07-15 "build rest, defer page") — no
  // spec was locatable; the ranking *information* lives here inline (club headers ranked by ΣSCAR).
  let clubFilter = null;   // null == all AFFL clubs
  let groupByClub = false;
  let posFilter = null;    // item 5: null == all positions
  // item 178(2): the club-valuation asset filter — "players only" (default, current behaviour) vs
  // "picks included" (players + the club's held draft picks, priced off the canonical PVC by the ingest).
  // Issued picks appear ONLY here (owner law) — the +1/+2 placeholder players are untouched.
  let picksIncluded = false;

  /* item 178(2): a club's held-pick asset value (sum over the ingest's priced picks). 0 if the overlay
     is absent/halted or the club holds none. Never a re-valuation — a sum of the ingest's figures. */
  function clubPicksValue(afflTeamLong) {
    return MD.seam.picksFor(afflTeamLong).reduce(function (s, p) { return s + p.value; }, 0);
  }

  /* distinct position labels present, in football order (for the position filter). */
  function positions() {
    const order = { "Mid": 1, "Ruck": 2, "Key Fwd": 3, "Fwd": 4, "Key Def": 5, "Def": 6 };
    const set = {};
    (MD.seam.working.players || []).forEach(function (p) { if (p.pos) set[p.pos] = 1; });
    return Object.keys(set).sort(function (a, b) { return (order[a] || 99) - (order[b] || 99); });
  }

  /* AFFL clubs present in the working board, alphabetical (for the filter control). */
  function afflClubs() {
    const set = {};
    (MD.seam.working.players || []).forEach(function (p) { if (p.affl_team) set[p.affl_team] = 1; });
    return Object.keys(set).sort();
  }

  /* per-club aggregate over a row pool: ΣSCAR (sum of displayed values) + player count, ranked by ΣSCAR. */
  function clubAgg(pool) {
    const m = {};
    pool.forEach(function (r) {
      const c = r.p.affl_team || "—";
      if (!m[c]) m[c] = { club: c, sigma: 0, n: 0 };
      m[c].sigma += r.val; m[c].n += 1;
    });
    return Object.keys(m).map(function (k) { return m[k]; }).sort(function (a, b) { return b.sigma - a.sigma; });
  }

  /* players visible at the active lens, with the displayed value + rank. */
  function rows(tier) {
    const s = MD.state;
    const nowLens = s.lens === 2;
    let pool;
    if (tier === "public") {
      // public tier carries no `ov` (leak-proof), so MD.dispVal falls back to p.v here
      pool = (MD.seam.public.players || []).map(function (p) { return { p: p, val: MD.dispVal(p) }; });
    } else {
      const w = MD.seam.working;
      // now-lens: displayed value = the override figure (ov.dispv) when overridden, else v; ordering follows
      // this displayed value. Lens boards show the projected lens-year figure (the override is a now read).
      pool = (w.players || []).map(function (p) { return { p: p, val: nowLens ? MD.dispVal(p) : p.lens[s.lens] }; });
      if (!nowLens && s.lens < 2) {
        // backward-board-only players surface at −1 / −2
        (w.back || []).forEach(function (p) {
          const val = p.lens[s.lens];
          if (val !== null && val !== undefined) pool.push({ p: p, val: val, back: true });
        });
      }
    }
    pool = pool.filter(function (r) { return r.val !== null && r.val !== undefined; });
    // Pick-asset filter (owner ruling, register v16 item 14): the current board is a player ranking.
    // Exclude pick-asset rows on the current + backward lenses; picks stay at the +1/+2 lenses and on
    // the trade desk. Display-only — the underlying board is untouched.
    if (s.lens <= 2) {
      pool = pool.filter(function (r) { return !MD.isPickAsset(r.p); });
    }
    pool.sort(function (a, b) { return b.val - a.val; });
    pool.forEach(function (r, i) { r.rank = i + 1; });
    return pool;
  }

  function maxVal(pool) { return pool.length ? pool[0].val : 1; }

  /* item 2: a club group header — club name · rank · ΣSCAR total · player count. When picks are
     included (item 178(2)) the header carries the club's held-picks value and a players+picks total. */
  function clubHeader(c, rank) {
    const el = fmt.el("div", "clubhead");
    let html = '<span class="crank num">' + (rank || "—") + "</span>" +
      '<span class="cname">' + fmt.esc(fmt.club(c.club)) + "</span>";
    if (picksIncluded) {
      const pv = clubPicksValue(c.club);
      html += '<span class="csig num">Σ ' + fmt.n(c.sigma + pv) + ' <small>players+picks</small></span>' +
        '<span class="ccount num">' + fmt.n(c.sigma) + ' <small>P</small> · ' + fmt.n(pv) +
          ' <small>PK</small> · ' + fmt.n(c.n) + " pl</span>";
    } else {
      html += '<span class="csig num">Σ ' + fmt.n(c.sigma) + ' <small>SCAR</small></span>' +
        '<span class="ccount num">' + fmt.n(c.n) + " players</span>";
    }
    el.innerHTML = html;
    // v1.3 (item 196): the ranked club name gains the pocket profile on hover / focus / tap.
    const nmEl = el.querySelector(".cname");
    if (nmEl && MD.pocket && MD.pocket.has(c.club)) MD.pocket.attach(nmEl, c.club);
    return el;
  }

  /* item 2: a single-club context banner shown when the board is filtered to one AFFL club. */
  function clubBanner(c, rank, clubRanks) {
    const total = Object.keys(clubRanks).length;
    const el = fmt.el("div", "clubbanner");
    let html = '<span class="cbname">' + fmt.esc(fmt.club(c.club)) + "</span>" +
      '<span class="cbstat">club rank <b>' + (rank || "—") + "</b> of " + total + "</span>" +
      '<span class="cbstat">Σ players <b class="num">' + fmt.n(c.sigma) + "</b></span>" +
      '<span class="cbstat"><b class="num">' + fmt.n(c.n) + "</b> players</span>";
    if (picksIncluded) {
      const pv = clubPicksValue(c.club);
      const np = MD.seam.picksFor(c.club).length;
      html += '<span class="cbstat">Σ picks <b class="num">' + fmt.n(pv) + "</b> (" + np + ")</span>" +
        '<span class="cbstat cbtot">overall <b class="num">' + fmt.n(c.sigma + pv) + "</b></span>";
    }
    el.innerHTML = html;
    const cbnm = el.querySelector(".cbname");
    if (cbnm && MD.pocket && MD.pocket.has(c.club)) MD.pocket.attach(cbnm, c.club);
    return el;
  }

  /* item 178(2): the held-picks panel for a single filtered club — each pick listed with its band and
     its PVC-priced value (from the ingest). Rendered under the roster when "picks included" is on.
     item 194 (UI v1.2.1): display-only ordering + layout. Picks are sorted VALUE DESC (tie-break
     band-low ASC, then year ASC) and split into per-year columns (2026 | 2027), each column headed by
     its own Σ + pick count. The panel header keeps the overall Σ + total count. No value is re-priced —
     this re-orders and groups the ingest's own figures; the data bundle is untouched. */
  function pickOrder(a, b) {
    // value desc, then band-low asc, then year asc — a pure comparator over the ingest's figures.
    return (b.value - a.value) || (a.low - b.low) || (a.year - b.year);
  }

  function picksColumn(yr, yearPicks) {
    const col = fmt.el("div", "pickcol");
    const yTotal = yearPicks.reduce(function (s, p) { return s + p.value; }, 0);
    col.appendChild(fmt.el("div", "pickcolh",
      "<span>" + yr + "</span>" +
      '<span class="num">Σ ' + fmt.n(yTotal) + " · " + yearPicks.length + " pick" +
        (yearPicks.length === 1 ? "" : "s") + "</span>"));
    yearPicks.slice().sort(pickOrder).forEach(function (p) {
      const row = fmt.el("div", "pickrow");
      row.innerHTML =
        '<span class="pkband">' + fmt.esc(p.band) + "</span>" +
        '<span class="pkmeta">R' + p.round + " · from " + fmt.esc(fmt.club(p.origin)) + "</span>" +
        '<span class="pkval num">' + fmt.n(p.value) + "</span>";
      col.appendChild(row);
    });
    return col;
  }

  function picksPanel(afflTeamLong) {
    const picks = MD.seam.picksFor(afflTeamLong);
    const wrap = fmt.el("div", "pickspanel");
    const total = picks.reduce(function (s, p) { return s + p.value; }, 0);
    wrap.appendChild(fmt.el("div", "picksh",
      '<span>Held draft picks <small>priced off the canonical PVC · 2027 × 0.90 (balanced)</small></span>' +
      '<span class="num">Σ ' + fmt.n(total) + " · " + picks.length + " pick" + (picks.length === 1 ? "" : "s") + "</span>"));
    if (!picks.length) {
      wrap.appendChild(fmt.el("div", "picknone", "no held picks in the ledger"));
      return wrap;
    }
    const years = Object.keys(picks.reduce(function (m, p) { m[p.year] = 1; return m; }, {}))
      .map(Number).sort(function (a, b) { return a - b; });
    const cols = fmt.el("div", "pickcols");
    years.forEach(function (yr) {
      cols.appendChild(picksColumn(yr, picks.filter(function (p) { return p.year === yr; })));
    });
    wrap.appendChild(cols);
    return wrap;
  }

  /* item 4: a column-heading row, grid-aligned to the tier's row template (a label on every column). */
  function boardHead(tier) {
    const s = MD.state;
    const el = fmt.el("div", "rowhead " + tier);
    if (tier === "working") {
      const dh = s.lens !== 2 ? "Δ vs now" : (s.deltaBase === "bake" ? "Δ vs bake" : "Δ vs round");
      el.innerHTML =
        '<span class="h r">#</span><span class="h c">★</span><span class="h">Player</span>' +
        '<span class="h">Pos</span><span class="h">Club <small>AFFL · AFL</small></span>' +
        '<span class="h r">Value</span><span class="h">vs top</span>' +
        '<span class="h r">' + dh + '</span><span class="h r">Pick · Yr</span>';
    } else {
      el.innerHTML =
        '<span class="h r">#</span><span class="h">Player</span><span class="h">Pos</span>' +
        '<span class="h r">Value</span><span class="h">vs top</span><span class="h r">Movement</span>';
    }
    return el;
  }

  function deltaPill(p, displayedVal) {
    const s = MD.state;
    if (s.lens !== 2) {
      // lens board: Δ shown vs now (a diff of two given board figures, not a recomputation)
      const d = p.v == null ? null : displayedVal - p.v;
      return '<span class="pill ' + fmt.cls(d) + '" title="' + MD.config.LENS_LABELS[s.lens] +
        ' board value vs now">' + fmt.signed(d) + '</span>';
    }
    if (s.deltaBase === "bake") {
      if (p.vPrev == null) {
        return '<span class="pill na" title="Δ vs last accepted bake — column built, awaiting the vPrev ' +
          'export field (§7.3; one-line engine-side addition). No Δ is invented.">—</span>';
      }
      return '<span class="pill ' + fmt.cls(p.v - p.vPrev) + '" title="Δ vs last accepted bake">' +
        fmt.signed(p.v - p.vPrev) + '</span>';
    }
    // round
    if (p.dRound == null) {
      return '<span class="pill na" title="Δ vs previous round — arrives with the weekly loop (Phase 3).">—</span>';
    }
    return '<span class="pill ' + fmt.cls(p.dRound) + '">' + fmt.signed(p.dRound) + "</span>";
  }

  function workingRow(r, maxV, byKey) {
    const p = r.p;
    const anc = MD.anchorStatus(p.key, byKey);
    let pin = '<span class="pin"></span>';
    if (anc) {
      pin = '<span class="pin ' + (anc.status === "met" ? "pinf" : "pinh") + '" title="Your read: ' +
        fmt.esc(anc.read) + " — " + (anc.status === "met" ? "met" : "watching") +
        (anc.verified ? " (verified on the board)" : "") + '">★</span>';
    }
    let nm = '<span class="nm">' + fmt.esc(p.name);
    if (p.owner_rule) {
      nm += '<span class="tag" title="Owner override active — the owner\'s rule, not the model\'s curve, ' +
        'is holding this number. Post-override figure shown. ' +
        (p.vRaw != null ? "Model pre-override: " + fmt.n(p.vRaw) + "."
          : "Model pre-override figure arrives with the vRaw export field (§7.3).") +
        '">Owner override</span>';
    }
    if (MD.state.slugs) nm += '<span class="slug">' + fmt.esc(p.key) + "</span>";
    nm += "</span>";
    const b = fmt.el("button", "row working");
    b.innerHTML =
      '<span class="rank num">' + r.rank + "</span>" + pin + nm +
      '<span class="pos">' + fmt.esc(p.pos) + "</span>" +
      // item 1: AFL club + AFFL club, listed per player (AFFL is the team-context lens focus, so it leads
      // in volt; AFL is the muted sub-line). Display-only strings from the bundle; "—" when absent.
      '<span class="club"><span class="affl" title="AFFL club">' + fmt.esc(fmt.club(p.affl_team)) + "</span>" +
        '<span class="afl" title="AFL club">' + fmt.esc(p.afl_club || "—") + "</span></span>" +
      '<span class="val num">' + fmt.n(r.val) + "</span>" +
      MD.valueLine(r.val, maxV) +
      deltaPill(p, r.val) +
      '<span class="meta">' + (p.pk ? "pk " + p.pk : "—") + " · ’" + String(p.yr || "").slice(2) + "</span>";
    b.addEventListener("click", function () { MD.go("card", p.key); });
    return b;
  }

  function publicRow(r, maxV) {
    const p = r.p;
    // item 7 (de-clunk): ONE movement instance, correctly aligned. The old row emitted two "steady"
    // pills (value-move + rank-move) into a 6-column grid, so the seventh cell wrapped under the name —
    // the duplicated "steady" the owner flagged. Collapsed to a single movement-vs-previous-round pill
    // (rank movement rides its tooltip); the row now emits exactly its grid's columns.
    const move = p.dRound == null
      ? '<span class="pill flat" title="Movement vs previous round — value and rank both publish with the ' +
        'weekly loop (Phase 3). Nothing fake shown until then.">— steady</span>'
      : '<span class="pill ' + fmt.cls(p.dRound) + '" title="movement vs previous round">' + fmt.signed(p.dRound) + "</span>";
    const b = fmt.el("button", "row public");
    b.innerHTML =
      '<span class="rank num">' + r.rank + "</span>" +
      '<span class="nm">' + fmt.esc(p.name) + "</span>" +
      '<span class="pos">' + fmt.esc(p.pos) + "</span>" +
      '<span class="val num">' + fmt.n(r.val) + "</span>" +
      MD.valueLine(r.val, maxV) + move;
    return b;
  }

  function strip(container) {
    const s = MD.state;
    const wrap = fmt.el("div", "strip");
    const st = MD.seam.working.stamp || {};
    const yr = st.baseYear || 2026;
    // Round label from the durable metadata contract (asOfRound); neutral "Round —" when unset —
    // never the old hardcoded "Round 17". MD.roundLabel is defined in main.js (loaded last); this runs
    // only at render time, so it is always resolved. Guarded for safety.
    const roundLbl = MD.roundLabel ? MD.roundLabel(st) : (st.asOfRound != null ? "Round " + st.asOfRound : "Round —");
    wrap.innerHTML = '<span class="lbl">' + roundLbl + " · " + yr + (s.tier === "public" ? " · published" : "") + "</span>";
    wrap.appendChild(fmt.el("span", "spacer"));

    // ±1/2-yr board lens (both tiers meaningful for value-by-year, but kept working-only per two-tier trim)
    if (s.tier === "working") {
      wrap.appendChild(fmt.el("span", "lbl", "Board lens"));
      const lens = fmt.el("div", "seg lens");
      MD.config.LENS_LABELS.forEach(function (lab, i) {
        // LEG E (SPEC §3): the +1/+2 forward-lens toggle is RE-ENABLED. The projection law (R103.3) has
        // landed — the forward lens now credits EXPECTED production (age+k through the map's own growth
        // curve; engine: rl_export _LENS_FORM + _merged_recover b6/price6 form-anchor). The ruled
        // no-improvement-floor defect (register v46) is retired with the interim lens (lens_tilt).
        // −2/−1/Now stay the real backward re-values + now; +1/+2 are the live projection lenses.
        const btn = fmt.el("button", i === s.lens ? "on" : "", lab);
        btn.addEventListener("click", function () { s.lens = i; render(container); });
        lens.appendChild(btn);
      });
      wrap.appendChild(lens);

      // Q-DELTA-BASE toggle (built; default = bake). Dimmed on a non-now lens (does not apply).
      wrap.appendChild(fmt.el("span", "lbl", "Δ base"));
      const dseg = fmt.el("div", "seg");
      [["bake", "bake"], ["round", "round"]].forEach(function (pair) {
        const btn = fmt.el("button", s.deltaBase === pair[0] ? "on" : "", pair[1]);
        if (s.lens !== 2) { btn.disabled = true; btn.style.opacity = ".4"; btn.style.cursor = "default"; }
        else btn.addEventListener("click", function () { s.deltaBase = pair[0]; render(container); });
        dseg.appendChild(btn);
      });
      wrap.appendChild(dseg);
      if (s.lens === 2) {
        const anyPrev = (MD.seam.working.players || []).some(function (p) {
          return s.deltaBase === "bake" ? p.vPrev != null : p.dRound != null;
        });
        if (!anyPrev) {
          const note = fmt.el("span", "lbl");
          note.style.color = "var(--faint)";
          note.style.letterSpacing = ".04em";
          note.style.textTransform = "none";
          note.textContent = s.deltaBase === "bake"
            ? "· Δ column built — awaiting the one-line vPrev bake export (§7.3); no Δ invented"
            : "· Δ vs round arrives with the weekly loop (Phase 3)";
          wrap.appendChild(note);
        }
      }

      // My reads filter
      wrap.appendChild(fmt.el("span", "lbl", "Filter"));
      const rseg = fmt.el("div", "seg");
      [["all", "all"], ["reads", "my reads"]].forEach(function (pair) {
        const on = (pair[0] === "reads") === onlyReads;
        const btn = fmt.el("button", on ? "on" : "", pair[1]);
        btn.addEventListener("click", function () { onlyReads = pair[0] === "reads"; render(container); });
        rseg.appendChild(btn);
      });
      wrap.appendChild(rseg);

      // item 5: filter by position.
      wrap.appendChild(fmt.el("span", "lbl", "Position"));
      const psel = document.createElement("select");
      psel.className = "boardsel";
      psel.innerHTML = '<option value="">all positions</option>' +
        positions().map(function (pp) {
          return '<option value="' + fmt.esc(pp) + '"' + (posFilter === pp ? " selected" : "") + ">" +
            fmt.esc(pp) + "</option>";
        }).join("");
      psel.addEventListener("change", function () { posFilter = psel.value || null; render(container); });
      wrap.appendChild(psel);

      // item 2: team-context lens — filter to one AFFL club + group-by-club (ΣSCAR totals).
      wrap.appendChild(fmt.el("span", "lbl", "Team lens"));
      const csel = document.createElement("select");
      csel.className = "boardsel";
      csel.innerHTML = '<option value="">all AFFL clubs</option>' +
        afflClubs().map(function (c) {
          // value = the raw affl_team (join key); label = the shortened display name (item 178(1)).
          return '<option value="' + fmt.esc(c) + '"' + (clubFilter === c ? " selected" : "") + ">" +
            fmt.esc(fmt.club(c)) + "</option>";
        }).join("");
      csel.addEventListener("change", function () { clubFilter = csel.value || null; render(container); });
      wrap.appendChild(csel);
      const gseg = fmt.el("div", "seg");
      [["off", "group off"], ["on", "by club"]].forEach(function (pair) {
        const on = (pair[0] === "on") === groupByClub;
        const btn = fmt.el("button", on ? "on" : "", pair[1]);
        btn.addEventListener("click", function () { groupByClub = pair[0] === "on"; render(container); });
        gseg.appendChild(btn);
      });
      wrap.appendChild(gseg);

      // item 178(2): players-only / picks-included asset filter (halt-aware).
      wrap.appendChild(fmt.el("span", "lbl", "Assets"));
      const halted = MD.seam.clubHalt();
      const aseg = fmt.el("div", "seg assets");
      [["players", "players only"], ["picks", "picks included"]].forEach(function (pair) {
        const on = (pair[0] === "picks") === picksIncluded;
        const btn = fmt.el("button", on ? "on" : "", pair[1]);
        if (pair[0] === "picks" && halted) {
          btn.disabled = true; btn.classList.add("lensoff");
          btn.title = "Picks overlay HALTED by the ingest — " + fmt.esc(halted.reason);
        } else {
          btn.addEventListener("click", function () { picksIncluded = pair[0] === "picks"; render(container); });
        }
        aseg.appendChild(btn);
      });
      wrap.appendChild(aseg);

      // Debug slugs
      wrap.appendChild(fmt.el("span", "lbl", "Debug"));
      const dbg = fmt.el("div", "seg dbg");
      [["off", "slugs off"], ["on", "on"]].forEach(function (pair) {
        const on = (pair[0] === "on") === s.slugs;
        const btn = fmt.el("button", on ? "on" : "", pair[1]);
        btn.addEventListener("click", function () { s.slugs = pair[0] === "on"; render(container); });
        dbg.appendChild(btn);
      });
      wrap.appendChild(dbg);
    }
    container.appendChild(wrap);
  }

  // ==== LEG F1 — PHANTOM INTAKE (+1/+2) + RETROSPECTIVE (−1/−2) VIEW LAW (MEMO_LEGF §4) ==================
  // Pure view; reads the board's additive phantom keys (present only on an RL_LEGF=1 board) and F2's
  // retrospective bundle. EMPTY-STATE SAFE: an RL_LEGF=0 board carries no phantom keys => nothing renders;
  // F2 not landed => the −1/−2 tab shows a pending note over the engine backward re-value. k=0 shows NONE.
  function phantomTotals() { return (MD.seam.working && MD.seam.working.phantomTotals) || null; }
  // F2 injects its stamped retrospective boards like the club overlay: window.__MATCHDAY_RETRO__ =
  // { "-1": {board, stamp}, "-2": {board, stamp} }. The real F2 artifact stamps its SOURCE STORE and its
  // BALANCED-BOARD reference (store_md5 / balanced_board_md5) — NOT the final post-Leg-F working-board
  // md5 — so we authenticate the retro against THOSE two provenance identities, independently, and name
  // the field that fails. No hardcoded fallback (the audit's stale-id hazard). balanced_board_md5 is set
  // only at the final bake; until the installed working board carries it the contract cannot be
  // authenticated, so the tab stays PENDING (never ok, never a guessed id).
  function retroFor(lensIdx) {
    const rb = window.__MATCHDAY_RETRO__ || null;
    if (!rb) return { state: "pending" };
    const entry = rb[lensIdx === 0 ? "-2" : "-1"];
    if (!entry) return { state: "pending" };
    const wst = ((MD.seam.working || {}).stamp) || {};
    const est = (entry.stamp || {});
    if (wst.balanced_board_md5 == null) return { state: "pending" };
    const checks = [
      { field: "store_md5", want: wst.store_md5, got: est.store_md5 },
      { field: "balanced_board_md5", want: wst.balanced_board_md5, got: est.balanced_board_md5 },
    ];
    for (let i = 0; i < checks.length; i++) {
      const want = String(checks[i].want || "").slice(0, 8);
      const got = String(checks[i].got || "").slice(0, 8);
      if (!want || got !== want) return { state: "mismatch", field: checks[i].field, got: got, want: want };
    }
    return { state: "ok", entry: entry };
  }
  function phantomBanner(container) {
    const s = MD.state;
    const money = function (n) { return (n < 0 ? "−" : "+") + Math.abs(Math.round(n)).toLocaleString(); };
    const banner = function (bg, html) {
      const el = fmt.el("div", "phantombanner");
      el.style.cssText = "margin:.35rem 0;padding:.4rem .6rem;border-left:3px solid " + bg +
        ";background:rgba(127,127,127,.08);font-size:.82rem;line-height:1.5";
      el.innerHTML = html; container.appendChild(el); return el;
    };
    const tag = function (txt, bg) {
      return '<span style="display:inline-block;padding:.02rem .3rem;margin-right:.4rem;border-radius:.2rem;' +
        'background:' + bg + ';color:#fff;font-size:.72rem;font-weight:600;letter-spacing:.02em">' + fmt.esc(txt) + '</span>';
    };
    // −1/−2: F2 retrospective board tab (empty-state safe)
    if (s.lens === 0 || s.lens === 1) {
      const r = retroFor(s.lens);
      if (r.state === "ok") return;   // F2 board present + stamp-asserted; row pipeline renders it (future wiring)
      banner("#c98a1a", r.state === "mismatch"
        ? tag("retrospective F2 · STAMP MISMATCH", "#b23") + "got " + fmt.esc(r.got) + " want " + fmt.esc(r.want) +
          " — showing the engine backward re-value"
        : tag("retrospective F2 · pending", "#8a7") + "the " + MD.config.LENS_LABELS[s.lens] +
          " tab reads F2’s stamped artifact when it lands; showing the engine backward re-value meanwhile");
      return;
    }
    // +1/+2: phantom intake layer
    if (s.lens === 3 || s.lens === 4) {
      const pt = phantomTotals(); if (!pt) return;   // RL_LEGF=0 board => no phantom keys => empty-state
      const lk = String(s.lens - 2);                 // lens 3 -> "1", 4 -> "2"
      const lg = pt.league[lk]; if (!lg) return;
      // LEG F5 §2.viii: the entrant LAYER (full sealed annual intake at PVC). Supersedes F1's exits/R/X
      // strawman fields (retired) — banner now shows the sealed entrant layer size + slot structure.
      const em = pt._meta || {};
      const el = banner("#3a7", tag("entrant layer · " + MD.config.LENS_LABELS[s.lens], "#2a6") +
        "league <b>WITH</b> Σ" + Math.round(lg.withPhantom).toLocaleString() +
        " vs <b>WITHOUT</b> Σ" + Math.round(lg.withoutPhantom).toLocaleString() +
        " (Δ " + money(lg.delta) + ") · entrant layer Σ" +
        Math.round(em.entrant_layer_pvc || lg.entrantValue || lg.delta).toLocaleString() +
        " PVC (" + (em.expected_slots_per_year != null ? em.expected_slots_per_year + " slots/yr" : "sealed intake") +
        ') · <span style="opacity:.6">report-only · k=0 phantom=none · §2.viii seal ' +
        fmt.esc(em.seal_sha256_8 || "") + "</span>");
      const tbl = fmt.el("div", "phantomclubs");
      tbl.style.cssText = "margin-top:.35rem;display:grid;grid-template-columns:repeat(auto-fill,minmax(15rem,1fr));gap:.15rem .8rem";
      Object.keys(pt.clubs).sort().forEach(function (c) {
        const row = pt.clubs[c][lk]; if (!row) return;
        const seg = fmt.el("div", "pcrow");
        seg.style.cssText = "display:flex;justify-content:space-between;gap:.5rem;font-size:.78rem";
        seg.innerHTML = '<span>' + fmt.esc(c) + "</span>" +
          '<span style="opacity:.8">Σ' + Math.round(row.withPhantom).toLocaleString() + "</span>" +
          '<span style="color:' + (row.delta >= 0 ? "#3a7" : "#b23") + '">' + money(row.delta) + "</span>" +
          tag("phantom", "#2a6");
        tbl.appendChild(seg);
      });
      el.appendChild(tbl);
    }
  }

  function render(container) {
    container.innerHTML = "";
    const s = MD.state;
    strip(container);
    if (s.tier === "working") phantomBanner(container);   // LEG F1: phantom (+1/+2) / retrospective (−1/−2) view, empty-state safe

    const byKey = MD.seam.indexed().byKey;
    let pool = rows(s.tier);
    const maxV = maxVal(pool);              // global board top (share-of-top-price reference), pre-filter
    if (s.tier === "working" && onlyReads) {
      pool = pool.filter(function (r) { return MD.anchors[r.p.key]; });
    }
    // item 5: position filter (applies before club aggregation, so ΣSCAR/ranks respect the active
    // position lens — e.g. "which club has the strongest mids").
    if (s.tier === "working" && posFilter) {
      pool = pool.filter(function (r) { return r.p.pos === posFilter; });
    }

    // item 2: canonical club ranking (ΣSCAR over the full unfiltered pool) — used for club-rank badges.
    const clubRanks = {};
    if (s.tier === "working") clubAgg(pool).forEach(function (c, i) { clubRanks[c.club] = i + 1; });

    // item 2: filter to a single AFFL club (working tier).
    if (s.tier === "working" && clubFilter) {
      pool = pool.filter(function (r) { return (r.p.affl_team || "—") === clubFilter; });
      const ca = clubAgg(pool)[0];
      if (ca) container.appendChild(clubBanner(ca, clubRanks[clubFilter], clubRanks));
    }

    if (pool.length) container.appendChild(boardHead(s.tier)); // item 4: column headings
    const rowsEl = fmt.el("div", "rows");
    if (s.tier === "working" && groupByClub) {
      // grouped: club headers ranked by ΣSCAR, each with its top players — the team-context lens (inline
      // club ranking; the standalone page is owner-deferred).
      clubAgg(pool).forEach(function (c) {
        rowsEl.appendChild(clubHeader(c, clubRanks[c.club]));
        const mine = pool.filter(function (r) { return (r.p.affl_team || "—") === c.club; }).slice(0, 6);
        mine.forEach(function (r) { rowsEl.appendChild(workingRow(r, maxV, byKey)); });
        const more = c.n - mine.length;
        if (more > 0) rowsEl.appendChild(fmt.el("div", "clubmore", "+ " + fmt.n(more) + " more " +
          fmt.esc(fmt.club(c.club)) + " player" + (more === 1 ? "" : "s")));
      });
    } else {
      pool.slice(0, clubFilter ? pool.length : 60).forEach(function (r) {
        rowsEl.appendChild(s.tier === "working" ? workingRow(r, maxV, byKey) : publicRow(r, maxV));
      });
    }
    // item 178(2): a single filtered club with "picks included" lists its held picks under the roster.
    if (s.tier === "working" && clubFilter && picksIncluded && !MD.seam.clubHalt()) {
      rowsEl.appendChild(picksPanel(clubFilter));
    }
    container.appendChild(rowsEl);

    const foot = fmt.el("footer", "foot");
    if (s.tier === "working") {
      const shown = groupByClub ? "grouped by AFFL club" :
        (pool.length > 60 ? "showing top 60 of " + fmt.n(pool.length) : "showing all " + fmt.n(pool.length));
      foot.innerHTML = "volt = your touch (reads · rules · controls) · the value line = share of the top price, its colour warming as it fills · " +
        "movement pills always signed · override headroom lives on the card's waterfall · " + shown +
        (s.lens !== 2 ? " at the " + MD.config.LENS_LABELS[s.lens] + " lens" : "");
    } else {
      foot.innerHTML = "the value line = share of the top price, its colour warming as it fills · movement pills always signed, never colour alone · public trim — no ids, no internals";
    }
    container.appendChild(foot);
  }

  /* item 178(3): the team-summary page links a club row into its filtered board view. Sets the
     team-lens filter (and turns picks on) before the router switches to the board. */
  function focusClub(afflTeamLong, withPicks) {
    clubFilter = afflTeamLong || null;
    groupByClub = false;
    if (withPicks && !MD.seam.clubHalt()) picksIncluded = true;
  }

  // retroFor exposed so the release-seam test can exercise the EXACT retrospective identity check
  // the UI runs (same doctrine as counting.js). Pure view; reads no DOM.
  return { render: render, focusClub: focusClub, retroFor: retroFor };
})();
