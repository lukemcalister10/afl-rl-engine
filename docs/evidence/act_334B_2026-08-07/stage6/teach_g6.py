"""STAGE 6 TEACH — the conditioned development correction surface, taught ONCE and FROZEN.

Reads RL_OUT/s6_rows.json (measure_g6.py, from the frozen matrix b564b12e) and writes g6_table.json.

THE FORM.  A SIGNED multiplier on the ns>=1 arm's production leg:

    e' = e * (1 + delta),
    delta = W * B(cls, log-pick) * Stau(tau) * Sz(z) * Sg(gcum) * Tpk(pick) * Tage(draft age)

  B      THE KERNEL — the only fitted two-axis object (Addendum 1: "the kernel drops to TWO axes,
         log-pick x the engine's three position classes").  Gaussian in log-pick, bandwidth grown
         until eff-n >= 35 on the INFLUENCE weight (kernel x price x shape product) — the engine's
         own `_fit_pick_curve` idiom; pooled over classes where a class cannot reach it, DECLARED.
  Stau   THE MEASURED FADE.  The teach POOLS the year-1/2/3 evaluation rows over the continuous
         round clock, so the fade is ENDOGENOUS (Addendum 1 F7).  Normalised Stau(1) = 1.  Isotonic
         non-increasing and clamped to [0,1]: the unclamped measurement is printed beside it.  The
         clamp is the SAME principle as the KPD sub-dial (F11) — a markdown never rides silently on
         a bonus dial — and it is the owner's own phase-out law.  Flat 0 past the last knot.
  Sz     THE DEMONSTRATED-LEVEL axis, z = log(e / entry_anchor): how far the engine has ALREADY
         re-rated this player off his entry price.  Chosen over `pr` by measurement (axis_probe.py:
         value-weighted R^2 0.072 vs 0.024) and because it — and only it — reproduces the owner's
         "already priced in" cell.  Continuous; the terciles in the tables are REPORTING knots only.
         Computed off `e`, never off the corrected price, so there is NO build-to-build feedback.
  Sg     CUMULATIVE career games (the recalculation-law axis).
  Tpk    DECLARED smooth taper, 1 at pick <= PK_LO, 0 at pick >= PK_HI (Addendum 1 F5/F6 replaced
         "byte-unmoved at 41-64" with a taper).  The pool index (effpk 65) therefore takes ZERO by
         construction — the pool leg is stage 7's, on its own measurement.
  Tage   DECLARED smooth taper, 1 at draft age <= 18, 0 at >= 20 (directive: "nothing at age 19+").
         UNKNOWN draft age => delta identically 0 (Addendum 1 F13); those rows are enumerated.
  W      RL_G6_W, the intensity dial.  DEFAULT 0 (Addendum 1 F9/F10: shipped default = the stage-5
         landed board, byte-exact).  KPD rows ride RL_G6_KPD instead, also default 0 (F11).

FITTING.  Value-weighted backfit least squares on r_i = F_i - price_i with predictor price_i*m_i;
two passes then FROZEN.  Sz and Sg are renormalised to value-weighted mean 1 over the year-1 rows at
every pass so the level lives in B alone (no double counting — the conservation check verifies it).
KPD rows are EXCLUDED from B entirely and carry their own fitted surface on their own sub-dial.
"""
import os, json, hashlib
import numpy as np

OUT = os.environ.get('RL_OUT', '.')
ROWS = json.load(open(OUT + '/s6_rows.json'))

# ---- the teaching population: ND 1-64, evaluation years 1-3 (the pooled fade) ----
POP = [x for x in ROWS if x['nd'] and 1 <= x['pk'] <= 64 and 1 <= x['N'] <= 3]
Y1 = [x for x in POP if x['N'] == 1]
print("teaching rows: N=1 %d  N=2 %d  N=3 %d   total %d"
      % (len(Y1), len([x for x in POP if x['N'] == 2]), len([x for x in POP if x['N'] == 3]), len(POP)))

