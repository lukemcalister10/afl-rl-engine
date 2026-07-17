"""RIDERS (i)-(iii) shared loader / smoother — READ-ONLY.

Loads the FROZEN Leg-D candidate inputs from the git object at the base-pin commit
e4177c2 (NOT the working tree) and ASSERTS the three stamps at load. HALT (SystemExit 3)
on any mismatch — silence is a red (S1). Nothing here writes the store, the engine, or
the curve; the curve/per_entrant are read-only inputs.

Design facts (established by reading derive_pvc2.py + the data; see PLAN.md):
- PVC(p) = year-0 point of the 2-D evidence-weighted non-median fit; shipped tau=0.12 makes
  the year-0 slice ~ the smoothed per-exact-pick mean of v0 (the entry snapshot).
- realized outcome (DECLARED primary) = mean(vpath): the codebase's own life-path measure.
  Gross (R107.7); busts full weight (R107.3); every in-curve entrant has >=1 vpath point.
- smoother = Gaussian kernel over log-pick, adaptive bandwidth to eff-n>=NMIN, mirroring the
  frozen curve's own fit_year0 (hmin=0.10, hmax=0.60, NMIN=35). Per exact pick. No decile bands.
"""
import subprocess, hashlib, json, sys
import numpy as np

BASE_SHA   = 'e4177c21934148c19d9cec3c015fee5d28480102'
REPO       = '/home/user/afl-rl-engine'
CURVE_PATH = 'engine/rl_after/pvc_curve_v2.json'
PER_PATH   = 'session_2026-07-17/legd_derivation/out/per_entrant.json'

# expected stamps (from the frozen curve's own stamp block + entry assertions)
EXP = dict(code_sha=BASE_SHA, curve_file_md5='56dd7a7b', curve_payload_md5='89c14729',
           per_entrant_md5='40d7da7c', store_base_md5='968de0c7')

KMIN, KMAX = 1, 99
NMIN, HMIN, HMAX, HSTEP = 35.0, 0.10, 0.60, 0.02
FIT_LO, FIT_HI = 2004, 2024          # the frozen curve's fit window
COMPLETE_MAXYEAR = 2017              # career-complete cohorts (mean vpath length >= ~6; ~all exited)

def _halt(msg):
    print(f"HALT: {msg}", file=sys.stderr); sys.exit(3)

def _git_show(path):
    r = subprocess.run(['git', '-C', REPO, 'show', f'{BASE_SHA}:{path}'],
                       capture_output=True)
    if r.returncode != 0:
        _halt(f"git show {BASE_SHA}:{path} failed rc={r.returncode}: {r.stderr.decode()[:200]}")
    return r.stdout

def _md5(b): return hashlib.md5(b).hexdigest()[:8]

def load_frozen():
    """Return (curve: dict[int->int], per_entrant: list[dict], stamps: dict). Asserts stamps; HALTs on mismatch."""
    raw_curve = _git_show(CURVE_PATH)
    raw_per   = _git_show(PER_PATH)
    # stamp assertions (HALT on any mismatch)
    cfile = _md5(raw_curve)
    cur_obj = json.loads(raw_curve)
    cpay = _md5(json.dumps(cur_obj['curve'], sort_keys=True).encode())
    pmd5 = _md5(raw_per)
    checks = [('curve_file_md5', cfile, EXP['curve_file_md5']),
              ('curve_payload_md5', cpay, EXP['curve_payload_md5']),
              ('per_entrant_md5', pmd5, EXP['per_entrant_md5']),
              ('store_base_md5', cur_obj['stamp']['store_md5'][:8], EXP['store_base_md5']),
              ('per_entrant_md5(stamp)', cur_obj['stamp']['per_entrant_md5'][:8], EXP['per_entrant_md5'])]
    bad = [(n, got, exp) for n, got, exp in checks if got != exp]
    if bad:
        for n, got, exp in bad: print(f"  STAMP FAIL {n}: got {got} expect {exp}", file=sys.stderr)
        _halt("frozen-input stamp mismatch — riders would NOT describe the candidate")
    curve = {int(k): int(v) for k, v in cur_obj['curve'].items()}
    per = json.loads(raw_per)
    stamps = dict(code_sha=BASE_SHA, curve_file_md5=cfile, curve_payload_md5=cpay,
                  per_entrant_md5=pmd5, store_base_md5=cur_obj['stamp']['store_md5'][:8])
    print(f"[common] frozen inputs loaded @ {BASE_SHA[:8]} — stamps PASS "
          f"(curve payload {cpay}, per_entrant {pmd5}, store base {stamps['store_base_md5']})")
    return curve, per, stamps

