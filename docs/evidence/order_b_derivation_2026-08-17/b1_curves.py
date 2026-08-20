#!/usr/bin/env python3
# =====================================================================================================
# ORDER B DERIVATION -- b1: position decline curves FITTED from realized production (PREREG_B.md §1).
# Read-only. Cohort construction reused from W5 (w5_veteran_mark.py); pair estimator per prereg.
# =====================================================================================================
import json, math, os, hashlib, collections
import numpy as np

SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
HERE = os.path.dirname(os.path.abspath(__file__))
CAND_P = SP + '/per_entrant_O31FFINAL.json'

SEED = 34
B_BOOT = 2000
FM = {'paddy-mccartin', 'thomas-boyd'}
POSG = {'KPD': 'TALL', 'KPF': 'TALL', 'MID': 'SMALL', 'SD': 'SMALL', 'SF': 'SMALL', 'RUCK': 'RUCK'}
GROUPS = ['TALL', 'RUCK', 'SMALL', 'KPD', 'KPF']   # KPD/KPF split = check only
LAST_REAL_SEASON = 2025
ENTRY_FLOOR = 2005
AGE_LO, AGE_HI = 21, 33          # pair earlier-age range
NMIN = 20                        # fat-cell threshold (prereg thin-cell rule)


def md5f(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()


m5 = md5f(CAND_P)
assert m5.startswith('d97f1aee'), 'HALT: input md5 mismatch ' + m5
A = json.load(open(CAND_P))
recs = A['recs']
print('input md5 %s recs %d' % (m5[:8], len(recs)))


def arm_of(r):
    if r.get('teaches_curve') and r['type'] == 'ND':
        return 'ND'
    if r.get('is_pool'):
        t = r['type']
        if t == 'RD':
            return 'RD'
        if t == 'MSD':
            return 'MSD'
        return 'OTHERPOOL'
    return None


# ---- build within-player consecutive-season pairs ---------------------------------------------------
pairs = []           # dict(key, a, grp, grp2, L0, L1, g0, g1, w, switch)
n_switch = collections.Counter()
for r in recs:
    k = r['key']
    if k in FM or arm_of(r) is None or r['year'] < ENTRY_FLOOR:
        continue
    seas = {}
    for s in r['seasons']:
        if s['year'] > LAST_REAL_SEASON:
            continue
        if s.get('bar') not in POSG or s['games'] < 4:
            continue
        seas[s['year']] = s
    for t in sorted(seas):
        if (t + 1) not in seas:
            continue
        s0, s1 = seas[t], seas[t + 1]
        a = r['age_draft'] + (t - r['year'])
        if not (AGE_LO <= a <= AGE_HI):
            continue
        g0, g1 = POSG[s0['bar']], POSG[s1['bar']]
        if g0 != g1:
            n_switch[g0] += 1
            continue
        pairs.append(dict(key=k, a=a, grp=g0, bar=s0['bar'], L0=s0['avg'], L1=s1['avg'],
                          w=min(s0['games'], s1['games'], 22)))

print('pairs %d  group-switch excluded %s' % (len(pairs), dict(n_switch)))

by_grp_age = collections.defaultdict(list)
for p in pairs:
    by_grp_age[(p['grp'], p['a'])].append(p)
    if p['bar'] in ('KPD', 'KPF'):
        by_grp_age[(p['bar'], p['a'])].append(p)

players = sorted({p['key'] for p in pairs})
pl_index = {k: i for i, k in enumerate(players)}
by_player = collections.defaultdict(list)
for p in pairs:
    by_player[p['key']].append(p)

RNG = np.random.default_rng(SEED)
boot_draws = [RNG.integers(0, len(players), size=len(players)) for _ in range(B_BOOT)]


def _match(p, grp):
    return (p['bar'] == grp) if grp in ('KPD', 'KPF') else (p['grp'] == grp)


def ratios_from(sel_pairs, grp):
    """age -> weighted-mean ratio for one (sub)sample of pairs."""
    agg = collections.defaultdict(lambda: [0.0, 0.0])
    for p in sel_pairs:
        if not _match(p, grp):
            continue
        acc = agg[p['a']]
        acc[0] += p['w'] * (p['L1'] / p['L0'])
        acc[1] += p['w']
    return {a: (v[0] / v[1] if v[1] > 0 else np.nan) for a, v in agg.items()}


OUT = dict(meta=dict(prereg='PREREG_B.md (pushed first)', input=dict(path=CAND_P, md5=m5),
                     seed=SEED, B_boot=B_BOOT, nmin=NMIN, pairs=len(pairs),
                     group_switch_excluded=dict(n_switch)),
           groups={})

for grp in GROUPS:
    cells = {a: by_grp_age.get((grp, a), []) for a in range(AGE_LO, AGE_HI + 1)}
    ns = {a: len(c) for a, c in cells.items()}
    point = ratios_from(pairs, grp)
    # bootstrap: cluster by player
    boots = {a: [] for a in range(AGE_LO, AGE_HI + 1)}
    for bp in boot_draws:
        sel = []
        for i in bp:
            sel.extend(by_player[players[i]])
        rr = ratios_from(sel, grp)
        for a in boots:
            boots[a].append(rr.get(a, np.nan))
    steps = {}
    for a in range(AGE_LO, AGE_HI + 1):
        n = ns.get(a, 0)
        if n == 0:
            continue
        bs = np.array(boots[a], dtype=float)
        ok = np.isfinite(bs)
        lo, hi = (np.nanpercentile(bs[ok], [5, 95]) if ok.sum() > 100 else (np.nan, np.nan))
        # raw envelope for thin cells (bound, never smoothed)
        env = [min(p['L1'] / p['L0'] for p in cells[a]), max(p['L1'] / p['L0'] for p in cells[a])] if n else None
        steps[a] = dict(n=n, ratio=round(float(point.get(a, np.nan)), 4),
                        ci=[round(float(lo), 4), round(float(hi), 4)],
                        thin=(n < NMIN), envelope=[round(env[0], 3), round(env[1], 3)])
    # chained curve on fat cells only, F(24)=1
    fat_ages = [a for a in sorted(steps) if not steps[a]['thin']]
    F = {24: 1.0}
    for a in range(24, AGE_HI + 1):
        if a in fat_ages and a in F:
            F[a + 1] = F[a] * steps[a]['ratio']
        else:
            break
    for a in range(23, AGE_LO - 1, -1):
        if a in fat_ages and (a + 1) in F:
            F[a] = F[a + 1] / steps[a]['ratio']
        else:
            break
    # bootstrap the chained curve
    Fboot = {a: [] for a in F}
    for bi in range(B_BOOT):
        Fb = {24: 1.0}
        ok = True
        for a in range(24, AGE_HI + 1):
            if a in fat_ages and a in Fb and np.isfinite(boots[a][bi]):
                Fb[a + 1] = Fb[a] * boots[a][bi]
            else:
                break
        for a in range(23, AGE_LO - 1, -1):
            if a in fat_ages and (a + 1) in Fb and np.isfinite(boots[a][bi]):
                Fb[a] = Fb[a + 1] / boots[a][bi]
            else:
                break
        for a in Fboot:
            Fboot[a].append(Fb.get(a, np.nan))
    curve = {}
    for a in sorted(F):
        bs = np.array(Fboot[a], dtype=float)
        fin = np.isfinite(bs)
        lo, hi = (np.nanpercentile(bs[fin], [5, 95]) if fin.sum() > 100 else (np.nan, np.nan))
        curve[a] = dict(F=round(F[a], 4), ci=[round(float(lo), 4), round(float(hi), 4)])
    # fitted peak age = argmax F (fat range only), and post-peak deltas
    pa_fit = max(F, key=lambda a: F[a])
    # peak-age CI: argmax per bootstrap
    pa_bs = []
    for bi in range(B_BOOT):
        d = {a: Fboot[a][bi] for a in Fboot if np.isfinite(Fboot[a][bi])}
        if d:
            pa_bs.append(max(d, key=lambda a: d[a]))
    pa_ci = [int(np.percentile(pa_bs, 5)), int(np.percentile(pa_bs, 95))] if pa_bs else None
    deltas = {}
    for a in sorted(F):
        j = a - pa_fit
        if j >= 0:
            bs = np.array(Fboot[a], dtype=float) / np.array(Fboot[pa_fit], dtype=float)
            fin = np.isfinite(bs)
            lo, hi = (np.nanpercentile(bs[fin], [5, 95]) if fin.sum() > 100 else (np.nan, np.nan))
            deltas[j] = dict(age=a, d=round(F[a] / F[pa_fit], 4),
                             ci=[round(float(lo), 4), round(float(hi), 4)])
    # tail rule: last fat annual decline rate held flat (never shallower)
    last_fat = max(fat_ages) if fat_ages else None
    tail_rate = steps[last_fat]['ratio'] if last_fat else None
    OUT['groups'][grp] = dict(steps=steps, curve=curve, peak_age_fit=pa_fit, peak_age_ci=pa_ci,
                              deltas_post_peak=deltas, last_fat_age=last_fat,
                              tail_annual_ratio=(round(tail_rate, 4) if tail_rate else None))
    print('\n[%s] peak_fit=%d ci=%s  last_fat_step=%s tail_ratio=%s' % (grp, pa_fit, pa_ci, last_fat, tail_rate))
    for a in sorted(steps):
        s = steps[a]
        print('  %d->%d n=%3d ratio=%.4f ci=[%.4f,%.4f]%s env=%s' % (
            a, a + 1, s['n'], s['ratio'], s['ci'][0], s['ci'][1], ' THIN' if s['thin'] else '', s['envelope']))
    print('  curve: ' + ' '.join('%d:%.3f' % (a, curve[a]['F']) for a in sorted(curve)))

# engine reference curves for the side-by-side
DELTAS = {-8: .58, -7: .62, -6: .68, -5: .74, -4: .80, -3: .86, -2: .92, -1: .97, 0: 1.0, 1: .99, 2: .98,
          3: .96, 4: .94, 5: .91, 6: .88, 7: .84, 8: .79, 9: .73, 10: .66, 11: .58, 12: .50, 13: .42, 14: .34}
PEAK_AGE = {'MID': 25, 'RUCK': 27, 'SD': 26, 'KPD': 27, 'SF': 25, 'KPF': 27}
OUT['engine_reference'] = dict(DELTAS=DELTAS, PEAK_AGE=PEAK_AGE)

with open(os.path.join(HERE, 'RESULTS_B_CURVES.json'), 'w') as f:
    json.dump(OUT, f, indent=1)
print('\nwrote RESULTS_B_CURVES.json')
