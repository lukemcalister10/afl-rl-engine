# PREREG — ACT B: THE COLUMN-SORT REPAIR

**Written and committed BEFORE any engine edit.** Base: `main` @ `63aa259`, live board
`7a3f4fe2` / 692,296 / 804, store `b745002e`, `as_of_round` 23, engine_head `1867e953`,
balanced `3970156c`.

Executed **first** of the two acts (order deviation from the brief, declared in §7).

---

## 1. THE DEFECT, MEASURED ON THE CURRENT TREE

`engine/rl_after/ingestion/out_of_round_column.py`:

* `_register:84` — `cols.sort(key=lambda c: (c['after_round'], c['id']))`
* `selectable_points:67` — sorts by `(after_round, kind)` only; Python's sort is **stable**, so
  out-of-round points inherit the stored list's order, which is the **alphabetical** order above.

`id` is alphabetical, not chronological. Measured on the shipped bundle `ui/data/movers.js`, the
five `after_round=22` columns display as:

```
dob-courier-10-8  <  g1-never-rises-10-8  <  the-d8-adoption-20-8  <  the-landing-20-8  <  the-sheet-recut-20-8
                                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                             WRONG: a05fe951 (THE LANDING) came FIRST and was
                                             SUPERSEDED by 5ea978f7 (THE D8 ADOPTION)
```

**The independent authority is `data/release_lineage.json`'s append-only
`release_transition_register`**, which records the true chain by destination board:

| reg # | source board | → destination board | column |
|---|---|---|---|
| 4 | `6e724cca` | `a672ed3a` | `dob-courier-10-8` |
| 5 | `a672ed3a` | `4b448a82` | `g1-never-rises-10-8` |
| **6** | `88ce647f` | **`a05fe951`** | **`the-landing-20-8`** |
| **8** | **`a05fe951`** | **`5ea978f7`** | **`the-d8-adoption-20-8`** |
| 9 | `5ea978f7` | `1d5c9f7a` | `the-sheet-recut-20-8` |

Register entry 8 proves it: the D8 adoption's **source** is `a05fe951`, the very board the
alphabet places *after* it. The stored display order contradicts the owner-approved lineage.

**Consequence of record (R23 FINAL_STATE §3):** before the R23 advance this left the *retired*
pre-D8 board `a05fe951` as the newest stored point, and turned two `movers.test.js` assertions
red. The R23 seat worked around it by asserting `previous_point` after writing rather than
trusting the alphabet, and **disclosed the defect without repairing it** (out of scope for a
round advance). This act repairs it.

---

## 2. THE REPAIR

**Reader and writer only. The three history files are NOT rewritten.**

1. `_register` stamps every **NEW** column with an explicit monotonic `seq` (and `registered_at`),
   so registration order — chronology — is recorded as data instead of inferred from the alphabet.
2. Ordering becomes `(after_round, kind, seq)`, shared by `_register` and `selectable_points` via
   one function, so writer and reader can never disagree again.
3. **Legacy entries carry no `seq` and are not given one.** They are ordered by an explicit,
   documented `_LEGACY_ORDER` constant whose provenance is the lineage register above. Legacy
   entries sort before `seq`-bearing ones within a round — correct, since all eight were
   registered before this repair.

The three `*_history.json` files stay **byte-identical**: Act B writes no column.

---

## 3. NUMERIC PREDICTIONS

