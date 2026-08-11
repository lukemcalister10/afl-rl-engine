"""Alternative par reading: rl_model.py's OWN par object expected_c(pos, pick, season)
   (rl_model.py:370, built on expected() :221; named 'below-par' at :1104 / 'position+experience bar' at :1094).
   Reported beside the live value-path par_at so the sitting sees both."""
import engine_load, math
g = engine_load.load()
MA = g['MA']; cp = g['cp']; PR = g['PR']; ev = g['ev']
entry_anchor = g['entry_anchor']; _ageR = g['_ageR']
Y = 2026; G0 = 8.0; QMAX = 2.0; KMAX = int(cp.KMAX)
data = MA.data
def get(k): return next((p for p in data if p.get('key') == k), None)
def career_g(p): return sum(x['games'] for x in p['scoring'])
def sa_c(p):
    t = career_g(p)
    return 0.0 if t == 0 else sum(x['games'] * x['avg'] for x in p['scoring']) / t

CASES = [('noah-mraz', None, None), ('archie-ludowyke', None, None),
         ('luke-beecken', None, None), ('gerrick-weedon', None, None),
         ('zeke-uwland', None, None), ('toby-conway', None, None),
         ('toby-conway', 1, 120.0)]
print('%-22s %-5s %-5s %8s %8s %8s | %8s %8s | %6s %6s' %
      ('key', 'pos', 'epk', 'sa', 'par_at', 'expC1', 'Q_parat', 'Q_expC', 'w_pa', 'w_ec'))
for k, go, so in CASES:
    p = get(k)
    pos = MA.gfut(p); pk = MA.effpk(p)
    gg = career_g(p) if go is None else go
    sa = sa_c(p) if so is None else so
    a = entry_anchor(p); e = float(ev(p, Y))
    T = int(min(max(_ageR(p) - 17, 1), 6))
    par_pa = PR.par_at(pos, min(pk, KMAX), T)
    par_ec = MA.expected_c(pos, pk, T)      # rl_model.py:370 — the season-stage expected bar
    G = gg / (gg + G0); gate = min(max(e / a, 0.0), 1.0)
    Qa = min(max(sa / par_pa, 0), QMAX); Qe = min(max(sa / par_ec, 0), QMAX)
    print('%-22s %-5s %-5d %8.2f %8.2f %8.2f | %8.4f %8.4f | %6.4f %6.4f' %
          (k + ('*' if go else ''), pos, pk, sa, par_pa, par_ec, Qa, Qe, G * Qa * gate, G * Qe * gate))
