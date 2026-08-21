# R24 DRESS REHEARSAL — THE ROUND LANDER'S REAL PATH, FLOWN AGAINST SYNTHETIC SCORES

**2026-08-21 · sandbox only · the live tree is byte-unmoved and the proof is at the foot of this
document.** Six flights of `tools/land round` against a machine-generated R24 score file, in a
`git worktree` sandbox cut from live HEAD `94bca14`. Nothing here was armed against the live tree,
no owner word exists or is claimed for anything in it, and the synthetic board it produced
(`29c5ac7b`) never left the sandbox.

**VERDICT: GO-WITH-NOTES**, and the notes are load-bearing. The machine works: the armed advance,
ADVANCE-REPIN, the generator sync, the day-0 active path, the contract restamp, all five UI
writers, the movers page, the state file, the claims file and the explicit-path commit all
performed correctly on a real round. But **the first real flight will halt twice before it lands**,
in two places nothing had ever exercised, and both halts are diagnosed below with their remedies.
Fly it knowing that, and R24 contains nothing novel. Fly it blind and it stops at step 3.

---

## 1. WHAT THE SELF-TEST'S BUILT-IN "ROUND REHEARSAL" ALREADY COVERED — AND WHAT IT DID NOT

`tools/landing/selftest.py::spec_round_noop` is the fixture every round case is injected into. It
is honest about what it is, and this section states its boundary so this act's added value is
**stated, not assumed**.

**WHAT IT COVERS (30 PASS / 0 FAIL, re-run four times inside this rehearsal as the lander's own
pre-transaction proof):**

| covered | how |
|---|---|
| the 15-step sequence runs clean | `round_control_clean_run`, a DECLARED NO-OP rehearsal |
| every step 2b adds, broken once | 7 fault cases, each caught, each aborting byte-exact with HEAD back at base |
| the sheet re-cut sole-writer path | `sheet_recut_writer` positive + `sheet_recut_wrong_prediction` negative |
| the M1b day-0 guard | `round_fault_day0`: activated + zero movers = halt |
| explicit-path commits | `round_commit_explicit_paths` |
| the live tree untouched | `live_tree_untouched` |

**WHAT IT DOES NOT COVER, AND CANNOT:** its fixture sets `round.scores: null`. Every one of its
round cases therefore logs *"no scores file declared — this act is a REHEARSAL and applies
nothing"*, *"no scores file — nothing to preflight"*, *"REHEARSAL — nothing is armed and nothing is
applied"*. It has never:

1. started from a tree carrying an owner score file (the step-0 / step-3 pincer, §3.1);
2. run `round_entry catchup` for real, armed or unarmed;
3. applied a round, moved a store, or built a board inside a landing;
4. run ADVANCE-REPIN, the generator sync with something to sync, the day-0 **positive** path, or the
   movers page against a real report;
5. **run the real gate set at all.** `selftest._spec_common` declares a deliberately CHEAP two-gate
   set (`release_manifest_check`, `release_contract_check`). The acceptance runner and BOTH movers
   suites — three of the five `DEFAULT_GATES` — have never executed inside a landing transaction.
   That is where this rehearsal found its second halt.

**THE ADDED VALUE OF THIS ACT, in one line:** it is the first and only run of `land round` that has
ever armed, applied a round, and reached the gates.

---

## 2. THE SYNTHETIC INPUTS

`synthetic_inputs/make_synthetic_r24.py` (deterministic, seed 20260824) produced
`scores/R24.csv` in exactly the shape the owner couriers: header `Player,2026 R24`, **cp1252**,
**CRLF**, trailing newline, names carried byte-verbatim off the R23 export including its trailing
U+00A0 artefacts. 7,268 bytes · md5 `58ae786bc8ef7bd218417a652892162e` · sha256 `6e9003d5…`.

* **411 listed / 393 DNP** of the 804-player active pool — the R23 shape.
* R23's names minus 13 dropped, plus 11 added from the active pool, plus **two deliberate H2 trips**
  (`Tom Green`, `Connor Rozee` — both `injured=Y` on the pinned sheet).
