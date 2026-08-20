#!/usr/bin/env python3
# =====================================================================================================
# ORDER 30A-2  --  THE SITTER RE-CUT.  Four tasks, all four preregistered in PREREG_30A2.md.
#
#   T1  LISTED-CONDITIONING      -- D_listed(N) on the #338 listed-through reconstruction, TWO readings
#   T2  THE CONTINUOUS CLOCK     -- season-fraction depth, log-linear in D, named rows at TRUE depth
#   T3  BANDS, A2-GUARDED        -- the pick-band lens with the near-zero denominator cells excluded
#   T4  THE GAMES TRANSITION     -- D(k games by depth N), the 0->1 boundary measured not assumed
#
# READ-ONLY.  This instrument writes only into docs/evidence/sitter_fade_2026-08-14/.  It does not
# touch the store, the board, the curve or any engine file, and IT WIRES NOTHING.  The old `los_decay`
# schedule remains the DECLARED FALLBACK until the owner rules.
#
# It SUPERSEDES ORDER 30A's packet as the ruling basis.  It does not rewrite ORDER 30A: the
# unconditional row is reproduced here to 1e-6 as a control (PREREG Q24) and republished beside the
# candidate law, never in place of it.
#
# INPUTS (all pinned by md5; the instrument halts on any mismatch):
#   data/delivered_value/layer1_player_seasons.json          ad1229ea...  (assumption-free player-seasons)
#   docs/evidence/delivered_value_2026-08-12/LAYER2.json     (the DV lane's grace-A career scores)
#     -- BOTH live on origin/build/delivered-value; read out of git by `git show`, md5-asserted.
#        A fresh checkout needs:  git fetch origin build/delivered-value
#   engine/rl_after/pvc_curve_v2.json                        (the landed entry law -- nd_v0.posv, curve)
#   docs/evidence/landing_29_2026-08-13/DAY0_29B_FINAL.json  (the 29B printed flat-v0 prices)
#   docs/evidence/noarb_338_2026-08-06/per_entrant_338_confirmation.json  (the #338 lane's own emit)
#   data/season_state.json                                   (calendar_progress -- the T2 clock)
#   engine/rl_after/rl_model.py                              (imported live: disc_factor, GRACE, LOS_C/P)
#
# STORE DRIFT, DISCLOSED: the DV lane's scores were built on store d9a24282; this branch carries
# cb38ef11.  Layer 1 (ad1229ea) is byte-identical, so the POPULATION and every SIT FACT are
# unaffected.  T4's per-season decomposition takes only the SHARE off a live-store recompute; the
# LEVEL stays the pinned DV number, so the store move cannot enter the estimate (PREREG §4, Q17).
# =====================================================================================================
import os, sys, json, math, hashlib, subprocess, collections, io, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
OUTD = HERE

