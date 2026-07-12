#!/usr/bin/env python3
"""READ-ONLY illustration of the G-Y0 identity: composition-weighted mean V0* vs the PVC, per pick band.

Runs against the PINNED v2.8 workspace (store 04f38dad / engine 7a07e369) — nothing written outside
the scratchpad. This is an ILLUSTRATION for the ruling paper, not the seam table (the adoption job
computes the binding table with realized entry ages + the wk1/y1/y2 chain).

Method:
  - Boot the shipped ev stack (exec _merged_recover.py, the SIM protocol from the icbhpu branch).
  - Sanity: shipped-board anchor parity (bontempelli 3721 · gawn 2538 · briggs 2221).
  - V0*(pos, pick) = the engine's D14 V0 curve function (star), evaluated at draft age 18
    (the modal ND entry age — labeled assumption).
  - Composition weights = the ACTUAL 2004-16 ND selections (harvest.json from the derivation):
    the weighted mean over a band is the mean of star(pos_i, 18, pick_i) over its real selections.
  - Rulers (player currency, pick1 = 3157): DERIVED = derived_curve.csv pinned d15 H10 x 1.0524;
    FROZEN = pick_redenomination.json (the shipped assets).
"""
import json, io, csv, contextlib, os, sys
from collections import defaultdict

SCRATCH = os.path.dirname(os.path.abspath(__file__))
WS = '/home/claude/rl_workspace/rl_after'
os.chdir(WS)

_ens = {'__name__': '_mr_illu'}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], _ens)
ev, MA = _ens['ev'], _ens['MA']
star = _ens['_V0CURVE_META']['_star']

# --- anchor parity sanity (shipped v2.8 board values) ---
by_key = {p.get('key'): p for p in MA.players}
with contextlib.redirect_stdout(io.StringIO()):
    anchors = {k: ev(by_key[k], 2026) for k in ('marcus-bontempelli', 'max-gawn', 'kieren-briggs')}
expect = {'marcus-bontempelli': 3721, 'max-gawn': 2538, 'kieren-briggs': 2221}
assert {k: round(v) for k, v in anchors.items()} == expect, f'ANCHOR PARITY FAIL: {anchors}'
print('anchor parity PASS:', anchors)

# --- rulers in player currency ---
SHIP = 1.0524
derived = {}
for row in csv.DictReader(open(os.path.join(SCRATCH, 'derived_curve.csv'))):
    derived[int(row['pick'])] = float(row['pinned_d15_H10']) * SHIP
_redenom = json.load(open('pick_redenomination.json'))
frozen = {int(k): float(v) * _redenom['factor']
          for k, v in _redenom['frozen_v34_pvc_baked_v2_7'].items()}

# --- composition from the derivation's own harvest (ND, 2004-16 primary window) ---
harv = json.load(open(os.path.join(SCRATCH, 'harvest.json')))
sel = [e for e in harv['entries']
       if e.get('type') == 'ND' and 2004 <= e.get('year', 0) <= 2016
       and e.get('effpk') and 1 <= e['effpk'] <= 60 and e.get('G')]
print(f'selections in window: {len(sel)}')

BANDS = [(1, 5), (6, 10), (11, 20), (21, 30), (31, 45), (46, 60)]
out = {'assumption': 'V0* at draft age 18; weights = actual 2004-16 ND selections', 'bands': []}
for lo, hi in BANDS:
    rows = [e for e in sel if lo <= e['effpk'] <= hi]
    n = len(rows)
    v0s = [star(e['G'], 18, e['effpk']) for e in rows]
    pvc_d = [derived[e['effpk']] for e in rows]
    pvc_f = [frozen.get(e['effpk'], float('nan')) for e in rows]
    wmean_v0 = sum(v0s) / n
    mean_d = sum(pvc_d) / n
    mean_f = sum(pvc_f) / n
    # per-position deviation vs the derived PVC (the identity's ruler)
    pos_dev, pos_n = defaultdict(float), defaultdict(int)
    for e, v in zip(rows, v0s):
        pos_dev[e['G']] += v - derived[e['effpk']]
        pos_n[e['G']] += 1
    devs = {g: {'n': pos_n[g], 'share': round(pos_n[g] / n, 3),
                'mean_dev_vs_derived': round(pos_dev[g] / pos_n[g])} for g in sorted(pos_n)}
    net = sum(pos_dev.values()) / n   # == wmean_v0 - mean_d by construction
    band = {'band': f'{lo}-{hi}', 'n_selections': n,
            'wmean_V0': round(wmean_v0), 'derived_PVC_mean': round(mean_d),
            'frozen_asset_mean': round(mean_f),
            'gap_vs_derived': round(wmean_v0 - mean_d),
            'gap_vs_derived_pct': round(100 * (wmean_v0 - mean_d) / mean_d, 1),
            'gap_vs_frozen_pct': round(100 * (wmean_v0 - mean_f) / mean_f, 1),
            'net_dev_check': round(net), 'per_position': devs}
    out['bands'].append(band)
    print(f"band {lo:>2}-{hi:<2} n={n:>3}  wV0*={wmean_v0:7.0f}  PVCder={mean_d:7.0f}  "
          f"PVCfroz={mean_f:7.0f}  gap(der)={100*(wmean_v0-mean_d)/mean_d:+6.1f}%  "
          f"gap(froz)={100*(wmean_v0-mean_f)/mean_f:+6.1f}%")
    for g, d in devs.items():
        print(f"    {g:<8} share={d['share']:.2f}  dev vs derived={d['mean_dev_vs_derived']:+6}")

json.dump(out, open(os.path.join(SCRATCH, 'identity_illustration.json'), 'w'), indent=1)
print('written:', os.path.join(SCRATCH, 'identity_illustration.json'))
