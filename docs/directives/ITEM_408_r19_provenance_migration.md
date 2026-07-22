# BUILD DIRECTIVE — ITEM 408 · R14→R19 PROVENANCE MIGRATION (owner-scoped release)
Issued: 2026-07-22 · supervisor pen (Fable) · owner words recorded below · execute VERBATIM.
Build seat: **GPT Sol 5.6** (may drive Claude Code / Codex as hands INSIDE this seat; one writer
at a time; disjoint files only; Sol signs the claims note — nobody else).
Blind review seat: a model that is neither Sol nor Fable, cold, review-only, never merges.

## Owner rulings of record (Luke, in chat, 2026-07-22)
- **R1 = C.** The pick curve is a FROZEN RULER. Do NOT rebuild it, its per_entrant pool, or the
  release contract. Re-scope the `one_source_selftest` STAMP guard to assert the curve's TRUE
  provenance triple — `stamp.store_md5 == contract curve_source_store_md5 (968de0c7)` AND
  `stamp.per_entrant_md5 == 40d7da7c` AND contract file untouched — HALT-not-warn. "Re-derivation
  due" (live store ≠ curve source store) moves to: (a) a register note under this item naming the
  queued RL_PVCFIT true re-adoption as its own future owner release, and (b) a BAKE_CHECKLIST.md
  line ("at every store bake: answer the curve question — re-derive or re-affirm frozen").
- **R2 = REGENERATE + ADVANCE-REPIN.** The balanced/strict board is a DERIVED artifact and tracks
  the ONE store. Regenerate it at R19 (expected ≈ 1373e824 / sumv 760253 / sheezel 9542 / 723
  movers vs 06d8af60 — verify, do not assume). Owner VIEWS before any pin moves (see STOP-1).
  Then design out the weekly re-alarm: the round-advance step must regenerate the balanced board +
  FV reference vector and move their pins IN THE SAME COMMIT as the store advance (scripted,
  build-and-compare); the club-curve test stops hardcoding historical board ids and asserts the
  ingest output against the manifest of record (data/expected_boot.json) — still fail-closed on
  any mismatch, tracking advances automatically.
- **R3 = BASED.** Cut ONE branch `ci/r19-provenance-migration` FROM
  `origin/ci/harness-migration-r19-phase2-cand` tip **83ed3bb** (the Kako fix rides in the
  lineage; no standalone Kako merge). Everything merges once, green, at the end.

## Fences (absolute)
- Owner-only, out of this seat's hands: rulebook edits · tags/releases · arming the score-write ·
  any pin bake past STOP-1 without the owner's word.
- Build-and-compare ONLY: never edit an expectation to match without rebuilding the artifact
  behind it and reconciling the numbers in the claims note.
- One store/engine writer at a time. Sol writes ONLY on `ci/r19-provenance-migration`. No pushes
  to main. Whoever builds never reviews.
- Frozen — must NOT rebuild: `engine/rl_after/pvc_curve_v2.json` (curve 89c14729) · the committed
  per_entrant (40d7da7c) · `ui/release_pick_curve.json` · the board of record 6f07f7cb · the store.
- Provenance-tag every claim in the claims note: [owner-seen] / [re-runnable] / [report-only].
  Prior seats' figures (including this directive's) are hypotheses — re-run before building on them.

## Ordered work
1. **DIAGNOSE FIRST (no edits).** Run all four suites end-to-end at the branch base — Final
   Integration, FV Provenance (full time budget; the 2026-07-20 run timed out mid-suite), CI
   Guards, Live Scoring (full scratch bootstrap). Record the complete measured red list. Live
   Scoring's cause is UNVERIFIED — its proofs pin relative identities, so "R14 staleness" is a
   hypothesis to test, not a fact.
2. **RESTORE THE NEGATIVE CONTROLS (priority 1).** In `ui/tests/club_curve_provenance.test.py`:
   CASE3b tampers contract key `store_md5`, which the resolver no longer reads — re-aim at
   `curve_source_store_md5` (valid-hex, wrong value → curve-store-binding halt). CASE5a/5b tamper
   contract `as_of_round`, also unread — re-aim at the live round enforcement (board-stamp
   asOfRound vs expected_boot mismatch; and missing `as_of_round` in the boot manifest →
   manifest-incomplete halt). PROVE each control returns rc=2 via a live halt naming the real
   failure. Then sweep `ui/tools/ingest_inputs.py` for every fail-closed key that has NO tamper
   case and add coverage (release_version, pathway, curve md5s, pin1, board id/store/round).
3. **R1 implementation** per the ruling above. Confirm the STAMP check is NOT one of the five SSI
   guards (it is a later self-test check, introduced 2e49963) and say so in the claims note; the
   re-scope keeps HALT-not-warn on the true invariant.
4. **R2 implementation — STOP-1 lives here.** Regenerate the balanced board + full value vector
   at R19. Produce for the owner: board_diff vs 06d8af60 AND vs 6f07f7cb, sumv/sheezel deltas,
   mover count. **STOP: owner views and gives his word.** Only then, ONE commit moves every pin:
   `data/expected_boot.json` (balanced_board_md5 + panel note) · `data/release_contract.json`
   (identities + present_lens_baseline + contract re-seal via its own tool) · FV
   `BOARD_MD5_GOOD` + aggregates + regenerated `reference_vector_*.json` · board bundle regen via
   `ui/tools/extract_board_view.py`. This is the ONLY board-artifact write in the job and the
   riskiest step — a missed pin here is a silent cross-environment mover.
5. **Advance-repin design** (R2 second half): script the sibling regeneration into the
   round-advance path; re-aim club-curve CASE1 at the manifest of record by build-and-compare.
6. **Live Scoring** — fix per step-1 diagnosis; build-and-compare any pinned proof outputs.
7. **CLOSE.** All four suites green from a fresh bootstrap, ZERO waivers. Numbered claims note on
   the branch (`docs/directives/ITEM_408_claims_note.md`), every pinned expectation traceable to
   an R19 build-and-compare. Run `tools/seat/prescreen.sh`. Hand to blind review. After review:
   **STOP-2 — owner views board + book, then his word to merge.** No tag, no score-arm, in scope.

## Acceptance
Four suites green, zero waivers · fail-closed controls proven firing on the REAL keys · frozen
artifacts byte-untouched · STOP-1 and STOP-2 owner words recorded in the claims note · blind
review filed by a third seat.
