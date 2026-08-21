# R23 RUNBOOK — the round-23 advance, rehearsed

> ## ERRATA — applied 2026-08-20 BY THE SEAT THAT EXECUTED THE ADVANCE, after the fact
>
> **R23 LANDED on 2026-08-20** (`docs/evidence/r23_advance_2026-08-20/`): store
> `cc02567f` → `b745002e`, board `1d5c9f7a` → `7a3f4fe2`, `as_of_round` 22 → 23, ledger 3,086 → 3,497,
> 411 played / 393 DNP.
>
> **This runbook was right about the shape of the week and wrong in five specific, load-bearing
> places.** Each is corrected in place below and marked **`ERRATUM`**. Three of the five would have
> HALTED the advance if followed literally; a read-only preflight against the owner's REAL file
> (`r23_preflight/PREFLIGHT_REPORT.md`) caught all three before anything was armed. They are recorded
> here so the R24 seat inherits the correction rather than the defect.
>
> | # | where | what was wrong | consequence if followed |
> |---|---|---|---|
> | **E1** | §3 expected verdicts, §4 H2 | **`enc=utf-8` is wrong; the file is `cp1252`**, and §4 H2's own check snippet decodes `utf-8` with `errors="replace"`, **mangling 16 names** | a seat checks the verdict against the runbook, sees a mismatch, and mistakes a correct parse for a fault; the snippet's name-matching is unreliable |
> | **E2** | §3 step 2 | **the Bailey remediation recipe does not work.** The override table is keyed by the EXACT display string; this export writes `Bailey Williams WBD` | **HALT** — the `Bailey Williams` rule is never consulted |
> | **E3** | (register v797, carried into the brief) | `Callum Brown -> callum-m-brown` — **`callum-m-brown` is not a key in the store** | **HALT** — override-target-invalid, and it overwrites the standing rule that already works |
> | **E4** | §4 H2 | the sheet's pins are **SIX literals in TWO blocks**, not three in one; the ORDER 41 block **halts first** | **HALT** at ORDER 41 with the ORDER 42 pins already moved |
> | **E5** | §3 artifact list | `ui/data/club_valuation.js` and `ui/data/ownership.js` are **not** advance artifacts in this era | a seat hunts for a mover that is skipped by design |
> | **E7** | §4 H2, and E4 above | **the sheet pins are no longer in the engine at all.** PLAN_v6 PACKAGE 3a (2026-08-21) moved them to `data/sheet_pins.json`; "move six literals in two engine blocks in the same commit as the sheet" is now the WRONG instruction | a seat edits `_merged_recover.py` for a **data** change — moving `engine_head`, owing a restamp nobody planned, and re-creating the drift E4 records |
>
> **Hazard status at the landing:** **H1 REPAIRED** in tree (`staged_apply.py` now copies
> `docs/owner_annotations` + `docs/evidence/exec_306_zlaarm` into the workspace, commit `6f2d58c`).
> **H3 REPAIRED** in tree (`rl_export.py:210`, commit `e19833e`; parity gate 96 → 0). **H2 BIT, exactly
> as feared** — the real R23 listed both `harry-armstrong` and `judson-clarke` — and was cleared by the
> owner-ruled re-cut (ACT 1, commits `b86bc9e` / `024b458` / `2305743`). **H4 self-cleared** in the
> sibling repin, as it said it would; the sidecar was never hand-edited. **H5 did not re-engage** — this
> export writes the two Baileys apart. **H6 is still open** and is still noise, not advance damage.
>
> **The dry-run base named below (`189c34e`, store `cb38ef11`, board `a05fe951`) is STALE.** The advance
> ran on `27458ad`, store `cc02567f`, board `1d5c9f7a`. Two board moves landed at round 22 between the
> rehearsal and the advance — THE D8 ADOPTION and the injury-sheet re-cut — and both sit on the R22 side
> of the R22→R23 movers boundary by rule M0.

Recon seat, read-only. Dry-run base: `origin/main` @ `189c34e` (store `cb38ef11`, board `a05fe951`,
`as_of_round=22`). Rehearsed in `scratchpad/r23_recon/` with SYNTHETIC scores; the real repo was never
touched.

**READ THE HAZARDS SECTION (§4) BEFORE RUNNING ANYTHING. Three blockers stop the R23 advance dead on
the current base. One is a one-line plumbing gap, one is an owner call, and one — a 96-of-804
export↔engine parity failure in the balanced/strict sibling build — is a pre-existing valuation break
that blocks unconditionally and is independent of anything the owner sends.**

The separate F5 off-by-one diagnosis lives at `scratchpad/F5_OFFBYONE_DIAGNOSIS.md`.

---

## 1. THE OWNER'S INPUT SPEC — what a round-23 scores file must look like

Hand this section to the owner verbatim.

> ### Your round-23 file
>
> Save it as **`scores/R23.csv`** in the repo. One row per player who **played** round 23.
>
> ```
> Player,2026 R23
> Izak Rankine,223
> Matt Rowell,174
> Bailey Smith,161
> ...
> Jy Farrar,9
> ```
>
> **The rules, in plain terms:**
>
> 1. **Two columns: name, then score.** The header line is `Player,2026 R23`. A FootyWire two-row
>    header (`Player,2026 R23` then `,Score`) is also fine — both shapes are recognised. If your export
>    has extra columns in the middle, they are ignored: the **first** cell is the name and the **last**
>    cell is the score.
> 2. **Only players who played.** A player who is **not in the file did not play** — nothing is
>    recorded for him, and no game is added to his average. This is the standing rule (owner ruling
>    2026-07-20). Do **not** add zero rows for players who were rested, injured or omitted. R22 listed
>    409 of 804 players; 395 were absent, and that was correct.
> 3. **A score of 0 is allowed and means a genuine played zero.** Only use it if he actually played.
> 4. **Names must match the database spelling.** Case, extra spaces and stray non-breaking spaces are
>    all forgiven automatically (R21 shipped with 12 trailing invisible spaces and every row still
>    matched). What is *not* forgiven is a genuinely different name — the tool will stop and ask rather
>    than guess.
> 5. **Blank or non-numeric scores are rejected loudly.** Every listed row needs a number. Lines
>    starting with `#` and blank lines are skipped.
> 6. **Encoding and line endings don't matter.** UTF-8, UTF-8-with-BOM and Windows/CP1252 are all read
>    correctly, and CRLF is preserved, never "fixed". **Send the file exactly as your league site gives
>    it — do not clean it up.** The file is stored byte-unmodified as the record of what you sent.
>
> **The two names to check before you send it:**
>
> - **Bailey Williams.** There are two active players. If your export writes them **apart** —
>   `Bailey Williams` (Western Bulldogs) and `Bailey J. Williams` (West Coast) — everything resolves by
>   itself and there is nothing to do. If your export collapses **both onto the bare name
>   `Bailey Williams`** (which is what R22 did), the tool will **stop** and ask you which score belongs
>   to which club. Save yourself the round-trip: tell us up front, e.g. *"97 = West Coast, 89 = Bulldogs"*.
> - **Callum Brown.** Your export writes `Callum Brown`; the database says `Callum M. Brown`. This is
>   already handled by a standing rule — no action needed.
>
> **`ERRATUM E3` (2026-08-20) — and this one is a trap, so it is spelled out.** The paragraph above is
> CORRECT and the correct action is *nothing*. Register **v797** nevertheless specified a second
> binding, `Callum Brown -> callum-m-brown`, and the R23 seat brief carried it. **`callum-m-brown` is
> not a key in the store.** The store holds `callum-brown-ire` (`Callum M. Brown`, GWS, **active**) and
> a **retired** bare `callum-brown`. A standing **unscoped** `map_all` override already binds the name
> to `callum-brown-ire` and fires correctly. `IdentityOverrides._by_name` is
> `{o['name']: o for o in overrides}` — a **second entry named `Callum Brown` silently overwrites the
> first** — and `_resolve_round` looks the target up with `by_key.get(okey)`, so a missing key yields
> `override-target-invalid` and **HALTS**. Simulated by the preflight: `PREFLIGHT HALT — 1 unresolved:
> ['Callum Brown']`. **TOUCH NOTHING.** Owner word 2026-08-20: *"Callum M brown is fine."*
>
> **One more thing that is new this week:** if any player who is marked **injured** on your
> `SITTER_2026_v1` sheet actually **played** round 23, tell us. The board cross-checks that sheet
> against the store and will stop if they disagree. (37 players are currently marked injured; one of
> them, Judson Clarke, was listed in R22.)

