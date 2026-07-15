#!/usr/bin/env python3
"""L-CAPTAIN WIRE — B3 walk-forward book RE-SEAL. The ruled captain curve replaces the retired saturating
capt_prem in rl_model.py; the book is engine-ev()-derived and the credit rides EVERY credited historical season
(register item 77 / L-CAPTAIN: the credit applies wherever a level is priced), so the book's columns move and
stable_sha256 advances. engine_head (_merged_recover.py) is UNCHANGED (fc7045d6) — only rl_model.py moved — so
head_md5 stays fc7045d6; the resealed stable_sha256 carries the real (ruled) content. Regenerates the candidate
matrix EXACTLY as ship_gates B3 does (s4_matrix_M1v7.py, gate mode => RL_CAPT unset => code default ON => ruled),
verifies engine/store stamps == the candidate, recomputes the stable-key sha256, rewrites data/book_stable_seal.json.
Store/config UNCHANGED. Candidate — owner tag/main promote owner-only.
"""
import json, sys, hashlib, os, subprocess, tempfile
ROOT = '/home/user/afl-rl-engine'; RA = '/home/claude/rl_workspace/rl_after'
HEAD = hashlib.md5(open(os.path.join(RA, '_merged_recover.py'), 'rb').read()).hexdigest()[:8]
RLMODEL = hashlib.md5(open(os.path.join(RA, 'rl_model.py'), 'rb').read()).hexdigest()[:8]
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
_fd, mpath = tempfile.mkstemp(prefix='s4_reseal_captaincy_', suffix='.json'); os.close(_fd)
env = {k: v for k, v in os.environ.items() if not k.startswith('SGC_') and not k.startswith('RL_CAPT')}
env.update(S4_MATRIX=mpath, RL_CONFIG_MODE='gate', RL_REPO=ROOT, PYTHONHASHSEED='0',
           RL_GAMMA='0.85', RL_PICK1='3000', RL_RUCK_TAX='0.25', RL_RECENCY_DECAY='0.72',
           RL_PRIOR_TREES='400', PAR_RAMPS='22', PYTHONPATH=RA + ':/home/claude/rl_vendor')
print('regenerating candidate matrix (gate mode; RL_CAPT default ON => ruled) ...')
r = subprocess.run([sys.executable, 's4_matrix_M1v7.py'], cwd=RA, env=env, capture_output=True, text=True, timeout=1800)
meta = json.load(open(mpath)).get('__meta__', {}) if os.path.exists(mpath) else {}
if not meta:
    print('FAILED: no __meta__ (exit=%s)\n%s' % (r.returncode, r.stderr[-1500:])); sys.exit(1)
eng, sto, cfg = meta.get('engine_head_md5', '')[:8], meta.get('store_md5', '')[:8], meta.get('config_sha256')
print('matrix meta: engine=%s store=%s config=%s' % (eng, sto, (cfg or '')[:12]))
assert eng == HEAD, 'engine mismatch %s != %s' % (eng, HEAD)
assert sto == STORE, 'store mismatch %s != %s' % (sto, STORE)
old = json.load(open(os.path.join(ROOT, 'data', 'book_stable_seal.json')))
sha, by = stable(mpath)
cfg_full = json.load(open(os.path.join(ROOT, 'data', 'model_config.json'))).get('config_sha256')
seal = {
    "_comment": ("Walk-forward book freeze-stamp — RE-SEALED 2026-07-15 at the L-CAPTAIN candidate (the ruled "
                 "captain curve credit(L)=G*integral[BAR->L]P replaces the retired saturating capt_prem in "
                 "rl_model.py). The book is engine-ev()-derived and the credit rides every credited historical "
                 "season, so it is RE-BUILT on the candidate engine (G-BOOK: the formula moved) and re-stamped. "
                 "engine_head (_merged_recover.py) UNCHANGED fc7045d6; rl_model.py moved -> %s. Store/config "
                 "UNCHANGED. Owner tag/main owner-only." % RLMODEL),
    "generator": "engine/rl_after/s4_matrix_M1v7.py",
    "head_md5": HEAD, "store_md5": STORE, "n_players": len(by), "stable_sha256": sha,
    "sealed_by": ("L-CAPTAIN re-seal 2026-07-15 (session_2026-07-15/captaincy; rl_model 952ddb3d -> %s ruled "
                  "captain curve; engine_head fc7045d6 UNCHANGED; store b1fd0bce UNCHANGED). stable_sha256 %s -> "
                  "%s because the captaincy credit moves in ev() (and thus the book) at every level it prices. "
                  "Candidate — owner tag/main promote owner-only." % (RLMODEL, old.get('stable_sha256', '')[:8], sha[:8])),
    "sealed_date": "2026-07-15", "config": cfg_full,
}
json.dump(seal, open(os.path.join(ROOT, 'data', 'book_stable_seal.json'), 'w'), indent=2)
os.remove(mpath)
print('RE-SEALED: head %s (unchanged) | rl_model 952ddb3d -> %s | n_players %s | stable_sha256 %s -> %s'
      % (HEAD, RLMODEL, len(by), old.get('stable_sha256', '')[:8], sha[:8]))
