#!/usr/bin/env python3
"""ORDER B — THE STANDING TWO-SIDED NO-ARB SUITE on the O33B matrix beside the O32RFINAL control.
  * five ND bands (1-10/11-20/21-30/31-40/41-64): year paths, yr0->1 appreciation, TWO-SIDED verdicts
    (sell-side RED if appreciation < 0; buy-side RED if appreciation > 14% carry)
  * per-arm pool tables (RD/MSD/UNR/IRE/PDA/PDN/SSP/PDS + pooled all-pool), cohort clock, same rules
  * the R3(c) vantage-consistency matrix: growth yrV->V+k (V=0,1,2; k=1..4) vs carry 1.14^k
  * THE ENTRY-YEAR CONTROL: yr0/yr1 cells vs the control within +-1.5% (the mechanisms hit veterans;
    the entry year must be nearly unmoved) — asserted, breaches printed loud.
ND band paths come from the disclosed extended instrument's JSON (t338_extended_DISCLOSED.py, run
first by bb_noarb33.sh); pool arms are computed here with noarb_table_allarm.py's own cohort/value
semantics (cohort = year+1 except MSD; pre-window excluded; ended/null = 0 kept in denominator)."""
import json, os, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
N33 = SP + '/o33/noarb'
CHARGE = 0.14
BANDS = ['picks 1-10', 'picks 11-20', 'picks 21-30', 'picks 31-40', 'picks 41-64']
WINDOWS = [('PRIMARY', 2005, 2023), ('MODERN', 2019, 2023)]
YEARS = list(range(0, 8))
LABELS = ['O32RFINAL', 'O33M']

OUTDOC = {'charge': CHARGE, 'labels': LABELS, 'nd': {}, 'arms': {}, 'vantage': {}, 'entry_control': {}}
L = []


def P(s=''):
    print(s); L.append(str(s))


T338 = {lab: json.load(open(N33 + '/table_EXT_%s.json' % lab)) for lab in LABELS}

P('=' * 114)
P('ORDER B — STANDING TWO-SIDED NO-ARB SUITE.  charge = 14%%/yr.  SELL-SIDE RED: yr0->1 < 0.  BUY-SIDE RED: yr0->1 > 14%%.')
P('=' * 114)
P('\n-- FIVE ND BANDS (t338 extended instrument, years 0..7 shown as mean-ratio vs the same-set yr0) --')
for lab in LABELS:
    P('\n[%s]' % lab)
    P('  %-12s %7s ' % ('band', 'n') + ' '.join('%7s' % ('yr%d' % n) for n in YEARS) +
      '  %9s %9s %9s' % ('apr0-1', 'buy-mgn', 'verdict'))
    for b in BANDS:
        rows = {r['N']: r for r in T338[lab]['groups'][b]['rows']}
        n = rows[0]['n_included']
        path = [rows[n_]['ratio_meanN_over_mean0'] if n_ in rows else None for n_ in YEARS]
        a01 = rows[1]['mean_yearN'] / rows[1]['mean_year0_same_set'] - 1.0
        mgn = CHARGE - a01
        verd = ('SELL-RED' if a01 < 0 else ('BUY-RED' if a01 > CHARGE else 'ok'))
        OUTDOC['nd'].setdefault(lab, {})[b] = dict(n=n, path=path, apprec01=round(a01, 4),
                                                   buy_margin=round(mgn, 4), verdict=verd)
        P('  %-12s %7d ' % (b, n) + ' '.join(('%7.3f' % v) if v is not None else '      -' for v in path) +
          '  %+8.1f%% %+8.1f%% %9s' % (100 * a01, 100 * mgn, verd))

# ---- pool arms --------------------------------------------------------------------------------------
ARM_TYPES = ['RD', 'MSD', 'UNR', 'IRE', 'PDA', 'PDN', 'SSP', 'PDS']


