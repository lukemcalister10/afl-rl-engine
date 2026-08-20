#!/usr/bin/env python3
"""ORDER 31 — THE ONE LAW's FITTED OBJECTS.  READ-ONLY.  No engine, no board, no store touched.

    price(p,Y) = rho(g) * Phat  +  pi(g, c_u, s) * V0

    pi(g, c_u, s) = D(c_u) * (1 - rho(g))  +  Phi(g,s) * beta_mono(g) * rho(g)

THE TWO ENDPOINTS ARE THE TWO RULED LAWS, REPRODUCED EXACTLY, NOT APPROXIMATED:

    g = 0      rho(0)=0  =>  price = D(c) * V0            THE WIRED STEP-2 SITTER LAW, exactly.
    rho -> 1   (deep)    =>  price = Phat + beta(g) * V0  THE 30B-R ADDITIVE READING (T1), exactly.

so pi(0,c) = D(c) EXACTLY (the brief's hard constraint) and "pi decays in g per the measured beta" is
literally true: pi's g-dependence IS the measured beta curve, handed over to by rho.  ONE formula, all g,
all pathways.  No lane, no bridge, no ownership-by-threshold.

THREE FITTED / DERIVED OBJECTS:

  beta_mono(g)  the measured pooled beta curve under the brief's EXPLICIT "pi decays in g" constraint,
                i.e. its monotone non-increasing projection (running minimum), log-linear in log(g)
                between band midpoints, flat outside -- the SAME interpolation the committed beta30bn
                uses.  The projection removes the measured 2.5->10.5 RISE, which 30B-C section 4.3 showed
                is the mechanism that paid 57 of 352 stall paths MORE for stalling.

  rho(g) = 1 - exp(-(g/TAU_RHO)^B_RHO),  rho(0)=0 exactly, monotone, -> 1.
                FITTED so a thin cohort's aggregate price matches the R1 re-derived cumulative backbone:
                    B(g) == rho(g)*1.0 + [ D(2)*(1-rho(g)) + beta_mono(g)*rho(g) ]
                (the backbone is RAW(1)-normalised, so the production leg reads 1.0 there).  Inverting
                that at each knot gives an EXACT rho target; only the two-parameter form is fitted.
                THE BACKBONE CONSTRAINS THE TOTAL.  IT NEVER REPLACES PRODUCTION.

  Phi(g,s) = 1 - min(s,2)/2 * (1 - PhiStall(g)),  Phi(g,0)=1 exactly.
                THE 30B-C STALL CONDITIONING.  s = the count of PLAYED-BUT-NOT-DELIVERED seasons.
                PhiStall(g) = the measured ratio beta_stall(g)/beta_pooled(g) at the five band midpoints,
                zero-floored where the stall coefficient is statistically zero, made non-increasing, and
                interpolated by the same log-linear rule.  The ramp denominator 2 is 30B-C's OWN
                definition of a continued staller (no delivered season at Y+1 or Y+2), not a tuned knob.
"""
import json, math, os, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
EV   = os.path.dirname(HERE)
OM   = os.path.join(EV, 'one_machinery_2026-08-14')
md5  = lambda p: hashlib.md5(open(p, 'rb').read()).hexdigest()

P_READING = os.path.join(OM, 'resolution', 'READING.json')
P_BLEND   = os.path.join(OM, 'BLEND30B.json')
P_CIRC    = os.path.join(OM, 'circularity', 'CIRCULARITY.json')
reading, blend, circ = (json.load(open(p)) for p in (P_READING, P_BLEND, P_CIRC))

BETA_POOLED = [(float(g), float(b)) for g, b in reading['beta_curve']['points']]
BACKBONE    = {int(k): float(v) for k, v in blend['backbone'].items()}
D2          = float(blend['D2'])
FADE_D      = {1: 1.0, 2: 0.5501935857356868, 3: 0.26278629823610156, 4: 0.3460004697526451}
BAND_N      = {2.5: 382, 10.5: 591, 25.5: 834, 53.0: 887, 85.5: 1339}
assert abs(FADE_D[2] - D2) < 1e-15
assert abs(BACKBONE[0] - D2) < 1e-12, 'backbone B(0) is not D(2): the RAW(1) normalisation moved'

