#!/usr/bin/env python3
"""THE SURVIVAL-HAZARD FIT (fix plan F1, 2026-10-14) — reads the store, writes data/survival_hazard.json.

    python3 engine/rl_after/ingestion/fit_survival_hazard.py                 fit + write the calibration
    python3 engine/rl_after/ingestion/fit_survival_hazard.py --dry           fit, print, write nothing
    python3 engine/rl_after/ingestion/fit_survival_hazard.py --measure OUT   fit, write, then apply the MODULE
                                                                              (survival_hazard.apply) to the live
                                                                              board's active rows and write the
                                                                              measured tables to OUT

THE OUTCOME, AS FITTED (fix plan F1 after the blind review of the first survival act; second review: PLAYED rows):
    S_k(age, evidence) = P( on an AFL list at the END of season Y+k | listed at the END of base season Y with
                            career games >= 1, age at Y, career games through Y ),   k in {1, 2}
  * last_listed_year per store row: `_last_listed` when present (a list FACT, the AFL 2024/2025 list changes);
    else 2026 for a row active today (on the live board's `active`); else the last season with a game — a
    PROXY that under-states listing for a retiree who sat out his last listed season(s): on the 170 retirees
    that carry both a list fact and games, 33 are one season short and 9 two seasons short (about 25%), so the
    pre-2024 played-band survival is biased DOWN and the charge biased UP by an unquantified amount.
  * "listed at the end of Y" iff debut <= Y <= last_listed_year; debut = draft year + 1 (MSD: the draft year),
    rl_model.py:171.  outcome_k = 1 iff last_listed_year >= Y + k.
  * base seasons 2010..2024 for k=1 and 2010..2023 for k=2 — the latest outcome year is 2025, which the
    couriered list changes cover; nothing depends on an unobserved future (2026 is "active today", no more).
  * age at Y is the engine's own clock: max(Y - birth_year, 18 + (Y - cycle_year)) (rl_model._age_at).
  * 0-game (never-played) records are COUNTED in the coverage table but NOT in the fit: a never-played
    retiree's exit season is not observable before the 2024/2025 list facts (575 of 619 carry none), and in
    the first F1 fit a 0-game band leaked into the shared age slopes. No fitted S is published for a 0-game
    row; the fact-only window's raw rates are recorded in the JSON for the record (`zero_game_fact_window`).

THE MODEL: one additive-logit per lens (IRLS, ridge 1e-6), design
    [1, min(age,24)-24, (age-24)+, (age-29)+, (age-33)+, band6-20, band21-50, band51-100, band101+]
  (the reference band is 1-5 career games). Applied monotone in evidence (survival_hazard.survival).

Deterministic: same store + same board -> byte-identical coefficients.
"""
import os, sys, json, math, argparse, hashlib, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
STORE = os.path.join(REPO, 'engine', 'rl_after', 'rl_model_data.json')
BOARD = os.path.join(REPO, 'data', 'rl_build', 'rl_app_data.json')
OUT = os.path.join(REPO, 'data', 'survival_hazard.json')
ACTIVE_YEAR = 2026                      # "active today" = listed through 2026, nothing beyond
BASE = {1: range(2010, 2025), 2: range(2010, 2024)}
BANDS = ((1, 5), (6, 20), (21, 50), (51, 100), (101, None))
BAND_NAMES = ('1-5', '6-20', '21-50', '51-100', '101+')
MIDPOINTS = (3, 12, 35, 75, 180)
DESIGN = '[1, min(age,24)-24, (age-24)+, (age-29)+, (age-33)+, band6-20, band21-50, band51-100, band101+]'
COEF_NAMES = ('const', 'young_slope', 'age24+', 'age29+', 'age33+', 'band6-20', 'band21-50', 'band51-100', 'band101+')
RULING = 'SURVIVAL_H2_2026-10-14'
GRID_AGES = (20, 24, 28, 32, 35)


# ---- the sample -----------------------------------------------------------------------------------------
def debut(r):
    return r['year'] if r['type'] == 'MSD' else r['year'] + 1


