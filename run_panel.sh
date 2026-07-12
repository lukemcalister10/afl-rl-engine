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
PANEL=[('Nick Daicos',8050),('Marcus Bontempelli',3721),('Harry Sheezel',8115),('Max Gawn',2538),('Harley Reid',3726),('Josh Ward',1746),('Darcy Moore',209),('Taylor Goad',818),('Josh Smillie',1301),('Will Green',588)]   # BAKED v2.8 (chapter-lever L1 young-GDEF transition credit + pick redenomination; engine 7a07e369 store 04f38dad config 69ead79b944d board 9ecbe0fa). RE-PINNED at the v2.8 bake to the reproduced candidate board (== ship_gates B4 board 9ecbe0fa, deterministic across repeat runs; == SWEEP_DISCOUNT 15% shipped column: Bont 3721 / Gawn 2538). Supersedes the ORPHAN W4+L1c stamp (store e1b4d8bf, never baked) that the chapter-lever candidate left un-updated. Prior baked panels: v2.5 Daicos 7002 Bont 3084 Gawn 2112 (engine efea88e5 store e1b4d8bf); the +5.24% pick redenomination + L1 GDEF credit account for the lift (L1 does not touch these 10 named — GEN_DEF-only). ALL-LEVERS-OFF still reproduces the v2.5 baked panel byte-exact (RL_FWDRECAL=0 RL_YOUNG=0 RL_OVPX=0 RL_KPFFIX=0 RL_V7FORM=0 RL_W4_RUC=0 RL_FORMDECL=0 RL_PVCFIT=0).
ok=True; print("%-22s%8s%8s"%('player','EV','EXPECT'))
for nm,exp in PANEL:
    p=find(nm); v=ev(p) if p else None; m='' if v==exp else '  <-- MISMATCH'; ok=ok and v==exp
    print("  %-20s%8s%8d%s"%(nm[:20],v,exp,m))
print("\nRESULT:", "PASS 10/10" if ok else "FAIL")
PY
