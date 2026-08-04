# L4 — THE FIRST LAWFUL IN-REPO BUILD. Chain green, census proven, three fitted models measured.

**#290, 2026-07-31.** Substrate named on every figure below: **store `81d24704` · v0surf `84fb0cde` · γ 1.0 · curve payload `e69a3f38`.** Base of the state diff: **`206a5f5`** (annotated beside it, per the v553 clause).

**Nothing landed. The tree is unbakeable and the EXECUTION word remains withheld.** Every engine act ran serially behind `tools/preboot_assert.sh`, which passed before each.

## THE HEADLINE — it runs, and it is cheap

The runbook priced L4 as **UNMEASURED — first lawful build**, with `RL_PRIOR_TREES=400` and the GBR path flagged as the expensive parts.

| act | measured |
|---|---|
| **`build_peak_model_v4.py`** — the first lawful in-repo build | **31s** |
| band refit (`PR.retrain()`, 400 trees) | **61s / 60s** |
| `refit_q97m.py --verify` | **51s** |
| full chain — bootstrap → board → book → selftest | **281s** (board 85s · book 124s · selftest 71s) |
| the control chain (for the delta) | 276s |

**L4 exit:**

```
bootstrap 0 · board 0 · book 0 · selftest 96 PASS / 1 FAIL
  the single FAIL = G-Y0 13.919% vs the 3.500% ceiling — the ACCEPTED WAYPOINT
board  92e397bd (control) -> 944abbd3 (L4)
```

The PASS/FAIL **label sets are identical to L3's committed exit** — 96/1, same checks. (An earlier count of "97" was my own loose grep; corrected by counting the way the record counts.)

## THE THREE DEFECTS — reproduced at source BEFORE they were fixed

| # | the defect | reproduced |
|---|---|---|
| 1 | `range(1,100)` snapshot loop against a 65-key live PVC | **`KeyError: 66`**, exactly as the runbook records; `MA.PVC` measured at **65 keys, 1..65 contiguous** |
| 2 | `dob_corrected.json` read from the workspace | **ABSENT** from the workspace and **untracked in the repo (0 occurrences)** — so bootstrap never copied it and this build could not run at all |
| 3 | `bust_prior_table.json` read from `…/forward_valuation/` | **ABSENT** there; **PRESENT** at `…/rl_after/`, where `bootstrap.sh` actually copies it |

Fixes applied in that order. Fix 1 does **not** substitute one literal for another: the domain is derived from `MA.PVC` and **asserted** to be the ruled shape (1..64 + pool index 65), so a domain change is loud rather than silently reshaping a pinned artifact — the I.2 lesson applied.

## THE C.1 IDENTITY HAZARD FIRED AGAIN, AS AT L1 AND T1

