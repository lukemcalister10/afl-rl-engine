#!/usr/bin/env python3
"""ORDER 33 SEAT W4 -- STEP 1: the trajectory panel build + census.

READ-ONLY. The engine is loaded from a staged copy purely for its scorer callables (bars, posval,
capt_prem, SCALE, _collapse_elig) -- exactly the o30bm staging convention. No engine file, board,
curve, config or law is written. Definitions per PREREG_W4.md (committed & pushed before this ran).

Writes W4_PANEL.json + CENSUS_W4_out.txt into this directory. No outcome REGRESSION is run here;
the panel rows carry the preregistered fields only. The age curve d(age,pos) is built here (it is
a preregistered covariate construction) and reported, per PREREG_W4.md section 2.
"""
import os, sys, io, json, math, hashlib, shutil, contextlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
STAGE = SP + '/eng33w4_run/rl_after'

STOREP = os.path.join(ROOT, 'engine', 'rl_after', 'rl_model_data.json')
SSP = os.path.join(ROOT, 'data', 'season_state.json')

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
# ENGINE STAGING -- scorer callables only (o30bm convention, verbatim)
# ==================================================================================================
shutil.rmtree(SP + '/eng33w4_run', ignore_errors=True)
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

# THE BARS -- computed off the engine, asserted against Ruling 1. Never typed.
BARS = {g: MA.REPL[g] - rd.REPL_DROP.get(g, 0.0) for g in MA.REPL}
RULING1 = {'KPD': 65.4, 'KPF': 63.8, 'MID': 77.1, 'RUCK': 75.5, 'SD': 75.3, 'SF': 67.9}
for g, b in RULING1.items():
    assert abs(BARS[g] - b) < 5e-2, "bar %s %.4f != Ruling 1's %.1f" % (g, BARS[g], b)
assert abs(float(MA.GAMMA) - 1.0) < 1e-12

def season_points(X, pos, games):
    """26B Ruling 3's pinned callable x Ruling 10's sqrt games weight. Undiscounted board points.
    Identical to o30bm_measure.py::season_points(wmode='sqrt') -- the original test's `cur`."""
    w = min(1.0, math.sqrt(max(0.0, games) / 10.0))
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
STORE_MD5 = md5(STOREP)
D = json.load(open(STOREP))
SS = json.load(open(SSP))
INPROG = int(SS['inprog_year'])              # 2026: never contributes to any outcome or to d
LASTDONE = INPROG - 1                        # 2025: last completed season

P('ORDER 33 W4 STEP 1 -- PANEL BUILD.  store %s (%d players)  inprog=%d' % (STORE_MD5[:8], len(D), INPROG))
P('bars asserted against Ruling 1: %s' % json.dumps({k: round(v, 1) for k, v in sorted(BARS.items())}))

# per-player played-season series with points
SERIES = {}          # key -> list of dicts (year, age, pos, games, avg, pts) sorted by year
META = {}
n_nofut = 0
for p in D:
    fallback = p.get('future_position')
    by = p.get('_by')
    sc = sorted((p.get('scoring') or []), key=lambda r: r['year'])
    played = [x for x in sc if (x.get('games') or 0) > 0]
    if not played or by is None:
        continue
    rows = []
    for x in played:
        pos = bar_group(x.get('pos'), fallback)
        if pos not in BARS:
            continue
        g = float(x['games']); a = float(x['avg'] or 0.0); y = int(x['year'])
        rows.append(dict(year=y, age=y - by, pos=pos, games=g, avg=a,
                         pts=season_points(a, pos, g)))
    if not rows:
        n_nofut += 1
        continue
    SERIES[p['key']] = rows
    META[p['key']] = dict(typ=p.get('type'), pick=p.get('pick'), entry_year=p.get('year'),
                          retired=bool(p.get('_retired')))
P('players with a scoreable played series: %d   (played but no bar group at all: %d)'
  % (len(SERIES), n_nofut))

# ==================================================================================================
# CONSECUTIVE PAIRS (for the age curve d and for TRAJ)   -- 2026 never contributes
# ==================================================================================================
def agebin(a):
    return 17 if a <= 17 else (34 if a >= 34 else int(a))

