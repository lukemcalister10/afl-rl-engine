#!/usr/bin/env python3
"""FORM-CONDITIONED DECLINER SHED — measurement + 2-D surface fit (2026-07-06).

Reads the LIVE engine (workspace _merged_recover.py, exec'd the run_panel way), (1) characterises
the current aging/shed cohort with $ incl. Gawn/Cameron/Bontempelli + genuine-decliner contrast
anchors, (2) measures realised forward decline r = Lfwd/Lc as f(age, lcr=Lc-REPL) over the
established shed population, (3) fits an up-only 2-D credit bump over the current age-only _agemult
(adaptive Gaussian bw grown to eff-n>=35, thin-cell shrinkage toward the 1-D prior, isotonic
non-decreasing in lcr / non-increasing in age), and emits _FBUMP_Z + _FBUMP_META as paste-ready
literals. READ-ONLY on the store; writes only under session_2026-07-06/out.
"""
import io, contextlib, os, json, sys
import numpy as np
from sklearn.isotonic import IsotonicRegression

OUT = os.environ.get('SS_OUT', '/home/user/afl-rl-engine/session_2026-07-06/out')
os.makedirs(OUT, exist_ok=True)

# ---- load the live engine exactly like run_panel.sh (exec up to the AFTER banner) ----
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA = g['MA']; ev = g['ev']; cp = g['cp']; PR = g['PR']
_lvlcurr = g['_lvlcurr']; _nqual = g['_nqual']; _agemult = g['_agemult']
DOWN_TOL = g['DOWN_TOL']; PROVEN_N = g['PROVEN_N']
_AGEMULT_X = g['_AGEMULT_X']; _AGEMULT_Y = g['_AGEMULT_Y']
REPL = MA.REPL
lvl_eff_orig = cp._lvl_eff_orig            # cp._lvl_eff_orig = original _lvl_eff (the "established" level Lo)

def find(nm):
    c = [p for p in MA.data if nm.lower() in p['player'].lower() and MA.GRP.get(p.get('pos'))]
    return c[0] if c else None

def branch_of(p, Y=2026):
    """Which _coreM1 branch a proven player lands in at Y (matches _merged_recover.py :177-182)."""
    n = _nqual(p, Y)
    if n < PROVEN_N:
        return ('thin' if n > 0 else 'cameo'), None, None, None
    Lo = lvl_eff_orig(p, Y); Lc = _lvlcurr(p, Y); drop = Lo - Lc
    if Lc >= Lo:
        return 'UP-hold', Lo, Lc, drop
    if drop <= DOWN_TOL:
        return 'hold(<=TOL)', Lo, Lc, drop
    return 'SHED', Lo, Lc, drop

def lcr_of(p, Y=2026):
    return _lvlcurr(p, Y) - REPL.get(MA.gfut(p), 0.0)

# =========================== (1) CHARACTERISE ===========================
print("="*96)
print("(1) CURRENT AGING/SHED COHORT — age-keyed _agemult in play only on the SHED branch")
print("="*96)
hdr = "%-22s %-8s %4s %4s %7s %7s %6s %7s %7s %8s"
print(hdr % ('player','pos','age','nq','Lo','Lc','drop','agemult','lcr','ev'))
NAMED = ['Marcus Bontempelli','Max Gawn','Jeremy Cameron','Kieren Briggs']
def row(p, Y=2026):
    if p is None: return
    br, Lo, Lc, drop = branch_of(p, Y)
    a = cp._age_asof(p, Y)
    am = _agemult(a) if br == 'SHED' else float('nan')
    lo = '%7.1f' % Lo if Lo is not None else '   --  '
    lc = '%7.1f' % Lc if Lc is not None else '   --  '
    dr = '%6.1f' % drop if drop is not None else '  --  '
    am_s = '%7.3f' % am if am == am else '   --  '
    print(hdr % (p['player'][:22], MA.gfut(p), '%.0f'%a, _nqual(p,Y), lo, lc, dr, am_s,
                 '%7.1f'%lcr_of(p,Y), '%8d'%ev(p,Y)) + ('   <<'+br if p['player'] in NAMED else '   '+br))
