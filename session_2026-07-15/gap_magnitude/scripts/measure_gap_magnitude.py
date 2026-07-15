#!/usr/bin/env python3
"""GAP-LENGTH MAGNITUDE MEASUREMENT (register item 122b; feeds parked R100.11 assumption 1).

READ-ONLY. Measures whether the DATA show longer mid-career absences produce larger post-return
level shortfalls, controlling for age at return via the SHIPPED absence age-curve.

BASE PIN: analysis at the candidate line head 62352729ec3523cec4bb117e713e1bec67a0d490
(branch claude/absence-penalty-evidence-fade-glcl8b). Store md5 340a7a32 == Guard-5 pin.

The absence-detection logic (_abs_gap) is copied VERBATIM from that head's
engine/rl_after/_merged_recover.py; the age-control curve (_ABS_AGE/_ABS_EFF) is the shipped
constant at :370-371; the fraction map (_abs_frac) at :383-388. cp.debutyr / MA.age reproduce
forward_valuation/conditional_prior.py:20 + rl_model.py:59-62.

NOTHING is written outside session_2026-07-15/gap_magnitude/. No store/engine/board is mutated.
"""
import io, contextlib, json, math, os
import numpy as np
from scipy import stats

with contextlib.redirect_stdout(io.StringIO()):
    import rl_model as MA   # workspace rl_model; loads store rl_model_data.json (md5 340a7a32 == head)

# ---- helpers reproducing the engine spine (cited) -------------------------------------------
def debutyr(p):  # conditional_prior.py:20 / rl_model.py:63 (verbatim)
    return p['year'] if p['type'] == 'MSD' else p['year'] + 1

def age_2026(p):  # MA.age(p) == _age_at(p, AGE_REF=2026); returns None-safe int
    return MA.age(p)

def isreal(p):  # engine _isreal: a real store row (not a synth). Store rows all carry 'key'.
    return True

# ---- SHIPPED absence age-curve, VERBATIM from head _merged_recover.py:370-371 ----------------
_ABS_AGE = [18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34]
_ABS_EFF = [3.65,0.28,-2.51,-4.49,-5.55,-5.73,-5.25,-4.46,-3.71,-3.25,-3.25,-3.85,-5.14,-7.10,-9.39,-11.29,-11.88]
_ABS_L_REF = 75.0    # :357
_ABS_CAP   = 0.20    # :358

def abs_pred_pts(age):
    """Age-curve predicted absence penalty in LEVEL POINTS (the |eff| the shipped _abs_frac uses
    before /_ABS_L_REF and the cap). max(0,-eff) == 'an absence is never a bonus' clamp (:372)."""
    if age is None:
        return 0.0
    a = float(np.clip(age, _ABS_AGE[0], _ABS_AGE[-1]))
    eff = float(np.interp(a, _ABS_AGE, _ABS_EFF))
    return max(0.0, -eff)

def abs_frac(age):  # shipped _abs_frac, :383-388 (verbatim), for reference/attribution
    if age is None:
        return 0.0
    a = float(np.clip(age, _ABS_AGE[0], _ABS_AGE[-1]))
    eff = float(np.interp(a, _ABS_AGE, _ABS_EFF))
    return float(np.clip(max(0.0, -eff)/_ABS_L_REF, 0.0, _ABS_CAP))

