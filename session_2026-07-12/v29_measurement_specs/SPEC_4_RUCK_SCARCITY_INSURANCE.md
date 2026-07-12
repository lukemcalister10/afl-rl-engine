# SPEC 4 — RUCK SCARCITY / BACKUP-INSURANCE VALUE — v2.9 investigation spec · 2026-07-12
### Register item 4 (OPEN_ITEMS v8) · TIER-3 spec (design only) · FABLE
### The tension: the owner's backup-ruck SCARCITY philosophy (insurance value) vs the bar-margin
### construction. Mandate: design how insurance value could be MEASURED and PRICED without a hand
### edit wearing a rule's clothes — and state explicitly how the v2.9 SSP line (92→~51) and PVC
### option (b) WIDEN the gap if unaddressed.

## 0 — THE ORDERING THE OWNER FLAGGED (verified this session, board 9ecbe0fa)
| player | profile | ev |
|---|---|---|
| lachlan-smith | ND pick 47 (2023), **2 games** (53.0 avg) | **693** |
| samson-ryan | ND pick 42, 26yo, nqual=1, fading line (54.2→44.0→38.5→51.3 thin) | **636** |
| max-knobel | ND pick 42 (2022), **0 games** | **402** |
| ned-reeves | SSP (2018), 28yo, **54 games**, career 57–70, 2026: 70.3 on 12g | **389** |
| oscar-steene | SSP (2022), 23yo, 8 games @ 51.6 (2026), LTI-out L=0.636, ret 2027 | **252** |
Why, mechanically: the proven backups are priced on the MARGIN construction — production above the
RUC replacement bar 78.5 — and both sit BELOW the bar (reeves 70.3, steene 51.6), so their
production leg is near zero (reeves's pre-mechanism `_v` ≈ 27). The kids are priced on the
PEDIGREE leg (pick-capital par priors, V0 scaffold, RUC prior cap 1.4 × draftval) with zero to two
games of evidence. The board is answering "who produces above 78.5" — the owner is asking "who
keeps my season alive when my #1 ruck goes down." Those are different questions, and only the
first is priced today.

## 1 — WHAT ALREADY CARRIES RUCK SCARCITY (census required before any new mechanism — the
##      double-count guard; complete this list in the build, from code, before pricing anything)
1. **REPL bar 78.5** — OWNER ARTIFACT (CONSTRAINTS Part 1b, recorded rationale: thin field of
   10–20 live rucks, breakpoint swings hard, injury replacement near-impossible — "SCARCITY TAXES
   are priced in deliberately"). Field size verified this session: 55 RUC rows, 37 with any 2026
   games, **20 with ≥8 games** — the owner's 10-20 figure is data-confirmed.
2. **RL_RUCK_TAX = 0.25** (env, consumed as rd.RUCK_TAX) — the young-ruck pick fade (G-MONO
   requires it smooth, no pk20/21 step).
3. **RUC prior cap** — 1.4 × draftval, the last live old-PVC consumer on the player side (PVC
   ADDENDUM); under option (b) it re-expresses onto the derived curve.
4. **keyruc staleness multipliers** (1.6/1.5 on the stalled/mediocre fracs) and the W4
   production-derived ruck ceiling (`_ruc_ceiling`, Emmett machinery).
Any measured insurance value must be priced NET of what these already pay, or the fix double-counts
the same scarcity the owner already hand-set into the bar.

## 2 — HOW THE v2.9 BATCH WIDENS THIS GAP IF UNADDRESSED (stated explicitly, as directed;
##      numbers from the banked option-(b) SIM, branch icbhpu @ 3c1d610f, out/sim_option_b.json)
- **PVC option (b)** moves exactly 24 players, all young pick-capital/pedestal RUCs, +8–27%:
  lachlan-smith 693→**733** (+5.8%) · max-knobel 402→**512** (+27.4%) · goad 818→878 ·
  conway 479→581 · barnett 544→651. The proven backups: **ned-reeves NOT a mover (389→389)**;
  oscar-steene moves only via his SSP prospect leg (252→**281**, +11.5%). Ordering gaps widen
  mechanically: knobel−reeves +13 → **+123**; knobel−steene +150 → **+231**; smith−steene
  +441 → +452.
- **The SSP line (92→~51, n=24 THIN, owner rules)** lifts the SSP PROSPECT leg (pick-equivalent
  pedigree: par priors / V0 scaffold for thin-career SSPs). It reaches steene (young SSP) and
  reeves only through his residual 0.25-weight par-prior leg (nqual=3) — it does NOT touch the
  margin construction that zeroes a proven below-bar producer. It also lifts every young SSP ruck
  PROSPECT alongside.
- **Net:** both v2.9 moves pay the UNPROVEN/pedigree side of the ordering and pay the proven-backup
  side ~nothing (reeves exactly nothing under (b)). If the insurance question is not designed into
  the same ruling session, the flagged ordering gets worse under the batch the owner is about to
  rule on — and it will look like the batch caused it.

## 3 — MEASUREMENT DESIGN — pricing the insurance seat as an option, from the store alone
The philosophy translated into a measurable object: a backup ruck's value = **margin leg** (what he
produces above the bar, already priced) **+ insurance leg** = the option value of his deputy
production in the states of the world where the primary ruck is absent. Every input below is
measurable walk-forward from the pinned store; no hand-set magnitude enters.
- **P_absence(k):** the league-wide distribution of primary-ruck missed games. Per season
  2010–2025, identify primary rucks (top-N ruck-position players by games that season at each games
  tier — see confound 1 on the club-history limitation) and measure the distribution of games
  missed the FOLLOWING season. Output: P(primary misses ≥ k games), smoothed over k.
- **L_street:** what a team actually fields when it has no listed backup — the realized scoring of
  emergency rucks: ruck-position player-seasons with ≤3 games or debut-callups (the actual next
  man up). Pooled 2010–2025, kernel-smoothed; this is the counterfactual the insurance pays against.
- **L_dep(p):** the candidate's own demonstrated deputy level — his engine-ruler recency level
  (the same `_lvlcurr` object used everywhere; no new level definition).
- **The option leg:** INS(p) = Σ_h disc(h) · E[games covered in year h] · max(0, L_dep(p) −
  L_street) · (the engine's own points→SCAR translation at the RUC margin) — where E[games
  covered] integrates P_absence over k. Discount = the live lens; report undiscounted beside it
  (dual-lens convention).
- **POSITION-AGNOSTIC BY CONSTRUCTION** (this is the no-hand-edit clause): the formula is defined
  for every position — GEN_DEF depth players have an INS(p) too. It prices materially only where
  the measured inputs make it material: P_absence × (bar − L_street) is large for RUC because the
  field is thin and the street level is far below the bar — by MEASUREMENT, not by an
  `if pos=='RUC'` rule. If the measured inputs do NOT make the ruck insurance leg material, the
  owner's philosophy is refuted by his own ruler (§6). A rule that fires only on rucks because a
  measured surface says so is a mechanism; a rule that fires only on rucks because it says
  'RUC' in the code is a hand edit wearing a rule's clothes — the build is held to the former.

## 4 — EXACT DATA CUTS
- Store 04f38dad basis (re-pin at fire time). Seasons 2010–2025 for absence/street measurement
  (older seasons: ruck usage patterns differ; declared choice, sensitivity 2004– shown).
  WALK-FORWARD BASIS (named): INS components at year Y use only ≤Y data; asserted by CODE READING
  of the derivation script (G-COHORT basis rule). The book question here is calibration (below),
  same basis.
- Primary-ruck identification: per season, RUC-position players binned by games (≥15 = primary
  tier; 8–14 = rotation; ≤7 = street/emergency) — thresholds declared, sensitivity ±2 games shown.
- L_street cut: RUC player-seasons ≤3 games and first-season RUC callups, pooled (thin — declared;
  expected n in the low hundreds across 15 seasons).
- Deputy candidates for the calibration test: RUC players with demonstrated level in (street, bar)
  — i.e. below 78.5 but above street — and ≥15 career games. This is the reeves/steene class.
- Calibration (the decider): walk-forward price-vs-delivered for that class — engine price at Y vs
  realized delivered SCAR Y+1..Y+5 (which INCLUDES their step-up games: history has already run
  the insurance experiment every time a primary went down). Dual-lens. Cluster bootstrap by player.
## 5 — TEST DESIGN
- **The class test:** if the backup class's delivered forward value exceeds its priced value with
  bands clear of zero, the gap IS the unpriced insurance leg, and its size calibrates INS(p) — the
  measured surface then replaces nothing and adds one separable leg (G-ATTR: per-lever delta
  reportable per player). If delivered ≈ priced, the bar-margin construction is already honest and
  the philosophy is refuted at board scale (§6).
- **Reconciliation against the census (§1):** re-derive the class test with the existing scarcity
  carriers toggled per the census map so the new leg is sized NET (no double count). In particular
  the REPL bar is an OWNER ARTIFACT — the build ASKS before any change there (Part 1b doctrine);
  this spec's mechanism ADDS a leg and does not move the bar.
- **Named-row restatement:** steene, reeves, smith, samson-ryan, knobel re-priced with the
  candidate leg; plus **kieren-briggs** — the A-GAWN comparator is a backup-profile ruck, so this
  lever moves an anchor's comparator BY DESIGN: A-GAWN ("Gawn clearly above Briggs") must be
  re-verified and reported with the sim (BINDING, magnitude owner-on-sight).
- **The four-cell interaction table (required output):** the five named rucks × {current board ·
  +PVC(b) · +SSP-51 · +both} so the owner rules on the batch WITH the widening visible, and the
  insurance leg's counterweight quantified in the same table.
- Owner inputs to fetch at fire time (the register's "with the owner's scarcity rationale in
  hand"): (i) does insurance value belong on the MARKET board (any team would pay it) or is it
  roster-contextual (worth more to a team with a fragile #1)? The board prices market/keeper value
  — the spec prices the league-average seat and the owner rules whether context enters; (ii) the
  owner's own sizing instinct for a "quality backup at scrap" so the measured number lands against
  a stated prior — recorded beside the dial per process rule (owner rationale beside hand-set
  dials), though the number itself comes from the measurement.

## 6 — REFUTATION CLAUSE (owner doctrine §49)
The philosophy is measurable and can lose on the owner's own ruler: if the backup-ruck class
delivers forward value ≈ its bar-margin price (the step-up games are rare enough, or short enough,
or street replacement good enough, that the option expires worthless on average), then the
bar-margin construction is vindicated, the kids-over-backups ordering is measured-correct
(capital+runway really is worth more than a below-bar deputy), and register item 4 closes with the
owner's philosophy REFUTED at board scale — while the widening table (§2) still ships, because the
batch's effect on the ordering is a fact regardless of which side wins. Partial outcomes are
expressible: the leg can price steene (young, cheap, LTI-suppressed) and not reeves (28yo — his
option has few forward years), or vice versa; the mechanism prices each from his own inputs.

## 7 — EXPECTED CONFOUNDS
1. **No historical club assignment in the store** (only current `_club`) — true team-season
   backup/primary pairing is not reconstructible in-store. Control: league-pooled absence exposure
   (P_absence measured over primary-ruck seasons league-wide) prices the AVERAGE insurance seat,
   not a specific depth chart. DECLARED as the design's resolution limit; if the owner wants
   depth-chart-true pricing, that needs the owner-held positioning registers (the FLEX build's
   input — same courier, noted, NOT fetched here).
2. **Step-up production ≠ deputy's bench level:** backups often score BETTER with full ruck minutes
   (role effect). L_dep from all-games level UNDERSTATES the delivered step-up level — measure the
   step-up seasons' levels separately where visible (seasons where a low-games ruck jumps to ≥15
   games year-over-year). Direction: makes the insurance leg LARGER; the naive estimate is
   conservative — state it.
3. **Survivorship in the backup class:** backups who never got a chance exit lists; delivered-value
   calibration is washout-inclusive (zeros counted), so the class test already carries the
   mortality the option must pay for.
4. **DPP/position drift:** players tagged RUC who are really forwards (and vice versa) contaminate
   both the field-size count and L_street. Control: games-weighted ruck-share where position
   history allows; sensitivity with KEY_FWD-tagged part-time rucks in/out, declared.
5. **Era effects in ruck usage** (the sub/interchange and 666 rule changes shift ruck loads):
   2010–2025 window with per-era splits shown if bands allow; pooled primary declared.
6. **Thinness everywhere:** 20 live rucks per season is the POINT of the question — every cut in
   this spec is thin by construction. Statistics at the finest supported resolution, kernel-
   smoothed, pools declared; where even pooling fails, the output is the raw event table and the
   owner reads names (the same fallback as SPEC 2 §3).
7. **The prior-cap artifact is already ruled:** the sweep showed the OLD prior cap misbehaving
   under rate changes (emmett −20/−22% at ≤13% — artifact; option (b) removes the mechanism) and
   the discount ruling is SEQUENCED to v2.9 with (b) (register item 4 addendum). This spec's
   measurement must run on the POST-(b) machinery if (b) is adopted first, or dual-run — declared
   in the build plan, so the insurance leg is not calibrated against a cap that is about to die.

## 8 — IMPLICATIONS (mandatory)
- **Sequencing is the whole game here.** Register item 4's trigger already binds this to the v2.9
  batch "alongside the SSP line." The widening table (§2) makes that concrete: adopting PVC (b) +
  SSP-51 without the insurance answer moves the flagged ordering the wrong way by +100–230 SC on
  the named pairs. The insurance measurement must reach the SAME ruling session as (b) and the SSP
  line, or the owner rules on a board that is about to contradict his own read harder.
- **If the leg ships:** it is additive and separable (G-ATTR), so gate exposure is contained:
  G-MONO untouched (no pick-curve change), G-COHORT grazed only via young-ruck members (direction:
  small numerator lift on year-4-6 ruck survivors — re-measure walk-forward, same standing gate),
  B4 non-mover parity holds outside RUC-adjacent rows, **A-GAWN re-verified by name** (comparator
  moves), A-DARCY untouched (KPF). The G-CONVEX young-RUC floor (the one genuinely under-priced
  pocket, picks 4-10 at 0.61 coverage) is ADVISORY and moves the safe way if young backups lift.
- **If the philosophy is refuted:** the register closes item 4 with a measured answer, the owner
  keeps his hand-set REPL bar (owner artifact, untouched either way), and the v2.9 batch ships
  with the widening DISCLOSED as correct pricing rather than silently.
- **The design generalizes** (deliberately): the same option construction prices depth at any thin
  position if the league ever thins elsewhere (e.g. genuine KPF droughts) — the mechanism outlives
  the ruck question, which is what separates it from a hand edit.
- **Cost of not running it:** the owner's scarcity philosophy and his own bar-margin artifact stay
  in unresolved contradiction ON the batch he is about to rule; every backup ruck stays priced at
  the margin leg alone; and the v2.9 adoption discussion inherits an ordering complaint it
  mechanically worsened.
