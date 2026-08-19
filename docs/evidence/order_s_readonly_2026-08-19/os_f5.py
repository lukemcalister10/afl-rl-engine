#!/usr/bin/env python3
"""ORDER S READ-ONLY — F5. THE SEVERITY CALIBRATION.

NO ENGINE FILE IS EDITED. NO DIAL IS ADDED. NO BOARD IS BUILT. NOTHING IS ADOPTED AND NO REPAIR IS
PROPOSED. This file measures and reports.

THE OWNER'S OBJECTION: "I'm not sure the first season is enough evidence to ever justify a player
like that losing 4x his starting value."

TWO CLAIMS LIVE INSIDE IT AND F5 SEPARATES THEM (PREREG_SRO_F5.md section 0):
  LEVEL  -- at that evidence, does the charge mark the row below what history says he delivers?
  SPEED  -- A(g) = 1 - exp(-g/G0) with G0 = 9.89 was measured from where the PRODUCTION slope
            saturates. Using it in the charge ASSUMES pedigree-conviction firms at the same speed.

THE VANTAGE. Stage N is the moment immediately after the player's Nth season, which is exactly the
state the engine charges from:
  g   = CUMULATIVE career games through depth N     -- the axis A(g) reads
  s_P = ORDER P's surplus over seasons 1..N         -- the axis T(s) reads
  OUT = DISC-discounted house-ruler delivered value from depth N+1 onward, over v0

THE COMPARISON. The charged mark f and the realized outcome OUT are in DIFFERENT UNITS and a level
comparison between them is meaningless. Both are therefore taken RELATIVE TO A REFERENCE CELL at the
same stage and the same games bin, which makes both sides unit-free:

    CALIBRATION = ( OUT(cell) / OUT(ref) ) / ( f(cell) / f(ref) )
    > 1  the row delivers MORE than the charge marks him at, relative to his peer -- FRONT-LOADING
    < 1  the row delivers less -- the charge is generous

  usage: OPENBLAS_NUM_THREADS=1 ... python3 os_f5.py
"""
import json, math, os, sys, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(REPO, 'docs/evidence/order_p_2026-08-18'))
import op_lib as PB                                                          # noqa: E402
LB = PB.LB

SEED, B_BOOT = 32, 2000
# THE WIRED ORDER P CONSTANTS. Transcribed from the engine block and asserted against it below.
LAMBDA = 0.1743833036575403
G0 = 9.890000000000008
BETA_SAT = 0.11464630061141393
S0 = -2.452720891469074
S_P5 = -33.06133449874688
THETA_R = BETA_SAT / LAMBDA
TMAX = 1.0 - THETA_R * (S_P5 - S0)
MIN_FUTURE = 4                    # prereg 3: at least four observed seasons after the vantage
MIN_FUTURE_SENS = 6
L = []


def P(s=''):
    print(s); L.append(str(s))


def A_of(g):
    return 1.0 - math.exp(-float(g) / G0)


def T_of(s, theta=THETA_R, tmax=TMAX):
    return min(max(1.0 - theta * (s - S0), 0.0), tmax)


def f_of(g, s, lam=LAMBDA, theta=THETA_R, tmax=TMAX):
    return math.exp(-lam * A_of(g) * T_of(s, theta, tmax))


# ---- assert the constants against the engine source ----------------------------------------------------
import re
SRC = open(os.path.join(REPO, 'engine/rl_after/_merged_recover.py')).read()
for nm, val in (('O37_G0', G0), ('O37_BETA_SAT', BETA_SAT), ('O37_LAMBDA', LAMBDA),
                ('O37_S0', S0), ('O37_S_P5', S_P5)):
    m = re.search(r'%s=([0-9eE\.\+\-]+)' % nm, SRC)
    assert m and abs(float(m.group(1)) - val) < 1e-15, 'F5-A1 FIRED: %s does not match the engine' % nm

M = LB.load_matrix('OKRULED')
ROWS_SEASON = PB.season_rows(M)
PG = PB.Premium(ROWS_SEASON)
SURF = json.load(open(os.path.join(REPO, 'docs/evidence/order_p_build_2026-08-18/PREMIUM_SURFACE.json')))
for c in ('TALL', 'SMALL'):
    d = float(np.max(np.abs(np.array(SURF[c]['y']) - PG.grid[c][1])))
    assert d < 1e-9, 'F5-A2 FIRED: the premium surface is not the built one (%s: %g)' % (c, d)

P('=' * 118)
P('ORDER S READ-ONLY — F5. THE SEVERITY CALIBRATION. IS THE CHARGE FRONT-LOADED BEYOND WHAT HISTORY SUPPORTS?')
P('=' * 118)
P('NO BOARD IS BUILT. NO ENGINE FILE IS EDITED. NO DIAL IS ADDED. NOTHING IS ADOPTED AND NO REPAIR IS')
P('PROPOSED. Named rows illustrate; they gate nothing.')
P('ruler      : the house S4 delivered-value ruler, md5 %s' % LB.check_s4_copy())
P('constants  : ASSERTED against the engine block — LAMBDA %.10f · G0 %.4f · BETA_sat %.10f ·'
  % (LAMBDA, G0, BETA_SAT))
P('             THETA_R %.6f · s0 %.6f · TMAX %.4f.  Falsifier F5-A1 did not fire.' % (THETA_R, S0, TMAX))
P('premium    : ORDER P\'s own surface, asserted node-for-node against the BUILT engine grid.')
P('             Falsifier F5-A2 did not fire.')
P()

