# FINAL STATE — THE F5 ROUNDING ACT, THE COLUMN-SORT REPAIR, AND THE AGE_REF PROBE

**Owner word:** *"Launch the ready items please."* · **Date:** 2026-08-20 · **Base:** `main` @ `63aa259`

Two acts landed, each with its own prereg, gates and evidence. One read-only probe added mid-flight,
which changed nothing. **Nothing was pushed.** `docs/OPEN_ITEMS_REGISTER.md` was not touched.

---

## 1. THE COMMITS

| # | sha | what |
|---|---|---|
| 1 | `d446f6f` | **PREREG (ACT B)** — the column-sort repair. Before any engine edit. |
| 2 | `4c3dedd` | **ACT B** — the repair: `out_of_round_column.py`, `ui/data/movers.js` |
| 3 | `3c983c3` | **ACT B** — R23 runbook `ERRATUM E6` |
| 4 | `2991740` | **PREREG (ACT A)** — the F5 rounding act. Before any engine edit. |
| 5 | `e6cdec0` | **ACT A** — the seal + the exporter + the board. `7a3f4fe2 → c97a4d9f` |
| 6 | `778cbcf` | **ACT A** — the landing transaction: pins, column, lineage, UI, test pins |
| 7 | *(this)* | evidence tail: the AGE_REF probe, the gate-mode probe, this file |

## 2. FINAL IDENTITIES

| identity | before | after | moved by |
|---|---|---|---|
| **board** | `7a3f4fe23207a29095e6d37408a4b727` | **`c97a4d9f9fa42597f85517c7850d3943`** | **ACT A** |
| **store** | `b745002eb0a0fbb1c34fa44f1ef708d6` | *unchanged* | — |
| **engine_head** | `1867e953cf844d089ab1da68379b1742` | *unchanged* | **neither act** |
| **contract** | `a3c2caf8908f` | **`c5149774b8ec`** | ACT A |
| **balanced_board_md5** | `3970156c8658fc9ecea8089e8b3ecdf1` | *unchanged* | — |
| **config / rl_model / fv / register / v0surf** | — | *all unchanged* | — |
| **as_of_round** | 23 | 23 (held) | — |
| **F5 seal** | `cbb7c431` | **`ccc26a9e`** | ACT A |
| board total | 692,296 / 804 | **692,296 / 804** | — |

**`engine_head` did not move, and that is a finding, not an oversight.** It is
`md5(engine/rl_after/_merged_recover.py)` — measured, not assumed. Act A edits
`engine/rl_after/rl_export.py`, the **exporter**, which no identity pin in `expected_boot.json` or
`release_contract.json` tracks. The valuation engine was not touched, which is exactly why no price
moved. `land_f5_pins.py` **asserts** engine_head does *not* move — the reverse of every prior landing,
deliberately. Act B touched no engine file at all.

---

## 3. ACT A — THE F5 ROUNDING ACT

### What the declared quantity is, in plain terms

The **F5 entrant layer**: the once-a-year value of a whole incoming AFL intake — the 64 national draft
picks at the release-active pick curve, plus the deep tail and the non-draft entry mechanisms — carried
on the `+1`/`+2` forward views as one report-only aggregate. **It is not a player price and not money.**
No club total, pick price, numéraire or store value depends on it.

The defect was that the board stated this one quantity **twice, by two conventions that differ by 1**:
`round(a)+round(b) = 56773` beside `round(a+b) = 56772` — three times over on the board (`_meta`,
`league`, `draftAssetTotals`) and once more in the sealed file. A double-rounding artifact at the seal
boundary, not a ledger miss.

### Premises re-verified before editing

The diagnosis predates the D8 adoption and the R23 advance, so its arithmetic was **recomputed from
first principles on the current tree**: `draft 49594.5606 → 49595`, `mech 7177.7109 → 7178`,
`sum 56772.2715 → 56772`, parts `56773`, residual **exactly 1**. Every figure reproduces. The curve
**payload** md5 is `9729f0c5` in both eras — the pricing basis never moved — which is *why* R23 and D8
did not disturb it. **The runbook's logic applied unchanged.**

