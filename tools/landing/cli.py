#!/usr/bin/env python3
"""tools/landing/cli.py — `land lever`. ONE command, the whole landing transaction.

    tools/land lever --spec <act_spec.json> [--root DIR] [--dry-run] [--no-commit]
    tools/land lever --print-sequence           what the ten steps are, and who writes what
    tools/land spec-template > my_act.json      a blank spec with every slot present
    tools/land selftest [--keep]                the sandbox self-test (PLAN_v6 2a.3)
    tools/land packet --check <PACKET.md>       the decision-packet slot validator (2a.2)

`land lever` RUNS THE SELF-TEST ITSELF, ONCE, STANDALONE, BEFORE it opens the transaction, and
refuses to open one if it fails. The gates step's acceptance run uses `--profile in-transaction`,
which is the full profile minus that same check. See `_preflight_selftest` for the ruling.

    tools/land round --spec <act_spec.json> [--root DIR] [--dry-run] [--no-commit]
    tools/land round --print-sequence           the fourteen steps, and which seven are SHARED

    tools/land edit --spec <edit_spec.json> [--dry-run]
    tools/land edit --print-sequence            the twelve steps, and which eleven are SHARED

`land edit` IS THE THIRD THIN ENTRY POINT (THE EDIT VERB, directive 2026-08-24) — the general
out-of-round store-edit lane the owner ruled into existence after `land lever` refused an owner-worded
one-field store edit three times, each refusal byte-exact and correct (register v836). It is
`cmd_lever` again with the sequence and the carrier set looked up from the act kind, and its one new
step, `store_edit`, applies a SURGICAL byte replacement inside the named row's span, in the WORK DIR,
between `preflight` and `build_proofs` — so the lineage entry's source and destination STRADDLE the
edit and the chain stays continuous with no flip commit. `--dry-run` is the user-friendly half: it
predicts in a scratch worktree and writes nothing (tools/landing/preview.py).

`land round` IS THE SECOND THIN ENTRY POINT (PLAN_v6 2b), landed 2026-08-21 on the same library.
`cmd_round` is `cmd_lever` with the sequence and the carrier set looked up from the act kind: seven
of its fourteen steps ARE the lever lander's own functions, and the driver, the abort ladder, the
build lock, the explicit-path commits, the per-step timing, the day-0 rule and the fv-provenance
exclusion are one implementation serving both verbs. Mirrored script pairs drift; the repo's
seventeen emitter forks are the standing evidence, and this file is the shape of the alternative.

WHAT 2b ADDS, and each is a step the R23 hand-walk performed by hand: the sheet/data commit in
PACKAGE 3a's form (`land round` is `data/sheet_pins.json`'s SOLE WRITER), the owner's score file and
its bindings, the read-only catch-up preflight, the ARMED catch-up (inside which `staged_apply` runs
ADVANCE-REPIN), the disclosed generator-side sync, the day-0 reference regeneration — which lives
HERE AND NOWHERE ELSE, because the ruling is "regenerate at the advance, never mid-round" — and the
owner's movers page.
"""

import argparse
import json
import os
import shutil
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
_LANDER_REPO = os.path.dirname(os.path.dirname(_HERE))
if _LANDER_REPO not in sys.path:
    sys.path.insert(0, _LANDER_REPO)

from tools.landing import carriers as CA                                       # noqa: E402
from tools.landing import spec as SP                                           # noqa: E402
from tools.landing import steps as ST                                          # noqa: E402
from tools.landing import txn as TX                                            # noqa: E402


def _print_sequence():
    print('THE LEVER-LANDING SEQUENCE — tools/landing/steps.py LEVER_SEQUENCE')
    print('=' * 102)
    for i, (name, title, fn) in enumerate(ST.LEVER_SEQUENCE):
        print('  %d. %-14s %s' % (i, name, title))
        doc = (fn.__doc__ or '').strip().splitlines()
        if doc:
            print('     %s' % doc[0])
    print()
    print('THE CARRIER SET — every path a lever landing may write, and its writer of record')
    print('=' * 102)
    for c in CA.LEVER_CARRIERS:
        print('  %-62s %s' % (c.pattern + ('  (glob)' if c.is_glob else ''), c.writer))
    return 0


