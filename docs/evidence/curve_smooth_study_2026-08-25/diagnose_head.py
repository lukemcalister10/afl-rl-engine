#!/usr/bin/env python3
"""ADDENDUM -- THE CONSERVATION BREACH, DIAGNOSED, AND TWO POST-HOC REPAIR VARIANTS.

*** THESE VARIANTS WERE CONSTRUCTED AFTER SEEING CANDIDATE S's RESULT. ***
They are EXPLORATORY DIAGNOSTICS, NOT prereg'd candidates.  Neither may be treated as a landing
candidate without its own prereg written before it is re-run.  Reported here because the mechanism
behind the breach is the load-bearing finding, and showing the mechanism is repairable is part of
reporting it honestly.
"""
import os, json, math, collections
import numpy as np
import _common as C

OUT = C.OUT
LOG = []
def P(s=''):
    print(s); LOG.append(s)

PICKS = list(range(1, 65))
nd = C.nd_rows_1_64()
O28 = C.derive_curve(nd, PICKS, smooth=None)
S = C.derive_curve(nd, PICKS, smooth=5)
pl_ship = math.fsum(C.CURVE_SHIPPED[p] for p in PICKS)

P('=' * 132)
P('ADDENDUM -- THE +5.5% CONSERVATION BREACH, DIAGNOSED')
P('=' * 132)
P('  POST-HOC. Constructed after seeing candidate S. NOT prereg\'d. Diagnostics only.')
P()
P('THE MECHANISM, IN THREE NUMBERS')
P('  1. the hybrid curve entering the smoother is STEEPLY CONVEX at the head:')
P('       hybrid pick1 %.1f  pick2 %.1f  pick3 %.1f  (pick1 sits %.1f%% above the mean of 1-3)'
  % (O28['hyb'][0], O28['hyb'][1], O28['hyb'][2],
     100 * (O28['hyb'][0] / np.mean(O28['hyb'][:3]) - 1)))
P('  2. a CENTERED MOVING AVERAGE IS A LOCAL-CONSTANT SMOOTHER. On a convex, steeply falling head')
P('     it drags pick 1 DOWN, because every point it borrows -- even after edge replication -- is')
P('     southern and worth less:')
P('       pre-anchor head   ORDER 28 %.4f  ->  CANDIDATE S %.4f   = %+.4f%%'
  % (O28['head'], S['head'], 100 * (S['head'] / O28['head'] - 1)))
P('  3. the anchor pin pick1 = 3000 then DIVIDES THE WHOLE CURVE BY THAT DEPRESSED HEAD, so the')
P('     head depression is converted one-for-one into a whole-curve INFLATION:')
P('       anchor factor %.6f -> %.6f  = %+.4f%%   and the plain total moves %+.4f%%'
  % (O28['anchor_factor'], S['anchor_factor'], 100 * (S['anchor_factor'] / O28['anchor_factor'] - 1),
     100 * (math.fsum(S['allin'][p] for p in PICKS) / pl_ship - 1)))
P()
P('  THE TWO ARE THE SAME NUMBER. head move %+.4f%%  <->  anchor-factor move %+.4f%%'
  % (100 * (S['head'] / O28['head'] - 1), 100 * (S['anchor_factor'] / O28['anchor_factor'] - 1)))
P('  The smoothing pass does NOT remove value. It INFLATES the curve, and it does so entirely')
P('  through the anchor, not through the shape.')
P()
P('THIS IS A KNOWN DEFECT IN THIS ESTATE, WITH A RULED CURE')
P('  o26b_loclin.py docstring, THE DEFECT (verbatim):')
P('    "The shipped year-zero aggregator ... is a Gaussian kernel over log(pick) followed by a')
P('     weighted MEAN -- a LOCAL-CONSTANT estimator. ... At pick 1 every borrowed point is southern')
P('     and worth less, so the estimate is dragged DOWN (-7.1% measured). ... That is textbook')
P('     one-sided boundary bias, and a local-constant estimator cannot fix it: it averages the')
P('     slope instead of fitting it."')
P('  ORDER 26B-C2 cured that by replacing the local-CONSTANT step with a local-LINEAR one.')
P('  The 5-point moving average is ITSELF a local-constant smoother, so it RE-INTRODUCES at the')
P('  head exactly the bias 26B-C2 was ruled in to remove: measured -7.1%% then, %+.2f%% here.'
  % (100 * (S['head'] / O28['head'] - 1)))
P()

# ---- variant A: local-LINEAR smoother of the same 5-point width -----------------------------------
def savgol_lin(y, width=5):
    """A 5-point LOCAL-LINEAR smoother (Savitzky-Golay, polynomial order 1) with the SAME
    edge-replicate padding. This is the 26B-C2 fix applied to the smoothing stage: fit the local
    slope instead of averaging it, so a convex boundary is not dragged down."""
    y = np.asarray(y, float); half = width // 2
    yp = np.concatenate([[y[0]] * half, y, [y[-1]] * half])
    x = np.arange(-half, half + 1, dtype=float)
    out = []
    for i in range(len(y)):
        w = yp[i:i + width]
        b1 = np.sum(x * (w - w.mean())) / np.sum(x * x)
        out.append(w.mean() + b1 * 0.0)   # value AT the centre = intercept of the local line
        out[-1] = w.mean()                 # order-1 SG at centre of a symmetric window == mean
    return np.asarray(out)


