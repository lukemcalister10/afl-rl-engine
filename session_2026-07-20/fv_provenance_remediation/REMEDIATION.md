# FORWARD-VALUATION PROVENANCE — FAIL-CLOSED REMEDIATION

**Bounded production fix for the `06d8af60 → d7a95e8d` 109-player wobble.** Import/provenance only — no
valuation mathematics, no §1b law, no parameter, no data, no board selection, no bake/tag/release.

## 0. Base / ancestry proof (STRICT START)

| Fact | Value |
|---|---|
| Fix branch base | `3055ea5ffdc390f81d5e17476a60fbb841f24cff` (env-pin commit #2, item 392) |
| Working tree at start | HEAD == `3055ea5`, clean |
| Diagnostic commit `7c6768e` merged/rebased in? | **NO** — read read-only via `git show`; never merged |
| Relationship to `origin/main` | **git-disjoint** (`git merge-base` = ∅); main is the stale 50-commit docs line whose `distribution_pricing.py` is the §1b-missing `21d530bf` |
| Strict `distribution_pricing.py` at base | `d0c8c69f` (with §1b), confirmed also on `15a9abd` — the bake-base checkout was correct |

The bad board did **not** come from a bad checkout. It came from the runtime importing a *stale workspace
copy* seeded from `main`, because `RL_FV` was unset and defaulted to the ambient workspace.

## 1. Root cause of record (verified same-host; cross-host PENDING)

`wire_redesign.py` / `par_redesign.py` defaulted `RL_FV` to `/home/claude/rl_workspace/forward_valuation`,
which `bootstrap.sh` seeds from **whatever branch is checked out at container start**. A previous `main`
bootstrap left the stale `21d530bf` `distribution_pricing.py` (missing the Leg-C §1b current-season DPP law)
there; a build with `RL_FV` unset imported it silently and the board diverged with **no guard firing** —
`data/expected_boot.json` pinned store/engine/q97m/v0surf but **not** the `forward_valuation` modules.
Confirmed live in this container: ambient `.../forward_valuation/distribution_pricing.py` = `21d530bf`
(0 §1b blends) while the checkout = `d0c8c69f` (4 §1b blends).

## 2. Canonical source-selection rule (the fix)

Implemented in `fv_provenance.resolve_fv()` and mirrored inline in `wire_redesign._resolve_fv` /
`par_redesign._resolve_fv` / `build_cohort_book`:

1. An explicit `RL_FV` wins — **but** Guard 5's loaded-path assertion verifies its identity == the pin, so
   an explicit-but-stale `RL_FV` **HALTS**; it is not trusted blindly.
2. Otherwise the **checked-out** `<RL_REPO>/engine/forward_valuation`.
3. Otherwise **HALT**. There is **no** ambient-workspace fallback — a canonical build never silently reads
   `/home/claude/rl_workspace/forward_valuation`.

rl_model resolves the same way: the hardcoded `sys.path.insert(0,'/home/claude/rl_after')` is removed from the
board-build FV chain; rl_model comes from the already-imported engine instance, else the explicit `RL_REPO`
checkout — never a hardcoded workspace path.

## 3. New pinned identity — what it covers

`data/expected_boot.json` gains:

```
"fv": "fa060917c8e5cd057c4248855c276f790764c1d4fee192b166c0218fc6c4db4f"
```

A canonical tree hash = sha256 over the **sorted relative paths + exact-byte sha256** of every `*.py` in
`engine/forward_valuation` — the **complete imported forward-valuation source set** (8 files:
build_cohort_book, build_peak_model_v4, conditional_prior, dist_redesign, distribution_pricing, par_build,
par_redesign, tail_restore). The identity changes when **any** imported forward-valuation source changes —
not `distribution_pricing.py` alone.

## 4. Guard 5 — checkout + loaded-path proofs

`boot_guard.assert_fv_provenance` / `fv_provenance_fails` (also folded into `assert_boot` block `(0g)`) assert
**both**:

1. **Checkout integrity** — `fv_identity(<repo>/engine/forward_valuation)` == pin.
2. **Loaded-path integrity** — `fv_identity(resolve_fv())` == pin, i.e. the **exact `RL_FV` directory the
   engine will import** == pin.

On mismatch / unresolved path it **HALTS** (never warns), naming the resolved `RL_FV`, the computed identity,
the expected identity, and the failure class (checkout drift / loaded-path drift / unresolved path).

## 5. Config enforcement fail-closed (JOB 4)

`rl_export.py`: in a canonical build (`RL_CONFIG_MODE=bake|gate`) config enforcement is fail-closed —
`config_manifest` must be importable (else HALT, replacing the old silent `except ImportError: pass`), its
module verified byte-identical to the checkout (shadow detection), its data file present under the resolved
repo, and `enforce()` must return an accepted config identity (reject-scan + manifest-hash-vs-pin inside).
Any failure **HALTS before board generation**. Dev-shell (no `RL_CONFIG_MODE`) stays available and is a no-op.

## 6. Provenance reporting (GREEN 2)

Before any board is generated, `rl_export.py` writes an `rl_app_data.provenance.json` sidecar and a one-line
`PROVENANCE …` stderr marker recording: `RL_FV`, the resolved directory, the full FV source-set identity
(+ per-file hashes), `distribution_pricing.py` path + md5, `rl_model` path + md5, and `config_manifest` path
+ identity — fingerprinting the exact import state that made the board.

## 7. Changed paths (import/provenance only)

```
fv_provenance.py                                  (NEW) canonical FV selection + identity + provenance report
boot_guard.py                                     Guard 5: FV checkout + loaded-path assertions
data/expected_boot.json                           + "fv" pin + note
bootstrap.sh                                       verify+report the copied FV tree vs the pin; seed fv_provenance/boot_guard
run_panel.sh                                       bind RL_FV to the checkout explicitly
engine/rl_after/rl_export.py                       fail-closed config + FV provenance + provenance record
engine/rl_after/wire_redesign.py                   fail-closed FV resolution (no ambient default)
engine/forward_valuation/par_redesign.py           fail-closed FV resolution; remove ambient/rl_after inserts
engine/forward_valuation/distribution_pricing.py   remove hardcoded /home/claude/rl_after insert (JOB 3 named file)
engine/forward_valuation/dist_redesign.py          remove hardcoded /home/claude/rl_after insert
engine/forward_valuation/conditional_prior.py      remove hardcoded /home/claude/rl_after insert
engine/forward_valuation/par_build.py              remove hardcoded /home/claude/rl_after insert
engine/forward_valuation/build_cohort_book.py      remove ambient dp path + rl_after insert (bake tool)
engine/forward_valuation/build_peak_model_v4.py    remove rl_after insert (bake tool)
.github/workflows/fv-provenance.yml               (NEW) permanent durable provenance CI (independent runner)
session_2026-07-20/fv_provenance_remediation/     (NEW) tests + fixtures + this proof
```

`engine/rl_after/rl_model.py` and `engine/rl_after/_merged_recover.py` are **UNTOUCHED**. The §1b law in
`distribution_pricing.py` is **UNCHANGED** (only import-plumbing lines edited; the byte-exact `06d8af60`
board proves it).

## 8. Red/Green results

See `RESULTS.json` (produced by `test_fv_provenance.py`) — filled in §10 below.

## 9. Pre-existing, OUT-OF-SCOPE condition (honest disclosure)

At `3055ea5` the **full** Guard 5 is already RED on an unrelated boot-pin drift: the checked-out
`rl_model.py` (`cc626d7d`) and `_merged_recover.py` (`904722cd`) advanced through the env-gated Legs E/F
(kill-switches, OFF in the balanced config) without the `rl_model`/`engine_head` pins in
`data/expected_boot.json` (`a5fd3d7d` / `40f43772`) being re-stamped — register **item 399, "stale-boot-pin
bug."** Reconciling those pins is a **bake** (re-stamp the engine pins / re-generate the display board), which
this task explicitly forbids ("do not select or promote a final v2.11 board … do not re-pin the board … do
not bake/tag/release"). This fix therefore leaves those pins untouched and proves the forward-valuation
provenance path **in isolation** (`assert_fv_provenance` + the strict board build, which do not depend on the
drifting `rl_model`/`engine_head` pins). The permanent CI workflow does the same, so the independent-runner
proof is not blocked by this pre-existing condition.

## 10. Verified results (this environment)

**Red/green suite — `test_fv_provenance.py` → 7/7 PASS** (`RESULTS.json`):

| Scenario | Result |
|---|---|
| GREEN 1 strict board | rc=0, board **06d8af60**, active **804**, Σv **752427**, Sheezel **7964**, 0 movers |
| GREEN 2 provenance record | all fields present; `fv_identity == pin`; stderr `PROVENANCE` marker; sidecar written |
| RED 1 stale ambient ignored | stale `21d530bf` seeded at the former default path → board **06d8af60** (never `d7a95e8d`); files unchanged |
| RED 2 explicit stale RL_FV | HALT (loaded-path drift), no board, files unchanged |
| RED 3 sibling FV source drift | HALT (checkout drift — `conditional_prior.py` changed), no board, files unchanged |
| RED 4 config manifest fail-closed | 4a missing → HALT; 4b hash mismatch → HALT; no board, files unchanged |
| RED 5 foreign rl_model @ /home/claude/rl_after | never imported; board **06d8af60**; `rl_model_path` is the verified staging copy; files unchanged |

Every red path additionally verified: **no board written, no pin changed, no production file changed, no retry.**

**Scope confirmation (the fix itself):**
- `rl_model.py` and `_merged_recover.py`: **UNCHANGED** → zero player-value movers, no Leg-E/Leg-F logic change.
- No store / fitted-artifact (`*.pkl`) / curve (`pvc_curve*`) / UI / display change.
- `data/expected_boot.json`: only `"fv"` + `"_fv_note"` added; `board` (`270a2c5f`) and `config` (`c2d233ae`)
  pins **unchanged**.
- Strict balanced build reproduces **06d8af60 byte-exact** (0 movers vs the accepted reference).

**Regression (isolated from the pre-existing rl_model pin drift):**
- `config_manifest.py check` → PASS (hash `c2d233ae`, pin+stored consistent).
- `ruling_config_check.py` → PASS (RL_PVCFIT=0 + R3 bake-guard; RL_LTI_CLOCK=advance).
- `fv_provenance.py` self-check → checkout identity == pin.
- Full `boot_guard.assert_boot` → the **only** failure is the pre-existing `rl_model` pin drift (§9); the new FV
  checkout + loaded-path assertions PASS.

**Independent-runner proof:** `.github/workflows/fv-provenance.yml` runs this suite on every push/PR on a clean
GitHub `ubuntu-24.04` runner — see the PR checks for the fresh-host result.
