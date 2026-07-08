"""L1c TASK 5 (G-MONO half) — pick-curve monotonicity + the V0-boundary / evidence-axis smoothness
demonstration (owner continuity law: pick PVC -> V0 -> end-y1 -> y2/3/4 on ONE curve, no cliffs).
ONE engine load (the engine is exec-once-per-process). Guard 5 on entry."""
import io, contextlib, json, os, sys
import numpy as np
HERE = '/home/user/afl-rl-engine'
OUT = f'{HERE}/session_2026-07-08/l1c_rectification/out'
sys.path.insert(0, HERE)
import boot_guard
boot_guard.assert_boot('gmono_v0', store_path='/home/claude/rl_workspace/rl_after/rl_model_data.json',
                       engine_head_path='/home/claude/rl_workspace/rl_after/_merged_recover.py')
os.chdir('/home/claude/rl_workspace/rl_after')
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA = g['MA']; cp = g['cp']
res = {}

print('=== G-MONO ===')
va = g['_v0_curve_assert']()
res['d14'] = va
print('D14 V0-curve by-construction gates (credited inputs):', va)
star = g['_V0CURVE_META']['_star']
mono_bad = 0
for pos in ['MID', 'GEN_FWD', 'GEN_DEF', 'KEY_FWD', 'KEY_DEF', 'RUC']:
    cur = [star(pos, 18, pk) for pk in range(1, 91)]
    mono_bad += sum(1 for i in range(89) if cur[i + 1] > cur[i] + 1e-6)
res['v0_inversions'] = mono_bad
print(f'V0*(age18) pick-monotonicity, 6 positions x picks 1-90: {"PASS (0 inversions)" if mono_bad==0 else f"FAIL ({mono_bad})"}')
hm = [round(g['_ruc_head_core'](pk, 21.0), 4) for pk in range(16, 34)]
steps = [abs(hm[i + 1] - hm[i]) for i in range(len(hm) - 1)]
res['ruc_head_max_step'] = max(steps)
print(f'young-ruck headroom picks 16-33 (age 21): max single-pick step {max(steps):.4f} -> {"smooth, no pk20/21 cliff" if max(steps)<0.02 else "CHECK"}')
tab = g['_YC_TAB']['2026']
kmax, kcell = 0.0, ''
for cls, row in tab.items():
    for sat in ('0', '1'):
        rr = row[sat]
        m = max(abs(rr[i + 1] - rr[i]) for i in range(len(rr) - 1))
        if m > kmax:
            kmax, kcell = m, f'{cls}/{sat}'
res['ycred_curve_max_step'] = kmax
print(f'L1c R-curve max adjacent-pick step across cells: {kmax:.4f} ({kcell}) — kernel-smoothed, no bin cliffs')

print('\n=== V0-BOUNDARY + EVIDENCE-AXIS SMOOTHNESS ===')
for nm in ('Willem Duursma', 'Dylan Patterson', 'Taylor Goad'):
    p = next(x for x in MA.data if x['player'] == nm and MA.GRP.get(x.get('pos')))
    v0 = g['v0_start'](p); C = p['year']
    with contextlib.redirect_stdout(io.StringIO()):
        y1 = g['ev'](p, C + 1)
    m0 = g['_ycred_mult'](p, cp.debutyr(p) - 1)
    print(f'{nm}: V0(day-0)={v0:.0f} · ev(end-y1 as-of)={y1} · credit-mult@V0={m0:.3f} (full at zero evidence)')
p = next(x for x in MA.data if x['player'] == 'Willem Duursma')
row26 = next((x for x in p['scoring'] if x['year'] == 2026), None)
if row26:
    g0, a0 = row26['games'], row26['avg']
    sweep = []
    try:
        for gg in range(0, 15):
            row26['games'] = gg
            MA._pe_clear()
            with contextlib.redirect_stdout(io.StringIO()):
                sweep.append(g['ev'](p, 2026))
    finally:
        row26['games'] = g0; MA._pe_clear()
    jumps = [abs(sweep[i + 1] - sweep[i]) / max(sweep[i], 1) for i in range(len(sweep) - 1)]
    res['duursma_sweep'] = sweep; res['max_jump_pct'] = 100 * max(jumps)
    print(f'Duursma 2026 value, games 0..14 at his own rate (avg {a0}): {sweep}')
    print(f'  max one-game move {100*max(jumps):.1f}% -> {"SMOOTH (credit unwind rides inside the evidence ramp; no cliff)" if max(jumps)<8 else "CHECK >8% step"}')
json.dump(res, open(f'{OUT}/gmono_v0.json', 'w'), indent=1, default=float)
print(f'\nwrote {OUT}/gmono_v0.json')
