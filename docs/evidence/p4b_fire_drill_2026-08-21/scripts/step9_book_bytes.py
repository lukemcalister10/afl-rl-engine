#!/usr/bin/env python3
"""P4b FIRE DRILL — step 9: does the RESTORED BOOK FILE ITSELF satisfy the tag's committed seal?
step 8 regenerated a book and sealed that; this asks the byte-restore question directly, and it
also explains why the raw md5 of s4_matrix.json is not reproducible across runs."""
import json, hashlib, sys

REST = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/p4b/restore'
BLD  = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/p4b/rebuild'


def stable(path):
    """byte-for-byte the gate's own _b3_stable_sha / reseal_bake.stable()."""
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


seal = json.load(open(REST + '/data/book_stable_seal.json'))
print('committed seal      : stable %s  n_players %s  head %s  store %s'
      % (seal['stable_sha256'], seal['n_players'], seal['head_md5'], seal['store_md5']))

for label, path in (('RESTORED book file  ', REST + '/engine/rl_after/s4_matrix.json'),
                    ('REBUILT  book file  ', BLD + '/engine/rl_after/s4_matrix.json')):
    raw = hashlib.md5(open(path, 'rb').read()).hexdigest()
    sha, by = stable(path)
    d = json.load(open(path))
    print('%s: raw md5 %s | top-level keys %d | stable-keyed rows %d | stable %s -> %s'
          % (label, raw, len(d), len(by), sha, 'SEAL MATCH' if sha == seal['stable_sha256'] else 'SEAL MISMATCH'))

# why the raw md5 is not reproducible: the top-level keys are CPython id() values
d = json.load(open(REST + '/engine/rl_after/s4_matrix.json'))
ks = [k for k in d if not k.startswith('__')][:4]
print()
print('top-level key sample (restored): %s' % ks)
print('  -> these are CPython id() values, so the raw file is not byte-reproducible across processes,')
print('     and an id COLLISION silently drops a row from the raw file (see the row counts above).')
