# ITEM 408 · D2 — COLD REVIEW OF THE FORWARD-LENS ADVANCE INTEGRATION (PARTIAL)

**Filed by the supervisor pen (seam) · 2026-07-27 · register v482**

## Provenance header

- **Reviewer:** `d2-cold-review` — a bare cold seat with no prior context, opened under v427
  isolation, implementer ≠ reviewer ≠ supervisor, mandatory under **D2 §3** because the work
  modifies the production advance path.
- **Subject:** `ci/item-408-d2-staging @ dd117adfe0f0a0e77f05ab82ae0cd725e18bfaa0`, eight
  build-seat commits atop the D2 pin `1a2b1933a663492c05c6a20b6be0f497655ddb48`.
- **Verdict as returned:** **HONEST-INFEASIBLE (PARTIAL).** Mandate items 2, 3 and 8 verified by
  re-run and passing; items 1, 4, 5, 6 not reached; item 7 partial. No merge-blocking finding on
  anything reached. One hardening note.
- **How this text reached the record:** owner-couriered into the seam channel on 2026-07-27,
  reproduced below as received.
- **Seam verification and the routing rulings** — including the pen's own extension of the
  centrepiece analysis, the sharpened reading of the hardening note, and the item-7 disposition —
  are at **register v482**. This document is the deliverable; the register carries the adjudication.
- **Precedent for the shape:** the ITEM 408 cold chain ran partial (v421) → continuing (v428) →
  final narrow pass (v446/v448). A cold seat that refuses to convert "consistent with everything I
  checked" into CLEAR is behaving exactly as this house requires.

> One sentence from the owner corrects any part of this filing if misstated.

---

## VERBATIM AS RECEIVED

**COLD REVIEW REPORT — ITEM 408 D2 FORWARD-LENS ADVANCE INTEGRATION**

Reviewer: d2-cold-review (cold seat, no prior context)
Subject: `ci/item-408-d2-staging @ dd117adfe0f0a0e77f05ab82ae0cd725e18bfaa0`,
github.com/lukemcalister10/afl-rl-engine
Authority: D2 §3 (modifies the production advance path)
Date of pass: 2026-07-27

### VERDICT

**HONEST-INFEASIBLE (PARTIAL).** Mandate items 2, 3 and 8 are verified by re-run and all pass.
Items 1, 4, 5, 6 were not reached; item 7 is partial. No merge-blocking finding on anything reached.
One hardening NOTE is filed below.

I am not signing CLEAR or CLEAR-WITH-NOTES. Roughly half the mandate is unexecuted, and a clean
verdict would be strongest exactly where the evidence is thinnest. This is a partial pass to be
completed, not a disposition.

### 1. PROVENANCE AND TOPOLOGY — VERIFIED

Repository is public and reachable; the filed record is accurate in every checkable particular.

```
git rev-parse origin/ci/item-408-d2-staging
  -> dd117adfe0f0a0e77f05ab82ae0cd725e18bfaa0
git merge-base dd117ad 1a2b1933
  -> 1a2b1933a663492c05c6a20b6be0f497655ddb48      (base is exactly as filed)
git rev-list --count 1a2b1933..dd117ad
  -> 8                                             (all authored code-hands-408-d2)
git merge-base --is-ancestor dd117ad origin/main
  -> NOT merged into main
```

Code-only known-known confirmed. `git diff --stat 1a2b1933..dd117ad` = 6 files, 1658 insertions, 31
deletions: `forward_lens.py`, `scratch_fixture.py`, `sibling_repin.py`, `staged_apply.py`, and the
two harnesses. No data, no board artifacts. Reality matches the disclosure.

### 2. ENVIRONMENT — FRESH AND PINNED

```
bash setup_env.sh
  -> setup_env PASS  (py numpy scipy sklearn openpyxl) = 3.12.3 2.4.4 1.17.1 1.8.0 3.1.5
bash bootstrap.sh
  -> bootstrap OK
  -> Guard 5 PASS: store f37d9716 == pinned f37d9716
                 | rl_model 4f776e07 == pinned | fv 6a9a520f == pinned
```

**Reviewer error, recorded for integrity.** My first run failed on
`ModuleNotFoundError: No module named 'unidecode'` and I began drafting it as a pin-completeness
finding. That was my mistake, not the branch's: `unidecode` is vendored (`vendor/unidecode`) and
seeded by `bootstrap.sh`; I had run only `setup_env.sh`. There is no pin defect. Withdrawn before it
reached a verdict, but noted here so the supervisor does not inherit a phantom.

### 3. THE CONFORMANCE GATE (mandate item 2) — PASS, re-run, at the filed figures

