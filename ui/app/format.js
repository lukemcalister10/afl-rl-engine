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
  /* ten-block power bar: fill = decile of the top price. Returns filled-block count 0..10. */
  decile: function (v, maxV) {
    if (!maxV || !v || v < 0) return 0;
    return Math.max(0, Math.min(10, Math.round((v / maxV) * 10)));
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
};

/* segmented power bar markup (ten blocks, N filled). */
MD.powerBar = function (v, maxV, mini) {
  const n = MD.fmt.decile(v, maxV);
  let s = '<span class="' + (mini ? "powmini" : "pow") + '">';
  for (let i = 0; i < 10; i++) s += "<i" + (i < n ? ' class="f"' : "") + "></i>";
  return s + "</span>";
};
