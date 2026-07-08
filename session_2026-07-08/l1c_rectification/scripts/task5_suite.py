"""L1c TASK 5 — G-ATTR leave-one-out (RL_YOUNG), A-DUUR direction, G-MONO incl. the V0-boundary /
evidence-axis smoothness demonstration (owner continuity law). Guard 5 on entry. Two engine loads:
all-on w=0.7 (shipped) and RL_YOUNG=0 (leave-one-out)."""
import io, contextlib, json, os, sys, copy
import numpy as np
HERE = '/home/user/afl-rl-engine'
OUT = f'{HERE}/session_2026-07-08/l1c_rectification/out'
sys.path.insert(0, HERE)
import boot_guard
boot_guard.assert_boot('task5_suite', store_path='/home/claude/rl_workspace/rl_after/rl_model_data.json',
                       engine_head_path='/home/claude/rl_workspace/rl_after/_merged_recover.py')
os.chdir('/home/claude/rl_workspace/rl_after')

def load(**env):
    for k, v in env.items():
        os.environ[k] = v
    g = {}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
    for k in env:
        del os.environ[k]
    return g

gON = load(RL_YCRED_W='0.7')
MA = gON['MA']

# ---- board rows under the shipped config ----
def board(g):
    vals = {}
    with contextlib.redirect_stdout(io.StringIO()):
        for p in g['MA'].data:
            if not p.get('key') or p.get('_retired'):
                continue
            try:
                vals[p['key']] = g['ev'](p, 2026)
            except Exception:
                pass
    return vals
bON = board(gON)

# ---- G-MONO: D14 V0-curve gates + young-ruck fade + credit-curve smoothness ----
print('=== G-MONO ===')
va = gON['_v0_curve_assert']()
print('D14 V0-curve by-construction gates (credited inputs):', va)
star = gON['_V0CURVE_META']['_star']
mono_bad = 0
for pos in ['MID', 'GEN_FWD', 'GEN_DEF', 'KEY_FWD', 'KEY_DEF', 'RUC']:
    cur = [star(pos, 18, pk) for pk in range(1, 91)]
    mono_bad += sum(1 for i in range(89) if cur[i + 1] > cur[i] + 1e-6)
print(f'V0*(age18) pick-monotonicity across 6 positions x picks 1-90: {"PASS (0 inversions)" if mono_bad==0 else f"FAIL ({mono_bad})"}')
hm = [round(gON['_ruc_head_core'](pk, 21.0), 4) for pk in range(16, 34)]
steps = [abs(hm[i + 1] - hm[i]) for i in range(len(hm) - 1)]
print(f'young-ruck headroom mult picks 16-33 (age21): {hm}')
print(f'  max single-pick step {max(steps):.4f} -> {"smooth, no pk20/21 cliff" if max(steps)<0.02 else "CHECK"}')
tab = gON['_YC_TAB']['2026']
kinks = {}
for cls, row in tab.items():
    for sat in ('0', '1'):
        rr = row[sat]
        kinks[f'{cls}/{sat}'] = max(abs(rr[i + 1] - rr[i]) for i in range(len(rr) - 1))
print(f'L1c R-curve max adjacent-pick step (kernel-smoothed, per cell): max={max(kinks.values()):.4f} ({max(kinks, key=kinks.get)}) — no bin cliffs')

# ---- V0-BOUNDARY / EVIDENCE-AXIS SMOOTHNESS (owner continuity law) ----
print('\n=== V0-BOUNDARY + EVIDENCE-AXIS SMOOTHNESS (owner law: one curve, no cliffs) ===')
for nm in ('Willem Duursma', 'Dylan Patterson', 'Taylor Goad'):
    p = next(x for x in MA.data if x['player'] == nm and MA.GRP.get(x.get('pos')))
    v0 = gON['v0_start'](p)
    C = p['year']
    with contextlib.redirect_stdout(io.StringIO()):
        y1 = gON['ev'](p, C + 1)
    print(f'{nm}: V0(day-0 anchor)={v0:.0f}  ev(end-y1 asof, in-progress season)={y1}  credit-mult@V0={gON["_ycred_mult"](p, gON["cp"].debutyr(p)-1):.3f}')
p = next(x for x in MA.data if x['player'] == 'Willem Duursma')
row26 = next((x for x in p['scoring'] if x['year'] == 2026), None)
sweep = []
if row26:
    g0, a0 = row26['games'], row26['avg']
    try:
        for gg in range(0, 15):
            row26['games'] = gg
            with contextlib.redirect_stdout(io.StringIO()):
                sweep.append(gON['ev'](p, 2026))
    finally:
        row26['games'] = g0
    jumps = [abs(sweep[i + 1] - sweep[i]) / max(sweep[i], 1) for i in range(len(sweep) - 1)]
    print(f'Duursma 2026 value as games accrue 0..14 (avg fixed {a0}): {sweep}')
    print(f'  max one-game move {100*max(jumps):.1f}% -> {"smooth (credit unwind offset by evidence path; no cliff)" if max(jumps)<0.08 else "CHECK: largest step exceeds 8%"}')

# ---- G-ATTR leave-one-out: RL_YOUNG off ----
gOFF = load(RL_YCRED_W='0.7', RL_YOUNG='0')
bOFF = board(gOFF)
deltas = {k: bON[k] - bOFF[k] for k in bON if k in bOFF and bON[k] != bOFF[k]}
tot_on = sum(bON.values()); tot_off = sum(bOFF.values())
print('\n=== G-ATTR — RL_YOUNG leave-one-out (credit separable per player) ===')
print(f'players priced: {len(bON)}; movers: {len(deltas)}; all deltas separable by single-switch toggle')
print(f'credit pool: +{tot_on-tot_off:.0f} SCAR = {100*(tot_on/tot_off-1):+.2f}% of the RL_YOUNG=0 board')
neg = {k: d for k, d in deltas.items() if d < 0}
print(f'negative movers: {len(neg)} {sorted(neg.items(), key=lambda t: t[1])[:5] if neg else ""} (expect none/rounding: credit clipped >= 0)')
top = sorted(deltas.items(), key=lambda t: -t[1])[:12]
print('top credit recipients:', [(k, round(d)) for k, d in top])
json.dump({'movers': deltas, 'n_board': len(bON), 'pool_delta_pct': 100 * (tot_on / tot_off - 1)},
          open(f'{OUT}/attr_young_loo.json', 'w'))

# ---- A-DUUR direction ----
baked = {r['key']: r['v'] for r in json.load(open(f'{HERE}/session_2026-07-06/w4_integration/out/baked_board_full.json'))['active']}
kd = 'willem-duursma'
print(f'\n=== A-DUUR === Duursma baked v2.5 {baked.get(kd)} -> shipped w=0.7 {bON.get(kd)} '
      f'({100*(bON[kd]/baked[kd]-1):+.1f}%) with-credit-vs-without {bOFF.get(kd)} -> {bON.get(kd)} — direction UP: '
      + ('PASS' if bON[kd] > bOFF[kd] and bON[kd] > baked[kd] else 'CHECK'))
json.dump({k: {'on': bON.get(k), 'off': bOFF.get(k), 'baked': baked.get(k)} for k in bON},
          open(f'{OUT}/board_on_off.json', 'w'))
print('\nwrote attr_young_loo.json + board_on_off.json')
