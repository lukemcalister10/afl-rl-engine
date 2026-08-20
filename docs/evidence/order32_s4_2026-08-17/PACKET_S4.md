# PACKET_S4 — THE OLD-LAW SHOOTOUT: did poles-and-pars actually predict worse?

**ORDER 32 seat S4 · read-only · prereg = `PREREG_S4.md`, committed and pushed (bf39901) BEFORE any
comparison number existed; every rule below was fixed there and none was changed after results.**
Scorer: `s4_shootout.py` (this directory). Full per-cell output with CIs: `RESULTS_S4.json`.

The owner asked: *"How do we know that paying for pedigree via poles and pars regardless of delivery
wasn't a strong way compared to this? How do we know draft pedigree isn't an effective predictor?"*

---

## 0 · THE HEADLINE — THE OLD LAW WINS REAL CELLS, AND THEY HAVE A SHAPE

**The old law is not dominated.** Out of the 24 primary ND cells (vantage years 1–6 × two horizons ×
two metrics), the preregistered verdict is **8 candidate / 8 tie / 8 old law** — a dead heat by cell
count. The cells are not scattered; they split perfectly by career age:

- **Years 1–3 after the draft: the candidate sweeps.** 8 wins, 4 ties, 0 losses. Its edge is large
  where it wins — up to **+0.085 Spearman** at year 1 (0.570 vs 0.485).
- **Years 4–6: the old law sweeps the rank metric.** 8 wins, 4 ties, 0 candidate wins. Its edge is
  small but statistically solid — **−0.008 to −0.023 Spearman**, every 90% CI excluding zero.

So the honest answer to the first question is: **paying for pedigree via poles and pars was NOT a
strong way to price years 1–3 — that is where the candidate's delivery-weighted law is clearly
better, and the margins there are 3–4× the old law's late margins. But from year 4 onward the old
law's stickier pedigree carry ranks remaining careers slightly better than the candidate does, and
that is a real, replicated result, not noise.** The pool arms never favour the old law anywhere
(candidate 27 wins / 53 ties / 0 losses across RD, MSD, other-pool and pool-all cells).

And the second question: **draft pedigree IS an effective predictor — at every horizon tested.**
Raw pick alone carries Spearman 0.40–0.47 against delivered value in years 1–2 and is still 0.25–0.31
at years 4–6, with every 90% CI excluding zero (§4). But it is far below either machine (0.48–0.80),
so "pedigree is real" and "pedigree alone is enough" are different claims — the first is true, the
second is not.

---

## 1 · WHAT WAS COMPARED (and how the old law was identified)

Two walk-forward per-entrant matrices, **byte-identical in everything except the valuation columns**
(2,648 records; identical keys, `yrs`, `seasons`, type/pick/year/pos on all records; same store
`cb38ef11`, same `v0surf 4405cba2`, same #338 minimum-tenure windows, same emitter family):

| | CANDIDATE | OLD LAW |
|---|---|---|
| matrix (md5) | `per_entrant_O31FFINAL.json` (`d97f1aee`) | `per_entrant_O29CFINAL.json` (`6db06e40`) |
| engine | `71d9949a`, `RL_O31=1` — the ORDER 31-F one law | `a353a9d3` — the ORDER 29C landed tree |
| what prices a player | `rho·Phat + [D·(1−rho) + Phi·beta·rho]·V0` — delivery-weighted, one formula | the standing pre-31 machinery: pedigree POLE leg live, PAR tables live, pathway pedestals live, **no delivery fade** |

**Identification evidence that O29CFINAL is truly the poles-and-pars law:**
1. The engine deletes the pole leg and the par-built ISO pick-tax **only** under the preview/O31
   dials — `_merged_recover.py:436-440`: `_O30B_NOPOLE` / `_O30B_NOISO` are true only when
   `RL_O30B_PREVIEW` / `RL_O30B_RESOLVED` / `RL_O31` is set. Dials off ⇒ poles and pars ACTIVE.
2. The O29C emit ran on the ORDER 29C landed tree (`emit.log`: `engine=a353a9d3`), which **predates
   the 30B/31 lanes entirely**; its emitter reads **zero** `RL_O31`/`RL_O30B` variables
   (`grep -c "RL_O31\|RL_O30B" emit.py` → 0; its only env reads are RL_REPO/RL_WORKDIR/etc.).
3. `PREREG_30B.md` names what 30B later deleted — "the 26A forbidden set (pathway pedestals, par
   tables, prior poles)" — i.e. at 29C those objects ARE the standing law.
