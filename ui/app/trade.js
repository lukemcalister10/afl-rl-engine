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
    MD.state.trade.give.push({ t: "pick", n: 24, year: baseYear() });
    if (byKey["kieren-briggs"]) MD.state.trade.get.push({ t: "player", key: "kieren-briggs" });
    MD.state.trade.get.push({ t: "pick", n: 5, year: baseYear() });
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

  /* THE BASE YEAR IS THE BOARD'S OWN, never a literal. Every pick chip on this desk used to read
     "2026 ND" from a string typed into two places — a fact about one bake wearing the look of a law,
     and wrong the morning the base year moves. It is read from the bundle stamp instead. A bundle that
     carries no base year cannot name the year of a pick, so the chips read a plain "ND": the desk still
     prices the curve, it simply does not claim a year it was never told. */
  function baseYear() {
    const y = (MD.seam.working.stamp || {}).baseYear;
    return typeof y === "number" && y > 0 ? y : null;
  }

  /* ITEM 7 (owner word 2026-08-31): "can future picks please be searchable — not just 2026 picks?"

     THE PRICE OF A FUTURE PICK IS NOT THIS VIEW'S TO COMPUTE. It is the owner's year rule — 2026 = own
     projected band at full price; 2027 = (1/3 own + 2/3 round average) × 0.9; 2028 = round average
     × 0.8, both multipliers READ from his Ladder sheet (2026-08-30) — and it is enforced in exactly one
     place, ui/tools/ingest_inputs.py price_pick(). Its answer already ships: every pick in
     ui/data/club_valuation.js carries the year-weighted `value`, and the bundle stamp states the rule
     verbatim in `yearRule`. This desk READS that ledger and re-derives nothing. It could not honestly
     re-derive it anyway — "own projected band" comes off the workbook's Ladder projection, which is in
     no bundle this page loads — so a desk that computed its own 2027 price would be inventing one.

     THE LEDGER IS REACHED THROUGH THE SEAM, not off the raw bundle, so this surface inherits the one
     choke point seam.js established (clubHalt / picksFor): a picks bundle that is not this tree's
     yields nothing here for the same reason it yields nothing to the clubs page and the board overlay.
     A stale pick price is a wrong number wearing the look of a right one, and there is no fallback the
     browser could compute in its place — so the desk offers no future pick at all rather than a price. */
  let _byYear = null;
  function futureIndex() {
    if (_byYear) return _byYear;
    const out = {};
    _byYear = out;
    const seam = MD.seam;
    const base = baseYear();
    // no base year, no picks reader, or a halted/refused bundle => this desk has no future years at all
    if (base == null || typeof seam.picksFor !== "function" || !seam.clubBundle) return out;
    if (typeof seam.clubHalt === "function" && seam.clubHalt()) return out;

    const pvc = MD.seam.working.pvc || {};
    const draft = {};
    let contradicted = false;
    Object.keys(seam.clubBundle.picksByTeam || {}).forEach(function (team) {
      (seam.picksFor(team) || []).forEach(function (p) {
        if (!p || typeof p.value !== "number") return;
        /* A BAND IS NOT AN ORDINAL. "#11" (low 11, high 11) is the answer to "pick 11"; a wider band
           is the answer to no pick number at all, so it is skipped rather than widened into a guess. */
        if (p.low == null || p.low !== p.high) return;
        const n = Number(p.low), y = Number(p.year);
        /* Law 4 again: everything past 64 is THE POOL, at one index. The ledger carries its round-5
           rows at 0 — a ledger convention, NOT a pick price — and reading them would stand a 0-SCAR
           "Pick 70" on the desk beside a pool item the same curve values at a real figure. */
        if (!(n >= 1 && n <= CURVE_MAX) || !(y > 0)) return;
        const cell = draft[y] = draft[y] || {};
        if (cell[n] != null && cell[n] !== p.value) contradicted = true;   // two prices for one pick
        cell[n] = p.value;
      });
    });
    /* ONE CURRENCY OR NONE. The ledger's BASE-YEAR rows are priced off the very curve this desk prices
       2026 off, so they must agree ordinal-for-ordinal; that is a check the desk can actually make, and
       it is the only evidence available here that the ledger's 2027/2028 figures are in these units.
       If they disagree the ledger was priced off a different curve, so NO future year is offered —
       rather than a 2027 row being set beside a 2026 row it cannot be compared with. */
    const mine = draft[base] || {};
    Object.keys(mine).forEach(function (k) {
      if (pvc[k] == null || pvc[k] !== mine[k]) contradicted = true;
    });
    if (contradicted) return out;
    Object.keys(draft).forEach(function (y) { if (Number(y) !== base) out[y] = draft[y]; });
    return out;
  }

  /* the years this desk can offer, in issue order: the base year (priced straight off the shipped PVC,
     which needs no ledger) followed by every later year the ledger actually prices. */
  function pickYears() {
    const base = baseYear();
    const fut = Object.keys(futureIndex()).map(Number).sort(function (a, b) { return a - b; });
    return [base].concat(fut);
  }

  /* Ordinals only, and only inside the curve's domain — index 65 is the pool and is never read as a
     pick. The base year is priced off the PVC (this desk's founding source); a later year is priced off
     the ledger, which already carries the owner's year rule. null means THIS DESK HAS NO PRICE for that
     pick — it is then never offered and never filled in with a stand-in figure. */
  function pickVal(n, year) {
    if (!(n >= 1 && n <= CURVE_MAX)) return null;
    if (year == null || year === baseYear()) {
      const pvc = MD.seam.working.pvc || {};
      return pvc[String(n)] != null ? pvc[String(n)] : null;
    }
    const cell = futureIndex()[String(year)];
    return cell && cell[n] != null ? cell[n] : null;
  }

  // a basket item written before picks carried a year is a BASE-YEAR pick; that is what it meant then.
  function yearOf(it) { return it && it.year != null ? it.year : baseYear(); }
  function yearChip(it) { const y = yearOf(it); return (y != null ? y + " " : "") + "ND"; }

  function pickItem(n, year) {
    return { t: "pick", n: n, year: year, label: "Pick " + n, val: pickVal(n, year) };
  }
  function poolItem() {
    // the pool level is a BASE-YEAR committed figure and no later year publishes one, so there is
    // exactly one pool item on this desk and it wears the base year.
    return { t: "pick", pool: true, year: baseYear(), label: POOL_LABEL, val: poolVal() };
  }

  function itemVal(it) {
    if (it.t === "pick") {
      if (it.pool) { const pv = poolVal(); return pv != null ? pv : 0; }
      const v = pickVal(it.n, yearOf(it));
      /* The search is the gate: it never offers a pick this desk cannot price, so a null can only reach
         here from a hand-set state. 0 keeps the totals arithmetic (a difference of GIVEN figures) sound
         rather than turning both panes into NaN — it is not a price for anything. */
      return v != null ? v : 0;
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

  /* ITEM 6 (owner word 2026-08-31): "can we please have picks also come up in the search when searched
     for as 'pick xx' not just '5' or '62'". The desk read BARE DIGITS and nothing else, so the words the
     owner actually types returned nothing that was a pick: "pick 62" matched no player and no ordinal
     and came back empty, and "pick" on its own listed Kysaiah Pickett and Latrelle Pickett. The query is
     parsed now rather than pattern-matched — an optional leading "pick"/"picks", an optional ISSUED YEAR
     named in full, and an optional ordinal, in either order — and anything it does not understand falls
     through to the player-name search exactly as before (which is why "pickett" still finds the Picketts:
     the leading word is stripped, "ett" is not digits, and the parse declines the query).

     A YEAR IS ONLY A YEAR IF THIS DESK ACTUALLY OFFERS IT. "2029" is not an issued year, so it stays a
     number — and a number the curve cannot place resolves to the pool under law 4, which is the answer
     "70" has always given and which must not change. Returns null when q is not a pick query at all. */
  function parsePick(q) {
    let rest = q, named = false;
    const m = /^picks?\s*/.exec(rest);
    if (m) { named = true; rest = rest.slice(m[0].length).trim(); }
    const years = pickYears();
    const toks = rest ? rest.split(/\s+/) : [];
    let year = null, digits = null;
    for (let i = 0; i < toks.length; i++) {
      const t = toks[i];
      if (!/^\d+$/.test(t)) return null;                       // a word: this is a name search
      if (t.length === 4 && years.indexOf(Number(t)) !== -1) {
        if (year != null) return null;                         // two years is not a query anyone means
        year = Number(t);
      } else {
        if (digits != null) return null;                       // two ordinals likewise
        digits = t;                       // kept as DIGITS, not a number: the ordinal scan is a PREFIX
      }
    }
    if (!named && year == null && digits == null) return null;
    return { named: named, year: year, digits: digits };
  }

  /* ITEM 5 (owner word 2026-08-31): "the drop down menu … currently it's only 2 items come up in the
     search, can it be at least 5 (unless there are less matching results)". Reproduced exactly: "62"
     returned Pick 62 and the pool, and nothing else existed to return. Two separate reasons the list ran
     short, both addressed here:
       · a fully-specified number could only ever match ONE ordinal, so "62" was Pick 62 + the pool and
         there was no third thing to show. With item 7 every issued year is searchable, so it is now one
         row per year plus the pool;
       · the scan capped ROWS at six, which is also the count of ordinals it wanted to show — so the
         moment a second year existed the years and the ordinals would have fought over the same six
         rows. The cap is on ORDINALS now, with a row cap above it, so every offered year of every
         matched ordinal has room.
     THE ORDINAL BREADTH IS DELIBERATELY UNCHANGED at six: typing "5" still shows picks 5 and 50–54 and
     still stops before 55–59. That is a real limit and it is stated here rather than papered over — the
     owner asked for a longer list, not for every prefix match, and pick 55 is one more keystroke away.
     MIN_ROWS is his floor, and the caps below are set to clear it — but it is a floor on what is SHOWN,
     never a pad: nothing is invented to reach it, so a query with four true matches shows four, and a
     query with one shows one. The dropdown scrolls (styles/matchday.css .combo .results carries
     max-height + overflow:auto), so the row caps are a sanity ceiling, not a viewport fit. */
  const MIN_ROWS = 5;
  const PICK_ORDINALS = 6;      // the pre-existing breadth of the ordinal scan, now not shared with years
  const PICK_ROWS = 18;         // six ordinals × the three issued years
  const PLAYER_ROWS = 8;
  const MAX_ROWS = 26;

  /* match a query to picks (ordinals 1–64 individually per issued year, plus the ONE pool item) and
     players (type-ahead by name). */
  function matchItems(q) {
    q = String(q || "").trim().toLowerCase();
    const players = MD.seam.working.players || [];
    const out = [];
    if (!q) {
      players.slice().sort(function (a, b) { return b.v - a.v; }).slice(0, PLAYER_ROWS)
        .forEach(function (pl) { out.push({ t: "player", key: pl.key, label: pl.name, val: pl.v }); });
      return out;
    }
    const pq = parsePick(q);
    if (pq) {
      const years = pq.year != null ? [pq.year] : pickYears();
      const ords = [];
      if (pq.digits == null) {
        // "pick", or a bare year: there is no ordinal to match, so the list starts at the top of the curve
        for (let n = 1; n <= CURVE_MAX && ords.length < PICK_ORDINALS; n++) ords.push(n);
      } else {
        // EXACT FIRST, then the prefix matches ascending — typing "5" means pick 5 before pick 50.
        const exact = Number(pq.digits);
        if (exact >= 1 && exact <= CURVE_MAX) ords.push(exact);
        for (let n = 1; n <= CURVE_MAX && ords.length < PICK_ORDINALS; n++) {
          if (n !== exact && String(n).indexOf(pq.digits) === 0) ords.push(n);
        }
      }
      for (let i = 0; i < ords.length && out.length < PICK_ROWS; i++) {
        for (let j = 0; j < years.length && out.length < PICK_ROWS; j++) {
          // offered ONLY where this desk holds a price for it — never a row carrying an invented figure
          if (pickVal(ords[i], years[j]) == null) continue;
          out.push(pickItem(ords[i], years[j]));
        }
      }
      /* typing "70" answers with the pool, not a phantom ordinal — that is what a pick past 64 is. The
         pool level is a base-year committed figure, so a query pinned to a later year is not given one. */
      if (poolVal() != null && (pq.year == null || pq.year === baseYear())) out.push(poolItem());
    } else {
      /* the pool by NAME. "pick" is a keyword now, so the leading word is stripped here too — otherwise
         "pick pool", which is exactly what a pool pick is called, would be the one phrasing that fails. */
      const t = q.replace(/^picks?\s*/, "");
      if (t && "pool pick".indexOf(t) === 0 && poolVal() != null) out.push(poolItem());
    }
    players.filter(function (pl) { return String(pl.name).toLowerCase().indexOf(q) !== -1; })
      .slice(0, PLAYER_ROWS)
      .forEach(function (pl) { out.push({ t: "player", key: pl.key, label: pl.name, val: pl.v }); });
    return out.slice(0, MAX_ROWS);
  }

  function combo(side, basket, container) {
    const wrap = fmt.el("div", "combo");
    const input = document.createElement("input");
    input.className = "tradesearch";
    input.type = "text";
    /* the hint NAMES the years the desk can actually offer (pickYears), so it cannot promise a 2027
       search on a bundle that prices none — and it says the "pick 24" form out loud, because the owner
       had no way to know the box only read bare digits. */
    const yrs = pickYears().filter(function (y) { return y != null; });
    const yrHint = yrs.length > 1 ? ", a draft year (" + yrs.join(" / ") + ")" : "";
    input.setAttribute("placeholder",
      "add — search a player, a pick 1–64 (“24” or “pick 24”)" + yrHint + ", or “pool”…");
    const results = fmt.el("div", "results");
    results.style.display = "none";

    function paint() {
      const items = matchItems(input.value);
      results.innerHTML = "";
      if (!items.length) {
        const none = fmt.el("div", "rnone",
          "no match — try a name, a pick 1–64 (“24” or “pick 24”)" + yrHint + ", or “pool”");
        results.appendChild(none);
      }
      items.forEach(function (it) {
        const b = fmt.el("button");
        const nm = it.t === "pick"
          ? '<span class="rpick">' + fmt.esc(it.label) + " <small>" + fmt.esc(yearChip(it)) + "</small></span>"
          : '<span>' + fmt.esc(it.label) + "</span>";
        b.innerHTML = nm + '<span class="rv num">' + fmt.n(it.val) + "</span>";
        b.addEventListener("mousedown", function (e) {
          e.preventDefault(); // fire before the input blur so the pick registers
          // the YEAR travels with the basket item: a 2027 pick that forgot its year would be re-priced
          // as a base-year pick, which is a different asset at a different figure.
          if (it.t === "pick") basket.push(it.pool ? { t: "pick", pool: true, year: it.year }
                                                   : { t: "pick", n: it.n, year: it.year });
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
        meta = '<i>' + fmt.esc(yearChip(it)) + (it.pool ? " · position-blind level" : "") + "</i>";
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
    // every ORDINAL pick 1–64 of every ISSUED YEAR is individually selectable, by its number or by name
    // ("pick 24"), with the single pool item covering everything past 64; the results dropdown is styled
    // in the board's condensed type (requirement 3: dropdown font matched to the board type style).
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
     computing no price. matchItems/parsePick/pickYears join it on the same terms — the search is the
     one thing between the owner's typing and what the desk offers, it reads no DOM, and MIN_ROWS is
     exported so the suite asserts the SHIPPED floor rather than a number retyped in a test. */
  return { render: render, describePick: describePick, matchItems: matchItems,
           parsePick: parsePick, pickYears: pickYears, MIN_ROWS: MIN_ROWS };
})();