def _preflight_selftest(a, doc):
    """THE LANDER PROVES ITSELF BEFORE IT OPENS A TRANSACTION — never inside one.

    SUPERVISOR RULING, 2026-08-21:

        "The lander's self-test moves OUTSIDE the landing transaction: a check that validates the
         lander by running seventeen practice landings must never run INSIDE a real landing
         (recursion, not coverage). It remains a registered runner check for every push/standalone
         run; the IN-TRANSACTION gate profile excludes it, and the lander runs it ONCE, standalone,
         immediately BEFORE opening the transaction (fresh proof, no recursion). Coverage identical,
         knot removed."

    This is the "runs it ONCE, standalone, immediately BEFORE" half; `acceptance.runner --profile
    in-transaction` (which the gates step now uses) is the "excludes it" half. The proof is FRESH —
    it is this run's self-test, on this tree, minutes old — which is strictly more than the old
    arrangement got, because the in-transaction copy never once completed.

    FAIL = NO TRANSACTION OPENED. Not a warning, not a note in the report: a lander that cannot prove
    its own abort ladder does not get to start a landing that may need it.

    It is skipped for `--selftest` runs and ONLY for those: those ARE the self-test's practice
    landings, and running the self-test from inside them is the recursion this ruling removes, with
    no bottom to it.

    ITS TRANSCRIPTS ARE WRITTEN OUTSIDE THE REPO and copied into the landing's evidence dir only
    AFTER the transaction closes. Writing them straight into `docs/evidence/...` would leave
    untracked files in the tree, and step 0 asserts a CLEAN tree — the lander's own proof would red
    the landing it was proving. Returns the temp dir for `cmd_lever` to file.

    IT RUNS ON A COHERENT TREE, WHICH IS NOT ALWAYS `HEAD` — supervisor ruling, 2026-08-21, quoted in
    full in `selftest.main`. The spec's optional `coherent_base` slot names the commit the sandbox is
    cut from; a dial-flip act sets it to the commit immediately before its flip, where pins == source.
    Omit it and the sandbox is cut from HEAD, which is right for every act that leaves the tree
    coherent. THE SLOT CHANGES NO PREDICTION AND NO IDENTITY: it selects the tree the LANDER is
    exercised against, and the lander under test is the working copy either way.
    """
    from tools.landing import selftest as SELF
    from tools.landing import proofstash as PS
    ev = tempfile.mkdtemp(prefix='preflight_lander_selftest_')
    base = doc.get('coherent_base') or None

    # SHRINK S13/S7 (owner word 2026-08-28): the selftest proves THE LANDER against a spec on a
    # base. Byte-identical lander + spec + base => the standing proof stands — re-proving the
    # identical abort ladder cost ~11 min on every retry of the combined-build landing (~10 runs
    # in one night, one informative). The marker lives outside the repo, records the pass it
    # stands on, and ANY byte moving in tools/landing/ or the spec (or LANDING_SELFTEST=force)
    # runs the full 43 legs again.
    _here = os.path.dirname(os.path.abspath(__file__))
    _fp = PS.lander_fingerprint(_here, a.spec, base)
    if os.environ.get('LANDING_SELFTEST') != 'force' and PS.selftest_passed(_fp):
        print('=' * 102)
        print('PRE-TRANSACTION SELF-TEST — STANDING PROOF (S13/S7): lander + spec + base are '
              'byte-identical to an already-passed run (fingerprint %s).' % _fp[:12])
        print('  Re-run it any time with LANDING_SELFTEST=force; any byte moving in '
              'tools/landing/ or the spec re-runs it automatically.')
        print('=' * 102)
        return None
    print('=' * 102)
    print('PRE-TRANSACTION SELF-TEST — the lander proves its abort ladder BEFORE opening a landing.')
    print('  transcripts: %s  (filed into the landing evidence dir when the transaction closes)' % ev)
    if base:
        print('  base       : %s  (the act declares this tree mid-act; the sandbox is cut from the '
              'last coherent base)' % base)
    print('=' * 102)
    rc = SELF.main(root=a.root, keep=False, only=None, evidence_dir=ev, base=base)
    print('=' * 102)
    if rc != 0:
        raise SystemExit('THE PRE-TRANSACTION SELF-TEST FAILED (exit %s). NO TRANSACTION WAS OPENED '
                         'and the tree is untouched. A lander that cannot prove its own abort ladder '
                         'does not start a landing. Transcripts: %s' % (rc, ev))
    print('PRE-TRANSACTION SELF-TEST PASSED. Opening the transaction.')
    print('=' * 102)
    print('')
    PS.record_selftest_pass(_fp, {'spec': os.path.abspath(a.spec), 'base': base or 'HEAD',
                                  'transcripts': ev})
    return ev


