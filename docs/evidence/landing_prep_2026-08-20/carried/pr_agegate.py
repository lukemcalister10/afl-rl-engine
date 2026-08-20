#!/usr/bin/env python3
"""THE CONTINUITY HARNESS'S OWN AGE AXIS, MADE R3-AWARE AND RL_O43-AWARE.

THIS IS THE ACCEPTANCE MEASUREMENT. `os_continuity.py`'s age axis asks one question: does a row's
price JUMP when only the CHARGE's age channel advances — the age-24 handover ORDER P introduced?
It holds games, output, pedigree and clock EXACTLY fixed and moves nothing but `o38_w(age)`.

WHY THE HARNESS'S OWN ANSWER COULD NOT BE BELIEVED, and what is different here:
  · the harness re-forms the price with `os_lib.assemble`, which rebuilds the ORDER 31 law
    rho*e + pi*ped + age_credit and HAS NO R3 TERM — so on any R3-live board it prints R3's whole
    collector as a birthday jump. That is the defect as_r3age.py diagnosed.
  · it also knows nothing of the RL_O43 parity max, so on the candidate it would mis-price every
    one of the 37 treated rows on top of that.
  THIS script re-forms NOTHING. It moves the charge's age channel and re-prices THROUGH ev(), with
  the parity max re-taken, so R3, the O42 consolidation and the O43 guard are all carried exactly.

DISTINGUISH THIS FROM pr_birthday.py. That script advances the row's age in EVERY channel at once
(p['_by'] -= 1) and measures what a whole year of ageing is worth. That is the model working as
designed, not a continuity question, and its number must never be read as a breach. THIS script
isolates the ONE channel the acceptance law is about.

GUARDS, both build-failing: (G1) unperturbed, reproduce the built board on every row; (G2) every
row restores exactly afterwards.

usage: LINE=CAND python3 pr_agegate.py
"""
import io, os, sys, json, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pr_lib as PR

LINE = os.environ.get('LINE', 'CAND')
CFG = {'CAND': (PR.DIALS, 'D7B_CAND', 'MY_NOR3_43', True),
       'HIST': (PR.DIALS_HIST, 'MY_V755_CAND', 'MY_V755_L5CR', False)}[LINE]
dials, ctag, ptag, o43 = CFG
OUT = []


def P(s=''):
    print(s)
    OUT.append(str(s))


CAND, mC = PR.board(ctag)
PRE, mP = PR.board(ptag)
CHARGED = {k: CAND[k]['v'] - PRE[k]['v'] for k in PRE if CAND[k]['v'] != PRE[k]['v']}

M = PR.Model(dials, o43=o43)
M.recording = False
NS = M.NS
SC = NS.get('_O37_SCACHE')
PC = NS.get('_O38_PCACHE')
if not NS.get('_O38'):
    raise SystemExit('this line is not on the O38 charge; the o38_w channel does not exist here.')
W0 = NS['o38_w']


def clear():
    if SC is not None:
        SC.clear()
    if PC is not None:
        PC.clear()


def priced(p):
    clear()
    return PR.bint(M.price(p, 'on')[0])


P('=' * 112)
P('THE AGE-GATE BIRTHDAY — the CHARGE\'s age channel (o38_w) advanced one year, everything else')
P('held EXACTLY fixed, re-priced through ev() with the parity max re-taken.  LINE=%s  board %s'
  % (LINE, mC))
P('=' * 112)
P('  RL_O42 %s · RL_O43 %s · treated %d · lifted %d · O37_AGE_GATE %s · _F %.4f'
  % (NS.get('_O42'), NS.get('_O43'), len(M.TREATED), len(M.D7_FLOOR),
     NS.get('O37_AGE_GATE'), PR._F))
P()

KEYS = [k for k in CAND if k in M.BY]
g1 = sum(1 for k in KEYS if priced(M.BY[k]) == CAND[k]['v'])
P('GUARD 1 — unperturbed, this routine reproduces the built board : %d of %d rows exact'
  % (g1, len(KEYS)))

