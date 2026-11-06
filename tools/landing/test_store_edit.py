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
    season_add()
    row_add()
    season_and_row_spec()
    season_and_row_live()

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

    # 2026-11-06: the anchor is the full precedence the exemplars agree on, so a row that lacks the
    # usual predecessor (`_pickless`) takes the field after its LAST key the exemplars put before it.
    out, applied = ST.apply_store_edits(ADD_STORE, [{'key': 's-target', 'field': '_last_listed', 'add': 2025}])
    srow = ST.store_row_spans(out, ['s-target'])['s-target'][2]
    ok(list(srow) == ['player', 'key', 'games', '_retired', '_last_listed', 'future_position'],
       'a row that LACKS the usual anchor key takes the field after its last agreed predecessor (`_retired`), keeping the order')
    got, why = refuses([{'key': 'c', 'field': '_ll', 'add': 3}],
                       json.dumps([{'key': 'a', '_ll': 1, 'p': 1}, {'key': 'b', 'p': 1, '_ll': 1}, {'key': 'c', 'p': 2}]),
                       'before it in some rows, after it in others')
    ok(got, 'a TRUE order conflict is refused when the target row carries the conflicting key  (%s)' % why)
    out, _ = ST.apply_store_edits(json.dumps([{'key': 'a', '_ll': 1, 'p': 1}, {'key': 'b', 'p': 1, '_ll': 1}, {'key': 'c', 'q': 2}]),
                                  [{'key': 'c', 'field': '_ll', 'add': 3}])
    ok(list(ST.store_row_spans(out, ['c'])['c'][2]) == ['key', '_ll', 'q'],
       'a conflicting key the target does NOT carry cannot break the order: the add goes after the last agreed predecessor')

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
    ok(anchor['kind'] == 'ordered' and '_pickless' in anchor['before'] and 'future_position' in anchor['after_keys']
       and anchor['exemplars'] == len(have),
       'the measured precedence puts `_pickless` before and `future_position` after, from %d exemplar row(s)' % len(have))
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


# ================================================= THE SEASON ADD AND THE ROW ADD (2026-11-06)
# A store shaped like the real one for the two container verbs: a top-level LIST, json.dumps default
# spacing, season objects in ONE key order (`year, avg, games, pos`, as all 11,484 live ones are)
# and in ascending year order, rows in writer order, and three key shapes so that `required`
# (every row) and `allowed` (any row) differ and the majority order has something to measure.
SEASON_STORE = json.dumps([
    {'player': 'A', 'key': 'a', 'games': 3, 'scoring': [
        {'year': 2024, 'avg': 10.0, 'games': 2, 'pos': 'SD'},
        {'year': 2025, 'avg': 12.0, 'games': 1, 'pos': 'SD'}], '_has26': False, '_retired': False,
     'afl_club': 'X', '_bd': '2000-01-01', 'affl_team': 'T'},
    {'player': 'B', 'key': 'b', 'games': 0, 'scoring': [], '_has26': False, '_retired': True,
     '_bd': '2000-01-02'},
    {'player': 'C', 'key': 'c', 'games': 5, 'scoring': [
        {'year': 2022, 'avg': 20.0, 'games': 5, 'pos': 'MID'}], '_has26': False, '_retired': True,
     '_bd': '2000-01-03', '_last_listed': 2024},
    {'player': 'D', 'key': 'd', 'games': 7, 'scoring': [
        {'year': 2024, 'avg': 30.0, 'games': 4, 'pos': 'SF'},
        {'year': 2026, 'avg': 31.0, 'games': 3, 'pos': 'SF'}], '_has26': True, '_retired': False,
     'afl_club': 'Y', '_bd': '2000-01-04', 'affl_team': 'U'},
])
S26 = {'year': 2026, 'avg': 0.0, 'games': 0, 'pos': 'MID'}


def _others_identical(before, after, keys):
    sb, sa = ST.store_row_spans(before, keys), ST.store_row_spans(after, keys)
    return all(before[sb[k][0]:sb[k][1]] == after[sa[k][0]:sa[k][1]] for k in keys)


