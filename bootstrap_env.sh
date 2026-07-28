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

# The pinned interpreter, written ONCE. The interpreter names searched below and the CPython ABI tag
# the installed numpy wheel must carry are both derived from this — neither is typed a second time.
PIN_PY_XY="3.12"
PIN_PY_FULL="3.12.3"

# ---- THE INTERPRETER IS PART OF THE PIN ------------------------------------------------------
# requirements-lock.txt pins the cp312 numpy wheel by sha256, so only Python 3.12 can satisfy it.
# Bare `python3` is whatever the container happens to default to. On a container defaulting to 3.11
# with 3.12 installed, pip resolves the cp311 wheel and dies with a HASH MISMATCH whose own text
# says "someone may have tampered with them" — a supply-chain alarm for what is really just the
# wrong interpreter. That misdirection has cost two seats.
#
# So discover 3.12 BY NAME, exactly as setup_env.sh and .github/workflows/live-scoring.yml already
# do, and halt readably when it is absent. Halting is the intended outcome, not a regression: a
# container without 3.12 cannot install this lock, and should say so in one line rather than
# half-working and failing later somewhere unrelated.
# A candidate must RUN and report 3.12 — being present and marked executable is not enough. A name
# that resolves but cannot execute (masked, broken symlink, wrong arch) would otherwise be selected
# here and then die further down as a bare "Permission denied", which is precisely the confusing
# failure this block exists to remove.
PY=""
for c in "python$PIN_PY_XY" "/usr/bin/python$PIN_PY_XY" "/usr/local/bin/python$PIN_PY_XY"; do
  command -v "$c" >/dev/null 2>&1 || continue
  cv=$("$c" -c 'import sys; print("%d.%d" % sys.version_info[:2])' 2>/dev/null) || continue
  [ "$cv" = "$PIN_PY_XY" ] || continue
  PY="$c"; break
done
if [ -z "$PY" ]; then
  cat >&2 <<MSG

■ HALT — no python$PIN_PY_XY found (checked PATH, /usr/bin, /usr/local/bin).

  requirements-lock.txt pins the cp${PIN_PY_XY/./} numpy wheel by sha256. No other interpreter can
  satisfy that lock: pip would resolve a different wheel and fail as an apparent tampered-artifact
  error.

  Fix: install Python $PIN_PY_XY (the pin is $PIN_PY_FULL) and re-run this script.

  Do NOT relax the pin to make this pass. A different numpy wheel changes np.interp on the live
  value path and silently reorders the board.
MSG
  exit 1
fi
PYV=$("$PY" -c 'import sys; print("%d.%d.%d" % sys.version_info[:3])')
[ "$PYV" = "$PIN_PY_FULL" ] || echo "[env-pin] WARN: $PY is $PYV, pin is $PIN_PY_FULL — values policy applies if drift appears"
echo "[env-pin] interpreter: $PY ($PYV)"

verify() {
  "$PY" - "$PIN_NUMPY_VER" "$PIN_BLAS_SHA" "$PIN_PY_XY" <<'PY'
import sys, os, glob, hashlib
import importlib.metadata as md
want_ver, want_blas, want_xy = sys.argv[1], sys.argv[2], sys.argv[3]

# ---- THE BUILD TAG IS THE ONLY THING THAT DISTINGUISHES THE TWO WHEELS ------------------------
# The version string and the bundled OpenBLAS hash below are BYTE-IDENTICAL across the cp311 and
# cp312 builds of numpy 2.4.4 — measured, not assumed:
#     cp311  version 2.4.4  OpenBLAS 05c9f9eb89ee68a4..  Tag cp311-cp311-manylinux_2_27_x86_64
#     cp312  version 2.4.4  OpenBLAS 05c9f9eb89ee68a4..  Tag cp312-cp312-manylinux_2_27_x86_64
# So a guard built only on those two CANNOT SEE the wheel swap it exists to detect: run against a
# cp311 install it printed "OK ... byte-exact to the pin" and exited 0. The dist-info WHEEL file
# records the build tag, pip wrote it at install time, and it is the one value that differs — so
# read it. Nothing here is hand-maintained: the expected tag is derived from want_xy, which is the
# interpreter pin declared once at the top of this script.
#
# Both halves are needed. The tag alone is vacuous, because a 3.11 interpreter with a cp311 numpy
# is self-consistent and would pass; the interpreter assertion is what makes the pair decisive.
run_xy = "%d.%d" % sys.version_info[:2]
if run_xy != want_xy:
    print(f"[env-pin] interpreter is Python {run_xy}, pin is {want_xy} "
          f"(a {run_xy} environment cannot hold the pinned wheel)"); sys.exit(2)
want_tag = "cp" + want_xy.replace(".", "")

try:
    import numpy as np
except Exception as e:
    print(f"[env-pin] numpy not importable: {e}"); sys.exit(2)
if np.__version__ != want_ver:
    print(f"[env-pin] numpy {np.__version__} != pinned {want_ver}"); sys.exit(2)

try:
    wheel = md.distribution("numpy").read_text("WHEEL")
except Exception as e:
    print(f"[env-pin] numpy dist-info unreadable: {e}"); sys.exit(2)
if not wheel:
    print("[env-pin] numpy dist-info carries no WHEEL metadata — build tag unverifiable"); sys.exit(2)
tags = [l.split(":", 1)[1].strip() for l in wheel.splitlines() if l.startswith("Tag:")]
if not tags:
    print("[env-pin] numpy WHEEL metadata carries no Tag: line — build tag unverifiable"); sys.exit(2)
bad = [t for t in tags if t.split("-")[:2] != [want_tag, want_tag]]
if bad:
    print(f"[env-pin] numpy is the {bad[0].split('-')[0]} build, pin is {want_tag} "
          f"(tags: {', '.join(tags)})"); sys.exit(2)

libs = glob.glob(os.path.join(os.path.dirname(os.path.dirname(np.__file__)), "numpy.libs", "libscipy_openblas*.so"))
if not libs:
    print("[env-pin] no bundled OpenBLAS in numpy.libs"); sys.exit(2)
got = hashlib.sha256(open(libs[0], "rb").read()).hexdigest()
if got != want_blas:
    print(f"[env-pin] bundled OpenBLAS {got[:16]}.. != pinned {want_blas[:16]}.."); sys.exit(2)
print(f"[env-pin] OK: numpy {np.__version__} {want_tag} build + bundled OpenBLAS {got[:16]}.. "
      f"(byte-exact to the pin)")
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
"$PY" -m pip install --require-hashes --only-binary=:all: -r "$HERE/requirements-lock.txt"

verify || { echo "[env-pin] FAILED: post-install verify did not match the pin"; exit 1; }
echo "[env-pin] pinned environment installed and verified."
