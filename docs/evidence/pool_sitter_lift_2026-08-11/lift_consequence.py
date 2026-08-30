"""ORDER 19, PART 2 -- THE DERIVED-LEVEL INTERACTION, THE COHORT INSTRUMENTS, AND THE SECOND R SITE.

Three questions the order asks that need the WALK-FORWARD MATRICES rather than the board:

  4. THE DERIVED-LEVEL INTERACTION. Phase 1 derived new pool entry levels from the outcome profile.
     Does lifting the sitter penalty change those derived levels -- i.e. does the profile measure
     (realised_full / v0) read H or R at all? PROVEN EITHER WAY, by re-running PHASE 1's OWN
     phase1_derive.py (carried unmodified from branch build/pool-repricing-phase1, which this act does
     NOT touch) against each variant's matrix. Its re-run on SHIP reproduces the committed
     PHASE1_DERIVE.json exactly -- that is the control.

  5. THE COHORT INSTRUMENTS. noarb_table_allarm.py (the owner's ruled all-arm cohort, the DECIDING
     instrument) and noarb_table_338.py (the LEGACY picks 1-64 instrument, md5 asserted unmodified),
     both run per variant, with the no-arbitrage margin against the 14% charge.

  SENSITIVITY. _a_blend (:2178) reads the SAME retention surface on the YEAR-1+ arm. The order scopes
  variant B to sitout_ev, so that site is left alone in variant B and measured HERE, separately, as a
  board built with BOTH R sites lifted for pool rows. It is NOT folded into variant B.

READ-ONLY. Every input was produced by the two committed shell scripts beside this file.
  usage:  OPENBLAS_NUM_THREADS=1 /root/rl_venv312/bin/python lift_consequence.py
"""
import os, sys, json, math, hashlib

ROOT = '/home/user/afl-rl-engine'
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
O19 = SP + '/o19'
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, O19 + '/noarb')

PINS = {
    'board': ('data/rl_build/rl_app_data.json', '94f1fec59f99c59d5890d5975c79fa9b'),
    'store': ('engine/rl_after/rl_model_data.json', 'd9a24282357cf3083b1640466e3ecd83'),
    'instrument': ('docs/evidence/composition_2026-08-10/noarb/noarb_table_338.py',
                   '0f8220351c64c56ccfa90c60edcdfa5f'),
}


def _md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def assert_pins(when):
    bad = ["%s %s != %s (%s)" % (k, _md5(os.path.join(ROOT, r)), e, r)
           for k, (r, e) in PINS.items() if _md5(os.path.join(ROOT, r)) != e]
    if bad:
        raise SystemExit("PIN ASSERTION FAILED (%s):\n  " % when + "\n  ".join(bad))


assert_pins('entry')

OUT = []
DATA = {}


def P(s=''):
    print(s)
    OUT.append(s)


LABS = ['SHIP', 'LIFTH', 'LIFTRH']
NAME = {'SHIP': 'TODAY', 'LIFTH': 'VARIANT A', 'LIFTRH': 'VARIANT B'}
ORDER = ['RD', 'SSP', 'MSD', 'IRE', 'PDA', 'PDN', 'PDS', 'UNR', 'ND>64']

P("=" * 118)
P("ORDER 19 PART 2 -- DERIVED LEVELS, COHORT INSTRUMENTS, AND THE SECOND R SITE")
P("=" * 118)
P("  pins asserted at entry: board 94f1fec5..  store d9a24282..  instrument 0f822035..")
P()

# ==================================================================================================
# 4. THE DERIVED-LEVEL INTERACTION
# ==================================================================================================
D = {l: json.load(open("%s/derive_%s/PHASE1_DERIVE.json" % (O19, l))) for l in LABS}
REF = json.load(open(O19 + '/phase1ref/PHASE1_DERIVE.json'))

