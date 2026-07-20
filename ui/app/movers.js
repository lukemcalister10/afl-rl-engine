/* Matchday UI — MOVERS view (native section of the existing engine; no new framework, no new shell).
   Pure view: consumes the generated movers bundle (window.__MATCHDAY_MOVERS__), never re-valuing or
   re-ranking. All deltas come from the two committed consecutive-round boards (via the report). Reuses
   the existing masthead/nav/tier shell, CSS variables, cards, tables, pills, filters and the player-
   card link (MD.go("card", key)). Fail-closes (existing .failclosed style) on an invalid/incomplete/
   mismatched report. Dual-target: the browser view + pure helpers unit-tested under node. */
(function (root) {
  "use strict";

  /* ---- pure, dual-target logic (unit-tested under node) ------------------------------------ */
  var core = {
    /* Fail-closed integrity of ONE report: it must carry a committed board identity, a unique + full
       active-player set, a release identity, and (in the bundle) a coherent board-identity chain. */
    integrity: function (report, bundle) {
      if (!report || report.kind !== "weekly_movers_report") return { ok: false, why: "no movers report" };
      var players = report.players || [];
      if (!players.length) return { ok: false, why: "movers report has no players" };
      var keys = {}; for (var i = 0; i < players.length; i++) keys[players[i].key] = 1;
      if (Object.keys(keys).length !== players.length) return { ok: false, why: "duplicate player rows" };
      if (report.integrity && report.integrity.players_unique === false) return { ok: false, why: "player set not unique" };
      if (report.integrity && report.integrity.coverage_full === false) return { ok: false, why: "player coverage incomplete" };
      if (report.integrity && report.integrity.board_after_matches_committed === false)
        return { ok: false, why: "board identity does not match the committed board" };
      if (!report.board_md5_after) return { ok: false, why: "missing committed board id" };
      if (!report.release_identity) return { ok: false, why: "missing release identity" };
      if (bundle && bundle.integrity && bundle.integrity.board_chain_ok === false)
        return { ok: false, why: "board-identity chain broken between rounds" };
      return { ok: true };
    },

    /* Deterministic comparator: primary movement field (dir), then current value desc, then key asc. */
    cmp: function (field, dir) {
      var sgn = dir === "asc" ? 1 : -1;
      return function (a, b) {
        var av = a[field], bv = b[field];
        var an = (av === null || av === undefined), bn = (bv === null || bv === undefined);
        if (an && bn) { /* both null */ }
        else if (an) return 1;   // nulls sort last regardless of dir
        else if (bn) return -1;
        else if (av !== bv) return sgn * (av < bv ? -1 : 1);
        var acv = a.cur_value == null ? -Infinity : a.cur_value;
        var bcv = b.cur_value == null ? -Infinity : b.cur_value;
        if (acv !== bcv) return bcv - acv;              // current value descending
        return a.key < b.key ? -1 : (a.key > b.key ? 1 : 0);  // stable key ascending
      };
    },

    filter: function (players, f) {
      f = f || {};
      return players.filter(function (p) {
        if (f.club && (p.affl_team || "—") !== f.club) return false;
        if (f.pos && p.pos !== f.pos) return false;
        if (f.status === "played" && !p.played) return false;
        if (f.status === "dnp" && p.played) return false;
        return true;
      });
    },

    /* The rows for a named view (value/rank risers/fallers, or all), filtered + deterministically sorted. */
    viewRows: function (report, view, f) {
      var players = core.filter(report.players || [], f);
      var spec = {
        value_risers: ["value_change", "desc"], value_fallers: ["value_change", "asc"],
        rank_risers: ["rank_change", "desc"], rank_fallers: ["rank_change", "asc"],
        all: ["cur_value", "desc"],
      }[view] || ["cur_value", "desc"];
      return players.slice().sort(core.cmp(spec[0], spec[1]));
    },

    /* The four summary headline movers (largest value inc/dec, largest overall-rank imp/decline). */
    summary: function (report) {
      var P = report.players || [];
      function top(field, dir) {
        var s = P.slice().sort(core.cmp(field, dir));
        return s.length ? s[0] : null;
      }
      return {
        value_increase: top("value_change", "desc"),
        value_decrease: top("value_change", "asc"),
        rank_improve: top("rank_change", "desc"),
        rank_decline: top("rank_change", "asc"),
      };
    },
  };

  /* ---- browser view ------------------------------------------------------------------------ */
  function makeView(MD) {
    var fmt = MD.fmt;
    var state = { round: null, view: "value_risers", club: null, pos: null, status: null, sort: null, dir: "desc" };

    function bundle() { return (typeof window !== "undefined" && window.__MATCHDAY_MOVERS__) || null; }

    function availableRounds(b) { return (b && b.rounds) ? b.rounds.slice() : []; }

    function reportFor(b, rnd) { return b && b.reports ? b.reports[String(rnd)] : null; }

    function failState(holder, why) {
      var box = fmt.el("div", "failclosed");
      box.innerHTML = "<h1>■ Movers unavailable — integrity check failed</h1>" +
        "<p>The Movers view renders only a movers report whose transaction committed and whose board " +
        "identities are coherent. This report did not pass the integrity check, so nothing is shown " +
        "rather than showing stale or partial data.</p>" +
        '<p class="mono">reason: ' + fmt.esc(why) + "</p>";
      holder.appendChild(box);
    }

    function metaStrip(report) {
      var s = fmt.el("div", "strip moversmeta");
      var rel = report.release_identity || {};
      s.innerHTML =
        '<span class="lbl">Round</span><b class="num">R' + report.submitted_round + "</b>" +
        '<span class="lbl">baseline</span><b class="num">R' + report.previous_round + "</b>" +
        '<span class="lbl">players</span><b class="num">' + fmt.n(report.player_count) + "</b>" +
        '<span class="lbl">played</span><b class="num">' + fmt.n((report.views || {}).played_count) + "</b>" +
        '<span class="lbl">DNP</span><b class="num">' + fmt.n((report.views || {}).dnp_count) + "</b>" +
        '<span class="lbl">board</span><b class="num">' + fmt.esc(String(report.board_md5_before || "").slice(0, 8)) +
          " → " + fmt.esc(String(report.board_md5_after || "").slice(0, 8)) + "</b>" +
        '<span class="lbl">tag</span><b class="num">' + fmt.esc(rel.tag || "—") + "</b>";
      return s;
    }

    function roundSelect(b, report) {
      const wrap = fmt.el("div", "strip moversbar");
      wrap.appendChild(fmt.el("span", "lbl", "Mover report"));
      const sel = fmt.el("select", "boardsel");
      availableRounds(b).forEach(function (r) {
        const o = fmt.el("option", "", "Round " + r + " vs " + (r - 1));
        o.value = String(r); if (r === report.submitted_round) o.selected = true;
        sel.appendChild(o);
      });
      sel.addEventListener("change", function () { state.round = parseInt(sel.value, 10); state.sort = null; render(MD.__moversHolder); });
      wrap.appendChild(sel);

      // view toggle (value risers/fallers, rank risers/fallers, all)
      const seg = fmt.el("div", "seg");
      [["value_risers", "Value risers"], ["value_fallers", "Value fallers"], ["rank_risers", "Rank risers"],
       ["rank_fallers", "Rank fallers"], ["all", "All players"]].forEach(function (d) {
        const btn = fmt.el("button", state.view === d[0] ? "on" : "", d[1]);
        btn.addEventListener("click", function () { state.view = d[0]; state.sort = null; render(MD.__moversHolder); });
        seg.appendChild(btn);
      });
      wrap.appendChild(seg);
      return wrap;
    }

    function filterBar(report) {
      const row = fmt.el("div", "strip moversfilters");
      row.appendChild(fmt.el("span", "lbl", "Filter"));
      // club
      const clubs = {}; (report.players || []).forEach(function (p) { if (p.affl_team) clubs[p.affl_team] = 1; });
      const csel = fmt.el("select", "boardsel");
      csel.appendChild(new Option("All clubs", ""));
      Object.keys(clubs).sort().forEach(function (c) { const o = new Option(fmt.club(c), c); if (c === state.club) o.selected = true; csel.appendChild(o); });
      csel.addEventListener("change", function () { state.club = csel.value || null; render(MD.__moversHolder); });
      row.appendChild(csel);
      // position
      const poss = {}; (report.players || []).forEach(function (p) { if (p.pos) poss[p.pos] = 1; });
      const psel = fmt.el("select", "boardsel");
      psel.appendChild(new Option("All positions", ""));
      Object.keys(poss).sort().forEach(function (c) { const o = new Option(c, c); if (c === state.pos) o.selected = true; psel.appendChild(o); });
      psel.addEventListener("change", function () { state.pos = psel.value || null; render(MD.__moversHolder); });
      row.appendChild(psel);
      // played / DNP
      const stseg = fmt.el("div", "seg");
      [["", "All"], ["played", "Played"], ["dnp", "DNP"]].forEach(function (d) {
        const btn = fmt.el("button", (state.status || "") === d[0] ? "on" : "", d[1]);
        btn.addEventListener("click", function () { state.status = d[0] || null; render(MD.__moversHolder); });
        stseg.appendChild(btn);
      });
      row.appendChild(stseg);
      return row;
    }

    function card(label, p, kind) {
      const c = fmt.el("div", "movercard");
      if (!p) { c.innerHTML = '<div class="mcl">' + label + '</div><div class="mcv">—</div>'; return c; }
      const isVal = kind === "value";
      const d = isVal ? p.value_change : p.rank_change;
      c.innerHTML = '<div class="mcl">' + label + "</div>" +
        '<div class="mcn">' + fmt.esc(p.name) + "</div>" +
        '<div class="mcv ' + fmt.cls(d) + '">' + (isVal ? fmt.signed(d) : (fmt.signed(d) + " places")) + "</div>" +
        '<div class="mcs num">' + (isVal ? (fmt.n(p.prev_value) + " → " + fmt.n(p.cur_value))
                                          : ("rank " + fmt.n(p.prev_rank) + " → " + fmt.n(p.cur_rank))) + "</div>";
      c.addEventListener("click", function () { MD.go("card", p.key); });
      c.style.cursor = "pointer";
      return c;
    }

    function summaryCards(report) {
      const s = core.summary(report);
      const grid = fmt.el("div", "movercards");
      grid.appendChild(card("Largest value increase", s.value_increase, "value"));
      grid.appendChild(card("Largest value decrease", s.value_decrease, "value"));
      grid.appendChild(card("Largest rank improvement", s.rank_improve, "rank"));
      grid.appendChild(card("Largest rank decline", s.rank_decline, "rank"));
      return grid;
    }

    function table(report) {
      let rows = core.viewRows(report, state.view, { club: state.club, pos: state.pos, status: state.status });
      var total = rows.length;
      // the focused views show the headline movers (not the whole ~800 board); "All players" is the
      // complete sortable/filterable table. Keeps the default view from overwhelming, per the spec.
      if (state.view !== "all" && !state.sort) rows = rows.slice(0, 60);
      if (state.sort) rows = rows.slice().sort(core.cmp(state.sort, state.dir));
      const wrap = fmt.el("div", "movertable");
      const head = fmt.el("div", "moverhead");
      const cols = [["cur_rank", "Rank"], ["name", "Player"], ["played", "P/DNP"], ["cur_value", "Value"],
                    ["value_change", "Δ value"], ["value_change_pct", "Δ%"], ["rank_change", "Δ rank"],
                    ["pos_rank_change", "Δ pos"]];
      cols.forEach(function (c) {
        const h = fmt.el("div", "mh" + (c[0] === "name" ? " l" : " r"), c[1]);
        h.setAttribute("data-sort", c[0]);
        h.addEventListener("click", function () {
          if (state.sort === c[0]) state.dir = state.dir === "desc" ? "asc" : "desc";
          else { state.sort = c[0]; state.dir = "desc"; }
          render(MD.__moversHolder);
        });
        head.appendChild(h);
      });
      wrap.appendChild(head);
      const body = fmt.el("div", "moverrows");
      rows.forEach(function (p) {
        const r = fmt.el("div", "moverrow" + (p.dnp ? " dnp" : ""));
        r.setAttribute("data-key", p.key);
        r.innerHTML =
          '<div class="mr rank num">' + fmt.n(p.cur_rank) + "</div>" +
          '<div class="mr who"><span class="nm">' + fmt.esc(p.name) + "</span>" +
            '<span class="sub">' + fmt.esc(p.pos || "—") + " · " + fmt.esc(fmt.club(p.affl_team || p.club || "—")) + "</span></div>" +
          '<div class="mr pdn">' + (p.played
              ? '<span class="pill up">PLAYED ' + fmt.n(p.score) + "</span>"
              : '<span class="pill na">DNP</span>') + "</div>" +
          '<div class="mr val num">' + fmt.n(p.cur_value) + "</div>" +
          '<div class="mr dv"><span class="pill ' + fmt.cls(p.value_change) + '">' + fmt.signed(p.value_change) + "</span></div>" +
          '<div class="mr dvp num ' + fmt.cls(p.value_change) + '">' + (p.value_change_pct == null ? "—" : (p.value_change_pct > 0 ? "+" : "") + p.value_change_pct.toFixed(1) + "%") + "</div>" +
          '<div class="mr dr"><span class="pill ' + fmt.cls(p.rank_change) + '">' + fmt.signed(p.rank_change) + "</span></div>" +
          '<div class="mr dpr num ' + fmt.cls(p.pos_rank_change) + '">' + fmt.signed(p.pos_rank_change) + "</div>";
        r.addEventListener("click", function () { MD.go("card", p.key); });
        body.appendChild(r);
      });
      wrap.appendChild(body);
      const count = fmt.el("div", "movercount", fmt.n(rows.length) + " of " + fmt.n(total) +
        " shown · " + '<span class="num">' + fmt.n((report.views || {}).played_count) + "</span> played · " +
        '<span class="num">' + fmt.n((report.views || {}).dnp_count) + "</span> DNP" +
        (state.view !== "all" && !state.sort && total > rows.length ? " · switch to <b>All players</b> for the complete table" : ""));
      wrap.appendChild(count);
      return wrap;
    }

    function render(holder) {
      MD.__moversHolder = holder;
      holder.innerHTML = "";
      const b = bundle();
      if (!b || !availableRounds(b).length) { failState(holder, "no movers reports available yet"); return; }
      if (state.round == null) state.round = availableRounds(b)[availableRounds(b).length - 1];
      const report = reportFor(b, state.round);
      const intg = core.integrity(report, b);
      if (!intg.ok) { failState(holder, intg.why); return; }
      holder.appendChild(roundSelect(b, report));
      holder.appendChild(metaStrip(report));
      holder.appendChild(summaryCards(report));
      holder.appendChild(filterBar(report));
      holder.appendChild(table(report));
    }

    return { render: render, core: core, _state: state };
  }

  /* ---- registration: browser (window.MD) + node (module.exports for tests) ----------------- */
  if (typeof window !== "undefined") {
    window.MD = window.MD || {};
    // defer construction until MD.fmt exists (script order guarantees it, but be safe)
    window.MD.movers = (window.MD.fmt) ? makeView(window.MD) : { render: function (h) { window.MD.movers = makeView(window.MD); window.MD.movers.render(h); }, core: core };
  }
  if (typeof module !== "undefined" && module.exports) {
    module.exports = { core: core, makeView: makeView };
  }
})(this);
