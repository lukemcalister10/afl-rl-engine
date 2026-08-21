# P4b — THE ROLLBACK FIRE DRILL · 2026-08-21

**PLAN_v6 4b, verbatim:** *"The one ROLLBACK fire drill before the first collapse: restore the tagged
artifact BYTES + boot guards accept them (tags are bytes, not recipes). Rebuild-from-source parity is
secondary, best-effort; its failure is a reproducibility finding, not a rollback failure."*

## VERDICT

> ### PASS — tags ARE restorable bytes.
>
> Every one of the 13 pinned identities at `baked-v2.11-2026-08-20` restored byte-exact from the tag
> and hashed to what that tag's own `data/expected_boot.json` declares. Guard 5 (`boot_guard.py`),
> its forward-valuation legs and `ruling_config_check.py` all ACCEPTED the restored bytes.
> **Elapsed, machine-measured, from `git archive` to a self-certified tree: 1.93 seconds.**
>
> ### BONUS — and it is a recipe too.
>
> The secondary leg was not merely attempted, it succeeded: `rl_export.py` at the tag rebuilt the
> board **BYTE-EXACT** to the tagged `a05fe951f78482c70520480e184c80ec`, three times — under the
> fenced `RL_CONFIG_MODE=bake` posture, under a bare posture, and again on a repeat build
> (build-twice determinism). ~85 seconds each. No reproducibility finding was owed on the board.
>
> ### BUT — the naive rollback is wrong in four specific ways, all measured below.
>
> A seat who, at 3am, ran the obvious sequence would restore a tree the contract gate rejects (F1),
> leave half the rollback undone in the shared workspace (F2), delete PACKAGE 1/2a/3a and the
> append-only register (F3), and get a FAIL verdict from the estate's own named restore-verifier that
> means nothing (F4). None of those is a byte-restore failure. All four are why this drill was run
> before the retirement era starts collapsing dials on the assumption that rollback works.

Everything below is measured. Transcripts in `transcripts/`, the exact scripts in `scripts/`, the
never-executed live sequence in `EMERGENCY_ROLLBACK_RUNBOOK.md`.

---

## 1. THE TARGET, AND WHY

The brief noted the record names **v2.9 at 9f8ae76** as canonical. That is verified as **stale
narrative, not a stale tag**: the phrase lives inside `data/expected_boot.json`'s `tag` field —
*"v2.9 tag (9f8ae76) is unmoved and remains canonical"* — a 2026-07-13 note that has been carried
forward verbatim in the manifest ever since and is still printed by Guard 5's PASS line today. The
tag itself is real and five releases old.

Twelve tags exist. Ordered by creation:

| tag | kind | date | commit |
|---|---|---|---|
| `prebake-v2.4-anchor` · `baked-v2.4-2026-07-04` | lightweight | 2026-07-03/04 | 6035ce1 / 389ac39 |
| `baked-v2.5-2026-07-05` · `prebake-v2.5-anchor` | annotated | 2026-07-05 | f30028b / 6002a37 |
| `v2.6` `v2.7` `v2.8` `v2.9` `v2.10` | lightweight | 2026-07-09 … 07-15 | … `v2.9` = 9f8ae76 |
| `v2.11-r19-mvp` | lightweight | 2026-07-22 | 6c47f03 |
| `baked-v2.11` | lightweight | 2026-08-20 | **463e53d** |
| **`baked-v2.11-2026-08-20`** | **annotated** | **2026-08-20** | **463e53d** |

**Target chosen: `baked-v2.11-2026-08-20` @ 463e53d.** Why:

1. It is the most recent tag, by five releases over the one the manifest's prose still names.
2. `baked-v2.11` points at the *same commit*, so the restored tree is identical either way; the
   annotated tag was preferred because it is the one carrying the owner-word record — its tag object
   reads *"THE LANDING: board a05fe951 / 664,949 replaces 88ce647f / 752,429. Owner word 2026-08-20.
   Bare build byte-exact; Guard 5 green unbound; book re-sealed; register v735-v781."* RULEBOOK law
   10(b) puts tags and releases on the owner's word; the annotated object is where that word is
   recorded, so it is the owner-release tag of the two.
3. It is the last certified state **before** the live tree moved past it — the staircase adoption
   (board `68be10c7` → `b3e8da99`) and PACKAGE 3a both landed on 2026-08-21, after the tag. That
   makes it the actual answer to "get back to a prior certified state", not a hypothetical one.