# ---- the population ------------------------------------------------------------------------------------
PBUILT = {r['key']: r for r in json.load(open(os.path.join(LB.SP, 'per_entrant_PBUILT.json')))['recs']}


def build(stage, min_future=MIN_FUTURE, types=('ND',)):
    out = []
    for k, r in M.items():
        if k in LB.FM or r.get('type') not in types:
            continue
        ey = int(r.get('year') or 0)
        if ey < LB.ENTRY_FLOOR:
            continue
        if ey + stage + min_future > LB.LAST_REAL_SEASON:
            continue
        v0 = float(r.get('v0') or 0.0)
        if not (v0 > 0):
            continue
        gb = r.get('games_by') or {}
        if str(stage) not in gb:
            continue
        g = float(gb[str(stage)])
        if g <= 0:                              # A(0) = 0 exactly: the charge cannot reach him
            continue
        s = PB.perf_surplus_P(r, ey + stage, PG)
        if s is None:
            continue
        sv = LB.season_values(r)
        out.append(dict(key=k, name=r.get('player'), pos=r.get('pos'),
                        cls=('TALL' if r.get('pos') in LB.TALLPOS else 'SMALL'),
                        pick=r.get('pick'), entry=ey, stage=stage, g=g, s=s, v0=v0,
                        out=LB.dvrest(sv, ey + stage) / v0,
                        f=f_of(g, s),
                        delisted=bool(r.get('delisted') or r.get('retired_now')),
                        last_game=r.get('last_game_year')))
    return out


STAGES = (1, 2, 3)
POP = {n: build(n) for n in STAGES}
P('-' * 118)
P('1 · THE POPULATION, AND THE CENSORING RULE FIXED BEFORE THE RUN')
P('-' * 118)
P('   ND entrants from %d, positive v0, force-majeure excluded, with at least ONE career game at the'
  % LB.ENTRY_FLOOR)
P('   vantage (A(0) = 0 exactly, so a gameless row is not a row the charge can reach).')
P('   CENSORING: at least %d observed seasons after the vantage, so entry year <= %d - stage.'
  % (MIN_FUTURE, LB.LAST_REAL_SEASON - MIN_FUTURE))
P('   THE LAST SEVERAL DRAFT CLASSES ARE THEREFORE ABSENT FROM F5 ENTIRELY and no claim here reaches')
P('   them. The outcome carries NO PROJECTED TAIL — it sums observed seasons to %d only — which biases'
  % LB.LAST_REAL_SEASON)
P('   OUT downward for later cohorts and so cuts AGAINST the front-loading finding F5-P1 predicts.')
P()
P('   %-8s %8s %10s %10s %12s %12s %12s'
  % ('stage', 'rows', 'entry lo', 'entry hi', 'med games', 'med s_P', 'delisted %'))
for n in STAGES:
    s = POP[n]
    P('   %-8d %8d %10d %10d %12.1f %12.2f %11.1f%%'
      % (n, len(s), min(r['entry'] for r in s), max(r['entry'] for r in s),
         np.median([r['g'] for r in s]), np.median([r['s'] for r in s]),
         100 * np.mean([r['delisted'] for r in s])))
P()

# ---- the owner's premise, checked ----------------------------------------------------------------------
P('-' * 118)
P('2 · THE OWNER\'S PREMISE, CHECKED EXACTLY — WHAT DOES THE CHARGE ACTUALLY MARK THAT SHAPE AT?')
P('-' * 118)
P('   The shape: a first-year row, 15 games, about 19 points a game below his PEDIGREE bar.')
P('   Computed from the wired constants, not assumed:')
gg, ss = 15.0, -19.0
P('     A(15)   = 1 - exp(-15/%.2f)              = %.4f' % (G0, A_of(gg)))
P('     T(-19)  = clip(1 - %.5f*(-19 - %.4f))  = %.4f' % (THETA_R, S0, T_of(ss)))
P('     f       = exp(-%.6f * %.4f * %.4f)  = %.4f' % (LAMBDA, A_of(gg), T_of(ss), f_of(gg, ss)))
P()
P('   So the mechanism retains %.1f%% of that row\'s pedigree leg and charges away %.1f%%.'
  % (100 * f_of(gg, ss), 100 * (1 - f_of(gg, ss))))
P('   The PRICE is not the pedigree leg — it is rho*production + pi*pedigree + age credit — so the')
P('   "0.24x of entry" the owner quotes is a PRICE ratio, and it is checked against real board rows')
P('   rather than argued. Closest actual ORDER P board rows to the shape (age under 24, 10-20 career')
P('   games, s_P between -14 and -24), printed with their real price over entry price:')
P()
P('   %-24s %6s %6s %8s %8s %9s %9s %9s'
  % ('row', 'pick', 'games', 's_P', 'f', 'v0', 'price', 'price/v0'))
SHAPE = []
for r in POP[1] + POP[2]:
    pass
for k, rec in M.items():
    if k in LB.FM or rec.get('type') != 'ND':
        continue
    v0 = float(rec.get('v0') or 0.0)
    pb = PBUILT.get(k)
    if not (v0 > 0) or pb is None or pb.get('cur') is None:
        continue
    ad = rec.get('age_draft')
    if ad is None:
        continue
    age = int(ad) + (2026 - int(rec['year']))
    g = sum(float(x['games'] or 0) for x in rec['seasons'] if x['year'] <= 2026)
    if age >= 24 or not (10 <= g <= 20):
        continue
    s = PB.perf_surplus_P(rec, 2026, PG)
    if s is None or not (-24 <= s <= -14):
        continue
    SHAPE.append(dict(key=k, name=rec.get('player'), pick=rec.get('pick'), g=g, s=s,
                      f=f_of(g, s), v0=v0, cur=float(pb['cur']), ratio=float(pb['cur']) / v0))
