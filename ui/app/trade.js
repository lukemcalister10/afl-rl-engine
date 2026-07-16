/* Matchday UI — trade desk. Players + picks in ONE SCAR currency (picks off the pick-value curve).
   Q-VERDICT (b): closes with a plain-language verdict sentence; figures alongside; model speaks, owner overrules.
   Totals/gap are arithmetic on given board figures — a difference, NOT a re-valuation of any player. */
window.MD = window.MD || {};

MD.trade = (function () {
  const fmt = MD.fmt;
  let seeded = false;

  function seed() {
    if (seeded) return;
    seeded = true;
    const byKey = MD.seam.indexed().byKey;
    // A real, illustrative starting trade so the desk + verdict render populated on open.
    if (byKey["max-gawn"]) MD.state.trade.give.push({ t: "player", key: "max-gawn" });
    MD.state.trade.give.push({ t: "pick", n: 24 });
    if (byKey["kieren-briggs"]) MD.state.trade.get.push({ t: "player", key: "kieren-briggs" });
    MD.state.trade.get.push({ t: "pick", n: 5 });
  }

  function pickVal(n) {
    const pvc = MD.seam.working.pvc || {};
    return pvc[String(n)] != null ? pvc[String(n)] : 0;
  }

  function itemVal(it) {
    if (it.t === "pick") return pickVal(it.n);
    const p = MD.seam.indexed().byKey[it.key];
    return p ? p.v : 0;
  }

  function maxRail() {
    // rail scale = top player value (shared currency reference)
    return (MD.seam.working.stamp || {}).maxV || 1;
  }

  /* nearest pick to a SCAR amount + a plain-language descriptor of that pick. */
  function describePick(amount) {
    const pvc = MD.seam.working.pvc || {};
    let best = null, bestD = Infinity;
    Object.keys(pvc).forEach(function (k) {
      const d = Math.abs(pvc[k] - amount);
      if (d < bestD) { bestD = d; best = parseInt(k, 10); }
    });
    if (best == null) return "a draft pick";
    const round = Math.ceil(best / 18);
    const within = ((best - 1) % 18) + 1;
    const pos = within <= 6 ? "early" : within <= 12 ? "mid" : "late";
    const ord = ["first", "second", "third", "fourth", "fifth", "sixth"][round - 1] || (round + "th");
    if (best <= 3) return "a top-" + best + " pick";
    return "a " + pos + " " + ord + "-round pick (≈ pick " + best + ")";
  }

  /* item 6: match a query to picks (1–80, individually) + players (type-ahead by name).
     numeric query -> the exact/prefix picks; text query -> player-name substring. */
  function matchItems(q) {
    q = String(q || "").trim().toLowerCase();
    const players = MD.seam.working.players || [];
    const out = [];
    if (!q) {
      players.slice().sort(function (a, b) { return b.v - a.v; }).slice(0, 8)
        .forEach(function (pl) { out.push({ t: "player", key: pl.key, label: pl.name, val: pl.v }); });
      return out;
    }
    if (/^\d+$/.test(q)) {
      for (let n = 1; n <= 80 && out.length < 6; n++) {
        if (String(n).indexOf(q) === 0) out.push({ t: "pick", n: n, label: "Pick " + n, val: pickVal(n) });
      }
    }
    players.filter(function (pl) { return String(pl.name).toLowerCase().indexOf(q) !== -1; })
      .slice(0, 8)
      .forEach(function (pl) { out.push({ t: "player", key: pl.key, label: pl.name, val: pl.v }); });
    return out.slice(0, 12);
  }

  function combo(side, basket, container) {
    const wrap = fmt.el("div", "combo");
    const input = document.createElement("input");
    input.className = "tradesearch";
    input.type = "text";
    input.setAttribute("placeholder", "add — search a player, or type a pick number 1–80…");
    const results = fmt.el("div", "results");
    results.style.display = "none";

    function paint() {
      const items = matchItems(input.value);
      results.innerHTML = "";
      if (!items.length) {
        const none = fmt.el("div", "rnone", "no match — try a name, or a pick number 1–80");
        results.appendChild(none);
      }
      items.forEach(function (it) {
        const b = fmt.el("button");
        const nm = it.t === "pick"
          ? '<span class="rpick">' + fmt.esc(it.label) + " <small>2026 ND</small></span>"
          : '<span>' + fmt.esc(it.label) + "</span>";
        b.innerHTML = nm + '<span class="rv num">' + fmt.n(it.val) + "</span>";
        b.addEventListener("mousedown", function (e) {
          e.preventDefault(); // fire before the input blur so the pick registers
          if (it.t === "pick") basket.push({ t: "pick", n: it.n });
          else basket.push({ t: "player", key: it.key });
          render(container);
        });
        results.appendChild(b);
      });
      results.style.display = "block";
    }
    input.addEventListener("focus", paint);
    input.addEventListener("input", paint);
    input.addEventListener("blur", function () { setTimeout(function () { results.style.display = "none"; }, 120); });
    wrap.appendChild(input);
    wrap.appendChild(results);
    return wrap;
  }

  function pane(side, title, container) {
    const p = fmt.el("div", "pane");
    p.innerHTML = "<h3>" + title + "</h3>";
    const basket = MD.state.trade[side];
    let total = 0;
    basket.forEach(function (it, idx) {
      const val = itemVal(it);
      total += val;
      const row = fmt.el("div", "trow");
      let nm, meta = "";
      if (it.t === "pick") {
        nm = '<span class="pickchip">Pick ' + it.n + "</span>";
        meta = '<i>2026 ND</i>';
      } else {
        const pl = MD.seam.indexed().byKey[it.key];
        const pin = MD.anchors[it.key] ? ' <span class="tpin" title="carries your ★ read">★</span>' : "";
        nm = fmt.esc(pl ? pl.name : it.key) + pin;
        meta = '<i>' + fmt.esc(pl ? pl.pos : "") + (pl && pl.age ? " · " + pl.age + "yo" : "") + "</i>";
      }
      row.innerHTML = '<span class="tnm">' + nm + meta + "</span>" +
        MD.valueLine(val, maxRail(), true) +
        '<span class="tfig num">' + fmt.n(val) + "</span>";
      p.appendChild(row);
    });
    // item 6: a custom type-ahead combobox (replaces the bare <select>) — players are searchable and
    // EVERY pick 1–80 is individually selectable by typing its number; the results dropdown is styled in
    // the board's condensed type (requirement 3: dropdown font matched to the board type style).
    p.appendChild(combo(side, basket, container));

    const tot = fmt.el("div", "ttotal");
    tot.innerHTML = '<span class="k">Total ' + (side === "give" ? "out" : "in") + '</span>' +
      '<span class="tfig num">' + fmt.n(total) + "</span>";
    p.appendChild(tot);
    return { el: p, total: total };
  }

  function verdict(giveTotal, getTotal) {
    const gap = getTotal - giveTotal; // + => you come out ahead
    const v = fmt.el("div", "verdict");
    let gapCls, gapTxt, line;
    if (gap === 0) {
      gapCls = "flat"; gapTxt = "0 SCAR";
      line = "<b>Line-ball.</b> The two sides value out within a whisker.";
    } else if (gap > 0) {
      gapCls = "up"; gapTxt = "+" + fmt.n(gap) + " SCAR";
      line = "You come out <b>ahead by " + fmt.n(gap) + "</b> — about " + describePick(gap) + " of value in your favour.";
    } else {
      gapCls = "dn"; gapTxt = "−" + fmt.n(-gap) + " SCAR";
      line = "You give up <b>" + fmt.n(-gap) + "</b> — roughly " + describePick(-gap) + ".";
    }
    // pinned-player note (the desk shows the read pin whenever a pinned player is on the table)
    const onTable = MD.state.trade.give.concat(MD.state.trade.get)
      .filter(function (it) { return it.t === "player" && MD.anchors[it.key]; })
      .map(function (it) { return MD.seam.indexed().byKey[it.key].name + " (" + MD.anchors[it.key].read + ")"; });
    const pinNote = onTable.length ? " Carries your ★ read: " + onTable.join(", ") + "." : "";
    v.innerHTML = '<div class="gap num ' + gapCls + '">' + gapTxt + "</div>" +
      '<div class="line">' + line + "</div>" +
      '<div class="sub">The model speaks; you overrule.' + pinNote + "</div>";
    return v;
  }

  function render(container) {
    seed();
    container.innerHTML = "";
    if (MD.state.tier === "public") {
      container.innerHTML = '<div class="reserved" style="margin-top:20px"><b>Trade desk is a working-aid view.</b> ' +
        "The public trim publishes values, ranks and movement only — trade tooling stays owner-side.</div>";
      return;
    }
    const desk = fmt.el("div", "desk");
    const give = pane("give", "You give", container);
    const get = pane("get", "You get", container);
    desk.appendChild(give.el);
    desk.appendChild(get.el);
    container.appendChild(desk);
    container.appendChild(verdict(give.total, get.total));

    const tr = fmt.el("div", "translator");
    tr.innerHTML = "<b>Draft translator — arrives after its calibration gate.</b>" +
      "<p>Will sit here: paste a live-draft pick swap, get it restated in board currency. " +
      "Designed in now, wired later; nothing fake rendered until the gate clears.</p>";
    container.appendChild(tr);

    const foot = fmt.el("footer", "foot");
    foot.innerHTML = "one currency: SCAR · picks priced off the pick-value curve (PVC, stamped artifact) · verdict in plain language, figures alongside";
    container.appendChild(foot);
  }

  return { render: render };
})();