### What moved

The complete control→F5 board diff is **ten fields**:

| field | from | to |
|---|---|---|
| `draftAssetTotals['+1'/'+2'].f5_entrant_layer_pvc` | 56772 | **56773** |
| `phantomTotals._meta.entrant_layer_pvc` | 56772 | **56773** |
| `phantomTotals._meta.seal_sha256_8` | `cbb7c431` | **`ccc26a9e`** |
| `phantomTotals.league['1'/'2'].delta` | 56772 | **56773** |
| `phantomTotals.league['1'/'2'].entrantValue` | 56772 | **56773** |
| `phantomTotals.league['1'].withPhantom` *(declared extension)* | 687952 | **687953** |
| `phantomTotals.league['2'].withPhantom` *(declared extension)* | 257524 | **257525** |

**Nothing else.** All **804** players' `v/vM2/vM1/vP1/vP2` and all **198** back rows byte-identical.
Lens 0 held at **692,296** — the k=0 zero-phantom invariant. `ui/data/board_view_public.js` is
byte-identical, which *confirms* it: that bundle carries player values and no board id.

### Predictions vs outcomes

| | prediction | outcome |
|---|---|---|
| A0 | control build reproduces `7a3f4fe2` | **MET** — exactly, so every diff is attributable |
| A1 | dev == canonical byte-for-byte | **MET** — both `c97a4d9f` |
| A2/A3 | 804 players + 198 back rows unmoved | **MET** |
| A4 | ladder/residuals/parts unmoved | **MET** |
| A5 | lens 0 unmoved at 692,296 | **MET** |
| A6 | balanced + store unmoved; engine_head *moves* | **MET on all but the engine_head clause, which was wrong in the prereg** — see §6 |
| A7 | diff == exactly the predicted set | **MET** — 10 fields |
| A8 | `invariant_proof` 26/28 → **28/28** | **MET** — zero FAIL |
| A9 | `r15_ladder_survival_proof` goes green | **SUBSTANCE MET, harness cannot run** — see §6 |
| A10 | `reconciled_to_f5` true *and non-vacuous* | **MET** — proved both directions |
| A11–A15 | column, pins, test pins, suites, gates | **MET** |
| F1–F10 | falsifiers | **all clear** |

### The seal — a declared method deviation

A literal re-run of `seal_structure.py` was **refused, on measurement**: it would have restamped
`store_md5` `d9a24282→b745002e`, `board_balanced_md5` `234c3414→3970156c` and `curve_file_md5`
`0be17c8f→78ad9842`, and re-measured occupancy against a store that has moved three times — a
**RE-COUNT**, which the runbook's cost list excludes and which `rl_export.py` explicitly disclaims.

Instead the artifact was re-emitted under the corrected rule with `total` derived from the seal's own
committed parts. **Result: `entrant_pvc.total` is the only changed field; the occupancy counts and the
whole provenance stamp are byte-identical.** The committed seal was verified to recompute to
`cbb7c431` *before* the hash function was used, and the new seal `ccc26a9e` was **predicted in the
prereg and matched**.

### Two guards that could not fail, made real

* The **`#306 L7` HALT** compared the board's `round(sum)` against the seal's `round(sum)` — the same
  convention on both sides, a number against itself, **structurally blind to this class**. It now
  compares the parts on both sides and checks the seal closes internally.
* **`reconciled_to_f5` was an algebraic tautology** — it reduces to `X == X` and was `True` for any
  inputs, which is why it printed PASS on the very board whose strengthened cross-check was FAILing.
  It now closes against the seal's own total. **Non-vacuity proved in both directions** (`07`).
  *Honest caveat, recorded not glossed:* on a board that renders it will always read `True`, because
  the strengthened halt now stops the mismatch earlier. It is a redundant restatement of a real guard
  rather than, as before, a decoration that could not fail.

