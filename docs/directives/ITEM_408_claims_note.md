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
build depends on them. This note does **not** assert final four-suite acceptance; the suites are not green and
STOP-1 is unresolved.

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
post-rebuild. They are the CI-Guards / club-curve red of section 2. Re-aiming CASE1 at the manifest of record
is the STOP-1-gated advance-repin (directive item 5) — `expected_boot.json`'s balanced-board pin is still
`06d8af60` and may not move before owner approval — so it is out of this pre-STOP-1 rebuild's scope.

## 5. R19 balanced-board regeneration and STOP-1

Filled by rebuild commit 4 ("ITEM 408: build R19 STOP-1 candidate evidence"). **No** balanced-board pin or
artifact moves before the owner views the measured comparison and gives explicit STOP-1 approval.

## 6. Advance-repin design

`[report-only]` Not performed in this mechanical rebuild. The round-advance scripted regeneration/repin design
is directive work item 5, owner-scoped, out of the rebuild's hands.

## 7. Live Scoring diagnosis and repair

`[report-only]` Not performed in this mechanical rebuild (directive work item 6). Recorded here only as an open
exact-head red (section 2).

---

## Signature

**Status: PENDING GPT Sol 5.6 INDEPENDENT REVIEW.**

The mechanical builder does not sign. GPT Sol 5.6 independently reviews the four rebuilt commits and their
evidence and is the sole signer. The owner separately holds STOP-1 approval, pin/board movement, and merge.
