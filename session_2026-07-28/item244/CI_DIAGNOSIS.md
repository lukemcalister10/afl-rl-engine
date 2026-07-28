# WHY THE THREE WORKFLOWS ARE RED — issue #244

**A report. Nothing was fixed.** Execution supervisor, cold seat, 2026-07-28.
Main at `4fe4781`, register v522, read against `docs/CURRENT_STATE.md` v14.

Everything below was measured on this seat by re-running, or quoted from the run's own log.
Where I could not establish something, it says so and names what is missing.

---

## THE HEADLINE — two premises in the directive are wrong, and they change the job

**1. They have not been red for a week. They went red today.**

All three workflows were **green at `a7dc1b4a`, 2026-07-28 04:25:55Z** — about ten hours before
main's current tip. They went red inside a **44-minute window** during the R20 go-live.

| workflow | last green run | first red run |
|---|---|---|
| CI Guards | `a7dc1b4a` · run 30328728550 · 04:25:55Z | `59d740ca` · run 30330714829 · 05:07:43Z |
| Final Integration | `a7dc1b4a` · run 30328728559 · 04:25:55Z | `59d740ca` · run 30330714807 · 05:07:43Z |
| Live Scoring | `a7dc1b4a` · run 30328728568 · 04:25:55Z | `69e84580` · run 30332689008 · 05:47:15Z |

Green at the five commits before that too (`0b48d9c2`, `cd869b18`, `9345881f`, `85e39ee0`,
`40a3da73`, back to 2026-07-27 14:52Z). Ancestry checked against `origin/main` after
`git fetch --unshallow`; all SHAs are on `origin/main` and the history is linear.

*(My first ancestry check said these SHAs were "not on main". That was the local `main` ref sitting
stale at `0a48d6a` — a container artifact, hazard 6. Corrected before it reached any finding.)*

**2. Somebody did look — but not at this.** `CI_MIGRATION_DIAGNOSIS.md` in the repo root is a
phase-1 diagnosis dated 2026-07-22 on branch `ci/harness-migration-r19`. It names causes for all
three workflows. **It is about a different era and is now overtaken** — its `ci-guards.yml`
finding (the hand-typed `2ab73a6f` board of record) was resolved; that line now reads the pin from
`data/expected_boot.json` and the file references `2ab73a6f` only as history. So the directive is
right in spirit — nobody has diagnosed *these* reds — but the repo is not a blank page.

**3. A caution on the established table.** Several cells in the directive's table say *cancelled*.
Those are `cancel-in-progress` concurrency cancellations from rapid pushes, not verdicts. A
cancelled run carries no information about pass or fail. Of the twelve cells in that table, the
three `cancelled` ones should be read as "not measured", not as "red".

---

## WHAT ACTUALLY BROKE — four root causes, not one

Established per job by re-running and by tracing the pins commit-by-commit. Not assumed from shape.

