"""acceptance/checks/landing.py — THE LANDER'S OWN SELF-TEST, AS A REGISTERED CHECK (PLAN_v6 2a.3).

REGISTERED RATHER THAN LEFT AS A SCRIPT, and the reason is the brief's own test: it is FAST and it
RUNS NO BUILD. Measured on this box, 2026-08-20: 10.5 seconds wall for the whole self-test — sandbox
worktree creation, a clean control landing, the build-lock refusal, ten fault cases (every step in
LEVER_SEQUENCE broken once), the write-then-abort depth case, the claims negative control and the
packet slot validator. The self-test's own landings use `SelftestBuilder`, which runs no engine at
all; the only real build the lander performs is in a real landing.

An unexercised fallback is fake safety, and an unexercised SELF-TEST is worse — it is fake proof.
Registering it means the lander's abort ladder is re-proved every time the spine runs, rather than
on the day someone remembers to run it.

PROFILE = 'full'. It is deliberately NOT in the per-push host-insensitive profile: it creates a git
worktree, and the per-push lane's floor is file reads and hashes.

IN_TRANSACTION = False — SUPERVISOR RULING, 2026-08-21, after the first A-raw landing attempt timed
this check out at 900s inside its own gates step:

    "The lander's self-test moves OUTSIDE the landing transaction: a check that validates the lander
     by running seventeen practice landings must never run INSIDE a real landing (recursion, not
     coverage). It remains a registered runner check for every push/standalone run; the
     IN-TRANSACTION gate profile excludes it, and the lander runs it ONCE, standalone, immediately
     BEFORE opening the transaction (fresh proof, no recursion). Coverage identical, knot removed."

The line this docstring used to carry — "including inside `land lever`'s own gates step" — was the
knot, written down as if it were a feature. It is struck above rather than quietly deleted.

BLOCKED, NOT FAIL, when the sandbox cannot be built. A tree with no git worktree support (a shallow
CI checkout, an export) can no more run this check than it can run a landing, and reporting that as
a failure of the lander would be a red about the host wearing the lander's name.
"""

import os
import subprocess
import sys

from acceptance import contract as C

_TIMEOUT = 900


def lander_selftest(ctx):
    """the landing library's self-test: every step broken once, every abort proved byte-exact."""
    root = ctx.root
    ev_dir = os.path.join(ctx.evidence_dir or root, 'lander_selftest') if ctx.evidence_dir else None
    argv = [sys.executable, os.path.join(root, 'tools', 'landing', 'cli.py'), 'selftest',
            '--root', root]
    if ev_dir:
        argv += ['--evidence', ev_dir]
    p = subprocess.run(argv, cwd=root, capture_output=True, text=True, timeout=_TIMEOUT,
                       env=dict(os.environ, RL_REPO=root))
    out = (p.stdout or '') + (p.stderr or '')
    ev = C.write_evidence(ctx, 'lander_selftest.txt',
                          '$ %s\n\n%s\n[exit %s]' % (' '.join(argv), out, p.returncode))

    tally = next((l.strip() for l in reversed(out.splitlines())
                  if l.strip().startswith('STEPS BROKEN')), '')
    total = next((l.strip() for l in reversed(out.splitlines())
                  if l.strip().startswith('SELF-TEST:')), '')
    reason = ('%s  |  %s' % (tally, total)).strip(' |') or ('exit %d' % p.returncode)

    if 'cannot create the sandbox worktree' in out:
        return C.Verdict('lander_selftest', C.BLOCKED, ev,
                         'no sandbox could be created on this host (git worktree unavailable) — the '
                         'self-test cannot run here, and that is a host fact, not a lander verdict')
    return C.Verdict('lander_selftest', C.PASS if p.returncode == 0 else C.FAIL, ev, reason)


lander_selftest.HALTS = ()
lander_selftest.PROFILE = 'full'
#: The one check excluded from the in-transaction gate profile. See the ruling in the module
#: docstring: it opens landings of its own, so running it inside a landing is recursion, not coverage.
lander_selftest.IN_TRANSACTION = False
