"""#279 STEP 2 — the minimal-vs-structural pick-basis prototype pair, VOR-denominated (gamma=1.0).

Both prototypes consume ONE evidence matrix and run through the SAME fit machinery carried verbatim
from #271 (fit_year0 / monotone_strict / pava_ni, tau, nmin, PW_FLOOR, pin(1)=3000, both windows).
The ONLY thing that differs is what each entrant contributes as its year-0 point.

BASELINE (as shipped): every entrant contributes its v0 -- the MODEL's year-0 estimate off the fitted
surface -- at weight 1.0 and ty=0, plus its realised path at ty=k with weight es. fit_year0 then applies
exp(-ty/tau), tau=0.12, so realised evidence is down-weighted by 2.4e-4 at ty=1 and 5.8e-8 at ty=2.

MINIMAL (S-1): for a CONCLUDED career the year-0 slot carries what he ACTUALLY did (the evidence-weighted
realised value, busts at 0.0) instead of what the model predicted. The prior is retired from concluded
careers entirely. Active careers are untouched -- the prior still stands in for their unwritten share.
One point per entrant either way, so the bandwidth/effn basis is unchanged: this is a re-weighting
INSIDE the current blend, nothing structural.

STRUCTURAL (S-2): every entrant contributes a COMPLETED career value. Concluded careers contribute their
realised value (same as MINIMAL). Active careers have their unwritten remainder completed actuarially
from concluded look-alikes -- matched on settled position x tenure-so-far -- with busts' zero-remainders
INCLUDED in the stratum. The model prior survives only as an explicit, COUNTED fallback for thin strata.

alpha stays parked at 1.0 throughout: no variance shaping in either prototype (step 3's question).
"""
import os, sys, io, json, time, hashlib, collections, contextlib
import numpy as np

MATRIX = sys.argv[1]
DERIVE = sys.argv[2]
OUTDIR = sys.argv[3]
WHICH = sys.argv[4] if len(sys.argv) > 4 else 'both'

os.environ.setdefault('CURVE_STATISTIC', 'VOR')
_src = open(DERIVE).read()
_defs = _src.split('def main(')[0]
G = {'__name__': '_proto_basis', '__file__': os.path.abspath(DERIVE)}
exec(_defs, G)

PW_FLOOR = G['PW_FLOOR']; TAU = G['TAU']; PIN1 = G['PIN1']
YR_LO, YR_HI = G['YR_LO'], G['YR_HI']
ND_CURVE_LAST = G['ND_CURVE_LAST']
fit_year0 = G['fit_year0']; monotone_strict = G['monotone_strict']
never_established = G['never_established']; realised = G['realised_scar']

M = json.load(open(MATRIX)); recs = M['recs']; meta = M['meta']

def is_nd(r):
    return bool(r.get('teaches_curve')) and r.get('pick') and 1 <= r['pick'] <= ND_CURVE_LAST
ND = [r for r in recs if is_nd(r) and YR_LO <= r['year'] <= YR_HI]
assert ND, "EMPTY ND curve population"

def concluded(r):
    """Concluded-career marker, from the emitter-derived fields (the store itself carries no
    retired_now/last_game_year -- #279 amendment C1; the emitter synthesises them from _retired /
    _last_listed via the engine's own helper)."""
    return bool(r.get('retired_now'))

def tenure_written(r):
    vp = r.get('vpath') or []
    return sum(1 for v in vp if v is not None)

def realised_at(r, t):
    """Evidence-weighted realised value over the first t written years. Busts -> 0.0."""
    pw = r.get('pw', {}); vp = r.get('vpath') or []
    num = den = 0.0
    for k in range(1, min(t, len(vp)) + 1):
        v = vp[k - 1]
        if v is None: continue
        pwk = pw.get(str(k), pw.get(str(min(k, 6))))
        if pwk is None: pwk = 1.0
        es = max(0.0, 1.0 - (pwk - PW_FLOOR) / (1.0 - PW_FLOOR))
        if es <= 0: continue
        num += es * v; den += es
    return float(num / den) if den > 0 else 0.0

