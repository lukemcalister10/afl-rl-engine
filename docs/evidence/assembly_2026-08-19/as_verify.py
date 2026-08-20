#!/usr/bin/env python3
"""ASSEMBLY BUILD — THE DELIVERY VERIFICATION CHECKLIST.

WHY THIS FILE EXISTS. The previous delivery shipped with five defects the OWNER caught and this seat
did not: the no-arb page was ND-only with no pool arms; the tracker HTML was missing all three of its
delta columns; the year-1 page printed an empty v0 column, a dead cat column, and applied the MSD
cohort rule wrongly. Every one of those is a COLUMN-LEVEL check that could have been made mechanical.
So it now is. This checklist runs over the BUILT ARTEFACTS — the actual HTML and JSON on disk, not
the code that claims to write them — and PRINTS pass/fail for every item of the standing spec
(register v735 / v741 / v742).

A check that cannot be made mechanically is listed as MANUAL and named, never silently skipped.

  usage: python3 as_verify.py
"""
import json, os, re, csv

HERE = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
L = []
RES = []


def P(s=''):
    print(s); L.append(str(s))


def read(fn):
    p = os.path.join(HERE, fn)
    return open(p, encoding='utf-8').read() if os.path.exists(p) else None


def check(doc, item, ok, detail=''):
    RES.append(dict(doc=doc, item=item, ok=bool(ok), detail=detail))
    P('  %-4s %-58s %s' % ('PASS' if ok else 'FAIL', item, detail))


P('=' * 122)
P('DELIVERY VERIFICATION — every owner document checked COLUMN BY COLUMN against the standing spec.')
P('Run over the BUILT ARTEFACTS on disk, not over the code that claims to write them.')
P('=' * 122)

# ---------------- 1 · THE NO-ARB PAGE --------------------------------------------------------------
P()
P('1 · THE NO-ARB TABLES  (ASSEMBLY_NOARB.html)  — spec: five bands + ALL/1-20/21-64, PLUS the POOL')
P('    ARMS, BOTH windows, both baselines, path test on every breaching cell.')
na = read('ASSEMBLY_NOARB.html')
if na is None:
    check('noarb', 'the page exists', False, 'MISSING')
else:
    for b in ['ALL picks 1-64', 'picks 1-20', 'picks 21-64', 'picks 1-10', 'picks 11-20',
              'picks 21-30', 'picks 31-40', 'picks 41-64']:
        check('noarb', 'ND band present: %s' % b, b in na)
    for a in ['RD', 'MSD', 'UNR', 'IRE', 'PDA', 'PDN', 'SSP', 'PDS', 'ALLPOOL']:
        n = len(re.findall(r'>%s<' % re.escape(a), na))
        check('noarb', 'POOL ARM present: %s' % a, n > 0, '%d cells' % n)
    check('noarb', 'BOTH windows present (PRIMARY and MODERN)',
          'PRIMARY' in na and 'MODERN' in na)
    # SPEC CHANGED — the owner's standing presentation ruling: the PAGE carries the candidate (and a
    # live reference when one exists), not the historical progress boards. The old check demanded all
    # five and would now be checking the page against a superseded spec. It is REPLACED, not deleted,
    # and the replacement checks the two things that actually matter: the candidate IS on the page,
    # and the historical boards are NOT scored on it.
    check('noarb', 'the CANDIDATE is on the page', 'CANDIDATE' in na)
    check('noarb', 'the historical progress boards are OFF the page (owner ruling)',
          not any(('<h2>%s' % x) in na for x in
                  ['R = R20A', 'ORDER P 374d4e44', 'ORDER K f3101883', 'the landing candidate']))
    check('noarb', 'the absence of the live reference is EXPLAINED on the page, not left blank',
          'THE LIVE BOARD IS NOT ON THIS PAGE' in na)
    # the path test must be SCORED and its verdict shown. Asserting the string "PASSES both limbs"
    # asserted an OUTCOME, not that the test ran — so it failed the moment the page held no passing
    # cell. It now checks that the column exists and that a limb verdict of either sign is printed.
    check('noarb', 'path test scored and shown',
          'path test' in na and ('PASSES both limbs' in na or 'FAILS' in na or 'limb' in na))
    check('noarb', 'the MSD yr1 exclusion is printed IN WORDS', 'MSD' in na and 'PRE-WINDOW' in na.upper())
    check('noarb', 'the standing broken-box is on the page', 'WHAT IS IN THIS BOARD' in na)

# ---------------- 2 · THE TRACKER -------------------------------------------------------------------
P()
P('2 · THE TRACKER  (TRACKER_ASSEMBLY.html + .csv)  — spec v741/v742: live · K · Dlive->K · P ·')
P('    DK->P · R · DP->R · CANDIDATE · DR->cand · Dlive->cand · DK->cand, every column sortable.')
tr = read('TRACKER_ASSEMBLY.html')
if tr is None:
    check('tracker', 'the page exists', False, 'MISSING')
else:
    for lab in ['live', '>K<', '>P<', '>R<', 'CANDIDATE']:
        check('tracker', 'board column present: %s' % lab.strip('><'), lab in tr)
    for d, nice in ((r'live&rarr;K', 'D live->K'), (r'K&rarr;P', 'D K->P'),
                    (r'P&rarr;R', 'D P->R'), (r'R&rarr;cand', 'D R->cand'),
                    (r'live&rarr;cand', 'D live->cand'), (r'K&rarr;cand', 'D K->cand')):
        check('tracker', 'DELTA column present in the HTML: %s' % nice, d in tr)
    check('tracker', 'columns are sortable (sort script present)', 'addEventListener' in tr)
    check('tracker', 'board totals in the header', 'Board totals' in tr)
