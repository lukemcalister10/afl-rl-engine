# ITEM 408 — R19 provenance migration claims note

- **Supervising build seat / sole signer:** GPT Sol 5.6
- **Mechanical builder (repository hands only):** Claude Code — no interpretive or sign-off authority
- **Owner / sole STOP-1 and merge authority:** Luke McAlister
- **Branch:** `ci/r19-provenance-migration`
- **Exact rebuild base:** `83ed3bb1606b708af16a2ad90a26d63553de6789`
  (`origin/ci/harness-migration-r19-phase2-cand` tip — "harness(one-source): refresh Kako 2026 pin to 10 games @ 45.4")

---

## Owner ruling of record — ITEM 408 Items 6–7 (Option A), 2026-07-23

`[owner-seen]` **Owner ruling (Option A), verbatim, relayed by GPT Sol 5.6:**

> The authorised Round 15–19 recovery counts as genuine production Movers history. Retain the R15–R19
> production Movers reports. Do not reset the production Movers bundle to empty. Preserve the historical
> reports and implement a fail-closed provenance bridge to the current accepted release identity. No
> historical report may be silently rewritten.

This ruling **supersedes the item-6 builder conclusion that `ui/data/movers.js` must ship empty** (the
Category 1 "unauthorised materialisation regression" verdict of §7.8, now **WITHDRAWN** — see §7.8 and
§9). The R15–R19 production Movers bundle is **restored populated** and displayed under the current
accepted release via a **separately-declared, owner-approved, fail-closed provenance transition**
(`data/release_lineage.json` `release_transition`, mirrored to `ui/data/movers_transition.js`, enforced
by `ui/app/movers.js core`). It is recorded in full in **§9** (the item-6 correction) and closed in **§7**.

It does **not** authorise: a new score application; rewriting historical movements; altering the
protected R19 store, board, ledger, histories or per-round movers reports; merging, tagging, releasing
or deploying; or granting STOP-2. The shipped score-write gate stays **OFF**; STOP-2 remains
exclusively owner-held and pending. (Working branch of record for this correction:
`claude/item-408-fixture-repair-e2o53i` — see the push-target deviation in §7.0.)

## Evidence classes

Every factual claim below is tagged exactly one of `[owner-seen]`, `[re-runnable]`, or `[report-only]`,
per the directive. Prior seats' figures — including the directive's own hypotheses — are re-run before any
build depends on them. This note does not assert final four-suite acceptance; the suites are not yet all green.
STOP-1 has been approved and executed; STOP-2 remains pending.

---

## 0. Rebuild governance — v382 ruling and the strike boundary

1. `[report-only]` **v382 ruling acknowledged.** CI may **run and report only**. CI must never reconstruct
   patches, decode payloads, create files, commit, push, move refs, or publish repository changes. No
   workflow may be created or modified for write purposes. This claims note and the rebuilt branch are
   authored by the mechanical build seat locally (git hands), **not** by any CI workflow.
2. `[report-only]` **In-flight exception (not a strike).** Two applier-tagged commits landed after the v382
   ruling was issued but before GPT Sol 5.6 acknowledged it. Per the ruling they are classified **in-flight**
   and are **not** a strike. In the discarded history the two latest applier-tagged (`[item408-apply]`) writes
   were `20dc36e` (2026-07-23 01:27:25 +1000) and `dc0b2a7` (2026-07-23 01:33:10 +1000). (The exact
   issuance-vs-acknowledgment wall-clock is supervisor-held; this builder records the ruling's classification,
   not an independent timing determination.)
3. `[report-only]` **Strike boundary now active.** As of GPT Sol 5.6's acknowledgment of v382, **any
   CI-authored repository write is a governance violation.** The next push to `ci/r19-provenance-migration`
   is the completed rebuilt branch only; no intermediate commits are pushed individually.
4. `[re-runnable]` **Force-rebuild reason.** The pre-rebuild branch carried a 32-commit transport/application
   history (encoded patch fragments `stage … part 00–05`, standalone/atomic appliers, observer and
   failure-capture workflows, a write-enabled `item408-stop1-candidate` CI job, `[item408-apply]`/`[item408-stop1]`
   trigger commits, a `TRIGGER.md`, edits to `docs/OPEN_ITEMS_REGISTER.md`, and placeholder one-line logs).
   31 of its 32 commits were authored under the owner identity `lukemcalister10 <lukemcalister10@gmail.com>`.
   It is discarded and rebuilt as four plain, seat-authored commits carrying only the legitimate additive
   substance, with the workflow and register left byte-identical to the base.
5. `[re-runnable]` **Discarded pre-rebuild remote tip:** `ab2405aa606d536ae345607ae470781c03da1bf5`
   (the force-with-lease expected value; the branch is force-pushed only against this exact tip).
6. `[re-runnable]` **Builder identity.** Every rebuilt commit is authored and committed as
   `build-seat-claude-code <build@seam.local>`. No commit is authored or committed as Luke McAlister,
   lukemcalister10, the owner, "Claude", or a GitHub Actions identity.
7. `[report-only]` **Roles.** Claude Code is the mechanical builder only. GPT Sol 5.6 remains the supervising
   build seat and the **sole signer** of this claims note. The owner remains the sole authority for STOP-1,
   pin/board/release movement, merges, tags, releases, deployment, and score-write activation.

---

## 1. Execution controls and exclusions

1. `[report-only]` **Prior PR-lane reds are excluded from the measured base red list.** GitHub Actions checked
   out a **synthetic PR merge ref** (`refs/remotes/pull/<n>/merge`) — the moving PR base merged with the head —
   rather than the exact untouched branch head. Their red/cancelled conclusions are **not** exact-head evidence;
   they evidence only that the PR lane was unsuitable for step-1 diagnosis.
2. `[re-runnable]` **Exact-head diagnosis requires a branch push run (or a local checkout whose `HEAD` is the
   named branch commit), never a `pull/<n>/merge` ref.**

---

## 2. Exact-head base diagnosis (measured red list)

`[owner-seen]` Source of record: `session_2026-07-22/item_408_exact_head/base_diagnosis.json`
(schema `item-408-exact-head-diagnosis-v1`) and its rendered `BASE_DIAGNOSIS.md`. All four runs are `event=push`
on `head_sha=a0df29c6ebf911a31cb517294786593c5000c0f6` on branch `ci/r19-provenance-migration`; the
`pull_request` event lane is explicitly excluded.

