# PRE-STATEMENT — ORDER 26B-V, THE GRACE-YEARS VARIANTS

**Filed 2026-08-13, committed and pushed BEFORE `o26b_variants.py` existed or any variant number was
computed.** Ordered by the owner at
[#334 comment 5275831956](https://github.com/lukemcalister10/afl-rl-engine/issues/334#issuecomment-5275831956).

**MEASUREMENT ONLY. NOT RULED. NOTHING LANDS.** flat-14 on the C2 basis remains the operative
derivation; these are two labelled Layer-2 re-runs placed beside it so the owner can see what he is
choosing between.

---

## 1. THE OWNER'S DIAGNOSIS, AND WHAT IS AND IS NOT IN DISPUTE

> *"the flat-from-year-1 fade compresses the hits' peak seasons (a year-4 peak carries ~0.59 weight
> from day 0 at 14%) while busts contribute zero under any fade, so hits under-contribute to the
> curve relative to their year-4 stature."*

**The arithmetic in his diagnosis is exactly right and is already confirmed on the current basis:** a
season at `k = 4` carries `1.14⁻⁴ = 0.5921`. Nothing below disputes that. What the variants change is
*when the fade starts*, and the pre-statement's job is to say — before the numbers exist — what that
should and should not be expected to do.

## 2. THE MECHANICS, AND THE ONE PLACE THE SPEC AND THE OWNER'S WORDS CAN COME APART

The scorer's existing convention, unchanged since step 3:

```
k = season_year − entry_year          # k = 1 is a normal draftee's FIRST played season
DF(k) = disc_factor(entry_age, 0.14, k) = 1.14^k     (k ≤ 0 ⇒ 1.0, the engine's own convention)
```

So on the **current basis** a first season carries `1.14⁻¹ = 0.877` and a year-4 season `1.14⁻⁴ =
0.592` — matching the owner's own figure, which confirms the mapping.

The order's formula is `(1.14)^(−max(0, j−1−G))` with `j = 1` the first season. **Mapped onto `k`,
`j = k`,** so the formula's exponent is `max(0, k−1−G)`.

**THE CONFLATION, NAMED BEFORE IT IS MEASURED.** At `G = 0` the formula gives exponent `max(0, k−1)`,
which is **not** the current basis (`k`) — it is already one free year for *everyone*, mature-agers
included. That collides with the owner's own restriction, verbatim: *"19 in their first year. **Not
mature age players**"*. Both of his constraints cannot hold at once under the literal formula, so
this order computes **both readings** and never silently picks one:

