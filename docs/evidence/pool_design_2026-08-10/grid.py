"""Agent 9 — pool design measurement. READ-ONLY.

F0 (year-0 honesty, stage4_amend1 matrix) = sum(vpath[3])/H^4 / sum(v0)      [busts -> 0 numerator, kept in denominator]
F1 (year-1,          stage5 landed matrix) = sum(vpath[3])/H^3 / sum(vpath[0])
H = 1.0939.  Pool = every non-ND-1-64 entrant.  Classes 2004-2022.
Both reproduce the published seam figures to 4dp (validated separately).
"""
import json, math, sys
import numpy as np
from statistics import NormalDist

ND_ = NormalDist()
H = 1.0939
B = 20000
SD = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/"

A = json.load(open(SD + "s4a1.json"))["recs"]
S5 = json.load(open(SD + "s5.json"))["recs"]
key = lambda r: (r["key"], r["type"], r["year"])
M5 = {key(r): r for r in S5}

POOL = [r for r in A if r["is_pool"] and 2004 <= r["year"] <= 2022]

def fut(r):
    vp = r.get("vpath") or []
    return float(vp[3]) if len(vp) >= 4 and vp[3] is not None else 0.0

ROWS = []
drop0 = []
for r in POOL:
    b = M5.get(key(r))
    v0 = float(r["v0"] or 0.0)
    p1 = float((b["vpath"][0] if b and b.get("vpath") else 0.0) or 0.0)
    if v0 <= 0 or p1 <= 0:
        drop0.append((r["player"], r["type"], r["year"], v0, p1))
        continue
    ag = r.get("age_draft")
    if ag is None:
        ab = "unk"
    elif ag <= 18:
        ab = "<=18"
    elif ag <= 20:
        ab = "19-20"
    elif ag <= 22:
        ab = "21-22"
    elif ag <= 24:
        ab = "23-24"
    else:
        ab = "25+"
    rt = r["type"]
    if rt == "ND":
        rt = "ND65+"
    if rt in ("PDA", "PDN", "PDS"):
        rt = "PSD"          # pre-season/ pre-draft selection family, pooled (disclosed)
    ROWS.append(dict(
        key=r["key"], player=r["player"], route=rt, raw_route=r["type"], pos=r["pos"],
        age=r.get("age_draft"), ageb=ab, yr=r["year"],
        n0=fut(r) / H ** 4, d0=v0,
        n1=fut(b) / H ** 3, d1=p1,
        gy1=r.get("games_yr1") or 0,
    ))

N0 = np.array([x["n0"] for x in ROWS]); D0 = np.array([x["d0"] for x in ROWS])
N1 = np.array([x["n1"] for x in ROWS]); D1 = np.array([x["d1"] for x in ROWS])
YR = np.array([x["yr"] for x in ROWS])

def kish(w):
    w = np.asarray(w, float)
    return (w.sum() ** 2) / (w ** 2).sum() if w.sum() > 0 else 0.0

def bca(num, den, rng, clusters=None):
    """BCa CI for ratio-of-sums. clusters=None -> player resample; else cluster resample."""
    n = len(num)
    if n < 3:
        return (float("nan"), float("nan"))
    th = num.sum() / den.sum()
    if clusters is None:
        reps = np.empty(B)
        step = 2000
        for s in range(0, B, step):
            k = min(step, B - s)
            idx = rng.integers(0, n, size=(k, n))
            reps[s:s + k] = num[idx].sum(1) / den[idx].sum(1)
    else:
        uc = np.unique(clusters)
        groups = [np.where(clusters == c)[0] for c in uc]
        gn = np.array([num[g].sum() for g in groups])
        gd = np.array([den[g].sum() for g in groups])
        m = len(uc)
        if m < 3:
            return (float("nan"), float("nan"))
        idx = rng.integers(0, m, size=(B, m))
        reps = gn[idx].sum(1) / gd[idx].sum(1)
    # bias correction
    p = (reps < th).mean()
    p = min(max(p, 1.0 / (2 * B)), 1 - 1.0 / (2 * B))
    z0 = ND_.inv_cdf(p)
    # jackknife acceleration (on the resampling unit)
    if clusters is None:
        tn, td = num.sum(), den.sum()
        jk = (tn - num) / (td - den)
    else:
        tn, td = gn.sum(), gd.sum()
        jk = (tn - gn) / (td - gd)
    jm = jk.mean(); dv = jm - jk
    s2 = (dv ** 2).sum()
    a = (dv ** 3).sum() / (6.0 * s2 ** 1.5) if s2 > 0 else 0.0
    out = []
    for zq in (ND_.inv_cdf(0.025), ND_.inv_cdf(0.975)):
        z = z0 + (z0 + zq) / (1 - a * (z0 + zq)) if abs(1 - a * (z0 + zq)) > 1e-12 else z0 + zq
        q = ND_.cdf(z)
        out.append(float(np.quantile(reps, min(max(q, 1e-6), 1 - 1e-6))))
    return tuple(out)

def cell(mask, label, rng):
    idx = np.where(mask)[0]
    n = len(idx)
    if n == 0:
        return None
    f0 = N0[idx].sum() / D0[idx].sum()
    f1 = N1[idx].sum() / D1[idx].sum()
    e0 = kish(D0[idx]); e1 = kish(D1[idx])
    c0 = bca(N0[idx], D0[idx], rng)
    c1 = bca(N1[idx], D1[idx], rng)
    k0 = bca(N0[idx], D0[idx], rng, YR[idx])
    k1 = bca(N1[idx], D1[idx], rng, YR[idx])
    return dict(label=label, n=n, f0=f0, f1=f1, effn0=e0, effn1=e1,
                ci0=c0, ci1=c1, kci0=k0, kci1=k1,
                nclass=int(len(np.unique(YR[idx]))))

