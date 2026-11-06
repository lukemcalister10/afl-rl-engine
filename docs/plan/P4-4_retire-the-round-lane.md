# P4-4 — Retire `land round` (MEDIUM; after P2-1 and P4-3)

**Goal.** Delete ROUND_SEQUENCE and the round-advance lane from tools/landing (steps, cli verb, carriers,
spec `round-advance` kind, preview, packet, state writers that branch on it), the catch-up/staged_apply round
machinery that only the lane used (engine/rl_after/ingestion/staged_apply.py c-lanes, round_apply.py,
round_catchup.py, round_finalize.py — check each for a live reader first), and the sibling copy inside it.

**Why.** P2-1 makes `tools/ingest` the one path for every week; the round lane is then the second copy of the
weekly machinery, 2,000+ lines nothing runs.

**Rules.** Grep every symbol; a live reader stops the deletion of that unit. Existing round-advance ACT_SPECs in
docs/evidence (R15–R24) must still load in the validator (kind accepted as historical, not refused). The
release_lineage.json entries and the register are history: untouched. docs/runbooks/ and the RULEBOOK's
PART 3 wording ("land lever" and "land round") updated to the two lanes that remain: `tools/ingest` for weeks,
`land lever`/`land edit` for acts.

**Proof.** Full tools/landing test set; validator on all specs; acceptance green; the R24 replay from P2-1 still
reproduces; CI green.

**Lands via.** Plain commits, one per unit.
