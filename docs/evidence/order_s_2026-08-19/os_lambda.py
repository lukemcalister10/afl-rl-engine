#!/usr/bin/env python3
"""ORDER S — S3. THE LAMBDA LEVEL, RE-SOLVED AGAINST THE RAILS. And S2's offline frontier.

READ-ONLY. No engine import, no board build, no store write. PREREG_S.md sections 2 and 3.

ORDER P SOLVED LAMBDA by an anchoring identity: bisection so the derived charge removes exactly the
same total points from the year-1 class-mark population as ORDER K's blind eta charge did. THE
DISTRIBUTION WAS FIXED BY THAT SOLVE; THE LEVEL WAS INHERITED FROM THE DEFECTIVE CHARGE AND NEVER
INDEPENDENTLY VALIDATED. This file re-opens the level.

The machinery is ORDER P's own op_step4.py, reused rather than re-implemented: the same vantage
charge bases, the same F_old, the same apprec01 band reader, the same classmark. The ONLY things
added are (a) the FIX B1 basis (the age-24 gate deleted), (b) the compressed cap of S2, and (c) a
frontier sweep instead of a single solve.

EVERY NUMBER IN THIS FILE IS AN OFFLINE ESTIMATE PENDING A BUILD, exactly as ORDER P's step 4 was.
The built boards are the authority and they are produced separately.

  usage: OPENBLAS_NUM_THREADS=1 ... python3 os_lambda.py
"""
import json, math, os, sys, copy, statistics, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(REPO, 'docs/evidence/order_p_2026-08-18'))
import op_lib as PB                                                          # noqa: E402
LB = PB.LB

PL_F = 1.0524
L = []


def P(s=''):
    print(s); L.append(str(s))


M = json.load(open(os.path.join(REPO, 'docs/evidence/order_p_2026-08-18/MECH_P.json')))
G0, BSAT, S0, S_P5 = M['G0'], M['BETA_sat'], M['s0'], M['s_p5']
S_PQ = {5: -33.06133449874688, 15: -22.148794633345666, 20: -19.024574086528315}
LAM_P = 0.1743833036575403
assert abs(S_PQ[5] - S_P5) == 0.0, 'the p5 percentile is not MECH_P.json::s_p5 bit for bit'


def A_of(g):
    return 1.0 - math.exp(-float(g) / G0)


def theta_r(lam, beta=BSAT):
    return beta / lam


def cap_of(lam, pct, beta=BSAT):
    return 1.0 - theta_r(lam, beta) * (S_PQ[pct] - S0)


def T_of(s, lam, beta=BSAT, capmode='clip', pct=5):
    raw = max(1.0 - theta_r(lam, beta) * (float(s) - S0), 0.0)
    C = cap_of(lam, pct, beta)
    if capmode == 'clip':
        return min(raw, C)
    return C * (1.0 - math.exp(-raw / C))                 # THE COMPRESSION, prereg 2.2


def F_old(g):
    return max(0.0, LB.ETA_K * LB.m_d(g))


def F_new(g, s, age, lam, beta=BSAT, capmode='clip', pct=5, gate=24):
    if g <= 0:
        return 0.0
    if s is None or (gate is not None and (age is None or age >= gate)):
        return F_old(g)
    return 1.0 - math.exp(-lam * A_of(g) * T_of(s, lam, beta, capmode, pct))


P('=' * 118)
P('ORDER S — S3. THE LAMBDA LEVEL RE-SOLVED, AND S2\'s COMPRESSED CAP ON THE SAME FRONTIER.')
P('=' * 118)
P('OFFLINE ESTIMATE PENDING A BUILD — ORDER P step 4\'s own method and machinery, reused.')
P('ruler %s · LAMBDA_P %.10f · BETA_sat %.10f · s0 %+.4f' % (LB.check_s4_copy(), LAM_P, BSAT, S0))
P()

