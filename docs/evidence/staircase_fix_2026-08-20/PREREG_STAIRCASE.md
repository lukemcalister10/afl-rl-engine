# PREREG — THE STAIRCASE FIX (ORDER 44), BOTH BOUNDED VARIANTS

**Seat:** pricing seat, THE STAIRCASE FIX · **Date:** 2026-08-20
**Base:** `main` @ `efbe1b6` · board `68be10c79d0ee096455754e084bcf757` / total **692,296** / **804** rows
**Store** `b745002eb0a0fbb1c34fa44f1ef708d6` (R23) · **engine_head** `1867e953cf844d089ab1da68379b1742`
**balanced** `556ad70d295923455982ae33e4b8bfd3` · **contract** `cde9f70a` · **book** `9f46aba3` · runner GREEN
**Owner word, verbatim:** *"Yes, bounded fix now"*

> **THIS FILE IS COMMITTED BEFORE THE ENGINE IS TOUCHED (process law P9).** Everything below is a
> PREDICTION. Where the tree disagrees with it, THE PREREG IS CORRECTED AGAINST THE TREE and the
> error is named in the packet — never the other way round.
>
> **THIS IS A PRICING ACT (P1).** Candidates are built and measured; **nothing is adopted**. The dial
> ships **OFF**. At this seat's final commit the shipped board must still be
> `68be10c79d0ee096455754e084bcf757`, byte-exact, and that is F1.

---

## 0 · WHAT IS BEING FIXED, IN ONE LINE

`docs/evidence/trough_diagnosis_2026-08-20/WORKINGS_TROUGH.md` established, by prediction, that the
five pinned quantile forests + `q97m` read at `engine/forward_valuation/conditional_prior.py:164-167`
are **piecewise-constant and unconstrained on the level feature** (feature index 9), so a player's
band can step DOWN on a RISING level. Register v806 records the verdict: **LAW 3 (NO CLIFFS)
VIOLATION**, 44 of 86 thin-evidence rows priced higher by some LOWER round-23 score than the one they
made. This act prices **FIX 2** — monotonise at the READ site — in **two bounded variants**, each
presented **raw and conserved**.

`conditional_prior.py` is **NOT edited**. The forests are **NOT refitted**. `cm_400.pkl` (`34faa865`)
and `data/q97m.pkl` (`cfdc7321`) are read exactly as they are, so no Guard-5-pinned frozen artifact
moves and this is not a bake. That is what makes the act bounded, and it is the whole difference
between FIX 2 and FIX 1.

---

## 1 · THE DIAL — ONE DECLARED DIAL, DEFAULT OFF, KILL-SWITCH SEMANTICS

    RL_O44_LVLMONO      ORDER 44 — THE LEVEL-AXIS BAND MONOTONISER

Pattern: the D8 ceiling dial (`_merged_recover.py:1118+`, `RL_O33_TAPEROFF`) and the
`RL_CAPT`/`RL_ISOFADE`/`RL_EVW`/`RL_UNCOMP`/`RL_ONEMACH` kill-switch family.

**NOT A MANIFEST DIAL, ON PURPOSE.** It is absent from `data/model_config.json`, so
`config_manifest.enforce()` **rejects it as an unknown model override in bake/gate/canonical mode**
and no certifying build can carry it. `config_sha256` is therefore **UNMOVED** by this act and the
release-contract seal `cde9f70a` stands. The `dial_coverage` acceptance check counts undeclared
engine-read `RL_*` vars as **REPORTED, NOT GATED** (`acceptance/checks/m1a.py:200-217`), so the
undeclared count moves by exactly **+1** and no gate reds on it. **PREDICTED, to be measured.**

**The five accepted values.** Anything else **HALTS** at import (law 2 — a check that produces no
verdict has failed; a dial that silently accepts a typo as "off" is that failure in dial form):

| value | variant |
|---|---|
| unset · `0` · `off` | **OFF** — the shipped expression, byte-identical. |
| `ratchet` | **VARIANT A**, raw |
| `ratchet+conserve` | **VARIANT A**, conserved |
| `smooth` | **VARIANT B**, raw |
| `smooth+conserve` | **VARIANT B**, conserved |