# ---- _abs_gap, copied VERBATIM from head _merged_recover.py (return-year <= Y most-recent gap)-
def _abs_gap(p, Y):
    d0 = debutyr(p)
    rows = {x['year']: x['games'] for x in p['scoring'] if (d0-1) < x['year']}
    yrs = [y for y, gmv in rows.items() if gmv > 0]
    if len(yrs) < 2:
        return None
    lo, hi = min(yrs), max(yrs)
    tl = [(y, rows.get(y, 0)) for y in range(lo, hi+1)]
    best = None; i = 0
    while i < len(tl):
        if tl[i][1] != 0:
            i += 1; continue
        prior = [yy for (yy, g2) in tl[:i] if g2 > 0]; j = i
        while j < len(tl) and tl[j][1] == 0:
            j += 1
        if prior and j < len(tl):
            ret = tl[j][0]
            if ret <= Y:
                last = prior[-1]; a = age_2026(p)
                age_pre = (a - (2026-last)) if a is not None else None
                npost = sum(1 for x in p['scoring'] if x['games'] >= 10 and x['year'] > ret and (d0-1) < x['year'] <= Y)
                gpost = sum(x['games'] for x in p['scoring'] if x['games'] > 0 and x['year'] >= ret and (d0-1) < x['year'] <= Y)
                best = dict(age_pre=age_pre, ret=ret, last=last, npost=npost, gpost=gpost)
        i = j
    return best

# ---- realised level measurement -------------------------------------------------------------
Y = 2026
QUAL_G = 6   # qualifying-season games bar (the engine's >=6g demonstrated-level bar)

def gwt_mean(seasons):
    """games-weighted mean avg over a list of (year,games,avg)."""
    tw = sum(g for _, g, _ in seasons)
    return (sum(g*a for _, g, a in seasons)/tw) if tw > 0 else None

def pre_level(p, gi, win=2):
    """games-weighted mean of up to `win` most-recent PRE-gap qualifying (>=6g) seasons (<= last).
    Returns (level, qualified): qualified=True iff a >=6g pre-gap season backed it (no cameo fallback)."""
    d0 = debutyr(p); last = gi['last']
    qs = [(x['year'], x['games'], x['avg']) for x in p['scoring']
          if x['games'] >= QUAL_G and (d0-1) < x['year'] <= last]
    qs.sort(key=lambda t: t[0], reverse=True)
    qs = qs[:win]
    if qs:
        return gwt_mean(qs), True
    qs = [(x['year'], x['games'], x['avg']) for x in p['scoring']   # fallback: sub-6g cameo baseline
          if x['games'] > 0 and (d0-1) < x['year'] <= last]
    return gwt_mean(qs), False

def post_level(p, gi, first_only=False):
    """games-weighted mean of POST-return qualifying (>=6g) seasons (year>=ret).
    Returns (level, qualified). first_only -> first qualifying (or first played) season only."""
    ret = gi['ret']
    qs = [(x['year'], x['games'], x['avg']) for x in p['scoring']
          if x['games'] >= QUAL_G and ret <= x['year'] <= Y]
    qs.sort(key=lambda t: t[0])
    qual = bool(qs)
    if not qs:  # fallback: any post-return played season (sub-6g cameo)
        qs = [(x['year'], x['games'], x['avg']) for x in p['scoring']
              if x['games'] > 0 and ret <= x['year'] <= Y]
        qs.sort(key=lambda t: t[0])
    if first_only and qs:
        qs = qs[:1]
    return gwt_mean(qs), qual

# ---- build the population --------------------------------------------------------------------
recs = []
for p in MA.data:
    gi = _abs_gap(p, Y)
    if gi is None or gi['age_pre'] is None:
        continue
    glen = gi['ret'] - gi['last'] - 1   # number of missed seasons (>=1 by construction)
    Lpre, pre_q = pre_level(p, gi)
    Lpost, post_q = post_level(p, gi)
    Lpost1, _ = post_level(p, gi, first_only=True)
    if Lpre is None or Lpost is None:
        continue
    age_pre = gi['age_pre']
    age_ret = age_pre + glen + 1   # age at the return season
    pred = abs_pred_pts(age_pre)
    shortfall = Lpre - Lpost              # positive = realised drop below pre-absence level
    resid = shortfall - pred              # age-adjusted (curve is pooled across gap lengths)
    recs.append(dict(
        player=p.get('player'), pos=p.get('drafted_position'), type=p.get('type'),
        last=gi['last'], ret=gi['ret'], glen=glen,
        age_pre=age_pre, age_ret=age_ret, gpost=gi['gpost'], npost=gi['npost'],
        Lpre=round(Lpre, 2), Lpost=round(Lpost, 2), Lpost1=round(Lpost1, 2) if Lpost1 else None,
        pred_pts=round(pred, 2), shortfall=round(shortfall, 2), resid=round(resid, 2),
        qualified=bool(pre_q and post_q),   # both endpoints rest on a >=6g season (clean baseline)
    ))

