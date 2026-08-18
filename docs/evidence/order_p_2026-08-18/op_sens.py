#!/usr/bin/env python3
"""ORDER P — THE DECLARED SENSITIVITIES, PRICED. READ-ONLY. NO BOARD IS BUILT.

Every headline of this order rests on one estimated surface. This file re-solves the whole mechanism
under each declared variation of that surface and prints the headline numbers again, so the owner can
see whether the result is a property of the data or of a smoothing choice.

Variations, all declared in PREREG_P.md section 3.3 before any number existed:
  H = 0.25 / 0.40 / 0.60         the kernel bandwidth in log-v0 units
  raw vs isotonised              the monotonicity guard on or off
  pick band in place of ln(v0)   the axis this order did NOT choose

  usage: OPENBLAS_NUM_THREADS=1 ... python op_sens.py
"""
import json, math, os, sys, statistics, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import op_lib as PB                                                          # noqa: E402
LB = PB.LB

PL_F = 1.0524
AGE_GATE = 24
M = json.load(open(os.path.join(HERE, 'MECH_P.json')))
G0, BSAT = M['G0'], M['BETA_sat']
L = []


def P(s=''):
    print(s); L.append(str(s))


def F_old(g):
    return max(0.0, LB.ETA_K * LB.m_d(g))


MK = LB.load_matrix('OKRULED')
ME = LB.load_matrix('M0ETA0')
ROWS = PB.season_rows(MK)
SRC = json.load(open(os.path.join(LB.SP, 'per_entrant_OKRULED.json')))['recs']
NDR = [r for r in SRC if (not r.get('is_pool')) and r.get('teaches_curve') and r.get('type') == 'ND'
       and r.get('pick') and 1 <= int(r['pick']) <= 64]
WEND = max(y for r in SRC for y, v in zip(r.get('yrs') or [], r.get('vpath') or []) if v is not None)

# the charge base, computed once — it does not depend on the surface
BASE = {}
for k, a in MK.items():
    b = ME[k]
    yrs = a.get('yrs') or []
    vpa = a.get('vpath') or []; vpb = b.get('vpath') or []
    row = []
    for i, y in enumerate(yrs):
        if i >= len(vpa) or i >= len(vpb) or vpa[i] is None or vpb[i] is None:
            row.append(None); continue
        g = LB.career_games(a, y); md = LB.m_d(g)
        row.append(dict(y=y, g=g, age=LB.age_at(a, y),
                        C=((vpb[i] - vpa[i]) / (0.50 * md)) if md > 1e-12 else 0.0,
                        v0eta=float(vpb[i])))
    BASE[k] = row


class BandPrem(object):
    """The declared pick-band sensitivity: the premium is a step function of the pick band, with
    pool and pickless rows in their own bucket. Games-weighted mean of the age surplus per cell."""

    def __init__(self, rows):
        acc = collections.defaultdict(lambda: [0.0, 0.0])
        for r in rows:
            cell = (r['band'], r['cls'])
            acc[cell][0] += r['games'] * r['d']; acc[cell][1] += r['games']
        self.v = {k: (a / b) for k, (a, b) in acc.items() if b > 0}

    def at(self, rec, cls):
        b = LB.band_of(rec.get('pick') if rec.get('type') == 'ND' else None)
        return self.v.get((b, cls), 0.0)


def surplus_with(rec, Y, getprem):
    ss = LB.seasons_upto(rec, Y)
    if not ss:
        return None
    num = den = 0.0
    for s in ss:
        a = LB.age_at(rec, s['year']); pos = s.get('bar')
        if pos not in LB.BARS or s.get('avg') is None:
            return None
        bb = LB.bar(pos, a)
        if bb is None:
            return None
        cls = 'TALL' if pos in LB.TALLPOS else 'SMALL'
        g = float(s['games'])
        num += g * (float(s['avg']) - bb - getprem(rec, cls)); den += g
    return num / den if den > 0 else None


