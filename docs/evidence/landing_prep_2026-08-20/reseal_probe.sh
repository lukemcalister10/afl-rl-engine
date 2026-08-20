#!/bin/bash
# THE BOOK RE-SEAL — PROCEDURE PROBE (landing prep 2026-08-20, order item 3).
#
# THE PROCEDURE OF RECORD, recovered from the two committed re-seal instruments
# (session_2026-07-15/captaincy/reseal_book.py and session_2026-07-17/legd_derivation/reseal_book.py,
# the LEG D ACT-2 act that last moved data/book_stable_seal.json at commit 2e49963) and from
# ship_gates_check.py's B3 gate:
#   1. regenerate the walk-forward matrix with engine/rl_after/s4_matrix_M1v7.py "EXACTLY AS ship_gates
#      B3 does" -- i.e. under RL_CONFIG_MODE=gate;
#   2. assert the matrix's embedded __meta__ engine_head_md5 / store_md5 == the candidate;
#   3. recompute stable_sha256 over the stable-keyed content and RE-COUNT n_players;
#   4. rewrite data/book_stable_seal.json (head_md5, store_md5, n_players, stable_sha256, config).
#
# THE QUESTION THIS PROBE ASKS: under WHICH DIAL LINE is step 1 run for THIS candidate?
#   ARM A -- the candidate's own 18-dial line (the line that defines a05fe951), under gate mode as the
#            procedure specifies.
#   ARM B -- the pinned-manifest line, which is what gate mode actually loads (and what every prior
#            re-seal ran), with NO candidate dials set.
# READ-ONLY: this probe writes NO seal. It only shows what each arm does.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../../.." && pwd)"
SP="${RL_SCRATCH:?}"; rm -rf "$SP"; mkdir -p "$SP"
export PATH="/root/rl_venv312/bin:$PATH"
WS="$SP/seal"
cp -rf "$ROOT/engine/rl_after" "$WS"; cp -rf "$ROOT/engine/forward_valuation" "$SP/forward_valuation"
cp -f "$ROOT/config_manifest.py" "$WS/config_manifest.py"; cp -f "$ROOT/fv_provenance.py" "$WS/fv_provenance.py"
cp -f "$ROOT/boot_guard.py" "$WS/boot_guard.py"; cp -f "$ROOT/LTI_REGISTER.md" "$WS/LTI_REGISTER.md"
chmod -R u+w "$WS"
COMMON=(RL_REPO="$ROOT" RL_FV="$SP/forward_valuation" PYTHONHASHSEED=0
        OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
        PYTHONPATH="$WS:$ROOT/vendor:$ROOT" RL_V0SURF_PKL="$ROOT/data/v0surf.pkl"
        RL_GAMMA=1.0 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22)
CAND=(RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1=0.40 RL_O36_TALL=1 RL_O36_FLOORFIX=1 RL_O36_KAPPA=0.20
      RL_O36_GAMMA=8.0 RL_O36_ETA=0.50 RL_O36_GAMMA_D=14.0 RL_O36_LAMBDA=1.08 RL_O37=1 RL_O38A=1 RL_O38B1=1
      RL_O39_BETASAT=0.105 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=15 RL_O40_RECW=0.47 RL_O40_PGMAT=1
      RL_O41_SDOFF=2.98 RL_O41_CREDIT=1 RL_O41_RESET=1 RL_O41_INJ=1 RL_O41_R3=1 RL_O41_RAMP=1
      RL_O41_BREAK=unwind RL_O41_UNWIND=7 RL_O42=1 RL_O43=1)

echo "=============================================================================="
echo "ARM A — the CANDIDATE dial line, under gate mode (the procedure as written)"
echo "=============================================================================="
env -i "${COMMON[@]}" "${CAND[@]}" S4_MATRIX="$SP/A.json" RL_CONFIG_MODE=gate \
  PATH=/root/rl_venv312/bin:/usr/bin:/bin HOME=/root \
  python3 "$WS/s4_matrix_M1v7.py" 2>&1 | head -30
echo "ARM A matrix produced: $( [ -f "$SP/A.json" ] && echo yes || echo NO )"

echo
echo "=============================================================================="
echo "ARM B — the PINNED-MANIFEST line, no candidate dials (what every prior re-seal ran)"
echo "=============================================================================="
env -i "${COMMON[@]}" S4_MATRIX="$SP/B.json" RL_CONFIG_MODE=gate \
  PATH=/root/rl_venv312/bin:/usr/bin:/bin HOME=/root \
  python3 "$WS/s4_matrix_M1v7.py" 2>&1 | tail -12
echo "ARM B matrix produced: $( [ -f "$SP/B.json" ] && echo yes || echo NO )"
if [ -f "$SP/B.json" ]; then
python3 - "$SP/B.json" "$ROOT" <<'PY'
import json,sys,hashlib
d=json.load(open(sys.argv[1])); meta=d.get('__meta__',{})
by={}
for k,r in d.items():
    if k.startswith('__'): continue
    by[(r.get('player'),r.get('type'),r.get('year'),r.get('pick'))]=r
h=hashlib.sha256()
for k in sorted(by, key=lambda t: json.dumps(t,sort_keys=True)):
    h.update(json.dumps(k,sort_keys=True).encode()); h.update(json.dumps(by[k],sort_keys=True,separators=(',',':')).encode())
seal=json.load(open(sys.argv[2]+'/data/book_stable_seal.json'))
print("  ARM B __meta__ engine_head_md5 : %s" % meta.get('engine_head_md5'))
print("  ARM B __meta__ store_md5       : %s" % meta.get('store_md5'))
print("  ARM B n_players (re-counted)   : %d   (sealed baseline %s)" % (len(by), seal.get('n_players')))
print("  ARM B stable_sha256            : %s" % h.hexdigest())
print("  sealed baseline stable_sha256  : %s" % seal.get('stable_sha256'))
PY
fi
