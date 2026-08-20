# FINAL STATE — THE R23 ROUND ADVANCE, 2026-08-20

**Base:** `main` @ `280df39` · **Head:** this commit (8 of 8; §1 lists them all) · **UNPUSHED.**

> ## ROUND 23 IS APPLIED.
> **store `cc02567f` → `b745002e` · board `1d5c9f7a` → `7a3f4fe2` · `as_of_round` 22 → 23 ·
> ledger 3,086 → 3,497 · 411 played / 393 DNP over 804 active rows · board total 692,296.**
>
> The R22→R23 movers baseline is **B0 = `1d5c9f7a`**, the post-injury-sheet-re-cut round-22 board.
> The D8 adoption and the sheet re-cut are both on the **round-22 side** of that boundary, so every
> delta on the movers page is what round 23's scores did — rule **M0**, enforced and asserted, not
> assumed.

**Owner words this act executes, verbatim, all given in chat 2026-08-20:**

> *"All good on the injury sheet. Fine by me."* — the re-cut (ACT 1)
> *"the one that isn't Bailey J Williams"* — the WBD binding (ACT 2)
> *"Callum M brown is fine."* — the standing Callum rule stays as it is (ACT 2)

This seat did not create any of them and does not interpret them. `docs/OPEN_ITEMS_REGISTER.md` is the
supervisor's pen and was **not touched**.

---

## 1. THE COMMITS, IN ORDER

