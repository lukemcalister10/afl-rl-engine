# PLAN — SEAT-TOOLS FIX 1: orient.sh register step

**Directive:** Fable supervisor seat, 2026-07-15. Tier 3, read-only tooling. Register items 119/120.
**Branch:** `claude/orient-register-step-fix-7p999u`
**Time band:** 10–25 min (confirmed; flag if >2× or <½×).

## Base pin — VERIFIED
- main == `75bc9bc4872bb38a844d83e1b6ef536043a76ef2` (at-or-after `0c4aba84`: ancestor check PASS)
- `git diff --name-only 0c4aba84..main` == `docs/OPEN_ITEMS_REGISTER.md` (docs/-only). PROCEED.

## The finding (item 119)
`orient.sh` step 2 "register header (raw line 1)" reads root `LTI_REGISTER.md` (availability sidecar),
NOT `docs/OPEN_ITEMS_REGISTER.md` (the durable open-items log whose header the freshness check requires).
The rung is omitted under a label that suggests it is covered.

## The job (fenced)
1. `tools/seat/orient.sh`:
   a. The "register header" step reads + prints line 1 of `docs/OPEN_ITEMS_REGISTER.md`.
      - die loud if file absent OR line 1 empty (SILENCE IS A RED, house law #3).
      - line is very long (~2001 chars): print first ~200 chars; append explicit ` …(truncated)`
        marker when the line is longer. Version + PEN summary lead the line (freshness-relevant part).
   b. KEEP the `LTI_REGISTER.md` existence check + header print, RELABELLED honestly
      (e.g. `-- LTI register header (pinned input, root) --`).
   c. No other behavioural change to the script.
2. Refresh `tools/seat/samples/orient.out.txt` from a live run (same 4-line comment header; exit 0 recorded).
3. NEGATIVE TEST (committed here): temp copy of checkout with `docs/OPEN_ITEMS_REGISTER.md` removed →
   orient.sh exits NON-ZERO with FAIL message. Never touch the real file.

## Fence — writes ONLY
- `tools/seat/orient.sh`
- `tools/seat/samples/orient.out.txt`
- `session_2026-07-15/seat_tools_fix1/`
Everything else read-only. No store/engine/data/docs writes.

## Steps
1. [x] Base pin verify · read orient.sh, sample, register items 119/120, CORE seam-pack rule.
2. [x] Commit this PLAN (first artifact).
3. [x] Edit orient.sh: new open-items rung (docs/OPEN_ITEMS_REGISTER.md line 1, die-loud, 200-char
       truncate) + LTI rung relabelled honestly as pinned input (root). Syntax OK, live exit 0.
4. [x] Live run → refreshed sample (4-line header; exit 0 recorded).
5. [x] Negative test proven (negative_test.md): register removed from a full checkout copy → exit 1,
       loud FAIL, real file untouched.
6. [x] Commit + push -u origin branch.
7. [x] RETURN.
