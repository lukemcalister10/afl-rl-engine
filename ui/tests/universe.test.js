/* THE TWO UNIVERSES (owner ruling 2026-08-31). Asserted against the SHIPPED bundle, and asserted as
   RELATIONSHIPS rather than this month's point counts — the counts move every time anything lands. */
global.window = { localStorage: { _d: {}, getItem: function (k) { return this._d[k] || null; },
                                  setItem: function (k, v) { this._d[k] = v; } } };
const fs = require("fs"), path = require("path");
(new Function("window", fs.readFileSync(path.join(__dirname, "..", "data", "movers.js"), "utf8")))(window);
const U = require("../app/universe.js");
const B = window.__MATCHDAY_MOVERS__;

let fails = 0, n = 0;
function ok(c, l) { n++; console.log((c ? "  [PASS] " : "  [FAIL] ") + l); if (!c) fails++; }
function ids(m) { U.setMode(m); return U.points(B).map(function (p) { return String(p.id); }); }

const cur = ids(U.CURRENT), all = ids(U.ALL);
const mc = U.modelChangeIds(B);

U.setMode(U.ALL);
ok(U.mode() === U.ALL, "the mode round-trips through storage");
U.setMode(U.CURRENT);
ok(U.mode() === U.CURRENT, "...and back");

/* THE DEFINING PROPERTY, and the whole reason the owner asked for this: no model change is inside
   the current-model universe, so a span across it is football and nothing else. */
ok(cur.every(function (i) { return !mc[i]; }),
   "NO model change is in the current-model universe (" + cur.filter(function (i) { return mc[i]; }).length + " found)");
ok(all.some(function (i) { return mc[i]; }),
   "...and the all-in universe DOES carry them — the switch is not vacuous");

ok(cur.join(",") !== all.join(","), "the two universes are different point sets");
ok(cur.length >= 2 && all.length >= 2, "both universes are non-empty enough to compare across");

ok(cur.some(function (i) { return /^retro-r14$/.test(i); }),
   "the current-model universe reaches back to R14");
/* ...AND FORWARD TO THE NEWEST POINT THE RULING ADMITS, which is not always the newest stored one.
   A model change is excluded from this universe BY DEFINITION (the assertion above), so in the window
   between a model change landing and the next round, the newest stored point is not admissible and the
   universe legitimately ends at the last retro point. The bust-exclusion landing (2026-09-01) opened
   exactly that window and the old form of this check — a bare `cur.last === all.last` — went red on a
   correct board. It was asserting a temporary state as an invariant; every model change opens this
   window until football lands. Stated properly it still catches the regression it was written for. */
const newestStored = all[all.length - 1];
const newestIsModelChange = !!mc[newestStored];
if (newestIsModelChange) {
  const lastRetro = cur.filter(function (i) { return i.indexOf("retro-r") === 0; }).pop();
  ok(cur[cur.length - 1] === lastRetro,
     "...and forward to the last retro point (" + cur[cur.length - 1] + ") — the newest stored point (" +
     newestStored + ") is a MODEL CHANGE and is excluded by the rule above, so this is the window " +
     "between a model change and the next round");
} else {
  ok(cur[cur.length - 1] === newestStored,
     "...and forward to the newest stored point (" + newestStored + ")");
}

/* NO ROUND'S FOOTBALL APPEARS TWICE. Stated carefully, because `after_round` is NOT a round
   identity: an out-of-round column carries the round it was registered AT, so retro-r24 and the FW1
   column both report after_round 24 and are nonetheless different events — one is round 24's
   football re-priced, the other is a board move that happened while the calendar stood at 24.
   Counting bare after_round collisions would call that a duplicate, which is why this counts only
   the thing that would actually double a history: a ROUND appearing as both a stored round and a
   retro re-pricing of the same round. */