| # | cause | class | landed | hits |
|---|---|---|---|---|
| 1 | Kako 2026 anchor is an R19 constant | stale expectation | R20 go-live 04:44–04:47 | CI Guards |
| 2 | season-state R19 constants (`0.727` / `c120cfd5`) | stale expectation | R20 go-live | Final Integration |
| 3 | `_repo_root_of` resolves to `/` | real defect | `eb602b9` 04:44:26 | Live Scoring (1 job) |
| 4 | v0surf frozen-signature HALT | design working as intended | `f1b3aa7` 08:46:51 | Live Scoring (6 jobs) |
| 5 | release-contract identity drift | real inconsistency | `6634221` (#217) 09:43:36 | Final Integration |

**Causes 1 and 2 genuinely share a root**: both are R19-era constants that R20 invalidated when it
moved the store. That is one cause at two sites across two workflows.

**Causes 3, 4 and 5 are independent** — different mechanisms, different commits, hours apart.

**The single most important structural fact: two of the three workflows changed cause during the
day.** Final Integration's failure at `df1b1cc6` is not the failure it has now. Live Scoring's
first failure predates the v0surf freeze that its six proof jobs now die on. **A fix aimed at
today's top failure will not restore either workflow to green** — there is a queue behind it.

---

# CI GUARDS

**One job (`guards`), 1 of 1 red.** Fails at step 7 of 10.

**Quoted from run 30370092477, job 90311451861:**

```
SELF-TEST FAILED: 1 check(s)
  - Kako 2026 == 10 games @ 45.4 (R15-19 entered: R16=11,R17=9,R18=47,R19=57, R15 DNP;
    prior 6@55.0=330 +124 =454/10); got (11, 44.18)
```

**Class: stale expectation.** Site is `engine/rl_after/one_source_selftest.py:128` — a hard-typed
constant `ksc.get(2026)==(10,45.4)`.

**The evidence that distinguishes it from a data defect**, rather than an assertion that it is one:

- The arithmetic reconciles exactly. 10 games × 45.4 = 454; R20 added Kako's 32 → 486 over 11
  games = 44.18. That is precisely what the store now holds and precisely what the check reports.
- Line **127** — `Kako 2025 == 23 games @ 55.2` — still passes. Only the *current-season* line is
  stale. A data defect would not politely confine itself to the season that just advanced.
- The store legitimately moved: `rl_model_data.json` is now `e3aaba77`, and `data/season_state.json`
  correctly reads `as_of_round: 20`.

So the number in the store is right and the anchor is out of date. This is the round-scoped-anchor
problem `CURRENT_STATE.md` already records as live and uncommissioned. **This report changes nothing
about it except to confirm it is the sole thing reddening CI Guards.**

**What is hidden behind it** (hazard 9 — the suite halts, so the red map is not a completeness
claim). Steps 8–10 never ran in CI. I ran two of them on this seat:

- `ruling_config_check.py` → **PASSED** (`RL_PVCFIT=0` + R3 export bake-guard active)
- `config_manifest.py check` → **PASSED** (hash `45b207c03a8c`, 59 vars)
- `guard_correction_canary.py` and `run_panel.sh`/Guard 5 → **NOT MEASURED**. Both need a full
  bootstrap and engine build; I did not run them. That is an honest gap, and it is the one place
  where CI Guards could be hiding a second failure.

Within `one_source_selftest.py` itself, every other check printed PASS — including the whole
pricing-split and Addendum-1 block, the frozen-ruler contract, and the G-Y0 national-curve leg at
0.730% against a 2% hard bar. **1 of 1 checks failing in that suite, on a suite that otherwise
reports clean.**

---

# FINAL INTEGRATION

**One job (`final-integration`), 1 of 1 red.** Currently fails at step 9 of 20 — the first
substantive step. Sixteen steps have not executed since `6634221`.

## Its cause changed at #217. There are two, stacked.

**Current failure, quoted from run 30370090865, job 90311364971:**

```
RELEASE-CONTRACT CHECK: FAILED
======== RELEASE CONTRACT (gate) REJECTED — BUILD HALTED ========
  - contract identity board=8a38cca44f53 != expected_boot 750446d74e7c (stale pin)
  - contract identity engine_head=7c452715dc98 != expected_boot 444831d5402a (stale pin)
  - contract identity rl_model=4f776e073ea5 != expected_boot eb1e065a398a (stale pin)
```

**Original failure, quoted from run 30343957111 at `df1b1cc6` — a different step entirely:**

```
RESULT: 24/25 PASS  -> session_2026-07-21/final_integration/evidence/season_progress_inventory.json
```

I established the change of cause by tracing both pin files commit by commit rather than inferring
it from the logs:

| commit | release_contract.json | expected_boot.json | |
|---|---|---|---|
| `a7dc1b4a` last green | `fa172ac1`/`7c452715`/`4f776e07` | same | SAME |
| `fef7f69` R20 go-live | `8a38cca4`/`7c452715`/`4f776e07` | same | SAME |
| `59d740ca` first red | `8a38cca4`/… | same | SAME |
| `df1b1cc6` pre-#217 | `8a38cca4`/… | same | SAME |
| **`6634221c` #217** | `8a38cca4`/`7c452715`/`4f776e07` | `750446d7`/`444831d5`/`eb1e065a` | **DRIFT** |
| `4fe47816` HEAD | unchanged | unchanged | DRIFT |

The two files were byte-consistent through the entire R20 go-live and diverged **only at #217**.

### Cause 5 — the release-contract drift. This is the finding the owner should care about most.

**#217 moved `data/expected_boot.json`'s board / engine_head / rl_model pins and did not move
`data/release_contract.json`.** The release-contract gate detected that on the very commit that
introduced it.

I am deliberately **not** calling this a "stale pin" despite the error text saying so, because the
evidence does not settle which side is wrong:

- The shipped UI bundle `ui/data/board_view_working.js` stamps `board_md5: 8a38cca44f53` and
  `asOfRound: 20` — it **agrees with the release contract**, not with `expected_boot.json`.
- #217's own note inside `expected_boot.json` says: *"THE BOARD MOVE IS NOT MADE HERE: no balanced
  reference, no UI bundles…"* — i.e. the board move was deliberately not propagated.
- So `expected_boot.board = 750446d7` names a board that is **not the one shipped**. Whether the
  right correction is to re-stamp the contract or to reconsider the boot pin is an owner call about
  what #217 intended, not something I can settle from the artifacts.

**This is a guard doing exactly its job, catching a real inconsistency in a landing, on the day it
landed — and nobody saw it, because the workflow was already red for an unrelated reason.** That is
the concrete cost of the wall of red, measured rather than asserted.

### Cause 2 — the season-state R19 constants, and they are duplicated

Reproduced on this seat. Locally the suite is now **23/25**, not CI's 24/25 — a second check has
broken since `df1b1cc6`:

```
FAIL (a) R19 (current store c120cfd5) exposure_pace == 0.727, calendar_progress == 0.79
FAIL (e) the fully coherent positive fixture PASSES release_contract.verify (baseline)
```

- **FAIL (a)** — `session_2026-07-21/final_integration/tests/season_progress_test.py:73-75`.
  The store is now `e3aaba77`, not `c120cfd5`. `season_state.derive(19)` returns
  **`exposure_pace 0.773`**, not 0.727 (calendar_progress 0.79 is still correct). The committed
  `data/season_state.json` is right and current: round 20, calendar 0.83, exposure 0.773.
  **Class: stale expectation**, same root as the Kako anchor — an R19 constant that R20 moved.
- **FAIL (e)** is a **cascade of the release-contract drift**, not an independent fault. It is the
  positive control that proves the fail-closed tests are not vacuous. The drift has **disabled a
  non-vacuity control** — the check that exists to prove the other five can fail. Worth naming: a
  broken baseline makes five neighbouring PASSes mean less than they appear to.

**The same stale constants are duplicated into the workflow YAML.** `.github/workflows/
final-integration.yml:154` inlines `calendar_progress==0.79 and exposure_pace==0.727 and
source_store_md5 startswith 'c120cfd5'` at a *later* step. **Two executable sites, hazard 2.**
Repairing the test file alone leaves the workflow's own copy red at step 15. (A third hit at
`acceptance_matrix.py:164` is prose inside a detail string, not an assertion — checked, not assumed.)