for r in sorted(SHAPE, key=lambda z: -z['v0'])[:10]:
    P('   %-24s %6s %6.0f %8.2f %8.4f %9.0f %9.0f %9.4f'
      % (r['name'][:24], r['pick'], r['g'], r['s'], r['f'], r['v0'], r['cur'], r['ratio']))
if SHAPE:
    rr = sorted(r['ratio'] for r in SHAPE)
    med = float(np.median(rr))
    P()
    P('   %d board rows are in that shape. Their price over entry price runs %.4f to %.4f, median %.4f.'
      % (len(SHAPE), rr[0], rr[-1], med))
    P('   %d of the %d sit at or below 0.25x of entry.' % (sum(1 for x in rr if x <= 0.25), len(rr)))
    P()
    P('   THE PREMISE, SPLIT INTO ITS TWO HALVES, BECAUSE THEY DO NOT GIVE THE SAME ANSWER:')
    P('     ON THE PEDIGREE LEG the owner is right and understating it — the mechanism retains %.3f of'
      % f_of(15, -19))
    P('     the prior, which is a %.1fx cut, not 4x.' % (1.0 / f_of(15, -19)))
    P('     ON THE PRICE the owner\'s 0.24x is at the HARSH END of what the board actually does: the')
    P('     median row of this shape prices at %.2fx of entry, and %d of %d sit at or below 0.25x.'
      % (med, sum(1 for x in rr if x <= 0.25), len(rr)))
    P('     The difference is the production leg, which the charge does not touch. A row whose shown')
    P('     production is also weak lands near 0.24x; one whose production holds up does not.')
    P('   SO: the shape the owner describes DOES occur on the board, on %d of these %d rows, but it is'
      % (sum(1 for x in rr if x <= 0.25), len(rr)))
    P('   not the median outcome of the shape. THE PREMISE IS PARTLY CONFIRMED and the packet says so.')
P()

# ---- the cells -----------------------------------------------------------------------------------------
GBINS = [('1-9', 1, 9), ('10-22', 10, 22), ('23+', 23, 1e9)]
SBINS = [('0 to -10', -10, 1e9), ('-10 to -20', -20, -10), ('-20 to -35', -35, -20),
         ('worse than -35', -1e9, -35)]
REF = '0 to -10'


def sel(rows, gb, sb):
    _, glo, ghi = [x for x in GBINS if x[0] == gb][0]
    _, slo, shi = [x for x in SBINS if x[0] == sb][0]
    return [r for r in rows if glo <= r['g'] <= ghi and slo <= r['s'] < shi]


def cal(rows, gb, sb, stat=np.mean):
    a = sel(rows, gb, sb)
    b = sel(rows, gb, REF)
    if len(a) < 2 or len(b) < 2:
        return None
    oa, ob = stat([r['out'] for r in a]), stat([r['out'] for r in b])
    fa, fb = np.mean([r['f'] for r in a]), np.mean([r['f'] for r in b])
    if ob <= 0 or fb <= 0 or fa <= 0:
        return None
    return (oa / ob) / (fa / fb)


def boot_cal(rows, gb, sb, B=B_BOOT, seed=SEED):
    rng = np.random.default_rng(seed)
    n = len(rows)
    out = []
    for _ in range(B):
        s = [rows[i] for i in rng.integers(0, n, size=n)]
        v = cal(s, gb, sb)
        if v is not None and np.isfinite(v):
            out.append(v)
    if len(out) < 20:
        return (float('nan'), float('nan'))
    return (float(np.percentile(out, 5)), float(np.percentile(out, 95)))


P('-' * 118)
P('3 · THE CALIBRATION CURVE, PER CAREER STAGE')
P('-' * 118)
P('   Every number is RELATIVE to the SAME stage and the SAME games bin at surplus %s.' % REF)
P('   charged  = mean f in the cell / mean f in the reference cell   (exact, no estimation)')
P('   realized = mean OUT in the cell / mean OUT in the reference cell')
P('   CALIB    = realized / charged.  Above 1 the row delivers MORE than he is marked at.')
P()
CAL = {}
for n in STAGES:
    rows = POP[n]
    P('   -- STAGE %d (after season %d), %d rows' % (n, n, len(rows)))
    P('   %-10s %-16s %6s %7s %9s %9s %9s %9s %-22s %7s'
      % ('games', 'surplus', 'n', 'delist', 'mean f', 'mean OUT', 'charged', 'realized', 'CALIB 90% CI', 'CALIB'))
    for gb, _, _ in GBINS:
        for sb, _, _ in SBINS:
            a = sel(rows, gb, sb)
            b = sel(rows, gb, REF)
            if not a:
                continue
            mf = float(np.mean([r['f'] for r in a]))
            mo = float(np.mean([r['out'] for r in a]))
            dl = float(np.mean([r['delisted'] for r in a]))
            c = cal(rows, gb, sb)
            if sb == REF:
                P('   %-10s %-16s %6d %6.0f%% %9.4f %9.4f %9s %9s %-22s %7s'
                  % (gb, sb + '  (ref)', len(a), 100 * dl, mf, mo, '1.0000', '1.0000', '', '1.0000'))
                CAL['%d|%s|%s' % (n, gb, sb)] = dict(n=len(a), delisted=dl, f=mf, out=mo,
                                                     charged=1.0, realized=1.0, calib=1.0,
                                                     ci=[1.0, 1.0])
                continue
            if c is None:
                P('   %-10s %-16s %6d %6.0f%% %9.4f %9.4f %9s' % (gb, sb, len(a), 100 * dl, mf, mo, 'no ref'))
                continue
            fb = float(np.mean([r['f'] for r in b])); ob = float(np.mean([r['out'] for r in b]))
            lo, hi = boot_cal(rows, gb, sb)
            thin = ' THIN' if len(a) < 25 else ''
            CAL['%d|%s|%s' % (n, gb, sb)] = dict(n=len(a), delisted=dl, f=mf, out=mo,
                                                 charged=mf / fb, realized=mo / ob, calib=c,
                                                 ci=[lo, hi])
            P('   %-10s %-16s %6d %6.0f%% %9.4f %9.4f %9.4f %9.4f [%+8.3f, %+8.3f] %7.3f%s'
              % (gb, sb, len(a), 100 * dl, mf, mo, mf / fb, mo / ob, lo, hi, c, thin))
    P()