* The Bailey pair written **APART** (`Bailey Williams` / `Bailey J. Williams`, the R20/R21 export
  shape), so R24 needs **no round-scoped identity override**. Only the standing `Callum Brown`
  `map_all` rule fires. Verified by the read-only preflight: `resolved=411`, PREFLIGHT CLEAN.
* **Ten declared risers** (scores forced to 115–148) and **ten declared fallers** (12–31), so the
  movers direction is a falsifier and not an impression.

**A sheet re-cut WAS exercised**, and it was not optional: the file was engineered so H2 trips, which
is the R23 shape exactly (`harry-armstrong`/`judson-clarke` flipped `Y -> N` there). The re-cut flips
the two rows, `injured_y 35 -> 33`, rows unchanged at 219, md5 `21361291… -> 4656041e…`, with a
prereg-lite (`01_PREREG_LITE_SHEET_RECUT.md`) committed WITH the data change.

---

## 3. THE FLIGHTS, EVERY STEP'S VERDICT AND TIMING

Six flights. Each ran the **real** invocation `python3 -m tools.landing.cli round --spec … --root …`
with the **real** builder; each therefore ran the full pre-transaction self-test first (30 PASS,
~25s) before opening a transaction.

| run | spec | outcome | halted at |
|---|---|---|---|
| A | `ACT_SPEC_R24_SYNTHETIC` (no re-cut), score file uncommitted | HALT | `preflight` — dirty tree |
| B | same, score file committed | HALT | `catchup_preflight` — **H2, as predicted** |
| C | `…_RECUT` (re-cut declared) | HALT | `catchup_preflight` — **input commit has nothing to commit** |
| D | `…_FULL` (re-cut + day-0 ON), `--no-commit` | HALT | `advance` — `RL_BUILD_LOCK_FILE` rejected |
| E | `…_FULL`, `--no-commit`, sandbox lock override removed | HALT | `gates` — acceptance runner RED |
| F | `…_LEG2` (gate set narrowed), `--no-commit` | **COMPLETE, exit 0** | — |

### 3.1 RUN A + RUN C — THE INPUT-COMMIT PINCER (**MACHINERY DEFECT, BLOCKS R24**)

Two halts, one root cause, reproduced on the real invocation and recorded in
`aborts/ABORT_A_preflight_dirty_scores.json` and `aborts/ABORT_C_catchup_preflight_nothing_to_commit.json`.

`steps.catchup_preflight`'s own docstring states its contract: *"THEN IT COMMITS THE INPUTS — the
score file and the override record — as their own explicit-path commit."* That requires the score
file to be **uncommitted** when the lander starts. But `steps.preflight` refuses any dirty path, and
`txn.Ctx.declared_dirt()` returns **only** the sheet and the prereg-lite (and only when a re-cut is
declared) — never the score file. So:

* **score file uncommitted** → RUN A: `THE TREE IS NOT CLEAN … ?? scores/R24.csv` at step 0;
* **score file committed** → RUN C: step 3 reaches `PREREG MET`, then
  `git commit failed: … nothing added to commit but untracked files present`. (`git commit -m … -- <unchanged paths>`
  exits 1; verified independently.)

There is **no third option**. The armed path of `land round` is unreachable as shipped, and the
self-test could not see it because its fixture declares no score file. **This is machinery and this
act did not touch it** — a rehearsal that rewrites the machine invalidates itself.

**REMEDY FOR THE MACHINERY OWNER (one of):** add the score file and
`catchup_identity_overrides.json` to `declared_dirt()` when `round.scores` is declared (the
symmetric, obviously-intended fix); **or** make `_git_commit` return `None` gracefully when the
named paths carry no change; **or** drop the input commit and declare the score file a pre-flight
seat commit in the runbook. The first is the smallest and matches the docstring.

