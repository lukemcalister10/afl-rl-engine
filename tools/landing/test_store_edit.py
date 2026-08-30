#!/usr/bin/env python3
"""apply_store_edits — the SEASON-ROW path and its refusals (2026-08-30).

Run:  python3 tools/landing/test_store_edit.py       (exit 0 = all pass)

The flat path (`p_dual`) has been exercised by a real landing and by the lander self-test. The
season path (`scoring[2017].games`) is new, and it reaches INSIDE a container the surgical editor
had until now refused to touch on the explicit ground that a container's on-disk spacing is not
this step's to assume. That ground still holds — the edit writes a SCALAR inside a season, never the
list around it — but a narrower target is a target that can be missed, so everything below is about
what happens when it is: a wrong `old`, an absent season, an absent field, a value that appears in
more than one season, and a replacement that strays past the season's own braces.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, ROOT)

from tools.landing import steps as ST                       # noqa: E402
from tools.landing.steps import StepError                   # noqa: E402

fails = 0
n = 0


def ok(cond, label):
    global fails, n
    n += 1
    print(('  [PASS] ' if cond else '  [FAIL] ') + label)
    if not cond:
        fails += 1


def refuses(edits, text, must_say):
    try:
        ST.apply_store_edits(text, edits)
        return False, 'no refusal'
    except StepError as exc:
        return (must_say.lower() in str(exc).lower()), str(exc).splitlines()[0][:90]


STORE = json.dumps({'players': [
    {'key': 'a-player', 'player': 'A Player', 'games': 40, 'scoring': [
        {'year': 2017, 'avg': 11.0, 'games': 61, 'pos': 'SD'},
        {'year': 2018, 'avg': 17.0, 'games': 60, 'pos': 'SD'},
        {'year': 2019, 'avg': 61.0, 'games': 11, 'pos': 'SD'}]},
    {'key': 'b-player', 'player': 'B Player', 'games': 5, 'scoring': [
        {'year': 2017, 'avg': 11.0, 'games': 61, 'pos': 'MID'}]},
]})


def main():
    print('STORE-EDIT SEASON PATH\n  ' + '-' * 70)

    # ---- the happy path -----------------------------------------------------------------------
    edits = [{'key': 'a-player', 'field': 'scoring[2017].games', 'old': 61, 'new': 11},
             {'key': 'a-player', 'field': 'scoring[2017].avg', 'old': 11.0, 'new': 61.0}]
    out, applied = ST.apply_store_edits(STORE, edits)
    d = json.loads(out)
    a = [r for r in d['players'] if r['key'] == 'a-player'][0]
    b = [r for r in d['players'] if r['key'] == 'b-player'][0]
    s17 = [s for s in a['scoring'] if s['year'] == 2017][0]
    ok(s17['games'] == 11 and s17['avg'] == 61.0, 'a season scalar is corrected in place')
    ok([s for s in a['scoring'] if s['year'] == 2018][0] == {'year': 2018, 'avg': 17.0,
                                                            'games': 60, 'pos': 'SD'},
       'the OTHER seasons of the same row are untouched')
    ok(b['scoring'][0]['games'] == 61 and b['scoring'][0]['avg'] == 11.0,
       'the identical season in ANOTHER row is untouched — this is a row-scoped edit, not a global '
       'substitution')
    ok(a['games'] == 40, 'the row\'s own top-level fields are untouched')

    # reversal, character for character
    rev = out
    for ap in reversed(applied):
        rev = rev[:ap['at']] + ap['old_text'] + rev[ap['at'] + len(ap['new_text']):]
    ok(rev == STORE, 'reversing every replacement reproduces the input CHARACTER FOR CHARACTER')

    # ---- THE REFUSALS -------------------------------------------------------------------------
    got, why = refuses([{'key': 'a-player', 'field': 'scoring[2017].games', 'old': 60, 'new': 11}],
                       STORE, 'OLD VALUE')
    ok(got, 'a WRONG `old` on a season field ABORTS — it is never repaired  (%s)' % why)

    got, why = refuses([{'key': 'a-player', 'field': 'scoring[2099].games', 'old': 61, 'new': 11}],
                       STORE, 'no scoring row')
    ok(got, 'a season the row does not have is refused — the lander never creates one')

    got, why = refuses([{'key': 'a-player', 'field': 'scoring[2017].nope', 'old': 1, 'new': 2}],
                       STORE, 'has no field')
    ok(got, 'a field the season does not carry is refused')

    got, why = refuses([{'key': 'nobody', 'field': 'scoring[2017].games', 'old': 61, 'new': 11}],
                       STORE, 'no row with key')
    ok(got, 'a key the store does not have is refused')

    got, why = refuses([{'key': 'a-player', 'field': 'scoring[2017].games', 'old': 61, 'new': 11},
                        {'key': 'a-player', 'field': 'scoring[2017].games', 'old': 61, 'new': 12}],
                       STORE, 'OLD VALUE')
    ok(got, 'a second edit to a field already edited aborts on its own `old` assertion')

    # ---- AMBIGUITY INSIDE ONE SEASON ----------------------------------------------------------
    # `avg` and `games` both 11 in the same season: the pattern is "field": value, so the field name
    # disambiguates and the edit is still exactly one hit. The value appearing twice must not matter.
    amb = json.dumps({'players': [{'key': 'c', 'scoring': [{'year': 2020, 'avg': 11, 'games': 11}]}]})
    out2, _ = ST.apply_store_edits(amb, [{'key': 'c', 'field': 'scoring[2020].games',
                                          'old': 11, 'new': 19}])
    c = json.loads(out2)['players'][0]['scoring'][0]
    ok(c['games'] == 19 and c['avg'] == 11,
       'when two fields of one season share a value, the NAMED field is the one that moves')

    # ---- the same year appearing twice in one row is REFUSED, not guessed ----------------------
    # This one was written the other way first and the implementation refused it. The refusal is
    # right: a row carrying one season twice is broken, and editing whichever came first is a guess
    # dressed as a surgical edit. The test was changed to the implementation, not the reverse.
    dup = json.dumps({'players': [{'key': 'd', 'scoring': [{'year': 2020, 'games': 5},
                                                           {'year': 2020, 'games': 6}]}]})
    got, why = refuses([{'key': 'd', 'field': 'scoring[2020].games', 'old': 5, 'new': 7}],
                       dup, 'duplicated season')
    ok(got, 'a row carrying the same season TWICE is refused rather than half-edited  (%s)' % why)

    # ---- the flat path still behaves ------------------------------------------------------------
    out4, _ = ST.apply_store_edits(STORE, [{'key': 'a-player', 'field': 'games',
                                            'old': 40, 'new': 48}])
    a4 = [r for r in json.loads(out4)['players'] if r['key'] == 'a-player'][0]
    ok(a4['games'] == 48 and a4['scoring'][0]['games'] == 61,
       'the FLAT path is unchanged: a top-level scalar moves and the seasons do not')
    # declared with the row's TRUE list, so the refusal is the container guard itself and not an
    # `old` mismatch arriving first — the distinction matters, because only one of those two is the
    # law being tested.
    true_list = [r for r in json.loads(STORE)['players'] if r['key'] == 'a-player'][0]['scoring']
    got, why = refuses([{'key': 'a-player', 'field': 'scoring',
                         'old': true_list, 'new': true_list[:1]}], STORE, 'container')
    ok(got, 'declaring the whole `scoring` list is still REFUSED as a container, even with a '
            'correct `old`  (%s)' % why)

    # ---- THE RE-READ RESOLVES A SEASON PATH TOO ---------------------------------------------
    # The first real flight of the season path aborted here and nowhere else: the edit applied
    # perfectly, and the step's post-write verification then read `row['scoring[2017].games']` — not
    # a key on the row — got null, and refused its own correct work. A verification that resolves a
    # path differently from the editor is asserting about a field nobody wrote.
    out5, ap5 = ST.apply_store_edits(STORE, [
        {'key': 'a-player', 'field': 'scoring[2017].games', 'old': 61, 'new': 11},
        {'key': 'a-player', 'field': 'games', 'old': 40, 'new': 48}])
    spans = ST.store_row_spans(out5)
    checked = []
    for ap in ap5:
        m = ST._SEASON_FIELD.match(str(ap['field']))
        if m:
            yr, sub = int(m.group(1)), m.group(2)
            srows = [x for x in spans[ap['key']][2]['scoring'] if x.get('year') == yr]
            checked.append(len(srows) == 1 and srows[0].get(sub) == ap['new'])
        else:
            checked.append(spans[ap['key']][2].get(ap['field']) == ap['new'])
    ok(all(checked) and len(checked) == 2,
       'the post-write re-read resolves BOTH a season path and a flat field to the written value')

    print('  ' + '-' * 70)
    print('STORE-EDIT TESTS: %s' % ('ALL %d PASS' % n if not fails else '%d FAIL / %d' % (fails, n)))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
