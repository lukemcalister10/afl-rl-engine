/* Matchday UI — PICK VALUE view (owner-commissioned).

   WHAT HE ASKED FOR, IN HIS WORDS
   -------------------------------
     "Can we create a Pick Value tab, that has a table of pick / pathway values based on what we know.
      And then also the ability to select a position, and have the table show the v0 for that position
      (and its + or - against the all in pick value)"

   So: ONE table down the pick ordinals. Column A is the ALL-IN, position-BLIND pick value — the
   adopted pick-value curve the board ships (`pvc`). Column B is what the entry surface actually paid
   for THAT POSITION at THAT PICK. Column C is the gap between them, signed. Nothing else.

   PURE VIEW. It computes no price. Both columns are READ off shipped artifacts; the only arithmetic
   is a subtraction of two given figures, which is a difference and not a re-valuation.

   ------------------------------------------------------------------------------------------------
   THE TWO SOURCES, AND WHY THE DELTA IS A COMPARISON AND NOT A DECOMPOSITION
   ------------------------------------------------------------------------------------------------
   ALL-IN  = `MD.seam.working.pvc` — the composed pathway curve adopted for the loaded release
             (ui/tools/ingest_inputs.py resolves and asserts it; pick 1 is the numeraire anchor).
             Position-blind by construction: one number per ordinal, for everybody.

   POSITION = the v0 ENTRY PRICE of every board player whose entry was a numbered pick, read through
             MD.v0 (ui/app/v0.js) — NOT off `window.__V0__` directly. That matters: MD.v0 already
             enforces the mirror law (the sidecar names the board + store it was generated from and is
             REFUSED when either disagrees with the loaded board). Reading the raw global here would
             have opened a SECOND, unpinned path to the same numbers, which is exactly the failure
             #232 hit. One reader, one pin, inherited.

   THESE ARE TWO DIFFERENT ARTIFACTS AND THE PAGE SAYS SO. v0 is the FROZEN YEAR-ZERO entry surface;
   `pvc` is the CURRENTLY ADOPTED curve. docs/ENGINE_PRIMER.md is explicit that position/age
   "redistribute around the anchor and never inflate it" — but the anchor there is year-zero's own
   position-blind level, which no bundle this page loads publishes. So the delta below is an honest
   comparison ACROSS the two artifacts and it is NOT a decomposition of the all-in curve: the
   position columns do not, and are not claimed to, average back to it. Measured on the shipped
   bundles the positional surface sits systematically off the adopted curve (MID and RUCK above it at
   almost every ordinal, the other four below), which is a real reading and not an artefact — but a
   reader who thinks he is looking at a partition of one number would misread it, so the page states
   the provenance of each column in words rather than leaving it to be inferred.

   ------------------------------------------------------------------------------------------------
   THE SLOT KEY — VERIFIED, NOT ASSUMED
   ------------------------------------------------------------------------------------------------
   The sidecar's `slot` is "POSITION|AGE|PICK", pipe-delimited, three fields. Cross-checked row by row
   against engine/rl_after/rl_model_data.json for all 561 pick-slot rows on the shipped bundle:
     · POSITION is `future_position` — 561/561. (It is NOT `drafted_position`, which disagrees on
       116 rows, and it is not the multi-code eligibility list in ui/app/positions_data.js: it is the
       ONE position the entry surface is indexed by. The page says "entry position" for that reason.)
     · PICK is `stream_pick` — 561/561 (equal to `pick` on every one of those rows).
     · AGE is the DRAFT-AGE BUCKET, not calendar arithmetic: it equals draft year minus birth year on
       554/561, and the 7 exceptions are all January-to-April birthdays bucketed up to 18. So it is
       read here as an opaque integer label and never recomputed.
   parseSlot() below re-checks that shape on every row at render time rather than trusting it. A row
   whose slot does not parse is COUNTED AND DROPPED, never guessed at.

   ------------------------------------------------------------------------------------------------
   WHAT THIS PAGE REFUSES TO DO
   ------------------------------------------------------------------------------------------------
   · IT NEVER INTERPOLATES. The position/pick grid is sparse — the board holds 804 players, only 561
     of them entered on a numbered pick, and those 561 careers do not cover every (position, pick)
     pair. An empty cell renders an em-dash and is counted in the coverage line. Curve-fitting a
     missing cell would put a number on screen that no career stands behind, which is the one thing
     the register's standing posture forbids.
   · IT NEVER RENDERS ORDINAL 65. The shipped `pvc` carries 65 keys: 1-64 are the curve, index 65 is
     THE POOL — everything past 64 at one position-blind level, "with order of selection carrying no
     value" (RULEBOOK v2.1 law 4, mirrored in ui/app/trade.js:21 and enforced ingest-side in
     ui/tools/ingest_inputs.py price_pick). 65 is not a pick, so it is shown beneath the table as the
     pool level it is, and never as a row in the ordinal column.
   · IT NEVER HIDES THE SAMPLE. Every populated cell carries the number of careers behind it, and a
     cell resting on THIN_MAX or fewer wears a dot marker as well — the owner's older tool used a dot
     for a thin sample and that instinct was right: the eye needs the warning before it reads the
     figure, not after.

   ------------------------------------------------------------------------------------------------
   AGGREGATION — DECLARED, BOUNDED, AND OFF BY DEFAULT
   ------------------------------------------------------------------------------------------------
   The entry surface is indexed by the TRIPLE (position, age, pick), not the pair. Verified on the
   shipped sidecar: 303 distinct triples, and every one of them carries exactly ONE v0 — zero
   violations. So a cell viewed at a FIXED draft age is the surface's own number, exact, with no
   aggregation of any kind. That is why the age control defaults to a single age (the modal one,
   DERIVED from the loaded data below and never typed in here) rather than pooling.

   "All draft ages" is offered because it fills more cells, and it is the only mode in which this page
   aggregates anything. When it does, it says so in three places: a standing line on the page, a
   marker on every cell that actually spans more than one distinct v0, and the full range in that
   cell's tooltip. Cells that span several ages but agree on the value are not marked, because
   nothing was averaged. Measured on the shipped bundle: pooling all ages fills 272 of the 384
   (position x pick) pairs against 255 at the modal age alone, and only 28 of those 272 are genuinely
   multi-valued — so the mode buys 17 extra cells at the cost of 28 approximations, and the reader is
   told exactly which 28.

   NO PINNED FIGURES ANYWHERE. Every position, every draft age, the default age, the ordinals, the
   pool level and the curve domain are read from the loaded artifacts. The only literals below are
   the RULED constants (the 64-ordinal domain, the pool index, the 18-pick round) which are law, not
   this month's numbers, and the thin-sample threshold, which is a display choice.

   Dual-target, on the ui/app/movers.js pattern: `core` is pure and unit-tested under node
   (ui/tests/pickvalue.test.js); the browser gets the view. */