# ---- the 30B-C stall-cohort coefficients, READ OUT OF THE ARTIFACT (not transcribed) --------------
def dig(o, path):
    for k in path:
        o = o[k]
    return o
STALL_SRC = {}
for band in ('0-5', '6-15', '16-35', '36-70', '71+'):
    STALL_SRC[band] = float(dig(circ, ['beta_stall_by_band', band, 'beta_v0']))
BANDS_ORDER = ['0-5', '6-15', '16-35', '36-70', '71+']
MIDPOINTS   = [2.5, 10.5, 25.5, 53.0, 85.5]
BETA_STALL_RAW = [(MIDPOINTS[i], STALL_SRC[BANDS_ORDER[i]]) for i in range(5)]
# 30B-C section 4 / limitation 5: past 36 games the stall coefficient is t=-0.29 / -0.90, CI spans zero.
# It is A ZERO, NOT A NEGATIVE NUMBER.  Floored, exactly as 30B-C's own zero-floored variant does.
BETA_STALL = [(g, max(0.0, b)) for g, b in BETA_STALL_RAW]

# ---- monotone non-increasing projection (running minimum) ----------------------------------------
def mono_dec(points):
    out, cur = [], None
    for g, y in points:
        cur = y if cur is None else min(cur, y)
        out.append((g, cur))
    return out

BETA_MONO_PTS  = mono_dec(BETA_POOLED)
STALL_MONO_PTS = mono_dec(BETA_STALL)

def loglin(pts, g):
    """Log-linear in log(g) between the band midpoints, FLAT outside -- the committed beta30bn rule."""
    g = max(1e-9, float(g))
    if g <= pts[0][0]:  return pts[0][1]
    if g >= pts[-1][0]: return pts[-1][1]
    for i in range(1, len(pts)):
        g0, y0 = pts[i - 1]; g1, y1 = pts[i]
        if g0 <= g <= g1:
            t = (math.log(g) - math.log(g0)) / (math.log(g1) - math.log(g0))
            if y0 <= 0.0 or y1 <= 0.0:           # linear where a knot is zero (log undefined)
                return y0 + t * (y1 - y0)
            return math.exp(math.log(y0) + t * (math.log(y1) - math.log(y0)))
    return pts[-1][1]

beta_mono  = lambda g: loglin(BETA_MONO_PTS, g)
beta_stall = lambda g: loglin(STALL_MONO_PTS, g)

def phi_stall(g):
    p = beta_mono(g)
    return 1.0 if p <= 0.0 else min(1.0, max(0.0, beta_stall(g) / p))
PHI_STALL_PTS = mono_dec([(m, phi_stall(m)) for m in MIDPOINTS])
phi_stall_c   = lambda g: loglin(PHI_STALL_PTS, g)      # the non-increasing, interpolated conditioner
PHI_RAMP = 2.0
def phi(g, s): return 1.0 if s <= 0 else 1.0 - (min(float(s), PHI_RAMP) / PHI_RAMP) * (1.0 - phi_stall_c(g))

# ---- rho: EXACT targets from the backbone, then a two-parameter form ------------------------------
RHO_TARGETS = []
for g in sorted(BACKBONE):
    den = 1.0 + beta_mono(g) - D2
    RHO_TARGETS.append((float(g), (BACKBONE[g] - D2) / den))