**So Final Integration is a chain of at least three blockers**, in the order a repair would meet
them: release contract → `season_progress_test` FAIL (a) → the inline YAML assertion. Steps beyond
are unmeasured. Not everything downstream is broken — I ran `ui/tests/extract_seam.test.py` on this
seat: **42/42 passed**.

---

# LIVE SCORING

**Seven jobs, 7 of 7 red.** Two causes, cleanly split 1 and 6.

## `live-scoring-light` — cause 3, a real defect

Fails at step 10 of 16; steps 11–15 skipped. **Quoted from job 90311363194:**

```
File ".../engine/rl_after/ingestion/round_movers.py", line 673, in accumulate_bundle
  bundle['points'], bundle['values'] = build_points_block(repo_root or _repo_root_of(path))
File ".../engine/rl_after/ingestion/round_movers.py", line 560, in build_points_block
  vh = _load(os.path.join(ing, 'value_history.json'))
FileNotFoundError: [Errno 2] No such file or directory: '/engine/rl_after/ingestion/value_history.json'
```

Reproduced byte-identically on this seat, down to the same synthesized `/engine/…` path.

**Mechanism.** `_repo_root_of` (`round_movers.py:529-531`) walks up exactly three directories,
assuming the path is `<repo>/ui/data/movers.js`. The test hands it a shallow temp path, so it walks
past the root and lands on `/`. `os.path.join('/', 'engine', …)` then yields an absolute path that
does not exist.

**Class: real defect — a contract regression, introduced by `eb602b9` (04:44:26), the Movers
from/to rework.** Before that commit `accumulate_bundle` needed no repo root; the rework added the
dependency without hardening the fallback or updating the caller.

