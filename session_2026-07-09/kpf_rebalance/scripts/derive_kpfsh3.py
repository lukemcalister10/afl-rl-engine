"""T1 DERIVATION (part 3 — RECENCY-WINDOWED LD (top-2 high-games seasons within Y-3..Y)) — GAP-RECOVERY rate for the demonstrated-backed residual slice.
For established-KPF season-years where the SUSTAINED demonstrated level LD (mean top-2 high-games
seasons, 12-bar, as-of Y) sits ABOVE the current recency-weighted level Lc: how much of the gap
(LD - Lc) is recovered in Y+1..Y+3?  r = (best_fwd - Lc)/(LD - Lc), clipped [0, 1.5].
E[r] = the honest retention rate for the residual slice that demonstrated output backs.
Also: E[max(fwd - LD, 0)] — delivery beyond ALL demonstration (the genuinely loose slice).
And the named players' 2026 coordinates (Lc, LD incl. prorated in-progress season, m, dm).
Walk-forward-safe: Y in 2008..2022, outcomes <= 2025. Guard 5 on entry.
Usage: derive_kpfsh3.py <out.json>"""
import io, contextlib, json, os, sys
import numpy as np
HERE = '/home/user/afl-rl-engine'
sys.path.insert(0, HERE)
import boot_guard
boot_guard.assert_boot('derive_kpfsh3', store_path='/home/claude/rl_workspace/rl_after/rl_model_data.json')
out = sys.argv[1]
os.chdir('/home/claude/rl_workspace/rl_after')
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA = g['MA']; cp = g['cp']; era = g['era']; REF = g.get('REF', 100)
_fEy = g['_fEy']

def adj(p, y, a):
    return a * REF / era.get(y, REF)

def LD_top2(p, Y):
    """sustained demonstrated level as-of Y: mean of top-2 high-games seasons (12-bar; in-progress
    season prorated 12*fE — same D10 convention as bestlvl's 6-bar)."""
    ls = sorted((adj(p, x['year'], x['avg']) for x in p['scoring']
                 if Y-3 <= x['year'] <= Y and x.get('games', 0) >= 12.0 * (_fEy(Y) if x['year'] == Y else 1.0)),
                reverse=True)
    if len(ls) < 2:
        return None
    return float(np.mean(ls[:2]))

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
        LD = LD_top2(p, Y)
        if LD is None:
            continue
        Lc = g['_lvlcurr'](p, Y)
        fwd = [adj(p, x['year'], x['avg']) for x in p['scoring']
               if Y < x['year'] <= Y + 3 and x.get('games', 0) >= 6]
        best_fwd = max(fwd) if fwd else 0.0
        samples.append({'key': p['key'], 'Y': Y, 'Lc': round(Lc, 2), 'LD': round(LD, 2),
                        'gap': round(LD - Lc, 2), 'up': round(best_fwd - Lc, 2),
                        'beyond': round(max(best_fwd - LD, 0.0), 2)})
gapS = [s for s in samples if s['gap'] >= 3.0]
print(f'established-KPF season-years: {len(samples)}; with demonstrated-above-current gap >=3: {len(gapS)}')
rs = np.array([min(max(s['up'] / s['gap'], 0.0), 1.5) for s in gapS])
print(f'GAP RECOVERY r=(best_fwd-Lc)/(LD-Lc) clip[0,1.5]: mean={rs.mean():.3f}  median={np.median(rs):.3f}  '
      f'P(r>=0.5)={np.mean(rs>=0.5):.2f}  P(full r>=1)={np.mean(rs>=1.0):.2f}')
for lo, hi in [(3, 6), (6, 10), (10, 99)]:
    S = [min(max(s['up'] / s['gap'], 0.0), 1.5) for s in gapS if lo <= s['gap'] < hi]
    if S:
        print(f'  gap in [{lo},{hi}): n={len(S):3d}  E[r]={np.mean(S):.3f}  median={np.median(S):.3f}')
byd = [(s['beyond']) for s in samples]
print(f'delivery BEYOND all demonstration: E[max(fwd-LD,0)]={np.mean(byd):.2f} (vs 4.2-4.6 beyond current — '
      f'the loose slice is the one past LD)')
# age robustness (T1 scope is age>=24; check the rate is not an old-age artifact)
for alo, ahi in [(24, 27), (27, 30), (30, 99)]:
    S = [min(max(s['up'] / s['gap'], 0.0), 1.5) for s in gapS
         if alo <= (cp._age_asof(next(x for x in MA.data if x.get('key') == s['key']), s['Y']) or 0) < ahi]
    if S:
        print(f'  age [{alo},{ahi}): n={len(S):3d}  E[r]={np.mean(S):.3f}')
# named 2026 coordinates
NAMED = ['jake-waterman', 'charlie-curnow', 'riley-thilthorpe', 'josh-treacy', 'sam-darcy', 'jeremy-cameron',
         'logan-mcdonald', 'mitch-georgiades', 'jack-lukosius', 'jack-gunston', 'aaron-naughton', 'harry-mckay',
         'peter-wright', 'darcy-fogarty', 'ben-king', 'nick-larkey', 'mitchito-owens']
named = {}
print(f"\n{'key':22s} {'nq':>2} {'Lc':>6} {'LD':>6} {'m':>6} {'dm=max(m,LD-R)':>8}")
for k in NAMED:
    p = next((x for x in MA.data if x.get('key') == k), None)
    if p is None:
        continue
    Lc = g['_lvlcurr'](p, 2026); LD = LD_top2(p, 2026); R = MA.REPL['KEY_FWD']
    m = Lc - R; dm = max(m, (LD - R) if LD is not None else m)
    named[k] = {'Lc': round(Lc, 1), 'LD': round(LD, 1) if LD else None, 'm': round(m, 1), 'dm': round(dm, 1),
                'nq': g['_nqual'](p, 2026)}
    print(f"{k:22s} {named[k]['nq']:>2} {Lc:6.1f} {LD if LD else -1:6.1f} {m:6.1f} {dm:8.1f}")
json.dump({'n': len(samples), 'n_gap': len(gapS), 'E_r': float(rs.mean()), 'median_r': float(np.median(rs)),
           'E_beyond': float(np.mean(byd)), 'named': named, 'samples': samples}, open(out, 'w'), indent=1)
print('wrote', out)
