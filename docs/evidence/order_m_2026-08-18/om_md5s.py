#!/usr/bin/env python3
"""ORDER M — the board md5 roll-call, recomputed from the built boards on disk.

DISCLOSURE, and it is this seat's own error rather than a tool problem: BUILD_LADDER_M_out.txt is
TRUNCATED. This seat ran `git stash` on that file to clear a working tree for a push while the ladder
build was still writing to it, and the stash-pop reverted the writes that had landed in between. The
BOARDS are unaffected — they are on disk, they were built by the same bbM.sh as every other board in
this order, and their md5s are recomputed here from the files themselves. What was lost is the tail of
a LOG, not a result. It is recorded here rather than quietly regenerated.
"""
import hashlib, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
OM = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/om'
TAGS = [('cand', 'dial off — the landing candidate', '-', '-', '-'),
        ('K', "ORDER K's ruled setting, rebuilt here", '0.40', '0.20', '0.50'),
        ('s1', 'the age bar alone, tall factor removed', '0.40', 'repair', 'repair'),
        ('M0', "ORDER K's knobs with ETA = 0", '0.40', '0.20', '0.00'),
        ('M0R', 'the determinism repeat of M0', '0.40', '0.20', '0.00'),
        ('MLO', 'the coolest eta=0 point in the grid', '0.00', '0.15', '0.00'),
        ('MMIN', 'the smallest legal eta anywhere', '0.00', '0.20', '0.31'),
        ('E10', 'ladder A', '0.40', '0.20', '0.10'),
        ('E20', 'ladder A', '0.40', '0.20', '0.20'),
        ('E30', 'ladder A', '0.40', '0.20', '0.30'),
        ('E40', 'ladder A', '0.40', '0.20', '0.40'),
        ('F20', 'ladder B — the legal frontier', '0.20', '0.20', '0.39'),
        ('F60', 'ladder B — the legal frontier', '0.60', '0.20', '0.64'),
        ('F70', 'ladder B — the legal frontier', '0.70', '0.20', '0.72'),
        ('KMAX', 'the maximum-kappa control (gamma_u 16)', '0.00', '0.60', '0.00'),
        ('KMX4', 'the maximum-kappa control (gamma_u 16)', '0.40', '0.60', '0.00')]
L = []


def P(s=''):
    print(s); L.append(str(s))


P('=' * 104)
P('ORDER M — EVERY BOARD BUILT BY THIS ORDER, md5 RECOMPUTED FROM THE FILE ON DISK')
P('=' * 104)
P('  %-5s %-40s %6s %7s %6s  %s' % ('tag', 'what it is', 'dose', 'kappa', 'eta', 'md5'))
OUT = {}
for tag, what, dose, kap, eta in TAGS:
    p = OM + '/bb_%s/rl_after/rl_app_data.json' % tag
    if not os.path.exists(p):
        P('  %-5s %-40s %6s %7s %6s  NOT BUILT' % (tag, what, dose, kap, eta)); continue
    m = hashlib.md5(open(p, 'rb').read()).hexdigest()
    OUT[tag] = dict(md5=m, dose=dose, kappa=kap, eta=eta, what=what)
    P('  %-5s %-40s %6s %7s %6s  %s' % (tag, what, dose, kap, eta, m))
P()
P('  M1  dial-off = 1f176444          : %s'
  % ('PASS' if OUT['cand']['md5'].startswith('1f176444') else 'FAIL — M1 FIRES'))
P('  M2  ORDER K rebuilds to f3101883 : %s'
  % ('PASS' if OUT['K']['md5'].startswith('f3101883') else 'FAIL — M2 FIRES'))
P('  M3  determinism x2 on M0         : %s'
  % ('PASS' if OUT['M0']['md5'] == OUT['M0R']['md5'] else 'FAIL — M3 FIRES'))
P()
P('  DISCLOSURE: BUILD_LADDER_M_out.txt is TRUNCATED and this seat truncated it. A `git stash` was run')
P('  on that log file to clear the working tree for a push while the ladder build was still writing to')
P('  it; the stash-pop reverted the lines that had landed in between. The BOARDS are unaffected — they')
P('  are on disk, built by the same bbM.sh as every other board here, and their md5s are recomputed')
P('  above from the files themselves. A log tail was lost, not a result. It is written down rather')
P('  than quietly regenerated.')
json.dump(OUT, open(os.path.join(HERE, 'BOARDS_M.json'), 'w'), indent=1, sort_keys=True)
open(os.path.join(HERE, 'BOARDS_M_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote BOARDS_M.json / BOARDS_M_out.txt')