def season_add():
    print('\nSTORE-EDIT SEASON ADD\n  ' + '-' * 70)
    before = json.loads(SEASON_STORE)
    c0 = [r for r in before if r['key'] == 'c'][0]

    # ---- the happy path: the un-retire shape, a 2026 season on a row whose last season is 2022 --
    out, ap = ST.apply_store_edits(SEASON_STORE, [{'key': 'c', 'field': 'scoring[2026]', 'add': S26}])
    r = _row(out, 'c')
    ok(r == dict(c0, scoring=c0['scoring'] + [S26]),
       'the row re-parses as the ORIGINAL dict plus the one new season, at the end of the list')
    ok(len(ap) == 1 and ap[0]['kind'] == 'add_season' and ap[0]['old'] is None and ap[0]['new'] == S26
       and ap[0]['old_text'] == '' and ap[0]['field'] == 'scoring[2026]',
       'applied records {kind: add_season, old: None, new: season} with an EMPTY old_text')
    ok(ap[0]['new_text'] == ', {"year": 2026, "avg": 0.0, "games": 0, "pos": "MID"}',
       'the inserted bytes are the file\'s own separator + the season in the file\'s key order (%r)'
       % ap[0]['new_text'])
    ok(ap[0]['anchor'] == 'after season 2022, as the LAST season' and ap[0]['exemplars'] == 5,
       'the record names the position (after 2022, last) and the %d season objects measured'
       % ap[0]['exemplars'])
    ok(_reversed(out, ap) == SEASON_STORE,
       'removing the inserted text reproduces the input CHARACTER FOR CHARACTER')
    ok(_others_identical(SEASON_STORE, out, ['a', 'b', 'd']), 'every other row\'s text is byte-identical')
    ok(len(ST.store_row_spans(out)) == len(before), 'the row count is unmoved')

    # ---- YEAR ORDER, not "at the end": before the first, in the middle ------------------------
    out2, ap2 = ST.apply_store_edits(SEASON_STORE, [{'key': 'a', 'field': 'scoring[2023]',
                                                     'add': dict(S26, year=2023)}])
    ok([s['year'] for s in _row(out2, 'a')['scoring']] == [2023, 2024, 2025]
       and ap2[0]['new_text'].endswith('}, ') and ap2[0]['anchor'].startswith('as the FIRST season'),
       'a season EARLIER than every season the row has goes FIRST, separator after it (%r)'
       % ap2[0]['anchor'])
    ok(_reversed(out2, ap2) == SEASON_STORE, '...and its reversal holds')
    out3, ap3 = ST.apply_store_edits(SEASON_STORE, [{'key': 'd', 'field': 'scoring[2025]',
                                                     'add': dict(S26, year=2025, pos='SF')}])
    ok([s['year'] for s in _row(out3, 'd')['scoring']] == [2024, 2025, 2026]
       and ap3[0]['anchor'] == 'after season 2024 (before 2026)',
       'a season BETWEEN two the row has goes between them, in year order (%r)' % ap3[0]['anchor'])
    ok(_reversed(out3, ap3) == SEASON_STORE, '...and its reversal holds')

    # ---- KEY ORDER is the file's, whatever order the spec wrote the object in ------------------
    scrambled = {'pos': 'MID', 'games': 0, 'year': 2026, 'avg': 0.0}
    out4, ap4 = ST.apply_store_edits(SEASON_STORE, [{'key': 'c', 'field': 'scoring[2026]',
                                                     'add': scrambled}])
    ok(list(_row(out4, 'c')['scoring'][-1]) == ['year', 'avg', 'games', 'pos']
       and ap4[0]['new_text'] == ap[0]['new_text'],
       'a season declared in another key order is WRITTEN in the file\'s (year, avg, games, pos)')

    # ---- an EMPTY scoring list (the Mirkov shape) takes the object with no separator -------------
    out5, ap5 = ST.apply_store_edits(SEASON_STORE, [{'key': 'b', 'field': 'scoring[2026]',
                                                     'add': dict(S26, pos='RUCK')}])
    ok(_row(out5, 'b')['scoring'] == [dict(S26, pos='RUCK')]
       and ap5[0]['new_text'] == '{"year": 2026, "avg": 0.0, "games": 0, "pos": "RUCK"}'
       and ap5[0]['anchor'] == 'into an EMPTY scoring list',
       'an empty `scoring: []` takes the bare object — no separator to copy, none written')
    ok(_reversed(out5, ap5) == SEASON_STORE, '...and its reversal holds')

    # ---- THE REFUSALS ----------------------------------------------------------------------------
    got, why = refuses([{'key': 'a', 'field': 'scoring[2025]', 'add': dict(S26, year=2025)}],
                       SEASON_STORE, 'ALREADY ON THE ROW')
    ok(got, 'a season the row CARRIES is refused — an add never overwrites  (%s)' % why)
    try:
        ST.apply_store_edits(SEASON_STORE, [{'key': 'a', 'field': 'scoring[2025]',
                                             'add': dict(S26, year=2025)}])
        msg = ''
    except StepError as exc:
        msg = str(exc)
    ok('row    : a' in msg and 'season : 2025' in msg and '"games": 1' in msg,
       '...and the refusal names the row, the season and the object it carries')

    got, why = refuses([{'key': 'c', 'field': 'scoring[2026]',
                         'add': {'year': 2026, 'avg': 0.0, 'games': 0}}], SEASON_STORE, 'carries keys')
    ok(got, 'a season MISSING a key the file\'s seasons carry (`pos`) is refused  (%s)' % why)
    got, why = refuses([{'key': 'c', 'field': 'scoring[2026]', 'add': dict(S26, extra=1)}],
                       SEASON_STORE, 'carries keys')
    ok(got, 'a season with an EXTRA key is refused — the key set is the file\'s, exactly')
    got, why = refuses([{'key': 'c', 'field': 'scoring[2026]', 'add': dict(S26, year=2025)}],
                       SEASON_STORE, 'must agree')
    ok(got, 'a `year` that is not the Y in the field path is refused')
    got, why = refuses([{'key': 'c', 'field': 'scoring[2026]', 'add': 2026}], SEASON_STORE, 'OBJECT')
    ok(got, 'a scalar under `scoring[Y]` is refused — the season add takes the object')
    got, why = refuses([{'key': 'x-exemplar', 'field': 'scoring[2026]', 'add': {'year': 2026,
                                                                                'games': 0}}],
                       ADD_STORE, 'no `scoring` list')
    ok(got, 'a row with no `scoring` list is refused — the lane adds a season, never the list')
    got, why = refuses([{'key': 'c', 'field': 'scoring[2026].games', 'add': 0}], SEASON_STORE,
                       'flat')
    ok(got, 'a field INSIDE a season (`scoring[Y].x`) is still refused under add  (%s)' % why)
    got, why = refuses([{'key': 'c', 'field': 'scoring[2026]', 'add': S26},
                        {'key': 'c', 'field': 'scoring[2026]', 'add': S26}],
                       SEASON_STORE, 'ALREADY ON THE ROW')
    ok(got, 'a second add of the same season to the same row aborts on the first one\'s output')

    # a file whose seasons disagree on key order has no shape to copy
    dis = json.dumps([{'key': 'a', 'scoring': [{'year': 2024, 'games': 1}]},
                      {'key': 'b', 'scoring': [{'games': 1, 'year': 2024}]}])
    got, why = refuses([{'key': 'a', 'field': 'scoring[2026]', 'add': {'year': 2026, 'games': 0}}],
                       dis, 'do not share one key order')
    ok(got, 'season objects that DISAGREE on key order refuse the add — no shape to copy  (%s)' % why)
    # a row whose years are out of order has no position that keeps the order
    ooo = json.dumps([{'key': 'a', 'scoring': [{'year': 2025, 'games': 1}, {'year': 2024, 'games': 1}]}])
    got, why = refuses([{'key': 'a', 'field': 'scoring[2026]', 'add': {'year': 2026, 'games': 0}}],
                       ooo, 'out of year order')
    ok(got, 'a row carrying its seasons OUT of year order is refused rather than appended to')

    # ---- MIXED: the un-retire shape (season add + flat change) on one row, with a flat add ------
    out6, ap6 = ST.apply_store_edits(SEASON_STORE, [
        {'key': 'c', 'field': 'scoring[2026]', 'add': S26},
        {'key': 'c', 'field': '_retired', 'old': True, 'new': False},
        {'key': 'c', 'field': 'games', 'old': 5, 'new': 6},
        {'key': 'b', 'field': '_last_listed', 'add': 2025}])
    r6 = _row(out6, 'c')
    ok(r6 == dict(c0, scoring=c0['scoring'] + [S26], _retired=False, games=6)
       and _row(out6, 'b')['_last_listed'] == 2025
       and [a['kind'] for a in ap6] == ['add_season', 'change', 'change', 'add'],
       'season add + two changes on one row + a flat add on another: all land, each with its kind')
    ok(_reversed(out6, ap6) == SEASON_STORE, '...and reversing all four reproduces the input')

    # ---- the post-write re-read resolves a season add by its year ------------------------------
    spans = ST.store_row_spans(out6)
    yr = int(ST._SEASON_ADD_FIELD.match(ap6[0]['field']).group(1))
    srows = [x for x in spans['c'][2]['scoring'] if x.get('year') == yr]
    ok(len(srows) == 1 and srows[0] == ap6[0]['new'],
       'the step\'s re-read finds exactly one season for the added year, equal to the record')