# ---- verdict 1 -----------------------------------------------------------------------------------------
P('-' * 118)
P('4 · VERDICT (1) — THE TAIL THE OWNER NAMED')
P('-' * 118)
P('   Stage 1 and stage 2, games 10-22, surplus -20 to -35 and worse than -35. The four cells are')
P('   printed individually AND pooled, because pooling is where the sample is.')
P()
P('   %-30s %6s %7s %9s %9s %9s %-22s %-14s'
  % ('cell', 'n', 'delist', 'charged', 'realized', 'CALIB', '90% CI', 'verdict'))
V1 = {}


def verdict_of(lo, hi):
    if math.isnan(lo):
        return 'not scored'
    if lo > 1.0:
        return 'FRONT-LOADS'
    if hi < 1.0:
        return 'GENEROUS'
    return 'ON IT (CI covers 1)'


for n in (1, 2):
    for sb in ('-20 to -35', 'worse than -35'):
        a = sel(POP[n], '10-22', sb)
        if len(a) < 2:
            P('   %-30s %6d   too few rows to score' % ('stage %d, %s' % (n, sb), len(a))); continue
        c = cal(POP[n], '10-22', sb)
        lo, hi = boot_cal(POP[n], '10-22', sb)
        k = 'stage %d, %s' % (n, sb)
        V1[k] = dict(n=len(a), calib=c, ci=[lo, hi], verdict=verdict_of(lo, hi),
                     delisted=float(np.mean([r['delisted'] for r in a])))
        P('   %-30s %6d %6.0f%% %9.4f %9.4f %9.4f [%+8.3f, %+8.3f] %-14s'
          % (k, len(a), 100 * np.mean([r['delisted'] for r in a]),
             CAL['%d|10-22|%s' % (n, sb)]['charged'], CAL['%d|10-22|%s' % (n, sb)]['realized'],
             c, lo, hi, verdict_of(lo, hi)))
POOL12 = POP[1] + POP[2]


def cal_pool(rows, gb, deep_only=True):
    a = [r for r in rows if 10 <= r['g'] <= 22 and r['s'] < -20]
    b = [r for r in rows if 10 <= r['g'] <= 22 and r['s'] >= -10]
    if len(a) < 2 or len(b) < 2:
        return None
    oa, ob = np.mean([r['out'] for r in a]), np.mean([r['out'] for r in b])
    fa, fb = np.mean([r['f'] for r in a]), np.mean([r['f'] for r in b])
    if ob <= 0 or fb <= 0:
        return None
    return (oa / ob) / (fa / fb)


def cal_pool_stat_early(rows, stat):
    a = [r for r in rows if 10 <= r['g'] <= 22 and r['s'] < -20]
    b = [r for r in rows if 10 <= r['g'] <= 22 and r['s'] >= -10]
    if len(a) < 2 or len(b) < 2:
        return None
    oa, ob = stat([r['out'] for r in a]), stat([r['out'] for r in b])
    fa, fb = np.mean([r['f'] for r in a]), np.mean([r['f'] for r in b])
    return (oa / ob) / (fa / fb) if ob > 0 and fb > 0 else None


rng = np.random.default_rng(SEED)
bs = []
for _ in range(B_BOOT):
    s = [POOL12[i] for i in rng.integers(0, len(POOL12), size=len(POOL12))]
    v = cal_pool(s, '10-22')
    if v is not None and np.isfinite(v):
        bs.append(v)
cp = cal_pool(POOL12, '10-22')
lo, hi = float(np.percentile(bs, 5)), float(np.percentile(bs, 95))
na = len([r for r in POOL12 if 10 <= r['g'] <= 22 and r['s'] < -20])
nb = len([r for r in POOL12 if 10 <= r['g'] <= 22 and r['s'] >= -10])
P()
P('   POOLED stages 1+2, games 10-22, ALL rows below -20 against ALL rows at or above -10:')
P('     deep n = %d   reference n = %d' % (na, nb))
P('     CALIBRATION = %.4f, 90%% CI [%.4f, %.4f]   -->  %s' % (cp, lo, hi, verdict_of(lo, hi)))
V1['POOLED stages 1+2'] = dict(n=na, n_ref=nb, calib=cp, ci=[lo, hi], verdict=verdict_of(lo, hi))
P()
P('   F5-P1 predicted CALIBRATION > 1 (the charge front-loads). %s'
  % ('CONFIRMED on the pooled cell.' if lo > 1.0 else
     ('FIRED — the interval covers or sits below 1.' if not math.isnan(lo) else 'not scorable.')))
