"""OUT-OF-ROUND HISTORY COLUMNS — a stored comparison point at a board that no round produced.

WHY THIS EXISTS. The three histories (value / rank / pos_rank) record one column per applied round.
That is enough while the board only ever moves by applying a round. It does not: the ITEM 411 D1 /
ITEM 408 D2 restructure moved the board (`6f07f7cb -> fa172ac1`) with no round attached, and the
re-derivation and ITEM 412 will each do it again. Those moments are real, they change every player's
value, and before this module there was nowhere to record them — so a from/to comparison could not
name them as endpoints.

THE STANDING RULE (owner word 2026-07-28): whenever the board moves OUTSIDE a round, write a column
at that point. It is cheap — a snapshot of the values a finished board already carries, not a
derivation — and it is what keeps the Movers dropdown honest.

HOW IT IS STORED. Numbered rounds keep the shape they have always had: integer keys in `by_round`,
and a top-level `rounds` list that readers int-coerce (`round_history.rounds_recorded`). An
out-of-round point must NOT go in that list — it is not a round and a fake round number would be a
lie the rest of the system would believe. Instead:

  * its values live in `by_round` under a STRING id (e.g. `post-r19-redesign-1`);
  * its metadata is registered in a new top-level `columns` list, which carries ONLY out-of-round
    points — numbered rounds stay implicit in `rounds`, so appending a round never needs to touch it.

`columns` entries are ordered by `after_round`: the point sits immediately after the last round that
preceded it. Selectable points = `rounds` + `columns`.

APPEND-ONLY, like the histories themselves. Re-registering a column with identical values is an
idempotent no-op; re-registering it with DIFFERENT values raises rather than overwriting.

NO VALUATION. This module reads a finished board and writes JSON. It computes no value, tunes no
parameter, and never touches the store or the engine.
"""
import json
import os

try:
    from . import round_history as RH
except (ImportError, ValueError):    # allow direct-script / non-package execution
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import round_history as RH       # type: ignore

HISTORY_FILES = (('value', 'value_history.json', 'v'),
                 ('rank', 'rank_history.json', 'rank'),
                 ('pos_rank', 'pos_rank_history.json', 'pos_rank'))


class ColumnConflictError(RuntimeError):
    """An existing column id carries different values — never silently overwritten."""


def _ingestion_dir(repo_root):
    return os.path.join(repo_root, 'engine', 'rl_after', 'ingestion')


def selectable_points(hist):
    """Every comparison point in a history, in display order.

    Returns [{'id','label','kind','after_round','board'}]. Numbered rounds come from `rounds`
    (kind='round'); out-of-round points come from `columns` (kind='out_of_round') and are placed
    immediately after the round they follow."""
    points = [{'id': str(r), 'label': 'Round %d' % r, 'kind': 'round', 'after_round': r, 'board': None}
              for r in RH.rounds_recorded(hist)]
    for col in (hist.get('columns') or []):
        points.append({'id': col['id'], 'label': col['label'], 'kind': 'out_of_round',
                       'after_round': col.get('after_round'), 'board': col.get('board')})
    # stable: by the round each point follows, out-of-round points AFTER that round's own column
    points.sort(key=lambda p: (p['after_round'] if p['after_round'] is not None else -1,
                               0 if p['kind'] == 'round' else 1))
    return points


def column_ids(hist):
    return [c['id'] for c in (hist.get('columns') or [])]


def _register(hist, column_id, label, after_round, board_md5):
    cols = hist.setdefault('columns', [])
    for c in cols:
        if c['id'] == column_id:
            c['label'], c['after_round'], c['board'] = label, int(after_round), board_md5
            return
    cols.append({'id': column_id, 'label': label, 'kind': 'out_of_round',
                 'after_round': int(after_round), 'board': board_md5})
    cols.sort(key=lambda c: (c['after_round'], c['id']))


def add_column(repo_root, *, column_id, label, after_round, board, board_md5, dry_run=False):
    """Write one out-of-round column into all three histories from a finished `board`.

    `board` is a parsed board object (dict with `active`, or a bare list). `board_md5` is recorded as
    the column's provenance. Returns an evidence dict. Raises ColumnConflictError if the column
    already exists with different values."""
    metrics = RH.board_metrics(board)
    ing = _ingestion_dir(repo_root)
    written, unchanged = {}, {}
    staged = []
    for name, fname, field in HISTORY_FILES:
        path = os.path.join(ing, fname)
        hist = RH.load_history(path)
        players = hist.setdefault('players', {})
        n_new = n_same = 0
        for key, m in metrics.items():
            entry = players.get(key)
            if entry is None:
                # a player on this board with no history yet — record identity alongside the value
                entry = {'name': m.get('name'), 'stable_player_id': m.get('stable_player_id'),
                         'by_round': {}}
                players[key] = entry
            by_round = entry.setdefault('by_round', {})
            val = m.get(field)
            if column_id in by_round:
                if by_round[column_id] != val:
                    raise ColumnConflictError(
                        '%s: column %r already holds %r for %s, refusing to overwrite with %r'
                        % (fname, column_id, by_round[column_id], key, val))
                n_same += 1
            else:
                by_round[column_id] = val
                n_new += 1
        _register(hist, column_id, label, after_round, board_md5)
        written[name], unchanged[name] = n_new, n_same
        staged.append((path, hist))

    if not dry_run:
        for path, hist in staged:
            RH.save_history(path, hist)

    return {'column_id': column_id, 'label': label, 'after_round': int(after_round),
            'board': board_md5, 'players_on_board': len(metrics),
            'values_written': written, 'values_already_present': unchanged,
            'dry_run': bool(dry_run)}


def load_board(path_or_text):
    """Parse a board from a path or from raw JSON text (so a board recovered from git history can be
    passed straight in without a temp file)."""
    if isinstance(path_or_text, (dict, list)):
        return path_or_text
    if os.path.exists(path_or_text):
        with open(path_or_text) as f:
            return json.load(f)
    return json.loads(path_or_text)