def clear(ci):
    lo, hi = ci
    if any(math.isnan(v) for v in (lo, hi)):
        return None
    return (lo > 1.0) or (hi < 1.0)

rng = np.random.default_rng(20260810)

route = np.array([x["route"] for x in ROWS])
pos = np.array([x["pos"] for x in ROWS])
ageb = np.array([x["ageb"] for x in ROWS])

ROUTES = ["RD", "ND65+", "MSD", "UNR", "IRE", "SSP", "PSD"]
POSS = ["MID", "SD", "SF", "KPF", "KPD", "RUCK"]
AGES = ["<=18", "19-20", "21-22", "23-24", "25+", "unk"]

results = {"drop0": drop0, "n_pool_rows": len(ROWS)}

def emit(tag, cells):
    results[tag] = [c for c in cells if c]

# ---- Level 3: full route x pos x age
lvl3 = []
for rt in ROUTES:
    for ps in POSS:
        for ab in AGES:
            m = (route == rt) & (pos == ps) & (ageb == ab)
            if m.sum() == 0:
                continue
            idx = np.where(m)[0]
            e0 = kish(D0[idx]); e1 = kish(D1[idx])
            if max(e0, e1) >= 20:      # only bootstrap plausible cells
                lvl3.append(cell(m, f"{rt} x {ps} x {ab}", rng))
            else:
                lvl3.append(dict(label=f"{rt} x {ps} x {ab}", n=int(m.sum()),
                                 f0=float(N0[idx].sum() / D0[idx].sum()),
                                 f1=float(N1[idx].sum() / D1[idx].sum()),
                                 effn0=e0, effn1=e1, ci0=(float('nan'),) * 2,
                                 ci1=(float('nan'),) * 2, kci0=(float('nan'),) * 2,
                                 kci1=(float('nan'),) * 2,
                                 nclass=int(len(np.unique(YR[idx]))), thin=True))
emit("lvl3", lvl3)

# ---- Level 2 pooled axes
emit("route_x_age", [cell((route == rt) & (ageb == ab), f"{rt} x {ab}", rng)
                     for rt in ROUTES for ab in AGES if ((route == rt) & (ageb == ab)).sum()])
emit("route_x_pos", [cell((route == rt) & (pos == ps), f"{rt} x {ps}", rng)
                     for rt in ROUTES for ps in POSS if ((route == rt) & (pos == ps)).sum()])
emit("pos_x_age", [cell((pos == ps) & (ageb == ab), f"{ps} x {ab}", rng)
                   for ps in POSS for ab in AGES if ((pos == ps) & (ageb == ab)).sum()])

# ---- Level 1 marginals
emit("route", [cell(route == rt, rt, rng) for rt in ROUTES])
emit("pos", [cell(pos == ps, ps, rng) for ps in POSS])
emit("age", [cell(ageb == ab, ab, rng) for ab in AGES])
emit("all", [cell(np.ones(len(ROWS), bool), "WHOLE POOL", rng)])

# ---- mature (21+) sub-grid, the owner's live question
mat = np.isin(ageb, ["21-22", "23-24", "25+"])
young = np.isin(ageb, ["<=18", "19-20"])
emit("mature", [cell(mat, "mature pool 21+", rng)] +
    [cell(mat & (route == rt), f"mature x {rt}", rng) for rt in ROUTES if (mat & (route == rt)).sum()] +
    [cell(mat & (pos == ps), f"mature x {ps}", rng) for ps in POSS if (mat & (pos == ps)).sum()])
emit("young", [cell(young, "young pool <=20", rng)] +
    [cell(young & (route == rt), f"young x {rt}", rng) for rt in ROUTES if (young & (route == rt)).sum()])

# ---- the headline three-way the law points at: mature x route x running/tall
RUN = np.isin(pos, ["MID", "SD", "SF"]); TALL = np.isin(pos, ["KPF", "KPD", "RUCK"])
emit("mature_shape", [
    cell(mat & RUN, "mature x RUNNING(MID/SD/SF)", rng),
    cell(mat & TALL, "mature x TALL(KPF/KPD/RUCK)", rng),
    cell(mat & (route == "RD") & RUN, "mature x RD x RUNNING", rng),
    cell(mat & (route == "RD") & TALL, "mature x RD x TALL", rng),
    cell(mat & (route != "RD") & RUN, "mature x non-RD x RUNNING", rng),
    cell(mat & (route != "RD") & TALL, "mature x non-RD x TALL", rng),
    cell(young & RUN, "young x RUNNING", rng),
    cell(young & TALL, "young x TALL", rng),
])

# ---- single-year age slope (no-cliff check), pooled over route/pos
slope = []
for a in range(17, 30):
    m = np.array([x["age"] == a for x in ROWS])
    if m.sum() == 0:
        continue
    slope.append(cell(m, f"age {a}", rng))
emit("age_slope", slope)

json.dump(results, open(SD + "grid_out.json", "w"), indent=1, default=float)
print("rows", len(ROWS), "dropped", len(drop0))
for d in drop0:
    print("  DROP", d)
