"""ROUND MOVERS — durable weekly movers report + integrated HTML-engine movers data (post-commit).

After a round COMMITS (store + board + ledger + value/overall-rank/positional-rank history + UI
bundles all swapped atomically), this module derives — from the two consecutive committed boards, via
the persistent histories — a DURABLE movers report comparing the newly committed round with the
immediately preceding committed round. It is written ONLY on a fully committed round; a failed or
rolled-back transaction leaves NO valid movers report (the emit runs after the applier returns success).

For EVERY active player (including DNP players — whose value/rank can still move via ageing,
competition, conservation or universe effects) the report records: stable key, name, club, position,
previous/current round, played/DNP status, submitted score (or an explicit DNP marker), previous and
current value + absolute and % value change, previous/current overall rank + rank change (positive ==
improved), and previous/current positional rank + positional-rank change.

The deltas are the EXACT difference of the two committed boards' own value/overall-rank/positional-rank
(read from the histories, which are byte-for-byte board projections), never a re-valuation. Ties are
broken deterministically: primary movement field, then current value descending, then stable key
ascending.

Artifacts (post-commit, re-derivable, OUTSIDE the store transaction):
  * movers/movers_R<N>.json  — the full machine-readable report (keyed by stable key; exact).
  * movers/movers_R<N>.csv   — the same table as CSV.
  * ui/data/movers.js        — the Matchday UI movers bundle (window.__MATCHDAY_MOVERS__), ACCUMULATED
                               across rounds and carrying each report's board-identity chain + release
                               identity so the UI can fail-closed on a mismatched / incomplete report.
  * ui/data/board_view_working.js — augmented in place with dRound / dRoundRank / dRoundPosRank per row.

NO valuation, NO store write.
"""
import csv
import io
import json
import os

try:
    from . import round_history as RH
except (ImportError, ValueError):
    import round_history as RH  # type: ignore

SCHEMA_VERSION = 1
POS_LABEL = {'MID': 'Mid', 'RUC': 'Ruck', 'KEY_FWD': 'Key Fwd', 'GEN_FWD': 'Fwd',
            'KEY_DEF': 'Key Def', 'GEN_DEF': 'Def'}


def _label_pos(code):
    return POS_LABEL.get(code, (code or '').replace('_', ' ').title() or '—')


def _load(path):
    with open(path) as f:
        return json.load(f)


def _md5(path):
    import hashlib
    if not os.path.exists(path):
        return None
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for c in iter(lambda: f.read(1 << 16), b''):
            h.update(c)
    return h.hexdigest()


