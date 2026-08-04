# L6 — **THE R-I BOUND IS EXHAUSTED WITHOUT A FIXED POINT.** HALT AND REPORT.

**#290, 2026-08-04, the fresh execution seat.** Four install passes run under R-H to the R-I bound of
four. **Payload equality was never reached, and the measurements show why it cannot be reached by
iterating this map further.** Reported, not declared — R-I's own words.

---

## THE PER-PASS RECORD — payload md5 · `s` · head · G-Y0 on the named surface

| pass | installed payload | surface md5 (fitted at that curve) | ladder | `s` | pooled head | board md5 | **G-Y0** | derived next |
|---|---|---|---|---|---|---|---|---|
| **0** | `e69a3f38` | `fb9efdec` | 54,722 | 0.977688 | 3068.4647 | `978c0eb3` | **8.084%** | `1a8db02b` |
| **1** | `1a8db02b` | `aaf45964` | 54,350 | 0.998224 | 3005.3384 | `f69f0c27` | **11.030%** | `ca662051` |
| **2** | `ca662051` | `864c11b9` | 54,336 | 0.977686 | 3068.47 | `c54ec1ba` | **8.842%** | `b0bda532` |
| **3** | `b0bda532` | `2d7dab64` | 54,351 | 0.998226 | 3005.332 | `7a29dadd` | **11.028%** | `ca662051` |
| **4** | `ca662051` | `31e7f00b` | 54,336 | 0.977684 | 3068.4766 | `1a2aacea` | **8.842%** | `b0bda532` |

Every pass: selftest **96 PASS / 1 FAIL**, the single FAIL being the G-Y0 ceiling. All six
FROZEN-RULER checks green at every pass on the freshly moved pins. F1 and F2 parity green,
**mismatches = 0**, every pass. Sealed history **4 | 6** at every step. Guard 5 green at every boot.

## THE FINDING — an EXACT PERIOD-2 CYCLE in the published payload

**Curve 4 is curve 2, and curve 5 is curve 3 — byte-identical ladders, not "close".**

```
curve 4 vs curve 2 : 64/64 identical, max abs difference 0, payload ca662051, ladder 54,336
curve 5 vs curve 3 : 64/64 identical, max abs difference 0, payload b0bda532, ladder 54,351
```

So the published sequence is

```
… -> ca662051 -> b0bda532 -> ca662051 -> b0bda532 -> …
```

and **R-I's fixed point — derived payload md5 EQUALS installed payload md5 — is unreachable by
further iteration**, because the map returns each installed payload to the other one. This is not an
inference from a trend: the cycle was measured, then re-measured one full period later, and the
ladders repeated **exactly** both times.

**G-Y0 alternates with the payload** and does not descend:

```
8.084%  ->  11.030%  ->  8.842%  ->  11.028%  ->  8.842%
```

Pass 4's 8.842% equals pass 2's to the printed precision; pass 3's 11.028% equals pass 1's 11.030%
to within 0.002 points. **The lowest number anywhere in the loop is pass 0's 8.084%, and pass 0
installed no curve at all.** Against the **2.000% hard bar** the whole cycle is roughly four to five
times over.

## THE SECOND FINDING — the refit carries PATH MEMORY, and it is why the cycle is exact in integers but not in reals

Pass 2 and pass 4 installed a **byte-identical curve** onto a **byte-identical frozen fitted stack**
(peak `f305fe53` · pvc_snapshot `ade79790` · cm_400 `34faa865` · q97m `cfdc7321`, all unmoved
throughout). The refit returned the **same shipped signature key** — `8291668eff41`, as it must,
since `_v0surf_sig` hashes the curve — but **not the same surface**:

```
pass 2 surface  864c11b9      pass 4 surface  31e7f00b       same key set, same curve, different bytes
pass 2 board    c54ec1ba      pass 4 board    1a2aacea
pass 2 matrix   43169abb      pass 4 matrix   85d2a04b
```

**The fitted surface is therefore not a function of the installed curve alone** — the refit inherits
state from the surface it replaces. This is **N22's layering fact meeting the loop**: the signature
*selects*, the full md5 *governs*, and across passes the two disagree. It also explains the precise
shape of what was measured — the underlying real-valued state is **not** periodic, it drifts:

