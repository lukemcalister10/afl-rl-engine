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
    return m[name] || name;
  },
};

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
