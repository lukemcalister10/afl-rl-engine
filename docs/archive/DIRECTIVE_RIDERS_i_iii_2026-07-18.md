# DIRECTIVE — RIDERS (i)–(iii): the ladder viewing instruments · seat 13 · 2026-07-18
### Ruled R107.6 (DECISIONS v123, item 325 "Adopt") · REPORT-ONLY · read-only analysis build
### (Tier 3, no ladder; S3 parallel — runs ALONGSIDE the five-migration writer, disjoint files).
### Job: compute three of the four adopted ladder-viewing riders against the FROZEN Leg-D curve.
### Rider (iv) (the replacement-adjusted view) is NOT in this job — it waits on the measured-R
### report the five-migration build emits.

## BASE PIN (engine-content base ⇒ STRICT; run first, HALT on mismatch)
`git ls-remote https://github.com/lukemcalister10/afl-rl-engine.git claude/legd-pvc-rederivation-act2-l2hqpl`
must return exactly `e4177c21934148c19d9cec3c015fee5d28480102`. Branch from that head. Entry
assertions: boot-store guard (store md5 `968de0c7`) · `pvc_curve_v2.json` payload stamp `89c14729`
(file `56dd7a7b` — a KAT names WHAT it hashes). Every report artifact this job emits carries all
three stamps (code SHA · store md5 · curve payload md5) so the ladder can assert, mechanically,
that early-computed riders describe the final candidate.

## EFFORT: High
Why not Medium: these are the statistical instruments the owner reads at the ladder, and the one
prior attempt at this exact ground (a decile-bands proposal) was an owner-caught CORE-rule-7
violation (item 325) — the failure mode here is subtle statistics, not broken code. Why not Extra:
read-only, no value moves, no gate; everything is stamped and re-runnable.

## MODE: auto — first committed artifact is the PLAN (job→output map + the derived fence + method
sketch per rider). TIME: one chat, ~2–4 h wall; heavy bootstrap compute runs BACKGROUNDED with
completion markers and SPARSE polling (S6). Confirm the band up front; flag >2×/<½×; report actual.

## FEED (fetch from the repo/branch — documents, never prose restatements)
DECISIONS v123 (R107.6 = this job's ruling; R107.4 + CORE rule 7 = the statistical law; R107.7 =
gross stays gross) · CONSTRAINTS v1.19 + `acceptance_v1_21.json` (context only — nothing here
gates) · SPEC_PVC_FLEX_CHAPTER v1.4 §1+§1b (curve semantics) · SSI v1.3 · the artifacts at
`e4177c2`: `pvc_curve_v2.json` + the store + the Leg-D session derivation material
(`session_2026-07-17/legd_derivation/`) for cohort/pathway definitions. Deliberately NOT fed: any
owner read or expectation about the tail — this job MEASURES; interpretation happens at the
owner's viewing, not here.

## THE JOB LIST (one rider = one commit; census-grade provenance in every output)
1. **RIDER (i) — realized-outcome cohort-holdout calibration, + washout-exit calibration.**
   Curve-predicted pathway value vs REALIZED outcomes, cohort-holdout (fit-era vs held-out
   cohorts, per the Leg-D construction's own trajectory data; busts full weight — R107.3).
   Washout/delist exits calibrated as their own view. Output: smoothed predicted-vs-realized
   calibration curves by exact pick + the residual view.
2. **RIDER (ii) — cohort-bootstrap tail influence, + the short-draft-era caveat.** Bootstrap over
   cohorts (not rows) to show how much single players/cohorts swing the deep tail (~p50+); the
   short-draft-era caveat stated on the artifact itself wherever era coverage thins the sample.
   Output: per-exact-pick influence/stability view of the tail.
3. **RIDER (iii) — uncertainty grading past ~p50.** A continuous, smoothed uncertainty grade along
   the curve past ~p50 (bootstrap/holdout dispersion at each exact pick).
4. EXIT: `README` in the session dir mapping each artifact → the rider it serves → its stamps ·
   candidate PR (report-only; nothing merges without the owner's word).

## THE STATISTICAL LAW (BINDING on every output — the item-325 lesson, encoded)
Finest resolution the sample supports, SMOOTHED (kernel / local regression), per exact pick.
**NEVER decile bands, never wide bins presented as one number across a band**; thin slices pooled
only deliberately and DECLARED on the artifact. No gate, no verdict language: these are findings
for the owner's viewing (S4: ad-hoc constructions are findings, never verdicts). GROSS STAYS
GROSS (R107.7): no replacement subtraction anywhere in these three riders.

## FENCE (derived from the job list; commit the derivation with the PLAN)
IN: `session_2026-07-18/riders_i_iii/` (all outputs live here) + analysis scripts committed INSIDE
that session dir. HARD-OUT: the store · ALL engine code (`rl_model.py`, `_merged_recover.py`,
`s4_matrix_7147.py`, everything) · `pvc_curve_v2.json` as a write (read-only input) · `docs/`
(builds never author docs) · the five-migration build's branch and files (disjoint by
construction). If a job mechanically requires touching a HARD-OUT file, HALT and return the
conflict. Mid-flight scope growth ⇒ new directive, new chat (S2).

## STANDING RULES
S1–S6 operative. SILENCE IS A RED: every check prints a verdict or HALTs; exit codes propagate;
no result read through `tail`/`head` without its exit checked; backgrounded computes end in an
asserted completion marker, never an assumed one.

## RETURN
≤30 lines + committed artifacts + an "in plain terms" close. ALWAYS: branch · head git SHA · PR
number · actual time vs band · per rider, the single most decision-relevant finding stated in one
plain sentence (a finding, not a verdict). A return without its SHA is incomplete.