PAIRS = []           # (key, year Y, agebin at Y, pos at Y, delta = P(Y)-P(Y-1), raw fields)
for k, rows in SERIES.items():
    byyear = {r['year']: r for r in rows}
    for r in rows:
        Y = r['year']
        if Y >= INPROG:          # a 2026 pair would put a partial season inside a delta
            continue
        prev = byyear.get(Y - 1)
        if prev is None:
            continue
        PAIRS.append(dict(key=k, year=Y, ab=agebin(r['age']), age=r['age'], pos=r['pos'],
                          delta=r['pts'] - prev['pts'],
                          g_now=r['games'], g_prev=prev['games'],
                          avg_now=r['avg'], avg_prev=prev['avg']))
P('consecutive played pairs (both seasons played, later season <= %d): %d' % (LASTDONE, len(PAIRS)))

SHRINK_K = 50.0
def age_curve(pairs):
    """d(agebin, pos): pos x age mean delta shrunk toward the all-position age mean, k=50."""
    by_a = collections.defaultdict(list)
    by_ap = collections.defaultdict(list)
    for q in pairs:
        by_a[q['ab']].append(q['delta'])
        by_ap[(q['ab'], q['pos'])].append(q['delta'])
    allm = sum(q['delta'] for q in pairs) / max(1, len(pairs))
    amean = {a: sum(v) / len(v) for a, v in by_a.items()}
    d = {}
    for (a, pos), v in by_ap.items():
        n = len(v); m = sum(v) / n
        d[(a, pos)] = (n * m + SHRINK_K * amean[a]) / (n + SHRINK_K)
    return d, amean, allm, {(a, pos): len(v) for (a, pos), v in by_ap.items()}

def d_lookup(d, amean, allm, ab, pos):
    if (ab, pos) in d:
        return d[(ab, pos)]
    if ab in amean:
        return amean[ab]
    return allm

DFULL, AMEAN, ALLM, DN = age_curve(PAIRS)

# ==================================================================================================
# THE PANEL -- one state per consecutive pair; targets per the prereg windows
# ==================================================================================================
PANEL = []
for k, rows in SERIES.items():
    byyear = {r['year']: r for r in rows}
    cum = 0.0
    m = META[k]
    for i, r in enumerate(rows):
        cum += r['games']
        Y = r['year']
        if Y >= INPROG:
            continue
        prev = byyear.get(Y - 1)
        if prev is None:
            continue
        prev2 = byyear.get(Y - 2)
        # targets: missing (unplayed) seasons contribute ZERO -- zeros stay in
        def pts_at(y):
            return byyear[y]['pts'] if y in byyear else 0.0
        row = dict(key=k, year=Y, age=r['age'], ab=agebin(r['age']), pos=r['pos'],
                   games_at_Y=r['games'], g=cum,
                   p0=r['pts'], p1=prev['pts'], p2=(prev2['pts'] if prev2 else None),
                   avg0=r['avg'], avg1=prev['avg'], g0=r['games'], g1=prev['games'],
                   has_prev2=bool(prev2),
                   delta=r['pts'] - prev['pts'],
                   delta3=((r['pts'] - prev2['pts']) / 2.0 if prev2 else None),
                   typ=m['typ'], pick=m['pick'], entry_year=m['entry_year'], retired=m['retired'])
        if Y + 1 <= LASTDONE:
            row['Y1'] = pts_at(Y + 1)
            row['Y1_played'] = (Y + 1) in byyear
        if Y + 3 <= LASTDONE:
            row['R3'] = sum(pts_at(Y + j) / (1.14 ** j) for j in (1, 2, 3))
        if Y + 6 <= LASTDONE:
            row['R6'] = sum(pts_at(Y + j) / (1.14 ** j) for j in range(1, 7))
        PANEL.append(row)

nY1 = sum(1 for r in PANEL if 'Y1' in r)
nR3 = sum(1 for r in PANEL if 'R3' in r)
nR6 = sum(1 for r in PANEL if 'R6' in r)
pl = len(set(r['key'] for r in PANEL))
P('')
P('PANEL: %d states, %d players' % (len(PANEL), pl))
P('  target (a) next-season Y1 (Y+1<=%d):   n=%d, players=%d'
  % (LASTDONE, nY1, len(set(r['key'] for r in PANEL if 'Y1' in r))))