const roundKinds = {};
let dup = 0;
U.setMode(U.CURRENT);
U.points(B).forEach(function (p) {
  const isRoundish = p.kind === "round" || p.kind === "retro";
  if (!isRoundish || p.after_round == null) return;
  const k = String(p.after_round);
  if (roundKinds[k]) dup++;
  roundKinds[k] = true;
});
ok(dup === 0, "no round's football appears twice in the current-model universe (" + dup + " duplicates)");

/* ...and the distinction just relied upon is itself asserted, so the reasoning above cannot quietly
   stop being true: at least one out-of-round column must share an after_round with a round point. */
/* ASSERTED OVER THE ALL-IN UNIVERSE, because that is where the distinction lives. It is a property of
   the BUNDLE — that `after_round` is a registration stamp and not a round identity — not a property of
   the current-model universe, which by construction holds few or no out-of-round columns and may hold
   none at all in the window described above. Checking it on CURRENT made it fail on a correct board
   for a reason that had nothing to do with what it defends. */
U.setMode(U.ALL);
const allRoundKinds = {};
U.points(B).forEach(function (p) {
  if ((p.kind === "round" || p.kind === "retro") && p.after_round != null) {
    allRoundKinds[String(p.after_round)] = true;
  }
});
const oorAtSameRound = U.points(B).filter(function (p) {
  return p.kind === "out_of_round" && p.after_round != null && allRoundKinds[String(p.after_round)];
});
U.setMode(U.CURRENT);
ok(oorAtSameRound.length >= 1,
   "an out-of-round column DOES sit at the same after_round as a round point — which is why the check above is not a bare collision count");

/* THE MEASURED JOIN. The retrospective's last round and the stored point it hands over to must be
   comparable across the whole board, or the series has a seam and "one model throughout" is false.
   This is the property that lets a finals week join with no re-pricing. */