def cycle_year(r):
    return r['year'] - (1 if r['type'] == 'MSD' else 0)


def age_at(r, Y):
    return max(Y - r['_by'], 18 + (Y - cycle_year(r)))


def band_index(g):
    """0..4 for g >= 1; None for 0 games (not a fitted band)."""
    if g == 0: return None
    for i, (lo, hi) in enumerate(BANDS):
        if lo <= g and (hi is None or g <= hi): return i
    raise ValueError(g)


def last_listed(r, active_keys):
    """(last_listed_year, source) — source in fact | active | lastplay | none (never played, no list fact)."""
    if r.get('_last_listed') is not None:
        return int(r['_last_listed']), 'fact'
    if r['key'] in active_keys:
        return ACTIVE_YEAR, 'active'
    played = [s['year'] for s in (r['scoring'] or []) if s['games'] > 0]
    if played:
        return max(played), 'lastplay'
    return None, 'none'


def build_sample(rows, active_keys):
    """Every (row, base season) with the row listed at the end of Y. 0-game records carry band None and are
    counted in the coverage table only; a never-played row with no list fact (last_listed None) is listed at
    its debut season only (the one season a drafted player is certainly on a list) with an unobservable outcome."""
    recs = []
    for r in rows:
        ll, src = last_listed(r, active_keys)
        d = debut(r)
        gy = collections.defaultdict(int)
        for s in r['scoring'] or []:
            gy[s['year']] += s['games']
        for Y in range(2010, 2025):
            if ll is None:
                if Y != d:
                    continue
            elif not (d <= Y <= ll):
                continue
            g = sum(v for y, v in gy.items() if y <= Y)
            recs.append({'key': r['key'], 'Y': Y, 'age': age_at(r, Y), 'g': g, 'band': band_index(g),
                         'tenure': Y - d + 1, 'ty': r['type'], 'src': src, 'll': ll,
                         'y1': ((ll >= Y + 1) if ll is not None else None) if Y in BASE[1] else None,
                         'y2': ((ll >= Y + 2) if ll is not None else None) if Y in BASE[2] else None})
    return recs


def played(recs):
    return [x for x in recs if x['g'] >= 1]


# ---- the model --------------------------------------------------------------------------------------------
def design(recs):
    a = np.array([x['age'] for x in recs], float)
    b = np.array([x['band'] for x in recs])
    cols = [np.ones_like(a), np.minimum(a, 24) - 24, np.maximum(0, a - 24), np.maximum(0, a - 29), np.maximum(0, a - 33)] + \
           [(b == i).astype(float) for i in range(1, 5)]
    return np.column_stack(cols)


def irls(Xm, y, it=100, ridge=1e-6):
    b = np.zeros(Xm.shape[1])
    for _ in range(it):
        p = 1 / (1 + np.exp(-Xm @ b)); W = p * (1 - p) + 1e-9
        H = Xm.T @ (Xm * W[:, None]) + ridge * np.eye(len(b))
        step = np.linalg.solve(H, Xm.T @ (y - p))
        b = b + step
        if np.max(np.abs(step)) < 1e-12:
            break
    p = 1 / (1 + np.exp(-Xm @ b)); W = p * (1 - p) + 1e-9
    se = np.sqrt(np.diag(np.linalg.inv(Xm.T @ (Xm * W[:, None]) + ridge * np.eye(len(b)))))
    return b, se


def fit_lens(recs, k, keep=lambda x: True):
    """The fit on the PLAYED records (g >= 1) with an observed outcome for lens k."""
    fld = 'y%d' % k
    R = [x for x in played(recs) if x[fld] is not None and keep(x)]
    y = np.array([1.0 if x[fld] else 0.0 for x in R])
    b, se = irls(design(R), y)
    return b, se, len(R), int(y.sum())


