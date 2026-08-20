#!/usr/bin/env python3
# =====================================================================================================
# ORDER 32 SEAT S7 -- THE PEDIGREE-LEG CELL FANS.  READ-ONLY.  PREREG: PREREG_S7.md (pushed first).
#
# Empirical outcome quantiles (q10/q30/q50/q70/q90/q97 -- the production fan's six levels) of realized
# career delivered value (grace-A total, #338 minimum-tenure basis) per:
#   ND lane   : pick band x position, on the v0 fit's OWN input rows (o31f_headfix.py:80-85 verbatim)
#   pool lane : pool arm (position-pooled primary), on o31f_pool.py's OWN POP construction, riding the
#               o30a2_recut.py prefix exec'd VERBATIM (md5-pinned)
#
# Nothing is smoothed, shrunk, winsorised or borrowed. Thin cells are BOUNDED per PREREG §5.
# WRITES ONLY: CELLFANS_S7.json / CELLFANS_S7.md / CELLFANS_S7_out.txt in this directory.
# =====================================================================================================
import os, sys, io, json, math, hashlib, collections, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(EV))
os.chdir(ROOT)

LOG = []
def P(s=''):
    print(s); LOG.append(s)

md5s = lambda t: hashlib.md5(t.encode()).hexdigest()

LEVELS = [0.10, 0.30, 0.50, 0.70, 0.90, 0.97]
LNAMES = ['q10', 'q30', 'q50', 'q70', 'q90', 'q97']
N_FLOOR = 8           # the project's own N_FLOOR (POOL31F.json fade.n_floor)
ZERO = 1e-9

P('=' * 118)
P('ORDER 32 S7 -- THE PEDIGREE-LEG CELL FANS.  PREREG_S7.md governs; committed before this ran.')
P('=' * 118)
P('')

# =====================================================================================================
# ND LANE -- the v0 fit's own rows (o31f_headfix.py:80-85, replicated verbatim; control below)
# =====================================================================================================
O28 = os.path.join(EV, 'grace_adoption_2026-08-13')
L2 = json.load(open(os.path.join(O28, 'inputs/LAYER2.json')))
L1 = json.load(open(os.path.join(O28, 'inputs/layer1_player_seasons.json')))
E = {e['key']: e for e in L1['entries']}; ATTR = L2['attribution']; GA = L2['grace_a']
nd = [dict(key=k, pick=ATTR[k]['pick'], value=GA[k]['total'], pos=E[k]['position_group'])
      for k in L2['fit_nd_keys']]
POS = ['KPD', 'KPF', 'MID', 'RUCK', 'SD', 'SF']

C1_TARGET = {'KPD': 125, 'KPF': 143, 'MID': 422, 'RUCK': 60, 'SD': 180, 'SF': 212}
got = collections.Counter(r['pos'] for r in nd)
C1_OK = (len(nd) == 1142) and all(got[g] == C1_TARGET[g] for g in POS)
P('CONTROL C1 -- the ND population IS the fit population (HEADFIX_31F_out.txt line 5)')
P('  rows %d (target 1142)   per-position %s' % (len(nd), dict(got)))
P('  VERDICT %s' % ('REPRODUCED' if C1_OK else '*** DRIFT -- HALT ***'))
if not C1_OK:
    raise SystemExit('S7 HALT: ND population drifted from the fit population')
P('')

HEADFIX = json.load(open(os.path.join(EV, 'candidate_31f', 'HEADFIX_31F.json')))
POSV = {g: {int(p): float(v) for p, v in HEADFIX['posv_headfixed'][g].items()} for g in POS}

# =====================================================================================================
# POOL LANE -- the o30a2 prefix exec'd verbatim, then o31f_pool.py's own POP loop (control below)
# =====================================================================================================
SRC30A2 = os.path.join(EV, 'sitter_fade_2026-08-14', 'o30a2_recut.py')
_t = open(SRC30A2).read()
MD5_30A2 = md5s(_t)
P('POOL PREFIX -- %s  md5 %s  (must equal POOL31F.json instruments.fade.md5)' %
  (os.path.relpath(SRC30A2, ROOT), MD5_30A2))
if MD5_30A2 != 'fe6f436ab23056d717f693091946309a':
    raise SystemExit('S7 HALT: o30a2_recut.py md5 drifted from the POOL31F pin')