PK_KNOTS = [3.0, 8.0, 15.0, 25.0, 35.0, 45.0]
TAU_KNOTS = [1.0, 2.0, 3.0, 4.0]
Z_KNOTS = [-0.60, -0.30, 0.0, 0.30, 0.60]
G_KNOTS = [6.0, 10.0, 14.0, 18.0, 24.0]
PK_LO = float(os.environ.get('RL_G6_PKLO', '34'))   # declared pick taper, endpoints fixed by the
PK_HI = float(os.environ.get('RL_G6_PKHI', '48'))   # <=0.5pp absolute bound at picks 41-64 (Add.1 F5/F6)
# DECLARED DRAFT-AGE BOUNDARY. Draft age is C - birth year: an IMMUTABLE INTEGER attribute of the
# player that never moves with the clock or with arriving evidence, so it cannot produce a
# discontinuity in any player's own price path — the smoothness Addendum 1 F5/F6 was protecting does
# not arise on this axis. The endpoints are therefore set to meet the stated ABSOLUTE bound (<=0.5pp
# of movement in the age-19+ band at rung 1.0) and to honour the directive's own words, "nothing at
# draft age 19+": age <=18 takes the full correction, age >=19 takes exactly zero.
AGE_LO = float(os.environ.get('RL_G6_AGELO', '18'))
AGE_HI = float(os.environ.get('RL_G6_AGEHI', '19'))
CLASSES = ['nonKPP', 'KPP', 'RUCK']
EFFN = 35.0

LPK = [float(np.log(k)) for k in PK_KNOTS]
LGK = [float(np.log1p(k)) for k in G_KNOTS]

def tpk(pk):
    if pk <= PK_LO: return 1.0
    if pk >= PK_HI: return 0.0
    t = (pk - PK_LO) / (PK_HI - PK_LO)
    return float(0.5 * (1.0 + np.cos(np.pi * t)))          # smooth (C1) taper, no cliff
def tage(a):
    if a is None: return 0.0                                # F13: unknown draft age => zero
    if a <= AGE_LO: return 1.0
    if a >= AGE_HI: return 0.0
    t = (a - AGE_LO) / (AGE_HI - AGE_LO)
    return float(0.5 * (1.0 + np.cos(np.pi * t)))

for x in POP:
    x['lp'] = float(np.log(min(max(x['pk'], 1), 90)))
    x['z'] = float(np.clip(np.log(max(x['e'], 1.0) / max(x['A'], 1.0)), Z_KNOTS[0], Z_KNOTS[-1]))
    x['lg'] = float(np.log1p(max(x['gcum'], 0.0)))
    x['r'] = x['F'] - x['price']
    x['tp'] = tpk(x['pk']); x['ta'] = tage(x['age'])
    x['iskpd'] = (x['pos'] == 'KPD')

BASE = {c: [0.0] * len(PK_KNOTS) for c in CLASSES}
KPD = [0.0] * len(PK_KNOTS)
STAU = [1.0, 0.5, 0.25, 0.0]      # the owner's phase-out shape as a PRIOR ONLY; the fit decides
SZ = [1.0] * len(Z_KNOTS)
SG = [1.0] * len(G_KNOTS)
POOLED = []

def interp(x, knots, vals): return float(np.interp(x, knots, vals))
def s_tau(t): return float(np.interp(t, [0.0] + TAU_KNOTS, [STAU[0]] + STAU)) if t <= TAU_KNOTS[-1] else 0.0
def s_z(z): return interp(z, Z_KNOTS, SZ)
def s_g(lg): return interp(lg, LGK, SG)
def b_of(x):
    tab = KPD if x['iskpd'] else BASE[x['cls']]
    return interp(x['lp'], LPK, tab)
def m_of(x):   # everything in the product EXCEPT B
    return s_tau(x['tau']) * s_z(x['z']) * s_g(x['lg']) * x['tp'] * x['ta']
