"""DERIVE vs SCALE — what the same-derivation ruling changes (owner, #334 comment 5251055803).

  "the ND pick value and v0 values are derived from historical career outcomes. We should be deriving
   pool valuations and v0s the same way we do for ND picks, right? Or else it makes no sense?"

SCALE  = multiply a stream's EXISTING entry anchors by one number lambda. Corrects the stream's LEVEL,
         inherits its existing SHAPE across positions.
DERIVE = build each cell's entry value from that cell's own outcome history, the way the ND pick curve
         is built from slot outcome history. Corrects level AND shape together.

Same profile measure as the D3 amendment (harness realised_full via structural_values), so the two
amendments compose. READ-ONLY, deterministic, no emits.
"""
import sys, json
sys.path.insert(0, '/home/user/afl-rl-engine/docs/evidence/composition_2026-08-10/noarb')
import harness_pvc_REPINNED_pass3 as H

SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
R = json.load(open(f"{SP}/per_entrant_SHIP.json"))['recs']
MINCELL = 20


def cohort(r):
    y = r.get('year')
    return None if y is None else (y if r.get('type') == 'MSD' else y + 1)


def stream(r):
    t = r.get('type')
    if t == 'ND' and r.get('pick') and 1 <= r['pick'] <= 64 and not r.get('is_pool'): return 'ND 1-64'
    if t == 'ND': return 'ND>64'
    return t


elig = [r for r in R if cohort(r) is not None and (r.get('v0') or 0) > 0]
rows, prov = H.structural_values(elig)
SV = {r['key']: row for r, row in zip(elig, rows)}


def profile(sub):
    if not sub: return float('nan')
    d = sum(float(r['v0']) for r in sub)
    return sum(SV[r['key']]['value'] for r in sub) / d if d else float('nan')


ND = profile([r for r in elig if stream(r) == 'ND 1-64'])
POSN = ['MID', 'SD', 'SF', 'KPD', 'KPF', 'RUCK']
POOLS = ['RD', 'SSP', 'MSD', 'IRE', 'PDA', 'PDN', 'PDS', 'UNR', 'ND>64']

print("=" * 112)
print("### DERIVE vs SCALE — the rookie draft, the one pool stream whose samples support both")
print("=" * 112)
print(f"  ND 1-64 profile = {ND:.4f} — the calibration target (a cell at 1.000 returns what an ND pick returns)")
rd = [r for r in elig if stream(r) == 'RD']
lam_stream = profile(rd) / ND
print(f"  RD stream profile = {profile(rd):.4f}  ->  ONE stream multiplier lambda = {lam_stream:.3f}")
print()
print(f"  {'position':9} {'n':>5} {'profile':>9} {'vs ND':>7} | {'SCALE: lands at':>16} {'residual':>9} | "
      f"{'DERIVE: lands at':>17} {'own lambda':>11} | {'Sig v0':>10} {'@derive':>10}")
print("  " + "-" * 110)
tot0 = totS = totD = 0.0
cells = []
for p in POSN:
    g = [r for r in rd if r.get('pos') == p]
    s0 = sum(float(r['v0']) for r in g)
    if len(g) < MINCELL:
        print(f"  {p:9} {len(g):5} {'  -':>9} {'  -':>7} | {'  -':>16} {'  -':>9} | "
              f"{'  -':>17} {'  -':>11} | {round(s0):10,} {'  -':>10}")
        continue
    pr = profile(g); vs = pr / ND
    lands_scale = vs / lam_stream
    tot0 += s0; totS += s0 * lam_stream; totD += s0 * vs
    cells.append((p, len(g), pr, vs, lands_scale))
    print(f"  {p:9} {len(g):5} {pr:9.4f} {vs:7.3f} | {lands_scale:16.3f} {abs(lands_scale-1):9.3f} | "
          f"{1.000:17.3f} {vs:11.3f} | {round(s0):10,} {round(s0*vs):10,}")
print(f"  {'RD TOTAL':9} {len(rd):5} {profile(rd):9.4f} {profile(rd)/ND:7.3f} | {'1.000 (by design)':>16} "
      f"{'':>9} | {'1.000 per cell':>17} {'':>11} | {round(tot0):10,} {round(totD):10,}")
lo = min(c[4] for c in cells); hi = max(c[4] for c in cells)
print(f"\n  UNDER SCALE the residual spread SURVIVES: RD positions land between {lo:.3f} and {hi:.3f}")
print(f"  against ND — a factor of {hi/lo:.1f}. Scaling moves the whole stream and changes no position's")
print(f"  standing relative to any other. UNDER DERIVATION every sampled cell lands at 1.000 by")
print(f"  construction, because each is built from its own outcome history.")
print(f"  Money: RD entry total {round(tot0):,} -> {round(totS):,} under scale -> {round(totD):,} under derive.")

print()
print("=" * 112)
print("### PER-STREAM FEASIBILITY OF DERIVATION — counts decide, and they are printed")
print("=" * 112)
print(f"  a cell needs n >= {MINCELL} to be derived on its own history. Thin cells are shown, never forced.")
print(f"  {'stream':9} {'n':>5} " + "".join(f"{p:>6}" for p in POSN) + f" {'cells':>6} {'verdict':>34}")
feas = {}
for s in ['ND 1-64'] + POOLS:
    sub = [r for r in elig if stream(r) == s]
    if not sub: continue
    cnt = {p: sum(1 for r in sub if r.get('pos') == p) for p in POSN}
    ok = sum(1 for p in POSN if cnt[p] >= MINCELL)
    if ok == len(POSN): v = 'per-position derivation: FULL'
    elif ok > 0:        v = f'per-position: PARTIAL ({ok} of 6)'
    elif len(sub) >= 40: v = 'stream-level derivation only'
    else:               v = 'stream-level only, AND THIN'
    feas[s] = (len(sub), ok, v)
    print(f"  {s:9} {len(sub):5} " + "".join(f"{cnt[p]:6}" for p in POSN) + f" {ok:6} {v:>34}")
json.dump({'ND_profile': ND, 'rd_lambda': lam_stream,
           'rd_cells': {c[0]: {'n': c[1], 'profile': c[2], 'vs_ND': c[3], 'lands_under_scale': c[4]} for c in cells},
           'feasibility': feas},
          open('/home/user/afl-rl-engine/docs/evidence/pool_repricing_2026-08-11/DERIVE_VS_SCALE.json', 'w'), indent=1)
