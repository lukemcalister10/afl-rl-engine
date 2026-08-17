# CANDIDATE 32 — THE REPAIR PACKET (plain language)

This is the repair the owner ordered on top of the Candidate 32 build. Nothing lands without his
word. Everything sits behind the same switch (`RL_O32`); with the switch off, the board is still
byte-for-byte Candidate 31 (`fe6be9d6`), and the 89 draft-day prices are untouched.

**The repaired board: `7802ee97`, total 667,398** (Candidate 31: 666,913 · live: 752,429).
Built twice, identical. Draft-day prices: 89 of 89 exact and identical to Candidate 31's.
Continuity, completeness, price reconciliation: all pass. The walk-forward matrix is
`per_entrant_O32RFINAL.json` (`f4300308`).

---

## 1 · What was wrong, in one paragraph

The build's re-mix moved price weight onto "shown production" — but it judged a young player's
production against the bars a MATURE player must clear. S1 had already measured that those bars
fail 86–100% of age-18/19 seasons even for players who turn out fine. So the re-mix punished good
young players (dean and duff-tytler were the symptom), and the measuring stick itself (W2's
"poor starter" bucket) was polluted: when we re-cut it age-fairly, HALF of the 5–9-game "poor
starter" bucket changed membership. The repair makes every NEW mechanism read production
age-fairly, re-measures the target surface the same way, and re-fits the re-mix knobs on the
corrected surface — under the same hard gates as before (the 1.14 no-arb line, the slope band,
the corrected production-weight band, price curves that never dip for an at-bar player, and a
monotone reliability curve). One extra term was added to the law: the re-mix's added production
weight now credits a young player with the measured gap between his age's expectation and the
mature bar (the "age credit"). It is zero at zero games and zero from age 24, so draft-day prices
cannot move.

## 2 · The corrected class number, and where the points went

- The year-1 class now marks **1.040** (walk-forward mean, classes 2005–15). The fair level is
  about 1.10–1.12. So roughly **6–7 points of appreciation are still owed to the class** — but
  the owner rejected "uniform", and he was right. Judged against each cell's OWN fair level
  (fair = 1.14 × (1 − the share of value the cell delivers in year one)):

| pick band | n | mark | fair | gap |
|---|---:|---:|---:|---:|
| 1-10 | 170 | 1.054 | 1.120 | −0.067 |
| 11-20 | 170 | 1.097 | 1.111 | **−0.014 (at fair)** |
| 21-30 | 170 | 1.049 | 1.124 | −0.075 |
| **31-40** | 170 | 0.895 | 1.103 | **−0.208** |
| **41-64** | 399 | 0.945 | 1.107 | **−0.162** |

  By pathway: RD is at fair (−0.04). The thin development arms are far under (UNR −0.55,
  PDN −0.48, PDS −0.35, PDA −0.26, MSD −0.25) and SSP is far OVER (+0.72). By position group:
  RUCK −0.43 is the worst single cut. By age: 17-year-old draftees −0.26.
  **The missing value is concentrated: late pick bands, rucks, the youngest draftees, and the
  thin development arms. Band 11-20 needs nothing.** No uniform component is claimed, so no
  uniform lift is proposed. Full tables: `ATTRIBUTION_32R_out.txt`.

## 3 · The five-band, two-sided no-arb table (the standing gate)

A band is fairly priced if it appreciates between 0% and +14% in its first year. Above +14% you
could buy it and beat the carry (buy-side red); below 0% you could sell it and buy it back
cheaper (sell-side red).

| band | Candidate 31 | verdict | **repaired** | verdict |
|---|---:|---|---:|---|
| picks 1-10 | +16.2% | **buy-side RED** | **+6.1%** | ok |
| picks 11-20 | +12.0% | ok | +7.4% | ok |
| picks 21-30 | +3.7% | ok | +1.6% | ok |
| picks 31-40 | −12.4% | sell-side RED | **−12.9%** | **sell-side RED — survives** |
| picks 41-64 | −11.4% | sell-side RED | **−6.1%** | **sell-side RED — halved** |

