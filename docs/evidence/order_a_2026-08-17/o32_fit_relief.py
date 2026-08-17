#!/usr/bin/env python3
"""ORDER A / CANDIDATE 32 — M6b-4(b): THE SELECTION-RELIEF SIZE λ, FIT ON THE S2 SPECTRUM SURFACE.

Model (PREREG_32 M4/M6): a cell at depth N with g games in season N-1 sits, under the NEW
definitions, at c_u = N - min(1, g/2) (G*=2 credit; no-reset reading, disclosed: the cells are not
delivery-conditioned so the fit is conservative w.r.t. M3), and the law would price its pedigree
fade at
        D_model = min(1, D31(c_u) * (1 + λ·σ(g))),      σ(g) = clip((g-5)/5, 0, 1)
against the cell's measured D (capped at 1 — the ceiling stays production-only; the relief cannot
and does not chase value above full pedigree). Fit: n-weighted least squares over the prereg grid
λ ∈ [0, 1.2] step 0.01, on every non-thin cell (the instrument's own thin flags), all depths.
The g=0 and g<5 cells carry σ=0, so they anchor the fit at λ-invariance: the credit moves the
clock, the relief pays ONLY the ≥5-games selection residual — no signal is paid twice.
D31 = the Candidate 31 fade row, which M6b-4(a) just re-derived at deviation 0.0 (FADE_32.json).
"""
import os, json, math

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.dirname(HERE)
S2 = json.load(open(os.path.join(EV, 'order32_s2_2026-08-17', 'SPECTRUM_S2.json')))
F32 = json.load(open(os.path.join(HERE, 'FADE_32.json')))
assert F32['p_d0_held'], 'the fade row moved — this fit must be re-run on the moved row'
D_ROW = {int(k): float(v) for k, v in F32['rederived_32'].items()}
D_ROW[1] = 1.0
FLAT_FROM = 4


def D31(c):
    if c <= 1.0:
        return 1.0
    if c >= FLAT_FROM:
        return D_ROW[FLAT_FROM]
    n = int(math.floor(c)); f = c - n
    d0 = D_ROW[n]; d1 = D_ROW[n + 1]
    return d0 if f <= 0.0 else math.exp((1.0 - f) * math.log(d0) + f * math.log(d1))


def sigma(g):
    return max(0.0, min(1.0, (g - 5.0) / 5.0))


CELLS = []
for key, c in sorted(S2['Q1']['cells'].items()):
    if not c.get('n') or c.get('thin', True):
        continue
    N = int(c['depth']); g = float(c['med_g'])
    cu = N - min(1.0, g / 2.0)
    CELLS.append(dict(key=key, depth=N, g=g, n=int(c['n']), D_cell=float(c['D']),
                      target=min(1.0, float(c['D'])), cu_new=cu, D_base=D31(cu), sig=sigma(g)))

GRID = [round(0.01 * i, 2) for i in range(0, 121)]
PROF = []
best = None
for lam in GRID:
    sse = 0.0
    for c in CELLS:
        m = min(1.0, c['D_base'] * (1.0 + lam * c['sig']))
        sse += c['n'] * (m - c['target']) ** 2
    PROF.append((lam, sse))
    if best is None or sse < best[1]:
        best = (lam, sse)
LAM = best[0]

print('ORDER A / CANDIDATE 32 — SELECTION RELIEF λ, FIT ON THE S2 SPECTRUM SURFACE')
print('  cells (non-thin, the instrument\'s own flags):')
print('  %-8s %5s %6s %8s %8s %8s %8s %10s' % ('cell', 'n', 'g', 'sigma', 'c_u_new', 'D_base', 'target', 'model@λ*'))
for c in CELLS:
    m = min(1.0, c['D_base'] * (1.0 + LAM * c['sig']))
    print('  %-8s %5d %6.1f %8.2f %8.3f %8.4f %8.4f %10.4f' % (
        c['key'], c['n'], c['g'], c['sig'], c['cu_new'], c['D_base'], c['target'], m))
print('  λ* = %.2f   (n-weighted SSE %.4f)' % (LAM, best[1]))
lo = min(l for l, s in PROF if s <= best[1] * 1.10)
hi = max(l for l, s in PROF if s <= best[1] * 1.10)
print('  identifiability (SSE within +10%% of optimum): λ ∈ [%.2f, %.2f] — reported, honest: the '
      'informative cells are 3|6-10 (n=31), 3|11+ (n=44) and 4|11+ (n=12); beyond the point where '
      'the capped model reaches 1 the objective flattens' % (lo, hi))

json.dump(dict(order='ORDER A / Candidate 32 — selection relief size',
               model='D_relieved = min(1, D(c_u)·(1+λ·σ(g_season))), σ = clip((g-5·f)/(5·f),0,1)',
               lam=LAM, sse=best[1], grid=[0.0, 1.2, 0.01],
               ident_band_10pct=[lo, hi],
               profile=[[l, s] for l, s in PROF[::5]],
               cells=CELLS,
               fade_row_source='FADE_32.json (re-derived at deviation 0.0 from 31-F)',
               disclosures=['no-reset reading of the cells (not delivery-conditioned): conservative w.r.t. M3',
                            'the deep saturated cells (3|11+, 4|11+) pull λ up against the cap; the cap '
                            'itself (never above full pedigree) is what bounds the pay, and the '
                            'identifiability band is published rather than smoothed']),
          open(os.path.join(HERE, 'RELIEF_32.json'), 'w'), indent=1, sort_keys=True)
print('written: RELIEF_32.json')
