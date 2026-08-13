# PRE-REGISTRATION — ORDER 28, THE GRACE-A ADOPTION BUILD

**Filed 2026-08-13, committed and pushed BEFORE any engine byte moved, before `o28_*.py` existed, and
before any grace-basis curve, board or gate number on this branch was computed.**

Ordered by the owner at
[#334 comment 5276077959](https://github.com/lukemcalister10/afl-rl-engine/issues/334#issuecomment-5276077959),
resting on [comment 5275831956](https://github.com/lukemcalister10/afl-rl-engine/issues/334#issuecomment-5275831956)
and the 26B-V appendix on `build/delivered-value`.

**NOTHING LANDS.** The engine dial ships **DEFAULT OFF**. No board is re-pinned, no curve is adopted,
no identity carrier moves. The product of this order is a packet to the owner.

---

## 0. THE TWO RULINGS BEING IMPLEMENTED, RESTATED FOR CORRECTION

**RULING A — GRACE-A EVERYWHERE.** Owner verbatim:

> *"No, I think we can lock grace A in. And also apply it at board level too - so for backtesting and
> the live board, the diminishing seasons only counts from the second season (i.e. age 20 onwards).
> Same implementation as on the curve. And grace A applies for the pool, for the pathways. For
> everything."*

Seat reading: a **normal-age entrant (entry age ≤ 19)** carries **seasons 1 AND 2 at FULL weight**; the
**third season (age 21 for a 19-year-old) is the first diminished**. An entrant at **20+ gets no
grace** and is on today's ladder unchanged. The rule lives in `disc_factor` itself, so the curve, the
walk-forward and the live board speak one language — the 26B-V §6 landing constraint, honoured.

**RULING B — THE ASYMMETRIC BOUNDARY.** Owner verbatim:

> *"I also think the loclin effect on the pick 64 is too intense. So I'd be happy to not extend below
> it, and just be inconsistent and apply it north to pick 1 but not south to pick 64."*

Seat reading: the 26B-C2 local-linear estimator **holds at the north end (pick 1) and through the
interior**; the **south tail reverts toward the shipped weighted-mean reading**. The owner accepted the
methodological inconsistency explicitly. The build proposes the exact seam rule below, and it is fixed
here before any number on it exists.

**Everything already ruled stays**: the 26B-C1 force-majeure whole-draft slide and its asserts,
loclin north/interior, flat 14% base rate, the k conventions, window tiers, games weighting, K = 15,
bars, positions, tails. **V5 is OFF** and is not an arm of this order.

---

## 1. THE ENGINE CHANGE — `disc_factor` PLUMBING, PROPOSED IN FULL

### 1.1 The two k-conventions, and why one rule has two exponents

There are two discount clocks in this system and they are **not** the same clock. This is the single
place this order can go wrong silently, so it is written out.

| | **CURVE SIDE** (Layer 2 scorer) | **ENGINE / BOARD SIDE** (`disc_factor`) |
|---|---|---|
| index | `k_c = season_year − entry_year` | `k_e` = seasons ahead of the pricing year |
| first played season | `k_c = 1`, carries `1.14⁻¹` | whichever `k_e` it happens to be |
| the free step | none — everything discounts to acquisition | `k_e = 0` is **always** `1.0` (engine convention, `rl_model.py:906`) |
| discounts to | the **acquisition date** | **today** |

Because the engine's present season is free by standing convention, the same career rule needs a
**different exponent shift on each side**:

* **Curve side (already measured, unchanged by this order):** `exponent = max(0, k_c − 2)`
  → `k_c = 1, 2` free, `k_c = 3` first diminished. This is 26B-V Reading O, `G_O = 2`.
* **Engine side (this order's new code):** `exponent = max(0, k_e − r)` with
  `r = remaining_grace = max(0, G − s)`, `G = 1` iff entry age ≤ 19, `s` = seasons already
  completed before the pricing year.

**The equivalence, stated so it can be checked, season by season** (entry age ≤ 19; `s = 0` means the
pricing year IS his first season):

| his career season | s = 0 (1st-year board row) | s = 1 (2nd-year row) | s = 2 (3rd-year row) |
|---|---|---|---|
| season 1 | `k_e=0` → exp 0 **full** | past | past |
| season 2 | `k_e=1`, r=1 → exp 0 **full** | `k_e=0` → exp 0 **full** | past |
| season 3 | `k_e=2`, r=1 → exp **1** | `k_e=1`, r=0 → exp **1** | `k_e=0` → exp 0 (engine convention) |
| season 4 | exp 2 | exp 2 | exp 1 |

Seasons 1 and 2 carry full weight and season 3 is the first diminished, on every row — which is the
ruling. **`r` is non-zero only when `s = 0`**, i.e. only for a player whose current season is his
first. That is a consequence of the rule, not a design choice, and it is why the live-board effect is
narrow (§4, P1). Second-year and later rows are byte-unchanged even with the dial ON.

**DISCLOSED, NOT SMUGGLED:** the engine's "present season is free" convention means a third-year
player's *current* season is undiscounted on the board while the curve charges it `1.14⁻¹`. That
divergence is pre-existing, applies identically on flat-14, is a per-player constant scalar, and is
**not** created by grace. It is named here so it cannot be reported later as a grace defect.

### 1.2 Getting entry age to the call sites — the minimal wiring

`disc_factor(a, d, k, lens)` today receives only the **current** age `a`. Grace needs **entry age** and
**seasons since entry**. The proposal adds **one kwarg**, defaulting to the identity:

```
disc_factor(a, d, k, lens='bal', grace=0)   ->  (1+r)**max(0, k-grace)
```

`grace = 0` reproduces `(1+r)**k` exactly — bit-for-bit, not approximately — so the dial-off path is
byte-identical by construction rather than by measurement (measurement is still run, §4 P2).

Entry age is obtained from the player record with **the same arithmetic Layer 1 used**, so the two
sides select the identical population:

```
Layer 1 :  entry_age = entry_year - _by                      (o26b_layer1.py:121; fallback 18)
engine  :  entry_age = p['year'] - by(p),  by(p) = p.get('_by') or (p['year']-18)   (rl_model.py:191)
```

These agree exactly, fallback included. **The engine's `_age_at()` is NOT used for this test** — it
carries a `18 + (ref − cycle_year)` floor that would shift every off-season entrant by one year and
silently change who gets grace. That trap is recorded here.

Seasons elapsed uses the engine's own debut clock: `s = max(0, AGE_REF − debut(p))`,
`debut(p) = p['year']` for MSD else `p['year']+1` (`rl_model.py:196`). In the walk-forward, `AGE_REF`
moves back with the board, so each cohort receives its grace in its own first year — one rule, both
boards, exactly as ruled.

**The helper** (new, in `rl_model.py`, beside `age`/`debut`):

```
GRACE_G = 1                                   # grace-A: one extra free future season
RL_GRACE = os.environ.get('RL_GRACE','0')!='0'   # DIAL, DEFAULT OFF
def grace_years(p):
    if not RL_GRACE or p is None: return 0
    if (p['year'] - by(p)) > 19: return 0     # entrants at 20+ get no grace (ruled)
    return max(0, GRACE_G - max(0, AGE_REF - debut(p)))
```

**The call sites** — every site that today calls `disc_factor`, and how `grace` reaches it:

| site | file:line | has `p`? | wiring |
|---|---|---|---|
| `proj_from_peak` | `rl_model.py:977` | no (takes scalar `a`) | new kwarg `grace=0`, threaded from its callers |
| `prod_floor` | `rl_model.py:1009` | **yes** | `grace_years(p)` computed locally |
| `_proj_w4` (W4 wrapper) | `_merged_recover.py:945` | no | new kwarg `grace=0`, forwarded |
| `_prod_floor_w4` (W4 copy) | `_merged_recover.py:985` | **yes** | `grace_years(p)` computed locally |
| `player_raw` | `rl_model.py:1093` | **yes** | passes `grace=grace_years(p)` into `proj_from_peak` |
| `dp.v_at_peak` | `distribution_pricing.py:273/275` | **yes** | passes `grace=grace_years(p)` |
| synthetic / pick-level | `rl_model.py:1127/1139`, `build_cohort_book.py:185` | no player | `grace` omitted → 0. **DECLARED**: a synthetic band node is not a person and has no entry age. |

The `⚠ DUPLICATE-LOOP HAZARD` fence at `rl_model.py:994` is honoured: `prod_floor` and
`_prod_floor_w4` are edited **together**, identically.

**Mode 9 (path-product) coherence:** mode 9 is inactive on the live config (`RL_AGE_DISC=False`, flat
14%, ruled). For coherence the grace drops the earliest `grace` factors from the product
(`j` runs `grace+1 … k`). Declared, and asserted unreachable on the live config.

---

## 2. THE SEAM RULE FOR THE SOUTH BOUNDARY — FIXED BEFORE MEASUREMENT

All quantities on the **grace-A** basis, picks 1…64, ND arm, 26B-C1 slide applied.

1. `LL(p)` = the 26B-C2 local-linear estimator (`o26b_loclin.kernel_loclin`).
   `WM(p)` = the **shipped** weighted-mean aggregator (`harness_pvc_REPINNED_pass3.kernel_raw`).
   Same rows, same Gaussian kernel, same bandwidth-growth rule — the estimator is the only difference.
2. `d(p) = LL(p)/WM(p) − 1`, the signed relative deviation.
3. **INTERIOR NORM** `ν = p90( |d(p)| : p ∈ [4, 48] )`. Picks 1–3 are the declared **north** boundary
   zone (where loclin is ruled to hold and where `d` is large by design); 48 is the southern edge of
   the norm sample. The window `[4,48]` and the p90 statistic are fixed **now**.
4. **SOUTH TAIL ZONE** `Z` = the maximal contiguous run of picks **ending at 64** on which
   `|d(p)| > ν`. `p₁ = min(Z)`; the **SEAM PICK** `p₀ = p₁ − 1` is the last pure-loclin pick.
   *Guard:* if `Z` would reach north of pick **50**, it is TRUNCATED at 50 and the truncation is
   DISCLOSED — the owner ruled a tail correction, not a re-estimation of the interior. If `Z` is
   empty, the hybrid **is** loclin and that is reported as such.
5. **BLEND** — for `p ∈ Z`, with `t = (p − p₀)/(64 − p₀)` and smoothstep `S(t) = 3t² − 2t³`:

   ```
   w(p) = S(t)              HYB(p) = (1 − w(p))·LL(p) + w(p)·WM(p)
   HYB(p) = LL(p)           for p ∉ Z
   ```

   At `p = p₀`: `t = 0`, `w = 0` → `HYB = LL` **exactly** (value-continuity at the seam), and
   `S'(0) = 0` so the weighting introduces **no kink** of its own. At `p = 64`: `w = 1` → `HYB = WM(64)`
   exactly — the owner's "revert to the weighted-mean reading".
6. **THE ANCHOR IS UNTOUCHED.** Pick 1 is never in `Z` (guard 4), so `head = HYB(1) = LL(1)` and
   `anchor factor = 3000/head` are **identical** to 26B-V's grace-A. This is an assert, not a hope.
7. **NO-CLIFF ASSERT (able to fail).** Over `p ∈ [p₀, 64]`, the hybrid's largest adjacent relative
   step must not exceed the larger of the two parents' largest adjacent relative step over the same
   range. Reported as a number either way; a breach RETURNS TO THE OWNER, it is not smoothed away.
8. **MONOTONICITY** over `[p₀, 64]` is measured and DISCLOSED, never enforced.
9. **PER-PICK METHOD DISCLOSURE.** The full curve table prints, for every pick, which method produced
   it: `LL` / `blend w=x.xx` / `WM`. The zone is named in the packet headline.
10. **SCOPE.** The hybrid applies to the **all-in ND curve**. The positional relativities are ratios
    renormalised against `allin[p]` and therefore ride the hybrid level by construction; the Ruling-13
    reconciliation assert (`< 1e-12`) still binds and is re-run. Disclosed, not silent.

---

## 3. WHAT IS BUILT, AND WHAT PROVES IT

| gate | what it is | can it go red? |
|---|---|---|
| **BYTE-IDENTITY OFF** | full board rebuild from a clean staged copy with the dial present but `RL_GRACE=0`; md5 must equal **88ce647f531030d8d2e094188b258191** | yes — any accidental non-identity path shows as a different md5 |
| **IDENTITY GATE, DIAL ON** | the 26B scorer with grace vs the engine's own `price6` with `RL_GRACE=1`, both routing the same `disc_factor` | yes — a plumbing mismatch (grace on one side only) shows as a non-zero gap |
| **RULING-9 ±2%** | scored careers vs board price, read against **both** the live 88ce647f board and the dial-ON variant board | yes |
| **ANCHOR-INVARIANCE** | hybrid head/factor/premium == 26B-V grace-A to 1e-9 | yes |
| **NORTH/INTERIOR IDENTITY** | `HYB(p) == LL(p)` bit-exact for every `p ∉ Z` | yes |
| **RECONCILIATION (Ruling 13)** | `Σ_g share·posv == allin` to `< 1e-12` | yes |
| **26B-C1 ASSERTS** | force-majeure keys absent from every cohort input | yes |
| **NO-CLIFF** | §2.7 | yes |
| **DETERMINISM** | the dial-ON board built twice, md5 compared | yes |

---

## 4. PREDICTIONS — STATED BEFORE THE NUMBERS EXIST

**P1 — THE BOARD MOVER SET IS EXACTLY THE FIRST-YEAR NORMAL-AGE COHORT, AND NOTHING ELSE.**
By §1.1, `r > 0` only at `s = 0`. The eligible set is
`E = {active rows : debut(p) == 2026 and entry_age ≤ 19}`. **`|E| = 75`** — a definitional count off
the pinned store, taken before any board was built: 53 ND · 5 RD · 5 PDN · 3 PDA · 3 SSP · 3 IRE ·
2 MSD · 1 UNR; 69 at entry age 18, 6 at 19. They hold **53,426 of the board's 752,429 points (7.10%)**.
Thirty further debut-2026 rows are entry-age ≥ 20 and get **no** grace — the ruled discrimination,
visible as a control group.
- **Predicted movers: 60–75 of the 75, and ZERO rows outside `E`.** A row outside `E` moving is a
  PLUMBING DEFECT and a halt.
- **Direction: every mover UP.** A down-mover is a defect.
- **Predicted median mover delta +6% to +14%** (ceiling `×1.14` on the pure production leg, damped by
  the pedigree pole, iso_eff, caps and the numéraire).
- **Predicted board total +0.5% to +1.5%.**
- **willem-duursma is predicted to be the largest single-point riser** (ND pick 1, entry 18, 3,977
  today); **dyson-sharp, sullivan-robey, zeke-uwland, jacob-farrow, harry-dean** predicted in the top
  15 by points.

**P2 — BYTE-IDENTITY OFF PASSES.** Board md5 with the dial present and `RL_GRACE=0`
== `88ce647f531030d8d2e094188b258191`. This is the load-bearing safety claim of the order.

**P3 — THE IDENTITY GATE HOLDS BIT-EXACT WITH THE DIAL ON.** The price-function identity
(`mine` vs `price6`) is predicted at **max |ratio − 1| < 1e-9, 12 of 12** on the panel and
**≥ 799 of 800** board-wide, because both sides shift the *same* exponent inside the *same* callable.
Anything worse is a plumbing mismatch, not a tolerance.
**The Ruling-9 ±2% leg against the LIVE (dial-off) board must DEGRADE and that is correct, not a
failure**: the scorer moves and the frozen board does not. Predicted: **willem-duursma leaves the ±2%
class** (from +1.84% to roughly +14–17%), panel drops **2/12 → 1/12**, board-wide within-2% falls from
9.0% to **7–9%**. Read against the **dial-ON variant board** the same leg is predicted to **return to
2/12** with duursma back inside ±2% — that is the comparison that means anything, and both are printed.

**P4 — THE RE-DERIVED CURVE MATCHES 26B-V's GRACE-A AT NORTH AND INTERIOR, EXACTLY.**
`head = 3191.2`, `anchor factor = 0.9401`, `premium = −6.0%` — **identical to 26B-V grace-A to 1e-9**,
because the hybrid cannot reach pick 1. Anchored values at picks 1, 2, 3, 5, 7, 10, 15, 20, 30, 40
predicted **bit-identical** to 26B-V's grace-A row (3000 / 2668 / 2569 / 1804 / 1243 / 1312 / 803 /
859 / 607 / 479). Divergence confined to `Z`.

**P5 — THE SEAM SITS IN THE DEEP SOUTH.** Predicted `p₀ ∈ [50, 58]`, zone length **6–14 picks**.
Predicted interior norm `ν ∈ [0.02, 0.06]`.

**P6 — THE PICK-64 VALUE ROUGHLY DOUBLES AND LANDS NEAR TODAY'S PVC.**
Grace-A loclin gives **106**; the hybrid reverts to the weighted-mean reading. Predicted anchored
pick-64 under the hybrid **∈ [160, 210], point 183**, against today's PVC of **185** and the owner's
"198-class" shorthand (which is the weighted-mean curve anchored on its *own* head, `150.5 × 1.3131 =
197.6`; on the ruled loclin head it reads `WM(64) × af` instead — **the difference between 183 and 198
is the anchoring, not the estimator, and it is disclosed**).

**P7 — RAISING THE THRESHOLD PUSHES FOUR TO FIVE PATHWAYS OUTSIDE PICK 64.**
On grace-A loclin (threshold 106) only PDS and IRE sat outside. At a ~183 threshold, predicted
**OUTSIDE: UNR (125), PDN (111), PDS (101), IRE (95)**, with **PDA (188) on the boundary — inside but
within 5%**. Predicted **INSIDE: MSD, ND>64, SSP, RD**. Every pathway's own anchored value is
predicted **unchanged** from 26B-V grace-A (the pool ladder does not read the ND curve); only the
*equivalent pick label* moves, and that is the whole point of the threshold.

**P8 — POOLED AGGREGATES ARE UNCHANGED BY THE BOUNDARY.**
`pooled derived/printed = 0.3477` and `pooled derived/ANCHOR = 0.8950`, **identical to 26B-V grace-A**,
because pool derived-v0s read the pathway × position cells, not the ND curve. Predicted exact.
Positional medians likewise unchanged. **If these move, the boundary has leaked where it should not.**

**P9 — RECONCILIATION AND THE C1 ASSERTS HOLD.** Ruling-13 reconciliation `< 1e-12` (predicted
`~2.2e-16`); 26B-C1 (a) PASS.

**P10 — DETERMINISM.** The dial-ON board built twice gives the identical md5.

**P11 — THE NAMED-ROW CONTRAST.** `willem-duursma`'s **derived v0 does not move** (ND pick 1, north
end, 3157.2 under grace-A) while his **board price does** (he is in `E`). Both facts are predicted
together, and the packet prints them side by side, because they are the clearest single illustration
of what this order does and does not do.

---

## 5. WHAT THIS ORDER DOES NOT DO

No landing. The dial is **OFF by default** and no default changes. No store write. No identity carrier
re-pinned. No curve adopted. No pool level signed. `ui/release_pick_curve.json` untouched. The
movers-registry is **not** written (the #334 finding-11 lesson: an un-adopted board must never be
registered). The **2011-insertions fix order runs first**, before any of this can land, and the packet
says so on its face.

---

## 6. INPUT PROVENANCE

Copied verbatim from `build/delivered-value` into `inputs/` so this branch stands alone and the two
branches do not depend on each other; md5s in `inputs/MD5SUMS.txt`. Engine pins at prereg time:
store `d9a24282` · board `88ce647f` · `_merged_recover.py` `3f1468e5` · `rl_model.py` `e5eb5e44` ·
`dist_redesign.py` `48ea1bfe`.
