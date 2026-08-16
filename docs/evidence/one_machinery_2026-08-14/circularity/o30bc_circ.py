#!/usr/bin/env python3
"""ORDER 30B-C -- THE CIRCULARITY DECOMPOSITION.

Answers the owner's suspicion, verbatim:

    "the raw or stalling players get to hold on to their pedigree much longer, a value propped up by
     the pedigree players of the past who went on to achieve something - and I suspect those players
     are the sharp tier guys who played early and well."

Three measurements, all on the COMMITTED 30B-M panel, which this harness re-derives by exec'ing the
committed harness verbatim up to its `q1 = {}` line (md5 asserted).  NOTHING of 30B-M's arithmetic is
retyped: build_states / panel / ols / cluster_se / band_fit / remaining are the committed callables.

    M1  the delivery decomposition -- an EXACT (Frisch-Waugh-Lovell) split of the committed band
        coefficient beta_b by who delivered it: breakout / slow-bloom / bust, within pick tiers.
    M2  the stall-persistence question -- what continued stallers measured forward, against what the
        wired additive law pays them.
    M3  the wired-law check along historical stall paths -- the law's pedigree pay year by year
        against the stall cohort's own measured pedigree contribution, with named real players.

READ-ONLY.  NOTHING WIRES.  Writes only CIRCULARITY.json and CIRC_out.txt in this directory.

  usage:  python3 o30bc_circ.py
"""
import os, sys, io, json, math, hashlib, contextlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
MEASURE = os.path.join(ROOT, 'docs', 'evidence', 'pedigree_persistence_2026-08-14', 'o30bm_measure.py')
READINGP = os.path.join(ROOT, 'docs', 'evidence', 'one_machinery_2026-08-14', 'resolution', 'READING.json')
RESOLVEDP = os.path.join(ROOT, 'docs', 'evidence', 'one_machinery_2026-08-14', 'resolution', 'RESOLVED_ROWS.json')
OUT_JSON = os.path.join(HERE, 'CIRCULARITY.json')
OUT_TXT = os.path.join(HERE, 'CIRC_out.txt')

MEASURE_MD5 = 'e910fe6482ab7b05a92f18c173667073'          # PINNED in PREREG_30BC s1
BOOT_SEED = 30_160_816                                     # declared in the prereg's spirit; fixed here

_LOG = []
def P(s=''):
    print(s)
    _LOG.append(str(s))


def md5f(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


# ==================================================================================================
# REUSE THE COMMITTED HARNESS -- verbatim prefix, md5 asserted
# ==================================================================================================
assert md5f(MEASURE) == MEASURE_MD5, '30B-M HARNESS PIN BROKEN: %s' % md5f(MEASURE)
SRC = open(MEASURE).read()
MARK = '\nq1 = {}\n'
assert MARK in SRC, 'split marker not found in the committed harness'
PREFIX = SRC.split(MARK)[0]

G = {'__file__': MEASURE, '__name__': 'o30bm_reused'}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(PREFIX, MEASURE, 'exec'), G)

np = G['np']
ROWS = G['ROWS']                    # the committed primary panel (H=6)
STATES = G['STATES']; PTS = G['PTS']
SEA = G['SEA']; ENT = G['ENT']; BARS = G['BARS']
POSES = G['POSES']; GAMES_BANDS = G['GAMES_BANDS']
band_fit = G['band_fit']; ols = G['ols']; remaining = G['remaining']
bar_group = G['bar_group']; q = G['q']; disp = G['disp']
PINS = G['PINS']

P('=' * 118)
P('ORDER 30B-C -- THE CIRCULARITY DECOMPOSITION.   READ-ONLY.  NOTHING WIRES.')
P('=' * 118)
P('committed 30B-M harness md5 : %s  (PINNED, asserted)' % MEASURE_MD5)
P('layer1 md5                  : %s' % PINS['layer1'])
P('v0 artifact md5             : %s' % PINS['v0_artifact'])
P('board md5                   : %s' % PINS['board'])

# ---- CONTROL: the panel and the five committed coefficients ---------------------------------------
NCAR = len({r['key'] for r in ROWS})
P('\nCONTROL -- panel re-derived: %d states over %d careers' % (len(ROWS), NCAR))
assert len(ROWS) == 4033 and NCAR == 767, 'PANEL CONTROL FAILED: %d / %d' % (len(ROWS), NCAR)

PTABLEP = os.path.join(ROOT, 'docs', 'evidence', 'pedigree_persistence_2026-08-14', 'PERSISTENCE_TABLE.json')
COMMITTED = json.load(open(PTABLEP))['q1_persistence']['band_fits']
P('committed PERSISTENCE_TABLE.json md5: %s' % md5f(PTABLEP))
BANDFIT = {}
CTRL = {}
for nm, lo, hi in GAMES_BANDS:
    rb = [r for r in ROWS if r['gb'] == nm]
    BANDFIT[nm] = band_fit(rb)
    dev = abs(BANDFIT[nm]['beta_v0'] - COMMITTED[nm]['beta_v0'])
    devs = abs(BANDFIT[nm]['sigma'] - COMMITTED[nm]['sigma'])
    CTRL[nm] = dict(beta=BANDFIT[nm]['beta_v0'], committed=COMMITTED[nm]['beta_v0'], dev=dev, dev_sigma=devs)
    P('  band %-6s n %4d  beta %.14f  (committed %.14f, dev %.2e ; sigma dev %.2e)'
      % (nm, len(rb), BANDFIT[nm]['beta_v0'], COMMITTED[nm]['beta_v0'], dev, devs))
    assert dev < 1e-9 and devs < 1e-9, 'BAND COEFFICIENT CONTROL FAILED at %s' % nm
    assert COMMITTED[nm]['n'] == len(rb), 'band n control failed at %s' % nm