def row_add():
    print('\nSTORE-EDIT ADD ROW\n  ' + '-' * 70)
    before = json.loads(SEASON_STORE)
    shape = ST._row_shape(SEASON_STORE)
    ok(shape['required'] == {'player', 'key', 'games', 'scoring', '_has26', '_retired', '_bd'}
       and shape['allowed'] == shape['required'] | {'afl_club', 'affl_team', '_last_listed'}
       and shape['sep'] == ', ',
       'the row shape is MEASURED: required = every row\'s keys, allowed = any row\'s, separator `, `')

    # ---- the happy path: a full-shape row, declared in a scrambled order -----------------------
    new_row = {'affl_team': 'V', '_bd': '2007-01-01', 'scoring': [], 'key': 'e', '_retired': False,
               'afl_club': 'Z', 'games': 0, 'player': 'E', '_has26': False}
    out, ap = ST.apply_store_edits(SEASON_STORE, [{'add_row': new_row}])
    r = _row(out, 'e')
    ok(r == new_row, 'the store re-parses with the new row, equal to the declared one')
    ok(list(r) == ['player', 'key', 'games', 'scoring', '_has26', '_retired', 'afl_club', '_bd',
                   'affl_team'],
       'the row is WRITTEN in the order the majority of rows use for those keys (declared scrambled)')
    ok(len(ap) == 1 and ap[0]['kind'] == 'add_row' and ap[0]['key'] == 'e' and ap[0]['old'] is None
       and ap[0]['old_text'] == '' and ap[0]['field'] is None and ap[0]['exemplars'] == 2
       and ap[0]['order'] == list(r),
       'applied records {kind: add_row, key, old: None, new: row, order, exemplars: 2} — the two '
       'rows (a, d) that use exactly this order')
    ok(ap[0]['new_text'] == ', ' + json.dumps({k: new_row[k] for k in ap[0]['order']})
       and out[ap[0]['at'] - 1] == '}' and out[ap[0]['at'] + len(ap[0]['new_text']):] == ']',
       'the inserted bytes are `, ` + the row, placed after the LAST row and before the closing `]`')
    ok(_reversed(out, ap) == SEASON_STORE,
       'removing the inserted text reproduces the input CHARACTER FOR CHARACTER')
    ok(_others_identical(SEASON_STORE, out, ['a', 'b', 'c', 'd']),
       'every existing row\'s text is byte-identical')
    ok(len(ST.store_row_spans(out)) == len(before) + 1 and json.loads(out)[:-1] == before,
       'the row count moved by exactly ONE and the existing rows parse unchanged, in order')
    ok(json.dumps(json.loads(out)) == out,
       'the file is still json.dumps-identical to its parse (the courier\'s P8 still holds)')

    # ---- the required set alone, and a season inside the new row in the file's key order --------
    req_row = {'player': 'F', 'key': 'f', 'games': 0, '_bd': '2007-02-02', '_has26': False,
               '_retired': False, 'scoring': [{'pos': 'KPD', 'games': 0, 'avg': 0.0, 'year': 2026}]}
    out2, ap2 = ST.apply_store_edits(SEASON_STORE, [{'add_row': req_row}])
    r2 = _row(out2, 'f')
    ok(list(r2) == ['player', 'key', 'games', 'scoring', '_has26', '_retired', '_bd']
       and ap2[0]['exemplars'] == 1,
       'a row carrying exactly the REQUIRED keys takes their majority order (1 exemplar, b)')
    ok(list(r2['scoring'][0]) == ['year', 'avg', 'games', 'pos'] and r2['scoring'][0] == req_row['scoring'][0],
       'a season inside the new row is written in the file\'s season key order')
    ok(_reversed(out2, ap2) == SEASON_STORE, '...and the reversal holds')

    # ---- THE REFUSALS ----------------------------------------------------------------------------
    got, why = refuses([{'add_row': dict(req_row, key='a')}], SEASON_STORE, 'ALREADY IN THE STORE')
    ok(got, 'a key the store CARRIES is refused — the lane never writes "the second one"  (%s)' % why)
    got, why = refuses([{'add_row': dict(req_row, _zzz=1)}], SEASON_STORE, 'NO store row carries')
    ok(got, 'an UNKNOWN key (one no row carries) is refused  (%s)' % why)
    missing = dict(req_row)
    del missing['_bd']
    got, why = refuses([{'add_row': missing}], SEASON_STORE, 'lacks')
    ok(got, 'a MISSING required key (one every row carries) is refused  (%s)' % why)
    got, why = refuses([{'add_row': req_row, 'key': 'f'}], SEASON_STORE, 'verb of its own')
    ok(got, 'an entry that carries `add_row` AND anything else is refused — one entry, one verb')
    nokey = dict(req_row)
    del nokey['key']
    got, why = refuses([{'add_row': nokey}], SEASON_STORE, 'non-empty string')
    ok(got, 'a row without `key` is refused before anything else is measured  (%s)' % why)
    got, why = refuses([{'add_row': dict(req_row, key='')}], SEASON_STORE, 'non-empty string')
    ok(got, 'an empty `key` is refused')
    got, why = refuses([{'add_row': dict(req_row, scoring=[{'year': 2026, 'games': 0}])}],
                       SEASON_STORE, 'seasons carry')
    ok(got, 'a season inside the new row with the WRONG key set is refused')
    got, why = refuses([{'add_row': dict(req_row, scoring=[dict(S26, year=2026), dict(S26, year=2024)])}],
                       SEASON_STORE, 'ascending year order')
    ok(got, 'seasons inside the new row out of year order are refused')
    nomaj = json.dumps([{'key': 'a', 'q': 1}, {'key': 'b', 'r': 1}])
    got, why = refuses([{'add_row': {'key': 'c', 'q': 1, 'r': 1, 'scoring': []}}], nomaj,
                       'NO store row carries')
    ok(got, 'a store with no `scoring` on any row refuses a row that carries it (unknown key)')
    nomaj2 = json.dumps([{'key': 'a', 'q': 1, 'scoring': []}, {'key': 'b', 'r': 1, 'scoring': []}])
    got, why = refuses([{'add_row': {'key': 'c', 'q': 1, 'r': 1, 'scoring': []}}], nomaj2,
                       'no majority order')
    ok(got, 'two keys NO row has ever carried together have no majority order — refused, not '
            'guessed  (%s)' % why)
    got, why = refuses([{'add_row': req_row}, {'add_row': req_row}], SEASON_STORE,
                       'ALREADY IN THE STORE')
    ok(got, 'a second add_row with the same key aborts on the first one\'s output')

    # ---- TWO rows in one list, and a FULLY MIXED list --------------------------------------------
    out3, ap3 = ST.apply_store_edits(SEASON_STORE, [{'add_row': new_row}, {'add_row': req_row}])
    ok([r['key'] for r in json.loads(out3)] == ['a', 'b', 'c', 'd', 'e', 'f']
       and _reversed(out3, ap3) == SEASON_STORE,
       'two add_rows land in order at the end, and reversing both reproduces the input')
    c0 = [r for r in before if r['key'] == 'c'][0]
    out4, ap4 = ST.apply_store_edits(SEASON_STORE, [
        {'key': 'c', 'field': 'scoring[2026]', 'add': S26},
        {'key': 'c', 'field': '_retired', 'old': True, 'new': False},
        {'add_row': new_row},
        {'key': 'b', 'field': '_last_listed', 'add': 2025},
        {'add_row': req_row},
        {'key': 'a', 'field': 'scoring[2025].games', 'old': 1, 'new': 2}])
    ok([a['kind'] for a in ap4] == ['add_season', 'change', 'add_row', 'add', 'add_row', 'change']
       and _row(out4, 'c') == dict(c0, scoring=c0['scoring'] + [S26], _retired=False)
       and _row(out4, 'e') == new_row and _row(out4, 'f') == req_row
       and _row(out4, 'b')['_last_listed'] == 2025 and _row(out4, 'a')['scoring'][1]['games'] == 2
       and len(ST.store_row_spans(out4)) == len(before) + 2,
       'all FOUR verbs in one list (season add, change, row add, flat add, row add, season change) '
       'land, the row count moving by exactly the two add_rows')
    ok(_reversed(out4, ap4) == SEASON_STORE, '...and reversing all six reproduces the input')
    ok(sum(1 for a in ap4 if a['kind'] == 'add_row') == 2,
       'the step\'s row-count tolerance is the number of add_row records (2 here)')

    # ---- the movers assertion orders an APPEARANCE (before: None) against numbers ---------------
    trip = [('z', 3, 4), ('e', None, 120), ('a', 5, None)]
    ok(sorted(trip, key=ST._mover_key) == sorted(trip, key=ST._mover_key)
       and [t[0] for t in sorted(trip, key=ST._mover_key)] == ['a', 'e', 'z'],
       'expected_movers with `before: None` (an appearance) sorts against numeric movers without a '
       'TypeError')
    import tempfile
    d = tempfile.mkdtemp()
    b0, b1 = os.path.join(d, 'b0.json'), os.path.join(d, 'b1.json')
    json.dump({'active': [{'key': 'a', 'v': 10, 'name': 'A'}], 'back': [{'key': 'c', 'v': 1, 'name': 'C'}]},
              open(b0, 'w'))
    json.dump({'active': [{'key': 'a', 'v': 10, 'name': 'A'}, {'key': 'e', 'v': 120, 'name': 'E'}],
               'back': [{'key': 'c', 'v': 1, 'name': 'C'}]}, open(b1, 'w'))
    movers, facts = ST.board_movers(b0, b1)
    ok(movers == [{'key': 'e', 'name': 'E', 'section': 'active', 'before': None, 'after': 120,
                   'delta': None}] and facts['rows_added'] == ['e'],
       'an added row that becomes ACTIVE is measured as an appearance in the ACTIVE section '
       '(before None), as a back-section appearance already was')


