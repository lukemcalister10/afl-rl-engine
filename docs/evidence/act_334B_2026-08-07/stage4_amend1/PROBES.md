# STAGE 4 AMENDMENT 1 — THE PROBES

Full machine output: `probes_stage4a1.txt` / `.json` (Mraz + the pedigree pair), `boundary_stage4a1.txt` /
`.json` (the boundary DiD and the no-cliff sweep). Method carried verbatim from stage 4's `probes.py`, with
the surprise chain added to the Mraz decomposition and the boundary re-cut as an **A/B in one process**.

## (b) THE MRAZ PROBE

**Noah Mraz — KPD, ND pick 35 (2024), route debut 2025, year-1 sit-out, one season: 2026, 4 games @ 84.25.**

| | |
|---|---|
| **board value** | **2,898 → 1,585** (**−1,313, −45.31%**) |
| engine `ev()` | 3,050 → 1,585 |
| rank | 56 → below the top 150 |
| his pick's own ladder value (pick 35) | 530 → he is now **2.99×** it, was 5.47× |

**The chain, every quantity from the engine's own objects:**

| step | value |
|---|---|
| draft-day anchor `entry_anchor` | 461.25 |
| retention `R` at sit-out depth τ=1.826 | 0.45877 |
| **`anchor_full` = R × entry_anchor** (the prior-implied full price) | **211.61** |
| production path `e_full` (raw_ev × iso on 4g @ 84.25) | 5,068.48 |
| **the claim: `e_full / anchor_full`** | **23.952×** |
| **surprise `s` = \|log(23.952)\|** | **3.176066** nats |
| games at pace (season 88% elapsed) | 4.5455 |
| resolution: `rho(4.5455)/rho(6)` | 0.884761 resolved |
| **unresolved share `u`** | **0.115239** |
| **surprise demand `SUR_W × s × u`** | **5.0 × 3.176066 × 0.115239 = 1.830035** extra ramp passes |
| stage-4 exponent `1 + PED_BAR(1−q)` | 1.431093 |
| **amended exponent** | **3.261128** |
| `lam` | 0.693727 raw → 0.592618 (stage 4) → **0.303531** (amended) |

**In two sentences.** Four games claiming a 23.95× re-rate is the largest claim on the board bar one, and
the record backing it is 88.5% short of the establishment bar — so the engine now demands 1.83 further
passes of its own evidence ramp before it will price that claim. His `lam` — the share of his price taken
from the four-game estimate rather than from his anchor — falls from 0.593 to 0.304, so the anchor holds
the majority of his price instead of the minority; **nothing about his four games was altered, capped or
re-scored**, and if he plays on at that level the shrink dissolves continuously to nothing by six games.

## (c) THE PEDIGREE PAIR — the owner's judgment number

One identical record (4 games @ 84.25, KPD, age and position matched to Mraz) priced under all four entry
histories. Both age-holds reported, as at stage 4, because neither is free of a disclosed consequence.

### HOLD = DRAFT-AGE HELD (every arm drafted at the same draft age; sit-out arms are a year older as of 2026)

| arm | stage 4 | **amendment 1** | Δ |
|---|---|---|---|
| **(i)** pick 3, straight year-1 debut | 4,666 | **3,962** | −15.1% |
| **(ii)** pick 35, year-1 sit-out *(Mraz-shaped)* | 3,050 | **1,668** | **−45.3%** |
| **(iii)** pick 3, year-1 sit-out | 3,947 | **3,212** | −18.6% |
| **(iv)** pick 35, straight year-1 debut | 3,436 | **2,033** | −40.8% |
| **RATIO (i)/(ii)** | **1.5298** | **2.3753** | **+0.8455** |
| pure pedigree, straight debut (i)/(iv) | 1.3580 | **1.9488** | +0.5908 |
| pure pedigree, after a sit-out (iii)/(ii) | 1.2941 | **1.9257** | +0.6316 |
| pure sit-out at pick 3 (iii)/(i) | 0.8459 | 0.8107 | −0.0352 |
| pure sit-out at pick 35 (ii)/(iv) | 0.8877 | 0.8205 | −0.0672 |

