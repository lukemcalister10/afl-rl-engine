"""#336 DESIGN PROBE (#334 ORDER 3b) — MINIMAL, MEASUREMENT ONLY. NO DESIGN IS WIRED BY THIS FILE.

Run under the budget rule the order itself set: if the channel split shows the year-1 drop does NOT
live in the unresolved-P / anchor leg, implement nothing beyond a minimal probe and state the ceiling.
The split says exactly that (the P-leg owns -0.2% of the give-back), so this file probes the two
candidate mechanisms and prints their ceilings instead of building either.

  (a) THE DISCOUNT UNWIND. Does the anchor leg a still-unresolved player is priced against carry one
      year of unwind as the future comes one year closer, or is it static in present value?
  (b) TENURE-CONDITIONAL P. What does P(ever establishes | not yet established at tenure t) do as t
      rises? The order asked for the sign to be stated plainly whichever way it falls.
"""
import sys, os, io, json, contextlib, statistics
sys.path.insert(0, '/home/user/afl-rl-engine/docs/evidence/composition_2026-08-10')
import numpy as np
import engine_load
g = engine_load.load()
MA = g['MA']; cp = g['cp']

print("=" * 100)
print("(a) THE ANCHOR LEG ACROSS TENURE — is it static in present value?")
print("=" * 100)
print("  the leg, from the source:  anch(p,tau) = R(class, pick, tau) x entry_anchor(p)")
print("    entry_anchor(p) = v0_start(p) for a non-pool row (_merged_recover.py:1830-1835)")
print("    R = _R_surf(...) = np.interp(tau, [0..6], [1.0] + dv), dv ISOTONIC NON-INCREASING (:1133-1144)")
print("  so the leg is  (a year-0 present value)  x  (a retention factor that only ever falls).")
print("  THERE IS NO (1+d)**tau TERM ANYWHERE IN IT.  Printed as a table, not asserted:\n")
_R = g['_R_surf']; _cls = g['_sitout_cls']
print(f"  {'class':8} {'pick':>5} " + "".join(f"{'tau=%d'%t:>9}" for t in range(0, 7)))
for cls, pk in [('nonKPP', 3), ('nonKPP', 35), ('KPP', 8), ('RUCK', 20)]:
    print(f"  {cls:8} {pk:5} " + "".join(f"{_R(cls, pk, t):9.4f}" for t in range(0, 7)))
print("\n  and what an HONEST as-of price would carry beside it, at the engine's own balanced-lens rate:")
d = g['MA'].LENS['bal'] if hasattr(g['MA'], 'LENS') else 0.14
print(f"    balanced-lens discount d = {d:.2f}   unwind (1+d)**tau = "
      + "  ".join(f"tau{t}:{(1+d)**t:.3f}" for t in range(0, 5)))
print("  READING: R falls with tenure while the unwind would rise with it. The two are opposite in")
print("  sign, and only one of them is in the code. That is the order's mechanism (a), CONFIRMED as a")
print("  code fact. Whether it is where the #336 year-1 value went is a SEPARATE question, answered")
print("  by the channel split, not by this table.")

# does entry_anchor itself move with the as-of clock?
def eligible(p): return MA.GRP.get(p.get('pos')) and not p.get('_pvc_exclude')
players = [p for p in MA.data if eligible(p)]
best = {}
for p in players:
    k = (p.get('key') or MA.slug(p['player']), p.get('type'), p.get('year'))
    if k not in best or len(p['scoring']) > len(best[k]['scoring']): best[k] = p
players = list(best.values())
POP = [p for p in players if p.get('type') == 'ND' and p.get('pick') and 1 <= p['pick'] <= 64
       and p.get('year') and 2004 <= p['year'] <= 2022]
