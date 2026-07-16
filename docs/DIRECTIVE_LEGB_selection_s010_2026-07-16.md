# DIRECTIVE — LEG-B SELECTION: WIRE s = 0.10 (OWNER-SET) + CLEAN RE-MEASUREMENT · 2026-07-16 · seat 10
### STATUS: fires on the owner's paste. OWNER RULING OF RECORD (register item 265, verbatim):
### "Let's lock in s=0.10 and move forward." This supersedes memo v1.3's machine-selection
### construction (the β ≥ 0.80 bar + the {0.55–0.70} grid are RETIRED — the strength is now an
### OWNER-SET number, like the fade d=0.25). ZERO seat-authored numbers: s = 0.10 is his.
### This is the chapter's ONE store/engine writer. The s=0.10 numbers to date are viewing-grade
### (item 264 base violation); THIS build re-measures them CLEAN on the properly-based line.

## EFFORT: Medium. Why not Low: a value-moving engine constant + the full frozen battery +
## guards is real verification surface. Why not High: one constant, a proven harness, no design.
## MODE: auto — PLAN first. TIME: 45–90 min. Confirm; flag >2×/<½×; report actual + APP/wall.

## BASE PIN — full-URL ls-remote against https://github.com/lukemcalister10/afl-rl-engine.git
- **Engine base — STRICT:** branch `claude/legb-conserved-measurement-j9tcf7` at **`fef2b64`**
  exactly (the candidate line: 91d08f2 + the default-off RL_UNCONSERVE toggle + the measurement
  record). NEW branch FROM IT — verify `git merge-base --is-ancestor fef2b64 HEAD` yourself and
  print it in the return (the item-264 lesson: artifacts and the tree that made them travel
  together; a scratch-staged engine is NOT conformance).
- **Docs base:** main AT OR AFTER the SHA in the owner's paste; diff docs/-only.

## FEED
Register items 258/259 (the band: floor 1.08 · cap 1.30 · ideal 1.15–1.25) · 262 (corrected
verdict law) · 264 (base-violation lesson + viewing-grade status) · 265 (THE RULING) ·
docs/acceptance_v1_20.json (seal 6b83e336) · session_2026-07-16/legb_conserved_measure/ (harness
of record) · session_2026-07-16/uncompress/beta_measure.py (FROZEN 14c59139) · this directive.

## THE JOB
1. **THE WIRE (one commit):** `rl_model.py` UNCOMP_S_DEFAULT: None → **0.10**, comment carrying
   the owner provenance (item 265; "the bar/grid construction retired — owner-set strength").
   UNCOMP_DECAY stays 0.25; RL_UNCONSERVE stays default-off; nothing else. Then a
   MINI-CHECKPOINT HALT (≤5 lines, diff SHA pushed) for the supervisor's diff prescreen.
2. **ON PROCEED — the clean battery at the WIRED DEFAULT (no env override — prove the default
   path itself):** the new default board built + named (md5) · kill-switch A/B: RL_UNCOMP=0 ⇒
   `8d90c9ac` BYTE-EXACT · full self-test suite GREEN (incl. the R105.5/R105.4 guards + SSI
   guards) · frozen β (CI/width/n) · G-COHORT y4/y5/y6 via the frozen July-8 construction,
   judged against the FULL BAND both sides · E/B vs 1.75 with raw parts · census gauge ·
   position-pool Δ totals · net ΣΔ · the all-804 SINCERITY ledger CSV (item-256 schema) with
   named top-20 rank gainers/losers + Bontempelli + every SCAR-up-rank-down row named ·
   A-PAIRS pair 2 + pair 3 scored (expected at s=0.10: pair_2 ≈ −14% FAIL — score and report,
   do NOT flag as a defect; its disposition is an open owner word) · S1 stamps on the new board.
3. Candidate PR opened (base fef2b64 line), number in the return.

## FENCE
IN: the one constant · the battery · session artifacts under
`session_2026-07-16/legb_selection_s010/` · the PR. OUT (touch = HALT): the STORE · docs/ ·
config · acceptance · gate/guard code · the toggle's default · any other constant · any re-tune.
SILENCE IS A RED — every check prints a verdict or the job HALTs.

## RETURN
≤30 lines + plain close: branch · head · PR · ancestry line (`fef2b64 ancestor: yes`) · new
default board md5 · A/B proof · suite verdict · β · y-band verdict both sides · E/B raw ·
Bontempelli SCAR+rank · pairs 2/3 · sincerity-fail count (named) · net ΣΔ · actual time.
The ladder (cold audit · sealed reads · owner viewing · his word) comes at CHAPTER END — this
build merges nothing and bakes nothing.