def run(tag, getprem, note):
    SU = {}
    for k, a in MK.items():
        SU[k] = {}
        for i, y in enumerate(a.get('yrs') or []):
            SU[k][y] = surplus_with(a, y, getprem)
    S2 = json.load(open(os.path.join(HERE, 'STEP2_P.json')))['rows']
    sv = []
    for r in S2:
        v = SU.get(r['key'], {}).get(r['Y'])
        if v is not None:
            sv.append((r['g'], v))
    gg = np.array([x[0] for x in sv]); ss = np.array([x[1] for x in sv])
    s0 = float((ss * gg).sum() / gg.sum()); s5 = float(np.percentile(ss, 5))

    def F(g, s, age, lam):
        if g <= 0: return 0.0
        if age is None or age >= AGE_GATE or s is None: return F_old(g)
        thr = BSAT / lam
        T = min(max(1.0 - thr * (s - s0), 0.0), 1.0 - thr * (s5 - s0))
        return 1.0 - math.exp(-lam * (1 - math.exp(-g / G0)) * T)

    anchor = []
    for k, a in MK.items():
        c = (a['year'] if a.get('type') == 'MSD' else a['year'] + 1)
        if c not in range(2005, 2016) or not (float(a.get('v0') or 0) > 0): continue
        yrs = a.get('yrs') or []
        if c not in yrs: continue
        v = BASE[k][yrs.index(c)]
        if v is None or v['C'] <= 0: continue
        anchor.append((v, SU[k].get(c)))
    tot_old = sum(v['C'] * F_old(v['g']) for v, _ in anchor)
    lo, hi = 1e-6, 20.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if sum(v['C'] * F(v['g'], s, v['age'], mid) for v, s in anchor) < tot_old: lo = mid
        else: hi = mid
    lam = 0.5 * (lo + hi)

    cache = {}
    for r in NDR:
        vp = list(r.get('vpath') or [])
        van = BASE.get(r['key']) or []
        for i in range(len(vp)):
            if i >= len(van) or van[i] is None or vp[i] is None: continue
            v = van[i]
            if v['C'] <= 0: continue
            vp[i] = round(v['v0eta'] - v['C'] * F(v['g'], SU[r['key']].get(v['y']), v['age'], lam), 1)
        cache[r['key']] = vp
    out = {}
    for wname, lo_, hi_ in (('PRIMARY', 2005, 2023), ('MODERN', 2019, 2023)):
        for bname, bf in (('ALL', lambda p: True), ('1-10', lambda p: p <= 10),
                          ('31-40', lambda p: 31 <= p <= 40), ('41-64', lambda p: 41 <= p <= 64)):
            incl = [r for r in NDR if lo_ <= r['year'] + 1 <= hi_ and bf(int(r['pick'])) and r['year'] + 1 <= WEND]
            vals = [(0.0 if (not cache[r['key']] or cache[r['key']][0] is None) else float(cache[r['key']][0]))
                    for r in incl]
            out['%s|%s' % (wname, bname)] = statistics.mean(vals) / statistics.mean(
                [float(r['v0']) for r in incl]) - 1.0
    # class mark, W2 basis
    per = []
    for y in range(2006, 2017):
        num = den = 0.0; n = 0
        for k, a in MK.items():
            c = (a['year'] if a.get('type') == 'MSD' else a['year'] + 1)
            if c != y or not (float(a.get('v0') or 0) > 0): continue
            yrs = a.get('yrs') or []
            vp = list(a.get('vpath') or []); van = BASE.get(k) or []
            for i in range(len(vp)):
                if i >= len(van) or van[i] is None or vp[i] is None: continue
                v = van[i]
                if v['C'] <= 0: continue
                vp[i] = v['v0eta'] - v['C'] * F(v['g'], SU[k].get(v['y']), v['age'], lam)
            if not yrs: v1 = 0.0
            elif y < yrs[0]: continue
            elif y > yrs[-1]: v1 = 0.0
            else:
                i = yrs.index(y); v1 = 0.0 if vp[i] is None else float(vp[i])
            num += v1; den += float(a['v0']); n += 1
        if den > 0 and n >= 5: per.append(num / den)
    w2 = sum(per) / len(per)
    # the pick correlation of the surplus
    from scipy.stats import rankdata
    nd = [(float(r['pick']), SU[r['key']].get(r['Y'])) for r in S2 if r['pick'] is not None
          and SU.get(r['key'], {}).get(r['Y']) is not None]
    x = np.array([a for a, _ in nd]); y = np.array([b for _, b in nd])
    rx, ry = rankdata(x), rankdata(y); rx = rx - rx.mean(); ry = ry - ry.mean()
    rho = float((rx * ry).sum() / math.sqrt((rx ** 2).sum() * (ry ** 2).sum()))
    P('   %-22s | %7.4f | %+7.2f%% %+7.2f%% | %+7.2f%% %+7.2f%% | %7.4f | %+7.4f' % (
        tag, lam, 100 * out['PRIMARY|1-10'], 100 * out['MODERN|1-10'],
        100 * out['PRIMARY|31-40'], 100 * out['PRIMARY|41-64'], w2, rho))
    return dict(tag=tag, note=note, LAMBDA=lam, s0=s0, s_p5=s5, bands=out, w2=w2, rho_pick=rho)


P('=' * 118)
P('ORDER P — THE DECLARED SENSITIVITIES, EACH RE-SOLVED FROM SCRATCH. ESTIMATES PENDING A BUILD.')
P('=' * 118)
P('   Each row below re-estimates the surface, re-solves LAMBDA by the anchoring identity, and')
P('   re-prices the board. Nothing is carried across from the primary run.')
P()
P('   %-22s | %7s | %8s %8s | %8s %8s | %7s | %8s' % (
    'surface', 'LAMBDA', 'p1-10 PRI', 'p1-10 MOD', 'p31-40', 'p41-64', 'W2', 'rho(pick,s)'))
P('   ' + '-' * 108)
OUT = []
for h in (0.25, 0.40, 0.60):
    g = PB.Premium(ROWS, h=h, iso=True)
    OUT.append(run('ln(v0), H=%.2f, iso' % h, (lambda gg: (lambda rec, cls: gg.at_v0(rec['v0'], cls)))(g),
                   'bandwidth sensitivity'))
g = PB.Premium(ROWS, h=0.40, iso=False)
OUT.append(run('ln(v0), H=0.40, RAW', (lambda gg: (lambda rec, cls: gg.at_v0(rec['v0'], cls)))(g),
               'monotonicity guard off'))
bp = BandPrem(ROWS)
OUT.append(run('pick band (not v0)', lambda rec, cls: bp.at(rec, cls), 'the axis not chosen'))
OUT.append(run('NO premium (= ORDER N)', lambda rec, cls: 0.0, 'the age-only bar, for reference'))
P()
P('   ORDER K for reference: picks 1-10 +8.22%% PRI / +13.65%% MOD · 31-40 -10.70%% · 41-64 -6.89%% · W2 1.0513')
P('   The +14%% buy rail is the line that matters on the first two columns.')
P()
json.dump(OUT, open(os.path.join(HERE, 'SENS_P.json'), 'w'), indent=1, default=float)
open(os.path.join(HERE, 'SENS_P_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote SENS_P.json and SENS_P_out.txt')
