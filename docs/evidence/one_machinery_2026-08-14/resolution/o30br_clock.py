#!/usr/bin/env python3
"""ORDER 30B-R -- T2 THE CLOCK.  Recency-weighted evidence u against raw career games g.

The owner's Kako year-3 scenario: path A (36 modest games in years 1-2, then 75 avg over 20 games in
year 3) against path B (sat two years, then the identical season).  Under a raw-games clock B prices
above A.  The candidate fix is the engine's own ruled recency constant d = 0.25/yr:

        u  =  SUM_s  games_s * 0.25 ** (Y - year_s)

This harness re-cuts the 30B-M persistence measurement on BOTH clocks -- same states, same target, same
regression design -- and scores them on the criterion fixed in PREREG_30BR.md section 1:

        5-fold cluster CV, folds by md5(player key) mod 5, pooled OUT-OF-FOLD RMSE against R.

It also asks whether the recency clock subsumes the AGE_LENS separation, and prices the Kako scenario.

READ-ONLY.  Engine staged under the scratchpad for scorer callables only.

  usage:  python3 o30br_clock.py     (writes CLOCK.json + CLOCK_out.txt)
"""
import os, sys, io, json, math, hashlib, shutil, contextlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
STAGE = SP + '/eng30br_clock/rl_after'

L1P = os.path.join(ROOT, 'docs', 'evidence', 'grace_adoption_2026-08-13', 'inputs',
                   'layer1_player_seasons.json')
L1_MD5 = 'ad1229ea6f443538479447132382b21c'
V0P = os.path.join(ROOT, 'docs', 'evidence', 'one_machinery_2026-08-14', 'V0REFIT30B.json')
OUT_JSON = os.path.join(HERE, 'CLOCK.json')
OUT_TXT = os.path.join(HERE, 'CLOCK_out.txt')

D_RECENCY = 0.25          # THE ENGINE'S OWN RULED CONSTANT.  Not fitted, not tuned.

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

# ==================================================================================================
# ENGINE STAGING -- scorer callables only (the 30B-M staging, unchanged)
# ==================================================================================================
shutil.rmtree(SP + '/eng30br_clock', ignore_errors=True)
os.makedirs(os.path.dirname(STAGE), exist_ok=True)
shutil.copytree(ROOT + '/engine/rl_after', STAGE, dirs_exist_ok=True)
if not os.path.exists(os.path.join(STAGE, 'LTI_REGISTER.md')):
    shutil.copy(os.path.join(ROOT, 'LTI_REGISTER.md'), STAGE)
os.environ.update(PYTHONHASHSEED='0', RL_REPO=ROOT, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1',
                  MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1',
                  RL_V0SURF_PKL=ROOT + '/data/v0surf.pkl')
sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', STAGE]
_cwd = os.getcwd(); os.chdir(STAGE)
G = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], G)
os.chdir(_cwd)
MA = G['MA']; rd = G['rd']
import numpy as np

BARS = {g: MA.REPL[g] - rd.REPL_DROP.get(g, 0.0) for g in MA.REPL}
RULING1 = {'KPD': 65.4, 'KPF': 63.8, 'MID': 77.1, 'RUCK': 75.5, 'SD': 75.3, 'SF': 67.9}
for g, b in RULING1.items():
    assert abs(BARS[g] - b) < 5e-2, 'bar %s moved' % g
assert abs(float(MA.GAMMA) - 1.0) < 1e-12
DISC = 0.14
NOW = 2026

def season_points(X, pos, games):
    w = min(1.0, math.sqrt(max(0.0, games) / 10.0))
    return float(MA.SCALE * MA.posval(X + MA.capt_prem(X) - BARS[pos]) * 21.0 * w)

def bar_group(pos_label, fallback):
    if pos_label:
        es = MA._collapse_elig(str(pos_label).replace('/', ','))
        if es:
            return min(es, key=lambda x: MA.REPL[x])
    return fallback

# ==================================================================================================
# DATA -- the 30B-M pins
# ==================================================================================================
assert md5(L1P) == L1_MD5, 'LAYER 1 PIN BROKEN'
L1 = json.load(open(L1P))
ENT = {e['key']: e for e in L1['entries']}
SEA = collections.defaultdict(list)
for s in L1['player_seasons']:
    SEA[s['key']].append(s)
for k in SEA:
    SEA[k].sort(key=lambda x: x['year'])
POSV = json.load(open(V0P))['posv_out']
PINS = dict(layer1=md5(L1P), v0_artifact=md5(V0P),
            merged_recover=md5(os.path.join(ROOT, 'engine/rl_after/_merged_recover.py')),
            store=md5(os.path.join(ROOT, 'engine/rl_after/rl_model_data.json')))
FORCE_MAJEURE = {'thomas-boyd', 'paddy-mccartin'}
POSES = ['KPD', 'KPF', 'MID', 'RUCK', 'SD', 'SF']
PICK_BANDS = [('A 1-6', 1, 6), ('B 7-12', 7, 12), ('C 13-20', 13, 20),
              ('D 21-40', 21, 40), ('E 41-64', 41, 64)]
GAMES_BANDS = [('0-5', 0, 5), ('6-15', 6, 15), ('16-35', 16, 35), ('36-70', 36, 70), ('71+', 71, 1e9)]
AGE_BANDS = [('<=19', 0, 19), ('20', 20, 20), ('21', 21, 21), ('22-23', 22, 23),
             ('24-26', 24, 26), ('27+', 27, 99)]
