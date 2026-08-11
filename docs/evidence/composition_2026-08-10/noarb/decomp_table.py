"""PER-ITEM DECOMPOSITION of the main->FULL year-1 drop, on the canonical no-arb instrument.

The owner asked where year-1 players lost their value and deserves exact shares, not mechanism prose.

METHOD — the repo's own attribution method, single-item removal through a DECLARED kill-switch. Each
arm is FULL with exactly one item switched OFF, so (arm - FULL) is the amount that item was
contributing to the drop: switch it off, and you get that much back.

    share of item X = (yr1_noX - yr1_FULL) / (yr1_main - yr1_FULL)

THE SHARES DO NOT SUM TO 100% AND THAT IS NOT AN ERROR. Single-item removal measures each item in
the PRESENCE of all the others, and the items interact — A's blend, the surprise law and the sitter
cuts all act on the same thin-record neighbourhood. The sum and the interaction residual are BOTH
printed. A residual is a real property of a composed package, not a rounding failure, and it is
never silently normalised away.

Progression numbers are read from noarb_table_338.py's own json (the unmodified canonical script).
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
G = 'ALL picks 1-64'

# (label, human name, how it was removed)
ARMS = [
    ('noA',   "ITEM A — the year-1+ anchor blend", 'RL_ITEM_A=0'),
    ('noSUR', "the surprise law",                  'RL_SUR_W=0'),
    ('noH',   "ITEM H — the sitter cuts",          'RL_ITEM_H=0'),
    ('no336', "the #336 reference layer",          'revert of 9a8bbd9 (no declared kill-switch)'),
]

L = []
def P(s=''):
    print(s); L.append(s)


def load(v):
    p = os.path.join(HERE, 'table_%s.json' % v)
    return json.load(open(p)) if os.path.exists(p) else None


def rr(t, g=G):
    return {r['N']: r['ratio_meanN_over_mean0'] for r in t['groups'][g]['rows']}


def main():
    need = ['main', 'FULL'] + [a for a, _, _ in ARMS]
    T = {v: load(v) for v in need}
    miss = [v for v in need if T[v] is None]
    if miss:
        print('MISSING TABLES: %s' % ', '.join(miss)); return 2

    m, f = rr(T['main']), rr(T['FULL'])
    drop1 = f[1] - m[1]
    drop4 = f[4] - m[4]

    P('=' * 100)
    P('PER-ITEM DECOMPOSITION OF THE YEAR-1 DROP — canonical no-arb instrument')
    P('=' * 100)
    P('  instrument : noarb_table_338.py UNMODIFIED · 1197 ND teaching entrants · pooled book ratio')
    P('  method     : single-item removal through a declared kill-switch; each arm is FULL with')
    P('               exactly one item OFF, so (arm - FULL) is what that item was contributing.')
    P()
    P('  main  yr1 %.4f   yr4 %.4f' % (m[1], m[4]))
    P('  FULL  yr1 %.4f   yr4 %.4f' % (f[1], f[4]))
    P('  THE DROP TO EXPLAIN: yr1 %+.4f (%+.1f%%)   yr4 %+.4f (%+.1f%%)'
      % (drop1, 100 * (f[1] / m[1] - 1), drop4, 100 * (f[4] / m[4] - 1)))
    P()
    P('  %-34s %9s %9s %11s %9s %11s'
      % ('item removed', 'yr1', 'gives back', 'share yr1', 'yr4', 'share yr4'))
    P('  ' + '-' * 88)
    s1 = s4 = 0.0
    rows = []
    for lab, nm, how in ARMS:
        r = rr(T[lab])
        b1, b4 = r[1] - f[1], r[4] - f[4]
        sh1 = -b1 / drop1 if drop1 else float('nan')
        sh4 = -b4 / drop4 if drop4 else float('nan')
        s1 += sh1; s4 += sh4
        rows.append((lab, nm, how, r[1], b1, sh1, r[4], b4, sh4))
        P('  %-34s %9.4f %+9.4f %10.1f%% %9.4f %10.1f%%' % (nm, r[1], b1, 100 * sh1, r[4], 100 * sh4))
    P('  ' + '-' * 88)
    P('  %-34s %9s %9s %10.1f%% %9s %10.1f%%' % ('SUM OF SHARES', '', '', 100 * s1, '', 100 * s4))
    P('  %-34s %9s %9s %10.1f%% %9s %10.1f%%'
      % ('INTERACTION RESIDUAL', '', '', 100 * (1 - s1), '', 100 * (1 - s4)))
    P()
    P('  The residual is the part of the drop that no single item owns alone — the amount that exists')
    P('  only because the items are composed together. It is reported, not normalised away.')
    P()

    # the ranking, stated plainly
    rk = sorted(rows, key=lambda z: -z[5])
    P('=' * 100)
    P('### THE ANSWER TO THE OWNER\'S QUESTION, RANKED')
    P('=' * 100)
    P('  "Where did year-1 players lose their value?" — largest contributor first:')
    P()
    for i, (lab, nm, how, y1, b1, sh1, y4, b4, sh4) in enumerate(rk, 1):
        P('  %d. %-36s %5.1f%% of the year-1 drop   [%s]' % (i, nm, 100 * sh1, how))
    P()
    top = rk[0]
    P('  The seat\'s arithmetic predicted ITEM A dominates via the symmetric blend at fade weight')
    P('  ~0.36. On the measurement the largest single contributor is %s at %.1f%% of the'
      % (top[1], 100 * top[5]))
    P('  year-1 drop — %s.'
      % ('CONFIRMED' if top[0] == 'noA' else 'REFUTED: the prediction named ITEM A, the measurement does not'))
    P()
    P('  A NOTE ON #336, because its arm is not like the others. #336 has NO declared kill-switch,')
    P('  and it landed as a mid-stack commit (9a8bbd9) with later work built on top, so it cannot be')
    P('  removed by git ref either. Its arm is a REVERT of that commit in a throwaway worktree —')
    P('  never pushed, never merged. The revert applied cleanly (678 lines out, the exact inverse of')
    P('  the 678 in) and touches only par_build.py and rl_model.py, and the engine head references')
    P('  none of the removed symbols. That the project has an item this large with no kill-switch is')
    P('  itself worth recording: every other item in this act can be ablated by dial, and this one')
    P('  cannot.')

    json.dump({x[0]: dict(yr1=x[3], give_back_yr1=x[4], share_yr1=x[5],
                          yr4=x[6], give_back_yr4=x[7], share_yr4=x[8]) for x in rows},
              open(os.path.join(HERE, 'DECOMP.json'), 'w'), indent=1)
    open(os.path.join(HERE, 'DECOMP.txt'), 'w').write('\n'.join(L) + '\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
