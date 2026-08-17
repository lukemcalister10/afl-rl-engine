# PREREG_D — ORDER D: THE PICK-CURVE SITTER FADE (owner ruling R-PICKFADE)

**Pushed BEFORE any Order-D edit.** Authority: #334 comment 5316404479 — "the pick-dependent
sitter fade is a SMOOTH CURVE in pick, never band steps." Base: the repaired Candidate 32
(board `7802ee97`, matrix `f4300308`). Dial: **`RL_O35`**, implies `RL_O32`; dial-off must
reproduce `7802ee97` byte-exact. NOT stacked on RL_O34 (Order C shelved pending the owner's
word). Evidence: this directory. NOTHING LANDS WITHOUT THE OWNER'S WORD.

## The idea in plain words

Today one fade schedule charges every sitter the same, whatever his pick. The owner's ruling:
a high pick who cannot get on the field is a louder alarm (the club paid for him and hands him
opportunity), while a late pick's sitting is partly what his cheap price already said. Our L3
measurement agrees: a sit-year multiplies five-year washout risk about 3.7x for an 11-20 pick
but only 1.5x at 41-64. Order D turns that measured trend into a smooth curve and lets the
fade's per-year cost follow it — deeper for early picks, shallower for late ones — while the
AVERAGE fade across the sitter population stays exactly the ruled row (a redistribution, not a
re-litigation).

## D1 — the curve (family fixed here)

Individual-level logistic on the L3 population (ND entrants 2005–2020, five observable years,
washout = zero above-bar surplus in years 1–5, S1's SDV object):
`logit P(washout) = α + β·ln(pick) + s(pick)·SAT`, with `s(pick) = γ0 + γ1·ln(pick)` — the
log-odds cost of a year-one sit at pick p. Primary contrast: SAT (g1 = 0) vs the played-11+
control (the L3 headline contrast; the 1–10-game slivers are excluded from the primary fit and
carried in a secondary all-played spec, reported). Smooth and monotone in ln(pick) by
construction — no band ever enters. CIs: player bootstrap B = 1000, seed 35. Data support
disclosed per region (top-10 sitters are n = 17 — the early end of the curve leans on the
trend; said plainly in the packet).

## D2 — the wiring and the redistribution identity

The fade's per-year cost is −ln D. Order D scales it:
`D_eff(c_u, pick) = D(c_u) ^ κ(pick)`, `κ(p) = clip( s(p) / s_norm , 0.5 , 2.0 )`,
applied to the row's own schedule (the ND row for ND/RD/pickless via the standing
effective-pick conventions; the pool row for pool rows), BEFORE the selection relief
(which keeps its cap at full pedigree). κ is continuous in ln(pick): smooth in pick, no cliffs
in pick, games or age (asserted). Rows the fade does not reach (c_u ≤ 1, D = 1) are untouched:
1^κ = 1 — murdock-class rows cannot move.

**The identity (the ruling's "redistributes, does not re-litigate"):** s_norm is solved so that
the pick-weighted mean fade at the ruled row's home cell (depth 2) over the fitted sitter
population equals the ruled D(2) = 0.5583 exactly:
`mean over sitters[ D(2)^κ(pick_i) ] = D(2)`, asserted at build to 1e-6. One constant cannot
pin every depth at once with an exponent form; the depth-3/4 pooled deviations are REPORTED
beside the pinned depth-2 identity, never hidden. Effective picks past 64 (the pool index)
evaluate the curve at 64 — flat extension, disclosed as beyond-data; the clip bounds it.

## D3 — predictions

- **PD1 smillie (pick 7, sitter, c_u 2.92):** κ(7) > 1, his fade DEEPENS — price falls below
  459 (predicted band 320–430).
- **PD2 carmichael (pick 21, c_u 1.92):** κ(21) near 1 — small move, |Δ| < 8%.
- **PD3 the late/high contrast:** dodson (p53) and west (p50) RISE (κ < 1); mccabe (p19) and
  green (p16) FALL (κ > 1) — note both are HIGH picks despite being late-round names in the
  repair story.
- **PD4 five-band economics:** the late sell-reds NARROW (41-64 from −6.1% toward 0; 31-40 from
  −12.9% toward 0); picks 1-10 FALL from +6.1% but stay above 0 (deepened early fades lower
  early yr1 marks — the headroom is 6 points; if 1-10 crosses 0 that is a halt-and-report, not
  an adjustment). The class number moves little (most sitters are late picks and rise; the few
  early sitters are valuable and fall).
- **PD5 day-0, stated precisely:** the printed-day-0 IDENTITY stays 89/89 at tolerance 0
  against the Order-D law, and ENTRY-year prints (c_u ≤ 1 ⇒ D = 1) are byte-unmoved — but the
  CURRENT prints of deep sitters MOVE BY THE RULING'S OWN DESIGN (smillie's deepening is a
  named prediction of the ruling). "Unmoved" cannot bind the very rows the ruling re-prices;
  this reading is stated here, before the build, so the packet's numbers cannot be mistaken
  for a breach.
- **PD6** dial-off byte-exact `7802ee97`; determinism; S4 recovery stays positive (the fade
  deepening on early sitters may even help years 4–6); mature/at-bar continuity passes; the
  vantage matrix stays DIAGNOSTIC-ONLY (the curve is justified by the L3 fit alone — nothing
  is tuned toward any table).

## D4 — acceptance

The standing two-sided five-band + pool-arm suite with fair-mark benchmarks · the vantage
matrix (diagnostic) · W2 scorecard both surfaces · S4 rescore · day-0 identity + entry-print
invariance (PD5 reading) · determinism · dial identities · the ledger's continuity/completeness
/reconciliation gates · κ-curve asserts (monotone, clipped, identity). Halt-and-report on any
breach; nothing self-adjusts.

## D5 — deliverables

`PACKET_D.md` (plain language) · movers ledger with live / C31 / C32R / Order-D columns ·
both preview pages refreshed (the landing candidate if ruled in) · named rows: smillie,
carmichael, dean, duff-tytler, gothard, wilson, madden, busslinger, mccabe, green, dodson,
west, gallop, annand, murdock.

*— Order A seat, Order D leg, 2026-08-17. Committed before any Order-D edit.*
