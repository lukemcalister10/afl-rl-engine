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

`land round` is PACKAGE 2b and is NOT built. It is not stubbed with a friendly message either: the
verb exists, states what it is waiting for (3a, which moves the data pins out of the engine and
changes the transaction 2b must script), and exits non-zero. A verb that pretended to work would be
the first thing a tired seat reached for.

THE ENTRY POINT IS THIN ON PURPOSE. Everything below the argument parsing lives in the shared
library, because 2b attaches there — `tools/landing/steps.py` gains a `ROUND_SEQUENCE` beside
`LEVER_SEQUENCE` and this file gains a verb. Mirrored script pairs drift; the repo's seventeen
emitter forks are the standing evidence.
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
    """
    from tools.landing import selftest as SELF
    ev = tempfile.mkdtemp(prefix='preflight_lander_selftest_')
    print('=' * 102)
    print('PRE-TRANSACTION SELF-TEST — the lander proves its abort ladder BEFORE opening a landing.')
    print('  transcripts: %s  (filed into the landing evidence dir when the transaction closes)' % ev)
    print('=' * 102)
    rc = SELF.main(root=a.root, keep=False, only=None, evidence_dir=ev)
    print('=' * 102)
    if rc != 0:
        raise SystemExit('THE PRE-TRANSACTION SELF-TEST FAILED (exit %s). NO TRANSACTION WAS OPENED '
                         'and the tree is untouched. A lander that cannot prove its own abort ladder '
                         'does not start a landing. Transcripts: %s' % (rc, ev))
    print('PRE-TRANSACTION SELF-TEST PASSED. Opening the transaction.')
    print('=' * 102)
    print('')
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


def cmd_lever(a):
    doc = SP.load(a.spec)
    if doc['act_kind'] != 'lever-landing':
        raise SystemExit('this spec is act_kind %r; `land lever` runs lever-landing specs.'
                         % doc['act_kind'])
    doc['_spec_rel'] = os.path.relpath(os.path.abspath(a.spec), os.path.abspath(a.root))
    builder = TX.BUILDERS[a.builder]() if a.builder in TX.BUILDERS else None
    if builder is None:
        raise SystemExit('unknown builder %r' % a.builder)
    if a.builder != 'real' and not a.selftest:
        raise SystemExit('builder %r is SELF-TEST ONLY. A landing uses the real builder, always.'
                         % a.builder)
    pre_ev = _preflight_selftest(a, doc) if not a.selftest else None
    opts = TX.Options(dry_run=a.dry_run, no_commit=a.no_commit, selftest=a.selftest)
    ctx = TX.Ctx(a.root, doc, opts, builder=builder, fault=a.fault)
    res = TX.run(ctx, ST.LEVER_SEQUENCE)
    _file_preflight_evidence(pre_ev, ctx.evidence_dir)
    if a.report:
        with open(a.report, 'w', encoding='utf-8') as fh:
            json.dump({'ok': res.ok, 'failed_step': res.failed_step,
                       'error': str(res.error) if res.error else None,
                       'timings': [{'step': n, 'seconds': s, 'verdict': v} for n, s, v in res.timings],
                       'abort': res.abort, 'facts': _jsonable(res.facts)}, fh, indent=2, sort_keys=True)
    if a.log:
        with open(a.log, 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(ctx.lines) + '\n')
    return 0 if res.ok else 1


def _jsonable(obj):
    try:
        json.dumps(obj)
        return obj
    except (TypeError, ValueError):
        return json.loads(json.dumps(obj, default=str))


def cmd_round(_a):
    print('`land round` is PACKAGE 2b and is NOT BUILT.')
    print()
    print('It is the SECOND thin entry point over this same library, and the plan puts it after 3a')
    print('for a stated reason: 3a moves the pure-data pins out of the engine, which removes the')
    print('engine-edit/repin step from the very transaction a round lander would script. Building it')
    print('now would mean scripting a transaction that 3a is about to change, and then soaking the')
    print('changed one on the strength of the old one\'s soak.')
    print()
    print('The interim writer for the 3a->2b window is the amended runbook\'s manual path (3a).')
    return 2


def cmd_spec_template(a):
    print(json.dumps(SP.template(a.act_kind), indent=2))
    return 0


def cmd_selftest(a):
    from tools.landing import selftest as SELF
    return SELF.main(root=a.root, keep=a.keep, only=a.only, evidence_dir=a.evidence)


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
    p.add_argument('--report', default=None, help='write a machine-readable result JSON here')
    p.add_argument('--log', default=None, help='write the full transcript here')
    p.add_argument('--print-sequence', action='store_true', help='print the steps and carriers, exit')
    p.set_defaults(fn=cmd_lever)

    p = sub.add_parser('round', help='PACKAGE 2b — not built; says what it waits for')
    p.set_defaults(fn=cmd_round)

    p = sub.add_parser('spec-template', help='print a blank act spec')
    p.add_argument('--act-kind', default='lever-landing')
    p.set_defaults(fn=cmd_spec_template)

    p = sub.add_parser('selftest', help='the sandbox self-test: every step broken once')
    p.add_argument('--root', default=os.environ.get('RL_REPO') or os.getcwd())
    p.add_argument('--keep', action='store_true', help='keep the sandbox for inspection')
    p.add_argument('--only', default=None, help='comma-separated step names to fault-test')
    p.add_argument('--evidence', default=None, help='directory for the self-test transcripts')
    p.set_defaults(fn=cmd_selftest)

    p = sub.add_parser('packet', help='the decision-packet template and its slot validator')
    p.add_argument('--check', default=None)
    p.add_argument('--template', action='store_true')
    p.set_defaults(fn=cmd_packet)

    a = ap.parse_args(argv)
    if not a.verb:
        ap.print_help()
        return 2
    if a.verb == 'lever' and getattr(a, 'print_sequence', False):
        return _print_sequence()
    if a.verb == 'lever' and not a.spec:
        raise SystemExit('`land lever` needs --spec (or --print-sequence)')
    return a.fn(a)


if __name__ == '__main__':
    sys.exit(main())
