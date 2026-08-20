"""acceptance/checks/standing.py — the estate's existing standing gates, wrapped in the contract.

These are NOT reimplementations. Each one shells out to the gate the tree already owns, exactly as
CI invokes it, and reads the verdict off its exit code. That matters for two reasons:

  1. The spine must assert the SAME SURFACE CI asserts. A wrapper that reimplements a gate's logic
     is a second implementation that can drift from the first — the hand-mirror hazard the audit
     flags as G4, where `boot_guard._resolve_q97m_load` and `_merged_recover._load_q97m` are
     byte-accurate today with nothing in the tree asserting they stay that way.

  2. Several of these gates are wired into NO workflow at all today (AUDIT_CI.md §2 and gap G9:
     doc_lint.py, verify_restore.sh, sibling_repin.py verify, ingest_inputs.py, preboot_assert.sh,
     ship_gates_check.py). Wrapping rather than rewriting means wiring them costs one registration
     line each, which is the only reason G9 is cheap to close.

Every wrapper captures the gate's full stdout+stderr to the evidence directory, so the one-line
reason in the table always has the raw output standing behind it.
"""

import os
import subprocess

from acceptance import contract as C

_TIMEOUT = 300


def _run(ctx, name, argv, cwd=None):
    """Run a gate and return (returncode, combined_output, evidence_path)."""
    try:
        p = subprocess.run(argv, cwd=cwd or ctx.root, capture_output=True, text=True,
                           timeout=_TIMEOUT)
        out = (p.stdout or '') + (p.stderr or '')
        rc = p.returncode
    except subprocess.TimeoutExpired as e:
        out = 'TIMEOUT after %ds\n%s' % (_TIMEOUT, e.stdout or '')
        rc = 124
    return rc, out, C.write_evidence(ctx, name + '.txt',
                                     '$ %s\n(cwd %s)\n\n%s\n[exit %s]'
                                     % (' '.join(argv), cwd or ctx.root, out, rc))


def _last_meaningful(out, n=1):
    lines = [ln.strip() for ln in (out or '').splitlines() if ln.strip() and set(ln.strip()) != {'='}]
    return ' / '.join(lines[-n:]) if lines else '(no output)'


# ------------------------------------------------------------------------------------------------
def boot_guard_checkout(ctx):
    """Guard 5 checkout legs: store / engine_head / band / register == pinned boot identity.

    All four legs are pointed at the CHECKOUT, never at /home/claude/rl_workspace. That is the
    whole reason this leg is safe to run anywhere: the audit measured `run_panel.sh` correctly
    HALTING on this box because the shared workspace carries the pre-bake engine, and it measured
    `ship_gates_check.py` unable to run at all because line 49 hardcodes that workspace. A spine
    check that depended on a mutable out-of-repo directory would inherit both problems.
    """
    rc, out, ev = _run(ctx, 'boot_guard_checkout', [
        'python3', 'boot_guard.py', 'acceptance-spine',
        os.path.join(ctx.root, 'engine/rl_after/rl_model_data.json'),
        os.path.join(ctx.root, 'engine/rl_after/_merged_recover.py'),
        os.path.join(ctx.root, 'data/cm_400.pkl'),
        os.path.join(ctx.root, 'LTI_REGISTER.md')])
    if rc == 0:
        return C.Verdict('boot_guard_checkout', C.PASS, ev, _last_meaningful(out))
    return C.Verdict('boot_guard_checkout', C.FAIL, ev, _last_meaningful(out))


def config_manifest(ctx):
    """manifest hash == pinned boot config == stored config_sha256."""
    rc, out, ev = _run(ctx, 'config_manifest', ['python3', 'config_manifest.py', 'check'])
    return C.Verdict('config_manifest', C.PASS if rc == 0 else C.FAIL, ev, _last_meaningful(out))


def ruling_config(ctx):
    """RL_PVCFIT=0 default + R3 export bake-guard + RL_LTI_CLOCK=advance, structurally."""
    rc, out, ev = _run(ctx, 'ruling_config', ['python3', 'ruling_config_check.py'])
    return C.Verdict('ruling_config', C.PASS if rc == 0 else C.FAIL, ev, _last_meaningful(out))


def release_contract_seal(ctx):
    """release_contract.py check — the stamped release-state seal."""
    rc, out, ev = _run(ctx, 'release_contract_seal', ['python3', 'release_contract.py', 'check'])
    if rc == 0:
        return C.Verdict('release_contract_seal', C.PASS, ev, _last_meaningful(out))
    # Reached only when the manifest check did NOT halt the four R2 carriers this check reads —
    # i.e. the seal is failing for some reason the widened manifest gate does not already own.
    return C.Verdict('release_contract_seal', C.FAIL, ev,
                     'seal check exit %d for a reason the manifest gate did not halt: %s'
                     % (rc, _last_meaningful(out)))


def store_coherence_six_way(ctx):
    """the original six-carrier store check, retained as its own verdict row."""
    rc, out, ev = _run(ctx, 'store_coherence_six_way',
                       ['python3', 'ui/tools/ownership_store_apply.py', 'verify'])
    return C.Verdict('store_coherence_six_way', C.PASS if rc == 0 else C.FAIL, ev,
                     _last_meaningful(out))


def doc_lint(ctx):
    """doc_lint.py — live/history doc consistency (gap G9: wired nowhere before now)."""
    rc, out, ev = _run(ctx, 'doc_lint', ['python3', 'doc_lint.py'])
    return C.Verdict('doc_lint', C.PASS if rc == 0 else C.FAIL, ev, _last_meaningful(out))
