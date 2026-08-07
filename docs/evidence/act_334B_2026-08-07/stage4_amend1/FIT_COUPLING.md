# STAGE 4 AMENDMENT 1 — FIT COUPLING: the verdict is NONE, and it is measured

## (a) The static argument — the change never leaves `sitout_ev`

The directive's rule: if the change stays inside `sitout_ev`, re-verify cheaply with the same three-signature
check stage 4 used; if it escapes `sitout_ev`, re-do the full coupling proof.

**It does not escape.** The amendment adds four module-level objects — the dial `SUR_W`, the normaliser
`_RHO_SIT_BAR`, the curve `_rho_res` and the demand `_surprise` — and every one of them is consumed inside
`sitout_ev`'s exponent and nowhere else. Verified by grep on the built engine file
`engine/rl_after/_merged_recover.py` (line numbers as shipped; comment mentions excluded):

| symbol | defined | referenced in code | where |
|---|---|---|---|
| `SUR_W` | 1855 | **once** | 1866, inside `_surprise` |
| `_RHO_SIT_BAR` | 1856 | **once** | 1866, inside `_surprise` |
| `_rho_res` | 1857 | **once** | 1866, inside `_surprise` |
| `_surprise` | 1860 | **once** | 1875, inside `sitout_ev` |
| `sitout_ev` | 1867 | **once** | 1956, the `ns==0` arm of `ev()` |

A repo-wide grep for `SUR_W`, `_surprise` and `_rho_res` across `engine/` returns **no hit in any file other
than `_merged_recover.py`**. The chain is a straight line with no branches: dial → `_surprise` →
`sitout_ev` → `ev()`, and it stops there.

`_build_v0_curve` fits `_v0_raw` (= `raw_ev × iso` at draft age) over the ND roster and **never calls
`ev()`**. There is therefore no path by which `RL_SUR_W` can reach the year-zero surface fit, and
`RL_SUR_W` is **not** a `_V0SURF_GATES` key. **No refit is owed.**

## (b) The measurement — three signatures, one result

Proven by measurement rather than by reading. A **declared refit** (`RL_V0SURF_REFIT=1`,
`refit_v0surf.py --verify`, dev shell with `RL_CONFIG_MODE` unset, as a declared experiment must be) was run
at `RL_SUR_W` **0.0 / 5.0 / 20.0** — the kill-switch value, the shipped value, and **four times the shipped
magnitude**.

| `RL_SUR_W` | config signature | fitted-surface md5 | vs committed pin |
|---|---|---|---|
| 0.0 | `3e8e50de5103` | `9713ec6c83270ab916bb4a5e3ded6cb3` | **REPRODUCES** |
| **5.0 (shipped)** | `3e8e50de5103` | `9713ec6c83270ab916bb4a5e3ded6cb3` | **REPRODUCES** |
| 20.0 | `3e8e50de5103` | `9713ec6c83270ab916bb4a5e3ded6cb3` | **REPRODUCES** |

All three produced the **identical config signature** and **byte-identical fitted surfaces**, and that md5 is
**the current committed pin**. Full log: `fit_coupling_refit_log.txt`.

That single run does double duty, exactly as stage 4's did: it re-verifies the fit class against the current
pickle on this box, and it proves the dial cannot move the surface even at four times the shipped magnitude.

**`v0surf` is UNMOVED and the pickle was not rewritten.**

## (c) Why the dial is a manifest var but not a fit gate

`_V0SURF_GATES` enumerates the variables whose change *invalidates the fitted year-zero surface*.
`data/model_config.json` enumerates every variable with **model semantics**, fit-coupled or not.
`RL_SUR_W` is squarely the second and demonstrably not the first: it changes the board (61 vars, config
`38a73675b28f`, board `b56bbdde`) and provably does not change the fit (§b). Stage 4 drew the same line for
`RL_PED_BAR`, on the same function, with the same evidence.