def bucket(glen):
    return '1' if glen == 1 else ('2' if glen == 2 else '3+')

for r in recs:
    r['bucket'] = bucket(r['glen'])

# ---- bucket statistics -----------------------------------------------------------------------
def ci95(x):
    x = np.asarray(x, float); n = len(x)
    if n == 0:
        return (None, None, None, None)
    m = float(np.mean(x)); sd = float(np.std(x, ddof=1)) if n > 1 else 0.0
    se = sd/math.sqrt(n) if n > 0 else 0.0
    if n > 1:
        h = stats.t.ppf(0.975, n-1)*se
    else:
        h = float('nan')
    return (m, m-h, m+h, sd)

def build_summary(pool):
    S = {}
    for b in buckets:
        sub = [r for r in pool if r['bucket'] == b]
        sf = [r['shortfall'] for r in sub]; rs = [r['resid'] for r in sub]; ap = [r['age_pre'] for r in sub]
        m_sf, lo_sf, hi_sf, sd_sf = ci95(sf); m_rs, lo_rs, hi_rs, sd_rs = ci95(rs)
        S[b] = dict(n=len(sub), mean_shortfall=m_sf, sf_ci=(lo_sf, hi_sf), sf_sd=sd_sf,
                    mean_resid=m_rs, resid_ci=(lo_rs, hi_rs), resid_sd=sd_rs,
                    mean_age_pre=float(np.mean(ap)) if ap else None,
                    mean_pred=float(np.mean([r['pred_pts'] for r in sub])) if sub else None)
    return S

def build_sep(pool):
    sp = {}
    g1s = [r['shortfall'] for r in pool if r['bucket'] == '1']; g3s = [r['shortfall'] for r in pool if r['bucket'] == '3+']
    g1r = [r['resid'] for r in pool if r['bucket'] == '1']; g3r = [r['resid'] for r in pool if r['bucket'] == '3+']
    g2r = [r['resid'] for r in pool if r['bucket'] == '2']
    sp['shortfall_3plus_vs_1'] = welch(g3s, g1s); sp['resid_3plus_vs_1'] = welch(g3r, g1r)
    sp['resid_2_vs_1'] = welch(g2r, g1r)
    gl = [r['glen'] for r in pool]; rr = [r['resid'] for r in pool]; ss = [r['shortfall'] for r in pool]
    rho, prho = stats.spearmanr(gl, rr); rho2, prho2 = stats.spearmanr(gl, ss)
    sp['spearman_glen_resid'] = dict(rho=float(rho), p=float(prho))
    sp['spearman_glen_shortfall'] = dict(rho=float(rho2), p=float(prho2))
    return sp

# ---- separation tests: Welch two-sample (defined before the summary builders call it) --------
def welch(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    if len(a) < 2 or len(b) < 2:
        return None
    t, pp = stats.ttest_ind(a, b, equal_var=False)
    return dict(t=float(t), p_two=float(pp), p_one=float(pp/2 if t > 0 else 1-pp/2),
                mean_diff=float(np.mean(a)-np.mean(b)))

buckets = ['1', '2', '3+']
qual = [r for r in recs if r['qualified']]   # clean subset: both endpoints rest on a >=6g season
summary = build_summary(recs)
summary_q = build_summary(qual)
sep = build_sep(recs)
sep_q = build_sep(qual)

out = dict(
    head='62352729ec3523cec4bb117e713e1bec67a0d490',
    store_md5='340a7a32', Y=Y, QUAL_G=QUAL_G,
    n_total=len(recs), n_qualified=len(qual),
    bucket_counts={b: summary[b]['n'] for b in buckets},
    bucket_counts_qualified={b: summary_q[b]['n'] for b in buckets},
    summary=summary, summary_qualified=summary_q,
    separation=sep, separation_qualified=sep_q,
    records=sorted(recs, key=lambda r: (r['glen'], -r['shortfall'])),
)

OUTDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(OUTDIR, 'gap_magnitude.json'), 'w') as f:
    json.dump(out, f, indent=2, default=str)

