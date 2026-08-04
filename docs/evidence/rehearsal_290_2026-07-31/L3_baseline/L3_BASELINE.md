# L3 BASELINE — measured before any change. Window word **A** received.

**#290, L3, 2026-07-31.** Every count names its denominator. Nothing changed yet; this is the
before-picture L3 is measured against.

Substrate: the reconstructed L1-exit tree on the **frozen ruled surface `84fb0cde`**, E3 applied,
`DRAFT_LO=2003` (window A). Strictly serial behind `tools/preboot_assert.sh`.

## 1 · THE TRAINING POPULATION (`build_cond_prior`, debut ≤ 2021, pick or `_ft`)

| | |
|---|---|
| store rows | 2,651 |
| GRP-mapped pool | 2,651 |
| **training players** | **1,930** |
| **training (player, year) rows** | **13,221** |

## 2 · CONCLUDED / ACTIVE SPLIT — the S-1 gap, with counts

| | count | share of 1,930 |
|---|---|---|
| **CONCLUDED** (`_retired` / `_last_listed`) | **1,572** | **81.45%** |
| **ACTIVE** | **358** | 18.55% |

Store markers re-measured: `_retired` **1,847** rows, `_last_listed` **13** — and **the 13 are a
strict subset of the 1,847**, so the concluded set is 1,847 store-wide, not 1,860. The runbook's
figures are confirmed; the nesting is recorded because a naive union would over-count by 13.

**The gap, stated plainly:** `build_cond_prior` trains on **all 1,930** resolved careers, concluded
and active alike. **S-1 retires the prior from concluded careers entirely** — so **1,572 careers
(81.45%)** currently teach a prior that S-1 says must not apply to them.

**S-1/S-2 are already implemented — in the step-4 harness, not in the live path.**
`harness_pvc_REPINNED.py:110-152` does exactly what S-1/S-2 require: `concluded(r)` →
`realised_full(r)` at full weight with the prior retired; not-concluded → actuarial completion from
the concluded (pos, tenure) stratum; the prior surviving only as a **counted** fallback
(`prior_fallback_no_written` + `prior_fallback_thin`) over `len(ND)`, with an assert that the three
provenance classes **sum to the population**. `concluded()` reads `retired_now`, which the emitter
synthesises from the **real store markers** per #279 C1. So L3's work is to carry this into the live
`conditional_prior` path, not to invent it.

**The WATCHED NUMBER's home** is that loader's `fallback_share_pct` over `EXPECT_N = 1197` ND
teaching rows — baseline **5.931% = 71/1,197**. L3 re-measures it there, with its denominator; a bare
percentage is a HALT.

## 3 · BIAS-1, SCOPED BY MEASUREMENT — and it is much smaller than it looks

Window A keeps the 2003 class, so this fix is **live** (under window B it would have been moot).

The store's scoring begins in **2005** — there are no 2003 or 2004 scoring rows at all. So every
training row emitted at `Y < 2005` carries `games=0, exposure=0, level=0`. A naive count says **278**
such rows. **That count is wrong to act on**, and the decomposition matters:

| pre-2005 training rows | count | what it is |
|---|---|---|
| `Y == d0` — the **draft-year** row | **214** | **zero games BY DESIGN.** `build_cond_prior`'s own docstring: *"one row per (player, as-of-year Y) from draft year (games 0)"*. Not a bias. |
| `Y > d0` — a **real season the store cannot see** | **64** | **the genuine phantom. This is bias-1.** |
| total | 278 | |

**Bias-1's true population is 64 training rows of 13,221 = 0.484%**, one per player, all of them the
2003 class's tenure-1 (2004) season. By year: 106 rows at Y=2003 (all draft-year) and 172 at Y=2004
(= 64 phantom + 108 draft-2004 draft-year rows).

**The second limb of bias-1 — the tenure offset — is not counted above and is the larger effect.**
`_feat` uses `ten = Y - (debutyr-1)`. A 2003 draftee at Y=2005 reads **tenure 2** carrying one season
of games; a 2004 draftee at Y=2005 reads **tenure 1** carrying one season. Same evidence, one tenure
year older — so the class systematically presents as slower developers, and this touches **every**
2003-class row (641 rows over 106 players), not just the 64.

## 4 · WHAT L3 OWES FROM HERE

1. Carry S-1/S-2 from the step-4 harness into the live `conditional_prior` path (the 1,572/358 split).
2. Land bias-1: the 64 phantom rows **and** the tenure-offset limb.
3. Busts' zero-remainders at full weight (THE BUST RULING) — the existing teach-as-zero is ruled
   behaviour, so this is a no-change to verify, not a change to make.
4. Re-measure the WATCHED NUMBER with its denominator; report the concluded/active split and the
   exposure-clock delta on the 2003 class.

Gates: selftest · Guard 5 · the fallback share **with** its denominator.

## 5 · A METHOD NOTE

The first attempt at §1 was run with stdlib against the raw store JSON and returned **0 training
players** — the raw rows carry `present_position` / `future_position`, and `pos` is derived by the
engine's loader. Every figure above is therefore measured **through the engine**, not through a
hand-rolled reading of the file. Recorded because it is the same shape as the predecessor's fault (a)
— reasoning from a file's appearance rather than from what the loader does — caught here by the
measurement returning an obviously impossible number.
