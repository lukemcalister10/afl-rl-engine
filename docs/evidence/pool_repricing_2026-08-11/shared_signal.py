"""THE SHARED-SIGNAL PRE-CHECK + K SENSITIVITY (owner ruling, #334 comment 5251186828).

Borrowing a positional SHAPE from the pool assumes the positional signal is SHARED across pathways.
RD and ND both have all six cells sampled, so the assumption is testable directly rather than assumed.

SHAPE is measured as the cell's profile divided by its own stream's all-in value. That removes the
LEVEL difference (which is the whole point of the repricing) and leaves only the positional pattern.
READ-ONLY, deterministic, no emits.
"""
import sys, json, statistics
sys.path.insert(0, '/home/user/afl-rl-engine/docs/evidence/composition_2026-08-10/noarb')
import harness_pvc_REPINNED_pass3 as H
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
R = json.load(open(f"{SP}/per_entrant_SHIP.json"))['recs']
POSN = ['MID', 'SD', 'SF', 'KPD', 'KPF', 'RUCK']
POOLS = ['RD', 'SSP', 'MSD', 'IRE', 'PDA', 'PDN', 'PDS', 'UNR', 'ND>64']
def cohort(r):
    y = r.get('year'); return None if y is None else (y if r.get('type') == 'MSD' else y + 1)
def stream(r):
    t = r.get('type')
    if t == 'ND' and r.get('pick') and 1 <= r['pick'] <= 64 and not r.get('is_pool'): return 'ND 1-64'
    if t == 'ND': return 'ND>64'
    return t
elig = [r for r in R if cohort(r) is not None and (r.get('v0') or 0) > 0]
rows, _ = H.structural_values(elig); SV = {r['key']: x for r, x in zip(elig, rows)}
val = lambda s: sum(SV[r['key']]['value'] for r in s); ent = lambda s: sum(float(r['v0']) for r in s)
def prof(s): return val(s) / ent(s) if s and ent(s) else float('nan')

print("=" * 104)
print("### THE SHARED-SIGNAL PRE-CHECK — is the positional pattern the same in RD and ND?")
print("=" * 104)
print("  SHAPE = cell profile / that stream's own all-in value. Level removed; pattern left.")
nd = [r for r in elig if stream(r) == 'ND 1-64']; rd = [r for r in elig if stream(r) == 'RD']
NDa, RDa = prof(nd), prof(rd)
print(f"  ND all-in {NDa:.4f}   RD all-in {RDa:.4f}")
print()
print(f"  {'position':9} {'ND n':>6} {'ND shape':>9} {'RD n':>6} {'RD shape':>9} {'ratio RD/ND':>12} {'rank ND':>8} {'rank RD':>8}")
shapes = {}
for p in POSN:
    gn = [r for r in nd if r.get('pos') == p]; gr = [r for r in rd if r.get('pos') == p]
    sn, sr = prof(gn) / NDa, prof(gr) / RDa
    shapes[p] = (len(gn), sn, len(gr), sr)
rk_nd = {p: i+1 for i, p in enumerate(sorted(POSN, key=lambda p: -shapes[p][1]))}
rk_rd = {p: i+1 for i, p in enumerate(sorted(POSN, key=lambda p: -shapes[p][3]))}
for p in POSN:
    n1, s1, n2, s2 = shapes[p]
    print(f"  {p:9} {n1:6} {s1:9.4f} {n2:6} {s2:9.4f} {s2/s1:12.4f} {rk_nd[p]:8} {rk_rd[p]:8}")
xs = [shapes[p][1] for p in POSN]; ys = [shapes[p][3] for p in POSN]
mx, my = statistics.mean(xs), statistics.mean(ys)
cov = sum((a-mx)*(b-my) for a, b in zip(xs, ys))
r = cov / ((sum((a-mx)**2 for a in xs) * sum((b-my)**2 for b in ys)) ** 0.5)
conc = sum(1 for i in range(6) for j in range(i+1, 6)
           if (xs[i]-xs[j]) * (ys[i]-ys[j]) > 0)
print(f"\n  correlation of the two shape vectors : {r:+.4f}")
print(f"  concordant pairs (ordering agreement) : {conc} of 15")
print(f"  spread ND {min(xs):.3f}-{max(xs):.3f} (factor {max(xs)/min(xs):.2f})   "
      f"RD {min(ys):.3f}-{max(ys):.3f} (factor {max(ys)/min(ys):.2f})")

print()
print("=" * 104)
print("### K SENSITIVITY — how much of its OWN data a thin cell keeps, w = n/(n+K)")
print("=" * 104)
print("  the engine's existing convention is K = 10 (rl_model.py _pest_336; par_build K_338).")
print(f"  {'cell':22} {'n':>4} " + "".join(f"{'K=%d'%k:>9}" for k in (5, 10, 20)))
THIN = [(s, p) for s in POOLS for p in POSN]
shown = 0
for s, p in THIN:
    g = [r for r in elig if stream(r) == s and r.get('pos') == p]
    n = len(g)
    if n == 0 or n >= 20: continue
    if shown >= 10: break
    shown += 1
    print(f"  {s+' '+p:22} {n:4} " + "".join(f"{n/(n+k):9.3f}" for k in (5, 10, 20)))
print(f"  {'(a sampled cell, ref)':22} {72:4} " + "".join(f"{72/(72+k):9.3f}" for k in (5, 10, 20)))
print("\n  At K=10 a 14-player cell keeps 58% of its own signal and borrows 42%; at K=5 it keeps 74%;")
print("  at K=20 it keeps 41%. K is how fast the engine stops believing a small cell.")
json.dump({'ND_allin': NDa, 'RD_allin': RDa, 'shapes': {p: shapes[p] for p in POSN},
           'corr': r, 'concordant': conc},
          open('/home/user/afl-rl-engine/docs/evidence/pool_repricing_2026-08-11/SHARED_SIGNAL.json','w'), indent=1)
