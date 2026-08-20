#!/usr/bin/env python3
"""ORDER J — THE MOVERS LEDGER, over the four standing board columns plus the mechanism legs.

Columns: live 88ce647f · Candidate 31 fe6be9d6 · the landing candidate 1f176444 · ORDER J.

"ORDER J" is TWO boards and the ledger keeps them apart, because they have different standing:
  * ORDER J (RULED)     = the owner-ruled tall/small sitter factor alone. R-TALLFACTOR is ADOPTED.
  * ORDER J (REFERENCE) = the cheapest setting that satisfies the owner's laws G1/G2/G3. IT FAILS THE
                          PREREGISTERED MATURE-ROW GATE J-TOL AND IS NOT CARRIED. It exists so the
                          owner can see, on real boards, what ~2% of veteran movement buys.

Legs, each priced as a REAL BOARD (a build, not an arithmetic split):
  leg TALL  = the ruled tall/small sitter factor alone
  leg S1    = the age-referenced projection bar alone at the reference dose
  leg RMX   = the remainder: the counterweight plus the interaction between the first two
The legs do NOT sum to the total and the residual is shown rather than hidden.

Pure JSON reads over boards already built by build_all37.sh — no engine run here.
"""
import json, os, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
O37 = SP + '/o37'
C31 = json.load(open(SP + '/cand31.json'))
assert C31['boards']['candidate'].startswith('fe6be9d6') and C31['boards']['live'].startswith('88ce647f')

TAGS = ['cand', 'tall', 's1', 'ref']
BP = {t: O37 + '/bb_%s/rl_after/rl_app_data.json' % t for t in TAGS}
MD5 = {t: hashlib.md5(open(BP[t], 'rb').read()).hexdigest() for t in TAGS}
B = {t: {r['key']: r for r in json.load(open(BP[t]))['active']} for t in TAGS}
print('boards:', {t: m[:8] for t, m in MD5.items()})
assert MD5['cand'].startswith('1f176444'), \
    'F3 FIRES: the dial-off rebuild is %s, not the landing candidate 1f176444 — HALT' % MD5['cand'][:8]

rows = []
for r in C31['rows']:
    k = r['key']
    if k not in B['cand']:
        continue
    b = B['cand'][k]
    vc, vt, v1, vf = (B[t][k]['v'] for t in TAGS)
    rows.append(dict(key=k, name=r['name'], pos=(b.get('gf') or b['grp']), age=b['age'],
                     pathway=r['pathway'], pick=r.get('pick'), g=r.get('g', 0), yr=r.get('yr'),
                     v0=r.get('v0', 0.0),
                     live=r['live'], cand31=r['cand'], landing=vc,
                     order_j_ruled=vt, order_j_ref=vf,
                     leg_tall=vt - vc, leg_s1=v1 - vc, leg_remix=vf - (v1 + vt - vc),
                     d_ruled_vs_landing=vt - vc, d_ref_vs_landing=vf - vc,
                     d_vs_cand31=vt - r['cand'], d_vs_live=vt - r['live']))
print('ledger rows: %d of %d C31 rows' % (len(rows), len(C31['rows'])))
tot = {f: sum(r[f] for r in rows) for f in
       ('live', 'cand31', 'landing', 'order_j_ruled', 'order_j_ref', 'leg_tall', 'leg_s1', 'leg_remix')}
print('totals:', {k: round(v) for k, v in tot.items()})

RM = [r for r in rows if r['d_ruled_vs_landing'] != 0]
RMM = [r for r in RM if r['age'] >= 24]
FM = [r for r in rows if r['d_ref_vs_landing'] != 0]
FMM = [r for r in FM if r['age'] >= 24]
print('\nORDER J (RULED, the tall factor): %d of %d rows move, %d of them aged 24+'
      % (len(RM), len(rows), len(RMM)))
print('ORDER J (REFERENCE, not carried) : %d of %d rows move, %d of them aged 24+'
      % (len(FM), len(rows), len(FMM)))

