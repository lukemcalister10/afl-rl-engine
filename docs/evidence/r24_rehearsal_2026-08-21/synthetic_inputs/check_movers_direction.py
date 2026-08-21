#!/usr/bin/env python3
"""THE MOVERS SANITY CHECK — do better scores move players UP?

The synthetic R24 file was authored with TEN DECLARED RISERS (scores forced into the 115-148 band)
and TEN DECLARED FALLERS (scores forced into the 12-31 band). This reads the movers report of
record the advance transaction wrote and checks the direction of each, so the answer is a
measurement rather than an impression.
"""
import json, os, re, sys
ROOT = sys.argv[1]
N = int(sys.argv[2]) if len(sys.argv) > 2 else 24
meta = json.load(open(os.path.join(ROOT, 'docs/evidence/r24_rehearsal_2026-08-21/R24_SYNTHETIC_META.json')))
rep = json.load(open(os.path.join(ROOT, 'engine/rl_after/ingestion/movers/movers_R%d.json' % N)))

def norm(s):
    return re.sub(r'[^a-z0-9]+', '-', str(s).strip().lower().replace('’', "'")).strip('-')

rows = rep.get('players') or rep.get('movers') or rep.get('rows') or []
if isinstance(rows, dict):
    rows = sum((v for v in rows.values() if isinstance(v, list)), [])
by = {}
for r in rows:
    if not isinstance(r, dict):
        continue
    k = r.get('key') or norm(r.get('name') or r.get('player') or '')
    by[k] = r
print('report keys      : %s' % sorted(rep)[:14])
print('mover rows       : %d' % len(rows))
if rows:
    print('a mover row      : %s' % json.dumps(rows[0], sort_keys=True)[:300])
print('baseline point   : %s' % rep.get('previous_round'))
print('board            : %s -> %s' % (rep.get('board_md5_before'), rep.get('board_md5_after')))
print('store            : %s -> %s' % (rep.get('source_store_md5_before'), rep.get('source_store_md5_after')))
print()

def delta(r):
    if 'value_change' in r:
        return r['value_change']
    if 'cur_value' in r and 'prev_value' in r:
        return r['cur_value'] - r['prev_value']
    return None

bad = []
for label, names, want in (('RISER', meta['risers'], +1), ('FALLER', meta['fallers'], -1)):
    for n in names:
        r = by.get(norm(n))
        d = delta(r) if r else None
        verdict = 'NOT IN REPORT' if r is None else ('no delta field' if d is None else
                  ('OK' if (d > 0) == (want > 0) else '*** WRONG DIRECTION'))
        if verdict.startswith('***'):
            bad.append((label, n, d))
        rk = (r or {}).get('rank_change')
        print('  %-7s %-22s score=%-6s value %-6s -> %-6s  delta=%-7s rank_change=%-5s %s'
              % (label, n.strip(), (r or {}).get('score'), (r or {}).get('prev_value'),
                 (r or {}).get('cur_value'), d, rk, verdict))
print()
print('WRONG-DIRECTION MOVERS: %d' % len(bad))
sys.exit(1 if bad else 0)
