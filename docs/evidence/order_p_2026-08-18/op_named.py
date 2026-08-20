#!/usr/bin/env python3
"""ORDER P — THE BAR ITSELF, THE ILLUSTRATION ROWS, THE MATCHED PAIR, AND THE AGE SENSITIVITY.

READ-ONLY. NO BOARD IS BUILT. Every price here is an ESTIMATE PENDING A BUILD.

NO NAMED ROW IS A TARGET. Not one constant in this order was chosen with any row in view. The rows
below are printed because the order asked to see them, wherever the derived rule puts them.

  usage: OPENBLAS_NUM_THREADS=1 ... python op_named.py
"""
import json, math, os, sys, statistics, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import op_lib as PB                                                          # noqa: E402
LB = PB.LB

PL_F = 1.0524
AGE_GATE = 24
L = []


def P(s=''):
    print(s); L.append(str(s))


S4 = json.load(open(os.path.join(HERE, 'STEP4_P.json')))
M = S4['mechanism']
G0, BSAT, S0, S_P5 = M['G0'], M['BETA_sat'], M['s0'], M['s_p5']
LAM, THR, TMAX, ZERO = M['LAMBDA'], M['THETA_R'], M['TMAX'], M['zero_at']

# ORDER N's own constants, for the third column
N_G0, N_BSAT, N_S0, N_LAM, N_THR, N_TMAX = 9.72, 0.11521, 2.3163, 0.82131, 0.14028, 5.998


def F_old(g):
    return max(0.0, LB.ETA_K * LB.m_d(g))


def F_p(g, s, age):
    if g <= 0: return 0.0
    if age is None or age >= AGE_GATE or s is None: return F_old(g)
    T = min(max(1.0 - THR * (s - S0), 0.0), TMAX)
    return 1.0 - math.exp(-LAM * (1 - math.exp(-g / G0)) * T)


def F_n(g, s, age):
    if g <= 0: return 0.0
    if age is None or age >= AGE_GATE or s is None: return F_old(g)
    T = min(max(1.0 - N_THR * (s - N_S0), 0.0), N_TMAX)
    return 1.0 - math.exp(-N_LAM * (1 - math.exp(-g / N_G0)) * T)


MK = LB.load_matrix('OKRULED')
MP = LB.load_matrix('PDERIV')
MN = LB.load_matrix('NVARB')
ROWS = PB.season_rows(MK)
PG = PB.Premium(ROWS, h=PB.H_PRIMARY, iso=True)
LED = LB.load_ledger()
byk = {r['key']: r for r in LED['rows']}

P('=' * 118)
P('ORDER P — THE BAR, THE ILLUSTRATIONS AND THE AGE SENSITIVITY. ESTIMATES PENDING A BUILD.')
P('=' * 118)
P()

# ---- 1 · the bar, printed ------------------------------------------------------------------------------
P('-' * 118)
P('1 · THE BAR ITSELF. What a player at this entry price is expected to produce at this age.')
P('-' * 118)
P('   BAR_P(v0, pos, age) = age bar(pos, age) + pedigree premium PG(ln v0, class)')
P()
for pos in ('MID', 'SF', 'KPD', 'KPF', 'RUCK', 'SD'):
    cls = 'TALL' if pos in LB.TALLPOS else 'SMALL'
    P('   %-5s (%s)   age bar 18..23: %s' % (
        pos, cls, ' '.join('%.1f' % LB.bar(pos, a) for a in range(18, 24))))
P()
P('   the premium added on top, by entry price:')
P('   %10s | %10s %10s' % ('v0', 'SMALL', 'TALL'))
for v in (100, 200, 300, 500, 800, 1200, 1700, 2400, 3200):
    P('   %10d | %+10.2f %+10.2f' % (v, PG.at_v0(v, 'SMALL'), PG.at_v0(v, 'TALL')))
P()
P('   WORKED. A 19-year-old midfielder taken at pick 6 has an entry price near 1660.')
P('     age bar 57.0  +  premium %+.2f  =  bar %.1f points a game.' % (
    PG.at_v0(1660, 'SMALL'), 57.0 + PG.at_v0(1660, 'SMALL')))
