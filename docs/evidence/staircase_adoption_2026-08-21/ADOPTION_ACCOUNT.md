# THE STAIRCASE FIX ADOPTION — VARIANT A RAW. THE ACCOUNT.

**Seat:** adoption seat, THE STAIRCASE FIX (ORDER 44) · **Date:** 2026-08-21
**Register:** v808 — **NOT touched by this seat.** **NOT PUSHED.**

> ## STATUS: **THE FLIP IS COMMITTED. THE LANDING IS STILL NOT DONE.** *(updated after the re-fly, §9)*
>
> **THE BOARD HAS NEVER MOVED.** It is still `68be10c79d0ee096455754e084bcf757` / **692,296** / **804**;
> the store is `b745002e`, unmoved; `engine_head` `8f591805`; contract `4cbc7f27`; balanced `556ad70d`.
> The engine default **is** flipped (committed at `531235c`), so the tree remains in the declared
> intermediate state: **dial ON in source, board not yet rebuilt.**
>
> **ATTEMPT 1** ran the full transaction and **ABORTED at step 7 of 10 (`gates`)**, restoring every
> carrier **byte-exact** — verified independently by this seat, not merely claimed by the lander. The
> abort was **not caused by the act**; every proof the act owns passed (§4).
>
> **THE RE-FLY (§9) FIXED BOTH MACHINERY DEFECTS AND THEN DID NOT FLY.** `0abf099` cuts the self-test
> recursion (F-1) and gives the gate run evidence capture (F-5); `bd299a9` closes the `/tmp` sandbox leak
> — **which the brief believed was already cleared and was not: 138 directories, 1.4 GB.**
>
> **THE LANDING IS BLOCKED BY ITS OWN NEW PRECONDITION, AND THE BLOCK IS REAL.** The ruling's second half
> — *the lander runs the self-test standalone before the transaction, fail = no transaction opened* —
> **cannot be satisfied until this landing lands.** Since the prereg restamped the contract, the sibling
> sidecar has been stale, so even a NO-OP sandbox landing must reconcile, which **builds** — and with the
> flip committed that build produces `b3e8da99` while a no-op's pin stays `68be10c7`, which
> `sibling_repin`'s conformance gate correctly refuses. **P9 puts every dial-flipping landing in that
> same window**, so the gate as ruled blocks the whole class, not just this act. Every abort in the
> self-test was still **byte-exact**: the lander is sound; the self-test's premise is not.
>
> **THIS SEAT DID NOT BYPASS THE GATE IT HAD JUST INSTALLED** to pass its own act. The ruling was given
> on a premise that was true at `efbe1b6` and stopped being true nine and a half hours later at the flip.
> **It is returned to the pen with the measurement — §9.4, §9.6.**

---

## 1 · THE COMMITS

| | sha | what |
|---|---|---|
| **prereg** | `fb3d3c0` | adoption prereg **+ the A-raw no-arb and class reading**, before the engine edit (P9) |
| **flip** | `531235c` | one engine commit: `RL_O44_LVLMONO` default `'0'` → `'ratchet'`, **restamp riding it** |
| **landing** | **NONE** | attempt 1 aborted at `gates`; the re-fly never opened a transaction. **The lander has committed nothing.** |
| **tooling** | `0abf099` | the self-test recursion cut (F-1) + the gate run's evidence capture (F-5) |
| **tooling** | `bd299a9` | the `/tmp` sandbox leak closed at both ends — 138 dirs / 1.4 GB |
| evidence | *(this commit)* | both attempts' full record |

---

## 2 · THE OWNER'S RE-RULING

This seat ran **twice**. Run 1 (variant B raw) **halted before its flip** at `36f1122` when the B-raw
no-arb reading was measured for the first time and showed **four** new buy-rail breaches, none removed.
The owner was shown it, the A/B difference was re-explained, and he re-ruled, **verbatim**:

> **"I misunderstood the A and B difference. I think based on those explanations, A raw I prefer. Lock
> that in, unconserved."**

**A measurement taken before the board moved changed a decision.** With it:

> **"in principle I don't like 'enforcing conservation' as that's another mechanism that gets baked in...
> If we want to conserve, I'd prefer to find a lever to remove value that works on its own"**

> **"happy to waive the no arb reading for this"**

— the second given **after** the supervisor told him A raw was expected to breach similarly to B raw.
**The waiver covers the band rails. It does not cover the class law (F4), and it does not cover
measurement.** Both were honoured: F4 was checked before the flip and **passed**; the full reading was
emitted anyway.

