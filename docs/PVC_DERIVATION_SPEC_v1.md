# PVC DERIVATION SPEC v1 — the outcome-based pick-value curve: methodology, execution plan, decision register

**SEAT: FABLE · DESIGN ONLY — this document wires NOTHING. Its product is executed later, job-by-job, on OPUS seats.**

> ⚠️ **HEADER STAMP — v1 · pre-v2.5 · DO NOT RUN P0–P8 AS-IS.** Every number in this spec was read
> off the **OLD v2.4 board** (store `644d1254`, canonical `8aed420a`). The board has since been
> re-baked to **v2.5** (store `e1b4d8bf`, canonical `efea88e5`, tag `baked-v2.5-2026-07-05`). This
> re-stamp (2026-07-06, housekeeping only — no fit, no board change) marks the contaminated numbers
> inline **[CONTAMINATED → …]** and records the v2.5 equivalent where one exists, or
> **"re-derive at fit"** where none does. See the **RE-STAMP LOG** at the end. Re-validate every
> quoted number at fit time; do not carry any `[CONTAMINATED]` value into execution unchanged.

**STATE STAMP (three-column reporting rule R6):**
`CONTROL = canonical 8aed420a · store 644d1254 · band 34faa865` ·
`CANDIDATE LINE = v2.4 engine 7c199a1f (PR #18, stacked on v2.3 f3e537ba / PR #17 on v2.2 af1fc6aa / PR #16), under combined scoped D13+D14 cold audit at spec time` ·
`THIS SPEC = docs/PVC_DERIVATION_SPEC_v1.md on branch claude/pvc-derivation-spec-17l4ly (no engine, board, or data change).`

**[RE-STAMP → v2.5, 2026-07-06]** `CONTROL = canonical 8aed420a→efea88e5 · store 644d1254→e1b4d8bf ·
band 34faa865 (UNCHANGED)` · `CANDIDATE LINE = the v2.4/v2.3/v2.2 engines 7c199a1f / f3e537ba /
af1fc6aa were BAKED into the v2.5 canonical efea88e5 (owner-authorised 2026-07-05); there is no
separate live candidate — efea88e5 is now CONTROL.` This re-stamp branch touches ONLY this spec file;
the v2.5 board/store is asserted untouched (store md5 still `e1b4d8bf`).

**Design target:** the spec designs against the **v2.4-shape world** (fitted V0 board curve · RUC prior cap 1.73 **[CONTAMINATED → v2.5 baked default 1.4]** · concave penalty ramp τ^1.5 · retention surface R_SURF · KPP floor O1) applied to the **post-bake corrected history**. Every assumption the pending D13+D14 audit could still move is marked **[AUDIT-EXPOSED]** and collected in §5.

**Read basis:** START_HERE.md · docs/KICKOFF_PROMPT.md · SHIP_GATES.md (frozen a55921f6-lineage, D14 amendments) · docs/CHANGELOG.md through the D14 entry · docs/process/LUKE_RULINGS_LEDGER.md (R1–R13) · docs/process/OWNER_OVERRIDES.md (O1) · BOARD_LAYERS_OBITUARY.md (E1–E5) · docs/AUDIT_COLD_v21_c8051893.md · d10_ask1_relic_inventory / d10_ask2_derivation · d13_ask1_ruck_cap / d13_ask3_retention · d14_ask1_curve_params · PR #16/#17/#18 bodies · supervisor handovers rev53/rev93 · PROVENANCE_2026-07-01.md · the pre-D10 rationale docs (nogames basis/override, step4 book, directive-v3 lowgames, cont.27 PVC history) · engine code at v2.4 (`_merged_recover.py`, `rl_model.py`, `conditional_prior.py`) · store `rl_model_data.json` (644d1254 **[CONTAMINATED → v2.5 store e1b4d8bf; all census counts below re-cut at P1/P2]**, read-only profiling this session).

**IN PLAIN TERMS (top):** today, when Luke trades pick 5, the engine prices that pick off a curve built last month from a risk-formula over old careers, glued to the old board's scale in two places, blind to position and to whether the pick is an 18-year-old or a 24-year-old — while every PLAYER on the board is now priced by a newer, smarter machine. This document is the recipe for rebuilding the pick curve the same way the player side was rebuilt: measure what every recorded pick since 2003 actually turned into (busts counted as zero, positions separated, mature-age separated), smooth it properly, and make the handful of judgment calls — like "is a pick worth what the kid is worth in year one, or what he might become by year four?" — Luke's explicit, written decisions instead of buried constants.

---

## §0 — VOCABULARY AND SCOPE

