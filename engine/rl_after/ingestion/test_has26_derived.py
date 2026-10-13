#!/usr/bin/env python3
"""`_has26` IS DEAD AS A READ (Phase 0.4, 2026-10-13) — the two expressions, both ways, over every row.

The flag was set at the 2026-07-02 seed and never maintained: 179 of 2,650 rows carry a 2026 season
the flag does not admit. rl_model.py read it in two places; both now derive the truth from the
scoring rows. This file is the unit check that the board cannot have moved:

  * line ~1346, `active()`: `_has26 or any(year>=2024) or year>=2024` -> drop the flag. Identical for
    EVERY row, because the flag is a SUBSET of "has a 2026 row" (asserted here: 0 rows are flagged
    without one) and a 2026 row already satisfies year>=2024. Nothing is weakened, nothing widened.
  * line ~2256, `rk()`: a stdout name-lookup diagnostic for 16 hard-coded names; nothing downstream
    reads it. `_has26` -> "played a 2026 game" (the flag's meaning, derived). The two can differ on
    rows the stale flag misses (a 2026 debutant drafted before 2023); none of the 16 names is such a
    row, so the diagnostic's output is unchanged too — asserted here against the live store.

Run:  python3 engine/rl_after/ingestion/test_has26_derived.py    (also collected by unittest/pytest)
"""
import json
import os
import re
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
STORE = os.path.join(REPO, 'engine', 'rl_after', 'rl_model_data.json')
RL_MODEL = os.path.join(REPO, 'engine', 'rl_after', 'rl_model.py')

#: the 16 names rk() is called with (rl_model.py, the two `for nm in [...]` print loops)
RK_NAMES = ['Sullivan Robey', 'Sam Cumming', 'Jacob Farrow', 'Cooper Duff-Tytler', 'Harry Dean',
            'Zeke Uwland', 'Dylan Patterson', 'Harry Kyle', "Connor O'Sullivan",
            'Josh Worrell', 'Sam Collins', 'Willem Duursma', 'Nick Daicos', 'Dayne Zorko',
            'Finn Callaghan', 'Harry Sheezel']


def _norm(s):
    return re.sub(r'[^a-z]', '', str(s).lower())


def _has_row_2026(p):
    return any(r['year'] >= 2026 for r in p['scoring'])


def _played_2026(p):
    return any(r['year'] >= 2026 and (r.get('games') or 0) > 0 for r in p['scoring'])


class Has26Derived(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = json.load(open(STORE, encoding='utf-8'))
        cls.src = open(RL_MODEL, encoding='utf-8').read()

    def test_the_store_is_the_expected_size(self):
        self.assertEqual(len(self.rows), 2650)
        self.assertTrue(all('_has26' in p for p in self.rows))

    def test_the_flag_is_a_subset_of_has_a_2026_row(self):
        # the lemma the active() rewrite rests on: flagged => a 2026 row exists
        bad = [p['key'] for p in self.rows if p.get('_has26') and not _has_row_2026(p)]
        self.assertEqual(bad, [])

    def test_the_flag_is_stale_so_it_cannot_be_the_truth(self):
        stale = [p['key'] for p in self.rows if _has_row_2026(p) and not p.get('_has26')]
        self.assertGreater(len(stale), 0, 'the flag is maintained after all — reconsider')

    def test_active_recent_expression_identical_for_every_row(self):
        diffs = []
        for p in self.rows:
            old = bool(p.get('_has26') or any(r['year'] >= 2024 for r in p['scoring']) or p['year'] >= 2024)
            new = bool(any(r['year'] >= 2024 for r in p['scoring']) or p['year'] >= 2024)
            if old != new:
                diffs.append(p['key'])
        self.assertEqual(diffs, [])

    def test_rk_candidate_filter_identical_for_every_rk_name(self):
        # rk() filters `players` (the active list) by substring on the normalised name; the store
        # is a superset of that list, so identity over the store's matches implies identity there.
        matched = 0
        for nm in RK_NAMES:
            cands = [p for p in self.rows if _norm(nm) in _norm(p['player'])]
            # a name with NO store match (rk prints 'NF' either way) is trivially identical
            matched += bool(cands)
            for p in cands:
                old = bool(p.get('_has26') or p['year'] >= 2023 or p.get('_unplayed'))
                new = bool(_played_2026(p) or p['year'] >= 2023 or p.get('_unplayed'))
                self.assertEqual(old, new, '%s / %s' % (nm, p['key']))
        self.assertGreaterEqual(matched, 12, 'most rk() names must resolve, or this proves nothing')

    def test_rl_model_no_longer_reads_the_flag(self):
        reads = [ln for ln in self.src.splitlines() if '_has26' in ln and not ln.lstrip().startswith('#')]
        self.assertEqual(reads, [], reads)

    def test_rk_names_are_the_ones_in_rl_model(self):
        for nm in RK_NAMES:
            self.assertIn(nm.replace("'", "\\'") if "'" in nm else nm, self.src, nm)


if __name__ == '__main__':
    unittest.main(verbosity=2)
