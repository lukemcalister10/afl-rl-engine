/* Matchday UI — router + masthead. Dark-only (Q-THEME a). Fail-closed on ring-fence rejection. */
window.MD = window.MD || {};

(function () {
  const fmt = MD.fmt;
  const root = document.getElementById("root");

  function failClosed(fence) {
    root.innerHTML =
      '<div class="failclosed"><h1>■ Board rejected — fail-closed</h1>' +
      "<p>This screen renders only the expected, stamped board. The loaded board did not pass the id ring-fence " +
      "(the UI analogue of Guard 5), so nothing is shown rather than showing an unauthenticated or wrong board.</p>" +
      '<p class="mono">reason: ' + fmt.esc(fence.why) +
        (fence.got ? " · got " + fmt.esc(fence.got) + " · want " + fmt.esc(fence.want) : "") + "</p></div>";
  }

  function masthead() {
    const s = MD.state, st = MD.seam.working.stamp || {};
    const pub = s.tier === "public";
    const bar = fmt.el("div", "pitchbanner");
    bar.textContent = pub
      ? "Player Values · public trim — values · ranks · movement"
      : "Working aid · live board · reads · rules · controls";

    const mast = fmt.el("header", "mast");
    mast.innerHTML = '<div class="brand">Value<b>Board</b><span class="sub">' +
      (pub ? "Player Values" : "Real-Draft Value Engine") + "</span></div>";
    mast.appendChild(fmt.el("div", "spacer"));
    const stamp = fmt.el("div", "stamp");
    if (pub) {
      stamp.innerHTML = "Round 17 · " + (st.baseYear || 2026) + "<br>movement vs previous round · " +
        fmt.n(st.nPlayers) + " players";
    } else {
      stamp.innerHTML = "board <b>" + st.tag + "</b> · engine <b>" + st.engine + "</b> · store <b>" + st.store +
        "</b> · board id <b>" + st.board + '</b><span class="badge">real</span><span class="badge ok">guard 5 pass</span><br>' +
        "Δ " + (s.deltaBase === "bake" ? "vs last accepted bake" : "vs previous round") + " · " +
        fmt.n(st.nPlayers) + " players · panel " + fmt.esc((st.panel || "").split(" ")[1] || "10/10");
    }
    mast.appendChild(stamp);
    return { bar: bar, mast: mast };
  }

  function controls(container) {
    const s = MD.state;
    const row = fmt.el("div", "controls");
    const tabs = fmt.el("div", "tabs");
    const defs = [["board", "Board"], ["card", "Player card"], ["trade", "Trade desk"], ["review", "Round review"]];
    defs.forEach(function (d) {
      const btn = fmt.el("button", s.view === d[0] ? "on" : "", d[1]);
      btn.addEventListener("click", function () { MD.go(d[0]); });
      tabs.appendChild(btn);
    });
    row.appendChild(tabs);

    const tier = fmt.el("div", "tier");
    [["working", "Working"], ["public", "Public"]].forEach(function (d) {
      const btn = fmt.el("button", s.tier === d[0] ? "on" : "", d[1]);
      btn.addEventListener("click", function () { s.tier = d[0]; render(); });
      tier.appendChild(btn);
    });
    row.appendChild(tier);
    container.appendChild(row);
  }

  function render() {
    const fence = MD.seam.ringFence();
    if (!fence.ok) { failClosed(fence); return; }
    const s = MD.state;
    root.innerHTML = "";
    const mh = masthead();
    root.appendChild(mh.bar);
    const app = fmt.el("div", "app");
    app.appendChild(mh.mast);
    controls(app);
    const holder = fmt.el("div");
    app.appendChild(holder);
    root.appendChild(app);

    if (s.view === "board") MD.board.render(holder);
    else if (s.view === "card") MD.card.render(holder);
    else if (s.view === "trade") MD.trade.render(holder);
    else if (s.view === "review") MD.review.render(holder);
  }

  MD.go = function (view, key) {
    MD.state.view = view;
    if (view === "card" && key) MD.state.cardKey = key;
    if (view === "card" && !MD.state.cardKey) {
      // default to the top-ranked player if none picked yet
      const top = (MD.seam.working.players || []).slice().sort(function (a, b) { return b.v - a.v; })[0];
      MD.state.cardKey = top ? top.key : null;
    }
    render();
    window.scrollTo(0, 0);
  };

  MD.render = render;
  document.addEventListener("DOMContentLoaded", render);
  if (document.readyState !== "loading") render();
})();
