#!/usr/bin/env python3
"""ORDER 31-F  --  F2: THE POOL PARAMETERS.  beta_pool DERIVED; D_pool RE-CONTROLLED.  READ-ONLY.

TWO OBJECTS, TWO TRANSPLANTED INSTRUMENTS, NEITHER RE-IMPLEMENTED.

  D_pool   the sitter fade on pool cohorts.  ORDER 31's own o31_pool.py construction, re-run: the 30A-2
           harness prefix is exec'd VERBATIM and only the population and the v0 object are swapped.  Its
           CONTROL is re-pointed to the 31-F re-derived ND row, because that is the row this candidate
           wires -- controlling against the superseded row would be controlling against the wrong ruler.

  beta_pool  THE OPEN ITEM ORDER 31 LEFT.  The 30B-M PANEL CONSTRUCTION is transplanted to pool cohorts:
           the harness's own `panel(..., nd_only=False)` pool states, its own `band_fit` regression
           (R ~ pos dummies + age + age^2 + o + o^2 + cur + cur^3 + games_at_Y + log1p(g) + v0, clustered
           on the player), its own games bands and its own H=6 horizon.  THE ONLY THING SUPPLIED HERE is
           the v0 the pool rows never had: `MA.pool_v0_of(p)`, the ONE accessor that HALTS on an unsigned
           cell.  Thin PATHWAY TIERS are K-shrunk (K = 15, the project's own K_SHRINK) toward the pooled
           pool row with the borrowing printed per cell.  MSD first-season-is-season-1 rides
           debut_year_338's own MSD clause inside the transplanted prefix.
           CONTROL, able to fail: re-running `band_fit` on the harness's ND panel must reproduce the
           31-F ND beta row exactly.
"""
import os, sys, json, math, collections, hashlib, io, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(EV))
SRC30A2 = os.path.join(EV, 'sitter_fade_2026-08-14', 'o30a2_recut.py')
SRC30BM = os.path.join(EV, 'pedigree_persistence_2026-08-14', 'o30bm_measure.py')
K_SHRINK_TIER = 15.0

OUT = []
def P(s=''):
    OUT.append(s); print(s)

FADE31F = json.load(open(os.path.join(HERE, 'FADE_31F.json')))
BETA31F = json.load(open(os.path.join(HERE, 'BETA_31F.json')))
ND_RULED_31F = {int(k): float(v) for k, v in FADE31F['wired'].items()}

P('ORDER 31-F  F2 -- THE POOL PARAMETERS (beta_pool DERIVED; D_pool re-controlled)')
P('')

# =====================================================================================================
# PART 1 -- D_pool, by the 30A-2 estimator (ORDER 31's construction, control re-pointed to the 31-F row)
# =====================================================================================================
_t = open(SRC30A2).read()
MD5_30A2 = hashlib.md5(_t.encode()).hexdigest()
NS = {'__name__': 'o30a2_prefix', '__file__': SRC30A2}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_t[:_t.index('\nSURF = collections.OrderedDict(')], SRC30A2, 'exec'), NS)

ENTRIES, ATTR, GA = NS['ENTRIES'], NS['ATTR'], NS['GA']
DEPTHS, K_SHRINK = NS['DEPTHS'], NS['K_SHRINK']
at_depth, cell, normalise, listed_LB = NS['at_depth'], NS['cell'], NS['normalise'], NS['listed_LB']
leading_sit, ever_played = NS['leading_sit'], NS['ever_played']
min_tenure_338, resolution_class, listed_through_LA = NS['min_tenure_338'], NS['resolution_class'], NS['listed_through_LA']
MA = NS['MA']

P('PART 1 -- D_pool.  transplanted prefix %s  md5 %s' % (os.path.relpath(SRC30A2, ROOT), MD5_30A2))
_bk = {}
for _p in MA.data:
    _bk.setdefault(_p.get('key') or MA.slug(_p['player']), _p)
