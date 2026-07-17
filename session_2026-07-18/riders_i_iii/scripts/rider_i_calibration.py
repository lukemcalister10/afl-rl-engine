"""RIDER (i) — realized-outcome cohort-holdout calibration + washout-exit calibration. READ-ONLY.

Predicted (frozen PVC curve) vs REALIZED (mean vpath) per EXACT pick, kernel-smoothed. Cohort-holdout:
fit-era-complete (2004-2017) vs held-out-complete (2003). Washout/delist-exit as its own view. Busts
FULL weight (R107.3); GROSS (R107.7). Finding, not verdict (S4). No decile bands (CORE rule 7 / R107.4).
"""
import json, sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
from svgplot import lineplot

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out')
REP_PICKS = [1, 2, 3, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 99]

def calib(pool, curve, kind='meanvpath', nmin=C.NMIN):
    """Smoothed realized(p) vs curve(p), residual rel%. Equal weight per entrant (gross; busts full weight)."""
    pk = [r['pick'] for r in pool]
    rv = [C.realized(r, kind) for r in pool]
    sm = C.smooth_perpick(pk, rv, nmin=nmin)
    raw = C.raw_perpick_mean(pk, rv)
    series = {}
    for p in sm['grid']:
        cv = curve[p]
        rz = sm['smooth'][p]
        series[p] = dict(curve=cv, realized_smooth=round(rz, 1),
                         resid_rel_pct=round(100.0 * (rz - cv) / cv, 2),
                         effn=round(sm['effn'][p], 1), h=sm['h'][p], raw_n=sm['raw_n'][p],
                         raw_mean=raw.get(p, {}).get('mean'))
    return series, sm

def tail_onset(series, lo=12):
    """Smallest pick p>=lo beyond which the smoothed residual stays <0 through pick 99
    (the deep-tail over-pricing onset; robust to the noisy top / pinned pick 1)."""
    picks = sorted(series)
    for p in picks:
        if p < lo: continue
        if all(series[q]['resid_rel_pct'] < 0 for q in picks if q >= p):
            return p
    return None

def midhump_peak(series, lo=12, hi=48):
    """Pick of maximum positive residual in the upper-mid (where the curve most under-prices)."""
    cand = [(series[p]['resid_rel_pct'], p) for p in series if lo <= p <= hi]
    m = max(cand)
    return dict(pick=m[1], resid_rel_pct=m[0])