def season_and_row_spec():
    print('\nSTORE-EDIT SEASON ADD + ADD ROW — spec validation\n  ' + '-' * 70)

    def problems(*entries):
        return [b for b in SPEC._validate_edit({'edit': {'store': list(entries)},
                                                'identities': {'moves': ['store']}})
                if 'edit.store' in b]

    ok(problems({'key': 'c', 'field': 'scoring[2026]', 'add': S26}) == [],
       'a well-formed season add validates')
    ok(any('year' in b for b in problems({'key': 'c', 'field': 'scoring[2026]',
                                          'add': dict(S26, year=2025)})),
       'a season whose `year` is not the Y in the path is refused by the validator')
    ok(any('OBJECT' in b for b in problems({'key': 'c', 'field': 'scoring[2026]', 'add': 0})),
       'a scalar under `scoring[Y]` is refused by the validator')
    ok(any('scalar' in b for b in problems({'key': 'c', 'field': 'scoring[2026]',
                                            'add': dict(S26, pos=['MID'])})),
       'a season carrying a container value is refused by the validator')
    ok(any('flat' in b.lower() for b in problems({'key': 'c', 'field': 'scoring[2026].games', 'add': 0})),
       'a field INSIDE a season under add is still refused by the validator')
    ok(problems({'add_row': {'key': 'x', 'scoring': [], 'player': 'X'}}) == [],
       'a well-formed add_row validates')
    ok(any('one verb' in b for b in problems({'add_row': {'key': 'x', 'scoring': []}, 'key': 'x'})),
       'add_row beside any other slot is refused by the validator')
    ok(any('`key`' in b for b in problems({'add_row': {'scoring': []}})),
       'add_row without a key is refused by the validator')
    ok(any('scoring' in b for b in problems({'add_row': {'key': 'x'}})),
       'add_row without a scoring list is refused by the validator')
    ok(any('OBJECT' in b for b in problems({'add_row': 'x'})),
       'add_row that is not an object is refused by the validator')
    ok(any('twice' in b for b in problems({'add_row': {'key': 'x', 'scoring': []}},
                                          {'add_row': {'key': 'x', 'scoring': []}})),
       'the same key added twice is refused by the validator')
    ok(problems({'add_row': {'key': 'x', 'scoring': []}},
                {'key': 'x', 'field': 'games', 'old': 1, 'new': 2}) == [],
       'an add_row and a change to another slot of the same key are two entries (the change\'s '
       '`old` is asserted at apply time against the row the add_row wrote)')