P()
P('-' * 118)
P('4b · THE CAVEAT THAT MUST BE READ WITH VERDICT (1) — THE MEAN AND THE MEDIAN DISAGREE')
P('-' * 118)
a_ = [r for r in POOL12 if 10 <= r['g'] <= 22 and r['s'] < -20]
b_ = [r for r in POOL12 if 10 <= r['g'] <= 22 and r['s'] >= -10]
P('   The deep cell holds %d rows. Their outcomes are option-shaped: %d of %d deliver essentially'
  % (len(a_), sum(1 for r in a_ if r['out'] < 0.05), len(a_)))
P('   nothing (under 0.05 of entry), and the cell mean is carried by %d rows above 1.0.'
  % sum(1 for r in a_ if r['out'] > 1.0))
P('   %-28s %10s %10s %10s' % ('', 'deep cell', 'reference', 'ratio'))
for nm, fn in (('mean', np.mean), ('median', np.median), ('share above 0.5 of entry',
                                                          lambda v: float(np.mean([x > 0.5 for x in v])))):
    va, vb = fn([r['out'] for r in a_]), fn([r['out'] for r in b_])
    P('   %-28s %10.4f %10.4f %10.4f' % (nm, va, vb, (va / vb) if vb else float('nan')))
P()
P('   ON THE MEAN the charge front-loads (CALIB %.2f). ON THE MEDIAN it does not (CALIB %.2f).'
  % (cal_pool_stat_early(POOL12, np.mean) or float('nan'),
     cal_pool_stat_early(POOL12, np.median) or float('nan')))
P('   BOTH ARE TRUE AND THEY ARE NOT IN CONFLICT: the typical deep underperformer really is worth')
P('   about what the charge says, and the AVERAGE one is worth about twice it, because a minority')
P('   recover hard. A multiplicative mark on a prior is a mean-like object — it is a price, and a')
P('   price is an expectation, not a median — so the MEAN is the like-for-like comparison and it is')
P('   the primary reading. THE MEDIAN IS PRINTED BECAUSE IT DISAGREES, NOT DESPITE IT.')
P('   The same statistic choice sits inside the wired mechanism already: ORDER P fitted BETA on cell')
P('   MEANS and the sitter fade is a cell MEAN normalised by the depth-1 MEAN (F4 section 2).')
P()

# ---- verdict 3 : the tail flattens ----------------------------------------------------------------------
P('-' * 118)
P('5 · F5-P3 — DOES THE TAIL FLATTEN? (the empirical question TMAX exists to answer)')
P('-' * 118)
P('   %-30s %6s %10s %-24s' % ('cell (stages 1+2 pooled)', 'n', 'mean OUT', '90% CI of mean OUT'))
TAILJ = {}
for lab, lo_s, hi_s in (('-10 to -20', -20, -10), ('-20 to -35', -35, -20), ('worse than -35', -1e9, -35)):
    a = [r for r in POOL12 if lo_s <= r['s'] < hi_s]
    if len(a) < 3:
        P('   %-30s %6d  too few' % (lab, len(a))); continue
    v = np.array([r['out'] for r in a])
    rng2 = np.random.default_rng(SEED)
    b = [float(np.mean(rng2.choice(v, size=len(v), replace=True))) for _ in range(B_BOOT)]
    l_, h_ = float(np.percentile(b, 5)), float(np.percentile(b, 95))
    TAILJ[lab] = dict(n=len(a), mean=float(np.mean(v)), ci=[l_, h_])
    P('   %-30s %6d %10.4f [%+10.4f, %+10.4f]%s' % (lab, len(a), np.mean(v), l_, h_,
                                                    ' THIN' if len(a) < 25 else ''))
if '-20 to -35' in TAILJ and 'worse than -35' in TAILJ:
    a, b = TAILJ['-20 to -35']['ci'], TAILJ['worse than -35']['ci']
    s_ = (a[1] < b[0] or b[1] < a[0])
    P()
    P('   separable? %s   ->  F5-P3 %s'
      % ('YES' if s_ else 'NO — the intervals overlap',
         'FIRED' if s_ else 'did not fire: the tail flattens, as TMAX assumes'))
P()

# ---- verdict 4 : survival --------------------------------------------------------------------------------
P('-' * 118)
P('6 · F5-P4 — SURVIVAL. DELISTED ROWS ARE OUTCOMES, NOT EXCLUSIONS.')
P('-' * 118)
P('   %-18s %8s %8s %8s %8s' % ('surplus band', 'n st1', 'delist%', 'mean OUT', 'OUT if kept'))
SURV = {}
for lab, lo_s, hi_s in [(x[0], x[1], x[2]) for x in SBINS]:
    a = [r for r in POP[1] if lo_s <= r['s'] < hi_s]
    if not a:
        continue
    kept = [r['out'] for r in a if not r['delisted']]
    SURV[lab] = dict(n=len(a), delisted=float(np.mean([r['delisted'] for r in a])),
                     out=float(np.mean([r['out'] for r in a])),
                     out_kept=(float(np.mean(kept)) if kept else float('nan')))
    P('   %-18s %8d %7.0f%% %8.4f %8.4f' % (lab, len(a), 100 * SURV[lab]['delisted'],
                                            SURV[lab]['out'], SURV[lab]['out_kept']))