def main():
    curve, per, stamps = C.load_frozen()
    P = C.in_curve_pool(per)
    complete = [r for r in P if C.is_complete_cohort(r)]
    fit_complete = [r for r in complete if C.is_fit_era(r)]              # 2004-2017
    held_complete = [r for r in P if C.is_heldout(r) and r['year'] <= C.COMPLETE_MAXYEAR]  # 2003
    exited = [r for r in P if C.is_exited(r)]
    censored_recent = [r for r in P if r['year'] > C.COMPLETE_MAXYEAR]

    print(f"[i] complete-career n={len(complete)}  fit-era-complete(2004-17) n={len(fit_complete)}  "
          f"held-out-complete(2003) n={len(held_complete)}  exited n={len(exited)}  censored(>2017) n={len(censored_recent)}")

    # primary calibration (career-complete pool) + sensitivities
    prim, sm_prim = calib(complete, curve, 'meanvpath')
    peak_ser, _ = calib(complete, curve, 'peak')
    cur_ser, _ = calib(complete, curve, 'cur')
    # cohort-holdout
    fit_ser, _ = calib(fit_complete, curve, 'meanvpath')
    held_ser, _ = calib(held_complete, curve, 'meanvpath')
    # washout/delist-exit (own view; terminal, censoring-free, all cohorts)
    exit_ser, _ = calib(exited, curve, 'meanvpath')

    # leave-one-complete-cohort-out residual envelope (shape not driven by one cohort)
    years = sorted(set(r['year'] for r in complete))
    loco = {p: [] for p in sm_prim['grid']}
    for y in years:
        sub = [r for r in complete if r['year'] != y]
        s, _ = calib(sub, curve, 'meanvpath')
        for p in s: loco[p].append(s[p]['resid_rel_pct'])
    loco_env = {p: dict(lo=round(min(v), 2), hi=round(max(v), 2)) for p, v in loco.items()}

    xo = tail_onset(prim)
    hump = midhump_peak(prim)
    # deep-tail sink dominance: eff-n at high picks vs the pick-99 sink raw n
    sink_n = prim[99]['raw_n']
    tail_effn_note = ('deep-tail smoothed realized is dominated by the pick-99+ sink '
                      '(raw n@99=%d; eff-n rises to ~%.0f by pick 99), so picks ~85–99 share '
                      'essentially one realized estimate — the finest resolution the data support there'
                      % (sink_n, prim[99]['effn']))

    result = dict(
        rider='(i) realized-outcome cohort-holdout calibration + washout-exit calibration',
        stamps=stamps, report_only=True, verdict_language=False,
        declared=dict(
            realized_primary='mean(vpath) — codebase life-path measure; gross; busts full weight',
            realized_sensitivities=['peak', 'cur'],
            pool_primary='career-complete cohorts (year<=2017; ~all exited, mean vpath length ~6)',
            weight='equal per entrant (gross; busts full weight)',
            smoother='Gaussian kernel over log-pick, adaptive bw to eff-n>=%g (mirrors frozen fit_year0)' % C.NMIN,
            pick1='numeraire pin=3000, NOT a fit point — not scored as a miss',
            pick99='deep-pick sink (n~252), not one exact pick — flagged',
            fit_window='2004-2024; held-out = 2003 (pre-fit complete) & 2025 (post-fit, censored -> excluded from realized calib)'),
        counts=dict(complete=len(complete), fit_complete=len(fit_complete),
                    held_complete=len(held_complete), exited=len(exited), censored_recent=len(censored_recent)),
        tail_overpricing_onset_pick=xo,
        midmarket_underpricing_peak=hump,
        deep_tail_sink_caveat=tail_effn_note,
        series=dict(primary=prim, fit_era=fit_ser, held_out_2003=held_ser, washout_exit=exit_ser,
                    sens_peak=peak_ser, sens_cur=cur_ser, loco_residual_envelope=loco_env),
    )
    os.makedirs(OUT, exist_ok=True)
    json.dump(result, open(os.path.join(OUT, 'rider_i_calibration.json'), 'w'), indent=1)

    # ---- SVG 1: predicted vs realized (log-y would compress; linear, primary pool) ----
    grid = sm_prim['grid']
    svg_cal = lineplot(
        [('frozen PVC curve (predicted)', grid, [curve[p] for p in grid], '#000', False),
         ('realized mean(vpath), smoothed', grid, [prim[p]['realized_smooth'] for p in grid], '#1f77b4', False),
         ('realized peak (sens.)', grid, [peak_ser[p]['realized_smooth'] for p in grid], '#2ca02c', True)],
        'exact pick', 'value (SCAR)', 'RIDER (i) — predicted (frozen curve) vs realized outcome, per exact pick',
        subtitle='career-complete cohorts <=2017; %s' % C.STAMP_NOTE[:70],
        xmarks=[1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 99],
        notes=['pick1=numeraire pin', 'pick99=deep sink', 'gross; busts full wt'])
    open(os.path.join(OUT, 'rider_i_calibration.svg'), 'w').write(svg_cal)

    # ---- SVG 2: residual curve (rel %), fit-era vs held-out ----
    svg_res = lineplot(
        [('residual %, primary (complete)', grid, [prim[p]['resid_rel_pct'] for p in grid], '#1f77b4', False),
         ('residual %, fit-era 2004-17', grid, [fit_ser[p]['resid_rel_pct'] for p in grid], '#ff7f0e', False),
         ('residual %, held-out 2003', grid, [held_ser[p]['resid_rel_pct'] for p in grid], '#d62728', True),
         ('washout/exit residual %', grid, [exit_ser[p]['resid_rel_pct'] for p in grid], '#9467bd', True)],
        'exact pick', 'signed residual  100*(realized-curve)/curve  [%]',
        'RIDER (i) — calibration residual, per exact pick (finding, not a gate)',
        subtitle='>0 = curve under-prices realized; <0 = over-prices. tail over-pricing onset ~pick %s' % xo,
        hline=0.0, xmarks=[1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 99],
        notes=['held-out 2003 = 1 cohort (thin)', 'no decile bands'])
    open(os.path.join(OUT, 'rider_i_calibration_residual.svg'), 'w').write(svg_res)

    # ---- MD ----
    L = []
    L.append('# RIDER (i) — realized-outcome cohort-holdout calibration + washout-exit calibration\n')
    L.append('**REPORT-ONLY · finding, not a verdict · gross · busts full weight · no decile bands.**  \n')
    L.append('`%s`\n' % C.STAMP_NOTE)
    L.append('\n**Declared:** realized = `mean(vpath)` (primary; codebase life-path measure). Predicted = '
             'the FROZEN PVC curve. Smoother = Gaussian kernel over log-pick, adaptive bandwidth to '
             'eff-n≥%g, per exact pick. Pool = career-complete cohorts (≤2017). Pick 1 = numeraire pin '
             '(3000), not a fit point; pick 99 = deep-pick sink (n≈252). Equal weight per entrant.\n' % C.NMIN)
    L.append('\n**Counts:** complete-career %d · fit-era-complete(2004–17) %d · held-out-complete(2003) %d '
             '· washout/exit %d · censored recent(>2017, excluded from realized calib) %d.\n'
             % (len(complete), len(fit_complete), len(held_complete), len(exited), len(censored_recent)))
    L.append('\n## Calibration residual by exact pick (signed rel %; smoothed)\n')
    L.append('| pick | curve | realized(smooth) | resid % | eff-n | bw | raw n@pick | fit-era % | held-out 2003 % | washout/exit % | LOCO env % |\n')
    L.append('|---|---|---|---|---|---|---|---|---|---|---|\n')
    for p in REP_PICKS:
        s = prim[p]; e = loco_env[p]
        flag = ' *(pin)*' if p == 1 else (' *(sink)*' if p == 99 else '')
        L.append('| %d%s | %d | %.0f | %+.1f | %.0f | %.2f | %d | %+.1f | %+.1f | %+.1f | [%+.1f,%+.1f] |\n'
                 % (p, flag, s['curve'], s['realized_smooth'], s['resid_rel_pct'], s['effn'], s['h'],
                    s['raw_n'], fit_ser[p]['resid_rel_pct'], held_ser[p]['resid_rel_pct'],
                    exit_ser[p]['resid_rel_pct'], e['lo'], e['hi']))
    L.append('\n_Full 1–99 series in `rider_i_calibration.json`. Curves: `rider_i_calibration.svg` '
             '(predicted vs realized), `rider_i_calibration_residual.svg` (residual, fit vs held-out)._\n')
    L.append('\n**Deep-tail caveat (declared):** %s.\n' % tail_effn_note)
    L.append('\n## Finding (one plain sentence, no verdict)\n')
    L.append('Smoothed against realized career life-path (busts full weight, gross), the frozen curve '
             '**under-prices the upper-mid** (picks ~12–48 realize above their price; residual peaks '
             '**+%.0f%% near pick %d**) and **over-prices the deep tail** (residual turns negative at '
             '**pick %s** and deepens to about **%+.0f%% by the pick-99 sink**); the pre-fit held-out '
             '2003 cohort shows the deep-tail over-pricing if anything *more* strongly (tail %+.0f%%), '
             'so the tail signal is not an artifact of the fit era (thin — one cohort of %d), and the '
             'terminal censoring-free washout/exit view shows the same deep-tail over-pricing, while '
             'pick 1 (numeraire pin) and picks 2–11 (per-pick n≈15, high variance) are not a clean signal.\n'
             % (hump['resid_rel_pct'], hump['pick'], xo, prim[99]['resid_rel_pct'],
                held_ser[99]['resid_rel_pct'], len(held_complete)))
    open(os.path.join(OUT, 'rider_i_calibration.md'), 'w').write(''.join(L))

    print(f"[i] upper-mid under-pricing peak {hump['resid_rel_pct']:+.1f}% @ pick {hump['pick']}; "
          f"deep-tail over-pricing onset @ pick {xo}")
    print(f"[i] resid @ picks 10/30/60/99 = "
          f"{prim[10]['resid_rel_pct']:+.1f}/{prim[30]['resid_rel_pct']:+.1f}/"
          f"{prim[60]['resid_rel_pct']:+.1f}/{prim[99]['resid_rel_pct']:+.1f} %")
    print("[i] wrote out/rider_i_calibration.{json,md,svg} (+residual.svg)")
    print("RIDER_I_COMPLETE")

if __name__ == '__main__':
    main()