---

## 2. THE PRIMARY DRILL — DO THE TAGGED ARTIFACTS *ARE* THE CERTIFIED BYTES?

`git archive baked-v2.11-2026-08-20 | tar -x` into an isolated scratch checkout: **4,503 files,
253,422,539 bytes, 1.714 s.** Then every pinned identity re-hashed in the restored tree and compared
to the tag's own `data/expected_boot.json`. Transcript: `transcripts/step2_hashes.txt`.

### A. Pinned file artifacts — 11 of 11 MATCH

| pin | path | pinned == restored md5 | verdict |
|---|---|---|---|
| `board` | `data/rl_build/rl_app_data.json` | `a05fe951f78482c70520480e184c80ec` | **MATCH** |
| `store` | `engine/rl_after/rl_model_data.json` | `cb38ef1171dcf20aae66ebf12682be0d` | **MATCH** |
| `engine_head` | `engine/rl_after/_merged_recover.py` | `5ac6780f3c4931edcaa527576bbdfb88` | **MATCH** |
| `rl_model` | `engine/rl_after/rl_model.py` | `6fe7c4155866d80e8045bed2d3bf2802` | **MATCH** |
| `band` | `data/cm_400.pkl` | `34faa8659cc8f19794f5cb9584fa19b2` | **MATCH** |
| `q97m` | `data/q97m.pkl` | `cfdc73216c099e5e8f1fda3968f31c00` | **MATCH** |
| `v0surf` | `data/v0surf.pkl` | `5dd34ca82735f5c8f021b1c7320df8f8` | **MATCH** |
| `peak_model` | `engine/rl_after/peak_model_v4.pkl` | `f305fe5330222f4fa14d3654a0e91ef7` | **MATCH** |
| `pvc_snapshot` | `engine/rl_after/pvc_snapshot.json` | `ade79790efc8ad4585c2c6800a935eaa` | **MATCH** |
| `bust_prior` | `engine/rl_after/bust_prior_table.json` | `5942aa6ad7be1d482eed737997486c70` | **MATCH** |
| `register` | `LTI_REGISTER.md` | `652d83e87780e415a01a2de6d8b3cc57` | **MATCH** |

The four fitted pickles are the ones that matter most here: the manifest's own `_fitted_note` says
*"the board's identity is MADE OF these"*. All four restored exact.

### B. Computed pins — 2 of 2 MATCH, recomputed by the tag's own code

| pin | recomputed by | value | verdict |
|---|---|---|---|
| `fv` | `fv_provenance.fv_identity()` over `engine/forward_valuation` | `6e9a370e5970c5aefa859858070f4c3420f0177b4698d6fac90bd08bf1780346` | **MATCH** |
| `config` | `config_manifest.manifest_hash()` | `eed19a75f775aeafe4ee5ea4b3990667192d8f90389ad6b0e8318e91062d14c1` | **MATCH** |

The board's own sidecar `data/rl_build/rl_app_data.json.srcmd5` independently agrees:
`own_md5 a05fe951…`, `source_md5 cb38ef11…`. `balanced_board_md5 234c3414…` has no in-tree artifact
by design (as `docs/STATE.md` also records) and is therefore not restorable or checkable as bytes —
stated, not silently skipped.

**13 pins declared, 13 pins verified, 0 drift.** Wall time for the whole comparison: **0.034 s**.

### C. DO THE BOOT GUARDS ACCEPT THEM?

Run against the restored bytes with `PATH="/root/rl_venv312/bin:$PATH"` and
`RL_REPO` / `CLAUDE_PROJECT_DIR` / `RL_FV` bound to the **scratch** checkout.
Transcripts: `transcripts/step3_guards.txt`, `transcripts/step3b_contract_check.txt`.

| guard | entry point | verdict | seconds |
|---|---|---|---|
| Guard 5 — boot store / rl_model / fv, all legs | `boot_guard.py <label> <store> <head> <band> <register>` | **PASS**, rc 0 | 0.062 |
| Guard 5 — forward-valuation checkout + loaded-path | `boot_guard.assert_fv_provenance()` | **PASS**, rc 0 | 0.031 |
| ruling-config (R3 + R-i) | `ruling_config_check.py` | **PASS** (13/13), rc 0 | 0.025 |
| release-state contract | `release_contract.py check` | **FAIL**, rc 1 — see F1 | 0.068 |

