/* Matchday UI — formatting helpers. LOCK amendment 2: comma digit grouping on every value. */
window.MD = window.MD || {};

MD.fmt = {
  /* "3,462" — comma grouping. Years and picks are labels, not grouped values (callers pass those raw). */
  n: function (x) {
    if (x === null || x === undefined || Number.isNaN(x)) return "—";
    return Math.round(x).toLocaleString("en-US");
  },
  /* signed movement figure with the fixed arrow grammar; colour is never the sole carrier. */
  signed: function (d) {
    if (d === null || d === undefined || Number.isNaN(d)) return "—";
    if (d > 0) return "▲ +" + MD.fmt.n(d);
    if (d < 0) return "▼ −" + MD.fmt.n(Math.abs(d));
    return "— 0";
  },
  cls: function (d) {
    if (d === null || d === undefined || Number.isNaN(d)) return "na";
    if (d > 0) return "up";
    if (d < 0) return "dn";
    return "flat";
  },
  /* fraction 0..1 of the top price (the value line's fill). */
  frac: function (v, maxV) {
    if (!maxV || !v || v < 0) return 0;
    return Math.max(0, Math.min(1, v / maxV));
  },
  el: function (tag, cls, html) {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html !== undefined) e.innerHTML = html;
    return e;
  },
  esc: function (s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  },
  /* item 178(1): the DISPLAY name for an AFFL club — the owner's three shortened clubs map here, every
     other club passes through verbatim. Display-only; callers keep the raw name as the join key. */
  club: function (name) {
    if (name == null) return "—";
    const m = (MD.config && MD.config.CLUB_DISPLAY) || {};
    const c = MD.canonClub(name);
    return m[c] || c;
  },
};

/* #139 item 5 — the duplicate "Free agents" category, CANONICALISED FOR DISPLAY AND FILTERING ONLY.
   The duplicate does NOT originate in the UI: the authored store carries two spellings of one AFFL
   bucket — 73 rows `Free agents` and 2 rows `Free Agents` (tyler-brockman, liam-stocker). Store
   authorship is the owner's alone and this job has no store authority, so nothing is fixed at source.

   ui/tools/extract_board_view.py already folds the two spellings for the BOARD bundles, so the board
   and the player card never showed the duplicate. `ui/data/movers.js` does NOT: it carries 511 rows
   spelled `Free agents` and 14 spelled `Free Agents`, so the Movers club filter listed the pool TWICE
   and each entry selected only part of it. That is the live defect this closes.

   The canonical spelling is not invented here and is not hardcoded: it is READ from the board bundle,
   whose team names the extractor has already normalised. A name that matches a board team
   case-insensitively resolves to the board's spelling; anything else passes through trimmed and
   verbatim. So a future case-variant of any club folds automatically, and a genuinely unknown club is
   never silently renamed into a different one. Built lazily on first call — format.js loads before
   seam.js, and this only ever runs at render time. */
MD.canonClub = (function () {
  let index = null;
  function build() {
    const m = {};
    const w = (typeof MD.seam !== "undefined" && MD.seam && MD.seam.working) || null;
    ((w && w.players) || []).forEach(function (p) {
      if (p && p.affl_team) m[String(p.affl_team).trim().toLowerCase()] = String(p.affl_team).trim();
    });
    return m;
  }
  return function (name) {
    if (name == null) return null;
    const raw = String(name).trim().replace(/\s+/g, " ");
    if (!raw) return null;
    if (index === null) index = build();
    return index[raw.toLowerCase()] || raw;
  };
})();

/* Pick-asset guard (owner ruling, register v16 item 14): the current board is a PLAYER RANKING.
   A pick-asset row is a draft-pick line, not a player. Display-only test used to keep the current /
   backward-lens ladders players-only; picks stay on the trade desk and at the +1/+2 lenses. */
MD.isPickAsset = function (p) {
  if (!p) return false;
  if (p.asset === "pick" || p.kind === "pick" || p.isPick === true || p.posCode === "PICK") return true;
  if (typeof p.key === "string" && /^pick[-_]?\d+/i.test(p.key)) return true;
  if (typeof p.name === "string" && /^pick\s*\d+\b/i.test(p.name)) return true;
  return false;
};

/* OVER-FREE LENS (#274 item 3; owner word 2026-07-29, durable spec in #279 seed ruling S-5).

   `v − FHV`: what a player is worth ABOVE what the free-agent tier reasonably hands you for nothing.
   FHV is the ruled constant (MD.config.FHV = 190; see the ruling note there). A player below it is a
   standing delist candidate — the "below free" flag — because his place on the list costs more than it
   returns against a free hit.

   COMPUTED AT RENDER, EVERY TIME. Nothing is stored, nothing is re-pinned, no bundle carries it. Pass a
   board value in, get the lens out; null in, null out, so a row without a value shows "—" rather than a
   fabricated −190. `belowFree` is the flag; `overFree` is the figure. */
MD.overFree = function (v) {
  return (v == null) ? null : (v - MD.config.FHV);
};
MD.belowFree = function (v) {
  return (v != null) && (v < MD.config.FHV);
};

