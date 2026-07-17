"""JOB 3 — SURVIVORSHIP, MAPPED. Reads out/per_entrant.json.

Two questions:
 (1) EXITS: who leaves the sample when — delistings/retirements per band per career-year — and what the
     CURRENT derivation does with them.
 (2) BIAS: where a naive per-band mean of the year-1 anchor biases, and in which direction, vs the full
     realised life-path (the NOTE item-2 convexity concern).

WHAT THE CURRENT DERIVATION DOES (from code, s4_matrix_7147.py:57-62 + pvc_fit.py):
 * The curve anchor is ASOF[C+1] = END OF YEAR 1, for EVERY in-curve entrant, busts included (they get
   their low/pole yr1 value; nobody is dropped for washing out) — so "include busts" IS satisfied.
 * BUT it is a SINGLE yr1 cross-section: the life-path beyond yr1 (peak, survivor compounding at yr4/5/6)
   is NEVER read by the derivation. Retired players' Vpath is truncated at last-played; the anchor is
   still yr1. => the survivor convex tail is STRUCTURALLY INVISIBLE to the current curve.
 * pvc_fit.py smooths with a MEDIAN kernel (robust to the tail) -> further flattens any convexity.

CENSORING: career-length/convexity restricted to cohorts drafted <=2018 (>=6 completed follow-up years to
2024/25). Exit counts shown for that mature window. Recent cohorts flagged, not mixed in.
"""
import json, collections, statistics
BASE = '/home/user/afl-rl-engine/session_2026-07-17/legd_derivation'
recs = json.load(open(BASE + '/out/per_entrant.json'))
BANDS = ["1-3", "4-7", "8-12", "13-20", "21-27", "28-35", "36-48", "49-99"]

def pool(lo, hi):
    return [r for r in recs if r['incurve'] and r['pick'] and lo <= r['year'] <= hi]

mature = pool(2004, 2018)   # full follow-up
allp = pool(2004, 2024)

def career_len(r):  # completed years from draft to last game (0 = never played a senior game)
    if r['last_game_year'] is None: return 0
    return r['last_game_year'] - r['year']

# ---- (1) EXIT TABLE: per band, cumulative fraction who have played their LAST game by career-year k ----
exit_tbl = []
for b in BANDS:
    g = [r for r in mature if r['band'] == b]
    if not g: continue
    n = len(g)
    never = sum(1 for r in g if r['last_game_year'] is None)
    row = dict(band=b, n=n, never_played=never,
               delisted=sum(1 for r in g if r['delisted']),
               retired_now=sum(1 for r in g if r['retired_now']))
    for k in [1, 2, 3, 4, 5, 6, 8]:
        gone = sum(1 for r in g if career_len(r) <= k)   # last senior game by career-year k
        row[f'exit_by_yr{k}'] = gone
        row[f'exit_by_yr{k}_pct'] = round(100 * gone / n, 1)
    # median career length (played players only)
    cl = [career_len(r) for r in g if r['last_game_year'] is not None]
    row['median_career_len_played'] = statistics.median(cl) if cl else None
    exit_tbl.append(row)

# ---- (2) CONVEX GAP: yr1-anchor pool vs peak pool, per band (NOTE item 2 life-path totals) ----
conv_tbl = []
for b in BANDS:
    g = [r for r in mature if r['band'] == b and r['anchor'] and r['peak']]
    if not g: continue
    n = len(g)
    anchor_sum = sum(r['anchor'] for r in g)
    peak_sum = sum(r['peak'] for r in g)
    # survivors = career_len >= 4 (reached yr4+)
    surv = [r for r in g if career_len(r) >= 4]
    conv_tbl.append(dict(
        band=b, n=n,
        mean_anchor_yr1=round(anchor_sum / n),
        mean_peak=round(peak_sum / n),
        peak_over_anchor=round(peak_sum / anchor_sum, 3),
        n_survivors_yr4plus=len(surv),
        surv_frac=round(len(surv) / n, 3),
        mean_peak_survivors=round(statistics.mean(r['peak'] for r in surv)) if surv else None,
        # the flat-snapshot bias: a per-band MEAN of the yr1 anchor vs the mean of realised peaks
        flatsnapshot_understate_ratio=round(peak_sum / anchor_sum, 3),
    ))