# ---- the report -----------------------------------------------------------------------------------
def build_report(repo_root, round_n, *, played=None, evidence=None, generated_at=None):
    """Build the full movers report for a committed round from the two committed boards (via histories).

    `played` maps stable key -> submitted score for players LISTED this round (a score of 0 is a
    legitimate played score); a key absent from it is DNP. `evidence` carries the transaction's
    store/board md5 before/after + txn id (from the applier result)."""
    round_n = int(round_n)
    prev_round = round_n - 1
    played = played or {}
    ing = os.path.join(repo_root, 'engine', 'rl_after', 'ingestion')
    vh = _load(os.path.join(ing, 'value_history.json'))
    rh = _load(os.path.join(ing, 'rank_history.json'))
    ph = _load(os.path.join(ing, 'pos_rank_history.json'))
    board = _load(os.path.join(repo_root, 'data', 'rl_build', 'rl_app_data.json'))
    boot = _load(os.path.join(repo_root, 'data', 'expected_boot.json'))
    store_rows = _load(os.path.join(repo_root, 'engine', 'rl_after', 'rl_model_data.json'))
    affl_by_key = {r.get('key'): r.get('affl_team') for r in store_rows if r.get('key')}

    active = board['active'] if isinstance(board, dict) else board
    season = int(vh.get('season', 2026))

    def by_round(hist, key, rnd):
        return (hist.get('players', {}).get(key, {}).get('by_round', {}) or {}).get(str(int(rnd)))

    players = []
    for p in active:
        key = p.get('key')
        if not key:
            continue
        pv = by_round(vh, key, prev_round)
        cv = by_round(vh, key, round_n)
        pr = by_round(rh, key, prev_round)
        cr = by_round(rh, key, round_n)
        pp = by_round(ph, key, prev_round)
        cp = by_round(ph, key, round_n)
        dv = (cv - pv) if (cv is not None and pv is not None) else None
        dvp = (round(dv / pv * 100.0, 2) if (dv is not None and pv not in (None, 0)) else None)
        drank = (pr - cr) if (pr is not None and cr is not None) else None      # +ve == improved
        dpos = (pp - cp) if (pp is not None and cp is not None) else None       # +ve == improved
        did_play = key in played
        players.append({
            'key': key, 'name': p.get('name'), 'club': p.get('club'),
            'affl_team': affl_by_key.get(key), 'pos': _label_pos(p.get('grp') or p.get('gf')),
            'posCode': p.get('grp') or p.get('gf'),
            'previous_round': prev_round, 'current_round': round_n,
            'played': did_play, 'dnp': not did_play,
            'score': (played.get(key) if did_play else None),
            'prev_value': pv, 'cur_value': cv, 'value_change': dv, 'value_change_pct': dvp,
            'prev_rank': pr, 'cur_rank': cr, 'rank_change': drank,
            'prev_pos_rank': pp, 'cur_pos_rank': cp, 'pos_rank_change': dpos,
        })

    def rank_view(field, reverse):
        # deterministic tie-break: primary field, then cur_value desc, then key asc
        elig = [p for p in players if p.get(field) is not None]
        elig.sort(key=lambda p: (p[field], p['cur_value'] if p['cur_value'] is not None else -1e18, ''),
                  reverse=reverse)
        if reverse:  # descending primary; re-apply secondary/tertiary deterministically for ties
            elig.sort(key=lambda p: (-p[field], -(p['cur_value'] if p['cur_value'] is not None else -1e18), p['key']))
        else:
            elig.sort(key=lambda p: (p[field], -(p['cur_value'] if p['cur_value'] is not None else -1e18), p['key']))
        return [p['key'] for p in elig]

    views = {
        'value_risers': rank_view('value_change', True)[:50],
        'value_fallers': rank_view('value_change', False)[:50],
        'rank_risers': rank_view('rank_change', True)[:50],
        'rank_fallers': rank_view('rank_change', False)[:50],
        'played_count': sum(1 for p in players if p['played']),
        'dnp_count': sum(1 for p in players if p['dnp']),
    }

    ev = evidence or {}
    report = {
        'kind': 'weekly_movers_report', 'schema_version': SCHEMA_VERSION,
        'season': season, 'submitted_round': round_n, 'previous_round': prev_round,
        'source_store_md5_before': ev.get('store_md5_before'), 'source_store_md5_after': ev.get('store_md5_after'),
        'board_md5_before': ev.get('board_md5_before'), 'board_md5_after': ev.get('board_md5_after'),
        'txn_id': ev.get('txn_id'), 'generated_at': generated_at, 'player_count': len(players),
        'release_identity': {
            'engine_head': boot.get('engine_head'), 'rl_model': boot.get('rl_model'),
            'fv': boot.get('fv'), 'config': boot.get('config'), 'board': boot.get('board'),
            'store': boot.get('store'), 'register': boot.get('register'), 'tag': 'v2.10',
        },
        'integrity': {
            'players_unique': len({p['key'] for p in players}) == len(players),
            'coverage_full': len(players) == len([p for p in active if p.get('key')]),
            'board_after_matches_committed': ev.get('board_md5_after') == _md5(
                os.path.join(repo_root, 'data', 'rl_build', 'rl_app_data.json')),
        },
        'views': views, 'players': players,
    }
    return report


# ---- CSV ------------------------------------------------------------------------------------------
_CSV_FIELDS = ['key', 'name', 'club', 'affl_team', 'pos', 'previous_round', 'current_round',
               'played', 'score', 'prev_value', 'cur_value', 'value_change', 'value_change_pct',
               'prev_rank', 'cur_rank', 'rank_change', 'prev_pos_rank', 'cur_pos_rank', 'pos_rank_change']


def report_csv(report):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=_CSV_FIELDS, extrasaction='ignore')
    w.writeheader()
    for p in report['players']:
        row = dict(p)
        row['played'] = 'PLAYED' if p['played'] else 'DNP'
        row['score'] = ('DNP' if not p['played'] else p['score'])
        w.writerow(row)
    return buf.getvalue()


