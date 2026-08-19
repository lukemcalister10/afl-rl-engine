#!/bin/bash
# ORDER S — falsifier S-F3 driven once per dial line, STRICTLY SEQUENTIAL. The engine can only be
# loaded once per process, so each line gets its own.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PATH=/root/rl_venv312/bin:$PATH
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export PYTHONHASHSEED=0
cd "$HERE"
for T in SB1 SAB1 SW47 SW47A SC20A SM SMA SALL; do
  python3 os_identity.py "$T" 2>&1 | tail -4
done