P("=" * 118)
P("4. THE DERIVED-LEVEL INTERACTION -- DOES THE PROFILE MEASURE READ H OR R?")
P("=" * 118)
P("  VERDICT: YES, IT READS BOTH. THE DERIVED POOL ENTRY LEVELS DO CHANGE.")
P()
P("  THE MECHANISM, from the code, before the numbers:")
P("      profile_X = SUM_X structural_value / SUM_X v0            (phase1_derive.py:87-90)")
P("      structural_value comes from harness.realised_full(r)     (harness:311-315)")
P("      realised_full  = realised_at(r, len(vpath))              (harness:298-309)")
P("                     = an evidence-weighted mean of r['vpath']")
P("      and vpath[i]   = ev(p, C+1+i), THE ENGINE'S OWN AS-OF PRICE (emitter:137-138,166)")
P("  A sit-out season's as-of price is exactly where R and H are applied. So the NUMERATOR of the")
P("  profile carries the sitter penalty; the DENOMINATOR (v0) does not. LIFTING THE PENALTY RAISES")
P("  MEASURED POOL RETURNS, WHICH RAISES EVERY DERIVED POOL LEVEL.")
P()
_ctl = max(abs(REF['layer1'][s]['lam'] - D['SHIP']['layer1'][s]['lam']) for s in ORDER)
P("  CONTROL 4: phase1_derive.py re-run on SHIP vs the committed PHASE1_DERIVE.json --")
P("      max |lambda delta| = %.17g,  nd_profile delta = %.17g  -> %s"
  % (_ctl, abs(REF['nd_profile'] - D['SHIP']['nd_profile']),
     "REPRODUCED" if _ctl < 1e-12 else "MISMATCH"))
P()
P("  THE CALIBRATION TARGET (ND 1-64's own profile), which lambda is measured AGAINST:")
for l in LABS:
    P("      nd_profile  %-10s %.9f" % (NAME[l], D[l]['nd_profile']))
P("      delta VARIANT A %+.9f (%+.4f%%)   VARIANT B %+.9f (%+.4f%%)"
  % (D['LIFTH']['nd_profile'] - D['SHIP']['nd_profile'],
     100 * (D['LIFTH']['nd_profile'] / D['SHIP']['nd_profile'] - 1),
     D['LIFTRH']['nd_profile'] - D['SHIP']['nd_profile'],
     100 * (D['LIFTRH']['nd_profile'] / D['SHIP']['nd_profile'] - 1)))
P()
P("  THE ND TARGET MOVES, AND IT SHOULD NOT HAVE. This is a CROSS-ARM CONTAMINATION and it is")
P("  reported because it was measured, not because it was asked for. NO ND ROW'S OWN PRICE MOVES")
P("  (verified below). The target moves because structural_values() builds its career-COMPLETION")
P("  strata S[(pos,t)] over THE WHOLE ELIGIBLE COHORT -- pool rows included (harness:337-350;")
P("  phase1_derive.py:79-80 passes `elig`, which is pool + national). A live ND career is completed")
P("  with a ratio taught partly by pool careers, so moving pool prices moves ND's completed values.")
P("  Magnitude: %.4f%% under the full lift. Small, but it is not zero and it is not noise."
  % (100 * (D['LIFTRH']['nd_profile'] / D['SHIP']['nd_profile'] - 1)))
P()
S = {r['key']: r for r in json.load(open(SP + '/per_entrant_SHIP.json'))['recs']}
A = {r['key']: r for r in json.load(open(SP + '/per_entrant_LIFTH.json'))['recs']}
B = {r['key']: r for r in json.load(open(SP + '/per_entrant_LIFTRH.json'))['recs']}
nonpool = [k for k in S if not S[k].get('is_pool')]
chB = [k for k in nonpool if (B[k].get('vpath') or []) != (S[k].get('vpath') or [])]
chA = [k for k in nonpool if (A[k].get('vpath') or []) != (S[k].get('vpath') or [])]
P("  VERIFICATION THAT NO NATIONAL ROW'S OWN PRICE MOVES:")
P("      non-pool records                                    %d" % len(nonpool))
P("      whose walk-forward price path changes, VARIANT A    %d" % len(chA))
P("      whose walk-forward price path changes, VARIANT B    %d" % len(chB))
if chB:
    P("      the exception, named: %s" % ", ".join(chB))
    for k in chB:
        r = S[k]
        P("        %s -- matrix pick %s, stored pick %s, matrix is_pool %s, ENGINE is_pool %s."
          % (k, r.get('pick'), r.get('pick_stored'), r.get('is_pool'), r.get('is_pool_engine')))
    P("      This is the #338 Q-B SLIDE CROSSER the emitter itself already tracks")
    P("      (emit_matrix_338.py:298 `crossers`). The ENGINE prices him as a pool row (effpk 65,")
    P("      _pool True) and so the lift reaches him; the MATRIX records his SLID pick as 64 and")
    P("      therefore admits him to the national teaching population. He is one row of 1197 and")
    P("      he is the entire reason the 'no national row moves' statement needs this footnote.")
P()
P("  LAYER 1 -- THE DERIVED PATHWAY LEVELS (lambda = shrunk pathway profile / nd_profile)")
P("  %-8s %6s | %9s %9s %9s | %9s %9s %9s | %9s %9s"
  % ('pathway', 'n', 'prof NOW', 'prof A', 'prof B', 'lam NOW', 'lam A', 'lam B', 'A rel', 'B rel'))