def pool_v0(key):
    p = _bk.get(key)
    if p is None or not p.get('_pool'): return None
    try: v = MA.pool_v0_of(p)
    except Exception: return None
    return float(v) if v else None

POP, SKIP = [], collections.Counter()
for e in ENTRIES:
    a = ATTR.get(e['key'])
    if not a or a.get('excluded'): SKIP['no attribution / excluded'] += 1; continue
    if a.get('mechanism') == 'ND 1-64' or e['type'] == 'ND': continue
    v0 = pool_v0(e['key'])
    if not v0 or v0 <= 0: SKIP['no signed pool v0 cell'] += 1; continue
    if e['entry_year'] is None: SKIP['no entry year'] += 1; continue
    if e['key'] not in GA: SKIP['no grace-A career score'] += 1; continue
    POP.append(dict(key=e['key'], entry_year=e['entry_year'], pathway=e['type'],
                    mech=a.get('mechanism'), v0=v0, retired=e['retired'], last_listed=e['last_listed'],
                    maxdepth=1 + leading_sit(e), ever=ever_played(e), min_tenure=min_tenure_338(e),
                    listed_through_LA=listed_through_LA(e), res=resolution_class(e),
                    ga_total=float(GA[e['key']]['total']), ga_tshare=float(GA[e['key']]['tail_share']), e=e))
FIT = [r for r in POP if 2004 <= r['entry_year'] <= 2021]

NDFIT = NS['FIT']
ND_SURF = {N: cell([r for r in at_depth(NDFIT, N) if listed_LB(r, N)], N) for N in DEPTHS}
ND_D = normalise(ND_SURF)
CTRL_DEV = {N: abs(ND_D[N] - ND_RULED_31F[N]) for N in (2, 3, 4) if ND_D.get(N) is not None}
CTRL_OK = all(v < 5e-4 for v in CTRL_DEV.values())
P('  CONTROL -- this transplanted estimator must reproduce THE 31-F ND ROW (not the superseded one)')
P('    here  %s' % '  '.join('%d:%.6f' % (N, ND_D[N]) for N in (2, 3, 4)))
P('    31-F  %s' % '  '.join('%d:%.6f' % (N, ND_RULED_31F[N]) for N in (2, 3, 4)))
P('    max deviation %.3e   VERDICT %s' % (max(CTRL_DEV.values()), 'REPRODUCED' if CTRL_OK else '*** DRIFT ***'))
if not CTRL_OK:
    raise SystemExit('ORDER 31-F HALT: the pool estimator no longer reproduces the ND row it is a transplant of')

POOL_SURF = {N: cell([r for r in at_depth(FIT, N) if listed_LB(r, N)], N) for N in DEPTHS}
POOL_D = normalise(POOL_SURF)
P('  THE POOLED POOL ROW (L-B listed-conditional, fitted window 2004-2021)')
P('    %2s %6s %12s %12s %9s %9s %9s %7s %10s'
  % ('N', 'n', 'mean(v/v0)', 'D(N)', 'median', 'p25', 'p75', 'n_ever', 'tail_share'))
for N in DEPTHS:
    c = POOL_SURF[N]
    if not c.get('n'): continue
    P('    %2d %6d %12.6f %12.6f %9.4f %9.4f %9.4f %7d %10.4f'
      % (N, c['n'], c['mean'], POOL_D[N], c['median'], c['p25'], c['p75'], c['n_ever'], c['tail_share']))
N_FLOOR = 8
_ok = [N for N in DEPTHS if POOL_SURF[N].get('n', 0) >= N_FLOOR and POOL_D.get(N) is not None and POOL_D[N] <= 1.0]
DEEPEST = max(_ok or [1])
REJECTED = {N: {'n': POOL_SURF[N].get('n', 0), 'D': POOL_D.get(N),
                'tail_share': POOL_SURF[N].get('tail_share'), 'n_ever': POOL_SURF[N].get('n_ever'),
                'why': ('n %d below the floor %d' % (POOL_SURF[N].get('n', 0), N_FLOOR))
                       if POOL_SURF[N].get('n', 0) < N_FLOOR else 'D > 1.0 -- the cell INVERTS (selection)'}
            for N in DEPTHS if N > DEEPEST and POOL_D.get(N) is not None}
