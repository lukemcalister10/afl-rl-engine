# RIDER (iv) — THE REPLACEMENT-ADJUSTED VIEW · PLAN (method per job + derived fence)

**REPORT-ONLY · read-only Tier-3 · DO-NOT-MERGE.** Runs parallel to the Leg-E writer (disjoint
files). Nothing gates, nothing merges, no value moves. Findings for the owner's viewing (items
325/332/342), **not verdicts**. The reading is the owner's at the ladder.

## Provenance (asserted at load in `scripts/common_riv.py`, HALT-on-mismatch — silence is a red)
- git entry: `claude/five-migration-pvc-consumers-kxykfd` head = `a90052add8570c014626196cc2e3e13eece02548` (verified this session by `ls-remote`).
- store base md5 `968de0c7` · curve **payload** md5 `89c14729` (curve file `56dd7a7b`) · per_entrant md5 `40d7da7c`.
- R-inputs artifact read from the git object `a90052a:session_2026-07-18/five_migration/out/rider_R_inputs.json`.
- All frozen inputs (curve v2, per_entrant, store) are **byte-identical** at `a90052a` and at the
  riders-(i)-(iii) base pin `e4177c2` (checked); rider (iv) loads from `a90052a` and reuses the
  riders-(i)-(iii) machinery (loader/smoother/realized-outcome convention) verbatim.

## The three R candidates (job 1) — constructed, labelled, symmetric

**Entry points.** The free-intake (no-national-slot) mechanisms enter at pick-equivalents
(R-inputs artifact): **MSD → 90**, all others (SSP/IRE/UNR/PDA/PDN/PDS) → **92**. Pick-equivalents
are curve-independent (measured against realised outcomes; `RIDER_R_inputs_report.md`).

- **(a) R_curve** = the **v2 curve** (`pvc_curve_v2.json`, payload `89c14729`) evaluated at the
  pick-equivalents. v2(90)=473, v2(92)=470 → pooled ≈ **471**.
  - **Circularity note — TESTED, not assumed.** The directive expects "the v2 deep tail was
    partly anchored on pickless pk90 outcomes, so R_curve is partly self-referential." I test this
    against `per_entrant.json` + `derive_pvc2.py`: the v2 curve's `load_pool` is
    `incurve AND real-pick AND 2004≤year≤2024`. **Every mechanism entrant has `incurve=False`**
    (0/389), so all are excluded from the curve fit; the pk86-94 region is anchored by **real-pick
    RD (109) + ND (9)** entrants, **0 mechanism/pickless**. → Under this construction R_curve is
    **not** self-referential on pickless outcomes. Reported as a finding on the artifact.

- **(b) R_realized** = era-matched realised-outcome value of the free-intake pool at the same
  entry points. Method (reuses riders-(i)-(iii) `realized`, gross, R107.3 busts full weight):
  - realised(entrant) = `mean(vpath)` (life-path measure) over non-null career-year points;
    never-produced → **0** (bust, full weight). No prior-anchor `v0` term (that is the list side).
  - **continuous evidence weighting, NO hard maturity cutoff (our law).** weight w = 1.0 if the
    entrant is terminal (`delisted`/`retired_now` → fully observed, bust full weight), else
    `min(1, n_observed_career_years / 6)` — recent/immature cohorts fade smoothly toward 0, none
    excluded. This is the correction to the engine `MECH_STATS` pooled value, which instead takes
    the **most-favourable ≥2021 hard cutoff** (the §5.3/§5.4 failure mode).
  - **era-matching:** each mechanism's realised value is cross-read against the **national (ND)**
    realised value at the same picks and same entry-year span (second panel), and the free-pool
    pick-equivalent is cross-checked against ND realised at pk88-94 (reading-B).
  - pooled free-intake R_realized ≈ **207**; per-mechanism spread ≈ 90–340 (thin — declared).

- **(c) R_owner = 220** — carried as a **labelled reference line only** (owner's stated prior,
  item 332). Not fitted, not an expectation, not fed to any computation.

## Uncertainty on R itself (job 2)
Cohort-bootstrap (resample entrants with replacement, seed **20260718**, B=5000) each mechanism and
the pool; recompute R_realized per draw. Report median, 16/84 (±1σ) and 2.5/97.5 bands, rel-SD.
The mechanism samples are **thin** — MSD 44/17 played, SSP 31/16 (engine cohort); the other five are
5–12 played — **said on every artifact**. Honest grade per R candidate:
- R_curve — grade = the rider-(iii) curve uncertainty at the entry pick (39.8% @ pk90; ≈2.3× the
  17.35% top reference) — the free-pool entry sits in the curve's low-confidence deep tail.
- R_realized — grade = bootstrap rel-SD (expected wide, thin cohorts).
- R_owner — a constant; no sampling uncertainty (it is a prior, graded "asserted, not measured").

## The view (job 3)
Per **exact** pick, smoothed (finest resolution the sample supports; **no decile bands**, item 325):
1. GROSS = v2(p) beside **v−R** for each of the three R candidates, full board 1–99.
2. **p1/p60** and **p1/p90** ratio table of v−R per candidate (vs the GROSS ratio) — how making
   v−R the traded currency re-shapes the ladder.
3. Deep-tail **premium-over-free-pool** curve: v−R past ~p50, per candidate, with the rider-(iii)
   uncertainty grade overlaid.

## THE LAW ON EVERY ARTIFACT (axes note, verbatim on the summary)
"production bars and list-space R are orthogonal (R107.7); v2.11 bakes GROSS either way; making
v−R the traded currency is the named post-v2.11 chapter, on the owner's word."

## FENCE
IN = `session_2026-07-18/rider_iv/` only. HARD-OUT (HALT on any need to write): every engine file,
the store, the curve `pvc_curve_v2.json`, `docs/`, the five-migration branch. Inputs are read
read-only from the `a90052a` git object; nothing outside the fence is written.

## S1–S6, silence is a red. Effort: High. Mode: auto, PLAN first (this file).
