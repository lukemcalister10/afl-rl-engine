#!/usr/bin/env python3
"""Build the complete owner-facing before/after report for the graded-staleness candidate."""
from __future__ import annotations

import argparse
import contextlib
import csv
import hashlib
import html
import io
import json
import os
import sys
from pathlib import Path


def md5(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def load_engine(workspace: Path):
    old_cwd = Path.cwd()
    vendor = Path("/home/claude/rl_vendor")
    for path in (workspace, vendor):
        if path.exists() and str(path) not in sys.path:
            sys.path.insert(0, str(path))
    env = {"__name__": "staleness_candidate_diagnostic"}
    try:
        os.chdir(workspace)
        with contextlib.redirect_stdout(io.StringIO()):
            source = (workspace / "_merged_recover.py").read_text(encoding="utf-8")
            exec(source.split('print("=== AFTER')[0], env)
    finally:
        os.chdir(old_cwd)
    return env


def board_rows(path: Path):
    board = json.loads(path.read_text(encoding="utf-8"))
    rows = board["active"] if isinstance(board, dict) else board
    return board, rows


def rank_map(rows, value_field="v"):
    """Canonical total-order law: descending value, ties by stable key."""
    ordered = sorted((p for p in rows if p.get("key")),
                     key=lambda p: (-(float(p.get(value_field) or 0.0)), p["key"]))
    return {p["key"]: i for i, p in enumerate(ordered, 1)}


def delta(a, b):
    if a is None or b is None:
        return None
    return int(b) - int(a)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--workspace", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    baseline_path = Path(args.baseline).resolve()
    candidate_path = Path(args.candidate).resolve()
    workspace = Path(args.workspace).resolve()
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)

    baseline_obj, baseline = board_rows(baseline_path)
    candidate_obj, candidate = board_rows(candidate_path)
    bmap = {p["key"]: p for p in baseline if p.get("key")}
    cmap = {p["key"]: p for p in candidate if p.get("key")}
    assert len(bmap) == len(cmap) == 804
    assert set(bmap) == set(cmap)

    brank = rank_map(baseline, "v")
    crank = rank_map(candidate, "v")
    brank1, crank1 = rank_map(baseline, "vP1"), rank_map(candidate, "vP1")
    brank2, crank2 = rank_map(baseline, "vP2"), rank_map(candidate, "vP2")
    assert brank["phoenix-gothard"] == 415, brank["phoenix-gothard"]

    g = load_engine(workspace)
    MA, PR = g["MA"], g["PR"]
    nseas_pro = g["nseas_pro"]
    stale_grade = g["_staleness_grade"]
    form_clock, fa_year = g["_form_anchor_clock"], g["_fa_year"]
    isreal = g["_isreal"]

    store_by_key = {p.get("key"): p for p in MA.data if p.get("key") and not p.get("_retired")}
    rows = []
    fire_keys = set()
    zero_live_fire = set()
    for key in sorted(bmap):
        before, after = bmap[key], cmap[key]
        p = store_by_key.get(key)
        fire = False
        grade = None
        current_qual = None
        current_games = None
        current_avg = None
        tenure = None
        qualifying_seasons = None
        onset = None
        if p is not None and isreal(p):
            Y = 2026
            pos = MA.gfut(p)
            with form_clock():
                tenure = int(PR.tenure(p, fa_year(Y)))
            qualifying_seasons = int(nseas_pro(p, Y))
            keyruc = pos in ("KEY_FWD", "KEY_DEF", "RUC")
            onset = 4 if keyruc else 3
            fire = qualifying_seasons > 0 and tenure >= onset and qualifying_seasons <= 1
            current = [x for x in p.get("scoring", []) if x.get("year") == Y]
            current_games = sum(float(x.get("games", 0)) for x in current)
            current_avg = next((x.get("avg") for x in current if x.get("games", 0) > 0), None)
            if fire:
                fire_keys.add(key)
                grade = float(stale_grade(p, Y, pos))
                current_qual = grade == 1.0
                if current_games == 0:
                    zero_live_fire.add(key)

        before_v, after_v = int(before.get("v", 0)), int(after.get("v", 0))
        before_p1, after_p1 = before.get("vP1"), after.get("vP1")
        before_p2, after_p2 = before.get("vP2"), after.get("vP2")
        row = {
            "key": key,
            "name": after.get("name") or before.get("name") or (p or {}).get("player"),
            "afl_club": after.get("club") or before.get("club") or (p or {}).get("afl_club"),
            "affl_team": (p or {}).get("affl_team"),
            "position": after.get("grp") or after.get("gf") or before.get("grp") or before.get("gf"),
            "before": before_v,
            "after": after_v,
            "delta": after_v - before_v,
            "before_rank": brank[key],
            "after_rank": crank[key],
            "rank_change": brank[key] - crank[key],
            "before_plus1": before_p1,
            "after_plus1": after_p1,
            "delta_plus1": delta(before_p1, after_p1),
            "before_plus1_rank": brank1[key],
            "after_plus1_rank": crank1[key],
            "plus1_rank_change": brank1[key] - crank1[key],
            "before_plus2": before_p2,
            "after_plus2": after_p2,
            "delta_plus2": delta(before_p2, after_p2),
            "before_plus2_rank": brank2[key],
            "after_plus2_rank": crank2[key],
            "plus2_rank_change": brank2[key] - crank2[key],
            "stalled_fire_population": fire,
            "staleness_grade": None if grade is None else round(grade, 5),
            "current_season_qualifies": current_qual,
            "current_games": current_games,
            "current_average": current_avg,
            "tenure": tenure,
            "qualifying_seasons": qualifying_seasons,
            "cap_onset": onset,
        }
        rows.append(row)

    present_changed = [r for r in rows if r["delta"] != 0]
    plus1_changed = [r for r in rows if r["delta_plus1"] not in (None, 0)]
    plus2_changed = [r for r in rows if r["delta_plus2"] not in (None, 0)]
    any_changed = [r for r in rows if r["delta"] != 0 or r["delta_plus1"] not in (None, 0)
                   or r["delta_plus2"] not in (None, 0)]
    present_changed.sort(key=lambda r: (-r["delta"], r["key"]))
    plus1_changed.sort(key=lambda r: (-r["delta_plus1"], r["key"]))
    plus2_changed.sort(key=lambda r: (-r["delta_plus2"], r["key"]))
    any_changed.sort(key=lambda r: (-max(r["delta"], r["delta_plus1"] or 0, r["delta_plus2"] or 0), r["key"]))
    changed_keys = {r["key"] for r in present_changed}

    # Predeclared PRESENT-mechanism gates. The candidate is a release from a cap, so it may never lower a
    # present value; present changes must be entirely inside the current stalled fire population; and genuine
    # zero-live-output ghosts remain unchanged. Forward-lens effects are measured and disclosed rather than
    # presumed absent: the original D8 prototype explicitly records forward-year re-cap as a known interaction.
    assert all(r["delta"] >= 0 for r in rows), "graded release lowered at least one present value"
    assert changed_keys <= fire_keys, sorted(changed_keys - fire_keys)[:20]
    assert not (changed_keys & zero_live_fire), sorted(changed_keys & zero_live_fire)[:20]
    goth = next(r for r in rows if r["key"] == "phoenix-gothard")
    assert goth["before"] == 410
    assert goth["after"] > goth["before"]
    assert goth["stalled_fire_population"] and goth["current_season_qualifies"]
    assert goth["staleness_grade"] == 1.0

    columns = list(rows[0])
    outputs = (
        ("before_after_all.csv", rows),
        ("before_after_present_changed.csv", present_changed),
        ("before_after_plus1_changed.csv", plus1_changed),
        ("before_after_plus2_changed.csv", plus2_changed),
        ("before_after_any_changed.csv", any_changed),
    )
    for name, data in outputs:
        with (out / name).open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=columns)
            w.writeheader(); w.writerows(data)

    summary = {
        "kind": "graded_staleness_r19_candidate",
        "status": "PASS",
        "baseline_board_md5": md5(baseline_path),
        "candidate_board_md5": md5(candidate_path),
        "candidate_engine_md5": md5(workspace / "_merged_recover.py"),
        "store_md5": md5(workspace / "rl_model_data.json"),
        "active_players": len(rows),
        "stalled_fire_population": len(fire_keys),
        "present_changed_players": len(present_changed),
        "present_unchanged_players": len(rows) - len(present_changed),
        "plus1_changed_players": len(plus1_changed),
        "plus2_changed_players": len(plus2_changed),
        "any_lens_changed_players": len(any_changed),
        "zero_live_fire_unchanged": len(zero_live_fire),
        "present_value_total_before": sum(r["before"] for r in rows),
        "present_value_total_after": sum(r["after"] for r in rows),
        "present_value_total_delta": sum(r["delta"] for r in rows),
        "plus1_total_delta": sum(r["delta_plus1"] or 0 for r in rows),
        "plus2_total_delta": sum(r["delta_plus2"] or 0 for r in rows),
        "plus1_negative_movers": sum(1 for r in rows if (r["delta_plus1"] or 0) < 0),
        "plus2_negative_movers": sum(1 for r in rows if (r["delta_plus2"] or 0) < 0),
        "all_present_changes_nonnegative": True,
        "all_present_value_changes_inside_fire_population": True,
        "forward_lens_effects_measured_not_suppressed": True,
        "phoenix_gothard": goth,
        "largest_present_changes": present_changed[:25],
        "largest_plus1_changes": plus1_changed[:25],
        "largest_plus2_changes": plus2_changed[:25],
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    (out / "candidate_board.json").write_bytes(candidate_path.read_bytes())

    table_rows = "\n".join(
        "<tr>" + "".join(f"<td>{html.escape(str(r.get(c, '')))}</td>" for c in
        ("name", "before", "after", "delta", "before_rank", "after_rank", "rank_change",
         "before_plus1", "after_plus1", "delta_plus1", "before_plus2", "after_plus2", "delta_plus2",
         "staleness_grade", "current_games", "current_average", "position", "afl_club", "affl_team")) + "</tr>"
        for r in any_changed
    )
    headers = ['Player','Before','After','Delta','Old rank','New rank','Rank Δ','+1 before','+1 after','+1 Δ',
               '+2 before','+2 after','+2 Δ','Grade','Games','Average','Position','AFL','AFFL']
    review = f"""<!doctype html><meta charset='utf-8'><title>R19 graded staleness candidate</title>
<style>body{{font:14px Arial;margin:24px;background:#0a0c10;color:#f2f5f9}}.wrap{{overflow:auto}}table{{border-collapse:collapse;width:100%}}th,td{{padding:7px 9px;border-bottom:1px solid #303643;text-align:right;white-space:nowrap}}th:first-child,td:first-child{{text-align:left}}th{{position:sticky;top:0;background:#181c25;color:#c8f04a}}.meta{{margin-bottom:20px;line-height:1.6}}</style>
<h1>Round 19 graded-staleness candidate</h1><div class='meta'>Baseline <code>{summary['baseline_board_md5']}</code> → candidate <code>{summary['candidate_board_md5']}</code><br>
Present changes: <b>{len(present_changed)}</b> / 804 · present total Δ <b>+{summary['present_value_total_delta']}</b><br>
Forward changes: +1 year <b>{len(plus1_changed)}</b>, +2 years <b>{len(plus2_changed)}</b><br>
Phoenix Gothard: present <b>{goth['before']} → {goth['after']} ({goth['delta']:+d})</b>; +1 <b>{goth['before_plus1']} → {goth['after_plus1']}</b>; +2 <b>{goth['before_plus2']} → {goth['after_plus2']}</b></div>
<div class='wrap'><table><thead><tr>{''.join('<th>'+x+'</th>' for x in headers)}</tr></thead><tbody>{table_rows}</tbody></table></div>"""
    (out / "before_after_review.html").write_text(review, encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
