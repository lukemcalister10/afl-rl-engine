#!/bin/bash
# SWEEP — DISCOUNT SENSITIVITY (read-only SIM on the LEVERED board; NO lens change ships).
# Reuses the derivation-pack SIM discipline (branch f686872, run_sim.sh/patch_C_lens.py): patch the
# WORKSPACE copy of rl_model.py LENS['bal'] 0.15 -> r, regenerate the board per rate, RESTORE the
# pristine engine + md5-verify after every arm. The repo engine is never touched.
# usage: run_discount_sweep.sh <scratch_dir>
set -e
SC=$1
RA=/home/claude/rl_workspace/rl_after
REPO=/home/user/afl-rl-engine
cd $RA
export PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
export PYTHONPATH=$RA:/home/claude/rl_vendor
export RL_REPO=$REPO
PRISTINE=$(md5sum rl_model.py | cut -c1-32)
cp rl_model.py $SC/rl_model_pristine.py
restore() { cp -f $SC/rl_model_pristine.py $RA/rl_model.py; }
trap restore EXIT

# baseline (15%) = the shipped levered board 9ecbe0fa, already committed — not re-run.
for R in 0.14 0.13 0.12; do
  restore
  python3 - "$R" <<'PY'
import sys
r = sys.argv[1]
src = open('rl_model.py').read()
OLD = "LENS={'now':0.34,'bal':0.15,'fut':0.05}"
NEW = "LENS={'now':0.34,'bal':%s,'fut':0.05}  # SIM (discount sweep): read-only arm" % r
assert src.count(OLD) == 1, 'LENS literal not found exactly once'
open('rl_model.py', 'w').write(src.replace(OLD, NEW))
print('patched bal ->', r)
PY
  echo "[sweep] rate $R: regenerating board ..."
  python3 rl_export.py > $SC/sweep_export_$R.log 2>&1
  cp -f rl_app_data.json $SC/board_disc_$R.json
  md5sum rl_app_data.json | cut -c1-8
done
restore
NOW=$(md5sum $RA/rl_model.py | cut -c1-32)
[ "$NOW" = "$PRISTINE" ] || { echo "ENGINE NOT RESTORED ($NOW != $PRISTINE)"; exit 1; }
# restore the shipped levered board into the workspace (rl_export overwrote it)
cp -f $REPO/data/rl_build/rl_app_data.json $RA/rl_app_data.json
md5sum $RA/rl_app_data.json | cut -c1-8
echo "sweep arms done; pristine engine verified restored"