Guard 5's PASS line, quoted from the transcript:

```
boot-store guard (Guard 5) PASS  [p4b_fire_drill]  store cb38ef11 == pinned cb38ef11
  |  rl_model 6fe7c415 == pinned 6fe7c415  |  fv 6e9a370e == pinned 6e9a370e (checkout+loaded-path)
```

**The restored world self-certifies on the boot-guard family. Success criterion met.**

---

## 3. TIMINGS — how long a real rollback actually takes

Every number machine-measured on this box (`date +%s.%N` around each step), venv
`/root/rl_venv312` (Python 3.12.3).

| # | step | seconds |
|---|---|---|
| 1 | `git archive` the tag → 4,503 files / 253 MB | **1.714** |
| 2 | re-hash + compare all 13 pinned identities | **0.034** |
| 3.1 | `boot_guard.py` CLI, every leg | **0.062** |
| 3.2 | `boot_guard.assert_fv_provenance()` | **0.031** |
| 3.3 | `release_contract.py` (summary branch) | 0.027 |
| 3.3b | `release_contract.py check` (the verifier) | **0.068** |
| 3.4 | `ruling_config_check.py` | **0.025** |
| 4 | `verify_restore.sh` (the tag's own restore-verifier) | 13.717 |
| 5.0 | copy restore → rebuild sandbox | 0.610 |
| 5.1 | rebuild `rl_export.py`, `RL_CONFIG_MODE=bake` | 84.975 |
| 5.2 | rebuild `rl_export.py`, bare posture | 84.070 |
| 6.1 | rebuild #2, canonical (build-twice) | 83.816 |
| 6.2 | rebuild the book, `s4_matrix_M1v7.py` | 133.484 |
| 6.3 | `one_source_selftest.py` | 95.701 |
| 8 | `reseal_bake.py --check` (book seal re-verify) | 136.148 |

**The four numbers to quote:**

| what you get | elapsed |
|---|---|
| tagged bytes on disk, all 13 pins verified, boot guards green | **1.93 s** |
| …plus the tag's own scripted restore-verify | **15.6 s** |
| …plus a from-source rebuild proving byte-parity | **~87 s** |
| full re-certification: rebuild + book regen + self-test + seal re-verify | **~7.5 min** |

The expensive half of a rollback is not the restore. It is the re-certification — and, per F1–F3, the
re-pinning and re-seeding the restore does not do for you.

Control timings on the live head (`transcripts/step7_live_control.txt`), for scale, not comparison —
they ran on a different tree and are quoted only so nothing is implied: copy 1.027 s, build 145.527 s,
book 328.263 s, self-test 149.692 s.

---

## 4. THE SECONDARY LEG — rebuild-from-source parity

PLAN_v6 4b makes this best-effort and rules that its failure is a reproducibility finding, not a
rollback failure. **It did not fail.** Transcripts: `transcripts/step5_rebuild.txt`,
`transcripts/step6_selftest.txt`.

| build | posture | rebuilt board md5 | vs tagged `a05fe951…` |
|---|---|---|---|
| 5.1 | `RL_CONFIG_MODE=bake` (fenced canonical) | — (overwritten by 5.2, re-run as 6.1) | — |
| 5.2 | bare — no model-semantics `RL_*` set at all | `a05fe951f78482c70520480e184c80ec` | **BYTE-EXACT** |
| 6.1 | `RL_CONFIG_MODE=bake`, repeat build | `a05fe951f78482c70520480e184c80ec` | **BYTE-EXACT** |

This independently confirms the tag's own `_bake_note` claim — *"the BARE build (no model-semantics
RL_* set at all, RL_V0SURF_PKL unset) reproduces it BYTE-EXACT"* — and extends it: the fenced
canonical posture reproduces it too, and it reproduces on a repeat build (build-twice determinism at
the tag, measured rather than assumed).

The reason it reproduced is worth naming because the brief expected the opposite: **the environment
pin is intact on today's venv.** `bootstrap.sh` hard-asserts numpy `2.4.4` plus a bundled OpenBLAS at
sha256 `05c9f9eb89ee68a4b9d673184fa91c99587e736392c0c2d49180a8aa5303d080`. Measured on
`/root/rl_venv312`: numpy `2.4.4`, bundled OpenBLAS sha256 `05c9f9eb89ee…` — **byte-exact to the pin.**
There is no tag-era env mismatch to report. The board `a05fe951` is reproducible here because the box
is still on the pin the tag was baked on; that is a measurement with a shelf life, not a law.

