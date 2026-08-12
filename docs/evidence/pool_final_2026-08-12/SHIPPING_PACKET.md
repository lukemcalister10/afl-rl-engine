# ORDER 22 — THE POOL REPRICING SHIPPING PACKET

**NOTHING HERE IS LANDED.** The checkout's engine, board and signed table are untouched. Every number
below was measured on a scratchpad copy. The packet goes to the owner; only his word lands it.

---

# READ THIS FIRST — THE FOUR THINGS THAT MATTER

## 1. The pool is NOT twice over-priced. It is about right, and slightly UNDER-priced.

The directive says the pool returns **0.52** for every point of entry price against the national
draft's **1.03** — that the pool is roughly **half** priced correctly. **That reading divides by the
wrong number.**

A pool player's entry price is his **signed division level**. That is what the engine leans him on
before he has played. The directive's measure divides by a *different* engine value called
`v0_start`, which for a pool player is a leftover the owner's own #326 ruling took out of his entry
price. For the whole pool those two numbers are **2.7 times apart**.

Measured against the price he actually pays:

| | pool returns, per point of entry price | against the national target 0.9900 |
|---|---|---|
| the directive's measure (`v0_start`) | 0.3837 | **0.388** — "the pool is 2.6× over-priced" |
| **the price actually paid (`entry_anchor`)** | **1.0422** | **1.053** — the pool is 5% UNDER-priced |

**This is a measurement, not an opinion, and it was proved by execution rather than argued.** We cut
every signed pool level by 53–80% and rebuilt. The rookie draft's total `v0_start` moved **−1.5%**,
and **622 of 691 rookie rows did not move by one point.** The lever and the measure are different
objects. Iterating on the directive's measure does not converge — it runs away.

**What this means for the owner:** the big pool markdown the directive sized (the rookie draft
351,045 → 179,181, key defenders 300 → 83) **is not supported once the right denominator is used.**
The real repricing is much smaller and goes both ways.

## 2. The prices barely move — and the ones that do are mostly rookie key defenders going UP.

| | today | derived | change |
|---|---|---|---|
| rookie MID | 294.8 | **289** | −2% |
| rookie SD | 246.9 | **246** | −0% |
| rookie SF | 231.5 | **217** | −6% |
| rookie **KPD** | 300.3 | **370** | **+23%** |
| rookie KPF | 216.0 | **209** | −3% |
| rookie RUCK | 282.5 | **258** | −9% |
| SSP | 252.8 | **320** | **+27%** |
| MSD | 286.8 | **379** | **+32%** |
| IRE | 133.4 | **107** | −20% |
| PDA | 194.3 | **191** | −2% |
| PDN | 123.0 | **97** | −21% |
| PDS | 145.0 | **57** | **−61%** |
| UNR | 103.7 | **66** | −36% |
| ND>64 | 185 (capped) | **274 wanted — BLOCKED, see 4** | 0% |

**The directive's single largest finding reverses.** It says rookie key defenders are the most
expensive and the worst-delivering cell, and should fall from 300 to about 83. Measured against what
they actually pay, they are the **best**-delivering rookie cell and their price should **rise**.

## 3. The board moves +1.0%, and the separation law holds exactly.

**746,043 → 753,668, +7,625 (+1.022%), 109 rows move, 88 up and 21 down.**
**ND 1-64 board value: 620,877 before and 620,877 after. Non-pool rows moved: 0.**
Across the whole 24-year walk-forward: **0 national records repriced, 0 national v0s moved.**
**No arbitrage opened: 0 of 20 instrument readings.**

## 4. ONE PATHWAY CANNOT BE PRICED, AND IT IS A LAW THAT STOPS IT.

National-draft selections past pick 64 (`ND>64`) return **1.53×** what a national pick returns for
the same money — they are the most under-priced group in the book. The derivation says their level
should be **274**. **The signed ND65+ rule caps them at the curve's pick-64 value, which is 185.**
The cap is doing its job: a pick-65 selection priced above pick 64 would be an absurdity on the
ladder. But it means this group stays 53% under-priced, and — measurably — **that one blocked pathway
is what stops every other pathway from landing exactly on target.** Excluding it, the pool lands on
**0.9969**, within 0.31% of the target. **This is an owner decision, not a build one.**

---

# THE PINS, THE STAGE, AND THE CONTROLS

| pin | md5 | asserted |
|---|---|---|
| board `data/rl_build/rl_app_data.json` | `1dbd1480a34c7823f330273211cbb76a` | entry and exit, every instrument |
| store `engine/rl_after/rl_model_data.json` | `d9a24282357cf3083b1640466e3ecd83` | entry and exit |
| instrument `noarb_table_338.py` | `0f8220351c64c56ccfa90c60edcdfa5f` | **computed at run, never hardcoded** |
| instrument `noarb_table_allarm.py` | `3f9124de638d5ed30792dbdffef591b8` | computed at run |
| ORDER 21 surface (isotonic, SUPERSEDED) | `00ca5c3d1d4eca7e3b9a7d3ed3877d2e` | the stage this act opened on |
| **ORDER 22 surface (both amendments, IN FORCE)** | **`b595d49982a083ed760ce629759366b3`** | the stage everything below sits on |

**CONTROLS, all PASSED:**

| control | result |
|---|---|
| C1 unstaged build reproduces the live board | **`1dbd1480a34c7823f330273211cbb76a` BYTE-IDENTICAL** |
| C2 staged build reproduces ORDER 21's DERIVED board (run before the amendments arrived) | **`be89cbac9b0db6d70ecedc28696445ff` BYTE-IDENTICAL** |
| C3 this act's own builder with `nolevels` reproduces C2 | **`be89cbac…` BYTE-IDENTICAL** |
| C4 `harness_armsplit` with `split=False` reproduces the pinned harness | **value-for-value on all 2,644 rows, 0 differences** |
| C5 U re-derived at the checkout levels reproduces ORDER 21's published table | **exact to 6 decimals on all 10 rows** |
| C6 the U harvest reproduces ORDER 21's population | **4,241 cells / 3,334 complete-window / 1,325 sit-outs — exact, and every per-pathway count** |
| C7 `H`-retirement-only board reproduces ORDER 21's VARIANT A | **`452623adeb9aaed115d883dbe6b0239c` BYTE-IDENTICAL** |
| C8 relaxed surface's depth-1 row vs ORDER 21 | 14 of 30 vectors move, by ≤0.68% — **a consequence of amendment 2**, printed (see below) |

