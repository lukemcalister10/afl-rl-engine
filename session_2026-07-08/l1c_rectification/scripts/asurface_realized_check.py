"""L1c AMENDMENT 1 — A-SURFACE VALIDATION: realized-production cross-check (REPORT ONLY, no re-wiring).

The shipped A-surface (ycred_table.json) is BOOK-ENDOGENOUS: A_cell from consecutive-year BOOK values on the
credit-off walk-forward matrix (one-iteration drift declared). That basis is SANCTIONED — G-COHORT is an
internal no-arbitrage bound in book currency. THIS script prints the required cross-check: A_cell re-derived
from REALIZED PRODUCTION trajectories, same cells, side by side, with >15% relative divergence flagged and
the aggregate effect on the w=0.7 landing if the realized basis were used instead. The owner rules with the
table in view.

REALIZED CONSTRUCTION (raw scoring -> SCAR via the standard machinery, exits -> 0):
  raw_real(p, Y) = sum over ACTUAL seasons y >= Y actually played:
        min(games_y/22, 1) * posval( lev_y + capt_prem(lev_y) - REPL[gfut] ) * 21 / 1.15^(y-Y)
  with lev_y = era-adjusted season average (adj = avg*REF/era[y]) — the engine's own level normalisation;
  posval/capt_prem/REPL/LENS['bal']=0.15 = the standard pricing machinery (proj_from_peak's year terms);
  v_real = raw_real^GAMMA (0.85) — the same concave raw->SCAR map the board applies (SCALE cancels in ratios).
  A player who never plays again from Y on has raw_real = 0 (EXITS -> 0; busts included).
DECLARED: no B2 haircuts, no floors, no priors — the realized basis prices DELIVERED production only; class
pool = the guard pool (2004-2020 incurve picked; late classes right-truncated at 2026, declared).
STRUCTURAL NOTE for the reader: a hindsight-value process can only re-rate one year at <= the discount rate
minus delivered consumption (v1 = own-year value + v2/1.15), so realized A is bounded ~<= +15% (~+12% after
GAMMA) by construction — the gap between the book surface and this bound IS the no-arbitrage tension the
guard exists to cap. Cell-aggregate A (plain class-sum ratio, no kernel) on the IDENTICAL pool both sides.
"""
import io, contextlib, json, os, sys
import numpy as np
HERE = '/home/user/afl-rl-engine'
OUT = f'{HERE}/session_2026-07-08/l1c_rectification/out'
sys.path.insert(0, HERE)
import boot_guard
boot_guard.assert_boot('asurface_realized', store_path='/home/claude/rl_workspace/rl_after/rl_model_data.json',
                       engine_head_path='/home/claude/rl_workspace/rl_after/_merged_recover.py')
os.chdir('/home/claude/rl_workspace/rl_after')

g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA = g['MA']; era = g['era']; REF = g['REF']; cp = g['cp']
GAMMA = float(os.environ.get('RL_GAMMA', '0.85')); D = 0.15

mat = json.load(open(f'{OUT}/s4_matrix_youngoff.json'))
store_by_key = {p.get('key'): p for p in MA.data if p.get('key')}
POS6 = ['MID', 'GEN_FWD', 'GEN_DEF', 'KEY_FWD', 'KEY_DEF', 'RUC']

def raw_real(p, Y):
    tot = 0.0
    gf = MA.gfut(p); rep = MA.REPL.get(gf, 0.0)
    for x in p.get('scoring') or []:
        y = x['year']
        if y < Y or y > 2026 or x.get('games', 0) <= 0:
            continue
        lev = x['avg'] * REF / era.get(y, REF)
        base = lev + MA.capt_prem(lev)
        tot += min(x['games'] / 22.0, 1.0) * MA.posval(base - rep) * 21.0 / ((1 + D) ** (y - Y))
    return tot

def v_real(p, Y):
    r = raw_real(p, Y)
    return r ** GAMMA if r > 0 else 0.0

