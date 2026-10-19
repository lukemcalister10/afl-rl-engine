# PLAYER LEDGER — ORDER 26B (re-issued 26B-L2, GRACE-A BASIS)

**One row per store player, 2,650 rows. Built for the owner's own reading. NO derivation changes.**

> ### THE RATING TO READ IS `observed_discounted_grace_a`
> **RE-ISSUED on the owner's clarification.** The first issue of this ledger was built pre-grace,
> on a reading that his *"before the year 1 grace thing"* was an instruction to exclude grace. It was
> not: he was citing the pre-grace number as **the KIND of rating he meant**, not asking for that
> basis. **The current ruled basis is grace-A**, and the ledger now leads with it.
>
> The pre-grace column is **kept as the baseline**, and the raw undiscounted column is **unchanged by
> grace** (no discount, nothing to shift).
>
> **Provenance, stated exactly:** relayed to this seat as ORDER 26B-L2, an owner clarification
> **still to be filed** on #334. `SHIPPING_PACKET_26B.md` §18 still carries grace-A as NOT-RULED
> because it was written before this clarification; the two will agree once the clarification is
> filed. **Nothing in this ledger feeds a derivation**, so no curve, cell or instrument moves either
> way.

| | |
|---|---|
| dataset | `PLAYER_LEDGER.csv` md5 `5472fe7549ea3edf983f9217b67afa52` |
| builder | `docs/evidence/delivered_value_2026-08-12/o26b_ledger.py` |
| source store | `engine/rl_after/rl_model_data.json` md5 `d9a24282357cf3083b1640466e3ecd83` |
| source Layer 1 | `layer1_player_seasons.json` md5 `ad1229ea6f443538479447132382b21c` |
| source Layer 2 | `docs/evidence/delivered_value_2026-08-12/LAYER2.json` |
| rows | **2650** |

**Deterministic**: no timestamp is written, so re-running the builder against the same inputs
reproduces the same bytes and the same md5. Read-only: the store pin is asserted at entry and exit.

---

## COLUMN DEFINITIONS

