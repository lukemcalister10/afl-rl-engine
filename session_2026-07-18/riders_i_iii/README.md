# RIDERS (i)–(iii) — the ladder viewing instruments (READ-ONLY, REPORT-ONLY)

Seat 13 · ruled **R107.6 / item 325 "Adopt"** · three of the four adopted ladder-viewing riders,
computed against the **FROZEN Leg-D ACT-2 candidate curve**. Nothing here gates, nothing merges, no
value moves. Findings for the owner's viewing (S4) — **not verdicts**. Rider **(iv)** (the
replacement-adjusted view) is **not** in this job; it waits on the measured-R report from the
five-migration build.

The **item-325 statistical law** is honoured on every artifact: finest resolution the sample
supports, **smoothed** (kernel / local regression) **per exact pick** — **never decile bands**;
thin slices pooled only deliberately and **declared**. **Busts full weight** (R107.3). **Gross
stays gross** (R107.7) — no replacement subtraction anywhere.

## Base pin & the three stamps (asserted at load in every rider — HALT on mismatch)

| stamp | value |
|-------|-------|
| code SHA (engine-content base) | `e4177c21934148c19d9cec3c015fee5d28480102` |
| pvc curve payload md5 | `89c14729` |
| store base md5 | `968de0c7` |
| per_entrant md5 | `40d7da7c` |
| curve file md5 | `56dd7a7b` |

Frozen inputs (`engine/rl_after/pvc_curve_v2.json`, `…/legd_derivation/out/per_entrant.json`) are
**read from the `e4177c2` git object** and their md5s asserted in `scripts/common.py`; they are
never written into the tree. See `FIRST_COMMANDS_PROOF.txt`. (Branch note: this designated dev
branch carries seat-13 governance commits that exist only here; provenance to the candidate is
carried **mechanically by the stamps**, per the directive, not by git parentage.)

## Fence

**IN:** this directory only — `out/` (artifacts) and `scripts/` (analysis). **HARD-OUT (read-only /
untouched):** the store · all engine code · `pvc_curve_v2.json` as a write · `docs/` · the
five-migration branch. No HARD-OUT file was written.

## Artifact → rider → stamps map

Every JSON/MD/SVG below carries the stamp block above (in the JSON `stamps` field / MD header).

| artifact | rider it serves | what it is |
|----------|-----------------|------------|
| `out/rider_i_calibration.{json,md}` | **(i)** | smoothed predicted(frozen curve)-vs-realized(mean vpath) calibration + residual, per exact pick; cohort-holdout (fit-era-complete 2004–17 vs pre-fit held-out 2003) + LOCO envelope; washout/delist-exit as its own view |
| `out/rider_i_calibration.svg` | (i) | predicted vs realized curves |
| `out/rider_i_calibration_residual.svg` | (i) | residual curve, fit-era vs held-out |
| `out/rider_ii_bootstrap.{json,md,svg}` | **(ii)** | cohort-bootstrap (unit = draft year, B=4000) tail influence: RAW per-exact-pick dispersion vs SMOOTHED (borrowed) dispersion; exact single-cohort / single-player leave-one-out swings; short-draft-era caveat |
| `out/rider_iii_uncertainty.{json,md,svg}` | **(iii)** | continuous smoothed uncertainty grade `U(p)` past ~p50 = RSS(rider-ii bootstrap SD, rider-i LOCO half-width), no bands |
| `scripts/common.py` | all | frozen-input loader + stamp assertions + realized-outcome definitions + the log-pick smoother |
| `scripts/svgplot.py` | all | dependency-free SVG line-plot helper |
| `scripts/rider_i_calibration.py`, `rider_ii_bootstrap.py`, `rider_iii_uncertainty.py` | (i),(ii),(iii) | the analyses |
| `PLAN.md` | — | job→output map, derived fence, per-rider method sketch |
| `FIRST_COMMANDS_PROOF.txt` | — | base-pin + three-stamp entry assertions (all PASS) |
| `run_all.sh` | — | re-runnable driver; asserts each rider's completion marker + exit 0 |

## Reproduce

```
bash session_2026-07-18/riders_i_iii/run_all.sh      # -> ALL_RIDERS_COMPLETE (markers asserted)
```
Deterministic (bootstrap seed 20260718); a re-run reproduces the committed outputs byte-for-byte.

## The three findings, in plain terms (findings, not verdicts)

- **(i) Calibration:** measured against what players actually became (career life-path, busts
  included, gross), the frozen curve **under-prices the upper-mid of the board** (picks ~12–48
  realise above their price, peaking about **+20% near pick 20**) and **over-prices the deep tail**
  (the residual turns negative around **pick 49** and deepens to about **−32%** by the pick-99 sink).
  The pre-fit held-out 2003 cohort and the censoring-free washout/exit view show the same deep-tail
  over-pricing. Pick 1 is the numeraire pin and picks 2–11 are noisy (small n) — not a clean signal.
- **(ii) Tail influence:** at its own per-exact-pick resolution the deep tail is far shakier than the
  top — cohort-bootstrap relative spread ~**34%** (p50–98) vs ~**17%** (top), and a **single player
  can move an individual deep-tail pick by up to ~73%**. The smoothed curve only looks steady there
  because it borrows across picks and leans on the pick-99+ sink; the deep tail rests on ~15
  older, career-complete drafts (recent cohorts are still-active and excluded).
- **(iii) Uncertainty grade:** a single continuous grade rises steeply past ~p50 — roughly **2.2×**
  the top's uncertainty by the deep tail — so past about pick 50 the curve should be read as a
  low-confidence region.

## Status

Candidate, **report-only**. Nothing merges without the owner's word (S2 / R107.6).