NAMED = ['harry-dean', 'cooper-duff-tytler', 'xavier-taylor', 'oskar-taylor', 'daniel-annable',
         'dylan-patterson', 'josh-smillie', 'chris-scerri', 'thomas-burton', 'milan-murdock',
         'will-green', 'toby-conway', 'steely-green', 'isaac-kako', 'alix-tauru', 'jedd-busslinger']
BYK = {r['key']: r for r in rows}
print('\n%-22s %4s %5s %4s %8s %8s %8s %9s %9s | %8s %8s %8s'
      % ('row', 'age', 'pick', 'g', 'live', 'C31', 'landing', 'J RULED', 'J REF',
         'leg TALL', 'leg S1', 'leg RMX'))
LED = []
for k in NAMED:
    r = BYK.get(k)
    if r is None:
        print('%-22s (not on the 804-row active board)' % k); continue
    LED.append(r)
    print('%-22s %4s %5s %4.0f %8d %8d %8d %9d %9d | %+8d %+8d %+8d'
          % (r['name'][:22], r['age'], r['pick'], r['g'], r['live'], r['cand31'], r['landing'],
             r['order_j_ruled'], r['order_j_ref'], r['leg_tall'], r['leg_s1'], r['leg_remix']))

for lab, fld in (('ORDER J RULED (the tall factor)', 'd_ruled_vs_landing'),
                 ('ORDER J REFERENCE (not carried)', 'd_ref_vs_landing')):
    print('\nTOP 15 UP  — %s, vs the landing candidate:' % lab)
    for r in sorted(rows, key=lambda r: -r[fld])[:15]:
        print('  %-24s %3s %4s %5.0fg  %7d -> %7d  %+7d'
              % (r['name'][:24], r['age'], r['pick'], r['g'], r['landing'], r['landing'] + r[fld], r[fld]))
    print('TOP 15 DOWN — %s:' % lab)
    for r in sorted(rows, key=lambda r: r[fld])[:15]:
        print('  %-24s %3s %4s %5.0fg  %7d -> %7d  %+7d'
              % (r['name'][:24], r['age'], r['pick'], r['g'], r['landing'], r['landing'] + r[fld], r[fld]))

for lab, mv in (('RULED', RM), ('REFERENCE', FM)):
    A = collections.Counter(r['age'] for r in mv)
    print('\nage profile of the rows that move [%s]: %s' % (lab, dict(sorted(A.items()))))

os.makedirs(os.path.join(ROOT, 'docs', 'ledgers'), exist_ok=True)
json.dump(dict(order='ORDER J — the movers ledger, four boards with mechanism legs',
               standing=dict(ruled='ORDER J RULED = R-TALLFACTOR, the owner-ruled tall/small sitter '
                                   'factor alone',
                             reference='ORDER J REFERENCE = the cheapest law-satisfying setting; FAILS '
                                       'J-TOL, NOT CARRIED, NOTHING LANDS'),
               meta=dict(boards=dict(live=C31['boards']['live'], cand31=C31['boards']['candidate'],
                                     landing=MD5['cand'], leg_tall=MD5['tall'], leg_s1=MD5['s1'],
                                     order_j_ref=MD5['ref'])),
               totals=tot, rows=rows, named=LED,
               n_moved_ruled=len(RM), n_mature_moved_ruled=len(RMM),
               n_moved_ref=len(FM), n_mature_moved_ref=len(FMM),
               age_profile_ruled={str(k): v for k, v in sorted(collections.Counter(r['age'] for r in RM).items())},
               age_profile_ref={str(k): v for k, v in sorted(collections.Counter(r['age'] for r in FM).items())}),
          open(os.path.join(ROOT, 'docs', 'ledgers', 'ORDER_J_MOVERS.json'), 'w'), indent=1, default=float)
print('\nwrote docs/ledgers/ORDER_J_MOVERS.json')