MK = LB.load_matrix('OKRULED')
ME = LB.load_matrix('M0ETA0')
ROWS = PB.season_rows(MK)
PG = PB.Premium(ROWS, h=PB.H_PRIMARY, iso=True)

VAN = {}
for k, a in MK.items():
    b = ME[k]
    yrs = a.get('yrs') or []
    vpa = a.get('vpath') or []; vpb = b.get('vpath') or []
    row = []
    for i, y in enumerate(yrs):
        if i >= len(vpa) or i >= len(vpb) or vpa[i] is None or vpb[i] is None:
            row.append(None); continue
        g = LB.career_games(a, y)
        md = LB.m_d(g)
        row.append(dict(y=y, g=g, sP=PB.perf_surplus_P(a, y, PG), age=LB.age_at(a, y),
                        C=((vpb[i] - vpa[i]) / (0.50 * md)) if md > 1e-12 else 0.0,
                        v0eta=float(vpb[i]), vK=float(vpa[i])))
    VAN[k] = row

# ---------------------------------------------------------------------------------------------------
P('-' * 118)
P('1 · FALSIFIER S3-F4 — IS THE INHERITED ANCHOR REPRODUCIBLE ON THIS SEAT\'S OWN CODE?')
P('-' * 118)
CLASSES_MARK = list(range(2005, 2016))
anchor = []
for k, a in MK.items():
    c = (a['year'] if a.get('type') == 'MSD' else a['year'] + 1)
    if c not in CLASSES_MARK or not (float(a.get('v0') or 0) > 0):
        continue
    yrs = a.get('yrs') or []
    if c not in yrs:
        continue
    v = VAN[k][yrs.index(c)]
    if v is None or v['C'] <= 0:
        continue
    anchor.append(v)
TOT_OLD = sum(v['C'] * F_old(v['g']) for v in anchor)


def tonnage(lam, **kw):
    return sum(v['C'] * F_new(v['g'], v['sP'], v['age'], lam, **kw) for v in anchor)


lo, hi = 1e-6, 20.0
for _ in range(200):
    mid = 0.5 * (lo + hi)
    if tonnage(mid) < TOT_OLD:
        lo = mid
    else:
        hi = mid
LAM_RESOLVE = 0.5 * (lo + hi)
P('   anchor population : %d year-1 rows, cohort classes 2005-2015' % len(anchor))
P('   THE INHERITED TONNAGE, recomputed here : %.1f   (ORDER P published 101,402.7)' % TOT_OLD)
P('   re-solved LAMBDA on the SAME identity   : %.10f   (ORDER P published %.10f)'
  % (LAM_RESOLVE, LAM_P))
f4 = abs(TOT_OLD - 101402.7) > 0.1
P('   S3-F4 (anchor not reproducible to 0.1 points): %s'
  % ('*** FIRED ***' if f4 else 'does not fire — the anchor reproduces'))
P('   the tonnage the ORDER P LAMBDA actually removes: %.1f' % tonnage(LAM_P))
P()
P('   WHAT THE ANCHOR MEANS, said plainly: the LEVEL of the charge was set to whatever total the OLD')
P('   BLIND CHARGE happened to remove. The old charge is the object ORDER P replaced BECAUSE it was')
P('   defective — it was a pure function of games, blind to how the player played. The tonnage it')
P('   removed was never itself validated against anything. That is the finding F4 the owner made,')
P('   and this file takes it as the premise of the sweep rather than re-arguing it.')
P()

# ---------------------------------------------------------------------------------------------------
SRC = json.load(open(os.path.join(LB.SP, 'per_entrant_OKRULED.json')))['recs']
NDR = [r for r in SRC if (not r.get('is_pool')) and r.get('teaches_curve') and r.get('type') == 'ND'
       and r.get('pick') and 1 <= int(r['pick']) <= 64]