| Suite | Conclusion | Run | Failing step |
|---|---|---|---|
| CI Guards | **failure** | [29930019510](https://github.com/lukemcalister10/afl-rl-engine/actions/runs/29930019510) | step 9 — Guards 1/2/3/5 + F1/F2 parity (`one_source_selftest.py`) |
| FV Provenance | **failure** | [29930019626](https://github.com/lukemcalister10/afl-rl-engine/actions/runs/29930019626) | step 9 — FV provenance red/green suite (strict board 06d8af60 + fail-closed red paths) |
| Final Integration | **failure** | [29930019442](https://github.com/lukemcalister10/afl-rl-engine/actions/runs/29930019442) | step 11 — Season-state derivation, wiring, behaviour, stale rejection + FENCED reads halt (req 1/2/4/5/7) |
| Live Scoring Updater | **failure** | [29930019353](https://github.com/lukemcalister10/afl-rl-engine/actions/runs/29930019353) | step 12 — Sequential two-round proof (R15→R16, history integrity, restart, UI, no-prod-touch) |

Notes:
- `[report-only]` The per-run step-log downloads returned HTTP 401 (`LOG DOWNLOAD ERROR`), so the four
  placeholder one-line `*.log` files carried no genuine evidence and are **dropped** from the rebuild. The
  structured run/job/step metadata above (run ids, job ids, conclusions, named failing steps) is the retained
  genuine exact-head evidence.
- `[re-runnable]` Live Scoring's root cause remains **unverified** — its proofs pin relative identities, so
  "R14/R19 staleness" is a hypothesis to test at implementation time, not an established fact.
- `[re-runnable]` The store in the base checkout is at **`as_of_round = 19`** while `expected_boot.json`
  `balanced_board_md5` is still pinned at the historical strict board `06d8af60…`. The FV Provenance red is
  consistent with the balanced board rebuilt from the R19 store no longer matching that pin — the pin move is
  STOP-1-governed (section 5), not performed here.

---

## 3. R1 frozen-ruler STAMP re-scope

`[re-runnable]` **Owner ruling R1 = C implemented.** The later Leg-D STAMP assertion in
`engine/rl_after/one_source_selftest.py` no longer compares the frozen curve's `stamp.store_md5` to the current
weekly **live** store (`md5(rl_model_data.json)[:8]`). At R19 the live store is `f37d9716`, which no longer
equals the frozen source store `968de0c7`; the old assertion would re-alarm on every weekly store advance even
though the pick curve is a **frozen ruler**. The re-scope asserts the curve's **true immutable provenance**
instead (HALT-not-warn):

1. `ui/release_pick_curve.json` exists and is parseable;
2. the contract is byte-untouched — `md5 == 676ad2b77612a4fbd4df3362b6f88fab`;
3. the contract's `curve_source_store_md5 == 968de0c7a0183ca3914165536f39607a`;
4. `pvc_curve_v2.json` `stamp.store_md5 == contract.curve_source_store_md5[:8]` (the stamp's stored 8-char form
   → `968de0c7`);
5. `pvc_curve_v2.json` `stamp.per_entrant_md5 == 40d7da7c`;
6. the curve file bytes match the contract's `pick_curve_file_md5` (`md5(pvc_curve_v2.json) == 56dd7a7b…`);
7. (additive) the curve payload `curve_md5 == contract.pick_curve_curve_md5` (`89c14729`).

`[re-runnable]` **Validated against the real frozen artifacts** (pinned venv 3.12.3): the block returns all-PASS
with a `0` verdict on the untouched tree, and each independent tamper — contract bytes, contract
`curve_source_store_md5`, stamp `store_md5`, stamp `per_entrant_md5` — flips a check and drives the self-test's
`sys.exit(1)` (`one_source_selftest.py` line 380: `sys.exit(1 if FAIL else 0)`), preserving HALT-not-warn. The
full `one_source_selftest.py` additionally needs a board bootstrap + vendored `unidecode` to reach this block;
that bootstrap is identical at base and post-rebuild, so the STAMP re-scope is the only behavioural change.

`[re-runnable]` **Git-history verification — DISCREPANCY REPORTED.** The directive states this STAMP assertion
"was introduced at commit `2e49963`". **`2e49963` does not exist in this repository** (`git cat-file -t` → "Not
a valid object name"; unreachable from any ref). By `git log -S"_boot_store"` and `git blame` it was introduced
at commit **`15a9abd`** ("leg F5: §2.viii ENTRANT LAYER + §2.x CONSERVATION GATE (MEMO_LEGF v1.3)",
2026-07-19), an ancestor of base `83ed3bb`. Recorded as a discrepancy for supervisor adjudication.

`[re-runnable]` **Confirmed NOT one of the five SSI guards.** GUARD 1/2/3/4/5 are defined at lines ~40–79
(GUARD 4 runs separately). The STAMP assertion sits inside the later `if _pvc2_on:` Leg-D block (file comment
line ~328: "The one instrument for the Leg-D curve … HALT-not-warn: any FAIL -> sys.exit(1)"). It is a later
Leg-D self-test check, as the ruling requires.

`[re-runnable]` **GPT Sol review finding 5 applied:** the R1 comment "\"re-derivation due\" in the
register/checklist" is corrected to "\"re-derivation due\" in the claims note/checklist" — comment-only; the
register (`docs/OPEN_ITEMS_REGISTER.md`) remains byte-identical to `83ed3bb`.

`[re-runnable]` **`BAKE_CHECKLIST.md`** receives one narrow additive binding rule: every future store bake must
explicitly answer the curve question — re-derive and re-adopt the ruler under separate owner release authority,
or expressly re-affirm the frozen ruler and its original provenance (`968de0c7` / `40d7da7c`, byte-bound to
`ui/release_pick_curve.json`). No other checklist step changes.

`[report-only]` **True `RL_PVCFIT` re-adoption remains a future, separate owner release and is NOT performed by
ITEM 408.** "Re-derivation due" (live store ≠ frozen curve source store) is a lifecycle note, not curve
corruption. Per the directive it lives in **this claims note** (and the BAKE_CHECKLIST rule), **not** in
`docs/OPEN_ITEMS_REGISTER.md` — the register is the supervisor's pen and is left byte-identical to `83ed3bb`.

## 4. Negative controls and the resolver blind review

### 4.a BLIND REVIEW REQUIRED — `ui/tools/ingest_inputs.py`

`[re-runnable]` **No production resolver change is required; `ui/tools/ingest_inputs.py` is left byte-identical
to `83ed3bb`** (md5 `c743e097833963c4551d7efcd9fad7c050219ccf1af2c404df89c8493ba88853`). The discarded branch's
12-line delta (7 add / 5 del) in `resolve_release_curve()` was comment + diagnostic-string wording only: the
functional line `cs_ok = curve_store[:8] == str(contract["curve_source_store_md5"])[:8]` is unchanged context;
the base already compared the curve stamp against the contract's frozen `curve_source_store_md5`. Verified live
below (CASE3b). No guard weakened, nothing added.

### 4.b Fail-closed controls — every case proves its SPECIFIC live guard

`[re-runnable]` Controls live in `ui/tests/club_curve_provenance.test.py`; each invokes the **real production
resolver** as a subprocess with `RL_UI_*` overrides into a scratch dir (production `club_valuation.js` never
overwritten; production board/contract/boot/curve never mutated). Following GPT Sol review finding 1, **every**
negative case (not only the restored ones) now asserts the exact live HALT reason via `halt_names(...)`, so a
control cannot pass on a bare `halt` object or because an unrelated earlier guard fired.

**Measured result (pinned venv 3.12.3): 35 checks, 33 pass.** The **18 fail-closed controls all pass**, each
`rc=2` with its guard-specific reason:

| Case | Tamper (scratch-only) | Guard reached | Live reason excerpt |
|---|---|---|---|
| CASE2a | contract points RL_PVC2 pathway at `pvc_curve_L1b.json` | resolve: name/pathway | `adopted_pathway RL_PVC2 must load pvc_curve_v2.json but … points at pvc_curve_L1b.json` |
| CASE2b | board PVC = L1b curve under RL_PVC2 contract | assert_pvc: byte-match | `STALE-CURVE GUARD: the board's PVC does not byte-match …` |
| CASE3a | contract `adopted_pathway = RL_BOGUS` | contract: known-pathway | `UNKNOWN curve-selection: adopted_pathway 'RL_BOGUS' is not a known pathway` |
| CASE3b | contract `curve_source_store_md5 = deadbeef…` | resolve: store binding | `pvc_curve_v2.json binds store 968de0c7 != release store deadbeef` |
| CASE3c | missing contract file | `_read_json` | `release pick-curve contract missing: …` |
| CASE3d | temp engine curve, file bytes drift (values intact) | resolve: file-md5 | `CURVE DRIFT: pvc_curve_v2.json md5 … != contract … — the engine curve file changed` |
| CASE4 | board stamp `board = aaaa…` | load_board: board-id ring fence | `board id mismatch — bundle aaaaaaaa != current release board 6f07f7cb (regenerate board_view)` |
| CASE5a | board stamp `asOfRound = R18` (≠ R19) | load_board: round | `board round mismatch — bundle R18 != current release R19` |
| CASE5b | temp expected_boot with `as_of_round` removed | `_release_manifest` | `release manifest lacks current weekly identity fields: ['as_of_round']` |
| CASE7 | contract `release_version` | contract: version | `contract release_version v0-tampered != release v2.11-final-rc1-PROVISIONAL` |
| CASE7 | contract `pick_curve_curve_md5` | resolve: curve-md5 | `CURVE DRIFT: pvc_curve_v2.json curve_md5 89c14729 != contract deadbeef` |
| CASE7 | contract `numeraire_pin1 = 2999` | contract: pin1 | `contract numeraire pin1 != 3000 — numeraire drift` |
| CASE7 | board stamp `store_md5`/`store` | load_board: store | `board store mismatch — bundle bbbbbbbb != current release store f37d9716` |
| CASE7 | contract missing `adopted_pathway` | contract: completeness | `release pick-curve contract is incomplete (missing ['adopted_pathway'])` |
| CASE8 | temp curve gate token → `RL_PVCADOPT` (file-md5 re-tracked) | resolve: gate/pathway | `pvc_curve_v2.json self-declares gate 'RL_PVCADOPT' != adopted pathway 'RL_PVC2'` |
| CASE9 | temp curve top-level `pin = 2999` (file-md5 re-tracked) | resolve: engine-curve numeraire | `release-active curve pvc_curve_v2.json pin != 3000 — numeraire drift` |
| CASE10 | temp curve + board PVC both `pick1 = 2999` (byte-match cleared) | assert_pvc: pick-1 | `PVC pick1 != 3000 — numeraire drift` |
| CASE11 | temp curve + board PVC both lift pick 60 > pick 59 (byte-match + pick1 cleared) | assert_pvc: monotone | `PVC is not monotone non-increasing — not a valid pick ruler` |

`[re-runnable]` **Finding-2 sweep completeness.** CASE8–CASE11 reach the four previously unswept production
guards. Each uses a temp engine dir + temp contract via `temp_curve_and_contract()`, which re-tracks
`pick_curve_file_md5` to the mutated file and keeps `pick_curve_curve_md5` mutually equal to the curve's own
field, so the tamper clears the earlier name/file-md5/curve-md5 guards and the intended guard is the one that
fires. CASE10/CASE11 additionally byte-match the temp board PVC to the temp engine curve so the assert_pvc
byte-match (and, for CASE11, pick-1) guards clear first. `ui/tools/ingest_inputs.py` is not changed.

`[re-runnable]` **Restoration proof (unchanged from prior review):** the base test file against the base
resolver = 21/26, with CASE3b/5a/5b dead (`rc=0`, tampering keys the corrected resolver no longer reads). The
rebuilt controls fire live against the byte-identical resolver.

`[report-only]` **Negative-control result reported separately from CASE1 (finding 2).** All 18 fail-closed
controls pass. The only two failing checks are **CASE1 positive-path** assertions that hardcode the historical
R14 board id `2ab73a6f` and `asOfRound 14`; the base store is at **R19**, so both fail identically at base and
post-rebuild. They are the CI-Guards / club-curve red of section 2. At the pre-STOP-1 measurement point,
`expected_boot.json` was still pinned to `06d8af60`, so re-aiming CASE1 was correctly outside the pre-STOP-1
rebuild scope. STOP-1 has since advanced the balanced-board pin to `1373e824` in commit
`348d0ff715d1a98f0ebc47d2a9cc2d32efde0d80`. Re-aiming CASE1 remains directive item 5 and has not been performed.

## 5. R19 balanced-board regeneration and STOP-1

`[re-runnable]` **Candidate regenerated afresh** from the exact accepted R19 store + current engine/config, via
`session_2026-07-22/item408_stop1/build_stop1_candidate.py`, which drives the existing disposable FV builder
(`test_fv_provenance.py::_run_build`, `balanced=True`) in a throwaway staging copy. The candidate hash is
**derived dynamically** (`md5(candidate board)`), never asserted to a pinned answer. The evidence script is
scratch-only and writes only under `session_2026-07-22/item408_stop1/`.

`[re-runnable]` **Real fences (GPT Sol review finding 3).** The builder hashes every protected artifact
**before and after** the build, **aborts non-zero** if any changed, and **derives each fence flag from the
measured before/after equality** (never hardcoded). Measured this run — all eight unchanged, so every fence is
`False` **because the hashes prove no mutation**:

| protected artifact | path | before = after md5 |
|---|---|---|
| canonical_board (board of record 6f07f7cb) | `data/rl_build/rl_app_data.json` | `6f07f7cbe042f8e56426a01226c967c9` |
| expected_boot | `data/expected_boot.json` | `f4603e627096ea04a9dbf2b23f0cceff` |
| release_contract | `data/release_contract.json` | `54ec77eb6c8d5a6c451604b034537130` |
| curve_contract | `ui/release_pick_curve.json` | `676ad2b77612a4fbd4df3362b6f88fab` |
| curve | `engine/rl_after/pvc_curve_v2.json` | `56dd7a7bca4306d9224aec0ef52efa32` |
| per_entrant | `…/legd_derivation/out/per_entrant.json` | `40d7da7c7461024048fe48fcba5692ff` |
| store (authoritative) | `engine/rl_after/rl_model_data.json` | `f37d9716648cfe4382b8c6a24c4f064f` |
| score_ledger | `engine/rl_after/ingestion/applied_rounds_ledger.json` | `1d9faae56bc4896a1bf10f9289d45461` |

`[re-runnable]` **Exact input identity recorded (finding 3)** in `STOP1_CANDIDATE.json` / `STOP1_REPORT.md`:
generated at commit `517af20bc019a088ed29d6550bed45eb7e2a6156`; authoritative store `f37d9716`; rl_model
`4f776e07`; forward-valuation identity `6a9a520f…`; distribution-pricing `dd19a234`; config-manifest identity
`45b207c0…`; expected_boot `f4603e62`; release-contract `54ec77eb`; release-pick-curve `676ad2b7`;
reference-vector `6565a4ef`; board-of-record `6f07f7cb`; pinned env py 3.12.3 / numpy 2.4.4 / scipy 1.17.1 /
sklearn 1.8.0 / openpyxl 3.1.5, `PYTHONHASHSEED=0` + single-thread BLAS + `RL_PVC2=1/RL_LEGE=0/RL_LEGF=0`.

`[re-runnable]` **Measured candidate identity** (freshly measured; the directive's prior figures were
hypotheses, all confirmed): candidate board md5 `1373e82471a81064ef96820f3db065df`; active 804; total value
760253; Harry Sheezel 9542.

`[re-runnable]` **Comparison 1 — candidate vs historical balanced board `06d8af60` (the stale pin):** 804 vs
804; sum 760253 vs 752427 (**Δ +7826**); Sheezel 9542 vs 7964 (**Δ +1578**); **723 movers**; 0 added/removed.
Top mover `noah-mraz` 412→2198 (+1786).

`[re-runnable]` **Comparison 2 — candidate vs board of record `6f07f7cb` (frozen; not replaced):** 804 vs 804;
sum 760253 vs 760253 (**Δ 0**); Sheezel 9542 vs 9542 (**Δ 0**); **0 movers**; 0 added/removed.

`[report-only]` **STOP-1 semantics (GPT Sol review finding 4).** Board of record `6f07f7cb` is **frozen** under
the directive and is **not** replaced by this build or by STOP-1. Specifically, in the evidence:
`candidate_vector_equals_board_of_record_vector = true` (the candidate's full active-player value vector equals
the frozen board-of-record vector, 0 movers); `candidate_md5_is_board_of_record_md5 = false` (the candidate
board artifact md5 `1373e824` is a distinct artifact, not the board-of-record md5 `6f07f7cb`);
`stop1_replaces_board_of_record_6f07f7cb = false`. The **STOP-1 decision is whether to approve advancing the
balanced/strict board pin from `06d8af60` to the candidate `1373e824`** and, after the owner's word, moving all
dependent balanced-board / FV / reference identities atomically. This builder moves nothing.

`[re-runnable]` **Deterministic.** Two clean scratch runs at the same checkout produced byte-identical outputs —
candidate board, full 804-row value vector, `STOP1_CANDIDATE.json` (incl. all 723 movers, the input-identity
block, and the measured protected before/after table), and `STOP1_REPORT.md` — md5-for-md5.

## 5.1 STOP-1 APPROVED AND EXECUTED (owner word 2026-07-22)

`[owner-seen]` **Owner STOP-1 word of record (verbatim):** "I approve STOP-1 for ITEM 408. Advance the
balanced/strict board pin from 06d8af60b679a12db07c064c60c065f9 to 1373e82471a81064ef96820f3db065df, and move
all dependent balanced-board, FV aggregate and reference-vector identities atomically. Do not replace board of
record 6f07f7cbe042f8e56426a01226c967c9. No merge, tag, release, deployment or score-write activation is
authorised." Approval relayed by supervisor GPT Sol 5.6 on 2026-07-22.

`[re-runnable]` **Pre-commit branch tip:** `ffd49047b8b0d9904dd7a69ea7019e67ee5830df` (verified == remote before
edits; working tree clean; candidate rebuilt twice byte-identically: `1373e824` / 804 / 760253 / 9542 / 723
movers vs 06d8af60 / 0 vs 6f07f7cb).

`[re-runnable]` **The single atomic pin movement** (one fast-forward commit; every dependent identity moves
together):

| identity | file | 06d8af60 → 1373e824 |
|---|---|---|
| boot balanced pin | `data/expected_boot.json` `balanced_board_md5` | advanced |
| boot panel note | `data/expected_boot.json` `panel` | re-pinned to R19 build-and-compare values (Daicos 8683, Bontempelli 4278, Sheezel 9542, Gawn 3372, Reid 3531, Ward 2684, Moore 234, Goad 1011, Smillie 1233, Green 651); distinguishes board of record 6f07f7cb from balanced/strict 1373e824 |
| contract identity | `data/release_contract.json` `identities.balanced_board_md5` | advanced |
| contract present-lens | `data/release_contract.json` `present_lens_baseline.balanced_board_md5` | advanced; `active` 804; `present_value_total` 757608 → **760253** (build-and-compare present-v sum; corrects a prior arithmetic inconsistency — see below) |
| contract seal | `data/release_contract.json` `contract_sha256` | `f94a432f…` → `4fdf3c10cee885bd7f57f8ef41e8a9fb3ee7d837c768a8e438f6ab41e6d1600e` (recomputed via `release_contract.contract_hash`) |
| FV accepted oracle | `session_2026-07-20/fv_provenance_remediation/test_fv_provenance.py` `BOARD_MD5_GOOD` / `sum_v` / `sheezel` / ref path | `1373e824` / 760253 / 9542 / `reference_vector_1373e824.json` |
| FV reference vector | `…/fixtures/reference_vector_1373e824.json` (new; md5 `4fcd55c9b5708e791be26e5e157b425e`) | 804 rows, sum 760253, Sheezel 9542; historical `reference_vector_06d8af60.json` preserved |
| UI working bundle | `ui/data/board_view_working.js` | regenerated via `extract_board_view.py` from the **unchanged** canonical board; stamp `board_md5=6f07f7cb`, `balanced_board_md5=1373e824`, store `f37d9716`, `asOfRound 19` |

`[re-runnable]` **present_value_total discrepancy (reported per directive B).** The established repository
semantic for `present_value_total` is the raw present-v sum of the R19 present board, which for the candidate =
**760253** (= board-of-record `6f07f7cb` present-v sum; = the present-board correction's own
`present_total_after` in `session_2026-07-22/present_board_correction/summary.json`). This equals the directive's
expected candidate sum (760253), so the directive's STOP condition ("if the established semantic produces a
different value") is **not** triggered. The prior stored `757608` was a pre-existing arithmetic error (it added
the +5181 D8 present-board delta to the FV present-lens baseline `752427` instead of the correction's present
baseline `755072`; `752427+5181=757608`, whereas `755072+5181=760253`). This regeneration corrects it to the
consistent `760253`.

`[re-runnable]` **Board of record `6f07f7cb` byte-identical (NOT replaced):** `data/rl_build/rl_app_data.json`
md5 `6f07f7cbe042f8e56426a01226c967c9` before and after; the authoritative store `f37d9716`, frozen curve
`56dd7a7b`, curve contract `676ad2b7`, per-entrant `40d7da7c`, `model_config.json`, `season_state.json`, the
score ledger, every workflow, and `docs/OPEN_ITEMS_REGISTER.md` are all byte-identical before/after (measured).

`[re-runnable]` **Tests before commit (pinned venv 3.12.3):**
- Candidate builder ×2 at `ffd49047` → byte-identical: `1373e824` / 804 / 760253 / 9542 / 723 movers vs 06d8af60 / 0 vs 6f07f7cb / `protected_all_unchanged: true`.
- FV provenance suite → **RESULT 8/8 PASS**; `GREEN1_strict_board_1373e824_zero_movers` rc=0 md5=`1373e824` active=804 sumv=760253 sheezel=9542 vector_movers=0 vs `reference_vector_1373e824.json`; GREEN2 + RED1–RED6 (fail-closed paths) all pass, every RED reports `files_unchanged=True`.
- Club-curve provenance → **18/18 fail-closed controls pass**; the only 2 failing checks are the pre-existing CASE1 positive-path historical hardcodes (`2ab73a6f` / `asOfRound 14`) — reported separately, not fixed here (directive item 5).
- `release_contract.py check` → **PASS** (contract `4fdf3c10cee8`; identities + config + posture consistent).
- `extract_board_view.py` → ring-fence OK; `board_view_working.js` stamp `board_md5=6f07f7cb`, `balanced_board_md5=1373e824`, `store=f37d9716`, `asOfRound=19`; `board_view_public.js` byte-identical.
- `py_compile` on every modified `.py` → OK; `git diff --check` → clean.
- Protected-artifact before/after fence → all byte-identical (board of record `6f07f7cb`, store `f37d9716`, curve `56dd7a7b`, curve contract `676ad2b7`, per-entrant `40d7da7c`, `model_config.json`, `season_state.json`, score ledger, all 4 workflows, `OPEN_ITEMS_REGISTER.md`); abort not triggered.

`[re-runnable]` **No prohibited action:** no board-of-record/store/curve/per-entrant/`release_pick_curve.json`
change; no model/valuation code change; no workflow change; no register change; no main merge; no branch merge;
no tag/release/deploy; no score-write activation. STOP-1 **APPROVED AND EXECUTED**; **STOP-2 remains pending**;
the claims-note final signature remains pending GPT Sol 5.6 final independent review (the mechanical builder
does not sign).

## 6. Advance-repin (directive item 5) — IMPLEMENTED

`[report-only]` **Status.** Directive item 5 (step 5 / R2 second half) has two halves — (a) re-aim club-curve
CASE1 at the manifest of record by build-and-compare, and (b) script the sibling regeneration+repin into the
round-advance path. Both are implemented on `ci/r19-provenance-migration`. This section supersedes the prior
"not performed / owner-scoped" note: the owner authorised item 5 through the supervisor after STOP-1. STOP-1
(sections 5 / 5.1) and the STOP-1 signature below are UNCHANGED and not reinterpreted. This builder signs nothing;
the item-5 implementation and evidence are returned for independent review.

`[report-only]` **Blocking correction (execution-supervisor screening, 2026-07-23).** The FIRST integration
(commits `7d73e916` / `99bccb2`) placed the sibling repin as a SEPARATE step after `staged_apply` had already
committed + finalized the store/board (a shell preflight gate + a post-advance `reconcile`). That is NOT the
same transaction: it left an externally-committed store/board interval with stale siblings, and a `.bat` / direct
CLI could bypass the shell gate. Per the supervisor's blocking correction the sibling generation/derivation/
validation/target-movement is now folded INTO the accepted `staged_apply` Python round-advance transaction so the
canonical store/board AND the sibling targets commit under ONE journal + ONE rollback/recovery boundary. The two
earlier commits are RETAINED in branch history (their build-and-compare module, overlay validation, dependent-pin
derivation, rollback machinery and proof harnesses are reused); **the two-step "same commit" / "lockstep" framing
in those commits is WITHDRAWN** and is corrected by §6.b/§6.c below.

`[re-runnable]` **Second blocking correction (execution-supervisor screening, 2026-07-23) — two residual
fail-closed defects closed; the principal single-transaction architecture at `aa55e29` is UNCHANGED.** Applied as
one additive fast-forward child of `aa55e29`; no existing commit amended, squashed or rewritten.

1. **Every declared transaction target is now MANDATORY.** `staged_apply._collect_staged` and `_commit` previously
   SKIPPED a declared target whose validated workspace payload was missing, so a 15-target manifest did not prove
   all 15 were collected + replaced — a missing `board_view_public.js` / sidecar / reference vector could leave a
   committed transaction with a stale dependent artifact. Corrected: once the target manifest is finalized, every
   declared effective target MUST exist in the validated workspace — `_collect_staged` FAILS before backup or
   commit if any is absent, asserts the collected set equals the manifest target set EXACTLY, and records each
   target's validated staged md5 into the txn manifest; `_commit` never silently continues on a missing staged
   payload (it raises an invariant violation → rollback, since commit has begun) and verifies each final live md5
   equals its validated staged md5, journaling `COMMIT_VERIFIED`; `_backup_originals` journals each target as
   backed-up-or-recorded-absent. Proven by §6.c controls P2/#7, P10/#1, P11/#2.
2. **"Full coherence" now covers the FULL sibling set.** Staged validation (`staged_apply._validate_sibling_staged`)
   and the live gate (`sibling_repin.verify` / `assert_current`) now assert, against the freshly-built sibling +
   the staged/live canonical board: BOTH board-view bundles (working balanced / canonical-board / store / round /
   release stamps; the public bundle's player count + name/value row parity with the canonical board and the
   working bundle; public leak-freedom — the two-tier UI law); the reference vector (board id, `active ==
   len(vector)`, `sum_v == sum(vector.values())`, the EXACT built vector, agreement with the sealed present-lens
   active + total); the FV oracle (board id + DERIVED active + sum + Sheezel + regenerated reference-vector
   filename); and the sidecar (store / balanced / active / total / Sheezel / reference-filename / contract-seal).
   `RepinPlan.changed_map` now includes board-view and sidecar coherence, so a view-only or sidecar-only corruption
   is REPAIRED by a standalone `reconcile` (reported changed) rather than returned as a no-op (a `changed_targets`
   KeyError this exposed — board_view/sidecar are not byte-targets in `self.targets` — is fixed). Proven by §6.c
   controls P12/#3–P15/#6.

`[re-runnable]` **Final completion correction (execution-supervisor screening, 2026-07-23) — three narrow
defects closed; still additive, no history rewritten.** Applied as one plain fast-forward child of `2e25ba6`.

1. **The authoritative full check now compares the EXACT vector.** `assert_current(full=True)` previously
   rebuilt the sibling but compared only the rebuilt board md5 to the balanced pin — so a SUM-PRESERVING
   reference-vector corruption (player A +1, player B −1; board id / active / total / Sheezel unchanged) passed
   both the no-build `verify()` (internal arithmetic intact) and the old full check. Corrected: `check --full`
   now loads the LIVE reference vector and compares its COMPLETE `vector` mapping — plus active / total /
   Sheezel — against the freshly-rebuilt sibling, failing with a specific EXACT-VECTOR mismatch reason. The
   two gates are now clearly distinguished (see §6.b): ordinary no-build coherence (`verify()`) vs authoritative
   build-and-compare (`check --full`, mode `full+build-and-compare`). Proven by §6.c control P16/D1.
2. **Standalone `reconcile` now repairs FV-oracle-only drift.** `RepinPlan` previously derived the "current"
   active/sum/Sheezel from the reference-vector DOCUMENT, so an FV-oracle-only corruption failed `verify()` but
   `reconcile` reported a no-op. Corrected: the current oracle is PARSED from its ACTUAL assertion tokens (board
   md5, active, sum, Sheezel, and the actual referenced reference-vector filename); `changed_map["fv_test"]`
   compares those parsed values with the freshly-built desired values; and `_repair_fv_oracle` regenerates the
   oracle STRUCTURALLY (anchored on token shape, fail-closed if any expected token is absent or not exactly
   once) so a corrupt assertion is replaced even when the reference vector is already current, and an unchanged
   oracle round-trips byte-identical. Proven by §6.c control P17/D2 (active / sum / Sheezel / reference-filename
   each independently).
3. **The obsolete two-step advance-chain proof is re-aimed to the folded-in design.** `advance_chain_proof.py`
   and `ADVANCE_CHAIN_RESULTS.json` previously asserted the WITHDRAWN two-step flow (stale-after-advance) and
   the committed result claimed 14/14. Re-aimed to the folded-in single-transaction design: the store, canonical
   board and balanced sibling advance in ONE transaction; the gate is CURRENT immediately (fast + ordinary +
   authoritative `check --full`); a subsequent standalone `reconcile` is a correct NO-OP; every dependent pin /
   vector / oracle / contract / view is coherent; the non-advancing frozen artifacts are byte-unchanged. The
   harness is now fully green and `ADVANCE_CHAIN_RESULTS.json` is regenerated (see §6.c).

### 6.a CASE1 re-aim (accepted separately)

`[re-runnable]` `ui/tests/club_curve_provenance.test.py` CASE1's two positive-path assertions no longer hardcode
the historical Round-14 identity (`2ab73a6f` / `asOfRound 14`). They DERIVE the expected board id, round and
release_version live from the authoritative current manifest `data/expected_boot.json` and assert the resolver's
output stamp equals them (board `6f07f7cb`, R19, `v2.11-final-rc1-PROVISIONAL`) — the same manifest
`ui/tools/ingest_inputs.py` ring-fences the board bundle against, so a clean CASE1 proves the resolved stamp equals
the manifest, and the assertion re-aims automatically after any advance-repin. Fail-closed on any mismatch.
Committed at `aecd719d20a2e5514e628aa2b750c9ea7e007665` (independently accepted). Club-curve suite **35/35** (was
33/35); all **18 fail-closed negative controls preserved**.

### 6.b Scripted sibling advance-repin (new)

`[re-runnable]` New module `engine/rl_after/ingestion/sibling_repin.py` — the scripted, fail-closed, atomic,
idempotent, rollback-safe advance-repin of the balanced/strict SIBLING board + FV reference vector. A `reconcile`:
(1) rebuilds the balanced sibling from the SAME store/config/FV source as the round's canonical board (the accepted
disposable FV builder `_run_build(balanced=True)`, `RL_PVC2=1/RL_LEGE=0/RL_LEGF=0`), asserting the store it built
from equals the manifest's store pin; (2) regenerates the COMPLETE FV reference vector from the built board;
(3) derives the identity + aggregates (board md5, active, present-v sum, sheezel, full vector) from the built
artifacts — never a supplied constant; (4) if the derived identity already equals the live pins, NO-OP (idempotent);
(5) else STAGES the coherent movement of `data/expected_boot.json` `balanced_board_md5`, `data/release_contract.json`
`identities.balanced_board_md5` + `present_lens_baseline` {`balanced_board_md5`, `active`, `present_value_total`} +
re-seal (`release_contract.contract_hash`), a regenerated `fixtures/reference_vector_<md5>.json`, the FV test oracle
(`BOARD_MD5_GOOD` + aggregates + reference path), the `ui/data/board_view_{working,public}.js` balanced stamp, and a
provenance sidecar; (6) VALIDATES the complete staged set on a throwaway OVERLAY (identity coherence across every
target + the contract self-seal + `py_compile` + a fail-closed `release_contract.verify`) BEFORE any live
replacement; (7) COMMITS by atomic `os.replace`, journaled, backing up every original; (8) ROLLS BACK every original
byte-for-byte on a mid-commit fault. It NEVER touches the board of record, store, frozen curve, curve contract,
per_entrant or score ledger (all asserted byte-unchanged before/after every reconcile) and NEVER arms or reads the
score-write gate (it applies NO scores).

`[re-runnable]` **Single-transaction integration (the corrected design).** `staged_apply._stage_sibling`, called
from `_staged_transaction` AFTER the store is merged and the season-state / canonical board / expected_boot /
release_contract are staged and BEFORE validation + commit, builds the balanced/strict sibling from the SAME
workspace's staged store (asserting the store it built from == the staged store), regenerates the full FV reference
vector, and stages every dependent balanced/FV pin + present_lens aggregate + contract re-seal + FV oracle +
board_view + provenance sidecar INTO THE WORKSPACE, on top of the restamped expected_boot / release_contract. The
transaction's target set is EXTENDED (persisted in the txn manifest; `_txn_targets` reads it) with the new sibling
targets — `reference_vector_<md5>.json`, the FV test oracle, `board_view_{working,public}.js`, the sidecar — so
`_collect_staged` / `_backup_originals` / `_commit` / `_restore_from_txn` / crash-recovery cover the canonical AND
the sibling targets under ONE journal + ONE rollback/recovery boundary (a genuine R19→R20 advance commits a
**15-target** set; `SIBLING_STAGED` precedes `COMMIT_BEGIN`, so there is NEVER an externally-committed store/board
state with stale siblings). Every declared target is MANDATORY (2nd blocking correction): `_collect_staged`
fail-closes before backup/commit on any missing target and asserts the collected set equals the manifest set
exactly; `_commit` never silently skips a target and verifies each final live md5 == its validated staged md5
(`COMMIT_VERIFIED`). Staged sibling coherence is validated across the FULL set (`_validate_sibling_staged`:
expected_boot / release_contract identities + present_lens; the reference vector's id + internal arithmetic
[`active == len(vector)`, `sum_v == sum(vector.values())`, exact built vector] + present-lens agreement; the FV
oracle's id + derived active/sum/Sheezel + reference filename; BOTH board-view bundles' stamps + public
parity + leak-freedom; the sidecar aggregate + seal; the contract self-seal) inside `_validate_staged` BEFORE any
live replacement; a sibling build or validation failure aborts pre-commit with nothing live touched; a
commit-phase fault rolls back BOTH canonical and sibling targets; an incomplete transaction blocks the next
advance until `recover` runs. The score-write gate is untouched (no score apply).
Because the invariant lives in the Python transaction that `tools/round_entry/round_entry.py` drives, EVERY
launcher — `weekly_update.sh`, `weekly_update.bat`, direct CLI — inherits it automatically and none can bypass it;
the shell preflight of the first integration is REMOVED (blocking-issues 1 + 2). The standalone
`sibling_repin.py reconcile` remains a REPAIR tool (its own `.sibling_txn`); its `check` / `assert_current` gate now
establishes FULL coherence (release_contract identities + present_lens; the reference vector's id + internal
arithmetic + present-lens agreement; the FV oracle's id + active/sum/Sheezel + reference filename; BOTH board-view
bundles + public leak-freedom; the sidecar aggregate + seal; the contract self-seal) AND refuses on any incomplete
sibling transaction — not merely the sidecar source-store (blocking-issue 3, extended by the 2nd blocking
correction). A view-only or sidecar-only corruption is now REPAIRED by `reconcile` (reported changed), not returned
as a no-op. The FV-oracle re-aim derives the ACTIVE COUNT (and present-v sum + Sheezel) from the built vector —
no literal `804` (blocking-issue 4), and (final correction 2) it PARSES the actual oracle assertion tokens so an
FV-oracle-only drift is detected and its actual corrupt token repaired even when the reference vector is current.

`[re-runnable]` **Two distinct gates (final correction 1 — do NOT conflate them).** (a) ORDINARY no-build
coherence — `sibling_repin.py verify` / `assert_current()` (mode `coherence`): internal agreement across
expected_boot / release_contract identities + present_lens / the reference vector's internal arithmetic / the FV
oracle / the sidecar, the contract self-seal, and `release_contract check`. It does NOT rebuild, so a
SUM-PRESERVING reference-vector corruption (A +1 / B −1) is internally consistent and passes it. (b) AUTHORITATIVE
build-and-compare — `sibling_repin.py check --full` / `assert_current(full=True)` (mode `full+build-and-compare`):
rebuilds the sibling and compares the live reference vector's COMPLETE vector mapping + active + total + Sheezel
against the freshly-rebuilt sibling, so the sum-preserving corruption fails here with an EXACT-VECTOR mismatch.
The claims note does not present ordinary coherence as build-and-compare.

`[re-runnable]` **Pinned environment.** Every board build ran in the accepted pinned environment
(`/root/rl_venv312`: Python 3.12.3 / numpy 2.4.4 / scipy 1.17.1 / scikit-learn 1.8.0 / openpyxl 3.1.5;
`PYTHONHASHSEED=0`, single-thread BLAS, `RL_PVC2=1/RL_LEGE=0/RL_LEGF=0`, bootstrap-seeded workspace, ENV-PIN
byte-exact numpy + bundled OpenBLAS `05c9f9eb`). FV provenance GREEN1 reproduces the accepted balanced board
`1373e824` / 804 / 760253 / 9542 / 0 movers under this env.

### 6.c Evidence (all re-runnable; scratch/fixtures only; NO real score apply; gate OFF)

`[re-runnable]` **Single-transaction integration** — `session_2026-07-23/item408_sibling_repin/staged_sibling_integration_proof.py`
→ **60/60 PASS** (the original 28 checks RETAINED; 18 controls added for the 2nd blocking correction; 14 more added for the final completion correction; scratch only; gate armed IN-PROCESS against the scratch only):
- **Current R19 no-op reproduction.** `build_sibling` on the LIVE tree rebuilds the sibling to `1373e824` / 804 /
  760253 / 9542; `sibling_repin.py reconcile` on the LIVE tree is a NO-OP (no pin moved), writing only the
  provenance sidecar — no existing committed file changed.
- **Genuine R19→R20 advance under ONE transaction.** A scratch driven through a REAL store advance by
  `staged_apply.apply_snapshot` moved the STORE (`f37d9716`→`18c5fea2`), the CANONICAL BOARD of record
  (`6f07f7cb`→`36e61ea5`) and the BALANCED SIBLING (`1373e824`→`4f940581` — it TRACKS the new store) together, with
  the full FV reference vector, expected_boot, release-contract identities + present_lens aggregate + re-seal, the
  FV oracle and the board_view stamp all coherent; `SIBLING_STAGED` precedes `COMMIT_BEGIN` (NO externally-committed
  stale-sibling interval); ONE txn manifest covers a **15-target** set (canonical + sibling); `release_contract
  check` PASS on the fully-advanced tree.
- **Fail-closed before commit.** An injected sibling-GENERATION failure AND an injected sibling-VALIDATION failure
  each abort pre-commit → NO live target changed.
- **Rollback across the single boundary.** A fault after the FIRST CANONICAL replacement, and a fault after a
  SIBLING replacement, each roll back EVERY canonical + sibling target byte-for-byte.
- **Crash recovery.** A COMMITTING crash (partial canonical + sibling writes) BLOCKS the next advance
  (`IncompleteTransactionError`) and is RECOVERED (rolled back), restoring every target.
- **Active-count derived / launchers.** The FV-oracle re-aim asserts a synthetic sibling's active count `== 800`
  (derived from the built vector, no literal `804`); `weekly_update.sh` / `weekly_update.bat` / the round_entry CLI
  all route through `staged_apply.apply_snapshot` which folds in `_stage_sibling` — no launcher bypass.
- **Mandatory targets + full sibling coherence (2nd blocking correction; the 18 added controls).** P2/#7: on the
  successful R19→R20 advance, manifest target count == collected count == replacement-event count (15/15/15) and
  every final live target md5 == its validated staged md5. P10/#1: dropping `board_view_public` after sibling
  staging but before validation aborts pre-commit, no live target changed. P11/#2: dropping any one declared
  target before collection refuses on the mandatory-target invariant, no partial commit. P12/#3: a reference-vector
  player-value corruption (board id retained) fails `assert_current` on the arithmetic (`sum_v != sum(vector)`).
  P13/#4: FV-oracle active / sum / Sheezel / reference-filename drifts (board id retained) each fail their OWN
  invariant. P14/#5: working and public board-view corruptions each fail the coherence gate. P15/#6: a view-only
  corruption is REPAIRED by standalone `reconcile` (reported changed, not a no-op) and the gate is coherent again
  after — this control also surfaced and fixed a `changed_targets` KeyError (board_view/sidecar are coherence
  flags, not byte-targets).
- **Authoritative full build-and-compare + FV-oracle-only repair (final correction; the 14 added controls).**
  P16/D1: a SUM-PRESERVING reference-vector corruption (A +1 / B −1) passes the no-build `verify()` (internal
  arithmetic intact) but `check --full` FAILS specifically on the EXACT-VECTOR mismatch (rebuild + complete-vector
  compare). P17/D2 (×4 — active / sum / Sheezel / reference-filename, each independently): an FV-oracle-only drift
  fails `verify()` on its OWN invariant; standalone `reconcile` reports changed=True (not a no-op) and REPAIRS the
  actual corrupt token; `verify()` and `check --full` (mode `full+build-and-compare`) are green afterward.

`[re-runnable]` **Supporting suites (re-run this container; pinned venv `/root/rl_venv312`):** FV provenance
**8/8 PASS** (GREEN1 reproduces `1373e824` / 804 / 760253 / 9542 / 0 movers; RED2/RED3 halt fail-closed with the
named FV loaded-path / checkout-drift reason); `one_source_selftest.py` (CI Guards) **PASS** (single source;
guards 1-3; board==engine F1; book==board F2; frozen-ruler STAMP re-scope), run after the standard CI-Guards
board+book bootstrap; club-curve CASE1 **35/35** (all 18 negatives fail-closed); `release_contract check` **PASS**
(seal `4fdf3c10cee8`); `sibling_repin.py check` **CURRENT** and `check --full` **CURRENT** (build-and-compare
rebuilds `1373e824`); `sibling_repin_proof.py` **26/26** (standalone reconcile build/derive/stage/validate/commit/
rollback/idempotence/repair, incl. the `changed_targets` fix). Frozen artifacts at accepted md5s (board of record
`6f07f7cb`, store `f37d9716`, curve `56dd7a7b`, curve contract `676ad2b7`, per_entrant `40d7da7c`).

`[re-runnable]` **`advance_chain_proof.py` re-aimed to the FOLDED-IN single-transaction design (final correction
3) — 15/15 PASS**, `ADVANCE_CHAIN_RESULTS.json` regenerated. On a genuine R19→R20 scratch advance the store,
canonical board of record and balanced sibling advance in ONE `staged_apply` transaction (CHAIN 1-2), every
dependent pin / reference vector / FV oracle / contract identities+present_lens+seal / board-view is coherent, the
gate is CURRENT IMMEDIATELY (fast + ordinary `verify` + authoritative `check --full` mode `full+build-and-compare`,
CHAIN 3), a subsequent standalone `reconcile` is a correct NO-OP moving no committed file (CHAIN 4), and the
non-advancing frozen artifacts — curve `56dd7a7b`, curve contract `676ad2b7`, per-entrant `40d7da7c` — are
byte-unchanged (CHAIN 5; the store, board of record, season-state and score ledger legitimately advance with the
round). The prior committed `14/14` asserted the WITHDRAWN two-step flow (stale-after-advance, from the two-step
commit `99bccb2`) and was superseded; the harness no longer describes obsolete behaviour.

`[report-only]` **Re-run environment reconstruction.** This container reconstructs the accepted pinned env:
`/home/claude/rl_vendor` (vendored `unidecode`) restored from the repo's committed `vendor/`; suites run under
`/root/rl_venv312` (py 3.12.3 / numpy 2.4.4 / scipy 1.17.1 / sklearn 1.8.0 / openpyxl 3.1.5), `PYTHONHASHSEED=0`,
single-thread BLAS. FV provenance runs with `RL_VENDOR` UNSET — bake-mode config enforcement correctly rejects
`RL_VENDOR` as an unknown model override, so `unidecode` is resolved via the FV builder's own `PYTHONPATH`, not
that env var. `one_source_selftest.py` runs after the standard CI-Guards board+book bootstrap (`rl_export.py` +
`s4_matrix_M1v7.py`, per `.github/workflows/ci-guards.yml`), with the repo root on `PYTHONPATH` for `fv_provenance`.

`[report-only]` **Legacy weekly-updater proofs vs the R19 store.** `failure_injection_proof.py` (applies R15) and
`two_round_proof.py` (R15→R16) now REFUSE at the dedup gate (`DuplicateRoundError`, `staged_apply.py` ~line 412 — a
PRE-STAGING refusal, before any sibling code) because the accepted store advanced R14→R19 (ledger = rounds
[15..19]). This is a pre-existing store-advancement staleness, independent of item 5 (the sibling integration lives
in `_staged_transaction`, never reached by those R15/R16 applies). The APPLICABLE weekly-updater proof for the R19
store is the single-transaction suite above (genuine R20 advance + fault injection + rollback + crash recovery
through `staged_apply`). `failure_injection_proof.py` is left BYTE-UNCHANGED; the integration suite self-augments
its scratch to be sibling-capable.

`[report-only]` **Scope boundary.** The sibling regeneration moves the machine-asserted balanced/strict + FV pins
only; the board of record `6f07f7cb` is FROZEN and NOT written by the sibling step (the canonical board is the
transaction's own `_regen_board_strict` output, and both advance together under the one commit). The descriptive
`expected_boot.panel` prose (board-of-record present values) is not a machine-checked sibling pin and is left to the
owner-scoped panel note. Items 6 (Live Scoring) and 7 were NOT begun.

## 7. Live Scoring diagnosis and repair (ITEM 408 item 6)

`[builder-generated evidence]` This section and section 8 are **builder-generated evidence** authored by
the `claude-code-builder` build seat. They are **NOT** the cold blind review; the execution supervisor
(GPT Sol 5.6) has **not** accepted them; **STOP-2 has not been granted**; no merge, tag, release,
deployment or score-write activation is authorised. The STOP-1 owner word (§5.1) and the GPT Sol 5.6
STOP-1 review signature below are **UNCHANGED** and not reinterpreted.

### 7.0 Branch, identity, deviations
- Repository `lukemcalister10/afl-rl-engine`; exact starting SHA `1606d13408f6ca45013e21faec2b3b6a9454f033`.
- Build seat: author == committer == `claude-code-builder <claude-code-builder@seam.local>` on every commit.
- **DEVIATION — push target.** The directive names `ci/r19-provenance-migration` as the push target; this
  session's harness constraint designates the feature branch `claude/item-408-fixture-repair-e2o53i` and
  forbids pushing elsewhere without explicit permission (the operator declined to override). All work is
  **based on the required tip `1606d134`** and pushed to the **feature branch**; `ci/r19-provenance-migration`
  is left byte-untouched for the supervisor to promote.
- **DEVIATION — side branch.** Directive §2 asks to delete remote `claude/item-408-item-5-continuation-hqmpm4`
  (currently == `1606d134`, no unique commits). NOT performed (destructive shared-remote op left to the owner).
  Command it would have used: `git push origin --delete claude/item-408-item-5-continuation-hqmpm4`. The branch
  remains present on the remote.
- **DEVIATION — commit trailers.** The harness default appends `Co-Authored-By: Claude …` / `Claude-Session`
  trailers; these are OMITTED to match the repo's trailer-free build-seat convention and the directive's
  single-build-seat provenance intent.

### 7.1 Complete baseline red list (exact tip 1606d134, pinned env, BEFORE any edit)
Env: `/root/rl_venv312` — Python 3.12.3; numpy 2.4.4 + bundled OpenBLAS `05c9f9eb89ee68a4b9d673…` (byte-exact
to the pin); scipy 1.17.1; scikit-learn 1.8.0; openpyxl 3.1.5. `RL_VENDOR=/home/claude/rl_vendor`.

| # | command | exit | elapsed | first natural failure |
|---|---------|------|---------|-----------------------|
| 1 | `test_weekly_updater.py` | 0 | 0.5s | PASS |
| 2 | `test_catchup_preflight.py` | 0 | 0.2s | PASS |
| 3 | `two_round_proof.py --write` | 1 | 1.3s | `round_apply.DuplicateRoundError: round already applied … 2026\|15` |
| 4 | `catchup_proof.py --write` | 1 | 0.7s | `KeyError: 'players_applied'` (downstream of a dedup-refused apply) |
| 5 | `node ui/tests/movers.test.js` | 1 | 0.3s | `MOVERS TESTS: 3 FAIL / 47` (production movers.js carries R15-19; test asserts EMPTY) |
| 6 | `movers_proof.py --write` | 1 | 0.1s | `FAIL 0_production_empty_and_derived_identity` |
| 7 | `failure_injection_proof.py --write` | 1 | 0.4s | `DuplicateRoundError … 2026\|15` |
| 8 | `finalization_injection_proof.py --write` | 1 | 0.2s | `DuplicateRoundError … 2026\|16` |
| 9 | `rc_manifest_compat_proof.py --write` | 0 | 0.0s | PASS |
| 10 | `storewrite_proof.py --write` | 1 | 90.9s | `DuplicateRoundError … 2026\|15` |
| 11 | `fv_provenance_proof.py --write` | 1 | 0.3s | `DuplicateRoundError … 2026\|15` |

- **First natural failure of the set:** cmd 3, `two_round_proof.py`, `round_apply.DuplicateRoundError`.
- **Live-file impact during the baseline run:** only `session_2026-07-20/live_scoring_catchup/movers_proof.json`
  (a proof-evidence file) changed; **no canonical production file was touched**.

### 7.2 Measured root cause (hypothesis CONFIRMED; fixture-only). Two defects, one over-materialisation.
Both were introduced by commit `6e4c28c "Materialize verified Round 19 MVP state"`:

1. **Fixture drift (dedup reds 3, 4, 7, 8, 10, 11).** Each Live Scoring proof builds a disposable scratch by
   `copytree` of the CURRENT checkout, which at `1606d134` is materialised at **R19**:
   `season_state`/`expected_boot` `as_of_round=19`; store `f37d9716…` (not R14 `968de0c7…`); board `6f07f7cb…`
   (not R14 `2ab73a6f…`); `applied_rounds_ledger.json` = 1858 entries for rounds {15:318, 16:319, 17:410,
   18:406, 19:405}. The proofs DECLARE an R14 baseline and apply R15/R16, which the **production
   duplicate-round gate correctly refuses** as already-applied. Fixture drift — the disposable fixture no
   longer reconstructs its declared R14 baseline — **not** a dedup defect. Confirmed: the R14 authority anchor
   `93bd01af` carries store `968de0c7`, board `2ab73a6f`, `expected_boot.as_of_round=14`, and an EMPTY ledger.
2. **Production movers regression (reds 5, 6).** The same commit flipped `ui/data/movers.js` from its EMPTY
   bundle to carrying R15-19 reports, silently undoing the accepted "review directive A" corrective — see the
   full movers adjudication in **§7.8**.

Also measured (the failure hidden behind dedup): the item-5 sibling-integrated staged transaction
(`staged_apply._prepare_workspace`, lines 706-710) copies three CURRENT source trees from the scratch root into
the txn workspace — `session_2026-07-20/fv_provenance_remediation`, `ui`, `session_2026-07-17/legd_derivation`
— but the shared `make_scratch` copied NONE; `generate_movers_bundle.py` patched only
`ui/tools/extract_board_view.py` ad hoc.

### 7.3 Repair (changed-file census + design)
| file | kind | change |
|---|---|---|
| `engine/rl_after/ingestion/scratch_fixture.py` | fixture | +`materialize_r14()`, `install_sibling_support_trees()`, `_verify_r14()`, `_restamp_contract_code_identity()`, R14 authority constants (+`shutil`,`subprocess`) |
| `session_2026-07-20/weekly_updater_hardening/failure_injection_proof.py` | proof factory | `make_scratch()` → install sibling trees + `materialize_r14()` (used by two_round, catchup, finalization via `FI.`) |
| `session_2026-07-20/weekly_updater_hardening/fv_provenance_proof.py` | proof factory | `make_scratch()` → install sibling trees + `materialize_r14()` (staged path) |
| `session_2026-07-19/storewrite/storewrite_proof.py` | proof factory | `make_scratch()` → `materialize_r14()` (RoundApplier path; no sibling advance) |
| `ui/data/movers.js` | production UI data | restored byte-exact to the accepted EMPTY bundle at `0e577f5` (see §7.8) |
| `.github/workflows/live-scoring.yml` | CI | checkout `fetch-depth: 0` (R14 fixture reads exact historical git bytes) |
| `engine/rl_after/ingestion/test_r14_fixture.py` | test (new) | fail-closed fixture tests + negative controls |
| `engine/rl_after/ingestion/test_weekly_updater.py` | test | runs the R14 controls from the existing fast-tests step |

**Historical R14 anchor:** `93bd01af86db00c169714652714a364bd2635764` (ancestor of `1606d134`). The helper reads
EXACT git bytes; it never recreates historical JSON from memory and never copies historical source over current
source.

**Restored R14 dynamic state (exact anchor bytes):** `engine/rl_after/rl_model_data.json` (store `968de0c7`);
`data/rl_build/rl_app_data.json` (board `2ab73a6f`) + `.srcmd5` sidecar; `data/expected_boot.json`
(`as_of_round=14`); `data/season_state.json` (`as_of_round=14`, `source_store_md5=968de0c7`);
`data/release_contract.json`; `engine/rl_after/ingestion/applied_rounds_ledger.json` (`applied==[]`).
**Reproduced R14 absence (removed from scratch, PROVEN absent at the anchor):** value/rank/pos_rank histories,
`finalization_state.json`, `finalization_journal.jsonl`, `sibling_repin_state.json`, `movers/`, `.weekly_txn/`.

**Restored + verified R14 identities (in the disposable scratch):** store `968de0c7`; canonical board
`2ab73a6f`; `expected_boot` `as_of_round=14`, store `968de0c7`, board `2ab73a6f`, `balanced_board_md5`
`06d8af60`; `season_state as_of_round=14` bound to `968de0c7`; `release_contract as_of_round=14`, identities
coherent, self-seal recomputes; ledger empty; `release_contract.verify(gate)` PASS.

**Only stamped identity (line-by-line justification):** `engine_head` moves `dc7e34b0` (R14-era code) →
`7c452715` (CURRENT `_merged_recover.py`) in both `expected_boot` and the contract, then re-seal — because the
fixture runs the **current engine** (directive §7). Every immutable model input (`rl_model 4f776e07`, `fv
6a9a520f`, `config 45b207c0`, `register 652d83e8`, `band 34faa865`, `q97m`, `v0surf`, …) is byte-coherent
R14 == checkout and is left exactly as restored — **no silent immutable re-stamp**. No scoring aggregation,
valuation, dedup, or gate code changed.

### 7.4 Negative controls (`test_r14_fixture.py` — ALL PASS)
1 unavailable anchor halts · 2 wrong R14 store md5 halts · 3 wrong R14 board md5 halts · 4 non-ancestor anchor
halts · 5 R19 ledger cannot leak · 6 R19 finalization cannot leak · 7 R19 movers cannot leak · 15 missing
sibling trees fail closed · 16 historical restore does not replace current source · 17 current immutable inputs
stay current · 18 release-contract verifies on the restored R14 fixture. Controls 8-14 (genuine dedup refusal;
gate OFF; canonical byte-stability; canonical+sibling advance under one txn; failure-injection / rollback /
crash-recovery over the canonical+sibling set) are PRESERVED in
`failure_injection_proof.py` / `finalization_injection_proof.py` / `two_round_proof.py` / `catchup_proof.py`
and are green in §7.5.

### 7.5 Item-6 acceptance — full Live Scoring set on the repaired R14 fixture — **ALL GREEN**
| # | command | exit | elapsed | evidence |
|---|---------|------|---------|----------|
| 1 | `test_weekly_updater.py` (wired R14 controls) | 0 | 3s | — |
| 2 | `test_catchup_preflight.py` | 0 | 0.2s | — |
| 3 | `two_round_proof.py --write` | 0 | 942.6s | `live_scoring_two_round/proof.json` (baseline board 2ab73a6f) |
| 4 | `catchup_proof.py --write` | 0 | 1288.0s | `live_scoring_catchup/proof.json` |
| 5 | `node ui/tests/movers.test.js` | 0 | 0.2s | ALL 47 PASS |
| 6 | `movers_proof.py --write` | 0 | 0.1s | `movers_proof.json` |
| 7 | `failure_injection_proof.py --write` | 0 | 1195.9s | `weekly_updater_hardening/proof.json` |
| 8 | `finalization_injection_proof.py --write` | 0 | 745.4s | `finalization_proof.json` |
| 9 | `rc_manifest_compat_proof.py --write` | 0 | 0.0s | `rc_manifest_compat_proof.json` |
| 10 | `storewrite_proof.py --write` | 0 | 666.6s | `storewrite/proof.json` |
| 11 | `fv_provenance_proof.py --write` | 0 | 363.9s | `fv_proof.json` |

Demonstrated: R15→R16 two-round; R15→R19 catch-up + restart/resume; genuine duplicate-execution refusal;
failure injection; rollback; crash recovery; finalization recovery; movers integrity; history integrity;
release metadata; FV provenance; balanced/strict sibling advancement integrated in the same transaction.

### 7.6 Production dedup NOT weakened
- Production files `round_apply.py`, `staged_apply.py`, `score_ingestor.py`, `applied_rounds_ledger.json` are
  **byte-identical** before/after (git-clean). No ledger reset/delete/ignore path was added.
- Negative control 5 proves an injected R15 ledger entry makes the R14 scratch fail closed; the
  failure-injection re-send/stale acceptance proves a genuinely repeated snapshot still raises
  `DuplicateRoundError`; a legitimate new round proceeds only on a clean R14 baseline.
- **No test-only flag affects real-repo execution:** the shipped gate needs BOTH halves
  (`score_ingestor.APPLY_DEFAULT=False` + env `INGEST_SCORE_APPLY` unset); the real-store apply refuses
  (`IngestionGatedError`); the proofs arm only in-process against scratch.

### 7.7 Protected artifacts — before == after (git-clean vs 1606d134)
| md5 | artifact |
|---|---|
| `f37d9716648cfe4382b8c6a24c4f064f` | `engine/rl_after/rl_model_data.json` (R19 store) |
| `6f07f7cbe042f8e56426a01226c967c9` | `data/rl_build/rl_app_data.json` (R19 board of record) |
| `1d9faae56bc4896a1bf10f9289d45461` | `applied_rounds_ledger.json` (real applied-round ledger) |
| `7aa05ab7150d9fece71dd6920de79cf0` | `value_history.json` |
| `d8b7a9d8efef54c70df33eb23aaada35` | `rank_history.json` |
| `03ebeab3e0ea72f7545de46eda8c69a2` | `pos_rank_history.json` |
| `a5d18fdbed570140198923357fbfd491` | `finalization_state.json` |
| `3af05e5fda4238ecce247da1af845879` | `finalization_journal.jsonl` |
| `56dd7a7bca4306d9224aec0ef52efa32` | `engine/rl_after/pvc_curve_v2.json` (adopted PVC curve) |
| `40d7da7c7461024048fe48fcba5692ff` | `session_2026-07-17/legd_derivation/out/per_entrant.json` (per-entrant) |
| `e8681864e4f02aed4f8bddc501ea8304` | `engine/rl_after/ingestion/movers/` (combined; protected per-round outputs) |

Prescreen independently recomputes `data/rl_build/rl_app_data.json` md5 `6f07f7cb` == pin, and reports
`expected_boot` unchanged and `run_panel.sh` pins unchanged (§8).

### 7.8 `ui/data/movers.js` adjudication — **CATEGORY 1 VERDICT WITHDRAWN by owner ruling (Option A, 2026-07-23)**

> **WITHDRAWN (owner ruling of record, top of note; §9).** The owner has ruled (Option A) that the
> authorised Round 15–19 recovery **is** genuine production Movers history. The Category 1 "unauthorised
> materialisation regression" verdict below is **withdrawn**: the populated R15–R19 bundle is **retained**
> (restored byte-exact from `1606d134:ui/data/movers.js`, md5 `2e1edb45…`) and bridged to the current
> accepted release by the owner-approved fail-closed provenance transition (§9). The empty-restore this
> subsection defended (md5 `83bc7b8f…`) is reverted. The paragraphs below are preserved as the
> **superseded** builder analysis; read §9 for the current, authoritative treatment.

The original (now-withdrawn) analysis, for the record:

This file **was changed** by this work (restored to empty). It is the UI **shipping** bundle, contractually
required to remain empty until an owner-authorised real scoring apply — **not** a protected R19 scoring artifact.

- **hash at base `1606d134`:** MD5 `2e1edb4557509a5f057ec5e6e16b7178` / SHA-256
  `9c6962c3a9bc86f7fe97548fb704c5ffd7bb728aceec16bb66938c7dec525a06`; `rounds:[15,16,17,18,19]` (POPULATED).
- **hash after repair:** MD5 `83bc7b8f977ad4c08082d6ea25bb9f5b` / SHA-256
  `121378a438b5f1cb280b4da82c282a57d295bd26ea11b3cb9c72cda0ec2755fc`; `rounds:[]` (EMPTY).
- **exact historical accepted-empty blob:** `0e577f5:ui/data/movers.js` — MD5 `83bc7b8f…` (byte-identical to
  the restore); commit `0e577f5 "movers UI: generic full-identity lineage anchoring + empty bundle anchored to
  the loaded app"`.
- **exact commit that changed EMPTY → POPULATED:** `6e4c28c "Materialize verified Round 19 MVP state"`
  (parent `6e4c28c^` had `rounds:[]`; `6e4c28c` has `rounds:[15,16,17,18,19]`).
- **contracts/tests/docs requiring the shipped bundle EMPTY (four, independent):** (i) the file's own header
  `"Ships EMPTY until real scoring is owner-applied … Do not hand-edit."`; (ii) `movers_proof.py` test 0
  (`prod_empty = rounds==[] and not reports`); (iii) `generate_movers_bundle.py` line 91
  `assert prod['rounds'] == []` + docstring "corrective 2026-07-20, review directive A: this NO LONGER writes
  the production ui/data/movers.js"; (iv) `ui/tests/movers.test.js` line 142 `eq(prod.rounds, [], …)` under
  "PRODUCTION bundle ships EMPTY (directive A)".
- **restoring discards NO owner-authorised real score application:** (a) the scratch evidence bundle
  `movers_bundle_scratch.js` still carries R15-19 — the movers **data** is preserved, not lost; (b) the shipped
  score-write gate is OFF (`APPLY_DEFAULT=False`, `INGEST_SCORE_APPLY` unset); (c) **STOP-2 is owner-held and
  not granted**, so no owner-authorised apply exists to discard; (d) `generate_movers_bundle.py` docstring: the
  R15-19 are "disposable scratch proof evidence (they begin from the superseded board 270a2c5f), NOT production
  state".
- **not a protected artifact:** the protected per-round movers outputs `engine/rl_after/ingestion/movers/` are
  **byte-unchanged** (§7.7). The R19 store/board/ledger are byte-unchanged. `ui/data/movers.js` is a downstream
  UI presentation bundle only.
- **Verdict (WITHDRAWN):** the original verdict — "the populated file is an unauthorised materialisation
  regression (category 1)" — is **withdrawn** by the owner Option A ruling. The populated R15–R19 bundle is
  the owner-authorised production Movers history; the empty-restore is reverted; the correct treatment is
  the retained bundle + fail-closed provenance transition of **§9**.

## 8. Item-7 close — four-suite + prescreen, Final Integration migration (ITEM 408 item 7)

`[builder-generated evidence]` This section SUPERSEDES the earlier "Final Integration RED (pre-existing R19
staleness)" conclusion. Under the owner Option A ruling, the stale R14-era Final Integration oracles are
MIGRATED (Commit E) to the accepted ITEM 408 STOP-1 R19 authorities, with **no protected production value
moved** (§8.4). Authored by `claude-code-builder`; NOT the cold blind review; STOP-2 NOT granted; no merge/
tag/release/deploy; score-write gate OFF.

### 8.1 Final Integration oracle migration table (every stale oracle → accepted replacement)

| stale oracle (superseded) | migrated to (accepted authority) | file(s) |
|---|---|---|
| present-lens (10): R14 Board A `f05ebe6` / balanced `06d8af60` / present-v total `752427` | committed reference vector `reference_vector_1373e824.json` (accepted balanced/strict `1373e824`, active 804, present-v total `760253`); board of record `6f07f7cb` has 0 present-v / rank / order movers vs it | `invariant_proof.py` |
| section cascade: one aggregate `ok` gated sections 10/11/12/13 | per-section booleans `ok_present`/`ok_forward`/`ok_draft`/`ok_f5`; each acceptance section consumes ONLY its own (no cascade) | `invariant_proof.py`, `acceptance_matrix.py` |
| forward-lens (11): R14 Board B `1f10220c` asserted as an R19 pass | owner-DEFERRED — no accepted R19 forward oracle; R19 vectors gated present+frozen on `6f07f7cb`; vs-Board-B deltas recorded, not asserted (§8.2) | `invariant_proof.py`, `acceptance_matrix.py` |
| R14 season-state: `derive(14, current R19 store f37d9716)` → 0.727 asserted `== 0.545` | `derive(14, exact R14 anchor store 968de0c7 @ 93bd01af)` → 0.545; the current R19 store SEPARATELY derives 0.727 / calendar 0.79 | `season_progress_test.py`, `final-integration.yml` |
| stale-state negatives: mutate-then-halt with no proven-coherent baseline | fully coherent positive fixture (every file `release_contract.verify` reads) PROVEN to pass first, then one field mutated per control + the halt reason names it | `season_progress_test.py` |
| canonical store (17): hardcoded `store_md5 == R14 968de0c7` | expected store DERIVED from the accepted manifest `expected_boot.store` (`f37d9716`, byte-unchanged); scratch's R14 `968de0c7` start proven SEPARATELY | `acceptance_matrix.py` |
| acceptance metadata: branch `integration/v2.11-final-rc`, board `2ab73a6f`, config `3a1e714f`, `generated_for` | current ITEM 408 candidate: branch `claude/item-408-fixture-repair-e2o53i`, board of record `6f07f7cb`, config `45b207c0` | `acceptance_matrix.py` |
| season-advance labels "968de0c7 / 2ab73a6f untouched" | labels DERIVE from the measured current store/board (`f37d9716` / `6f07f7cb`); scratch R14 baseline `2ab73a6f` clarified as distinct | `season_advance_r14_r19_proof.py` |

Every migrated expectation points to an already-accepted authority (the committed reference vector, the
accepted manifest, the exact R14 anchor bytes) or is derived from one. **No expectation was changed merely
to make a failure disappear.** No protected store/board/valuation moved; the board of record `6f07f7cb`
stays frozen.

### 8.2 Forward-lens acceptance is OWNER-DEFERRED — surfaced for supervisor ratification

`[builder-generated evidence — JUDGMENT, awaiting GPT Sol 5.6 / owner ratification]` The forward-lens
(vP1/vP2) has **no accepted R19 authority**: the owner has explicitly NOT accepted the vP1/vP2 outputs and
the forward-lens repair is DEFERRED (`data/expected_boot.json` `_present_staleness_note`
"forward-lens treatment intentionally unchanged and deferred"; `data/release_lineage.json`
`_present_lens_only` "owner … has NOT accepted the old vP1/vP2 forward-lens outputs"). Board B `1f10220c`
is the SUPERSEDED R14 forward oracle; the R19 board-of-record forward vectors advanced with the round
(**vP1 684 / vP2 674 changed** vs Board B — the same advance as the **723 present-v STOP-1 movers**).
`invariant_proof.py` therefore does NOT assert vP1/vP2 equality to the stale R14 oracle; it gates the
ACCEPTED property (forward vectors present + numeric on the frozen board of record over the exact active
universe) and RECORDS the vs-Board-B deltas as a transparent DEFERRED item; `acceptance_matrix.py` marks
section 11 `DEFERRED` (a non-blocking status, distinct from FAIL). This is a builder JUDGMENT consistent
with the documented owner deferral — it moves no board/store/valuation and asserts no stale oracle as a
pass — but it is a material treatment and is surfaced here for ratification. **A supervisor/owner who
prefers to treat forward-lens as a hard blocker would leave Final Integration RED and this candidate NOT
ready.** (The owner declined to rule on this specific point at build time; the builder proceeded with the
transparent deferral and flags it.)

### 8.3 Suite results

`[re-runnable]` The four required suites and prescreen run authoritatively in CI (GitHub Actions), which
carries the full history + pinned-env bootstrap this build container lacks. Local results below confirm the
migrated code; the **authoritative four-suite green is the CI run triggered by this push**.

| suite | migrated-code local result | authoritative (CI) |
|---|---|---|
| **FV Provenance** | **RE-CONFIRMED GREEN 8/8 in this container** — `test_fv_provenance.py`: GREEN1 rebuilds the balanced board `1373e824` / active 804 / present-v total 760253 / Sheezel 9542 / 0 movers (== the accepted R19 present authority the §8.1 migration targets); GREEN2 provenance record; RED1–RED6 all fail-closed, every RED `files_unchanged=True`. Code byte-UNCHANGED by this work (`data/release_lineage.json`'s additive `release_transition` is not read by the FV path). | CI `fv-provenance.yml` is authoritative (pending this push) |
| **CI Guards** | code byte-UNCHANGED (`one_source_selftest.py` / `rl_export.py` / `run_panel.sh` untouched); `data/release_lineage.json` addition is NOT read/pinned by any guard | CI `ci-guards.yml` (pending this push) |
| **Live Scoring** | fast tests GREEN — `test_weekly_updater.py` (incl. R14 fixture + new movers transition 25/25), `test_catchup_preflight.py`, `movers.test.js` **62/62**, `movers_proof.py` ALL PASS (test 0 = populated + provenance bridge), `movers_ui_check.mjs` **21/21** (browser: shipped bundle BRIDGES, fails closed without the transition). Board-building proofs (two_round / catch-up / storewrite / fv / failure- + finalization-injection) are CI-authoritative (each 600–1300 s; need the pinned-env board bootstrap). | CI `live-scoring.yml` (pending this push) |
| **Final Integration** | MIGRATED (§8.1). `invariant_proof.py` **33/33** (present-lens vs `reference_vector_1373e824`; forward-lens DEFERRED; draft-assets + F5 green); `season_progress_test.py` **25/25** (R14 from the anchor store 0.545; R19 current 0.727; 5 stale-state negatives each naming their field); `acceptance_matrix.py` sections all PASS/DEFERRED — **no hard-fail** section (10 PASS, 11 DEFERRED, 12/13 PASS, 17 PASS on the manifest-derived store); `movers.test.js` **62/62**; `season_state_fenced_test.py` / `release_state_failclosed_test.py` / seams unchanged. `extract_seam.test.py` **42/42** on the new committed schema fixture (the runtime `git show 6720dfae` was a fixture-portability defect — the commit is dangling/unreachable and failed in CI too; **repaired in §10**); the clean-room / r15-ladder / season-advance board builds are CI-authoritative. | CI `final-integration.yml` GREEN through every step after the §10 repair |
| **prescreen** | `tools/seat/prescreen.sh claude/item-408-fixture-repair-e2o53i 902bd435` reads the pushed remote branch — run after push; board recompute `6f07f7cb` == pin; `expected_boot` byte-unchanged | run post-push |

**Item-6/7 impact is strictly positive:** the earlier Final Integration reds are RESOLVED by the migration —
present-lens (10) `752427`→`760253` on the accepted reference vector, R14 season-state `0.727`→`0.545` from
the anchor store, the section cascade removed, `movers.test.js` GREEN. The one non-green section is the
owner-DEFERRED forward-lens (§8.2), which is non-blocking and awaits ratification.

### 8.4 Protected artifacts — before == after (byte-unchanged vs base `902bd435`)

`[re-runnable]` Every protected artifact is byte-identical before (base `902bd435`) and after (Commit F):

| md5 (before == after) | artifact |
|---|---|
| `f37d9716648cfe4382b8c6a24c4f064f` | `engine/rl_after/rl_model_data.json` (R19 store) |
| `6f07f7cbe042f8e56426a01226c967c9` | `data/rl_build/rl_app_data.json` (R19 board of record) |
| `1d9faae56bc4896a1bf10f9289d45461` | `applied_rounds_ledger.json` |
| `7aa05ab7150d9fece71dd6920de79cf0` | `value_history.json` |
| `d8b7a9d8efef54c70df33eb23aaada35` | `rank_history.json` |
| `03ebeab3e0ea72f7545de46eda8c69a2` | `pos_rank_history.json` |
| `a5d18fdbed570140198923357fbfd491` | `finalization_state.json` |
| `3af05e5fda4238ecce247da1af845879` | `finalization_journal.jsonl` |
| `56dd7a7bca4306d9224aec0ef52efa32` | `engine/rl_after/pvc_curve_v2.json` (adopted PVC curve) |
| `40d7da7c7461024048fe48fcba5692ff` | `…/legd_derivation/out/per_entrant.json` (per-entrant) |

Also byte-unchanged vs `902bd435` (git-verified): `data/expected_boot.json`, `data/release_contract.json`,
`ui/data/board_view_working.js`, `data/model_config.json`, `data/season_state.json`, every
`engine/rl_after/ingestion/movers/movers_R*.json`, and every valuation/engine source. The **only**
production-data changes are `ui/data/movers.js` (the owner-authorised R15-R19 UI bundle, §9.1) and
`data/release_lineage.json` (the additive `release_transition` governance record, §9.3 — NOT md5-pinned or
read by any guard). **No score was applied; the score-write gate is OFF.**

### 8.5 Deviations
- **Push target.** The directive header names `ci/r19-provenance-migration`; this build continues on the
  live remote feature branch `claude/item-408-fixture-repair-e2o53i` (the branch carrying commits A–C at the
  required tip `902bd435`; `ok0mp3` from the session harness note does NOT exist on the remote). Additive
  commits D/E/F are pushed there; `ci/r19-provenance-migration` is left untouched for the supervisor.
- **Forward-lens DEFERRED (§8.2)** is a builder JUDGMENT (owner declined to rule at build time) — surfaced
  for GPT Sol 5.6 / owner ratification.
- **Final Integration fixture-portability defect FOUND + REPAIRED (§10).** The first CI run showed FI RED on
  `extract_seam.test.py`'s runtime `git show 6720dfae` — a dangling/unreachable commit (it failed in CI too,
  not just the shallow container). Repaired with a committed self-contained schema fixture; `extract_seam`
  42/42; no git/network at test time. The pinned-env board-building proofs remain CI-authoritative.
- **Commit trailers OMITTED** to match the branch's trailer-free build-seat convention (commits A–C).
- **Committed Final Integration SUITE evidence** (`session_2026-07-21/final_integration/evidence/*.json`) is
  NOT re-committed by the builder (it is CI-runtime output; the v382 ruling forbids CI writes and the local
  container cannot regenerate the board-build + `extract_seam` evidence green). The committed evidence
  predates this migration; the CI run is the authoritative regeneration + report. `movers_proof.json` (fast,
  deterministic, no board build) IS regenerated to the new test-0 (populated + provenance bridge).

### 8.6 Remaining issues
- **Forward-lens (vP1/vP2) repair** remains owner-DEFERRED (§8.2) — a future, separate owner-scoped release;
  ITEM 408 does not perform it.
- **CI confirmation pending.** The authoritative four-suite green + prescreen is the CI run on this push;
  this note records the migrated-code local verification, not a CI attestation.

### Status
**ITEM 6: COMPLETE** — the owner-authorised R15-R19 Movers history is retained and bridged fail-closed to
the current accepted release (§9); Live Scoring fast tests + movers (62/62) + browser bridge (21/21) GREEN;
production dedup unchanged; score-write gate OFF; every protected artifact byte-unchanged; no score applied.
**ITEM 7: the stale Final Integration oracles are MIGRATED** to the accepted R19 authorities with no
protected value moved (§8.1); `invariant_proof` 33/33, `season_progress` 25/25, `acceptance_matrix` no
hard-fail (forward-lens owner-DEFERRED, §8.2).

This note **does NOT unconditionally declare `READY FOR COLD BLIND REVIEW`**: (1) the authoritative
four-suite green + prescreen is the CI run this push triggers (not reproducible in this build container),
and (2) the forward-lens DEFERRED treatment (§8.2) is a builder judgment awaiting supervisor ratification.
The correction is complete and every locally-runnable check is green; READY is **recommended pending** CI
confirming all four suites green and GPT Sol 5.6 ratifying the forward-lens deferral. This note is
builder-generated evidence; the execution supervisor has not accepted it; STOP-2 is not granted; no merge,
tag, release, deployment or score-write activation is authorised.

---

## 9. Owner-ruling Movers correction (ITEM 408 Items 6–7, Option A) — retained history + provenance bridge

`[builder-generated evidence]` This section implements the owner Option A ruling (recorded verbatim at the
top of this note). It **supersedes** the §7.8 empty-bundle conclusion. Authored by the `claude-code-builder`
seat; NOT the cold blind review; no STOP-2; no merge/tag/release/deploy; score-write gate OFF.

### 9.1 Restored production Movers history (owner-authorised)
`[re-runnable]` `ui/data/movers.js` is restored **byte-exact** from `1606d13408f6ca45013e21faec2b3b6a9454f033:ui/data/movers.js`.

| state | md5 | sha256 | rounds |
|---|---|---|---|
| before (obsolete empty R14-era blob, at feature tip `902bd435`) | `83bc7b8f977ad4c08082d6ea25bb9f5b` | `121378a4…` | `[]` |
| after (owner-authorised recovery history) | `2e1edb4557509a5f057ec5e6e16b7178` | `9c6962c3a9bc86f7fe97548fb704c5ffd7bb728aceec16bb66938c7dec525a06` | `[15,16,17,18,19]` |

Preserved exactly (verified): rounds 15–19; every player row (804/round); every score; every value/rank/pos-rank
movement; before/after store + board identities; transaction ids (`txn_catchup_r15…r19`); original timestamps
(`generated_at 2026-07-21T16:17:44Z`); each report's frozen governing identity (`v2.11-present-lens-baseline`,
engine_head `dc7e34b0`, balanced `06d8af60`). The movements are **NOT** regenerated from the current board and
the historical identities are **NOT** replaced with current identities.

### 9.2 Historical board/store chain — exact + continuous (R14 → R19)
`[re-runnable]` baseline R14 board `2ab73a6f` / store `968de0c7`, then per report `board_md5_before/after` +
`source_store_md5_before/after`:

| round | store before → after | board before → after |
|---|---|---|
| R15 | `968de0c7` → `692d6302` | `2ab73a6f` → `2fe26675` |
| R16 | `692d6302` → `0b951852` | `2fe26675` → `8ad41708` |
| R17 | `0b951852` → `c312eb5b` | `8ad41708` → `0308202f` |
| R18 | `c312eb5b` → `64795076` | `0308202f` → `4323c448` |
| R19 | `64795076` → **`f37d9716`** | `4323c448` → **`92a8f3a0`** |

Continuous (each `before` == prior `after`; first `before` == baseline). The latest report **terminates at
the accepted R19 materialised store `f37d9716`** (the current authoritative store) and the recovery's R19
board `92a8f3a0`.

### 9.3 The fail-closed provenance transition (exact source → destination)
`[re-runnable]` The R15–R19 reports were generated under the earlier accepted **present-lens** release; the
application has since advanced (accepted model + balanced-board identity changes, ITEM 408 STOP-1). The
narrowest fail-closed mechanism that shows the historical reports under the **current** accepted release —
without pretending they were generated under it and without rewriting any report — is a **separately-declared,
owner-approved release transition**: canonical authority `data/release_lineage.json` `release_transition`,
mirrored byte-consistent to `ui/data/movers_transition.js` (`window.__MATCHDAY_TRANSITION__`), enforced by
`ui/app/movers.js core` (`bridge` / `matchAppToDest` / `sameId` / `reportsDigest`).

| field | SOURCE (historical reports) | DESTINATION (current app) | moved? |
|---|---|---|---|
| release_version | `v2.11-present-lens-baseline` | `v2.11-final-rc1-PROVISIONAL` | **moved** |
| balanced_board_md5 | `06d8af60…` | `1373e824…` | **moved** |
| engine_head | `dc7e34b0…` | `7c452715…` | **moved** |
| board | `92a8f3a0…` | `6f07f7cb…` | **moved** |
| rl_model | `4f776e07…` | `4f776e07…` | unchanged |
| fv | `6a9a520f…` | `6a9a520f…` | unchanged |
| config | `45b207c0…` | `45b207c0…` | unchanged |
| register | `652d83e8…` | `652d83e8…` | unchanged |
| store | `f37d9716…` | `f37d9716…` | unchanged |

The transition moves **exactly** the release presentation (release_version / balanced / engine_head / board);
the underlying R19 **store and every model pin are identical** — a legitimate re-presentation of the SAME R19
data, not a data change. SOURCE is derived from the R19 report's own identity + terminal board/store;
DESTINATION is derived from `data/expected_boot.json`. Owner-approved (`owner_approved: true`,
`owner_ruling_id: ITEM_408_items_6_7_option_A`).

**Content anchor.** `applies_to.historical_reports_digest` =
`sha256:6aea584536c6cd98c7949947620687d549b6f6f54fcc44acf3ca6fd71aaf8c4d` — a SHA-256 over the canonical
serialization of exactly the R15–R19 reports. Recomputed identically by `round_movers.canonical_reports_digest`
(Python) and `ui/app/movers.js core.reportsDigest` (browser/node) — **cross-language verified equal**. ANY
modification of a report (an identity field OR a player's movement value) changes the digest and fails closed.

### 9.4 The twelve required properties (all satisfied)
`[re-runnable]` (verified by `ui/tests/movers.test.js` 62/62 + `engine/rl_after/ingestion/test_movers_transition.py`
25/25): (1) each report retains its original fixed + dynamic identity fields (byte-exact restore; no rewrite);
(2) the R14→R19 board/store chain is exact + continuous (§9.2); (3) the latest report terminates at the accepted
R19 board/store `92a8f3a0`/`f37d9716`; (4) a separately-declared owner-approved transition connects the historical
release identity to the current application release identity; (5) it identifies exact source + destination
identities (§9.3); (6) it cannot be inferred from similar data — the full owner-approved record is required, a
matching store/board alone is insufficient; (7) an absent / partial / wrong / reversed / tampered transition
fails closed; (8) a transition cannot authorise an unrelated lineage (SOURCE must match the reports exactly);
(9) historical report contents cannot be modified without detection (per-report identity consistency + content
digest); (10) future weekly reports append under the then-current governing identity without altering R15–R19
(byte-for-byte + digest unchanged, proven via `accumulate_bundle`); (11) the browser displays R15–R19 when
loaded against the current accepted application (`state: bridged`); (12) the score-write gate remains OFF
(`APPLY_DEFAULT False`, no apply token; no score applied).

### 9.5 Fail-closed negative controls (each proven)
`[re-runnable]` `ui/tests/movers.test.js` + `test_movers_transition.py`: no transition → fail closed; wrong
SOURCE → fail; wrong DESTINATION → fail; REVERSED (source↔destination) → fail; not owner-approved → fail;
modified historical report **identity** → fail (per-report consistency + digest); modified player **movement**
data → fail (digest); modified board/store **chain** → fail; **unrelated release lineage** → fail (source
mismatch); current-application board ≠ destination → fail. Positive: owner-approved transition ⇒ `state:
bridged`; current application identity == transition destination; future append preserves R15–R19 byte-for-byte.
No wildcard / "accept any previous release" path was added; generic lineage validation was **not** weakened.

### 9.6 No historical report rewritten; no score applied; protected artifacts untouched
`[re-runnable]` The restored bundle is byte-identical to `1606d134:ui/data/movers.js`; the reports are read-only
data the transition anchors, never regenerated. Protected artifacts are byte-unchanged by this correction
(measured before/after — see §F close table): R19 store `f37d9716`, board of record `6f07f7cb`, balanced/strict
`1373e824`, per-round movers outputs `engine/rl_after/ingestion/movers/`, score ledger, histories. `movers.js`
(the UI shipping bundle) and the new transition files are the only production-data changes; the score-write gate
is OFF and **no score was applied**.

---

## 10. Final Integration fixture-portability repair (authorised narrow infrastructure repair)

`[re-runnable]` Authored by `claude-code-builder` under GPT Sol 5.6; authorises no valuation, scoring,
release-policy or protected-artifact change.

### 10.1 Observed failure
On the first four-suite run of the migrated candidate, **CI Guards, FV Provenance and Live Scoring were GREEN;
Final Integration was RED** (run `30051576666`, 51 s). Steps 1–12 passed — including the migrated
`invariant_proof.py` **33/33** (present-lens vs `reference_vector_1373e824`; forward-lens DEFERRED) and
`season_progress`. FI failed at step 13 "UI seams", first command `python3 ui/tests/extract_seam.test.py`:
`[FAIL] read diagnostic candidate fixture from 6720dfae … cannot read fixture; aborting` (exit 1). The
remaining FI steps (clean-room rebuild, generated-bundle equality, R15 ladder, season advance,
acceptance-matrix) were **skipped**.

### 10.2 Root cause — unreachable historical fixture
`extract_seam.test.py` read its schema fixture at test time via `git show
6720dfae438ec4eef87a956d63ee4468c05105f4:recovery_artifacts/v2.11/post_legf_candidate/rl_app_data.json`. That
commit is **dangling in GitHub's object database but is NOT reachable from any advertised branch or tag**, so
`actions/checkout` `fetch-depth: 0` cannot supply it (`git fetch origin 6720dfae` → "couldn't find remote ref").
An executable **test-fixture portability defect** — unrelated to the ITEM 408 oracle migration, which passed.

### 10.3 Repair — committed, self-contained fixture (no git / network at test time)
`[re-runnable]` New committed fixture **`ui/tests/fixtures/extract_seam_legf_schema.json`** (56 KB), derived
from the authentic source blob (fetched once at build time via the GitHub Git-Database blob API; **the
committed test performs NO fetch / API call / git access**). `extract_seam.test.py` now loads the committed
fixture directly and stages it as a temporary board; it no longer depends on `git show`, commit `6720dfae`,
remote-branch availability or network. `final-integration.yml` is unchanged (it never claimed the dangling
commit was reachable; it adds no fetch for `6720dfae`, per the repair scope). Production `data/rl_build/
rl_app_data.json` is NOT used as the fixture — the test stays isolated from the live board.

### 10.4 Fixture source + blob identity (recorded in the fixture's `_fixture_provenance`)
- **source commit:** `6720dfae438ec4eef87a956d63ee4468c05105f4`
- **source path:** `recovery_artifacts/v2.11/post_legf_candidate/rl_app_data.json`
- **source blob SHA-1:** `e119b9e34bf3ff1e415a41d8150034e437e25d62` (verified: `git hash-object` of the
  API-fetched 1,229,049-byte source == this SHA)
- **statement:** a REDUCED SCHEMA FIXTURE, **not** a production board or accepted valuation oracle.

### 10.5 Reduction method (authentic, minimal)
Only the keys `extract_board_view.py` reads are kept, byte-for-byte from source; the ~40 engine-parameter keys
the extractor never reads are dropped; no value is fabricated or recomputed: `active[:30]`, `back[:5]`,
`picks[:5]`, `PVC` (full), `lensPicks[:8]`, `lensConservation` (full), `phantomLayer` (3 clubs), `phantomPicks[:8]`,
`phantomTotals` (`_meta` + `league` + the 3 kept clubs), `BASE_YEAR`. The sealed `phantomTotals._meta` is
preserved verbatim — **`entrant_layer_pvc 83538`, `expected_slots_per_year 103.43`, `seal_sha256_8 a17aafed`**.
The reduced set preserves active-player pass-through, non-empty `phantomLayer`/`phantomPicks`/`phantomTotals`,
`lensPicks`, `lensConservation`, and working/public field separation.

### 10.6 Result
`[re-runnable]` `extract_seam.test.py` → **42/42 PASS** locally (was 41; +1 committed-fixture validity check;
no extractor assertion weakened or removed). No protected artifact changed; no score applied; gate OFF. The
post-repair CI four-suite conclusions on the final SHA are recorded in the hand-back / §8.3 (this note is
updated once CI attaches to the new tip).

`[re-runnable]` **Post-§10 CI (SHA `5acbccf`):** CI Guards **success**, FV Provenance **success**, Live
Scoring **success**; Final Integration advanced PAST extract_seam (step 13 UI seams + step 14 asset-view UI
both green) and surfaced a SECOND, different first-natural failure — see §11.

---

## 11. Final Integration responsive-UI 320px repair (authorised narrow responsive-UI acceptance repair)

`[re-runnable]` Authored by `claude-code-builder` under GPT Sol 5.6; authorises no valuation, scoring, model,
board, store, provenance-policy or protected-artifact change.

### 11.1 Second Final Integration first-natural failure
With extract_seam repaired (§10), Final Integration on SHA `5acbccf` cleared step 13 (UI seams;
`extract_seam` 42/42) and step 14 (unified asset-view UI 40/40) and failed at **step 15
`ui/tests/responsive_layout.test.mjs`** (run `30060925214`). Steps 16–21 (bootstrap, clean-room rebuild,
generated-bundle equality, R15 ladder survival, R14→R19 season advance, acceptance matrix) were **skipped**.

### 11.2 Exact 320px symptom
`71/72` responsive assertions passed; per-width `320:11/12 360:12/12 390:12/12 430:12/12 720:12/12
1440:12/12`. The single failure: at the **320px** viewport the Board view's 5th-ranked player name
**"Nasiah Wanganeen-Milera"** (a long hyphenated real name) rendered in **3 text lines** in the ~171px
condensed uppercase name column — the assertion `names render in <= 2 text lines` requires ≤2. It is a
**Board**-view typography issue, not Movers. Reproduced locally byte-for-byte (playwright-core 1.47.2 +
`chromium_headless_shell`): `1L 1L 1L 1L 3L`.

### 11.3 Proof the defect pre-dated ITEM 408
`[re-runnable]` `ui/styles/matchday.css`, `ui/data/board_view_working.js`, `ui/data/board_view_public.js`
and `ui/tests/responsive_layout.test.mjs` are **byte-identical from the ITEM 408 base `902bd435` through
`5acbccf`** (`git diff 902bd435 5acbccf -- <path>` empty for each). No ITEM 408 commit touched the board
typography, board data or the responsive test; this repair is the FIRST edit to `matchday.css`. The defect
was latent — never *reached* in CI before, because Final Integration previously failed at earlier steps
(extract_seam, R14/present-lens oracle reds).

### 11.4 The CSS repair (measured; generic; narrowest)
`[re-runnable]` A single `@media(max-width:360px)` block reducing ONLY the board name element at the two
smallest phone widths:
```
@media(max-width:360px){
  .row.working .nm,.row.public .nm{font-size:15px;letter-spacing:0}
}
```
Placed after the existing `max-width:560px` block so it wins at ≤360px by source order. **Measured** (320px,
playwright-core): `letter-spacing:0` alone → still 3 lines; **`font-size:16px→15px` + `letter-spacing:.02em→0`
→ 2 lines** (the narrowest combination that works). It changes **nothing** at ≥390px (normal mobile) or
desktop, is **name-generic** (no Nasiah special-case, no `<wbr>`, no per-name rule), keeps the **full name**
(no truncation / ellipsis / hiding), does not touch the board data, and introduces no horizontal document
overflow. Name column width stays 171px (≥50px). All other required fields (rank/name/club/value/movement,
nav reachability, containment) preserved. The existing real-board assertion is **NOT** weakened, removed or
special-cased, and the assertion count stays **72** (no synthetic assertion added — the existing real-board
first-five-name assertion already exercises the long hyphenated name at 320px and is the regression guard).

### 11.5 Before / after responsive results
| | 320px | 360 | 390 | 430 | 720 | 1440 | total |
|---|---|---|---|---|---|---|---|
| before (5acbccf) | 11/12 (Nasiah `3L`) | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 | **71/72** |
| after (this repair) | **12/12** (Nasiah `2L`) | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 | **72/72** |

### 11.6 Local validation + result
`[re-runnable]` `responsive_layout.test.mjs` **72/72** (12/12 at 320px); `asset_view_ui_check.mjs` **40/40**
(no regression from the CSS); `extract_seam.test.py` **42/42**; `invariant_proof.py` **33/33**;
`season_progress_test.py` **25/25**; `acceptance_matrix.py` **OVERALL PASS** (forward-lens DEFERRED);
`movers.test.js` **62/62**; `test_movers_transition.py` **25/25**. Protected artifacts byte-unchanged; no
score applied; gate OFF. Post-repair CI four-suite conclusions + confirmation that every Final Integration
step executed are recorded in the hand-back.

---

## Signature

**SIGNED — GPT Sol 5.6 final independent STOP-1 review, 2026-07-23.**

`[re-runnable]` GPT Sol 5.6 independently reviewed the live remote branch at atomic STOP-1 commit
`348d0ff715d1a98f0ebc47d2a9cc2d32efde0d80`. The branch resolves exactly to that commit; it is one fast-forward
child of pre-STOP-1 tip `ffd49047b8b0d9904dd7a69ea7019e67ee5830df`; and its diff contains exactly the six
authorised STOP-1 paths.

The balanced/strict identity movement `06d8af60b679a12db07c064c60c065f9` → `1373e82471a81064ef96820f3db065df`
is accepted. The dependent boot, release-contract, present-value aggregate, FV oracle/reference-vector and
working UI identities move coherently. The release-contract seal independently recomputes to
`4fdf3c10cee885bd7f57f8ef41e8a9fb3ee7d837c768a8e438f6ab41e6d1600e`.

The board of record remains `6f07f7cbe042f8e56426a01226c967c9` and was not replaced. The authoritative store,
frozen curve, curve contract, per-entrant artifact, score ledger, model/config/season state, workflows and
open-items register are outside the changed-file set and remain untouched by the STOP-1 commit.

Verdict: STOP-1 execution ACCEPTED.

This signature is limited to the rebuilt pre-STOP-1 work and the atomic STOP-1 execution. It does not assert
final four-suite acceptance: the suites are not yet all green, ordered work items 5–7 remain open, and the
commit has no GitHub CI attestation. STOP-2 remains exclusively owner-held and pending. No merge, tag, release,
deployment or score-write activation is authorised by this signature.
