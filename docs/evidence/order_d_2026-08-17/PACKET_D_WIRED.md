# ORDER D — WIRED (the owner's word: the measured pick-curve fade). THE LANDING CANDIDATE.

**Plain language. Board `1f176444`, total 667,916** (repaired C32: 667,398 · Candidate 31:
666,913 · live: 752,429). Built twice, byte-identical. With the new switch off (`RL_O35`), the
board is byte-for-byte the repaired C32 (`7802ee97`). Matrix `per_entrant_O35FINAL.json`
(`e029bc9f`).

## 1 · What was wired

One curve, exactly as measured and as the owner ruled: the sitter fade's per-year cost now
scales with the pick-signal — **fade exponent κ = 0.50 at pick 1, 0.67 at 10, 0.85 at 20, 0.96
at 30, 1.03 at 40, 1.09 at 50, 1.15 at 64** — smooth in log(pick), never a band step, clipped to
[0.5, 2.0]. Pool and pickless rows evaluate the curve at the standing effective-pick convention
(the flat 64 end — disclosed extrapolation). The redistribution identity holds: the AVERAGE fade
across the sitter population is still exactly the ruled row — the curve moves fade between
picks, it does not change the total. Rows the fade does not reach cannot move (1^κ = 1).

## 2 · The named rows (the owner asked for smillie first)

| player | pick | live | C31 | C32R | **Order D** | pick-fade leg |
|---|---|---:|---:|---:|---:|---:|
| **josh-smillie** | 7 | 953 | 459 | 459 | **772** | **+313 — inside the flagged ~700–770 arithmetic** |
| lachlan-carmichael | 21 | 548 | 453 | 453 | **487** | +34 |
| william-mccabe | 19 | 599 | 316 | 385 | **410** | +25 |
| will-green | 16 | 604 | 338 | 408 | **483** | +75 |
| alex-dodson | 53 | 274 | 175 | 178 | **171** | −7 |
| charlie-west | 50 | 692 | 330 | 384 | **381** | −3 |
| phoenix-gothard | 12 | 1891 | 1012 | 1327 | **1327** | 0 (no fade reaches him — delivered) |
| billy-wilson | 34 | 983 | 547 | 675 | **675** | 0 (same) |

Exactly the ruled shape: high-pick sitters (smillie, green, mccabe, carmichael) are no longer
fully charged for what history says is mostly managed time; late-pick sitters (dodson, west)
fade slightly deeper; delivered players are untouched.

## 3 · The economics tables (before = repaired C32, after = Order D)

Year-one appreciation per band, two-sided (fair = between 0% and +14%):

| band | C32R | **Order D** | verdicts |
|---|---:|---:|---|
| picks 1-10 | +6.1% | **+7.9%** | ok — **6.1 points of headroom to the 14% line** |
| picks 11-20 | +7.4% | **+9.2%** | ok (4.8 points headroom) |
| picks 21-30 | +1.6% | **+2.8%** | ok |
| picks 31-40 | −12.9% | **−12.8%** | sell-side red — unchanged (its residual is the fade-signal question already filed) |
| picks 41-64 | −6.1% | **−7.9%** | sell-side red — widens ~1.7 points (late fades deepen, the ruled trade) |

Year-1 class aggregate: **1.042** (was 1.040) — essentially unchanged, as the redistribution
identity promises. Hard 1.14 line: max class 1.1311 — PASS, cooler than ever. Pool arms: RD
−2.2% (a mild new red as its effective-pick fade deepens — reported), SSP +50.5% buy-red and
the thin arms' sell-reds stand as the already-filed refit questions (R-REFIT owns them).

## 4 · The acceptance record

Dial-off byte-exact `7802ee97` · determinism ×2 · day-0 identity 89/89 at tolerance 0 (all 89
deep-sitter prints MOVE by the ruling's own design — smillie's rise IS the ruling working; the
89 entry objects/v0 are bit-identical to Candidate 31's) · continuity (incl. the at-bar gate and
the Carmichael one-game case, jump +24%) PASS · completeness PASS · reconciliation 804/804 ·
coverage 100% · S4 mid-career recovery **+45% median** (all six years-4–6 cells +34% to +53%,
every years-1–3 win retained) · κ-curve asserts (smooth, monotone, clipped, transcription
pinned to `O35_CURVE.json`) build-failing and passing · vantage matrix diagnostic-only,
refreshed in `NOARB_D_out.txt` · numeraire untouched.

**One owed number, said plainly:** the corrected-surface production-weight W reads 0.308
against its band floor 0.312 — a hair outside. The pick fade returns pedigree value to early-
pick sitters, which nudges the measured production weight down 0.018. The fade was justified by
the L3 fit alone (nothing was tuned to W); re-balancing the re-mix constants after Order D was
not in this order's scope and would re-open the repair calibration. Filed as a note for the
landing word, not adjusted away.

## 5 · Files

`PREREG_D.md` (+AD1, the owner's word) · `O35_CURVE.json` / `O35_VALUE_CONTRAST.json` (the
measurement) · engine: `RL_O35` block in `_merged_recover.py` · `W2_D_*` · `RESULTS_S4_D.json` /
`S4_D_RECOVERY.json` · `NOARB_D{.json,_out.txt}` · `DAY0_32_FINAL.json` (Order-D board) ·
`docs/ledgers/CANDIDATE_32_MOVERS.{json,md}` (live / C31 / C32R / Order-D + seven legs) ·
`PREVIEW_32_PLAYERS.html` / `PREVIEW_32_YEAR1.html` (the landing candidate pages).

*— Order A seat, Order D wired. The owner's landing word decides.*
