#!/usr/bin/env python3
# =====================================================================================================
# ORDER B DERIVATION -- b1b: EFFECTIVE (delivered-value-scale) decline surfaces. DISCLOSED EXTENSION
# of PREREG_B.md §1: the prereg'd avg-scale pair fit measures per-game level among players who play
# >=4 games -- it is blind to the availability channel (games fade + missed seasons), which the W5
# remaining-value ruler credits. The prereg's own closure rule ("the fitted curve must CLOSE the called
# bias") forces the fit onto the delivered-value scale; this file measures that surface with the SAME
# cohort + ruler as W5. Estimator: within-player paired ratio-of-sums of season value SV between
# consecutive ages, conditioned on ALIVE at both ages (alive = year inside the player's own career
# span; missed years inside the span count as SV=0). Exits stay OUT of this curve -- they are the
# terminal discount's channel (b2). Career-complete players only (W5 primary rule) to kill censoring.
# =====================================================================================================
import json, math, os, hashlib, collections
import numpy as np

SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
HERE = os.path.dirname(os.path.abspath(__file__))
CAND_P = SP + '/per_entrant_O31FFINAL.json'
SEED = 34
B_BOOT = 2000
FM = {'paddy-mccartin', 'thomas-boyd'}
BARS = {'KPD': 65.4, 'KPF': 63.8, 'MID': 77.1, 'RUCK': 75.5, 'SD': 75.3, 'SF': 67.9}
S_SH = 3.0
LCAPT_BAR, LCAPT_M, LCAPT_W, LCAPT_G = 105.0, 109.5, 1.85, 1.00
POSG = {'KPD': 'TALL', 'KPF': 'TALL', 'MID': 'SMALL', 'SD': 'SMALL', 'SF': 'SMALL', 'RUCK': 'RUCK'}
LAST_REAL_SEASON = 2025
ENTRY_FLOOR = 2005
NMIN = 20