# ---------------- the completion table (STRUCTURAL only) ----------------
MIN_STRATUM = 20
def build_completion(pop):
    """From CONCLUDED careers only: per (settled position x tenure-so-far), the ratio between the full
    realised career and the realised-so-far at that tenure. Busts (never established -> 0.0) are IN."""
    num = collections.defaultdict(list); den = collections.defaultdict(list)
    for r in pop:
        if not concluded(r): continue
        T = tenure_written(r)
        if T <= 0: continue
        full = 0.0 if never_established(r) else realised(r)
        for t in range(1, T + 1):
            sofar = 0.0 if never_established(r) else realised_at(r, t)
            num[(r['pos'], t)].append(full); den[(r['pos'], t)].append(sofar)
    tab = {}
    for k in num:
        a = float(np.mean(num[k])); b = float(np.mean(den[k]))
        tab[k] = {'n': len(num[k]), 'mean_full': a, 'mean_sofar': b,
                  'ratio': (a / b) if b > 0 else None}
    return tab

def completed_value(r, tab, stats):
    """Concluded -> its own realised value. Active -> realised-so-far scaled by the look-alike ratio;
    prior only as a COUNTED fallback when the stratum is thin or degenerate."""
    if concluded(r):
        stats['concluded'] += 1
        return (0.0 if never_established(r) else realised(r)), 'concluded_realised'
    T = tenure_written(r)
    if T <= 0:
        stats['fallback_no_written'] += 1
        return float(r['v0']), 'prior_fallback_no_written'
    key = (r['pos'], T)
    e = tab.get(key)
    if e is None or e['n'] < MIN_STRATUM or e['ratio'] is None:
        stats['fallback_thin_stratum'] += 1
        return float(r['v0']), 'prior_fallback_thin'
    sofar = 0.0 if never_established(r) else realised_at(r, T)
    stats['completed'] += 1
    return sofar * e['ratio'], 'completed'

# ---------------- point builders ----------------
def points_baseline(P):
    lp, ty, val, wt = [], [], [], []
    for r in P:
        L = np.log(r['pick'])
        lp.append(L); ty.append(0); val.append(float(r['v0'])); wt.append(1.0)
        pw = r.get('pw', {}); vp = r.get('vpath') or []
        for k in range(1, len(vp) + 1):
            v = vp[k - 1]
            if v is None: continue
            pwk = pw.get(str(k), pw.get(str(min(k, 6))))
            if pwk is None: pwk = 1.0
            es = max(0.0, 1.0 - (pwk - PW_FLOOR) / (1.0 - PW_FLOOR))
            if es <= 0: continue
            lp.append(L); ty.append(k); val.append(float(v)); wt.append(es)
    return (np.array(lp), np.array(ty, float), np.array(val, float), np.array(wt, float), None)

def points_minimal(P, stats):
    lp, ty, val, wt = [], [], [], []
    for r in P:
        L = np.log(r['pick'])
        if concluded(r):
            stats['concluded_evidence_voted'] += 1
            y0 = 0.0 if never_established(r) else realised(r)
            lp.append(L); ty.append(0); val.append(float(y0)); wt.append(1.0)
            continue                      # prior retired; no decayed evidence points either
        stats['active_prior_retained'] += 1
        lp.append(L); ty.append(0); val.append(float(r['v0'])); wt.append(1.0)
        pw = r.get('pw', {}); vp = r.get('vpath') or []
        for k in range(1, len(vp) + 1):
            v = vp[k - 1]
            if v is None: continue
            pwk = pw.get(str(k), pw.get(str(min(k, 6))))
            if pwk is None: pwk = 1.0
            es = max(0.0, 1.0 - (pwk - PW_FLOOR) / (1.0 - PW_FLOOR))
            if es <= 0: continue
            lp.append(L); ty.append(k); val.append(float(v)); wt.append(es)
    return (np.array(lp), np.array(ty, float), np.array(val, float), np.array(wt, float), None)

def points_structural(P, tab, stats):
    lp, ty, val, wt, prov = [], [], [], [], collections.Counter()
    for r in P:
        v, how = completed_value(r, tab, stats)
        prov[how] += 1
        lp.append(np.log(r['pick'])); ty.append(0); val.append(float(v)); wt.append(1.0)
    return (np.array(lp), np.array(ty, float), np.array(val, float), np.array(wt, float), None), prov

def fit(points):
    grid, raw, effn = fit_year0(points)
    curve = monotone_strict(grid, raw, effn)
    sc = PIN1 / curve[0] if curve[0] else 1.0
    pinned = [max(1, int(round(c * sc))) for c in curve]
    # re-assert strict descent after the pin's rounding, and COUNT how many points the enforcement
    # had to move — a forced point is the pin talking, not the data, and must be disclosed.
    forced = []
    for i in range(1, len(pinned)):
        if pinned[i] >= pinned[i - 1]:
            forced.append(i + 1); pinned[i] = pinned[i - 1] - 1
    diag = {'raw_at': {str(k): round(float(raw[k-1]), 2) for k in (1,2,3,10,24,32,40,50,57,64)},
            'effn_at': {str(k): round(float(effn[k-1]), 1) for k in (1,2,3,10,24,32,40,50,57,64)},
            'monotone_raw_violations_1_64': int(sum(1 for i in range(1,64) if raw[i] >= raw[i-1])),
            'forced_by_descent_enforcement': forced,
            'n_forced': len(forced)}
    return grid, raw, effn, pinned, diag