# ---- the wired law's beta(g): the 30B-R object, read from the committed artifact -------------------
RD = json.load(open(READINGP))
BPTS = [tuple(x) for x in RD['beta_curve']['points']]


def beta_wired(g):
    """READING.json's beta curve: log-linear in log(games) between band midpoints, flat outside.
    Identical to o30br_resolved.py::beta_at (asserted below against the committed resolved rows)."""
    g = max(1e-6, float(g))
    if g <= BPTS[0][0]:
        return BPTS[0][1]
    if g >= BPTS[-1][0]:
        return BPTS[-1][1]
    for i in range(1, len(BPTS)):
        g0, b0 = BPTS[i - 1]; g1, b1 = BPTS[i]
        if g0 <= g <= g1:
            t = (math.log(g) - math.log(g0)) / (math.log(g1) - math.log(g0))
            return math.exp(math.log(b0) + t * (math.log(b1) - math.log(b0)))
    return BPTS[-1][1]


RR = json.load(open(RESOLVEDP))['rows']
NCHK = 0
for k, r in RR.items():
    if r.get('beta') is not None and r.get('games'):
        d = abs(beta_wired(r['games']) - r['beta'])
        assert d < 1e-12, 'beta_wired disagrees with the committed resolved row %s (%.3e)' % (k, d)
        NCHK += 1
P('\nbeta_wired(g) asserted against %d committed resolved rows to 1e-12  (e.g. kako g=36 -> %.6f)'
  % (NCHK, beta_wired(36.0)))

# ==================================================================================================
# THE ATOMS -- delivered seasons, outcome classes, stall paths
# ==================================================================================================
DELIVERED = {}        # (key, year) -> bool
GAMES_Y = {}          # (key, year) -> games played that year
for k, ss in SEA.items():
    e = ENT.get(k)
    if e is None:
        continue
    fb = e['position_group']
    for s in ss:
        pos = bar_group(s['position_played'], fb)
        if pos not in BARS:
            continue
        GAMES_Y[(k, s['year'])] = float(s['games'])
        DELIVERED[(k, s['year'])] = bool(float(s['games']) >= 10.0 and float(s['avg']) >= BARS[pos])


def delivered(k, y):
    return DELIVERED.get((k, y), False)


def outcome_class(k, Y, H=6):
    if delivered(k, Y + 1) or delivered(k, Y + 2):
        return 'breakout'
    for j in range(3, H + 1):
        if delivered(k, Y + j):
            return 'slow-bloom'
    return 'bust'


def stall_k(k, Y, H=6):
    """number of CONSECUTIVE stall seasons starting at Y+1 (capped at H)."""
    n = 0
    for j in range(1, H + 1):
        if delivered(k, Y + j):
            break
        n += 1
    return n


TIERS = [('T1 1-20', 1, 20), ('T2 21-64', 21, 64)]
def tier_of(pk):
    return 'T1 1-20' if pk <= 20 else 'T2 21-64'


CLASSES = ['breakout', 'slow-bloom', 'bust']
LOWMID = ['0-5', '6-15', '16-35']

for r in ROWS:
    r['cls'] = outcome_class(r['key'], r['year'])
    r['tier'] = tier_of(r['pick'])
    r['k_stall'] = stall_k(r['key'], r['year'])
    r['bw'] = beta_wired(r['g'])
    r['law_ped'] = r['bw'] * r['v0']

RES = dict(order='30B-C', date='2026-08-16', read_only=True, nothing_wires=True,
           pins=dict(PINS, o30bm_measure=MEASURE_MD5),
           panel=dict(n_states=len(ROWS), n_careers=NCAR),
           definitions=dict(
               delivered_season='store row with games >= 10 AND avg >= BARS[bar-group played]; anything else (incl. no row) is a STALL season',
               breakout='>=1 delivered season in {Y+1,Y+2}',
               slow_bloom='no delivered season in {Y+1,Y+2}, >=1 in {Y+3..Y+6}',
               bust='no delivered season in {Y+1..Y+6}',
               tiers='T1 = effective_pick 1-20, T2 = 21-64',
               beta_wired='READING.json beta_curve, log-linear in log(g); the 30B-R additive law price = P + beta(g)*v0'),
           bars={g: BARS[g] for g in sorted(BARS)})

