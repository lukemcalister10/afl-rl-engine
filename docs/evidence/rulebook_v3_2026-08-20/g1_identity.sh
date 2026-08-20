#!/usr/bin/env bash
# G1 — THE STANDING FALSIFIER for the v3 RULEBOOK amendment act (RULEBOOK PART 4, P1).
#   bash docs/evidence/rulebook_v3_2026-08-20/g1_identity.sh
#
# THIS ACT IS DOCS + TOOLING. Every value-bearing identity below must be BYTE-IDENTICAL before and
# after; any line that moves is a HALT, not a finding. The governing document itself MOVES by
# design — that is the act — so docs/RULEBOOK.md and the retired twin are printed in a SEPARATE
# "DELIBERATE MOVES" block rather than being silently dropped from the falsifier's list.
set -uo pipefail
cd "${RL_REPO:-$(git rev-parse --show-toplevel)}"
echo "commit            $(git rev-parse HEAD)"
echo "--- VALUE-BEARING (must not move) ---"
for f in engine/rl_after/rl_model_data.json \
         data/rl_build/rl_app_data.json \
         engine/rl_after/_merged_recover.py \
         engine/rl_after/rl_model.py \
         data/model_config.json \
         data/q97m.pkl data/v0surf.pkl data/cm_400.pkl \
         LTI_REGISTER.md \
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
echo "--- DELIBERATE MOVES (this act's whole subject) ---"
for f in docs/RULEBOOK.md tools/rulebook_lint.py; do
  printf '%-44s %s\n' "$f" "$(md5sum "$f" | cut -d' ' -f1)"
done
for f in docs/acceptance_v2_0.json tools/rulebook_twin.py; do
  if [ -f "$f" ]; then printf '%-44s %s\n' "$f" "PRESENT $(md5sum "$f" | cut -d' ' -f1)";
  else printf '%-44s %s\n' "$f" "ABSENT (retired by the v3 amendment)"; fi
done
