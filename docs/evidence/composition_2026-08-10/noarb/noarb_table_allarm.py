"""noarb_table_allarm.py — THE ALL-ARM COHORT INSTRUMENT (owner ruling, #334 ORDER 7).

  "a cohort is all players drafted through mechanisms that are eligible to debut in the same year
   (for example, the most recent cohort is ND, RD, SSP in 2025 + MSD in 2026)."   -- the owner

A SIBLING of noarb_table_338.py. THAT FILE IS NOT MODIFIED AND IS NOT IMPORTED FOR ITS FILTER: its md5
is asserted here (0f8220351c64c56ccfa90c60edcdfa5f) so a reader can see the canonical instrument was
untouched by this act.

WHY NO NEW EMIT. The per-entrant matrices already carry EVERY row (2645), every arm included — it was
only the canonical READER that filtered to ND picks 1-64. So this table is produced from the SAME
matrices already emitted for each engine variant, and any difference between the two instruments is the
POPULATION, never the engine.

THE COHORT KEY, the owner's rule implemented literally and nowhere else in this file:
      cohort(p) = draft year + 1,   except MSD, where cohort(p) = draft year
which is the engine's own debutyr convention (MSD debuts in its entry year, every other route the year
after), and which puts ND+RD+SSP of 2025 with MSD of 2026 in cohort 2026 — the owner's worked example.

VALUE SEMANTICS — the canonical reader's, re-stated on the COHORT clock instead of the draft clock.
  cohort year 0  = the entrant's own v0 (his year-zero price under THIS engine variant).
  cohort year N  = his as-of price in calendar year (cohort + N - 1), looked up BY CALENDAR YEAR in the
                   matrix's own `yrs` list rather than by a positional index, because the arms do not
                   share a draft-to-debut offset and a positional index would silently mis-align MSD.
  past the end   = 0.0 ('ended'), kept in the denominator, exactly the standing order.
  before the start = EXCLUDED from that row, not scored zero ('pre'). This is the disclosed MSD gap:
                   the emitter builds `yrs` from draft year + 1, so an MSD entrant's cohort year 1 (his
                   debut season) is not carried. Scoring it 0 would be a false statement about a player
                   who played, so the row is excluded from that year and the count is PRINTED.

  usage:  OPENBLAS_NUM_THREADS=1 python noarb_table_allarm.py <matrix.json> [label]
"""
import os, sys, json, hashlib, statistics
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
CANON = os.path.join(HERE, 'noarb_table_338.py')
CANON_MD5 = '0f8220351c64c56ccfa90c60edcdfa5f'
_m = hashlib.md5(open(CANON, 'rb').read()).hexdigest()
assert _m == CANON_MD5, "canonical instrument md5 moved: %s != %s" % (_m, CANON_MD5)

MATRIX = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else os.path.basename(MATRIX)
WINDOWS = [('PRIMARY  cohorts 2005-2023', 2005, 2023), ('MODERN   cohorts 2019-2023', 2019, 2023)]
YEARS = list(range(0, 8))

D = json.load(open(MATRIX))
meta, R = D['meta'], D['recs']
# the identity pins, asserted the same way the harness asserts them
assert meta['store_md5'][:8] == 'd9a24282', "store pin moved: %s" % meta['store_md5']
assert meta['v0surf_sig'][:12] == '6ef67f07db98', "v0surf pin moved: %s" % meta['v0surf_sig']
# WINDOW END, DERIVED EXACTLY AS THE CANONICAL READER DERIVES IT, and for its stated reason: the
# emitter writes a PLACEHOLDER yrs=[C+1] with vpath=[None] for a class with no season yet, so the 2026
# draft class carries yrs=[2027]. Using max(yrs) would push the window a year past the real data and
# silently score a whole class at 0. CAUGHT BY THE P7.1 SELF-CHECK: the first cut of this file used
# max(yrs), got WINDOW_END 2027, admitted the 2022 class into cohort year 5 and read 1.4515 where the
# canonical reads 1.5328. The self-check existed to catch exactly that and it did.
WINDOW_END = max(y for r in R
                 for y, v in zip(r.get('yrs') or [], r.get('vpath') or []) if v is not None)


def cohort(r):
    y = r.get('year')
    if y is None: return None
    return y if r.get('type') == 'MSD' else y + 1


def value_at(r, N):
    """(value, kind) at COHORT year N. kind in {'v0','path','ended','null','pre'}."""
    if N == 0:
        return float(r['v0']), 'v0'
    Y = cohort(r) + N - 1
    yrs = r.get('yrs') or []
    vp = r.get('vpath') or []
    if not yrs:
        return 0.0, 'ended'
    if Y < yrs[0]:
        return None, 'pre'                      # before the emitted window (the MSD debut-year gap)
    if Y > yrs[-1]:
        return 0.0, 'ended'                     # career concluded -> 0, kept in the denominator
    i = yrs.index(Y)
    if vp[i] is None:
        return 0.0, 'null'
    return float(vp[i]), 'path'


elig = [r for r in R if cohort(r) is not None and (r.get('v0') or 0) > 0]
L = []
def P(s=''):
    print(s); L.append(s)

P("=" * 112)
P("ALL-ARM COHORT PROGRESSION — %s" % LABEL)
P("=" * 112)
P("  OWNER RULING: a cohort is every player drafted through mechanisms eligible to debut in the SAME")
P("  YEAR. ND + RD + SSP of year Y sit with MSD of year Y+1. This is that instrument.")
P("  matrix        : %s" % os.path.basename(MATRIX))
P("  store         : %s   v0surf %s   window end %d" % (meta['store_md5'][:8], meta['v0surf_sig'][:12], WINDOW_END))
P("  canonical file: noarb_table_338.py UNMODIFIED, md5 %s (asserted at run)" % CANON_MD5)
P("  excluded      : %d rows of %d (no draft year, or v0 <= 0)" % (len(R) - len(elig), len(R)))
P("  aggregation   : pooled book ratio, mean(value at cohort year N) / mean(v0) over the SAME set")
P("  year 0        : each entrant's OWN v0 under this engine variant (v0 moves with the pool arm's")
P("                  own year-zero repair, so the denominator is arm-appropriate by measurement)")
P()

