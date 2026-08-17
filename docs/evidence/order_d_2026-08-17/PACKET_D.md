# ORDER D — THE PICK-CURVE SITTER FADE: **HALT AND REPORT** (nothing wired)

**Plain language, for the owner directly.** The ruling R-PICKFADE was adopted on this rationale:
a high pick who is not playing is a bigger alarm than a late pick who is not playing, so the
sitter fade should deepen for early picks, as a smooth curve. We built the measurement to size
that curve — and the measurement, run three ways, does not support the ruled direction. Wiring
the ruled direction would mean writing a curve the data rejects; wiring the measured direction
would invert an explicit ruling. So per the standing law we stopped, wired NOTHING (the repaired
Candidate 32 board `7802ee97` stands untouched, all identities intact), and this packet brings
you the numbers and the exact question.

## 1 · What the three measurements say

**(a) The washout-odds curve (the prereg'd primary fit).** How much a year-one sit raises the
odds of a five-year washout, as a smooth line in log(pick), fitted player-by-player (ND
2005–2020; 408 sitters vs 213 played-11+ controls):

> sit-penalty(pick) = 0.13 + 0.45·ln(pick) — **it RISES with pick number.**
> 93% of 1,000 bootstrap draws say the slope is positive (the ruled direction needs it negative).

Read plainly: a late pick's sit-year is MORE informative about washing out, not less. The
band table that motivated the ruling (risk 3.7× at 11-20 vs 1.5× at 41-64) was a ratio of
probabilities — and ratios compress when the base rate is already high (59% of late-pick
non-sitters wash out anyway). On the odds scale the compression disappears and the trend flips.

**(b) The value scale — the decisive one, because the fade multiplies the entry price.** How
much of his entry-relative forward value a sitter keeps, versus a same-pick player who played
11+ games (F = 1 would mean sitting costs nothing):

| band | F (sitter keeps) | 90% CI | sitters |
|---|---:|---|---:|
| picks 1-10 | **0.535** | [0.31, 0.80] | 17 |
| picks 11-20 | 0.390 | [0.18, 0.65] | 37 |
| picks 21-30 | **0.128** | [0.06, 0.25] | 50 |
| picks 31-40 | 0.269 | [0.13, 0.61] | 82 |
| picks 41-64 | 0.310 | [0.17, 0.58] | 222 |

**Top-10 sitters keep the MOST of their entry-relative value, and the 1-10 vs 21-30 intervals
do not even overlap.** The shape is a trough in the 20s-30s, not a slide from pick 1 down.

**(c) The original band table** (risk multipliers 1.1 / 3.7 / 2.6 / 2.0 / 1.5): itself not
monotone — the top-10 cell is the LOWEST. Under every reading, the early end refuses the ruled
direction.

## 2 · Why the data may look this way (stated, not assumed)

A plausible mechanism, consistent with S2's injury findings: an early pick who does not play is
often a MANAGED asset (injury, development plans, ready-made roster ahead of him — smillie is
the live example), while a late pick who does not play has usually just lost the selection
contest. History cannot split injury from non-selection (S2 measured 0 of 7,212 historical
sit-seasons resolvable), so the pooled data carries the managed early-pick sitters inside it.
Your instinct about opportunity-and-investment may be right about the *unselected* early
sitter — but the wired fade cannot see the difference, and the pooled population it would
apply to measures the other way.

## 3 · What was built and stands ready (nothing wired)

The full machinery is committed and tested: the smooth curve family (no bands anywhere), the
clip bounds, and the redistribution identity that keeps the AVERAGE fade exactly the ruled row
(solved and asserted to 1e-6 at the ruled depth-2 cell — the curve only moves value between
picks). If you rule a direction, the wire is one constant swap away. The two live options, with
smillie (pick 7 sitter, today 459) and carmichael (pick 21, today 453) as arithmetic:

- **Your ruled direction** (early deepen — requires overriding the measurement): smillie falls
  toward ~270–330; carmichael roughly flat; late-pick sitters rise; the late sell-reds narrow.
- **The measured direction** (early soften, late deepen — requires overriding the ruling's
  rationale): smillie RISES toward ~700–770 (his sit reads as managed-elite, not failure);
  carmichael +30-ish; late-pick sitters fade slightly deeper, which would WIDEN the late-band
  sell-reds the repair just narrowed.

Neither was wired. The prereg's own named prediction (PD1: smillie deepens) is breached by the
measurement, and that breach is precisely the finding.

## 4 · The question for the owner (one sentence)

When you say a high pick sitting is "a bigger signal of problems": should the fade follow the
measured pooled history above (top-10 sitters have mostly been managed assets who kept their
value), or do you want the ruled direction anyway — knowing the data says the pooled top-10
sitter is the safest sitter on the board — or do you want this whole question parked until a
historical injury/availability table exists (S2 named that as the single biggest data gap, and
it is exactly the split this ruling needs)?

## 5 · State of the world (unchanged)

Board: the repaired Candidate 32, `7802ee97`, total 667,398 — untouched by this order. No
RL_O35 code exists in the engine. All identities, the day-0 prints, the five-band tables, the
class number (1.040) and the named rows stand exactly as the repair packet reported them.
Files here: `PREREG_D.md` · `o35_fit_curve.py` → `O35_CURVE.json` (the fitted curve + the
identity constant) · `o35_value_contrast.py` → `O35_VALUE_CONTRAST.json` (the decisive value
table). *— Order A seat, Order D leg. Halted per the standing law; the owner's word decides.*
