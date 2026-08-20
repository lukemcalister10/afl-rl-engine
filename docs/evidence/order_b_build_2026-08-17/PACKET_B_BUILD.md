# PACKET — ORDER B BUILD (the veteran fixes, RL_O33)

**Nothing lands on this packet.** The build rides the repaired Candidate 32 and LANDS ONLY AFTER it
lands and is ruled — two packets, two reviews (owner sequencing, #334 c.5314553763). Authority:
c.5312733761 (commission) · c.5314553763 (rulings B-1/B-2/B-3) · PACKET_B_DERIVATION.md. Prereg
`PREREG_B_BUILD.md` pushed before any engine edit (a6c6ec3). Everything is behind **RL_O33, default
OFF**; with the dial off the current tree's boards reproduce **byte-exact** (asserted after every
rebase; the repair seat moved the base under this build twice and the identities were re-run each
time — final asserts at base 3e40344: default board `bce0c65d`, RL_O32=1 board `7802ee97`; re-proven once more
at the delivery HEAD 31b79a7 after the Order C seat's eff2044 landed under this build — all three
boards byte-identical: bce0c65d / 7802ee97 / candidate b786141a).

Plain-language glossary, used throughout: a row's **mark** is its board price. **Output surplus** is
how far a player's demonstrated scoring level sits above his position's replacement level. The
**anchored B** instrument says how a group's marks compare with the value those players actually
delivered afterwards (B > 1 = over-marked, 1 = right). A **leg** is the real board delta one
mechanism contributes.

## 0. The headline, honestly

Three ruled mechanisms are wired. Two behave exactly as ruled. The third — the output-conditional
terminal fade — **could not be identified on these samples, twice, and the build therefore wires the
ruled FALLBACK (the flat hazard knots)**. The consequence the owner must see before any landing word:
the fallback is flat in output, so validated star veterans take the same 29+ terminal cut as fringe
veterans — Bontempelli −238, Sinclair −236, Merrett −146 on the fade leg — which is precisely the
behaviour his B-2 question ("are all 31-year-olds equal?") pushed against. The identification failure
is genuine, shown in section 2, and the un-closable part of the veteran terminal gap is located in a
channel no discount schedule can reach (the exit-hazard weighting of the current season itself,
already named by the derivation for a future order). If the owner prefers no fade to a flat fade,
stage 1+3 without stage 2 is a one-word dial position (`RL_O33_STAGE=1` plus taper; every leg is
separately built and measured below).

**Boards** (all totals in board points): live 752,429 · Candidate 31 666,913 · C32-base (the repair,
7802ee97) 667,398 · **B-preview (b786141a) 680,932** = base −9,318 (ladder) −5,294 (fade) +28,146
(taper retirement). Determinism: full board built twice, identical md5. Day-0: **89/89 prints
byte-identical** (the emitter's fail-closed guard, run against the repair board's own published
day-0 file). Boot/numeraire guards green on every build.

## 1. B-1 — the anchored tall ladder (wired as ruled)

