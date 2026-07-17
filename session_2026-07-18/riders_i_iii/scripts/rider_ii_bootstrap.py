"""RIDER (ii) — cohort-bootstrap tail influence + short-draft-era caveat. READ-ONLY.

Bootstrap over COHORTS (draft years), NOT rows: rows within a draft year are correlated, so the
cohort is the resampling unit (stated). Shows how much single cohorts / single players swing the
smoothed realized deep tail (~p50+). Fixed smoother bandwidth (from the full complete pool) so the
resolution is held constant while the data are resampled. Busts full weight (R107.3); gross (R107.7).
Finding, not verdict (S4). No decile bands (CORE rule 7 / R107.4). Seeded — reproducible.
"""
import json, sys, os, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
from svgplot import lineplot

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out')
SEED = 20260718
B = 4000
REP_PICKS = [50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 99]

def fixed_bandwidth(pk, nmin=C.NMIN, hmin=C.HMIN, hmax=C.HMAX, hstep=C.HSTEP):
    """Adaptive bw per pick from the (unresampled) pool point-picks; held fixed across bootstrap draws."""
    Lp = np.log(np.asarray(pk, float))
    hs = {}
    for p in range(C.KMIN, C.KMAX + 1):
        L = np.log(p); h = hmin
        while h < hmax:
            if np.sum(np.exp(-0.5 * ((Lp - L) / h) ** 2)) >= nmin: break
            h += hstep
        hs[p] = h
    return hs

