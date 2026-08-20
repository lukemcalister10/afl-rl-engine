#!/usr/bin/env python3
"""ORDER E part 4 — the five-band year-1 economics on the AS-OF read (the committed instrument's own
semantics: record truncated to <= Y, BASE_REF/AGE_REF pinned to Y, ev(p,Y) vs v0_start(p)), run over
the draft classes 2021-2025 so the year-1 cell has real n. READ-ONLY: the scoring list is swapped for
a truncated copy and restored in a finally-block; nothing is written anywhere."""
import os, sys, io, json, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import loadeng, cf

MA, G = loadeng.load()
cf.bind(MA, G)
cp = G['cp']
PLF = G['_PL_F']
LOG = []


def P(s=''):
    print(s, flush=True)
    LOG.append(str(s))


def S1(lam):
    def inst():
        def use(pos, age):
            return MA.REPL[pos] - lam * cf.delta(pos, age)
        op, of = MA.proj_from_peak, MA.prod_floor
        MA.proj_from_peak = cf.make_proj_w4(use)
        MA.prod_floor = cf.make_floor_w4(use)

        def un():
            MA.proj_from_peak = op
            MA.prod_floor = of
        return un
    return inst


def joint(*insts):
    def _i():
        uns = [f() for f in insts]

        def un():
            for u in reversed(uns):
                u()
        return un
    return _i


CLASSES = [2021, 2022, 2023, 2024, 2025]
COH = {}
for C in CLASSES:
    rows = [p for p in MA.data
            if p.get('key') and not p.get('_pool') and p.get('type') == 'ND'
            and not p.get('_pickless') and not p.get('_retired') and not G['delisted'](p)
            and p.get('year') and int(p['year']) == C and 1 <= MA.effpk(p) <= 64]
    COH[C] = rows
N = sum(len(v) for v in COH.values())
P('=== ORDER E · FIVE-BAND YEAR-1 ECONOMICS, AS-OF READ ===')
P('Semantics carried from the committed instrument: for a class drafted in year C the year-1 value is')
P('ev(p, C+1) with the record TRUNCATED to seasons <= C+1 and BASE_REF/AGE_REF pinned to C+1; the')
P('year-0 value is v0_start(p). Classes %s. n = %d rows (%s).'
  % (CLASSES, N, ' / '.join('%d:%d' % (c, len(COH[c])) for c in CLASSES)))
P('')
P('TWO DISCLOSED DEPARTURES FROM THE STANDING 338 TABLE, registered before measurement (PREREG_E §5):')
P('  1. the standing table is the WALK-FORWARD per-entrant matrix over the 2004-2022 classes; this is')
P('     a single-store as-of read over 2021-2025. Different population, different window.')
P('  2. this read is SURVIVOR-ONLY — a row already delisted/retired is excluded, whereas the standing')
P('     instrument keeps busts in the denominator at 0. That biases these levels UP.')
P('THEREFORE: read the MOVEMENT between baseline and counterfactual on the IDENTICAL population.')
P('The absolute levels here are NOT the standing instrument\'s numbers and are never quoted as such.')
P('')

BANDS = [('1-10', 1, 10), ('11-20', 11, 20), ('21-30', 21, 30), ('31-40', 31, 40), ('41-64', 41, 64)]


def read_cells():
    cells = []
    for C in CLASSES:
        Y = C + 1
        saved = {}
        for p in COH[C]:
            saved[id(p)] = p['scoring']
            p['scoring'] = [r for r in p['scoring'] if r['year'] <= Y]
        sb, sa = MA.BASE_REF, MA.AGE_REF
        MA.BASE_REF = Y; MA.AGE_REF = Y; MA._pe_clear()
        try:
            for p in COH[C]:
                try:
                    with contextlib.redirect_stdout(io.StringIO()):
                        v1 = float(G['ev'](p, Y)) / PLF
                        v0 = float(G['v0_start'](p)) / PLF
                except Exception:
                    continue
                cells.append(dict(cls=C, pick=int(MA.effpk(p)), v1=v1, v0=v0))
        finally:
            MA.BASE_REF, MA.AGE_REF = sb, sa
            MA._pe_clear()
            for p in COH[C]:
                if id(p) in saved:
                    p['scoring'] = saved[id(p)]
    return cells


