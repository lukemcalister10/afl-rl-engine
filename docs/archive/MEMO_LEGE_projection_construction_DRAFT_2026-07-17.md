# MEMO — LEG-E PROJECTION-LAW + POSTURE CONSTRUCTION (DRAFT)
**v0.1 DRAFT** · 2026-07-17 · seat-12 pen (the Fable-assigned construction per SPEC v1.4 §3 Leg E)
**STATUS: DRAFT — NOT OPERATIVE. Nothing here rules.** Finalized and issued as the Leg-E directive
AFTER Leg D lands (picks price through the active lens ⇒ the lens consumes the NEW curve; any dial
line number below re-pins from the Leg-E base at issue). Feed: the job-6 rider @ `9845180` · SPEC v1.4
§3 Leg E + §6.2 · R103.3 · R104.4/R104.5 · LTI_REGISTER (Rozee) · register items 183 · 307/308 (noted,
out of scope). Owner parameters are marked **[OWNER]** throughout — proposed workflows, never numbers.

## 1 — WHAT LEG E IS (and is not)
Display machinery: the +1/+2 projection lens and the three posture profiles. **Values un-baked; the
BALANCED board remains the ONLY board that gates, bakes, or seals (R104.4).** UI and lenses never bake.
No new model, no new lever: a posture is a named vector over the EXISTING dial family; a projection
horizon is the SAME valuation map evaluated at a projected state.

## 2 — R103.3: THE PROJECTION LAW (the subtle half; the construction of record, proposed)
**The +1/+2 lens must show PROJECTED value with expected production CREDITED — not the
no-improvement floor.** Construction:
- For horizon +k, a player's projected level = the SAME un-compressed production map evaluated at his
  PROJECTED evidence state: age+k · expected games accrual per the availability layer (LTI truncation
  honoured — Rozee's 2026 stays at his real 2 games) · expected production per the map's own
  cohort/growth curves. **The Reid constraint: gap-year credit flows through the SAME map that prices
  everyone — no separate young multiplier, no lens-only growth term** (the ≤22 slope the base board
  carries is the slope the lens carries).
- The interim lens (no-improvement floor) RETIRES when this lands; the UI toggle re-enables ONLY on
  this landing (SPEC §3). Cross-age trades become readable off the lens for the first time — that is
  the deliverable's point (LENS-PROJECTION law, acceptance `laws[LENS-PROJECTION]`).
- **Laws that bind inside the lens exactly as outside:** L-SMOOTH (projection is continuous in age and
  evidence — no horizon cliffs), L-SYMMETRY (projected improvement and decline face the same
  evidentiary bar), weight-don't-gate (R105.4). A lens is a VIEW of the law, never an exemption.
- **Invariant (assertable):** at k=0 the lens reproduces the balanced board byte-exactly.

## 3 — POSTURES: THE PARAMETERIZATION (mechanics pinned from code at issue; rider Q2)
Profile = a named vector over the existing D5 dial family (`LENS = {now, bal, fut}`, at
`rl_model.py:397` on the groundwork base — **re-pin from the Leg-E base; the register's `:317` is
stale**, consumed `:425`/`:444`). Contender and rebuilder DO NOT EXIST in code (rider job-6 grep:
empty) — they are new VALUES, not new code paths. The Leg-E build's FIRST ACT (the measurement
discipline, again): read the dial's exact semantics from the code — which horizon each key discounts
or weights — and state it in the build's plan BEFORE any profile renders. The sketch (owner, adopted
R104.4): CONTENDER = current/+1 weight UP, future discount UP (`0.14 → 0.18–0.20 [OWNER]`);
REBUILDER = current weight DOWN, future discount DOWN (`0.14 → ~0.10 [OWNER]`).

## 4 — COMPOSITION LAW (rider Q3: one discount per axis, no double-count)
A 2027 pick under a posture = (the LIVE Leg-D curve over its band, lens-weighted like every future
stream) × (1 − R104.5 discount) applied ONCE as the FINAL step: `{balanced 0.10 · contender 0.15 ·
rebuilder 0.05}` EXACT (acceptance `leg_d_placeholders.posture_2027_discounts`). The lens `fut` dial
must not touch a pick asset a second time. **Assertable unit test:** a synthetic pick valued under
each posture shows exactly one discount application; committed with the build.

## 5 — INJURY × POSTURE (rider Q4; no mechanism pre-committed)
DEFAULT CONSTRUCTION: graded amplification for free — the existing B2/RL_AVAIL current-season haircut
composes with a contender lens's higher now-weight automatically; no new term. The owner's categorical
read (*a season-long-injured player's contender value ≈ trade value only*) is a **MAGNITUDE question
he rules at the movers report [OWNER]** with the named LTI rows in front of him — **Rozee (out 2026,
out_until_2027, A3 standing-fail scored-never-skipped) is the mandatory named case.** If his read
demands more than the free amplification delivers, that is a NEW ruling on the availability axis
(L-AXIS: cured where it lives), specced then — not smuggled into a lens weight.

## 6 — RATIFICATION + SEALING WORKFLOW (rider Q1/Q6; audit #31/#33)
1. Build implements profiles PARAMETERIZED, presets at the sketch strawmen.
2. **SEAL FIRST:** the preset vectors (hash + timestamp) recorded in the PLAN commit BEFORE any
   non-balanced report renders — the feedback path is the risk.
3. **THE MOVERS REPORT:** top-20 risers/fallers per lens vs balanced + the named LTI rows + every
   held pick per posture. Rendered, couriered.
4. **[OWNER] ratifies the §6.2 preset numbers at the report** (tuned from evidence, not a priori);
   ratified numbers re-sealed; only then are the profiles law. Only balanced ever gates/bakes/seals.

## 7 — OUT OF SCOPE, NOTED
Item 307/308 (season-leverage convex weighting + the scoped smoothness waiver) is POST-v2.11 and will
interact with the now-weight when specced — the Leg-E build must not anticipate it. SEASON_PROG stays
0.58 (item 297, owner dial). The dormant 15% alternate stream and §1b machinery: read-only to Leg E.

## 8 — FINALIZATION GATE (what turns this DRAFT into the directive)
Leg D returned + prescreened → re-pin the dial site and the curve artifact name from the Leg-E base →
fold any Leg-D construction consequences (the curve's band evaluation is the lens's pick input) →
issue as DIRECTIVE_LEGE with THE FIVE + strict base pin + the sealing workflow above.