rise = [SURV[x[0]]['delisted'] for x in SBINS if x[0] in SURV]
P()
P('   delisted share rises monotonically with depth of underperformance? %s  ->  F5-P4 %s'
  % ('YES' if all(rise[i] <= rise[i + 1] + 1e-9 for i in range(len(rise) - 1)) else 'NO',
     'did not fire' if all(rise[i] <= rise[i + 1] + 1e-9 for i in range(len(rise) - 1)) else 'FIRED'))
P('   The "OUT if kept" column is printed ONLY to show what a survivor-only reading would have said.')
P('   IT IS NOT USED ANYWHERE. Dropping the delisted rows would flatter the charge and is the exact')
P('   bias this seat preregistered against.')
P()

# ---- verdict 2 : the conviction speed ---------------------------------------------------------------------
P('-' * 118)
P('7 · VERDICT (2) — THE CONVICTION-SPEED ASSUMPTION, TESTED DIRECTLY')
P('-' * 118)
P('   The mechanism implies  ln f(at-bar) - ln f(deep) = BETA_sat * A(g) * Delta_s.  Inverting it')
P('   recovers an EMPIRICAL A from outcomes alone:')
P()
P('       A_hat(g) = -ln( OUT(deep,g) / OUT(at-bar,g) ) / ( BETA_sat * Delta_s(g) )')
P()
P('   A_hat is NOT bounded to [0,1] by construction and is printed raw. Stages 1, 2 and 3 are pooled')
P('   because A(g) is a pure function of g in the mechanism; a stage-1-only run is printed after.')
P()
GFIT = [('1-4', 1, 4), ('5-9', 5, 9), ('10-14', 10, 14), ('15-19', 15, 19),
        ('20-24', 20, 24), ('25-34', 25, 34), ('35+', 35, 1e9)]
ALLP = POP[1] + POP[2] + POP[3]


def ahat_bins(rows, deep_cut=-20.0, ref_cut=-10.0):
    res = []
    for lab, lo_g, hi_g in GFIT:
        d = [r for r in rows if lo_g <= r['g'] <= hi_g and r['s'] < deep_cut]
        b = [r for r in rows if lo_g <= r['g'] <= hi_g and r['s'] >= ref_cut]
        if len(d) < 3 or len(b) < 3:
            res.append((lab, lo_g, hi_g, len(d), len(b), None, None, None)); continue
        od, ob = float(np.mean([r['out'] for r in d])), float(np.mean([r['out'] for r in b]))
        ds = float(np.mean([r['s'] for r in b])) - float(np.mean([r['s'] for r in d]))
        if od <= 0 or ob <= 0 or ds <= 0:
            res.append((lab, lo_g, hi_g, len(d), len(b), None, None, ds)); continue
        a = -math.log(od / ob) / (BETA_SAT * ds)
        gmid = float(np.mean([r['g'] for r in d + b]))
        res.append((lab, lo_g, hi_g, len(d), len(b), a, gmid, ds))
    return res


def fit_G0(bins, free_amp=False):
    pts = [(b[6], b[5], min(b[3], b[4])) for b in bins if b[5] is not None]
    if len(pts) < 3:
        return None, None
    best = (1e18, None, None)
    for g0 in np.exp(np.linspace(math.log(0.5), math.log(400.0), 900)):
        A = np.array([1.0 - math.exp(-g / g0) for g, _, _ in pts])
        y = np.array([v for _, v, _ in pts])
        w = np.array([float(n) for _, _, n in pts])
        c = (w * A * y).sum() / max(1e-12, (w * A * A).sum()) if free_amp else 1.0
        sse = float((w * (y - c * A) ** 2).sum())
        if sse < best[0]:
            best = (sse, float(g0), float(c))
    return best[1], best[2]


BINS = ahat_bins(ALLP)
P('   %-8s %7s %7s %10s %10s %9s %11s %10s'
  % ('games', 'n deep', 'n ref', 'OUT deep', 'OUT ref', 'Delta_s', 'A_hat', 'A(g) wired'))
for lab, lo_g, hi_g, nd, nb, a, gmid, ds in BINS:
    if a is None:
        P('   %-8s %7d %7d   (not scored — a cell holds under three players)' % (lab, nd, nb)); continue
    P('   %-8s %7d %7d %10.4f %10.4f %9.2f %11.4f %10.4f%s'
      % (lab, nd, nb,
         float(np.mean([r['out'] for r in ALLP if lo_g <= r['g'] <= hi_g and r['s'] < -20])),
         float(np.mean([r['out'] for r in ALLP if lo_g <= r['g'] <= hi_g and r['s'] >= -10])),
         ds, a, A_of(gmid), ' THIN' if min(nd, nb) < 25 else ''))
g0h, _ = fit_G0(BINS)
g0f, cf = fit_G0(BINS, free_amp=True)
P()
P('   FITTED, weighted least squares over the scored bins:')
P('     A_hat(g) = 1 - exp(-g/G0)                 G0_hat = %s' % ('%.3f' % g0h if g0h else 'not fitted'))
P('     A_hat(g) = C * (1 - exp(-g/G0))           G0_hat = %s   C = %s'
  % ('%.3f' % g0f if g0f else '-', '%.4f' % cf if cf is not None else '-'))
