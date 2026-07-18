"""RIDER (iv) — THE REPLACEMENT-ADJUSTED VIEW · shared loader + method · READ-ONLY.

Loads the FROZEN inputs from the git object at the rider-(iv) git-entry pin `a90052a`
(the five-migration head; NOT the working tree) and ASSERTS the stamps at load. HALT
(SystemExit 3) on any mismatch — silence is a red (S1). Nothing here writes the store,
the engine, the curve, or docs; all are read-only inputs.

Reuses the riders-(i)-(iii) machinery verbatim in spirit (loader / realized-outcome
convention / log-pick adaptive-bandwidth smoother). The frozen curve, per_entrant and
store are byte-identical at `a90052a` and the riders-(i)-(iii) base pin `e4177c2`.

DECLARED (see PLAN.md):
- R_curve      = v2 curve payload evaluated at the free-intake pick-equivalents (90/92).
- R_realized   = era-matched realised-outcome value of the free-intake pool; realised =
                 mean(vpath) (gross; busts full weight, R107.3; never-produced -> 0);
                 CONTINUOUS evidence weighting (no hard maturity cutoff): w=1.0 if terminal
                 (delisted/retired), else min(1, n_obs_career_years/6).
- R_owner      = 220, a labelled reference constant (item 332); never fed to a computation.
"""
import subprocess, hashlib, json, sys
import numpy as np

PIN_SHA  = 'a90052add8570c014626196cc2e3e13eece02548'   # rider-(iv) git entry (five-migration head)
REPO     = '/home/user/afl-rl-engine'
CURVE_PATH = 'engine/rl_after/pvc_curve_v2.json'
PER_PATH   = 'session_2026-07-17/legd_derivation/out/per_entrant.json'
RINP_PATH  = 'session_2026-07-18/five_migration/out/rider_R_inputs.json'

# expected stamps (from the frozen curve's own stamp block + the riders-(i)-(iii) assertions)
EXP = dict(curve_file_md5='56dd7a7b', curve_payload_md5='89c14729',
           per_entrant_md5='40d7da7c', store_base_md5='968de0c7')

# reproducibility / smoother constants (mirrors derive_pvc2.fit_year0 + riders common.py)
BOOT_SEED = 20260718
NMIN, HMIN, HMAX, HSTEP = 35.0, 0.10, 0.60, 0.02
KMIN, KMAX = 1, 99
YFULL = 6                      # career-year horizon for the continuous evidence weight
COMPLETE_MAXYEAR = 2017        # career-complete cohorts (riders convention; used for the era view)
MECH = ['MSD', 'SSP', 'IRE', 'UNR', 'PDA', 'PDN', 'PDS']
R_OWNER = 220                  # labelled reference constant (item 332)


def _halt(msg):
    print(f"HALT: {msg}", file=sys.stderr); sys.exit(3)


def _git_show(path):
    r = subprocess.run(['git', '-C', REPO, 'show', f'{PIN_SHA}:{path}'], capture_output=True)
    if r.returncode != 0:
        _halt(f"git show {PIN_SHA}:{path} failed rc={r.returncode}: {r.stderr.decode()[:200]}")
    return r.stdout


def _md5(b):
    return hashlib.md5(b).hexdigest()[:8]


def load_frozen():
    """Return (curve, per_entrant, rinputs, stamps). Asserts stamps; HALTs on any mismatch."""
    # git-entry precision law: the pin must resolve to EXACTLY PIN_SHA
    ls = subprocess.run(['git', '-C', REPO, 'rev-parse', PIN_SHA], capture_output=True, text=True)
    if ls.returncode != 0 or ls.stdout.strip() != PIN_SHA:
        _halt(f"git entry: {PIN_SHA} did not resolve to itself ({ls.stdout.strip()})")
    raw_curve = _git_show(CURVE_PATH)
    raw_per   = _git_show(PER_PATH)
    raw_rinp  = _git_show(RINP_PATH)
    cur_obj = json.loads(raw_curve)
    cfile = _md5(raw_curve)
    cpay  = _md5(json.dumps(cur_obj['curve'], sort_keys=True).encode())
    pmd5  = _md5(raw_per)
    checks = [('curve_file_md5', cfile, EXP['curve_file_md5']),
              ('curve_payload_md5', cpay, EXP['curve_payload_md5']),
              ('per_entrant_md5', pmd5, EXP['per_entrant_md5']),
              ('store_base_md5', cur_obj['stamp']['store_md5'][:8], EXP['store_base_md5']),
              ('per_entrant_md5(stamp)', cur_obj['stamp']['per_entrant_md5'][:8], EXP['per_entrant_md5'])]
    bad = [(n, g, e) for n, g, e in checks if g != e]
    if bad:
        for n, g, e in bad:
            print(f"  STAMP FAIL {n}: got {g} expect {e}", file=sys.stderr)
        _halt("frozen-input stamp mismatch — rider (iv) would NOT describe the pinned lineage")
    curve = {int(k): int(v) for k, v in cur_obj['curve'].items()}
    per = json.loads(raw_per)
    rinp = json.loads(raw_rinp)
    stamps = dict(pin_sha=PIN_SHA, curve_file_md5=cfile, curve_payload_md5=cpay,
                  per_entrant_md5=pmd5, store_base_md5=cur_obj['stamp']['store_md5'][:8])
    print(f"[common_riv] frozen inputs loaded @ {PIN_SHA[:8]} — stamps PASS "
          f"(curve payload {cpay}, per_entrant {pmd5}, store base {stamps['store_base_md5']})")
    return curve, per, rinp, stamps