# ==================================================================================================
# M0 -- CLASS MIX  (prereg C2)
# ==================================================================================================
P('\n' + '=' * 118)
P('M0 -- THE CLASS MIX.  Who, sitting in a low/mid state, was about to play well?')
P('=' * 118)
P('%-8s %-10s %6s | %10s %10s %10s | %10s' % ('band', 'tier', 'n', 'breakout', 'slow-bloom', 'bust', 'mean v0'))
mix = {}
for gb in LOWMID + ['36-70', '71+']:
    for tn, lo, hi in TIERS:
        rb = [r for r in ROWS if r['gb'] == gb and r['tier'] == tn]
        if not rb:
            continue
        c = collections.Counter(r['cls'] for r in rb)
        mix['%s|%s' % (gb, tn)] = dict(n=len(rb), mean_v0=sum(r['v0'] for r in rb) / len(rb),
                                       **{cl: c.get(cl, 0) for cl in CLASSES})
        P('%-8s %-10s %6d | %5d %4.0f%% %5d %4.0f%% %5d %4.0f%% | %10.1f'
          % (gb, tn, len(rb), c['breakout'], 100 * c['breakout'] / len(rb),
             c['slow-bloom'], 100 * c['slow-bloom'] / len(rb), c['bust'], 100 * c['bust'] / len(rb),
             sum(r['v0'] for r in rb) / len(rb)))
    rb = [r for r in ROWS if r['gb'] == gb]
    c = collections.Counter(r['cls'] for r in rb)
    mix['%s|BOTH TIERS' % gb] = dict(n=len(rb), mean_v0=sum(r['v0'] for r in rb) / len(rb),
                                     **{cl: c.get(cl, 0) for cl in CLASSES})
    P('%-8s %-10s %6d | %5d %4.1f%% %5d %4.1f%% %5d %4.1f%% | %10.1f   <== band total'
      % (gb, 'BOTH', len(rb), c['breakout'], 100 * c['breakout'] / len(rb),
         c['slow-bloom'], 100 * c['slow-bloom'] / len(rb), c['bust'], 100 * c['bust'] / len(rb),
         sum(r['v0'] for r in rb) / len(rb)))
RES['class_mix'] = mix

# ==================================================================================================
# M1 -- THE DELIVERY DECOMPOSITION (exact, Frisch-Waugh-Lovell)
# ==================================================================================================
P('\n' + '=' * 118)
P('M1 -- THE DELIVERY DECOMPOSITION.  beta_b = SUM_i c_i,  c_i = v0~_i * R_i / SUM v0~^2   (EXACT)')
P('=' * 118)


def band_design(rows_b, with_v0):
    """the committed band_fit design, reproduced column for column (band_fit is the authority; this
    function exists only to be able to residualise v0 out of the SAME Z)."""
    n = len(rows_b)
    cols = [np.ones(n)]
    for p in POSES[1:]:
        cols.append(np.array([1.0 if r['pos'] == p else 0.0 for r in rows_b]))
    age = np.array([r['age'] for r in rows_b], float)
    o = np.array([r['o'] for r in rows_b], float)
    cur = np.array([r['cur'] for r in rows_b], float)
    cur3 = np.array([r['cur3'] for r in rows_b], float)
    gay = np.array([r['games_at_Y'] for r in rows_b], float)
    lg = np.array([math.log1p(r['g']) for r in rows_b], float)
    for v in [age, age ** 2, o, o ** 2, cur, cur3, gay, lg]:
        cols.append(v)
    if with_v0:
        cols.append(np.array([r['v0'] for r in rows_b], float))
    return np.column_stack(cols)


FWL = {}
for gb in LOWMID + ['36-70', '71+']:
    rb = [r for r in ROWS if r['gb'] == gb]
    Z = band_design(rb, with_v0=False)
    v0 = np.array([r['v0'] for r in rb], float)
    y = np.array([r['R'] for r in rb], float)
    bz = ols(Z, v0)
    v0t = v0 - Z @ bz
    denom = float(v0t @ v0t)
    c = (v0t * y) / denom
    bfwl = float(c.sum())
    dev = abs(bfwl - BANDFIT[gb]['beta_v0'])
    FWL[gb] = dict(beta_fwl=bfwl, beta_bandfit=BANDFIT[gb]['beta_v0'], identity_dev=dev)
    P('  band %-6s  beta(FWL) %.12f   beta(band_fit) %.12f   |dev| %.3e' % (gb, bfwl, BANDFIT[gb]['beta_v0'], dev))
    for j, r in enumerate(rb):
        r['c_fwl'] = float(c[j]); r['v0_tilde'] = float(v0t[j])
IDENT_MAX = max(v['identity_dev'] for v in FWL.values())
P('  MAX identity deviation across the five bands: %.3e' % IDENT_MAX)
RES['fwl_identity'] = dict(by_band=FWL, max_dev=IDENT_MAX)

THIN = []
dec = {}
P('')
P('%-7s %-9s %-11s %5s %8s %8s %10s | %9s %8s %8s %8s %7s | %9s %9s'
  % ('band', 'tier', 'class', 'n', 'signed%', 'gross%', 'pts/state', 'mean R6', 'p25', 'med', 'p75', 'zero%',
     'mean v0', 'mean v0~'))
for gb in LOWMID + ['36-70', '71+']:
    rb = [r for r in ROWS if r['gb'] == gb]
    bb = BANDFIT[gb]['beta_v0']
    gross_tot = sum(abs(r['c_fwl']) for r in rb)
    band_pts = bb * BANDFIT[gb]['mean_v0']          # the band's mean pedigree contribution, in points
    for tn, lo, hi in TIERS:
        rt = [r for r in rb if r['tier'] == tn]
        if not rt:
            continue
        for cl in CLASSES + ['ALL']:
            rc = rt if cl == 'ALL' else [r for r in rt if r['cls'] == cl]
            if not rc:
                continue
            if cl != 'ALL' and len(rc) < 8:
                THIN.append(dict(band=gb, tier=tn, cls=cl, n=len(rc)))
                continue
            sc = sum(r['c_fwl'] for r in rc)
            gc = sum(abs(r['c_fwl']) for r in rc)
            d = disp([r['R'] for r in rc])
            row = dict(d)
            row.update(n=len(rc), signed_share=sc / bb, gross_share=gc / gross_tot,
                       points_per_band_state=(sc / bb) * band_pts,
                       mean_v0=sum(r['v0'] for r in rc) / len(rc),
                       mean_v0_tilde=sum(r['v0_tilde'] for r in rc) / len(rc),
                       mean_law_ped=sum(r['law_ped'] for r in rc) / len(rc))
            dec['%s|%s|%s' % (gb, tn, cl)] = row
            P('%-7s %-9s %-11s %5d %7.1f%% %7.1f%% %10.1f | %9.1f %8.1f %8.1f %8.1f %6.1f%% | %9.1f %9.1f'
              % (gb, tn, cl, len(rc), 100 * row['signed_share'], 100 * row['gross_share'],
                 row['points_per_band_state'], d['mean'], d['p25'], d['median'], d['p75'],
                 100 * d['zero_share'], row['mean_v0'], row['mean_v0_tilde']))
    P('')
