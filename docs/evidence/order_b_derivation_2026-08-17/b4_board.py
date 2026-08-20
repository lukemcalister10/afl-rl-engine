#!/usr/bin/env python3
# =====================================================================================================
# ORDER B DERIVATION -- b4: BOTH-BASELINE BOARD IMPACT PREVIEW (PREREG_B.md Object 5). Read-only,
# offline counterfactual arithmetic. Derived objects applied:
#   O1 tall ladder (pa*=27, rho0=.03, g=.025) + ANCHOR-PRESERVING renorm s* (wiring W-A)
#   O2 discount knots r={28:.15, 29:.16, 30:.22, 31:.34(boundary)}; hazard-variant sensitivity
#   O4 taper retirement: per-row dprice_A from W6_BOARD_IMPACT.json (variant A == derived object)
# Per-row production ratio uses the ENGINE'S OWN inputs (pn=peak, ln=level_now, gf/fut) from the
# candidate app-data. First-order on the production leg; pedigree leg untouched; stated as such.
# =====================================================================================================
import json, math, os, hashlib, collections
import numpy as np

SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
HERE = os.path.dirname(os.path.abspath(__file__))

REPL = {'MID': 80.1, 'SD': 78.3, 'RUCK': 78.5, 'KPD': 68.4, 'SF': 70.9, 'KPF': 66.8}
PEAK = {'MID': 92, 'RUCK': 92, 'SD': 78, 'KPD': 70, 'SF': 70, 'KPF': 72}
PEAK_AGE = {'MID': 25, 'RUCK': 27, 'SD': 26, 'KPD': 27, 'SF': 25, 'KPF': 27}
DELTAS = {-8: .58, -7: .62, -6: .68, -5: .74, -4: .80, -3: .86, -2: .92, -1: .97, 0: 1.0, 1: .99, 2: .98,
          3: .96, 4: .94, 5: .91, 6: .88, 7: .84, 8: .79, 9: .73, 10: .66, 11: .58, 12: .50, 13: .42, 14: .34}
PMAX = 0.25
S_SH = 3.0
LCAPT_BAR, LCAPT_M, LCAPT_W, LCAPT_G = 105.0, 109.5, 1.85, 1.00
PA_F, RHO_F, G_F = 27, 0.030, 0.025
KNOTS = {28: 0.15, 29: 0.16, 30: 0.22, 31: 0.34}
KNOTS_HAZ = {28: 0.14, 29: 0.211, 30: 0.232, 31: 0.246}


def softplus(x):
    return math.log1p(math.exp(x)) if x < 30.0 else x


def capt_prem(lev):
    c = LCAPT_G * LCAPT_W * (softplus((lev - LCAPT_M) / LCAPT_W) - softplus((LCAPT_BAR - LCAPT_M) / LCAPT_W))
    return c if c > 0.0 else 0.0


def posval(x):
    return S_SH * math.log(1 + math.exp(min(x / S_SH, 40.0)))


def ladder_of(rho0, g, n=12):
    f, out = 1.0, []
    for j in range(1, n + 1):
        out.append(f := f * (1.0 - min(0.60, max(0.0, rho0 + g * (j - 1)))))
    return out


LAD = ladder_of(RHO_F, G_F)


def frac_engine(a, pa):
    return DELTAS[max(-8, min(14, int(round(a - pa))))]


def frac_new(a, pa_star, ladder=LAD):
    j = int(round(a - pa_star))
    if j <= 0:
        return DELTAS[max(-8, j)]
    if j <= len(ladder):
        return ladder[j - 1]
    lr = ladder[-1] / (ladder[-2] if len(ladder) > 1 else 1.0)
    f = ladder[-1]
    for _ in range(j - len(ladder)):
        f *= lr
    return f


def rate_of(a, knots):
    if a <= 27:
        return 0.14
    return knots.get(min(int(a), 31), knots[31])


def mark_stream(g, g0, fut, lp, cl, a, r, fracfn, pa, tall_prem=True):
    """proj_from_peak replica with the board's REPL conventions (k=0 on g0; k>=1 on fut mix)."""
    prod = 0.0
    for k in range(18):
        ag = a + k
        fv = fracfn(ag, pa)
        if ag > 38 or fv < 0.42:
            break
        lev = lp * fv
        if cl is not None and (ag <= pa or k == 0):
            lev = max(lev, cl)
        base = lev + capt_prem(lev)
        df = (1.0 + r) ** k
        if k == 0:
            prod += posval(base - REPL[g0]) * 21 / df
        else:
            prod += sum(w * posval(base - REPL[gg]) for gg, w in fut) * 21 / df
    if g in ('KPF', 'KPD') and tall_prem:
        prod *= 1.05
    runway = min(max((25 - a) / 6.0, 0), 1)
    elite = min(max((lp / PEAK[g] - 0.97) / 0.30, 0), 1)
    return prod * (1 + runway * elite * PMAX)