| reading | exponent | grace-A: age ≤19 / ≥20 | grace-B: ≤19 / 20 / ≥21 | mature-ager vs today |
|---|---|---|---|---|
| **READING O — PRIMARY** (owner-words, current-basis-preserving) | `max(0, k − Gᴼ)` | **Gᴼ = 2 / 0** | **Gᴼ = 3 / 2 / 0** | **unchanged** ✔ |
| READING L — SECONDARY (the order's formula, literal) | `max(0, k − 1 − G)` | G = 1 / 0 | G = 2 / 1 / 0 | one free year ✘ |

**Reading O is primary** because it reproduces the owner's stated weights *exactly* — grace-A gives
*"years 1 and 2 … 100%, then year 3 14% less"* (`k=1,2 → 1.0`; `k=3 → 1.14⁻¹`) — **and** leaves
mature-age entrants on today's ladder, which is his other stated constraint. Reading L is computed and
reported beside it at the head/factor level so the difference is a number on the page, not a choice
made in private. A third diagnostic arm, **grace-0** (`max(0, k−1)` for everyone), isolates the
universal one-year shift the literal formula embeds.

Everything else is identical to the operative C2 basis: loclin curve, force-majeure slide, window
tiers, games weighting, K = 15, bars, positions, tails. Entry age from Layer 1 (100 % coverage).

## 3. PREDICTIONS — stated before computation, with bands

**PV1 — HEADS RISE, AND BY A PREDICTABLE FACTOR.** A grace of `Gᴼ` multiplies every season at
`k ≥ Gᴼ` by exactly `1.14^Gᴼ` and every earlier season by less, so a career whose value sits mostly
beyond year 2 scales by close to `1.14^Gᴼ`. Almost every ND entrant is 18–19, so:
- **grace-A** pick-1 head ratio in **[1.24, 1.30]**, point **1.28** (ceiling `1.14² = 1.2996`);
- **grace-B** pick-1 head ratio in **[1.40, 1.49]**, point **1.45** (ceiling `1.14³ = 1.4815`).

**PV2 — THE PREMIUM FALLS THROUGH ZERO AND GOES NEGATIVE.** The anchor factor is `3000 / head`, so it
falls by the same ratio. From C2's `×1.2180` (premium +21.8 %):
- **grace-A** anchor factor in **[0.937, 0.982]**, point **0.951** → **premium ≈ −5 %**;
- **grace-B** anchor factor in **[0.818, 0.870]**, point **0.840** → **premium ≈ −16 %**.
**I predict grace-A is roughly where the measured pick-vs-player premium vanishes**, and that this,
not the curve shape, is the variants' most consequential consequence.

**PV3 — GRACE DOES *NOT* RESTORE HITS RELATIVE TO BUSTS, AND THE OWNER SHOULD SEE THAT PLAINLY.**
This is the prediction I most want on the record before the numbers exist. A bust scores ~0 under
*every* discount ladder, so grace cannot move him; but grace is also very nearly a **uniform
multiplier on every non-zero career**, because it shifts the exponent rather than re-weighting seasons
against each other. The hits-vs-busts *ratio* is therefore largely unchanged; what rises is the whole
level, and with it the head, which then divides back out through the anchor. **Prediction: within the
pick-1 cohort, the ratio of the top career to the cohort mean moves by less than 5 % under either
variant, and every zero stays a zero.**
The one genuine differential: a one-season career gains only `×1.14` (its single season sits at
`k=1 < Gᴼ`) while a long career gains the full `×1.14^Gᴼ`. **Prediction: long careers gain 12–16
percentage points more than one-season careers under grace-A**, so the variants *do* tilt toward
longevity — just not in the hits-vs-busts direction the diagnosis names.

**PV4 — MATURE-HEAVY POOL PATHWAYS LOSE GROUND; YOUNG-HEAVY ONES HOLD.** Under Reading O a pathway's
gain tracks its entry-age mix, while the anchor factor falls by the *ND* arm's gain. So any pathway
older than the ND arm loses in anchored terms. **Predicted biggest losers: the mature-age recruiting
routes (SSP, IRE, UNR, PDA) — anchored values down 15–25 % under grace-A. Predicted least moved: RD
and ND>64** (young intakes), within ±8 %. **MSD I expect to lose**, its entrants being older than
draftees, despite it being the "young pathway" of the pool question.

**PV5 — POOLED RATIOS FALL.** Whole-pool `derived / signed anchor` from C2's **1.0056** to
**[0.82, 0.97]** under grace-A and **[0.72, 0.92]** under grace-B; `derived / printed day-0` from
**0.3906** to **[0.32, 0.38]** and **[0.28, 0.35]** respectively. **The pool's agreement with the
owner's signed anchors — the strongest result in the packet — gets WORSE under both variants**, and I
am registering that expectation now so it cannot be read as a discovery afterwards.

**PV6 — SHAPE BARELY MOVES.** Grace is close to a scalar on the ND arm, so post-anchor the curve
shape should be almost unchanged. **Max |variant/flat-14 − 1| across picks 1–64, post-anchor, under
5 % for grace-A and under 8 % for grace-B.** The reconciliation law holds at ~1e−16 in both.

**PV7 — READING L vs READING O.** Reading L multiplies Reading O by a further `×1.14` on the mature-age
rows only, so the two should differ by **1–4 %** at the head (the ND arm is almost all ≤19) but by
**10–14 %** on the mature-heavy pool pathways. **I predict the reading choice is immaterial to the
curve and material to the pool**, which is exactly why it is being reported rather than resolved.

## 4. WHAT THIS ORDER DOES NOT DO

No board is built and no engine byte moves. This is the **curve-side** measurement only. The
board-side twin — a dial-gated grace parameter inside `rl_model.py::disc_factor` — is the follow-up
act *if the owner likes what he sees*, and it is not written here.

**AT LANDING THE TWO SIDES CANNOT MOVE APART.** The identity gate ties the scorer to the engine's own
`price6`, which discounts projected seasons through the same `disc_factor`. A grace applied to the
curve side alone would break that identity: the derived v0s would be built on one ladder and the
printed prices on another, and the ruled landing assert (`printed day-0 == derived v0 × the display
numéraire`) would fail. **If a grace variant is ever ruled in, it must be ruled into `disc_factor`
itself, and both sides re-derive together.** That is a constraint on the decision, not a detail of it,
and it is stated here before any number is seen.
