# PREREG — THE INJURY-SHEET RE-CUT (v790). Committed BEFORE the sheet or the engine is touched (law F6).

**Seat:** R23 advance engine seat · **Date:** 2026-08-20 · **Base:** `main` @ `d02520e`
**Governing documents:** `docs/runbooks/R23_RUNBOOK.md` §4 H2 · the read-only R23 preflight
(`r23_preflight/PREFLIGHT_REPORT.md` §6, `EXECUTION_CORRECTIONS.md` item C) · register v790 (the
remedy) / v798 (the base).

**THE CORRECTIONS OVERRIDE THE RUNBOOK AND THE v797 REGISTER SPEC WHERE THEY CONFLICT.** This prereg
is written to the corrections, and names each place it departs from the runbook.

---

## 0. THE OWNER'S WORD

Given in chat this session, **verbatim**:

> **"All good on the injury sheet. Fine by me."**

That is the approval this act executes. This seat did not create it and does not interpret it.
`docs/OPEN_ITEMS_REGISTER.md` is the supervisor's pen and is **not touched** by this seat.

## 1. WHY THE RE-CUT IS MANDATORY, NOT OPTIONAL

`docs/owner_annotations/SITTER_2026_v1.csv` is the single source of injury truth and a **pinned input**:
its md5, row count and `injured=Y` count are asserted in the engine, and ORDER 42
(`_merged_recover.py`, `_SHEET_*` block) additionally requires **every `injured=Y` row's `games_2026`
to equal the store's 2026 `games` exactly**.

A round advance increments `games` for every listed player. The R23 file the owner sent lists
**exactly two** of the 37 `injured=Y` players — **Harry Armstrong** and **Judson Clarke** — so applying
R23 desynchronises the sheet from the store and **ORDER 42 halts the board regen inside the
transaction**. The runbook rated H2 "a coin flip on the owner's file"; the preflight measured the real
file and it **landed**. Without this act the R23 advance cannot complete.

## 2. WHAT CHANGES — AND THE FIRST DEPARTURE FROM THE WRITTEN SPEC

### 2.1 The sheet: two characters

Column 14 (`injured`), `Y` → `N`, on two rows. Byte length unchanged, CRLF preserved, no other byte moved.

```
line  17  - Harry Armstrong,Richmond,KPF,20,ND,2024,3,11,2026,1,1,never,620,Y,
          + Harry Armstrong,Richmond,KPF,20,ND,2024,3,11,2026,1,1,never,620,N,
line 163  - Judson Clarke,Richmond,SF,23,ND,2021,1,17,2026,2.79,0.307,never,90,Y,
          + Judson Clarke,Richmond,SF,23,ND,2021,1,17,2026,2.79,0.307,never,90,N,
```

### 2.2 The pins: **SIX literals in TWO blocks, not two in one**

> **THE DEPARTURE.** The brief and register v790 name only `_SHEET_MD5` / `_SHEET_ROWS` / `_SHEET_Y`
> (the ORDER 42 block). The preflight found a **second, earlier** pin block — ORDER 41's
> `O41_INJ_MD5` / `O41_INJ_ROWS` / `O41_INJ_Y` — which asserts the same three facts and **halts
> first**. Moving only the ORDER 42 pins leaves ORDER 41 to halt the build before ORDER 42 is reached.
> **All six move in the same commit as the sheet.**
>
> The preflight's line numbers are PRE-D8-adoption and the adoption edited the same file. The pins were
> located by **grepping the pin names**, not by line number; the line numbers below were re-measured
> against `d02520e` and are recorded as observations, not as the locator.