WIRED_D = {1: 1.0}
for N in DEPTHS:
    if N != 1 and POOL_D.get(N) is not None and N <= DEEPEST:
        WIRED_D[N] = POOL_D[N]
P('  THE WIRED POOL FADE (n floor %d; a cell must BE A FADE (D<=1); FLAT from depth %d out)' % (N_FLOOR, DEEPEST))
for N in sorted(REJECTED):
    r = REJECTED[N]
    P('    REJECTED D_pool(%d) = %.6f  n %d  n_ever %s  tail_share %.4f  -- %s'
      % (N, r['D'], r['n'], r['n_ever'], r['tail_share'], r['why']))
for N in sorted(WIRED_D):
    P('    D_pool(%d) = %.16f   n = %d' % (N, WIRED_D[N], POOL_SURF[N].get('n', 0)))
P('    D_pool(c >= %d) FLAT at %.16f' % (DEEPEST, WIRED_D[DEEPEST]))
P('')

# =====================================================================================================
# PART 2 -- beta_pool, by the 30B-M PANEL CONSTRUCTION TRANSPLANTED TO POOL COHORTS
# =====================================================================================================
_b = open(SRC30BM).read()
MD5_30BM = hashlib.md5(_b.encode()).hexdigest()
V0SUB = [("V0P = os.path.join(ROOT, 'docs', 'evidence', 'one_machinery_2026-08-14', 'V0REFIT30B.json')",
          "V0P = os.path.join(ROOT, 'docs', 'evidence', 'candidate_31f', 'HEADFIX_31F.json')"),
         ("POSV = V0ART['posv_out']", "POSV = V0ART['posv_headfixed']"),
         ("SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'",
          "SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o31f'")]
_brun = _b
for a, bb in V0SUB:
    assert _brun.count(a) == 1, 'sub target not unique: %r' % a[:50]
    _brun = _brun.replace(a, bb)
MARK = '\nq1 = {}\n'
PREFIX = _brun.split(MARK)[0]
G = {'__file__': SRC30BM, '__name__': 'o30bm_reused'}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(PREFIX, SRC30BM, 'exec'), G)

np = G['np']
STATES, PTS = G['STATES'], G['PTS']
panel, band_fit, GAMES_BANDS = G['panel'], G['band_fit'], G['GAMES_BANDS']
ENT2, MA2 = G['ENT'], G['MA']
ROWS_ND = G['ROWS']
MIDS = {'0-5': 2.5, '6-15': 10.5, '16-35': 25.5, '36-70': 53.0, '71+': 85.5}
ORDER = ['0-5', '6-15', '16-35', '36-70', '71+']

P('PART 2 -- beta_pool.  transplanted panel %s  md5 %s (v0 source re-pointed to the head-fixed surface)'
  % (os.path.relpath(SRC30BM, ROOT), MD5_30BM))

# --- the control: band_fit on the harness's OWN ND panel must reproduce the 31-F ND beta row ---------
CTRL_B = {}
for nm, lo, hi in GAMES_BANDS:
    f = band_fit([r for r in ROWS_ND if r['gb'] == nm])
    CTRL_B[nm] = float(f['beta_v0']) if f else None
