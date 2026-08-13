# STEP 0 — THE CONTROL AT ENTRY (PREREG P1, THE STOP-GATE)

**ORDER 29 · branch `land/order-29` · 2026-08-13 · build seat (second seat; the first died on an API
error immediately after committing the prereg).**

> ## P1 — HELD.
> A full board rebuild from a clean staged copy of this branch's engine, with the grace dial at its
> committed default (**OFF**), reproduces the live board **`88ce647f531030d8d2e094188b258191`**
> byte-exactly.

## WHY THIS FILE EXISTS AND WHY IT IS FIRST

The order is absolute and it was nearly lost. The first seat edited the store — the unflag-three — and
died before running this control. Had that control then been run, it would have been run on a tree
whose store had already moved, and it would have proven nothing: a control that shares the change it
is controlling for is not a control. That uncommitted edit died with its worktree.

**This seat therefore started from a clean tree and ran the control BEFORE touching a single store
byte.** The entry-state hashes below are the proof that the tree was untouched when the control ran.

## THE ENTRY STATE, HASHED BEFORE THE BUILD

| artifact | md5 at entry | expected (prereg §0 / ORDER 28) | |
|---|---|---|---|
| `engine/rl_after/rl_model_data.json` (store) | `d9a24282357cf3083b1640466e3ecd83` | `d9a24282357cf3083b1640466e3ecd83` | **match** |
| `engine/rl_after/rl_app_data.json` (live board) | `88ce647f531030d8d2e094188b258191` | `88ce647f531030d8d2e094188b258191` | **match** |
| `engine/rl_after/pvc_curve_v2.json` | `f6f3027fc56615fc77cd455638a5fa79` | — | recorded |
| `engine/rl_after/rl_model.py` | `5d1e7b7a8172c58cb2c8c49a0aaad77a` | `5d1e7b7a` (ORDER 28 post) | **match** |
| `engine/rl_after/_merged_recover.py` | `e51098648c1ccb6951b30d57d9aac3fe` | `e5109864` (ORDER 28 post) | **match** |

`git status --porcelain` was **empty** at the moment of the build. The branch tip was `a19525d`
(the prereg commit), reset hard to `origin/land/order-29`.

## THE RUN

Harness: `o29/bb.sh` (scratch workspace; the checkout is never written). The engine's `rl_after` and
`forward_valuation` are copied into a fresh scratch dir together with the four repo-anchored helpers
`bootstrap.sh` seeds, and `rl_export.py` is run there under the pinned environment:

```
PATH=/root/rl_venv312/bin:$PATH                    (pinned venv, numpy 2.4.4 bundled-OpenBLAS pin)
RL_REPO=<checkout>  RL_FV=<staged forward_valuation>  PYTHONHASHSEED=0
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1     (FULL FIVE-VAR PINNING, the proven fix)
RL_GAMMA=1.0 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
RL_GRACE=0
```

| run | tree | dial | `rl_app_data.json` md5 | verdict |
|---|---|---|---|---|
| **entry0** | clean `land/order-29` @ `a19525d`, store `d9a24282` | `RL_GRACE=0` | **`88ce647f531030d8d2e094188b258191`** | **BYTE-IDENTICAL — P1 HELD** |

Wall time **1m57s** under full five-var pinning and sequential execution — against the *1h53m without
finishing* that the unpinned configuration cost ORDER 28. The environment fix holds.

Provenance recorded by the run itself (`export_stderr.txt`): `rl_model_md5 5d1e7b7a8172c58cb2c8c49a0aaad77a`,
`distribution_pricing_md5 33e07a9ee66a29e9d8ef3dc45cca52f6`, `config_manifest_identity bf012105…`.
The board stamped `src=d9a24282 (read-only)` — the store it read is the store hashed above.

## WHAT THIS CONTROL DOES AND DOES NOT LICENCE

It licences exactly one claim: **every divergence measured from here on is caused by a change this
build makes, not by the harness, the venv, the box, or the staging.** The harness is now known to
reproduce the live board from this tree.

It does **not** prove anything about the dial ON, the store edit, the curve, or the numéraire. Those
are the steps that follow, each with its own control.

**The store is untouched at the moment this file is committed.** Step 1 moves it, and not before.
