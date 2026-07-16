/* Matchday UI v1.3 — CLUB POCKET-PROFILE + POSITIONAL BREAKDOWN (item 196(1)(2)(3)).
   A hover/tap panel shown on a club anywhere it renders RANKED (the Clubs summary rows, the board's
   ranked club headers/banner).  PURE VIEW: every figure is read from the stamped bundles —
   club_valuation.js (the 7 pocket metrics + club PLAYER value) and the board bundle (`v`), with the
   values-free position map (positions_data.js) driving the counting rule.  Nothing is recomputed;
   Best-23 is the ingest's existing exact greedy, read from the bundle.  League average = the mean over
   the 16 ranked clubs; the Free-Agents pool is excluded from every denominator (item 191). */
window.MD = window.MD || {};

MD.pocket = (function () {
  const fmt = MD.fmt, C = MD.counting;
  const POS = window.__CLUB_POSITIONS__ || null;
  const FREE = "Free Agents";

  // the 7 pocket metrics, in the owner's order.
  const METRICS = [
    { key: "overall", label: "Overall" },
    { key: "totalPlayer", label: "Player" },
    { key: "totalPicks", label: "Picks" },
    { key: "top5", label: "Top-5" },
    { key: "top10", label: "Top-10" },
    { key: "best23", label: "Best-23" },
    { key: "nonBest23", label: "Non-Best-23" },
  ];

  let _cache = null;
  /* All aggregates are functions of the stamped bundles only (independent of lens / Δ-base / sort),
     so they are computed once.  Positional sums use the board `v` — the same figure club_valuation's
     totalPlayer is built from — so Σ(positions) == totalPlayer exactly (the % denominator is clean). */
  function compute() {
    if (_cache) return _cache;
    const cv = MD.seam.club;
    if (!cv || cv.halt || !cv.clubs || !cv.clubs.length) return null;
    const clubs = cv.clubs;
    const nClubs = clubs.length;

    const avg = {};
    METRICS.forEach(function (m) {
      avg[m.key] = clubs.reduce(function (s, c) { return s + (c[m.key] || 0); }, 0) / nClubs;
    });

    const byTeamPos = {}, unlisted = {};
    (MD.seam.working && MD.seam.working.players || []).forEach(function (p) {
      const t = p.affl_team;
      if (!t || t === FREE) return;
      if (!byTeamPos[t]) byTeamPos[t] = {};
      const codes = POS && POS.byKey ? POS.byKey[p.key] : null;
      const val = p.v;                                   // board value; matches club_valuation totals
      if (codes && codes.length) C.accumulate(byTeamPos[t], codes, val);
      else unlisted[t] = (unlisted[t] || 0) + val;       // full coverage today; guarded regardless
    });

    const posAvg = {};
    C.POSITIONS.forEach(function (pos) {
      posAvg[pos] = clubs.reduce(function (s, c) {
        return s + ((byTeamPos[c.team] || {})[pos] || 0);
      }, 0) / nClubs;
    });

    _cache = { clubs: clubs, byTeam: {}, avg: avg, byTeamPos: byTeamPos, posAvg: posAvg,
               unlisted: unlisted, nClubs: nClubs, stamp: cv.stamp || {} };
    clubs.forEach(function (c) { _cache.byTeam[c.team] = c; });
    return _cache;
  }

  function pct(v, d) {
    if (!d) return "—";
    return (v / d * 100).toFixed(1) + "%";
  }
  /* "vs league average" — signed distance from the mean + the ratio, colour never the sole carrier. */
  function vsAvg(v, a) {
    const d = v - a;
    const ratio = a ? (v / a).toFixed(2) + "×" : "—";
    return '<span class="pk-vs ' + fmt.cls(d) + '">' + fmt.signed(d) +
      ' <small>' + ratio + '</small></span>';
  }

  function metricRows(club, agg) {
    let h = "";
    METRICS.forEach(function (m) {
      const v = club[m.key] || 0;
      h += '<tr><td class="pk-lbl">' + fmt.esc(m.label) + "</td>" +
        '<td class="num pk-abs">' + fmt.n(v) + "</td>" +
        '<td class="num pk-pct">' + pct(v, club.overall) + "</td>" +
        '<td class="num">' + vsAvg(v, agg.avg[m.key]) + "</td></tr>";
    });
    return h;
  }

  function positionRows(club, agg) {
    const pv = (agg.byTeamPos[club.team]) || {};
    let h = "";
    C.POSITIONS.forEach(function (pos) {
      const v = pv[pos] || 0;
      h += '<tr><td class="pk-lbl">' + fmt.esc(C.LABELS[pos]) + "</td>" +
        '<td class="num pk-abs">' + fmt.n(v) + "</td>" +
        '<td class="num pk-pct">' + pct(v, club.totalPlayer) + "</td>" +
        '<td class="num">' + vsAvg(v, agg.posAvg[pos]) + "</td></tr>";
    });
    const un = agg.unlisted[club.team];
    if (un) {
      h += '<tr><td class="pk-lbl" style="color:var(--alarm)">Unlisted</td>' +
        '<td class="num pk-abs">' + fmt.n(un) + '</td><td class="num pk-pct">' +
        pct(un, club.totalPlayer) + '</td><td class="num">—</td></tr>';
    }
    return h;
  }

  function panelHTML(teamLong) {
    const agg = compute();
    if (!agg) return null;
    const club = agg.byTeam[teamLong];
    if (!club) return null;
    const disp = club.display || fmt.club(teamLong);
    const head =
      '<div class="pk-head"><span class="pk-name">' + fmt.esc(disp) + "</span>" +
      '<span class="pk-sub">pocket profile · vs a ' + agg.nClubs + "-club league</span></div>";

    const colhead = '<thead><tr><th></th><th class="num">abs</th>' +
      '<th class="num">% ovr</th><th class="num">vs avg</th></tr></thead>';
    const posColhead = '<thead><tr><th></th><th class="num">abs</th>' +
      '<th class="num">% player</th><th class="num">vs avg</th></tr></thead>';

    const block1 = '<div class="pk-sec">Value pockets</div>' +
      '<table class="pk-tbl">' + colhead + "<tbody>" + metricRows(club, agg) + "</tbody></table>";
    const block2 = '<div class="pk-sec">Positional value <small>(owner counting rule)</small></div>' +
      '<table class="pk-tbl">' + posColhead + "<tbody>" + positionRows(club, agg) + "</tbody></table>";

    const foot = '<div class="pk-foot">' +
      "League average = mean over the " + agg.nClubs + " ranked clubs; the Free-Agents pool is " +
      "excluded from every denominator and is never ranked (item 191). Positional value uses the " +
      "owner rule, collapse-first — a Key listing absorbs its General counterpart (Key-Fwd absorbs " +
      "Gen-Fwd, Key-Def absorbs Gen-Def; the General token is slot eligibility, not a second position). " +
      "After that collapse a player counts 1 to his position, a DPP player 0.5 to each, except a DPP " +
      "midfielder (the non-mid counts 1, the mid 0). Best-23 is the existing exact greedy." +
      "</div>";
    return head + block1 + block2 + foot;
  }

  // ------------------------------------------------------------------ the single floating panel
  let panel = null, hideTimer = null, pinnedTarget = null;
  function ensurePanel() {
    if (panel) return panel;
    panel = fmt.el("div", "pocketpanel");
    panel.setAttribute("role", "tooltip");
    panel.style.display = "none";
    panel.addEventListener("mouseenter", function () { clearTimeout(hideTimer); });
    panel.addEventListener("mouseleave", scheduleHide);
    document.body.appendChild(panel);
    document.addEventListener("click", function (e) {
      if (pinnedTarget && panel.style.display !== "none" &&
          !panel.contains(e.target) && e.target !== pinnedTarget) { hide(); }
    });
    return panel;
  }
  function position(target) {
    const r = target.getBoundingClientRect();
    const p = ensurePanel();
    p.style.display = "block";
    const pw = p.offsetWidth, ph = p.offsetHeight;
    let left = r.left, top = r.bottom + 8;
    if (left + pw > window.innerWidth - 10) left = Math.max(10, window.innerWidth - pw - 10);
    if (top + ph > window.innerHeight - 10) top = Math.max(10, r.top - ph - 8);
    p.style.left = Math.max(10, left) + "px";
    p.style.top = Math.max(10, top) + "px";
  }
  function show(target, teamLong) {
    const html = panelHTML(teamLong);
    if (!html) return;
    clearTimeout(hideTimer);
    const p = ensurePanel();
    p.innerHTML = html;
    position(target);
  }
  function hide() { if (panel) panel.style.display = "none"; pinnedTarget = null; }
  function scheduleHide() { clearTimeout(hideTimer); hideTimer = setTimeout(hide, 140); }

  /* attach hover + keyboard-focus + tap to a club-name element that renders ranked. */
  function attach(el, teamLong) {
    if (!el || !teamLong) return el;
    el.classList.add("pk-target");
    el.setAttribute("tabindex", "0");
    el.addEventListener("mouseenter", function () { pinnedTarget = null; show(el, teamLong); });
    el.addEventListener("mouseleave", scheduleHide);
    el.addEventListener("focus", function () { show(el, teamLong); });
    el.addEventListener("blur", scheduleHide);
    el.addEventListener("click", function (e) {
      // tap-to-pin on touch (no lingering hover); a second tap / outside tap dismisses.
      if (pinnedTarget === el && panel && panel.style.display !== "none") { hide(); return; }
      e.stopPropagation();
      pinnedTarget = el; show(el, teamLong);
    });
    return el;
  }

  /* is there a ranked-club pocket profile for this team? (Free Agents / unknown → no target). */
  function has(teamLong) {
    const agg = compute();
    return !!(agg && agg.byTeam[teamLong]);
  }

  return { attach: attach, panelHTML: panelHTML, compute: compute, hide: hide, has: has };
})();
