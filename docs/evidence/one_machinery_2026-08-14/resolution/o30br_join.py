#!/usr/bin/env python3
"""ORDER 30B-R -- T3 THE JOIN.  Closing the first-game cliff (G1).

The two curves the join has to reconcile were measured on DIFFERENT populations, in DIFFERENT
currencies, by DIFFERENT orders:

  * the 30A2 CUMULATIVE BACKBONE (SITTER_FADE_PACKET_2.md section 6.4) -- "<= k games by depth N",
    a monotone ratio of realized from-depth-N delivered value to the entry reference.  Measured at
    k in {0, 2, 5, 10}, depths 2 and 3.  Its k = 0 point IS the sitter law.
  * the 30B-M sigma PERSISTENCE CURVE -- a share of remaining delivered value, fitted on career
    states, and used by the 30B-P preview from 16 games upward (it is fitted from 1 game upward but
    its shallow residuals are the known hot end).

PREREG_30BR section 1 fixes the join before it is fitted:
    g = 0            price = v0 x D(c)                       (the wired sitter law, exactly)
    1 <= g <= 10     price = v0 x D(c) x b(g; c)             b = B(<=g)/B(<=0), log-linear in log1p(g)
    g >= 16          the deep lane, under BOTH readings of the share
    11 <= g <= 15    linear in log1p(g) between the two      -- DECLARED A BRIDGE, not a measurement
and requires the 11-15 CONFLICT to be published rather than averaged away.

THE PRODUCTION LEG IS NOT RE-DERIVED.  It is INVERTED out of the committed preview continuity curves:
    price(g) = (1 - sigma(g)) P(g) + sigma(g) v0    =>    P(g) = [price(g) - sigma(g) v0] / (1 - sigma(g))
which is exact given the committed numbers.  The published prices are INTEGERS, so the inversion
amplifies +/- 0.5 by 1/(1 - sigma); that amplification is printed per point and never hidden.

READ-ONLY.  No engine load, no board, no re-run.

  usage:  python3 o30br_join.py     (writes JOIN.json + JOIN_out.txt)
"""
import os, json, math, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
MOVP = os.path.join(ROOT, 'docs', 'evidence', 'one_machinery_2026-08-14', 'preview', 'PREVIEW_MOVERS.json')
PERSP = os.path.join(ROOT, 'docs', 'evidence', 'pedigree_persistence_2026-08-14', 'PERSISTENCE_TABLE.json')
PK2 = os.path.join(ROOT, 'docs', 'evidence', 'sitter_fade_2026-08-14', 'SITTER_FADE_PACKET_2.md')
OUT_JSON = os.path.join(HERE, 'JOIN.json')
OUT_TXT = os.path.join(HERE, 'JOIN_out.txt')

_LOG = []
def P(s=''):
    print(s)
    _LOG.append(str(s))

def md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()

PINS = dict(preview_movers=md5(MOVP), persistence_table=md5(PERSP), sitter_packet_2=md5(PK2))
MOV = json.load(open(MOVP))
PERS = json.load(open(PERSP))
BF = PERS['q1_persistence']['band_fits']
BYK = {r['key']: r for r in MOV['rows']}
CONT = MOV['continuity']

TAU, BETA = MOV['sigma']['tau'], MOV['sigma']['beta']       # 23.0, 0.80 -- the wired curve
def sigma(g):
    return math.exp(-((max(1e-9, float(g)) / TAU) ** BETA))

GAMES_BANDS = [('0-5', 0, 5), ('6-15', 6, 15), ('16-35', 16, 35), ('36-70', 36, 70), ('71+', 71, 100)]
MIDS = {nm: (lo + min(hi, 100)) / 2.0 for nm, lo, hi in GAMES_BANDS}
BPTS = sorted((MIDS[nm], BF[nm]['beta_v0']) for nm, _, _ in GAMES_BANDS)
def beta_at(g):
    g = max(1e-6, float(g))
    if g <= BPTS[0][0]:
        return BPTS[0][1]
    if g >= BPTS[-1][0]:
        return BPTS[-1][1]
    for i in range(1, len(BPTS)):
        g0, b0 = BPTS[i - 1]; g1, b1 = BPTS[i]
        if g0 <= g <= g1:
            t = (math.log(g) - math.log(g0)) / (math.log(g1) - math.log(g0))
            return math.exp(math.log(b0) + t * (math.log(b1) - math.log(b0)))
    return BPTS[-1][1]

