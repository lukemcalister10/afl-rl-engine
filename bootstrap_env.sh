#!/bin/bash
# ============================================================================
# ENV-PIN BOOTSTRAP — install + verify the pinned build environment (item 392)
# ----------------------------------------------------------------------------
# ROOT FIX for the cross-build board divergence (item 391): np.interp on the live
# value path diverges >=1e-8 across DIFFERENT numpy WHEELS, amplifying past the
# board flip threshold and reordering the board RANK-UNSAFELY on a minority of
# containers. np.interp is compiled C IN the numpy wheel (numpy/_core,
# compiled_base.c) and does NOT call BLAS; the numpy wheel ALSO bundles its
# OpenBLAS (numpy.libs/), so a hash-pinned numpy wheel pins BOTH in one artifact.
#
# ONE COMMAND, idempotent, offline-safe:
#   - if the pinned numpy (2.4.4 + the exact bundled OpenBLAS) is ALREADY present,
#     it verifies and exits WITHOUT touching the network;
#   - otherwise it hash-installs the pinned wheels from requirements-lock.txt.
# Run this ONCE at build/container start, before bootstrap.sh.
# ============================================================================
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)

# The determinism-critical identity: the exact numpy wheel + its bundled OpenBLAS.
PIN_NUMPY_VER="2.4.4"
PIN_BLAS_SHA="05c9f9eb89ee68a4b9d673184fa91c99587e736392c0c2d49180a8aa5303d080"

verify() {
  python3 - "$PIN_NUMPY_VER" "$PIN_BLAS_SHA" <<'PY'
import sys, os, glob, hashlib
want_ver, want_blas = sys.argv[1], sys.argv[2]
try:
    import numpy as np
except Exception as e:
    print(f"[env-pin] numpy not importable: {e}"); sys.exit(2)
if np.__version__ != want_ver:
    print(f"[env-pin] numpy {np.__version__} != pinned {want_ver}"); sys.exit(2)
libs = glob.glob(os.path.join(os.path.dirname(os.path.dirname(np.__file__)), "numpy.libs", "libscipy_openblas*.so"))
if not libs:
    print("[env-pin] no bundled OpenBLAS in numpy.libs"); sys.exit(2)
got = hashlib.sha256(open(libs[0], "rb").read()).hexdigest()
if got != want_blas:
    print(f"[env-pin] bundled OpenBLAS {got[:16]}.. != pinned {want_blas[:16]}.."); sys.exit(2)
print(f"[env-pin] OK: numpy {np.__version__} + bundled OpenBLAS {got[:16]}.. (byte-exact to the pin)")
PY
}

if verify >/dev/null 2>&1; then
  verify
  echo "[env-pin] already pinned; no install needed (offline-safe no-op)."
  exit 0
fi

echo "[env-pin] installing the pinned environment from requirements-lock.txt (hash-verified, wheel-only)..."
# --require-hashes: every artifact (incl. transitive deps) must match a pinned sha256 or pip HALTS.
# --only-binary=:all:: forbid an sdist build (recompiling numpy would reintroduce the cross-build divergence).
python3 -m pip install --require-hashes --only-binary=:all: -r "$HERE/requirements-lock.txt"

verify || { echo "[env-pin] FAILED: post-install verify did not match the pin"; exit 1; }
echo "[env-pin] pinned environment installed and verified."
