# PRIORITY 4 · ROUND 20 — GO LIVE ON WEEKLY SCORE INGESTION

**Seat:** one fresh execution supervisor (build seat), directing hands. One writer.
**Authority:** owner word, 2026-07-28. His priority 4.
**Nature:** THIS JOB WRITES TO THE STORE. It is the only job in flight that does.

---

## WHY NOW

The tooling has been built and merged for weeks; the switch has been off by the owner's own decision
since 2026-07-12. Its one remaining dependency was the D2 forward-lens merge, which landed on
2026-07-27 at `265bdab`. The board sits at round 19 and the season does not wait — this is the only
item on the owner's list that is time-sensitive.

---

## 0 · WHAT THE OWNER MUST SUPPLY

You cannot start without both:

1. **The round-20 score file.** Participation is defined by **file membership** — a listed row means
   the player played (owner ruling, `footywire_parser.py:16`). Format is one round file parsed by
   `parse_round_file(path)`: rows of `(name, score)`.
2. **His word to arm the gate.** Nothing else — see §1.1. `INGEST_SCORE_APPLY` is not a credential and
   is not issued by anything; any non-empty string arms the env half. Do not ask him for a token.

So in practice there is **one** thing to ask for: the round-20 score file. Ask once, clearly, and
wait. Do not synthesise a feed and do not proceed on a partial one.

## 0b · ENVIRONMENT CHECK — FIRST ACT

    bash bootstrap_env.sh && bash bootstrap.sh

Deterministic per container, not intermittent. Must pass before anything else. Never bypass it — an
unpinned numpy silently reorders the board.

---

## 1 · TWO CORRECTIONS TO THE RUNBOOK — READ BEFORE FOLLOWING IT

`docs/GO_LIVE_round_score_ingestion.md` is the procedure of record and **it is stale in two places.**
Both were found by the owner's questions on 2026-07-28, not by the runbook.

### 1.1 · The gate arms by environment. There is no token to obtain.

The runbook's step 4 says to set the code half by editing `APPLY_DEFAULT = True` in the go-live commit.
The code has since grown a local override that makes that unnecessary (`score_ingestor.py:47–66`):

    code half : APPLY_DEFAULT (stays False)  OR  INGEST_SCORE_APPLY_ARMED=1
    env  half : INGEST_SCORE_APPLY=<any non-empty value>

**`INGEST_SCORE_APPLY` is not a credential and is not issued by anything.** The check is
`bool(os.environ.get('INGEST_SCORE_APPLY'))` — any non-empty string arms the env half. The runbook's
phrase "owner token" means a value the owner chooses, not a secret that exists somewhere. It is a
second deliberate opt-in, nothing more.

**Use the environment path. Do not edit `APPLY_DEFAULT`.** Strictly safer: no commit ever arms the
gate, so a stray checkout of `main` can never write to the store. Both halves are still required.

### 1.2 · `round_apply.RoundApplier` is SUPERSEDED. Do not use it.

`staged_apply.py`'s own header states it: *"This is the hardened successor to
round_apply.RoundApplier (PR #125). PR #125's applier mutated the LIVE files in sequence (store, then
board, then manifest, then ledger) with NO staging and NO rollback: a failure after the store write
left a NEW store with an OLD board / manifest / ledger — a silently broken build."*

The go-live runbook and `round_apply.py`'s own docstring both predate that replacement and describe
the superseded flow. **The live-scoring proofs drive `staged_apply`, not `round_apply`
(`two_round_proof.py:43`).** So does `round_catchup`.

Do not edit either document in place. Note both corrections in your return and the seam will file
them.

---

## 2 · THE SEQUENCE — TWO PHASES, AND THE SECOND ONE IS NOT OPTIONAL

Flip-order steps 1–2 are discharged: the write path and `dry_run_proof.py` are on `main` and
`APPLY_DEFAULT` ships `False`. You begin at the proof.

1. **Dry-run proof.** `python3 engine/rl_after/ingestion/dry_run_proof.py` — expect PROOF PASS,
   exceptions 0, anomalies 0, byte-for-byte reproduction. **A red here blocks go-live.** Stop and
   return.
2. **Preview the real R20 feed, gate still OFF.** `preview(rows)`, then read `preview.exceptions` and
   `preview.anomalies`. Exceptions must be empty or every name owner-explained; every anomaly must be
   owner-cleared. **Do not proceed with a non-empty exceptions list** — route it to the owner by name
   and wait. Identity resolves by stable key, never by display name or row order; any unresolved,
   ambiguous or duplicate assignment HALTS before the first write.
3. **Arm both halves** — environment only, per §1.1 — in the run environment, never in a commit.
4. **PHASE ONE — the canonical commit.** `staged_apply`: STAGE into a throwaway repo-shaped
   workspace → VALIDATE the staged outputs end-to-end (store parses, only permitted rows changed,
   board regenerates, board source-stamp == staged store, boot pins == staged store+board, Guard 5
   green against the staged set, ledger == the snapshot triples, board player-universe unchanged) →
   only then ATOMIC SWAP inside a transaction directory with rollback and crash recovery. This commits
   store, board, sidecar, boot manifest, ledger and the three histories together. **This commit is the
   source of truth.**
