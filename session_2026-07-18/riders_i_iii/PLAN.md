# PLAN — LADDER-VIEWING RIDERS (i)–(iii)  ·  seat 13  ·  R107.6 / item 325 "Adopt"

**REPORT-ONLY, read-only.** These are the statistical instruments the owner reads at the ladder.
Nothing here gates, nothing merges, no value moves. The binding law is the **item-325 lesson**
(CORE rule 7 / R107.4): **finest resolution the sample supports, SMOOTHED (kernel / local
regression), per EXACT pick — NEVER decile bands, never a wide bin presented as one number.**
Thin slices pooled only deliberately and **declared on the artifact**. No verdict language:
these are **findings** for the owner's viewing (S4). **GROSS STAYS GROSS (R107.7)** — no
replacement subtraction anywhere in (i)–(iii). Rider (iv) is NOT in this job.

The tail read (item 325 §1) is **deliberately not a target**: this job MEASURES and reports;
interpretation happens at the owner's viewing, not here. No number is bent toward any expectation.

---

## BASE / STAMPS (asserted at load; HALT on mismatch — see FIRST_COMMANDS_PROOF.txt)

| stamp | value | meaning |
|-------|-------|---------|
| code SHA (engine-content base) | `e4177c21934148c19d9cec3c015fee5d28480102` | the frozen Leg-D ACT-2 candidate |
| pvc curve payload md5 | `89c14729` | `pvc_curve_v2.json` `curve_md5` (the frozen curve) |
| store base md5 | `968de0c7` | per-entrant / curve `derived_from` base (boot-store guard stamp) |
| per_entrant md5 | `40d7da7c` | realized-trajectory source (`stamp.per_entrant_md5`) |
| curve file md5 | `56dd7a7b` | raw `pvc_curve_v2.json` file |

Every output artifact carries all of these so the ladder can assert, mechanically, that these
early-computed riders describe the final candidate. Frozen inputs are **read from the `e4177c2`
git object** and their md5s asserted in `scripts/common.py` — never written into the tree.

## FENCE (derived from the job list)

**IN:** `session_2026-07-18/riders_i_iii/` — all outputs (`out/`) and all analysis scripts
(`scripts/`) live here.
**HARD-OUT (read-only inputs / never touched):** the store · ALL engine code (`rl_model.py`,
`_merged_recover.py`, `s4_matrix_7147.py`, …) · `engine/rl_after/pvc_curve_v2.json` **as a write**
(read-only input) · `docs/` (builds never author docs) · the five-migration build's branch and
files (disjoint). If a job mechanically requires touching a HARD-OUT file → **HALT** and return the
conflict. Mid-flight scope growth ⇒ new directive, new chat.

---

## THE FROZEN OBJECT WE ARE VIEWING (established by reading the derivation, not assumed)

`PVC(p)` = the year-0 point of the 2-D (pick × career-year) evidence-weighted **non-median** fit
(`derive_pvc2.py`, R107.3). Shipped `tau=0.12` ⇒ `exp(-t/tau)` at t≥1 ≈ 2·10⁻⁴, so the year-0
slice is **dominated by the day-after entry value `v0`**: the frozen curve is, to within its own
G-Y0 gate, the **smoothed per-exact-pick mean of `v0`** (verified: curve vs mean-`v0` matches to a
few SCAR at picks 1/30/50/99). This is a property of the frozen object, stated as context — it is
the reason a *realized-outcome* view is informative: the curve prices the **entry** snapshot; the
riders read it against what players drafted at each pick **realized**.

**Realized outcome (DECLARED primary):** `realized_i = mean(vpath_i)` — the mean of the entrant's
realized walk-forward as-of value trajectory. This is the codebase's own life-path measure
(`build_memo_c` uses `mean(vpath)` as the evidence end). **Gross** (R107.7). **Busts full weight**
(R107.3): a bust's low trajectory is included at its real values, never dropped. Every in-curve
entrant has ≥1 `vpath` point (no empty-path edge case).
**Declared sensitivity (secondary, reported alongside — never the headline):** `realized = peak`
(the survivor-credited upper framing) and `realized = cur` (terminal as-of).

**Right-censoring (DECLARED, drives every cohort split):** mean `vpath` length falls 6.8 (2006) →
2.0 (2024) → 1.0 (2025); recent cohorts are ~100% still-active. Realized life-path is only
**complete for cohorts ≲ 2017**. Recent cohorts cannot support a realized calibration — their
realized ≈ entry (circular). This is the **short-draft-era caveat**; it is stated on every artifact
where era coverage thins the sample.

