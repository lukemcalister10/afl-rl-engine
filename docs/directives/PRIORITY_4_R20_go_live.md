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
2. **The `INGEST_SCORE_APPLY` token** — the env half of the gate. Owner-worded at go-live.

Ask once, clearly, and wait. Do not synthesise a feed and do not proceed on a partial one.

## 0b · ENVIRONMENT CHECK — FIRST ACT

    bash bootstrap_env.sh && bash bootstrap.sh

Deterministic per container, not intermittent. Must pass before anything else. Never bypass it — an
unpinned numpy silently reorders the board.

---

## 1 · CORRECTION TO THE RUNBOOK — READ THIS BEFORE FOLLOWING IT

`docs/GO_LIVE_round_score_ingestion.md` is the procedure of record, **and its step 4 is stale.** It
says to set the code half by editing `APPLY_DEFAULT = True` in the go-live commit. The code has since
grown a local override that makes that unnecessary:

    code half : APPLY_DEFAULT (stays False)  OR  INGEST_SCORE_APPLY_ARMED=1
    env  half : INGEST_SCORE_APPLY=<owner token>

`score_ingestor.py:47–66`. The comment states the intent directly — the local half "lets the owner arm
without editing Python, while the SHIPPED constant stays False."

**Use the environment path. Do not edit `APPLY_DEFAULT`.** It is strictly safer: no commit ever arms
the gate, so a stray checkout of `main` can never write to the store. Both halves are still required;
this is not a relaxation.

Do not edit the runbook in place. Note the correction in your return and the seam will file it.

---

## 2 · THE SEQUENCE

Flip-order steps 1–2 are already discharged: `round_apply.py` and `dry_run_proof.py` are both on
`main`, and `APPLY_DEFAULT` ships `False`. You begin at the proof.

1. **Dry-run proof.** `python3 engine/rl_after/ingestion/dry_run_proof.py` — expect PROOF PASS,
   exceptions 0, anomalies 0, byte-for-byte reproduction. **A red here blocks go-live.** Stop and
   return.
2. **Preview the real R20 feed, gate still OFF.** `preview(rows)`, then read `preview.exceptions` and
   `preview.anomalies`. Exceptions must be empty or every name owner-explained; every anomaly must be
   owner-cleared. **Do not proceed with a non-empty exceptions list** — route it to the owner by name
   and wait.
3. **Arm both halves** — env only, per §1 — in the run environment, never in a commit.
4. **Apply ONE round.** `round_apply.py` runs eight steps all-or-nothing: gate → clean → season →
   dedup → merge → regen → re-stamp → ledger. It merges scores in place on the single source
   (atomic temp+rename), regenerates the board via `rl_export.py`, and moves the `store` and `board`
   pins in `data/expected_boot.json` to the new md5s.
5. **Assert the landing.** The boot-store guard re-pins to the new store md5; the derived board
   regenerated; the SSI correction-sticks canary green. Record old and new md5s for both store and
   board.
6. **Stop.** Do not wire the recurring weekly loop. That is a separate owner decision.

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

## 6 · RETURN

To the seam, with: the environment check; the dry-run proof result; the preview's exceptions and
anomalies and how each was cleared; store md5 before and after; board md5 before and after; the
derived panel with its working; the terminal CI map; the runbook correction from §1; and anything you
could not do, stated plainly.

*Filed by the seam authority + supervisor pen, 2026-07-28, on the owner's word. Docs-only.*
