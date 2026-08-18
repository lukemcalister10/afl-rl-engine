#!/usr/bin/env python3
"""ORDER K — THE MOVERS LEDGER, over the four standing board columns plus the mechanism legs.

Columns: live 88ce647f · Candidate 31 fe6be9d6 · the landing candidate 1f176444 · ORDER K f3101883.

Legs, each priced as a REAL BOARD (a build, not an arithmetic split):
  leg TALL   = the owner-ruled tall/small sitter factor alone, with the ORDER K re-sited fade floor
  leg S1     = the age-referenced projection bar alone at the RULED dose 0.40
  leg CW     = the counterweight's own contribution: (S1 + counterweight) minus (S1 alone)
  leg FLOOR  = what the FADE FLOOR FIX itself is worth: (the factor, fixed floor) minus (the factor,
               Order J's wired floor). Negative on the seven smalls the defect was paying.
  residual   = ORDER K minus (landing + tall + S1 + CW) — the interaction between the levers, SHOWN
               rather than hidden. The legs do not sum to the total and the ledger says so.

Pure JSON reads over boards already built by build_allK.sh — no engine run here.
"""
import json, os, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
OK = SP + '/ok'
C31 = json.load(open(SP + '/cand31.json'))
assert C31['boards']['candidate'].startswith('fe6be9d6') and C31['boards']['live'].startswith('88ce647f')
TAGS = ['cand', 'tallJ', 'tallK', 's1', 'cw', 'K']
BP = {t: OK + '/bb_%s/rl_after/rl_app_data.json' % t for t in TAGS}
MD5 = {t: hashlib.md5(open(BP[t], 'rb').read()).hexdigest() for t in TAGS}
B = {t: {r['key']: r for r in json.load(open(BP[t]))['active']} for t in TAGS}
print('boards:', {t: m[:8] for t, m in MD5.items()})
assert MD5['cand'].startswith('1f176444'), \
    'K5 FIRES: the dial-off rebuild is %s, not the landing candidate 1f176444 — HALT' % MD5['cand'][:8]

TALLPOS = frozenset(('KPD', 'KPF', 'RUCK'))
rows = []
for r in C31['rows']:
    k = r['key']
    if k not in B['cand']:
        continue
    b = B['cand'][k]
    vc = B['cand'][k]['v']; vtJ = B['tallJ'][k]['v']; vtK = B['tallK'][k]['v']
    v1 = B['s1'][k]['v']; vw = B['cw'][k]['v']; vK = B['K'][k]['v']
    rows.append(dict(key=k, name=r['name'], pos=(b.get('gf') or b['grp']),
                     tall=(b.get('gf') or b['grp']) in TALLPOS,
                     age=b['age'], pathway=r['pathway'], pick=r.get('pick'), g=r.get('g', 0),
                     yr=r.get('yr'), v0=r.get('v0', 0.0), club=b.get('club'),
                     live=r['live'], cand31=r['cand'], landing=vc, orderk=vK,
                     leg_tall=vtK - vc, leg_s1=v1 - vc, leg_cw=vw - v1, leg_floor=vtK - vtJ,
                     residual=vK - (vc + (vtK - vc) + (v1 - vc) + (vw - v1)),
                     d_vs_landing=vK - vc, d_vs_cand31=vK - r['cand'], d_vs_live=vK - r['live']))
print('ledger rows: %d of %d C31 rows' % (len(rows), len(C31['rows'])))
tot = {f: sum(r[f] for r in rows) for f in
       ('live', 'cand31', 'landing', 'orderk', 'leg_tall', 'leg_s1', 'leg_cw', 'leg_floor', 'residual')}
print('totals:', {k: round(v) for k, v in tot.items()})

MV = [r for r in rows if r['d_vs_landing'] != 0]
MVM = [r for r in MV if r['age'] >= 24]
print('\nORDER K vs the landing candidate: %d of %d rows move, %d of them aged 24+'
      % (len(MV), len(rows), len(MVM)))
print('the FADE FLOOR FIX alone moves %d rows (%d board points net)'
      % (sum(1 for r in rows if r['leg_floor'] != 0), sum(r['leg_floor'] for r in rows)))

NAMED = ['harry-dean', 'cooper-duff-tytler', 'xavier-taylor', 'daniel-annable', 'dylan-patterson',
         'oskar-taylor', 'josh-smillie', 'will-brodie', 'campbell-chesser', 'james-leake',
         'tom-brown', 'sam-sturt', 'chris-scerri', 'thomas-burton', 'milan-murdock', 'will-green',
         'toby-conway', 'william-mccabe', 'alex-dodson', 'steely-green', 'isaac-kako', 'alix-tauru',
         'jedd-busslinger', 'noah-mraz', 'murphy-reid', 'taylor-goad']
BYK = {r['key']: r for r in rows}
print('\n%-22s %4s %5s %4s %8s %8s %8s %9s | %8s %8s %8s %8s %6s'
      % ('row', 'age', 'pick', 'g', 'live', 'C31', 'landing', 'ORDER K',
         'leg TALL', 'leg S1', 'leg CW', 'leg FLR', 'resid'))
for k in NAMED:
    r = BYK.get(k)
    if r is None:
        print('%-22s (not on the 804-row active board)' % k); continue
    print('%-22s %4s %5s %4.0f %8d %8d %8d %9d | %+8d %+8d %+8d %+8d %+6d'
          % (r['name'][:22], r['age'], r['pick'], r['g'], r['live'], r['cand31'], r['landing'],
             r['orderk'], r['leg_tall'], r['leg_s1'], r['leg_cw'], r['leg_floor'], r['residual']))

for nm, key, rev in (('TOP 20 UP', 'd_vs_landing', True), ('TOP 20 DOWN', 'd_vs_landing', False)):
    print('\n%s — ORDER K vs the landing candidate:' % nm)
    for r in sorted(MV, key=lambda x: (-x[key] if rev else x[key]))[:20]:
        print('  %-26s %-5s %3s %4s %3.0fg  %6d -> %6d  %+5d   [tall %+d · S1 %+d · CW %+d]'
              % (r['name'][:26], r['pos'], r['age'], r['pick'], r['g'], r['landing'], r['orderk'],
                 r['d_vs_landing'], r['leg_tall'], r['leg_s1'], r['leg_cw']))

print('\nage profile of the rows that move: %s'
      % dict(sorted(collections.Counter(r['age'] for r in MV).items())))
print('pathway profile: %s' % dict(collections.Counter(r['pathway'] for r in MV)))

out = dict(order='ORDER K — the movers ledger',
           meta=dict(boards=dict(live=C31['boards']['live'], cand31=C31['boards']['candidate'],
                                 landing=MD5['cand'], orderk=MD5['K'], leg_tallK=MD5['tallK'],
                                 leg_tallJ=MD5['tallJ'], leg_s1=MD5['s1'], leg_cw=MD5['cw']),
                     setting=dict(dose=0.40, kappa=0.20, gamma_u=8.0, eta=0.50, gamma_d=14.0,
                                  lam_rel=1.08, tall_factor='R-TALLFACTOR, ORDER K fade floor')),
           totals=tot, rows=rows)
os.makedirs(os.path.join(ROOT, 'docs', 'ledgers'), exist_ok=True)
json.dump(out, open(os.path.join(ROOT, 'docs', 'ledgers', 'ORDER_K_MOVERS.json'), 'w'),
          indent=1, sort_keys=True, default=float)
print('\nwrote docs/ledgers/ORDER_K_MOVERS.json')
