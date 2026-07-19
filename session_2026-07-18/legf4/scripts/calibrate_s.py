#!/usr/bin/env python3
# LEG F4 — CALIBRATE s(age) in-process (fast; no board build): solve the geometric-blend coefficient s(a) so
# the DAMPED forward transition median(vP1/v) per age == the sealed r_pop(a). The damper reads _LSYM_TAB['s']
# live, so we bisect s per age by mutating the dict and recomputing ev. s is the deterministic coefficient
# reproducing the sealed measured rate (Reid); NOT iterated against a backtest.
import json, io, contextlib, statistics as st
from collections import defaultdict
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA = g['MA']; ev = g['ev']; TAB = g['_LSYM_TAB']; lsym_age = g['_lsym_age']
players = g['MA'].__dict__['players']
rpop = {int(k): v for k, v in TAB['r_pop'].items()}
def rp(a): return rpop[a] if a in rpop else rpop[min(rpop, key=lambda x: abs(x - a))]

def now_v(p):
    MA._LENS_FORM = None; MA.BASE_REF = MA.AGE_REF = 2026; MA._pe_clear()
    return ev(p, 2026)
def fwd_v(p):
    MA._LENS_FORM = 2026; MA.AGE_REF = 2027; MA.BASE_REF = 2026; MA._pe_clear()
    r = ev(p, 2027); MA._LENS_FORM = None; MA.BASE_REF = MA.AGE_REF = 2026; MA._pe_clear(); return r

# group players by draft-year age; precompute now-v
by_age = defaultdict(list)
for p in players:
    v = now_v(p)
    if v > 50: by_age[lsym_age(p)].append((p, v))

def emergent(a, s):
    TAB['s'][str(a)] = s
    rr = [fwd_v(p) / v for p, v in by_age[a]]
    return st.median(rr) if rr else 1.0

sol = {}
for a in sorted(by_age):
    tgt = rp(a); n = len(by_age[a])
    e1 = emergent(a, 1.0)          # full modeled (max decline)
    e0 = emergent(a, 0.0)          # form-anchored (min decline)
    if tgt >= e0:                  # target shallower than even s=0 can reach -> clamp 0 (no further lift available)
        s = 0.0
    elif tgt <= e1:                # target steeper than s=1 -> clamp 1 (blend cannot amplify)
        s = 1.0
    else:
        lo, hi = 0.0, 1.0
        for _ in range(24):
            mid = 0.5 * (lo + hi); em = emergent(a, mid)
            if em > tgt: lo = mid  # too shallow (ratio too high) -> more decline -> higher s
            else: hi = mid
        s = 0.5 * (lo + hi)
    sol[a] = round(s, 4)
    TAB['s'][str(a)] = sol[a]
    print("  age %2d n=%3d  target %.4f  s=%.4f  emergent@s=%.4f  (s0=%.3f s1=%.3f)" % (a, n, tgt, sol[a], emergent(a, sol[a]), e0, e1))

# write solved s
doc = json.load(open('lsym_rate.json'))
import hashlib
doc['s'] = {str(a): sol[a] for a in sorted(sol)}
doc['s_sha256_8'] = hashlib.sha256(json.dumps(doc['s'], sort_keys=True).encode()).hexdigest()[:8]
doc['s_derivation'] = ('s(a) = the geometric-blend coefficient bisected in-process so the DAMPED median(vP1/v) '
    'per draft-year age == the sealed r_pop(a) (24-iter bisection; clamped [0,1], no blend amplification). '
    'Deterministic solution of the sealed rate constraint (Reid); NOT iterated against any backtest.')
json.dump(doc, open('lsym_rate.json', 'w'), indent=1, sort_keys=True)
print("s_sha256_8:", doc['s_sha256_8'])
