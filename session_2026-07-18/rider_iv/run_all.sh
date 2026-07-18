#!/bin/bash
# RIDER (iv) — reproduce all artifacts (REPORT-ONLY, read-only, deterministic).
# HALTs (SystemExit 3) on any stamp mismatch. Bootstrap seed 20260718 -> byte-reproducible.
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
cd "$HERE/scripts"
echo "== rider (iv) S1: loader self-test (stamps asserted, HALT-on-mismatch) =="
python3 common_riv.py
echo "== rider (iv) job 1+2: three R candidates + uncertainty on R =="
python3 build_r_candidates.py
echo "== rider (iv) job 3: the view (GROSS vs v-R, ratios, deep-tail premium) =="
python3 build_view.py
echo "RIDER_IV_COMPLETE"
