# PREREG — ORDER 26B, THE DELIVERED-VALUE REDERIVATION

Committed **before any measurement of this order's own quantities**. Never edited after commit; breaches
owned by name in `SHIPPING_PACKET_26B.md`.

Authority: #334 comment 5269952564 (ORDER 26B brief, thirteen owner rulings, "Go" filed the same hour).
Branch `build/delivered-value` from `origin/main` @ `3b4df6f`. **NOTHING LANDS FROM THIS ORDER.**

Pins at prereg:

| object | path | md5 |
|---|---|---|
| store | `engine/rl_after/rl_model_data.json` | `d9a24282357cf3083b1640466e3ecd83` |
| board | `engine/rl_after/rl_app_data.json` | `88ce647f531030d8d2e094188b258191` |
| engine (price chain) | `engine/rl_after/_merged_recover.py` | `3f1468e5468462ab789e49aace264c90` |
| engine (model) | `engine/rl_after/rl_model.py` | `e5eb5e4405c09eebef45a9db89f014bc` |
| netting utility | `engine/forward_valuation/dist_redesign.py` | `48ea1bfeccc6d1ea51add66b0cb93965` |

---

## §0A — WHAT I HAD ALREADY SEEN BEFORE WRITING THIS (the 26A disclosure discipline, carried)

This prereg is **NOT BLIND on §1**. Before writing it I booted the engine read-only and measured the
following. Every one of them is disclosed here so that no confirmation below can be read as a prediction:

1. The live config: `GAMMA = 1.0` (so `val(r) = round(SCALE·r)` is **linear** — delivered value is
   additive across seasons in board points), `SCALE = 1.4398232006949683`, `SCALE_DIST = 1.0`,
   `LENS['bal'] = 0.14`, `RL_AGE_DISC` OFF, `REPL_DROP` uniform 3.0.
2. The effective bars off the engine's own netting path, `MA.REPL[g] − rd.REPL_DROP[g]`:
   **{MID 77.1, SD 75.3, RUCK 75.5, KPD 65.4, SF 67.9, KPF 63.8}** — identical to Ruling 1's stated set.
   Ruling 1 is therefore **verified, not predicted**.
3. That `price6(p, b6(p))` decomposes exactly into six band-level season paths through
   `proj_from_peak`, and that a season-path scorer built on
   `SCALE · posval(X + capt_prem(X) − bar[P]) · 21 / 1.14^k` reproduces the projection leg to floating
   point **once the two projection-side multipliers (×1.05 KPF/KPD; ×(1+runway·elite·PMAX)) and the
   `max(·, prod_floor)` are included**. On a first pass without the `prod_floor` context the
   reconstruction matched `price6` at the 1e-9 level for the plainest cases and diverged on
   floor-dominated veterans.
4. That the **live board price `v` is NOT `price6`**. On the 804 active rows I saw the summary
   distribution of `price6/ev` (median ≈ 0.956, p05 ≈ 0.086, p95 ≈ 4.01) and of `ev/board_v`
   (median 1.0524 — the L7 numéraire divisor). I did **not** attribute that wedge before writing this.

**Consequence for scoring: §1's prediction is a VERIFICATION, not a blind prediction, and must be read
that way.** §2–§7 were written before any of their quantities were computed and are genuinely open.

---

## §1 — THE IDENTITY GATE (Ruling 9) — NOT BLIND, see §0A

**Pinned price function (Ruling 3), declared here before the gate runs:**

```
season_points(X, P) = SCALE · posval( X + capt_prem(X) − (MA.REPL[P] − rd.REPL_DROP[P]) ) · 21
```
with `posval`, `capt_prem`, `SCALE` = `rl_model.py` (md5 `e5eb5e44…`) at lines 785, 676, 1120/1324; the
bar read live off `MA.REPL` **inside the engine's own lowered-REPL netting context** (never hand-copied);
`REPL_DROP` = `dist_redesign.py::REPL_DROP` (md5 `48ea1bfe…`, line 39). Discounting via
`rl_model.py::disc_factor(a, LENS['bal'], k)` at line 906. This is the k-th season term of
`rl_model.py::proj_from_peak` (line 963) — i.e. the engine's own per-season production price, reused, not
reimplemented.

