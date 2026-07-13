# ITEM 20 — THE STORE-IDENTITY JOB · RETURN

Branch `claude/store-identity-job-v2-9-kuers3` · base main @ 4234bf5 (v2.9 tag 9f8ae76 canonical).
Trigger verified (ls-remote): `refs/tags/v2.9 → 9f8ae76`, main == bake head + docs. One store-writer.

**Store b0c39d78 → 340a7a32 · Board 81e48293 → 3dc19fbb** (engine ev()/config/band/rl_model UNCHANGED).

Five parts executed to register 20/20a/33:
- (a) BRAMBLE 2026 15g@62.4 → 14g@62.3; career games 91 → 90.
- (b) `afl_club` imported on the 804 from the (now-archived) CSV `legacy_afl_club`; `affl_team` kept.
- (c) `_club` → `_draft_club` store-wide (0 remain); ten enumerated rows draft-backfilled := afl_club.
- (d) id_resolver `_club_match` repointed affl_team → afl_club (docstring fixed); export `club` →
  afl_club (draft-club fallback for retired back rows); CAT_BY_CLUB grouped by `_draft_club`.
- (e) eligibilities K/G-normalized (191) + owner corrections gardiner→K-DEF · whitlock→K-DEF,K-FWD ·
  cooke→K-DEF (spec of record 20a; note the directive body listed two — 20a rules three).
- (f) importer entry-bound assertions (games≤14 · DOB · club∈18 · legal tags) — HALT with row named.
- (g) CSV stamped + moved to docs/inputs/archive/ (store is the sole carrier; SSI clean).
- (h) board/book/UI regenerated + re-pinned; book re-sealed at the post-fix store.

**COMPLETE affected-`v`-row list: session_2026-07-13/store_identity_job/out/AFFECTED_ROWS.md — 1 row.**
The only value mover is `lachlan-bramble 92 → 93 (+1)` (sum 696247→696248); the feared collateral
ripple did NOT appear (his 2024 peak season is untouched, so the calibration moved no one else).
182 club-DISPLAY corrections (172 draft→current + 10 blank-fills) — display-only, 0 `v` impact.
Eligibility before/after table (194 rows): out/ELIGIBILITY_TABLE.md.

Named lines:
- **houston** — afl_club **Collingwood** · _draft_club Port Adelaide · affl_team St Kilda Saints;
  board `club` now shows Collingwood (was Port Adelaide). ✓ owner acceptance.
- **keays** — afl_club Adelaide · _draft_club Brisbane; board shows Adelaide.
- **bramble** — 14g@62.3, career 90; value 92 → 93 (+1, the accepted move).

STRICT-FENCE report: 325 other rows carry a null draft club — ALL retired historical, 0 live, 0 in
CSV; none backfilled (no inference). No live row needed an owner ruling.

Ingestion go-live blocker (d) CLEARED: the id_resolver club-semantics defect is fixed — feed rows
now match on the current AFL club, and the two Max Kings stay separated (distinct afl_club St Kilda
vs Sydney; collision sentry re-pinned to `_draft_club`, green).

GUARDS (fresh bootstrap, all GREEN — stays Tier 2, no escalation):
- Guard 5 boot-store PASS (store 340a7a32 == pin; board 3dc19fbb == pin) · config-manifest + ruling PASS.
- ZERO-EMPTY-CLUB PASS (0 blank across 1002 rows) · export↔engine parity PASS (804/804).
- one_source_selftest PASS (guards 1-3, F1 board==engine, F2 book==board, collision sentry King pair
  clean under `_draft_club`) · Guard-4 correction canary PASS (store restored 340a7a32).
- 3 red-paths ALL PROVEN (presence-assertion HALT · Guard-5 wrong-pin HALT · +the (f) importer HALT).
- Panel 10/10 · ship_gates B1/B2/B3/B4/B6 PASS, reds EXACTLY {A2,A3,A12} (certified owner-known set;
  B1 y4/y5/y6 = 127/125/116; B3 book seal d371a27c matches the re-seal).
- Official July-8 cohort gate PASS: y4 126.8 · y5 125.2 · y6 116.1 (hard 130) — unmoved by bramble +1.

v2.9 tag (9f8ae76) unmoved; this is the next chapter's first store write, no re-tag. Store is now
the SOLE carrier of every club/ID/eligibility (CSV stamped + archived; SSI clean).