def md5f(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()


def softplus(x):
    return math.log1p(math.exp(x)) if x < 30.0 else x


def capt_prem(lev):
    c = LCAPT_G * LCAPT_W * (softplus((lev - LCAPT_M) / LCAPT_W) - softplus((LCAPT_BAR - LCAPT_M) / LCAPT_W))
    return c if c > 0.0 else 0.0


def posval(x):
    return S_SH * math.log(1 + math.exp(min(x / S_SH, 40.0)))


def season_raw(X, g):
    return posval(X + capt_prem(X) - BARS[g]) * 21.0


def w_sqrt(g):
    return min(1.0, math.sqrt(max(0.0, g) / 10.0))


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


m5 = md5f(CAND_P)
assert m5.startswith('d97f1aee'), 'HALT md5 ' + m5
A = json.load(open(CAND_P))
recs = A['recs']

# per-player: career span, per-year SV + bar + games (career-complete only)
P = {}
for r in recs:
    k = r['key']
    if k in FM or arm_of(r) is None or r['year'] < ENTRY_FLOOR:
        continue
    lg = r.get('last_game_year')
    complete = (r['retired_now'] or r['delisted']) and (lg is not None and lg <= LAST_REAL_SEASON) \
        and not any(s['year'] > LAST_REAL_SEASON for s in r['seasons'])
    if not complete:
        continue
    yrs = [s['year'] for s in r['seasons'] if s.get('games', 0) >= 1 and s['year'] <= LAST_REAL_SEASON]
    if not yrs:
        continue
    sv, bar, gms = {}, {}, {}
    for s in r['seasons']:
        if s['year'] > LAST_REAL_SEASON or s.get('bar') not in BARS:
            continue
        sv[s['year']] = w_sqrt(s['games']) * season_raw(s['avg'], s['bar'])
        bar[s['year']] = s['bar']
        gms[s['year']] = s['games']
    P[k] = dict(y0=min(yrs), y1=max(yrs), sv=sv, bar=bar, gms=gms,
                age0=r['age_draft'], yr=r['year'])
print('career-complete players %d' % len(P))


def age_of(p, t):
    return p['age0'] + (t - p['yr'])


def grp_at(p, t):
    """position group at year t: bar of that year, else nearest earlier bar."""
    if t in p['bar']:
        return POSG[p['bar'][t]], p['bar'][t]
    for u in range(t - 1, p['yr'] - 1, -1):
        if u in p['bar']:
            return POSG[p['bar'][u]], p['bar'][u]
    return None, None


# paired player-age observations: alive at a (year t in span) and alive at a+1 (t+1 in span)
obs = []   # (key, grp, bar, a, sv_a, sv_a1, g_a, g_a1)
for k, p in P.items():
    for t in range(p['y0'], p['y1']):        # t and t+1 both inside span
        a = age_of(p, t)
        if not (21 <= a <= 33):
            continue
        g, b = grp_at(p, t)
        if g is None:
            continue
        obs.append(dict(key=k, grp=g, bar=b, a=a,
                        s0=p['sv'].get(t, 0.0), s1=p['sv'].get(t + 1, 0.0),
                        g0=p['gms'].get(t, 0), g1=p['gms'].get(t + 1, 0)))
print('alive-paired obs %d' % len(obs))

players = sorted({o['key'] for o in obs})
by_player = collections.defaultdict(list)
for o in obs:
    by_player[o['key']].append(o)
RNG = np.random.default_rng(SEED)
boot_draws = [RNG.integers(0, len(players), size=len(players)) for _ in range(B_BOOT)]


def match(o, grp):
    return (o['bar'] == grp) if grp in ('KPD', 'KPF') else (o['grp'] == grp)


def chain_stats(sel, grp):
    """age -> (sum s1, sum s0, n) ratio-of-sums."""
    agg = collections.defaultdict(lambda: [0.0, 0.0, 0])
    for o in sel:
        if not match(o, grp):
            continue
        c = agg[o['a']]
        c[0] += o['s1']; c[1] += o['s0']; c[2] += 1
    return {a: (v[0] / v[1] if v[1] > 0 else np.nan, v[2]) for a, v in agg.items()}


OUT = dict(meta=dict(note='b1b effective delivered-value-scale surfaces; disclosed extension per closure rule',
                     input=dict(path=CAND_P, md5=m5), seed=SEED, B_boot=B_BOOT,
                     players=len(P), obs=len(obs)),
           groups={}, games_by_age={}, sv_by_age={})

# descriptive: games + SV by age for TALL/RUCK/SMALL (alive-conditioned)
for grp in ('TALL', 'RUCK', 'SMALL'):
    ga = collections.defaultdict(list); sa = collections.defaultdict(list)
    for o in obs:
        if match(o, grp):
            ga[o['a']].append(o['g0']); sa[o['a']].append(o['s0'])
    OUT['games_by_age'][grp] = {a: dict(n=len(v), mean_games=round(float(np.mean(v)), 2)) for a, v in sorted(ga.items())}
    OUT['sv_by_age'][grp] = {a: dict(n=len(v), mean_sv=round(float(np.mean(v)), 1)) for a, v in sorted(sa.items())}

for grp in ('TALL', 'RUCK', 'SMALL', 'KPD', 'KPF'):
    pt = chain_stats(obs, grp)
    boots = {a: [] for a in range(21, 34)}
    for bp in boot_draws:
        sel = []
        for i in bp:
            sel.extend(by_player[players[i]])
        rr = chain_stats(sel, grp)
        for a in boots:
            boots[a].append(rr.get(a, (np.nan,))[0])
    steps = {}
    for a in sorted(pt):
        ratio, n = pt[a]
        bs = np.array(boots[a], dtype=float)
        fin = np.isfinite(bs)
        lo, hi = (np.nanpercentile(bs[fin], [5, 95]) if fin.sum() > 100 else (np.nan, np.nan))
        steps[a] = dict(n=n, ratio=round(float(ratio), 4), ci=[round(float(lo), 4), round(float(hi), 4)],
                        thin=(n < NMIN))
    fat = [a for a in sorted(steps) if not steps[a]['thin'] and np.isfinite(steps[a]['ratio'])]
    F = {24: 1.0}
    for a in range(24, 34):
        if a in fat and a in F:
            F[a + 1] = F[a] * steps[a]['ratio']
        else:
            break
    for a in range(23, 20, -1):
        if a in fat and (a + 1) in F:
            F[a] = F[a + 1] / steps[a]['ratio']
        else:
            break
    Fboot = {a: [] for a in F}
    for bi in range(B_BOOT):
        Fb = {24: 1.0}
        for a in range(24, 34):
            if a in fat and a in Fb and np.isfinite(boots[a][bi]):
                Fb[a + 1] = Fb[a] * boots[a][bi]
            else:
                break
        for a in range(23, 20, -1):
            if a in fat and (a + 1) in Fb and np.isfinite(boots[a][bi]):
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
    pa_fit = max(F, key=lambda a: F[a])
    pa_bs = []
    for bi in range(B_BOOT):
        d = {a: Fboot[a][bi] for a in Fboot if np.isfinite(Fboot[a][bi])}
        if d:
            pa_bs.append(max(d, key=lambda a: d[a]))
    pa_ci = [int(np.percentile(pa_bs, 5)), int(np.percentile(pa_bs, 95))] if pa_bs else None
    last_fat = max(fat) if fat else None
    OUT['groups'][grp] = dict(steps=steps, curve=curve, peak_age_fit=pa_fit, peak_age_ci=pa_ci,
                              last_fat_age=last_fat,
                              tail_annual_ratio=(round(steps[last_fat]['ratio'], 4) if last_fat else None))
    print('\n[%s SV-scale] peak=%d ci=%s last_fat=%s' % (grp, pa_fit, pa_ci, last_fat))
    for a in sorted(steps):
        s = steps[a]
        print('  %d->%d n=%3d ratio=%.4f ci=[%.4f,%.4f]%s' % (a, a + 1, s['n'], s['ratio'],
                                                              s['ci'][0], s['ci'][1], ' THIN' if s['thin'] else ''))
    print('  curve: ' + ' '.join('%d:%.3f' % (a, curve[a]['F']) for a in sorted(curve)))
    if grp in ('TALL', 'RUCK', 'SMALL'):
        gg = OUT['games_by_age'][grp]
        print('  games: ' + ' '.join('%d:%.1f' % (a, gg[a]['mean_games']) for a in sorted(gg) if 23 <= a <= 32))

with open(os.path.join(HERE, 'RESULTS_B_EFFECTIVE.json'), 'w') as f:
    json.dump(OUT, f, indent=1)
print('\nwrote RESULTS_B_EFFECTIVE.json')
