/* Matchday UI — board view (working + public tiers). Pure view; no re-valuation. */
window.MD = window.MD || {};

MD.board = (function () {
  const fmt = MD.fmt;
  let onlyReads = false;

  /* players visible at the active lens, with the displayed value + rank. */
  function rows(tier) {
    const s = MD.state;
    const nowLens = s.lens === 2;
    let pool;
    if (tier === "public") {
      // public tier carries no `ov` (leak-proof), so MD.dispVal falls back to p.v here
      pool = (MD.seam.public.players || []).map(function (p) { return { p: p, val: MD.dispVal(p) }; });
    } else {
      const w = MD.seam.working;
      // now-lens: displayed value = the override figure (ov.dispv) when overridden, else v; ordering follows
      // this displayed value. Lens boards show the projected lens-year figure (the override is a now read).
      pool = (w.players || []).map(function (p) { return { p: p, val: nowLens ? MD.dispVal(p) : p.lens[s.lens] }; });
      if (!nowLens && s.lens < 2) {
        // backward-board-only players surface at −1 / −2
        (w.back || []).forEach(function (p) {
          const val = p.lens[s.lens];
          if (val !== null && val !== undefined) pool.push({ p: p, val: val, back: true });
        });
      }
    }
    pool = pool.filter(function (r) { return r.val !== null && r.val !== undefined; });
    // Pick-asset filter (owner ruling, register v16 item 14): the current board is a player ranking.
    // Exclude pick-asset rows on the current + backward lenses; picks stay at the +1/+2 lenses and on
    // the trade desk. Display-only — the underlying board is untouched.
    if (s.lens <= 2) {
      pool = pool.filter(function (r) { return !MD.isPickAsset(r.p); });
    }
    pool.sort(function (a, b) { return b.val - a.val; });
    pool.forEach(function (r, i) { r.rank = i + 1; });
    return pool;
  }

  function maxVal(pool) { return pool.length ? pool[0].val : 1; }

  function deltaPill(p, displayedVal) {
    const s = MD.state;
    if (s.lens !== 2) {
      // lens board: Δ shown vs now (a diff of two given board figures, not a recomputation)
      const d = p.v == null ? null : displayedVal - p.v;
      return '<span class="pill ' + fmt.cls(d) + '" title="' + MD.config.LENS_LABELS[s.lens] +
        ' board value vs now">' + fmt.signed(d) + '</span>';
    }
    if (s.deltaBase === "bake") {
      if (p.vPrev == null) {
        return '<span class="pill na" title="Δ vs last accepted bake — column built, awaiting the vPrev ' +
          'export field (§7.3; one-line engine-side addition). No Δ is invented.">—</span>';
      }
      return '<span class="pill ' + fmt.cls(p.v - p.vPrev) + '" title="Δ vs last accepted bake">' +
        fmt.signed(p.v - p.vPrev) + '</span>';
    }
    // round
    if (p.dRound == null) {
      return '<span class="pill na" title="Δ vs previous round — arrives with the weekly loop (Phase 3).">—</span>';
    }
    return '<span class="pill ' + fmt.cls(p.dRound) + '">' + fmt.signed(p.dRound) + "</span>";
  }

  function workingRow(r, maxV, byKey) {
    const p = r.p;
    const anc = MD.anchorStatus(p.key, byKey);
    let pin = '<span class="pin"></span>';
    if (anc) {
      pin = '<span class="pin ' + (anc.status === "met" ? "pinf" : "pinh") + '" title="Your read: ' +
        fmt.esc(anc.read) + " — " + (anc.status === "met" ? "met" : "watching") +
        (anc.verified ? " (verified on the board)" : "") + '">★</span>';
    }
    let nm = '<span class="nm">' + fmt.esc(p.name);
    if (p.owner_rule) {
      nm += '<span class="tag" title="Owner override active — the owner\'s rule, not the model\'s curve, ' +
        'is holding this number. Post-override figure shown. ' +
        (p.vRaw != null ? "Model pre-override: " + fmt.n(p.vRaw) + "."
          : "Model pre-override figure arrives with the vRaw export field (§7.3).") +
        '">Owner override</span>';
    }
    if (MD.state.slugs) nm += '<span class="slug">' + fmt.esc(p.key) + "</span>";
    nm += "</span>";
    const b = fmt.el("button", "row working");
    b.innerHTML =
      '<span class="rank num">' + r.rank + "</span>" + pin + nm +
      '<span class="pos">' + fmt.esc(p.pos) + "</span>" +
      // item 1: AFL club + AFFL club, listed per player (AFFL is the team-context lens focus, so it leads
      // in volt; AFL is the muted sub-line). Display-only strings from the bundle; "—" when absent.
      '<span class="club"><span class="affl" title="AFFL club">' + fmt.esc(p.affl_team || "—") + "</span>" +
        '<span class="afl" title="AFL club">' + fmt.esc(p.afl_club || "—") + "</span></span>" +
      '<span class="val num">' + fmt.n(r.val) + "</span>" +
      MD.powerBar(r.val, maxV) +
      deltaPill(p, r.val) +
      '<span class="meta">' + (p.pk ? "pk " + p.pk : "—") + " · ’" + String(p.yr || "").slice(2) + "</span>";
    b.addEventListener("click", function () { MD.go("card", p.key); });
    return b;
  }

  function publicRow(r, maxV) {
    const p = r.p;
    const move = p.dRound == null
      ? '<span class="pill flat" title="movement vs previous round — published with the weekly loop">— steady</span>'
      : '<span class="pill ' + fmt.cls(p.dRound) + '">' + fmt.signed(p.dRound) + "</span>";
    const rankMove = p.dRoundRank == null
      ? '<span class="pill flat">— steady</span>'
      : '<span class="pill ' + fmt.cls(p.dRoundRank) + '">' +
        (p.dRoundRank > 0 ? "▲ " + p.dRoundRank : p.dRoundRank < 0 ? "▼ " + Math.abs(p.dRoundRank) : "— 0") + "</span>";
    const b = fmt.el("button", "row public");
    b.innerHTML =
      '<span class="rank num">' + r.rank + "</span>" +
      '<span class="nm">' + fmt.esc(p.name) + "</span>" +
      '<span class="pos">' + fmt.esc(p.pos) + "</span>" +
      '<span class="val num">' + fmt.n(r.val) + "</span>" +
      MD.powerBar(r.val, maxV) + move + rankMove;
    return b;
  }

  function strip(container) {
    const s = MD.state;
    const wrap = fmt.el("div", "strip");
    const yr = (MD.seam.working.stamp || {}).baseYear || 2026;
    wrap.innerHTML = '<span class="lbl">Round 17 · ' + yr + (s.tier === "public" ? " · published" : "") + "</span>";
    wrap.appendChild(fmt.el("span", "spacer"));

    // ±1/2-yr board lens (both tiers meaningful for value-by-year, but kept working-only per two-tier trim)
    if (s.tier === "working") {
      wrap.appendChild(fmt.el("span", "lbl", "Board lens"));
      const lens = fmt.el("div", "seg lens");
      MD.config.LENS_LABELS.forEach(function (lab, i) {
        const btn = fmt.el("button", i === s.lens ? "on" : "", lab);
        btn.addEventListener("click", function () { s.lens = i; render(container); });
        lens.appendChild(btn);
      });
      wrap.appendChild(lens);

      // Q-DELTA-BASE toggle (built; default = bake). Dimmed on a non-now lens (does not apply).
      wrap.appendChild(fmt.el("span", "lbl", "Δ base"));
      const dseg = fmt.el("div", "seg");
      [["bake", "bake"], ["round", "round"]].forEach(function (pair) {
        const btn = fmt.el("button", s.deltaBase === pair[0] ? "on" : "", pair[1]);
        if (s.lens !== 2) { btn.disabled = true; btn.style.opacity = ".4"; btn.style.cursor = "default"; }
        else btn.addEventListener("click", function () { s.deltaBase = pair[0]; render(container); });
        dseg.appendChild(btn);
      });
      wrap.appendChild(dseg);
      if (s.lens === 2) {
        const anyPrev = (MD.seam.working.players || []).some(function (p) {
          return s.deltaBase === "bake" ? p.vPrev != null : p.dRound != null;
        });
        if (!anyPrev) {
          const note = fmt.el("span", "lbl");
          note.style.color = "var(--faint)";
          note.style.letterSpacing = ".04em";
          note.style.textTransform = "none";
          note.textContent = s.deltaBase === "bake"
            ? "· Δ column built — awaiting the one-line vPrev bake export (§7.3); no Δ invented"
            : "· Δ vs round arrives with the weekly loop (Phase 3)";
          wrap.appendChild(note);
        }
      }

      // My reads filter
      wrap.appendChild(fmt.el("span", "lbl", "Filter"));
      const rseg = fmt.el("div", "seg");
      [["all", "all"], ["reads", "my reads"]].forEach(function (pair) {
        const on = (pair[0] === "reads") === onlyReads;
        const btn = fmt.el("button", on ? "on" : "", pair[1]);
        btn.addEventListener("click", function () { onlyReads = pair[0] === "reads"; render(container); });
        rseg.appendChild(btn);
      });
      wrap.appendChild(rseg);

      // Debug slugs
      wrap.appendChild(fmt.el("span", "lbl", "Debug"));
      const dbg = fmt.el("div", "seg dbg");
      [["off", "slugs off"], ["on", "on"]].forEach(function (pair) {
        const on = (pair[0] === "on") === s.slugs;
        const btn = fmt.el("button", on ? "on" : "", pair[1]);
        btn.addEventListener("click", function () { s.slugs = pair[0] === "on"; render(container); });
        dbg.appendChild(btn);
      });
      wrap.appendChild(dbg);
    }
    container.appendChild(wrap);
  }

  function render(container) {
    container.innerHTML = "";
    const s = MD.state;
    strip(container);

    const byKey = MD.seam.indexed().byKey;
    let pool = rows(s.tier);
    const maxV = maxVal(pool);
    if (s.tier === "working" && onlyReads) {
      pool = pool.filter(function (r) { return MD.anchors[r.p.key]; });
    }

    const rowsEl = fmt.el("div", "rows");
    pool.slice(0, 60).forEach(function (r) {
      rowsEl.appendChild(s.tier === "working" ? workingRow(r, maxV, byKey) : publicRow(r, maxV));
    });
    container.appendChild(rowsEl);

    const foot = fmt.el("footer", "foot");
    if (s.tier === "working") {
      foot.innerHTML = "volt = your touch (reads · rules · controls) · blocks = share of the top price, one block a decile · " +
        "movement pills always signed · override headroom lives on the card's waterfall · showing top 60 of " +
        fmt.n(pool.length) + (s.lens !== 2 ? " at the " + MD.config.LENS_LABELS[s.lens] + " lens" : "");
    } else {
      foot.innerHTML = "blocks = share of the top price, one block a decile · movement pills always signed, never colour alone · public trim — no ids, no internals";
    }
    container.appendChild(foot);
  }

  return { render: render };
})();
