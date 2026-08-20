#!/usr/bin/env python3
# =====================================================================================================
# ORDER 30A -- THE ND SITTER DISCOUNT, DERIVED FROM EVIDENCE.
#
# READ-ONLY.  This instrument writes only into docs/evidence/sitter_fade_2026-08-14/.  It does not
# touch the store, the board, the curve or any engine file, and it does not wire anything.  The old
# `los_decay` schedule remains the DECLARED FALLBACK until the owner rules.
#
# Estimator, censoring rule and every prediction were committed FIRST in PREREG_30A.md.
#
# INPUTS (all pinned by md5; the instrument halts on any mismatch):
#   data/delivered_value/layer1_player_seasons.json          ad1229ea...  (assumption-free player-seasons)
#   docs/evidence/delivered_value_2026-08-12/LAYER2.json     (the DV lane's grace-A career scores)
#     -- BOTH live on origin/build/delivered-value, not on this branch; they are read out of git by
#        `git show` rather than duplicated into this directory, and md5-asserted after the read.
#   engine/rl_after/pvc_curve_v2.json                        (the landed entry law -- nd_v0.posv)
#   docs/evidence/landing_29_2026-08-13/DAY0_29B_FINAL.json  (the 29B printed flat-v0 prices)
#   engine/rl_after/rl_model.py                              (imported live: disc_factor, GRACE, LOS_C/P)
#
# STORE DRIFT, DISCLOSED (PREREG CENSOR-4): the DV lane's scores were built on store d9a24282; this
# branch carries store cb38ef11.  Layer 1 (ad1229ea) is byte-identical, so the POPULATION and every
# SIT FACT are unaffected.  The depth-1 normalisation absorbs any level offset.  No DV number is
# recomputed on the new store; the secondary observed-leg instrument (§SECONDARY) is computed wholly
# on the live store so the store cancels inside its own ratio.
# =====================================================================================================
import os, sys, json, math, hashlib, subprocess, collections, io, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
OUTD = HERE