**LAW 9, stated not netted:** the adopted board mints **+8,460 SCAR = +1.2220 %**, **42.3×** the 200-SCAR
rail. A breach on its face, **accepted by owner word**. A raw is the arm the owner's own "1.22 %" was
quoted from.

---

## 3 · THE PRE-FLIP MEASUREMENT — all halt conditions cleared

Emit `SFX_LABEL=SFXARAW RL_O44_LVLMONO=ratchet`: **exit 0, 5m22s**, matrix `a756078e`. All instrument
checks **PASS**; ORDER K reproduced at difference **0.0000**.

**F4 CLASS LAW — PASS.** W2 **1.0943**, floor +0.0643, rail −0.0457 (live 1.0738 · B raw 1.0952 ·
A con 1.0829 · B con 1.0838). **Inside 1.03–1.14.**

**DAY-0 — HELD.** 87 of 87 wired entrants at tolerance 0. No reference re-based.

**BAND RAILS — waived, measured anyway.** Three new ND crossings on the standing PRIMARY basis
(picks 1-20 +12.98→**+14.94 %**; picks 1-10 +13.12→**+14.87 %**; picks 11-20 +12.71→**+15.08 %**);
**zero** new pool-arm crossings. `PRIMARY IRE`, which crossed under B raw at +14.18 % and failed the
owner's path test there, reads **+13.63 %** under A raw and does not breach. Breaches removed: **NONE**.

**A raw reads lower than B raw on every cell in both tables** — 3 new breaches and 0 new path-test
failures against B raw's 4 and 1. **Not dressed up as a pass:** three top-of-draft cells still move fair
→ buy-side red, and nothing is repaired on the buy side.

---

## 4 · THE LANDING ATTEMPT

`tools/land lever --spec …/ACT_SPEC_A_RAW.json`, started 01:02:15Z. **Total 2,223 s (37.1 min).**

| # | step | seconds | verdict |
|---|---|---|---|
| 0 | preflight | 0.1 | **OK** |
| 1 | build_proofs | 221.1 | **OK** |
| 2 | pins | 0.0 | **OK** |
| 3 | lineage | 0.3 | **OK** |
| 4 | contract | 0.1 | **OK** |
| 5 | sibling | 280.5 | **OK** |
| 6 | ui | 0.2 | **OK** |
| 7 | **gates** | **1,720.8** | **FAIL → ABORT** |
| 8 | claims | — | not reached |
| 9 | commit | — | not reached |

*(Baseline for scale: the no-op rehearsal was 9.4 min. This act's two real builds plus the sibling
rebuild account for 502 s of the difference; `gates` accounts for the rest and is the story.)*

### 4.1 Every proof the act owns — MET

* **F1 — the prediction.** Bare build (`RL_O44_LVLMONO` unset, no model-semantics `RL_*` at all) →
  **`b3e8da99bc7f632e5d1eebc732f9cf01`**, **byte-exact** against the prereg, **139.1 s**.
  **700,756 / 804 rows.**
* **F2 — the kill-switch.** `RL_O44_LVLMONO=0` → **`68be10c79d0ee096455754e084bcf757`** byte-exact, 82 s.
* **F3 — the positive control.** switch-off ≠ switch-on. Held.
* **THE FOUR NAMED ROWS**, read out of the built board: **Kondogiannis 409 · Dolan 311 · West 383 ·
  Hayes 250.** All four rise. Exactly as predicted.
* **Day-0** — `off`, no reference regenerated.
* **pins** — `board` moved; **10 declared-unmoved identities checked, 0 moved**; byte-check confirmed only
  the declared pin bytes differed.
* **lineage** — column `the-staircase-adoption-21-8` registered; register entry appended (13 entries);
  chain verified with **no bridge needed**; `moved_by_transition = ['board']`.
* **contract** — seal `4cbc7f27` → `213443de`; `release_contract.py check` **PASS**; frozen fields unmoved.
* **sibling** — reconciled, **balanced `556ad70d` → `7c32a540578b799922daea41d8acdfa2`** (F8 satisfied,
  the sibling did move); 8 fails before → **0 after**; 9 targets committed.
* **ui** — both writers ran; the html bundle's own embedded identity read back as **`b3e8da99…`**.

### 4.2 Why `gates` red — and it is not variant A