# ==================================================================================================
# THE CUMULATIVE BACKBONE -- SITTER_FADE_PACKET_2.md section 6.4, transcribed and asserted
# ==================================================================================================
BACKBONE = {2: [(0, 0.5684), (2, 0.6560), (5, 0.6936), (10, 0.8236)],
            3: [(0, 0.3600), (2, 0.5933), (5, 0.6807), (10, 0.6930)]}
_txt = open(PK2).read()
for d, pts in BACKBONE.items():
    for k, v in pts:
        assert ('**%.4f**' % v) in _txt, 'backbone knot %.4f (depth %d, <=%d) not found in the packet' % (v, d, k)

def depth_lane(c):
    """PREREG: depth-2 knots for c < 2.5, depth-3 knots for c >= 2.5; depth 4 is NOT extrapolated
    (SITTER_FADE_PACKET_2 section 6.5 declines to wire it), so c >= 3.5 HOLDS the depth-3 lift."""
    return 2 if c < 2.5 else 3

def b_lift(g, c):
    """B(<=g)/B(<=0) on the row's depth lane, log-linear in log1p(g) between the measured knots."""
    pts = BACKBONE[depth_lane(c)]
    b0 = pts[0][1]
    lift = [(k, v / b0) for k, v in pts]
    x = math.log1p(max(0.0, float(g)))
    if g <= 0:
        return 1.0
    for i in range(1, len(lift)):
        k0, l0 = lift[i - 1]; k1, l1 = lift[i]
        x0, x1 = math.log1p(k0), math.log1p(k1)
        if x0 <= x <= x1:
            t = (x - x0) / (x1 - x0)
            return math.exp(math.log(l0) + t * (math.log(l1) - math.log(l0)))
    # PAST the last knot: extrapolate the <=5 -> <=10 slope in log1p(g).  USED ONLY for the
    # conflict display in 11-15; the wired join uses the declared bridge instead.
    (k0, l0), (k1, l1) = lift[-2], lift[-1]
    sl = (math.log(l1) - math.log(l0)) / (math.log1p(k1) - math.log1p(k0))
    return math.exp(math.log(l1) + sl * (x - math.log1p(k1)))

P('=' * 100)
P('ORDER 30B-R -- T3 THE JOIN: closing the first-game cliff')
P('=' * 100)
P('pins: ' + json.dumps(PINS, sort_keys=True))
P('')
P('THE CUMULATIVE BACKBONE, transcribed from SITTER_FADE_PACKET_2.md section 6.4 and ASSERTED')
P('against that file (every knot string-matched in the committed packet):')
P('  %-7s %-8s %10s %10s' % ('depth', '<=games', 'B', 'lift b'))
for d in (2, 3):
    b0 = BACKBONE[d][0][1]
    for k, v in BACKBONE[d]:
        P('  %-7d %-8d %10.4f %10.5f' % (d, k, v, v / b0))
P('')
P('  The lift b is the object the join uses: the backbone AS A RELATIVE LIFT ON THE SITTER PRICE,')
P('  so the g = 0 end is the wired sitter law v0 x D(c) EXACTLY and nothing is re-levelled.')
P('')

# ==================================================================================================
# THE PRODUCTION LEG, INVERTED OUT OF THE COMMITTED PREVIEW CURVES
# ==================================================================================================
P('=' * 100)
P('T3.1 -- THE PRODUCTION LEG, INVERTED FROM THE COMMITTED PREVIEW CONTINUITY CURVES')
P('=' * 100)
ROWSD = {}
for k, curve in sorted(CONT.items()):
    r = BYK[k]
    v0 = r['v0_step1_board']; D = r['fade_D']; c = r['fade_clock']
    pts = {int(g): float(p) for g, p in curve}
    prod = {}
    for g, pr in sorted(pts.items()):
        if g == 0:
            continue
        s = sigma(g)
        prod[g] = (pr - s * v0) / (1.0 - s)
    ROWSD[k] = dict(name=r['name'], pathway=r['pathway'], pick=r['pick'], pos=r['pos'],
                    v0=v0, D=D, c=c, depth=depth_lane(c), preview=pts, production=prod)
    P('')
    P('  %-16s %-4s pick %-4s %-5s   v0 %8.1f   D(c=%.2f) %.4f   sitter price %8.1f   depth lane %d'
      % (k, r['pathway'], r['pick'], r['pos'], v0, c, D, v0 * D, depth_lane(c)))
    if 0 in pts:
        P('     preview 0-game print %d  vs  v0 x D = %.1f   (agreement %.2f)'
          % (pts[0], v0 * D, pts[0] / (v0 * D)))
    P('     %-4s %10s %10s %10s %12s' % ('g', 'preview', 'sigma(g)', 'prod P(g)', 'inv amp +/-'))
    for g in sorted(prod):
        if g > 15 and k != 'isaac-kako':
            continue
        s = sigma(g)
        P('     %-4d %10.0f %10.4f %10.1f %12.2f' % (g, pts[g], s, prod[g], 0.5 / (1.0 - s)))