Five-band spread: 28.6 points → **20.3 points** (diagnostic — reported, never targeted).
The early-band buy-side arbitrage Candidate 31 carried is CURED. The late-band depreciation
shrinks but survives — and §5 says why and what would close it.

Pool arms (same rules; PRIMARY window): SSP **+51.6% buy-side RED** (n=31, thin — bounded);
UNR −37.9%, PDN −30.5%, PDS −19.5%, PDA −10.4%, MSD −11.7% all sell-side RED; RD −0.5% and the
pooled all-pool path +3.1% are fine. MSD's year-1 cell: a mid-season draftee debuts the same year
he is drafted, but the matrix stores his seasons from the following year, so his true first
season cannot be read from this matrix — those rows are excluded from that one year and counted
(never zeroed, never a blank). Full tables both windows: `NOARB_32R_out.txt`.

## 4 · The vantage matrix (diagnostic only — nothing was tuned toward it)

From every standpoint year, a fairly priced band should be priced to grow near the carry
(1.14 per year). The full matrix (vantages 0/1/2, horizons 1–4, all bands and arms, carry
printed beside every row) is in `NOARB_32R_out.txt`. The headline: the year-1-vantage one-year
spread between bands narrowed from 0.097 (C31) to 0.065; the surviving divergence sits with the
late bands, and the leg attribution (using each band's own fair year-1 level) splits it cleanly:

- picks 31-40: year-1 mark 20 points TOO LOW (0.895 vs fair 1.103) — the year-1 leg carries it;
- picks 41-64: year-1 mark 16 points too low AND the year-1→5 growth still trails the carry —
  both legs;
- picks 1-10: the year-1 mark is now near fair (−0.067); its weak forward growth from year 1
  points at the LATER-year marks (the S4 mid-career residual), not the year-1 mark.

## 5 · The three investigation lanes (owner hypotheses — measured, not assumed)

**L1 — "is late-pick ENTRY value too low?" NOT SUPPORTED as posed.** S5's decomposition shows
the entry curve sits ~9% under raw delivered history at picks 11-30 (the smoothing stage flattens
the head) and only ~2-3% at 31-64. A too-low entry price would make year-1 appreciation look
BETTER, not worse — so the late-band depreciation is not an entry-price artifact. The picks-11-30
smoothing-head refit stays owed at the next v0 refit (rulings-material).

**L2 — "are the arm entry cells mispriced?" CONFIRMED for the thin arms.** Price-to-delivered
multiples (delivered career value ÷ entry price, arm-summed; ND is the reference at 0.51):
PDS 0.13, PDN 0.29, PDA 0.31, MSD 0.11 — **those arms' entry cells sit far above what their own
players ever delivered**, and the K-shrink borrowing is the located mechanism (S7's own ratios:
PDS/PDN/IRE delivered 0.27/0.59/0.73 of their signed cells). **SSP is the contrast case and needs
care**: its career multiple (0.21 on 13 players) cannot judge the arm — SSP is new and its
careers are unfinished, which drags that number down mechanically. The live SSP evidence is the
year-one lens: mark 1.62 against a fair 0.90 (the +51% buy-side red; 31 players, thin, bounded)
— the engine immediately re-prices mature-age SSP production far above cells that price
development-class entries. The owner's "entry too low" reading is supported on that lens and
untestable on the career lens; both statements travel to the refit. Candidate fix for the whole
lane: OWN-ARM RE-ANCHOR of the thin arms' entry cells at the next v0 refit — rulings-material, no
entry surface touched here. RD is career-fair at entry; its question belongs to the leg
attribution, not the entry cells.

**L3 — "is a year-one sit less meaningful for a late pick?" YES — material, the owner's
direction.** P(the player never delivers a single above-bar point in five years), by year-one
games and band, with the risk ratio of sitting vs playing 11+ games:

| band | sat (0g) | 1-4g | 5-10g | 11+g | risk ratio sat/11+ |
|---|---:|---:|---:|---:|---:|
| 1-10 | 18% | 25% | 36% | 15% | 1.1× |
| 11-20 | 62% | 46% | 48% | 17% | **3.7×** |
| 21-30 | 78% | 61% | 47% | 30% | 2.6× |
| 31-40 | 74% | 69% | 44% | 38% | 2.0× |
| 41-64 | 89% | 62% | 54% | 59% | **1.5×** |

A sit-year multiplies washout risk 3.7× for an 11-20 pick but only 1.5× for a 41-64 pick — the
signal weakens steadily down the draft, while sitting becomes three times more common (23% of
top-10 first-years sit or barely play; 76% of 41-64). **The one fade schedule the law applies to
every band therefore over-charges late-band sitters — and that is the best-evidenced closure for
the late-band residual in §2.** A band-dependent fade touches the owner's earlier band rulings:
rulings-material, reported with these tables, wired nowhere. (The 30A scan that found pick
unusable was about multi-year fade DEPTH; this year-one interaction had never been tested.)

## 6 · The acceptance record

- Corrected-surface production weight W: **0.326**, inside the corrected hindsight band
  [0.312, 0.556] (the hindsight point is 0.413). Slope 1.001 (band 0.885–1.115). No class above
  1.14 (max 1.1375 — Candidate 31's 1.1410 breach stays cured). Sitters' cell untouched (−0.017).
- Age-fair 5–9g terciles: riser gap +0.135 (nearly closed), poor gap −0.261 (better than the
  build's −0.513; the rest is the same g-keyed limitation, disclosed).
- S4 mid-career rescore: **median +53% of the years-4–6 gap recovered** (all six cells +40% to
  +67%; every years-1–3 win retained). The repair did not disturb the recovery.
- Identities: dial-off `fe6be9d6` byte-exact; fully-off `bce0c65d` byte-exact; built twice
  identical; day-0 89/89 exact AND identical to Candidate 31's prints; boot guard clean;
  coverage 100%; price reconciliation 804/804; numeraire untouched (`78ad9842`, s unmoved).

## 7 · Named rows (values vs live and Candidate 31; legs are real board deltas)

| player | live | C31 | **repaired C32** | vs C31 | what happened, in a sentence |
|---|---:|---:|---:|---:|---|
| harry-dean | 2577 | 2670 | **2400** | **−270** | the age bars clear his stall (+96) and the age credit pays him ~+50, but every feasible calibration keeps a ~35% pedigree de-rate at his 17 games and his price is 90% pedigree — see the breach note below |
| cooper-duff-tytler | 1561 | 1832 | **1572** | −260 | same shape as dean |
| billy-wilson | 983 | 547 | **675** | +128 | delivered under his age bar → fade reset (+83) plus bars (+29) |
| phoenix-gothard | 1891 | 1012 | **1327** | +315 | his 15-game season is DELIVERED → fade wiped (+394), re-mix −79 |
| nick-madden | 1766 | 715 | **1009** | +294 | relief for sustained selection (+42) and the re-mix now backs his above-bar ruck production (+252) |
| chris-scerri | 459 | 232 | **313** | +81 | age-fair re-mix backs his production (was −— a predicted faller in the build; the corrected surface reverses it) |
| thomas-burton | 439 | 213 | **309** | +96 | same |
| milan-murdock | 208 | 187 | **170** | −17 | mature, roughly flat |
| kye-annand | 239 | 334 | **282** | −52 | still a games-leg stall (9 < 9.2); his below-mature-par output re-weighted |
| lukas-cooke | 364 | 338 | **307** | −31 | two thin games, slightly re-weighted |
| ty-gallop | 1199 | 781 | **835** | +54 | late-pick young tall: age bars +30, re-mix +24 |
| charlie-west | 692 | 330 | **384** | +54 | late-pick 7-gamer: relief +42, re-mix +58, credit −44 |
| alex-dodson | 274 | 175 | **178** | +3 | the credit's two-sided cost (−38) now offset by the age-fair re-mix (+41) |
| william-mccabe | 599 | 316 | **385** | +69 | age-fair re-mix (+70) — the build had him falling; corrected, he rises |
| jedd-busslinger | 916 | 469 | **537** | +68 | relief +103 for nine above-bar games of repeated selection |
| lachlan-carmichael | 548 | 453 | **453** | 0 | gameless — untouched; his one-game jump is now +33% (half a cure), not the +71% cliff |
| josh-smillie | 953 | 459 | **459** | 0 | gameless — untouched |
| isaac-kako | 1413 | 806 | **788** | −18 | 2025 delivered at his age bar (+46) vs re-mix at 36 games (−64) |
| xavier-taylor | 802 | 1288 | **1176** | −112 | 2 games at 42: below even the age-19 expectation — poor starters can fall (the ruling) |
| daniel-annable | 1395 | 1633 | **1530** | −103 | same |

**The dean/duff-tytler breach, owned in plain words (prereg PR1 predicted they would recover;
they fell further).** The corrected surface itself says their games cell (16+) should be priced
HIGHER than any feasible calibration achieves — but the same surface demands the 1–9-game cells
come DOWN and the production weight go UP, and the only tools this repair is allowed are keyed on
GAMES, not on quality inside a cell. Dean is a pedigree-giant (entry 2741) at exactly the games
where the pedigree de-rate is deepest, and the age credit (≈+50) cannot cover a ≈35% de-rate of
2,700 points. The channel that would price dean correctly is the age lens INSIDE the pre-existing
production projection itself (his 59.7 at age 19 projected as what it is — a well-above-
expectation season — rather than a below-mature-par one). That projection is outside every scope
this order granted (the "pre-existing production legs stay untouched" discipline). Named for the
owner as the remaining dean-shaped defect; we did not improvise into it.

## 8 · What stands open for the owner (everything in one place)

1. **The late-band/thin-arm residual** (§2): closure candidates, ranked by evidence — (a) the
   band-dependent fade/credit (L3, measured 3.7×→1.5×), (b) the own-arm entry re-anchors
   (L2: PDN/PDS/PDA/MSD down, SSP up), (c) the picks-11-30 smoothing-head refit (L1/S5). All
   rulings-material.
2. **The dean-shaped defect** (§7): the age lens inside the production projection. Rulings-material.
3. **31-40's sell-side red survives** (−12.9%); 41-64's halved (−6.1%). Printed red, root causes
   above.
4. **The class level** still sits ~6 points under fair IN AGGREGATE, but §2 shows it is not
   uniform; closing the named cells closes most of it. No uniform lift proposed or wired.
5. Prereg 32R scorecard: PR2 held (half the poor bucket re-labeled; corrected W CI overlaps),
   PR3 held (concentration, not uniformity), PR4 held (41-64 toward 0, exact numbers above),
   PR5 held (+53%), PR6 held (all identities); **PR1 breached** (dean/duff-tytler — §7),
   R3's original "no band below 0" target missed for 31-40/41-64 (reported, not adjusted away;
   the vantage matrix was diagnostic-only per amendment A2). Declared deviation: one grid
   refinement pass around the single feasible point (same selection rule; disclosed in
   `REMIX_32R.json`).

Files: `PREREG_32R.md` (+A1–A3) · `REMIX_32R.json` · `W2_32R_{RESULTS,SCORECARD}.json` ·
`NOARB_32R{.json,_out.txt}` · `ATTRIBUTION_32R{.json,_out.txt}` · `S4_32_RECOVERY.json` ·
`DAY0_32_FINAL.json` · `docs/ledgers/CANDIDATE_32_MOVERS.{json,md}` · `PREVIEW_32_PLAYERS.html` ·
`PREVIEW_32_YEAR1.html` · board `7802ee97` / matrix `f4300308` in the scratchpad.

*— Order A seat, repair leg. Candidate only; the owner's word decides.*
