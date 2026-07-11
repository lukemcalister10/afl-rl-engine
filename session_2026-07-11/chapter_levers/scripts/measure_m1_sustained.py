"""L2 — SUSTAINED-FORM WEIGHTING: measure the pattern population + derive the corrected persistence
fraction from realized outcomes. READ-ONLY measurement (the implement/stop decision rides the result).

OWNER READS (canonical, directive 2026-07-11): kysaiah-pickett — GFWD averaging 90-95 two straight
seasons, priced significantly lower because of 3 years ago ("that's silly"); bailey-smith the same
pattern. MECHANISM UNDER TEST: the M1 up-branch (engine _merged_recover.py:225) credits a proven
riser S_M1=0.46 of his current-over-baseline gap (Lc-Lo) UNCONDITIONED on persistence — a
two-straight-season demonstrated level is haircut the same 46% as a one-year spike (pickett trace,
branch claude/pickett-form-history-trace-8ov1uv: LEVEL not bug, calibration gap = no
consecutive-year persistence conditioning).

MEASUREMENT (the committed _m1_refine methodology, stratified):
  points: every (player, Y) with n_qual >= PROVEN_N, M1-fire condition as the engine applies it
          ((Lc-Lo) >= TOL_M1 AND _radq), and a realized forward window — rf = games-weighted avg of
          seasons Y+1..Y+3 with games >= 10. LEAK-FREE: primary fit uses Y <= 2022 (fully completed
          3-season forward windows; the 2026 in-progress season never enters a fit target);
          Y <= 2024 variant reported as sensitivity.
  strata: SUST2 = seasons Y and Y-1 BOTH games >= G_ADQ(12) and BOTH avg > Lo  (the owner's
          "two straight seasons" pattern, applied exactly as the engine could at year Y);
          OTHER  = fire-condition points not SUST2 (single-season risers).
  fit:    s = sum((Lc-Lo)(rf-Lo)) / sum((Lc-Lo)^2)  per stratum (the committed formula), with
          1000-resample bootstrap percentile CIs. VERDICT RULE (declared before looking): implement a
          persistence-conditioned S only if s_SUST2 exceeds the shipped 0.46 by a margin the bootstrap
          supports (SUST2 CI 5th percentile > 0.46) — otherwise commit the numbers and STOP.
Also measured: the pattern POPULATION on today's board (proven players whose SUST2 level exceeds
their priced level), with kysaiah-pickett + bailey-smith named.
"""
import io, contextlib, json, sys
import numpy as np

HERE = '/home/user/afl-rl-engine'
sys.path.insert(0, HERE)
import boot_guard
boot_guard.assert_boot('measure_m1_sustained', store_path=f'{HERE}/engine/rl_after/rl_model_data.json')

np.random.seed(0)
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA = g['MA']; cp = g['cp']
_lvlcurr = g['_lvlcurr']; _nqual = g['_nqual']; _radq = g['_radq']
PROVEN_N = g['PROVEN_N']; TOL_M1 = g['TOL_M1']; G_ADQ = g['G_ADQ']; S_M1 = g['S_M1']
G_EVAL = 10

def seasons(p):
    return [(x['year'], x['games'], x['avg']) for x in p['scoring'] if x['games'] > 0 and (cp.debutyr(p) - 1) < x['year']]

def realized(p, Y):
    fwd = [(y, gm, a) for (y, gm, a) in seasons(p) if Y < y <= Y + 3 and gm >= G_EVAL]
    if not fwd: return None
    return sum(gm * a for _, gm, a in fwd) / sum(gm for _, gm, a in fwd)

def sust2(p, Y, Lo):
    """seasons Y and Y-1 both >= G_ADQ games and both avg > Lo — evaluable at year Y (leak-free)."""
    ss = {y: (gm, a) for (y, gm, a) in seasons(p)}
    return all(y in ss and ss[y][0] >= G_ADQ and ss[y][1] > Lo for y in (Y, Y - 1))

pts = []
for p in MA.data:
    if not (p.get('pick') or p.get('_ft')): continue
    ys = [y for y, _, _ in seasons(p)]
    if not ys: continue
    for Y in range(min(ys), 2025):
        if _nqual(p, Y) < PROVEN_N: continue
        Lo = cp._lvl_eff_orig(p, Y); Lc = _lvlcurr(p, Y)
        if not ((Lc - Lo) >= TOL_M1 and _radq(p, Y, Lo)): continue   # the engine's own fire condition
        rf = realized(p, Y)
        if rf is None: continue
        pts.append(dict(nm=p.get('key') or p['player'], Y=Y, Lo=Lo, Lc=Lc, rf=rf, sust=sust2(p, Y, Lo)))