def s_raw(coef, age, g):
    b = band_index(max(1, g))
    x = [1, min(age, 24) - 24, max(0, age - 24), max(0, age - 29), max(0, age - 33)] + [1 if b == i else 0 for i in range(1, 5)]
    return 1 / (1 + math.exp(-sum(u * float(c) for u, c in zip(x, coef))))


def s_mono(coef, age, g):
    """The module's rule: monotone in evidence (a thinner band never beats a thicker one at the same age)."""
    g = max(1, g)
    s = s_raw(coef, age, g)
    if g <= max(MIDPOINTS):
        s = min(s, min(s_raw(coef, age, m) for m in MIDPOINTS if m >= g))
    return s


# ---- the printed fit report -------------------------------------------------------------------------------
def pct(a, n):
    return '%.3f' % (a / n) if n else '  -  '


def coverage_table(recs):
    out = ['COVERAGE per base season Y: listed rows n (0-game n0 among them, NOT fitted), PLAYED rows: exits at +1 (not listed end Y+1) and S1,',
           'exits at +2 and S2; rows by last_listed source (fact = _last_listed; active = listed through 2026; lastplay = last played',
           'season, PROXY; none = never-played retiree with no list fact, outcome unobservable, counted at the debut season only)',
           '  Y      n   n0 | played exit1   S1  | exit2   S2  | fact active lastplay none']
    def line(lbl, s):
        pl = [x for x in s if x['g'] >= 1]
        e1 = sum(1 for x in pl if x['y1'] is False); n1 = sum(1 for x in pl if x['y1'] is not None)
        e2 = sum(1 for x in pl if x['y2'] is False); n2 = sum(1 for x in pl if x['y2'] is not None)
        src = collections.Counter(x['src'] for x in s)
        return '  %s  %5d %4d | %6d %5d  %s | %5s  %s | %4d %6d %8d %4d' % (
            lbl, len(s), sum(1 for x in s if x['g'] == 0), len(pl), e1, pct(n1 - e1, n1), (str(e2) if n2 else '-'),
            pct(n2 - e2, n2), src['fact'], src['active'], src['lastplay'], src['none'])
    for Y in range(2010, 2025):
        out.append(line(str(Y), [x for x in recs if x['Y'] == Y]))
    out.append(line('all ', recs))
    return '\n'.join(out)


def cell_table(recs, coef1, coef2):
    AG = [(18, 20), (21, 22), (23, 24), (25, 26), (27, 28), (29, 30), (31, 32), (33, 40)]
    out = ['CELL CHECK raw vs fit (played rows): S1 raw/fit  S2 raw/fit  n (k=1 rows) by age group x band; cells n<8 shown as n only',
           '  ' + '%-7s' % 'age' + ''.join('%-29s' % b for b in BAND_NAMES)]
    for lo, hi in AG:
        ln = '  %-7s' % ('%d-%d' % (lo, hi))
        for i, nm in enumerate(BAND_NAMES):
            s1 = [x for x in played(recs) if lo <= x['age'] <= hi and x['band'] == i and x['y1'] is not None]
            s2 = [x for x in played(recs) if lo <= x['age'] <= hi and x['band'] == i and x['y2'] is not None]
            if len(s1) < 8:
                ln += '%-29s' % ('n=%d' % len(s1)); continue
            f1 = np.mean([s_mono(coef1, x['age'], x['g']) for x in s1])
            f2 = np.mean([s_mono(coef2, x['age'], x['g']) for x in s2]) if s2 else float('nan')
            ln += '%-29s' % ('%.2f/%.2f  %s/%.2f  n=%d' % (np.mean([x['y1'] for x in s1]), f1, pct(sum(x['y2'] for x in s2), len(s2)), f2, len(s1)))
        out.append(ln)
    return '\n'.join(out)


def grid(coef1, coef2, ages=GRID_AGES, title='S GRID (S1/S2, as the module applies them) by age x band (band midpoints 3/12/35/75/180):'):
    out = [title, '  ' + '%-5s' % 'age' + ''.join('%-13s' % b for b in BAND_NAMES)]
    for a in ages:
        out.append('  %-5d' % a + ''.join('%-13s' % ('%.3f/%.3f' % (s_mono(coef1, a, m), s_mono(coef2, a, m))) for m in MIDPOINTS))
    return '\n'.join(out)


