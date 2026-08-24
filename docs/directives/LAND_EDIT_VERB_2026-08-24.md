# THE EDIT VERB — `tools/land edit` · directive 2026-08-24

**Owner words, verbatim (2026-08-24):** *"There will likely be lots of out of round edits. So that
lander needs to be redone so round edits are one option, but there's also a general edit option.
That is user unfriendly as it stands."*

**Context (register v836):** the Graham dual correction — an owner-worded one-field store edit —
was refused three times by the lever lander, each refusal byte-exact and correct: the lineage chain
demands the store move INSIDE the transaction, and the lever sequence has no step that edits a
store. The last out-of-round store writes predate the lander. The owner has now ruled the general
lane into existence.

## THE VERB

A third verb beside `lever` and `round`, same one-library law (S7 — no mirrored script pairs):

    tools/land edit --spec <edit_spec.json> [--dry-run]

1. **Declarative edit block** in the spec: a list of `{key, field, old, new}` store edits. `old` is
   asserted against the store before applying (a mismatch is an abort, not a repair — the exact-
   string law, ERRATUM E2 class). The edit is applied as a SURGICAL byte replacement inside the
   named row's span, never a whole-file rewrite (the store's serialization is not round-trippable;
   proven at the Graham act).
2. **A new `store_edit` step** inserted after `preflight`, before `build_proofs`, applying the edit
   in the WORK DIR — so the lineage source side (measured at HEAD) is pre-edit, the destination is
   post-edit, the pins step re-pins `store` measured-not-typed, and the chain stays continuous with
   no flip commit and no pin-companion choreography. The rest of the sequence is the lever's own
   shared steps (contract, sibling, ui, state, gates, claims, commit) — registered, not copied.
3. **`--dry-run` is the user-friendly half:** applies the edit in a scratch build, prints the
   one-screen summary (store old→new md5, board old→new md5, EVERY mover with values, identities
   that move), and writes NOTHING to any carrier. The owner reads the dry-run, gives his word, the
   spec cites it verbatim, and the same command without `--dry-run` flies. One command to predict,
   one to land.
4. **Spec validation** (`tools/landing/spec.py`): `act_kind: "store-edit"`; requires the edit
   block, owner word, lineage citation fields, column (an out-of-round board move still earns its
   column per the 2026-07-28 standing rule), `day0_rebase` (default off); `board_after` in the
   prereg block is OPTIONAL for this kind — when present it is asserted byte-exact at build_proofs
   (the Graham re-flight will use its standing prediction 82fcd8bb), when absent the dry-run is the
   prediction of record and build_proofs asserts internal consistency (bare build reproducibility).

## NON-NEGOTIABLES

- **Self-test coverage** (`tools/landing/selftest.py`): new cases for the verb, each proven able to
  fail — old-value mismatch aborts; a second unexpected mover aborts when board_after is declared;
  mid-step failure restores every carrier byte-exact (the commit-rewind leg); the happy path lands
  and the lineage entry's source/destination straddle the edit. The existing lever and round cases
  stay green untouched.
- **P1 proof:** adding the verb moves NOTHING — every carrier and the live board byte-identical
  until an edit act actually flies. State it and measure it.
- **P9:** prereg for this tooling act committed before the first edit to `tools/landing/`.
- **P8 / identity:** explicit-path commits, configured identity, never the owner's email.
- Work in your ISOLATED WORKTREE on its own branch; never touch `docs/register/`; no pushes; the
  supervisor reviews, lands the verb, and flies the real Graham act himself.
- The store remains the ONE SOURCE and edits remain OWNER-WORDED: the spec must carry his words
  verbatim; the verb is a lane, not an authority.

## ACCEPTANCE

The Graham edit spec (`docs/evidence/graham_dual_2026-08-24/`, prediction standing: store
`daa93053 → fb640ca0`, board `6fd0f7de → 82fcd8bb`, one mover will-graham 1533 → 1271) must fly
clean through the new verb IN THE SELF-TEST SANDBOX (not against the live tree). Hand back: branch
+ tip, prereg commit, the new/changed files, self-test counts (with the new cases named), the
sandbox Graham flight transcript, and anything found that was not on this list.