def _file_preflight_evidence(src, dest_dir):
    """Move the pre-transaction self-test's transcripts into the landing's evidence dir."""
    if not src or not os.path.isdir(src):
        return
    dest = os.path.join(dest_dir, 'preflight_lander_selftest')
    shutil.rmtree(dest, ignore_errors=True)
    try:
        shutil.copytree(src, dest)
        shutil.rmtree(src, ignore_errors=True)
        print('pre-transaction self-test transcripts filed: %s' % dest)
    except OSError as e:
        print('could not file the pre-transaction self-test transcripts (%s); they remain at %s'
              % (e, src))


def _run_cheap_preflight(a, doc):
    """The sub-second battery, before the selftest (minutes) and the first build (more minutes).
    Skipped under --selftest for the same reason _preflight_selftest is: the sandbox's fault runs
    exercise the transaction, and every one of these checks re-runs at gate time anyway.

    Returns the results list; THE RECORD IS FILED AFTER THE TRANSACTION, never before it (shrink
    review S4, 2026-08-28). The launch-time write into the TRACKED evidence dir dirtied the very
    tree step 0 then refused — twice as timing jitter, then every launch as the lock-holder line —
    and each launch cost a ritual commit to clear its own paperwork. Verdicts stay on stdout at
    launch (the M2 measure-then-quote surface); the file rides the transaction's own commit window,
    the same pattern the selftest transcripts have always used (_file_preflight_evidence)."""
    if a.selftest:
        return None
    from tools.landing import preflight as PF
    ok, results = PF.run_preflight(a.root, a.spec)
    if not ok:
        raise SystemExit('PREFLIGHT FAILED. No lock taken, no sandbox cut, no build run, the tree '
                         'untouched — every failure above was knowable in seconds, which is the '
                         'point (ORDER 45 ledger, register v858).')
    return results


def _file_cheap_preflight(results, evidence_dir):
    """File the launch preflight record into the act's evidence dir AFTER the transaction closed
    (committed or restored either way — the write can no longer trip step 0's clean-tree law)."""
    if not results:
        return
    from tools.landing import preflight as PF
    PF.file_evidence(results, evidence_dir)