4. Caveat, disclosed in the prereg: the literal dial-off board at HEAD is the 30B **Step-2** law
   (fade already wired). O29C is one step further back — the machinery **without** any delivery-fade
   of pedigree, which is exactly the law the owner's phrase "regardless of delivery" describes. No
   per-entrant matrix of the intermediate Step-2 law exists; none was fabricated.

**Ground truth** is raw production, not either engine's marks: each realized season is priced by the
house Ruling-3 callable — `posval(avg + capt_prem(avg) − bar) × 21`, Ruling-1 bars (KPD 65.4 ·
KPF 63.8 · MID 77.1 · RUCK 75.5 · SD 75.3 · SF 67.9), √-games weight — with two horizons per vantage
year Y: **next season** (`DV1`, the year-Y+1 season, 0 if none) and **rest of career**
(`DVrest`, all realized seasons Y+1…2025, flat-14 discounted, zeros stay in, **no projections**).
Vantage-N predictor = each machine's own as-of price `ev(p, draft_year+N)`. Cohorts: ND pick 1–64
(primary), pool arms; entry ≥ 2005 (left censor), futures observable through 2025 (2026 in progress
excluded); players whose #338 window closed before the vantage carry no live price on either machine
and are excluded with counts disclosed (`RESULTS_S4.json::meta.exclusions`).

**Verdict rule (fixed in prereg):** per cell, paired player bootstrap (B=2,000, seed 32), Δ =
candidate − old law skill; a machine wins iff the 90% CI on Δ excludes zero, else statistical tie.
Metrics: **M1** = Spearman within cell; **M2** = normalized mean absolute error of relative value
(both series scaled to mean 1; lower better).

---

## 2 · PRIMARY VERDICT TABLE — ND pick 1–64, vantage years 1–6

ρ = Spearman (higher better) · NMAE = relative-value error (lower better) · Δ>0 favours candidate.

| N | horizon | n | ρ cand | ρ old | Δρ [90% CI] | M1 verdict | NMAE cand | NMAE old | M2 verdict |
|---|---|---:|---:|---:|---|---|---:|---:|---|
| 1 | next season | 1201 | **0.570** | 0.485 | +0.085 [+0.067, +0.105] | **CANDIDATE** | 1.321 | 1.308 | tie |
| 1 | rest of career | 1201 | **0.576** | 0.528 | +0.048 [+0.030, +0.067] | **CANDIDATE** | 0.993 | 0.999 | tie |
| 2 | next season | 1137 | **0.668** | 0.626 | +0.043 [+0.023, +0.063] | **CANDIDATE** | **1.067** | 1.094 | **CANDIDATE** |
| 2 | rest of career | 1137 | **0.677** | 0.644 | +0.034 [+0.014, +0.053] | **CANDIDATE** | **0.879** | 0.900 | **CANDIDATE** |
| 3 | next season | 955 | 0.677 | 0.665 | +0.012 [−0.003, +0.025] | tie | **0.854** | 0.883 | **CANDIDATE** |
| 3 | rest of career | 955 | 0.689 | 0.692 | −0.003 [−0.017, +0.012] | tie | **0.790** | 0.809 | **CANDIDATE** |
| 4 | next season | 807 | 0.681 | **0.701** | −0.020 [−0.031, −0.009] | **OLD LAW** | 0.747 | 0.747 | tie |
| 4 | rest of career | 807 | 0.729 | **0.752** | −0.023 [−0.034, −0.012] | **OLD LAW** | 0.684 | **0.675** | **OLD LAW** |
| 5 | next season | 680 | 0.704 | **0.718** | −0.014 [−0.022, −0.006] | **OLD LAW** | 0.642 | 0.637 | tie |
| 5 | rest of career | 680 | 0.748 | **0.765** | −0.017 [−0.025, −0.009] | **OLD LAW** | 0.614 | **0.606** | **OLD LAW** |
| 6 | next season | 574 | 0.726 | **0.733** | −0.008 [−0.014, −0.001] | **OLD LAW** | 0.631 | 0.627 | tie |
| 6 | rest of career | 574 | 0.791 | **0.801** | −0.010 [−0.016, −0.005] | **OLD LAW** | 0.581 | 0.577 | tie |

**Score: 8 candidate / 8 tie / 8 old law.** The crossing sits between years 3 and 4. The candidate's
early wins are 3–4× the size of the old law's late wins, and the late M2 (calibration) gaps are
mostly ties — but the late M1 losses are consistent across both horizons and both eras (§3) and are
not dismissible.

## 3 · SLICES — every family, every old-law win printed

**Verdict tallies by family** (scored cells; M1+M2 combined):