def arm_paths(matrix_path):
    D = json.load(open(matrix_path))
    R = D['recs']
    WINDOW_END = max(y for r in R for y, v in zip(r.get('yrs') or [], r.get('vpath') or []) if v is not None)

    def cohort(r):
        y = r.get('year')
        return None if y is None else (y if r.get('type') == 'MSD' else y + 1)

    def value_at(r, N):
        if N == 0:
            return float(r['v0']), 'v0'
        Y = cohort(r) + N - 1
        yrs = r.get('yrs') or []
        vp = r.get('vpath') or []
        if not yrs:
            return 0.0, 'ended'
        if Y < yrs[0]:
            return None, 'pre'
        if Y > yrs[-1]:
            return 0.0, 'ended'
        i = yrs.index(Y)
        return (0.0, 'null') if vp[i] is None else (float(vp[i]), 'path')

    elig = [r for r in R if cohort(r) is not None and (r.get('v0') or 0) > 0 and r.get('is_pool')]
    out = {}
    for wname, lo, hi in WINDOWS:
        for arm in ARM_TYPES + ['ALLPOOL']:
            pop = [r for r in elig if lo <= cohort(r) <= hi and (arm == 'ALLPOOL' or r['type'] == arm)]
            if not pop:
                continue
            path, meta = [], []
            for N in YEARS:
                reached = pop if N == 0 else [r for r in pop if cohort(r) + N - 1 <= WINDOW_END]
                vals = []
                for r in reached:
                    v, kind = value_at(r, N)
                    if kind == 'pre':
                        continue
                    vals.append((v, float(r['v0'])))
                if len(vals) < 5:
                    path.append(None); meta.append(len(vals))
                    continue
                mN = sum(v for v, _ in vals) / len(vals)
                m0 = sum(v0 for _, v0 in vals) / len(vals)
                path.append(mN / m0 if m0 > 0 else None); meta.append(len(vals))
            out[(wname, arm)] = dict(n=len(pop), path=path, n_by_year=meta)
    return out


ARMP = {lab: arm_paths(SP + '/per_entrant_%s.json' % lab) for lab in LABELS}
P('\n-- POOL ARMS (cohort clock; MSD yr1 = the debut-gap exclusion, printed not nan\'d; all-pool = every non-ND arm) --')
for lab in LABELS:
    P('\n[%s]' % lab)
    for wname, _, _ in WINDOWS:
        P('  %s window:' % wname)
        P('    %-8s %5s ' % ('arm', 'n') + ' '.join('%7s' % ('yr%d' % n) for n in YEARS) + '  %9s %9s' % ('apr0-1', 'verdict'))
        for arm in ARM_TYPES + ['ALLPOOL']:
            d = ARMP[lab].get((wname, arm))
            if d is None:
                continue
            a01 = (d['path'][1] / d['path'][0] - 1.0) if (d['path'][0] and d['path'][1] is not None) else None
            verd = ('n/a — MSD yr1 is the debut-gap exclusion (plain-words caption, never a silent nan)'
                    if (arm == 'MSD' and a01 is None) else
                    ('thin/absent' if a01 is None else
                     ('SELL-RED' if a01 < 0 else ('BUY-RED' if a01 > CHARGE else 'ok'))))
            OUTDOC['arms'].setdefault(lab, {})['%s|%s' % (wname, arm)] = dict(
                n=d['n'], path=d['path'], apprec01=(round(a01, 4) if a01 is not None else None), verdict=verd)
            P('    %-8s %5d ' % (arm, d['n']) +
              ' '.join(('%7.3f' % v) if v is not None else '      -' for v in d['path']) +
              ('  %+8.1f%% %s' % (100 * a01, verd) if a01 is not None else '        —  %s' % verd))