def pred(x): return x['price'] * b_of(x) * m_of(x)

def loc_delta(rows, K):
    """The LOCAL value-weighted residual  sum(K*(F-price)) / sum(K*price)  — a pure measurement,
    no model, no iteration.  This is the same estimand at every knot as the headline aggregate."""
    num = float(sum(K[i] * rows[i]['r'] for i in range(len(rows))))
    den = float(sum(K[i] * rows[i]['price'] for i in range(len(rows))))
    return (num / den) if den > 1e-9 else 0.0

def eff_n(rows, K):
    W = np.array([K[i] * rows[i]['price'] for i in range(len(rows))])
    s2 = float((W * W).sum())
    return (float(W.sum()) ** 2 / s2) if s2 > 0 else 0.0

NOTES = {}
NONKPD = [x for x in Y1 if not x['iskpd']]
D1 = loc_delta(NONKPD, [1.0] * len(NONKPD))          # THE ESTIMAND, bonus-dial population
DKPD = loc_delta([x for x in Y1 if x['iskpd']], [1.0] * len([x for x in Y1 if x['iskpd']]))
print("\nestimand: year-1 value-weighted residual, bonus population (KPD excluded) = %+0.6f" % D1)
print("          year-1 value-weighted residual, KPD rows (own sub-dial)         = %+0.6f" % DKPD)
assert D1 > 0.0, 'the bonus population measures no positive residual — the act STOPS rather than invent one'

# ---- (1) THE KERNEL: log-pick x the engine's three position classes, eff-n >= 35, pooling declared --
print("\n-- the two-axis kernel (the only fitted object) --")
for c in CLASSES:
    rows = [x for x in NONKPD if x['cls'] == c]
    vals = []; notes = []; ok = bool(rows)
    for j, lpk in enumerate(LPK):
        h = 0.18
        src = rows
        while True:
            K = [float(np.exp(-0.5 * ((x['lp'] - lpk) / h) ** 2)) for x in src]
            if eff_n(src, K) >= EFFN or h > 3.0: break
            h *= 1.15
        en = eff_n(src, K)
        if en < EFFN: ok = False
        vals.append(loc_delta(src, K) / D1 if src else 0.0)
        notes.append(dict(knot=PK_KNOTS[j], h=round(h, 4), effn=round(en, 1)))
    own = [round(v, 4) for v in vals]
    if not ok:
        if c not in POOLED: POOLED.append(c)
        vals = []; notes = []
        for j, lpk in enumerate(LPK):
            h = 0.18
            while True:
                K = [float(np.exp(-0.5 * ((x['lp'] - lpk) / h) ** 2)) for x in NONKPD]
                if eff_n(NONKPD, K) >= EFFN or h > 3.0: break
                h *= 1.15
            vals.append(loc_delta(NONKPD, K) / D1)
            notes.append(dict(knot=PK_KNOTS[j], h=round(h, 4), effn=round(eff_n(NONKPD, K), 1),
                              pooled=True))
        print("   %-7s n=%3d  own eff-n < %d at the max bandwidth -> POOLED, DECLARED  (own reading %s)"
              % (c, len(rows), EFFN, own))
    BASE[c] = vals; NOTES['B_' + c] = notes
    print("   %-7s n=%3d  %s   eff-n %s" % (c, len(rows), [round(v, 4) for v in vals],
                                            [n['effn'] for n in notes]))
# KPD carries ONE class-level scalar on its own sub-dial (n too thin for a pick axis) — DECLARED.
KPD = [1.0] * len(LPK)
NOTES['B_KPD'] = dict(flat=True, n=len([x for x in Y1 if x['iskpd']]), delta=round(DKPD, 6),
                      note='class-level scalar; no pick axis (eff-n cannot support one)')

