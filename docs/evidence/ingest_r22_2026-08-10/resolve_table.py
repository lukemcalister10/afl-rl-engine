#!/usr/bin/env python3
"""Read-only: dump the R22 name-resolution table exactly as the catch-up resolves it.

Writes:
  _scratch/r22_resolution.json  — every listed row -> stable key, and how it resolved
  _scratch/r22_absent.json      — active store players NOT listed in the file (DNP by owner ruling)
Nothing is written to the store, board or any repo artifact.
"""
import json
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(REPO, 'engine', 'rl_after', 'ingestion'))
sys.path.insert(0, os.path.join(REPO, 'engine', 'rl_after'))

import round_catchup as RC       # noqa: E402
import footywire_parser as FW    # noqa: E402

SRC = os.path.join(REPO, 'scores', 'R22.csv')
cu = RC.RoundCatchup(REPO, [(22, SRC)])
report, rounds = cu.preflight()
rd = rounds[0]
assert rd['round'] == 22
assert not rd['unresolved'] and not rd['ambiguous'] and not rd['duplicate_keys']

parsed = FW.parse_round_file(SRC)
raw = parsed['rows']
rows = rd['resolved_rows']
assert len(raw) == len(rows) == 409, (len(raw), len(rows))

store = json.load(open(os.path.join(REPO, 'engine', 'rl_after', 'rl_model_data.json')))
by_key = {r['key']: r for r in store if r.get('key')}

table = []
for (fname, fscore), r in zip(raw, rows):
    assert float(fscore) == float(r.score), (fname, fscore, r.score)
    srow = by_key[r.key]
    table.append({
        'file_name': fname,
        'file_score': fscore,
        'store_key': r.key,
        'store_name': srow.get('player'),
        'afl_club': srow.get('afl_club'),
        'stable_player_id': r.stable_player_id,
        'exact_name_match': srow.get('player') == fname,
        'via': r.via,
    })

json.dump({'kind': 'r22_identity_resolution', 'round': 22, 'season': 2026,
           'source_file': 'scores/R22.csv (owner-couriered, byte-unmodified)',
           'source_sha256': rd['sha256'],
           'listed': rd['listed'], 'resolved': rd['resolved'],
           'distinct_stable_keys': len({t['store_key'] for t in table}),
           'listed_zero': rd['listed_zero'], 'absent_dnp': rd['absent_dnp'],
           'active_universe': rd['active_universe'], 'preflight_clean': report['clean'],
           'table': table},
          open(os.path.join(REPO, '_scratch', 'r22_resolution.json'), 'w'),
          indent=1, sort_keys=True)

listed_keys = {t['store_key'] for t in table}
active = [r for r in store if r.get('stable_player_id') and not r.get('_retired')]
absent = sorted([{'key': r['key'], 'name': r.get('player'), 'afl_club': r.get('afl_club')}
                 for r in active if r['key'] not in listed_keys], key=lambda d: d['key'])
json.dump({'kind': 'r22_absent_dnp', 'round': 22, 'active_pool': len(active),
           'listed': len(listed_keys), 'absent_dnp': len(absent),
           'convention': 'Owner ruling 2026-07-20: file membership defines participation. A player '
                         'ABSENT from the round file DID NOT PLAY — nothing is appended, no game is '
                         'added, and absence is not an unresolved-input condition.',
           'players': absent},
          open(os.path.join(REPO, '_scratch', 'r22_absent.json'), 'w'), indent=1, sort_keys=True)

print('listed %d · resolved %d · distinct keys %d · listed-zero %d · absent/DNP %d · active %d · clean %s'
      % (rd['listed'], rd['resolved'], len(listed_keys), rd['listed_zero'], len(absent),
         rd['active_universe'], report['clean']))
nonexact = [t for t in table if not t['exact_name_match']]
print('\nrows whose FILE name is not byte-identical to the STORE name: %d' % len(nonexact))
for t in nonexact:
    print('  file %-22r %6g  ->  %-22s  store name %-22r  club %-18s  via %s'
          % (t['file_name'], t['file_score'], t['store_key'], t['store_name'],
             t['afl_club'], t['via']))
print('\nrows with no store key: %d' % len([t for t in table if not t['store_key']]))