RES['decomposition'] = dec
RES['control_band_fits'] = CTRL
RES['thin_cells_collapsed'] = THIN

# ---- the same table normalised WITHIN tier (the C3 lens: who moves the tier's own coefficient) -----
P('\nWITHIN-TIER GROSS MASS SHARE (each tier normalised to its own gross |c| total) -- the C3 lens:')
P('%-7s %-9s %10s %12s %10s %10s' % ('band', 'tier', 'breakout', 'slow-bloom', 'bust', 'tier n'))
wt = {}
for gb in LOWMID + ['36-70', '71+']:
    for tn, lo, hi in TIERS:
        rt = [r for r in ROWS if r['gb'] == gb and r['tier'] == tn]
        tot = sum(abs(r['c_fwl']) for r in rt)
        if tot <= 0:
            continue
        row = {cl: sum(abs(r['c_fwl']) for r in rt if r['cls'] == cl) / tot for cl in CLASSES}
        row['n'] = len(rt)
        wt['%s|%s' % (gb, tn)] = row
        P('%-7s %-9s %9.1f%% %11.1f%% %9.1f%% %10d'
          % (gb, tn, 100 * row['breakout'], 100 * row['slow-bloom'], 100 * row['bust'], len(rt)))
RES['within_tier_gross_share'] = wt
P('THIN CELLS (n<8, collapsed into their tier ALL row, disclosed): %s'
  % (json.dumps(THIN) if THIN else 'NONE'))

# ---- pooled low/mid view: bust mass vs bust population (C4) ---------------------------------------
rlm = [r for r in ROWS if r['gb'] in LOWMID]
pool_gross = {}
for gb in LOWMID:
    rb = [r for r in ROWS if r['gb'] == gb]
    tot = sum(abs(r['c_fwl']) for r in rb)
    for cl in CLASSES:
        pool_gross[cl] = pool_gross.get(cl, 0.0) + sum(abs(r['c_fwl']) for r in rb if r['cls'] == cl) / tot * len(rb)
tot_lm = len(rlm)
P('\nPOOLED LOW/MID (0-5, 6-15, 16-35; n=%d states) -- gross beta-mass share vs population share,'
  % tot_lm)
P('  n-weighted across the three bands (each band normalised to its own gross mass first):')
P('  %-12s %10s %10s' % ('class', 'mass%', 'states%'))
poolrow = {}
for cl in CLASSES:
    ms = pool_gross[cl] / tot_lm
    ps = sum(1 for r in rlm if r['cls'] == cl) / tot_lm
    poolrow[cl] = dict(mass_share=ms, state_share=ps)
    P('  %-12s %9.1f%% %9.1f%%' % (cl, 100 * ms, 100 * ps))
RES['pooled_lowmid'] = poolrow

# ==================================================================================================
# M2 -- THE STALL-PERSISTENCE QUESTION
# ==================================================================================================
P('\n' + '=' * 118)
P('M2 -- THE STALL-PERSISTENCE QUESTION.  What do CONTINUED STALLERS measure forward, and what does')
P('     the wired additive law pay them?   (continued staller = no delivered season at Y+1 or Y+2)')
P('=' * 118)

# pick-blind residuals, band by band (the committed band_fit design MINUS v0)
for gb in LOWMID + ['36-70', '71+']:
    rb = [r for r in ROWS if r['gb'] == gb]
    Z = band_design(rb, with_v0=False)
    y = np.array([r['R'] for r in rb], float)
    b = ols(Z, y)
    res = y - Z @ b
    for j, r in enumerate(rb):
        r['resid_blind'] = float(res[j])

rng = np.random.default_rng(BOOT_SEED)


def boot_mean_ci(rows_g, field='resid_blind', nrep=300):
    """300-replicate player-cluster bootstrap on the subgroup mean."""
    if not rows_g:
        return None
    keys = sorted({r['key'] for r in rows_g})
    byk = collections.defaultdict(list)
    for r in rows_g:
        byk[r['key']].append(r[field])
    boots = []
    for _ in range(nrep):
        pick = rng.integers(0, len(keys), len(keys))
        vals = []
        for t in pick:
            vals.extend(byk[keys[t]])
        if vals:
            boots.append(sum(vals) / len(vals))
    boots.sort()
    return [q(boots, .05), q(boots, .95)]


P('%-7s %-9s %-14s %5s %6s | %9s %9s %9s %9s | %11s %13s'
  % ('band', 'tier', 'group', 'n', 'clust', 'mean R6', 'median', 'p75', 'zero%',
     'law pays', 'ped excess (90% CI)'))
