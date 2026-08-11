# H ladder — pre-registration, written BEFORE the emits

Three emits of the FULL package at `RL_C_H` = 1.20, 1.25, 1.30. `FULL@1.13` already exists as the
baseline (`c698b5b2`), so no identity re-proof is needed and none is claimed.

## The ordered expectation

> yr1 rises with H while yr4 stays ~1.531 (H touches the taught year-1 ceiling only); if yr4 moves
> materially under H, that is a wiring surprise — halt and report.

## The mechanism this expectation rests on, stated so it can be wrong

`RL_C_H` scales the ITEM C release: `_a_blend` multiplies the anchor by `1 + _c_w(...)·(C_H − 1)`.
`_a_blend` is called in `ev()` on the ITEM A arm, and **A's share fades hard with career evidence** —
measured on the verified synthetic at `item_a_verify.py`: share **v1 0.3589 → v6 0.0038**. By year 4
the A blend is nearly extinguished, so an anchor multiplier carried inside it has almost no purchase
there. That is *why* yr1 should move and yr4 should not.

**One honest caveat, registered in advance so a small yr4 move is not later dressed up as a
confirmation.** `_c_w` also enters the **ITEM E2 ruck cap** in `ev()`, which is *not* inside the A
blend and therefore does *not* fade with career evidence. E2 is position-scoped (RUCK only), so it
can leak a small, persistent, all-years effect. Therefore:

- a **tiny** yr4 move is mechanistically expected and is **not** a wiring surprise;
- a **large** yr4 move is, and halts the ladder.

## Pre-registered thresholds (ALL picks 1-64, canonical instrument)

| quantity | baseline `FULL@1.13` | pre-registered expectation |
|---|---|---|
| yr1 | 0.9974 | **rises monotonically** with H |
| yr4 | 1.5310 | **holds**: \|Δ\| ≤ 0.010 (≈0.65%) across the whole ladder |

- **HOLD** (expectation met): `|Δ yr4| ≤ 0.010` at every rung.
- **HALT** (wiring surprise): `|Δ yr4| > 0.010` at any rung — stop, do not read the ladder as a
  counterbalance result, report the mismatch.
- If yr1 does **not** rise monotonically with H, that is also a surprise and is reported as one.

## The no-arb bound the ladder is for

H raises yr1, so the yr0→yr1 appreciation **rises** and its margin against the **14%** charged to an
18-year-old **shrinks**. `FULL@1.13` sits at −0.26% appreciation vs a 14.00% charge. The crossing
point — the H at which yr0→yr1 appreciation exceeds 14% — **bounds lawful H**, and finding it is the
point of the exercise. It is reported as a bound, **not** tuned to.

## Reported per rung

yr0-5 ladder · young/peak contrast vs main · no-arb at yr0→yr1 and yr1→peak · peak/yr0 and peak/yr1
envelope columns · **and the 1-20 / 21-64 pick-band split**, since the young cut concentrated in
21-64 (−11.74% vs −7.90%) and C's releases are evidence-weighted — the sitting should see whether
H's restoration lands where the cut actually fell.

**Nothing is tuned toward any of this.** The envelope and the no-arb frame are frames for judging,
not targets. Sizing remains the owner's word.
