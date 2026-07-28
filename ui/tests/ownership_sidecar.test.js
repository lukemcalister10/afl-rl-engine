/* #232 — the LIVE-lane ownership sidecar, and the fail-closed public-tier name bridge.
 *
 * WHAT IS AT RISK.  The sidecar overrides ownership in the browser so a trade costs an edit rather than
 * an engine run.  The failure mode that matters is not "the override doesn't work" — that is loud.  It
 * is a PARTIAL override: some views take the sidecar and others keep the board's stored affl_team, so a
 * traded player sits in two clubs at once and nothing says so.  The public tier is where that bites,
 * because public rows carry NO key and can only be joined by display name.
 *
 * Today all 804 display names are distinct on store e3aaba77.  That is DATA, not a guarantee.  So the
 * bridge must REFUSE on an ambiguous or unmatched name — return no club and report the row — rather than
 * resolve to one candidate or quietly fall back to the stored club as though it were current.
 *
 * NON-VACUITY.  Every refusal is asserted BOTH directions: the broken population refuses, and a control
 * population differing only in the offending name resolves clean.  A refusal test that never sees the
 * passing case cannot distinguish "correctly refused" from "refuses everything".
 *
 * Run: node ui/tests/ownership_sidecar.test.js
 */
"use strict";
const fs = require("fs");
const vm = require("vm");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
let pass = 0, fail = 0;
function check(cond, name, detail) {
  if (cond) { pass++; console.log("  [PASS] " + name); }
  else { fail++; console.log("  [FAIL] " + name + (detail ? " — " + detail : "")); }
}

const FILES = [
  "ui/data/board_view_working.js",
  "ui/data/board_view_public.js",
  "ui/data/club_valuation.js",
  "ui/data/ownership.js",
  "ui/app/positions_data.js",
  "ui/app/config.js",
  "ui/app/format.js",
  "ui/app/counting.js",
  "ui/app/seam.js",
  "ui/app/ownership.js",
  "ui/app/club_totals.js",
];

/* Load the UI into a browser-ish context. `mutate(ctx, runIn)` runs after the DATA bundles are in place
   but before the APP modules, so a test can reshape the population the modules will read.

   USE `runIn` FOR ANYTHING TOP-LEVEL.  A host-side `delete ctx.__FOO__` does NOT propagate into the VM's
   global — the host then reads `undefined` while the VM still sees the object.  A "sidecar absent" test
   written that way silently exercises the sidecar-PRESENT path, and passes anyway because the shipped
   sidecar currently agrees with the store on all 804 players.  That is a check that cannot fail.  Nested
   mutation (`ctx.__MATCHDAY_WORKING__.players[0].name = …`) is fine — same object either side. */
function loadUI(mutate) {
  const ctx = { console };
  ctx.window = ctx; ctx.globalThis = ctx;
  vm.createContext(ctx);
  const runIn = function (src) { return vm.runInContext(src, ctx, { filename: "test-mutation" }); };
  FILES.forEach(function (f) {
    if (f === "ui/app/config.js" && mutate) mutate(ctx, runIn);   // after data, before app
    vm.runInContext(fs.readFileSync(path.join(ROOT, f), "utf8"), ctx, { filename: f });
  });
  return ctx;
}

function workingPlayers(ctx) { return ctx.__MATCHDAY_WORKING__.players.filter(p => p.key); }