`seal_structure.py` now rounds once, sums, and **asserts the triple closes**, so it cannot go latent again.

---

## 4. ACT B — THE COLUMN-SORT REPAIR

`out_of_round_column` ordered columns within an `after_round` by `id` — **alphabetically** — in both the
writer and (via a stable sort) the reader. That placed `the-d8-adoption-20-8` (`5ea978f7`) **before**
`the-landing-20-8` (`a05fe951`), the board it superseded.

**Repair:** one `_order_key` — `(after_round, kind, seq)` — shared by writer and reader. New columns are
stamped with an explicit monotonic `seq`; `registered_at` is optional provenance and deliberately *not*
wall-clock-defaulted, so an append stays reproducible. The eight pre-repair columns **keep their bytes**
— no `seq` was back-filled into a stored history — and are ordered by the closed `_LEGACY_ORDER` table,
sourced from `release_lineage.json`'s append-only register.

**Independent confirmation:** the two repaired `model_changes` boundaries now reproduce register
entry **8** (`a05fe951 → 5ea978f7`) and entry **9** (`5ea978f7 → 1d5c9f7a`) **exactly**.

All 8 predictions met, all 7 falsifiers clear. `previous_point(23)` **unchanged** at
`the-sheet-recut-20-8`, so R23's movers baseline did not move. **Byte-unmoved and verified by md5:** the
board, the store, all three history files, `expected_boot.json`, `release_contract.json`,
`release_lineage.json`. In `ui/data/movers.js` only the derived `points`/`model_changes` blocks moved;
every per-round report and the whole `values` block byte-verbatim. **No value, rank or positional rank
moved anywhere.**

Act A then became the **first column written under the repaired sort** — `the-f5-rounding-20-8`, stamped
`seq` 0, its position recorded rather than won by an alphabetical race.

---

## 5. ACT C — THE BACK-ROWS `AGE_REF=2028` PROBE (read-only)

### VERDICT: **PERSISTS.** The item is **not closable.**

It was **not** washed out by the D8 adoption or the R23 advance, and there was no mechanism by which it
could have been: the H3 repair re-pinned the clock in the **players** loop only. The `back_extra` loop
variant was applied, measured, and **reverted** at H3 time (F1 fired), and no commit has touched that
loop since. It still runs with **no clock re-pin**, entering at `BASE_REF=2026` but **`AGE_REF=2028`**.

**Measured** with one build in a throwaway worktree (the real repo never edited; board byte-unmoved):
fixed-clock `68be10c7` vs live `c97a4d9f` —

* **ACTIVE rows that move: 0 of 804** — the live player board is unaffected.
* **BACK rows that move: 25 of 198**, all **down**, sum **772 → 700** (**−72**).
* `lensConservation` lens −1 and −2 each move **−72**.
* The H3-era named examples reproduce: `charlie-dean` **41 → 39** and `jacob-bauer` **29 → 27**
  exactly; `tyler-sellers` still moves −1 from a re-valued base (21→20 then, 22→21 now).

**26 at H3, 25 now** — stated honestly: the H3 account named only three of its 26 and never listed them
(`H3_96_rows.csv` is the 96 *active* parity rows, a different set), so the one-row difference cannot be
attributed row-by-row. It is consistent with ordinary era movement and is **not** evidence of partial
repair. The full movers list is in `14_actc_ageref_probe.txt` — that is the thing to rule on.

It blocks nothing. It remains a **valuation act on the board of record** needing its own owner word,
and belongs with the in-`ev()` structural cure in the modernisation programme.

---

## 6. DEVIATIONS, MISSES AND THINGS REFERRED — NONE ABSORBED

1. **ORDER: Act B was run first**, though the brief lists F5 first. Declared in Act B's prereg §7: it
   is the smaller, board-neutral act, and running it first meant Act A's column was placed by explicit
   sequence rather than alphabetical coincidence.
