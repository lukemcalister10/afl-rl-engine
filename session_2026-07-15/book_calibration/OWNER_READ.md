# OWNER READ — Walk-forward book calibration (one page)

Priced vs realised, by cohort, on the sealed base book (`9be07b8e`, N=2649). Measurement only — no cure
proposals. Under-priced = the book pays you less than your realised output warrants.

## What the numbers SUPPORT

**1. The top-output compression is real (your English/Briggs read, item 131).**
Across the whole book, price rewards realised output **sub-proportionally**. Age-neutral peak map:
price grows as output^**0.36** (n=598, CI [0.32, 0.41]) — double the output, only ~1.28× the price.
Among proven players (27+), the elasticity is **0.68** (CI excludes 1). English vs Briggs directly:
English is **5.8× more above replacement right now** (28.2 vs 4.9) yet priced **1.56×** (3402 vs 2182).
The top is under-rewarded at the margin — as measured fact, not a read.

**2. The mid-round pick trough is real, RUC-severe, and untouched by the trio (item 132).**
`iso_corr` is a permanent, evidence-blind pick multiplier. For rucks it docks **picks 19–33 by −10 to
−19 %** while pick-34 escapes at 1.000 and pick-1 gets +6.9 % — a *better* pick, a *worse* forever-tax.
English carries **−11.5 %** for pick-19; Grundy −18 % for pick-22; Gawn −18 % for pick-33. The trio
store reprice changed none of it (it is a position×pick function). **What remains is the entire table.**
38 genuine contributors sit in the trough. Other positions have only a shallow late-20s dip; **the bite
is on rucks** — which is why it landed on English.

**3. Young star-track is already under-priced vs realisation — so a net-cut is wrong-direction (item 130).**
Players who went on to produce were priced, when young, **below** what their realised peak implies —
~1.4× under for top picks, up to ~7.7× under for late picks (the convex upside is under-weighted, more so
the lower the pick: Gulden pick-34, Newcombe pick-90). This is by-design under your cohort guard, and it
is a **baseline to score cures against, not a call to lift**: because the young side is already
under-priced on realisation, **stripping it fails as measured law.**

## What the numbers do NOT support

- **They do not say English's price is "low for the league."** His 3402 is *high* versus a random 27+
  player. The mispricing lives in the **shape of the reward curve** (compression) and the **pick tax**
  (iso), not in his absolute price level. A cure has to un-compress the top and fade the pick tax — not
  raise a cohort's baseline. (This is why the population signed-mispricing surface reads English as
  `over`, and why that surface is the *backdrop*, not the verdict on your pair.)
- **They do not license a young-side lever.** Young is under-priced on realisation; the instrument's job
  is to flag if a cure *widens the young gap or eats guard headroom*, nothing more.
- **They do not resolve fine cohorts.** Only 300 current contributors; past position×age×pick, cells go
  thin and are withheld (declared). The robust findings are the three axes above; cohort-specific
  price-level anomalies are mostly not distinguishable from fair.
- **They are not bit-exact to the seal.** The regenerated book matches the seal on N and every identity
  stamp and reproduces the canonical board **99.6 % exact** (≤4-SCAR cross-runner float drift on 0.4 %
  of cells); the calibration is smoothed well above that noise.

## The one-line handoff to the PVC spec
The proven-side gap (English/Briggs) is **compression + an evidence-blind RUC pick tax**, both on the
proven axis; the young side is already under-priced on realisation. A spec that lifts the compressed top
and fades the pick tax moves the defect where it lives; a spec that cuts the young side moves value away
from the side the walk-forward shows is already short.