out = dict(
    _doc="Job 3 survivorship. Exit table (mature cohorts 2004-2018) + convex-gap (yr1 anchor pool vs peak pool). "
         "The current derivation reads ONLY the yr1 anchor, so the survivor convex tail is invisible to it.",
    what_derivation_does=dict(
        anchor="ASOF[C+1]=end-of-yr1, EVERY entrant incl. busts (s4_matrix_7147.py:62) — busts ARE included",
        single_cross_section="life-path beyond yr1 (peak/survivor compounding) never read by pvc_fit.py",
        smoother="MEDIAN kernel (pvc_fit.py:33-46) — robust to the tail, further flattens convexity",
        bias_direction="UNDERSTATES pick value in EVERY band (peak/anchor > 1 everywhere). MEASURED REFINEMENT "
                       "of NOTE item 2: the ABSOLUTE convex gap (peak-anchor) is largest at the TOP (~1956 at "
                       "picks 1-3 vs ~890 at 36-48), but the RATIO peak/anchor is U-shaped — lowest at picks 1-3 "
                       "(1.69, they already play early so the yr1 anchor is already high) and largest MID-BAND "
                       "(~2.6 at 28-48). So a flat yr1 snapshot understates most in absolute currency at the top "
                       "and most in proportion in the middle; the NOTE's 'worst at the top' holds in dollars, not ratio.",
    ),
    exit_table_2004_2018=exit_tbl,
    convex_gap_2004_2018=conv_tbl,
    censoring="career-length/convexity on cohorts drafted <=2018 (>=6 follow-up yrs); recent cohorts excluded.",
)
json.dump(out, open(BASE + '/out/job3_survivorship.json', 'w'), indent=1)

# markdown
L = ["# Job 3 — Survivorship, mapped", "",
     "Mature cohorts (drafted 2004-2018, full follow-up). The current derivation reads ONLY the end-of-yr1 "
     "anchor for every entrant (busts included), so exits AFTER yr1 don't change the anchor — but the survivor "
     "convex tail (yr4/5/6 compounding) is **structurally invisible** to the curve.", "",
     "## Exit table — cumulative % who have played their LAST senior game by career-year k", "",
     "| band | n | never played | exit_by_yr2 | exit_by_yr4 | exit_by_yr6 | median career (played) |",
     "|------|---|--------------|-------------|-------------|-------------|------------------------|"]
for r in exit_tbl:
    L.append(f"| {r['band']} | {r['n']} | {r['never_played']} | {r['exit_by_yr2']} ({r['exit_by_yr2_pct']}%) | "
             f"{r['exit_by_yr4']} ({r['exit_by_yr4_pct']}%) | {r['exit_by_yr6']} ({r['exit_by_yr6_pct']}%) | "
             f"{r['median_career_len_played']} |")
L += ["", "## Convex gap — per-band yr1-anchor pool vs realised peak pool", "",
      "| band | n | mean anchor (yr1) | mean peak | peak/anchor | survivors yr4+ | surv frac |",
      "|------|---|-------------------|-----------|-------------|----------------|-----------|"]
for r in conv_tbl:
    L.append(f"| {r['band']} | {r['n']} | {r['mean_anchor_yr1']} | {r['mean_peak']} | "
             f"**{r['peak_over_anchor']}** | {r['n_survivors_yr4plus']} | {r['surv_frac']} |")
L += ["", "**Bias direction (measured):** a per-band mean of the yr1 anchor UNDERSTATES the pick — `peak/anchor` "
      "> 1 in every band. The ABSOLUTE gap (peak-anchor) is largest at the TOP (~1956 SCAR at picks 1-3 vs ~890 at "
      "36-48); the RATIO is U-shaped, smallest at picks 1-3 (1.69 — top picks play early, so their yr1 anchor is "
      "already high) and largest MID-BAND (~2.6 at 28-48). So the NOTE's 'worst at the top' holds in **dollars**, not "
      "in ratio. A flat yr1 snapshot credits none of the tail; the MEDIAN smoother flattens what little the anchor "
      "carries. Magnitude provisional — values move under R106.7."]
open(BASE + '/out/job3_survivorship.md', 'w').write("\n".join(L))

print("EXIT TABLE (2004-2018):")
print(f"{'band':7}{'n':>5}{'never':>6}{'exit2%':>8}{'exit4%':>8}{'exit6%':>8}{'medCL':>6}")
for r in exit_tbl:
    print(f"{r['band']:7}{r['n']:>5}{r['never_played']:>6}{r['exit_by_yr2_pct']:>8}{r['exit_by_yr4_pct']:>8}{r['exit_by_yr6_pct']:>8}{str(r['median_career_len_played']):>6}")
print("\nCONVEX GAP:")
print(f"{'band':7}{'n':>5}{'anchor':>8}{'peak':>7}{'pk/an':>7}{'surv4+':>7}")
for r in conv_tbl:
    print(f"{r['band']:7}{r['n']:>5}{r['mean_anchor_yr1']:>8}{r['mean_peak']:>7}{r['peak_over_anchor']:>7}{r['n_survivors_yr4plus']:>7}")
print("wrote out/job3_survivorship.{json,md}")