for nm in NAMED:
    row(find(nm))

# full SHED cohort (established, drop>DOWN_TOL) — sort by lcr so still-elite dippers sit on top
shed = []
for p in MA.data:
    if not MA.GRP.get(p.get('pos')): continue
    br, Lo, Lc, drop = branch_of(p, 2026)
    if br == 'SHED':
        shed.append((lcr_of(p,2026), p, Lo, Lc, drop))
shed.sort(key=lambda t: -t[0])
print("\n--- FULL SHED COHORT (%d players), sorted by lcr=Lc-REPL (still-elite on top) ---" % len(shed))
for lcr, p, Lo, Lc, drop in shed:
    a = cp._age_asof(p, 2026)
    print(hdr % (p['player'][:22], MA.gfut(p), '%.0f'%a, _nqual(p,2026), '%7.1f'%Lo, '%7.1f'%Lc,
                 '%6.1f'%drop, '%7.3f'%_agemult(a), '%7.1f'%lcr, '%8d'%ev(p,2026)))

# =========================== (2) MEASURE ===========================
# realised forward level Lfwd over complete seasons Y+1..min(Y+H,2025), washout-inclusive (missing/<6g season -> 0);
# r = Lfwd / Lc.  Population = the SHED gate (established & Lo-Lc>DOWN_TOL) so the surface is a drop-in for _agemult.
H = 3; LASTC = 2025
def norm_avg_year(p, yr):
    for x in p['scoring']:
        if x['year'] == yr:
            return x['avg'] if x['games'] >= 6 else 0.0   # washout / cameo -> 0
    return 0.0                                            # did not play -> washout 0
def realised_fwd(p, Y):
    yrs = list(range(Y+1, min(Y+H, LASTC)+1))
    if not yrs: return None
    return float(np.mean([norm_avg_year(p, yr) for yr in yrs]))

obs = []   # (age, lcr, r, weight, player, Y)
for p in MA.data:
    if not MA.GRP.get(p.get('pos')): continue
    d0 = cp.debutyr(p)
    for Y in range(d0, LASTC):                 # need >=1 complete forward season
        if _nqual(p, Y) < PROVEN_N: continue
        Lo = lvl_eff_orig(p, Y); Lc = _lvlcurr(p, Y)
        if Lc <= 0 or (Lo - Lc) <= DOWN_TOL: continue   # SHED gate
        Lfwd = realised_fwd(p, Y)
        if Lfwd is None: continue
        r = min(2.0, Lfwd / max(1.0, Lc))               # winsor 2.0 (house convention)
        age = cp._age_asof(p, Y); lcr = Lc - REPL.get(MA.gfut(p), 0.0)
        obs.append((float(age), float(lcr), float(r), p['player'], Y))
obs = [o for o in obs if 20 <= o[0] <= 40]
print("\n" + "="*96)
print("(2) MEASUREMENT — %d established shed-population player-seasons (debut..%d, H=%d washout-incl)" % (len(obs), LASTC-1, H))
print("="*96)
A = np.array([o[0] for o in obs]); L = np.array([o[1] for o in obs]); R = np.array([o[2] for o in obs])
# sanity: mean r by age bin, and by lcr bin
def binstat(x, y, edges, lbl):
    print("  mean r by %s:" % lbl)
    for i in range(len(edges)-1):
        m = (x>=edges[i]) & (x<edges[i+1])
        if m.sum(): print("    [%5.0f,%5.0f)  n=%4d  r=%.3f  _agemult(mid)=%.3f" %
                           (edges[i], edges[i+1], m.sum(), y[m].mean(), _agemult((edges[i]+edges[i+1])/2) if lbl=='age' else float('nan')))
binstat(A, R, [20,28,30,32,34,40], 'age')
binstat(L, R, [-40,-10,0,10,20,60], 'lcr')

# =========================== (3) FIT — up-only 2-D credit bump over _agemult ===========================
_AGE_X = [22,25,28,30,32,34,37]
_LCR_X = [-15,-5,5,15,30]
# residual target d = max(0, r - agemult(age)); NW-2D adaptive bw grown to eff-n>=35; shrink to 0 (=> pure _agemult) where thin.
d = np.maximum(0.0, R - np.array([_agemult(a) for a in A]))
def eff_n(w):
    s = w.sum(); return (s*s)/max(1e-12,(w*w).sum())
