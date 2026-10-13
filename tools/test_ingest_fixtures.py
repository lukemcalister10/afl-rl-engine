#!/usr/bin/env python3
"""THE FINALS FIXTURE IS WRITTEN BY THE WEEK THAT PLAYS IT (tools/ingest, 2026-10-13).

FW3, FW4 and the GF landed with `"clubs": []` in scores/fixtures.json because filling it was a hand
step. round_movers.fixture_clubs HALTS a finals report on an empty list, so the gap was a latent halt
for any later rebuild of those weeks' reports. The ingest now derives the week's sides from the
resolved list + the store (the same side count it already printed) and writes them. Proven here:

  * the side rule (more than SIDE_MIN_LISTED listed players at a store club) and the mover list;
  * the series-shape assertion (a week with the wrong number of sides is refused);
  * the writer: fills a blank week, preserves every other byte, no-ops on an identical re-run,
    refuses to overrule a hand-declared week, refuses an undeclared week, keeps the file's format;
  * the COMMITTED fixture for feed rounds 27, 28, 29 equals what the tool derives from the committed
    resolved files and the live store — the data and the writer agree, so this cannot recur unseen.

Run:  python3 tools/test_ingest_fixtures.py     (also collected by unittest / pytest)
"""
import io
import json
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import ingest as IG                                           # noqa: E402

STORE = [
    {'key': 'a1', 'afl_club': 'Fremantle'}, {'key': 'a2', 'afl_club': 'Fremantle'},
    {'key': 'a3', 'afl_club': 'Fremantle'}, {'key': 'a4', 'afl_club': 'Fremantle'},
    {'key': 'b1', 'afl_club': 'Brisbane'}, {'key': 'b2', 'afl_club': 'Brisbane'},
    {'key': 'b3', 'afl_club': 'Brisbane'}, {'key': 'b4', 'afl_club': 'Brisbane'},
    {'key': 'b5', 'afl_club': 'Brisbane'},
    {'key': 'm1', 'afl_club': 'Geelong'},            # a mover: store says Geelong, he played for one of the sides
    {'key': 'm2', 'afl_club': 'West Coast'},
    {'key': 'n1', 'afl_club': 'Carlton'}, {'key': 'n2', 'afl_club': 'Carlton'},
    {'key': 'n3', 'afl_club': 'Carlton'},            # exactly three: NOT a side
    {'key': 'z1', 'afl_club': 'Sydney'},             # not listed this week
]
LISTED = {'a1', 'a2', 'a3', 'a4', 'b1', 'b2', 'b3', 'b4', 'b5', 'm1', 'm2'}

FIXTURE = {
    '_doc': 'test — fixture', 'season': 2026,
    'weeks': {
        '25': {'label': 'FW1', 'clubs': ['Carlton', 'Collingwood', 'Melbourne', 'Western Bulldogs'],
               '_note': 'hand-declared'},
        '28': {'label': 'FW4', 'clubs': []},
        '29': {'label': 'GF', 'clubs': []},
    },
    '_shape': 'FW1 4 ... GF 2',
}


class SideRule(unittest.TestCase):
    def test_sides_are_clubs_with_more_than_three_listed(self):
        sides, movers = IG.fixture_clubs(LISTED, STORE, 29)
        self.assertEqual(sides, ['Brisbane', 'Fremantle'])
        self.assertEqual(movers, [('m1', 'Geelong'), ('m2', 'West Coast')])

    def test_exactly_three_is_not_a_side(self):
        sides, movers = IG.fixture_clubs(LISTED | {'n1', 'n2', 'n3'}, STORE, 29)
        self.assertEqual(sides, ['Brisbane', 'Fremantle'])
        self.assertIn(('n1', 'Carlton'), movers)

    def test_four_makes_a_side_and_the_shape_then_refuses_it(self):
        store = STORE + [{'key': 'n4', 'afl_club': 'Carlton'}]
        with self.assertRaises(ValueError) as cm:
            IG.fixture_clubs(LISTED | {'n1', 'n2', 'n3', 'n4'}, store, 29)
        self.assertIn('fields 2 clubs', str(cm.exception))
        self.assertIn('Carlton', str(cm.exception))
        # ...and the same listing is a legitimate FW3/FW4-shaped week? No: 3 sides != 4. Refused too.
        with self.assertRaises(ValueError):
            IG.fixture_clubs(LISTED | {'n1', 'n2', 'n3', 'n4'}, store, 27)

    def test_a_round_without_a_declared_shape_is_not_asserted(self):
        sides, _ = IG.fixture_clubs(LISTED, STORE, 24)
        self.assertEqual(sides, ['Brisbane', 'Fremantle'])

    def test_the_shape_is_the_owners(self):
        self.assertEqual(IG.FINALS_SIDES, {25: 4, 26: 8, 27: 4, 28: 4, 29: 2})
        self.assertEqual(IG.SIDE_MIN_LISTED, 3)


