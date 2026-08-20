#!/usr/bin/env python3
"""ORDER 29 -- STEP 7 / PREREG P12: THE PRINTED-DAY-0 ASSERT ON FRESH ENTRANTS.

P12: for every FRESH entrant, printed day-0 price == derived v0 x numeraire, to the artifact's
rounding; and the four legs (_uncomp_prod, pedigree-pole blend, ev/raw_ev, L7) are verified to
COLLAPSE on fresh entrants. The legs are NOT rewired in this act (deferred whole to the
consumption-rewire act, owner-ruled) -- this VERIFIES the collapse, it does not implement it.

  usage: python3 o29_day0.py <board.json>
"""
import os, sys, json, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
BOARD = sys.argv[1] if len(sys.argv) > 1 else ROOT + '/engine/rl_after/rl_app_data.json'

LOG = []
def P(s=''):
    print(s); LOG.append(s)

b = json.load(open(BOARD))
art = json.load(open(ROOT + '/engine/rl_after/pvc_curve_v2.json'))
curve = {int(k): int(v) for k, v in art['curve'].items()}
NUM = art['numeraire']

P("=" * 112)
P("ORDER 29  --  STEP 7 / P12: THE PRINTED DAY-0 ASSERT ON FRESH ENTRANTS")
P("=" * 112)
P()
P("  board            %s" % os.path.basename(BOARD))
P("  numeraire        s %.16f   head %.10f   pin %.1f"
  % (NUM['s'], NUM['pooled_head_pre_scale'], NUM['published_pin']))

# A FRESH entrant: on the board, zero career games, and a national-draft pick inside the curve.
rows = b['active']
fresh = [r for r in rows if (r.get('cg') or 0) == 0 and r.get('ty') == 'ND'
         and r.get('pk') and 1 <= int(r['pk']) <= 64]
P()
P("  FRESH ENTRANTS (board rows, zero career games, ND pick 1..64):  %d" % len(fresh))
assert fresh, 'no fresh entrants found — the assert would be vacuous'

# ---- THE COLLAPSE. On a fresh entrant every production-side leg has no input, so the printed price
#      must be the ladder's own value at his pick. That is the collapse P12 names, and it is the
#      testable form of "printed day-0 == derived v0 x numeraire": the SHIPPED ladder IS raw x s, so
#      the numeraire is already inside curve[pick] and must not be applied twice.
P()
P("  THE COLLAPSE, STATED BEFORE IT IS MEASURED. On a fresh entrant the production legs have no")
P("  input: _uncomp_prod has no games, the pedigree-pole blend sits at the pedigree pole, ev/raw_ev")
P("  carries no realised season, and L7 is a display re-base. What is left is the entry anchor, and")
P("  for a national draftee that anchor IS the shipped ladder at his pick. The SHIPPED ladder is")
P("  already raw x s (that is what publishing s means), so the numeraire is ALREADY INSIDE")
P("  curve[pick] -- applying it again would be the double-count the E6 design exists to prevent.")
P()
P("  %-26s %5s %8s %10s %10s %9s" % ('row', 'pick', 'printed', 'curve[pk]', 'diff', 'ratio'))
bad = []
for r in sorted(fresh, key=lambda x: int(x['pk']))[:24]:
    pk = int(r['pk']); pr = r['v']; cv = curve[pk]
    P("  %-26s %5d %8d %10d %10d %9.4f" % (r['key'], pk, pr, cv, pr - cv, (pr / cv) if cv else 0))
allf = []
for r in fresh:
    pk = int(r['pk']); pr = r['v']; cv = curve[pk]
    allf.append((r['key'], pk, pr, cv, pr - cv))
    if pr != cv: bad.append((r['key'], pk, pr, cv))
P()
P("  fresh entrants whose printed day-0 EQUALS the shipped ladder exactly: %d of %d"
  % (len(allf) - len(bad), len(allf)))
if bad:
    P()
    P("  THE ROWS THAT DO NOT COLLAPSE TO THE LADDER, every one of them, with its gap:")
    P("  %-26s %5s %10s %10s %10s %9s" % ('row', 'pick', 'printed', 'curve[pk]', 'diff', 'ratio'))
    for k, pk, pr, cv in sorted(bad, key=lambda t: t[1]):
        P("  %-26s %5d %10d %10d %10d %9.4f" % (k, pk, pr, cv, pr - cv, (pr / cv) if cv else 0))
    _r = [pr / cv for _k, _pk, pr, cv in bad if cv]
    P()
    P("  ratio printed/ladder over the non-collapsing rows: min %.4f  max %.4f  mean %.4f"
      % (min(_r), max(_r), sum(_r) / len(_r)))

P()
P("  E6 COHERENCE, re-asserted on the artifact the board was built from:")
P("     published_pin / pooled_head_pre_scale = %.16f" % (NUM['published_pin'] / NUM['pooled_head_pre_scale']))
P("     published s                           = %.16f" % NUM['s'])
P("     |difference|                          = %.3e   (_load_numeraire HALTs above 1e-9)"
  % abs(NUM['published_pin'] / NUM['pooled_head_pre_scale'] - NUM['s']))
assert abs(NUM['published_pin'] / NUM['pooled_head_pre_scale'] - NUM['s']) < 1e-9

open(HERE + '/DAY0_29_out.txt', 'w').write("\n".join(LOG) + "\n")
json.dump({'n_fresh': len(allf), 'n_collapse_exact': len(allf) - len(bad),
           'noncollapsing': [{'key': k, 'pick': pk, 'printed': pr, 'ladder': cv} for k, pk, pr, cv in bad],
           'rows': [{'key': k, 'pick': pk, 'printed': pr, 'ladder': cv, 'diff': df} for k, pk, pr, cv, df in allf]},
          open(HERE + '/DAY0_29.json', 'w'), indent=1)
