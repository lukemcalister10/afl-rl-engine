/* Matchday UI — router + masthead. Dark-only (Q-THEME a). Fail-closed on ring-fence rejection. */
window.MD = window.MD || {};

(function () {
  const fmt = MD.fmt;
  const root = (typeof document !== "undefined") ? document.getElementById("root") : null;

  // ---- release/round labels from the durable metadata contract (no hardcoded v2.10 / Round 17) -----
  // The stamp carries releaseVersion / asOfRound VERBATIM from data/expected_boot.json (via the
  // extractor). When either is unset the label is a NEUTRAL UNKNOWN — never an invented version or
  // round. On MD so the seam tests exercise the exact functions the masthead renders.
  function releaseLabel(st) {
    const v = st && st.releaseVersion;
    return (v === null || v === undefined || v === "") ? "unversioned" : String(v);
  }
  function roundLabel(st) {
    const r = st && st.asOfRound;
    return (r === null || r === undefined || r === "") ? "Round —" : "Round " + r;
  }
  MD.releaseLabel = releaseLabel;
  MD.roundLabel = roundLabel;

  function failClosed(fence) {
    root.innerHTML =
      '<div class="failclosed"><h1>■ Board rejected — fail-closed</h1>' +
      "<p>This screen renders only the expected, stamped board. The loaded board did not pass the id ring-fence " +
      "(the UI analogue of Guard 5), so nothing is shown rather than showing an unauthenticated or wrong board.</p>" +
      '<p class="mono">reason: ' + fmt.esc(fence.why) +
        (fence.got ? " · got " + fmt.esc(fence.got) + " · want " + fmt.esc(fence.want) : "") + "</p></div>";
  }

  /* REDESIGNED 2026-08-28 (owner word): one clean masthead — the round, the year, the player
     count. Identity/provenance chrome lives in ui/MAINTAINER.md, never on this surface; the seam
     ring-fence still fail-closes the whole page if the data is not the stamped board. */
  function masthead() {
    const st = MD.seam.working.stamp || {};
    const mast = fmt.el("header", "mast");
    mast.innerHTML = '<div class="brand">Value<b>Board</b><span class="sub">AFFL Keeper League</span></div>';
    mast.appendChild(fmt.el("div", "spacer"));
    const stamp = fmt.el("div", "stamp");
    stamp.innerHTML = roundLabel(st) + " · " + (st.baseYear || 2026) + " · " + fmt.n(st.nPlayers) + " players";
    mast.appendChild(stamp);
    return { mast: mast };
  }

  /* #139 items 2, 13 and 14 — the tab list.
     · item 2  — "Round review" is RETIRED (owner word 2026-07-28: "Movers is fine, round review can
                 go"). It never rendered a real round: it was a reserved placeholder waiting on the
                 weekly loop, and Movers became that surface. review.js is deleted with it.
     · item 13 — "Board" is renamed "AFFL Rankings".
     · item 14 — every tab carries a subtitle beneath the main title (third element). */
  const TABS = [
    ["board",  "AFFL Rankings", "Player Rankings"],
    ["clubs",  "Clubs",         "Club Breakdown"],
    ["card",   "Player card",   "Player Profiles"],
    ["trade",  "Trade desk",    "Trade Desk"],
    ["movers", "Movers",        "Weekly Review"],
    ["config", "Config",         "Settings"],
  ];
  MD.TABS = TABS;

  function tabDef(view) {
    for (let i = 0; i < TABS.length; i++) if (TABS[i][0] === view) return TABS[i];
    return null;
  }

  /* item 14: the active tab's title + subtitle, beneath the masthead and above the view. */
  function viewTitle() {
    const d = tabDef(MD.state.view);
    if (!d) return null;
    const el = fmt.el("div", "viewtitle");
    el.innerHTML = "<h1>" + fmt.esc(d[1]) + "</h1><p>" + fmt.esc(d[2]) + "</p>";
    return el;
  }

  function controls(container) {
    const s = MD.state;
    const row = fmt.el("div", "controls");

    /* #139 item 15 — UNIVERSAL BACK. Previously the only Back lived on the player card and always went
       to the board, so club → player → Back dropped you on the all-player list and player → club had no
       Back at all. This one returns to the ACTUAL previous product page, whatever it was, and restores
       the board's own filter state with it (see MD.board.snapshot/restore). Rendered only when there is
       somewhere to go back TO — a dead control is worse than no control. */
    if ((s.nav || []).length) {
      const prev = s.nav[s.nav.length - 1];
      const pd = tabDef(prev.view);
      const backWrap = fmt.el("div", "backnav");
      const btn = fmt.el("button", "", "← Back");
      btn.title = "Back to " + ((pd && pd[1]) || prev.view) +
        (prev.board && prev.board.clubFilter ? " · " + fmt.club(prev.board.clubFilter) : "");
      btn.addEventListener("click", function () { MD.back(); });
      backWrap.appendChild(btn);
      row.appendChild(backWrap);
    }

    const tabs = fmt.el("div", "tabs");
    TABS.forEach(function (d) {
      const btn = fmt.el("button", s.view === d[0] ? "on" : "", d[1]);
      btn.addEventListener("click", function () { MD.go(d[0]); });
      tabs.appendChild(btn);
    });
    row.appendChild(tabs);

    container.appendChild(row);   // the tier toggle is gone: ONE transparent board (owner word 2026-08-28)
  }

  function render() {
    const fence = MD.seam.ringFence();
    if (!fence.ok) { failClosed(fence); return; }
    const s = MD.state;
    root.innerHTML = "";
    const mh = masthead();
    const app = fmt.el("div", "app");
    app.appendChild(mh.mast);
    controls(app);
    const vt = viewTitle();                 // item 14: tab subtitle beneath the main title
    if (vt) app.appendChild(vt);
    const holder = fmt.el("div");
    app.appendChild(holder);
    root.appendChild(app);

    if (s.view === "board") MD.board.render(holder);
    else if (s.view === "clubs") MD.clubs.render(holder);
    else if (s.view === "config") MD.configview.render(holder);
    else if (s.view === "card") MD.card.render(holder);
    else if (s.view === "trade") MD.trade.render(holder);
    else if (s.view === "movers") MD.movers.render(holder);
  }

  /* #139 item 15 — the navigation stack. A location is the whole visible product page: the view, the
     tier, the selected player AND the board's filter state, because "the previous page" means the board
     you were actually looking at, not merely the board tab. Capped so a long session cannot grow it
     without bound; consecutive duplicates are not pushed, so Back never appears to do nothing. */
  const NAV_MAX = 50;

  function here() {
    return {
      view: MD.state.view,
      tier: MD.state.tier,
      cardKey: MD.state.cardKey,
      board: (MD.board && MD.board.snapshot) ? MD.board.snapshot() : null,
    };
  }
  function sameLocation(a, b) {
    if (!a || !b) return false;
    return a.view === b.view && a.tier === b.tier && a.cardKey === b.cardKey &&
      JSON.stringify(a.board) === JSON.stringify(b.board);
  }

  MD.go = function (view, key) {
    const from = here();
    MD.state.view = view;
    if (view === "card" && key) MD.state.cardKey = key;
    if (view === "card" && !MD.state.cardKey) {
      // default to the top-ranked player if none picked yet
      const top = (MD.seam.working.players || []).slice().sort(function (a, b) { return b.v - a.v; })[0];
      MD.state.cardKey = top ? top.key : null;
    }
    if (!sameLocation(from, here())) {
      MD.state.nav.push(from);
      if (MD.state.nav.length > NAV_MAX) MD.state.nav.shift();
    }
    render();
    window.scrollTo(0, 0);
  };

  MD.back = function () {
    const prev = (MD.state.nav || []).pop();
    if (!prev) return false;
    MD.state.view = prev.view;
    MD.state.tier = prev.tier;
    MD.state.cardKey = prev.cardKey;
    if (MD.board && MD.board.restore) MD.board.restore(prev.board);
    render();
    window.scrollTo(0, 0);
    return true;
  };

  MD.render = render;
  // Only auto-mount in a real browser; under a headless test harness (no document) the module just
  // exposes MD.releaseLabel / MD.roundLabel for the seam tests without trying to render.
  if (typeof document !== "undefined" && document.addEventListener) {
    document.addEventListener("DOMContentLoaded", render);
    if (document.readyState !== "loading") render();
  }
})();
