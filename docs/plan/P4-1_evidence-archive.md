# P4-1 — The evidence archive branch (LOW; owner decision D4 = yes)

**Goal.** `docs/evidence/` (148 act directories, 216 MB) stays complete in history on an archive branch
`evidence-archive`, and `main` keeps only the directories something live reads plus the last 10 acts.

**Why.** Every clone, CI checkout and worktree carries 216 MB of flight logs and gate outputs nothing reads;
the owner's pain point is the weight of the repo.

**Rules.** FIRST find what reads docs/evidence at runtime: `grep -rn "docs/evidence" --include=*.py
--include=*.js --include=*.yml --include=*.sh . | grep -v "^./docs/evidence"` — known live readers today:
docs/evidence/walkforward_retro_2026-08-29/ (the retro + as-at machinery and banks: KEEP, and consider moving
it to tools/retro/ in the same change, updating every reference incl. tools/ingest.py WEEK_CARRIERS,
tools/landing/carriers.py, the landing steps' retro bank writer, ui/MAINTAINER.md), fw1/fw2 report emitters
(check), anything the acceptance checks or release_manifest_check.py name. Nothing that a gate reads may move
without the gate moving with it. Create the archive branch from the current main (so history is intact there),
then on main `git rm -r` the dead directories in ONE commit whose message lists them and names the branch.
Keep the last 10 acts by date (they are the recent record). docs/register/ and docs/STATE.md untouched.

**Proof.** acceptance green; every landing gate in tools/landing/steps.py DEFAULT_GATES still runs green on
the trimmed tree (run them); `python3 tools/landing/test_proofstash.py`; CI green on the pushed tree.

**Lands via.** Plain commit + `git push origin evidence-archive`. Reversible: the branch holds everything.
