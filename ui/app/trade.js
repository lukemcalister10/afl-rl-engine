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

  /* THE RULED SPLIT (RULEBOOK v2.1 law 4) — the same law ui/tools/ingest_inputs.py:378 price_pick()
     enforces on the ingest side, mirrored here rather than approximated. The national curve prices
     picks 1–64 individually; EVERYTHING past 64 is THE POOL at ONE index, position-blind, "with order
     of selection carrying no value". There is no ordinal pick 65, and no price for pick 70.
     The shipped pvc bundle carries exactly 65 keys: 1–64 = the curve, index 65 = the committed pool
     value. Both halves are READ from that artifact — no number is hard-coded here. */
  const CURVE_MAX = 64;
  const POOL_KEY = "65";
  const POOL_LABEL = "Pool pick — position-blind level";

  // the pool level, one-source read off the bundle. null => the bundle publishes none, so the desk
  // offers no pool item rather than pricing one at a made-up figure (the ingest side HALTs here).
  function poolVal() {
    const pvc = MD.seam.working.pvc || {};
    return pvc[POOL_KEY] != null ? pvc[POOL_KEY] : null;
  }

  // ordinals only, and only inside the curve's domain — index 65 is the pool and is never read as a pick.
  function pickVal(n) {
    const pvc = MD.seam.working.pvc || {};
    if (!(n >= 1 && n <= CURVE_MAX)) return 0;
    return pvc[String(n)] != null ? pvc[String(n)] : 0;
  }

  function pickItem(n) { return { t: "pick", n: n, label: "Pick " + n, val: pickVal(n) }; }
  function poolItem() { return { t: "pick", pool: true, label: POOL_LABEL, val: poolVal() }; }

  function itemVal(it) {
    if (it.t === "pick") {
      if (it.pool) { const pv = poolVal(); return pv != null ? pv : 0; }
      return pickVal(it.n);
    }
    const p = MD.seam.indexed().byKey[it.key];
    return p ? p.v : 0;
  }

  function maxRail() {
    // rail scale = top player value (shared currency reference)
    return (MD.seam.working.stamp || {}).maxV || 1;
  }

  /* nearest pick to a SCAR amount + a plain-language descriptor of that pick. Scans the SAME domain
     the law rules — ordinals 1–64 only. Anything below pick 64's value is the pool, so it describes as
     "a pool pick"; it never invents a phantom ordinal past the end of the curve. */
  /* THE CEILING CLAMP (Phase-0 bug, blind UI review 2026-08-10; located at UI_PARKED_2026-08-21 item 7).
     The nearest-neighbour scan below has a FLOOR clamp and had no ceiling, so every gap above pick 1's
     value nearest-neighboured onto pick 1 and printed "a top-1 pick" — the blind reviewer saw −11,376
     SCAR described as "roughly a top-1 pick" while pick 1 ≈ 3,000. The curve simply does not price a gap
     that size: there is no ordinal above 1, so the honest answer states the gap in units of the curve's
     own top rather than naming a pick that cannot carry it.

     Two rungs, both read off the shipped PVC and neither hardcoded:
       · above the WHOLE FIRST ROUND (Σ picks 1–18) — "more than a whole first round of picks";
       · above pick 1 but not a whole round — "more than pick 1".
     Both carry the multiple of pick 1 so the size is legible, and both are strictly outside the curve's
     domain, so the nearest-neighbour path below is untouched for every amount the curve can actually
     price (including amounts just under pick 1, which correctly read "a top-1 pick"). */
  const ROUND_SIZE = 18;
  function firstRoundValue(pvc) {
    let s = 0;
    for (let n = 1; n <= ROUND_SIZE; n++) {
      const v = pvc[String(n)];
      if (v == null) return null;   // an incomplete curve prices no round total; the rung is skipped
      s += v;
    }
    return s;
  }

  function describePick(amount) {
    const pvc = MD.seam.working.pvc || {};
    const floor = pvc[String(CURVE_MAX)];
    if (floor != null && amount < floor) return "a pool pick";
    const top = pvc["1"];
    if (top != null && top > 0 && amount > top) {
      const mult = amount / top;
      const times = (mult >= 10 ? Math.round(mult) : Math.round(mult * 10) / 10) + "× pick 1";
      const r1 = firstRoundValue(pvc);
      if (r1 != null && amount >= r1) return "more than a whole first round of picks (≈ " + times + ")";
      return "more than pick 1 (≈ " + times + ")";
    }
    let best = null, bestD = Infinity;
    for (let n = 1; n <= CURVE_MAX; n++) {
      const v = pvc[String(n)];
      if (v == null) continue;
      const d = Math.abs(v - amount);
      if (d < bestD) { bestD = d; best = n; }
    }
    if (best == null) return "a draft pick";
    const round = Math.ceil(best / 18);
    const within = ((best - 1) % 18) + 1;
    const pos = within <= 6 ? "early" : within <= 12 ? "mid" : "late";
    const ord = ["first", "second", "third", "fourth", "fifth", "sixth"][round - 1] || (round + "th");
    if (best <= 3) return "a top-" + best + " pick";
    return "a " + pos + " " + ord + "-round pick (≈ pick " + best + ")";
  }

  /* item 6: match a query to picks (ordinals 1–64 individually, plus the ONE pool item) + players
     (type-ahead by name). numeric query -> the exact/prefix ordinals AND the pool, because a number
     past 64 IS the pool under law 4; text query -> "pool", or a player-name substring. */
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
      for (let n = 1; n <= CURVE_MAX && out.length < 6; n++) {
        if (String(n).indexOf(q) === 0) out.push(pickItem(n));
      }
      // typing "70" answers with the pool, not a phantom ordinal — that is what a pick past 64 is.
      if (poolVal() != null) out.push(poolItem());
    } else if (q && "pool pick".indexOf(q) === 0 && poolVal() != null) {
      out.push(poolItem());
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
    input.setAttribute("placeholder", "add — search a player, type a pick number 1–64, or “pool”…");
    const results = fmt.el("div", "results");
    results.style.display = "none";

    function paint() {
      const items = matchItems(input.value);
      results.innerHTML = "";
      if (!items.length) {
        const none = fmt.el("div", "rnone", "no match — try a name, a pick number 1–64, or “pool”");
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
          if (it.t === "pick") basket.push(it.pool ? { t: "pick", pool: true } : { t: "pick", n: it.n });
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
        nm = '<span class="pickchip">' + (it.pool ? "Pool pick" : "Pick " + it.n) + "</span>";
        meta = it.pool ? '<i>2026 ND · position-blind level</i>' : '<i>2026 ND</i>';
      } else {
        const pl = MD.seam.indexed().byKey[it.key];
        const pin = "";   // the ★ read pin is retired from every surface (owner word 2026-08-28)
        nm = fmt.esc(pl ? pl.name : it.key) + pin;
        meta = '<i>' + fmt.esc(pl ? pl.pos : "") + (pl && pl.age ? " · " + pl.age + "yo" : "") + "</i>";
      }
      row.innerHTML = '<span class="tnm">' + nm + meta + "</span>" +
        MD.valueLine(val, maxRail(), true) +
        '<span class="tfig num">' + fmt.n(val) + "</span>";
      p.appendChild(row);
    });
    // item 6: a custom type-ahead combobox (replaces the bare <select>) — players are searchable and
    // every ORDINAL pick 1–64 is individually selectable by typing its number, with the single pool item
    // covering everything past 64; the results dropdown is styled in the board's condensed type
    // (requirement 3: dropdown font matched to the board type style).
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
    v.innerHTML = '<div class="gap num ' + gapCls + '">' + gapTxt + "</div>" +
      '<div class="line">' + line + "</div>";
    return v;
  }

  function render(container) {
    seed();
    container.innerHTML = "";
    const desk = fmt.el("div", "desk");
    const give = pane("give", "You give", container);
    const get = pane("get", "You get", container);
    desk.appendChild(give.el);
    desk.appendChild(get.el);
    container.appendChild(desk);
    container.appendChild(verdict(give.total, get.total));

    // The "Draft translator" promise-placeholder used to render here; an unwired feature is not
    // screen furniture (owner word 2026-08-28). describePick stays live for when it is wired.
  }

  /* describePick is exposed so the defect suite can exercise the EXACT shipped translator (same
     doctrine as counting.js): a pure function of an amount and the stamped PVC, reading no DOM and
     computing no price. */
  return { render: render, describePick: describePick };
})();