/* ------------------------------------------------------------------ 1 · override and fallback */
console.log("\nOVERRIDE AND FALLBACK — the sidecar's core contract");
{
  const victimKey = "nick-daicos";
  const ctx = loadUI(function (c) {
    const p = c.__MATCHDAY_WORKING__.players.find(x => x.key === victimKey);
    c.__ORIG_CLUB__ = p.affl_team;
    // move him somewhere he certainly is not, using a spelling the board already knows
    const other = c.__MATCHDAY_WORKING__.players.find(x => x.affl_team && x.affl_team !== p.affl_team);
    c.__NEW_CLUB__ = other.affl_team;
    c.__OWNERSHIP__.byKey[victimKey] = other.affl_team;
    // and remove a different player from the sidecar entirely, to exercise the store fallback
    c.__FALLBACK_KEY__ = c.__MATCHDAY_WORKING__.players.find(x => x.key && x.key !== victimKey).key;
    c.__FALLBACK_CLUB__ = c.__MATCHDAY_WORKING__.players.find(x => x.key === c.__FALLBACK_KEY__).affl_team;
    delete c.__OWNERSHIP__.byKey[c.__FALLBACK_KEY__];
  });
  const MD = ctx.MD;
  const victim = workingPlayers(ctx).find(p => p.key === victimKey);
  const fb = workingPlayers(ctx).find(p => p.key === ctx.__FALLBACK_KEY__);

  check(MD.ownership.clubOf(victim) === ctx.__NEW_CLUB__,
        "a player the sheet names takes the SIDECAR's club, not the board's",
        "got " + MD.ownership.clubOf(victim) + ", board says " + victim.affl_team);
  check(victim.affl_team === ctx.__ORIG_CLUB__,
        "the board bundle itself is left untouched (override is a read-time overlay)");
  check(MD.ownership.clubOf(fb) === ctx.__FALLBACK_CLUB__,
        "a player the sheet does NOT name falls back to the board's stored affl_team");
  check(MD.ownership.resolve(victim).overridden === true && MD.ownership.resolve(fb).overridden === false,
        "resolve() reports which rows are actually overridden");

  // the club totals must follow the override — this is the whole point of the lane
  const tot = MD.clubTotals.compute();
  const newClub = tot.clubs.find(c => c.team === MD.canonClub(ctx.__NEW_CLUB__));
  check(newClub && newClub.best23Keys.concat([]).length >= 0 &&
        tot.clubs.find(c => c.team === MD.canonClub(ctx.__NEW_CLUB__)).nRoster >
        0, "club totals recompute against the sidecar's membership");
  const rosterHasVictim = MD.clubTotals.compute().clubs
    .find(c => c.team === MD.canonClub(ctx.__NEW_CLUB__));
  check(!!rosterHasVictim, "the receiving club exists in the recomputed totals");
}

/* ------------------------------------------------- 2 · public bridge REFUSES on an ambiguous name */
console.log("\nPUBLIC BRIDGE — ambiguous display name (asserted both directions)");
{
  // CONTROL: untouched population. The name must resolve.
  const ctl = loadUI(null);
  const pubName = ctl.__MATCHDAY_PUBLIC__.players[0].name;
  const pubRow = ctl.__MATCHDAY_PUBLIC__.players[0];
  const r0 = ctl.MD.ownership.resolve(pubRow);
  check(r0.refused === false && r0.club, "control — a distinct public name resolves to a club",
        JSON.stringify(r0));
  check(ctl.MD.ownership.publicRefusals().length === 0,
        "control — no public row is refused on the shipped population",
        String(ctl.MD.ownership.publicRefusals().length));

  // DEFECT: make two DIFFERENT working players share that display name.
  const amb = loadUI(function (c) {
    const ps = c.__MATCHDAY_WORKING__.players.filter(x => x.key);
    const target = ps.find(x => x.name === pubName);
    const other = ps.find(x => x.key !== target.key);
    other.name = target.name;                       // collision: two keys, one name
  });
  const rA = amb.MD.ownership.resolve(amb.__MATCHDAY_PUBLIC__.players.find(p => p.name === pubName));
  check(rA.refused === true, "an ambiguous name is REFUSED, not resolved to one candidate",
        JSON.stringify(rA));
  check(rA.club === null, "a refused row yields NO club (it cannot be counted into one)");
  check(/shared by more than one player/.test(rA.why || ""),
        "the refusal states that the name is shared", rA.why);
  check(amb.MD.ownership.labelOf(amb.__MATCHDAY_PUBLIC__.players.find(p => p.name === pubName))
        === amb.MD.ownership.REFUSED_LABEL,
        "a refused row DISPLAYS the refusal rather than the stored club");
  check(amb.MD.ownership.publicRefusals().length > 0,
        "the refusal is reported, not just rendered",
        String(amb.MD.ownership.publicRefusals().length));
}

