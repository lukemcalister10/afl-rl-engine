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
   sole carrier (LOCK). Supersedes the ten-block MD.powerBar; the old squares are not protected. */
MD.valueLine = function (v, maxV, mini) {
  const pct = (MD.fmt.frac(v, maxV) * 100).toFixed(1);
  return '<span class="vline' + (mini ? " vline-m" : "") + '">' +
    '<span class="vmask" style="left:' + pct + '%"></span></span>';
};
