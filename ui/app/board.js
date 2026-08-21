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
  /* v0 COLUMN (owner-commissioned 2026-08-21), OFF BY DEFAULT AND BEHIND A TOGGLE.
     The row already carries ten columns and the UI review found it overcrowded — the grid was rebuilt
     once to stop a seventh cell wrapping under the name. So this does not ADD an eleventh column: it
     SWAPS the "Over free" column for the entry-price one, keeping the grid, the header alignment and
     every responsive breakpoint exactly as the stylesheet defines them (which is not this seat's file
     to widen). Two lenses over the same row, one visible at a time, chosen by the owner. */
  let v0Col = false;
  // the three new filters (owner ask 2026-08-21). null == unfiltered, exactly like posFilter/clubFilter.
  let cohortFilter = null;   // a cohort year, as a string
  let ageFilter = null;      // an exact age, or a "b:lo-hi" band id
  let eligFilter = null;     // a canonical slot code from the store's eligibilities column

  /* item 178(2): a club's held-pick asset value (sum over the ingest's priced picks). 0 if the overlay
     is absent/halted or the club holds none. Never a re-valuation — a sum of the ingest's figures. */
  function clubPicksValue(afflTeamLong) {
    return MD.seam.picksFor(afflTeamLong).reduce(function (s, p) { return s + p.value; }, 0);
  }

  /* ================= THE THREE NEW BOARD FILTERS (owner ask, 2026-08-21) ==========================
     Cohort year · age · position by LIVE ELIGIBILITY. All three are pure row predicates over fields the
     working bundle already carries (`yr`, `ty`, `age`, `elig`) — no new data, no new carrier, no
     valuation touched. They compose with the filters already here (reads, position, club, group-by),
     and they run BEFORE the club aggregation for the same reason the position filter does: so ΣSCAR and
     the club ranks answer the question actually on screen ("which club has the strongest 2024 cohort").

     ---- THE COHORT CLOCK, VERIFIED FROM THE STORE BEFORE IT WAS IMPLEMENTED -----------------------
     The owner stated the grouping: "2024 cohort would be 2024 ND, RD, SSP etc. + 2025 MSD". That is a
     real football fact, not a convention, and the store proves it. Measured over every scoring record
     in engine/rl_after/rl_model_data.json, the gap between a player's `year` and his FIRST season with
     games, by entry type:

         MSD   most common gap  0   (53 of 77 debut in the SAME year as their `year`)
         ND    most common gap +1   (859 rows)     RD  +1 (207)     SSP +1 (34)
         PDA/PDN/PDS/UNR/IRE   +1

     The national, rookie and pre-season/supplemental intakes happen at the END of a year for the season
     that follows; the mid-season draft happens DURING that following season. So a 2024 ND draftee and a
     2025 MSD selection both take the field for the first time in 2025 — one cohort, arriving by two
     doors. The cohort is therefore labelled by the NATIONAL-DRAFT year:

         cohortYear(p) = (p.ty === "MSD") ? p.yr - 1 : p.yr

     This is the owner's stated grouping implemented as stated, and the derivation above is what the
     control's tooltip says on screen so nobody has to come back here to read it. It is a DISPLAY
     grouping only — no valuation, ordering or selection law reads it. */
  function cohortYear(p) {
    if (!p || p.yr == null) return null;
    return p.ty === "MSD" ? (p.yr - 1) : p.yr;
  }

  const COHORT_TIP =
    "Cohort = the intake that first takes the field together, labelled by its NATIONAL-DRAFT year. " +
    "The 2024 cohort is the 2024 national, rookie and pre-season/supplemental entrants PLUS the 2025 " +
    "mid-season draft: the end-of-year drafts feed the season that follows, and the mid-season draft " +
    "happens during that same season, so both groups debut together. Verified against the store — MSD " +
    "rows debut in the same year as their draft year, every other entry type the year after. Display " +
    "grouping only; no value reads it.";

  /* distinct cohort years present, newest first (a draft class reads newest-first). */
  function cohortYears() {
    const set = {};
    (MD.seam.working.players || []).forEach(function (p) {
      const c = cohortYear(p); if (c != null) set[c] = 1;
    });
    return Object.keys(set).map(Number).sort(function (a, b) { return b - a; });
  }

  /* distinct ages present, ascending. `age` is the board's own age field; a row without one is only
     ever excluded by an ACTIVE age filter, never silently bucketed. */
  function ages() {
    const set = {};
    (MD.seam.working.players || []).forEach(function (p) { if (p.age != null) set[p.age] = 1; });
    return Object.keys(set).map(Number).sort(function (a, b) { return a - b; });
  }

  /* AGE BANDS, offered alongside the exact ages because "the kids" and "the 29+ tail" are the two
     questions actually asked of this control. Bounds inclusive; they are display buckets and nothing
     downstream reads them. */
  const AGE_BANDS = [
    { id: "b:-20", label: "20 and under", lo: 0, hi: 20 },
    { id: "b:21-24", label: "21–24", lo: 21, hi: 24 },
    { id: "b:25-28", label: "25–28", lo: 25, hi: 28 },
    { id: "b:29-", label: "29 and over", lo: 29, hi: 999 },
  ];
  function ageMatches(p, sel) {
    if (!sel) return true;
    if (p.age == null) return false;          // an age filter is active and this row has no age
    if (sel.indexOf("b:") === 0) {
      const band = AGE_BANDS.filter(function (b) { return b.id === sel; })[0];
      return !!band && p.age >= band.lo && p.age <= band.hi;
    }
    return String(p.age) === String(sel);
  }

  /* ---- POSITION BY LIVE ELIGIBILITY ------------------------------------------------------------
     DELIBERATELY NOT THE SAME AXIS AS THE EXISTING "Position" FILTER, and both are kept.
       · "Position" filters on `pos` — the board's MODELLING axis, one code per player, the position
         his trajectory is priced on.
       · "Eligible" filters on `elig` — the owner-maintained SLOT-LEGALITY set from the store's
         `eligibilities` column, the same axis the Best-23 law selects over. A dual-position player
         appears under BOTH of his codes here and under exactly one code there.
     The owner's example — "players eligible to play KPF now" — is the second question, and the first
     filter cannot answer it: the modelling axis cannot see dual eligibility at all, which is precisely
     the blindness #274 item 2 carried this column across to fix. Keeping both, labelled differently,
     is the honest shape; collapsing them would silently change what one of the two controls means. */
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
    // #139 item 5: canonical club key (the board bundle is already extractor-normalised, so this is
    // uniformity of the join key rather than a fix here — the duplicate bites on the Movers bundle).
    (MD.seam.working.players || []).forEach(function (p) {
      const c = MD.canonClub(MD.ownership.clubOf(p)); if (c) set[c] = 1;   // #232: live ownership
    });
    return Object.keys(set).sort();
  }

  /* per-club aggregate over a row pool: ΣSCAR (sum of displayed values) + player count, ranked by ΣSCAR. */
  function clubAgg(pool) {
    const m = {};
    pool.forEach(function (r) {
      if (MD.isPickAsset(r.p)) return;   // anonymous future picks have no AFFL club — never in ΣSCAR / club ranks
      // #232: live ownership. A public row the name bridge cannot identify resolves to null and lands
      // in the "—" bucket — excluded from every club's ΣSCAR rather than counted into a wrong one.
      const c = MD.canonClub(MD.ownership.clubOf(r.p)) || "—";
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
      // final integration: the +1/+2 forward lenses are UNIFIED asset ladders — the 64 anonymous national-
      // draft placeholders rank TOGETHER with the 804 players (by value), one combined value-descending
      // ranking of 868 assets. Player-only filters (position / club / group-by-club) remove them while
      // active; the default unfiltered future view contains BOTH players and picks. Residual aggregates are
      // NOT ranked — they live in the reconciliation panel.
      if ((s.lens === 3 || s.lens === 4) && !posFilter && !clubFilter && !groupByClub) {
        const off = s.lens - 2;
        (w.lensPicks || []).forEach(function (pk) {
          if (pk.lens !== off || pk.residual) return;
          pool.push({ p: pickAsset(pk), val: pk.v, pick: true });
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

  /* #139 item 11 — THE CLUB PROFILE SUMMARY. A club page (the board filtered to one AFFL club) now
     OPENS with the same metrics the Clubs comparison page ranks on — Overall · Player · Picks · Top-5 ·
     Top-10 · Best-23 · Non-Best-23 — each with the club's rank on that metric, before any player row.
     Previously you had to go back to the Clubs tab to see any of it.

     The figures come from MD.clubTotals, so they are summed live off the stamped board and are the same
     numbers the Clubs table and the pocket profile show — one computation, three surfaces. They are
     deliberately NOT the banner's ΣSCAR: that is a sum over the *currently filtered, lens-adjusted*
     pool and moves with the position filter and the board lens, which is the right figure for "what am
     I looking at" and the wrong one for "how does this club compare". */
  const SUMMARY_METRICS = [
    { key: "overall", label: "Overall", tip: "players + held picks" },
    { key: "totalPlayer", label: "Player value", tip: "sum of every player on the list" },
    { key: "totalPicks", label: "Picks value", tip: "held draft picks at the canonical PVC" },
    { key: "top5", label: "Top-5", tip: "the five most valuable players" },
    { key: "top10", label: "Top-10", tip: "the ten most valuable players" },
    { key: "best23", label: "Best-23", tip: "the most valuable legally-fieldable 23 — XVIII + 5 bench, chosen over each player's eligible positions" },
    { key: "nonBest23", label: "Non-Best-23", tip: "roster depth beyond the best XXIII" },
  ];

  function clubSummary(teamLong) {
    const ct = MD.clubTotals.compute();
    if (!ct) return null;
    const c = MD.clubTotals.byTeam(teamLong);
    if (!c) return null;                       // Free-Agents pool / unknown club → no ranked profile
    const el = fmt.el("div", "clubsummary");
    let cells = "";
    SUMMARY_METRICS.forEach(function (m) {
      const na = !ct.picksAvailable && (m.key === "totalPicks" || m.key === "overall");
      const rank = na ? null : MD.clubTotals.rankOf(c.team, m.key);
      cells +=
        '<div class="csm" title="' + fmt.esc(m.tip) + '">' +
          '<div class="csm-k">' + fmt.esc(m.label) + "</div>" +
          '<div class="csm-v num">' + (na ? "<small>n/a</small>" : fmt.n(c[m.key])) + "</div>" +
          '<div class="csm-r">' + (rank ? "rank " + rank + " of " + ct.clubs.length : "—") + "</div>" +
        "</div>";
    });
    el.innerHTML =
      '<div class="csm-head"><span class="csm-name">' + fmt.esc(c.display || fmt.club(c.team)) + "</span>" +
        '<span class="csm-sub">club profile · ' + fmt.n(c.nRoster) + " players · " +
        (ct.picksAvailable ? fmt.n(c.nPicks) + " held picks" : "picks unavailable") +
        " · ranked against " + ct.clubs.length + " clubs</span></div>" +
      '<div class="csm-grid">' + cells + "</div>";
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
        '<span class="h r">' + dh + '</span>' +
        /* the swappable lens cell: "Over free" (#274 item 3) or the entry-price lens. Both are computed
           at render from given board figures and stored nowhere. */
        (v0Col
          ? '<span class="h r ofree" title="' + fmt.esc(
              "Entry price (v0) and what he is worth against it. v0 is the price the model put on him " +
              "the moment he entered — his draft slot's year-zero value, or his division's signed " +
              "entry level if he came through the pool. The small line is the absolute gap and the " +
              "ratio. A difference of two given figures; nothing is re-valued and nothing is ranked.") +
              '">v0 <small>· vs entry</small></span>'
          : '<span class="h r ofree" title="' + fmt.esc(
              "Over free = board value − free-hit value (" + MD.config.FHV + "). What this player is worth " +
              "above what the free-agent tier reasonably gives you for nothing. A negative figure is a " +
              "delist candidate: his place costs more than it returns against a free hit. Computed on the " +
              "board on screen, never stored.") + '">Over free</span>') +
        '<span class="h r">Pick · Yr</span>';
    } else {
      el.innerHTML =
        '<span class="h r">#</span><span class="h">Player</span><span class="h">Pos</span>' +
        // #139 item 9: the AFFL/AFL club column now appears on the public tier too.
        '<span class="h">Club <small>AFFL · AFL</small></span>' +
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
    // round — `dRound` has NO WRITER (0/804 on both shipped bundles; not in rl_export.py's row schema).
    // The old tooltip said it "arrives with the weekly loop (Phase 3)"; the weekly loop landed and the
    // field did not, so the tooltip named a delivery that had already happened without it.
    if (p.dRound == null) {
      return '<span class="pill na" title="Δ vs previous round is NOT PUBLISHED on this board — the ' +
        'dRound export field has no writer. Use Δ vs bake, which is populated on every row; the ' +
        'per-round record lives on the Movers tab.">—</span>';
    }
    return '<span class="pill ' + fmt.cls(p.dRound) + '">' + fmt.signed(p.dRound) + "</span>";
  }

  /* #274 item 3 — the over-free lens, on the DISPLAYED value so it follows the board lens the way every
     other figure on the row does. Computed here; nothing is stored. */
  function overFreeCell(val) {
    return '<span class="ofree num' + (MD.belowFree(val) ? " belowfree" : "") + '" title="' + fmt.esc(
      MD.belowFree(val)
        ? "BELOW FREE — worth less than the free-hit value (" + MD.config.FHV + "), so a free agent is " +
          "the better use of the place. A standing delist candidate."
        : "Over free = value − " + MD.config.FHV + " (the ruled free-hit value).") + '">' +
      /* NOT fmt.signed: its ▲/▼ arrows are the fixed grammar for MOVEMENT, and nothing has moved here.
         A standing gap gets a plain sign. */
      (val == null ? "—" : (MD.overFree(val) >= 0 ? "+" : "−") + fmt.n(Math.abs(MD.overFree(val)))) +
      "</span>";
  }

  /* The entry-price lens (owner 2026-08-21): v0 on top, the absolute gap and the ratio underneath.
     v0 is a DRAFT-TIME constant read from the stamped sidecar, so it does not follow the board lens —
     and the comparison figures are therefore taken against the player's NOW value, never against a
     projected lens year. A refused or absent row prints an em-dash carrying its reason; there is no
     second source for an entry price and none is invented. NOTHING IS RANKED (see ui/app/v0.js). */
  function v0Cell(p) {
    const r = MD.v0.of(p);
    if (r.refused || !r.has) {
      return '<span class="ofree num" title="' + fmt.esc(
        r.why || "no entry price is available for this row") + '">—</span>';
    }
    const cls = r.delta == null ? "" : (r.delta > 0 ? " up" : r.delta < 0 ? " dn" : "");
    const tip = "Entry price (v0) " + fmt.n(r.v0) + " · " + MD.v0.originWord(r.origin) + ". Now " +
      fmt.n(r.live) + " — that is " + (r.delta >= 0 ? "+" : "−") + fmt.n(Math.abs(r.delta)) + " and " +
      MD.v0.ratioText(r.ratio) + ". " + MD.v0.originTip(r.origin);
    return '<span class="ofree num' + cls + '" title="' + fmt.esc(tip) + '">' + fmt.n(r.v0) +
      '<small style="display:block;font-size:9px;letter-spacing:.02em;opacity:.75">' +
      (r.delta >= 0 ? "+" : "−") + fmt.n(Math.abs(r.delta)) + " · " + fmt.esc(MD.v0.ratioText(r.ratio)) +
      "</small></span>";
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
      // #232: the AFFL club is the live sidecar's, falling back to the board's stored value.
      '<span class="club"><span class="affl" title="' + fmt.esc(MD.ownership.titleOf(p)) + '">' +
        fmt.esc(MD.ownership.labelOf(p)) + "</span>" +
        '<span class="afl" title="AFL club">' + fmt.esc(p.afl_club || "—") + "</span></span>" +
      '<span class="val num">' + fmt.n(r.val) + "</span>" +
      MD.valueLine(r.val, maxV) +
      deltaPill(p, r.val) +
      (v0Col ? v0Cell(p) : overFreeCell(r.val)) +
      '<span class="meta">' + (p.pk ? "pk " + p.pk : "—") + " · ’" + String(p.yr || "").slice(2) + "</span>";
    b.addEventListener("click", function () { MD.go("card", p.key); });
    return b;
  }

  function publicRow(r, maxV, byKey) {
    const p = r.p;
    // item 7 (de-clunk): ONE movement instance, correctly aligned. The old row emitted two "steady"
    // pills (value-move + rank-move) into a 6-column grid, so the seventh cell wrapped under the name —
    // the duplicated "steady" the owner flagged. Collapsed to a single movement-vs-previous-round pill
    // (rank movement rides its tooltip); the row now emits exactly its grid's columns.
    /* dRound — THE COMMENT THAT OUTLIVED ITS TRUTH, AND THE BRIDGE IT JUSTIFIED. REMOVED.

       What stood here asserted that "the working bundle has all 804 populated" while the public
       projection dropped the field, and on that belief built a name→key bridge so a public row could
       borrow the working figure. The premise was never true. Measured on both shipped bundles:
       `dRound` is 0/804 and `dRoundRank` is 0/804 on the WORKING bundle as well as the public one, and
       a search for any WRITER across engine/, tools/ and ui/tools/ finds only readers — the exported
       row schema in rl_export.py `player_rec()` has never contained the key. No production writer has
       ever existed, so the bridge was resolving null → null and the field is dead on both tiers.

       The bridge is deleted rather than left returning null: a mechanism that cannot work is worse than
       no mechanism, because the next reader believes it. The row now reads the bundle field directly
       and says plainly that no movement is published — which is the truth, and is what the tier's own
       fail-safe doctrine requires. The movement information DOES exist, in ui/data/movers.js, and
       joining it is a real (queued) piece of work; it is not this fix, and pretending the join is
       already here was the defect.

       Note the tier asymmetry this leaves standing, named rather than masked: the public projection
       carries `dRound`/`dRoundRank` as keys it never fills. That is filed at UI_PARKED item 18. */
    const dRound = p.dRound;
    const move = dRound == null
      ? '<span class="pill na" title="No previous-round movement is published on this board. The ' +
        'dRound export field has no writer, so nothing is shown rather than a fabricated move — the ' +
        'per-round record lives on the Movers tab and on the player card’s weekly history.">not published</span>'
      : '<span class="pill ' + fmt.cls(dRound) + '" title="movement vs previous round">' + fmt.signed(dRound) + "</span>";
    const b = fmt.el("button", "row public");
    b.innerHTML =
      '<span class="rank num">' + r.rank + "</span>" +
      '<span class="nm">' + fmt.esc(p.name) + "</span>" +
      '<span class="pos">' + fmt.esc(p.pos) + "</span>" +
      // #139 item 9: Public rankings now carry the AFFL team alongside the player, the same way the
      // working row does — AFFL leading, AFL as the muted sub-line. This is ownership information the
      // public tier already ships in its own bundle (board_view_public.js carries affl_team/afl_club);
      // it was simply never rendered.
      // #232: a public row carries NO key, so ownership is resolved by bridging its display name to a
      // working-board key. If that bridge cannot identify the row, MD.ownership refuses and this shows
      // "⚠ unverified" rather than the board's stored club — because with the sidecar live we cannot
      // claim the stored club is current, and a wrong club shown confidently is the defect.
      '<span class="club"><span class="affl" title="' + fmt.esc(MD.ownership.titleOf(p)) + '">' +
        fmt.esc(MD.ownership.labelOf(p)) + "</span>" +
        '<span class="afl" title="AFL club">' + fmt.esc(p.afl_club || "—") + "</span></span>" +
      '<span class="val num">' + fmt.n(r.val) + "</span>" +
      MD.valueLine(r.val, maxV) + move;
    // #139 item 16: clicking a player in Public opens that player's profile. The working row has always
    // done this; the public row simply had no handler, so a tap did nothing. The card key is the working
    // bundle's key — the public bundle carries no `key`, so the row joins on name to the working index
    // (the public tier is a sanitised VIEW of the same 804 players, not a different population).
    const key = p.key || (byKey && byKey.byName && byKey.byName[p.name]);
    if (key) {
      b.addEventListener("click", function () { MD.go("card", key); });
    } else {
      // No join → no navigation, and the row says so rather than pretending to be clickable.
      b.classList.add("noprofile");
      b.title = "No player profile is joinable for this row.";
    }
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
      /* THE +1/+2 LENSES ARE OFF (owner word 2026-08-21; ruling register v46). What stood here said the
         forward toggle was "RE-ENABLED … the projection law (R103.3) has landed"; the rebuild it cites
         has not shipped and no entry retires the ruling, so the comment was licensing a ruled-wrong
         number on the owner's primary surface. The disabled set lives in config.js (LENS_DISABLED) with
         the full ruling; lifting it is emptying that list, on the owner's word, after the rebuild.
         −2/−1/Now are untouched — real backward re-values and the live board. */
      MD.config.LENS_LABELS.forEach(function (lab, i) {
        const off = MD.lensDisabled(i);
        const btn = fmt.el("button", i === s.lens ? "on" : "", lab);
        if (off) {
          btn.disabled = true;
          btn.classList.add("lensoff");
          btn.title = MD.config.LENS_DISABLED_WHY;
        } else {
          btn.addEventListener("click", function () { s.lens = i; render(container); });
        }
        lens.appendChild(btn);
      });
      wrap.appendChild(lens);
      if ((MD.config.LENS_DISABLED || []).length) {
        const lnote = fmt.el("span", "lbl");
        lnote.style.color = "var(--faint)";
        lnote.style.letterSpacing = ".04em";
        lnote.style.textTransform = "none";
        lnote.title = MD.config.LENS_DISABLED_WHY;
        lnote.textContent = "· " + MD.config.LENS_DISABLED_NOTE;
        wrap.appendChild(lnote);
      }

      /* Q-DELTA-BASE toggle. Dimmed on a non-now lens (does not apply).
         A BASIS WITH NO WRITER IS NOT OFFERED AS A CHOICE. `dRound` is 0/804 on both shipped bundles
         and has no production writer, so the "round" basis can only ever produce a column of dashes —
         the UI review's "DEAD COLUMNS SHIP BY DEFAULT" finding, arriving through the default rather
         than through the design. The button stays visible (the basis is real and is queued) and is
         disabled with the reason on hover, exactly as the picks-overlay button is on an ingest halt.
         The check is on the DATA, not on a constant: the day a writer lands, the button lights itself. */
      wrap.appendChild(fmt.el("span", "lbl", "Δ base"));
      const dseg = fmt.el("div", "seg");
      const basisFed = { bake: false, round: false };
      (MD.seam.working.players || []).forEach(function (p) {
        if (p.vPrev != null) basisFed.bake = true;
        if (p.dRound != null) basisFed.round = true;
      });
      [["bake", "bake"], ["round", "round"]].forEach(function (pair) {
        const btn = fmt.el("button", s.deltaBase === pair[0] ? "on" : "", pair[1]);
        if (s.lens !== 2) { btn.disabled = true; btn.style.opacity = ".4"; btn.style.cursor = "default"; }
        else if (!basisFed[pair[0]]) {
          btn.disabled = true; btn.classList.add("lensoff");
          // the .lensoff rule is scoped to .seg.lens / .seg.assets in the stylesheet; this seg is
          // neither, and the stylesheet is not this seat's to widen — so the affordance is inline.
          btn.style.opacity = ".3"; btn.style.cursor = "not-allowed"; btn.style.textDecoration = "line-through";
          btn.title = pair[0] === "round"
            ? "Δ vs previous round is not published on this board — the dRound export field has no " +
              "writer (0 of " + fmt.n((MD.seam.working.players || []).length) + " rows carry it). " +
              "Queued; the button lights itself the day a writer lands."
            : "Δ vs last accepted bake is not carried on this board — no row carries vPrev.";
        }
        else btn.addEventListener("click", function () { s.deltaBase = pair[0]; render(container); });
        dseg.appendChild(btn);
      });
      wrap.appendChild(dseg);
      if (s.lens === 2 && !basisFed[s.deltaBase]) {
        // the ACTIVE basis is unfed — say so beside the column rather than leaving a wall of dashes
        const note = fmt.el("span", "lbl");
        note.style.color = "var(--faint)";
        note.style.letterSpacing = ".04em";
        note.style.textTransform = "none";
        note.textContent = s.deltaBase === "bake"
          ? "· no row carries vPrev on this board; no Δ invented"
          : "· Δ vs round is not published — the dRound export field has no writer; no Δ invented";
        wrap.appendChild(note);
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
      psel.title = "The board's MODELLING position — one code per player, the axis his trajectory is " +
        "priced on. For \"who is eligible to play there now\", use Eligible.";
      wrap.appendChild(psel);

      /* ---- owner ask 2026-08-21: eligibility · cohort year · age. Same control vocabulary as the
         filters already here (a labelled <select class="boardsel">), so they read as one row. Each
         carries its rule on hover rather than assuming the reader knows it. */

      // (c) POSITION BY LIVE ELIGIBILITY — "players eligible to play KPF now".
      const eligOpts = eligCodes();
      if (eligOpts.length) {
        wrap.appendChild(fmt.el("span", "lbl", "Eligible"));
        const esel = document.createElement("select");
        esel.className = "boardsel";
        esel.title = "Filters on the store's owner-maintained ELIGIBILITIES column — the slot-legality " +
          "axis the Best-23 law selects over. A dual-position player appears under BOTH of his codes " +
          "here, which is exactly what the modelling Position axis cannot see.";
        esel.innerHTML = '<option value="">any eligibility</option>' +
          eligOpts.map(function (c) {
            return '<option value="' + fmt.esc(c) + '"' + (eligFilter === c ? " selected" : "") + ">" +
              fmt.esc((ELIG_LABELS[c] || c) + " (" + c + ")") + "</option>";
          }).join("");
        esel.addEventListener("change", function () { eligFilter = esel.value || null; render(container); });
        wrap.appendChild(esel);
      }

      // (a) COHORT YEAR — the owner's stated grouping; the clock rule is verified in cohortYear().
      const cohorts = cohortYears();
      if (cohorts.length) {
        wrap.appendChild(fmt.el("span", "lbl", "Cohort"));
        const ysel = document.createElement("select");
        ysel.className = "boardsel";
        ysel.title = COHORT_TIP;
        ysel.innerHTML = '<option value="">all cohorts</option>' +
          cohorts.map(function (y) {
            return '<option value="' + y + '"' + (String(cohortFilter) === String(y) ? " selected" : "") +
              ">" + y + " cohort</option>";
          }).join("");
        ysel.addEventListener("change", function () { cohortFilter = ysel.value || null; render(container); });
        wrap.appendChild(ysel);
      }

      // (b) AGE — bands first (the two questions actually asked), then every exact age present.
      const ageOpts = ages();
      if (ageOpts.length) {
        wrap.appendChild(fmt.el("span", "lbl", "Age"));
        const asel = document.createElement("select");
        asel.className = "boardsel";
        asel.title = "The board's own age field. Bands are display buckets; the exact ages below them " +
          "are the board's values verbatim. A row carrying no age drops out while an age filter is on, " +
          "rather than being bucketed into an age it does not have.";
        asel.innerHTML = '<option value="">all ages</option>' +
          AGE_BANDS.map(function (b) {
            return '<option value="' + b.id + '"' + (ageFilter === b.id ? " selected" : "") + ">" +
              fmt.esc(b.label) + "</option>";
          }).join("") +
          ageOpts.map(function (a) {
            return '<option value="' + a + '"' + (String(ageFilter) === String(a) ? " selected" : "") +
              ">" + a + " yo</option>";
          }).join("");
        asel.addEventListener("change", function () { ageFilter = asel.value || null; render(container); });
        wrap.appendChild(asel);
      }

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

      /* v0 COLUMN TOGGLE (owner ask 2026-08-21). It SWAPS the "Over free" column rather than adding an
         eleventh — see the v0Col declaration. Disabled, with the reason on hover, whenever the sidecar
         is absent or fails its board/store pin: an unauthenticated mirror must look unavailable, not
         empty. The card carries the full four-figure block regardless of this toggle. */
      wrap.appendChild(fmt.el("span", "lbl", "Lens col"));
      const vseg = fmt.el("div", "seg assets");
      const v0st = MD.v0.status();
      [["free", "over free"], ["v0", "entry price"]].forEach(function (pair) {
        const on = (pair[0] === "v0") === v0Col;
        const btn = fmt.el("button", on ? "on" : "", pair[1]);
        if (pair[0] === "v0" && !v0st.active) {
          btn.disabled = true; btn.classList.add("lensoff");
          btn.title = "Entry prices unavailable — " + (v0st.pinWhy || "no v0 sidecar is loaded") + ".";
        } else {
          btn.addEventListener("click", function () { v0Col = pair[0] === "v0"; render(container); });
        }
        vseg.appendChild(btn);
      });
      wrap.appendChild(vseg);

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

  /* final integration 2026-07-21: an anonymous future-draft placeholder, RANKED among the players in the
     +1/+2 lens. It is an ASSET, not a player: no key, no card, no AFL/AFFL club, no position, a stable
     asset id, posCode "PICK" so MD.isPickAsset() ring-fences it out of the current/backward ladders and off
     the player-only joins (club aggregation / positional rank / club filter / player card). */
  function pickAsset(pk) {
    return { asset: "pick", kind: "pick", posCode: "PICK", id: pk.id, label: pk.label, n: pk.n,
             v: pk.v, labelYear: pk.labelYear, assetType: pk.assetType, affl_team: null, club: null, pos: null };
  }

  /* render one ranked future-draft placeholder row (same grid as workingRow; GLOBAL combined rank in the
     rank column, the draft PICK NUMBER shown separately in the meta column). No player-card click. */
  function pickRow(r, maxV) {
    const pk = r.p;
    const b = fmt.el("button", "row working pickrow");
    b.setAttribute("data-asset", pk.id);
    b.innerHTML =
      '<span class="rank num">' + r.rank + "</span>" +
      '<span class="pin"></span>' +
      '<span class="nm">' + fmt.esc(pk.label) +
        '<span class="tag" title="Anonymous future national-draft asset — NOT a player, and not held by any ' +
        'AFL or AFFL club. Valued at the release-active pick-value curve (PVC). Ranked among players by value.">' +
        'Draft asset</span></span>' +
      '<span class="pos">—</span>' +
      '<span class="club"><span class="affl" title="Future asset — no AFFL club">Future draft</span>' +
        '<span class="afl" title="Future asset — no AFL club">—</span></span>' +
      '<span class="val num">' + fmt.n(pk.v) + "</span>" +
      MD.valueLine(pk.v, maxV) +
      '<span class="pill na" title="Future asset — no round movement">—</span>' +
      '<span class="meta">' + (pk.n != null ? "pick " + pk.n : "aggregate") + " · " + fmt.esc(String(pk.labelYear)) + "</span>";
    return b;   // no click handler — assets have no player card
  }

  /* +1/+2 F5 reconciliation panel (residuals held OUT of the ranking): visible Σ PVC[1..64] + national-draft
     deep-tail residual + non-national-draft mechanism residual == the sealed F5 entrant layer. */
  function reconciliationPanel(container) {
    const s = MD.state;
    if (!(s.lens === 3 || s.lens === 4)) return;
    const dat = ((MD.seam.working || {}).draftAssetTotals || {})["+" + (s.lens - 2)];
    if (!dat) return;
    const el = fmt.el("div", "reconpanel");
    el.style.cssText = "margin:.5rem 0;padding:.4rem .6rem;border-left:3px solid #6a8;background:rgba(127,127,127,.06);font-size:.8rem;line-height:1.6";
    el.innerHTML = '<b>' + dat.lensYear + " future-entrant reconciliation</b> (residuals held out of the ranking) — " +
      "visible Picks 1–64 Σ<b>" + fmt.n(dat.visible_1_64) + "</b> + national-draft deep-tail residual <b>" +
      fmt.n(dat.residual_nd_tail) + "</b> + non-national-draft entry residual <b>" + fmt.n(dat.residual_mech) +
      "</b> = sealed F5 entrant layer <b>" + fmt.n(dat.f5_entrant_layer_pvc) + "</b>" +
      (dat.reconciled_to_f5 ? " ✓" : " ✗") +
      ' <span style="opacity:.6">· the deep-tail (picks 65+) and non-national-draft mechanisms (MSD/SSP/rookie/' +
      'pre-season/international) are aggregates, not single tradeable assets — never ranked</span>';
    container.appendChild(el);
  }

  function render(container) {
    container.innerHTML = "";
    const s = MD.state;
    // THE CLAMP (owner word 2026-08-21): a ruled-off lens can never be the active lens, however it got
    // set — a restored Back snapshot, a stale value, a future caller. See MD.lensClamp in seam.js.
    s.lens = MD.lensClamp(s.lens);
    strip(container);
    if (s.tier === "working") phantomBanner(container);   // LEG F1: phantom (+1/+2) / retrospective (−1/−2) view, empty-state safe

    const idx = MD.seam.indexed();
    const byKey = idx.byKey;
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
    /* owner ask 2026-08-21 — eligibility · cohort · age, applied on the same line and for the same
       reason as the position filter above: BEFORE club aggregation, so ΣSCAR and the club ranks answer
       the question on screen. Each predicate is skipped entirely when its filter is null, so the
       unfiltered board is byte-identical to what it was. */
    if (s.tier === "working" && eligFilter) {
      pool = pool.filter(function (r) { return eligMatches(r.p, eligFilter); });
    }
    if (s.tier === "working" && cohortFilter) {
      pool = pool.filter(function (r) { return String(cohortYear(r.p)) === String(cohortFilter); });
    }
    if (s.tier === "working" && ageFilter) {
      pool = pool.filter(function (r) { return ageMatches(r.p, ageFilter); });
    }

    // item 2: canonical club ranking (ΣSCAR over the full unfiltered pool) — used for club-rank badges.
    const clubRanks = {};
    if (s.tier === "working") clubAgg(pool).forEach(function (c, i) { clubRanks[c.club] = i + 1; });

    /* #139 item 12 — THE PUBLIC CLUB-PROFILE DEFECT. Opening a club from the Clubs page set the club
       filter and routed to the board, but the filter was only ever APPLIED on the working tier, so a
       public visitor landed on the unfiltered all-player list — the club they picked silently ignored.
       The filter now applies on both tiers. Public sees the club's players and the same club summary;
       the figures are sums of values the public board already prints, and the Clubs comparison table is
       already public, so this exposes no new field — it makes the destination match the click. */
    if (s.tier === "public" && clubFilter) {
      pool = pool.filter(function (r) { return (MD.canonClub(MD.ownership.clubOf(r.p)) || "—") === clubFilter; });
      const summary = clubSummary(clubFilter);
      if (summary) container.appendChild(summary);
      const clear = fmt.el("div", "clubclear");
      clear.innerHTML = '<button type="button">← all players</button>' +
        '<span class="lbl">showing ' + fmt.esc(fmt.club(clubFilter)) + " only</span>";
      clear.firstChild.addEventListener("click", function () { focusClub(null, false); render(container); });
      container.appendChild(clear);
    }

    // item 2: filter to a single AFFL club (working tier).
    if (s.tier === "working" && clubFilter) {
      pool = pool.filter(function (r) { return (MD.canonClub(MD.ownership.clubOf(r.p)) || "—") === clubFilter; });
      // #139 item 11: the comparison-page metrics lead the club page, before any player row.
      const summary = clubSummary(clubFilter);
      if (summary) container.appendChild(summary);
      const ca = clubAgg(pool)[0];
      if (ca) container.appendChild(clubBanner(ca, clubRanks[clubFilter], clubRanks));
    }

    if (pool.length) container.appendChild(boardHead(s.tier)); // item 4: column headings
    // final integration: the +1/+2 future-entrant reconciliation panel (residuals held out of the ranking).
    if (s.tier === "working") reconciliationPanel(container);
    const rowsEl = fmt.el("div", "rows");
    if (s.tier === "working" && groupByClub) {
      // grouped: club headers ranked by ΣSCAR, EVERY player for every club (owner ruling: no truncation).
      clubAgg(pool).forEach(function (c) {
        rowsEl.appendChild(clubHeader(c, clubRanks[c.club]));
        const mine = pool.filter(function (r) { return (MD.canonClub(MD.ownership.clubOf(r.p)) || "—") === c.club; });
        mine.forEach(function (r) { rowsEl.appendChild(workingRow(r, maxV, byKey)); });
      });
    } else {
      // owner ruling: EVERY matching row renders — no top-60 cap, no hidden rows (players + ranked picks).
      pool.forEach(function (r) {
        rowsEl.appendChild(r.pick ? pickRow(r, maxV)
          : (s.tier === "working" ? workingRow(r, maxV, byKey) : publicRow(r, maxV, idx)));
      });
    }
    // item 178(2): a single filtered club with "picks included" lists its held picks under the roster.
    if (s.tier === "working" && clubFilter && picksIncluded && !MD.seam.clubHalt()) {
      rowsEl.appendChild(picksPanel(clubFilter));
    }
    container.appendChild(rowsEl);

    const foot = fmt.el("footer", "foot");
    if (s.tier === "working") {
      const nPick = pool.filter(function (r) { return r.pick; }).length;
      const nPlayer = pool.length - nPick;
      const shown = groupByClub ? ("grouped by AFFL club · all " + fmt.n(pool.length) + " rows")
        : ("rendering all " + fmt.n(pool.length) + " rows" +
           (nPick ? " (" + fmt.n(nPlayer) + " players + " + fmt.n(nPick) + " draft assets)" : ""));
      // name the active filters in the footer: a filtered board that does not say it is filtered is
      // the same class of defect as a dead column that does not say it is dead.
      const active = [];
      if (onlyReads) active.push("my reads");
      if (posFilter) active.push("position " + posFilter);
      if (eligFilter) active.push("eligible " + (ELIG_LABELS[eligFilter] || eligFilter));
      if (cohortFilter) active.push(cohortFilter + " cohort");
      if (ageFilter) {
        const band = AGE_BANDS.filter(function (b) { return b.id === ageFilter; })[0];
        active.push("age " + (band ? band.label : ageFilter));
      }
      if (clubFilter) active.push(fmt.club(clubFilter));
      foot.innerHTML = "volt = your touch (reads · rules · controls) · the value line = share of the top price, its colour warming as it fills · " +
        "movement pills always signed · override headroom lives on the card's waterfall · " + shown +
        (s.lens !== 2 ? " at the " + MD.config.LENS_LABELS[s.lens] + " lens" : "") +
        (active.length ? " · filtered: " + fmt.esc(active.join(" · ")) : "") +
        (v0Col ? " · the lens column shows ENTRY PRICE (v0) — draft-time, so it does not follow the board lens" : "");
    } else {
      foot.innerHTML = "the value line = share of the top price, its colour warming as it fills · movement pills always signed, never colour alone · public trim — no ids, no internals";
    }
    container.appendChild(foot);
  }

  /* item 178(3): the team-summary page links a club row into its filtered board view. Sets the
     team-lens filter (and turns picks on) before the router switches to the board. */
  function focusClub(afflTeamLong, withPicks) {
    clubFilter = MD.canonClub(afflTeamLong) || null;
    groupByClub = false;
    if (withPicks && !MD.seam.clubHalt()) picksIncluded = true;
  }

  /* #139 item 15 — universal Back. The board's filter state lives in this module's closure, so a Back
     that only restored MD.state would return you to "the board" but not to THE BOARD YOU WERE ON: the
     club you had open, the position lens, whether picks were showing. These let the router snapshot and
     restore the whole visible board, so club → player → Back lands on the club page again. */
  function snapshot() {
    return { clubFilter: clubFilter, groupByClub: groupByClub, posFilter: posFilter,
             picksIncluded: picksIncluded, onlyReads: onlyReads,
             // owner ask 2026-08-21 — the three new filters and the column lens ride Back too, or
             // "the board you were on" quietly stops meaning the board you were on.
             cohortFilter: cohortFilter, ageFilter: ageFilter, eligFilter: eligFilter, v0Col: v0Col };
  }
  function restore(s) {
    if (!s) return;
    clubFilter = s.clubFilter; groupByClub = s.groupByClub; posFilter = s.posFilter;
    picksIncluded = s.picksIncluded; onlyReads = s.onlyReads;
    cohortFilter = s.cohortFilter || null;
    ageFilter = s.ageFilter || null;
    eligFilter = s.eligFilter || null;
    v0Col = !!s.v0Col;
  }

  // retroFor exposed so the release-seam test can exercise the EXACT retrospective identity check
  // the UI runs (same doctrine as counting.js). Pure view; reads no DOM.
  // cohortYear / ageMatches / eligMatches are exposed so the defect+filter suite can exercise the EXACT
  // shipped predicates (same doctrine as retroFor and counting.js). Pure functions; they read no DOM.
  return { render: render, focusClub: focusClub, retroFor: retroFor,
           snapshot: snapshot, restore: restore,
           cohortYear: cohortYear, ageMatches: ageMatches, eligMatches: eligMatches,
           AGE_BANDS: AGE_BANDS };
})();
