#!/usr/bin/env python3
"""ORDER 32 S5 STEP 1 -- reconstruct the v0 fit's own inputs, from its own data path. READ-ONLY.

1. Verify lineage: artifact nd_v0.posv == HEADFIX_31F.posv_headfixed (already asserted pre-prereg).
2. Recompute the shrunk PAVA input surface from HEADFIX_31F's persisted posv_raw + credibility_w
   and the artifact's share/curve (the exact o31f_headfix.py arithmetic, lines 96-104).
3. Re-run the COMMITTED o30b_v0refit.py PAVA->floor->tiebreak->lambda block, lifted by source text
   exactly as o31f_headfix.py lifts it, and assert it reproduces posv_headfixed EXACTLY.
4. Build the raw delivered-value table from the fit population itself (LAYER2.fit_nd_keys, value =
   grace_a.total, pick = attribution.pick, pos = layer1 position_group, era = entry_year):
   per pick x position mean / SD / n, persisted whole.
Writes S5_INPUTS.json + s5_step1_out.txt.  Nothing outside docs/evidence/order32_s5_2026-08-17/.
"""
import json, os, hashlib, math, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
EV = os.path.join(ROOT, 'docs', 'evidence')
_OUT = []
def P(s=''):
    print(s); _OUT.append(s)
md5f = lambda p: hashlib.md5(open(p, 'rb').read()).hexdigest()

ART = os.path.join(ROOT, 'engine/rl_after/pvc_curve_v2.json')
HFX = os.path.join(EV, 'candidate_31f/HEADFIX_31F.json')
REFIT_SRC = os.path.join(EV, 'one_machinery_2026-08-14/o30b_v0refit.py')
L2P = os.path.join(EV, 'grace_adoption_2026-08-13/inputs/LAYER2.json')
L1P = os.path.join(EV, 'grace_adoption_2026-08-13/inputs/layer1_player_seasons.json')

P('ORDER 32 S5 STEP 1 -- THE FIT INPUTS, RECONSTRUCTED FROM THE FIT\'S OWN DATA PATH')
for p in (ART, HFX, REFIT_SRC, L2P, L1P):
    P('  %-70s md5 %s' % (os.path.relpath(p, ROOT), md5f(p)))

J = json.load(open(ART))
H = json.load(open(HFX))
POS = list(J['nd_v0']['positions'])
PICKS = list(range(1, 65))
share = {g: {int(k): float(v) for k, v in J['nd_v0']['share'][g].items()} for g in POS}
curve = {int(k): float(v) for k, v in J['curve'].items()}
CURVE_TOT = sum(curve[p] for p in PICKS)
FLOOR = 100.0
fin_pub = {g: {int(k): float(v) for k, v in J['nd_v0']['posv'][g].items()} for g in POS}
posv_raw = {g: {int(k): float(v) for k, v in H['posv_raw'][g].items()} for g in POS}
w = {g: {int(k): float(v) for k, v in H['credibility_w'][g].items()} for g in POS}
effn = {g: {int(k): float(v) for k, v in H['effective_n'][g].items()} for g in POS}

# lineage
mism = max(abs(fin_pub[g][p] - H['posv_headfixed'][g][str(p)]) for g in POS for p in PICKS)
P('  lineage: artifact nd_v0.posv == HEADFIX_31F.posv_headfixed  max|diff| %.3e  %s'
  % (mism, 'HELD' if mism < 1e-9 else 'BROKEN'))
assert mism < 1e-9

# ---- 2. the shrunk PAVA input (o31f_headfix.py lines 96-104, verbatim arithmetic) -----------------
relat = {g: {p: posv_raw[g][p] / curve[p] for p in PICKS} for g in POS}
rel1 = {g: {p: w[g][p] * relat[g][p] + (1.0 - w[g][p]) * 1.0 for p in PICKS} for g in POS}
nrm = {p: sum(share[g][p] * rel1[g][p] for g in POS) for p in PICKS}
rel2 = {g: {p: rel1[g][p] / nrm[p] for p in PICKS} for g in POS}
posv = {g: {p: rel2[g][p] * curve[p] for p in PICKS} for g in POS}   # THE PAVA INPUT
recon = max(abs(sum(share[g][p] * rel2[g][p] for g in POS) - 1.0) for p in PICKS)
P('  shrunk PAVA input recomputed; reconciliation identity max|.-1| %.3e' % recon)
assert recon < 1e-12

# ---- 3. the lifted pipeline, re-run, must reproduce the shipped surface EXACTLY -------------------
_src = open(REFIT_SRC).read()
_blk = _src.split("# ---- 1. weighted PAVA, non-increasing ")[1]
_blk = '# ---- 1. weighted PAVA, non-increasing ' + _blk.split('# ---- OUTPUT ')[0]
P('  pipeline lift md5 %s (must equal HEADFIX_31F pipeline_text_md5 %s): %s'
  % (hashlib.md5(_blk.encode()).hexdigest(), H['pipeline_text_md5'],
     'MATCH' if hashlib.md5(_blk.encode()).hexdigest() == H['pipeline_text_md5'] else 'MISMATCH'))

