"""T1 DERIVATION — demonstration-keyed retention of the established-KPF residual.
QUESTION: how often (and how much) does an established KPF (nqual>=4, age>=24) subsequently DELIVER
output ABOVE his then-demonstrated level — conditioned on his SUSTAINED demonstrated margin
d = mean(top-2 era-adjusted qualifying seasons) - REPL[KEY_FWD]?
If upside realization rises with d, a demonstration-keyed retention SH(d) is data-earned: the residual
above the engine's price-of-demonstrated-level is NOT equally 'loose' at every d.
Walk-forward-safe: seasons Y in 2008..2022, outcomes measured Y+1..Y+3 (all <= 2025, observed).
One engine load (helpers only, no pricing). Guard 5 on entry.
Usage: derive_kpfsh.py <out.json>"""
import io, contextlib, json, os, sys
import numpy as np
HERE = '/home/user/afl-rl-engine'
sys.path.insert(0, HERE)
import boot_guard
boot_guard.assert_boot('derive_kpfsh', store_path='/home/claude/rl_workspace/rl_after/rl_model_data.json')
out = sys.argv[1]
os.chdir('/home/claude/rl_workspace/rl_after')
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA = g['MA']; cp = g['cp']; era = g['era']; REF = g.get('REF', 100)

def adj(p, y, a):                       # era-adjusted level (same convention as bestlvl)
    return a * REF / era.get(y, REF)

def qual_levels(p, Y, gbar=12):
    """era-adjusted levels of HIGH-GAMES seasons (games>=gbar) up to Y (completed seasons only)."""
    return sorted((adj(p, x['year'], x['avg']) for x in p['scoring']
                   if x['year'] <= Y and x['year'] < 2026 and x.get('games', 0) >= gbar), reverse=True)

def d_sust(p, Y):
    """SUSTAINED demonstrated margin: mean of top-2 high-games season levels (needs >=2) - REPL."""
    ls = qual_levels(p, Y)
    if len(ls) < 2:
        return None
    return float(np.mean(ls[:2])) - MA.REPL['KEY_FWD']

samples = []
for p in MA.data:
    if MA.gfut(p) != 'KEY_FWD' or p.get('type') not in ('ND', 'RD'):
        continue
    for Y in range(2008, 2023):
        if g['_nqual'](p, Y) < 4:
            continue
        a = cp._age_asof(p, Y)
        if a is None or a < 24.0:
            continue
        d = d_sust(p, Y)
        if d is None:
            continue
        Lc = g['_lvlcurr'](p, Y)
        fwd = [adj(p, x['year'], x['avg']) for x in p['scoring']
               if Y < x['year'] <= Y + 3 and x.get('games', 0) >= 6]
        if not fwd:                      # exited the system: delivered nothing above demonstrated
            fwd = [0.0]
        best_fwd = max(fwd)
        samples.append({'key': p['key'], 'Y': Y, 'd': round(d, 2), 'Lc': round(Lc, 2),
                        'up': round(best_fwd - Lc, 2), 'realized': int(best_fwd >= Lc - 1.0)})
print(f'samples (established-KPF season-years, 2008-2022): {len(samples)}')
BINS = [(-99, -8), (-8, 0), (0, 8), (8, 16), (16, 99)]
rows = []
for lo, hi in BINS:
    S = [s for s in samples if lo <= s['d'] < hi]
    if not S:
        continue
    ups = np.array([s['up'] for s in S]); rz = np.mean([s['realized'] for s in S])
    rows.append({'bin': f'[{lo},{hi})', 'n': len(S), 'mean_up': float(np.mean(ups)),
                 'mean_up_pos': float(np.mean(np.maximum(ups, 0.0))), 'p_realize': float(rz)})
    print(f"d in [{lo:>3},{hi:>3}): n={len(S):4d}  E[fwd-Lc]={np.mean(ups):+6.2f}  "
          f"E[max(fwd-Lc,0)]={np.mean(np.maximum(ups,0)):5.2f}  P(re-deliver >= Lc-1)={rz:.2f}")
# named present-day d values (sizing the T1/T2 ramps; report-only)
NAMED = ['jake-waterman', 'charlie-curnow', 'riley-thilthorpe', 'josh-treacy', 'sam-darcy', 'jeremy-cameron',
         'logan-mcdonald', 'mitch-georgiades', 'jack-lukosius', 'jack-gunston', 'aaron-naughton', 'harry-mckay',
         'peter-wright', 'darcy-fogarty', 'ben-king', 'jack-whitlock', 'jed-walter', 'ethan-read']
named_d = {}
for k in NAMED:
    p = next((x for x in MA.data if x.get('key') == k), None)
    if p is None:
        continue
    ls = qual_levels(p, 2026)
    named_d[k] = {'d_top2': round(float(np.mean(ls[:2])) - MA.REPL['KEY_FWD'], 2) if len(ls) >= 2 else None,
                  'n_hi_seasons': len(ls), 'top3': [round(x, 1) for x in ls[:3]]}
    print(f"{k:22s} d_top2={named_d[k]['d_top2']} hi-seasons={len(ls)} top3={named_d[k]['top3']}")
json.dump({'n': len(samples), 'bins': rows, 'named_d': named_d, 'samples': samples}, open(out, 'w'), indent=1)
print('wrote', out)
