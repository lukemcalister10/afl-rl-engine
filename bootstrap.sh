#!/bin/bash
# ============================================================================
# COMPLETE COLD-START BOOTSTRAP — AFL RL engine, snapshot md5 8aed420a
# Recreates the exact layout the engine's absolute paths expect. OFFLINE-SAFE
# (unidecode is VENDORED, no pip/network needed). Idempotent.
# ============================================================================
set -euo pipefail   # SUITE HYGIENE 2026-07-13: +pipefail so a failing `md5sum | cut` on a missing seed
                    # file HALTs instead of printing a wrong md5; +u so an unset var is a red, not empty.
HERE=$(cd "$(dirname "$0")" && pwd)

# When the caller has provisioned the pinned virtual environment, use it for every
# python3 invocation in this bootstrap. This preserves the fail-closed pin check instead
# of accidentally checking the runner's unpinned system Python.
if [ -n "${RL_VENV:-}" ] && [ -x "$RL_VENV/bin/python3" ]; then
  export PATH="$RL_VENV/bin:$PATH"
fi

# ENV PIN (item 392, 2026-07-19): fail-closed check that the running numpy is the PINNED build. The board
# of record 06d8af60 is only reproducible on the pinned numpy wheel (np.interp diverges >=1e-8 across
# DIFFERENT numpy builds -> rank-unsafe board flip; item 391). This is an OFFLINE hash check (no network,
# no install) — it HALTs if the container is on an unpinned numpy. To INSTALL the pin, run bootstrap_env.sh
# at build start (one command, hash-verified). Kept a hard assert here, mirroring Guard 5's store/q97m/v0surf
# asserts: an unverified ENV is a silent cross-container board mover exactly as an unverified store is.
if [ -f "$HERE/bootstrap_env.sh" ]; then
  PIN_BLAS_SHA="05c9f9eb89ee68a4b9d673184fa91c99587e736392c0c2d49180a8aa5303d080"
  python3 - "2.4.4" "$PIN_BLAS_SHA" <<'PY' || { echo "bootstrap HALT: numpy env is NOT the pinned build — run 'bash $HERE/bootstrap_env.sh' to install the pin (see requirements-lock.txt). The board 06d8af60 is not reproducible off the pin (item 391/392)."; exit 1; }
import sys, os, glob, hashlib
want_ver, want_blas = sys.argv[1], sys.argv[2]
import numpy as np
assert np.__version__ == want_ver, f"numpy {np.__version__} != pinned {want_ver}"
libs = glob.glob(os.path.join(os.path.dirname(os.path.dirname(np.__file__)), "numpy.libs", "libscipy_openblas*.so"))
assert libs, "no bundled OpenBLAS in numpy.libs"
got = hashlib.sha256(open(libs[0], "rb").read()).hexdigest()
assert got == want_blas, f"bundled OpenBLAS {got[:16]}.. != pinned {want_blas[:16]}.."
print(f"  ENV PIN        : numpy {np.__version__} + bundled OpenBLAS {got[:8]} (byte-exact to the pin; item 392)")
PY
fi

mkdir -p /home/claude/rl_workspace /home/claude/rl_build /home/claude/rl_vendor

# 1. engine + support modules + harness + pipeline + data files
cp -rf "$HERE/engine/rl_after"          /home/claude/rl_workspace/
cp -rf "$HERE/engine/forward_valuation" /home/claude/rl_workspace/
# gate-integrity (e): the config manifest helper must be importable from the workspace cwd (rl_export.py /
# s4_matrix_M1v7.py call config_manifest.enforce() — a no-op unless RL_CONFIG_MODE=bake|gate). It self-locates
# the repo (RL_REPO / CLAUDE_PROJECT_DIR) for the manifest DATA file, so only the module is seeded here.
cp -f "$HERE/config_manifest.py"        /home/claude/rl_workspace/rl_after/config_manifest.py
# fv-provenance remediation 2026-07-20: rl_export.py imports fv_provenance (always, for the pre-export
# provenance record) and boot_guard (in bake/gate mode, for the fail-closed forward-valuation assertion), so
# both must be importable from the workspace cwd exactly as config_manifest is. Both are repo-anchored (they
# locate the checkout via RL_REPO / CLAUDE_PROJECT_DIR), so only the module is seeded here.
cp -f "$HERE/fv_provenance.py"          /home/claude/rl_workspace/rl_after/fv_provenance.py
cp -f "$HERE/boot_guard.py"             /home/claude/rl_workspace/rl_after/boot_guard.py

