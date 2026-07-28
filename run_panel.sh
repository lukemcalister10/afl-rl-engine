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
# fv-provenance remediation 2026-07-20: bind RL_FV EXPLICITLY to the checked-out engine/forward_valuation (JOB
# 1 — no ambient-workspace default) so Guard 5's forward-valuation loaded-path assertion verifies the exact
# tree the engine will import == the pin. RL_REPO also resolves it, but the explicit bind is the intended
# canonical source and makes the selection auditable.
export RL_FV="$HERE/engine/forward_valuation"
RL_REPO="$HERE" RL_FV="$HERE/engine/forward_valuation" python3 "$HERE/boot_guard.py" run_panel "$WS/rl_model_data.json" "$WS/_merged_recover.py" "$HERE/data/cm_400.pkl" "$WS/LTI_REGISTER.md" || exit 1
cd "$WS"
# CONFIG-MANIFEST v2.9 COMPLETION 2026-07-14: run the panel UNDER RL_CONFIG_MODE=gate so the engine takes
# ALL model vars from the pinned manifest (data/model_config.json) rather than code defaults / a hand-copied
# subset. enforce() (called in the heredoc below) clears the ambient model env, rejects any unknown/divergent
# RL_*/PAR_* override, and loads the manifest — its values == the engine defaults, so the panel is byte-identical.
# RL_REPO lets config_manifest find the repo manifest after the `cd "$WS"` above. The pinned exports remain the
# panel's official env; they equal the manifest so the gate-mode reject-scan passes.
export RL_REPO="$HERE" RL_CONFIG_MODE=gate RL_FV="$HERE/engine/forward_valuation"
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
PANEL=[('Nick Daicos',8990),('Marcus Bontempelli',4172),('Harry Sheezel',9655),('Max Gawn',3347),('Harley Reid',3574),('Josh Ward',2721),('Darcy Moore',232),('Taylor Goad',1015),('Josh Smillie',1110),('Will Green',658)]   # ITEM 208 R20 PANEL RE-PIN to the board of record 8a38cca4 (owner word 2026-07-28; round 20 applied AND finalized). balanced/strict 4939d740, store e3aaba77, engine_head 7c452715, config 45b207c0, as_of_round 20. Values = round(ev/1.0524), pick-1=3000, DERIVED from the regenerated board (data/rl_build/rl_app_data.json, md5 8a38cca4) via run_panel.sh — never typed. Round 20 moved 9 of the 10: Daicos 8765->8990, Bontempelli 4318->4172, Sheezel 9631->9655, Gawn 3405->3347, Reid 3563->3574, Ward 2710->2721, Moore 236->232, Goad 1021->1015, Smillie 1125->1110; Will Green 658 unchanged (sat out). SUPERSEDES, truth preserved as history: the ITEM 411 D1 panel pinned to board of record fa172ac1 (balanced/strict 5546f278, store c120cfd5, as_of_round 19) read 8765/4318/9631/3405/3563/2710/236/1021/1125/658; it in turn superseded the ITEM 408 STOP-1 R19 panel pinned to 6f07f7cb (store f37d9716, balanced/strict 1373e824, owner T1 ruling 2026-07-22) reading 8683/4278/9542/3372/3531/2684/234/1011/1233/651, and the balanced-board panel (06d8af60: 8017/3897/7964/3416/3348/2003/257/914/1324/651).
ok=True; print("%-22s%8s%8s"%('player','EV(num)','EXPECT'))
for nm,exp in PANEL:
    p=find(nm); v=int(round(ev(p)/_F)) if p else None; m='' if v==exp else '  <-- MISMATCH'; ok=ok and v==exp
    print("  %-20s%8s%8d%s"%(nm[:20],v,exp,m))
print("\nRESULT:", "PASS 10/10" if ok else "FAIL")
import sys as _sys; _sys.exit(0 if ok else 1)   # exit code IS the verdict (SUITE HYGIENE 2026-07-13)
PY
