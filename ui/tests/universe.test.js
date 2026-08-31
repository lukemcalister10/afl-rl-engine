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
const newestStored = all[all.length - 1];
ok(cur[cur.length - 1] === newestStored,
   "...and forward to the newest stored point (" + newestStored + ")");

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
const oorAtSameRound = U.points(B).filter(function (p) {
  return p.kind === "out_of_round" && p.after_round != null && roundKinds[String(p.after_round)];
});
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
  ok(compared > 700, "the retro tail and the live head are comparable across the board (" + compared + " players)");
  ok(differ > 0 && differ < compared,
     "...and the handover carries real football, not a copy (" + differ + " of " + compared + " moved)");
} else {
  ok(false, "could not locate the retro/live handover in the current-model universe");
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
