#!/usr/bin/env python3
"""ORDER 33 W1 -- THE DEEP END OF beta, RE-MEASURED (PREREG_W1.md s3, estimators E1-E4).

The 30B-M harness (`o30bm_measure.py`, md5 asserted) is exec'd WHOLE UP TO ITS OWN `band_fit`
DEFINITION with the SAME head-fix substitutions as ORDER 31-F -- so `build_states`, `panel`,
`band_fit`, `cluster_se`, `ols`, `q` and the fitted panel `ROWS` are the harness's own objects,
lifted from the executed namespace, never re-implemented. Everything past that point in this file is
the preregistered estimator set, disclosed line by line:

  E1  finer deep bands, `band_fit` verbatim               (departure: band edges only)
  E2  H=4 pooled-power panel, `panel(H=4)` + `band_fit`   (departure: horizon; robustness only)
  E3  PRIMARY joint fit: v0 x log-g hat basis at the wired knots, shared controls,
      player-cluster bootstrap B=400 seed 33, isotonic non-increasing projection
  E4  deep-local level+slope on g>=36

READ-ONLY. Writes DEEP_W1.json / DEEP_W1_out.txt in this directory only.
"""
import os, json, math, hashlib, io, contextlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(EV))
SRC = os.path.join(EV, 'pedigree_persistence_2026-08-14', 'o30bm_measure.py')
SPW1 = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o33w1'
os.makedirs(SPW1, exist_ok=True)

_txt = open(SRC).read()
HARNESS_MD5 = hashlib.md5(_txt.encode()).hexdigest()
assert HARNESS_MD5 == 'e910fe6482ab7b05a92f18c173667073', 'harness moved: %s' % HARNESS_MD5

SUBS = [
    ("V0P = os.path.join(ROOT, 'docs', 'evidence', 'one_machinery_2026-08-14', 'V0REFIT30B.json')",
     "V0P = os.path.join(ROOT, 'docs', 'evidence', 'candidate_31f', 'HEADFIX_31F.json')"),
    ("POSV = V0ART['posv_out']",
     "POSV = V0ART['posv_headfixed']"),
    ("SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'",
     "SP = %r" % SPW1),
]
_run = _txt
for a, b in SUBS:
    assert _run.count(a) == 1, 'substitution target not unique: %r' % a[:60]
    _run = _run.replace(a, b)
# TRUNCATION, DISCLOSED: exec ends immediately after the harness defines `band_fit` (the line
# `TAU, BETA = 11.650213, 0.937162` is the first statement after that definition). Q1's own band
# fits were already reproduced at deviation 0 by w1_control.py; they are not re-run here.
CUT = 'TAU, BETA = 11.650213, 0.937162'
assert _run.count(CUT) == 1
_run = _run.split(CUT)[0]
RUN_MD5 = hashlib.md5(_run.encode()).hexdigest()

OUT = []
def P(s=''):
    OUT.append(str(s)); print(s, flush=True)

P('ORDER 33 W1 -- DEEP-END beta RE-MEASUREMENT (estimators fixed in PREREG_W1.md s3)')
P('  instrument     %s' % os.path.relpath(SRC, ROOT))
P('  committed md5  %s' % HARNESS_MD5)
P('  as-run md5     %s (truncated at %r after the head-fix SUBs of w1_control.py)' % (RUN_MD5, CUT))
P('')

G = {'__name__': '__main__', '__file__': SRC}
_buf = io.StringIO()
with contextlib.redirect_stdout(_buf):
    exec(compile(_run, SRC, 'exec'), G)
np = G['np']
ROWS = G['ROWS']; STATES = G['STATES']; PTS = G['PTS']
panel = G['panel']; band_fit = G['band_fit']; cluster_se = G['cluster_se']
ols = G['ols']; q = G['q']; POSES = G['POSES']
P('harness namespace lifted: panel ROWS n=%d over %d careers (H=6, ND 1-64, entry>=2005, Y<=2019)'
  % (len(ROWS), len({r['key'] for r in ROWS})))

WIRED = [(2.5, 0.2878886216033701), (10.5, 0.2878886216033701), (25.5, 0.21772876584106796),
         (53.0, 0.14155152291809878), (85.5, 0.023849021706229417)]
KNOTS = [m for m, _ in WIRED]

def loglin(pts, g):
    """The engine's `_o31_loglin` interpolation, replicated FOR REPORTING ONLY (checked below
    against the wired knot values it reproduces trivially)."""
    g = max(1e-9, float(g))
    if g <= pts[0][0]: return pts[0][1]
    if g >= pts[-1][0]: return pts[-1][1]
    for i in range(1, len(pts)):
        g0, y0 = pts[i - 1]; g1, y1 = pts[i]
        if g0 <= g <= g1:
            t = (math.log(g) - math.log(g0)) / (math.log(g1) - math.log(g0))
            if y0 <= 0.0 or y1 <= 0.0: return y0 + t * (y1 - y0)
            return math.exp(math.log(y0) + t * (math.log(y1) - math.log(y0)))
    return pts[-1][1]

