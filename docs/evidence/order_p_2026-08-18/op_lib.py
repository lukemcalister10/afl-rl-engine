#!/usr/bin/env python3
"""ORDER P — the shared constructions. READ-ONLY. No engine import, no board build, no store write.

ORDER N's on_lib.py is imported whole and NOT re-implemented: the age bar, the performance surplus,
the house delivered-value ruler, the matrices, the eta charge, the bins. Everything in this file is
the ONE new object PREREG_P.md section 3.3 fixes:

  PG(x, class)   -- the PEDIGREE PREMIUM. How far above his age bar a player priced at v0 = e^x
                    actually produces, measured on realised per-game production, games-weighted,
                    by local-linear kernel regression on ln(v0), tricube, bandwidth H.
  BAR_P          -- bar(pos, age) + PG(ln v0, class)
  perf_surplus_P -- the games-weighted mean distance from BAR_P

Nothing here reads a board price except v0, which is the pedigree LABEL (prereg 2.2, bound P-F3).
"""
import json, math, os, sys, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
ORDER_N = os.path.join(REPO, 'docs/evidence/order_n_2026-08-18')
sys.path.insert(0, ORDER_N)
import on_lib as LB                                                          # noqa: E402

SP = LB.SP
H_PRIMARY = 0.40                 # prereg 3.3: bandwidth in log-v0 units
H_SENS = (0.25, 0.60)
AGE_LO, AGE_HI = 18, 23          # the ages the C3 surface has content at
GRID_N = 121                     # evaluation grid points over the 1-99 pct of ln(v0)
ESS_THIN = 30.0


# ---- the estimator -----------------------------------------------------------------------------------
def tricube(u):
    u = np.abs(u)
    out = np.zeros_like(u)
    m = u < 1.0
    out[m] = (1.0 - u[m] ** 3) ** 3
    return out


def loclin(x0, xs, ys, ws, h):
    """Games-weighted local-linear kernel regression, tricube. Returns (fit, ESS).

    Same estimator family par_build.py used over log-pick (its loclin, bandwidth H_LOGPICK = 0.40),
    used here over log-v0 deliberately, so the comparison with the deleted object is like-for-like."""
    k = tricube((xs - x0) / h) * ws
    ess = float(k.sum() ** 2 / max(1e-12, (k ** 2).sum())) if k.sum() > 0 else 0.0
    if k.sum() <= 0:
        return float('nan'), 0.0
    d = xs - x0
    S0 = k.sum(); S1 = (k * d).sum(); S2 = (k * d * d).sum()
    T0 = (k * ys).sum(); T1 = (k * d * ys).sum()
    den = S0 * S2 - S1 * S1
    if abs(den) < 1e-12 * max(1.0, S0 * S2):
        return float(T0 / S0), ess
    return float((S2 * T0 - S1 * T1) / den), ess


def isotonize_up(y):
    """Pool-adjacent-violators, non-decreasing. The house instrument's own law, written out so this
    file carries no new dependency; asserted against sklearn where sklearn is importable."""
    y = list(map(float, y))
    n = len(y)
    val = []; wt = []
    for v in y:
        val.append(v); wt.append(1.0)
        while len(val) > 1 and val[-2] > val[-1]:
            v2 = val.pop(); w2 = wt.pop()
            v1 = val.pop(); w1 = wt.pop()
            val.append((v1 * w1 + v2 * w2) / (w1 + w2)); wt.append(w1 + w2)
    out = []
    for v, w in zip(val, wt):
        out.extend([v] * int(round(w)))
    assert len(out) == n
    return np.array(out)


