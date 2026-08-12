#!/usr/bin/env python3
"""ORDER 22 -- THE LEVEL STAGER. Writes derived pool entry levels into a SCRATCHPAD WORKTREE's
`engine/rl_after/pvc_curve_v2.json` `pool_levels` block, and nothing else.

  usage: o22_levels.py <worktree> <levels.json>

`levels.json` carries exactly the two fields ORDER 22 is authorised to move:

    {"signed_flat": {"MSD": ..., "SSP": ..., "PDA": ..., "PDS": ..., "IRE": ..., "PDN": ..., "UNR": ...},
     "signed_rd_positional": {"KPD": ..., "MID": ..., "RUCK": ..., "SD": ..., "SF": ..., "KPF": ...},
     "nd65_measured_k15": ...}

THE CHECKOUT'S engine/rl_after/pvc_curve_v2.json IS NEVER WRITTEN BY THIS SCRIPT. Only a worktree
under the scratchpad is touched, and the worktree is destroyed by the builder afterwards.

TWO THINGS THIS SCRIPT DECLARES RATHER THAN HIDES.

1. **THE ENGINE TRUNCATES.** `rl_model.py:1425-1427` builds `_POOL_LEVELS` with `int(float(v))`.
   A level written as 83.7 IS 83 in the engine. This script prints the truncation cost per level so
   the quantisation is a measured number in the packet and not a surprise.

2. **THESE ARE OWNER-SIGNED NUMBERS.** `one_source_selftest.py:624-626` carries the N43 signature as
   literals (`_N43_FLAT`, `_N43_RD`, `_N43_ND65_K15`) and checks the artifact against them, precisely
   so an edited level cannot agree with itself. The board build (`rl_export.py`) does not run that
   gate, so this staging does not trip it -- but ADOPTION REQUIRES THE OWNER TO RE-SIGN those literals.
   That is a feature of the design, it is reported in the packet, and this script does not touch the
   selftest.
"""
import sys, json, pathlib

wt, lev_path = sys.argv[1], sys.argv[2]
L = json.load(open(lev_path))
f = pathlib.Path(wt + '/engine/rl_after/pvc_curve_v2.json')
d = json.loads(f.read_text())
pl = d['pool_levels']

assert set(L['signed_flat']) == set(pl['signed_flat']), \
    "flat key set moved: %s vs %s" % (sorted(L['signed_flat']), sorted(pl['signed_flat']))
assert set(L['signed_rd_positional']) == set(pl['signed_rd_positional']), "rd positional key set moved"

before = dict(flat=dict(pl['signed_flat']), rd=dict(pl['signed_rd_positional']),
              nd65=pl['signed_nd65_plus']['measured_k15'])

pl['signed_flat'] = {k: round(float(v), 4) for k, v in L['signed_flat'].items()}
pl['signed_rd_positional'] = {k: round(float(v), 4) for k, v in L['signed_rd_positional'].items()}
pl['signed_nd65_plus']['measured_k15'] = round(float(L['nd65_measured_k15']), 4)
pl['_ORDER22_STAGED'] = ("ORDER 22 DERIVED LEVELS, STAGED ONLY -- NOT SIGNED, NOT LANDED. The N43 owner "
                         "signature is unchanged in the checkout and in one_source_selftest.py; adoption "
                         "requires the owner to re-sign those literals.")
f.write_text(json.dumps(d, indent=1) + "\n")

print("  LEVELS STAGED (engine truncates to int -- cost printed):")
print("    %-10s %10s %10s %10s %10s" % ('key', 'before', 'written', 'engine int', 'trunc %'))
for k in sorted(before['flat']):
    b = float(before['flat'][k]); w = float(pl['signed_flat'][k]); i = int(w)
    print("    %-10s %10.1f %10.4f %10d %9.3f%%" % (k, b, w, i, 100.0 * (i - w) / w))
for k in sorted(before['rd']):
    b = float(before['rd'][k]); w = float(pl['signed_rd_positional'][k]); i = int(w)
    print("    RD:%-7s %10.1f %10.4f %10d %9.3f%%" % (k, b, w, i, 100.0 * (i - w) / w))
b = float(before['nd65']); w = float(pl['signed_nd65_plus']['measured_k15'])
cap = int(d['curve'][str(int(pl['signed_nd65_plus']['cap_against_curve_pick']))])
eff = min(w, float(cap))
print("    %-10s %10.1f %10.4f %10d %9.3f%%   [cap curve[%d]=%d -> effective %d, cap %s]"
      % ('ND65+', b, w, int(eff), 100.0 * (int(eff) - eff) / eff,
         int(pl['signed_nd65_plus']['cap_against_curve_pick']), cap, int(eff),
         'BINDS' if w > cap else 'does not bind'))