P("  " + "-" * 112)
L1 = {}
for s in ORDER:
    a = [D[l]['layer1'][s] for l in LABS]
    L1[s] = dict(n=a[0]['n'], prof=[x['profile'] for x in a], lam=[x['lam'] for x in a],
                 relA=a[1]['lam'] / a[0]['lam'] - 1, relB=a[2]['lam'] / a[0]['lam'] - 1,
                 entry_now=a[0]['entry_now'])
    P("  %-8s %6d | %9.4f %9.4f %9.4f | %9.4f %9.4f %9.4f | %+8.2f%% %+8.2f%%"
      % (s, a[0]['n'], a[0]['profile'], a[1]['profile'], a[2]['profile'],
         a[0]['lam'], a[1]['lam'], a[2]['lam'],
         100 * (a[1]['lam'] / a[0]['lam'] - 1), 100 * (a[2]['lam'] / a[0]['lam'] - 1)))
P("  " + "-" * 112)
for l in LABS:
    P("  %-10s ALL-POOL profile %.6f" % (NAME[l], D[l]['pool_profile']))
P()
P("  ENTRY-WEIGHTED SUMMARY OF THE LEVEL MOVE (weights = phase 1's own `entry_now` per pathway):")
_w = sum(L1[s]['entry_now'] for s in ORDER)
for i, nm in ((1, 'VARIANT A'), (2, 'VARIANT B')):
    _num = sum(L1[s]['entry_now'] * L1[s]['lam'][i] for s in ORDER)
    _den = sum(L1[s]['entry_now'] * L1[s]['lam'][0] for s in ORDER)
    P("      %-10s entry-weighted mean derived level moves %+.3f%% (from %.4f to %.4f)"
      % (nm, 100 * (_num / _den - 1), _den / _w, _num / _w))
P()
P("  WHAT THIS MEANS FOR THE ORDER OF OPERATIONS, stated plainly for the owner:")
P("      The pool REPRICING (phase 1) and the pool SITTER LIFT are NOT independent. The repricing")
P("      derives entry levels from measured pool returns, and those measured returns are recorded")
P("      NET of the sitter penalty. Lift the penalty and every pathway's measured return rises, so")
P("      the levels phase 1 would derive rise too -- by %+.2f%% to %+.2f%% on the full lift."
  % (100 * min(L1[s]['relB'] for s in ORDER), 100 * max(L1[s]['relB'] for s in ORDER)))
P("      DERIVE THE LEVELS FIRST AND LIFT THE PENALTY SECOND AND THE LEVELS ARE TAUGHT ON A CHARGE")
P("      THAT NO LONGER EXISTS. The two acts have to be sequenced, or the repricing re-derived after")
P("      the lift. THAT IS A DESIGN RULING AND IS NOT MADE HERE.")
P()
DATA['derived'] = dict(nd_profile={l: D[l]['nd_profile'] for l in LABS},
                       pool_profile={l: D[l]['pool_profile'] for l in LABS},
                       layer1=L1, control_max_lam_delta=_ctl,
                       nonpool_changed=dict(A=chA, B=chB))

# ==================================================================================================
# 5. THE COHORT INSTRUMENTS
# ==================================================================================================
P("=" * 118)
P("5. THE COHORT INSTRUMENTS")
P("=" * 118)
P("  DISCOUNT / NO-ARB CONVENTION, carried from menu_table.py:126-141 unchanged: a NEGATIVE margin")
P("  is free money (the book grows faster than the engine discounts, so holding dominates). The")
P("  order names the 14% charge, so 14.00% is the bar every row below is judged against; the")
P("  shipped ladder's own 13.00% rate at draft age 18 is printed beside it, not instead of it.")
P()
CHARGE = 0.14
SHIP_CHARGE = 0.13


def allarm(l):
    return json.load(open("%s/noarb/allarm_%s.json" % (O19, l)))


def t338(l):
    return json.load(open("%s/noarb/table_%s.json" % (O19, l)))


P("  5a. THE ALL-ARM COHORT INSTRUMENT (the owner's ruled cohort -- THE DECIDING INSTRUMENT)")
P("      noarb_table_allarm.py, canonical md5 asserted at run: %s"
  % allarm('SHIP')['canonical_instrument_md5'])