const vals = B.values || {};
const retros = cur.filter(function (i) { return i.indexOf("retro-r") === 0; });
const lastRetro = retros[retros.length - 1];
const firstLive = cur[cur.indexOf(lastRetro) + 1];
if (lastRetro && firstLive) {
  let compared = 0, differ = 0;
  Object.keys(vals).forEach(function (k) {
    const bp = vals[k].byPoint || {};
    if (bp[lastRetro] && bp[firstLive]) { compared++; if (bp[lastRetro].v !== bp[firstLive].v) differ++; }
  });
  /* RESTATED 2026-09-24 (FINALS WEEK 3). At FW2 the live tail was ONE finals week, so "the point after
     the last retro" and "the live head" were the same point and `differ === 0` held. At FW3 the tail is
     two weeks, and the check compared retro-r27 (FW3) with fw2 (FW2): 177 players differ, which is
     one week of football, not a broken seam. What that exposed was real — the current-model history
     carried every finals week TWICE (retro-rN and its stored column) — and universe.points now keeps
     only the stored one. The seam is asserted as the three things it always meant: */
  const weekOfBoard = {};
  Object.keys(B.reports || {}).forEach(function (r) {
    const rep = B.reports[r];
    if (rep && rep.board_md5_after) weekOfBoard[String(rep.board_md5_after)] = Number(r);
  });
  const byId = {};
  U.points(B).forEach(function (p) { byId[String(p.id)] = p; });
  (B.points || []).forEach(function (p) { if (!byId[String(p.id)]) byId[String(p.id)] = p; });
  const weekOf = function (id) { const p = byId[id]; return p && p.board ? weekOfBoard[String(p.board)] : undefined; };
  ok(compared > 700, "the retro tail and the live head are comparable across the board (" + compared + " players)");
  // (a) ONE WEEK, ONE BOARD: every banked retro week that is also a stored point agrees with it exactly.
  let pairs = 0, pairDiffer = 0;
  (B.points || []).filter(function (p) { return p.kind === "retro"; }).forEach(function (rp) {
    const rep = (B.reports || {})[String(rp.after_round)];
    // the twin must be a LIVE point (after the last model change): an older stored point for the
    // same week (FW1, before the bust exclusion) is the same football under a superseded model.
    const twin = rep && cur.map(function (i) { return byId[i]; }).filter(function (q) {
      return q && q.kind !== "retro" && q.board && String(q.board) === String(rep.board_md5_after); })[0];
    if (!twin) return;
    pairs++;
    Object.keys(vals).forEach(function (k) {
      const bp = vals[k].byPoint || {};
      if (bp[rp.id] && bp[twin.id] && bp[rp.id].v !== bp[twin.id].v) pairDiffer++;
    });
  });
  ok(pairs > 0 && pairDiffer === 0,
     "the seam is EXACT: every banked week that is also a stored point is the same board (" + pairs +
     " week(s), " + pairDiffer + " player readings differ)");
  // (b) NO WEEK TWICE in the current-model history.
  const curWeeks = cur.map(function (i) {
    return i.indexOf("retro-r") === 0 ? Number(i.slice("retro-r".length)) : weekOf(i); })
    .filter(function (w) { return w !== undefined; });
  const dupWeeks = curWeeks.filter(function (w, j) { return curWeeks.indexOf(w) !== j; });
  ok(dupWeeks.length === 0, "no week appears twice in the current-model history (" + dupWeeks.join(",") + ")");
  // (c) NO GAP, NO OVERLAP at the handover: the first live point is the week after the last retro.
  const handoverWeek = weekOf(firstLive);
  ok(handoverWeek === undefined || handoverWeek === Number(lastRetro.slice("retro-r".length)) + 1,
     "the handover is seamless: " + lastRetro + " is followed by week " + handoverWeek + " (" + firstLive + ")");
  let repriced = 0, checkedRounds = 0;
  retros.forEach(function (rid) {
    const rn = String(rid).slice("retro-r".length);
    if (!allRoundKinds[rn]) return;                       // no stored round at that number to compare
    checkedRounds++;
    Object.keys(vals).forEach(function (k) {
      const bp = vals[k].byPoint || {};
      if (bp[rid] && bp[rn] && bp[rid].v !== bp[rn].v) repriced++;
    });
  });
  ok(checkedRounds > 0 && repriced > 0,
     "...and the retrospective is a RE-PRICING, not duplicated stored values (" + repriced +
     " player-round readings differ across " + checkedRounds + " rounds that have both)");
} else {
  /* NO HANDOVER EXISTS IN THIS WINDOW, and that is not a failure. The handover is the seam between the
     retro tail and the live head, so it only exists once a ROUND has landed after the last model
     change. Between a model change and the next round the universe is retro-only, there is no live
     head, and a `ok(false)` here reds a correct board — which is what it did on 2026-09-01. What is
     worth asserting instead is that the absence has the RIGHT CAUSE: retro-only because the newest
     stored point is a model change, not because the retro series went missing. */
  const lastRetroOnly = cur.filter(function (i) { return i.indexOf("retro-r") === 0; });
  ok(lastRetroOnly.length === cur.length && cur.length > 0 && newestIsModelChange,
     "no retro/live handover yet, and for the right reason: the universe is retro-only (" +
     cur.length + " points) because the newest stored point (" + newestStored + ") is a model change. " +
     "The handover returns with the next round.");
}

const realLS = window.localStorage;
window.localStorage = { getItem: function () { throw new Error("blocked"); },
                        setItem: function () { throw new Error("blocked"); } };
let threw = false;
try { U.setMode(U.ALL); U.points(B); } catch (e) { threw = true; }
window.localStorage = realLS;
ok(!threw, "a localStorage that throws does not break the universe (it falls back in-page)");

console.log("  " + "-".repeat(60));
if (fails) { console.log("UNIVERSE TESTS: " + fails + " FAIL / " + n); process.exit(1); }
console.log("UNIVERSE TESTS: ALL " + n + " PASS");