P('   A 19-year-old midfielder taken at pick 50 has an entry price near 285.')
P('     age bar 57.0  +  premium %+.2f  =  bar %.1f points a game.' % (
    PG.at_v0(285, 'SMALL'), 57.0 + PG.at_v0(285, 'SMALL')))
P('   Same age, same position, same league. The expensive one has to produce %.1f more points a game' % (
    PG.at_v0(1660, 'SMALL') - PG.at_v0(285, 'SMALL')))
P('   to be judged as being ON TRACK. That is the owner\'s sentence, written as a number.')
P()

# ---- 2 · the named rows -------------------------------------------------------------------------------
P('-' * 118)
P('2 · THE ILLUSTRATION ROWS. CONSEQUENCES, NEVER TARGETS.')
P('-' * 118)
NAMED = ['harry-dean', 'cooper-duff-tytler', 'xavier-taylor', 'daniel-annable', 'dylan-patterson',
         'isaac-kako', 'josh-smillie', 'milan-murdock']
P('   %-20s %3s %5s %5s %6s | %7s %6s %7s | %6s %6s %6s | %6s %6s %6s' % (
    'row', 'age', 'pick', 'g', 'v0', 's_N', 'prem', 's_P', 'chg K', 'chg N', 'chg P',
    'K', 'N', 'P'))
NAM = {}
for k in NAMED:
    r = byk.get(k); m = MK.get(k)
    if r is None or m is None:
        P('   %-20s  not on the 804-row board' % k); continue
    g = float(r['g'] or 0)
    age = LB.age_at(m, 2026)
    sN = LB.perf_surplus(m, 2026)
    sP = PB.perf_surplus_P(m, 2026, PG)
    prem = PB.premium_of(m, PG)
    vk = float(r['orderk'])
    vn = float(MN[k]['cur']) / PL_F if MN[k].get('cur') is not None else vk
    vp = float(MP[k]['cur']) / PL_F if MP[k].get('cur') is not None else vk
    P('   %-20s %3d %5s %5.0f %6.0f | %7s %6s %7s | %5.1f%% %5.1f%% %5.1f%% | %6d %6d %6d' % (
        r['name'][:20], r['age'], r['pick'], g, float(m['v0']),
        ('%+.2f' % sN) if sN is not None else 'n/a',
        ('%+.2f' % prem) if prem is not None else 'n/a',
        ('%+.2f' % sP) if sP is not None else 'n/a',
        100 * F_old(g), 100 * F_n(g, sN, age), 100 * F_p(g, sP, age),
        round(vk), round(vn), round(vp)))
    NAM[k] = dict(name=r['name'], age=r['age'], pick=r['pick'], g=g, v0=float(m['v0']),
                  sN=sN, sP=sP, prem=prem, chgK=100 * F_old(g), chgN=100 * F_n(g, sN, age),
                  chgP=100 * F_p(g, sP, age), K=vk, N=vn, P=vp)
P()

# ---- 3 · the matched pair -------------------------------------------------------------------------------
P('-' * 118)
P('3 · THE MATCHED PAIR — the owner\'s point, made visible on two real rows')
P('-' * 118)
P('   A top-10 pick and a pick 41-64 (or pool) row, produced to within 1.5 points a game of each other')
P('   against the SAME age bar, and within 4 career games of each other. Chosen only on those two')
P('   conditions, nothing else. The point of the pair is what the PEDIGREE bar does to them.')
P()
cand = []
for r in LED['rows']:
    k = r['key']; m = MK.get(k)
    if m is None or int(r['age']) >= 24:
        continue
    g = float(r['g'] or 0)
    if g < 1:
        continue
    sN = LB.perf_surplus(m, 2026); sP = PB.perf_surplus_P(m, 2026, PG)
    if sN is None or sP is None:
        continue
    pick = r.get('pick')
    try:
        pk = int(pick)
    except (TypeError, ValueError):
        pk = None
    grp = 'top' if (pk is not None and pk <= 10) else ('late' if (pk is None or pk >= 41) else None)
    if grp is None:
        continue
    cand.append(dict(key=k, name=r['name'], age=int(r['age']), pick=pick, g=g, v0=float(m['v0']),
                     sN=sN, sP=sP, grp=grp, K=float(r['orderk']),
                     N=(float(MN[k]['cur']) / PL_F if MN[k].get('cur') is not None else float(r['orderk'])),
                     P=(float(MP[k]['cur']) / PL_F if MP[k].get('cur') is not None else float(r['orderk'])),
                     age_v=LB.age_at(m, 2026)))
