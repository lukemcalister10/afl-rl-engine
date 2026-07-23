# ITEM 409 — EVIDENCE MEMO · FINAL · model review seat · 2026-07-23
Identity stamp: main 07c12e5 · store f37d9716 · board 6f07f7cb · frozen curve 89c14729 (968de0c7 / 40d7da7c).
Sealed reads SR-1…SR-7 filed before their measurements. Hands: one blind read-only Fable Code session (pack
prescreened; every cheap decisive claim re-run at this seat and reproduced exactly) plus seat-side measurements.
OWNER REFRAME (word, 2026-07-23, sealed in SR-7): the governing question is not "which players deviate from the
model's surface" but "is the way we're valuing wrong." This final issue is structured around that question.
Method limitation owned: the blind residual pass (Part C) measures deviation from the board's OWN pricing
surface — it can find bugs, it structurally cannot judge the framework, because the framework defines its
comparators. Framework judgment requires external anchors; those are Parts A and B.

## PART A — IS THE FRAMEWORK WRONG? (the owner's five fundamentals + the netting zero-point)

**Unifying hypothesis (seat analysis, for adjudication — not asserted as fact):** the model prices the
AGE-COHORT CURVE strongly and the individual's demonstrated deviation from it weakly, and it encodes the same
age/evidence priors at more than one layer, so they compound. Every major anomaly in this review is one flaw
seen from a different side:
- Young side: flat-to-DECLINING young MIDs price +670…+1160 over comparators (Soligo 88.4→69.8 DOWN, Long
  78.9→70.0 DOWN, Sonsie never near the bar) — career-year upside granted by cohort membership, blind to the
  individual trajectory. VAL-001 (re-verified exactly) shows two caution layers stacking then the improver
  restoring asymmetrically — the register's "double-conservatism" is the same double-encoding pattern.
- Old side, the owner's exhibit measured: **Amon vs Farrell average an IDENTICAL 86.5 in 2026**; Amon's last
  three seasons (92.3/92.3/86.5) dominate Farrell's (82.6/88.0/86.5) — yet Amon is assigned a LOWER level
  (81.4 vs 85.9) and 0.37× the price (546 vs 1455), and was crashed −61% in a year (1394→546) on a −6%
  production dip. Assigning lower current level to dominated-better current production means the age prior
  enters at the LEVEL layer (window reach-back + shrinkage) and AGAIN at projection — double-charged, the
  mirror image of VAL-001. (AUD-007, layer interaction / signal reuse, anticipated exactly this and is
  BLOCKED on AUD-004.)
- The cohort economics agree: SOLID producers median 234 $/PAR vs young-pedigree 690 $/PAR; sub-bar veterans
  crater to median 56 while sub-bar young projects hold hundreds-to-thousands.
- McInerney (owner reason now in-stats, so a model-defect claim per doctrine): a 91.8 MID at 26 with a steady
  incline and no shown ceiling holds 1920 — under the hypothesis, cohort-peak runway priced without
  demonstrated upside. Counter-position: Dean/O'Sullivan over Mraz is ENDORSED by the owner — pedigree + games
  beating a 3-game streak is the model getting reliability right; the flaw claim is about the age-curve
  weighting, not about pedigree per se.

The five fundamentals (SR-7), each with what current evidence says and how it is decided:
- **F1 — replacement bars too high.** Bars 66.8–80.1 vs the measured free pool (level rank-16 = 52.94, gaps
  14–27 pts). Owner-flagged exploratory: reduce and observe. Decide: walk-forward — did near-bar producers
  outperform their prices?
- **F2 — projecting forward wrongly.** Strongest current evidence (young decliners priced up; Amon crashed;
  trajectory-blind career-year credit). Decide: walk-forward realization test of projection vs demonstrated
  deviation.
- **F3 — the averaging window.** Amon's ln 81.4 sits 7–9 pts below his own last-three (window reaching into
  2021-23). Decide: pure prediction horse-race — refit level under alternative windows on history, score
  next-season prediction error. Cheapest decisive test; runnable read-only from the ONE SOURCE's per-year
  scoring today.