AGE_GROUP = {'<=19': '<=20', '20': '<=20', '21': '21', '22-23': '22-23', '24-26': '24+', '27+': '24+'}

def band_of(v, bands):
    for nm, lo, hi in bands:
        if lo <= v <= hi:
            return nm
    return None

# ==================================================================================================
# STATES -- the 30B-M construction, plus the recency-weighted clock u
# ==================================================================================================
def build_states():
    states, pts_by = [], {}
    for k, e in ENT.items():
        if k in FORCE_MAJEURE:
            continue
        ss = SEA.get(k, [])
        if not ss:
            continue
        fallback = e['position_group']
        cum = 0.0
        hist = []
        for s in ss:
            pos = bar_group(s['position_played'], fallback)
            if pos not in BARS:
                continue
            pts = season_points(s['avg'], pos, s['games'])
            pts_by[(k, s['year'])] = pts
            hist.append((s['year'], float(s['avg']), float(s['games']), pos, pts))
        for i, (yr, av, gm, pos, pts) in enumerate(hist):
            cum += gm
            # THE RECENCY CLOCK -- d = 0.25 per year back, over every played season up to and incl. Y
            u = 0.0
            for (y2, _a2, g2, _p2, _t2) in hist[:i + 1]:
                u += g2 * (D_RECENCY ** (yr - y2))
            num, den = av * gm, gm
            if i > 0 and (yr - hist[i - 1][0]) <= 2:
                num += hist[i - 1][1] * hist[i - 1][2]; den += hist[i - 1][2]
            o = num / den if den > 0 else av
            last3 = [h[4] for h in hist[max(0, i - 2):i + 1]]
            states.append(dict(key=k, year=yr, pos=pos, entry_pos=e['position_group'],
                               age=yr - e['birth_year'], pick=e['effective_pick'], typ=e['type'],
                               g=cum, u=u, games_at_Y=gm, o=o, avg=av, cur=pts,
                               cur3=sum(last3) / len(last3), entry_year=e['entry_year']))
    return states, pts_by

def remaining(k, Y, H, pts_by):
    tot = 0.0
    for j in range(1, H + 1):
        y = Y + j
        if y >= NOW:
            continue
        tot += pts_by.get((k, y), 0.0) / ((1.0 + DISC) ** j)
    return tot

STATES, PTS = build_states()
H = 6
ROWS = []
for st in STATES:
    if st['entry_year'] is None or st['entry_year'] < 2005:
        continue
    if st['year'] + H > NOW - 1:
        continue
    if not (st['typ'] == 'ND' and st['pick'] and 1 <= st['pick'] <= 64):
        continue
    r = dict(st)
    r['R'] = remaining(st['key'], st['year'], H, PTS)
    r['pb'] = band_of(st['pick'], PICK_BANDS)
    r['ab'] = band_of(st['age'], AGE_BANDS)
    r['ag'] = AGE_GROUP[r['ab']]
    r['v0'] = float(POSV[st['entry_pos']][str(int(st['pick']))])
    ROWS.append(r)

P('=' * 100)
P('ORDER 30B-R -- T2 THE CLOCK: recency-weighted evidence u vs raw career games g')
P('=' * 100)
P('pins: ' + json.dumps(PINS, sort_keys=True))
P('recency constant d = %.2f per year back (THE ENGINE\'S OWN RULED CONSTANT -- not fitted here)' % D_RECENCY)
P('panel: %d states, %d players.  Target R = discounted remaining 6-season delivered value.'
  % (len(ROWS), len({r['key'] for r in ROWS})))
P('CONTROL -- 30B-M reported 4,033 states on this population; this rebuild has %d.' % len(ROWS))
P('')