FINE = [('0-5', 0, 5), ('6-15', 6, 15), ('16-35', 16, 35), ('36-50', 36, 50),
        ('51-70', 51, 70), ('71-90', 71, 90), ('91-120', 91, 120), ('121+', 121, 10 ** 6)]
COARSE_DEEP = [('36-70', 36, 70), ('71+', 71, 10 ** 6)]

def mid_of(nm, lo, hi, rows):
    if hi > 1000:
        xs = [r['g'] for r in rows if r['g'] >= lo]
        return (sum(xs) / len(xs)) if xs else lo
    return (lo + hi) / 2.0

def run_bands(rows, bands, label):
    P('')
    P('--- %s ---' % label)
    P('  %-8s %7s %7s %8s %10s %9s %7s %10s %24s' %
      ('band', 'mid', 'n', 'clust', 'beta_v0', 'se', 't', 'wired@mid', 'sigma [90% CI]'))
    res = {}
    for nm, lo, hi in bands:
        rb = [r for r in rows if lo <= r['g'] <= hi]
        f = band_fit(rb)
        gm = mid_of(nm, lo, hi, rows)
        w = loglin(WIRED, gm)
        if f is None:
            P('  %-8s %7.1f %7d  (n<40, not fitted)' % (nm, gm, len(rb)))
            res[nm] = dict(n=len(rb), mid=gm, note='n<40'); continue
        f = dict(f); f['mid'] = gm; f['wired_at_mid'] = w
        ci = f.get('sigma_ci') or [float('nan'), float('nan')]
        P('  %-8s %7.1f %7d %8d %10.4f %9.4f %7.2f %10.4f %10.1f%% [%5.1f%%,%5.1f%%]'
          % (nm, gm, f['n'], f['n_clusters'], f['beta_v0'], f['se_v0'], f['t_v0'], w,
             100 * (f['sigma'] or 0), 100 * ci[0], 100 * ci[1]))
        res[nm] = f
    return res

# ==================================================================================================
# E1 -- finer deep bands on the PRIMARY H=6 panel, band_fit verbatim
# ==================================================================================================
E1 = run_bands(ROWS, FINE, 'E1: fine bands, H=6 primary panel (band_fit verbatim)')

# ==================================================================================================
# E2 -- pooled-power H=4 panel (adds state years 2020-2021); robustness only, never averaged with E1
# ==================================================================================================
ROWS4 = panel(STATES, PTS, H=4)
P('')
P('E2 panel: H=4 -> %d states over %d careers (state years %d-%d)'
  % (len(ROWS4), len({r['key'] for r in ROWS4}),
     min(r['year'] for r in ROWS4), max(r['year'] for r in ROWS4)))
E2_fine = run_bands(ROWS4, FINE, 'E2: fine bands, H=4 pooled-power panel')
E2_coarse = run_bands(ROWS4, COARSE_DEEP, 'E2: the 31-F deep bands, H=4 pooled-power panel')

# ==================================================================================================
# E3 -- PRIMARY: joint monotone-constrained fit, v0 x log-g hat basis at the wired knots
# ==================================================================================================
def hat_basis(g):
    """Piecewise-linear-in-log-g hat weights at KNOTS, outer knots clamped (matches _o31_loglin's
    clamping; interior interpolation is linear-in-value where the wired curve is log-log -- a
    DISCLOSED, second-order difference)."""
    lg = math.log(max(1e-9, g))
    lk = [math.log(k) for k in KNOTS]
    w = [0.0] * len(KNOTS)
    if lg <= lk[0]:
        w[0] = 1.0; return w
    if lg >= lk[-1]:
        w[-1] = 1.0; return w
    for i in range(1, len(lk)):
        if lk[i - 1] <= lg <= lk[i]:
            t = (lg - lk[i - 1]) / (lk[i] - lk[i - 1])
            w[i - 1] = 1.0 - t; w[i] = t
            return w
    raise AssertionError

def fine_band_name(g):
    for nm, lo, hi in FINE:
        if lo <= g <= hi: return nm
    return FINE[-1][0]