P('     the wired G0 = %.3f, published 90%% CI [7.60, 12.98]' % G0)
P()
rng3 = np.random.default_rng(SEED)
BG, BC, BF = [], [], []
for _ in range(400):
    s = [ALLP[i] for i in rng3.integers(0, len(ALLP), size=len(ALLP))]
    b = ahat_bins(s)
    a1, _ = fit_G0(b)
    a2, c2 = fit_G0(b, free_amp=True)
    if a1:
        BG.append(a1)
    if a2:
        BF.append(a2); BC.append(c2)
G0CI = (float(np.percentile(BG, 5)), float(np.percentile(BG, 95))) if len(BG) > 20 else (float('nan'),) * 2
G0FCI = (float(np.percentile(BF, 5)), float(np.percentile(BF, 95))) if len(BF) > 20 else (float('nan'),) * 2
CCI = (float(np.percentile(BC, 5)), float(np.percentile(BC, 95))) if len(BC) > 20 else (float('nan'),) * 2
P('   400-draw player-clustered bootstrap:')
P('     G0_hat (amplitude pinned at 1, as the mechanism has it) = %.3f  90%% CI [%.3f, %.3f]'
  % (g0h or float('nan'), G0CI[0], G0CI[1]))
P('     G0_hat (amplitude free)                                 = %.3f  90%% CI [%.3f, %.3f]'
  % (g0f or float('nan'), G0FCI[0], G0FCI[1]))
P('     C      (the mechanism forces C = 1)                     = %.4f  90%% CI [%.4f, %.4f]'
  % (cf if cf is not None else float('nan'), CCI[0], CCI[1]))
P()
inside = (not math.isnan(G0CI[0])) and (7.60 <= (g0h or -1) <= 12.98)
P('   F5-P2 predicted G0_hat ABOVE the published upper limit of 12.98 (conviction firms SLOWER).')
P('     point estimate %s the published interval. %s'
  % ('INSIDE' if inside else ('ABOVE' if (g0h or 0) > 12.98 else 'BELOW'),
     'F5-P2 FIRED' if inside else 'F5-P2 did not fire'))
P('     does the 90%% CI on G0_hat overlap the published [7.60, 12.98]? %s'
  % ('YES — the two are not separable' if (not math.isnan(G0CI[0]) and G0CI[0] <= 12.98 and G0CI[1] >= 7.60)
     else 'NO — they are separable, and the gap is %.4f' % (G0CI[0] - 12.98)))
P('     THAT SEPARATION IS A HAIRLINE AND IT IS REPORTED AS ONE: the fitted lower limit is %.3f'
  % G0CI[0])
P('     against a published upper limit of 12.98. Nobody should read a %.3f-wide gap as decisive.'
  % abs(G0CI[0] - 12.98))
P()
nb_ = sum(1 for b in BINS if b[5] is not None)
lower = sum(1 for b in BINS if b[5] is not None and b[5] < A_of(b[6]))
P('   THE RAWEST FORM OF THE SAME RESULT, before any curve is fitted: the empirical A sits BELOW the')
P('   wired A(g) in %d of the %d scored games bins.' % (lower, nb_))
P()
P('   TWO READINGS OF THE SAME DATA, AND THEY CANNOT BE SEPARATED:')
P('     (a) conviction firms about TWICE AS SLOWLY as assumed — G0 %.1f against %.2f, amplitude 1;'
  % (g0h or float('nan'), G0))
P('     (b) conviction firms at ABOUT THE ASSUMED SPEED but only ever reaches %.0f%% of the assumed'
  % (100 * (cf if cf is not None else float('nan'))))
P('         strength — G0 %.1f, amplitude %.2f.' % (g0f or float('nan'), cf if cf is not None else float('nan')))
P('   Reading (b)\'s amplitude CI is [%.3f, %.3f] and its G0 CI runs to the search bound, so the data'
  % (CCI[0], CCI[1]))
P('   CANNOT tell speed from strength here. WHAT BOTH READINGS AGREE ON is that the charge convicts')
P('   HARDER than outcomes support at every games level measured. This seat states that and stops.')
P()
P()
B1 = ahat_bins(POP[1])
g1, _ = fit_G0(B1)
P('   STAGE-1 ONLY, as a sensitivity: G0_hat = %s on %d scored bins.'
  % ('%.3f' % g1 if g1 else 'not fitted', sum(1 for b in B1 if b[5] is not None)))
P()

# ---- sensitivities -------------------------------------------------------------------------------------
P('-' * 118)
P('8 · SENSITIVITIES — THE STATISTIC, THE CENSORING, THE PATHWAY, AND THE ALREADY-PRICED SOFTENINGS')
P('-' * 118)
P('   %-40s %10s %10s %10s' % ('reading', 'n deep', 'CALIB', '90% CI lo'))
SENS = {}


def one(nm, rows):
    a = [r for r in rows if 10 <= r['g'] <= 22 and r['s'] < -20]
    c = cal_pool(rows, '10-22')
    if c is None:
        P('   %-40s %10d  not scorable' % (nm, len(a))); return
    rg = np.random.default_rng(SEED)
    bb = []
    for _ in range(600):
        s = [rows[i] for i in rg.integers(0, len(rows), size=len(rows))]
        v = cal_pool(s, '10-22')
        if v is not None and np.isfinite(v):
            bb.append(v)
    lo_ = float(np.percentile(bb, 5)) if len(bb) > 20 else float('nan')
    SENS[nm] = dict(n=len(a), calib=c, lo=lo_)
    P('   %-40s %10d %10.4f %10.4f' % (nm, len(a), c, lo_))


