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

ORDER WITHIN A ROUND IS CHRONOLOGICAL, AND IT IS RECORDED, NOT INFERRED (repair 2026-08-20).
Two or more columns can share an `after_round` — five of them do at round 22 — and until this repair
both the writer and the reader broke that tie on `id`, i.e. ALPHABETICALLY. The alphabet is not
chronology: `the-d8-adoption-20-8` sorts before `the-landing-20-8`, but THE LANDING (`a05fe951`)
came first and the D8 adoption (`5ea978f7`) is the board that SUPERSEDED it. The consequence is
recorded in `docs/runbooks/R23_RUNBOOK.md` (errata) and `docs/evidence/r23_advance_2026-08-20/`:
before the R23 advance the newest stored point was the RETIRED pre-D8 board, and two
`ui/tests/movers.test.js` assertions were red because of it. The R23 seat worked around it by
asserting `previous_point` after writing its column instead of trusting the alphabet.

The repair: every NEW column is stamped with an explicit monotonic `seq` (plus `registered_at`), so
registration order — which IS chronology, since a column is written when the board moves — is stored
as data. Writer and reader share ONE ordering key (`_order_key`), so they can never drift apart again.

The eight columns registered BEFORE the repair carry no `seq` and are NOT given one: they are history,
and back-filling a field into a stored history to make a new reader happy is the bending this tree
forbids. They are ordered instead by `_LEGACY_ORDER` below — an explicit, one-time table whose
provenance is `data/release_lineage.json`'s append-only `release_transition_register`, the
owner-approved record of every board move, which chains them unambiguously by destination board.
Legacy entries sort before `seq`-bearing ones within a round, which is correct: all eight were
registered before any `seq` existed.


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


# ---- ordering -------------------------------------------------------------------------------------
# THE CHRONOLOGICAL ORDER OF THE EIGHT PRE-REPAIR COLUMNS. Sourced from data/release_lineage.json's
# append-only `release_transition_register`, which records each board move as source -> destination and
# so chains them without ambiguity. The two entries the alphabet got wrong are marked:
#
#   reg 1  8a38cca4 -> f2df6e0a   rederivation-30-7
#   reg 3  f2df6e0a -> 827fb1fd   redesign-adoption-6-8
#   reg 4  6e724cca -> a672ed3a   dob-courier-10-8
#   reg 5  a672ed3a -> 4b448a82   g1-never-rises-10-8
#   reg 6  88ce647f -> a05fe951   the-landing-20-8        <- came FIRST  (alphabet put it fourth)
#   reg 8  a05fe951 -> 5ea978f7   the-d8-adoption-20-8    <- SUPERSEDED it (alphabet put it third)
#   reg 9  5ea978f7 -> 1d5c9f7a   the-sheet-recut-20-8
#
# `post-r19-redesign-1` predates the register; it is the only column at after_round 19, so no tie
# exists for it to lose. This table is CLOSED — it describes history and never grows. A column
# registered from now on carries its own `seq` and is ordered by it.
_LEGACY_ORDER = ('post-r19-redesign-1',
                 'rederivation-30-7',
                 'redesign-adoption-6-8',
                 'dob-courier-10-8',
                 'g1-never-rises-10-8',
                 'the-landing-20-8',
                 'the-d8-adoption-20-8',
                 'the-sheet-recut-20-8')
_LEGACY_RANK = {cid: i for i, cid in enumerate(_LEGACY_ORDER)}


def _order_key(col):
    """The ONE ordering key, shared by the writer (`_register`) and the reader (`selectable_points`),
    so the stored order and the displayed order cannot drift apart.

    `(after_round, tier, rank)`. `tier` 0 = a legacy column ordered by `_LEGACY_ORDER`; tier 1 = a
    column carrying an explicit `seq`. Legacy before sequenced within a round, because every legacy
    column was registered before `seq` existed. A column with neither — an id this module has never
    seen, registered by something other than `_register` — sorts last within its round rather than
    silently taking a position it has no claim to."""
    after = col.get('after_round')
    after = -1 if after is None else int(after)
    seq = col.get('seq')
    if seq is not None:
        return (after, 1, int(seq))
    rank = _LEGACY_RANK.get(col.get('id'))
    if rank is not None:
        return (after, 0, rank)
    return (after, 2, 0)