**PREDICTIONS:**

1. **P1.1** The scorer reproduces `price6(p, b6(p))` for **every** active board player to within 1e-6
   relative, once the six band season paths are built with the engine's own `frac`/`PEAK_AGE`/`bnow`/
   `futblend` and floored with the engine's own `prod_floor` inside `price6`'s own REPL context.
   (VERIFICATION — see §0A.3.)
2. **P1.2** The gate **as literally specified — WQ6-weighted scored band careers vs the LIVE BOARD PRICE
   at ±2% — FAILS** for the majority of the panel. I predict **≤ 3 of 9** panel players inside ±2%.
3. **P1.3** The failure is **not** a defect in the price function. It is the wedge between `price6` (the
   band-blend production price) and `ev` (the shipped board price), which carries at least these named
   legs on top: the LEG-B un-compress map `_uncomp_prod` (RL_UNCOMP on, s = 0.10), the pedigree-pole
   blend `w·recover(perf,par)·max(0, po − pr)` in `raw_ev`, the isotonic pick guard `iso_eff`, the
   position caps (RUCK ceiling / W4 KPF compression), the sit-out and entry-anchor floors, and the L7
   numéraire divisor ≈ 1.0524.
4. **P1.4** The wedge is **signed by evidence depth**: thin-record and pool players read `mine/board_v`
   **above** 1 or far below 1 (pole-dominated), established high-tenure players read within ~10 %.
   Specifically I predict `mine/board_v` for **nick-daicos in [0.85, 0.95]** and for
   **vigo-visentini > 2.0**.
5. **P1.5 — THE DECISION RULE, STATED BEFORE THE RESULT.** If P1.2 realises, Ruling 9 binds:
   **STOP.** No derivation runs on an ungated scorer. The order then delivers (a) this prereg,
   (b) the gate with a full per-leg attribution of the gap, (c) **Layer 1 only** — because Ruling 11's
   Layer 1 is assumption-free raw facts with *no valuation fields at all*, is therefore not a derivation
   in Ruling 9's sense, and is explicitly "kept beyond the exercise" — and (d) the packet reporting the
   stop. Steps 3–6 (Layer 2, the derivations, the comparisons, the two instruments) **do not run**.
   I bind myself to this rule now so that a disappointing gate cannot be re-read into a pass.
6. **P1.6 — THE CLOSEST ACHIEVABLE IDENTITY CHECK**, named before the result so it cannot be chosen to
   flatter: `WQ6·[scored six band careers] == price6(p, b6(p))` at 1e-6, on the same panel. That check
   certifies the **price function**; it does not certify the board price, and I will not claim it does.

**Panel (fixed here, before the gate runs; ≥8 plus duursma, all six positions, ND + pool, young/mid/old,
established + thin):** `willem-duursma` (named by the owner), `nick-daicos`, `harry-sheezel`,
`marcus-bontempelli`, `max-gawn`, `harley-reid`, `jai-newcombe`, `harrison-ramm`, `vigo-visentini`, plus
a KPF, an SF and an SD row and at least two pool-pathway rows selected by the harness's own documented
rule (highest-board-value row in each missing cell) — the selection rule is fixed here, the identities
are not, so the panel cannot be shopped.

---

## §2 — THE ALL-IN PICK CURVE (Ruling 6, 13) — BLIND

Today's shipped curve (`rl_app_data.json::PVC`, the comparison target):

| pick | 1 | 2 | 3 | 5 | 7 | 10 | 15 | 20 | 30 | 40 | 50 | 64 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PVC | 3000 | 2999 | 2874 | 1881 | 1549 | 1460 | 1030 | 990 | 663 | 514 | 346 | 185 |

1. **P2.1 — PRE-ANCHOR SCALE.** Cohort-mean delivered value at pick 1 (busts at 0, entries ≤2021,
   discounted to acquisition, board points) lands in **[1800, 3800]**, point estimate **2600**.
   The anchoring factor to pin pick 1 = 3000 is therefore in **[0.79, 1.67]**, point estimate **1.15**.
