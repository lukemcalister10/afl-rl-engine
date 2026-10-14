#!/usr/bin/env python3
"""Unit test for engine/rl_after/survival_hazard.py — owner ruling SURVIVAL_H2_2026-10-14.

    python3 engine/rl_after/ingestion/test_survival_hazard.py     (exit 0 = all pass, exit 1 = a failure)

Light: no engine load. It (a) rebuilds S for a few synthetic (age, games) from the JSON coefficients by hand
and checks the module agrees; (b) checks sum-preservation per age on a synthetic active set; (c) checks the
cap_lift behaviour; and it checks the halts (missing file, unformable age/games).
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


def _hand_S(doc, age, games, k):
    """Independent arithmetic: the design string, read literally, then the logistic; then the band-monotone min."""
    coef = doc['coef']['S%d' % k]

    def raw(g):
        b = 0 if g <= 5 else 1 if g <= 20 else 2 if g <= 50 else 3 if g <= 100 else 4
        x = [1, min(age, 24) - 24, max(0, age - 24), max(0, age - 29), max(0, age - 33),
             1 if b == 1 else 0, 1 if b == 2 else 0, 1 if b == 3 else 0, 1 if b == 4 else 0]
        return 1 / (1 + math.exp(-sum(a * c for a, c in zip(x, coef))))
    g = max(1, games)
    if g > 180:
        return raw(g)
    return min([raw(g)] + [raw(m) for m in (3, 12, 35, 75, 180) if m >= g])


def main():
    doc = SH.load(HZ)
    check(doc['ruling'] == 'SURVIVAL_H2_2026-10-14' and doc['cap_lift'] is False, 'calibration loads; ruling id and cap_lift=false recorded')
    check(len(doc['coef']['S1']) == 9 and len(doc['coef']['S2']) == 9, 'two 9-coefficient vectors')

    # (a) S from the coefficients, synthetic (age, games)
    cases = [(19, 3), (22, 1), (24, 46), (27, 95), (31, 143), (35, 271), (23, 250), (20, 180), (29, 51)]
    ok = True
    for a, gm in cases:
        for k in (1, 2):
            want = _hand_S(doc, a, gm, k)
            got = SH.survival_of({'key': 'x', 'age': a, 'games': gm}, k, doc, 2026)
            if abs(want - got) > 1e-12:
                ok = False; print('     S%d(%d,%d) module %.6f hand %.6f' % (k, a, gm, got, want))
    check(ok, '(a) S1/S2 on %d synthetic (age, games) equal the hand-built logistic from the JSON coefficients' % len(cases))
    # pinned values from the scratch calibration (hazard_final_v2.json rows): nick-daicos (23,118) 0.9849/0.9709,
    # harry-sheezel (22,88) 0.9746/0.9500, luke-jackson (25,146) 0.9698/0.9368
    pins = [((23, 118), (0.9849, 0.9709)), ((22, 88), (0.9746, 0.9500)), ((25, 146), (0.9698, 0.9368))]
    ok = all(round(SH.survival_of({'key': 'p', 'age': a, 'games': g}, k, doc, 2026), 4) == want[k - 1]
             for (a, g), want in pins for k in (1, 2))
    check(ok, '(a) three scratch-calibration pins reproduce to 4 dp (daicos / sheezel / jackson)')
    mono = all(SH.survival_of({'key': 'm', 'age': a, 'games': g1}, k, doc, 2026) <= SH.survival_of({'key': 'm', 'age': a, 'games': g2}, k, doc, 2026) + 1e-12
               for a in range(19, 37) for k in (1, 2) for g1, g2 in ((1, 6), (6, 21), (21, 51), (51, 101), (3, 300)))
    check(mono, '(a) S is monotone non-decreasing in evidence at fixed age (the band-min rule)')
    aged = all(SH.survival_of({'key': 'm', 'age': a, 'games': 150}, k, doc, 2026) > SH.survival_of({'key': 'm', 'age': a + 1, 'games': 150}, k, doc, 2026)
               for a in range(24, 36) for k in (1, 2))
    check(aged, '(a) S falls with age past 24 at fixed evidence')
    # 0-game: ever0[type|tenure] as S2, sqrt as S1; MSD tenure is +1; unknown type -> default
    z1 = SH.survival_of({'key': 'z', 'age': 19, 'games': 0, 'ty': 'ND', 'yr': 2025}, 1, doc, 2026)
    z2 = SH.survival_of({'key': 'z', 'age': 19, 'games': 0, 'ty': 'ND', 'yr': 2025}, 2, doc, 2026)
    m2 = SH.survival_of({'key': 'z', 'age': 22, 'games': 0, 'ty': 'MSD', 'yr': 2025}, 2, doc, 2026)
    u2 = SH.survival_of({'key': 'z', 'age': 22, 'games': 0, 'ty': 'XYZ', 'yr': 2024}, 2, doc, 2026)
    check(abs(z2 - doc['ever0']['ND|1']) < 1e-12 and abs(z1 - math.sqrt(doc['ever0']['ND|1'])) < 1e-12
          and abs(m2 - doc['ever0']['MSD|2']) < 1e-12 and abs(u2 - doc['ever0_default']) < 1e-12,
          '(a) 0-game rows take ever0[type|tenure] (S2) and its sqrt (S1); MSD tenure +1; unknown type -> default')

    # (b) sum-preservation per age on a synthetic set
    rows = []
    i = 0
    for a in (19, 21, 24, 27, 30, 33):
        for gm, v in ((0, 400), (2, 650), (14, 1200), (40, 2300), (88, 4100), (210, 3000)):
            i += 1
            rows.append({'key': 'p%d' % i, 'age': a, 'games': gm, 'ty': 'ND', 'yr': 2026 - max(1, a - 18),
                         'vP1': v + 7 * i, 'vP2': v - 5 * i})
    per, rep = SH.apply(rows, doc, 2026, cap_lift=False)
    ok = True
    for k in (1, 2):
        fld = 'vP%d' % k
        for a in sorted(set(r['age'] for r in rows)):
            s = [r for r in rows if r['age'] == a]
            before = sum(r[fld] for r in s); after = sum(per[r['key']][fld] for r in s)
            if abs(after - before) > 0.5 * len(s):
                ok = False; print('     age %d %s %d -> %d' % (a, fld, before, after))
    check(ok, '(b) per-age lens sums preserved to rounding on the synthetic set (%d rows, 6 ages, both lenses)' % len(rows))
    check(all(abs(t['delta']) <= 0.5 * len(rows) for t in rep['totals'].values()), '(b) board totals before/after equal to rounding',
          repr(rep['totals']))
    # the charge is by risk: at a fixed age the thin row moves down and the proven row up
    thin = per['p2']; proven = per['p5']  # age 19: (2 games) vs (88 games)
    check(thin['m1'] < 1.0 < proven['m1'] and thin['m2'] < 1.0 < proven['m2'], '(b) at one age the thin row is charged (m<1) and the proven row lifted (m>1)')
    # Sbar is the lens-value-weighted mean of S at that age
    a19 = [r for r in rows if r['age'] == 19]
    want = sum(r['vP1'] * per[r['key']]['S1'] for r in a19) / sum(r['vP1'] for r in a19)
    check(abs(rep['sbar_by_age']['S1']['19']['sbar'] - want) < 1e-6, '(b) Sbar_1(19) is the vP1-weighted mean of S1 over the rows at 19')
    check(all(abs(per[r['key']]['m1'] - per[r['key']]['S1'] / rep['sbar_by_age']['S1'][str(r['age'])]['sbar']) < 1e-5 for r in rows),
          '(b) m_k = S_k / Sbar_k(age) on every row')
    check(all(per[r['key']][k2] is not None for r in rows for k2 in ('S1', 'S2', 'age', 'games', 'm1', 'm2')), '(b) per-row record carries S1,S2,age,games,m1,m2')
    check(rep['cap_lift'] is False and rep['source_md5'] and rep['ruling'] == 'SURVIVAL_H2_2026-10-14', '(b) report carries ruling, source md5, cap_lift')

    # (c) cap_lift
    perc, repc = SH.apply(rows, doc, 2026, cap_lift=True)
    check(repc['cap_lift'] is True and all(perc[r['key']]['m1'] <= 1.0 and perc[r['key']]['m2'] <= 1.0 for r in rows),
          '(c) cap_lift=True: every multiplier <= 1.0')
    check(all(perc[r['key']]['m1'] == min(1.0, per[r['key']]['m1']) for r in rows), '(c) capped m == min(1, uncapped m) row by row')
    check(all(t['after'] < t['before'] for t in repc['totals'].values()), '(c) capped totals fall (no lifts, charges kept)')
    check(any(per[r['key']]['m1'] > 1.0 for r in rows), '(c) uncapped (pure H2) carries lifts')
    # the document default drives apply() when neither the argument nor the module constant is set
    saved = SH.CAP_LIFT
    try:
        SH.CAP_LIFT = None
        _, r0 = SH.apply(rows, doc, 2026)
        SH.CAP_LIFT = True
        _, r1 = SH.apply(rows, doc, 2026)
    finally:
        SH.CAP_LIFT = saved
    check(r0['cap_lift'] is False and r1['cap_lift'] is True, '(c) CAP_LIFT=None reads the document (false); CAP_LIFT=True flips the build')

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

    print('  ' + '-' * 66)
    if _fails:
        print('  %d FAILED: %s' % (len(_fails), _fails)); return 1
    print('SURVIVAL HAZARD TESTS: ALL %d PASS' % _n[0])
    return 0


if __name__ == '__main__':
    sys.exit(main())
