"""ROUND HISTORY — persistent per-player round-by-round VALUE, overall-RANK and positional-RANK history.

The weekly updater's staged transaction (staged_apply.py) regenerates the board from the newly merged
store. This module turns each committed board into three DURABLE, APPEND-ONLY records:

  * value_history.json     — every active player's board value `v`, keyed by round;
  * rank_history.json      — every active player's OVERALL board rank (1 = highest `v`), keyed by round;
  * pos_rank_history.json  — every active player's rank WITHIN their position group (grp), keyed by round.

All three are transaction targets (see staged_apply.TARGETS): staged in the workspace, validated,
committed atomically with the store/board, and rolled back / recovered on any failure — a crash can
never leave a half-written history. They are the persistent record the Matchday UI's previous-round
movement (`dRound` / `dRoundRank`) and the owner's week-over-week + movers views read from.

LAWS
  * APPEND-ONLY. An existing (player, round) value/rank is NEVER modified — a round already recorded
    stays byte-identical. The dedup ledger blocks re-applying a round, so a round is written once.
  * TRANSITION SEED. The FIRST apply seeds the PREVIOUS round (round-1) from the PRE-APPLY board — the
    accepted round-14 board when round 15 is applied — so the first history already carries the
    round-14 -> round-15 transition for every active player. Later applies only append the new round.
  * DETERMINISTIC BYTES. Canonical JSON (sorted keys, fixed indent). Overall rank is a total order
    (descending `v`, ties by key); positional rank is the same order within a group — both reproducible
    from a board alone.
  * NO VALUATION. This module reads a finished board and writes JSON. It computes NO value, tunes NO
    parameter, and never touches the store or the engine.
"""
import json
import os
import tempfile

KIND_VALUE = 'weekly_value_history'
KIND_RANK = 'weekly_rank_history'
KIND_POS_RANK = 'weekly_pos_rank_history'
SCHEMA_VERSION = 1

# (kind, field-in-metrics) for the three histories — drives staging/validation uniformly.
HISTORIES = (('value', KIND_VALUE, 'v'), ('rank', KIND_RANK, 'rank'),
             ('pos_rank', KIND_POS_RANK, 'pos_rank'))


def board_active(board):
    """The active player list of a board (a dict with `active`, or a bare list)."""
    if isinstance(board, dict):
        return board.get('active') or []
    return board or []


def board_metrics(board):
    """Map each active player key -> {'name','stable_player_id','v','rank','grp','pos_rank'}.

    `rank` is the OVERALL total order (1 = highest value; ties by key). `pos_rank` is the rank within
    the player's position group `grp` (same order, restricted to the group). Both are reproducible from
    the board alone. Rows without a key are skipped (a keyless row cannot be tracked across rounds)."""
    rows = [p for p in board_active(board) if p.get('key')]
    ordered = sorted(rows, key=lambda p: (-(float(p.get('v') or 0.0)), p.get('key')))
    out = {}
    pos_counter = {}
    for rank, p in enumerate(ordered, start=1):
        grp = p.get('grp') or p.get('gf')
        pos_counter[grp] = pos_counter.get(grp, 0) + 1
        out[p['key']] = {
            'name': p.get('name'),
            'stable_player_id': p.get('stable_player_id') or p.get('sid'),
            'v': p.get('v'),
            'rank': rank,
            'grp': grp,
            'pos_rank': pos_counter[grp],
        }
    return out


def value_rank_map(board):
    """Backward-compatible view: {key: {'name','stable_player_id','v','rank'}} (overall rank)."""
    return {k: {'name': m['name'], 'stable_player_id': m['stable_player_id'], 'v': m['v'], 'rank': m['rank']}
            for k, m in board_metrics(board).items()}


def empty_history(kind, season):
    return {'kind': kind, 'schema_version': SCHEMA_VERSION, 'season': int(season),
            'rounds': [], 'players': {}}


def _ensure(hist, kind, season):
    if not isinstance(hist, dict) or hist.get('kind') != kind:
        return empty_history(kind, season)
    hist.setdefault('schema_version', SCHEMA_VERSION)
    hist.setdefault('season', int(season))
    hist.setdefault('rounds', [])
    hist.setdefault('players', {})
    return hist


