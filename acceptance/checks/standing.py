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


def rulebook_lint(ctx):
    """tools/rulebook_lint.py — the RULEBOOK's own lint (PLAN_v6 1a; a NEW instrument).

    The one place in the spine where a check consults the STEP half of the ruled-red ledger. It
    carried a ruling for exactly as long as the finding was live: the twin's two unruled laws plus
    its missing banner rode here as RULED-RED (RB1), non-gating, naming the 1b diff that presented
    it to the owner. THE OWNER SIGNED THAT DIFF ON 2026-08-20 ("Okay agree to the laws updated."):
    docs/acceptance_v2_0.json is removed, the lint is 0 FAIL, RB1's probe expired and RB1 is retired
    — so this row is a plain PASS and consults the ledger only if the lint ever reds again. The
    ledger lookup stays because that is the row's contract, not because anything is being carried.
    """
    from acceptance import known_red
    rc, out, ev = _run(ctx, 'rulebook_lint', ['python3', 'tools/rulebook_lint.py', ctx.root])
    if rc == 0:
        return C.Verdict('rulebook_lint', C.PASS, ev, _last_meaningful(out))
    entry = known_red.covering_step_entry('acceptance::rulebook_lint')
    fails = [l.strip() for l in out.splitlines() if l.strip().startswith('FAIL')]
    if entry:
        return C.Verdict('rulebook_lint', C.RULED_RED, ev,
                         'ruling %s (presented: %s) — %d finding(s), first: %s'
                         % (entry.get('id'), (entry.get('presented') or '')[:60], len(fails),
                            (fails[0] if fails else '')[:80]))
    return C.Verdict('rulebook_lint', C.FAIL, ev,
                     '%d rulebook finding(s), first: %s' % (len(fails),
                                                            (fails[0] if fails else _last_meaningful(out))[:100]))


# ------------------------------------------------------------------------------------------------
def register_form(ctx):
    """The 3b register act's standing falsifiers (2026-08-21), both existing tools, sub-second:
    tools/seat/pen.py verify (frozen-file seal md5, entry well-formedness, version contiguity,
    LATEST/index freshness) + tools/incident_index.py check (the generated incident index is
    current — the READERS_3B defect-1 gap: a generated surface with no gate drifts silently).
    Registered under the owner's same-day quick-and-easy bar; no build, no engine import."""
    rc1, out1, _ = _run(ctx, 'register_form_pen', ['python3', 'tools/seat/pen.py', 'verify'])
    rc2, out2, ev = _run(ctx, 'register_form_index', ['python3', 'tools/incident_index.py', 'check'])
    status = C.PASS if rc1 == 0 and rc2 == 0 else C.FAIL
    return C.Verdict('register_form', status, ev,
                     '%s / %s' % (_last_meaningful(out1), _last_meaningful(out2)))


# ------------------------------------------------------------------------------------ profile tags
# PROFILE says where a check can honestly run (runner.py --profile).
#
#   host-insensitive  reads the CHECKOUT and nothing else. Safe on a bare GitHub runner, which is
#                     what PLAN_v6 1a arms on every push.
#   host-sensitive    needs the seeded out-of-repo layout (/home/claude/...). boot_guard_checkout
#                     is the one here: its checkout legs are host-insensitive, but Guard 5's
#                     fitted-artifact LOADED-PATH leg resolves /home/claude/cm_<trees>.pkl and
#                     reports "band LOAD-PATH unresolved" where bootstrap.sh has not run. ci-guards
#                     runs it AFTER bootstrap.sh, which is the right place for it.
#   heavy             minutes of engine. Never per-push.
boot_guard_checkout.PROFILE = 'host-sensitive'
config_manifest.PROFILE = 'host-insensitive'
ruling_config.PROFILE = 'host-insensitive'
release_contract_seal.PROFILE = 'host-insensitive'
store_coherence_six_way.PROFILE = 'host-insensitive'
doc_lint.PROFILE = 'host-insensitive'
rulebook_lint.PROFILE = 'host-insensitive'
register_form.PROFILE = 'host-insensitive'


def inbox_manifest(ctx):
    """tools/inbox_manifest.py check — the owner-inputs provenance archive is current (1d).

    Registered rather than left as a command somebody remembers to run, because a provenance
    manifest that has stopped describing the inbox is worse than none: it reads as a record and is
    a guess. The check fails on a stale generated file, on an archived input with no canonical copy,
    and on an archived input with no declared purpose.
    """
    rc, out, ev = _run(ctx, 'inbox_manifest', ['python3', 'tools/inbox_manifest.py', 'check'])
    return C.Verdict('inbox_manifest', C.PASS if rc == 0 else C.FAIL, ev, _last_meaningful(out))


inbox_manifest.HALTS = ()
inbox_manifest.PROFILE = 'host-insensitive'


def state_file(ctx):
    """docs/STATE.md IS a regeneration of this tree (PLAN_v6 3c freshness gate, process law P6).

    THE CHEAPEST HONEST FORM, and the one the owner's same-day quick-and-easy bar asked for: shell
    out to the generator's own `check` verb, which regenerates the file from the carriers and
    compares byte-for-byte. No second implementation of the render — a wrapper that re-derived the
    content would be a hand-mirror of the writer, which is the G4 hazard this estate has already
    paid for once.

    WHY THIS ROW EXISTS AT ALL. `docs/CURRENT_STATE.md` had an authority banner, a named writer and
    no gate, and sat 156 register versions stale (process law P6's own incident). The banner on
    `docs/STATE.md` is worth exactly what this row's verdict says it is worth: a generated surface
    with no gate drifts silently, which is the same defect the 3b act closed for the incident index.

    Sub-second, no build, no engine import — it reads five JSON carriers, two doc headers and runs
    the rulebook lint the state file quotes.
    """
    rc, out, ev = _run(ctx, 'state_file', ['python3', '-m', 'tools.landing.state', 'check'])
    return C.Verdict('state_file', C.PASS if rc == 0 else C.FAIL, ev, _last_meaningful(out, 2))


state_file.HALTS = ()
state_file.PROFILE = 'host-insensitive'
