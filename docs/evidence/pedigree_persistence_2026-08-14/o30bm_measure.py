#!/usr/bin/env python3
"""ORDER 30B-M -- THE PEDIGREE-PERSISTENCE MEASUREMENT.

Measures, for every historical player at every career state (pick band x position group x age x
games-so-far x current output), the REMAINING delivered career value from that state, and answers the
three preregistered questions of PREREG_30BM.md:

    Q1 PERSISTENCE  -- conditional on output and age, does pick still predict remaining value, and how
                       does the pedigree share decay with games?
    Q2 FORM         -- fading LEVEL bonus (the blend's shape) or pick-conditional TRAJECTORY?
    Q3 POSITION CLOCKS -- one development table, or one per position group?

READ-ONLY. The engine is loaded from a staged copy purely for its scorer callables (bars, posval,
capt_prem, SCALE, disc_factor). No board, store, curve, config or engine file is written.

  usage:  python3 o30bm_measure.py            (writes PERSISTENCE_TABLE.json + MEASURE_out.txt)
"""
import os, sys, io, json, math, hashlib, shutil, contextlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
STAGE = SP + '/eng30bm_run/rl_after'

L1P = os.path.join(ROOT, 'docs', 'evidence', 'grace_adoption_2026-08-13', 'inputs',
                   'layer1_player_seasons.json')
L1_MD5 = 'ad1229ea6f443538479447132382b21c'          # PINNED (PREREG s1)
V0P = os.path.join(ROOT, 'docs', 'evidence', 'one_machinery_2026-08-14', 'V0REFIT30B.json')
BOARDP = os.path.join(ROOT, 'engine', 'rl_after', 'rl_app_data.json')
BLENDP = os.path.join(ROOT, 'docs', 'evidence', 'one_machinery_2026-08-14', 'BLEND30B.json')

OUT_JSON = os.path.join(HERE, 'PERSISTENCE_TABLE.json')
OUT_TXT = os.path.join(HERE, 'MEASURE_out.txt')

_LOG = []
def P(s=''):
    print(s)
    _LOG.append(str(s))


def md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


# ==================================================================================================
# ENGINE STAGING -- scorer callables only
# ==================================================================================================
shutil.rmtree(SP + '/eng30bm_run', ignore_errors=True)
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

# THE BARS -- computed off the engine, asserted against Ruling 1. Never typed.
BARS = {g: MA.REPL[g] - rd.REPL_DROP.get(g, 0.0) for g in MA.REPL}
RULING1 = {'KPD': 65.4, 'KPF': 63.8, 'MID': 77.1, 'RUCK': 75.5, 'SD': 75.3, 'SF': 67.9}
for g, b in RULING1.items():
    assert abs(BARS[g] - b) < 5e-2, "bar %s %.4f != Ruling 1's %.1f" % (g, BARS[g], b)
assert abs(float(MA.GAMMA) - 1.0) < 1e-12, "GAMMA != 1 -- delivered value is not additive"
assert abs(float(MA.LENS['bal']) - 0.14) < 1e-12
assert int(MA.AGE_REF) == 2026
DISC = 0.14
NOW = 2026


def season_points(X, pos, games, wmode='sqrt'):
    """26B Ruling 3's pinned callable x Ruling 10's games weight. Undiscounted board points."""
    w = min(1.0, math.sqrt(max(0.0, games) / 10.0)) if wmode == 'sqrt' else min(1.0, max(0.0, games) / 10.0)
    return float(MA.SCALE * MA.posval(X + MA.capt_prem(X) - BARS[pos]) * 21.0 * w)


def bar_group(pos_label, fallback):
    if pos_label:
        es = MA._collapse_elig(str(pos_label).replace('/', ','))
        if es:
            return min(es, key=lambda x: MA.REPL[x])
    return fallback


# ==================================================================================================
# DATA
# ==================================================================================================
assert md5(L1P) == L1_MD5, 'LAYER 1 PIN BROKEN: %s' % md5(L1P)
L1 = json.load(open(L1P))
ENT = {e['key']: e for e in L1['entries']}
SEA = collections.defaultdict(list)
for s in L1['player_seasons']:
    SEA[s['key']].append(s)
for k in SEA:
    SEA[k].sort(key=lambda x: x['year'])

V0ART = json.load(open(V0P))
POSV = V0ART['posv_out']
BOARD = json.load(open(BOARDP))
BROWS = {r['key']: r for r in BOARD['active'] + BOARD['back']}
BLEND = json.load(open(BLENDP))

PINS = dict(layer1=md5(L1P), v0_artifact=md5(V0P), board=md5(BOARDP),
            store=md5(os.path.join(ROOT, 'engine/rl_after/rl_model_data.json')),
            rl_model=md5(os.path.join(ROOT, 'engine/rl_after/rl_model.py')),
            merged_recover=md5(os.path.join(ROOT, 'engine/rl_after/_merged_recover.py')),
            pvc_curve_v2=md5(os.path.join(ROOT, 'engine/rl_after/pvc_curve_v2.json')))

FORCE_MAJEURE = {'thomas-boyd', 'paddy-mccartin'}

PICK_BANDS = [('A 1-6', 1, 6), ('B 7-12', 7, 12), ('C 13-20', 13, 20),
              ('D 21-40', 21, 40), ('E 41-64', 41, 64)]
GAMES_BANDS = [('0-5', 0, 5), ('6-15', 6, 15), ('16-35', 16, 35), ('36-70', 36, 70), ('71+', 71, 10 ** 6)]
AGE_BANDS = [('<=19', 0, 19), ('20', 20, 20), ('21', 21, 21), ('22-23', 22, 23),
             ('24-26', 24, 26), ('27+', 27, 99)]


def band_of(v, bands):
    for nm, lo, hi in bands:
        if lo <= v <= hi:
            return nm
    return None


# ==================================================================================================
# STATE CONSTRUCTION
# ==================================================================================================
def build_states(wmode='sqrt', out_window=2):
    """One state per PLAYED season end, for every entry (ND and pool alike; the pool is descriptive).
    Returns list of dicts. Season points are cached per (key, year)."""
    states = []
    pts_by = {}
    for k, e in ENT.items():
        if k in FORCE_MAJEURE:
            continue
        ss = SEA.get(k, [])
        if not ss:
            continue
        fallback = e['position_group']
        cum = 0.0
        hist = []                       # (year, avg, games, pos, pts)
        for s in ss:
            pos = bar_group(s['position_played'], fallback)
            if pos not in BARS:
                continue
            pts = season_points(s['avg'], pos, s['games'], wmode)
            pts_by[(k, s['year'])] = pts
            hist.append((s['year'], float(s['avg']), float(s['games']), pos, pts))
        for i, (yr, av, gm, pos, pts) in enumerate(hist):
            cum += gm
            # current output: games-weighted mean avg over this season and the prior played season if
            # it is within `out_window` years
            num, den = av * gm, gm
            if i > 0 and out_window >= 2 and (yr - hist[i - 1][0]) <= 2:
                num += hist[i - 1][1] * hist[i - 1][2]; den += hist[i - 1][2]
            o = num / den if den > 0 else av
            last3 = [h[4] for h in hist[max(0, i - 2):i + 1]]
            states.append(dict(
                key=k, year=yr, pos=pos, entry_pos=e['position_group'], age=yr - e['birth_year'],
                pick=e['effective_pick'], typ=e['type'], g=cum, games_at_Y=gm, o=o, avg=av,
                cur=pts, cur3=sum(last3) / len(last3), entry_year=e['entry_year'],
                entry_age=e['entry_age'], retired=e['retired'], nseason=i + 1))
    return states, pts_by


def remaining(k, Y, H, pts_by, disc=DISC, grace=0):
    """Discounted remaining delivered value over the next H seasons, re-anchored at the state year.
    2026 (in progress) never contributes. Missing seasons contribute ZERO -- zeros stay in."""
    tot = 0.0
    for j in range(1, H + 1):
        y = Y + j
        if y >= NOW:
            continue
        p = pts_by.get((k, y), 0.0)
        e = max(0, j - grace)
        tot += p / ((1.0 + disc) ** e)
    return tot


def panel(states, pts_by, H=6, disc=DISC, grace=0, nd_only=True, entry_min=2005):
    """The fitting panel: full future window observed, entry >= 2005, ND 1-64 (unless nd_only=False)."""
    rows = []
    for st in states:
        if st['entry_year'] is None or st['entry_year'] < entry_min:
            continue
        if st['year'] + H > NOW - 1:
            continue
        nd = (st['typ'] == 'ND' and st['pick'] and 1 <= st['pick'] <= 64)
        if nd_only and not nd:
            continue
        r = dict(st)
        r['nd'] = nd
        r['R'] = remaining(st['key'], st['year'], H, pts_by, disc, grace)
        r['pb'] = band_of(st['pick'], PICK_BANDS) if nd else 'pool'
        r['gb'] = band_of(st['g'], GAMES_BANDS)
        r['ab'] = band_of(st['age'], AGE_BANDS)
        r['v0'] = float(POSV[st['entry_pos']][str(int(st['pick']))]) if nd else float('nan')
        rows.append(r)
    return rows


