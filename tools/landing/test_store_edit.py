#!/usr/bin/env python3
"""apply_store_edits — the SEASON-ROW path and its refusals (2026-08-30); the ADD verb (2026-10-14).

Run:  python3 tools/landing/test_store_edit.py       (exit 0 = all pass)

The flat path (`p_dual`) has been exercised by a real landing and by the lander self-test. The
season path (`scoring[2017].games`) is new, and it reaches INSIDE a container the surgical editor
had until now refused to touch on the explicit ground that a container's on-disk spacing is not
this step's to assume. That ground still holds — the edit writes a SCALAR inside a season, never the
list around it — but a narrower target is a target that can be missed, so everything below is about
what happens when it is: a wrong `old`, an absent season, an absent field, a value that appears in
more than one season, and a replacement that strays past the season's own braces.

THE ADD VERB (`{key, field, add}`, 2026-10-14) is the lane's one way to put a field on a row that
does not carry it — `_last_listed`, a listing fact the owner supplied for ~204 retired rows. The
second half below is about where the field goes (after the key the rows that already carry it have
it after — the store is NOT key-sorted, so the position is measured, never computed), what it
refuses (a row that carries the field, a season path, an entry that also says old/new, a row with
no anchor, a container value), that it mixes with changes on other rows and on the same row, and
that removing the inserted bytes reproduces the input character for character.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, ROOT)

from tools.landing import steps as ST                       # noqa: E402
from tools.landing import spec as SPEC                      # noqa: E402
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
    # A TOP-LEVEL VALUE THAT A SEASON ALSO CARRIES (2026-09-24). Career games kept equal to the season
    # sum makes `"games": N` at the top of a row and inside a season the COMMON case (every one-season
    # player). The flat path must edit the row's own field and leave the season alone, not refuse.
    same = json.dumps({'players': [{'key': 'e', 'games': 21, 'scoring': [
        {'year': 2026, 'avg': 60.0, 'games': 21}]}]})
    out6, _ = ST.apply_store_edits(same, [{'key': 'e', 'field': 'games', 'old': 21, 'new': 22},
                                          {'key': 'e', 'field': 'scoring[2026].games',
                                           'old': 21, 'new': 22}])
    e6 = json.loads(out6)['players'][0]
    ok(e6['games'] == 22 and e6['scoring'][0]['games'] == 22,
       'a top-level field whose value a season also carries: each path edits its OWN field')
    out7, _ = ST.apply_store_edits(same, [{'key': 'e', 'field': 'games', 'old': 21, 'new': 30}])
    e7 = json.loads(out7)['players'][0]
    ok(e7['games'] == 30 and e7['scoring'][0]['games'] == 21,
       '...and the flat edit alone leaves the equal-valued season untouched')

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

    add_verb()
    add_spec()
    add_live_store()

    print('  ' + '-' * 70)
    print('STORE-EDIT TESTS: %s' % ('ALL %d PASS' % n if not fails else '%d FAIL / %d' % (fails, n)))
    return 1 if fails else 0


# A store shaped like the real one: a top-level LIST, `json.dumps` default spacing (`, ` and `: `),
# rows in writer order (NOT sorted), and two exemplar rows that carry `_last_listed` right after
# `_pickless` — which is what all 13 rows in engine/rl_after/rl_model_data.json do (2026-10-14).
ADD_STORE = json.dumps([
    {'player': 'X', 'key': 'x-exemplar', 'games': 3, '_retired': True, '_pickless': False,
     '_last_listed': 2025, 'future_position': 'MID'},
    {'player': 'Y', 'key': 'y-exemplar', 'games': 1, '_retired': True, '_pickless': True,
     '_last_listed': 2024, 'future_position': 'SF'},
    {'player': 'R', 'key': 'r-target', 'games': 9, 'scoring': [{'year': 2024, 'games': 9}],
     '_retired': True, '_pickless': False, '_bd': '2000-01-01', 'future_position': 'SD'},
    {'player': 'S', 'key': 's-target', 'games': 2, '_retired': True, 'future_position': 'SD'},
])


def _reversed(out, applied):
    rev = out
    for ap in reversed(applied):
        rev = rev[:ap['at']] + ap['old_text'] + rev[ap['at'] + len(ap['new_text']):]
    return rev


def _row(text, key):
    return ST.store_row_spans(text, [key])[key][2]


def add_verb():
    print('\nSTORE-EDIT ADD VERB\n  ' + '-' * 70)
    before = json.loads(ADD_STORE)
    r0 = [r for r in before if r['key'] == 'r-target'][0]

    # ---- the happy path: inserted AFTER the anchor the exemplars share --------------------------
    out, applied = ST.apply_store_edits(ADD_STORE, [{'key': 'r-target', 'field': '_last_listed',
                                                     'add': 2025}])
    r = _row(out, 'r-target')
    ok(r == dict(r0, _last_listed=2025), 'the row re-parses as the ORIGINAL dict plus the one new key')
    ok(list(r) == ['player', 'key', 'games', 'scoring', '_retired', '_pickless', '_last_listed',
                   '_bd', 'future_position'],
       'the field is inserted AFTER `_pickless` — the key every exemplar row carries it after — and '
       'before whatever that row has next (`_bd` here, not `future_position`: anchored, not sorted)')
    ok(len(applied) == 1 and applied[0]['kind'] == 'add' and applied[0]['old'] is None
       and applied[0]['new'] == 2025 and applied[0]['old_text'] == '',
       'applied records {kind: add, old: None, new: value} with an EMPTY old_text')
    ok(applied[0]['new_text'] == ', "_last_listed": 2025',
       'the inserted bytes are exactly `, "_last_listed": 2025` — the row\'s own separator and colon '
       'spacing, copied (%r)' % applied[0]['new_text'])
    ok(out[applied[0]['at'] - len('"_pickless": false'):applied[0]['at']] == '"_pickless": false',
       'the insertion offset is the end of the anchor field\'s value')
    ok(_reversed(out, applied) == ADD_STORE,
       'removing the inserted text reproduces the input CHARACTER FOR CHARACTER')
    others = [k for k in ('x-exemplar', 'y-exemplar', 's-target')]
    sb, sa = ST.store_row_spans(ADD_STORE, others), ST.store_row_spans(out, others)
    ok(all(ADD_STORE[sb[k][0]:sb[k][1]] == out[sa[k][0]:sa[k][1]] for k in others),
       'every other row\'s text is byte-identical')
    ok(json.loads(out)[0] == before[0] and json.loads(out)[1] == before[1],
       'the exemplar rows still carry their own values')

    # ---- THE REFUSALS ----------------------------------------------------------------------------
    got, why = refuses([{'key': 'x-exemplar', 'field': '_last_listed', 'add': 2025}], ADD_STORE,
                       'ALREADY ON THE ROW')
    ok(got, 'an add to a row that CARRIES the field ABORTS — it never overwrites  (%s)' % why)
    try:
        ST.apply_store_edits(ADD_STORE, [{'key': 'x-exemplar', 'field': '_last_listed', 'add': 2026}])
        msg = ''
    except StepError as exc:
        msg = str(exc)
    ok('x-exemplar' in msg and '_last_listed' in msg and 'carries: 2025' in msg,
       '...and the refusal names the row, the field and the value it carries')

    got, why = refuses([{'key': 'r-target', 'field': 'scoring[2024].avg', 'add': 50.0}], ADD_STORE,
                       'FLAT')
    ok(got, 'an add on a SEASON path is refused — the verb is top-level only  (%s)' % why)

    got, why = refuses([{'key': 'r-target', 'field': '_last_listed', 'add': 2025, 'old': None,
                         'new': 2025}], ADD_STORE, 'mutually exclusive')
    ok(got, 'an add that also carries old/new is refused — one entry is one verb  (%s)' % why)

    got, why = refuses([{'key': 's-target', 'field': '_last_listed', 'add': 2025}], ADD_STORE,
                       'lacks')
    ok(got, 'a row that LACKS the anchor key has no position that keeps the file\'s order — '
            'refused, not guessed  (%s)' % why)

    got, why = refuses([{'key': 'r-target', 'field': '_tags', 'add': ['a']}], ADD_STORE, 'container')
    ok(got, 'a container value is refused, as it is for a change  (%s)' % why)

    got, why = refuses([{'key': 'nobody', 'field': '_last_listed', 'add': 2025}], ADD_STORE,
                       'no row with key')
    ok(got, 'a key the store does not have is refused — the lane never creates a ROW')

    got, why = refuses([{'key': 'r-target', 'field': '_last_listed', 'add': 2025},
                        {'key': 'r-target', 'field': '_last_listed', 'add': 2025}],
                       ADD_STORE, 'ALREADY ON THE ROW')
    ok(got, 'a second add of the same field to the same row aborts on the first one\'s output')

    # exemplars that DISAGREE on the position are a refusal, not a vote
    dis = json.dumps([{'key': 'a', 'p': 1, '_ll': 1, 'q': 2}, {'key': 'b', 'p': 1, 'q': 2, '_ll': 1},
                      {'key': 'c', 'p': 1, 'q': 2}])
    got, why = refuses([{'key': 'c', 'field': '_ll', 'add': 3}], dis, 'do not agree')
    ok(got, 'exemplar rows that place the field after DIFFERENT keys refuse the add  (%s)' % why)

    # ---- NO EXEMPLAR: the file has no order for the field, so it goes LAST --------------------
    out2, ap2 = ST.apply_store_edits(ADD_STORE, [{'key': 'r-target', 'field': '_note', 'add': 'x'}])
    r2 = _row(out2, 'r-target')
    ok(list(r2)[-1] == '_note' and r2 == dict(r0, _note='x') and ap2[0]['anchor'] == 'as the LAST field',
       'a field NO row carries yet is appended as the row\'s LAST field')
    ok(_reversed(out2, ap2) == ADD_STORE, '...and its reversal holds')

    # ---- the file's own escaping: ascii-escaped store takes the escaped form --------------------
    out3, ap3 = ST.apply_store_edits(ADD_STORE, [{'key': 'r-target', 'field': '_club',
                                                  'add': 'Ca\u00f1as'}])
    ok('\\u00f1' in ap3[0]['new_text'] and _row(out3, 'r-target')['_club'] == 'Ca\u00f1as',
       'a non-ASCII string added to a pure-ASCII store is written `\\u`-escaped, as the file is')

    # ---- MIXED LISTS: change + add on different rows, and on the SAME row --------------------
    out4, ap4 = ST.apply_store_edits(ADD_STORE, [
        {'key': 'x-exemplar', 'field': 'games', 'old': 3, 'new': 4},
        {'key': 'r-target', 'field': '_last_listed', 'add': 2025}])
    ok(_row(out4, 'x-exemplar')['games'] == 4 and _row(out4, 'r-target')['_last_listed'] == 2025
       and [a['kind'] for a in ap4] == ['change', 'add'],
       'a change on one row and an add on another apply in order, each recorded with its kind')
    ok(_reversed(out4, ap4) == ADD_STORE, '...and reversing both reproduces the input')

    out5, ap5 = ST.apply_store_edits(ADD_STORE, [
        {'key': 'r-target', 'field': 'games', 'old': 9, 'new': 10},
        {'key': 'r-target', 'field': '_last_listed', 'add': 2025},
        {'key': 'r-target', 'field': 'scoring[2024].games', 'old': 9, 'new': 10}])
    r5 = _row(out5, 'r-target')
    ok(r5 == dict(r0, games=10, _last_listed=2025, scoring=[{'year': 2024, 'games': 10}])
       and list(r5).index('_last_listed') == list(r5).index('_pickless') + 1,
       'change, add and a season change on the SAME row: all three land, the add in its place')
    ok(_reversed(out5, ap5) == ADD_STORE, '...and reversing all three reproduces the input')
    out6, ap6 = ST.apply_store_edits(ADD_STORE, [
        {'key': 'r-target', 'field': '_last_listed', 'add': 2025},
        {'key': 'r-target', 'field': 'games', 'old': 9, 'new': 10}])
    ok(_row(out6, 'r-target') == dict(r0, games=10, _last_listed=2025)
       and _reversed(out6, ap6) == ADD_STORE,
       'the same pair in the other order (add first) lands and reverses too')

    # ---- the step's post-write re-read resolves an add like a flat change --------------------
    spans = ST.store_row_spans(out4)
    ok(all(spans[a['key']][2].get(a['field']) == a['new'] for a in ap4),
       'the post-write re-read (`row.get(field) == new`) holds for an add as for a change')


def add_spec():
    print('\nSTORE-EDIT ADD VERB — spec validation\n  ' + '-' * 70)

    def problems(*entries):
        return [b for b in SPEC._validate_edit({'edit': {'store': list(entries)},
                                                'identities': {'moves': ['store']}})
                if 'edit.store' in b]

    ok(problems({'key': 'r', 'field': '_last_listed', 'add': 2025}) == [],
       'a well-formed add validates')
    ok(any('add' in b and '`old`' in b for b in problems(
        {'key': 'r', 'field': '_last_listed', 'add': 2025, 'old': None, 'new': 2025})),
       'add + old/new is refused by the validator')
    ok(any('flat' in b.lower() for b in problems(
        {'key': 'r', 'field': 'scoring[2024].games', 'add': 1})),
       'a season path under add is refused by the validator')
    ok(any('SCALAR' in b for b in problems({'key': 'r', 'field': '_x', 'add': {'a': 1}})),
       'a container value under add is refused by the validator')
    ok(any('twice' in b for b in problems({'key': 'r', 'field': 'games', 'old': 1, 'new': 2},
                                          {'key': 'r', 'field': 'games', 'add': 2})),
       'an add and a change of the SAME field on the SAME row are refused as a duplicate')
    ok(any('required' in b for b in problems({'key': 'r', 'add': 2025})),
       'an add without a field is refused')
    ok(problems({'key': 'r', 'field': 'games', 'old': 1, 'new': 2}) == [],
       'a plain change still validates')


def add_live_store():
    """Against the REAL store when it is present: the anchor the 13 `_last_listed` rows share."""
    path = os.path.join(ROOT, ST.STORE_REL)
    if not os.path.isfile(path):
        return
    print('\nSTORE-EDIT ADD VERB — the live store\n  ' + '-' * 70)
    text = open(path, 'rb').read().decode('utf-8')
    rows = json.loads(text)
    have = [r for r in rows if '_last_listed' in r]
    ok(have and all(list(r)[list(r).index('_last_listed') - 1] == '_pickless' for r in have),
       'every row that carries `_last_listed` (%d) has it immediately after `_pickless`' % len(have))
    anchor = ST._add_anchor(text, '_last_listed')
    ok(anchor == {'kind': 'after', 'after': '_pickless', 'exemplars': len(have)},
       'the measured anchor is `_pickless`, from %d exemplar row(s)' % len(have))
    targets = []
    for nxt in ('future_position', '_bd'):
        for r in rows:
            ks = list(r)
            if r.get('_retired') and '_last_listed' not in r and '_pickless' in ks \
                    and ks[ks.index('_pickless') + 1] == nxt:
                targets.append(r['key'])
                break
    edits = [{'key': k, 'field': '_last_listed', 'add': 2025} for k in targets]
    out, applied = ST.apply_store_edits(text, edits)
    ok(len(applied) == len(targets) == 2 and all(
        a['new_text'] == ', "_last_listed": 2025' for a in applied),
       'two retired rows (one `_pickless, future_position`, one `_pickless, _bd`) take exactly '
       '`, "_last_listed": 2025`')
    ok(all(list(_row(out, k)).index('_last_listed') == list(_row(out, k)).index('_pickless') + 1
           for k in targets), '...each right after `_pickless`')
    ok(_reversed(out, applied) == text, '...and removing both reproduces the live store byte-for-byte')
    ok(len(ST.store_row_spans(out)) == len(rows), '...with the row count unmoved')


if __name__ == '__main__':
    sys.exit(main())
