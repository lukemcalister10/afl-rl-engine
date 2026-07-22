# DIRECTIVE — READ-ONLY DIAGNOSTIC: THE QUALIFYING-SEASON RULE · v2 · 2026-07-16 · seat 9 (Fable)
### ⚠ THIS IS ITS OWN FRESH CHAT — separate from, and parallel to, the Leg-B build chat (S3). It
### MEASURES; it writes NOTHING to store/engine/board/docs. v2 consolidates the v1 directive + its
### addendum (both archived) after a cross-model review: the DECLINE third category folded in, the
### interruption BAR declared, pins tightened. Fresh Claude Code (Opus) chat · Tier 3 · **HIGH** ·
### ~2–2.5 h. SILENCE IS A RED. Report context at HALT/RETURN; reap background tasks.
### EFFORT — why not one lower (owner-challenged, raised from Medium): the job is read-only and its
### NUMBERS are re-verified downstream, but its CLASSIFICATION TEST is a judgment surface that shapes
### memo v1.2 directly — a subtle classification error costs a DESIGN ROUND (three paid today), and
### the insurance (self-verify the test against the named cases BEFORE committing the census; sanity-
### check phase boundaries on knowns) is ~30 min on a 2 h job. High buys verification breadth at the
### one point downstream checks reach LAST. Why not Extra: the harness is pre-built and pinned, the
### sample is fixed, nothing ships — design-grade scrutiny belongs to the memo, not the measurement.

## WHY (register items 230/231/233)
Leg B's un-compression target reads a player's recent-2 QUALIFYING seasons. A hard games-floor
mislabels careers at BOTH ends of the arc: it deletes a developing player's 4–9-game EARLY seasons
(his year-4 reads as year-1 — a phantom rookie, under-reading the protected young cohort), and any
fix that excludes "low-game seasons with a prior higher level" also sweeps up a POST-PEAK veteran's
low-game season — which may be the decline SIGNAL itself, so excluding it would inflate fading
veterans (the mirror defect). The cure must condition on CAREER PHASE. This job sizes all of it in
real counts so the rule is designed on evidence. FINDINGS ONLY — no design adopted here.

## PINS (verify by full-URL ls-remote / fresh fetch; state every SHA you read in the findings)
- Store/engine READ base: the candidate parent **`c27d697`** (store `b1fd0bce` — assert its md5).
- The frozen-β harness: **`e3ff2c7`** on branch `claude/legb-segment3-v1-rewire-5jy7f3`
  (`session_2026-07-16/segment3_rewire/rho_axis_v11.py` + CONFIRM) — read AT THAT SHA (the branch
  is moving; the pin is not).
- Docs: main AT OR AFTER **`8272aff`**, `git diff --name-only 8272aff..main` docs/-only.

## THE CLASSIFICATION (used by every measurement below)
For every real player-season with games in [1, 9], classify into exactly one of THREE:
- **ASCENT** — pre-established: no prior season at a demonstrably higher level (the early-career rung).
- **INTERRUPTION** — a dip below a level already demonstrated, at an age ≤ PEAK_AGE[pos] (the
  injury case; Docherty-class).
- **POST-PEAK LOW-GAME** — same dip test but age > PEAK_AGE[pos] (may be decline signal, NOT
  presumed interruption — sized separately for the owner to rule on).
"Demonstrably higher level": state the exact test you use from the engine's own machinery
(`level_demo` / `_nqual` family) in the findings — one test, applied uniformly.

## THE FOUR MEASUREMENTS
1. **THE MISLABEL CENSUS:** counts of players holding ≥1 season in each category; how many players'
   recent-2 window CHANGES under a hard floor of 6, and of 10 (i.e. a genuinely different season
   pair chosen vs no-floor); top-20 by |window shift| with name · pos · age · category.
2. **THE CONDITIONED RULE (measure, don't adopt):** qualifying = keep every season EXCEPT
   INTERRUPTION-classified ones, at BAR = 6 AND at BAR = 10 (the games threshold inside the dip
   test — run both). POST-PEAK LOW-GAME seasons are KEPT in the base variant and EXCLUDED in a
   sensitivity variant — report both (this is the category the owner must rule; show its size and
   its effect). Report the recent-2 measure's delta per cohort (≤22 · 23–26 · proven-27+) under:
   floor-6 · floor-10 · conditioned@6 · conditioned@10 (base and sensitivity).
3. **λ RE-MEASURE:** the target-axis output-elasticity λ_ρ (the pinned frozen fit_beta harness,
   same n=116 sample) under each rule variant of (2). The Leg-B fix needs λ ≈ 1 — flag any variant
   that materially degrades it.
4. **NAMED CASES (the concrete mislabels):** the exact recent-2 window each rule picks for —
   one Docherty-class established-then-injured player · THREE young key-position players with
   4–9-game early seasons (you choose; name them) · TWO post-peak veterans with a recent low-game
   season (you choose; name them) · Harley Reid.

## DELIVERABLE + RETURN
Findings committed to `session_2026-07-16/qualifying_diag/` on a fresh read-only branch (fine to
branch from main; nothing merges). One-paragraph read at the end: does the conditioned rule fix the
young mislabel WITHOUT breaking injury exclusion, what does the post-peak category cost/save, and
at what λ. RETURN ≤15 lines: head SHA · SHAs read · the census headline · λ per variant · actual
time · context.

## FENCE
IN: the one session_ diagnostic dir on your own branch. OUT (touch = HALT): store · engine ·
board · gates/guards · docs/ · ui/ · any branch you did not create. This job cannot move the
candidate line; it informs MEMO v1.2, which the supervisor authors.