# ---- console report --------------------------------------------------------------------------
def fmt(m, lo, hi):
    if m is None: return 'n/a'
    if lo is None or (isinstance(lo, float) and math.isnan(lo)): return f"{m:6.2f} [single]"
    return f"{m:6.2f} [{lo:6.2f},{hi:6.2f}]"

def report_view(name, S, SP):
    print(f"=== {name} ===")
    print(f"{'bkt':>4} {'n':>3} {'age_pre':>7} {'pred':>6} {'shortfall (95% CI)':>26} {'age-adj resid (95% CI)':>26}")
    for b in buckets:
        s = S[b]
        if s['n'] == 0:
            print(f"{b:>4} {0:>3}  (empty)"); continue
        print(f"{b:>4} {s['n']:>3} {s['mean_age_pre']:>7.1f} {s['mean_pred']:>6.2f} "
              f"{fmt(s['mean_shortfall'], *s['sf_ci']):>26} {fmt(s['mean_resid'], *s['resid_ci']):>26}")
    print("  SEPARATION:")
    for k in ('shortfall_3plus_vs_1', 'resid_3plus_vs_1', 'resid_2_vs_1'):
        v = SP[k]
        if v is None:
            print(f"    {k}: insufficient n")
        else:
            print(f"    {k}: mean_diff={v['mean_diff']:+.2f}  t={v['t']:+.2f}  p_two={v['p_two']:.3f}  p_one(>)={v['p_one']:.3f}")
    print(f"    spearman(glen,resid): rho={SP['spearman_glen_resid']['rho']:+.3f} p={SP['spearman_glen_resid']['p']:.3f}")
    print(f"    spearman(glen,shortfall): rho={SP['spearman_glen_shortfall']['rho']:+.3f} p={SP['spearman_glen_shortfall']['p']:.3f}")
    print()

print(f"POPULATION (ALL detectable most-recent absences): {len(recs)}  |  QUALIFIED (>=6g both ends): {len(qual)}")
print(f"bucket counts ALL: {out['bucket_counts']}  |  QUALIFIED: {out['bucket_counts_qualified']}")
print("shortfall = pre-absence level - realised post-return level (POSITIVE = a realised DROP).")
print("resid = shortfall - shipped age-curve predicted penalty (age_pre; _merged_recover.py:370-388).\n")
report_view("VIEW 1 — ALL detectable absences (directive's 'every player')", summary, sep)
report_view("VIEW 2 — QUALIFIED baseline (both endpoints on a >=6g season; the clean cut)", summary_q, sep_q)
print("NAMED PLAYERS BY BUCKET (Q = qualified baseline; player | pos last->ret glen | age_pre | Lpre->Lpost | pred | shortfall | resid):")
for b in buckets:
    print(f"--- bucket {b} (n={summary[b]['n']}, qualified={summary_q[b]['n']}) ---")
    for r in sorted([x for x in recs if x['bucket'] == b], key=lambda r: -r['shortfall']):
        print(f"  {'Q' if r['qualified'] else ' '} {r['player']:<24} {r['pos']:<8} {r['last']}->{r['ret']} g{r['glen']} "
              f"age_pre={r['age_pre']:>2} L {r['Lpre']:>6.1f}->{r['Lpost']:>6.1f} "
              f"pred={r['pred_pts']:>5.2f} short={r['shortfall']:>+6.1f} resid={r['resid']:>+6.1f}")
print("\nJSON written to gap_magnitude.json")
