#!/usr/bin/env python3
"""Unit test for engine/rl_after/survival_hazard.py — owner ruling SURVIVAL_H2_2026-10-14, capped; fix plan F1.

    python3 engine/rl_after/ingestion/test_survival_hazard.py     (exit 0 = all pass, exit 1 = a failure)

Light: no engine load. It (a) rebuilds S for a few synthetic (age, games, tenure) from the JSON coefficients by
hand and checks the module agrees, with pins against the fit script's own S grid; (b) checks the cohort rule
(integer ages, >= 33 pooled, < 5 charged rows joins the cohort below); (c) checks the capped application on a
synthetic active set — charged rows only, 0-game rows untouched and outside Sbar, no lifts, totals fall; (d) the
pure-H2 measurement variant is sum-preserving per cohort over the charged rows; and it checks the halts (missing
file, unformable age/games, 0-game row without type/year, another ruling id).
"""
import json
import math
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'engine', 'rl_after'))
os.environ.setdefault('RL_REPO', REPO)
import survival_hazard as SH  # noqa: E402

HZ = os.path.join(REPO, 'data', 'survival_hazard.json')
_fails = []
_n = [0]


def check(cond, label, detail=''):
    _n[0] += 1
    print('  [%s] %s%s' % ('PASS' if cond else 'FAIL', label, ('  ' + detail) if (detail and not cond) else ''))
    if not cond:
        _fails.append(label)


def _hand_S(doc, age, games, k, tenure=1):
    """Independent arithmetic: the design string, read literally, then the logistic; then the played-band
    monotone min (the 0-game band stands on its own value)."""
    coef = doc['coef']['S%d' % k]

    def raw(g, t=1):
        b = 0 if g == 0 else 1 if g <= 5 else 2 if g <= 20 else 3 if g <= 50 else 4 if g <= 100 else 5
        x = [1, min(age, 24) - 24, max(0, age - 24), max(0, age - 29), max(0, age - 33),
             1 if b == 0 else 0, 1 if (b == 0 and t >= 2) else 0,
             1 if b == 2 else 0, 1 if b == 3 else 0, 1 if b == 4 else 0, 1 if b == 5 else 0]
        return 1 / (1 + math.exp(-sum(a * c for a, c in zip(x, coef))))
    if games == 0:
        return raw(0, tenure)
    if games > 180:
        return raw(games)
    return min([raw(games)] + [raw(m) for m in (3, 12, 35, 75, 180) if m >= games])


