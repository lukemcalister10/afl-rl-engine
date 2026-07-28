#!/bin/bash
# Print the panel cross-section, and run Guard 5 on entry. OFFLINE-safe (vendored unidecode on PYTHONPATH).
# The ten-row hand-typed re-pin was REMOVED 2026-07-28 (owner word) — see the note at the PANEL list below.
set -euo pipefail   # SUITE HYGIENE 2026-07-13: exit code is the authority, not a printed string.
                    # pipefail + the explicit sys.exit below make a crash exit non-zero instead of
                    # silently reporting nothing. (SHIP_GATES §HARNESS)
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
# red) — callers that don't want warnings already filter them (`| grep -v Warning`). The heredoc still
# ends with an explicit sys.exit so the EXIT CODE is the authority, but as of 2026-07-28 the only thing
# it can report is a structural break (a named player missing from the board), never a moved value.
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
# THE TEN HAND-TYPED EXPECTED VALUES WERE REMOVED 2026-07-28, on the owner's word.
#
# They compared ten typed numbers against the derived board and exited non-zero on any difference.
# Across R15-R20 the check never once caught a defect: every failure it produced was a board that had
# legitimately moved, and the remedy was always to re-type the ten numbers across four surfaces (this
# line, the expected_boot.json panel block, that block's narrative, and the regenerated UI bundle).
# It blocked every landing and cost a hand re-pin each time — upkeep exceeding return, which is this
# project's stated test for removing a guard rather than keeping it.
#
# KEPT: Guard 5 on entry (line 16), which asserts the store / rl_model / fv identity and HAS fired in
# anger — including mid-job on 2026-07-28, catching a stale workspace store and naming its own remedy.
# The ten rows are still PRINTED because seeing them is useful. There is no typed expectation and no
# 10/10 verdict: this script reports, Guard 5 judges.
PANEL=['Nick Daicos','Marcus Bontempelli','Harry Sheezel','Max Gawn','Harley Reid','Josh Ward','Darcy Moore','Taylor Goad','Josh Smillie','Will Green']
print("%-22s%10s"%('player','EV(num)'))
missing=[]
for nm in PANEL:
    p=find(nm); v=int(round(ev(p)/_F)) if p else None
    if p is None: missing.append(nm)
    print("  %-20s%10s"%(nm[:20],v))
# The only failure left is STRUCTURAL: a named player absent from the board entirely. That is a broken
# board rather than a moved one, and it needs no typed value to detect.
if missing:
    print("\nRESULT: FAIL - not on the board: " + ", ".join(missing))
    import sys as _sys; _sys.exit(1)
print("\nRESULT: panel printed (derived; no hand-typed pin - Guard 5 above is the gate)")
PY
