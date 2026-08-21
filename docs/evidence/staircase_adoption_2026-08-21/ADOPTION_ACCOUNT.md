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
> That precondition then **blocked the landing** (§9): standalone on HEAD the self-test went 11 PASS /
> 5 FAIL, because P9 leaves the tree incoherent between the flip and the landing. **This seat did not
> bypass the gate it had just installed** — it measured it and sent it up. **The pen ruled** (§10): the
> self-test proves the lander, not the act, so it runs on a **coherent tree** — sandbox cut at the last
> coherent base. Implemented at `07783e4`; the self-test then went **17 PASS / 0 FAIL, CAUGHT 10/10**.
>
> **THE LANDING THEN FLEW (§11), AND ABORTED AT `gates` — ON ONE CHECK, WITH THE EVIDENCE CAPTURED.**
> Steps 0–6 all **OK**; every proof the act owns **met again** (`b3e8da99` byte-exact against the prereg,
> kill-switch → `68be10c7`, 10 must-not-move identities unmoved, sibling → `7c32a540`). `lander_selftest`
> is gone from the gate set: **`gates` fell 1,720.8 s → 287.9 s**, the transaction **2,223 s → 796 s**,
> and the gate run read **15 PASS / 1 FAIL**.
>
> **THE ONE FAILURE IS `oneliner_r14_restore`, AND IT IS A REAL COUPLING — NOT CONTENTION.** With F-5's
> evidence capture the assertion is now *read*: step 3 appends to `data/release_lineage.json`
> (**12 → 13** entries) while `ui/data/movers_transition.js` — the mirror the gate asserts equal — is
> **never written by a lever landing at all**, its writer of record being the **unbuilt 2b round
> lander**. **Every lever landing that registers an out-of-round column reds its own gates step by
> construction.** That is **F-9**, and it is this act's finding, not this act's fault.
>
> **HALTED AND REPORTED, per the brief.** The fix is one line of sequencing and **this seat did not
> write it**: it would add a writer to the transaction and move a carrier's writer of record, on this
> seat's initiative, to make its own act pass. **Abort byte-exact again — 37 carriers restored, all 16
> tracked carriers independently re-hashed against `HEAD`, zero differences.**

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

---

## 11 · THE LANDING FLEW — AND `oneliner_r14_restore` IS A REAL COUPLING, WITH THE EVIDENCE

The transaction opened at **02:48:17Z** and ran to **1,632 s** wall (796 s of transaction, the rest the
pre-transaction self-test). **It aborted at `gates` again — but nothing else about it is the same as
attempt 1, and the one thing that red it is now READ rather than guessed at.**

### 11.1 · Both machinery fixes did exactly what they were built to do

* **The pre-transaction self-test ran and PASSED — `17 PASS / 0 FAIL`, `CAUGHT 10/10`, `ABORTED
  BYTE-EXACT 10/10`** — cut from `fb3d3c0` off the act spec's `coherent_base` slot, automatically. Then
  and only then: *"PRE-TRANSACTION SELF-TEST PASSED. Opening the transaction."*
* **`lander_selftest` is GONE from the gate set**, as ruled. **`gates` fell from 1,720.8 s to 287.9 s**
  and the whole transaction from **2,223 s to 796 s** — and the gate run reported **16 checks**, the
  in-transaction profile, with its own header naming the profile that produced it.
* **F-5 DELIVERED THE ONE THING IT WAS BUILT FOR.** The runner wrote per-check output into
  `gate_acceptance_runner_evidence/`, the `StepError` named the path, and the failing assertion is on
  disk in full. **Attempt 1 could only report a truncated 110-character reason and two candidate
  causes. This attempt has the traceback.**
* **The lander cleaned up after itself:** *"work dir discarded (the abort proved every carrier
  byte-exact)"*, and the pre-transaction transcripts were filed into the evidence dir when the
  transaction closed. **Zero orphans in `/tmp` afterwards.**

### 11.2 · Every step and every proof the act owns — MET AGAIN

| # | step | seconds | verdict |
|---|---|---|---|
| 0 | preflight | 0.08 | **OK** — 111 carriers captured |
| 1 | build_proofs | 225.03 | **OK** |
| 2 | pins | 0.02 | **OK** |
| 3 | lineage | 0.15 | **OK** |
| 4 | contract | 0.08 | **OK** |
| 5 | sibling | 282.84 | **OK** |
| 6 | ui | 0.19 | **OK** |
| 7 | **gates** | **287.91** | **FAIL → ABORT** |
| 8 | claims | — | not reached |
| 9 | commit | — | not reached |
| | **TOTAL** | **796.30** | |

**`PREDICTED BOARD MET: b3e8da99bc7f632e5d1eebc732f9cf01 == prereg`.** Kill-switch `RL_O44_LVLMONO=0`
→ **`68be10c7`**, 82.7 s; switch-off ≠ switch-on. `pins`: `board` moved, **10 must-not-move checked, 0
moved**. `lineage`: column `the-staircase-adoption-21-8` registered, **12 prior entries byte-verbatim**,
baseline unmoved. `contract`: `4cbc7f27` → `213443de`, **10 frozen fields unmoved**. `sibling`: 8 fails
→ **0**, balanced `556ad70d` → **`7c32a540578b799922daea41d8acdfa2`**. `ui`: both writers,
`stamp.balanced_board_md5 = 7c32a540…` read back **OK**.

### 11.3 · The gate result: 15 PASS / 1 FAIL, and the one is not environmental

```
AGGREGATE  16 checks  |  PASS 15  FAIL 1  BLOCKED 0  RULED-RED 0
VERDICT    RED — 1 gating failure(s): oneliner_r14_restore
```