NS = {'__name__': 'o30a2_prefix', '__file__': SRC30A2}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_t[:_t.index('\nSURF = collections.OrderedDict(')], SRC30A2, 'exec'), NS)
ENTRIES, ATTR2, GA2 = NS['ENTRIES'], NS['ATTR'], NS['GA']
leading_sit, ever_played = NS['leading_sit'], NS['ever_played']
min_tenure_338, resolution_class = NS['min_tenure_338'], NS['resolution_class']
listed_through_LA = NS['listed_through_LA']
MA = NS['MA']
q = NS['q']                                   # THE PROJECT'S OWN QUANTILE ESTIMATOR, reused

_bk = {}
for _p in MA.data:
    _bk.setdefault(_p.get('key') or MA.slug(_p['player']), _p)
def pool_v0(key):
    p = _bk.get(key)
    if p is None or not p.get('_pool'): return None
    try: v = MA.pool_v0_of(p)
    except Exception: return None
    return float(v) if v else None

# --- o31f_pool.py:69-83, verbatim (one field ADDED: pos = e['day0_position'], used only to split) ---
POP, SKIP = [], collections.Counter()
for e in ENTRIES:
    a = ATTR2.get(e['key'])
    if not a or a.get('excluded'): SKIP['no attribution / excluded'] += 1; continue
    if a.get('mechanism') == 'ND 1-64' or e['type'] == 'ND': continue
    v0 = pool_v0(e['key'])
    if not v0 or v0 <= 0: SKIP['no signed pool v0 cell'] += 1; continue
    if e['entry_year'] is None: SKIP['no entry year'] += 1; continue
    if e['key'] not in GA2: SKIP['no grace-A career score'] += 1; continue
    POP.append(dict(key=e['key'], entry_year=e['entry_year'], pathway=e['type'],
                    mech=a.get('mechanism'), v0=v0, retired=e['retired'], last_listed=e['last_listed'],
                    maxdepth=1 + leading_sit(e), ever=ever_played(e), min_tenure=min_tenure_338(e),
                    listed_through_LA=listed_through_LA(e), res=resolution_class(e),
                    ga_total=float(GA2[e['key']]['total']), ga_tshare=float(GA2[e['key']]['tail_share']),
                    pos=e['day0_position'], e=e))
FIT = [r for r in POP if 2004 <= r['entry_year'] <= 2021]

C2_OK = (len(FIT) == 840 and len(POP) == 1080)
P('CONTROL C2 -- the pool population IS the pool fit population (POOL31F.json fade)')
P('  fitted 2004-2021 %d (target 840)   total %d (target 1080)   skips %s'
  % (len(FIT), len(POP), dict(SKIP)))
P('  VERDICT %s' % ('REPRODUCED' if C2_OK else '*** DRIFT -- HALT ***'))
if not C2_OK:
    raise SystemExit('S7 HALT: pool population drifted from the fit population')
P('')

# =====================================================================================================
# THE FAN -- one function, PREREG §4-§6.  No smoothing, no borrowing; bounds where thin.
# =====================================================================================================
def fan(vals):
    n = len(vals)
    out = dict(n=n)
    if n == 0:
        return out
    vs = sorted(vals)
    out['n_zero'] = sum(1 for x in vs if x <= ZERO)
    out['zero_share'] = out['n_zero'] / n
    out['mean'] = sum(vs) / n
    out['min'] = vs[0]; out['max'] = vs[-1]
    out['median'] = q(vs, 0.5)
    if n < N_FLOOR:
        out['status'] = 'UNRESOLVED (n < %d): min/median/max only' % N_FLOOR
        return out
    out['status'] = 'resolved'
    out['levels'] = {}
    for f, nm in zip(LEVELS, LNAMES):
        resolved = (n * (1.0 - f) >= 1.0)
        out['levels'][nm] = dict(value=(q(vs, f) if resolved else vs[-1]),
                                 resolved=resolved,
                                 flag=('' if resolved else 'BOUND(max)'))
    md = out['median']
    out['mean_over_median'] = (out['mean'] / md) if md > ZERO else None
    return out


def fanrow(c):
    if c['n'] == 0:
        return '     -- empty --'
    if 'levels' not in c:
        return ('n=%4d  n0=%3d (%4.0f%%)  min %8.1f  med %8.1f  max %8.1f   %s'
                % (c['n'], c['n_zero'], 100 * c['zero_share'], c['min'], c['median'], c['max'],
                   c['status']))
    L = c['levels']
    cells = ' '.join('%8.1f%s' % (L[nm]['value'], '*' if not L[nm]['resolved'] else ' ')
                     for nm in LNAMES)
    mm = ('%6.1f' % c['mean_over_median']) if c['mean_over_median'] is not None else '   inf'
    return ('n=%4d  n0=%3d (%4.0f%%)  %s  mean %8.1f  mean/med %s'
            % (c['n'], c['n_zero'], 100 * c['zero_share'], cells, c['mean'], mm))