OUT = {}
for wname, lo, hi in WINDOWS:
    pop = [r for r in elig if lo <= cohort(r) <= hi]
    arms = Counter(r['type'] for r in pop)
    P("-" * 112)
    P("### %s   n = %d" % (wname, len(pop)))
    P("-" * 112)
    P("  arms: " + "  ".join("%s %d" % (t, n) for t, n in sorted(arms.items(), key=lambda x: -x[1])))
    hdr = ("  %-4s %7s %7s %8s %8s %11s %11s %9s" %
           ("yrN", "n_incl", "n_zero", "n_notyet", "n_pre", "mean_yrN", "mean_yr0", "ratio"))
    P(hdr); P("  " + "-" * (len(hdr) - 2))
    rows = []
    for N in YEARS:
        reached = pop if N == 0 else [r for r in pop if cohort(r) + N - 1 <= WINDOW_END]
        notreach = len(pop) - len(reached)
        vals, v0s, kinds, npre = [], [], [], 0
        for r in reached:
            v, k = value_at(r, N)
            kinds.append(k)
            if k == 'pre':
                npre += 1
                continue                        # excluded from THIS year, never scored zero
            vals.append(v); v0s.append(float(r['v0']))
        mN = statistics.mean(vals) if vals else float('nan')
        m0 = statistics.mean(v0s) if v0s else float('nan')
        ratio = (mN / m0) if m0 else float('nan')
        nzero = sum(1 for v in vals if v == 0.0)
        P("  %-4d %7d %7d %8d %8d %11.1f %11.1f %9.4f"
          % (N, len(vals), nzero, notreach, npre, mN, m0, ratio))
        rows.append(dict(N=N, n_included=len(vals), n_zero=nzero, n_not_yet_reached=notreach,
                         n_pre_excluded=npre, mean_yearN=round(mN, 2),
                         mean_year0_same_set=round(m0, 2), ratio_meanN_over_mean0=round(ratio, 4),
                         kinds={k: kinds.count(k) for k in set(kinds)}))
    P("  n_pre = rows whose cohort year N precedes the emitted window (the disclosed MSD debut-year")
    P("          gap). They are EXCLUDED from that year, never scored zero.")
    P()
    # per-arm year-1 and year-4, so no arm can hide inside the pooled number
    P("  BY ARM (pooled ratio within the arm, same construction):")
    P("    %-6s %6s %9s %9s %9s" % ("arm", "n", "yr1", "yr4", "yr1 mean_v0"))
    per = {}
    for t in sorted(arms, key=lambda t: -arms[t]):
        sub = [r for r in pop if r['type'] == t]
        cells = {}
        for N in (1, 4):
            reached = [r for r in sub if cohort(r) + N - 1 <= WINDOW_END]
            vv, zz = [], []
            for r in reached:
                v, k = value_at(r, N)
                if k == 'pre': continue
                vv.append(v); zz.append(float(r['v0']))
            cells[N] = (statistics.mean(vv) / statistics.mean(zz)) if vv and statistics.mean(zz) else float('nan')
            if N == 1: m0a = statistics.mean(zz) if zz else float('nan')
        P("    %-6s %6d %9.4f %9.4f %9.1f" % (t, len(sub), cells[1], cells[4], m0a))
        per[t] = dict(n=len(sub), yr1=round(cells[1], 4), yr4=round(cells[4], 4))
    P()
    OUT[wname] = dict(n=len(pop), arms=dict(arms), rows=rows, by_arm=per)

# the self-check the pre-registration named as P7.1
P("-" * 112)
P("### SELF-CHECK (P7.1) — the CANONICAL population, read by THIS reader")
P("-" * 112)
canon = [r for r in elig if r['type'] == 'ND' and r.get('pick') and 1 <= r['pick'] <= 64
         and 2005 <= cohort(r) <= 2023 and r.get('teaches_curve')]
P("  n = %d  (the canonical instrument's own population is 1197)" % len(canon))
cr = {}
for N in YEARS:
    reached = canon if N == 0 else [r for r in canon if cohort(r) + N - 1 <= WINDOW_END]
    vv, zz = [], []
    for r in reached:
        v, k = value_at(r, N)
        if k == 'pre': continue
        vv.append(v); zz.append(float(r['v0']))
    cr[N] = (statistics.mean(vv) / statistics.mean(zz)) if vv else float('nan')
P("  " + "  ".join("yr%d %.4f" % (N, cr[N]) for N in YEARS[:6]))
P("  These must match noarb_table_338.py's own ratios for the same variant, or nothing above is readable.")
OUT['self_check_canonical'] = dict(n=len(canon), ratios={N: round(cr[N], 4) for N in YEARS})

json.dump(dict(matrix=os.path.basename(MATRIX), label=LABEL, store=meta['store_md5'],
               v0surf=meta['v0surf_sig'], window_end=WINDOW_END,
               canonical_instrument_md5=CANON_MD5, groups=OUT),
          open(os.path.join(HERE, 'allarm_%s.json' % LABEL), 'w'), indent=1)
open(os.path.join(HERE, 'allarm_%s.txt' % LABEL), 'w').write('\n'.join(L) + '\n')