| term | meaning (engine's own usage) |
|---|---|
| **PVC / draftval** | the per-pick-number price curve. Today = `MA.PVC` from `build_pvc_v34()` [rl_model.py:531, v2.4]; `draftval(p)=PVC[effpk(p)]`. Position-blind, draft-age-blind. "Old PVC" in D10-era docs = this same object. |
| **V0** | a player's live zero-evidence start value. Raw form = `raw_ev(p, draft-yr) × iso` (band prior, pick+position+age-aware). On the v2.4 BOARD PATH overwritten by the fitted curve **V0\*(position × draft-age × log recorded pick)** [D14, R12]. |
| **SCAR** | the board currency: `val(r)=SCALE·r^γ`, γ=`RL_GAMMA`=0.85. **γ is a concavity (diminishing-returns) exponent on realised value, NOT a time discount** [rl_model.py:266,436-439]. Pick 1 = 3000 by the locked `RL_PICK1` anchor. |
| **price6 / WQ6** | the engine's locked distribution-aware pricing convention: quantiles [q10,q30,q50,q70,q90,q97] weighted [0.18×5, 0.10]. The realisation ruler used by the D10/D13 derivations. |
| **decided cohort** | a draft year old enough that its careers are (essentially) complete. Realised values stabilise at draft ≤2017/2018 [cont.27 censoring-boundary finding, CHANGELOG 2026-06-29]. |
| **the two staged pick anchors** | the two scale-anchoring stages inside `build_pvc_v34()`: (1) the **legacy top-band anchor** `SCALE_PVC = legacy_top/new_top` (pools picks 1–3 against the ORIGINAL realised curve `build_pvc(ALPHA)`) [rl_model.py:555-559]; (2) the **pick-1 anchor** `BOARD_FACTOR = RL_PICK1/PVC[1]` (=3000), which co-rescales `SCALE` (players) and `PVC` (picks) [rl_model.py:565-570]. Distinct from A13/A14, the two PVC-staged pick GATES (SHIP_GATES, PENDING until the curve exists). |

**Scope:** this spec covers the derivation of the outcome-based PVC and everything that re-bases when it lands (§7 of handover rev93: "A13/A14 activate · draftval re-bases · 1.19× revisit · B5 generating-rule re-derivation · MSD/SSP pick-equivalents — price+floor are ONE shared object"). It does NOT cover distribution pricing (the q90–97 upside successor to the floor — a later stage that consumes the same fitted object, §2a.4) or the LTI workstream.

---

## §1 — ASK 1: CURRENT-STATE DIAGNOSIS — where every pricing-curve assumption lives

Summary table first; provenance and retirement analysis per row below. "Breaks if retired naively" = the concrete damage from deleting the stopgap without its principled replacement in place.

| # | assumption | where it lives [state] | status |
|---|---|---|---|
| 1 | PVC v3.4 itself (measure + tiered CE α 0.6→0.8 + loclin/isotonic) | `rl_model.py:516-562` [v2.4 = CONTROL here] | LIVE — the object this spec replaces |
| 2 | legacy top-band anchor `SCALE_PVC` | `rl_model.py:555-559` | LIVE — sets the pick-vs-player exchange rate |
| 3 | pick-1 = 3000 anchor `BOARD_FACTOR` | `rl_model.py:565-570`, `RL_PICK1` | LIVE — Luke-locked "permanent" [cont.11] |
| 4 | ~16% anchor over-discount flag | carried supervisor-side; repo traces §1.2 | UNPINNED — provenance resolved below |
| 5 | 1.19× first-year (sit-out) multiplier | NOWHERE in live code — PARKED [PROVENANCE_2026-07-01 §c]; its target deleted at D10 (obituary E2) | DE-FACTO RETIRED — formal strike rides this spec's plan |
| 6 | penalty ramp shape τ^1.5 | `_merged_recover.py:461` [v2.4] | LIVE — Luke-signed law R7, with a recorded PVC-era revisit hook |
| 7 | RUC prior cap 1.73 **[CONTAMINATED → v2.5 baked default 1.4]** | `_merged_recover.py:305-317` [v2.4] → v2.5 at `_merged_recover.py:322-324` (`RUC_PRIOR_CAP`, dial `RL_RUC_PRIOR_CAP` name UNCHANGED) | LIVE stopgap [AUDIT-EXPOSED] — R9; dial is Luke's; **v2.5 baked 1.73→1.4** |
| 8 | C1/C2 baseline gates | SHIP_GATES §C — harness NOT built | PENDING — "if either fails: stop and re-scope before the PVC" |
| 9 | MSD/SSP pick-equivalents + 2 credit phantoms | `rl_model.py:675-727` (PICKEQ), `rl_model.py:11-20` (MSD_Y1_MULT 1.5), phantoms in store | LIVE — PICKEQ inverts the OLD PVC |
| 10 | B5 floor schedule + generating rule; A5 SCAR floors | `_merged_recover.py` floor block [v2.4, V0-based per R8]; SHIP_GATES B5/A5 re-base notes | LIVE — re-base coupled to the PVC by frozen gate text |
| 11 | D14 V0\* board curve | `_merged_recover.py:358-434` [v2.4] [AUDIT-EXPOSED] | LIVE — the PVC's conditioning twin, fitted on PRIORS not outcomes |

### 1.1 The PVC v3.4 and its two staged anchors

**What it does.** `build_pvc_v34()` [rl_model.py:531; built 2026-06-20, CHANGELOG cont.9/10]: measures per-pick realised `posval(best2+capt−REPL)` with busts→0, applies a **tiered certainty-equivalent** α=0.6 (top picks)→0.8 (tail) — a designed risk haircut, not the mean — smooths (varying-bandwidth local-linear, parametric power-decay top blended below ~pick 12, light isotonic), then stages two anchors: `SCALE_PVC` chains the level to the ORIGINAL (V1-era) curve's pooled picks-1–3 band, and `BOARD_FACTOR` rescales players AND picks together so PVC[1]=3000. It is **position-blind and draft-age-blind** — one curve for everyone.

**Why it is a stopgap.** (i) Position-blind while the whole v2.x player side is position-aware — the D10 relic inventory measured the live consequences (Dean V0=0.55×PVC below, Robey 1.17× above, RUC 2.5× hot) [d10_ask1, v2.1-verified]. (ii) Draft-age-blind — mature-age picks (Tim Kelly pk24 age 23) priced as 18-year-olds. (iii) The tiered CE α is a hand-set risk appetite (0.6→0.8) with a recorded rationale but no owner ruling in the R-ledger. (iv) The legacy top-band anchor chains today's pick-vs-player exchange rate to the pre-2026 board's scale — the one thing A13/A14 are supposed to *measure* is currently *assumed*. (v) Its measure (best2+capt career peak) prices a pick at career-peak expectation with no time treatment (§2a).

**Principled replacement.** The §2 derivation: a per-(position × draft-age) distributional outcome object over log recorded pick, priced in board currency directly (no cross-anchor staging needed — realised career value is already in `val()` units), with pick-1=3000 kept as the single outer currency rescale.

**Breaks if retired naively.** `draftval` consumers at v2.4: the B5 floor *generating rule* (schedule fractions ≈0.9×smoothed clean p5 of dv — the schedule was signed on the dv ruler), the RUC cap's denominator (`cap·PVC`), `effpk`→PICKEQ (every MSD/SSP/IRE/UNR/PDA/PDN/PDS player's effective pick feeds the band's log-pick feature — an ENGINE VALUE channel, not display), Measure-2 pick-sum ruler, A5's absolute SCAR floors (gate text: "RE-BASE if the PVC re-levels the currency"), display prints. Deleting or re-levelling the curve without re-pointing these in order moves player values through the PICKEQ/effpk channel and silently re-bases two Luke-signed schedules. Ordering is §3.

### 1.2 The ~16% anchor over-discount flag — provenance resolution (the supervisor holds the flag; the repo does not pin a derivation)

**What the repo actually contains** (exhaustive trace, this session):
- The phrase appears exactly twice, both 2026-07-03 DIAG-B rev3 (PR #12 lineage): *"the sit-out anchor's known ~16% over-discount (pre-registered book caveat)"* [d8_2025_shortfall_verdict.md:83; diagB_rev3_notes.md:6]. Both use it as an ATTRIBUTION RESIDUAL in the 2025-cohort shortfall decomposition — neither derives it.
- **Best-evidence origin:** `Yr1/mean(Yr2–7) = 0.84` **[CONTAMINATED — no v2.5 equivalent; re-derive at fit (P8)]** on the M1v7 walk-forward book [BUILD_report_2026-07-01_directive-v3-lowgames.md:13, state = M1v7 prototype on head 8aed420a, pre-v2.5] — the year-1 cohort total sits ~16% below the year-2–7 plateau, attributed to the sit-out anchor's harshness. **1/0.84 ≈ 1.19** — the parked "1.19× uniform sit-out lift" (§1.3) is the same number seen from the other side. The lift was sized to close exactly this gap ("bring the anchored sat-out Yr1 level up to the ~217,573 empirical target" **[CONTAMINATED — pre-D10/pre-v2.5 book number; no pinned derivation and no v2.5 equivalent; re-measure at the post-bake head, P8]** [PROVENANCE_2026-07-01 §c]).
- Secondary candidate (same magnitude, different object): the calendar-year re-index of the book's Yr1 anchor moved the pool-wide anchor sum +16% (1,237k→1,436k) [SESSION_SUMMARY_2026-06-30_step4_book §6] — but that was a FIX APPLIED, not a live caveat.
- **Nothing associates ~16% with the PVC pick anchors themselves.** Every repo use attaches it to the *sit-out anchor* — whose carrier (`SITOUT_RETAIN×draftval`) was **deleted at D10** (obituary E2) and re-derived twice since (D10 R_SIT → D13 R_SURF).

**Resolution offered (see DECISION-NEEDED D2):** the flag is a **book-level symptom of the pre-D10 world** — the Yr1 cohort priced ~16% under its own plateau, with the flat sit-out anchor the argued cause. It has no pinned derivation, and its mechanism has since been deleted and re-derived. The correct disposition is not to carry it into the new derivation as a constant but to **re-measure the symptom at the post-bake head** (job P8): if the v2.x games-ramp/retention work closed the gap, the flag retires; any residual becomes a named validation target for the new PVC. If the supervisor's flag refers to something else, that referent must be stated — the repo cannot produce it.

### 1.3 The 1.19× first-year multiplier

**What it does: nothing.** It was proposed as a uniform lift on `SITOUT_RETAIN` to close the §1.2 gap; PARKED with a recorded breach (uniform 1.19× pushes RUC yr1-2 retention to 0.85×1.19=1.01 > 1.0) [PROVENANCE_2026-07-01 §c]; then its target table was deleted at D10 [obituary E2; UNRESOLVED w9 "OVERTAKEN"]. The only literal `1.19` in live code is unrelated: `_SCALE['MID']=1.19`, the STEP3-B per-position pole re-level [\_merged_recover.py:124] — **derived, not a stopgap, NOT in this spec's retirement scope** (do not confuse them; an Opus job grepping "1.19" will find the wrong one first).

**Retirement path.** Formal, not mechanical: (i) strike UNRESOLVED w9 with a pointer to this spec; (ii) register the underlying symptom (§1.2) as validation diagnostic V-D6 (§2e); (iii) the new PVC + V0 re-level answers the year-1-level question directly — no uniform multiplier concept survives. **Breaks if retired naively:** nothing (it is unwired) — the only risk is *conceptual*: retiring the multiplier without re-measuring the symptom would leave "is year 1 still under-priced?" unanswered. P8 closes that.

### 1.4 The games-ramp penalty shape t^1.5

**What it does.** Within-season accrual of the sit-out penalty: `tau = completed_seasons + fe^1.5` [\_merged_recover.py:461, v2.4] — penalty fraction (season progress)^1.5, Luke-signed OPTION A (R7, verbatim in ledger), penalty path only; the reward-side G_ADQ gate deliberately untouched. R7 records the hook: *"a PVC-era derivation may replace the t^1.5 SHAPE from partial-season snapshots (open, not a block)."*

**What a principled replacement requires — and why history cannot supply it.** The store is **season-aggregate** (per-season `{year, games, avg}` only; no round-by-round) [store 644d1254; confirmed C.8, BUILD_report directive-v3: "within-season penalty-proration shape NOT derivable — season-aggregate data"]. A derived within-season shape needs partial-season snapshots, which exist only for the current season (R14/24) plus whatever pinned matrices future sessions archive. **Consequence:** the t^1.5 revisit is NOT a historical-derivation job at all. Options (DECISION-NEEDED D3): (a) keep t^1.5 as owner law indefinitely (recommended — it is signed, bounded, and behaved green through B6 at v2.2–v2.4); (b) commit to archiving in-season board snapshots from 2026 onward so a shape derivation becomes possible in 2–3 seasons. **Breaks if retired naively:** replacing the shape with anything un-derived re-opens the exact "invented constant" class D12 closed; and the shape interacts with B6 continuity at the graduation bar — any change must re-prove B6's three clauses.

### 1.5 The RUC prior cap 1.73 **[CONTAMINATED → v2.5 baked default 1.4]** [AUDIT-EXPOSED]

**[RE-STAMP → v2.5]** The `1.73` throughout this section is the pre-v2.5 dial value. At the v2.5 bake
(2026-07-04) the owner moved the ruck-cap dial to **`RUC_PRIOR_CAP=1.4`** (baked default,
`_merged_recover.py:322`; env override `RL_RUC_PRIOR_CAP` preserved). The class-median mechanism
described below is unchanged; the **level** (1.73, the Emmett ladder rungs, the "1.73 default" price
1054) is contaminated and re-cuts at the current head — the design (§2d.5/P6 replaces the cap with an
outcome-based ruck curve) stands regardless of the dial's numeric value.

**What it does.** `RL_RUC_PRIOR_CAP=1.73` caps the ruck band prior at cap×PVC at the raw_ev/band level (pure prior capped unconditionally; production leg capped only in the prior-dominated regime; proven rucks byte-exact) [\_merged_recover.py:305-317, v2.3/v2.4; R9]. 1.73 = the measured ND-ruck class **median** V0/PVC (1.7274) — i.e., the cap says "no ruck's prior may run hotter than the class's typical hotness," which contains the tail (Emmett 2.52×→1.73×) but **ratifies the class-median hotness itself**. Luke's own eyeball says the median is still hot: his stated Emmett range 650–800 sits at rungs ~1.1–1.3 (670/792), vs 1054 at the 1.73 default [d13_ask1 ladder, v2.3].

**Why it is a stopgap, precisely.** The denominator is the position-blind old PVC — the ruck "hotness ratio" conflates (i) genuine ruck scarcity/late-development priced by the band and (ii) the old PVC's failure to price rucks at all. A cap on a ratio of two wrong things is a tourniquet. The principled replacement is the **full ruck V0/PVC derivation** (§2d.5): an outcome-based ruck pick-value level (busts in, pooled shape × ruck level per the standing thin-RUC rule) that replaces both the denominator and the cap.

**Interaction with the owner's rung choice at the bake.** If Luke moves the dial (e.g., to 1.3) at the bake board view, that rung becomes the ruck prior level the league trades on — and the derived ruck curve, when it lands, will disagree with it by construction (it re-levels from outcomes, not from a ratio rung). Pre-register NOW (D4): **the derived ruck curve supersedes whatever rung is in force**, with Luke's Emmett read (650–800) and the A6 gate (early-career RUC median ≤ pick-matched MID median) as its acceptance anchors — so the rung choice is an interim board preference, never a competing derivation. **Breaks if retired naively:** dropping the cap before the derivation re-opens h-ruc-startvalue-hot (Emmett→2.52× hot, RUC floor-saves polluted); the cap also feeds the fitted V0\* curve (cap applies FIRST, then the curve fits capped values [D14 declared order]) — retiring it re-shapes the RUC V0\* cell silently.

### 1.6 C1/C2 baselines

**What they are.** Not engine constants — the two SECTION C acceptance gates [SHIP_GATES]: C1 = ship head beats a NAIVE BASELINE (last-2-season avg + simple age curve + position multipliers) on the walk-forward book headline metrics; C2 = ship head beats the ORIGINAL V1 pick model on the same metrics. Frozen instruction: *"If either fails: stop and re-scope before the PVC."* Neither harness exists yet [d4_instrument_audit: PENDING].

**Slot in this design.** They are the **gate-zero** of the execution plan (§3 P0): the baselines must be built and run BEFORE PVC work begins, because (i) the frozen suite says so, and (ii) C2's "original V1 pick model" is itself the natural benchmark for the new PVC (the new curve should beat the V1 curve at predicting realised pick outcomes out-of-sample — a direct, pre-registerable test). **Breaks if skipped:** the PVC would ship against an unmeasured null; a later C-failure would force re-scoping after the currency re-levelled — the expensive order.

### 1.7 MSD/SSP pick-equivalents + the 2 credit phantoms

**What they do.** Pickless entry mechanisms ({SSP, MSD, IRE, UNR, PDA, PDN, PDS}, 391 records [store 644d1254]) get an effective pick via `PICKEQ`: pool each pathway's realised value, invert the OLD PVC at that value (`_pick_equiv`) [rl_model.py:675-727]. `effpk` then feeds (a) `draftval` and (b) the band's log-pick FEATURE — so PICKEQ is an engine-value channel. MSD standardisation: debut-year games ×1.5 (`MSD_Y1_MULT`, Luke-set 2026-06-20) + `MSD_S1_MULT=2.0` in P_estab. The 2 credit phantoms (Mark Keane IRE-credit, Lachlan McAndrew MSD-credit) deliberately double-count those players to feed the IRE/MSD pathway pools [PHANTOMS.md; Luke's call, cont.4] — plus 2 synthetic calibration bust phantoms; all 4 are excluded from the PVC pool and from MSD games-scaling by existing code.

**Slot in this design.** PICKEQ is **derived FROM the PVC**, so it re-derives mechanically when the curve re-levels (job P7): same pooling, invert the NEW curve — with one new decision: the new PVC is (position × draft-age)-conditioned, and a pathway pool has a position/age mix, so the inversion must state its cell convention (recommended: invert on the pathway's realised position-age mix, weighted; the alternative — a mix-blind marginal curve — reintroduces position-blindness exactly where the pathways live). Phantoms: keep, keep-excluded, re-declare (they are pool-feeders, not curve points). **Breaks if retired naively:** deleting phantoms un-anchors the IRE/MSD pools (their thin pools were deliberately credited); swapping the PVC without re-deriving PICKEQ moves every pathway player's band feature against a stale inversion.

### 1.8 The B5 floor and A5 SCAR floors — "price + floor are ONE shared object"

The B5 schedule (.45/.35/.28/.21/.13/.09 + .05 tail; V0-denominated since R8) is Luke-signed; its **generating rule** is frozen in the gate text: *"floor ≈ 0.9 × smoothed clean p5 (ND-only) — RE-BASE at the PVC stage when the draftval denominator re-levels, by re-running the generating rule."* A5's absolute floors (Ginnivan 1600 / Bowey 2100 / Blakey 2600) carry the sibling note ("RE-BASE if the PVC re-levels the currency"). The §2a design makes the coupling structural: the fitted object is distributional, so the floor's p5 and the price's WQ6 aggregate are two functionals of ONE fitted surface — re-running the generating rule is reading a different quantile off the same object, not a second derivation. **Breaks if ignored:** a re-levelled currency under unchanged absolute floors silently changes who the floor catches (the D12 churn — 13 leave/7 join — was exactly this class of effect, there deliberate).

### 1.9 The D14 V0\* board curve — the PVC's conditioning twin [AUDIT-EXPOSED]

V0\*(position × draft-age × log recorded pick) [D14, R12] has **identical conditioning to the new PVC** — but it is fitted on the current roster's (capped) **prior** V0s: it smooths what the band model already believes, it does not measure outcomes. The new PVC measures outcomes on the same axes. Where they disagree beyond noise, the outcome curve is the calibration truth for start values (that is what "outcome-based" means), and the natural end-state is **V0\* levels := reconciled to the outcome PVC** on the board path (§2d.6, DECISION-NEEDED D6). **Breaks if done naively:** V0 is the denominator of the retention surface (R_SURF ratios r=O/V0) and the base of the B5 floor — re-levelling V0 without re-deriving R_SURF and re-running the floor generating rule corrupts both (sequencing, §3 P7).

**IN PLAIN TERMS (§1):** the pick prices Luke trades on today come from one position-blind curve glued to the old board's scale; the "fixes" bolted around it — the ruck cap, the parked 1.19×, the floor schedule, the pathway pick-equivalents — are all patches over the same missing thing: nobody has yet measured, position by position and age by age, what each draft pick actually turns into. Everything in this table either gets replaced by that measurement or gets re-based on it, in a set order, so nothing silently moves twice.

---

## §2 — ASK 2: THE DERIVATION METHODOLOGY

### 2a — ESTIMAND: what the principled PVC is

**2a.1 The fitted object (the central deliverable).** For each cell c = (at-draft position × draft-age tier) and log recorded pick k, fit the **conditional realised-outcome distribution**:

> **F(v | k, c)** = the distribution of realised career value v for entries at pick k in cell c, with **busts and never-played entries in-sample at their realised value (0 / delist scrap)** — represented as smoothed quantile curves {q5, q10, q30, q50, q70, q90, q97} over log-pick plus an establishment-probability curve P_est(k, c), per the two-part structure of §2b.

Everything downstream is a functional of this ONE object:
- **PVC price** = the WQ6-weighted aggregate of F (the engine's own locked distribution-pricing convention — weights [0.18×5, 0.10] over [q10,q30,q50,q70,q90,q97]), with the CE-α ladder (0.5–1.0) printed as a DIAGNOSTIC dial beside it (risk appetite is Luke's; the v3.4 tiered α becomes a visible choice, not a buried constant — DECISION-NEEDED D8);
- **B5 floor generating rule** = 0.9 × smoothed clean p5 read off the same F (§1.8);
- **distribution pricing** (the later stage) = the q90–q97 tail of the same F;
- **PICKEQ** = inversion of the price functional (§1.7).

**2a.2 The value definition v (what "outcome" means).** v = the entry's realised career value in board currency, computed from RAW scoring histories (store 644d1254 post-bake), NEVER from engine `ev()` (leakage rule, §2e.4):

- **Per-season value ruler:** era-adjusted level (avg/REPL by season-year, the engine's existing era adjustment) priced through the locked **price6/WQ6** map — the same ruler the D10/D13 derivations locked and the cold audit reproduced to 3 decimals [AUDIT_COLD_v21 A2]. A reconciliation step (P2) confirms rank-agreement with the v3.4 measure `val(posval(best2+capt−REPL))` on decided cohorts; material disagreement is an abort-to-supervisor, not a silent pick.
- **The trajectory, not just the peak:** compute the entry's realised value **trajectory** T(d | entry) at each career depth d = 1..10 (value at depth d = price of the best era-adjusted qualifying level achieved in a trailing window at that depth; busts/unplayed = 0; delisted = 0 from delist year). The v3.4 measure (career-peak posval) is the d→career-max special case.

**2a.3 The time-aggregation — the sharpest owner fork in this spec.** A pick converts into an asset whose expected trajectory RISES to a peak in years 4–6 (the B1 law: cross-cohort average yr1=100 → peak ~130–160 [book, two views]). So "expected career value" is ill-posed until a time convention is chosen:

- **(E-spot)** PVC[k,c] = E[asset value at end of year 1] — prices the pick at what the rookie will be worth on the next board. Historically cohort Yr1 ≈ 73–95% of pick sums [d8_2025_shortfall pick-mix table] — the lowest candidate.
- **(E-peak)** PVC[k,c] = E[career-peak asset value] — what v3.4 approximates. Highest; implies a pick is worth its player's year-4-6 value today, i.e. buying picks would dominate buying equivalent current players.
- **(E-disc, recommended)** PVC[k,c] = **max over d of δ^d · E-trajectory(d | k, c)** — the discounted value of the appreciating asset, with δ an explicit owner time-preference dial. δ=1 collapses to E-peak; δ→0 to E-spot. **γ=0.85 is NOT δ** — γ is value concavity and stays inside the ruler; δ is time preference and does not exist in the engine today. Default: fit δ so the pre-registered pick-vs-player gates (A13: pick 1 vs Wardlaw AND Ashcroft; A14: pick ~8 vs Rivers/Zach Reid/Burgoyne; ±20% line-ball) land mid-band, then present δ and its named-player consequences for Luke's signature (DECISION-NEEDED **D1** — this is football semantics: "what is a pick worth: the kid's year-one value, his ceiling-year value, or something in between that you choose?"). The E-trajectory(d) curves are fitted from the same harvest either way, so the fork costs no re-derivation — only the aggregation changes.

**2a.4 Currency and anchoring.** The derivation outputs are ALREADY in board SCAR units (the ruler prices through val()/price6) — **the legacy top-band anchor (SCALE_PVC staging) is retired**: no chaining of the new curve to the pre-2026 board's top band (DECISION-NEEDED D7; recommendation: retire — it is the one place the "over-discount" class of scale error can hide, §1.2). The **pick-1=3000 anchor stays** (Luke-locked; it co-rescales players and picks so it is relativity-neutral by construction — DECISION-NEEDED D9, recommendation: keep).

**2a.5 Censored careers enter without bias** — via the window design of §2b.3, never by silent inclusion: the primary fit uses decided cohorts only; censored cohorts enter only through the explicitly-modelled extension (P4) and as out-of-sample validation targets.

### 2b — SURVIVORSHIP & SELECTION: the traps, named, each with its estimator strategy

| trap | mechanism | strategy |
|---|---|---|
| **delisted busts leaving the sample** | a delisted player's record simply ends; naive "value of players seen at depth d" forgets him | busts are IN-SAMPLE at 0 (v3.4's rule, kept): the harvest emits every ND/RD entry with a realised trajectory, never-played = 0 at every depth, delisted = 0 from delist year. The two-part estimator (below) makes the zero-mass explicit: **P_est(k,c)** (probability of ever establishing, ≥6-game qualifying season at era-adjusted level) × **F(v \| established)** — so the deep-pick price falls because P_est falls, measured, not because anyone hand-set a bust floor |
| **survivors flattening deep-pick tails** (the owner's live D14-era concern) | value-given-played flattens with pick because deep survivors are positively selected; a mean over survivors overprices the tail | the two-part split isolates it: P_est carries the pick gradient the survivor-conditional value hides (cont.27 U8/U9 measured exactly this: never-qualified 0% at picks 1–10 vs ~40–55% deep; realised gradient 1.7–1.9× pk20/40 once busts fold in). Additional guard: the **hit-concentration diagnostic** — per deep-pick band, print the share of band value owned by the top-5 realisations [decided census, this session: 41+ band, ~200 decided entries]; if a fitted tail cell is >50% owned by <5 players, the cell is DECLARED concentration-fragile and the CE ladder (2a.1) is the owner's honest lever, not the mean |
| **right-censoring (active careers)** | cohorts 2013+ are 21–71/cohort still active [store census this session]; including them naively biases values down (careers unfinished), excluding them wastes the most era-relevant data | three-window design: **primary fit = decided cohorts 2006–2018** **[SUPERSEDED → primary window moved 2006→2004; this change is DONE — the primary fit is now 2004-based. The `2006`/`2003–2005 left-censored` framing below is the pre-change text, retained for provenance; read the primary window as 2004–2018 throughout (§2c.2, §2/§5 plain-terms echoes are pre-change).]** (scoring rows begin 2005 [store]; 2003–2005 drafts are left-censored — see era row; realised values stabilise at ≤2017/2018 [cont.27]); **extension = 2019–2022** entering ONLY via censoring-adjusted projection: per (cell, current depth, current status) multiply observed partial trajectories by completion factors measured from decided cohorts' realised trajectories (realised-to-realised, never engine values — no circularity); **2023+ = validation-only** (out-of-sample targets for the curve's Yr1/Yr2 predictions). Leave-one-cohort-out stability across the primary window is a pre-registered diagnostic (V-D3) |
| **era effects** | (i) 2003–2005: scoring history starts 2005 → left-censored early careers; (ii) pre-2015 father/son were fixed-slot picks, post-2015 bid-priced — recorded pick ≠ market pedigree pre-2015 (the store already repacks the worst: Hawkins #41→#2 et al [cont.15]); (iii) GC/GWS concession intake (2009–2011) distorts pick meaning (37 already removed [cont.15]); (iv) list-size/draft-length drift: deep picks (66+) are mostly old-era observations; (v) COVID 2020: ~17-round season deflates games-based establishment bars; (vi) scoring-basis drift across 20 years | (i) exclude 2003–2005 from the primary window (matches the book's REFONLY-2003 precedent); (ii) P1 hygiene job enumerates pre-2015 F/S + academy entries and flags `_pvc_exclude` (the store's existing exclusion mechanism) unless Luke supplies bid-equivalents; (iii) verify the concession removals carried into the current store; (iv) fit on log-pick with eff-n-grown bandwidth (thin modern deep-tail borrows strength smoothly) + print an era-split diagnostic (2006–2011 vs 2012–2018 curves) — DIAGNOSTIC ONLY, never two fitted eras (wide-bin rule); (v) 2020 season games prorated ×22/17 in every games-bar the harvest applies (pre-registered constant); (vi) the era-adjusted level ruler (avg/REPL by year) is the existing, audit-reproduced answer |
| **re-drafted / mature-age re-entry double-counting** | a delisted-then-redrafted player (RD/MSD/SSP re-entries; Will Hayes carries a known dup record [cont.15 OPEN]) would otherwise contribute his whole career to BOTH entries | **entry-windowing rule:** each recorded entry is its own observation; its realisation window runs from its own draft year to its own next delist (or career end). The first entry's outcome INCLUDES the fact of later re-drafting only through what was realised inside its own window (delist = 0 thereafter — the pick bought that tenure, not the comeback). Draft-age conditioning (§2c) prices the re-entry demographics honestly. Phantoms (4) excluded; Max King/Maxwell King + two Uwlands + 8 known collisions keyed by pick/cohort/id (standing name guard) |
| **missing draft-age** | 175/1572 ND records lack `_by` [store census this session]; a handful carry placeholder _by=2000 [START_HERE landmine] | adopt the engine's `age()` at-draft estimator (recorded reliable [archive HANDOVER: "Model age() is reliable"]) for the age FEATURE; P1 prints the disagreement set (estimator vs _by where both exist) and the placeholder set for Luke's data pass; fit proceeds on estimator-age with the missing-_by flag carried as a diagnostic split |
| **at-draft position integrity** | the store's `pos` mixes eras: 81 legacy generic 'DEF' records; position-switchers (Maric drafted GFWD→now MID); 548 historical positions were owner-backfilled in one 2026-06-20 pass | the conditioning variable is **at-draft position** (what a trader knows when pricing the pick). P1 verifies a usable at-draft position field: maps legacy 'DEF' (rule proposed: KEY/GEN split by the same height/role logic Luke used in the backfill — his sign-off on the 81), confirms switchers carry their DRAFT position not `_pos_now`, and reports the residue. The owner-backfilled positions are accepted as ground truth (they were Luke's own assignments) |

### 2c — CONDITIONING & SMOOTHING

**2c.1 The binding statistics rule (standing, KICKOFF/D5):** measure at the finest resolution the sample supports; smooth on the continuous axis (kernel/local regression over **log recorded pick**, adaptive Gaussian bandwidth grown until local **eff-n ≥ 35**); **wide bins are BANNED as derivation and allowed only as diagnostics**; pooling is DECLARED, never silent; isotonic projections stated with their authority (data vs owner-law).

**2c.2 The cell census and the expected pooling tree** [decided ND 2006–2018 **[CONTAMINATED — read window as 2004–2018 per §2b.3 supersession; counts re-cut at P2 on store e1b4d8bf]** ≈ 1,130 entries; counts below are the ≤2018 census profiled this session, store 644d1254 **[→ v2.5 e1b4d8bf]** — P2 re-cuts them on the exact primary window]:

| cell | decided n (age≤18) | expected resolution |
|---|---|---|
| MID | ~270 | own curve, comfortably (D14's roster fit reached eff-n 35 with n=427 unmaxed) |
| GEN_FWD | ~155 | own curve |
| KEY_FWD | ~104 | own curve, bandwidth will grow |
| GEN_DEF / KEY_DEF | ~97 / ~96 | own curves, bandwidth will grow; +81 legacy 'DEF' rejoin these after P1 mapping |
| RUC | ~41 | **own curve NOT supported** → declared pooling: establishment/trajectory SHAPE pooled (recommend: pooled with KPP × measured RUC level, the D10-declared precedent; test vs all-position pooled shape) — the standing "AFL rucks are thin — pool and say so" rule |
| mature (draft-age ≥19, all positions) | ~160 (plus ~175 age-unknown pending P1) | per-position NOT supported → the D14 TIER2 precedent: one 2D (draft-age × log-pick) surface pooled across non-RUC positions, RUC-mature separate and FLAGGED (D14 measured eff-n ≈ 12 there) |

**Pre-registered pooling decision rule (so Opus never improvises):** attempt the finest cell; if bandwidth maxes before eff-n≥35 on >20% of the pick grid, apply the next pooling rung (position-pair by KPP/nonKPP class → class → all-position shape × cell level) and DECLARE the rung in the output. The pooling TEST for any pooled pair: the R2-style ribbon check (max deviation of the finer slices from the pooled curve; fires at >0.05 of level, the D13 convention) — if the finer resolution genuinely differs, the pool is refused and the cell ships wide-bandwidth instead. RUC and mature pooling are EXPECTED (declared here in advance); everything else is expected unpooled at age≤18.

**2c.3 Draft-age structure.** Two tiers minimum (≤18 vs mature 19+), mature age-resolved within its 2D surface (the D14 precedent). Draft-age is a CONDITIONING variable, not a monotone constraint axis by default: mature-age picks realise faster with shorter runway, and the OUTCOME curve may legitimately cross the age-18 curve at deep picks (a 23-year-old at pick 40 can out-realise an 18-year-old at pick 40 in E-spot terms). The D14 monotone-in-age constraint was a law on PRIOR start values; whether Luke wants the same law imposed on the outcome-based curve (it would bind only where data disagrees with intuition) is DECISION-NEEDED **D5** (recommendation: TEST, don't impose — print violations for his eyeball; impose only on his word).

**2c.4 Shape constraints and their authority:**
- **Isotonic non-increasing in recorded pick within every (position × draft-age) cell — OWNER-LAW** (the R10/R12 order-law family, extended to the outcome curve; also structural: recorded pick is a market ranking). Applied as the final projection after kernel fit.
- **Across-position: NO constraint** (positions genuinely differ; Dean-below/Robey-above is signal — data-driven).
- **Tail plateau: ALLOWED** (v3.4 precedent) — monotone-to-plateau, never forced to zero; the deep tail's honest floor is the delist-scrap/washout mass in F, not an invented slope.
- **Winsorisation: value-given-established leg winsorised at 2.0× the cell norm (the D13 convention), pre-registered**; the quantile representation makes the price functional robust to the tail anyway.
- **P_est: isotonic non-increasing in pick, isotonic in nothing else.**

### 2d — THE KNOWN BUNDLE — each item's slot in the design

1. **1.19× retirement path** → §1.3. Slot: no derivation slot (unwired); P8 re-measures the symptom, strikes UNRESOLVED w9, registers the closure in CHANGELOG. Validation diagnostic V-D6 (§2e).
2. **~16% anchor resolution** → §1.2. Slot: P8 re-measures Yr1-vs-plateau on the post-bake head book (two views, full + 2015–24); the number that survives (if any) becomes a named residual with a mechanism hunt pre-registered; DECISION-NEEDED D2 records the supervisor-side referent question.
3. **MSD/SSP equivalents + phantoms** → §1.7. Slot: P7 re-derives PICKEQ by inverting the NEW price functional at the pathway pools' realised values, mix-weighted across (position × age) cells; phantoms keep-excluded, re-declared; the MSD ×1.5 stays (Luke-set constant, out of scope).
4. **Ramp-shape revisit** → §1.4. Slot: NOT a derivation job. D3 asks Luke to either close the R7 hook (keep t^1.5 as law) or open the snapshot-archive workstream. The spec's default: keep.
5. **FULL ruck V0/PVC derivation (replaces the ruck cap; 1.73 **[CONTAMINATED → v2.5 baked 1.4]**)** → §1.5. Slot: P6. Design: the RUC cell of the SAME fitted object (pooled shape × measured RUC level per 2c.2), giving (i) an outcome-based ruck pick price (the PVC's RUC column) and (ii) the outcome-based ruck start-value level that replaces the capped prior in V0\*'s RUC cell. The cap dial `RL_RUC_PRIOR_CAP` then has NOTHING to cap against the old PVC and is retired with an obituary; the owner's rung choice at the bake (if any) is superseded per the D4 pre-registration. Acceptance anchors: Emmett in Luke's stated 650–800 band [his words, D13] unless he re-rules on seeing the derived number; A6 gate green; the 172-ruck ladder [d14_ask3d] re-printed three-column. Ruck-specific traps declared: bimodal outcomes (Xerri-class late bloomers), ruck-onset timing (late establishment must not read as bust inside short windows — the trajectory depth grid handles it), n=41 decided age≤18 (the pool is the point).
6. **C1/C2 re-baselining** → §1.6. Slot: P0 (gate-zero). C1 naive baseline: last-2-season avg + simple age curve + position multipliers, scored on the book's headline metrics; C2: resurrect the V1 pick model as a scoring rule for realised pick outcomes; both harnesses become permanent gate scripts. Additionally C2's model is the pre-registered BENCHMARK for the new PVC's out-of-sample test (§2e.3).
7. **V0\* reconciliation** (not in the relay's bundle list but forced by the design, §1.9) → slot: P7, DECISION-NEEDED D6. The board-path start-value levels reconcile to the outcome curve; retention R_SURF re-derives on the new denominator; floor generating rule re-runs. This is the single largest board-value consequence of the whole program and is fenced accordingly (own job, own acceptance, own Luke read).

### 2e — VALIDATION DESIGN

**2e.1 Gates that must pass UNTOUCHED at the PVC-integrated candidate** (three-column, CONTROL · previous candidate · PVC-candidate, per R6): A1, A2*, A3*, A4, A5 (RE-BASED per its own note — the re-base is gate-text-sanctioned, not a violation), A6, A7, A8, A9, A10, A11, A12*, B1 (**the growth law: cross-cohort simple-average peak in years 4–6 with ≤5% pre-peak dip — the constitutional gate; the PVC must not tune to it, only be measured against it**), B2 (leakage), B5 (feature; saves-list re-printed and EXPECTED to churn at the re-base — the churn is the alarm surface doing its job, printed loud), B6 (ramp continuity), D14a/b/c (the V0 laws — the reconciled curve must satisfy them BY CONSTRUCTION, same as V0\* does). (*A2/A3/A12 are Luke-ruled reds at v2.x — carried, not caused.)

**2e.2 A13/A14 ACTIVATE** — the two PVC-staged pick gates leave PENDING for the first time: pick 1 line-ball (±20%) with EACH of Wardlaw and Ashcroft; pick ~8 line-ball with EACH of Rivers, Zach Reid, Burgoyne. Under E-disc these double as the δ-calibration anchors (2a.3) — which is legitimate exactly once and must be declared: **δ is FIT on A13/A14, so A13/A14 cease to be independent tests of the curve and become its calibration; the independent tests are the NEW anchors below** (leakage discipline: never count a number both as calibration and as validation).

**2e.3 New pre-registered validation, BEFORE any wiring:**
- **Out-of-sample pick-outcome test:** fit the curve on cohorts ≤2015, score its predictions of 2016–2018 realised outcomes against C2's V1 model and the v3.4 curve (log-score on F; absolute error on the price functional). The new curve must beat both. [OPUS-runnable, fully mechanical.]
- **Named-anchor set (owner ground truth):** Luke supplies 3–6 live pick-for-player relativities he would stake trades on TODAY (the A15/V_NEXT package-vs-star convexity question re-posed with exact picks belongs here). Registered VERBATIM before the derivation's numbers are seen (DECISION-NEEDED D10). His existing on-record reads join them: Emmett 650–800; "not all firsts are equal — pick 1 and pick 15 wildly different value" [A15 strike rationale].
- **Yr1-vs-plateau diagnostic (V-D6):** the §1.2 symptom re-measured at the post-bake head and again at the PVC candidate.
- **Cohort pick-mix table:** Yr1/pick-sum ratios re-cut against NEW pick denominators — the 73–95% band [d8 verdict] re-based; drift explained or flagged.
- **Hit-concentration + era-split + leave-one-cohort-out diagnostics** (§2b/§2c) printed with the derivation.

**2e.4 Leakage protections:** realised outcomes computed from raw store scoring only — the harvest NEVER reads `ev()`, board values, or any v2.x candidate machinery (the D10/D13 harvests are the audited precedent); fit/validate cohort splits pre-registered (≤2015 / 2016–18 / 2023+ as 2b.3); δ fitted only on A13/A14 with the anchor set quarantined; B2's IS-vs-WF harness re-run at the integrated candidate.

**2e.5 The walk-forward book: exempt or re-cut? Reasoned through, not assumed.** The precedent (R12): Luke exempted the BACKTEST from the V0 board curve because backtesting must see what the engine believed with the information of the day. The PVC is different in one decisive way: it is not a board-path start-value convention — it re-prices the RULER (draftval) that the book itself uses for pick-sum comparisons, and it feeds engine values through the PICKEQ/effpk band feature. So: **split by channel.** (a) The book's VALUATION path (player trajectories): must reproduce byte-identically under a PVC that only re-levels pick prices and display rulers — asserted with the maxΔ=0.000000 discipline of D14. (b) The book's RULER sheets (Measure-2 pick-sum, cohort/pick-mix tables): RE-CUT on the new denominators, clearly relabelled — these are display conventions, and leaving them on a retired curve would be the exact "dead yardstick" the 2026-06-30 diagnosis named. (c) The PICKEQ/effpk channel DOES move non-ND player values engine-wide — this is an ENGINE CHANGE, it goes through the full candidate + scoped-audit + gates machinery like any other (P7), and the book re-cuts with it at that stage. Nothing here is Luke's D14 exemption being overridden: (a) preserves it; (b)(c) are new decisions — registered as DECISION-NEEDED D11 for his confirmation of the channel split.

**2e.6 Pre-registered ABORT criteria (any → stop at a section boundary, report, hold for supervisor):**
1. C1 or C2 FAILS at the pre-PVC head → stop and re-scope (frozen SHIP_GATES instruction).
2. The primary-window harvest cannot support per-position age≤18 curves at eff-n≥35 for at least 4 of 6 positions → the conditioning promise of this spec is wrong; re-scope the cell structure with the supervisor.
3. The two value rulers (price6-based vs posval-best2-based) rank-disagree materially (Spearman <0.9 on decided cohorts) → the estimand definition is unstable; owner/supervisor decision before proceeding.
4. The out-of-sample test does NOT beat the V1 model → the derivation has no license to replace anything; publish the negative result.
5. A13/A14 cannot be brought inside ±20% by any δ ∈ [0.6, 1.0] → the curve and Luke's pick-vs-player intuitions are structurally inconsistent; that is a finding for his read, not a knob-hunt.
6. B1 breaks at the integrated candidate in an ENGINE-CAUSED way → standard bake-blocker triage.

**IN PLAIN TERMS (§2):** measure what every pick since 2006 actually became — including the kids who never played a game — separately for mids, talls, rucks and mature-agers; from that one measurement read off the pick's price, the safety-net floor, and the long-shot upside numbers, so they can never drift apart again; let Luke choose the one thing the data cannot tell him (whether a pick is priced at year-one value or closer to its ceiling); and prove the whole thing against his named trades — pick 1 against Wardlaw and Ashcroft — before a single board number changes.

---

## §3 — ASK 3: EXECUTION PLAN FOR OPUS (the owner's exposure map)

Sequenced jobs. Each: objective · inputs · pre-registered acceptance · session band · must-NOT-touch. Every design element carries **[OPUS-EXECUTABLE]** or **[FABLE-TIER RESIDUAL]**. Standing constraints on every job: engine evals sequential; one exec-load per process; three-column reporting (R6); loud state labels; per-job PR; canonical untouched; the pinned ENV incl. PYTHONHASHSEED=0 and PAR_RAMPS=22; exact-name guard.

**P0 — C1/C2 baseline harnesses (gate-zero).** Objective: build + run the naive baseline and the V1 pick model on the walk-forward book headline metrics at the post-bake head. Acceptance: both harnesses scripted into the gates suite; PASS/FAIL verdicts printed three-column; on FAIL → global abort #1. Band: ~2–3h. Must not touch: engine values. **[OPUS-EXECUTABLE — the C1 recipe is written in the gate text; C2's V1 model is in-repo history (`build_pvc` legacy + rl_model lineage).]**

**P1 — PVC-pool data hygiene.** Objective: the fit-ready entry table — at-draft position field (81 legacy 'DEF' mapped, switchers verified at draft position), draft-age (age() estimator adopted; 175 missing-_by + placeholder set printed for Luke), pre-2015 father/son & academy flag sweep (`_pvc_exclude`), concession-removal verification, Will Hayes dedup, entry-windowing keys for re-entries, phantom/name-guard assertions. Acceptance: a census doc with every exclusion/mapping COUNTED and named; zero unexplained rows; Luke sign-off items separated from mechanical ones. Band: ~2–4h. Must not touch: the store itself without Luke's data-pass word (proposals ride the census doc). **[OPUS-EXECUTABLE; one FABLE-TIER RESIDUAL inside: if the legacy-'DEF' mapping rule proves contentious (owner disagreement on >~10 players), the mapping is an owner data-pass, fallback = exclude-flag the residue and proceed (81 players ≈ 7% of decided pool).]**

**P2 — Harvest + ruler reconciliation.** Objective: per-entry realised trajectories T(d) on the locked price6/WQ6 era-adjusted ruler, busts=0, windows per §2b.3 (2020 games ×22/17), plus the ruler-agreement check vs posval-best2. Acceptance: harvest counts reconcile to the P1 census exactly; ruler Spearman ≥0.9 (else abort #3); artifacts pinned with md5s. Band: ~2–3h, 1–2 engine loads. Must not touch: `ev()` or any candidate machinery (raw store only). **[OPUS-EXECUTABLE — the D10/D13 harvest scripts are the audited template.]**

**P3 — The core fit.** Objective: F(v|k,c) + P_est(k,c) per §2c: two-part kernel fits over log-pick, eff-n≥35, pre-registered pooling tree, isotonic-in-pick projection, quantile surfaces, WQ6 price functional + CE ladder + E-trajectory aggregations (E-spot/E-disc/E-peak all computed). Acceptance: every cell's eff-n/bandwidth/pooling-rung printed (the D14 census format); pooling-test outcomes printed; constraint-authority table (data vs owner-law) printed; hit-concentration/era-split/LOCO diagnostics green or declared. Band: ~3–5h. Must not touch: any engine file. **[OPUS-EXECUTABLE — the pooling tree, tests and constraints are fully pre-specified; residual below.]** **[FABLE-TIER RESIDUAL, bounded: if the data refuses the pre-specified pooling tree in a NOVEL way (e.g. a non-RUC position fails eff-n at max bandwidth, or the ribbon test refuses ALL rungs), the re-scoping judgment is open-ended. Fallback without a Fable seat: apply abort #2 and hold — do not improvise a new tree.]**

**P4 — Censoring extension.** Objective: completion factors from decided-cohort realised trajectories; extend the fit input to 2019–2022; re-fit; compare against the P3 primary curve. Acceptance: extension moves the primary curve by a printed, bounded amount (pre-registered ribbon: cell-level shifts >10% are individually attributed); LOCO stability holds. Band: ~2–4h. **[FABLE-TIER RESIDUAL — the projection-factor design (how status/depth condition the completion factor, how uncertainty propagates) retains open-ended judgment; this spec fixes the skeleton but not every fork. Fallback: SHIP THE DECIDED-COHORTS-ONLY CURVE (P3) with the era-limitation declared — it is complete and valid on its own; the extension is an improvement, not a dependency.]**

**P5 — Estimand aggregation + owner read.** Objective: δ fit on A13/A14; the E-spot/E-disc/E-peak candidate curves at named anchors (Wardlaw, Ashcroft, Rivers, Zach Reid, Burgoyne, Emmett, + the D10 registry set); the Luke-facing pack (league-manager language, pipe tables, dollars-and-names) putting D1/D5/D8 to him with recommendations. Acceptance: pack sent; NOTHING WIRES until his rulings land in the ledger. Band: ~2h. **[OPUS-EXECUTABLE — the fork is presented, not decided; presenting it is mechanical once P3 prints the numbers.]**

**P6 — Ruck derivation (replaces the ruck cap; pre-v2.5 1.73 **[CONTAMINATED → v2.5 baked 1.4]**).** Objective: §2d.5. Acceptance: Emmett inside 650–800 OR the deviation put to Luke as a named read; A6 green; 172-ruck ladder three-column; cap-retirement obituary drafted (wires only with the P7 candidate). Band: ~2–3h. Must not touch: the dial itself outside the candidate branch. **[FABLE-TIER RESIDUAL, moderate: thin-bimodal pooling judgment (which shape donor, how the level factor is measured, ruck-onset windowing) — the spec pre-registers the D10 precedent (pool with KPP × measured level) but rucks have surprised this program twice (bimodal N1–3 means >1.0 [directive-v3 C.7]; scarcity prior 2.5× [D10]). Fallback: keep the R9 dial at Luke's chosen rung, curve the OTHER five positions, declare RUC deferred — explicitly acceptable per R9's design ("dial is Luke's to move").]**

**P7 — Integration candidate (the ENGINE CHANGE).** Objective: one candidate branch wiring, in order: (1) new PVC object → `draftval`/PVC swap + Measure-2/ruler re-cuts; (2) PICKEQ re-derivation (mix-weighted inversion); (3) V0\* level reconciliation (D6, per Luke's ruling); (4) R_SURF re-derivation on the new V0 denominator (same D13 method, denominators swapped); (5) B5 generating rule re-run + A5 re-base proposal; (6) ruck cap retirement (with P6); (7) full gates board three-column + book channel-split per D11 + A13/A14 first-ever evaluation. Acceptance: every §2e.1 gate green-or-Luke-ruled; walk-forward valuation path maxΔ=0 for channels (a); PICKEQ/V0 channels' movers ATTRIBUTED player-by-player (the D12/D13 discipline); scoped cold audit follows (the bake chain is unchanged: candidate → cold audit → Luke's written bake word). Band: ~4–6h (the big one) — split into P7a (curve+rulers) / P7b (PICKEQ) / P7c (V0+retention+floor) if any session runs short, in exactly that order (each sub-stage is independently gateable). Must not touch: canonical; the backtest guard path (Luke's exemption). **[OPUS-EXECUTABLE — every step has a v2.x-audited precedent (D10 re-anchor, D13 re-derivation, D12 re-base, D14 curve wiring); the order is fixed here; the acceptance is pre-registered.]**

**P8 — Symptom closure + paperwork.** Objective: V-D6 re-measures Yr1-vs-plateau at post-bake head and PVC candidate; strike UNRESOLVED w9 (1.19×); resolve the ~16% flag per D2; obituaries (SCALE_PVC staging, cap, superseded PVC v3.4) in BOARD_LAYERS_OBITUARY format with resurrection refs; SHIP_GATES A13/A14 PENDING→live status flip; V_NEXT #1 (package-vs-star) re-posed with exact picks. Acceptance: doc_lint green; ledger/CHANGELOG entries. Band: ~1–2h. **[OPUS-EXECUTABLE]**

**FABLE-TIER RESIDUAL COUNT: 4** (P1-minor: legacy-'DEF' owner mapping · P3-bounded: novel pooling-tree refusal · **P4: censoring-extension design — THE WORST RESIDUAL** · P6-moderate: ruck thin-bimodal pooling). **The single worst: P4.** Reason: it is the only place where an open-ended modelling choice (how unfinished careers are projected) directly moves fitted LEVELS with no owner-readable anchor to catch a bad choice — the others all fail loudly against pre-registered tests or Luke's own reads. Its fallback (decided-cohorts-only) is honest and complete, at the cost of the curve leaning on 2006–2018 football. Every other element of the program is executable from this spec without Fable-tier improvisation.

**IN PLAIN TERMS (§3):** eight jobs in a fixed order — prove the current engine beats the dumb baselines, clean the draft data, measure the outcomes, fit the curves, let Luke pick the one judgment number, fix the rucks, wire it all in one audited candidate, then close the old flags; four places are marked where a future session would need real judgment rather than instructions, and each of those has a written safe fallback.

---

## §4 — ASK 4: DECISION-NEEDED REGISTER (every owner fork, one place)

| # | the question (plain) | recommendation | what would change it |
|---|---|---|---|
| **D1** | When you trade for pick 5, are you buying what that kid will be worth NEXT YEAR, what he might be worth at his PEAK, or something in between? (the estimand time-aggregation, §2a.3) | **In between (E-disc):** a discount dial δ, defaulted so pick 1 lands square between Wardlaw and Ashcroft (your own A13 gate), then shown to you as named-player consequences for signature | your read of the named-anchor table at P5 — if the δ-fit prices feel wrong against trades you'd actually make, you move δ, not the curve |
| **D2** | The "~16% pick-anchor over-discount" flag the supervisor carries: the repo pins no derivation — the traceable origin is the OLD book's year-1 gap (0.84 ratio, 1/1.19), whose mechanism was deleted at D10. Confirm the flag means that symptom (and let P8 re-measure it), or state its other referent | treat as the year-1 book symptom; re-measure at the post-bake head; retire or re-target on the measurement | the supervisor producing a different referent with evidence |
| **D3** | The (season progress)^1.5 sit-out ramp you signed: keep it as your law permanently, or start archiving mid-season board snapshots so a data-derived shape becomes possible in ~2–3 seasons? | keep your law; archiving is cheap if you want the option (both is fine) | you caring enough about the shape to want it measured |
| **D4** | If you set the ruck dial to some rung at the bake (Emmett 650–800 sits at ~1.1–1.3), the later ruck derivation WILL supersede that rung. Pre-agree now that derived beats dialled, with your Emmett read as its acceptance anchor | pre-agree (prevents a future "dial vs derivation" standoff) | you deciding the dial should be permanent owner-law like the floor schedule |
| **D5** | Must a 23-year-old at pick 40 always price BELOW an 18-year-old at pick 40 (imposing your V0 age law on the OUTCOME curve), even if history says mature picks there realise more? | test, don't impose — print the violations for your eyeball first | your read of the printed violations |
| **D6** | When the outcome curve disagrees with today's fitted start values (V0\*), do outcomes win on the board? (this is the single biggest board-value mover in the program — it re-levels rookies, then retention and the floor re-derive on it) | outcomes win, phased through the P7 candidate with full gates + audit | the movers table at P7 — if outcome-priced start values break your named reads, the reconciliation becomes a blend and that blend is YOUR dial |
| **D7** | Retire the hidden glue (the legacy top-band anchor) that chains pick prices to the pre-2026 board's scale? | retire — the new curve is measured in board currency directly; the glue is where scale errors hide | nothing foreseeable; kept only if you want the old board's exchange rate preserved as law |
| **D8** | The old curve quietly paid deep picks a RISK BONUS (CE α 0.6→0.8, credits the rare hit). The new one prices the honest expectation and shows the risk ladder beside it. Who sets the risk appetite, and where? | derive the expectation; print the α/quantile ladder as a visible dial like the ruck cap; you set it at the board view if you want lottery tickets priced above expectation | your trading style — if you systematically value deep-pick upside, say so and the dial carries it, visibly |
| **D9** | Pick 1 stays = 3000? | yes (your locked anchor; pure rescale, moves nothing relative) | only a whole-currency re-anchor decision |
| **D10** | Name 3–6 pick-for-player trades you would stake your league record on TODAY (e.g. "I'd give pick 4 for player X, not for Y") — registered verbatim BEFORE the derivation prints, as its independent ground truth; include your package-vs-star instinct with exact picks (the struck A15, re-poseable) | supply them at P0–P2 time, before anyone sees fitted numbers | — (the earlier the cleaner; after P3 prints they are calibration, not validation) |
| **D11** | The historical book after the PVC lands: player-value pages stay byte-identical (your D14 exemption), but the pick-sum rulers and pathway pick-equivalents re-cut on the new prices. Confirm that channel split | confirm as specced (§2e.5) | you ruling the book must stay frozen on the old rulers too (then the new rulers ship as ADDITIONAL sheets, old ones marked retired) |

**DECISION-NEEDED COUNT: 11** (D1, D5, D6, D8 are the football-semantics/risk-appetite core; D2/D3/D4/D7/D9/D10/D11 are governance and can be batched).

---

## §5 — AUDIT DEPENDENCY + ASSUMPTIONS REGISTER

**Could the pending D13+D14 cold audit invalidate spec sections? YES — named:**
- **§1.5 / §2d.5 / P6 (ruck cap + ruck derivation):** if the audit faults the 1.73 **[CONTAMINATED → v2.5 baked 1.4]** median measurement or the cap's two-leg mechanism, the cap's baseline numbers (Emmett ladder, class median) re-measure — the DESIGN stands (an outcome-based ruck curve replaces whatever the cap turns out to be), the numbers re-cut.
- **§1.9 / D6 / P7c (V0\* reconciliation):** if the audit faults the D14 curve fit (cell census, pooling, isotonic application), the reconciliation TARGET changes — the principle (outcomes calibrate priors) survives, but P7c must re-baseline against the audited V0\*.
- **§2e.1 gate baselines and every three-column number quoted from v2.3/v2.4** (retention surfaces, anchor values, cohort totals): re-stamp after the audit + bake; this spec deliberately quotes them with state labels so the re-stamp is mechanical.
- **NOT exposed:** the estimand (§2a), survivorship design (§2b), conditioning/smoothing rules (§2c), the execution plan's structure, and the decision register — these derive from the raw store + governance history, not from the candidate engine.

**Assumptions this spec rests on (each checkable at P1/P2):** store profile numbers from this session's read-only census [store 644d1254 **[CONTAMINATED → v2.5 store e1b4d8bf; EVERY count in this paragraph re-cuts at P1/P2 on the current store]**]: 2,656 records · ND-with-pick 2003–2025 = 1,572 · decided ≤2018 ND = 1,130 (never-played 149) · season rows 2005–2026 · missing `_by` = 175 · pathway records 391 · phantoms 4 · RD = 693 (own 1–67 pick numbering — RD entries condition on entry-type, never mixed into the ND pick axis without a declared mapping). The bake lands before P-jobs run (the spec's "post-bake corrected history" premise) — if the bake order changes, P0 re-anchors to whatever head Luke blesses.

---

**IN PLAIN TERMS (bottom line):** this is the recipe for replacing the last old-world number Luke trades on — the draft-pick price list — with one measured from twenty years of what picks actually became, position by position, age by age, busts included; it names the four places where judgment (not instructions) would still be needed and gives each a safe fallback, and it puts the eleven calls that belong to Luke — starting with "is a pick worth next year's kid or his ceiling?" — in one register with a recommendation on each, so the remaining work can run on execution seats without anyone quietly deciding his league's economics for him.

---

## RE-STAMP LOG (v2.5, 2026-07-06 · housekeeping only — no fit, no board change)

**Board-untouched assertion:** this re-stamp branch (`claude/pvc-spec-restamp-…`) is based on the v2.5
`main` and edits ONLY this spec file. Store `engine/rl_after/rl_model_data.json` md5 = **`e1b4d8bf`**
(== pinned `data/expected_boot.json`); engine head `efea88e5`; band `34faa865`; `boot_guard.py`
Guard 5 **PASS** — verified before and after the edits.

### Contaminated → v2.5 equivalent
| number (as quoted in spec) | v2.5 disposition |
|---|---|
| RUC prior cap **1.73** | **→ 1.4** — baked default `RUC_PRIOR_CAP` (`_merged_recover.py:322`, "BAKED 1.73→1.4", v2.4-bake 2026-07-04); env dial `RL_RUC_PRIOR_CAP` name unchanged |
| canonical **8aed420a** | **→ efea88e5** (BAKED v2.5 canonical; `data/report_states.json`) |
| store **644d1254** | **→ e1b4d8bf** (baked-v2.5-2026-07-05) |
| band **34faa865** | **34faa865 — UNCHANGED** (still current in v2.5) |
| candidate line **7c199a1f** (v2.4) / **f3e537ba** (v2.3) / **af1fc6aa** (v2.2) | **→ folded into efea88e5** — that line was baked to the v2.5 canonical; no separate live candidate |
| V0 / Yr1 target **~217,573**, ratio **0.84**, **1.19×** | **no v2.5 equivalent — RE-DERIVE AT FIT** (pre-D10 book symptom, no pinned derivation; P8 re-measures Yr1-vs-plateau at the post-bake head) |
| primary window **2006**(–2018) | **→ 2004** — window moved 2006→2004 (DONE); read primary fit as **2004–2018** (§2b.3 supersession note) |

### Coordinate re-check — v2.5 `engine/rl_after/rl_model.py` (4 present, 0 moved-file, 0 deleted)
| coordinate | spec cite (v2.4) | v2.5 location | status |
|---|---|---|---|
| `SCALE_PVC` | rl_model.py:555-559 | rl_model.py:555-556 | **PRESENT** (same block) |
| pick-1 = 3000 (`RL_PICK1`/`BOARD_FACTOR`) | rl_model.py:565-570 | rl_model.py:565-567 (`RL_PICK1` default `'3000'`) | **PRESENT** (line-drift −3) |
| `PICKEQ` (`_pick_equiv`) | rl_model.py:675-727 | `_pick_equiv` :693, `PICKEQ` dict :699-724 | **PRESENT** (moved to :693-724) |
| `build_pvc_v34` | rl_model.py:531 | def :528, `PVC=build_pvc_v34()` :559 | **PRESENT** (moved to :528) |

The Wave-0 DPP strip / F1-F2 one-source rewire did **not** delete or relocate any of the four PVC
coordinates; only line numbers drifted v2.4→v2.5.

### Window confirmation (item 4)
The 2006→2004 primary-window change is **superseded/DONE** and now noted at §2b.3. The pre-change
`2006` echoes in §2c.2 and the §2/§5 plain-terms passages are retained for provenance and flagged;
read the primary fit as **2004-based** throughout.

**Bottom line of the re-stamp:** the DESIGN is intact and engine-current; what is contaminated is the
LEVELS the spec quoted off the old board. One number carries cleanly to v2.5 (ruck cap 1.73→1.4);
the state hashes re-point (canonical/store to efea88e5/e1b4d8bf, band unchanged, v2.2–v2.4 candidates
baked into efea88e5); the Yr1/V0 targets have no v2.5 equivalent and must be **re-derived at fit**;
the primary window is now 2004. All four code coordinates the derivation depends on still exist.
