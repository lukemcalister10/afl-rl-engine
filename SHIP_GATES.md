# SHIP_GATES.md — AFL SuperCoach RL engine — FROZEN ACCEPTANCE SUITE
### Status: READY TO FREEZE (02/07/2026) — all decisions resolved by Luke; becomes
### FROZEN on his word, then committed to the repo.
### Rule: when every gate passes, the engine SHIPS and gets used for real trades.
### Post-freeze the list does not grow — new reads go to V_NEXT.md unless they
### demonstrate an existing gate is broken. Every line becomes a scripted PASS/FAIL
### check (ship_gates_check.py), run at each candidate head and at any bake.
###
### SCRIPTING NOTES (for the build):
### - EXACT-ID matching mandatory: the suite contains Harley Reid AND Zach Reid;
###   the league contains two Uwlands. No substring matching.
### - Line-ball = within ±20% (Luke, 02/07/2026).
### - A13-A14 are PVC-coupled: staged PENDING (not RED) until the pick curve exists.
### - A6 pick-matching: finest resolution with smoothing; pool the thin RUC slice
###   deliberately and say so (standing banding rule).
### - [DC] = DATA-CONDITIONAL gate (rests on current-season / thin-evidence facts as
###   of 02/07/2026); on failure, run the failure triage below FIRST.

## SECTION A — LUKE'S NAMED CALLS (all confirmed)

A1.  Willem Duursma > Zeke Uwland.
A2.  Josh Ward below genuine producers: Ward < Paul Curtis AND Ward < Josh Weddle.
A3.  [DC] Connor Rozee: thin current season must not halve him — 2026 value >= 80%
     of 2025.
A4.  Harley Reid uncratered — Reid remains TOP 40 on the board by value.
A5.  Improvers not slashed: Jack Ginnivan > 1600, Jake Bowey > 2100,
     Nick Blakey > 2600.
     [Absolute SCAR floors — RE-BASE if the PVC re-levels the currency.]
A6.  Early-career rucks: years-1-3 RUC cohort median <= pick-matched MID cohort
     median at the same stage.
A7.  Position fixes stay fixed: Ryan Maric prices off a MID pole; Ed Langdon off a
     GDEF-dominant future. (Regression insurance vs silent reversion.)
A8.  [DC] Sam Berry > Elijah Tsatas by at least 2x.
     (Luke, 02/07/2026: fair on the data available today; explicitly expected to be
      re-ruled if Tsatas's evidence base materially changes — the engine SHOULD
      respond to new data. The exemplar data-conditional gate.)
A9.  Jack Ginnivan > Josh Ward.
A10. [DC] Charlie Curnow: 2026 value >= 70% of 2025.
A11. [DC] Playing beats sitting — named pairs: Jacob Farrow > Dylan Patterson;
     Sam Cumming > Dan Annable.
A12. [DC] Sitting is not unreasonably punished — named pairs: Tobie Travaglia >
     Christian Moraes; Josh Smillie > Patrick Retschko.
     (A11+A12 bracket sit-out retention from both directions; jointly define
      acceptable outcomes for the 1.19x/retention rework.)

### Pick-vs-player anchors (PVC-coupled; PENDING until the curve exists)
A13. Pick 1 line-ball (±20%) with EACH of George Wardlaw and Levi Ashcroft.
A14. Pick ~8 line-ball (±20%) with EACH of Trent Rivers, Zach Reid, Jase Burgoyne.

A15. STRUCK (Luke, 02/07/2026): the Robey-shape package anchor. Reason: "not all
     firsts are equal — pick 1 and pick 15 have wildly different value," and the
     Robey trade itself is not a good exemplar of reasonable value. Consequence
     logged: package-vs-star CONVEXITY is the suite's one known untested dimension
     → seeded as V_NEXT entry #1 (re-poseable with exact pick numbers post-PVC).

### Deliberate NON-GATES (disagreement bounded on purpose; shipping does not wait)
N1. Mid-career (years 3-5) Parish valuation — decider: the matched same-player cut.
N2. The years-4-6 peak LEVEL — not a gate until the matched cut runs.

## SECTION B — STRUCTURAL GATES
B1. Cohort growth law: per-cohort aggregate value rises from draft to its yr4-6 peak.
B2. GATE-1: leakage ~0 (IS vs WF, tree-matched) + clean good/bust separation.
B3. Walk-forward book gates pass at the ship head.
B4. JS parity: Python and board JS byte-agree on the shipped board.
B5. No-crater guard: no first-year/unproven player value cratered (founding rule).
B6. No hard lines: value continuous across the games ramp (no step at the 6-game
    seam) AND monotone in evidence — more games at the same scoring rate is never
    worth less.

## SECTION C — BASELINE GATE (complexity must earn its keep)
C1. Ship head beats the NAIVE BASELINE (last-2-season avg + simple age curve +
    position multipliers) on the walk-forward book headline metrics.
C2. Ship head beats the ORIGINAL V1 pick model on the same metrics.
    (If either fails: stop and re-scope before the PVC.)

## PROCESS
- FREEZE: on Luke's word; committed to the repo; build scripts every line into
  ship_gates_check.py, run at each candidate head and mandatorily at any bake.
- FAILURE TRIAGE (Luke's rule, 02/07/2026 — a live engine must respond to live
  data): on any gate failure, the build attributes the cause BEFORE anything blocks:
    * ENGINE-CAUSED (a code/calibration/store change moved the value) → the gate
      blocks the bake per normal rules.
    * DATA-CAUSED (new real-world results changed the facts the gate rests on,
      e.g. Tsatas returns and performs) → NOT a block; escalate to Luke for an
      uphold-or-amend ruling, logged in CHANGELOG per the amendment process.
    * AMBIGUOUS → decompose (isolate engine change vs data change) before either
      path; no undecomposed attribution.
  [DC]-tagged gates get the triage question first by default.
- V_NEXT.md: every post-freeze read/gripe lands there, dated, untouched until the
  suite passes. Entry #1 (seeded at freeze): package-vs-star convexity anchor,
  re-poseable with exact picks once the PVC exists.
- AMENDMENT: Luke-only, in writing, reason logged in CHANGELOG.
- Red gates at freeze time are allowed and expected (e.g., A3/A10 pre-decay-fix):
  a red gate is the definition of what a fix must achieve before shipping.
- ENVIRONMENT: gates evaluated in the canonical build environment per the values
  policy (byte-exact within environment; see BAKE_CHECKLIST).