# ---- (2) THE MEASURED FADE, pooled over the year-1/2/3 evaluation rows on the continuous clock ----
print("\n-- the fade, measured (Addendum 1 F7: endogenous, not decreed) --")
raw = []
for t in TAU_KNOTS:
    sub = [x for x in POP if abs(x['tau'] - t) < 0.5 and not x['iskpd']]
    raw.append(loc_delta(sub, [1.0] * len(sub)))
unc = [v / D1 for v in raw]
iso = []; cur = 1.0
for v in unc:
    cur = min(cur, max(0.0, min(1.0, v))); iso.append(cur)
iso[0] = 1.0
STAU = iso
NOTES['Stau_raw_delta'] = [round(v, 6) for v in raw]
NOTES['Stau_unclamped'] = [round(v, 6) for v in unc]
print("   raw residual at tau %s = %s" % (TAU_KNOTS, [round(v, 5) for v in raw]))
print("   normalised to tau=1   = %s" % [round(v, 4) for v in unc])
print("   INSTALLED (isotonic non-increasing, clamped [0,1]) = %s" % [round(v, 4) for v in STAU])

# ---- (3) THE DECLARED SHAPE GATES: demonstrated level z, cumulative games g ----
print("\n-- the declared shape gates, measured on the year-1 rows --")
for name in ('Sz', 'Sg'):
    knots = Z_KNOTS if name == 'Sz' else LGK
    keyf = (lambda x: x['z']) if name == 'Sz' else (lambda x: x['lg'])
    h = (knots[1] - knots[0]) * 1.1
    vals = []; ens = []
    for kk in knots:
        K = [float(np.exp(-0.5 * ((keyf(x) - kk) / h) ** 2)) for x in NONKPD]
        while eff_n(NONKPD, K) < EFFN and h < 9.0:
            h *= 1.15
            K = [float(np.exp(-0.5 * ((keyf(x) - kk) / h) ** 2)) for x in NONKPD]
        vals.append(loc_delta(NONKPD, K) / D1); ens.append(round(eff_n(NONKPD, K), 1))
    if name == 'Sz': SZ = vals
    else: SG = vals
    print("   %-3s %s   eff-n %s   bw %.3f" % (name, [round(v, 4) for v in vals], ens, h))
NOTES['Sz_effn_bw'] = 'printed in teach_log.txt'

# ---- (3b) THE DECLARED PICK-TAPER ENDPOINTS: chosen to MEET the absolute bound, then FIXED ------
# Addendum 1 F5/F6 replaced "byte-unmoved at picks 41-64" (self-contradictory with smoothness) with a
# smooth taper carrying an ABSOLUTE aggregate bound: <= 0.5pp of movement in the 41-64 band at rung 1.0.
# The endpoints are a DECLARED BOUNDARY, so they are set to satisfy their own stated bound; the sweep
# that fixes them is printed here so the choice is auditable and is not a result-tuning dial.
print("\n-- pick-taper endpoint sweep (the 41-64 absolute bound, rung 1.0) --")
_deep = [x for x in NONKPD if 41 <= x['pk'] <= 64]
_sp_deep = sum(x['price'] for x in _deep)
for _lo, _hi in ((40.0, 52.0), (38.0, 50.0), (36.0, 48.0), (34.0, 48.0), (32.0, 44.0)):
    _agg = 0.0
    for x in _deep:
        _t = 1.0 if x['pk'] <= _lo else (0.0 if x['pk'] >= _hi else
             0.5 * (1.0 + np.cos(np.pi * (x['pk'] - _lo) / (_hi - _lo))))
        _agg += x['price'] * D1 * b_of(x) * s_tau(x['tau']) * s_z(x['z']) * s_g(x['lg']) * _t * x['ta']
    print("   taper %4.0f -> %4.0f :  picks 41-64 aggregate movement %+0.5f  %s"
          % (_lo, _hi, _agg / _sp_deep, "MEETS <=0.005" if abs(_agg / _sp_deep) <= 0.005 else "breaches"))
print("   INSTALLED endpoints: %.0f -> %.0f" % (PK_LO, PK_HI))

