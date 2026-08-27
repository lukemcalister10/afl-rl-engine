#!/usr/bin/env python3
"""Coherent dial flip for the combined-build candidate (the set_o45_manifest pattern):
   python3 set_cand_dials.py <ROOT> 0|1
Sets RL_O46/RL_O47/RL_O48 to the given state in data/model_config.json and restamps
config_sha256 + expected_boot's config pin, so gate mode accepts either posture coherently.
RL_O48_W is left as declared (a weight, not a switch). Requires the dials to already exist
in the manifest (bake_cand.py adds them) — refuses to invent them here.
"""
import json, os, sys

ROOT = os.path.abspath(sys.argv[1]); state = sys.argv[2]
assert state in ('0', '1')
sys.path.insert(0, ROOT)
import config_manifest as CM
man = json.load(open(os.path.join(ROOT, 'data', 'model_config.json')))
for k in ('RL_O46', 'RL_O47', 'RL_O48'):
    if k not in man['vars']:
        raise SystemExit('set_cand_dials HALT: %s not in the manifest — run bake_cand.py first.' % k)
    man['vars'][k] = state
man['config_sha256'] = CM.canonical_hash(man['vars'])
json.dump(man, open(os.path.join(ROOT, 'data', 'model_config.json'), 'w'), indent=1, sort_keys=True)
eb = json.load(open(os.path.join(ROOT, 'data', 'expected_boot.json')))
eb['config'] = man['config_sha256']
json.dump(eb, open(os.path.join(ROOT, 'data', 'expected_boot.json'), 'w'), indent=1, sort_keys=True)
print('dials 46/47/48 = %s · config %s' % (state, man['config_sha256'][:8]))
