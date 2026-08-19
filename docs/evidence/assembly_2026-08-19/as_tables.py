#!/usr/bin/env python3
"""ASSEMBLY BUILD — THE POOL-ARM NO-ARB TABLES. The standing format, both windows, five boards.

THE GAP THIS CLOSES: the first no-arb delivery was ND-ONLY. The v748 standing format requires the
POOL ARMS in both windows against both baselines, and they were missing. This file produces them in
ORDER P BUILD's exact layout (STANDING_TABLES_P_out.txt is the reference).

  arms: RD · MSD · UNR · IRE · PDA · PDN · SSP · PDS · ALLPOOL
  windows: PRIMARY cohorts 2005-2023 · MODERN cohorts 2019-2023
  per row: years 0..7 as mean-ratio vs the SAME-SET year 0, the yr0->1 appreciation, the buy-side
           margin against the 14% carry, and a two-sided verdict.
  plus: the arm-by-arm MOVE of the candidate against every baseline board, and THE OWNER'S PATH TEST
        scored on every breaching arm cell.

THE MSD EXCLUSION, IN WORDS: MSD rows key their cohort on the DRAFT YEAR ITSELF, not draft+1, because
a mid-season draftee's first season IS his draft season. At year 1 an MSD row therefore falls BEFORE
the first year his path covers, and those rows are counted as PRE-WINDOW and EXCLUDED from the year-1
cell rather than scored as zero. That is why MSD's yr1 cell can read '-' while its later years do not.

The value semantics and the cohort clock are the all-arm instrument's own, lifted from ORDER P
BUILD's op_tables.py unchanged. NO ENGINE RUN HERE — this is an instrument pass over five
walk-forward matrices that already exist.

  usage: python3 as_tables.py
"""
import json, os, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
NOARB = SP + '/asm/noarb'
CHARGE = 0.14
WINDOWS = [('PRIMARY', 2005, 2023), ('MODERN', 2019, 2023)]
YEARS = list(range(0, 8))
ARM_TYPES = ['RD', 'MSD', 'UNR', 'IRE', 'PDA', 'PDN', 'SSP', 'PDS']
CARRY = [1.140, 1.300, 1.482, 1.689, 1.925, 2.195, 2.502]

LABELS = [('ASMCAND', '*** THE ASSEMBLY CANDIDATE ca73176e — THE BOARD UNDER REVIEW ***'),
          ('R20A', 'R = R20A 7f88f509 — the owner\'s reference'),
          ('PBUILT', 'ORDER P 374d4e44 — the assembly base'),
          ('OKRULED', 'ORDER K f3101883 — the base, carrying the DEFECTIVE blind eta charge'),
          ('O35FINAL', 'the landing candidate 1f176444')]
LABELS = [(l, n) for l, n in LABELS if os.path.exists(SP + '/per_entrant_%s.json' % l)]

# ---- the pins, computed at run and ASSERTED -------------------------------------------------------
PINS = {'noarb_table_allarm.py': '8673d7e33a6267ff51ff6331cc13b171',
        'noarb_table_338.py': '0f8220351c64c56ccfa90c60edcdfa5f',
        't338_extended_DISCLOSED.py': 'd59ad550116ebbe3d90ed82becd2c4d5'}
L = []


def P(s=''):
    print(s); L.append(str(s))


P('=' * 122)
P('ASSEMBLY BUILD — THE POOL-ARM NO-ARB TABLES. carry charge = 14%/yr.')
P('   SELL-SIDE RED: yr0->1 appreciation < 0.     BUY-SIDE RED: yr0->1 appreciation > +14%.')
P('=' * 122)
P('instrument pins, computed at run and ASSERTED:')
for nm, want in sorted(PINS.items()):
    fp = os.path.join(NOARB, nm)
    got = hashlib.md5(open(fp, 'rb').read()).hexdigest() if os.path.exists(fp) else 'MISSING'
    ok = (got == want)
    P('  %-30s %s   %s' % (nm, got, 'OK' if ok else '*** MOVED, expected %s ***' % want))
    assert ok, 'INSTRUMENT MD5 MOVED: %s %s != %s' % (nm, got, want)
P()
P('THE MSD YEAR-1 EXCLUSION, IN WORDS: an MSD row keys its cohort on the DRAFT YEAR ITSELF, not')
P('draft+1, because a mid-season draftee\'s first season IS his draft season. At year 1 such a row')
P('therefore falls BEFORE the first year his path covers; those rows are counted PRE-WINDOW and')
P('EXCLUDED from the year-1 cell rather than scored as zero. That is why MSD\'s yr1 can read "-".')
P()


