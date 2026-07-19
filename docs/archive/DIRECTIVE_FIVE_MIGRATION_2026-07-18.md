# DIRECTIVE — THE FIVE-MIGRATION (Leg D, pre-ladder build) · seat 13 · 2026-07-18
### Ruled R107.5 (DECISIONS v123) · released item 328 · authored by seat 13 (item 330).
### Job: migrate the five `rl_model.py` MA.PVC consumers off the frozen v3.4 curve onto
### `pvc_curve_v2`, ONE CONSUMER AT A TIME, per-consumer before/after proofs. Engine-code only.

## BASE PIN (engine base ⇒ STRICT equality; run first, HALT on mismatch)
`git ls-remote https://github.com/lukemcalister10/afl-rl-engine.git claude/legd-pvc-rederivation-act2-l2hqpl`
must return exactly `e4177c21934148c19d9cec3c015fee5d28480102`. Branch from that head (stacked on
PR #109 ← PR #105). Entry assertions before any edit: boot-store guard (store md5 `968de0c7`) ·
curve artifact present with **payload stamp `89c14729`** (file md5 `56dd7a7b` — a KAT names WHAT it
hashes) · `RL_PVC2=0` ⇒ board `9829d01a` byte-exact (entry re-proof; it is twice-proven on this line).

## EFFORT: High
Why not Medium: five value-moving consumer sites plus a trained-model dependency (train/serve skew);
thin proofs here are exactly the item-322 failure class. Why not Extra: the construction is complete
and cold-audited; this is mechanical wiring against a fixed MAP OF RECORD with per-step proofs.

## MODE: auto — the first committed artifact is the PLAN (which must contain the derived fence; see FENCE).

## TIME: one chat, ~2–4 h wall. Confirm the band up front; flag >2×/<½×; report actual in the return.

## FEED (fetch from the repo/branch — documents, never prose restatements)
DECISIONS v123 (R107.3/.4/.5 context; R107.5 is this job's ruling) · CONSTRAINTS v1.19 +
`acceptance_v1_21.json` (assert the JSON) · SPEC_PVC_FLEX_CHAPTER v1.4 §1+§1b · SSI v1.3 ·
HANDOVER rev159 §2 ACT 1 · **THE MAP OF RECORD: `session_2026-07-17/legd_derivation/SITE_CENSUS.md`
@ `e4177c2`** — sites named from the code with line numbers. Any prose list, INCLUDING THE ONE BELOW,
is a paraphrase; the census wins on any disagreement.

## THE JOB LIST (ordered; per-consumer commits; census wins)
0. ENTRY: base-pin + entry assertions above. Commit the PLAN (job→file map + the mechanically
   derived fence + the proof template).
1. **MEASURE FIRST — `pvc_snapshot` → peak-model (census `rl_model.py:515,:530`, `_V4PVC`).** The
   peak model was TRAINED on the old snapshot; the census marks it "must NOT track live PVC —
   train/serve skew." Quantify, with a committed measurement, what migrating this feature would do
   to peak-model inputs/outputs. If it needs retraining: DO NOT retrain — the consumer HOLDS frozen,
   the retrain is recorded as the POST-BAKE FALLBACK (R107.5), and the measurement justifying the
   hold is committed. Migrate it only if the committed numbers show no retrain is needed (the
   memo-C rule: fallback/hold only on committed measurement, never on assumption).
2.–5. **The remaining four consumers, ONE AT A TIME, one commit each** (census §E / halt-flag list):
   the `build_pvc_v34` import-time fit + `CURVE_H` + `BOARD_FACTOR` pin + `_deplateau`
   (`rl_model.py:714,:716,:720-722,:726-737`) · pickless `unpl_eq` (`:798`) · the pedestal (`:813`) ·
   the `_natcv34` inversion base (`:834-853`). Design constraint (census verdict + PART 7): the new
   path is OFFLINE + LOADED under **`RL_PVC2`** (the `RL_PVCADOPT`/L1b template) — **no new
   import-time fit**; `RL_PVC2=0` leaves the v3.4 import-fit path byte-exact. Sequencing of 2–5 is
   the PLAN's to fix from the census's dependency order.
6. **RIDER (report-only, items 326/327):** emit the engine-side R inputs (the free-intake
   pick-equivalents) as a committed report. No engine value change; not a gate.
7. EXIT: full FROZEN repo suite (S4) · five SSI guards green · **`RL_PVC2=0` ⇒ `9829d01a`
   byte-exact (third proof)** · store md5 still `968de0c7` · gates snapshot committed
   (`tools/seat/gates_score.py`) · candidate PR raised.

## PER-CONSUMER PROOFS (each of jobs 1–5 carries all of these in its commit)
(a) BEFORE/AFTER board hashes at `RL_PVC2=1` and the affected-row diff artifact
(`tools/seat/board_diff.py`), rows NAMED — counts are not behaviours (item 293). (b) the
byte-hold proof: `RL_PVC2=0` board unchanged after the commit. (c) a one-line WHY for every
moved row class. A consumer whose migration moves nothing proves the null (hash-equal, stated).

## FENCE (the item-322 law: DERIVED MECHANICALLY FROM the job list — never parallel-maintained)
The PLAN derives the fence as: the union of files the jobs above name — expected
`rl_model.py` + the session proof directory (`session_2026-07-18/five_migration/`) + any conduit
file a job MECHANICALLY requires to carry the loaded curve to `MA.PVC` (the census names
`_merged_recover.py:1336-1342` as the load template) — commit the derivation with the plan.
HARD-OUT regardless of derivation: the store `engine/rl_after/rl_model_data.json` (md5 `968de0c7`
untouched) · `pvc_curve_v2.json` as a WRITE (read-only input) · the V0/`_iso_dec` instrument chain
(`_merged_recover.py:1121-1171` — the G-Y0 gate input; census §D) · `s4_matrix_7147.py:62` anchor ·
SEASON_PROG (`rl_model.py:738`, owner dial, stays 0.58) · `docs/` (builds never author docs).
If a job mechanically requires a HARD-OUT file, HALT and return the conflict — fence extension is a
checkpoint question, never a build's call. Mid-flight scope growth ⇒ new directive, new chat (S2).

## STANDING RULES
SPEED RULES S1–S6 operative. S4 boilerplate: gates and guards are measured with the FROZEN repo
suite only; ad-hoc constructions are FINDINGS to report, never verdicts to act on. SILENCE IS A
RED: every check prints a verdict or HALTs; exit codes propagate; nothing piped past `tail`/`head`
without its exit checked.

## RETURN
≤30 lines + committed artifacts + an "in plain terms" close. ALWAYS: branch · head git SHA · PR
number · actual time vs band · the three narrowest margins observed. A return without its SHA is
incomplete.
