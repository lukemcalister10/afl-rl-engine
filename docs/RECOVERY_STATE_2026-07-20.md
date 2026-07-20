# RECOVERY STATE — v2.11 controlled handover

Date: 2026-07-20 (Australia/Sydney)
Supervisor: ChatGPT
Builder: Claude Code
Owner/final authority: Luke McAlister

---

## STATUS UPDATE — ARTIFACT-RECOVERY HALT SUPERSEDED (2026-07-20, `release/v2.11-rc1`)

The earlier read-only reconciliation ended in a **HALT** (see `RELEASE_ARTIFACT_MAP_v2_11.md` §G):
the intended round-14 board of record `06d8af60` was **not byte-recoverable committed content**, so the
release could not ship the verified artifact from committed bytes alone. **That finding was correct at the
time and is now RESOLVED by new evidence.** It is preserved verbatim below and in the artifact map — nothing
is erased.

Under the owner's **Option 1** ruling (controlled read-only v2.11 release-candidate assembly), the HALT is
lifted by:

1. **Committed exact board bytes.** The full round-14 balanced board of record is now committed in Git as the
   diagnostic cross-host reference fixture — commit `7c6768ee51adc2cf939ffa18f620bbec1d6b4249`, path
   `session_2026-07-20/root_cause_109_wobble/cross_host_gate/fixtures/reference_06d8af60.json`, Git blob
   `e546ab0b1033af2b8e4331e66899d14245ef3b58`. This is exactly the missing-evidence item (§G.1) that lifts the HALT.
2. **Full MD5.** `06d8af60b679a12db07c064c60c065f9` (full length, byte-verified — no longer an 8-char prose prefix).
   Facts confirmed against the accepted reference vector: active players **804**, Σ active `v` **752,427**,
   Harry Sheezel `v` **7,964**.
3. **Accepted clean-runner reproduction.** The FV-provenance suite GREEN1 rebuilds the balanced board
   (`RL_PVC2=1 RL_LEGE=0 RL_LEGF=0`, pinned env, accepted provenance path) and asserts it is byte-identical to
   `06d8af60` with 0 movers vs the reference vector — the reproduction gate the HALT (§G.3) required.
4. **Accepted provenance remediation `df5066a`.** `claude/fv-provenance-fail-closed-fm2gas` head
   `df5066a0106363a6d00a2dbdd0bd2b62f97c36ae` closes the stale-`distribution_pricing.py` import hole that
   caused the `06d8af60 → d7a95e8d` cross-host wobble; Guard 5 now fail-closes on forward-valuation
   checkout/loaded-path drift.

The release candidate `release/v2.11-rc1` (created from `df5066a`) **installs those exact committed bytes** at
`data/rl_build/rl_app_data.json` (it does **not** ship the superseded ACT-2 `270a2c5f`, and does **not** adopt a
freshly generated board — the fresh build is only a reproduction test). The stale engine pins (§D, item 399) are
re-stamped to the already-committed engine source (`engine_head 40f43772 → 904722cd`, `rl_model a5fd3d7d →
cc626d7d`), and the board pin moves `270a2c5f → 06d8af60`, so board provenance and engine provenance are now
coherent (the §D "Guard-5-green but internally incoherent" caveat is closed). No valuation formula, engine data,
player value or ranking changed. Full evidence: `docs/RELEASE_CANDIDATE_v2_11.md`.

Restrictions unchanged: **no merge, tag, release, public deploy, or valuation-math change** is authorised by this
update. The RC is a DRAFT for independent review (head `release/v2.11-rc1`, base
`claude/fv-provenance-fail-closed-fm2gas`).

---

## Immutable checkpoint

- `checkpoint/pre-chatgpt-v2.11`
- SHA: `612d4c058560568b3d4d49ecd785759931885081`
- Policy: never modify or move this branch.

## Recovery branch

- `recovery/v2.11`
- Starting SHA: `612d4c058560568b3d4d49ecd785759931885081`
- All recovery documentation and accepted recovery changes target this branch until the owner rules otherwise.

## Operating model

- ChatGPT is the supervisor: clarify goals, issue bounded directives, independently review GitHub evidence, maintain live governance documentation, and make accept/correct/reject recommendations.
- Claude Code is the builder: implement directives, run builds/tests, commit to dedicated branches, and return evidence.
- The owner approves merges, tags, releases, and material valuation decisions.
- Existing Claude branches and pull requests are not modified, merged, closed, rebased, or retargeted without an explicit recovery ruling.

## Current recovery objective

Recover and release v2.11 without inheriting unsupported claims or restarting model development.

The immediate read-only reconciliation must identify:

1. the exact candidate lineage intended for release;
2. the exact canonical round-14 board artifact and its provenance;
3. which board hash is the shipped artifact, which is a diagnostic configuration, and which is Guard-5-pinned;
4. the minimum boot-integrity correction required for a defensible release;
5. which open PRs are evidence-only, candidate lineage, or post-release work.

No release, tag, merge, or valuation change is authorised by this document.

## Weekly score ingestion

The intended post-release product is a fully local owner workflow requiring no AI or coding during normal weekly use. Supplying one round of scores must validate identities, update the canonical store, regenerate ratings and UI bundles, preserve per-player round-by-round value/rank history, and fail without partial writes.

PR #125 is treated as a candidate backend component only. It is not accepted as the completed weekly updater until transaction safety, stale-preview protection, UI refresh, round-history persistence, and sequential multi-round proof are independently verified.

## Next permissible action

Complete the read-only release/artifact map. Do not modify code or release artifacts until that map is recorded and reviewed with the owner.