def fit(rs):
    Lo = np.array([q['Lo'] for q in rs]); Lc = np.array([q['Lc'] for q in rs]); rf = np.array([q['rf'] for q in rs])
    return float(np.sum((Lc - Lo) * (rf - Lo)) / np.sum((Lc - Lo) ** 2))

def boot(rs, n=1000):
    idx = np.arange(len(rs)); out = []
    for _ in range(n):
        smp = [rs[i] for i in np.random.choice(idx, len(rs))]
        out.append(fit(smp))
    return float(np.percentile(out, 5)), float(np.percentile(out, 50)), float(np.percentile(out, 95))

res = {'S_M1_shipped': S_M1, 'fire_condition': f'(Lc-Lo)>={TOL_M1} & _radq', 'strata': {}}
print(f'M1-fire points with realized forward: {len(pts)} (S_M1 shipped = {S_M1})')
for tag, cut in (('PRIMARY_Y<=2022', lambda q: q['Y'] <= 2022), ('SENS_Y<=2024', lambda q: True)):
    sub = [q for q in pts if cut(q)]
    for lab, sel in (('SUST2', lambda q: q['sust']), ('OTHER', lambda q: not q['sust']), ('ALL', lambda q: True)):
        rs = [q for q in sub if sel(q)]
        if len(rs) < 8:
            print(f'  {tag} {lab}: n={len(rs)} TOO THIN'); continue
        s = fit(rs); lo5, med, hi95 = boot(rs)
        res['strata'][f'{tag}/{lab}'] = dict(n=len(rs), s=round(s, 3), boot_p5=round(lo5, 3), boot_p50=round(med, 3), boot_p95=round(hi95, 3),
                                             mean_gap=round(float(np.mean([q['Lc'] - q['Lo'] for q in rs])), 2),
                                             mean_rf_minus_Lo=round(float(np.mean([q['rf'] - q['Lo'] for q in rs])), 2))
        print(f"  {tag} {lab:6s} n={len(rs):4d}  s={s:.3f}  boot[p5,p50,p95]=[{lo5:.3f},{med:.3f},{hi95:.3f}]  "
              f"mean(Lc-Lo)={np.mean([q['Lc']-q['Lo'] for q in rs]):.2f}  mean(rf-Lo)={np.mean([q['rf']-q['Lo'] for q in rs]):.2f}")

prim = res['strata'].get('PRIMARY_Y<=2022/SUST2')
verdict = bool(prim and prim['boot_p5'] > S_M1)
res['verdict'] = ('IMPLEMENT: s_SUST2 bootstrap p5 %.3f > shipped %.2f' % (prim['boot_p5'], S_M1)) if verdict else \
                 ('STOP: the data does not support a stronger sustained weighting at bootstrap confidence '
                  '(SUST2 p5 %s vs shipped %.2f)' % (prim and prim['boot_p5'], S_M1))
print('\nVERDICT:', res['verdict'])

# --- the pattern population on today's board (Y=2026, engine's own fire test) ---
pop = []
for p in MA.data:
    if not (p.get('pick') or p.get('_ft')): continue
    if _nqual(p, 2026) < PROVEN_N: continue
    Lo = cp._lvl_eff_orig(p, 2026); Lc = _lvlcurr(p, 2026)
    if (Lc - Lo) >= TOL_M1 and _radq(p, 2026, Lo) and sust2(p, 2026, Lo):
        pop.append(dict(key=p.get('key') or p['player'], Lo=round(Lo, 1), Lc=round(Lc, 1), gap=round(Lc - Lo, 1),
                        haircut_now=round((1 - S_M1) * (Lc - Lo), 1)))
pop.sort(key=lambda d: -d['gap'])
res['population_2026_SUST2'] = pop
print(f'\nSUST2 population on today\'s board (proven, fire-condition, 2-straight seasons above Lo): {len(pop)}')
for d in pop[:25]:
    print(f"  {d['key']:26s} Lo={d['Lo']:6.1f} Lc={d['Lc']:6.1f} gap={d['gap']:5.1f}  level held back now={d['haircut_now']:5.1f}")
json.dump(res, open(f'{HERE}/session_2026-07-11/chapter_levers/out/m1_sustained_measurement.json', 'w'), indent=1)
print(f"\nwrote {HERE}/session_2026-07-11/chapter_levers/out/m1_sustained_measurement.json")
