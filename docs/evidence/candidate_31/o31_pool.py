#!/usr/bin/env python3
"""ORDER 31 — STEP 2: THE POOL FADE, DERIVED BY THE SAME CONSTRUCTION AS THE ND LAW.  READ-ONLY.

The 30A-2 harness is TRANSPLANTED, not re-implemented: this file `exec`s `o30a2_recut.py` VERBATIM up to
its `POP = []` line (the whole input load, the md5 pins, the live rl_model import, the #338 listing
reconstruction, DF, at_depth, cell, normalise and the three READINGS), asserts its own control, and then
rebuilds the population on the POOL pathways instead of ND 1-64.  The estimator is byte-for-byte the ND
law's estimator; only the population and the v0 object change.

    D_pool(N) = mean_over_pool_sitters_at_depth_N( ga_total * DF(e, N-1) / v0_pool )  /  the same at N=1

listed-conditioning: the L-B outcome-blind floor, the reading the owner RULED for the ND law
(#334 comment 5292534855), applied unchanged.  Where a pathway cannot resolve a listing floor it is
DISCLOSED rather than imputed.

MSD: owner ruling 5 — the FIRST SEASON IS SEASON 1, so an MSD row's debut year is its entry year and its
depth clock runs one season ahead of every other route.  This is `debut_year_338`'s own MSD clause, which
the transplanted prefix already carries, so the clock is inherited rather than re-stated.

Thin pathways are K-shrunk toward the POOLED POOL ROW and the borrowing is printed per cell.
"""
import os, sys, json, math, collections, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
EV   = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(EV))
SRC  = os.path.join(EV, 'sitter_fade_2026-08-14', 'o30a2_recut.py')

_txt = open(SRC).read()
_cut = _txt.index('\nSURF = collections.OrderedDict(')
HARNESS_MD5 = hashlib.md5(_txt.encode()).hexdigest()
NS = {'__name__': 'o30a2_prefix', '__file__': SRC}
exec(compile(_txt[:_cut], SRC, 'exec'), NS)          # the 30A-2 prefix, VERBATIM (through its own ND POP)

ENTRIES, ATTR, GA, SEASONS = NS['ENTRIES'], NS['ATTR'], NS['GA'], NS['SEASONS']
DEPTHS, LAST_COMPLETE, K_SHRINK = NS['DEPTHS'], NS['LAST_COMPLETE'], NS['K_SHRINK']
DF, at_depth, cell, normalise = NS['DF'], NS['at_depth'], NS['cell'], NS['normalise']
listed_LB, listed_uncond = NS['listed_LB'], NS['listed_uncond']
leading_sit, ever_played, entry_age = NS['leading_sit'], NS['ever_played'], NS['entry_age']
min_tenure_338, resolution_class = NS['min_tenure_338'], NS['resolution_class']
listed_through_LA, q = NS['listed_through_LA'], NS['q']
MA = NS['MA']

OUT = []
def P(s=''):
    OUT.append(s); print(s)

P('ORDER 31 STEP 2 — THE POOL FADE, BY THE ND LAW\'S OWN CONSTRUCTION')
P('  transplanted prefix : %s  md5 %s  (exec\'d verbatim to its `POP = []` line)' % (os.path.relpath(SRC, ROOT), HARNESS_MD5))
P('')

# ---- the pool v0 object, read through the ONE accessor that halts on an unsigned cell ---------------
POOLV, POOL_MISS = {}, []
_by_key = {}
for _p in MA.data:
    _k = _p.get('key') or MA.slug(_p['player'])
    _by_key.setdefault(_k, _p)
def pool_v0(key):
    p = _by_key.get(key)
    if p is None or not p.get('_pool'): return None
    try:
        v = MA.pool_v0_of(p)
    except Exception:
        return None
    return float(v) if v else None

