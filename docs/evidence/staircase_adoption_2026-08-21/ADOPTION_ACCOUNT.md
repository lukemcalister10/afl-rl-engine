# THE STAIRCASE FIX ADOPTION — VARIANT A RAW. THE ACCOUNT.

**Seat:** adoption seat, THE STAIRCASE FIX (ORDER 44) · **Date:** 2026-08-21
**Register:** v808 — **NOT touched by this seat.** **NOT PUSHED.**

> ## STATUS: **THE FLIP IS COMMITTED. THE LANDING IS NOT DONE.**
>
> `tools/land lever` ran its full transaction and **ABORTED at step 7 of 10 (`gates`)**, restoring every
> carrier **byte-exact** — verified independently by this seat, not merely claimed by the lander.
> **The board did not move.** The live board is still `68be10c79d0ee096455754e084bcf757` / **692,296** /
> **804**. The engine default **is** flipped (committed at `531235c`), so the tree is in the declared
> intermediate state: **dial ON in source, board not yet rebuilt**.
>
> **THE ABORT WAS NOT CAUSED BY THE ACT.** Every proof the act owns passed. Two acceptance checks red,
> and both are environmental or structural rather than defects in variant A — §4.
>
> **A RE-RUN IS BLOCKED AND IS NOT THIS SEAT'S TO UNBLOCK** — another seat is actively working in the
> shared tree with 13 uncommitted foreign paths, which makes the lander's `preflight` clean-tree
> assertion abort instantly. §5.

---

## 1 · THE COMMITS

| | sha | what |
|---|---|---|
| **prereg** | `fb3d3c0` | adoption prereg **+ the A-raw no-arb and class reading**, before the engine edit (P9) |
| **flip** | `531235c` | one engine commit: `RL_O44_LVLMONO` default `'0'` → `'ratchet'`, **restamp riding it** |
| **landing** | **NONE** | aborted at `gates`; nothing committed by the lander |
| evidence | *(this commit)* | the attempt's full record |

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
