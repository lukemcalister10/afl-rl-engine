# DIRECTIVE — OWNER TOOL: LTI REGISTER RE-PIN · 2026-07-16 · seat 9 (Fable) · FIREABLE NOW
### Tier 3, DISJOINT from the Leg-B engine fence (tools/ + data pin only — S3 parallel-safe).
### Fresh Claude Code (Opus) chat. Low-Medium · auto · **1–1.5 h**. SILENCE IS A RED. Report
### context at HALT/RETURN; reap background tasks.

## THE JOB — `tools/owner/lti_repin.py` (one command the owner runs after editing LTI_REGISTER.md)
1. VALIDATE the register: table parses · every player name resolves against the store (report-only
   read of rl_model_data.json — this tool NEVER writes the store) · sections/статуses in the known
   vocab · dates sane. Any failure ⇒ refuse with the exact row and reason (validate-or-halt).
2. RE-PIN: update `data/expected_boot.json`'s register md5 to the edited file (THE ONLY pin this
   tool may move; assert every other pin unchanged before and after).
3. REPORT: print the diff of register entries (added/removed/changed) + the old→new md5 + the
   plain instruction "rebuild the board to consume this" (the tool does NOT itself rebuild).
4. TESTS: a good edit re-pins · a bad name refuses · a non-register change to expected_boot is
   detected and refused · idempotent on re-run.
## BASE PIN: main at-or-after `94ec2d9`, `git diff --name-only 94ec2d9..main` docs/-only. Branch
## from main; PR; per-task commits. FENCE — IN: tools/owner/ · the ONE pin field · tests · a short
## HOW_TO block appended to ui/HOW_TO_UPDATE_INPUTS.md's pattern (new file docs/HOW_TO_LTI.md is
## fine). OUT (HALT): engine/ · the store · every other expected_boot field · docs/ beyond the
## HOW_TO · ui/. RETURN ≤15 lines: head SHA · PR · tests · actual time · context.