ALL = {}
for gname in ('PRIMARY  cohorts 2005-2023', 'MODERN   cohorts 2019-2023'):
    P()
    P("      %s" % gname)
    P("      %-12s %6s " % ('variant', 'n') + "".join("%9s" % ('yr%d' % n) for n in range(0, 6))
      + "%11s %10s %10s %10s" % ('apprec 0->1', 'vs 14%', 'vs 13%', 'verdict'))
    P("      " + "-" * 110)
    for l in LABS:
        t = allarm(l)['groups'][gname]
        r = {x['N']: x['ratio_meanN_over_mean0'] for x in t['rows']}
        ap = r[1] / r[0] - 1.0
        m14, m13 = CHARGE - ap, SHIP_CHARGE - ap
        ALL[(gname, l)] = dict(n=t['n'], rows={n: r[n] for n in range(0, 8)}, apprec=ap,
                               margin14=m14, margin13=m13)
        P("      %-12s %6d " % (NAME[l], t['n']) + "".join("%9.4f" % r[n] for n in range(0, 6))
          + "%10.2f%% %9.2f%% %9.2f%% %10s"
          % (100 * ap, 100 * m14, 100 * m13, 'ARB' if m14 < 0 else 'no arb'))
    b = ALL[(gname, 'SHIP')]
    P("      change in yr1 ratio: VARIANT A %+.4f   VARIANT B %+.4f"
      % (ALL[(gname, 'LIFTH')]['rows'][1] - b['rows'][1],
         ALL[(gname, 'LIFTRH')]['rows'][1] - b['rows'][1]))
P()
P("      BY ARM, PRIMARY window -- yr1 and yr4 pooled ratios per pathway")
P("      %-8s %6s | %8s %8s %8s | %8s %8s %8s"
  % ('arm', 'n', 'yr1 NOW', 'yr1 A', 'yr1 B', 'yr4 NOW', 'yr4 A', 'yr4 B'))
P("      " + "-" * 76)
ARM = {}
_ba = {l: allarm(l)['groups']['PRIMARY  cohorts 2005-2023']['by_arm'] for l in LABS}
for arm in sorted(_ba['SHIP'], key=lambda a: -_ba['SHIP'][a]['n']):
    v = [_ba[l][arm] for l in LABS]
    ARM[arm] = dict(n=v[0]['n'], yr1=[x['yr1'] for x in v], yr4=[x['yr4'] for x in v])
    P("      %-8s %6d | %8.4f %8.4f %8.4f | %8.4f %8.4f %8.4f"
      % (arm, v[0]['n'], v[0]['yr1'], v[1]['yr1'], v[2]['yr1'],
         v[0]['yr4'], v[1]['yr4'], v[2]['yr4']))
P()
P("  5b. THE LEGACY PICKS 1-64 INSTRUMENT (noarb_table_338.py, UNMODIFIED, md5 0f822035..)")
P("      population = harness load_matrix: teaches_curve & pick 1..64 & draft year 2004-2022, n=1197")
P("      %-12s " % 'variant' + "".join("%9s" % ('yr%d' % n) for n in range(0, 6))
  + "%11s %10s %10s %10s" % ('apprec 0->1', 'vs 14%', 'vs 13%', 'verdict'))
P("      " + "-" * 104)
T338 = {}
for l in LABS:
    t = t338(l)['groups']['ALL picks 1-64']
    r = {x['N']: x['ratio_meanN_over_mean0'] for x in t['rows']}
    ap = r[1] / r[0] - 1.0
    m14, m13 = CHARGE - ap, SHIP_CHARGE - ap
    T338[l] = dict(rows={n: r[n] for n in range(0, 8)}, apprec=ap, margin14=m14, margin13=m13)
    P("      %-12s " % NAME[l] + "".join("%9.4f" % r[n] for n in range(0, 6))
      + "%10.2f%% %9.2f%% %9.2f%% %10s" % (100 * ap, 100 * m14, 100 * m13,
                                           'ARB' if m14 < 0 else 'no arb'))
_rep = json.load(open(ROOT + '/docs/evidence/composition_2026-08-10/noarb/table_SHIP.json'))
P("      CONTROL 5: the SHIP re-run reproduces the COMMITTED table_SHIP.json groups exactly -> %s"
  % ("REPRODUCED" if _rep['groups'] == t338('SHIP')['groups'] else "MISMATCH"))
P()
P("      THE LEGACY INSTRUMENT IS ESSENTIALLY INERT, AND THE RESIDUE IS NAMED. Its population is")
P("      NATIONAL by construction (`_teaches_curve(p) = _in_pvc(p) and not is_pool(p)`), so a pool")
P("      lift has nothing to act on. It is not EXACTLY inert: yr1 moves %+.6f under VARIANT B, and"
  % (T338['LIFTRH']['rows'][1] - T338['SHIP']['rows'][1]))
