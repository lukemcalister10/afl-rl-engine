"""#279 step-3 EVIDENCE ADDENDUM — six alpha schedules, full 64-point ladders.

Owner viewing request before the alpha ruling. Adds two per-pick linear schedules to the four already
filed, on the SAME _ce0 machinery and the SAME fit pipeline as the ruled curve:

    (5) linear  0.8 at pick 1 -> 1.00 at pick 64
    (6) linear  0.9 at pick 1 -> 1.05 at pick 64      <- crosses 1.0, so the tail is UPSIDE-weighted

REPORT-ONLY. alpha stays parked at 1.0. Nothing here implies or anticipates a ruling.

Everything is derived on the ruled basis: STRUCTURAL completion, hard class cut at 2022, VOR (gamma=1.0),
own-surface discipline unchanged. alpha=1.0 must reproduce the ruled curve 4fc40e91 exactly -- that is the
control on this harness.
"""
import os, sys, json, math, time, csv, hashlib, collections
import numpy as np

VOR_MATRIX, DERIVE, OUTDIR = sys.argv[1], sys.argv[2], sys.argv[3]
CLASS_CUT = int(os.environ.get('CLASS_CUT', '2022'))
os.environ.setdefault('CURVE_STATISTIC', 'VOR')

_src = open(DERIVE).read()
G = {'__name__': '_alpha_sched', '__file__': os.path.abspath(DERIVE)}
exec(_src.split('def main(')[0], G)
PW_FLOOR = G['PW_FLOOR']; PIN1 = G['PIN1']; NMIN = G['NMIN']
HMIN, HMAX = G['HMIN'], G['HMAX']; YR_LO = G['YR_LO']; ND_LAST = G['ND_CURVE_LAST']
monotone_strict = G['monotone_strict']; never_established = G['never_established']
realised = G['realised_scar']
MIN_STRATUM = 20

M = json.load(open(VOR_MATRIX)); meta = M['meta']
ND = [r for r in M['recs'] if r.get('teaches_curve') and r.get('pick')
      and 1 <= r['pick'] <= ND_LAST and YR_LO <= r['year'] <= CLASS_CUT]
assert ND, "EMPTY ND population"

def concluded(r): return bool(r.get('retired_now'))
def depth(r): return sum(1 for v in (r.get('vpath') or []) if v is not None)
def realised_at(r, t):
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
def full_realised(r): return 0.0 if never_established(r) else realised(r)
def sofar(r, t): return 0.0 if never_established(r) else realised_at(r, t)

S = collections.defaultdict(lambda: [0.0, 0.0, 0])
for r in ND:
    if not concluded(r): continue
    T = depth(r)
    if T <= 0: continue
    f = full_realised(r)
    for t in range(1, T + 1):
        e = S[(r['pos'], t)]; e[0] += f; e[1] += sofar(r, t); e[2] += 1

stats = collections.Counter(); vals = []
for r in ND:
    if concluded(r):
        stats['concluded_realised'] += 1; vals.append((r['pick'], full_realised(r))); continue
    T = depth(r)
    if T <= 0:
        stats['prior_fallback_no_written'] += 1; vals.append((r['pick'], float(r['v0']))); continue
    key = (r['pos'], T)
    if key not in S:
        stats['prior_fallback_thin'] += 1; vals.append((r['pick'], float(r['v0']))); continue
    sf, ss, n = S[key]
    if n < MIN_STRATUM or ss <= 0:
        stats['prior_fallback_thin'] += 1; vals.append((r['pick'], float(r['v0']))); continue
    stats['completed'] += 1
    vals.append((r['pick'], sofar(r, T) * ((sf / n) / (ss / n))))

nPop = len(ND)
fb = stats['prior_fallback_thin'] + stats['prior_fallback_no_written']
assert stats['concluded_realised'] + stats['completed'] + fb == nPop, "provenance does not sum to population"

