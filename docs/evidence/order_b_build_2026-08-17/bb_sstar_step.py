#!/usr/bin/env python3
"""ORDER B: s* fixed-point step. Usage: bb_sstar_step.py <base_tag> <new_tag> [sstar_used]
Prints the tall-anchor (gf in KPD/KPF, age 23-26) aggregate board value of both builds and the
next s* iterate = sstar_used * (sumV_base / sumV_new)."""
import json, sys

SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o33'
base = json.load(open('%s/bb_%s/rl_after/rl_app_data.json' % (SP, sys.argv[1])))
new = json.load(open('%s/bb_%s/rl_after/rl_app_data.json' % (SP, sys.argv[2])))
used = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0


def vsum(D):
    sel = [r for r in D['active'] if (r.get('gf') or r['grp']) in ('KPD', 'KPF') and 23 <= r['age'] <= 26]
    return sum(r['v'] for r in sel), len(sel)


vb, nb = vsum(base)
vn, nn = vsum(new)
print('tall anchor rows 23-26: n base %d / new %d' % (nb, nn))
print('sum V base %.1f  new %.1f  new/base-1 = %+.4f%%' % (vb, vn, 100 * (vn / vb - 1)))
print('next s* iterate = %.6f' % (used * vb / vn))