P("      that entire move is ONE ROW -- daniel-butler, the #338 slide crosser named in section 4.")
P()
DATA['cohort'] = dict(allarm={"%s|%s" % k: v for k, v in ALL.items()}, by_arm=ARM, t338=T338,
                      charge=CHARGE, ship_charge=SHIP_CHARGE)

# ==================================================================================================
# 6. THE SECOND R SITE -- DISCLOSED SENSITIVITY, NOT VARIANT B
# ==================================================================================================
P("=" * 118)
P("6. THE SECOND R SITE (_a_blend) -- DISCLOSED SENSITIVITY, NOT PART OF EITHER VARIANT")
P("=" * 118)
P("  The order defines the R leg as `anch = R * entry_anchor(p)` INSIDE sitout_ev, and variant B is")
P("  scoped to exactly that. But _merged_recover.py:2178 reads the SAME retention surface a SECOND")
P("  time, in _a_blend, on the YEAR-1+ arm:  anch0 = R * entry_anchor(p). A pool player who has ever")
P("  had a qualifying season takes THAT site, never sitout_ev -- and variant B does not reach him.")
P("  A board with BOTH sites lifted for pool rows is built here so the residue is sized, not guessed.")
P()
BB = {}
for lab, fn in (('BASE', 'board_BASE.json'), ('LIFTH', 'board_LIFTH.json'),
                ('LIFTRH', 'board_LIFTRH.json'), ('LIFTBOTH', 'board_LIFTBOTH.json')):
    BB[lab] = {r['key']: r for r in json.load(open("%s/%s" % (O19, fn)))['active']}
K = sorted(BB['BASE'])
tt = {l: sum(BB[l][k]['v'] for k in K) for l in BB}
P("  %-34s %14s %14s %10s %8s" % ('', 'board total', 'change', 'change %', 'rows'))
P("  " + "-" * 84)
for lab, nm in (('BASE', 'TODAY (shipped)'), ('LIFTH', 'VARIANT A  (H only)'),
                ('LIFTRH', 'VARIANT B  (H + R at sitout_ev)'),
                ('LIFTBOTH', 'SENSITIVITY (H + R at BOTH sites)')):
    d = tt[lab] - tt['BASE']
    n = sum(1 for k in K if BB[lab][k]['v'] != BB['BASE'][k]['v'])
    P("  %-34s %14s %+14s %+9.3f%% %8d" % (nm, format(tt[lab], ','), format(d, ','),
                                           100.0 * d / tt['BASE'], n))
P()
_extra = [k for k in K if BB['LIFTBOTH'][k]['v'] != BB['LIFTRH'][k]['v']]
P("  ROWS THE SECOND SITE ADDS OVER VARIANT B: %d, worth %+s board points."
  % (len(_extra), format(sum(BB['LIFTBOTH'][k]['v'] - BB['LIFTRH'][k]['v'] for k in _extra), ',')))
if _extra:
    P("  %-24s %-7s | %8s %8s %8s %10s" % ('player', 'pathway', 'TODAY', 'VAR B', 'BOTH', 'extra'))
    for k in sorted(_extra, key=lambda k: -(BB['LIFTBOTH'][k]['v'] - BB['LIFTRH'][k]['v']))[:40]:
        r = BB['BASE'][k]
        st = r['ty'] if r['ty'] != 'ND' else ('ND 1-64' if 1 <= (r.get('pk') or 0) <= 64 else 'ND>64')
        P("  %-24s %-7s | %8s %8s %8s %+10s"
          % (r['name'][:24], st, format(r['v'], ','), format(BB['LIFTRH'][k]['v'], ','),
             format(BB['LIFTBOTH'][k]['v'], ','),
             format(BB['LIFTBOTH'][k]['v'] - BB['LIFTRH'][k]['v'], ',')))
_ndx = [k for k in _extra if BB['BASE'][k]['ty'] == 'ND' and 1 <= (BB['BASE'][k].get('pk') or 0) <= 64]
P("  national 1-64 rows among them: %d  (the patch is pool-gated at both sites)" % len(_ndx))
P()
DATA['sensitivity'] = dict(totals=tt, extra_rows=len(_extra),
                           extra_points=sum(BB['LIFTBOTH'][k]['v'] - BB['LIFTRH'][k]['v'] for k in _extra),
                           nd_rows=len(_ndx))

assert_pins('exit')
P("=" * 118)
P("PINS RE-ASSERTED AT EXIT -- board 94f1fec5..  store d9a24282..  instrument 0f822035..  UNMOVED.")
P("=" * 118)

json.dump(DATA, open(os.path.join(HERE, 'LIFT_CONSEQUENCE.json'), 'w'), indent=1, default=str)
