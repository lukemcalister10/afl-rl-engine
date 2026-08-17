#!/usr/bin/env python3
"""ORDER E part 3 — the verdict search: which dose / which minimal set reaches the owner-expected
neighbourhood, and what it costs the year-1 class and the five bands. READ-ONLY."""
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


BY = {}
for p in MA.data:
    BY.setdefault(p.get('key'), p)
ROWS = ['harry-dean', 'cooper-duff-tytler', 'milan-murdock', 'levi-ashcroft',
        'connor-o-sullivan', 'logan-morris']


def board(p, Y=2026):
    with contextlib.redirect_stdout(io.StringIO()):
        return float(G['ev'](p, Y)) / PLF


def snap():
    return {k: board(BY[k]) for k in ROWS}


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


BASE = snap()

# ---------- year-1 class population, three readings (the "~105" question, answered honestly) ------
def pop(pred):
    return [p for p in MA.data
            if p.get('key') and not p.get('_retired') and not G['delisted'](p) and pred(p)]


def yis(p):
    y = p.get('year')
    return (2026 - int(y)) if y else None


A = pop(lambda p: (not p.get('_pool')) and p.get('type') == 'ND' and not p.get('_pickless') and yis(p) == 1)
B = pop(lambda p: (not p.get('_pool')) and yis(p) == 1)
C = pop(lambda p: yis(p) == 1)
D = pop(lambda p: yis(p) == 1 and MA.GRP.get(p.get('pos')))
P('=== ORDER E · THE YEAR-1 CLASS POPULATION ===')
P('  ND, non-pool, picked, active, drafted 2025 ...... %3d rows   <- the class used below' % len(A))
P('  any non-pool row drafted 2025, active ........... %3d rows' % len(B))
P('  any row (incl. pool) drafted 2025, active ....... %3d rows' % len(C))
P('  any row drafted 2025 with a priced position ..... %3d rows' % len(D))
P('  (the brief says "~105-row year-1 class"; on this store no draft-2025 reading reaches 105 —')
P('   the closest object is the whole draft-2025 intake including every pool pathway. The class')
P('   numbers below are stated on the %d-row ND reading and the row count is printed every time.)' % len(A))
P('')

Y1 = sorted(A, key=lambda p: (MA.effpk(p), p['key']))
BANDS = [('picks 1-10', 1, 10), ('picks 11-20', 11, 20), ('picks 21-30', 21, 30),
         ('picks 31-40', 31, 40), ('picks 41-64', 41, 64)]


def class_rows():
    out = []
    for p in Y1:
        with contextlib.redirect_stdout(io.StringIO()):
            v1 = float(G['ev'](p, 2026)) / PLF
            v0s = float(G['v0_start'](p)) / PLF          # the object the committed 338 instrument reads
            v0p = float(G['pv_pedigree'](p)) / PLF       # the day-0 pedigree leg
        out.append(dict(pick=int(MA.effpk(p)), v1=v1, v0s=v0s, v0p=v0p))
    return out


def table(rows, label, den='v0s'):
    tot = sum(r['v1'] for r in rows)
    res = dict(total=tot, mean=tot / len(rows), n=len(rows), bands={})
    line = []
    for nm, lo, hi in BANDS:
        sub = [r for r in rows if lo <= r['pick'] <= hi]
        if not sub:
            continue
        m1 = sum(r['v1'] for r in sub) / len(sub)
        m0 = sum(r[den] for r in sub) / len(sub)
        app = m1 / m0 - 1.0
        res['bands'][nm] = dict(n=len(sub), y0=m0, y1=m1, app=app)
        line.append('%+7.2f%%%s' % (100 * app, '!' if app > 0.14 else (' ' if app >= 0 else '-')))
    P('  %-22s class tot %9.1f  mean %7.1f | %s' % (label, tot, tot / len(rows), '  '.join(line)))
    return res


