"""ui/templates/selftest.py — prove the slot validator actually refuses.

    python3 ui/templates/selftest.py

A validator nobody has watched reject something is a validator that returns True. This file makes it
reject, one failure mode at a time, and asserts that a page which cannot be filled honestly is NEVER
produced — because the failure mode being defended against is not a crash, it is a page that renders
beautifully and says nothing.

The audit measured what that costs. Nine live self-test probes report `board v=-` and have been
reporting it for long enough that nobody knows when it started:

    "every one reports `board v=-`, i.e. the probe cannot reach a live entrant's board price at all
     (`0 of 14`, `0 of 28`, `0 of 16`, ...)"

A dash rendered. A dash aligned. A dash sorted. Nothing asked why.

Exit 0 = the validator refuses what it should and accepts what it should. Exit 1 = it does not.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import slots                                                                  # noqa: E402


P, F = [0], [0]


def ok(msg):
    P[0] += 1
    print('  PASS  %s' % msg)


def bad(msg):
    F[0] += 1
    print('  FAIL  %s' % msg)


def check(cond, msg):
    ok(msg) if cond else bad(msg)


def refuses(name, data, because, needle=None):
    """Assert render() REFUSES, and that it says why."""
    try:
        slots.render(name, data)
        bad('refuses %s' % because)
    except slots.SlotError as e:
        if needle and needle not in str(e):
            bad('refuses %s — but the message never mentions %r' % (because, needle))
        else:
            ok('refuses %s' % because)


# ---------------------------------------------------------------------------- a complete, good page
def good_tracker():
    row = {'player': 'Toby Conway', 'pos': 'RUCK', 'club': 'Geelong', 'cat': slots.ABSENT,
           'age': 23, 'band': 4, 'pick': 24, 'live': 503, 'K': 899, 'd_live_K': 396, 'P': 1066,
           'd_K_P': 167, 'R': 1066, 'd_P_R': 0, 'candidate': 460, 'd_R_cand': -606,
           'd_live_cand': -43, 'd_K_cand': -439}
    return {
        'page_title': 'Assembly Tracker', 'subtitle': 'The owner standing presentation law.',
        'standing_note': 'Nothing here is adopted; the candidate is for owner review.',
        'board_md5': 'a05fe951', 'store_md5': 'cc02567f', 'engine_head': '5ac6780f',
        'config': 'eed19a75f775', 'as_of_round': 22, 'generated_at': '2026-08-20T04:00:00Z',
        'rows': [row],
    }


def main():
    print(__doc__.strip().split('\n')[0])
    print('=' * 96)

    print('\nPART A — the five skeletons exist, parse, and agree with the manifest')
    expected = ['movers', 'noarb', 'players', 'tracker', 'year1']
    check(slots.names() == expected, 'exactly the five owner-facing pages are declared: %s' % expected)
    for n in expected:
        try:
            _t, sc, bl = slots.parse(n)
            check(bool(sc) and bool(bl), '%-8s parses: %d scalar slot(s), %d row block(s)'
                  % (n, len(sc), len(bl)))
        except Exception as e:                                                # noqa: BLE001
            bad('%-8s parses (%s: %s)' % (n, type(e).__name__, e))

    # The manifest/markup cross-check runs on a page with NO data: every problem reported must then
    # be a missing-value problem, never a "slot not declared" one. If the two files had drifted this
    # is where it would show, on every page at once.
    print('\nPART B — manifest and markup cannot drift apart')
    for n in expected:
        probs = slots.validate(n, {})
        drift = [p for p in probs if 'manifest.json' in p]
        check(not drift, '%-8s manifest declares exactly the slots the markup uses' % n)

    print('\nPART C — a complete page renders')
    html = None
    try:
        html = slots.render('tracker', good_tracker())
        ok('a fully-supplied tracker renders')
    except slots.SlotError as e:
        bad('a fully-supplied tracker renders (%s)' % e)
    if html:
        check('Toby Conway' in html, 'the injected row value reaches the page')
        check('a05fe951' in html, 'the identity stamp reaches the page')
        check('{{' not in html, 'no unfilled slot markers survive into the output')
        check('THE TRACKER' in html, 'the FROZEN layout survives — the seat did not supply it')

    print('\nPART D — the one rule: a missing value is a loud failure, never a dash')
    for value, label in ((None, 'None'), ('', 'an empty string'), ('-', 'a hyphen'),
                         ('—', 'an em dash'), ('N/A', 'N/A'), ('  ', 'whitespace only'),
                         ('null', 'the string "null"'), ('nan', 'nan')):
        d = good_tracker()
        d['rows'][0]['live'] = value
        refuses('tracker', d, 'a row value of %s' % label, needle='live')

    d = good_tracker()
    d['board_md5'] = '—'
    refuses('tracker', d, 'a DASH IN THE IDENTITY STAMP (the worst place for one)', needle='board_md5')

    print('\nPART E — absence must be DECLARED, never inferred')
    d = good_tracker()
    d['rows'][0]['pick'] = slots.ABSENT
    try:
        out = slots.render('tracker', d)
        ok('a nullable slot accepts the EXPLICIT slots.ABSENT marker')
        check('class="absent"' in out,
              'and renders as the declared empty-marker, not as a bare dash')
    except slots.SlotError as e:
        bad('a nullable slot accepts slots.ABSENT (%s)' % e)

    d = good_tracker()
    d['rows'][0]['live'] = slots.ABSENT           # 'live' is NOT nullable in the manifest
    try:
        slots.render('tracker', d)
        bad('a NON-nullable slot refuses slots.ABSENT — undeclared absence must not sneak through')
    except slots.SlotError:
        ok('a NON-nullable slot refuses slots.ABSENT — undeclared absence must not sneak through')

    print('\nPART F — structural refusals')
    d = good_tracker(); del d['rows'][0]['K']
    refuses('tracker', d, 'a row missing a column entirely', needle='K')
    d = good_tracker(); del d['as_of_round']
    refuses('tracker', d, 'a page missing a scalar slot', needle='as_of_round')
    d = good_tracker(); d['rows'] = []
    refuses('tracker', d, 'an EMPTY table (indistinguishable from a broken query)', needle='EMPTY')
    d = good_tracker(); d['rows'] = 'not a list'
    refuses('tracker', d, 'a row list that is not a list')

    print('\nPART G — every problem is reported at once, not one per attempt')
    d = good_tracker()
    del d['as_of_round']; del d['board_md5']; d['rows'][0]['K'] = '-'
    probs = slots.validate('tracker', d)
    check(len(probs) >= 3, 'a page with three defects reports all three (got %d)' % len(probs))

    print('\nPART H — a seat cannot inject layout')
    d = good_tracker()
    d['rows'][0]['player'] = '<script>alert(1)</script>'
    out = slots.render('tracker', d)
    check('<script>' not in out and '&lt;script&gt;' in out,
          'injected markup is ESCAPED — data is data, layout is the template\'s')

    print('')
    print('=' * 96)
    print('TEMPLATE SLOT SELF-TEST: %d PASS / %d FAIL' % (P[0], F[0]))
    if F[0]:
        print('The validator does not refuse what it must. Do not ship a page through it.')
        return 1
    print('A page that cannot be filled honestly is not produced. Seats inject data, never layout.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
