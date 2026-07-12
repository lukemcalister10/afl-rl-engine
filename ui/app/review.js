/* Matchday UI — round review. Reserved: blocked on the Phase-3 weekly loop. Rendered in the Matchday
   look so the slot is designed-in now, wired later (never renders a fake round). */
window.MD = window.MD || {};

MD.review = (function () {
  const fmt = MD.fmt;
  function render(container) {
    const yr = (MD.seam.working.stamp || {}).baseYear || 2026;
    container.innerHTML =
      '<div class="summary">' +
        '<span><b>▲ —</b>players up</span>' +
        '<span><b>▼ —</b>players down</span>' +
        '<span><b>—</b>unchanged / not graded</span>' +
        '<span><b>—</b>board total</span>' +
      "</div>" +
      '<div class="reserved" style="margin-top:16px">' +
        '<b>Wired in the weekly-loop phase (Phase 3).</b> "What moved and why": movers ranked by |Δ|, each row ' +
        "expanding to the same per-lever waterfall as the player card — one attribution language everywhere. " +
        "History starts clean post-overhaul; the view states its round + model version; a re-bake mid-season starts a " +
        "new series with a seam marker, never a mixed line. Round " + (yr) + " deltas arrive with round-score ingestion." +
      "</div>" +
      '<footer class="foot">round review renders nothing fake until the weekly loop exists — the contract is written in DATA_CONTRACT (ii)</footer>';
  }
  return { render: render };
})();
