"""noarb_table.py -- whole-cohort mean/median engine value at year 0..7 after draft.

READ-ONLY. Writes nothing into the repo tree. Re-runnable.

  usage:  OPENBLAS_NUM_THREADS=1 /root/rl_venv312/bin/python noarb_table.py [matrix.json]

POPULATION / FILTER
  The population is taken by CALLING the harness's own loader,
  harness_pvc_REPINNED.pass3.load_matrix(), not by re-implementing it. That filter is:
        r['teaches_curve'] and r['pick'] and 1 <= r['pick'] <= 64 and 2004 <= r['year'] <= 2022
  (ND_LAST=64, YR_LO=2004, CLASS_CUT=2022). The loader also asserts the matrix identity pins
  (store 81d24704, v0surf 1cbbd9b00ff4) and the population size EXPECT_N=1197.

VALUE SEMANTICS (read from the emitter, not guessed)
  emit_matrix_271.py lines 137-138 / 166:
        yrs   = list(range(C + 1, yend + 1))          # C = the player's draft year
        Vpath = [ASOF.get((id(p), y)) for y in yrs]   # ASOF[(p,Y)] = ev(p, Y) walk-forward
  so vpath[i] is the engine's as-of valuation ev(p, C+1+i) computed with that player's scoring
  record truncated to seasons <= C+1+i (emitter lines 100-118). Therefore:
        year N >= 1  ->  vpath[N-1]
        year 0       ->  r['v0'] = v0_start(p), the engine's year-zero (draft-day) value.
  yend = last active season for a concluded career, else the window end. So a player whose career
  ended before year N simply HAS NO vpath entry at N -- that is the bust, and it is scored 0 and
  KEPT IN THE DENOMINATOR, per the standing order.
"""
import os, sys, json, math, statistics

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import harness_pvc_REPINNED_pass3 as H   # symlink/copy of the committed harness (dots -> underscores)

MATRIX = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'pass3_matrix.json')
YEARS = list(range(0, 8))
GROUPS = [('ALL picks 1-64', lambda r: True),
          ('picks 1-20',     lambda r: 1 <= r['pick'] <= 20),
          ('picks 21-64',    lambda r: 21 <= r['pick'] <= 64)]

CAPTIONS = [
 "Values are the ENGINE'S OWN as-of valuations ev(p,Y) (walk-forward), NOT raw scores or raw output.",
 "Early-career years lean heavily on the year-zero estimate -- the engine has little evidence yet.",
 "Denomination: VOR board points (pick-1 pinned at 3000).",
 "This is measured on the PRE-CLOSURE basis matrix (surface b683e2ec era). The landed basis will",
 "  differ by about the closure residual (<= 1 ladder point per pick).",
 "Busts stay in the denominator at 0. Players whose careers have not yet reached year N are",
 "  EXCLUDED from year N and reported separately as 'not yet reached'.",
]


def value_at(r, N):
    """Return (value, kind) for year N after the draft year. kind in
    {'v0','path','ended','null'}. 'ended' = career concluded before year N -> 0 by the standing order."""
    if N == 0:
        return float(r['v0']), 'v0'
    vp = r.get('vpath') or []
    yrs = r.get('yrs') or []
    i = N - 1
    if i >= len(vp):
        return 0.0, 'ended'
    # index/year alignment is an ASSERT, never an assumption
    assert yrs[i] == r['year'] + N, \
        "yrs misalignment: key=%s yrs[%d]=%s expected %d" % (r['key'], i, yrs[i], r['year'] + N)
    if vp[i] is None:
        return 0.0, 'null'
    return float(vp[i]), 'path'