# ==================================================================================================
# BAND EDGES ON u -- set by the RAW bands' own population quantiles (preregistered, tuning-free)
# ==================================================================================================
gs = sorted(r['g'] for r in ROWS)
us = sorted(r['u'] for r in ROWS)
n = len(ROWS)
raw_edges = [5, 15, 35, 70]
fracs = [sum(1 for x in gs if x <= e) / float(n) for e in raw_edges]
def quant(xs, f):
    i = f * (len(xs) - 1)
    lo = int(math.floor(i)); hi = min(len(xs) - 1, lo + 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (i - lo)
u_edges = [quant(us, f) for f in fracs]
P('u band edges, set by the RAW bands\' own population fractions (no edge chosen after a reading):')
P('   raw edge %5s -> population frac %.4f -> u edge %8.3f' % ('<=5', fracs[0], u_edges[0]))
for e, f, ue in zip(raw_edges[1:], fracs[1:], u_edges[1:]):
    P('   raw edge %5s -> population frac %.4f -> u edge %8.3f' % ('<=%d' % e, f, ue))
U_BANDS = [('U1', -1e9, u_edges[0]), ('U2', u_edges[0], u_edges[1]), ('U3', u_edges[1], u_edges[2]),
           ('U4', u_edges[2], u_edges[3]), ('U5', u_edges[3], 1e9)]
def uband_of(v):
    for nm, lo, hi in U_BANDS:
        if lo < v <= hi or (nm == 'U1' and v <= hi):
            return nm
    return 'U5'
for r in ROWS:
    r['gb'] = band_of(r['g'], GAMES_BANDS)
    r['ub'] = uband_of(r['u'])
P('')
P('band populations:  g %s' % {nm: sum(1 for r in ROWS if r['gb'] == nm) for nm, _, _ in GAMES_BANDS})
P('                   u %s' % {nm: sum(1 for r in ROWS if r['ub'] == nm) for nm, _, _ in U_BANDS})
P('')

# ==================================================================================================
# THE DESIGN MATRIX -- the 30B-M band_fit design, unchanged except which clock enters log1p()
# ==================================================================================================
def design(rows_b, clock):
    m = len(rows_b)
    cols = [np.ones(m)]
    names = ['const']
    for p in POSES[1:]:
        cols.append(np.array([1.0 if r['pos'] == p else 0.0 for r in rows_b])); names.append('pos_' + p)
    for nm, fn in [('age', lambda r: r['age']), ('age2', lambda r: r['age'] ** 2),
                   ('o', lambda r: r['o']), ('o2', lambda r: r['o'] ** 2),
                   ('cur', lambda r: r['cur']), ('cur3', lambda r: r['cur3']),
                   ('games_at_Y', lambda r: r['games_at_Y']),
                   ('lg', lambda r: math.log1p(r[clock]))]:
        cols.append(np.array([float(fn(r)) for r in rows_b])); names.append(nm)
    cols.append(np.array([float(r['v0']) for r in rows_b])); names.append('v0')
    return np.column_stack(cols), np.array([float(r['R']) for r in rows_b]), names

def ols(X, y):
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    return b

def cluster_se(X, y, beta, groups):
    k = X.shape[1]
    r = y - X @ beta
    XtXi = np.linalg.pinv(X.T @ X)
    meat = np.zeros((k, k))
    od = collections.defaultdict(list)
    for i, gg in enumerate(groups):
        od[gg].append(i)
    for idx in od.values():
        u = X[idx].T @ r[idx]
        meat += np.outer(u, u)
    V = XtXi @ meat @ XtXi
    return np.sqrt(np.maximum(np.diag(V), 0.0)), len(od)

def band_fit(rows_b, clock, boot=300, seed=30_140_814):
    m = len(rows_b)
    if m < 40:
        return None
    X, y, names = design(rows_b, clock)
    b = ols(X, y)
    se, ncl = cluster_se(X, y, b, [r['key'] for r in rows_b])
    i = names.index('v0')
    mv0 = float(X[:, i].mean()); mR = float(y.mean())
    sig = b[i] * mv0 / mR if mR > 0 else None
    keys = sorted({r['key'] for r in rows_b})
    byk = collections.defaultdict(list)
    for j, r in enumerate(rows_b):
        byk[r['key']].append(j)
    rng = np.random.default_rng(seed)
    boots = []
    for _ in range(boot):
        pick = rng.integers(0, len(keys), len(keys))
        idx = []
        for t in pick:
            idx.extend(byk[keys[t]])
        idx = np.array(idx)
        try:
            bb = ols(X[idx], y[idx]); mm = float(y[idx].mean())
            if mm > 0:
                boots.append(float(bb[i] * float(X[idx, i].mean()) / mm))
        except Exception:
            pass
    boots.sort()
    def qq(f):
        if not boots:
            return None
        i2 = f * (len(boots) - 1); lo = int(math.floor(i2)); hi = min(len(boots) - 1, lo + 1)
        return boots[lo] + (boots[hi] - boots[lo]) * (i2 - lo)
    return dict(n=m, n_clusters=ncl, beta_v0=float(b[i]), se_v0=float(se[i]),
                t_v0=float(b[i] / se[i]) if se[i] > 0 else None, mean_v0=mv0, mean_R=mR,
                sigma=float(sig) if sig is not None else None,
                sigma_ci=[qq(.05), qq(.95)], sigma_boot_median=qq(.5))

P('=' * 100)
P('T2.1 -- THE PERSISTENCE CURVE ON EACH CLOCK (same states, same target, same design)')
P('=' * 100)
CURVES = {}
for tag, bands, key in (('RAW g', GAMES_BANDS, 'gb'), ('RECENCY u', U_BANDS, 'ub')):
    P('')
    P('  clock = %s' % tag)
    P('  %-8s %6s %7s %10s %8s %9s %20s %10s %10s'
      % ('band', 'n', 'clust', 'beta_v0', 't', 'sigma', 'sigma 90% CI', 'mean v0', 'mean R'))
    cv = {}
    for nm, lo, hi in bands:
        rb = [r for r in ROWS if r[key] == nm]
        f = band_fit(rb, 'g' if key == 'gb' else 'u')
        if f is None:
            P('  %-8s %6d  (n<40, not fitted)' % (nm, len(rb))); continue
        clk = 'g' if key == 'gb' else 'u'
        f['clock_midpoint'] = float(np.median([r[clk] for r in rb]))
        f['clock_lo'] = float(min(r[clk] for r in rb)); f['clock_hi'] = float(max(r[clk] for r in rb))
        cv[nm] = f
        P('  %-8s %6d %7d %10.5f %8.2f %8.1f%% %9.1f%%..%-8.1f%% %10.1f %10.1f'
          % (nm, f['n'], f['n_clusters'], f['beta_v0'], f['t_v0'], 100 * f['sigma'],
             100 * f['sigma_ci'][0], 100 * f['sigma_ci'][1], f['mean_v0'], f['mean_R']))
        P('           %s median clock %.2f  (range %.2f .. %.2f)'
          % (clk, f['clock_midpoint'], f['clock_lo'], f['clock_hi']))
    CURVES[tag] = cv
P('')

# ==================================================================================================
# T2.2 -- THE PREREGISTERED HELD-OUT CRITERION
# ==================================================================================================
P('=' * 100)
P('T2.2 -- HELD-OUT: 5-fold cluster CV, folds by md5(key) mod 5, pooled OOF RMSE.  LOWER WINS.')
P('=' * 100)
FOLD = {}
for r in ROWS:
    FOLD[r['key']] = int(hashlib.md5(r['key'].encode()).hexdigest(), 16) % 5
for r in ROWS:
    r['fold'] = FOLD[r['key']]
P('  fold sizes (states): %s' % {f: sum(1 for r in ROWS if r['fold'] == f) for f in range(5)})
P('  fold sizes (players): %s'
  % {f: len({r['key'] for r in ROWS if r['fold'] == f}) for f in range(5)})

def cv_score(bands, key, clock, clock_by_band=None):
    """clock_by_band, when given, maps band name -> clock name, so a HYBRID arm can use one clock
    in the thin bands and another in the deep ones.  Bands are always assigned by `key`."""
    def clk(bn):
        return clock_by_band.get(bn, clock) if clock_by_band else clock
    pred = np.empty(len(ROWS)); pred[:] = np.nan
    idx_of = {id(r): i for i, r in enumerate(ROWS)}
    nfallback = 0
    for f in range(5):
        tr = [r for r in ROWS if r['fold'] != f]
        te = [r for r in ROWS if r['fold'] == f]
        # pooled fallback model, fitted on the training folds only
        Xp, yp, _ = design(tr, clock)
        bp = ols(Xp, yp)
        models = {}
        for nm, lo, hi in bands:
            sub = [r for r in tr if r[key] == nm]
            if len(sub) < 40:
                continue
            Xb, yb, _ = design(sub, clk(nm))
            models[nm] = ols(Xb, yb)
        bybandte = collections.defaultdict(list)
        for r in te:
            bybandte[r[key] if r[key] in models else '__pool'].append(r)
        for bn, sub in bybandte.items():
            b = models[bn] if bn != '__pool' else bp
            if bn == '__pool':
                nfallback += len(sub)
            Xs, _, _ = design(sub, clock if bn == '__pool' else clk(bn))
            yh = Xs @ b
            for r, v in zip(sub, yh):
                pred[idx_of[id(r)]] = float(v)
    y = np.array([r['R'] for r in ROWS])
    resid = pred - y
    rmse = float(np.sqrt(np.mean(resid ** 2)))
    mae = float(np.mean(np.abs(resid)))
    sst = float(np.sum((y - y.mean()) ** 2))
    r2 = 1.0 - float(np.sum(resid ** 2)) / sst
    return dict(rmse=rmse, mae=mae, r2=r2, n_fallback=nfallback, pred=pred, resid=resid)

SC = {}
SC['RAW g'] = cv_score(GAMES_BANDS, 'gb', 'g')
SC['RECENCY u'] = cv_score(U_BANDS, 'ub', 'u')
P('')
P('  %-12s %12s %12s %10s %10s' % ('clock', 'OOF RMSE', 'OOF MAE', 'OOF R2', 'fallbacks'))
for tag in ('RAW g', 'RECENCY u'):
    s = SC[tag]
    P('  %-12s %12.3f %12.3f %10.5f %10d' % (tag, s['rmse'], s['mae'], s['r2'], s['n_fallback']))
rel = (SC['RAW g']['rmse'] - SC['RECENCY u']['rmse']) / SC['RAW g']['rmse']
P('')
P('  RMSE improvement of u over g: %+.4f%%   -->  WINNER: %s'
  % (100 * rel, 'RECENCY u' if rel > 0 else 'RAW g'))

# paired cluster bootstrap on the RMSE difference, so the verdict carries dispersion
keys = sorted({r['key'] for r in ROWS})
byk = collections.defaultdict(list)
for i, r in enumerate(ROWS):
    byk[r['key']].append(i)
rng = np.random.default_rng(30_140_814)
dif = []
rg, ru = SC['RAW g']['resid'], SC['RECENCY u']['resid']
for _ in range(1000):
    pick = rng.integers(0, len(keys), len(keys))
    idx = []
    for t in pick:
        idx.extend(byk[keys[t]])
    idx = np.array(idx)
    dif.append(float(np.sqrt(np.mean(rg[idx] ** 2)) - np.sqrt(np.mean(ru[idx] ** 2))))
dif.sort()
def bq(f):
    i2 = f * (len(dif) - 1); lo = int(math.floor(i2)); hi = min(len(dif) - 1, lo + 1)
    return dif[lo] + (dif[hi] - dif[lo]) * (i2 - lo)
P('  paired cluster bootstrap (1000 draws) on RMSE(g) - RMSE(u):')
P('     median %+.3f   90%% interval [%+.3f , %+.3f]   share of draws favouring u %.3f'
  % (bq(.5), bq(.05), bq(.95), sum(1 for x in dif if x > 0) / len(dif)))
P('')

# per-band OOF RMSE, so the verdict is not a single pooled number
P('  OOF RMSE by RAW games class, both PREREGISTERED clocks (the same rows scored twice):')
P('  %-8s %6s %12s %12s %10s' % ('cg', 'n', 'RMSE g', 'RMSE u', 'u better?'))
byband = {}
for nm, lo, hi in GAMES_BANDS:
    m = np.array([r['gb'] == nm for r in ROWS])
    if m.sum() == 0:
        continue
    a = float(np.sqrt(np.mean(rg[m] ** 2))); b = float(np.sqrt(np.mean(ru[m] ** 2)))
    byband[nm] = dict(n=int(m.sum()), rmse_g=a, rmse_u=b)
    P('  %-8s %6d %12.3f %12.3f %10s' % (nm, m.sum(), a, b, 'YES' if b < a else 'no'))
P('')
P('  ---- POST-HOC, NOT PREREGISTERED, LABELLED AS SUCH -------------------------------------------')
P('  The band table above points straight at a hybrid: the recency clock wins where evidence is thin')
P('  and loses where careers are long.  A third arm is therefore scored and reported.  It did NOT')
P('  exist in the prereg, it is NOT eligible to win the criterion, and it is published so the owner')
P('  can see it rather than have it discovered later.')
P('     HYBRID: bands assigned by RAW g; the log1p(clock) term reads u in 0-5 / 6-15 / 16-35 and')
P('             g in 36-70 / 71+.')
HYB = {'0-5': 'u', '6-15': 'u', '16-35': 'u', '36-70': 'g', '71+': 'g'}
SC['HYBRID (post-hoc)'] = cv_score(GAMES_BANDS, 'gb', 'g', clock_by_band=HYB)
sh = SC['HYBRID (post-hoc)']
P('     OOF RMSE %.3f   MAE %.3f   R2 %.5f   (raw g %.3f, recency u %.3f)'
  % (sh['rmse'], sh['mae'], sh['r2'], SC['RAW g']['rmse'], SC['RECENCY u']['rmse']))
P('     improvement over raw g: %+.4f%%'
  % (100 * (SC['RAW g']['rmse'] - sh['rmse']) / SC['RAW g']['rmse']))
rh = sh['resid']
difh = []
rng3 = np.random.default_rng(30_140_814)
for _ in range(1000):
    pick = rng3.integers(0, len(keys), len(keys))
    idx = []
    for t in pick:
        idx.extend(byk[keys[t]])
    idx = np.array(idx)
    difh.append(float(np.sqrt(np.mean(rg[idx] ** 2)) - np.sqrt(np.mean(rh[idx] ** 2))))
difh.sort()
def bqh(f):
    i2 = f * (len(difh) - 1); lo = int(math.floor(i2)); hi = min(len(difh) - 1, lo + 1)
    return difh[lo] + (difh[hi] - difh[lo]) * (i2 - lo)
P('     paired cluster bootstrap on RMSE(g) - RMSE(hybrid): median %+.3f  90%% [%+.3f , %+.3f]'
  % (bqh(.5), bqh(.05), bqh(.95)))
P('     share of draws favouring the hybrid: %.3f' % (sum(1 for x in difh if x > 0) / len(difh)))
HYBOOT = dict(median=bqh(.5), lo=bqh(.05), hi=bqh(.95),
              share_favouring=sum(1 for x in difh if x > 0) / len(difh))
P('  ----------------------------------------------------------------------------------------------')
P('')
P('  CLOCK SATURATION, the mechanism behind the deep-band loss:')
P('     raw g  spans %.0f .. %.0f  (ratio %.1fx)' % (min(gs), max(gs), max(gs) / max(1e-9, min(gs))))
P('     u      spans %.2f .. %.2f  (ratio %.1fx)' % (min(us), max(us), max(us) / max(1e-9, min(us))))
P('     with d = 0.25 a full-season player converges to 20/(1-0.25) = %.2f, so the recency clock'
  % (20.0 / (1 - D_RECENCY)))
P('     CANNOT separate a 71-game player from a 295-game one.  The 71+ band (n %d) spans u %.2f..%.2f.'
  % (sum(1 for r in ROWS if r['gb'] == '71+'),
     min(r['u'] for r in ROWS if r['gb'] == '71+'), max(r['u'] for r in ROWS if r['gb'] == '71+')))
SAT = dict(g_min=min(gs), g_max=max(gs), u_min=min(us), u_max=max(us),
           u_asymptote_20g_season=20.0 / (1 - D_RECENCY),
           u_range_in_71plus=[min(r['u'] for r in ROWS if r['gb'] == '71+'),
                              max(r['u'] for r in ROWS if r['gb'] == '71+')])
P('')

# ==================================================================================================
# T2.3 -- DOES THE RECENCY CLOCK SUBSUME THE AGE_LENS SEPARATION?
# ==================================================================================================
P('=' * 100)
P('T2.3 -- THE AGE LENS UNDER EACH CLOCK (matched pick contrast, pos x age-group x output quintile)')
P('=' * 100)
HIB = ('A 1-6', 'B 7-12')
LOB = ('D 21-40', 'E 41-64')

def out_quintiles(rows):
    cuts = {}
    for p in POSES:
        xs = sorted(r['o'] for r in rows if r['pos'] == p)
        if len(xs) < 25:
            cuts[p] = None; continue
        cuts[p] = [quant(xs, f) for f in (.2, .4, .6, .8)]
    return cuts
OQ = out_quintiles(ROWS)
def oband(r):
    c = OQ.get(r['pos'])
    if c is None:
        return 'all'
    for i, t in enumerate(c):
        if r['o'] <= t:
            return 'q%d' % (i + 1)
    return 'q5'
for r in ROWS:
    r['oq'] = oband(r)

def matched_contrast(rows, min_cell=8):
    """High-pick minus low-pick, matched within (pos x output quintile) strata, n-weighted."""
    st = collections.defaultdict(lambda: {'hi': [], 'lo': []})
    for r in rows:
        k = (r['pos'], r['oq'])
        if r['pb'] in HIB:
            st[k]['hi'].append(r['R'])
        elif r['pb'] in LOB:
            st[k]['lo'].append(r['R'])
    num = den = 0.0
    used = 0
    per = []
    for k, d in st.items():
        if len(d['hi']) < min_cell or len(d['lo']) < min_cell:
            continue
        w = len(d['hi']) + len(d['lo'])
        g = sum(d['hi']) / len(d['hi']) - sum(d['lo']) / len(d['lo'])
        num += w * g; den += w; used += 1
        per.append((k, g, len(d['hi']), len(d['lo'])))
    if den == 0:
        return None
    return dict(delta=num / den, n=int(den), strata=used, per=[(list(a), b, c, d2) for a, b, c, d2 in per])

def boot_gap(rows_a, rows_b, mc=8, draws=600, seed=30_140_814):
    """Cluster bootstrap of [matched(a) - matched(b)], resampling players."""
    allr = rows_a + rows_b
    keys = sorted({r['key'] for r in allr})
    byk2 = collections.defaultdict(list)
    for r in allr:
        byk2[r['key']].append(r)
    tag = {id(r): 'a' for r in rows_a}
    rng2 = np.random.default_rng(seed)
    out = []
    for _ in range(draws):
        pick = rng2.integers(0, len(keys), len(keys))
        A, B = [], []
        for t in pick:
            for r in byk2[keys[t]]:
                (A if tag.get(id(r)) == 'a' else B).append(r)
        ma, mb = matched_contrast(A, mc), matched_contrast(B, mc)
        if ma and mb:
            out.append(ma['delta'] - mb['delta'])
    out.sort()
    if not out:
        return None
    def qb(f):
        i2 = f * (len(out) - 1); lo = int(math.floor(i2)); hi = min(len(out) - 1, lo + 1)
        return out[lo] + (out[hi] - out[lo]) * (i2 - lo)
    m = sum(out) / len(out)
    sd = math.sqrt(sum((x - m) ** 2 for x in out) / max(1, len(out) - 1))
    return dict(median=qb(.5), lo=qb(.05), hi=qb(.95), sd=sd, z=(m / sd if sd > 0 else None), draws=len(out))

AGELENS = {}
shrink = {}
P('')
P('  NOTE ON CELL MINIMA, stated before the numbers: the preview AGE_LENS pooled the COMMITTED cell')
P('  table (pos|age|games band|output quintile|pick band, min cell 8).  This harness re-cuts the PANEL,')
P('  so the 24+ x 16-35 subgroup is thin at min-cell 8 and empties.  Both minima are published; the')
P('  verdict is stated so that it does not depend on which is read.')
for mc in (8, 3):
    AGELENS['min_cell_%d' % mc] = {}
    P('')
    P('  --- stratum cell minimum = %d ---' % mc)
    for tag, key, target in (('RAW g', 'gb', '16-35'), ('RECENCY u', 'ub', 'U3')):
        band = [r for r in ROWS if r[key] == target]
        young = [r for r in band if r['ag'] == '<=20']
        old = [r for r in band if r['ag'] == '24+']
        my = matched_contrast(young, mc)
        mo = matched_contrast(old, mc)
        bg = boot_gap(young, old, mc=mc) if (my and mo) else None
        AGELENS['min_cell_%d' % mc][tag] = dict(
            band=target, n_band=len(band), n_young=len(young), n_old=len(old),
            young=my, old=mo, gap=(my['delta'] - mo['delta']) if (my and mo) else None, boot=bg)
        P('  clock %-11s band %-6s (n %d states; <=20 n %d, 24+ n %d)'
          % (tag, target, len(band), len(young), len(old)))
        P('     <=20 : %s' % (('matched contrast %+9.1f  n %4d over %d strata'
                               % (my['delta'], my['n'], my['strata'])) if my else 'EMPTY at this minimum'))
        P('     24+  : %s' % (('matched contrast %+9.1f  n %4d over %d strata'
                               % (mo['delta'], mo['n'], mo['strata'])) if mo else 'EMPTY at this minimum'))
        if my and mo:
            P('     GAP  : %+9.1f' % (my['delta'] - mo['delta']))
        if bg:
            P('     cluster bootstrap of the gap: median %+.1f  90%% [%+.1f , %+.1f]  z %+.2f  (%d draws)'
              % (bg['median'], bg['lo'], bg['hi'], bg['z'], bg['draws']))
    a = AGELENS['min_cell_%d' % mc]['RAW g']['gap']
    b = AGELENS['min_cell_%d' % mc]['RECENCY u']['gap']
    if a and b:
        shrink['min_cell_%d' % mc] = 1.0 - b / a
        P('     GAP SHRINKAGE, raw clock -> recency clock: %+.1f%%' % (100 * (1.0 - b / a)))
    else:
        shrink['min_cell_%d' % mc] = None
        P('     GAP SHRINKAGE: NOT COMPUTABLE at this minimum -- one cell is empty.')
P('')

# ==================================================================================================
# T2.4 -- THE OWNER'S KAKO YEAR-3 SCENARIO
# ==================================================================================================
P('=' * 100)
P('T2.4 -- THE KAKO YEAR-3 SCENARIO, PRICED UNDER BOTH CLOCKS')
P('=' * 100)
POS = 'SF'; PICK = 13; AGE3 = 20
V0K = float(POSV[POS][str(PICK)])
MOD_G = 18.0                     # "36 modest games in years 1-2" = 18 + 18
GOOD_AVG, GOOD_G = 75.0, 20.0    # "75 avg over 20 games in year 3"
MOD_GRID = [55.0, 60.0, 65.0, 70.0]   # "modest" is not a number; the whole grid is published
P('  stipulated: SF, effective pick %d, age %d at the end of year 3, Step-1 v0 = %.1f' % (PICK, AGE3, V0K))
P('  path A: %.0f games in each of years 1 and 2 (36 total) at a MODEST avg, then %.0f games @ %.0f in yr 3'
  % (MOD_G, GOOD_G, GOOD_AVG))
P('  path B: no games in years 1 and 2, then the IDENTICAL year-3 season')
P('  "modest" is not a number, so the whole grid %s is published; the SF bar is %.1f.'
  % (MOD_GRID, BARS[POS]))
P('')
pts3 = season_points(GOOD_AVG, POS, GOOD_G)
gA, gB = MOD_G * 2 + GOOD_G, GOOD_G
uA = GOOD_G + MOD_G * D_RECENCY + MOD_G * (D_RECENCY ** 2)
uB = GOOD_G
oB = GOOD_AVG
stB = dict(key='__pathB', pos=POS, age=AGE3, g=gB, u=uB, games_at_Y=GOOD_G, o=oB, cur=pts3,
           cur3=pts3, v0=V0K, R=0.0)
P('  path A: raw g %6.2f   recency u %6.2f' % (gA, uA))
P('  path B: raw g %6.2f   recency u %6.2f   output window o %5.2f   cur %8.1f' % (gB, uB, oB, pts3))
P('')

# --- LENS 1: the measurement's own currency -- fitted remaining value under each clock -----------
P('  LENS 1 -- the MEASUREMENT\'s currency: predicted remaining 6-season delivered value R-hat')
P('            from the band model each clock selects.  Full-panel fits (not held-out).')
FITB = {}
for tag, bands, key, clock in (('RAW g', GAMES_BANDS, 'gb', 'g'), ('RECENCY u', U_BANDS, 'ub', 'u')):
    mods = {}
    for nm, lo, hi in bands:
        sub = [r for r in ROWS if r[key] == nm]
        if len(sub) >= 40:
            X, y, names = design(sub, clock)
            mods[nm] = (ols(X, y), names)
    FITB[tag] = mods
SCEN = {}
P('  %-6s %-11s %8s %8s %12s %12s %10s' % ('modest', 'clock', 'band A', 'band B', 'R-hat A', 'R-hat B', 'B over A'))
for mav in MOD_GRID:
    ptsA = season_points(mav, POS, MOD_G)
    oA = (GOOD_AVG * GOOD_G + mav * MOD_G) / (GOOD_G + MOD_G)
    stA = dict(key='__pathA', pos=POS, age=AGE3, g=gA, u=uA, games_at_Y=GOOD_G, o=oA, cur=pts3,
               cur3=(ptsA + ptsA + pts3) / 3.0, v0=V0K, R=0.0)
    for tag, clock, bandfn in (('RAW g', 'g', lambda v: band_of(v, GAMES_BANDS)),
                               ('RECENCY u', 'u', uband_of)):
        res = {}
        for pn, st in (('A', stA), ('B', stB)):
            bn = bandfn(st[clock])
            b, names = FITB[tag][bn]
            X, _, _ = design([st], clock)
            res[pn] = dict(band=bn, Rhat=float((X @ b)[0]), clock_value=st[clock])
        res['B_over_A'] = res['B']['Rhat'] / res['A']['Rhat'] if res['A']['Rhat'] else None
        res['modest_avg'] = mav
        res['pathA_o'] = oA
        res['pathA_cur3'] = stA['cur3']
        SCEN['%s @ modest %.0f' % (tag, mav)] = res
        P('  %-6.0f %-11s %8s %8s %12.1f %12.1f %+9.2f%%'
          % (mav, tag, res['A']['band'], res['B']['band'], res['A']['Rhat'], res['B']['Rhat'],
             100 * (res['B_over_A'] - 1)))
P('')

# --- LENS 2: the BOARD's currency -- the blend arithmetic with the production leg held identical --
P('  LENS 2 -- the BOARD\'s currency: the blend arithmetic with the PRODUCTION LEG HELD IDENTICAL')
P('            between the two paths, so the ONLY difference priced is the evidence clock.')
P('            sigma is the 30B-P wired curve exp(-(x/23)^0.80) evaluated on each clock\'s axis,')
P('            and re-fitted to THIS order\'s own u-curve for the recency row.  Both shown.')

def fit_tau_beta(points):
    """n-weighted least squares over the ruled family exp(-(x/tau)^beta), the 30B-M grid."""
    best = None
    for tau in [x / 2.0 for x in range(4, 801)]:
        for bb in [x / 100.0 for x in range(20, 201)]:
            sse = 0.0
            for x, s, w in points:
                pr = math.exp(-((max(1e-9, x) / tau) ** bb))
                sse += w * (100 * (pr - s)) ** 2
            if best is None or sse < best[2]:
                best = (tau, bb, sse)
    return best

pts_g = [(CURVES['RAW g'][nm]['clock_midpoint'], CURVES['RAW g'][nm]['sigma'], CURVES['RAW g'][nm]['n'])
         for nm, _, _ in GAMES_BANDS if nm in CURVES['RAW g']]
pts_u = [(CURVES['RECENCY u'][nm]['clock_midpoint'], CURVES['RECENCY u'][nm]['sigma'], CURVES['RECENCY u'][nm]['n'])
         for nm, _, _ in U_BANDS if nm in CURVES['RECENCY u']]
TAU_G, BETA_G, SSE_G = fit_tau_beta(pts_g)
TAU_U, BETA_U, SSE_U = fit_tau_beta(pts_u)
P('')
P('     refit of the ruled family to THIS order\'s band medians:')
P('        raw g   : tau %7.2f  beta %5.2f  n-weighted SSE %10.2f   (30B-P wired: tau 23.00 beta 0.80)'
  % (TAU_G, BETA_G, SSE_G))
P('        recency u: tau %7.2f  beta %5.2f  n-weighted SSE %10.2f' % (TAU_U, BETA_U, SSE_U))

def sig_of(x, tau, bb):
    return math.exp(-((max(1e-9, x) / tau) ** bb))

PROD = 744.3   # kako's own measured preview production leg -- STIPULATED, held identical A and B
L2 = {}
P('')
P('     production leg held at %.1f (kako\'s own measured preview leg), v0 = %.1f' % (PROD, V0K))
P('     %-26s %8s %8s %10s %10s %9s' % ('clock / curve', 'sigma A', 'sigma B', 'price A', 'price B', 'B over A'))
for lab, xa, xb, tau, bb in (('raw g, 30B-P wired curve', gA, gB, 23.0, 0.80),
                             ('raw g, this order refit', gA, gB, TAU_G, BETA_G),
                             ('recency u, this order refit', uA, uB, TAU_U, BETA_U)):
    sa, sb = sig_of(xa, tau, bb), sig_of(xb, tau, bb)
    pa = (1 - sa) * PROD + sa * V0K
    pb = (1 - sb) * PROD + sb * V0K
    L2[lab] = dict(sigma_A=sa, sigma_B=sb, price_A=pa, price_B=pb, B_over_A=pb / pa)
    P('     %-26s %8.4f %8.4f %10.1f %10.1f %+8.2f%%' % (lab, sa, sb, pa, pb, 100 * (pb / pa - 1)))
P('')
P('     SENSITIVITY -- the same three rows with the production leg swept, since B/A depends on P vs v0:')
P('     %-26s %10s %10s %10s %10s %10s' % ('clock / curve', 'P=300', 'P=600', 'P=900', 'P=1500', 'P=2500'))
SWEEP = {}
for lab, xa, xb, tau, bb in (('raw g, 30B-P wired curve', gA, gB, 23.0, 0.80),
                             ('raw g, this order refit', gA, gB, TAU_G, BETA_G),
                             ('recency u, this order refit', uA, uB, TAU_U, BETA_U)):
    sa, sb = sig_of(xa, tau, bb), sig_of(xb, tau, bb)
    row = []
    for Pv in (300.0, 600.0, 900.0, 1500.0, 2500.0):
        pa = (1 - sa) * Pv + sa * V0K
        pb = (1 - sb) * Pv + sb * V0K
        row.append(pb / pa - 1)
    SWEEP[lab] = row
    P('     %-26s %9.2f%% %9.2f%% %9.2f%% %9.2f%% %9.2f%%' % tuple([lab] + [100 * x for x in row]))
P('')

RES = dict(order='30B-R', task='T2 the clock', pins=PINS, d_recency=D_RECENCY,
           panel=dict(n_states=len(ROWS), n_players=len({r['key'] for r in ROWS}),
                      raw_bands=[[a, b, c] for a, b, c in GAMES_BANDS],
                      u_band_edges=u_edges, u_band_fractions=fracs),
           curves={k: v for k, v in CURVES.items()},
           cv={k: {kk: vv for kk, vv in v.items() if kk not in ('pred', 'resid')} for k, v in SC.items()},
           cv_rel_improvement_u_over_g=rel,
           cv_bootstrap=dict(median=bq(.5), lo=bq(.05), hi=bq(.95),
                             share_favouring_u=sum(1 for x in dif if x > 0) / len(dif), draws=len(dif)),
           cv_by_raw_band=byband, hybrid_post_hoc=dict(bootstrap=HYBOOT, map=HYB),
           clock_saturation=SAT,
           age_lens=AGELENS, age_gap_shrinkage=shrink,
           kako=dict(v0=V0K, modest_grid=MOD_GRID,
                     path_A=dict(g=gA, u=uA, games_yr12=MOD_G),
                     path_B=dict(g=gB, u=uB, o=oB, cur=pts3, cur3=stB['cur3']),
                     lens1_fitted_remaining=SCEN,
                     lens2_board_arithmetic=L2, lens2_sweep=SWEEP,
                     sigma_refits=dict(raw=[TAU_G, BETA_G, SSE_G], recency=[TAU_U, BETA_U, SSE_U],
                                       points_raw=pts_g, points_recency=pts_u)))
json.dump(RES, open(OUT_JSON, 'w'), indent=1, sort_keys=True, default=float)
open(OUT_TXT, 'w').write('\n'.join(_LOG) + '\n')
P('wrote %s and %s' % (OUT_JSON, OUT_TXT))