2. **P2.2 — SHAPE vs THE CURRENT CURVE.** The derived all-in curve is **steeper at the very top and
   flatter in the deep tail** than the shipped PVC. Concretely: the shipped curve is almost flat over
   picks 1–3 (3000/2999/2874 = a 4.2 % drop); I predict the derived curve drops **more than 12 %** from
   pick 1 to pick 3.
3. **P2.3 — THE CROSSING.** Anchored at pick 1 = 3000, the derived curve sits **below** the shipped
   curve through the early picks and **crosses above it between picks 18 and 34** (point estimate
   **pick 26**), staying above through pick 64.
4. **P2.4 — THE DEEP TAIL.** Derived pick 64 / derived pick 1 lands in **[0.08, 0.18]** (shipped:
   185/3000 = 0.0617). Derived pick 64 (anchored) lands in **[240, 540]**.
5. **P2.5 — THE TOP RATIO.** Derived pick 1 / derived pick 10 lands in **[1.9, 3.0]** (shipped 2.05).
6. **P2.6 — SMOOTHER.** I pre-commit to reporting the smoother by name and printing per-pick n before
   any smoothing choice is defended, and to publishing the raw per-pick cohort means beside the smoothed
   curve. I expect per-pick n ≈ 18–20 for picks 1–20 on entries 2004–2021.
7. **P2.7 — RECONCILIATION LAW.** Position-weighted mean of the positional relativities equals the all-in
   curve at every pick, to **≤ 0.5 %** by construction; any pick where it does not is a HALT, not a
   tolerance.

---

## §3 — THE POOL PATHWAYS (Rulings 5, 12) — BLIND

26A's measured facts entering this: printed pool day-0 runs **2.6498×** the signed anchors overall;
positional `v0/anchor` spans **RUCK 1.315 → KPF 5.114**.

1. **P3.1 — PATHWAY ALL-INS, ND-PICK EQUIVALENTS.** Ranked, all-in delivered value per entrant:
   **RD > SSP > MSD > UNR ≈ IRE > PDA > PDN > PDS**. In ND-pick equivalents I predict
   **RD ≈ picks 48–62**, **SSP ≈ picks 55–64**, **MSD ≈ picks 58–64**, and **PDA/PDN/PDS/IRE/UNR all
   BELOW the pick-64 value** (i.e. off the bottom of the ND curve).
2. **P3.2 — THE CUT vs PRINTED DAY-0.** Derived pool v0s come in **far below** today's printed day-0
   prices. Whole-pool derived-v0 / printed-day-0 lands in **[0.28, 0.55]**, point estimate **0.40**
   (a cut of ~60 %).