# ---- vantage-consistency matrix ---------------------------------------------------------------------
P('\n-- VANTAGE-CONSISTENCY MATRIX (implied growth yrV -> yrV+k vs the 14%% carry; five ND bands) --')
for lab in LABELS:
    P('\n[%s]' % lab)
    P('  %-12s %3s ' % ('band', 'V') + ' '.join('%8s' % ('k=%d' % k) for k in (1, 2, 3, 4)) + '    carry: ' +
      ' '.join('%8s' % ('%.1f%%' % (100 * (1.14 ** k - 1))) for k in (1, 2, 3, 4)))
    for b in BANDS:
        rows = {r['N']: r['ratio_meanN_over_mean0'] for r in T338[lab]['groups'][b]['rows']}
        for V in (0, 1, 2):
            gr = []
            for k in (1, 2, 3, 4):
                if V in rows and (V + k) in rows and rows[V] > 0:
                    gr.append(rows[V + k] / rows[V] - 1.0)
                else:
                    gr.append(None)
            OUTDOC['vantage'].setdefault(lab, {})['%s|V%d' % (b, V)] = [round(g, 4) if g is not None else None for g in gr]
            P('  %-12s %3d ' % (b if V == 0 else '', V) +
              ' '.join(('%+7.1f%%' % (100 * g)) if g is not None else '       -' for g in gr))
    # band-vs-band spread at each vantage, k=4
    for V in (0, 1, 2):
        g4 = [OUTDOC['vantage'][lab]['%s|V%d' % (b, V)][3] for b in BANDS]
        g4 = [g for g in g4 if g is not None]
        if len(g4) >= 2:
            P('  spread at V=%d (k=4): max-min = %.1f pts' % (V, 100 * (max(g4) - min(g4))))
            OUTDOC['vantage'][lab]['spread_V%d_k4' % V] = round(max(g4) - min(g4), 4)

# ---- ENTRY-YEAR CONTROL -----------------------------------------------------------------------------
P('\n-- ENTRY-YEAR CONTROL (the veteran mechanisms must leave the entry year nearly unmoved) --')
P('   bound: every ND-band and pool-arm yr0 and yr1 MEAN within +-1.5%% of the O32RFINAL control cell')
breaches = []
for b in BANDS:
    r_c = {r['N']: r for r in T338['O32RFINAL']['groups'][b]['rows']}
    r_n = {r['N']: r for r in T338['O33M']['groups'][b]['rows']}
    for N in (0, 1):
        c = r_c[N]['mean_yearN']; n_ = r_n[N]['mean_yearN']
        rel = n_ / c - 1.0
        ok = abs(rel) <= 0.015
        OUTDOC['entry_control']['%s|yr%d' % (b, N)] = dict(control=c, o33m=n_, rel=round(rel, 5), ok=bool(ok))
        if not ok:
            breaches.append((b, N, rel))
        P('   %-12s yr%d: control %9.1f  O33B %9.1f  %+6.2f%%  %s' % (b, N, c, n_, 100 * rel, 'ok' if ok else 'BREACH'))
for key, d in ARMP['O32RFINAL'].items():
    wname, arm = key
    d2 = ARMP['O33M'].get(key)
    if d2 is None or wname != 'PRIMARY':
        continue
    for N in (0, 1):
        if d['path'][N] is None or d2['path'][N] is None:
            continue
        rel = (d2['path'][N] / d['path'][N]) - 1.0   # ratio paths share the v0 denominator basis
        ok = abs(rel) <= 0.015
        OUTDOC['entry_control']['arm %s|yr%d' % (arm, N)] = dict(rel=round(rel, 5), ok=bool(ok))
        if not ok:
            breaches.append(('arm ' + arm, N, rel))
        P('   %-12s yr%d: path-ratio control %7.3f  O33B %7.3f  %+6.2f%%  %s' % (
            'arm ' + arm, N, d['path'][N], d2['path'][N], 100 * rel, 'ok' if ok else 'BREACH'))
P('\nENTRY-YEAR CONTROL: %s' % ('PASS — every cell inside +-1.5%' if not breaches else
                                'BREACHES: %s' % breaches))
OUTDOC['entry_control']['pass'] = not breaches

with open(os.path.join(HERE, 'STANDING_TABLES_B.json'), 'w') as f:
    json.dump(OUTDOC, f, indent=1)
with open(os.path.join(HERE, 'STANDING_TABLES_B_out.txt'), 'w') as f:
    f.write('\n'.join(L) + '\n')
print('\nwrote STANDING_TABLES_B.json / _out.txt')
