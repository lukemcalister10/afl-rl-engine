#!/bin/bash
# Reproduce the fixed panel. OFFLINE-safe (vendored unidecode on PYTHONPATH).
cd /home/claude/rl_workspace/rl_after
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
PANEL=[('Nick Daicos',7059),('Marcus Bontempelli',3101),('Harry Sheezel',7287),('Max Gawn',2126),('Harley Reid',3523),('Josh Ward',1782),('Darcy Moore',177),('Taylor Goad',545),('Josh Smillie',896),('Will Green',741)]
ok=True; print("%-22s%8s%8s"%('player','EV','EXPECT'))
for nm,exp in PANEL:
    p=find(nm); v=ev(p) if p else None; m='' if v==exp else '  <-- MISMATCH'; ok=ok and v==exp
    print("  %-20s%8s%8d%s"%(nm[:20],v,exp,m))
print("\nRESULT:", "PASS 10/10" if ok else "FAIL")
PY