def main():
    doc = SH.load(HZ)
    check(doc['ruling'] == 'SURVIVAL_H2_2026-10-14' and doc['cap_lift'] is True, 'calibration loads; ruling id and cap_lift=true recorded (owner ruling 2026-10-14: the lift is capped)')
    check(len(doc['coef']['S1']) == 11 and len(doc['coef']['S2']) == 11 and len(doc['coef_names']) == 11, 'two 11-coefficient vectors (band0 + band0 x tenure2+ added, F1)')
    check('on an AFL list at the END of season Y+k' in doc['outcome'] and '_last_listed' in doc['outcome'] and 'PROXY' in doc['outcome'],
          'the JSON states the fitted outcome (listed at the end of Y+k | listed at the end of Y), its sources and its proxies')
    check('ever0' not in doc, 'the ever0 intake table is gone (the 0-game band is fitted on the same outcome)')

    # (a) S from the coefficients, synthetic (age, games, tenure)
    cases = [(19, 3, 1), (22, 1, 1), (24, 46, 1), (27, 95, 1), (31, 143, 1), (35, 271, 1), (23, 250, 1), (20, 180, 1), (29, 51, 1),
             (19, 0, 1), (20, 0, 2), (23, 0, 1), (25, 0, 3)]
    ok = True
    for a, gm, t in cases:
        for k in (1, 2):
            want = _hand_S(doc, a, gm, k, t)
            yr = 2026 - t + 1 - 1          # tenure t = 2026 - debut + 1, debut = yr + 1 (ND)
            got = SH.survival_of({'key': 'x', 'age': a, 'games': gm, 'ty': 'ND', 'yr': yr}, k, doc, 2026)
            if abs(want - got) > 1e-12:
                ok = False; print('     S%d(%d,%d,t%d) module %.6f hand %.6f' % (k, a, gm, t, got, want))
    check(ok, '(a) S1/S2 on %d synthetic (age, games, tenure) equal the hand-built logistic from the JSON coefficients' % len(cases))
    # pins from the fit script's S grid (fit_survival_hazard.py; MEASURED_TABLES_F1.txt): age 20 g3 0.870/0.770,
    # age 24 g75 0.949/0.896, age 28 g180 0.927/0.829, age 35 g180 0.586/0.280, age 20 0-game tenure 2+ 0.491/0.397
    pins = [((20, 3, 1), (0.870, 0.770)), ((24, 75, 1), (0.949, 0.896)), ((28, 180, 1), (0.927, 0.829)), ((35, 180, 1), (0.586, 0.280)),
            ((20, 0, 2), (0.491, 0.397))]
    ok = all(round(SH.survival_of({'key': 'p', 'age': a, 'games': g, 'ty': 'ND', 'yr': 2026 - t}, k, doc, 2026), 3) == want[k - 1]
             for (a, g, t), want in pins for k in (1, 2))
    check(ok, '(a) five pins from the fit script\'s S grid reproduce to 3 dp')
    mono = all(SH.survival_of({'key': 'm', 'age': a, 'games': g1}, k, doc, 2026) <= SH.survival_of({'key': 'm', 'age': a, 'games': g2}, k, doc, 2026) + 1e-12
               for a in range(19, 37) for k in (1, 2) for g1, g2 in ((1, 6), (6, 21), (21, 51), (51, 101), (3, 300)))
    check(mono, '(a) S is monotone non-decreasing in evidence across the played bands at fixed age (the band-min rule)')
    aged = all(SH.survival_of({'key': 'm', 'age': a, 'games': 150}, k, doc, 2026) > SH.survival_of({'key': 'm', 'age': a + 1, 'games': 150}, k, doc, 2026)
               for a in range(24, 36) for k in (1, 2))
    check(aged, '(a) S falls with age past 24 at fixed evidence')
    # 0-game: own band by tenure; tenure 2+ below tenure 1 (the fitted term); MSD tenure counts the draft year
    z1 = SH.survival_of({'key': 'z', 'age': 19, 'games': 0, 'ty': 'ND', 'yr': 2025}, 1, doc, 2026)
    z2 = SH.survival_of({'key': 'z', 'age': 19, 'games': 0, 'ty': 'ND', 'yr': 2024}, 1, doc, 2026)
    m1 = SH.survival_of({'key': 'z', 'age': 19, 'games': 0, 'ty': 'MSD', 'yr': 2026}, 1, doc, 2026)
    m2 = SH.survival_of({'key': 'z', 'age': 19, 'games': 0, 'ty': 'MSD', 'yr': 2025}, 1, doc, 2026)
    check(z2 < z1 and m2 < m1 and abs(m1 - z1) < 1e-12 and SH.tenure_of('MSD', 2025, 2026) == 2 and SH.tenure_of('ND', 2025, 2026) == 1,
          '(a) 0-game rows: tenure 1 (ND drafted 2025 / MSD 2026) above tenure 2+ (ND 2024 / MSD 2025); MSD debuts in its draft year')
    check(abs(SH.survival_of({'key': 'z', 'age': 19, 'games': 0, 'ty': 'ND', 'yr': 2022}, 2, doc, 2026) - z2 * 0 - _hand_S(doc, 19, 0, 2, 5)) < 1e-12,
          '(a) tenure 5 is the same 2+ term (no third level)')

    # (b) the cohort rule
    coh = SH.cohorts_of({19: 30, 20: 40, 21: 3, 22: 50, 23: 50, 33: 10, 34: 4, 36: 1})
    check(coh[21] == coh[20] == '20-21' and coh[19] == '19' and coh[22] == '22' and coh[33] == coh[34] == coh[36] == '33+',
          '(b) an age with < 5 charged rows joins the cohort below; ages >= 33 pool into one', repr(coh))
    coh2 = SH.cohorts_of({18: 2, 19: 30, 20: 40, 33: 2, 34: 1})
    check(coh2[18] == coh2[19] == '18-19' and coh2[33] == coh2[34] == coh2[20] == '20+', '(b) a thin lowest age joins the first cohort above; a thin veteran pool joins the cohort below', repr(coh2))
    coh3 = SH.cohorts_of({24: 1})
    check(coh3 == {24: '24'}, '(b) a single thin age stands alone (nothing to join)', repr(coh3))

    # (c) the capped application on a synthetic set
    rows = []
    i = 0
    for a in (19, 21, 24, 27, 30, 33, 35):
        for gm, v in ((0, 400), (2, 650), (14, 1200), (40, 2300), (88, 4100), (210, 3000)):
            i += 1
            rows.append({'key': 'p%d' % i, 'age': a, 'games': gm, 'ty': 'ND', 'yr': 2026 - max(1, a - 18),
                         'vP1': v + 7 * i, 'vP2': v - 5 * i})
    perc, repc = SH.apply(rows, doc, 2026)          # the document default: capped
    check(repc['cap_lift'] is True and all(perc[r['key']]['m1'] <= 1.0 and perc[r['key']]['m2'] <= 1.0 for r in rows),
          '(c) document default is capped: every multiplier <= 1.0')
    check(all(t['after'] < t['before'] for t in repc['totals'].values()), '(c) capped totals fall (charges kept, no lifts)', repr(repc['totals']))
    zero = [r for r in rows if r['games'] == 0]
    check(all(perc[r['key']]['m1'] == 1.0 and perc[r['key']]['m2'] == 1.0 and perc[r['key']]['vP1'] == r['vP1'] and perc[r['key']]['vP2'] == r['vP2']
              and perc[r['key']]['charged'] is False for r in zero),
          '(c) 0-game rows are not charged: m=1, vP1/vP2 untouched, charged=False')
    check(all(perc[r['key']]['S1'] > 0 and perc[r['key']]['S2'] > 0 for r in zero), '(c) 0-game rows still report their fitted S1/S2')
    # Sbar excludes the 0-game rows: the value-weighted mean over the CHARGED rows of the cohort
    for k, fld in ((1, 'vP1'), (2, 'vP2')):
        a19 = [r for r in rows if r['age'] == 19 and r['games'] >= 1]
        want = sum(r[fld] * perc[r['key']]['S%d' % k] for r in a19) / sum(r[fld] for r in a19)
        check(abs(repc['sbar_by_cohort']['S%d' % k]['19']['sbar'] - want) < 1e-6 and repc['sbar_by_cohort']['S%d' % k]['19']['n_charged'] == 5
              and repc['sbar_by_cohort']['S%d' % k]['19']['n_zero_game'] == 1,
              '(c) Sbar_%d(19) is the %s-weighted mean of S%d over the 5 charged rows at 19 (the 0-game row outside it)' % (k, fld, k))
    check(all(abs(perc[r['key']]['m1'] - min(1.0, perc[r['key']]['S1'] / repc['sbar_by_cohort']['S1'][perc[r['key']]['cohort']]['sbar'])) < 1e-5
              for r in rows if r['games'] >= 1), '(c) m_k = min(1, S_k / Sbar_k(cohort)) on every charged row')
    check(repc['cohort_of_age']['33'] == '33+' and repc['cohort_of_age']['35'] == '33+' and perc['p37']['cohort'] == '33+'
          and set(repc['sbar_by_cohort']['S1']['33+']['ages']) == {33, 35},
          '(c) ages 33 and 35 share the pooled 33+ cohort and one Sbar')
    thin = perc['p2']; proven = perc['p5']  # age 19: (2 games) vs (88 games)
    check(thin['m1'] < 1.0 and thin['m2'] < 1.0 and proven['m1'] == 1.0 and proven['m2'] == 1.0, '(c) at one age the thin row is charged (m<1) and the proven row is held (m=1, no lift)')
    check(all(perc[r['key']][k2] is not None for r in rows for k2 in ('S1', 'S2', 'age', 'games', 'cohort', 'm1', 'm2')), '(c) per-row record carries S1,S2,age,games,cohort,charged,m1,m2')
    check(repc['source_md5'] and repc['ruling'] == 'SURVIVAL_H2_2026-10-14' and repc['nCharged'] == 35 and repc['nZeroGame'] == 7
          and 'not sum-preserving' in repc['law'] and repc['outcome'], '(c) report carries ruling, source md5, charged/0-game counts, the capped law, the outcome')

    # (d) the pure-H2 measurement variant: sum-preserving per cohort over the charged rows
    per, rep = SH.apply(rows, doc, 2026, cap_lift=False)
    ok = True
    for k in (1, 2):
        fld = 'vP%d' % k
        for c in set(per[r['key']]['cohort'] for r in rows if r['games'] >= 1):
            s = [r for r in rows if r['games'] >= 1 and per[r['key']]['cohort'] == c]
            before = sum(r[fld] for r in s); after = sum(per[r['key']][fld] for r in s)
            if abs(after - before) > 0.5 * len(s):
                ok = False; print('     cohort %s %s %d -> %d' % (c, fld, before, after))
    check(ok, '(d) cap_lift=False: per-cohort charged lens sums preserved to rounding (%d rows, 7 ages, both lenses)' % len(rows))
    check(rep['cap_lift'] is False and any(per[r['key']]['m1'] > 1.0 for r in rows) and all(per[r['key']]['m1'] == 1.0 for r in zero),
          '(d) uncapped carries lifts on charged rows; 0-game rows still m=1')
    check(all(perc[r['key']]['m1'] == min(1.0, per[r['key']]['m1']) for r in rows), '(d) capped m == min(1, uncapped m) row by row')
    saved = SH.CAP_LIFT
    try:
        SH.CAP_LIFT = None
        _, r0 = SH.apply(rows, doc, 2026)
        SH.CAP_LIFT = False
        _, r1 = SH.apply(rows, doc, 2026)
    finally:
        SH.CAP_LIFT = saved
    check(r0['cap_lift'] is True and r1['cap_lift'] is False, '(d) CAP_LIFT=None reads the document (true, capped); CAP_LIFT=False flips a measurement build to pure H2')

    # halts
    def raises(fn):
        try:
            fn()
        except SH.SurvivalHazardError as e:
            return str(e)
        return None
    check(raises(lambda: SH.load(os.path.join(tempfile.gettempdir(), 'no_such_survival_hazard.json'))) is not None, 'halt: absent calibration file')
    e = raises(lambda: SH.apply([{'key': 'bad-age', 'age': None, 'games': 10, 'vP1': 1, 'vP2': 1}], doc, 2026))
    check(e is not None and 'bad-age' in e, 'halt names the key: unformable age')
    e = raises(lambda: SH.apply([{'key': 'bad-games', 'age': 22, 'games': None, 'vP1': 1, 'vP2': 1}], doc, 2026))
    check(e is not None and 'bad-games' in e, 'halt names the key: unformable games')
    e = raises(lambda: SH.apply([{'key': 'bad-zero', 'age': 22, 'games': 0, 'ty': None, 'yr': 2025, 'vP1': 1, 'vP2': 1}], doc, 2026))
    check(e is not None and 'bad-zero' in e, 'halt names the key: 0-game row without type/year')
    with tempfile.TemporaryDirectory() as td:
        bad = dict(json.load(open(HZ))); bad['ruling'] = 'OTHER'
        p = os.path.join(td, 'h.json'); json.dump(bad, open(p, 'w'))
        check(raises(lambda: SH.load(p)) is not None, 'halt: a calibration carrying another ruling id')
        bad = dict(json.load(open(HZ))); bad['coef'] = {'S1': bad['coef']['S1'][:9], 'S2': bad['coef']['S2']}
        p = os.path.join(td, 'h9.json'); json.dump(bad, open(p, 'w'))
        check(raises(lambda: SH.load(p)) is not None, 'halt: a 9-coefficient (pre-F1) calibration')

    print('  ' + '-' * 66)
    if _fails:
        print('  %d FAILED: %s' % (len(_fails), _fails)); return 1
    print('SURVIVAL HAZARD TESTS: ALL %d PASS' % _n[0])
    return 0


if __name__ == '__main__':
    sys.exit(main())