REF_B = {nm: b for nm, (m, b) in zip(ORDER, BETA31F['rederived_points'])}
DEVB = {nm: abs(CTRL_B[nm] - REF_B[nm]) for nm in ORDER if CTRL_B[nm] is not None}
P('  CONTROL -- band_fit on the ND panel reproduces the 31-F ND beta row')
P('    here  %s' % '  '.join('%s:%.7f' % (nm, CTRL_B[nm]) for nm in ORDER))
P('    31-F  %s' % '  '.join('%s:%.7f' % (nm, REF_B[nm]) for nm in ORDER))
P('    max deviation %.3e   VERDICT %s' % (max(DEVB.values()), 'REPRODUCED' if max(DEVB.values()) < 1e-9 else '*** DRIFT ***'))
if max(DEVB.values()) >= 1e-9:
    raise SystemExit('ORDER 31-F HALT: the transplanted panel does not reproduce the ND beta row')

# --- the POOL panel: the harness's own pool states, given the v0 they never had ----------------------
_bk2 = {}
for _p in MA2.data:
    _bk2.setdefault(_p.get('key') or MA2.slug(_p['player']), _p)
def pool_v0_2(key):
    p = _bk2.get(key)
    if p is None or not p.get('_pool'): return None
    try: v = MA2.pool_v0_of(p)
    except Exception: return None
    return float(v) if v else None

POOLROWS_RAW = [r for r in panel(STATES, PTS, H=6, nd_only=False) if not r['nd']]
POOLROWS, NOV0 = [], collections.Counter()
for r in POOLROWS_RAW:
    v = pool_v0_2(r['key'])
    if not v or v <= 0:
        NOV0[(ENT2.get(r['key']) or {}).get('type') or '?'] += 1
        continue
    r = dict(r); r['v0'] = float(v)
    r['tier'] = (ENT2.get(r['key']) or {}).get('type') or '?'
    POOLROWS.append(r)
P('  POOL PANEL: %d states over %d careers  (dropped for an unsigned/absent pool v0 cell: %d %s)'
  % (len(POOLROWS), len({r['key'] for r in POOLROWS}), sum(NOV0.values()), dict(NOV0)))
P('  by pathway tier: %s' % dict(collections.Counter(r['tier'] for r in POOLROWS)))
P('')

P('  beta_pool BY GAMES BAND -- the SAME band_fit, on the pool panel')
P('    %-8s %6s %7s %8s %14s %9s %10s %12s'
  % ('band', 'mid', 'n', 'clusters', 'beta_pool', 't', 'sigma %', 'ND beta 31-F'))
BPOOL, BPOOL_FIT = {}, {}
for nm, lo, hi in GAMES_BANDS:
    rb = [r for r in POOLROWS if r['gb'] == nm]
    f = band_fit(rb)
    BPOOL_FIT[nm] = f
    if f is None:
        P('    %-8s %6.1f %7d %8s %14s %9s %10s %12.6f  -- n < 40, NO FIT'
          % (nm, MIDS[nm], len(rb), '-', '-', '-', '-', REF_B[nm]))
        BPOOL[nm] = None
        continue
    BPOOL[nm] = float(f['beta_v0'])
    P('    %-8s %6.1f %7d %8d %14.7f %9.2f %10.2f %12.6f'
      % (nm, MIDS[nm], f['n'], f['n_clusters'], f['beta_v0'], f['t_v0'] or float('nan'),
         100 * (f['sigma'] or 0), REF_B[nm]))
P('')

# --- thin PATHWAY TIERS, K-shrunk toward the pooled pool row -----------------------------------------
TIERS = sorted({r['tier'] for r in POOLROWS})
P('  BY PATHWAY TIER, K-SHRUNK TOWARD THE POOLED POOL ROW (K = %.0f). BORROWING PRINTED.' % K_SHRINK_TIER)
P('    %-6s %-8s %6s %13s %8s %13s %9s'
  % ('tier', 'band', 'n', 'raw beta', 'w_own', 'SHRUNK beta', 'borrowed'))