# ---- the season-row population ------------------------------------------------------------------------
def season_rows(M, age_lo=AGE_LO, age_hi=AGE_HI):
    """PREREG_P 3.3: every season with games>0 played at age 18-23 by an entrant from 2005 on."""
    out = []
    for k, r in M.items():
        if k in LB.FM:
            continue
        if (r.get('year') or 0) < LB.ENTRY_FLOOR:
            continue
        v0 = float(r.get('v0') or 0.0)
        if not (v0 > 0):
            continue
        cg = 0.0
        for s in sorted(r['seasons'], key=lambda z: z['year']):
            g = float(s.get('games') or 0.0)
            if g <= 0:
                continue
            pre = cg                       # career games BEFORE this season
            cg += g
            if s['year'] > LB.LAST_REAL_SEASON:
                continue
            pos = s.get('bar')
            if pos not in LB.BARS or s.get('avg') is None:
                continue
            a = LB.age_at(r, s['year'])
            if a is None or a < age_lo or a > age_hi:
                continue
            b = LB.bar(pos, a)
            out.append(dict(key=k, year=s['year'], age=a, games=g, avg=float(s['avg']), pos=pos,
                            cls=('TALL' if pos in LB.TALLPOS else 'SMALL'),
                            v0=v0, x=math.log(v0), d=float(s['avg']) - b,
                            cg_before=pre, cg_after=cg,
                            pick=(r.get('pick') if r.get('type') == 'ND' else None),
                            band=LB.band_of(r.get('pick') if r.get('type') == 'ND' else None),
                            typ=r.get('type')))
    return out


# ---- the surface --------------------------------------------------------------------------------------
class Premium(object):
    """PG(x, class): the fitted, bounded, monotone pedigree premium in points per game."""

    def __init__(self, rows, h=H_PRIMARY, iso=True, grid_n=GRID_N):
        self.h = h; self.iso = iso
        self.grid = {}; self.raw = {}; self.ess = {}; self.lo = {}; self.hi = {}
        self.n = {}
        for cls in ('TALL', 'SMALL'):
            sub = [r for r in rows if r['cls'] == cls]
            xs = np.array([r['x'] for r in sub]); ys = np.array([r['d'] for r in sub])
            ws = np.array([r['games'] for r in sub])
            lo = float(np.percentile(xs, 1)); hi = float(np.percentile(xs, 99))
            gx = np.linspace(lo, hi, grid_n)
            fit = np.zeros(grid_n); ess = np.zeros(grid_n)
            for i, x0 in enumerate(gx):
                fit[i], ess[i] = loclin(x0, xs, ys, ws, h)
            self.raw[cls] = fit.copy()
            self.grid[cls] = (gx, isotonize_up(fit) if iso else fit)
            self.ess[cls] = ess
            self.lo[cls] = lo; self.hi[cls] = hi
            self.n[cls] = len(sub)

    def at(self, x, cls):
        gx, gy = self.grid[cls]
        return float(np.interp(min(max(x, gx[0]), gx[-1]), gx, gy))   # HELD FLAT outside support

    def at_v0(self, v0, cls):
        return self.at(math.log(max(1e-9, float(v0))), cls)

    def bar_p(self, pos, age, v0):
        cls = 'TALL' if pos in LB.TALLPOS else 'SMALL'
        b = LB.bar(pos, age)
        return None if b is None else b + self.at_v0(v0, cls)


def perf_surplus_P(rec, Y, PG):
    """PREREG_P 3.4. Games-weighted mean of (avg - BAR_P). None when no played season up to Y."""
    ss = LB.seasons_upto(rec, Y)
    if not ss:
        return None
    v0 = float(rec.get('v0') or 0.0)
    if not (v0 > 0):
        return None
    num = den = 0.0
    for s in ss:
        a = LB.age_at(rec, s['year'])
        pos = s.get('bar')
        bp = PG.bar_p(pos, a, v0) if pos in LB.BARS else None
        if bp is None or s.get('avg') is None:
            return None
        g = float(s['games'])
        num += g * (float(s['avg']) - bp)
        den += g
    return num / den if den > 0 else None


def premium_of(rec, PG):
    """The single shift between ORDER N's surplus and ORDER P's, for this row. s_P = s_N - premium.

    It is a per-PLAYER constant because the age level is already carried by bar(pos, age) and the
    premium does not depend on the season. For a row that changes position class mid-career the
    games-weighted mix is used, which is why this is computed rather than looked up."""
    ss = [s for s in rec['seasons'] if (s.get('games') or 0) > 0 and s.get('bar') in LB.BARS]
    if not ss:
        return None
    v0 = float(rec.get('v0') or 0.0)
    num = den = 0.0
    for s in ss:
        cls = 'TALL' if s['bar'] in LB.TALLPOS else 'SMALL'
        g = float(s['games'])
        num += g * PG.at_v0(v0, cls); den += g
    return num / den if den > 0 else None
