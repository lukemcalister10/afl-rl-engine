#!/usr/bin/env python3
"""R100.11 REWORK — B3 walk-forward book RE-SEAL. The book is engine-ev()-derived; the evidence-fade rework
moves ev() for the ~28 gap players the absence term touches, so the book's present-year and walk-forward
columns for those rows move and stable_sha256 advances. Regenerates the candidate matrix EXACTLY as
ship_gates B3 does (s4_matrix_M1v7.py, gate mode), verifies its embedded engine/store/config stamps ==
the candidate, computes the same stable-key sha256, and rewrites data/book_stable_seal.json.
Store/config UNCHANGED; only head_md5 + stable_sha256 move. Candidate — owner tag/main promote remain owner-only.
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

_fd, mpath = tempfile.mkstemp(prefix='s4_reseal_r100_11_', suffix='.json'); os.close(_fd)
env = dict(os.environ, S4_MATRIX=mpath, RL_CONFIG_MODE='gate', RL_REPO=ROOT, PYTHONHASHSEED='0',
           RL_GAMMA='0.85', RL_PICK1='3000', RL_RUCK_TAX='0.25', RL_RECENCY_DECAY='0.72',
           RL_PRIOR_TREES='400', PAR_RAMPS='22',
           PYTHONPATH=RA + ':/home/claude/rl_vendor')
print('regenerating candidate matrix (gate mode) ...')
r = subprocess.run([sys.executable, 's4_matrix_M1v7.py'], cwd=RA, env=env, capture_output=True, text=True, timeout=1800)
meta = json.load(open(mpath)).get('__meta__', {}) if os.path.exists(mpath) else {}
if not meta:
    print('FAILED: no __meta__ (exit=%s)\n%s' % (r.returncode, r.stderr[-800:])); sys.exit(1)
eng, sto, cfg = meta.get('engine_head_md5', '')[:8], meta.get('store_md5', '')[:8], meta.get('config_sha256')
print('matrix meta: engine=%s store=%s config=%s' % (eng, sto, cfg[:12] if cfg else None))
assert eng == HEAD, 'engine mismatch %s != %s' % (eng, HEAD)
assert sto == STORE, 'store mismatch %s != %s' % (sto, STORE)
old = json.load(open(os.path.join(ROOT, 'data', 'book_stable_seal.json')))
sha, by = stable(mpath)
cfg_full = json.load(open(os.path.join(ROOT, 'data', 'model_config.json'))).get('config_sha256')
seal = {
    "_comment": ("Walk-forward book freeze-stamp — RE-SEALED 2026-07-15 at the R100.11 REWORK candidate "
                 "(absence penalty fades on EVIDENCE, not a schedule). The book is engine-ev()-derived; the "
                 "evidence-fade moves ev() for the gap players the absence term touches, so it is RE-BUILT on "
                 "the reworked engine (G-BOOK: the formula moved) and re-stamped, not re-hashed. Store/config "
                 "UNCHANGED. Owner tag/main promote remain owner-only."),
    "generator": "engine/rl_after/s4_matrix_M1v7.py",
    "head_md5": HEAD,
    "store_md5": STORE,
    "n_players": len(by),
    "stable_sha256": sha,
    "sealed_by": ("R100.11 REWORK re-seal 2026-07-15 (session_2026-07-15/r100_11_rework; engine "
                  "118f8ac6 -> %s evidence-fade; store 340a7a32 UNCHANGED). stable_sha256 %s -> %s because the "
                  "gap players the absence term touches move in ev() and thus in the book. head_md5 stamp "
                  "advanced 118f8ac6 -> %s. Candidate — owner tag/main promote remain owner-only."
                  % (HEAD, old.get('stable_sha256', '')[:8], sha[:8], HEAD)),
    "sealed_date": "2026-07-15",
    "config": cfg_full,
}
json.dump(seal, open(os.path.join(ROOT, 'data', 'book_stable_seal.json'), 'w'), indent=2)
os.remove(mpath)
print('RE-SEALED: head %s -> %s | n_players %s | stable_sha256 %s -> %s'
      % (old.get('head_md5'), HEAD, len(by), old.get('stable_sha256', '')[:8], sha[:8]))