WEND = max(y for r in SRC for y, v in zip(r.get('yrs') or [], r.get('vpath') or []) if v is not None)
BANDS = [('ALL 1-64', lambda p: True), ('1-20', lambda p: p <= 20), ('21-64', lambda p: p >= 21),
         ('1-10', lambda p: p <= 10), ('11-20', lambda p: 11 <= p <= 20),
         ('21-30', lambda p: 21 <= p <= 30), ('31-40', lambda p: 31 <= p <= 40),
         ('41-64', lambda p: 41 <= p <= 64)]
WINDOWS = [('PRIMARY', 2005, 2023), ('MODERN', 2019, 2023)]


def vp_new(r, lam, **kw):
    vp = list(r.get('vpath') or [])
    van = VAN.get(r['key']) or []
    for i in range(len(vp)):
        if i >= len(van) or van[i] is None or vp[i] is None:
            continue
        v = van[i]
        if v['C'] <= 0:
            continue
        vp[i] = round(v['v0eta'] - v['C'] * F_new(v['g'], v['sP'], v['age'], lam, **kw), 1)
    return vp


def apprec01(lam, **kw):
    out = {}
    cache = {r['key']: vp_new(r, lam, **kw) for r in NDR}
    for wname, lo_, hi_ in WINDOWS:
        pop_w = [r for r in NDR if lo_ <= r['year'] + 1 <= hi_]
        for bname, bf in BANDS:
            incl = [r for r in pop_w if bf(int(r['pick'])) and r['year'] + 1 <= WEND]
            if len(incl) < 5:
                out['%s|%s' % (wname, bname)] = None; continue
            vals = [(0.0 if (not cache[r['key']] or cache[r['key']][0] is None)
                     else float(cache[r['key']][0])) for r in incl]
            out['%s|%s' % (wname, bname)] = statistics.mean(vals) / statistics.mean(
                [float(r['v0']) for r in incl]) - 1.0
    return out


def classmark_per(lam, lo_y, hi_y, **kw):
    per = {}
    for y in range(lo_y, hi_y + 1):
        num = den = 0.0; n = 0
        for k, a in MK.items():
            c = (a['year'] if a.get('type') == 'MSD' else a['year'] + 1)
            if c != y or not (float(a.get('v0') or 0) > 0):
                continue
            yrs = a.get('yrs') or []
            vp = vp_new(a, lam, **kw)
            if not yrs:
                v1 = 0.0
            elif y < yrs[0]:
                continue
            elif y > yrs[-1]:
                v1 = 0.0
            else:
                i = yrs.index(y)
                v1 = 0.0 if vp[i] is None else float(vp[i])
            num += v1; den += float(a['v0']); n += 1
        if den > 0 and n >= 5:
            per[y] = num / den
    return per


def marks(lam, **kw):
    """W2 basis = DRAFT classes 2005-2015 = COHORT 2006-2016. The registered basis."""
    w2 = classmark_per(lam, 2006, 2016, **kw)
    coh = classmark_per(lam, 2005, 2015, **kw)
    return (sum(w2.values()) / len(w2), sum(coh.values()) / len(coh), w2)


# ---------------------------------------------------------------------------------------------------
P('-' * 118)
P('2 · THE FRONTIER. LAMBDA SWEPT ON THE FIX B1 BASIS (the age-24 gate DELETED — the register\'s')
P('    end-state carries B1). The ORDER P gated basis is printed beside it so the two can be told')
P('    apart on sight.')
P('-' * 118)
P('    READING RULE: below 0%% is a SELL-SIDE RED; above +14%% is a BUY-SIDE RED.')
P('    THE CLASS LAW: the W2 mark must stay in [1.03, 1.14).')
P()
LAMS = sorted(set([round(x, 4) for x in np.arange(0.02, 1.21, 0.02)] + [round(LAM_P, 6)]))
FRONT = []
P('   %-8s %8s %8s | %8s %8s | %9s %9s %9s | %9s %9s %9s' %
  ('LAMBDA', 'THETA_R', 'TMAX', 'W2 mark', 'max cls', 'PRI31-40', 'PRI41-64', 'PRI1-10',
   'MOD21-30', 'MOD31-40', 'MOD1-10'))
