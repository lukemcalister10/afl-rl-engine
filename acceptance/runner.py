"""acceptance/runner.py — executes the registered checks, aggregates, prints ONE table.

    python3 -m acceptance.runner [--root DIR] [--evidence DIR] [--json PATH] [--only NAME,...]

Exit codes:
    0   no FAIL. (PASS / BLOCKED / RULED-RED rows do not red a run — see contract.py.)
    1   at least one FAIL.
    2   the registry itself is mis-ordered (a check reads a carrier that a LATER check can halt).

ONE TABLE. Not one table per check, not a table plus a summary plus a per-suite breakdown. The
estate's problem was never too little output — `final-integration.yml` prints thousands of lines and
its tail re-runs its own head. The problem was that nothing anywhere said, in one place, what state
the tree is in and why. That is this file's entire job.
"""

import argparse
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from acceptance import contract as C                                          # noqa: E402


DEFAULT_ROOT = _ROOT


class RunContext(object):
    """Everything a check is allowed to know: where the tree is, where to write evidence."""

    __slots__ = ('root', 'evidence_dir', 'halted')

    def __init__(self, root, evidence_dir):
        self.root = os.path.abspath(root)
        self.evidence_dir = evidence_dir
        self.halted = {}          # carrier -> (check name, reason) — filled in as the run proceeds


def validate_registry(checks=None):
    """Refuse to run a registry whose order cannot honour the blocked-once law.

    The law only works if every check that can halt a carrier runs BEFORE the checks that read it.
    If that is violated the downstream check runs first, fails on its own, and the estate gets two
    reds for one cause — precisely the thing the contract exists to prevent. Rather than let that
    happen quietly at 3am, the runner refuses the registry and says which pair is wrong.

    A carrier is "haltable by" a check if the check declares it in `halts` (set by the check module
    at registration time via the HALTS attribute on the function). Checks that read a carrier no
    check can halt are fine — that carrier simply never blocks anything.
    """
    checks = checks if checks is not None else C.registry()
    halter_index = {}
    for i, c in enumerate(checks):
        for carrier in getattr(c.fn, 'HALTS', ()) or ():
            halter_index.setdefault(carrier, i)
    problems = []
    for i, c in enumerate(checks):
        for carrier in c.reads:
            j = halter_index.get(carrier)
            if j is not None and j > i:
                problems.append(
                    "  %-34s reads carrier %-38s which %r can halt, but %r runs LATER (%d > %d)"
                    % (c.name, carrier, checks[j].name, checks[j].name, j, i))
    return problems


def run(ctx, checks=None):
    """Execute the checks in registration order, honouring the blocked-once law.

    Returns the list of Verdicts, one per registered check, in order. Every registered check gets
    exactly one row — a check that did not run gets a BLOCKED row, never a missing row. A silently
    absent check is how a suite quietly stops watching, which is the `RL_M3_FE` failure mode the
    audit found in `_V0SURF_GATES`.
    """
    checks = checks if checks is not None else C.registry()
    rows = []
    for c in checks:
        blocking = [carrier for carrier in c.reads if carrier in ctx.halted]
        if blocking:
            carrier = blocking[0]
            by, why = ctx.halted[carrier]
            rows.append(C.Verdict(
                c.name, C.BLOCKED,
                evidence='',
                reason='carrier %s halted by %s — %s' % (carrier, by, why)))
            continue
        v = C.guard(c.name, c.fn, ctx)
        for carrier in v.halted_carriers:
            ctx.halted.setdefault(carrier, (v.name, v.reason))
        rows.append(v)
    return rows


# ------------------------------------------------------------------------------------- the table
def _fit(s, n):
    s = str(s)
    return s if len(s) <= n else s[:n - 1] + '…'