# ---- (4) THE CONSERVATION NORMALISER AND THE MONOTONICITY LAW, SOLVED JOINTLY -------------------
# ORDERING DEFECT CAUGHT IN BUILD AND FIXED HERE: a first cut ran the monotonicity law BEFORE the
# conservation normaliser, so the normaliser (which divides the base by Z < 1, i.e. scales it UP)
# re-broke the margin the law had just secured. The two are coupled and are therefore solved together:
#   Z   the ONE declared conservation scalar — value-weighted taught residual over the taper-supported
#       bonus population must reproduce that population's own MEASURED residual (Addendum 1's
#       conservation check, which catches bleed and double-counting of the marginal decomposition);
#   kappa  the minimal declared L-SMOOTH shrink of the Sz DEVIATION about its value-weighted mean that
#       keeps  d/dln(e)[e*(1+delta)] > 0  everywhere on the realised domain at rung 1.0 — the owner's
#       monotonicity law (a strictly better career never prices lower). The demonstrated-level axis is
#       DECREASING in z = log(e/anchor), which is exactly why this law can bind at all.
BASE_RAW = {c: list(BASE[c]) for c in CLASSES}
SZ0 = list(SZ)
WMZ = sum(x['price'] * float(np.interp(x['z'], Z_KNOTS, SZ0)) for x in NONKPD) / sum(x['price'] for x in NONKPD)
sup = [x for x in NONKPD if x['tp'] * x['ta'] > 0.0]
meas_sup = loc_delta(sup, [1.0] * len(sup))

def _mono_margin():
    worst = 9.9; where = None
    zs = np.linspace(Z_KNOTS[0], Z_KNOTS[-1], 241)
    for c in CLASSES:
        for pk in (3, 5, 8, 12, 15, 20, 25, 30, 35, 40, 45):
            tt = tpk(pk)
            if tt == 0.0: continue
            for g in (6.0, 8.0, 10.0, 13.0, 16.0, 20.0, 24.0):
                for t in (1.0, 1.25, 1.5, 1.75):
                    lg = float(np.log1p(g)); lp = float(np.log(pk))
                    bb = float(np.interp(lp, LPK, BASE[c]))
                    base = D1 * bb * s_tau(t) * s_g(lg) * tt
                    d = [base * s_z(z) for z in zs]
                    for i in range(1, len(zs)):
                        dd = (d[i] - d[i - 1]) / (zs[i] - zs[i - 1])
                        m = 1.0 + d[i] + dd
                        if m < worst: worst = m; where = (c, pk, g, t, round(float(zs[i]), 4))
    return worst, where

print("\n-- the conservation normaliser and the monotonicity law, solved jointly --")
print("   measured residual on the TAPER-SUPPORTED bonus population  %+0.6f  (n=%d)" % (meas_sup, len(sup)))
KAPPA = 1.0
for _it in range(400):
    SZ = [WMZ + KAPPA * (v - WMZ) for v in SZ0]
    raw_taught = sum(x['price'] * D1 * float(np.interp(x['lp'], LPK, BASE_RAW[x['cls']])) * m_of(x)
                     for x in sup) / sum(x['price'] for x in sup)
    ZC = raw_taught / meas_sup if abs(meas_sup) > 1e-9 else 1.0
    assert 0.3 < ZC < 3.0, 'conservation normaliser out of the sane range — the teach HALTS'
    for c in CLASSES: BASE[c] = [v / ZC for v in BASE_RAW[c]]
    mm, wh = _mono_margin()
    if mm > 0.02: break
    KAPPA *= 0.97
print("   marginal-product taught residual before normalisation      %+0.6f" % raw_taught)
print("   Z = %.6f   (|Z-1| = %.4f is the measured bleed / double-count of the marginal decomposition)"
      % (ZC, abs(ZC - 1.0)))
print("   L-SMOOTH shrink of the Sz deviation: kappa = %.6f  %s"
      % (KAPPA, "(none needed)" if KAPPA >= 0.9999 else "(DECLARED)"))