### The machine-readable version

| field | rule |
|---|---|
| file name | `scores/R23.csv` (round parsed from the `R<N>` in the filename when using `--dir`) |
| header | `Player,2026 R23`; optional second header row `,Score`; recognised structurally |
| name column | first cell; `id_resolver._norm` = unidecode + lowercase + `[a-z ]` + collapse |
| score column | **last** cell; `float`, rounded to 1 dp; `0` legitimate; blank/non-numeric → `FootyWireParseError` |
| membership | listed ⇒ played (score appended, +1 game); absent ⇒ DNP (nothing appended, not an error) |
| encoding | BOM → `utf-8-sig`; else `utf-8`; else `cp1252`. Reported in the preflight as `enc=`. |
| line endings | preserved verbatim; file hashed (`sha256`) and stored byte-unmodified |
| skipped lines | blank lines; lines whose first cell starts with `#` |
| identity | exact match to one **active** stable key, or an owner override; anything else HALTS |
| overrides file | `engine/rl_after/ingestion/catchup_identity_overrides.json` |

### Edge cases and what happens

| case | behaviour |
|---|---|
| DNP / rested / injured | omit the row. Absence is not an error and is not unresolved-input. |
| genuine played zero | list the row with `0`. Preflight reports it under `listed-zero`. |
| trailing `\xa0` / double spaces / case drift | absorbed by the normaliser; resolves clean |
| name not in the DB (new intake not yet loaded) | `UNRESOLVED` → **preflight HALTS**, nothing applied |
| two active players sharing one display name | `DUPLICATE stable key` → **preflight HALTS** (this is the guard working) |
| same player listed twice | duplicate stable key → HALT |
| late correction after a round is applied | the dedup ledger blocks a re-send of the same (player, season, round). Use `repair`/a corrective act, never a second `catchup`. |
| retired player listed | override-target-invalid / unresolved → HALT |

---

## 2. HOW R22 WAS INGESTED — the trace (this is the pattern R23 follows)

**Input of record.** `scores/R22.csv` — the owner's couriered file, byte-unmodified.
`Player,2026 R22` header, 409 data rows, CRLF, UTF-8, md5 `82b456d5675c18b137180416b82432fc`,
sha256 prefix `c8f3748462d0`. It entered the repo by being placed at `scores/R22.csv`; nothing edited it.

**Command (both preflight runs and the apply):**

```
round_entry catchup --file 22=scores/R22.csv
```

**What happened, in order:**

1. **Preflight run 1 (read-only) — HALTED.** The R22 export regressed and wrote *both* Bailey Williams
   players under the one bare name (97 and 89). With the disambiguation rule retired at R20, both
   resolved to `bailey-williams-wb` and the duplicate stable-key guard halted the whole catch-up before
   any write. `absent/DNP=396`. **This was the only halt reason**; the other 407 rows resolved unaided.
2. **Owner ruling.** *"97 = West Coast, 89 = Bulldogs"* — recorded as a **round-22-scoped `(round, score)`
   mapping** in `catchup_identity_overrides.json` (`"22|97"→bailey-williams-wc`, `"22|89"→bailey-williams-wb`).
   The score file was **not** edited; the ruling lives in the identity record, not the data.
3. **Preflight run 2 — CLEAN.** `listed/played=409 resolved=409 listed-zero=0 absent/DNP=395`,
   three identity overrides fired (two Bailey by round-score, Callum Brown by `map_all`).
   The `396 → 395` move is the correct consequence of the two rows no longer collapsing.
4. **Apply**, as one sequential staged transaction `txn_catchup_r22`
   (STAGE → VALIDATE → ATOMIC SWAP, with rollback + crash recovery), 17 of 17 targets, `failure: null`.

**What each step wrote:**

| artifact | before → after |
|---|---|
| store `engine/rl_after/rl_model_data.json` | `37ced3ce` → `0dd6b4a0` |
| board `data/rl_build/rl_app_data.json` | `113b36f8` → `6e724cca` |
| board srcmd5 sidecar | `6d80c58c` → `ded7e537` |
| `data/expected_boot.json` | `dca47923` → `2317e692` |
| `data/release_contract.json` | `773416a6` → `887bed3f` |
| `data/season_state.json` | `57945b89` → `f30ff89d` (round 21 → 22, calendar 0.92) |
| `applied_rounds_ledger.json` | 2,677 → 3,086 triples (**+409**, no double-count) |
| `value_history.json` / `rank_history.json` / `pos_rank_history.json` | all bumped; rounds now `[14…22]` |
| `sibling_repin_state.json` | `3ba6bdc1` → `1e0d8022` |
| `finalization_state.json` | `f42c32ad` → `47f32657` |
| `ui/data/{board_view_public,board_view_working,club_valuation,movers,ownership}.js` | all regenerated |
| `ui/data/movers_transition.js` | **unchanged** — no out-of-round board between R21 and R22 |
| movers | `movers/movers_R22.{json,csv}`, 804 rows injected to UI |