def nelder_mead(f, x0, step=0.3, tol=1e-15, maxit=40000):
    n = len(x0); pts = [list(x0)]
    for i in range(n):
        p = list(x0); p[i] += step * (abs(p[i]) or 1.0); pts.append(p)
    vals = [f(p) for p in pts]
    for _ in range(maxit):
        o = sorted(range(n + 1), key=lambda i: vals[i]); pts = [pts[i] for i in o]; vals = [vals[i] for i in o]
        if abs(vals[-1] - vals[0]) <= tol * (abs(vals[0]) + abs(vals[-1]) + 1e-300): break
        cen = [sum(p[i] for p in pts[:-1]) / n for i in range(n)]
        ref = [cen[i] + (cen[i] - pts[-1][i]) for i in range(n)]; fr = f(ref)
        if fr < vals[0]:
            ex = [cen[i] + 2.0 * (cen[i] - pts[-1][i]) for i in range(n)]; fe = f(ex)
            pts[-1], vals[-1] = (ex, fe) if fe < fr else (ref, fr)
        elif fr < vals[-2]: pts[-1], vals[-1] = ref, fr
        else:
            co = [cen[i] + 0.5 * (pts[-1][i] - cen[i]) for i in range(n)]; fc = f(co)
            if fc < vals[-1]: pts[-1], vals[-1] = co, fc
            else:
                for i in range(1, n + 1):
                    pts[i] = [pts[0][j] + 0.5 * (pts[i][j] - pts[0][j]) for j in range(n)]; vals[i] = f(pts[i])
    i = min(range(n + 1), key=lambda i: vals[i]); return pts[i], vals[i]

def obj_rho(z):
    tau, b = math.exp(z[0]), math.exp(z[1]); s = 0.0
    for g, y in RHO_TARGETS:
        yh = 0.0 if g <= 0 else 1.0 - math.exp(-((g / tau) ** b))
        s += (yh - y) ** 2
    return s
z, SSE_RHO = nelder_mead(obj_rho, [math.log(20.0), math.log(0.9)])
TAU_RHO, B_RHO = math.exp(z[0]), math.exp(z[1])
rho = lambda g: 0.0 if float(g) <= 0.0 else 1.0 - math.exp(-((float(g) / TAU_RHO) ** B_RHO))

def pi(g, D, s=0):
    # Phi conditions the MEASURED COEFFICIENT ONLY.  beta_stall/beta_pooled is a ratio of ADDITIVE
    # COEFFICIENTS estimated on played players; the D(c_u) channel is the sitter fade, measured on
    # GAMELESS listed players, and no stall measurement was ever taken on it.  Applying Phi to both
    # would push a conditioning through a population it was not estimated on -- and it makes
    # pi(0,c,s) == D(c) hold for EVERY s structurally, not merely on an unreachable-state argument.
    r = rho(g)
    return D * (1.0 - r) + phi(g, s) * beta_mono(g) * r

RHO_ROWS = []
for g, y in RHO_TARGETS:
    B_fit = rho(g) * 1.0 + (D2 * (1.0 - rho(g)) + beta_mono(g) * rho(g))
    RHO_ROWS.append({'g': g, 'B_target': BACKBONE[int(g)], 'beta_mono': beta_mono(g),
                     'rho_target_exact': y, 'rho_fit': rho(g), 'B_fit': B_fit,
                     'resid_D_units': B_fit - BACKBONE[int(g)]})
RMS_RHO = math.sqrt(sum(r['resid_D_units'] ** 2 for r in RHO_ROWS) / len(RHO_ROWS))

