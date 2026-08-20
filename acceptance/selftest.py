"""acceptance/selftest.py — prove the spine can actually fail.

    python3 -m acceptance.selftest

A gate nobody has ever seen fire is a decoration. The audit is full of instruments that were
green for the wrong reason — the `_V0SURF_GATES['RL_M3_FE']` key frozen at 0.58 for a channel that
has since moved to 0.92 ("a guard that has quietly stopped watching"), the `'0.85'` RL_GAMMA
fallback that "can never fall through to it in a real build", the nine `#326` pool-entry probes
reporting `board v=-` because they can no longer reach a live entrant at all. Each was passing, or
believed to be passing, while asserting nothing.

So before this spine is allowed to certify anything, it certifies itself. Part A is the requirement
this order names explicitly:

    FORCE A FAILURE IN EVERY REGISTERED CHECK, ONE AT A TIME, AND ASSERT THE AGGREGATE GOES
    NON-ZERO EACH TIME.

If a registered check can be made to fail and the runner still exits 0, that check is decoration
and the spine is lying. Part B then proves the blocked-once law itself — that BLOCKED suppresses a
duplicate red without ever suppressing an independent one, which is the property the whole contract
turns on and the easiest one to get subtly wrong.

Exit 0 = the spine is honest. Exit 1 = it is not, and nothing it says should be believed.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from acceptance import contract as C                                          # noqa: E402
from acceptance import known_red                                              # noqa: E402
from acceptance import runner as R                                            # noqa: E402


class Out(object):
    def __init__(self):
        self.lines, self.passed, self.failed = [], 0, 0

    def ok(self, msg):
        self.passed += 1
        self.lines.append('  PASS  %s' % msg)

    def bad(self, msg):
        self.failed += 1
        self.lines.append('  FAIL  %s' % msg)

    def assert_(self, cond, msg):
        self.ok(msg) if cond else self.bad(msg)

    def head(self, msg):
        self.lines.append('')
        self.lines.append(msg)


def _ctx():
    """A context with no evidence dir — the self-test asserts verdicts, not files."""
    return R.RunContext(_ROOT, None)


def _stub(name, verdict=C.PASS, reason='stub', halts=()):
    def fn(_ctx_):
        return C.Verdict(name, verdict, '', reason, halted_carriers=halts)
    fn.HALTS = tuple(halts)
    return fn


# ==================================================================================================
def part_a_force_each_check(o):
    """Force a failure in EVERY registered check, one at a time; assert non-zero each time."""
    import acceptance.checks                                                  # noqa: F401
    real = C.registry()
    o.head('PART A — force a failure in each registered check (%d checks)' % len(real))
    o.assert_(len(real) > 0, 'the registry is non-empty (a spine with no checks certifies nothing)')

    for target in real:
        # Every OTHER check is stubbed to a clean PASS that halts nothing, so the only thing that
        # can red this run is the one check under test. Without that isolation a check that is
        # already BLOCKED on this tree could never be shown to gate, and the proof would be vacuous
        # for exactly the checks most likely to be decoration.
        forced = []
        for c in real:
            if c.name == target.name:
                forced.append(C.Check(c.name, _stub(c.name, C.FAIL, 'FORCED FAILURE (self-test)'),
                                      reads=(), doc=c.doc))
            else:
                forced.append(C.Check(c.name, _stub(c.name, C.PASS, 'stubbed PASS'),
                                      reads=(), doc=c.doc))

        rows = R.run(_ctx(), forced)
        code = R.exit_code(rows)
        row = [r for r in rows if r.name == target.name][0]

        o.assert_(code != 0,
                  'forcing %-24s to FAIL reds the aggregate (exit %d)' % (target.name, code))
        o.assert_(row.verdict == C.FAIL,
                  'forcing %-24s produces a FAIL row, not a swallowed one' % target.name)
        o.assert_(len(rows) == len(real),
                  'forcing %-24s still yields exactly %d rows (no check vanishes)'
                  % (target.name, len(real)))

    # And the control: with nothing forced, the same stubbed registry must go green. A self-test
    # whose harness fails everything proves nothing about the checks.
    allpass = [C.Check(c.name, _stub(c.name, C.PASS, 'stubbed PASS'), (), c.doc) for c in real]
    rows = R.run(_ctx(), allpass)
    o.assert_(R.exit_code(rows) == 0,
              'CONTROL: the same harness with nothing forced exits 0 (the failures above are the '
              'forced ones, not the harness)')


# ==================================================================================================
def part_b_blocked_once_law(o):
    """The law: one halted carrier is reported ONCE, everything downstream BLOCKED."""
    o.head('PART B — the blocked-once law (register v787)')
    carrier = 'expected_boot:store'

    trunk = C.Check('trunk', _stub('trunk', C.FAIL, 'carrier drifted', halts=(carrier,)),
                    reads=(), doc='')
    d1 = C.Check('down_1', _stub('down_1', C.FAIL, 'would restate the same drift'),
                 reads=(carrier,), doc='')
    d2 = C.Check('down_2', _stub('down_2', C.FAIL, 'would restate it again'),
                 reads=(carrier,), doc='')
    indep = C.Check('independent', _stub('independent', C.FAIL, 'a genuinely separate defect'),
                    reads=('some_other:carrier',), doc='')

    ctx = _ctx()
    rows = R.run(ctx, [trunk, d1, d2, indep])
    by = {r.name: r for r in rows}

    o.assert_(by['trunk'].verdict == C.FAIL, 'the check that finds the drift reports it (FAIL)')
    o.assert_(by['down_1'].verdict == C.BLOCKED and by['down_2'].verdict == C.BLOCKED,
              'BOTH downstream checks are BLOCKED, not failed a second and third time')
    o.assert_(carrier in by['down_1'].reason and 'trunk' in by['down_1'].reason,
              'a BLOCKED row names the carrier AND the check that halted it')

    # The property that makes the law safe rather than merely tidy.
    o.assert_(by['independent'].verdict == C.FAIL,
              'an INDEPENDENT failure still fails — blocking never hides an unrelated red')

    nfail = sum(1 for r in rows if r.verdict == C.FAIL)
    o.assert_(nfail == 2,
              'one halted carrier + one independent defect == 2 reds, not 4 (this is the '
              'thirty-failures antipattern, measured)')
    o.assert_(len(ctx.halted) == 1 and carrier in ctx.halted,
              'the carrier ledger names the halt exactly ONCE')

    # BLOCKED alone must not gate: the cause is already reported upstream by whoever halted it.
    ctx2 = _ctx()
    rows2 = R.run(ctx2, [
        C.Check('ruled', _stub('ruled', C.RULED_RED, 'presented fork', halts=(carrier,)), (), ''),
        C.Check('down', _stub('down', C.FAIL, 'unreached'), (carrier,), '')])
    o.assert_(R.exit_code(rows2) == 0,
              'RULED-RED upstream + BLOCKED downstream exits 0 (a presented fork is not this '
              "run's to clear)")
    o.assert_([r.verdict for r in rows2] == [C.RULED_RED, C.BLOCKED],
              'and the rows say exactly that: RULED-RED, then BLOCKED')

    # ... but a RULED-RED must never let an unrelated FAIL through.
    rows3 = R.run(_ctx(), [
        C.Check('ruled', _stub('ruled', C.RULED_RED, 'presented fork', halts=(carrier,)), (), ''),
        C.Check('other', _stub('other', C.FAIL, 'unrelated'), (), '')])
    o.assert_(R.exit_code(rows3) != 0,
              'a RULED-RED row does NOT make the run green: an unrelated FAIL still reds it')


# ==================================================================================================
def part_c_contract_integrity(o):
    """The contract refuses malformed verdicts rather than passing them through."""
    o.head('PART C — the verdict contract refuses to be abused')

    for bad, why in ((lambda: C.Verdict('x', 'GREENISH', '', 'r'), 'a verdict outside the four'),
                     (lambda: C.Verdict('x', C.FAIL, '', ''), 'a verdict with no reason'),
                     (lambda: C.Verdict('x', C.PASS, '', 'r', halted_carriers=('c',)),
                      'a PASS that claims to halt a carrier')):
        try:
            bad()
            o.bad('rejected: %s' % why)
        except C.ContractError:
            o.ok('rejected: %s' % why)

    # A check that raises becomes a FAIL with the traceback as evidence — it never takes the run down.
    def explode(_c):
        raise RuntimeError('deliberate')
    rows = R.run(_ctx(), [C.Check('boom', explode, (), '')])
    o.assert_(len(rows) == 1 and rows[0].verdict == C.FAIL and 'deliberate' in rows[0].reason,
              'a check that RAISES becomes a FAIL row, not a crashed run')

    # A check that returns the wrong type is a contract violation, not a silent pass.
    rows = R.run(_ctx(), [C.Check('liar', lambda _c: 'fine', (), '')])
    o.assert_(rows[0].verdict == C.FAIL and 'CONTRACT VIOLATION' in rows[0].reason,
              'a check returning a non-Verdict is a CONTRACT VIOLATION FAIL')


# ==================================================================================================
def part_d_registry_order(o):
    """A registry ordered so the law cannot hold is refused, not run."""
    o.head('PART D — registry ordering is validated, not assumed')
    carrier = 'expected_boot:board'
    early = C.Check('reads_it_first', _stub('reads_it_first'), reads=(carrier,), doc='')
    late = C.Check('halts_it_later', _stub('halts_it_later', C.FAIL, 'drift', halts=(carrier,)),
                   reads=(), doc='')

    o.assert_(bool(R.validate_registry([early, late])),
              'a registry where the reader runs BEFORE the halter is refused')
    o.assert_(not R.validate_registry([late, early]),
              'the correct order (halter first) is accepted')

    import acceptance.checks                                                  # noqa: F401
    o.assert_(not R.validate_registry(C.registry()),
              'THE SHIPPED REGISTRY is correctly ordered')


# ==================================================================================================
def part_e_known_red_ledger(o):
    """The RULED-RED ledger is self-expiring, and cannot quietly stop being true."""
    o.head('PART E — the RULED-RED ledger cannot go stale unnoticed')
    entries = [{'id': 'TEST-1', 'carriers': ['a:x', 'a:y'], 'presented': 'doc'}]

    ruled, unruled = known_red.classify(['a:x'], entries)
    o.assert_(len(ruled) == 1 and not unruled, 'a covered carrier classifies as ruled')

    ruled, unruled = known_red.classify(['a:x', 'b:z'], entries)
    o.assert_(unruled == ['b:z'],
              'an UNCOVERED carrier alongside a covered one is still unruled (being mostly-known '
              'is not a defence)')

    o.assert_(not known_red.stale(['a:x'], entries),
              'an entry with one carrier still drifting is NOT stale')
    o.assert_([e['id'] for e in known_red.stale([], entries)] == ['TEST-1'],
              'an entry whose carriers are all coherent again IS stale, and must be retired')

    live = known_red.load()
    o.assert_(all(e.get('presented') and e.get('carriers') and e.get('id') for e in live),
              'every SHIPPED ledger entry names an id, its carriers, and where the fork was '
              'presented (a red nobody has presented is a FAIL, not a RULED-RED)')


# ==================================================================================================
def main():
    o = Out()
    print(__doc__.strip().split('\n')[0])
    print('=' * 100)
    part_a_force_each_check(o)
    part_b_blocked_once_law(o)
    part_c_contract_integrity(o)
    part_d_registry_order(o)
    part_e_known_red_ledger(o)

    print('\n'.join(o.lines))
    print('')
    print('=' * 100)
    print('SPINE SELF-TEST: %d PASS / %d FAIL' % (o.passed, o.failed))
    if o.failed:
        print('THE SPINE IS NOT HONEST — do not believe any verdict it prints until this is green.')
        return 1
    print('The spine can fail, fails for the right reasons, and reports each cause exactly once.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