The acceptance runner returned **RED, 15 PASS / 2 FAIL**. Everything that judges the landed state passed:
`release_manifest`, `boot_guard_checkout`, `config_manifest`, `ruling_config`, `release_contract_seal`,
`store_coherence_six_way`, `doc_lint`, `rulebook_lint`, `ruled_red_ledger`, `inbox_manifest`,
`mirror_parity`, `dial_coverage`, `oneliner_gamma`, `oneliner_f1_lens`, **`build_twice_determinism`**.

The two failures:

1. **`lander_selftest` — `TimeoutExpired`.** **A STRUCTURAL FINDING, not a flake.** The acceptance runner
   registers `lander_selftest`, and the lander runs the acceptance runner as a gate. So
   **`land lever` → `gates` → `acceptance.runner` → `lander_selftest` → seventeen nested `land lever`
   runs in sandboxes.** Every real landing pays for a full re-proof of the lander itself, inside itself.
   That is what made `gates` cost 1,720 s, and under a contended box it exceeded its own timeout. It also
   **leaked**: a nested sandbox lander outlived the killed parent and was still running minutes later
   (pid 28621, `/tmp/landing_selftest_14673`), alongside **eleven** leftover sandbox trees in `/tmp`.
2. **`oneliner_r14_restore` — FAIL.** **Not pre-existing: it PASSES in isolation on the restored tree**,
   re-run by this seat immediately after the abort (`50 [PASS], exit 0, GREEN`). It failed only while the
   landed state was live. The check shells out to `engine/rl_after/ingestion/test_weekly_updater.py`,
   which delegates to `test_movers_transition.run_all()` — the suite that reads `ui/data/movers.js`,
   `ui/data/movers_transition.js`, `data/release_lineage.json` and `data/expected_boot.json` together.
   **The precise failing assertion was not recovered** and this seat will not guess it: the runner ran
   with `evidence: (none)`, so the check's own `oneliner_r14_restore.txt` was never written to the repo.
   **Two candidate causes remain open** — a genuine coupling between a board-moving lever landing and the
   movers mirror (which the 2b round lander, *not built*, is the writer of record for), or contention
   from the concurrent seat. **Distinguishing them requires the landed state again, so it is a question
   for the re-run, and it is flagged rather than assumed.**

### 4.3 The abort itself — **the lander's best moment**

`byte_exact: true`. The abort report is `ABORT_gates.json` (full restore-point manifest, 60+ carriers).
**This seat verified the restoration independently** rather than trusting the flag — re-hashing every
carrier against the flip commit `531235c` via `git show`:

```
board 68be10c7 · store b745002e · engine_head 8f591805 · expected_boot · release_contract ·
release_lineage · value_history · board_view_working · board_view_public · test_fv_provenance.py
      → ALL 10 RESTORED BYTE-EXACT.   git status: no carrier modifications.
```

**On its first real landing the lander detected a red it did not cause, refused to proceed, and put the
tree back exactly as it found it.** That is the property the whole package exists for, and it held.

---

## 5 · WHY THE RE-RUN DID NOT HAPPEN

**The shared tree is actively owned by another seat.** At the time of writing it carries **13 uncommitted
foreign paths** — `ui/app/{board,card,config,movers,seam,trade,v0}.js`, `ui/index.html`,
`ui/tests/ui_defects_2026-08-21.test.js`, `ui/tools/gen_v0_sidecar.py`, `ui/data_aux/`,
`docs/evidence/ui_work_2026-08-21/`, `docs/proposals/ui_backlog/UI_PARKED_2026-08-21.md` — and that seat
is **still writing** (files touched 01:42:21) and **running its own `acceptance.runner`**, holding the
build lock.

Two independent hard blocks follow, both by the lander's own design and both correct:

1. **`preflight` asserts a clean tree** (`is_ignorable_dirt` returns `False` for everything, deliberately:
   *"Nothing is ignorable. Kept as one named place so an exception can never be added quietly."*). A
   re-run aborts in 0.1 s.
2. **`commit` refuses foreign paths** — *"THE TREE CARRIES CHANGES THIS LANDING DID NOT MAKE, and an
   explicit-path commit will not sweep them up."* Even with green gates, step 9 would abort.

**Clearing that tree is not this seat's to do.** Committing, stashing or reverting another seat's live
work to make my own landing runnable is precisely the improvisation the brief forbids, and it would
destroy work in progress. **So the act stops here and reports.**

---

## 6 · WHAT THE RE-RUN NEEDS