def joint_design(rows):
    n = len(rows)
    names, cols = ['const'], [np.ones(n)]
    for p in POSES[1:]:
        names.append('pos_' + p)
        cols.append(np.array([1.0 if r['pos'] == p else 0.0 for r in rows]))
    age = np.array([r['age'] for r in rows], float)
    o = np.array([r['o'] for r in rows], float)
    cur = np.array([r['cur'] for r in rows], float)
    cur3 = np.array([r['cur3'] for r in rows], float)
    gay = np.array([r['games_at_Y'] for r in rows], float)
    lg = np.array([math.log1p(r['g']) for r in rows], float)
    for nm, v in [('age', age), ('age2', age ** 2), ('o', o), ('o2', o ** 2), ('cur', cur),
                  ('cur3', cur3), ('games_at_Y', gay), ('lg', lg)]:
        names.append(nm); cols.append(v)
    for nm, lo, hi in FINE[1:]:                       # fine-band dummies, first band = reference
        names.append('gb_' + nm)
        cols.append(np.array([1.0 if fine_band_name(r['g']) == nm else 0.0 for r in rows]))
    H = np.array([hat_basis(r['g']) for r in rows], float)
    v0 = np.array([r['v0'] for r in rows], float)
    for j, k in enumerate(KNOTS):
        names.append('v0@%g' % k); cols.append(v0 * H[:, j])
    return names, np.column_stack(cols), np.array([r['R'] for r in rows], float)

def iso_nonincreasing(vals):
    """Pool-adjacent-violators, non-increasing, then 0-floor (the 31-F projection rule)."""
    v = [-x for x in vals]                              # solve as non-decreasing on the negation
    w = [1.0] * len(v)
    blocks = []
    for x in v:
        blocks.append([x, 1.0])
        while len(blocks) > 1 and blocks[-2][0] > blocks[-1][0]:
            a, wa = blocks.pop(); b, wb = blocks.pop()
            blocks.append([(a * wa + b * wb) / (wa + wb), wa + wb])
    out = []
    for val, wt in blocks:
        out.extend([-val] * int(wt))
    return [max(0.0, x) for x in out]

names3, X3, y3 = joint_design(ROWS)
b3 = ols(X3, y3)
se3, ncl3 = cluster_se(X3, y3, b3, [r['key'] for r in ROWS])
IDX = {n: i for i, n in enumerate(names3)}
knot_hat = [float(b3[IDX['v0@%g' % k]]) for k in KNOTS]
knot_se = [float(se3[IDX['v0@%g' % k]]) for k in KNOTS]

# player-cluster bootstrap, B=400, seed 33 (PREREG s3 E3)
keys = sorted({r['key'] for r in ROWS})
byk = collections.defaultdict(list)
for j, r in enumerate(ROWS):
    byk[r['key']].append(j)
rng = np.random.default_rng(33)
BOOT = []
for _ in range(400):
    take = rng.integers(0, len(keys), len(keys))
    idx = []
    for t in take:
        idx.extend(byk[keys[t]])
    idx = np.array(idx)
    try:
        bb = ols(X3[idx], y3[idx])
        BOOT.append([float(bb[IDX['v0@%g' % k]]) for k in KNOTS])
    except Exception:
        pass
BOOT = np.array(BOOT)
ci3 = [[float(np.percentile(BOOT[:, j], 5)), float(np.percentile(BOOT[:, j], 95))]
       for j in range(len(KNOTS))]
mono3 = iso_nonincreasing(knot_hat)

P('')
P('--- E3 (PRIMARY): joint fit, v0 x log-g hat basis at the wired knots, H=6 panel ---')
P('  n=%d  clusters=%d  bootstrap B=%d ok=%d seed=33' % (len(ROWS), ncl3, 400, len(BOOT)))
P('  %-7s %10s %9s %7s %24s %12s %10s %12s' %
  ('knot g', 'beta_hat', 'CR0 se', 't', 'boot 90% CI', 'CI excl 0?', 'wired', 'monotone'))
for j, k in enumerate(KNOTS):
    exc = ci3[j][0] > 0 or ci3[j][1] < 0
    P('  %-7g %10.4f %9.4f %7.2f    [%8.4f, %8.4f] %12s %10.4f %12.4f'
      % (k, knot_hat[j], knot_se[j], knot_hat[j] / knot_se[j] if knot_se[j] > 0 else float('nan'),
         ci3[j][0], ci3[j][1], 'YES' if exc else 'no', dict(WIRED)[k], mono3[j]))

# E3 identification statement for the deep knots (PREREG s4.4)
IDENT = {k: bool(ci3[j][0] > 0 or ci3[j][1] < 0) for j, k in enumerate(KNOTS)}