stall = {}
for gb in LOWMID:
    for tn, lo, hi in TIERS:
        rt = [r for r in ROWS if r['gb'] == gb and r['tier'] == tn]
        groups = [('breakout', [r for r in rt if r['cls'] == 'breakout']),
                  ('cont. staller', [r for r in rt if r['cls'] != 'breakout']),
                  ('  of which bust', [r for r in rt if r['cls'] == 'bust'])]
        for gn, rg in groups:
            if len(rg) < 8:
                THIN.append(dict(band=gb, tier=tn, group=gn, n=len(rg)))
                P('%-7s %-9s %-14s %5d   THIN (n<8) -- collapsed, disclosed' % (gb, tn, gn, len(rg)))
                continue
            d = disp([r['R'] for r in rg])
            mres = sum(r['resid_blind'] for r in rg) / len(rg)
            ci = boot_mean_ci(rg)
            law = sum(r['law_ped'] for r in rg) / len(rg)
            key = '%s|%s|%s' % (gb, tn, gn.strip())
            srow = dict(d)
            srow.update(n=len(rg), n_clusters=len({r['key'] for r in rg}), mean_resid=mres,
                        resid_ci=ci, mean_law_ped=law, mean_v0=sum(r['v0'] for r in rg) / len(rg),
                        mean_beta_wired=sum(r['bw'] for r in rg) / len(rg))
            stall[key] = srow
            P('%-7s %-9s %-14s %5d %6d | %9.1f %9.1f %9.1f %8.1f%% | %11.1f %+7.1f (%+.0f..%+.0f)'
              % (gb, tn, gn, len(rg), len({r['key'] for r in rg}), d['mean'], d['median'], d['p75'],
                 100 * d['zero_share'], law, mres, ci[0], ci[1]))
    P('')
RES['stall_persistence'] = stall

# ---- the re-price: the same player two seasons later ----------------------------------------------
P('THE RE-PRICE -- continued stallers who played again at Y+2 (so a state exists there):')
P('%-7s %-9s %5s | %8s %8s %8s | %9s %9s %8s | %9s %9s'
  % ('band', 'tier', 'n', 'g at Y', 'g at Y+2', 'd g', 'beta(Y)', 'beta(Y+2)', 'ratio', 'law(Y)', 'law(Y+2)'))
STATE_BY = {}
for s in STATES:
    STATE_BY[(s['key'], s['year'])] = s
repr_ = {}
for gb in LOWMID:
    for tn, lo, hi in TIERS:
        rt = [r for r in ROWS if r['gb'] == gb and r['tier'] == tn and r['cls'] != 'breakout']
        pairs = []
        for r in rt:
            s2 = STATE_BY.get((r['key'], r['year'] + 2))
            if s2 is None:
                continue
            b2 = beta_wired(s2['g'])
            pairs.append((r, s2, b2))
        if len(pairs) < 8:
            THIN.append(dict(band=gb, tier=tn, group='reprice Y+2', n=len(pairs)))
            P('%-7s %-9s %5d   THIN (n<8) -- collapsed, disclosed' % (gb, tn, len(pairs)))
            continue
        g0 = sum(r['g'] for r, s2, b2 in pairs) / len(pairs)
        g2 = sum(s2['g'] for r, s2, b2 in pairs) / len(pairs)
        b0 = sum(r['bw'] for r, s2, b2 in pairs) / len(pairs)
        b2m = sum(b2 for r, s2, b2 in pairs) / len(pairs)
        l0 = sum(r['law_ped'] for r, s2, b2 in pairs) / len(pairs)
        l2 = sum(b2 * r['v0'] for r, s2, b2 in pairs) / len(pairs)
        relch = sorted(abs(b2 - r['bw']) / r['bw'] for r, s2, b2 in pairs)
        rose = sum(1 for r, s2, b2 in pairs if b2 > r['bw'])
        r6_2 = [remaining(r['key'], r['year'] + 2, 6, PTS) for r, s2, b2 in pairs if r['year'] + 2 <= 2019]
        repr_['%s|%s' % (gb, tn)] = dict(n=len(pairs), mean_g=g0, mean_g2=g2, mean_beta=b0, mean_beta2=b2m,
                                         mean_law=l0, mean_law2=l2,
                                         median_abs_rel_change=q(relch, .5), n_beta_rose=rose,
                                         n_r6_from_Y2=len(r6_2),
                                         mean_R6_from_Y2=(sum(r6_2) / len(r6_2)) if r6_2 else None,
                                         median_R6_from_Y2=q(r6_2, .5) if r6_2 else None)
        P('%-7s %-9s %5d | %8.1f %8.1f %8.1f | %9.4f %9.4f %8.3f | %9.1f %9.1f   [median |dbeta|/beta %.1f%%; beta ROSE for %d of %d; mean R6 from Y+2 %s on n=%d]'
          % (gb, tn, len(pairs), g0, g2, g2 - g0, b0, b2m, b2m / b0, l0, l2,
             100 * q(relch, .5), rose, len(pairs),
             ('%.1f' % (sum(r6_2) / len(r6_2))) if r6_2 else 'n/a', len(r6_2)))
RES['reprice'] = repr_

# ---- THE PURE CASE: continued stallers who barely played at all in Y+1..Y+2 -----------------------
# (M2's own words: "low games/output at s+1, s+2". This is the sub-lens where the games clock CANNOT
#  advance, so the wired beta(g) cannot re-price. Declared inside M2's scope, not discovered after.)
P('\nTHE PURE CASE -- continued stallers with FEWER THAN 10 GAMES TOTAL across Y+1 and Y+2')
P('(the games clock barely moves, so beta(g) cannot re-price them):')
P('%-7s %-9s %5s | %8s %8s | %9s %9s %8s | %11s %11s %9s %9s'
  % ('band', 'tier', 'n', 'g at Y', 'g at Y+2', 'beta(Y)', 'beta(Y+2)', 'ratio', 'law(Y)', 'law(Y+2)',
     'mean R6', 'med R6'))
