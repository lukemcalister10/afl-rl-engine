"""ORDER 20 — POPULATION PROBE. For every fit/norm/shrinkage population named in the sweep, print
how many NATIONAL rows and how many POOL rows it contains, using the ENGINE's own `is_pool`.

Run from a tree root:  RL_REPO=<tree> python3 population_probe.py
It execs the engine head exactly as the instruments do (emit_matrix_338.py:73-77), so the numbers are
the engine's, not a re-implementation.
"""
import os, sys, io, contextlib, collections, json

REPO = os.environ.get('RL_REPO', os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))
WORKDIR = os.environ.get('RL_WORKDIR', REPO + '/engine/rl_after')
sys.path.insert(0, os.environ.get('RL_VENDOR', REPO + '/vendor'))
os.chdir(WORKDIR); sys.path.insert(0, '.'); sys.path.insert(0, REPO)

src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
G = {'__name__': '_o20_probe'}
with contextlib.redirect_stdout(io.StringIO()):
    exec(src, G)
MA = G['MA']; PR = G['PR']; cp = G['cp']
import importlib.util as _iu


def _load(name, path):
    s = _iu.spec_from_file_location(name, path); m = _iu.module_from_spec(s)
    with contextlib.redirect_stdout(io.StringIO()): s.loader.exec_module(m)
    return m


P = print
OUT = {}


def report(tag, where, rows, note=''):
    n = sum(1 for p in rows if not MA.is_pool(p)); q = sum(1 for p in rows if MA.is_pool(p))
    OUT[tag] = {'where': where, 'national': n, 'pool': q, 'total': n + q,
                'pool_share_pct': round(100.0 * q / max(1, n + q), 2), 'note': note}
    P("  %-28s %-46s national %5d  pool %5d  (pool %5.2f%%)%s"
      % (tag, where, n, q, 100.0 * q / max(1, n + q), ('  ' + note) if note else ''))


P("=" * 128)
P("ORDER 20 — POPULATION PROBE: which fit populations mix the two arms?   (membership = MA.is_pool, the engine's own)")
P("=" * 128)

report('hist  (#336 / BASEPK)', 'rl_model.py:283', MA.hist,
       'consumed by BPK/_pest_336/POOL/BASEPK_REG :456-502')
report('_curve_sample (build_pvc)', 'rl_model.py:1169,1225,1585',
       [p for p in MA.hist if MA._teaches_curve(p)], 'GATED by _teaches_curve — clean')
report('_cohP (establishment-P)', 'rl_model.py:1639',
       [p for p in MA.data if p.get('_grp') in ('ND', 'RD') and MA.debut(p) <= 2019 and p['pos'] in MA.GRP],
       'consumed by _brateP/_pavaP/_ovP/_grpoffP/pick_prior/P_estab')

# par_build gather() pool  (par_build.py:261-263)
pb = PR.pb if hasattr(PR, 'pb') else _load('pb', REPO + '/engine/forward_valuation/par_build.py')


def _draftyr(p): return cp.debutyr(p) - 1


report('par_build gather() pool', 'par_build.py:261-263',
       [p for p in MA.data if MA.GRP.get(p.get('pos')) and (p.get('pick') or p.get('_ft'))
        and 2003 <= _draftyr(p) <= 2018],
       'levelfn/level_grid/gramp/base + build_pest band marginal')
report('par_redesign BASE_RATE', 'par_redesign.py:75-77',
       [p for p in MA.data if MA.GRP.get(p.get('pos')) and (p.get('pick') or p.get('_ft'))
        and 2003 <= _draftyr(p) <= 2018], 'BASE_RATE[(pos,T)] -> shortfall(p,Y)')
report('distribution_pricing build()', 'distribution_pricing.py:297',
       [p for p in MA.data if MA.GRP.get(p['pos'])],
       'build_training GBR + build_prior +-4 pick window')
report('conditional_prior build', 'conditional_prior.py:146',
       [p for p in MA.data if MA.GRP.get(p['pos'])], 'cond_prior_band GBR quantiles, feature log(pick)')
report('_uncomp_scope (LEG B refs)', '_merged_recover.py:2489-2519',
       [p for p in MA.data if G['_isreal'](p) and not G['delisted'](p) and not p.get('_retired')],
       'V_ref_b / RHO_DEN / C[pos]')
report('rl_model players (backward)', 'rl_model.py:1757-1759',
       [p for p in MA.data if MA.active(p)] if hasattr(MA, 'active') else [],
       'vM1/vM2 conservation factor _f')

# ---- the +-4 pick window at the national/pool boundary: how much of pick 61-64's neighbourhood is pool?
P()
P("  THE +-4 WINDOW AT THE BOUNDARY (the concentration hazard rl_model.py:296-310 names).")
P("  distribution_pricing.build_prior windows on min(effpk,70) with |k-pick|<=4; every pool row sits at 65.")
allp = [p for p in MA.data if MA.GRP.get(p['pos']) and (p.get('_ft') or p.get('pick'))]
for k in (55, 58, 60, 61, 62, 63, 64):
    w = [p for p in allp if abs(min(MA.effpk(p), 70) - k) <= 4]
    n = sum(1 for p in w if not MA.is_pool(p)); q = len(w) - n
    P("    pick %2d window: national %4d  pool %4d  -> pool is %5.1f%% of the window"
      % (k, n, q, 100.0 * q / max(1, len(w))))
    OUT['window_pick_%d' % k] = {'national': n, 'pool': q, 'pool_share_pct': round(100.0 * q / max(1, len(w)), 2)}

# ---- hist band composition (the #336 band tables) ----
P()
P("  #336 BAND TABLE COMPOSITION (rl_model.py:456-502, bands on MA.effpk):")
c = collections.Counter((MA.bandof(MA.effpk(p)), MA.is_pool(p)) for p in MA.hist)
for b in range(MA.NB):
    P("    band %d %-9s national %5d  pool %5d" % (b, '%d-%d' % tuple(MA.BANDS[b]),
                                                   c.get((b, False), 0), c.get((b, True), 0)))
    OUT['hist_band_%d' % b] = {'range': MA.BANDS[b], 'national': c.get((b, False), 0), 'pool': c.get((b, True), 0)}

json.dump(OUT, open(os.environ.get('RL_PROBE_OUT', '/tmp/population_probe.json'), 'w'), indent=1)
P()
P("  json -> %s" % os.environ.get('RL_PROBE_OUT', '/tmp/population_probe.json'))