- The fitted KPD/KPF post-peak ladder is pinned exactly as adopted: decline 3.0%/yr at 28 growing
  +2.5pp/yr → fractions-of-peak **0.970 / 0.917 / 0.843 / 0.755 / 0.657** at ages 28–32, family
  continued beyond (the projection loop's own 0.42 floor bounds the tail). Pre-peak DELTAS and the
  27/27 peak ages untouched. **RUCK keeps its current curve** (derivation KEEP; the built board's
  RUCK B cells stay 0.96–1.05, none called).
- The **anchor-preserving renorm s\*** was derived at build time as a fixed point on the engine's own
  boards: s\* = **1.2988** conserves the aggregate board value of the 55 tall rows aged 23–26 to
  **−0.06%** (gate ±3%; iteration log `SSTAR_DERIVE_out.txt`). It multiplies the tall projection
  stream only — the demonstrated floor is not renormed (a flat ×1.30 on every tall floor is not what
  the prime-anchor evidence licenses; disclosed choice).
- **The one piece of engine plumbing this exposed, disclosed loudly:** the engine's price scale is
  anchored at load time to the 99th percentile of raw production and to the pre-anchor pick-curve
  head. With the dial live during load, the ladder moved that basis and **lifted every non-tall row
  ~+6.4%** — a re-denomination of the whole board by a veteran fix. The basis section now runs with
  the dial forced off (one extra pass), so dial-on and dial-off boards share one currency. Measured
  before/after in `QUICKLOOK_out.txt` / commit history; the numeraire s itself never moved.
- **Verification:** rank-ordering among 27+ rows preserved — Spearman(base, B-preview) = **0.9921**
  (all 27+ rows) and **0.9859** (tall 27+; gate ≥ 0.95); max rank move 148 places, mean 21.3 (the
  named veteran talls fall many places by design — the order WITHIN the veteran cohort holds).
  No age cliff: the fixed-level sweep of the board-value object (ENGINE_CHECKS_B.json) shows a
  smooth, monotone on/off ratio path — the annual steps are the fitted ladder's own escalating
  rates, and there is no jump anywhere resembling the rejected age-27 switch.

## 2. B-2 — the terminal fade: THE CONDITIONAL FIT FAILED IDENTIFICATION; THE RULED FALLBACK IS WIRED

The owner withdrew the universal knob and ordered an output-conditional fade, with the flat 25%
hazard variant as FALLBACK ONLY if the conditional fit fails identification. It failed. Twice.

**Attempt 1 — the prereg'd fit** (family r(a,s) = 0.14 + A·φ(age)·exp(−surplus/s0), survivor-view
tier×age LEVEL cells as the loss, W5 CIs as weights, full-view over-correction floors;
`RESULTS_B_FADE_FIT.json`): the loss surface is flat — best point A=0.02 (essentially zero fade),
bootstrap **A CI [0.00, 0.60]** (does not exclude 0), **G(star) CI [0.00, 0.77]** (not below the 0.5
bar). Cause, visible in the cells: the survivor level cells mix directions (mid 29 B=0.77 and role 30
B=0.57 sit UNDER par while role 28–29 sit over), so no monotone fade improves that loss.

**Attempt 2 — the disclosed rescue** (same family, surplus, grids, floors, identification rule and
star gate; the loss moved to the tier-resolved RATE instrument after the diagnosis showed the signal
lives there; `RESULTS_B_FADE_DIAG.json`, `RESULTS_B_FADE_FIT2.json`): the diagnosis is striking and
worth the owner's eye — **star veterans' engine step declines match realized at every age** (gaps
+0.006…+0.067, never called) while **mid/role veterans' engine steps are far too shallow** (role
called at 28→29 +0.40, 29→30 +0.56, 30→31 +1.90). The fit then identifies that a fade exists
(**A CI [0.14, 0.60]**, excludes 0) but CANNOT identify output-conditionality: s0 runs to the top of
its grid (CI [8, 64]), **G(star) = 0.71, CI [0.12, 0.77]** — the family goes near-flat trying to
close mid/role gaps that no discount rate can reach (a role 29→30 realized step of 0.15 cannot be
priced by any per-annum discount; the family exhausts at the level floors), and the near-flat fit
breaks the star gate (star 30 shifts −0.069 > 0.05). Per the prereg'd decision rule: **FALLBACK**.

**What is wired** (stage 2): the hazard-arithmetic knots — the per-annum balanced-lens discount rises
from 0.14 by the measured excess exit hazard: **28: 0.14 · 29: 0.211 · 30: 0.232 · 31+: 0.246**,
piecewise-linear in continuous age, zero rows below 28 move, output-flat. The fitted-34% boundary
value is dead as ruled and appears nowhere.

**The star-preservation evidence, side by side** (W5 harness re-run, byte-carried ruler, on the
built matrix vs the C32R control matrix — `W5_COMPARE_out.txt`):

| tier/pos, survivor B | 27 | 28 | 29 | 30 | 31 |
|---|---|---|---|---|---|
| TALL — control | 1.20 | 1.27 | 1.32 | 1.65 | 1.40 |
| **TALL — built** | **1.01** | **0.93** | **0.83** | **1.00** | **0.83** |
| (called?) | no | no | no | no | no |
| STAR — control | 0.95 | 0.96 | 1.03 | 1.10 | 1.02 |
| **STAR — built** | **0.91** | **0.89** | **0.87** | **0.93** | **0.86** |
| (called?) | under\* | under\* | no | no | no |
| ROLE — control | 1.36 | 1.68 | 2.21 | 0.56 | 0.91 |
| **ROLE — built** | 1.35 | 1.60 | **1.91** | 0.47 | 0.71 |

\*The two marginal under-mark calls (star 27 CI-hi 0.994, star 28 CI-hi 0.9993) are **not the fade**
— the fade is zero at 27–28. They are the B-1 ladder acting on TALL stars (the adopted ladder is
itself output-blind) plus the renorm-lifted anchor. Stated plainly: **the called tall bias closes
completely (1.20–1.65 → 0.83–1.01, nothing called), at the cost of a broad ~0.1 downward drift of
every veteran group including stars — the price of two output-blind mechanisms.** The role-tier 29
over-mark improves (2.21 → 1.91) but survives — the un-closable remainder is the exit-hazard channel
(a role veteran's risk is leaving the game entirely, which discounts on FUTURE seasons cannot express
because his mark is mostly his undiscounted current season). That channel stays named for a future
order; nothing is smuggled in here.

