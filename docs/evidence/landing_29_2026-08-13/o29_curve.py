#!/usr/bin/env python3
"""ORDER 29 -- STEP 3, THE MONOTONE HYBRID CURVE.

Composes the landed pvc_curve_v2.json from the ORDER-28 candidate (DERIVE28.json::candidate) and
scores PREREG P5 and P6.  Writes to a path given on the command line; the artifact is NOT installed
into the checkout by this script.

  usage:  python3 o29_curve.py <out.json> [--numeraire]
          --numeraire   also re-stamp the numeraire block for the new pooled head (STEP 6)
"""
import os, sys, json, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
LIVE = ROOT + '/engine/rl_after/pvc_curve_v2.json'
D28 = ROOT + '/docs/evidence/grace_adoption_2026-08-13/DERIVE28.json'

OUT = sys.argv[1]
DO_NUM = '--numeraire' in sys.argv

LOG = []
def P(s=''):
    print(s); LOG.append(s)

art = json.loads(open(LIVE).read(), object_pairs_hook=collections.OrderedDict)
cand = json.load(open(D28))['candidate']

P("=" * 116)
P("ORDER 29  --  STEP 3, THE MONOTONE HYBRID CURVE  (P5 / P6)")
P("=" * 116)

allin = {int(k): float(v) for k, v in cand['allin'].items()}
pre = {int(k): float(v) for k, v in cand['allin_pre'].items()}
nper = {int(k): float(v) for k, v in cand['nper'].items()}
curve = {k: int(round(allin[k])) for k in sorted(allin)}

# ------------------------------------------------------------------ P5
P()
P("P5 -- THE CURVE, RE-CHECKED RATHER THAN ASSUMED")
P("-" * 116)
P("  pre-anchor head        %.10f" % cand['head'])
P("  anchor factor          %.12f" % cand['anchor_factor'])
P("  head x factor          %.6f   (== the published pin 3000)" % (cand['head'] * cand['anchor_factor']))
P("  domain                 %d..%d  (%d entries)" % (min(curve), max(curve), len(curve)))

SPOT = {1: 3000, 2: 2668, 3: 2569, 5: 1804, 7: 1319, 10: 1319, 15: 812, 20: 812,
        30: 607, 40: 479, 50: 274, 64: 179}
bad = {k: (curve[k], v) for k, v in SPOT.items() if curve[k] != v}
P("  P5 spot values (int)   %s" % {k: curve[k] for k in sorted(SPOT)})
P("  P5 predicted           %s" % SPOT)
P("  spot verdict           %s" % ("ALL 12 MATCH -- HELD" if not bad else "MISMATCH %s" % bad))
assert not bad

seam = None
for i, m in enumerate(cand['meth'], 1):
    if m == 'LL': seam = i
    else: break
_lastLL = max(i for i, m in enumerate(cand['meth'], 1) if m == 'LL')
P("  seam pick (last pure-loclin)  %d      P5 predicted 56    %s"
  % (_lastLL, "HELD" if _lastLL == 56 else "BREACH"))
_tail = [i for i, m in enumerate(cand['meth'], 1) if m != 'LL']
P("  tail zone                     %d-%d    P5 predicted 57-64 %s"
  % (min(_tail), max(_tail), "HELD" if (min(_tail), max(_tail)) == (57, 64) else "BREACH"))
P("  pick 64                       %d      P5 predicted the 179-class  %s"
  % (curve[64], "HELD" if abs(curve[64] - 179) <= 1 else "BREACH"))

# THE DESCENT RE-CHECK.  Two DIFFERENT properties, and the difference is the whole of §3b:
asc = [k for k in range(1, 64) if curve[k + 1] > curve[k]]
flat = [k for k in range(1, 64) if curve[k + 1] == curve[k]]
P()
P("  NON-INCREASING (no ascent)          %s   ascents: %s"
  % ("PASS" if not asc else "FAIL", asc or "none"))
P("  STRICTLY DECREASING (no plateau)    %s   plateau steps: %d at picks %s"
  % ("PASS" if not flat else "FAIL", len(flat), flat))