pairs = []
for a in [c for c in cand if c['grp'] == 'top']:
    for b in [c for c in cand if c['grp'] == 'late']:
        if abs(a['sN'] - b['sN']) <= 1.5 and abs(a['g'] - b['g']) <= 4 and min(a['g'], b['g']) >= 3:
            pairs.append((abs(a['sN'] - b['sN']) + 0.1 * abs(a['g'] - b['g']), a, b))
pairs.sort(key=lambda t: t[0])
P('   %-22s %3s %5s %5s %6s | %7s %7s %7s | %6s %6s | %6s %6s' % (
    'row', 'age', 'pick', 'g', 'v0', 's_N', 'premium', 's_P', 'chg K', 'chg P', 'ORDER K', 'ORDER P'))
PAIRS = []
seen = set()
for _, a, b in pairs:
    if (a['key'], b['key']) in seen or len(PAIRS) >= 3:
        continue
    seen.add((a['key'], b['key']))
    for c in (a, b):
        prem = PB.premium_of(MK[c['key']], PG)
        P('   %-22s %3d %5s %5.0f %6.0f | %+7.2f %+7.2f %+7.2f | %5.1f%% %5.1f%% | %6d %6d' % (
            c['name'][:22], c['age'], c['pick'], c['g'], c['v0'], c['sN'], prem, c['sP'],
            100 * F_old(c['g']), 100 * F_p(c['g'], c['sP'], c['age_v']), round(c['K']), round(c['P'])))
    P('   ' + '-' * 108)
    PAIRS.append(dict(top=a['name'], late=b['name'], dsN=a['sN'] - b['sN']))
P()
P('   Read one pair. The two produced the same amount above their AGE bar. Under ORDER K they pay')
P('   almost the same charge, because the charge only reads games. Under ORDER P the expensive one')
P('   is measured against a higher bar, so the same production is a WORSE result for him, and he')
P('   pays more. That is the owner\'s sentence, on two real rows.')
P()

# ---- 4 · the age sensitivity ------------------------------------------------------------------------------
P('-' * 118)
P('4 · THE DECLARED AGE SENSITIVITY. The premium is NOT age-flat, and this prices what that costs.')
P('-' * 118)
P('   Step 2 measured the premium spread PG(p90)-PG(p10) at every age: 19 +8.83 · 20 +14.27 ·')
P('   21 +16.44 · 22 +17.29 · 23 +19.60. The primary bar POOLS ages, as preregistered, because the')
P('   ages 18-19 TALL cells hold 8 and 169 rows. The pooled spread is +16.7 SMALL / +9.8 TALL.')
P('   So the pooled bar is MORE demanding of a 19-year-old high pick than his own age slice says, and')
P('   LESS demanding of a 23-year-old one. This variant carries the age axis and re-solves LAMBDA.')
P()


class AgePrem(object):
    """PG(x, class, age). Ages 18 and 19 are pooled — the age-18 cell holds 39 rows in total."""

    def __init__(self, rows):
        self.byage = {}
        for a in range(18, 24):
            sub = [r for r in rows if (r['age'] == a or (a == 19 and r['age'] == 18))]
            self.byage[a] = PB.Premium(sub, h=PB.H_PRIMARY, iso=True)
        self.byage[18] = self.byage[19]

    def at_v0(self, v0, cls, age):
        a = max(18, min(23, int(age if age is not None else 21)))
        return self.byage[a].at_v0(v0, cls)

    def bar_p(self, pos, age, v0):
        cls = 'TALL' if pos in LB.TALLPOS else 'SMALL'
        b = LB.bar(pos, age)
        return None if b is None else b + self.at_v0(v0, cls, age)