def payload(ci):
    return hashlib.md5(json.dumps({str(i + 1): v for i, v in enumerate(ci)},
                                  sort_keys=True).encode()).hexdigest()[:8]

out = {'matrix': {'file': os.path.basename(MATRIX), 'store_md5': meta['store_md5'],
                  'v0surf_sig': meta['v0surf_sig'][:12], 'v0surf_frozen': meta.get('v0surf_frozen'),
                  'gamma': '1.0 (VOR, owner-ruled 2026-07-30)'},
       'population': {'nd_curve_rows': len(ND), 'window': [YR_LO, YR_HI],
                      'concluded': sum(1 for r in ND if concluded(r)),
                      'active': sum(1 for r in ND if not concluded(r)),
                      'never_established': sum(1 for r in ND if never_established(r))},
       'alpha': 1.0, 'runs': {}}

t0 = time.time()
_, _, _, base, dbase = fit(points_baseline(ND))
out['runs']['baseline'] = {'seconds': round(time.time() - t0, 2), 'payload': payload(base),
                           'ladder_total': int(sum(base)), 'diagnostics': dbase,
                           'curve': {str(k): base[k - 1] for k in (1, 2, 3, 10, 24, 32, 40, 50, 57, 64)}}

if WHICH in ('minimal', 'both'):
    t0 = time.time(); st = collections.Counter()
    _, _, _, mini, dmini = fit(points_minimal(ND, st))
    out['runs']['minimal'] = {'seconds': round(time.time() - t0, 2), 'payload': payload(mini),
                              'ladder_total': int(sum(mini)), 'counts': dict(st), 'diagnostics': dmini,
                              'curve': {str(k): mini[k - 1] for k in (1, 2, 3, 10, 24, 32, 40, 50, 57, 64)},
                              'vs_baseline_ratio': {str(k): round(mini[k - 1] / base[k - 1], 4)
                                                    for k in (1, 2, 3, 10, 24, 32, 40, 50, 57, 64)}}
if WHICH in ('structural', 'both'):
    t0 = time.time(); st = collections.Counter()
    tab = build_completion(ND)
    pts, prov = points_structural(ND, tab, st)
    _, _, _, stru, dstru = fit(pts)
    out['runs']['structural'] = {'seconds': round(time.time() - t0, 2), 'payload': payload(stru),
        'ladder_total': int(sum(stru)), 'counts': dict(st), 'provenance': dict(prov), 'diagnostics': dstru,
        'strata_total': len(tab), 'strata_usable': sum(1 for v in tab.values()
                                                       if v['n'] >= MIN_STRATUM and v['ratio']),
        'min_stratum': MIN_STRATUM,
        'curve': {str(k): stru[k - 1] for k in (1, 2, 3, 10, 24, 32, 40, 50, 57, 64)},
        'vs_baseline_ratio': {str(k): round(stru[k - 1] / base[k - 1], 4)
                              for k in (1, 2, 3, 10, 24, 32, 40, 50, 57, 64)}}
    if 'minimal' in out['runs']:
        out['divergence_minimal_vs_structural'] = {
            'note': 'S-2: the divergence between the two IS the measurement of the surviving self-reference',
            'by_pick': {str(k): round(stru[k - 1] / mini[k - 1], 4)
                        for k in (1, 2, 3, 10, 24, 32, 40, 50, 57, 64)},
            'ladder_ratio': round(sum(stru) / sum(mini), 4)}

os.makedirs(OUTDIR, exist_ok=True)
json.dump(out, open(os.path.join(OUTDIR, 'proto_basis_279.json'), 'w'), indent=1, sort_keys=True)
open(os.path.join(OUTDIR, 'proto_basis_279.json'), 'a').write("\n")
full = {'baseline': base}
if 'minimal' in out['runs']: full['minimal'] = mini
if 'structural' in out['runs']: full['structural'] = stru
json.dump(full, open(os.path.join(OUTDIR, 'proto_curves_full_279.json'), 'w'), indent=1, sort_keys=True)
open(os.path.join(OUTDIR, 'proto_curves_full_279.json'), 'a').write("\n")
print(json.dumps(out, indent=1, sort_keys=True))