One name, five states. Conservation is a *state of the same dial* rather than a second dial,
because a raw variant and its conserved sibling are two readings of ONE fix and must never be
settable into an unintended fourth combination.

---

## 2 · THE SITE, THE WINDOW, AND THE OBJECT MONOTONISED — ALL DECLARED

**Site.** `_b6_core` (`engine/rl_after/_merged_recover.py:370-372`) — the READ site, which is exactly
what LEG A already does to `iso_corr` (`_merged_recover.py:986`, *"the ratio is non-monotone even
though the numerator is"*) and what `_iso_dec` / `_fit_pick_curve` do on the pick axis. One engine
file, one hunk at the band, one hunk at the production hook, one load-time calibration block.

**Window — DECLARED.** Level grid **[40.0, 120.0] step 0.5** = 161 points. This is the FULL model
domain and it is deliberately the SAME window the diagnosis measured Fix 2's blast radius on
(`tasks/task_06_blastradius`), so the diagnosis's **mean +0.61 % / 39 rows > 5 % / 466 of 801
unmoved** are directly comparable to what this act measures. A row whose own level sits outside the
domain is clamped to the ends for the grid; **its own exact level is always an evaluation point**, so
no row is ever priced off a grid approximation of itself.

**The object.** The FULL six-leg band as `_b6_core` emits it — the five sorted quantiles AND the q97
tail leg. At each grid point the base rule is applied unchanged:
`v(g) = concat( sort([m_q(f_g) for q in Q]) , [ max(q97m(f_g), sorted[4]) ] )`.

This answers **diagnosis §8 open question 5** — *"whether the q97 tail leg should be monotonised at
all, given `_b6_core` already applies `max(q97, b[4])` — the interaction of two monotone instruments
needs one reading, not two"* — with ONE reading: the `max` is composed FIRST and the monotoniser runs
on the composed six-vector. A max of two non-decreasing functions is non-decreasing, so the two
instruments cannot fight. **Sortedness is preserved by construction:** if `b_i(g) <= b_{i+1}(g)` at
every `g`, then `max_{g'<=g} b_i <= max_{g'<=g} b_{i+1}`.

---

## 3 · THE TWO VARIANTS

### VARIANT A — THE RATCHET

    A_i(lvl) = max( v_i(lvl) , max{ v_i(g) : g in GRID, g <= lvl } )

The running maximum: the isotonic-increasing projection under the only-ever-raise reading, which is
the shape the diagnosis measured. **Non-decreasing in level by construction.**

### VARIANT B — RATCHET + SMOOTHED

The ratchet `A_i(·)` is evaluated across the whole grid; it is a non-decreasing **step** function.
Its maximal plateaus are located; each plateau's value is placed at **that plateau's midpoint**; B is
the **linear interpolation between consecutive midpoints**, evaluated at the row's own level, held
flat outside the first and last midpoint.

**Why this smoothing and not another — declared.** It introduces **NO NEW PARAMETER**. A
minimum-slope floor was considered and **REJECTED** for exactly that reason: it needs a slope
constant, and a slope constant is a fitted number this seat would be choosing. The midpoint rule and
linear interpolation are parameter-free, and the estate's standing answer to "which constant?" is
"none, if the derivation has a boundary solution" (ORDER D8's `asc == 1`).

**Two properties, both stated up front because they are the honest case against B:**

1. **B is strictly rising on `[m_first, m_last]` wherever the ratchet rises at all**, and flat only
   outside that interval. Flatness at the two ends is a boundary of any interpolation, not a defect
   this seat chose to leave in.
2. **B is NOT `>=` A pointwise.** On the left half of a plateau B sits BELOW the plateau value and on
   the right half ABOVE it. So B **redistributes within the plateau** and is predicted to **mint less
   than A**, and **some rows will move DOWN against the live board under B**. That is a real
   difference in kind, not a cosmetic on A, and it is why B is priced as its own variant.

---

## 4 · CONSERVATION (LAW 9) — THE RENORMALISATION LEG

Law 9: *re-pricing redistributes value; it does not mint or burn it*, threshold `band_scar = 200`
(RULEBOOK v3 PART 3). Against a 692,296 board that is **±0.029 %**. The diagnosis measured raw FIX 2
at **mean +0.61 %** — roughly **+4,200 SCAR**, about **21x the rail**. So a raw variant is a law-9
breach on its face and must be presented as one.

**The machinery, and it is the engine's own.** The renormalisation is ISOMORPHIC to the shipped
`_UC_C` production-side per-position conservation renorm — declared at `_merged_recover.py:892-893`,
applied at `:934-935` (`return _C*v0p+delta`), calibrated at `:5866-5878`
(`_UC_C[_g]=(_s0/_s0p)`). That is the prior lever that conserved, and **the class it conserves on is
the POSITION** (`MA.gfut(p)`) — the class law is the rail, so the renormaliser rides the same class.

    LOAD TIME, over the valuation scope ( _isreal and not delisted and not _retired ), clock pinned
    to the present exactly as the _UC_C block pins it:

        for each scoped row p:   pr_off = price6(p, band_OFF(p,2026), 2026)
                                 pr_on  = price6(p, band_VARIANT(p,2026), 2026)
        C[pos] = SUM(pr_off) / SUM(pr_on)          per future-position class

    APPLIED at the raw_ev production hook:   pr = price6(p, b6(p,Y), Y) * C[gfut(p)]

By construction each position's TOTAL production leg is unchanged. **The board total is not
identically the production total** — ORDER 31 blends production with pedigree and age credit
downstream (`_merged_recover.py:5194-5199`, `price = rho31(g)*e + o31_pi*ped + age_credit`) — so a
residual board drift is EXPECTED and will be **MEASURED and reported against the 200-SCAR rail, never
assumed to be zero.** The single-constant-per-class choice (C calibrated at Y=2026, applied at every
lens year) is the choice `_UC_C` already makes, carried, not invented.

**If the conserved builds do not land inside the rail**, the raw variants are presented WITH THEIR
MINT STATED as an OWNER RULING option — the diagnosis's §8.1 wording: *"either renormalise ... or the
owner must rule that the lift is the correction rather than an inflation"*. **The mint is never
hidden under either outcome.**

---

## 5 · PREDICTED AFFECTED-CLASS BEHAVIOUR

**The trough is removed.** Band-only sweeps under the isotonic band already measured it; this act
re-runs it through TRUE `ev()`:

| player | raw max-drop (measured, diagnosis §8) | predicted, variant A | predicted, variant B |
|---|---|---|---|
| Max Kondogiannis | 40.2 % | **~0.0 %** | **~0.0 %** |
| Josh Dolan | 27.2 % | **~0.0 %** | **~0.0 %** |
| Charlie West | 34.1 % | **~0.0 %** | **~0.0 %** |
| Will Hayes | 39.8 % | **~0.0 %** | **~0.0 %** |

Predicted across the 86 thin-evidence rows: the owner's count **44 of 86 → 0**, and the
counterfactual-depth counts (33 > 5 %, 16 > 10 %, 5 > 20 %) **all → 0** under both variants.

**Predicted board movement.** Raw A: up-only, concentrated in level 40-60 and in `g0`/`g1-4` rows,
majority of rows unmoved. Raw B: smaller net than A, **with movers in both directions**. Conserved A
and conserved B: net ~0 by construction, with the SAME rows moving relative to each other.

**A PRECISION THIS SEAT WILL NOT FAKE.** The diagnosis's `+0.61 %` is a mean over `price6` at each
row's own features — the PRODUCTION leg. The BOARD total moves by a *different* number, because
ORDER 31 weights production by `rho31(g)` against pedigree, and the diagnosis measured that
transmission explicitly (Billy Cootee's production share is 0.029, and he is immune). **So this
prereg predicts the DIRECTION and the ORDER OF MAGNITUDE of the board mint, not its value.** A
prereg that quoted a board delta to two decimals here would be a number invented to be satisfied.

---

## 6 · THE FALSIFIERS

**F1 — THE KILL-SWITCH.** With the dial OFF, a build off the EDITED tree reproduces
`68be10c79d0ee096455754e084bcf757` **BYTE-EXACT**, and the balanced sibling reproduces
`556ad70d295923455982ae33e4b8bfd3` **BYTE-EXACT**. *Fires if any byte differs.* This is also P1's
standing falsifier for the act: the shipped board must be unmoved at the final commit.

**F2 — THE TROUGH IS MEASURABLY GONE.** The diagnosis's own sweeps are re-run through TRUE `ev()`
under each variant: the four named victims plus the full 86-row class sweep, score 0→150.
*Fires if ANY named victim retains a max-drop > 1.0 % under either variant, or if the 86-row
`>5 %` count is not 0.* Additionally, the MONOTONICITY PROOF: variant A must be **non-decreasing**
in score for every named player (no negative step at any of the 76 sweep points), and variant B must
be **strictly rising** — every score step that raises the level must raise the price. *A strict-rise
failure in B's interior fires F2 for B and only for B.*

**F3 — LAW 12 (G-Y0) CLOSURE.** The pooled absolute percentage gap at the year-0 lens stays within
**2.0 %** on every candidate. *Fires above 2.0 %.* Reported per candidate with its margin (PART 3:
every gate names its measured value and margin).

**F4 — THE CLASS LAW.** The year-1 class cohort mark on the registered W2 basis (draft classes
2005-2015) stays inside the owner's floor **>= 1.03** and under the buy rail **< 1.14** on every
candidate. Live board reads **1.0672**. *Fires outside those bounds — and if it fires, the breach is
STATED with its number rather than the candidate being withdrawn.*

**F5 — DETERMINISM (carried from PREREG_D8 F3).** Each candidate builds byte-identically twice.
*Fires on any disagreement.*

---

## 7 · WHAT IS DELIVERED, AND UNDER WHOSE LAW

Per candidate: full movers list vs `68be10c7` **by name** with before/after/delta; the four victims
plus west/hayes explicitly; the W2 class number vs the law; the conservation accounting (total
before, total after, mint, renormalisation effect); the day-0 check; the **no-arb standing tables AND
the rendered page** — *the law: no-arb + rendered page ride every priced delivery*; and the
score-sweep monotonicity proof. Then the decision packet through `tools/landing/packet.py` +
`PACKET_TEMPLATE.md` **and its validator**, a `tools/claims.py` claims file, and the standing gates
green on the FINAL tree with the shipped board unmoved.

## 8 · THE RETIREMENT CLAUSE — DECLARED NOW, NOT LATER

**This fix is SCAFFOLDING.** It monotonises the OUTPUT of a surface whose defect is at the FIT. FIX 1
— `monotonic_cst` on feature 9 at `conditional_prior.py:160-161` and at `refit_q97m.py` — makes
"more demonstrated level is never worth less" true BY CONSTRUCTION, permanently, for every row, and
retires this entire dial. It is a bake-class act (it refits Guard-5-pinned frozen artifacts) and it
is **owner-scheduled for the variant-C rebake next week, post-R24**.

ORDER 44 is therefore **CLASSIFIED FOR RETIREMENT AT THAT REBAKE**, and **its removal is a rebake
MUST-MOVE PROOF**: the rebake is not complete until this dial and its code are gone from
`_merged_recover.py` and the board built without them reproduces the monotone behaviour from the
constrained forests alone. Filed here, in the prereg, so that the retirement is on the record from
the moment the scaffolding is erected (process law P11's principle applied forward).

## 9 · CONDUCT DECLARED IN ADVANCE (PART 4)

- **P9** prereg first — this file, committed before the engine edit. **P8** explicit paths on every
  commit; no `git add -A`. **P3** one writer — every build under `tools/build_lock.sh`.
  **P2** never boot on an unverified store — every build asserts the pinned boot identity.
  **P1** the board moves in this act's CANDIDATE builds only.
- **No push.** **`docs/OPEN_ITEMS_REGISTER.md` is not touched by this seat.**
- Evidence, trimmed and claims-style, to `docs/evidence/staircase_fix_2026-08-20/`.
- **No variable in this seat's own tooling carries the `RL_` prefix** (the thrice-burned rule): the
  drivers use `SFX_`. An `RL_`-prefixed tooling name is read by `config_manifest.enforce()` as an
  unknown model override and HALTS a canonical build — it has cost this estate three incidents.
- The pre-edit baseline was built FIRST and reproduced `68be10c7` byte-exact (101.3 s), so every
  downstream comparison is against a board this box can actually make.