**The staged configuration, stated exactly:**

> **env** `RL_H_POOLSIT=1.0 RL_H_UNION=1.0` (manifest dials, gate mode, config hash restamped, boot guards armed)
> **patch** `o21_patch.py <worktree> derived <surface>` — the ORDER 21 patcher, **carried, never modified** (md5 `b2c01de9fc8fdb615adf35819ea5f9b3`)
> **levels** `o22_levels.py <worktree> <levels.json>` — the signed table, staged copy only
> **surface** `POOL_RETENTION_SURFACE_FINAL.json` (`b595d499…`)

---

# THE TWO MID-FLIGHT OWNER AMENDMENTS, AND WHAT THEY DID

Both arrived while the act was running. Both are folded into **one** surface regeneration, built by
`o22_make_relaxed_surface.py`, which **reads** ORDER 21's `pool_retention_derive.py` (md5
`6df38acbdf860db7c8387b4f87159342`, **never written**), applies nine printed textual substitutions,
and runs the copy from the scratchpad.

## Amendment 1 — the isotonic constraint relaxed at depths ≥ 2 (#334 comment 5262159933)

Owner: *"survival can be a more positive sign… it would be fine for 2 year sitters/3 year sitters to
reflect the data we have."*

## Amendment 2 — class-axis K=10 shrinkage (#334 comment 5262213139)

Owner: *"potentially we apply the K thing again to the KPP cells if there isn't much of a sample?"*

**THE ORDER OF OPERATIONS, DECLARED SO IT REPRODUCES:**

> kernel-smooth raw (depth axis only) → **class-axis K=10 shrink toward the all-class same-depth
> cell** → **clip [0.05, 1.0]** → **no isotonic step** → pathway layer K=10 borrowing, now borrowing
> from the **shrunk** whole-pool class cells.

**The whole-pool surface, before and after:**

| class | ORDER 21 (isotonic) | **ORDER 22 (relaxed + class-shrunk) — WIRED** |
|---|---|---|
| nonKPP | 0.6242 0.3799 0.3799 0.3799 0.3799 0.3799 | **0.6257 0.3828 0.4978 0.5111 0.4782 0.3896** |
| KPP | 0.8173 0.4996 0.4673 0.3594 0.3594 0.3363 | **0.8118 0.4910 0.4780 0.4008 0.3917 0.3674** |
| RUCK | 1.0000 0.5222 0.5222 0.4879 0.3543 0.3444 | **1.0000 0.4982 0.6236 0.4781 0.3959 0.3738** |

**30 depth-over-depth rises are now wired** across the 27 pathway × class vectors.

**Amendment 2 moves depth 1 too, and that is stated rather than discovered.** The coordinator's note
said depth 1 would be unchanged — that is true of amendment 1 alone (index 0 is never projected), but
the class-axis shrink applies at **every** depth. **14 of 30 wired vectors move at depth 1, all by
≤0.68%**; every move is printed in `RETENTION_RELAXED_out.txt`. The largest is whole-pool KPP
0.8173 → 0.8118 (−0.68%).

**THE WIRED CONSEQUENCE THE OWNER ACCEPTED, STATED PLAINLY:** a listed pool sitter's board value can
now **RISE** while he keeps sitting. A non-key-position pool sitter keeps **38.3%** of his entry
anchor at two years sat, **49.8%** at three and **51.1%** at four. That is the survival information
being priced as real. **This amendment is POOL-SCOPED — the national surface keeps its isotonic law
and is not touched by anything in this act.**

---

# THE TARGET, MEASURED FRESH

**`0.9900060981`** — the national arm's full-career profile, n = 1,443, measured on the staged engine
with **ORDER 20's ARM-SPLIT strata** (`harness_armsplit.structural_values(split=True)`).

**The separation law read at the calibration target itself: the target is IDENTICAL to the last
printed digit across all eight iteration rounds**, while pool prices moved through cuts of up to 61%.
Under the contaminated (unsplit) strata a pool price change moves the national target; under the
arm split it cannot, and eight rounds of execution say so.

---

# LAYER 1 — THE ALL-IN VALUE PER PATHWAY

Uniform **K=15** shrinkage toward the whole-pool aggregate, **every pathway** (owner verbatim,
2026-08-12: *"K=15 was across the board, not PDS"*). `w = n/(n+15)`.

**As first measured, on the staged engine at TODAY's levels:**

| pathway | n | w | raw profile | raw λ | shrunk profile | **shrunk λ** | level now | **derived level** |
|---|---|---|---|---|---|---|---|---|
| RD | 691 | 0.9788 | 0.988114 | 0.998089 | 0.989265 | **0.999251** | (positional) | (positional) |
| SSP | 52 | 0.7761 | 1.186956 | 1.198938 | 1.154557 | **1.166212** | 252.8 | **320** |
| MSD | 106 | 0.8760 | 1.223144 | 1.235491 | 1.200718 | **1.212839** | 286.8 | **379** |
| IRE | 57 | 0.7917 | 0.798728 | 0.806791 | 0.849460 | **0.858035** | 133.4 | **107** |
| PDA | 51 | 0.7727 | 0.961218 | 0.970921 | 0.979633 | **0.989522** | 194.3 | **191** |
| PDN | 43 | 0.7414 | 0.792315 | 0.800313 | 0.856952 | **0.865602** | 123.0 | **97** |
| PDS | 21 | 0.5833 | 0.441489 | 0.445946 | 0.691803 | **0.698787** | 145.0 | **57** |
| UNR | 59 | 0.7973 | 0.653470 | 0.660066 | 0.732275 | **0.739667** | 103.7 | **66** |
| ND>64 | 120 | 0.8889 | 1.517992 | 1.533316 | 1.465131 | **1.479921** | 185 (capped) | **274 — BLOCKED at 185** |
| **ALL POOL** | 1200 | — | **1.042243** | **1.052764** | (donor) | — | — | — |

**The shrinkage direction is exactly as predicted:** PDS (w 0.58) and PDN/IRE/UNR are pulled up
toward the pool; SSP and MSD are pulled down. RD (w 0.979) is effectively untouched.