ea = g['entry_anchor']
print("\n  DOES entry_anchor MOVE WITH THE AS-OF CLOCK? (same 60 rows, BASE_REF/AGE_REF advanced)")
sample = POP[::max(1, len(POP)//60)][:60]
rows = {}
for Y in (2020, 2021, 2022):
    MA.BASE_REF = Y; MA.AGE_REF = Y; MA._pe_clear()
    rows[Y] = [float(ea(p)) for p in sample]
MA.BASE_REF = MA.AGE_REF = 2026; MA._pe_clear()
same = sum(1 for i in range(len(sample)) if abs(rows[2020][i] - rows[2022][i]) < 1e-9)
print(f"    rows probed {len(sample)}   entry_anchor IDENTICAL across 2020/2021/2022: {same}")
print("    => entry_anchor is a FIXED year-zero object; it does not re-price as the clock advances.")

print("\n" + "=" * 100)
print("(b) TENURE-CONDITIONAL P  —  P(ever establishes | NOT YET established at tenure t)")
print("=" * 100)
QUAL = g['MA'].QUAL_336 if hasattr(g['MA'], 'QUAL_336') else 6
hist = MA.hist
def debutyr(p):
    C = p.get('year')
    return None if C is None else (C if p.get('type') == 'MSD' else C + 1)
def est_year(p):
    ys = [r['year'] for r in p['scoring'] if r['games'] >= QUAL]
    return min(ys) if ys else None
K = 10.0
print(f"  population = the engine's own hist ({len(hist)} rows), establishment bar >= {QUAL} games,")
print(f"  shrinkage n/(n+K) with K = {K:.0f} toward the all-tenure marginal — the SAME discipline #336 uses.")
print(f"\n  {'t':>3} {'at risk':>8} {'ever est':>9} {'raw P':>8} {'shrunk P':>9}")
allest = sum(1 for p in hist if est_year(p) is not None)
pbar = allest / len(hist)
prev = None
for t in range(1, 7):
    at_risk = []
    for p in hist:
        d = debutyr(p)
        if d is None: continue
        ey = est_year(p)
        # still unresolved entering tenure t: no >=6g season strictly before d+t
        if ey is not None and ey < d + t: continue
        at_risk.append(p)
    n = len(at_risk); k = sum(1 for p in at_risk if est_year(p) is not None)
    P = (k / n) if n else 0.0
    Ps = (k + K * pbar) / (n + K)
    flag = '' if prev is None else ('  DOWN' if Ps < prev else '  UP')
    print(f"  {t:3} {n:8} {k:9} {P:8.4f} {Ps:9.4f}{flag}")
    prev = Ps
print(f"\n  all-tenure marginal P(ever establishes) = {pbar:.4f}  ({allest}/{len(hist)})")
print("  READING, stated whichever way it fell: by iterated expectations the year-1 establishers LEAVE")
print("  the not-yet-established pool, so conditioning on 'still unresolved at t' can only lower P as t")
print("  rises. The table above is the measurement of that. A design that swapped the flat career P for")
print("  this conditional one would therefore charge an unresolved year-2 player MORE than a year-1 one,")
print("  i.e. it DEEPENS the dip rather than lifting it. It is not wired, and it is not proposed as a lift.")

print("\n" + "=" * 100)
print("(c) WHERE THE VALUE ACTUALLY WENT — the par sample change, and the ONE sizing number")
print("=" * 100)
sys.path.insert(0, '/home/user/afl-rl-engine/engine/forward_valuation')
import importlib
pb = importlib.import_module('par_build')
CP = pb.CP
pool = [p for p in MA.data if MA.GRP.get(p.get('pos'))
        and (p.get('pick') or p.get('_ft')) and pb.DRAFT_LO <= pb.draftyr(p) <= pb.DRAFT_HI]
raw = []
for p in pool:
    pk = min(MA.effpk(p), CP.KMAX); d0 = pb.draftyr(p)
    for T in range(1, pb.TEN_MAX + 1):
        Y = d0 + T; r = pb.season_row(p, Y); gm = r['games'] if r else 0
        if gm > 0:
            pos = pb.season_pos(r)
            if pos is None: continue
            raw.append((pos, pk, T, Y, gm, p))
print(f"  raw played (pos,tenure) observations in the par cohort: {len(raw)}")
print("\n  THE SAMPLE CHANGE #336 MADE, re-measured here from the same rows (cell mean of _lvl_wt):")
print(f"  {'T':>3} {'n(>=6g)':>8} {'n(>=1g est)':>12} {'mean >=6g':>10} {'mean >=1g':>10} {'ratio':>7}"
      f" {'exp-wtd >=1g':>13} {'exp/equal':>10}")
for T in range(1, 7):
    a = [(CP._lvl_wt(p, Y), gm) for (pos, pk, t, Y, gm, p) in raw if t == T and gm >= pb.MIN_GAMES]
    b = [(CP._lvl_wt(p, Y), gm) for (pos, pk, t, Y, gm, p) in raw
         if t == T and gm >= 1 and pb._ever_established_338(p)]
    if not a or not b: continue
    ma = float(np.mean([x[0] for x in a])); mb = float(np.mean([x[0] for x in b]))
    mw = float(np.average([x[0] for x in b], weights=[min(x[1], 18.0) for x in b]))
    print(f"  {T:3} {len(a):8} {len(b):12} {ma:10.2f} {mb:10.2f} {mb/ma:7.3f} {mw:13.2f} {mw/mb:10.3f}")
print("\n  COLUMN 'ratio' is the #336 par sample change, reproduced independently: it is FRONT-LOADED,")
print("  which is why its price effect lands on year 1 and fades out by year 6.")
print("  COLUMN 'exp/equal' is the SIZING OF ONE CANDIDATE REPAIR AND NOTHING MORE: the same")
print("  de-survivored sample, with each season weighted by its own exposure (games, capped at 18)")
print("  instead of counting a one-game debut and a twenty-game season equally. It re-admits NO")
print("  survivor bias — every faded establisher's season is still in the sample — and it refunds no")
print("  bust charge, because P is untouched. IT IS NOT WIRED AND NOT PROPOSED HERE; it is a number")
print("  for the owner to rule on, and its price effect is UNMEASURED (a cell mean is not a fit, and")
print("  the fit's isotonic priors and kernel ESS would carry some of it away).")
