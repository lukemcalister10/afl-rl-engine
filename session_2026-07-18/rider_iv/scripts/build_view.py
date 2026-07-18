"""RIDER (iv) job 3 — THE VIEW: GROSS beside v-R (three candidates), per EXACT pick, smoothed,
full board; the p1/p60 & p1/p90 ratio table per candidate; the deep-tail premium-over-free-pool
curve (v-R past ~p50) with rider-(iii)'s uncertainty grade overlaid.

REPORT-ONLY. Symmetric, no verdict. Emits out/the_view.json + .md + three SVGs. The v2 curve is
already the per-exact-pick smoothed object (item 325); v-R is a labelled shift of it — no rebinning.
"""
import json, os
import numpy as np
import common_riv as C
from svgplot import lineplot

OUT = os.path.join(os.path.dirname(__file__), '..', 'out')
PICKS = list(range(1, 100))


def main():
    curve, per, rinp, stamps = C.load_frozen()
    peq = C.pickeq(rinp)
    grade, top_grade, deep_grade, deep_ratio = C.rider_iii_grade()

    # R scalars (pooled) from job 1
    rc = json.load(open(os.path.join(OUT, 'r_candidates.json')))
    R = {
        'R_curve':    rc['candidates']['R_curve']['pooled'],
        'R_realized': rc['candidates']['R_realized']['pooled'],
        'R_owner':    rc['candidates']['R_owner']['value'],
    }

    gross = {p: curve[p] for p in PICKS}
    vminusR = {name: {p: round(gross[p] - r, 1) for p in PICKS} for name, r in R.items()}

    # ---- ratio table: p1/p60 and p1/p90 for GROSS and each v-R candidate ----
    def ratio(series, a, b):
        da, db = series[a], series[b]
        return round(da / db, 2) if db not in (0,) and abs(db) > 1e-9 else None
    ratios = {'GROSS': dict(p1=gross[1], p60=gross[60], p90=gross[90],
                            r_1_60=ratio(gross, 1, 60), r_1_90=ratio(gross, 1, 90))}
    for name in R:
        s = vminusR[name]
        ratios[name] = dict(R=R[name], p1=s[1], p60=s[60], p90=s[90],
                            r_1_60=ratio(s, 1, 60), r_1_90=ratio(s, 1, 90))

    # ---- deep-tail premium (v-R past p50) + rider-(iii) grade overlaid ----
    deep = list(range(50, 100))
    deep_tail = {
        'picks': deep,
        'premium': {name: [vminusR[name][p] for p in deep] for name in R},
        'rider_iii_grade_pct': [round(grade[p], 2) for p in deep],
        'gross': [gross[p] for p in deep],
    }

    result = dict(
        rider="(iv) the view — GROSS beside v-R, three candidates, per exact pick",
        report_only=True, do_not_merge=True, verdict=False,
        stamps=stamps, axes_note=C.AXES_NOTE, R_scalars=R,
        gross=gross, v_minus_R=vminusR, ratios=ratios, deep_tail=deep_tail,
        note="per EXACT pick; the v2 curve is the smoothed object (item 325); v-R is a labelled "
             "constant shift, not a rebinning; no decile bands.")
    os.makedirs(OUT, exist_ok=True)
    json.dump(result, open(os.path.join(OUT, 'the_view.json'), 'w'), indent=1)

    # ---------------- SVG 1: full board GROSS + three v-R ----------------
    colors = dict(GROSS='#111', R_curve='#1f77b4', R_realized='#d62728', R_owner='#2ca02c')
    series1 = [('GROSS = v2(p)', PICKS, [gross[p] for p in PICKS], colors['GROSS'], False)]
    for name in ['R_curve', 'R_realized', 'R_owner']:
        series1.append((f'v-{name} (R={R[name]})', PICKS, [vminusR[name][p] for p in PICKS], colors[name], True))
    svg1 = lineplot(series1, 'exact pick', 'value (SCAR units)',
                    'Rider (iv) — GROSS vs v-R, full board (three R candidates)',
                    subtitle=C.STAMP_NOTE[:120], hline=0,
                    xmarks=[1, 20, 40, 60, 80, 90, 99],
                    notes=['REPORT-ONLY / DO-NOT-MERGE  ·  no verdict — the reading is the owner\'s',
                           C.AXES_NOTE])
    open(os.path.join(OUT, 'view_fullboard.svg'), 'w').write(svg1)

    # ---------------- SVG 2: deep-tail premium + grade overlay (right-scaled) ----------------
    prem_vals = [vminusR[n][p] for n in R for p in deep]
    pmin, pmax = min(prem_vals + [0]), max(prem_vals)
    gvals = [grade[p] for p in deep]
    gmin, gmax = min(gvals), max(gvals)
    # scale grade% into the premium value range so it overlays on one axis (labelled right-scaled)
    def gscale(g):
        return pmin + (g - gmin) / (gmax - gmin) * (pmax - pmin)
    series2 = []
    for name in ['R_curve', 'R_realized', 'R_owner']:
        series2.append((f'premium v-{name}', deep, [vminusR[name][p] for p in deep], colors[name], False))
    series2.append((f'rider-iii grade % [{round(gmin,1)}-{round(gmax,1)}%, right-scaled]', deep,
                    [gscale(grade[p]) for p in deep], '#888', True))
    svg2 = lineplot(series2, 'exact pick (deep tail, past ~p50)', 'premium v-R (SCAR units)',
                    'Rider (iv) — deep-tail premium-over-free-pool, grade overlaid',
                    subtitle='v-R past p50 for each R candidate; grey dashed = rider-(iii) curve uncertainty (right-scaled)',
                    hline=0, xmarks=[50, 60, 70, 80, 90, 92, 99],
                    notes=[f'free-pool entry at pk90/92 (grade ~{round(grade[90],0)}%, ~{deep_ratio}x top)',
                           'under R_curve the premium collapses to ~0 at the entry (self-consistent, not a verdict)'])
    open(os.path.join(OUT, 'view_deeptail_premium.svg'), 'w').write(svg2)

    # ---------------- markdown ----------------
    L = []
    L.append("# Rider (iv) — THE VIEW: GROSS beside v-R  (REPORT-ONLY / DO-NOT-MERGE)\n")
    L.append(f"_{C.STAMP_NOTE}_\n")
    L.append(f"> **Axes note.** {C.AXES_NOTE}\n")
    L.append("Per **exact** pick, smoothed (the v2 curve is the item-325 smoothed object; v-R is a "
             "labelled constant shift — **no decile bands**). Symmetric: three candidates, **no verdict**.\n")
    L.append(f"R scalars (pooled, from job 1): R_curve=**{R['R_curve']}**, R_realized=**{R['R_realized']}**, R_owner=**{R['R_owner']}**.\n")

    L.append("## Ratio table — p1/p60 and p1/p90 (how v-R re-shapes the ladder)\n")
    L.append("| currency | p1 | p60 | p90 | p1/p60 | p1/p90 |")
    L.append("|---|---:|---:|---:|---:|---:|")
    for name in ['GROSS', 'R_curve', 'R_realized', 'R_owner']:
        r = ratios[name]
        tag = name if name == 'GROSS' else f"v-{name} (R={r['R']})"
        r160 = r['r_1_60'] if r['r_1_60'] is not None else '—'
        r190 = r['r_1_90'] if r['r_1_90'] is not None else 'unstable (denom~0)'
        L.append(f"| {tag} | {r['p1']} | {r['p60']} | {r['p90']} | {r160} | {r190} |")
    L.append("")
    L.append("- GROSS compresses ~6x top-to-p90. Making **v-R** the traded currency **steepens** the "
             "ladder: under R_realized/R_owner the p1/p90 ratio roughly doubles (~10-11x). Under "
             "R_curve the deep-tail premium collapses toward 0 at the free-pool entry, so p1/p90 is "
             "**unstable** (denominator ~0) — a direct consequence of R_curve being the curve's own "
             "value at that pick. Findings, not a recommendation.\n")

    L.append("## Full board — GROSS vs v-R\n")
    L.append("![full board](view_fullboard.svg)\n")
    L.append("| pick | GROSS | v-R_curve | v-R_realized | v-R_owner |")
    L.append("|---:|---:|---:|---:|---:|")
    for p in [1, 10, 20, 40, 50, 60, 70, 80, 90, 92, 99]:
        L.append(f"| {p} | {gross[p]} | {vminusR['R_curve'][p]} | {vminusR['R_realized'][p]} | {vminusR['R_owner'][p]} |")
    L.append("")

    L.append("## Deep-tail premium-over-free-pool (v-R past ~p50) with rider-(iii) grade overlaid\n")
    L.append("![deep tail premium](view_deeptail_premium.svg)\n")
    L.append("| pick | GROSS | v-R_curve | v-R_realized | v-R_owner | rider-iii grade % |")
    L.append("|---:|---:|---:|---:|---:|---:|")
    for p in [50, 60, 70, 80, 90, 92, 95, 99]:
        L.append(f"| {p} | {gross[p]} | {vminusR['R_curve'][p]} | {vminusR['R_realized'][p]} | "
                 f"{vminusR['R_owner'][p]} | {round(grade[p],1)} |")
    L.append("")
    L.append(f"- The premium region past ~p50 carries a rider-(iii) uncertainty grade rising to "
             f"~{round(grade[90],0)}% at the free-pool entry (~{deep_ratio}x the {top_grade}% top): "
             f"**whichever R the owner reads, the deep-tail premium is a low-confidence number.**")
    L.append(f"- Under **R_realized ({R['R_realized']})** and **R_owner ({R['R_owner']})** the premium at "
             f"pk90 is ~{vminusR['R_realized'][90]:.0f} / ~{vminusR['R_owner'][90]:.0f} SCAR — a real "
             f"gap of a top pick over the free pool. Under **R_curve ({R['R_curve']})** it is "
             f"~{vminusR['R_curve'][90]:.0f} (collapses to ~0 by construction).\n")

    open(os.path.join(OUT, 'the_view.md'), 'w').write("\n".join(L))
    print("[build_view] wrote out/the_view.json + .md + 2 SVGs")
    print(f"  p1/p90: GROSS={ratios['GROSS']['r_1_90']}  v-R_realized={ratios['R_realized']['r_1_90']}  "
          f"v-R_owner={ratios['R_owner']['r_1_90']}  v-R_curve={ratios['R_curve']['r_1_90']}")
    return result


if __name__ == '__main__':
    main()