def fit_ce(alpha_fn):
    lp = np.array([math.log(k) for k, _ in vals], float)
    v = np.array([max(x, 0.0) for _, x in vals], float)      # _ce0 semantics
    raw, effn = [], []
    for p in range(1, ND_LAST + 1):
        Lp = math.log(p); h = HMIN
        while h < HMAX:
            if np.sum(np.exp(-0.5 * ((lp - Lp) / h) ** 2)) >= NMIN: break
            h += 0.02
        W = np.exp(-0.5 * ((lp - Lp) / h) ** 2)
        al = alpha_fn(p)
        if abs(al - 1.0) < 1e-12:
            r = float(np.sum(W * v) / np.sum(W))
        else:
            r = float((np.sum(W * np.power(v, al)) / np.sum(W)) ** (1.0 / al))
        raw.append(r); effn.append(float(np.sum(np.exp(-0.5 * ((lp - Lp) / h) ** 2))))
    return np.array(raw), np.array(effn)

def pin(raw, effn):
    mono = monotone_strict(list(range(1, ND_LAST + 1)), raw, effn)
    out = list(mono); forced = []
    for i in range(1, len(out)):
        if out[i] >= out[i - 1]: forced.append(i + 1); out[i] = out[i - 1] - 1
    return out, forced

def payload(ci):
    return hashlib.md5(json.dumps({str(i + 1): v for i, v in enumerate(ci)},
                                  sort_keys=True).encode()).hexdigest()[:8]

SCHED = collections.OrderedDict([
 ('a0.6_flat',              (lambda k: 0.6, 'flat 0.6 — most risk-averse of the filed set')),
 ('a0.8_flat',              (lambda k: 0.8, 'flat 0.8')),
 ('a1.0_flat',              (lambda k: 1.0, 'flat 1.0 — the honest mean; the ruled curve')),
 ('tiered_0.6_to_0.8_by50', (lambda k: 0.6 + 0.2 * min(k - 1, 49) / 49.0,
                             "the engine's own _alpha_pvc: 0.6 at pick 1 -> 0.8 by pick 50, flat after")),
 ('lin_0.8_to_1.00_at64',   (lambda k: 0.8 + (1.00 - 0.8) * (k - 1) / 63.0,
                             'NEW: linear 0.8 at pick 1 -> 1.00 at pick 64')),
 ('lin_0.9_to_1.05_at64',   (lambda k: 0.9 + (1.05 - 0.9) * (k - 1) / 63.0,
                             'NEW: linear 0.9 at pick 1 -> 1.05 at pick 64 — crosses 1.0, tail UPSIDE-weighted')),
])

t0 = time.time()
raw1, effn1 = fit_ce(SCHED['a1.0_flat'][0])
honest_mean_total = float(np.sum(raw1))
honest_mean_tail = float(np.sum(raw1[1:]))
ruled_ladder, _ = pin(raw1, effn1)

OUT = {'status': 'REPORT-ONLY evidence addendum. alpha stays PARKED at 1.0; no ruling is implied.',
 'basis': {'gamma': '1.0 VOR', 'basis': 'STRUCTURAL', 'class_cut': CLASS_CUT,
           'store_md5': meta['store_md5'], 'v0surf_sig': meta['v0surf_sig'][:12],
           'v0surf_frozen': meta.get('v0surf_frozen')},
 'population': {'n': nPop, 'concluded': sum(1 for r in ND if concluded(r)),
                'active': sum(1 for r in ND if not concluded(r))},
 'FALLBACK_SHARE': {'rows': fb, 'of': nPop, 'share_pct': round(100.0 * fb / nPop, 3),
                    'asserted': 'provenance sums to population'},
 'ce_form': "CE_alpha = (sum(W*v^alpha)/sum(W))^(1/alpha), busts floored at 0.0 per the engine's own _ce0",
 'conservation_yardstick': {'total_mean_production_picks_1_64': round(honest_mean_total, 1),
                            'mean_production_picks_2_64': round(honest_mean_tail, 1)},
 'schedules': collections.OrderedDict()}