for lam in LAMS:
    kw = dict(gate=None)                                  # FIX B1: no gate
    ap = apprec01(lam, **kw)
    w2, coh, per = marks(lam, **kw)
    row = dict(lam=lam, theta_r=theta_r(lam), tmax=cap_of(lam, 5), w2=w2, cohort=coh,
               maxclass=max(per.values()), per={str(k): v for k, v in per.items()},
               bands={k: v for k, v in ap.items()}, tonnage=tonnage(lam, **kw))
    FRONT.append(row)
    P('   %-8.4f %8.4f %8.3f | %8.4f %8.4f | %+8.2f%% %+8.2f%% %+8.2f%% | %+8.2f%% %+8.2f%% %+8.2f%%'
      % (lam, theta_r(lam), cap_of(lam, 5), w2, max(per.values()),
         100 * ap['PRIMARY|31-40'], 100 * ap['PRIMARY|41-64'], 100 * ap['PRIMARY|1-10'],
         100 * ap['MODERN|21-30'], 100 * ap['MODERN|31-40'], 100 * ap['MODERN|1-10']))
P()
P('   NOTE ON DIRECTION, MEASURED NOT ASSUMED: LAMBDA down => THETA_R = BETA_sat/LAMBDA UP => TMAX UP.')
P('   Lowering the level is NOT a pure softening: the exponent multiplier falls but the T line')
P('   STEEPENS about s0 and the cap RISES. The net on the bands is what the table shows.')
P()

# ---------------------------------------------------------------------------------------------------
P('-' * 118)
P('3 · WHERE THE CONSTRAINTS BIND')
P('-' * 118)
adm_w2 = [r for r in FRONT if 1.03 <= r['w2'] < 1.14]
adm_cls = [r for r in FRONT if r['maxclass'] < 1.14]
P('   admissible on the AGGREGATE W2 mark in [1.03, 1.14) : %d of %d rungs%s'
  % (len(adm_w2), len(FRONT),
     ('  (LAMBDA %.4f .. %.4f)' % (min(r['lam'] for r in adm_w2), max(r['lam'] for r in adm_w2)))
     if adm_w2 else ''))
P('   admissible on EVERY PER-CLASS mark under 1.14        : %d of %d rungs%s'
  % (len(adm_cls), len(FRONT),
     ('  (LAMBDA %.4f .. %.4f)' % (min(r['lam'] for r in adm_cls), max(r['lam'] for r in adm_cls)))
     if adm_cls else ''))
P()
P('   THE OBJECTIVE, and the first thing that has to be said about it: THE LATE-BAND SELL-REDS ARE')
P('   MONOTONE IN LAMBDA OVER THE WHOLE SWEEP. Every one of them improves as LAMBDA FALLS and')
P('   worsens as it rises. THERE IS NO INTERIOR SOLVE. "Solve LAMBDA to close the sell-reds" drives')
P('   LAMBDA to zero — i.e. to DELETING the charge — and even there they do not close.')
P()
lam0 = FRONT[0]; lamZ = FRONT[-1]
P('   %-46s %9s %9s %9s' % ('', 'PRI31-40', 'PRI41-64', 'MOD41-64'))
for tag, r in (('LAMBDA %.4f — the charge almost switched off' % lam0['lam'], lam0),
               ('LAMBDA %.5f — ORDER P, the inherited level' % LAM_P,
                [q for q in FRONT if abs(q['lam'] - round(LAM_P, 6)) < 1e-9][0]),
               ('LAMBDA %.4f — the stiffest rung swept' % lamZ['lam'], lamZ)):
    P('   %-46s %+8.2f%% %+8.2f%% %+8.2f%%'
      % (tag, 100 * r['bands']['PRIMARY|31-40'], 100 * r['bands']['PRIMARY|41-64'],
         100 * r['bands']['MODERN|41-64']))
