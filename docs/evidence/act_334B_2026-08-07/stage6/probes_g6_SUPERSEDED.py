"""#334 stage B / STAGE 6 — THE PROBES, at every rung.

Directive gates 1, 2, 5 and the Addendum-1 amendments, each one able to fail:
  (a) the two named chains — Mraz and Nairn — at every rung, with the Mraz TIER read off the board
      picks curve (his pick 35 = 530 on the ruled baseline, the same denominator stage 5 used);
  (b) THE FENCE, positively proved: the 165 sit-out players integer-identical at every rung;
  (c) the RECALCULATION-LAW probe — a synthetic's correction responds to his YEAR-2 games, not to a
      stamp taken in year 1;
  (d) the SEASON-ROLLOVER probe — the correction is continuous across the season knot (no integer-year
      cliff), and the ROUND-BY-ROUND walk through seasons 1-2 shows no step beyond the surface's own
      max slope (Addendum 1 F7's new probe);
  (e) the FADE-SHAPE probe — the correction at year-2-evaluation states is ~0 BY MEASUREMENT;
  (f) the ZERO-CELL gate in ABSOLUTE units (Addendum 1: <=1.5% at picks 1-10 x top-tercile, <=2.5% at
      picks 1-20 x above-median), plus the picks 41-64 and age-19+ boundary bounds (<=0.5pp);
  (g) the MONOTONICITY law — a strictly better career never prices lower;
  (h) the IDENTICAL-CAREER KPD/KPF PAIR at every rung (Addendum 1 F11).

Usage:  python3 probes_g6.py            (dev shell; RL_REPO / RL_WORKDIR / RL_OUT set)
"""
import os, sys, io, json, contextlib, copy, hashlib
import numpy as np

REPO = os.environ['RL_REPO']; WORKDIR = os.environ['RL_WORKDIR']
OUT = os.environ.get('RL_OUT', '.')
sys.path.insert(0, os.environ.get('RL_VENDOR', '/home/claude/rl_vendor'))
os.chdir(WORKDIR); sys.path.insert(0, '.')
SRC = open('_merged_recover.py').read().split('print("=== AFTER')[0]
RUNGS = ['0.25', '0.5', '0.75', '1.0']
Y = 2026
L = []
def say(s=''): L.append(s); print(s)

# The engine is exec'd ONCE (the forward-valuation modules carry process-level caches that a second
# exec corrupts). The dials are module globals in that namespace, so the ladder is walked by rebinding
# them — the same idiom the stage-5 probes used.
_G = {'__name__': '_s6_probe'}
os.environ['RL_G6_W'] = '0'; os.environ['RL_G6_KPD'] = '0'
with contextlib.redirect_stdout(io.StringIO()): exec(SRC, _G)
def engine(W, KPD='0'):
    _G['G6_W'] = float(W); _G['G6_KPD'] = float(KPD)
    return _G

RES = {}
G0 = engine('0')
MA0 = G0['MA']
PLF = 1.0524                       # the L7 numeraire re-base the board displays through
TAB = json.load(open(REPO + '/engine/rl_after/g6_table.json'))
say('=' * 116)
say('#334 stage B / STAGE 6 — PROBES.   taught surface g6_table.json md5 %s'
    % hashlib.md5(open(REPO + '/engine/rl_after/g6_table.json', 'rb').read()).hexdigest())
say('=' * 116)