P('')
P('  The "inv amp" column is the rounding amplification 0.5/(1-sigma): the published prices are')
P('  integers, so P(g) inherits that band.  At g = 1 it is +/- 6.4 board points.  Disclosed.')
P('')

# ==================================================================================================
# T3.2 -- THE JOINED CURVE
# ==================================================================================================
P('=' * 100)
P('T3.2 -- THE JOINED CURVE, PRICE vs GAMES 0 -> 16 AT FIXED OUTPUT')
P('=' * 100)
P('  thin lane 0-10 : v0 x D(c) x b(g; c)          -- the backbone IS the whole price law there')
P('  deep lane 16+  : W (1-sigma)P + sigma v0  and  A  P + beta(g) v0   -- BOTH readings shown')
P('  bridge 11-15   : linear in log1p(g) between the thin lane at 10 and the deep lane at 16')
P('                   DECLARED A BRIDGE.  It is not a measurement and it is not called one.')
P('')

def prod_at16(prod):
    """P(16) by log-linear extrapolation of P over g in [10,15].  A ONE-GAME extrapolation, declared."""
    xs = [g for g in prod if 10 <= g <= 15]
    if len(xs) < 2:
        return None
    x0, x1 = min(xs), max(xs)
    y0, y1 = prod[x0], prod[x1]
    if y0 <= 0 or y1 <= 0:
        return y1 + (y1 - y0) / (math.log1p(x1) - math.log1p(x0)) * (math.log1p(16) - math.log1p(x1))
    sl = (math.log(y1) - math.log(y0)) / (math.log1p(x1) - math.log1p(x0))
    return math.exp(math.log(y1) + sl * (math.log1p(16) - math.log1p(x1)))

JOIN = {}
for k, d in ROWSD.items():
    if 0 not in d['preview']:
        continue
    v0, D, c = d['v0'], d['D'], d['c']
    P16 = prod_at16(d['production'])
    deep16_W = (1 - sigma(16)) * P16 + sigma(16) * v0
    deep16_A = P16 + beta_at(16) * v0
    thin10 = v0 * D * b_lift(10, c)
    def joined(g, deep16):
        if g <= 0:
            return v0 * D
        if g <= 10:
            return v0 * D * b_lift(g, c)
        if g >= 16:
            return deep16
        x0, x1 = math.log1p(10), math.log1p(16)
        t = (math.log1p(g) - x0) / (x1 - x0)
        return thin10 + t * (deep16 - thin10)
    curveW = [(g, joined(g, deep16_W)) for g in range(0, 17)]
    curveA = [(g, joined(g, deep16_A)) for g in range(0, 17)]
    prev = d['preview']
    stepW = curveW[1][1] / curveW[0][1] - 1.0
    prev_step = (prev[1] / prev[0] - 1.0) if 0 in prev and 1 in prev else None
    monoW = all(curveW[i + 1][1] >= curveW[i][1] - 1e-9 for i in range(len(curveW) - 1))
    monoA = all(curveA[i + 1][1] >= curveA[i][1] - 1e-9 for i in range(len(curveA) - 1))
    prevmono = all(prev[g + 1] >= prev[g] for g in range(0, 15) if g in prev and g + 1 in prev)
    JOIN[k] = dict(v0=v0, D=D, c=c, depth=d['depth'], P16=P16,
                   deep16_weight=deep16_W, deep16_additive=deep16_A,
                   curve_weight=curveW, curve_additive=curveA,
                   first_game_step_join=stepW, first_game_step_preview=prev_step,
                   monotone_join_weight=monoW, monotone_join_additive=monoA,
                   monotone_preview_0_15=prevmono,
                   implied_pedigree_weight_thin={g: (v0 * D * b_lift(g, c) - d['production'][g]) / v0
                                                 for g in sorted(d['production']) if 1 <= g <= 10})
    P('')
    P('  %-16s  v0 %8.1f  D %.4f  c %.2f  depth %d   P(16) %s'
      % (k, v0, D, c, d['depth'], ('%.1f' % P16) if P16 else 'n/a'))
    P('     %-4s %12s %12s %12s %14s' % ('g', 'PREVIEW', 'JOIN (W)', 'JOIN (A)', 'lane'))
    for g in range(0, 17):
        lane = 'sitter' if g == 0 else ('backbone' if g <= 10 else ('BRIDGE' if g < 16 else 'deep'))
        pv = ('%d' % prev[g]) if g in prev else '-'
        P('     %-4d %12s %12.1f %12.1f %14s' % (g, pv, curveW[g][1], curveA[g][1], lane))
    P('     FIRST-GAME STEP:  preview %s   ->   JOIN %+.1f%%'
      % (('%+.1f%%' % (100 * prev_step)) if prev_step is not None else 'n/a', 100 * stepW))
    P('     MONOTONE 0->16:   preview(0-15) %s   JOIN(W) %s   JOIN(A) %s'
      % ('YES' if prevmono else 'NO', 'YES' if monoW else 'NO', 'YES' if monoA else 'NO'))
    P('     implied pedigree weight in the thin lane, lambda(g) = [price_join(g) - P(g)] / v0:')
    ipw = JOIN[k]['implied_pedigree_weight_thin']
    P('       ' + '  '.join('g%d %+.3f' % (g, ipw[g]) for g in sorted(ipw) if g <= 10))