**Blast radius — measured, and it is narrower than it looks.** I enumerated every caller:

- `round_movers.py:747` and `round_finalize.py:314` — **the two production callers — both pass
  `repo_root=` explicitly.**
- Only `test_weekly_updater.py:227` relies on the fallback.

**So the weekly ingest is not affected.** This is a genuine regression correctly caught by the
test, but it breaks the test harness, not the shipped path. That distinction matters for how
urgently it is worth anyone's time.

**Hidden behind it** — CI has never run the four skipped steps. I ran the Movers acceptance proof
on this seat and found a **further real failure CI has never reported**:

```
[FAIL] 0_production_populated_and_provenance_bridge
[PASS] 1_one_report_per_round … [PASS] 9_no_silent_overwrite, [PASS] csv_reports
```

**1 of 11 checks failing**, invisible behind the first halt. Textbook hazard 9.

## The six `proof-*` jobs — cause 4, all identical

`proof-catchup`, `proof-two-round`, `proof-storewrite`, `proof-failure-injection`,
`proof-finalization-injection`, `proof-fv-provenance`. Each fails at its own step 10.

Reproduced all six on this seat under a Python 3.12.3 venv built from `requirements-lock.txt` with
`--require-hashes --only-binary=:all:`, with `/home/claude` seeded exactly as the workflow does.
**All six produce the identical halt:**

```
v0surf FROZEN-SIGNATURE HALT: this build's config signature 65b9fbafa89b29ac1aba16fdf29564e6
is NOT in data/v0surf.pkl (frozen: 1cbaf33de27ad9a2ccadf7cc98f57314, 76498b5a7a7a80db17f5bb9748ff1492).
```

Confirmed against CI: job 90311363264's log ends on the same halt text.

**Class: the design working as intended — and therefore a finding, not a fault.** The directive said
so in advance and it is right. `f1b3aa7` (08:46:51) froze v0surf and deleted the silent refit
fallback. The live-scoring proofs regenerate a board inside a staged scratch workspace, and that
build computes a **third** config signature that was never baked into the frozen set of two.

**The consequence is structural, and it is the part worth acting on: these six jobs cannot pass in
their current form.** They are not testing catch-up, store writes, crash recovery or FV
provenance — they all halt at the same import-time gate before reaching any of it. Six parallel
runners are producing one bit of information, repeatedly.

**Duration — a finding, as the directive asked.** The directive warned some `proof-*` jobs are long.
**Right now they are not.** Each fails in **25–28 seconds** (CI step times: 26–29s; my
reproductions: 25–28s). They die early. Their true runtime is therefore **unmeasured** — the
~86-minute figure in `CURRENT_STATE.md` cannot be confirmed or refuted from any recent run.

---

# WOULD THEY HAVE CAUGHT ANYTHING REAL?

The question the directive says actually matters. Answered per workflow, from what they did catch
today.

**CI Guards — yes, and the mechanism has value, but the anchor is the wrong shape.**
The Kako check is a genuine owner-ground-truth anchor against the store; it is the one guard
positioned to catch a bad score ingest. It fired correctly. But its expectation is a hand-typed
current-season constant, so **it will red on every single round application, forever**, and each
time it will be a false alarm about a legitimately moved store. That is precisely the
maintenance-burden pattern the governing test warns about. The mechanism is worth keeping; the
hand-typed constant is not. `CURRENT_STATE.md` already names the fix and the precedent (#208
round-scoping the Bailey Williams override), and the anchor must not derive its expectation from
the store — that would make it vacuous.

**Final Integration — yes, unambiguously, and it is the strongest case of the three.**
It caught a real identity inconsistency introduced by #217 on the day #217 landed, and the finding
was lost in the noise. This is the exact failure mode the owner described: a change merged against
no signal. Had this workflow been green, #217's drift would have been a red on a green board and
impossible to miss. **This is the one I would argue hardest against deleting.** Its release-state
closure is doing real work that nothing else in the tree does.

**Live Scoring — split, and the two halves deserve opposite answers.**
- `live-scoring-light` caught a real regression from the Movers rework within minutes of it landing.
  That is a working test. Keep it.
- The six `proof-*` jobs currently catch nothing, cannot catch anything, and each burns a runner to
  re-report the same halt. They are not broken tests — they are tests that the v0surf freeze has
  made unrunnable.