AP = AgePrem(ROWS)


def surplus_age(rec, Y):
    ss = LB.seasons_upto(rec, Y)
    if not ss:
        return None
    v0 = float(rec.get('v0') or 0.0)
    if not (v0 > 0):
        return None
    num = den = 0.0
    for s in ss:
        a = LB.age_at(rec, s['year']); pos = s.get('bar')
        bp = AP.bar_p(pos, a, v0) if pos in LB.BARS else None
        if bp is None or s.get('avg') is None:
            return None
        g = float(s['games']); num += g * (float(s['avg']) - bp); den += g
    return num / den if den > 0 else None


S2J = json.load(open(os.path.join(HERE, 'STEP2_P.json')))
sa = []
for r in S2J['rows']:
    m = MK[r['key']]
    v = surplus_age(m, r['Y'])
    if v is not None:
        sa.append(dict(g=r['g'], s=v))
gg = np.array([r['g'] for r in sa]); ss = np.array([r['s'] for r in sa])
S0A = float((ss * gg).sum() / gg.sum()); S5A = float(np.percentile(ss, 5))
P('   age-carrying surplus: games-weighted mean %+.4f (pooled bar %+.4f), p5 %+.2f' % (S0A, S0, S5A))

ME = LB.load_matrix('M0ETA0')
VANA = {}
for k, a in MK.items():
    b = ME[k]
    yrs = a.get('yrs') or []
    vpa = a.get('vpath') or []; vpb = b.get('vpath') or []
    row = []
    for i, y in enumerate(yrs):
        if i >= len(vpa) or i >= len(vpb) or vpa[i] is None or vpb[i] is None:
            row.append(None); continue
        g = LB.career_games(a, y); md = LB.m_d(g)
        row.append(dict(y=y, g=g, s=surplus_age(a, y), age=LB.age_at(a, y),
                        C=((vpb[i] - vpa[i]) / (0.50 * md)) if md > 1e-12 else 0.0, v0eta=float(vpb[i])))
    VANA[k] = row


def F_a(g, s, age, lam):
    if g <= 0: return 0.0
    if age is None or age >= AGE_GATE or s is None: return F_old(g)
    thr = BSAT / lam
    tmax = 1.0 - thr * (S5A - S0A)
    T = min(max(1.0 - thr * (s - S0A), 0.0), tmax)
    return 1.0 - math.exp(-lam * (1 - math.exp(-g / G0)) * T)


anchor = []
for k, a in MK.items():
    c = (a['year'] if a.get('type') == 'MSD' else a['year'] + 1)
    if c not in range(2005, 2016) or not (float(a.get('v0') or 0) > 0): continue
    yrs = a.get('yrs') or []
    if c not in yrs: continue
    v = VANA[k][yrs.index(c)]
    if v is None or v['C'] <= 0: continue
    anchor.append(v)
tot_old = sum(v['C'] * F_old(v['g']) for v in anchor)
lo, hi = 1e-6, 20.0
for _ in range(200):
    mid = 0.5 * (lo + hi)
    if sum(v['C'] * F_a(v['g'], v['s'], v['age'], mid) for v in anchor) < tot_old:
        lo = mid
    else:
        hi = mid
LAMA = 0.5 * (lo + hi)
P('   SOLVED under the age-carrying bar: LAMBDA = %.5f (pooled bar: %.5f)' % (LAMA, LAM))

SRC = json.load(open(os.path.join(LB.SP, 'per_entrant_OKRULED.json')))['recs']
NDR = [r for r in SRC if (not r.get('is_pool')) and r.get('teaches_curve') and r.get('type') == 'ND'
       and r.get('pick') and 1 <= int(r['pick']) <= 64]
WEND = max(y for r in SRC for y, v in zip(r.get('yrs') or [], r.get('vpath') or []) if v is not None)


def vp_a(r, lam):
    vp = list(r.get('vpath') or [])
    van = VANA.get(r['key']) or []
    for i in range(len(vp)):
        if i >= len(van) or van[i] is None or vp[i] is None: continue
        v = van[i]
        if v['C'] <= 0: continue
        vp[i] = round(v['v0eta'] - v['C'] * F_a(v['g'], v['s'], v['age'], lam), 1)
    return vp


