"""THE OWNER-BASIS COHORT TABLES + THE NO-ARB PER-ENTRY-YEAR VIEW, per engine variant. READ-ONLY.

INSTRUMENT OF RECORD: the per-entrant matrices emitted by emit_matrix_338.py (one per engine
variant). NOT a live-board cross-section — that was the basis error the owner caught.

THE COHORT RULE (his words, #334 comment 5235016488; register v611/v616):
    "The 2025 cohort is NOT the 2025 MSD. The 2025 MSD played in 2025, so that is their year 1.
     The 2025 cohort is 2025 ND, 2025 RD, 2025 pathways, SSP, 2026 MSD."
    "We're not balancing the ND book, we're balancing the cohort book."
So COHORT N = every entrant whose YEAR 1 is season N+1, whatever route: entrants labelled year N on
every route EXCEPT MSD, plus MSD entrants labelled year N+1 (the mid-season draft happens inside
their year-1 season). No route is excluded.

YEAR-N IS THE AVERAGE OVER ALL COHORTS AT YEAR N — never a single class read as a rung. That is the
property the owner named and the one my cross-sectional tables violated.

Every figure is labelled with its instrument. Anchor-relative (no-arb) form throughout: each
entrant's year-N value is divided by his OWN year-0 value, so cohorts of different absolute size
compose without one class dominating.
"""
import os, sys, json, collections
import numpy as np

SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
YR_LO, YR_HI = 2004, 2022
NMAX = 5

VARIANTS = [("main (pre-act)", "main"), ("FULL (the package)", "FULL"),
            ("V2 four-band", "V2"), ("V3 corrected", "V3"), ("V1 13/15", "V1")]


def load(tag):
    p = SP + "/per_entrant_%s.json" % tag
    if not os.path.exists(p): return None
    return json.load(open(p))["recs"]


def cohort_of(r):
    """COHORT N under the owner's rule: MSD entrants belong to the cohort of year-1, i.e. year-1."""
    y = r.get("year")
    if y is None: return None
    return (y - 1) if r.get("type") == "MSD" else y


def v(r, n):
    """value at career year n; n=0 is the entry value."""
    if n == 0:
        v0 = r.get("v0")
        return float(v0) if v0 else None
    vp = r.get("vpath") or []
    if n - 1 >= len(vp): return None
    x = vp[n - 1]
    return None if x is None else float(x)


def rows(recs):
    out = []
    for r in recs:
        c = cohort_of(r)
        if c is None or not (YR_LO <= c <= YR_HI): continue
        v0 = v(r, 0)
        if not v0 or v0 <= 0: continue
        out.append((c, r, v0))
    return out


def cohort_progression(recs):
    """year-N = the AVERAGE OVER COHORTS of that cohort's mean anchor-relative value at year N."""
    per = collections.defaultdict(lambda: collections.defaultdict(list))
    for c, r, v0 in rows(recs):
        for n in range(0, NMAX + 1):
            x = v(r, n)
            if x is not None: per[n][c].append(x / v0)
    out = {}
    for n in range(0, NMAX + 1):
        cm = [float(np.mean(vals)) for c, vals in sorted(per[n].items()) if vals]
        out[n] = (float(np.mean(cm)) if cm else float("nan"), len(cm))
    return out


def young_peak(recs):
    """young = cohort-averaged years 0-1 book; peak = cohort-averaged years 4-5 book.
    Bands of the COHORT-AVERAGED books, not of a 2026 cross-section."""
    prog = cohort_progression(recs)
    y = np.nanmean([prog[n][0] for n in (0, 1)])
    p = np.nanmean([prog[n][0] for n in (4, 5)])
    return float(y), float(p), (float(y / p) if p else float("nan"))


def free_money(recs, rate_at):
    """Per-rung expected appreciation from the cohort book vs the discount charged at that rung's
    typical age. Free money if appreciation exceeds the charge."""
    prog = cohort_progression(recs)
    ages = {0: 18.5, 1: 19.5, 2: 20.5, 3: 21.5, 4: 22.5, 5: 23.5}
    out = []
    for n in range(0, NMAX):
        a, b = prog[n][0], prog[n + 1][0]
        if not (a and b) or a != a or b != b: continue
        app = b / a - 1.0
        chg = rate_at(ages[n])
        out.append((n, app, chg, app - chg))
    return out