def _accrue(hist, kind, season, round_n, prev_round_n, cur_map, prev_map, field):
    """Append `round_n` (and, if missing, seed `prev_round_n`) into a history, NON-DESTRUCTIVELY.

    An existing (player, round) entry is NEVER overwritten. Returns the same dict, mutated."""
    hist = _ensure(hist, kind, season)
    players = hist['players']
    rounds_present = set(hist['rounds'])
    for key, cur in cur_map.items():
        entry = players.get(key)
        if entry is None:
            entry = {'name': cur.get('name'), 'stable_player_id': cur.get('stable_player_id'),
                     'by_round': {}}
            players[key] = entry
        else:
            if cur.get('name'):
                entry['name'] = cur.get('name')
            if cur.get('stable_player_id'):
                entry['stable_player_id'] = cur.get('stable_player_id')
        by_round = entry.setdefault('by_round', {})
        pk = str(prev_round_n)
        if prev_round_n >= 1 and pk not in by_round and key in prev_map:
            by_round[pk] = prev_map[key].get(field)
            rounds_present.add(prev_round_n)
        ck = str(round_n)
        if ck not in by_round:
            by_round[ck] = cur.get(field)
            rounds_present.add(round_n)
    hist['rounds'] = sorted(rounds_present)
    return hist


def update_histories(histories, *, season, round_n, prev_board, new_board):
    """Fold one committed board transition into the value / overall-rank / positional-rank histories.

    `histories` is a dict {'value':.., 'rank':.., 'pos_rank':..} of the current history objects (any may
    be an empty/None history). Returns the same dict with each history appended (append-only). The
    previous round is seeded only if missing, so the next round never rewrites an earlier round."""
    round_n = int(round_n)
    prev_round_n = round_n - 1
    cur_metrics = board_metrics(new_board)
    prev_metrics = board_metrics(prev_board) if prev_board is not None else {}
    for name, kind, field in HISTORIES:
        histories[name] = _accrue(histories.get(name), kind, season, round_n, prev_round_n,
                                  cur_metrics, prev_metrics, field)
    return histories


def compute_movers(prev_board, new_board, round_n):
    """Per-player movement of a committed round vs the previous round: value delta, overall-rank delta,
    positional-rank delta. Returns a movers report {round, players:[...], top_value_gain/loss,
    top_rank_gain/loss}. A rank DELTA is prev_rank - new_rank (positive == moved UP the ladder). Only
    players present in BOTH boards get a delta; a rank of None means no prior round to compare."""
    cur = board_metrics(new_board)
    prev = board_metrics(prev_board) if prev_board is not None else {}
    players = []
    for key, m in cur.items():
        p = prev.get(key)
        dv = (m['v'] - p['v']) if (p and m['v'] is not None and p['v'] is not None) else None
        drank = (p['rank'] - m['rank']) if p else None                # +ve == moved up overall
        dpos = (p['pos_rank'] - m['pos_rank']) if p else None         # +ve == moved up within position
        players.append({'key': key, 'name': m['name'], 'stable_player_id': m['stable_player_id'],
                        'grp': m['grp'], 'v': m['v'], 'rank': m['rank'], 'pos_rank': m['pos_rank'],
                        'dRound': dv, 'dRoundRank': drank, 'dRoundPosRank': dpos})
    movers = [p for p in players if p['dRound'] is not None]
    by_v = sorted(movers, key=lambda p: p['dRound'])
    by_rank = sorted((p for p in movers if p['dRoundRank'] is not None), key=lambda p: p['dRoundRank'])
    return {
        'round': int(round_n), 'players_compared': len(movers), 'players_total': len(players),
        'top_value_gain': list(reversed(by_v[-10:])), 'top_value_loss': by_v[:10],
        'top_rank_gain': list(reversed(by_rank[-10:])), 'top_rank_loss': by_rank[:10],
        'by_key': {p['key']: {'dRound': p['dRound'], 'dRoundRank': p['dRoundRank'],
                              'dRoundPosRank': p['dRoundPosRank']} for p in players},
    }


def report_bytes(obj):
    return (json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=True) + '\n').encode('utf-8')


def history_bytes(hist):
    """Canonical, byte-deterministic serialization of a history file."""
    return report_bytes(hist)


def load_history(path, kind=None, season=2026):
    """Load a history file; an absent/blank file is an empty history (nothing recorded yet)."""
    if not path or not os.path.exists(path):
        return empty_history(kind or KIND_VALUE, season)
    with open(path) as f:
        return json.load(f)


def save_history(path, hist):
    """Write a history file atomically (temp + rename; never a torn/partial history)."""
    save_json_atomic(path, history_bytes(hist))


def save_json_atomic(path, raw_bytes):
    d = os.path.dirname(os.path.abspath(path))
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix='.hist_tmp_', suffix='.json', dir=d)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(raw_bytes)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def rounds_recorded(hist):
    return sorted(int(r) for r in (hist.get('rounds') or []))


def player_round_value(hist, key, round_n):
    """Fetch one (player, round) recorded value/rank, or None. Used by the integrity proof."""
    entry = (hist.get('players') or {}).get(key)
    if not entry:
        return None
    return (entry.get('by_round') or {}).get(str(int(round_n)))