def season_and_row_live():
    """Against the REAL store when it is present: the measured shapes, and the two owner rows."""
    path = os.path.join(ROOT, ST.STORE_REL)
    if not os.path.isfile(path):
        return
    print('\nSTORE-EDIT SEASON ADD + ADD ROW — the live store\n  ' + '-' * 70)
    text = open(path, 'rb').read().decode('utf-8')
    rows = json.loads(text)
    n_seasons = sum(len(r.get('scoring') or []) for r in rows)
    sshape = ST._season_shape(text)
    ok(sshape == {'keys': ['year', 'avg', 'games', 'pos'], 'sep': ', ', 'objects': n_seasons},
       'the live season shape is `year, avg, games, pos`, separated by `, `, on all %d objects'
       % n_seasons)
    ok(all([s['year'] for s in r.get('scoring') or []] == sorted(s['year'] for s in r.get('scoring') or [])
           for r in rows), 'every live row carries its seasons in ascending year order')
    rshape = ST._row_shape(text)
    req = set.intersection(*[set(r) for r in rows])
    allw = set.union(*[set(r) for r in rows])
    ok(rshape['required'] == req and rshape['allowed'] == allw and rshape['sep'] == ', '
       and len(req) == 19 and len(allw) == 31,
       'the live row shape: %d required keys, %d allowed, rows separated by `, `' % (len(req), len(allw)))
    ok(ST._row_order(rshape, sorted(req)) == [
        'player', 'pick', 'year', 'type', 'drafted_position', 'present_position', 'key', 'games',
        'scoring', '_has26', '_retired', '_by', '_cat', '_draft', '_draft_club', '_pickless',
        'future_position', 'draft_stream', 'stream_year'],
       'the majority order of the 19 required keys is the writer order every row starts with')
    full = sorted(allw - {'_force_active', '_last_listed', '_pick_source', 'pick_correction_note'})
    ok(ST._row_order(rshape, full) == [
        'player', 'pick', 'year', 'type', 'drafted_position', 'present_position', 'key', 'games',
        'scoring', '_has26', '_retired', '_by', '_cat', '_draft', '_draft_club', 'afl_club',
        '_pickless', '_bd', 'future_position', 'stable_player_id', 'affl_team', 'eligibilities',
        'alternate_position', 'p_dual_stream', 'draft_stream', 'stream_pick', 'stream_year'],
       'the majority order of the active-row key set is the 524-row writer order')

    # THE TWO OWNER ROWS: retired, no 2026 season, no afl_club/affl_team. Bedendo's last season is
    # 2022; Mirkov has never played (`scoring: []`). The un-retire is a season add + a flat change.
    targets = [r for r in rows if r['key'] in ('dominic-bedendo', 'alex-mirkov')]
    if len(targets) == 2 and all(r.get('_retired') and not any(s['year'] == 2026 for s in r['scoring'])
                                 for r in targets):
        edits = [{'key': 'dominic-bedendo', 'field': 'scoring[2026]',
                  'add': {'year': 2026, 'avg': 0.0, 'games': 0, 'pos': 'SF'}},
                 {'key': 'dominic-bedendo', 'field': '_retired', 'old': True, 'new': False},
                 {'key': 'alex-mirkov', 'field': 'scoring[2026]',
                  'add': {'year': 2026, 'avg': 0.0, 'games': 0, 'pos': 'RUCK'}},
                 {'key': 'alex-mirkov', 'field': '_retired', 'old': True, 'new': False}]
        out, ap = ST.apply_store_edits(text, edits)
        ok(ap[0]['anchor'] == 'after season 2022, as the LAST season'
           and ap[2]['anchor'] == 'into an EMPTY scoring list'
           and ap[0]['new_text'] == ', {"year": 2026, "avg": 0.0, "games": 0, "pos": "SF"}'
           and ap[2]['new_text'] == '{"year": 2026, "avg": 0.0, "games": 0, "pos": "RUCK"}',
           'Bedendo takes `, {season}` after 2022; Mirkov takes the bare object into `[]`')
        ok([s['year'] for s in _row(out, 'dominic-bedendo')['scoring']] == [2022, 2026]
           and _row(out, 'alex-mirkov')['scoring'][0]['year'] == 2026
           and not _row(out, 'dominic-bedendo')['_retired'] and not _row(out, 'alex-mirkov')['_retired'],
           '...both rows carry 2026 and read un-retired')
        ok(_reversed(out, ap) == text, '...and reversing all four reproduces the live store byte-for-byte')
        ok(len(ST.store_row_spans(out)) == len(rows), '...with the row count unmoved')
    # A NEW ROW of the required shape appends after the last live row, in the writer order.
    new_row = {k: None for k in req}
    new_row.update({'player': 'Test Rookie', 'key': 'test-rookie-zz', 'games': 0, 'year': 2026,
                    'scoring': [{'year': 2026, 'avg': 0.0, 'games': 0, 'pos': 'KPD'}], '_has26': False,
                    '_retired': False, 'type': 'RD', '_pickless': True, 'draft_stream': 'RD',
                    'stream_year': 2026})
    out2, ap2 = ST.apply_store_edits(text, [{'add_row': new_row}])
    ok(len(ST.store_row_spans(out2)) == len(rows) + 1 and json.loads(out2)[-1] == new_row
       and list(json.loads(out2)[-1]) == ST._row_order(rshape, sorted(req))
       and ap2[0]['exemplars'] > 0 and _reversed(out2, ap2) == text
       and json.dumps(json.loads(out2)) == out2,
       'a required-shape row appends as row %d in the writer order (%d live rows use it), reverses '
       'byte-exact, and the file stays json.dumps-identical' % (len(rows) + 1, ap2[0]['exemplars']))


if __name__ == '__main__':
    sys.exit(main())