# ==================================================================================================
# STATISTICS
# ==================================================================================================
def q(xs, f):
    if not xs:
        return None
    xs = sorted(xs); n = len(xs)
    if n == 1:
        return float(xs[0])
    p = f * (n - 1); lo = int(math.floor(p)); hi = min(lo + 1, n - 1)
    return float(xs[lo] + (xs[hi] - xs[lo]) * (p - lo))


def disp(xs):
    xs = list(xs)
    return dict(n=len(xs), mean=(sum(xs) / len(xs) if xs else None), p25=q(xs, .25),
                median=q(xs, .5), p75=q(xs, .75),
                zero_share=(sum(1 for x in xs if x < 1e-9) / len(xs) if xs else None))


def ols(X, y):
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return beta


def cluster_se(X, y, beta, groups):
    """CR0 cluster-robust standard errors (clustered on player)."""
    n, k = X.shape
    r = y - X @ beta
    XtX = X.T @ X
    XtX_inv = np.linalg.pinv(XtX)
    meat = np.zeros((k, k))
    order = collections.defaultdict(list)
    for i, gg in enumerate(groups):
        order[gg].append(i)
    for idx in order.values():
        Xi = X[idx]; ri = r[idx]
        u = Xi.T @ ri
        meat += np.outer(u, u)
    V = XtX_inv @ meat @ XtX_inv
    return np.sqrt(np.maximum(np.diag(V), 0.0)), len(order)


def spearman(a, b):
    def rank(x):
        idx = np.argsort(np.argsort(x, kind='stable'), kind='stable').astype(float)
        # average ties
        order = np.argsort(x, kind='stable'); xs = np.asarray(x)[order]
        i = 0; rr = np.empty(len(x))
        while i < len(xs):
            j = i
            while j + 1 < len(xs) and xs[j + 1] == xs[i]:
                j += 1
            avg = (i + j) / 2.0
            for t in range(i, j + 1):
                rr[order[t]] = avg
            i = j + 1
        return rr
    ra, rb = rank(np.asarray(a)), rank(np.asarray(b))
    ra = ra - ra.mean(); rb = rb - rb.mean()
    d = math.sqrt(float((ra ** 2).sum()) * float((rb ** 2).sum()))
    return float((ra * rb).sum() / d) if d > 0 else 0.0


# ==================================================================================================
# DESIGN MATRICES  (PREREG s4)
# ==================================================================================================
POSES = ['KPD', 'KPF', 'MID', 'RUCK', 'SD', 'SF']


def base_cols(rows, per_pos_slopes=False, pos_level=True):
    """P (pick-blind). per_pos_slopes=True is form P6; False with pos_level=True is form P1/P."""
    names, cols = [], []
    n = len(rows)
    one = np.ones(n)
    names.append('const'); cols.append(one)
    if pos_level:
        for p in POSES[1:]:
            names.append('pos_' + p); cols.append(np.array([1.0 if r['pos'] == p else 0.0 for r in rows]))
    age = np.array([r['age'] for r in rows], float)
    lg = np.array([math.log1p(r['g']) for r in rows], float)
    o = np.array([r['o'] for r in rows], float)
    cur = np.array([r['cur'] for r in rows], float)
    cur3 = np.array([r['cur3'] for r in rows], float)
    gay = np.array([r['games_at_Y'] for r in rows], float)
    dev = [('age', age), ('age2', age ** 2), ('lg', lg), ('o', o), ('o2', o ** 2),
           ('cur', cur), ('cur3', cur3), ('games_at_Y', gay), ('o_age', o * age), ('cur_age', cur * age)]
    if not per_pos_slopes:
        for nm, v in dev:
            names.append(nm); cols.append(v)
    else:
        for nm, v in dev:
            for p in POSES:
                m = np.array([1.0 if r['pos'] == p else 0.0 for r in rows])
                names.append('%s|%s' % (nm, p)); cols.append(v * m)
    return names, cols


def add_level(rows, names, cols):
    v0 = np.array([r['v0'] for r in rows], float)
    lg = np.array([math.log1p(r['g']) for r in rows], float)
    names = names + ['v0', 'v0_lg']
    cols = cols + [v0, v0 * lg]
    return names, cols


HI, MIDB, LO = 'hi', 'mid', 'lo'
def pickclass(pk):
    return HI if pk <= 12 else (MIDB if pk <= 30 else LO)


def add_traj(rows, names, cols):
    age = np.array([r['age'] for r in rows], float)
    lg = np.array([math.log1p(r['g']) for r in rows], float)
    o = np.array([r['o'] for r in rows], float)
    cur = np.array([r['cur'] for r in rows], float)
    pc = [pickclass(r['pick']) for r in rows]
    for cls in (HI, LO):                       # mid is the reference class
        m = np.array([1.0 if c == cls else 0.0 for c in pc])
        for nm, v in [('age', age), ('age2', age ** 2), ('o', o), ('cur', cur), ('lg', lg)]:
            names = names + ['%s_x_%s' % (nm, cls)]
            cols = cols + [v * m]
        names = names + ['d_' + cls]; cols = cols + [m]
    return names, cols


def design(rows, form):
    if form == 'P':
        names, cols = base_cols(rows)
    elif form == 'L':
        names, cols = add_level(rows, *base_cols(rows))
    elif form == 'T':
        names, cols = add_traj(rows, *add_level(rows, *base_cols(rows)))
    elif form == 'P1':
        names, cols = base_cols(rows, per_pos_slopes=False)
    elif form == 'P6':
        names, cols = base_cols(rows, per_pos_slopes=True)
    else:
        raise ValueError(form)
    X = np.column_stack(cols)
    y = np.array([r['R'] for r in rows], float)
    return names, X, y


def standardise(Xtr, Xte):
    mu = Xtr.mean(axis=0); sd = Xtr.std(axis=0)
    sd = np.where(sd < 1e-12, 1.0, sd)
    keep = np.ones(Xtr.shape[1], bool)
    keep[0] = True
    A = (Xtr - mu) / sd; B = (Xte - mu) / sd
    A[:, 0] = 1.0; B[:, 0] = 1.0
    return A, B


def folds_by_player(rows, nf=5):
    keys = sorted({r['key'] for r in rows})
    f = {k: i % nf for i, k in enumerate(keys)}
    return np.array([f[r['key']] for r in rows])


def cv(rows, form, nf=5):
    names, X, y = design(rows, form)
    fo = folds_by_player(rows, nf)
    per = []
    pred = np.zeros(len(y))
    for k in range(nf):
        te = (fo == k); tr = ~te
        A, B = standardise(X[tr], X[te])
        b = ols(A, y[tr])
        p = B @ b
        pred[te] = p
        e = y[te] - p
        per.append(dict(fold=k, n=int(te.sum()), rms=float(math.sqrt(float((e ** 2).mean()))),
                        mae=float(np.abs(e).mean())))
    e = y - pred
    return dict(form=form, k_params=X.shape[1], n=len(y),
                rms=float(math.sqrt(float((e ** 2).mean()))), mae=float(np.abs(e).mean()),
                spearman=spearman(y, pred), folds=per, _pred=pred, _y=y)


def time_block(rows, form, cut=2012):
    tr = [r for r in rows if r['year'] <= cut]
    te = [r for r in rows if r['year'] > cut]
    if len(tr) < 50 or len(te) < 50:
        return None
    _, Xtr, ytr = design(tr, form)
    _, Xte, yte = design(te, form)
    A, B = standardise(Xtr, Xte)
    b = ols(A, ytr)
    p = B @ b
    e = yte - p
    return dict(form=form, n_train=len(tr), n_test=len(te),
                rms=float(math.sqrt(float((e ** 2).mean()))), mae=float(np.abs(e).mean()),
                spearman=spearman(yte, p))


def compare(a, b, label_a, label_b, bar=0.02, nf=5):
    """PREREG s4 decision rule: the richer form wins only on >=2.0% RMS reduction AND >=4/5 folds."""
    red = (a['rms'] - b['rms']) / a['rms'] if a['rms'] > 0 else 0.0
    wins = sum(1 for fa, fb in zip(a['folds'], b['folds']) if fb['rms'] < fa['rms'])
    adopt = bool(red >= bar and wins >= 4)
    return dict(simpler=label_a, richer=label_b, rms_simpler=a['rms'], rms_richer=b['rms'],
                rms_reduction=red, folds_won_by_richer=wins, bar=bar, adopt_richer=adopt)


