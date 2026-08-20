#!/usr/bin/env bash
# G1 — THE STANDING FALSIFIER. Every value-bearing identity, printed. Run before and after; diff.
#   bash docs/evidence/p1_safety_net_2026-08-20/g1_identity.sh
# P1 is pure tooling: any line that moves between two runs is a HALT, not a finding.
set -uo pipefail
cd "${RL_REPO:-$(git rev-parse --show-toplevel)}"
echo "commit            $(git rev-parse HEAD)"
for f in engine/rl_after/rl_model_data.json \
         data/rl_build/rl_app_data.json \
         engine/rl_after/_merged_recover.py \
         engine/rl_after/rl_model.py \
         data/model_config.json \
         data/q97m.pkl data/v0surf.pkl data/cm_400.pkl \
         LTI_REGISTER.md \
         docs/RULEBOOK.md docs/acceptance_v2_0.json \
         ui/data/board_view_working.js ui/data/board_view_public.js; do
  [ -f "$f" ] && printf '%-44s %s\n' "$f" "$(md5sum "$f" | cut -d' ' -f1)"
done
python3 - <<'PY'
import json
b = json.load(open('data/expected_boot.json'))
c = json.load(open('data/release_contract.json'))
s = json.load(open('data/book_stable_seal.json'))
for k in ('store','board','balanced_board_md5','engine_head','rl_model','fv','config','register','as_of_round'):
    print('%-44s %s' % ('expected_boot:'+k, b.get(k)))
print('%-44s %s' % ('release_contract:contract_sha256', c.get('contract_sha256')))
print('%-44s %s' % ('book_seal:stable_sha256', s.get('stable_sha256')))
print('%-44s %s' % ('book_seal:head_md5', s.get('head_md5')))
print('%-44s %s' % ('book_seal:store_md5', s.get('store_md5')))
PY