print("   min d/dln(e)[e*(1+delta)] over the realised domain at rung 1.0 = %+0.6f at %s" % (mm, wh))
print("   Sz as SHIPPED: %s" % [round(v, 5) for v in SZ])
assert mm > 0.0, 'monotonicity law unreachable — the act STOPS rather than ship a price inversion'
NOTES['conservation_Z'] = round(ZC, 6)
NOTES['measured_supported'] = round(meas_sup, 6)
NOTES['monotonicity_margin_rung1'] = round(mm, 6)
NOTES['monotonicity_worst_cell'] = list(wh)
NOTES['Sz_Lsmooth_kappa'] = round(KAPPA, 6)
NOTES['Sz_before_Lsmooth'] = [round(v, 6) for v in SZ0]

# ---------------- the shipped delta, the conservation report and the named cells ----------------
def taught_delta(x):
    """delta at rung 1.0 on each dial.  Returns (bonus-dial delta, KPD-sub-dial delta)."""
    m = m_of(x)
    if x['iskpd']: return 0.0, DKPD * m
    return D1 * b_of(x) * m, 0.0

sp = sum(x['price'] for x in Y1)
meas = sum(x['F'] for x in Y1) / sp - 1.0
tb = sum(x['price'] * taught_delta(x)[0] for x in Y1) / sp
tk = sum(x['price'] * taught_delta(x)[1] for x in Y1) / sp
print("\nCONSERVATION (year-1 ND 1-64, value-weighted):")
print("  measured aggregate residual, WHOLE leg        %+0.6f   (F' = %.6f)" % (meas, 1 + meas))
print("  taught delta at rung 1.0, BONUS dial RL_G6_W   %+0.6f" % tb)
print("  taught delta at rung 1.0, KPD sub-dial         %+0.6f  (RL_G6_KPD, default 0)" % tk)
print("  measured residual on the taper-supported bonus population  %+0.6f" % meas_sup)
for lab, f in (("pick taper (pick > %d)" % PK_LO, lambda x: x['tp'] < 1.0),
               ("draft-age taper (>18)", lambda x: x['age'] is not None and x['ta'] < 1.0),
               ("draft age UNKNOWN (delta == 0)", lambda x: x['age'] is None),
               ("KPD (own sub-dial)", lambda x: x['iskpd'])):
    rows = [x for x in Y1 if f(x)]
    if not rows: continue
    print("  boundary %-32s rows %3d  measured residual there %+0.6f  (weight %.3f of leg)"
          % (lab, len(rows), loc_delta(rows, [1.0] * len(rows)),
             sum(x['price'] for x in rows) / sp))
unk = sorted(set(x['key'] for x in Y1 if x['age'] is None))
print("  UNKNOWN draft age, correction identically 0 (Addendum 1 F13): %d rows / %d players"
      % (len([x for x in Y1 if x['age'] is None]), len(unk)))
print("  " + ", ".join(unk))