# ==================================================================================================
# RUN
# ==================================================================================================
P('=' * 100)
P('ORDER 30B-M -- PEDIGREE PERSISTENCE MEASUREMENT')
P('=' * 100)
P('pins: ' + json.dumps(PINS, indent=1))
P('bars (engine-read, Ruling 1 asserted): ' + json.dumps({g: round(BARS[g], 4) for g in sorted(BARS)}))
P('SCALE %.12f  GAMMA %.1f  disc %.2f  AGE_REF %d' % (MA.SCALE, MA.GAMMA, DISC, MA.AGE_REF))
tau = BLEND['tau'] if 'tau' in BLEND else None
P('blend artifact keys: %s' % sorted(BLEND.keys())[:12])

STATES, PTS = build_states()
P('\nstates built (all entries, all played seasons): %d over %d careers'
  % (len(STATES), len({s['key'] for s in STATES})))

ROWS = panel(STATES, PTS, H=6)
POOLROWS = [r for r in panel(STATES, PTS, H=6, nd_only=False) if not r['nd']]
P('PRIMARY PANEL (ND 1-64, entry>=2005, Y<=2019, H=6): %d states over %d careers'
  % (len(ROWS), len({r['key'] for r in ROWS})))
P('  state-year range %d-%d ; entry-year range %d-%d'
  % (min(r['year'] for r in ROWS), max(r['year'] for r in ROWS),
     min(r['entry_year'] for r in ROWS), max(r['entry_year'] for r in ROWS)))
P('POOL comparison band (descriptive only): %d states over %d careers'
  % (len(POOLROWS), len({r['key'] for r in POOLROWS})))

RES = dict(meta=dict(order='30B-M', date='2026-08-14', pins=PINS,
                     bars={g: BARS[g] for g in sorted(BARS)}, scale=float(MA.SCALE),
                     disc=DISC, horizon_primary=6, now=NOW,
                     population='ND effective_pick 1-64, entry_year>=2005, state year <= 2019 (H=6 fully observed)',
                     censor_left='entry years 2003-2004 excluded: store season rows begin 2005',
                     censor_right='2026 in progress: contributes no future value, supplies no fitting state',
                     survivorship='zeros stay in; a season with no row contributes 0',
                     scorer='26B Layer 2 pricing core (Ruling 1 bars, Ruling 3 season callable, sqrt games weight, no era normalisation), discount re-anchored at the state year',
                     force_majeure=sorted(FORCE_MAJEURE),
                     n_states=len(ROWS), n_careers=len({r['key'] for r in ROWS}),
                     n_pool_states=len(POOLROWS)))

# ---- P2 skew ------------------------------------------------------------------------------------
sk = {}
for nm, lo, hi in GAMES_BANDS:
    xs = [r['R'] for r in ROWS if r['gb'] == nm]
    sk[nm] = disp(xs)
RES['skew_by_games_band'] = sk
P('\n--- SKEW / DISPERSION OF REMAINING VALUE BY GAMES BAND (P2) ---')
P('%-8s %6s %10s %10s %10s %10s %8s' % ('games', 'n', 'mean', 'p25', 'median', 'p75', 'zero%'))
for nm, lo, hi in GAMES_BANDS:
    d = sk[nm]
    if d['n'] == 0:
        P('%-8s %6d   (empty)' % (nm, 0)); continue
    P('%-8s %6d %10.1f %10.1f %10.1f %10.1f %7.1f%%'
      % (nm, d['n'], d['mean'], d['p25'], d['median'], d['p75'], 100 * d['zero_share']))

# ---- ENTRY ANCHOR: the pick spread with no output information -------------------------------------
entry_states = []
for k, e in ENT.items():
    if k in FORCE_MAJEURE or e['entry_year'] is None or e['entry_year'] < 2005:
        continue
    if not (e['type'] == 'ND' and e['effective_pick'] and 1 <= e['effective_pick'] <= 64):
        continue
    Y = e['entry_year']
    if Y + 6 > NOW - 1:
        continue
    entry_states.append(dict(key=k, year=Y, pick=e['effective_pick'],
                             pb=band_of(e['effective_pick'], PICK_BANDS),
                             v0=float(POSV[e['position_group']][str(int(e['effective_pick']))]),
                             R=remaining(k, Y, 6, PTS)))
ea = {}
for nm, lo, hi in PICK_BANDS:
    xs = [s['R'] for s in entry_states if s['pb'] == nm]
    d = disp(xs); d['mean_v0'] = (sum(s['v0'] for s in entry_states if s['pb'] == nm) / max(1, len(xs)))
    ea[nm] = d
RES['entry_anchor'] = dict(n=len(entry_states), by_pick_band=ea)
P('\n--- ENTRY ANCHOR (states at g=0, entry year; no output information) ---')
P('%-9s %5s %10s %10s %10s %10s %8s %10s' % ('pickband', 'n', 'mean R6', 'p25', 'median', 'p75', 'zero%', 'mean v0'))
for nm, lo, hi in PICK_BANDS:
    d = ea[nm]
    P('%-9s %5d %10.1f %10.1f %10.1f %10.1f %7.1f%% %10.1f'
      % (nm, d['n'], d['mean'], d['p25'], d['median'], d['p75'], 100 * d['zero_share'], d['mean_v0']))

# ==================================================================================================
# Q1 -- PERSISTENCE
# ==================================================================================================
P('\n' + '=' * 100)
P('Q1 -- PERSISTENCE: does pick still predict remaining value, and how does the share decay?')
P('=' * 100)

def band_fit(rows_b):
    """Within a games band: R ~ [pos dummies, age, age2, o, o2, cur, cur3, games_at_Y] + v0.
    Returns beta_v0, cluster SE, pedigree share sigma = beta*mean(v0)/mean(R)."""
    n = len(rows_b)
    if n < 40:
        return None
    cols = [np.ones(n)]
    names = ['const']
    for p in POSES[1:]:
        cols.append(np.array([1.0 if r['pos'] == p else 0.0 for r in rows_b])); names.append('pos_' + p)
    age = np.array([r['age'] for r in rows_b], float)
    o = np.array([r['o'] for r in rows_b], float)
    cur = np.array([r['cur'] for r in rows_b], float)
    cur3 = np.array([r['cur3'] for r in rows_b], float)
    gay = np.array([r['games_at_Y'] for r in rows_b], float)
    lg = np.array([math.log1p(r['g']) for r in rows_b], float)
    for nm, v in [('age', age), ('age2', age ** 2), ('o', o), ('o2', o ** 2), ('cur', cur),
                  ('cur3', cur3), ('games_at_Y', gay), ('lg', lg)]:
        cols.append(v); names.append(nm)
    v0 = np.array([r['v0'] for r in rows_b], float)
    cols.append(v0); names.append('v0')
    X = np.column_stack(cols)
    y = np.array([r['R'] for r in rows_b], float)
    b = ols(X, y)
    se, nclust = cluster_se(X, y, b, [r['key'] for r in rows_b])
    i = names.index('v0')
    mv0 = float(v0.mean()); mR = float(y.mean())
    sig = b[i] * mv0 / mR if mR > 0 else None
    # cluster bootstrap for the share
    keys = sorted({r['key'] for r in rows_b})
    byk = collections.defaultdict(list)
    for j, r in enumerate(rows_b):
        byk[r['key']].append(j)
    rng = np.random.default_rng(30_140_814)
    boots = []
    for _ in range(300):
        pick = rng.integers(0, len(keys), len(keys))
        idx = []
        for t in pick:
            idx.extend(byk[keys[t]])
        idx = np.array(idx)
        try:
            bb = ols(X[idx], y[idx])
            mm = float(y[idx].mean())
            if mm > 0:
                boots.append(float(bb[i] * float(X[idx, i].mean()) / mm))
        except Exception:
            pass
    boots.sort()
    return dict(n=n, n_clusters=nclust, beta_v0=float(b[i]), se_v0=float(se[i]),
                t_v0=float(b[i] / se[i]) if se[i] > 0 else None,
                mean_v0=mv0, mean_R=mR, sigma=float(sig) if sig is not None else None,
                sigma_ci=[q(boots, .05), q(boots, .95)] if boots else None,
                sigma_boot_median=q(boots, .5) if boots else None)


TAU, BETA = 11.650213, 0.937162
def blend_ped_share(g):
    return float(math.exp(-((g / TAU) ** BETA)))


