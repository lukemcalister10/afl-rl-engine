"""FAST unit test — catch-up preflight, identity overrides + participation classification (no board).

Runs in ~1s against the REAL store (READ-ONLY) + the owner's R15-R19 fixtures. Exercises the preflight
+ identity-override + FootyWire-parser paths only — it never stages or applies anything (no board is
generated, no file written). The heavy end-to-end apply is the catch-up proof
(session_2026-07-20/live_scoring_catchup/catchup_proof.py).

Run:  python3 engine/rl_after/ingestion/test_catchup_preflight.py     (or under pytest)
Exit 0 = PASS.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RA = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(RA))
sys.path.insert(0, HERE)
sys.path.insert(0, RA)

import footywire_parser as FW      # noqa: E402
import round_catchup as RC         # noqa: E402

FIX = os.path.join(REPO, 'session_2026-07-20', 'live_scoring_catchup', 'fixtures')
FILES = [(r, os.path.join(FIX, 'R%d.csv' % r)) for r in (15, 16, 17, 18, 19)]
EXPECT_LISTED = {15: 318, 16: 319, 17: 410, 18: 406, 19: 405}


def test_footywire_encodings_and_header():
    # CP1252 rounds and UTF-8 rounds both decode without error; the two-row header is stripped.
    for rnd, path in FILES:
        d = FW.parse_round_file(path)
        assert d['listed'] == EXPECT_LISTED[rnd], (rnd, d['listed'])
        assert d['encoding'] in ('cp1252', 'utf-8', 'utf-8-sig'), d['encoding']
        # header rows never leak in as data
        names = {n for n, _s in d['rows']}
        assert 'Player' not in names and '' not in names
    print("  test_footywire_encodings_and_header PASS")


def test_preflight_clean_with_overrides():
    cu = RC.RoundCatchup(REPO, FILES)
    report, rounds = cu.preflight()
    assert report['clean'], report['halt_reasons']
    assert set(report['identity_override_names']) == {'Callum Brown', 'Bailey Williams'}
    # no unresolved / ambiguous / duplicate anywhere
    for rd in report['rounds']:
        assert not rd['unresolved'] and not rd['ambiguous'] and not rd['duplicate_keys'], rd['round']
        assert rd['listed'] == EXPECT_LISTED[rd['round']]
    print("  test_preflight_clean_with_overrides PASS")


def test_bailey_williams_routed_by_stable_key():
    cu = RC.RoundCatchup(REPO, FILES)
    _report, rounds = cu.preflight()
    by_round = {rd['round']: rd for rd in rounds}
    # collect (round -> {key: score}) for the two Bailey Williams from the resolved rows
    got = {}
    for rd in rounds:
        for rr in rd['resolved_rows']:
            if rr.key in ('bailey-williams-wb', 'bailey-williams-wc'):
                got.setdefault(rd['round'], {})[rr.key] = rr.score
    assert got.get(16, {}).get('bailey-williams-wc') == 67
    assert got.get(17, {}).get('bailey-williams-wc') == 82
    assert got.get(18, {}).get('bailey-williams-wc') == 100
    assert got.get(18, {}).get('bailey-williams-wb') == 55
    assert got.get(19, {}).get('bailey-williams-wb') == 137
    assert got.get(19, {}).get('bailey-williams-wc') == 84
    # they never collapse: R18/R19 carry BOTH distinct keys
    assert set(got[18]) == {'bailey-williams-wb', 'bailey-williams-wc'}
    assert set(got[19]) == {'bailey-williams-wb', 'bailey-williams-wc'}
    print("  test_bailey_williams_routed_by_stable_key PASS")


def test_callum_brown_override_and_croft_zero():
    cu = RC.RoundCatchup(REPO, FILES)
    _report, rounds = cu.preflight()
    for rd in rounds:
        keys = {rr.key: rr.score for rr in rd['resolved_rows']}
        assert 'callum-brown-ire' in keys, ('callum missing', rd['round'])
    r19 = next(rd for rd in rounds if rd['round'] == 19)
    # Jordan Croft's legitimate played zero is preserved as a resolved row with score 0
    croft = [rr for rr in r19['resolved_rows'] if rr.key == 'jordan-croft']
    assert croft and croft[0].score == 0, "Croft R19 zero must be a resolved played score"
    assert r19['listed_zero'] == 1
    print("  test_callum_brown_override_and_croft_zero PASS")


def test_unmapped_override_is_unresolved():
    # a covered name with a (round, score) NOT in the owner map is treated as unresolved (halt), never
    # guessed — a crafted round proves the fail-closed behaviour.
    ov = RC.IdentityOverrides.load()
    key, kind = ov.resolve(16, 'Bailey Williams', 999)   # 999 not in the owner map for R16
    assert key is None and kind == 'unmapped', (key, kind)
    key2, kind2 = ov.resolve(15, 'Callum Brown', 45)     # map_all always resolves
    assert key2 == 'callum-brown-ire' and kind2 == 'map_all'
    print("  test_unmapped_override_is_unresolved PASS")


def main():
    tests = [test_footywire_encodings_and_header, test_preflight_clean_with_overrides,
             test_bailey_williams_routed_by_stable_key, test_callum_brown_override_and_croft_zero,
             test_unmapped_override_is_unresolved]
    print("catch-up preflight fast tests:")
    for t in tests:
        t()
    print("ALL CATCH-UP PREFLIGHT TESTS PASS")
    return 0


if __name__ == '__main__':
    sys.exit(main())
