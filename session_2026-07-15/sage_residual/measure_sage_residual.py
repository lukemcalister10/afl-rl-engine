#!/usr/bin/env python3
"""L-SAGE-FADE 30+ residual — register 122a, 2026-07-15.

Measures the realised breakout-persistence slope s_real(age) for proven players and compares it to
the engine's _S_AGE(age) (which is 0.0 at age>=30). Read-only on the store; writes only under
session_2026-07-15/sage_residual/. Exec's _merged_recover.py exactly as run_panel.sh (config gate).
"""
import io, contextlib, os, sys, json, csv
import numpy as np

OUT = os.path.dirname(os.path.abspath(__file__))
np.random.seed(0)

# --- exec the engine exactly as run_panel.sh (gate mode: manifest == defaults) -------------------
import config_manifest
config_manifest.enforce()
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
    exec(src, g)

MA = g['MA']; cp = g['cp']
_lvlcurr = g['_lvlcurr']; _nqual = g['_nqual']; _radq = g['_radq']; _S_AGE = g['_S_AGE']
lvl_orig = cp._lvl_eff_orig
PROVEN_N = g['PROVEN_N']; TOL_M1 = g['TOL_M1']; G_ADQ = g['G_ADQ']
INPROG_Y = g['INPROG_Y']
print(f"# engine loaded: PROVEN_N={PROVEN_N} TOL_M1={TOL_M1} G_ADQ={G_ADQ} INPROG_Y={INPROG_Y}", file=sys.stderr)
print(f"# S_AGE curve: " + " ".join(f"{a}:{_S_AGE(a):.4f}" for a in range(28,37)), file=sys.stderr)

data = [p for p in MA.data if MA.GRP.get(p.get('pos'))]

def next_season_avg(p, Y, min_games):
    for x in p['scoring']:
        if x['year'] == Y+1 and x['games'] >= min_games and (cp.debutyr(p)-1) < x['year']:
            return x['avg'], x['games']
    return None, 0

# --- build the observation table -----------------------------------------------------------------
# One row per proven up-branch player-year with a realised Y+1 season.
def build(min_games_next=10, gap_floor=TOL_M1, y_end=2024):
    rows = []
    for p in data:
        yrs = sorted({x['year'] for x in p['scoring'] if x['games']>0 and (cp.debutyr(p)-1)<x['year']})
        for Y in yrs:
            if Y > y_end:            # need completed Y+1
                continue
            if _nqual(p, Y) < PROVEN_N:
                continue
            Lo = lvl_orig(p, Y); Lc = _lvlcurr(p, Y)
            gap = Lc - Lo
            if gap < gap_floor:      # up-branch trigger, engine's exact floor
                continue
            if not _radq(p, Y, Lo):
                continue
            Lnext, gnext = next_season_avg(p, Y, min_games_next)
            if Lnext is None:
                continue
            age = cp._age_asof(p, Y)
            if age is None:
                continue
            rows.append(dict(player=p['player'], pos=p['pos'], year=Y, age=float(age),
                             Lo=Lo, Lc=Lc, gap=gap, Lnext=Lnext, gnext=gnext,
                             y=Lnext-Lo, sage=_S_AGE(age),
                             pid=p.get('stable_player_id') or p['player']))
    return rows

# --- kernel ratio-of-means slope + player-cluster bootstrap --------------------------------------
def kslope(rows, a, h=1.5):
    w = np.array([np.exp(-0.5*((r['age']-a)/h)**2) for r in rows])
    x = np.array([r['gap'] for r in rows]); y = np.array([r['y'] for r in rows])
    num = float(np.sum(w*y)); den = float(np.sum(w*x))
    return num/den if den > 0 else float('nan')

def boot_ci(rows, a, h=1.5, B=5000):
    # cluster resample by player
    by_p = {}
    for r in rows:
        by_p.setdefault(r['pid'], []).append(r)
    pids = list(by_p.keys())
    ests = []
    for _ in range(B):
        samp = []
        for pid in np.random.choice(pids, size=len(pids), replace=True):
            samp.extend(by_p[pid])
        s = kslope(samp, a, h)
        if s == s:  # not nan
            ests.append(s)
    ests = np.array(ests)
    return float(np.percentile(ests, 2.5)), float(np.percentile(ests, 97.5))

def eff_n(rows, a, h=1.5):
    # kernel-effective player-year weight + distinct players within ~1 bandwidth
    w = np.array([np.exp(-0.5*((r['age']-a)/h)**2) for r in rows])
    raw = int(sum(1 for r in rows if abs(r['age']-a) < 0.5))
    dpl = len({r['pid'] for r in rows if abs(r['age']-a) <= h})
    return raw, dpl, float(np.sum(w))