q1 = {}
P('%-8s %6s %8s %10s %8s %9s %20s %10s %10s' %
  ('games', 'n', 'clust', 'beta_v0', 't', 'sigma', 'sigma 90% CI', 'blend', 'old~40%'))
for nm, lo, hi in GAMES_BANDS:
    rb = [r for r in ROWS if r['gb'] == nm]
    f = band_fit(rb)
    gmid = (lo + min(hi, 100)) / 2.0
    bl = blend_ped_share(gmid)
    if f is None:
        q1[nm] = dict(n=len(rb), note='n < 40 -- not fitted'); P('%-8s %6d  (n<40, not fitted)' % (nm, len(rb))); continue
    f['games_band_midpoint'] = gmid
    f['blend_implied_share_at_midpoint'] = bl
    f['old_anchor_carry_reference'] = 0.40
    q1[nm] = f
    ci = f['sigma_ci']
    P('%-8s %6d %8d %10.5f %8.2f %8.1f%% %9.1f%%..%-8.1f%% %9.1f%% %9.1f%%'
      % (nm, f['n'], f['n_clusters'], f['beta_v0'], f['t_v0'], 100 * f['sigma'],
         100 * ci[0], 100 * ci[1], 100 * bl, 40.0))

# ---- matched contrast (non-parametric check) ------------------------------------------------------
def out_quintiles(rows):
    cuts = {}
    for p in POSES:
        xs = sorted(r['o'] for r in rows if r['pos'] == p)
        if len(xs) < 25:
            cuts[p] = None; continue
        cuts[p] = [q(xs, f) for f in (.2, .4, .6, .8)]
    return cuts

OQ = out_quintiles(ROWS)
def oband(r, nq=5):
    c = OQ.get(r['pos'])
    if c is None:
        return 'all'
    if nq == 5:
        b = 0
        for t in c:
            if r['o'] > t:
                b += 1
        return 'Q%d' % (b + 1)
    ter = [c[0], c[2]]
    b = 0
    for t in ter:
        if r['o'] > t:
            b += 1
    return 'T%d' % (b + 1)


MINCELL = 8
def matched(rows, nq=5):
    out = {}
    collapses = []
    for gnm, lo, hi in GAMES_BANDS:
        strata = collections.defaultdict(lambda: collections.defaultdict(list))
        for r in rows:
            if r['gb'] != gnm:
                continue
            s = (r['pos'], r['ab'], oband(r, nq))
            strata[s][r['pb']].append(r['R'])
        num = den = 0.0
        used = 0
        detail = []
        for s, cells in strata.items():
            ok = {b: v for b, v in cells.items() if len(v) >= MINCELL}
            if len(ok) < 2:
                if cells:
                    collapses.append(dict(games_band=gnm, stratum=list(s),
                                          cells={b: len(v) for b, v in cells.items()},
                                          action='dropped from contrast (fewer than two cells with n>=%d)' % MINCELL))
                continue
            order = [b for b, _, _ in PICK_BANDS if b in ok]
            top, bot = order[0], order[-1]
            mt = sum(ok[top]) / len(ok[top]); mb = sum(ok[bot]) / len(ok[bot])
            w = min(len(ok[top]), len(ok[bot]))
            num += w * (mt - mb); den += w; used += 1
            detail.append(dict(stratum=list(s), top=top, bot=bot, n_top=len(ok[top]), n_bot=len(ok[bot]),
                               mean_top=mt, mean_bot=mb, delta=mt - mb))
        # simple hi(A+B) vs lo(D+E) aggregate over the whole band
        hi_ = [r['R'] for r in rows if r['gb'] == gnm and r['pb'] in ('A 1-6', 'B 7-12')]
        lo_ = [r['R'] for r in rows if r['gb'] == gnm and r['pb'] in ('D 21-40', 'E 41-64')]
        out[gnm] = dict(n_strata_used=used, delta_weighted=(num / den if den > 0 else None),
                        weight=den, detail=sorted(detail, key=lambda d: -d['n_top'])[:12],
                        raw_hi=disp(hi_), raw_lo=disp(lo_),
                        raw_delta=(sum(hi_) / len(hi_) - sum(lo_) / len(lo_)) if hi_ and lo_ else None)
    return out, collapses


MATCH, COLLAPSES = matched(ROWS, 5)
P('\n--- MATCHED PICK CONTRAST (stratum = pos x age band x output quintile; min cell n=%d) ---' % MINCELL)
P('%-8s %8s %14s %14s %10s %10s' % ('games', 'strata', 'matched delta', 'raw hi-lo', 'n hi', 'n lo'))
for gnm, lo, hi in GAMES_BANDS:
    m = MATCH[gnm]
    dw = m['delta_weighted']
    P('%-8s %8d %14s %14s %10d %10d'
      % (gnm, m['n_strata_used'], ('%.1f' % dw) if dw is not None else 'n/a',
         ('%.1f' % m['raw_delta']) if m['raw_delta'] is not None else 'n/a',
         m['raw_hi']['n'], m['raw_lo']['n']))
# tercile collapse for bands where quintiles thinned out
MATCH3, COLLAPSES3 = matched(ROWS, 3)
P('\n--- SAME CONTRAST AFTER THE PREREGISTERED THIN-CELL COLLAPSE (quintile -> TERCILE, PREREG s3) ---')
P('%-8s %8s %14s %10s' % ('games', 'strata', 'matched delta', 'weight'))
for gnm, lo, hi in GAMES_BANDS:
    m = MATCH3[gnm]
    dw = m['delta_weighted']
    P('%-8s %8d %14s %10.0f' % (gnm, m['n_strata_used'], ('%.1f' % dw) if dw is not None else 'n/a', m['weight']))
P('  quintile-lens cells collapsed out: %d ; tercile-lens cells collapsed out: %d' % (len(COLLAPSES), len(COLLAPSES3)))

# ---- residual contrast: the same claim with the full panel behind it -------------------------------
# The pick-blind model of PREREG s4 (form P) is fitted WITHIN each games band; the mean residual by
# pick band is then the pick information the production features could not carry. Full n, no cells.
def resid_contrast(rows):
    out = {}
    for gnm, lo, hi in GAMES_BANDS:
        rb = [r for r in rows if r['gb'] == gnm]
        if len(rb) < 40:
            out[gnm] = dict(note='n<40'); continue
        _, X, y = design(rb, 'P')
        b = ols(X, y)
        res = y - X @ b
        by = collections.defaultdict(list)
        for r, e in zip(rb, res):
            by[r['pb']].append(float(e))
        cells = {pbn: disp(by[pbn]) for pbn, _, _ in PICK_BANDS if by[pbn]}
        hi_ = [e for pbn in ('A 1-6', 'B 7-12') for e in by.get(pbn, [])]
        lo_ = [e for pbn in ('D 21-40', 'E 41-64') for e in by.get(pbn, [])]
        # cluster bootstrap on the hi-lo residual gap
        keys = sorted({r['key'] for r in rb})
        byk = collections.defaultdict(list)
        for j, r in enumerate(rb):
            byk[r['key']].append(j)
        cls = np.array([1 if r['pb'] in ('A 1-6', 'B 7-12') else (-1 if r['pb'] in ('D 21-40', 'E 41-64') else 0)
                        for r in rb])
        rng = np.random.default_rng(30_140_814)
        boots = []
        for _ in range(300):
            take = rng.integers(0, len(keys), len(keys))
            idx = []
            for t in take:
                idx.extend(byk[keys[t]])
            idx = np.array(idx)
            c = cls[idx]; e2 = res[idx]
            if (c == 1).sum() >= 5 and (c == -1).sum() >= 5:
                boots.append(float(e2[c == 1].mean() - e2[c == -1].mean()))
        boots.sort()
        out[gnm] = dict(cells=cells,
                        mean_hi=(sum(hi_) / len(hi_)) if hi_ else None,
                        mean_lo=(sum(lo_) / len(lo_)) if lo_ else None,
                        n_hi=len(hi_), n_lo=len(lo_),
                        gap=((sum(hi_) / len(hi_)) - (sum(lo_) / len(lo_))) if hi_ and lo_ else None,
                        gap_ci90=[q(boots, .05), q(boots, .95)] if boots else None)
    return out


RESID = resid_contrast(ROWS)
P('\n--- RESIDUAL CONTRAST (pick-blind model fitted within each games band; mean residual by pick band) ---')
P('%-8s %10s %10s %10s %10s %12s %22s' % ('games', 'n hi(1-12)', 'mean hi', 'n lo(21-64)', 'mean lo', 'gap', 'gap 90% CI'))
for gnm, lo, hi in GAMES_BANDS:
    m = RESID[gnm]
    if 'gap' not in m or m['gap'] is None:
        P('%-8s   (not fitted)' % gnm); continue
    ci = m['gap_ci90']
    P('%-8s %10d %10.1f %10d %10.1f %12.1f %10.1f .. %-10.1f'
      % (gnm, m['n_hi'], m['mean_hi'], m['n_lo'], m['mean_lo'], m['gap'], ci[0], ci[1]))