# ---- thread pinning BEFORE the engine import (the DV lane's rule, carried verbatim) -----------------
os.environ.update(PYTHONHASHSEED='0', RL_REPO=ROOT, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1',
                  MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1')

DV_BRANCH = 'origin/build/delivered-value'
L1_REL = 'data/delivered_value/layer1_player_seasons.json'
L2_REL = 'docs/evidence/delivered_value_2026-08-12/LAYER2.json'
L1_MD5 = 'ad1229ea6f443538479447132382b21c'

# pins ON THIS BRANCH -- recorded, and asserted so a later reader knows exactly what was read
PINS = {
    'curve':  ('engine/rl_after/pvc_curve_v2.json',                      None),
    'day0_29b': ('docs/evidence/landing_29_2026-08-13/DAY0_29B_FINAL.json', None),
    'rl_model': ('engine/rl_after/rl_model.py',                          '14000af2a46f7a3c4cdfde303f5a1aff'),
    'store':  ('engine/rl_after/rl_model_data.json',                     'cb38ef1171dcf20aae66ebf12682be0d'),
}


def md5b(b):
    h = hashlib.md5(); h.update(b); return h.hexdigest()


def md5f(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()


def git_show(ref, rel):
    """Read a pinned input out of git rather than duplicating 7 MB of it into this directory.
    If the ref is missing:  git fetch origin build/delivered-value"""
    try:
        return subprocess.check_output(['git', '-C', ROOT, 'show', '%s:%s' % (ref, rel)],
                                       stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as ex:
        raise SystemExit('cannot read %s:%s -- run `git fetch origin %s` first.\n  %s'
                         % (ref, rel, ref.split('/', 1)[-1], (ex.stderr or b'').decode().strip()))


LOG = []


def P(s=''):
    print(s); LOG.append(s)


P('=' * 118)
P('ORDER 30A  --  THE ND SITTER DISCOUNT, DERIVED FROM EVIDENCE')
P('=' * 118)
P('READ-ONLY.  Nothing wires.  The old los_decay schedule stands as the DECLARED FALLBACK.')
P('Prereg: PREREG_30A.md, committed before this file existed in runnable form.')
P('')

# -----------------------------------------------------------------------------------------------------
# INPUTS
# -----------------------------------------------------------------------------------------------------
_l1b = git_show(DV_BRANCH, L1_REL)
if md5b(_l1b) != L1_MD5:
    raise SystemExit('LAYER1 PIN FAILED: %s != %s' % (md5b(_l1b), L1_MD5))
L1 = json.loads(_l1b.decode())
_l2b = git_show(DV_BRANCH, L2_REL)
L2_MD5 = md5b(_l2b)
L2 = json.loads(_l2b.decode())

PIN_OBS = {}
for k, (rel, exp) in PINS.items():
    got = md5f(os.path.join(ROOT, rel))
    PIN_OBS[k] = got
    if exp and got != exp:
        raise SystemExit('PIN FAILED %s: %s != %s (%s)' % (k, got, exp, rel))

CURVE = json.load(open(os.path.join(ROOT, PINS['curve'][0])))
POSV = CURVE['nd_v0']['posv']                      # posv[group][str(pick)]  -- the landed entry law
DAY0 = json.load(open(os.path.join(ROOT, PINS['day0_29b'][0])))
NUMERAIRE = float(CURVE['numeraire_pin1_3000']) if isinstance(CURVE.get('numeraire_pin1_3000'), (int, float)) \
    else None

P('INPUTS')
P('  layer1                 %s  (%s:%s)' % (L1_MD5[:12], DV_BRANCH, L1_REL))
P('  LAYER2 (grace-A)       %s  (%s:%s)' % (L2_MD5[:12], DV_BRANCH, L2_REL))
for k in sorted(PIN_OBS):
    P('  %-22s %s  (%s)' % (k, PIN_OBS[k][:12], PINS[k][0]))
P('  STORE DRIFT DISCLOSED: DV scores built on d9a24282; this branch carries %s. Layer 1 identical.'
  % PIN_OBS['store'][:8])
P('')

# ---- the engine, live: disc_factor and the OLD schedule's own constants, never hand-typed -----------
sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', ROOT + '/engine/rl_after']
_cwd = os.getcwd(); os.chdir(ROOT + '/engine/rl_after')
with contextlib.redirect_stdout(io.StringIO()):
    import rl_model as MA
    import dist_redesign as rd
os.chdir(_cwd)
assert int(MA.AGE_REF) == 2026, 'AGE_REF %s' % MA.AGE_REF
assert MA.AGE_DISC is False, 'AGE_DISC must be OFF (flat-14 ladder) -- got %s' % MA.AGE_DISC

NOW = 2026
LAST_COMPLETE = 2025          # 2026 is in progress (CENSOR-2)

# =====================================================================================================
# THE ONE CONFIG BLOCK.  Every constant here is read live off the engine or is a stated owner ruling.
# =====================================================================================================
CFG = dict(
    act='ORDER 30A -- the ND sitter discount, derived',
    read_only=True,
    wires_nothing='the old los_decay stands as the DECLARED FALLBACK until the owner rules',

    depth='N = season_year - entry_year, the engine\'s own los() clock. N=1 is a normal draftee\'s '
          'first season. STILL SITTING AT DEPTH N == zero games in every season k=1..N-1. The cells '
          'are NESTED: a player who sat two seasons appears in the N=1, N=2 and N=3 cells.',

    numerator='LAYER2.json::grace_a[key].total (the delivered-value lane\'s grace-A career score, '
              'discounted to acquisition) RE-ANCHORED to the start of year N by x disc_factor(k=N-1). '
              'A sitter has zero delivered value before depth N, so his whole career score IS his '
              'from-depth-N score -- no per-season decomposition is needed and none is performed.',
    reanchor='V_N(i) = grace_a[i].total * DF_i(N-1);  DF_i(k) = MA.disc_factor(entry_age, 0.14, '
             'max(0, k - G_i));  G_i = 2 if entry_age <= 19 else 0  (grace-A reading O, the DV lane\'s '
             'own primary). Without it a player who sat a year and then delivered a fresh entrant\'s '
             'career would read a 0.877 discount that is pure time-value and says nothing about sitting.',
    reanchor_note='disc_factor is IMPORTED from the engine, never reimplemented.',

    denominator='pvc_curve_v2.json::nd_v0.posv[day0_position][attributed_pick] -- the ORDER-29 landed '
                'positional ND day-0 entry law, read at the ACQUISITION SLOT (Ruling 5: drafted '
                'position; force-majeure slid pick from LAYER2::attribution).',

    statistic='r_i = V_N(i) / posv_i ;  RAW(N) = mean_i r_i ;  D(N) = RAW(N)/RAW(1). The depth-1 '
              'normalisation cancels every level offset between the outcome basis and the price basis '
              '(different stores, different SCALE, numeraire 0.94009) and leaves only the CONDITIONAL '
              'effect of having sat. RAW(1) is published so the offset is visible.',

    window_fit='entry_year in [2004, 2021] -- the DV lane\'s core (<=2014) + augmented (2015-2021) tiers',
    window_sensitivity='entry_year >= 2022 -- EXCLUDED from every fitted number; separate panel only',
    censor_depth='a row enters the depth-N cell only if seasons k=1..N-1 are COMPLETED (entry_year + '
                 'N - 1 <= %d)' % LAST_COMPLETE,
    censor_tail='a cell with mean tail share > 0.50 is flagged NOT USABLE AS EVIDENCE (mostly the '
                'engine\'s own projection of the very players in question -- circular)',
    censor_listing='LIST MEMBERSHIP IS NOT OBSERVABLE IN LAYER 1 (last_listed is non-null on 3 of 1,448 '
                   'ND rows). A player delisted after two gameless seasons is therefore still counted '
                   'in the depth-3 and depth-4 cells at zero delivered value. This makes reading ALL a '
                   'HARSH (lower) bound. The generous (upper) bound EVER-PLAYED restricts each cell to '
                   'entrants who played >=1 AFL game at some point -- that is selection on the outcome '
                   'and is published as a BOUND, never as the recommendation. The truth is between.',

    robustness_W=dict(
        what='WINSORISATION OF THE PER-PLAYER RATIO AT 2.0 -- a ROBUSTNESS READING, not the primary.',
        declared='NOT prestated in PREREG_30A.md; added AFTER the first run and published BESIDE the '
                 'prestated primary, which is unchanged and remains the recommendation.',
        borrowed='winsor 2.0 is ORDER 21 / the pool psi construction\'s OWN guard '
                 '(POOL_RETENTION_SURFACE.json::meta.winsor = 2.0), reused verbatim rather than '
                 'invented here.',
        what_it_showed='It bites 192 of the 1,140 depth-1 rows and cuts RAW(1) by 40 %, because the '
                       'right tail it truncates is NOT an artefact -- it is jordan-dawson (pick 55), '
                       'thomas-stewart (40), errol-gulden (34), harris-andrews (59): real late-pick '
                       'stars. It is therefore NOT adopted as the primary. What matters is that the '
                       'NORMALISED discount D(N) moves by less than 0.04 at every depth under it: the '
                       'derived surface is robust to the whole right tail.',
        verdict='ROBUSTNESS ONLY. The prestated un-winsorised surface is the recommendation.',
    ),
    winsor=2.0,

    K_shrink=15.0,
    K_shrink_note='borrowed from the delivered-value lane (K=15). shrunk = (n*cell + K*allpick)/(n+K) '
                  'at the SAME depth; the borrowing fraction K/(n+K) is disclosed on every cell.',

    pick_bands=[(1, 20), (21, 40), (41, 64)],
    positions=['KPD', 'KPF', 'MID', 'RUCK', 'SD', 'SF'],
    position_collapse='KPP+RUCK = {KPF,KPD,RUCK} (the three the old schedule grants a 2.5-year grace) '
                      'vs nonKPP = {MID,SD,SF} (grace 1.0)',

    old_schedule=dict(
        source='engine/rl_after/rl_model.py:725-729, read LIVE off the imported module',
        LOS_C=float(MA.LOS_C), LOS_P=float(MA.LOS_P), GRACE=dict(MA.GRACE),
        form='los_decay = exp(-LOS_C * max(0, s - GRACE[gfut])**LOS_P)',
        axis='gfut -- the PLAYED position axis. This act\'s denominator uses day0_position (the '
             'ACQUISITION slot, Ruling 5). For a 0-game player the two coincide; disclosed regardless.',
    ),
)

BARS = {g: MA.REPL[g] - rd.REPL_DROP.get(g, 0.0) for g in MA.REPL}
CFG['bars_live_store'] = {g: round(BARS[g], 4) for g in sorted(BARS)}
CFG['scale_live_store'] = float(MA.SCALE)


def los_decay_at(group, s):
    """THE OLD SCHEDULE, evaluated from the engine's own constants."""
    over = max(0.0, s - MA.GRACE.get(group, 1.0))
    return math.exp(-MA.LOS_C * over ** MA.LOS_P)


# =====================================================================================================
# POPULATION
# =====================================================================================================
ENTRIES = L1['entries']
SEASONS = collections.defaultdict(list)
for s in L1['player_seasons']:
    SEASONS[s['key']].append(s)
for k in SEASONS:
    SEASONS[k].sort(key=lambda x: x['year'])

ATTR = L2['attribution']
GA = L2['grace_a']            # PRIMARY basis
BASE = L2['base']             # flat-14 sensitivity


def entry_age(e):
    a = e['entry_age']
    return a if a is not None else e['entry_age_fallback_if_null']


def grace_A_G(a):
    return 2 if (a is not None and a <= 19) else 0


def DF(e, k):
    """The re-anchoring factor, through the ENGINE'S OWN disc_factor."""
    a = entry_age(e)
    return MA.disc_factor(a, MA.LENS['bal'], max(0, k - grace_A_G(a)), 'bal')


def DF_flat(e, k):
    return MA.disc_factor(entry_age(e), MA.LENS['bal'], max(0, k), 'bal')


def games_in(key, year):
    g = 0.0
    for s in SEASONS.get(key, []):
        if s['year'] == year:
            g += s['games']
    return g


def leading_sit(e):
    """Number of leading COMPLETED gameless seasons from k=1. maxdepth = 1 + that."""
    ey = e['entry_year']
    n = 0
    k = 1
    while ey + k <= LAST_COMPLETE:
        if games_in(e['key'], ey + k) > 0:
            break
        n += 1
        k += 1
    return n


def ever_played(e):
    return any(s['games'] > 0 for s in SEASONS.get(e['key'], []))


POP = []
for e in ENTRIES:
    a = ATTR.get(e['key'])
    if not a or a.get('excluded'):
        continue
    if a.get('mechanism') != 'ND 1-64':
        continue
    if e['type'] != 'ND':
        continue
    pk = a['pick']
    g0 = e['day0_position']
    if g0 not in POSV or str(pk) not in POSV[g0]:
        continue
    v0 = float(POSV[g0][str(pk)])
    ey = e['entry_year']
    if ey is None:
        continue
    rec = dict(key=e['key'], entry_year=ey, pick=pk, natural_pick=a['natural_pick'], slid=a['slid'],
               pos=g0, v0=v0, entry_age=entry_age(e), retired=e['retired'],
               tier=e['window_tier'], maxdepth=1 + leading_sit(e), ever=ever_played(e),
               ga_total=float(GA[e['key']]['total']), ga_obs=float(GA[e['key']]['obs']),
               ga_tail=float(GA[e['key']]['tail']), ga_tshare=float(GA[e['key']]['tail_share']),
               base_total=float(BASE[e['key']]['total']),
               e=e)
    POP.append(rec)

FIT = [r for r in POP if 2004 <= r['entry_year'] <= 2021]
SENS = [r for r in POP if r['entry_year'] >= 2022]
PRE = [r for r in POP if r['entry_year'] < 2004]

P('POPULATION  (ND, attributed mechanism "ND 1-64", priceable on the landed entry law)')
P('  total ND 1-64 rows carried            %5d' % len(POP))
P('  FITTED window  2004-2021              %5d   (core <=2014 %d + augmented 2015-2021 %d)'
  % (len(FIT), sum(1 for r in FIT if r['entry_year'] <= 2014), sum(1 for r in FIT if r['entry_year'] >= 2015)))
P('  SENSITIVITY    2022+   (EXCLUDED)     %5d' % len(SENS))
P('  pre-2004       (EXCLUDED, DV floor)   %5d' % len(PRE))
P('  v0 == 0 rows in fitted window         %5d   (the RUCK pick 63/64 floor -- dropped from ratios)'
  % sum(1 for r in FIT if r['v0'] <= 0))
P('')

FIT = [r for r in FIT if r['v0'] > 0]
SENS = [r for r in SENS if r['v0'] > 0]


# =====================================================================================================
# CELL STATISTICS
# =====================================================================================================
def q(xs, f):
    if not xs:
        return None
    ys = sorted(xs)
    if len(ys) == 1:
        return ys[0]
    i = f * (len(ys) - 1)
    lo = int(math.floor(i)); hi = int(math.ceil(i))
    return ys[lo] + (ys[hi] - ys[lo]) * (i - lo)


WINSOR = 2.0


def cell(rows, N, basis='grace_a', anchor='now', winsor=False):
    """rows must ALREADY be the depth-N members. Returns the full disclosure dict."""
    if not rows:
        return dict(n=0)
    rr = []
    num = 0.0; den = 0.0; ts = []; nw = 0
    for r in rows:
        tot = r['ga_total'] if basis == 'grace_a' else (
            r['base_total'] if basis == 'flat14' else r['ga_obs'])
        if anchor == 'now':
            f = DF(r['e'], N - 1) if basis != 'flat14' else DF_flat(r['e'], N - 1)
        else:
            f = 1.0
        v = tot * f
        x = v / r['v0']
        if winsor and x > WINSOR:
            x = WINSOR; nw += 1
        rr.append(x)
        num += v; den += r['v0']
        ts.append(r['ga_tshare'])
    return dict(n=len(rr), mean=sum(rr) / len(rr), median=q(rr, 0.5), p25=q(rr, 0.25), p75=q(rr, 0.75),
                pooled=(num / den if den else None), tail_share=sum(ts) / len(ts),
                n_zero=sum(1 for x in rr if x <= 1e-12), n_winsorised=nw,
                n_ever=sum(1 for r in rows if r['ever']))


def at_depth(rows, N):
    return [r for r in rows if r['maxdepth'] >= N and (r['entry_year'] + N - 1) <= LAST_COMPLETE]


DEPTHS = [1, 2, 3, 4, 5, 6]


def surface(rows, basis='grace_a', anchor='now', ever_only=False, winsor=False):
    src = [r for r in rows if (r['ever'] if ever_only else True)]
    out = {}
    for N in DEPTHS:
        out[N] = cell(at_depth(src, N), N, basis, anchor, winsor)
    return out


def normalise(surf):
    b = surf[1].get('mean')
    if not b:
        return {}
    return {k: (v['mean'] / b if v.get('n') else None) for k, v in surf.items()}


PRIMARY = surface(FIT)
PRIM_D = normalise(PRIMARY)

P('=' * 118)
P('THE ALL-PICK ROW  --  PRIMARY BASIS (grace-A, re-anchored to the valuation moment), FITTED WINDOW')
P('=' * 118)
P('  depth      n   n=0   ever  RAW mean   median      p25      p75   pooled  tailshr   D(N)=RAW/RAW(1)   old los_decay')
for N in DEPTHS:
    c = PRIMARY[N]
    if not c.get('n'):
        P('  %-6s %5d   -- cell empty --' % (N, 0)); continue
    old_non = los_decay_at('MID', N); old_kpp = los_decay_at('RUCK', N)
    P('  %-6s %5d %5d %6d  %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f        %8.4f      %.3f / %.3f'
      % (N, c['n'], c['n_zero'], c['n_ever'], c['mean'], c['median'], c['p25'], c['p75'],
         c['pooled'], c['tail_share'], PRIM_D[N], old_non, old_kpp))
P('  (old los_decay column: non-KPP grace 1.0 / KPP+RUCK grace 2.5)')
P('')

# ---- DECLARED DEPARTURE D1: the winsorised surface -------------------------------------------------
WSURF = surface(FIT, winsor=True)
WD = normalise(WSURF)
P('ROBUSTNESS W  --  THE SAME ROW, PER-PLAYER RATIO WINSORISED AT %.1f (ORDER 21\'s own guard)' % WINSOR)
P('  NOT prestated; published BESIDE the primary, which is unchanged and remains the recommendation.')
P('  It bites 192 of the 1,140 depth-1 rows and cuts RAW(1) by 40%: the tail it truncates is REAL')
P('  (dawson pk55, stewart pk40, gulden pk34, andrews pk59), not an artefact -- so it is not adopted.')
P('  WHAT IT PROVES: the NORMALISED D(N) moves by less than 0.04 at every depth. The derived surface')
P('  does not depend on the right tail at all.')
P('  depth      n  n_wins   RAW mean   median      p25      p75   D_w(N)   old(nonKPP/KPP)')
for N in DEPTHS:
    c = WSURF[N]
    if not c.get('n'):
        continue
    P('  %-6s %5d %6d  %9.4f %8.4f %8.4f %8.4f %8.4f   %.3f / %.3f'
      % (N, c['n'], c['n_winsorised'], c['mean'], c['median'], c['p25'], c['p75'], WD[N],
         los_decay_at('MID', N), los_decay_at('RUCK', N)))
P('')

# ---- the anomaly: which rows blow up, and why ------------------------------------------------------
BLOW = []
for r in FIT:
    x = r['ga_total'] * DF(r['e'], 0) / r['v0']
    if x > WINSOR:
        BLOW.append((x, r))
BLOW.sort(key=lambda t: -t[0])
P('ANOMALY A1  --  the right tail is REAL. Rows with per-player ratio > %.1f at depth 1: %d of %d.'
  % (WINSOR, len(BLOW), PRIMARY[1]['n']))
P('  %-24s %-5s %5s %10s %12s %8s' % ('key', 'pos', 'pick', 'landed v0', 'delivered', 'ratio'))
for x, r in BLOW[:12]:
    P('  %-24s %-5s %5d %10.1f %12.1f %8.2f' % (r['key'], r['pos'], r['pick'], r['v0'], r['ga_total'], x))
P('  These are late-pick stars, not artefacts. The distribution of ND outcomes is a spike at zero plus')
P('  a very long right tail; both belong in an expectation, which is why the MEAN is the right')
P('  statistic for a price and the median (0.15 at depth 1) is not.')
P('')

# ---- ANOMALY A2: the deep tail of the positional entry law ------------------------------------------
P('ANOMALY A2  --  the positional entry law goes to ~0 in its own deep tail, so ANY delivery there')
P('  reads as a huge ratio. Landed nd_v0.posv at the last picks:')
for g in CFG['positions']:
    P('    %-5s %s' % (g, '  '.join('pk%d=%.0f' % (p, float(POSV[g][str(p)])) for p in (50, 55, 60, 62, 63, 64))))
P('  The ORDER-29 artifact declares this about itself (nd_v0.ruck_floor_63_64: "THE FLOOR VALUE IS')
P('  ZERO ... a thin-cell artefact of the last two picks"). CONSEQUENCE FOR THIS ACT: the RUCK')
P('  position cells at depth 5-6 read D_raw 1.20 and 1.56 -- a six-year sitter apparently worth MORE')
P('  than a fresh entrant. That is the denominator, not the evidence, and it is the single clearest')
P('  demonstration that the POSITION LENS carries no usable signal at depth.')
P('')

# ---- census by entry class -------------------------------------------------------------------------
P('CENSUS  --  depth-cell membership by entry class (fitted window). Deep cells are OLD classes.')
P('  depth   n    entry-year span    median entry year   %% from core (<=2014)')
for N in DEPTHS:
    rows = at_depth(FIT, N)
    if not rows:
        continue
    ys = sorted(r['entry_year'] for r in rows)
    P('  %-6s %4d   %d-%d          %d               %.0f%%'
      % (N, len(rows), ys[0], ys[-1], ys[len(ys) // 2],
         100.0 * sum(1 for r in rows if r['entry_year'] <= 2014) / len(rows)))
P('')

# ---- sensitivities ----------------------------------------------------------------------------------
SENSES = collections.OrderedDict()
SENSES['S1 day-0 anchored (no re-anchor)'] = normalise(surface(FIT, 'grace_a', 'day0'))
SENSES['S2 flat-14 basis (DV operative)'] = normalise(surface(FIT, 'flat14', 'now'))
SENSES['S3 observed leg only (no tail)'] = normalise(surface(FIT, 'obs', 'now'))
SENSES['S4 core window only (<=2014)'] = normalise(surface([r for r in FIT if r['entry_year'] <= 2014]))
SENSES['S5 EVER-PLAYED bound (generous)'] = normalise(surface(FIT, 'grace_a', 'now', ever_only=True))

P('SENSITIVITIES  --  D(N) on each alternative basis (all-pick row, fitted window)')
P('  %-38s %8s %8s %8s %8s %8s' % ('basis', 'D(2)', 'D(3)', 'D(4)', 'D(5)', 'D(6)'))
P('  %-38s %8.4f %8.4f %8.4f %8.4f %8.4f' % ('PRIMARY grace-A re-anchored',
   PRIM_D[2] or 0, PRIM_D[3] or 0, PRIM_D[4] or 0, PRIM_D[5] or 0, PRIM_D[6] or 0))
for lab, s in SENSES.items():
    P('  %-38s %8s %8s %8s %8s %8s' % (lab,
      *['%8.4f' % s[k] if s.get(k) else '     n/a' for k in (2, 3, 4, 5, 6)]))
P('')

# ---- LENS 2: pick bands ------------------------------------------------------------------------------
K = CFG['K_shrink']
BANDS = CFG['pick_bands']
PICK = {}
P('=' * 118)
P('LENS 2  --  DRAFT PICK.  raw cell, then K-shrunk toward the all-pick row at the SAME depth (K=%.0f)' % K)
P('=' * 118)
P('  depth  band        n   RAW mean   median      p25      p75   D_raw   D_shrunk  | D_w_raw D_w_shrunk  borrow%   old')
for N in DEPTHS:
    base = PRIMARY[1]['mean']; wbase = WSURF[1]['mean']
    allc = PRIMARY[N]; wallc = WSURF[N]
    if not allc.get('n'):
        continue
    for (lo, hi) in BANDS:
        rows = [r for r in at_depth(FIT, N) if lo <= r['pick'] <= hi]
        c = cell(rows, N); w = cell(rows, N, winsor=True)
        key = '%d|%d-%d' % (N, lo, hi)
        if not c.get('n'):
            PICK[key] = dict(n=0)
            P('  %-6s %-7s %5d   -- empty --' % (N, '%d-%d' % (lo, hi), 0)); continue
        draw = c['mean'] / base
        dshr = ((c['n'] * c['mean'] + K * allc['mean']) / (c['n'] + K)) / base
        wraw = w['mean'] / wbase
        wshr = ((w['n'] * w['mean'] + K * wallc['mean']) / (w['n'] + K)) / wbase
        borrow = K / (c['n'] + K)
        c.update(D_raw=draw, D_shrunk=dshr, D_w_raw=wraw, D_w_shrunk=wshr,
                 n_winsorised=w['n_winsorised'], borrow=borrow, band=[lo, hi], depth=N)
        PICK[key] = c
        P('  %-6s %-7s %5d  %8.4f %8.4f %8.4f %8.4f %7.4f   %8.4f  | %7.4f %10.4f  %5.1f%%  %.3f'
          % (N, '%d-%d' % (lo, hi), c['n'], c['mean'], c['median'], c['p25'], c['p75'],
             draw, dshr, wraw, wshr, 100 * borrow, los_decay_at('MID', N)))
P('')

# ---- LENS 3: position --------------------------------------------------------------------------------
POSCELL = {}
P('=' * 118)
P('LENS 3  --  POSITION (acquisition slot).  six groups, then the ruled collapse')
P('=' * 118)
P('  depth  pos        n   RAW mean   median   D_raw   D_shrunk  | D_w_raw D_w_shrunk  borrow%   old')
for N in DEPTHS:
    base = PRIMARY[1]['mean']; wbase = WSURF[1]['mean']
    allc = PRIMARY[N]; wallc = WSURF[N]
    if not allc.get('n'):
        continue
    for g in CFG['positions'] + ['KPP+RUCK', 'nonKPP']:
        if g == 'KPP+RUCK':
            rows = [r for r in at_depth(FIT, N) if r['pos'] in ('KPF', 'KPD', 'RUCK')]
        elif g == 'nonKPP':
            rows = [r for r in at_depth(FIT, N) if r['pos'] in ('MID', 'SD', 'SF')]
        else:
            rows = [r for r in at_depth(FIT, N) if r['pos'] == g]
        c = cell(rows, N); w = cell(rows, N, winsor=True)
        key = '%d|%s' % (N, g)
        if not c.get('n'):
            POSCELL[key] = dict(n=0); continue
        draw = c['mean'] / base
        dshr = ((c['n'] * c['mean'] + K * allc['mean']) / (c['n'] + K)) / base
        wraw = w['mean'] / wbase
        wshr = ((w['n'] * w['mean'] + K * wallc['mean']) / (w['n'] + K)) / wbase
        c.update(D_raw=draw, D_shrunk=dshr, D_w_raw=wraw, D_w_shrunk=wshr,
                 n_winsorised=w['n_winsorised'], borrow=K / (c['n'] + K), pos=g, depth=N)
        POSCELL[key] = c
        oldg = 'RUCK' if g in ('KPF', 'KPD', 'RUCK', 'KPP+RUCK') else 'MID'
        P('  %-6s %-9s %5d  %8.4f %8.4f %7.4f   %8.4f  | %7.4f %10.4f  %5.1f%%  %.3f'
          % (N, g, c['n'], c['mean'], c['median'], draw, dshr, wraw, wshr, 100 * c['borrow'],
             los_decay_at(oldg, N)))
P('')

# ---- the 2022+ sensitivity panel ---------------------------------------------------------------------
P('=' * 118)
P('SENSITIVITY PANEL  --  entry_year >= 2022.  EXCLUDED FROM EVERY FITTED NUMBER (CENSOR-1).')
P('=' * 118)
SENSSURF = surface(SENS)
P('  depth      n   RAW mean   tailshr   usable?')
for N in DEPTHS:
    c = SENSSURF[N]
    if not c.get('n'):
        continue
    P('  %-6s %5d  %8.4f  %8.4f   %s' % (N, c['n'], c['mean'], c['tail_share'],
      'NO -- mean tail share > 0.50 (CENSOR-3): this is the engine projecting the very players in question'
      if c['tail_share'] > 0.5 else 'marginal'))
P('')

# ---- the 29B reinflated rows -------------------------------------------------------------------------
D29 = {r['key']: r for r in DAY0['rows']}
E1_ALL = {e['key']: e for e in ENTRIES}
REIN = [r for r in POP if r['maxdepth'] >= 2 and r['key'] in D29]
ALL89 = []
for k in D29:
    e = E1_ALL.get(k)
    if e is None or e['entry_year'] is None:
        continue
    if (1 + leading_sit(e)) >= 2:
        ALL89.append((k, e['type'], e['entry_year']))
P('THE 29B REINFLATED ROWS  (0-career-game rows the flat-v0 keying returned to full v0)')
P('  wired rows on the 29B day-0 print     : %d  (fresh ND %d + pool %d)'
  % (DAY0['n_wired'], DAY0['n_fresh_nd'], DAY0['n_pool']))
P('  year-2+ sitters across ALL wired rows  : %d   (of which ND 1-64 %d, pool %d)'
  % (len(ALL89), len(REIN), len(ALL89) - len(REIN)))
P('  of those, in the 2022+ sensitivity tier: %d  (contribute NOTHING to any fitted number)'
  % sum(1 for (k, t, y) in ALL89 if y >= 2022))
P('  ND 1-64 year-2+ sitters in 2022+ tier  : %d of %d'
  % (sum(1 for r in REIN if r['entry_year'] >= 2022), len(REIN)))
P('')

# =====================================================================================================
# SECONDARY -- METHOD SYMMETRY WITH THE POOL psi/ORDER-21 CONSTRUCTION
# The pool divides by a SAME-DEPTH norm over all cells at that depth; this act normalises on the
# depth-1 baseline.  Reproducing the pool's norm on ND needs a per-season decomposition of the
# delivered-value scorer for NON-sitters too.  That is computed HERE on the LIVE store, with the DV
# lane's own season scorer text, so the store cancels inside the ratio.  OBSERVED LEG ONLY -- a
# projected tail cannot be attributed to a season that has not happened.
# =====================================================================================================
BYKEY = {}
for p in MA.data:
    kk = p.get('key') or MA.slug(p['player'])
    if kk not in BYKEY:
        BYKEY[kk] = p


def season_raw(X, pos):
    """DV lane o26b_layer2.py::season_raw, carried verbatim."""
    return MA.posval(X + MA.capt_prem(X) - BARS[pos]) * 21.0


def season_bar_group(pos_label, p):
    """DV lane o26b_layer2.py::season_bar_group, carried verbatim (the engine's own _fit_bar rule)."""
    if pos_label:
        es = MA._collapse_elig(str(pos_label).replace('/', ','))
        if es:
            return min(es, key=lambda x: MA.REPL[x])
    if p is not None:
        try:
            return MA._decl_bar(p)
        except Exception:
            pass
    return None


def obs_from_depth(r, N):
    """Observed delivered value from season N onward, discounted to the START OF YEAR N,
    on the live store.  Used ONLY for the pool-symmetric norm reading."""
    e = r['e']; ey = e['entry_year']; ea = r['entry_age']
    p = BYKEY.get(r['key'])
    tot = 0.0
    for s in SEASONS.get(r['key'], []):
        k = s['year'] - ey
        if k < N:
            continue
        g = season_bar_group(s['position_played'], p)
        if g is None or g not in BARS:
            continue
        w = min(1.0, math.sqrt(max(0.0, s['games']) / 10.0))
        d = MA.disc_factor(ea, MA.LENS['bal'], max(0, (k - (N - 1)) - grace_A_G(ea)), 'bal')
        tot += MA.SCALE * season_raw(s['avg'], g) * w / d
    return tot


P('=' * 118)
P('SECONDARY  --  THE POOL-SYMMETRIC (ORDER-21 / psi) READING, OBSERVED LEG, LIVE STORE')
P('=' * 118)
P('  pool construction: R(cls,d) = E[winsor(O/entry_anchor,2)| sit-out] / norm(cls,d),')
P('                     norm(cls,d) = E[winsor(O/entry_anchor,2)] over ALL cells at that depth.')
P('  ND analogue here : Rn(N) = E[obs_from_N / v0 | sitting at N] / E[obs_from_N / v0 | ALL entrants]')
P('  winsor 2.0 on the ratio, exactly as ORDER 21. Observed leg only, so both legs are like for like.')
P('')
WIN = 2.0
NORMREAD = {}
CORE = [r for r in FIT if r['entry_year'] <= 2014]   # complete-window, the pool's own discipline
P('  depth   n_sit  n_all   E[sit]   norm    Rn(N)   D(N) primary   old los_decay(nonKPP)')
for N in DEPTHS:
    allr = [r for r in CORE if (r['entry_year'] + N - 1) <= LAST_COMPLETE]
    sitr = [r for r in allr if r['maxdepth'] >= N]
    if len(sitr) < 1 or len(allr) < 1:
        continue
    va = [min(WIN, obs_from_depth(r, N) / r['v0']) for r in allr]
    vs = [min(WIN, obs_from_depth(r, N) / r['v0']) for r in sitr]
    norm = sum(va) / len(va); es = sum(vs) / len(vs)
    Rn = es / norm if norm else None
    NORMREAD[N] = dict(n_sit=len(vs), n_all=len(va), e_sit=es, norm=norm, Rn=Rn)
    P('  %-6s %6d %6d %8.4f %7.4f %8.4f       %8.4f   %.3f'
      % (N, len(vs), len(va), es, norm, Rn, PRIM_D[N] or 0, los_decay_at('MID', N)))
P('')
P('  ORDER-21 pool retention surface, for the side-by-side (whole_pool, depth 1..6):')
try:
    O21 = json.load(open(os.path.join(ROOT, 'docs/evidence/pool_retention_2026-08-12/POOL_RETENTION_SURFACE.json')))
    for cls in ('nonKPP', 'KPP', 'RUCK'):
        P('    %-7s %s' % (cls, '  '.join('%.3f' % x for x in O21['whole_pool'][cls])))
    CFG['order21_surface'] = O21['whole_pool']
except Exception as ex:
    P('    (not readable: %s)' % ex)
P('')

# =====================================================================================================
# NAMED TEST ROWS
# =====================================================================================================
NAMED_ND = ['josh-smillie', 'harry-demattia', 'max-knobel']
NAMED_POOL = ['harrison-ramm', 'mani-liddy', 'vigo-visentini']
E1 = {e['key']: e for e in ENTRIES}
BYK = {r['key']: r for r in POP}

# THE RECOMMENDED SURFACE: all-pick, depth-keyed, winsorised (departure D1), monotone-enforced
# downward by a running minimum -- a deeper sit may never be priced above a shallower one.
REC = {}
_run = None
for N in DEPTHS:
    if PRIM_D.get(N) is None:
        continue
    v = PRIM_D[N] if _run is None else min(_run, PRIM_D[N])
    REC[N] = v; _run = v
MONO_BREACH = [N for N in DEPTHS if PRIM_D.get(N) is not None and abs(REC[N] - PRIM_D[N]) > 1e-12]
P('THE RECOMMENDED SURFACE (prestated primary, all-pick, running-min monotone enforcement)')
P('  depth   D(N) raw   D_rec(N)   D_w(N) robustness   |D-D_w|   monotone repair?')
for N in DEPTHS:
    if N in REC:
        P('  %-6s %9.4f   %8.4f   %14.4f   %7.4f   %s'
          % (N, PRIM_D[N], REC[N], WD[N], abs(PRIM_D[N] - WD[N]), 'YES' if N in MONO_BREACH else '-'))
P('')


def rec_at(N):
    if N in REC:
        return REC[N]
    m = max(k for k in REC)
    return REC[m]


# ---- OPTIONAL: the OLD FUNCTIONAL FORM, RE-FITTED to the derived points ------------------------------
# Offered only for an owner who wants to keep exp(-C*over**P) rather than a five-row table. Grace is
# held at 1.0 for EVERY position (the derived two-way gap does not support 2.5 -- see the position lens).
_pts = [(N - 1.0, REC[N]) for N in DEPTHS if N in REC and N >= 2 and REC[N] > 0]
_x = [math.log(o) for o, d in _pts]
_y = [math.log(-math.log(d)) for o, d in _pts]
_mx = sum(_x) / len(_x); _my = sum(_y) / len(_y)
_sxy = sum((a - _mx) * (b - _my) for a, b in zip(_x, _y))
_sxx = sum((a - _mx) ** 2 for a in _x)
FIT_P = _sxy / _sxx
FIT_C = math.exp(_my - FIT_P * _mx)
P('OPTIONAL  --  THE OLD FUNCTIONAL FORM RE-FITTED (offered, NOT recommended over the table)')
P('  form kept: los_decay = exp(-C * max(0, s - GRACE)**P), GRACE = 1.0 for EVERY position')
P('  shipped   C = %.4f   P = %.4f   GRACE = KPF/KPD/RUCK 2.5, others 1.0' % (MA.LOS_C, MA.LOS_P))
P('  RE-FITTED C = %.4f   P = %.4f   GRACE = 1.0 everywhere' % (FIT_C, FIT_P))
P('  depth   D_rec(N)   refit    residual')
for N in DEPTHS:
    if N in REC and N >= 2:
        v = math.exp(-FIT_C * (N - 1.0) ** FIT_P)
        P('  %-6s %8.4f %8.4f %10.4f' % (N, REC[N], v, v - REC[N]))
P('  The re-fit is offered for continuity of form only. It misses the table by up to 0.05 in the')
P('  middle of the range; the five-row table IS the measurement and is what the seat recommends.')
P('')

BOARD = json.load(open(os.path.join(ROOT, 'engine/rl_after/rl_app_data.json')))
BROW = {r['key']: r for r in (BOARD['active'] + BOARD['back'])}

NAMED_OUT = []
P('=' * 118)
P('NAMED TEST ROWS  --  what each law says TODAY.  NOTHING IS WIRED; this is arithmetic on a packet.')
P('=' * 118)
P('  %-18s %-5s %-5s %-6s %8s %10s %10s %10s %10s' %
  ('player', 'pos', 'pick', 'depth', '29B flat', 'old los', 'DERIVED', 'D_pickband', 'basis'))
for k in NAMED_ND + NAMED_POOL:
    e = E1.get(k)
    d29 = D29.get(k)
    if e is None:
        continue
    N = NOW - e['entry_year']
    pos = e['day0_position']
    ispool = (e['type'] != 'ND')
    printed = d29['printed'] if d29 else None
    old = los_decay_at(pos, N)
    Dn = rec_at(N)
    band = None
    for (lo, hi) in BANDS:
        if e['pick'] and lo <= e['pick'] <= hi:
            band = '%d|%d-%d' % (N, lo, hi)
    Db = PICK.get(band, {}).get('D_shrunk') if band else None
    cg = sum(s['games'] for s in SEASONS.get(k, []))
    br = BROW.get(k, {})
    row = dict(key=k, pos=pos, pick=e['pick'], entry_year=e['entry_year'], depth=N,
               pathway=e['mechanism'], career_games=cg, printed_29b=printed,
               live_board_v=br.get('v'), live_board_losd=br.get('losd'),
               live_board_cg=br.get('cg'),
               old_los_decay=old, old_price=(round(printed * old) if printed else None),
               D_derived=(None if ispool else Dn),
               derived_price=(None if (ispool or printed is None) else round(printed * Dn)),
               D_pickband_shrunk=(None if ispool else Db),
               derived_price_pickband=(None if (ispool or printed is None or Db is None) else round(printed * Db)),
               pool_note=('POOL row -- carried for method-symmetry commentary only; no ND-derived '
                          'discount is applied to it in this act' if ispool else None))
    NAMED_OUT.append(row)
    P('  %-18s %-5s %-5s %-6s %8s %10s %10s %10s %10s'
      % (k, pos, e['pick'], N, printed if printed is not None else '--',
         ('%.3f/%s' % (old, row['old_price'])) if printed else '%.3f' % old,
         ('%.3f/%s' % (Dn, row['derived_price'])) if (printed and not ispool) else ('POOL' if ispool else '--'),
         ('%s' % row['derived_price_pickband']) if row['derived_price_pickband'] else '--',
         'grace-A' if not ispool else 'n/a'))
P('')

# =====================================================================================================
# WRITE
# =====================================================================================================
OUT = dict(
    act='ORDER 30A', read_only=True, cfg=CFG,
    pins=dict(layer1=L1_MD5, layer2=L2_MD5, **{k: PIN_OBS[k] for k in PIN_OBS}),
    population=dict(total=len(POP), fitted=len(FIT), sensitivity=len(SENS), pre2004=len(PRE),
                    fitted_core=sum(1 for r in FIT if r['entry_year'] <= 2014),
                    fitted_augmented=sum(1 for r in FIT if r['entry_year'] >= 2015)),
    allpick={str(N): PRIMARY[N] for N in DEPTHS},
    allpick_D={str(N): PRIM_D[N] for N in DEPTHS},
    allpick_winsorised={str(N): WSURF[N] for N in DEPTHS},
    allpick_D_winsorised={str(N): WD[N] for N in DEPTHS},
    recommended_surface={str(N): REC[N] for N in REC},
    refit_old_form=dict(shipped_C=float(MA.LOS_C), shipped_P=float(MA.LOS_P),
                        shipped_GRACE=dict(MA.GRACE), refit_C=FIT_C, refit_P=FIT_P,
                        refit_GRACE=1.0,
                        note='offered for continuity of functional form only; the five-row table is '
                             'the measurement and is what the seat recommends'),
    monotone_repairs=[str(N) for N in MONO_BREACH],
    anomaly_A1=[dict(key=r['key'], pos=r['pos'], pick=r['pick'], v0=r['v0'],
                     delivered=r['ga_total'], ratio=x) for x, r in BLOW[:40]],
    anomaly_A1_n=len(BLOW),
    sensitivities={lab: {str(k): v for k, v in s.items()} for lab, s in SENSES.items()},
    pick_lens=PICK, position_lens=POSCELL,
    sensitivity_panel_2022plus={str(N): SENSSURF[N] for N in DEPTHS},
    pool_symmetric={str(N): v for N, v in NORMREAD.items()},
    old_schedule={str(N): {g: los_decay_at(g, N) for g in CFG['positions']} for N in DEPTHS},
    named_rows=NAMED_OUT,
    reinflated_29b=dict(wired=DAY0['n_wired'], fresh_nd=DAY0['n_fresh_nd'], pool=DAY0['n_pool'],
                        year2plus_all_wired=len(ALL89), year2plus_nd=len(REIN),
                        year2plus_pool=len(ALL89) - len(REIN),
                        of_which_2022plus=sum(1 for (k, t, y) in ALL89 if y >= 2022)),
    per_player_fitted=[{k: v for k, v in r.items() if k != 'e'} for r in FIT],
)
with open(os.path.join(OUTD, 'SITTER_DISCOUNT_TABLE.json'), 'w') as f:
    json.dump(OUT, f, indent=1, sort_keys=True, default=float)
with open(os.path.join(OUTD, 'DERIVE30A_out.txt'), 'w') as f:
    f.write('\n'.join(LOG) + '\n')
print('\nwrote SITTER_DISCOUNT_TABLE.json and DERIVE30A_out.txt')
