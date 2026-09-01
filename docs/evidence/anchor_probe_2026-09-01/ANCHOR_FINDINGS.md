# The player/pick anchor: what I can prove, what I disproved of my own, and what I could not settle

**Date:** 2026-09-01 · READ-ONLY investigation, owner-directed. **Nothing was changed.**

## The question

```
BOARD_FACTOR = (_P1 / PVC[1]) * _NUM['s']          rl_model.py:1556
SCALE        = SCALE * BOARD_FACTOR                 → every player value on the board
```

Is that second `s` doing work, or is it applied twice?

## 1. THE ALGEBRA — established, and it reproduces the live number exactly

`_load_numeraire` HALTS the build unless BOTH of these hold, so they are not assumptions:

* `s == published_pin / pooled_head_pre_scale` (coherence halt at 1e-9)
* `RL_PICK1 == published_pin` (a second halt, by name)

Therefore `_P1` is **not independent**: `_P1 == published_pin == H · s`. Substituting:

```
shipped   BOARD_FACTOR = (_P1/PVC[1])·s = (H·s/PVC[1])·s = H·s² / PVC[1]
                       = 3191.178972 · 0.9400914291² / 3784  =  0.7453156150
measured live BOARD_FACTOR                                   =  0.7453156150   ✓ to 10 dp
```

**The shipped form carries `s` squared.** That is arithmetic, not interpretation.

## 2. EVERY DIMENSIONAL ROUTE I CAN CONSTRUCT GIVES ONE `s`, NOT TWO

`PVC[1] = 3784` is pick 1's worth in **pre-anchor player money** — `build_pvc_v34` step 5 anchors its
shape to `build_pvc(ALPHA)`'s top band, which is `peakval()`, a player-side quantity. Two routes:

* normalise players by v3.4's head → "fraction of pick 1" → multiply by the PUBLISHED pin:
  `_P1/PVC[1]`
* normalise by v3.4's head → multiply by the adopted RAW head `H` → then publish with `·s`:
  `(H/PVC[1])·s`

**Both equal `_P1/PVC[1] = 0.7928118393`**, because `H·s == _P1`. Neither yields the shipped 0.7453.

If the second `s` is spurious, every player value on the board is **5.99% low against every pick**.

## 3. WHAT THE E6 ACT ACTUALLY PROVED — relativity, not level

`session_2026-07-30/item279_step4/out/G5_four_scaling_controls.txt`:

```
both sides from one H (RULED)         GREEN   0/12 relativities moved
PICK SIDE ALONE (artifact scaled)     RED    12/12 relativities moved
PLAYER SIDE ALONE (SCALE only)        RED    12/12 relativities moved
DOUBLE application on players         RED    12/12 relativities moved
E6 live control: BOARD_FACTOR at s=0.977688 = 0.660451004 == 0.675524*s
```

The live control asserts the code multiplies by `s` — it verifies the code does what was INTENDED. It
does not test whether the intent is dimensionally right. And "0/12 relativities moved" is a statement
about RATIOS: scaling both sides by the same factor preserves every ratio **whatever the base level
is**. A level error of exactly `s` survives that control untouched.

**The script that produced those four lines is not in the tree** — only its output — so I cannot read
what its twelve relativities were. That is the single biggest gap in this investigation.

## 4. A TEST OF MINE THAT LOOKED DECISIVE AND IS CIRCULAR — reported so it is not repeated

I compared each pick's published price against the mean **v0** (entry price) of the men actually drafted
there, reasoning that a pick-1 player's entry price should equal what pick 1 costs.

```
mean ratio v0/curve over 18 picks   0.9881      (≈1.00 → shipped form is right)
the same divided by s               1.0510      (would be ≈1.00 if the second s were spurious)
```

That reads as a clean vindication of the shipped form. **It is worthless.** The shipped v0 lane (#306,
`RL_V0_LENS` default on) fits `value/anchor` ratios where `_anchor(pk)` **is the adopted curve**
(`_merged_recover.py:2321`), and it enforces LOCAL NEUTRALITY at every pick to `_LA_TOL = 0.005`. So
`v0(pk)/curve(pk) ≈ 1` is imposed by construction, per pick. The test recovers the constraint, not the
economy. **Discarded — it is not evidence either way.**

## 5. WHAT I COULD NOT SETTLE, AND WHY

Every downstream surface I can reach is anchored on the same construction, so it cannot referee it:
v0 is neutrality-locked to the curve; club ratings sum both sides without an external check; the no-arb
tables measure a pick's price against its own returns over time, not against the player scale.

**The player↔pick LEVEL may not be decidable from inside the model.** "A player worth pick 1" needs a
definition, and the only two available disagree by exactly `s`: the v3.4 kernel says 3784 in player
money; the adopted ladder says 3000 published, 3191 raw, in structural-VOR money. Which one defines the
unit is a RULING, not a measurement.

## What would settle it

1. **The E6 control script** — if it exists off-tree, what its twelve relativities were, and whether any
   spanned a player and a pick.
2. **The owner's own reading**: when the board says a player is worth 2,820 and pick 1 is priced 3,000,
   is that the same claim as "this player is worth slightly less than pick 1"? If yes, the shipped form
   is right and my §2 is wrong about which head defines the unit. If those two are meant to be the same
   number, the second `s` is spurious.

## Stakes

If spurious: every player is **6% cheap against every pick**, which touches every player-for-pick trade
and every club rating (56 assets, both kinds). It would be a level error, not a shape error — no
relativity among players moves, and no relativity among picks moves.

**No action taken. Nothing changed. This is for the owner's ruling.**