pure = {}
for gb in LOWMID:
    for tn, lo, hi in TIERS:
        rt = [r for r in ROWS if r['gb'] == gb and r['tier'] == tn and r['cls'] != 'breakout']
        sub = []
        for r in rt:
            g2 = r['g'] + GAMES_Y.get((r['key'], r['year'] + 1), 0.0) + GAMES_Y.get((r['key'], r['year'] + 2), 0.0)
            if g2 - r['g'] < 10.0:
                sub.append((r, g2))
        if len(sub) < 8:
            THIN.append(dict(band=gb, tier=tn, group='pure staller <10g', n=len(sub)))
            P('%-7s %-9s %5d   THIN (n<8) -- collapsed, disclosed' % (gb, tn, len(sub)))
            continue
        g0 = sum(r['g'] for r, _ in sub) / len(sub)
        gg2 = sum(x for _, x in sub) / len(sub)
        b0 = sum(r['bw'] for r, _ in sub) / len(sub)
        b2 = sum(beta_wired(x) for _, x in sub) / len(sub)
        l0 = sum(r['law_ped'] for r, _ in sub) / len(sub)
        l2 = sum(beta_wired(x) * r['v0'] for r, x in sub) / len(sub)
        rr = [r['R'] for r, _ in sub]
        pure['%s|%s' % (gb, tn)] = dict(n=len(sub), mean_g=g0, mean_g2=gg2, beta=b0, beta2=b2,
                                        law=l0, law2=l2, mean_R6=sum(rr) / len(rr), median_R6=q(rr, .5),
                                        p75_R6=q(rr, .75))
        P('%-7s %-9s %5d | %8.1f %8.1f | %9.4f %9.4f %8.3f | %11.1f %11.1f %9.1f %9.1f'
          % (gb, tn, len(sub), g0, gg2, b0, b2, b2 / b0, l0, l2, sum(rr) / len(rr), q(rr, .5)))
RES['pure_staller'] = pure

# ---- WHO ACTUALLY COLLECTS: concentration inside the continued-staller cohort ----------------------
P('\nWHO COLLECTS -- inside the T1 (picks 1-20) continued-staller cohort, how concentrated is the')
P('realized value, and how many of them ever earn back even the law\'s pedigree top-up?')
P('%-7s %5s | %10s %12s %14s %16s'
  % ('band', 'n', 'top-10% R6', 'top-10% mass', 'R6 > law ped', 'R6 > 2x law ped'))
coll = {}
for gb in LOWMID:
    rg = [r for r in ROWS if r['gb'] == gb and r['tier'] == 'T1 1-20' and r['cls'] != 'breakout']
    if len(rg) < 8:
        continue
    rs = sorted(rg, key=lambda r: -r['R'])
    ntop = max(1, int(round(0.10 * len(rs))))
    tot = sum(r['R'] for r in rs)
    topm = sum(r['R'] for r in rs[:ntop])
    over = sum(1 for r in rg if r['R'] > r['law_ped'])
    over2 = sum(1 for r in rg if r['R'] > 2 * r['law_ped'])
    coll[gb] = dict(n=len(rg), n_top=ntop, top10_mass_share=(topm / tot if tot > 0 else None),
                    share_R6_over_law=over / len(rg), share_R6_over_2x_law=over2 / len(rg),
                    min_R6_in_top10=rs[ntop - 1]['R'])
    P('%-7s %5d | %10d %11.1f%% %13.1f%% %15.1f%%'
      % (gb, len(rg), ntop, 100 * topm / tot, 100 * over / len(rg), 100 * over2 / len(rg)))
RES['who_collects'] = coll

# ---- beta re-fitted on the stall subpopulation -----------------------------------------------------
P('\nBETA RE-FITTED ON THE STALL SUBPOPULATION (states whose Y+1 and Y+2 are both stall seasons).')
P('The committed band_fit refuses n<40; where it refuses, this order reports NO SIGNAL.')
P('%-7s %6s %8s %11s %8s %9s %20s' % ('band', 'n', 'clust', 'beta_stall', 't', 'sigma', 'sigma 90% CI'))
BSTALL = {}
for gb in LOWMID + ['36-70', '71+']:
    rs = [r for r in ROWS if r['gb'] == gb and r['cls'] != 'breakout']
    f = band_fit(rs)
    BSTALL[gb] = f
    if f is None:
        P('%-7s %6d   NO SIGNAL -- n < 40, the committed fitter refuses' % (gb, len(rs)))
        continue
    ci = f['sigma_ci']
    P('%-7s %6d %8d %11.5f %8.2f %8.1f%% %9.1f%% .. %-8.1f%%'
      % (gb, f['n'], f['n_clusters'], f['beta_v0'], f['t_v0'], 100 * f['sigma'], 100 * ci[0], 100 * ci[1]))
RES['beta_stall_by_band'] = {k: (v if v else 'NO SIGNAL (n<40)') for k, v in BSTALL.items()}

# also: beta re-fitted on the BREAKOUT subpopulation, for contrast
P('\nBETA RE-FITTED ON THE BREAKOUT SUBPOPULATION (contrast; same fitter, same rule):')
BBREAK = {}
for gb in LOWMID + ['36-70', '71+']:
    rs = [r for r in ROWS if r['gb'] == gb and r['cls'] == 'breakout']
    f = band_fit(rs)
    BBREAK[gb] = f
    if f is None:
        P('%-7s %6d   NO SIGNAL -- n < 40' % (gb, len(rs)))
        continue
    P('%-7s %6d %8d %11.5f %8.2f %8.1f%%' % (gb, f['n'], f['n_clusters'], f['beta_v0'], f['t_v0'],
                                             100 * f['sigma']))