def cmd_lever(a):
    doc = SP.load(a.spec)
    if doc['act_kind'] != 'lever-landing':
        raise SystemExit('this spec is act_kind %r; `land lever` runs lever-landing specs.'
                         % doc['act_kind'])
    pf_results = _run_cheap_preflight(a, doc)
    doc['_spec_rel'] = os.path.relpath(os.path.abspath(a.spec), os.path.abspath(a.root))
    builder = TX.BUILDERS[a.builder]() if a.builder in TX.BUILDERS else None
    if builder is None:
        raise SystemExit('unknown builder %r' % a.builder)
    if a.builder != 'real' and not a.selftest:
        raise SystemExit('builder %r is SELF-TEST ONLY. A landing uses the real builder, always.'
                         % a.builder)
    pre_ev = _preflight_selftest(a, doc) if not a.selftest else None
    opts = TX.Options(dry_run=a.dry_run, no_commit=a.no_commit, selftest=a.selftest)
    ctx = TX.Ctx(a.root, doc, opts, builder=builder, fault=a.fault, keep_work=a.keep_work)
    res = TX.run(ctx, ST.LEVER_SEQUENCE)
    _file_preflight_evidence(pre_ev, ctx.evidence_dir)
    _file_cheap_preflight(pf_results, ctx.evidence_dir)
    _write_reports(a, ctx, res)
    return 0 if res.ok else 1


def _write_reports(a, ctx, res):
    """The machine-readable result and the full transcript. ONE writer, both verbs."""
    if a.report:
        with open(a.report, 'w', encoding='utf-8') as fh:
            json.dump({'ok': res.ok, 'failed_step': res.failed_step,
                       'error': str(res.error) if res.error else None,
                       'timings': [{'step': n, 'seconds': s, 'verdict': v} for n, s, v in res.timings],
                       'abort': res.abort, 'commits': list(ctx.commits_made),
                       'facts': _jsonable(res.facts)}, fh, indent=2, sort_keys=True)
    if a.log:
        with open(a.log, 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(ctx.lines) + '\n')


def _jsonable(obj):
    try:
        json.dumps(obj)
        return obj
    except (TypeError, ValueError):
        return json.loads(json.dumps(obj, default=str))


def cmd_round(a):
    """`land round` — the SECOND thin entry point over the same library (PLAN_v6 2b).

    It is the same twelve lines as `cmd_lever` with two words changed, and that is the deliverable:
    the sequence and the carrier set are looked up from the act kind, everything else — the
    pre-transaction self-test, the options, the driver, the abort ladder, the report and the log —
    is literally the lever lander's. Two commands must never become two divergent scripts (S7).
    """
    doc = SP.load(a.spec)
    if doc['act_kind'] != 'round-advance':
        raise SystemExit('this spec is act_kind %r; `land round` runs round-advance specs.'
                         % doc['act_kind'])
    pf_results = _run_cheap_preflight(a, doc)
    doc['_spec_rel'] = os.path.relpath(os.path.abspath(a.spec), os.path.abspath(a.root))
    builder = TX.BUILDERS[a.builder]() if a.builder in TX.BUILDERS else None
    if builder is None:
        raise SystemExit('unknown builder %r' % a.builder)
    if a.builder != 'real' and not a.selftest:
        raise SystemExit('builder %r is SELF-TEST ONLY. A landing uses the real builder, always.'
                         % a.builder)
    pre_ev = _preflight_selftest(a, doc) if not a.selftest else None
    opts = TX.Options(dry_run=a.dry_run, no_commit=a.no_commit, selftest=a.selftest)
    ctx = TX.Ctx(a.root, doc, opts, builder=builder, fault=a.fault, keep_work=a.keep_work,
                 carriers=CA.ROUND_CARRIERS)
    res = TX.run(ctx, ST.ROUND_SEQUENCE)
    _file_preflight_evidence(pre_ev, ctx.evidence_dir)
    _file_cheap_preflight(pf_results, ctx.evidence_dir)
    _write_reports(a, ctx, res)
    return 0 if res.ok else 1