def rate_main(_a): return 0.14
def _pw(a, kn):
    a = float(a)
    if a <= kn[0][0]: return kn[0][1]
    if a >= kn[-1][0]: return kn[-1][1]
    for (a0, r0), (a1, r1) in zip(kn, kn[1:]):
        if a0 <= a <= a1: return r0 if a1 == a0 else r0 + (r1 - r0) * (a - a0) / (a1 - a0)
    return kn[-1][1]
V2K = [(19.,.12),(20.,.13),(21.,.13),(25.,.15),(27.,.15),(28.,.16)]
V3K = [(20.,.10),(21.,.11),(22.,.11),(23.,.12),(25.,.12),(26.,.13),(28.,.13),(29.,.14)]
RATE = {"main": rate_main, "FULL": rate_main,
        "V1": lambda a: 0.13 if a <= 21 else (0.15 if a >= 26 else 0.13 + 0.02 * (a - 21) / 5),
        "V2": lambda a: _pw(a, V2K), "V3": lambda a: _pw(a, V3K)}

print("=" * 108)
print("THE OWNER-BASIS COHORT TABLES — INSTRUMENT: per-entrant matrices (emit_matrix_338.py)")
print("  cohort rule: COHORT N = every entrant whose YEAR 1 is season N+1, all routes; MSD folded")
print("  back one year. year-N = the AVERAGE OVER COHORTS at year N. Anchor-relative (no-arb) form.")
print("  NOT a live-board cross-section.")
print("=" * 108)

avail = [(lab, tag, load(tag)) for lab, tag in VARIANTS]
avail = [(lab, tag, r) for lab, tag, r in avail if r]
if not avail:
    print("\n  NO MATRICES YET — the emits are still running. Re-run when they land."); sys.exit(0)

print("\n=== (1) COHORT PROGRESSION, anchor-relative (year-0 = 1.000 by construction) ===")
print(" %-22s %8s %8s %8s %8s %8s %8s   %s" % ("variant", "yr0", "yr1", "yr2", "yr3", "yr4", "yr5", "cohorts@yr4"))
for lab, tag, recs in avail:
    pr = cohort_progression(recs)
    print(" %-22s %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f   %d"
          % (lab, pr[0][0], pr[1][0], pr[2][0], pr[3][0], pr[4][0], pr[5][0], pr[4][1]))

print("\n=== (2) YOUNG vs PEAK on the COHORT-AVERAGED books (years 0-1 vs years 4-5) ===")
print(" %-22s %10s %10s %12s %10s" % ("variant", "young", "peak", "young/peak", "vs main"))
base = None
for lab, tag, recs in avail:
    y, p, r = young_peak(recs)
    if base is None: base = r
    print(" %-22s %10.3f %10.3f %12.4f %+10.2f%%" % (lab, y, p, r, 100 * (r / base - 1)))

print("\n=== (3) THE FREE-MONEY CHECK (within-instrument; replaces the confounded cross-section) ===")
print("  per-rung cohort-book appreciation vs the discount charged at that rung's typical age.")
print("  POSITIVE margin = appreciation exceeds the charge = free money.")
for lab, tag, recs in avail:
    fm = free_money(recs, RATE.get(tag, rate_main))
    print(" %-22s %s" % (lab, "  ".join("y%d->%d %+.1f%% vs %.1f%% = %+.1f%%"
                                        % (n, n + 1, 100 * a, 100 * c, 100 * m) for n, a, c, m in fm)))
    worst = max((m for _n, _a, _c, m in fm), default=0)
    print("   %-20s worst margin %+.1f%%  %s" % ("", 100 * worst,
          "NO FREE MONEY" if worst <= 0 else "** FREE MONEY at this rung — inspect"))

print("\n=== (4) THE 140/130 ENVELOPE on the cohort book (A FRAME, NOT A TARGET) ===")
print("  peak = cohort-averaged years 4-5; year-0 and year-1 are the cohort-averaged books.")
print(" %-22s %14s %14s" % ("variant", "peak/year-0", "peak/year-1"))
for lab, tag, recs in avail:
    pr = cohort_progression(recs)
    pk = np.nanmean([pr[n][0] for n in (4, 5)])
    print(" %-22s %13.1f%% %13.1f%%" % (lab, 100 * pk / pr[0][0], 100 * pk / pr[1][0]))
print("  envelope 140% / 130%. NO component in this act was sized against these numbers.")