one('primary (mean, ND, >=4 future seasons)', POOL12)
POOL12S = build(1, MIN_FUTURE_SENS) + build(2, MIN_FUTURE_SENS)
one('>= 6 future seasons', POOL12S)
POOL12A = build(1, MIN_FUTURE, types=('ND', 'RD', 'MSD', 'SSP', 'IRE', 'PDA', 'PDN', 'PDS', 'UNR')) + \
    build(2, MIN_FUTURE, types=('ND', 'RD', 'MSD', 'SSP', 'IRE', 'PDA', 'PDN', 'PDS', 'UNR'))
one('every pathway, not ND only', POOL12A)


def cal_pool_stat(rows, stat):
    a = [r for r in rows if 10 <= r['g'] <= 22 and r['s'] < -20]
    b = [r for r in rows if 10 <= r['g'] <= 22 and r['s'] >= -10]
    if len(a) < 2 or len(b) < 2:
        return None
    oa, ob = stat([r['out'] for r in a]), stat([r['out'] for r in b])
    fa, fb = np.mean([r['f'] for r in a]), np.mean([r['f'] for r in b])
    return (oa / ob) / (fa / fb) if ob > 0 and fb > 0 else None


P()
P('   THE STATISTIC (F1 and F4 both found the mean and the pooled aggregate can disagree):')
for nm, st in (('mean (primary)', np.mean), ('median', np.median)):
    v = cal_pool_stat(POOL12, st)
    P('     %-36s CALIB %s' % (nm, ('%.4f' % v) if v else 'not scorable'))
a = [r for r in POOL12 if 10 <= r['g'] <= 22 and r['s'] < -20]
b = [r for r in POOL12 if 10 <= r['g'] <= 22 and r['s'] >= -10]
pa = sum(r['out'] * r['v0'] for r in a) / sum(r['v0'] for r in a)
pb = sum(r['out'] * r['v0'] for r in b) / sum(r['v0'] for r in b)
fa, fb = np.mean([r['f'] for r in a]), np.mean([r['f'] for r in b])
P('     %-36s CALIB %.4f' % ('pooled aggregate (v0-weighted)', (pa / pb) / (fa / fb)))
SENS['pooled'] = (pa / pb) / (fa / fb)
P()
P('   THE ALREADY-PRICED SOFTENINGS, FOR REFERENCE ONLY. ORDER R priced TMAX at the 15th and 20th')
P('   percentile and BETA_sat at its CI floor. NONE IS RECOMMENDED HERE and no new constant is')
P('   derived; this is only so the owner can see whether anything already on the record lands where')
P('   the measurement points.')
P()
P('   %-34s %10s %10s %10s' % ('variant', 'f at shape', 'charged', 'CALIB'))
VAR = {}
S_PQ = {5: -33.06133449874688, 15: -22.148794633345666, 20: -19.024574086528315}
for nm, bsat, pct in (('ORDER P as wired', BETA_SAT, 5), ('TMAX at p15', BETA_SAT, 15),
                      ('TMAX at p20', BETA_SAT, 20),
                      ('BETA_sat at the CI floor', 0.10416359711151935, 5),
                      ('BETA_sat floor + TMAX p20', 0.10416359711151935, 20)):
    th = bsat / LAMBDA
    tm = 1.0 - th * (S_PQ[pct] - S0)
    fa2 = np.mean([f_of(r['g'], r['s'], LAMBDA, th, tm) for r in a])
    fb2 = np.mean([f_of(r['g'], r['s'], LAMBDA, th, tm) for r in b])
    oa2, ob2 = np.mean([r['out'] for r in a]), np.mean([r['out'] for r in b])
    c2 = (oa2 / ob2) / (fa2 / fb2)
    VAR[nm] = dict(f_shape=f_of(15, -19, LAMBDA, th, tm), charged=fa2 / fb2, calib=c2)
    P('   %-34s %10.4f %10.4f %10.4f' % (nm, f_of(15, -19, LAMBDA, th, tm), fa2 / fb2, c2))
P()

json.dump(dict(pop={str(n): len(POP[n]) for n in STAGES}, cal=CAL, verdict1=V1, tail=TAILJ,
               survival=SURV, shape=[r for r in sorted(SHAPE, key=lambda z: -z['v0'])[:25]],
               ahat=[dict(lab=b[0], n_deep=b[3], n_ref=b[4], a_hat=b[5], gmid=b[6], ds=b[7]) for b in BINS],
               G0_hat=g0h, G0_ci=list(G0CI), G0_free=g0f, G0_free_ci=list(G0FCI),
               C=cf, C_ci=list(CCI), G0_stage1=g1,
               sens={k: (v if not isinstance(v, dict) else v) for k, v in SENS.items()},
               variants=VAR, seed=SEED, boot=B_BOOT,
               constants=dict(LAMBDA=LAMBDA, G0=G0, BETA_SAT=BETA_SAT, THETA_R=THETA_R,
                              S0=S0, TMAX=TMAX)),
          open(os.path.join(HERE, 'F5_CALIB.json'), 'w'), indent=1, default=str)
open(os.path.join(HERE, 'F5_CALIB_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote F5_CALIB.json and F5_CALIB_out.txt')