**INTERIM PATH FOR R24 IF THE MACHINERY IS NOT REPAIRED FIRST:** commit the owner's score file (and
any override entry) as a seat commit before the flight — the R23 ACT-2 shape — and fly with
`--no-commit`, then make the landing commit by hand from the path list step 14 prints. That is a
downgrade of the very thing 2b bought and it should be a last resort, not the plan.

### 3.2 RUN B — H2 FIRED EXACTLY AS DESIGNED (**a GOOD outcome**)

```
--- STEP 3/14  catchup_preflight ---
injured=Y players listed in R24: 2 ['connor-rozee', 'tom-green']
  ORDER 42 WILL HALT THE ADVANCE. … The remedy is the owner-worded re-cut … not a weakened guard.
carriers that moved before the failure: 0
ABORT PROOF: every carrier is BYTE-EXACT to the identity captured at step 0.
```

Pre-arming, zero carriers moved, correct remedy named. The runbook rated H2 *"a coin flip on the
owner's file"*; it landed at R23 and it lands here. **Expect it at R24 and have the owner's sheet
word ready before the flight.**

### 3.3 RUN D — `RL_BUILD_LOCK_FILE` IS FATAL TO AN ARMED ADVANCE (**machinery-adjacent, 4th of its class**)

```
staged_apply.ConfigPolicyError: the board build must use the accepted release policy…
  - UNKNOWN inherited valuation flag RL_BUILD_LOCK_FILE='…' (not in the release config manifest)
```

`config_manifest.INFRA_ALLOW` is `{RL_ALLOW_PVCFIT_BOARD, RL_APP_DATA, RL_CONFIG_MODE, RL_FV,
RL_REPO, RL_V0SURF_PKL, RL_VENV}`. `RL_BUILD_LOCK_FILE` and `RL_BUILD_LOCK` are the **lock tooling's
own flags** and both carry the `RL_` prefix — precisely what `carriers.py`'s own header forbids in as
many words: *"A TOOL'S OWN FLAGS ARE NEVER `RL_*`."* That header records three prior burns of this
class; **this is the fourth**, and the first to be caught by an armed run.

It matters beyond this rehearsal because `selftest.Sandbox.env()` **sets `RL_BUILD_LOCK_FILE`** to
keep its sandboxes off the shared lock. The self-test never arms, so it never fires. Any seat that
follows that isolation recipe and then arms — a rehearsal, a recovery, a soak — halts at step 4 with
a message about shell flags, not about locks. **Reported, not fixed.**

*Rehearsal remedy, applied to the seat's own environment and not to the machine:* the override was
dropped and the sandbox took the real shared lock (verified free first), which is also the real R24
behaviour.

### 3.4 RUN E — THE FULL JOURNEY, AND THE GATE RED THAT WILL MEET R24

Every step through `state` passed. Machine-recorded timings:

| step | seconds | verdict |
|---|---:|---|
| preflight | 0.07 | OK |
| sheet | 0.01 | OK — pins written, ONE explicit-path commit, `engine_head` asserted UNMOVED |
| scores | 0.00 | OK — md5 + sha256 asserted, 0 declared overrides, 3 in file |
| catchup_preflight | 0.10 | OK — H2 clear, PREFLIGHT CLEAN, PREREG MET |
| **advance** | **271.11** | **OK** |
| generator_sync | 0.01 | OK — synced and DISCLOSED |
| day0 | 0.00 | OK — ACTIVE, row diff printed, installed |
| contract | 0.07 | OK — restamped, 10 frozen fields asserted unmoved, check PASSES |
| sibling | 0.11 | OK — current, nothing to reconcile (the repin ran in-transaction) |
| ui | 1.70 | OK — all five writers, identity read back out of the bundle |
| movers_page | 0.10 | OK — 193,908 bytes, 804 rows |
| state | 0.15 | OK — regeneration verified |
| **gates** | **8.05** | **FAIL** |
| | **281.49** | **TOTAL** |

**The advance is 97% of the wall clock.** Budget ~5 minutes per flight plus ~25s of pre-transaction
self-test; a full R24 with one retry is well under fifteen minutes.