# R-REG=R2 (Chapter-3 2026-07-09): seed the owner-authored LTI register — a pinned availability INPUT the
# RL_AVAIL layer consumes at build. Copied into the workspace rl_after (the engine's cwd) so lti_register.py
# reads the ONE committed source; Guard 5 asserts its md5 == the pin (data/expected_boot.json 'register').
cp -f "$HERE/LTI_REGISTER.md"           /home/claude/rl_workspace/rl_after/LTI_REGISTER.md

# 2. absolute-path data deps
cp -f "$HERE/data/cm_400.pkl"                /home/claude/cm_400.pkl
# q97m FROZEN 2026-07-14 (owner ruling): seed the frozen q97 CEILING model beside cm_400.pkl. The engine LOADS
# this (/home/claude/q97m.pkl) — it NEVER fits q97m at build time. Guard 5 asserts data/q97m.pkl == the pin.
cp -f "$HERE/data/q97m.pkl"                  /home/claude/q97m.pkl
cp -f "$HERE/data/rl_build/rl_app_data.json" /home/claude/rl_build/rl_app_data.json

# 3. VENDORED unidecode (offline; no pip). Placed on PYTHONPATH via run_panel/ENV.
cp -rf "$HERE/vendor/unidecode" /home/claude/rl_vendor/unidecode

# 4. the rl_after symlink par_redesign.py inserts on sys.path
ln -sfn /home/claude/rl_workspace/rl_after /home/claude/rl_after

# 5. AUTHORITATIVE STORE = the ONE source of truth engine/rl_after/rl_model_data.json, copied verbatim in step 1.
#    (One-source rewire 2026-07-05: the .pre_stage0 / .stage0 lookalikes are DELETED; the store is no longer
#    reconstituted from a backup here -- it stands alone. Nothing to do in this step.)

M=$(md5sum /home/claude/rl_workspace/rl_after/_merged_recover.py | cut -c1-8)
C=$(md5sum /home/claude/cm_400.pkl | cut -c1-8)
Q=$(md5sum /home/claude/q97m.pkl | cut -c1-8)
S=$(md5sum /home/claude/rl_workspace/rl_after/rl_model_data.json | cut -c1-8)
U=$(python3 -c "import sys; sys.path.insert(0,'/home/claude/rl_vendor'); import unidecode; print('OK')" 2>/dev/null || echo FAIL)
# GUARD 5 (boot-store): the seed above copies from THIS checkout, so the workspace store/head/band MUST now
# equal the pinned expected (data/expected_boot.json). Assert it hard and HALT — a bootstrap that leaves a
# stale store in the workspace is the exact failure this hardening exists to make impossible.
RL_REPO="$HERE" python3 "$HERE/boot_guard.py" bootstrap \
  /home/claude/rl_workspace/rl_after/rl_model_data.json \
  /home/claude/rl_workspace/rl_after/_merged_recover.py \
  /home/claude/cm_400.pkl \
  /home/claude/rl_workspace/rl_after/LTI_REGISTER.md || { echo "bootstrap FAILED: seeded workspace does not match the pinned store/register (see above)"; exit 1; }
