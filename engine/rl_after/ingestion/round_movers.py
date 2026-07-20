"""ROUND MOVERS — per-round movement report + integrated HTML-engine movers data (post-commit).

After a round is COMMITTED, this module derives — from the persistent value / overall-rank /
positional-rank histories — each active player's movement vs the immediately preceding recorded round:

  * dRound        = value(round) - value(round-1)
  * dRoundRank    = rank(round-1) - rank(round)          (positive == moved UP the overall ladder)
  * dRoundPosRank = pos_rank(round-1) - pos_rank(round)  (positive == moved UP within the position)

It writes two artifacts per round (both post-commit, re-derivable, OUTSIDE the store transaction):

  1. movers_R<N>.json — the authoritative movers report, keyed by STABLE player key (exact; the two
     Bailey Williams never collide here).
  2. the Matchday WORKING UI bundle, augmented in place with `dRound` / `dRoundRank` /
     `dRoundPosRank` on each player row — the "integrated HTML-engine movers data" the owner's HTML
     board renders (the working bundle carries identity keys, so the injection is exact).

NO valuation, NO store write. Reads finished histories + the committed working bundle and writes JSON.
"""
import json
import os

try:
    from . import round_history as RH
except (ImportError, ValueError):
    import round_history as RH  # type: ignore


def _by_round(hist, key, rnd):
    return (hist.get('players', {}).get(key, {}).get('by_round', {}) or {}).get(str(int(rnd)))


def movers_from_histories(vh, rh, ph, round_n):
    """Build the movers report for `round_n` from the three committed histories."""
    round_n = int(round_n)
    prev = round_n - 1
    players = []
    for key, entry in (vh.get('players') or {}).items():
        v_now, v_prev = _by_round(vh, key, round_n), _by_round(vh, key, prev)
        r_now, r_prev = _by_round(rh, key, round_n), _by_round(rh, key, prev)
        p_now, p_prev = _by_round(ph, key, round_n), _by_round(ph, key, prev)
        dv = (v_now - v_prev) if (v_now is not None and v_prev is not None) else None
        dr = (r_prev - r_now) if (r_now is not None and r_prev is not None) else None
        dp = (p_prev - p_now) if (p_now is not None and p_prev is not None) else None
        players.append({'key': key, 'name': entry.get('name'),
                        'stable_player_id': entry.get('stable_player_id'),
                        'v': v_now, 'rank': r_now, 'pos_rank': p_now,
                        'dRound': dv, 'dRoundRank': dr, 'dRoundPosRank': dp})
    movers = [p for p in players if p['dRound'] is not None]
    by_v = sorted(movers, key=lambda p: p['dRound'])
    by_r = sorted((p for p in movers if p['dRoundRank'] is not None), key=lambda p: p['dRoundRank'])
    return {
        'kind': 'weekly_movers_report', 'round': round_n, 'prev_round': prev,
        'players_total': len(players), 'players_compared': len(movers),
        'top_value_gain': list(reversed(by_v[-10:])), 'top_value_loss': by_v[:10],
        'top_rank_gain': list(reversed(by_r[-10:])), 'top_rank_loss': by_r[:10],
        'by_key': {p['key']: {'dRound': p['dRound'], 'dRoundRank': p['dRoundRank'],
                              'dRoundPosRank': p['dRoundPosRank']} for p in players},
    }


def _load(path):
    with open(path) as f:
        return json.load(f)


def emit(repo_root, round_n, *, movers_dir=None, ui_working=None):
    """Post-commit: write movers_R<N>.json and inject movers into the working UI bundle. Returns an
    evidence dict. `repo_root` locates the committed histories + default artifact paths."""
    ing = os.path.join(repo_root, 'engine', 'rl_after', 'ingestion')
    vh = _load(os.path.join(ing, 'value_history.json'))
    rh = _load(os.path.join(ing, 'rank_history.json'))
    ph = _load(os.path.join(ing, 'pos_rank_history.json'))
    report = movers_from_histories(vh, rh, ph, round_n)

    movers_dir = movers_dir or os.path.join(ing, 'movers')
    os.makedirs(movers_dir, exist_ok=True)
    report_path = os.path.join(movers_dir, 'movers_R%d.json' % int(round_n))
    RH.save_json_atomic(report_path, RH.report_bytes(report))

    ui_working = ui_working or os.path.join(repo_root, 'ui', 'data', 'board_view_working.js')
    injected = 0
    ui_working_out = None
    if os.path.exists(ui_working):
        injected, ui_working_out = _inject_working(ui_working, report['by_key'])
    return {'round': int(round_n), 'movers_report': report_path,
            'players_total': report['players_total'], 'players_compared': report['players_compared'],
            'ui_working_bundle': ui_working_out, 'ui_rows_injected': injected}


def _inject_working(path, by_key):
    """Augment each player row of a `window.__MATCHDAY_WORKING__ = {...}` bundle with dRound /
    dRoundRank / dRoundPosRank (matched by the row's identity key). Re-emits in the extractor's own
    format. Returns (rows_injected, path)."""
    with open(path) as f:
        text = f.read()
    i, j = text.index('{'), text.rindex('}')
    prefix, obj, suffix = text[:i], json.loads(text[i:j + 1]), text[j + 1:]
    injected = 0
    for row in obj.get('players', []):
        mv = by_key.get(row.get('key'))
        if mv:
            row['dRound'] = mv['dRound']
            row['dRoundRank'] = mv['dRoundRank']
            row['dRoundPosRank'] = mv['dRoundPosRank']
            injected += 1
    with open(path, 'w') as f:
        f.write(prefix)
        json.dump(obj, f, ensure_ascii=False, separators=(',', ':'))
        f.write(suffix)
    return injected, path