def render(rows, ctx, root, profile='full'):
    """The one table, plus the carrier ledger and the aggregate line. Returns the text."""
    counts = {v: 0 for v in C.VERDICTS}
    for r in rows:
        counts[r.verdict] += 1

    name_w = max([len(r.name) for r in rows] + [12])
    reason_w = max(40, 118 - name_w - 12)

    out = []
    out.append('=' * (name_w + reason_w + 16))
    out.append('THE VERDICT SPINE — acceptance/runner.py')
    out.append('  tree: %s' % root)
    out.append('  evidence: %s' % (ctx.evidence_dir or '(none)'))
    out.append('  profile : %s%s' % (profile,
                                     '   (per-push floor: checkout-only checks)'
                                     if profile == 'host-insensitive' else '   (every registered check)'))
    out.append('=' * (name_w + reason_w + 16))
    out.append('%-*s  %-10s  %s' % (name_w, 'CHECK', 'VERDICT', 'REASON'))
    out.append('%-*s  %-10s  %s' % (name_w, '-' * name_w, '-' * 10, '-' * reason_w))
    for r in rows:
        out.append('%-*s  %-10s  %s' % (name_w, r.name, r.verdict, _fit(r.reason, reason_w)))
    out.append('%-*s  %-10s  %s' % (name_w, '-' * name_w, '-' * 10, '-' * reason_w))

    if ctx.halted:
        out.append('')
        out.append('HALTED CARRIERS — each named ONCE; every BLOCKED row above points at one of these:')
        for carrier, (by, why) in ctx.halted.items():
            out.append('  %-40s halted by %s' % (carrier, by))
            out.append('  %-40s %s' % ('', _fit(why, 100)))

    ev = [r for r in rows if r.evidence]
    if ev:
        out.append('')
        out.append('EVIDENCE:')
        for r in ev:
            out.append('  %-*s  %s' % (name_w, r.name, r.evidence))

    out.append('')
    out.append('AGGREGATE  %d checks  |  PASS %d  FAIL %d  BLOCKED %d  RULED-RED %d'
               % (len(rows), counts[C.PASS], counts[C.FAIL], counts[C.BLOCKED], counts[C.RULED_RED]))
    fails = [r.name for r in rows if r.verdict in C.GATING]
    if fails:
        out.append('VERDICT    RED — %d gating failure(s): %s' % (len(fails), ', '.join(fails)))
    else:
        out.append('VERDICT    GREEN — no gating failures.')
        if counts[C.BLOCKED] or counts[C.RULED_RED]:
            out.append('           (%d blocked, %d ruled-red — non-gating by contract; the causes are '
                       'named above and are not this run\'s to clear.)'
                       % (counts[C.BLOCKED], counts[C.RULED_RED]))
    return '\n'.join(out)


def exit_code(rows):
    """Non-zero on any FAIL. Nothing else reds a run."""
    return 1 if any(r.verdict in C.GATING for r in rows) else 0


# ---------------------------------------------------------------------------------------- driver
def main(argv=None):
    ap = argparse.ArgumentParser(description='Run the acceptance verdict spine.')
    ap.add_argument('--root', default=os.environ.get('RL_REPO') or DEFAULT_ROOT,
                    help='repo root to assert against (default: this checkout)')
    ap.add_argument('--evidence', default=None, help='directory to write per-check raw output into')
    ap.add_argument('--json', dest='json_path', default=None, help='also write the rows as JSON here')
    ap.add_argument('--only', default=None, help='comma-separated check names to run (others BLOCKED-out)')
    ap.add_argument('--profile', default='full', choices=('full', 'host-insensitive'),
                    help='"host-insensitive" runs ONLY the checks that read the checkout and nothing '
                         'else — the per-push CI floor (PLAN_v6 1a). "full" (default) runs everything, '
                         'including the heavy determinism leg.')
    a = ap.parse_args(argv)

    import acceptance.checks                                                  # noqa: F401
    checks = C.registry()

    problems = validate_registry(checks)
    if problems:
        print('REGISTRY MIS-ORDERED — the blocked-once law cannot hold with this order:')
        print('\n'.join(problems))
        return 2

    if a.profile == 'host-insensitive':
        # A FILTER, NOT A FAKE VERDICT. Checks the profile excludes are not run and not reported —
        # they are not given a PASS they did not earn, and not given a BLOCKED that would claim a
        # halted carrier that does not exist. The table's own header says which profile produced it,
        # so a reader can never mistake a per-push run for a full one.
        checks = [c for c in checks
                  if getattr(c.fn, 'PROFILE', 'host-insensitive') == 'host-insensitive']

    if a.only:
        want = {s.strip() for s in a.only.split(',') if s.strip()}
        unknown = want - {c.name for c in C.registry()}
        if unknown:
            print('unknown check name(s): %s' % ', '.join(sorted(unknown)))
            return 2
        checks = [c for c in checks if c.name in want]

    ctx = RunContext(a.root, a.evidence)
    if ctx.evidence_dir:
        os.makedirs(ctx.evidence_dir, exist_ok=True)
    rows = run(ctx, checks)
    text = render(rows, ctx, ctx.root, profile=a.profile)
    print(text)

    if a.json_path:
        with open(a.json_path, 'w', encoding='utf-8') as fh:
            json.dump({'root': ctx.root,
                       'rows': [r.as_dict() for r in rows],
                       'halted_carriers': {k: {'by': v[0], 'reason': v[1]}
                                           for k, v in ctx.halted.items()}},
                      fh, indent=2, sort_keys=True)
        print('\nJSON: %s' % a.json_path)

    return exit_code(rows)


if __name__ == '__main__':
    sys.exit(main())