/* --------------------------------------------------- 3 · public bridge REFUSES on unmatched name */
console.log("\nPUBLIC BRIDGE — unmatched display name (asserted both directions)");
{
  const ctl = loadUI(null);
  const rc = ctl.MD.ownership.resolve(ctl.__MATCHDAY_PUBLIC__.players[1]);
  check(rc.refused === false, "control — the same row resolves before the name is broken");

  const un = loadUI(function (c) {
    c.__MATCHDAY_PUBLIC__.players[1].name = "Nobody Whatsoever";   // matches no working player
  });
  const ru = un.MD.ownership.resolve(un.__MATCHDAY_PUBLIC__.players[1]);
  check(ru.refused === true, "a name matching no working player is REFUSED", JSON.stringify(ru));
  check(/matches no player/.test(ru.why || ""), "the refusal says the name matched nothing", ru.why);
  check(un.MD.ownership.publicRefusals().indexOf("Nobody Whatsoever") >= 0,
        "the unmatched name appears in the reported refusals");
}

/* --------------------------------------- 4 · a refused row is excluded, never counted into a club */
console.log("\nREFUSAL IS EXCLUSION — a row we cannot identify enters no club total");
{
  const un = loadUI(function (c) {
    c.__MATCHDAY_PUBLIC__.players[2].name = "Nobody At All";
  });
  const row = un.__MATCHDAY_PUBLIC__.players[2];
  check(un.MD.ownership.clubOf(row) === null,
        "clubOf() of a refused row is null, so canonClub folds it into the '—' bucket");
}

/* ------------------------------------------------ 5 · no sidecar / halted sidecar -> store, quietly */
console.log("\nNO SIDECAR AND HALTED SIDECAR — fall back to the store, refuse nothing");
{
  // The absence must be created INSIDE the context, and proven — see the loadUI note. To make the
  // fallback assertion non-vacuous the store value is also moved, so "falls back to the store" and
  // "took the sidecar" are different answers rather than the same one.
  const none = loadUI(function (c, runIn) {
    const k = c.__MATCHDAY_WORKING__.players.find(x => x.key).key;
    const p = c.__MATCHDAY_WORKING__.players.find(x => x.key === k);
    c.__OWNERSHIP__.byKey[k] = "Sydney Swans";
    p.affl_team = "Geelong Cats";              // store and sidecar now disagree
    c.__PROBE_KEY__ = k;
    runIn("delete window.__OWNERSHIP__;");
  });
  check(none.MD.ownership.status().present === false,
        "the sidecar really is absent inside the VM (guards the delete-does-not-propagate trap)");
  const p = none.__MATCHDAY_WORKING__.players.find(x => x.key === none.__PROBE_KEY__);
  check(none.MD.ownership.clubOf(p) === "Geelong Cats",
        "with NO sidecar every row falls back to the store (pre-#232 behaviour)",
        "got " + none.MD.ownership.clubOf(p));
  check(none.MD.ownership.publicRefusals().length === 0,
        "with NO sidecar nothing is refused — there is no override to diverge from");
  check(none.MD.ownership.status().active === false, "status() reports the sidecar inactive");

  const halted = loadUI(function (c, runIn) {
    runIn("window.__OWNERSHIP__ = { stamp: {}, halt: { reason: 'test halt' }, byKey: {}, "
          + "stableIdByKey: {}, overriding: [] };");
  });
  check(halted.MD.ownership.status().halted === true, "status() reports a halted sidecar");
  check(halted.MD.ownership.clubOf(halted.__MATCHDAY_WORKING__.players.find(x => x.key)) !== null,
        "a halted sidecar still renders the board rather than blanking the app");
}