# NOTE, stated rather than glossed: for an INTERIOR point a symmetric-window order-1 Savitzky-Golay
# filter is algebraically identical to the moving average. The two differ ONLY where the window is
# padded, i.e. at the boundary -- which is precisely where the defect lives. So the honest local-
# linear variant must EXTRAPOLATE the local line into the pad rather than replicate the endpoint.
def savgol_lin_extrap(y, width=5):
    y = np.asarray(y, float); half = width // 2
    n = len(y)
    x = np.arange(width, dtype=float)
    # build padding by extrapolating the local line fitted to the first/last `width` points
    def linfit(xs, ys):
        b1 = np.sum((xs - xs.mean()) * (ys - ys.mean())) / np.sum((xs - xs.mean()) ** 2)
        return ys.mean() - b1 * xs.mean(), b1
    a0, b0 = linfit(x, y[:width])
    a1, b1 = linfit(x, y[-width:])
    left = [a0 + b0 * t for t in range(-half, 0)]
    right = [a1 + b1 * t for t in range(width, width + half)]
    yp = np.concatenate([left, y, right])
    k = np.ones(width) / float(width)
    return np.convolve(yp, k, mode='valid')


def derive_with(vec_fn, label):
    nper = collections.Counter(r['pick'] for r in nd)
    ll, _e, _d = C.LL.kernel_loclin(nd, PICKS, C.HP.NMIN, C.HP.HMIN, C.HP.HMAX)
    wm, _ = C.HP.kernel_raw(nd, PICKS)
    hyb, meth, bw, z = C.hybrid_boundary(ll, wm, PICKS, end=64)
    pre = [float(x) for x in vec_fn(hyb)]
    wts_n = [float(nper[p]) for p in PICKS]
    post = [float(x) for x in C.SHIPPED_PAVA(pre, wts_n, increasing=False)]
    a1 = not (abs(post[0] - post[1]) < 1e-12 and abs(pre[0] - pre[1]) > 1e-12)
    a3 = all(post[i] >= post[i + 1] - 1e-12 for i in range(len(post) - 1))
    af = C.PIN1 / post[0]
    allin = {p: post[i] * af for i, p in enumerate(PICKS)}
    return dict(label=label, head=post[0], af=af, allin=allin, post=post, pre=pre,
                A1=a1, A3=a3, nper=dict(nper))


def hold1_ma(y, width=5):
    """VARIANT B: the ruled MA5, but the ANCHOR PICK IS HELD. Justification: pick 1 is a ruled PIN,
    not an estimate, and assert A1 already forbids the monotone stage from touching it. Holding it
    through the smoothing stage treats the pin consistently across both stages."""
    sm = C.l_smooth_ma(y, width)
    sm = np.asarray(sm, float).copy()
    sm[0] = y[0]
    return sm


VA = derive_with(lambda h: savgol_lin_extrap(h, 5), 'S-LL5  (local-LINEAR 5pt, 26B-C2 logic)')
VB = derive_with(lambda h: hold1_ma(h, 5), 'S-HOLD1 (ruled MA5, anchor pick held)')

P('TWO POST-HOC REPAIR VARIANTS')
P('  %-42s %11s %11s %11s %11s %8s' % ('variant', 'head', 'anchor f', 'plain tot', 'vs ship%', 'blocks'))
rows = [('ORDER 28 (ships)', O28['head'], O28['anchor_factor'], math.fsum(O28['allin'][p] for p in PICKS)),
        ('CANDIDATE S (prereg\'d, MA5)', S['head'], S['anchor_factor'], math.fsum(S['allin'][p] for p in PICKS)),
        (VA['label'], VA['head'], VA['af'], math.fsum(VA['allin'][p] for p in PICKS)),
        (VB['label'], VB['head'], VB['af'], math.fsum(VB['allin'][p] for p in PICKS))]
blk = {'ORDER 28 (ships)': len(C.blocks_of(O28['post'])),
       "CANDIDATE S (prereg'd, MA5)": len(C.blocks_of(S['post'])),
       VA['label']: len(C.blocks_of(VA['post'])), VB['label']: len(C.blocks_of(VB['post']))}
for lab, h, af, t in rows:
    P('  %-42s %11.2f %11.6f %11.1f %+10.4f%% %8d' % (lab, h, af, t, 100 * (t / pl_ship - 1), blk[lab]))
P()
P('  CONSERVATION vs THE 1%% TOLERANCE')
for lab, h, af, t in rows[1:]:
    d = 100 * (t / pl_ship - 1)
    P('    %-42s %+8.4f%%   %s' % (lab, d, 'WITHIN' if abs(d) <= 1.0 else 'BREACH'))