## 3. B-3 — taper retirement (wired as ruled)

The v7 ascending age-taper on the q97 ceiling band is not applied at stage 3: band[5] stays
max(q97m, q90) exactly as emitted; the frozen q97m is untouched (bake-time refit per R-W6).
Measured on the 804 board rows (`ENGINE_CHECKS_B.json`): **ceiling inversions (band5 < band4)
407 → 0** — every ▼ dies by construction (the W6 count of 341 was the older matrix's count; this
board's own count is 407, and it goes to zero the same way). 646 rows get ceiling-band level back
(+5,290 level points); the **price effect through the 0.10 WQ6 weight is the taper leg: +28,146
board points** (derivation preview said ~+30,224 — same object, the engine's own arithmetic). Biggest
single-row taper risers: T.De Koning +196, S.Ryan +171, Visentini +170, Bryan +173, Soligo +144.

## 4. The standing two-sided no-arb suite (instruments carried, pins printed at run)

Five ND bands, yr0→1 appreciation vs the 14% carry (`STANDING_TABLES_B_out.txt`, control = the
repair seat's O32RFINAL matrix):

| band | control apr0→1 | B-build apr0→1 | verdict |
|---|---|---|---|
| picks 1-10 | +6.1% | +6.3% | ok both sides |
| picks 11-20 | +7.4% | +7.7% | ok |
| picks 21-30 | +1.6% | +2.0% | ok |
| picks 31-40 | −12.9% | −12.1% | SELL-RED — inherited from the base, slightly improved |
| picks 41-64 | −6.1% | −4.3% | SELL-RED — inherited, improved |

No buy-side red anywhere (max +7.7% vs the 14% line). The two sell-reds are the repair packet's own
owned standing residuals; Order B improves both and introduces none. Pool arms: no new red; SSP's
standing +53%/+60% yr0→1 (its own named investigation) rises to +60% under the taper — same
attribution as below. Vantage-consistency matrix printed in full in the evidence file; the V1
(year-1-vantage) band spread widens 18.7 → 23.6 pts (k=4) because the taper lifts late-band ceilings
— reported, not averaged away.

**THE ENTRY-YEAR CONTROL — the build's cleanest control, asserted explicitly:** every band and arm
year-0 cell moves **0.00%** (v0 untouched by construction). Year-1 cells: 21 of 26 inside the
prereg'd ±1.5%; five breach it (picks 41-64 +1.9%, RD +2.7%, ALLPOOL +2.7%, SSP +4.4%, UNR +5.2%).
**Attribution is exact** (`ENTRY_ATTRIB_out.txt`): re-read on the stage-2 matrix (no taper) every one
of those cells sits within ±0.75% — the breaches are 100% the B-3 taper-retirement leg lifting
MATURE-AGE year-1 entrants' ceilings (UNR/SSP recruits enter at 22–27, where the old taper bit
hardest), zero the veteran mechanisms. Halt-and-report satisfied: reported, attributed to a ruled
mechanism, not cured away.

## 5. Numeraire

**s does not move.** The artifact (pvc_curve_v2.json) is byte-identical to Candidate 31's
(md5 78ad9842…), s = 0.9400914291… re-asserted by `_load_numeraire` on every build; the NUMÉRAIRE
GUARD line is green in every export log. The one place the dial could have re-denominated the board
(the load-time P99/PVC-head basis) is frozen to the dial-off basis by construction (section 1). The
candidate remains PRE-NUMERAIRE exactly as its base is.

## 6. Movers ledger and pages

`docs/ledgers/ORDER_B_MOVERS.json` (+ evidence copy `LEDGER_B.json`): all 804 rows, Live · C31 ·
C32-base · B-preview, the three mechanism legs per row (their sum is Δ vs base exactly), deltas vs
all three references. Pages refreshed in the standing formats: `PREVIEW_B_PLAYERS.html` (full board,
sortable, legs inline) and `PREVIEW_B_YEAR1.html` (draft order; **85 of 120 year-1 rows unchanged**;
the 35 movers are the taper leg plus 17 year-1 TALL rows carrying the disclosed W-A young-tall
renorm reach; the fade reaches no year-1 row).

**Named rows** (Δ = B-preview vs C32-base; legs ladder/fade/taper):

| row | pos/age | base | B-prev | Δ | legs | note |
|---|---|---|---|---|---|---|
| Wilkie | KPD 30 | 3,422 | 1,938 | **−1,484** | −1447/−70/+33 | the W5 poster row |
| Wright | KPF 30 | 1,531 | 950 | −581 | −568/−23/+10 | |
| Andrews | KPD 30 | 1,521 | 919 | −602 | −587/−28/+13 | |
| Battle | KPD 28 | 1,879 | 1,311 | −568 | −623/0/+55 | |
| McKay | KPF 29 | 1,636 | 1,005 | −631 | −641/−19/+29 | preview predicted UP; the real engine resolves the ln>pn subsidy DOWN — prediction miss, owned |
| Curnow | KPF 29 | 1,297 | 810 | −487 | −500/−15/+28 | |
| Moyle | RUCK 24 | 1,645 | 1,774 | +129 | 0/+1/+128 | taper only |
| McAndrew | RUCK 26 | 897 | 1,010 | +113 | 0/0/+113 | taper only |
| S.De Koning | KPD 25 | 861 | 924 | +63 | −26/0/+89 | |
| T.De Koning | RUCK 27 | 1,688 | 1,887 | +199 | 0/+3/+196 | biggest taper riser |
| Bontempelli | MID 31 | 3,677 | 3,469 | −208 | 0/−238/+30 | STAR EXHIBIT — the fallback's flat cut |
| Sinclair | SD 31 | 3,180 | 2,972 | −208 | 0/−236/+28 | STAR EXHIBIT — same |
| Merrett | MID 31 | 2,542 | 2,400 | −142 | 0/−146/+4 | STAR EXHIBIT — same |

## 7. Prereg scorecard

Direction predictions: **8 of 13 named rows correct** (Wilkie, Andrews, Battle, Curnow, Moyle,
McAndrew, both De Konings, T. via taper). Misses, owned: McKay (predicted UP off the preview's flat-
renorm subsidy; the full engine's floor/pedigree resolution takes him DOWN −631) and Wright (down
far more than "small"); the three star exhibits were predicted ~unmoved **under the conditional
fade** — the fallback replaced it, and they move −4…−7%. Cohort predictions: tall 28–30 cut ✓
(−35% aggregate); young talls ≤24 rise ✓ but smaller than the preview (+1.2% vs +4.2% — the frozen
scale basis removes the preview's hidden global lift); entry year ~unmoved ✓ with the taper
attribution; totals dominated by the taper ✓. Prereg deviations, all disclosed above: (1) the
fade-fit loss moved to the rate instrument after the prereg'd level-cell loss was shown structurally
unidentifiable — both fits published, the decision rule (identification bar, star gate, fallback)
never changed, and the OUTCOME followed the rule: fallback; (2) floor scope at ages 28–31 with the
min(floor, zero-fade-level) clarification (matches the derivation's own feasible()); (3) the
pre-anchor basis freeze (section 1) — an identity-preserving guard, not a mechanism.

## 8. The landing dependency, restated

This build re-runs its full acceptance ON TOP OF the repaired Candidate 32 as landed (row overlap is
real: the taper lifts young talls inside Order A's constituency, and Order A's own suite must re-run
after Order B wires — the derivation's interaction note stands). The two seats' work was never
hand-merged: every rebase was clean or this seat would have halted; dial-off identity was re-proven
against each new base (cf443a6 → 3e40344).

## 9. Files

PREREG_B_BUILD.md · bb_fade_fit.py → RESULTS_B_FADE_FIT.json (failed, shown) · bb_fade_diag.py →
RESULTS_B_FADE_DIAG.json · bb_fade_fit2.py → RESULTS_B_FADE_FIT2.json (failed, shown) · bb33.sh
(builder) · SSTAR_DERIVE_out.txt · bb_ledger.py → LEDGER_B.json + docs/ledgers/ORDER_B_MOVERS.json ·
bb_engine_checks.py → ENGINE_CHECKS_B.json (taper + continuity) · run_emit_o33.sh →
per_entrant_O33B/O33L2 (scratch) · w5_rerun.py → RESULTS_W5_O32RFINAL/O33B.json + W5_COMPARE_out.txt ·
bb_noarb33.sh + bb_standing_tables.py → STANDING_TABLES_B.json/_out.txt · bb_entry_attrib.py →
ENTRY_ATTRIB.json · bb_pages.py → PREVIEW_B_PLAYERS.html / PREVIEW_B_YEAR1.html · this packet.
