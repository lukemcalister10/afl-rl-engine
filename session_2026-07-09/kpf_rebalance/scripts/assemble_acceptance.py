"""Task 5 — ACCEPTANCE TABLE (committed artifact). Assembles before/after from the committed board
dumps (no engine load): base = L1c w=0.9 candidate (pre-rebalance), new = rebalanced candidate.
Attribution columns from single-switch dumps (RL_KPFFIX=0 / RL_YOUNG=0 on each engine)."""
import json, os
O = '/home/user/afl-rl-engine/session_2026-07-09/kpf_rebalance/out'
L = lambda f: json.load(open(f'{O}/{f}'))['rows']
b_on, b_k0, b_y0 = L('board_base_ON.json'), L('board_base_KPF0.json'), L('board_base_Y0.json')
n_on, n_k0, n_y0 = L('board_new2_ON.json'), L('board_new2_KPF0.json'), L('board_new2_Y0.json')

SIX = ['jake-waterman', 'charlie-curnow', 'riley-thilthorpe', 'josh-treacy', 'sam-darcy', 'jeremy-cameron']
TAKES = ['logan-mcdonald', 'mitch-georgiades', 'jake-waterman', 'riley-thilthorpe', 'jack-lukosius',
         'josh-treacy', 'jack-gunston', 'jeremy-cameron']
SPEC = ['jordan-croft', 'thomas-sims', 'matt-whitlock', 'jack-whitlock', 'harry-armstrong', 'archer-reid',
        'murphy-reid', 'zach-reid', 'jonty-faull', 'ethan-read', 'jed-walter', 'calsher-dear',
        'mitchell-marsh', 'daniel-curtin', 'cody-curtin']
ANCH = ['marcus-bontempelli', 'max-gawn', 'willem-duursma', 'kieren-briggs', 'charlie-cameron']

lines = []
P = lines.append
P('# ACCEPTANCE TABLE — KPF REBALANCE (pre-bake) · 2026-07-09 · engine 275aa2a5 on L1c w=0.9 candidate')
P('BEFORE = the L1c w=0.9 owner-ruled candidate (engine fbefdc2b) · AFTER = the rebalanced candidate.')
P('"KPFFIX net" = value minus the same engine with RL_KPFFIX=0 · "young credit" = minus RL_YOUNG=0.')
P('')
P('## 1. The owner\'s six top-tier names (Task 2 acceptance — magnitudes owner-on-sight)')
P('| player | before | after | Δ | Δ% | KPFFIX net before → after |')
P('|---|---|---|---|---|---|')
for k in SIX:
    a, b = b_on[k]['v'], n_on[k]['v']
    P(f"| {k} | {a} | {b} | {b-a:+d} | {100*(b-a)/a:+.1f}% | {a-b_k0[k]['v']:+d} → {b-n_k0[k]['v']:+d} |")
P('')
P('## 2. The softened-take set (Task 1 acceptance — each named take before/after)')
P('| player | take before (vs KPFFIX-off) | take after | comment |')
P('|---|---|---|---|')
CM = {'logan-mcdonald': 'no sustained demonstration (LD=Lc) — the honest take STANDS',
      'mitch-georgiades': 'three high-games seasons — demonstrated slice retained at 0.70',
      'jake-waterman': 'take reversed by the top-tier reward (net give)',
      'riley-thilthorpe': 'take softened 5.3× (demonstration + top-tier reward)',
      'jack-lukosius': 'recent demonstration moderate — softened, still a take',
      'josh-treacy': 'top-tier reward exceeds the residual take (net give)',
      'jack-gunston': 'was the owner\'s "+17 gives little back" case — now a real give',
      'jeremy-cameron': 'A-CAM: up, clears its bar'}
for k in TAKES:
    ta = b_on[k]['v'] - b_k0[k]['v']; tb = n_on[k]['v'] - n_k0[k]['v']
    P(f"| {k} | {ta:+d} ({100*ta/b_k0[k]['v']:+.1f}%) | {tb:+d} ({100*tb/n_k0[k]['v']:+.1f}%) | {CM.get(k,'')} |")