```
ODD  state heads (curves 1, 3, 5): 3005.3384  ->  3005.332   ->  3005.3241     drifting DOWN
EVEN state heads (curves 2, 4)   : 3068.47    ->  3068.4766                    drifting UP
```

The drift per cycle is ~0.007–0.008 units on a ~3,000-unit head — far below the integer rounding
granularity of the published ladder, which is why the **integer** curve locks into an exact 2-cycle
while the **real** state underneath it does not settle. **The two limbs are moving apart, not
together.** Nothing here supports a claim that more passes would converge; the measured direction is
the opposite one.

## WHAT THIS DOES AND DOES NOT SAY

**It does NOT say the substrate re-derivation failed.** L1–L5 did what they were for, and the surface
catch-up at pass 0 moved G-Y0 13.919% → 8.084%, the largest single improvement in the record.

**It does NOT say the 2.000% bar is unreachable.** It says the bar cannot be *judged*, because
Acceptance 1 defines PASS at "the converged fixed point" and **this loop has no fixed point to
converge to**. Acceptance 1's own second branch applies: **anything else = HOLD**, and a HOLD BLOCKS
landing and adoption until the owner rules.

**N16's trigger is NOT evaluable, and there is no converged surface md5 to name.** The L6 hand-back
was to state the converged G-Y0 against N16's trigger naming the converged surface md5. There is no
converged G-Y0 and no converged surface. Declining to name one is the whole point of R-I's
*"never declare"*, and it is what this filing does.

## WHAT I DID NOT DO, and why each is the seam's call and not mine

1. **I did not run a fifth pass.** R-I's bound is four and the cycle is proven; a fifth would return
   `b0bda532` and cost 11 minutes to re-confirm what two full periods already show.
2. **I did not break the cycle by picking a limb.** Installing either `ca662051` (G-Y0 8.842%) or
   `b0bda532` (G-Y0 11.028%) and freezing there would be *choosing* a substrate the loop rejects, and
   R-H's exit clause is written for a **converged** surface. Choosing a limb is a ruling.
3. **I did not touch the fixed-point definition.** Redefining convergence as "payload equality within
   a 2-cycle" or "ladder within N units" would be re-speccing a gate to make it pass — the exact
   failure H.3 records this job talking itself out of once already.
4. **I did not re-open the numeraire, the fitter or the pin policy.** They are ruled (#279), and a
   cycle in the *composed* map is not evidence against any single ruled component.

## WHAT THE MEASUREMENTS SUGGEST IS WORTH THE SEAM'S ATTENTION

Stated as candidates for a ruling, not as recommendations dressed up as findings:

- **The path memory in the refit is the mechanism to look at first.** If the surface were a pure
  function of the curve, the map would be a genuine one-variable iteration and the 2-cycle would be a
  property of the fit itself. Because it is not, the loop is a **two-variable** map whose second
  variable never resets — and that is a property of the *harness*, not of the ruled design.
- **The oscillation's amplitude is stable, not shrinking**, over two full periods. Damping would have
  shown by now.
- **POOL is stable across the entire loop** — 233.4 / 233.3 / 233.4 / 233.3, n = 1,005 every time,
  relative SE 6.1%. Five measurements now. **N5 is strengthened by the whole exercise**, whatever is
  ruled about convergence. MSD 293.8–293.9 (n=44) · SSP 321.7–322.0 (n=31), intervals and
  denominators, no point-estimate law lines.

## COSTS

| act | measured |
|---|---|
| compute-path assert (pre-L4 control rebuild) | **116s** |
| double-fit byte-compare (R-H clause 1b, this box) | **62s + 68s** |
| per pass: refit · board · book · selftest | 62–72s · 113–128s · 172–181s · 89–99s |
| per pass: matrix re-emit · derivation | 167–204s · **1s** |
| **four install passes, end to end** | **≈ 51 minutes of engine compute**, all strictly serial, preboot assert PASS before every act |

## POSTURE

Rehearsal throughout. R-C held: **nothing landed**, no gate moved, no pin outside the lane's recorded
bytes, the record carrier `claude/exec-seat-290-handoff-j0kwl0` untouched at `8e8c15b`, the three HOLD
branches untouched, main untouched. **The EXECUTION word remains WITHHELD.**

**HALTING. The loop is the seam's to rule on.**