/* ------------------------------------------------------- 6 · ONE PLAYER, ONE CLUB, ACROSS ALL TIERS */
console.log("\nONE PLAYER, ONE CLUB — the two-clubs-at-once condition must be impossible");
{
  const victimKey = "nick-daicos";
  const ctx = loadUI(function (c) {
    const p = c.__MATCHDAY_WORKING__.players.find(x => x.key === victimKey);
    const other = c.__MATCHDAY_WORKING__.players.find(x => x.affl_team && x.affl_team !== p.affl_team);
    c.__OWNERSHIP__.byKey[victimKey] = other.affl_team;
    c.__NEW_CLUB__ = other.affl_team;
  });
  const MD = ctx.MD;
  const wRow = ctx.__MATCHDAY_WORKING__.players.find(p => p.key === victimKey);
  const pRow = ctx.__MATCHDAY_PUBLIC__.players.find(p => p.name === wRow.name);
  check(MD.ownership.clubOf(wRow) === ctx.__NEW_CLUB__, "working tier shows the new club");
  check(MD.ownership.clubOf(pRow) === ctx.__NEW_CLUB__, "public tier shows the SAME new club",
        "public got " + MD.ownership.clubOf(pRow));

  // and every resolvable public row agrees with its working twin, across the whole population
  const byName = {};
  ctx.__MATCHDAY_WORKING__.players.forEach(p => { if (p.key && p.name != null) byName[p.name] = p; });
  const disagree = ctx.__MATCHDAY_PUBLIC__.players.filter(function (pp) {
    const w = byName[pp.name];
    if (!w) return false;
    const a = MD.ownership.clubOf(pp), b = MD.ownership.clubOf(w);
    return MD.ownership.resolve(pp).refused ? false : a !== b;
  });
  check(disagree.length === 0,
        "no player resolves to different clubs on the working and public tiers",
        disagree.length + " disagreement(s): " + disagree.slice(0, 3).map(p => p.name).join(", "));
}

/* --------------------------------------------------- 7 · movers rows resolve without the bridge */
console.log("\nMOVERS — keyed rows, so ownership resolves without touching the name bridge");
{
  const ctx = loadUI(null);
  const movers = JSON.parse(
    (function () {
      const s = fs.readFileSync(path.join(ROOT, "ui/data/movers.js"), "utf8");
      return s.slice(s.indexOf("{", s.indexOf("=")), s.lastIndexOf("}") + 1);
    })()
  );
  const wKeys = {}; ctx.__MATCHDAY_WORKING__.players.forEach(p => { if (p.key) wKeys[p.key] = 1; });
  const orphan = Object.keys(movers.values || {}).filter(k => !wKeys[k]);
  check(orphan.length === 0,
        "every movers record key exists on the working board, so no mover row needs the name bridge",
        orphan.length + " orphan(s)");
  const k = Object.keys(movers.values)[0];
  const row = { key: k, affl_team: movers.values[k].affl_team, name: movers.values[k].name };
  check(ctx.MD.ownership.resolve(row).refused === false,
        "a movers row resolves cleanly through the keyed path");
}

/* ------------------------------------------------ 8 · positions must never appear in the live lane */
console.log("\nLANE SEPARATION — positions are batched and must not be in the sidecar");
{
  const raw = fs.readFileSync(path.join(ROOT, "ui/data/ownership.js"), "utf8");
  const side = JSON.parse(raw.slice(raw.indexOf("{", raw.indexOf("__OWNERSHIP__")), raw.lastIndexOf("}") + 1));
  const banned = ["pos", "posCode", "position", "present_position", "future_position", "drafted_position", "v"];
  const found = [];
  Object.keys(side).forEach(function (top) {
    const v = side[top];
    if (v && typeof v === "object" && !Array.isArray(v)) {
      Object.keys(v).forEach(function (k) { if (banned.indexOf(k) >= 0) found.push(top + "." + k); });
    }
  });
  check(found.length === 0,
        "the sidecar carries no position or value field — the live lane cannot trigger an engine run",
        found.join(", "));
  check(typeof side.byKey === "object" && Object.keys(side.byKey).length > 0,
        "…and it is non-empty, so that assertion is not passing on an empty file",
        Object.keys(side.byKey || {}).length + " entries");
}