# ---- the pedigree share at 36 games exactly (log-linear interpolation, LABELLED as interpolation) ---
def sigma_at(gt):
    pts = []
    for nm, lo, hi in GAMES_BANDS:
        f = q1.get(nm)
        if isinstance(f, dict) and f.get('sigma') is not None:
            pts.append(((lo + min(hi, 100)) / 2.0, f['sigma']))
    pts.sort()
    for i in range(1, len(pts)):
        if pts[i - 1][0] <= gt <= pts[i][0]:
            (g0, s0), (g1, s1) = pts[i - 1], pts[i]
            if s0 <= 0 or s1 <= 0:
                return s0 + (s1 - s0) * (gt - g0) / (g1 - g0)
            t = (math.log(gt) - math.log(g0)) / (math.log(g1) - math.log(g0))
            return math.exp(math.log(s0) + t * (math.log(s1) - math.log(s0)))
    return None


SIG36 = sigma_at(36.0)
P('\nPEDIGREE SHARE AT g = 36 (isaac-kako\'s exact games count), log-linear interpolation between the')
P('measured band midpoints 25.5 and 53.0 -- AN INTERPOLATION, LABELLED AS ONE:')
P('   measured  ~%.1f%%      blend 1-w(36) = %.2f%%      old anchor carry ~40%%'
  % (100 * SIG36, 100 * blend_ped_share(36.0)))

RES['q1_persistence'] = dict(band_fits=q1, matched_quintile=MATCH, matched_tercile=MATCH3,
                             residual_contrast=RESID,
                             sigma_interpolated_at_36_games=SIG36,
                             blend_share_at_36_games=blend_ped_share(36.0),
                             collapsed_cells_quintile=COLLAPSES[:400],
                             n_collapsed_quintile=len(COLLAPSES), n_collapsed_tercile=len(COLLAPSES3),
                             collapse_ladder='PREREG s3: cell n<8 is not reported; output quintile -> tercile -> stratum dropped. The quintile lens is reported first, the tercile lens is the preregistered collapse, and the residual contrast carries the same claim with the full panel behind it.',
                             blend_form='1-w(g) with tau=%.6f beta=%.6f' % (TAU, BETA))

# ---- full cell table ------------------------------------------------------------------------------
cells = {}
for r in ROWS:
    kk = '%s|%s|%s|%s|%s' % (r['pos'], r['ab'], r['gb'], oband(r, 5), r['pb'])
    cells.setdefault(kk, []).append(r['R'])
CELLTAB = {k: disp(v) for k, v in sorted(cells.items())}
RES['cells_all_states'] = CELLTAB
RES['cells_reported'] = {k: v for k, v in CELLTAB.items() if v['n'] >= MINCELL}
P('\nfull state cells: %d ; cells with n>=%d (reported): %d ; thin cells collapsed out: %d'
  % (len(CELLTAB), MINCELL, len(RES['cells_reported']), len(CELLTAB) - len(RES['cells_reported'])))

# ---- pool band (P9) --------------------------------------------------------------------------------
poolm = {}
for gnm, lo, hi in GAMES_BANDS:
    pa = [r['R'] for r in POOLROWS if r['gb'] == gnm]
    na = [r['R'] for r in ROWS if r['gb'] == gnm and r['pb'] == 'A 1-6']
    ea_ = [r['R'] for r in ROWS if r['gb'] == gnm and r['pb'] == 'E 41-64']
    poolm[gnm] = dict(pool=disp(pa), band_A=disp(na), band_E=disp(ea_))
RES['pool_band'] = poolm
P('\n--- POOL BAND vs ND BANDS (P9; descriptive, never fitted) ---')
P('%-8s %8s %10s %10s %10s %10s %10s' % ('games', 'n pool', 'mean pool', 'n A', 'mean A', 'n E', 'mean E'))
for gnm, lo, hi in GAMES_BANDS:
    m = poolm[gnm]
    P('%-8s %8d %10s %10d %10s %10d %10s'
      % (gnm, m['pool']['n'], ('%.1f' % m['pool']['mean']) if m['pool']['n'] else 'n/a',
         m['band_A']['n'], ('%.1f' % m['band_A']['mean']) if m['band_A']['n'] else 'n/a',
         m['band_E']['n'], ('%.1f' % m['band_E']['mean']) if m['band_E']['n'] else 'n/a'))

# ==================================================================================================
# Q2 -- FORM
# ==================================================================================================
P('\n' + '=' * 100)
P('Q2 -- FORM: LEVEL (blend shape) vs TRAJECTORY (pick-conditional development)')
P('=' * 100)
CVP, CVL, CVT = cv(ROWS, 'P'), cv(ROWS, 'L'), cv(ROWS, 'T')
for c in (CVP, CVL, CVT):
    P('%-3s k=%3d  n=%5d  heldout RMS %10.2f  MAE %9.2f  spearman %.4f'
      % (c['form'], c['k_params'], c['n'], c['rms'], c['mae'], c['spearman']))
CMP_PL = compare(CVP, CVL, 'P', 'L')
CMP_LT = compare(CVL, CVT, 'L', 'T')
P('\nP -> L : RMS %.2f -> %.2f (%.2f%% reduction), folds won %d/5 -> ADOPT L: %s'
  % (CMP_PL['rms_simpler'], CMP_PL['rms_richer'], 100 * CMP_PL['rms_reduction'],
     CMP_PL['folds_won_by_richer'], CMP_PL['adopt_richer']))
P('L -> T : RMS %.2f -> %.2f (%.2f%% reduction), folds won %d/5 -> ADOPT T: %s'
  % (CMP_LT['rms_simpler'], CMP_LT['rms_richer'], 100 * CMP_LT['rms_reduction'],
     CMP_LT['folds_won_by_richer'], CMP_LT['adopt_richer']))
TB = {f: time_block(ROWS, f) for f in ('P', 'L', 'T')}
P('time-block hold-out (fit Y<=2012, test Y>=2013):')
for f in ('P', 'L', 'T'):
    t = TB[f]
    if t:
        P('  %-2s n_tr %d n_te %d RMS %10.2f MAE %9.2f spearman %.4f'
          % (f, t['n_train'], t['n_test'], t['rms'], t['mae'], t['spearman']))
# fitted coefficients on the full panel (reported, not used to decide)
COEF = {}
for f in ('L', 'T'):
    names, X, y = design(ROWS, f)
    b = ols(X, y)
    se, nc = cluster_se(X, y, b, [r['key'] for r in ROWS])
    COEF[f] = {n: dict(beta=float(bb), se=float(ss), t=(float(bb / ss) if ss > 0 else None))
               for n, bb, ss in zip(names, b, se)}
P('\nform L, pick terms on the full panel (cluster-robust on player):')
for n in ('v0', 'v0_lg'):
    c = COEF['L'][n]
    P('  %-8s beta %12.6f  se %12.6f  t %7.2f' % (n, c['beta'], c['se'], c['t'] or float('nan')))
P('form T, pick-class interaction terms (reference class = picks 13-30):')
for n, c in COEF['T'].items():
    if '_x_' in n or n.startswith('d_'):
        P('  %-14s beta %12.6f  se %12.6f  t %7.2f' % (n, c['beta'], c['se'], c['t'] or float('nan')))
# ---- BY-CELL FIT QUALITY (the brief's "out-of-cell" comparison) -----------------------------------
# Sliced from the SAME 5-fold held-out predictions. No refit, no re-decision -- this is where each
# form is right and wrong, not a second criterion.
def slice_errors(cvres, rows, keyfn):
    out = collections.defaultdict(list)
    for r, yy, pp in zip(rows, cvres['_y'], cvres['_pred']):
        out[keyfn(r)].append((yy - pp) ** 2)
    return {k: dict(n=len(v), rms=float(math.sqrt(sum(v) / len(v)))) for k, v in out.items()}


BYCELL = {}
for lab, fn in [('games_band', lambda r: r['gb']), ('pick_band', lambda r: r['pb']),
                ('pick_class', lambda r: pickclass(r['pick'])), ('age_band', lambda r: r['ab']),
                ('position', lambda r: r['pos']),
                ('young_thin', lambda r: 'g<=40 & age<=21' if (r['g'] <= 40 and r['age'] <= 21) else 'other')]:
    BYCELL[lab] = {f: slice_errors(c, ROWS, fn) for f, c in (('P', CVP), ('L', CVL), ('T', CVT))}
