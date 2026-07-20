# RELEASE / ARTIFACT MAP — v2.11 (read-only reconciliation)

Date: 2026-07-20 (Australia/Sydney) · Supervisor: ChatGPT · Builder: Claude Code · Owner: Luke McAlister
Scope: **read-only.** No pipeline was run, no container retried, no model refit, no engine/store/UI/artifact
changed. Every hash below was computed from committed Git objects (`git cat-file blob … | md5sum`) unless
explicitly labelled a *prose claim*. Prose in directives/handovers/register is treated as a claim to verify.

---

> ## ▲ SUPERSEDING UPDATE — HALT RESOLVED (2026-07-20, `release/v2.11-rc1`)
>
> **This read-only map was correct at the time and its HALT (§G) is now RESOLVED by new evidence.** Nothing
> below is deleted; the original findings stand as the historical record. Under the owner's **Option 1**
> ruling, the release candidate `release/v2.11-rc1` was assembled from `df5066a`.
>
> The single blocker was §B.2 / §G: the board of record `06d8af60` existed **only as an 8-char prose prefix**,
> not as committed bytes. That gap is closed:
>
> - **`06d8af60` is now committed, byte-recoverable content** — commit
>   `7c6768ee51adc2cf939ffa18f620bbec1d6b4249`, path
>   `session_2026-07-20/root_cause_109_wobble/cross_host_gate/fixtures/reference_06d8af60.json`,
>   Git blob `e546ab0b1033af2b8e4331e66899d14245ef3b58`, **full MD5
>   `06d8af60b679a12db07c064c60c065f9`** (active 804 / Σv 752,427 / Sheezel 7,964 — verified). This is the
>   missing-evidence item named at §F.1 / §G.1 / §U2, and it resolves §U1's "full MD5 UNKNOWN" for `06d8af60`.
> - **§U6 resolved from bytes:** `270a2c5f` vs `06d8af60` are byte-identical when sorted by key — **0 value
>   movers**, identical value-ranking; they differ **only in the `active` row order** (697 rows), exactly the
>   register's "parity 0/804, 697 rank movers". `06d8af60` is the current-engine (`cc626d7d`/`904722cd`) row
>   order; `270a2c5f` was the superseded #109-engine order.
> - **Reproduction gate met (§G.3):** the FV-provenance suite GREEN1 rebuilds the balanced board
>   (`RL_PVC2=1 RL_LEGE=0 RL_LEGF=0`, pinned env, accepted `RL_FV`) byte-identical to `06d8af60`, 0 movers.
> - **Provenance root cause fixed:** `df5066a` (fail-closed forward-valuation import provenance) closes the
>   stale-`distribution_pricing.py` hole behind the `06d8af60 → d7a95e8d` wobble (§B.6/§F long-term item).
>
> **What the RC does:** installs the exact `06d8af60` bytes at `data/rl_build/rl_app_data.json` (§B.1 file),
> re-stamps the two stale engine pins to their already-committed source (§D: `engine_head → 904722cd`,
> `rl_model → cc626d7d`), and moves `board 270a2c5f → 06d8af60`. Board and engine provenance are now coherent,
> closing the §D "Guard-5-green but internally incoherent" caveat (§F C2). It does **not** ship the stale ACT-2
> `270a2c5f`, and does **not** adopt a freshly generated board (the fresh build is a reproduction test only).
> No valuation formula, engine data, player value, or ranking changed. Full evidence + hashes + test/CI run IDs:
> `docs/RELEASE_CANDIDATE_v2_11.md`. Restrictions unchanged: no merge/tag/release/public-deploy/valuation change.

---

## 0 — Method & anchors (verified)

- Immutable checkpoint `checkpoint/pre-chatgpt-v2.11` = `612d4c058560568b3d4d49ecd785759931885081`.
  `main` and `recovery/v2.11` both point at this same SHA (verified `git rev-parse`).
- The checkpoint is a **clean, self-consistent v2.10 captaincy state** — NOT the v2.11 candidate:
  board file `data/rl_build/rl_app_data.json` md5 = `790136a380b56ebdf5db2874b6f354de`, store
  `b1fd0bced30baa838325814c39d43233`, engine `_merged_recover.py fc7045d6` / `rl_model.py f79fc740`;
  every `data/expected_boot.json` pin matches its file (Guard 5 passes, per the session-start hook).