def cmd_edit(a):
    """`land edit` — THE THIRD THIN ENTRY POINT over the same library (directive 2026-08-24).

    It is `cmd_lever` with the sequence and the carrier set looked up from the act kind, exactly as
    `cmd_round` is — ELEVEN of its twelve steps are the lever lander's own functions, and the driver,
    the abort ladder, the build lock, the explicit-path commits, the per-step timing and the
    pre-transaction self-test are one implementation serving three verbs. What the edit verb adds is
    the one step a store edit genuinely has and the other two genuinely do not.

    `--dry-run` DOES NOT WALK THE SEQUENCE, and that is deliberate rather than a shortcut. A board
    that reflects an edit can only be built from a tree where the edit exists, so a dry run that
    "called no writer" would build the PRE-edit store and predict the board the tree already has.
    `tools/landing/preview.py` applies the edit in a scratch git worktree, builds there, prints the
    owner's one screen, and proves it moved no live carrier. See its header for the whole loop.
    """
    doc = SP.load(a.spec)
    if doc['act_kind'] != 'store-edit':
        raise SystemExit('this spec is act_kind %r; `land edit` runs store-edit specs.'
                         % doc['act_kind'])
    pf_results = _run_cheap_preflight(a, doc)
    doc['_spec_rel'] = os.path.relpath(os.path.abspath(a.spec), os.path.abspath(a.root))
    if a.dry_run:
        from tools.landing import preview as PV
        return PV.dry_run(a.root, doc, keep=a.keep_work, report=a.report, log=a.log)
    builder = TX.BUILDERS[a.builder]() if a.builder in TX.BUILDERS else None
    if builder is None:
        raise SystemExit('unknown builder %r' % a.builder)
    if a.builder != 'real' and not a.selftest:
        raise SystemExit('builder %r is SELF-TEST ONLY. A landing uses the real builder, always.'
                         % a.builder)
    pre_ev = _preflight_selftest(a, doc) if not a.selftest else None
    opts = TX.Options(dry_run=False, no_commit=a.no_commit, selftest=a.selftest)
    ctx = TX.Ctx(a.root, doc, opts, builder=builder, fault=a.fault, keep_work=a.keep_work,
                 carriers=CA.EDIT_CARRIERS)
    res = TX.run(ctx, ST.EDIT_SEQUENCE)
    _file_preflight_evidence(pre_ev, ctx.evidence_dir)
    _file_cheap_preflight(pf_results, ctx.evidence_dir)
    _write_reports(a, ctx, res)
    return 0 if res.ok else 1


def _print_edit_sequence():
    print('THE STORE-EDIT SEQUENCE — tools/landing/steps.py EDIT_SEQUENCE')
    print('=' * 102)
    shared = {n for n, _t, _f in ST.LEVER_SEQUENCE}
    for i, (name, title, fn) in enumerate(ST.EDIT_SEQUENCE):
        print('  %2d. %-14s %-56s %s' % (i, name, title,
                                         'SHARED with land lever' if name in shared
                                         else 'NEW in the edit verb'))
        doc = (fn.__doc__ or '').strip().splitlines()
        if doc:
            print('      %s' % doc[0])
    print()
    print('  %d of %d steps are the lever lander\'s OWN functions, registered again rather than '
          'copied.' % (sum(1 for n, _t, _f in ST.EDIT_SEQUENCE if n in shared),
                       len(ST.EDIT_SEQUENCE)))
    print()
    print('THE CARRIER SET — every path a store edit may write, and its writer of record')
    print('=' * 102)
    for c in CA.EDIT_CARRIERS:
        print('  %-62s %s' % (c.pattern + ('  (glob)' if c.is_glob else ''), c.writer))
    print()
    print('  %d carriers: the LEVER set exactly, named rather than re-enumerated — the store has been '
          'in it\n  since the first draft, captured so an abort could prove it byte-exact.'
          % len(CA.EDIT_CARRIERS))
    return 0