BANDS = [(1, 10), (11, 20), (21, 30), (31, 40), (41, 64)]
FINER = [(a, min(a + 4, 64)) for a in range(1, 62, 5)]     # 1-5, 6-10, ..., 56-60, 61-64

OUT = {'prereg': 'PREREG_S7.md', 'levels': LNAMES, 'weights_production_fan': 'WQ6 = [.18 x5, .10]',
       'value': 'grace_a total (#338 minimum-tenure basis), the fit target itself; no DF, no smoothing',
       'estimator': "o30a2_recut.py q() -- linear interpolation between order statistics",
       'n_floor': N_FLOOR,
       'resolution_rule': 'level f resolved iff n*(1-f) >= 1; else BOUND(max), flagged, never smoothed',
       'controls': {'C1_nd_population': {'n': len(nd), 'per_pos': dict(got), 'ok': C1_OK},
                    'C2_pool_population': {'fitted': len(FIT), 'total': len(POP), 'ok': C2_OK},
                    'o30a2_md5': MD5_30A2},
       'nd': {}, 'nd_finer': {}, 'pool': {}, 'pool_by_pos': {}}

# ---- ND: pick band x position + position-pooled row -------------------------------------------------
P('=' * 118)
P('ND LANE -- OUTCOME FANS PER PICK BAND x POSITION   (* = BOUND(max), an unresolved level)')
P('  columns: %s   value = realized career delivered value (grace-A total)' % ' '.join(LNAMES))
P('=' * 118)
for (lo, hi) in BANDS:
    P('')
    P('BAND %d-%d' % (lo, hi))
    rows_band = [r for r in nd if lo <= r['pick'] <= hi]
    c = fan([r['value'] for r in rows_band])
    v0c = sum(POSV[r['pos']][r['pick']] for r in rows_band) / max(1, len(rows_band))
    c['v0_comparator'] = v0c
    c['mean_over_v0'] = c.get('mean', 0) / v0c if v0c else None
    OUT['nd']['%d-%d|ALL' % (lo, hi)] = c
    P('  %-5s %s' % ('ALL', fanrow(c)))
    P('        fitted-v0 comparator (head-fixed posv over the cell rows) %8.1f   mean/v0 %.3f'
      % (v0c, c['mean_over_v0']))
    for g in POS:
        rows = [r for r in rows_band if r['pos'] == g]
        c = fan([r['value'] for r in rows])
        if rows:
            v0c = sum(POSV[g][r['pick']] for r in rows) / len(rows)
            c['v0_comparator'] = v0c
            c['mean_over_v0'] = (c.get('mean', 0) / v0c) if v0c else None
        OUT['nd']['%d-%d|%s' % (lo, hi, g)] = c
        P('  %-5s %s' % (g, fanrow(c)))

# ---- ND finer cut (conditional on every cell n >= 34, PREREG §3) ------------------------------------
P('')
P('ND FINER CUT -- position-pooled 5-pick bands (published only if EVERY cell n >= 34)')
fine = {}
for (lo, hi) in FINER:
    rows = [r for r in nd if lo <= r['pick'] <= hi]
    fine['%d-%d' % (lo, hi)] = fan([r['value'] for r in rows])
supported = all(c['n'] >= 34 for c in fine.values())
P('  cell n: %s' % '  '.join('%s:%d' % (k, c['n']) for k, c in fine.items()))
P('  SUPPORTED: %s' % supported)
if supported:
    for k, c in fine.items():
        rows = [r for r in nd if int(k.split('-')[0]) <= r['pick'] <= int(k.split('-')[1])]
        v0c = sum(POSV[r['pos']][r['pick']] for r in rows) / len(rows)
        c['v0_comparator'] = v0c; c['mean_over_v0'] = c['mean'] / v0c if v0c else None
        OUT['nd_finer'][k] = c
        P('  %-6s %s' % (k, fanrow(c)))
else:
    OUT['nd_finer'] = {'unsupported': True, 'cell_n': {k: c['n'] for k, c in fine.items()}}
P('')