GRID = [(a,l) for a in _AGE_X for l in _LCR_X]
raw = {}; effn = {}
H_AGE0, H_LCR0 = 1.6, 6.0; H_AGE_CAP, H_LCR_CAP = 7.0, 45.0
for (a,l) in GRID:
    ha, hl = H_AGE0, H_LCR0
    while True:
        w = np.exp(-0.5*(((A-a)/ha)**2 + ((L-l)/hl)**2))
        if eff_n(w) >= 35 or (ha >= H_AGE_CAP and hl >= H_LCR_CAP): break
        ha = min(H_AGE_CAP, ha*1.15); hl = min(H_LCR_CAP, hl*1.15)
    en = eff_n(w); effn[(a,l)] = en
    val = float((w*d).sum()/max(1e-9,w.sum())) if w.sum()>0 else 0.0
    shrink = min(1.0, en/35.0)                              # thin-cell shrinkage toward the 1-D prior (bump->0)
    raw[(a,l)] = max(0.0, val*shrink)
# monotone projection: non-decreasing in lcr at each age (PAV increasing); then non-increasing in age at each lcr.
Z = np.array([[raw[(a,l)] for l in _LCR_X] for a in _AGE_X])   # rows=age, cols=lcr
for i,a in enumerate(_AGE_X):
    Z[i,:] = IsotonicRegression(increasing=True).fit_transform(range(len(_LCR_X)), Z[i,:])
for j,l in enumerate(_LCR_X):
    Z[:,j] = IsotonicRegression(increasing=False).fit_transform(range(len(_AGE_X)), Z[:,j])  # bump not larger for older at same lcr
Z = np.maximum(0.0, Z)

print("\n" + "="*96)
print("(3) FITTED up-only credit bump _FBUMP_Z  (rows=age %s, cols=lcr %s)" % (_AGE_X, _LCR_X))
print("="*96)
print("     lcr:  " + "".join("%8d"%l for l in _LCR_X))
for i,a in enumerate(_AGE_X):
    print("  age %2d:  " % a + "".join("%8.3f"%Z[i,j] for j in range(len(_LCR_X))) +
          "   [eff-n " + ",".join("%.0f"%effn[(a,l)] for l in _LCR_X) + "]")

# resulting agemult2 at the knots (base + bump, clipped) for eyeballing
print("\n  resulting _agemult2(age,lcr) = clip(_agemult(age)+bump, 0.53, 0.98):")
print("     lcr:  " + "".join("%8d"%l for l in _LCR_X))
for i,a in enumerate(_AGE_X):
    print("  age %2d:  " % a + "".join("%8.3f"%min(0.98,max(0.53,_agemult(a)+Z[i,j])) for j in range(len(_LCR_X))) +
          "   [_agemult=%.3f]"%_agemult(a))

meta = {'H':H,'LASTC':LASTC,'n_obs':len(obs),'AGE_X':_AGE_X,'LCR_X':_LCR_X,
        'effn':{f"{a}|{l}":round(effn[(a,l)],1) for (a,l) in GRID},
        'thin_cells':[f"{a}|{l}" for (a,l) in GRID if effn[(a,l)]<35]}
json.dump({'Z':[[round(float(Z[i,j]),4) for j in range(len(_LCR_X))] for i in range(len(_AGE_X))],
           'AGE_X':_AGE_X,'LCR_X':_LCR_X,'meta':meta}, open(os.path.join(OUT,'fbump_fit.json'),'w'), indent=1)
print("\n  _FBUMP_Z (paste-ready):")
print("  _FBUMP_Z=" + repr([[round(float(Z[i,j]),4) for j in range(len(_LCR_X))] for i in range(len(_AGE_X))]))
print("  thin cells (eff-n<35, shrunk toward 1-D prior):", meta['thin_cells'])
print("\n  wrote", os.path.join(OUT,'fbump_fit.json'))