def _print_round_sequence():
    print('THE ROUND-ADVANCE SEQUENCE — tools/landing/steps.py ROUND_SEQUENCE')
    print('=' * 102)
    shared = {n for n, _t, _f in ST.LEVER_SEQUENCE}
    for i, (name, title, fn) in enumerate(ST.ROUND_SEQUENCE):
        print('  %2d. %-18s %-56s %s' % (i, name, title,
                                         'SHARED with land lever' if name in shared else 'NEW in 2b'))
        doc = (fn.__doc__ or '').strip().splitlines()
        if doc:
            print('      %s' % doc[0])
    print()
    print('  %d of %d steps are the lever lander\'s OWN functions, registered again rather than '
          'copied.' % (sum(1 for n, _t, _f in ST.ROUND_SEQUENCE if n in shared), len(ST.ROUND_SEQUENCE)))
    print()
    print('THE CARRIER SET — every path a round advance may write, and its writer of record')
    print('=' * 102)
    for c in CA.ROUND_CARRIERS:
        print('  %-62s %s' % (c.pattern + ('  (glob)' if c.is_glob else ''), c.writer))
    print()
    print('  %d carriers: %d shared with the lever landing, %d added by 2b.'
          % (len(CA.ROUND_CARRIERS), len(CA.LEVER_CARRIERS), len(CA.ROUND_EXTRA_CARRIERS)))
    return 0


def cmd_preflight(a):
    from tools.landing import preflight as PF
    ok, _results = PF.run_preflight(a.root, a.spec)
    return 0 if ok else 1


def cmd_spec_template(a):
    print(json.dumps(SP.template(a.act_kind), indent=2))
    return 0


def cmd_selftest(a):
    from tools.landing import selftest as SELF
    return SELF.main(root=a.root, keep=a.keep, only=a.only, evidence_dir=a.evidence, base=a.base)


def cmd_packet(a):
    from tools.landing import packet as PK
    if a.template:
        print(PK.TEMPLATE)
        return 0
    if not a.check:
        print('nothing to do: pass --check <PACKET.md> or --template')
        return 2
    problems = PK.validate_file(a.check)
    print(PK.render_report(a.check, problems))
    return 0 if not problems else 1


