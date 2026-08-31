/* Matchday UI — THE CONFIG TAB. One setting today: which universe the app reads in.

   OWNER REQUEST, 2026-08-31, verbatim:
     "Can we have a config tab, and on the config tab, the option to have model changes 'on' or 'off'
      - this just dictates whether they appear in the movers list and player cards or not. On the
      player cards for example, ideally the default is just the player's progression over the rounds
      since 14 under the live model (and only reviewing the changes if you choose to tick it on).
      Ditto the movers list round 14-24 and FW1 are the options, not the model changes unless you
      turn it on"

   WHY THIS IS A UNIVERSE SWITCH AND NOT A "HIDE ROWS" CHECKBOX. Hiding the model-change points from
   a selector would not remove their EFFECT: a comparison from R14 to FW1 across hidden points still
   carries every model move inside its number, it just stops saying so. That is how a reader gets
   quietly misled, and it is the opposite of what the owner asked for. So OFF does not hide rows — it
   changes which pricing the app reads: the retrospective series, where every round is re-priced under
   the live model, so one model holds across the whole span and the difference is football.

   The switch is per-viewer and lives in localStorage. It changes NO data and recomputes NO value;
   both universes are already in the shipped bundle. */
window.MD = window.MD || {};

MD.configview = (function () {
  const fmt = MD.fmt;

  function counts() {
    const b = window.__MATCHDAY_MOVERS__ || {};
    const U = MD.universe;
    const was = U.mode();
    U.setMode(U.CURRENT); const nCur = U.points(b).length;
    U.setMode(U.ALL);     const nAll = U.points(b).length;
    U.setMode(was);
    return { cur: nCur, all: nAll, mc: Object.keys(U.modelChangeIds(b)).length };
  }

  function render(container) {
    container.innerHTML = "";
    const U = MD.universe;
    const c = counts();
    const on = U.mode() === U.ALL;

    const page = fmt.el("div", "page cfgpage");
    page.appendChild(fmt.el("h1", "", "Config"));
    page.appendChild(fmt.el("div", "sub", "How the app reads its own history"));

    const card = fmt.el("div", "panel cfgpanel");
    const head = fmt.el("div", "cfgrow");
    const lab = fmt.el("div", "cfglab");
    lab.appendChild(fmt.el("div", "cfgtitle", "Show model changes"));
    lab.appendChild(fmt.el("div", "cfgnote",
      "Off — every round is read under the CURRENT model, so a change from one point to another is "
      + "football and nothing else. This is the default and it is what the Movers list and the player "
      + "cards show unless you turn this on."));
    lab.appendChild(fmt.el("div", "cfgnote",
      "On — the record as it was served each week, model changes included. A span that crosses one "
      + "carries the model's movement inside its number as well as the football."));
    head.appendChild(lab);

    const btn = fmt.el("button", "cfgtoggle" + (on ? " on" : ""), on ? "ON" : "OFF");
    btn.setAttribute("role", "switch");
    btn.setAttribute("aria-checked", on ? "true" : "false");
    btn.addEventListener("click", function () {
      U.setMode(U.mode() === U.ALL ? U.CURRENT : U.ALL);
      render(container);
    });
    head.appendChild(btn);
    card.appendChild(head);

    /* THE COUNTS ARE MEASURED FROM THE SHIPPED BUNDLE, not described. A viewer deciding whether to
       flip this deserves to see what it actually changes, and a number that is read cannot drift
       away from the thing it describes. */
    const facts = fmt.el("div", "cfgfacts");
    facts.appendChild(fmt.el("div", "", "Current model: " + c.cur + " points"));
    facts.appendChild(fmt.el("div", "", "All-in: " + c.all + " points"));
    facts.appendChild(fmt.el("div", "", c.mc + " model changes have landed"));
    card.appendChild(facts);

    page.appendChild(card);
    container.appendChild(page);
  }

  return { render: render };
})();
