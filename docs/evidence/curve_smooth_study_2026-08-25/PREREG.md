# PREREG — THE SMOOTHING-PASS CANDIDATE (S) AND THE EXTENDED CANDIDATE (X)

**Seat:** derivation seat, read-only on `/home/user/afl-rl-engine`.
**Written:** before any candidate number was computed. Nothing in this file is a result.
**Status:** MEASUREMENT ONLY. **NOTHING LANDS.** No engine byte is touched; no artifact is written.
**Outputs:** `/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/curve_smooth/`

---

## 0. WHAT IS BEING TESTED, AND WHAT IS BEING HELD

The owner has commissioned a **smoothing-pass candidate** against the shipped all-in pick curve
(`engine/rl_after/pvc_curve_v2.json :: curve`, picks 1–64, pick 1 = 3000). The complaint is structural,
not cosmetic: the shipped curve carries a **cliff** (pick 3 → 6, 2569 → 1322) immediately beside two
**PAVA plateaus** (picks 6–12 pooled at 1319, picks 15–20 pooled at 812), separated only by the
`ordering_tiebreak` −1-point-per-pick convention. Those plateaus are the weighted PAVA of ORDER 28
absorbing ascents; the tiebreak makes them *look* like a ladder without being one.

**HELD EXACTLY (carried, not re-decided).** Every one of these is cited to its source below:

| Held object | Source of record |
|---|---|
| Scoring basis: grace-A, Reading O, `G_O = 2` if entry_age ≤ 19 | `inputs/LAYER2.json :: grace_a`, `grace_cfg.reading_O` |
| Fit population: ND 1-64, entry_year 2004–2021 | `inputs/LAYER2.json :: fit_nd_keys` (n = 1142) |
| Window floor 2004 / ceiling 2021 (2022+ = sensitivity, excluded) | `o26b_layer2.py` L606–612, `CFG.window_floor`, Ruling 8 |
| Busts score zero (they are IN the population at value 0) | grace-A totals as serialised; no filter applied |
| Force-majeure: `thomas-boyd`, `paddy-mccartin` excluded; whole-draft slide 2013/2014 | `LAYER2.json :: force_majeure`, ORDER 26B-C1; already baked into `attribution.pick` |
| LOCLIN estimator | `inputs/o26b_loclin.py :: kernel_loclin` (26B-C2) |
| WM aggregator | `inputs/harness_pvc_REPINNED_pass3.py :: kernel_raw` (the SHIPPED year-0 aggregator) |
| `NMIN=35.0, HMIN=0.10, HMAX=0.60`; board `RANGES` | same file, L269–271 |
| RULING B south-boundary seam (`NORM_LO,NORM_HI = 4,48`; `ZONE_NORTH_LIMIT = 50`; smoothstep) | `o28_derive.py :: hybrid_boundary`, PREREG_ORDER28 §2 |
| RULING C monotone: SHIPPED weighted PAVA, non-increasing, weights = per-pick cohort n | `engine/forward_valuation/par_build.py :: _pava`, lifted by source text, md5-printed |
| Anchor: pick 1 = 3000 | `PIN1` |
| K_SHRINK = 15 | `DERIVE.json :: pool.K` |

**GATE R0 (reproduction).** Before either candidate is reported, the harness must re-run the ORDER 28
pipeline unmodified and reproduce `DERIVE28.json :: candidate.allin` to ≤ 1e-9 on all 64 picks, and
reproduce the published reference head 3191.2 / anchor factor 0.9401. If R0 fails, **no candidate is
reported** and the failure is returned instead. This proves the harness is the estate's machinery and
not a re-implementation.

---

## 1. CANDIDATE S — THE SMOOTHING PASS

### 1.1 The pipeline, with the one added step named

ORDER 28 ships:

```
raw cohorts -> LOCLIN -> HYBRID south boundary -> weighted PAVA -> anchor pick1=3000
```

Candidate S inserts **exactly one** declared step, between the hybrid stage and the monotone projection:

```
raw cohorts -> LOCLIN -> HYBRID south boundary -> [ L-SMOOTH ] -> weighted PAVA -> anchor pick1=3000
                                                   ^^^^^^^^^^
                                                   THE ONLY CHANGE
```

