# REBAKE WEEK · ARM 1 — THE STORE-ALONE ARM · directive 2026-08-24

**Charter:** register v831 (all six rebake decisions ruled, owner words verbatim) and v833 (the
binding handover). Comparison paper `docs/proposals/REBAKE_COMPARISON_2026-08-21.md` §1.11: *"Land
the rebake in attributable arms, store-alone refit first — the one arm with no design content,
whose mover table honestly measures how stale the estate became."*

**This arm has NO design content.** It refits the scoped fitted artifacts with the INCUMBENT
constructions on the CURRENT store (pinned `daa93053`) and measures the movement. Its movers list
goes to the owner BEFORE any design change is built. **Nothing in this arm touches the live
board:** the live pins, `data/expected_boot.json`, and the release contract are UNTOUCHED; the
board moves ONCE, at week's end, on the owner's word, through `tools/land lever`.

## Scope (v831 D6, owner: "Happy to rebake the ones you suggest")

- `cm_400` — the five-quantile band forests (currently seeded to `/home/claude/cm_400.pkl` by
  `bootstrap.sh`, outside the repo — this arm brings the candidate in-repo).
- `q97m` — the frozen ceiling (`data/q97m.pkl`; entry point `refit_q97m.py`, never yet exercised).
- `peak_model_v4` (+ `pvc_snapshot`, which CO-EMITS with the peak-model build by design — verified
  at `rl_model.py:1234` as the frozen train-time PVC feature; it regenerates with its model, never
  separately).
- `bust_prior_table`.
- `v0surf` UNTOUCHED (current).

**Incumbent construction means:** same estimator class, same hyperparameters, same training-row
rule as each shipped artifact — read them from the build scripts and the forensics in
`docs/proposals/rebake_study_A/` and `rebake_study_B/`; verify against source, do not guess.
The read-site ratchet is part of the incumbent construction and stays ON in this arm.
Exhaustive list of what differs from the shipped artifacts, to be confirmed in the prereg:
(1) the training store is current (`daa93053`) rather than the 2026-07-15→17 epoch;
(2) T1 (the owner's fabricated-zeros rule) IS applied — the shipped artifacts predate his word
(v831: every arm carries T1). Name T1's row impact separately in the report so the store-vs-T1
attribution is visible.

## Non-negotiables riding this arm (v831: "every arm carries")

1. **In-repo provenance stamps** beside every candidate pickle — training store md5, row count,
   hyperparameters, old→new artifact hashes — written by the committed refit entry point. This
   includes fixing `build_peak_model_v4.py`'s two output paths so its stamp lands in-repo (the
   embarrassing detail both studies found: the right stamp written where nothing can read it).
2. **The cm loader HALT** — delete the silent-refit-on-cache-miss fallback (the one-line fix both
   studies name). Prove behaviour-unchanged on the live path first: show the fallback cannot fire
   with the cache present, and the live board is byte-identical across the change (P1).
3. **Full-population level census (V3)** on the candidate at the read site, expected ZERO
   descending steps across all board rows over the model's level range.
4. **B2 / B6 / G-Y0** on the candidate board.
5. **Pinball monitor reading** against the study A §5.1 baseline tables.
6. **Law-9 mint measured and REPORTED** — waived as a gate (v830, owner: "Waiving the minted
   value, not bothered about conservation for this"), still a number on the record.
7. **P12 per-arm no-arb reading** on the candidate — a reading taken on a sibling variant does
   not cover this arm.
8. **Fit-twice reproducibility measured** on this box and recorded honestly whichever way it
   goes — the freeze buys travel, not reproducibility (scope paper §5.5).

## Deliverables

1. **Prereg FIRST (P9):** predictions and falsifiers committed before any engine or artifact
   edit — predicted direction/size of candidate-board movement, the falsifier list, the exhaustive
   shipped-vs-refit difference list above. Correct the prereg against the tree, never the tree
   against the prereg.
2. **One committed, versioned refit entry point** per artifact (or one orchestrator), producing
   candidate artifacts at CANDIDATE paths in-repo (never overwriting the live pickles or
   `/home/claude/cm_400.pkl`).
3. **Candidate board** built in the worktree from the candidate artifacts. Any switch this needs
   must be DECLARED in the prereg, wired at exactly one site, and default to shipped behaviour —
   never an undeclared name nothing sets (the RL_*/PAR_* burn class).
4. **THE MOVERS REPORT vs the live board `6fd0f7de`** — the owner-facing deliverable: up/down/flat
   counts, every mover by size, the biggest named individually, T1's contribution named.
5. The full measurement battery above, filed under
   `docs/evidence/rebake_arm1_store_alone_2026-08-24/` with a `REPORT.md` the supervisor can
   verify by re-running the deciding figures.

## Practices (a breach is an abort, not a footnote)

- Work in your ISOLATED WORKTREE on its own branch; never write the shared
  `/home/claude/rl_workspace` — do everything from the worktree checkout per
  `docs/runbooks/STANDING_PROCEDURES.md` (pinned venv `/root/rl_venv312`, single-thread BLAS,
  `RL_REPO`/`RL_FV` bound to the worktree).
- NEVER touch `docs/register/` — the pen is the supervisor's.
- Explicit-path commits only (P8). Committer identity: the configured repo identity
  (`Claude <noreply@anthropic.com>`) — NEVER the owner's email. Standard trailers.
- P4: assert relationships, never hand-typed identities — measure every hash from the artifact.
- Owner-only words (law 10) are out of reach: no tags, no live-pin moves, no rulebook edits, no
  score-write arming.
- Assume this act finds something not on this list (scope paper §5.8) — report it, do not absorb
  it silently.