def coef_table(fits):
    out = ['COEFFICIENTS (estimate (SE) z) per lens:', '  %-16s %-28s %-28s' % ('term', 'S1', 'S2')]
    for i, nm in enumerate(COEF_NAMES):
        out.append('  %-16s ' % nm + ' '.join('%9.4f (%6.4f) z=%6.2f' % (f[0][i], f[1][i], f[0][i] / f[1][i]) for f in fits))
    return '\n'.join(out)


def fact_window(recs):
    """Y=2024, k=1: every exit in the 2024/2025 off-seasons is a list fact. Raw S1 by band, the 0-game rows split
    by tenure (1st listed season vs 2nd+) — the only window where the 0-game outcome is observable."""
    s24 = [x for x in recs if x['Y'] == 2024 and x['y1'] is not None]
    cells = [('0g t1', lambda x: x['g'] == 0 and x['tenure'] == 1), ('0g t2+', lambda x: x['g'] == 0 and x['tenure'] >= 2)] + \
            [(nm, (lambda i: lambda x: x['band'] == i)(i)) for i, nm in enumerate(BAND_NAMES)]
    return s24, [(nm, [x for x in s24 if sel(x)]) for nm, sel in cells]


def proxy_tables(recs, fits):
    out = ['PROXY SENSITIVITY — the fit on (i) all played rows (SHIPPED) and (ii) without the lastplay proxy rows (fact + active',
           'only; a SURVIVOR-ONLY sample for the pre-2024 exits, so it over-states survival and is shown for the measurement, not as',
           'an alternative). The lastplay proxy under-states listing for about 25% of retirees (33 of 170 one season, 9 two), so the',
           'shipped pre-2024 played-band survival is biased DOWN and the charge UP by an unquantified amount. S grid S1/S2 by age x band:']
    variants = [('(i) ALL played rows (shipped)', lambda x: True),
                ('(ii) without the lastplay proxy rows (fact + active only)', lambda x: x['src'] in ('fact', 'active'))]
    for lbl, keep in variants:
        f1 = fit_lens(recs, 1, keep); f2 = fit_lens(recs, 2, keep)
        out.append('  %s: n1=%d (survivors %d) n2=%d (survivors %d)' % (lbl, f1[2], f1[3], f2[2], f2[3]))
        out.append('  ' + '%-5s' % 'age' + ''.join('%-13s' % b for b in BAND_NAMES))
        for a in GRID_AGES:
            out.append('  %-5d' % a + ''.join('%-13s' % ('%.3f/%.3f' % (s_mono(f1[0], a, m), s_mono(f2[0], a, m))) for m in MIDPOINTS))
    s24, cells = fact_window(recs)
    out.append('FACT-ONLY WINDOW Y=2024, k=1 (n=%d; every exit in the 2024/2025 off-seasons is a list fact, so no proxy enters the outcome):' % len(s24))
    out.append('  raw S1 by band vs the shipped fit averaged over the same rows (0-game rows: raw rate only, by tenure; no fitted S)')
    for nm, s in cells:
        if not s: continue
        fitv = ('fit %.3f' % np.mean([s_mono(fits[0][0], x['age'], x['g']) for x in s])) if s[0]['g'] >= 1 else 'no fitted S'
        out.append('  %-7s n=%4d  raw S1 %.3f  %s' % (nm, len(s), np.mean([x['y1'] for x in s]), fitv))
    return '\n'.join(out)