### HOLD = AS-OF-AGE HELD (every arm the same age as of 2026; the 2025-drafted arms were drafted older)

| arm | stage 4 | **amendment 1** | Δ |
|---|---|---|---|
| **(i)** pick 3, straight year-1 debut | 4,058 | **3,564** | −12.2% |
| **(ii)** pick 35, year-1 sit-out | 3,050 | **1,668** | −45.3% |
| **(iii)** pick 3, year-1 sit-out | 3,947 | **3,212** | −18.6% |
| **(iv)** pick 35, straight year-1 debut | 3,062 | **1,885** | −38.4% |
| **RATIO (i)/(ii)** | **1.3305** | **2.1367** | **+0.8062** |

**Reading it.** The gap the owner asked stage 4 to open **widens further, and for the right reason.** The
top-pick arm falls too — it must, because a pick-3 player claiming the same 4-game re-rate is also making a
large claim on a thin sample, and `s` does not read the pick. But it falls far less (−15% vs −45%), because
its `anchor_full` is 2,375 rather than 212, so **the same four games are a much smaller surprise against a
top-5 prior** — `s` is smaller where the prior already expected something like this. The pedigree separation
therefore emerges from the statistic itself rather than from an added pedigree term, and it more than
doubles the pure-pedigree ratio (1.358 → 1.949).

## (d) THE BOUNDARY — the establishment bar

The dial is toggled **0 ↔ 5.0 inside one process**, so both arms are priced by the same loaded engine on the
same store with the same caches cleared. Prices are compared at the one-sided limits `6·fE ∓ 1e-4` raw games.

| probe | pos | pick | jump s4 | jump a1 | **SEAM RATIO** | prices AT the bar | placebo (3 at pace, mechanism live) |
|---|---|---|---|---|---|---|---|
| Noah Mraz | KPD | 35 | +1 | +1 | **1.0000** | **IDENTICAL** | −66.36% |
| Josh Smillie | MID | 7 | 0 | 0 | **1.0000** | **IDENTICAL** | −13.13% |
| Charlie West | KPF | 50 | 0 | 0 | **1.0000** | **IDENTICAL** | −82.56% |
| Samuel Swadling | MID | 37 | 0 | 0 | **1.0000** | **IDENTICAL** | −23.80% |

**Prices at the establishment bar are byte-identical across the change on all four probes.** The seam is
inert **twice over**: `lam(6)=1` and `1**e==1` (stage 4's argument), **and** `u(6)=0` exactly (this
amendment's own normalisation). The placebo column confirms the mechanism is emphatically **live** away from
the bar — the effect is in the ramp, never at the seam.

### The no-new-cliff sweep, raw games 1..10, both arms, three probes

| probe | check | result |
|---|---|---|
| all three | `u(g)` strictly decreasing in `g` (*more games → less shrink*) | **TRUE** |
| all three | level ratio reaches exactly **1.0000** at and above the bar (g≥6) | **TRUE** |
| all three | **amendment introduces NO new non-monotonicity in the price** | **NONE** |
| Smillie, West | amended price monotone non-decreasing in `g` (B6 law) | **TRUE** |
| Mraz | amended price monotone non-decreasing in `g` | False — **and the stage-4 arm is False in exactly the same places** (5,767 → 5,752 → 5,715 at g=8,9,10, *above* the bar where this amendment is inert and the two arms are identical). Pre-existing; not this change. |

**The level ratio is NOT monotone in `g`, and that is correct** — see `MEMO.md §7`. In this synthetic sweep
`e_full`, and therefore `s`, grows with `g` too, so the deepest shrink lands at two or three games rather
than at one: a one-game player claiming almost nothing has almost nothing to shrink. The design constraint
is *more games → less shrink at a fixed claim*, which is `u(g)`, and that is strictly monotone on every
probe. Full decomposition of `s(g)`, `u(g)` and the demand is printed in `boundary_stage4a1.txt`.

**Verdict: no new cliff anywhere in g = 1..10.**