BASEROWS = class_rows()
P('=== FIVE-BAND YEAR-1 ECONOMICS (LIVE-BOARD DRAFT-CLOCK PROXY — NOT the committed 338 walk-forward')
P('    instrument; PREREG_E §5 registered this substitution before measurement). Denominator =')
P('    v0_start(p), the same year-zero object the 338 instrument reads. "!" = buy-RED past +14%.')
P('    Bands, left to right: 1-10 · 11-20 · 21-30 · 31-40 · 41-64. n = 10/10/10/10/18.')
P('')
OUT = {}
OUT['baseline'] = table(BASEROWS, 'BASELINE C32R')
P('    [reference — the COMMITTED walk-forward 338 table for the repaired C32 (PACKET_C §6):')
P('     +6.10%   +7.40%   +1.60%  -12.90%   -6.10% ; the proxy above runs hot on the early bands')
P('     and much colder on 21-30, so read DIRECTIONS and MOVEMENT here, never the levels.]')
P('')

SCEN = [
    ('S1 lam=0.15', S1(0.15)),
    ('S1 lam=0.20', S1(0.20)),
    ('S1 lam=0.25', S1(0.25)),
    ('S1 lam=0.30', S1(0.30)),
    ('S1 lam=0.40', S1(0.40)),
    ('S1 lam=0.72', S1(0.72)),
    ('S1 lam=1.00', S1(1.00)),
    ('S2 V5 ladder', lambda: cf.install_S2('5')),
    ('S2 V3 ladder', lambda: cf.install_S2('3')),
    ('S22 age-keyed', lambda: cf.install_S22('full')),
    ('S1 .20 + S2 V5', joint(S1(0.20), lambda: cf.install_S2('5'))),
    ('S1 .20 + S2 V3', joint(S1(0.20), lambda: cf.install_S2('3'))),
    ('S1 .30 + S2 V5', joint(S1(0.30), lambda: cf.install_S2('5'))),
]
NAMED = {}
for nm, inst in SCEN:
    un = inst()
    try:
        rr = class_rows()
        NAMED[nm] = snap()
    finally:
        un()
    OUT[nm] = table(rr, nm)

after = snap()
for k in ROWS:
    assert abs(after[k] - BASE[k]) < 1e-9, 'RESTORE FAILED %s' % k
P('')
P('RESTORE CONTROL: all six named rows byte-identical to baseline after every scenario — PASS')
P('')
P('=== NAMED ROWS UNDER EACH SCENARIO (board points) ===')
P('%-18s %8s %8s | %8s %8s %8s %8s' %
  ('scenario', 'dean', 'CDT', 'murdock', 'ashcrft', 'osulliv', 'morris'))
P('%-18s %8.1f %8.1f | %8.1f %8.1f %8.1f %8.1f  <- BASELINE' %
  ('baseline C32R', BASE['harry-dean'], BASE['cooper-duff-tytler'], BASE['milan-murdock'],
   BASE['levi-ashcroft'], BASE['connor-o-sullivan'], BASE['logan-morris']))
for nm, _ in SCEN:
    s = NAMED[nm]
    ok = ('BOTH' if (s['harry-dean'] >= 2600 and s['cooper-duff-tytler'] >= 1800) else
          ('dean only' if s['harry-dean'] >= 2600 else
           ('CDT only' if s['cooper-duff-tytler'] >= 1800 else '-')))
    P('%-18s %8.1f %8.1f | %8.1f %8.1f %8.1f %8.1f  %s' %
      (nm, s['harry-dean'], s['cooper-duff-tytler'], s['milan-murdock'], s['levi-ashcroft'],
       s['connor-o-sullivan'], s['logan-morris'], ok))
P('  target: dean >= 2600, CDT >= 1800 (their Candidate-31 levels are 2670 / 1832)')

HERE = os.path.dirname(os.path.abspath(__file__))
json.dump(dict(base=BASE, named=NAMED, classes=OUT,
               pops=dict(nd=len(A), nonpool=len(B), all=len(C), priced=len(D))),
          open(os.path.join(HERE, 'VERDICT_E.json'), 'w'), indent=1)
open(os.path.join(HERE, 'VERDICT_E_out.txt'), 'w').write('\n'.join(LOG) + '\n')
P('wrote VERDICT_E.json + VERDICT_E_out.txt')