P()
P('  THE PLATEAUS AND THE CLIFF, ALL FOUR')
P('  %-42s %10s %10s %10s %10s' % ('variant', 'pick3', 'pick6', '3->6 drop', 'plateaus'))
for lab, res in (('ORDER 28 (ships)', O28), ("CANDIDATE S (prereg'd, MA5)", S),
                 (VA['label'], VA), (VB['label'], VB)):
    a = res['allin']
    P('  %-42s %10.1f %10.1f %9.1f%% %10d'
      % (lab, a[3], a[6], 100 * (a[6] / a[3] - 1), blk[lab]))
for lab, res in ((VA['label'], VA), (VB['label'], VB)):
    bl = C.blocks_of(res['post'])
    P('    %s blocks: %s' % (lab.split()[0],
                             ', '.join('%d-%d (n=%d)' % (PICKS[i], PICKS[j], j - i + 1) for i, j in bl)
                             or 'NONE -- strictly descending'))
P()
P('  A1 / A3 on both variants: S-LL5 A1=%s A3=%s   S-HOLD1 A1=%s A3=%s'
  % (VA['A1'], VA['A3'], VB['A1'], VB['A3']))
P()
P('  PER-PICK, ALL FOUR (headline picks)')
HEAD = [1, 2, 3, 4, 5, 6, 7, 10, 13, 15, 20, 25, 30, 40, 50, 64]
P('  %-42s %s' % ('variant', ''.join('%8d' % p for p in HEAD)))
P('  %-42s %s' % ('shipped integer curve', ''.join('%8.0f' % C.CURVE_SHIPPED[p] for p in HEAD)))
for lab, res in (('ORDER 28 float', O28), ("CANDIDATE S (MA5)", S), (VA['label'], VA), (VB['label'], VB)):
    P('  %-42s %s' % (lab, ''.join('%8.0f' % res['allin'][p] for p in HEAD)))
P()
P('READING')
P('  * The breach is NOT loss of value -- the curve INFLATES. The owner\'s stated fear ("shouldn\'t')
P('    remove total value") is not what happened; the failure is in the opposite direction, and it')
P('    is still outside the 1% band, so it is reported as a breach.')
P('  * The breach is entirely an ANCHOR artifact. Shape-wise the smoothing does what was asked.')
P('  * S-HOLD1 keeps the ruled MA5 and the ruled pin, cures the breach to %+.4f%%, and still removes'
  % (100 * (math.fsum(VB['allin'][p] for p in PICKS) / pl_ship - 1)))
P('    the cliff and most of the plateau. IT IS THE VARIANT WORTH PREREG\'ING NEXT -- but it has NOT')
P('    been prereg\'d, and this seat does not present it as a candidate.')

json.dump(dict(status='POST-HOC DIAGNOSTIC -- NOT PREREG\'D, NOT A CANDIDATE',
               mechanism='MA5 is a local-constant smoother; on the convex head it depresses pick 1 by '
                         '%.4f%%, and the pin=3000 converts that into a whole-curve inflation of %.4f%%'
                         % (100 * (S['head'] / O28['head'] - 1), 100 * (math.fsum(S['allin'][p] for p in PICKS) / pl_ship - 1)),
               cited_precedent='o26b_loclin.py -- the same local-constant boundary bias 26B-C2 was ruled in to cure',
               variants={
                   'ORDER28': dict(head=O28['head'], anchor_factor=O28['anchor_factor'],
                                   plain_total=math.fsum(O28['allin'][p] for p in PICKS),
                                   curve={str(p): O28['allin'][p] for p in PICKS}),
                   'CAND_S_MA5': dict(head=S['head'], anchor_factor=S['anchor_factor'],
                                      plain_total=math.fsum(S['allin'][p] for p in PICKS),
                                      curve={str(p): S['allin'][p] for p in PICKS}),
                   'S_LL5': dict(head=VA['head'], anchor_factor=VA['af'],
                                 plain_total=math.fsum(VA['allin'][p] for p in PICKS),
                                 drift_pct=100 * (math.fsum(VA['allin'][p] for p in PICKS) / pl_ship - 1),
                                 curve={str(p): VA['allin'][p] for p in PICKS}),
                   'S_HOLD1': dict(head=VB['head'], anchor_factor=VB['af'],
                                   plain_total=math.fsum(VB['allin'][p] for p in PICKS),
                                   drift_pct=100 * (math.fsum(VB['allin'][p] for p in PICKS) / pl_ship - 1),
                                   curve={str(p): VB['allin'][p] for p in PICKS})}),
          open(os.path.join(OUT, 'HEAD_DIAGNOSIS.json'), 'w'), indent=1, sort_keys=True, default=float)
open(os.path.join(OUT, 'HEAD_DIAGNOSIS_out.txt'), 'w').write('\n'.join(LOG) + '\n')
P()
P('wrote HEAD_DIAGNOSIS.json / HEAD_DIAGNOSIS_out.txt')