# ---------------- pick-equivalents (from the R-inputs artifact) ----------------
def pickeq(rinp):
    """{mechanism -> pick-equivalent} from the frozen R-inputs artifact."""
    return {k: int(v) for k, v in rinp['PICKEQ'].items()}


# ---------------- realised-outcome + evidence weight (DECLARED) ----------------
def realized(r):
    """Life-path realised value = mean(vpath); never-produced -> 0 (bust, full weight). Gross."""
    vp = [v for v in (r.get('vpath') or []) if v is not None]
    return float(np.mean(vp)) if vp else 0.0


def n_obs(r):
    return sum(1 for v in (r.get('vpath') or []) if v is not None)


def is_terminal(r):
    return bool(r.get('delisted') or r.get('retired_now'))


def evidence_weight(r):
    """Continuous evidence weight, NO hard maturity cutoff (our law). Terminal (fully observed,
    incl. busts) -> 1.0; else fade with observed career-years toward 0. Never excludes a cohort."""
    if is_terminal(r):
        return 1.0
    return min(1.0, n_obs(r) / YFULL)


def mech_rows(per, t):
    return [r for r in per if r['type'] == t]


def free_pool(per):
    return [r for r in per if r['type'] in MECH]


def r_realized(rows):
    """Evidence-weighted realised value over a list of entrant rows. Returns (value, sum_w, n)."""
    num = den = 0.0
    for r in rows:
        w = evidence_weight(r)
        den += w
        num += w * realized(r)
    return (num / den if den > 0 else float('nan')), den, len(rows)


# ---------------- the smoother (log-pick Gaussian NW, adaptive bw to eff-n>=NMIN) --------------
def smooth_perpick(points_pick, points_val, points_wt=None, nmin=NMIN, grid=None,
                   hmin=HMIN, hmax=HMAX, hstep=HSTEP):
    """Kernel-smoothed estimate per integer pick; mirrors derive_pvc2.fit_year0's bandwidth rule.
    Finest resolution the sample supports; per exact pick; NO decile bands (item 325)."""
    pk = np.asarray(points_pick, float)
    val = np.asarray(points_val, float)
    wt = np.ones_like(val) if points_wt is None else np.asarray(points_wt, float)
    Lp = np.log(pk)
    if grid is None:
        grid = list(range(KMIN, KMAX + 1))
    out = dict(grid=list(grid), smooth={}, effn={}, h={})
    for p in grid:
        L = np.log(p)
        h = hmin
        while h < hmax:
            if float(np.sum(np.exp(-0.5 * ((Lp - L) / h) ** 2))) >= nmin:
                break
            h += hstep
        K = np.exp(-0.5 * ((Lp - L) / h) ** 2) * wt
        out['smooth'][p] = float(np.sum(K * val) / np.sum(K)) if np.sum(K) > 0 else float('nan')
        out['effn'][p] = float(np.sum(np.exp(-0.5 * ((Lp - L) / h) ** 2)))
        out['h'][p] = round(h, 3)
    return out


# ---------------- rider-(iii) uncertainty grade (frozen, for overlay) ----------------
def rider_iii_grade():
    """Return {pick -> uncertainty_grade_pct} from the frozen riders-(i)-(iii) artifact (PR #110)."""
    r = subprocess.run(['git', '-C', REPO, 'show',
                        '03cecdec:session_2026-07-18/riders_i_iii/out/rider_iii_uncertainty.json'],
                       capture_output=True)
    if r.returncode != 0:
        _halt("rider-(iii) grade artifact not reachable (fetch 03cecdec / PR #110)")
    d = json.loads(r.stdout)
    return ({int(k): v['uncertainty_grade_pct'] for k, v in d['series'].items()},
            d['top_reference_grade_pct'], d['deep_tail_median_grade_pct'], d['deep_tail_vs_top_ratio'])


AXES_NOTE = ("production bars and list-space R are orthogonal (R107.7); v2.11 bakes GROSS either "
             "way; making v-R the traded currency is the named post-v2.11 chapter, on the owner's word.")

STAMP_NOTE = ("stamps: pin=%s curve_payload=%s store_base=%s per_entrant=%s (five-migration head; "
              "read-only; asserted at load, HALT-on-mismatch)" % (PIN_SHA[:8], EXP['curve_payload_md5'],
              EXP['store_base_md5'], EXP['per_entrant_md5']))


if __name__ == '__main__':
    curve, per, rinp, stamps = load_frozen()
    peq = pickeq(rinp)
    fp = free_pool(per)
    rr, den, n = r_realized(fp)
    print(f"[common_riv] pick-equivalents: {peq}")
    print(f"[common_riv] free-intake pool n={n}  R_realized(pooled)={rr:.1f} (sum_w={den:.1f})")
    print(f"[common_riv] R_curve(pooled@pickeq)~{curve[90]}-{curve[92]}   R_owner={R_OWNER}")
    g, top, deep, ratio = rider_iii_grade()
    print(f"[common_riv] rider-(iii) grade @pk90={g[90]}%  top={top}%  deep-median={deep}%  ratio={ratio}")
    print("[common_riv] self-test OK")
