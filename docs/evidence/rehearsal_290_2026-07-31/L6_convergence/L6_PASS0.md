# L6 PASS 0 under R-H — both gates PASS · **G-Y0 13.919% → 8.084%** · handing back before the curve install

**#290, 2026-07-31.** Every figure names its substrate. Nothing outside the lane's recorded bytes was installed; no gate moved; the EXECUTION word remains withheld.

## R-H.1 — THE PRE-LOOP GATES, BOTH PASS

| gate | measured | verdict |
|---|---|---|
| **(a) compute-path assert** | the pre-L4 rebuild reproduced board **`92e397bd`** byte-exact (139s) | **PASS** — this box still matches the host that produced the record's figures |
| **(b) double-fit byte-compare** | two fresh processes from an identical reset state → **`fb9efdec`** twice (72s, 74s) | **PASS** — the refit lane is viable here |

**The lane is viable, so R-H proceeds.** Had (b) mismatched, this filing would be a HALT.

## R-H.2 — PASS 0's SURFACE, COMMITTED BEFORE THE ENGINE LOADED IT

`pass0_surface/v0surf.pkl` + `IDENTITY.json`, committed at `3971298` **before** any board build read it:

```
md5   fb9efdec4d669d389fe3beef2bca3092    blob 331889aedb9e    49,758 bytes
keys  0589a2620e24 · 96d671c952c8         prior surface 84fb0cde
substrate: curve e69a3f38 · store 81d24704 · gamma 1.0
```

`data/v0surf.pkl`'s load-or-HALT is untouched; the dict gained no unrecorded key.

## THE FINDING OF THIS PASS — the signature does not cover the fitted stack

**Pass 0 is a surface CATCH-UP, not a curve move.** The curve is unchanged at `e69a3f38`, and the **signature keys are identical** (`0589a262`, `96d671c9`) — yet the surface **bytes moved**, `84fb0cde` → `fb9efdec`.

So **two different surfaces can share a signature key.** L4's retrained peak model and snapshot changed the fitted surface's *content* while leaving its *signature* untouched, because `_v0surf_sig` hashes the curve, the roster and the gates — not the fitted stack.

**This is not a hole**, and it should not be reported as one: Guard 5 pins the artifact by **full md5** (`expected_boot.v0surf`), and that pin caught exactly this during my own harness slip below. The two layers do different jobs — the **signature selects** a surface within the dict; the **md5 pin governs** the artifact's identity. They should not be conflated, and the L6 halt filing's reasoning (a *moved curve* changes the signature and forces a re-bake) stands unaffected.

## THE MEASUREMENT — G-Y0 fell by 5.8 points on the surface catch-up alone

| | |
|---|---|
| G-Y0 on `84fb0cde` (the L3–L5 record substrate) | **13.919%** |
| **G-Y0 on `fb9efdec` (pass 0)** | **8.084%** |
| board | `92e397bd` → `944abbd3` (L4) → **`978c0eb3`** (pass 0) |
| chain | bootstrap 0 · board 0 (118s) · book 0 (178s) · selftest 98s |

**Read carefully: this is not the converged number, and it is not a verdict against the 2.000% bar.** It is the year-zero residual measured on a surface that has caught up to the L4 stack, at the *unchanged* curve. The bar judges the converged fixed point (Acceptance 1), and the fixed point has not been reached.

## THE MATRIX RE-EMIT — routed as ruled

```
PRE  2f8b4bd4  ->  emit (183s)  ->  CAPTURED 9c4bca53  ->  RESTORED 2f8b4bd4    RESTORE PROVEN
```

backup → emit → capture → restore, restore proven by md5, `git` clean. The pass-0 matrix carries `store 81d24704 · v0surf_sig 96d671c952c8 · frozen True · 2,646 recs`. **Its signature is unchanged**, which is why the re-pinned harness still loads it without any pin being touched.

## THE TRAJECTORY — the loop is converging

| state | payload | ladder | `s` | pooled head | G-Y0 |
|---|---|---|---|---|---|
| installed (L3–L5 record) | `e69a3f38` | 54,722 | 0.977688 | 3068.4647 | **13.919%** on `84fb0cde` |
| derived on the `84fb0cde` matrix | `6dedc611` | 54,532 | 0.996218 | 3011.3898 | not measured — no ruled substrate existed for it |
| **PASS 0** — surface `fb9efdec`, curve unchanged | `e69a3f38` | 54,722 | 0.977688 | 3068.4647 | **8.084%** on `fb9efdec` |
| **derived on the `fb9efdec` matrix → curve 1** | **`1a8db02b`** | **54,350** | **0.998224** | **3005.3384** | pass 1 would measure |

**`s` → 1.0 and the pooled head → 3000** across the sequence (0.9777 → 0.9962 → 0.9982; 3068.46 → 3011.39 → 3005.34). That is what convergence looks like from the outside, and it is consistent with step 4's own history (`s` 0.975872 → 0.999968 in two iterations). **It is not yet a fixed point:** curve 1 `1a8db02b` ≠ installed `e69a3f38`.

**POOL is stable across every pass measured — 233.0, then 233.4, n=1,005 both times.** N5's 233 does not move under the surface catch-up, which strengthens the completed N5 condition rather than re-opening it. MSD 293.9 [84.9, 502.8] n=44 and SSP 322.1 [72.3, 571.8] n=31 — **intervals and denominators, no point estimates**, per the binding posture.

## WHERE I STOP, AND WHY

**Pass 1 requires INSTALLING curve `1a8db02b`** — and a curve install is not a file copy. It is **L1(b)'s enumerated same-commit set** (Addendum C.3): the curve artifact with its numeraire block, `pool_value`, `stamp.statistic`, `stamp.store_md5`, `stamp.per_entrant_md5`, the six FROZEN-RULER pins across `one_source_selftest.py` / `ui/release_pick_curve.json` / `release_contract.pvc_provenance` + `contract_sha256`, then the refit, then the re-pin of `expected_boot.v0surf` inside C.1.

That is a structural act with an enumerated identity set, and this seat has now been running a long session. **The record's own calibration is that a third slip at the tail of a long session is how one reaches a commit** — and my two slips this session (the harness cwd at L4, the incomplete reset below) were both at boundaries like this one.

So I am doing what my predecessor did at the T1 boundary, for the same reason: **scoping it precisely and handing it back rather than rushing it.** The gates are passed, the lane is proven viable, the surface and matrix are committed, and the next act is fully specified.

**Convergence bound and fixed-point definition — stated, since C.4 sets no number.** I take the fixed point to be *the derived payload equals the installed payload*, and the bound to be **4 passes**, from the record's own evidence (step 4 converged in 2; the runbook prices ~3). **Bound exhausted without a fixed point → HALT and report, never declare.** If the seam intends a different bound, it should be named before pass 1 rather than after.

## MY HARNESS SLIP, RECORDED

The first double-fit attempt reset only `data/v0surf.pkl` between runs; run B halted at bootstrap. **The lane re-pins `expected_boot.v0surf` itself** (Addendum E.1 records this), so resetting the surface without its pin leaves the two out of sync. **Guard 5 was right and my reset was incomplete** — the same shape as my L4 cwd slip: the engine was correct, my harness was not. Fixed to reset both; the re-run gave the identical-bytes result that passed gate (b).

## COSTS

compute-path assert **139s** · double-fit **72s + 74s** · pass-0 chain **394s** (board 118 · book 178 · selftest 98) · matrix re-emit **183s** · derivation **1s**. **Total ~14 min of engine compute, all serial, preboot assert PASS before each act.**