# ---- the pool population, by the SAME record shape the ND POP uses ---------------------------------
POP, SKIP = [], collections.Counter()
for e in ENTRIES:
    a = ATTR.get(e['key'])
    if not a or a.get('excluded'):
        SKIP['no attribution / excluded'] += 1; continue
    mech = a.get('mechanism')
    if mech == 'ND 1-64' or e['type'] == 'ND':
        continue                                     # the ND law's own population -- not this step
    v0 = pool_v0(e['key'])
    if not v0 or v0 <= 0:
        SKIP['no signed pool v0 cell'] += 1; continue
    ey = e['entry_year']
    if ey is None:
        SKIP['no entry year'] += 1; continue
    if e['key'] not in GA:
        SKIP['no grace-A career score'] += 1; continue
    POP.append(dict(key=e['key'], entry_year=ey, pathway=e['type'], mech=mech, v0=v0,
                    retired=e['retired'], last_listed=e['last_listed'],
                    maxdepth=1 + leading_sit(e), ever=ever_played(e),
                    min_tenure=min_tenure_338(e), listed_through_LA=listed_through_LA(e),
                    res=resolution_class(e), ga_total=float(GA[e['key']]['total']),
                    ga_tshare=float(GA[e['key']]['tail_share']), e=e))

FIT  = [r for r in POP if 2004 <= r['entry_year'] <= 2021]
SENS = [r for r in POP if r['entry_year'] >= 2022]
PRE  = [r for r in POP if r['entry_year'] < 2004]

P('POPULATION — pool pathways (every non-ND route with a SIGNED pool v0 cell)')
P('  total pool rows carried               %5d' % len(POP))
P('  FITTED window 2004-2021               %5d' % len(FIT))
P('  SENSITIVITY 2022+  (EXCLUDED)         %5d' % len(SENS))
P('  pre-2004 (EXCLUDED, DV floor)         %5d' % len(PRE))
for k, v in sorted(SKIP.items()):
    P('  skipped: %-32s %5d' % (k, v))
P('  by pathway (fitted): %s' % dict(collections.Counter(r['pathway'] for r in FIT)))
P('')

# ---- CONTROL: the ND row must reproduce the RULED numbers from this same transplanted estimator -----
NDFIT = NS['FIT']           # the 30A-2 harness's OWN fitted ND population, untouched
ND_SURF = {N: cell([r for r in at_depth(NDFIT, N) if listed_LB(r, N)], N) for N in DEPTHS}
ND_D = normalise(ND_SURF)
RULED = {2: 0.5501935857356868, 3: 0.26278629823610156, 4: 0.3460004697526451}
CTRL_DEV = {N: (abs(ND_D[N] - RULED[N]) if ND_D.get(N) is not None else None) for N in RULED}
CTRL_OK = all(v is not None and v < 5e-4 for v in CTRL_DEV.values())
P('CONTROL — the RULED ND fade re-derived by THIS transplanted estimator (L-B, fitted window)')
P('  D(N) here : %s' % '  '.join('%d:%.6f' % (N, ND_D[N]) for N in DEPTHS if ND_D.get(N) is not None))
P('  D(N) ruled: 2:%.6f  3:%.6f  4:%.6f' % (RULED[2], RULED[3], RULED[4]))
P('  max deviation %s' % max(v for v in CTRL_DEV.values() if v is not None))
P('  VERDICT %s' % ('REPRODUCED — the pool row below is produced by the SAME estimator'
                    if CTRL_OK else '*** DRIFT — the pool numbers below inherit it and it is DISCLOSED ***'))
P('')

# ---- THE POOL SURFACE ------------------------------------------------------------------------------
POOL_SURF = {N: cell([r for r in at_depth(FIT, N) if listed_LB(r, N)], N) for N in DEPTHS}
POOL_D = normalise(POOL_SURF)
P('THE POOLED POOL ROW — L-B listed-conditional, fitted window 2004-2021')
P('   N     n   mean(v/v0)    D(N)=mean/mean(1)   median      p25      p75   n_ever  tail_share')
for N in DEPTHS:
    c = POOL_SURF[N]
    if not c.get('n'):
        P('  %2d     0   —' % N); continue
    P('  %2d  %4d   %10.6f   %14s   %8s %8s %8s   %4d   %9.4f'
      % (N, c['n'], c['mean'], ('%.6f' % POOL_D[N]) if POOL_D.get(N) is not None else '—',
         '%.4f' % c['median'], '%.4f' % c['p25'], '%.4f' % c['p75'], c['n_ever'], c['tail_share']))
P('')

