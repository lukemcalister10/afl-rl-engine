"""ITEM 271 STAGE B — NON-VACUITY of the both-directions exclusion check.

A check that passes proves nothing until it is shown able to fail. This harness lifts each exclusion
in turn and requires the corresponding check to FAIL BY NAME. Eight crossings: two directions x two
channels x two fit families.

THE SECOND CHANNEL IS THE POINT. The priors blend w*posfit + (1-w)*pool with w <= 0.6, so at least
40% of every prior is the POOLED term. Compute that term over the combined population and the other
population is inside every prior, while EVERY SAMPLED ROW STAYS CLEAN and a sampled-rows check reads
green. #225 stage 2 found 818 pool rows teaching the ND prior through exactly this channel. This
harness re-establishes that the check can still see it.

Run after derive_271.py. Writes nothing but its own report.
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import derive_271 as D

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = BASE + '/out'
M = json.load(open(OUT + '/per_entrant_271.json'))
recs = M['recs']

ND   = D.nd_population(recs)
POOL = D.pool_population(recs)
PR_ND = [r for r in recs if D.is_nd_curve_row(r) and r['pick'] and D.PRIOR_LO <= r['year'] <= D.PRIOR_HI]
PR_PO = [r for r in recs if D.is_pool_row(r) and D.PRIOR_LO <= r['year'] <= D.PRIOR_HI]
GRID = list(range(1, 71))

results = []

def attempt(name, setup, site, kind, expect_pool_free):
    """Run one crossing and require the check to FAIL."""
    D._FIT_OBS.clear()
    setup()
    rows = D._FIT_OBS.get(site, {}).get(kind)
    if rows is None:
        results.append(dict(crossing=name, site=site, kind=kind, ran=False,
                            detected=False, note='site/kind not observed'))
        return
    bad = [r for r in rows if (D.is_pool_row(r) if expect_pool_free else D.is_nd_curve_row(r))]
    results.append(dict(crossing=name, site=site, kind=kind, ran=True,
                        n_rows=len(rows), violations=len(bad), detected=bool(bad),
                        examples=[r['player'] for r in bad[:4]]))

# ---- direction 1: a pool row reaches the national curve ----------------------------------------
attempt('ND curve fit sampled over ND + POOL',
        lambda: D.observe('nd_curve', 'sample', ND + POOL), 'nd_curve', 'sample', True)
attempt('ND curve pooled term computed over ND + POOL',
        lambda: D.observe('nd_curve', 'pooling', ND + POOL), 'nd_curve', 'pooling', True)
attempt('ND priors sampled over ND + POOL',
        lambda: D.fit_priors(PR_ND + PR_PO, 'ND_1_64', GRID), 'priors_ND_1_64', 'sample', True)
attempt('ND priors POOLED TERM over ND + POOL, sample left clean',
        lambda: D.fit_priors(PR_ND, 'ND_1_64', GRID, pooling_rows=PR_ND + PR_PO),
        'priors_ND_1_64', 'pooling', True)

# ---- direction 2: a national 1-64 row reaches the pool level ------------------------------------
attempt('pool level sampled over POOL + ND',
        lambda: D.observe('pool_level', 'sample', POOL + ND), 'pool_level', 'sample', False)
attempt('pool level pooled term computed over POOL + ND',
        lambda: D.observe('pool_level', 'pooling', POOL + ND), 'pool_level', 'pooling', False)
attempt('pool priors sampled over POOL + ND',
        lambda: D.fit_priors(PR_PO + PR_ND, 'POOL', GRID), 'priors_POOL', 'sample', False)
attempt('pool priors POOLED TERM over POOL + ND, sample left clean',
        lambda: D.fit_priors(PR_PO, 'POOL', GRID, pooling_rows=PR_PO + PR_ND),
        'priors_POOL', 'pooling', False)

# ---- THE VACUITY DEMONSTRATION: the pooled-term crossing with the sample checked instead --------
# Cross ONLY the pooled term, then run the SAMPLED-ROWS check. It reads green while 40%+ of every
# prior is contaminated -- which is why the sample check alone is not a proof.
D._FIT_OBS.clear()
D.fit_priors(PR_ND, 'ND_1_64', GRID, pooling_rows=PR_ND + PR_PO)
_s = D._FIT_OBS['priors_ND_1_64']['sample']
_p = D._FIT_OBS['priors_ND_1_64']['pooling']
vac = dict(sampled_rows_violations=len([r for r in _s if D.is_pool_row(r)]),
           pooled_term_violations=len([r for r in _p if D.is_pool_row(r)]),
           blend_floor='1-w >= %.2f of every prior' % (1.0 - D.PRIOR_CEIL))

json.dump(dict(crossings=results, vacuity_demonstration=vac),
          open(OUT + '/nonvacuity_271.json', 'w'), indent=1)

print("NON-VACUITY — each exclusion lifted in turn; the check MUST fail\n")
allgood = True
for r in results:
    ok = r['detected']
    allgood &= ok
    print("  %-8s %-52s site %-16s [%-7s] %s"
          % ('DETECTED' if ok else 'MISSED', r['crossing'], r['site'], r['kind'],
             ('%d violations, e.g. %s' % (r['violations'], r['examples'])) if ok else '<-- CHECK IS VACUOUS'))
print("\nTHE VACUITY DEMONSTRATION (why the sampled-rows check alone is not a proof):")
print("  cross ONLY the pooled term of the ND priors, then look at each channel --")
print("    sampled rows : %d violations  (reads GREEN)" % vac['sampled_rows_violations'])
print("    pooled term  : %d violations  (the contamination)" % vac['pooled_term_violations'])
print("    and %s" % vac['blend_floor'])
print("\nRESULT: %s" % ('all eight crossings detected — the check is non-vacuous in both directions '
                        'and both channels' if allgood else 'AT LEAST ONE CROSSING WENT UNDETECTED'))
sys.exit(0 if allgood else 1)