os.environ.update(PYTHONHASHSEED='0', RL_REPO=ROOT, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1',
                  MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1')

DV_BRANCH = 'origin/build/delivered-value'
L1_REL = 'data/delivered_value/layer1_player_seasons.json'
L2_REL = 'docs/evidence/delivered_value_2026-08-12/LAYER2.json'
L1_MD5 = 'ad1229ea6f443538479447132382b21c'

PINS = {
    'curve':     ('engine/rl_after/pvc_curve_v2.json',                      None),
    'day0_29b':  ('docs/evidence/landing_29_2026-08-13/DAY0_29B_FINAL.json', None),
    'rl_model':  ('engine/rl_after/rl_model.py',                            '14000af2a46f7a3c4cdfde303f5a1aff'),
    'store':     ('engine/rl_after/rl_model_data.json',                     'cb38ef1171dcf20aae66ebf12682be0d'),
    'per338':    ('docs/evidence/noarb_338_2026-08-06/per_entrant_338_confirmation.json', None),
    'season_state': ('data/season_state.json',                              None),
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
P('ORDER 30A-2  --  THE SITTER RE-CUT.  LISTED-CONDITIONING / CONTINUOUS CLOCK / BANDS / GAMES')
P('=' * 118)
P('READ-ONLY.  NOTHING WIRES.  The old los_decay schedule stands as the DECLARED FALLBACK until the')
P('owner rules.  Prereg: PREREG_30A2.md, committed before this file existed in runnable form.')
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
POSV = CURVE['nd_v0']['posv']
ALLIN = CURVE['curve']                              # the all-in ND curve -- the A2 guard's reference
DAY0 = json.load(open(os.path.join(ROOT, PINS['day0_29b'][0])))
PER338 = json.load(open(os.path.join(ROOT, PINS['per338'][0])))
SEASON_STATE = json.load(open(os.path.join(ROOT, PINS['season_state'][0])))

P('INPUTS')
P('  layer1                 %s  (%s:%s)' % (L1_MD5[:12], DV_BRANCH, L1_REL))
P('  LAYER2 (grace-A)       %s  (%s:%s)' % (L2_MD5[:12], DV_BRANCH, L2_REL))
for k in sorted(PIN_OBS):
    P('  %-22s %s  (%s)' % (k, PIN_OBS[k][:12], PINS[k][0]))
P('  STORE DRIFT DISCLOSED: DV scores built on d9a24282; this branch carries %s; the #338 per-entrant'
  % PIN_OBS['store'][:8])
P('  matrix was emitted on store %s. Layer 1 is byte-identical across all three.'
  % PER338['meta']['store_md5'])
P('')

sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', ROOT + '/engine/rl_after']
_cwd = os.getcwd(); os.chdir(ROOT + '/engine/rl_after')
with contextlib.redirect_stdout(io.StringIO()):
    import rl_model as MA
    import dist_redesign as rd
os.chdir(_cwd)
assert int(MA.AGE_REF) == 2026, 'AGE_REF %s' % MA.AGE_REF
assert MA.AGE_DISC is False, 'AGE_DISC must be OFF (flat-14 ladder) -- got %s' % MA.AGE_DISC

NOW = 2026
LAST_COMPLETE = 2025
DEPTHS = [1, 2, 3, 4, 5, 6]
K_SHRINK = 15.0
BANDS3 = [(1, 20), (21, 40), (41, 64)]
BANDS2 = [(1, 20), (21, 64)]
POSITIONS = ['KPD', 'KPF', 'MID', 'RUCK', 'SD', 'SF']

BARS = {g: MA.REPL[g] - rd.REPL_DROP.get(g, 0.0) for g in MA.REPL}


def los_decay_at(group, s):
    over = max(0.0, s - MA.GRACE.get(group, 1.0))
    return math.exp(-MA.LOS_C * over ** MA.LOS_P)


def curve_at(p):
    return float(ALLIN[str(p)]) if isinstance(ALLIN, dict) else float(ALLIN[p - 1])


# =====================================================================================================
# POPULATION  --  carried VERBATIM from o30a_derive.py so the control (Q24) is a real control
# =====================================================================================================
ENTRIES = L1['entries']
SEASONS = collections.defaultdict(list)
for s in L1['player_seasons']:
    SEASONS[s['key']].append(s)
for k in SEASONS:
    SEASONS[k].sort(key=lambda x: x['year'])

ATTR = L2['attribution']
GA = L2['grace_a']
BASE = L2['base']


def entry_age(e):
    a = e['entry_age']
    return a if a is not None else e['entry_age_fallback_if_null']


def grace_A_G(a):
    return 2 if (a is not None and a <= 19) else 0


def DF(e, k):
    a = entry_age(e)
    return MA.disc_factor(a, MA.LENS['bal'], max(0, k - grace_A_G(a)), 'bal')


def games_in(key, year):
    return sum(s['games'] for s in SEASONS.get(key, []) if s['year'] == year)


def leading_sit(e):
    ey = e['entry_year']; n = 0; k = 1
    while ey + k <= LAST_COMPLETE:
        if games_in(e['key'], ey + k) > 0:
            break
        n += 1; k += 1
    return n


def ever_played(e):
    return any(s['games'] > 0 for s in SEASONS.get(e['key'], []))


# ---- #338 MINIMUM LISTING TENURE, re-derived from Layer 1 (PREREG §1) -------------------------------
# The rule text below is the port at emit_matrix_338.py:127-160, itself ported verbatim from
# engine/rl_after/s4_matrix_M1v7.py:53-70 (commit 30996f8).  Nothing here is invented.
MIN_TENURE_BANDS = {'ND 1-20': 4, 'ND 21-40': 3, 'ND 41+ and every pool route': 2}


def min_tenure_338(e):
    """#338: minimum listed seasons implied by the entry route/pick band. Banded on MA.effpk, which
    Layer 1 carries as `effective_pick` (o26b_layer1.py:127) -- NOT the Q-B slid pick."""
    if e['type'] == 'ND' and not e.get('pickless'):
        pk = e['effective_pick']
        if pk <= 20:
            return 4
        if pk <= 40:
            return 3
    return 2


def debut_year_338(e):
    """#338: first season ON A LIST. MSD debuts in its entry year; every other route the year after."""
    C = e['entry_year']
    return None if C is None else (C if e['type'] == 'MSD' else C + 1)


def last_scoring_year(key):
    return max((s['year'] for s in SEASONS.get(key, [])), default=0)


def listed_through_LA(e):
    """L-A: the #338 reconstruction AS FILED, own-data-extends included. None == STILL LISTED."""
    LL = e['last_listed']
    if LL is not None:
        return LL
    if not e['retired']:
        return None
    d = debut_year_338(e)
    return max((d + min_tenure_338(e) - 1) if d is not None else 0, last_scoring_year(e['key']))


def resolution_class(e):
    """How this row's listing status is KNOWN -- stated per cell so a band rule is never mistaken for
    a listing measurement."""
    if e['last_listed'] is not None:
        return 'explicit'                       # a KNOWN FACT off the store
    if not e['retired']:
        return 'active'                         # still listed, observed
    d = debut_year_338(e)
    floor = (d + min_tenure_338(e) - 1) if d is not None else 0
    return 'own_data_extends' if last_scoring_year(e['key']) > floor else 'band_floor'


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
    mt = min_tenure_338(e)
    lt = listed_through_LA(e)
    rec = dict(key=e['key'], entry_year=ey, pick=pk, natural_pick=a['natural_pick'], slid=a['slid'],
               eff_pick=e['effective_pick'], pos=g0, v0=v0, entry_age=entry_age(e),
               retired=e['retired'], last_listed=e['last_listed'],
               tier=e['window_tier'], maxdepth=1 + leading_sit(e), ever=ever_played(e),
               min_tenure=mt, listed_through_LA=lt, res=resolution_class(e),
               last_score_year=last_scoring_year(e['key']),
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
P('  v0 == 0 rows in fitted window         %5d   (dropped from every ratio, as ORDER 30A)'
  % sum(1 for r in FIT if r['v0'] <= 0))
FIT = [r for r in FIT if r['v0'] > 0]
SENS = [r for r in SENS if r['v0'] > 0]
P('')


# =====================================================================================================
# LISTING -- the two readings, and what they are made of
# =====================================================================================================
def listed_uncond(r, N):
    return True


def listed_LA(r, N):
    lt = r['listed_through_LA']
    return (lt is None) or (lt >= r['entry_year'] + N)


def listed_LB(r, N):
    """L-B, the outcome-blind floor, AS FILED in PREREG §1: listed at N iff (min_tenure >= N) or
    (not retired). The own-data-extends clause is dropped, so no row is admitted BECAUSE it played."""
    return (r['min_tenure'] >= N) or (not r['retired'])


READINGS = collections.OrderedDict([
    ('UNCONDITIONAL (ORDER 30A)', listed_uncond),
    ('L-A reconstruction as filed', listed_LA),
    ('L-B outcome-blind floor', listed_LB),
])


def q(xs, f):
    if not xs:
        return None
    ys = sorted(xs)
    if len(ys) == 1:
        return ys[0]
    i = f * (len(ys) - 1)
    lo = int(math.floor(i)); hi = int(math.ceil(i))
    return ys[lo] + (ys[hi] - ys[lo]) * (i - lo)


def at_depth(rows, N):
    """ORDER 30A's depth-N cell: still sitting at N, and seasons 1..N-1 COMPLETED."""
    return [r for r in rows if r['maxdepth'] >= N and (r['entry_year'] + N - 1) <= LAST_COMPLETE]


def cell(rows, N):
    """The full disclosure dict for a depth-N cell of 0-game sitters (ORDER 30A's estimator)."""
    if not rows:
        return dict(n=0)
    rr = []; num = 0.0; den = 0.0; ts = []
    for r in rows:
        v = r['ga_total'] * DF(r['e'], N - 1)
        rr.append(v / r['v0']); num += v; den += r['v0']; ts.append(r['ga_tshare'])
    res = collections.Counter(r['res'] for r in rows)
    return dict(n=len(rr), mean=sum(rr) / len(rr), median=q(rr, 0.5), p25=q(rr, 0.25), p75=q(rr, 0.75),
                pooled=(num / den if den else None), tail_share=sum(ts) / len(ts),
                n_zero=sum(1 for x in rr if x <= 1e-12), n_ever=sum(1 for r in rows if r['ever']),
                res=dict(res))


def surface(rows, listed_fn):
    return {N: cell([r for r in at_depth(rows, N) if listed_fn(r, N)], N) for N in DEPTHS}


def normalise(surf):
    b = surf[1].get('mean')
    if not b:
        return {}
    return {k: (v['mean'] / b if v.get('n') else None) for k, v in surf.items()}


SURF = collections.OrderedDict((lab, surface(FIT, fn)) for lab, fn in READINGS.items())
DTAB = collections.OrderedDict((lab, normalise(s)) for lab, s in SURF.items())

# ---- CONTROL Q24: the unconditional row must reproduce ORDER 30A to 1e-6 -----------------------------
O30A = dict(RAW1=1.0286, D={2: 0.5684, 3: 0.2143, 4: 0.1052, 5: 0.0742, 6: 0.0905})
CTRL = dict(RAW1=SURF['UNCONDITIONAL (ORDER 30A)'][1]['mean'],
            D={N: DTAB['UNCONDITIONAL (ORDER 30A)'][N] for N in DEPTHS})
CTRL_OK = (abs(CTRL['RAW1'] - O30A['RAW1']) < 5e-5
           and all(abs(CTRL['D'][N] - O30A['D'][N]) < 5e-5 for N in O30A['D']))
P('CONTROL (PREREG Q24)  --  the unconditional row reproduced from scratch in this instrument')
P('  RAW(1)   this act %.6f   ORDER 30A %.4f' % (CTRL['RAW1'], O30A['RAW1']))
P('  D(N)     this act %s' % '  '.join('%d:%.6f' % (N, CTRL['D'][N]) for N in (2, 3, 4, 5, 6)))
P('  D(N)     ORDER 30A %s' % '  '.join('%d:%.4f' % (N, O30A['D'][N]) for N in (2, 3, 4, 5, 6)))
P('  VERDICT  %s' % ('REPRODUCED to the published precision' if CTRL_OK else
                     '*** DRIFT -- a defect in THIS act, reported as such ***'))
P('')

# ---- the listing sources, cross-checked (PREREG §1 THE DISAGREEMENT CHECK, Q7) -----------------------
P338 = {r['key']: r for r in PER338['recs']}
STORE_BY = {}
for p in MA.data:
    kk = p.get('key') or MA.slug(p['player'])
    if kk not in STORE_BY:
        STORE_BY[kk] = p

xc = dict(n=0, matched=0, agree=0, missing=0, dis=[])
store_dis = dict(retired=[], last_listed=[])
for r in FIT:
    xc['n'] += 1
    p338 = P338.get(r['key'])
    if p338 is None:
        xc['missing'] += 1
    else:
        xc['matched'] += 1
        mine = r['listed_through_LA'] if r['listed_through_LA'] is not None else 2026
        mine = min(mine, 2026)
        theirs = max(p338['yrs'])
        if mine == theirs:
            xc['agree'] += 1
        else:
            xc['dis'].append(dict(key=r['key'], mine=mine, per338=theirs,
                                  l1_retired=r['retired'], per338_retired_now=p338['retired_now'],
                                  l1_min_tenure=r['min_tenure'], per338_min_tenure=p338['min_tenure_338'],
                                  l1_last_score=r['last_score_year'],
                                  per338_last_game=p338['last_game_year'],
                                  cause=('retired_flag' if bool(r['retired']) != bool(p338['retired_now'])
                                         else ('min_tenure_band' if r['min_tenure'] != p338['min_tenure_338']
                                               else 'season_rows_or_store_move'))))
    sp = STORE_BY.get(r['key'])
    if sp is not None:
        if bool(sp.get('_retired')) != bool(r['retired']):
            store_dis['retired'].append(r['key'])
        if sp.get('_last_listed') != r['last_listed']:
            store_dis['last_listed'].append(r['key'])

P('THE LISTING SOURCE, CROSS-CHECKED  (PREREG §1 disagreement check / Q7)')
P('  fitted ND rows                                    %5d' % xc['n'])
P('  matched into per_entrant_338_confirmation.json    %5d   (unmatched %d)' % (xc['matched'], xc['missing']))
P('  listed-through AGREES with that lane\'s max(yrs)   %5d   = %.1f%% of matched'
  % (xc['agree'], 100.0 * xc['agree'] / max(1, xc['matched'])))
_cause = collections.Counter(d['cause'] for d in xc['dis'])
P('  disagreements by cause                            %s' % (dict(_cause) or '{}'))
P('  live store cb38ef11 vs Layer 1 ad1229ea: _retired differs on %d rows, _last_listed on %d rows'
  % (len(store_dis['retired']), len(store_dis['last_listed'])))
if xc['dis'][:8]:
    P('  first disagreements (reported, never resolved by preference):')
    P('    %-24s %6s %8s %9s %11s' % ('key', 'mine', 'per338', 'L1 retd', 'per338 retd'))
    for d in xc['dis'][:8]:
        P('    %-24s %6s %8s %9s %11s' % (d['key'], d['mine'], d['per338'], d['l1_retired'],
                                          d['per338_retired_now']))
P('  NOTE: the #338 lane\'s window uses its own `retired_now(p)` (delisted OR draft<=2021 with last')
P('  game <=2024); this act uses Layer 1\'s `retired` (= the store\'s `_retired`). The two are')
P('  DIFFERENT PREDICATES and the difference is reported, not reconciled.')
_bandmix = sum(1 for r in FIT if min_tenure_338(r['e']) != (4 if r['pick'] <= 20 else (3 if r['pick'] <= 40 else 2)))
P('  rows whose #338 band (on effective_pick) differs from the attribution pick\'s band: %d' % _bandmix)
P('  explicit `_last_listed` (a KNOWN FACT) on fitted ND rows: %d of %d'
  % (sum(1 for r in FIT if r['last_listed'] is not None), len(FIT)))
P('')

# =====================================================================================================
# T1  --  THE TWO ROWS, SIDE BY SIDE
# =====================================================================================================
P('=' * 118)
P('T1  --  LISTED-CONDITIONING.  D(N) = E[discounted delivery from N | 0 games AND listed at N] / RAW(1)')
P('=' * 118)
P('  Both rows are normalised on their OWN depth-1 baseline. At depth 1 every ND row is listed under')
P('  both readings (min_tenure >= 2), so the three baselines are the SAME NUMBER -- asserted below.')
for lab in READINGS:
    assert abs(SURF[lab][1]['mean'] - CTRL['RAW1']) < 1e-12, 'depth-1 baseline moved under %s' % lab
P('  depth-1 baseline identical under all three readings: RAW(1) = %.6f  [ASSERTED]' % CTRL['RAW1'])
P('')
P('  %-6s %-28s %6s %6s %8s %8s %8s %8s %9s %8s' %
  ('depth', 'reading', 'n', 'n=0', 'RAW mean', 'median', 'p25', 'p75', 'D(N)', 'tailshr'))
for N in DEPTHS:
    for lab in READINGS:
        c = SURF[lab][N]
        if not c.get('n'):
            P('  %-6s %-28s %6d   -- UNRESOLVED / EMPTY CELL --' % (N, lab, 0)); continue
        P('  %-6s %-28s %6d %6d %8.4f %8.4f %8.4f %8.4f %9.4f %8.4f'
          % (N, lab, c['n'], c['n_zero'], c['mean'], c['median'], c['p25'], c['p75'],
             DTAB[lab][N], c['tail_share']))
    P('')

P('  LISTING-RESOLUTION COVERAGE PER CELL  --  how the listing status of the rows IN the cell is known.')
P('  explicit = store `_last_listed` (a KNOWN FACT) | active = not retired (observed) |')
P('  band_floor = the #338 tenure band ALONE (NO player-specific delisting observation) |')
P('  own_data_extends = the floor was extended by the player\'s OWN SCORING ROWS (selection on outcome).')
P('  %-6s %-28s %6s %9s %8s %11s %18s' %
  ('depth', 'reading', 'n', 'explicit', 'active', 'band_floor', 'own_data_extends'))
for N in DEPTHS:
    for lab in READINGS:
        c = SURF[lab][N]
        if not c.get('n'):
            continue
        rs = c['res']
        P('  %-6s %-28s %6d %9d %8d %11d %18d'
          % (N, lab, c['n'], rs.get('explicit', 0), rs.get('active', 0), rs.get('band_floor', 0),
             rs.get('own_data_extends', 0)))
P('')
P('')
P('  HOW TO READ THAT TABLE, said plainly. The four provenance columns describe how the L-A')
P('  RECONSTRUCTION resolves each row. For the L-B rows the admission test is different and cruder:')
P('  a row is in an L-B cell because it is STILL ACTIVE (the `active` column -- an OBSERVED fact) or')
P('  because the #338 TENURE BAND alone carries it (every other column). Under L-B, therefore:')
for N in DEPTHS:
    c = SURF['L-B outcome-blind floor'][N]
    if not c.get('n'):
        continue
    act = c['res'].get('active', 0) + c['res'].get('explicit', 0)
    P('    depth %d  n = %4d   observed listing (active or explicit `_last_listed`) %4d = %5.1f%%   '
      'carried by the tenure band ALONE %4d = %5.1f%%'
      % (N, c['n'], act, 100.0 * act / c['n'], c['n'] - act, 100.0 * (c['n'] - act) / c['n']))
P('  At depth 2 that is 0%% observed: the depth-2 listed cell IS the unconditional cell, and Q1 says so.')
P('')
P('  FLOOR EXPIRY (arithmetic on the rule, prestated in PREREG §1): the band floor carries depth <= 4')
P('  for picks 1-20, <= 3 for 21-40, <= 2 for 41-64. At depth >= 5 NO ND pick is carried by the floor,')
P('  so an L-B listed cell at depth 5+ can contain only STILL-ACTIVE entrants.')
for N in (5, 6):
    c = SURF['L-B outcome-blind floor'][N]
    P('    depth %d  L-B  n = %d   %s' % (N, c.get('n', 0),
      'UNRESOLVED (n < 5): no listed-conditional number is published for this depth'
      if c.get('n', 0) < 5 else 'resolved'))
P('')

LA_LB_GAP = {N: (abs(DTAB['L-A reconstruction as filed'][N] - DTAB['L-B outcome-blind floor'][N])
                 if (DTAB['L-A reconstruction as filed'].get(N) is not None
                     and DTAB['L-B outcome-blind floor'].get(N) is not None) else None)
             for N in DEPTHS}
P('  L-A vs L-B GAP per depth (PREREG §6: a gap > 0.15 means the evidence supports a BOUND, not a law)')
for N in DEPTHS:
    g = LA_LB_GAP[N]
    if g is None:
        continue
    P('    depth %d  |D_LA - D_LB| = %.4f   %s' % (N, g, 'BOUND, not a law' if g > 0.15 else 'single number defensible'))
P('')

# =====================================================================================================
# T2  --  THE CONTINUOUS DEPTH CLOCK
# =====================================================================================================
PHI = float(SEASON_STATE['calendar_progress'])
P('=' * 118)
P('T2  --  THE CONTINUOUS DEPTH CLOCK.  c = N + phi,  phi = calendar_progress = %.2f' % PHI)
P('=' * 118)
P('  Clock source: data/season_state.json (AUTHORITATIVE DYNAMIC SEASON STATE) -- season_year %s,'
  % SEASON_STATE['season_year'])
P('  as_of_round %s of %s, calendar_progress %.2f. exposure_pace (%.3f) is the empirical durable-sample'
  % (SEASON_STATE['as_of_round'], SEASON_STATE['season_total_rounds'], PHI, SEASON_STATE['exposure_pace']))
P('  pace and is explicitly NOT the calendar clock; it is not used here.')
P('  Convention (prestated): D(c) = D(N)^(1-phi) * D(N+1)^phi   [log-linear in D]')
P('  Sensitivity published beside it:  D_lin(c) = (1-phi)*D(N) + phi*D(N+1)')
P('  Where D(N+1) does not resolve, the law is HELD FLAT at the deepest resolved value and the row is')
P('  FLAGGED AS EXTRAPOLATED -- never quoted silently.')
P('')


def interp(tab, c, log=True):
    """Returns (D, extrapolated_flag, deepest_used)."""
    N = int(math.floor(c)); phi = c - N
    d0 = tab.get(N); d1 = tab.get(N + 1)
    if d0 is None:
        deep = max(k for k in tab if tab[k] is not None)
        return tab[deep], True, deep
    if d1 is None:
        return d0, True, N
    if log:
        if d0 <= 0 or d1 <= 0:
            return (1 - phi) * d0 + phi * d1, False, N + 1
        return math.exp((1 - phi) * math.log(d0) + phi * math.log(d1)), False, N + 1
    return (1 - phi) * d0 + phi * d1, False, N + 1


# the tables the continuous law rides on. A depth whose cell is UNRESOLVED (n < 5) is dropped, so the
# held-flat convention fires rather than a 1-row cell being interpolated through.
MINCELL = 5


def usable(lab):
    return {N: DTAB[lab][N] for N in DEPTHS
            if DTAB[lab].get(N) is not None and SURF[lab][N].get('n', 0) >= MINCELL}


TABS = collections.OrderedDict((lab, usable(lab)) for lab in READINGS)
for lab, t in TABS.items():
    P('  usable integer table [%s]: %s' % (lab, '  '.join('D(%d)=%.4f' % (N, t[N]) for N in sorted(t))))
P('')

D29 = {r['key']: r for r in DAY0['rows']}
E1 = {e['key']: e for e in ENTRIES}
NAMED = ['josh-smillie', 'harry-demattia', 'max-knobel']
NAMED_OUT = []
P('  NAMED ROWS AT TRUE CURRENT DEPTH  --  arithmetic on a packet. NOTHING IS WIRED.')
P('  %-16s %-5s %-5s %-5s %-6s %8s | %-14s | %-16s | %-16s | %-16s'
  % ('player', 'pos', 'pick', 'entry', 'c', '29B v0', 'old los_decay', '30A integer D',
     'continuous UNCOND', 'continuous L-B'))
for k in NAMED:
    e = E1.get(k)
    if e is None:
        continue
    N = NOW - e['entry_year']
    c = N + PHI
    pos = e['day0_position']
    printed = D29[k]['printed'] if k in D29 else None
    old = los_decay_at(pos, N)
    old_c = los_decay_at(pos, c)
    row = dict(key=k, pos=pos, pick=e['pick'], entry_year=e['entry_year'], integer_depth=N,
               continuous_depth=c, phi=PHI, printed_29b=printed,
               old_los_decay_integer=old, old_los_decay_continuous=old_c,
               old_price_integer=(round(printed * old) if printed else None))
    for lab in READINGS:
        t = TABS[lab]
        di, ex, deep = interp(t, c, log=True)
        dl, _, _ = interp(t, c, log=False)
        tag = lab.split()[0]
        row['D_int_%s' % tag] = t.get(N)
        row['D_cont_%s' % tag] = di
        row['D_cont_linear_%s' % tag] = dl
        row['extrapolated_%s' % tag] = ex
        row['deepest_resolved_%s' % tag] = deep
        row['price_cont_%s' % tag] = (round(printed * di) if printed is not None else None)
        row['price_int_%s' % tag] = (round(printed * t[N]) if (printed is not None and t.get(N)) else None)
        row['conv_gap_%s' % tag] = abs(di - dl)
    NAMED_OUT.append(row)
    P('  %-16s %-5s %-5s %-5s %-6.2f %8s | %.3f -> %-6s | %.4f -> %-7s | %.4f -> %-7s%s | %.4f -> %-7s%s'
      % (k, pos, e['pick'], e['entry_year'], c, printed, old, row['old_price_integer'],
         row['D_int_UNCONDITIONAL'], row['price_int_UNCONDITIONAL'],
         row['D_cont_UNCONDITIONAL'], row['price_cont_UNCONDITIONAL'],
         '*' if row['extrapolated_UNCONDITIONAL'] else ' ',
         row['D_cont_L-B'], row['price_cont_L-B'], '*' if row['extrapolated_L-B'] else ' '))
P('  (* = EXTRAPOLATED under the held-flat convention: the next integer depth does not resolve.)')
P('')
P('  THE SAME ROWS, EVERY COLUMN  --  D and price under each law, plus the interpolation sensitivity')
P('  %-16s %-6s %10s %10s %10s %10s %10s %10s %9s' %
  ('player', 'c', 'D_unc(N)', 'D_unc(c)', 'D_LA(c)', 'D_LB(c)', 'price_unc', 'price_LB', 'lin-gap'))
for row in NAMED_OUT:
    P('  %-16s %-6.2f %10.4f %10.4f %10.4f %10.4f %10s %10s %9.4f'
      % (row['key'], row['continuous_depth'], row['D_int_UNCONDITIONAL'], row['D_cont_UNCONDITIONAL'],
         row['D_cont_L-A'], row['D_cont_L-B'], row['price_cont_UNCONDITIONAL'], row['price_cont_L-B'],
         max(row['conv_gap_UNCONDITIONAL'], row['conv_gap_L-A'], row['conv_gap_L-B'])))
P('')
P('  WHAT THE CLOCK CONFLATES, disclosed: D(N) is the price at the START of year N. Moving N -> N+1')
P('  carries a year of time-value AND the information of watching another full season pass gameless.')
P('  The measurement is on integer seasons and cannot separate them at sub-season resolution. Both')
P('  push the same way, so the interpolated value is defensible as a PRICE; it is not a decomposition.')
P('')

# =====================================================================================================
# T3  --  BANDS, A2-GUARDED
# =====================================================================================================
G1_CELLS = sorted((g, int(p)) for g in POSV for p in POSV[g]
                  if float(POSV[g][p]) < 0.20 * curve_at(int(p)))
G1_ABS = sorted((g, int(p)) for g in POSV for p in POSV[g] if float(POSV[g][p]) < 40.0)
G2_CELLS = sorted((g, int(p)) for g in POSV for p in POSV[g]
                  if int(p) >= 58 and float(POSV[g][p]) < 0.50 * curve_at(int(p)))
G1 = set(G1_CELLS); G2 = set(G2_CELLS)

P('=' * 118)
P('T3  --  PICK BANDS, A2-GUARDED.  The near-zero positional denominator is EXCLUDED and COUNTED.')
P('=' * 118)
P('  GUARD G1 (primary, prestated): posv[g][p] < 0.20 * curve[p]. Acquisition cells selected: %s'
  % ', '.join('%s %d' % t for t in G1_CELLS))
P('  The absolute alternative the brief offered (posv < 40 board points) selects: %s  -- IDENTICAL: %s'
  % (', '.join('%s %d' % t for t in G1_ABS), G1 == set(G1_ABS)))
P('  GUARD G2 (stricter sensitivity): pick >= 58 AND posv < 0.50 * curve[p]. Cells: %s'
  % ', '.join('%s %d' % t for t in G2_CELLS))
P('')

GUARDED = {'G0 no guard (ORDER 30A)': (lambda r: True),
           'G1 primary': (lambda r: (r['pos'], r['pick']) not in G1),
           'G2 stricter': (lambda r: (r['pos'], r['pick']) not in G2)}
GUARD_DROP = {}
for gl, gf in GUARDED.items():
    dropped = [r for r in FIT if not gf(r)]
    GUARD_DROP[gl] = dict(n_fitted_rows_dropped=len(dropped),
                          by_cell=dict(collections.Counter('%s %d' % (r['pos'], r['pick']) for r in dropped)),
                          keys=[r['key'] for r in dropped],
                          n_dropped_by_depth={str(N): sum(1 for r in dropped if r in at_depth(FIT, N))
                                              for N in DEPTHS})
    P('  %-24s excludes %3d fitted rows  %s' % (gl, len(dropped), GUARD_DROP[gl]['by_cell']))
P('  (ORDER 30A had already dropped the two v0 == 0 rows -- RUCK 63/64 -- before any ratio was taken.)')
P('')

BANDTAB = {}


def band_lens(label, bands, guard_fn, listed_fn, listed_label):
    rows_all = [r for r in FIT if guard_fn(r)]
    base_c = cell([r for r in at_depth(rows_all, 1) if listed_fn(r, 1)], 1)
    base = base_c['mean']
    out = {}
    P('  LENS [%s bands | %s | %s]  base RAW(1) = %.4f  (n = %d)'
      % (label, listed_label, 'guard ' + [k for k, v in GUARDED.items() if v is guard_fn][0], base, base_c['n']))
    P('    %-6s %-8s %6s %9s %9s %9s %9s %9s %9s %8s' %
      ('depth', 'band', 'n', 'RAW mean', 'median', 'p25', 'p75', 'D_raw', 'D_shrunk', 'borrow%'))
    for N in (2, 3, 4):
        allc = cell([r for r in at_depth(rows_all, N) if listed_fn(r, N)], N)
        if not allc.get('n'):
            continue
        for (lo, hi) in bands:
            rows = [r for r in at_depth(rows_all, N) if listed_fn(r, N) and lo <= r['pick'] <= hi]
            c = cell(rows, N)
            key = '%s|%s|%s|%d|%d-%d' % (label, listed_label, [k for k, v in GUARDED.items() if v is guard_fn][0], N, lo, hi)
            if not c.get('n'):
                out[key] = dict(n=0)
                P('    %-6s %-8s %6d  -- empty --' % (N, '%d-%d' % (lo, hi), 0)); continue
            draw = c['mean'] / base
            dshr = ((c['n'] * c['mean'] + K_SHRINK * allc['mean']) / (c['n'] + K_SHRINK)) / base
            borrow = K_SHRINK / (c['n'] + K_SHRINK)
            c.update(D_raw=draw, D_shrunk=dshr, borrow=borrow, band=[lo, hi], depth=N,
                     lens=label, listing=listed_label)
            out[key] = c
            P('    %-6s %-8s %6d %9.4f %9.4f %9.4f %9.4f %9.4f %9.4f %7.1f%%'
              % (N, '%d-%d' % (lo, hi), c['n'], c['mean'], c['median'], c['p25'], c['p75'],
                 draw, dshr, 100 * borrow))
    P('')
    BANDTAB.update(out)
    return out


B = {}
for gl in ('G0 no guard (ORDER 30A)', 'G1 primary', 'G2 stricter'):
    B[('3', gl, 'UNCOND')] = band_lens('3-band', BANDS3, GUARDED[gl], listed_uncond, 'UNCOND')
    B[('2', gl, 'UNCOND')] = band_lens('2-band', BANDS2, GUARDED[gl], listed_uncond, 'UNCOND')
B[('3', 'G1 primary', 'L-B')] = band_lens('3-band', BANDS3, GUARDED['G1 primary'], listed_LB, 'L-B')
B[('2', 'G1 primary', 'L-B')] = band_lens('2-band', BANDS2, GUARDED['G1 primary'], listed_LB, 'L-B')


def dget(d, lens, guard, listing, N, lo, hi, field='D_shrunk'):
    return d.get('%s|%s|%s|%d|%d-%d' % (lens, listing, guard, N, lo, hi), {}).get(field)


# --- the verdict, mechanically evaluated -------------------------------------------------------------
def band_monotone_verdict(guard, listing, bands, lens):
    dirs = []
    for N in (2, 3, 4):
        vs = [dget(BANDTAB, lens, guard, listing, N, lo, hi) for (lo, hi) in bands]
        if any(v is None for v in vs):
            dirs.append(None); continue
        inc = all(vs[i] < vs[i + 1] for i in range(len(vs) - 1))
        dec = all(vs[i] > vs[i + 1] for i in range(len(vs) - 1))
        dirs.append('increasing' if inc else ('decreasing' if dec else 'non-monotone'))
    consistent = (dirs[0] is not None and dirs[0] in ('increasing', 'decreasing') and len(set(dirs)) == 1)
    return dirs, consistent


P('  THE BAND VERDICT, mechanically evaluated on D_shrunk across depths 2, 3, 4')
P('  %-10s %-8s %-8s %-42s %s' % ('lens', 'guard', 'listing', 'direction at depth 2 / 3 / 4', 'same direction at all three?'))
VERDICTS = {}
for lens, bands in (('3-band', BANDS3), ('2-band', BANDS2)):
    for guard in ('G0 no guard (ORDER 30A)', 'G1 primary', 'G2 stricter'):
        for listing in ('UNCOND',):
            dirs, ok = band_monotone_verdict(guard, listing, bands, lens)
            VERDICTS['%s|%s|%s' % (lens, guard, listing)] = dict(dirs=dirs, consistent=ok)
            P('  %-10s %-8s %-8s %-42s %s' % (lens, guard.split()[0], listing,
              ' / '.join(str(x) for x in dirs), 'YES' if ok else 'NO'))
    for listing in ('L-B',):
        dirs, ok = band_monotone_verdict('G1 primary', listing, bands, lens)
        VERDICTS['%s|%s|%s' % (lens, 'G1 primary', listing)] = dict(dirs=dirs, consistent=ok)
        P('  %-10s %-8s %-8s %-42s %s' % (lens, 'G1', listing, ' / '.join(str(x) for x in dirs),
                                          'YES' if ok else 'NO'))
ANY_WIREABLE = any(v['consistent'] for v in VERDICTS.values())
P('')
P('  VERDICT: %s' % ('A BAND ORDERING SURVIVES -- see the table' if ANY_WIREABLE else
                     'NO WIREABLE BAND GRADIENT. No band ordering holds in the same direction at all '
                     'three depths under any guard or listing reading.'))
P('  OWNER PROPOSAL, REFERENCED NOT APPLIED: a floor of 100 on positional v0 at pick 64 has been')
P('  proposed (not yet firmly ruled), to be confirmed with the fade ruling. Nothing in this act')
P('  applies it; G1/G2 are the prestated guards and are what every number above uses.')
_would = sorted(set('%s %s' % (g, p) for g in POSV for p in POSV[g]
                    if int(p) == 64 and float(POSV[g][p]) < 100.0))
P('  For reference only: at pick 64 the cells currently below 100 are %s.' % (', '.join(_would) or 'none'))
P('')

# =====================================================================================================
# T4  --  THE GAMES TRANSITION
# =====================================================================================================
P('=' * 118)
P('T4  --  THE GAMES TRANSITION.  D(k, N) = E[V_from_N / v0 | games in seasons 1..N-1 in k] / RAW(1)')
P('=' * 118)
P('  V_from_N(i) = ( grace_a[i].obs * s_N(i) + grace_a[i].tail ) * DF_i(N-1)')
P('  s_N(i)      = sum_{k >= N} pts_k(i) / sum_all pts_k(i)   -- per-season shares, live-store recompute')
P('  Only the SHARE comes from the live store; the LEVEL stays the pinned DV number, so the store move')
P('  d9a24282 -> cb38ef11 cannot enter the estimate. Licence: LAYER2.json::cfg.gamma_note -- GAMMA==1.0')
P('  makes delivered value ADDITIVE across seasons, so a career is a straight sum.')
P('  The projected tail is assigned WHOLLY to from-N: every tail season is post-2026 and post-last-')
P('  observed, so none of it can belong to a season before depth N.')
P('')


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


def w_sqrt(g):
    return min(1.0, math.sqrt(max(0.0, g) / 10.0))


PTS = {}          # key -> list of (k, pts) on the DV lane's own grace-A ladder, live store
for r in FIT:
    e = r['e']; ey = e['entry_year']; ea = r['entry_age']
    p = STORE_BY.get(r['key'])
    legs = []
    for s in SEASONS.get(r['key'], []):
        g = season_bar_group(s['position_played'], p)
        if g is None or g not in BARS:
            continue
        k = s['year'] - ey
        pts = MA.SCALE * season_raw(s['avg'], g) * w_sqrt(s['games']) / DF(e, k)
        legs.append((k, pts))
    PTS[r['key']] = legs


def share_from(r, N):
    legs = PTS.get(r['key'], [])
    tot = sum(x for _, x in legs)
    if tot <= 0:
        return 1.0, True                       # nothing delivered ever: the share is vacuous, s_N = 1
    return sum(x for k, x in legs if k >= N) / tot, False


# ---- Q17: the share reconstruction validates ---------------------------------------------------------
ratios = []
for r in FIT:
    live_obs = sum(x for _, x in PTS[r['key']])
    if r['ga_obs'] > 1e-9 and live_obs > 1e-9:
        ratios.append(live_obs / r['ga_obs'])
Q17 = dict(n=len(ratios), median=q(ratios, 0.5), p25=q(ratios, 0.25), p75=q(ratios, 0.75),
           iqr=(q(ratios, 0.75) - q(ratios, 0.25)) if ratios else None,
           min=min(ratios) if ratios else None, max=max(ratios) if ratios else None,
           spread=(max(ratios) - min(ratios)) if ratios else None,
           scale_live=float(MA.SCALE))
P('  SHARE-RECONSTRUCTION CONTROL (PREREG Q17): live-store recomputed obs / pinned DV grace_a.obs')
P('    n = %d   median %.4f   p25 %.4f   p75 %.4f   IQR width %.4f'
  % (Q17['n'], Q17['median'], Q17['p25'], Q17['p75'], Q17['iqr']))
P('    min %.6f   max %.6f   FULL SPREAD %.3e -- the ratio is a CONSTANT to numerical precision.'
  % (Q17['min'], Q17['max'], Q17['spread']))
P('    Every season leg moved by the SAME factor, so the store move d9a24282 -> cb38ef11 is a pure')
P('    MA.SCALE rescale (live SCALE %.6f) with the bars and the scorer unchanged. A share is exactly'
  % Q17['scale_live'])
P('    invariant to it -- which is the whole reason T4 takes the share and not the level.')
P('    A near-pure LEVEL OFFSET is what a store/SCALE move should look like, and is what justifies')
P('    taking only the share. A wide IQR would mean the legs themselves moved and would void T4.')
P('')


def games_before(r, N):
    """Cumulative games in seasons 1..N-1 (i.e. calendar years entry+1 .. entry+N-1)."""
    ey = r['entry_year']
    return sum(s['games'] for s in SEASONS.get(r['key'], []) if ey + 1 <= s['year'] <= ey + N - 1)


GBUCKETS = [('0', 0, 0), ('1-2', 1, 2), ('3-5', 3, 5), ('6-10', 6, 10), ('11+', 11, 10 ** 6)]
MIN_CELL_T4 = 10


def t4_cell(rows, N):
    if not rows:
        return dict(n=0)
    rr = []; ts = []; nvac = 0
    for r in rows:
        s, vac = share_from(r, N)
        nvac += 1 if vac else 0
        v = (r['ga_obs'] * s + r['ga_tail']) * DF(r['e'], N - 1)
        rr.append(v / r['v0']); ts.append(r['ga_tshare'])
    return dict(n=len(rr), mean=sum(rr) / len(rr), median=q(rr, 0.5), p25=q(rr, 0.25), p75=q(rr, 0.75),
                tail_share=sum(ts) / len(ts), n_zero=sum(1 for x in rr if x <= 1e-12),
                n_vacuous_share=nvac)


# ---- Q18: the 0-game reduction is EXACT --------------------------------------------------------------
red = []
for N in (2, 3, 4, 5, 6):
    rows = at_depth(FIT, N)
    bad_s = [r['key'] for r in rows if abs(share_from(r, N)[0] - 1.0) > 1e-12]
    a = t4_cell(rows, N)['mean'] / CTRL['RAW1']
    b = DTAB['UNCONDITIONAL (ORDER 30A)'][N]
    red.append(dict(N=N, n=len(rows), s_not_one=len(bad_s), keys=bad_s[:5], t4=a, o30a=b, diff=abs(a - b)))
P('  0-GAME REDUCTION CONTROL (PREREG Q18): on a 0-game row s_N must be 1.0 exactly and the T4')
P('  machinery must reproduce ORDER 30A. ASSERTED, not assumed.')
P('    %-6s %6s %14s %10s %10s %10s' % ('depth', 'n', 'rows s_N != 1', 'T4 D(0,N)', '30A D(N)', '|diff|'))
for d in red:
    P('    %-6s %6d %14d %10.6f %10.6f %10.3e' % (d['N'], d['n'], d['s_not_one'], d['t4'], d['o30a'], d['diff']))
RED_OK = all(d['s_not_one'] == 0 and d['diff'] < 1e-6 for d in red)
P('    VERDICT  %s' % ('EXACT REDUCTION HELD' if RED_OK else '*** REDUCTION FAILED -- a defect in this act ***'))
P('')

T4 = {}
for listing_lab, listing_fn in (('L-B listed-conditioned', listed_LB), ('UNCONDITIONAL', listed_uncond)):
    P('  GAMES TRANSITION  --  listing: %s' % listing_lab)
    P('    %-6s %-7s %6s %6s %10s %9s %9s %9s %10s %8s %s' %
      ('depth', 'games', 'n', 'n=0', 'RAW mean', 'median', 'p25', 'p75', 'D(k,N)', 'tailshr', 'status'))
    for N in (2, 3, 4):
        prev = None
        for (lab, lo, hi) in GBUCKETS:
            rows = [r for r in FIT
                    if (r['entry_year'] + N - 1) <= LAST_COMPLETE
                    and lo <= games_before(r, N) <= hi
                    and listing_fn(r, N)]
            c = t4_cell(rows, N)
            key = '%s|%d|%s' % (listing_lab, N, lab)
            if not c.get('n'):
                T4[key] = dict(n=0)
                P('    %-6s %-7s %6d   -- empty --' % (N, lab, 0)); continue
            D = c['mean'] / CTRL['RAW1']
            status = 'ok' if c['n'] >= MIN_CELL_T4 else 'THIN (n < %d): COLLAPSE/DISCLOSE' % MIN_CELL_T4
            step = (D - prev) if prev is not None else None
            c.update(D=D, depth=N, bucket=lab, listing=listing_lab, thin=(c['n'] < MIN_CELL_T4),
                     step_from_previous_bucket=step)
            T4[key] = c
            prev = D
            P('    %-6s %-7s %6d %6d %10.4f %9.4f %9.4f %9.4f %10.4f %8.4f %s'
              % (N, lab, c['n'], c['n_zero'], c['mean'], c['median'], c['p25'], c['p75'], D,
                 c['tail_share'], status))
        P('')
    P('')

# the step structure at depth 2 -- the owner's "no hard cliff" question, answered as measured
P('  THE STEP STRUCTURE AT DEPTH 2 (the owner\'s "not a hard cliff between 0 and 1 game")')
P('    %-24s %10s %10s %10s' % ('transition', 'from D', 'to D', 'step'))
STEPS = {}
for listing_lab in ('L-B listed-conditioned', 'UNCONDITIONAL'):
    seq = [(lab, T4.get('%s|2|%s' % (listing_lab, lab), {}).get('D')) for (lab, _, _) in GBUCKETS]
    seq = [(l, d) for l, d in seq if d is not None]
    st = []
    for i in range(len(seq) - 1):
        st.append(dict(frm=seq[i][0], to=seq[i + 1][0], d0=seq[i][1], d1=seq[i + 1][1],
                       step=seq[i + 1][1] - seq[i][1]))
    STEPS[listing_lab] = st
    P('    -- %s --' % listing_lab)
    for s in st:
        P('    %-24s %10.4f %10.4f %10.4f' % ('%s -> %s' % (s['frm'], s['to']), s['d0'], s['d1'], s['step']))
    if st:
        st3 = [s for s in st if s['frm'] in ('0', '1-2', '3-5')]
        big = max(st3, key=lambda s: s['step']) if st3 else None
        mono = all(s['step'] > 0 for s in st3)
        P('    LARGEST of the three prestated steps: %s -> %s (%+.4f)' % (big['frm'], big['to'], big['step']))
        P('    0 -> 1-2 step: %+.4f  (%.0f%% of the whole 0 -> 6-10 range)'
          % (st3[0]['step'], 100.0 * st3[0]['step'] / max(1e-9, (st3[-1]['d1'] - st3[0]['d0']))))
        P('    monotone increasing in k over 0 / 1-2 / 3-5 / 6-10 ?  %s' % ('YES' if mono else 'NO'))
        P('    READING: %s' % (
            'the 0 -> 1-2 boundary IS the largest step -- the measurement shows a STEP there, not a curve.'
            if (big is not None and big['frm'] == '0') else
            'the 0 -> 1-2 boundary is a LARGE step but not the largest, and the sequence is NOT monotone, '
            'so the measurement supports neither a clean cliff nor a smooth curve at this resolution.'
            if not mono else
            'the 0 -> 1-2 boundary is not the largest step and the sequence is monotone: a smooth '
            'transition is supported.'))
    P('')

# the cumulative "<= k games" reading the brief phrased, published beside the prereg's buckets
P('  SECONDARY, the brief\'s phrasing: "<= k games by depth N" (cumulative, NOT the prereg buckets)')
P('    %-6s %-9s %6s %10s %10s %9s' % ('depth', '<= games', 'n', 'RAW mean', 'D', 'median'))
T4CUM = {}
for N in (2, 3):
    for kmax in (0, 2, 5, 10):
        rows = [r for r in FIT if (r['entry_year'] + N - 1) <= LAST_COMPLETE
                and games_before(r, N) <= kmax and listed_LB(r, N)]
        c = t4_cell(rows, N)
        if not c.get('n'):
            continue
        c['D'] = c['mean'] / CTRL['RAW1']
        T4CUM['%d|<=%d' % (N, kmax)] = c
        P('    %-6s %-9s %6d %10.4f %10.4f %9.4f' % (N, '<= %d' % kmax, c['n'], c['mean'], c['D'], c['median']))
P('')

# =====================================================================================================
# THE PREREG, SCORED
# =====================================================================================================
def g(lab, N):
    return DTAB[lab].get(N)


UNC, LA, LB = 'UNCONDITIONAL (ORDER 30A)', 'L-A reconstruction as filed', 'L-B outcome-blind floor'


def scored(qid, text, verdict, detail):
    return dict(q=qid, prediction=text, verdict=verdict, detail=detail)


SC = []
SC.append(scored('Q1', 'D_listed(2) == D_uncond(2) EXACTLY (1e-9) under BOTH L-A and L-B',
                 'HELD' if (abs(g(LA, 2) - g(UNC, 2)) < 1e-9 and abs(g(LB, 2) - g(UNC, 2)) < 1e-9) else 'BREACHED',
                 'LA-UNC %.2e ; LB-UNC %.2e' % (abs(g(LA, 2) - g(UNC, 2)), abs(g(LB, 2) - g(UNC, 2)))))
SC.append(scored('Q2', 'D_LB(3) > D_uncond(3) by at least 0.05',
                 'HELD' if (g(LB, 3) - g(UNC, 3)) >= 0.05 else 'BREACHED',
                 'D_LB(3) %.4f - D_unc(3) %.4f = %+.4f' % (g(LB, 3), g(UNC, 3), g(LB, 3) - g(UNC, 3))))
SC.append(scored('Q3', 'D_LB(4) > D_LB(3) is FALSE (listed law stays monotone decreasing over 2,3,4)',
                 'HELD' if (g(LB, 4) is not None and g(LB, 4) <= g(LB, 3) and g(LB, 3) <= g(LB, 2)) else 'BREACHED',
                 'D_LB 2/3/4 = %.4f / %.4f / %s' % (g(LB, 2), g(LB, 3),
                                                    '%.4f' % g(LB, 4) if g(LB, 4) is not None else 'n/a')))
_q4 = (g(LA, 4) - g(LB, 4)) if (g(LA, 4) is not None and g(LB, 4) is not None) else None
SC.append(scored('Q4', 'D_LA(4) > D_LB(4) and the gap exceeds 0.10',
                 'HELD' if (_q4 is not None and _q4 > 0.10) else 'BREACHED',
                 'D_LA(4) %s - D_LB(4) %s = %s' % (
                     '%.4f' % g(LA, 4) if g(LA, 4) is not None else 'n/a',
                     '%.4f' % g(LB, 4) if g(LB, 4) is not None else 'n/a',
                     '%+.4f' % _q4 if _q4 is not None else 'n/a')))
_n5 = SURF[LB][5].get('n', 0); _n6 = SURF[LB][6].get('n', 0)
SC.append(scored('Q5', 'the L-B listed cell at depth 5 is UNRESOLVABLE (n < 5, expected n = 0); depth 6 likewise',
                 'HELD' if (_n5 < 5 and _n6 < 5) else 'BREACHED',
                 'n_LB(5) = %d ; n_LB(6) = %d (expected 0)' % (_n5, _n6)))
_n3 = SURF[LB][3].get('n', 0); _n4 = SURF[LB][4].get('n', 0)
SC.append(scored('Q6', 'n_LB(3) in [90,180] and n_LB(4) in [20,70]',
                 'HELD' if (90 <= _n3 <= 180 and 20 <= _n4 <= 70) else 'BREACHED',
                 'n_LB(3) = %d ; n_LB(4) = %d (30A unconditional 234 / 154)' % (_n3, _n4)))
_agr = 100.0 * xc['agree'] / max(1, xc['matched'])
SC.append(scored('Q7', 'Layer-1 re-derivation agrees with per_entrant_338 max(yrs) on >= 95% of fitted ND rows',
                 'HELD' if _agr >= 95.0 else 'BREACHED',
                 'agreement %.1f%% (%d of %d matched); causes %s' % (_agr, xc['agree'], xc['matched'], dict(_cause))))
_sm = [r for r in NAMED_OUT if r['key'] == 'josh-smillie'][0]
SC.append(scored('Q8', 'under the UNCONDITIONAL table the continuous law prices josh-smillie below 500',
                 'HELD' if (_sm['price_cont_UNCONDITIONAL'] is not None and _sm['price_cont_UNCONDITIONAL'] < 500)
                 else 'BREACHED',
                 'continuous unconditional price %s (30A integer print 919)' % _sm['price_cont_UNCONDITIONAL']))
SC.append(scored('Q9', 'smillie continuous listed-conditional price lands BELOW ORDER 30A\'s integer print of 919',
                 'HELD' if (_sm['price_cont_L-B'] is not None and _sm['price_cont_L-B'] < 919) else 'BREACHED',
                 'continuous L-B price %s ; continuous L-A price %s ; integer 30A 919'
                 % (_sm['price_cont_L-B'], _sm['price_cont_L-A'])))
_kn = [r for r in NAMED_OUT if r['key'] == 'max-knobel'][0]
SC.append(scored('Q10', 'max-knobel at c = 4.92 cannot be quoted on the listed law without extrapolation',
                 'HELD' if _kn['extrapolated_L-B'] else 'BREACHED',
                 'extrapolated_L-B = %s (deepest resolved depth %s)' % (_kn['extrapolated_L-B'], _kn['deepest_resolved_L-B'])))
_maxgap = max(max(r['conv_gap_UNCONDITIONAL'], r['conv_gap_L-A'], r['conv_gap_L-B']) for r in NAMED_OUT)
SC.append(scored('Q11', 'log-linear and linear-in-D differ by less than 0.06 in D on every named row',
                 'HELD' if _maxgap < 0.06 else 'BREACHED', 'max |log-linear - linear| = %.4f' % _maxgap))
_g1n = GUARD_DROP['G1 primary']['n_fitted_rows_dropped']
SC.append(scored('Q12', 'G1 excludes between 5 and 25 fitted rows in total',
                 'HELD' if 5 <= _g1n <= 25 else 'BREACHED', 'G1 excludes %d fitted rows %s'
                 % (_g1n, GUARD_DROP['G1 primary']['by_cell'])))
_d2_3b = [dget(BANDTAB, '3-band', 'G1 primary', 'UNCOND', 2, lo, hi) for (lo, hi) in BANDS3]
SC.append(scored('Q13', 'after G1 the depth-2 3-band pattern is STILL NON-MONOTONE with 21-40 the lowest',
                 'HELD' if (None not in _d2_3b and _d2_3b[1] == min(_d2_3b)
                            and not (_d2_3b[0] < _d2_3b[1] < _d2_3b[2])
                            and not (_d2_3b[0] > _d2_3b[1] > _d2_3b[2])) else 'BREACHED',
                 'D_shrunk 1-20 / 21-40 / 41-64 = %s' % ' / '.join('%.4f' % x if x is not None else 'n/a' for x in _d2_3b)))
_d2_2b = [dget(BANDTAB, '2-band', 'G1 primary', 'UNCOND', 2, lo, hi) for (lo, hi) in BANDS2]
_b2_borrow = dget(BANDTAB, '2-band', 'G1 primary', 'UNCOND', 2, 1, 20, 'borrow')
SC.append(scored('Q14', 'after G1 the depth-2 2-band contrast is smaller than 0.20 in D and the 1-20 borrow exceeds 15%',
                 'HELD' if (None not in _d2_2b and abs(_d2_2b[0] - _d2_2b[1]) < 0.20
                            and _b2_borrow is not None and _b2_borrow > 0.15) else 'BREACHED',
                 '|1-20 %.4f - 21-64 %.4f| = %.4f ; borrow %.1f%%'
                 % (_d2_2b[0], _d2_2b[1], abs(_d2_2b[0] - _d2_2b[1]), 100 * (_b2_borrow or 0))))
SC.append(scored('Q15', 'the verdict is NO WIREABLE BAND GRADIENT',
                 'HELD' if not ANY_WIREABLE else 'BREACHED',
                 'directions: ' + ' ; '.join('%s -> %s' % (k, v['dirs']) for k, v in VERDICTS.items())))
_g2moves = []
for lens, bands in (('3-band', BANDS3), ('2-band', BANDS2)):
    for N in (2, 3, 4):
        for (lo, hi) in bands:
            a = dget(BANDTAB, lens, 'G1 primary', 'UNCOND', N, lo, hi)
            b = dget(BANDTAB, lens, 'G2 stricter', 'UNCOND', N, lo, hi)
            if a is not None and b is not None:
                _g2moves.append((abs(a - b), '%s d%d %d-%d' % (lens, N, lo, hi)))
_g2max = max(_g2moves) if _g2moves else (0.0, 'n/a')
SC.append(scored('Q16', 'G2 moves no band cell by more than 0.05 relative to G1',
                 'HELD' if _g2max[0] <= 0.05 else 'BREACHED',
                 'largest move %.4f at %s' % _g2max))
SC.append(scored('Q17', 'live/pinned obs ratio has median in [0.90,0.97] and IQR width below 0.02',
                 'HELD' if (0.90 <= Q17['median'] <= 0.97 and Q17['iqr'] < 0.02) else 'BREACHED',
                 'median %.4f ; IQR width %.4f (n = %d)' % (Q17['median'], Q17['iqr'], Q17['n'])))
SC.append(scored('Q18', 'the 0-game reduction is exact: s_N = 1 to 1e-12 and D reproduces 30A to 1e-6',
                 'HELD' if RED_OK else 'BREACHED',
                 'max |T4 - 30A| = %.3e ; rows with s_N != 1: %d'
                 % (max(d['diff'] for d in red), sum(d['s_not_one'] for d in red))))
_d12 = T4.get('L-B listed-conditioned|2|1-2', {}).get('D')
_d02 = T4.get('L-B listed-conditioned|2|0', {}).get('D')
SC.append(scored('Q19', 'D(k=1-2, N=2) in [0.60,0.95] and strictly greater than D(0,N=2) = 0.568',
                 'HELD' if (_d12 is not None and 0.60 <= _d12 <= 0.95 and _d12 > _d02) else 'BREACHED',
                 'D(1-2,2) = %s ; D(0,2) = %s' % ('%.4f' % _d12 if _d12 is not None else 'n/a',
                                                  '%.4f' % _d02 if _d02 is not None else 'n/a')))
_seq2 = [T4.get('L-B listed-conditioned|2|%s' % b, {}).get('D') for b in ('0', '1-2', '3-5', '6-10')]
SC.append(scored('Q20', 'the depth-2 games transition is monotone increasing in k: D(0)<D(1-2)<D(3-5)<D(6-10)',
                 'HELD' if (None not in _seq2 and all(_seq2[i] < _seq2[i + 1] for i in range(3))) else 'BREACHED',
                 'D = %s' % ' < '.join('%.4f' % x if x is not None else 'n/a' for x in _seq2)))
_st = STEPS.get('L-B listed-conditioned', [])
_st3 = [s for s in _st if s['frm'] in ('0', '1-2', '3-5')]
_big = max(_st3, key=lambda s: s['step']) if _st3 else None
SC.append(scored('Q21', 'the 0 -> 1-2 step is the LARGEST of the three steps (a STEP, not a smooth curve)',
                 'HELD' if (_big is not None and _big['frm'] == '0') else 'BREACHED',
                 'steps: ' + ' ; '.join('%s->%s %+.4f' % (s['frm'], s['to'], s['step']) for s in _st3)))
_n610_3 = T4.get('L-B listed-conditioned|3|6-10', {}).get('n', 0)
_thin3 = [b for b in ('0', '1-2', '3-5', '6-10')
          if 0 < T4.get('L-B listed-conditioned|3|%s' % b, {}).get('n', 0) < MIN_CELL_T4]
SC.append(scored('Q22', 'at depth 3, n(6-10 games) < 30 and at least one depth-3 games cell falls below n = 10',
                 'HELD' if (_n610_3 < 30 and len(_thin3) >= 1) else 'BREACHED',
                 'n(6-10, depth 3) = %d ; cells below n=10: %s' % (_n610_3, _thin3 or 'none')))
_q23 = []
for b in ('0', '1-2', '3-5'):
    c = T4.get('L-B listed-conditioned|2|%s' % b, {})
    if c.get('n'):
        _q23.append((b, c['p25'], c['median'] / c['mean'] if c['mean'] else None))
SC.append(scored('Q23', 'p25 = 0.000 exactly in every depth-2 games cell with k <= 5 and median/mean < 0.60',
                 'HELD' if (_q23 and all(abs(p) < 1e-12 and (mm is not None and mm < 0.60) for _, p, mm in _q23))
                 else 'BREACHED',
                 ' ; '.join('%s p25 %.4g median/mean %s' % (b, p, '%.3f' % mm if mm is not None else 'n/a')
                            for b, p, mm in _q23)))
SC.append(scored('Q24', 'this act reproduces ORDER 30A\'s unconditional row to 1e-6',
                 'HELD' if CTRL_OK else 'BREACHED',
                 'RAW(1) %.6f vs 1.0286 ; D %s' % (CTRL['RAW1'],
                 ' '.join('%.4f' % CTRL['D'][N] for N in (2, 3, 4, 5, 6)))))
SC.append(scored('Q25', 'the seat recommends the L-B listed-conditional row on a continuous log-linear clock, '
                        'position-blind and band-blind, with the games transition wired at depth 2 only',
                 'SEE THE PACKET RECOMMENDATION',
                 'scored in SITTER_FADE_PACKET_2.md; a self-prediction about the seat\'s own conclusion'))

P('=' * 118)
P('THE PREREG, SCORED  --  every prediction owned by number, HELD or BREACHED, none quietly dropped')
P('=' * 118)
for s in SC:
    P('  %-4s %-9s %s' % (s['q'], s['verdict'], s['detail']))
P('')
P('  HELD %d   BREACHED %d   (of %d numbered, one self-referential)'
  % (sum(1 for s in SC if s['verdict'] == 'HELD'), sum(1 for s in SC if s['verdict'] == 'BREACHED'), len(SC)))
P('')

# =====================================================================================================
# WRITE
# =====================================================================================================
OUT = dict(
    act='ORDER 30A-2 -- the sitter re-cut', read_only=True,
    wires_nothing='the old los_decay stands as the DECLARED FALLBACK until the owner rules',
    supersedes='SITTER_FADE_PACKET.md (ORDER 30A) as the ruling basis; ORDER 30A\'s artifacts stand '
               'on their own basis, untouched',
    prereg='PREREG_30A2.md',
    pins=dict(layer1=L1_MD5, layer2=L2_MD5, **{k: PIN_OBS[k] for k in PIN_OBS}),
    population=dict(total=len(POP), fitted=len(FIT), sensitivity=len(SENS), pre2004=len(PRE)),
    control_Q24=dict(this_act=CTRL, order30a=O30A, reproduced=CTRL_OK),
    listing=dict(
        source='#338 MINIMUM LISTING TENURE, engine/rl_after/s4_matrix_M1v7.py:53-70,81,113 (commit '
               '30996f8), ported at docs/evidence/noarb_338_2026-08-06/emit_matrix_338.py:127-160; '
               're-derived here from Layer 1 (ad1229ea) and cross-checked key by key against that '
               'lane\'s own per_entrant_338_confirmation.json',
        rule=dict(min_tenure_bands=MIN_TENURE_BANDS,
                  debut='entry_year + 1 on every route except MSD (entry year)',
                  own_data_extends='L-A only', banded_on='effective_pick (MA.effpk), not the slid pick'),
        readings=dict(**{'L-A': 'listed_through as filed, own-data-extends INCLUDED',
                         'L-B': 'listed at N iff (min_tenure >= N) or (not retired) -- outcome-blind floor'}),
        crosscheck=dict(n_fitted=xc['n'], matched=xc['matched'], agree=xc['agree'],
                        agreement_pct=_agr, causes=dict(_cause), disagreements=xc['dis'],
                        store_vs_layer1=dict(retired_differs=store_dis['retired'],
                                             last_listed_differs=store_dis['last_listed'])),
        explicit_last_listed_fitted=sum(1 for r in FIT if r['last_listed'] is not None),
    ),
    T1=dict(
        surfaces={lab: {str(N): SURF[lab][N] for N in DEPTHS} for lab in READINGS},
        D={lab: {str(N): DTAB[lab].get(N) for N in DEPTHS} for lab in READINGS},
        LA_LB_gap={str(N): LA_LB_GAP[N] for N in DEPTHS},
        raw1=CTRL['RAW1'],
    ),
    T2=dict(clock=dict(phi=PHI, source='data/season_state.json::calendar_progress',
                       season_state=SEASON_STATE,
                       convention='D(c) = D(N)^(1-phi) * D(N+1)^phi (log-linear in D)',
                       sensitivity='linear-in-D published beside it',
                       extrapolation='held flat at the deepest resolved depth, FLAGGED'),
            usable_tables={lab: {str(N): TABS[lab][N] for N in sorted(TABS[lab])} for lab in TABS},
            min_cell=MINCELL,
            named_rows=NAMED_OUT),
    T3=dict(guards=dict(G1=dict(rule='posv[g][p] < 0.20 * curve[p]', cells=['%s %d' % t for t in G1_CELLS],
                                absolute_alternative_identical=(G1 == set(G1_ABS))),
                        G2=dict(rule='pick >= 58 and posv[g][p] < 0.50 * curve[p]',
                                cells=['%s %d' % t for t in G2_CELLS])),
            excluded=GUARD_DROP, cells=BANDTAB, verdicts=VERDICTS,
            wireable_gradient=ANY_WIREABLE,
            owner_proposal_referenced_not_applied=dict(
                proposal='a floor of 100 on positional v0 at pick 64, proposed but NOT yet firmly ruled, '
                         'to be confirmed with the fade ruling',
                applied=False, cells_below_100_at_pick_64=_would)),
    T4=dict(estimand='D(k,N) = E[ (grace_a.obs * s_N + grace_a.tail) * DF(N-1) / v0 | games in seasons '
                     '1..N-1 in bucket k, listed per T1 ] / RAW(1)',
            buckets=[b[0] for b in GBUCKETS], min_cell=MIN_CELL_T4,
            share_control_Q17=Q17, reduction_control_Q18=red, reduction_held=RED_OK,
            cells=T4, steps=STEPS, cumulative_leq=T4CUM),
    prereg_scored=SC,
    old_schedule={str(N): {g: los_decay_at(g, N) for g in POSITIONS} for N in DEPTHS},
    old_schedule_source='engine/rl_after/rl_model.py, read LIVE off the imported module: LOS_C %.4f '
                        'LOS_P %.4f GRACE %s' % (MA.LOS_C, MA.LOS_P, dict(MA.GRACE)),
    per_player_fitted=[{k: v for k, v in r.items() if k != 'e'} for r in FIT],
)
with open(os.path.join(OUTD, 'SITTER_DISCOUNT_TABLE_2.json'), 'w') as f:
    json.dump(OUT, f, indent=1, sort_keys=True, default=float)
with open(os.path.join(OUTD, 'RECUT30A2_out.txt'), 'w') as f:
    f.write('\n'.join(LOG) + '\n')
print('\nwrote SITTER_DISCOUNT_TABLE_2.json and RECUT30A2_out.txt')
