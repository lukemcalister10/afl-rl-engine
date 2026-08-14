# PREREG — ORDER 30A-2: THE SITTER RE-CUT

**Committed BEFORE any quantity of interest was measured.** Nothing in this file is edited after the
first measurement ran; breaches are owned by number in `SITTER_FADE_PACKET_2.md` §Prereg scored, and
the prediction text is left exactly as filed.

Act: ORDER 30A-2, the measurement seat. Brief:
[#334 comment 5290213551](https://github.com/lukemcalister10/afl-rl-engine/issues/334#issuecomment-5290213551).
Branch `land/order-29`. **READ-ONLY**: no engine file, no board, no store, no curve is touched.
**NOTHING WIRES.** The old `los_decay` schedule stands as the DECLARED FALLBACK until the owner rules.

This act supersedes `SITTER_FADE_PACKET.md` as the ruling basis. It does not rewrite it: ORDER 30A's
artifacts stand on their own basis, untouched.

---

## 0. THE FOUR CORRECTIONS BEING ANSWERED

The owner's words, verbatim from the brief:

1. *"Draft pick is unusable, but what about a band / range of draft picks. There's nothing there at all?"* → **T3**
2. *"if a penalty for 0 is so severe, then it should transition to 1/2/3/4 etc in a curve, not be a hard cliff between 0 games and 1 game"* → **T4**
3. *"Smillie is nearly at the end of year 2, not the start"* → **T2**
4. *"There is information on delistings. We have a policy on helping the model know when a player was listed - so you should have that data?"* → **T1**

---

## 1. THE LISTING SOURCE, NAMED BEFORE IT IS USED (T1)

The owner is right that the data exists. It is not an observation table — it is a **policy
reconstruction**, and this act names it as such on its face.

**THE SOURCE OF RECORD.** The `#338` MINIMUM LISTING TENURE rule, owner word *"Fire 338"* 2026-08-06,
implemented at commit `30996f8` in `engine/rl_after/s4_matrix_M1v7.py:53-70,81,113`, and ported
verbatim into the #338 no-arb lane's emitter at
`docs/evidence/noarb_338_2026-08-06/emit_matrix_338.py:127-160` (helpers `_min_tenure`, `_debut_year`,
`_listed_through`). Its emitted output is
`docs/evidence/noarb_338_2026-08-06/per_entrant_338_confirmation.json`, whose `meta.rule_338` block
carries the rule constants and whose per-record `yrs` array is the reconstructed listed window.

**THE RULE, restated exactly:**

```
min_tenure(p)      = 4 if ND pick 1-20 ; 3 if ND pick 21-40 ; 2 otherwise (ND 41+ and every pool route)
debut_year(p)      = entry_year + 1     (every route except MSD, which debuts in its entry year)
listed_through(p)  = p._last_listed                          if explicitly recorded (a KNOWN FACT)
                   = None  (STILL LISTED)                    if not p._retired
                   = max(debut + min_tenure - 1, last_scoring_year)   otherwise   ("own data extends")
```

**STILL LISTED ENTERING YEAR N** (this act's conditioning event) is therefore
`listed_through is None  OR  listed_through >= entry_year + N`, on the same depth clock as ORDER 30A
(`N = season_year - entry_year`, so the depth-N season is `entry_year + N` and `debut = depth 1`).

**WHAT THIS SOURCE IS, said plainly before any number is read off it.** Explicit `_last_listed` is
non-null on **13 of 2,650** store rows and **3 of 1,570** ND rows (verified on store `cb38ef11` before
this file was written; Layer 1's `last_listed` mirrors it). For a genuine sitter — a retired ND
entrant with zero games and therefore no scoring rows — `last_scoring_year` is 0, so
`listed_through` collapses to `entry_year + min_tenure` exactly. **For that population the
reconstruction is a deterministic function of pick band alone.** It carries no player-specific
delisting observation. This act says so per cell rather than presenting a band rule as a listing
measurement.

**THE TWO READINGS, both published:**

- **L-A — the reconstruction as filed.** `listed_through` exactly as above, including *own data
  extends*. This is what the #338 lane emits.
- **L-B — the outcome-blind floor.** `listed at N iff (min_tenure >= N) or (not retired)`. The
  *own data extends* clause is dropped.

**Why both.** *Own data extends* infers listing FROM delivery: past the band floor, the only rows
L-A admits are rows that played. At depths where the floor has expired, L-A's conditioning is
therefore **selection on the outcome** — the same defect ORDER 30A named in R5 for its EVER-PLAYED
bound. L-B is free of that leak but confounds listing with pick band. The truth for the pricing
question sits between them, and this act publishes both rather than picking silently.

**Floor expiry, stated in advance** (arithmetic on the rule, not a measurement): the band floor
covers depth ≤ 4 for picks 1-20, depth ≤ 3 for 21-40, depth ≤ 2 for 41-64. At depth ≥ 5 **no** ND
pick is carried by the floor, so an L-B listed cell at depth 5+ can contain only still-active
entrants.

**THE DISAGREEMENT CHECK.** The rule is re-derived here from **Layer 1** (`ad1229ea`, byte-pinned)
and cross-checked, key by key, against `per_entrant_338_confirmation.json`'s own `yrs`/`min_tenure_338`
fields and against the live store's `_retired` / `_last_listed`. The per-entrant matrix was emitted
on store `37ced3ce`; Layer 1 is `ad1229ea`; this branch carries store `cb38ef11`. **If the sources
disagree the disagreement is reported by key, never resolved by preference.**

---

## 2. THE CONTINUOUS DEPTH CLOCK, STATED BEFORE IT IS APPLIED (T2)

**The clock.** `c = N + φ`, where `N = 2026 − entry_year` (ORDER 30A's integer depth, the engine's
own `los()`) and `φ` is the fraction of the current season elapsed.

**The fraction source, named.** `data/season_state.json` — the engine's AUTHORITATIVE DYNAMIC SEASON
STATE, the file `rl_model.py`, `_merged_recover.py` and `conditional_prior.py` were re-routed to read
at the 2026-07-21 final integration. It carries `season_year 2026`, `as_of_round 22`,
`season_total_rounds 24`, **`calendar_progress 0.92`**. This act uses `φ = calendar_progress = 0.92`
— **round 22 of 24**, i.e. two home-and-away rounds remain as of 2026-08-14. No second convention is
invented; `exposure_pace` (0.818) is the empirical durable-sample pace and is explicitly NOT the
calendar clock, so it is not used here.

**The interpolation convention.** **Log-linear in D between integer depths:**

```
D(c) = exp( (1 − φ)·ln D(N)  +  φ·ln D(N+1) )       =  D(N)^(1−φ) · D(N+1)^φ
```

Reasons, prestated: the discount is a multiplicative survival-style object (the shipped `los_decay`
is itself an exponential); log-linear interpolation is positive everywhere, monotone whenever the
integer table is monotone, and reduces to the table exactly at φ = 0 and φ = 1. Linear-in-D is
published beside it as a sensitivity so the convention is visible and not load-bearing.

**What it conflates, disclosed now.** `D(N)` is the price at the START of year N. Moving from N to
N+1 carries two things at once — a year of time-value, and the information gained by watching a
further full season pass gameless. The measurement is on integer seasons and **cannot separate them
at sub-season resolution.** Both push the same way, so the interpolated value is defensible as a
price; it is not a decomposition, and this act does not claim it is one.

**Extrapolation convention, stated in advance.** Where `D(N+1)` does not exist on a given row (the
deepest resolved depth), the law is **held flat** at the deepest resolved value. Any named row priced
under that rule is flagged as extrapolated, not quoted silently.

**The named rows' true depths** (arithmetic, not measurement): `josh-smillie` ND 2024 → `c = 2.92`;
`harry-demattia` ND 2023 → `c = 3.92`; `max-knobel` ND 2022 → `c = 4.92`.

---

## 3. THE A2 GUARD, STATED BEFORE THE BANDS ARE CUT (T3)

Anomaly A2: the landed positional entry law `nd_v0.posv` is floored at zero in the thinnest part of
its own deep tail, which the ORDER-29 artifact declares about itself
(`pvc_curve_v2.json::nd_v0.ruck_floor_63_64`). A near-zero denominator inflates any ratio taken
against it.

**GUARD G1 (primary).** Exclude — and **count** — every row whose acquisition cell satisfies

```
posv[g][p]  <  0.20 × curve[p]            (curve = the all-in ND curve on the same artifact)
```

**Why this floor.** It is relative to the object the positional law must reconcile to, so it is
scale-free and does not need a board-points threshold argued into existence. Verified on the
denominator alone before this file was written (no outcome touched): the criterion selects exactly
four acquisition cells — **RUCK 62, RUCK 63, RUCK 64, SF 64** — and the absolute alternative the
brief offered (`posv < 40` board points) selects the **identical four**. The choice between the two
stated floors is therefore not load-bearing, and this is recorded so the reader does not have to take
it on trust. ORDER 30A already dropped `posv <= 0` rows (RUCK 63/64); G1 additionally removes
RUCK 62 and SF 64.

**GUARD G2 (stricter sensitivity).** `pick >= 58 AND posv[g][p] < 0.50 × curve[p]` — the deep tail
where the positional fit is visibly collapsing, without reaching the mid-tail cells whose low ratio
is genuine shape rather than artefact.

**The re-cut.** 2-band (**1-20 vs 21-64**) and 3-band (**1-20 / 21-40 / 41-64**), at depths 2-4,
each reported with **n · mean · median · p25 · p75 · borrow%** and the count excluded by the guard.

---

## 4. THE GAMES TRANSITION, STATED BEFORE IT IS BUILT (T4)

**The estimand.** For thin-evidence entrants:

```
D(k, N) = E[ V_from_N / v0  |  cumulative games in seasons 1..N-1 ∈ k,  listing state stated ] ÷ RAW(1)
```

for `k ∈ {0} ∪ {1-2, 3-5, 6-10}` at depths 2 and 3 (deeper only if a cell reaches n ≥ 10).

**The from-depth-N decomposition.** ORDER 30A needed none: a sitter has delivered nothing before
depth N, so his whole career score IS his from-depth-N score. A player with 1-10 games has NOT, so
the pre-depth-N seasons must come out. The DV lane's own config states the licence:
`LAYER2.json::cfg.gamma_note` — *"GAMMA==1.0 makes val(r)=SCALE*r LINEAR, so delivered value is
ADDITIVE across seasons in board points and a career is a straight sum."*

```
V_from_N(i) = ( grace_a[i].obs × s_N(i)  +  grace_a[i].tail ) × DF_i(N−1)
s_N(i)      = Σ_{k ≥ N} pts_k(i)  ÷  Σ_all pts_k(i)          (per-season shares, live store)
```

The per-season legs are recomputed with the DV lane's own scorer text
(`o26b_layer2.py::season_raw` / `season_bar_group` / `w_sqrt`, already carried verbatim in
`o30a_derive.py`). **Only the SHARE is taken from the live-store recompute; the LEVEL stays the
pinned DV number.** This is deliberate: the live store is `cb38ef11` and the DV scores were built on
`d9a24282` (`MA.SCALE` differs), so a level recompute would launder store drift into the estimate
while a share is invariant to it. For a 0-game sitter `s_N = 1` exactly, so the construction
**reduces to ORDER 30A's identically** — that reduction is asserted in the harness, not assumed.

The projected tail is assigned wholly to `from-N` (every tail season is post-2026 and post-last-observed,
so none of it can belong to a season before depth N).

---

## 5. THE PREDICTIONS

### T1 — listed-conditioning

**Q1.** `D_listed(2) = D_unconditional(2)` **EXACTLY** (agreement to 1e-9), under BOTH L-A and L-B.
Every ND pick carries `min_tenure >= 2`, so the floor lists every depth-2 sitter and the depth-1
baseline alike. The owner's *"year 2 barely moves"* is, on this source, **"year 2 does not move at
all"** — and that is a statement about the reconstruction's resolution, not evidence that listing
does not matter at depth 2.

**Q2.** `D_LB(3) > D_uncond(3)`, by **at least 0.05** in absolute terms. L-B at depth 3 keeps picks
1-40 and drops the 41-64 retired non-extenders, a group I expect to be dominated by never-played
busts delivering exactly zero.

**Q3.** `D_LB(4) > D_LB(3)` is **FALSE** — the listed-conditional law stays monotone decreasing in
depth over the depths it resolves (2, 3, 4).

**Q4.** `D_LA(4) > D_LB(4)`, and the gap exceeds **0.10**. L-A's extra rows at depth 4 are, by the
rule's own construction, rows that played — outcome selection, in the direction of generosity.

**Q5.** The listed-conditional cell at depth **5** is **UNRESOLVABLE** in the fitted window: `n < 5`
under L-B (the floor carries no ND pick past depth 4, so only still-active 2004-2021 entrants who sat
four full seasons could qualify, and I expect **n = 0**). Depth 6 likewise. Reported per cell as
unresolved, never approximated.

**Q6.** Cell counts: `n_LB(3) ∈ [90, 180]` and `n_LB(4) ∈ [20, 70]`, against ORDER 30A's
unconditional 234 and 154.

**Q7.** The Layer-1 re-derivation of `listed_through` agrees with
`per_entrant_338_confirmation.json`'s own `max(yrs)` on **≥ 95 %** of the fitted ND rows, and every
disagreement is attributable to the store move `37ced3ce → cb38ef11` (a `_retired` flip or a season
row added by the #334 census), not to a port error.

### T2 — the continuous clock

**Q8.** Under the **unconditional** table, the continuous law at `c = 2.92` prices `josh-smillie`
**below 500** — i.e. the season-fraction correction alone is a **larger** move than ORDER 30A's
entire integer-depth recommendation was (919), because 0.92 of the way through year 2 puts him
essentially at the year-3 discount.

**Q9.** The two corrections **oppose each other on the named rows**: listed-conditioning raises the
price and the continuous clock lowers it. On `josh-smillie` the clock correction is the **larger** of
the two, so his continuous listed-conditional price lands **below** ORDER 30A's integer print of 919.

**Q10.** `max-knobel` at `c = 4.92` **cannot be quoted on the listed-conditional law without
extrapolation** — depth 5 is unresolved (Q5) — and is reported flagged as extrapolated under the
held-flat convention.

**Q11.** The log-linear and linear-in-D interpolation conventions differ by **less than 0.06** in D
on every named row, so the convention is disclosed but not decisive.

### T3 — bands, A2-guarded

**Q12.** G1 excludes between **5 and 25** fitted rows in total across all depths.

**Q13.** After G1 the depth-2 **3-band** pattern is **STILL NON-MONOTONE**, with the middle band
(21-40) still the lowest of the three. A2 sits only in the 41-64 band's denominator; nothing in the
guard can touch the 21-40 dip, which is the actual source of the non-monotonicity.

**Q14.** After G1 the depth-2 **2-band** contrast (1-20 vs 21-64) is **smaller than 0.20** in D and
the 1-20 cell's K-shrinkage borrow exceeds **15 %**.

**Q15.** The **verdict is NO WIREABLE BAND GRADIENT.** No band ordering survives G1 monotonically
across depths 2, 3 and 4 in the same direction.

**Q16.** G2 (the stricter guard) moves no band cell by more than **0.05** relative to G1 — the guard
choice is disclosed but not load-bearing, exactly as the floor choice is not.

### T4 — the games transition

**Q17.** The share reconstruction validates: recomputed live-store `obs` divided by the pinned DV
`grace_a.obs` has median in **[0.90, 0.97]** and an interquartile width **below 0.02** — a near-pure
level offset, which is what a store/`SCALE` move should look like and what justifies taking only the
share.

**Q18.** The 0-game reduction is **exact**: for every 0-game row `s_N = 1.0` to 1e-12 and the T4
machinery reproduces ORDER 30A's `D(2)`/`D(3)` to **1e-6**.

**Q19.** `D(k=1-2, N=2) ∈ [0.60, 0.95]` and is strictly greater than `D(0, N=2) = 0.568`.

**Q20.** The games transition at depth 2 is **monotone increasing** in k:
`D(0) < D(1-2) < D(3-5) < D(6-10)`.

**Q21.** **The measurement will NOT support a smooth curve: the 0 → 1-2 step will be the LARGEST of
the three steps** — bigger than 1-2 → 3-5 and bigger than 3-5 → 6-10. A first AFL game is the single
most informative games event in a young career (he was on the list, fit, and picked). If this holds,
the owner's ruled "no hard cliff between 0 games and 1 game" is a **design choice imposed on the
measurement**, not a shape the measurement produces, and the seat will say so in those words.

**Q22.** At depth 3 the cells thin out: `n(6-10 games by depth 3) < 30`, and at least one depth-3
games cell falls below n = 10 and must be collapsed.

**Q23.** Dispersion holds its ORDER 30A shape: `p25 = 0.000` exactly in every depth-2 games cell with
k ≤ 5, and `median / mean < 0.60` in every one of them.

### Reproduction

**Q24.** This act reproduces ORDER 30A's headline unconditional row to **1e-6**:
`RAW(1) = 1.0286`, `D = 0.568 / 0.214 / 0.105 / 0.074`. Any drift is a defect in this act, not a
correction to that one, and is reported as such.

### The recommendation I expect to make

**Q25.** I expect to recommend the **listed-conditional L-B row on a continuous log-linear clock,
position-blind and band-blind**, with L-A published as the generous bound and the unconditional row
retained as the harsh bound — and to recommend that the games transition be **wired from the
measured points at depth 2 only**, with the 0→1 boundary handled by an owner-ruled shape rather than
by an extrapolated fit, because I expect the measurement to show a step there (Q21).

---

## 6. WHAT WOULD FALSIFY THE ACT

If the listed-through reconstruction cannot resolve listing at a depth, the seat reports that cell as
**UNRESOLVED** with its reason, and does not publish a listed-conditional number for it. If a games
cell falls below n = 10 it is collapsed and the collapse is disclosed. If the L-A and L-B readings
disagree by more than 0.15 at a depth, the seat publishes the band as a **bound**, not a law, and says
the evidence does not support a single number there.

---

*Filed 2026-08-14, before `o30a2_recut.py` existed in runnable form and before any cell of any of the
four tasks was counted. The denominator-only facts recorded in §1 (13/3 explicit `_last_listed` rows)
and §3 (the four A2 cells, and the agreement of the two stated floors) were verified before filing and
are stated here so they cannot be mistaken for findings.*
