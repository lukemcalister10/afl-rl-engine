"""acceptance/contract.py — THE VERDICT CONTRACT.

The whole spine is four fields. A check does not get to invent its own reporting shape:

    name          the check's stable identifier (never a line number, never a count)
    verdict       exactly one of PASS / FAIL / BLOCKED / RULED-RED
    evidence      a path a reader can open — the raw output the verdict was read off
    reason        ONE line, in English, naming the thing that is wrong

--------------------------------------------------------------------------------------------------
THE DESIGN PRINCIPLE (register v787, adopted from AUDIT_CI.md §5 "One thing M1a should NOT do"):

    "The verdict spine's job is to make that legible — one halted carrier, named once, with
     everything downstream of it reported as *blocked* rather than as thirty independent failures.
     That legibility is the deliverable, not a green wall."

That sentence is law here, and it is enforced structurally, not by convention. The audit measured
~40 failing assertions across the estate of which **R1 alone accounted for about 30** — one
un-appended lineage entry, behind an owner ruling that was already presented. An estate that reports
that as thirty reds is not informing anyone; it is burying the one fact that matters under
twenty-nine restatements of it.

So: checks declare the CARRIERS they read (`depends_on`). A check that discovers a carrier is
halted says so once, by returning that carrier in `halted_carriers`. Every later check that reads
that carrier is then NOT RUN AT ALL — it is recorded BLOCKED, naming the carrier and the check that
halted it. The downstream check never gets the chance to produce its own duplicate red.

--------------------------------------------------------------------------------------------------
THE FOUR VERDICTS, and what each one means to the exit code:

  PASS       The assertion held.                                     exit contribution: none
  FAIL       The assertion did not hold, and nothing upstream        exit contribution: NON-ZERO
             excuses it. This is the only verdict that reds a run.
  BLOCKED    Not run. A carrier this check reads is halted, and      exit contribution: none
             the halt is already reported once, upstream. Reporting
             it again would be the thirty-failures antipattern.
  RULED-RED  Measured red, KNOWN, and already before the owner or    exit contribution: none
             supervisor as a presented ruling. Carries the ruling
             id in `reason`. Non-gating by construction: a seat must
             never be blocked from shipping by a red that only the
             owner can clear, and must never silently "fix" it.

RULED-RED is the instrument the audit asked for in §5/RETIRE: "If declared known-reds must be
carried, carry them as a machine-readable list keyed by assertion name" — not as a hand-typed count
in a workflow comment, which is the instrument class the panel 10/10 was retired for.

--------------------------------------------------------------------------------------------------
THE RULE EVERY NEW ASSERTION IS WRITTEN TO (AUDIT_CI.md §5/EXTEND, from fv-provenance.yml):

    "Assert the *relationship*, never this month's number."

fv-provenance is the only workflow in the estate a board move or a dial flip cannot red, because on
2026-07-28 it swapped `board_md5 == <pin>` for `_built(r)`. Every other red the audit measured was a
hand-typed expectation outrun by a legitimate move: the panel 10/10, the movers "exactly two
known-reds", the R14 fixture's config pin, BOARD_MD5_GOOD. Checks registered here MUST NOT carry
hex literals of this month's identities. Compute the truth from the artifact and assert the
carriers agree with it.
"""

import os
import time
import traceback

# ---------------------------------------------------------------------------------- the verdicts
PASS = 'PASS'
FAIL = 'FAIL'
BLOCKED = 'BLOCKED'
RULED_RED = 'RULED-RED'

VERDICTS = (PASS, FAIL, BLOCKED, RULED_RED)

#: Only FAIL reds a run. See the table in the module docstring for why.
GATING = (FAIL,)


class ContractError(RuntimeError):
    """A check violated the verdict contract itself (bad verdict value, missing field, ...).

    This is deliberately NOT a FAIL verdict: a check that cannot report correctly cannot be
    trusted to report at all, and the runner surfaces it as a FAIL of the check with the contract
    violation as its reason.
    """


