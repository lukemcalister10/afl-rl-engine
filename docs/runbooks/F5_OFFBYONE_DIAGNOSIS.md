# THE 1-POINT F5 OFF-BY-ONE — DIAGNOSIS (register v787)

**DIAGNOSIS ONLY. Nothing was applied.** Read-only throughout; the finding is reproduced from first
principles, not inferred from the audit's output.

## Verdict in one line

It is a **double-rounding artifact at the seal boundary**, not a ledger miss. `draft` and `mech` are
each rounded to an integer *independently*, and the *total* is rounded *independently again* from the
unrounded sum — so `round(a) + round(b)` and `round(a + b)` are allowed to differ by 1, and right now
they do. No value is lost, no player price moves, nothing in the store is wrong.

## The arithmetic, reproduced exactly

Recomputed from `session_2026-07-18/legf5/sealed_entrant_structure.json` + the release-active
`engine/rl_after/pvc_curve_v2.json` (`pool_value = 237.2`), following `rl_export.py:733-745`:

```
draft_float  = 49594.5606   ->  round = 49595   (rounded UP  +0.4394)
mech_float   =  7177.7109   ->  round =  7178   (rounded UP  +0.2891)
                                --------
sum_float    = 56772.2715   ->  round = 56772   (rounded DOWN -0.2715)   <- the DECLARED total
round(draft) + round(mech)  =    56773                                    <- the PARTS
                                 residual = exactly 1
```

The two upward roundings total `+0.7285`; the sum's own downward rounding is `-0.2715`; the difference
is exactly `1.0`. `Σ PVC[1..64] = 47315` is a sum of integers and is **exact**, so *all* of the draft-side
fraction lands in `residual_nd_tail` and *all* of the mech fraction in `residual_mech`.

## Which rows carry the residual

Read from the live board `data/rl_build/rl_app_data.json` (`a05fe951`):

| row | value | true float | rounding |
|---|---:|---:|---|
| `draftAssetTotals['+1'/'+2'].visible_1_64` | 47315 | 47315.0000 | **exact** |
| `draftAssetTotals['+1'/'+2'].residual_nd_tail` | **2280** | 2279.5606 | **up +0.4394** ← carrier |
| `draftAssetTotals['+1'/'+2'].residual_mech` | **7178** | 7177.7109 | **up +0.2891** ← carrier |
| `draftAssetTotals['+1'/'+2'].total` | 56773 | — | = sum of the rounded parts |
| `draftAssetTotals['+1'/'+2'].f5_entrant_layer_pvc` | 56772 | — | = `round(sum)` |
| `phantomTotals._meta.draft_pvc` / `.mech_pvc` | 49595 / 7178 | — | same two roundings |
| `phantomTotals._meta.entrant_layer_pvc` | 56772 | — | `round(sum)` |
| `phantomTotals.league['1'/'2'].draftValue` / `.freeValue` | 49595 / 7178 | — | sum = 56773 |
| `phantomTotals.league['1'/'2'].entrantValue` / `.delta` | 56772 | — | `round(sum)` |
| sealed `entrant_pvc` | `{draft:49595, mech:7178, total:56772}` | — | **the seal is itself internally inconsistent** |

**The two carrier rows are `residual_nd_tail` and `residual_mech`.** Neither is individually wrong —
each is correctly rounded on its own. The `+1` exists only in the comparison between the two
conventions. Note the same defect is visible three separate times on one board (`_meta`, `league`,
`draftAssetTotals`), and a fourth time in the sealed file.

## The code

**Root, `session_2026-07-18/legf5/scripts/seal_structure.py:103`:**

```python
'entrant_pvc': {'draft': round(draft_pvc), 'mech': round(mech_pvc), 'total': round(total_pvc)},
```

Three independent roundings of the same float triple, with **no assertion that `draft + mech == total`**.

**Mirrored in `engine/rl_after/rl_export.py`:**