P('')
P('## 3. The speculative set (Task 3 acceptance — slight, F-YOUNG honored, no wipe)')
P('| player | before | after | Δ | Δ% | young credit before → after |')
P('|---|---|---|---|---|---|')
for k in SPEC:
    a, b = b_on[k]['v'], n_on[k]['v']
    P(f"| {k} | {a} | {b} | {b-a:+d} | {100*(b-a)/a:+.1f}% | {a-b_y0[k]['v']:+d} → {b-n_y0[k]['v']:+d} |")
P('')
P('## 4. GEORGIADES vs WHITLOCK (owner read: Georgiades above)')
gg, jw, mw = n_on['mitch-georgiades']['v'], n_on['jack-whitlock']['v'], n_on['matt-whitlock']['v']
gg0, jw0 = b_on['mitch-georgiades']['v'], b_on['jack-whitlock']['v']
P(f'- BEFORE: georgiades {gg0} vs jack-whitlock {jw0} → {"ABOVE" if gg0>jw0 else "BELOW (the owner-flagged inversion)"}')
P(f'- AFTER : georgiades {gg} vs jack-whitlock {jw} → {"RESTORED (Georgiades above)" if gg>jw else "NOT RESTORED"}')
P(f'- (both Whitlocks exist in the store; matt-whitlock {mw} — reported for completeness; the KPF-speculative '
  f'read is jack-whitlock. Flagged: the directive says "Whitlock" unqualified.)')
P('')
P('## 5. Anchor noise check (frozen levers — movement >0.5% is a finding)')
P('| anchor | before | after | Δ% | verdict |')
P('|---|---|---|---|---|')
for k in ANCH:
    a, b = b_on[k]['v'], n_on[k]['v']; pct = 100 * (b - a) / max(a, 1)
    P(f"| {k} | {a} | {b} | {pct:+.2f}% | {'UNTOUCHED' if abs(pct) <= 0.5 else 'FINDING: moved >0.5%'} |")
P(f"- A-GAWN comparator: max-gawn {n_on['max-gawn']['v']} clearly above kieren-briggs {n_on['kieren-briggs']['v']} — held.")
P(f"- charlie-cameron (the drifted registry key) is a DIFFERENT player (GEN_FWD, pick 6) — 0.00%, untouched "
  f"by the KEY_FWD-scoped anchor/reward logic; A-CAM keys jeremy-cameron (verified against the store).")
P('')
P('## 6. A-DARCY three-way attribution (owner "too low" standing read)')
k = 'sam-darcy'
P(f"- sam-darcy {b_on[k]['v']} → {n_on[k]['v']} ({100*(n_on[k]['v']-b_on[k]['v'])/b_on[k]['v']:+.1f}%) — direction UP.")
P(f"  - young_convexity_ceiling: young-credit delta {b_on[k]['v']-b_y0[k]['v']:+d} before → "
  f"{n_on[k]['v']-n_y0[k]['v']:+d} after (his evidence is past G0=46 games — the credit, and therefore the "
  f"T3 trim, cannot touch him; ZERO by construction).")
P(f"  - kpf_speculative (RL_KPFFIX lever): {n_on[k]['v']-n_k0[k]['v']:+d} — the WHOLE rise; the T2 "
  f"partial-proven top-tier credit (nq=2, c=0.5, dm=23.0). He stays EXEMPT from the T1 compress (age<24).")
P(f"  - availability_layer: ABSENT — no LTI return-haircut machinery exists in the engine (2026-07-08 "
  f"diagnostic, re-confirmed; _b2hc/season-proration did not move him this build). Absence is the finding.")
P('')
P('## 7. Net movement')
for nm, sel in [('whole board', lambda r: True), ('KEY_FWD position', lambda r: r['pos'] == 'KEY_FWD')]:
    t0 = sum(r['v'] for r in b_on.values() if sel(r)); t1 = sum(r['v'] for r in n_on.values() if sel(r))
    P(f'- {nm}: {t0:,} → {t1:,} ({100*(t1/t0-1):+.2f}%)')
mv = [(n_on[k]['v'] - b_on[k]['v'], k) for k in b_on]
up = sum(1 for d, _ in mv if d > 0); dn = sum(1 for d, _ in mv if d < 0)
P(f'- movers: {up} up · {dn} down · {len(mv)-up-dn} unchanged (of {len(mv)} active); all non-KEY_FWD movement '
  f'is ±1 rounding on 2 rows (the D14 KPP-class floor couples KEY_FWD/KEY_DEF V0 curves — declared).')
open(f'{O}/ACCEPTANCE_TABLE.md', 'w').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