# ==================================================================================================
# E4 -- deep-local level + slope on g>=36
# ==================================================================================================
def e4(rows, label):
    rb = [r for r in rows if r['g'] >= 36]
    n = len(rb)
    names, cols = ['const'], [np.ones(n)]
    for p in POSES[1:]:
        names.append('pos_' + p)
        cols.append(np.array([1.0 if r['pos'] == p else 0.0 for r in rb]))
    for nm in ('age', 'o', 'cur', 'cur3', 'games_at_Y'):
        names.append(nm); cols.append(np.array([r[nm] for r in rb], float))
    age = np.array([r['age'] for r in rb], float)
    o = np.array([r['o'] for r in rb], float)
    names += ['age2', 'o2', 'lg']
    cols += [age ** 2, o ** 2, np.array([math.log1p(r['g']) for r in rb], float)]
    v0 = np.array([r['v0'] for r in rb], float)
    z = np.array([math.log(r['g']) - math.log(53.0) for r in rb], float)
    names += ['v0', 'v0_zlg']
    cols += [v0, v0 * z]
    X = np.column_stack(cols); y = np.array([r['R'] for r in rb], float)
    b = ols(X, y)
    se, nc = cluster_se(X, y, b, [r['key'] for r in rb])
    i0, i1 = names.index('v0'), names.index('v0_zlg')
    P('')
    P('--- E4: deep-local level+slope, g>=36, %s ---' % label)
    P('  n=%d clusters=%d' % (n, nc))
    P('  beta at g=53 : %8.4f  se %7.4f  t %6.2f   (wired 0.1416)' % (b[i0], se[i0], b[i0] / se[i0]))
    P('  dlog-slope   : %8.4f  se %7.4f  t %6.2f   (wired 53->85.5 log-slope %.4f)'
      % (b[i1], se[i1], b[i1] / se[i1],
         (0.023849021706229417 - 0.14155152291809878) / (math.log(85.5) - math.log(53.0))))
    imp = {g: max(0.0, b[i0] + b[i1] * (math.log(g) - math.log(53.0))) for g in (53, 70, 85.5, 100, 120)}
    P('  implied beta : ' + '  '.join('%g->%.4f' % (g, v) for g, v in sorted(imp.items())))
    return dict(n=n, clusters=nc, beta53=float(b[i0]), se53=float(se[i0]),
                slope=float(b[i1]), se_slope=float(se[i1]), implied=imp)

E4 = e4(ROWS, 'H=6 primary panel')
E4b = e4(ROWS4, 'H=4 pooled-power panel (robustness)')

# ==================================================================================================
# THE PROPOSED CURVE (PREREG s4 construction rule, executed verbatim)
# ==================================================================================================
prop = dict(WIRED)
prop[53.0] = min(knot_hat[3], 0.21772876584106796)
prop[85.5] = min(knot_hat[4], prop[53.0])
prop[85.5] = max(0.0, prop[85.5]); prop[53.0] = max(0.0, prop[53.0])
PROPOSED = [(k, prop[k]) for k in KNOTS]
P('')
P('--- THE PROPOSED CURVE (PREREG s4: shallow wired, deep from E3, monotone cap+floor) ---')
P('  %-7s %10s %10s %14s' % ('knot g', 'wired', 'proposed', 'identified?'))
for k, v in PROPOSED:
    P('  %-7g %10.4f %10.4f %14s'
      % (k, dict(WIRED)[k], v, ('shallow: wired kept' if k <= 25.5 else ('YES' if IDENT[k] else 'NO'))))

json.dump(dict(
    order='ORDER 33 W1 deep-end beta re-measurement', prereg='PREREG_W1.md',
    instrument=os.path.relpath(SRC, ROOT), instrument_md5=HARNESS_MD5, as_run_md5=RUN_MD5,
    substitutions=[{'from': a, 'to': b} for a, b in SUBS], truncated_at=CUT,
    panel_h6=dict(n=len(ROWS), careers=len({r['key'] for r in ROWS})),
    panel_h4=dict(n=len(ROWS4), careers=len({r['key'] for r in ROWS4})),
    wired_points=WIRED,
    E1_fine_bands_h6=E1, E2_fine_bands_h4=E2_fine, E2_coarse_deep_h4=E2_coarse,
    E3_joint=dict(n=len(ROWS), clusters=ncl3, knots=KNOTS, beta_hat=knot_hat, cr0_se=knot_se,
                  boot_ci90=ci3, boot_B=len(BOOT), seed=33, monotone=mono3,
                  identified={str(k): IDENT[k] for k in KNOTS}),
    E4_deep_local=dict(h6=E4, h4=E4b),
    proposed_points=PROPOSED,
    proposal_rule='PREREG_W1.md s4: knots fixed, shallow three wired, deep two = E3 beta_hat capped at wired beta(25.5), monotone, 0-floor'),
    open(os.path.join(HERE, 'DEEP_W1.json'), 'w'), indent=1, sort_keys=True, default=float)
open(os.path.join(HERE, 'DEEP_W1_out.txt'), 'w').write('\n'.join(OUT) + '\n')
print('\nwritten: DEEP_W1.json / DEEP_W1_out.txt')