| # | column | definition |
|---|---|---|
| 1 | `key` | the store's own player key |
| 2 | `stream` | the pathway the career was ATTRIBUTED to: `ND 1-64`, `ND>64`, `RD`, `SSP`, `MSD`, `IRE`, `PDA`, `PDN`, `PDS`, `UNR` |
| 3 | `entry_year` | draft / intake year (the store's `year`) |
| 4 | `natural_pick` | the pick as the store records it. **Blank for pickless pool entrants.** |
| 5 | `attributed_pick` | **the attribution the curve actually used.** ND rows only; blank for pool rows, which are attributed to pathway × day-0-position cells and never to a pick. |
| 6 | `day0_position` | the ACQUISITION-slot position group (Ruling 5) — the position on his card the day he arrived, not the position he ended up playing |
| 7 | `n_seasons` | played-season rows in the store |
| 8 | `career_games` | games summed from those season rows |
| 9 | **`observed_discounted_grace_a`** | **THE CURRENT-BASIS RATING.** Every played season valued at the position played that season against its replacement bar (via the engine's own netting path), games-weighted, summed — discounted back to acquisition under **grace-A**: for an entrant aged **≤19**, seasons 1 and 2 are **undiscounted** and the 14 %/yr fade starts at season 3; for an entrant aged **20+**, unchanged from the baseline. **Board points.** |
| 10 | `observed_discounted_flat14_baseline` | **the BASELINE, PRE-GRACE.** Identical in every respect except that the 14 %/yr fade starts at season 1 for everybody. This was column 9 of the first issue. |
| 11 | `raw_undiscounted_value` | **the same season valuation with the discount OFF** — identical bars, identical games weighting, every season counting equally. **Unchanged by grace**: with no discount there is no exponent to shift. The gap between 10 and 11 is purely the time-weighting. |
| 12 | `grace_a_over_baseline` | column 9 ÷ column 10. **Exactly 1.0000 for every 20+ entrant** and ~1.30 for a ≤19 entrant whose value sits past season 2. Blank where the baseline is 0. |
| 13 | `flags` | `·`-separated (see below) |
| 14 | `player` | display name — a convenience column |

### Flags

| flag | meaning |
|---|---|
| `FORCE-MAJEURE-EXCLUDED` | `thomas-boyd` / `paddy-mccartin` — the owner's standing force-majeure ruling. **Their values ARE in this ledger**; they were excluded from the *curve*, not from the record. |
| `ACTIVE` | not retired in the store |
| `FIT-TIER-core` / `-augmented` / `-sensitivity` | Ruling 8's window on the entry year: ≤2014 / 2015–2021 / 2022+ |
| `IN-ND-CURVE-FIT` / `IN-POOL-CELL-FIT` | which fit population the career actually fed |
| `SLID-2013-14` | slid up one pick by the force-majeure whole-draft slide |
| `STORE-PVC-EXCLUDE` | the store carries `_pvc_exclude=True` on this row — **see NUANCES 3** |
| `PICKLESS` | the store records no pick |
| `PRE-2004-OUT-OF-WINDOW` | entry before 2004, outside every fit population |

---

## WHAT COLUMN 9 IS AND IS NOT — read this before comparing rows

1. **NO PROJECTED TAILS ANYWHERE IN THIS FILE.** Column 9 is the measured record only. That is the
   owner's explicit instruction, and it is why `jason-horne-francis` appears here on his four played
   seasons alone rather than on the observed-plus-projection total the curve saw.
2. **For a CORE-TIER (≤2014) ND player, column 9 IS his curve contribution — for a concluded career,
   exactly; for the handful still playing, to within a tail of 0.6 % value-weighted.** Core-tier
   careers are almost all finished, so observed = total for them. **The exception is worth naming
   rather than rounding away**: `joshua-kelly` contributed 3,592.8 to the curve and shows 3,590.9
   here (tail 1.9); `christian-petracca` contributed 3,621.7 and shows 3,513.0 (tail 108.7). Both
   are still playing. So "exactly" holds for retired core-tier players and to ~0.6 % for the rest.
3. **For an AUGMENTED-TIER (2015–2021) player, column 9 is LESS than what he contributed.** Those
   careers fed the fit as observed **+ a gated projected tail**, and the tail is 37.0 % of the
   augmented tier's value. Column 9 deliberately omits it.
4. **For a SENSITIVITY-TIER (2022+) player, he contributed NOTHING to any fit.** Those entries are
   walk-forward sensitivity only and never shape a curve.
5. **Pool players fed pathway × position CELLS, not the pick curve.** Their column-5 attribution is
   blank for that reason.
6. **GRACE-A IS APPLIED — this supersedes the first issue's note.** The first issue said *"grace-A /
   grace-B are NOT applied. These are pre-grace numbers, as asked."* **That note is withdrawn.**
   Column 9 is the grace-A basis and is the rating to read; column 10 preserves the pre-grace number
   it replaced. **grace-B is still not applied** and remains a NOT-RULED variant
   (`SHIPPING_PACKET_26B.md` §18); it would lift a ≤19 entrant by ~1.46 rather than ~1.30.
7. **The two observed columns rank players differently, and the difference is entirely entry age.**
   grace-A multiplies a ≤19 entrant by ~1.30 and a 20+ entrant by exactly 1.0000, so **mature-age
   entrants slide down the rankings and teenagers rise** — with no change whatever to the seasons
   underneath. The biggest movers in both directions are listed at the end of this file. A rank
   difference here is a statement about the discount rule, **not** about the careers.
8. **A zero is a real zero.** A career whose every season sat at or below its replacement bar scores
   0 and stays in every denominator. 948 of the 2650 rows score 0.00 in column 9.

## THE 2026 IN-PROGRESS SEASON — carried as it stands

**Confirmed against the harvest**: Layer 1 carries **805** season rows for the in-progress 2026
season, of which **433** are full seasons (≥10 games), **230** are PARTIAL (1–9 games) and
**142** are listed-not-yet-played placeholders at 0 games. All of them are included in columns 9
and 10 exactly as they stand.

**The games weighting handles the partials by construction**: `w = min(1, sqrt(games/10))`, so a
season of ≥10 games counts as a full season at its average and anything below is down-weighted on the
square root — a 4-game cameo carries `sqrt(0.4) = 0.632` of a season, not a full one. A 0-game
placeholder contributes exactly 0. **No 2026 row is extrapolated to a full season.**

## NUANCES HIT WHILE BUILDING THIS — reported, not resolved

1. **The 2011 ND rows stand as they are, pre-insertion-fix.** Column 5 shows the attribution this
   order's curve actually used, which for 2011 is the store's own picks with no correction applied.
2. **The 2013 and 2014 drafts are slid** (flag `SLID-2013-14`): every ND draftee in those years is
   attributed one pick better than his natural pick, `thomas-boyd` and `paddy-mccartin` are dropped
   from the curve, and the natural pick-2s — **`joshua-kelly` and `christian-petracca` — carry
   attributed pick 1**. Their natural picks (2) are in column 4 beside it.
3. **THREE store rows carry `_pvc_exclude=True` and this order's derivation did not honour it.**
   They are `dylan-shiel` (ND 2011 pick 4), **`jeremy-cameron` (ND 2011 pick 12)** and
   `adam-treloar` (ND 2011 pick 14). The engine's own curve excludes these three from teaching; this
   order's fit population was built from Layer 1, which carries raw facts and not engine teaching
   flags, so **all three sat in the ND curve fit at picks 4, 12 and 14**. Flagged per row as
   `STORE-PVC-EXCLUDE`. Two things follow and neither is adjudicated here:
   - it is a **real divergence** between this derivation's teaching population and the engine's, and
     it is not covered by any assert in the packet;
   - the sweep's flag F1 records that the ruling's Cameron *"sits as RD 2013 pick 6, unflagged"* —
     that row is **`charlie-cameron`**, a different player. **`jeremy-cameron` IS in the store as ND
     2011 pick 12 with the exclude flag set.** Whether F1 means one Cameron or the other is an owner
     question, not a build decision.
4. **Career games are summed from the season rows**, not read off the store's career counter. The
   two disagree on 457 active records by 1–2 games — the counter is a round-lagged snapshot of the
   in-progress season (recorded in Layer 1's own `measured_anomaly_323`). Column 8 matches what was
   actually valued.

---

## TOP 60 BY GRACE-A OBSERVED VALUE (the current basis)

| key | player | stream | entry | nat. pick | attr. pick | d0 pos | seasons | games | **GRACE-A (current basis)** | baseline pre-grace | raw undiscounted | flags |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `scott-pendlebury` | Scott Pendlebury | ND 1-64 | 2005 | 5 | 5 | MID | 21 | 407 | **8,450.5** | 6,502.4 | 20,130.2 | ACTIVE · FIT-TIER-core · IN-ND-CURVE-FIT |
| `marcus-bontempelli` | Marcus Bontempelli | ND 1-64 | 2013 | 4 | 3 | MID | 13 | 279 | **8,259.9** | 6,365.3 | 17,224.4 | ACTIVE · FIT-TIER-core · SLID-2013-14 · IN-ND-CURVE-FIT |
| `clayton-oliver` | Clayton Oliver | ND 1-64 | 2015 | 4 | 4 | MID | 11 | 226 | **7,738.2** | 5,955.2 | 12,505.1 | ACTIVE · FIT-TIER-augmented · IN-ND-CURVE-FIT |
| `nathan-fyfe` | Nathan Fyfe | ND 1-64 | 2009 | 20 | 20 | MID | 16 | 248 | **7,339.2** | 5,668.3 | 12,948.5 | FIT-TIER-core · IN-ND-CURVE-FIT |
| `jackson-macrae` | Jackson Macrae | ND 1-64 | 2012 | 8 | 8 | MID | 14 | 280 | **7,296.2** | 5,614.2 | 14,151.3 | ACTIVE · FIT-TIER-core · IN-ND-CURVE-FIT |
| `joel-selwood` | Joel Selwood | ND 1-64 | 2006 | 8 | 8 | MID | 16 | 355 | **7,256.6** | 5,591.6 | 14,087.6 | FIT-TIER-core · IN-ND-CURVE-FIT |
| `patrick-dangerfield` | Patrick Dangerfield | ND 1-64 | 2007 | 10 | 10 | MID | 19 | 376 | **6,862.3** | 5,280.4 | 17,500.7 | ACTIVE · FIT-TIER-core · IN-ND-CURVE-FIT |
| `zachary-merrett` | Zachary Merrett | ND 1-64 | 2013 | 26 | 25 | MID | 13 | 272 | **6,707.8** | 5,163.8 | 12,985.2 | ACTIVE · FIT-TIER-core · SLID-2013-14 · IN-ND-CURVE-FIT |
| `brodie-grundy` | Brodie Grundy | ND 1-64 | 2012 | 22 | 22 | RUCK | 14 | 261 | **6,570.4** | 5,059.6 | 14,888.1 | ACTIVE · FIT-TIER-core · IN-ND-CURVE-FIT |
| `lance-franklin` | Lance Franklin | ND 1-64 | 2004 | 5 | 5 | KPF | 18 | 326 | **6,491.7** | 4,997.2 | 14,509.9 | FIT-TIER-core · IN-ND-CURVE-FIT |
| `lachie-neale` | Lachie Neale | ND>64 | 2011 | 66 | 66 | MID | 15 | 315 | **6,389.9** | 4,916.8 | 15,321.7 | ACTIVE · FIT-TIER-core · IN-POOL-CELL-FIT |
| `dustin-martin` | Dustin Martin | ND 1-64 | 2009 | 3 | 3 | MID | 15 | 302 | **6,138.8** | 4,731.8 | 11,994.0 | FIT-TIER-core · IN-ND-CURVE-FIT |
| `max-gawn` | Max Gawn | ND 1-64 | 2009 | 33 | 33 | RUCK | 15 | 268 | **6,068.7** | 4,669.7 | 20,143.3 | ACTIVE · FIT-TIER-core · IN-ND-CURVE-FIT |
| `tom-rockliff` | Tom Rockliff | RD | 2008 | 1 | — | MID | 13 | 205 | **5,828.6** | 4,484.9 | 9,743.4 | FIT-TIER-core · IN-POOL-CELL-FIT |
| `brett-deledio` | Brett Deledio | ND 1-64 | 2004 | 1 | 1 | MID | 15 | 266 | **5,751.3** | 4,450.6 | 11,152.1 | FIT-TIER-core · IN-ND-CURVE-FIT |
| `adam-treloar` | Adam Treloar | ND 1-64 | 2011 | 14 | 14 | MID | 15 | 263 | **5,679.0** | 4,419.7 | 10,736.5 | ACTIVE · FIT-TIER-core · STORE-PVC-EXCLUDE · IN-ND-CURVE-FIT |
| `patrick-cripps` | Patrick Cripps | ND 1-64 | 2013 | 13 | 12 | MID | 13 | 251 | **5,500.1** | 4,232.1 | 9,989.0 | ACTIVE · FIT-TIER-core · SLID-2013-14 · IN-ND-CURVE-FIT |
| `nick-daicos` | Nick Daicos | ND 1-64 | 2021 | 4 | 4 | MID | 5 | 115 | **5,438.2** | 4,234.7 | 6,494.0 | ACTIVE · FIT-TIER-augmented · IN-ND-CURVE-FIT |
| `josh-dunkley` | Josh Dunkley | ND 1-64 | 2015 | 25 | 25 | MID | 11 | 215 | **5,403.9** | 4,161.4 | 9,606.7 | ACTIVE · FIT-TIER-augmented · IN-ND-CURVE-FIT |
| `dayne-zorko` | Dayne Zorko | ND 1-64 | 2011 | 38 | 38 | MID | 15 | 315 | **5,250.5** | 5,250.5 | 12,623.4 | ACTIVE · FIT-TIER-core · IN-ND-CURVE-FIT |
| `marc-murphy` | Marc Murphy | ND 1-64 | 2005 | 1 | 1 | MID | 16 | 294 | **5,243.7** | 4,035.9 | 10,037.5 | FIT-TIER-core · IN-ND-CURVE-FIT |
| `tom-mitchell` | Tom Mitchell | ND 1-64 | 2011 | 13 | 13 | MID | 12 | 207 | **5,208.6** | 4,007.8 | 10,161.0 | FIT-TIER-core · IN-ND-CURVE-FIT |
| `harry-sheezel` | Harry Sheezel | ND 1-64 | 2022 | 3 | 3 | SF | 4 | 88 | **4,985.3** | 3,939.0 | 5,593.2 | ACTIVE · FIT-TIER-sensitivity |
| `sam-walsh` | Sam Walsh | ND 1-64 | 2018 | 1 | 1 | MID | 8 | 154 | **4,940.1** | 3,833.5 | 6,743.9 | ACTIVE · FIT-TIER-augmented · IN-ND-CURVE-FIT |
| `isaac-heeney` | Isaac Heeney | ND 1-64 | 2014 | 4 | 3 | MID | 12 | 243 | **4,836.4** | 3,722.0 | 9,355.0 | ACTIVE · FIT-TIER-core · SLID-2013-14 · IN-ND-CURVE-FIT |
| `zak-butters` | Zak Butters | ND 1-64 | 2018 | 12 | 12 | MID | 8 | 156 | **4,798.7** | 3,692.5 | 7,697.1 | ACTIVE · FIT-TIER-augmented · IN-ND-CURVE-FIT |
| `todd-goldstein` | Todd Goldstein | ND 1-64 | 2006 | 38 | 38 | RUCK | 18 | 345 | **4,787.7** | 3,684.0 | 13,287.7 | FIT-TIER-core · IN-ND-CURVE-FIT |
| `jack-steele` | Jack Steele | ND 1-64 | 2014 | 21 | 20 | MID | 12 | 223 | **4,767.9** | 3,670.9 | 9,056.7 | ACTIVE · FIT-TIER-core · SLID-2013-14 · IN-ND-CURVE-FIT |
| `dayne-beams` | Dayne Beams | ND 1-64 | 2008 | 29 | 29 | MID | 11 | 177 | **4,718.7** | 3,633.2 | 7,710.8 | FIT-TIER-core · IN-ND-CURVE-FIT |
| `joshua-kelly` | Joshua Kelly | ND 1-64 | 2013 | 2 | 1 | MID | 13 | 230 | **4,666.2** | 3,590.9 | 8,574.1 | ACTIVE · FIT-TIER-core · SLID-2013-14 · IN-ND-CURVE-FIT |
| `steele-sidebottom` | Steele Sidebottom | ND 1-64 | 2008 | 11 | 11 | MID | 18 | 373 | **4,649.1** | 3,585.7 | 9,814.1 | ACTIVE · FIT-TIER-core · IN-ND-CURVE-FIT |
| `luke-parker` | Luke Parker | ND 1-64 | 2010 | 42 | 42 | MID | 16 | 336 | **4,643.1** | 3,572.7 | 10,490.6 | ACTIVE · FIT-TIER-core · IN-ND-CURVE-FIT |
| `christian-petracca` | Christian Petracca | ND 1-64 | 2014 | 2 | 1 | MID | 11 | 231 | **4,565.6** | 3,513.0 | 9,323.6 | ACTIVE · FIT-TIER-core · SLID-2013-14 · IN-ND-CURVE-FIT |
| `rory-laird` | Rory Laird | RD | 2011 | 8 | — | SD | 14 | 285 | **4,510.2** | 3,470.4 | 11,602.4 | ACTIVE · FIT-TIER-core · IN-POOL-CELL-FIT |
| `josh-p-kennedy` | Josh Kennedy | ND 1-64 | 2006 | 41 | 41 | MID | 15 | 290 | **4,351.2** | 3,348.1 | 10,340.9 | FIT-TIER-core · IN-ND-CURVE-FIT |
| `nicholas-naitanui` | Nicholas Naitanui | ND 1-64 | 2008 | 2 | 2 | RUCK | 13 | 213 | **4,340.6** | 3,340.0 | 9,059.9 | FIT-TIER-core · IN-ND-CURVE-FIT |
| `rory-sloane` | Rory Sloane | ND 1-64 | 2008 | 44 | 44 | MID | 15 | 255 | **4,324.6** | 3,327.6 | 8,669.7 | FIT-TIER-core · IN-ND-CURVE-FIT |
| `oliver-wines` | Oliver Wines | ND 1-64 | 2012 | 10 | 10 | MID | 14 | 290 | **4,290.3** | 3,304.3 | 7,912.3 | ACTIVE · FIT-TIER-core · IN-ND-CURVE-FIT |
| `andrew-brayshaw` | Andrew Brayshaw | ND 1-64 | 2017 | 2 | 2 | MID | 9 | 191 | **4,278.0** | 3,291.8 | 6,932.9 | ACTIVE · FIT-TIER-augmented · IN-ND-CURVE-FIT |
| `bryce-gibbs` | Bryce Gibbs | ND 1-64 | 2006 | 1 | 1 | MID | 14 | 268 | **4,210.2** | 3,239.7 | 7,408.0 | FIT-TIER-core · IN-ND-CURVE-FIT |
| `touk-miller` | Touk Miller | ND 1-64 | 2014 | 29 | 28 | MID | 12 | 235 | **4,203.8** | 3,236.9 | 8,458.8 | ACTIVE · FIT-TIER-core · SLID-2013-14 · IN-ND-CURVE-FIT |
| `heath-shaw` | Heath Shaw | ND 1-64 | 2003 | 46 | 46 | SD | 16 | 298 | **4,116.3** | 3,167.3 | 9,131.9 | FIT-TIER-core · PRE-2004-OUT-OF-WINDOW |
| `timothy-english` | Timothy English | ND 1-64 | 2016 | 19 | 19 | RUCK | 10 | 169 | **4,114.0** | 3,165.6 | 7,672.4 | ACTIVE · FIT-TIER-augmented · IN-ND-CURVE-FIT |
| `matt-priddis` | Matt Priddis | RD | 2005 | 27 | — | MID | 12 | 228 | **3,942.8** | 3,942.8 | 9,648.6 | FIT-TIER-core · IN-POOL-CELL-FIT |
| `luke-jackson` | Luke Jackson | ND 1-64 | 2019 | 3 | 3 | RUCK | 7 | 140 | **3,925.5** | 3,020.6 | 5,920.6 | ACTIVE · FIT-TIER-augmented · IN-ND-CURVE-FIT |
| `cyril-rioli` | Cyril Rioli | ND 1-64 | 2007 | 12 | 12 | SF | 11 | 189 | **3,869.1** | 3,003.8 | 5,880.5 | FIT-TIER-core · IN-ND-CURVE-FIT |
| `rowan-marshall` | Rowan Marshall | RD | 2016 | 8 | — | RUCK | 10 | 175 | **3,834.6** | 3,834.6 | 8,217.2 | ACTIVE · FIT-TIER-augmented · IN-POOL-CELL-FIT |
| `thomas-liberatore` | Thomas Liberatore | ND 1-64 | 2010 | 24 | 24 | MID | 15 | 267 | **3,791.7** | 2,921.4 | 9,313.5 | ACTIVE · FIT-TIER-core · IN-ND-CURVE-FIT |
| `jarryd-roughead` | Jarryd Roughead | ND 1-64 | 2004 | 2 | 2 | KPD | 14 | 262 | **3,777.8** | 2,907.3 | 8,600.3 | FIT-TIER-core · IN-ND-CURVE-FIT |
| `tim-taranto` | Tim Taranto | ND 1-64 | 2016 | 2 | 2 | MID | 10 | 192 | **3,730.0** | 2,876.4 | 6,142.6 | ACTIVE · FIT-TIER-augmented · IN-ND-CURVE-FIT |
| `travis-boak` | Travis Boak | ND 1-64 | 2006 | 6 | 6 | MID | 19 | 387 | **3,701.9** | 2,848.5 | 10,017.9 | FIT-TIER-core · IN-ND-CURVE-FIT |
| `errol-gulden` | Errol Gulden | ND 1-64 | 2020 | 34 | 34 | MID | 6 | 112 | **3,701.0** | 2,852.7 | 4,805.8 | ACTIVE · FIT-TIER-augmented · IN-ND-CURVE-FIT |
| `bailey-smith` | Bailey Smith | ND 1-64 | 2018 | 7 | 7 | MID | 7 | 146 | **3,662.0** | 2,822.4 | 5,711.4 | ACTIVE · FIT-TIER-augmented · IN-ND-CURVE-FIT |
| `toby-greene` | Toby Greene | ND 1-64 | 2011 | 17 | 17 | MID | 15 | 279 | **3,651.6** | 2,866.8 | 6,953.4 | ACTIVE · FIT-TIER-core · IN-ND-CURVE-FIT |
| `michael-barlow` | Michael Barlow | RD | 2009 | 5 | — | MID | 9 | 141 | **3,602.9** | 3,602.9 | 6,065.2 | FIT-TIER-core · IN-POOL-CELL-FIT |
| `jack-gunston` | Jack Gunston | ND 1-64 | 2009 | 29 | 29 | KPF | 17 | 298 | **3,585.9** | 2,759.3 | 7,674.7 | ACTIVE · FIT-TIER-core · IN-ND-CURVE-FIT |
| `james-sicily` | James Sicily | ND 1-64 | 2013 | 52 | 51 | SF | 11 | 199 | **3,549.1** | 2,730.9 | 8,230.3 | ACTIVE · FIT-TIER-core · SLID-2013-14 · IN-ND-CURVE-FIT |
| `robert-gray` | Robbie Gray | ND 1-64 | 2006 | 55 | 55 | SF | 16 | 271 | **3,545.4** | 2,731.3 | 8,506.4 | FIT-TIER-core · IN-ND-CURVE-FIT |
| `hugh-mccluggage` | Hugh McCluggage | ND 1-64 | 2016 | 3 | 3 | MID | 10 | 222 | **3,508.5** | 2,699.8 | 5,887.0 | ACTIVE · FIT-TIER-augmented · IN-ND-CURVE-FIT |
| `sam-fisher-2003` | Sam Fisher | ND 1-64 | 2003 | 50 | 50 | KPD | 12 | 208 | **3,506.3** | 3,506.3 | 8,004.9 | FIT-TIER-core · PRE-2004-OUT-OF-WINDOW |

---

## THE ROWS THE OWNER ASKED FOR BY NAME

| key | player | stream | entry | nat. pick | attr. pick | d0 pos | seasons | games | **GRACE-A (current basis)** | baseline pre-grace | raw undiscounted | flags |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `joshua-kelly` | Joshua Kelly | ND 1-64 | 2013 | 2 | 1 | MID | 13 | 230 | **4,666.2** | 3,590.9 | 8,574.1 | ACTIVE · FIT-TIER-core · SLID-2013-14 · IN-ND-CURVE-FIT |
| `christian-petracca` | Christian Petracca | ND 1-64 | 2014 | 2 | 1 | MID | 11 | 231 | **4,565.6** | 3,513.0 | 9,323.6 | ACTIVE · FIT-TIER-core · SLID-2013-14 · IN-ND-CURVE-FIT |
| `jason-horne-francis` | Jason Horne-Francis | ND 1-64 | 2021 | 1 | 1 | MID | 5 | 100 | **1,985.0** | 1,529.3 | 2,489.5 | ACTIVE · FIT-TIER-augmented · IN-ND-CURVE-FIT |
| `willem-duursma` | Willem Duursma | ND 1-64 | 2025 | 1 | 1 | MID | 1 | 19 | **61.4** | 53.8 | 61.4 | ACTIVE · FIT-TIER-sensitivity |
| `callum-moore` | Callum Moore | RD | 2015 | 9 | — | KPF | 3 | 10 | **6.7** | 5.2 | 7.6 | FIT-TIER-augmented · IN-POOL-CELL-FIT |
| `thomas-boyd` | Thomas Boyd | ND 1-64 | 2013 | 1 | — | KPF | 5 | 61 | **60.5** | 46.6 | 74.4 | FORCE-MAJEURE-EXCLUDED · FIT-TIER-core |
| `paddy-mccartin` | Paddy McCartin | ND 1-64 | 2014 | 1 | — | KPF | 6 | 63 | **57.2** | 44.0 | 124.9 | FORCE-MAJEURE-EXCLUDED · FIT-TIER-core |
| `harrison-ramm` | Harrison Ramm | MSD | 2025 | 3 | — | KPD | 2 | 5 | **0.0** | 0.0 | 0.0 | ACTIVE · FIT-TIER-sensitivity |
| `vigo-visentini` | Vigo Visentini | RD | 2023 | 5 | — | RUCK | 2 | 3 | **72.8** | 56.0 | 83.0 | ACTIVE · FIT-TIER-sensitivity |
| `jai-newcombe` | Jai Newcombe | MSD | 2021 | 2 | — | MID | 6 | 123 | **2,016.3** | 2,016.3 | 3,062.1 | ACTIVE · FIT-TIER-augmented · IN-POOL-CELL-FIT |

---

## RANK MOVERS BETWEEN THE TWO OBSERVED COLUMNS

Ranked over the **790 players whose baseline is at least 100 board points** — a material
career. Rank moves inside the block of players tied at 0.00 are an artefact of tie ordering and are
excluded for that reason. `move` is positive when a player rises under grace-A.

**The whole effect is the entry-age clause.** A 20+ entrant is multiplied by exactly 1.0000 — his
grace-A and baseline figures are the same number — and he is simply overtaken by teenagers lifted
~1.30. Nothing about any career changed.

### Biggest SLIDES (mature-age entrants, passed by teenagers)

| key | player | stream | entry | entry age | grace-A | baseline | rank base → grace-A | move |
|---|---|---|---|---|---|---|---|---|
| `tom-campbell` | Tom Campbell | RD | 2011 | 20 | 247.8 | 247.8 | 590 → 649 | -59 |
| `dale-morris` | Dale Morris | RD | 2004 | 22 | 541.0 | 541.0 | 406 → 464 | -58 |
| `jack-hayes` | Jack Hayes | SSP | 2021 | 25 | 245.1 | 245.1 | 595 → 653 | -58 |
| `jonathon-ceglar` | Jonathon Ceglar | RD | 2012 | 21 | 496.9 | 496.9 | 424 → 482 | -58 |
| `lachlan-schultz` | Lachlan Schultz | ND 1-64 | 2018 | 21 | 495.6 | 495.6 | 425 → 483 | -58 |
| `matthew-jaensch` | Matthew Jaensch | RD | 2009 | 20 | 499.3 | 499.3 | 423 → 481 | -58 |
| `robin-nahas` | Robin Nahas | RD | 2008 | 21 | 535.6 | 535.6 | 409 → 467 | -58 |
| `ben-howlett` | Ben Howlett | RD | 2009 | 21 | 510.2 | 510.2 | 421 → 478 | -57 |
| `hayden-ballantyne` | Hayden Ballantyne | ND 1-64 | 2008 | 21 | 546.5 | 546.5 | 404 → 461 | -57 |
| `nick-hind` | Nick Hind | ND 1-64 | 2018 | 24 | 777.2 | 777.2 | 325 → 382 | -57 |
| `ricky-henderson` | Ricky Henderson | RD | 2008 | 20 | 560.9 | 560.9 | 394 → 451 | -57 |
| `sam-lloyd` | Sam Lloyd | ND 1-64 | 2013 | 23 | 246.2 | 246.2 | 593 → 650 | -57 |
| `zach-tuohy` | Zach Tuohy | IRE | 2009 | 20 | 548.8 | 548.8 | 401 → 458 | -57 |
| `liam-anthony` | Liam Anthony | ND 1-64 | 2008 | 21 | 797.5 | 797.5 | 323 → 379 | -56 |
| `mark-baguley` | Mark Baguley | RD | 2011 | 24 | 256.6 | 256.6 | 585 → 641 | -56 |

### Biggest RISES (≤19 entrants)

| key | player | stream | entry | entry age | grace-A | baseline | rank base → grace-A | move |
|---|---|---|---|---|---|---|---|---|
| `jarrad-grant` | Jarrad Grant | ND 1-64 | 2007 | 18 | 464.1 | 357.1 | 521 → 500 | +21 |
| `noah-balta` | Noah Balta | ND 1-64 | 2017 | 18 | 459.6 | 353.6 | 522 → 501 | +21 |
| `ollie-dempsey` | Ollie Dempsey | RD | 2021 | 18 | 458.4 | 352.8 | 523 → 502 | +21 |
| `adam-tomlinson` | Adam Tomlinson | ND 1-64 | 2011 | 18 | 468.7 | 360.7 | 517 → 497 | +20 |
| `jake-waterman` | Jake Waterman | ND>64 | 2016 | 18 | 468.4 | 360.4 | 518 → 498 | +20 |
| `kade-kolodjashnij` | Kade Kolodjashnij | ND 1-64 | 2013 | 18 | 471.5 | 363.7 | 514 → 494 | +20 |
| `michael-talia` | Michael Talia | ND 1-64 | 2011 | 18 | 452.3 | 348.3 | 524 → 504 | +20 |
| `sam-powell-pepper` | Sam Powell-Pepper | ND 1-64 | 2016 | 18 | 468.1 | 360.4 | 519 → 499 | +20 |
| `darcy-macpherson` | Darcy MacPherson | RD | 2015 | 18 | 388.6 | 299.1 | 559 → 540 | +19 |
| `jasper-mcmillan-pittard` | Jasper Mcmillan-Pittard | ND 1-64 | 2009 | 18 | 474.1 | 364.8 | 512 → 493 | +19 |
| `levi-greenwood` | Levi Greenwood | ND 1-64 | 2007 | 18 | 553.4 | 425.8 | 475 → 456 | +19 |
| `massimo-d-ambrosio` | Massimo D'Ambrosio | MSD | 2022 | 19 | 470.2 | 361.8 | 515 → 496 | +19 |
| `matthew-taberner` | Matthew Taberner | RD | 2012 | 19 | 517.9 | 398.5 | 494 → 475 | +19 |
| `nathan-van-berlo` | Nathan van Berlo | ND 1-64 | 2004 | 18 | 547.2 | 421.1 | 478 → 459 | +19 |
| `robert-warnock` | Robert Warnock | ND 1-64 | 2005 | 18 | 520.9 | 400.8 | 493 → 474 | +19 |