```
[PASS] D0 authorities of record verified — config=45b207c03a8c
       posture={'RL_PVC2':'1','RL_LEGE':'1','RL_LEGF':'1'} f5_seal=a17aafed
[PASS] D0 store UNCHANGED vs manifest of record — store=f37d9716 manifest=f37d9716
[PASS] D0 config-of-record rebuild reproduces the SHIPPED board identity
       — rebuilt=6f07f7cb shipped=6f07f7cb manifest=6f07f7cb
[PASS] D0 CONFORMANCE +1 lens: regenerated == shipped vP1 for EVERY player
       — cohort_identical=True per_player_diffs=0 sum=705057/705057
[PASS] D0 CONFORMANCE +2 lens: regenerated == shipped vP2 for EVERY player
       — cohort_identical=True per_player_diffs=0 sum=656811/656811
[PASS] D0 CONFORMANCE +1/+2 conservation rows == shipped lensConservation
       — nPlayers: 804, nPicks: 64, picks: 64617, players: 705057 / 656811
[PASS] D10 no hardcoded historical board id in the new forward path — hits=[]
[PASS] D10 forward filenames derive from the manifest's CANONICAL board
       — board=6f07f7cb (balanced pin 1373e824 deliberately NOT used)
[PASS] D1 plan WROTE NOTHING (build-and-compare only) — 0 file(s) differ
[PASS] D2 forward view is the FULL two-lens vector over the exact active universe
[PASS] D2 the regenerated forward ORACLE runs green standalone
```

All four filed conformance figures independently reproduced: Σ vP1 705,057 · Σ vP2 656,811 · 804
active · board `6f07f7cb` byte-identical.

I also read the gate rather than trusting its label. It is genuinely per-player —
`diffs = sorted(k for k in sa if int(sa[k][fld]) != vec.get(k))` — and raises `SystemExit` before any
changed-data case. It cannot be satisfied by agreeing sums alone.

### 4. THE NAMED CENTREPIECE, v477 (mandate item 3) — VERIFIED

This is the item the gate structurally cannot see, and it is the reason the seat exists.

#### 4a. Mode parity — divergence found, and it is benign

There are exactly two call sites of the shared `derive_forward`: `sibling_repin.py:399` (gate path)
and `sibling_repin.py:449` (production attach). The docstrings name different modes —
`RL_CONFIG_MODE=canonical` at line 356 versus `RL_CONFIG_MODE=gate` at line 416 — and
`FORWARD_CONFIG_MODE = "canonical"` (`forward_lens.py:62`). So two differently-moded boards do feed
one `derive_forward`. That is the declared failure class, and it resolves in the branch's favour:

`config_manifest.enforce()` gates on `if mode not in ('bake','gate','canonical'): return None`
(line 84). Within that fenced set, `mode` is used only for the membership test and two message
strings (lines 128, 145). The reject scan, the `SGC_*` seam scan, the boot-pin check, and the
clear-and-load all read `cvars = man['vars']` from the same `data/model_config.json`. No branch gives
`gate` a different posture from `canonical`.

| Axis | Gate path | Production path | Parity |
|---|---|---|---|
| `derive_forward` args | `(board, md5, present_vector=present)` | `(board, got, present_vector=present)` | identical |
| `present_vector` build | `{p["key"]: int(p["v"]) for p in board["active"]}` | identical expression | identical |
| ambient `RL_*`/`PAR_*` cleared | yes (373–376 + builder:96) | yes (staged_apply:1033) | identical |
| `PYTHONHASHSEED` | 0 (builder:99) | 0 (staged_apply:1038) | identical |
| BLAS thread pins | 1 ×4 (builder:100) | 1 ×4 (staged_apply:1039–40) | identical |
| `SGC_*` seam scan armed | yes (builder:109 sets ambient mode) | yes (staged_apply:1037) | identical |
| manifest-load proof | literal (canonical mode) LOADED in stdout | literal (gate mode) LOADED in stdout → bool → fail-closed | equivalent |

Two specific concerns I carried into the review, both discharged:

**Determinism env asymmetry** — none. Both pin `PYTHONHASHSEED` and all four `*_NUM_THREADS` because
the gate path routes through the shared builder `test_fv_provenance.py:99-100`, which pins them
itself.

**`manifest_loaded` as caller convenience** — it is not. `staged_apply:1129` computes
`config_mode_gate_loaded` from the build's own stdout, threads it through `:537`, and
`attach_forward_from_board:428` fail-closes on it.

#### 4b. The md5 pin fails closed — 6/6

Direct exercise of the guards against the live board (no rebuild required):

```
board md5 : 6f07f7cbe042f8e56426a01226c967c9   bytes=1256166   active cohort=804

[PASS] (a) md5 pin tampered      -> SiblingBuildError: canonical board for the forward view
                                    is 6f07f7cb but the transaction staged 00000000
[PASS] (b) manifest_loaded=False -> SiblingBuildError: refusing to derive the forward view
                                    ... did not report loading the config manifest
[PASS] (c) board file missing    -> SiblingBuildError: canonical board missing for the forward view
[PASS] (d) cohort mismatch       -> SiblingRepinError: cohort differs at 1 key(s)
                                    (e.g. ['nick-daicos']) — G-COHORT
[PASS] (e) board bytes tampered  -> SiblingBuildError: canonical board for the forward view
                                    is 9cd75770 but the transaction staged 6f07f7cb
[PASS] CONTROL — honest attach SUCCEEDED
        +1 sum = 705057   +2 sum = 656811   active = 804
        auth.source = the transaction's own gate-mode canonical build (no second rebuild)
RESULT: 6/6
```