RES['beta_breakout_by_band'] = {k: (v if v else 'NO SIGNAL (n<40)') for k, v in BBREAK.items()}

# ==================================================================================================
# M3 -- THE WIRED-LAW CHECK ALONG HISTORICAL STALL PATHS
# ==================================================================================================
P('\n' + '=' * 118)
P('M3 -- THE WIRED LAW ALONG HISTORICAL STALL PATHS (picks 1-20, low/mid states, k>=2 stall seasons)')
P('=' * 118)


def cohort_beta(gb):
    """what the stall cohort measured from a state in this band; falls back, LABELLED, to the whole
    band's committed beta where the stall band is not estimable."""
    f = BSTALL.get(gb)
    if f is not None:
        return f['beta_v0'], 'stall-cohort fit'
    return BANDFIT[gb]['beta_v0'], 'FALLBACK: whole-band beta (stall band not estimable)'


def band_of_g(g):
    for nm, lo, hi in GAMES_BANDS:
        if lo <= g <= hi:
            return nm
    return GAMES_BANDS[-1][0]


PATHS = []
for r in ROWS:
    if r['tier'] != 'T1 1-20' or r['gb'] not in LOWMID:
        continue
    if r['k_stall'] < 2:
        continue
    Y, k = r['year'], r['k_stall']
    steps = []
    gcum = r['g']
    for t in range(0, k + 1):
        if t > 0:
            gcum += GAMES_Y.get((r['key'], Y + t), 0.0)
        gb_t = band_of_g(gcum)
        cb, lab = cohort_beta(gb_t)
        bw = beta_wired(gcum)
        r6 = remaining(r['key'], Y + t, 6, PTS) if (Y + t) <= 2019 else None
        steps.append(dict(t=t, year=Y + t, g=gcum, games_this_year=(GAMES_Y.get((r['key'], Y + t), 0.0) if t > 0 else r['games_at_Y']),
                          beta_wired=bw, law_ped=bw * r['v0'], cohort_beta=cb, cohort_ped=cb * r['v0'],
                          gap=(bw - cb) * r['v0'], cohort_label=lab, R6=r6,
                          played=(r['key'], Y + t) in GAMES_Y))
    PATHS.append(dict(key=r['key'], year=Y, pick=r['pick'], pos=r['pos'], age=r['age'], g0=r['g'],
                      v0=r['v0'], gb=r['gb'], k=k, cls=r['cls'], R6_at_state=r['R'], steps=steps))
RES['n_paths'] = len(PATHS)
P('T1 (picks 1-20) low/mid states with k>=2 consecutive stall seasons: %d paths over %d careers'
  % (len(PATHS), len({p['key'] for p in PATHS})))

# ---- the gap path aggregated by k ------------------------------------------------------------------
P('\nTHE GAP PATH, aggregated over those paths (mean over paths that reach step t):')
P('%-6s %6s %10s %12s %14s %12s %12s | %11s %8s %12s'
  % ('step t', 'n', 'mean g', 'beta_wired', 'cohort beta', 'law pays', 'cohort says', 'GAP (pts)',
     'law/coh', 'GAP@coh>=0'))
gappath = {}
for t in range(0, 5):
    st = [p['steps'][t] for p in PATHS if len(p['steps']) > t]
    if len(st) < 8:
        THIN.append(dict(group='gap path step', t=t, n=len(st)))
        P('%-6s %6d   THIN (n<8) -- collapsed, disclosed' % (t, len(st)))
        continue
    mlaw = sum(s['law_ped'] for s in st) / len(st)
    mcoh = sum(s['cohort_ped'] for s in st) / len(st)
    # disclosure variant: where the stall cohort's beta is measured negative it is statistically
    # indistinguishable from zero (t = -0.29, -0.90 in the two deep bands); flooring it at zero is
    # reported BESIDE the primary, never instead of it.
    mcoh0 = sum(max(0.0, s['cohort_ped']) for s in st) / len(st)
    gappath[t] = dict(n=len(st), mean_g=sum(s['g'] for s in st) / len(st),
                      mean_beta_wired=sum(s['beta_wired'] for s in st) / len(st),
                      mean_cohort_beta=sum(s['cohort_beta'] for s in st) / len(st),
                      mean_law=mlaw, mean_cohort=mcoh,
                      mean_gap=sum(s['gap'] for s in st) / len(st),
                      median_gap=q([s['gap'] for s in st], .5),
                      law_over_cohort=(mlaw / mcoh if mcoh > 0 else None),
                      mean_cohort_floored=mcoh0, mean_gap_floored=mlaw - mcoh0)
    g = gappath[t]
    P('%-6d %6d %10.1f %12.4f %14.4f %12.1f %12.1f | %+11.1f %8s %+12.1f'
      % (t, g['n'], g['mean_g'], g['mean_beta_wired'], g['mean_cohort_beta'], g['mean_law'],
         g['mean_cohort'], g['mean_gap'],
         ('%.2fx' % g['law_over_cohort']) if g['law_over_cohort'] else '   n/a', g['mean_gap_floored']))
RES['gap_path'] = gappath

# ---- named historical paths -------------------------------------------------------------------------
def nice(k):
    return ' '.join(w.capitalize() for w in k.split('-'))