3. **P3.3 — THE POSITIONAL PATTERN (26A's ordering, carried as a prediction).** The cut is **hardest for
   KPF and KPD, lightest for RUCK**. Specifically: derived/printed for **RUCK > 0.60** and for
   **KPF < 0.30**, with the full positional ordering
   **RUCK > MID ≈ SD > SF > KPD > KPF**.
4. **P3.4 — vs THE SIGNED ANCHORS.** Derived pool v0s land **much closer to the signed anchors than to
   the printed day-0 prices**: whole-pool derived/anchor in **[0.8, 1.6]**, point estimate **1.10**.
5. **P3.5 — BORROWING.** Under Ruling 12's ladder, **PDS, PDN and IRE cells borrow ≥ 60 %** of their
   positional v0 from the pathway-all-in × all-pool-lens rung or above; **RD borrows < 15 %** in every
   position; **MSD is mostly lens-on-level** (borrowing share ≥ 50 % in at least four of six positions).

---

## §4 — THE MSD / YOUNG-PATHWAY QUESTION, BOTH WAYS — BLIND

1. **P4.1** Augmented gated tails **raise** the MSD all-in relative to structural borrowing, by
   **10–35 %**.
2. **P4.2** My recommendation will be **structural borrowing**, on the ground that MSD's own tail
   projections are the thinnest-evidence objects in the order and the borrowing ladder is auditable
   per cell. I pre-commit to this recommendation now so that it cannot be selected by the number.
   If the numbers contradict it I will say so and change it **by name, as a registered deviation**.

---

## §5 — NAMED ROWS — BLIND (except duursma per §0A)

1. **P5.1 `willem-duursma`** — the gate row. Predicted `mine/board_v` in **[0.90, 1.06]**.
2. **P5.2 `callum-moore`-class** — a retired/near-zero pool row. Predicted delivered value
   **< 60 board points**, and predicted printed day-0 **more than 5×** it.
3. **P5.3 `harrison-ramm`-class** — thin-record young pool/late entrant. Predicted delivered value to
   date **< 120 board points** against a printed board value of **545**; ratio **< 0.25**.
4. **P5.4 `vigo-visentini`-class** — near-zero observed record, RUCK. Predicted delivered value
   **< 40 board points** against printed **182**.
5. **P5.5 `jai-newcombe`** — the pool success case. Predicted delivered value **> 1500 board points**,
   i.e. **above** the derived pick-30 all-in value, and the single strongest argument in the packet that
   the pathway *means* are low because of mortality, not because live pool players are cheap.

---

## §6 — THE TWO INSTRUMENTS — BLIND

**THE MARK-PATH PROGRESSION TEST.** Form, fixed here: with the **derived v0 as day-0** and the walk-forward
matrix's historical `vpath` marks as numerators, form for each pathway the big-cohort mean ratio
`m(d) = mean_i vpath_i[d] / v0_i` at career depths d = 0..6, all-in (dead kept at 0 in the numerator,
entry kept in the denominator). **PASS** for a pathway iff `m(d)` rises from `m(0)` and attains a maximum
`m*` with `m* > m(0)` at some d ≥ 2 — the ND shape.
- **P6.1** Every pathway with n ≥ 40 **passes**. Point prediction: `m(0) ≈ 1.0` by construction and
  `m* ∈ [1.4, 2.6]` for RD, MSD and SSP.
- **P6.2** At least one thin pathway (n < 40; PDS or PDN) **fails** — its curve is flat or falls — and I
  will report that as a thin-sample failure, not a design failure.

**THE REVERSE NO-ARB TEST.** Form, fixed here: a pathway is a *systematic guaranteed-loss hold* iff its
expected mark path from the derived entry value is **strictly dominated by selling at entry**, i.e.
`m(d) < 1` for **every** d ≥ 1 at the big-cohort grain, with the whole-pathway bootstrap upper CI on
`max_d m(d)` also below 1. **PASS = no pathway is a guaranteed-loss hold.**
- **P6.3** **No pathway fails.** I predict a clean pass on all pathways with n ≥ 40, and I predict the
  tightest pathway is **PDS**.

---

## §7 — THE V5 APPENDIX (NOT-RULED) — BLIND

1. **P7.1** Re-running Layer 2 with `RL_AGE_DISC=1, RL_AGE_DISC_MODE=5` (the owner's fifth ladder)
   **lowers** every delivered value relative to flat-14 for entrants acquired at age ≤ 21 by
   **less than 4 %** at the all-in level, because V5's young-side rates (12–13.5 %) are *below* flat-14
   and a lower discount **raises** present value — so the direction is a **rise**, not a fall.
   *I state the direction explicitly: V5 delivered values for age-18 entrants are HIGHER than flat-14,
   by 4–12 % at the all-in level.*
2. **P7.2** The V5 variant does **not** change the sign of any §3 conclusion, and moves no pathway's
   ND-pick equivalent by more than **6 picks**.

---

## §8 — PROCESS COMMITMENTS

- Explicit-path staging only; never `git add -A`; no model IDs in commits.
- One writer; every instrument committed beside its output.
- The Layer-1 dataset is a **first-class durable dataset** under `data/delivered_value/`, pinned by md5,
  with its builder committed beside it (Ruling 11).
- Nothing lands: no engine file changes, no pins moved, no board rebuild. PR to main; **MERGE NOTHING**.
- Any deviation from this prereg is reported **by name** in the packet, with the point at which it was
  taken and whether a result had already been seen.