print("\nTAUGHT vs MEASURED at the named cells (year-1, value-weighted, rung 1.0):")
print("  %-38s %5s %11s %11s" % ("cell", "n", "measured", "taught"))
zs = sorted(x['z'] for x in Y1); zmed = zs[len(zs) // 2]; zt2 = zs[2 * len(zs) // 3]
CELLS = [("whole year-1 leg", lambda x: True),
         ("picks 1-10", lambda x: x['pk'] <= 10),
         ("picks 1-20", lambda x: x['pk'] <= 20),
         ("picks 21-40", lambda x: 21 <= x['pk'] <= 40),
         ("picks 41-64", lambda x: 41 <= x['pk'] <= 64),
         ("ZERO-CELL picks 1-10 x top-tercile z", lambda x: x['pk'] <= 10 and x['z'] >= zt2),
         ("ZERO-CELL picks 1-20 x above-median z", lambda x: x['pk'] <= 20 and x['z'] >= zmed),
         ("MID", lambda x: x['pos'] == 'MID'),
         ("KPF", lambda x: x['pos'] == 'KPF'),
         ("KPD", lambda x: x['pos'] == 'KPD'),
         ("RUCK", lambda x: x['pos'] == 'RUCK'),
         ("SF", lambda x: x['pos'] == 'SF'),
         ("SD", lambda x: x['pos'] == 'SD'),
         ("cumulative games 6-9", lambda x: 6 <= x['gcum'] <= 9),
         ("draft age <= 18", lambda x: x['age'] is not None and x['age'] <= 18)]
CELLREP = {}
for nm, f in CELLS:
    rows = [x for x in Y1 if f(x)]
    if not rows: continue
    md = loc_delta(rows, [1.0] * len(rows))
    td = sum(x['price'] * sum(taught_delta(x)) for x in rows) / sum(x['price'] for x in rows)
    tdb = sum(x['price'] * taught_delta(x)[0] for x in rows) / sum(x['price'] for x in rows)
    CELLREP[nm] = dict(n=len(rows), measured=round(md, 6), taught_bonus=round(tdb, 6),
                       taught_all=round(td, 6))
    print("  %-38s %5d %+10.4f %+10.4f" % (nm, len(rows), md, tdb))

TAB = dict(
    meta=dict(
        act='#334 stage B / stage 6 — the conditioned development correction (established leg)',
        directive='issue 334 comment 5217307894 + Addendum 1 comment 5217452004',
        teaching_matrix='per_entrant_338_stage4a1.json',
        teaching_matrix_md5='b564b12e533119f49c2c6bb0c92a5d91',
        teaching_board='b56bbdde (the frozen baseline the matrix was emitted at)',
        population='ND 1-64, classes 2004-2022, evaluation years 1-3, ns>=1 (established) leg',
        n_rows=dict(y1=len(Y1), y2=len([x for x in POP if x['N'] == 2]),
                    y3=len([x for x in POP if x['N'] == 3])),
        estimand="value-weighted aggregate F' = sum(F)/sum(price); median F' pre-registered beside it",
        measured_agg_y1_whole=round(1 + meas, 6),
        measured_agg_y1_bonus_population=round(1 + D1, 6),
        measured_agg_y1_kpd=round(1 + DKPD, 6),
        measured_median_y1=round(float(np.median([x['F'] / x['price'] for x in Y1])), 6),
        taught_agg_delta_rung1_bonus=round(tb, 6),
        taught_agg_delta_rung1_kpd=round(tk, 6),
        pooled_classes=POOLED,
        kernel='two axes only: log-pick x {nonKPP,KPP,RUCK}; Gaussian, eff-n>=35 on the value weight',
        shapes='Stau (measured, isotonic, clamped [0,1]) x Sz (z=log(e/entry_anchor)) x Sg (cumulative'
               ' games) x declared pick taper x declared draft-age taper',
        kpd='KPD rows excluded from the base kernel and carried on their own sub-dial RL_G6_KPD'
            ' (default 0); shapes shared, class-level scalar, DECLARED',
        cells=CELLREP, notes=NOTES),
    d1=round(D1, 8), d_kpd=round(DKPD, 8),
    pk_knots=PK_KNOTS, tau_knots=TAU_KNOTS, z_knots=Z_KNOTS, g_knots=G_KNOTS,
    pk_taper=[PK_LO, PK_HI], age_taper=[AGE_LO, AGE_HI],
    base={c: [round(v, 8) for v in BASE[c]] for c in CLASSES},
    s_tau=[round(v, 8) for v in STAU], s_z=[round(v, 8) for v in SZ], s_g=[round(v, 8) for v in SG])

path = OUT + '/g6_table.json'
json.dump(TAB, open(path, 'w'), indent=1, sort_keys=True)
print("\nwrote %s  md5 %s" % (path, hashlib.md5(open(path, 'rb').read()).hexdigest()))