1. **A quiet tree.** The UI seat commits or pauses; `git status` clean.
2. **A ruling on the nested self-test.** `lander_selftest` inside `land lever`'s own gate set is what red
   this landing. It is a **declared spec slot** (`gates`), so it *can* be scoped — but **narrowing a gate
   set to make one's own landing pass is exactly what this estate refuses**, and this seat will not do it
   on its own initiative. The supervisor should rule: either the runner's `lander_selftest` is excluded
   from the lander's own gate profile (it is re-proving the instrument that is running, and it already
   ran green standalone at `efbe1b6`: 10/10 byte-exact aborts, 17 PASS / 0 FAIL), or its timeout is
   raised to cover a loaded box.
3. **`oneliner_r14_restore` re-observed with evidence captured**, so the failing assertion is *read*, not
   inferred. If it is the movers-mirror coupling, that is a **lever-landing-vs-2b gap** and a finding in
   its own right.

Everything else is ready and unchanged: the prereg and its predictions are committed at `fb3d3c0`, the
flip at `531235c`, and the act spec validates clean against `tools/landing/spec.py`.

---

## 7 · FINDINGS

**F-1 · THE LANDER RUNS ITS OWN SELF-TEST INSIDE EVERY LANDING.** `land lever` → `gates` →
`acceptance.runner` → `lander_selftest` → 17 nested `land lever` runs. It dominated the cost (1,720 s of
a 2,223 s transaction), it timed out, and it **leaked an orphaned nested lander plus eleven sandbox trees
into `/tmp`**. Re-entrancy of an instrument through its own gate set is a design question, not a flake.

**F-2 · THE ABORT PATH IS PROVEN ON A REAL ACT.** Byte-exact restoration of 60+ carriers after a
mid-transaction red, independently verified. First real landing; the safety property held.

**F-3 · THE CLEAN-TREE CONTRACT AND SHARED-WORKSPACE CONCURRENCY ARE IN TENSION.** The build lock
serialises *builds*; nothing serialises the *working tree*. A landing that takes 37 minutes on a box
where other seats edit files cannot rely on the tree still being clean at step 9. Either landings need a
tree-level lease, or the estate needs a convention that a landing has exclusive tenancy while it runs.

**F-4 · `engine_head` MOVES OUTSIDE THE MEASURED TRANSITION** (carried from run 1, and it held in
practice): P9 forces the engine edit into its own commit and `preflight` demands a clean tree, so the
flip is already `HEAD` when `_measure_sides` reads its source side. The flip commit **must** carry the
restamp — it did, and `lineage` passed as a result — and the landing must declare `engine_head` unmoved,
with the lineage invariants saying in words why.

