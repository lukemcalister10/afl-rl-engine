#!/usr/bin/env python3
"""ORDER 21 -- the two cohort instruments' readings, SHIP vs the STAGED configuration, with the
no-arbitrage margin against the owner's 14% carry charge.

  margin vs 14%  =  14%  -  (cohort year-0 -> year-1 appreciation)
  a NEGATIVE margin is an arbitrage: the book appreciates faster than the charge to hold it.

Both instruments are the canonical files, copied and UNMODIFIED (noarb_table_338.py md5
0f8220351c64c56ccfa90c60edcdfa5f, asserted by noarb_table_allarm.py at run and re-asserted here).
  usage: python noarb_margins.py
"""
import os, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
N = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o21/noarb'
PINS = {
    'board': ('data/rl_build/rl_app_data.json', '1dbd1480a34c7823f330273211cbb76a'),
    'store': ('engine/rl_after/rl_model_data.json', 'd9a24282357cf3083b1640466e3ecd83'),
    'instrument': ('docs/evidence/composition_2026-08-10/noarb/noarb_table_338.py',
                   '0f8220351c64c56ccfa90c60edcdfa5f'),
}
CHARGE = 0.14


def _md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


def assert_pins(when):
    bad = ["%s %s != %s (%s)" % (k, _md5(os.path.join(ROOT, r)), e, r)
           for k, (r, e) in PINS.items() if _md5(os.path.join(ROOT, r)) != e]
    if bad: raise SystemExit("PIN ASSERTION FAILED (%s): %s" % (when, bad))


assert_pins('entry')
assert _md5(os.path.join(N, 'noarb_table_338.py')) == PINS['instrument'][1], "the run copy differs"

OUT = []


def P(s=''):
    print(s); OUT.append(s)


LABS = ('SHIP', 'DERIVED')
AA = {L: json.load(open(os.path.join(N, 'allarm_%s.json' % L))) for L in LABS}
TB = {L: json.load(open(os.path.join(N, 'table_%s.json' % L))) for L in LABS}
DATA = {}

P("=" * 114)
P("ORDER 21 -- BOTH COHORT INSTRUMENTS UNDER THE STAGED CONFIGURATION")
P("=" * 114)
P("  pins asserted at entry: board 1dbd1480..  store d9a24282..  instrument 0f822035..")
P("  instrument copy actually run: noarb_table_338.py %s (UNMODIFIED)"
  % _md5(os.path.join(N, 'noarb_table_338.py')))
P("  allarm's own assertion of that md5, recorded in its output: %s"
  % AA['SHIP'].get('canonical_instrument_md5'))
P()
P("  SHIP     = HEAD defaults on the ADOPTED engine (main c330169, the par fix landed).")
P("             engine_head a8071af4.  matrix per_entrant_O21SHIP.json")
P("  DERIVED  = ** THE STAGED CONFIGURATION **: RL_H_POOLSIT=1.0 RL_H_UNION=1.0 and the ONE derived")
P("             object at BOTH pool read sites (R at sitout_ev, U at _a_blend).")
P("             engine_head 54347ed4.  matrix per_entrant_O21DERIVED.json")
P("  store pin carried on both matrices: %s / %s" % (AA['SHIP']['store'], AA['DERIVED']['store']))
P("  v0 surface pin carried on both:     %s / %s" % (AA['SHIP']['v0surf'], AA['DERIVED']['v0surf']))
P()
P("  NOTE ON THE BASELINE. ORDER 19's readings were taken on the SUPERSEDED board/engine")
P("  (94f1fec5, pre-par-fix): PRIMARY yr1 0.8850, legacy yr1 1.0884. The par fix moved BOTH")
P("  baselines. Everything below is SHIP-vs-STAGED on the SAME adopted engine; ORDER 19's numbers")
P("  are not comparable across that boundary and are not used as a baseline here.")
P()


def ratios(rows):
    return {int(r['N']): float(r['ratio_meanN_over_mean0']) for r in rows}


P("=" * 114)
P("A. THE ALL-ARM DECIDING INSTRUMENT -- noarb_table_allarm.py")
P("=" * 114)
P("  Owner's cohort definition: every player drafted through mechanisms eligible to debut in the")
P("  SAME year. ND + RD + SSP of year Y sit with MSD of year Y+1. THIS is the deciding instrument.")
P()
ALL = {}
for gname in ('PRIMARY  cohorts 2005-2023', 'MODERN   cohorts 2019-2023'):
    g0 = AA['SHIP']['groups'][gname]
    P("-" * 114)
    P("### %s    n = %d" % (gname, g0['n']))
    P("-" * 114)
    P("  %-10s %8s %8s %8s %8s %8s %8s | %12s %15s %11s"
      % ('variant', 'yr0', 'yr1', 'yr2', 'yr3', 'yr4', 'yr5', 'apprec 0->1', 'margin vs 14%', 'verdict'))
    P("  " + "-" * 106)
    res = {}
    for L in LABS:
        rt = ratios(AA[L]['groups'][gname]['rows'])
        ap = rt[1] - 1.0; mg = CHARGE - ap
        res[L] = dict(ratio=[rt.get(i) for i in range(6)], apprec=ap, margin=mg)
        P("  %-10s %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f | %+11.2f%% %+14.2f%% %11s"
          % (L, rt[0], rt[1], rt[2], rt[3], rt[4], rt[5], 100 * ap, 100 * mg,
             'no arb' if mg > 0 else '** ARBITRAGE **'))
    P("  yr1 ratio moves %+.4f ; margin moves %+.2f points (toward the bound if negative)."
      % (res['DERIVED']['ratio'][1] - res['SHIP']['ratio'][1],
         100 * (res['DERIVED']['margin'] - res['SHIP']['margin'])))
    ALL[gname] = res
    P()
