# R23 RUNBOOK — the round-23 advance, rehearsed

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

**How the pins moved — the ADVANCE-REPIN design.** The balanced/strict sibling board and the FV
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

# 2. If the preflight HALTS on Bailey Williams, get the owner's word and record it as a
#    ROUND-23-SCOPED (round, score) mapping in catchup_identity_overrides.json:
#      add 23 to overrides[Bailey Williams].applies_to_rounds
#      add  "23|<score>": "bailey-williams-wc" / "bailey-williams-wb" to its map
#    DO NOT EDIT scores/R23.csv. Re-run step 1 until CLEAN.

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
| preflight counts | `listed/played=N resolved=N listed-zero=0 absent/DNP=804-N`, `enc=utf-8` |
| overrides fired | `Callum M. Brown -> callum-brown-ire (map_all)` — and Bailey only if R23 collapses the names |
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
`ui/data/{board_view_public,board_view_working,club_valuation,movers,ownership}.js` ·
`session_2026-07-20/fv_provenance_remediation/fixtures/{reference_vector_*,forward_vector_*}.json` ·
`session_2026-07-20/fv_provenance_remediation/test_forward_lens_*.py` · `test_fv_provenance.py` ·
plus the round-advance expectations in `engine/rl_after/ingestion/test_movers_transition.py` and
`ui/tests/movers.test.js` (bumped every week; R22 bumped 21→22 and moved the future-append fixture
R22→R23 — this week they move 22→23 and R23→R24).

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

The sheet is also **triple-pinned** — md5 `b26798c35adcd9bda5cef50ff2c884da`, 219 rows, 37 `injured=Y`
(`_merged_recover.py:4163-4165` and `5861`) — so it **cannot be quietly re-cut**: updating `games_2026`
moves the md5 and trips a different halt in the same file. Any fix must move the sheet **and** the three
pinned literals in `_merged_recover.py` in **one commit**.

**Blast radius is data-dependent and small:** of the 37 injured-marked players, **0** appeared in
`R21.csv` and **1** (`judson-clarke`) appeared in `R22.csv`. So R23 may well pass untouched — but it is
a coin flip on the owner's file, not a guarantee.

**Check this before you apply** (read-only, seconds):

```bash
python3 - <<'PY'
import json,csv,re
R="/home/user/afl-rl-engine"
n=lambda s: re.sub(r'[^a-z0-9]+','-',str(s).strip().lower().replace('’',"'")).strip('-')
inj={n(r['player']) for r in csv.DictReader(open(R+"/docs/owner_annotations/SITTER_2026_v1.csv"))
     if (r.get('injured') or '').strip().upper()=='Y'}
b=open(R+"/scores/R23.csv","rb").read().decode("utf-8",errors="replace")
hit=sorted({n(l.rsplit(",",1)[0]) for l in b.splitlines()[1:] if l.strip()} & inj)
print("injured=Y players listed in R23:", len(hit), hit)
print("-> if non-empty, ORDER 42 WILL HALT the advance. Escalate before applying.")
PY
```

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
