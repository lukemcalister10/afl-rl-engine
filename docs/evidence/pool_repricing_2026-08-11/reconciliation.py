"""THE RECONCILIATION LAW AS A CHECKABLE TEST (owner ruling, #334 comment 5251155728).

  "like the ND, v0 may differ from the 'all-in value' of the selection, but across all possibilities,
   it doesn't. The average v0 of all pool (or pathways within it) players should be near identical to
   the all-in value."

THE TEST the build will run, per pathway:

    LAYER 1 (pathway value)  P_s      = SUM_over_stream(realised_full) / SUM_over_stream(v0) / ND
    LAYER 2 (player v0)      lam_c    = SUM_over_cell(realised_full)  / SUM_over_cell(v0)  / ND
    RECONCILIATION           SUM_c ( v0_c * lam_c )  ==  ( SUM_c v0_c ) * P_s      within tolerance

i.e. the ENTRY-WEIGHTED mean of the layer-2 multipliers must equal the layer-1 pathway multiplier.
Tolerance: 1e-9 relative on sampled cells (it is an identity, so anything above float noise is a bug).

CONDITION (a): the weighting convention must MATCH. This file also computes the headcount-weighted mean
to show, with a number, that it does NOT reconcile.
CONDITION (b): it holds across SAMPLED cells only. Unsampled players carry the pathway value itself, so
they reconcile trivially and receive no positional differentiation.

READ-ONLY, deterministic, no emits.
"""
import sys, json
sys.path.insert(0, '/home/user/afl-rl-engine/docs/evidence/composition_2026-08-10/noarb')
import harness_pvc_REPINNED_pass3 as H

SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
R = json.load(open(f"{SP}/per_entrant_SHIP.json"))['recs']
MINCELL = 20
POSN = ['MID', 'SD', 'SF', 'KPD', 'KPF', 'RUCK']
PATHWAYS = ['RD', 'SSP', 'MSD', 'IRE', 'PDA', 'PDN', 'PDS', 'UNR', 'ND>64']


def cohort(r):
    y = r.get('year')
    return None if y is None else (y if r.get('type') == 'MSD' else y + 1)


def stream(r):
    t = r.get('type')
    if t == 'ND' and r.get('pick') and 1 <= r['pick'] <= 64 and not r.get('is_pool'): return 'ND 1-64'
    if t == 'ND': return 'ND>64'
    return t


elig = [r for r in R if cohort(r) is not None and (r.get('v0') or 0) > 0]
rows, _ = H.structural_values(elig)
SV = {r['key']: row for r, row in zip(elig, rows)}
val = lambda sub: sum(SV[r['key']]['value'] for r in sub)
ent = lambda sub: sum(float(r['v0']) for r in sub)
ND = val([r for r in elig if stream(r) == 'ND 1-64']) / ent([r for r in elig if stream(r) == 'ND 1-64'])

print("=" * 112)
print("### THE RECONCILIATION TEST — layer 2 must aggregate to layer 1, per pathway")
print("=" * 112)
print(f"  ND 1-64 profile (the calibration target) = {ND:.6f}")
print(f"  a cell is SAMPLED at n >= {MINCELL}; unsampled players carry the pathway value itself")
print()
print(f"  {'pathway':8} {'n':>5} {'L1 pathway':>11} | {'RULE1 naive':>12} {'rel':>10} {'':>5} | "
      f"{'RULE2 residual':>14} {'rel':>10} {'':>5} | {'lam_rem':>9} {'n_rem':>6}")
