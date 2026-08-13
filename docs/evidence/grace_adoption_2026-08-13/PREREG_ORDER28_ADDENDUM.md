# PRE-REGISTRATION ADDENDUM — ORDER 28, THE MONOTONE RULING

**Filed 2026-08-13, committed and pushed BEFORE `o28_derive.py` existed and before any curve number
on the grace-A basis had been computed on this branch.** Amends `PREREG_ORDER28.md` §2 and §4.

Ordered by the owner at
[#334 comment 5276216984](https://github.com/lukemcalister10/afl-rl-engine/issues/334#issuecomment-5276216984),
as amended by the coordinator's addendum-2 correction (same day).

---

## 1. THE RULING

> *"I'm reviewing the v0 sheet and it seems like it's non-monotonous? Pick 8 worth more than pick 6.
> And by position too. I know we went for loclin - but I thought that was just at the top and there'd
> be a smoother to create a curve. It doesn't make sense that a lower pick would be worth more than a
> higher pick?"*

The deciding argument, on the record: **pick N strictly dominates pick N+1** — it can select whoever
pick N+1 would have — so a priced ascent is an arbitrage in pick-trading terms. **The data may be
non-monotone; the priced object must not be.**

**RULED:** the shipped PAVA step (isotonic non-increasing projection) applies **AFTER** loclin and the
hybrid south boundary, re-anchored pick 1 = 3000, with **every removed ascent disclosed** beside the
final curve.

## 2. WHAT THE ADDENDUM-2 CORRECTION RETRACTED, AND WHAT REPLACES IT

The first addendum ordered the positional relativities rebuilt as continuous curves, on a reading that
they were flat per-band steps. **That reading was withdrawn**: the implementation is already
**continuous per pick** — `posv[g][p] = allin[p] · rawpos_g(p) / Σ_h share_h(p)·rawpos_h(p)`, where
`rawpos_g` is a per-position loclin fit over log(pick). The five-band table in the 26B packet was a
**summary of band means**, not the wiring. Consequently:

* **NO relativity machinery is rebuilt.**
* The packet **publishes the per-pick relativity curves for all six positions, picks 1–64**, so a band
  summary can never again be mistaken for the implementation. The band table stays, **relabelled
  "summary means of the continuous per-pick curves"**.
* **PER-POSITION MONOTONICITY IS NOT ENFORCED.** Owner lean, on the record: *"it's quite reasonable
  for a position to be 'better than all-in' at some parts of the draft and worse than others."* The
  domination argument binds the **all-in** curve (pick N can select whoever pick N+1 would); a
  positional v0 is a price **conditional on the position actually taken**, where selection effects
  legitimately produce non-monotone shapes. **Per-position ascents are DISCLOSED as data and
  monotonized NOWHERE.**

## 3. THE MONOTONE STEP, FIXED BEFORE MEASUREMENT

**Estimator:** `engine/forward_valuation/par_build.py::_pava(y, w, increasing=False)` — the **shipped**
weighted pool-adjacent-violators routine, reused and cited, not reimplemented. It is the same callable
the engine already uses for its non-increasing-in-pick monotonicity prior (`par_build.py:561`).

**Weights:** `w_p` = the **per-pick cohort n** (the number of careers attributed to pick `p` after the
26B-C1 slide: 18 for picks 1–60, tapering to 14 at pick 64). Weighted PAVA replaces each violating
block by its **weighted mean**, so **`Σ_p w_p · value_p` is conserved exactly**, block by block and
over the whole curve. That is the owner's conservation requirement satisfied by construction rather
than by adjustment.

**Order of operations** (fixed here):

```
raw cohort values ──► LOCLIN (26B-C2)  ──► HYBRID south boundary (PREREG §2)
                  ──► weighted PAVA, non-increasing, weights = per-pick n
                  ──► anchor:  × 3000 / value(pick 1)
```

PAVA is a monotone projection and anchoring is a positive scalar, so the two commute; PAVA is applied
**pre-anchor** and the anchor read afterwards.

**ASSERTS, each able to fail:**

| assert | statement | on breach |
|---|---|---|
| **A1 — PAVA does not touch pick 1** | the pick-1 block emerging from PAVA has size 1, i.e. pick 1 is not pooled with pick 2 | **HALT and report.** Never silently rescale the anchor. |
| **A2 — weighted-sum conservation** | `\|Σ w·post / Σ w·pre − 1\| < 1e-12` | HALT |
| **A3 — monotone out** | `post[p] ≥ post[p+1]` for every p | HALT |
| **A4 — reconciliation (Ruling 13)** | `max_p \|Σ_g share_g(p)·posv_g(p)/allin(p) − 1\| < 1e-12` **after** the monotone all-in is substituted | HALT |
| **A5 — anchor invariance vs 26B-V** | head, anchor factor and premium reported against 26B-V grace-A with the delta printed; a move must be explained by PAVA at pick 1 (which A1 forbids) or by nothing | report |

**THE CONSERVATION LEDGER** (printed in the packet, per the owner's *"in enforcing the curve, total
values all in or by position drop or rise a lot, that is not ideal"*):

1. `Σ w·value` pre- and post-PAVA — **exact to floating point** by construction (A2);
2. the plain (unweighted) `Σ value` pre/post, with the drift printed — *not* conserved when the
   per-pick n differs, and the difference is confined to picks 61–64 where n tapers;
3. the anchor factor pre/post — **must not move** (A1);
4. `Σ_p posv_g(p)` per position, pre/post the per-pick renormalisation onto the monotone all-in, with
   the drift printed for all six positions.

**DISCLOSURE OF REMOVED ASCENTS:** every pick at which the pre-PAVA curve ascends is listed with
(a) the pick pair, (b) the ascent size in pre-anchor and anchored points, (c) the **raw cohort means**
behind it, and (d) the pooled value PAVA assigned. The full pre-PAVA and post-PAVA curves both appear
in the curve table, so nothing is replaced silently.

## 4. ADDITIONAL PREDICTIONS (bands, before the numbers exist)

**P12 — 6 to 12 ascents are removed, all in the interior, none at pick 1.**
26B measured **8 genuine cohort ascents at n=18** on the flat-14 loclin curve, deliberately left
visible pending this ruling. Grace-A is close to a scalar on the ND arm (26B-V PV3/PV6), so the ascent
*locations* should be nearly unchanged; the hybrid south boundary may add or remove one at the seam.
**Predicted: 6–12 ascending adjacent pairs; A1 holds; the owner's named case (pick 8 > pick 6) is
among them.**

**P13 — the anchor does not move.** head `3191.2`, factor `0.9401`, premium `−6.0%` — unchanged from
26B-V grace-A and from the pre-PAVA hybrid, because PAVA cannot reach pick 1 (A1).

**P14 — the weighted total is conserved to floating point; the plain total drifts by < 0.5%.**

**P15 — the positional totals move by less than 2% each** under the per-pick renormalisation onto the
monotone all-in, since PAVA redistributes within blocks rather than rescaling.

**P16 — the per-pick positional curves are non-monotone for at least two positions**, and that is
reported as data, not corrected. KPD is predicted to be one of them (its relativity rises into the
late draft: 0.847@42 → 1.053@45 → 1.145@46 → 1.519@50 on the 26B basis).
