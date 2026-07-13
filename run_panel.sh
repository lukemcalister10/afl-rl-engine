#!/bin/bash
# Reproduce the fixed panel. OFFLINE-safe (vendored unidecode on PYTHONPATH).
HERE=$(cd "$(dirname "$0")" && pwd)
WS=/home/claude/rl_workspace/rl_after
# GUARD 5 (boot-store): HALT before the engine loads if the workspace store/head is not the checked-out,
# pinned store. Closes the stale-boot hole the four data guards miss (they validate whichever dir they are
# imported from, so a stale-but-self-consistent workspace passes them). Re-run bootstrap.sh to re-seed.
RL_REPO="$HERE" python3 "$HERE/boot_guard.py" run_panel "$WS/rl_model_data.json" "$WS/_merged_recover.py" "$HERE/data/cm_400.pkl" "$WS/LTI_REGISTER.md" || exit 1
cd "$WS"
export PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
export PYTHONPATH=/home/claude/rl_workspace/rl_after:/home/claude/rl_vendor
rm -f /tmp/inspect.py
python3 2>/dev/null - << 'PY'
import io,contextlib
g={}
with contextlib.redirect_stdout(io.StringIO()): exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA'];ev=g['ev'];nseas=g['nseas']
def find(nm):
    c=[p for p in MA.data if nm.lower() in p['player'].lower() and MA.GRP.get(p.get('pos'))]; return c[0] if c else None
PANEL=[('Nick Daicos',8069),('Marcus Bontempelli',3664),('Harry Sheezel',8204),('Max Gawn',2518),('Harley Reid',3782),('Josh Ward',1735),('Darcy Moore',207),('Taylor Goad',919),('Josh Smillie',1349),('Will Green',689)]   # v2.9 REFIT candidate (engine 2030e5df store b0c39d78 config 69ead79b944d board 8a66b4ba); all six levers default-ON. RE-PINNED from the ID-migration base (board de4baef9): the 10 named move to the wired all-lever board — L1's _PVC0 swap + V0/RUC rebuild lifts the young sat-out rucks (Goad 818->919, Green 588->689, both +101, same mechanism as knobel 402->505), L2/L3/L4 ripple the rest (Bont 3721->3664, Gawn 2538->2518, Sheezel 8116->8204). == ship_gates B4 board 8a66b4ba (deterministic). ALL-GATES-OFF reproduces the base panel byte-exact: RL_PVCADOPT=0 RL_MSD_POOL_EXCL=0 RL_DIAL14=0 RL_AGE=0 RL_L5_PICKLESS=0 (+ the prior RL_FWDRECAL=0 RL_YOUNG=0 RL_OVPX=0 RL_KPFFIX=0 RL_V7FORM=0 RL_W4_RUC=0 RL_FORMDECL=0 RL_PVCFIT=0) -> n=804 sum=723075, Daicos 8050 Bont 3721 Gawn 2538. Candidate ONLY (no tag/main/bake).
ok=True; print("%-22s%8s%8s"%('player','EV','EXPECT'))
for nm,exp in PANEL:
    p=find(nm); v=ev(p) if p else None; m='' if v==exp else '  <-- MISMATCH'; ok=ok and v==exp
    print("  %-20s%8s%8d%s"%(nm[:20],v,exp,m))
print("\nRESULT:", "PASS 10/10" if ok else "FAIL")
PY