**The ledger and journal recorded:**

- `applied_rounds_ledger.json`: +409 `stable_id|2026|22` triples (3,086 total; R15–R22 all present,
  409 for R22). This is what blocks a re-sent feed from double-counting.
- `finalization_journal.jsonl` lines 51–55, the clean five-line shape:
  `CORE_COMMITTED (board_md5_after 6e724cca, txn_catchup_r22, reconciled:false)` →
  `STATUS FINALIZING` → `FINALIZE_BEGIN (force:false, historical:false)` → `STATUS FINALIZED` →
  `FINALIZED (injected:804, movers_json: movers_R22.json)`.
  *(Contrast R20, lines 28–45: two `FINALIZATION_INCOMPLETE — movers bundle board-identity chain broken`
  and three `force:true` retries. That is what a bad round looks like in the journal.)*

**How the pins moved — the ADVANCE-REPIN design.**
> **`ERRATUM E7` (2026-08-21) applies to this section too.** The **sheet** pins are no longer part of
> ADVANCE-REPIN's engine-side work at all: `data/sheet_pins.json` is a data file, moved in the sheet's
> own commit **before** the advance, by the manual path in §4 H2 — which is the **INTERIM WRITER**
> until `land round` (PLAN_v6 2b) takes over as sole writer. Everything below is about the
> **balanced/strict sibling and the FV vector**, which are unaffected by 3a and still move inside the
> staged transaction. A sheet re-cut and an ADVANCE-REPIN are now two commits, not one, and the sheet
> commit must leave `engine_head` unmoved.

The balanced/strict sibling board and the FV
reference vector are derived siblings of the one store. `staged_apply._stage_sibling` runs the repin
**inside the same transaction** (step c3, `staged_apply.py:546-565`), so the balanced board and the FV
vector move in the **same commit** as the store: it rebuilds the sibling from the *staged* store via the
accepted FV builder, asserts the store it built from equals the canonical manifest pin, regenerates the
complete FV reference vector **from that freshly-built board**, derives the identity from the generated
artifacts (never from a supplied constant — **build-and-compare**), and stages the coherent movement of
every dependent pin (expected_boot `balanced_board_md5`, release_contract identities +
`present_lens_baseline` + re-seal, `reference_vector_<md5>.json`, `forward_vector_<board>.json`,
`test_forward_lens_<board>.py`, `test_fv_provenance.py`, the two board-view bundles, and the
`sibling_repin_state.json` sidecar). At R22 that moved balanced `123deccb` → `b4cc0b2b`, added
`reference_vector_b4cc0b2b.json` and `forward_vector_6e724cca.json`, board total Σv 759,722 → 761,583,
Sheezel 12,124 → 11,925, **PICK 1 numéraire 3,000 unmoved**.

**Verification that followed** (evidence `docs/evidence/ingest_r22_2026-08-10/`): independent board
re-derivation from the landed store in a clean workspace reproduced `6e724cca` **byte-exact**; Guard 5
green in and out of the transaction; one-source self-test 142 PASS / 0 FAIL / 0 STALE; movers suites
39/39 (py) + 66/66 (js); F1 and F2 parity 0 mismatches.

---

## 3. THE COMMAND LIST FOR THE REAL R23 ADVANCE

```bash
export PATH="/root/rl_venv312/bin:$PATH"
export RL_REPO=/home/user/afl-rl-engine
export RL_FV="$RL_REPO/engine/forward_valuation"
export PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
cd "$RL_REPO"

# 0. place the owner's file, byte-unmodified
#    -> scores/R23.csv        (record its md5 + sha256 before anything else)
md5sum scores/R23.csv && sha256sum scores/R23.csv

# 1. PREFLIGHT — read-only, writes nothing. Run this first, always.
python3 tools/round_entry/round_entry.py catchup --file 23=scores/R23.csv
#    Expect: PREFLIGHT CLEAN, listed/played=N, resolved=N, absent/DNP=804-N,
#            identity override: Callum M. Brown -> callum-brown-ire (map_all)
#    Then it stops at "NOT APPROVED — nothing applied." That is correct.

# 2. If the preflight HALTS on a Bailey Williams name, get the owner's word and record it in
#    catchup_identity_overrides.json. DO NOT EDIT scores/R23.csv. Re-run step 1 until CLEAN.
#
#    ERRATUM E2 (2026-08-20): THE RECIPE THAT USED TO BE HERE DOES NOT WORK, AND WAS SIMULATED
#    FAILING. It said: add 23 to overrides["Bailey Williams"].applies_to_rounds and a
#    "23|<score>": "bailey-williams-wb" line to its map. IdentityOverrides._by_name is keyed by the
#    EXACT display string and resolve() looks it up on the RAW name (round_catchup.py:71,85), so a
#    "Bailey Williams" rule is NEVER CONSULTED for a row the export writes as something else.
#    The R23 export wrote "Bailey Williams WBD" (69) alongside "Bailey J. Williams" (125). Applying
#    the old recipe still halted: 1 unresolved, ['Bailey Williams WBD'].
#
#    WHICH RECIPE TO USE DEPENDS ON THE SHAPE OF THE EXPORT. LOOK AT THE FILE FIRST.
#      (a) BOTH players under ONE bare display name (the R22 regression) -> the by_round_score rule
#          on that exact name, scoped to the round: "<round>|<score>" -> the right stable key.
#      (b) The two players written APART but one carrying a name the store does not have (R23:
#          "Bailey Williams WBD") -> a NEW ENTRY keyed by that EXACT string:
#              {"name": "Bailey Williams WBD", "rule": "map_all",
#               "stable_key": "bailey-williams-wb", "applies_to_rounds": [23],
#               "reason": "<owner citation verbatim>"}
#          NOT an extension of the existing "Bailey Williams" rule. This also HONOURS H5 rather than
#          violating it: the R20 retirement of the bare-name rule stands, because the export is not
#          collapsing the two names — it is decorating one of them.
#      (c) The two players written apart with store-exact names -> nothing to do; both resolve.
#    Round-scope whatever you add, so it carries no standing weekly cost.

# 3. APPLY — arm both halves of the gate for this run only (no code edit).
INGEST_SCORE_APPLY_ARMED=1 INGEST_SCORE_APPLY=<owner-worded-token> \
python3 tools/round_entry/round_entry.py catchup --file 23=scores/R23.csv --approve

# 4. if finalization is left incomplete (exit 6):
python3 tools/round_entry/round_entry.py finalize --round 23
#    or, to force-rebuild the derived outputs without re-applying:
python3 tools/round_entry/round_entry.py repair --round 23

# 5. if an apply is interrupted mid-flight:
python3 tools/round_entry/round_entry.py recover
```

