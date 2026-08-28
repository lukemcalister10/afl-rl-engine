/* Matchday UI — the rankings board. Pure view; no re-valuation.

   REDESIGNED 2026-08-28 ON THE OWNER'S WORD: the app is the owner's product surface. Process,
   provenance and modelling chrome (tier splits, guard badges, lens machinery, delta bases, debug
   slugs, reads/stars, the phantom/reconciliation panels) are GONE from this surface — what they
   verified still runs underneath (the seam ring-fence fail-closes the page), it just never
   decorates the screen. The record of what was removed and why lives in ui/MAINTAINER.md.

   What renders: one transparent board — rank · player · position · clubs · value · share-of-top ·
   ROUND CHANGE (this round vs the round before, from the weekly report) · draft pick/year — with
   the filters that answer the owner's questions (position, eligibility, cohort, age, club). A club
   view opens with the club profile, the roster, and ALWAYS the club's held picks. */
window.MD = window.MD || {};

MD.board = (function () {
  const fmt = MD.fmt;
  let clubFilter = null;   // null == all AFFL clubs
  let posFilter = null;
  let cohortFilter = null;
  let ageFilter = null;
  let eligFilter = null;

  /* Cohort clock (owner's stated grouping, store-verified): the intake that first takes the field
     together, labelled by its national-draft year — MSD rows belong to the year before theirs. */
  function cohortYear(p) {
    if (!p || p.yr == null) return null;
    return p.ty === "MSD" ? (p.yr - 1) : p.yr;
  }
  function cohortYears() {
    const set = {};
    (MD.seam.working.players || []).forEach(function (p) {
      const c = cohortYear(p); if (c != null) set[c] = 1;
    });
    return Object.keys(set).map(Number).sort(function (a, b) { return b - a; });
  }

  function ages() {
    const set = {};
    (MD.seam.working.players || []).forEach(function (p) { if (p.age != null) set[p.age] = 1; });
    return Object.keys(set).map(Number).sort(function (a, b) { return a - b; });
  }
  const AGE_BANDS = [
    { id: "b:-20", label: "20 and under", lo: 0, hi: 20 },
    { id: "b:21-24", label: "21–24", lo: 21, hi: 24 },
    { id: "b:25-28", label: "25–28", lo: 25, hi: 28 },
    { id: "b:29-", label: "29 and over", lo: 29, hi: 999 },
  ];
  function ageMatches(p, sel) {
    if (!sel) return true;
    if (p.age == null) return false;
    if (sel.indexOf("b:") === 0) {
      const band = AGE_BANDS.filter(function (b) { return b.id === sel; })[0];
      return !!band && p.age >= band.lo && p.age <= band.hi;
    }
    return String(p.age) === String(sel);
  }

  const ELIG_LABELS = { KPD: "Key Def", SD: "Gen Def", MID: "Mid", SF: "Gen Fwd", KPF: "Key Fwd", RUCK: "Ruck" };
  const ELIG_ORDER = ["MID", "RUCK", "KPF", "SF", "KPD", "SD"];
  function eligCodes() {
    const set = {};
    (MD.seam.working.players || []).forEach(function (p) {
      (p.elig || []).forEach(function (c) { if (c) set[c] = 1; });
    });
    return Object.keys(set).sort(function (a, b) {
      const ia = ELIG_ORDER.indexOf(a), ib = ELIG_ORDER.indexOf(b);
      return (ia < 0 ? 99 : ia) - (ib < 0 ? 99 : ib);
    });
  }
  function eligMatches(p, code) {
    if (!code) return true;
    return (p.elig || []).indexOf(code) !== -1;
  }

  function positions() {
    const order = { "Mid": 1, "Ruck": 2, "Key Fwd": 3, "Fwd": 4, "Key Def": 5, "Def": 6 };
    const set = {};
    (MD.seam.working.players || []).forEach(function (p) { if (p.pos) set[p.pos] = 1; });
    return Object.keys(set).sort(function (a, b) { return (order[a] || 99) - (order[b] || 99); });
  }

  function afflClubs() {
    const set = {};
    (MD.seam.working.players || []).forEach(function (p) {
      const c = MD.canonClub(MD.ownership.clubOf(p)); if (c) set[c] = 1;
    });
    return Object.keys(set).sort();
  }

  /* ---- ROUND CHANGE — this round's move per player, from the weekly report of record ----------
     The latest committed weekly report carries every player's value_change for the round (current
     vs previous round at that round's apply). Model changes between rounds are NOT smeared into
     this number — they appear in the player's history as their own "Model change" lines. */
  let _rd;   // undefined = unbuilt; null = no report; object = key -> {d, prev, cur, round}
  function roundDeltas() {
    if (_rd !== undefined) return _rd;
    _rd = null;
    const mv = window.__MATCHDAY_MOVERS__ || null;
    const rounds = (mv && mv.rounds) || [];
    if (!mv || !rounds.length) return _rd;
    const rep = (mv.reports || {})[String(rounds[rounds.length - 1])];
    if (!rep || !rep.players) return _rd;
    // The report names its round as submitted_round (older fixtures: current_round) and its baseline
    // as the immediately-preceding POINT, which can be a model-change id. The football pair the pill
    // names is round vs previous ROUND — the model changes between them are their own history lines.
    const cur = rep.submitted_round != null ? rep.submitted_round : rep.current_round;
    const priorRounds = rounds.map(Number).filter(function (n) { return !isNaN(n) && n < Number(cur); });
    const prev = priorRounds.length ? Math.max.apply(null, priorRounds) : rep.previous_round;
    _rd = { _round: cur, _prev: prev };
    rep.players.forEach(function (r) {
      if (r.key) _rd[r.key] = { d: r.value_change, prev: r.prev_value, cur: r.cur_value };
    });
    return _rd;
  }
  function roundDeltaPill(p) {
    const rd = roundDeltas();
    const r = rd && rd[p.key];
    if (!r || r.d == null) return '<span class="pill na">—</span>';
    return '<span class="pill ' + fmt.cls(r.d) + '" title="Round ' + rd._round + " vs Round " +
      rd._prev + '">' + fmt.signed(r.d) + "</span>";
  }

  /* per-club aggregate over the visible pool (for the single-club banner rank). */
  function clubAgg(pool) {
    const m = {};
    pool.forEach(function (r) {
      const c = MD.canonClub(MD.ownership.clubOf(r.p)) || "—";
      if (!m[c]) m[c] = { club: c, sigma: 0, n: 0 };
      m[c].sigma += r.val; m[c].n += 1;
    });
    return Object.keys(m).map(function (k) { return m[k]; }).sort(function (a, b) { return b.sigma - a.sigma; });
  }

  function rows() {
    const w = MD.seam.working;
    const pool = (w.players || [])
      .map(function (p) { return { p: p, val: MD.dispVal(p) }; })
      .filter(function (r) { return r.val !== null && r.val !== undefined && !MD.isPickAsset(r.p); });
    pool.sort(function (a, b) { return b.val - a.val; });
    pool.forEach(function (r, i) { r.rank = i + 1; });
    return pool;
  }

  function maxVal(pool) { return pool.length ? pool[0].val : 1; }

  /* The club profile that heads a single-club view — the Clubs page's own metrics, one computation
     shared across surfaces (MD.clubTotals). */
  const SUMMARY_METRICS = [
    { key: "overall", label: "Rating" },
    { key: "totalPlayer", label: "Player value" },
    { key: "totalPicks", label: "Picks value" },
    { key: "top5", label: "Top-5" },
    { key: "top10", label: "Top-10" },
    { key: "best23", label: "Best-23" },
    { key: "nonBest23", label: "Depth" },
  ];

  function clubSummary(teamLong) {
    const ct = MD.clubTotals.compute();
    if (!ct) return null;
    const c = MD.clubTotals.byTeam(teamLong);
    if (!c) return null;
    const el = fmt.el("div", "clubsummary");
    let cells = "";
    SUMMARY_METRICS.forEach(function (m) {
      const na = !ct.picksAvailable && (m.key === "totalPicks" || m.key === "overall");
      const rank = na ? null : MD.clubTotals.rankOf(c.team, m.key);
      cells +=
        '<div class="csm">' +
          '<div class="csm-k">' + fmt.esc(m.label) + "</div>" +
          '<div class="csm-v num">' + (na ? "<small>n/a</small>" : fmt.n(c[m.key])) + "</div>" +
          '<div class="csm-r">' + (rank ? "rank " + rank + "</div>" : "—</div>") +
        "</div>";
    });
    el.innerHTML =
      '<div class="csm-head"><span class="csm-name">' + fmt.esc(c.display || fmt.club(c.team)) + "</span>" +
        '<span class="csm-sub">' + fmt.n(c.nRoster) + " players · " +
        (ct.picksAvailable ? fmt.n(c.nPicks) + " picks" : "picks unavailable") + "</span></div>" +
      '<div class="csm-grid">' + cells + "</div>";
    return el;
  }

  /* Held picks for a club — ALWAYS shown on a club view. Sorted value desc within per-year columns. */
  function pickOrder(a, b) {
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
      '<span>Held draft picks <small>2026 full band · 2027 ½ band + ½ round avg · 2028 round avg · R5 = 0</small></span>' +
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

  function boardHead() {
    const el = fmt.el("div", "rowhead working");
    el.innerHTML =
      '<span class="h r">#</span><span class="h">Player</span>' +
      '<span class="h">Pos</span><span class="h">Club <small>AFFL · AFL</small></span>' +
      '<span class="h r">Value</span><span class="h">vs top</span>' +
      '<span class="h r">Round Δ</span>' +
      '<span class="h r">Pick · Yr</span>';
    return el;
  }

  function workingRow(r, maxV) {
    const p = r.p;
    const b = fmt.el("button", "row working");
    b.innerHTML =
      '<span class="rank num">' + r.rank + "</span>" +
      '<span class="nm">' + fmt.esc(p.name) + "</span>" +
      '<span class="pos">' + fmt.esc(p.pos) + "</span>" +
      '<span class="club"><span class="affl">' + fmt.esc(MD.ownership.labelOf(p)) + "</span>" +
        '<span class="afl">' + fmt.esc(p.afl_club || "—") + "</span></span>" +
      '<span class="val num">' + fmt.n(r.val) + "</span>" +
      MD.valueLine(r.val, maxV) +
      roundDeltaPill(p) +
      '<span class="meta">' + (p.pk ? "pk " + p.pk : "—") + " · ’" + String(p.yr || "").slice(2) + "</span>";
    b.addEventListener("click", function () { MD.go("card", p.key); });
    return b;
  }

  /* The filter bar — one quiet row of selects. */
  function strip(container) {
    const wrap = fmt.el("div", "strip");
    const st = MD.seam.working.stamp || {};
    const roundLbl = MD.roundLabel ? MD.roundLabel(st) : "Round " + (st.asOfRound || "—");
    wrap.innerHTML = '<span class="lbl">' + roundLbl + " · " + (st.baseYear || 2026) + "</span>";
    wrap.appendChild(fmt.el("span", "spacer"));

    function sel(label, options, current, onChange) {
      wrap.appendChild(fmt.el("span", "lbl", label));
      const s = document.createElement("select");
      s.className = "boardsel";
      s.innerHTML = options;
      s.addEventListener("change", function () { onChange(s.value || null); render(container); });
      wrap.appendChild(s);
      return s;
    }

    sel("Position",
      '<option value="">all</option>' + positions().map(function (pp) {
        return '<option value="' + fmt.esc(pp) + '"' + (posFilter === pp ? " selected" : "") + ">" + fmt.esc(pp) + "</option>";
      }).join(""), posFilter, function (v) { posFilter = v; });

    const eligOpts = eligCodes();
    if (eligOpts.length) {
      sel("Eligible",
        '<option value="">any</option>' + eligOpts.map(function (c) {
          return '<option value="' + fmt.esc(c) + '"' + (eligFilter === c ? " selected" : "") + ">" +
            fmt.esc(ELIG_LABELS[c] || c) + "</option>";
        }).join(""), eligFilter, function (v) { eligFilter = v; });
    }

    const cohorts = cohortYears();
    if (cohorts.length) {
      sel("Cohort",
        '<option value="">all</option>' + cohorts.map(function (y) {
          return '<option value="' + y + '"' + (String(cohortFilter) === String(y) ? " selected" : "") + ">" + y + "</option>";
        }).join(""), cohortFilter, function (v) { cohortFilter = v; });
    }

    const ageOpts = ages();
    if (ageOpts.length) {
      sel("Age",
        '<option value="">all</option>' +
        AGE_BANDS.map(function (b) {
          return '<option value="' + b.id + '"' + (ageFilter === b.id ? " selected" : "") + ">" + fmt.esc(b.label) + "</option>";
        }).join("") +
        ageOpts.map(function (a) {
          return '<option value="' + a + '"' + (String(ageFilter) === String(a) ? " selected" : "") + ">" + a + "</option>";
        }).join(""), ageFilter, function (v) { ageFilter = v; });
    }

    sel("Club",
      '<option value="">all clubs</option>' + afflClubs().map(function (c) {
        return '<option value="' + fmt.esc(c) + '"' + (clubFilter === c ? " selected" : "") + ">" +
          fmt.esc(fmt.club(c)) + "</option>";
      }).join(""), clubFilter, function (v) { clubFilter = v; });

    container.appendChild(wrap);
  }

  function render(container) {
    container.innerHTML = "";
    strip(container);

    let pool = rows();
    const maxV = maxVal(pool);
    if (posFilter) pool = pool.filter(function (r) { return r.p.pos === posFilter; });
    if (eligFilter) pool = pool.filter(function (r) { return eligMatches(r.p, eligFilter); });
    if (cohortFilter) pool = pool.filter(function (r) { return String(cohortYear(r.p)) === String(cohortFilter); });
    if (ageFilter) pool = pool.filter(function (r) { return ageMatches(r.p, ageFilter); });

    if (clubFilter) {
      pool = pool.filter(function (r) { return (MD.canonClub(MD.ownership.clubOf(r.p)) || "—") === clubFilter; });
      const summary = clubSummary(clubFilter);
      if (summary) container.appendChild(summary);
    }

    if (pool.length) container.appendChild(boardHead());
    const rowsEl = fmt.el("div", "rows");
    pool.forEach(function (r) { rowsEl.appendChild(workingRow(r, maxV)); });
    // A club's held picks ALWAYS accompany its roster (owner word 2026-08-28).
    if (clubFilter) rowsEl.appendChild(picksPanel(clubFilter));
    container.appendChild(rowsEl);

    const foot = fmt.el("footer", "foot");
    const active = [];
    if (posFilter) active.push(posFilter);
    if (eligFilter) active.push(ELIG_LABELS[eligFilter] || eligFilter);
    if (cohortFilter) active.push(cohortFilter + " cohort");
    if (ageFilter) {
      const band = AGE_BANDS.filter(function (b) { return b.id === ageFilter; })[0];
      active.push("age " + (band ? band.label : ageFilter));
    }
    if (clubFilter) active.push(fmt.club(clubFilter));
    foot.innerHTML = fmt.n(pool.length) + " players" +
      (active.length ? " · " + fmt.esc(active.join(" · ")) : "");
    container.appendChild(foot);
  }

  /* The Clubs page links a club row into its filtered board view. */
  function focusClub(afflTeamLong) {
    clubFilter = MD.canonClub(afflTeamLong) || null;
  }

  function snapshot() {
    return { clubFilter: clubFilter, posFilter: posFilter,
             cohortFilter: cohortFilter, ageFilter: ageFilter, eligFilter: eligFilter };
  }
  function restore(s) {
    if (!s) return;
    clubFilter = s.clubFilter || null;
    posFilter = s.posFilter || null;
    cohortFilter = s.cohortFilter || null;
    ageFilter = s.ageFilter || null;
    eligFilter = s.eligFilter || null;
  }

  // Pure predicates exposed for the test suites (they exercise the exact shipped functions).
  return { render: render, focusClub: focusClub,
           snapshot: snapshot, restore: restore,
           cohortYear: cohortYear, ageMatches: ageMatches, eligMatches: eligMatches,
           roundDeltas: roundDeltas, AGE_BANDS: AGE_BANDS };
})();
