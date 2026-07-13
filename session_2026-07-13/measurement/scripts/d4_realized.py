"""D4.2 — the REALIZED captaincy value as an ORDER STATISTIC on the walk-forward record.
Captaincy is a slot good (one captain/week): the worth of the top option = the gap to the NEXT option.
Per completed season, rank realized SC averages (games>=10) and measure top-vs-2nd/5th/10th; test whether the
gap is CONVEX in how far the top sits above the field. Raw scoring only (no ev)."""
import json
import numpy as np
import harness as H
MA = H.MA
BASE = "/home/user/afl-rl-engine/session_2026-07-13/measurement"

# realized season averages, games>=10, completed seasons 2009-2025 (real store rows)
seasons = {}
for p in MA.data:
    for s in p["scoring"]:
        if s.get("games", 0) >= 10 and 2009 <= s["year"] <= 2025:
            seasons.setdefault(s["year"], []).append(s["avg"])

rows = []
for Y in sorted(seasons):
    a = np.array(sorted(seasons[Y], reverse=True))
    if len(a) < 12: continue
    top1, top2, top5, top10 = a[0], a[1], a[4], a[9]
    med = float(np.median(a)); mean = float(np.mean(a))
    rows.append(dict(year=Y, n=len(a), top1=round(top1,1), top2=round(top2,1), top5=round(top5,1), top10=round(top10,1),
                     field_median=round(med,1),
                     gap_top_2nd=round(top1-top2,1), gap_top_5th=round(top1-top5,1), gap_top_10th=round(top1-top10,1),
                     top_above_field=round(top1-med,1)))

# convexity test 1: is (top1 - 2nd) larger when top1 sits further above the field?
tf = np.array([r["top_above_field"] for r in rows]); g2 = np.array([r["gap_top_2nd"] for r in rows])
slope = np.polyfit(tf, g2, 1)[0]; corr = float(np.corrcoef(tf, g2)[0, 1])

# convexity test 2: the POOLED rank-value gap curve — is the rank1->2 gap bigger than deeper gaps? (concave live term
# should be justified only if the realized top gap is SMALL; a big top gap => the field-topping player is a difference-maker)
pooled_gaps = {}
for Y in sorted(seasons):
    a = np.array(sorted(seasons[Y], reverse=True))
    if len(a) < 12: continue
    for k in range(1, 11):
        pooled_gaps.setdefault(k, []).append(a[k-1] - a[k])   # gap from rank k to rank k+1
gap_curve = {k: round(float(np.mean(v)), 2) for k, v in sorted(pooled_gaps.items())}

# convexity of the top: mean rank1->2 gap vs mean rank5->6 gap
top_gap = gap_curve[1]; mid_gap = gap_curve[5]
out = dict(board="realized walk-forward record (store scoring, games>=10, 2009-2025)",
           per_season=rows,
           mean_gap_top_2nd=round(float(np.mean(g2)),2),
           mean_gap_top_5th=round(float(np.mean([r["gap_top_5th"] for r in rows])),2),
           mean_gap_top_10th=round(float(np.mean([r["gap_top_10th"] for r in rows])),2),
           convexity_gap_vs_field=dict(slope=round(slope,3), corr=round(corr,3),
               reading="gap(top-2nd) rises with how far the top sits above the field => CONVEX top" if slope>0 else "flat/concave"),
           pooled_rank_gap_curve=gap_curve,
           top_gap_rank1to2=top_gap, mid_gap_rank5to6=mid_gap,
           top_is_convex=(top_gap > mid_gap))
json.dump(out, open(BASE + "/out/d4_realized.json", "w"), indent=1)
print("=== D4.2 REALIZED ORDER-STATISTIC CAPTAIN VALUE (walk-forward record) ===")
print(f"{'year':5s}{'n':>5s}{'top1':>7s}{'2nd':>7s}{'5th':>7s}{'10th':>7s}{'field_med':>10s}{'g1-2':>7s}{'g1-5':>7s}{'g1-10':>7s}{'top-field':>10s}")
for r in rows:
    print(f"{r['year']:<5d}{r['n']:5d}{r['top1']:7.1f}{r['top2']:7.1f}{r['top5']:7.1f}{r['top10']:7.1f}{r['field_median']:10.1f}{r['gap_top_2nd']:7.1f}{r['gap_top_5th']:7.1f}{r['gap_top_10th']:7.1f}{r['top_above_field']:10.1f}")
print(f"\nmean gaps: top-2nd={out['mean_gap_top_2nd']}  top-5th={out['mean_gap_top_5th']}  top-10th={out['mean_gap_top_10th']}")
print(f"convexity vs field: slope={out['convexity_gap_vs_field']['slope']} corr={out['convexity_gap_vs_field']['corr']} -> {out['convexity_gap_vs_field']['reading']}")
print(f"pooled rank-gap curve (rank k -> k+1): {gap_curve}")
print(f"top gap (1->2)={top_gap}  mid gap (5->6)={mid_gap}  top_is_convex={out['top_is_convex']}")
print("wrote out/d4_realized.json")
