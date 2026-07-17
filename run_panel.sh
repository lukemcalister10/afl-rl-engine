#!/bin/bash
# Reproduce the fixed panel. OFFLINE-safe (vendored unidecode on PYTHONPATH).
set -euo pipefail   # SUITE HYGIENE 2026-07-13: the panel is a gate; its exit code must be the authority,
                    # not a printed string. pipefail + the panel's own sys.exit below make a crash or a
                    # computed FAIL exit non-zero instead of silently reporting nothing. (SHIP_GATES §HARNESS)
HERE=$(cd "$(dirname "$0")" && pwd)
WS=/home/claude/rl_workspace/rl_after
# GUARD 5 (boot-store): HALT before the engine loads if the workspace store/head is not the checked-out,
# pinned store. Closes the stale-boot hole the four data guards miss (they validate whichever dir they are
# imported from, so a stale-but-self-consistent workspace passes them). Re-run bootstrap.sh to re-seed.
RL_REPO="$HERE" python3 "$HERE/boot_guard.py" run_panel "$WS/rl_model_data.json" "$WS/_merged_recover.py" "$HERE/data/cm_400.pkl" "$WS/LTI_REGISTER.md" || exit 1
cd "$WS"
# CONFIG-MANIFEST v2.9 COMPLETION 2026-07-14: run the panel UNDER RL_CONFIG_MODE=gate so the engine takes
# ALL model vars from the pinned manifest (data/model_config.json) rather than code defaults / a hand-copied
# subset. enforce() (called in the heredoc below) clears the ambient model env, rejects any unknown/divergent
# RL_*/PAR_* override, and loads the manifest — its values == the engine defaults, so the panel is byte-identical.
# RL_REPO lets config_manifest find the repo manifest after the `cd "$WS"` above. The pinned exports remain the
# panel's official env; they equal the manifest so the gate-mode reject-scan passes.
export RL_REPO="$HERE" RL_CONFIG_MODE=gate
export PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
export PYTHONPATH=/home/claude/rl_workspace/rl_after:/home/claude/rl_vendor
rm -f /tmp/inspect.py
# SUITE HYGIENE 2026-07-13: stderr NO LONGER discarded (a hidden traceback is silence, and silence is a
# red) — callers that don't want warnings already filter them (`| grep -v Warning`). The heredoc ends with
# an explicit sys.exit so the EXIT CODE, not the printed "PASS/FAIL" string, is the panel's authority.
python3 - << 'PY'
import io,contextlib,config_manifest
# CONFIG-MANIFEST v2.9 COMPLETION: gate mode — clear ambient model env + load data/model_config.json BEFORE
# the engine reads os.environ, so all 47 pinned model vars (incl. the v2.9 levers) come from the manifest.
# NO-OP outside bake/gate mode (dev-shell unaffected). This is mode wiring only; the panel maths are untouched.
config_manifest.enforce()
g={}
with contextlib.redirect_stdout(io.StringIO()): exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA'];ev=g['ev'];nseas=g['nseas']
_F=1.0524   # L7 numéraire divisor (baked 2026-07-13): the panel shows round(ev/F) so the 10 named read in the numéraire (pick-1=3000), consistent with the shipped board.
def find(nm):
    c=[p for p in MA.data if nm.lower() in p['player'].lower() and MA.GRP.get(p.get('pos'))]; return c[0] if c else None
PANEL=[('Nick Daicos',8017),('Marcus Bontempelli',3897),('Harry Sheezel',7964),('Max Gawn',3416),('Harley Reid',3348),('Josh Ward',2003),('Darcy Moore',257),('Taylor Goad',914),('Josh Smillie',1324),('Will Green',651)]   # LEG D ACT-2 RE-PIN (2026-07-17): board 9829d01a -> 270a2c5f (RL_PVC2 composed-pathway ev-channel swap, default ON). ONLY Will Green moves 649->651 (+2): pk16 RUC, his prior-cap reads the lifted deep-tail draftval; the other 9 HOLD (ev-channel only). RL_PVC2=0 reproduces 649 (board 9829d01a byte-exact). Prior pin below stands for RL_PVC2=0. RE-PINNED to the LEG C flex + §1b candidate board ee70335a (engine head a0635745, store 0efdc5d6, rl_model d0e28978). RL_FLEX default ON; RL_FLEX=0 reproduces the Leg-B board f2f077b2 byte-exact. Supersedes the stale Leg-A pin (board 8d90c9ac, values 8140/3625/8006/3138/3468/2004/257/917/1285/657). Values = round(ev/1.0524) and equal the shipped board 'v' for all 10 (cross-checked against data/rl_build/rl_app_data.json). The iso pick-tax fades on the v2.10 evidence weight + the ISO table is monotonized: the ruck Gawn rises 2574->3138 (his pk33 penalty dissolves at proven evidence), Sheezel/Reid/Ward drift a touch as pick premiums fade; Daicos ->8140. RL_ISOFADE=0 reproduces the v2.10 CAPTAINCY BAKE board 790136a3 byte-exact (proven full-board md5). Supersedes the v2.10 captaincy pins.
ok=True; print("%-22s%8s%8s"%('player','EV(num)','EXPECT'))
for nm,exp in PANEL:
    p=find(nm); v=int(round(ev(p)/_F)) if p else None; m='' if v==exp else '  <-- MISMATCH'; ok=ok and v==exp
    print("  %-20s%8s%8d%s"%(nm[:20],v,exp,m))
print("\nRESULT:", "PASS 10/10" if ok else "FAIL")
import sys as _sys; _sys.exit(0 if ok else 1)   # exit code IS the verdict (SUITE HYGIENE 2026-07-13)
PY