# ---- checks that can fail --------------------------------------------------------------------------
GRID = [x * 0.25 for x in range(0, 1601)]
CHK = {}
CHK['rho(0)==0 exactly']        = rho(0.0) == 0.0
CHK['pi(0,c)==D(c) exactly']    = all(pi(0.0, FADE_D[k], 0) == FADE_D[k] for k in FADE_D)
# s>0 at g==0 is STRUCTURALLY UNREACHABLE: s counts PLAYED-but-not-delivered seasons, so s>=1 implies
# at least one season with games>0, i.e. g>=1.  It is asserted ON THE BOARD POPULATION in the engine
# (a build-failing assert), not papered over with a maths trick here.
CHK['pi(0,c,s)==D(c) any s']   = all(pi(0.0, FADE_D[k], s) == FADE_D[k] for k in FADE_D for s in (0,1,2,5,9))
CHK['rho strictly increasing']  = all(rho(GRID[i]) < rho(GRID[i + 1]) for i in range(len(GRID) - 1))
CHK['rho -> 1']                 = rho(400.0) > 0.999
CHK['rho in [0,1)']             = all(0.0 <= rho(g) < 1.0 for g in GRID)
CHK['beta_mono non-increasing'] = all(beta_mono(GRID[i]) >= beta_mono(GRID[i + 1]) - 1e-15 for i in range(len(GRID) - 1))
CHK['PhiStall non-increasing']  = all(phi_stall_c(GRID[i]) >= phi_stall_c(GRID[i + 1]) - 1e-15 for i in range(len(GRID) - 1))
CHK['Phi(g,0)==1 exactly']      = all(phi(g, 0) == 1.0 for g in GRID)
CHK['Phi in [0,1]']             = all(0.0 <= phi(g, s) <= 1.0 for g in GRID for s in (1, 2, 6))
# pi's ONE non-monotonicity, MEASURED not asserted: where D(c_u) < beta_mono (the depth-3 kink at 0.2628
# against beta 0.29683) pi rises before it falls.  Bounded and printed rather than smoothed.
_pk3 = max(pi(g, FADE_D[3]) for g in GRID); _r3 = _pk3 / FADE_D[3] - 1.0
CHK['pi depth-3 rise <= 10%']   = _r3 <= 0.10
CHK['backbone g=0 resid == 0']  = abs(RHO_ROWS[0]['resid_D_units']) < 1e-15
# pi decays in g for EVERY depth at or below the D=1 entry-year level, once evidence exists
CHK['pi non-increasing for D=1']= all(pi(GRID[i], 1.0) >= pi(GRID[i + 1], 1.0) - 1e-15 for i in range(len(GRID) - 1))
# deep limit: the law becomes EXACTLY the ruled additive reading
CHK['deep -> additive (1e-3)']  = abs(pi(300.0, 0.3460004697526451) - beta_mono(300.0)) < 1e-3

OUT = {
    'order': 'ORDER 31 -- THE ONE LAW',
    'law': 'price = rho(g)*Phat + [ D(c_u)*(1-rho(g)) + Phi(g,s)*beta_mono(g)*rho(g) ]*V0',
    'endpoints': {'g=0': 'price = D(c)*V0  -- the wired Step-2 sitter law, EXACT',
                  'deep': 'price = Phat + beta(g)*V0 -- the 30B-R additive reading (T1), EXACT'},
    'inputs': {'READING.json': {'md5': md5(P_READING), 'beta_points': BETA_POOLED},
               'BLEND30B.json': {'md5': md5(P_BLEND), 'backbone_R1': BACKBONE, 'D2': D2},
               'CIRCULARITY.json': {'md5': md5(P_CIRC), 'beta_stall_by_band_read_from_artifact': STALL_SRC},
               'band_n': BAND_N, 'fade_D': FADE_D},
    'beta_mono': {'points_measured': BETA_POOLED, 'points_monotone': BETA_MONO_PTS,
                  'projection': 'running minimum (monotone non-increasing projection)',
                  'why': "the brief's explicit constraint 'pi decays in g'; 30B-C section 4.3 measured the "
                         "2.5->10.5 rise paying 57 of 352 stall paths MORE for stalling",
                  'interpolation': 'log-linear in log(g) between midpoints, flat outside (== beta30bn)'},
    'rho': {'form': 'rho(g) = 1 - exp(-(g/TAU_RHO)^B_RHO)', 'TAU_RHO': TAU_RHO, 'B_RHO': B_RHO,
            'sse': SSE_RHO, 'rms_D_units': RMS_RHO, 'targets_exact': RHO_TARGETS, 'rows': RHO_ROWS,
            'calibration': 'B(g) == rho(g)*1.0 + [D(2)*(1-rho(g)) + beta_mono(g)*rho(g)] on the R1 backbone'},
    'phi': {'form': 'Phi(g,s) = 1 - min(s,2)/2 * (1 - PhiStall(g)); it multiplies the MEASURED COEFFICIENT beta_mono ONLY',
            'beta_stall_raw': BETA_STALL_RAW, 'beta_stall_floored': BETA_STALL,
            'beta_stall_monotone': STALL_MONO_PTS, 'PhiStall_knots': PHI_STALL_PTS,
            'ramp_denominator': PHI_RAMP,
            'ramp_source': "30B-C's own continued-staller definition: no delivered season at Y+1 or Y+2",
            's_definition': 'THE CURRENT STALL RUN: the number of CONSECUTIVE most-recent seasons up to and '
                            'including Y in which the player PLAYED (games>0) but did NOT deliver '
                            '(delivered == games>=10 AND avg >= the position bar).  A DELIVERED season '
                            'RESETS s to 0.  A GAMELESS season is SKIPPED (neither increments nor resets) '
                            'because unplayed time is D(c_u)\'s channel and counting it twice is the '
                            'double-discount the no-stacking constraint forbids.  This is the BACKWARD '
                            'transplant of 30B-C\'s FORWARD definition (no delivered season at Y+1 or '
                            'Y+2) and the substitution is the weakest joint in the conditioning -- '
                            'declared in PREREG_31 disclosure 4.'},
    'checks': CHK,
    'pi_depth3_peak_rise_pct': (max(pi(g, FADE_D[3]) for g in GRID) / FADE_D[3] - 1.0) * 100.0,
    'curve_table': [{'g': g, 'rho': rho(g), 'beta_mono': beta_mono(g), 'PhiStall': phi_stall_c(g),
                     'pi_D1_s0': pi(g, 1.0, 0), 'pi_D2_s0': pi(g, FADE_D[2], 0),
                     'pi_D4_s0': pi(g, FADE_D[4], 0), 'pi_D4_s2': pi(g, FADE_D[4], 2)}
                    for g in (0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 16, 20, 25, 36, 50, 71, 100, 150, 200, 300)],
}
json.dump(OUT, open(os.path.join(HERE, 'LAW31.json'), 'w'), indent=1, sort_keys=True)

