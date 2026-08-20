# BYTE-IDENTITY WITH THE DIAL OFF — THE PROOF

**ORDER 28 STEP 1.** The engine now carries the grace-A dial. This file is the proof that the dial,
**with `RL_GRACE` unset or `0`, is inert to the byte.**

## THE CLAIM

> A full board rebuild from a clean staged copy of the **modified** engine, with the dial present but
> OFF, reproduces the live board **`88ce647f531030d8d2e094188b258191`** exactly.

## THE METHOD

The checkout's `engine/rl_after` and `engine/forward_valuation` are copied into a fresh scratch
workspace (plus the four repo-anchored helpers `bootstrap.sh` seeds: `config_manifest.py`,
`fv_provenance.py`, `boot_guard.py`, `LTI_REGISTER.md`), and `rl_export.py` is run there under the
panel's own pinned environment:

```
RL_REPO=<checkout>  RL_FV=<staged forward_valuation>  PYTHONHASHSEED=0  OPENBLAS_NUM_THREADS=1
RL_GAMMA=1.0  RL_PICK1=3000  RL_RUCK_TAX=0.25  RL_RECENCY_DECAY=0.72  RL_PRIOR_TREES=400  PAR_RAMPS=22
RL_GRACE=<0 or 1>
python3 rl_export.py
```

Nothing in the checkout is written; the board that is compared is the one `rl_export.py` emits in the
scratch workspace.

## THE RUNS

| run | dial | `rl_app_data.json` md5 | verdict |
|---|---|---|---|
| **base0** — *pre-change control*, engine as committed on `origin/main` | n/a | `88ce647f531030d8d2e094188b258191` | the harness reproduces the live board |
| **off1** — **modified engine, dial OFF** | `RL_GRACE=0` | **`88ce647f531030d8d2e094188b258191`** | **BYTE-IDENTICAL — PASS** |
| **on1** — modified engine, dial ON | `RL_GRACE=1` | `0ce52771ed8f9ef326dd61f0e4aa71a8` | the variant board (step 3) |
| **on2** — modified engine, dial ON, independent rebuild | `RL_GRACE=1` | see `DETERMINISM.txt` | determinism check |

**`base0` is what makes `off1` non-vacuous**: the same harness, run against the *unmodified* engine,
produces the same md5 — so `off1`'s match is a statement about the engine change, not about a harness
that always prints `88ce647f`. And `on1` differing proves the dial is **reachable**: an inert-when-on
dial would have produced `88ce647f` three times and proved nothing.

## WHY IT IS IDENTITY BY CONSTRUCTION, NOT BY TOLERANCE

`disc_factor` gained one kwarg, `grace=0`:

```
if grace:
    k = max(0, int(k) - int(grace))
    if k <= 0: return 1.0
```

At `grace = 0` the branch is not entered at all, so the returned expression is the pre-order
`(1.0 + age_disc(a,d,lens))**k` evaluated on the pre-order `k` — the same float operations in the same
order. Every new call site passes a value that is `0` whenever `RL_GRACE` is off, because
`grace_years()` returns `0` on its first line in that case. There is no path on which the dial-off
engine performs an arithmetic operation the pre-order engine did not.

## THE FILES THAT MOVED

| file | pre-ORDER-28 md5 | post md5 |
|---|---|---|
| `engine/rl_after/rl_model.py` | `e5eb5e4405c09eebef45a9db89f014bc` | see `GATE28_out.txt` header |
| `engine/rl_after/_merged_recover.py` | `3f1468e5468462ab789e49aace264c90` | see `GATE28_out.txt` header |
| `engine/forward_valuation/distribution_pricing.py` | (recorded at gate) | see `GATE28_out.txt` header |

`engine/rl_after/rl_model_data.json` (store) and `engine/rl_after/rl_app_data.json` (board) are
**unmoved** and are asserted so at both entry and exit of the gate harness. **NOTHING IS LANDED.**

## THE DUPLICATE-LOOP FENCE

`rl_model.py::prod_floor` and `_merged_recover.py::_prod_floor_w4` are the parallel copy pair the
engine's own comment fences (`rl_model.py:994`, *"edit BOTH or neither"*). Both were edited, with the
identical two lines (`_gr = grace_years(p)` / `MA.grace_years(p)`, and `_gr` passed to `disc_factor`).
The byte-identity-off result is what proves neither edit leaked.
