"""RIDER (iii) — uncertainty grading past ~p50. READ-ONLY.

A CONTINUOUS, smoothed uncertainty grade U(p) along the curve past ~p50, composed at each EXACT
pick from the dispersion the other two riders already measured on the frozen candidate:
  - sampling dispersion  = rider (ii) RAW per-exact-pick cohort-bootstrap relative SD  (finest resolution)
  - generalization disp. = rider (i) leave-one-cohort-out residual envelope half-width (+ fit-vs-2003 gap, reported)
U(p) = RSS(sampling, generalization), then kernel-smoothed over log-pick into a continuous grade.
No bands, no verdict (S4 / CORE rule 7 / R107.4). Gross (R107.7). Stamps carried through (must match).
"""
import json, sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
from svgplot import lineplot

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out')
GRADE_BW = 0.08          # log-pick bandwidth for the continuous grade (declared)
SINK_WT = 0.2            # pick-99 sink down-weight in the grade smoother (aggregate, not a same-resolution pick)
REP = [40, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 98, 99]

def main():
    curve, per, stamps = C.load_frozen()   # re-assert stamps (HALT on mismatch)
    ri = json.load(open(os.path.join(OUT, 'rider_i_calibration.json')))
    rii = json.load(open(os.path.join(OUT, 'rider_ii_bootstrap.json')))
    # provenance: the composed grade must describe the SAME frozen candidate
    for k in ('curve_payload_md5', 'store_base_md5', 'per_entrant_md5'):
        if not (stamps[k] == ri['stamps'][k] == rii['stamps'][k]):
            print(f"HALT: stamp {k} mismatch across riders", file=sys.stderr); sys.exit(3)

    grid = list(range(C.KMIN, C.KMAX + 1))
    prim = ri['series']['primary']; fit = ri['series']['fit_era']
    held = ri['series']['held_out_2003']; env = ri['series']['loco_residual_envelope']
    sii = rii['series']

    # per-pick uncertainty components (relative %)
    samp = np.array([sii[str(p)]['raw_boot_rel_sd_pct'] if sii[str(p)]['raw_boot_rel_sd_pct'] is not None
                     else np.nan for p in grid])
    loco_hw = np.array([(env[str(p)]['hi'] - env[str(p)]['lo']) / 2.0 for p in grid])   # generalization dispersion
    fit_vs_2003 = np.array([abs(fit[str(p)]['resid_rel_pct'] - held[str(p)]['resid_rel_pct']) for p in grid])
    U_raw = np.sqrt(np.nan_to_num(samp) ** 2 + loco_hw ** 2)                            # RSS of the two (declared)

    # continuous smoothed grade over log-pick (down-weight the pick-99 sink)
    Lp = np.log(np.array(grid, float))
    w = np.array([SINK_WT if p == 99 else 1.0 for p in grid])
    U = np.zeros(len(grid))
    for gi, p in enumerate(grid):
        K = np.exp(-0.5 * ((Lp - np.log(p)) / GRADE_BW) ** 2) * w
        U[gi] = float(np.sum(K * U_raw) / np.sum(K))

    # reference: median grade over the top (p<=30) to frame "past p50 is X times the top"
    top_ref = float(np.median([U[gi] for gi, p in enumerate(grid) if p <= 30]))
    tail_med = float(np.median([U[gi] for gi, p in enumerate(grid) if 50 <= p <= 98]))

    series = {}
    for gi, p in enumerate(grid):
        series[p] = dict(uncertainty_grade_pct=round(float(U[gi]), 2),
                         U_raw_pct=round(float(U_raw[gi]), 2),
                         comp_sampling_bootSD_pct=None if np.isnan(samp[gi]) else round(float(samp[gi]), 2),
                         comp_generalization_loco_halfwidth_pct=round(float(loco_hw[gi]), 2),
                         comp_fit_vs_2003_gap_pct=round(float(fit_vs_2003[gi]), 2),
                         curve=curve[p], raw_n=sii[str(p)]['raw_n'])

    result = dict(
        rider='(iii) uncertainty grading past ~p50',
        stamps=stamps, report_only=True, verdict_language=False,
        declared=dict(
            grade='U(p) = RSS( rider-ii RAW per-exact-pick cohort-bootstrap rel-SD , '
                  'rider-i leave-one-cohort-out residual half-width ), kernel-smoothed over log-pick (bw=%.2f); '
                  'continuous, no bands' % GRADE_BW,
            fit_vs_2003_gap='reported as a component but thin (single held-out cohort); not the grade driver',
            pick99='deep sink down-weighted (w=%.1f) in the grade smoother — it is an aggregate, not a '
                   'same-resolution exact pick' % SINK_WT,
            gross=True),
        top_reference_grade_pct=round(top_ref, 2), deep_tail_median_grade_pct=round(tail_med, 2),
        deep_tail_vs_top_ratio=round(tail_med / top_ref, 2) if top_ref else None,
        series=series)
    os.makedirs(OUT, exist_ok=True)
    json.dump(result, open(os.path.join(OUT, 'rider_iii_uncertainty.json'), 'w'), indent=1)

    # ---- SVG: continuous grade + its two components, p>=40 emphasis ----
    g2 = [p for p in grid if p >= 40]
    svg = lineplot(
        [('uncertainty grade U(p) (smoothed)', g2, [series[p]['uncertainty_grade_pct'] for p in g2], '#000', False),
         ('  sampling: cohort-boot rel-SD', g2, [series[p]['comp_sampling_bootSD_pct'] or 0 for p in g2], '#d62728', True),
         ('  generalization: LOCO half-width', g2, [series[p]['comp_generalization_loco_halfwidth_pct'] for p in g2], '#1f77b4', True)],
        'exact pick', 'uncertainty (relative %)',
        'RIDER (iii) — continuous uncertainty grade past ~p50',
        subtitle='grade = RSS(bootstrap, holdout) kernel-smoothed; rises steeply past p50; %s' % C.STAMP_NOTE[:52],
        xmarks=[40, 50, 60, 70, 80, 90, 99], hline=top_ref,
        notes=['dashed line = top (p<=30) grade', 'pick99 sink down-weighted', 'no bands'])
    open(os.path.join(OUT, 'rider_iii_uncertainty.svg'), 'w').write(svg)

    # ---- MD ----
    L = []
    L.append('# RIDER (iii) — uncertainty grading past ~p50\n')
    L.append('**REPORT-ONLY · finding, not a verdict · gross · no decile bands.**  \n')
    L.append('`%s`\n' % C.STAMP_NOTE)
    L.append('\n**Declared grade:** `U(p) = RSS( sampling , generalization )`, kernel-smoothed over log-pick '
             '(bw=%.2f) into a **continuous** curve — no bands. `sampling` = rider-(ii) RAW per-exact-pick '
             'cohort-bootstrap relative SD; `generalization` = rider-(i) leave-one-cohort-out residual '
             'half-width. The fit-vs-2003 gap is reported per pick as context but is thin (one held-out '
             'cohort) and does not drive the grade. The pick-99 sink is down-weighted (w=%.1f) in the '
             'smoother — it is an aggregate, not a same-resolution exact pick.\n' % (GRADE_BW, SINK_WT))
    L.append('\n**Headline:** the uncertainty grade is roughly flat and low across the top and rises '
             'steeply past ~p50 — deep-tail median **%.0f%%** vs top (p≤30) **%.0f%%**, about **%.1f×** '
             'higher. Past ~p50 the curve should be read as a low-confidence region.\n'
             % (tail_med, top_ref, tail_med / top_ref if top_ref else float('nan')))
    L.append('\n## Uncertainty grade by exact pick (past ~p50)\n')
    L.append('| pick | grade U(p) % | sampling (boot-SD) % | generalization (LOCO ½) % | fit-vs-2003 gap % | curve | raw n |\n')
    L.append('|---|---|---|---|---|---|---|\n')
    for p in REP:
        s = series[p]; flag = ' *(sink)*' if p == 99 else ''
        L.append('| %d%s | %.1f | %s | %.1f | %.1f | %d | %d |\n'
                 % (p, flag, s['uncertainty_grade_pct'],
                    'n/a' if s['comp_sampling_bootSD_pct'] is None else '%.1f' % s['comp_sampling_bootSD_pct'],
                    s['comp_generalization_loco_halfwidth_pct'], s['comp_fit_vs_2003_gap_pct'],
                    s['curve'], s['raw_n']))
    L.append('\n_Full 1–99 series in `rider_iii_uncertainty.json`; curve in `rider_iii_uncertainty.svg`._\n')
    L.append('\n## Finding (one plain sentence, no verdict)\n')
    L.append('A continuous uncertainty grade built from cohort-bootstrap and leave-one-cohort-out '
             'dispersion is low and flat across the top of the board and climbs steeply beyond ~p50 '
             '(about %.1f× the top by the deep tail), so the deep-tail region of the frozen curve carries '
             'materially less statistical support per exact pick than the top.\n'
             % (tail_med / top_ref if top_ref else float('nan')))
    open(os.path.join(OUT, 'rider_iii_uncertainty.md'), 'w').write(''.join(L))

    print(f"[iii] grade top(p<=30 median)={top_ref:.1f}%  deep-tail(p50-98 median)={tail_med:.1f}%  "
          f"ratio={tail_med/top_ref:.1f}x")
    print(f"[iii] grade @ 50/70/90/98 = {series[50]['uncertainty_grade_pct']:.1f}/"
          f"{series[70]['uncertainty_grade_pct']:.1f}/{series[90]['uncertainty_grade_pct']:.1f}/"
          f"{series[98]['uncertainty_grade_pct']:.1f} %")
    print("[iii] wrote out/rider_iii_uncertainty.{json,md,svg}")
    print("RIDER_III_COMPLETE")

if __name__ == '__main__':
    main()