The **book** is a different story and is F5.

---

## 5. FINDINGS

### F1 — MATERIAL. The tag's release contract is STALE. A rollback to it restores a tree Guard 5 accepts and the contract gate rejects.

`data/release_contract.json` at the tag was last written on **2026-08-10** (commit 5babe71) and was
**never re-stamped at the 2026-08-20 landing** that the tag commemorates. Its `identities` block
therefore describes a different release from the `expected_boot.json` committed beside it:

| field | contract says | expected_boot says | |
|---|---|---|---|
| `board` | `4b448a821f54…` | `a05fe951f784…` | **DIFFER** |
| `store` | `d9a24282357c…` | `cb38ef1171dc…` | **DIFFER** |
| `engine_head` | `c0a7e969fdd9…` | `5ac6780f3c49…` | **DIFFER** |
| `rl_model` | `33f940735281…` | `6fe7c4155866…` | **DIFFER** |
| `fv` | `d920557ef21d…` | `6e9a370e5970…` | **DIFFER** |
| `config_sha256` | `cef06fd6250b…` | `eed19a75f775…` | **DIFFER** |
| `band`, `register`, `balanced_board_md5`, `as_of_round` | | | AGREE |

`held_candidates` is **absent**, so not one of those six is a declared, excused hold. The contract's
own self-seal is **INTACT** (`contract_sha256 ef25c259…` recomputes exactly) — it is not tampered, it
is stale, which is the harder failure to see. Run under the tag's own verifier the result is
unambiguous (`transcripts/step3b_contract_check.txt`):

```
RELEASE-CONTRACT CHECK: FAILED
  - contract config_sha256 cef06fd6250b != live manifest hash eed19a75f775 (stale config pin)
  - contract identity board=4b448a821f54 != expected_boot a05fe951f784 (stale pin; …)
  - contract identity engine_head=c0a7e969fdd9 != expected_boot 5ac6780f3c49 (…)
  - contract identity fv=d920557ef21d != expected_boot 6e9a370e5970 (…)
  - contract identity rl_model=33f940735281 != expected_boot 6fe7c4155866 (…)
  - contract identity store=d9a24282357c != expected_boot cb38ef1171dc (…)
  - season_state.json source_store_md5 d9a24282 != live store cb38ef11 — exposure_pace was derived
    from a STALE store
```

**Attributed, not assumed.** The same verifier run against the CURRENT head, read-only
(`transcripts/step3c_live_control.txt`): `RELEASE-CONTRACT CHECK: PASS (contract 1b435ff6f988;
identities + config + posture consistent)`. The instrument works and the box is fine. The tag is the
incoherent one.

**Two consequences the retirement era needs to know.** First, a rollback to this tag must re-stamp the
contract in the same commit as the restore — the bytes cannot be trusted to bring their own release
state. Second, and worse: **the stale contract does not block a canonical rebuild.** `rl_export.py`
enforces `config_manifest` (its transcript prints `CONFIG ACCEPTED eed19a75f775`) but never calls
`release_contract.verify`, so the fenced `RL_CONFIG_MODE=bake` build at §4 completed rc 0 on a tree
whose release contract rejects it. The standalone gate is the only thing in the estate that catches
this, which means it only fires when someone runs it.

### F2 — MATERIAL. Restoring the repo is HALF a rollback. The shared workspace does not come back with it.

`verify_restore.sh` ends by calling `run_panel.sh`, and that call **HALTED**
(`transcripts/step4_verify_restore.txt`):

```
        at /home/claude/rl_workspace/rl_after/_merged_recover.py
        md5 3af8c1f7  !=  expected 5ac6780f (pinned; repo checkout )
        STALE BOOT: this is not the checked-out store. Re-run bootstrap.sh to re-seed the workspace…
```