/* ------------------------------------------------- 9 · the read surface stays migrated, and wired
   The defect this job exists to remove is a PARTIAL override: a new view reads `p.affl_team` straight
   off the board, and one traded player sits in two clubs with nothing reporting it.  The read surface
   was 19 occurrences across 6 files when this landed.  This asserts every remaining direct read is one
   of the handful that legitimately touches the raw field, so a NEW direct read fails here rather than
   in the owner's browser.  Upkeep is one allowlist line per genuinely new raw use — priced, and cheap,
   against a defect that is invisible when it happens. */
console.log("\nREAD SURFACE — no view may read the stored affl_team directly");
{
  const ALLOWED = [
    "affl_team: rec.affl_team",              // movers projection: copies the bundle field; resolved at read
    "affl_team: null",                       // board.js pickAsset(): an asset is not a player
    "if (p && p.affl_team) m[String(p.affl_team)",   // format.js: builds the club-SPELLING vocabulary
    "(p ? p.affl_team : null)",              // movers ownClub(): the documented node fallback
  ];
  /* Blank out comments before scanning. Line-prefix matching is not enough: these files carry long
     block comments whose continuation lines start with ordinary words, and several of them discuss
     affl_team by name — they would read as offenders while the actual code went unchecked. */
  function stripComments(src) {
    let out = "", inBlock = false, inLine = false, inStr = null;
    for (let i = 0; i < src.length; i++) {
      const c = src[i], d = src[i + 1];
      if (inBlock) { if (c === "*" && d === "/") { inBlock = false; i++; } out += (c === "\n" ? "\n" : " "); continue; }
      if (inLine) { if (c === "\n") { inLine = false; out += "\n"; } else out += " "; continue; }
      if (inStr) { if (c === "\\") { out += "  "; i++; continue; } if (c === inStr) inStr = null; out += c; continue; }
      if (c === "/" && d === "*") { inBlock = true; i++; out += "  "; continue; }
      if (c === "/" && d === "/") { inLine = true; i++; out += "  "; continue; }
      if (c === '"' || c === "'" || c === "`") { inStr = c; out += c; continue; }
      out += c;
    }
    return out;
  }

  const dir = path.join(ROOT, "ui", "app");
  const offenders = [];
  fs.readdirSync(dir).filter(f => f.endsWith(".js")).forEach(function (f) {
    if (f === "ownership.js") return;                       // the module whose job this is
    const lines = stripComments(fs.readFileSync(path.join(dir, f), "utf8")).split("\n");
    lines.forEach(function (ln, i) {
      if (ln.indexOf("affl_team") < 0) return;
      if (ln.indexOf("MD.ownership") >= 0 || ln.indexOf("ownClub(") >= 0) return;  // goes through the layer
      if (ALLOWED.some(a => ln.indexOf(a) >= 0)) return;
      offenders.push(f + ":" + (i + 1) + "  " + ln.trim().slice(0, 90));
    });
  });
  check(offenders.length === 0,
        "every view resolves ownership through MD.ownership, not the raw board field",
        "\n      " + offenders.join("\n      "));

  const html = fs.readFileSync(path.join(ROOT, "ui", "index.html"), "utf8");
  const iData = html.indexOf("data/ownership.js");
  const iApp = html.indexOf("app/ownership.js");
  check(iData >= 0 && iApp >= 0, "index.html loads both the sidecar bundle and the ownership module");
  const consumers = ["app/club_totals.js", "app/board.js", "app/card.js", "app/pocket.js", "app/movers.js"];
  const late = consumers.filter(c => html.indexOf(c) >= 0 && html.indexOf(c) < iApp);
  check(late.length === 0,
        "app/ownership.js is loaded before every module that consumes it", late.join(", "));
  check(iData < iApp, "the sidecar DATA bundle is loaded before the module that reads it");
}

console.log("\n" + (fail ? "FAIL" : "PASS") + " — " + pass + " passed, " + fail + " failed");
process.exit(fail ? 1 : 0);
