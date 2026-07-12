# SPEC 1 — NEWCOMBE PRODUCTION-SIDE DECOMPOSITION — v2.9 investigation spec · 2026-07-12
### Register item 1 (OPEN_ITEMS v8) · TIER-3 spec (design only; nothing here ships) · FABLE
### Board facts verified on the baked v2.8 board (store 04f38dad · engine 7a07e369 · board 9ecbe0fa).

## 0 — WHAT IS ALREADY SETTLED (do not re-measure)
The PVC re-derivation (banked branch `claude/pvc-re-derivation-icbhpu` @ 3c1d610f, ADDENDUM item 1)
replicated the MSD pathway pedestal EXACTLY on delivered value: pooled MSD delivered (n=45, H5)
re-expresses to pick-equivalent **60 — identical to the shipped 60**. The pathway pedestal is NOT
the mechanism. Any Newcombe overvaluation, if real, lives on the PRODUCTION side: how the engine
turns his delivered line into 4495, versus what that line-at-that-age has historically delivered
forward. This spec designs that decomposition.

## 1 — SUBJECT AND PILOT EVIDENCE (read-only, this session)
`jai-newcombe` — MID, MSD 2021 pick 2 (`_eff`=60), born 2001-08-02 (25 in 2026), 114 games.
Line: 45.7(7g) → 86.9(22) → 98.3(22) → 101.6(25) → 96.7(26) → 102.5(13, in-progress). **ev 4495.**
Twin pilot (in-memory clones of his exact line, priced by the live engine; no store writes):
| twin | ev | reads as |
|---|---|---|
| as-is (MSD, eff 60, born 2001) | 4495 | the board row |
| ND pick 60, born 2001 (same line, same age) | 4405 | pathway label ≈ **−90 (2%)** — confirms §0 |
| ND pick 60, born 2003 (same line, normal-age) | 5715 | age is priced hard: **+1220 (+28%)** younger |
| ND pick 2, born 2001 (same line, top capital) | 4058 | **pick-2 label prices BELOW pick-60 (−347)** |
Two structural facts fall out: (i) the engine already discounts Newcombe ~21% against a normal-age
twin — the owner's "overvalued vs normal-age draftees with the same line" is NOT true as a
same-price claim; if the read survives, it must mean the age discount is TOO SHALLOW; (ii) the
par-relative machinery REWARDS a low-expectation label at the same output (pick-60 > pick-2 at an
identical elite line) — `iso_corr` (isotonic pick guard, multiplicative ≥1 at shallow picks) and
`recover(perf/par)` saturation both credit output *relative to a low par*. The MSD-60 pedestal
inherits exactly this flattery. That is a production-side mechanism candidate, and it is measurable.

## 2 — MEASUREMENT DESIGN
Two instruments, run in order; the second is the decider.

**M-1 · Twin-ladder attribution (engine-internal, deterministic).** Formalize the pilot: a ladder of
in-memory twins {pathway label · pick capital · birth year · line truncations} priced by the live
engine, each rung's Δ recorded so the 4495 decomposes into: production base (price6/b6 band value)
· par-relative credits (iso_corr multiplier; pole term w·recover(perf,par)·(po−pr)) · M1 up-branch
credit (S_M1=0.46 on the current-over-recency gap, TOL_M1=5) · forward-years/age term (wage,
tfade(T), _agemult family) · floor/staleness (expected inert — verify). G-ATTR discipline: every
rung separable, rungs sum to the twin gap. Output: one table, SC points per layer.

**M-2 · Walk-forward delivery calibration (the actual question).** Does the engine's price of an
age-25, ~100-SC-level, high-games MID match what such players DELIVERED forward, and is there a
mature-entry residual after conditioning on age and level?
- Estimand: R = delivered forward value (engine ruler, SCAR above positional REPL, summed Y+1..Y+5)
  ÷ engine price at end-Y, per player-season.
- Population A (subject class): players with debut age ≥ 20.5 (mature/alternate-pathway: MSD + SSP
  + rookie-elevation mature entrants), measured at each established season Y.
- Population B (comparator): normal-age entrants (debut age < 19.5) in the SAME age × level cells.
- The read is about a DIFFERENTIAL: ΔR = R_A − R_B within cell. The engine already prices age
  (pilot: +28% for −2 years); only a residual pathway effect after age × level matching would
  support the owner's read.

## 3 — EXACT DATA CUTS
- Store: the single-source store (Guard 5 pinned, 04f38dad basis; the v2.9 job re-pins at fire time).
- Event seasons Y: 2004–2020 inclusive so Y+5 outcomes complete by 2025 (leak-free vs the 2026
  board). WALK-FORWARD BASIS (named, per doctrine): any model quantity evaluated at Y uses only
  data ≤ Y; assert by CODE READING of the extraction script (the G-COHORT basis rule; numeric
  fingerprints are non-discriminating and retired).
- Cells: age at Y ∈ {23,24,25,26,27} × level (recency-weighted `_lvlcurr`-convention) bands
  {80–90, 90–100, 100–110, 110+} × position pooled-primary with MID cell shown (MID is the subject
  cell; other positions pooled — POOLING DECLARED).
- Mature-entry side: MSD did not exist before 2019 — the mature-age population pre-2019 is VFL/SSP/
  rookie mature entrants. The n=45 MSD harvest (ADDENDUM, H5) is the pathway-pedestal set, NOT this
  set; this cut is debut-age-defined, not mechanism-defined, precisely so it has history. Expected
  n: thin at high levels (few mature entrants reach 100+); pool level bands upward as needed and
  DECLARE each pooled cell in the output table.