def build_doc(fits, recs, store_md5, n_ll):
    (b1, se1, n1, s1), (b2, se2, n2, s2) = fits
    s24, cells = fact_window(recs)
    zg = {nm: {'n': len(s), 'raw_S1': round(float(np.mean([x['y1'] for x in s])), 3)} for nm, s in cells if nm.startswith('0g')}
    return {
        'ruling': RULING, 'date': '2026-10-14', 'cap_lift': True,
        'bands': [list(b) for b in BANDS], 'band_midpoints': list(MIDPOINTS),
        'coef': {'S1': [float(x) for x in b1], 'S2': [float(x) for x in b2]},
        'coef_se': {'S1': [round(float(x), 6) for x in se1], 'S2': [round(float(x), 6) for x in se2]},
        'coef_names': list(COEF_NAMES),
        'design': DESIGN,
        'outcome': ('S_k(age, evidence) = P(on an AFL list at the END of season Y+k | listed at the END of base season Y with career '
                    'games >= 1, age at Y, career games through Y), k in {1,2}; PLAYED rows only. last_listed_year per store row = '
                    '_last_listed (a list fact, the AFL 2024/2025 list changes) when present; else 2026 for a row active today (the live '
                    'board); else the last season with a game (a PROXY that under-states listing for a retiree who sat out his last listed '
                    'season(s)). Listed at the end of Y iff debut <= Y <= last_listed_year (debut = draft year + 1; MSD = the draft year). '
                    'outcome_k = 1 iff last_listed_year >= Y+k. Base seasons 2010..2024 (k=1) and 2010..2023 (k=2): the latest outcome '
                    'year is 2025, covered by the couriered list changes; nothing depends on an unobserved future. 0-game (never-played) '
                    'records are not in the fit and carry no fitted S.'),
        'design_notes': {
            'age': "the engine's integer age at the base season: max(Y - birth_year, 18 + (Y - cycle_year)) (rl_model._age_at); "
                   "at application the board row's age(p) at AGE_REF = 2026",
            'games': "career games through the base season (fit: cumulative scoring games <= Y; application: the board row's games)",
            'bands': 'career-games bands; the reference band is 1-5 games; dummies for 6-20, 21-50, 51-100, 101+',
            'zero_games': 'NOT fitted and NOT charged. A never-played retiree\'s exit season is not observable before the 2024/2025 list '
                          'facts (575 of the 619 never-played retirees carry no list fact), and a 0-game band in the fit leaked into the '
                          'shared age slopes (first F1 fit: young_slope -0.309 vs -0.419 played-only for S1). At application a 0-game row '
                          'carries charged=false, S1/S2 = null, m = 1: its vP is a pick-curve expectation that already averages over busts. '
                          'The fact-only window\'s raw rates are recorded in zero_game_fact_window for the record only.',
            'monotone_in_evidence': 'S(age,g) = min over band midpoints m >= g of S_raw(age,m), together with S_raw(age,g); for g > 180, S_raw(age,g)',
            'application': "RELATIVE within a cohort by EVIDENCE, CAPPED: vP_k' = round(vP_k x min(1, S_k(age_i, g_i) / R_k(age_i))) over the "
                           'CHARGED rows (games >= 1); R_k(age_i) = sum_j w_j S_k(age_i, g_j) over the charged rows j of the cohort, w_j = '
                           'vP_j / sum vP — the cohort\'s evidence mix priced at the row\'s OWN age, so a row is charged for thinner evidence, '
                           'never for being older than its cohort-mates (for a single-age cohort this is the value-weighted mean of S_k). '
                           'Cohorts: one per integer age, ages >= 33 pooled into one, and any age with fewer than 5 charged rows joins the '
                           'nearest larger cohort below it. The cap means the lens totals can only fall: NOT sum-preserving.'},
        'zero_game_fact_window': {'window': 'Y=2024, k=1 (listed at the end of 2025 | 0 career games through 2024)', 'by_tenure': zg,
                                  'note': 'raw rates for the record; the 0-game outcome is not observable before the 2024/2025 list facts, '
                                          'so no S is fitted or published for 0-game rows'},
        'fit': {
            'fitted_by': 'engine/rl_after/ingestion/fit_survival_hazard.py (deterministic; re-run to reproduce)',
            'model': 'additive-logit per lens (IRLS, ridge 1e-6); S1 = P(listed at the end of Y+1), S2 = P(listed at the end of Y+2)',
            'store': 'engine/rl_after/rl_model_data.json', 'store_md5': store_md5, 'rows_carrying_last_listed': n_ll,
            'base_seasons': {'S1': '2010-2024', 'S2': '2010-2023'},
            'n': {'S1': n1, 'S2': n2}, 'survivors': {'S1': s1, 'S2': s2},
            'n_zero_game_records_not_fitted': sum(1 for x in recs if x['g'] == 0),
            'last_listed_sources_played': dict(sorted(collections.Counter(x['src'] for x in played(recs)).items())),
            'proxy_note': 'DIRECTION OF BIAS: the last-played proxy UNDER-STATES listing — of the 170 retirees that carry both a list fact '
                          'and games, 33 were listed one season beyond their last game and 9 two seasons (about 25%). Where the proxy '
                          'stands (every pre-2024 exit without a list fact) a retiree is counted as exited one season early, so the '
                          'pre-2024 played-band survival is biased DOWN and the within-cohort charge biased UP, by an unquantified '
                          'amount. The fit with and without the proxy rows: '
                          'docs/evidence/engine_survival_hazard_2026-10-14/MEASURED_TABLES_F1.txt.'},
        'ruling_text': 'D-H = H2: retirement/exit risk on the +1 and +2 lens values is probability-based survival, spread across each '
                       'age cohort by risk; the lift is capped at 1.0 (owner ruling 2026-10-14), so the lens totals fall by the '
                       'within-cohort thin-evidence charge.',
        'cap_lift_note': 'Owner ruling 2026-10-14: the lift is capped at 1.0 — nobody rises for survival; the charge on thin-evidence '
                         'players stands and the lens totals fall by it. Measured: MEASURED_TABLES_F1.txt.',
    }


