#!/usr/bin/env python3
"""ui/data/club_valuation.js — the PICKS contract.

WHAT CHANGED, AND WHY THIS TEST CHANGED WITH IT (#139 item 21, owner ruling 2026-07-28).

This file used to assert that the bundle's baked per-club totals were current, by requiring
`cv.stamp.board == expected_boot.board`. That assertion was correct for what the bundle then was, and
it was the thing that would have caught the staleness — but it was never wired into CI, and the bundle
went stale twice unnoticed: it was generated against board fa172ac1 while the board moved on to
8a38cca4 (the ITEM 411 restructure, then round 20). All 16 clubs' player totals were wrong.

The ruling was not "regenerate it more reliably" but "stop baking the sum": per-club player totals,
Top-5/10, Best-23 and Non-Best-23 are now computed in the browser from the board on screen
(ui/app/club_totals.js), so they cannot lag the board at all. That computation is proven equal to the
ingest's own algorithm by ui/tests/club_totals_parity.test.js.

So the board-identity assertion is now the WRONG assertion to make here, and keeping it would leave a
permanently-red test asserting a property nothing depends on. What the bundle is still authoritative
for is its PICKS: each held pick priced by the engine's canonical PVC evaluated over a band. A pick's
price comes from the curve, not from the board, so it does not go stale when the board moves — which is
exactly why the picks side stayed correct while the totals rotted.

This test therefore asserts (a) the picks contract, against the PVC identity that actually governs it,
and (b) that no UI code has started reading the baked totals again — the regression that would quietly
reintroduce the staleness.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]


def load_js(path):
    text = path.read_text(encoding="utf-8")
    return json.loads(text[text.index("{"):text.rindex("}") + 1])


cv = load_js(ROOT / "ui/data/club_valuation.js")
stamp = cv["stamp"]

# ---------------------------------------------------------------- (a) the picks contract
assert cv.get("halt") is None, "ingest halted: %r" % (cv.get("halt"),)

picks_by_team = cv.get("picksByTeam", {})
n_picks = sum(len(v) for v in picks_by_team.values())
assert len(picks_by_team) == 16, "expected 16 teams in the picks ledger, got %d" % len(picks_by_team)
_years = sorted({p["year"] for t in cv["picksByTeam"].values() for p in t})
_expected = 16 * 5 * len(_years)
assert n_picks == _expected, "expected %d held picks (16x5x%d years %s), got %d" % (_expected, len(_years), _years, n_picks)
assert stamp["nPicks"] == n_picks, "stamp nPicks %r disagrees with the ledger (%d)" % (stamp["nPicks"], n_picks)

# every pick is a band with a price on it; the price is the curve's, never re-derived here.
for team, picks in picks_by_team.items():
    for p in picks:
        assert p["value"] > 0, "%s: pick %r has no value" % (team, p.get("band"))
        assert p["low"] <= p["high"], "%s: band %r is inverted" % (team, p.get("band"))
        assert p["year"] in (2026, 2027, 2028), "%s: unexpected pick year %r" % (team, p.get("year"))

# the PVC identity that actually governs pick prices.
assert stamp["pvcOk"] is True, "the ingest did not validate the PVC"
assert stamp["pvcCurveMd5"], "no PVC curve identity on the bundle"
release_curve = ROOT / stamp["releaseCurveContract"]
assert release_curve.exists(), "release curve contract missing: %s" % stamp["releaseCurveContract"]

# ---------------------------------------------------------------- (b) nothing reads the baked totals
# The bundle still CARRIES `clubs` (the ingest writes it); the point is that the UI must not read it.
# MD.seam deliberately exposes the bundle as `clubBundle`, and only the picks accessors touch it.
BAKED_KEYS = ("totalPlayer", "best23", "nonBest23", "top5", "top10", "overall")
app_dir = ROOT / "ui/app"
offenders = []
for js in sorted(app_dir.glob("*.js")):
    src = js.read_text(encoding="utf-8")
    # strip block and line comments so the explanatory prose above these guards is not itself a hit
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    src = re.sub(r"^\s*//.*$", "", src, flags=re.M)
    for m in re.finditer(r"(clubBundle|__CLUB_VALUATION__)\s*(?:\.\s*|\[\s*[\"'])(\w+)", src):
        field = m.group(2)
        if field in ("clubs",) or field in BAKED_KEYS:
            offenders.append("%s: reads %s.%s" % (js.name, m.group(1), field))
assert not offenders, (
    "UI code is reading the baked club totals again — they go stale on every board move. "
    "Use MD.clubTotals (computed from the board). Offenders: " + "; ".join(offenders)
)

print(
    "CLUB VALUATION PICKS PASS: 16 teams, %d picks, PVC %s; no UI code reads the baked totals "
    "(they are computed live by MD.clubTotals — see ui/tests/club_totals_parity.test.js)"
    % (n_picks, stamp["pvcCurveMd5"])
)