# ---------------- pool + realized-outcome definitions (DECLARED) ----------------
def in_curve_pool(per):
    """In-curve entrants with a real pick and a v0 (the curve's own eligibility)."""
    return [r for r in per if r.get('incurve') and r.get('pick') and r.get('v0')]

def realized(r, kind='meanvpath'):
    """Realized outcome scalar. Primary = mean(vpath) (codebase life-path measure; gross; busts full weight)."""
    vp = [v for v in r.get('vpath', []) if v is not None]
    if kind == 'meanvpath':
        return float(np.mean(vp)) if vp else float(r['v0'])
    if kind == 'peak':
        return float(r.get('peak') or (max(vp) if vp else r['v0']))
    if kind == 'cur':
        return float(r.get('cur') or (vp[-1] if vp else r['v0']))
    raise ValueError(kind)

def is_exited(r):
    """Washout/delist-exit: terminal career (censoring-free realized)."""
    return bool(r.get('delisted') or r.get('retired_now'))

def is_complete_cohort(r):   return r['year'] <= COMPLETE_MAXYEAR
def is_fit_era(r):           return FIT_LO <= r['year'] <= FIT_HI
def is_heldout(r):           return not is_fit_era(r)

# ---------------- the smoother (log-pick Gaussian NW, adaptive bw to eff-n>=NMIN) ----------------
def smooth_perpick(points_pick, points_val, points_wt=None, nmin=NMIN,
                   grid=None, hmin=HMIN, hmax=HMAX, hstep=HSTEP):
    """Kernel-smoothed estimate at each integer pick. Mirrors derive_pvc2.fit_year0's bandwidth rule.

    Returns dict: grid, smooth[p], effn[p] (kernel eff-n at p), h[p] (bandwidth), raw_n[p] (exact-pick count).
    Bandwidth grows until the local Gaussian eff-n (of the SAMPLE point-picks) >= nmin, so the resolution
    is 'the finest the sample supports' and is reported per pick. Weights default to 1.0 per point
    (equal weight per entrant = gross, busts full weight)."""
    pk = np.asarray(points_pick, float)
    val = np.asarray(points_val, float)
    wt = np.ones_like(val) if points_wt is None else np.asarray(points_wt, float)
    Lp_all = np.log(pk)
    if grid is None: grid = list(range(KMIN, KMAX + 1))
    from collections import Counter
    cnt = Counter(int(x) for x in pk)
    out = dict(grid=list(grid), smooth={}, effn={}, h={}, raw_n={})
    for p in grid:
        L = np.log(p)
        h = hmin
        while h < hmax:
            effn = float(np.sum(np.exp(-0.5 * ((Lp_all - L) / h) ** 2)))
            if effn >= nmin: break
            h += hstep
        K = np.exp(-0.5 * ((Lp_all - L) / h) ** 2) * wt
        sm = float(np.sum(K * val) / np.sum(K)) if np.sum(K) > 0 else float('nan')
        out['smooth'][p] = sm
        out['effn'][p] = float(np.sum(np.exp(-0.5 * ((Lp_all - L) / h) ** 2)))
        out['h'][p] = round(h, 3)
        out['raw_n'][p] = int(cnt.get(p, 0))
    return out

def raw_perpick_mean(points_pick, points_val):
    """Unsmoothed per-exact-pick mean (the scatter the smoother rests on; transparency)."""
    from collections import defaultdict
    d = defaultdict(list)
    for p, v in zip(points_pick, points_val): d[int(p)].append(v)
    return {p: dict(n=len(d[p]), mean=round(float(np.mean(d[p])), 1)) for p in sorted(d)}

STAMP_NOTE = ("stamps: code_sha=%s curve_payload=%s store_base=%s per_entrant=%s (frozen @ e4177c2; "
              "read-only; asserted at load)" % (BASE_SHA, EXP['curve_payload_md5'],
              EXP['store_base_md5'], EXP['per_entrant_md5']))

if __name__ == '__main__':
    curve, per, stamps = load_frozen()
    P = in_curve_pool(per)
    print(f"[common] in-curve pool n={len(P)}  complete(<= {COMPLETE_MAXYEAR}) n={sum(is_complete_cohort(r) for r in P)}"
          f"  exited n={sum(is_exited(r) for r in P)}")
    print("[common] self-test OK")
