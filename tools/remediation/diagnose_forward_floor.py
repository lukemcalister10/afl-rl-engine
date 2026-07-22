#!/usr/bin/env python3
"""Classify raw forward values versus the sealed Leg-F3 pedigree floor.

This is read-only evidence. It reproduces rl_export's raw ev(p, 2027/2028), numeraire conversion,
and final max(raw, phi(current career games) * present) operation. It identifies whether exact +1/+2
equalities arise from the shared sealed floor or from the underlying engine projection.
"""
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


def load_engine(workspace: Path):
    old = Path.cwd()
    for p in (workspace, Path('/home/claude/rl_vendor')):
        if p.exists() and str(p) not in sys.path:
            sys.path.insert(0, str(p))
    env = {'__name__': 'forward_floor_diagnostic'}
    try:
        os.chdir(workspace)
        with contextlib.redirect_stdout(io.StringIO()):
            src = (workspace / '_merged_recover.py').read_text(encoding='utf-8')
            exec(src.split('print("=== AFTER')[0], env)
    finally:
        os.chdir(old)
    return env


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--workspace', required=True)
    ap.add_argument('--board', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    ws, board_path, out = map(lambda x: Path(x).resolve(), (args.workspace, args.board, args.out))
    out.mkdir(parents=True, exist_ok=True)

    board_obj = json.loads(board_path.read_text(encoding='utf-8'))
    board_rows = board_obj['active'] if isinstance(board_obj, dict) else board_obj
    board = {p['key']: p for p in board_rows if p.get('key')}
    assert len(board) == 804

    env = load_engine(ws)
    MA, ev = env['MA'], env['ev']
    g = MA.__dict__
    players = [p for p in env['MA'].data if p.get('key') in board and not p.get('_retired')]
    # Board players may include synthesized rows; use the exact engine `players` list when available.
    engine_players = {p['key']: p for p in env.get('players', players) if p.get('key') in board}
    assert len(engine_players) == 804, len(engine_players)
    factor = json.loads((ws / 'pick_redenomination.json').read_text(encoding='utf-8'))['factor']
    nb = lambda x: int(round(float(x) / factor))

    rows = []
    with contextlib.redirect_stdout(io.StringIO()):
        for key in sorted(board):
            p = engine_players[key]
            MA.BASE_REF = MA.AGE_REF = 2026
            MA._LENS_FORM = None
            MA._pe_clear()
            present = nb(ev(p, 2026))

            MA._LENS_FORM = 2026
            raw_p1 = nb(ev(p, 2027))
            raw_p2 = nb(ev(p, 2028))
            MA._LENS_FORM = None
            MA.BASE_REF = MA.AGE_REF = 2026
            MA._pe_clear()

            games = p.get('games')
            if games is None:
                games = sum(int(x.get('games', 0) or 0) for x in (p.get('scoring') or []))
            games = float(games)
            floor = int(round(((1.0 - games / 46.0) ** 2) * present)) if games < 46 else None
            final_p1 = max(raw_p1, floor) if floor is not None else raw_p1
            final_p2 = max(raw_p2, floor) if floor is not None else raw_p2
            br = board[key]
            assert present == int(br['v']), (key, present, br['v'])
            assert final_p1 == int(br['vP1']), (key, raw_p1, floor, final_p1, br['vP1'])
            assert final_p2 == int(br['vP2']), (key, raw_p2, floor, final_p2, br['vP2'])

            bind1 = floor is not None and raw_p1 < floor
            bind2 = floor is not None and raw_p2 < floor
            rows.append({
                'key': key, 'name': br.get('name'), 'age': br.get('age'), 'position': br.get('grp') or br.get('gf'),
                'career_games_used_by_floor': games, 'present': present,
                'raw_plus1': raw_p1, 'raw_plus2': raw_p2, 'sealed_floor_both_horizons': floor,
                'floor_binds_plus1': bind1, 'floor_binds_plus2': bind2,
                'final_plus1': final_p1, 'final_plus2': final_p2,
                'final_equal': final_p1 == final_p2,
                'equal_because_shared_floor': final_p1 == final_p2 and bind1 and bind2,
                'raw_equal': raw_p1 == raw_p2,
                'plus1_minus_present': final_p1 - present,
                'plus2_minus_plus1': final_p2 - final_p1,
            })

    columns = list(rows[0])
    with (out / 'forward_floor_all.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=columns); w.writeheader(); w.writerows(rows)
    equal = [r for r in rows if r['final_equal']]
    shared = [r for r in rows if r['equal_because_shared_floor']]
    bind = [r for r in rows if r['floor_binds_plus1'] or r['floor_binds_plus2']]
    for filename, data in (('forward_floor_equal.csv', equal), ('forward_floor_binding.csv', bind)):
        with (out / filename).open('w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=columns); w.writeheader(); w.writerows(data)

    watch_keys = ['phoenix-gothard','jai-serong','billy-wilson','max-heath','cooper-lord','oscar-steene',
                  'james-leake','will-mclachlan']
    summary = {
        'kind': 'forward_floor_diagnostic', 'status': 'PASS',
        'board_md5': md5(board_path), 'engine_md5': md5(ws / '_merged_recover.py'),
        'active_players': len(rows),
        'floor_binds_plus1': sum(r['floor_binds_plus1'] for r in rows),
        'floor_binds_plus2': sum(r['floor_binds_plus2'] for r in rows),
        'floor_binds_either': len(bind),
        'final_plus1_equals_plus2': len(equal),
        'equal_because_shared_floor': len(shared),
        'equal_raw_projection': sum(r['raw_equal'] for r in rows),
        'watch_rows': [r for r in rows if r['key'] in watch_keys],
    }
    (out / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