class Writer(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='ingest_fx_')
        self.path = os.path.join(self.tmp, 'fixtures.json')
        io.open(self.path, 'w', encoding='utf-8').write(json.dumps(FIXTURE, indent=1))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _doc(self):
        return json.loads(io.open(self.path, encoding='utf-8').read())

    def test_fills_a_blank_week_and_preserves_everything_else(self):
        before = self._doc()
        moved = IG.write_fixture_clubs(self.path, 29, ['Brisbane', 'Fremantle'],
                                       [('m1', 'Geelong')], 'scores/resolved/2026_GF.json')
        self.assertTrue(moved)
        after = self._doc()
        self.assertEqual(after['weeks']['29']['clubs'], ['Brisbane', 'Fremantle'])
        self.assertIn('m1 (store: Geelong)', after['weeks']['29']['_note'])
        self.assertIn('scores/resolved/2026_GF.json', after['weeks']['29']['_note'])
        self.assertEqual(list(after['weeks']['29']), ['label', 'clubs', '_note'])   # the FW1/FW2 key order
        for k in before:
            if k != 'weeks':
                self.assertEqual(before[k], after[k])
        for w in ('25', '28'):
            self.assertEqual(before['weeks'][w], after['weeks'][w])

    def test_format_is_the_files_own(self):
        IG.write_fixture_clubs(self.path, 29, ['Brisbane', 'Fremantle'], [], 'r')
        raw = io.open(self.path, encoding='utf-8').read()
        self.assertEqual(raw, json.dumps(json.loads(raw), indent=1))      # indent=1, no trailing newline
        self.assertIn('\\u2014', raw)                                      # ASCII-escaped, as shipped

    def test_rerun_with_the_same_clubs_is_a_no_op(self):
        IG.write_fixture_clubs(self.path, 29, ['Brisbane', 'Fremantle'], [], 'r')
        raw1 = io.open(self.path, encoding='utf-8').read()
        self.assertFalse(IG.write_fixture_clubs(self.path, 29, ['Fremantle', 'Brisbane'], [], 'r'))
        self.assertEqual(io.open(self.path, encoding='utf-8').read(), raw1)

    def test_never_overrules_a_hand_declared_week(self):
        raw0 = io.open(self.path, encoding='utf-8').read()
        with self.assertRaises(ValueError) as cm:
            IG.write_fixture_clubs(self.path, 25, ['Brisbane', 'Fremantle', 'Geelong', 'Sydney'], [], 'r')
        self.assertIn('never overruled', str(cm.exception))
        self.assertEqual(io.open(self.path, encoding='utf-8').read(), raw0)

    def test_refuses_an_undeclared_week(self):
        with self.assertRaises(ValueError) as cm:
            IG.write_fixture_clubs(self.path, 27, ['Brisbane', 'Fremantle'], [], 'r')
        self.assertIn('not declared', str(cm.exception))

    def test_refuses_a_reformatted_file(self):
        io.open(self.path, 'w', encoding='utf-8').write(json.dumps(FIXTURE, indent=2))
        with self.assertRaises(ValueError):
            IG.write_fixture_clubs(self.path, 29, ['Brisbane', 'Fremantle'], [], 'r')


class CommittedFixtureAgreesWithTheTool(unittest.TestCase):
    """The shipped scores/fixtures.json for feed rounds 27-29 is what the tool derives today."""

    @classmethod
    def setUpClass(cls):
        cls.store = json.load(io.open(os.path.join(REPO, IG.STORE_REL), encoding='utf-8'))
        cls.fx = json.load(io.open(os.path.join(REPO, IG.FIXTURES_REL), encoding='utf-8'))

    def _check(self, label, feed):
        res = json.load(io.open(os.path.join(REPO, 'scores', 'resolved', '2026_%s.json' % label),
                                encoding='utf-8'))
        keys = {p['key'] for p in res['players']}
        sides, movers = IG.fixture_clubs(keys, self.store, feed)
        wk = self.fx['weeks'][str(feed)]
        self.assertEqual(sorted(wk['clubs']), sides, label)
        self.assertEqual(len(sides), IG.FINALS_SIDES[feed])
        for k, c in movers:
            self.assertIn('%s (store: %s)' % (k, c), wk.get('_note', ''), label)
        return sides, movers

    def test_fw3(self):
        sides, movers = self._check('FW3', 27)
        self.assertEqual(sides, ['Adelaide', 'Brisbane', 'Fremantle', 'Geelong'])

    def test_fw4(self):
        sides, movers = self._check('FW4', 28)
        self.assertEqual(sides, ['Brisbane', 'Fremantle', 'Hawthorn', 'Sydney'])

    def test_gf(self):
        sides, movers = self._check('GF', 29)
        self.assertEqual(sides, ['Brisbane', 'Fremantle'])

    def test_no_finals_week_is_blank(self):
        for feed in range(25, 30):
            self.assertTrue(self.fx['weeks'][str(feed)]['clubs'], feed)

    def test_the_shipped_file_round_trips(self):
        raw = io.open(os.path.join(REPO, IG.FIXTURES_REL), encoding='utf-8').read()
        self.assertEqual(raw, json.dumps(json.loads(raw), indent=1))


if __name__ == '__main__':
    unittest.main(verbosity=2)