`build_twice_determinism` **PASS** (two bare builds byte-identical, on the landed board).
`release_manifest`, `boot_guard_checkout`, `config_manifest`, `ruling_config`, `release_contract_seal`,
`store_coherence_six_way`, `doc_lint`, `rulebook_lint`, `ruled_red_ledger`, `inbox_manifest`,
`mirror_parity`, `dial_coverage`, `oneliner_gamma`, `oneliner_f1_lens` — **all PASS on the landed
state.**

### 11.4 · **THE VERDICT ON r14: A REAL COUPLING. NOT CONTENTION.**

`gate_acceptance_runner_evidence/oneliner_r14_restore.txt`, the actual failure:

```
File "engine/rl_after/ingestion/test_movers_transition.py", line 107, in run_all
  _ck(trans_js.get(REGISTER_KEY) == lineage.get(REGISTER_KEY),
AssertionError: FAIL: release_lineage.json release_transition_register == the mirror's register
                      (era succession: ALL entries reach the reader)
```

Everything before it passed — the eight weekly-updater tests, all seven R14 fail-closed controls, and
the assertion immediately above (`release_transition == ui/data/movers_transition.js`, the transition
mirrored exactly). **Only the REGISTER diverged.** The mechanism, each link measured from this run's
own record:

1. `trans_js` is **`ui/data/movers_transition.js`** — the mirror; `lineage` is
   **`data/release_lineage.json`** — the record. Line 107 asserts their
   `release_transition_register` are **equal**.
2. **Step 3 appended to the record.** The abort's own moved-carrier list:
   `data/release_lineage.json  f486ecd40dc8 -> 611bf4454202` — **12 entries → 13**.
3. **The landing never wrote the mirror.** `ui/data/movers_transition.js` appears **nowhere** in the
   moved-carrier list — not written, so not restored, because there was nothing to restore.
4. So in the landed state the record held **13** entries and the mirror held **12**. The check did its
   job.
5. **It is structural, not incidental.** `carriers.py` names the mirror's writer of record as
   `round_movers` — **the 2b round lander, which is NOT BUILT** — and the lever landing's `ui` step
   runs **two** writers (`extract_board_view`, `inject_release_contract`), neither of which projects
   the lineage. **The projector exists**: `ui/tools/generate_movers_transition.py`, whose own docstring
   says it is a *"MECHANICAL SERIALIZATION"* of `release_lineage.json` carrying *"ZERO authorship"*,
   written because *"the js header has always said 'do not hand-edit; regenerate from
   release_lineage.json' while no generator existed in the tree to do it"*.

**CONTENTION IS RULED OUT.** The tree was quiet and exclusively this seat's; the failure is a
deterministic equality between two files, one of which this landing writes and the other of which it
structurally cannot. **It reproduced on the first attempt under a quiet tree**, which is exactly what
§4.2 left open and §9.5 said was owed.

**THIS IS THE LEVER-LANDING-VS-2b GAP, CONFIRMED.** Any lever landing that registers an out-of-round
column — that is, **every lever landing that moves the board out of round** — appends a register entry
the mirror never receives, and reds `oneliner_r14_restore` at its own gates step. **This act did not
cause it and is not special to it.** It is the first act to reach the landed state with the evidence
switched on.

### 11.5 · HALTED, AND WHY THIS SEAT DID NOT FIX IT

**The abort is again the lander's best moment.** `byte_exact: true`, **37 carriers restored**, and this
seat verified it independently rather than trusting the flag: **all 16 tracked carriers re-hashed and
byte-identical to `HEAD`** — board `68be10c7` / **692,296** / **804** · store `b745002e` · engine_head
`8f591805` · contract `4cbc7f27` · balanced `556ad70d` · lineage back to **12** entries.

The fix is one line of sequencing — run the projector in the `ui` step whenever `lineage` appended —
and **this seat will not write it.** It adds a writer to the landing transaction and moves a carrier's
declared writer of record, on this seat's own initiative, to make its own act pass. That is the third
time in this account the same temptation has come round, and the answer has not changed. **The brief's
own instruction is explicit: a real coupling the landed state exposes is a HALT-and-report.**

### 11.6 · WHAT THE PEN IS ASKED TO RULE — **F-9**

**F-9 · A LEVER LANDING MOVES THE LINEAGE RECORD AND CANNOT MOVE ITS MIRROR.** `data/release_lineage.json`
is written by `steps.lineage`; `ui/data/movers_transition.js` is declared to be written by 2b, which is
not built. The two are asserted **equal** by a standing gate. Therefore the lever lander, as shipped,
**cannot complete any landing that registers an out-of-round column** — the transaction is
self-inconsistent at step 7 by construction, and it took the landed state plus F-5's evidence capture
to see it. Options, none taken here:

1. **Add the projector as the lever landing's third UI writer** (`ui/tools/generate_movers_transition.py`),
   and move `ui/data/movers_transition.js`'s writer of record in `carriers.py` from *"round_movers (2b)"*
   to name the lever landing too. **Smallest change, uses the existing writer of record, and the
   projector is by its own charter authorless** — this seat's reading, offered and not acted on.
2. **Declare the mirror out of scope for a lever landing** and scope the r14 gate accordingly — which
   would mean shipping a board whose reader cannot see the transition that produced it, and is named
   here only so it is not adopted by accident.
3. **Hold the act for 2b.** Correct and expensive: 2b waits on 3a, and the owner's word is already given.

**Everything else is ready and unchanged.** Prereg `fb3d3c0`, flip `531235c`, spec validates clean,
self-test green on a coherent tree, the in-transaction profile green, and **every proof the act owns
met twice, on two separate flights.**