- **None of the v2.11 candidate lineage is merged into `main`** (verified: `git merge-base --is-ancestor`
  returns false for #109/#119/#121/#123/#125). All eleven named PRs are **open**.
- Pin→file mapping (from `boot_guard.py`): `board`→`data/rl_build/rl_app_data.json`;
  `store`→`engine/rl_after/rl_model_data.json`; `rl_model`→`engine/rl_after/rl_model.py`;
  `engine_head`→`engine/rl_after/_merged_recover.py`; `q97m`→`data/q97m.pkl`; `band`→`cm_400.pkl`;
  `v0surf`→`data/v0surf.pkl`; `register`→`LTI_REGISTER.md`; `config`→`data/model_config.json`.
- The **bake base named by every current directive is `3055ea5` (PR #123 head).** All byte inspection of
  the "candidate head" below is at `3055ea5` unless noted.

---

## A — Candidate lineage (exact, ordered; SHAs and parents from Git, not PR metadata)

The stack is a **clean linear chain** — for every PR the base-branch tip equals the merge-base (verified),
so there is no divergence/rebase drift. `data/rl_build/rl_app_data.json` md5 is shown per head to expose the
frozen board.

| PR | branch (head) | base full SHA | head full SHA | parent | substantive contribution (verified) | req. for v2.11 | evidence-only | superseded | unresolved |
|----|---------------|---------------|---------------|--------|-------------------------------------|----------------|---------------|------------|------------|
| **#109** | claude/legd-pvc-rederivation-act2-l2hqpl | `33c8b52cb7a38d5fda2ceff5d3fb96841575c2e7` (r1067 #105 head) | `e4177c21934148c19d9cec3c015fee5d28480102` | child of base (mb==base) | Leg-D PVC re-derivation (RL_PVC2, ev-channel). **Last commit that wrote the board file** (`270a2c5f`) and last that stamped `expected_boot`'s engine pins (`a5fd3d7d`/`40f43772`). Engine: `_merged_recover.py`, `rl_export.py`. Store **not** touched (already `968de0c7`). | YES (lineage root) | no | no | board `270a2c5f` frozen here; never regenerated downstream despite engine advancing |
| **#111** | claude/five-migration-pvc-consumers-kxykfd | `e4177c21…` | `a90052add8570c014626196cc2e3e13eece02548` | child (mb==base) | Leg-D Build B: MA.PVC consumers → `pvc_curve_v2.json` (`56dd7a7b…`). Engine `rl_model.py` only. Register claims *"270a2c5f→06d8af60, shipped-v parity 0/804, 697 rank movers"* — **board not re-committed** (file stays `270a2c5f`). | YES | no | no | the `→06d8af60` transition is claimed, not committed; this is where the committed board first goes stale |
| **#113** | claude/lege-projection-law-postures-63u283 | `a90052ad…` | `cc58570a65616a643a5dcfc955a79f5a44dd5adc` | child (mb==base) | Leg E projection law (R103.3) + postures. Engine advances `rl_model.py`→`cc626d7d`, `_merged_recover.py`→`6ad07bb2`; `rl_export.py`; +ui. "display, values un-baked". | YES | no | no | forward-lens board `d85901af` not committed |
| **#115** | claude/legf-phantom-intake-build-dvbipz | `cc58570a…` | `7b6dfc52324e0b3a2367c9324e1acff6c8b0abaa` | child (mb==base) | Leg F1 Phantom Intake Layer (+1/+2), gated `RL_LEGF`. `rl_export.py`; +ui. "phantom 0/804". | YES | no | no | — |
| **#117** | claude/legf3-projection-fix-tbvxu5 | `7b6dfc52…` | `bccc23145e154f5b83385ffe8c06a54beab09030` | child (mb==base) | Leg F3 projection fix (§2.vi/§2.iii). `_merged_recover.py`→`99e75d68`, `rl_export.py`. | YES | no | no | ±5% backtest carried as a tension (per PR title) |
| **#118** | claude/legf4-midvet-calibration-o6x36j | `bccc2314…` | `a9570cb5d567300cc1969328018035e700f88963` | child (mb==base) | Leg F4 mid/veteran forward calibration (§2.vii L-SYMMETRY damper). `_merged_recover.py`→`caf013e2`, `rl_export.py`. | YES | no | no | — |
| **#119** | claude/legf5-entrant-layer-conservation-p4susl | `a9570cb5…` | `15a9abd996f8f7426e98f173d83a0d600b966a3c` | child (mb==base) | Leg F5 entrant layer (§2.viii) + conservation gate (§2.x). `rl_export.py`; +ui. **Named "audit-clear head 15a9abd"** in the directive. | YES | no | no | — |
| **#121** | claude/legf6-iso-freeze-bhigmd | `15a9abd9…` | `540b62f3c1600178aabc56f2dd1ab59c68460b2b` | child (mb==base) | Leg F6 freeze `_iso_dec`→ `data/v0surf.pkl` (`3af2b725`). `_merged_recover.py`→`904722cd`; `boot_guard.py` (+Guard-5 v0surf wiring); `expected_boot` gains the `v0surf` pin. | YES | no | no | **PARTIAL determinism fix** — F6 "scope=one" falsified (register item 389): a residual live `np.interp` weather path remains |
| **#123** | claude/env-pin-2026-07-19-4y4w0p | `540b62f3…` | `3055ea5ffdc390f81d5e17476a60fbb841f24cff` | child (mb==base) | ENV-PIN: `requirements-lock.txt` (numpy 2.4.4 --hash), `bootstrap_env.sh`, fail-closed ENV-PIN assert in `bootstrap.sh`. **Zero** engine/store/board/`expected_boot` bytes changed → value-neutral by construction (verified). **This is the bake base.** | YES (bake base) | no | no | wheel-pin **INSUFFICIENT**: container-#2 gate RED (item 394 — divergence is CPU-dispatch, not the wheel). Does **not** re-stamp the stale engine pins → Guard 5 still HALTs here |
| **#125** | claude/weekly-store-write-directive-8rmmkp | `3055ea5…` | `f6e7f8457c87a54d9dd198ca1111da0a17ed97a1` | child of #123 (mb==base) | Weekly-apply store-write `apply()` (`round_apply.py`, `score_ingestor.py`) + dedup ledger (`applied_rounds_ledger.json`). **Store byte-UNCHANGED** (`968de0c7`, no real write). Also re-stamps the SAME 2 engine pins as the bake (Pre-Step 0). | **NO — post-release** | no (candidate code; report-only / DO-NOT-MERGE until go-live) | no | not accepted as the completed weekly updater (transaction-safety / stale-preview / UI-refresh / round-history / multi-round proof unverified) |
| **#124** | claude/code-build-viewing-pack-f61i52 | base `main`; fork point `d415e175a6fac30255e2e2f1bdced060edd6c35d` (NOT the current main tip) | `05d3da352f97d94a66d2b95469e3fb7284a7fae2` | off an earlier main | REPORT-ONLY viewing render. **HALTED at the reproduction precondition**; committed the divergent balanced board `d7a95e8d…` as container-#2 evidence. | NO | **YES — evidence-only** | no | it proves the divergence (does **not** reproduce `06d8af60`) |

Related report-only PRs off `main` (not in the named set but part of the same saga; do not merge):
`#114` legf2 retrospective boards, `#116` fwd_calib, `#120`/`#122` viewing packs (all REPORT-ONLY / DO-NOT-MERGE).

DO-NOT-MERGE branches flagged by the record (verified *not* in the candidate chain): `fc7045d6` (an F7
experiment that **deleted** `data/v0surf.pkl`), `8b8ab7d` (stale iso-corr), `b854fbf` (F7 diagnostic), the
dispatch-pin branch (HALTed).

---

## B — Board identities (full inspection; committed bytes vs prose)

**Common inputs for every "current-engine" board below** (all byte-verified at `3055ea5`): store
`968de0c7a0183ca3914165536f39607a`, curve `pvc_curve_v2.json 56dd7a7bca4306d9224aec0ef52efa32`,
q97m `cfdc73216c099e5e8f1fda3968f31c00`, band `34faa8659cc8f19794f5cb9584fa19b2`, v0surf
`3af2b7258b8c8c596c4184617f99d3ca`, engine `rl_model.py cc626d7db7524929e5d2f1b024b25fb4` /
`_merged_recover.py 904722cd3fc16957a58796d8e2cb4caa`.

### B.1 — `270a2c5f` — the ONLY board committed in the release lineage
- **Path / provenance:** `data/rl_build/rl_app_data.json`, present byte-identical at every stack head
  **#109→#123** (and on report branch #120). Full MD5 **`270a2c5ffda21dc4945ebbcfb4c34562`**.
- **`.srcmd5`:** `own 270a2c5f… / source 968de0c7… (rl_model_data.json) / tier 1`.
- **Semantic configuration:** the **pre-five-migration ("ACT-2 / #109-era") board.** The register calls it
  *"the stale 270a2c5f … the e4177c2/ACT-2-era board"* and *"the ACT-2 baseline"*. It was built by the
  **#109 engine** (`rl_model.py a5fd3d7d` / `_merged_recover.py 40f43772`) — **not** by the current
  `cc626d7d`/`904722cd` engine. It is not any of the current-engine quartet configs.
- **Source store MD5:** `968de0c7…` (round-14 store — see D/round-14 caveat).
- **Committed & byte-recoverable?** **YES** (Git blob; full hash recoverable).
- **`expected_boot` pins it?** **YES** at the candidate head (`board = 270a2c5f`), so Guard-5 block-0c passes.
- **Guard 5 validates it?** Yes for the *board* field (committed==pin). Guard 5 does **not** check that the
  board is reproducible from the pinned engine — and it is not (see contradictions).
- **Any directive calls it the release artifact?** **No.** Manifest/handover call the release board `06d8af60`.
- **Verification status:** VERIFIED committed bytes.
- **Contradiction:** it is the **committed & pinned** board but the record names a **different** board
  (`06d8af60`) as the round-14 board of record. It predates Legs D-five/E/F entirely.

### B.2 — `06d8af60` — the intended "board of record" (NOT committed)
- **Semantic configuration:** **BALANCED** board — `RL_LEGE=0 RL_LEGF=0` (`RL_PVC2=1`) on the **current**
  engine. HANDOVER rev164: *"Board of record: balanced 06d8af60 (RL_LEGE=0 RL_LEGF=0)."* Manifest v4.57:
  *"board of record 06d8af60."* It is the reproduction-gate target in `DIRECTIVE_BAKE_v2_11` Step 2.
- **Committed & byte-recoverable?** **NO.** A full-tree, all-blob MD5 scan of every candidate head
  (#109/#119/#121/#123) **and** the report-only branches (#114/#120/#122/#124) found **zero** files whose
  content md5 is `06d8af60`. No 32-char form of the hash exists in any doc either — it lives only as an
  8-char prefix in prose + session proof logs.
- **`expected_boot` pins it?** No (the pin is `270a2c5f`). **Guard 5 does not validate it.**
- **Provenance provable without rerun?** **NO** — materialising it requires re-running the board build,
  which is the unstable `np.interp` pipeline (see D/G).
- **Verification status:** **PROSE-ONLY (8-char).** Byte-unverifiable.

### B.3 — `1f10220c` — DEFAULT board (all legs ON) — NOT committed
- Config: **default / shipped-default env** (`RL_LEGE=1 RL_LEGF=1`) on the current engine ("the candidate
  default is 1f10220c (F5 head)"). **Not committed anywhere** (all-blob scan negative). No full hash in prose.
- Guard 5 does not pin/validate it. Verification status: **PROSE-ONLY (8-char)**.

### B.4 — `d85901af` — FORWARD lens board (`RL_LEGE=1 RL_LEGF=0`) — NOT committed
- Config: **forward / Leg-E lens** (register: *"RL_LEGF=0 ⇒ d85901af MATCHES the filed Leg-E lens board"*,
  *"the LEGE=1 lens board d85901af"*). **Not committed** (all-blob scan negative). No full hash in prose.
- Verification status: **PROSE-ONLY (8-char)**.

### B.5 — `9829d01a` — KILL-SWITCH board (`RL_PVC2=0`) — NOT committed
- Config: **RL_PVC2 kill-switch** (register: *"RL_PVC2=0 ⇒ 9829d01a byte-exact"*). The declared-off
  reproduction of the pre-Leg-D pathway. **Not committed** (all-blob scan negative). No full hash in prose.
- Verification status: **PROSE-ONLY (8-char)**.

### B.6 — `d7a95e8d` — WEATHER / FLIP board (divergent balanced build) — committed only as EVIDENCE on #124
- **Path:** `session_2026-07-19/viewing_pack/evidence/board_balanced_repro.container2.json` on **#124 only**.
  Full MD5 **`d7a95e8d1882ad21e5a5fb0f895a033f`**.
- **Semantic:** the **container-#2 divergent build of the balanced config** — same env, same recipe, but the
  `np.interp` CPU-dispatch flip yields Σv 750,171 / Sheezel 7869 (−95) **≠** the intended `06d8af60`
  (Σv 752,427 / Sheezel 7964). It is a **rank-unsafe** board; it exists **as proof the gate must exist**.
- **Committed & recoverable?** YES, but as *evidence of failure*, on a report-only branch. **Never a ship
  candidate.** No directive names it the release artifact. Verification status: VERIFIED (as flip evidence).

### B.7 — `83a4b21d` — WEATHER / FLIP board (F5/F6-era divergence) — NOT committed
- **Semantic:** the earlier weather-flip signature of the balanced board (register: *"83a4b21d = foreign-
  container … Σv 750,159 / Sheezel −95"*, *"83a4b21d (F6-era)"*). Same failure class as `d7a95e8d`.
- **Not committed anywhere** (all-blob scan negative). No full hash in prose. Verification status:
  **PROSE-ONLY (8-char)**.

### B.8 — reconciliation summary of the seven required hashes

| hash (short) | config / role | full MD5 | committed bytes? | pinned? | Guard-5 validates? | status |
|---|---|---|---|---|---|---|
| `270a2c5f` | pre-five-migration ACT-2 board (committed & pinned) | `270a2c5ffda21dc4945ebbcfb4c34562` | **YES** (`data/rl_build/rl_app_data.json`, #109→#123) | **YES** (candidate head) | yes (board field) | VERIFIED |
| `06d8af60` | **balanced, intended board of record** | — (not recoverable) | **NO** | no | no | PROSE-ONLY |
| `1f10220c` | default (all legs on) | — | **NO** | no | no | PROSE-ONLY |
| `d85901af` | forward / Leg-E lens (LEGE=1 LEGF=0) | — | **NO** | no | no | PROSE-ONLY |
| `9829d01a` | kill-switch (RL_PVC2=0) | — | **NO** | no | no | PROSE-ONLY |
| `d7a95e8d` | weather flip of balanced (container #2) | `d7a95e8d1882ad21e5a5fb0f895a033f` | YES (evidence on #124 only) | no | no | VERIFIED (flip evidence) |
| `83a4b21d` | weather flip of balanced (F5/F6-era) | — | **NO** | no | no | PROSE-ONLY |

**Headline:** of the seven, exactly **one shippable-lineage board is byte-recoverable — `270a2c5f`, and it is
the stale ACT-2 board, not the board of record.** The board of record `06d8af60` and every other current-engine
config exist **only as 8-char prefixes in prose**. The only other committed board bytes are a *flip-failure
sample* (`d7a95e8d`).

---

## C — Shipped-artifact determination

1. **Which exact file does the HTML application currently load?**
   `data/rl_build/rl_app_data.json`, surfaced through `ui/data/board_view_working.js` /
   `board_view_public.js` (generated by `tools/extract_board_view.py`) and ring-fenced by
   `ui/app/config.js EXPECTED_BOARD`. On `main`/checkpoint that value is **`790136a3`** (the v2.10 captaincy
   board). The v2.11 candidate is not on `main`, and the candidate lineage does **not** re-pin the UI
   (`EXPECTED_BOARD` is still `790136a3` at `3055ea5`; only `ui/app/board.js` display code differs). So the
   HTML currently renders **the v2.10 board `790136a380b56ebdf5db2874b6f354de`**, not any v2.11 board.

2. **Which exact file is pinned in `data/expected_boot.json`?**
   `board` → `data/rl_build/rl_app_data.json`. On `main`/checkpoint the pin is
   **`790136a380b56ebdf5db2874b6f354de`**. At the candidate/bake head `3055ea5` the pin is
   **`270a2c5ffda21dc4945ebbcfb4c34562`** (= the committed ACT-2 board file).

3. **Which hash is the balanced diagnostic gate?** `06d8af60` (`RL_LEGE=0 RL_LEGF=0`) — the reproduction-gate
   reference in `DIRECTIVE_BAKE_v2_11` Step 2 and DECISIONS v125 R108.7(b). **Not committed as bytes.**

4. **Which hash is the default / forward-enabled board?** Default (all legs on) = `1f10220c`; forward
   (`RL_LEGE=1 RL_LEGF=0`, Leg-E lens) = `d85901af`. **Neither committed as bytes.**

5. **Which artifact was intended to be shipped as the round-14 v2.11 release?** Per manifest v4.57 + HANDOVER
   rev164, the **balanced board `06d8af60`** (round-14 store `968de0c7`). This intent **contradicts** the
   committed/pinned board `270a2c5f`.

6. **Does that exact artifact still exist as committed, byte-recoverable Git content?** **NO** for `06d8af60`.
   The only byte-recoverable release-lineage board is `270a2c5f` (the stale ACT-2 board), which is **not** the
   intended artifact.

7. **Can its provenance be proven without rerunning the unstable numerical build?**
   - For `270a2c5f`: **YES** — blob + `.srcmd5` (source `968de0c7`) + the #109 engine that built it
     (`a5fd3d7d`/`40f43772`) are all committed and byte-recoverable. But it is the *superseded* board.
   - For `06d8af60` (the intended one): **NO** — it is not committed; reproducing it means re-running the
     `np.interp` board pipeline, whose cross-container divergence is the entire determinism saga. On a
     diverging container the same config yields `d7a95e8d`/`83a4b21d` instead.

**C-verdict:** the board the record intends to ship (`06d8af60`) is **not** the board that is committed and
pinned (`270a2c5f`), and the intended one is **not byte-recoverable**. See G.

---

## D — Boot-integrity map (`data/expected_boot.json` at candidate head `3055ea5`)

| key | expected (pinned) hash | file it validates | mapping unambiguous? | pass/fail at `3055ea5` | re-stamp effect |
|---|---|---|---|---|---|
| `store` | `968de0c7a0183ca3914165536f39607a` | `engine/rl_after/rl_model_data.json` (md5 `968de0c7`) | yes | **PASS** | n/a (unchanged) |
| `board` | `270a2c5ffda21dc4945ebbcfb4c34562` | `data/rl_build/rl_app_data.json` (md5 `270a2c5f`) | yes | **PASS** | leaving it re-stamps **already-accepted committed bytes** — but of the *stale* board (see caveat) |
| `engine_head` | `40f43772dc0950e4d4ba6cb6bee59748` | `engine/rl_after/_merged_recover.py` (actual md5 `904722cd`) | yes | **FAIL** (pin lags) | Step-1 → `904722cd`: **re-stamps already-committed, byte-recoverable engine source** (not new bytes) |
| `rl_model` | `a5fd3d7d6af87328a42d5793daa1b826` | `engine/rl_after/rl_model.py` (actual md5 `cc626d7d`) | yes | **FAIL** (pin lags) | Step-1 → `cc626d7d`: **re-stamps already-committed, byte-recoverable engine source** (not new bytes) |
| `q97m` | `cfdc73216c099e5e8f1fda3968f31c00` | `data/q97m.pkl` | yes | **PASS** | n/a |
| `band` | `34faa8659cc8f19794f5cb9584fa19b2` | `cm_400.pkl` (`/home/claude/cm_400.pkl` load-path) | yes | PASS (per hook) | n/a |
| `v0surf` | `3af2b7258b8c8c596c4184617f99d3ca` | `data/v0surf.pkl` (md5 `3af2b725`) | yes | **PASS** | n/a |
| `config` | `c2d233ae…71b53b` | `data/model_config.json` (via `config_manifest`) | yes | PASS | n/a |
| `register` | `652d83e8…` | `LTI_REGISTER.md` | yes | PASS | n/a |
| `peak_model`/`pvc_snapshot`/`bust_prior` | (as pinned) | `engine/rl_after/*.pkl/.json` | yes | PASS | n/a |

**Item 399 confirmed from bytes:** the ONLY failing pins at `3055ea5` are the two engine pins — they were
last stamped at #109 (`a5fd3d7d`/`40f43772`) and never advanced while Legs D-five/E/F1–F6 moved the engine to
`cc626d7d`/`904722cd`. The Step-1 re-stamp corrects exactly and only those two, to values that are
**already-committed byte-recoverable source** → it *re-stamps accepted bytes*, it does **not** accept newly
generated bytes. This is the value-neutral half.

**Caveat that Guard 5 cannot see:** after the Step-1 re-stamp, the manifest pins `board = 270a2c5f`
(built by the OLD `a5fd3d7d` engine) alongside `engine = cc626d7d`. Guard-5 block-0c only checks
`committed board == board pin`; it does **not** check the board is reproducible from the pinned engine — and
it is not. So the re-stamped manifest is Guard-5-green but internally incoherent (board provenance ≠ engine
provenance). This is the crux contradiction, not a boot pass/fail.

---

## E — Open-PR classification

| PR | class |
|----|-------|
| #109, #111, #113, #115, #117, #118 | **required candidate lineage** (Leg-D re-derivation → Leg-D Build B → Leg-E → Leg-F1/F3/F4) |
| #119 (F5, audit-clear), #121 (F6/v0surf) | **required candidate lineage** (#121 carries an unresolved *partial-determinism* flag, item 389) |
| #123 (env-pin) | **required candidate lineage / bake base** — but its stated purpose (fix the flip) is **unresolved**: container-#2 RED proved the wheel-pin insufficient (item 394) |
| #125 (weekly store-write) | **post-release** ingestion work (gate OFF; no real store write). **Explicitly NOT a release prerequisite.** Not accepted as the completed weekly updater. |
| #124 (viewing render) | **evidence-only** (report-only; committed the flip board `d7a95e8d` as proof the repro-gate must hold) |
| #114, #116, #120, #122 | **evidence-only / report-only** (retrospective boards, fwd_calib, viewing packs) — DO-NOT-MERGE |
| the dispatch-pin branch, `fc7045d6`, `8b8ab7d`, `b854fbf` | **unsafe / unaccepted** (DO-NOT-MERGE; `fc7045d6` deletes `v0surf.pkl`) |

---

## F — Release blockers (evidence-backed only)

**TRUE release blocker**
1. **The intended round-14 board of record `06d8af60` is not byte-recoverable committed content anywhere**
   (all-blob scan negative across the whole candidate + report lineage), and no full-length hash for it is
   recorded. Proving/producing it requires re-running the board pipeline — the exact `np.interp` build that
   diverges cross-container. → the release cannot ship the intended artifact from committed bytes alone.
2. **The committed & pinned board `270a2c5f` is stale** (pre-five-migration ACT-2, built by the superseded
   `a5fd3d7d` engine). Shipping it would ship a board that predates Legs D-five/E/F and whose provenance
   contradicts the re-stamped engine pins.

**Post-release corrective work (not a v2.11 blocker)**
- UI re-pin: `ui/app/config.js EXPECTED_BOARD` is `790136a3` (v2.10); any new board requires re-pinning +
  regenerating the `ui/data/*` bundles or the UI fail-closes. (Not to be done in this read-only job.)
- Weekly ingestion (#125) — post-release, gate OFF; needs the independent verification named in RECOVERY_STATE.
- Docs-carry items the bake directive defers: `docs/acceptance_v1_21.json`, INFRA_ALLOW entries.

**Long-term determinism work**
- The `np.interp` CPU-dispatch flip (items 391/394): F6 = partial, F7 = wrong-target, env-pin wheel =
  insufficient, dispatch-pin = unproven. Cross-machine reproducibility is **not** achieved. This is the root
  reason `06d8af60` cannot be trusted to re-materialise on an arbitrary container.

**Documentation contradictions (report directly)**
- **C1:** Manifest v4.57 / HANDOVER rev164 name `06d8af60` "board of record", but the committed & pinned board
  at every candidate head is `270a2c5f`. The two are different boards on different engine lineages.
- **C2:** `DIRECTIVE_BAKE_v2_11` Step-1 asserts "the balanced board is UNCHANGED … a re-stamp cannot move the
  board" and Step-3 "nothing more is needed". True for the *balanced* build (`06d8af60`), but the *committed*
  board file is `270a2c5f`; the directive never regenerates/re-commits the board, so as written it would ship
  `270a2c5f` while pinning `cc626d7d` — an incoherent (board≠engine) manifest.
- **C3:** `DIRECTIVE_BAKE_v2_11` Step-1 says to "close the `build_board.sh` engine-assert BYPASS", but **there
  is no root `build_board.sh` at `3055ea5`** — only per-session copies
  (`session_2026-07-14/…`, `session_2026-07-18/legf1/scripts/…`, `session_2026-07-19/envpin/scripts/…`). The
  directive's own hedge ("If it isn't where reported, report what you find") applies.
- **C4 (lesser):** register #111 line claims "shipped-v parity 0/804" for `270a2c5f→06d8af60` yet "697 rank
  movers" — a Leg-D-only comparison, superseded by Legs E/F; it does not make `270a2c5f` a value-equivalent
  stand-in for the current-engine board.

---

## G — Minimum defensible release path

> **▲ RESOLVED 2026-07-20 (`release/v2.11-rc1`):** the HALT below is lifted by missing-evidence item **G.1** —
> `06d8af60` is now committed byte-recoverable content (commit `7c6768ee`, blob `e546ab0b`, full MD5
> `06d8af60b679a12db07c064c60c065f9`) and reproduces byte-exact under the fixed provenance (FV suite GREEN1).
> The RC adopts + pins those exact bytes without a rebuild, exactly as G.1 describes. Original finding retained
> below as the historical record.

**HALT — canonical artifact not recoverable.**

The narrowest sequence that would release the *verified* round-14 board of record without rerunning the
unstable pipeline **does not exist from committed content**, because:

- the intended artifact `06d8af60` is **not** committed and has **no** recoverable full hash — the only way to
  obtain it is to re-run the `np.interp` board build (forbidden here, and unstable cross-container); and
- the only byte-recoverable release-lineage board, `270a2c5f`, is the **superseded ACT-2 board** — not the
  round-14 board of record, and provenance-incoherent with the engine the bake would pin.

**Precisely what evidence is missing (any ONE would lift the HALT):**
1. **The committed bytes of `06d8af60`** — a byte-for-byte copy of the round-14 balanced board checked into
   Git (e.g. under a session/evidence path), whose md5 = `06d8af60…` at full length, so it can be adopted +
   pinned without a rebuild. (None exists today.)
2. **OR** an owner ruling that redefines the round-14 release artifact as the *committed* `270a2c5f`, together
   with acceptance that it is the pre-five-migration board and a coherent re-pin of both `board` and the two
   engine pins to a matched `270a2c5f`+`a5fd3d7d`/`40f43772` snapshot (this ships the ACT-2 board, not the
   board built by Legs D-five/E/F — a material product decision, **not** authorised by evidence).
3. **OR** a reproduced `06d8af60` from a container that passes the reproduction gate — which is *running the
   pipeline*, explicitly out of scope for this job and unproven to be repeatable given items 391/394.

What is **verified and defensible right now** (for the owner review, not a release authorisation): the engine
source (`cc626d7d`/`904722cd`), the store (`968de0c7`), the curve (`56dd7a7b`), q97m/band/v0surf, and the
two-engine-pin boot re-stamp are all byte-recoverable and internally consistent. The gap is exclusively the
**board artifact**: the record's board of record is a hash without bytes.

---

## Verified-fact appendix (all from `git cat-file … | md5sum`)

- checkpoint = main = recovery/v2.11 base = `612d4c058560568b3d4d49ecd785759931885081`
- checkpoint board/store/engine: `790136a3…` / `b1fd0bce…` / `_merged_recover fc7045d6` `rl_model f79fc740`
- candidate stack heads: #109 `e4177c21…` · #111 `a90052ad…` · #113 `cc58570a…` · #115 `7b6dfc52…` ·
  #117 `bccc2314…` · #118 `a9570cb5…` · #119 `15a9abd9…` · #121 `540b62f3…` · #123 `3055ea5f…` ·
  #125 `f6e7f845…` · #124 `05d3da35…`
- board file md5 at #109…#123 = `270a2c5ffda21dc4945ebbcfb4c34562` (unchanged the whole way)
- engine at `3055ea5`: `rl_model.py cc626d7db7524929e5d2f1b024b25fb4`,
  `_merged_recover.py 904722cd3fc16957a58796d8e2cb4caa`
- stale engine pins at `3055ea5`: `engine_head 40f43772dc0950e4d4ba6cb6bee59748`,
  `rl_model a5fd3d7d6af87328a42d5793daa1b826`
- store `968de0c7a0183ca3914165536f39607a`; curve `pvc_curve_v2.json 56dd7a7bca4306d9224aec0ef52efa32`;
  v0surf `3af2b7258b8c8c596c4184617f99d3ca`; q97m `cfdc73216c099e5e8f1fda3968f31c00`
- committed flip board (#124 only): `session_2026-07-19/viewing_pack/evidence/board_balanced_repro.container2.json`
  = `d7a95e8d1882ad21e5a5fb0f895a033f`
- all-blob MD5 scans (#109/#119/#121/#123 + #114/#120/#122/#124) returned **no** match for
  `06d8af60`/`1f10220c`/`d85901af`/`9829d01a`/`83a4b21d`

## UNKNOWN / unresolved (explicit)

- **U1 — full MD5 of `06d8af60`, `1f10220c`, `d85901af`, `9829d01a`, `83a4b21d`:** `UNKNOWN` / not recoverable
  (never committed; only 8-char prefixes in prose).
- **U2 — byte-recoverable `06d8af60`:** `UNKNOWN` (none found; would require a rebuild).
- **U3 — "round-14" label on store `968de0c7`:** store md5 is VERIFIED; the *round-14* labelling is a
  consistent prose claim across manifest/handover/directive but was **not** independently confirmed from the
  store's internal scoring arrays in this read-only pass. `UNKNOWN` pending a store-internal check.
- **U4 — whether the residual `np.interp` divergence moves ranks for `270a2c5f` specifically:** `UNKNOWN`
  (rank-unsafety was shown for the balanced `06d8af60↔d7a95e8d` flip; not analysed for `270a2c5f`, and cannot
  be without a build).
- **U5 — the exact `build_board.sh` the bake directive means to de-bypass:** `UNKNOWN` (no root file;
  multiple per-session copies).
- **U6 — value equivalence of `270a2c5f` vs `06d8af60`:** `UNKNOWN` (the "parity 0/804" figure is a Leg-D-only
  prose claim, superseded by Legs E/F; not byte-verifiable without a build).