cache = {r['key']: vp_a(r, LAMA) for r in NDR}
AGEBANDS = {}
for wname, lo_, hi_ in (('PRIMARY', 2005, 2023), ('MODERN', 2019, 2023)):
    for bname, bf in (('ALL picks 1-64', lambda p: True), ('picks 1-10', lambda p: p <= 10),
                      ('picks 31-40', lambda p: 31 <= p <= 40), ('picks 41-64', lambda p: 41 <= p <= 64)):
        incl = [r for r in NDR if lo_ <= r['year'] + 1 <= hi_ and bf(int(r['pick'])) and r['year'] + 1 <= WEND]
        vals = [(0.0 if (not cache[r['key']] or cache[r['key']][0] is None) else float(cache[r['key']][0]))
                for r in incl]
        AGEBANDS['%s|%s' % (wname, bname)] = statistics.mean(vals) / statistics.mean(
            [float(r['v0']) for r in incl]) - 1.0


def classmark_a(lam, lo_y, hi_y):
    per = []
    for y in range(lo_y, hi_y + 1):
        num = den = 0.0; n = 0
        for k, a in MK.items():
            c = (a['year'] if a.get('type') == 'MSD' else a['year'] + 1)
            if c != y or not (float(a.get('v0') or 0) > 0): continue
            yrs = a.get('yrs') or []
            vp = vp_a(a, lam)
            if not yrs: v1 = 0.0
            elif y < yrs[0]: continue
            elif y > yrs[-1]: v1 = 0.0
            else:
                i = yrs.index(y); v1 = 0.0 if vp[i] is None else float(vp[i])
            num += v1; den += float(a['v0']); n += 1
        if den > 0 and n >= 5: per.append(num / den)
    return sum(per) / len(per)


w2a = classmark_a(LAMA, 2006, 2016)
P()
P('   %-18s | %-12s %-12s | %-12s' % ('', 'pooled bar', 'age-carrying', 'ORDER K'))
P('   %-18s | %+11.2f%% %+11.2f%% | %+11.2f%%' % (
    'picks 1-10 PRI', 100 * S4['ladder'][0]['p110_pri'], 100 * AGEBANDS['PRIMARY|picks 1-10'], 8.22))
P('   %-18s | %+11.2f%% %+11.2f%% | %+11.2f%%' % (
    'picks 1-10 MOD', 100 * S4['ladder'][0]['p110_mod'], 100 * AGEBANDS['MODERN|picks 1-10'], 13.65))
P('   %-18s | %+11.2f%% %+11.2f%% | %+11.2f%%' % (
    'picks 31-40 PRI', -8.88, 100 * AGEBANDS['PRIMARY|picks 31-40'], -10.70))
P('   %-18s | %+11.2f%% %+11.2f%% | %+11.2f%%' % (
    'picks 41-64 PRI', -5.03, 100 * AGEBANDS['PRIMARY|picks 41-64'], -6.89))
P('   %-18s | %11.4f %11.4f | %11.4f' % ('W2 class mark', S4['class_w2'], w2a, 1.0513))
P()
P('   The age-carrying bar is a SENSITIVITY, not the proposal. It is printed so the owner can see')
P('   what the pooling costs, and it is not adopted here because the prereg fixed the pooled bar as')
P('   primary before any of these numbers existed.')
P()

json.dump(dict(named=NAM, pairs=PAIRS, age_variant=dict(LAMBDA=LAMA, s0=S0A, s_p5=S5A,
                                                        bands=AGEBANDS, w2=w2a),
               premium_table={str(v): dict(SMALL=PG.at_v0(v, 'SMALL'), TALL=PG.at_v0(v, 'TALL'))
                              for v in (100, 200, 300, 500, 800, 1200, 1700, 2400, 3200)}),
          open(os.path.join(HERE, 'NAMED_P.json'), 'w'), indent=1, default=float)
open(os.path.join(HERE, 'NAMED_P_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote NAMED_P.json and NAMED_P_out.txt')
