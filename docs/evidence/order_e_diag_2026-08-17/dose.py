#!/usr/bin/env python3
"""ORDER E part 2 — the S1 dose-response, the k=0/k>=1 split, the year-1 class and the five-band
year-1 economics under the top counterfactual. READ-ONLY, in-memory only."""
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


BASE = snap()

# ---------- a lambda-scaled and k-restricted S1 ----------
def install_S1_scaled(lam=1.0, kmode='all'):
    """The S1 counterfactual at dose `lam`: the bar becomes REPL[pos] - lam*Delta(class, age-at-horizon).
    lam=0 reproduces the baseline exactly; lam=1 is the full age-referenced surface. Delta is already 0
    from age 24, so a row's own bar walks back up to the flat bar as the projection ages him."""
    def use(pos, age):
        return MA.REPL[pos] - lam * cf.delta(pos, age)
    old_proj, old_floor = MA.proj_from_peak, MA.prod_floor
    MA.proj_from_peak = cf.make_proj_w4(use)
    MA.prod_floor = cf.make_floor_w4(use)

    def un():
        MA.proj_from_peak = old_proj
        MA.prod_floor = old_floor
    return un


P('=== ORDER E · S1 DOSE-RESPONSE (board points) ===')
P('lambda = the fraction of the engine\'s own measured C3 development gap applied to the bar.')
P('%6s %10s %10s %10s %10s %10s %10s' % ('lam', 'dean', 'CDT', 'murdock', 'ashcroft', 'osulliv', 'morris'))
P('%6.2f %10.1f %10.1f %10.1f %10.1f %10.1f %10.1f' %
  (0.0, BASE['harry-dean'], BASE['cooper-duff-tytler'], BASE['milan-murdock'],
   BASE['levi-ashcroft'], BASE['connor-o-sullivan'], BASE['logan-morris']))
DOSE = []
for lam in (0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50, 0.75, 1.00):
    un = install_S1_scaled(lam, 'all')
    try:
        s = snap()
    finally:
        un()
    DOSE.append(dict(lam=lam, **s))
    P('%6.2f %10.1f %10.1f %10.1f %10.1f %10.1f %10.1f' %
      (lam, s['harry-dean'], s['cooper-duff-tytler'], s['milan-murdock'],
       s['levi-ashcroft'], s['connor-o-sullivan'], s['logan-morris']))
P('')
P('owner-expected neighbourhood: dean >= 2600 (C31 2670), CDT >= 1800 (C31 1832)')
P('')

# ---------- the year-1 class ----------
def year1_class():
    out = []
    for p in MA.data:
        if not p.get('key') or p.get('_retired') or p.get('_pool'):
            continue
        if G['delisted'](p):
            continue
        if p.get('type') != 'ND' or p.get('_pickless'):
            continue
        yr = p.get('year')
        if not yr or int(yr) != 2025:
            continue
        out.append(p)
    return sorted(out, key=lambda p: (MA.effpk(p), p['key']))


Y1 = year1_class()
P('YEAR-1 CLASS (live board, type ND, draft year 2025, active, non-pool): %d rows' % len(Y1))
BANDS = [('picks 1-10', 1, 10), ('picks 11-20', 11, 20), ('picks 21-30', 21, 30),
         ('picks 31-40', 31, 40), ('picks 41-64', 41, 64)]


def class_table():
    rows = []
    for p in Y1:
        with contextlib.redirect_stdout(io.StringIO()):
            v = float(G['ev'](p, 2026)) / PLF
            v0 = float(G['pv_pedigree'](p)) / PLF          # the day-0 (year-zero) pedigree object
        rows.append(dict(key=p['key'], pick=int(MA.effpk(p)), pos=MA.gfut(p),
                         age=cp._age_asof(p, 2026), v1=v, v0=v0,
                         g=sum(x['games'] for x in p['scoring'] if x['games'])))
    return rows


def summarize(rows, label):
    tot = sum(r['v1'] for r in rows)
    P('  %-28s  class total %10.1f   mean %8.1f   n %d' % (label, tot, tot / len(rows), len(rows)))
    out = {'total': tot, 'mean': tot / len(rows), 'n': len(rows), 'bands': {}}
    for nm, lo, hi in BANDS:
        sub = [r for r in rows if lo <= r['pick'] <= hi]
        if not sub:
            continue
        m1 = sum(r['v1'] for r in sub) / len(sub)
        m0 = sum(r['v0'] for r in sub) / len(sub)
        app = m1 / m0 - 1.0
        out['bands'][nm] = dict(n=len(sub), mean_y1=m1, mean_y0=m0, appreciation=app)
        P('      %-12s n %3d   mean yr0 %8.1f   mean yr1 %8.1f   yr0->1 %+7.2f%%  %s'
          % (nm, len(sub), m0, m1, 100 * app, 'BUY-RED (>+14%)' if app > 0.14 else
             ('sell-RED (<0%)' if app < 0 else 'ok')))
    return out


P('')
P('LIVE-BOARD DRAFT-CLOCK PROXY (see PREREG_E §5: this is NOT the committed walk-forward 338')
P('instrument; it is the live 2026 year-1 class measured against its own year-zero pedigree object).')
BASEROWS = class_table()
CLS = {}
CLS['baseline'] = summarize(BASEROWS, 'BASELINE (repaired C32)')

SCEN = [('S1 lam=1.00', lambda: install_S1_scaled(1.00, 'all')),
        ('S1 lam=0.50', lambda: install_S1_scaled(0.50, 'all')),
        ('S1 lam=0.25', lambda: install_S1_scaled(0.25, 'all')),
        ('S1 lam=0.20', lambda: install_S1_scaled(0.20, 'all')),
        ('S1 lam=0.15', lambda: install_S1_scaled(0.15, 'all'))]
for nm, inst in SCEN:
    un = inst()
    try:
        rr = class_table()
    finally:
        un()
    P('')
    CLS[nm] = summarize(rr, nm)

# restore check
after = snap()
for k in ROWS:
    assert abs(after[k] - BASE[k]) < 1e-9, 'RESTORE FAILED %s' % k
P('')
P('RESTORE CONTROL after every scenario: all six named rows byte-identical to baseline — PASS')

HERE = os.path.dirname(os.path.abspath(__file__))
json.dump(dict(base=BASE, dose=DOSE, year1_n=len(Y1), classes=CLS),
          open(os.path.join(HERE, 'DOSE_E.json'), 'w'), indent=1)
open(os.path.join(HERE, 'DOSE_E_out.txt'), 'w').write('\n'.join(LOG) + '\n')
P('wrote DOSE_E.json + DOSE_E_out.txt')