- **F4 — recency weighting wrong.** Same horse-race, recency-parameter sweep (subject to the L-RECENCY
  monotone guard). Note the evidence cuts both ways by age — Amon under-recency, Soligo's price ignoring his
  down-year — consistent with the unifying hypothesis rather than a single global recency error.
- **F5 — replacement transition too hard / smoothing too narrow.** Measured shape at the bar is smooth (no
  cliff; softplus) — the SHARPNESS (curvature width) is a free parameter the walk-forward can score.
- **F6 — the zero-point (SR-4 netting).** Assets read against zero, not against the free alternative
  (V_free ≈ 225 at the general rank-16-by-value anchor; circularity caveat — the pool's top values are
  pedestal rows this review finds overpriced, and 16 keeper teams passed on them, so honest V_free ≤ 225).
  Consequences: the pick tail compresses far more than the head in net terms (the owner's tail instinct IS
  the netting); consolidation trades gain an uncredited freed-spot value; sub-V_free players read negative-net
  (a delist signal). Presentation fork (net values / gross + spot asset line / diagnostic column) is an owner
  ruling after the framework verdict.

## PART B — THE INSTRUMENT
**AUD-004 (historical validation framework) is OWNER-RULED with reopen trigger "before the next material
valuation-changing bake" — that trigger is now.** Design sketch: walk-forward replay — as-of boards/levels at
historical rounds, scored against realized production and value 1–3 seasons ahead; per-cohort calibration
(price percentile vs realized percentile) answers F1/F2/F5; estimator horse-race on the store's per-year
scoring answers F3/F4 (read-only, runnable pre-408 under this seat's fences); the F6 anchor re-measured after
any pedestal cure. Assets: store carries full per-year scoring; book machinery exists
(forward_valuation/build_cohort_book.py; session_2026-07-15/book_calibration incl. young_cohort_walkforward.csv;
reseal_book.py harnesses). Full price-level replay may need the harness migration the register already notes.
Constraint carried from doctrine: multi-lever framework changes must be ABLATED, not reasoned; origin-safe
folds per AUD-004's own requirements; G-COHORT and L-RECENCY guards stay hard.

## PART C — BUG-LEVEL FINDINGS (stand regardless of the framework verdict; demoted from headline)
1. Pedestal: the flat-581 no-evidence MSD/UNR cluster sits +179…+261$ above empirical E[v|ep]; min(ep,70) cap
   flattens picks 71–99; all four project ruckmen confirmed on it. [re-runnable]
2. Curve-tail echo: 19 tail rows lifted ×1.5044 because the adopted curve feeds back into its own inputs via
   the pedestal — the R19 re-derivation's +20 tail rise partly hears its own echo; break the loop before any
   RL_PVCFIT re-adoption. Genuine store-side rise (R15–19 evidence) exists beneath it. [re-runnable]
3. Smoothness census (15 live items): B5 FLOOR_YRS anniversary STEP schedule (ND-only — unequal bar by entry
   door); 3-game role-decay on/off boundary; games≥6 FV filters; assorted kinks. None at PAR=0 itself. [re-runnable]
4. Thin-evidence admission: Mraz's 3 games (all 2026, avg 85 — owner-corrected record) enter ln at full face
   (== raw avg to 6 d.p., prior pn 53.4 unblended, uncertainty maxed) and move core value +1,773; natural
   experiment: Zakostelsky, same position, same 3 games, level 49 → 465 (4.7× gap on a 3-game average).
   Ross: level leans on one s8 surge at 26 — surge-persistence weighting question. [re-runnable]
5. Store hygiene: Mraz `_has26`=false despite a 2026 scoring row (defanged by or-clauses rl_model.py:617/:1165);
   Brisbane roster 47 vs 46 cap; in-season pool 64 [owner-seen] vs 75 measured (likely the 18 _force_active
   rows). All routed to the owner for the seam seat.
6. VAL-001 CONFIRMED exactly at the committed artifact lines. [re-runnable]

## CORRECTIONS LEDGER (this seat, owner-caught, owned)
C1: SR-4 first misread as level-bar re-anchoring; corrected to value-axis netting (F6). C2: "2026 breakout"
label wrong — tracks show flat-to-declining; corrected to trajectory-blind career-year credit (F2). C3:
Mraz/Ross/McInerney wrongly lumped; split (Part C.4; McInerney reclassified in-stats after the owner supplied
his reason). C4: Mraz "zero games this season" mis-statement corrected — all three games ARE this season.
C5: Dean/O'Sullivan "ordering tension" retracted — owner endorses that ordering. C6: headline reframed from
bug-ranking to the framework question, on the owner's word.

## RECOMMENDATION OF RECORD
Activate the framework review as its own owner-worded workstream: the F3/F4 estimator horse-race may run now
(read-only, this seat's fences, one Code session); the full AUD-004 walk-forward replay lands post-408 with
the harness migration; F1/F5/F6 decided on its results; Part C cures batch behind it. No model change moves
from this seat; every cure becomes its own owner-worded release under the full seam pattern.
*Returns to the owner; the supervisor pen files it.*

## ADDENDUM — PACK 2 RESULTS (framework tests; independently re-run in full at this seat, all numbers reproduced exactly) · 2026-07-23
Identity: artifacts byte-identical to the pin (f37d9716 / 6f07f7cb / 89c14729); hands' tip d97a8e77 differs from the
seat pin 07c12e5 by three docs-only register commits (v386–v388) — verified benign. Panel: 8,985 cells, 1,587
players, cutoffs 2005–2025, origin-safe. Fence note for the record: the session harness requested a branch commit;
the hands refused per the read-only fence.

**F3 (averaging window) — WRONG, measured.** Every exponential-recency estimator with λ∈[0.10,0.60] beats every
calendar window; the 3-season window ranks 18/25; pooled winner EXP λ=0.30 beats the best window by ΔwMAE +0.32,
CI90 [+0.27,+0.37], 100% of resamples. Windows lose as a CLASS.
**F4 (recency) — opposite direction, with structure.** Prediction-optimal weighting is MORE recency-concentrated
than any window (λ=0.30: last season ×0.30, two back ×0.09) but not truncation (last-season-only ranks 17th).
≤22 wants even faster decay (λ=0.20, resolved at 90%); 27–29 points slower (0.50, unresolved). Exhibit: EXP0.30
reads Amon's form at ≈88.6 vs board ln 81.4 — a measured ~7-pt level-layer staleness on the owner's exhibit.
**F2 (projection) — split, measured, targets delivered.** Realized-optimal blend weight on INDIVIDUAL evidence:
0.79 pooled; by band 0.67 (≤22) / 0.88 (23–26) / 0.85 (27–29) / 0.79 (30+) — CIs tight; the age curve earns its
keep mainly through drift intercepts (+7.1 pts/yr at ≤22, −3.4 at 30+). Young decliners REBOUND: next season
+7.2 above the down year (vs improvers −0.4; diff +7.6, CI [+6.7,+8.5]) — holding a young down-year UP is
directionally right, which cuts against both the seat's unifying hypothesis and part of the over-read; the open
question is magnitude vs comparators. 30+ high producers fade hard: −9.4 mean next season vs current form, only
41% hold within −5, and 23% never return — fading vets is directionally right; the defect narrows to level
staleness (measured) plus possible double-fade (magnitude unmeasured).
**F6 (V_free) — fragile to the pedestal ruling.** Full free pool: rank-16 = 225 (median 96); excluding
no-evidence rows: rank-16 = 75 (median 44). Rank-1 of the whole pool is itself a pedestal row (Barnett 615).
The netting constant depends on whether no-evidence project rows count at their disputed prices — owner ruling.
Correction C7 (seat): the directive said "four" pedestal RUCs; the class has five board-wide (Barnett 615
included) plus a third in-pool RUC lnNull row (446). Hands' count report resolved: seat error, owned.
**F1/F5 — untouched by this pack (need price-side replay).**
**Task E feasibility (report-only):** the committed build_cohort_book.py is a GENUINE as-of walk-forward
(in-memory truncation to ≤Y, 2009–2026, no repo-tree writes) — runnable TODAY in a Code container after
installing the repo's pinned deps; only its output path needs an existing out-dir. The book-LEDGER replay is
blocked on two uncommitted input JSONs (builder never committed); reseal harnesses write in-tree and are
excluded. → The F1/F2-magnitude/F5 study does NOT need to wait for the 408 merge.

**Calibration targets now on record** (what any post-408 cure must match): λ*(band) = 0.20/0.40/0.50/0.25
(only ≤22 resolved vs pooled 0.30); w*(band) = 0.67/0.88/0.85/0.79; drift(band) = +7.1/+2.5/−0.6/−3.4 pts/yr;
vet-fade −9.4 conditional + 23% attrition; young-decliner rebound +7.2.

**Addendum 2 (seat measurement, [re-runnable]): λ optimum is an ARC IN AGE, not a constant** — per-age-year race on the pack-2 panel: λ* ≈ 0.05–0.15 at 18–21, rising to 0.55–0.60 at 26–27, falling past 30 (thin cells 31+). Largest gains vs flat 0.30: age 21 (+0.145), 26 (+0.147), 27 (+0.273). Design constraints recorded: implement as a SMOOTH λ(age) curve (no band constants — Smoothness Law applies to the estimator itself); position layering NOT yet supported (retrospective-grp confound, half-coverage, no significance); thin segments take partial pooling; all optima are in-sample — adoption requires out-of-fold ablation under AUD-004 origin-safe rules. The Task-B blend weight w(age) is the second, separately resolved dial and takes the same smooth-curve treatment.

## ADDENDUM 3 — PACK 3: THE WALK-FORWARD VERDICT (scoring independently re-derived at this seat from the raw panel; engine run attested by runmeta + workbook md5 e921bd05 + row-level extraction assertions) · 2026-07-23
Label carried per the owner's standing AUD-004 ruling: RETROSPECTIVE LIFECYCLE RECONSTRUCTION, not origin-time
validation. Leakage inventory delivered (18 inputs; parameters full-history-fitted; three present-state leaks
found in the replay machinery itself — career-total games inside peak_est, 2026-only position fields,
SEASON_PROG=0.79 applied at every historical year — logged as bug-class register items). Asymmetric validity
rule applied as predeclared. Repo-integrity note: the hands observed their clone snap from a nonexistent local
ref to the true tip; seat verification confirms GitHub main intact and linear (both pins ancestors; the stale
SHA unknown to history) — recurring Code-environment artifact, benign, logged.

**(b) THE VERDICT [seat re-derived, exact]:** at ranking next-season production, the model — parameters
flattered by full-history fitting — loses to the two-parameter benchmark (EXP0.30 level + band age drift):
games-weighted standing MAE 17.874 vs 14.931, gap +2.943, CI90 [+2.58, +3.31] (seat bootstrap), positive in
every band, largest at ≤22 (+3.82), robust across constructions. A fortiori valid under the leakage rule.
**(d) AGE TILT [seat re-derived, exact]:** pooled value percentile minus realized next-season production
percentile: ≤22 +8.91 · 23–26 −10.45 · 27–29 −16.25 · 30+ −21.68 (all CIs far from zero). Honest frame: a
dynasty value SHOULD tilt toward youth in kind (it prices future years, and realization is conditional on
returning — washouts drop out, so the young tilt is if anything understated); what makes the tilt a defect
finding is (b) — the ordering it produces is measurably beaten by a simple production-based alternative,
worst among the young — plus (a): within young low deciles, value draws ×1.5–2.3 distinctions over outcomes
flat within ~2 pts (project differentiation is mostly attrition noise), while 30+ mid-deciles show real
outcome differences the value surface flattens (the Amon defect in cohort form). Within-band residual
(seat diagnostic, pm_pct construction): small and opposite-signed (≤22 −6.6 … 30+ +2.8) — cross-band
allocation, not within-band ordering, carries the main error.
**(c)** All 13 owner exhibits tabulated in csv/exhibits.csv, trajectories only. **Near-bar zoom:** value
separates outcomes (rp-pct 43→82) with flat patches d2–d5 — F5 partially supported, transition-width study
remains for the origin-safe framework.
**Fence record:** third consecutive session refused harness push-boilerplate under the directive fence.

## CLOSING STATE OF ITEM 409
F2 answered (verdict above); F3 proven wrong, F4 inverted with the λ(age) arc measured; F1/F5 partially
answered by calibration curves, final answer assigned to the post-408 origin-safe framework (AUD-004
activation); F6 measured with the V_free fork awaiting the owner's pedestal ruling. The definite/consider
change lists stand as recorded above. No model change moved from this seat. The memo files on the owner's
word; the change program becomes owner-worded releases under the full seam pattern after ITEM 408 merges.

**Addendum 4 (seat measurement on the verified panel, owner-prompted): the 3-YEAR horizon.** Target = games-
weighted realized production percentile over Y+1..Y+3 (rp_pct, weight gw; conditional on ≥1 game in window).
The model still loses: standing MAE 17.733 vs benchmark 15.585, gap +2.149, CI90 [+1.78, +2.53], positive in
every band (+0.93…+2.59) — the multi-year machinery does not redeem itself at the horizon it exists for, against
a benchmark not even built for that horizon. Raw VALUE ordering vs the same target: gap +3.583 overall, but the
band split is the finding — ≤22 only +0.78 (over three years the youth tilt nearly pays for itself among the
young), while 23–26/27–29/30+ lose by +5.2/+6.6/+9.6, worsening with age. Reading: young value partially
captures real multi-year upside; veteran under-ranking is not redeemed at any measurable horizon. Beyond Y+3:
unmeasurable from this panel (attrition-dominated); assigned to the origin-safe framework, with the standing
caveat that dynasty value also prices non-production economics (picks, trades) no production target captures.
Label correction (seat): the "two-parameter benchmark" is precisely two INGREDIENTS, five constants — one
recency decay (λ=0.30) and a four-entry age-drift table (+7.11/+2.49/−0.61/−3.35) — all pack-2-measured, none
model-tuned; no position, pedigree, pick, injury, or captaincy inputs.

**Addendum 5 (seat measurements + hand-off design, owner-prompted).** (i) Pedigree at maturity [re-runnable]:
ND cohorts ≤2020, peak era (ages 24–28) — reach rate 95%→41% top-5→picks 56–80; games-weighted peak avg 91.3
(top-5) vs 73–77 (picks 21+); elite (≥90) rate 42.7%→2.5%, monotone. Correction of the seat's year-1-only
claim: pedigree is survival-dominant early and a genuine production signal at maturity → model ingredient
shape: career-year-indexed pedigree curves, not a flat year-0 pedestal. (ii) Best-model program (hand-off
recommendation): 1. build the AUD-004 origin-safe referee (frozen chronological folds, predeclared multi-
horizon metrics incl. attrition, immutable protocol); 2. measure the ceiling (unconstrained model, never
adopted — sizes the prize); 3. grow a governed forecast core from the 5-constant benchmark by forward
selection of measured ingredients (λ(age) arc, drift, blend w(age), career-year pedigree, attrition model,
rebound, position-if-resolved), out-of-fold-resolved admissions only, smooth curves, partial pooling; the
core forecasts each player's future-season distribution incl. the zero-games branch; 4. pricing layer kept
separate and owner-ruled (γ discounting, V_free netting, conservation, captaincy; pick prices derived from
entrant forecast distributions — endogenously resolves the tail and removes the pedestal feedback by
construction; makes the AUD-005 empirical/policy boundary architectural); 5. the race: incumbent engine
(leakage declared) vs benchmark vs governed rebuild vs ceiling under the referee; adoption only by owner
word under the seam pattern. Post-408; read-only until adoption; Fable-tier design per doctrine.

## OWNER CLOSING NOTE + WORDS OF RECORD (2026-07-23)
Owner-observed gap, recorded verbatim in substance: the replacement values themselves and the SCAR
system/valuation mapping were never directly validated in this investigation — F1 received only partial
calibration-curve evidence and the production→SCAR scale, replacement bars, and numéraire conservation were
not adjudicated. Carried as a NAMED QUESTION into the best-model workstream (pricing-layer validation).
OWNER WORDS: (1) FILE this memo — given 2026-07-23 in the model-review chat; filing executes via the
supervisor pen per the one-pen doctrine. (2) OPEN the best-model workstream — charter drafted by this seat
(docs/directives candidate: BEST_MODEL_WORKSTREAM_CHARTER.md), register number assigned by the pen.
Seat close: ITEM 409 investigation complete; corrections ledger C1–C9 owned (C9 = the year-1-only pedigree
generalization, corrected by the peak-era measurement); no writes were made to the repo by this seat or its
Code hands at any point.