(function (root) {
  "use strict";

  /* ---- RULED CONSTANTS (law, not data) ---------------------------------------------------------
     Mirrored from the same law ui/app/trade.js states and ui/tools/ingest_inputs.py enforces, rather
     than approximated: the national curve prices ordinals 1-64 individually and everything past 64
     is the pool at one index. Kept as named constants so a reader can see they are the rulebook's
     numbers and not a board's. */
  var CURVE_MAX = 64;
  var POOL_KEY = "65";
  var ROUND_SIZE = 18;

  /* A DISPLAY CHOICE, and the only one: how few careers behind a cell earns the dot. Two or fewer.
     One career is obviously an anecdote; two is still one career and its friend. Three is where a
     cell stops being a coin flip about a single man's outcome. Deliberately NOT a data-derived
     quantile — a threshold that moved with the bake would mean something different every week. */
  var THIN_MAX = 2;

  /* ---- pure, dual-target logic (unit-tested under node) ---------------------------------------- */

  function uniqSortedNums(a) {
    var seen = {}, out = [];
    a.forEach(function (x) { if (!seen[x]) { seen[x] = 1; out.push(x); } });
    return out.sort(function (p, q) { return p - q; });
  }

  /* "KPF|18|1" -> {pos:"KPF", age:18, pick:1}, or null.
     STRICT ON PURPOSE. Anything that is not exactly three fields, with a non-empty position and two
     plain non-negative integers, is not a slot this page understands — and a slot whose pick falls
     outside the curve's ruled domain is not a PICK at all (it would be pool territory, where order
     of selection carries no value). All of those return null and are counted as dropped by index()
     rather than being coerced into the nearest thing that would render. */
  function parseSlot(slot) {
    if (typeof slot !== "string") return null;
    var parts = slot.split("|");
    if (parts.length !== 3) return null;
    var pos = String(parts[0]).trim();
    if (!pos) return null;
    if (!/^[0-9]+$/.test(parts[1]) || !/^[0-9]+$/.test(parts[2])) return null;
    var age = Number(parts[1]), pick = Number(parts[2]);
    if (!(age > 0)) return null;
    if (!(pick >= 1 && pick <= CURVE_MAX)) return null;
    return { pos: pos, age: age, pick: pick };
  }

  /* The all-in column, read off the board bundle's `pvc`.
     Returns {ok, why, ordinals:[{n,v}], missing:[n...], pool}. FAILS CLOSED: a bundle with no curve,
     or a curve with nothing inside the ruled domain, yields ok:false and a reason naming the artifact
     — the page then renders that sentence instead of a table. An ordinal the curve does not price is
     omitted from `ordinals` and listed in `missing`, so a partial curve shows the rows it can stand
     behind and states which it could not, rather than filling the hole. */
  function curve(pvc) {
    if (!pvc || typeof pvc !== "object") {
      return { ok: false, why: "the loaded board bundle publishes no pick-value curve (`pvc` in " +
               "ui/data/board_view_working.js)", ordinals: [], missing: [], pool: null };
    }
    var ordinals = [], missing = [];
    for (var n = 1; n <= CURVE_MAX; n++) {
      var v = pvc[String(n)];
      if (typeof v === "number" && isFinite(v)) ordinals.push({ n: n, v: v });
      else missing.push(n);
    }
    if (!ordinals.length) {
      return { ok: false, why: "the loaded board's pick-value curve prices no ordinal in the ruled " +
               "1-" + CURVE_MAX + " domain", ordinals: [], missing: missing, pool: null };
    }
    /* The pool is read but kept OUT of `ordinals` — that separation is the whole point of law 4 and
       the reason this function exists rather than a bare Object.keys(pvc) loop somewhere. */
    var pool = pvc[POOL_KEY];
    return { ok: true, why: null, ordinals: ordinals, missing: missing,
             pool: (typeof pool === "number" && isFinite(pool)) ? pool : null };
  }

  /* Build the (position, pick) grid from resolved v0 rows.
     entries: [{key, slot, v0, origin}] — the shape MD.v0.of() answers in, so the browser hands this
     function exactly what the pinned reader gave it and nothing is re-derived.

     THE THREE EXCLUSIONS ARE COUNTED, NOT SWALLOWED, because the coverage line on the page has to be
     able to account for every board player it did not use:
       · nNoEntryPrice — the row carries no v0 at all (MD.v0 refused it, or none was recoverable).
       · nNotPickSlot  — a real entry price that is not a pick slot. Pool entrants (origin
                         "entry-anchor") live here: their entry price is a division level, so they
                         belong to no ordinal and cannot be put on a pick axis without inventing one.
       · nBadSlot      — a slot string that did not parse, or priced a pick outside the ruled domain.
                         Expected to be zero; if it ever is not, the page must be able to say so. */
  function index(entries) {
    var cells = {}, posSeen = {}, ageCount = {};
    var nUsed = 0, nNoEntryPrice = 0, nNotPickSlot = 0, nBadSlot = 0;
    (entries || []).forEach(function (e) {
      if (!e || e.v0 == null || typeof e.v0 !== "number" || !isFinite(e.v0)) { nNoEntryPrice++; return; }
      if (e.slot == null || e.slot === "") { nNotPickSlot++; return; }
      var s = parseSlot(e.slot);
      if (!s) { nBadSlot++; return; }
      posSeen[s.pos] = 1;
      ageCount[s.age] = (ageCount[s.age] || 0) + 1;
      var k = s.pos + "|" + s.pick;
      (cells[k] = cells[k] || []).push({ age: s.age, v0: e.v0, key: e.key || null });
      nUsed++;
    });
    var ages = Object.keys(ageCount).map(Number).sort(function (a, b) { return a - b; });
    /* THE DEFAULT DRAFT AGE IS DERIVED, NEVER TYPED. It is whichever age the loaded sidecar has the
       most observations at; ties break to the younger, so the answer is deterministic across bakes.
       A hardcoded 18 would be this bundle's fact wearing the look of a law. */
    var modalAge = null, best = -1;
    ages.forEach(function (a) { if (ageCount[a] > best) { best = ageCount[a]; modalAge = a; } });
    return {
      cells: cells,
      positions: Object.keys(posSeen).sort(),
      ages: ages,
      ageCount: ageCount,
      modalAge: modalAge,
      nUsed: nUsed,
      nNoEntryPrice: nNoEntryPrice,
      nNotPickSlot: nNotPickSlot,
      nBadSlot: nBadSlot,
    };
  }

  /* One grid cell, or null when the data genuinely has nothing there.
     age === null means "pool every draft age"; otherwise only that age's observations are used.

     `n` is the count of the observations ACTUALLY USED for this cell's figure and can never exceed
     them — the page prints it as the sample and a printed sample that overstated its evidence would
     be the same lie as an interpolated value. `aggregated` is true only when the used observations
     disagree, in which case `v0` is their mean and `lo`/`hi` carry the real range so the reader can
     see how much was smoothed; when they agree, nothing is averaged and lo === v0 === hi. */
  function cell(idx, pos, pick, age) {
    if (!idx || !pos) return null;
    var all = idx.cells[pos + "|" + pick];
    if (!all || !all.length) return null;
    var use = (age == null) ? all : all.filter(function (o) { return o.age === age; });
    if (!use.length) return null;
    var vals = use.map(function (o) { return o.v0; });
    var distinct = uniqSortedNums(vals);
    var aggregated = distinct.length > 1;
    var sum = 0;
    vals.forEach(function (v) { sum += v; });
    return {
      pos: pos,
      pick: pick,
      n: use.length,
      v0: aggregated ? (sum / vals.length) : distinct[0],
      lo: distinct[0],
      hi: distinct[distinct.length - 1],
      aggregated: aggregated,
      ages: uniqSortedNums(use.map(function (o) { return o.age; })),
      thin: use.length <= THIN_MAX,
    };
  }

  /* The rendered table, as data. One entry per ordinal the curve actually prices — so every row is
     inside the curve's domain by construction, and the pool can never leak in as a row.
     `pos` null (or an index with nothing for it) yields rows with cell/delta null: the all-in column
     stands alone, which is exactly the "no position selected" state and also the honest state when
     the v0 side is refused. */
  function rows(cur, idx, pos, age) {
    return ((cur && cur.ordinals) || []).map(function (o) {
      var c = pos ? cell(idx, pos, o.n, age) : null;
      /* A delta needs BOTH figures. Neither side is ever stood in for: no position value means no
         delta, not a delta against zero (which would render as a large negative number and read as
         a finding). */
      var delta = (c && typeof o.v === "number") ? (c.v0 - o.v) : null;
      return {
        n: o.n,
        round: Math.ceil(o.n / ROUND_SIZE),
        allIn: o.v,
        cell: c,
        delta: delta,
        ratio: (c && typeof o.v === "number" && o.v !== 0) ? (c.v0 / o.v) : null,
      };
    });
  }

  /* What the page says about its own sparsity, computed from the rows it is about to draw so the
     sentence can never drift from the table beneath it. */
  function coverage(rs) {
    var total = rs.length, filled = 0, thin = 0, aggregated = 0, obs = 0;
    rs.forEach(function (r) {
      if (!r.cell) return;
      filled++; obs += r.cell.n;
      if (r.cell.thin) thin++;
      if (r.cell.aggregated) aggregated++;
    });
    return { total: total, filled: filled, absent: total - filled, thin: thin,
             aggregated: aggregated, observations: obs };
  }

  var core = {
    CURVE_MAX: CURVE_MAX,
    POOL_KEY: POOL_KEY,
    ROUND_SIZE: ROUND_SIZE,
    THIN_MAX: THIN_MAX,
    parseSlot: parseSlot,
    curve: curve,
    index: index,
    cell: cell,
    rows: rows,
    coverage: coverage,
  };

  /* ---- the browser view ------------------------------------------------------------------------ */

  function makeView(MD) {
    var fmt = MD.fmt;

    /* View state. `pos` null is the opening state: the owner asked for a table of pick values FIRST
       and a position selector SECOND, so the page opens on the all-in table exactly as he described
       it. `age` is resolved lazily against the loaded data (see resolveAge) — it cannot be
       initialised here because the sidecar has not been read yet at module construction time.
       `allAges` is a separate flag rather than age===null so that flipping to all-ages and back
       remembers which single age you were on. */
    var state = { pos: null, age: null, allAges: false };

    /* Read every board player's entry price THROUGH MD.v0, one row at a time. Deliberately not a
       bulk read of window.__V0__: MD.v0.of() is the pinned path, and a refusal there (stale sidecar,
       wrong board, wrong store) must reach this page as a refusal rather than being routed around. */
    function entries() {
      if (!MD.v0 || typeof MD.v0.of !== "function") return null;
      var players = (MD.seam.working && MD.seam.working.players) || [];
      var out = [];
      players.forEach(function (p) {
        if (MD.isPickAsset && MD.isPickAsset(p)) return;   // a draft asset is not a player
        var r = MD.v0.of(p);
        if (!r || r.refused) return;
        out.push({ key: p.key, slot: r.slot, v0: r.v0, origin: r.origin });
      });
      return out;
    }

    /* Position order and labels come from MD.counting — the board's own six-code vocabulary and the
       owner's own labels — so this page cannot drift into a second spelling of "Key Fwd". A code the
       sidecar carries that counting.js does not know is still offered, under its raw code and after
       the known ones: dropping it would silently hide real data. */
    function orderedPositions(idx) {
      var known = (MD.counting && MD.counting.POSITIONS) || [];
      var have = {};
      idx.positions.forEach(function (p) { have[p] = 1; });
      var out = [];
      known.forEach(function (p) { if (have[p]) { out.push(p); delete have[p]; } });
      return out.concat(Object.keys(have).sort());
    }
    function posLabel(code) {
      var L = (MD.counting && MD.counting.LABELS) || {};
      return L[code] || code;
    }

    /* The selected age, clamped to what the data actually has. A remembered age that this bundle no
       longer carries falls back to the derived modal age rather than emptying the whole column. */
    function resolveAge(idx) {
      if (state.allAges) return null;
      if (state.age != null && idx.ageCount[state.age]) return state.age;
      return idx.modalAge;
    }

    function halt(page, headline, body) {
      var el = fmt.el("div", "cintro");
      el.innerHTML = '<span class="halt">' + fmt.esc(headline) + "</span> " + body;
      page.appendChild(el);
    }

    /* ---- controls ---- */

    function positionBar(idx, activeAge) {
      var wrap = fmt.el("div", "strip");
      wrap.appendChild(fmt.el("span", "lbl", "Position"));
      var seg = fmt.el("div", "seg");

      var allBtn = fmt.el("button", state.pos === null ? "on" : "", "All-in");
      allBtn.title = "The position-blind pick value curve on its own — no position selected.";
      allBtn.addEventListener("click", function () { state.pos = null; MD.render(); });
      seg.appendChild(allBtn);

      orderedPositions(idx).forEach(function (code) {
        var btn = fmt.el("button", state.pos === code ? "on" : "", fmt.esc(posLabel(code)));
        /* The tooltip carries the cell count for THIS position at the age currently selected, so the
           reader can see how thin a position is before he clicks into it and finds a column of
           em-dashes wondering whether the page is broken. */
        var filled = 0;
        for (var n = 1; n <= CURVE_MAX; n++) if (cell(idx, code, n, activeAge)) filled++;
        btn.title = posLabel(code) + " (" + code + ") — entry prices at " + filled + " of the " +
          CURVE_MAX + " pick ordinals" + (activeAge == null ? ", pooling every draft age" :
          " at draft age " + activeAge);
        btn.addEventListener("click", function () { state.pos = code; MD.render(); });
        seg.appendChild(btn);
      });
      wrap.appendChild(seg);
      return wrap;
    }

    function ageBar(idx) {
      var wrap = fmt.el("div", "strip");
      wrap.appendChild(fmt.el("span", "lbl", "Draft age"));
      var seg = fmt.el("div", "seg");
      var active = resolveAge(idx);

      idx.ages.forEach(function (a) {
        var btn = fmt.el("button", (!state.allAges && active === a) ? "on" : "", String(a));
        btn.title = "Draft age " + a + " — " + idx.ageCount[a] + " entry price" +
          (idx.ageCount[a] === 1 ? "" : "s") + " on the board." +
          " At a single draft age the surface carries exactly one value per (position, pick), so " +
          "nothing on the table is averaged.";
        btn.addEventListener("click", function () {
          state.allAges = false; state.age = a; MD.render();
        });
        seg.appendChild(btn);
      });

      var allBtn = fmt.el("button", state.allAges ? "on" : "", "All ages");
      allBtn.title = "Pool every draft age. This is the only mode that aggregates: where the pooled " +
        "ages disagree the cell shows their mean, marked ≈, with the real range on hover.";
      allBtn.addEventListener("click", function () { state.allAges = true; MD.render(); });
      seg.appendChild(allBtn);

      wrap.appendChild(seg);
      return wrap;
    }

    /* ---- the table ---- */

    function header(showPos, code) {
      var tr = fmt.el("tr");
      tr.appendChild(fmt.el("th", "rk", "Pick"));
      var rd = fmt.el("th", "club", "Round");
      rd.title = "Rounds of " + ROUND_SIZE + " — the ruled national draft round size.";
      tr.appendChild(rd);
      var ai = fmt.el("th", "", "All-in value");
      ai.title = "The adopted, position-blind pick value curve for the loaded release.";
      tr.appendChild(ai);
      if (showPos) {
        var pv = fmt.el("th", "", fmt.esc(posLabel(code)) + " v0");
        pv.title = "The entry price the frozen year-zero surface carries for a " + posLabel(code) +
          " at this pick. Read from the board's own players' entry prices — never fitted here.";
        tr.appendChild(pv);
        var sn = fmt.el("th", "picks", "n");
        sn.title = "How many board careers stand behind that figure. A dot marks " + THIN_MAX +
          " or fewer.";
        tr.appendChild(sn);
        var dl = fmt.el("th", "overall", "Δ vs all-in");
        dl.title = "Position entry price minus the all-in curve at the same pick. Two different " +
          "artifacts compared, not one decomposed — see the note below the table.";
        tr.appendChild(dl);
        var rt = fmt.el("th", "", "×");
        rt.title = "The same gap as a multiple of the all-in figure.";
        tr.appendChild(rt);
      }
      return tr;
    }

    /* THE ABSENT CELL. One em-dash, carrying its reason on hover, in every column the position side
       would have filled. Never a neighbour's value, never a fitted one, never a blank that could be
       mistaken for a rendering fault. */
    function absentCells(tr, code, n, activeAge) {
      var why = "No board player entered as a " + posLabel(code) + " at pick " + n +
        (activeAge == null ? " at any draft age" : " at draft age " + activeAge) +
        ". Nothing is interpolated, so nothing is shown.";
      ["", "picks", "overall", ""].forEach(function (cls) {
        var td = fmt.el("td", "num " + cls, "—");
        td.title = why;
        tr.appendChild(td);
      });
    }

    function row(r, showPos, code, activeAge) {
      var tr = fmt.el("tr");
      tr.appendChild(fmt.el("td", "rk num", String(r.n)));
      var within = ((r.n - 1) % ROUND_SIZE) + 1;
      tr.appendChild(fmt.el("td", "club", "R" + r.round + " · " + within));
      tr.appendChild(fmt.el("td", "num", fmt.n(r.allIn)));
      if (!showPos) return tr;

      if (!r.cell) { absentCells(tr, code, r.n, activeAge); return tr; }

      var c = r.cell;
      /* "≈" is carried ONLY when this cell actually averaged disagreeing values. A cell pooling
         several ages that all agree is exact and is not marked — marking it would cry wolf and blunt
         the marker where it matters. */
      var vtd = fmt.el("td", "num", (c.aggregated ? "≈ " : "") + fmt.n(c.v0));
      vtd.title = c.aggregated
        ? ("Mean of " + c.n + " entry prices across draft ages " + c.ages.join(", ") +
           ", which disagree: " + fmt.n(c.lo) + " to " + fmt.n(c.hi) + ". Shown as a mean because " +
           "“All ages” is selected; pick a single draft age for the exact figure.")
        : ("The surface's own figure for a " + posLabel(code) + " at pick " + r.n +
           " (draft age" + (c.ages.length === 1 ? " " : "s ") + c.ages.join(", ") +
           "). Nothing averaged: every observation here carries the same value.");
      tr.appendChild(vtd);

      /* The sample, and the dot. The dot is a TEXT character, not a colour or a border, so it
         survives a stylesheet this view is not allowed to touch and reads on any display. */
      var ntd = fmt.el("td", "num picks", String(c.n) + (c.thin ? " ·" : ""));
      ntd.title = c.n + " board career" + (c.n === 1 ? "" : "s") + " stand" + (c.n === 1 ? "s" : "") +
        " behind this figure" + (c.thin ? " — a thin sample; the dot marks it." : ".");
      tr.appendChild(ntd);

      var dtd = fmt.el("td", "num overall " + fmt.cls(r.delta), fmt.signed(Math.round(r.delta)));
      dtd.title = "A " + posLabel(code) + " entering at pick " + r.n + " was priced " +
        fmt.n(Math.abs(r.delta)) + " " + (r.delta >= 0 ? "above" : "below") +
        " the all-in curve at the same pick.";
      tr.appendChild(dtd);

      tr.appendChild(fmt.el("td", "num", r.ratio == null ? "—" :
        (Math.round(r.ratio * 100) / 100).toFixed(2) + "×"));
      return tr;
    }

    /* ---- render ---- */

    function render(container) {
      container.innerHTML = "";
      /* Reuses the clubs page's intro/halt/table styling contract by wearing its class as well as its
         own. The stylesheet is visual law and this view may not amend it, so it borrows rather than
         inventing an unstyled second vocabulary for the same three things. */
      var page = fmt.el("div", "clubspage pickvaluepage");

      var cur = curve(MD.seam.working && MD.seam.working.pvc);
      if (!cur.ok) {
        halt(page, "Pick value curve absent.", "There is no table to draw: " + fmt.esc(cur.why) +
          ". Nothing is estimated in its place.");
        container.appendChild(page);
        return;
      }

      /* THE POSITION SIDE MAY BE ABSENT WITHOUT TAKING THE PAGE DOWN. The all-in curve is on the
         board bundle and is honest on its own; the entry prices ride a separate, separately pinned
         sidecar. So a refused or missing sidecar costs the position column and says which artifact
         and why — it does not blank a table the loaded board can fully stand behind. */
      var raw = entries();
      var v0why = null;
      if (raw === null) {
        v0why = "the v0 entry-price reader (ui/app/v0.js) is not loaded";
      } else if (MD.v0 && typeof MD.v0.pin === "function" && !MD.v0.pin().ok) {
        v0why = MD.v0.pin().why;
      }
      var idx = index(raw || []);
      if (!v0why && !idx.nUsed) {
        v0why = "the v0 sidecar carries no entry price that resolves to a numbered pick on this board";
      }

      var activeAge = resolveAge(idx);
      var showPos = !v0why && state.pos != null;
      var rs = rows(cur, idx, showPos ? state.pos : null, activeAge);
      var cov = coverage(rs);

      // ---- provenance line: what each column is, always, whether or not a position is selected ----
      var prov = fmt.el("div", "cintro");
      /* The second sentence explains a column that only exists when the v0 side resolved, so it is
         withheld when that side is refused: a standing caveat about a comparison the page is not
         making would read as though it were making it. */
      prov.innerHTML =
        "<b>All-in value</b> is the adopted, position-blind pick value curve published by the loaded " +
        "board (<b>pvc</b>, ordinals 1–" + CURVE_MAX + "). " +
        (v0why ? "" :
          "<b>Position v0</b> is the frozen year-zero <i>entry price</i> of the board's own players, " +
          "read through the pinned v0 sidecar and keyed by the entry position the surface itself uses " +
          "— not a player's current eligibility. These are two different artifacts: the Δ is a " +
          "<b>comparison</b> between them and not a breakdown of the all-in curve, so the position " +
          "columns are not expected to average back to it.");
      page.appendChild(prov);

      if (v0why) {
        halt(page, "Position entry prices unavailable —", fmt.esc(v0why) +
          ". The all-in curve below is unaffected; no position column is shown rather than a " +
          "stand-in one.");
      } else {
        page.appendChild(positionBar(idx, activeAge));
        page.appendChild(ageBar(idx));
      }

      // ---- the honest sparsity / aggregation statement, computed from the rows drawn below -------
      if (showPos) {
        var note = fmt.el("div", "note");
        var parts = [];
        parts.push("<b>" + posLabel(state.pos) + "</b>: entry prices at <b>" + cov.filled +
          "</b> of the " + cov.total + " pick ordinals" +
          (activeAge == null ? ", pooling every draft age" : " at draft age " + activeAge) +
          " — <b>" + cov.absent + "</b> show an em-dash because the board holds no such entrant, " +
          "and nothing is interpolated to fill them.");
        parts.push(cov.observations + " careers stand behind the filled cells; <b>" + cov.thin +
          "</b> rest on " + THIN_MAX + " or fewer and are marked with a dot.");
        if (activeAge == null) {
          parts.push("<b>Aggregation is on.</b> “All ages” pools draft ages, and <b>" +
            cov.aggregated + "</b> cell" + (cov.aggregated === 1 ? "" : "s") +
            " below average genuinely disagreeing values — each is marked ≈ and carries its " +
            "full range on hover. Select a single draft age for figures the surface carries exactly.");
        } else {
          parts.push("<b>Nothing on this table is aggregated.</b> The entry surface is indexed by " +
            "(position, draft age, pick), so at a fixed draft age each cell is a single value the " +
            "surface carries — not a mean.");
        }
        note.innerHTML = parts.join(" ");
        page.appendChild(note);
      }

      // ---- the table ----
      var table = fmt.el("table", "ctable");
      var thead = fmt.el("thead");
      thead.appendChild(header(showPos, state.pos));
      table.appendChild(thead);
      var tbody = fmt.el("tbody");
      rs.forEach(function (r) { tbody.appendChild(row(r, showPos, state.pos, activeAge)); });
      table.appendChild(tbody);
      var wrap = fmt.el("div", "tablewrap");
      wrap.appendChild(table);
      page.appendChild(wrap);

      /* THE POOL, BENEATH THE TABLE AND NEVER IN IT. Index 65 of `pvc` is the committed pool level,
         not a 65th pick: past ordinal 64 the rulebook prices one bucket and order of selection
         carries no value. Printing it as a row would manufacture an ordinal that does not exist. */
      var foot = fmt.el("div", "note");
      var poolTxt = (cur.pool == null)
        ? "The loaded board publishes no pool level, so none is shown."
        : "<b>Pool — " + fmt.n(cur.pool) + "</b>. Everything past pick " + CURVE_MAX +
          " is one position-blind bucket at this level, with order of selection carrying no value. " +
          "It is not a " + (CURVE_MAX + 1) + "th pick and is deliberately not a row above.";
      var missTxt = cur.missing.length
        ? " The loaded curve prices no value at ordinal" + (cur.missing.length === 1 ? " " : "s ") +
          cur.missing.join(", ") + ", so " + (cur.missing.length === 1 ? "that row is" : "those rows are") +
          " absent rather than filled."
        : "";
      /* The board's own accounting of who could not be placed on this axis at all. Stated even when
         every count is zero, because a coverage claim the reader cannot audit is not a coverage
         claim. */
      var accTxt = v0why ? "" :
        " Entry prices read: " + idx.nUsed + " on numbered picks" +
        (idx.nNotPickSlot ? ", " + idx.nNotPickSlot + " pool entrants (a division level, not a pick " +
          "slot — they belong to no ordinal)" : "") +
        (idx.nNoEntryPrice ? ", " + idx.nNoEntryPrice + " with no recoverable entry price" : "") +
        (idx.nBadSlot ? ", " + idx.nBadSlot + " with an unreadable slot key (dropped, never guessed)" : "") +
        ".";
      foot.innerHTML = poolTxt + missTxt + accTxt;
      page.appendChild(foot);

      container.appendChild(page);
    }

    return { render: render, core: core, _state: state };
  }

  /* ---- registration: browser (window.MD) + node (module.exports for tests) --------------------- */
  if (typeof window !== "undefined") {
    window.MD = window.MD || {};
    // Deferred exactly as movers.js defers: script order guarantees MD.fmt, but a view that assumes
    // it and is wrong renders a blank tab instead of an error, which is the worst of both.
    window.MD.pickvalue = (window.MD.fmt) ? makeView(window.MD) : {
      render: function (h) { window.MD.pickvalue = makeView(window.MD); window.MD.pickvalue.render(h); },
      core: core,
    };
  }
  if (typeof module !== "undefined" && module.exports) {
    module.exports = { core: core, makeView: makeView };
  }
})(this);