# ---- the board measurement (the MODULE's apply on the live board) ---------------------------------------
AGE_BANDS = ((18, 20), (21, 22), (23, 24), (25, 26), (27, 28), (29, 30), (31, 33), (34, 40))
EV_BANDS = ((0, 0), (1, 5), (6, 20), (21, 50), (51, 100), (101, 999))


def measure(doc_path, board_path, out_path, recs, fits):
    sys.path.insert(0, os.path.join(REPO, 'engine', 'rl_after'))
    os.environ.setdefault('RL_REPO', REPO)
    import survival_hazard as SH
    doc = SH.load(doc_path)
    board = json.load(open(board_path)); act = board['active']
    rows = [{'key': p['key'], 'age': p['age'], 'games': p['g'], 'vP1': p['vP1'], 'vP2': p['vP2']} for p in act]
    per, rep = SH.apply(rows, doc, 2026)
    present = sum(p['v'] for p in act)
    ent = board['phantomTotals']['_meta']['entrant_layer_pvc']
    L = []
    L.append('SURVIVAL HAZARD F1 — MEASURED ON THE LIVE BOARD (data/rl_build/rl_app_data.json active rows, %d; calibration %s md5 %s; cap_lift=%s)'
             % (len(act), rep['source'], rep['source_md5'], rep['cap_lift']))
    L.append('law: %s' % rep['law'])
    L.append('charged rows %d; 0-game rows (no fitted S, not charged) %d' % (rep['nCharged'], rep['nZeroGame']))
    L.append('')
    L.append('LENS TOTALS (players): ' + '   '.join('%s %d -> %d (%+d, %+.2f%%)' % (lbl, t['before'], t['after'], t['delta'], 100.0 * t['delta'] / t['before'])
                                                   for lbl, t in sorted(rep['totals'].items())))
    L.append('RECONCILED vs present %s (players + %s x classes): ' % (format(present, ','), format(ent, ',')) +
             '   '.join('%s before %s (%+.2f%%) -> after %s (%+.2f%%)' % (lbl, format(t['before'] + ent * k, ','), 100.0 * (t['before'] + ent * k) / present - 100,
                                                                        format(t['after'] + ent * k, ','), 100.0 * (t['after'] + ent * k) / present - 100)
                       for k, (lbl, t) in enumerate(sorted(rep['totals'].items()), 1)))
    L.append('')
    L.append('COHORTS (R per cohort = the cohort\'s evidence mix at its own age(s); n_charged / n_zero_game / charged lens sum):')
    for nm in ('S1', 'S2'):
        L.append('  %s: ' % nm + '  '.join('%s:%s(%d/%d/%d)' % (c, '/'.join('%s@%s' % (v, a) for a, v in d['ref_by_age'].items()) if len(d['ref_by_age']) > 1 else '%.3f' % d['sbar'],
                                                            d['n_charged'], d['n_zero_game'], d['lens_sum']) for c, d in rep['sbar_by_cohort'][nm].items()))
    ages_merged = {a: c for a, c in rep['cohort_of_age'].items() if c != a}
    L.append('  ages pooled/merged: %s' % (', '.join('%s->%s' % (a, c) for a, c in sorted(ages_merged.items(), key=lambda t: int(t[0]))) or 'none'))
    for k in (1, 2):
        fld = 'vP%d' % k
        L.append('')
        L.append('+%d MOVERS BY EVIDENCE BAND (career games): n, moved, before -> after (delta, %%; share of the charge)' % k)
        tot_charge = sum(p[fld] - per[p['key']][fld] for p in act)
        for lo, hi in EV_BANDS:
            s = [p for p in act if lo <= p['g'] <= hi]
            b = sum(p[fld] for p in s); a = sum(per[p['key']][fld] for p in s)
            L.append('   g %3d-%3d n=%3d moved=%3d  %7d -> %7d (%+6d, %+5.1f%%; %4.1f%% of the charge)'
                     % (lo, hi, len(s), sum(1 for p in s if per[p['key']][fld] != p[fld]), b, a, a - b, (100.0 * (a - b) / b) if b else 0.0, (100.0 * (b - a) / tot_charge) if tot_charge else 0.0))
        L.append('+%d MOVERS BY AGE BAND: n, moved, before -> after (delta, %%)' % k)
        for lo, hi in AGE_BANDS:
            s = [p for p in act if lo <= p['age'] <= hi]
            b = sum(p[fld] for p in s); a = sum(per[p['key']][fld] for p in s)
            L.append('   age %2d-%2d n=%3d moved=%3d  %7d -> %7d (%+6d, %+5.1f%%)'
                     % (lo, hi, len(s), sum(1 for p in s if per[p['key']][fld] != p[fld]), b, a, a - b, (100.0 * (a - b) / b) if b else 0.0))
        s = [p for p in act if 26 <= p['age'] <= 32]
        b = sum(p[fld] for p in s); a = sum(per[p['key']][fld] for p in s)
        L.append('   the 26-32 lens (the r_pop damper\'s cohorts): n=%d  %d -> %d  charge %d = %.2f%% of the 26-32 %s total' % (len(s), b, a, b - a, 100.0 * (b - a) / b, fld))
        L.append('+%d BIGGEST 12 DOWN:' % k)
        for p in sorted(act, key=lambda p: per[p['key']][fld] - p[fld])[:12]:
            q = per[p['key']]
            L.append('   %-26s age %2d g %3d %-3s cohort %-5s  v %6d  %s %6d -> %6d (%+5d, %+5.1f%%)  S%d=%.3f R=%.3f m%d=%.3f'
                     % (p['name'], p['age'], p['g'], p['ty'], q['cohort'], p['v'], fld, p[fld], q[fld], q[fld] - p[fld], 100.0 * (q[fld] - p[fld]) / p[fld], k, q['S%d' % k], q['ref%d' % k], k, q['m%d' % k]))
        L.append('+%d moved rows: %d of %d (down %d; up 0 under the cap)' % (k, sum(1 for p in act if per[p['key']][fld] != p[fld]), len(act), sum(1 for p in act if per[p['key']][fld] < p[fld])))
    pooled = [c for c in rep['sbar_by_cohort']['S1'] if c.endswith('+')]
    for c in pooled:
        L.append('')
        L.append('THE %s COHORT, every charged row: S_k at own age, R_k (the cohort\'s evidence mix at that age), m_k, vP before -> after' % c)
        for p in sorted([p for p in act if per[p['key']]['cohort'] == c and per[p['key']]['charged']], key=lambda p: (p['age'], -p['g'])):
            q = per[p['key']]
            L.append('   %-26s age %2d g %3d  S1 %.3f R1 %.3f m1 %.3f vP1 %6d -> %6d (%+5d) | S2 %.3f R2 %.3f m2 %.3f vP2 %6d -> %6d (%+5d)'
                     % (p['name'], p['age'], p['g'], q['S1'], q['ref1'], q['m1'], p['vP1'], q['vP1'], q['vP1'] - p['vP1'], q['S2'], q['ref2'], q['m2'], p['vP2'], q['vP2'], q['vP2'] - p['vP2']))
    L.append('')
    L.append('0-GAME ROWS (no fitted S, vP untouched): n=%d  sum v %d  vP1 %d  vP2 %d'
             % (rep['nZeroGame'], sum(p['v'] for p in act if p['g'] == 0), sum(p['vP1'] for p in act if p['g'] == 0), sum(p['vP2'] for p in act if p['g'] == 0)))
    L.append('')
    L.append(coverage_table(recs))
    L.append('')
    L.append('FIT (played rows): k=1 n=%d survivors %d | k=2 n=%d survivors %d' % (fits[0][2], fits[0][3], fits[1][2], fits[1][3]))
    L.append(coef_table(fits))
    L.append(grid(fits[0][0], fits[1][0]))
    L.append(cell_table(recs, fits[0][0], fits[1][0]))
    L.append('')
    L.append(proxy_tables(recs, fits))
    open(out_path, 'w').write('\n'.join(L) + '\n')
    print('\nwrote %s' % os.path.relpath(out_path, REPO))
    return rep


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry', action='store_true')
    ap.add_argument('--measure', default=None, help='write the measured board tables to this path')
    args = ap.parse_args(argv)
    raw = open(STORE, 'rb').read(); rows = json.loads(raw)
    board = json.load(open(BOARD)); active_keys = {p['key'] for p in board['active']}
    store_active = {r['key'] for r in rows if not r.get('_retired')}
    print('store %s md5 %s rows %d; board active %d; store non-retired %d; symmetric difference %d'
          % (os.path.relpath(STORE, REPO), hashlib.md5(raw).hexdigest(), len(rows), len(active_keys), len(store_active), len(active_keys ^ store_active)))
    n_ll = sum(1 for r in rows if r.get('_last_listed') is not None)
    print('rows carrying _last_listed: %d' % n_ll)
    recs = build_sample(rows, active_keys)
    print('sample: %d (row, base season) records; played %d; 0-game (not fitted) %d'
          % (len(recs), len(played(recs)), sum(1 for x in recs if x['g'] == 0)))
    print(coverage_table(recs))
    fits = [fit_lens(recs, 1), fit_lens(recs, 2)]
    print('\nFIT (played rows): k=1 n=%d survivors %d | k=2 n=%d survivors %d' % (fits[0][2], fits[0][3], fits[1][2], fits[1][3]))
    print(coef_table(fits))
    print(cell_table(recs, fits[0][0], fits[1][0]))
    print(grid(fits[0][0], fits[1][0]))
    print(proxy_tables(recs, fits))
    doc = build_doc(fits, recs, hashlib.md5(raw).hexdigest(), n_ll)
    if not args.dry:
        with open(OUT, 'w') as f:
            json.dump(doc, f, indent=1, sort_keys=True); f.write('\n')
        print('\nwrote %s md5 %s' % (os.path.relpath(OUT, REPO), hashlib.md5(open(OUT, 'rb').read()).hexdigest()))
        if args.measure:
            measure(OUT, BOARD, args.measure, recs, fits)
    return 0


if __name__ == '__main__':
    sys.exit(main())
