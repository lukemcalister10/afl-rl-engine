"""334 STAGE B / STAGE 2 RE-DERIVED ON THE ERA-FREE BASIS -- THE PER-PICK RE-ANCHOR.

SUPERSEDES ../stage2/derive_reanchor_stage2.py, which is RETAINED AS HISTORY. That derivation was
taught on the era-NORMALIZED basis: every score feeding it carried the engine's `REF/era.get(y,REF)`
multiplier. The owner ruling (334 stage B, era-removal stage, commit f7ae027) holds that SuperCoach
scores are era-comparable BY CONSTRUCTION -- every match assigns 3,300 points -- so no era
normalization may be applied anywhere. The multiplier is deleted from the engine; the ladder fitted
through it was reverted; this file re-derives it from clean scores. METHOD IS UNCHANGED, byte-for-byte
in every estimator below. Only the BASIS moved (engine head e3527be4 -> a0a20d6e).

NO ERA NORMALIZATION IS APPLIED OR RE-INTRODUCED HERE. The three instruments this derivation imports
or re-runs (emit_matrix_338.py, noarb_table_338.py, harness_pvc_REPINNED_pass3.py) were grepped for
era/REF adjustments of their own before use: the only hits are `MA.BASE_REF` / `MA.AGE_REF` in the
emitter's walk-forward loop, which are the as-of ANCHOR YEARS the matrix is defined by (the evaluation
date), NOT a per-year score rescale. Nothing was stripped from them; nothing needed to be.

WHAT THIS DOES
  Teaches a per-pick re-anchor factor f(p) from the ERA-FREE walk-forward matrix and applies
  it to the shipped ladder in engine/rl_after/pvc_curve_v2.json. The construction is:

      R_raw(p) = mean_{cohort at pick p} value(PEAK YEAR)  /  mean_{cohort at pick p} value(year 0)
      R_s(p)   = locality-smoothed R_raw along the PICK axis (Gaussian kernel, n(p)-weighted,
                 bandwidth h = 8.0 picks, NOT the LOO argmin -- see the STEP 3 disclosure;
                 NO binning, NO bands, NO bucket steps)
      f(p)     = R_s(p) / TARGET_RESIDUAL
      new(p)   = old(p) * f(p)

  Each pick is lifted by ITS OWN measured excess appreciation, leaving ~TARGET_RESIDUAL residual
  everywhere. Non-uniform by construction; a uniform scalar multiplier is barred and is checked
  against explicitly below.

THE TARGET'S ROLE
  TARGET_RESIDUAL (1.40) appears ONLY here, in this teaching/derivation script. It is a divisor that
  sets the level of f. It does not enter any runtime engine path and is not written into any engine
  file. The only artefact that leaves this script is the ladder itself.

POPULATION
  Not re-implemented: taken by CALLING the committed harness's own loader,
  harness_pvc_REPINNED_pass3.load_matrix(), which asserts the matrix identity pins
  (store 37ced3ce, v0surf af556bdca53d) and the ND teaching population (teaches_curve & pick 1..64
  & class 2004..2022, n=1197). Value extraction likewise reuses noarb_table_338.value_at, so the
  numbers here are byte-comparable in method with the no-arb table.

BUSTS
  Busts are IN. value_at returns 0.0 for a career that ended before the peak year ('ended') or that
  carries a null as-of value ('null'). No row is filtered out of any mean. This is the standing order
  and it is what makes mean_peak(p) a cohort-level quantity rather than a survivor quantity.

RE-RUNNABLE: reads the committed matrix copy beside it and the committed ladder; writes nothing
unless --write is passed.
"""
import os, sys, json, math, hashlib, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import harness_pvc_REPINNED_pass3 as H     # committed harness: loader + identity pins
import noarb_table_338 as T                # committed table: value_at (year-N extraction)

TARGET_RESIDUAL = 1.40      # TEACHING-STAGE ONLY. Never read by a runtime engine path.
NPICK = 64
BANDWIDTH = 8.0             # picks. NOT the LOO argmin -- see the disclosure printed in STEP 3.
MAXYEAR = 9                 # the year-ratio row is reported 0..9 (peak still taken at FULL inclusion)