| file:line (`d02520e`) | literal | current | must become |
|---|---|---|---|
| `engine/rl_after/_merged_recover.py:4201` | `O41_INJ_MD5` | `'b26798c35adcd9bda5cef50ff2c884da'` | `'21361291f26d35108b88f92f885c5063'` |
| `engine/rl_after/_merged_recover.py:4202` | `O41_INJ_ROWS` | `219` | `219` (**unchanged**) |
| `engine/rl_after/_merged_recover.py:4203` | `O41_INJ_Y` | `37` | **`35`** |
| `engine/rl_after/_merged_recover.py:5901` | `_SHEET_MD5` | `'b26798c35adcd9bda5cef50ff2c884da'` | `'21361291f26d35108b88f92f885c5063'` |
| `engine/rl_after/_merged_recover.py:5901` | `_SHEET_ROWS` | `219` | `219` (**unchanged**) |
| `engine/rl_after/_merged_recover.py:5901` | `_SHEET_Y` | `37` | **`35`** |

Assertion sites that fire on drift: ORDER 41 `:4214` (md5), `:4219` (rows), `:4225` (Y);
ORDER 42 `:5909` (md5), `:5914` (rows), `:5917` (Y).

**No other engine expression changes. No parameter is added, fitted or targeted. `data/model_config.json`
is not touched.**

## 3. THE NUMERIC PREDICTIONS

### 3.1 The sheet artifact — falsifiable to the byte

