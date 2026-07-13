#!/usr/bin/env python3
"""v2.9 BAKE — B3 BOOK RE-SEAL. The walk-forward book is engine-ev()-derived; the L7 bake is display-only
(engine 2030e5df UNCHANGED), so the book content is the refit candidate's. This moves the seal head
7a07e369 -> 2030e5df so B3 reads PASS (sealed head == candidate head), not differs-by-design.

Regenerates the candidate matrix EXACTLY as ship_gates B3 does (s4_matrix_M1v7.py, gate mode), verifies its
embedded engine/store/config stamps == the candidate, computes the stable-key sha256 (same algorithm as
ship_gates B3), and writes data/book_stable_seal.json. Run from the bootstrapped workspace.
"""
import json, sys, hashlib, os, subprocess, tempfile

ROOT = '/home/user/afl-rl-engine'
RA = '/home/claude/rl_workspace/rl_after'
HEAD = hashlib.md5(open(os.path.join(RA, '_merged_recover.py'), 'rb').read()).hexdigest()[:8]
STORE = hashlib.md5(open(os.path.join(RA, 'rl_model_data.json'), 'rb').read()).hexdigest()[:8]

def stable(path):
    d = json.load(open(path)); by = {}
    for _idk, rec in d.items():
        if _idk.startswith('__'):
            continue
        by[(rec.get('player'), rec.get('type'), rec.get('year'), rec.get('pick'))] = rec
    h = hashlib.sha256()
    for k in sorted(by.keys(), key=lambda t: json.dumps(t, sort_keys=True)):
        h.update(json.dumps(k, sort_keys=True).encode())
        h.update(json.dumps(by[k], sort_keys=True, separators=(',', ':')).encode())
    return h.hexdigest(), by

_fd, mpath = tempfile.mkstemp(prefix='s4_reseal_', suffix='.json'); os.close(_fd)
env = dict(os.environ, S4_MATRIX=mpath, RL_CONFIG_MODE='gate', RL_REPO=ROOT, PYTHONHASHSEED='0',
           PYTHONPATH=RA + ':/home/claude/rl_vendor')
print('regenerating candidate matrix (gate mode) ...')
r = subprocess.run([sys.executable, 's4_matrix_M1v7.py'], cwd=RA, env=env, capture_output=True, text=True, timeout=1800)
meta = json.load(open(mpath)).get('__meta__', {}) if os.path.exists(mpath) else {}
if not meta:
    print('FAILED: no __meta__ (exit=%s)\n%s' % (r.returncode, r.stderr[-500:])); sys.exit(1)
eng, sto, cfg = meta.get('engine_head_md5', '')[:8], meta.get('store_md5', '')[:8], meta.get('config_sha256')
print('matrix meta: engine=%s store=%s config=%s' % (eng, sto, cfg[:12] if cfg else None))
assert eng == HEAD, 'engine mismatch %s != %s' % (eng, HEAD)
assert sto == STORE, 'store mismatch %s != %s' % (sto, STORE)
sha, by = stable(mpath)
cfg_full = json.load(open(os.path.join(ROOT, 'data', 'model_config.json'))).get('config_sha256')
seal = {
    "_comment": ("Walk-forward book freeze-stamp — RE-SEALED 2026-07-13 at the v2.9 BAKE for the refit "
                 "candidate (engine 2030e5df, store b0c39d78). The L7 numéraire bake is DISPLAY-ONLY (board "
                 "presentation ÷1.0524 + adopted-curve repoint + Brodie override); the walk-forward book is "
                 "engine-ev()-derived and UNCHANGED by it, so this re-seal simply advances the sealed head "
                 "7a07e369 -> 2030e5df (the refit engine that B3 previously flagged differs-by-design). "
                 "Owner tag/main promote remain owner-only."),
    "generator": "engine/rl_after/s4_matrix_M1v7.py",
    "head_md5": HEAD,
    "store_md5": STORE,
    "n_players": len(by),
    "stable_sha256": sha,
    "sealed_by": "v2.9 BAKE re-seal 2026-07-13 (refit engine 2030e5df; L7 display-only, book unchanged)",
    "sealed_date": "2026-07-13",
    "config": cfg_full,
}
json.dump(seal, open(os.path.join(ROOT, 'data', 'book_stable_seal.json'), 'w'), indent=2)
os.remove(mpath)
print('RE-SEALED: head %s | store %s | n %d | stable_sha256 %s' % (HEAD, STORE, len(by), sha[:16] + '..'))