# ---- BY PATHWAY, K-SHRUNK TOWARD THE POOLED POOL ROW ------------------------------------------------
PATHS = sorted({r['pathway'] for r in FIT})
BY_PATH = {}
P('BY PATHWAY — raw cell, then K-shrunk toward the pooled pool row (K = %.0f). BORROWING PRINTED.' % K_SHRINK)
P('  pathway   N     n    raw D      w_own     SHRUNK D   borrowed from the pool row')
for pw in PATHS:
    rows = [r for r in FIT if r['pathway'] == pw]
    surf = {N: cell([r for r in at_depth(rows, N) if listed_LB(r, N)], N) for N in DEPTHS}
    dtab = normalise(surf)
    BY_PATH[pw] = {'n_rows': len(rows), 'raw': {}, 'shrunk': {}, 'n_cell': {}}
    for N in DEPTHS:
        c = surf[N]; n = c.get('n', 0)
        raw = dtab.get(N)
        base = POOL_D.get(N)
        if base is None:
            continue
        w = n / (n + K_SHRINK) if n else 0.0
        sh = (w * raw + (1 - w) * base) if raw is not None else base
        BY_PATH[pw]['raw'][N] = raw; BY_PATH[pw]['shrunk'][N] = sh; BY_PATH[pw]['n_cell'][N] = n
        P('  %-8s %2d  %4d   %8s  %8.4f   %8.6f   %5.1f%%'
          % (pw, N, n, ('%.6f' % raw) if raw is not None else '   —   ', w, sh, 100 * (1 - w)))
P('')

# ---- THE WIRED SCHEDULE ----------------------------------------------------------------------------
# The ND law's ruled SHAPE decisions transfer, because they are decisions about the ESTIMATOR and the
# owner ruled them for this construction: log-linear between integer depths, 1.0 at/below depth 1, and
# FLAT from the deepest cell that clears the n floor.  Nothing is extrapolated.
# THE WIRING RULE, DECLARED AS A RULE AND APPLIED MECHANICALLY (not chosen after the reading):
#   wire the deepest cell that (i) clears the n floor AND (ii) IS A FADE, i.e. D <= D(1) = 1.0, then HOLD
#   FLAT from there.  (ii) is not a smoothing: a fade that AMPLIFIES contradicts the premise of the law
#   the owner ruled ("sitting is evidence", D(1)=1 is the no-discount anchor).  The owner's own Step-2
#   amendment retired extrapolating a fitted decay THROUGH a selection kink; the pool's depth-3 cell is
#   that kink in its extreme form -- n 17, ALL 17 eventual players, 45% of the value in the unobserved
#   tail -- and it inverts.  Every rejected cell is PUBLISHED IN FULL above with its n and dispersion.
N_FLOOR = 8
_ok = [N for N in DEPTHS if POOL_SURF[N].get('n', 0) >= N_FLOOR and POOL_D.get(N) is not None
       and POOL_D[N] <= 1.0]
DEEPEST = max(_ok or [1])
REJECTED = {N: {'n': POOL_SURF[N].get('n', 0), 'D': POOL_D.get(N),
                'tail_share': POOL_SURF[N].get('tail_share'), 'n_ever': POOL_SURF[N].get('n_ever'),
                'why': ('n %d below the floor %d' % (POOL_SURF[N].get('n', 0), N_FLOOR))
                       if POOL_SURF[N].get('n', 0) < N_FLOOR else 'D > 1.0 -- the cell INVERTS (selection)'}
            for N in DEPTHS if N > DEEPEST and POOL_D.get(N) is not None}
WIRED = {1: 1.0}
for N in DEPTHS:
    if N == 1: continue
    if POOL_D.get(N) is None: continue
    WIRED[N] = POOL_D[N] if N <= DEEPEST else None
WIRED = {k: v for k, v in WIRED.items() if v is not None}
P('THE WIRED POOL SCHEDULE  (n floor %d; a cell must BE A FADE (D<=1); FLAT from depth %d out)' % (N_FLOOR, DEEPEST))
for N in sorted(REJECTED):
    r = REJECTED[N]
    P('  REJECTED D_pool(%d) = %s   n %d   n_ever %s   tail_share %s   -- %s'
      % (N, ('%.6f' % r['D']) if r['D'] is not None else '—', r['n'], r['n_ever'],
         ('%.4f' % r['tail_share']) if r['tail_share'] is not None else '—', r['why']))
for N in sorted(WIRED):
    P('  D_pool(%d) = %.16f     n = %d' % (N, WIRED[N], POOL_SURF[N].get('n', 0)))
P('  D_pool(c >= %d) = %.16f  FLAT' % (DEEPEST, WIRED[DEEPEST]))
P('')
P('AGAINST THE ND LAW: ND 2:%.4f 3:%.4f 4+:%.4f   POOL %s'
  % (RULED[2], RULED[3], RULED[4], ' '.join('%d:%.4f' % (N, WIRED[N]) for N in sorted(WIRED))))
