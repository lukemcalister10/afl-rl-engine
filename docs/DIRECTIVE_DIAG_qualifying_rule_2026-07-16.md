# DIRECTIVE — READ-ONLY DIAGNOSTIC: THE QUALIFYING-SEASON RULE · 2026-07-16 · seat 9 (Fable)
### Tier 3, READ-ONLY, DISJOINT from the Leg-B engine lane (measures; writes NOTHING to store/
### engine/board). Fresh Claude Code (Opus) chat, PARALLEL to the halted seg-3 build (S3). Grounds
### memo v1.2's development-aware qualifying rule in COUNTS, not intuition. ~1-1.5 h. Report context
### at HALT/RETURN; reap tasks. SILENCE IS A RED.

## WHY (register items 229/230; owner-caught defect)
A hard games-floor for the recent-2 qualifying-season measure MISLABELS developing players: a young
key-pos player with 4/7/9-game early seasons has them EXCLUDED, so the measure reads year-4 as his
FIRST season — a phantom rookie, under-reading exactly the young cohort items 130/170 protect. The
same low game-count means OPPOSITE things: an INTERRUPTION to an established level (injury — exclude)
vs an ASCENDING early-career rung (development — keep). The fix must condition on WHICH, not on the
count. This job MEASURES the size of the problem and tests the conditioned rule before it is designed.

## THE MEASUREMENTS (read-only, off the store at b1fd0bce; NO board write)
1. **THE MISLABEL CENSUS:** over all real players, count seasons with games in [1,9] and classify
   each as (A) INTERRUPTION — a dip below a level the player had already demonstrated (prior
   qualifying season at higher level) — or (B) ASCENT — part of a non-decreasing early-career
   sequence before any established level. Report: how many players have ≥1 sub-floor ASCENT season
   that a floor=6 / floor=10 would exclude; of those, how many would have their "recent-2 qualifying"
   window SHIFTED (i.e. a genuinely different pair chosen). Name the top-20 by |shift| with pos/age.
2. **THE CANDIDATE CONDITIONED RULE (measure, don't adopt):** define qualifying as — keep a season
   unless it is an INTERRUPTION (games < BAR AND the player had a prior season at a demonstrably
   higher level, using the engine's existing demonstrated-level machinery `level_demo`/`_nqual`;
   state the exact test). Recompute the recent-2 measure under (i) hard floor 6, (ii) hard floor 10,
   (iii) the conditioned rule, and report the DELTA in the measure for the young cohort (≤22, 23-26)
   vs the proven-27+ cohort. The conditioned rule should move young players TOWARD their real recent
   output and leave proven injury cases (Docherty-class) excluded.
3. **λ RE-MEASURE:** the target-axis output-elasticity λ_ρ under all three rules (the seg-3 CONFIRM
   harness, frozen fit_beta) — does the conditioned rule keep λ≈1 (the fix must still clear its gate)?
4. **NAMED CASES:** print the recent-2 window each rule picks for: a Docherty-class established-then-
   injured player · 3 young key-pos players with 4-9-game early seasons · Harley Reid. Show the
   mislabel concretely.

## DELIVERABLE
A committed findings file (session_2026-07-16/qualifying_diag/) with the four measurements + a
one-paragraph read: does the conditioned rule fix the young mislabel WITHOUT breaking injury
exclusion, and at what λ. FINDINGS ONLY — no design adopted, nothing selected, no store/engine/board
write. RETURN ≤15 lines: head SHA · the mislabel count · λ per rule · actual time · context.

## BASE / FENCE
Base: any recent main or the c27d697 candidate head (READ-ONLY — measurement only; state which you
read). FENCE: a session_ diagnostic dir ONLY. OUT (HALT): any store/engine/board/gate/docs/ui write.
This job cannot move the candidate line; it informs memo v1.2, which the supervisor authors.
