#!/usr/bin/env python3
"""ORDER S — FALSIFIER S-F3. THE FIX A DECOMPOSITION IDENTITY, UNDER EVERY ORDER S DIAL.

FIX A monotonises the pedigree leg in entry price by running the maximum of

    psi(x) = x - LAMBDA*A(g)*T( s_P(x) )        over x = ln(v0)

and it can only be correct if the reconstruction `s_P(x)` it uses AGREES WITH THE ENGINE'S OWN
`o37_surplus` at the row's actual entry price. ORDER Q built that identity on the games-weighted
surplus. THIS ORDER CHANGES THE SURPLUS TWICE — the recency weight (RL_O40_RECW) and the mature
premium (RL_O40_PGMAT) — so the identity has to be re-proved, not assumed.

It is proved here on EVERY REAL ROW, at the row's own entry price, on every dial line priced.

  usage: python3 os_identity.py
"""
import io, os, sys, math, json, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import os_lib as L

SPECS = [
    ('SB1', dict(RL_O37='1', RL_O38B1='1')),
    ('SAB1', dict(RL_O37='1', RL_O38A='1', RL_O38B1='1')),
    ('SW47', dict(RL_O37='1', RL_O38B1='1', RL_O40_RECW='0.47')),
    ('SW47A', dict(RL_O37='1', RL_O38A='1', RL_O38B1='1', RL_O40_RECW='0.47')),
    ('SC20A', dict(RL_O37='1', RL_O38A='1', RL_O38B1='1',
                   RL_O40_CAPFORM='smooth', RL_O40_CAPPCT='20')),
    ('SM', dict(RL_O37='1', RL_O38B1='1', RL_O40_PGMAT='1')),
    ('SMA', dict(RL_O37='1', RL_O38A='1', RL_O38B1='1', RL_O40_PGMAT='1')),
    ('SALL', dict(RL_O37='1', RL_O38A='1', RL_O38B1='1', RL_O40_RECW='0.47',
                  RL_O40_CAPFORM='smooth', RL_O40_CAPPCT='20', RL_O40_PGMAT='1')),
]
TAG = sys.argv[1] if len(sys.argv) > 1 else None
LL = []


def P(s=''):
    print(s); LL.append(str(s))


P('=' * 118)
P('ORDER S — FALSIFIER S-F3. THE FIX A DECOMPOSITION IDENTITY UNDER EVERY ORDER S DIAL.')
P('=' * 118)
P('  For every real row: does o38_parts\' reconstruction of the surplus at the row\'s OWN entry price')
P('  equal the engine\'s own o37_surplus, to 1e-9? If it does not, FIX A is monotonising the wrong')
P('  object and every A-on board in this packet is wrong.')
P()
P('  %-8s %8s %14s %14s   %s' % ('dial line', 'rows', 'worst |diff|', 'verdict', 'dials'))
OUT = {}
for tag, dials in SPECS:
    if TAG and tag != TAG:
        continue
    NS = L.load(**dials)
    import rl_model as MA
    parts = NS['o38_parts']; surp = NS['o37_surplus']
    pg_at = NS['o38_pg_at']
    pgm_at = NS.get('o40_pg_at')
    PLF = NS['_PL_F']
    d0 = NS['day0_v0']
    pgmat = bool(NS.get('_O40_PGMAT'))
    worst = 0.0; n = 0; wk = None
    for p in MA.players:
        pr = parts(p, 2026)
        s = surp(p, 2026)
        v = d0(p)
        if pr is None or s is None or v is None:
            continue
        OUTv, wT, wS, wTm, wSm = pr
        x = math.log(round(float(v) * PLF, 1))
        if pgmat:
            sx = OUTv - ((wT - wTm) * pg_at(x, 'TALL') + wTm * pgm_at(x, 'TALL')
                         + (wS - wSm) * pg_at(x, 'SMALL') + wSm * pgm_at(x, 'SMALL'))
        else:
            sx = OUTv - (wT * pg_at(x, 'TALL') + wS * pg_at(x, 'SMALL'))
        d = abs(sx - s)
        n += 1
        if d > worst:
            worst = d; wk = p.get('key')
    ok = worst < 1e-9
    OUT[tag] = dict(rows=n, worst=worst, pass_=bool(ok), dials=dials)
    P('  %-8s %8d %14.3e %14s   %s'
      % (tag, n, worst, 'PASS' if ok else '**S-F3 FIRES**',
         ' '.join('%s=%s' % kv for kv in sorted(dials.items()))))
    if not ok:
        P('        worst row key: %s' % wk)
    # a fresh process is required per dial line; this loop is only valid for ONE line per run.
    break
P()
if TAG is None:
    P('  NOTE: the engine can only be loaded once per process, so this file measures ONE dial line')
    P('  per run. run_identityS.sh drives it once per line, strictly sequentially.')
json.dump(OUT, open(os.path.join(HERE, 'IDENTITY_S_%s.json' % (TAG or 'first')), 'w'), indent=1)
open(os.path.join(HERE, 'IDENTITY_S_%s_out.txt' % (TAG or 'first')), 'w').write('\n'.join(LL) + '\n')