class Verdict(object):
    """One row of the one table. Four fields, plus the carriers this row halts."""

    __slots__ = ('name', 'verdict', 'evidence', 'reason', 'halted_carriers', 'seconds')

    def __init__(self, name, verdict, evidence='', reason='', halted_carriers=(), seconds=0.0):
        if verdict not in VERDICTS:
            raise ContractError(
                "verdict %r is not one of %s (check %r)" % (verdict, '/'.join(VERDICTS), name))
        reason = (reason or '').strip().replace('\n', ' ')
        if not reason:
            raise ContractError("check %r returned no reason; every verdict names its one line" % name)
        self.name = name
        self.verdict = verdict
        self.evidence = evidence or ''
        self.reason = reason
        self.halted_carriers = tuple(halted_carriers or ())
        self.seconds = seconds
        if self.halted_carriers and verdict == PASS:
            raise ContractError(
                "check %r returned PASS but declared halted carriers %s — a passing check halts nothing"
                % (name, list(self.halted_carriers)))

    def as_dict(self):
        return {'name': self.name, 'verdict': self.verdict, 'evidence': self.evidence,
                'reason': self.reason, 'halted_carriers': list(self.halted_carriers),
                'seconds': round(self.seconds, 3)}

    def __repr__(self):
        return '<Verdict %s %s: %s>' % (self.name, self.verdict, self.reason)


# ------------------------------------------------------------------------------ check registration
class Check(object):
    """A registered check.

    fn(ctx) -> Verdict.  `ctx` is a RunContext (see runner.py): it carries the repo root and the
    evidence directory, and nothing else — a check must not reach for global state.

    `reads` names the CARRIERS this check depends on. A carrier is a named upstream fact, not a
    file: 'release_contract.identities' is a carrier; 'data/release_contract.json' is a file that
    happens to hold three of them. Carriers are what get halted, and what BLOCKED rows name.
    """

    __slots__ = ('name', 'fn', 'reads', 'doc')

    def __init__(self, name, fn, reads=(), doc=''):
        self.name = name
        self.fn = fn
        self.reads = tuple(reads or ())
        self.doc = doc or (fn.__doc__ or '').strip().split('\n')[0]


_REGISTRY = []


def register(name, fn, reads=(), doc=''):
    """Register a check. Registration ORDER IS EXECUTION ORDER — and that is load-bearing.

    A check that can halt a carrier must be registered BEFORE every check that reads it, or the
    downstream check runs first and produces the duplicate red the contract exists to prevent.
    `runner.validate_registry()` asserts exactly that and refuses to run an order that violates it.
    """
    if any(c.name == name for c in _REGISTRY):
        raise ContractError("check %r is already registered" % name)
    c = Check(name, fn, reads, doc)
    _REGISTRY.append(c)
    return c


def registry():
    """The registered checks, in execution order."""
    return list(_REGISTRY)


def clear_registry():
    """Empty the registry. For the self-test only — production callers import `checks` and run."""
    del _REGISTRY[:]


# --------------------------------------------------------------------------------------- helpers
def write_evidence(ctx, basename, text):
    """Write a check's raw output and return the path that goes in the `evidence` field.

    Every verdict must be readable back off a file. A verdict whose evidence is 'trust me' is the
    instrument class this whole order exists to retire.
    """
    if ctx is None or not getattr(ctx, 'evidence_dir', None):
        return ''
    os.makedirs(ctx.evidence_dir, exist_ok=True)
    path = os.path.join(ctx.evidence_dir, basename)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(text if text.endswith('\n') else text + '\n')
    return path


def guard(name, fn, ctx):
    """Run one check fn, converting anything it throws into a FAIL rather than a crashed run.

    A check that raises has still told us something true — it just told us badly. The traceback
    becomes the evidence and the exception line becomes the reason, so one broken check never takes
    the table down with it.
    """
    t0 = time.time()
    try:
        v = fn(ctx)
        if not isinstance(v, Verdict):
            raise ContractError(
                "check %r returned %r, not a Verdict" % (name, type(v).__name__))
        v.seconds = time.time() - t0
        return v
    except ContractError as e:
        return Verdict(name, FAIL, write_evidence(ctx, name + '.contract-error.txt',
                                                  traceback.format_exc()),
                       'CONTRACT VIOLATION: %s' % e, seconds=time.time() - t0)
    except Exception as e:                                       # noqa: BLE001 - deliberate
        return Verdict(name, FAIL, write_evidence(ctx, name + '.traceback.txt',
                                                  traceback.format_exc()),
                       '%s: %s' % (type(e).__name__, e), seconds=time.time() - t0)