BY_TIER = {}
for tr in TIERS:
    BY_TIER[tr] = {'n_states': sum(1 for r in POOLROWS if r['tier'] == tr), 'raw': {}, 'shrunk': {}, 'n': {}}
    for nm, lo, hi in GAMES_BANDS:
        rb = [r for r in POOLROWS if r['tier'] == tr and r['gb'] == nm]
        base = BPOOL.get(nm)
        if base is None: continue
        f = band_fit(rb)
        raw = float(f['beta_v0']) if f else None
        n = len(rb)
        w = n / (n + K_SHRINK_TIER) if n else 0.0
        if raw is None: w = 0.0
        sh = w * (raw if raw is not None else base) + (1 - w) * base
        BY_TIER[tr]['raw'][nm] = raw; BY_TIER[tr]['shrunk'][nm] = sh; BY_TIER[tr]['n'][nm] = n
        P('    %-6s %-8s %6d %13s %8.4f %13.7f %8.1f%%'
          % (tr, nm, n, ('%.7f' % raw) if raw is not None else '  no fit  ', w, sh, 100 * (1 - w)))
P('')

# --- the WIRED beta_pool object ----------------------------------------------------------------------
# THE WIRING RULE, DECLARED AND APPLIED MECHANICALLY: the wired object is the POOLED POOL ROW (the same
# decision the pool fade made, for the same reason -- per-tier cells mostly do not clear band_fit's own
# n>=40 floor).  Bands with no fit inherit the ND 31-F beta and THE BORROW IS PRINTED.  The curve is then
# put through the SAME monotone non-increasing projection the brief's "pi decays in g" requires.
def mono_dec(pts):
    out, cur = [], None
    for g, y in pts:
        cur = y if cur is None else min(cur, y)
        out.append((g, cur))
    return out
BORROWED = [nm for nm in ORDER if BPOOL[nm] is None]
RAWPTS = [(MIDS[nm], BPOOL[nm] if BPOOL[nm] is not None else REF_B[nm]) for nm in ORDER]
FLOORED = [(g, max(0.0, b)) for g, b in RAWPTS]
MONOPTS = mono_dec(FLOORED)
P('  THE WIRED beta_pool  (pooled pool row; ND-borrowed where band_fit has no fit; then the SAME')
P('  monotone non-increasing projection the ND beta carries)')
P('    raw       ' + ' '.join('%.4f' % b for _, b in RAWPTS))
P('    floored   ' + ' '.join('%.4f' % b for _, b in FLOORED))
P('    monotone  ' + ' '.join('%.4f' % b for _, b in MONOPTS))
P('    ND 31-F   ' + ' '.join('%.4f' % b for _, b in BETA31F['monotone_points']))
P('    BANDS BORROWED FROM THE ND ROW: %s' % (', '.join(BORROWED) if BORROWED else 'none'))
_neg = [(g, b) for g, b in RAWPTS if b < 0]
P('    negative raw cells zero-floored: %s' % (_neg if _neg else 'none'))
P('')

# --- Phi on pool rows: does the pool panel support the 30B-C conditioning? ----------------------------
# 30B-C's Phi is beta_stall/beta_pooled where beta_stall is the SAME band_fit run on the stall
# sub-cohort.  Test whether the pool panel can carry it: split the pool panel the same way and see
# whether ANY band clears band_fit's own n>=40 floor.
def stalled(r):
    """30B-C's forward definition: no DELIVERED season in the H window after the state year."""
    k, Y = r['key'], r['year']
    for j in (1, 2):
        for s in G['SEA'].get(k, []):
            if s['year'] == Y + j and (s['games'] or 0) >= 10:
                g = G['bar_group'](s.get('position_played'), None)
                if g and g in G['BARS'] and float(s.get('avg') or 0) >= G['BARS'][g]:
                    return False
    return True
