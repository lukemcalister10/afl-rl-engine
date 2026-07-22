#!/usr/bin/env python3
"""Produce complete before/after evidence for the true-now-anchored graded-staleness candidate."""
from __future__ import annotations

import argparse
import contextlib
import csv
import hashlib
import io
import json
import os
import sys
from pathlib import Path


def md5(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def rows_of(path: Path):
    obj = json.loads(path.read_text(encoding="utf-8"))
    return obj, obj["active"] if isinstance(obj, dict) else obj


def rank_map(rows, field):
    ordered = sorted((p for p in rows if p.get("key")),
                     key=lambda p: (-(float(p.get(field) or 0)), p["key"]))
    return {p["key"]: i for i, p in enumerate(ordered, 1)}


def load_engine(workspace: Path):
    old = Path.cwd()
    for p in (workspace, Path("/home/claude/rl_vendor")):
        if p.exists() and str(p) not in sys.path:
            sys.path.insert(0, str(p))
    env = {"__name__": "anchor_fix_diagnostic"}
    try:
        os.chdir(workspace)
        with contextlib.redirect_stdout(io.StringIO()):
            src = (workspace / "_merged_recover.py").read_text(encoding="utf-8")
            exec(src.split('print("=== AFTER')[0], env)
    finally:
        os.chdir(old)
    return env


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--workspace", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    bp, cp, ws, out = map(Path, (a.baseline, a.candidate, a.workspace, a.out))
    bp, cp, ws, out = bp.resolve(), cp.resolve(), ws.resolve(), out.resolve()
    out.mkdir(parents=True, exist_ok=True)

    _, before_rows = rows_of(bp)
    _, after_rows = rows_of(cp)
    before = {p["key"]: p for p in before_rows if p.get("key")}
    after = {p["key"]: p for p in after_rows if p.get("key")}
    assert len(before) == len(after) == 804 and set(before) == set(after)
    ranks = {(side, field): rank_map(rows, field)
             for side, rows in (("before", before_rows), ("after", after_rows))
             for field in ("v", "vP1", "vP2")}

    g = load_engine(ws)
    MA, PR = g["MA"], g["PR"]
    nseas_pro, stale_grade = g["nseas_pro"], g["_staleness_grade"]
    form_clock, fa_year, isreal = g["_form_anchor_clock"], g["_fa_year"], g["_isreal"]
    store = {p.get("key"): p for p in MA.data if p.get("key") and not p.get("_retired")}

    output = []
    fire_keys, zero_live = set(), set()
    for key in sorted(before):
        b, c, p = before[key], after[key], store.get(key)
        pos = (c.get("grp") or c.get("gf") or b.get("grp") or b.get("gf"))
        fire = False
        grade_now = grade_p1 = grade_p2 = None
        anchor_p1 = anchor_p2 = None
        current_games = current_avg = tenure = quals = onset = None
        if p is not None and isreal(p):
            pos = MA.gfut(p)
            with form_clock():
                tenure = int(PR.tenure(p, fa_year(2026)))
            quals = int(nseas_pro(p, 2026))
            onset = 4 if pos in ("KEY_FWD", "KEY_DEF", "RUC") else 3
            fire = quals > 0 and tenure >= onset and quals <= 1
            cur = [x for x in p.get("scoring", []) if x.get("year") == 2026]
            current_games = sum(float(x.get("games", 0) or 0) for x in cur)
            current_avg = next((x.get("avg") for x in cur if x.get("games", 0) > 0), None)
            if fire:
                fire_keys.add(key)
                grade_now = float(stale_grade(p, 2026, pos))
                old_lens = g.get("_LENS_FORM")
                g["_LENS_FORM"] = 2026
                try:
                    anchor_p1, anchor_p2 = int(fa_year(2027)), int(fa_year(2028))
                    grade_p1 = float(stale_grade(p, anchor_p1, pos))
                    grade_p2 = float(stale_grade(p, anchor_p2, pos))
                finally:
                    g["_LENS_FORM"] = old_lens
                if current_games == 0:
                    zero_live.add(key)

        def iv(row, field):
            x = row.get(field)
            return None if x is None else int(x)
        bv, av = iv(b, "v"), iv(c, "v")
        b1, a1, b2, a2 = iv(b, "vP1"), iv(c, "vP1"), iv(b, "vP2"), iv(c, "vP2")
        output.append({
            "key": key, "name": c.get("name") or b.get("name"), "position": pos,
            "afl_club": c.get("club") or b.get("club"), "affl_team": (p or {}).get("affl_team"),
            "before": bv, "after": av, "delta": av-bv,
            "before_rank": ranks[("before", "v")][key], "after_rank": ranks[("after", "v")][key],
            "before_plus1": b1, "after_plus1": a1, "delta_plus1": None if b1 is None or a1 is None else a1-b1,
            "before_plus2": b2, "after_plus2": a2, "delta_plus2": None if b2 is None or a2 is None else a2-b2,
            "after_plus1_minus_present": None if a1 is None else a1-av,
            "after_plus2_minus_plus1": None if a1 is None or a2 is None else a2-a1,
            "stalled_fire_population": fire,
            "grade_now": None if grade_now is None else round(grade_now, 5),
            "forward_anchor_year_plus1": anchor_p1, "forward_anchor_year_plus2": anchor_p2,
            "grade_plus1": None if grade_p1 is None else round(grade_p1, 5),
            "grade_plus2": None if grade_p2 is None else round(grade_p2, 5),
            "current_games": current_games, "current_average": current_avg,
            "tenure": tenure, "qualifying_seasons": quals, "cap_onset": onset,
        })

    changed = [r for r in output if r["delta"] or (r["delta_plus1"] or 0) or (r["delta_plus2"] or 0)]
    present_changed = [r for r in output if r["delta"]]
    changed_keys = {r["key"] for r in present_changed}
    assert all(r["delta"] >= 0 for r in output)
    assert changed_keys <= fire_keys, sorted(changed_keys-fire_keys)
    assert not (changed_keys & zero_live), sorted(changed_keys & zero_live)
    fire = [r for r in output if r["stalled_fire_population"]]
    assert all(r["forward_anchor_year_plus1"] == 2026 and r["forward_anchor_year_plus2"] == 2026 for r in fire)
    assert all(r["grade_plus1"] == r["grade_now"] == r["grade_plus2"] for r in fire)
    goth = next(r for r in output if r["key"] == "phoenix-gothard")
    assert goth["before"] == 410 and goth["after"] > 410 and goth["grade_now"] == 1.0

    cols = list(output[0])
    for filename, data in (("before_after_all.csv", output), ("before_after_changed.csv", changed)):
        with (out / filename).open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(data)

    summary = {
        "kind": "graded_staleness_anchor_fix_r19_candidate", "status": "PASS",
        "baseline_board_md5": md5(bp), "candidate_board_md5": md5(cp),
        "candidate_engine_md5": md5(ws / "_merged_recover.py"), "store_md5": md5(ws / "rl_model_data.json"),
        "active_players": len(output), "fire_population": len(fire),
        "present_changed_players": len(present_changed), "any_lens_changed_players": len(changed),
        "forward_grade_anchor_year": 2026, "forward_grade_matches_present_for_all_fire_players": True,
        "present_above_plus1_among_present_movers": sum(1 for r in present_changed if r["after"] > r["after_plus1"]),
        "plus1_equals_plus2_among_present_movers": sum(1 for r in present_changed if r["after_plus1"] == r["after_plus2"]),
        "present_total_delta": sum(r["delta"] for r in output),
        "plus1_total_delta": sum(r["delta_plus1"] or 0 for r in output),
        "plus2_total_delta": sum(r["delta_plus2"] or 0 for r in output),
        "phoenix_gothard": goth,
        "changed_players": sorted(changed, key=lambda r: (-max(r["delta"], r["delta_plus1"] or 0, r["delta_plus2"] or 0), r["key"])),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    (out / "candidate_board.json").write_bytes(cp.read_bytes())
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
