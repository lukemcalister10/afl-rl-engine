# THE MODERNISATION PROGRAMME — v2, restructured under adversarial review

**Status: PROPOSED — nothing commissioned until the owner rules.** Drafted by the supervisor, self-audited against the repo, adversarially reviewed (19 findings, verdict NEEDS RESTRUCTURING), restructured. The draft and the full review ride in the register record (v783). Every load-bearing review claim was independently re-verified by the supervisor before this restructure.

**The goal, honestly restated:** the owner asked for "an hour to discuss, 15 minutes to implement and push live." What this programme delivers is: **a ~3-minute iteration loop while deciding, and a measured, single-transaction landing when done** — with the landing's true cost measured before any target is promised. The review proved the original 15-minute framing omitted the landing's tail (the re-seal, the pin re-key, the release contract) and the true instrument-estate size; this version does not repeat that.

---

## M0 — THE DATA/LEVER SEPARATION RULE (one ruling, no code; FIRST)
Five of the eighteen boot pins are data, not levers (store, register, band, balanced board, as_of_round), and a weekly in-season ingestion pipeline moves the board on its own schedule. **The rule: no lever change lands in the same commit or round-window as a round advance; `pipeline diff`'s baseline must be a board at the SAME as_of_round as the candidate, and the pipeline halts if they differ.** Without this, the mover table the owner rules on attributes to the lever what the round did.

## M1-pre — AUDIT THE EXISTING CI ESTATE (read-only, one seat)
Five workflows already exist in .github/workflows/ — including a push-triggered halt-not-warn guard battery and an independent-host negative-control suite (RED 1–5) that is precisely the "deliberate-defect drill" the draft thought it was inventing; one workflow is already de-scoped permanent-red (the noise-hides-real-reds failure realised). **First act: audit all five** — which are green, red, rotted, or contradicted by campaign instruments — then EXTEND them, never build a parallel estate beside an unaudited one.

## M1a — THE VERDICT CONTRACT + THE CANONICAL RUNNER (one order, NO migrations)
The review's deepest finding: the existing "suite" is an evidence *generator*, not a *gate* — no `set -e`, exit codes printed never acted on, terminal `echo "ALL DONE"` (exit 0 always), every verdict reached by a human reading tails. **M1a builds the spine only:** every instrument returns a machine-readable PASS/FAIL record; the runner aggregates and exits non-zero; the runner's self-test forces a failure in each stage and asserts a non-zero aggregate; everything runs **from a fresh clone with nothing but the repo and the pinned venv** (no /tmp literals, no cross-order absolute paths — the current frozen copies are readable but not runnable, which M3 later depends on fixing). Includes a **build lock** (flock; ten lines) — the strict-sequential rule becomes a mechanism, not a convention that has already failed once.