**F-5 · A GATE THAT FAILS ONLY INSIDE A LANDING IS INVISIBLE WITHOUT EVIDENCE CAPTURE.**
`oneliner_r14_restore` passes standalone and failed only in-transaction, and the runner's `evidence:
(none)` meant the check's own output was never persisted. The lander should point the runner at its
evidence dir so a gate red is diagnosable from the record instead of by re-running a 37-minute act.

---

## 8 · A PROVENANCE DEFECT IN THIS FILE'S OWN COMMIT — RECORDED, NOT REWRITTEN

**The nine evidence files above, including this account, were swept into another seat's commit.**

This seat staged them with `git add -- docs/evidence/staircase_adoption_2026-08-21/` and then ran
`git commit`. Between those two calls the concurrent UI seat committed with a non-explicit-path stage,
and **its commit `19e5abe` ("UI (a) + (3) — MOVERS: participation becomes tri-state…") carries all nine
of this landing's evidence files alongside `ui/app/movers.js`.** This seat's own `git commit` then found
an empty index and made no commit at all.

**NOTHING WAS LOST OR CORRUPTED.** Verified: the committed `ADOPTION_ACCOUNT.md` is byte-identical to the
file on disk (`md5 45de53e3…`), all nine files are present in `HEAD`, and the landing's carriers are
untouched — board `68be10c7`, engine_head `8f591805` (the flip), `expected_boot e0965d29`.

**THE HISTORY IS NOT BEING REWRITTEN TO TIDY THIS.** An amend or rebase with another seat actively
committing to the same branch is how a real loss gets manufactured out of a cosmetic one. The record is
corrected the way this estate corrects records: **by saying what happened, where the bytes actually
live, and leaving the commits alone.**

**THIS IS FINDING F-6**, and it is the same failure mode as F-3 seen from the other side. The lander is
rigorous about this — explicit paths only, and `commit` aborts outright on any path it did not write
(*"THE TREE CARRIES CHANGES THIS LANDING DID NOT MAKE, and an explicit-path commit will not sweep them
up"*). **But that discipline protects only the seat that has it.** Nothing in the estate stops a
hand-driven seat from staging broadly and sweeping up a neighbour's in-flight work, and **`git`'s index
is a single shared mutable object with no lock at all** — the build lock does not cover it, and neither
does anything else. Two seats committing to one working tree share one index; the loser finds out
afterwards. The estate needs either a tree-level lease for the duration of an act, or a standing rule
that every commit everywhere is explicit-path — the same rule the lander already enforces on itself.

---

## 9 · THE RE-FLY, 2026-08-21 02:00–02:30Z — **THE TWO FIXES LANDED. THE LANDING DID NOT.**

The tree was quiet, the disk was clear, both machinery defects named in §6 were repaired and committed,
and the landing **still did not fly** — stopped by its own newly-installed precondition, for a reason
neither §6 nor the ruling that answered it knew about. **This section is that reason, measured.**

### 9.1 · The two machinery fixes — committed

| sha | fix |
|---|---|
| `0abf099` | **THE SELF-TEST RECURSION, CUT** — F-1, on the supervisor's ruling; and **F-5**, the gate run's evidence capture, in the same commit |
| `bd299a9` | **THE LANDER CLEANS UP AFTER ITSELF** — the `/tmp` sandbox leak, closed at both ends |

**THE RULING, IMPLEMENTED IN BOTH HALVES, VERBATIM:**

> *"The lander's self-test moves OUTSIDE the landing transaction: a check that validates the lander by
> running seventeen practice landings must never run INSIDE a real landing (recursion, not coverage). It
> remains a registered runner check for every push/standalone run; the IN-TRANSACTION gate profile
> excludes it, and the lander runs it ONCE, standalone, immediately BEFORE opening the transaction (fresh
> proof, no recursion). Coverage identical, knot removed."*

* **(i) excluded in-transaction.** `acceptance/runner.py` gains a third profile, `in-transaction` —
  `full` minus the checks that open a landing. A **filter, not a fake verdict**, on the same terms as the
  existing `host-insensitive` profile: the excluded check is not run and not reported, and the table's
  header names the profile that produced it. Membership is `IN_TRANSACTION`, **default TRUE**, so a new
  check cannot drop out of a landing's gates by forgetting an attribute. **Measured: 17 registered
  checks, 16 selected, exactly `lander_selftest` excluded.**
* **(ii) run standalone, before.** `cli.cmd_lever` runs it once before constructing the transaction;
  failure exits with **no transaction opened**. Skipped for `--selftest` runs and only those. Its
  transcripts are written **outside the repo** and filed into the evidence dir after the transaction
  closes — writing them into `docs/evidence/` directly would leave untracked files in the tree and
  **step 0 asserts a clean tree**, so the lander's own proof would have red the landing it was proving.
* **F-5.** A gate argv may now carry `@EVIDENCE@`, substituted for a per-gate directory inside the
  landing's evidence dir; the default acceptance gate carries it, and the `StepError` names the path.

**Verified with the fixes in place:** `acceptance/selftest.py` **84 PASS / 0 FAIL**;
`--profile host-insensitive` **14/14 GREEN**; `oneliner_r14_restore` **PASS standalone (50 [PASS])**.

### 9.2 · The leak premise was false, and was checked rather than taken

The re-fly brief stated the leaked sandboxes had already been removed. **They had not.** `/tmp` carried
**138 `landing_work_*` directories totalling 1.4 GB** — every landing and self-test since the package was
built — on a disk that had been hand-cleared to 12 G to make room for this re-fly. One more was created
during this session when a self-test was killed at a tool timeout, leaving `/tmp/landing_selftest_1151`
and its worktree behind.

`bd299a9` closes it at both ends, because one end is not enough: the transaction discards its own work
dir **only once the restore point has done its job** (landing complete, or abort proved byte-exact — an
**unproved** abort keeps it, because that is exactly when a human needs it), and
`txn.sweep_orphan_sandboxes` runs at the **start** of every landing and self-test, since a `SIGKILL`ed
run executes no `finally` block on the way out. The sweep decides by **liveness of the owning pid** —
every dir is named `<prefix><pid>` — and leaves a live pid strictly alone. Verified in flight: with a
self-test running it spared both that sandbox and its child's work dir. **1.4 GB reclaimed.**

**PROVED END TO END.** The self-test in §9.3 ran **twelve landings** — one control, ten fault cases, one
depth case — plus its own sandbox worktree. **It left ZERO directories behind**: `/tmp` holds no
`landing_work_*` and no `landing_selftest_*`, `git worktree list` shows no sandbox, and the disk is
unchanged at 13 G free. The same run before this fix would have left a dozen.

### 9.3 · THE STANDALONE SELF-TEST DOES NOT PASS — and the cause is the tree, not the lander

`tools/land selftest` on the quiet tree, with the fixed lander under test (the sandbox overlays the
working copy of `tools/landing`, so this measures the code as committed). **1,379 s wall, exit 1:**

```
STEPS BROKEN 10   CAUGHT 6   ABORTED BYTE-EXACT 10
SELF-TEST: 11 PASS / 5 FAIL
```

| | case | |
|---|---|---|
| **FAIL** | `control_clean_run` | a clean no-op landing in this sandbox must SUCCEED — **aborts at `sibling`** |
| **FAIL** | `fault_ui`, `fault_gates`, `fault_claims`, `fault_commit` | **each aborts at `sibling`**, before reaching the step its fault was injected into |
| PASS | `build_lock_refuses` | the landing refused to become a second writer |
| PASS | `fault_preflight` … `fault_sibling` (6) | each caught at its own step, **byte-exact** |
| PASS | `abort_restores_writers` | the depth case — **11 carriers written, then all restored** |
| PASS | `claims_negative_control` | 11 PASS / 0 FAIL — a false claim still reds |
| PASS | `packet_slot_validator` | 5 PASS / 0 FAIL |
| PASS | `live_tree_untouched` | **every live carrier byte-unmoved across the whole self-test** |

**READ THE TALLY LINE, NOT THE PASS COUNT: `ABORTED BYTE-EXACT 10` — TEN OF TEN.** Every abort in the
run, including all five failures, restored every carrier byte-exact. **No carrier moved anywhere, and
the live tree was asserted untouched.** The abort ladder — the whole reason the package exists — is
intact. The five failures are all one thing: `CAUGHT 6` of `10`, because four faults were never reached,
because the landing had already stopped at step 5. **What failed is the self-test's premise, not the
lander.**

**THE CONTROL LANDING ABORTS AT `sibling`, AND THE MESSAGE IS THE DIAGNOSIS:**

> *CONFORMANCE GATE FAILED — the forward view rebuilt under the config of record produced board
> `b3e8da99` but the manifest of record pins the board at `68be10c7`. The regenerated forward view is NOT
> the view the owner sees; refusing to stage it. This is a STOP (owner ruling v471 §4).*

**The chain, each link measured, none inferred:**

1. **The sibling sidecar is stale on the live tree, and has been since the prereg.** Tracked across the
   commits:

   | commit | live contract seal | sibling sidecar seal | |
   |---|---|---|---|
   | `efbe1b6` — register v807, *"self-test 10/10, no-op reproduced the live board"* | `cde9f70a49b6` | `cde9f70a49b6` | **AGREE** |
   | `fb3d3c0` — the prereg | `8e6dcdbc89d6` | `cde9f70a49b6` | **STALE** |
   | `531235c` — the flip, restamp riding it | `4cbc7f27c990` | `cde9f70a49b6` | **STALE** |
   | `f071a33` — HEAD | `4cbc7f27c990` | `cde9f70a49b6` | **STALE** |

   Restamping the contract moved the seal; reconciling the sibling to it would require a **build**, and
   in the P9 window there is no board to build that the pins would accept. Nothing did anything wrong.
2. **So `sibling.verify()` reports a fail even for a NO-OP landing** — `sidecar contract_sha256 != live
   contract seal` — which makes step 5 attempt a **reconcile**, which **builds**.
3. **The flip is committed, so the build produces `b3e8da99`** — the variant-A board, correctly.
4. **The no-op landing's pin is still `68be10c7`**, because a no-op moves no pin.
5. **`sibling_repin`'s conformance gate refuses the mismatch.** *It is doing precisely its job.*

**Consequently every self-test case that reaches step 5 aborts at `sibling` instead of where its fault
was injected** — the control run, and each fault case injected at `ui` / `gates` / `claims` / `commit`.
Cases that abort before step 5 all pass, byte-exact.

**WHY IT WAS GREEN AT `efbe1b6` AND IS RED NOW:** register v807 recorded the passing run's premise in its
own words — *"no-op reproduced the live board"*. After the flip, **a build no longer reproduces the live
board, by design**. The 10.5-second self-test of 2026-08-20 was a run in which the sibling never needed
to reconcile at all.

### 9.4 · THE DEADLOCK, STATED PLAINLY

**The ruling's half (ii) — *fail = no transaction opened* — cannot be satisfied on this tree until this
landing lands, and this landing cannot start until it is satisfied.**

It is not special to variant A. **P9 forces the engine edit into its own commit ahead of the landing**,
and the lander's `preflight` demands a clean tree — so *every* dial-flipping lever landing passes through
a window in which the source builds a board the pins do not yet name. **In that window the self-test's
control case cannot pass.** The gate as ruled would block the entire class of landings the lander exists
to perform, not merely this one.

**The ruling was given on a premise that was true when it was written and is not true now** — that the
self-test passes standalone. §6 of this account told the supervisor it *"already ran green standalone at
`efbe1b6`"*, which was accurate; what nobody checked was that `efbe1b6` **precedes the flip by nine and a
half hours**.

### 9.5 · WHY THIS SEAT DID NOT FLY ANYWAY

The failing case says nothing bad about the lander, the landing was already proven to pass step 5 on the
real spec in attempt 1, and the owner's word and waiver stand. It would have been easy to argue the gate
away. **This seat did not, and the reason is the reason the gate exists.**

To fly, this seat would have had to **bypass, on its first run and for its own act, the precondition it
had installed minutes earlier on the supervisor's instruction.** §6 refused a smaller version of exactly
this — *"narrowing a gate set to make one's own landing pass is exactly what this estate refuses"* — and
sent the question up instead. **The answer to a ruling made on a stale premise is to return it with the
measurement, not to route around it.** So the transaction was never opened and the tree was never
touched.

**`oneliner_r14_restore` therefore remains UNRESOLVED.** It passes standalone on this tree (50 `[PASS]`,
exit 0) and its in-transaction failure can only be observed *in the landed state*. With `0abf099` the
evidence will now be captured the moment it is: the runner writes per-check output into
`gate_acceptance_runner_evidence/` inside the act's evidence dir. **The instrument is ready; the
observation is owed.**

### 9.6 · WHAT THE SUPERVISOR IS ASKED TO RULE

Three ways out. **This seat implements none of them on its own initiative** — each changes what a proof
means.

1. **Make the sandbox self-consistent at creation.** The sandbox is synthetic and already has fixture
   specs written and committed into it; making *its own* sibling sidecar agree with *its own* contract
   seal at creation would remove the hidden dependency on live-tree coherence and restore the
   10.5-second no-op. Touches no live carrier. **The measurement says this is sufficient:** the control
   landing reports **`fails=1`**, and the one fail is `sidecar contract_sha256 != live contract seal` —
   clear it and `verify()` returns `ok`, the sibling step returns early having written nothing, no build
   happens, and the control run reaches `ui` / `gates` / `claims` / `commit` as it is meant to.
   **This seat's recommendation**, but it is a change to a proof harness and belongs to the pen.
2. **Move the standalone self-test earlier in the act, not just earlier in the transaction** — run it at
   prereg time, *before* the engine edit, where the P9 window has not yet opened. Keeps the ruling's
   intent (fresh proof, no recursion) and sits outside the contradiction.
3. **Rule that the pre-transaction gate reads the control case as advisory inside a declared P9 window.**
   Honest only if the window is declared in the act spec and the reason is printed at the top of the
   landing. Weakest of the three, and named here so it is not adopted by accident.

**Everything else remains ready and unchanged.** Prereg `fb3d3c0`, flip `531235c`, act spec validates
clean, board `68be10c7` / **692,296** / **804**, store `b745002e` unmoved, engine_head `8f591805`,
contract `4cbc7f27`, balanced `556ad70d`. **Nothing in this session moved a single identity.**

### 9.7 · FINDINGS ADDED

**F-7 · THE SELF-TEST HAS AN UNDECLARED PRECONDITION ON THE LIVE TREE.** *"A clean no-op landing must
succeed"* silently requires that a build from source reproduces the pinned board **and** that the sibling
sidecar already agrees with the contract seal. Neither is a property of the lander; both are properties
of the tree, and **P9 guarantees the first is false for exactly the acts the lander is for.** A proof
harness whose green depends on state it does not declare will go red for reasons nobody can read off it —
which is what happened here, and it took a commit-by-commit seal table to see it.

**F-8 · A RESTAMP MOVES THE SEAL AND SILENTLY STALES THE SIBLING SIDECAR.** `fb3d3c0` and `531235c` each
restamped the contract; neither could reconcile the sibling, because reconciling requires a build and the
board did not yet exist. The staleness is invisible until something runs `sibling.verify()` — and then it
forces a full rebuild inside any landing, no-op or not. **The 275-second `sibling` step of a landing that
moves nothing is this defect's price**, and it is paid on every practice landing the self-test runs.

---

## 10 · THE PEN'S ANSWER — **THE SELF-TEST RUNS ON A COHERENT TREE**

§9.4 returned the deadlock to the supervisor with the measurement. **The pen answered, and it did not
pick any of the three options §9.6 offered.** It picked a fourth and better one — and the difference
matters, because §9.6's own recommendation would have changed what the harness *proves*, while this
changes only *where it stands*.

> **"The lander self-test proves THE LANDER, not the act. It therefore runs on a COHERENT tree: the
> pre-transaction standalone run executes in a sandbox worktree checked out at the LAST COHERENT BASE —
> for a dial-flip act, the commit immediately before the flip (where pins == source); for any non-flip
> act, HEAD. Fresh proof each landing, no recursion, and the mid-act incoherence window (flip committed,
> board pending) can no longer deadlock its own landing. The in-transaction gate profile continues to
> exclude the self-test, and the self-test remains a registered runner check on every coherent tree."**

**Implemented minimally at `07783e4`:** `Sandbox` takes a `base` (default `HEAD`); `selftest.main` and
`tools/land selftest --base` pass it through; `cli._preflight_selftest` reads the act spec's new optional
`coherent_base` slot. This act declares `fb3d3c0` — `531235c^`, the prereg, the last commit at which a
build from source still reproduces the pinned board. **The slot names a commit and nothing else:** no
prediction, no identity, no gate and no carrier of this act reads it, and the spec diff is **+2 lines,
0 removed**, with `board_after` / `board_before` / `moves` untouched.

**AND THE LANDER UNDER TEST IS STILL THE LIVE ONE.** `Sandbox.create` overlays `tools/landing` and
`tools/land` from the **working copy** on top of whatever base is checked out. Moving the base changes
the *tree the lander is exercised against*, never the lander. That is the ruling's own distinction, and
it is the reason this is not a weakened proof.

### 10.1 · The measurement, both sides, same command and same lander

| | | |
|---|---|---|
| `tools/land selftest` *(HEAD, mid-act)* | **11 PASS / 5 FAIL** · CAUGHT **6/10** · 1,379 s · exit 1 | §9.3 |
| `tools/land selftest --base fb3d3c0` | **17 PASS / 0 FAIL** · CAUGHT **10/10** · 796 s · **exit 0** | **GREEN** |

**`ABORTED BYTE-EXACT` was 10 of 10 in BOTH runs, and `live_tree_untouched` passed in both.** Nothing
about the abort ladder was broken and nothing about it was repaired. What changed is that the control
case became answerable, so the four faults that had been unreachable — `ui`, `gates`, `claims`,
`commit` — are each now caught **at their own step**, byte-exact. `commit_explicit_paths` runs for the
first time since the flip (it is gated on the control run succeeding): **5 paths committed, all
declared**.

**The coherence is visible in the sandbox's own numbers:** at `fb3d3c0` its sibling reconcile rebuilt
balanced `556ad70d` → `556ad70d`, **unchanged** — a build from source reproducing the board the pins
already carry. That is precisely what `HEAD` could not do, and precisely what the ruling names.

### 10.2 · The gate profile, proved on the real tree

`acceptance.runner --profile in-transaction` on this tree, the profile `land lever`'s gates step now
uses: **16 checks, 16 PASS, 0 FAIL — GREEN, 279 s.** Exactly one check excluded (`lander_selftest`), and
**`oneliner_r14_restore` PASSES here** (50 `[PASS]`, exit 0) — as it has every time it has been run
outside a landing. Whether it survives *inside* one is the observation §9.5 said was owed, and `0abf099`
now captures the evidence either way.

**The transaction is opened next. §11 is what it did.**