print("  " + "-" * 108)
OUT = {}
for s in PATHWAYS:
    sub = [r for r in elig if stream(r) == s]
    if not sub: continue
    P1 = val(sub) / ent(sub) / ND
    cells = []
    for p in POSN:
        g = [r for r in sub if r.get('pos') == p]
        if len(g) >= MINCELL and ent(g) > 0:
            cells.append((p, len(g), ent(g), val(g) / ent(g) / ND))
    sampled = [r for r in sub if any(r.get('pos') == c[0] for c in cells)]
    unsampled = [r for r in sub if r not in sampled]
    # LAYER 2 as the build would set it: sampled cells get their own lambda; the rest carry P1.
    # RULE 1 (naive, and it BREAKS on partial pathways): unsampled players carry the pathway value.
    l2 = (sum(e * lam for _, _, e, lam in cells) + ent(unsampled) * P1) / ent(sub)
    rel = abs(l2 - P1) / P1 if P1 else 0.0
    # RULE 2 (the fix): the unsampled REMAINDER is priced as its OWN residual group.
    if unsampled and ent(unsampled) > 0:
        lamR = val(unsampled) / ent(unsampled) / ND
        l2f = (sum(e * lam for _, _, e, lam in cells) + ent(unsampled) * lamR) / ent(sub)
    else:
        lamR = float('nan'); l2f = sum(e * lam for _, _, e, lam in cells) / ent(sub)
    relf = abs(l2f - P1) / P1 if P1 else 0.0
    if cells:
        hc = (sum(n * lam for _, n, _, lam in cells) + len(unsampled) * P1) / len(sub)
        hcerr = abs(hc - P1) / P1
        hcs, hces = f"{hc:14.6f}", f"{100*hcerr:9.2f}%"
    else:
        hcs, hces = f"{'n/a':>14}", f"{'n/a':>10}"
    print(f"  {s:8} {len(sub):5} {P1:11.6f} {l2:13.6f} {rel:11.2e} {'PASS' if rel < 1e-9 else 'FAIL':>6} | "
          f"{l2f:13.6f} {relf:11.2e} {'PASS' if relf < 1e-9 else 'FAIL':>6} | {lamR:9.4f} {len(unsampled):6}")
    OUT[s] = {'n': len(sub), 'L1': P1, 'L2_rule1': l2, 'rel_rule1': rel,
              'L2_rule2': l2f, 'rel_rule2': relf, 'lam_remainder': lamR,
              'sampled_n': len(sampled), 'cells': {c[0]: {'n': c[1], 'lam': c[3]} for c in cells}}
print()
print("  RULE 1 = 'unsampled players carry the pathway value'. RULE 2 = 'the unsampled REMAINDER is")
print("  priced as its own residual group'. RULE 1 FAILS ON EVERY PARTIAL PATHWAY - see MSD, IRE, UNR,")
print("  ND>64 - because the remainder's own profile is not the pathway average, so the sampled cells'")
print("  deviation is left unoffset. RULE 2 reconciles everywhere at float noise. THE ACT MUST USE RULE 2.")
print()
print("  PASS at 1e-9 is the correct bar: this is an IDENTITY, not an approximation. A pathway's")
print("  profile IS the entry-weighted mean of its cell profiles, so layer 2 sums back to layer 1 by")
print("  construction. Anything above float noise means the build broke the construction.")
print()
print("  CONDITION (a) - THE WEIGHTING CONVENTION MUST MATCH, and here is the cost of getting it wrong:")
for s in PATHWAYS:
    if s in OUT and OUT[s]['cells']:
        sub = [r for r in elig if stream(r) == s]
        cells = [(p, d['n'], d['lam']) for p, d in OUT[s]['cells'].items()]
        hc = sum(n * lam for _, n, lam in cells) / sum(n for _, n, lam in cells)
        print(f"    {s:8} entry-weighted {OUT[s]['L1']:.4f}  vs  headcount-weighted {hc:.4f}"
              f"   -> {100*(hc/OUT[s]['L1']-1):+.1f}% error if the act mixed conventions")
print("  THE ACT ADOPTS ENTRY-WEIGHTING IN BOTH LAYERS. A headcount mean weights a 21-player cell the")
print("  same as a 176-player one and does not reconcile.")
json.dump(OUT, open('/home/user/afl-rl-engine/docs/evidence/pool_repricing_2026-08-11/RECONCILIATION.json', 'w'), indent=1)

print()
print("=" * 112)
print("### LAYER-2 STATUS PER PATHWAY (D4's decision surface — the seat does not choose)")
print("=" * 112)
print(f"  {'pathway':8} {'n':>5} " + "".join(f"{p:>6}" for p in POSN) + f" {'sampled':>8} {'status':>28}")
for s in PATHWAYS:
    sub = [r for r in elig if stream(r) == s]
    if not sub: continue
    cnt = {p: sum(1 for r in sub if r.get('pos') == p) for p in POSN}
    ok = [p for p in POSN if cnt[p] >= MINCELL]
    cov = sum(cnt[p] for p in ok)
    st = ('DERIVABLE (all cells)' if len(ok) == 6 else
          (f'PARTIAL ({len(ok)} of 6)' if ok else 'COLLAPSES TO LAYER 1'))
    print(f"  {s:8} {len(sub):5} " + "".join(f"{cnt[p]:6}" for p in POSN)
          + f" {cov:8} {st:>28}")
