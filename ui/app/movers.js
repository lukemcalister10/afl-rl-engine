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

    /* The FIXED release-baseline identity fields — immutable across weekly rounds (owner ruling
       2026-07-20). balanced_board_md5 is the fixed PRESENT-LENS baseline anchor (not the final
       full-board hash); the model pins + release_version move only at a separately-approved
       valuation-changing release. They must be identical between every report and the loaded release.
       (board / store / as_of_round are the DYNAMIC weekly fields; `board` is the current artifact.) */
    RELEASE_FIXED: ["release_version", "balanced_board_md5", "engine_head", "rl_model", "fv", "config", "register"],

    sameFixed: function (a, b) {
      a = a || {}; b = b || {};
      for (var i = 0; i < core.RELEASE_FIXED.length; i++) {
        var k = core.RELEASE_FIXED[i];
        if (a[k] == null || b[k] == null || a[k] !== b[k]) return { ok: false, field: k, a: a[k], b: b[k] };
      }
      return { ok: true };
    },

    /* Fail-closed LINEAGE anchoring of the WHOLE bundle against the CURRENT loaded application
       (corrective 2026-07-20, review directives D + E; owner ruling on balanced_board_md5). The bundle
       must sit on the SAME release lineage the working app is loaded at — validated against the FULL
       release contract (window.__MATCHDAY_WORKING__.stamp.release), never abbreviated / self-declared
       stamp fields. For a POPULATED bundle:
         - FIXED identity: every report + the loaded release carry the same balanced_board_md5, and the
           latest report's release_version + engine/rl_model/fv/config/register equal the loaded release;
         - baseline board + store anchor the first report;
         - board AND store continuity between every consecutive report; previous_round == round - 1;
         - the LATEST report board_md5_after == the loaded CURRENT board, and source_store_md5_after ==
           the loaded CURRENT store; as_of_round is coherent (latest report == latest round == loaded).
       For an EMPTY bundle the baseline identity (board, store, fixed pins) is validated against the
       loaded application BEFORE returning the honest empty state — an empty bundle on the wrong lineage
       (e.g. an empty 270a2c5f bundle loaded against a DIFFERENT present-lens baseline board) fails
       closed, it is not "empty". This is generic board/store/release lineage checking: balanced_board_md5
       is the fixed present-lens baseline anchor and the moving `board` field is the complete current
       artifact; it makes no assumption about final switch values or a final full-board hash.
       `app` = {board, store, release} from the loaded working stamp. Absent app.release -> best-effort
       "unanchored" (board/store/chain only); the browser always supplies the full contract. */
    lineage: function (bundle, app) {
      if (!bundle || bundle.kind !== "matchday_movers_bundle") return { ok: false, state: "nobundle", why: "no movers bundle" };
      app = app || {};
      var appRel = app.release || null;
      var rounds = (bundle.rounds || []).slice();
      var reports = bundle.reports || {};
      var baseline = bundle.baseline || {};

      // ---- EMPTY bundle: validate the baseline identity vs the loaded app before the empty state ----
      if (!rounds.length) {
        if (app.board && baseline.board && baseline.board !== app.board)
          return { ok: false, state: "mismatch", why: "empty bundle baseline board " + String(baseline.board).slice(0, 8) +
                   " does not match the loaded app board " + String(app.board).slice(0, 8) };
        if (app.store && baseline.store && baseline.store !== app.store)
          return { ok: false, state: "mismatch", why: "empty bundle baseline store " + String(baseline.store).slice(0, 8) +
                   " does not match the loaded app store " + String(app.store).slice(0, 8) };
        if (appRel) {
          var sfE = core.sameFixed(baseline.release_identity, appRel);
          if (!sfE.ok) return { ok: false, state: "mismatch", why: "empty bundle baseline release identity differs at " + sfE.field };
        }
        return { ok: true, state: "empty", why: "no finalized round reports yet" };
      }

      // ---- POPULATED bundle ----
      var first = reports[String(rounds[0])];
      if (!first) return { ok: false, state: "mismatch", why: "bundle lists round " + rounds[0] + " but has no report for it" };
      if (baseline.board && first.board_md5_before && first.board_md5_before !== baseline.board)
        return { ok: false, state: "mismatch", why: "first report baseline board " + String(first.board_md5_before).slice(0, 8) +
                 " does not match the release baseline board " + String(baseline.board).slice(0, 8) };
      if (baseline.store && first.source_store_md5_before && first.source_store_md5_before !== baseline.store)
        return { ok: false, state: "mismatch", why: "first report baseline store does not match the release baseline store" };
      // fixed balanced_board_md5 identical across EVERY report
      for (var b = 0; b < rounds.length; b++) {
        var rb = reports[String(rounds[b])], rel = (rb || {}).release_identity || {};
        if (baseline.release_identity && baseline.release_identity.balanced_board_md5 &&
            rel.balanced_board_md5 !== baseline.release_identity.balanced_board_md5)
          return { ok: false, state: "mismatch", why: "R" + rounds[b] + " carries a different balanced_board_md5 than the baseline" };
      }
      // board AND store continuity + sequential rounds
      for (var i = 1; i < rounds.length; i++) {
        var cur = reports[String(rounds[i])], prev = reports[String(rounds[i - 1])];
        if (!cur || !prev) return { ok: false, state: "mismatch", why: "a report is missing from the round chain" };
        if (cur.board_md5_before !== prev.board_md5_after)
          return { ok: false, state: "mismatch", why: "board-identity chain break before R" + rounds[i] };
        if (cur.source_store_md5_before !== prev.source_store_md5_after)
          return { ok: false, state: "mismatch", why: "store-identity chain break before R" + rounds[i] };
        if (cur.previous_round !== cur.submitted_round - 1)
          return { ok: false, state: "mismatch", why: "non-sequential rounds at R" + rounds[i] };
      }
      if (bundle.integrity && bundle.integrity.board_chain_ok === false)
        return { ok: false, state: "mismatch", why: "bundle declares a broken board chain" };
      if (bundle.integrity && bundle.integrity.baseline_anchor_ok === false)
        return { ok: false, state: "mismatch", why: "bundle does not anchor to the release baseline board" };

      var last = reports[String(rounds[rounds.length - 1])];
      var lastRel = last.release_identity || {};
      // latest dynamic report vs the loaded CURRENT board + store
      if (app.board && last.board_md5_after !== app.board)
        return { ok: false, state: "mismatch", why: "latest report board " + String(last.board_md5_after).slice(0, 8) +
                 " != loaded current board " + String(app.board).slice(0, 8) };
      if (app.store && last.source_store_md5_after !== app.store)
        return { ok: false, state: "mismatch", why: "latest report store " + String(last.source_store_md5_after).slice(0, 8) +
                 " != loaded current store " + String(app.store).slice(0, 8) };
      // as_of_round coherence
      if (lastRel.as_of_round != null && lastRel.as_of_round !== last.submitted_round)
        return { ok: false, state: "mismatch", why: "latest report as_of_round " + lastRel.as_of_round + " != submitted round " + last.submitted_round };
      if (appRel && appRel.as_of_round != null && lastRel.as_of_round != null && appRel.as_of_round !== lastRel.as_of_round)
        return { ok: false, state: "mismatch", why: "loaded as_of_round " + appRel.as_of_round + " != latest report as_of_round " + lastRel.as_of_round };
      // all FIXED model identity pins + release_version match the loaded release
      if (appRel) {
        var sf = core.sameFixed(lastRel, appRel);
        if (!sf.ok) return { ok: false, state: "mismatch", why: "release identity differs from the loaded release at " + sf.field };
        return { ok: true, state: "ok" };
      }
      return { ok: true, state: "unanchored" };
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

    /* The identity of the working board the app is CURRENTLY loaded at — the lineage anchor. Prefers
       the FULL release contract (stamp.release: full-length board/store + fixed pins) so lineage is
       validated against verified identity, not the abbreviated stamp fields. */
    function appIdentity() {
      var w = (typeof window !== "undefined") && window.__MATCHDAY_WORKING__;
      var st = w && w.stamp;
      if (!st) return null;
      var rel = st.release || null;
      return {
        board: (rel && rel.board) || st.srcmd5 || st.board,
        store: (rel && rel.store) || st.store_md5 || st.store,
        release: rel,
      };
    }

    function availableRounds(b) { return (b && b.rounds) ? b.rounds.slice() : []; }

    function reportFor(b, rnd) { return b && b.reports ? b.reports[String(rnd)] : null; }

    /* HONEST empty state — no finalized round reports yet. This is NOT an integrity alarm and NOT
       scratch data; a fresh baseline (e.g. Round 14) app renders exactly this. */
    function emptyState(holder, why) {
      var box = fmt.el("div", "moversempty");
      box.innerHTML = "<h1>Movers — no finalized round reports yet</h1>" +
        "<p>Weekly movers appear here once a round's scores are applied and <b>finalized</b>. There are " +
        "no finalized round reports on this build, so the view is intentionally empty rather than " +
        "showing placeholder or scratch data.</p>" +
        '<p class="mono">' + fmt.esc(why || "no finalized round reports") + "</p>";
      holder.appendChild(box);
    }

    function failState(holder, why) {
      var box = fmt.el("div", "failclosed");
      box.innerHTML = "<h1>■ Movers unavailable — integrity check failed</h1>" +
        "<p>The Movers view renders only a movers report whose transaction committed and whose board " +
        "identities sit on the SAME lineage as the loaded application. This bundle did not pass the " +
        "lineage / integrity check, so nothing is shown rather than showing stale, out-of-lineage or " +
        "partial data.</p>" +
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
        '<span class="lbl">release</span><b class="num">' + fmt.esc(rel.release_version || "—") + "</b>";
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
      // LINEAGE first: anchor the whole bundle to the loaded application before touching a report.
      const lin = core.lineage(b, appIdentity());
      if (lin.state === "empty") { emptyState(holder, lin.why); return; }   // honest empty, not an alarm
      if (!lin.ok) { failState(holder, lin.why); return; }                  // out-of-lineage -> fail closed
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
