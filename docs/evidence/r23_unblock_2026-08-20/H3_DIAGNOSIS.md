# H3 — the 96/804 sibling parity failure. VERDICT: **REAL. The sibling board is mispriced.**

**Seat:** R23 unblock, build seat · **Date:** 2026-08-20
**Base measured:** `origin/main` @ `7f6c40a` (with M1a's `aebf192` landed) — store `cc02567f`,
board `a05fe951`, `as_of_round=22`, `rl_model` `6fe7c415`, `fv_identity` `6e9a370e…`, config `eed19a75`.
**Nothing was written to the repo by any measurement here. No valuation expression was changed.**

---

## 0. The verdict in one paragraph

The supervisor's cross-link hypothesis was tested **first** and is **refuted for the sibling build**.
The same *defect class* is at work — a `BASE_REF` residue left by the un-lensed forward `ev()` calls —
and it is the **same 96 rows**. But in `one_source_selftest` the polluted side was the **checker** and the
canonical board was clean, which is why M1a's `aebf192` correctly cured it. In the balanced/strict
**sibling build** the polarity is reversed: the parity gate's recompute is the **clean** side and the
**board** is the polluted one. Applying full lens/memo discipline to the *comparison* was measured
directly and changes **nothing** (96 → 96). The sibling board's 96 values are wrong — provably, against
the board of record itself. **The advance stays blocked. The fix moves board prices and is a valuation
act above this seat.**

---

## 1. Reproduction

Pristine base, no R23 data, no synthetic data, `sibling_repin._run_sibling_build(balanced=True)`
(`RL_PVC2=1 / RL_LEGE=0 / RL_LEGF=0`, no `RL_CONFIG_MODE`) — the exact call `staged_apply._stage_sibling`
→ `sibling_repin.build_sibling` makes inside the transaction:

```
EXPORT<->ENGINE PARITY GATE FAILED for 96/804 players (board v != engine gated ev, eps=0):
  harry-sheezel: board=10310 engine=10433   |  will-ashcroft: board=6494 engine=6607
  nasiah-wanganeen-milera: board=8593 engine=8644 | aaron-cadman: board=1667 engine=1781
  ...  (all 96 are board < engine)
```

Raw: `raw/h3_sibling_parity_mainbase.txt`. Driver: `raw/h3_repro_driver.py`.
Reproduced identically **before and after `aebf192`** — that commit touches
`engine/rl_after/one_source_selftest.py` only, and the sibling build never imports it.

The **canonical** build on the same tree (`balanced=False`, `RL_CONFIG_MODE=canonical`) returns
`rc=0`, board **`a05fe951f78482c70520480e184c80ec` — byte-exact to the pin** — and prints
`PARITY GATE PASS: all 804 active board values == engine gated ev()`
(`raw/h3_canonical_build_pass.txt`).

---

## 2. Testing the cross-link hypothesis on the comparison — the ordered first test

The gate that fires is `rl_export.py:649-666`, the exporter's **own** eps=0 F1 tripwire, not a separate
checker. Its recompute loop was instrumented in scratch to evaluate, for every player, `ev(p,2026)`:

| variant | what it does |
|---|---|
| `gate_asis` | as the gate calls it today |
| `gate_2nd` | called a second time immediately (idempotence) |
| `gate_clean` | after `_LENS_FORM=None; BASE_REF=AGE_REF=2026; _pe_clear()` — the exporter's full lens/memo discipline, applied to the **comparison only** |

Result, on the 96 failing rows:

```
gate_asis == gate_2nd == gate_clean       96 / 96
board_v   == gate_clean                    0 / 96
```

**The lens/memo discipline applied to the comparison changes nothing.** The gate's recompute was
already clean and is order-independent. This is not a false red.

---

## 3. Where the divergence actually comes from — isolated to one symbol

Same instrumentation, this time forcing the engine clock before each recompute:

| forced state before `ev(p,2026)` | matches the **sibling board** |
|---|---|
| `BASE_REF=2026, AGE_REF=2026` (clean) | 0 / 96 |
| `BASE_REF=2026, AGE_REF=2028` | 0 / 96 |
| **`BASE_REF=2028, AGE_REF=2026`** | **96 / 96** |
| `BASE_REF=2028, AGE_REF=2028` | 96 / 96 |
| `ev(p,2028)` then `ev(p,2026)` | 96 / 96 |
| `ev(prev_player,2028)` then `ev(p,2026)` | 96 / 96 |

`AGE_REF` residue is provably inert. **The entire effect is `MA.BASE_REF`.**

Across the whole board: `sibling_board_v == value_at_BASE_REF_2028` for **803 of 804** rows. The one
exception is `nick-daicos` — `players[0]`, priced before any residue could exist, because
`rl_export.py:113` pins the clock immediately before the loop. That is the signature of order-dependent
pricing, and it is what the fixture below explains.

### The mechanism, stated exactly

`rl_export.py:189-221` — the value loop — evaluates, per player:

```python
_r = _ev(_p, 2026)                                   # <-- the board's value, FIRST call of the iteration
_p['_vM2'], _p['_vM1'] = _nb(_ev(_p, 2024)), _nb(_ev(_p, 2025))
if os.environ.get('RL_LEGE', '1') != '0': g['_LENS_FORM'] = 2026     # :197
_p['_vP1'], _p['_vP2'] = _nb(_ev(_p, 2027)), _nb(_ev(_p, 2028))
g['_LENS_FORM'] = None                                              # :199
```

`_merged_recover.ev()` re-pins the clock only once it reaches `_b6_core` / `price6`
(`_merged_recover.py:371, 389`), which do
`MA.AGE_REF=Y; MA.BASE_REF=(MA._LENS_FORM if … else Y); MA._pe_clear()`.
**Everything `ev()` evaluates before that point reads the ambient `MA.BASE_REF`** — the value the
*previous player's last call* left standing. The exporter knows this: `rl_export.py:222` says in as many
words, *"the ev loop advanced the clock to the last as-of year; re-pin to the present"* — but it re-pins
**after** the loop, not per row.

* **Canonical posture (`RL_LEGE=1`).** Line 197 sets `_LENS_FORM=2026`, so `ev(p,2027)` and `ev(p,2028)`
  set `BASE_REF = _LENS_FORM = 2026`. The residue *is* the present. Harmless — and F1 passes 804/804.
* **Balanced/strict sibling (`RL_LEGE=0`).** `_LENS_FORM` is never set, so `ev(p,2028)` leaves
  `BASE_REF = 2028`. The next player's `ev(p,2026)` — the number written to the board — is computed on a
  **2028 form/tenure/peak basis**. For 96 rows that changes the rounded value.

This is exactly why the two counts are the same 96: it is one BASE_REF-sensitive cohort, seen from
opposite sides. Measured directly — the set of rows whose value moves between `BASE_REF=2026` and
`BASE_REF=2028` is **97 keys under both postures**, and the sibling's 96 failures are that set **minus
`nick-daicos`**, the row that escapes because it is priced first.

---

## 4. Is the board wrong, or is the gate wrong? — the both-ways evidence

**Three independent lines all say the board.**

1. **Hand-computed `ev()` under the correct as-of sequence.** For twelve probed keys spanning the fail
   set and the pass set, `ev(p,2026)` issued as the **very first engine call after load**, clock pinned
   to the present, nothing else evaluated first, equals the `gate_clean` value **exactly**, in **both**
   postures. Example: `harry-sheezel` `10979.257` first-call = `10979.257` clean = board-of-record
   `10433` after ÷ numéraire 1.0524; the sibling board writes `10310` = the `BASE_REF=2028` value.

2. **The board of record.** Corrected sibling value vector vs the canonical board `a05fe951`:
   **804 / 804 identical**, sum 664,949 = 664,949. The sibling **as built** agrees on 708 and disagrees
   on exactly the 96. So the sibling board contradicts the board of record on those rows and agrees with
   it everywhere else — including on `nick-daicos`, the row the residue could not reach.

3. **Internal inconsistency.** `players[0]` is priced at `BASE_REF=2026` and rows 1…803 at
   `BASE_REF=2028`. A board on which a player's price depends on his position in the iteration is not a
   board on a basis; it is a board on an accident. Order-dependence cannot be the intent.

The direction is uniform — **every one of the 96 is board < correct**, by **0.39 % to 9.65 %**, total
**+2,772 (+0.419 %)** on a 662,177 board. The cohort is drafted **2021 (44) / 2022 (37)** plus 15 later
rows, `ND` 70 · `MSD` 12 · `RD` 7 · `PDA` 3 · `SSP` 3 · `PDN` 1. Full table: **`H3_96_rows.csv`**
(key, loop index, draft year, type, pick, games, sibling value, correct as-of-2026 value, delta, %,
`board == BASE_REF_2028` flag, canonical board value).

---

## 5. What is NOT wrong

* **The board of record `a05fe951` is not affected.** It is built canonical, its F1 gate passes
  804/804, and `board == clean` for all 804 rows. Measured, not assumed.
* **The F1 gate is not defective.** It is doing precisely its job: refusing to write a board whose
  values are not the engine's gated `ev()`.
* **M1a's `aebf192` is correct** for the checker it fixes, and its own note is exactly right that
  *"RL_LEGE=0 still replicates the RL_LEGE=0 export byte-for-byte"* — which is why it is a **no-op for
  the sibling**: faithfully replicating the `RL_LEGE=0` export faithfully reproduces the defect.
* **H4's eight stale-sidecar gripes are still not the blocker**, as the recon found.

---

## 6. Why this seat stops here

The only repair that removes the 96 is to re-pin the engine clock **inside the value loop** — for
example `g['BASE_REF']=g['AGE_REF']=2026; g['_pe_clear']()` at the top of each iteration, or closing
the forward calls with a re-pin rather than only clearing `_LENS_FORM`. That is a one-line change to
the **board build**, not to the comparison harness, and it **moves 96 written prices** (+0.39 % to
+9.65 %, +2,772 on the board total). Downstream it moves `balanced_board_md5`,
`release_contract.present_lens_baseline` and its seal, `reference_vector_<md5>.json`,
`forward_vector_<board>.json`, `test_forward_lens_<board>.py`, both board-view bundles and
`sibling_repin_state.json` — the balanced/strict board being, by `sibling_repin`'s own words, *"the
immutable present-lens baseline anchor"*.

Per this seat's order: **a fix that touches the board rather than the comparison is a valuation act
above this seat. HALTING and reporting.** No repair was attempted, no expression was edited, and no
pin was moved.

### What the valuation owner is being asked to rule

1. Whether the corrected basis (clock pinned to the present for every row, which reproduces the board
   of record's own vector 804/804) is the intended one — the evidence says yes, but the price movement
   is the owner's to accept.
2. Whether the repair belongs in `rl_export.py`'s loop (re-pin per row) or in `_merged_recover.ev()`
   (make `ev(p,Y)` pin its own clock before *any* evaluation, so it stops being ambient-state-dependent
   at all). The second is the durable fix and is strictly larger.
3. That the same latent order-dependence sits under the **canonical** board too — it is masked only
   because `RL_LEGE=1` happens to pin `BASE_REF` to 2026. A future posture change or a reordering of
   the loop would expose it there as well.

---

## 7. Method note (reproducible)

Measurements were made by running the real builders against an isolated `git archive` export of the
tree, with the parity gate instrumented **in the scratch copy only** to dump per-player values before
raising. Environment on every run: `PYTHONHASHSEED=0`,
`OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=NUMEXPR_NUM_THREADS=1`.
Build time ≈ 90–150 s per run. The live repo was never written; `/home/user/afl-rl-engine`'s store and
board are byte-unchanged at `cc02567f` / `a05fe951`.
