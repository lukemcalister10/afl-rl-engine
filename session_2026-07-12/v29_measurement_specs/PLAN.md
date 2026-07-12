# PLAN — v2.9 INVESTIGATIONS SPEC — session 2026-07-12 · branch claude/v2-9-measurement-specs-jj52xd
### TIER 3 (read-only) · FABLE · one job, one chat · supervisor directive v1 2026-07-12

## BASE VERIFICATION (done before this commit)
- `git ls-remote https://github.com/lukemcalister10/afl-rl-engine` (full URL):
  - main == **626c83780f678c9204e1fcf80f43868b239dfc2f** — EXACT match to the directive pin.
  - tag v2.8 == **9bd0cfdbf9faff83fee21c843fac2ebb5baa25c9** — EXACT match.
- Banked-research branch pins verified against ls-remote:
  - `claude/pvc-re-derivation-icbhpu` == 3c1d610f ✓
  - `claude/age-persistence-curve-research-l7hinr` == 394cd16 ✓
- Boot guard (session start): store 04f38dad == pinned ✓ · engine 7a07e369 · cm_400 34faa865 ·
  register 652d83e8. This job WRITES NONE of those — Tier 3 read-only.
- Session branch `claude/v2-9-measurement-specs-jj52xd` cut from main 626c8378.

## FEED (all present, none missing — no STOP required)
- docs/DECISIONS_v95_2026-07-12.md ✓
- docs/CONSTRAINTS_v1_7.md + docs/acceptance_v1_7.json ✓
- docs/OPEN_ITEMS_REGISTER.md v8 ✓ (items 1, 4, 6, 7 = the four subjects)
- Banked: PVC re-derivation (icbhpu @ 3c1d610f) · age-persistence (l7hinr @ 394cd16) — fetched.

## TIME BAND
2–4h confirmed. Estimate: lower half of band (spec authoring + read-only store/book computation
for context numbers). Will flag if projection crosses >2× or <½×. Fable-window note acknowledged:
this is the last Fable job before the window closes — no dependency on any later Fable session is
allowed to enter any spec.

## DELIVERABLES (four committed spec docs, one per register item; this directory)
1. `SPEC_1_NEWCOMBE_PRODUCTION_SIDE.md` — register item 1. Given: MSD pedestal replicated exactly
   (60→60), pathway is NOT the mechanism. Design the production-side decomposition: what in his
   delivered line vs cohort pricing carries the suspected overvaluation.
2. `SPEC_2_UGLEHAGAN_CLEARY_DECOMPOSE_FIRST.md` — register item 6. JUH 196 (former #1-pick KFWD,
   70g, at scrap — absence machinery suspected) · cleary 779 ("a bit high"). Layer-by-layer
   attribution for each, sized per layer, BEFORE any fix is proposed.
3. `SPEC_3_RYAN_MOORE_DOWN_PERSISTENCE.md` — register item 7. The DOWN-side mirror: does one poor
   season in a large body of work (moore 137g) mean-revert? Body-of-work-inertia measurement,
   explicitly paired with the age-persistence machinery (l7hinr) so the two curves cannot ship
   contradictory shapes.
4. `SPEC_4_RUCK_SCARCITY_INSURANCE.md` — register item 4. Owner's backup-ruck insurance philosophy
   vs the bar-margin construction (steene 252 / reeves 389 UNDER nd-kid rucks smith 693 /
   samson-ryan 636 / knobel 402). Design how insurance value could be measured and priced WITHOUT
   a hand edit wearing a rule's clothes; state explicitly how the v2.9 SSP line (92→~51) and PVC
   option (b) WIDEN the gap if unaddressed.

Every spec carries ALL FIVE mandatory sections: measurement design · exact data cuts · test
design · expected-confound list · **IMPLICATIONS** (mandatory per directive and CORE process rule).

## DOCTRINE BINDING (applies to all four; asserted inside each spec)
- Acceptance = owner reads + hard guards; NEVER pre-registered statistical gates.
- Statistics at the finest resolution the sample supports; smoothed; thin slices pooled AND declared.
- No blanket multipliers as fixes — identified mechanisms only (G-COHORT remediation doctrine).
- Every spec names its walk-forward/leak-free basis wherever a book measurement is designed
  (code-read-assertable, per the G-COHORT basis rule).
- Owner doctrine §49: reads are starting points to investigate — each spec must state the honest
  outcome under which it REFUTES the owner's read.

## METHOD
1. Read the two banked returns (icbhpu RETURN + addendum; l7hinr ruling package) for the numbers
   the specs must interlock with (SSP 92→~51 · MSD 60→60 · PVC option (b) SIM · s(age) curve).
2. Read-only store/board lookups for the ten named players (context numbers quoted in the specs;
   no store writes, no engine runs beyond read-only scoring already materialized in data/).
3. Author the four specs; commit each; push; open the candidate PR (spec docs only).

## FENCE (restated from the directive)
IN: read-only computation on the current tree · committed spec docs on this one session branch.
OUT: any store/engine/gate/data write · doc-pack authoring · any implementation · the two
in-flight Opus lanes' files (migration · UI) — this job writes ONLY under
`session_2026-07-12/v29_measurement_specs/`.

## RETURN SHAPE
≤30 lines + the four committed specs + an "in plain terms" close · branch · head SHA · PR number
(merge-commit policy) · BUILD-REPORTED until supervisor prescreen.