# F1 (register item 91): ASSERT the workspace q97m the ENGINE will LOAD (/home/claude/q97m.pkl) == the pin —
# do not merely echo it. boot_guard's (0e) loaded-path block also asserts this on entry; this is the visible,
# fail-closed check in bootstrap's own verify block, matching the store/cm/register assertions in the call above.
QPIN=$(python3 -c "import json,sys; sys.stdout.write(json.load(open('$HERE/data/expected_boot.json'))['q97m'][:8])")
[ "$Q" = "$QPIN" ] || { echo "bootstrap FAILED: workspace q97m /home/claude/q97m.pkl md5 $Q != pinned $QPIN — the engine would LOAD an unverified pickle (F1)"; exit 1; }
# FORWARD-VALUATION PROVENANCE (fv-provenance remediation 2026-07-20): the seed above copies
# engine/forward_valuation -> /home/claude/rl_workspace/forward_valuation. Verify that COPIED tree against the
# pinned FV source-set identity (data/expected_boot.json 'fv') and report its identity — a bootstrap that leaves
# a STALE forward_valuation copy in the workspace (the exact 06d8af60 -> d7a95e8d hole) must HALT loudly, not
# pass. NOTE: the canonical build no longer SELECTS this workspace copy — RL_FV is bound to the CHECKED-OUT
# engine/forward_valuation (JOB 1) and Guard 5 asserts the loaded RL_FV dir == the pin — so this copy can never
# outrank the checkout; this check makes a stale copy a loud halt rather than a silent latent hole.
FVCK=$(python3 - "$HERE" <<'PY'
import sys, os
sys.path.insert(0, sys.argv[1])
import fv_provenance as fp
root = sys.argv[1]
pin = fp.expected_identity(root)
ck  = fp.fv_identity(fp.checkout_fv_dir(root))                                  # the checkout source set
ws  = fp.fv_identity('/home/claude/rl_workspace/forward_valuation')            # the workspace COPY
print("%s|%s|%s" % (pin, ck, ws))
PY
)
FVPIN=${FVCK%%|*}; FVREST=${FVCK#*|}; FVCKID=${FVREST%%|*}; FVWS=${FVREST##*|}
if [ -n "$FVPIN" ] && [ "$FVPIN" != "None" ]; then
  [ "$FVCKID" = "$FVPIN" ] || { echo "bootstrap FAILED: CHECKOUT engine/forward_valuation identity ${FVCKID:0:12} != pinned ${FVPIN:0:12} (data/expected_boot.json 'fv') — a forward-valuation source drifted from the pin (re-pin at a bake)"; exit 1; }
  [ "$FVWS" = "$FVPIN" ] || { echo "bootstrap FAILED: workspace COPY /home/claude/rl_workspace/forward_valuation identity ${FVWS:0:12} != pinned ${FVPIN:0:12} — a STALE forward_valuation copy is in the workspace (re-run bootstrap.sh from the intended checkout; the canonical build binds RL_FV to the checkout, but a stale copy must halt loudly)"; exit 1; }
fi
R=$(md5sum /home/claude/rl_workspace/rl_after/LTI_REGISTER.md | cut -c1-8)
echo "bootstrap OK"
echo "  engine md5     : $M   (candidate: F1/F2 one-source rewire)"
echo "  cm_400 md5     : $C   (expect 34faa865)"
echo "  q97m md5       : $Q   (expect cfdc7321 — FROZEN q97 ceiling; loaded, never fitted; Guard 5 asserted == pinned)"
echo "  store md5      : $S   (single source; no .pre_stage0/.stage0 lookalikes; Guard 5 asserted == pinned)"
echo "  register md5   : $R   (LTI_REGISTER.md — R-REG=R2 pinned availability input; Guard 5 asserted == pinned)"
echo "  fv identity    : ${FVPIN:0:8}   (engine/forward_valuation source set; CHECKOUT + workspace copy asserted == pinned 'fv'; canonical build binds RL_FV to the CHECKOUT)"
echo "  unidecode      : $U   (vendored, offline)"
echo "  ENV (with vendor): PYTHONPATH=/home/claude/rl_workspace/rl_after:/home/claude/rl_vendor ; RL_FV=<repo>/engine/forward_valuation (canonical FV source)"
echo "  next: bash $HERE/run_panel.sh"
