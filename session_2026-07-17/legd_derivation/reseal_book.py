#!/usr/bin/env python3
"""LEG D ACT-2 (PVC re-derivation, RL_PVC2) — B3 walk-forward book RE-SEAL. The ev-channel _PVC0 swap to the
composed-pathway curve moves ev() for the young rows whose V0-scaffold/RUC-cap/floor read draftval, so the
book's present + walk-forward columns move for those rows and stable_sha256 advances (G-BOOK: the formula
moved -> re-BUILT on the candidate engine and re-stamped, not re-hashed). Store/config UNCHANGED. RL_PVC2=0
reproduces the L1b book. Candidate — owner tag/main promote owner-only.
Regenerates the candidate matrix EXACTLY as ship_gates B3 does, verifies the embedded engine/store stamps ==
the candidate, rewrites data/book_stable_seal.json."""
import json, sys, hashlib, os, subprocess, tempfile
ROOT = '/home/user/afl-rl-engine'; RA = '/home/claude/rl_workspace/rl_after'
HEAD = hashlib.md5(open(os.path.join(RA, '_merged_recover.py'), 'rb').read()).hexdigest()[:8]
STORE = hashlib.md5(open(os.path.join(RA, 'rl_model_data.json'), 'rb').read()).hexdigest()[:8]
def stable(path):
    d = json.load(open(path)); by = {}
    for _idk, rec in d.items():
        if _idk.startswith('__'): continue
        by[(rec.get('player'), rec.get('type'), rec.get('year'), rec.get('pick'))] = rec
    h = hashlib.sha256()
    for k in sorted(by.keys(), key=lambda t: json.dumps(t, sort_keys=True)):
        h.update(json.dumps(k, sort_keys=True).encode())
        h.update(json.dumps(by[k], sort_keys=True, separators=(',', ':')).encode())
    return h.hexdigest(), by
_fd, mpath = tempfile.mkstemp(prefix='s4_reseal_legd_', suffix='.json'); os.close(_fd)
env = {k: v for k, v in os.environ.items() if not k.startswith('SGC_')}
env.update(S4_MATRIX=mpath, RL_CONFIG_MODE='gate', RL_REPO=ROOT, PYTHONHASHSEED='0',
           RL_GAMMA='0.85', RL_PICK1='3000', RL_RUCK_TAX='0.25', RL_RECENCY_DECAY='0.72',
           RL_PRIOR_TREES='400', PAR_RAMPS='22', PYTHONPATH=RA + ':/home/claude/rl_vendor')
print('regenerating candidate matrix (gate mode, RL_PVC2 default ON) ...')
r = subprocess.run([sys.executable, 's4_matrix_M1v7.py'], cwd=RA, env=env, capture_output=True, text=True, timeout=1800)
meta = json.load(open(mpath)).get('__meta__', {}) if os.path.exists(mpath) else {}
if not meta:
    print('FAILED: no __meta__ (exit=%s)\n%s' % (r.returncode, r.stderr[-1500:])); sys.exit(1)
eng, sto = meta.get('engine_head_md5', '')[:8], meta.get('store_md5', '')[:8]
print('matrix meta: engine=%s store=%s' % (eng, sto))
assert eng == HEAD, 'engine mismatch %s != %s' % (eng, HEAD)
assert sto == STORE, 'store mismatch %s != %s' % (sto, STORE)
old = json.load(open(os.path.join(ROOT, 'data', 'book_stable_seal.json')))
sha, by = stable(mpath)
cfg_full = json.load(open(os.path.join(ROOT, 'data', 'model_config.json'))).get('config_sha256')
seal = {
    "_comment": ("Walk-forward book freeze-stamp — RE-SEALED 2026-07-17 at the LEG D ACT-2 PVC re-derivation "
                 "candidate (RL_PVC2, the composed-pathway ev-channel _PVC0 swap, default ON). The book is "
                 "engine-ev()-derived; the swap moves ev() for the young rows whose scaffold/cap/floor read "
                 "draftval, so it is RE-BUILT on the candidate engine (G-BOOK) and re-stamped, not re-hashed. "
                 "Store/config UNCHANGED. RL_PVC2=0 reproduces the L1b book. Owner tag/main owner-only."),
    "generator": "engine/rl_after/s4_matrix_M1v7.py",
    "head_md5": HEAD, "store_md5": STORE, "n_players": len(by), "stable_sha256": sha,
    "sealed_by": ("LEG D ACT-2 re-seal 2026-07-17 (session_2026-07-17/legd_derivation; engine bea8fea8 -> %s, the "
                  "RL_PVC2 composed-pathway swap; store 968de0c7 UNCHANGED). stable_sha256 %s -> %s because the young "
                  "rows the tail lift touches move in ev() and thus in the book. Candidate — owner tag/main owner-only."
                  % (HEAD, old.get('stable_sha256', '')[:8], sha[:8])),
    "sealed_date": "2026-07-17", "config": cfg_full,
}
json.dump(seal, open(os.path.join(ROOT, 'data', 'book_stable_seal.json'), 'w'), indent=2)
os.remove(mpath)
print('RE-SEALED: head %s -> %s | n_players %s | stable_sha256 %s -> %s'
      % (old.get('head_md5'), HEAD, len(by), old.get('stable_sha256', '')[:8], sha[:8]))