Use `--file 23=scores/R23.csv`, **not** `--dir scores` — `--dir` picks up `R21.csv`/`R22.csv` too and
relies on the ledger to skip them. Explicit is safer.

### Expected verdicts

| step | expected |
|---|---|
| preflight | `PREFLIGHT CLEAN — every name resolves to a stable identity; no duplicate/ambiguous.` |
| preflight counts | `listed/played=N resolved=N listed-zero=0 absent/DNP=804-N`, `enc=` **whatever the file is** |
| overrides fired | `Callum M. Brown -> callum-brown-ire (map_all)` — and Bailey only if the export needs it |

> **`ERRATUM E1` (2026-08-20) — `enc=utf-8` WAS WRONG AND IS NOT A FAULT WHEN IT DIFFERS.** The
> owner's real R23 file is **`cp1252`**: 16 raw `0xA0` (NBSP) bytes, each trailing a player name, and a
> strict UTF-8 decode fails at byte 43. That is **within spec** — `footywire_parser.decode_bytes`
> tries BOM→`utf-8-sig`, then `utf-8`, then `cp1252` — and the R23 preflight and apply both reported
> `enc=cp1252` and resolved 411 of 411. **Do not "fix" the file and do not treat the encoding line as a
> verdict.** The actual R23 verdict line was:
> `R23 enc=cp1252 listed/played=411 resolved=411 listed-zero=0 absent/DNP=393 sha256 e3d5410e0e57`.
>
> A related precision: the 16 trailing-`\xa0` names are absorbed by **`str.strip()` inside the parser**,
> *before* the normaliser is consulted — 409 exact matches plus 16 post-strip exact matches. The
> normaliser absorbs case/spacing drift, but it was not what saved these.
| apply line | `R23  store <8>-><8>  board <8>-><8>  players=N  guard5=True  hist=[14…23]  final=FINALIZED  movers->UI=804` |
| ledger | 3,086 → 3,086+N triples |
| journal | five lines: `CORE_COMMITTED` → `FINALIZING` → `FINALIZE_BEGIN force:false` → `FINALIZED` → `FINALIZED injected:804 movers_json:movers_R23.json` |
| numéraire | PICK 1 = 3000, unmoved |
| sibling | balanced board + FV vector move in the same transaction; new `reference_vector_<new>.json`, `forward_vector_<newboard>.json`, `test_forward_lens_<newboard>.py` |

### Artifacts that move (the full expected-mover set)

`engine/rl_after/rl_model_data.json` · `data/rl_build/rl_app_data.json` (+ `.srcmd5`) ·
`data/expected_boot.json` · `data/release_contract.json` · `data/season_state.json` ·
`engine/rl_after/ingestion/{applied_rounds_ledger,value_history,rank_history,pos_rank_history,sibling_repin_state,finalization_state}.json` ·
`engine/rl_after/ingestion/finalization_journal.jsonl` ·
`engine/rl_after/ingestion/movers/movers_R23.{json,csv}` ·
`ui/data/{board_view_public,board_view_working,movers}.js` ·
`session_2026-07-20/fv_provenance_remediation/fixtures/{reference_vector_*,forward_vector_*}.json` ·
`session_2026-07-20/fv_provenance_remediation/test_forward_lens_*.py` · `test_fv_provenance.py` ·
`engine/rl_after/ingestion/.weekly_txn/txn_catchup_R<N>/{journal.jsonl,manifest.json}` (tracked — R15…R23
all are) · plus the round-advance expectations in `engine/rl_after/ingestion/test_movers_transition.py`
and `ui/tests/movers.test.js` (bumped every week; R22 bumped 21→22 and moved the future-append fixture
R22→R23; R23 moved 22→23 and R23→R24).

> **`ERRATUM E5` (2026-08-20) — TWO NAMED "MOVERS" DO NOT MOVE, AND ONE MORE DOES.**
> * **`ui/data/club_valuation.js` is SKIPPED BY DESIGN**, and the code says so:
>   `round_finalize.py:340` emits `'club_valuation': 'SKIPPED (Track A owns the club-valuation curve)'`.
>   Do not hunt for it.
> * **`ui/data/ownership.js` is not an advance artifact** either — its writer of record is
>   `ui/tools/ingest_inputs.py`, driven by `docs/inputs/` changes.
> * **`engine/rl_after/rl_app_data.json` (+ `.srcmd5`) is the GENERATOR-side copy and the transaction
>   does NOT publish to it** — `round_apply.py:139-141` publishes only to `data/rl_build/`. R22 left it
>   stale with every gate green. R23 synced it by hand **and disclosed the sync**, because THE BAKE and
>   THE D8 ADOPTION both moved the pair in lockstep and the same seat had just moved it in ACT 1.
>   Either choice is defensible; the one thing that is not is moving it silently.
> * **A ROUND ADVANCE EARNS NO `data/release_lineage.json` ENTRY.** The lineage register records
>   OUT-OF-ROUND board moves. R23's register tail correctly remains the ACT 1 re-cut boundary at round
>   22. (`generate_movers_transition.py --check` and `rebuild_movers_derived.py --check` must still both
>   exit 0 afterwards.)

---

## 4. KNOWN HAZARDS — what the dry run actually hit

Ranked by what stops you first.

### H1 (BLOCKER, plumbing) — the transaction workspace does not carry `docs/`, so ORDER 41 halts the board regen

```
ORDER 41 HALT: RL_O41_INJ=1 but the owner's annotation file is ABSENT at
  <ws>/docs/owner_annotations/SITTER_2026_v1.csv. The injury stream reads a PINNED OWNER INPUT
  and will not run without it, and will not substitute a guess for it.
```