### 1.2 L-SMOOTH is the estate's own ruled recipe, not a new invention

The recommended recipe in the commission is the estate's own, from the **modernized bust table**:

> `docs/evidence/bust_prior_rederivation_2026-08-24/build_bust_prior.py` L10:
> *"SMOOTH over pick (L-SMOOTH): isotonic at integer picks -> 5-point centered moving average ->
> non-increasing re-projection (PAVA), so the curve is monotone AND has no plateau cliffs"*

implemented at `build_bust_prior.py :: smooth_curve` (L62–68):

```python
k = np.ones(5) / 5.0
ypad = np.concatenate([[y[0]] * 2, y, [y[-1]] * 2])   # edge-replicate padding, 2 each side
ysm  = np.convolve(ypad, k, mode='valid')             # 5-point CENTERED moving average
proj = IsotonicRegression(increasing=False).fit(picks, ysm)   # non-increasing re-projection
```

**I take this recipe and declare TWO deviations, both forced by standing rulings:**

- **D1 — the re-projection estimator.** The bust recipe re-projects with sklearn's *unweighted*
  `IsotonicRegression(increasing=False)`. On the pick curve, RULING C (#334 c.5276216984 + addendum-2)
  fixes the monotone step as **the SHIPPED weighted PAVA** (`par_build.py::_pava`, weights = per-pick
  cohort n). Ruling C governs the curve; the bust table's unweighted projector does not. **I use the
  ruled weighted PAVA.** Structurally this is the same stage — "non-increasing re-projection" — with the
  estimator the curve's own ruling names. This is why the added step is written above as L-SMOOTH's
  *moving-average half only*: its re-projection half is the PAVA that ORDER 28 already runs.
- **D2 — the input to the MA.** The bust recipe smooths an *already-isotonic* curve. Here the MA is
  applied to the **pre-PAVA hybrid**, which is not yet monotone. This is deliberate and is the whole
  point: smoothing *before* the projection is what stops PAVA from manufacturing plateaus, because the
  ascents the MA absorbs are ascents PAVA never has to pool. Smoothing *after* PAVA would sand the
  plateaus but re-break monotonicity and re-require a projection — an infinite regress.

**Bandwidth justification.** The 5-point width is not chosen by me; it is the estate's ruled width, taken
as-is. I therefore owe no bandwidth argument — but I will **report the ablation** (3-point and 7-point)
as a sensitivity so the owner can see what the width buys. No kernel alternative is declared; the
declared recipe is the rectangular 5-point centered MA with edge-replicate padding, verbatim, and the
MA half of `smooth_curve` is **lifted by source text and md5-printed**, the estate's own reuse discipline.

### 1.3 What is reported for Candidate S

1. **Per-pick table, old vs new**, all 64 picks: shipped integer curve · ORDER-28 float `allin` ·
   Candidate S · Δ · Δ%. Written to JSON; headline picks tabled in the report.
   Two baselines are used on purpose: the **shipped integer curve** is what the owner sees and what the
   board consumes; the **ORDER-28 float `allin`** is the apples-to-apples derivation comparison that
   isolates the smoothing pass from the integer/tiebreak re-basing.
2. **Total value conservation**, three readings, each old / new / Δ%:
   - plain total `Σ_p curve(p)` over 1–64 (shipped reference: `ordering_tiebreak.curve_plain_sum_post = 47315`)
   - cohort-weighted total `Σ_p n_p · curve(p)` — the A2 basis, the "board-consumed weighted total"
   - share-weighted positional grand total `Σ_g Σ_p share_g(p)·posv_g(p)` (must equal the plain total by
     the 30B conservation scalar)
   **Owner tolerance: 1%.** Declared in advance: **no post-hoc rescale of the curve will be applied to
   hit that tolerance.** The drift is measured and published as measured. If |Δ| > 1% on any of the three,
   it is reported as a **BREACH** with its number, not absorbed. (The estate's own "NO SLASH" discipline,
   `o30b_v0refit.py` L17.)
3. **Where the cliff and the plateaus land**: the pick 3→6 step, and the pick ranges (if any) that PAVA
   still pools, with block lengths — the direct answer to the commission.
4. **A1 / A2 / A3**, the ORDER-28 asserts, re-run verbatim:
   - **A1** PAVA must not pool pick 1 with pick 2 (never silently rescale the anchor)
   - **A2** weighted-sum conservation across the PAVA step, |post/pre − 1| < 1e-12
   - **A3** output non-increasing over the domain
5. **A5 is expected to move and that is disclosed, not hidden.** ORDER 28's A5 records that the boundary
   and monotone steps both leave pick 1 alone, so the pre-anchor head, the anchor factor and the
   pick-vs-player premium are unchanged. **The MA does not leave pick 1 alone** — pick 1 is an MA
   boundary and is pulled toward picks 2–3. So Candidate S **will** move the pre-anchor head and
   therefore the anchor factor and the premium. This is predicted here, in advance, and will be reported
   with its number. Anything downstream keyed to the pre-anchor head is flagged as out of scope for this
   seat rather than silently assumed unaffected.

---

## 2. CANDIDATE X — THE EXTENDED CANDIDATE (no hard 64 endpoint)

Answers *"What would happen if pick 64 wasn't a hard endpoint"*.

### 2.1 Domain and population

- **Domain:** picks **1–70**. Everything else identical to Candidate S (same L-SMOOTH, same PAVA, same
  anchor pick 1 = 3000).
- **Entrants added:** ND rows whose (slid) pick is 65–70, under the **same** window rule as the ND fit
  (`2004 ≤ entry_year ≤ 2021`), same grace-A totals, same force-majeure exclusions.
- **Declared population accounting.** Those rows are **today** in the pool fit as the `ND>64` pathway
  (`fit_pool_keys`). Moving them onto the curve without removing them from the pool would **double-count**
  them. So for Candidate X they **enter the ND curve fit and leave the `ND>64` pool pathway** — which is
  not a new rule but the estate's own already-ruled mechanic, verbatim:
  > `LAYER2.json :: force_majeure.mechanics`: *"A natural pick 65 slides to 64, **ENTERS the ND 1-64 fit
  > and LEAVES the ND>64 pathway** for that year."*
  Their n, their zero-count and their outcome distribution are reported.
- Picks **71+** stay in the pool as `ND>64`. The extension is to 70 because that is what the commission
  names and where the resolved population is; it is not a claim that the curve should run to 81.

### 2.2 RULING B (south boundary) re-declared for the longer domain — **and why**

Ruling B is asymmetric: LOCLIN holds north + interior, the **south tail reverts toward the shipped
weighted-mean reading** via a smoothstep blend. Its rationale (`o26b_loclin.py` docstring) is *one-sided
boundary bias*: at the deepest pick every borrowed point is northern, so the local-constant WM is
flattered up and the local-linear extrapolation is running on one-sided support.

On the 1–70 domain that rationale **moves with the endpoint**. I declare, for Candidate X:

- **KEEP** the seam machinery and both of its pick-space guards unchanged: interior-norm window
  `NORM_LO, NORM_HI = 4, 48` (still strictly interior of 1–70) and `ZONE_NORTH_LIMIT = 50` (the prereg
  guard on how far north the WM revert may reach — it is a statement about *picks*, not about the
  endpoint, so it does not move).
- **RE-BASE** the blend denominator from the hard 64 to the new endpoint: `t = (p − p0) / (70 − p0)`,
  `w = smoothstep(t)`, so `w(p0) = 0` and `w(70) = 1`. The seam rule is "revert fully **at the deepest
  pick**"; with the domain extended, the deepest pick is 70.

**Why this and not the alternative.** The alternative — hold `w(64) = 1` and let 65–70 ride pure WM —
would re-impose exactly the hard endpoint at 64 that the commission asks us to remove, and would put a
kink at 64 in a curve that now has real data either side of it. Re-basing to 70 is the choice that makes
64 an ordinary interior pick, which *is the question being asked*. **The cost is declared:** picks in the
high 40s–64 now sit at a *lower* blend weight `w` than they did on the 1–64 domain (the same pick is
further from the endpoint), so they revert **less** toward WM and stay **closer to LOCLIN**. That is the
mechanism by which the 48–64 zone will shift, and I will report the shift decomposed against it rather
than presenting it as an unexplained move.

### 2.3 What is reported for Candidate X

- Implied values at picks **65–70**, and how they sit against the shipped `ND>64` pool level
  (`pool_levels.signed_nd65_plus.measured_k15 = 297`, anchored `pool_v0.pathway_levels_anchored['ND>64']
  = 263.9`) — i.e. does the curve, extended, agree with the pool price those same players get today.
- The **shift in the 40–64 zone** vs Candidate S, per pick, with the seam/`w` decomposition above.
- **Alex Dodson** (`alex-dodson`, ND pick 53, RUCK, entry 2024) — his v0 **old → S → X**.
  *Declared now:* Dodson is `window_tier = sensitivity2022+` and is **NOT in any fit population**. He is a
  **consumer** of the curve, not a teacher of it. His number moves only because the surface under him
  moves. Verified: shipped `nd_v0.posv.RUCK[53] = 237.199`, matching the commission's "≈ 238".

---

## 3. POSITIONAL REBUILD (on S, and on X if time permits)

### 3.1 Relativities are REUSED, never refitted

The commission is explicit: *reuse the 31-F-shrunk relativities from the artifact — do not refit them.*
The 31-F shrunk relativity is reconstructed **arithmetically from stored artifact values only**:

```
relat_g(p)   = V0REFIT30B.json::posv_in[g][p] / curve_shipped(p)     # the PRE-monotone surface
w_gp         = pvc_curve_v2.json::nd_v0.head_shrink_31f.credibility_w[g][p]   # AS STORED, not recomputed
rel1_g(p)    = w_gp * relat_g(p) + (1 - w_gp) * 1.0                  # 31-F: K-toward-all-in-relativity
rel2_g(p)    = rel1_g(p) / Σ_h share_h(p) * rel1_h(p)                # 31-F per-pick renormalisation
```

with `share` = `pvc_curve_v2.json :: nd_v0.share` as shipped. **No estimator is run.** In particular the
credibility weights `w_gp` are read from the artifact, *not* recomputed from `kernel_loclin` effective n
— that is the difference between reusing 31-F and refitting it.

**GATE R1.** `rel2` must reproduce the shipped surface: feeding `rel2 × curve_shipped` through the 30B
pipeline must return `nd_v0.posv` as shipped, to ≤ 1e-6. If R1 fails, the reconstruction is wrong and the
positional rebuild is not reported.

**The key property, stated in advance:** `rel2` is normalised so that `Σ_g share_g(p) · rel2_g(p) = 1` at
**every** pick. That identity is **curve-independent**. So `posv_g(p) = rel2_g(p) · curve_S(p)` satisfies
`Σ_g share_g(p) · posv_g(p) = curve_S(p)` **exactly, by construction**, on any candidate curve. This is
why the 31-F pattern is the right one to reuse and why the identity survives the swap.

### 3.2 The pipeline

`rel2 × curve_candidate` → the **committed `o30b_v0refit.py` stages 1–4, lifted by source text and
exec'd verbatim** (the same lift discipline 31-F used, md5-printed):
weighted PAVA (weights = `share_g(p)`) → floor 100 → −1 ordering tiebreak → one conservation scalar λ.

For Candidate X the pipeline runs on the 1–70 domain; the floor-100 plateau anchor, written in 30B as
`v(p) = 100 + (64 − p)`, is **re-based to the endpoint** as `v(p) = 100 + (END − p)` so that the deepest
pick sits exactly on the ruled floor. This is declared as the one necessary edit to the lifted text for X;
**for Candidate S the text is lifted with no edit at all.**

### 3.3 Reconciliation — reported honestly at both levels

The commission asks for the identity "EXACT to 1e-9". **Declared in advance: that is achievable at one
level and not the other, and both are reported rather than one being quoted.**

- **Relativity stage / pre-pipeline:** `Σ_g share_g(p)·posv_g(p) = curve(p)` per pick — **EXACT** (≈1e-16).
  Target ≤ 1e-9. This is the identity the 31-F renormalisation restores.
- **Population identity, post-pipeline:** `Σ_g Σ_p share_g(p)·posv_g(p) = Σ_p curve(p)` — **EXACT** by the
  conservation scalar λ. Target ≤ 1e-9.
- **Per-pick, post-pipeline:** **NOT exact, and cannot be.** Monotonicity and the floor are constraints
  the raw relativities do not satisfy. The shipped surface itself carries
  `nd_v0.reconciliation.per_pick_max_abs_ratio_minus_1 = 0.1718` at pick 64. Candidate S's residual will
  be reported **in full and beside the shipped 0.1718**, so the owner can see whether smoothing makes the
  price of monotonicity cheaper or dearer. It will not be quoted as 1e-9, because it is not.

Reported: per-position head values (pick 1), the floor tail, λ, and **Dodson's new v0**.

---

## 4. THE RUCK QUESTION

*"Please also measure rucks here as they might need to be separated out a little bit."*

From the **fit population only** (the same 1142 ND rows; for the 65–70 band, Candidate X's added rows):

- Bands: **1–10 / 11–20 / 21–40 / 41–64 / 65–70**.
- Cells: **n** and **mean career grace-A delivered value** per band, for **RUCK**, for **KPD**, for
  **KPF**, for the **pooled tall class**, and for the small positions **MID / SD / SF**.
- **Pooled tall class is reported twice**, because the two readings answer different questions and
  conflating them would beg the question: `TALL = KPD ∪ KPF ∪ RUCK` (the class RUCK currently sits in)
  and `TALL_ex_RUCK = KPD ∪ KPF` (the contrast that actually tests separation).
- **CIs:** percentile bootstrap, **10,000 resamples, resampling players within (position, band)**,
  seed **fixed at 20260825** and printed. Non-parametric because these distributions are
  zero-inflated (busts score exactly 0) and nowhere near normal — a t-interval would be a lie here.
- Also reported: **zero-share** (bust rate) per cell, since a mean over a zero-inflated distribution
  is two facts (how often, and how much when it hits) wearing one number.

**The "does the deep tail flatten" test, declared before it is run.** "Flatten" is made falsifiable as a
**within-position flatness ratio**: `F_g = mean(g, 41–70) / mean(g, 1–10)`. A position whose deep tail
flattens relative to another has the **higher** F. Reported with a bootstrap CI on `F_RUCK − F_TALL_ex_RUCK`.

**Verdict rule, fixed in advance so it cannot be fitted to the answer:**
- **SUPPORTS** a ruck-specific deep relativity iff the bootstrap CI on `F_RUCK − F_TALL_ex_RUCK`
  **excludes 0**, *and* the deep-band (41–70) RUCK mean CI does not overlap the `TALL_ex_RUCK` deep mean CI.
- **DOES NOT SUPPORT** if both overlap 0 / each other.
- **INCONCLUSIVE** if exactly one of the two holds, or if any deep RUCK cell has **n < 30** — in which
  case the honest reading is that the deep tail is too thin to separate, and that will be said plainly
  rather than dressed up.

---

## 5. WHAT THIS SEAT WILL NOT DO

- Not write into the repo; not touch `/home/claude/rl_workspace`; not modify any live artifact.
- Not re-fit the 31-F relativities, the pool ladder, the numeraire, or the bust prior.
- Not rescale any candidate curve to hit the 1% tolerance. Measured is published.
- Not report a per-pick reconciliation figure as "exact" when it is not.
- Not land anything. **NOTHING LANDS.**

---

## 6. FILES THIS SEAT WILL WRITE

| File | Contents |
|---|---|
| `PREREG.md` | this file |
| `derive_smooth.py` | the harness (R0/R1 gates, candidates S and X, positional rebuild, ruck cells) |
| `SMOOTH_OUT.txt` | full console transcript |
| `CANDIDATE_S.json` | per-pick old/new table, conservation ledger, asserts, plateaus, ablation |
| `CANDIDATE_X.json` | 1–70 curve, 65–70 values, 40–64 shift, seam decomposition |
| `POSV_REBUILD.json` | rebuilt positional surfaces on S and X, λ, reconciliation at all three levels |
| `RUCK_CELLS.json` | ruck/tall/small band cells, n, means, zero-shares, bootstrap CIs, verdict |
