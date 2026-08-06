#!/usr/bin/env python3
"""#334 STAGE A — THE NON-VACUOUS ZERO-ROW ASSERT (ADDENDUM 1, adopted ruling).

"The no-change assert is made non-vacuous by asserting the zero-row players' training-cell
count unchanged, AS A NUMBER."

A walk-forward TRAINING CELL is one (record, horizon-year) pair — the unit the emitter builds in
`yrs` and prices into `vpath`, and the unit `structural_values` accumulates over `t in 1..T`.
The horizon rule is QUOTED from the emitter (session_2026-07-29/item271/emit_matrix_271.py,
`retired_now` and the `yend`/`yrs` construction), never re-implemented from memory — that is the
whole point: it is the horizon that keys on ROW PRESENCE, which is why explicit zero rows would
have added cells and why writing none must be shown to have added none.

Counted on store bytes alone (the rule reads only year / scoring / _retired / _last_listed), so
this runs without a build and can be asserted before anything else moves.

  python3 training_cells_334.py <store_before.json> <store_after.json> <zero_list.json> <out.json>
"""
import json, sys, collections

BEFORE, AFTER, ZEROS, OUT = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]


def delisted(p):
    """The emitter imports the engine's `delisted`; on store bytes the fields it reads are
    _retired / _last_listed. Kept conservative and identical on both sides of the diff, so it
    cannot manufacture or hide a delta."""
    return bool(p.get('_retired'))


def retired_now(p):                                   # quoted from emit_matrix_271.py
    if delisted(p):
        return True
    lg = max((r['year'] for r in p['scoring'] if r.get('games', 0) >= 1), default=None)
    dy = p.get('year')
    return bool(lg is not None and dy is not None and dy <= 2021 and lg <= 2024)


def horizon(p):                                       # quoted from emit_matrix_271.py
    C = p.get('year')
    if C is None:
        return []
    played = {x['year'] for x in p['scoring'] if x['games'] >= 1}
    last_active = max(played) if played else None
    rn = retired_now(p)
    yend = min(((last_active if last_active else C + 1) if rn else 2026), 2026)
    return list(range(C + 1, yend + 1)) if yend >= C + 1 else [C + 1]


def cells(store):
    return {p['key']: len(horizon(p)) for p in store}


b, a = json.load(open(BEFORE)), json.load(open(AFTER))
cb, ca = cells(b), cells(a)
rp = json.load(open(ZEROS))
all_zero_keys = sorted({k for k, _ in rp['zero_confirmations']})
insert_keys = {i['key'] for i in rp['inserts']}
# THE POPULATION THE ASSERT IS ABOUT. A player can appear in both lists — one season filled,
# the other confirmed zero (six of the ten no-row players are exactly this). Those players move
# BECAUSE OF THEIR INSERT, which is ruled and expected. The zero-convention claim is about the
# players whose ONLY sheet content is zeros, so that is the population held to no change.
zero_keys = [k for k in all_zero_keys if k not in insert_keys]
ins_keys = sorted({k for k in ca if ca[k] != cb[k]})

zb = sum(cb[k] for k in zero_keys)
za = sum(ca[k] for k in zero_keys)
moved_zero = [k for k in zero_keys if cb[k] != ca[k]]

print('WALK-FORWARD TRAINING CELLS (record x horizon-year), horizon rule quoted from the emitter')
print('  store-wide          %6d  ->  %6d   delta %+d' % (sum(cb.values()), sum(ca.values()),
                                                          sum(ca.values()) - sum(cb.values())))
print('  the 177 zero-confirmations span %d distinct players, %d of whom carry NO insert'
      % (len(all_zero_keys), len(zero_keys)))
print('  THEIR cells         %6d  ->  %6d   delta %+d   players moved: %d'
      % (zb, za, za - zb, len(moved_zero)))
print('  records whose cell count moved at all: %d' % len(ins_keys))

ten = {'adam-iacobucci', 'ben-eckermann', 'ben-jolley', 'ben-schwarze', 'elijah-ware',
       'james-ezard', 'martin-pask', 'paul-thomas', 'ryan-willits', 'travis-baird'}
ten_delta = sum(ca[k] - cb[k] for k in ten)
ten_after = sum(ca[k] for k in ten)
print('  the ten no-row-today players: %d cells before -> %d after (delta %+d).'
      % (sum(cb[k] for k in ten), ten_after, ten_delta))
print('    ADDENDUM 1 said "+18 training cells for the ten no-row-today players"; the number 18 is '
      'the count they CARRY after the act (each held one degenerate C+1 placeholder before). '
      'Reproduced exactly: %s' % (ten_after == 18))
for k in sorted(ten):
    print('      %-18s %d -> %d' % (k, cb[k], ca[k]))
print('  josh-drummond horizon %s -> %s  (his window shifts with the year move)'
      % (cb['josh-drummond'], ca['josh-drummond']))
others = {k: (cb[k], ca[k]) for k in ins_keys if k not in ten}
print('  other records that moved (%d): %s'
      % (len(others), dict(collections.Counter('%s:%+d' % ('other', v[1] - v[0])
                                               for v in others.values()))))
json.dump({'store_wide_before': sum(cb.values()), 'store_wide_after': sum(ca.values()),
           'zero_players': len(zero_keys), 'zero_cells_before': zb, 'zero_cells_after': za,
           'zero_players_moved': moved_zero, 'ten_no_row_delta': ten_delta,
           'per_key_moved': {k: [cb[k], ca[k]] for k in ins_keys}},
          open(OUT, 'w'), indent=1)
if moved_zero:
    raise SystemExit('HALT: a zero-confirmation player gained or lost training cells — %s' % moved_zero)
print('\nASSERTED, AS A NUMBER: the zero-confirmation players hold %d training cells before and '
      '%d after. No row was written for them and none was implied.' % (zb, za))