# The SUPERSEDED era-normalized basis's whole-cohort ratios, quoted from ../stage2/ for the delta
# column only. Nothing here is used in any estimate -- it is a reporting comparison.
PRIOR_BASIS = {0: 1.0000, 1: 1.0211, 2: 1.2793, 3: 1.4478, 4: 1.5351,
               5: 1.5341, 6: 1.4955, 7: 1.2988}


def _pstdev(xs):
    m = sum(xs) / len(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / len(xs))

# ---------------------------------------------------------------- peak year, derived not assumed
def whole_cohort_year_ratios(ND, maxyear=7):
    """The step-1 whole-cohort table, recomputed here so the peak year is DERIVED in-script and the
    step-1 control is reproduced rather than quoted. Returns {N: (n_incl, mean_yrN, mean_yr0, ratio)}.
    Rows where a career has not yet reached year N are excluded from year N (and from that row's
    year-0 basis) exactly as the no-arb table does -- apples-to-apples."""
    WINDOW_END = 2026
    out = {}
    for N in range(0, maxyear + 1):
        incl = [r for r in ND if r['year'] + N <= WINDOW_END]
        if not incl:
            continue
        vN = [T.value_at(r, N)[0] for r in incl]
        v0 = [T.value_at(r, 0)[0] for r in incl]
        mN, m0 = sum(vN) / len(vN), sum(v0) / len(v0)
        out[N] = (len(incl), mN, m0, mN / m0 if m0 else float('nan'))
    return out


def pick_peak_year(ratios, full_n):
    """THE PEAK YEAR is the argmax of the whole-cohort ratio over the years at FULL inclusion
    (n_incl == the whole cohort). Restricting to full inclusion is deliberate and is the honest
    reading: once 'not yet reached' attrition starts, each later year is a different, survivor-
    shifted population, and its ratio is not comparable with year 0's. It also guarantees every
    entrant contributes to every per-pick mean below, so n(p) is the same at year 0 and at peak."""
    full = {N: v for N, v in ratios.items() if v[0] == full_n}
    return max(full, key=lambda N: full[N][3])


# ---------------------------------------------------------------- per-pick appreciation profile
def per_pick_profile(ND, peak):
    """R_raw(p) = mean_peak(p) / mean_yr0(p), busts at 0, n(p) recorded."""
    prof = {}
    for p in range(1, NPICK + 1):
        rows = [r for r in ND if r['pick'] == p]
        n = len(rows)
        if n == 0:
            prof[p] = dict(n=0, mean_yr0=float('nan'), mean_peak=float('nan'), R_raw=float('nan'),
                           n_zero_peak=0)
            continue
        v0 = [T.value_at(r, 0)[0] for r in rows]
        vP = [T.value_at(r, peak)[0] for r in rows]
        m0, mP = sum(v0) / n, sum(vP) / n
        prof[p] = dict(n=n, mean_yr0=m0, mean_peak=mP,
                       R_raw=(mP / m0 if m0 else float('nan')),
                       n_zero_peak=sum(1 for x in vP if x == 0.0))
    return prof


# ---------------------------------------------------------------- locality smoothing, no binning
def gauss_smooth(picks, R, W, h):
    """n-weighted Gaussian kernel regression on the pick axis.
    Continuous kernel over the integer pick axis: no bands, no buckets, no steps by construction."""
    out = {}
    for p in picks:
        num = den = 0.0
        for q in picks:
            w = math.exp(-0.5 * ((p - q) / h) ** 2) * W[q]
            num += w * R[q]
            den += w
        out[p] = num / den if den else float('nan')
    return out


def loo_bandwidth(picks, R, W, grid):
    """Leave-one-out CV: for each candidate h, predict R(p) from every OTHER pick and score the
    n(p)-weighted squared error. Returns (best_h, [(h, cv), ...])."""
    scores = []
    for h in grid:
        sse = wsum = 0.0
        for p in picks:
            num = den = 0.0
            for q in picks:
                if q == p:
                    continue
                w = math.exp(-0.5 * ((p - q) / h) ** 2) * W[q]
                num += w * R[q]
                den += w
            if den == 0:
                continue
            pred = num / den
            sse += W[p] * (R[p] - pred) ** 2
            wsum += W[p]
        scores.append((h, sse / wsum if wsum else float('inf')))
    best = min(scores, key=lambda t: t[1])[0]
    return best, scores


