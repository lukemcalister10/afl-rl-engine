# P4-3 — The engine flip moves inside the landing transaction (MEDIUM)

**Goal.** An engine act no longer needs the hand procedure (edit data/expected_boot.json pins → `restamp.py
apply` → "the flip" commit → fly). The lander's `pins` step measures engine_head / rl_model / fv from the tree
it is landing, and a lever spec declares them in `moves` when the engine source changed. tools/restamp.py
becomes a check-only tool (or is deleted once nothing else needs `apply`).

**Why.** Every engine act today is two commits and a ritual that an agent gets wrong on the first try (ORDER 45
attempt 4; the chain act's first flight 2026-10-14; the survival act's stamp drift). The spec law that
"flip-carried identities go in `unmoved`" exists only because of the ritual.

**Files.** tools/landing/steps.py (`pins`, `_measure_sides`, PIN_MEASURERS / DELEGATED_PINS; the `contract`
step's restamp_dynamic), tools/landing/spec.py (FLIP_SCOPED_IDENTITIES / NO_WRITER_IDENTITIES rules),
tools/restamp.py (+ tools/test_restamp.py), docs/runbooks (the flip procedure text), tools/landing/carriers.py
(board_view_working / club_valuation stamps carry engine_head — the UI writers must re-stamp inside the txn).

**Rules.** A spec may declare engine_head/rl_model/fv in `moves`; then the pins step asserts the tree's md5s
differ from the pinned ones BEFORE the build and writes the new pins in the transaction; `unmoved` keeps its
byte-stability assertion. The old specs (flip-carried, declared unmoved) must still validate and still land
(backwards compatible). The restore point must put the pins back on abort (they are carriers already).

**Proof.** A rehearsal: a comment-only change to _merged_recover.py landed as a lever act with engine_head in
`moves` and board byte-identical, on a worktree with a scratch remote (no push), end to end; test_txn,
test_restamp, spec validation of all existing specs; acceptance green.

**Lands via.** Plain commit of the lander; the rehearsal act is the proof (its evidence dir committed).
