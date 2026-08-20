# PREREG — ACT A: THE F5 ROUNDING ACT

**Written and committed BEFORE any engine edit.** Base: `main` @ `3c983c3` (Act B landed).
Live board `7a3f4fe2` / 692,296 / 804, store `b745002e`, `as_of_round` 23, engine_head `1867e953`,
balanced `3970156c`. Authority: `docs/runbooks/F5_OFFBYONE_DIAGNOSIS.md`.

---

## 1. THE PREMISES, RE-VERIFIED AGAINST THE CURRENT TREE

The diagnosis predates the D8 adoption and the R23 advance, so its arithmetic was **recomputed from
first principles on this tree** (sealed occupancy counts × the release-active `pvc_curve_v2.json`),
not read from its own output:

```
draft_float  = 49594.5606  ->  round = 49595   (up +0.4394)
mech_float   =  7177.7109  ->  round =  7178   (up +0.2891)
sum_float    = 56772.2715  ->  round = 56772   <- the DECLARED total
round(draft) + round(mech) =   56773           <- the PARTS
                               residual = exactly 1
```

**Every figure reproduces the runbook exactly. The declared move `56772 → 56773` stands unchanged**,
and `Σ PVC[1..64] = 47315`, `residual_nd_tail = 2280`, `residual_mech = 7178` all reproduce. The
curve **payload** md5 is `9729f0c5` in both eras — the pricing basis never moved — which is why R23
and D8 did not disturb the arithmetic. The two `invariant_proof` FAILs are live on the current board
(26/28 PASS), and they are exactly the predicted pair.

**Premises hold. The runbook's logic applies unchanged. Proceeding.**

### What the declared quantity IS, in plain terms

It is the **F5 entrant layer**: the once-a-year value of a whole incoming AFL intake — the 64 national
draft picks priced off the release-active pick curve, plus the deep tail and the non-draft entry
mechanisms — carried on the +1/+2 forward views as one report-only aggregate. It is **not** a player
price and **not** money: no club total, no pick price, no numéraire and nothing in the store depends
on it. The defect is that the board states this one quantity **twice by two different conventions** —
`round(a)+round(b) = 56773` beside `round(a+b) = 56772` — and the two disagree by 1.

---

## 2. THE METHOD DECISION ON THE SEAL, AND WHY (a deviation, declared)

The runbook says "the seal must be rebuilt". **A literal re-run of `seal_structure.py` is REFUSED**,
on measurement:

| stamp field | committed seal | a re-run today would write |
|---|---|---|
| `curve_payload_md5` | `9729f0c5` | `9729f0c5` — **same** (the pricing basis) |
| `store_md5` | `d9a24282` | `b745002e` — **moved** |
| `board_balanced_md5` | `234c3414` | `3970156c` — **moved** |
| `curve_file_md5` | `0be17c8f` | `78ad9842` — **moved** |

A re-run would **re-measure occupancy against a store that has moved three times** since the seal
(R22, R23, D8, the sheet re-cut) and would restamp three provenance fields. That is a **RE-COUNT**.
The runbook's own cost list does not include it, and `rl_export.py:730` records that seal `cbb7c431`
is "a re-price of a frozen measurement, **never a re-count**".

**What is done instead** — exactly the runbook's fix item 1 and nothing else: the sealed artifact is
re-emitted under the corrected rounding rule, with `total` derived from **the seal's own committed
parts** (`49595 + 7178`). The counts are frozen history and are not re-measured; the parts are
independently re-verified every render by repricing those frozen counts at the live curve (the
`#306 L7` reconciliation), and that check is strengthened by this act.

**Predicted: the ONLY field that changes in the sealed file is `entrant_pvc.total`
(56772 → 56773), and `seal_sha256_8` `cbb7c431` → `ccc26a9e`.** (Computed, not typed. The committed
seal was verified to recompute to `cbb7c431` first, so the hash function is confirmed before use.)

---

## 3. THE CODE FIX — ONE ROUNDING DECISION, AT ONE BOUNDARY

