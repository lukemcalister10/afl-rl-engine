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

---

# CORRECTION, same day: the missing instrument was found, and it tests the thing I said it did not

A background search finished after this note was filed and turned up a file I had not opened:
`session_2026-07-30/item279_step4/out/G5_s_invariance_instrument.txt`.

```
committed: s=0.977688  pooled head=3068.4647  ladder=54722
SINGLE application (ruled) relativities preserved: True   (0 of 12 moved)
DOUBLE application (bug)   relativities preserved: False  (12 of 12 moved)
     e.g. pick1/star: 0.428571 -> 0.438352  (x1.022822)
NON-VACUITY: instrument passes the correct case and FAILS the named failure mode: True
conservation s-invariance: 0.9998 -> 0.9998 (both sides rescale identically)
```

## What this changes

**§3 above is wrong on its central point.** I wrote that "0/12 relativities moved" was a statement
about ratios that "a level error of exactly `s` survives untouched", and that I could not tell whether
any of the twelve spanned a player and a pick. The instrument names one: **`pick1/star`** — a PICK over
a PLAYER. It is exactly the cross-side ratio I said was missing, and it is the worked example.

It also shows the instrument is NON-VACUOUS: it passes the ruled case and FAILS the named failure mode,
which is the discipline this estate applies to every check that matters. The failure mode it fails on is
called, in as many words, **"DOUBLE application (bug)"** — the very thing I was alleging.

## Where my algebra went wrong

I treated `_P1` as dimensionally carrying an `s`, on the grounds that a halt asserts `_P1 ==
published_pin == H·s`. That is a COHERENCE requirement between two pinned numbers, not a statement that
the symbol `_P1` is an s-scaled quantity in this expression. Operationally the two factors are:

* `_P1 / PVC[1]` — the BASE map, putting the v3.4 curve's pick 1 onto the owner's pin;
* `· s` — ONE application of the numéraire scale on the player side, matching the ONE the ladder takes
  when it is published as `raw · s`.

One per side. That is the "SINGLE application (ruled)" the instrument certifies, and it is why the
cross-side ratio holds still as `s` moves. Reading it as `s²` counts the ladder's own application
against the player side.

## What I still cannot close, stated smaller than before

The instrument proves **s-INVARIANCE** — that relativities do not move as `s` moves, both sides
rescaling identically, with a conservation quantity at 0.9998. It is a strong result and it is the one
the act needed. It does not, on its own, fix the LEVEL at a particular `s`; that still rests on which
curve defines "a player worth pick 1". But the burden has flipped: the construction is certified
coherent and non-vacuous by an instrument that fails when it should, and I have no measurement against
it — only a dimensional reading I have now shown to be mistaken.

**Standing recommendation: no action, and no re-anchoring.** My §2 claim of a 5.99% error should not be
relied on. If the anchor is ever revisited it should start from this instrument, not from this note.
