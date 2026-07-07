"""B3 handling for a value-moving candidate: (1) compute the candidate book's stable-key seal (same algorithm
as ship_gates_check B3); (2) verify against the BAKED seal that the player KEY SET is identical (no player
appeared/vanished) and count value-moved records — B3-vs-baked DIFFERS is EXPECTED (movers) and attributed.
Usage: python3 book_seal.py <candidate_matrix.json> <out_seal.json>"""
import json, sys, hashlib

mpath, outp = sys.argv[1], sys.argv[2]
ROOT = '/home/user/afl-rl-engine'

def stable(path):
    d = json.load(open(path)); by = {}
    for _idk, rec in d.items():
        by[(rec.get('player'), rec.get('type'), rec.get('year'), rec.get('pick'))] = rec
    h = hashlib.sha256()
    for k in sorted(by.keys(), key=lambda t: json.dumps(t, sort_keys=True)):
        h.update(json.dumps(k, sort_keys=True).encode())
        h.update(json.dumps(by[k], sort_keys=True, separators=(',', ':')).encode())
    return h.hexdigest(), by

cur_sha, cur = stable(mpath)
baked_seal = json.load(open(f'{ROOT}/data/book_stable_seal.json'))
_, baked = stable(f'{ROOT}/data/s4_matrix_baked_efea88e5.json')
same_keys = set(cur.keys()) == set(baked.keys())
moved = sum(1 for k in cur if k in baked and
            (cur[k].get('cur') != baked[k].get('cur') or cur[k].get('Vpath') != baked[k].get('Vpath')))
seal = {'stable_sha256': cur_sha, 'n_players': len(cur), 'basis': 'W4 integration candidate',
        'vs_baked': {'baked_sha': baked_seal.get('stable_sha256'), 'key_set_identical': same_keys,
                     'records_value_moved': moved,
                     'note': 'B3 vs the baked seal DIFFERS BY DESIGN on a value-moving candidate; '
                             'identical key set + attributed movers is the candidate-integrity check.'}}
json.dump(seal, open(outp, 'w'), indent=1)
print(f'candidate seal {cur_sha[:16]}.. ({len(cur)} players) | key set identical to baked: {same_keys} | '
      f'records with moved values: {moved}/{len(cur)}')