- `:817` — `'entrant_layer_pvc': round(_lf_ent_pvc), 'draft_pvc': round(_lf_draft_pvc), 'mech_pvc': round(_lf_mech_pvc)`
- `:842` — `_draft_r = round(_lf_draft_pvc); _mech_r = round(_lf_mech_pvc)`, then `total = _PVC64 + _res_nd + _res_mech`
- `:875` — the same rounded total emitted beside the rounded parts
- `:829-833` — the league roll-up rounds `draftValue`, `freeValue` and `entrantValue` independently

### Why the guard that should have caught it structurally cannot

`rl_export.py:752-757` (the `#306 L7` reconciliation HALT):

```python
if round(_lf_ent_pvc) != _lf_sealed_total:
    raise SystemExit('LEG F5 HALT (#306 L7 reconciliation): ...')
```

Both sides use the **same** `round(sum)` convention — the board's `round(_lf_ent_pvc)` against the
seal's `round(total_pvc)`. It compares a number to itself computed the same way, so it is blind to the
parts/total split by construction. It passes, and the render proceeds.

### And why `reconciled_to_f5` reports PASS while the real check FAILs

`rl_export.py:872` computes:

```python
'reconciled_to_f5': (_PVC64 + _res_nd + _res_mech == _draft_r + _mech_r)
```

Substituting `_res_nd = _draft_r - _PVC64` and `_res_mech = _mech_r`, the left side reduces to
`_draft_r + _mech_r` — the right side. **It is a tautology: always `True`, for any inputs.** That is
why `invariant_proof.py` prints `PASS (13) lens +1: draftAssetTotals reconciled_to_f5` on the very same
board where the strengthened cross-check fails. The vacuous flag was camouflaging the real one.

## When it first appeared

Bisected cheaply through the four commits that ever touched
`session_2026-07-18/legf5/sealed_entrant_structure.json` — reading each committed `entrant_pvc` triple
and recomputing the floats against that commit's own curve. No rebuilds.

| commit | date | draft | mech | total | parts − declared | fracs (draft + mech) |
|---|---|---:|---:|---:|:--:|---|
| `a5b306c` leg F5 seal created | 07-18 | 69266 | 14272 | 83538 | **0** | — |
| `dab9657` #306 landing | 08-05 | 55669 | 7057 | 62726 | **0** | 0.1328 + 0.5681 = 0.7009 → no carry |
| `d4f0be1` #328 resumed | — | 55753 | 7178 | 62931 | **0** | 0.9899 + 0.7109 = 1.7008 → carry, and `sum` frac 0.7008 also rounds up |
| **`1fd8e12`** **ORDER 29: THE BOOK RE-SEALED** | **2026-08-13** | 49595 | 7178 | **56772** | **1** | **0.5606 + 0.7109 = 1.2715 → carry, but `sum` frac 0.2715 rounds DOWN** |
| `3c51271`, `189c34e` (current) | 08-19/20 | 49595 | 7178 | 56772 | **1** | unchanged |

**First appearance: `1fd8e12`, 2026-08-13, "ORDER 29: THE BOOK RE-SEALED — ISOLATED COMMIT (PREREG P19)".**

The important nuance: **the code defect is older than the symptom.** The three-independent-roundings
pattern has been there since the seal was created on 2026-07-18. It stayed invisible for three seals
purely by luck of the fractional parts — at `dab9657` the two fractions did not carry, and at `d4f0be1`
they carried *and* the sum rounded up too, so both conventions moved together. ORDER 29 moved the curve
head, which moved the draft fraction from `0.9899` to `0.5606`, and the luck ran out. Nothing was
"broken" on 08-13; a latent defect became observable.

This also confirms the released baseline was internally consistent: `65925 + 2631 + 9055 = 77611` exactly.

## Materiality — does anything consume the declared total where 1 point could matter?

**No money moves. No player price, club total, pick price or numéraire is affected.**