def _next_seq(cols):
    """One past the highest `seq` any column already carries (0 if none does). Monotonic across the
    whole history, not per-round, so a `seq` is a global registration ordinal."""
    seqs = [int(c['seq']) for c in cols if c.get('seq') is not None]
    return (max(seqs) + 1) if seqs else 0


def _ingestion_dir(repo_root):
    return os.path.join(repo_root, 'engine', 'rl_after', 'ingestion')


def selectable_points(hist):
    """Every comparison point in a history, in display order.

    Returns [{'id','label','kind','after_round','board'}]. Numbered rounds come from `rounds`
    (kind='round'); out-of-round points come from `columns` (kind='out_of_round') and are placed
    immediately after the round they follow."""
    points = [{'id': str(r), 'label': 'Round %d' % r, 'kind': 'round', 'after_round': r, 'board': None,
               '_ord': (r, 0, -1)}
              for r in RH.rounds_recorded(hist)]
    for col in (hist.get('columns') or []):
        after, tier, rank = _order_key(col)
        points.append({'id': col['id'], 'label': col['label'], 'kind': 'out_of_round',
                       'after_round': col.get('after_round'), 'board': col.get('board'),
                       # the numbered round itself is (after, 0, -1), so any out-of-round point at the
                       # same after_round lands AFTER it whatever its tier — the round comes first.
                       '_ord': (after, 1 + tier, rank)})
    # by the round each point follows; within a round, the round's own column first, then the
    # out-of-round points in CHRONOLOGICAL order (explicit `seq`, or the closed legacy table).
    points.sort(key=lambda p: p['_ord'])
    for p in points:
        del p['_ord']
    return points


def column_ids(hist):
    return [c['id'] for c in (hist.get('columns') or [])]


def _register(hist, column_id, label, after_round, board_md5, registered_at=None):
    """Register (or idempotently re-register) one column's metadata.

    A NEW column is stamped with the next global `seq` and a `registered_at` timestamp — the record
    of WHEN, which is what the ordering needs and what the id could never supply. A re-registration
    updates the mutable descriptive fields and LEAVES `seq`/`registered_at` alone: the moment a
    column was first written does not change because someone relabelled it."""
    cols = hist.setdefault('columns', [])
    for c in cols:
        if c['id'] == column_id:
            c['label'], c['after_round'], c['board'] = label, int(after_round), board_md5
            cols.sort(key=_order_key)
            return
    entry = {'id': column_id, 'label': label, 'kind': 'out_of_round',
             'after_round': int(after_round), 'board': board_md5,
             'seq': _next_seq(cols)}
    if registered_at:
        entry['registered_at'] = registered_at
    cols.append(entry)
    # sorted by the SAME key the reader uses, so the stored order is the display order
    cols.sort(key=_order_key)


def add_column(repo_root, *, column_id, label, after_round, board, board_md5, dry_run=False,
               registered_at=None):
    """Write one out-of-round column into all three histories from a finished `board`.

    `board` is a parsed board object (dict with `active`, or a bare list). `board_md5` is recorded as
    the column's provenance. Returns an evidence dict. Raises ColumnConflictError if the column
    already exists with different values.

    `registered_at` is OPTIONAL provenance the caller may supply (an ISO-8601 string). It is not the
    ordering key — `seq`, stamped by `_register`, is, and it is deterministic, so a replay of the same
    registrations reproduces the same file. A wall-clock default is deliberately NOT taken: it would
    make an append unreproducible for no ordering benefit."""
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
        _register(hist, column_id, label, after_round, board_md5, registered_at=registered_at)
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