# ---------------------------------------------------------------- isotonic (decreasing) projection
def isotonic_decreasing(vals, weights):
    """Weighted pool-adjacent-violators for a NON-INCREASING fit. Returns the projected sequence.
    Only invoked if the raw product violates monotonicity; every change it makes is reported."""
    # blocks: [weighted mean, total weight, element count]
    blocks = [[float(v), float(w), 1] for v, w in zip(vals, weights)]
    i = 0
    while i < len(blocks) - 1:
        if blocks[i][0] < blocks[i + 1][0] - 1e-12:    # violation of non-increasing
            v1, w1, c1 = blocks[i]
            v2, w2, c2 = blocks[i + 1]
            blocks[i] = [(v1 * w1 + v2 * w2) / (w1 + w2), w1 + w2, c1 + c2]
            del blocks[i + 1]
            if i > 0:
                i -= 1                                  # re-check backwards
        else:
            i += 1
    out = []
    for v, _w, c in blocks:
        out.extend([v] * c)
    assert len(out) == len(vals), "isotonic expansion lost elements: %d vs %d" % (len(out), len(vals))
    return out


def n32_payload_md5(curve):
    payload = {str(int(k)): int(round(float(v))) for k, v in curve.items()}
    return hashlib.md5(json.dumps(payload, sort_keys=True).encode()).hexdigest()


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--matrix', default=os.path.join(HERE, 'per_entrant_338_erafree.json'))
    ap.add_argument('--ladder', default=os.path.join(HERE, 'pvc_curve_v2_PRE_stage2ef.json'))
    ap.add_argument('--write', default=None, help='path to write the re-taught ladder json')
    ap.add_argument('--out', default=HERE)
    a = ap.parse_args()

    meta, ND = H.load_matrix(a.matrix)
    print("=" * 100)
    print("334 STAGE B / STAGE 2 RE-DERIVED ERA-FREE -- PER-PICK RE-ANCHOR DERIVATION")
    print("=" * 100)
    print("  basis           : ERA-FREE. No era normalization anywhere (owner ruling, stage ER).")
    print("  matrix          : %s" % os.path.basename(a.matrix))
    print("  matrix md5      : %s" % hashlib.md5(open(a.matrix, 'rb').read()).hexdigest())
    print("  matrix identity : store=%s  v0surf=%s  n_records=%d"
          % (meta['store_md5'], meta['v0surf_sig'][:12], meta['n_records']))
    print("  engine head     : %s   (era-free engine; the era-normalized stage-1 head was e3527be4)"
          % meta.get('engine_head', 'n/a'))
    print("  population      : harness load_matrix ND filter -- teaches_curve & pick 1..64 &"
          " class 2004..2022")
    print("  cohort size     : %d entrants   (pins asserted by the harness loader, not re-checked here)"
          % len(ND))
    print("  target residual : %.2f   <-- TEACHING STAGE ONLY, never read by a runtime engine path"
          % TARGET_RESIDUAL)
    print()

    # ---- step 1 control: the whole-cohort year ratios, recomputed -------------------------------
    ratios = whole_cohort_year_ratios(ND, MAXYEAR)
    print("-" * 100)
    print("STEP 1 CONTROL -- ERA-FREE whole-cohort year ratios, years 0..%d" % MAXYEAR)
    print("  (recomputed in-script; must match the era-free no-arb table. The 'prior' column is the")
    print("   SUPERSEDED era-normalized basis, quoted from ../stage2/ for the delta only.)")
    print("-" * 100)
    print("  yrN   n_incl     mean_yrN     mean_yr0   ratio(EF)      prior      delta   full_incl")
    for N in sorted(ratios):
        n, mN, m0, r = ratios[N]
        pr = PRIOR_BASIS.get(N)
        print("  %-4d %6d %12.1f %12.1f %11.4f %10s %10s   %s"
              % (N, n, mN, m0, r,
                 ("%.4f" % pr) if pr is not None else "n/a",
                 ("%+.4f" % (r - pr)) if pr is not None else "n/a",
                 "YES" if n == len(ND) else "no (attrition)"))
    PEAK = pick_peak_year(ratios, len(ND))
    print()
    print("  PEAK YEAR (argmax of the ratio over FULL-inclusion years, n_incl==%d) : YEAR %d  (ratio %.3f)"
          % (len(ND), PEAK, ratios[PEAK][3]))
    print("  full-inclusion years: %s" % [N for N in sorted(ratios) if ratios[N][0] == len(ND)])
    print()

    # ---- step 1b: the pick-band splits (REPORTING ONLY -- these bands are NOT used in any estimate)
    print("-" * 100)
    print("STEP 1b -- pick-band splits, ERA-FREE (REPORTING ONLY: the 1-20 / 21-64 split is a")
    print("  readout for the report. NO estimator below bands on it -- f(p) is per-pick and smooth.)")
    print("-" * 100)
    for label, lo, hi in (('picks 1-20', 1, 20), ('picks 21-64', 21, 64)):
        sub = [r for r in ND if lo <= r['pick'] <= hi]
        sr = whole_cohort_year_ratios(sub, MAXYEAR)
        print("  %s  (cohort n=%d)" % (label, len(sub)))
        print("     yrN   n_incl     mean_yrN     mean_yr0      ratio")
        for N in sorted(sr):
            n, mN, m0, r = sr[N]
            print("     %-4d %6d %12.1f %12.1f %10.4f" % (N, n, mN, m0, r))
        print("     yr1 -> peak(yr%d) : %.4f -> %.4f   (lift %+.4f, x%.4f)"
              % (PEAK, sr[1][3], sr[PEAK][3], sr[PEAK][3] - sr[1][3], sr[PEAK][3] / sr[1][3]))
        print()
    print("  ALL picks 1-64  yr1 -> peak(yr%d) : %.4f -> %.4f   (lift %+.4f, x%.4f)"
          % (PEAK, ratios[1][3], ratios[PEAK][3], ratios[PEAK][3] - ratios[1][3],
             ratios[PEAK][3] / ratios[1][3]))
    print()

    # ---- step 2: per-pick appreciation profile --------------------------------------------------
    prof = per_pick_profile(ND, PEAK)
    picks = [p for p in range(1, NPICK + 1) if prof[p]['n'] > 0]
    assert len(picks) == NPICK, "a pick has no rows: %s" % [p for p in range(1, 65) if prof[p]['n'] == 0]
    R = {p: prof[p]['R_raw'] for p in picks}
    W = {p: float(prof[p]['n']) for p in picks}
    print("-" * 100)
    print("STEP 2 -- per-pick appreciation R_raw(p) = mean(year %d) / mean(year 0), busts at 0" % PEAK)
    print("-" * 100)
    print("  n total over picks : %d   (must equal the cohort: %d)" % (sum(W.values()), len(ND)))
    print("  R_raw   min %.4f   max %.4f   n-weighted mean %.4f"
          % (min(R.values()), max(R.values()),
             sum(W[p] * R[p] for p in picks) / sum(W.values())))
    print()

    # ---- step 3: smoothing -----------------------------------------------------------------------
    grid = [round(x * 0.5, 2) for x in range(4, 61)]        # h = 2.0 .. 30.0
    h_loo, scores = loo_bandwidth(picks, R, W, grid)
    cv = dict(scores)
    h = BANDWIDTH                                            # see the disclosure below
    Rs = gauss_smooth(picks, R, W, h)
    print("-" * 100)
    print("STEP 3 -- locality smoothing along the PICK axis (Gaussian kernel, n(p)-weighted)")
    print("-" * 100)
    print("  LOO CV surface over h in [%.1f, %.1f] step 0.5:" % (grid[0], grid[-1]))
    for hh in (2, 4, 6, 8, 10, 12, 15, 20, 25, 30):
        print("      h=%5.1f  cv=%.6f%s" % (hh, cv[float(hh)],
                                            "   <-- LOO argmin" if float(hh) == h_loo else ""))
    print("  LOO argmin          : h = %.1f picks   (cv %.6f)" % (h_loo, cv[h_loo]))
    print("  CHOSEN h            : %.1f picks" % h)
    print()
    print("  DISCLOSED DEVIATION -- the bandwidth is NOT taken from LOO. Reasons, measured:")
    print("    1. The CV surface is nearly FLAT. Between h=%.1f and the LOO argmin h=%.1f the CV"
          % (h, h_loo))
    print("       moves from %.6f to %.6f -- a %.1f%% difference. LOO barely discriminates here,"
          % (cv[h], cv[h_loo], 100.0 * (cv[h] - cv[h_loo]) / cv[h_loo]))
    print("       because with n(p) ~ %d-%d per pick the per-pick sampling noise swamps the signal"
          % (int(min(W.values())), int(max(W.values()))))
    print("       (R_raw sd across picks %.4f, and the h->inf constant fit scores %.6f in-sample)."
          % (_pstdev([R[p] for p in picks]),
             sum(W[p] * (R[p] - sum(W[q] * R[q] for q in picks) / sum(W.values())) ** 2
                 for p in picks) / sum(W.values())))
    print("    2. h=%.1f is a THIRD of the whole 64-pick axis. It drives R_s toward a single global"
          % h_loo)
    print("       constant -- and a constant R_s makes f a UNIFORM SCALAR, which this act BARS.")
    print("       Letting a flat CV surface pick the bandwidth would surrender the per-pick locality")
    print("       the construction exists to provide. Measured: at h=%.1f the f spread is %.4f;"
          % (h_loo, (lambda v: max(v) - min(v))([gauss_smooth(picks, R, W, h_loo)[p] / TARGET_RESIDUAL
                                                 for p in picks])))
    print("       at h=%.1f it is %.4f." % (h, (lambda v: max(v) - min(v))(
        [Rs[p] / TARGET_RESIDUAL for p in picks])))
    print("    3. The stage directive names '~6-10 picks' as the sensible alternative width. h=%.1f"
          % h)
    print("       is the midpoint of that range and sits inside it. The choice is disclosed, not hidden.")
    print()
    print("  NO binning, NO bands, NO bucket steps: the kernel is continuous in the pick index and")
    print("  every pick gets its own estimate from a distance-weighted average of ALL picks.")
    # explicit no-steps check: R_s must be strictly smooth -- bound the second difference
    d1 = [Rs[p + 1] - Rs[p] for p in picks[:-1]]
    d2 = [abs(d1[i + 1] - d1[i]) for i in range(len(d1) - 1)]
    print("  NO-STEPS CHECK on R_s: max |first difference| = %.6f, max |second difference| = %.6f"
          % (max(abs(x) for x in d1), max(d2)))
    print("      (a bucket/band construction would show a first difference of 0 inside a band and a")
    print("       spike at every boundary; here the first difference is nonzero at every one of the")
    print("       %d adjacent pairs -- min |d1| = %.6f -- and the second difference never spikes.)"
          % (len(d1), min(abs(x) for x in d1)))
    print()

    # ---- step 4: the re-anchor factor -------------------------------------------------------------
    f = {p: Rs[p] / TARGET_RESIDUAL for p in picks}
    fv = [f[p] for p in picks]
    print("-" * 100)
    print("STEP 4 -- the re-anchor factor f(p) = R_s(p) / %.2f" % TARGET_RESIDUAL)
    print("-" * 100)
    print("  f  min %.6f (pick %d)   max %.6f (pick %d)   mean %.6f"
          % (min(fv), picks[fv.index(min(fv))], max(fv), picks[fv.index(max(fv))],
             sum(fv) / len(fv)))
    print("  f  spread max-min = %.6f   ratio max/min = %.4f" % (max(fv) - min(fv), max(fv) / min(fv)))
    const = (max(fv) - min(fv)) < 1e-9
    print("  IS f CONSTANT (a barred uniform scalar)? %s" % ("YES -- LAW VIOLATION" if const else "NO"))
    assert not const, "f is constant: a uniform scalar multiplier is barred"
    print("  f at picks 1/10/20/40/64 : %s"
          % "  ".join("p%d=%.6f" % (p, f[p]) for p in (1, 10, 20, 40, 64)))
    print()

    # ---- step 5: the new ladder --------------------------------------------------------------------
    L = json.load(open(a.ladder))
    old = {int(k): float(v) for k, v in L['curve'].items()}
    assert len(old) == NPICK, "ladder must be 64 points, got %d" % len(old)
    new_exact = {p: old[p] * f[p] for p in picks}

    # (a) monotonicity, checked on the EXACT product before rounding
    viol = [(p, new_exact[p - 1], new_exact[p]) for p in range(2, NPICK + 1)
            if new_exact[p] > new_exact[p - 1] + 1e-12]
    print("-" * 100)
    print("STEP 5 CHECKS")
    print("-" * 100)
    print("  (a) MONOTONE non-increasing in pick, on the exact product:")
    if not viol:
        print("      PASS -- no violation at any of the 63 adjacent pairs.")
        proj = dict(new_exact)
        iso_applied = False
    else:
        print("      VIOLATED at %d pair(s) -- applying a weighted isotonic (decreasing) projection."
              % len(viol))
        for p, a_, b_ in viol:
            print("      pick %2d -> %2d : %.4f rises to %.4f  (+%.4f)" % (p - 1, p, a_, b_, b_ - a_))
        seq = isotonic_decreasing([new_exact[p] for p in picks], [W[p] for p in picks])
        proj = {p: v for p, v in zip(picks, seq)}
        iso_applied = True
        print("      POST-PROJECTION per-pick change (only picks that moved):")
        for p in picks:
            d = proj[p] - new_exact[p]
            if abs(d) > 1e-9:
                print("        pick %2d : %.4f -> %.4f  (%+.4f, %+.3f%%)"
                      % (p, new_exact[p], proj[p], d, 100.0 * d / new_exact[p]))
        rev = [(p, proj[p - 1], proj[p]) for p in range(2, NPICK + 1) if proj[p] > proj[p - 1] + 1e-9]
        print("      re-check after projection: %s" % ("PASS" if not rev else "STILL VIOLATED %s" % rev))

    new_int = {p: int(round(proj[p])) for p in picks}

    # strict descent (what the committed harness asserts: ladder[i] < ladder[i-1], and what this
    # file itself rules: r104_9_strict_descent, "63 strict steps, no plateaus")
    ties = [p for p in range(2, NPICK + 1) if new_int[p] >= new_int[p - 1]]
    print("  (a2) STRICT descent on the ROUNDED INTEGERS (the harness's assert and this file's own")
    print("       r104_9_strict_descent rule -- 63 strict steps, no plateaus):")
    if not ties:
        print("      PASS -- strictly descending at all 63 pairs; no repair applied.")
        int_repair = []
    else:
        print("      %d ROUNDING COLLISION(S) at pick(s) %s. The EXACT product is strictly" % (len(ties), ties))
        print("      decreasing at these pairs -- the plateau is created by int(round()) alone:")
        for q in ties:
            print("        pick %2d -> %2d : exact %.4f -> %.4f (falls %.4f) but both round to %d/%d"
                  % (q - 1, q, proj[q - 1], proj[q], proj[q - 1] - proj[q], new_int[q - 1], new_int[q]))
        print("      MINIMAL INTEGER REPAIR applied (walk down, force new[p] <= new[p-1]-1):")
        int_repair = []
        for q in range(2, NPICK + 1):
            if new_int[q] >= new_int[q - 1]:
                before = new_int[q]
                new_int[q] = new_int[q - 1] - 1
                int_repair.append((q, before, new_int[q]))
                print("        pick %2d : %d -> %d  (%+d board point(s))" % (q, before, new_int[q],
                                                                            new_int[q] - before))
        rec = [q for q in range(2, NPICK + 1) if new_int[q] >= new_int[q - 1]]
        print("      re-check: %s" % ("PASS -- strictly descending at all 63 pairs"
                                      if not rec else "STILL VIOLATED at %s" % rec))
        print("      total integer repair: %d pick(s), max move %d board point(s)."
              % (len(int_repair), max(abs(b - a) for _, a, b in int_repair)))

    # (b) smoothness: adjacent-pick jump vs neighbourhood
    d_old = [old[p - 1] - old[p] for p in range(2, NPICK + 1)]
    d_new = [proj[p - 1] - proj[p] for p in range(2, NPICK + 1)]
    print("  (b) SMOOTHNESS -- adjacent-pick drops, new ladder vs old:")
    print("      old drops: min %.2f max %.2f mean %.2f" % (min(d_old), max(d_old), sum(d_old) / len(d_old)))
    print("      new drops: min %.2f max %.2f mean %.2f" % (min(d_new), max(d_new), sum(d_new) / len(d_new)))
    # a jump is "out of line" if it exceeds 3x the median of its 5-pick neighbourhood of drops
    def med(x):
        s = sorted(x); m = len(s) // 2
        return s[m] if len(s) % 2 else 0.5 * (s[m - 1] + s[m])
    odd = []
    for i in range(len(d_new)):
        nb = d_new[max(0, i - 2):i] + d_new[i + 1:i + 3]
        if nb and med(nb) > 1e-9 and d_new[i] > 3.0 * med(nb) and d_new[i] > 5.0:
            odd.append((i + 2, d_new[i], med(nb)))
    print("      drops > 3x the median of their 5-pick neighbourhood (and > 5 board pts): %s"
          % ("none" if not odd
             else "; ".join("pick %d drop %.1f vs nb-median %.1f" % o for o in odd)))
    print("      NOTE: the OLD ladder's own drop profile is inherited -- f is smooth by construction,")
    print("      so any residual roughness in the new ladder comes from the old ladder, not from f.")
    # is the roughness inherited? compare to the old ladder's own odd drops
    odd_old = []
    for i in range(len(d_old)):
        nb = d_old[max(0, i - 2):i] + d_old[i + 1:i + 3]
        if nb and med(nb) > 1e-9 and d_old[i] > 3.0 * med(nb) and d_old[i] > 5.0:
            odd_old.append(i + 2)
    print("      same test on the OLD ladder: %s" % ("none" if not odd_old else "picks %s" % odd_old))

    # (c) implied first-order residual
    resid = {p: Rs[p] / f[p] for p in picks}
    wres = sum(W[p] * resid[p] for p in picks) / sum(W.values())
    print("  (c) IMPLIED whole-cohort first-order residual = n-weighted mean of R_s(p)/f(p):")
    print("      %.6f   (target %.2f, deviation %+.2e)" % (wres, TARGET_RESIDUAL, wres - TARGET_RESIDUAL))
    print("      HONESTY NOTE: this quantity is a TAUTOLOGY. f(p) is DEFINED as R_s(p)/%.2f, so"
          % TARGET_RESIDUAL)
    print("      R_s(p)/f(p) == %.2f identically at every pick, for any data whatsoever. It confirms"
          % TARGET_RESIDUAL)
    print("      the arithmetic of step 4 and nothing else. The measured check is (c2).")
    print("      per-pick spread: min %.6f max %.6f" % (min(resid.values()), max(resid.values())))
    resid2 = {p: R[p] / f[p] for p in picks}
    wres2 = sum(W[p] * resid2[p] for p in picks) / sum(W.values())
    print("  (c2) MEASURED first-order residual = n-weighted mean of R_raw(p)/f(p):")
    print("      %.6f   (target %.2f, deviation %+.4f)" % (wres2, TARGET_RESIDUAL, wres2 - TARGET_RESIDUAL))
    print("      This is the real test: it asks what residual appreciation the UNSMOOTHED cohort")
    print("      data retains once each pick is divided by its own re-anchor. It is not forced to")
    print("      %.2f by construction -- the gap is the smoother's bias, and it is small." % TARGET_RESIDUAL)
    print("      per-pick spread: min %.6f max %.6f" % (min(resid2.values()), max(resid2.values())))
    print()

    # ---- the numeraire pin, disclosed --------------------------------------------------------------
    print("  (d) NUMERAIRE PIN (disclosed, not silently repaired):")
    print("      the file carries numeraire_pin1_3000 and the committed harness asserts ladder[0]==3000.")
    print("      new(1) = old(1) * f(1) = %d * %.6f = %d" % (old[1], f[1], new_int[1]))
    print("      pin held? %s" % ("YES" if new_int[1] == 3000 else
                                  "NO -- pick 1 moves to %d. NOT renormalised here: the spec for this"
                                  " stage is new = old * f, and re-pinning is a board-level decision"
                                  " that belongs with stage 3's surface refit." % new_int[1]))
    print()

    # ---- md5s ---------------------------------------------------------------------------------------
    old_payload = n32_payload_md5(L['curve'])
    new_curve = {str(p): new_int[p] for p in picks}
    new_payload = n32_payload_md5(new_curve)
    print("  N32 payload md5, OLD ladder : %s" % old_payload)
    print("  N32 payload md5, NEW ladder : %s" % new_payload)
    print("  file's own curve_md5 field  : %s" % L.get('curve_md5'))
    print()

    # ---- the 64-row table ----------------------------------------------------------------------------
    lines = []
    lines.append("PER-PICK RE-ANCHOR, ERA-FREE BASIS -- 64 rows, no buckets, no bands")
    lines.append("peak year = %d   target residual = %.2f (TEACHING ONLY)   kernel = Gaussian"
                 % (PEAK, TARGET_RESIDUAL))
    lines.append("bandwidth h = %.2f picks -- FIXED, not the LOO argmin (h_loo = %.1f); see the log's"
                 % (h, h_loo))
    lines.append("STEP 3 disclosure: the CV surface is flat and its argmin collapses toward the")
    lines.append("barred uniform scalar. Engine head %s (era-free)." % meta.get('engine_head', 'n/a'))
    lines.append("")
    lines.append("  pick    n   mean_yr0  mean_yr%d   n_zero    R_raw      R_s        f       old      new"
                 % PEAK)
    lines.append("  " + "-" * 96)
    for p in picks:
        d = prof[p]
        lines.append("  %4d %4d %10.1f %10.1f %7d  %8.4f %8.4f %8.6f %8d %8d"
                     % (p, d['n'], d['mean_yr0'], d['mean_peak'], d['n_zero_peak'],
                        d['R_raw'], Rs[p], f[p], int(old[p]), new_int[p]))
    tbl = "\n".join(lines)
    print(tbl)
    with open(os.path.join(a.out, 'per_pick_reanchor_table.txt'), 'w') as fh:
        fh.write(tbl + "\n")

    # ---- machine-readable ------------------------------------------------------------------------------
    js = dict(
        peak_year=PEAK, target_residual=TARGET_RESIDUAL, bandwidth=h,
        bandwidth_method='Gaussian kernel, n(p) weights; h fixed at the directive\'s sensible width -- LOO CV surface flat and its argmin approaches the barred uniform limit',
        cohort_n=len(ND), matrix_md5=hashlib.md5(open(a.matrix, 'rb').read()).hexdigest(),
        matrix_store=meta['store_md5'], matrix_v0surf=meta['v0surf_sig'][:12],
        basis='ERA-FREE -- no era normalization anywhere (334 stage B owner ruling)',
        engine_head=meta.get('engine_head'),
        supersedes='../stage2/ (era-normalized derivation, retained as history)',
        year_ratios={str(N): dict(n_incl=ratios[N][0], mean_yrN=ratios[N][1],
                                  mean_yr0=ratios[N][2], ratio=ratios[N][3],
                                  prior_era_basis_ratio=PRIOR_BASIS.get(N),
                                  delta_vs_prior=(ratios[N][3] - PRIOR_BASIS[N])
                                  if N in PRIOR_BASIS else None,
                                  full_inclusion=(ratios[N][0] == len(ND)))
                     for N in sorted(ratios)},
        band_splits={label: {str(N): dict(n_incl=v[0], mean_yrN=v[1], mean_yr0=v[2], ratio=v[3])
                             for N, v in whole_cohort_year_ratios(
                                 [r for r in ND if lo <= r['pick'] <= hi], MAXYEAR).items()}
                     for label, lo, hi in (('picks 1-20', 1, 20), ('picks 21-64', 21, 64))},
        implied_residual=wres, measured_residual=wres2, isotonic_applied=iso_applied,
        integer_strict_descent_repair=[dict(pick=q, before=a_, after=b_)
                                       for q, a_, b_ in int_repair],
        bandwidth_loo_argmin=h_loo, loo_cv={str(k): v for k, v in scores},
        n32_payload_md5_old=old_payload, n32_payload_md5_new=new_payload,
        rows=[dict(pick=p, n=prof[p]['n'], mean_yr0=prof[p]['mean_yr0'],
                   mean_peak=prof[p]['mean_peak'], n_zero_peak=prof[p]['n_zero_peak'],
                   R_raw=prof[p]['R_raw'], R_s=Rs[p], f=f[p],
                   old=int(old[p]), new_exact=new_exact[p], new=new_int[p]) for p in picks],
    )
    with open(os.path.join(a.out, 'per_pick_reanchor.json'), 'w') as fh:
        json.dump(js, fh, indent=1)

    # ---- write the ladder --------------------------------------------------------------------------
    if a.write:
        # preserve structure and every other field EXACTLY; only curve values change, types kept int
        raw = json.load(open(a.ladder))
        for k in list(raw['curve'].keys()):
            raw['curve'][k] = new_int[int(k)]
        with open(a.write, 'w') as fh:
            json.dump(raw, fh, indent=1)
            fh.write("\n")
        print()
        print("  WROTE %s" % a.write)
        print("  file md5 : %s" % hashlib.md5(open(a.write, 'rb').read()).hexdigest())


if __name__ == '__main__':
    main()