**THE ROUND, APPLIED:**
```
R24  store b745002e->303a0765  board b3e8da99->29c5ac7b  players=411  guard5=True
     hist=[14..24]  final=FINALIZED  movers->UI=804
ledger 3497 -> 3908 (+411), 0 duplicates
as_of_round 24 in expected_boot, season_state, release_contract, sibling_repin_state
engine_head 3af8c1f7 UNMOVED — no engine file is touched by an advance
balanced_board_md5 7c32a540 -> 578c7dbc, BUILT inside the transaction by ADVANCE-REPIN
```

`RUN F` reproduced board `29c5ac7b` and contract seal `53af7b50e4c8` **byte-identically** on a second
independent armed run — an unplanned determinism proof.

### 3.5 RUN F — COMPLETE, exit 0

Same act with the gate set narrowed **in the rehearsal spec only** (declared and documented in that
spec) so the last three steps were reached. `gates` OK, `claims` **GREEN — 9 of 9 verified against
the tree**, `commit` staged **38 explicit paths, every one inside the declared carrier set**.
TOTAL 278.36s. The full five-gate set was then measured by hand on the landed tree — §4.

---

## 4. THE GATES, MEASURED ON THE LANDED R24 TREE

| gate | verdict | cause |
|---|---|---|
| `release_manifest_check` | **PASS** | |
| `release_contract_check` | **PASS** | |
| `acceptance_runner --profile in-transaction` | **RED — 15 PASS / 2 FAIL** | `oneliner_r14_restore` (real) + `inbox_manifest` (sandbox artefact) |
| `test_movers_transition.py` | **FAIL** | the weekly round pin |
| `ui/tests/movers.test.js` | **3 FAIL / 66** | the weekly round pins |

### 4.1 THE WEEKLY ROUND PINS (**the second thing that will halt R24 — procedural, remedy known**)

`carriers.py` names `engine/rl_after/ingestion/test_movers_transition.py` and
`ui/tests/movers.test.js` with writer of record **"the advance (weekly round expectation)"**, and the
py suite says so in its own comment: *"WEEKLY ROUND PIN — bumped by each round advance, and by
nothing else… **It is a hand-pin: the advance transaction does not own this file**, so the advance
seat moves it in the advance's own commit and discloses it."* R23 did exactly that (commit `b7ec627`
moved four pins). **No step of `ROUND_SEQUENCE` moves them**, and the lander's `gates` step runs both
suites — so a round advance through `land round` reds its own gate by construction.

Both suites are **green on the live tree today** (39/39 py, 66/66 js) — this is not pre-existing
drift; it is created by the advance and must be pre-empted.

**THE COMPLETE, MEASURED R24 PIN LIST** (the py suite halts on the first, so the second was unmasked
by a temporary sandbox-only edit that was reverted byte-exact):

`engine/rl_after/ingestion/test_movers_transition.py`
1. L204 `_ck(eb.get('as_of_round') == 23, …)` → `== 24`
2. the future-append fixture L254–L272: `live23`→`live24`, `_mk_future_report(24,…)`→`25`,
   `prod['rounds'] + [24]`→`+ [25]`, `reports['24']`→`['25']`, and the same-round conflict guard's
   `fake23`→`fake24`. Measured red: `FAIL: appending a future R24 report writes (no overwrite conflict)`
   — R24 is real history now, so the guard correctly refuses it.

`ui/tests/movers.test.js`
3. L170 `eq(prod.rounds, [15…23])` → `[15…24]`  *(measured: got `[15,…,24]`)*
4. L171 `reports.length === 9` → `10`
5. the lineage-state pin `bridged` → **`ok`** — a round advance makes the latest round report
   terminate on the loaded board, which is the `ok` branch. (It reads `bridged` today because the
   staircase adoption moved the board out of round last.)