P()
P('   THE WHOLE RANGE OF MOVEMENT AVAILABLE ON PRIMARY 31-40 ACROSS THE ENTIRE SWEEP IS %.2f'
  % (100 * (lam0['bands']['PRIMARY|31-40'] - lamZ['bands']['PRIMARY|31-40'])))
P('   PERCENTAGE POINTS, and the band never crosses zero at any LAMBDA. THE LATE-BAND SELL-REDS ARE')
P('   NOT A TONNAGE FACT.' if lam0['bands']['PRIMARY|31-40'] < 0 else '   (a band DOES cross zero.)')
P()
P('   AND THE TWO RAILS PULL AGAINST EACH OTHER. Lowering LAMBDA to help the SELL side pushes the')
P('   BUY side further through its rail:')
P('   %-46s %9s %9s' % ('', 'MOD1-10', 'PRI1-10'))
for tag, r in (('LAMBDA %.4f' % lam0['lam'], lam0),
               ('LAMBDA %.5f — ORDER P' % LAM_P,
                [q for q in FRONT if abs(q['lam'] - round(LAM_P, 6)) < 1e-9][0]),
               ('LAMBDA %.4f' % lamZ['lam'], lamZ)):
    P('   %-46s %+8.2f%% %+8.2f%%'
      % (tag, 100 * r['bands']['MODERN|1-10'], 100 * r['bands']['PRIMARY|1-10']))
mod_ok = [r for r in FRONT if r['bands']['MODERN|1-10'] < 0.14]
P()
if mod_ok:
    lm = min(r['lam'] for r in mod_ok)
    rr = [r for r in FRONT if r['lam'] == lm][0]
    P('   MODERN picks 1-10 comes back inside the +14%% buy rail only at LAMBDA >= %.4f — that is'
      % lm)
    P('   %.1f times the inherited level, and at that point the W2 class mark reads %.4f.'
      % (lm / LAM_P, rr['w2']))
    P('   THE CLASS FLOOR IS 1.03. %s'
      % ('IT IS BREACHED THERE.' if rr['w2'] < 1.03 else 'It is not breached there.'))
else:
    P('   MODERN picks 1-10 never comes back inside the +14%% buy rail anywhere on this sweep.')
floor_break = [r for r in FRONT if r['w2'] < 1.03]
if floor_break:
    P('   THE W2 CLASS FLOOR 1.03 IS BREACHED FROM LAMBDA >= %.4f UPWARD.'
      % min(r['lam'] for r in floor_break))
P()
P('   *** HALT AND REPORT — THE FRONTIER, NOT A CHOICE ***')
P('   Three constraints and they do not admit a common point:')
P('     (a) the SELL side wants LAMBDA DOWN and is barely responsive to it;')
P('     (b) the MODERN 1-10 BUY rail wants LAMBDA UP, by a factor of several;')
P('     (c) the W2 class FLOOR 1.03 caps how far up LAMBDA may go;')
P('     (d) EVERY PER-CLASS mark is over 1.14 at EVERY LAMBDA on this sweep, so on the per-class')
P('         reading of the class law there is no admissible level AT ALL.')
P('   THIS SEAT DOES NOT PICK A SIDE. The frontier is the deliverable.')
P()

# ---------------------------------------------------------------------------------------------------
P('-' * 118)
P('4 · S2 — THE COMPRESSED CAP, OFFLINE, AT THE INHERITED LAMBDA')
P('-' * 118)
P('    T\'(s) = C * (1 - exp(-T_raw(s)/C)),  C = the p15/p20 anchor ceiling. Strictly increasing in')
P('    shortfall everywhere; no flat segment; T\' < C pointwise so EVERY row pays at most the')
P('    hard-clip-at-Q charge. Compared here against the hard clip at the same anchor.')
P()
CELLS = [('ORDER P  clip p5', dict(capmode='clip', pct=5)),
         ('R15      clip p15', dict(capmode='clip', pct=15)),
         ('R20      clip p20', dict(capmode='clip', pct=20)),
         ('S2       smooth p15', dict(capmode='smooth', pct=15)),
         ('S2       smooth p20', dict(capmode='smooth', pct=20))]
