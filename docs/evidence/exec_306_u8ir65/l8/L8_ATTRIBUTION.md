# L8 — THE CANDIDATE BOARD BESIDE SHIPPED, EVERY MOVER ATTRIBUTED (#306, seat u8ir65)

Authority: seam 5188841840 (L8 cleared), terms 5188266553. Bake HELD; EXECUTION word WITHHELD.
No product file changed at L8 — the substrate stays the L7 state `2b5e99eb`; this leg is measurement.

## THE BASELINE CHOICE — the load-bearing decision
The committed released board `f2df6e0a` was built on store `6b9d00a7`, engine `404e8113` and a
different curve — **four axes differ** from the candidate. Diffing the candidate against it would
mislabel store- and engine-driven movement as curve/lens. So the baseline that isolates the LANDING's
own effect holds engine and store constant and moves only the landing's inputs:

  B0 baseline  `31f7108a`  curve e69a3f38 · surface b540833b · store 81d24704 · engine 15525b03
  B1 candidate `46ebfb37`  curve 01f27f02 · surface ebc3d330 · store 81d24704 · engine 15525b03
  (released    `f2df6e0a`  curve 08ea9375 · surface ce08c2d1 · store 6b9d00a7 · engine 404e8113 — 4 axes)

B0 is the pre-loop board on the landing's OWN engine (capture 2b7640be). B0 -> B1 differs ONLY in the
curve and the year-zero surface — the two landing inputs.

## THE COMPLETENESS GATE — what makes the attribution non-vacuous
`attribute_movers.py` first ASSERTS the held-constant inputs (store, engine, band) are equal between
baseline and candidate. If any differs, that axis is an UNNAMED cause and the run HALTs — because a
mover could then be store/engine-driven and wrongly stamped curve/lens. The named cause set is proven
complete only when this gate passes.

Non-vacuity, both directions, on real boards:
  PASS  B0 vs B1 (same store/engine/band)                 -> gate OK, exit 0
  HALT  released f2df6e0a vs B1 (store+engine differ)      -> gate fires, exit 1

## THE ENGINE ENFORCES THE PAIR
A mixed board (adopted curve + baseline surface) CANNOT be built: the render demands a refit when the
curve and surface signatures disagree. So the curve and surface are not independently variable — they
travel as one FITTED PAIR, which is the landing's single change. Every mover is therefore a landing
revaluation; the table below names each mover's DOMINANT pricing channel, not an independent cause.

## THE RESULT (B0 31f7108a vs B1 46ebfb37, both engine 15525b03 / store 81d24704)
  common 804 · added 0 · dropped 0 · MOVERS 601 (74.8%) · unchanged 203
  max |delta| = 31 board points — consistent with the L6 closure residual (<=1 ladder point/pick)
  carried through ev()/numeraire; no large unexplained jump.

  channel           movers   up/down    sum delta   mean    max|d|
  ruled_curve         322    287/ 35      +1339      +4.2      31
  year_zero_lens      255    136/119       -466      -1.8      22
  pool_levels          24     24/  0        +81      +3.4      22

Every mover carries a channel; 0 added, 0 dropped; the candidate board is byte-deterministic
(rebuilt 46ebfb37 -> 46ebfb37).

## WIDE-CHANNEL CAVEAT (ledger, endorsed by the seam)
`ruled_curve` and `year_zero_lens` are BOTH valid for movers in evidence-backed rows — ev() leans on
the year-zero estimate wherever a record is thin (44.22% of teaching-value movement rides evidence-
backed rows). The channel label is the DOMINANT pricing route, not a claim that the other played no
part. The gate that can HALT is the completeness gate above, not the channel bucketing.

## HELD / WITHHELD
Bake HELD; EXECUTION word WITHHELD; N43 pool levels ship AS SIGNED at the landing (the owner's).