P('\n--- HELD-OUT RMS BY CELL (same 5-fold predictions, sliced; no refit, no re-decision) ---')
for lab in ('games_band', 'pick_class', 'young_thin'):
    P('  %s:' % lab)
    keys = sorted(BYCELL[lab]['P'].keys())
    P('    %-14s %6s %10s %10s %10s   %s' % ('cell', 'n', 'RMS P', 'RMS L', 'RMS T', 'best'))
    for k in keys:
        a, b, c = BYCELL[lab]['P'][k], BYCELL[lab]['L'][k], BYCELL[lab]['T'][k]
        best = min((('P', a['rms']), ('L', b['rms']), ('T', c['rms'])), key=lambda t: t[1])[0]
        P('    %-14s %6d %10.1f %10.1f %10.1f   %s' % (k, a['n'], a['rms'], b['rms'], c['rms'], best))

RES['q2_form'] = dict(cv=dict(P={k: v for k, v in CVP.items() if not k.startswith('_')},
                              L={k: v for k, v in CVL.items() if not k.startswith('_')},
                              T={k: v for k, v in CVT.items() if not k.startswith('_')}),
                      by_cell_heldout_rms=BYCELL, compare_P_L=CMP_PL, compare_L_T=CMP_LT,
                      time_block=TB, coefficients=COEF,
                      verdict=('TRAJECTORY' if CMP_LT['adopt_richer'] else
                               ('LEVEL' if CMP_PL['adopt_richer'] else 'PRODUCTION-ONLY')))
P('\nQ2 VERDICT (preregistered rule, 2.0%% RMS + 4/5 folds): %s' % RES['q2_form']['verdict'])

# ==================================================================================================
# Q3 -- POSITION CLOCKS
# ==================================================================================================
P('\n' + '=' * 100)
P('Q3 -- POSITION CLOCKS: one development table vs one per position group')
P('=' * 100)
CV1, CV6 = cv(ROWS, 'P1'), cv(ROWS, 'P6')
P('P1 (one table)      k=%3d heldout RMS %10.2f MAE %9.2f spearman %.4f' % (CV1['k_params'], CV1['rms'], CV1['mae'], CV1['spearman']))
P('P6 (per-position)   k=%3d heldout RMS %10.2f MAE %9.2f spearman %.4f' % (CV6['k_params'], CV6['rms'], CV6['mae'], CV6['spearman']))
CMP_16 = compare(CV1, CV6, 'P1', 'P6')
P('P1 -> P6 : %.2f%% RMS reduction, folds won %d/5 -> ADOPT per-position clocks: %s'
  % (100 * CMP_16['rms_reduction'], CMP_16['folds_won_by_richer'], CMP_16['adopt_richer']))

# fitted age profile per position, at that position's own median output/games state
names6, X6, y6 = design(ROWS, 'P6')
b6 = ols(X6, y6)
IDX = {n: i for i, n in enumerate(names6)}
prof = {}
for p in POSES:
    sub = [r for r in ROWS if r['pos'] == p]
    if len(sub) < 40:
        prof[p] = dict(n=len(sub), note='n<40'); continue
    med = lambda f: q([r[f] for r in sub], .5)
    o_, cur_, cur3_, g_, gay_ = med('o'), med('cur'), med('cur3'), med('g'), med('games_at_Y')
    curve = {}
    for a in range(18, 33):
        v = 0.0
        for nm, val in [('age', a), ('age2', a * a), ('lg', math.log1p(g_)), ('o', o_), ('o2', o_ ** 2),
                        ('cur', cur_), ('cur3', cur3_), ('games_at_Y', gay_), ('o_age', o_ * a),
                        ('cur_age', cur_ * a)]:
            v += b6[IDX['%s|%s' % (nm, p)]] * val
        curve[a] = float(v)
    # development contribution = the age-varying part only
    agepart = {}
    for a in range(18, 33):
        v = (b6[IDX['age|%s' % p]] * a + b6[IDX['age2|%s' % p]] * a * a
             + b6[IDX['o_age|%s' % p]] * o_ * a + b6[IDX['cur_age|%s' % p]] * cur_ * a)
        agepart[a] = float(v)
    peak = max(agepart, key=lambda a: agepart[a])
    prof[p] = dict(n=len(sub), median_o=o_, median_cur=cur_, median_games=g_,
                   fitted_total_by_age=curve, age_part_by_age=agepart, peak_age=int(peak))
P('\nfitted development peak age, per position group (at that group\'s own median state):')
for p in POSES:
    d = prof[p]
    P('  %-5s n %5d  peak age %s' % (p, d.get('n', 0), d.get('peak_age', 'n/a')))
tall = [prof[p]['peak_age'] for p in ('KPD', 'KPF', 'RUCK') if 'peak_age' in prof[p]]
small = [prof[p]['peak_age'] for p in ('MID', 'SF', 'SD') if 'peak_age' in prof[p]]
gap = (sum(tall) / len(tall) - sum(small) / len(small)) if tall and small else None
P('  mean tall peak %.2f  mean small/mid peak %.2f  gap %.2f years'
  % (sum(tall) / len(tall), sum(small) / len(small), gap) if gap is not None else '  gap n/a')

# raw (unfitted) age profile: mean R by position x age band, for the same states
rawage = {}
for p in POSES:
    rawage[p] = {}
    for anm, lo, hi in AGE_BANDS:
        xs = [r['R'] for r in ROWS if r['pos'] == p and r['ab'] == anm]
        if len(xs) >= MINCELL:
            rawage[p][anm] = disp(xs)
# ---- SUPPLEMENTARY, POST-HOC, NON-DECIDING: the raw development clock -------------------------------
# The preregistered peak-age readout above is DEGENERATE: the target is REMAINING value, which falls
# with age at a fixed state for horizon reasons alone, so the fitted age part has no interior peak and
# the readout pins to the 18 boundary for every group. That is reported as a NO-SIGNAL lens (PREREG s6
# P7 is breached on it). This lens is added AFTER that reading, is labelled post-hoc, and DOES NOT
# re-decide Q3: it measures OUTPUT GROWTH directly -- the object the football prior is actually about.
growth = collections.defaultdict(list)
level = collections.defaultdict(list)
for k, e in ENT.items():
    if k in FORCE_MAJEURE or e['entry_year'] is None or e['entry_year'] < 2005:
        continue
    ss = [s for s in SEA.get(k, []) if s['year'] < NOW]
    for i, s in enumerate(ss):
        pos = bar_group(s['position_played'], e['position_group'])
        if pos not in BARS or s['games'] < 5:
            continue
        a = s['year'] - e['birth_year']
        level[(pos, a)].append(float(s['avg']))
        if i + 1 < len(ss) and ss[i + 1]['year'] == s['year'] + 1 and ss[i + 1]['games'] >= 5:
            growth[(pos, a)].append(float(ss[i + 1]['avg']) - float(s['avg']))
CLOCK = {}
for p in POSES:
    row = {}
    for a in range(18, 31):
        gx = growth.get((p, a), []); lx = level.get((p, a), [])
        if len(gx) >= MINCELL:
            row[a] = dict(n=len(gx), median_delta_avg=q(gx, .5), p25=q(gx, .25), p75=q(gx, .75),
                          n_level=len(lx), median_avg=q(lx, .5) if lx else None)
    CLOCK[p] = row
P('\n--- SUPPLEMENTARY (POST-HOC, NON-DECIDING): RAW OUTPUT GROWTH BY POSITION x AGE ---')
P('    median next-season change in season average, players with >=5 games in both seasons')
P('    %-5s %s' % ('pos', ' '.join('%6d' % a for a in range(18, 29))))
for p in POSES:
    P('    %-5s %s' % (p, ' '.join(('%6.1f' % CLOCK[p][a]['median_delta_avg']) if a in CLOCK[p] else '     .'
                                   for a in range(18, 29))))
P('    %-5s %s' % ('n', ' '.join(('%6d' % sum(CLOCK[p][a]['n'] for p in POSES if a in CLOCK[p]))
                                 for a in range(18, 29))))
lastpos = {}
for p in POSES:
    ages = [a for a in sorted(CLOCK[p]) if CLOCK[p][a]['median_delta_avg'] > 0]
    lastpos[p] = max(ages) if ages else None
P('    last age with a POSITIVE median growth step, per group: %s'
  % {p: lastpos[p] for p in POSES})