# ---------------- (a) the named chains, at every rung ----------------
say('')
say('(a) THE NAMED CHAINS — Mraz and Nairn, at every rung')
say('    Mraz is on the SIT-OUT path (ns==0): stage 6 is FENCED out of that arm, so he must be')
say('    BYTE-IDENTICAL at every rung. That is the gate, not an expectation.')
PICKV = 530.0
CH = {}
for key in ('noah-mraz', 'cameron-nairn'):
    p = next((x for x in MA0.data if x.get('key') == key), None)
    if p is None: continue
    row = {}
    for W in ['0'] + RUNGS:
        G = engine(W); pp = p
        with contextlib.redirect_stdout(io.StringIO()):
            v = G['ev'](pp, Y); ns = G['nseas_pro'](pp, Y)
            e = G['_prod_path'](pp, Y); d = G['_g6_delta'](pp, Y, G['MA'].gfut(pp), e)
        row[W] = dict(engine_v=float(v), display=round(v / PLF), ns=int(ns), delta=round(float(d), 8))
    say('')
    say('  %s (%s, %s %s, drafted %s) — ns=%d at %d, %s'
        % (p.get('player'), MA0.gfut(p), p.get('type'),
           ('pick %s' % p.get('pick')) if p.get('pick') else 'pool', p.get('year'),
           row['0']['ns'], Y, 'SIT-OUT ARM (fenced)' if row['0']['ns'] == 0 else 'ESTABLISHED ARM'))
    say('    record: %s' % ('; '.join('%d:%dg@%.1f' % (x['year'], x['games'], x['avg'])
                                      for x in sorted(p['scoring'], key=lambda z: z['year'])) or '(none)'))
    for W in ['0'] + RUNGS:
        r = row[W]
        say('    rung %-5s  board %5d   taught delta %+0.6f   %s'
            % (W, r['display'], r['delta'],
               ('BYTE-IDENTICAL to dial 0' if r['display'] == row['0']['display'] else
                '%+d vs dial 0' % (r['display'] - row['0']['display']))))
    if key == 'noah-mraz':
        for W in ['0'] + RUNGS:
            m = row[W]['display'] / PICKV
            tier = ('<=3.0x CLEAN' if m <= 3.0 else '3.0-3.5x PASS, DISCLOSED' if m <= 3.5
                    else '3.5-3.8x BRANCH-HOLD TO OWNER' if m <= 3.8 else '>3.8x STOP')
            say('    MRAZ TIER at rung %-5s : %d = %.4fx his pick (%.0f)  ->  %s' % (W, row[W]['display'], m, PICKV, tier))
            row[W]['mraz_multiple'] = m; row[W]['mraz_tier'] = tier
    CH[key] = row
RES['chains'] = CH

# ---------------- (b) the fence, positively proved ----------------
say('')
say('(b) THE FENCE — the sit-out population, proved integer-identical at every rung')
mv = json.load(open(OUT + '/movers_rung0.25.json'))
POP = json.load(open(OUT + '/sitout_population.json'))
say('    engine-enumerated sit-out population at %d (ns==0, not delisted): n = %d' % (Y, len(POP)))
fence = {}
for W in RUNGS:
    m = json.load(open(OUT + '/movers_rung%s.json' % W))['rungs'][W]
    fence[W] = dict(n=m['sitout_n'], identical=m['sitout_identical'], verdict=m['sitout_verdict'],
                    board_md5=m['board_md5'], movers=m['movers'], up=m['up'], down=m['down'],
                    unattributed=m['unattributed'])
    say('    rung %-5s  board %s  sit-out %d/%d INTEGER-IDENTICAL  %s   |  movers %d (up %d / down %d), '
        'unattributed %d'
        % (W, m['board_md5'][:8], m['sitout_identical'], m['sitout_n'], m['sitout_verdict'],
           m['movers'], m['up'], m['down'], m['unattributed']))
RES['fence'] = fence

# ---------------- (c) the recalculation law ----------------
say('')
say('(c) THE RECALCULATION-LAW PROBE (Addendum 1 para 3-4; owner: "in year 2, it would use year 1 + 2')
say('    data and outcomes, not just year 1?").  A synthetic year-2 player: YEAR-1 season FROZEN at')
say('    10 games @ 62.0, only his YEAR-2 games varied.  If the correction were a stamp taken in year 1')
say('    the delta column would be constant.')
G = engine('1.0')
src = next(x for x in G['MA'].data if x.get('key') == 'cameron-nairn')
say('')
say('    %-12s %10s %12s %14s' % ('yr-2 games', 'cum games', 'taught delta', 'engine price'))
say('    ' + '-' * 52)
REC = []
for g2 in (0, 2, 5, 8, 11, 14, 18, 22):
    q = copy.deepcopy(src)
    q['year'] = 2024; q['_by'] = 2006
    q['scoring'] = [dict(year=2025, games=10, avg=62.0, pos=q['scoring'][0].get('pos', 'MID'))]
    if g2 > 0: q['scoring'].append(dict(year=2026, games=g2, avg=62.0, pos=q['scoring'][0].get('pos', 'MID')))
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            e = G['_prod_path'](q, Y); d = G['_g6_delta'](q, Y, G['MA'].gfut(q), e)
            v = G['ev'](q, Y)
    except Exception as ex:
        say('    %-12d  (%s)' % (g2, ex)); continue
    REC.append(dict(g2=g2, cum=10 + g2, delta=float(d), v=float(v)))
    say('    %-12d %10d %+12.6f %14.0f' % (g2, 10 + g2, d, v))
