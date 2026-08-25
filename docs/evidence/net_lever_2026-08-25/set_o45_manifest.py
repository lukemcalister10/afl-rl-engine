#!/usr/bin/env python3
"""Set RL_O45 in the candidate root's manifest to the given value ('0'|'1') and restamp
config_sha256 + expected_boot 'config' + release_contract config_sha256/contract seal coherently."""
import json, sys
sys.path.insert(0, '/home/user/arm2_norec/root_final')
import config_manifest as CM
import release_contract as RCT
val = sys.argv[1]
assert val in ('0', '1')
R = '/home/user/arm2_norec/root_final'
man = json.load(open(R + '/data/model_config.json'))
man['vars']['RL_O45'] = val
h = CM.canonical_hash(man['vars'])
man['config_sha256'] = h
json.dump(man, open(R + '/data/model_config.json', 'w'), indent=1)
boot = json.load(open(R + '/data/expected_boot.json'))
boot['config'] = h
json.dump(boot, open(R + '/data/expected_boot.json', 'w'), indent=2)
rc = json.load(open(R + '/data/release_contract.json'))
rc['config_sha256'] = h
rc['contract_sha256'] = RCT.contract_hash(rc)
json.dump(rc, open(R + '/data/release_contract.json', 'w'), indent=2)
print('manifest RL_O45=%s  config %s  contract %s' % (val, h[:12], rc['contract_sha256'][:12]))