| consumer | affected? |
|---|---|
| player values / board `v` / club totals | **No.** The per-club allocation uses the *unrounded floats* (`_lf_mech_share`, `_cdraft_val`) and rounds only at display. The 1 never reaches a club or a player. |
| PICK 1 numéraire (3000) | **No.** Untouched. |
| the store | **No.** Occupancy conservation is separately asserted (`rl_export.py:739`) and holds. |
| `gate_f5.py` (§2.x conservation gate) | **No.** It compares `board_ent == ENT` — both the `round(sum)` convention, so it agrees; its numeric gates are ±5% and 1/56772 = 0.0018%. |
| `#306 L7` reconciliation HALT | **No** — and that is the problem: it is structurally blind here (see above). |
| `invariant_proof.py` per-push lane | **Yes.** 2 of 28 FAIL, both lenses. This is the red under diagnosis. |
| `session_2026-07-21/final_integration/tests/r15_ladder_survival_proof.py:143-157` | **Yes.** It carries the *identical* strengthened assertion and must be red for the same reason — a second consumer that one fix clears. |
| `ui/tests/extract_seam.test.py:132-135` | Separate, pre-existing: hardcoded `83538` / `103.43`, stale since the #274 adoption. Not this bug. |
| the 13 `ADOPT-RED` rows | **Unrelated.** Those are the *released baseline literals* (`RELEASED_F5_ENTRANT=77611`, `65925`, `2631`, `9055`) still naming the pre-ORDER-29 layer. Different root cause; the audit's separation is correct. |

So the materiality is **not arithmetic, it is gate integrity**: a board that disagrees with itself keeps
a per-push lane red, trains readers to expect red, and — as the `reconciled_to_f5` tautology shows —
the surrounding checks are weak enough that a *real* miss of the same size would look identical.

## Proposed fix (NOT APPLIED)

**Principle: make ONE rounding decision, at ONE boundary, and derive everything else from it.** The
parts are the primitive — they are what the reconciliation panel shows and what ties to the visible
1–64 ladder. The total is *definitionally* their sum and must never be rounded a third time.

1. **`seal_structure.py:103`** — round once, sum the rounded parts, and assert:
   ```python
   _d, _m = round(draft_pvc), round(mech_pvc)
   'entrant_pvc': {'draft': _d, 'mech': _m, 'total': _d + _m},
   ```
   plus a hard `assert` that the emitted triple closes, so it can never go latent again.

2. **`rl_export.py`** — emit the integer total as `_draft_r + _mech_r` everywhere it appears
   (`:817` `entrant_layer_pvc`, `:875` `f5_entrant_layer_pvc`, `:829-833` `league.entrantValue`/`delta`),
   while keeping the **float** `_lf_ent_pvc` as the basis for per-club allocation (so no club number moves).

3. **`rl_export.py:872`** — replace the tautological `reconciled_to_f5` with a real comparison against
   the seal's own total, so the flag can actually fail.

4. **`rl_export.py:752`** — keep the `#306 L7` HALT but compare the *parts* convention on both sides,
   so it is no longer blind to this class.

### The cost, stated honestly

This is a **pin-moving act**, not a one-line patch:

- the declared layer moves **56772 → 56773**, which is owner-visible;
- the seal must be rebuilt: `seal_sha256_8` `cbb7c431` → new, and the literal pinned at
  `rl_export.py:718` (`== 'cbb7c431'`) must move **in the same commit** or the render halts;
- `data/release_contract.json`'s f5 block, `data/expected_boot.json` and the board md5 all move with it;
- `r15_ladder_survival_proof.py` and `invariant_proof.py`'s per-push lane both go green as a consequence.

**The alternative — changing the proof's convention to accept 56772 vs 56773 — should be refused.** That
is editing the expectation to match an output, which is exactly what the build-and-compare law in
`sibling_repin.py` forbids, and it would leave the board genuinely disagreeing with itself.

### Sequencing note

Because this moves the board md5 and the seal, it should **not** be folded into the R23 round advance —
that act is "data and nothing else", with the five model pins deliberately still. Land it as its own
isolated act, before or after R23, with its own prereg. Until it lands, the two `invariant_proof` FAILs
will re-fire on every rebuilt board including R23's, and must not be mistaken for round-advance damage.