/* value line (item 3 · owner-worded amendment to the Matchday LOCK, register item 163, 2026-07-15):
   a CONTINUOUS filling line, not ten segmented blocks. The colour spectrum is anchored to the TRACK
   (0..top price), and the unfilled remainder is masked, so the fill reveals the spectrum from the cool
   end up to the player's value — the colour shifts as it fills (a top player reaches the hot end, a
   sub-bar player only the cool end). The figure is always printed alongside, so colour is never the
   sole carrier (LOCK). Supersedes the ten-block MD.powerBar; the old squares are not protected.

   ================= OWNER ITEM 11 (2026-08-31): THE BAR IS NOW READ "vs PICK 1" =================
   His word: the column stops being "vs top" and becomes "vs Pick 1", carrying a ratio to two decimal
   places, rendered ON the bar and legible against it.

   TWO DIFFERENT THINGS SHARE ONE BAR, AND THEY ARE KEPT SEPARATE ON PURPOSE:

     · THE FILL is still anchored 0..top-of-board. That is what makes the column comparable DOWN the
       page — every bar is drawn on the same track, so their lengths rank the board at a glance. If
       the fill were anchored to pick 1 instead, every player above pick 1 would peg at 100% and the
       whole top of the board would render as one identical full bar, which destroys the column.
     · THE NUMBER is the ratio to pick 1, to 2dp. That is the reading he asked for: 9000 against a
       pick 1 of 3000 reads 3.00x, 300 reads 0.10x.
     · THE TICK reconciles them. A single hairline sits at pick 1's own position ON that same track,
       so "past the tick" means worth more than pick 1 and "short of it" means worth less. Without
       the tick the ratio would be a number floating on a bar that does not encode it; with it, the
       bar and the figure are the same statement.

   PICK 1 IS READ, NEVER HARDCODED. MD.pick1() takes ordinal 1 off the loaded board's own published
   curve (`MD.seam.working.pvc`). It is 3000 on today's release and that number appears nowhere in
   this file: a re-anchored curve moves the tick and every ratio with it, with no code change. When
   the curve is absent the ratio and tick are simply not drawn — the bar degrades to what it always
   was rather than printing a ratio against a denominator nobody published.

   LEGIBILITY IS DECIDED, NOT HOPED FOR. The label cannot be painted at a fixed spot: the track runs
   from a dark cool end to a bright warm one, and the unfilled remainder is dark. So the label is
   placed on whichever side of the fill boundary it can be read against, and takes the matching
   colour — outside the fill (light text on the dark remainder) while the bar is short, inside the
   fill (dark text on the bright warm end) once the fill is long enough to swallow it. */
MD.pick1 = function () {
  const pvc = (MD.seam && MD.seam.working && MD.seam.working.pvc) || null;
  if (!pvc) return null;
  const v = pvc["1"];
  return (typeof v === "number" && isFinite(v) && v > 0) ? v : null;
};

/* the point on the 0..maxV track where pick 1 sits, as a percentage; null when it is off the track
   (no curve, or a board whose top player is worth less than pick 1 — then there is nothing to mark). */
MD.pick1Mark = function (maxV) {
  const p1 = MD.pick1();
  if (p1 == null || !maxV || p1 >= maxV) return null;
  return (p1 / maxV) * 100;
};

/* the label flips sides at the point where the fill is long enough to hold it. 62% is measured, not
   guessed: the label is ~34px wide in the board's mono at 10px, and the narrowest board bar column
   is 88px at the smallest wide-layout width, so the fill must reach roughly three fifths before the
   text fits inside it with its own padding. Below that it reads on the dark remainder instead. */
const VRATIO_INSIDE_AT = 62;

MD.valueLine = function (v, maxV, mini) {
  const pct = (MD.fmt.frac(v, maxV) * 100).toFixed(1);
  const p1 = mini ? null : MD.pick1();
  let extra = "";
  if (p1 != null && v != null) {
    const mark = MD.pick1Mark(maxV);
    if (mark != null) {
      extra += '<span class="vp1" style="left:' + mark.toFixed(2) + '%" ' +
        'title="Pick 1 = ' + MD.fmt.n(p1) + '. Bars past this line are worth more than pick 1."></span>';
    }
    /* TWO DECIMALS COLLAPSE AT THE FOOT OF THE BOARD, AND "0.00x" IS A FALSE READING. Caught on
       the rendered page, not in a test: the bottom ~120 rows are worth single digits against a pick
       1 of 3000, so every one of them printed 0.00x — a column of zeroes against players who are
       not worth zero. Below the point where 2dp rounds to nothing the cell says "<0.01x", which is
       exactly true and still honours the two decimals he asked for, rather than inventing a third
       and fourth to fill a screen nobody reads at that precision. A genuine zero still prints
       0.00x, so the two cases stay distinguishable. */
    const rr = v / p1;
    const ratio = (rr > 0 && rr < 0.005) ? "<0.01" : rr.toFixed(2);
    const inside = parseFloat(pct) >= VRATIO_INSIDE_AT;
    extra += '<span class="vratio ' + (inside ? "in" : "out") + '" style="left:' + pct + '%" ' +
      'title="' + MD.fmt.n(v) + ' against pick 1 at ' + MD.fmt.n(p1) + '">' +
      ratio + "\u00d7</span>";
  }
  /* the taller line is asked for by CLASS, not inferred by the stylesheet from its own contents.
     A :has() selector would have read the same but makes the row height depend on a selector
     feature; the class states it, and one grep finds every rule that reacts to it. */
  return '<span class="vline' + (mini ? " vline-m" : "") + (extra ? " vline-r" : "") + '">' +
    '<span class="vmask" style="left:' + pct + '%"></span>' + extra + "</span>";
};
