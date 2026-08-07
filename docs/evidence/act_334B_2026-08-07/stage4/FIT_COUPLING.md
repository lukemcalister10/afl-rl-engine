# STAGE 4 — THE FIT-COUPLING PROOF

**QUESTION (directive §3).** Does the pedigree-conditioned evidence bar participate in the year-zero
surface fit path? Does it bind before the V0 guard / curve builds? Do its dials belong in
`_V0SURF_GATES`?

**VERDICT: NO, NO, NO.** `v0surf` is UNMOVED at `9713ec6c83270ab916bb4a5e3ded6cb3`, the pickle was not
rewritten, and `RL_PED_BAR` is deliberately absent from `_V0SURF_GATES`. Below is how that was proven,
in two independent ways — a static reachability argument and a three-sided measurement.

---

## (a) STATIC — one caller, and the fit does not go through it

`sitout_ev` is called from exactly **one** site in the whole checkout:

```
$ grep -rn "sitout_ev" --include=*.py .   (excluding docs/ and session_* history)
engine/rl_after/_merged_recover.py:1753(def)   <- the definition
engine/rl_after/_merged_recover.py:1838        <- `if ns==0: return round(sitout_ev(p,Y,e))`, inside ev()
```

`_build_v0_curve()` fits over `_v0_raw(p)` — the zero-evidence band start value, `raw_ev × iso` at draft
age, with the ASK1 ruck cap. It never calls `ev()`, never calls `sitout_ev`, and never reads `PED_BAR`.
The fit's inputs are the `_PVC0` pick curve, the ND roster `(pos, ageR, pick)`, and the `_V0SURF_GATES`
environment — none of which this change touches.

The direction of the dependency runs the other way and only the other way: `sitout_ev` READS
`entry_anchor(p) → v0_start(p) → _V0CURVE`, i.e. it consumes the frozen surface. Consumption is not
coupling. A dial that only reads the surface cannot move it.

## (b) MEASURED — the declared refit, three-sided

The engine's ONE committed fit path is `RL_V0SURF_REFIT=1` driving
`session_2026-07-18/legf6/scripts/refit_v0surf.py`. It was run in `--verify` mode (no write) at three
values of the dial spanning zero, shipped, and four times shipped:

```
export PATH=/root/rl_venv312/bin:$PATH
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export PYTHONPATH=/home/claude/rl_workspace/rl_after:/home/claude/rl_vendor
export RL_REPO=/home/claude/seamcheck_landing RL_FV=$RL_REPO/engine/forward_valuation
cd /home/claude/rl_workspace/rl_after            # dev shell: NO RL_CONFIG_MODE (a declared experiment)

RL_PED_BAR=0   RL_V0SURF_REFIT=1 python3 $RL_REPO/session_2026-07-18/legf6/scripts/refit_v0surf.py --verify
               RL_V0SURF_REFIT=1 python3 $RL_REPO/session_2026-07-18/legf6/scripts/refit_v0surf.py --verify   # shipped 0.5
RL_PED_BAR=2.0 RL_V0SURF_REFIT=1 python3 $RL_REPO/session_2026-07-18/legf6/scripts/refit_v0surf.py --verify
```

| `RL_PED_BAR` | shipped config signature | fitted-surface md5 | surfaces frozen | vs committed pin |
|---|---|---|---|---|
| `0` (kill-switch) | `3e8e50de5103` | `9713ec6c83270ab916bb4a5e3ded6cb3` | 2 | **REPRODUCES** |
| **`0.5` (SHIPPED)** | `3e8e50de5103` | `9713ec6c83270ab916bb4a5e3ded6cb3` | 2 | **REPRODUCES** |
| `2.0` (4× shipped) | `3e8e50de5103` | `9713ec6c83270ab916bb4a5e3ded6cb3` | 2 | **REPRODUCES** |

Both `--verify` legs of the directive are satisfied by this one table:

1. **The fit class is re-verified on this box against the CURRENT pickle first.** The `9713ec6c` the refit
   computes here IS the committed stage-3 pin, so the fit lane still reproduces on this instance. Had it
   diverged, that would have been the halt-worthy finding and no refit would have been credited.
2. **The dial cannot move the surface**, even at four times the shipped magnitude and even with the fit
   FORCED. Signature identical, all three fitted surfaces byte-identical.

The second row also has a second reading worth stating plainly: `9713ec6c` was fitted at stage 3 by an
engine that did not contain this change at all, and a stage-4 engine with the change fits the same bytes.
That is the cleanest possible statement that the change is not in the fit path.

## (c) Consequences, carried through

* `RL_PED_BAR` is **NOT** added to `_V0SURF_GATES`. Adding it would be actively wrong: the gate set is the
  set of keys that CAN move the surface, and putting a key in it that cannot would make a harmless dial
  change look like a surface-moving one and force a spurious refit at every future flip.
* `data/expected_boot.json` `v0surf` stays `9713ec6c83270ab916bb4a5e3ded6cb3`. `data/v0surf.pkl` is
  untouched (0 bytes changed).
* The stage-4 gated board build loaded the frozen surface normally — `v0surf_frozen=True`, signature
  `3e8e50de5103`, zero fits at build — as the `import`-time assert at the bottom of `_merged_recover.py`
  requires.
* `RL_PED_BAR` **IS** added to `data/model_config.json` `vars`, because it is a **valued owner dial**
  (like `RL_YCRED_W`, `RL_V7_FORM_W`, `RL_RUC_YRH`), not a declared kill-switch. That moves
  `config_sha256` `cef06fd6…` → `0b5d2703…` and the `expected_boot.json` `config` pin with it, in this
  same commit, exactly as the manifest's own instruction requires. Those two are a DIFFERENT pin surface
  from `_V0SURF_GATES` and must not be confused: the manifest hash governs *which configuration shipped*;
  `_V0SURF_GATES` governs *which configuration can invalidate the frozen fit*.