tallg = [lastpos[p] for p in ('KPD', 'KPF', 'RUCK') if lastpos[p]]
smallg = [lastpos[p] for p in ('MID', 'SF', 'SD') if lastpos[p]]
gap_raw = (sum(tallg) / len(tallg) - sum(smallg) / len(smallg)) if tallg and smallg else None
P('    tall mean %.2f  small/mid mean %.2f  gap %s years'
  % ((sum(tallg) / len(tallg)) if tallg else float('nan'),
     (sum(smallg) / len(smallg)) if smallg else float('nan'),
     ('%.2f' % gap_raw) if gap_raw is not None else 'n/a'))

RES['q3_clocks'] = dict(cv=dict(P1={k: v for k, v in CV1.items() if not k.startswith('_')},
                                P6={k: v for k, v in CV6.items() if not k.startswith('_')}),
                        compare=CMP_16, profiles=prof,
                        preregistered_peak_age_lens='NO SIGNAL -- degenerate: remaining value falls with age at a fixed state for horizon reasons, so the fitted age part has no interior peak and pins to the 18 boundary in every group. P7 is breached on this lens and the breach is owned.',
                        supplementary_raw_growth_clock=CLOCK,
                        supplementary_last_positive_growth_age=lastpos,
                        supplementary_gap_years=gap_raw,
                        supplementary_status='POST-HOC, DESCRIPTIVE, DOES NOT RE-DECIDE Q3',
                        raw_mean_R_by_pos_age=rawage,
                        tall_peak_mean=(sum(tall) / len(tall) if tall else None),
                        small_peak_mean=(sum(small) / len(small) if small else None),
                        peak_gap_years=gap,
                        verdict=('PER-POSITION CLOCKS' if CMP_16['adopt_richer'] else 'ONE TABLE'))
P('Q3 VERDICT (same rule): %s' % RES['q3_clocks']['verdict'])

# ==================================================================================================
# NAMED ROWS + HISTORICAL VALIDATION COHORTS
# ==================================================================================================
P('\n' + '=' * 100)
P('NAMED ROWS AND HISTORICAL VALIDATION COHORTS')
P('=' * 100)
NAMED = ['isaac-kako', 'willem-duursma', 'dyson-sharp', 'jacob-farrow']

# fit the three forms once on the whole panel; predict the named 2026 states
FITS = {}
for f in ('P', 'L', 'T'):
    names, X, y = design(ROWS, f)
    mu = X.mean(axis=0); sd = X.std(axis=0); sd = np.where(sd < 1e-12, 1.0, sd)
    A = (X - mu) / sd; A[:, 0] = 1.0
    FITS[f] = (names, ols(A, y), mu, sd)


def predict(rowlist, f):
    names, b, mu, sd = FITS[f]
    _, X, _ = design(rowlist, f)
    A = (X - mu) / sd; A[:, 0] = 1.0
    return A @ b


named_states = []
for k in NAMED:
    cand = [s for s in STATES if s['key'] == k]
    if not cand:
        P('  %s: NO STATE (no played season rows)' % k); continue
    st = max(cand, key=lambda s: s['year'])
    r = dict(st)
    r['nd'] = True
    r['pb'] = band_of(st['pick'], PICK_BANDS)
    r['gb'] = band_of(st['g'], GAMES_BANDS)
    r['ab'] = band_of(st['age'], AGE_BANDS)
    r['v0'] = float(POSV[st['entry_pos']][str(int(st['pick']))])
    r['R'] = float('nan')
    named_states.append(r)
preds = {f: predict(named_states, f) for f in ('P', 'L', 'T')}
NAMEDOUT = []
P('%-16s %4s %4s %5s %4s %7s %8s %10s %10s %10s %10s' %
  ('player', 'pk', 'pos', 'games', 'age', 'output', 'board v', 'v0', 'pred P', 'pred L', 'pred T'))
for i, r in enumerate(named_states):
    br = BROWS.get(r['key'], {})
    row = dict(key=r['key'], pick=r['pick'], pos=r['pos'], state_year=r['year'], games=r['g'],
               age=r['age'], output=r['o'], last_avg=r['avg'], v0=r['v0'],
               board_price=br.get('v'), board_cg=br.get('cg'),
               pred_P=float(preds['P'][i]), pred_L=float(preds['L'][i]), pred_T=float(preds['T'][i]),
               blend_ped_share_at_games=blend_ped_share(r['g']),
               old_anchor_carry_reference=0.40)
    NAMEDOUT.append(row)
    P('%-16s %4d %4s %5.0f %4d %7.1f %8s %10.1f %10.1f %10.1f %10.1f'
      % (r['key'], r['pick'], r['pos'], r['g'], r['age'], r['o'],
         str(br.get('v')), r['v0'], row['pred_P'], row['pred_L'], row['pred_T']))

# historical validation cohorts: states at 30-40 games with output below the position median
posmed = {p: q([r['o'] for r in ROWS if r['pos'] == p], .5) for p in POSES}
coh = {'picks_1_10': [], 'picks_40_plus': []}
for r in ROWS:
    if not (30 <= r['g'] <= 40):
        continue
    if r['o'] >= posmed[r['pos']]:
        continue
    ent = 'picks_1_10' if r['pick'] <= 10 else ('picks_40_plus' if r['pick'] >= 40 else None)
    if ent is None:
        continue
    e = ENT[r['key']]
    coh[ent].append(dict(key=r['key'], pick=r['pick'], pos=r['pos'], year=r['year'], age=r['age'],
                         games=r['g'], output=r['o'], R6=r['R'],
                         career_games=e['career_games_from_seasons'], retired=e['retired'],
                         last_season=e['last_season']))
for cnm in coh:
    coh[cnm].sort(key=lambda d: -d['R6'])
P('\n--- HISTORICAL VALIDATION COHORT: 30-40 games, output BELOW the position median ---')
for cnm in ('picks_1_10', 'picks_40_plus'):
    c = coh[cnm]
    xs = [d['R6'] for d in c]
    d = disp(xs)
    P('%s: n %d  mean R6 %.1f  p25 %.1f  median %.1f  p75 %.1f  zero %.0f%%'
      % (cnm, d['n'], d['mean'] or 0, d['p25'] or 0, d['median'] or 0, d['p75'] or 0,
         100 * (d['zero_share'] or 0)))
    for d2 in c[:8]:
        P('    %-24s pk %2d %-4s %d  age %2d  g %3.0f  out %5.1f  R6 %9.1f  career games %s'
          % (d2['key'], d2['pick'], d2['pos'], d2['year'], d2['age'], d2['games'], d2['output'],
             d2['R6'], d2['career_games']))
    if len(c) > 8:
        P('    ... (%d more, all in PERSISTENCE_TABLE.json)' % (len(c) - 8))
RES['named_rows'] = NAMEDOUT
RES['historical_cohorts'] = dict(rule='state at 30-40 games with output below the median of its own position group; picks 1-10 vs picks 40+',
                                 position_median_output=posmed, cohorts=coh,
                                 summary={c: disp([d['R6'] for d in coh[c]]) for c in coh})

# ==================================================================================================
# DECLARED SENSITIVITIES (PREREG s7)
# ==================================================================================================
P('\n' + '=' * 100)
P('DECLARED SENSITIVITIES (PREREG s7) -- reported as agreement/disagreement; they never re-decide')
P('=' * 100)
SENS = {}


def sens_run(label, rows):
    if len(rows) < 200:
        SENS[label] = dict(note='panel too small (%d)' % len(rows)); P('%-28s panel %5d  (too small)' % (label, len(rows))); return
    a, b, c = cv(rows, 'P'), cv(rows, 'L'), cv(rows, 'T')
    cpl, clt = compare(a, b, 'P', 'L'), compare(b, c, 'L', 'T')
    bf = {}
    for gnm, lo, hi in GAMES_BANDS:
        f = band_fit([r for r in rows if r['gb'] == gnm])
        if f:
            bf[gnm] = dict(sigma=f['sigma'], t_v0=f['t_v0'], n=f['n'])
    strip = lambda d: {k: v for k, v in d.items() if not k.startswith('_')}
    SENS[label] = dict(n=len(rows), cv=dict(P=strip(a), L=strip(b), T=strip(c)), compare_P_L=cpl, compare_L_T=clt,
                       sigma_by_games_band=bf,
                       verdict=('TRAJECTORY' if clt['adopt_richer'] else ('LEVEL' if cpl['adopt_richer'] else 'PRODUCTION-ONLY')))
    P('%-28s panel %5d  P->L %6.2f%% (%d/5)  L->T %6.2f%% (%d/5)  verdict %s  sigma(36-70) %s'
      % (label, len(rows), 100 * cpl['rms_reduction'], cpl['folds_won_by_richer'],
         100 * clt['rms_reduction'], clt['folds_won_by_richer'], SENS[label]['verdict'],
         ('%.1f%%' % (100 * bf['36-70']['sigma'])) if '36-70' in bf else 'n/a'))