def main(argv=None):
    ap = argparse.ArgumentParser(prog='land', description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest='verb')

    p = sub.add_parser('lever', help='run the full lever-landing transaction')
    p.add_argument('--spec', help='the act spec (tools/land spec-template writes a blank one)')
    p.add_argument('--root', default=os.environ.get('RL_REPO') or os.getcwd())
    p.add_argument('--dry-run', action='store_true', help='compute and assert; call no writer')
    p.add_argument('--no-commit', action='store_true', help='write, but do not make the commit')
    p.add_argument('--builder', default='real', help='real | selftest | selftest-moved (self-test only)')
    p.add_argument('--fault', default=None, help='SELF-TEST ONLY: break one step (see txn.FAULTS)')
    p.add_argument('--selftest', action='store_true', help='permit fault injection / fake builders')
    p.add_argument('--keep-work', action='store_true',
                   help='keep the work dir (restore point + intermediate boards) after the '
                        'transaction closes; the default discards it once the restore point has '
                        'done its job. An unproved abort keeps it regardless.')
    p.add_argument('--report', default=None, help='write a machine-readable result JSON here')
    p.add_argument('--log', default=None, help='write the full transcript here')
    p.add_argument('--print-sequence', action='store_true', help='print the steps and carriers, exit')
    p.set_defaults(fn=cmd_lever)

    p = sub.add_parser('round', help='run the full round-advance transaction (PLAN_v6 2b)')
    p.add_argument('--spec', help='the act spec (tools/land spec-template --act-kind round-advance)')
    p.add_argument('--root', default=os.environ.get('RL_REPO') or os.getcwd())
    p.add_argument('--dry-run', action='store_true', help='compute and assert; arm nothing, call no '
                                                          'writer, apply no round')
    p.add_argument('--no-commit', action='store_true', help='write, but do not make the commit')
    p.add_argument('--builder', default='real', help='real | selftest | selftest-moved (self-test only)')
    p.add_argument('--fault', default=None, help='SELF-TEST ONLY: break one step (see txn.FAULTS)')
    p.add_argument('--selftest', action='store_true', help='permit fault injection / fake builders')
    p.add_argument('--keep-work', action='store_true', help='keep the work dir after the close')
    p.add_argument('--report', default=None, help='write a machine-readable result JSON here')
    p.add_argument('--log', default=None, help='write the full transcript here')
    p.add_argument('--print-sequence', action='store_true', help='print the steps and carriers, exit')
    p.set_defaults(fn=cmd_round)

    p = sub.add_parser('edit', help='run the store-edit transaction (THE EDIT VERB, 2026-08-24)')
    p.add_argument('--spec', help='the act spec (tools/land spec-template --act-kind store-edit)')
    p.add_argument('--root', default=os.environ.get('RL_REPO') or os.getcwd())
    p.add_argument('--dry-run', action='store_true',
                   help='THE OWNER\'S PREDICTION: apply the edit in a SCRATCH git worktree, build '
                        'there, print the one-screen summary (store and board old -> new, every '
                        'mover with values, the identities that move) and write NOTHING to any '
                        'carrier. Read it, get the owner\'s word, put it in the spec, and run the '
                        'same command without this flag.')
    p.add_argument('--no-commit', action='store_true', help='write, but do not make the commit')
    p.add_argument('--builder', default='real', help='real | selftest | selftest-moved (self-test only)')
    p.add_argument('--fault', default=None, help='SELF-TEST ONLY: break one step (see txn.FAULTS)')
    p.add_argument('--selftest', action='store_true', help='permit fault injection / fake builders')
    p.add_argument('--keep-work', action='store_true', help='keep the work dir / scratch worktree')
    p.add_argument('--report', default=None, help='write a machine-readable result JSON here')
    p.add_argument('--log', default=None, help='write the full transcript here')
    p.add_argument('--print-sequence', action='store_true', help='print the steps and carriers, exit')
    p.set_defaults(fn=cmd_edit)

    p = sub.add_parser('preflight', help='the sub-second pre-launch battery, standalone (it also '
                                         'runs automatically at the top of lever/round/edit)')
    p.add_argument('--spec', required=True)
    p.add_argument('--root', default=os.environ.get('RL_REPO') or os.getcwd())
    p.set_defaults(fn=cmd_preflight)

    p = sub.add_parser('spec-template', help='print a blank act spec')
    p.add_argument('--act-kind', default='lever-landing')
    p.set_defaults(fn=cmd_spec_template)

    p = sub.add_parser('selftest', help='the sandbox self-test: every step broken once')
    p.add_argument('--root', default=os.environ.get('RL_REPO') or os.getcwd())
    p.add_argument('--keep', action='store_true', help='keep the sandbox for inspection')
    p.add_argument('--only', default=None, help='comma-separated step names to fault-test')
    p.add_argument('--evidence', default=None, help='directory for the self-test transcripts')
    p.add_argument('--base', default=None,
                   help='the commit the sandbox worktree is cut from (default HEAD). Set it to the '
                        'LAST COHERENT BASE when the tree is mid-act — for a dial-flip act, the '
                        'commit immediately before the flip. See the ruling in selftest.main.')
    p.set_defaults(fn=cmd_selftest)

    p = sub.add_parser('packet', help='the decision-packet template and its slot validator')
    p.add_argument('--check', default=None)
    p.add_argument('--template', action='store_true')
    p.set_defaults(fn=cmd_packet)

    a = ap.parse_args(argv)
    if not a.verb:
        ap.print_help()
        return 2
    if a.verb in ('lever', 'round', 'edit') and getattr(a, 'print_sequence', False):
        return {'lever': _print_sequence, 'round': _print_round_sequence,
                'edit': _print_edit_sequence}[a.verb]()
    if a.verb in ('lever', 'round', 'edit') and not a.spec:
        raise SystemExit('`land %s` needs --spec (or --print-sequence)' % a.verb)
    return a.fn(a)


if __name__ == '__main__':
    sys.exit(main())
