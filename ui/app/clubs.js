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
    { key: "overall", label: "Overall", cls: "overall", tip: "players + picks" },
    { key: "totalPlayer", label: "Player value", cls: "" },
    { key: "totalPicks", label: "Picks value", cls: "picks" },
    { key: "top5", label: "Top-5", cls: "" },
    { key: "top10", label: "Top-10", cls: "" },
    { key: "best23", label: "Best-23", cls: "" },
    { key: "nonBest23", label: "Non-Best-23", cls: "" },
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

  function row(c, rank) {
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
    open.title = "open " + fmt.esc(c.display || c.team) + " on the board (picks included)";
    open.addEventListener("click", function (e) {
      e.preventDefault();
      MD.board.focusClub(c.team, true);   // filter the board to this club + turn picks on
      MD.go("board");
    });
    club.appendChild(open);
    tr.appendChild(club);
    COLS.forEach(function (col) {
      tr.appendChild(fmt.el("td", "num " + col.cls, fmt.n(c[col.key])));
    });
    return tr;
  }

  function render(container) {
    container.innerHTML = "";
    const page = fmt.el("div", "clubspage");
    const cv = MD.seam.club;
    const halt = MD.seam.clubHalt();

    const intro = fmt.el("div", "cintro");
    if (!cv) {
      intro.innerHTML = '<span class="halt">Club-valuation bundle absent.</span> Run ' +
        "<b>python3 ui/tools/ingest_inputs.py</b> to generate <b>ui/data/club_valuation.js</b> " +
        "(see ui/HOW_TO_UPDATE_INPUTS.md).";
      page.appendChild(intro);
      container.appendChild(page);
      return;
    }
    if (halt) {
      intro.innerHTML = '<span class="halt">■ Overlay HALTED by the ingest.</span> ' +
        fmt.esc(halt.reason) + " — nothing is guessed; fix the input and re-run the ingest.";
      page.appendChild(intro);
      container.appendChild(page);
      return;
    }

    const st = cv.stamp || {};
    intro.innerHTML =
      "<b>" + fmt.n((cv.clubs || []).length) + " AFFL clubs</b> ranked by Overall Value " +
      "(players + held picks). Player value is the stamped board <b>" + fmt.esc(st.tag || "") +
      "</b>; picks priced off the canonical PVC (2027 × " + fmt.esc(String(st.mult2027 != null ? st.mult2027 : 0.9)) +
      ", balanced). <b>Best-23</b> = the best positionally-compliant XVIII " +
      "(2 K-DEF · 4 G-DEF · 5 MID · 4 G-FWD · 2 K-FWD · 1 RUC) by board value + 5 best-remaining bench. " +
      "Every column sortable; click a club to open its board view. " +
      "<small>(The AFFL league is 16 clubs + a Free-Agents pool; Free Agents is a pool, not a club, so it is not ranked.)</small>";
    page.appendChild(intro);

    const table = fmt.el("table", "ctable");
    const thead = fmt.el("thead");
    thead.appendChild(header());
    table.appendChild(thead);
    const tbody = fmt.el("tbody");
    sorted(cv.clubs || []).forEach(function (c, i) { tbody.appendChild(row(c, i + 1)); });
    table.appendChild(tbody);
    page.appendChild(table);

    const foot = fmt.el("div", "cfoot");
    foot.textContent = "Non-Best-23 = Total Player Value − Best-23 (roster depth beyond the best XXIII). " +
      "Pure view — no value is recomputed; picks and player values share one currency (pick 1 = 3000).";
    page.appendChild(foot);
    container.appendChild(page);
  }

  return { render: render };
})();
