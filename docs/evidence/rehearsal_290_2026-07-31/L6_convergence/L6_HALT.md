# L6 — **HALT AT PASS 2.** Convergence cannot run on the frozen surface. Levels re-measured; N5's 233 confirmed.

**#290, 2026-07-31.** Substrate for every figure: **store `81d24704` · v0surf `84fb0cde` · γ 1.0.** Nothing installed, no pin re-stamped, no gate moved, no bake. Every act behind `tools/preboot_assert.sh`.

## THE HALT — measured on L6's first act, before anything was installed

**L6's convergence iterates the curve against the surface. The frozen surface cannot serve a moved curve, so pass 2 cannot start.**

Measured, not reasoned:

| | |
|---|---|
| `data/v0surf.pkl` is a **dict keyed by signature**, holding | **2** surfaces: `96d671c952c8` (the live curve's) and `0589a2620e24` |
| `_v0surf_sig` (`_merged_recover.py:1299`) hashes | `{'pvc': the curve, 'roster': …, 'gates': …}` — **the curve is an input to the hash** |
| pass-1 candidate curve vs the installed `e69a3f38` | **differs at 61 of 64 picks** |
| its curve-component hash | `a9b89d7c…` vs the installed `dd790e77…` — **differs** |

So the pass-2 curve's signature is **not** one of the two frozen keys, and `data/v0surf.pkl` is **load-or-HALT**. The engine would refuse to boot. **A convergence pass that moves the curve forces a v0surf re-bake — and the re-bake is, in N16's own words, "the chain's only machine-sensitive act."**

## THE CONFLICT THIS EXPOSES — a ruling-level question, presented and not resolved

**N16** names the frozen bytes as the ruled substrate for *"L3–L8, **L6's convergence** and the landing."*
**Addendum C.4** keeps at L6 *"the curve↔surface convergence iteration"*, adding that if a pass moves the curve *"the refit is re-run as part of that pass."*

**Both cannot hold.** Convergence moves the curve; a moved curve invalidates the frozen surface; re-baking re-introduces exactly the machine-sensitivity the freeze removed — the sensitivity that produced the 19.869% vs 13.919% episode on one artifact's bytes.

This is not a defect in either ruling. It is the point where they meet, and it was not visible until the mechanism was measured. **I have not chosen between them**, and I have not:

- installed the pass-1 candidate curve,
- re-baked the surface,
- or produced a G-Y0 figure on a substrate no ruling names.

Any of those would have manufactured a number whose substrate could not be cited — the precise failure N16 exists to prevent.

**The options, stated neutrally for the seam:**

1. **Convergence re-bakes per pass**, and every G-Y0 in the iteration is explicitly container-bound — the landing then ships the final surface's bytes and the earlier passes are working figures only.
2. **Convergence is held** and the ruled curve stands as the landing curve, with the fixed point declared unreached — which makes the 2.000% bar a judgement on the current curve rather than a converged one.
3. **A bounded iteration** — N passes with the re-bake accepted, the byte-determinism re-proven on one machine each pass, and the acceptance evaluated only on the final pass.

Each has a different consequence for **Acceptance 1** (`G-Y0 ≤ 2.000% at the converged fixed point`), so this is the owner's/seam's call, not mine.

## WHAT L6 *DID* COMPLETE — the levels, with denominators (D2's seam word, N5)

Re-measured through the carried derivation lane on the ruled substrate. **Pass-1 curve `6dedc611`** — a waypoint, *not* a converged fixed point:

| | LEVEL (×s) | ci95 | **n** | provenance (concluded / completed / fallback) | fallback |
|---|---|---|---|---|---|
| **POOL** | **233.0** | [205.2, 260.8] | **1,005** | 888 / 56 / 61 | 6.07% |
| **MSD** | **293.3** | [84.8, 501.8] | **44** | 30 / 13 / 1 | 2.27% |
| **SSP** | **321.5** | [72.2, 570.8] | **31** | 20 / 9 / 2 | 6.45% |

Stop-point comparison: POOL 234.3 [206.4, 262.3] · MSD 296.4 · SSP 333.4.

### N5's 233 — RE-MEASURED, and it holds

N5 records: *"Pool ≈ tail equivalence; the register-carried **233** has no committed artifact — re-measure with denominator before the law line lands."*

**Measured: POOL = 233.0, n = 1,005, ci95 [205.2, 260.8], provenance 888 concluded / 56 completed / 61 fallback (6.07%).** The register's 233 is confirmed to the integer, and it now has both a committed artifact (`pass1_ruled_substrate.json`) and its denominator. **The law line can cite a measurement rather than a carried number.**

**Carried honestly — the lane's own denominator warning**, which I am repeating rather than burying: *MSD and SSP rest on far fewer rows than the store-level stream counts of 106 and 52 (those are all-2,651-row counts). Under the ruled class cut they are much smaller and the intervals are correspondingly wide.* **Read the interval, not the mean** — MSD's ci95 spans 84.8–501.8 on n=44, and SSP's 72.2–570.8 on n=31. Neither should be worded into a law line as a point estimate. POOL, at n=1,005 and a 6.1% relative standard error, is the only one of the three that carries a usable interval.

**The MSD/SSP ordering inverts versus the schedule live in `ui/app/config.js:54`** — carried forward from the runbook, and still true at these values (MSD 293.3 < SSP 321.5). Nothing is worded off the old schedule.

## G-Y0 AGAINST N16's TRIGGER — stated as the seam requires, and honestly

| | |
|---|---|
| G-Y0, current | **13.919%** |
| measured on surface md5 | **`84fb0cde29f36c1a91d440e63b753c3c`** |
| the bar | **2.000%** at the converged fixed point |
| converged? | **NO — the fixed point was not reached.** L6 halted at pass 2. |

**So N16's trigger is NOT evaluable yet, and I am not going to imply otherwise.** N16 fires the year-zero redesign on *"L6's converged G-Y0"*; there is no converged G-Y0. The 13.919% is the L3/L4 waypoint on the named surface, and the gap to 2.000% is large — but a waypoint is not a verdict, and reporting it as one would be exactly the misreading the T1 hand-back warned against when it insisted a green gate is not progress toward the bar.

## COSTS

Lane re-derivation **1s** · signature/frozen-surface probes **~3s** · **no engine act, no bake, no board build this leg.** The halt was reached before any expensive act — which is the whole value of measuring the mechanism first.