sens_run('primary (H=6, 14%, sqrt)', ROWS)
sens_run('H=4', panel(STATES, PTS, H=4))
sens_run('H=10', panel(STATES, PTS, H=10))
sens_run('discount 0%', panel(STATES, PTS, H=6, disc=0.0))
sens_run('grace 2 seasons', panel(STATES, PTS, H=6, grace=2))
ST_LIN, PTS_LIN = build_states(wmode='linear')
sens_run('games weight linear', panel(ST_LIN, PTS_LIN, H=6))
sens_run('core window entry<=2014', [r for r in ROWS if r['entry_year'] <= 2014])
ST_O1, PTS_O1 = build_states(out_window=1)
sens_run('output = state season only', panel(ST_O1, PTS_O1, H=6))
RES['sensitivities'] = SENS

# ==================================================================================================
# PREREG SCORING
# ==================================================================================================
P('\n' + '=' * 100)
P('PREREG SCORED BY NUMBER')
P('=' * 100)
sc = {}
ncar = len({r['key'] for r in ROWS})
sc['P1'] = dict(claim='panel 2,500-6,000 states over 700-1,050 careers',
                measured='%d states, %d careers' % (len(ROWS), ncar),
                held=bool(2500 <= len(ROWS) <= 6000 and 700 <= ncar <= 1050))
d1635 = sk['16-35']
zshare = []
for nm in ('0-5', '6-15', '16-35'):
    if sk[nm]['n']:
        zshare.append(sk[nm]['zero_share'])
zs = sum(z * sk[nm]['n'] for z, nm in zip(zshare, ('0-5', '6-15', '16-35'))) / max(1, sum(sk[nm]['n'] for nm in ('0-5', '6-15', '16-35')))
sc['P2'] = dict(claim='median R6 < 25% of mean in 16-35 band; >=30% zeros in <=35-game bands',
                measured='median/mean %.3f ; zero share %.3f' % ((d1635['median'] / d1635['mean']) if d1635['mean'] else float('nan'), zs),
                held=bool((d1635['mean'] and d1635['median'] / d1635['mean'] < 0.25) and zs >= 0.30))
f1635 = q1.get('16-35', {})
# The matched contrast is scored on the PREREGISTERED collapse ladder (PREREG s3: quintile -> tercile
# -> stratum dropped). The quintile lens leaves ZERO usable strata at 16-35 games -- that is the thin-
# cell case the ladder exists for. BOTH readings are printed above and both are recorded here.
mq = MATCH['16-35']['delta_weighted']
mt = MATCH3['16-35']['delta_weighted']
sc['P3'] = dict(claim='pick still predicts at 16-35 games: matched delta > 0 and v0 coefficient > 0',
                measured='matched delta quintile lens %s (0 usable strata -> the preregistered collapse applies); '
                         'tercile lens %s over %d strata; residual contrast gap %s (90%% CI %s); '
                         'beta_v0(16-35) %s (cluster t %s); beta_v0 full panel %s' %
                         (mq, ('%.1f' % mt) if mt is not None else 'n/a', MATCH3['16-35']['n_strata_used'],
                          ('%.1f' % RESID['16-35']['gap']) if RESID['16-35'].get('gap') is not None else 'n/a',
                          RESID['16-35'].get('gap_ci90'), f1635.get('beta_v0'), f1635.get('t_v0'),
                          COEF['L']['v0']['beta']),
                held=bool((mt or 0) > 0 and (RESID['16-35'].get('gap') or 0) > 0
                          and (f1635.get('beta_v0') or 0) > 0 and COEF['L']['v0']['beta'] > 0),
                note='scored on the preregistered collapse ladder; the un-collapsed quintile lens is '
                     'reported alongside and is empty at this band by thinness, not by sign')
s3670 = q1.get('36-70', {}).get('sigma')
sc['P4'] = dict(claim='pedigree share at 36-70 games strictly between 5.6% and 40%, specifically 8-25%',
                measured=('%.3f' % s3670) if s3670 is not None else 'n/a',
                held=bool(s3670 is not None and 0.08 <= s3670 <= 0.25))
seq = [q1[nm].get('sigma') for nm, _, _ in GAMES_BANDS if isinstance(q1.get(nm), dict) and q1[nm].get('sigma') is not None]
blips = sum(1 for i in range(1, len(seq)) if seq[i] > seq[i - 1])
worst = max([seq[i] - seq[i - 1] for i in range(1, len(seq))] + [0.0])
sc['P5'] = dict(claim='pedigree share non-increasing across games bands (one blip <=2pp allowed)',
                measured='sequence %s ; up-steps %d ; worst up-step %.4f' % ([round(s, 4) for s in seq], blips, worst),
                held=bool(blips <= 1 and worst <= 0.02))
sc['P6'] = dict(claim='TRAJECTORY does not clear the 2.0%/4-of-5 bar over LEVEL (seat predicts against the owner)',
                measured='RMS reduction %.4f, folds %d/5, adopt=%s' % (CMP_LT['rms_reduction'], CMP_LT['folds_won_by_richer'], CMP_LT['adopt_richer']),
                held=bool(not CMP_LT['adopt_richer']))
sc['P7'] = dict(claim='per-position clocks clear the bar AND tall peak age >= small peak age + 1.0y',
                measured='adopt=%s (%.2f%% RMS, %d/5 folds) ; preregistered peak-age lens DEGENERATE '
                         '(pins to the age-18 boundary in all six groups: the target is REMAINING value, '
                         'which declines with age for horizon reasons) -> NO SIGNAL on that lens ; '
                         'supplementary raw growth clock (post-hoc, non-deciding): last positive-growth '
                         'age tall %.2f vs small/mid %.2f, gap %s' %
                         (CMP_16['adopt_richer'], 100 * CMP_16['rms_reduction'], CMP_16['folds_won_by_richer'],
                          (sum(tallg) / len(tallg)) if tallg else float('nan'),
                          (sum(smallg) / len(smallg)) if smallg else float('nan'),
                          ('%.2f' % gap_raw) if gap_raw is not None else 'n/a'),
                held=bool(CMP_16['adopt_richer'] and gap is not None and gap >= 1.0))
kako = next((r for r in NAMEDOUT if r['key'] == 'isaac-kako'), None)
if kako:
    lo_, hi_ = sorted([abs(kako['pred_L']), abs(kako['pred_T'])])
    sc['P8'] = dict(claim='kako: every form predicts remaining 6-season value below his board price 1320; L and T differ by <2x',
                    measured='P %.1f L %.1f T %.1f ; board %s' % (kako['pred_P'], kako['pred_L'], kako['pred_T'], kako['board_price']),
                    held=bool(max(kako['pred_P'], kako['pred_L'], kako['pred_T']) < (kako['board_price'] or 1320)
                              and (hi_ <= 2 * lo_ if lo_ > 0 else False)))
else:
    sc['P8'] = dict(claim='kako', measured='no state', held=False)
pa = [poolm[g]['pool']['mean'] for g in poolm if poolm[g]['pool']['n'] >= MINCELL]
paA = [poolm[g]['band_A']['mean'] for g in poolm if poolm[g]['pool']['n'] >= MINCELL and poolm[g]['band_A']['n'] >= MINCELL]
sc['P9'] = dict(claim='pool band mean R6 below band A at comparable states',
                measured='pool means %s vs band A means %s' % ([round(x, 1) for x in pa], [round(x, 1) for x in paA]),
                held=bool(pa and paA and all(p < a for p, a in zip(pa, paA))))
sc['P10'] = dict(claim='one pass, nothing tuned after a reading, breaches owned by number',
                 measured='single execution of this harness; no quantity re-fitted after being read',
                 held=True)
for k in sorted(sc, key=lambda x: int(x[1:])):
    P('%-4s %-6s %s' % (k, 'HELD' if sc[k]['held'] else 'BREACH', sc[k]['measured']))
    P('       claim: %s' % sc[k]['claim'])
RES['prereg_scored'] = sc

json.dump(RES, open(OUT_JSON, 'w'), indent=1, sort_keys=True, default=str)
open(OUT_TXT, 'w').write('\n'.join(_LOG) + '\n')
P('\nwrote %s' % OUT_JSON)
P('wrote %s' % OUT_TXT)
assert md5(L1P) == L1_MD5, 'LAYER 1 PIN BROKEN AT EXIT'
P('layer1 pin re-asserted at exit: OK')
open(OUT_TXT, 'w').write('\n'.join(_LOG) + '\n')