5. **PHASE TWO — finalization. This is where the Movers tab comes from.** `round_finalize`:
   a separate, journaled, idempotent phase that derives everything downstream from the committed
   state — the Matchday UI board bundles, the release contract, **the per-round movers report (JSON +
   CSV), the accumulated UI movers bundle `ui/data/movers.js`**, and the round-delta injection.

   **Stopping after phase one leaves an R20 board with an R14–R19 Movers tab.** That is the failure
   mode this step exists to prevent, and it is the single most likely way this job goes wrong.

   Finalization is fail-closed by design and you must not force it: `MV.movers_conflict()` runs before
   any same-round artifact is written and refuses rather than mutating on conflict; derivatives are
   generated while the round is FINALIZING, full validation runs first, and FINALIZED is written last.
   A crash at any point restarts as unfinalized and repairs. **If it refuses, return it — do not
   hand-edit `movers.js`.** The file's own header says so: *"Do not hand-edit."*
6. **Assert the landing.** Boot-store guard re-pinned to the new store md5; board regenerated; SSI
   correction-sticks canary green; **round 20 present in `ui/data/movers.js` alongside R14–R19, with
   the existing rounds byte-preserved**; the movers provenance transition
   (`ui/data/movers_transition.js`) still fail-closed and intact. Record old and new md5s for store,
   board and the movers bundle.
7. **Stop.** Do not wire the recurring weekly loop. That is a separate owner decision.

---

## 3 · THE PANEL WILL MOVE, AND THAT IS EXPECTED

Regenerating the board moves the ten-row panel in `expected_boot.json`, `run_panel.sh:43` and the
panel narrative. Those are the four surfaces that must be re-pinned together — never
`PANEL_EXPECTED.txt`, which has zero executable readers.

**Derive the new panel values; never type them.** Read them from the regenerated board and show your
working. The panel narrative must state that this is the R20 apply, name the superseded R19 values,
and preserve them as history rather than overwriting the record.

---

## 4 · YOU ARE RUNNING ALONGSIDE A MEASUREMENT JOB — AND YOU ARE THE ONE THAT MOVES

The priority-1 stage-1 seat is measuring the fitted artifacts against store `c120cfd5`, from a pinned
checkout at `85e39ee`. **It is pinned precisely so that you can move the store underneath it.**

- You are the **only** writer to the store. It writes nothing.
- Do not coordinate with it, wait for it, or hold your apply for it. Its figures stay valid for the
  store they name.
- One consequence to record rather than resolve: when stage 2 comes to adopt any re-derived artifact,
  it adopts against whatever the store is *then*, so those deltas get re-measured at adoption. That is
  expected and is not a defect in either job.

The CI parallelisation job (#205) is also in flight and touches only
`.github/workflows/live-scoring.yml`. If it lands before your first push, your test cycle drops from
~86 minutes to ~21. Do not wait for it.

---

## 5 · FENCES

- **One round.** Round 20 only. Not a catch-up, not a backfill.
- Never fuzzy-attach a name and never silently merge a suspicious row — the gate refuses an unclean
  preview and that refusal is correct.
- This job merges scores and regenerates derived artifacts. **It never touches valuation logic, the
  curve, the model, or pricing.** New scores flow through the unchanged engine at regen time.
- No tag, no release, no score-arm beyond the apply itself, no model change.
- Arm by environment only. `APPLY_DEFAULT` stays `False` in the tree.
- No prediction of the resulting CI map. Read the terminal map after it is terminal, step-level.

## 5b · RECORD WHICH GUARDS ACTUALLY FIRED — this feeds the owner's priority 5

His priority 5 is running the engine locally without the bake ceremony. That decision should rest on
evidence from a real round, not on argument. **Costs you nothing: the job runs anyway.**

For every gate this round passes through, record one line: **did it fire, or did it just re-arm?**

- **Fired** = it refused, halted, or caught something that was actually wrong.
- **Re-armed** = it moved because the round moved, and you updated it so it would pass.

Cover at least: Guard 5 / the boot pins · the staged-transaction validate list · the dedup ledger ·
identity resolution · `movers_conflict` · the ten-row panel · the release contract · each CI suite.

A gate that has never fired in anger across R15–R19 and does not fire at R20 is an evidence-based
candidate for dropping from the weekly loop. **Do not drop anything.** Record it and hand it back.

## 6 · RETURN

To the seam, with: the environment check; the dry-run proof result; the preview's exceptions and
anomalies and how each was cleared; store md5 before and after; board md5 before and after; the
derived panel with its working; the terminal CI map; the runbook correction from §1; and anything you
could not do, stated plainly.

*Filed by the seam authority + supervisor pen, 2026-07-28, on the owner's word. Docs-only.*
