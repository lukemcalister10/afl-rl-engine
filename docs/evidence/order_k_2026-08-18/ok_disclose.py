#!/usr/bin/env python3
"""ORDER K — the LEVER disclosure the engine emits under the dial, and the fade table the packet
quotes. Loads the engine module ONCE (a second in-process exec is not safe), reads the LIVE exponent
from the module itself, and reconstructs ORDER J's WIRED exponent from the module's OWN constants —
so the before/after comparison cannot drift from what the engine actually carries. Builds no board."""
import io, os, sys, math, contextlib, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
os.environ.update(
    PYTHONHASHSEED='0', OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1',
    NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1',
    RL_REPO=ROOT, RL_FV=os.path.join(ROOT, 'engine', 'forward_valuation'),
    RL_V0SURF_PKL=os.path.join(ROOT, 'data', 'v0surf.pkl'),
    RL_GAMMA='1.0', RL_PICK1='3000', RL_RUCK_TAX='0.25', RL_RECENCY_DECAY='0.72',
    RL_PRIOR_TREES='400', PAR_RAMPS='22',
    RL_O31='1', RL_O32='1', RL_O36='1', RL_O36_LAM_S1='0.40', RL_O36_TALL='1',
    RL_O36_FLOORFIX='1', RL_O36_KAPPA='0.20', RL_O36_GAMMA='8.0', RL_O36_ETA='0.50',
    RL_O36_GAMMA_D='14.0', RL_O36_LAMBDA='1.08')
sys.path[:0] = [os.path.join(ROOT, 'engine', 'rl_after'), ROOT, os.path.join(ROOT, 'vendor')]
_cwd = os.getcwd()
os.chdir(os.path.join(ROOT, 'engine', 'rl_after'))
buf = io.StringIO()
NS = {}
with contextlib.redirect_stdout(buf):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], NS)
os.chdir(_cwd)
print('=' * 112)
print("THE ENGINE'S OWN DISCLOSURE, RL_O36_FLOORFIX=1 (the default, the lane the decision board is built on)")
print('=' * 112)
for ln in buf.getvalue().splitlines():
    if ('LEVER' in ln or 'ORDER K' in ln or 'ORDER I LIVE' in ln or 'active rows sit' in ln):
        print('  ' + ln)

kp = NS['o35_kappa_at']; kK = NS['o36_kappa_at']
D2 = NS['O36_D2_FULL']
TG0, TG1, HT, SNJ = NS['O36_TG0'], NS['O36_TG1'], NS['O36_HTALL'], NS['O36_SNORM']
CLIP = NS['O35_CLIP']
def kJ(p, tall):     # ORDER J's WIRED exponent, from the engine's own constants
    p = max(1.0, min(64.0, float(p)))
    return min(CLIP[1], max(CLIP[0], (TG0 + TG1 * math.log(p) + (HT if tall else 0.0)) / SNJ))

print('\n' + '=' * 112)
print('THE FADE EXPONENT AND THE FADE, PICK BY PICK.  fade = D2^kappa at the ruled depth-2 cell '
      '%.7f.' % D2)
print('THE BASE IS BELOW 1, SO A LOWER EXPONENT IS A LIGHTER FADE (a smaller discount, a higher price).')
print('=' * 112)
print('%4s | %8s | %8s %8s | %8s %8s | %10s %10s | %10s %10s'
      % ('pick', 'pooled', 'small J', 'small K', 'tall J', 'tall K',
         'smlJ vs pre', 'smlK vs pre', 'tallJ vs pre', 'tallK vs pre'))