| family | candidate | tie | old law |
|---|---:|---:|---:|
| ND primary (above) | 8 | 8 | 8 |
| ND pick bands × N | 19 | 84 | 17 |
| ND eras × N | 16 | 24 | 8 |
| RD (rookie draft) | 6 | 18 | 0 |
| MSD | 2 | 6 | 0 |
| other pool (ND>64/UNR/IRE/SSP/PDA/PDN/PDS) | 8 | 16 | 0 |
| POOL-ALL | 11 | 13 | 0 |
| day-0 supplementary | 2 | 4 | 2 |
| **all scored cells** | **72** | **173** | **35** |

**Every cell the old law wins** (all 35, verbatim from `RESULTS_S4.json`; Δ>0 favours candidate):

| cell | N | horizon | n | metric | Δ [90% CI] |
|---|---|---|---:|---|---|
| ND band 1-10 | 1 | next | 190 | M1 | −0.063 [−0.127, −0.002] |
| ND band 1-10 | 1 | next | 190 | M2 | −0.045 [−0.072, −0.023] |
| ND band 41-64 | 3 | rest | 275 | M1 | −0.060 [−0.111, −0.011] |
| ND (primary) | 4 | next | 807 | M1 | −0.020 [−0.031, −0.009] |
| ND band 21-30 | 4 | next | 134 | M1 | −0.034 [−0.072, −0.000] |
| ND band 21-30 | 4 | next | 134 | M2 | −0.025 [−0.046, −0.004] |
| ND era 2005-2014 | 4 | next | 507 | M1 | −0.017 [−0.030, −0.003] |
| ND era 2015+ | 4 | next | 300 | M1 | −0.024 [−0.043, −0.006] |
| ND (primary) | 4 | rest | 807 | M1 | −0.023 [−0.034, −0.012] |
| ND (primary) | 4 | rest | 807 | M2 | −0.009 [−0.017, −0.001] |
| ND band 11-20 | 4 | rest | 160 | M2 | −0.015 [−0.030, −0.002] |
| ND band 21-30 | 4 | rest | 134 | M1 | −0.030 [−0.062, −0.001] |
| ND band 21-30 | 4 | rest | 134 | M2 | −0.022 [−0.040, −0.002] |
| ND era 2005-2014 | 4 | rest | 507 | M1 | −0.019 [−0.033, −0.006] |
| ND era 2015+ | 4 | rest | 300 | M1 | −0.025 [−0.043, −0.008] |
| ND (primary) | 5 | next | 680 | M1 | −0.014 [−0.022, −0.006] |
| ND band 11-20 | 5 | next | 136 | M2 | −0.020 [−0.031, −0.010] |
| ND band 21-30 | 5 | next | 113 | M1 | −0.020 [−0.040, −0.003] |
| ND band 21-30 | 5 | next | 113 | M2 | −0.017 [−0.029, −0.002] |
| ND era 2005-2014 | 5 | next | 451 | M1 | −0.015 [−0.024, −0.005] |
| ND (primary) | 5 | rest | 680 | M1 | −0.017 [−0.025, −0.009] |
| ND (primary) | 5 | rest | 680 | M2 | −0.008 [−0.014, −0.002] |
| ND band 11-20 | 5 | rest | 136 | M1 | −0.020 [−0.042, −0.000] |
| ND band 21-30 | 5 | rest | 113 | M1 | −0.024 [−0.044, −0.007] |
| ND band 41-64 | 5 | rest | 183 | M1 | −0.026 [−0.049, −0.004] |
| ND era 2005-2014 | 5 | rest | 451 | M1 | −0.017 [−0.027, −0.009] |
| ND era 2005-2014 | 5 | rest | 451 | M2 | −0.011 [−0.018, −0.005] |
| ND (primary) | 6 | next | 574 | M1 | −0.008 [−0.014, −0.001] |
| ND band 11-20 | 6 | next | 116 | M2 | −0.008 [−0.016, −0.000] |
| ND band 41-64 | 6 | next | 148 | M2 | −0.016 [−0.029, −0.004] |
| ND (primary) | 6 | rest | 574 | M1 | −0.010 [−0.016, −0.005] |
| ND band 41-64 | 6 | rest | 148 | M1 | −0.019 [−0.035, −0.006] |
| ND era 2005-2014 | 6 | rest | 405 | M1 | −0.011 [−0.018, −0.004] |
| ND day-0 | 0 | next | 1265 | M2 | −0.008 [−0.014, −0.002] |
| ND day-0 | 0 | rest | 1265 | M2 | −0.015 [−0.025, −0.005] |

Two named losses deserve the owner's eye beyond the year-4-6 block:
- **Top-10 picks, year 1** (n=190): the old law ranks AND calibrates first-year delivery of the
  premium picks better (Δρ −0.063; ΔNMAE −0.045). At the very head of the draft, one year in, the
  pole-held pedigree price was the better predictor.