`staged_apply._build_workspace` (`staged_apply.py:698-736`) copies an **allow-list** into the throwaway
build workspace: `engine/rl_after`, `engine/forward_valuation`, six root `.py`/`.md` files, `data/`,
`session_2026-07-18/legf5`, `session_2026-07-20/fv_provenance_remediation`, `ui`,
`session_2026-07-17/legd_derivation`. **No `docs/` subtree is copied.** Since the ORDER 41/42 bake
(`_merged_recover.py:595`, *"BAKE 2026-08-20 (register v780): RL_O41_RESET / RL_O41_INJ / RL_O41_R3 ARE
NOW DEFAULT-ON"*) the engine reads three `RL_REPO`-relative files that live under `docs/`:

| file | read at | consequence if absent |
|---|---|---|
| `docs/owner_annotations/SITTER_2026_v1.csv` | `_merged_recover.py:4167` (ORDER 41, I3 injury stream) | **SystemExit HALT** |
| `docs/owner_annotations/SITTER_2026_v1.csv` | `_merged_recover.py:5862` (ORDER 42 consolidation) | **SystemExit HALT** |
| `docs/evidence/exec_306_zlaarm/basis/structural_basis_279.json` | `_merged_recover.py:2154` (v0 lens basis) | **SystemExit HALT** unless `RL_LENS_BASIS` is set |
| `docs/evidence/exec_306_zlaarm/basis/lane_expectation.json` | `_merged_recover.py:2373` | optional, no halt |

All four files exist and are tracked in `origin/main`; only the **workspace builder** omits them. R22
landed 2026-08-10, before the bake — so the weekly transaction has **never been run since these inputs
became mandatory**. This is a pure plumbing gap, not a data problem.

**Proposed fix (one line, `staged_apply._build_workspace`):** extend the copytree list —

```python
for rel in (os.path.join('session_2026-07-20', 'fv_provenance_remediation'), 'ui',
            os.path.join('session_2026-07-17', 'legd_derivation'),
            os.path.join('docs', 'owner_annotations'),
            os.path.join('docs', 'evidence', 'exec_306_zlaarm')):
```

**Proven:** applying exactly this in the scratch tree cleared the ORDER 41 halt and the canonical board
regen then ran to completion (including its own F1 parity gate).

### H2 (BLOCKER, data) — ORDER 42 pins the injury sheet's `games_2026` to the store, and a round advance moves it

```
ORDER 42 HALT: judson-clarke — the sheet reads games_2026=1 and the store reads 2. The store is
  the single source of production and the sheet is the single source of injury; a disagreement
  between them is an input defect, not something to average away.
```

`_merged_recover.py:5906-5920` walks the **37 `injured=Y`** rows of `SITTER_2026_v1.csv` and requires
each one's `games_2026` to equal the store's 2026 `games` **exactly**. On the landed base the two agree
perfectly (215 matched rows, **0 mismatch**) — the sheet is a snapshot of the post-R22 store. But the
round advance **increments `games` for every listed player**, so the first R23 file that lists any of
the 37 injured-marked players desynchronises the sheet and halts the board regen *inside the
transaction*.

The sheet is also pinned — md5, row count and `injured=Y` count — so it **cannot be quietly re-cut**:
changing it moves the md5 and trips a different halt in the same file. Any fix must move the sheet
**and** its pins in **one commit**. ~~Any fix must move the sheet **and** the pinned literals in
`_merged_recover.py` in **one commit**.~~ — **SUPERSEDED BY `ERRATUM E7`: the pins are not in
`_merged_recover.py` any more. Read E7 before you touch anything in this section.**

> ## `ERRATUM E7` (2026-08-21) — **THE PINS LEFT THE ENGINE. A SHEET UPDATE IS A DATA COMMIT.**
>
> PLAN_v6 **PACKAGE 3a** landed on 2026-08-21 (`docs/evidence/p3a_pins_out_2026-08-21/`). The six
> literals E4 describes — `O41_INJ_MD5`/`O41_INJ_ROWS`/`O41_INJ_Y` and
> `_SHEET_MD5`/`_SHEET_ROWS`/`_SHEET_Y` — **are gone from `engine/rl_after/_merged_recover.py`.** The
> three facts are now **ONE declaration** in **`data/sheet_pins.json`**, read by both blocks through
> `_sheet_pins()`. E4's warning that the two copies can drift apart is retired *because the second
> copy no longer exists*; everything else E4 says about the two guards still stands.
>
> **NOTHING ABOUT THE GUARD CHANGED.** A drifted sheet — md5, rows or `injured=Y` disagreeing with the
> declaration — still **HALTS the build**, with the ORDER 41 / ORDER 42 halt text byte-unchanged.
> **ORDER 41 still halts FIRST.** Each block still reads the pins only inside its own dial's branch,
> so a dial-off build reads the declaration not at all. **An absent or malformed
> `data/sheet_pins.json` HALTS** (`SHEET-PIN HALT`), fail-closed, in any build that would have read
> the pins.
>
> ### THE CORRECT PROCEDURE for a sheet re-cut (replaces E4's "six literals in two blocks")
>
> ```bash
> # 1. PREREG-LITE FIRST — see the box below. Write it before you change a byte.
> # 2. re-cut docs/owner_annotations/SITTER_2026_v1.csv (CRLF and cp1252 preserved — ERRATUM E1)
> # 3. measure the sheet, do not type it:
> python3 - <<'PY'
> import csv, hashlib, json, os
> R = os.environ['RL_REPO']; S = 'docs/owner_annotations/SITTER_2026_v1.csv'
> raw = open(os.path.join(R, S), 'rb').read()
> rows = list(csv.DictReader(raw.decode('utf-8').splitlines()))
> ys = [r for r in rows if (r.get('injured') or '').strip().upper() == 'Y']
> print('sheet_md5       ', hashlib.md5(raw).hexdigest())
> print('sheet_rows      ', len(rows))
> print('sheet_injured_y ', len(ys))
> PY
> # 4. write those three MEASURED values into data/sheet_pins.json. Nothing else in that file moves
> #    except `pinned_at` and a `provenance` line naming the owner word that authorised the re-cut.
> # 5. ONE COMMIT, EXPLICIT PATHS ONLY (process law P8), carrying exactly:
> git add docs/owner_annotations/SITTER_2026_v1.csv data/sheet_pins.json <the prereg-lite path>
> git commit -- docs/owner_annotations/SITTER_2026_v1.csv data/sheet_pins.json <the prereg-lite path>
> # 6. then advance/land as normal. VERIFY: engine_head MUST NOT HAVE MOVED.
> md5sum engine/rl_after/_merged_recover.py   # == data/expected_boot.json engine_head
> ```
>
> **`engine_head` MOVING ON A SHEET UPDATE IS A RED, NOT A CHORE.** That is the whole effect 3a bought:
> *engine_head moves if and only if code changed.* If it moved, the commit touched the engine and the
> act is not the data act it claims to be — stop and find out why, do not restamp it forward.
>
> ### THE INTERIM WRITER — say it out loud, because it expires
>
> **Until PACKAGE 2b's `land round` exists, THIS MANUAL PATH IS THE INTERIM WRITER of
> `data/sheet_pins.json`.** `tools/land round` is deliberately unbuilt and exits non-zero saying so.
> When 2b lands it becomes the **SOLE writer** of the declaration, and this manual path retires for
> this act type on the owner's word (PLAN_v6 2a.3 / 2a.4 — an unexercised fallback is fake safety, and
> the manual round path is never retired before 2b exists).
>
> **This paragraph is a REPEAT, not the rule's home.** The rule lives in the pin file's own header
> (`data/sheet_pins.json` → `_writer_of_record`) and in the engine's `_sheet_pins()` header. A runbook
> is a procedure, not a law's home — this one needed five errata inside a single round.
>
> ### PREREG-LITE — the review-forcing step a data commit still owes
>
> Moving the pins out of the engine removed the engine's prereg (P9) from the path of a sheet update.
> **It does not remove the review.** A sheet change carries a **prereg-lite**, committed **WITH** the
> data change, in the same commit, stating:
>
> | slot | what it holds |
> |---|---|
> | **predicted `sheet_md5`** | the md5 the re-cut sheet is expected to have |
> | **predicted `sheet_rows`** | expected row count |
> | **predicted `sheet_injured_y`** | expected `injured=Y` count |
> | **disclosed movers** | who this re-cut is expected to move on the board, **by name**, and by roughly how much — or the explicit claim that it moves nobody |
> | **the owner word** | verbatim, that authorised the re-cut (the R23 re-cut's was *"All good on the injury sheet. Fine by me."*) |
>
> Predicted **first**, measured **after**; the prereg-lite is corrected against the tree, never the
> tree against the prereg-lite. A re-cut whose measured movers are not the disclosed movers is a
> **halt and a report**, not a note. Worked example of the full-fat form this is the light version of:
> `docs/evidence/r23_advance_2026-08-20/01_PREREG_SHEET_RECUT.md`.

> **`ERRATUM E4` (2026-08-20) — IT IS SIX LITERALS IN TWO BLOCKS, NOT THREE IN ONE, AND THE BLOCK THIS
> SECTION NAMES IS THE ONE THAT HALTS *SECOND*.** **(Kept as history. The pins' LOCATION is superseded
> by `ERRATUM E7` above — there are no literals in the engine any more. What E4 says about the two
> guards, their order, and the R23 re-cut's own numbers is still correct.)** Register v790 and this section both named only the
> ORDER 42 trio. There is an **earlier ORDER 41 block** asserting the same three facts, and it halts
> **first** — so a re-cut that moves only the ORDER 42 pins dies at ORDER 41 with the sheet already
> changed.
>
> | block | literals | assertion sites |
> |---|---|---|
> | **ORDER 41** (halts FIRST) | `O41_INJ_MD5` · `O41_INJ_ROWS` · `O41_INJ_Y` | md5, rows, Y-count, then a 35-of-35 name match |
> | **ORDER 42** | `_SHEET_MD5` · `_SHEET_ROWS` · `_SHEET_Y` (one line, `;`-separated) | md5, rows, Y-count, name match, ambiguity, key count, then the `games_2026` compare |
>
> **GREP THE PIN NAMES. DO NOT TRUST LINE NUMBERS** — `_merged_recover.py` is edited by other acts
> (the D8 adoption moved it the same week) and every line number in this runbook and in the preflight
> is pre-adoption.
>
> **What the R23 re-cut actually did** (`docs/evidence/r23_advance_2026-08-20/`, prereg `b86bc9e`,
> edit `024b458`): `harry-armstrong` and `judson-clarke` flipped `injured` `Y`→`N`, **two bytes**, size
> 15,948 and rows 219 both unchanged, CRLF preserved; md5 `b26798c3…` → `21361291f26d35108b88f92f885c5063`;
> `injured=Y` **37 → 35**; all six literals moved in the same commit as the sheet. **Neither guard was
> weakened** — option (b) below, loosening the compare to `store_games >= sheet_games`, was **NOT**
> taken, because the owner ruled the re-cut: *"All good on the injury sheet. Fine by me."*
>
> **The re-cut moves the board, so it owes an out-of-round column and a lineage entry.** Standing owner
> rule 2026-07-28. It is also what rule **M0** needs: `round_finalize` builds the round-N movers against
> `round_movers.previous_point(repo, N)` — the stored point IMMEDIATELY BEFORE round N — so the
> post-re-cut round-22 board must exist as a stored point, or the round's movers silently report the
> re-cut as the round's own work. **Watch the ordering:** `out_of_round_column._register` sorts columns
> by `(after_round, id)` — **alphabetically**, not chronologically — so a new round-22 column only lands
> last if its id sorts last. **Assert `previous_point` after writing the column; do not trust the
> alphabet.** (The R23 seat's column `the-sheet-recut-20-8` does sort last, and the assertion is in
> `register_recut_column.py`.)
>
> > **`ERRATUM E6` (2026-08-20) — THE SORT IS REPAIRED. THE ALPHABET NO LONGER DECIDES.**
> > Landed as its own act (prereg `d446f6f`, repair `4c3dedd`,
> > `docs/evidence/f5_and_sort_2026-08-20/01_PREREG_SORT.md`), after the R23 advance disclosed it.
> >
> > `out_of_round_column` now orders columns by **`(after_round, kind, seq)`** through a single
> > `_order_key` shared by the writer and the reader, so the stored order and the displayed order
> > cannot drift apart. Every **new** column is stamped with an explicit monotonic `seq` at
> > registration — chronology recorded as data, not inferred from an id. The **eight** columns that
> > predate the repair keep their bytes (no `seq` was back-filled into a stored history) and are
> > ordered by the closed `_LEGACY_ORDER` table, whose provenance is `data/release_lineage.json`'s
> > append-only `release_transition_register`.
> >
> > **What it fixed, measured:** at `after_round=22` the display order was
> > `… g1-never-rises-10-8 · the-d8-adoption-20-8 · the-landing-20-8 · the-sheet-recut-20-8`, placing
> > THE LANDING (`a05fe951`) *after* the D8 adoption (`5ea978f7`) that superseded it. It is now
> > `… g1-never-rises-10-8 · the-landing-20-8 · the-d8-adoption-20-8 · the-sheet-recut-20-8`, and the
> > two repaired `model_changes` boundaries reproduce lineage register entries **8**
> > (`a05fe951 → 5ea978f7`) and **9** (`5ea978f7 → 1d5c9f7a`) exactly. The three history files, the
> > board and the store were **byte-unmoved**; only the derived `points` / `model_changes` blocks of
> > `ui/data/movers.js` moved, rebuilt by the tool of record `ui/tools/rebuild_movers_derived.py`.
> > `previous_point(repo, 23)` is **unchanged** at `the-sheet-recut-20-8`, so R23's movers baseline
> > did not move. Suites 39/39 and 66/66; all three gates green.
> >
> > **KEEP ASSERTING `previous_point` AFTER WRITING A COLUMN ANYWAY.** The advice above stands on its
> > own merits: it costs nothing, and it checks the outcome rather than the mechanism. What has
> > changed is that it should now always pass, and that a *new* column no longer needs an id chosen
> > to win an alphabetical race.

**Blast radius is data-dependent and small:** of the 37 injured-marked players, **0** appeared in
`R21.csv` and **1** (`judson-clarke`) appeared in `R22.csv`. So R23 may well pass untouched — but it is
a coin flip on the owner's file, not a guarantee.

**Check this before you apply** (read-only, seconds).

> **`ERRATUM E1b` (2026-08-20) — THE SNIPPET THAT USED TO BE HERE IS DELETED. DO NOT RESURRECT IT.**
> It decoded the score file with `.decode("utf-8", errors="replace")`. The real R23 file is `cp1252`
> with 16 `0xA0` bytes, so that line turned **all 16** of those names into `�` and the set
> intersection below it was unreliable on exactly the file it was written to check. A check that
> silently mis-reads 16 of 411 rows is worse than no check.
>
> **USE THE REAL PARSER.** It is the same code the apply uses, it handles the encoding by spec, and it
> is free:

```bash
python3 - <<'PY'
import csv, os, re, sys
R = "/home/user/afl-rl-engine"; RN = 23
sys.path.insert(0, os.path.join(R, "engine", "rl_after", "ingestion"))
import footywire_parser as FP                       # THE PARSER OF RECORD — decode_bytes handles
                                                    # BOM/utf-8/cp1252 and strips each name itself
n = lambda s: re.sub(r'[^a-z0-9]+', '-', str(s).strip().lower().replace('’', "'")).strip('-')
inj = {n(r['player']) for r in csv.DictReader(
           open(os.path.join(R, "docs/owner_annotations/SITTER_2026_v1.csv")))
       if (r.get('injured') or '').strip().upper() == 'Y'}
parsed = FP.parse_round_file(os.path.join(R, "scores/R%d.csv" % RN))
rows = parsed['rows'] if isinstance(parsed, dict) else parsed
hit = sorted({n(name) for name, _score in rows} & inj)
print("injured=Y players listed in R%d: %d %s" % (RN, len(hit), hit))
print("-> if non-empty, ORDER 42 WILL HALT the advance. The remedy is the re-cut below.")
PY
```

*(If `parse_round_file`'s return shape has moved, read it rather than guessing — the point of this
erratum is that the parser is the authority on what the file says, not a hand-rolled decode.)*

**What it said for the real R23, against the PRE-re-cut sheet:**
`injured=Y players listed in R23: 2 ['harry-armstrong', 'judson-clarke']` — exactly the two the v790
re-cut was written for. H2 was not a coin flip; it landed.

**Re-run today it says `0 []`, and that is the check working, not the check broken:** the two rows are
now `injured=N`, so no listed player is injury-annotated and ORDER 42 has nothing to disagree about.
Zero is the state a round is safe to apply in.

**Measured, for anyone tempted to restore the old snippet:** run on this same file it mangles exactly
**16** names — `Isaac Heeney�`, `Chad Warner�`, `Nick Haynes�`, `Nick Blakey�`, … — none of which can
match the sheet. It would have reported `0 []` for the wrong reason on a file where the answer was 2.

**Proposed fix (owner-worded, not a seat decision):** ORDER 42's cross-check is not round-aware. Either
(a) re-cut the sheet's `games_2026` from the store and move the md5/rows/Y pins in the same commit as
the round advance — making the sheet a *per-round* artifact with a standing weekly cost; or (b) make the
check tolerate `store_games >= sheet_games` (the sheet is an as-of snapshot, and a player playing more
is production news, not an input defect); or (c) scope the check to the round the sheet was cut at.
(b) is the cheapest and preserves the guard's real purpose — catching a sheet that names the wrong
player — while dropping the false positive that a round advance manufactures every week. **Owner call.**

### H3 (BLOCKER, valuation — PRE-EXISTING, and the most serious finding here) — the balanced/strict SIBLING build fails the F1 export↔engine parity gate on **96 of 804** players

```
EXPORT<->ENGINE PARITY GATE FAILED for 96/804 players (board v != engine gated ev, eps=0):
  harry-sheezel: board=10310 engine=10433   |  will-ashcroft:  board=6494 engine=6607
  nasiah-wanganeen-milera: board=8593 engine=8644 | jason-horne-francis: board=5554 engine=5600
  sam-darcy: board=5016 engine=5076         |  aaron-cadman:   board=1667 engine=1781
  ... (the gate prints the first 25; all 96 are board < engine)
```

The canonical board of record rebuilt cleanly and **passed** its own F1 parity gate
(`rl_export.py:650-666`, `eps=0`). The **sibling** build — the balanced/strict posture
(`RL_PVC2=1 / RL_LEGE=0 / RL_LEGF=0`, `sibling_repin.build_sibling`) — fails the same gate. Because
`_stage_sibling` runs *inside* the transaction and is fail-closed, this aborts the whole advance
**pre-commit**.

**This is PRE-EXISTING on main, not caused by the round advance.** Proven by running
`sibling_repin.py plan` on the **pristine** scratch base with **no R23 data applied at all** (store
`cb38ef11`, ledger 3,086): it fails identically. The failing set shifts slightly between the pristine
and post-R23 runs (the store differs), but the failure is present either way.

**It is not a stale-builder artifact.** `rl_model.py` is md5 `6fe7c415` in the repo, in the disposable
FV builder copy, *and* in `expected_boot.json`'s `rl_model` pin — all three agree. `fv_identity`
`6e9a370e…` matches `fv_identity_expected`. The provenance preamble reports `LOADED-PROVENANCE OK`.

**The signature is a sharp cohort edge, not numeric drift.** Every one of the 25 named players is drafted
in **2021 or 2022 and nothing else** (born 2003–2004; 22 ND, 2 PDA, 1 RD), against an all-active mean
birth year of 2001.3. Games played is *not* the discriminator (fail mean 79 vs all-active mean 80).
Every divergence is one-directional — **the board understates the engine** — by roughly 0.5–7%.
A clean draft-year band boundary at 2021/2022 points at a years-since-draft / age-taper / year-zero band
edge, consistent with the constants re-derived in ORDER 30B (positional v0 re-fit) and ORDER 31-F (the
head fix at all six curve heads) reaching the config-of-record path but not reproducing identically
under the balanced/strict posture. **Root-causing the valuation is the valuation owner's call, not the
ingestion seat's** — but the R23 advance cannot complete until it is resolved.

Note this is also why H4's 8 stale-pin gripes matter less than they look: they were the *visible* noise
sitting on top of a sibling layer that cannot actually build.

### H4 (GRIPE, not a blocker) — the 8 sibling-layer `verify` fails

`sibling_repin.py verify` currently reports `ok:false` with 8 fails:

```
forward reference vector for 234c3414 missing
forward oracle test_forward_lens_a05fe951.py missing
sidecar source_store_md5 != current store
sidecar contract_sha256 != live contract seal
sidecar forward_board_md5 != the canonical board of record
sidecar forward_vector filename != regenerated forward vector
sidecar forward_oracle filename != regenerated forward oracle
release_contract check failed
```

**All 8 are one fact.** `sibling_repin_state.json` is pinned to store `d9a24282` / forward board
`4b448a82` / balanced `234c3414` / contract `ef25c259`, which is the **DOB-courier landing** state
(commit `064abca`, the last commit to touch the sidecar). Since then the board of record advanced
through ORDER 29 / 29B / 30 / 31-F and the LANDING PREP C3 six-pin re-key to `a05fe951`, and the store
to `cb38ef11` — **all without running the sibling advance-repin**. Every one of the 8 lines is a
restatement of "the sidecar names the pre-ORDER-29 board".

**Do these block a round advance? No — by design they are what the advance *fixes*.** `_stage_sibling`
does **not** read the stale sidecar as an expectation; it *rebuilds* the sibling from the staged store,
derives the identity from the built artifact, and — because the derived identity will not equal the
stale live pins — takes the "otherwise STAGE the coherent movement" branch and moves them. A stale
sidecar is precisely the non-no-op case the module exists to serve. The dry run confirms the ordering:
the run reached `_stage_sibling` and got as far as *building* the sibling, i.e. the 8 stale-pin fails
never gated anything. What stopped it was H3, a genuine parity failure in the build itself — a different
and more serious thing that the 8 gripes were camouflaging.

**Consequence for the runbook:** do not treat `sibling_repin verify` green as a precondition for R23,
and do not "fix" the sidecar by hand — hand-editing it would be exactly the
edit-the-expectation-to-match move the module forbids. It should move in the advance transaction.

### H5 (procedural) — the identity-override retirement decision is still open

`catchup_identity_overrides.json` scopes the Bailey Williams rule to rounds `[15,16,17,18,19,22]`. R22
was a **one-round re-engagement** forced by a regressed export, not a reversal of the R20 retirement.
The file's own note is explicit: *"If future exports keep collapsing the two names, the standing cost
returns and the rule should be re-argued rather than hand-extended each week."* If R23's export also
collapses them, escalate the rule rather than adding a `23|…` line by reflex.

### H6 (cosmetic, real) — the F5 self-consistency off-by-one

The board's declared F5 entrant layer (`56772`) disagrees with the sum of its own parts (`49595 + 7178
= 56773`) by exactly 1. `invariant_proof.py` fails 2/28 on this at both lenses. It is a **double-rounding
artifact**, not a ledger miss, and it does **not** block a round advance — but it will keep the per-push
invariant lane red through the R23 landing, and it will re-fire on the rebuilt board. See the separate
diagnosis note. **Do not let it be mistaken for round-advance damage.**

---

## 5. DRY-RUN RESULT — every halt, in order

Base: scratch export of `origin/main` @ `189c34e`, store `cb38ef11`, board `a05fe951`, `as_of_round=22`,
ledger 3,086. Synthetic R23 files built by copying R22's exact 409-name list with obviously-fake
patterned scores (`60 + i mod 61`).

| # | run | result |
|---|---|---|
| 1 | preflight, `R23_SYNTH_apart.csv` (R20/R21 shape — the two Bailey written apart) | **PREFLIGHT CLEAN** · 409/409 resolved · absent/DNP 395 · `Callum M. Brown` override fired · Bailey rule correctly *not* in scope for R23 · exit 0 · **nothing written** |
| 2 | preflight, `R23_SYNTH_regressed.csv` (R22 shape — both under the bare name) | **PREFLIGHT HALTED** · `DUPLICATE stable key: bailey-williams-wb scores=[75.0, 99.0]` · absent/DNP 396 · exit 2 · **nothing written** — reproduces the R22 halt exactly |
| 3 | armed apply, variant `apart` | **H1** — `StagedValidationError: staged board regen FAILED rc=1` → `ORDER 41 HALT ... SITTER_2026_v1.csv ... ABSENT` · aborted pre-commit, store/board/ledger byte-unchanged |
| 4 | armed apply, variant `apart`, with the H1 one-line workspace fix applied **to the scratch copy only** | **H2** — `ORDER 42 HALT: judson-clarke — sheet games_2026=1, store 2` · aborted pre-commit, clean |
| 5 | armed apply, variant `clean` (H1 fix + the single injured=Y player dropped, 408 rows) | canonical board regen **PASSED** (incl. its own F1 parity gate) → **H3** — `SiblingBuildError: sibling board build failed rc=1` · aborted pre-commit · store `cb38ef11`, board `a05fe951`, ledger 3,086 all **byte-unchanged**, transaction rolled back cleanly |
| 6 | `sibling_repin.py plan` on the **pristine** base (no R23 applied, zero synthetic data) | **fails identically** → **H3 is PRE-EXISTING on main**, not advance-induced |
| 7 | direct `_run_sibling_build(balanced=True)` on the pristine base, full stderr captured | `EXPORT<->ENGINE PARITY GATE FAILED for **96/804** players`, all `board < engine`; the 25 printed are drafted **2021–2022 exclusively** |

**What the dry run proves.**
- The **identity layer is fully rehearsed and healthy**: the resolver, the override machinery, the
  duplicate guard and the DNP/absence rule all behave exactly as the R22 record describes.
- The **transaction discipline is sound**: three separate mid-flight halts, three clean pre-commit
  aborts, zero partial writes, ledger never moved.
- The **canonical board regen works** on the landed base once H1 is fixed.
- The advance is **blocked** by H1 (one line, seat-fixable), H2 (owner call, may not bite), and **H3
  (pre-existing valuation break, 96/804, blocks unconditionally)**.

**Order of work before R23 can land:** H3 first (it blocks regardless of the owner's file and is
independent of the round), then H1 (one line), then H2 (check the file, escalate only if it bites).
H4 needs no action — the advance clears it. H6 is noise to be labelled, not fixed in this act.

**Read-only discipline:** the real repo was never written. The only patch was to
`scratchpad/r23_recon/engine/rl_after/ingestion/staged_apply.py`; `/home/user/afl-rl-engine/...`
staged_apply.py stayed at md5 `f81c4d9ca7dc92921d17023c09048c01` throughout. Synthetic score files
exist only under `scratchpad/r23_recon/scores/R23_SYNTH_*.csv` and were never placed in the real
`scores/`.