**A note on ND>64 that matters for reading the table:** the stored `measured_k15` is 266.1, but the
level the engine actually reads is `min(266.1, curve[64]) = 185` — **the cap already binds today**.
Phase 1 divided by 266.1 and so mis-stated this pathway's current price by 44%. Corrected here.

---

# LAYER 2 — THE PLAYER v0 PER PATHWAY × POSITION

Keys: **pathway × position × age ONLY.** No pick axis and none invented — `effpk` is the constant
`POOL_PICK = 65` for every pool row. The age key is the multiplicative `_b_shape`/`_b_factor` leg,
which is **flat at 1.0** by ORDER 9 and is not wired here (see the age option below).

**13 of 54 cells reach n ≥ 20 and derive on their own outcomes** — exactly as pre-registered
(RD 6, ND>64 3, MSD 2, IRE 1, UNR 1). Thin cells borrow the **whole-pool** positional shape at
**K=10**; the unsampled remainder of a partially sampled pathway is priced as **its own residual
group** (rule 2); and **every pathway is RENORMALISED after borrowing**.

**THE FINAL WIRED LAYER-2 OBJECT — the rookie draft, the only pathway the signed table can express:**

| position | n | level now | **derived level** | change | own-cell λ (at today's levels) |
|---|---|---|---|---|---|
| MID | 176 | 294.8 | **289** | −2.0% | 0.9761 |
| SD | 158 | 246.9 | **246** | −0.4% | 0.9974 |
| SF | 149 | 231.5 | **217** | −6.3% | 0.9521 |
| **KPD** | 72 | 300.3 | **370** | **+23.2%** | **1.1970 — the best RD cell** |
| KPF | 65 | 216.0 | **209** | −3.2% | 0.9617 |
| RUCK | 71 | 282.5 | **258** | −8.7% | 0.9462 |

**A LIMIT THE BUILD FOUND AND DID NOT DECIDE.** The signed table carries positional cells for the
**rookie draft only**; the other eight pathways carry one flat level each. Their derived positional
cells are computed and printed in `DERIVE_FINAL_out.txt` — MSD MID at 1.61× the pathway value, UNR
MID at 1.73×, PDN KPD at 2.99× — but **they cannot be wired without adding structure to the signed
table.** That is an owner decision. **The load-bearing layer is delivered for the rookie draft, 691
of the 1,200 pool entrants.**

## THE RECONCILIATION PROOF

Entry-weighted in **both** layers, tolerance **1e-9 relative**:

| pathway | entry-weighted mean of the cells | the pathway's all-in value | relative residual |
|---|---|---|---|
| RD | 0.990257125528 | 0.990257125528 | **0.00e+00** |
| SSP | 0.990625668973 | 0.990625668973 | **0.00e+00** |
| MSD | 0.989627836729 | 0.989627836729 | 1.72e-16 |
| IRE | 0.988849577833 | 0.988849577833 | 1.42e-16 |
| PDA | 0.988366700409 | 0.988366700409 | **0.00e+00** |
| PDN | 0.991985074041 | 0.991985074041 | **0.00e+00** |
| PDS | 0.994818570197 | 0.994818570197 | **0.00e+00** |
| UNR | 0.993452549314 | 0.993452549314 | 2.21e-16 |
| ND>64 | 1.464925857437 | 1.464925857437 | **0.00e+00** |

**WORST RESIDUAL 2.21e-16 against a 1e-9 tolerance.** That is float noise, which is what an identity
should read.

**A CONDITION THIS BUILD FOUND, GENERALISING ORDER 17's.** ORDER 17 recorded that rule 2 alone fails
for PDS because the shrinkage moves the pathway off its own measured profile. **Under the owner's
uniform K=15 that is now true of EVERY pathway, RD included** (rule-2 residual 1.16e-03 for RD, up to
3.62e-01 for PDS, all nine failing). **The renormalisation guard is what makes the uniform-shrinkage
ruling and the reconciliation law compatible at all.** It is not optional and it is not cosmetic.

---

# THE ITERATE-TO-TOLERANCE STEP

**Declared tolerance, pre-registered: 1.0% relative on every pathway's λ. Declared cap: 8 rounds.**
Eight rounds were run — five on the superseded isotonic surface (A0–A4, which converged), then three
on the amended surface (R1, R2, F1), warm-started from that fixed point rather than restarted.

**The update rule.** `L ← L × λ`, then from round 2 a **declared secant acceleration**: the plain
rule assumes the numerator is invariant to the level, and it is not — a pool entrant with a thin
record is priced off the anchor, so cutting his level cuts his realised value too. Measured: PDS's
gap to 1 closed by only ~32% per round under the plain rule. Fitting `λ ∝ L^(−β)` on two consecutive
rounds and solving for `λ = 1` closed it. **β is clipped to [0.25, 3.0] and the per-round move is
capped at a factor of 2**; the fitted β is printed every round.

**RAW λ by round (pathway career profile ÷ the freshly measured target):**

| pathway | A0 | A1 | A2 | A3 | A4 | R1 | R2 | **F1** |
|---|---|---|---|---|---|---|---|---|
| RD | 0.9981 | 0.9964 | 0.9992 | 0.9999 | 1.0003 | 1.0019 | 0.9995 | **0.9994** |
| SSP | 1.1989 | 1.0554 | 1.0143 | 0.9892 | 0.9893 | 0.9900 | 0.9899 | **0.9896** |
| MSD | 1.2355 | 1.0591 | 1.0150 | 0.9947 | 0.9948 | 0.9963 | 0.9941 | **0.9941** |
| IRE | 0.8068 | 0.9311 | 0.9711 | 0.9880 | 0.9880 | 0.9883 | 0.9883 | **0.9883** |
| PDA | 0.9709 | 0.9805 | 0.9848 | 0.9897 | 0.9897 | 0.9919 | 0.9871 | **0.9864** |
| PDN | 0.8003 | 0.9129 | 0.9619 | 0.9892 | 0.9892 | 0.9892 | 0.9892 | **0.9891** |
| PDS | 0.4459 | 0.5994 | 0.7369 | 1.0244 | 0.9614 | 0.9808 | 0.9808 | **0.9806** |
| UNR | 0.6601 | 0.8613 | 0.9543 | 0.9945 | 0.9945 | 0.9944 | 0.9944 | **0.9945** |
| **ND>64** | 1.5333 | 1.5335 | 1.5337 | 1.5337 | 1.5337 | 1.5350 | 1.5350 | **1.5348** |
| ALL POOL | 1.0528 | 1.0414 | 1.0402 | 1.0395 | 1.0395 | 1.0411 | 1.0389 | **1.0389** |

**Monotone, no oscillation, and stable across the last three rounds to the fourth decimal.** PDS
overshoots once at A3 (1.0244) and the secant corrects it; that is reported, not smoothed.

**THE VERDICT, HONESTLY:**

| pathway | raw λ | \|raw−1\| | shrunk λ | \|shrunk−1\| | within 1%? |
|---|---|---|---|---|---|
| RD | 0.999416 | 0.06% | 1.000254 | 0.03% | **yes, both** |
| MSD | 0.994066 | 0.59% | 0.999618 | 0.04% | **yes, both** |
| UNR | 0.994488 | 0.55% | 1.003481 | 0.35% | **yes, both** |
| SSP | 0.989599 | 1.04% | 1.000626 | 0.06% | shrunk yes, raw 0.04pp out |
| PDN | 0.989143 | 1.09% | 1.001999 | 0.20% | shrunk yes, raw 0.09pp out |
| IRE | 0.988300 | 1.17% | 0.998832 | 0.12% | shrunk yes, raw 0.17pp out |
| PDA | 0.986430 | 1.36% | 0.998344 | 0.17% | shrunk yes, raw 0.36pp out |
| PDS | 0.980581 | 1.94% | 1.004861 | 0.49% | shrunk yes, raw 0.94pp out |
| **ND>64** | 1.534822 | **53.5%** | 1.479714 | **48.0%** | **NO — STRUCTURALLY BLOCKED** |

**The driven quantity — the shrunk λ the level step acts on — is within 0.49% on all eight
repriceable pathways.** The raw-λ residual is **an identity, not slack**, and this build proves it
rather than asserting it. Shrinkage makes `shrunk = w·raw + (1−w)·pool_aggregate`, so
`raw = (shrunk − (1−w)·pool_agg)/w`. Predicted against measured, at the final round:

| pathway | w | raw PREDICTED | raw MEASURED | difference |
|---|---|---|---|---|
| RD | 0.9788 | 0.999416 | 0.999416 | 1.1e-16 |
| SSP | 0.7761 | 0.989599 | 0.989599 | 0.0e+00 |
| PDS | 0.5833 | 0.980581 | 0.980581 | 2.2e-16 |
| *(all nine)* | | | | **≤ 2.2e-16** |

**And the pool aggregate is held above 1 by exactly one thing:**

| | pool aggregate |
|---|---|
| including ND>64 | **1.038853** |
| **excluding ND>64** (7.8% of the pool's entry weight) | **0.996912** |

**So: the iteration converged. The residual on seven of eight pathways is the arithmetic shadow of
the one pathway a signed law forbids repricing.** Lift or amend the ND65+ cap and every pathway lands
inside 0.5%. **NOT A BLOCKER OF THE BUILD — A BLOCKER OF ONE PATHWAY, AND IT IS THE OWNER'S CAP.**

**One quantisation fact, declared.** `rl_model.py:1425-1427` builds the engine's lookup with
`int(float(v))` — it **truncates**. Today's signed table is therefore already read one way and
written another: 133.4 is **133** in the engine, 286.8 is **286**, 294.8 is **294**. This act writes
**integers**, so the signed table and the engine's table become the same object and the up-to-0.9-point
silent haircut disappears. The cost is that a level of 57 moves in steps of 1.75%; every step size is
printed each round.

---

# BOTH HEADLINE METRICS — NEITHER IS A TARGET, BOTH ARE READ

At the final configuration, on the price actually paid:

| pathway | n | **CAREER PROFILE** | vs target | **YEAR 4 / YEAR 0** | vs target |
|---|---|---|---|---|---|
| NATIONAL 1-64 | 1443 | 0.990006 | 1.000000 | **1.554717** | 1.000000 |
| RD | 691 | 0.989428 | 0.999416 | 1.380578 | 0.887993 |
| SSP | 52 | 0.979709 | 0.989599 | 1.244563 | 0.800508 |
| MSD | 106 | 0.984131 | 0.994066 | 0.861547 | 0.554151 |
| IRE | 57 | 0.978423 | 0.988300 | 1.224208 | 0.787416 |
| PDA | 51 | 0.976571 | 0.986430 | 1.599841 | 1.029024 |
| PDN | 43 | 0.979257 | 0.989143 | 1.168689 | 0.751705 |
| PDS | 21 | 0.970781 | 0.980581 | 1.401896 | 0.901705 |
| UNR | 59 | 0.984550 | 0.994488 | 2.410193 | 1.550246 |
| ND>64 | 120 | 1.519483 | 1.534822 | 1.955962 | 1.258083 |
| **ALL POOL** | 1200 | **1.028471** | **1.038853** | **1.394887** | **0.897197** |

**The two answer different questions and the gap between them is the finding.** Calibrating the whole
career leaves year four far from 1: MSD reads 0.86 at year four while its career profile reads 0.98,
and UNR reads 2.41 while its career reads 0.98. **YEAR 4 IS NOT A TARGET** — the standing law is
unchanged and nothing here aimed at it.

---

# BOTH COHORT INSTRUMENTS, WITH THE 14% CHARGE BESIDE EVERY READING

`margin vs 14% = 14% − (year-0 → year-1 appreciation)`. **A negative margin is an arbitrage.**

## All-arm DECIDING instrument (`noarb_table_allarm.py`)

| window | variant | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | apprec 0→1 | **margin vs 14%** | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| PRIMARY n=2212 | SHIP | 1.0000 | 0.7767 | 0.9581 | 1.0608 | 1.1231 | 1.1047 | −22.33% | **+36.33%** | no arb |
| PRIMARY | ORDER 21 staged | 1.0000 | 0.7995 | 0.9660 | 1.0638 | 1.1275 | 1.1082 | −20.05% | **+34.05%** | no arb |
| PRIMARY | **FINAL** | 1.0000 | **0.7988** | 0.9672 | 1.0671 | 1.1300 | 1.1104 | −20.12% | **+34.12%** | **no arb** |
| PRIMARY | FINAL + O1 | 1.0000 | 0.7988 | 0.9674 | 1.0679 | 1.1304 | 1.1106 | −20.12% | **+34.12%** | no arb |
| MODERN n=540 | SHIP | 1.0000 | 0.8007 | 0.9084 | 0.9717 | 0.9734 | 1.0309 | −19.93% | **+33.93%** | no arb |
| MODERN | **FINAL** | 1.0000 | **0.8180** | 0.9184 | 0.9752 | 0.9788 | 1.0362 | −18.20% | **+32.20%** | **no arb** |

## Legacy retained instrument (`noarb_table_338.py`, UNMODIFIED)

| group | SHIP | **FINAL** | apprec 0→1 | **margin vs 14%** | verdict |
|---|---|---|---|---|---|
| ALL picks 1-64 | 1.0730 | **1.0730** | +7.30% | **+6.70% → +6.70%** | no arb |
| picks 1-20 | 1.1218 | **1.1218** | +12.18% | **+1.82% → +1.82%** | no arb |
| picks 21-64 | 0.9994 | **0.9995** | −0.05% | **+14.06% → +14.05%** | no arb |

**The legacy 1-64 aggregate does not move at all.** The picks 21-64 slice moves by +0.0001, and
`separation_check.py` named the single row responsible in ORDER 21: **`daniel-butler`**, a POOL row
admitted to a population selected by *stored* pick number — the documented crosser, not a national
reprice.

> **ARBITRAGES OPENED BY THE FINAL CONFIGURATION: 0 of 20 readings. No arbitrage-grade flag is raised.**

---

# BOARD TOTALS AND THE COMPOSED POOL-UPDATE MOVERS LEDGER

| board | md5 | total | vs LIVE | % | moved | up | down |
|---|---|---|---|---|---|---|---|
| **LIVE** | `1dbd1480a34c7823f330273211cbb76a` | 746,043 | — | — | — | — | — |
| lever 1 — H retirement only | `452623adeb9aaed115d883dbe6b0239c` | 748,355 | +2,312 | +0.310% | 48 | 48 | 0 |
| lever 2 — + the derived retention | `b65212c6d5096809c0993de411a390ef` | 751,679 | +5,636 | +0.755% | 82 | 74 | 8 |
| **lever 3 — + the repricing (FINAL)** | **`21055b901312f76a8f0b17d362932130`** | **753,668** | **+7,625** | **+1.022%** | **109** | **88** | **21** |
| FINAL with owner override O1 applied | `e97974ed9f963123c4d019b912f79523` | 753,797 | +7,754 | +1.039% | 113 | 92 | 21 |

**Lever totals across every moved row: H retirement +2,312 · retention +3,324 · repricing +1,989.**

## By pathway

| pathway | rows | moved | LIVE | H only | + retention | **FINAL** | **Δ** | **%** |
|---|---|---|---|---|---|---|---|---|
| **ND 1-64** | **561** | **0** | **620,877** | **620,877** | **620,877** | **620,877** | **0** | **+0.000%** |
| RD | 66 | 22 | 45,874 | 46,148 | 46,304 | 46,235 | +361 | +0.787% |
| MSD | 63 | 35 | 36,089 | 36,962 | 39,404 | 41,604 | **+5,515** | **+15.282%** |
| ND>64 | 28 | 4 | 18,828 | 18,887 | 18,945 | 18,945 | +117 | +0.621% |
| SSP | 28 | 14 | 11,535 | 12,237 | 12,240 | 12,568 | +1,033 | +8.955% |
| PDA | 15 | 5 | 8,103 | 8,159 | 8,263 | 8,255 | +152 | +1.876% |
| PDN | 16 | 10 | 2,729 | 2,906 | 3,325 | 3,149 | +420 | +15.390% |
| IRE | 14 | 10 | 712 | 803 | 950 | 828 | +116 | +16.292% |
| **UNR** | 13 | 9 | 1,296 | 1,376 | 1,371 | **1,207** | **−89** | **−6.867%** |

## The largest movers, named, with the lever decomposition

| player | pathway | pos | LIVE | H only | + retention | **FINAL** | **Δ** | % | lever H | lever retention | lever repricing |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Mani Liddy | MSD | MID | 128 | 128 | 785 | **1039** | **+911** | +711.7% | 0 | +657 | +254 |
| Nicholas Martin | SSP | SF | 2822 | 3509 | 3518 | **3520** | **+698** | +24.7% | +687 | +9 | +2 |
| Robert Hansen | MSD | SF | 80 | 80 | 509 | **658** | **+578** | +722.5% | 0 | +429 | +149 |
| Flynn Young | MSD | SF | 128 | 128 | 386 | **508** | **+380** | +296.9% | 0 | +258 | +122 |
| James Blanck | MSD | KPD | 60 | 60 | 333 | **437** | **+377** | +628.3% | 0 | +273 | +104 |
| Caleb May | MSD | RUCK | 52 | 231 | 274 | **362** | **+310** | +596.2% | +179 | +43 | +88 |
| Harrison Coe | MSD | RUCK | 52 | 231 | 274 | **362** | **+310** | +596.2% | +179 | +43 | +88 |
| Max Mapley | MSD | RUCK | 52 | 231 | 274 | **362** | **+310** | +596.2% | +179 | +43 | +88 |
| Will McLachlan | MSD | SF | 117 | 117 | 317 | **390** | **+273** | +233.3% | 0 | +200 | +73 |
| Tom Hanily | MSD | SF | 154 | 154 | 286 | **334** | **+180** | +116.9% | 0 | +132 | +48 |

**21 rows go DOWN**, driven by the repricing lever on the pathways whose levels fall (UNR −36%,
PDS −61%, PDN −21%, IRE −20%). **The full ledger — all 109 rows, each with its three lever
components — is in `CONSEQUENCE.json['ledger']`.**

**A finding worth the owner's eye:** the biggest movers are all MSD, and their moves are dominated by
the **retention** lever, not the repricing. The repricing itself is the smallest of the three levers
(+1,989 of +7,625). **This act's headline change is the smallest part of its board effect.**

---

# U RE-DERIVED ON THE REPRICED LEVELS

ORDER 21 handed this back: `U` is a pure function of sit share and mean `R`, weighted by
`entry_anchor`, so it moves when the levels move; `R` is a ratio and carries unchanged.

**AND THE ANSWER IS DERIVED, NOT ASSERTED.** `entry_anchor(p) = pool_level(p) × _PL_F × _b_factor(p)`
and `_b_factor == 1.0 exactly` (asserted on every harvested row, 0 violations). So `e` is a pure
function of the signed division. **For the eight pathways that carry ONE flat level, `e` is the same
constant for every row and CANCELS OUT of U — their U cannot move when their own level moves.** Only
**RD** (six positional levels, so `e` varies within the pathway) and the ALL POOL aggregate can move.

| pathway | cells | sitters | sit share (wtd) | **mean R (sitters)** | **U (everyone else)** | post-redistribution mean |
|---|---|---|---|---|---|---|
| RD | 2352 | 832 | 0.3522 | 0.620537 | **1.206324** | **1.0000000000** |
| ND>64 | 441 | 193 | 0.4376 | 0.526268 | **1.368670** | **1.0000000000** |
| IRE | 137 | 70 | 0.5109 | 0.676516 | **1.337969** | **1.0000000000** |
| UNR | 126 | 65 | 0.5159 | 0.526965 | **1.504054** | **1.0000000000** |
| PDA | 106 | 53 | 0.5000 | 0.385563 | **1.614437** | **1.0000000000** |
| PDS | 62 | 36 | 0.5806 | 0.699571 | **1.415978** | **1.0000000000** |
| MSD | 40 | 34 | 0.8500 | 0.630135 | **3.095901** | **1.0000000000** |
| PDN | 36 | 29 | 0.8056 | 0.735545 | **2.095600** | **1.0000000000** |
| SSP | 34 | 13 | 0.3824 | 0.676768 | **1.200096** | **1.0000000000** |
| **ALL POOL** | 3334 | 1325 | 0.3829 | **0.604156** | **1.245650** | **1.0000000000** |

**Pathways whose post-redistribution entry-weighted mean is not exactly 1: 0. The instrument halts
otherwise.** The mean-preserving law survives both amendments and the repricing intact.

**PDA is still charged MORE than the shipped read** (its depth-1 nonKPP cell is the harshest fitted
cell), though the class-axis shrinkage softened it: mean R 0.3517 → **0.3856**.

---

# `_ruc_prior_cap` — CHECKED, AND IT BINDS

The cap is `v0 := min(v0_uncapped, RUC_PRIOR_CAP × _cap_basis(p) × _ruc_head_v0(p))`, and for a pool
row `_cap_basis(p) == pool_level(p)` in **ladder currency, unconverted**.

**It binds on 121 of 140 pool ruck rows.** A bound row's v0 is **exactly 1.400 × the signed level**,
before and after — e.g. `flynn-riley`, level 286 → 379, v0 400.4 → 530.6 (+32.5%), moving one for one
with the level.

| pathway | rucks | on the cap | Σ v0 SHIP | Σ v0 FINAL | Δ% | level SHIP → FINAL |
|---|---|---|---|---|---|---|
| RD | 71 | 66 | 27,575.8 | 25,358.2 | −8.04% | 282 → 258 |
| UNR | 30 | 30 | 4,326.0 | 2,772.0 | **−35.92%** | 103 → 66 |
| MSD | 14 | 11 | 5,170.6 | 6,673.3 | **+29.06%** | 286 → 379 |
| ND>64 | 9 | 0 | 2,092.9 | 2,092.9 | 0.00% | 185 → 185 (level unmoved, so the test cannot separate — declared) |
| SSP | 6 | 4 | 1,905.8 | 2,286.6 | +19.98% | 252 → 320 |
| PDA | 5 | 5 | 1,358.0 | 1,337.0 | −1.55% | 194 → 191 |
| IRE | 2 | 2 | 372.4 | 299.6 | −19.55% | 133 → 107 |
| PDN | 2 | 2 | 344.4 | 271.6 | −21.14% | 123 → 97 |
| PDS | 1 | 1 | 203.0 | 79.8 | −60.69% | 145 → 57 |

**This is the same finding as the denominator departure, seen from the other side: the ruck prior cap
is the ONLY route by which a signed pool level reaches `v0_start` at all.** 122 pool records' v0
moved; every one is a ruck at the cap.

---

# NO AGE ADJUSTMENT IS WIRED — THE OPTION, WITH ITS NUMBERS (directive D7)

Nothing age-related is wired. The RD-only quality-fitted signal from phase 1 (`phase1_age.py`,
branch `build/pool-repricing-phase1`) is presented as an **OPTION**:

| stream | t | \|t\|≥2 | % of mean | ruling under the pre-specified rule |
|---|---|---|---|---|
| ND 1-64 | 0.19 | NO | 1.6% | no adjustment |
| **RD** | **2.45** | **yes** | **25.9%** | **AGE ADJUSTMENT EARNED** |
| SSP | 0.74 | NO | 10.2% | no adjustment |
| MSD | 0.96 | NO | 16.8% | no adjustment |
| IRE | −0.64 | NO | 14.7% | no adjustment |
| PDA | 0.60 | NO | 16.0% | no adjustment |
| PDN | 1.02 | NO | 28.8% | no adjustment |
| PDS | 0.14 | NO | 7.7% | no adjustment |
| UNR | 0.88 | NO | 21.2% | no adjustment |
| ND>64 | 1.26 | NO | 28.7% | no adjustment |

**One of nine pool pathways earns an age adjustment; eight get none, and the national draft shows no
age signal at all (t = 0.19).** The fit is to **playing quality only** — the play-quality principle,
which is what retired ITEM B's steps: quality and participation move differently across age bands
(RD quality 56.40 / 62.34 / 63.00 against career games 65.9 / 91.8 / 66.1). **Wiring this is the
owner's call and it is not in this configuration.**

---

# THE SEPARATION ASSERTIONS — ASSERTED AND PRINTED

| check | result |
|---|---|
| ND 1-64 board rows moved, every lever | **0** |
| ANY non-pool board row moved, every lever | **0** |
| ND 1-64 board value, LIVE and FINAL | **620,877 → 620,877** |
| national records repriced on ANY year of the 24-year walk-forward (1,443 records) | **0** |
| national records whose **v0** moved, SHIP vs FINAL | **0 — exactly zero, not merely small** |
| the calibration target across all 8 iteration rounds | **0.9900060981 at every round — 1 distinct value** |

1,130 records reprice on the walk-forward under the final configuration and **every single one is a
pool record**. The instrument is plainly sensitive; the national arm still does not move by one float
bit.

---

# THE FLAGS CARRIED TO THE OWNER — THE SEAT RULES NONE OF THEM

## (a) Owner override O1 on the pool retention object — **now nearly moot, and here is why**

O1 is the owner's signed override on the **national** surface: `KPP := pointwise max(KPP, nonKPP)`.
On the ORDER 22 surface it binds at **4 of 6** whole-pool KPP depths (up from 3) and **33 of 60**
cells overall — the isotonic relaxation raised nonKPP's deep cells, so KPP sits below it more often.

**But the class-axis shrinkage (amendment 2) already did what O1 was for.** Deep KPP rests on 17/7/3
raw sit-out seasons, and those cells now pull toward the pooled cell by their own weight.

**The board consequence is almost nothing:**

| | board total | vs FINAL | rows moved by O1 |
|---|---|---|---|
| FINAL, O1 OFF (wired) | **753,668** | — | — |
| FINAL, O1 ON | 753,797 | **+129 (+0.017%)** | **4** |

Named, all four: Xavier Walsh (RD KPF) 143 → 206 · Hudson O'Keeffe (SSP KPF) 187 → 218 ·
Max Ramsden (MSD KPF) 169 → 197 · Luker Kentfield (MSD KPF) 271 → 278.
**Instrument consequence: none — every margin identical to two decimal places, 0 arbitrages both
ways.** **The owner rules; the numbers say it barely matters either way.**

## (b) RUCK depth-1 = 1.000 on the clip ceiling

A first-year pool ruck sitter is charged **nothing**. The unclipped ratio exceeds 1 — a depth-1 pool
ruck who has not yet qualified realises *more* forward output than the same-depth all-pool ruck
average, which is the survivor-selection norm at its most extreme (RUCK d1 norm 0.240). The clip is
the ND method's own `[0.05, 1.0]`, carried. **Survived both amendments unchanged. Flagged, not
smoothed.**

## (c) PDA is charged MORE than today

Derived mean R **0.3856** against today's composed **0.4077**. Its depth-1 nonKPP cell is the
harshest fitted cell in the surface, at n = 23. The class-axis shrinkage softened it (0.3517 →
0.3856) but did not reverse it. **Small and harsh; worth a second look before landing.**

## (d) THIS BUILD ADDS FOUR — and the first two are the largest things in the packet

**(d1) THE DENOMINATOR. The directive's derivation basis divides by a number the pool does not pay.**
The full argument is section 1 above. **It reverses the directive's central claim and its largest
positional finding.** This is ORDER 21's own D2 departure — *"a surface derived against `v0_start`
and then multiplied onto `entry_anchor` would not be a retention of anything"* — applied to the level
instead of the retention. **The seat adopted it to produce a converging derivation and flags it as
the packet's first owner question.** Both bases are printed on every table.

**(d2) THE ND65+ CAP BLOCKS THE MOST UNDER-PRICED GROUP IN THE BOOK.** ND>64 returns 1.53× the
target; its derived level is 274; the signed cap holds it at 185 (the curve's pick-64 value). The cap
is not a number but a **law** (`"THE CAP IS A LAW, NOT A NUMBER"`), and it exists to stop a pick-65
selection outpricing pick 64. **It is also, provably, the sole reason the other eight pathways land
1% short instead of exactly on target.**

**(d3) LAYER 2 IS ONLY WIRABLE FOR THE ROOKIE DRAFT.** The signed table has positional cells for RD
alone. The other eight pathways' derived positional cells are real, computed and printed — and
un-installable without new structure the owner would have to sign.

**(d4) ADOPTION REQUIRES THE OWNER'S SIGNATURE IN CODE, BY DESIGN.** `one_source_selftest.py:624-626`
carries the N43 levels as **literals** (`_N43_FLAT`, `_N43_RD`, `_N43_ND65_K15`) and checks the
artefact against them, *"so that an edited level would agree with itself and pass"*. The board build
does not run that gate, so this staging does not trip it — **but nothing here can land until the
owner re-signs those literals.** The guard works exactly as intended and is reported as a feature.

---

# PRE-REGISTRATION SCORING — 25 + 8 PREDICTIONS, BREACHES OWNED

`PREREG_ORDER22.md` committed at `6cdb9b2` before any measurement; `PREREG_ORDER22_ADDENDUM.md`
committed at `68af31d` after the first ruling and before any measurement on the amended stage.

| # | prediction | measured | result |
|---|---|---|---|
| P1 | target in 0.97–1.02 | **0.9900060981** | ✓ |
| P2 | C1 reproduces `1dbd1480` | byte-identical | ✓ |
| P3 | C2 reproduces `be89cbac` | byte-identical (run before the amendments) | ✓, then **SUPERSEDED** |
| P4 | raw λ order SSP > MSD > ND>64 > RD > PDA > UNR > IRE > PDN > PDS | **ND>64 > MSD > SSP > PDA > IRE > PDN > UNR > RD > PDS** | **BREACH** — ND>64 is the most under-priced group, not fourth; and RD sits near the bottom because it is already right. The prediction was inherited from the directive's basis, which the act then showed to be the wrong basis. Owned as a prediction made on a measure I went on to reject. |
| P5 | RD w > 0.97; PDS w < 0.62; others 0.70–0.99 | 0.9788 / 0.5833 / 0.7414–0.8889 | ✓ |
| P6 | shrinkage lifts PDS/PDN/IRE/UNR/PDA, lowers SSP/MSD | exactly that | ✓ |
| P7 | reconciliation worst residual ≤1e-9, in fact <1e-12 | **2.21e-16** | ✓ |
| P8 | rule 1 fails on ≥3 partially-sampled pathways; rule 2 passes all nine | rule 1 fails on 4; **rule 2 fails on all nine** | **BREACH, and it is the packet's most useful one** — under uniform K=15 rule 2 alone fails everywhere; only rule 2 **plus the renormalisation guard** passes. ORDER 17 saw this for PDS; the owner's uniform ruling generalised it. |
| P9 | 13 of 54 sampled cells (RD 6, ND>64 3, MSD 2, IRE 1, UNR 1) | **13 of 54, exactly that split** | ✓ |
| P10 | derived RD order RUCK highest, KPD lowest | **KPD highest (1.197), RUCK 0.946** — inverted | **BREACH** — same root cause as P4: the prediction was made on the directive's basis. |
| P11 | converges to 1.0% on every pathway within 6 rounds | 8 rounds; **shrunk λ within 0.49% on all 8 repriceable pathways; raw λ within 1% on 3 of 8**; ND>64 structurally blocked | **PARTIAL BREACH**, re-scored as R4 |
| P12 | board total falls vs 751,554 | **rises to 753,668** | **BREACH** — the baseline moved with the amendments, and the repricing raises MSD/SSP rather than cutting the pool. |
| P13 | ND rows moved 0; national v0 delta 0 | **0 and 0** | ✓ |
| P14 | all-arm PRIMARY yr1 rises vs 0.7995 | **0.7988 — falls by 0.0007** | **BREACH**, tiny and in the opposite direction |
| P15 | 0 of 5 readings open an arbitrage | **0 of 20** | ✓ |
| P16 | legacy 1-64 margin moves ≤0.05 pts | **0.00 pts** | ✓ |
| P17 | `_ruc_prior_cap` binds on ≥1 pathway's rucks | **121 of 140 rows, 8 of 9 pathways** | ✓ |
| P18 | derived ND>64 lands below the 185 cap | **274 — the cap BINDS** | **BREACH**, and it became flag (d2) |
| P19 | RD the only pathway with \|t\|>2 age signal | RD t=2.45, only one | ✓ |
| P20 | int truncation costs <1.0% on every level | up to **1.75%** at PDS=57 | **BREACH** — mitigated by writing integers, so the residual truncation cost is now **0.000%** on every level |
| P21 | layer 2 wirable for RD only | confirmed | ✓ |
| P22 | ND 1-64 board value exactly 620,877 | **620,877** | ✓ |
| P23 | ≤120 pool board rows move | **109** | ✓ |
| P24 | pool yr4/yr0 rises vs SHIP and stays below ND's | 1.3949 vs ND 1.5547 — below ✓ | ✓ |
| P25 | all four flags carried unresolved; the seat rules none | four carried, and this build added four more | ✓ |
| **R1** | staged board on the amended surface differs from `be89cbac`, total above 751,554 | `b65212c6…`, **751,679** | ✓ |
| **R2** | unstaged control still reproduces `1dbd1480` | byte-identical | ✓ |
| **R3** | depth-1 identical to ORDER 21 at all 30 vectors | **14 of 30 move**, ≤0.68% | **BREACH** — true of amendment 1 alone; amendment 2 shrinks at every depth. Predicted before amendment 2 arrived; the cause is named and every move printed. |
| **R4** | ≤3 further rounds to tolerance, warm-started | **3 rounds (R1, R2, F1)**, and stable to 4 decimals across the last three | ✓ |
| **R5** | O1 binds at more than 3 of 6 KPP depths, larger gaps | **4 of 6** | ✓ |
| **R6** | pool sitters whose value can rise while sitting > 0 | nonKPP d2 0.383 → d3 0.498 → d4 0.511, wired | ✓ (surface arithmetic; the live-row incidence is **not separately enumerated** — declared) |
| **R7** | 0 of 5 readings open an arbitrage | **0 of 20** | ✓ |
| **R8** | separation unchanged by the amendments | 0 and 0 | ✓ |

**SCORE: 24 held, 8 breached, 1 partial.** Six of the breaches (P4, P10, P12, P14, P18, P20) trace to
two roots — predictions anchored to the directive's denominator, which the act then measured to be
wrong, and a baseline that two mid-flight rulings moved. **They are listed as breaches, not
re-labelled as discoveries.**

---

# WHAT IS UNRESOLVED, AND HANDED BACK

1. **The denominator (d1).** The largest question in the packet. Both bases printed everywhere.
2. **The ND65+ cap (d2).** Blocks the most under-priced group and is the arithmetic cause of the last
   1% of residual on every other pathway.
3. **Layer-2 structure for the eight non-RD pathways (d3).** Derived, printed, un-installable.
4. **Owner override O1 (a).** Binds at 4 of 6 depths; worth +129 board points and 4 rows.
5. **RUCK depth-1 = 1.000 (b)** and **PDA harsher than today (c).**
6. **The age adjustment (D7).** RD earns one on quality; nothing is wired.
7. **The N43 re-signature (d4).** Adoption requires it, by the guard's own design.
8. **The live-board incidence of rising sitters** was not separately enumerated — the surface
   arithmetic is printed instead, and this is a declared gap rather than a silent one.

---

# REPRODUCE

    export PATH="/root/rl_venv312/bin:$PATH"
    E=docs/evidence/pool_final_2026-08-12
    OPENBLAS_NUM_THREADS=1 python3 $E/o22_make_relaxed_surface.py $E/POOL_RETENTION_SURFACE_FINAL.json
    OPENBLAS_NUM_THREADS=1 python3 $E/o22_uharvest.py  $SP/o22/ucells.json
    bash $E/build_board_o22.sh $SP/o22/board_C1_unstaged.json nopatch nolevels        # -> 1dbd1480
    O22_SURFACE=$SP/o22/iter/surface_F1.json bash $E/build_board_o22.sh \
        $SP/o22/board_FINAL.json derived $E/FINAL_LEVELS.json RL_H_POOLSIT=1.0 RL_H_UNION=1.0
    O22_SURFACE=$SP/o22/iter/surface_F1.json bash $E/emit_variant_o22.sh \
        F1 derived $E/FINAL_LEVELS.json RL_H_POOLSIT=1.0 RL_H_UNION=1.0
    python3 $E/o22_derive.py $SP/per_entrant_O22F1.json $E/FINAL_LEVELS.json /tmp/d.json FINAL
    bash   $E/run_noarb_o22.sh <ship.json> SHIP <final.json> FINAL
    python3 $E/o22_margins.py $E/NOARB_MARGINS.json SHIP FINAL
    python3 $E/o22_consequence.py $E/CONSEQUENCE.json
    python3 $E/o22_separation_ruck.py <ship.json> <final.json> $E/FINAL_LEVELS.json $E/SEPARATION_RUCK.json
    python3 $E/o22_trajectory.py $E/ITERATION.json A0 A1 A2 A3 A4 R1 R2 F1

**THE PACKET GOES TO THE OWNER. NOTHING LANDS WITHOUT HIS WORD ON IT.**
