#!/usr/bin/env python3
"""ORDER I — THE MOVERS LEDGER, four board columns with the mechanism legs.

Columns: live 88ce647f · Candidate 31 fe6be9d6 · the landing candidate 1f176444 · ORDER I.
Legs, priced as real boards (each is a build, not an arithmetic split):
  leg S1     = the age-referenced projection bar alone, at the chosen dose
  leg TALL   = the tall/small sitter factor alone
  leg REMIX  = the counterweight (whatever the mature-row law leaves free)
  ORDER I    = all three together — and the sum of the legs is printed BESIDE the joint number so the
               non-additivity is visible rather than assumed away.
Pure JSON reads over boards already built by bb36.sh — no engine run here.
"""
import json, os, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
O36 = SP + '/o36'
C31 = json.load(open(SP + '/cand31.json'))
assert C31['boards']['candidate'].startswith('fe6be9d6') and C31['boards']['live'].startswith('88ce647f')

TAGS = ['cand', 's1', 'tall', 'full']          # cand = the landing candidate rebuild (dial off)
BP = {t: O36 + '/bb_%s/rl_after/rl_app_data.json' % t for t in TAGS}
MD5 = {t: hashlib.md5(open(BP[t], 'rb').read()).hexdigest() for t in TAGS}
B = {t: {r['key']: r for r in json.load(open(BP[t]))['active']} for t in TAGS}
print('boards:', {t: m[:8] for t, m in MD5.items()})
assert MD5['cand'].startswith('1f176444'), \
    'the dial-off rebuild is %s, not the landing candidate 1f176444 — HALT' % MD5['cand'][:8]

rows = []
for r in C31['rows']:
    k = r['key']
    if k not in B['cand']:
        continue
    b = B['cand'][k]
    vc, v1, vt, vf = (B[t][k]['v'] for t in TAGS)
    rows.append(dict(key=k, name=r['name'], pos=(b.get('gf') or b['grp']), age=b['age'],
                     pathway=r['pathway'], pick=r.get('pick'), g=r.get('g', 0), yr=r.get('yr'),
                     v0=r.get('v0', 0.0),
                     live=r['live'], cand31=r['cand'], landing=vc, order_i=vf,
                     leg_s1=v1 - vc, leg_tall=vt - vc, leg_remix=vf - (v1 + vt - vc),
                     legsum=(v1 - vc) + (vt - vc),
                     d_vs_landing=vf - vc, d_vs_cand31=vf - r['cand'], d_vs_live=vf - r['live']))
print('ledger rows: %d of %d C31 rows' % (len(rows), len(C31['rows'])))
tot = {f: sum(r[f] for r in rows) for f in
       ('live', 'cand31', 'landing', 'order_i', 'leg_s1', 'leg_tall', 'leg_remix')}
print('totals:', {k: round(v) for k, v in tot.items()})

MOVED = [r for r in rows if r['d_vs_landing'] != 0]
MATURE_MOVED = [r for r in MOVED if r['age'] >= 24]
print('rows that moved vs the landing candidate: %d of %d' % (len(MOVED), len(rows)))
print('MATURE (24+) rows that moved: %d  %s'
      % (len(MATURE_MOVED), 'PASS — the cap law holds store-wide' if not MATURE_MOVED
         else 'FAIL: ' + str([(r['key'], r['d_vs_landing']) for r in MATURE_MOVED[:8]])))

NAMED = ['harry-dean', 'cooper-duff-tytler', 'xavier-taylor', 'oskar-taylor', 'daniel-annable',
         'dylan-patterson', 'josh-smillie', 'chris-scerri', 'thomas-burton', 'milan-murdock',
         'will-green', 'toby-conway', 'steely-green', 'isaac-kako', 'alix-tauru', 'jedd-busslinger']
BYK = {r['key']: r for r in rows}
print('\n%-22s %4s %5s %4s %8s %8s %8s %8s | %8s %8s %8s %9s'
      % ('row', 'age', 'pick', 'g', 'live', 'C31', 'landing', 'ORDER I', 'leg S1', 'leg TALL', 'leg RMX', 'vs landing'))
LED = []
for k in NAMED:
    r = BYK.get(k)
    if r is None:
        print('%-22s (not on the 804-row active board)' % k); continue
    LED.append(r)
    print('%-22s %4s %5s %4.0f %8d %8d %8d %8d | %+8d %+8d %+8d %+8d (%+.1f%%)'
          % (r['name'][:22], r['age'], r['pick'], r['g'], r['live'], r['cand31'], r['landing'],
             r['order_i'], r['leg_s1'], r['leg_tall'], r['leg_remix'], r['d_vs_landing'],
             100.0 * r['d_vs_landing'] / max(1, r['landing'])))

TOPUP = sorted(rows, key=lambda r: -r['d_vs_landing'])[:20]
TOPDN = sorted(rows, key=lambda r: r['d_vs_landing'])[:20]
print('\nTOP 20 UP vs the landing candidate:')
for r in TOPUP:
    print('  %-24s %3s %4s %5.0fg  %7d -> %7d  %+7d' % (r['name'][:24], r['age'], r['pick'], r['g'],
                                                        r['landing'], r['order_i'], r['d_vs_landing']))
print('\nTOP 20 DOWN vs the landing candidate:')
for r in TOPDN:
    print('  %-24s %3s %4s %5.0fg  %7d -> %7d  %+7d' % (r['name'][:24], r['age'], r['pick'], r['g'],
                                                        r['landing'], r['order_i'], r['d_vs_landing']))

AGE = collections.Counter()
for r in MOVED:
    AGE[r['age']] += 1
print('\nage profile of the rows that moved: %s' % dict(sorted(AGE.items())))

os.makedirs(os.path.join(ROOT, 'docs', 'ledgers'), exist_ok=True)
json.dump(dict(order='ORDER I — the movers ledger, four boards with mechanism legs',
               meta=dict(boards=dict(live=C31['boards']['live'], cand31=C31['boards']['candidate'],
                                     landing=MD5['cand'], leg_s1=MD5['s1'], leg_tall=MD5['tall'],
                                     order_i=MD5['full'])),
               totals=tot, rows=rows, named=LED, n_moved=len(MOVED), n_mature_moved=len(MATURE_MOVED),
               age_profile={str(k): v for k, v in sorted(AGE.items())}),
          open(os.path.join(ROOT, 'docs', 'ledgers', 'ORDER_I_MOVERS.json'), 'w'), indent=1, default=float)
print('\nwrote docs/ledgers/ORDER_I_MOVERS.json')
