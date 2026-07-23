# MODEL REVIEW BRIEF — ITEM 409 · filed 2026-07-23 · supervisor pen (Fable seam seat)
For: a fresh Fable chat = **MODEL REVIEW SEAT** (investigation supervisor; the owner sits in
this chat) directing one **Fable Code session** as read-only hands. This brief is your charter.
You are NOT the seam authority and NOT the supervisor pen — that seat exists separately.

## Context handover (verify, don't trust — every prior claim is a hypothesis until re-run)
- Repo: github.com/lukemcalister10/afl-rl-engine (public). Governing doc: docs/RULEBOOK.md on
  main. Structure of record + seat rules: register header v384+ and docs/directives/SEAT_CHARTER_sol.md.
- ITEM 408 (R14→R19 provenance migration) is IN FLIGHT on branch ci/r19-provenance-migration
  under the execution supervisor. That branch is UNTOUCHABLE by this seat. Work from main only.

## First acts, in order
1. **Pin your world.** Record the identities you are reading and stamp every finding with them:
   live store md5 (expect f37d9716), board of record (expect 6f07f7cb), frozen pick curve
   89c14729 (source store 968de0c7, per_entrant 40d7da7c). If any differ from expectation, a
   bake landed — note it and pin to what you measure, never to "current".
2. **Seal the owner reads.** Take the owner's valuation concerns and player examples VERBATIM,
   date them, anchor them at R19, file them in your working notes BEFORE any measurement runs.
   The analysis reconciles against sealed reads; it never rationalises around them.
3. **Ingest the pre-work issue register** (the owner supplies it in-chat; it is a seat document
   from a prior audit — flaws + improvements on the artifact being canonised). Treat every entry
   as report-only until re-run.

## The investigation (direct Fable Code; read-only; scale as evidence demands)
A. **Replacement-floor shape.** Owner's stated concern, sealed as the primary read: the model
   punishes players who are neither elite nor young — value-over-replacement is applied too
   convexly at the floor. "+2 above replacement is still solid vs −10 below it; price is not
   binary; locking cheap +2 players frees budget to consolidate elsewhere" — a real team-level
   value the per-player lens may miss. Measure: value vs points-above-replacement across the
   full board; cliff/kink detection at the floor (the rulebook's own L-SMOOTH law speaks
   against cliffs); the "solid cohort" (mid-output, mid-age, durable) vs the owner's examples.
B. **Curve-tail triangle.** Late-pick pricing is partly the FROZEN ruler, not the live model:
   pick prices come from curve 89c14729, deliberately anchored to its R14-era pool (R1=C
   ruling); player values come from the R19 store. Resolve three-way: current frozen tail vs
   the R19 re-derivation (known direction: tail RISES, pick99 463→483) vs the owner's instinct
   (tail should FALL). This is decision-critical input to the queued RL_PVCFIT release.
C. **Issue-register triage.** Re-run what's cheap, classify the rest; fold into the memo.

## Fences (absolute)
- READ-ONLY on engine, store, board, contracts, tests — everything. No pushes, no writes, no
  branches, no PRs, from either the chat seat or the Code hands.
- No contact with ci/r19-provenance-migration. No model changes from this seat, EVER — changes
  become their own owner-worded release after ITEM 408 merges, under the full seam pattern.
- Provenance-tag every claim: [owner-seen] / [re-runnable] / [report-only]. An owner read is
  ground truth; a measurement is evidence; never conflate them.
- Escalate to the seam seat (via the owner) on: fence ambiguity, anything suggesting the live
  store/board is wrong (not just the model's shape), or any plan-changing surprise.

## Deliverable
One evidence memo: identity-stamped, every claim re-runnable, findings vs sealed reads stated
plainly (confirmed / refuted / partial, with margins), candidate hypotheses for the post-408
model release ranked by decision value. It returns to the owner; the supervisor pen files it.