TAB = []
for p in list(range(1, 26)) + [30, 40, 50, 53, 64]:
    a, b, c, d, e = kp(p), kJ(p, False), kK(p, False), kJ(p, True), kK(p, True)
    row = dict(pick=p, pooled=a, smallJ=b, smallK=c, tallJ=d, tallK=e,
               smallJ_vs_pool=100 * (D2 ** b / D2 ** a - 1), smallK_vs_pool=100 * (D2 ** c / D2 ** a - 1),
               tallJ_vs_pool=100 * (D2 ** d / D2 ** a - 1), tallK_vs_pool=100 * (D2 ** e / D2 ** a - 1))
    TAB.append(row)
    print('%4d | %8.4f | %8.4f %8.4f | %8.4f %8.4f | %+9.2f%% %+9.2f%% | %+9.2f%% %+9.2f%%'
          % (p, a, b, c, d, e, row['smallJ_vs_pool'], row['smallK_vs_pool'],
             row['tallJ_vs_pool'], row['tallK_vs_pool']))
lj = [p for p in range(1, 65) if D2 ** kJ(p, False) > D2 ** kp(p) + 1e-12]
lk = [p for p in range(1, 65) if D2 ** kK(p, False) > D2 ** kp(p) + 1e-12]
hj = [p for p in range(1, 65) if D2 ** kJ(p, True) < D2 ** kp(p) - 1e-12]
hk = [p for p in range(1, 65) if D2 ** kK(p, True) < D2 ** kp(p) - 1e-12]
print('\nK-FLOOR (a) — SMALLS MADE LIGHTER (the picks where a small pays LESS than his pre-factor value):')
print('  ORDER J, the wired floor : picks %s   <- THE DEFECT' % (lj or 'none'))
print('  ORDER K, the re-sited floor: %s' % ('picks %s' % lk if lk else 'NONE — at no pick, for any row'))
print('K-FLOOR (d) — TALLS MADE HEAVIER (the ruled relief reversing):')
print('  ORDER J: %s   ORDER K: %s' % (hj or 'none', hk or 'none'))
tb = [p for p in range(1, 65) if abs(kK(p, True) - CLIP[0]) < 1e-12]
sb = [p for p in range(1, 65) if abs(kK(p, False) - kp(p)) < 1e-12]
s05 = [p for p in sb if abs(kp(p) - CLIP[0]) < 1e-12]
tbj = [p for p in range(1, 65) if abs(kJ(p, True) - CLIP[0]) < 1e-12]
sbj = [p for p in range(1, 65) if abs(kJ(p, False) - CLIP[0]) < 1e-12]
print('\nWHERE THE FLOOR STILL BINDS, AND FOR WHOM:')
print('  ORDER J  TALL on 0.5 : picks %d-%d (%d)   SMALL on 0.5 : picks %d-%d (%d)'
      % (min(tbj), max(tbj), len(tbj), min(sbj), max(sbj), len(sbj)))
print('  ORDER K  TALL on 0.5 : picks %d-%d (%d)' % (min(tb), max(tb), len(tb)))
print('  ORDER K  SMALL on the re-sited floor (his own pooled exponent): picks %d-%d (%d)'
      % (min(sb), max(sb), len(sb)))
print('           ...of which also on the 0.5 hard floor, because the pooled curve is itself clipped '
      'there: picks %d-%d (%d)' % (min(s05), max(s05), len(s05)))
print('\ns_norm            ORDER J %.16f   ORDER K %.16f' % (SNJ, NS['O36_SNORM_K']))
print('identity residual ORDER K %.3e   (build-failing above 1e-9)' % NS['O36_IDENT_RESID'])
print('h_TALL            %.16f  — UNCHANGED from the owner-ruled value' % HT)
json.dump(dict(table=TAB, lighter_J=lj, lighter_K=lk, heavier_tall_J=hj, heavier_tall_K=hk,
               tall_floor_picks_K=tb, small_floor_picks_K=sb, small_floor_at_05_K=s05,
               tall_floor_picks_J=tbj, small_floor_picks_J=sbj,
               s_norm_J=SNJ, s_norm_K=NS['O36_SNORM_K'], resid_K=NS['O36_IDENT_RESID'],
               h_TALL=HT, D2=D2), open(os.path.join(HERE, 'FADE_K.json'), 'w'), indent=1)
