#!/bin/bash
# ORDER L — the run. Sequential, thread-pinned, read-only. Instruments are DISCLOSED COPIES,
# asserted by md5 inside each reader and never modified by this order.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PATH=/root/rl_venv312/bin:$PATH
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export PYTHONHASHSEED=0
STEP="${1:-all}"
run () { echo; echo "======== $1 ========"; python "$HERE/$1"; echo "exit=$?"; }
case "$STEP" in
  bands) run ol_bands.py ;;
  arms)  run ol_arms.py ;;
  class) run ol_class.py ;;
  pages) run ol_pages.py ;;
  all)   run ol_bands.py; run ol_arms.py; run ol_class.py; run ol_pages.py ;;
  *) echo "unknown step $STEP"; exit 2 ;;
esac
