#!/usr/bin/env python3
"""Unit test for engine/rl_after/survival_hazard.py — owner ruling SURVIVAL_H2_2026-10-14, capped; fix plan F1.

    python3 engine/rl_after/ingestion/test_survival_hazard.py     (exit 0 = all pass, exit 1 = a failure)

Light: no engine load. It (a) rebuilds S for a few synthetic (age, games) from the JSON coefficients by hand and
checks the module agrees, with pins against the fit script's own S grid; (b) checks the cohort rule (integer
ages, >= 33 pooled, < 5 charged rows joins the cohort below); (c) checks the capped application on a synthetic
active set — charged rows only, 0-game rows untouched with no fitted S and outside R, the evidence-only reference
R_k(age_i) in the pooled cohort, no lifts, totals fall; (d) the pure-H2 measurement variant is sum-preserving
within each single-age cohort; and it checks the halts (missing file, unformable age/games, another ruling id,
a calibration of the wrong width).
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
    check(doc['ruling'] == 'SURVIVAL_H2_2026-10-14' and doc['cap_lift'] is True, 'calibration loads; ruling id and cap_lift=true recorded (owner ruling 2026-10-14: the lift is capped)')
    check(len(doc['coef']['S1']) == 9 and len(doc['coef']['S2']) == 9 and len(doc['coef_names']) == 9, 'two 9-coefficient vectors (played rows only; no 0-game columns)')
    check('on an AFL list at the END of season Y+k' in doc['outcome'] and '_last_listed' in doc['outcome'] and 'PROXY' in doc['outcome']
          and 'PLAYED rows only' in doc['outcome'], 'the JSON states the fitted outcome (listed at the end of Y+k | listed at the end of Y, played rows), its sources and its proxy')
    check('ever0' not in doc and 'not observable before the 2024/2025 list facts' in doc['design_notes']['zero_games']
          and 'UNDER-STATES' in doc['fit']['proxy_note'] and 'biased DOWN' in doc['fit']['proxy_note'],
          'the ever0 table is gone; the 0-game outcome is recorded as unobservable pre-2024/2025; the proxy note states the direction of its bias')

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
    # pins from the fit script's S grid (fit_survival_hazard.py; MEASURED_TABLES_F1.txt): age 20 g3 0.885/0.789,
    # age 24 g75 0.946/0.891, age 28 g180 0.929/0.831, age 35 g180 0.587/0.281
    pins = [((20, 3), (0.885, 0.789)), ((24, 75), (0.946, 0.891)), ((28, 180), (0.929, 0.831)), ((35, 180), (0.587, 0.281))]
    ok = all(round(SH.survival_of({'key': 'p', 'age': a, 'games': g}, k, doc, 2026), 3) == want[k - 1] for (a, g), want in pins for k in (1, 2))
    check(ok, '(a) four pins from the fit script\'s S grid reproduce to 3 dp')
    mono = all(SH.survival_of({'key': 'm', 'age': a, 'games': g1}, k, doc, 2026) <= SH.survival_of({'key': 'm', 'age': a, 'games': g2}, k, doc, 2026) + 1e-12
               for a in range(19, 37) for k in (1, 2) for g1, g2 in ((1, 6), (6, 21), (21, 51), (51, 101), (3, 300)))
    check(mono, '(a) S is monotone non-decreasing in evidence at fixed age (the band-min rule)')
    aged = all(SH.survival_of({'key': 'm', 'age': a, 'games': 150}, k, doc, 2026) > SH.survival_of({'key': 'm', 'age': a + 1, 'games': 150}, k, doc, 2026)
               for a in range(24, 36) for k in (1, 2))
    check(aged, '(a) S falls with age past 24 at fixed evidence')
    check(SH.survival_of({'key': 'z', 'age': 19, 'games': 0}, 1, doc, 2026) is None and SH.survival_of({'key': 'z', 'age': 25, 'games': 0}, 2, doc, 2026) is None,
          '(a) a 0-game row has no fitted S (None); no type/year needed')

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
              and perc[r['key']]['charged'] is False and perc[r['key']]['S1'] is None and perc[r['key']]['S2'] is None
              and perc[r['key']]['ref1'] is None for r in zero),
          '(c) 0-game rows are not charged: charged=False, S1/S2/ref None, m=1, vP1/vP2 untouched')
    # single-age cohort: R == the value-weighted mean of the CHARGED rows' own S (the 0-game row outside it)
    for k, fld in ((1, 'vP1'), (2, 'vP2')):
        a19 = [r for r in rows if r['age'] == 19 and r['games'] >= 1]
        want = sum(r[fld] * perc[r['key']]['S%d' % k] for r in a19) / sum(r[fld] for r in a19)
        d = repc['sbar_by_cohort']['S%d' % k]['19']
        check(abs(d['sbar'] - want) < 1e-6 and abs(d['ref_by_age']['19'] - want) < 1e-6 and d['n_charged'] == 5 and d['n_zero_game'] == 1
              and all(abs(perc[r['key']]['ref%d' % k] - want) < 1e-5 for r in a19),
              '(c) single-age cohort 19: R_%d(19) == the %s-weighted mean of S%d over the 5 charged rows (the 0-game row outside it)' % (k, fld, k))
    check(all(abs(perc[r['key']]['m1'] - min(1.0, perc[r['key']]['S1'] / perc[r['key']]['ref1'])) < 1e-5 for r in rows if r['games'] >= 1),
          '(c) m_k = min(1, S_k / R_k(age_i)) on every charged row')
    # the pooled cohort: R_k(age_i) is the cohort's evidence mix priced at the row's OWN age (not at the cohort-mates' ages)
    pool = [r for r in rows if r['age'] >= 33 and r['games'] >= 1]
    ok = True
    for k, fld in ((1, 'vP1'), (2, 'vP2')):
        coef = doc['coef']['S%d' % k]; mids = tuple(doc['band_midpoints'])
        den = sum(r[fld] for r in pool)
        for a in (33, 35):
            want = sum(r[fld] * SH.survival(a, r['games'], coef, mids) for r in pool) / den
            got = repc['sbar_by_cohort']['S%d' % k]['33+']['ref_by_age'][str(a)]
            rows_a = [r for r in pool if r['age'] == a]
            if abs(got - want) > 1e-6 or any(abs(perc[r['key']]['ref%d' % k] - want) > 1e-5 for r in rows_a):
                ok = False; print('     k=%d age %d R %.6f want %.6f' % (k, a, got, want))
    check(ok, '(c) pooled 33+ cohort: R_k(33) and R_k(35) are the SAME evidence mix priced at 33 and at 35 (evidence-only reference)')
    # the evidence-only reference: the 35-year-old with the same games as a 33-year-old is NOT charged more for his age
    p33 = {r['games']: perc[r['key']] for r in pool if r['age'] == 33}; p35 = {r['games']: perc[r['key']] for r in pool if r['age'] == 35}
    # under an age-level reference (one Sbar for the pool) the 35-year-old would be charged S(35,g)/Sbar < S(33,g)/Sbar, i.e. for
    # being older; under the evidence-only reference the two multipliers differ only by the small residual age effect on the
    # S(age,g)/R(age) RATIO (a few hundredths), and the proven rows at BOTH ages are held at 1.
    check(all(abs(p33[g]['m1'] - p35[g]['m1']) < 0.05 and abs(p33[g]['m2'] - p35[g]['m2']) < 0.10 for g in p33)
          and p33[210]['m1'] == p35[210]['m1'] == 1.0 and p33[88]['m1'] == p35[88]['m1'] == 1.0 and p33[210]['m2'] == p35[210]['m2'] == 1.0,
          '(c) in the pool a 35-year-old is not charged for his age: same-games multipliers at 33 and 35 agree to a few hundredths; the proven rows at both ages are held at 1',
          repr([(g, p33[g]['m1'], p35[g]['m1'], p33[g]['m2'], p35[g]['m2']) for g in sorted(p33)]))
    check(repc['cohort_of_age']['33'] == '33+' and repc['cohort_of_age']['35'] == '33+' and set(repc['sbar_by_cohort']['S1']['33+']['ages']) == {33, 35},
          '(c) ages 33 and 35 share the pooled 33+ cohort')
    thin = perc['p2']; proven = perc['p5']  # age 19: (2 games) vs (88 games)
    check(thin['m1'] < 1.0 and thin['m2'] < 1.0 and proven['m1'] == 1.0 and proven['m2'] == 1.0, '(c) at one age the thin row is charged (m<1) and the proven row is held (m=1, no lift)')
    check(all(k2 in perc[r['key']] for r in rows for k2 in ('S1', 'S2', 'age', 'games', 'cohort', 'charged', 'ref1', 'ref2', 'm1', 'm2')), '(c) per-row record carries S1,S2,age,games,cohort,charged,ref1,ref2,m1,m2')
    check(repc['source_md5'] and repc['ruling'] == 'SURVIVAL_H2_2026-10-14' and repc['nCharged'] == 35 and repc['nZeroGame'] == 7
          and 'not sum-preserving' in repc['law'] and 'R_k(age_i)' in repc['law'] and repc['outcome'], '(c) report carries ruling, source md5, charged/0-game counts, the capped evidence-only law, the outcome')

    # (d) the pure-H2 measurement variant: sum-preserving within each single-age cohort over the charged rows
    per, rep = SH.apply(rows, doc, 2026, cap_lift=False)
    ok = True
    for k in (1, 2):
        fld = 'vP%d' % k
        for c in ('19', '21', '24', '27', '30'):
            s = [r for r in rows if r['games'] >= 1 and per[r['key']]['cohort'] == c]
            before = sum(r[fld] for r in s); after = sum(per[r['key']][fld] for r in s)
            if abs(after - before) > 0.5 * len(s):
                ok = False; print('     cohort %s %s %d -> %d' % (c, fld, before, after))
    check(ok, '(d) cap_lift=False: single-age cohorts\' charged lens sums preserved to rounding (both lenses)')
    check(rep['cap_lift'] is False and any(per[r['key']]['m1'] > 1.0 for r in rows) and all(per[r['key']]['m1'] == 1.0 for r in zero)
          and all(abs(per[r['key']]['m1'] - per[r['key']]['S1'] / per[r['key']]['ref1']) < 1e-5 for r in pool),
          '(d) uncapped carries lifts on charged rows; 0-game rows still m=1; the pool uses the same S/R(age_i) uncapped')
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
    e = raises(lambda: SH.apply([{'key': 'bad-lens', 'age': 22, 'games': 10, 'vP1': 1, 'vP2': None}], doc, 2026))
    check(e is not None and 'bad-lens' in e, 'halt names the key: unformable lens value')
    with tempfile.TemporaryDirectory() as td:
        bad = dict(json.load(open(HZ))); bad['ruling'] = 'OTHER'
        p = os.path.join(td, 'h.json'); json.dump(bad, open(p, 'w'))
        check(raises(lambda: SH.load(p)) is not None, 'halt: a calibration carrying another ruling id')
        bad = dict(json.load(open(HZ))); bad['coef'] = {'S1': bad['coef']['S1'] + [0.0, 0.0], 'S2': bad['coef']['S2']}
        p = os.path.join(td, 'h11.json'); json.dump(bad, open(p, 'w'))
        check(raises(lambda: SH.load(p)) is not None, 'halt: a calibration of the wrong width (an 11-coefficient vector)')

    print('  ' + '-' * 66)
    if _fails:
        print('  %d FAILED: %s' % (len(_fails), _fails)); return 1
    print('SURVIVAL HAZARD TESTS: ALL %d PASS' % _n[0])
    return 0


if __name__ == '__main__':
    sys.exit(main())