DATA['allarm'] = ALL

P("=" * 114)
P("B. BY ARM, PRIMARY WINDOW -- where the staged object actually acts")
P("=" * 114)
BYARM = {}
for gname in ('PRIMARY  cohorts 2005-2023', 'MODERN   cohorts 2019-2023'):
    a0, a1 = AA['SHIP']['groups'][gname]['by_arm'], AA['DERIVED']['groups'][gname]['by_arm']
    P("  --- %s ---" % gname)
    P("  %-8s %7s %11s %11s %10s | %11s %11s %10s"
      % ('arm', 'n', 'yr1 SHIP', 'yr1 STAGED', 'move', 'yr4 SHIP', 'yr4 STAGED', 'move'))
    P("  " + "-" * 92)
    for arm in sorted(a0, key=lambda a: -(a0[arm]['n'] if isinstance(a0[a], dict) else 0)) if False else a0:
        s, t = a0[arm], a1[arm]

        def f(x):
            return ('%.4f' % x) if isinstance(x, (int, float)) and x == x else 'nan'

        def mv(k):
            x, y = s.get(k), t.get(k)
            ok = all(isinstance(z, (int, float)) and z == z for z in (x, y))
            return ('%+.4f' % (y - x)) if ok else '-'

        P("  %-8s %7s %11s %11s %10s | %11s %11s %10s"
          % (arm, s.get('n'), f(s.get('yr1')), f(t.get('yr1')), mv('yr1'),
             f(s.get('yr4')), f(t.get('yr4')), mv('yr4')))
    BYARM[gname] = dict(SHIP=a0, DERIVED=a1)
    P()
DATA['by_arm'] = BYARM

P("=" * 114)
P("C. THE LEGACY RETAINED INSTRUMENT -- noarb_table_338.py, UNMODIFIED")
P("=" * 114)
P("  Population = teaches_curve & pick 1..64 & draft years 2004-2022, n = %d."
  % TB['SHIP']['groups']['ALL picks 1-64']['cohort_n'])
P("  NATIONAL BY CONSTRUCTION, so a pool-only object has nothing to act on. It is retained because")
P("  the owner retained it, and here it doubles as the SEPARATION CHECK with a cohort instrument")
P("  attached rather than a board diff.")
P()
LG = {}
for gname in TB['SHIP']['groups']:
    P("  --- %s   (n=%d) ---" % (gname, TB['SHIP']['groups'][gname]['cohort_n']))
    P("  %-10s %8s %8s %8s %8s %8s %8s | %12s %15s %11s"
      % ('variant', 'yr0', 'yr1', 'yr2', 'yr3', 'yr4', 'yr5', 'apprec 0->1', 'margin vs 14%', 'verdict'))
    row = {}
    for L in LABS:
        rt = ratios(TB[L]['groups'][gname]['rows'])
        ap = rt[1] - 1.0; mg = CHARGE - ap
        row[L] = dict(ratio=[rt.get(i) for i in range(6)], apprec=ap, margin=mg)
        P("  %-10s %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f | %+11.2f%% %+14.2f%% %11s"
          % (L, rt[0], rt[1], rt[2], rt[3], rt[4], rt[5], 100 * ap, 100 * mg,
             'no arb' if mg > 0 else '** ARBITRAGE **'))
    same = all(row['DERIVED']['ratio'][i] == row['SHIP']['ratio'][i] for i in range(6))
    P("  IDENTICAL to the published precision across all six years: %s" % same)
    LG[gname] = row
    P()
DATA['legacy'] = LG
sc = {L: AA[L]['groups']['self_check_canonical'] for L in LABS}
P("  SELF-CHECK (P7.1): allarm's own read of the canonical population, n=%d" % sc['SHIP']['n'])
for L in LABS:
    P("    %-8s %s" % (L, "  ".join("yr%s %.4f" % (k, v) for k, v in sorted(sc[L]['ratios'].items(),
                                                                           key=lambda kv: int(kv[0])))))
P("    matches noarb_table_338.py's own ALL picks 1-64 ratios: %s"
  % all(abs(sc[L]['ratios'][str(i)] - ratios(TB[L]['groups']['ALL picks 1-64']['rows'])[i]) < 1e-9
        for L in LABS for i in range(6)))
P()

P("=" * 114)
P("D. THE VERDICT")
P("=" * 114)
allm = [("all-arm %s" % k.split()[0], v['DERIVED']['margin']) for k, v in ALL.items()]
allm += [("legacy %s" % k, v['DERIVED']['margin']) for k, v in LG.items()]
P("  every margin measured under the STAGED configuration:")
for k, m in allm:
    P("    %-28s %+8.2f%%   %s" % (k, 100 * m, 'no arb' if m > 0 else '** ARBITRAGE **'))
P()
P("  ARBITRAGES OPENED BY THE STAGED CONFIGURATION: %d of %d readings"
  % (sum(1 for _, m in allm if m <= 0), len(allm)))
DATA['verdict'] = dict(margins={k: m for k, m in allm}, arbitrages=sum(1 for _, m in allm if m <= 0))
json.dump(DATA, open(os.path.join(HERE, 'NOARB_MARGINS.json'), 'w'), indent=1)
P()
P("wrote NOARB_MARGINS.json  md5 %s" % _md5(os.path.join(HERE, 'NOARB_MARGINS.json')))
assert_pins('exit')
P("PINS RE-ASSERTED AT EXIT -- all three UNMOVED.")
open(os.path.join(HERE, 'noarb_margins_out.txt'), 'w').write("\n".join(OUT) + "\n")