P('')

# ---- named rows, at their TRUE clocks ---------------------------------------------------------------
NAMED = ['luke-beecken', 'liam-reidy', 'cooper-trembath', 'chris-scerri', 'nick-madden',
         'kalani-white', 'jai-newcombe', 'marcus-herbert', 'jaxon-artemis', 'nicholas-martin']
P('NAMED POOL ROWS — pathway, entry year, signed v0 cell, leading sit')
for k in NAMED:
    e = next((x for x in ENTRIES if x['key'] == k), None)
    v = pool_v0(k)
    if e is None:
        P('  %-20s  not in the DV entry list' % k); continue
    P('  %-20s %-5s entry %s  v0_pool %s  leading_sit %d  retired %s'
      % (k, e['type'], e['entry_year'], ('%.1f' % v) if v else 'UNSIGNED/absent',
         leading_sit(e), e['retired']))
P('')

LIMITS = [
 'The pool population is SMALL and its depth cells are thinner than the ND law\'s at every depth; n is '
 'printed on every cell and no cell below the n floor is wired.',
 'Pathways are POOLED into one pool row for the wired schedule. The per-pathway cells are published '
 'K-shrunk so the borrowing is visible, but the WIRED object is the pooled row -- a per-pathway law '
 'would be fitted on cells that mostly do not clear the floor.',
 'The DV grace-A scores were built on store d9a24282 and this branch carries a different store; Layer 1 '
 'is byte-identical, so the population and every sit fact are unaffected. Inherited disclosure from 30A-2.',
 'MSD depth runs one season ahead (owner ruling 5) via debut_year_338\'s MSD clause, inherited from the '
 'transplanted prefix rather than restated here.',
 'beta_pool is NOT separately fitted in this step. The pooled ND beta curve is carried on pool rows and '
 'THE BORROWING IS DISCLOSED ON THE PACKET rather than hidden here. It is the largest open item this step '
 'leaves.',
 'THE DEPTH-3 POOL CELL INVERTS (D = 2.26 on n = 17, every one of the 17 an eventual player, 45% of the '
 'value in the unobserved tail). It is PUBLISHED and NOT WIRED, by the declared rule above. Wiring it '
 'would price a three-season pool sitter at 2.26x his entry value, which contradicts the premise of the '
 'law the owner ruled. This is the seat\'s reading of the owner\'s flat-deep-end amendment applied to a '
 'cell that inverts, and it is flagged on the packet as an OWED CONFIRMATION, not presented as ruled.',
]
P('LIMITATIONS, STATED')
for i, l in enumerate(LIMITS, 1):
    P('  %d. %s' % (i, l))

json.dump({'order': 'ORDER 31 STEP 2 — the pool fade',
           'harness_prefix': {'path': os.path.relpath(SRC, ROOT), 'md5': HARNESS_MD5},
           'control_nd': {'D': {str(N): ND_D.get(N) for N in DEPTHS}, 'ruled': {str(k): v for k, v in RULED.items()},
                          'max_dev': max((v for v in CTRL_DEV.values() if v is not None), default=None),
                          'reproduced': CTRL_OK},
           'population': {'total': len(POP), 'fitted': len(FIT), 'sens2022plus': len(SENS), 'pre2004': len(PRE),
                          'by_pathway_fitted': dict(collections.Counter(r['pathway'] for r in FIT)),
                          'skipped': dict(SKIP)},
           'pool_surface': {str(N): POOL_SURF[N] and {k: v for k, v in POOL_SURF[N].items() if k != 'res'} for N in DEPTHS},
           'pool_D': {str(N): POOL_D.get(N) for N in DEPTHS},
           'by_pathway': BY_PATH, 'K_SHRINK': K_SHRINK, 'n_floor': N_FLOOR,
           'wired': {str(k): v for k, v in WIRED.items()}, 'flat_from': DEEPEST,
           'rejected_cells': {str(k): v for k, v in REJECTED.items()},
           'wiring_rule': 'deepest cell clearing n>=%d AND D<=1.0 (a fade cannot amplify); FLAT from there' % N_FLOOR,
           'limitations': LIMITS},
          open(os.path.join(HERE, 'POOL31.json'), 'w'), indent=1, sort_keys=True, default=str)
open(os.path.join(HERE, 'POOL31_out.txt'), 'w').write('\n'.join(OUT) + '\n')
print('\nPOOL31.json written.')
