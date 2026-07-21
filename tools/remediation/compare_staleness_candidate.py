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


def rank_map(rows):
    """Canonical weekly rank law: descending v, ties by stable key."""
    ordered = sorted((p for p in rows if p.get("key")),
                     key=lambda p: (-(float(p.get("v") or 0.0)), p["key"]))
    return {p["key"]: i for i, p in enumerate(ordered, 1)}


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

    brank = rank_map(baseline)
    crank = rank_map(candidate)
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

        dv = int(after.get("v", 0)) - int(before.get("v", 0))
        row = {
            "key": key,
            "name": after.get("name") or before.get("name") or (p or {}).get("player"),
            "afl_club": after.get("club") or before.get("club") or (p or {}).get("afl_club"),
            "affl_team": (p or {}).get("affl_team"),
            "position": after.get("grp") or after.get("gf") or before.get("grp") or before.get("gf"),
            "before": int(before.get("v", 0)),
            "after": int(after.get("v", 0)),
            "delta": dv,
            "before_rank": brank[key],
            "after_rank": crank[key],
            "rank_change": brank[key] - crank[key],
            "before_plus1": before.get("vP1"),
            "after_plus1": after.get("vP1"),
            "before_plus2": before.get("vP2"),
            "after_plus2": after.get("vP2"),
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

    changed = [r for r in rows if r["delta"] != 0]
    changed.sort(key=lambda r: (-r["delta"], r["key"]))
    changed_keys = {r["key"] for r in changed}

    # Predeclared mechanism gates. The candidate is a release from a cap, so it may never lower a present value.
    assert all(r["delta"] >= 0 for r in rows), "graded release lowered at least one present value"
    assert changed_keys <= fire_keys, sorted(changed_keys - fire_keys)[:20]
    assert not (changed_keys & zero_live_fire), sorted(changed_keys & zero_live_fire)[:20]
    # The historical design's documented forward-year limitation is preserved: no vP1/vP2 repricing here.
    assert all(r["before_plus1"] == r["after_plus1"] and r["before_plus2"] == r["after_plus2"] for r in rows)
    goth = next(r for r in rows if r["key"] == "phoenix-gothard")
    assert goth["before"] == 410
    assert goth["after"] > goth["before"]
    assert goth["stalled_fire_population"] and goth["current_season_qualifies"]
    assert goth["staleness_grade"] == 1.0

    columns = list(rows[0])
    for name, data in (("before_after_all.csv", rows), ("before_after_changed.csv", changed)):
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
        "changed_players": len(changed),
        "unchanged_players": len(rows) - len(changed),
        "zero_live_fire_unchanged": len(zero_live_fire),
        "present_value_total_before": sum(r["before"] for r in rows),
        "present_value_total_after": sum(r["after"] for r in rows),
        "present_value_total_delta": sum(r["delta"] for r in rows),
        "all_changes_nonnegative": True,
        "all_value_changes_inside_fire_population": True,
        "future_player_values_unchanged": True,
        "phoenix_gothard": goth,
        "largest_changes": changed[:25],
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    (out / "candidate_board.json").write_bytes(candidate_path.read_bytes())

    table_rows = "\n".join(
        "<tr>" + "".join(f"<td>{html.escape(str(r.get(c, '')))}</td>" for c in
        ("name", "before", "after", "delta", "before_rank", "after_rank", "rank_change",
         "staleness_grade", "current_games", "current_average", "position", "afl_club", "affl_team")) + "</tr>"
        for r in changed
    )
    review = f"""<!doctype html><meta charset='utf-8'><title>R19 graded staleness candidate</title>
<style>body{{font:14px Arial;margin:24px;background:#0a0c10;color:#f2f5f9}}table{{border-collapse:collapse;width:100%}}th,td{{padding:7px 9px;border-bottom:1px solid #303643;text-align:right}}th:first-child,td:first-child{{text-align:left}}th{{position:sticky;top:0;background:#181c25;color:#c8f04a}}.meta{{margin-bottom:20px;line-height:1.6}}</style>
<h1>Round 19 graded-staleness candidate</h1><div class='meta'>Baseline <code>{summary['baseline_board_md5']}</code> → candidate <code>{summary['candidate_board_md5']}</code><br>
Changed players: <b>{len(changed)}</b> / 804 · total value Δ <b>+{summary['present_value_total_delta']}</b><br>
Phoenix Gothard: <b>{goth['before']} → {goth['after']} ({goth['delta']:+d})</b></div>
<table><thead><tr>{''.join('<th>'+x+'</th>' for x in ['Player','Before','After','Delta','Old rank','New rank','Rank Δ','Grade','Games','Average','Position','AFL','AFFL'])}</tr></thead><tbody>{table_rows}</tbody></table>"""
    (out / "before_after_review.html").write_text(review, encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