def arm_paths(matrix_path):
    """ORDER P BUILD's op_tables.py::arm_paths, lifted unchanged."""
    D = json.load(open(matrix_path))
    R = D['recs']
    WINDOW_END = max(y for r in R for y, v in zip(r.get('yrs') or [], r.get('vpath') or [])
                     if v is not None)

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
            path, meta, npre = [], [], []
            for N in YEARS:
                reached = pop if N == 0 else [r for r in pop if cohort(r) + N - 1 <= WINDOW_END]
                vals = []
                pre = 0
                for r in reached:
                    v, kind = value_at(r, N)
                    if kind == 'pre':
                        pre += 1
                        continue
                    vals.append((v, float(r['v0'])))
                if len(vals) < 5:
                    path.append(None); meta.append(len(vals)); npre.append(pre); continue
                mN = sum(v for v, _ in vals) / len(vals)
                m0 = sum(v0 for _, v0 in vals) / len(vals)
                path.append(mN / m0 if m0 > 0 else None)
                meta.append(len(vals)); npre.append(pre)
            out[(wname, arm)] = dict(n=len(pop), path=path, n_by_year=meta, n_pre=npre)
    return out


def verdict(a):
    return 'SELL-RED' if a < 0 else ('BUY-RED' if a > CHARGE else 'ok')


def path_test(path):
    """The owner's path test, as PREREG_S.md section 7 froze it BEFORE any table was read."""
    if not path or path[0] in (None, 0) or len(path) < 2 or path[1] is None:
        return None
    r = [(path[k] / path[0]) if path[k] is not None else None for k in range(len(path))]
    a01 = r[1] - 1.0
    if a01 <= CHARGE:
        return dict(breaches=False)
    beat = [k for k in range(2, min(8, len(r))) if r[k] is not None and r[k] > CARRY[k - 1]]
    la = (len(beat) == 0)
    p6 = r[6] if len(r) > 6 else None
    p7 = r[7] if len(r) > 7 else None
    lb = (p7 is not None and p6 is not None and p7 <= p6 and p7 <= CARRY[6])
    return dict(breaches=True, limb_a=la, limb_b=lb, both=(la and lb), beat=beat)


ARMP = {lab: arm_paths(SP + '/per_entrant_%s.json' % lab) for lab, _n in LABELS}
OUT = {'charge': CHARGE, 'labels': [l for l, _ in LABELS], 'arms': {}, 'moves': {}, 'pathtest': {}}

P('-- POOL ARMS (cohort clock, all-arm instrument semantics; years 0..7 as mean-ratio vs the')
P('   SAME-SET year 0) --')
for lab, nice in LABELS:
    P()
    P('  %s' % nice)
    for wname, lo, hi in WINDOWS:
        P('  %s  cohorts %d-%d' % (wname, lo, hi))
        P('    %-8s %5s ' % ('arm', 'n') + ' '.join('%7s' % ('yr%d' % n) for n in YEARS)
          + '   %9s %9s %9s' % ('yr0->1', 'margin', 'verdict'))
        for arm in ARM_TYPES + ['ALLPOOL']:
            d = ARMP[lab].get((wname, arm))
            if not d:
                continue
            pth = d['path']
            a01 = (pth[1] / pth[0] - 1.0) if (pth[0] and pth[1] is not None) else None
            mgn = (CHARGE - a01) if a01 is not None else None
            pt = path_test(pth)
            OUT['arms'].setdefault(lab, {})['%s|%s' % (wname, arm)] = dict(
                n=d['n'], path=pth, n_by_year=d['n_by_year'], n_pre=d['n_pre'],
                apprec01=a01, margin=mgn,
                verdict=(verdict(a01) if a01 is not None else 'n/a'))
            if pt and pt.get('breaches'):
                OUT['pathtest'].setdefault(lab, {})['%s|%s' % (wname, arm)] = pt
            cells = ' '.join('%7s' % ('-' if v is None else '%.3f' % v) for v in pth)
            tail = ('%+8.2f%% %+8.2f%% %9s' % (100 * a01, 100 * mgn, verdict(a01))
                    if a01 is not None else
                    '%9s %9s %9s' % ('-', '-', 'MSD yr1 excl' if arm == 'MSD' else 'n<5'))
            P('    %-8s %5d ' % (arm, d['n']) + cells + '   ' + tail)

