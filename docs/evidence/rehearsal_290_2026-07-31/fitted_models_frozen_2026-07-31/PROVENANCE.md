# FROZEN FITTED MODELS — the ruled travel substrate for L6 and the landing

**Seam ruling R-A, 2026-07-31 ([#290 issuecomment-5144017860](https://github.com/lukemcalister10/afl-rl-engine/issues/290#issuecomment-5144017860)), owner-reversible.**
N16's remedy, extended from the v0 surface to the fitted models: **they ride the same OpenBLAS path that produced the v0surf episode, so they travel as BYTES.** This file is that freeze's provenance record; the artifacts are committed beside it.

Mirrors `v0surf_frozen_2026-07-31/` exactly: bytes + md5 + provenance naming the machine.

---

## THE ARTIFACTS

**Three fitted models, as ruled — plus one co-emitted pair member, disclosed.**

| artifact | path when live | **md5** | git blob | size | what it is |
|---|---|---|---|---|---|
| **`peak_model_v4.pkl`** | `engine/rl_after/peak_model_v4.pkl` | **`f305fe5330222f4fa14d3654a0e91ef7`** | `00f906ac782c` | 1,341,030 | model 1 — **retrained at L4** on this substrate |
| **`cm_400.pkl`** | `data/cm_400.pkl` | **`34faa8659cc8f19794f5cb9584fa19b2`** | `be0f158d2fd0` | 4,174,555 | model 2 — the band. **SHIPPED artifact, not retrained** (see below) |
| **`q97m.pkl`** | `data/q97m.pkl` | **`cfdc73216c099e5e8f1fda3968f31c00`** | `8346608c9605` | 387,567 | model 3 — the q97 ceiling. **SHIPPED artifact, not refitted** (see below) |
| `pvc_snapshot.json` | `engine/rl_after/pvc_snapshot.json` | `ade79790efc8ad4585c2c6800a935eaa` | `74c376784b67` | 855 | **not a model** — peak's co-emitted train-time PVC |

**Why `pvc_snapshot.json` is here although R-A named three models.** The build's own law is that it and `peak_model_v4.pkl` are *"co-generated so they can never drift apart"*, and the anti-skew rule forbids re-pointing the snapshot alone. Freezing the model without its snapshot would freeze half a pair. Disclosed as an addition to the ruled three, not folded in silently; one word removes it.

Every copy above was verified **byte-identical to the live tree** at freeze time (`cmp`, 4 of 4).

## THE `.srcmd5` INPUTS — as R-A requires

The two tier-2 stamp files present in the tree at freeze time, captured because `git diff` cannot carry them and `L4_state.diff` therefore does not (stated in `L4_build/L4_state.diff.BASE`):

| file | md5 |
|---|---|
| `peak_model_v4.pkl.srcmd5` | `d14f0f12…` |
| `pvc_snapshot.json.srcmd5` | `aaccad1c…` |

They are build products of `build_peak_model_v4.py` (31s) and regenerate on any re-run. They are captured so a reconstruction can be checked, **not** because they are inputs to a fit.

## THE SUBSTRATE THESE WERE FITTED / MEASURED ON

| | |
|---|---|
| store | `81d2470440a80f72afea4405e94338c5` |
| v0surf | `84fb0cde29f36c1a91d440e63b753c3c` (N16's frozen surface) |
| γ | **1.0** |
| curve payload | `e69a3f38` |
| `fv` identity | `d920557ef21d0eec…` (post-L4) |
| board built from it | `944abbd34223875229874e2d32894565` |

## THE MACHINE — measured at freeze time

| | |
|---|---|
| CPU | `Intel(R) Xeon(R) Processor @ 2.80GHz` — family 6, **model 85 (Skylake-SP)** |
| numpy AVX-512 tiers | `AVX512F`, `AVX512CD`, `AVX512VL`, `AVX512BW`, `AVX512DQ`, `AVX512VNNI` |
| python | 3.12.3 |
| numpy | 2.4.4 · scipy-openblas **0.3.31.188.0** · OpenBLAS byte-pin `05c9f9eb` (item 392, asserted green by `bootstrap.sh`) |
| scipy / sklearn / openpyxl | 1.17.1 / 1.8.0 / 3.1.5 — 5/5 re-proven independently, not from the script's PASS line |

**This is the same class as the v0surf freeze's HOST 1** (`Xeon @2.80GHz`, AVX-512 SKX/CLX). It is corroborated empirically rather than by CPU string alone: rebuilding the pre-L4 fitted artifacts here produced board **`92e397bd`**, **byte-exact to the board the T1 hand-back recorded on host 1**. Compute matches.

**Recorded honestly:** `/proc/uptime` read **102.88s** at freeze time. Containers in this environment have migrated hosts mid-session before (v552 provenance, host 1 → host 2), and a low uptime is the signature that was noticed then. The byte-exact T1 board reproduction above is the evidence that whatever happened, **the compute path did not move**. Stated so a successor is not surprised by it.

## WHAT THE FREEZE DOES AND DOES NOT GUARANTEE

**GUARANTEES:** these exact bytes travel to L6, to the landing, and to any other machine, so no leg has to refit and no figure depends on a refit succeeding identically elsewhere. That is precisely what the v0surf freeze bought, and it is the whole content of N16.

**DOES NOT GUARANTEE reproducibility.** Two of the three are shipped artifacts whose own fits are **not** reproducible here, measured:

| model | on-box bit-stability (2 fresh processes) | reproduces its shipped pin? |
|---|---|---|
| `peak_model_v4.pkl` | **byte-identical** | new by design — L4 re-derivation, `f305fe53` vs pre-L4 `b763f59e` |
| `cm_400.pkl` | **byte-identical** (`3c568d86` twice) | **NO** — fresh `3c568d86` vs pinned `9804bc48`, like-for-like serializer |
| `q97m.pkl` | (declared lane) | **NO** — `refit_q97m.py --verify` exit 3: `ba86aae8` vs pin `cfdc7321` |

So the band and q97m are frozen **as shipped**, and the freeze guarantees they will *travel* identically — it does not make them *regenerable*. Anyone who refits either one gets a different artifact and a moved board. That is the state of the world, recorded rather than smoothed.

## WHY THE BAND AND q97m WERE NOT RETRAINED AT L4

- **band** — a refit does not reproduce the shipped artifact and would move the board; the cross-machine question is open. Measured and **presented, not taken** (L4 filing).
- **q97m** — its own declared lane is **BAKE-ONLY** (`RL_BAKE_REFIT=1 refit_q97m.py --bake`) and the tree is **unbakeable** until the EXECUTION word. `--verify` was run instead, which writes nothing.

## NOT IN THIS FREEZE

`bust_prior_table.json` (pinned `5942aa6a`) is **not** frozen here. It is not a fitted model, and it **has no writer anywhere in the tree** — the pinned `_fitted_note` claims `build_peak_model_v4.py` regenerates it, and measured, that file reads it at line 16 and nothing writes it. That false provenance is docketed (R-D); correcting a pinned note is a landing act.

## NO GATE MOVES

Per R-A: this freeze re-stamps nothing and moves no gate. It is a byte record beside the live tree. The live pins are unchanged and continue to match disk.