# ---- inputs -----------------------------------------------------------------------------------------
def md5f(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()


B = json.load(open(SP + '/cand31.json'))
assert md5f(SP + '/cand31.json').startswith('d4e80349')
assert B['boards']['candidate'].startswith('fe6be9d6') and B['boards']['live'].startswith('88ce647f')
APP = json.load(open(SP + '/o31f/bb_f2on/rl_after/rl_app_data.json'))
ACT = {r['key']: r for r in APP['active']}
W6I = json.load(open(os.path.join(os.path.dirname(HERE), 'order33_w6_2026-08-17', 'W6_BOARD_IMPACT.json')))
W6ROW = {r['key']: r for r in W6I['rows']}

# ---- s*: anchor-preserving renorm, derived from the cohort tall anchor rows (ages 23-26) -------------
# (the same construction the Order B build would run against the full engine: s* = sum M_old / sum M_new
#  over the W5 tall anchor rows, so prime-tall marks are unchanged in aggregate and the whole measured
#  RELATIVE correction lands on the veteran side)
CAND_P = SP + '/per_entrant_O31FFINAL.json'
A = json.load(open(CAND_P))
BARS = {'KPD': 65.4, 'KPF': 63.8, 'MID': 77.1, 'RUCK': 75.5, 'SD': 75.3, 'SF': 67.9}
FM = {'paddy-mccartin', 'thomas-boyd'}


def arm_of(r):
    if r.get('teaches_curve') and r['type'] == 'ND':
        return 'ND'
    if r.get('is_pool'):
        return {'RD': 'RD', 'MSD': 'MSD'}.get(r['type'], 'OTHERPOOL')
    return None


num = den = 0.0
n_anchor = 0
for r in A['recs']:
    k = r['key']
    if k in FM or arm_of(r) is None or r['year'] < 2005:
        continue
    lg = r.get('last_game_year')
    complete = (r['retired_now'] or r['delisted']) and (lg is not None and lg <= 2025) \
        and not any(s['year'] > 2025 for s in r['seasons'])
    if not complete:
        continue
    seas = {s['year']: s for s in r['seasons'] if s['year'] <= 2025 and s.get('bar') in BARS}
    for i, Y in enumerate(r['yrs']):
        if Y > 2021:
            continue
        a = r['age_draft'] + (Y - r['year'])
        if a not in (23, 24, 25, 26):
            continue
        s0 = seas.get(Y)
        if s0 is None or s0['bar'] not in ('KPD', 'KPF'):
            continue
        nu = de = 0.0
        for t in (Y, Y - 1):
            s = seas.get(t)
            if s and s['games'] >= 4:
                w = min(s['games'], 22)
                nu += w * s['avg']; de += w
        if de <= 0:
            continue
        L = nu / de
        bar = s0['bar']
        f_a = frac_engine(a, PEAK_AGE[bar])
        mo = mark_stream(bar, bar, [(bar, 1.0)], L / f_a, L, a, 0.14, frac_engine, PEAK_AGE[bar])
        fn_a = frac_new(a, PA_F)
        mn = mark_stream(bar, bar, [(bar, 1.0)], L / fn_a, L, a, 0.14, frac_new, PA_F)
        if mo > 0 and mn > 0:
            num += mo; den += mn; n_anchor += 1
S_STAR = num / den
print('anchor-preserving renorm s* = %.4f (over %d cohort tall anchor rows, ages 23-26)' % (S_STAR, n_anchor))

# ---- per-row preview --------------------------------------------------------------------------------
rows_out = []
tot = dict(cand=0, live=0, prev=0, d_prod=0, d_taper=0)
for r in B['rows']:
    k = r['key']
    ar = ACT.get(k)
    age = r['age']
    pos = r['pos']
    d_taper = float(W6ROW.get(k, {}).get('dprice_A', 0.0))
    d_prod = 0.0
    d_prod_haz = 0.0
    ratio = ratio_haz = 1.0
    if ar is not None and ar.get('pn'):
        g = ar.get('gf') or ar['grp']
        g0 = ar['grp']
        fut = [(f[0], f[1]) for f in (ar.get('fut') or [[g, 1.0]])]
        lp = float(ar['pn'])
        cl = float(ar['ln']) if ar.get('ln') else None
        is_tall = g in ('KPD', 'KPF')
        mo = mark_stream(g, g0, fut, lp, cl, age, 0.14, frac_engine, PEAK_AGE[g])
        if mo > 0:
            if is_tall:
                f_a = frac_engine(age, PEAK_AGE[g])
                fn_a = frac_new(age, PA_F)
                # lp is a PEAK-scale object; the ladder changes only post-peak fractions, lp unchanged
                mn = S_STAR * mark_stream(g, g0, fut, lp, cl, age, rate_of(age, KNOTS), frac_new, PA_F)
                mh = S_STAR * mark_stream(g, g0, fut, lp, cl, age, rate_of(age, KNOTS_HAZ), frac_new, PA_F)
            else:
                mn = mark_stream(g, g0, fut, lp, cl, age, rate_of(age, KNOTS), frac_engine, PEAK_AGE[g])
                mh = mark_stream(g, g0, fut, lp, cl, age, rate_of(age, KNOTS_HAZ), frac_engine, PEAK_AGE[g])
            ratio = mn / mo
            ratio_haz = mh / mo
            d_prod = r['production_pts'] * (ratio - 1.0)
            d_prod_haz = r['production_pts'] * (ratio_haz - 1.0)
    prev = r['cand'] + d_prod + d_taper
    rows_out.append(dict(key=k, name=r['name'], age=age, pos=pos, pathway=r['pathway'],
                         cand=r['cand'], live=r['live'],
                         prod_ratio=round(ratio, 4), prod_ratio_hazard=round(ratio_haz, 4),
                         d_prod=round(d_prod, 1), d_prod_hazard=round(d_prod_haz, 1),
                         d_taper=round(d_taper, 1),
                         preview=round(prev, 1),
                         d_vs_cand31=round(prev - r['cand'], 1),
                         d_vs_live=round(prev - r['live'], 1)))
    tot['cand'] += r['cand']; tot['live'] += r['live']; tot['prev'] += prev
    tot['d_prod'] += d_prod; tot['d_taper'] += d_taper

print('\nTOTALS: cand31 %d  live %d  preview %.0f  (d_prod %+.0f, d_taper %+.0f)'
      % (tot['cand'], tot['live'], tot['prev'], tot['d_prod'], tot['d_taper']))

NAMED = ['callum-wilkie', 'peter-wright', 'harris-andrews', 'josh-battle', 'harry-mckay', 'charlie-curnow',
         'ned-moyle', 'sam-de-koning', 'tom-de-koning', 'marcus-bontempelli', 'jack-sinclair',
         'zachary-merrett', 'isaac-heeney', 'timothy-english', 'nick-madden']
ro = {x['key']: x for x in rows_out}
print('\nNAMED ROWS (preview vs BOTH baselines):')
print('%-22s %-9s %5s %7s %7s %8s %8s %8s | %8s %8s' % ('row', 'pos/age', '', 'cand31', 'live', 'd_prod', 'd_taper', 'preview', 'vs_c31', 'vs_live'))
for k in NAMED:
    x = ro.get(k)
    if not x:
        print('%-22s  (not on board)' % k)
        continue
    print('%-22s %-4s %2d   %7d %7d %+8.0f %+8.0f %8.0f | %+8.0f %+8.0f' % (
        x['name'][:22], x['pos'], x['age'], x['cand'], x['live'], x['d_prod'], x['d_taper'],
        x['preview'], x['d_vs_cand31'], x['d_vs_live']))

TALL_VET = [x for x in rows_out if x['pos'] in ('KPD', 'KPF') and 28 <= x['age'] <= 30]
print('\nTALL 28-30 constituency: %d rows, cand %d, d_prod %+.0f' % (
    len(TALL_VET), sum(x['cand'] for x in TALL_VET), sum(x['d_prod'] for x in TALL_VET)))
TERM = [x for x in rows_out if x['age'] >= 31 and x['pos'] not in ('KPD', 'KPF')]
print('non-tall 31+ (terminal-rate exposure): %d rows, d_prod %+.0f (hazard-variant %+.0f)' % (
    len(TERM), sum(x['d_prod'] for x in TERM), sum(x['d_prod_hazard'] for x in TERM)))
YT = [x for x in rows_out if x['pos'] in ('KPD', 'KPF') and x['age'] <= 24]
print('young talls <=24 (Order A overlap): %d rows, d_prod %+.0f (of cand %d)' % (
    len(YT), sum(x['d_prod'] for x in YT), sum(x['cand'] for x in YT)))

movers = sorted(rows_out, key=lambda x: x['d_vs_cand31'])
print('\ntop 12 fallers vs cand31:')
for x in movers[:12]:
    print('  %-24s %-4s %2d  %+7.0f (prod %+.0f taper %+.0f)' % (x['name'][:24], x['pos'], x['age'],
                                                                 x['d_vs_cand31'], x['d_prod'], x['d_taper']))
print('top 12 risers vs cand31:')
for x in movers[-12:][::-1]:
    print('  %-24s %-4s %2d  %+7.0f (prod %+.0f taper %+.0f)' % (x['name'][:24], x['pos'], x['age'],
                                                                 x['d_vs_cand31'], x['d_prod'], x['d_taper']))

OUT = dict(meta=dict(s_star=round(S_STAR, 4), n_anchor=n_anchor, knots=KNOTS, knots_hazard=KNOTS_HAZ,
                     ladder={j + 1: round(v, 4) for j, v in enumerate(LAD[:10])},
                     boards=dict(cand31='fe6be9d6', live='88ce647f'),
                     note='first-order production-leg arithmetic; taper deltas = W6 variant A'),
           totals=dict(cand31=tot['cand'], live=tot['live'], preview=round(tot['prev'], 0),
                       d_prod=round(tot['d_prod'], 0), d_taper=round(tot['d_taper'], 0)),
           rows=rows_out)
with open(os.path.join(HERE, 'BOARD_PREVIEW_B.json'), 'w') as f:
    json.dump(OUT, f, indent=1)
print('\nwrote BOARD_PREVIEW_B.json')