## M1b…n — INSTRUMENT MIGRATION, one family per tranche
The estate is 52 evidence dirs, 533 script paths, 17 emitter forks — an order of magnitude beyond "one order." Each tranche migrates ONE family (boards/identities · day-0 · burn+birthday · class · no-arb · documents), gated by: the canonical version reproduces the frozen copy's printed figures on the landed board. Specific rulings folded in from the review:
- **The byte-carried 31-F emitter is kept as a permanent frozen CONTROL ARM**; the canonical config-reading emitter runs beside it and retires it only after N boards of cell-for-cell agreement, recorded not intended.
- **os_continuity is FIXED, not retired** — the birthday probe covers one axis of its many; retiring broad for narrow is a coverage cut dressed as a repair. If it ever dies, its obituary enumerates which axis moved to which instrument.
- **Day-0 re-basing becomes an explicit, owner-visible, off-by-default input** with a mandatory printed diff of every moved row — the judgement currently lives in a shell-script comment, and a suite inheriting the capability without the judgement re-bases itself green on the first halt.
- **A must-move instrument enters the suite** (see M3's paired gate — the positive control that once caught a silently deleted dial producing a byte-identical board).
- **The kill-switch inventory problem**: a declared `kill_switches` block in model_config.json — named, excluded from the value hash, admitted by the reject scan on explicit identity-chain runs — resolving the measured mutual exclusion between the config gate and the identity chain (today, setting any kill-switch under gate mode halts the build; the campaign's identity proofs necessarily ran ungated).

## M2 — THE ONE-COMMAND PIPELINE (after M1a; target MEASURED, then set)
`pipeline build`: config → board → matrix → documents → acceptance verdict, provenance-triple stamped, behind the lock. `pipeline diff <baseline>`: mover table + per-lever + no-arb delta, refusing cross-round baselines (M0). **Scope corrected by the review: the pipeline's landing mode includes the WHOLE shipped set — the re-seal, the pin re-key, the release contract — or its estimate must say "plus the landing transaction."** First act: time one full acceptance run end-to-end and QUOTE THAT NUMBER as the target; measured floor so far: ~80s/board, ~3.5min/emit, ~13 minutes of builds before any acceptance stage — an honest 45 beats a promised 30.

## M5 — THE CHANGE PROTOCOL (a ruling; after M2's drill)
Two lanes. **Lane A (existing lever, new value):** the hour of discussion → a pen that carries (a) **at least one numeric prediction with an explicit falsifier** and (b) **the named standing rails the change must leave alone**, printed before/after by the diff → pipeline → owner's word → the landing transaction. The review proved a direction-only pen is not thin F6, it is the removal of F6's only working mechanism: the campaign's audit found three HIGH defects — including two fired falsifiers written up as held — while every standing instrument was green; and ORDER P's modern rail sits 0.012 from the class floor, a gap only a pen that names it is watching. **Rollback is a Lane-A change in the opposite direction** — the pen records the pre-change board id; reversion is a run against it, never a rebuild from history. **Lane B (new mechanism):** full discipline unchanged, on M1/M2 rails. **The independent read stays**: any mechanism change, and every Nth Lane-A change, gets an independent reader who did not build it — the only watcher class with a demonstrated hit rate (the drill guards yesterday's threat model by construction). Owner-only gates unchanged.

## M3 — THE CONFIG COLLAPSE (after soak; each tranche PRICED AS A BAKE)
Honest re-statement per the review: deleting a dial branch always moves engine_head — a re-pin, i.e. a bake-class transaction under the house's own config law, not "a routine order" (unless the owner explicitly delegates engine_head re-pinning inside proven-no-op tranches). **The paired gate, non-negotiable:** (a) the default board byte-exact AND (b) the retired branch still reproduces its historical identity byte-exact before retirement — because the must-not-move gate alone is provably blind to deletion (the record's own case: a silently deleted dial, byte-identical board, caught only by must-move). **History becomes ARTIFACT tags, not source tags** — the board, book, matrix and acceptance table committed as bytes at each retirement; bytes survive M4's refactor, a rebuild recipe may not (M3 and M4 are otherwise on a collision course). Scale honestly: ~100 pre-existing dials plus the 18 baked.

## M4 — THE STRUCTURAL REFACTOR (behind everything; negative controls FIRST)
Re-scoped per the review: the campaign already bypasses /home/claude/rl_workspace — the real target is **"one build root"** (today: per-build /tmp copies + per-seat worktrees + the workspace remnants in run_panel/bootstrap). The exec-split sentinel is a **126-file idiom (37 in engine/rl_after alone)**, a migration not a line-fix. **Every tranche's gate: board byte-exact AND the negative-control battery still fails closed** — extended to the two remaining hand-mirrored loader pairs (q97m, cm_trees) BEFORE their mirrors are touched, because a forgotten mirror leaves the board identical while a guard silently loses coverage (a failure class the register already names).

---

## Sequencing
**M0 → M1-pre → M1a → { M1b…n ‖ M2 } → M5 → M3 (post-soak) → M4 tranches.**

## What this still does not promise
New mechanisms are never 15-minute changes (Lane B is where a dozen real defects died this campaign). The owner stays the gate. "Live" includes the landing transaction, priced honestly once measured.