P('')

# ==================================================================================================
# T3.3 -- THE OVERLAP CONFLICT, 11-15.  SHOWN, NOT AVERAGED.
# ==================================================================================================
P('=' * 100)
P('T3.3 -- THE 11-15 OVERLAP: DO THE TWO MEASURED CURVES AGREE?  (shown, never averaged)')
P('=' * 100)
P('  thin-lane EXTRAPOLATION: the backbone lift carried past its last knot (<=10) on the')
P('    <=5 -> <=10 slope in log1p(g).  deep-lane EXTRAPOLATION: the sigma blend carried down')
P('    below 16, which is exactly the preview\'s own printed curve.  Both are extrapolations of')
P('    a measured object outside where it was measured, and both are labelled as such.')
P('')
CONFLICT = {}
for k, d in ROWSD.items():
    if 11 not in d['preview']:
        continue
    v0, D, c = d['v0'], d['D'], d['c']
    rows = []
    P('')
    P('  %-16s (depth lane %d)' % (k, d['depth']))
    P('     %-4s %12s %12s %12s %10s %10s'
      % ('g', 'thin extrap', 'deep W', 'deep A', 'W/thin', 'A/thin'))
    for g in range(11, 16):
        th = v0 * D * b_lift(g, c)
        Pg = d['production'][g]
        dw = (1 - sigma(g)) * Pg + sigma(g) * v0
        da = Pg + beta_at(g) * v0
        rows.append(dict(g=g, thin=th, deep_W=dw, deep_A=da, ratio_W=dw / th, ratio_A=da / th))
        P('     %-4d %12.1f %12.1f %12.1f %9.3fx %9.3fx' % (g, th, dw, da, dw / th, da / th))
    m = [r for r in rows if r['g'] == 13][0]
    CONFLICT[k] = dict(rows=rows, at13_ratio_W=m['ratio_W'], at13_ratio_A=m['ratio_A'],
                       at13_rel_W=m['ratio_W'] - 1.0, at13_rel_A=m['ratio_A'] - 1.0)
    P('     AT g = 13: deep(W) is %+.1f%% above the thin extrapolation; deep(A) is %+.1f%%.'
      % (100 * (m['ratio_W'] - 1), 100 * (m['ratio_A'] - 1)))
P('')
P('  READ THIS PLAINLY: the two curves are measurements of DIFFERENT OBJECTS on DIFFERENT')
P('  POPULATIONS and they do not meet.  The join does not make them meet; it declares a bridge')
P('  across the gap and prints the size of the gap.  Averaging them would have hidden exactly this.')
P('')

json.dump(dict(order='30B-R', task='T3 the join', pins=PINS, backbone=BACKBONE,
               sigma=dict(tau=TAU, beta=BETA), beta_curve=BPTS,
               rows={k: {kk: vv for kk, vv in v.items() if kk != 'preview'} for k, v in ROWSD.items()},
               join=JOIN, conflict=CONFLICT),
          open(OUT_JSON, 'w'), indent=1, sort_keys=True, default=float)
open(OUT_TXT, 'w').write('\n'.join(_LOG) + '\n')
P('wrote %s and %s' % (OUT_JSON, OUT_TXT))
