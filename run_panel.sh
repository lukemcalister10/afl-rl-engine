#!/bin/bash
# Reproduce the fixed panel. OFFLINE-safe (vendored unidecode on PYTHONPATH).
HERE=$(cd "$(dirname "$0")" && pwd)
WS=/home/claude/rl_workspace/rl_after
# GUARD 5 (boot-store): HALT before the engine loads if the workspace store/head is not the checked-out,
# pinned store. Closes the stale-boot hole the four data guards miss (they validate whichever dir they are
# imported from, so a stale-but-self-consistent workspace passes them). Re-run bootstrap.sh to re-seed.
RL_REPO="$HERE" python3 "$HERE/boot_guard.py" run_panel "$WS/rl_model_data.json" "$WS/_merged_recover.py" || exit 1
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
PANEL=[('Nick Daicos',7626),('Marcus Bontempelli',3524),('Harry Sheezel',7734),('Max Gawn',2413),('Harley Reid',3592),('Josh Ward',1650),('Darcy Moore',198),('Taylor Goad',801),('Josh Smillie',1015),('Will Green',563)]   # CANDIDATE W4 integration 2026-07-06 (multi-lever; store e1b4d8bf UNCHANGED) — NOT BAKED; movers vs the v2.5 baked panel ARE the W4 levers (baked was: Daicos 7002 Bont 3084 Sheezel 7151 Gawn 2112 Reid 3549 Ward 1650 Moore 198 Goad 723 Smillie 974 Green 536); ALL-LEVERS-OFF reproduces the baked panel byte-exact (RL_FWDRECAL=0 RL_YOUNG=0 RL_OVPX=0 RL_KPFFIX=0 RL_V7FORM=0 RL_W4_RUC=0 RL_FORMDECL=0 RL_PVCFIT=0 — verified this session)
ok=True; print("%-22s%8s%8s"%('player','EV','EXPECT'))
for nm,exp in PANEL:
    p=find(nm); v=ev(p) if p else None; m='' if v==exp else '  <-- MISMATCH'; ok=ok and v==exp
    print("  %-20s%8s%8d%s"%(nm[:20],v,exp,m))
print("\nRESULT:", "PASS 10/10" if ok else "FAIL")
PY
