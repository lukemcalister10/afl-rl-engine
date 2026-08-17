#!/usr/bin/env python3
"""ORDER 33 W1 -- COUNTERFACTUAL PIPELINE, steps 2-4 (PREREG_W1.md s5). Run AFTER w1_emit_cf.sh.

  STEP 2  CONTROLS on the counterfactual matrix vs per_entrant_O31FFINAL.json (all must PASS):
            day-0 v0 identical on all records; pool rows identical everywhere; vpath identical on
            every record whose whole career is <= 25.5 games (the proposed curve equals the wired
            curve on g <= 25.5 by construction).
  STEP 3  the S4 scorer (`s4_shootout.py`, prereg-bound) exec'd WHOLE with two declared
            substitutions: CAND_P -> the counterfactual matrix; RESULTS output -> this directory.
  STEP 4  recovery table: RESULTS_W1CF.json against the committed RESULTS_S4.json.

READ-ONLY outside this directory.
"""
import os, json, math, hashlib, io, contextlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(EV))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
S4DIR = os.path.join(EV, 'order32_s4_2026-08-17')

OUT = []
def P(s=''):
    OUT.append(str(s)); print(s, flush=True)

def md5f(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()

# ==================================================================================================
# STEP 2 -- CONTROLS
# ==================================================================================================
CF_P = SP + '/per_entrant_W1CF.json'
BASE_P = SP + '/per_entrant_O31FFINAL.json'
CF = json.load(open(CF_P)); BASE = json.load(open(BASE_P))
P('ORDER 33 W1 -- counterfactual controls')
P('  W1CF matrix   %s md5 %s' % (os.path.basename(CF_P), md5f(CF_P)[:8]))
P('  base matrix   %s md5 %s (must be d97f1aee, the S4 candidate input)' % (os.path.basename(BASE_P), md5f(BASE_P)[:8]))
cfr = {r['key']: r for r in CF['recs']}; bar = {r['key']: r for r in BASE['recs']}
assert set(cfr) == set(bar) and len(CF['recs']) == len(BASE['recs']) == 2648, 'record sets differ'
fails = []
n_v0 = sum(1 for k in cfr if cfr[k]['v0'] != bar[k]['v0'])
if n_v0: fails.append('v0 differs on %d records' % n_v0)
pool_diff = [k for k in cfr if bar[k]['is_pool'] and (cfr[k]['vpath'] != bar[k]['vpath'] or cfr[k]['cur'] != bar[k]['cur'])]
if pool_diff: fails.append('pool rows moved: %d e.g. %s' % (len(pool_diff), pool_diff[:5]))
shallow_diff = [k for k in cfr if (bar[k].get('games_total') or 0) <= 25 and cfr[k]['vpath'] != bar[k]['vpath']]
if shallow_diff: fails.append('g<=25 careers moved: %d e.g. %s' % (len(shallow_diff), shallow_diff[:5]))
n_shallow = sum(1 for k in cfr if (bar[k].get('games_total') or 0) <= 25 and not bar[k]['is_pool'])
# structural identity
n_struct = sum(1 for k in cfr if cfr[k]['yrs'] != bar[k]['yrs'] or cfr[k]['seasons'] != bar[k]['seasons'])
if n_struct: fails.append('yrs/seasons differ on %d records' % n_struct)
# describe the movement that DID happen
moved, dmax, dsum, nvals = 0, 0.0, 0.0, 0
for k in cfr:
    if bar[k]['is_pool']: continue
    for a, b in zip(cfr[k]['vpath'], bar[k]['vpath']):
        if a is None or b is None: continue
        nvals += 1
        if a != b:
            moved += 1; d = a - b; dsum += d; dmax = max(dmax, abs(d))
P('  CONTROL day-0 v0 identical .......... %s' % ('PASS (2648/2648)' if not n_v0 else 'FAIL'))
P('  CONTROL pool rows identical ......... %s (1201 pool rows)' % ('PASS' if not pool_diff else 'FAIL'))
P('  CONTROL g<=25 careers identical ..... %s (%d such ND rows)' % ('PASS' if not shallow_diff else 'FAIL', n_shallow))
P('  CONTROL yrs/seasons identical ....... %s' % ('PASS' if not n_struct else 'FAIL'))
P('  movement (non-pool vpath entries): %d of %d changed, mean delta %+.1f, max |delta| %.1f'
  % (moved, nvals, (dsum / moved if moved else 0.0), dmax))
if fails:
    raise SystemExit('ORDER 33 W1 STOP: counterfactual controls failed -- %s' % fails)

# ==================================================================================================
# STEP 3 -- the S4 scorer, run whole, two declared substitutions
# ==================================================================================================
SRC = os.path.join(S4DIR, 's4_shootout.py')
_txt = open(SRC).read()
S4_MD5 = hashlib.md5(_txt.encode()).hexdigest()
SUBS = [
    ("CAND_P = SP + '/per_entrant_O31FFINAL.json'",
     "CAND_P = SP + '/per_entrant_W1CF.json'"),
    ("with open(os.path.join(HERE, 'RESULTS_S4.json'), 'w') as f:",
     "with open(%r, 'w') as f:" % os.path.join(HERE, 'RESULTS_W1CF.json')),
]
_run = _txt
for a, b in SUBS:
    assert _run.count(a) == 1, 'substitution target not unique: %r' % a[:60]
    _run = _run.replace(a, b)
P('')
P('S4 scorer exec (prereg-bound rules carried whole): committed md5 %s as-run md5 %s'
  % (S4_MD5, hashlib.md5(_run.encode()).hexdigest()))
for a, b in SUBS:
    P('    SUB  %-60s ->  %s' % (a[:60], b[:80]))
_buf = io.StringIO()
with contextlib.redirect_stdout(_buf):
    exec(compile(_run, SRC, 'exec'), {'__name__': '__main__', '__file__': SRC})
open(os.path.join(HERE, 'SCORE_W1CF_console.txt'), 'w').write(_buf.getvalue())
P('  scorer ran clean; console SCORE_W1CF_console.txt')

# ==================================================================================================
# STEP 4 -- recovery vs the committed S4 result
# ==================================================================================================
NEW = json.load(open(os.path.join(HERE, 'RESULTS_W1CF.json')))
OLD = json.load(open(os.path.join(S4DIR, 'RESULTS_S4.json')))
def key_of(c):
    return (c['pop'], c['N'], c['horizon'])
newc = {key_of(c): c for c in NEW['cells']}
oldc = {key_of(c): c for c in OLD['cells']}
assert set(newc) == set(oldc)

# control: the old-law column must be unchanged cell by cell (same OLD matrix, same seed)
bad_old = [k for k in newc if newc[k].get('M1') and oldc[k].get('M1')
           and newc[k]['M1']['rho_old'] != oldc[k]['M1']['rho_old']]
P('')
P('  CONTROL rho_old unchanged in every scored cell ... %s' % ('PASS' if not bad_old else 'FAIL %s' % bad_old[:4]))
pool_cells_moved = [k for k in newc if k[0].startswith(('POOL', 'RD', 'MSD', 'OTHERPOOL'))
                    and newc[k].get('M1') and newc[k]['M1']['rho_cand'] != oldc[k]['M1']['rho_cand']]
P('  CONTROL pool-cell candidate skill unchanged ...... %s' % ('PASS' if not pool_cells_moved else 'FAIL %s' % pool_cells_moved[:4]))

P('')
P('=== PRIMARY ND CELLS: the wired candidate vs the W1 counterfactual vs the old law (M1 Spearman) ===')
P('  %-3s %-6s %5s %8s %8s %8s %22s %10s %22s %10s %9s' %
  ('N', 'hz', 'n', 'rho_old', 'rho_cand', 'rho_W1', 'S4 delta [90% CI]', 'S4 verd', 'W1 delta [90% CI]', 'W1 verd', 'recovery'))
REC = []
for N in range(1, 7):
    for hz in ('dv1', 'dvrest'):
        k = ('ND', N, hz)
        o, n = oldc[k], newc[k]
        m0, m1 = o['M1'], n['M1']
        gap = m0['rho_old'] - m0['rho_cand']
        rec = (m1['rho_cand'] - m0['rho_cand']) / gap if abs(gap) > 1e-12 else float('nan')
        REC.append(dict(N=N, hz=hz, n=o['n'], rho_old=m0['rho_old'], rho_cand=m0['rho_cand'],
                        rho_w1=m1['rho_cand'], s4_delta=m0['delta'], s4_ci=m0['delta_ci'],
                        s4_verdict=m0['verdict'], w1_delta=m1['delta'], w1_ci=m1['delta_ci'],
                        w1_verdict=m1['verdict'], recovery=rec,
                        m2_s4=o.get('M2', {}).get('verdict'), m2_w1=n.get('M2', {}).get('verdict')))
        P('  %-3d %-6s %5d %8.3f %8.3f %8.3f %8.3f [%6.3f,%6.3f] %10s %8.3f [%6.3f,%6.3f] %10s %8s' %
          (N, hz, o['n'], m0['rho_old'], m0['rho_cand'], m1['rho_cand'],
           m0['delta'], m0['delta_ci'][0], m0['delta_ci'][1], m0['verdict'],
           m1['delta'], m1['delta_ci'][0], m1['delta_ci'][1], m1['verdict'],
           ('%+.0f%%' % (100 * rec)) if rec == rec else 'n/a'))

old_won = [r for r in REC if r['s4_verdict'] == 'oldlaw']
early_won = [r for r in REC if r['N'] <= 3 and r['s4_verdict'] == 'candidate']
recs_ = sorted(r['recovery'] for r in old_won)
med_rec = recs_[len(recs_) // 2] if len(recs_) % 2 else 0.5 * (recs_[len(recs_) // 2 - 1] + recs_[len(recs_) // 2])
P('')
P('  P3 READING: %d S4 old-law-won primary M1 cells; median recovery %+.0f%%; per-cell %s'
  % (len(old_won), 100 * med_rec, ['N%d %s %+.0f%%' % (r['N'], r['hz'], 100 * r['recovery']) for r in old_won]))
lost_early = [r for r in early_won if r['w1_verdict'] != 'candidate']
flipped = [r for r in old_won if r['w1_verdict'] != 'oldlaw']
P('  years 1-3 candidate wins retained: %d of %d %s' %
  (len(early_won) - len(lost_early), len(early_won),
   ('-- LOST: %s' % [(r['N'], r['hz']) for r in lost_early]) if lost_early else '(all)'))
P('  old-law cells no longer old-law wins: %d of %d -> %s'
  % (len(flipped), len(old_won), [(r['N'], r['hz'], r['w1_verdict']) for r in flipped]))

# verdict tallies over every scored cell family
def tally(cells, fam):
    t = collections.Counter()
    for k, c in cells.items():
        if c['status'] != 'scored' or not fam(k): continue
        for m in ('M1', 'M2'):
            v = c.get(m, {}).get('verdict')
            if v: t[v] += 1
    return dict(t)
P('')
P('  all-scored-cell verdict tally  S4: %s   W1CF: %s'
  % (tally(oldc, lambda k: True), tally(newc, lambda k: True)))
P('  ND-primary tally               S4: %s   W1CF: %s'
  % (tally(oldc, lambda k: k[0] == 'ND' and k[1] >= 1), tally(newc, lambda k: k[0] == 'ND' and k[1] >= 1)))

json.dump(dict(order='ORDER 33 W1 counterfactual scoring', prereg='PREREG_W1.md s5',
               cf_matrix_md5=md5f(CF_P), base_matrix_md5=md5f(BASE_P),
               s4_scorer_md5=S4_MD5,
               controls=dict(v0_identical=n_v0 == 0, pool_identical=not pool_diff,
                             shallow_identical=not shallow_diff, structure_identical=n_struct == 0,
                             rho_old_unchanged=not bad_old, pool_cells_unchanged=not pool_cells_moved,
                             vpath_entries_changed=moved, vpath_entries_total=nvals,
                             mean_delta=(dsum / moved if moved else 0.0), max_abs_delta=dmax),
               primary_cells=REC, median_recovery_oldlaw_cells=med_rec,
               early_wins_lost=[(r['N'], r['hz']) for r in lost_early],
               oldlaw_cells_flipped=[(r['N'], r['hz'], r['w1_verdict']) for r in flipped],
               tally_all=dict(S4=tally(oldc, lambda k: True), W1CF=tally(newc, lambda k: True))),
          open(os.path.join(HERE, 'RECOVERY_W1.json'), 'w'), indent=1, sort_keys=True, default=float)
open(os.path.join(HERE, 'RECOVERY_W1_out.txt'), 'w').write('\n'.join(OUT) + '\n')
print('\nwritten: RESULTS_W1CF.json / RECOVERY_W1.json / RECOVERY_W1_out.txt')