---

# ON DELETION

**I did not find the thing the directive left room for.** The deletion case was framed as: red for
weeks, nobody noticed, would not have caught anything. **No workflow here fits that.** They have
been red for ten hours, and two of them caught real problems in that time. On the evidence, "delete
it" is not the right answer for any of the three, and I am not going to manufacture one to fill the
slot.

**But there is a related recommendation the evidence does support, and it is not "fix it".**

The six `proof-*` jobs are structurally incompatible with the frozen v0surf. There are three honest
options and they are the owner's to pick, not mine:

1. **Bake the staged-build signature** into `v0surf.pkl` — makes them runnable again, at the cost of
   widening the frozen set, which is exactly what the freeze exists to prevent.
2. **Stop running them on every push.** They were built as one-off proof harnesses for the
   weekly-updater work. `CURRENT_STATE.md` already records that the proof harnesses are "wired to
   nothing". Running six of them on every commit to re-report one halt is upkeep with no return —
   and the governing test says price the upkeep before keeping the guard.
3. **Leave them.** Defensible only if someone intends to resolve the v0surf interaction soon.

My read, offered as a recommendation and nothing more: **option 2 for the six proof jobs**, keep
`live-scoring-light`. That is the closest thing to a removal finding in this diagnosis, and it is a
de-scoping, not a deletion.

---

# WHAT IT WOULD TAKE TO GET BACK TO GREEN

Stated as a map, not as a plan, and **not authorised by this job.** Note the ordering — each
workflow has a queue, and the counts below are what is *currently visible*, which hazard 9 says is a
floor and not a total.

| workflow | blockers currently visible | notes |
|---|---|---|
| CI Guards | 1 (Kako anchor) + 2 steps unmeasured | round-scope the anchor; do not retype the number |
| Final Integration | 3, stacked | contract drift needs an owner decision first |
| Live Scoring | 2 causes over 7 jobs | 6 of 7 need a v0surf decision, not a code fix |

**The single cheapest thing that buys the most signal**, if the owner wants one move before the
positional rebuild starts: **resolve the release-contract drift**. It is one file, it is the top
blocker on the workflow with the best catch record, and it is currently masking a stale constant and
a disabled non-vacuity control behind it.

---

# GAPS — what I did not establish

Named honestly, because a confident guess is worth less than a stated hole.

1. **`run_panel.sh` / Guard 5 and `guard_correction_canary.py` were not run.** They need a full
   bootstrap and engine build. If CI Guards has a second failure, it is in one of those two.
2. **Final Integration's steps 10–20 are unmeasured**, beyond `extract_seam.test.py` (42/42) and the
   inline YAML assertion at line 154, which I read but could not execute. I cannot say the chain is
   only three deep.
3. **The true runtime of the `proof-*` jobs is unknown.** They have not completed a full pass in any
   recent run.
4. **I did not determine why the staged build produces config signature `65b9fbaf…`** — only that it
   does, deterministically, in all six proofs. Identifying what in the staged workspace moves the
   signature would tell you whether option 1 above is even sound.
5. **Whether `expected_boot.json` or `release_contract.json` holds the correct board is not
   resolvable from the artifacts.** It depends on what #217 intended. That is an owner question.
6. **Run history was read to 30 runs per workflow** (of 664 CI Guards / 167 Final Integration / 167
   Live Scoring total). Green at `a7dc1b4a` is established directly; I did not walk the full history
   before 2026-07-27 14:52Z and make no claim about it.

---

# FENCE COMPLIANCE — including one thing I have to disclose

Nothing was repaired. No workflow, test, engine, store or board byte was edited. `git status` is
clean; the only files created are this report and its directory.

**One disclosure.** Running `season_progress_test.py` to reproduce the failure caused the test to
write its own evidence file, `session_2026-07-21/final_integration/evidence/
season_progress_inventory.json`. That was an unintended write inside the fence. **I restored it with
`git checkout --` immediately and verified the tree clean.** Every subsequent proof was run without
`--write` for exactly this reason, and `git status` was checked after each batch. Recording it
because a fence breach that only I know about is worth less than one written down.

---

*Read current to register v522, main `4fe4781`. Every figure above was re-derived on this seat or
quoted from the named run's own log. Screened by re-running, not by reading.*