steps = {}
bad = []
noby = 0
for k in KEYS:
    p = M.BY[k]
    if not p.get('_by'):
        noby += 1
        steps[k] = 0
        continue
    age = 2026 - int(p['_by'])
    v0 = CAND[k]['v']
    NS['o38_w'] = (lambda x, _w=W0, _t=age + 1: _w(_t))
    try:
        v1 = priced(p)
    finally:
        NS['o38_w'] = W0
        clear()
    if priced(p) != v0:
        bad.append(k)
    steps[k] = v1 - v0

P('GUARD 2 — every row restores EXACTLY after the perturbation      : %d failures' % len(bad))
P('  rows with no birth year (not testable, counted as 0): %d' % noby)
P()

if g1 != len(KEYS) or bad:
    P('*** A GUARD FAILED. This measurement says NOTHING and is reported as a failure. ***')
else:
    mv = {k: v for k, v in steps.items() if v}
    P('  ROWS TESTED                                                  : %d' % (len(KEYS) - noby))
    P('  ROWS WHOSE PRICE MOVES ON THE CHARGE\'S BIRTHDAY ALONE        : %d' % len(mv))
    P('  NET BOARD POINTS HANDED ACROSS THE BIRTHDAY, WHOLE BOARD     : %+d' % sum(steps.values()))
    P('  ROWS MOVING BY 50%% OR MORE OF THEIR OWN PRICE                : %d'
      % sum(1 for k in mv if CAND[k]['v'] and abs(mv[k]) >= 0.5 * abs(CAND[k]['v'])))
    P()
    ch = [k for k in CHARGED if k in steps]
    tr = [k for k in M.TREATED if k in steps]
    lf = [k for k in tr if k in M.D7_FLOOR]
    sh = [k for k in tr if k not in M.D7_FLOOR]
    P('  BY POPULATION')
    for nm, ks in (('the %d R3-moved rows' % len(ch), ch),
                   ('the %d D7-TREATED rows' % len(tr), tr),
                   ('  of which %d D7-LIFTED' % len(lf), lf),
                   ('  of which %d SHIELD' % len(sh), sh)):
        if ks:
            P('    %-28s  movers %3d   net %+7d' % (nm, sum(1 for k in ks if steps[k]),
                                                    sum(steps[k] for k in ks)))
    P()
    if mv:
        P('  EVERY ROW THAT MOVES, LARGEST FIRST')
        P('  %-26s %4s %9s %9s %8s %9s' % ('row', 'age', 'v now', 'v +1yr', 'step', 'group'))
        for k in sorted(mv, key=lambda k: -abs(mv[k]))[:40]:
            p = M.BY[k]
            grp = ('LIFTED' if k in M.D7_FLOOR else 'shield') if k in M._treated_set else (
                'R3-moved' if k in CHARGED else '-')
            P('  %-26s %4d %9d %9d %+8d %9s'
              % ((p.get('player') or k)[:26], 2026 - int(p['_by']), CAND[k]['v'],
                 CAND[k]['v'] + mv[k], mv[k], grp))
        P()
        P('  BY AGE (only ages with movers)')
        ages = {}
        for k in KEYS:
            p = M.BY[k]
            if p.get('_by'):
                ages.setdefault(2026 - int(p['_by']), []).append(k)
        P('  %-5s %6s %8s %12s' % ('age', 'n', 'movers', 'net points'))
        for a in sorted(ages):
            ks = ages[a]
            nm_ = sum(1 for k in ks if steps[k])
            if nm_:
                P('  %-5d %6d %8d %+12d' % (a, len(ks), nm_, sum(steps[k] for k in ks)))
    else:
        P('  NO ROW MOVES. The charge does not read current age on this line at all.')

json.dump(dict(line=LINE, board=mC, guard1=g1, n=len(KEYS), restore_failures=bad, steps=steps),
          open(os.path.join(HERE, 'PR_AGEGATE_%s.json' % LINE), 'w'), indent=1)
open(os.path.join(HERE, 'PR_AGEGATE_%s_out.txt' % LINE), 'w').write('\n'.join(OUT) + '\n')