def ascents_of(tab):
    return [p for p in PICKS[1:] if tab[p] > tab[p - 1] + 1e-12]
_sink = []
NS = dict(PICKS=PICKS, POS=POS, posv=posv, share=share, curve=curve, CURVE_TOT=CURVE_TOT,
          FLOOR=FLOOR, P=lambda s='': _sink.append(s), ascents_of=ascents_of,
          asc_in={g: ascents_of(posv[g]) for g in POS}, json=json, collections=collections)
exec(_blk, NS)
fin = NS['fin']; LAM = NS['LAM']; blocks_of = NS['blocks_of']
rep = max(abs(fin[g][p] - fin_pub[g][p]) for g in POS for p in PICKS)
P('  re-run reproduces the shipped surface: max|fin - artifact posv| %.3e  %s   lambda %.12f (pub %.12f)'
  % (rep, 'EXACT' if rep < 1e-9 else '*** FAIL ***', LAM, H['lam']))
assert rep < 1e-9 and abs(LAM - H['lam']) < 1e-12

# PAVA pooled blocks touching the 21-40 region -- where the constraint binds
P('')
P('  PAVA POOLED BLOCKS (len>1) PER POSITION -- the picks where monotonicity actually binds')
for g in POS:
    bl = [b for b in blocks_of[g] if len(b) > 1]
    P('    %-5s %s' % (g, '  '.join('%d-%d' % (b[0], b[-1]) for b in bl) or '(none)'))

# ---- 4. the raw delivered-value table --------------------------------------------------------------
L2 = json.load(open(L2P)); L1 = json.load(open(L1P))
E = {e['key']: e for e in L1['entries']}
ATTR = L2['attribution']; GA = L2['grace_a']
rows = []
excl = []
for k in L2['fit_nd_keys']:
    e = E.get(k)
    if e is None or ATTR[k]['pick'] is None or GA[k]['total'] is None or e.get('position_group') is None:
        excl.append(k); continue
    rows.append(dict(key=k, pick=int(ATTR[k]['pick']), value=float(GA[k]['total']),
                     pos=e['position_group'], entry_year=int(e['entry_year'])))
P('')
P('  fit population %d rows; EXCLUSIONS: %d %s' % (len(rows), len(excl), excl if excl else '(none)'))
yrs = collections.Counter(r['entry_year'] for r in rows)
P('  entry years: %s' % ' '.join('%d:%d' % kv for kv in sorted(yrs.items())))

cell = collections.defaultdict(list)
for r in rows:
    cell[(r['pos'], r['pick'])].append(r['value'])
def mstats(vs):
    n = len(vs)
    if n == 0: return dict(n=0, mean=None, sd=None)
    m = sum(vs) / n
    sd = math.sqrt(sum((v - m) ** 2 for v in vs) / (n - 1)) if n > 1 else 0.0
    return dict(n=n, mean=m, sd=sd)
tab = {g: {p: mstats(cell.get((g, p), [])) for p in PICKS} for g in POS}

P('')
P('  RAW DELIVERED-VALUE MEANS (fit population, #338 min-tenure basis) -- pick x position, n in ()')
P('  %4s' % 'pick' + ''.join('%22s' % g for g in POS) + '%12s' % 'ALL')
for p in PICKS:
    allv = [v for g in POS for v in cell.get((g, p), [])]
    a = mstats(allv)
    line = '  %4d' % p
    for g in POS:
        s = tab[g][p]
        line += '%22s' % ('-' if s['n'] == 0 else '%.0f+-%.0f(%d)' % (s['mean'], s['sd'], s['n']))
    line += '%12s' % ('%.0f(%d)' % (a['mean'], a['n']))
    P(line)

OUT = dict(
    order='ORDER 32 S5 STEP 1 -- fit inputs reconstructed',
    md5=dict(artifact=md5f(ART), headfix=md5f(HFX), refit_src=md5f(REFIT_SRC), layer2=md5f(L2P), layer1=md5f(L1P)),
    lineage=dict(artifact_eq_headfix_maxdiff=mism, rerun_reproduces_maxdiff=rep, LAM=LAM,
                 pipeline_md5_match=True, shrink_recon_max=recon),
    posv_pava_input={g: {str(p): posv[g][p] for p in PICKS} for g in POS},
    posv_raw_loclin={g: {str(p): posv_raw[g][p] for p in PICKS} for g in POS},
    posv_fitted={g: {str(p): fin[g][p] for p in PICKS} for g in POS},
    pava_blocks={g: [[b[0], b[-1]] for b in blocks_of[g] if len(b) > 1] for g in POS},
    effective_n={g: {str(p): effn[g][p] for p in PICKS} for g in POS},
    raw_cell_stats={g: {str(p): tab[g][p] for p in PICKS} for g in POS},
    rows=rows, exclusions=excl,
)
json.dump(OUT, open(os.path.join(HERE, 'S5_INPUTS.json'), 'w'), indent=1, sort_keys=True)
open(os.path.join(HERE, 's5_step1_out.txt'), 'w').write('\n'.join(_OUT) + '\n')
P('')
P('S5_INPUTS.json written.')