def table(cells, label):
    res = {'n': len(cells), 'bands': {}}
    parts = []
    for nm, lo, hi in BANDS:
        sub = [c for c in cells if lo <= c['pick'] <= hi]
        if not sub:
            continue
        m1 = sum(c['v1'] for c in sub) / len(sub)
        m0 = sum(c['v0'] for c in sub) / len(sub)
        app = m1 / m0 - 1.0
        res['bands'][nm] = dict(n=len(sub), y0=m0, y1=m1, app=app)
        parts.append('%+7.2f%%%s' % (100 * app, '!' if app > 0.14 else (' ' if app >= 0 else '-')))
    res['class_total'] = sum(c['v1'] for c in cells)
    res['class_mean'] = res['class_total'] / max(len(cells), 1)
    P('  %-20s  yr1 class mean %8.1f  | %s' % (label, res['class_mean'], '  '.join(parts)))
    return res


P('bands left to right: 1-10 · 11-20 · 21-30 · 31-40 · 41-64.   "!" = buy-side RED past +14%%.')
P('')
OUT = {}
BASECELLS = read_cells()
OUT['baseline C32R'] = table(BASECELLS, 'BASELINE C32R')
for nm, lo, hi in BANDS:
    sub = [c for c in BASECELLS if lo <= c['pick'] <= hi]
    P('        band %-6s n %3d   mean yr0 %8.1f   mean yr1 %8.1f'
      % (nm, len(sub), sum(c['v0'] for c in sub) / len(sub), sum(c['v1'] for c in sub) / len(sub)))
P('')

SCEN = [('S1 lam=0.20', S1(0.20)), ('S1 lam=0.30', S1(0.30)), ('S1 lam=0.40', S1(0.40)),
        ('S1 lam=0.72', S1(0.72)), ('S1 lam=1.00', S1(1.00)),
        ('S2 V5 ladder', lambda: cf.install_S2('5')), ('S2 V3 ladder', lambda: cf.install_S2('3')),
        ('S22 age-keyed', lambda: cf.install_S22('full')),
        ('S1 .20 + S2 V5', joint(S1(0.20), lambda: cf.install_S2('5')))]
for nm, inst in SCEN:
    un = inst()
    try:
        cc = read_cells()
    finally:
        un()
    OUT[nm] = table(cc, nm)

chk = read_cells()
dev = max(abs(a['v1'] - b['v1']) for a, b in zip(BASECELLS, chk))
P('')
P('RESTORE CONTROL: baseline re-read after every scenario, max |delta| = %.10f board points -> %s'
  % (dev, 'PASS' if dev < 1e-9 else 'FAIL'))

P('')
P('=== MOVEMENT vs baseline, in percentage POINTS of yr0->1 appreciation ===')
P('%-20s %8s %8s %8s %8s %8s' % ('scenario', '1-10', '11-20', '21-30', '31-40', '41-64'))
b0 = OUT['baseline C32R']['bands']
for nm, _ in SCEN:
    bb = OUT[nm]['bands']
    P('%-20s %8s %8s %8s %8s %8s' % (nm, *['%+7.2f' % (100 * (bb[k]['app'] - b0[k]['app']))
                                            for k, _, _ in BANDS]))

HERE = os.path.dirname(os.path.abspath(__file__))
json.dump(dict(classes=CLASSES, n=N, tables=OUT), open(os.path.join(HERE, 'BANDS_E.json'), 'w'), indent=1)
open(os.path.join(HERE, 'BANDS_E_out.txt'), 'w').write('\n'.join(LOG) + '\n')
P('wrote BANDS_E.json + BANDS_E_out.txt')