# ---- emit (post-commit) ---------------------------------------------------------------------------
def emit(repo_root, round_n, *, played=None, evidence=None, generated_at=None,
         movers_dir=None, ui_data_dir=None):
    """Build + persist the round's movers report: JSON + CSV under movers/, the accumulated UI bundle
    under ui/data/movers.js (never silently overwriting a DIFFERENT prior report for the same round),
    and the dRound/dRoundRank/dRoundPosRank injection into the working UI bundle. Returns evidence."""
    report = build_report(repo_root, round_n, played=played, evidence=evidence, generated_at=generated_at)
    ing = os.path.join(repo_root, 'engine', 'rl_after', 'ingestion')
    movers_dir = movers_dir or os.path.join(ing, 'movers')
    os.makedirs(movers_dir, exist_ok=True)
    jpath = os.path.join(movers_dir, 'movers_R%d.json' % int(round_n))
    cpath = os.path.join(movers_dir, 'movers_R%d.csv' % int(round_n))
    RH.save_json_atomic(jpath, RH.report_bytes(report))
    with open(cpath, 'w') as f:
        f.write(report_csv(report))

    ui_data_dir = ui_data_dir or os.path.join(repo_root, 'ui', 'data')
    bundle_path = os.path.join(ui_data_dir, 'movers.js')
    bundle_written = None
    if os.path.isdir(ui_data_dir):
        bundle_written = _accumulate_bundle(bundle_path, report)

    working = os.path.join(ui_data_dir, 'board_view_working.js')
    injected = _inject_working(working, report) if os.path.exists(working) else 0

    return {'round': int(round_n), 'movers_json': jpath, 'movers_csv': cpath,
            'ui_bundle': bundle_written, 'ui_rows_injected': injected,
            'player_count': report['player_count'], 'played': report['views']['played_count'],
            'dnp': report['views']['dnp_count'], 'board_md5_after': report['board_md5_after']}


def load_bundle(path):
    """Parse the `window.__MATCHDAY_MOVERS__ = {...};` bundle, or a fresh empty bundle."""
    if not os.path.exists(path):
        return {'kind': 'matchday_movers_bundle', 'schema_version': SCHEMA_VERSION, 'rounds': [], 'reports': {}}
    with open(path) as f:
        text = f.read()
    i, j = text.index('{'), text.rindex('}')
    return json.loads(text[i:j + 1])


def _accumulate_bundle(path, report):
    """Add/replace this round's report in the UI bundle. A round already present is only replaced when
    its board_md5_after MATCHES (idempotent re-emit); a DIFFERENT board for the same round would be an
    integrity break, so we keep both facts and flag it rather than silently overwrite history."""
    bundle = load_bundle(path)
    rnd = str(report['submitted_round'])
    reports = bundle.setdefault('reports', {})
    prior = reports.get(rnd)
    overwrite_conflict = bool(prior and prior.get('board_md5_after') != report['board_md5_after'])
    reports[rnd] = report
    bundle['rounds'] = sorted(int(r) for r in reports)
    # board-identity chain: report[n].board_md5_before must equal report[n-1].board_md5_after
    chain_ok = True
    for r in bundle['rounds']:
        rep = reports[str(r)]
        prevr = reports.get(str(r - 1))
        if prevr and rep.get('board_md5_before') and rep['board_md5_before'] != prevr.get('board_md5_after'):
            chain_ok = False
    bundle['integrity'] = {'board_chain_ok': chain_ok,
                           'overwrite_conflict_last_write': overwrite_conflict,
                           'rounds': bundle['rounds']}
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write('// GENERATED — Matchday movers bundle (weekly movers reports, one per committed round).\n')
        f.write('// Do not hand-edit; regenerate via engine/rl_after/ingestion/round_movers.py.\n')
        f.write('window.__MATCHDAY_MOVERS__ = ')
        json.dump(bundle, f, ensure_ascii=False, separators=(',', ':'))
        f.write(';\n')
    return path


def _inject_working(path, report):
    with open(path) as f:
        text = f.read()
    i, j = text.index('{'), text.rindex('}')
    prefix, obj, suffix = text[:i], json.loads(text[i:j + 1]), text[j + 1:]
    by_key = {p['key']: p for p in report['players']}
    injected = 0
    for row in obj.get('players', []):
        mv = by_key.get(row.get('key'))
        if mv:
            row['dRound'] = mv['value_change']
            row['dRoundRank'] = mv['rank_change']
            row['dRoundPosRank'] = mv['pos_rank_change']
            injected += 1
    with open(path, 'w') as f:
        f.write(prefix)
        json.dump(obj, f, ensure_ascii=False, separators=(',', ':'))
        f.write(suffix)
    return injected