That is **Guard 5 working exactly as designed** — `3af8c1f7` is the LIVE engine head, `5ac6780f` is the
restored tag's. `run_panel.sh` hardcodes `WS=/home/claude/rl_workspace/rl_after` with no override, so
the tag-era panel cannot be pointed at a scratch restore at all. The guard refused to certify the
wrong tree rather than certifying it silently. This is the P2 incident (*"never boot on an unverified
store"*) doing its job on a rollback, and it is the loudest positive result in the drill.

**The luck that must not be mistaken for design:** the fitted pickles the engine loads from outside the
repo — `/home/claude/{cm_400,q97m,v0surf}.pkl` — happened to be byte-identical between the tag and
HEAD (`34faa865…`, `cfdc7321…`, `5dd34ca8…` in both manifests), so Guard 5's loaded-path leg passed.
A rollback across a bake that moved `q97m.pkl` or `v0surf.pkl` would find the engine loading the wrong
pickle and would depend entirely on that leg firing. `bootstrap.sh` is a mandatory rollback step, not
a convenience.

**The drill deliberately did NOT run `bootstrap.sh`.** Two reasons, both recorded rather than assumed:
it would overwrite the shared workspace with tag-era bytes, and `/home/claude/.rl_build.lock` was
**held by another seat at the time** — `land-round-19205`, an R24 rehearsal sandbox, since
`2026-08-21T10:49:54Z`. Seeding it would have been a P3 ONE WRITER breach committed by the drill that
exists to prove the estate can recover safely. The step is written into the runbook instead.

### F3 — MATERIAL. `git checkout <tag> -- .` is not a rollback. It is a deletion.

`baked-v2.11-2026-08-20` predates PACKAGE 1, PACKAGE 2a and PACKAGE 3a. Measured absences in the
restored tree:

- `acceptance/` — **absent.** The whole acceptance runner and its ruled-red ledger.
- `tools/landing/` — **absent.** The lander, the carrier set, the abort ladder, the STATE generator.
- `docs/register/` — **absent.** The append-only record's new form and its 14 entries.
- `data/sheet_pins.json` — **absent.** PACKAGE 3a's pin carrier; at the tag those pins were still
  inside the engine.

A whole-tree checkout would un-land all of it and delete an append-only record. A rollback must be
**scoped to the value-bearing carriers**, and the estate already enumerates them —
`tools/landing/carriers.py` `LEVER_CARRIERS` (+ `ROUND_EXTRA_CARRIERS` if the rollback crosses an
advance), which is the list the runbook uses rather than a fresh guess. Note the engine sources are
deliberately *not* in that set (a lever landing never moves them), so a rollback must add
`_merged_recover.py`, `rl_model.py` and `engine/forward_valuation/` explicitly.

`data/sheet_pins.json` is a **P13 trap** specifically: rolling `_merged_recover.py` back across the
3a seam restores the in-engine pin block and orphans the live pin file — two declarations, no writer
of record for either. P13 says a pin moved by any other hand is a halt. That is a stop-and-ask, not a
step.

### F4 — MATERIAL. `verify_restore.sh` — the estate's named scripted restore-verifier — is broken, and it is broken at HEAD too.

Its verdict on the restored tag world was `9 PASS / 2 FAIL => RESTORE-VERIFY FAIL`, rc 1. **Both
failures are the instrument, not the restore.** Three defects, each measured:

1. **Its `PYTHONPATH` omits the repo root.** It `cd`s to `engine/rl_after` and exports
   `PYTHONPATH="$RA:$ROOT/engine/forward_valuation:$ROOT/vendor:…"` — no `$ROOT`. Since the
   2026-07-20 fv-provenance remediation the engine's loader fails closed without `fv_provenance`, so
   the named-player probe dies with
   `wire_redesign: the canonical resolver fv_provenance is not importable (ModuleNotFoundError…)`
   — and the script runs that probe under `2>/dev/null`, so the two checks compare an **empty string**
   against their expectations and report a value mismatch that never happened
   (`transcripts/step4b_diag.txt`).
2. **Its env preamble is incompatible with the tag-era engine.** It exports
   `RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 PAR_RAMPS=22` — v2.4/v2.5-era
   dials. With the root on `PYTHONPATH` the probe then gets one step further and **HALTS**
   (`transcripts/step4d_probe_full.txt`):
   `v0surf FROZEN-SIGNATURE HALT: this build's config signature cf0fc631… is NOT in data/v0surf.pkl
   (frozen: 41af7326…, 4405cba2…)`. Also a guard doing its job — but it means the restore-verifier's
   own preamble is the thing the frozen surface rejects.
3. **Its expectations are hand-typed and stale.** Under a bare env the probe runs clean and returns
   Maric `1356.96` / Langdon `782.55`; the script asserts `1271` / `567`. Those numbers described the
   rounds they were typed for. This is a textbook **P4** violator (*"assert the relationship, never
   this month's number"*) still sitting in the tree unretired.

**This is a live-estate condition, not a tag artefact.** `verify_restore.sh` is **byte-identical** at
the tag and at the current head — md5 `cc481bd82407936bd46592d89c64e47c` in both. The estate's
scripted restore-verify, named in CONTEXT_BUDGET_RULES §1 as a required kickoff asset, produces a
meaningless FAIL today.

### F5 — MATERIAL, REPRODUCIBILITY. The committed book does not satisfy its own seal — at the tag AND at HEAD — and cannot, by construction.

`data/book_stable_seal.json` at the tag pins `stable_sha256 86a82e6e…`, `n_players 2650`,
`head 5ac6780f`, `store cb38ef11`. Two different questions, two different answers
(`transcripts/step8_book_seal.txt`, and step 9 below):

| what was checked | result |
|---|---|
| a **freshly regenerated** gate-mode book at the tag, via the tag's own `reseal_bake.py --check` | **PASS** — `stable 86a82e6ebce66844`, `n 2650`, head/store/config all matching, every field |
| the **committed** `engine/rl_after/s4_matrix.json` bytes that the restore actually brings back | **SEAL MISMATCH** — `stable 79fdbb02…`, **2,647** rows, not 2,650 |

The cause is visible in the file: **its top-level keys are CPython `id()` values**
(`'140119988848320'`, `'140119988639104'`, …). Three consequences follow directly. The raw file is
not byte-reproducible across processes (rebuilt md5 `f98efdea…` vs committed `afeef743…`). An `id()`
collision — an object freed and its address reused — **silently drops a row**, which is why the
committed file carries 2,647 of the 2,650 rows the generator produced. And the seal can therefore
only ever be verified against a regenerated book, never against the committed one.

**Control, and it is the uncomfortable half:** the LIVE head's committed `s4_matrix.json` is
byte-identical to the tag's (`afeef743…`, same 2,647 rows) and mismatches the LIVE seal as well
(live seal `stable 9f46aba3…`). The committed book is a decorative copy in both trees.

For the rollback this is actionable and simple: **after a rollback the book must be REGENERATED, not
trusted as restored bytes.** Measured cost: 133 s to rebuild, 136 s to re-verify the seal, and the
regenerated book at the tag seals green.

### F6 — OBSERVATION, live estate, outside this drill's scope. The live book seal is one engine-move stale.

`data/book_stable_seal.json` at HEAD records `head_md5 1867e953` (the ACT B re-seal, 2026-08-20). The
live `engine/rl_after/_merged_recover.py` is `3af8c1f7` — moved on 2026-08-21 by the staircase flip
and PACKAGE 3a. The book is engine-`ev()`-derived, so the seal is behind its engine. Recorded here
because the drill measured it; repairing it is an owner/register matter, not a fire-drill act.

### F7 — MINOR. The tag-era self-test's F1 leg has a known, since-repaired defect. 96 rows, and none of them are the board's fault.

`one_source_selftest.py` on the rebuilt restored world: **126 PASS / 13 FAIL**
(`transcripts/selftest_restored_tag_full.txt`). Guard 5 inside it passed; F2 book-parity passed with
0 mismatches. The F1 export-parity leg failed with 96 mismatches, all young high-value rows
(sheezel, ashcroft, wanganeen-milera, …).

The board is not at fault — it rebuilt byte-exact three times. The **instrument** is, and the LIVE
tree says so in its own words. The live `one_source_selftest.py` (md5 `278520be…` vs the tag's
`2ecf7a35…`) carries this comment at exactly that block:

> *"This block used to call ev() at the five as-of years and nothing else, under the comment
> 'replicate the export's as-of sequence'. It did not replicate it. rl_export.py does three further
> things around the same five calls, and all three change what the NEXT row computes… Without the
> wrap, the LEG-E lens state and the LEG-F3 pedigree anchor leak across rows."*

The tag carries the pre-fix version. Not a restore failure, not a board defect, and already repaired
upstream.

Two of the other 13 — `FROZEN-RULER curve bytes == contract file md5 78ad9842` and
`FROZEN-RULER curve payload md5=9729f0c5 == contract` — are **downstream of F1's stale contract**, the
same root cause, not a separate one.

### F8 — OBSERVATION. Ten of the thirteen self-test reds are red today too.

Live-head control, same build + same self-test, in a scratch copy (`transcripts/step7_live_control.txt`,
`transcripts/selftest_live_control_full.txt`): **128 PASS / 11 FAIL.** The failing families are the
`LEG A fade` zero-evidence check and the `#326` per-division level anchors (10 live, 9 on the tag).
Those are a pre-existing instrument condition of the estate, unrelated to rollback. The control also
rebuilt the live board byte-exact to its pin (`b3e8da99bc7f632e5d1eebc732f9cf01`), which is what makes
the comparison trustworthy.

### F9 — POSITIVE, measured. The env pin is intact; there is no tag-era environment finding.

The brief anticipated one. There is none: numpy `2.4.4` + bundled OpenBLAS
`05c9f9eb89ee68a4b9d673184fa91c99587e736392c0c2d49180a8aa5303d080` on `/root/rl_venv312`, byte-exact
to `bootstrap.sh`'s pin. Stated as a measurement with a shelf life: the day this box drifts off the
pin, §4's byte-parity result expires and F5's regeneration requirement becomes the whole story.

### F10 — POSITIVE. The drill held P3.

The build lock was held by another seat throughout (`land-round-19205`, R24 rehearsal sandbox, since
`2026-08-21T10:49:54Z`). No shared surface was written. Every write this drill made went to
`/tmp/…/scratchpad/p4b/` or to this evidence directory.

---

## 6. WHAT THIS DRILL DID NOT PROVE

Stated plainly, so the retirement era does not lean on more than was measured.

- **The live rollback sequence has never been executed.** `EMERGENCY_ROLLBACK_RUNBOOK.md` is written
  from a scratch rehearsal. Its §5a contract re-stamp is written as a shape, not as a tested
  one-liner: `release_contract.restamp_dynamic` takes a season-state argument and the correct call
  for a rollback (as against an advance) has not been exercised. The first real rollback should
  expect to spend its time there — and per PLAN_v6 2a.3 must not improvise it under pressure.
- **`bootstrap.sh` was not run** (F2), so the workspace half of a rollback is proven necessary but not
  proven sufficient.
- **This was a rollback across an engine + board move, not across a fitted-artifact move.** All six
  frozen artifacts were byte-identical between the tag and HEAD, so the hardest case for Guard 5's
  loaded-path leg was not exercised.
- **4c is a different gate and stays different.** This drill is a byte-restore. PLAN_v6 4c requires a
  switch-set REBUILD reproducing a historical board byte-exact, *"never a byte-restore, which is
  precisely the leg the record proved blind to silent deletion."* §4's byte-exact rebuild is
  encouraging for 4c; it is not 4c, and F5 is a live example of exactly the silent-deletion class 4c
  exists to catch (three rows gone from a committed derived artifact, no gate red).

---

## 7. FILES

```
FIRE_DRILL.md                       this page
EMERGENCY_ROLLBACK_RUNBOOK.md       the live sequence — WRITTEN, NOT EXECUTED
scripts/                            every script the drill ran, verbatim
transcripts/
  step1_extract.txt                 the byte restore
  step2_hashes.txt                  all 13 pins compared
  step3_guards.txt                  Guard 5 + fv + ruling-config on the restored bytes
  step3b_contract_check.txt         the contract verifier's rejection (F1)
  step3c_live_control.txt           the same verifier PASSING on the current head
  step4_verify_restore.txt          verify_restore.sh, and the run_panel Guard 5 halt (F2)
  step4b_diag.txt                   the muzzled stderr, unmuzzled (F4.1)
  step4d_probe_full.txt             the frozen-signature halt + the true named-player values (F4.2/3)
  step5_rebuild.txt                 rebuild-from-source, canonical + bare
  step6_selftest.txt                rebuild #2, book regen, one_source_selftest
  step7_live_control.txt            the live-head control build + self-test (F8)
  step8_book_seal.txt               reseal_bake.py --check on the restored tree (F5, green half)
  step9_book_bytes.txt              the committed book vs its seal, tag and live (F5, red half)
  selftest_restored_tag_full.txt    full self-test output, restored tag world
  selftest_live_control_full.txt    full self-test output, live head control
```

Scratch working tree (not committed, deliberately):
`/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/p4b/`.
No `RL_`- or `PAR_`-prefixed variable was invented by this drill; every one used appears in the
tag's own scripts.