| # | prediction |
|---|---|
| **P1** | After the repair `selectable_points` orders `after_round=22` as `dob-courier-10-8`, `g1-never-rises-10-8`, **`the-landing-20-8`**, **`the-d8-adoption-20-8`**, `the-sheet-recut-20-8` — exactly one adjacent transposition vs today. |
| **P2** | `previous_point(repo, 23)` == `the-sheet-recut-20-8` — **UNCHANGED**. (It sorts last under both conventions; R23's movers baseline must not move.) |
| **P3** | The newest stored point overall stays round **`23`**. |
| **P4** | `model_changes` stays at **8** boundaries; exactly **two** change, and both change *into* agreement with the lineage register: `['g1-never-rises-10-8','the-d8-adoption-20-8']` → `['g1-never-rises-10-8','the-landing-20-8']`, and `['the-d8-adoption-20-8','the-landing-20-8']` → `['the-landing-20-8','the-d8-adoption-20-8']`. After the repair the boundary `['the-landing-20-8','the-d8-adoption-20-8'] → 5ea978f7` reproduces register entry 8 exactly, and `['the-d8-adoption-20-8','the-sheet-recut-20-8'] → 1d5c9f7a` reproduces entry 9 exactly. |
| **P5** | All 8 boundaries stay `owner_approved_record: true`. |
| **P6** | `test_movers_transition.py` **39/39**; `ui/tests/movers.test.js` **66/66** (both are 39/39 and 66/66 at baseline). |
| **P7** | A fresh registration ordering test: registering `zzz-earlier` then `aaa-later` at the same `after_round` in a temp fixture yields display order `zzz-earlier`, `aaa-later` — registration order, **not** alphabet. Under today's code it yields the reverse. |
| **P8** | Gates: `acceptance.runner` **GREEN**, `release_manifest_check.py` **PASS**, `release_contract.py check` **PASS**. |

### BYTE-UNMOVED (the value-bearing set) — md5s pinned at `02_sort_baseline.txt`

| artifact | md5 that must not move |
|---|---|
| `data/rl_build/rl_app_data.json` | `7a3f4fe23207a29095e6d37408a4b727` |
| `engine/rl_after/rl_model_data.json` | `b745002eb0a0fbb1c34fa44f1ef708d6` |
| `engine/rl_after/ingestion/value_history.json` | `5b6d2573d251d3a517d9adbe544114aa` |
| `engine/rl_after/ingestion/rank_history.json` | `19dfd4da2b39e855bd53342c7ea0d21b` |
| `engine/rl_after/ingestion/pos_rank_history.json` | `e767256c37c47852e34027f4a4744747` |
| `data/expected_boot.json` | `16608e90078f6e7814f0920f8981ad74` |
| `data/release_contract.json` | `dcf2257cf52907b6937358a61a72d3b8` |
| `data/release_lineage.json` | `49dc6de19fad5303b1cad8669cae59af` |

**EXPECTED to move:** `out_of_round_column.py` (the repair), `ui/data/movers.js` (the derived
`points`/`model_changes` blocks, rebuilt by the tool of record
`ui/tools/rebuild_movers_derived.py` — the per-round **reports** are carried through
byte-verbatim by that tool's design), `docs/runbooks/R23_RUNBOOK.md` (errata), evidence.

---

## 4. FALSIFIERS — ANY ONE OF THESE HALTS ACT B

* **F1** `the-landing-20-8` does not order before `the-d8-adoption-20-8` after the repair.
* **F2** `previous_point(repo, 23)` changes from `the-sheet-recut-20-8` (R23's movers baseline would move).
* **F3** **Any** artifact in the byte-unmoved table above moves a single byte.
* **F4** The suites are not exactly 39/39 and 66/66.
* **F5** Any `model_changes` boundary loses `owner_approved_record: true`, or the count leaves 8.
* **F6** Any gate goes red, or `rebuild_movers_derived.py` rewrites a per-round **report**.
* **F7** Any player value, rank or positional rank changes anywhere. This act is bookkeeping; it
  reads no board and computes no value. If anything value-bearing moves, **HALT**.

---

## 5. WHAT THIS ACT IS NOT

It does not re-register, re-order or rewrite the eight stored columns in the histories. It does
not move the board. It does not touch valuation. It is a reader/writer ordering repair plus the
regeneration of one derived UI block.

## 6. RUNBOOK ERRATUM

`docs/runbooks/R23_RUNBOOK.md`'s standing warning ("**Assert `previous_point` after writing the
column; do not trust the alphabet**") is updated to record that the sort is repaired, while
keeping the assert-after-write advice — a belt-and-braces check that costs nothing.

## 7. DECLARED DEVIATION

The brief lists the F5 act first. Act B is executed first because it is the smaller and
board-neutral of the two, and because Act A registers a new out-of-round column — which under a
repaired sorter is placed by explicit sequence rather than by luck of its id. Running B first
means A's column is correct by construction rather than by alphabetical coincidence. Both acts
keep their own separate prereg, gates and evidence, as the brief requires.