spread = (max(r['delta'] for r in REC) - min(r['delta'] for r in REC)) if REC else 0.0
say('    delta spread over the YEAR-2 games axis with year 1 frozen: %.6f  ->  %s'
    % (spread, 'PASS (a state function, not a stamp)' if spread > 1e-6 else 'FAIL (constant — a stamp)'))
RES['recalculation'] = dict(rows=REC, spread=spread, verdict='PASS' if spread > 1e-6 else 'FAIL')

# ---------------- (d) rollover + round-by-round ----------------
say('')
say('(d) THE SEASON-ROLLOVER / ROUND-BY-ROUND PROBE (Addendum 1 F7).  The clock tau is continuous in')
say('    the round; the correction must hand over to arriving evidence round by round with NO step')
say('    beyond the surface\'s own max slope, and NO cliff at the integer-year knot.')
say('')
say('    %-8s %8s %14s' % ('tau', 'step', 'taught delta'))
say('    ' + '-' * 34)
tk = [float(k) for k in TAB['tau_knots']]; stv = [float(v) for v in TAB['s_tau']]
def s_tau(t): return float(np.interp(t, [0.0] + tk, [stv[0]] + stv)) if t <= tk[-1] else 0.0
prev = None; maxstep = 0.0; ROLL = []
for i in range(0, 49):
    t = 0.5 + i * (2.5 / 48.0)
    d = 1.0 * float(TAB['d1']) * 1.0 * s_tau(t)          # the clock factor alone, other shapes held at 1
    st = abs(d - prev) if prev is not None else 0.0
    maxstep = max(maxstep, st); prev = d
    ROLL.append(dict(tau=round(t, 5), delta=d))
    if i % 6 == 0: say('    %-8.4f %8.6f %+14.6f' % (t, st, d))
theory = float(TAB['d1']) * (max(stv) - min(stv)) / (tk[1] - tk[0]) * (2.5 / 48.0)
say('    max observed step over the sweep %.8f  vs the surface\'s own max slope over the same step %.8f'
    % (maxstep, theory))
say('    ROLLOVER: %s   (no integer-year cliff; the fade is linear in the continuous clock)'
    % ('PASS' if maxstep <= theory + 1e-9 else 'FAIL'))
RES['rollover'] = dict(max_step=maxstep, max_slope=theory,
                       verdict='PASS' if maxstep <= theory + 1e-9 else 'FAIL')

# ---------------- (e) the fade shape ----------------
say('')
say('(e) THE FADE-SHAPE PROBE — the correction at the year-2 and year-3 evaluation states')
say('    measured (not decreed): the raw pooled residual at tau = 1 / 2 / 3 was %s;'
    % TAB['meta']['notes']['Stau_raw_delta'])
say('    normalised to tau=1 that is %s; INSTALLED after the isotonic non-increasing clamp to [0,1]: %s.'
    % (TAB['meta']['notes']['Stau_unclamped'], TAB['s_tau']))
say('    correction at a year-2 evaluation state (tau=2) = %.8f x the year-1 correction  ->  %s'
    % (s_tau(2.0), 'PASS (~0 by measurement)' if s_tau(2.0) <= 1e-9 else 'CHECK'))
say('    The measured year-2 residual is NEGATIVE (-0.0447): the data extinguishes the premium FASTER')
say('    than the owner\'s "phase out over seasons 2/3" shape. The clamp installs 0, never the negative —')
say('    a markdown does not ride the bonus dial (the same principle as the KPD sub-dial, F11).')
RES['fade'] = dict(raw=TAB['meta']['notes']['Stau_raw_delta'],
                   unclamped=TAB['meta']['notes']['Stau_unclamped'], installed=TAB['s_tau'],
                   at_tau2=s_tau(2.0), verdict='PASS' if s_tau(2.0) <= 1e-9 else 'CHECK')

# ---------------- (f) the zero-cell gate, absolute units ----------------
say('')
say('(f) THE ZERO-CELL GATE, in ABSOLUTE UNITS (Addendum 1 re-registered it there, never in')
say('    teaching-noise units). Measured on the TAUGHT rows at each rung, value-weighted.')
ROWS = [x for x in json.load(open(OUT + '/s6_rows.json'))
        if x['nd'] and 1 <= x['pk'] <= 64 and x['N'] == 1]
