#!/usr/bin/env python3
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
def load_js(path):
    text = path.read_text(encoding="utf-8")
    return json.loads(text[text.index("{"):text.rindex("}") + 1])
boot = json.load(open(ROOT / "data/expected_boot.json"))
cv = load_js(ROOT / "ui/data/club_valuation.js")
assert cv.get("halt") is None, cv.get("halt")
assert cv["stamp"]["board"] == boot["board"]
assert cv["stamp"]["asOfRound"] == boot["as_of_round"]
assert len(cv.get("clubs", [])) == 16
assert sum(len(v) for v in cv.get("picksByTeam", {}).values()) == 160
assert len({c["team"] for c in cv["clubs"]}) == 16
for c in cv["clubs"]:
    assert c["overall"] == c["totalPlayer"] + c["totalPicks"]
    assert c["totalPlayer"] == c["best23"] + c["nonBest23"]
    assert c["nRoster"] > 0
print("CLUB VALUATION CURRENT PASS: R%d, 16 clubs, 160 picks" % boot["as_of_round"])