**THE ORDERING, AND IT MATTERS.** The R23 hand-walk put the bump inside the advance's own commit —
after the advance, before the gates. `land round` runs its gates INSIDE the transaction, before its
commit, so that ordering is gone. Two workable recipes, both measured against this rehearsal:

* **RECOMMENDED — pre-bump.** Bump all five pins and commit them as a seat commit **immediately
  before** the flight, disclosing that the tree is deliberately red on those two suites until the
  advance lands. Verified safe: the pre-transaction self-test uses the cheap two-gate set and does
  **not** run either suite, so a pre-bumped tree does not block the transaction from opening. Cost:
  the tree is transiently red, and if the flight aborts the seat must revert the bump.
* **FALLBACK — fly, halt, bump, re-fly.** Exactly what this rehearsal did. The abort is byte-exact
  and the ledger rolls back, so R24 is re-appliable (proved: RUN F succeeded after RUN E's abort).
  Cost: one throwaway ~5-minute flight.

### 4.2 `inbox_manifest` — A SANDBOX ARTEFACT, NOT AN R24 RISK

`tools/inbox_manifest.py` derives each entry's `arrived` date from the file's mtime. `git worktree
add` resets every mtime to checkout time, so the sandbox recomputes `arrived: 2026-08-21` against a
recorded `2026-08-20` and reports STALE. **Measured on the live tree at HEAD: `0 problem(s), 0 stale`
and the full in-transaction profile is 17/17 GREEN.** It will not fire on the real flight. Worth
knowing because it will fire in any future worktree rehearsal.

---

## 5. THE DAY-0 STEP'S FIRST ACTIVE EXERCISE (register v810 item 1)

`day0` had never run in the positive direction anywhere — the self-test only ever proves the M1b
guard (activated + zero movers = halt). Activated here, it behaved exactly as `_day0` documents:

```
--- STEP 6/14  day0 ---
day-0 re-base : ACTIVATED by "…"
   docs/evidence/final_candidate_2026-08-19/DAY0_CP.json -> docs/evidence/r24_rehearsal_2026-08-21/DAY0_R24_SYNTHETIC.json
   THE MANDATORY ROW DIFF — every moved row, printed, 3 of 89:
     blake-thredgold                    381 -> 388
     harley-barker                      504 -> 509
     liam-hetherton                     70 -> 73
```

**PRINTED ROW DIFF BEHAVIOUR, precisely:** it diffs the `printed` field of the two files' `rows` by
`key`, prints **every** moved row (no truncation, no summary), refuses a re-base where zero rows
move, then installs `new_reference` over `reference` byte-for-byte. It computes nothing and asserts
nothing about day-0 law — by design, so no second implementation of the law exists beside its
emitter. The step took **0.00s**; the cost is entirely in the generator, if one is declared.

**THE FINDING THE REAL R24 MUST ACT ON BEFORE IT FLIES: there is no runnable day-0 emitter for R24.**
The emitter of record, `docs/evidence/final_candidate_2026-08-19/cprb_day0.py`, is **act-pinned**: it
reads its board from a named scratch directory that no longer exists, diffs against
`order_k_2026-08-18/DAY0_K.json`, and hard-asserts SIX named movers with their exact old and new
printed integers (assertions A3/A4). It cannot run for R24 as it stands. This rehearsal therefore
declared **no generator** and supplied a hand-perturbed, unmistakably-labelled synthetic reference —
which exercises the step but proves nothing about day-0 itself.

**So the R24 seat owes a carried emitter** (the R23-era chain's own pattern: `ok_day0.py` ->
`fcrb_day0.py` -> `cprb_day0.py`, each carried with its changes declared), authored and run BEFORE
the flight, with `day0_rebase.generator` naming it. Alternatively the owner leaves day-0 **OFF** at
R24 — it is off by default and the M1b ruling keeps it that way — and the reference stays stale for
another round. **That is an owner-visible choice and this report is the place it gets asked.**

---

## 6. THE MOVERS — DO BETTER SCORES MOVE PLAYERS UP?

Measured against the movers report of record `movers_R24.json` (804 rows), not eyeballed.
**20 of 20 declared movers moved the right way; 0 wrong-direction.**

| | player | R24 score | value | Δ | rank Δ |
|---|---|---:|---|---:|---:|
| RISER | Zeke Uwland | 148 | 1809 → 2361 | +552 | +41 |
| RISER | Sam Cumming | 141 | 2198 → 2895 | +697 | +30 |
| RISER | Will Darcy | 115 | 220 → 412 | +192 | +119 |
| FALLER | Errol Gulden | 26 | 7205 → 6061 | −1144 | −4 |
| FALLER | Nick Blakey | 12 | 4199 → 3413 | −786 | −17 |
| FALLER | Chad Warner | 15 | 4132 → 3419 | −713 | −15 |

(full table: `flight_logs/LANDED_movers_direction.txt`)

**THE BOUNDARY NOTE THE OWNER WILL NEED.** Rule M0 puts R24's baseline at
**`the-staircase-adoption-21-8`**, not at round 23 — three out-of-round columns have landed since
R23. So the R24 movers page compares FROM the staircase board `b3e8da99`, and every number on it is
"since the staircase adoption", not "since round 23". The `movers_page` step asserted this itself
(`baseline 'the-staircase-adoption-21-8' at round 23 (rule M0, via previous_point)`), and the act
spec's `movers_page.boundary_note` slot is where the seat says so in the owner's language.

---

## 7. THE SEASON BOUNDARY — R24 IS THE LAST ROUND

`data/season_state.json` carries `season_total_rounds: 24`. The advance derived
**`calendar_progress: 1.0`** (from 0.96) and `exposure_pace 0.864 -> 0.909`. R24 is the round that
closes the season calendar, and `staged_apply` raises `SeasonBoundError` for any round outside
`[1, season_rounds]` — so an R25 would halt at the door and needs an owner decision on
`season_total_rounds` before it could ever be applied. Nothing about R24 itself is affected; it is
recorded so nobody discovers it in a fortnight.

---

## 8. THE ABORT LADDER, PROVED ON A REAL ROUND

The self-test proves the ladder on synthetic faults. RUN E proved it on a **real applied round**: the
landing had moved the store, the board, the season clock, the ledger, three histories, the day-0
reference, the sheet, four UI bundles and four FV fixtures — **30 carriers, some created, some
rewritten** — and the abort put every one back:

```
carriers that moved before the failure: 30
RESTORING 30 carrier(s): … rewrite … delete engine/rl_after/ingestion/.weekly_txn/txn_catchup_r24/… …
ABORT PROOF: every carrier is BYTE-EXACT to the identity captured at step 0.
```

RUN C additionally proved the **commit** rewind: the sheet commit `c4cffe02` was made mid-flight,
the abort rewound it, and `HEAD is back at the base commit … History carries no trace of this landing.`

**TWO OPERATIONAL NOTES ON abort-then-retry**, both measured, neither a defect:

1. **The abort's own `ABORT_<step>.json` is dirt and blocks the retry** at step 0. Move it aside
   before re-flying (the self-test's own `_stage_recut` does exactly this).
2. **A rewound sheet commit takes the prereg-lite with it.** The sheet is a carrier and is restored;
   the prereg-lite is not, so the working-tree copy is deleted by the rewind and the seat must
   re-create it (recoverable with `git show <rewound-sha>:<path>`) before the retry.

---

## 9. THE EXACT SEQUENCE THE REAL R24 NEEDS

### 9.1 THE ONE WORD FROM THE OWNER

**The score-write arming word — RULEBOOK law 10(c).** Concretely, the owner supplies **his R24 score
file** plus a sentence authorising the write and **his own apply token** (R23's was
`R23-2026-08-20-owner-approved`). Both go into the act spec verbatim:
`round.arming.owner_word` and `round.arming.env.INGEST_SCORE_APPLY`. **The lander composes neither
and this seat never will.**

Two **conditional** words may also be needed and should be asked for in the same message so the
flight is not stopped twice:

* **the injury-sheet word**, if H2 trips (it did at R23 and it trips on any file listing an
  `injured=Y` player) — R23's was *"All good on the injury sheet. Fine by me."*;
* **the day-0 word**, if the standing reference is to be regenerated at this advance (§5). If it is
  not given, day-0 stays OFF, which is its default and its ruling.

### 9.2 THE SUPERVISOR'S COMMAND SEQUENCE

```bash
export PATH="/root/rl_venv312/bin:$PATH"
export RL_REPO=/home/user/afl-rl-engine
export RL_FV="$RL_REPO/engine/forward_valuation"
export PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
cd "$RL_REPO"
# NEVER export RL_BUILD_LOCK_FILE or RL_BUILD_LOCK — §3.3. Any RL_* outside
# config_manifest.INFRA_ALLOW halts the armed advance inside staged_apply.

# 0. place the owner's file byte-unmodified and record its identity
cp <couriered> scores/R24.csv && md5sum scores/R24.csv && sha256sum scores/R24.csv

# 1. read-only preflight — measure the seven round_expected falsifiers off the tool, never type them
python3 tools/round_entry/round_entry.py catchup --file 24=scores/R24.csv
#    expect PREFLIGHT CLEAN, listed/resolved/absent-DNP, sha256, then "NOT APPROVED"
#    if a name does not resolve: the owner's word into catchup_identity_overrides.json,
#    NEVER an edit to the score file (R23 runbook ERRATUM E2 — read the export's shape first)

# 2. the act spec
tools/land spec-template --act-kind round-advance > ACT_SPEC_R24.json
#    fill: owner_word, authority, prereg.path + board_before (b3e8da99… today) + all seven
#    round_expected fields, round.number=24, round.scores{path,md5,sha256}, round.arming
#    (BOTH halves, owner's token), sheet (null or the declared re-cut), column=null, lineage=null,
#    day0_rebase (§5), movers_page.boundary_note (§6 — the baseline is the staircase column),
#    evidence_dir. Commit it BEFORE the flight; an uncommitted spec is dirt at step 0.

# 3. the weekly round pins — BUMP AND COMMIT BEFORE THE FLIGHT (§4.1, five pins named there)
git add -- engine/rl_after/ingestion/test_movers_transition.py ui/tests/movers.test.js
git commit -m "R24 weekly round pins bumped ahead of the advance (disclosed: these two suites are
   RED until the advance lands)" -- engine/rl_after/ingestion/test_movers_transition.py ui/tests/movers.test.js

# 4. the dry run — arms nothing, applies nothing
tools/land round --spec ACT_SPEC_R24.json --dry-run

# 5. THE FLIGHT.  <-- BLOCKED TODAY BY §3.1. Either the machinery is repaired first, or the
#    score file is seat-committed and this runs with --no-commit and a hand-made landing commit.
tools/land round --spec ACT_SPEC_R24.json \
  --report docs/evidence/r24_advance_<date>/REPORT.json \
  --log    docs/evidence/r24_advance_<date>/FLIGHT.log

# on any abort: move docs/evidence/.../ABORT_<step>.json aside, restore the prereg-lite if the
# sheet commit was rewound, fix the named cause, re-fly. Abort-then-retry IS the recovery; a
# landing that cannot complete after abort+retry is a round that SLIPS, on the owner's call.
```

**Wall clock:** ~25s pre-transaction self-test + ~4.6 min advance + ~12s everything else ≈ **5
minutes per flight**.

---

## 10. VERDICT — **GO-WITH-NOTES**

**The machine is sound.** Every postcondition it asserts held on a real round: the armed catch-up,
ADVANCE-REPIN building the balanced sibling and FV reference inside the same transaction, Guard 5,
FINALIZED with no exit-6, the ledger `+411` with zero duplicates, the disclosed generator sync, the
day-0 row diff, the contract restamp with ten frozen fields asserted unmoved, all five UI writers
with the identity read back out of the bundle, the movers page through the frozen template, the
state file regenerated and verified, nine claims recomputed GREEN, and 38 explicit paths every one
inside the carrier set. The abort ladder restored thirty carriers and a mid-flight commit byte-exact.
Two independent armed runs produced the same board.

**Three things must happen before the first real flight**, and none of them is a surprise any more:

1. **§3.1 — the input-commit pincer must be repaired by the machinery's owner seat, or the flight
   planned around it.** This is the only hard blocker. Left alone, R24 halts at step 0 or step 3.
2. **§4.1 — the five weekly round pins must be bumped and committed before the flight**, with the
   transient red disclosed.
3. **§5 — the day-0 question must be put to the owner**: a carried R24 emitter, or OFF.

And two to know rather than do: **§3.3** never export an `RL_`-prefixed lock flag near an armed
advance, and **§7** R24 closes the season calendar at `calendar_progress 1.0`.

Fly it with those three settled and the first real R24 contains nothing this rehearsal has not
already met.

---

## 11. THE LIVE TREE, ASSERTED BYTE-UNMOVED

Measured before the first flight and after the last, on `/home/user/afl-rl-engine`:

| identity | md5 | verdict |
|---|---|---|
| board `data/rl_build/rl_app_data.json` | `b3e8da99bc7f632e5d1eebc732f9cf01` | **UNMOVED** |
| store `engine/rl_after/rl_model_data.json` | `b745002eb0a0fbb1c34fa44f1ef708d6` | **UNMOVED** |
| engine head `engine/rl_after/_merged_recover.py` | `3af8c1f7d61275c198a5df70c34608c7` | **UNMOVED** |

Also unmoved and checked, because this act's flights wrote all of them inside the sandbox:
`engine/rl_after/rl_app_data.json` `b3e8da99…` · `data/expected_boot.json` `d749f42d…` ·
`docs/owner_annotations/SITTER_2026_v1.csv` `21361291…` · `data/sheet_pins.json` `a4ee39f7…` ·
`engine/rl_after/ingestion/test_movers_transition.py` `0fec509b…` · `ui/tests/movers.test.js`
`07ba31dc…` · `docs/evidence/final_candidate_2026-08-19/DAY0_CP.json` `210510fe…`.

`git status` on the live tree names exactly one path from this act:
`docs/evidence/r24_rehearsal_2026-08-21/`. Nothing under `docs/register/`,
`docs/OPEN_ITEMS_REGISTER.md` or `docs/proposals/rebake_study_B/` was read for writing or touched.

**The synthetic board `29c5ac7b`, the synthetic store `303a0765`, the synthetic balanced sibling
`578c7dbc` and the rendered `MOVERS_R24.html` were produced in the sandbox worktree and are
deliberately NOT filed here.** They are not a board of record and must never be mistaken for one, so
the sandbox worktree was removed and pruned when this report was written — only these transcripts,
specs and inputs survive it. Every identity above is quoted from the machine-recorded transcripts in
`flight_logs/`, which is where a reader re-derives them, and the whole rehearsal is reproducible from
`synthetic_inputs/make_synthetic_r24.py` (seed 20260824) plus the act specs.

---

## 12. WHAT IS IN THIS DIRECTORY

```
REHEARSAL_REPORT.md              this document
00_REHEARSAL_PREREG.md           the predictions, committed before the first flight
01_PREREG_LITE_SHEET_RECUT.md    the sheet re-cut's review-forcing step
act_specs/                       the four act specs flown (SYNTHETIC / RECUT / FULL / LEG2)
synthetic_inputs/                the generator, its metadata, R24_SYNTHETIC.csv, the sandbox env,
                                 and the movers-direction checker
flight_logs/                     RUN_A..F stdout + machine reports + transcripts, the lander's own
                                 08_preflight / 09_armed captures, the claims file and its check,
                                 the pre-transaction self-test summary, and the FIVE gate verdicts
                                 measured by hand on the landed R24 tree
aborts/                          the five ABORT_<step>.json records, one per halt
```
