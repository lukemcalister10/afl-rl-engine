import json, math, random
from collections import Counter, defaultdict
from a1_lib import load, pop, v4, H

random.seed(3341)
B = 20000

def stat(S):
    """value-weighted F0 = sum(discounted realized)/sum(v0)"""
    num = sum(v4(x) for x in S)/(H**4)
    den = sum(x['v0'] for x in S)
    return num/den

def effn(S):
    w = [x['v0'] for x in S]
    sw = sum(w); sw2 = sum(t*t for t in w)
    return sw*sw/sw2 if sw2 else 0.0

def boot(S, B=B):
    n = len(S)
    num = [v4(x)/(H**4) for x in S]
    den = [x['v0'] for x in S]
    out = []
    ri = random.randrange
    for _ in range(B):
        a = 0.0; b = 0.0
        for _ in range(n):
            j = ri(n); a += num[j]; b += den[j]
        out.append(a/b)
    out.sort()
    return out

def bca(S, reps):
    """bias-corrected accelerated 95% CI"""
    from statistics import NormalDist
    nd = NormalDist()
    th = stat(S)
    B = len(reps)
    nless = sum(1 for t in reps if t < th)
    if nless == 0: nless = 1
    if nless == B: nless = B-1
    z0 = nd.inv_cdf(nless/B)
    # jackknife
    n = len(S)
    num = [v4(x)/(H**4) for x in S]
    den = [x['v0'] for x in S]
    tn = sum(num); td = sum(den)
    jk = [(tn-num[i])/(td-den[i]) for i in range(n)]
    m = sum(jk)/n
    d = [m-t for t in jk]
    s2 = sum(t*t for t in d); s3 = sum(t**3 for t in d)
    a = s3/(6*(s2**1.5)) if s2 > 0 else 0.0
    res = []
    for alpha in (0.025, 0.975):
        za = nd.inv_cdf(alpha)
        adj = z0 + (z0+za)/(1-a*(z0+za))
        p = nd.cdf(adj)
        p = min(max(p, 1.0/B), 1-1.0/B)
        res.append(reps[int(p*(B-1))])
    return res

def clusterboot(S, keyfn, B=8000):
    groups = defaultdict(list)
    for x in S:
        groups[keyfn(x)].append(x)
    gl = list(groups.values())
    gn = [sum(v4(x) for x in g)/(H**4) for g in gl]
    gd = [sum(x['v0'] for x in g) for g in gl]
    G = len(gl); out = []
    ri = random.randrange
    for _ in range(B):
        a = 0.0; b = 0.0
        for _ in range(G):
            j = ri(G); a += gn[j]; b += gd[j]
        if b: out.append(a/b)
    out.sort()
    return out[int(0.025*len(out))], out[int(0.975*len(out))]

def cell(S, label, minn=8):
    if len(S) < minn:
        return None
    f = stat(S)
    reps = boot(S)
    lo, hi = bca(S, reps)
    clo, chi = clusterboot(S, lambda x: x['year'])
    totv0 = sum(x['v0'] for x in S)
    totre = sum(v4(x) for x in S)/(H**4)
    miss_total = totv0 - totre           # positive = overpriced
    miss_per = miss_total/len(S)
    verdict = 'OVERPRICED' if hi < 1 else ('UNDERPRICED' if lo > 1 else 'honest')
    cver = 'OVER' if chi < 1 else ('UNDER' if clo > 1 else 'honest')
    return dict(cell=label, n=len(S), effn=round(effn(S), 1), F0=round(f, 4),
                lo=round(lo, 4), hi=round(hi, 4), verdict=verdict,
                clo=round(clo, 4), chi=round(chi, 4), cver=cver,
                mean_v0=round(totv0/len(S), 1),
                miss_per=round(miss_per, 1), miss_total=round(miss_total, 0))

def ageband(a):
    if a is None: return 'unk'
    if a <= 18: return '<=18'
    if a <= 20: return '19-20'
    return '21+'

def pickband(p):
    if p is None: return None
    if p <= 3: return '1-3'
    if p <= 10: return '4-10'
    if p <= 20: return '11-20'
    if p <= 40: return '21-40'
    if p <= 64: return '41-64'
    return '65+'

POS = ['MID', 'SD', 'SF', 'KPF', 'KPD', 'RUCK']