| # | act | sha | subject | paths |
|---|---|---|---|---|
| — | *(not this seat's)* | `280df39ca724f038fcd209e374ba2a2a9b123417` | ignore the sibling transaction journal | `.gitignore` |
| 1 | ACT 1 | `b86bc9e6c36b15d4939a4e9c8011a138b145ddd5` | **PREREG** — the injury-sheet re-cut (law F6, before anything is touched) | `docs/evidence/r23_advance_2026-08-20/01_PREREG_SHEET_RECUT.md` |
| 2 | ACT 1 | `024b4585daab140045ef4d4169fadd67b81181f5` | **the edit** — the sheet AND all six pins, one commit | `docs/owner_annotations/SITTER_2026_v1.csv`, `engine/rl_after/_merged_recover.py` |
| 3 | ACT 1 | `230574361395b5d1d58c02c031411380af653269` | **the landing transaction** — pre-R23 board is now `1d5c9f7a` / 693,727 / 804 | `data/expected_boot.json`, `data/release_contract.json`, `data/release_lineage.json`, `data/rl_build/rl_app_data.json`(+`.srcmd5`), `engine/rl_after/rl_app_data.json`(+`.srcmd5`), `engine/rl_after/ingestion/{value,rank,pos_rank}_history.json`, `engine/rl_after/ingestion/sibling_repin_state.json`, `session_2026-07-20/fv_provenance_remediation/test_fv_provenance.py` + `fixtures/forward_vector_1d5c9f7a.json` + `fixtures/reference_vector_e616936e.json` + `test_forward_lens_1d5c9f7a.py`, `ui/data/{board_view_public,board_view_working,movers,movers_transition}.js` |
| 4 | ACT 2 | `27458ada7538911492e7552a9fc81b9ab9c8b7bd` | **the scores + the one binding** — preflight CLEAN 411/411 | `scores/R23.csv`, `engine/rl_after/ingestion/catchup_identity_overrides.json`, `docs/evidence/r23_advance_2026-08-20/08_preflight_r23.txt` |
| 5 | ACT 3/4 | `b7ec6270e6171d41f4463cb4a82c7058078f0bf4` | **the round is applied** + the weekly fixtures + both UI writers | `data/expected_boot.json`, `data/release_contract.json`, `data/season_state.json`, `data/rl_build/rl_app_data.json`(+`.srcmd5`), `engine/rl_after/rl_model_data.json`, `engine/rl_after/rl_app_data.json`(+`.srcmd5`), `engine/rl_after/ingestion/{applied_rounds_ledger,finalization_state,value_history,rank_history,pos_rank_history,sibling_repin_state}.json`, `.../finalization_journal.jsonl`, `.../movers/movers_R23.{json,csv}`, `.../.weekly_txn/txn_catchup_r23/{journal.jsonl,manifest.json}`, `.../test_movers_transition.py`, `ui/tests/movers.test.js`, `session_2026-07-20/fv_provenance_remediation/test_fv_provenance.py` + `fixtures/forward_vector_7a3f4fe2.json` + `fixtures/reference_vector_3970156c.json` + `test_forward_lens_7a3f4fe2.py`, `ui/data/{board_view_public,board_view_working,movers}.js` |
| 6 | ACT 5 | `01355d24b4df7f05deedb2360e06e3c1b3d6d662` | **the runbook errata** — five corrections, three of them would have halted the advance | `docs/runbooks/R23_RUNBOOK.md` |
| 7 | ACT 7 | `11c7d63f0e9527c50d2e3fb605d4123a12cc5ed5` | the evidence packet | `docs/evidence/r23_advance_2026-08-20/*` |
| 8 | ACT 7 | *(this commit)* | FINAL_STATE names commit 7's sha | `docs/evidence/r23_advance_2026-08-20/FINAL_STATE.md` |

*(Commit 7's sha cannot exist inside the file it commits, so commit 8 fills it in — the only thing
commit 8 does. `git log` is the authority; this table is a convenience.)*

Every commit used `git commit -- <explicit paths>` (with `git add -- <explicit paths>` for new files
only). No bare `git commit`, no `git add -A`, no sweep. **Nothing pushed. No tag.**

**Disclosed: the base moved by one commit under this seat.** `280df39` (`.gitignore`, another seat,
09:27:28) landed between this seat's first read of `main` at `d02520e` and its prereg at 09:33:44. It
is not this seat's commit, it touches nothing this advance touches, and it is recorded rather than
quietly absorbed into "the base".

---

## 2. EVERY IDENTITY, BEFORE → AFTER

`B_precut` = the D8 adoption board this act started from. `B0` = the post-re-cut round-22 board and the
R22→R23 movers baseline. `B_final` = the round-23 board of record.

| identity | before (`280df39`) | after ACT 1 (`2305743`) | after ACT 3 (`b7ec627`) | |
|---|---|---|---|---|
| **board** | `5ea978f7b6a073abb2012f10cccbc3e3` **(B_precut)** | `1d5c9f7a3898c7cc62d0e91787ee2606` **(B0)** | **`7a3f4fe23207a29095e6d37408a4b727`** **(B_final)** | MOVED twice |
| board total / rows | 693,753 / 804 | 693,727 / 804 (−26) | **692,296 / 804** (−1,431) | |
| **store** | `cc02567f80bef39228f25854d121a766` | *same* | **`b745002eb0a0fbb1c34fa44f1ef708d6`** | MOVED **only** at the advance |
| **engine_head** (`_merged_recover.py`) | `3cfc4325aa323b7f26594cb2a202a976` | **`1867e953cf844d089ab1da68379b1742`** | *same* | MOVED **only** at the sheet-pin commit — exactly as the brief required |
| **balanced_board_md5** | `a49c155fa20f7084bcaa0d3dceca6cb1` | `e616936ef9be3fe55b37d4c5497093ac` | **`3970156c8658fc9ecea8089e8b3ecdf1`** | MOVED twice, **BUILT** both times |
| **contract_sha256** | `7dc087563cda3c17a7a273830729076a…` | `b3728affb8b2…` | **`a3c2caf8908f25ec45e2e637b26e13590f365e6d5baaf8ac9185ca3ab23cf6cf`** | MOVED twice (re-sealed by its writer) |
| **as_of_round** | 22 | 22 (**HELD**) | **23** | |
| **config_sha256** | `eed19a75f775aeafe4ee5ea4b3990667192d8f90389ad6b0e8318e91062d14c1` | *same* | *same* | **UNMOVED** |
| `rl_model` | `6fe7c4155866d80e8045bed2d3bf2802` | *same* | *same* | UNMOVED |
| `fv` | `6e9a370e5970c5aefa859858070f4c3420f0177b4698d6fac90bd08bf1780346` | *same* | *same* | UNMOVED |
| `band` | `34faa8659cc8f19794f5cb9584fa19b2` | *same* | *same* | UNMOVED |
| `register` (LTI) | `652d83e87780e415a01a2de6d8b3cc57` | *same* | *same* | UNMOVED |
| `q97m` | `cfdc73216c099e5e8f1fda3968f31c00` | *same* | *same* | UNMOVED (FROZEN) |
| `v0surf` | `5dd34ca82735f5c8f021b1c7320df8f8` | *same* | *same* | UNMOVED |
| `peak_model` / `bust_prior` / `pvc_snapshot` | as pinned | *same* | *same* | UNMOVED |
| `data/model_config.json` | — | — | — | **NOT TOUCHED** |
| **injury sheet** | `b26798c35adcd9bda5cef50ff2c884da` (219 rows, 37 Y) | **`21361291f26d35108b88f92f885c5063`** (219 rows, **35** Y) | *same* | MOVED once |
| ledger | 3,086 triples | 3,086 (**HELD**) | **3,497** (+411, 0 duplicates) | |
| histories | rounds `[14…22]` | `[14…22]` + column `the-sheet-recut-20-8` | **`[14…23]`** | |
| lineage register | 9 entries | **10** (entry 10 = the re-cut, boundary `["22","the-sheet-recut-20-8"]`) | 10 (**a round advance earns no entry**) | |

**`engine_head` moved at exactly one commit and nowhere else** — `024b458`, the six-pin edit. The
advance itself touches no engine file, and the manifest, the contract and the UI stamp all agree on
`1867e953` afterwards.

**`config_sha256` is UNMOVED and that is the safety property, not an oversight.** The injury sheet is a
**PINNED OWNER INPUT** asserted by md5/rows/Y-count inside the engine, not a manifest dial. Moving
`data/model_config.json` would have destroyed the property that a canonical build carries no `RL_` name
for it. **Canonical mode accepted the re-cut**: the BARE canonical build was **byte-identical** to the
BARE dev build (1,223,688 bytes).

### UI bundle identities (after ACT 3, both writers)

| carrier | value |
|---|---|
| `board_view_working.stamp.board_md5` / `.board` / `.srcmd5` | `7a3f4fe23207a29095e6d37408a4b727` |
| `.stamp.store_md5` / `.stamp.store` | `b745002eb0a0fbb1c34fa44f1ef708d6` / `b745002e` |
| `.stamp.balanced_board_md5` | `3970156c8658fc9ecea8089e8b3ecdf1` |
| `.stamp.engine` / `.stamp.config` / `.stamp.register` | `1867e953` / `eed19a75f775` / `652d83e8` |
| `.stamp.asOfRound` / `.stamp.release.as_of_round` | **23** / **23** |
| `.stamp.release.balanced_board_md5` | `06d8af60b679a12db07c064c60c065f9` — **correctly unmoved**: `round_movers.release_identity` reads it from `release_lineage.json`'s frozen present-lens baseline, not from `expected_boot`. Pre-existing and by design. |
| `ui/data/movers.js` | latest report **R23**, `rebuild_movers_derived.py --check` exit 0 |
| `ui/data/movers_transition.js` | 10 register entries mirrored, `--check` exit 0 |

---

## 3. ACT 1 — THE SHEET RE-CUT

**Why it was mandatory.** ORDER 42 pins every `injured=Y` row's `games_2026` to the store's 2026
`games`. A round advance increments `games` for every listed player. The owner's real R23 lists exactly
**two** of the 37 injured-marked players — `harry-armstrong` and `judson-clarke` — so applying R23
would have desynchronised the sheet and halted the board regen **inside** the transaction. The runbook
rated H2 "a coin flip on the owner's file". It landed.

**The edit, against the prereg's predictions.** md5 `b26798c3…` → **`21361291f26d35108b88f92f885c5063`**
— **MATCH**. 15,948 bytes and 219 rows unchanged, CRLF preserved, `injured=Y` **37 → 35**, and
**exactly two bytes differ** (offsets 1,258 and 11,836 — one `Y`→`N` on line 17, one on line 163). The
re-cut was built independently by this seat and is byte-identical to the read-only preflight's.

**Six pins in two blocks, located by GREPPING THE PIN NAMES** (the preflight's line numbers are
pre-D8-adoption and the adoption edited the same file):

| block | literal | before → after |
|---|---|---|
| ORDER 41 (**halts first**) | `O41_INJ_MD5` / `O41_INJ_ROWS` / `O41_INJ_Y` | `b26798c3…`→`21361291…` / 219→219 / **37→35** |
| ORDER 42 | `_SHEET_MD5` / `_SHEET_ROWS` / `_SHEET_Y` | `b26798c3…`→`21361291…` / 219→219 / **37→35** |

**Neither guard was weakened.** Both still assert md5 + rows + Y-count + the full name match; only the
pinned values moved, to values this act measured. The runbook's option (b) — loosening the compare to
`store_games >= sheet_games` — was **not** taken, because the owner ruled the re-cut.

**The build.** The accepted disposable FV builder (`test_fv_provenance._run_build`) via the byte-carried
`d8_build.py` driver, `PYTHONHASHSEED=0`, BLAS pinned to 1, throwaway staging, nothing written under the
repo, strictly sequential, one writer under `tools/build_lock.sh`. **BARE dev** and **BARE canonical**
both produced `1d5c9f7a3898c7cc62d0e91787ee2606` and are **byte-identical**.

### The movers, B_precut → B0 — EXACTLY ONE OF 804

| key | name | club | before | after | delta |
|---|---|---|---:|---:|---:|
| `judson-clarke` | Judson Clarke | Richmond | 75 | **49** | **−26** |
| `harry-armstrong` | Harry Armstrong | Richmond | 518 | 518 | **0** — UNMOVED |

803 of 804 rows byte-identical. **PICK 1 numéraire 3,000, unmoved.** Board total 693,753 → 693,727.

### THE PREDICTION ACCOUNT, HONESTLY

The prereg predicted `judson-clarke` **DOWN by roughly 6** and `harry-armstrong` **≈ 0**.

* **Armstrong: exact.** 0.
* **Clarke: the DESTINATION was exact and the DELTA was not.** v790 predicted he would land on **49**,
  and he landed on **49**. But the delta is **−26**, not −6, because v790 measured his *before* value
  at 55 on the pre-D8 board, and the D8 adoption had since lifted his **injury-shielded** price to 75
  while his **healthy** price stayed at 49. Direction and destination held; the carried delta was
  **stale in its before-value**.
* **No falsifier fired.** F1 (sheet md5/rows/Y) PASS · F2 (804 rows) PASS · F3 (clarke moves DOWN)
  PASS · F4 (armstrong within ±25) PASS · F5 (nothing on the must-not-move list moved) PASS ·
  F6 (`as_of_round` still 22) PASS · F7 (no unattributable gate red) PASS.
  The magnitude miss is written down rather than rounded away.

### The out-of-round column — and a pre-existing defect it exposed

Standing owner rule 2026-07-28: whenever the board moves outside a round, write a column. Written by
the writer of record `out_of_round_column.add_column`, 804 points into each of the three histories:
**`the-sheet-recut-20-8`**, `after_round` 22, board `1d5c9f7a`.

**It is also what rule M0 requires of the advance.** `round_finalize` builds the round-23 report against
`round_movers.previous_point(repo, 23)` — the stored point immediately before round 23 — so B0 had to
exist as a point at round 22 or the round-23 movers would have reported the D8 adoption and this re-cut
as round 23's own work.

**DISCLOSED, PRE-EXISTING, NOT REPAIRED HERE.** `out_of_round_column._register` sorts columns by
`(after_round, id)` — **alphabetically**, not chronologically. That left `the-landing-20-8`
(`a05fe951`, the **retired** pre-D8 board) sitting *after* `the-d8-adoption-20-8` that superseded it,
so before this act the newest stored point was **not** the board the app was serving. Repairing the sort
is an engine change and is **out of scope for a round advance**; the defect is written down in the
runbook errata instead. Its *consequence* for this act was handled: `the-sheet-recut-20-8` sorts after
all four, and `register_recut_column.py` **asserts the resulting `previous_point`** rather than trusting
the alphabet.

### Lineage

Entry **10**, boundary `["22","the-sheet-recut-20-8"]`, 42,622 → 50,032 bytes. Append-only **proven**:
9 prior entries byte-verbatim, round-trips at `indent=1` before and after, top-level present-lens
baseline `06d8af60` asserted **UNMOVED**, and the tail chain continuous on **both** store and board
(register tail `destination.board` `5ea978f7` == this entry's `source.board`). Both sides **re-hashed** —
source from a checkout of `b86bc9e`, destination from the live tree — each checked against that tree's
own `expected_boot.json`. Nothing typed in.

### Sibling

`sibling_repin.py reconcile`, **build-and-compare**, under the build lock. 9 committed targets. `verify`
**8 fails → 0**, `ok: true`. The **H4 residual** ("sidecar `contract_sha256` != live seal") **self-cleared
in the transaction exactly as H4 said it would**; the sidecar was never hand-edited.

---

## 4. ACT 2 — THE SCORES AND THE ONE BINDING

`docs/inputs/incoming/R23.csv` → `scores/R23.csv`, **byte-identical** (`cmp` clean).
md5 **`f4849bc4933801e80228bfc0e29e0c65`** (verified *before* the copy) ·
sha256 `e3d5410e0e57a9251cf94a9cf2d20daa63f1255f6551ba497e3cd89a5ce77c40` · 7,279 bytes · 412 lines
(1 header + 411 data) · header `Player,2026 R23` · **CRLF** · **encoding `cp1252`**, 16 raw `0xA0`
bytes, strict UTF-8 fails at byte 43. Within spec; the runbook's `enc=utf-8` expectation was wrong and
is corrected in ACT 5. **Nothing was cleaned up, re-encoded or normalised.**

**BAILEY WILLIAMS — a NEW entry, not an extension.**
`{"name": "Bailey Williams WBD", "rule": "map_all", "stable_key": "bailey-williams-wb",
"applies_to_rounds": [23]}`, owner word *"the one that isn't Bailey J Williams"* recorded verbatim in
the entry's `reason`. The runbook's §3-step-2 recipe (extend `overrides["Bailey Williams"]`) **does not
work** — `IdentityOverrides._by_name` is keyed by the **exact** display string and `resolve()` looks it
up on the **raw** name, so the `Bailey Williams` rule is never consulted for a row reading
`Bailey Williams WBD`. The preflight simulated that recipe **still halting**. It also **honours H5**:
the R20 retirement of the bare-name rule stands, because this export does not collapse the two names —
`Bailey J. Williams` (125) resolves unaided to `bailey-williams-wc`. There is no bare `Bailey Williams`
row, so the binding creates **no duplicate stable key**.

**CALLUM BROWN — TOUCHED NOTHING, ON PURPOSE.** The v797 spec's `callum-m-brown` **is not a key in the
store**. The store holds `callum-brown-ire` (`Callum M. Brown`, GWS, **active**) and a **retired** bare
`callum-brown`. A standing **unscoped** `map_all` override already binds the name correctly. Because
`_by_name` is a dict keyed by name, writing the v797 binding would have **overwritten** the working rule
and halted with `override-target-invalid` — the preflight simulated exactly that. The diff on
`catchup_identity_overrides.json` is **insertions only**.

**Preflight — read-only, wrote nothing, stopped itself:**

```
R23  enc=cp1252  listed/played=411  resolved=411  listed-zero=0  absent/DNP=393  sha256 e3d5410e0e57
     identity override: Callum M. Brown -> callum-brown-ire   (score 90, owner-override:map_all)
     identity override: Bailey Williams -> bailey-williams-wb (score 69, owner-override:map_all)
PREFLIGHT CLEAN — every name resolves to a stable identity; no duplicate/ambiguous.
NOT APPROVED — nothing applied.
```

411 + 393 = 804. Exactly the counts the read-only preflight predicted in simulation.

---

## 5. ACT 3 — THE ADVANCE

**Invocation** — the runbook's own, exactly, `--file` not `--dir`:

```
INGEST_SCORE_APPLY_ARMED=1 INGEST_SCORE_APPLY=R23-2026-08-20-owner-approved \
python3 tools/round_entry/round_entry.py catchup --file 23=scores/R23.csv --approve
```

under `tools/build_lock.sh`, single writer. `RL_BUILD_LOCK_HELD` was dropped from the **child**
environment only — the lock exports it and `config_manifest.enforce()` rejects any unknown
`RL_`-prefixed var as a model override, so a canonical-mode build launched from inside the lock would
halt. The lock stayed held by the shell's fd throughout.

**The apply line:**

```
R23  store cc02567f->b745002e  board 1d5c9f7a->7a3f4fe2  players=411  guard5=True
     hist=[14…23]  final=FINALIZED  movers->UI=804
```

**The journal — the clean five-line shape** (contrast R20's two `FINALIZATION_INCOMPLETE` and three
`force:true`): `CORE_COMMITTED (board_md5_after 7a3f4fe2, txn_catchup_r23, reconciled:false)` →
`STATUS FINALIZING` → `FINALIZE_BEGIN (force:false, historical:false)` → `STATUS FINALIZED` →
`FINALIZED (injected:804, movers_json: movers_R23.json)`. No exit-6, no `repair`, no `recover`;
`scan_incomplete()` was `[]` before and after.

**ADVANCE-REPIN.** The balanced sibling and the FV reference vector moved **inside** the transaction by
`staged_apply._stage_sibling`'s build-and-compare, in the same commit as the store — never from a
supplied constant. New append-only artifacts: `forward_vector_7a3f4fe2.json`,
`reference_vector_3970156c.json`, `test_forward_lens_7a3f4fe2.py`. Every prior vector preserved.
`sibling_repin.py verify`: `ok: true`, 0 fails.

### The weekly round-pin fixtures — hand-pins the transaction does not own

Moved in the advance's own commit and disclosed, as R22 did with the same two files.

| file | pin | before → after |
|---|---|---|
| `test_movers_transition.py` | manifest `as_of_round` | 22 → **23** |
| `test_movers_transition.py` | future-append fixture | R23 → **R24** (and its conflict-guard negative, `fake22` → `fake23`) |
| `ui/tests/movers.test.js` | production bundle | R15–R22 / eight reports → **R15–R23 / nine reports** |
| `ui/tests/movers.test.js` | lineage state | `bridged` → **`ok`** |
| `ui/tests/movers.test.js` | out-of-round boundary count | 6 → **8** |

**Two of those were ALREADY RED before this advance, and one cleared on its own merits.**

* The **boundary count** was red at 7-vs-6: **THE D8 ADOPTION wrote its boundary and its owner-approved
  lineage record but did not bump this counter.** This act absorbs that increment **and names it
  separately** from its own (`the-sheet-recut-20-8`), rather than folding two causes into one number.
* The **lineage state** was red with `[false, "mismatch"]` — caused by the alphabetical column sort
  described in §3, which left the retired pre-D8 board as the newest stored point. Round 23's own
  column put the live board back at the end, so the red cleared **because the tree got healthier**, not
  because a pin was moved to meet it. `ok` is the direct-lineage branch: the latest **round** report must
  terminate on the loaded board, which is exactly what a round advance makes true.
* **Nothing was loosened.** Both non-vacuity assertions around the lineage state still pass in both
  directions, and "EVERY boundary anchored to an owner-approved record" passes **8 of 8**.

Result: `test_movers_transition.py` **39/39** (was 38/39) · `ui/tests/movers.test.js` **66/66** (was 62/66).

### Deviation, disclosed: the generator-side board copy

`engine/rl_after/rl_app_data.json` + `.srcmd5` were **synced by hand** to the published board. The
transaction publishes only to `data/rl_build/` (`round_apply.py:139-141`), and the R22 advance left the
generator copy stale with every gate green — so it is **not** a carrier this transaction owns. It was
synced anyway for two reasons, **neither of them a gate**: THE BAKE `48ec96f` and THE D8 ADOPTION both
moved the pair in lockstep, and **this seat moved it itself at ACT 1** — leaving it would have left a
file this session wrote pointing at a board this session superseded. It is a byte-copy of the published
board and of the transaction's own sidecar; no new claim is made.

### Not moved, and correctly

* `data/release_lineage.json` — a round advance is **not** an out-of-round move and earns no entry. The
  register tail correctly remains the ACT 1 boundary at round 22.
* `ui/data/club_valuation.js` — **skipped by design**: `round_finalize.py:340` emits
  `'club_valuation': 'SKIPPED (Track A owns the club-valuation curve)'`.
* `ui/data/ownership.js` — written by `ui/tools/ingest_inputs.py` from `docs/inputs/`, not by an advance.

Both of the last two are named in the runbook's expected-mover list; that list is stale and is corrected
in ACT 5.

---

## 6. ACT 4 — THE MOVERS PAGE

**Path: `docs/evidence/r23_advance_2026-08-20/MOVERS_R23.html`** (193,832 bytes, 804 rows,
md5 `2b67925c2fb4f47bf3c3f53e58689761`; `_base.css` sits beside it).

Rendered through `ui/templates` under the layout law — **a seat injects data, a seat never injects
layout**. `slots.validate('movers', …)` returned **NO PROBLEMS**: the template fits. This is the **first
genuinely fitting live use** of `ui/templates/movers.html`. The D8 pricing seat tried it and reported
honestly that it did not fit a **lever** comparison (no age column; `played` has no honest value across
a dial; `previous_round == as_of_round`). All three objections are about a dial-shaped comparison in a
round-shaped schema. **This is a round boundary**, so `played` and `score` are facts of it and
`previous_round != as_of_round`. `score` — the one declared-nullable slot — is passed as `slots.ABSENT`
for the 393 who did not play, which is the honest use of the sentinel.

**Both UI writers ran, in order**: `ui/tools/extract_board_view.py` (which drops `stamp.release`) **then**
`round_movers.inject_release_contract(bundle, root, 23)`. The embedded board identity reads back
`7a3f4fe2` and the release block is present. Evidence: `10_ui_writers_r23.txt`.

**Rule M0, asserted rather than assumed** (`12_lineage_season_state.txt`):
`previous_point(repo, 23)` == `the-sheet-recut-20-8`; the movers report's `previous_round` **is** that
point; that point's `after_round` is **22**; its board is **B0 `1d5c9f7a`**. So the D8 adoption and the
sheet re-cut are both on the round-22 side and **every delta on the page is round 23's scores**.

**Summary of the page:** 804 players · 411 played, 393 did not · **686 moved (221 up, 465 down)** ·
board total 693,727 → 692,296 (**−1,431**).

### TOP 20 R23 MOVERS (by value gain)

| # | player | club | pos | v before → after | Δ | Δ% | R23 score |
|---:|---|---|---|---:|---:|---:|---:|
| 1 | Errol Gulden | Sydney | Mid | 6,506 → 7,075 | **+569** | +8.8% | **151** |
| 2 | Isaac Heeney | Sydney | Mid | 3,436 → 3,958 | **+522** | +15.2% | **169** |
| 3 | Izak Rankine | Adelaide | Fwd | 4,405 → 4,819 | **+414** | +9.4% | **157** |
| 4 | Dyson Sharp | Essendon | Fwd | 2,879 → 3,232 | **+353** | +12.3% | 86 |
| 5 | Lachlan Ash | GWS | Def | 5,456 → 5,763 | **+307** | +5.6% | **144** |
| 6 | Levi Ashcroft | Brisbane | Mid | 3,394 → 3,686 | **+292** | +8.6% | **140** |
| 7 | Jordon Sweet | Port Adelaide | Ruck | 2,093 → 2,379 | **+286** | +13.7% | **145** |
| 8 | Jordan Clark | Fremantle | Def | 3,082 → 3,318 | **+236** | +7.7% | 114 |
| 9 | Kade Chandler | Melbourne | Fwd | 863 → 1,091 | **+228** | +26.4% | **136** |
| 10 | Aaron Cadman | GWS | Key Fwd | 1,839 → 2,056 | **+217** | +11.8% | 89 |
| 11 | Miles Bergman | Port Adelaide | Def | 977 → 1,190 | **+213** | +21.8% | 118 |
| 12 | Mitchito Owens | St Kilda | Key Fwd | 1,973 → 2,180 | **+207** | +10.5% | 113 |
| 13 | Samuel Swadling | Collingwood | Mid | 749 → 954 | **+205** | +27.4% | 114 |
| 14 | Oliver Florent | Carlton | Def | 788 → 991 | **+203** | +25.8% | 128 |
| 15 | Connor Idun | GWS | Def | 2,063 → 2,256 | **+193** | +9.4% | 134 |
| 16 | Max Hall | St Kilda | Fwd | 2,184 → 2,346 | **+162** | +7.4% | **181** (top score of the round) |
| 17 | Jack Graham | West Coast | Fwd | 738 → 893 | **+155** | +21.0% | 108 |
| 18 | Zach Reid | Essendon | Key Def | 921 → 1,067 | **+146** | +15.8% | 106 |
| 19 | Harvey Thomas | GWS | Fwd | 2,022 → 2,163 | **+141** | +7.0% | 94 |
| 20 | Daniel Turner | Melbourne | Key Def | 1,395 → 1,534 | **+139** | +10.0% | 94 |

### TOP 20 R23 FALLERS

| # | player | club | pos | v before → after | Δ | Δ% | R23 score |
|---:|---|---|---|---:|---:|---:|---:|
| 1 | Willem Duursma | West Coast | Mid | 4,225 → 3,720 | **−505** | −11.9% | 20 |
| 2 | Luke Davies-Uniacke | North Melbourne | Mid | 3,948 → 3,615 | **−333** | −8.4% | 64 |
| 3 | Sam Berry | Adelaide | Mid | 3,661 → 3,387 | **−274** | −7.5% | 38 |
| 4 | Christian Petracca | Gold Coast | Fwd | 2,026 → 1,796 | **−230** | −11.3% | 34 |
| 5 | Nicholas Martin | Essendon | Fwd | 4,288 → 4,061 | **−227** | −5.3% | **DNP** |
| 6 | Will Day | Hawthorn | Mid | 2,284 → 2,071 | **−213** | −9.3% | 58 |
| 7 | Connor MacDonald | Hawthorn | Fwd | 2,585 → 2,380 | **−205** | −7.9% | 40 |
| 8 | Peter Wright | Essendon | Key Fwd | 1,585 → 1,386 | **−199** | −12.6% | 39 |
| 9 | Lachie Neale | Brisbane | Mid | 2,314 → 2,125 | **−189** | −8.2% | 65 |
| 10 | Zachary Merrett | Essendon | Mid | 2,547 → 2,368 | **−179** | −7.0% | 72 |
| 11 | Jack Whitlock | Port Adelaide | Key Fwd | 994 → 823 | **−171** | −17.2% | 20 |
| 12 | Touk Miller | Gold Coast | Fwd | 2,271 → 2,109 | **−162** | −7.1% | 55 |
| 13 | Luke Jackson | Fremantle | Ruck | 9,417 → 9,265 | **−152** | −1.6% | 111 |
| 14 | Isaac Quaynor | Collingwood | Def | 603 → 455 | **−148** | −24.5% | 56 |
| 15 | Harvey Langford | Melbourne | Mid | 2,470 → 2,327 | **−143** | −5.8% | 50 |
| 16 | Jobe Shanahan | West Coast | Key Fwd | 1,438 → 1,298 | **−140** | −9.7% | 28 |
| 17 | Kysaiah Pickett | Melbourne | Fwd | 4,017 → 3,878 | **−139** | −3.5% | 70 |
| 18 | Beau Addinsall | Gold Coast | Mid | 1,310 → 1,172 | **−138** | −10.5% | 28 |
| 19 | Josh Worrell | Adelaide | Def | 3,240 → 3,106 | **−134** | −4.1% | 48 |
| 20 | Mattaes Phillipou | St Kilda | Fwd | 2,019 → 1,885 | **−134** | −6.6% | 37 |

`Nicholas Martin` is the one **DNP** in either table: he was not in the file, so nothing was recorded and
no game was added — his fall is the standing decay of an unplayed round, not a submitted score.

---

## 7. THE GATES

| gate | verdict |
|---|---|
| `python3 -m acceptance.runner` | **GREEN** — 7 checks, **PASS 7 / FAIL 0 / BLOCKED 0 / RULED-RED 0** |
| `python3 release_manifest_check.py` | **PASS** — 40 carrier fields across 8 identities and 7 files: **38 coherent, 0 incoherent**, 2 sealed-lag |
| `python3 release_contract.py check` | **PASS** — contract `a3c2caf8908f` |
| boot-store Guard 5 | **PASS** — store `b745002e` == pinned `b745002e` |
| six-way store coherence | **PASS** |
| `config_manifest` | **PASS** — hash `eed19a75f775`, 84 vars |
| `ruling_config` | **PASS** |
| `doc_lint` | **PASS** — 0 FAIL, 0 WARN |
| `sibling_repin.py verify` | **`ok: true`, 0 fails** |
| `test_movers_transition.py` | **39 / 39 PASS** |
| `ui/tests/movers.test.js` | **66 / 66 PASS** |
| `generate_movers_transition.py --check` | exit 0 — 10 register entries mirrored |
| `rebuild_movers_derived.py --check` | exit 0 — latest report R23 |
| round-23 lineage / season_state coherence | **COHERENT — 0 failures** (`12_lineage_season_state.txt`) |

**No check was weakened and no acceptance pin had to move.** The 2 **sealed-lag** stamps are the
pre-existing, reported-never-gating freeze-lag on `data/book_stable_seal.json` (`store_md5` sealed
against `cb38ef11`, `head_md5` against `5ac6780f`). **THE BOOK IS NOT RE-SEALED** — a re-seal is a
separate act and was not smuggled into this one.

**H6 (the F5 entrant-layer off-by-one, `49595 + 7178 = 56773` vs declared `56772`) is still open and
still re-fires on the rebuilt board.** It is a double-rounding artifact, it does not gate, and it is
**not** round-advance damage. Labelled, as the runbook asked, not fixed here.

**Two of this seat's own assertions were wrong and were corrected against the tree, never the reverse**
(the D8 seat's precedent, kept). The round-23 coherence checker first read `len(applied_rounds_ledger
.json)` and got 3, because the ledger is a dict whose triples live under `applied`; and it asserted a
continuous store chain across **all ten** lineage entries, which is not the law — entry 0 is the ITEM 408
pointer stub with no boards, and applied rounds legitimately move the store between out-of-round entries.
Both were re-checked against their real sources and both pass. Recorded because a seat that silently
fixes its own failed assertion is indistinguishable from one that bends a result.

---

## 8. DEVIATIONS FROM THE BRIEF, AND WHY

1. **The prereg's `judson-clarke ≈ −6` was wrong in magnitude (actual −26).** §3 gives the full account:
   the destination (49) was exact and the direction held; the carried delta was stale in its
   before-value because D8 had moved his injury-shielded price. No falsifier fired. Disclosed, not
   rounded away.
2. **`engine/rl_after/rl_app_data.json` + `.srcmd5` were synced by hand** beyond the carriers the
   advance transaction owns. Reasoned and disclosed in §5.
3. **One comment was restamped inside the six-pin commit.** The ORDER 41 block read "name match asserted
   37 of 37", which the pin beneath it now contradicts; corrected to 35 of 35, with the re-cut and the
   two-block warning recorded there. No expression other than the six literals changed.
4. **The `ui/tests/movers.test.js` boundary count absorbed an increment this act did not create** — the
   D8 adoption's un-bumped `the-d8-adoption-20-8`. Named separately from this act's own increment rather
   than folded into one number.
5. **The alphabetical out-of-round column sort was NOT repaired.** It is a real, pre-existing defect that
   made the newest stored point the retired pre-D8 board. Repairing it is an engine change and is out of
   scope for a round advance; it is written into the runbook errata and its consequence for this act was
   handled by asserting `previous_point` after the write.
6. **`engine/rl_after/ingestion/.weekly_txn/txn_catchup_r23/` IS committed** (journal + manifest), because
   R15–R22 all are. The **sibling** transaction dir stays untracked — `.gitignore` now says so
   (commit `280df39`, another seat).
7. **The base moved by one commit under this seat** (`280df39`). Recorded in §1 rather than absorbed.

---

## 9. THE TREE

Committed and clean. **UNPUSHED, no tag, no promote.** `docs/OPEN_ITEMS_REGISTER.md` untouched — it is
the supervisor's to pen.
