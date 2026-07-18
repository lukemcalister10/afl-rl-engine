# PLAN — FORWARD-LENS CALIBRATION INVESTIGATION (item 351) · seat 13 · 2026-07-18
READ-ONLY (Tier 3) · report-only · findings not verdicts · changes NOTHING. FENCE: writes ONLY
`session_2026-07-18/fwd_calib/`. Engine/store/curve/docs imported READ-ONLY, never edited.

## GIT ENTRY (read-only variant — item-338 law)
`git fetch origin main claude/legf-phantom-intake-build-dvbipz claude/legf-retrospective-boards-cyqx00`
ls-remote asserted this session:
- `claude/legf-phantom-intake-build-dvbipz` = **7b6dfc52324e0b3a2367c9324e1acff6c8b0abaa** (STRICT ✓, matches directive)
- `claude/legf-retrospective-boards-cyqx00`  = **cf945898784bbdb7c064b5aa5ae1ece677383679** (F2 boards @ `cf94589` ✓)

## PROVENANCE — HONEST STAMP NOTE (read this before trusting a number)
The directive asks the forward lens be run at F1's entry stamps (store `968de0c7`, curve payload
`89c14729`). **Those are NOT reproducible in this container:** F1's private build workspace
`/home/claude/rl_ws_legf` is absent and store `968de0c7` is not on disk (the only store present is the
checked-out pin `b1fd0bce`, the v2.10 captaincy-bake head). Rather than go SILENT (a red), the probe
was run against the closest faithful lens available — the **same Leg-E/Leg-F projection family** at the
v2.10 head:

    store b1fd0bce · engine (rl_export/rl_model with vP1/vP2/RL_LEGE/RL_LEGF) · board **790136a3**
    RL_LEGE=1 RL_PVC2=1 RL_LEGF=1 · OPENBLAS_NUM_THREADS=1 (+OMP/MKL/NUMEXPR=1, item 349)

**Version-delta is bounded and does not move the verdict.** The probe reproduces F1's filed
WITHOUT-phantom +1 to ~1% (Σ vP1 = 532,870 vs F1 537,768) and its +2 (406,836 vs 393,375); the
now-total is 725,590 (v2.10) vs F2's 752,427 (F1 base) — a captaincy-bake level shift, not a shape
change. **Every finding below is a *structural* property of the lens (a rate/shape asymmetry), and it
reproduces independently on F2's separately-built −2/−1/now boards.** Where a headline cites the
directive's exact 752,427, it uses F2's board; where it cites a per-player split it uses the probe run.
Any consumer wanting byte-exact F1 numbers must re-run on store `968de0c7` — flagged, not smuggled.

## METHOD (smoothed per-cohort, no wide bins)
- **Job 1 backtest** — two independent constructions:
  (A) *composition-controlled*: the identical 804-player roster, forward one-year rate (Σv→ΣvP1) vs
      the engine's own realized backward one-year rate (ΣvM1→Σv). No membership confound.
  (B) *F2 actual boards*: a smoothed one-year forward ratio r(age)=median(vP1/v) from the probe,
      applied to F2's recorded −1 board (and −2), reproduced total vs actual now (752,427) / −1.
- **Job 2 decomp** — Σ(vP1−v) split by age cohort {developing ≤23 · mid 24–27 · veteran ≥28}, signed
  total + per-cohort mean; exits/phantom cross-referenced to F1's filed §2.v report.
- **Job 3 pedigree** — young (≤23) high-pick (≤20) low-games (≤40) rows: v (pedigree-anchored now)
  vs vP1; premium lost; share of job-2(b).
- **Job 4 distributed retirement** — P(retire|age) = pooled empirical exit hazard from F2 −2/−1/now
  (±1yr smoothed, age≥26 eligible, youth floored); per-player haircut P·v, no named exits; aggregate
  +1/+2 vs F1's discrete X=207 rule.

## CONSTRUCTION CHOICES the owner's model settles (no HALT needed)
- Cohort bands (≤23 / 24–27 / ≥28) are the directive's own (age ≥~28 veteran, ≤~23 developing).
- Distributed-retirement FORM is owner-given (P(retire|age)·value, no named exits); P(retire|age) is
  *estimated from recorded F2 exits*, which "spread probabilistically across the age-eligible cohort"
  sanctions. No owner-unsettled choice was invented; nothing here rules or bakes.
