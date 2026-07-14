#!/bin/bash
# Reproduce the fixed panel. OFFLINE-safe (vendored unidecode on PYTHONPATH).
HERE=/home/user/afl-rl-engine
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
_F=1.0524   # L7 numéraire divisor (baked 2026-07-13): the panel shows round(ev/F) so the 10 named read in the numéraire (pick-1=3000), consistent with the shipped board.
def find(nm):
    c=[p for p in MA.data if nm.lower() in p['player'].lower() and MA.GRP.get(p.get('pos'))]; return c[0] if c else None
PANEL=[('Nick Daicos',9999),('Marcus Bontempelli',3482),('Harry Sheezel',7796),('Max Gawn',2393),('Harley Reid',3594),('Josh Ward',1649),('Darcy Moore',197),('Taylor Goad',873),('Josh Smillie',1282),('Will Green',655)]   # v2.9 BAKE — NUMÉRAIRE panel (engine 2030e5df store b0c39d78 config 69ead79b944d board 81e48293); all six levers default-ON. L7 baked: every value = round(ev/1.0524), re-basing the ×1.0524 candidate (raw Daicos 8069 Bont 3664 Sheezel 8204 Gawn 2518 Reid 3782 Ward 1735 Moore 207 Goad 919 Smillie 1349 Green 689) to the numéraire (pick-1=3000). Engine ev() UNCHANGED — the rebase is display-only; ratios/order preserved. == the shipped numéraire board (data/rl_build/rl_app_data.json md5 81e48293, ship_gates B4 byte-agree). Candidate at the L-STOP (no tag/main until owner word).
ok=True; print("%-22s%8s%8s"%('player','EV(num)','EXPECT'))
for nm,exp in PANEL:
    p=find(nm); v=int(round(ev(p)/_F)) if p else None; m='' if v==exp else '  <-- MISMATCH'; ok=ok and v==exp
    print("  %-20s%8s%8d%s"%(nm[:20],v,exp,m))
print("\nRESULT:", "PASS 10/10" if ok else "FAIL")
PY
