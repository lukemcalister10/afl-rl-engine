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

  /* ONE LIST OF ROUND WORDS, read by the translator's prose (describePick) AND by the search's parse
     of "first"/"1st"/"r1". They were about to be two lists saying the same thing. */
  const ROUND_WORDS = ["first", "second", "third", "fourth", "fifth", "sixth"];
  function roundOrd(n) {
    const t = n % 100, u = n % 10;
    const suf = (t >= 11 && t <= 13) ? "th" : u === 1 ? "st" : u === 2 ? "nd" : u === 3 ? "rd" : "th";
    return n + suf;
  }

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
     — AND THE OWNER'S CORRECTION OF IT, the same day, which is the law this file now follows:

       "2027 pick 62 isn't pick 62. It's a fourth round pick. 2027 and 2028 picks don't have numbers.
        They exist as concepts — Hawthorn's future 1st round pick — we don't know what pick that will
        be yet. So they shouldn't be recorded as future picks. … You should be able to search for
        future picks, but they don't have numbers. So you'd search for Hawthorn 2027 4th — or 4th
        round 27 Hawthorn etc."

     THE FIRST CUT OF THIS SEARCH READ THE LEDGER'S BAND AS AN ORDINAL and offered "Pick 62 · 2027 ND".
     There is no such asset. A LATER YEAR'S PICK HAS NO NUMBER: its whole identity is (origin club,
     year, round), and a number printed beside it states as fact a thing nobody knows yet. So this desk
     names a future pick by its club, its year and its round, and offers no ordinal for a later year at
     all — not in the dropdown, not on a chip, not behind a query.

     THE BAND IS A PRICING INPUT AND STAYS ONE. The owner's year rule — 2026 = own projected band at
     full price; 2027 = (1/3 own + 2/3 round average) × 0.9; 2028 = round average × 0.8, both
     multipliers read off his Ladder sheet (2026-08-30) — is enforced in exactly ONE place,
     ui/tools/ingest_inputs.py price_pick(), and its answer already ships as `value` on every row of
     ui/data/club_valuation.js. This desk READS that value and re-derives nothing. It could not honestly
     re-derive it anyway: "own projected band" comes off the workbook's Ladder projection, which is in
     no bundle this page loads, so a desk that computed its own 2027 price would be inventing one.

     WHY THE RULE HAS THAT SHAPE, in the owner's words: "2028 picks are all worth the same for each
     round — it's too far away to use 2026 finishing positions to value them. 2027 is close enough you
     can infer some value from how the teams went this year, but not the full value of the pick."
     Measured on the shipped ledger that is exactly what it does: all sixteen 2028 first-rounders carry
     ONE figure, all sixteen second-rounders another, and so on. Which is why two clubs' 2028 firsts are
     the same price and are still TWO DIFFERENT ASSETS held by two different clubs — they are never
     folded into one row here, because a price is not an identity.

     A BASE-YEAR PICK IS THE OPPOSITE CASE AND IS LEFT ALONE. Finishing positions have made it real, so
     it HAS a number; it is named "Pick 24" and priced off the shipped PVC exactly as before.

     THE LEDGER IS REACHED THROUGH THE SEAM, not off the raw bundle, so this surface inherits the one
     choke point seam.js established (clubHalt / picksFor): a picks bundle that is not this tree's
     yields nothing here for the same reason it yields nothing to the clubs page and the board overlay.
     A stale pick price is a wrong number wearing the look of a right one, and there is no fallback the
     browser could compute in its place — so the desk offers no future pick at all rather than a price. */
  let _ledger = null;
  function ledger() {
    if (_ledger) return _ledger;
    // years: the LATER years only (the base year needs no ledger). rounds/clubs: the vocabulary the
    // search may parse. assets: every pick asset the ledger prices, in dropdown order. byKey: the
    // one-lookup a basket item re-prices through.
    const out = { years: [], rounds: [], clubs: [], assets: [], byKey: {} };
    _ledger = out;
    const seam = MD.seam;
    const base = baseYear();
    // no base year, no picks reader, or a halted/refused bundle => this desk has no ledger at all
    if (base == null || typeof seam.picksFor !== "function" || !seam.clubBundle) return out;
    if (typeof seam.clubHalt === "function" && seam.clubHalt()) return out;

    const pvc = MD.seam.working.pvc || {};
    const rows = [], seen = {}, mine = {};
    let contradicted = false;
    Object.keys(seam.clubBundle.picksByTeam || {}).forEach(function (team) {
      (seam.picksFor(team) || []).forEach(function (p) {
        if (!p) return;
        const y = Number(p.year), r = Number(p.round);
        /* NO ORIGIN, NO YEAR OR NO ROUND IS NO IDENTITY. "Hawthorn's 2027 first" is the whole name of
           the asset; a row missing any part of it cannot be named, so it is not offered. */
        if (!p.origin || !(y > 0) || !(r > 0)) return;
        /* THE ROUND-5 ROWS, DECLINED IN EVERY YEAR. The ledger carries them at 0 — a LEDGER
           CONVENTION recording that the round exists, not a price for anything — and the gate is
           stated as what it means rather than as the round number: THIS DESK OFFERS NO ASSET IT HAS
           NO PRICE FOR. Reading them would stand a 0-SCAR "Hawthorn 2027 5th" on the desk beside a
           pool item the same curve values at a real figure. */
        if (typeof p.value !== "number" || !(p.value > 0)) return;
        const k = p.origin + "|" + y + "|" + r;
        if (seen[k] != null && seen[k] !== p.value) contradicted = true;   // two prices for one asset
        seen[k] = p.value;
        /* THE BASE YEAR'S ROWS DO CARRY A NUMBER, and it is the only year whose rows do. "#11" (low 11,
           high 11) is the answer to "pick 11"; a wider band answers no pick number at all, so it is
           left as no number rather than widened into a guess. Past 64 there is no ordinal under law 4. */
        let n = null;
        if (y === base && p.low != null && p.low === p.high) {
          const c = Number(p.low);
          if (c >= 1 && c <= CURVE_MAX) { n = c; mine[c] = p.value; }
        }
        const display = p.originDisplay || p.origin;
        rows.push({ origin: p.origin, display: display, year: y, round: r, n: n, value: p.value,
                    lc: String(p.origin).toLowerCase(), dlc: String(display).toLowerCase() });
      });
    });
    /* ONE CURRENCY OR NONE. The ledger's BASE-YEAR rows are priced off the very curve this desk prices
       2026 off, so they must agree ordinal-for-ordinal; that is a check the desk can actually make, and
       it is the only evidence available here that the ledger's 2027/2028 figures are in these units.
       If they disagree the ledger was priced off a different curve, so NOTHING off it is offered —
       rather than a 2027 row being set beside a 2026 row it cannot be compared with. */
    Object.keys(mine).forEach(function (k) {
      if (pvc[k] == null || pvc[k] !== mine[k]) contradicted = true;
    });
    if (contradicted) return out;

    // dropdown order: year, then round, then the dearest first, then alphabetical so it is stable.
    rows.sort(function (a, b) {
      return (a.year - b.year) || (a.round - b.round) || (b.value - a.value) ||
             (a.display < b.display ? -1 : a.display > b.display ? 1 : 0);
    });
    const yrs = {}, rds = {}, cl = {};
    rows.forEach(function (a) {
      out.byKey[a.origin + "|" + a.year + "|" + a.round] = a;
      if (a.year !== base) yrs[a.year] = 1;
      rds[a.round] = 1;
      if (!cl[a.origin]) cl[a.origin] = { origin: a.origin, display: a.display, lc: a.lc, dlc: a.dlc };
    });
    out.assets = rows;
    out.years = Object.keys(yrs).map(Number).sort(function (a, b) { return a - b; });
    out.rounds = Object.keys(rds).map(Number).sort(function (a, b) { return a - b; });
    out.clubs = Object.keys(cl).map(function (k) { return cl[k]; });
    return out;
  }

  /* the years this desk can offer, in issue order: the base year (priced straight off the shipped PVC,
     which needs no ledger) followed by every later year the ledger actually prices. */
  function pickYears() {
    return [baseYear()].concat(ledger().years);
  }
  // the rounds the ledger prices — the only rounds a query may name, and the only ones offered.
  function pickRounds() { return ledger().rounds.slice(); }

  // does a club query (already lowercased) name this club? SUBSTRING, exactly as the player search
  // matches a name, so "hawthorn", "hawks" and "north melbourne" all land.
  function clubHit(a, qs) { return a.lc.indexOf(qs) !== -1 || a.dlc.indexOf(qs) !== -1; }

  /* AN ORDINAL IS A BASE-YEAR FACT. Only inside the curve's domain — index 65 is the pool and is never
     read as a pick — and only for the base year: a later year has no pick numbers at all, so there is
     nothing here to price and null is the honest answer rather than a figure off a projected band.
     null means THIS DESK HAS NO PRICE, and a pick with no price is never offered. */
  function pickVal(n, year) {
    if (!(n >= 1 && n <= CURVE_MAX)) return null;
    if (year != null && year !== baseYear()) return null;
    const pvc = MD.seam.working.pvc || {};
    return pvc[String(n)] != null ? pvc[String(n)] : null;
  }

  // a basket item written before picks carried a year is a BASE-YEAR pick; that is what it meant then.
  function yearOf(it) { return it && it.year != null ? it.year : baseYear(); }

  /* ONE PRICE PATH FOR EVERY PICK ASSET, so the dropdown row and the basket chip cannot drift onto two
     different figures for the same thing. null = no price, which is the search's gate and the totals'
     fail-closed case both. */
  function priceOf(it) {
    if (!it) return null;
    if (it.pool) return poolVal();
    if (it.club != null) {
      const a = ledger().byKey[it.club + "|" + yearOf(it) + "|" + it.round];
      return a ? a.value : null;
    }
    return pickVal(it.n, yearOf(it));
  }

  /* ONE NAME PER PICK ASSET, read by the dropdown row AND by the basket chip. They used to be two
     spellings of the same thing (the row read `it.label`, the chip rebuilt "Pick " + n), which is
     precisely how a future pick would have kept an ordinal on one surface after losing it on the other. */
  function pickName(it) {
    if (!it) return "";
    if (it.pool) return "Pool pick";
    /* A LATER YEAR'S ORDINAL IS NOT AN ASSET, SO IT DOES NOT GET A NAME. The search cannot produce one
       and no basket is persisted, so this only reaches here from a hand-set state (or one written under
       the retired future-ordinal model) — and the single thing this display must never do again is
       print "Pick 62 · 2027 ND". It prices at nothing through priceOf for exactly the same reason. */
    if (it.club == null && it.n != null && yearOf(it) !== baseYear()) return "—";
    if (it.club != null) {
      // the CLUB'S OWN display spelling comes off the ledger row (originDisplay) — the same shortening
      // the rest of the UI applies — rather than this view inventing a second spelling rule.
      const a = ledger().byKey[it.club + "|" + yearOf(it) + "|" + it.round];
      return (a ? a.display : it.club) + " " + yearOf(it) + " " + roundOrd(it.round);
    }
    return "Pick " + it.n;
  }
  function yearChip(it) {
    // A FUTURE PICK ALREADY NAMES ITS YEAR ("Hawthorn Hawks 2027 1st"), so the meta line has only the
    // draft tag left to say; repeating the year there would read as two separate facts about one asset.
    if (it && it.club != null) return "ND";
    const y = yearOf(it);
    return (y != null ? y + " " : "") + "ND";
  }

  function pickItem(n, year) {
    const it = { t: "pick", n: n, year: year };
    it.label = pickName(it); it.val = priceOf(it);
    return it;
  }
  function futureItem(a) {
    const it = { t: "pick", club: a.origin, year: a.year, round: a.round };
    it.label = pickName(it); it.val = priceOf(it);
    return it;
  }
  // the ledger's base-year rows ARE ordinal picks — same asset, and that year's has a number — so they
  // are offered under the number, priced off the PVC like every other base-year pick on this desk.
  function assetItem(a) { return a.n != null ? pickItem(a.n, a.year) : futureItem(a); }
  function poolItem() {
    // the pool level is a BASE-YEAR committed figure and no later year publishes one, so there is
    // exactly one pool item on this desk and it wears the base year.
    return { t: "pick", pool: true, year: baseYear(), label: POOL_LABEL, val: poolVal() };
  }

  function itemVal(it) {
    if (it.t === "pick") {
      const v = priceOf(it);
      /* The search is the gate: it never offers a pick this desk cannot price, so a null can only reach
         here from a hand-set state (or from a basket item written under the retired future-ordinal
         model). 0 keeps the totals arithmetic (a difference of GIVEN figures) sound rather than turning
         both panes into NaN — it is not a price for anything. */
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
  /* ROUND_SIZE IS THE NATIONAL DRAFT'S ROUND (18 clubs), which is what the PVC is a curve over. It is
     NOT the AFFL's round — the ledger's own `round` field is that, and it is read, never recomputed. */
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
    const round = Math.ceil(best / ROUND_SIZE);
    const within = ((best - 1) % ROUND_SIZE) + 1;
    const pos = within <= 6 ? "early" : within <= 12 ? "mid" : "late";
    const ord = ROUND_WORDS[round - 1] || roundOrd(round);
    if (best <= 3) return "a top-" + best + " pick";
    return "a " + pos + " " + ord + "-round pick (≈ pick " + best + ")";
  }

  /* ITEM 6 (owner word 2026-08-31): "can we please have picks also come up in the search when searched
     for as 'pick xx' not just '5' or '62'". The desk read BARE DIGITS and nothing else, so the words the
     owner actually types returned nothing that was a pick: "pick 62" matched no player and no ordinal
     and came back empty, and "pick" on its own listed Kysaiah Pickett and Latrelle Pickett.

     THE QUERY IS PARSED, NOT PATTERN-MATCHED, and it now has to carry two different asset languages:

       · A BASE-YEAR PICK IS A NUMBER.  "24", "pick 24", "24 2026".
       · A LATER YEAR'S PICK IS A CLUB, A YEAR AND A ROUND, in any order and in any subset —
         "Hawthorn 2027 4th", "4th round 27 Hawthorn", "hawthorn 2027", "2027 1st". No ordinal is
         accepted or offered for a later year, because there is no such thing.

     THE ONE GENUINE AMBIGUITY IS "27": it is both the owner's shorthand for 2027 and the ordinal pick
     27, which this desk has answered since it opened. It is resolved by CONTEXT, never by preference:
     two digits are the year ONLY when the query also names a club, a round or… nothing else it could
     be. Bare "27" keeps its established meaning — pick 27 — because breaking a working query to make a
     new one work is not a fix. A four-digit year is unambiguous and is read as one when the desk
     actually offers it; "2029" is not an issued year, so it stays a number, and a number the curve
     cannot place resolves to the pool under law 4 — which is the answer "70" has always given.

     A WORD IS ONLY A CLUB IF THE LEDGER HOLDS ONE BY THAT NAME. Anything else falls through to the
     player-name search exactly as before — which is why "pickett" still finds the Picketts: the leading
     keyword is stripped, "ett" names no club, and the parse declines the query rather than guessing.
     Returns null when q is not a pick query at all. */
  function parsePick(q) {
    let rest = String(q == null ? "" : q).trim().toLowerCase(), named = false;
    const m = /^picks?\s*/.exec(rest);
    if (m) { named = true; rest = rest.slice(m[0].length).trim(); }
    const L = ledger(), base = baseYear(), years = pickYears();
    const toks = rest ? rest.split(/\s+/) : [];
    let year = null, digits = null, round = null, dual = null, wantRound = false;
    const clubToks = [];
    for (let i = 0; i < toks.length; i++) {
      // the owner writes "Hawthorn's future 1st" as readily as "hawthorn 1st"; neither the possessive
      // nor the word "future" adds anything the (club, year, round) triple does not already say.
      const t = toks[i].replace(/['’]s$/, "");
      if (!t || t === "future" || t === "futures") continue;
      if (t === "round" || t === "rounds" || t === "rd") { wantRound = true; continue; }
      /* A ROUND TOKEN IS ONLY A ROUND IF THE LEDGER PRICES THAT ROUND. "5th" names the round the ledger
         carries at 0 — a convention, not an asset — so it is not round vocabulary here and falls through
         to the club test, which declines it. One gate for "r4", "4th" and "fourth" alike. */
      let rnd = null;
      const rm = /^r(\d{1,2})$/.exec(t), om = /^(\d{1,2})(?:st|nd|rd|th)$/.exec(t),
            wi = ROUND_WORDS.indexOf(t);
      if (rm) rnd = Number(rm[1]);
      else if (om) rnd = Number(om[1]);
      else if (wi !== -1) rnd = wi + 1;
      if (rnd != null && L.rounds.indexOf(rnd) !== -1) {
        if (round != null) return null;
        round = rnd; wantRound = false; continue;
      }
      if (/^\d+$/.test(t)) {
        const nn = Number(t);
        // "round 1" — the armed keyword takes the next number only while no round is named and that
        // number could be one, so "4th round 27" leaves 27 alone to be the year it plainly is.
        if (wantRound && round == null && L.rounds.indexOf(nn) !== -1) { round = nn; wantRound = false; continue; }
        wantRound = false;
        if (t.length === 4 && years.indexOf(nn) !== -1) {
          if (year != null) return null;                       // two years is not a query anyone means
          year = nn; continue;
        }
        if (t.length === 2 && base != null && years.indexOf(2000 + nn) !== -1 && 2000 + nn !== base) {
          if (dual != null) return null;
          dual = nn; continue;                                 // year-or-ordinal; resolved below
        }
        if (digits != null) return null;                       // two ordinals likewise
        digits = t;                        // kept as DIGITS, not a number: the ordinal scan is a PREFIX
        continue;
      }
      wantRound = false;
      clubToks.push(t);
    }
    let club = clubToks.length ? clubToks.join(" ") : null;
    // a word that names no club in the ledger is a NAME, not a failed pick query — decline and let the
    // player search have it whole.
    if (club != null && !L.clubs.some(function (c) { return clubHit(c, club); })) return null;

    if (dual != null) {
      if (year != null) return null;                           // "27 2027" is not a query anyone means
      else if (club != null || round != null) year = 2000 + dual;   // the context makes it the year
      else if (digits != null) return null;                    // "27 62" is two ordinals
      else digits = String(dual);                              // bare "27" keeps meaning pick 27
    }
    // (club, year, round) is the language of a LATER year's pick; a number is the language of the base
    // year's. A query that mixes them describes no asset, so it is declined rather than half-answered.
    const future = club != null || round != null || (year != null && year !== base);
    if (future && digits != null) return null;
    if (!named && !future && year == null && digits == null) return null;
    return { named: named, future: future, year: year, round: round, club: club, digits: digits };
  }

  /* ITEM 5 (owner word 2026-08-31): "the drop down menu … currently it's only 2 items come up in the
     search, can it be at least 5 (unless there are less matching results)". Reproduced exactly: "62"
     returned Pick 62 and the pool, and nothing else existed to return. The scan also capped ROWS at six,
     which is also the count of ordinals it wanted to show, so years and ordinals fought over the same
     six rows. The cap is on ORDINALS now, with a row cap above it.
     THE ORDINAL BREADTH IS DELIBERATELY UNCHANGED at six: typing "5" still shows picks 5 and 50–54 and
     still stops before 55–59. That is a real limit and it is stated here rather than papered over — the
     owner asked for a longer list, not for every prefix match, and pick 55 is one more keystroke away.
     MIN_ROWS is his floor, and the caps below clear it — but it is a floor on what is SHOWN, never a
     pad: nothing is invented to reach it, so a query with four true matches shows four, and a query with
     one shows one. PICK_ROWS has to clear the widest honest club query, which is every year × every
     round the ledger prices for that club (12 on the shipped ledger); a broader query — a bare round,
     say — genuinely matches more assets than a dropdown should list, so it is trimmed, dearest first.
     The dropdown scrolls (styles/matchday.css .combo .results carries max-height + overflow:auto), so
     the row caps are a sanity ceiling, not a viewport fit. */
  const MIN_ROWS = 5;
  const PICK_ORDINALS = 6;      // the pre-existing breadth of the ordinal scan
  const PICK_ROWS = 18;
  const PLAYER_ROWS = 8;
  const MAX_ROWS = 26;

  /* match a query to picks (base-year ordinals 1–64 individually, every later year's club/round asset
     the ledger prices, plus the ONE pool item) and players (type-ahead by name). */
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
    if (pq && pq.future) {
      /* THE CLUB/YEAR/ROUND QUERY. Each named part narrows; an unnamed part matches everything, so
         "hawthorn" lists Hawthorn's whole holding and "2027 1st" lists every club's 2027 first.
         TWO CLUBS' 2028 FIRSTS PRICE THE SAME AND ARE STILL TWO ROWS — they are different assets held
         by different clubs, and folding equal prices into one row would lose the club, which is the
         only thing a future pick actually is.
         A club query also reaches the BASE year, whose rows the ledger holds too; that year's pick has
         a number, so it is offered under its number rather than as a club/round concept. */
      ledger().assets.forEach(function (a) {
        if (out.length >= PICK_ROWS) return;
        if (a.n != null && pq.club == null) return;   // base-year rows answer a club query, not a bare round
        if (pq.year != null && a.year !== pq.year) return;
        if (pq.round != null && a.round !== pq.round) return;
        if (pq.club != null && !clubHit(a, pq.club)) return;
        out.push(assetItem(a));
      });
    } else if (pq) {
      /* THE ORDINAL QUERY — the base year's language, and only the base year's. */
      const ords = [];
      if (pq.digits == null) {
        // "pick", or a bare base year: there is no ordinal to match, so the list starts at the top
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
        // offered ONLY where this desk holds a price for it — never a row carrying an invented figure
        if (pickVal(ords[i], baseYear()) == null) continue;
        out.push(pickItem(ords[i], baseYear()));
      }
      /* typing "70" answers with the pool, not a phantom ordinal — that is what a pick past 64 is. The
         pool level is a base-year committed figure, so a query pinned to a later year is not given one
         (and a later year cannot reach here anyway: it parses as a club/round query). */
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

  /* THE HINT IS READ OFF THE DESK, never typed alongside it. It names the base year the board stamped
     and, as the worked example of the future form, a REAL asset off the ledger — so it can neither
     promise a 2027 search on a bundle that prices none nor show a shape the ledger has no row for.
     One string, used by the placeholder and by the no-match line, which were drifting apart. */
  function searchHint() {
    const base = baseYear();
    let s = "a player, a " + (base != null ? base + " " : "") + "pick by number (“24” or “pick 24”)";
    const ex = ledger().assets.filter(function (a) { return a.n == null; })[0];
    if (ex) s += ", a future pick by club + year + round (“" + pickName(futureItem(ex)) + "”)";
    return s + ", or “pool”";
  }

  function combo(side, basket, container) {
    const wrap = fmt.el("div", "combo");
    const input = document.createElement("input");
    input.className = "tradesearch";
    input.type = "text";
    const hint = searchHint();
    input.setAttribute("placeholder", "add — search " + hint + "…");
    const results = fmt.el("div", "results");
    results.style.display = "none";

    function paint() {
      const items = matchItems(input.value);
      results.innerHTML = "";
      if (!items.length) results.appendChild(fmt.el("div", "rnone", "no match — try " + hint));
      items.forEach(function (it) {
        const b = fmt.el("button");
        const nm = it.t === "pick"
          ? '<span class="rpick">' + fmt.esc(it.label) + " <small>" + fmt.esc(yearChip(it)) + "</small></span>"
          : '<span>' + fmt.esc(it.label) + "</span>";
        b.innerHTML = nm + '<span class="rv num">' + fmt.n(it.val) + "</span>";
        b.addEventListener("mousedown", function (e) {
          e.preventDefault(); // fire before the input blur so the pick registers
          /* THE WHOLE IDENTITY TRAVELS WITH THE BASKET ITEM. A base-year pick is its number and its
             year; a later year's pick is its club, its year and its round, and one of those dropped
             would leave a different asset at a different price behind. */
          if (it.t === "pick") {
            basket.push(it.pool ? { t: "pick", pool: true, year: it.year }
              : it.club != null ? { t: "pick", club: it.club, year: it.year, round: it.round }
              : { t: "pick", n: it.n, year: it.year });
          } else basket.push({ t: "player", key: it.key });
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
        // the SAME namer the dropdown row used, so what he clicked is what the chip reads
        nm = '<span class="pickchip">' + fmt.esc(pickName(it)) + "</span>";
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
    // item 6: a custom type-ahead combobox (replaces the bare <select>) — players are searchable, every
    // ORDINAL pick 1–64 of the base year is individually selectable by its number or by name
    // ("pick 24"), every later year's pick is selectable by club + year + round ("Hawthorn 2027 1st"),
    // and the single pool item covers everything past 64; the results dropdown is styled in the board's
    // condensed type (requirement 3: dropdown font matched to the board type style).
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
     computing no price. matchItems/parsePick/pickYears/pickRounds/pickName join it on the same terms —
     the search is the one thing between the owner's typing and what the desk offers, the namer is the
     one thing between what he clicked and what the chip reads, neither touches the DOM, and MIN_ROWS is
     exported so the suite asserts the SHIPPED floor rather than a number retyped in a test. */
  return { render: render, describePick: describePick, matchItems: matchItems,
           parsePick: parsePick, pickYears: pickYears, pickRounds: pickRounds,
           pickName: pickName, MIN_ROWS: MIN_ROWS };
})();