P('  target (b) 3yr forward R3 (Y+3<=%d):   n=%d' % (LASTDONE, nR3))
P('  target (c) 6yr forward R6 (Y<=%d):     n=%d  [the ORIGINAL target window]' % (LASTDONE - 6, nR6))
nd = [r for r in PANEL if 'R6' in r and r['typ'] == 'ND' and r['pick'] and 1 <= r['pick'] <= 64
      and r['entry_year'] and r['entry_year'] >= 2005]
P('  s3 ND 1-64 entry>=2005 subpanel on (c): n=%d   (original 30B-M panel had n=4033 on ND states)' % len(nd))
P('')
P('POWER COMPARISON (prereg section: the original L->T test ran on n=4033 ND-only 6yr-window states;')
P('target (a) here pools %d states / %d players, all entry types, 1 df)' % (nY1, pl))

# census tables
P('')
P('STATES (target a) BY AGE BAND x POSITION')
POSL = sorted(BARS)
ABL = ['<=19', '20-21', '22-23', '24-25', '26-28', '29+']
def abland(a):
    return '<=19' if a <= 19 else ('20-21' if a <= 21 else ('22-23' if a <= 23 else
           ('24-25' if a <= 25 else ('26-28' if a <= 28 else '29+'))))
tab = collections.Counter((abland(r['age']), r['pos']) for r in PANEL if 'Y1' in r)
P('%-8s' % 'age' + ''.join('%7s' % g for g in POSL) + '%8s' % 'ALL')
for ab in ABL:
    P('%-8s' % ab + ''.join('%7d' % tab[(ab, g)] for g in POSL) + '%8d' % sum(tab[(ab, g)] for g in POSL))
P('%-8s' % 'ALL' + ''.join('%7d' % sum(tab[(ab, g)] for ab in ABL) for g in POSL) + '%8d' % nY1)

P('')
P('THE AGE CURVE d(age) -- population expected one-season change in season points (pairs, 2026 out)')
P('%-6s %8s %12s   per-position (shrunk, k=%.0f), n in parens' % ('age', 'n', 'mean dP', SHRINK_K))
for a in sorted(AMEAN):
    na = sum(1 for q in PAIRS if q['ab'] == a)
    parts = []
    for g in POSL:
        if (a, g) in DFULL:
            parts.append('%s %+.0f(%d)' % (g, DFULL[(a, g)], DN[(a, g)]))
    P('%-6s %8d %+12.1f   %s' % (('<=17' if a == 17 else ('34+' if a == 34 else a)), na, AMEAN[a], '  '.join(parts)))
P('overall mean pair delta: %+.1f points' % ALLM)

json.dump(dict(meta=dict(store_md5=STORE_MD5, built='2026-08-17 ORDER33 W4 step1',
                         n_players_store=len(D), n_players_series=len(SERIES),
                         n_pairs=len(PAIRS), n_panel=len(PANEL), n_Y1=nY1, n_R3=nR3, n_R6=nR6,
                         inprog=INPROG, bars={k: round(v, 4) for k, v in BARS.items()},
                         shrink_k=SHRINK_K, disc=0.14,
                         prereg='PREREG_W4.md pushed before this ran'),
               age_curve=dict(by_age={str(a): AMEAN[a] for a in AMEAN},
                              by_age_pos={'%d|%s' % (a, g): v for (a, g), v in DFULL.items()},
                              n_by_age_pos={'%d|%s' % (a, g): n for (a, g), n in DN.items()},
                              overall=ALLM),
               pairs=PAIRS, panel=PANEL),
          open(os.path.join(HERE, 'W4_PANEL.json'), 'w'))
open(os.path.join(HERE, 'CENSUS_W4_out.txt'), 'w').write('\n'.join(_LOG) + '\n')
P('')
P('wrote W4_PANEL.json + CENSUS_W4_out.txt')