STALLROWS = [r for r in POOLROWS if stalled(r)]
P('  Phi ON POOL ROWS -- can the pool panel carry the 30B-C conditioning by the same construction?')
P('    %-8s %8s %8s %14s %8s' % ('band', 'n_pool', 'n_stall', 'beta_stall_pool', 't'))
BSTALL_POOL, BSTALL_T, PHI_SUPPORTED = {}, {}, True
for nm, lo, hi in GAMES_BANDS:
    rs = [r for r in STALLROWS if r['gb'] == nm]
    f = band_fit(rs)
    BSTALL_POOL[nm] = float(f['beta_v0']) if f else None
    BSTALL_T[nm] = float(f['t_v0']) if (f and f.get('t_v0') is not None) else None
    if f is None: PHI_SUPPORTED = False
    P('    %-8s %8d %8d %14s %8s'
      % (nm, sum(1 for r in POOLROWS if r['gb'] == nm), len(rs),
         ('%.7f' % f['beta_v0']) if f else 'n < 40 -- NO FIT',
         ('%.2f' % f['t_v0']) if (f and f.get('t_v0') is not None) else '-'))

def loglin(pts, g):
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

if PHI_SUPPORTED:
    # THE SAME CONSTRUCTION o31_fit.py APPLIES TO THE ND ROW, APPLIED HERE UNCHANGED:
    # zero-floor the stall coefficients, monotone-project them, take the ratio to the wired (monotone)
    # beta_pool, clip to [0,1], monotone-project the ratio.
    SP_FLOOR = [(MIDS[nm], max(0.0, BSTALL_POOL[nm])) for nm in ORDER]
    SP_MONO = mono_dec(SP_FLOOR)
    _bp = lambda g: loglin(MONOPTS, g)
    _bs = lambda g: loglin(SP_MONO, g)
    PHI_RAW_POOL = [(MIDS[nm], (1.0 if _bp(MIDS[nm]) <= 0 else
                                min(1.0, max(0.0, _bs(MIDS[nm]) / _bp(MIDS[nm]))))) for nm in ORDER]
    PHI_POOL_PTS = mono_dec(PHI_RAW_POOL)
    PHI_VERDICT = ('SUPPORTED -- every pool games band clears band_fit\'s own n>=40 floor, so pool rows '
                   'carry a POOL-MEASURED PhiStall by the same construction as the ND row. NOTHING IS '
                   'BORROWED HERE.')
    P('')
    P('  PhiStall_pool = beta_stall_pool / beta_pool, zero-floored, monotone, clipped to [0,1]')
    P('    %6s %14s %16s %14s %16s' % ('mid', 'beta_pool', 'beta_stall_pool', 'PhiStall_pool', 'PhiStall_ND(31-F)'))
    for (m, ph), (_, ndph) in zip(PHI_POOL_PTS, [(2.5, 0.5792926948039687), (10.5, 0.298245232115451),
                                                 (25.5, 0.298245232115451), (53.0, 0.0), (85.5, 0.0)]):
        P('    %6.1f %14.7f %16.7f %14.7f %16.7f' % (m, _bp(m), _bs(m), ph, ndph))
else:
    PHI_POOL_PTS = None
    PHI_VERDICT = ('NOT SUPPORTED -- at least one pool games band does not clear band_fit\'s own n>=40 '
                   'floor. Pool rows therefore carry the ND-MEASURED PhiStall, and that borrowing is '
                   'DISCLOSED, not hidden.')
P('    VERDICT: %s' % PHI_VERDICT)
P('')

