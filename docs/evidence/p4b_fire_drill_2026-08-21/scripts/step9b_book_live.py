#!/usr/bin/env python3
"""P4b FIRE DRILL — step 9b: CONTROL. Does the LIVE HEAD's committed s4_matrix.json satisfy the
LIVE book_stable_seal.json? Read-only; attributes the step-9 finding to the tag or to the estate."""
import json, hashlib

LIVE = '/home/user/afl-rl-engine/.claude/worktrees/agent-a08984efece15f9d4'


def stable(path):
    d = json.load(open(path)); by = {}
    for _idk, rec in d.items():
        if _idk.startswith('__'):
            continue
        by[(rec.get('player'), rec.get('type'), rec.get('year'), rec.get('pick'))] = rec
    h = hashlib.sha256()
    for k in sorted(by, key=lambda t: json.dumps(t, sort_keys=True)):
        h.update(json.dumps(k, sort_keys=True).encode())
        h.update(json.dumps(by[k], sort_keys=True, separators=(',', ':')).encode())
    return h.hexdigest(), by


seal = json.load(open(LIVE + '/data/book_stable_seal.json'))
p = LIVE + '/engine/rl_after/s4_matrix.json'
sha, by = stable(p)
d = json.load(open(p))
print('LIVE committed seal : stable %s  n_players %s  head %s  store %s'
      % (seal['stable_sha256'][:32], seal['n_players'], seal['head_md5'], seal['store_md5']))
print('LIVE book file      : raw md5 %s | top-level keys %d | stable-keyed rows %d'
      % (hashlib.md5(open(p, 'rb').read()).hexdigest(), len(d), len(by)))
print('LIVE book stable    : %s -> %s'
      % (sha[:32], 'SEAL MATCH' if sha == seal['stable_sha256'] else 'SEAL MISMATCH'))
print('top-level key sample: %s' % [k for k in d if not k.startswith('__')][:3])