2. **A6's `engine_head` clause was WRONG IN THE PREREG.** It predicted engine_head would move "an engine
   file was edited". It does not: engine_head tracks `_merged_recover.py`, and this act edits
   `rl_export.py`. The prereg was corrected **against the tree, not the reverse** — the landing
   instrument now asserts engine_head does *not* move. Named rather than quietly satisfied.
3. **`r15_ladder_survival_proof.py` CANNOT RUN ON THIS TREE.** `KeyError: 'GFWD'` in `rl_model.py` at
   engine-import time. **Proved pre-existing** by running the same proof from a clean worktree at
   `2991740` — before any Act A edit — which fails with the identical traceback. Its F5 assertion was
   lifted verbatim and evaluated against both boards instead: **red before, green after**.
   **Referred, not repaired** — nobody has ruled on it.
4. **THE ONE DECLARED EXTENSION.** The runbook names `league.entrantValue`/`delta`; this act also
   derives `withPhantom = withoutPhantom + entrantValue`. Reason: `delta` **is** `with − without` by
   construction, so moving `delta` alone would have left the league block newly self-contradictory —
   the exact disease being cured. Prereged as an extension, not smuggled. **It is the one line to
   revert if the owner prefers the strictly minimal reading.** The block now closes:
   `with − without == delta == entrantValue == draftValue + freeValue` at both lenses.
5. **THE LINEAGE CHAIN ASSERTION WAS ADAPTED, NOT COPIED.** The R23 seat's strict
   "tail destination == this source" would have falsely halted, and its store leg *did* halt the first
   draft. The gap is the R23 **round advance**, which moves board and store and gets no register entry.
   It is **closed by evidence** — a single movers report must bridge both legs, and R23's does.
   Precedent: register entries 4 and 6 have the same shape.
6. **TWO WEEKLY TEST PINS MOVED** in `ui/tests/movers.test.js` (state `ok`→`bridged`, boundary count
   `8`→`9`), because the *kind* of act that last moved the board changed. The file documents this line
   as having swung both ways twice; this is the third. **Nothing was loosened**: both non-vacuity
   assertions were re-run at the swing and still discriminate in both directions, and all 9 boundaries
   remain anchored to owner-approved records. The F5 proofs themselves were **not** touched — changing
   a proof to accept `56772` was explicitly refused.
7. **`release_contract.f5_entrant_reconciliation` was asserted FROZEN at 77611** and did not move. It
   names the RELEASED baseline under the adoption lane — a different era's number that does *not* track
   the declared layer. A seat reading only the runbook's cost list might have moved it.
8. **The gate-mode probe:** all three `RESEAL_HALT` blockers are now **mechanically clear** (A no longer
   fires because the bake wired the dials default-ON; B repaired in tree by that bake; C self-healed at
   the R23 board sync). **The full book re-seal stays owner-pending and `book_stable_seal.json` was not
   touched** — blocker A's *mechanism* is not its *question*, and ruling that the price-line fork has
   dissolved is the owner's call. Full account in `15_gate_mode_probe.txt`.

## 7. GATES — AFTER EACH ACT

| gate | after ACT B | after ACT A |
|---|---|---|
| `python3 -m acceptance.runner` | **GREEN** 7/7 | **GREEN** 7/7 |
| `python3 release_manifest_check.py` | **PASS** | **PASS** |
| `python3 release_contract.py check` | **PASS** `a3c2caf8908f` | **PASS** `c5149774b8ec` |
| `test_movers_transition.py` | **39/39** | **39/39** |
| `ui/tests/movers.test.js` | **66/66** | **66/66** |
| `invariant_proof.py` | 26/28 (F5 reds standing) | **28/28** |

## 8. OPEN, REFERRED TO THE OWNER

1. **The back-rows `AGE_REF` residue** — persists, 25 rows, movers list in `14`. Needs an owner word.
2. **`r15_ladder_survival_proof.py`** — cannot run (`KeyError: 'GFWD'`), pre-existing, unowned.
3. **The full book re-seal** — mechanically unblocked, but the price-line question is the owner's.
4. **The `withPhantom` extension** — landed as declared; one line to revert if unwanted.