# ---- POOL: per arm, position-pooled -----------------------------------------------------------------
ARMS_DECLARED = ['RD', 'SSP', 'MSD', 'UNR', 'IRE', 'PDA', 'PDN', 'PDS']
arms_seen = sorted({r['pathway'] for r in FIT})
extra = [a for a in arms_seen if a not in ARMS_DECLARED]
P('=' * 118)
P('POOL LANE -- OUTCOME FANS PER POOL ARM (position-pooled; fitted window 2004-2021)')
P('  arms seen: %s%s' % (arms_seen, ('   OUTSIDE THE DECLARED LIST: %s' % extra) if extra else ''))
P('=' * 118)
for arm in ARMS_DECLARED + extra:
    rows = [r for r in FIT if r['pathway'] == arm]
    c = fan([r['ga_total'] for r in rows])
    if rows:
        v0c = sum(r['v0'] for r in rows) / len(rows)
        c['v0_comparator'] = v0c
        c['mean_over_v0'] = (c.get('mean', 0) / v0c) if v0c else None
    OUT['pool'][arm] = c
    P('  %-4s %s' % (arm, fanrow(c)))
    if rows and c.get('mean') is not None:
        P('       mean signed pool v0 of the cell rows %8.1f   mean/v0 %s'
          % (c['v0_comparator'], ('%.3f' % c['mean_over_v0']) if c['mean_over_v0'] else '-'))

# ---- POOL per-position split where an arm x position cell has n >= 20 -------------------------------
P('')
P('POOL ARM x POSITION SPLIT -- published only where the cell has n >= 20 (a split of a thin arm)')
any_split = False
for arm in ARMS_DECLARED + extra:
    for g in sorted({r['pos'] for r in FIT if r['pathway'] == arm}):
        rows = [r for r in FIT if r['pathway'] == arm and r['pos'] == g]
        if len(rows) < 20:
            continue
        any_split = True
        c = fan([r['ga_total'] for r in rows])
        v0c = sum(r['v0'] for r in rows) / len(rows)
        c['v0_comparator'] = v0c; c['mean_over_v0'] = c['mean'] / v0c if v0c else None
        OUT['pool_by_pos']['%s|%s' % (arm, g)] = c
        P('  %-4s %-5s %s' % (arm, g, fanrow(c)))
if not any_split:
    P('  -- no arm x position cell reaches n >= 20 --')
P('')

# ---- the signature-shape statement, mechanically evaluated ------------------------------------------
P('=' * 118)
P('SIGNATURE SHAPES (PREREG §7), mechanically evaluated')
P('=' * 118)
late = OUT['nd']['41-64|ALL']; early = OUT['nd']['1-10|ALL']
P('  late picks 41-64 ALL : median %.1f vs mean %.1f, zero-share %.0f%%, q90 %.1f, q97 %.1f'
  % (late['median'], late['mean'], 100 * late['zero_share'],
     late['levels']['q90']['value'], late['levels']['q97']['value']))
P('  early picks 1-10 ALL : median %.1f vs mean %.1f, zero-share %.0f%%, mean/med %.2f'
  % (early['median'], early['mean'], 100 * early['zero_share'], early['mean_over_median']))
skew_cells = [(k, c) for k, c in OUT['nd'].items() if c.get('mean_over_median') is not None]
n_skew = sum(1 for _, c in skew_cells if c['mean_over_median'] > 1.0)
P('  mean > median in %d of %d resolved ND cells with a finite ratio' % (n_skew, len(skew_cells)))
mm_by_band = [(('%d-%d' % b), OUT['nd']['%d-%d|ALL' % b].get('mean_over_median')) for b in BANDS]
P('  mean/median by band (ALL): %s'
  % '  '.join('%s:%s' % (k, ('%.2f' % v) if v else 'inf') for k, v in mm_by_band))
OUT['signature'] = {'late_41_64_ALL': {'median': late['median'], 'mean': late['mean'],
                                       'zero_share': late['zero_share']},
                    'early_1_10_ALL': {'median': early['median'], 'mean': early['mean'],
                                       'zero_share': early['zero_share']},
                    'mean_gt_median_cells': [n_skew, len(skew_cells)],
                    'mean_over_median_by_band_ALL': dict(mm_by_band)}

json.dump(OUT, open(os.path.join(HERE, 'CELLFANS_S7.json'), 'w'), indent=1, sort_keys=True)
open(os.path.join(HERE, 'CELLFANS_S7_out.txt'), 'w').write('\n'.join(LOG) + '\n')
print('\nCELLFANS_S7.json / CELLFANS_S7_out.txt written.')
