/* Matchday UI — the TEAM SUMMARY page (item 178(3), the item-173 ranking page, owner-specced).
   One ranked, fully-sortable table over every AFFL club: Overall Value (players + picks) · Total
   Player Value · Total Picks Value · Top-5 · Top-10 · Best-23 · Non-Best-23. Pure view: the numbers
   come from the VALIDATE-OR-HALT ingest bundle (ui/tools/ingest_inputs.py) — this page computes no
   value; Best-23 is a greedy positional SELECTION over the stamped board `v`, done in the ingest. */
window.MD = window.MD || {};

MD.clubs = (function () {
  const fmt = MD.fmt;

  // default sort: Overall Value, descending (owner spec). Every column sortable; numeric.
  let sortKey = "overall";
  let sortDir = "desc";

  const COLS = [
    { key: "overall", label: "Rating", cls: "overall", tip: "the 56-asset club rating" },
    { key: "totalPlayer", label: "Player value", cls: "" },
    { key: "totalPicks", label: "Picks value", cls: "picks" },
    { key: "top5", label: "Top-5", cls: "" },
    { key: "top10", label: "Top-10", cls: "" },
    { key: "best23", label: "Best-23", cls: "" },
    { key: "nonBest23", label: "Depth", cls: "", tip: "player value beyond the best 23" },
  ];

  function sorted(clubs) {
    const arr = clubs.slice();
    arr.sort(function (a, b) {
      const d = (a[sortKey] - b[sortKey]);
      return sortDir === "desc" ? -d : d;
    });
    return arr;
  }

  function header() {
    const tr = fmt.el("tr");
    tr.appendChild(fmt.el("th", "rk", "#"));
    tr.appendChild(fmt.el("th", "club", "Club"));
    COLS.forEach(function (c) {
      const on = c.key === sortKey;
      const th = fmt.el("th", (c.cls ? c.cls + " " : "") + (on ? "on" : ""),
        fmt.esc(c.label) + (on ? '<span class="ar">' + (sortDir === "desc" ? "▼" : "▲") + "</span>" : ""));
      if (c.tip) th.title = c.tip;
      th.addEventListener("click", function () {
        if (sortKey === c.key) { sortDir = sortDir === "desc" ? "asc" : "desc"; }
        else { sortKey = c.key; sortDir = "desc"; }
        MD.render();
      });
      tr.appendChild(th);
    });
    return tr;
  }

  function row(c, rank, picksAvailable) {
    const tr = fmt.el("tr");
    tr.appendChild(fmt.el("td", "rk num", String(rank)));
    const club = fmt.el("td", "club");
    // the club NAME is the pocket-profile target (hover / keyboard-focus / tap on touch → the panel);
    // a separate "open ›" link carries the board navigation, so the two intents never collide on touch.
    const nm = fmt.el("span", "cnm", fmt.esc(c.display || fmt.club(c.team)));
    nm.title = "hover / tap for the pocket profile";
    if (MD.pocket) MD.pocket.attach(nm, c.team);
    club.appendChild(nm);
    const open = fmt.el("a", "copen", "open ›");
    open.href = "#";
    open.title = "open " + fmt.esc(c.display || c.team);
    open.addEventListener("click", function (e) {
      e.preventDefault();
      MD.board.focusClub(c.team);   // the club view always shows roster + held picks
      MD.go("board");
    });
    club.appendChild(open);
    tr.appendChild(club);
    COLS.forEach(function (col) {
      // Picks and Overall are UNAVAILABLE (never 0) when the picks overlay is halted or absent —
      // a printed 0 would understate the club by its entire pick holding and read as a real figure.
      const na = !picksAvailable && (col.key === "totalPicks" || col.key === "overall");
      tr.appendChild(fmt.el("td", "num " + col.cls, na ? "<small>n/a</small>" : fmt.n(c[col.key])));
    });
    return tr;
  }

  function render(container) {
    container.innerHTML = "";
    const page = fmt.el("div", "clubspage");
    // #139 item 21: the player-side totals are computed HERE, in the browser, off the stamped board —
    // they are no longer read from the baked (and twice-stale) club_valuation.js.
    const ct = MD.clubTotals.compute();
    const halt = MD.seam.clubHalt();

    const intro = fmt.el("div", "cintro");
    if (!ct) {
      intro.innerHTML = '<span class="halt">Board bundle absent.</span> The club table is computed from ' +
        "the stamped board, so there is nothing to rank until <b>ui/data/board_view_working.js</b> loads.";
      page.appendChild(intro);
      container.appendChild(page);
      return;
    }

    // REDESIGNED 2026-08-28 (owner word): no description blob — the table is the page. The one
    // sentence that survives is a picks-unavailable warning, because n/a columns need their reason.
    if (!ct.picksAvailable) {
      intro.innerHTML = '<span class="halt">Picks unavailable</span> — ' +
        fmt.esc((ct.picksSource || {}).reason || (halt && halt.reason) || "the picks bundle is absent") +
        ". Rating and Picks show n/a.";
      page.appendChild(intro);
    }

    const table = fmt.el("table", "ctable");
    const thead = fmt.el("thead");
    thead.appendChild(header());
    table.appendChild(thead);
    const tbody = fmt.el("tbody");
    sorted(ct.clubs).forEach(function (c, i) { tbody.appendChild(row(c, i + 1, ct.picksAvailable)); });
    table.appendChild(tbody);
    // Wrap the wide sortable table so it scrolls WITHIN its own region on narrow screens — the document
    // never overflows horizontally (display-only; the table markup + values are unchanged).
    const tablewrap = fmt.el("div", "tablewrap");
    tablewrap.appendChild(table);
    page.appendChild(tablewrap);

    container.appendChild(page);
  }

  return { render: render };
})();