def raw_slope_ci(rows, a, B=5000):
    # UNSMOOTHED: only obs at exactly integer age a. Player-cluster bootstrap.
    sel = [r for r in rows if abs(r['age']-a) < 0.5]
    if not sel:
        return float('nan'), float('nan'), float('nan')
    x = np.array([r['gap'] for r in sel]); y = np.array([r['y'] for r in sel])
    s = float(np.sum(y)/np.sum(x))
    by_p = {}
    for r in sel: by_p.setdefault(r['pid'], []).append(r)
    pids = list(by_p.keys()); ests = []
    for _ in range(B):
        samp = []
        for pid in np.random.choice(pids, size=len(pids), replace=True):
            samp.extend(by_p[pid])
        xx = np.array([r['gap'] for r in samp]); yy = np.array([r['y'] for r in samp])
        if np.sum(xx) > 0: ests.append(float(np.sum(yy)/np.sum(xx)))
    ests = np.array(ests)
    return s, float(np.percentile(ests,2.5)), float(np.percentile(ests,97.5))

# --- MAIN measurement ----------------------------------------------------------------------------
rows = build()
print(f"# up-branch proven player-years w/ realised Y+1 (games>=10, gap>=5): {len(rows)}", file=sys.stderr)
ages = list(range(29, 37))
out = []
for a in ages:
    s = kslope(rows, a)
    lo, hi = boot_ci(rows, a)
    raw, dpl, wsum = eff_n(rows, a)
    sage = _S_AGE(a)
    resid = s - sage
    zero_in = (lo <= 0.0 <= hi)
    rs, rlo, rhi = raw_slope_ci(rows, a)
    out.append(dict(age=a, n_raw=raw, n_players=dpl, wsum=round(wsum,1),
                    s_real=round(s,4), ci_lo=round(lo,4), ci_hi=round(hi,4),
                    s_raw=round(rs,4) if rs==rs else '', raw_lo=round(rlo,4) if rlo==rlo else '',
                    raw_hi=round(rhi,4) if rhi==rhi else '',
                    sage_engine=round(sage,4), residual=round(resid,4),
                    zero_in_ci=zero_in))

with open(os.path.join(OUT,'residual_by_age.csv'),'w',newline='') as f:
    wr = csv.DictWriter(f, fieldnames=list(out[0].keys())); wr.writeheader(); wr.writerows(out)

print("\nage n_raw n_pl  s_smooth    95%CI(smooth)   s_raw(age-only) 95%CI(raw)      S_AGE  0inCI(smooth)")
for r in out:
    raw = f"{r['s_raw']:+.3f} [{r['raw_lo']:+.3f},{r['raw_hi']:+.3f}]" if r['s_raw']!='' else "  (no obs)"
    print(f"{r['age']:>3} {r['n_raw']:>5} {r['n_players']:>4}  {r['s_real']:+.3f}  [{r['ci_lo']:+.3f},{r['ci_hi']:+.3f}]  {raw:>26}  {r['sage_engine']:.3f}  {r['zero_in_ci']}")

# --- SENSITIVITY (report, don't bury) ------------------------------------------------------------
print("\n# SENSITIVITY: pooled 30+ realised slope under knob variations")
def pooled30(rows):
    r30 = [r for r in rows if r['age'] >= 30]
    x = np.array([r['gap'] for r in r30]); y = np.array([r['y'] for r in r30])
    ratio = float(np.sum(y)/np.sum(x)) if len(r30) else float('nan')
    perobs = float(np.mean([r['y']/r['gap'] for r in r30])) if r30 else float('nan')
    return len(r30), len({r['pid'] for r in r30}), ratio, perobs
for mg, gf in [(10,5.0),(6,5.0),(10,3.0),(6,3.0)]:
    rr = build(min_games_next=mg, gap_floor=gf)
    n, npl, ratio, perobs = pooled30(rr)
    print(f"  next_games>={mg}, gap>={gf}: n30={n} players30={npl}  slope(ratio)={ratio:+.3f}  slope(mean y/x)={perobs:+.3f}")

# --- ATTRITION / survivorship (declared caveat) --------------------------------------------------
# Of proven up-branch player-years at age>=29, how many have NO qualifying (>=10g) Y+1 season?
# Those washouts are EXCLUDED from s_real, biasing it UP (survivors persist; washouts don't).
print("\n# ATTRITION: proven up-branch (gap>=5, radq) breakouts with NO qualifying Y+1 (games>=10)")
att = {}
for p in data:
    yrs = sorted({x['year'] for x in p['scoring'] if x['games']>0 and (cp.debutyr(p)-1)<x['year']})
    for Y in yrs:
        if Y > 2024: continue
        if _nqual(p,Y) < PROVEN_N: continue
        Lo = lvl_orig(p,Y); Lc = _lvlcurr(p,Y)
        if (Lc-Lo) < TOL_M1 or not _radq(p,Y,Lo): continue
        age = cp._age_asof(p,Y)
        if age is None or age < 29: continue
        a = int(round(age))
        Lnext,_ = next_season_avg(p,Y,10)
        d = att.setdefault(a,[0,0]); d[0]+=1
        if Lnext is None: d[1]+=1
print("  age  breakouts  washed_out(no qual Y+1)  washout_rate")
for a in sorted(att):
    tot,wo = att[a]; print(f"  {a:>3}   {tot:>7}   {wo:>18}        {wo/tot:.2f}")

# stash rows for the mispricing step
with open(os.path.join(OUT,'_obs_rows.json'),'w') as f:
    json.dump(rows, f)
print("\n# wrote residual_by_age.csv + _obs_rows.json", file=sys.stderr)