print('=== ORDER 31 — THE ONE LAW ==================================================')
print('price = rho(g)*Phat + [ D(c_u)*(1-rho(g)) + Phi(g,s)*beta_mono(g)*rho(g) ]*V0')
print()
print('beta measured  :', ' '.join('%.4f' % b for _, b in BETA_POOLED))
print('beta MONOTONE  :', ' '.join('%.4f' % b for _, b in BETA_MONO_PTS), '  <- the brief\'s "pi decays in g"')
print('beta stall raw :', ' '.join('%+.5f' % b for _, b in BETA_STALL_RAW), '  (read from CIRCULARITY.json)')
print('beta stall used:', ' '.join('%.5f' % b for _, b in STALL_MONO_PTS), '  (zero-floored, monotone)')
print('PhiStall knots :', ' '.join('%.4f' % y for _, y in PHI_STALL_PTS))
print()
print('rho(g) = 1 - exp(-(g/%.10f)^%.10f)      SSE %.3e' % (TAU_RHO, B_RHO, SSE_RHO))
for r in RHO_ROWS:
    print('  backbone g=%2.0f  B %.6f   rho* %.6f  rho_fit %.6f   B_fit %.6f   resid %+.6f'
          % (r['g'], r['B_target'], r['rho_target_exact'], r['rho_fit'], r['B_fit'], r['resid_D_units']))
print('  RMS residual %.6f D units   (the Step-3 calibration bar was 0.05)' % RMS_RHO)
print()
print('   g    rho     beta_mono  PhiStall   pi(D=1)  pi(D=.550) pi(D=.346) pi(D=.346,s=2)')
for r in OUT['curve_table']:
    print(' %4g  %.5f   %.5f   %.5f   %.5f   %.5f   %.5f   %.5f'
          % (r['g'], r['rho'], r['beta_mono'], r['PhiStall'], r['pi_D1_s0'], r['pi_D2_s0'], r['pi_D4_s0'], r['pi_D4_s2']))
print()
for k, v in CHK.items():
    print('  %-30s %s' % (k, 'PASS' if v else '*** FAIL ***'))
if not all(CHK.values()):
    sys.exit('ORDER 31 FIT HALT: a declared check failed.')
print('\nLAW31.json written.')