The rounded parts `_draft_r` / `_mech_r` are hoisted to the point where the floats are computed and
**reused everywhere**, so the principle is literal in the code rather than repeated by hand.

| site | change |
|---|---|
| `seal_structure.py` entrant_pvc | round once, `total = _d + _m`, plus a hard `assert` so it can never go latent again |
| `rl_export.py` seal pin `cbb7c431` | → `ccc26a9e` (same commit as the seal, or the render halts) |
| `rl_export.py` `#306 L7` HALT | compare the **parts** convention on both sides — it currently compares `round(sum)` to `round(sum)`, i.e. a number to itself, and is blind to this class by construction |
| `rl_export.py` `_meta.entrant_layer_pvc` | `round(_lf_ent_pvc)` → `_draft_r + _mech_r` |
| `rl_export.py` `f5_entrant_layer_pvc` | `round(_lf_ent_pvc)` → `_draft_r + _mech_r` |
| `rl_export.py` `reconciled_to_f5` | replace the **tautology** (it reduces algebraically to `X == X` and is `True` for any inputs) with a real comparison that includes the seal's own total |
| `rl_export.py` league `entrantValue` / `delta` | parts convention, derived per lens as `round(draftValue) + round(freeValue)` — so lens 0 stays **0** (the k=0 zero-phantom invariant) |

**The float `_lf_ent_pvc` remains the basis for per-club allocation, so no club and no player number
moves.** Per-club `phantomLayer` is deliberately untouched.

### THE ONE DECLARED EXTENSION beyond the runbook's enumerated sites

The runbook names `league.entrantValue`/`delta`. But `delta` **is** `withPhantom − withoutPhantom` by
construction, so moving `delta` alone would leave the league block newly self-contradictory — the
exact disease this act cures. `withPhantom` is therefore derived as
`withoutPhantom + entrantValue`, closing the block. This is **declared as an extension**, with its
own predictions below, rather than smuggled in. If the owner prefers the strictly-minimal reading,
this is the one line to revert.

---

## 4. NUMERIC PREDICTIONS

### The build
* **A0** A control build on the unmodified tree reproduced **`7a3f4fe2` exactly** (already measured,
  `06_f5_builds.txt`), so every diff below is attributable to these edits alone.
* **A1** The dev and canonical builds agree **byte-for-byte** on the new board id.

### The board — what MOVES (and by exactly 1)
| field | from | to |
|---|---|---|
| `draftAssetTotals['+1'/'+2'].f5_entrant_layer_pvc` | 56772 | **56773** |
| `phantomTotals._meta.entrant_layer_pvc` | 56772 | **56773** |
| `phantomTotals.league['1'/'2'].entrantValue` | 56772 | **56773** |
| `phantomTotals.league['1'/'2'].delta` | 56772 | **56773** |
| `phantomTotals.league['1'].withPhantom` *(extension)* | 687952 | **687953** |
| `phantomTotals.league['2'].withPhantom` *(extension)* | 257524 | **257525** |
| `phantomTotals._meta.seal_sha256_8` | `cbb7c431` | **`ccc26a9e`** |

### The board — what MUST NOT MOVE
* **A2** All **804** players' `v`, `vM2`, `vM1`, `vP1`, `vP2` — **byte-identical**.
* **A3** The **198** `back` rows — **byte-identical**.
* **A4** `lensPicks` (128 rows), `visible_1_64` = 47315, `residual_nd_tail` = 2280,
  `residual_mech` = 7178, `total` = 56773, `f5_draft_pvc` = 49595, `f5_mech_pvc` = 7178 — unchanged.
* **A5** **`phantomTotals.league['0']` entirely unchanged, `withPhantom` = 692,296** — the headline
  board number. The balanced board carries zero phantom; if lens 0 moves, the k=0 invariant is broken
  and this act is wrong.
* **A6** `balanced_board_md5` `3970156c` **unmoved** (this act does not rebuild the sibling), store
  `b745002e` unmoved, `engine_head` moves (an engine file is edited — `rl_export.py`).
