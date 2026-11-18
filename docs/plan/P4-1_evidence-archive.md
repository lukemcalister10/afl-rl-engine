# P4-1 — Evidence: (a) the retro guards fail loudly; (b) the archive branch (owner decision D4)

Two items, landed separately and far apart in the order (README #2 and #15).

## P4-1a — hard-fail the two exists-guards (LOW, ~10 lines; depends on nothing; serial rule: steps.py)
**Facts (checked at 9a400286).** tools/landing/steps.py:2529-2530 wraps writer 4b in `if os.path.exists(_retro):`
and :2650-2652 wraps writer 4c's bank in `if os.path.exists(_bank) and not _res.get('already_present'):`.
Writer 4 has already dropped the retro series (:2496-2500), so a moved or missing emitter ships a bundle with no
movers series and no error. The scripts also locate the repo by depth: emit_retro_series.py:23 and emit_asat_seasons.py:41
(`REPO = HERE/../../..`), so moving their directory breaks them even if the guards are fixed.
**Done when.** A missing `_retro` or `_bank` file raises StepError naming the path and the remedy; the
`already_present` skip is kept exactly as it is.
**Must not change.** Behaviour when both files exist (every gate and carrier identical).
**Prove it.** `python3 tools/landing/test_txn.py`, `test_store_edit.py`, `test_proofstash.py`; a new test (or a
scratch-tree run of the ui step) with each file renamed shows the StepError; acceptance `--profile full` green.
**Lands via.** Plain commit.

## P4-1b — the archive branch and, separately, a history rewrite (LOW; owner decision; after P4-4)
**Facts (checked at 9a400286) — the honest benefit.** docs/evidence is 219 MB in the worktree (149 directories +
INSTRUMENTS_INDEX_2026-08-10.md); the repository's .git was 222 MB (pack 173 MB) on a full clone at ffb2663b (not
re-measured: the 9a400286 check ran on a shallow clone). `git rm` does not shrink history, and CI checks out with
`fetch-depth: 0` (.github/workflows/final-integration.yml:69,88; fv-provenance.yml:44), which fetches every
branch, so an `evidence-archive` branch on origin is downloaded by CI anyway. The ONLY gain of an archive branch
plus `git rm` is checkout/worktree size (~219 MB per worktree). Shrinking clones requires rewriting history
(filter-repo + force-push of main), which changes every commit SHA the register, release_lineage.json and the
evidence notes cite — that is a separate decision that needs the owner's explicit word; do not do it under D4.
**Live readers (code, not comments) — each stays, or moves in the same commit as its reader:**
- walkforward_retro_2026-08-29/ — steps.py:2529, :2541, :2552-2555, :2650; tools/ingest.py:444-448 (WEEK_CARRIERS
  glob `values_r*.json`); the depth-based REPO in its scripts (above); `tools/harness …/pass_retro_series.py` and
  `pass_asat_seasons.py` (steps.py:2555 remedy text); ui/tests/movers.test.js:688 (message).
- final_candidate_2026-08-19/DAY0_CP.json — carriers.py:308-313, txn.py:376.
- candidate_31f/ext_2026-08-17/t338_extended_DISCLOSED.py — md5-pinned by tools/noarb_standing_page.py:37-38.
- exec_306_zlaarm/ — copied by staged_apply.py:808; read by the refit lane (_merged_recover.py:2163-2165,
  :2382-2384) and by ui/tests/draftday.test.js:753-754.
- finals_fw1_2026-08-30/FW1_EDIT_PLAN.json — engine/rl_after/ingestion/test_finals_report.py:66 (a DEFAULT_GATE).
- ingest/ — tools/ingest.py:616 writes each week's evidence there; act evidence dirs named in specs.
- tools/landing/carriers.py has NO walkforward reference (the old brief was wrong to list it).
Re-run before deleting anything: `git grep -n "docs/evidence\|'evidence', '" -- '*.py' '*.js' '*.mjs' '*.sh' '*.yml'
':!docs/evidence' ':!session_*' ':!backups'` and classify every hit (comment / fixture string / live read).
**Done when.** `evidence-archive` exists on origin at the pre-trim main; main has one `git rm -r` commit listing
every removed directory and naming the branch; every live reader above still resolves.
**Must not change.** Any file a reader above opens; docs/register/, docs/STATE.md; the last 10 act directories.
**Prove it.** Every DEFAULT_GATE (steps.py:139-185) green on the trimmed tree (run them); `test_proofstash.py`,
`test_txn.py`; `md5sum` of the T338 file still equals T338_MD5 (noarb_standing_page.py:38); acceptance `--profile
full`; CI green.
**Lands via.** Plain commit + `git push origin evidence-archive` (reversible). History rewrite: owner word only.