def main():
    t0 = time.time()
    curve, per, stamps = C.load_frozen()
    P = C.in_curve_pool(per)
    pool = [r for r in P if C.is_complete_cohort(r)]     # career-complete realized (consistent w/ rider i)
    pk = np.array([r['pick'] for r in pool], float)
    val = np.array([C.realized(r, 'meanvpath') for r in pool], float)
    years = np.array([r['year'] for r in pool])
    names = [r['player'] for r in pool]
    uyears = sorted(set(years.tolist()))
    yidx = {y: i for i, y in enumerate(uyears)}
    ymap = np.array([yidx[y] for y in years])           # cohort index per entrant
    nC = len(uyears)
    print(f"[ii] pool n={len(pool)} over {nC} complete cohorts {uyears[0]}-{uyears[-1]}; B={B} cohort-bootstrap; seed={SEED}")

    grid = list(range(C.KMIN, C.KMAX + 1))
    hs = fixed_bandwidth(pk)
    Lp = np.log(pk)
    # kernel weight matrix K[p_i, entrant_j]  (99 x n)  — the SMOOTHED (cross-pick borrowing) estimator
    K = np.zeros((len(grid), len(pool)))
    for gi, p in enumerate(grid):
        K[gi] = np.exp(-0.5 * ((Lp - np.log(p)) / hs[p]) ** 2)
    # indicator matrix I[p_i, entrant_j] (99 x n) — the RAW per-EXACT-pick estimator (no borrowing; finest resolution)
    I = np.array([[1.0 if int(pk[j]) == p else 0.0 for j in range(len(pool))] for p in grid])

    from collections import Counter
    rawn = Counter(int(x) for x in pk)
    cv = np.array([curve[p] for p in grid])

    # point estimates (unresampled)
    Wp = K.sum(1); smooth0 = (K * val).sum(1) / Wp
    In = I.sum(1); raw0 = np.where(In > 0, (I * val).sum(1) / np.where(In > 0, In, 1), np.nan)

    # ---- COHORT BOOTSTRAP (resample nC cohorts w/ replacement -> per-cohort multiplicity) ----
    rng = np.random.default_rng(SEED)
    draws = rng.integers(0, nC, size=(B, nC))
    mult = np.zeros((B, nC))
    for b in range(B):
        mult[b] = np.bincount(draws[b], minlength=nC)
    Wt = mult.T[ymap]                                              # (n, B) entrant weight per draw
    # RAW per-exact-pick bootstrap (the finest resolution — this is where tail fragility lives)
    rden = I @ Wt; rnum = I @ (Wt * val[:, None])
    raw_boot = np.where(rden > 0, rnum / rden, np.nan)             # (99, B)
    raw_boot_sd = np.nanstd(raw_boot, axis=1)
    raw_boot_rel_sd = 100.0 * raw_boot_sd / np.where(np.isnan(raw0), np.nan, raw0)
    # SMOOTHED (borrowed) bootstrap — contrast: how much stability the smoother buys by pooling
    sden = K @ Wt; snum = K @ (Wt * val[:, None])
    sm_boot = np.where(sden > 0, snum / sden, np.nan)
    sm_boot_rel_sd = 100.0 * np.nanstd(sm_boot, axis=1) / smooth0

    # ---- single-CObHORT / single-PLAYER leave-one-out on the RAW per-exact-pick mean (finest resolution) ----
    loco_rel = np.full(len(grid), np.nan); loco_cohort = np.zeros(len(grid), int)
    ploo_rel = np.full(len(grid), np.nan); ploo_i = np.zeros(len(grid), int)
    contrib = np.zeros(len(grid), int)
    for gi, p in enumerate(grid):
        mem = np.where(I[gi] > 0)[0]
        if len(mem) < 2:
            contrib[gi] = len(set(ymap[mem].tolist())); continue
        vv = val[mem]; mu = raw0[gi]; nmem = len(mem)
        # single-player LOO delta on the raw mean
        d_pl = (mu - vv) / (nmem - 1)
        j = int(np.argmax(np.abs(d_pl))); ploo_rel[gi] = 100.0 * abs(d_pl[j]) / mu; ploo_i[gi] = mem[j]
        # single-cohort LOO on the raw mean
        best = 0.0; bc = 0
        cohs = set(ymap[mem].tolist()); contrib[gi] = len(cohs)
        for c in cohs:
            keep = vv[ymap[mem] != c]
            if len(keep) == 0: continue
            d = abs(np.mean(keep) - mu)
            if d > best: best = d; bc = c
        loco_rel[gi] = 100.0 * best / mu; loco_cohort[gi] = int(uyears[bc])

    series = {}
    for gi, p in enumerate(grid):
        series[p] = dict(
            resid0=round(float(100.0 * (smooth0[gi] - cv[gi]) / cv[gi]), 2),
            smooth0=round(float(smooth0[gi]), 1), raw0=None if np.isnan(raw0[gi]) else round(float(raw0[gi]), 1),
            raw_boot_rel_sd_pct=None if np.isnan(raw_boot_rel_sd[gi]) else round(float(raw_boot_rel_sd[gi]), 2),
            smoothed_boot_rel_sd_pct=round(float(sm_boot_rel_sd[gi]), 2),
            loco_max_rel_pct=None if np.isnan(loco_rel[gi]) else round(float(loco_rel[gi]), 2),
            loco_cohort=int(loco_cohort[gi]) or None,
            player_max_rel_pct=None if np.isnan(ploo_rel[gi]) else round(float(ploo_rel[gi]), 2),
            player=names[int(ploo_i[gi])] if not np.isnan(ploo_rel[gi]) else None,
            n_cohorts_contrib=int(contrib[gi]), raw_n=int(rawn.get(p, 0)))

    # headline: RAW per-pick fragility, tail (p50+, excl the 99-sink) vs top (p<=30)
    def med(key, lo, hi, excl99=True):
        vs = [series[p][key] for p in grid if lo <= p <= hi and series[p][key] is not None and not (excl99 and p == 99)]
        return float(np.median(vs)) if vs else float('nan')
    tail = [p for p in grid if 50 <= p <= 98]
    med_raw_tail = med('raw_boot_rel_sd_pct', 50, 98); med_raw_top = med('raw_boot_rel_sd_pct', 1, 30)
    med_sm_tail = med('smoothed_boot_rel_sd_pct', 50, 98); med_sm_top = med('smoothed_boot_rel_sd_pct', 1, 30)
    worst_player = max(tail, key=lambda p: series[p]['player_max_rel_pct'] or 0)

    worst_player_swing = series[worst_player]['player_max_rel_pct']
    tail_player_max = max((series[p]['player_max_rel_pct'] or 0) for p in tail)
    result = dict(
        rider='(ii) cohort-bootstrap tail influence + short-draft-era caveat',
        stamps=stamps, report_only=True, verdict_language=False,
        declared=dict(resampling_unit='cohort (draft year) — rows within a cohort are correlated',
                      pool='career-complete cohorts (<=2017), realized=mean(vpath); gross; busts full weight',
                      B=B, seed=SEED,
                      raw_estimator='per-EXACT-pick mean (no cross-pick borrowing) — the finest resolution; '
                                    'this is where tail fragility is honestly visible',
                      smoothed_estimator='fixed-bandwidth log-pick kernel — shown as CONTRAST: its tail '
                                         'stability is bought by borrowing from neighbours and the pick-99 sink',
                      pick99='deep-pick sink (raw n~250) — flagged; excluded from tail medians', no_bands=True),
        raw_median_boot_rel_sd_pct=dict(deep_tail_p50_98=round(med_raw_tail, 2), top_p1_30=round(med_raw_top, 2)),
        smoothed_median_boot_rel_sd_pct=dict(deep_tail_p50_98=round(med_sm_tail, 2), top_p1_30=round(med_sm_top, 2)),
        single_player_worst_tail=dict(pick=worst_player, player=series[worst_player]['player'],
                                      swing_rel_pct=worst_player_swing),
        series=series)
    os.makedirs(OUT, exist_ok=True)
    json.dump(result, open(os.path.join(OUT, 'rider_ii_bootstrap.json'), 'w'), indent=1)

    # ---- SVG: RAW per-pick fragility vs SMOOTHED (borrowed) stability + single-player swing ----
    def col(key): return [series[p][key] if series[p][key] is not None else 0 for p in grid]
    svg = lineplot(
        [('RAW per-exact-pick boot rel-SD %', grid, col('raw_boot_rel_sd_pct'), '#d62728', False),
         ('SMOOTHED (borrowed) boot rel-SD %', grid, col('smoothed_boot_rel_sd_pct'), '#1f77b4', False),
         ('single-player max swing %', grid, col('player_max_rel_pct'), '#ff7f0e', True)],
        'exact pick', 'cohort-bootstrap dispersion / swing  [rel %]',
        'RIDER (ii) — cohort-bootstrap tail influence (raw resolution vs borrowed smoothing)',
        subtitle='resample unit=cohort; B=%d seed=%d; gap raw-vs-smoothed = confidence borrowed across picks' % (B, SEED),
        xmarks=[1, 20, 40, 50, 60, 70, 80, 90, 99],
        notes=['RAW = finest resolution', 'SMOOTHED borrows', 'pick99 = deep sink', 'no decile bands'])
    open(os.path.join(OUT, 'rider_ii_bootstrap.svg'), 'w').write(svg)

    # ---- MD ----
    L = []
    L.append('# RIDER (ii) — cohort-bootstrap tail influence + short-draft-era caveat\n')
    L.append('**REPORT-ONLY · finding, not a verdict · gross · busts full weight · no decile bands.**  \n')
    L.append('`%s`\n' % C.STAMP_NOTE)
    L.append('\n**Declared:** resampling unit = **cohort (draft year)**, not the row — rows within a draft '
             'year are correlated, so the cohort is the bootstrap unit. B=%d (seed %d). Realized = '
             '`mean(vpath)` on career-complete cohorts (≤2017). Two estimators are reported per exact pick: '
             'the **RAW per-exact-pick mean** (no cross-pick borrowing — the finest resolution, where tail '
             'fragility is honestly visible) and, as a **contrast**, the fixed-bandwidth **smoothed** kernel '
             '(whose tail stability is *borrowed* from neighbours and the pick-99+ sink). Pick 99 = deep '
             'sink (raw n≈%d), excluded from tail medians. Single-cohort/player swings are exact LOO on the raw mean.\n'
             % (B, SEED, series[99]['raw_n']))
    L.append('\n**Headline (the item-325 point):** at the RAW per-exact-pick resolution the deep tail is '
             '**far less stable** than the top — median cohort-bootstrap relative SD **%.1f%% (p50–98)** vs '
             '**%.1f%% (p≤30)**. The smoother *masks* this: its tail rel-SD collapses to **%.1f%%** only by '
             'borrowing across picks/the sink (top %.1f%%). A single player can swing an individual deep-tail '
             'pick by up to **%.0f%%** (worst: **%s at pick %d, %.1f%%**).\n'
             % (med_raw_tail, med_raw_top, med_sm_tail, med_sm_top, tail_player_max,
                series[worst_player]['player'], worst_player, worst_player_swing))
    L.append('\n## Tail influence by exact pick (p50+)\n')
    L.append('| pick | resid0 % | RAW boot rel-SD % | SMOOTHED boot rel-SD % | 1-cohort swing % (which) | 1-player swing % (who) | #cohorts | raw n |\n')
    L.append('|---|---|---|---|---|---|---|---|\n')
    def f(x, spec='%.1f'): return 'n/a' if x is None else (spec % x)
    for p in REP_PICKS:
        s = series[p]
        flag = ' *(sink)*' if p == 99 else ''
        L.append('| %d%s | %+.1f | %s | %.1f | %s (%s) | %s (%s) | %d | %d |\n'
                 % (p, flag, s['resid0'], f(s['raw_boot_rel_sd_pct']), s['smoothed_boot_rel_sd_pct'],
                    f(s['loco_max_rel_pct']), s['loco_cohort'], f(s['player_max_rel_pct']), s['player'],
                    s['n_cohorts_contrib'], s['raw_n']))
    L.append('\n_Full 1–99 series in `rider_ii_bootstrap.json`; curve in `rider_ii_bootstrap.svg`._\n')
    L.append('\n**Short-draft-era caveat (declared):** the deep-tail per-exact-pick sample is thin '
             '(raw n≈11–15 per pick for picks ~70–98) drawn from only %d complete cohorts, and the '
             'smoothed deep-tail realized leans on the pick-99+ sink. Recent cohorts (>2017) are '
             'right-censored and **excluded** from this realized bootstrap — the tail here rests on the '
             'older, career-complete drafts only, so its coverage genuinely thins with depth.\n' % nC)
    L.append('\n## Finding (one plain sentence, no verdict)\n')
    L.append('At its own (per-exact-pick) resolution the deep tail is markedly less stable than the top '
             'under cohort resampling (median bootstrap relative SD ~%.0f%% vs ~%.0f%%) and a single '
             'player or cohort can move an individual deep-tail pick by up to ~%.0f%%; the smoothed curve '
             'looks steadier there only because it borrows across picks and from the pick-99+ sink, so '
             'deep-tail values are neighbourhood/sink averages, not pick-specific estimates.\n'
             % (med_raw_tail, med_raw_top, tail_player_max))
    open(os.path.join(OUT, 'rider_ii_bootstrap.md'), 'w').write(''.join(L))

    dt = time.time() - t0
    print(f"[ii] RAW boot rel-SD tail(p50-98)={med_raw_tail:.1f}%  top={med_raw_top:.1f}%  | "
          f"SMOOTHED tail={med_sm_tail:.1f}%  top={med_sm_top:.1f}%")
    print(f"[ii] worst single-player tail swing {series[worst_player]['player']}@{worst_player} {worst_player_swing:.1f}%")
    print(f"[ii] wrote out/rider_ii_bootstrap.{{json,md,svg}}  ({dt:.1f}s, B={B})")
    print("RIDER_II_COMPLETE")

if __name__ == '__main__':
    main()