LIMITS = [
 'beta_pool is now DERIVED rather than borrowed -- the largest open item ORDER 31 left. What is still '
 'borrowed is named on every line above: any games band whose pool panel does not clear band_fit\'s own '
 'n >= 40 floor carries the ND 31-F coefficient, and those bands are listed.',
 'The WIRED beta_pool object is the POOLED POOL ROW, not a per-tier law. Per-tier cells are published '
 'K-shrunk (K = 15) so the borrowing is visible; most do not clear the fitting floor on their own.',
 'The pool panel is SMALLER and MORE HETEROGENEOUS than the ND panel: it mixes rookie-draft, mid-season '
 'draft, pre-season and supplemental routes whose entry ages and clocks differ. The tier table is the '
 'disclosure of that heterogeneity.',
 'THE DEPTH-3 POOL FADE CELL STILL INVERTS and is still NOT WIRED, by the pre-declared rule. OWED '
 'OWNER CONFIRMATION.',
 'The DV grace-A scores were built on store d9a24282; this branch carries a different store. Layer 1 is '
 'byte-identical, so the population and every sit fact are unaffected. Inherited from 30A-2.',
 'MSD first-season-is-season-1 (owner ruling 5) rides debut_year_338\'s own MSD clause inside the '
 'transplanted prefix, inherited rather than restated.',
]
P('LIMITATIONS, STATED')
for i, l in enumerate(LIMITS, 1):
    P('  %d. %s' % (i, l))

json.dump({'order': 'ORDER 31-F F2 -- the pool parameters',
           'instruments': {'fade': {'path': os.path.relpath(SRC30A2, ROOT), 'md5': MD5_30A2},
                           'beta': {'path': os.path.relpath(SRC30BM, ROOT), 'md5': MD5_30BM,
                                    'v0_substitutions': [{'from': a, 'to': b} for a, b in V0SUB]}},
           'fade': {'control_nd_31f': {str(N): ND_D.get(N) for N in DEPTHS},
                    'control_target': {str(k): v for k, v in ND_RULED_31F.items()},
                    'control_max_dev': max(CTRL_DEV.values()), 'control_ok': CTRL_OK,
                    'pool_surface': {str(N): {k: v for k, v in POOL_SURF[N].items() if k != 'res'} for N in DEPTHS},
                    'pool_D': {str(N): POOL_D.get(N) for N in DEPTHS},
                    'wired': {str(k): v for k, v in WIRED_D.items()}, 'flat_from': DEEPEST,
                    'n_floor': N_FLOOR, 'rejected_cells': {str(k): v for k, v in REJECTED.items()},
                    'population_fitted': len(FIT), 'population_total': len(POP)},
           'beta_pool': {'control_nd_band_fit': CTRL_B, 'control_target': REF_B,
                         'control_max_dev': max(DEVB.values()),
                         'panel_n': len(POOLROWS), 'panel_careers': len({r['key'] for r in POOLROWS}),
                         'by_band': {nm: BPOOL_FIT[nm] for nm in ORDER},
                         'raw_points': [[g, b] for g, b in RAWPTS],
                         'monotone_points': [[g, b] for g, b in MONOPTS],
                         'borrowed_bands': BORROWED,
                         'by_tier': BY_TIER, 'K_tier': K_SHRINK_TIER,
                         'nd_beta_31f': BETA31F['monotone_points']},
           'phi_pool': {'beta_stall_by_band': BSTALL_POOL, 't_by_band': BSTALL_T,
                        'supported': PHI_SUPPORTED, 'verdict': PHI_VERDICT,
                        'phistall_points': ([[m, y] for m, y in PHI_POOL_PTS] if PHI_POOL_PTS else None),
                        'n_stall_states': len(STALLROWS)},
           'limitations': LIMITS},
          open(os.path.join(HERE, 'POOL31F.json'), 'w'), indent=1, sort_keys=True, default=str)
open(os.path.join(HERE, 'POOL31F_out.txt'), 'w').write('\n'.join(OUT) + '\n')
print('\nPOOL31F.json written.')
print('\nTHE CONSTANTS TO WIRE:')
print('  O31_POOL_D={%s}  flat from %d' % (','.join('%d:%r' % (k, v) for k, v in sorted(WIRED_D.items())), DEEPEST))
print('  O31_BETA_POOL=(' + ','.join('(%r,%r)' % (g, b) for g, b in MONOPTS) + ')')
if PHI_POOL_PTS:
    print('  O31_PHIST_POOL=(' + ','.join('(%r,%r)' % (g, b) for g, b in PHI_POOL_PTS) + ')')