# ---- the arm-by-arm move of the candidate against every baseline ----------------------------------
P()
P('=' * 122)
P('THE ARM-BY-ARM MOVE — THE CANDIDATE against every baseline board, on the yr0->1 appreciation.')
P('A POSITIVE move means the candidate appreciates MORE over year one than the baseline does.')
P('=' * 122)
if 'ASMCAND' in ARMP:
    for wname, _lo, _hi in WINDOWS:
        P()
        P('  %s' % wname)
        for lab, _nice in LABELS:
            if lab == 'ASMCAND':
                continue
            P('    vs %s' % lab)
            P('      %-9s %12s %12s %12s   %s'
              % ('arm', 'candidate', lab, 'move', 'verdict  cand -> base'))
            for arm in ARM_TYPES + ['ALLPOOL']:
                a = OUT['arms'].get('ASMCAND', {}).get('%s|%s' % (wname, arm))
                b = OUT['arms'].get(lab, {}).get('%s|%s' % (wname, arm))
                if not a or not b or a['apprec01'] is None or b['apprec01'] is None:
                    continue
                mv = a['apprec01'] - b['apprec01']
                chg = '' if a['verdict'] == b['verdict'] else '   *** VERDICT CHANGES ***'
                OUT['moves'].setdefault('%s|%s' % (wname, lab), {})[arm] = dict(
                    cand=a['apprec01'], base=b['apprec01'], move=mv,
                    v_cand=a['verdict'], v_base=b['verdict'], changed=bool(chg))
                P('      %-9s %11.2f%% %11.2f%% %11.2f%%   %-8s -> %-8s%s'
                  % (arm, 100 * a['apprec01'], 100 * b['apprec01'], 100 * mv,
                     a['verdict'], b['verdict'], chg))

# ---- the path test on every breaching arm cell ----------------------------------------------------
P()
P('=' * 122)
P('THE OWNER\'S PATH TEST, ON EVERY BREACHING ARM CELL')
P('  limb (a) the path afterwards does not keep beating carry -> zero years k in 2..7 with path>carry')
P('  limb (b) the end destination does not keep increasing     -> path7 <= path6 AND path7 <= carry7')
P('  A cell PASSES only when BOTH limbs pass. Carry: ' + ' '.join('%.3f' % c for c in CARRY))
P('=' * 122)
any_b = False
for lab, _nice in LABELS:
    for wname, _lo, _hi in WINDOWS:
        for arm in ARM_TYPES + ['ALLPOOL']:
            pt = OUT['pathtest'].get(lab, {}).get('%s|%s' % (wname, arm))
            if not pt:
                continue
            any_b = True
            a = OUT['arms'][lab]['%s|%s' % (wname, arm)]
            det = ('PASSES both limbs' if pt['both'] else
                   'FAILS — ' + '; '.join(
                       ([] if pt['limb_a'] else ['beats carry in yr %s'
                                                 % ','.join(str(x) for x in pt['beat'])])
                       + ([] if pt['limb_b'] else ['still rising at yr7'])))
            P('  %-9s %-8s %-9s yr0->1 %+7.2f%%  n=%-5d %s'
              % (lab, wname, arm, 100 * a['apprec01'], a['n'], det))
if not any_b:
    P('  (no breaching arm cell on any board in either window)')

# ---- SSP, called out by name -----------------------------------------------------------------------
P()
P('=' * 122)
P('SSP — THE INHERITED BREACH, READ ON THE CANDIDATE')
P('=' * 122)
for wname, _lo, _hi in WINDOWS:
    row = []
    for lab, _n in LABELS:
        a = OUT['arms'].get(lab, {}).get('%s|SSP' % wname)
        if a and a['apprec01'] is not None:
            row.append('%s %+.2f%% (%s, n=%d)' % (lab, 100 * a['apprec01'], a['verdict'], a['n']))
    if row:
        P('  %-8s  %s' % (wname, '   ·   '.join(row)))
P()
P('SSP IS NOT REPAIRED BY THIS BUILD AND WAS NEVER MEANT TO BE — it is parked (register v744 C6) and')
P('is reported here so its reading on the candidate is on the record beside the baselines rather than')
P('described only in prose.')

json.dump(OUT, open(os.path.join(HERE, 'STANDING_TABLES_ASM.json'), 'w'), indent=1, default=float)
open(os.path.join(HERE, 'STANDING_TABLES_ASM_out.txt'), 'w').write('\n'.join(L) + '\n')
P()
P('written: STANDING_TABLES_ASM.json · STANDING_TABLES_ASM_out.txt')