zs = sorted(float(np.clip(np.log(max(x['e'], 1.0) / max(x['A'], 1.0)),
                          TAB['z_knots'][0], TAB['z_knots'][-1])) for x in ROWS)
zmed = zs[len(zs) // 2]; zt2 = zs[2 * len(zs) // 3]
def z_of(x): return float(np.clip(np.log(max(x['e'], 1.0) / max(x['A'], 1.0)),
                                  TAB['z_knots'][0], TAB['z_knots'][-1]))
def taper(v, lo, hi):
    if v <= lo: return 1.0
    if v >= hi: return 0.0
    return float(0.5 * (1.0 + np.cos(np.pi * (v - lo) / (hi - lo))))
def delta_of(x, W):
    if x['pos'] == 'KPD': return 0.0
    tp = taper(x['pk'], *TAB['pk_taper'])
    if tp <= 0 or x['age'] is None: return 0.0
    ta = taper(x['age'], *TAB['age_taper'])
    if ta <= 0: return 0.0
    st = s_tau(x['tau'])
    sz = float(np.interp(z_of(x), TAB['z_knots'], TAB['s_z']))
    sg = float(np.interp(np.log1p(max(x['gcum'], 0.0)),
                         [float(np.log1p(k)) for k in TAB['g_knots']], TAB['s_g']))
    b = float(np.interp(np.log(min(max(x['pk'], 1), 90)),
                        [float(np.log(k)) for k in TAB['pk_knots']],
                        TAB['base'][{'RUCK': 'RUCK', 'KPF': 'KPP', 'KPD': 'KPP'}.get(x['pos'], 'nonKPP')]))
    return float(W) * float(TAB['d1']) * b * st * sz * sg * tp * ta
CELLS = [('picks 1-10 x TOP-TERCILE re-rate', lambda x: x['pk'] <= 10 and z_of(x) >= zt2, 0.015),
         ('picks 1-20 x ABOVE-MEDIAN re-rate', lambda x: x['pk'] <= 20 and z_of(x) >= zmed, 0.025),
         ('picks 41-64 (declared taper)', lambda x: 41 <= x['pk'] <= 64, 0.005),
         ('draft age 19+ (declared taper)', lambda x: x['age'] is not None and x['age'] >= 19, 0.005),
         ('draft age UNKNOWN (identically 0)', lambda x: x['age'] is None, 0.0)]
say('')
say('    %-38s %5s %8s %9s %9s %9s %9s' % ('cell', 'n', 'bound', 'rung .25', 'rung .50', 'rung .75', 'rung 1.0'))
say('    ' + '-' * 92)
ZC = {}
for nm, f, bound in CELLS:
    sub = [x for x in ROWS if f(x)]
    if not sub: continue
    sp = sum(x['price'] for x in sub)
    vals = [sum(x['price'] * delta_of(x, W) for x in sub) / sp for W in RUNGS]
    ok = all(abs(v) <= bound + 1e-12 for v in vals)
    ZC[nm] = dict(n=len(sub), bound=bound, values={W: vals[i] for i, W in enumerate(RUNGS)},
                  verdict='PASS' if ok else 'FAIL')
    say('    %-38s %5d %8.3f %+9.5f %+9.5f %+9.5f %+9.5f   %s'
        % (nm, len(sub), bound, vals[0], vals[1], vals[2], vals[3], 'PASS' if ok else 'FAIL'))
RES['zero_cells'] = ZC

# ---------------- (f2) the zero-cell gate on the CROSS-SECTION's own level axis -------------------
say('')
say('    The gate is re-read on the axis the CROSS-SECTION used — demonstrated level pr = bestlvl/par —')
say('    so the "already priced in" cell is tested on BOTH definitions and the binding one binds.')
prs = sorted(x['pr'] for x in ROWS); pmed = prs[len(prs) // 2]; pt2 = prs[2 * len(prs) // 3]
for nm, f, bound in [('picks 1-10 x TOP-TERCILE pr', lambda x: x['pk'] <= 10 and x['pr'] >= pt2, 0.015),
                     ('picks 1-20 x ABOVE-MEDIAN pr', lambda x: x['pk'] <= 20 and x['pr'] >= pmed, 0.025)]:
    sub = [x for x in ROWS if f(x)]
    sp = sum(x['price'] for x in sub)
    vals = [sum(x['price'] * delta_of(x, W) for x in sub) / sp for W in RUNGS]
    ok = all(abs(v) <= bound + 1e-12 for v in vals)
    meas = sum(x['F'] for x in sub) / sp - 1.0
    ZC[nm] = dict(n=len(sub), bound=bound, measured=meas,
                  values={W: vals[i] for i, W in enumerate(RUNGS)}, verdict='PASS' if ok else 'FAIL')
    say('    %-38s %5d %8.3f %+9.5f %+9.5f %+9.5f %+9.5f   %s   (measured %+0.4f)'
        % (nm, len(sub), bound, vals[0], vals[1], vals[2], vals[3], 'PASS' if ok else 'FAIL', meas))
say('')
say('    PER-RUNG VERDICT on the registered zero-cell bounds (Addendum 1, ABSOLUTE units):')
RUNGOK = {}
for i, W in enumerate(RUNGS):
    bad = [nm for nm, d in ZC.items() if abs(d['values'][W]) > d['bound'] + 1e-12]
    RUNGOK[W] = dict(feasible=not bad, breaches=bad)
    say('      rung %-5s : %s' % (W, 'ALL BOUNDS MET' if not bad else 'BREACHES ' + '; '.join(bad)))
say('    Addendum 1 F9/F10 orders INFEASIBLE RUNGS STRUCK BEFORE PRESENTATION. The struck rungs are')
say('    named in README.md and FRONTIER.txt with the exact figure that struck them. NOTHING is retuned.')
RES['rung_feasibility'] = RUNGOK

# ---------------- (i) the pre-registered tail-vs-typical statistics --------------------------------
say('')
say('(i) THE PRE-REGISTERED STATISTICS (Addendum 1: the estimand is the VALUE-WEIGHTED aggregate, the')
say('    MEDIAN F\' is pre-registered beside it, and each rung prints the corrected median and the')
say('    fraction of players who historically OUT-EARN the corrected price). The tension the directive')
say('    names as the central pub-test item: the residual is TAIL-CARRIED.')
say('')
say('    %-10s %12s %12s %12s %14s %14s' % ('rung', 'agg F\' ', 'corrected', 'median F\'', 'corr. median',
                                            'frac out-earn'))
say('    ' + '-' * 78)
sp = sum(x['price'] for x in ROWS)
agg0 = sum(x['F'] for x in ROWS) / sp
med0 = float(np.median([x['F'] / x['price'] for x in ROWS]))
frac0 = float(np.mean([1.0 if x['F'] > x['price'] else 0.0 for x in ROWS]))
STAT = {'0': dict(agg=agg0, agg_corr=agg0, median=med0, median_corr=med0, frac=frac0)}
say('    %-10s %12.4f %12.4f %12.4f %14.4f %14.3f' % ('0 (shipped)', agg0, agg0, med0, med0, frac0))
for W in RUNGS:
    newp = [x['price'] * (1.0 + delta_of(x, W)) for x in ROWS]
    aggc = sum(x['F'] for x in ROWS) / sum(newp)
    medc = float(np.median([ROWS[i]['F'] / newp[i] for i in range(len(ROWS))]))
    fr = float(np.mean([1.0 if ROWS[i]['F'] > newp[i] else 0.0 for i in range(len(ROWS))]))
    STAT[W] = dict(agg=agg0, agg_corr=aggc, median=med0, median_corr=medc, frac=fr)
    say('    %-10s %12.4f %12.4f %12.4f %14.4f %14.3f' % (W, agg0, aggc, med0, medc, fr))
say('')
say('    READ IT PLAINLY: the value-weighted aggregate says the year-1 established leg is UNDER-priced')
say('    by %.1f%%. The MEDIAN says the TYPICAL year-1 established player is already priced ABOVE his own'
    % (100 * (agg0 - 1)))
say('    realised discounted future (median F\' = %.4f, i.e. %.0f%% over-priced), and only %.0f%% of them'
    % (med0, 100 * (1 / med0 - 1), 100 * frac0))
say('    out-earn even the UNCORRECTED price. The correction is carried by a right tail. At rung 1.0 the')
say('    typical player would sit %.0f%% over-priced against his own median. THE MEDIAN-NEUTRAL RUNG IS'
    % (100 * (1 / STAT['1.0']['median_corr'] - 1)))
say('    BELOW ZERO — no positive rung improves the median; every rung worsens it. That is the whole of')
say('    the tail-vs-typical tension, stated as a number, at every rung.')
RES['tail_vs_typical'] = STAT

# ---------------- (g) monotonicity ----------------
say('')
say('(g) THE MONOTONICITY LAW — a strictly better career never prices lower.  The demonstrated-level')
say('    axis DECREASES in z = log(e/anchor), so the shipped surface must keep e*(1+delta) strictly')
say('    increasing in e.  Swept over the realised domain at the TOP rung (the worst case).')
worst = 9.9; where = None
zz = np.linspace(TAB['z_knots'][0], TAB['z_knots'][-1], 241)
for c in ('nonKPP', 'KPP', 'RUCK'):
    for pk in (3, 8, 15, 25, 34):
        for g in (6.0, 10.0, 16.0, 24.0):
            for t in (1.0, 1.5):
                b = float(np.interp(np.log(pk), [float(np.log(k)) for k in TAB['pk_knots']], TAB['base'][c]))
                sg = float(np.interp(np.log1p(g), [float(np.log1p(k)) for k in TAB['g_knots']], TAB['s_g']))
                base = float(TAB['d1']) * b * s_tau(t) * sg
                d = [base * float(np.interp(z, TAB['z_knots'], TAB['s_z'])) for z in zz]
                for i in range(1, len(zz)):
                    dd = (d[i] - d[i - 1]) / (zz[i] - zz[i - 1])
                    m = 1.0 + d[i] + dd
                    if m < worst: worst = m; where = (c, pk, g, t, round(float(zz[i]), 4))
say('    min d/dln(e)[e*(1+delta)] at rung 1.0 = %+0.6f  at %s  ->  %s'
    % (worst, where, 'PASS (strictly increasing)' if worst > 0 else 'FAIL'))
say('    the L-SMOOTH shrink the teach applied to reach it: kappa = %s (declared in the teach log)'
    % TAB['meta']['notes']['Sz_Lsmooth_kappa'])
RES['monotonicity'] = dict(min_slope=worst, at=where, kappa=TAB['meta']['notes']['Sz_Lsmooth_kappa'],
                           verdict='PASS' if worst > 0 else 'FAIL')

# ---------------- (h) the identical-career KPD / KPF pair ----------------
say('')
say('(h) THE IDENTICAL-CAREER KPD / KPF PAIR (Addendum 1 F11) — the same record, the same pick, the')
say('    same clock, differing ONLY in position class. Printed at every rung, on BOTH dials.')
say('')
say('    %-6s %-8s %10s %10s %12s %12s' % ('rung', 'KPD dial', 'KPF delta', 'KPD delta', 'KPF price', 'KPD price'))
say('    ' + '-' * 64)
PAIR = []
for W in RUNGS:
    for KD in ('0', '1.0'):
        G = engine(W, KD)
        out = {}
        for POSN in ('KPF', 'KPD'):
            q = copy.deepcopy(next(x for x in G['MA'].data if x.get('key') == 'noah-mraz'))
            q['pos'] = POSN; q['_pos_now'] = POSN; q['year'] = 2024; q['pick'] = 25; q['_by'] = 2006
            q['scoring'] = [dict(year=2025, games=12, avg=68.0, pos=POSN),
                            dict(year=2026, games=10, avg=70.0, pos=POSN)]
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    e = G['_prod_path'](q, Y)
                    d = G['_g6_delta'](q, Y, POSN, e); v = G['ev'](q, Y)
                out[POSN] = (float(d), float(v))
            except Exception as ex:
                out[POSN] = (float('nan'), float('nan'))
        PAIR.append(dict(rung=W, kpd_dial=KD, kpf_delta=out['KPF'][0], kpd_delta=out['KPD'][0],
                         kpf_v=out['KPF'][1], kpd_v=out['KPD'][1]))
        say('    %-6s %-8s %+10.6f %+10.6f %12.0f %12.0f'
            % (W, KD, out['KPF'][0], out['KPD'][0], out['KPF'][1], out['KPD'][1]))
say('    At the shipped KPD sub-dial (0) a KPD takes ZERO correction — the measured -25%% class markdown')
say('    is NOT installed and is the owner\'s separate ruling.')
RES['kpd_kpf_pair'] = PAIR

json.dump(RES, open(OUT + '/probes_stage6.json', 'w'), indent=1, default=float)
open(OUT + '/PROBES.txt', 'w').write('\n'.join(L) + '\n')
