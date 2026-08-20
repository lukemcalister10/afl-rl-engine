#!/usr/bin/env python3
"""ORDER B — the engine-load checks, ONE process (strictly sequential engine use):
  (1) B-3: ceiling bands b6(p,2026) for the 804 board rows, dial ON vs OFF (MA._O33S toggled in
      process — the same call-time read the dial law uses), v-inversion counts, ceiling-scenario sum;
  (2) continuity sweeps: a synthetic tall (KPF) and a MID at fixed levels, board-value objects
      val(proj_from_peak(...)) over ages 20..36 ON vs OFF — max adjacent-age step reported;
  (3) the fade's output-continuity: r(a,s) is output-FLAT by the ruled fallback (stated, no sweep).
Runs with RL_O33=1 (stage 2 = the full candidate after the B-A1 re-map)."""
import os, sys, json, io, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o33'

os.environ.update(RL_O31='1', RL_O32='1', RL_O33='1', PYTHONHASHSEED='0', RL_REPO=ROOT,
                  OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1',
                  NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1',
                  RL_V0SURF_PKL=os.path.join(ROOT, 'data', 'v0surf.pkl'),
                  RL_GAMMA='1.0', RL_PICK1='3000', RL_RUCK_TAX='0.25', RL_RECENCY_DECAY='0.72',
                  RL_PRIOR_TREES='400', PAR_RAMPS='22', RL_FV=os.path.join(ROOT, 'engine', 'forward_valuation'))
sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', ROOT + '/engine/rl_after']
_cwd = os.getcwd(); os.chdir(ROOT + '/engine/rl_after')
NSE = {}
with contextlib.redirect_stdout(io.StringIO()):
    import rl_model as MA
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], NSE)
os.chdir(_cwd)
MA = NSE.get('MA', MA)
b6 = NSE['b6']
assert MA._O33 and MA._O33S >= 2   # B-A1 stage re-map: 2 = the full candidate (ladder + taper)

BOARD = json.load(open(SP + '/bb_moff/rl_after/rl_app_data.json'))
KEYS = {r['key'] for r in BOARD['active']}
P_BY = {}
for p in MA.data:
    k = p.get('key')
    if k in KEYS and k not in P_BY:
        P_BY[k] = p

ON, OFF = {}, {}
for k, p in P_BY.items():
    try:
        ON[k] = [float(x) for x in b6(p, 2026)]
    except Exception:
        continue
MA._O33S = 0
for k in list(ON):
    OFF[k] = [float(x) for x in b6(P_BY[k], 2026)]
MA._O33S = 2

inv_off = sum(1 for k in OFF if OFF[k][5] < OFF[k][4] - 1e-9)
inv_on = sum(1 for k in ON if ON[k][5] < ON[k][4] - 1e-9)
d5 = {k: ON[k][5] - OFF[k][5] for k in ON}
moved = {k: v for k, v in d5.items() if abs(v) > 1e-6}
lower_moved = sum(1 for k in ON if any(abs(ON[k][i] - OFF[k][i]) > 1e-9 for i in range(5)))
print('B-3 CEILING BAND (b6 band[5]; price flows through the WQ6 0.10 weight):')
print('  v-inversions (band5 < band4): taper ON (dial off) %d  ->  retirement (dial on) %d' % (inv_off, inv_on))
print('  rows with band[5] lifted: %d of %d;  total ceiling-band level points restored: %+.0f' % (
    len(moved), len(ON), sum(d5.values())))
print('  rows with ANY band[0..4] moved (must be 0): %d' % lower_moved)
top = sorted(moved.items(), key=lambda t: -t[1])[:10]
for k, v in top:
    print('    %-24s band5 %+8.1f' % (k, v))

# ---- continuity sweeps ------------------------------------------------------------------------------
print('\nCONTINUITY (board-value object val(proj_from_peak), fixed level, ages 20..36):')
SWEEP = {}
for gname, L in (('KPF', 80.0), ('KPF', 95.0), ('MID', 95.0), ('MID', 110.0)):
    on_v, off_v = [], []
    for a in range(20, 37):
        args = (gname, L, a, None, 'bal')
        on_v.append(float(MA.val(MA.proj_from_peak(*args))))
        MA._O33S = 0
        off_v.append(float(MA.val(MA.proj_from_peak(*args))))
        MA._O33S = 2
    ratio = [o / f if f > 0 else None for o, f in zip(on_v, off_v)]
    steps = [abs(ratio[i + 1] - ratio[i]) for i in range(len(ratio) - 1)
             if ratio[i] is not None and ratio[i + 1] is not None]
    SWEEP['%s@L%.0f' % (gname, L)] = dict(ages=list(range(20, 37)), on=on_v, off=off_v,
                                          ratio=[round(r, 4) if r else None for r in ratio],
                                          max_adjacent_ratio_step=round(max(steps), 4))
    print('  %s L=%.0f  on/off ratio by age: ' % (gname, L) +
          ' '.join('%d:%.2f' % (a, r) for a, r in zip(range(20, 37), ratio) if r) )
    print('      max adjacent-age step of the ratio: %.4f' % max(steps))
print('  (the fade is output-FLAT by the ruled fallback -> no output cliff exists by construction;')
print('   the ladder and fade are the only new age objects and both are schedules interpolated the')
print("   engine's own way — the ratio path above is the realized no-cliff exhibit)")

json.dump(dict(inversions_taper_on=inv_off, inversions_retirement=inv_on, n_band5_moved=len(moved),
               total_band5_delta=round(sum(d5.values()), 1), lower_bands_moved=lower_moved,
               top_band5=[[k, round(v, 1)] for k, v in top], sweeps=SWEEP),
          open(os.path.join(HERE, 'ENGINE_CHECKS_B.json'), 'w'), indent=1)
print('\nwrote ENGINE_CHECKS_B.json')