# pool: guard classes, same records as the book-basis surface
cells = {}
for v in mat.values():
    C = int(v['year']) if v['year'] is not None else None
    if C is None or not v['incurve'] or v.get('pickless') or not v.get('pick') or not (2004 <= C <= 2020):
        continue
    cls = v['cpos']
    if cls not in POS6 or v['key'] not in store_by_key:
        continue
    p = store_by_key[v['key']]
    gy1 = sum(x['games'] for x in p.get('scoring') or [] if x['year'] == C + 1)
    sat = 1 if gy1 == 0 else 0
    b1 = float(v['Vpath'][0] or 0.0) if len(v['Vpath']) >= 1 else 0.0
    b2 = float(v['Vpath'][1] or 0.0) if len(v['Vpath']) >= 2 else 0.0
    if b1 <= 0:
        continue
    r1 = v_real(p, C + 1); r2 = v_real(p, C + 2)
    cells.setdefault((cls, sat), []).append((b1, b2, r1, r2, gy1, v['pick'], v['key']))

print('=== A-SURFACE CROSS-CHECK — book-basis vs realized-production basis (cell-aggregate, classes 2004-2020) ===')
print(f'{"cell":18s}{"n":>5s}{"A_book":>9s}{"A_real":>9s}{"reldiv":>8s}  flag')
side = {}
for cls in POS6:
    for sat in (0, 1):
        rows = cells.get((cls, sat), [])
        if not rows:
            continue
        sb1 = sum(r[0] for r in rows); sb2 = sum(r[1] for r in rows)
        sr1 = sum(r[2] for r in rows); sr2 = sum(r[3] for r in rows)
        Ab = sb2 / sb1 - 1.0
        Ar = (sr2 / sr1 - 1.0) if sr1 > 0 else None
        rel = abs(Ab - Ar) / max(abs(Ar), 0.05) if Ar is not None else None
        flag = 'DIVERGES >15%' if (rel is not None and rel > 0.15) else ''
        side[f'{cls}/{"sat" if sat else "played"}'] = dict(n=len(rows), A_book=round(Ab, 4),
                                                           A_real=(round(Ar, 4) if Ar is not None else None),
                                                           rel_div=(round(rel, 3) if rel is not None else None),
                                                           flag=bool(flag))
        print(f'{cls+"/"+("sat" if sat else "played"):18s}{len(rows):5d}{Ab:+9.3f}'
              f'{(f"{Ar:+9.3f}" if Ar is not None else "     n/a"):>9s}'
              f'{(f"{100*rel:6.0f}%" if rel is not None else "   n/a"):>8s}  {flag}')

# aggregate effect on the w=0.7 landing if the realized basis were used instead (arithmetic estimate — the
# shipped landing itself comes from the real w=0.7 book; numerator years held fixed, DECLARED approximation)
W = 0.7; G0 = 46.0
def lift(year_idx, basis):
    num = den = 0.0
    for (cls, sat), rows in cells.items():
        sb1 = sum(r[0] for r in rows); sb2 = sum(r[1] for r in rows)
        sr1 = sum(r[2] for r in rows); sr2 = sum(r[3] for r in rows)
        A = (sb2 / sb1 - 1.0) if basis == 'book' else ((sr2 / sr1 - 1.0) if sr1 > 0 else 0.0)
        A = max(A, 0.0)
        for b1, b2, _r1, _r2, gy1, _pk, k in rows:
            v = b1 if year_idx == 1 else b2
            p = store_by_key[k]; C = p['year']
            gg = sum(x['games'] for x in p.get('scoring') or [] if C < x['year'] <= C + year_idx)
            phi = (1.0 - gg / G0) ** 2 if gg < G0 else 0.0
            num += v * W * A * phi; den += v
    return num / den
for basis in ('book', 'real'):
    l1, l2 = lift(1, basis), lift(2, basis)
    y1, y2 = 57558.5 * (1 + l1), 70211.0 * (1 + l2)
    dn = min(y1, y2)
    print(f'\nESTIMATED w=0.7 landing on the {basis.upper()} basis (cell-aggregate A, numerators y4-6 held '
          f'fixed — approximation): y1 {y1:,.0f} (+{100*l1:.1f}%) y2 {y2:,.0f} (+{100*l2:.1f}%) den {dn:,.0f}'
          f' -> y4 {100*81959.2/dn:.1f}% y5 {100*81043.6/dn:.1f}% y6 {100*75822.8/dn:.1f}%')
json.dump(side, open(f'{OUT}/asurface_realized_check.json', 'w'), indent=1)
print(f'\nwrote {OUT}/asurface_realized_check.json — REPORT ONLY: the shipped surface stays book-basis '
      f'(sanctioned); the owner rules with this table in view.')
