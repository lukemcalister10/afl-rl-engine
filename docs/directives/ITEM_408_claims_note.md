# ITEM 408 — R19 provenance migration claims note

- **Supervising build seat / sole signer:** GPT Sol 5.6
- **Mechanical builder (repository hands only):** Claude Code — no interpretive or sign-off authority
- **Owner / sole STOP-1 and merge authority:** Luke McAlister
- **Branch:** `ci/r19-provenance-migration`
- **Exact rebuild base:** `83ed3bb1606b708af16a2ad90a26d63553de6789`
  (`origin/ci/harness-migration-r19-phase2-cand` tip — "harness(one-source): refresh Kako 2026 pin to 10 games @ 45.4")

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
no literal `804` (blocking-issue 4).

`[re-runnable]` **Pinned environment.** Every board build ran in the accepted pinned environment
(`/root/rl_venv312`: Python 3.12.3 / numpy 2.4.4 / scipy 1.17.1 / scikit-learn 1.8.0 / openpyxl 3.1.5;
`PYTHONHASHSEED=0`, single-thread BLAS, `RL_PVC2=1/RL_LEGE=0/RL_LEGF=0`, bootstrap-seeded workspace, ENV-PIN
byte-exact numpy + bundled OpenBLAS `05c9f9eb`). FV provenance GREEN1 reproduces the accepted balanced board
`1373e824` / 804 / 760253 / 9542 / 0 movers under this env.

### 6.c Evidence (all re-runnable; scratch/fixtures only; NO real score apply; gate OFF)

`[re-runnable]` **Single-transaction integration** — `session_2026-07-23/item408_sibling_repin/staged_sibling_integration_proof.py`
→ **46/46 PASS** (the original 28 checks RETAINED; 18 controls ADDED for the 2nd blocking correction; scratch only; gate armed IN-PROCESS against the scratch only):
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

`[re-runnable]` **Supporting suites (re-run this container; pinned venv `/root/rl_venv312`):** FV provenance
**8/8 PASS** (GREEN1 reproduces `1373e824` / 804 / 760253 / 9542 / 0 movers; RED2/RED3 halt fail-closed with the
named FV loaded-path / checkout-drift reason); `one_source_selftest.py` (CI Guards) **PASS** (single source;
guards 1-3; board==engine F1; book==board F2; frozen-ruler STAMP re-scope), run after the standard CI-Guards
board+book bootstrap; club-curve CASE1 **35/35** (all 18 negatives fail-closed); `release_contract check` **PASS**
(seal `4fdf3c10cee8`); `sibling_repin.py check` **CURRENT** and `check --full` **CURRENT** (build-and-compare
rebuilds `1373e824`); `sibling_repin_proof.py` **26/26** (standalone reconcile build/derive/stage/validate/commit/
rollback/idempotence/repair, incl. the `changed_targets` fix). Frozen artifacts at accepted md5s (board of record
`6f07f7cb`, store `f37d9716`, curve `56dd7a7b`, curve contract `676ad2b7`, per_entrant `40d7da7c`).

`[report-only]` **`advance_chain_proof.py` is a RETAINED harness for the WITHDRAWN two-step design and now
measures 11/14** (was reported 14/14). Its CHAIN(1)/CHAIN(2)/CHAIN(3) checks assert the pre-fold-in flow —
`balanced_board_md5` STALE after `apply_snapshot`, the gate STALE, and a follow-up `reconcile` reporting changed.
Under the folded-in architecture at `aa55e29` the sibling advances INSIDE the `staged_apply` transaction, so the
siblings are NOT stale after an advance and the follow-up `reconcile` is a correct NO-OP — those three checks are
obsolete. This is INDEPENDENT of the 2nd blocking correction: re-running the harness at CLEAN `aa55e29` (the two
corrected modules stashed to their `aa55e29` bytes) yields the SAME 11/14 with identical failures
(`new=e4687458` / `sumv=759783`), so the prior `14/14` was a stale carry-over from the two-step commit `99bccb2`.
The AUTHORITATIVE end-to-end evidence for the folded-in design is the 46/46 single-transaction suite above. The
harness file and its committed `ADVANCE_CHAIN_RESULTS.json` are left byte-unchanged (out of this correction's scope).

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

## 7. Live Scoring diagnosis and repair

`[report-only]` Not performed in this mechanical rebuild (directive work item 6). Recorded here only as an open
exact-head red (section 2).

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