- Both lenses: live 15% discount and undiscounted (lens-robustness convention from the PVC METHOD).
- Delivered value counts games actually played; exits/delists contribute zero forward — washout-
  INCLUSIVE (the delivery question includes career mortality; that is the point of the test).

## 4 — TEST DESIGN
- Primary: kernel-smoothed ΔR over age (eff-n ≥ 35 per node, the repo's standing kernel discipline),
  cluster bootstrap by player (B=1000) for bands. "Supported" = ΔR bands separate from 0 across the
  24–26 age range (the same bands-separate standard the age-persistence research used) — NOT a
  pre-registered p-gate (doctrine: acceptance = owner reads + hard guards, never statistical gates;
  the statistics INFORM the owner's ruling).
- Secondary (mechanism sizing, only if primary finds a residual): regress the residual on the M-1
  layer exposures (iso_corr multiplier, pole-credit share, M1-credit share) to name WHICH layer
  carries it — the fix must be a mechanism correction, not a mature-age multiplier (blanket
  multipliers FORBIDDEN, G-COHORT remediation doctrine).
- Newcombe himself: after M-2, restate his 4495 as (calibrated class price) ± (his personal
  deviations: durability 22-26 games/yr, still-rising line at 25). He is ONE draw; the class curve
  rules, the owner rules the name (OWNER-ON-SIGHT convention).

## 5 — EXPECTED CONFOUNDS (each with its control)
1. **Survivorship at entry** — mature entrants are pre-filtered (drafted off proven state-league
   output), so their downside tail may be thinner: biases ΔR UP for A. Control: condition on
   level-at-Y (both populations already producing); report years-1-2-since-debut separately.
2. **Age-at-same-tenure vs tenure-at-same-age** — engine curves split across both clocks (wage/
   _agemult on age; tfade/par_at(T) on tenure). A mature entrant sits in a (young-tenure × old-age)
   cell normal draftees rarely occupy — the fitted surfaces there are extrapolating. Control: M-1
   sizes each clock's term directly; M-2 cells are AGE-defined (the market-relevant clock).
3. **List-security mortality** — mature entrants may exit lists earlier at the same level (shorter
   leash, no capital sunk). This is REAL forward-value loss, not a confound to remove — but report
   exit rates separately so the owner sees whether ΔR is production decline or list mortality.
4. **In-progress 2026 season** (Newcombe 13g @ 102.5) — M3/SEASON_PROG handling; M-1 runs at the
   season-complete convention too so the twin table isn't a mid-season artifact.
5. **Era drift** — scoring levels drift across 2004–2020; level bands computed vs season REPL, and
   class-year effects absorbed by the cluster bootstrap; report per-era splits if bands allow.
6. **The pick-60 par flattery is not Newcombe-specific** — every MSD/late-pick producer rides it
   (pilot: pick-2 twin −347). If M-2 finds the class over-delivers relative to price (ΔR > 0), the
   same machinery may be UNDER-paying — symmetric outcome, honestly reported.

## 6 — REFUTATION CLAUSE (owner doctrine §49: the read is a starting point)
This spec REFUTES the owner's read as one honest outcome: if ΔR bands include 0 at ages 24–26
(mature entrants deliver forward like normal-age entrants at the same age × level), then pathway
carries no production-side residual either, Newcombe's 4495 stands as the calibrated price of an
elite 25-year-old MID line, and register item 1 closes with "measured, no mechanism found" — the
same closure class as the Travaglia and Kysaiah waivers. The pilot already shows the naive form of
the read (same price as a young twin) is false; what remains testable is the discount's DEPTH.

## 7 — IMPLICATIONS (mandatory)
- **If a residual is found (mature entrants under-deliver their price):** the carrier will almost
  certainly be one of (a) too-shallow age slope in wage/_agemult at 24–27, or (b) par-relative
  flattery (iso_corr / recover saturation) crediting low-expectation labels. Fix (a) touches EVERY
  ~25yo (Butters/Holmes — A-PEAK ≤2% drop tolerance binds; G-COHORT y4-6 numerator falls — ratio
  moves the SAFE way). Fix (b) touches every late-pick producer and the MSD/SSP pedestal consumers
  — it interacts with the SSP 92→~51 line (same PICKEQ consumers) and MUST be sequenced with the
  PVC adoption job in the v2.9 batch, not ruled separately.
- **If refuted:** the owner's Newcombe read joins Travaglia/Kysaiah as waived-after-measurement; the
  residual owner lever is the ND pricing-floor/label question, already closed.
- **Interlock:** M-2's population-A definition (debut-age, not mechanism) deliberately covers the
  nicholas-martin side too (SSP, 83g, ev 2935) — one measurement serves both halves of register
  item 1; the SSP pedestal (92→~51) rides the PVC job and is NOT re-derived here.
- **Guards touched by any fix:** G-COHORT (re-measure walk-forward, mandatory), G-PEAK/A-PEAK,
  A-BONT (Bontempelli is 30yo-cohort; age-slope fixes graze him — BINDING ≥+10% from 3246), G-MONO
  (iso_corr changes reshape the pick curve). All named here so the v2.9 build carries them as
  acceptance from day one; acceptance itself = owner reads + hard guards, per doctrine.
- **Cost of not running it:** the owner's read stays an anecdote against a 4495 board row that the
  pedestal replication already half-cleared; every future mature-age entrant (a growing class under
  MSD) prices on unaudited machinery.
