"""RECONCILIATION GATE — does my aggregation reproduce the canonical historical output?

THE ORDER: "before trusting your own choice again, RECONCILE the form against the canonical
historical output (the stage-5 noarb table in the evidence and the owner-basis re-emit at
stage-b tip 3820303) — match their exact aggregation, cohort labeling incl. the MSD offset,
and presentation shape."

This script does NOT read any of my act's emits. It re-implements the aggregation from scratch
and runs it against the SAME stage-5 matrix the canonical owner-basis table consumed, then
diffs against the canonical committed numbers. If it does not match to 1e-12, the rebuilt
reader is not trustworthy and the decision table must not be printed.

PRE-REGISTERED EXPECTATIONS (written before the first run, per HALT-NO-SURPRISE).
Targets are read out of OWNER_BASIS_COHORT.json at stage-b tip 3820303, state "s5 LANDED",
table_4_full_cohort_path — the full cohort book, all routes, cohorts 2004-2025:

    yr0  n=2535  1.0
    yr1  n=2517  0.9460496098408091
    yr2  n=2414  1.1112251275413227
    yr3  n=2296  1.2460161076427445
    yr4  n=2198  1.3454616923441254
    yr5  n=2089  1.3469226008389965
    yr6  n=1981  1.2957679202997474
    yr7  n=1893  1.1448858108433444

If n matches but the ratio does not, my value convention is wrong.
If n does not match, my population/window/MSD rule is wrong.
Either way: STOP and record. Do not tune the reader until it agrees.

ONE KNOWN RISK, stated in advance: the canonical script aggregated over the KEY INTERSECTION of
the six matrices it compared. This gate reads ONE matrix, so its population is that file's own
keys. If the six states shared a population the counts coincide and the match is exact; if they
did not, my n will come out HIGHER than canonical and that is a population difference, not a
form error — it would be reported as such, not patched away.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
STAGE5 = SP + '/per_entrant_338_stage5.json'
CANON = SP + '/OWNER_BASIS_COHORT.json'

WINDOW_END = 2026
COHORT_LO, COHORT_HI = 2004, 2025

# ---------------------------------------------------------------- canonical value convention
# Copied in FORM from docs/evidence/act_334B_2026-08-07/owner_basis_COHORT_RULE/owner_basis_cohort.py
# at 3820303 (val / ratio), which itself follows the committed stage5/owner_basis.py:
#   year 0 = v0; year N = vpath[N-1]; a bust / concluded career scores 0 and STAYS in the
#   denominator; an entrant that has not reached year N (LABEL year + N > WINDOW_END) is excluded
#   from that row entirely; rows with v0 <= 0 are excluded.


def val(r, n):
    if r['year'] + n > WINDOW_END:
        return None
    if n == 0:
        return float(r['v0'])
    vp = r.get('vpath') or []
    if n - 1 >= len(vp):
        return 0.0
    v = vp[n - 1]
    return 0.0 if v is None else float(v)


def book_ratio(recs, keys, n):
    """THE CANONICAL AGGREGATION: pooled book ratio, sum(price) / sum(anchor).

    NOT the mean of per-player ratios (that star-skews), and NOT per-cohort-then-averaged
    (the canonical pools; see the note this gate prints).
    """
    num = den = 0.0
    cnt = 0
    for k in keys:
        r = recs[k]
        a, b = val(r, n), val(r, 0)
        if a is None or b is None or b <= 0:
            continue
        num += a
        den += b
        cnt += 1
    return (num / den if den else float('nan')), cnt


def mean_of_ratios(recs, keys, n):
    """THE ARTIFACT FORM my earlier reader used, kept only to show the size of the error."""
    rs = []
    for k in keys:
        r = recs[k]
        a, b = val(r, n), val(r, 0)
        if a is None or b is None or b <= 0:
            continue
        rs.append(a / b)
    return (sum(rs) / len(rs) if rs else float('nan')), len(rs)


def cohort_of(k):
    """THE OWNER'S RULE: cohort N = every entrant whose YEAR 1 is season N+1.
    The MSD is drafted mid-season, so an MSD labelled year Y belongs to cohort Y-1."""
    key, typ, yr = k
    return yr - 1 if typ == 'MSD' else yr


def load(path):
    return {(r['key'], r['type'], r['year']): r for r in json.load(open(path))['recs']}


def main():
    if not os.path.exists(STAGE5):
        print('MISSING stage-5 matrix: %s' % STAGE5)
        return 2
    recs = load(STAGE5)
    canon = json.load(open(CANON))['table_4_full_cohort_path']

    keys = [k for k in sorted(recs) if COHORT_LO <= cohort_of(k) <= COHORT_HI]

    print('=' * 96)
    print('RECONCILIATION GATE — my aggregation vs the canonical owner-basis output (3820303)')
    print('=' * 96)
    print('  matrix under test : per_entrant_338_stage5.json (the stage-5 landed matrix)')
    print('  canonical source  : OWNER_BASIS_COHORT.json @ 3820303, state "s5 LANDED"')
    print('  aggregation       : POOLED BOOK RATIO  sum(price)/sum(anchor)')
    print('  cohort rule       : MSD folds back one year (cohort_of), cohorts %d-%d'
          % (COHORT_LO, COHORT_HI))
    print('  window            : label year + N <= %d' % WINDOW_END)
    print('  members in scope  : %d' % len(keys))
    print('-' * 96)
    print('  %-4s %8s %8s   %-22s %-22s %12s' %
          ('yrN', 'n_mine', 'n_canon', 'mine', 'canonical', 'delta'))
    ok = True
    for n in range(0, 8):
        mine, cnt = book_ratio(recs, keys, n)
        c = canon[str(n)]
        cr, cn = float(c['s5']), int(c['n'])
        d = mine - cr
        flag = '' if (cnt == cn and abs(d) < 1e-12) else '   <-- MISMATCH'
        if flag:
            ok = False
        print('  %-4d %8d %8d   %-22.16f %-22.16f %12.2e%s' % (n, cnt, cn, mine, cr, d, flag))
    print('-' * 96)
    print('  VERDICT: %s' % ('PASS — the rebuilt aggregation reproduces the canonical output exactly'
                             if ok else 'FAIL — DO NOT TRUST THE REBUILT READER; halt and report'))
    print()

    # ------------------------------------------------------------ both aggregations, side by side
    print('=' * 96)
    print('BOTH AGGREGATIONS SIDE BY SIDE — for the record of why the correction mattered')
    print('=' * 96)
    print('  Same matrix, same population, same value convention. The ONLY difference is how the')
    print('  per-player numbers are combined.')
    print('-' * 96)
    print('  %-4s %8s   %-18s %-18s %10s' %
          ('yrN', 'n', 'BOOK RATIO', 'mean-of-ratios', 'inflation'))
    print('  %-4s %8s   %-18s %-18s %10s' %
          ('', '', 'sum(v)/sum(v0)', 'mean(v/v0)', 'x'))
    print('  ' + '-' * 62)
    for n in range(0, 8):
        b, cnt = book_ratio(recs, keys, n)
        m, _ = mean_of_ratios(recs, keys, n)
        print('  %-4d %8d   %-18.6f %-18.6f %10.3f' % (n, cnt, b, m, (m / b) if b else float('nan')))
    print('-' * 96)
    print('  The mean-of-ratios column is star-skewed: a player whose v0 is small and whose career')
    print('  value is large contributes an enormous per-player ratio that the average cannot damp,')
    print('  while the book ratio weights every dollar of anchor equally. That is the whole of the')
    print('  292%/392% artifact — it was never a property of the engine.')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
