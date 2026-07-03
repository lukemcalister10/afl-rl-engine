# LUKE'S RULINGS LEDGER — repo-side authority trail
_Minted 2026-07-03 (DIRECTIVE 8 ASK 1). Until now the ledger lived supervisor-side only
(`docs/supervisor_handover_2026-07-02_rev93_ROTATION.md` §4). From D8 on, every Luke ruling the build
must honour is registered HERE verbatim (plus CHANGELOG), same session it lands. Rulings are quoted
exactly as relayed; the relaying directive is the provenance. Backfill for pre-D8 rulings is
POINTER-ONLY (CHANGELOG citations) — no historical wording is reconstructed here._

## Format
`R<N> · date · ruling name · Luke verbatim · consequence · status`

## D8 rulings (2026-07-03, relayed via DIRECTIVE 8 v1)

**R1 · 2026-07-03 · A3 accept-red at 0.7307**
Luke verbatim: "Accept-red on rozee."
Consequence: A3 ships red at 0.7307 vs the amended 0.75 bar, by ruling (joins A2/Curtis as a
Luke-ruled red). Real remedy = the LTI workstream, queued. No threshold motion.
Status: ACTIVE.

**R2 · 2026-07-03 · Tsatas accept-and-track at 1140**
Luke verbatim: "Accept and track on Tsatas."
Consequence: the M3-caused lift above his preferred 1083 is accepted; TRACK the fade to 979 as the
season completes (fE→1). A8 holds 2.12x.
Status: ACTIVE (tracking).

**R3 · 2026-07-03 · Staleness-cap fix Form A — endorsement WITHHELD**
Luke verbatim: "The two cap fix is odd, because someone like Cleary is far too low when he triggers
it and probably too high when he doesn't. That Hardeman doesn't get rescued is a challenging one for
me. And looking at Cooper Lord - he's another in the Cleary boat but worse - he shouldn't be so low
now, but the idea of him being over 1000 if it didn't catch him is a bit crazy to me."
Consequence: Form A (binary gap=0 exemption) is NOT endorsed and joins NO candidate. The D7 design
read stands as a derivation artifact, superseded by the D8 graded-form round (continuum ghost-floor →
full price, driven by evidence of live output). Also registered in SYMPTOM_REGISTER.md family 1.
Status: SUPERSEDING WORK IN FLIGHT (D8 ASK 2).

**R4 · 2026-07-03 · McAndrew release ENDORSED**
Luke verbatim: "McAndrew is fine."
Consequence: his D7 cap-fix release (99→1408, 13g @ 87.1 = 1.11×REPL) is Luke-approved; McAndrew is
an ANCHOR for the graded derivation (strong-evidence upper anchor: strong current output → full
release), no longer an open question.
Status: ACTIVE (anchor).

## Pre-D8 rulings (pointer-only backfill — verbatim lives in the cited CHANGELOG entries)
- Growth law redefined (cross-cohort AVERAGE, per-cohort ungated) — CHANGELOG 2026-07-02 D5 STEP 1.
- Overlay keep M1 + v7-asc, DELETE v7-cB — CHANGELOG 2026-07-02 D7 (ASK 1).
- A3 bar 0.80→0.75 ("Happy to adjust Rozee to 75%") — CHANGELOG 2026-07-02 D7 STEP 1.
- B5 alarm RETIRED → pricing floor feature, flat tail variant A — CHANGELOG 2026-07-02 D7 STEP 1.
- A2 unchanged at 0.90, ships red ("we can look at Curtis down the line") — CHANGELOG 2026-07-02 D7 STEP 1.
- A10 bar 0.70→0.50 (data-caused, provisional) — CHANGELOG 2026-07-02 D4 STEP 1.
- Gothard calibration "probably fine, a touch rich, happy to leave it" (~1790, no shaving) — CHANGELOG 2026-07-02 D6/D7 (ASK 4).
- Effort rule + downward-justification amendment — docs/process/PROCESS_CHANGES_2026-07-02.md §11.

## D10 rulings (2026-07-03, relayed via DIRECTIVE 10 — GAMES-RAMP REWORK)

**R5 · 2026-07-03 · The games-ramp design statement (BINDING SPEC — the old-PVC sit-out anchor is retired)**
Luke verbatim: "B6 - fix first. But I do not accept the 'half of draft value' as that is derived from
the old PVC, which I believe is a relic and retired. So it makes no sense. All players are being given
a value 'the moment they are drafted' that they hold over the pre-season before their first season
starts, and then it starts responding to matches throughout the season. [...] what is happening
currently is that Annable and Cumming are being drafted, assigned a value based on their draft pick
and position, and then when matches start and Annable does not play, his rating is flipping back to
50% of the old, historical PVC." · "we should not be punishing players like Patterson for not playing
a full season when the full season has not concluded. And we should not be considering players like
Annable a full 'no sit' when he has played 1 game, that penalty should smooth in between games 0-6."
Consequence: the flat SITOUT_RETAIN×draftval anchor DELETED (obituary E2); every penalty path
re-anchored to the LIVE start value V0 (pick+position); smoothed, season-prorated, scoring-aware
games-ramp treatment derived from historical outcomes and wired at CANDIDATE v2.1 (engine e15bafa9);
B6 taken to green. The Luke-signed B5 floor stays dv-based (declared exception, pricing feature).
Status: ACTIVE (candidate v2.1; cold audit before any bake).

**R6 · 2026-07-03 · The three reporting rules (BINDING, permanent)**
Luke's word (relayed as BINDING, D10 ASK 5): (1) every gates/board output reports THREE COLUMNS —
CONTROL · PREVIOUS · CURRENT, deltas explicit; (2) every board/report carries a LOUD state label; no
unlabelled player value anywhere Luke-facing; (3) the rules bind all future sessions.
Consequence: wired in ship_gates_check.py + the book renderer + BAKE_CHECKLIST.md §REPORTING +
KICKOFF_PROMPT.md + START_HERE.md; state registry data/report_states.json; snapshots data/gates_snapshots/.
Status: ACTIVE (permanent process).

## D12 rulings (2026-07-03, relayed via DIRECTIVE 12 — CONCAVE RAMP + FLOOR RE-ANCHOR)

**R7 · 2026-07-03 · Concave penalty ramp (Luke-signed OPTION A — SUPERSEDES the D10 linear form)**
Luke verbatim: "I'm not sure that the proration should be strictly linear... especially when it comes
as a penalty, it should be slightly more generous as the sample is smaller... it will be 100% after 24
games, as it should... something like 33-40% at half way." · Ruling: OPTION A — penalty fraction =
(season progress)^1.5.
Consequence: the sit-out retention's within-season proration goes linear -> concave (sitout_ev tau term
fe -> fe**1.5), PENALTY PATH ONLY; the reward-side M1 G_ADQ gate (its harder-than-linear proration is BY
DESIGN and conforms to this same principle) is left untouched, verified by diff. Penalty fraction printed
R6/12/18/24 = .125/.354/.650/1.0; halfway .354 in the stated 33-40% band; 100% at R24. B6 seam re-proven
green at v2.2. Wired at CANDIDATE v2.2 (engine 05d38c65 after ASK1). REVISIT HOOK: a PVC-era derivation
may replace the t^1.5 SHAPE from partial-season snapshots (recorded open, not a block).
Status: ACTIVE (candidate v2.2; scoped re-audit before any bake).