- **Day-0 calibration**: at the gate the candidate's entry ladder RANKS better (+0.029/+0.012, both
  CIs clear of zero) but the old law's day-0 relative-value ladder is slightly closer to realized
  relative delivery (M2, both horizons). Rank and level pull in opposite directions at day 0.

Both eras show the same year-4+ pattern, so this is not an era artifact. The pool arms are a clean
sweep for the candidate: **0 old-law wins in 78 scored pool cells** (day-0 pool cells tie trivially —
the two laws share the pool day-0 cells).

## 4 · IS DRAFT PEDIGREE AN EFFECTIVE PREDICTOR? — YES. AND IT IS NOT ENOUGH.

Pedigree standalone (ND arm; Spearman vs realized delivered value; 90% bootstrap CI), beside what
each machine achieves at the same vantage:

| N | horizon | **raw pick alone** [CI] | frozen v0 (old) | frozen v0 (cand) | old law live | candidate live |
|---|---|---|---:|---:|---:|---:|
| 1 | rest | **0.449** [0.412, 0.489] | 0.445 | 0.457 | 0.528 | 0.576 |
| 2 | rest | **0.466** [0.426, 0.503] | 0.457 | 0.471 | 0.644 | 0.677 |
| 3 | rest | **0.347** [0.299, 0.395] | 0.368 | 0.367 | 0.692 | 0.689 |
| 4 | rest | **0.306** [0.251, 0.361] | 0.336 | 0.333 | 0.752 | 0.729 |
| 5 | rest | **0.297** [0.237, 0.354] | 0.339 | 0.333 | 0.765 | 0.748 |
| 6 | rest | **0.275** [0.206, 0.338] | 0.334 | 0.320 | 0.801 | 0.791 |

(next-season horizon shows the same shape: pick ρ 0.40 → 0.25 from N1 to N6, every CI clear of zero;
full numbers in `RESULTS_S4.json`.)

Three plain facts:
1. **Pedigree is a real predictor at every horizon tested** — six years after the draft, the pick a
   player was taken at still rank-correlates ~0.27 with the rest of his delivered career, CI clear of
   zero. The owner's instinct that pedigree carries persistent signal is confirmed, and this matches
   ORDER 30B-M's conditional finding (pick still predicts after production/age/position out to ~70
   games).
2. **Frozen day-0 pedigree never decays to noise** — a v0 you never update still holds ρ ≈ 0.33 at
   year 6. Pedigree "regardless of delivery" is genuinely informative...
3. **...but both machines roughly double it.** Live prices reach ρ 0.53–0.80 where pedigree alone is
   0.27–0.47. Whatever else divides the two laws, watching delivery adds enormous predictive power
   over any pedigree-only rule. Nobody should trade on poles alone.

## 5 · PLAIN-LANGUAGE CONCLUSION

**Was poles-and-pars a strong way?** Stronger than the program has been saying — and in specific,
now-measured places, stronger than the candidate. The old law was **not** a bad predictor: by year 4
it ranks remaining careers slightly *better* than the one law (ρ up to 0.80 at year 6, beating the
candidate by 0.008–0.023 with clean CIs), it beat the candidate on the top-10 picks' first year, and
its day-0 relative ladder was marginally better calibrated. The reason is visible in §4: pedigree
signal persists deep into careers, and the old law's poles-and-pars carry holds onto that signal
where the candidate's delivery-weighting fades it slightly too fast in mid-career.

**Why the candidate still carries the argument on outcomes:** its wins are where the money moves —
years 1–3, the biggest cohorts, the largest margins in the whole exercise (+0.03 to +0.085 ρ, plus
four calibration wins) — and the entire pool side, where the old law never wins a cell. Cell counts
over everything measured: candidate 72, tie 173, old law 35. But the shootout's honest summary is
not "the candidate dominates"; it is: **the candidate prices the young and the pool better; the old
law's pedigree carry priced established mid-career players a little better; and the measured gap at
years 4–6 is a named, bounded defect the one law should be asked to close** (its ρ-fade of pedigree
looks ~1–2 points of rank skill too aggressive after year 3 — consistent with the 30B-M persistence
measurement that was already on the record).

**Limitations (standing):** one store, one league history — the bootstrap CIs are within-history
dispersion, not across-history; delivered value is the house v0-language construction (√-games,
Ruling-1 bars, flat-14) and level conclusions do not transfer outside it; the old law here is O29C
(pre-fade poles-and-pars) — the intermediate Step-2 dial-off law (poles+pars+fade) has no emitted
matrix and was not scored; 2026 is right-censored, so N=1 for the 2024 class and later is unseen.

*Seat S4. The prereg bound; no metric was added, dropped or reweighted after results.*
