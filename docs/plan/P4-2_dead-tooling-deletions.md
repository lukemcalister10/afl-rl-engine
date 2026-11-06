# P4-2 — Delete the retired tooling (LOW)

**Goal.** Remove the code the 2026-10-13 rulebook amendment and the sibling/LTI retirements left dead:
tools/landing/selftest.py (1,343 lines; the launch self-test, retired by P7/P9 retirement), tools/claims.py
and the `claims` step (retired echo), tools/landing/day0_emit.py and the `day0_rebase` spec slot (owner: off),
acceptance/selftest.py, the `--selftest` paths in tools/landing/cli.py, `engine/rl_after/ingestion/
sibling_repin.py` and `forward_lens.py` (kept only because staged_apply c3 imported them — remove that import
and the c3 lane with them if nothing else uses it), the sibling copy in the round lane (if P4-4 has not landed
yet, leave the round lane's sibling for P4-4).

**Why.** 11,345 lines in tools/landing alone; every retired step is a place the next change can break and a
page the next agent has to read.

**Rules.** For each deletion: `grep -rn` the symbol across tools/, acceptance/, .github/, docs/runbooks/,
docs/RULEBOOK.md, ui/tools/; a reference that is live is a reason to stop and report, not to delete. Specs:
tools/landing/spec.py must still LOAD every existing docs/evidence/**/ACT_SPEC.json (run the validator on all)
— a retired slot (`day0_rebase`, `claims`) becomes accepted-and-ignored, not refused. The RULEBOOK's retired
paragraphs (P7/P9/P11/P12) stay as written (numbers kept); update any runbook that names a deleted command.

**Proof.** tools/landing/test_txn.py, test_proofstash.py, test_store_edit.py, tools/test_restamp.py,
tools/test_ingest.py, ui/tests/ownership_store_apply.test.py; acceptance green; one REAL store-edit dry run
(`tools/ingest --check` on a finals file) still works; CI green.

**Lands via.** Plain commit, one per deleted unit, each message naming the ruling that retired it.
