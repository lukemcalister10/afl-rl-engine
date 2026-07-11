#!/bin/bash
# (d) Regenerate derived artifacts for the candidate: board (rl_app_data.json) + walk-forward book (matrix)
# + re-seal the candidate book. Serial (no concurrency — the engine is CPU-heavy and contends). Assumes
# bootstrap.sh already re-seeded the workspace from the corrected checkout.
set -e
REPO=/home/user/afl-rl-engine
RA=/home/claude/rl_workspace/rl_after
SC=/tmp/claude-0/-home-user-afl-rl-engine/f2070dfe-a1e4-5548-8c3c-ecc8ab9d2f64/scratchpad
cd $RA
export PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
export PYTHONPATH=$RA:/home/claude/rl_vendor
export RL_REPO=$REPO

echo "[1/3] regenerating board (rl_export.py) ..."
python3 rl_export.py
BOARD_MD5=$(md5sum rl_app_data.json | cut -c1-8)
echo "board md5 = $BOARD_MD5"
# ship it (B4 compares regenerated vs shipped) + repo copy + eyeball source
cp -f rl_app_data.json /home/claude/rl_build/rl_app_data.json
cp -f rl_app_data.json $REPO/data/rl_build/rl_app_data.json
cp -f rl_app_data.json $SC/board_final.json

echo "[2/3] regenerating candidate walk-forward book (s4_matrix_M1v7.py) ..."
S4_MATRIX=$SC/s4_matrix_cand.json RL_CONFIG_MODE=gate python3 s4_matrix_M1v7.py > $SC/matrix_regen.log 2>&1 || { echo "matrix regen FAILED"; tail -20 $SC/matrix_regen.log; exit 1; }

echo "[3/3] re-sealing the candidate book (transparent candidate re-seal; baked/main seal untouched) ..."
python3 - << PY
import json, hashlib
MPATH="$SC/s4_matrix_cand.json"
def stable_sha(path):
    d=json.load(open(path)); by={}
    for idk,rec in d.items():
        if idk.startswith('__'): continue
        by[(rec.get('player'),rec.get('type'),rec.get('year'),rec.get('pick'))]=rec
    h=hashlib.sha256()
    for k in sorted(by.keys(), key=lambda t: json.dumps(t,sort_keys=True)):
        h.update(json.dumps(k,sort_keys=True).encode()); h.update(json.dumps(by[k],sort_keys=True,separators=(',',':')).encode())
    return h.hexdigest(), len(by)
meta=json.load(open(MPATH)).get('__meta__',{})
sha,n=stable_sha(MPATH)
store=hashlib.md5(open("$RA/rl_model_data.json",'rb').read()).hexdigest()[:8]
head=hashlib.md5(open("$RA/_merged_recover.py",'rb').read()).hexdigest()[:8]
seal={
 "_comment":"Walk-forward book freeze-stamp — RE-SEALED 2026-07-11 for the CANDIDATE pick-corrections+redenomination "
   "(branch claude/pick-corrections-redenomination-ywqmdi). NOT a bake: no tag, no main merge. The book MOVED by design "
   "— the (a) band-pool fix re-rates every player ~+5.24% and the (c) store corrections change some (player,type,year,pick) "
   "stable keys (13 rookie renumbers, 3 PSD splits, 325 _draft fills). The seal is re-pointed to THIS candidate so B3 can "
   "certify it. The BAKED/main seal (stable-sha 2a74c731, head 7a07e369, store a2fbc9a0) is UNTOUCHED upstream; an owner "
   "bake-time re-seal is still required before any promotion. Prior baked seal: v2.7 bake 2026-07-10.",
 "generator":"engine/rl_after/s4_matrix_M1v7.py",
 "head_md5":head,
 "store_md5":store,
 "n_players":n,
 "stable_sha256":sha,
 "sealed_by":"CANDIDATE re-seal 2026-07-11 (pick-corrections build; NOT a bake). Prior baked seal 2a74c731 (v2.7, 2026-07-10) preserved upstream on main.",
 "sealed_date":"2026-07-11",
 "config":meta.get('config_sha256')
}
json.dump(seal, open("$REPO/data/book_stable_seal.json",'w'), indent=2)
print("RE-SEALED: stable_sha256=%s.. n=%d head=%s store=%s"%(sha[:16],n,head,store))
print("matrix __meta__:", {k:(v[:8] if isinstance(v,str) else v) for k,v in meta.items()})
PY
echo "DONE regen_derived  board=$BOARD_MD5"