ladders = collections.OrderedDict()
for name, (fn, desc) in SCHED.items():
    raw, effn = fit_ce(fn)
    ci, forced = pin(raw, effn)
    ladders[name] = ci
    OUT['schedules'][name] = {
      'description': desc,
      'alpha_at': {str(k): round(fn(k), 4) for k in (1, 2, 10, 24, 32, 40, 50, 57, 64)},
      'raw_at_pick1': round(float(raw[0]), 1),
      'pinned_pick1': ci[0],
      'pin_lift_on_pick1': round(PIN1 / float(raw[0]), 4),
      'post_pin_ladder_total': int(sum(ci)),
      'ladder_2_to_64': int(sum(ci[1:])),
      'CONSERVATION_ratio_ladder_over_mean_production': round(sum(ci) / honest_mean_total, 4),
      'ladder_2_64_vs_mean_production_2_64_pct': round(100 * (sum(ci[1:]) / honest_mean_tail - 1), 3),
      'PICK_CLASS_PRICE_vs_numeraire': round(sum(ci[1:]) / ci[0], 4),
      'PICK_CLASS_vs_alpha1_pct': None,
      'raw_monotone_violations': int(sum(1 for i in range(1, ND_LAST) if raw[i] >= raw[i - 1])),
      'forced_by_descent_enforcement': len(forced),
      'payload': payload(ci)}
base_class = OUT['schedules']['a1.0_flat']['PICK_CLASS_PRICE_vs_numeraire']
for name in OUT['schedules']:
    s = OUT['schedules'][name]
    s['PICK_CLASS_vs_alpha1_pct'] = round(100 * (s['PICK_CLASS_PRICE_vs_numeraire'] / base_class - 1), 3)
    s['vs_alpha1_ratio_by_pick'] = {str(k): round(ladders[name][k - 1] / ladders['a1.0_flat'][k - 1], 4)
                                    for k in (1, 3, 10, 24, 32, 40, 50, 57, 64)}

OUT['control'] = {'alpha1_payload': OUT['schedules']['a1.0_flat']['payload'],
                  'ruled_curve_payload': '4fc40e91',
                  'alpha1_reproduces_ruled_curve':
                      OUT['schedules']['a1.0_flat']['payload'] == '4fc40e91'}
OUT['nonvacuity'] = {'schedules_are_distinct':
                        len({OUT['schedules'][n]['payload'] for n in OUT['schedules']}) == len(OUT['schedules']),
                     'n_schedules': len(OUT['schedules']),
                     'upside_schedule_exceeds_alpha1_somewhere':
                        any(ladders['lin_0.9_to_1.05_at64'][k] > ladders['a1.0_flat'][k]
                            for k in range(ND_LAST))}
OUT['seconds'] = round(time.time() - t0, 3)

os.makedirs(OUTDIR, exist_ok=True)
json.dump(OUT, open(os.path.join(OUTDIR, 'alpha_schedules_279.json'), 'w'), indent=1)
open(os.path.join(OUTDIR, 'alpha_schedules_279.json'), 'a').write("\n")
json.dump({n: ladders[n] for n in ladders},
          open(os.path.join(OUTDIR, 'alpha_ladders_full_279.json'), 'w'), indent=1)
open(os.path.join(OUTDIR, 'alpha_ladders_full_279.json'), 'a').write("\n")

names = list(SCHED.keys())
with open(os.path.join(OUTDIR, 'alpha_ladders_279.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['pick'] + names + ['alpha_' + n for n in names])
    for k in range(1, ND_LAST + 1):
        w.writerow([k] + [ladders[n][k - 1] for n in names]
                       + [round(SCHED[n][0](k), 4) for n in names])
    w.writerow(['LADDER_TOTAL'] + [int(sum(ladders[n])) for n in names] + [''] * len(names))
    w.writerow(['CONSERVATION'] + [OUT['schedules'][n]['CONSERVATION_ratio_ladder_over_mean_production']
                                   for n in names] + [''] * len(names))
    w.writerow(['PICK_CLASS_vs_NUMERAIRE'] + [OUT['schedules'][n]['PICK_CLASS_PRICE_vs_numeraire']
                                              for n in names] + [''] * len(names))
print(json.dumps(OUT, indent=1))
