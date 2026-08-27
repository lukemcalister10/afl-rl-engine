#!/usr/bin/env python3
"""THE COMBINED-BUILD BAKE (candidate root only) — L2 S_LL5G into the pvc artifacts + the four new
dials into the manifest + coherent pin restamps. Owner words v874/v875 ("Lock in LL5G then" + the
mechanism). Usage:  python3 bake_cand.py <ROOT>   (idempotent; originals preserved under
docs/evidence/combined_build_2026-08-27/pre_bake/ on the first run).

Asserts before writing: smoothed pick-1 == 3000 exactly (the numeraire pin, law 4), strict descent
on the smoothed curve AND every posv row (law 4 / R104.9), position set unchanged. HALTS otherwise.
"""
import hashlib, json, os, shutil, sys

ROOT = os.path.abspath(sys.argv[1])
RA = os.path.join(ROOT, 'engine', 'rl_after')
EV = os.path.join(ROOT, 'docs', 'evidence', 'combined_build_2026-08-27')
SM = json.load(open(os.path.join(ROOT, 'docs/evidence/curve_smooth_study_2026-08-25/S_LL5G_POSV.json')))

pre = os.path.join(EV, 'pre_bake')
os.makedirs(pre, exist_ok=True)
for f in ('pvc_curve_v2.json', 'pvc_snapshot.json'):
    dst = os.path.join(pre, f)
    if not os.path.exists(dst):
        shutil.copy2(os.path.join(RA, f), dst)

curve = {k: float(v) for k, v in SM['curve'].items()}
posv = {g: {k: float(v) for k, v in row.items()} for g, row in SM['posv'].items()}
if curve['1'] != 3000.0:
    raise SystemExit('BAKE HALT: smoothed pick-1 != 3000 — the numeraire pin (law 4) is broken.')
def _desc(d):
    v = [d[str(i)] for i in sorted(int(k) for k in d)]
    return all(a > b for a, b in zip(v, v[1:]))
if not _desc(curve) or not all(_desc(r) for r in posv.values()):
    raise SystemExit('BAKE HALT: the smoothed tables are not strictly decreasing everywhere.')

pvc = json.load(open(os.path.join(pre, 'pvc_curve_v2.json')))
if set(posv) != set(pvc['nd_v0']['posv']):
    raise SystemExit('BAKE HALT: position set changed.')
pvc['curve'] = curve
pvc['nd_v0']['posv'] = posv
pvc['curve_md5'] = hashlib.md5(json.dumps(curve, sort_keys=True).encode()).hexdigest()[:8]
pvc['r104_9_strict_descent'] = True
pvc['sll5g_bake'] = {'date': '2026-08-27', 'owner_word': 'Lock in LL5G then (register v874)',
                     'source': 'docs/evidence/curve_smooth_study_2026-08-25/S_LL5G_POSV.json',
                     'conservation_drift_pct': -0.18,
                     'pre_bake_originals': 'docs/evidence/combined_build_2026-08-27/pre_bake/'}
json.dump(pvc, open(os.path.join(RA, 'pvc_curve_v2.json'), 'w'), indent=0, sort_keys=True)
# pvc_snapshot.json is NOT touched: it is the peak model's FROZEN train-time PVC feature
# (rl_model.py:1234 — "must NOT track [the live curve]; feeding the live PVC here would be
# train/serve skew; regenerated only by the peak-model build"). The first draft of this bake
# re-derived it from the smoothed curve and was caught by the artifact's own key range before
# any wrong number was produced — filed in the register.

man = json.load(open(os.path.join(ROOT, 'data', 'model_config.json')))
sys.path.insert(0, ROOT)
import config_manifest as CM
for k, v in (('RL_O46', '1'), ('RL_O47', '1'), ('RL_O48', '1'), ('RL_O48_W', '0.25')):
    man['vars'][k] = v
man['config_sha256'] = CM.canonical_hash(man['vars'])
json.dump(man, open(os.path.join(ROOT, 'data', 'model_config.json'), 'w'), indent=1, sort_keys=True)

eb = json.load(open(os.path.join(ROOT, 'data', 'expected_boot.json')))
eb['engine_head'] = hashlib.md5(open(os.path.join(RA, '_merged_recover.py'), 'rb').read()).hexdigest()
eb['config'] = man['config_sha256']
json.dump(eb, open(os.path.join(ROOT, 'data', 'expected_boot.json'), 'w'), indent=1, sort_keys=True)
print('BAKED: curve_md5 %s · config %s · engine_head %s · pvc_snapshot %s'
      % (pvc['curve_md5'], man['config_sha256'][:8], eb['engine_head'][:8], eb['pvc_snapshot'][:8]))
