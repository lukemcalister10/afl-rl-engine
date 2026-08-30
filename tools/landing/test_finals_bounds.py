"""THE TWO NUMBERS THAT BOUND A FINALS WEEK, AND THE FACT THAT THEY LIVE IN TWO PLACES.

`tools/landing/spec.py` bounds what an ACT may declare; `round_movers` names the weeks and refuses
to label anything else. They are separate files because they answer to separate callers — the lander
must be able to refuse a spec without importing the engine — and separate files drift. So the
agreement is asserted rather than assumed, which is the whole of this module.

The lower bound (24) has been asserted since the calendar hold shipped. The upper bound (29) exists
because of a red the self-test caught on 2026-08-30: `min(n, 24)` reads EVERY feed round above the
home-and-away season as a finals week holding the calendar, so an act claiming round 99 described a
tree standing at 24 and passed its own postcondition. A bound with no ceiling is not a bound.
"""
import os
import sys
import unittest

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))

sys.path.insert(0, os.path.dirname(_HERE))
from landing.spec import HOME_AND_AWAY_ROUNDS, FINALS_FEED_CEILING, validate  # noqa: E402


def _round_movers():
    import importlib.util
    p = os.path.join(_ROOT, 'engine', 'rl_after', 'ingestion', 'round_movers.py')
    spec = importlib.util.spec_from_file_location('_rm_bounds', p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class FinalsBounds(unittest.TestCase):
    def test_the_two_files_agree_on_the_home_and_away_season(self):
        self.assertEqual(HOME_AND_AWAY_ROUNDS, _round_movers().HOME_AND_AWAY_ROUNDS)

    def test_the_ceiling_is_the_last_named_finals_week(self):
        names = _round_movers().FINALS_WEEK_NAMES
        self.assertEqual(FINALS_FEED_CEILING, max(names),
                         'the lander would accept a round the engine refuses to name')
        self.assertEqual(min(names), HOME_AND_AWAY_ROUNDS + 1,
                         'the first finals week must be the round after the season')
        self.assertEqual(sorted(names), list(range(HOME_AND_AWAY_ROUNDS + 1, FINALS_FEED_CEILING + 1)),
                         'the finals weeks must be contiguous — a gap is a week nobody can land')

    def test_every_named_week_gets_a_label_and_nothing_else_does(self):
        rm = _round_movers()
        for n in range(HOME_AND_AWAY_ROUNDS + 1, FINALS_FEED_CEILING + 1):
            self.assertTrue(rm.round_label(n).strip(), 'week %d has no name' % n)
        self.assertEqual(rm.round_label(HOME_AND_AWAY_ROUNDS), 'round %d' % HOME_AND_AWAY_ROUNDS)
        with self.assertRaises(ValueError):
            rm.round_label(FINALS_FEED_CEILING + 1)

    def test_the_calendar_hold_is_the_identity_below_the_season_and_a_hold_above_it(self):
        for n in (1, 12, HOME_AND_AWAY_ROUNDS):
            self.assertEqual(min(n, HOME_AND_AWAY_ROUNDS), n)
        for n in range(HOME_AND_AWAY_ROUNDS + 1, FINALS_FEED_CEILING + 1):
            self.assertEqual(min(n, HOME_AND_AWAY_ROUNDS), HOME_AND_AWAY_ROUNDS)


class SpecRefusesRoundsPastTheGrandFinal(unittest.TestCase):
    """The validator's half of the bound. `validate` collects problems rather than raising, so the
    assertion is on the TEXT of the problem it reports — a bound nobody can read is not a bound."""

    def _spec(self, number):
        return {
            'schema_version': 1, 'act_kind': 'round-advance',
            'round': {'number': number, 'scores': {'path': 'scores/X.csv', 'md5': 'x', 'sha256': 'y'},
                      'arming': {'env': {}, 'owner_word': 'test'}},
            'sheet': None,
        }

    def _problems(self, number):
        try:
            out = validate(self._spec(number))
        except Exception as exc:                              # a raise is also a refusal
            return [str(exc)]
        return [str(p) for p in (out or [])]

    def test_a_round_past_the_grand_final_is_refused_by_name(self):
        for bad in (FINALS_FEED_CEILING + 1, 99, 1000):
            hits = [p for p in self._problems(bad) if 'Grand Final' in p or 'feed round %d' % bad in p]
            self.assertTrue(hits, 'round %d was not refused for being past the season' % bad)

    def test_a_real_finals_week_is_not_refused_for_its_number(self):
        for ok in range(HOME_AND_AWAY_ROUNDS + 1, FINALS_FEED_CEILING + 1):
            hits = [p for p in self._problems(ok) if 'Grand Final' in p]
            self.assertFalse(hits, 'feed round %d was refused as past the season' % ok)


if __name__ == '__main__':
    unittest.main(verbosity=2)