| quantity | prediction |
|---|---|
| post-re-cut md5 | **`21361291f26d35108b88f92f885c5063`** |
| size | 15,948 bytes (**unchanged**) |
| data rows | 219 (**unchanged**) |
| `injured=Y` (csv.DictReader, the engine's own reader) | **37 → 35** |
| line endings | CRLF, preserved verbatim |
| bytes that differ | exactly **2** — one `Y`→`N` on line 17, one on line 163 |

**Already verified before this prereg was written, by re-cutting into scratch and hashing:** the value
above is this seat's **own** re-cut, and it is byte-identical to the read-only preflight's independently
constructed `r23_preflight/SITTER_2026_v1_RECUT.csv`. **HALT if the applied re-cut hashes to anything
else.**

### 3.2 Does the re-cut clear H2? — asserted, to be re-proved by the build

Of the 37 currently-`injured=Y` rows, **all 37 agree with store `cc02567f` today** (0 mismatch).
The **2** that R23 lists are exactly the 2 being flipped. The remaining **35** are **not** listed in
R23, so their `games` do not move and they still agree after the advance ⇒ **ORDER 42 passes.**
Name-match assertions (ORDER 41, ORDER 42) are unaffected — the annotated set only shrinks.

### 3.3 The identities

| identity | before (`d02520e`) | prediction |
|---|---|---|
| **board** | `5ea978f7b6a073abb2012f10cccbc3e3` (**B_precut**) | **MOVES** → **B0**, value **COMPUTED FROM THE BUILD**, never typed |
| board total / rows | 693,753 / 804 | rows **804 held**; total moves by the disclosed movers only |
| **engine_head** (`_merged_recover.py`) | `3cfc4325aa323b7f26594cb2a202a976` | **MOVES** — recomputed by the tree's own definition (md5 of the file) |
| **balanced_board_md5** | `a49c155fa20f7084bcaa0d3dceca6cb1` | **MOVES** — **BUILT** by `sibling_repin.py` and derived from the built artifact |
| **contract_sha256** | `7dc087563cda3c17a7a273830729076a97f1edcd81e767bba8f0c6fac6d0599d` | **MOVES** (re-sealed by its writer of record) |
| **store** | `cc02567f80bef39228f25854d121a766` | **UNMOVED** — nothing here writes the store |
| **config_sha256** | `eed19a75f775aeafe4ee5ea4b3990667192d8f90389ad6b0e8318e91062d14c1` | **UNMOVED** — the sheet is a pinned owner input, not a manifest dial |
| `rl_model` / `fv` / `band` / `register` / `q97m` / `v0surf` / `peak_model` / `bust_prior` / `pvc_snapshot` | as pinned | **UNMOVED** |
| **as_of_round** | 22 | **HELD at 22** — no round is applied by this act |
| `data/model_config.json` | — | **NOT TOUCHED** |

### 3.4 The movers — the numbers this prereg is answerable for

Both flipped players leave the injury layer entirely. Measured **against the CURRENT live board
`5ea978f7` / 693,753** (not against the retired pre-D8 board the v790 estimate was cut on):

| key | v now | prediction | basis |
|---|---:|---|---|
| `judson-clarke` | **75** | **DOWN, by roughly 6** (≈ 69) | he currently holds his injury-side price under the D7 shield; de-listing re-prices him on the healthy machinery. v790 measured 55 → 49 under the pre-D8 lever; the direction and rough magnitude are carried, the exact figure is not, because the lever moved beneath it. |
| `harry-armstrong` | **518** | **≈ 0** | already parity-lifted to his healthy value; de-listing should be a no-op or near it. |
| everyone else | — | **small fork-`v`/`fE` ripples possible** | the layer's removal can perturb neighbouring fork sites |

**FALSIFIERS — any one of these is a HALT, not a footnote:**

* **F1** — the applied sheet hashes to anything other than `21361291f26d35108b88f92f885c5063`, or rows ≠ 219, or `injured=Y` ≠ 35.
* **F2** — the rebuilt board does not carry **exactly 804** active rows.
* **F3** — `judson-clarke` does **not** move, or moves **UP**.
* **F4** — `harry-armstrong` moves by **more than ±25** (≈5% of his 518).
* **F5** — any identity in §3.3 marked **UNMOVED** moves — in particular `store` or `config_sha256`.
* **F6** — `as_of_round` is not 22 after the act.
* **F7** — a gate that was green before this act goes red and the red cannot be attributed to a pin
  this act legitimately owns.

**EVERY mover is disclosed by name and delta in the evidence packet — not just the two predicted.**
A mover set that is larger than "two players plus small ripples" is a disclosure obligation, not a
licence to round it away.

## 4. HOW IT IS DONE — writers of record only

1. **Prereg** (this file), committed first, `git commit -- <explicit path>`.
2. **The edit commit:** the sheet **and** all six engine pins, together, `git commit -- <the two paths>`.
   Splitting them would leave the tree at a state where the pinned md5 and the file disagree — a
   guaranteed build halt at whichever of the two commits landed first.
3. **The rebuild:** the accepted disposable FV builder
   (`session_2026-07-20/fv_provenance_remediation/test_fv_provenance._run_build`) via the byte-carried
   `d8_build.py` driver, `PYTHONHASHSEED=0`, BLAS threads pinned to 1, staging into a throwaway dir,
   writing nothing under the repo, strictly sequential, under `tools/build_lock.sh` (single writer).
   **BARE (dev)** and **BARE (canonical)** must agree byte-for-byte, or the manifest and the shipped
   default disagree.
4. **The landing transaction**, each carrier by its writer of record, in the D8 adoption's order:
   board artifacts + `expected_boot` `board`/`engine_head` pins (the C3 pattern) → the out-of-round
   history column (`out_of_round_column.add_column`) → the lineage entry (append-only) →
   `release_contract.restamp_dynamic` + the bake-lane identity restamp → `sibling_repin.py reconcile`
   (**build-and-compare**: the balanced pin moves to a value that was just built) → both UI writers
   (`extract_board_view.py` **then** `round_movers.inject_release_contract`).
5. **The out-of-round column is not optional.** The standing owner rule (2026-07-28,
   `out_of_round_column.py`): *whenever the board moves OUTSIDE a round, write a column at that point*.
   It is also what rule **M0** requires of the R23 movers — the R22→R23 baseline must share
   `as_of_round` with the candidate, so **B0 must exist as a stored point at round 22**. Without it the
   R23 movers would report this re-cut (and D8) as round 23's own work.

## 5. WHAT THIS ACT IS NOT

* It does **not** apply a round. `as_of_round` stays 22 and the ledger stays at 3,086 triples.
* It does **not** re-seal the book. A re-seal is a separate act and is not smuggled into this one.
* It does **not** touch `scores/`, the identity-override file, or `docs/OPEN_ITEMS_REGISTER.md`.
* It does **not** weaken ORDER 41 or ORDER 42. Both guards keep asserting md5 + rows + Y-count + the
  full name match; only the pinned values move, to values this act measured. The runbook's option (b)
  — loosening the check to `store_games >= sheet_games` — was **not** taken: the owner ruled the re-cut.
