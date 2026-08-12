#!/bin/bash
# ORDER 20B — the full channel sweep: both controls + one-at-a-time FIX for every channel.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
export PATH=/root/rl_venv312/bin:$PATH
bash "$HERE/run_chan.sh" ALL_HEAD "$SP/chan_ALL_HEAD.json"
bash "$HERE/run_chan.sh" ALL_FIX  "$SP/chan_ALL_FIX.json"
for C in ISO POLE BLEND BAR BASE LVLPAR; do
  bash "$HERE/run_chan.sh" "$C:FIX" "$SP/chan_only_$C.json"
done
# and the complement: everything FIX EXCEPT one channel (leave-one-out), which separates a channel's
# marginal contribution at the FIX baseline from its contribution at the HEAD baseline.
for C in ISO POLE BLEND BAR BASE LVLPAR; do
  SPEC=$(python3 - "$C" <<'PY'
import sys
c=sys.argv[1]; ch=['ISO','POLE','BLEND','BAR','BASE','LVLPAR','OTHER']
print(','.join('%s:%s'%(x,'HEAD' if x==c else 'FIX') for x in ch))
PY
)
  bash "$HERE/run_chan.sh" "$SPEC" "$SP/chan_wo_$C.json"
done
echo "SWEEP DONE"