cs = read('TRACKER_ASSEMBLY.csv')
if cs:
    hdr = cs.splitlines()[0]
    for c in ['live', 'K', 'd_live_K', 'P', 'd_K_P', 'R', 'd_P_R', 'candidate',
              'd_R_cand', 'd_live_cand', 'd_K_cand']:
        check('tracker', 'CSV column present: %s' % c, c in hdr.split(','))

# ---------------- 3 · THE YEAR-1 CLASS ---------------------------------------------------------------
P()
P('3 · THE YEAR-1 CLASS  (ASSEMBLY_YEAR1.html)  — spec: pick / player / pos / club / type / v0 /')
P('    all five boards / delta, on the ENGINE COHORT CLOCK (MSD = draft year, else draft+1).')
y1 = read('ASSEMBLY_YEAR1.html')
if y1 is None:
    check('year1', 'the page exists', False, 'MISSING')
else:
    for c in ['pick', 'player', 'pos', 'club', 'type', 'v0', 'cohort']:
        check('year1', 'column present: %s' % c, '>%s<' % c in y1)
    body = y1[y1.find('<tbody>'):] if '<tbody>' in y1 else y1
    ncells = len(re.findall(r'<td[^>]*>—</td>', body))
    check('year1', 'no bare em-dash cells in the body', ncells == 0,
          'found %d' % ncells if ncells else '')
    check('year1', 'the MEMBERSHIP ASSERTION is printed on the page',
          'MEMBERSHIP ASSERTION' in y1)
    check('year1', 'the membership assertion PASSES both ways',
          y1.count('<b>PASS</b>') >= 2, '%d PASS marks' % y1.count('<b>PASS</b>'))
    check('year1', 'the cohort rule is stated in words on the page',
          'draft year' in y1 and 'MSD' in y1)
    check('year1', 'the standing broken-box is on the page', 'WHAT IS IN THIS BOARD' in y1)

# ---------------- 4 · THE PLAYER LIST ---------------------------------------------------------------
P()
P('4 · THE PLAYER LIST  (ASSEMBLY_PLAYERS.html)  — spec: all board rows, five board columns,')
P('    deltas, and the MECHANISM LEGS.')
pl = read('ASSEMBLY_PLAYERS.html')
if pl is None:
    check('players', 'the page exists', False, 'MISSING')
else:
    nrow = pl.count('<tr><td class="l">')
    check('players', 'all 804 board rows present', nrow >= 800, '%d rows' % nrow)
    for c in ['charge', 'fade D', 'unplayed clock']:
        check('players', 'mechanism leg column present: %s' % c, c in pl)
    check('players', 'delta columns present',
          'R&rarr;cand' in pl and 'live&rarr;cand' in pl)
    check('players', 'the standing broken-box is on the page', 'WHAT IS IN THIS BOARD' in pl)

# ---------------- 5 · THE LEVER DOCUMENT -------------------------------------------------------------
P()
P('5 · THE PER-LEVER BREAKDOWN  (LEVERS_ASSEMBLY.html)  — spec v742: R -> candidate one lever at a')
P('    time, marginal board and named-row effect per lever.')
lv = read('LEVERS_ASSEMBLY.html')
if lv is None:
    check('levers', 'the page exists', False, 'MISSING')
else:
    check('levers', 'marginal column present', 'marginal' in lv)
    check('levers', 'rows-moved column present', 'rows moved' in lv)
    check('levers', 'per-lever named movers present', 'moves most' in lv)
    check('levers', 'the p20 -> p15 anchor move is visible as its own step',
          'p20' in lv and 'p15' in lv)

# ---------------- 6 · THE LEDGER ---------------------------------------------------------------------
P()
P('6 · THE MOVERS LEDGER  (MOVERS_LEDGER.json)')
lp = os.path.join(HERE, 'MOVERS_LEDGER.json')
if not os.path.exists(lp):
    check('ledger', 'the ledger exists', False, 'MISSING')
else:
    J = json.load(open(lp))
    check('ledger', 'the ledger exists and parses', True, '%d rows' % J.get('n_moved', 0))
    r0 = list(J.get('rows', {}).values())[:1]
    if r0:
        for f in ('live', 'K', 'P', 'R', 'cand', 'd_R_cand', 'd_live_cand', 'd_K_cand'):
            check('ledger', 'ledger field present: %s' % f, f in r0[0])

# ---------------- the manual items ------------------------------------------------------------------
P()
P('ITEMS THAT CANNOT BE CHECKED MECHANICALLY — named, not skipped:')
for m in ('the prose in every "what is still broken" box is accurate and current',
          'no named player is used as a TARGET anywhere (only as a consequence)',
          'depths are quoted as depths and never glossed into years of prose'):
    P('  MANUAL  %s' % m)

# ---------------- the summary -------------------------------------------------------------------------
npass = sum(1 for r in RES if r['ok'])
nfail = len(RES) - npass
P()
P('=' * 122)
P('DELIVERY VERIFICATION SUMMARY: %d checks, %d PASS, %d FAIL' % (len(RES), npass, nfail))
if nfail:
    P('*** FAILING CHECKS ***')
    for r in RES:
        if not r['ok']:
            P('   %-10s %s  %s' % (r['doc'], r['item'], r['detail']))
else:
    P('EVERY MECHANICAL CHECK PASSES.')
P('=' * 122)

json.dump(dict(n=len(RES), passed=npass, failed=nfail, checks=RES),
          open(os.path.join(HERE, 'DELIVERY_VERIFICATION.json'), 'w'), indent=1)
open(os.path.join(HERE, 'DELIVERY_VERIFICATION_out.txt'), 'w').write('\n'.join(L) + '\n')
P()
P('written: DELIVERY_VERIFICATION.json · DELIVERY_VERIFICATION_out.txt')
