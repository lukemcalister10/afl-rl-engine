# DIRECTIVE — THE BASE GUARD (tools/seat/first_commands.sh + prescreen hook)
2026-07-17 · supervisor seat 11 · Opus · ONE JOB, ONE CHAT · disjoint-file (runs in parallel, S3)
STATUS: ISSUED — fire when pasted by the owner.

## BASE (this job writes TOOLS, so it branches from MAIN)
```
git ls-remote https://github.com/lukemcalister10/afl-rl-engine.git refs/heads/main
git fetch origin main && git checkout -B claude/tools-base-guard origin/main
git log -1 --format=%H   # MUST be bee58cc71079112fb0b1c9b6ed039f338d78a801 OR LATER with
git diff --name-only bee58cc71079112fb0b1c9b6ed039f338d78a801..HEAD   # docs/-ONLY (the pen moves main) — else HALT.
```
Commit the output as FIRST_COMMANDS_PROOF.txt (yes, the guard job proves its own base by hand — the last time).

## THE FIVE
EFFORT: Medium (small, sharp tool; why not Low: it must fail correctly, which needs red-path proofs).
MODE: auto; PLAN first. TIME: 1–2 h. FEED: register items 264 · 270 · 298 · 299 (the failure class);
directive v1.1's execute-first block (the manual template being mechanized). FENCE: `tools/seat/` +
`session_2026-07-17/base_guard/` ONLY. You never touch engine/, data/, docs/, run_panel.sh.

## THE JOB
1. **`tools/seat/first_commands.sh BRANCH_REF EXPECTED_SHA NEW_BRANCH [EXPECTED_STORE_MD5] [REQUIRED_SYMBOL[:FILE]]`**
   Does, in order, each printing an explicit PASS/FAIL verdict (SILENCE IS A RED — a check that
   prints nothing has failed; set -euo pipefail; non-zero exit on ANY failure):
   ls-remote(BRANCH_REF)==EXPECTED_SHA → fetch → checkout -B NEW_BRANCH EXPECTED_SHA →
   merge-base --is-ancestor proof → optional store-md5 assert → optional symbol grep-count ≥1 →
   writes the full transcript to FIRST_COMMANDS_PROOF.txt in the CWD and prints the one line the
   build must commit it with. Refuses to run if the working tree is dirty.
2. **Prescreen hook:** extend `tools/seat/prescreen.sh` with a first check: the branch's FIRST
   commit contains FIRST_COMMANDS_PROOF.txt and its recorded SHA matches the branch's actual base
   — verdict printed, non-zero on fail.
3. **RED-PATH PROOFS (committed):** run the script against (a) a wrong EXPECTED_SHA, (b) a wrong
   store md5, (c) a missing symbol — all three must FAIL loudly with non-zero exits; transcripts
   committed to the session dir. One green-path run against the true relay pin committed too.

## RETURN
≤20 lines · branch + head SHA + PR · the four proof transcripts · "in plain terms" close.