**Fit window:** the curve was fit on in-curve `2004 ≤ year ≤ 2024`. Held-out cohorts = **2003**
(pre-fit, complete careers → the genuine out-of-sample cohort) and **2025** (post-fit, censored →
non-comparable; caveat).

**Smoother (all riders):** Gaussian kernel over **log-pick**, adaptive bandwidth grown until local
eff-n ≥ `NMIN=35`, mirroring the frozen curve's own `fit_year0` smoother (`hmin=0.10, hmax=0.60`)
so predicted and realized sit on equal footing. Per exact pick; bandwidth and eff-n reported at
every pick so "finest resolution the sample supports" is explicit and auditable. No decile bands.
Pick 1 is the **numeraire pin (3000), not a fit point** — flagged, never scored as a miss. Pick 99
is a **deep-pick sink (n≈252)**, not one exact pick — flagged wherever it appears.

---

## JOB → OUTPUT MAP (one rider = one commit)

### Rider (i) — realized-outcome cohort-holdout calibration + washout-exit calibration
`scripts/rider_i_calibration.py` → `out/rider_i_calibration.json`, `out/rider_i_calibration.md`,
`out/rider_i_calibration.svg`
- Smoothed **predicted (frozen curve) vs realized (`mean vpath`)** calibration, **per exact pick**,
  on the **career-complete pool** (cohorts ≲ 2017), with the **residual curve** (signed rel %).
- **Cohort-holdout:** overlay **in-fit-era complete (2004–2017)** vs **held-out complete (2003)**
  calibration/residual curves; 2025 shown only as censored (caveat). Complemented by a
  leave-one-cohort-out residual envelope so the residual shape is shown not to hinge on one cohort.
- **Washout/delist-exit calibration (own view):** restrict to **exited** entrants
  (`delisted or retired_now`) — terminal, censoring-free realized — calibrated per exact pick.
  Busts full weight.
- Declared sensitivities: `peak` / `cur` realized curves reported beside the primary.

### Rider (ii) — cohort-bootstrap tail influence + short-draft-era caveat
`scripts/rider_ii_bootstrap.py` → `out/rider_ii_bootstrap.json`, `out/rider_ii_bootstrap.md`,
`out/rider_ii_bootstrap.svg`  *(bootstrap backgrounded with an asserted completion marker)*
- **Bootstrap over COHORTS, not rows** (rows within a draft year are correlated; the cohort is the
  resampling unit — stated as the reason). B≈2000 resamples of the complete-career cohorts;
  recompute the smoothed realized/residual curve each draw; report **per-exact-pick dispersion**
  (SD, 5–95%) — how much cohorts swing each pick, concentrated in the deep tail (~p50+).
- **Single-player / single-cohort influence:** leave-one-player-out and leave-one-cohort-out max
  |Δ| per tail pick, **naming** the player/cohort that moves each tail pick most.
- **Short-draft-era caveat** annotated per pick: contributing-cohort count / eff-n, and a flag
  wherever the tail slice is dominated by few cohorts or by the pick-99 sink.

### Rider (iii) — uncertainty grading past ~p50
`scripts/rider_iii_uncertainty.py` → `out/rider_iii_uncertainty.json`, `out/rider_iii_uncertainty.md`,
`out/rider_iii_uncertainty.svg`
- A **continuous, smoothed uncertainty grade** `U(p)` along the curve **past ~p50**, built from the
  rider-(ii) cohort-bootstrap dispersion and the rider-(i) holdout residual spread at each exact
  pick (relative %). A single continuous grade curve — **no bands** — with the drivers (thin
  per-pick n, few contributing cohorts, censoring) annotated per pick.

### EXIT
`README.md` mapping each artifact → the rider it serves → its stamps · candidate PR (report-only).

---

## METHOD DISCIPLINE (the item-325 lesson, encoded per rider)
1. Per **exact pick**, kernel-smoothed. No decile bands anywhere. Pooling (career-complete pool;
   pick-99 sink) is deliberate and declared on the artifact.
2. Resampling unit = **cohort** (draft year), never the row.
3. **Busts full weight** (R107.3); **gross** (R107.7); pick-1 numeraire and pick-99 sink flagged.
4. **Findings, not verdicts** (S4). No gate, no pass/fail, no target.
5. **Silence is a red** (S1): every check prints a verdict or HALTs; exit codes propagate;
   backgrounded compute ends in an **asserted** completion marker.