# The selection rule, fixed here and applied mechanically: the ten longest/highest-pedigree BUST paths
# (the overpaid), then the six paths with the LARGEST realized R6 from the state (the vindicated --
# players who stalled two or more seasons and still delivered). Both lists are named in full.
seen, shown = set(), []
for p in sorted([x for x in PATHS if x['cls'] == 'bust'], key=lambda p: (-p['k'], -p['v0'])):
    if p['key'] in seen:
        continue
    seen.add(p['key']); shown.append(p)
    if len(shown) >= 10:
        break
NBUST = len(shown)
for p in sorted(PATHS, key=lambda p: -p['R6_at_state']):
    if p['key'] in seen:
        continue
    seen.add(p['key']); shown.append(p)
    if len(shown) >= NBUST + 6:
        break

P('\nNAMED HISTORICAL STALL PATHS -- the law\'s pedigree pay year by year against what the stall cohort')
P('measured from the same state, and what the player actually went on to deliver.')
P('Selection rule (fixed, mechanical): the %d longest/highest-pedigree BUST paths, then the %d paths with'
  % (NBUST, len(shown) - NBUST))
P('the LARGEST realized R6 from the state -- the stallers who DID eventually collect.')
named_out = []
for i, p in enumerate(shown):
    if i == NBUST:
        P('')
        P('  ' + '-' * 100)
        P('  THE VINDICATED -- players who stalled >= 2 seasons from a low/mid state and still delivered:')
        P('  ' + '-' * 100)
    P('')
    P('  %-22s pick %2d %-4s  v0 %7.1f  state %d (age %d, %.0f games)  class=%s  k=%d  R6 at state %.1f'
      % (nice(p['key']), p['pick'], p['pos'], p['v0'], p['year'], p['age'], p['g0'], p['cls'], p['k'], p['R6_at_state']))
    P('     %-6s %6s %8s %8s %11s %12s %12s %11s %11s'
      % ('year', 'games', 'cum g', 'beta(g)', 'LAW PAYS', 'cohort says', 'GAP', 'realized R6', 'law/R6'))
    for s in p['steps']:
        r6s = ('%11.1f' % s['R6']) if s['R6'] is not None else '  censored'
        ratio = ('%10.2fx' % (s['law_ped'] / s['R6'])) if (s['R6'] is not None and s['R6'] > 1.0) else '         -'
        P('     %-6d %6.0f %8.1f %8.4f %11.1f %12.1f %+12.1f %s %s'
          % (s['year'], s['games_this_year'], s['g'], s['beta_wired'], s['law_ped'], s['cohort_ped'],
             s['gap'], r6s, ratio))
    named_out.append(p)
RES['named_paths'] = named_out

# ---- does the law ever RAISE the pedigree pay while the player stalls? (C6 second leg) -------------
rose_paths = []
for p in PATHS:
    for a, b in zip(p['steps'], p['steps'][1:]):
        if b['beta_wired'] > a['beta_wired'] + 1e-12:
            rose_paths.append(dict(key=p['key'], year_from=a['year'], year_to=b['year'],
                                   g_from=a['g'], g_to=b['g'], law_from=a['law_ped'], law_to=b['law_ped'],
                                   pick=p['pick'], v0=p['v0']))
            break
RES['paths_where_law_rose_while_stalling'] = rose_paths
P('\nPATHS WHERE THE WIRED LAW PAID **MORE** PEDIGREE AFTER A STALLED SEASON: %d of %d'
  % (len(rose_paths), len(PATHS)))
for x in rose_paths[:8]:
    P('   %-22s pick %2d  g %.0f -> %.0f   law %.1f -> %.1f  (+%.1f)'
      % (nice(x['key']), x['pick'], x['g_from'], x['g_to'], x['law_from'], x['law_to'],
         x['law_to'] - x['law_from']))

# ---- C8: the strong form ---------------------------------------------------------------------------
P('\nC8 -- THE STRONG FORM: law pedigree leg vs the WHOLE realized R6, T1 continued stallers:')
P('%-7s %5s %14s %14s %8s' % ('band', 'n', 'mean law ped', 'mean R6', 'ratio'))
c8 = {}
for gb in LOWMID:
    rg = [r for r in ROWS if r['gb'] == gb and r['tier'] == 'T1 1-20' and r['cls'] != 'breakout']
    if len(rg) < 8:
        P('%-7s %5d  THIN' % (gb, len(rg))); continue
    ml = sum(r['law_ped'] for r in rg) / len(rg)
    mr = sum(r['R'] for r in rg) / len(rg)
    c8[gb] = dict(n=len(rg), mean_law_ped=ml, mean_R6=mr, ratio=(ml / mr if mr > 0 else None),
                  median_R6=q([r['R'] for r in rg], .5))
    P('%-7s %5d %14.1f %14.1f %8.2f' % (gb, len(rg), ml, mr, ml / mr if mr > 0 else float('nan')))
RES['c8_strong_form'] = c8

RES['thin_cells_collapsed'] = THIN

# ==================================================================================================
# EXIT
# ==================================================================================================
assert md5f(MEASURE) == MEASURE_MD5, '30B-M HARNESS PIN BROKEN AT EXIT'
assert G['md5'](G['L1P']) == G['L1_MD5'], 'LAYER 1 PIN BROKEN AT EXIT'
json.dump(RES, open(OUT_JSON, 'w'), indent=1, sort_keys=True, default=float)
open(OUT_TXT, 'w').write('\n'.join(_LOG) + '\n')
P('\nwrote %s' % OUT_JSON)
P('wrote %s' % OUT_TXT)
open(OUT_TXT, 'w').write('\n'.join(_LOG) + '\n')
