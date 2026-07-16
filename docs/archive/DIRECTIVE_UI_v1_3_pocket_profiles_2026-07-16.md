# DIRECTIVE — UI v1.3: CLUB POCKET-PROFILES + POSITIONAL BREAKDOWN · 2026-07-16 · seat 9 (Fable)
### Tier 3 (S3 parallel; never touches the Leg-B ladder). Scope = register item 196, APPROVED at
### item 197(2). Owner-viewed then merged on HIS click. Fresh disposable Claude Code chat (Opus).

## EFFORT: Medium
Why not lower: two new render surfaces + a counting rule carrying an exception; league-average
denominators need care. Why not higher: display-only — no pricing, no ingest change; the v1.2
patterns (panel/hover/summary) are established and reused.

## MODE: auto — first committed artifact is the PLAN (brief: surfaces, counting-rule tests, files)

## TIME: 2–3 hours wall-clock (confirm up front; flag >2× / <½×; report actual)

## FEED
1. This directive. 2. `ui/README.md` + `ui/HOW_TO_UPDATE_INPUTS.md` + the v1.2 PLAN files (house
patterns). 3. The shipped bundles in `ui/data/` — THE ONLY VALUE SOURCE. 4. Register item 196 verbatim
(quoted in THE JOB below — no other scope source).

## BASE PIN
Branch from `main`: `git ls-remote https://github.com/lukemcalister10/afl-rl-engine main` — AT OR
AFTER `21d94a4`, and `git diff --name-only 21d94a4..main` must be `docs/`-ONLY (the pen moves main;
the Leg-B writer merges only at the chapter bake, never mid-flight). Any ui/ or engine/ file in that
diff ⇒ HALT-AND-ASK.

## RING-FENCE PIN (assert in code and in the return)
`ui/config.js EXPECTED_BOARD == 790136a3` — values come from the SHIPPED board's bundles, never a
candidate, never the owner's sheet. The Leg-B candidate does not exist for this job.

## THE JOB (item 196 verbatim-in-substance; display-only)
1. **Club hover pocket-profile:** on hover (and tap on touch) of a club anywhere it renders ranked, a
   pocket panel: **overall / player / picks / top-5 / top-10 / Best-23 / non-Best-23** — EACH shown
   three ways: absolute · % of the club's overall · vs league average. Best-23 = the existing exact
   greedy (reuse, don't reimplement).
2. **Positional value breakdown per club:** per current position — absolute · % of the club's PLAYER
   value · vs league average — positions from the locations CSV's `Position/s` column via the
   ESTABLISHED name→ID join (HALT on ambiguity; the two Max Kings are distinct). **THE OWNER'S
   COUNTING RULE, VERBATIM-IN-SUBSTANCE: each player counts 1 to his position; a DPP player counts
   0.5 to each; EXCEPT DPP midfielders — the non-mid position counts 1 and the midfield component
   counts 0.** Commit unit tests for the rule incl. the DPP-mid exception.
3. **League average = the mean over the 16 ranked clubs; the Free Agents pool is EXCLUDED from every
   denominator and never ranked** (item 191's structure). State this on the panel (small footnote) so
   the owner sees the construction at viewing.
4. **DEFERRED-FLAGGED, NOT BUILT:** lens-awareness (posture re-render + ±1/±2) — the post-Leg-E pass
   (item 196(3)). Leave the flags where v1.2 left them.

## DELIVERABLES
- Branch + PR; per-task commits; PLAN first.
- `ui/screenshots/v1_3/` — the pocket-profile open on two clubs + the positional breakdown on two
  clubs (one containing a DPP-mid case), before/after where a surface changed.
- Committed verdicts file (the v1.2 pattern): ring-fence pin asserted · counting-rule tests pass ·
  bundle byte-match (`ui/data/` untouched — md5s printed) · fence 100% ui/.
- RETURN ≤30 lines + plain-terms close: branch · head SHA · PR number · actual time.

## FENCE
IN: `ui/app`, `ui/styles`, `ui/screenshots/v1_3/`, ui unit tests, the PLAN file.
OUT (HALT if needed): `ui/data/` bundles · `ui/tools/ingest_inputs.py` · `ui/config.js` beyond
reading the pin · engine/ · docs/ · any pricing, rounding, or Best-23 algorithm change · anything
lens-related beyond the existing deferred flags. Mid-flight scope growth = a NEW directive (S2).