* **A7** The diff between the control board and the F5 board consists of **nothing but** the seven
  rows in the MOVES table.

### The consumers that must go green
* **A8** `invariant_proof.py` per-push lane **26/28 → 28/28**; both F5 FAILs cleared.
* **A9** `r15_ladder_survival_proof.py`'s identical strengthened assertion goes green.
* **A10** `reconciled_to_f5` stays `true` — but now as a **real** check. Non-vacuity is proved
  separately: the new expression must be shown to return `False` on a deliberately mismatched input.

### The landing
* **A11** The board move is **out of round**, so by the standing owner rule (2026-07-28) it owes an
  out-of-round column `the-f5-rounding-20-8` at `after_round` **23** and a lineage entry
  (`owner_ruling_id: THE_F5_ROUNDING_2026-08-20_launch_the_ready_items`). Written by the writer of
  record `out_of_round_column.add_column`. Under Act B's repair it is stamped `seq` 0 — the first
  column whose position is recorded rather than raced for alphabetically.
* **A12** Pins that move with the board: `data/expected_boot.json`, `data/release_contract.json`
  identities, both `.srcmd5` sidecars, `ui/data/board_view_working.js`, `ui/data/board_view_public.js`,
  `ui/data/movers.js`, `ui/data/movers_transition.js`, `data/release_lineage.json`.
* **A13** Two `ui/tests/movers.test.js` **weekly pins** move, both because the *kind* of act that
  last moved the board changed from a round advance to an out-of-round move — the file documents this
  line as tracking exactly that and as having "swung both ways twice":
  * boundary count `8` → **9**;
  * lineage state `[true,"ok"]` → `[true,"bridged"]`.
  The two **non-vacuity** assertions around the state must keep passing in both directions. If either
  non-vacuity assertion fails, the state has stopped discriminating and this act **HALTS**.
* **A14** Suites: `test_movers_transition.py` **39/39**, `ui/tests/movers.test.js` **66/66**.
* **A15** Gates: `acceptance.runner` **GREEN**, `release_manifest_check.py` **PASS**,
  `release_contract.py check` **PASS**.

---

## 5. FALSIFIERS — ANY ONE HALTS ACT A

* **F1** Any player `v`/`vM2`/`vM1`/`vP1`/`vP2` moves, or any `back` row moves. *(No money may move.
  The whole warrant for this act is that it is a presentation-consistency repair.)*
* **F2** `phantomTotals.league['0']` moves at all — the k=0 zero-phantom invariant.
* **F3** The board diff contains anything outside the seven predicted rows.
* **F4** The sealed file differs from the committed one in any field other than `entrant_pvc.total`,
  or the new seal is not `ccc26a9e`.
* **F5** `invariant_proof` does not reach 28/28, or any *other* check regresses.
* **F6** The new `reconciled_to_f5` cannot be shown to return `False` on a mismatched input — i.e. it
  is still a tautology wearing a new expression.
* **F7** Dev and canonical builds disagree.
* **F8** Suites are not 39/39 and 66/66, or a movers non-vacuity assertion fails.
* **F9** Any gate goes red. **F10** `balanced_board_md5` or the store moves.

## 6. THE RE-SEAL BLOCKERS — SCOPE, STATED UP FRONT

`docs/evidence/landing_prep_2026-08-20/RESEAL_HALT.md`'s three blockers are about
**`data/book_stable_seal.json`**, the FULL book re-seal, which runs `s4_matrix_M1v7.py` under gate
mode. **That is not this act's seal and stays owner-pending regardless.** F5's own seal
(`sealed_entrant_structure.json`) neither runs `s4_matrix` nor enters gate mode. The gate-mode probe
required by the brief is reported separately in `FINAL_STATE.md`; it changes nothing here.

## 7. WHAT THIS ACT REFUSES

Changing the proofs to accept `56772` vs `56773`. That is editing the expectation to match an output,
which `sibling_repin.py`'s build-and-compare law forbids, and it would leave the board genuinely
disagreeing with itself. The board is corrected; the proofs are not touched.