One edit inside `engine/forward_valuation/` moved the `fv` identity and Guard 5 refused to boot. Re-pinned in **both** carriers in one act, **field-level and byte-surgical** (the T1 seat's slip #1 was a wholesale JSON rewrite; not repeated):

```
expected_boot.fv                95277b76… -> d920557e…
release_contract.identities.fv  95277b76… -> d920557e…
asserted: exactly 1 occurrence per file · line count unchanged · byte length unchanged
```

**Sealed history untouched:** `release_lineage.json` and `finalization_state.json` both `git`-unmodified through every step; the ten historical `45b207c0` occurrences unmoved (4|4|4, 6|6|6). The 8/8 `release_contract.identities` mirror re-verified by content.

## THE AGE-SOURCE CENSUS — the hard acceptance, and it works

Emitted by the build, asserted to sum, and **it reproduces the Addendum 4 baseline exactly**:

| store level | measured | Addendum 4 baseline |
|---|---|---|
| store rows | **2,651** | 2,651 |
| `_by` present | **2,349** | 2,349 |
| `_bd` present | **848** | 848 |
| `_by` missing | **302** | 302 |
| `_bd` ⊆ `_by` | **True** | 848/848 |

**Training level — the acceptance denominator is the training population, 6,339 rows / 1,222 players:**

| class | rows | of 6,339 | players |
|---|---|---|---|
| REAL_DATE (`_bd`) | 1,669 | 26.329% | 134 |
| REAL_YEAR (`_by` only) | 4,197 | 66.209% | 987 |
| **FALLBACK** (18.0 + years-since-debut) | **473** | **7.462%** | **102** |
| **sums to denominator** | **6,339 = 6,339** | **OK** | |

This is exactly what runbook §5.1 asked for: the lane dry-run at *current* coverage, census emitted and counted, **pricing the courier's gap before any data arrives**.

**A FINDING THE COURIER ACCEPTANCE NEEDS.** The acceptance says the FALLBACK count *"must fall by EXACTLY the number of rows written"* — 302. At **store level** that is right. At **training level** the same courier clears **473 rows across 102 players**, because one player contributes many training rows, and only 102 of the 302 fall inside the debut window. **So the HALT rule must name which denominator it counts in, or the leg HALTs on a true result.** Both numbers are now emitted side by side.

## ACT 4 (bias-2) — a measured NO-OP for this build, not a skipped step

| measured | |
|---|---|
| peak-model training window | debut **2006–2015** |
| players in window | **1,226** of 2,651 position-mapped store rows (1,222 contribute ≥1 row; 4 contribute none) |
| of those, debut ≤ 2005 | **0** |
| store players debuting 2004 (the 2003 class core) | **107**, **0** of them inside the window |
| training-window scoring rows at year 2004 | **0** |
| store scoring span | **2005–2026; 2004 absent entirely** |

The missing-2004 understatement **cannot reach this build's teaching quantities**: no 2003-class row is in the peak model's training population and no 2004 season exists anywhere in the store. Bias-2 remains live for the **conditional prior**, whose population is the 13,221 rows T1 acted on — a different leg, already done.

## THE THREE FITTED MODELS — and one prior claim corrected

Full detail in `FITTED_ARTIFACT_REPRODUCTION.txt`. Summary:

| | on-box determinism (2 fresh processes) | reproduces its shipped pin? |
|---|---|---|
| `peak_model_v4.pkl` | **byte-identical** | new by design — `f305fe53` vs pre-L4 `b763f59e` |
| `cm_400.pkl` (band) | **byte-identical** | **NO** — `3c568d86` vs `9804bc48`, like-for-like serializer |
| `q97m.pkl` | (declared lane) | **NO** — `ba86aae8` vs pin `cfdc7321`, `--verify` exit 3 |

**A correction to a claim on the record.** `wire_redesign.py`'s docstring states of the band refit: *"a refit is not bit-stable even on one box"*. **Measured here, that is false** — two fresh-process retrains produced identical bytes on this box and pinned stack. The docstring's *other* half stands and I confirmed it fairly (same serializer both sides): a fresh refit does **not** reproduce the shipped band.

**What this does NOT settle: the cross-machine question.** The band is a RandomForest and q97m a GBR, both through OpenBLAS `DYNAMIC_ARCH` — the exact mechanism that made v0surf machine-sensitive (N16). On-box determinism is not cross-machine determinism, and this very container migrated hosts mid-session once already. **The remedy already ruled for v0surf — fit once, freeze the bytes, travel them, name the md5 in every figure — is the candidate remedy for all three, and it is a seam call. Not taken here.**

## THE BOARD DELTA — control rebuilt here, not inherited

Detail in `BOARD_DELTA_L4.txt`. The control (pre-L4 fitted artifacts, full chain re-run) came out at **`92e397bd`** — **byte-exact to the board md5 the T1 hand-back recorded.** So this container reproduces the predecessor's board exactly, and the delta is L4's effect and not the machine's.

| | |
|---|---|
| movers | **65 of 804 = 8.1%** |
| direction | **0 up / 65 down** |
| median / p90 / max relative | 0.041% / 0.158% / **0.433%** |
| total ev | 755,941 → 755,874 = **−0.009%** |

Every mover is a **single integer unit** — a rounding-boundary ripple, not a revaluation. **The one-directional pattern (65 down, 0 up) is named rather than waved through:** a symmetric ripple would not be one-sided. It is far too small to matter to anything this job steers by, and it is **not explained here** — recorded for L8, where a mover with no named cause HALTs.

**G-Y0 unchanged at 13.919%.** As at T1: L4 retrains the player stack; G-Y0 measures the year-zero pick-curve residual governed by the frozen surface and the curve. **A green L4 gate is not progress toward the 2.000% bar.**

## WHAT L4 DID *NOT* DO, each with its measured reason

| artifact | state | reason |
|---|---|---|
| `cm_400.pkl` (band) | **unmoved at `34faa865`** | a fresh refit does not reproduce it and would move the board; the cross-machine question above is open. **A seam call, presented not taken.** |
| `q97m.pkl` | **unmoved at `cfdc7321`** | its own declared lane refuses: refit is **BAKE-ONLY** (`RL_BAKE_REFIT=1`), and the tree is unbakeable until the EXECUTION word. `--verify` was run instead. |
| `bust_prior_table.json` | **unmoved at `5942aa6a`** | **it has no writer.** See below. |

### THE bust_prior FINDING — a pinned note asserting a provenance that does not exist

`data/expected_boot.json`'s `_fitted_note` states `bust_prior_table.json` is *"regenerated only by `build_peak_model_v4.py` at a bake"*, and the runbook's L4 act 3 repeats it. **Measured: `build_peak_model_v4.py` READS that file at `:16` and never writes it, and no file anywhere in the tree writes it.** So L4's act 3 is **not performable** for that artifact as specified.

This is the hazard-1 shape — a true-sounding provenance attached to the wrong mechanism — living inside a **pinned** note, which is where it is most likely to be believed. Docketed; not silently worked around, and not fixed here because correcting a pinned note is a landing act.

## THE TRAINING-STORE STAMPS (act 6)

Emitted beside the artifacts as `training_store_stamp.json`: store md5 · v0surf md5 · γ · curve payload · PVC domain and key count · training rows · training window · and the md5 of each artifact this build produced. This closes the gap the runbook names — *today `cm_400`, `q97m`, `peak_model_v4`, `pvc_snapshot`, `bust_prior_table` are pinned by md5 and **none** records the store or curve it was trained on.*

## MY OWN SLIP, RECORDED

My first chain invoked `rl_export.py` **by its repo path** with the workspace as cwd. The board built correctly all the way through — *"PARITY GATE PASS: all 804 active board values == engine gated ev()"* — and then died at the final stamping step on a `FileNotFoundError`, because `single_source` resolves the artifact path against the repo. **The engine was right and my harness was wrong.** CI does `cd /home/claude/rl_workspace/rl_after; python3 rl_export.py` — the workspace copies. Corrected and re-run. Cost: one wasted 275s chain, recorded.

## COSTS, ACTUAL

Build 31s · band refits 61s + 60s · q97m verify 51s · chains 281s + 276s + 281s (+ one wasted 275s from my slip) · probes ~10s. **Every engine act serial, preboot assert PASS before each. Zero parallel engine runs.**