P("  the artifact's live self-declaration r104_9_strict_descent = %r" % art.get('r104_9_strict_descent'))
P()
P("  ** THE CURVE IS NON-INCREASING BUT NOT STRICTLY DECREASING. **")
P("  PAVA (Ruling C) replaces each violating block by its weighted mean, so a pooled block IS a")
P("  plateau BY CONSTRUCTION.  picks 6-11 pool to %d and picks 15-20 pool to %d."
  % (curve[6], curve[15]))

# ------------------------------------------------------------------ P6 conservation
P()
P("P6 -- THE CONSERVATION LEDGER")
P("-" * 116)
wpre = sum(nper[k] * pre[k] for k in pre)
wpost = sum(nper[k] * allin[k] for k in allin)
ppre = sum(pre.values()); ppost = sum(allin.values())
pint = sum(curve.values())
P("  %-46s %16s %16s %14s" % ("quantity", "pre", "post", "drift"))
P("  %-46s %16.4f %16.4f %14.3e" % ("weighted  sum n_p * v_p  (PAVA step)", wpre, wpost, abs(wpost / wpre - 1)))
P("  %-46s %16.4f %16.4f %13.4f%%" % ("plain     sum v_p       (PAVA step)", ppre, ppost, 100.0 * (ppost / ppre - 1)))
P("  %-46s %16.4f %16d %13.4f%%" % ("plain sum, float -> int (artifact schema)", ppost, pint, 100.0 * (pint / ppost - 1)))
P("  %-46s %16.4f %16.4f %14s" % ("anchor (pick 1)", pre[1], allin[1], "unmoved"))
P()
P("  P6 predicted: weighted conserved to 0.000e+00        MEASURED %.3e   %s"
  % (abs(wpost / wpre - 1), "HELD" if abs(wpost / wpre - 1) < 1e-12 else "BREACH"))
P("  P6 predicted: plain conserved to 0.0000%%             MEASURED %+.4f%%   %s"
  % (100.0 * (ppost / ppre - 1), "HELD" if abs(ppost / ppre - 1) < 5e-6 else "BREACH"))
P("  P6 predicted: int-rounding drift < 0.05%%, PRINTED    MEASURED %+.4f%%   %s"
  % (100.0 * (pint / ppost - 1), "HELD" if abs(pint / ppost - 1) < 5e-4 else "BREACH"))
P("  P6 predicted: anchor untouched by boundary+monotone  %s"
  % ("HELD" if pre[1] == allin[1] else "BREACH"))
P("  The int drift is PRINTED, NOT ABSORBED: no compensating adjustment is applied anywhere.")

# ------------------------------------------------------------------ compose the artifact
art['curve'] = collections.OrderedDict((str(k), curve[k]) for k in sorted(curve))
art['curve_md5'] = hashlib.md5(
    json.dumps(art['curve'], sort_keys=True, separators=(',', ':')).encode()).hexdigest()[:8]

if DO_NUM:
    H = float(cand['head'])
    pin = float(art['numeraire']['published_pin'])
    old = dict(art['numeraire'])
    s_new = pin / H
    art['numeraire'] = collections.OrderedDict([
        ('_doc', old['_doc']),
        ('basis', 'pooled'),
        ('pooled_head_pre_scale', H),
        ('published_pin', pin),
        ('s', s_new),
    ])
    P()
    P("STEP 6 -- THE NUMERAIRE RE-PIN")
    P("-" * 116)
    P("  pooled_head_pre_scale  %.10f -> %.10f" % (old['pooled_head_pre_scale'], H))
    P("  published_pin          %.1f -> %.1f  (unmoved: the standing law pins pick 1 = 3000)"
      % (old['published_pin'], pin))
    P("  s = pin / H            %.16f -> %.16f" % (old['s'], s_new))
    P("  player re-denomination ratio  s_new / s_old = %.12f" % (s_new / old['s']))
    P("  E6 coherence: |pin/H - s| = %.3e   (_load_numeraire halts above 1e-9)"
      % abs(pin / H - s_new))

json.dump(art, open(OUT, 'w'), indent=1)
P()
P("  written: %s   curve_md5 %s" % (OUT, art['curve_md5']))
open(HERE + '/CURVE29_out.txt', 'w').write("\n".join(LOG) + "\n")