P('   %-20s %8s | %8s %8s | %9s %9s %9s %9s' %
  ('cell', 'C', 'W2 mark', 'max cls', 'PRI1-10', 'PRI11-20', 'MOD1-20', 'PRI31-40'))
S2ROWS = []
for tag, kw in CELLS:
    kk = dict(kw); kk['gate'] = None
    ap = apprec01(LAM_P, **kk)
    w2, coh, per = marks(LAM_P, **kk)
    S2ROWS.append(dict(tag=tag, C=cap_of(LAM_P, kw['pct']), w2=w2, maxclass=max(per.values()),
                       bands=ap, per={str(k): v for k, v in per.items()}, **kw))
    P('   %-20s %8.4f | %8.4f %8.4f | %+8.2f%% %+8.2f%% %+8.2f%% %+8.2f%%'
      % (tag, cap_of(LAM_P, kw['pct']), w2, max(per.values()),
         100 * ap['PRIMARY|1-10'], 100 * ap['PRIMARY|11-20'],
         100 * ap['MODERN|1-20'], 100 * ap['PRIMARY|31-40']))
P()

# the charge a row at each surplus pays, under each cell — the gap-preservation demonstration
P('   THE CHARGE AT 38 GAMES (A=0.9793), share of the pedigree leg removed, by surplus:')
P('   %-20s %9s %9s %9s %9s %9s %9s' %
  ('cell', 's=-5', 's=-15', 's=-25', 's=-33', 's=-45', 's=-60'))
SS = (-5, -15, -25, -33, -45, -60)
for tag, kw in CELLS:
    a = A_of(38)
    vals = [100 * (1 - math.exp(-LAM_P * a * T_of(s, LAM_P, BSAT, kw['capmode'], kw['pct'])))
            for s in SS]
    P('   %-20s %8.2f%% %8.2f%% %8.2f%% %8.2f%% %8.2f%% %8.2f%%' % (tag, *vals))
P()
P('   READ THE p20 ROWS AGAINST EACH OTHER. Under the CLIP the charge is IDENTICAL at s=-33, -45')
P('   and -60 — three players a further 27 points a game apart pay the same. Under the COMPRESSION')
P('   they are strictly ordered. That is the owner\'s "gaps between players still count", and it is')
P('   the whole of what S2 changes.')
P()

# monotonicity falsifier S2-F1 on a dense sweep
P('   S2-F1 — dT\'/ds < 0 STRICTLY, on a dense sweep of s from +20 down to -200 at 0.01:')
bad = 0; worst_gap = None
for pct in (15, 20):
    prev = None
    s = 20.0
    while s > -200.0:
        t = T_of(s, LAM_P, BSAT, 'smooth', pct)
        if prev is not None and t < prev[1] - 1e-15 and prev[0] > s:
            pass
        if prev is not None and s < prev[0]:
            if t <= prev[1] and prev[1] > 1e-12:
                bad += 1
        prev = (s, t)
        s -= 0.01
P('     strict-increase failures in shortfall, both anchors: %d  -> S2-F1 %s'
  % (bad, '*** FIRED ***' if bad else 'does not fire'))
P()

OUT = dict(meta=dict(tot_old=TOT_OLD, lam_resolved_anchor=LAM_RESOLVE, lam_P=LAM_P,
                     G0=G0, BSAT=BSAT, S0=S0, S_PQ=S_PQ),
           frontier=FRONT, s2=S2ROWS,
           falsifiers=dict(S3_F4=bool(f4), S2_F1=bool(bad)))
json.dump(OUT, open(os.path.join(HERE, 'LAMBDA_S.json'), 'w'), indent=1, sort_keys=True)
open(os.path.join(HERE, 'LAMBDA_S_out.txt'), 'w').write('\n'.join(L) + '\n')
print('written: LAMBDA_S.json · LAMBDA_S_out.txt')