(e) is the load-bearing one: a real byte flip in the board, caught on identity rather than shape. The
control is present so the guards cannot pass merely by raising at everything — and it independently
re-lands the filed sums a second time by a different route.

### 5. SUITE MAP FROM THE ACTIONS API (mandate item 8) — COMPLETE

Pulled directly from the API on `dd117ad`, not from a filed summary:

```
total_count: 4   (head_sha=dd117adfe0f0a0e77f05ab82ae0cd725e18bfaa0)
  FV Provenance         completed  success  push  2026-07-26T13:10:19Z
  Final Integration     completed  success  push  2026-07-26T13:10:19Z
  CI Guards             completed  success  push  2026-07-26T13:10:19Z
  Live Scoring Updater  completed  success  push  2026-07-26T13:10:19Z
```

Cross-checked against the tree at that commit: 4 workflow files exist (`ci-guards.yml`,
`final-integration.yml`, `fv-provenance.yml`, `live-scoring.yml`), all triggered on
push/pull_request. 4 exist, 4 ran, 4 green, none skipped.

### 6. PROTECTED SET + STORE 0-DIFF (mandate item 7) — PARTIAL

Store 0-diff by exact path, with real byte counts:

```
engine/rl_after/rl_model_data.json          bytes: 1530130
  branch  f37d9716648cfe4382b8c6a24c4f064f
  base    f37d9716648cfe4382b8c6a24c4f064f  bytes: 1530130
data/rl_build/rl_app_data.json              bytes: 1256166
  md5     6f07f7cbe042f8e56426a01226c967c9
md5(empty) = d41d8cd98f00b204e9800998ecf8427e
  -> neither hash matches the empty-input sentinel; real bytes were hashed
```

Store is byte-identical to base — 0-diff confirmed on the exact path.

**Not verified:** the protected set. `grep -rni 'protected'` returns nothing across
`engine/rl_after/ingestion/*.py`. It is either named differently in this codebase or lives outside
the branch surface. I could not resolve it and am not going to claim it.

> **Pen note, register v482:** the protected set is a **named list** in the D2 directive §3 and
> register v442 — the frozen pick curve, the curve contract, `per_entrant.json` and the store — not a
> code keyword. The pen re-verified all four 0-diff at this branch, so the property is not in doubt;
> the mandate line stays the reviewer's to discharge.

### 7. NOTE FOR THE OWNER — hardening, not a defect

`attach_forward_from_board` sets `auth["config_manifest_loaded"] = True` unconditionally at
`sibling_repin.py:447`. It records **that** a manifest loaded, not **which mode** was proven.

As shipped this is correct: the sole caller derives the boolean from a real gate-mode stdout. The
narrow exposure is that the function fail-closes on the caller's boolean without verifying the mode
itself, so a future second caller passing `manifest_loaded=True` from a non-fenced build would be
accepted, and the evidence record would not preserve the difference.

Cheap fix: pass the mode string through and assert membership in the fenced set, mirroring the check
at line 390.

Flagged because mode divergence is the declared blind spot of the conformance gate, and this is the
single place in the centrepiece where the branch takes it on trust rather than on proof.

### 8. NOT DONE — nothing in this section is verified

| Item | Status |
|---|---|
| 1 — both harnesses to full count (33/33, 73/73) | NOT DONE — harness 1 reached 17 checks, all PASS, then reaped |
| 4 — negative controls on live key names | NOT DONE |
| 5 — atomicity, injected mid-transaction fault, zero targets moved | NOT DONE |
| 6 — P13/P15 scratch-relative, fail-on-corruption preserved | NOT DONE |
| 7 — protected set | NOT DONE (store portion verified, §6) |

The three disclosed reds, the P2/P8 harness vacuities, and Board B (`70ef0ff`) were not reached; I
can say nothing about them either way. Forward valuation MATH was correctly not touched — this pass
integrates the view only.

**Tool limits, reported not papered:**

*Compute.* Review container is `nproc=1`. Each config-of-record board build runs ~4–6 minutes and
both harnesses require many. Full 33/33 + 73/73 plus tamper, negative, and atomicity passes is on the
order of hours of single-core time.

*Process reaping.* Background jobs are killed at tool-call and turn boundaries. Plain `nohup ... &`
dies silently with no traceback — I initially misread this as a crash. `setsid` survives call
boundaries but not turn boundaries. Whoever completes this should use a runner without per-call
reaping.

**Recommendation:** re-task on a multi-core runner with persistent processes, or split into per-item
passes. Start at items 5 and 4 (atomicity and live-key negative controls) — items 2, 3 and 8 are now
evidenced and re-running them is the cheapest way to look thorough while learning nothing new.

Signed: **d2-cold-review**

Disposition: partial pass; no merge-blocking finding on items reached; one hardening note; merge gate
remains held pending items 1, 4, 5, 6, 7 and the separate item landing first.

---

*End of verbatim text. Adjudication, the pen's extension of the centrepiece analysis, the sharpened
reading of the hardening note, and the routing rulings are at register v482.*