def main():
    meta, ND = H.load_matrix(MATRIX)
    full = json.load(open(MATRIX))['recs']

    # WINDOW END, DERIVED FROM THE DATA: the last calendar year at which ANY record in the whole
    # matrix carries a real (non-null) as-of valuation. NOT max(yrs): the emitter's
    #   yrs = range(C+1, yend+1) if yend >= C+1 else [C+1]
    # emits a placeholder yrs=[C+1] for a class with no season yet, so the 2026 draft class
    # carries yrs=[2027] with vpath=[None]. Using max(yrs) would push the window one year past
    # the real data and silently score a whole draft class at 0.
    WINDOW_END = max(y for r in full
                     for y, v in zip(r.get('yrs') or [], r.get('vpath') or []) if v is not None)
    PLACEHOLDER_MAX = max(max(r['yrs']) for r in full if r.get('yrs'))
    draft_years = sorted({r['year'] for r in ND})

    print("=" * 100)
    print("WHOLE-COHORT ENGINE VALUE BY YEAR AFTER DRAFT  --  year 0..7")
    print("=" * 100)
    for c in CAPTIONS:
        print("  " + c)
    print("-" * 100)
    print("  matrix          : %s" % os.path.basename(MATRIX))
    print("  matrix identity : store=%s  v0surf=%s  n_records=%d"
          % (meta['store_md5'], meta['v0surf_sig'][:12], meta['n_records']))
    print("  population      : harness load_matrix ND filter -- teaches_curve & pick 1..64 & "
          "year %d..%d" % (H.YR_LO, H.CLASS_CUT))
    print("  cohort size     : %d entrants" % len(ND))
    print("  draft classes   : %d..%d (%d distinct classes)"
          % (draft_years[0], draft_years[-1], len(draft_years)))
    print("  observed window : as-of years end at %d (last year ANY record carries a real "
          "as-of value)" % WINDOW_END)
    print("                    (max yrs label in the matrix is %d, but it is a placeholder row "
          "with vpath=[None])" % PLACEHOLDER_MAX)
    print("  inclusion at N  : draft_year + N <= %d" % WINDOW_END)
    print("  value field     : year 0 = rec['v0'] (v0_start); year N>=1 = rec['vpath'][N-1] "
          "= ev(p, draft_year+N)")
    print("-" * 100)

    out = {}
    for gname, gfilt in GROUPS:
        pop = [r for r in ND if gfilt(r)]
        print()
        print("### %s   (cohort n=%d)" % (gname, len(pop)))
        hdr = ("  %-4s %7s %7s %8s %10s %10s %10s %10s %8s"
               % ("yrN", "n_incl", "n_zero", "notreach", "mean_yrN", "med_yrN",
                  "mean_yr0*", "med_yr0*", "ratio"))
        print(hdr)
        print("  " + "-" * (len(hdr) - 2))
        rows = []
        for N in YEARS:
            incl = [r for r in pop if r['year'] + N <= WINDOW_END]
            notreach = len(pop) - len(incl)
            vals, kinds = [], []
            for r in incl:
                v, k = value_at(r, N)
                vals.append(v); kinds.append(k)
            v0s = [float(r['v0']) for r in incl]
            nzero = sum(1 for v in vals if v == 0.0)
            mN = statistics.mean(vals) if vals else float('nan')
            m0 = statistics.mean(v0s) if v0s else float('nan')
            medN = statistics.median(vals) if vals else float('nan')
            med0 = statistics.median(v0s) if v0s else float('nan')
            ratio = (mN / m0) if m0 else float('nan')
            print("  %-4d %7d %7d %8d %10.1f %10.1f %10.1f %10.1f %8.3f"
                  % (N, len(incl), nzero, notreach, mN, medN, m0, med0, ratio))
            rows.append(dict(N=N, n_included=len(incl), n_zero=nzero, n_not_yet_reached=notreach,
                             mean_yearN=round(mN, 2), median_yearN=round(medN, 2),
                             mean_year0_same_set=round(m0, 2), median_year0_same_set=round(med0, 2),
                             ratio_meanN_over_mean0=round(ratio, 4),
                             zero_kinds={k: kinds.count(k) for k in set(kinds)}))
        print("  * mean_yr0 / med_yr0 are computed over the SAME included set as that row "
              "(apples-to-apples).")
        out[gname] = dict(cohort_n=len(pop), rows=rows)

    # zero-source breakdown for the ALL group, so 'zero' is never an unexplained bucket
    print()
    print("### zero-source breakdown, ALL picks 1-64  (how each included row got its number)")
    print("  %-4s %10s %10s %8s %8s" % ("yrN", "from_v0", "from_path", "ended", "null"))
    for N in YEARS:
        incl = [r for r in ND if r['year'] + N <= WINDOW_END]
        kinds = [value_at(r, N)[1] for r in incl]
        print("  %-4d %10d %10d %8d %8d" % (N, kinds.count('v0'), kinds.count('path'),
                                            kinds.count('ended'), kinds.count('null')))

    jp = os.path.join(HERE, 'noarb_table.json')
    json.dump(dict(matrix=os.path.basename(MATRIX), store=meta['store_md5'],
                   v0surf=meta['v0surf_sig'], window_end=WINDOW_END,
                   draft_years=[draft_years[0], draft_years[-1]],
                   captions=CAPTIONS, groups=out), open(jp, 'w'), indent=1)
    print()
    print("json -> %s" % jp)


if __name__ == '__main__':
    main()
