#!/usr/bin/env python3
"""ORDER E part 5 — the isolation check for S1 and the printed bar arithmetic. READ-ONLY."""
import os, sys, io, json, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import loadeng, cf

MA, G = loadeng.load()
cf.bind(MA, G)
cp = G['cp']; PLF = G['_PL_F']
LOG = []


def P(s=''):
    print(s, flush=True)
    LOG.append(str(s))


BY = {}
for p in MA.data:
    BY.setdefault(p.get('key'), p)
KEYS = ['harry-dean', 'cooper-duff-tytler', 'milan-murdock', 'levi-ashcroft',
        'connor-o-sullivan', 'logan-morris']


def legs(p, Y=2026):
    with contextlib.redirect_stdout(io.StringIO()):
        return dict(ev=float(G['ev'](p, Y)) / PLF,
                    phat=float(G['_prod_path'](p, Y)) / PLF,
                    v0=float(G['v0_start'](p)) / PLF,
                    ped=float(G['pv_pedigree'](p)) / PLF,
                    anch=float(G['entry_anchor'](p)) / PLF,
                    rho=float(G['rho31'](G['pv_games'](p, Y))),
                    pi=float(G['o31_pi'](p, Y, G['pv_games'](p, Y))),
                    cred=float(G['o32_age_credit'](p, Y, G['pv_games'](p, Y))) / PLF)


def S1(lam):
    def use(pos, age):
        return MA.REPL[pos] - lam * cf.delta(pos, age)
    op, of = MA.proj_from_peak, MA.prod_floor
    MA.proj_from_peak = cf.make_proj_w4(use)
    MA.prod_floor = cf.make_floor_w4(use)

    def un():
        MA.proj_from_peak = op
        MA.prod_floor = of
    return un


P('=== ORDER E · THE BAR ARITHMETIC AT THE NAMED ROWS (avg points per game) ===')
P('flat bar = REPL[pos] - REPL_DROP(3) = the number price6 actually subtracts inside the projection.')
P('age bar  = flat bar - Delta(class, age), Delta = the engine\'s own O32_GATE_DELTA C3 gap.')
P('%-22s %5s %5s %8s %9s %8s %9s %9s' %
  ('row', 'pos', 'age', 'shown', 'flat bar', 'age bar', 'vs flat', 'vs age'))
BARS = {}
for k in KEYS:
    p = BY[k]; pos = MA.gfut(p); a = cp._age_asof(p, 2026)
    flat = G['_O30BP_BARS'][pos]; d = cf.delta(pos, a); aged = flat - d
    shown = float(cp._lvl_wt(p, 2026))
    BARS[k] = dict(pos=pos, age=a, flat=flat, delta=d, aged=aged, shown=shown)
    P('%-22s %5s %5.0f %8.1f %9.1f %8.1f %+9.1f %+9.1f'
      % (k, pos, a, shown, flat, aged, shown - flat, shown - aged))
P('')

BASE = {k: legs(BY[k]) for k in KEYS}
P('=== S1 ISOLATION CHECK — does the counterfactual touch anything but the production leg? ===')
P('(v0_start, the day-0 pedigree leg and the entry anchor are all built from FROZEN load-time objects;')
P(' if S1 were leaking into them these three columns would move.)')
P('%-22s %10s %10s %10s %10s %10s %10s' % ('row', 'd_ev', 'd_Phat', 'd_v0', 'd_pedigree', 'd_anchor', 'd_rho'))
un = S1(1.0)
try:
    AFT = {k: legs(BY[k]) for k in KEYS}
finally:
    un()
for k in KEYS:
    b, a = BASE[k], AFT[k]
    P('%-22s %+10.2f %+10.2f %+10.6f %+10.6f %+10.6f %+10.6f'
      % (k, a['ev'] - b['ev'], a['phat'] - b['phat'], a['v0'] - b['v0'], a['ped'] - b['ped'],
         a['anch'] - b['anch'], a['rho'] - b['rho']))
mx = max(max(abs(AFT[k][c] - BASE[k][c]) for c in ('v0', 'ped', 'anch', 'rho', 'pi', 'cred')) for k in KEYS)
P('')
P('max |movement| across v0_start / pedigree leg / entry anchor / rho / pi / age-credit = %.10f -> %s'
  % (mx, 'CLEAN: S1 moves the production leg and nothing else' if mx < 1e-9 else
     'LEAK: S1 is NOT cleanly isolated, bound rather than quote'))
P('')
P('=== LEG DECOMPOSITION, baseline vs S1 full (board points) ===')
P('price = rho31(g)*Phat + pi(g,c_u,s)*v0_pedigree + age_credit')
for k in KEYS:
    b, a = BASE[k], AFT[k]
    P('  %-22s base: rho %.4f x Phat %8.1f = %8.1f | ped %8.1f x %.4f = %7.1f | cred %6.1f | ev %8.1f'
      % (k, b['rho'], b['phat'], b['rho'] * b['phat'], b['ped'], b['pi'], b['pi'] * b['ped'], b['cred'], b['ev']))
    P('  %-22s S1  : rho %.4f x Phat %8.1f = %8.1f | ped %8.1f x %.4f = %7.1f | cred %6.1f | ev %8.1f'
      % ('', a['rho'], a['phat'], a['rho'] * a['phat'], a['ped'], a['pi'], a['pi'] * a['ped'], a['cred'], a['ev']))

HERE = os.path.dirname(os.path.abspath(__file__))
json.dump(dict(bars=BARS, base=BASE, s1=AFT), open(os.path.join(HERE, 'ISOLATE_E.json'), 'w'), indent=1)
open(os.path.join(HERE, 'ISOLATE_E_out.txt'), 'w').write('\n'.join(LOG) + '\n')
P('wrote ISOLATE_E.json + ISOLATE_E_out.txt')
