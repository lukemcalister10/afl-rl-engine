# OVERHAUL SPEC v1 — the sequenced V0/PVC overhaul: aim-points, tags, sequence, owner decisions

**SEAT: FABLE · DESIGN ONLY — this document wires NOTHING. No engine load, no re-fit, no canonical/store/engine/board
touch. Its product is executed later, job-by-job, each scoped from this spec and gated the normal way.**

**STATE STAMP:**
`CANONICAL = main 7bc5726 (v2.5) · store e1b4d8bf · engine efea88e5 · board 7d1eeef8 · book seal 5799a9ce · tag baked-v2.5-2026-07-05 @ e1d8d78` ·
`THIS SPEC = docs/OVERHAUL_SPEC_v1.md on branch claude/fable-synthesis-overhaul-spec-pgfula (candidate; PR, no merge).`

**INPUTS (by branch NAME + SHA, per binding directive 2):**
1. **Evidence pack v2.5** — `claude/evidence-pack-v2-5-o4wcib` @ `2e369cb`, `evidence/pack_v2.5/` (EVID1 growth curve ·
   EVID2 compression · EVID3 flags · Part B coordinate confirm + absence-as-freshness). All numbers `[v2.5]`, re-runnable
   (scripts committed, relabelled to `efea88e5`).
2. **FABLE cold design review** — `claude/engine-cold-design-review-c62k2c` @ `283cd9b` (`review/fable_cold_2026-07-04/`:
   DESIGN_CRITIQUE + 26-entry RISK_REGISTER F1–F26). All numbers `[BAKED c47cb43d]` (pre-v2.5) — **report-only relative
   to v2.5 until re-stamped**; the scripts are committed and re-runnable.
3. **v2.5 fix delta** — `docs/` on `main` @ `7bc5726` (KICKOFF v8 · HANDOVER rev112 · DECISIONS v70 · ROADMAP v6):
   F1/F2 export bugs fixed, DPP stripped (0 `_fut`), phantoms scrubbed, Kako 2025 folded, off-by-one games fixed, the 34
   present-position reassignments applied, five single-source guards live.
4. **PVC derivation spec v1** — `claude/pvc-derivation-spec-17l4ly` @ `033b366`, `docs/PVC_DERIVATION_SPEC_v1.md`.
   Design core carried (§1.6 below); cohort start corrected; numbers/coordinates flagged for re-stamp on v2.5.

**IN PLAIN TERMS (top):** the plumbing is fixed — the board Luke reads is now the board the engine actually produces.
This document is the battle plan for the football work: it takes every confirmed problem (kids priced too hot, aging
stars squashed together, rucks priced blind to talent, injured players read as "fresh", and the draft-pick price list
still being an old-world relic), says for each one *what the fix should aim at*, *how we'll know it worked*, and *which
calls belong to Luke*, then puts them in the order that avoids re-doing work. Nothing in here changes a number on the
board — every actual change comes later as its own gated job.

---

## §0 — RULES OF THIS SPEC

**Tags (every item carries exactly one):**
- **survives-fix** — confirmed (or code-read) still present on v2.5; the work item stands as designed here.
- **confirm-with-a-number** — believed live, but the build job must open by re-stamping a NAMED measurement on v2.5
  before anything is built. The tag names the measurement.
- **superseded** — closed by v2.5 (or by an owner ruling); paperwork/closure only.

**Provenance (every basis labelled, KICKOFF binding directive 6):** `owner-seen` (Luke eyeballed it) ·
`re-runnable [v2.5]` (committed script, runs on the honest board) · `report-only [c47cb43d]` (measured pre-v2.5;
re-stamp before building on it). Report-only never sits in an acceptance criterion.

**Standing constraints on every downstream job:** single-source invariant (KICKOFF §0, five guards); candidate branch →
PR → cold audit → Luke's written bake word; name-collision guard (all per-player references keyed by store `key` —
`sam-berry` vs `jarrod-berry`, four Picketts, the Kings); statistics rule (finest resolution the sample supports +
smoothing; wide bins diagnostics-only; pooling declared, never silent); no unlabelled numbers; firm-requirement fixes
ship as PROPOSALS for owner ruling, never locked mechanisms.

**Thresholds in acceptance criteria are PROPOSED** (marked `[proposed]`) — the owner may tighten or loosen them; the
measurement itself is the binding part.

---

## §1 — THE CORE OVERHAUL ITEMS (OV-1 … OV-7)

### OV-1 · YOUNG-SLOPE FLATTEN — the highest-leverage shape fix
**Tag: survives-fix.** Basis: re-runnable `[v2.5]` (EVID1, `growth_curve/`) — reproduces on the honest board and is
marginally LARGER than the contaminated read (Δ +0.6 to +1.3 SC across ages 19–22 vs was).

- **The confirmed defect:** the forward-production projection over-projects young players — fine local-linear curve
  **+7.0% of base at age 19 → +2.5% at age 22**, zero-crossing at **24.7** (peak location right, `PEAK_AGE` defensible).
  This is a genuine growth-curve **shape defect**, not board contamination (that was the whole point of the re-run).
- **Design approach (aim-point):** re-derive the age-production growth law so the 19–22 slope flattens by the measured
  overshoot (~+4–7% of base at the young end, grading to ~0 by 24–25). Tune **off the production residual, never the
  value residual** (the value residual's level is convex band-optionality, not mispricing — EVID1's explicit warning).
  The fit target is EVID1's own primary artifact: the matched walk-forward production residual, local-linear (LOESS
  deg-1), 0.5-yr grid, adaptive bandwidth with per-age eff-n — i.e. the correction is derived at the same resolution
  the defect was measured at (statistics rule). The carriers to re-derive against it are the age-growth surfaces the
  band/level machinery reads (`_AGEMULT`, the age-curve family, the band's age conditioning) — WHICH carrier moves is
  the build job's first deliverable (a one-page attribution: which surface contributes what share of the 19–22
  overshoot), not something this spec pre-empts.
- **Interactions:** re-levelling young forward-production moves V0-adjacent quantities → couples into the PVC/V0*
  reconciliation channel (OV-5, P7c) and everything V0-denominated (retention R_SURF, B5 floor). It also moves the
  cohort growth curve that **B1 (the constitutional growth-law gate)** certifies — see OD-6: B1 must be *measured
  against*, never *tuned to*; if the honest curve breaks B1's written bounds, that is a frozen-gate re-sign for the
  owner (A7 precedent), not a knob-hunt.
- **Acceptance criterion:** re-run the EVID1 harness byte-identical on the candidate: production residual at every
  0.5-yr grid point in 19–22 within **±2% of base `[proposed]`** (was +7.0→+2.5); zero-cross stays in **24–26
  `[proposed]`**; old-age end moves only if deliberately targeted; horizon≥5 control preserves sign/shape; B1
  green-or-owner-re-signed; three-column movers list (the young cohort re-prices — every mover attributed).
- **Owner decision surfaced:** OD-6 (B1 exposure). No mechanism fork — the lever is unambiguous.

### OV-2 · AGING-ELITE COMPRESSION — localised fix, do NOT globally widen
**Tag: survives-fix.** Basis: re-runnable `[v2.5]` (EVID2, `compression/`).

- **The confirmed defect:** compression is **LOCALISED**, not global. Global scale is if anything expanded vs realised
  (engine p99/p50 13.01× on realised ~3.9×; spearman(peakP, peakV) 0.888) — **do NOT widen the scale**. The defect
  lives in the aging-elite locus (the pack's `age 11–15, recentP≥100` frame — career-depth, the Petracca/Bont
  regime, n=14): value spread **3.35×** on production spread **1.26×**, spearman(recentP, cur) 0.77, and retention (cur/peakV)
  swings 0.2–0.8 **unaligned with production** (top producers retain less than mid producers). RUC is the
  most-compressed position (index 2.47 — mostly the OV-3 plateau wearing a different hat).
- **Design approach (aim-point):** condition the veteran decline/retention on **demonstrated current level** (EVID1
  shape-verdict #3 says the same thing from the other side: a single unconditional age multiplier cannot serve elite
  survivors and washouts at once). Aim-point: for established veterans, the value trajectory tracks the demonstrated
  production trajectory — an aging star still producing 125+ holds proportionally more value than one producing 95,
  at the same age/tenure. **Statistics rule bites hard here:** the n=14 locus is a DIAGNOSIS cell, not a fit set. The
  fitted object must derive on the widest veteran frame that supports it (all established players above a declared
  tenure bar, level entered continuously — pooling declared), with the n=14 locus reserved as the acceptance PROBE.
- **What this is NOT:** a global scale change; a rebuild of γ/SCALE/WQ6; a fix that touches the young half.
- **Acceptance criterion:** re-run EVID2's `localise.py` on the candidate: locus spearman(recentP, cur) rises from
  0.77 toward **≥0.90 `[proposed]`**; locus value-spread/production-spread ratio falls from 3.35/1.26 = 2.7 toward
  **≤1.5 `[proposed]`**; retention becomes production-monotone within the locus (printed, eyeballed by owner); global
  spread stats (p90/p50, p99/p50, Gini, spearman) move by less than **±5% `[proposed]`** — the localisation guarantee.
  Named pair sanity (ID-keyed): Bontempelli (`marcus-bontempelli`, cur 3084, recentP 129.05 `[v2.5]`) vs Petracca
  (`christian-petracca`, cur 2414, recentP 107.19 `[v2.5]`) stays production-ordered with a production-proportionate gap.
- **Owner decision surfaced:** OD-5 (the conditioned-decline principle, plain-language). Depends on: retention/V0
  re-derivation sequencing (must land WITH or AFTER P7c, never before — §3).

### OV-3 · RUCK V0 DERIVATION — replace the talent-blind cap
**Tag: survives-fix.** Basis: re-runnable `[v2.5]` (EVID3 `flags/ruck/`); owner-seen (Emmett read; the 1.4 rung in force).

- **The confirmed defect:** under the 1.4×PVC cap the production-leg clamp is **talent-blind**: elite proven
  `max-gawn`·33·2010 (V0_unc 1232 → clamped **841**) ≈ unproven `mitchell-edwards`·32·2024 (1231 → **844**). Cap binds
  186/31 of 217 real rucks; proven still-scoring rucks (`sean-darcy`·38·2017 → rides 1.4×PVC; `reilly-o-brien`·8·2015
  → same) are pinned to the legacy PVC ladder, not demonstrated output; M3 partially rescues. The cap is a stopgap on
  a ratio of two wrong things (band-prior heat ÷ a position-blind pick curve).
- **Design approach (aim-point):** carry PVC spec §2d.5/P6 unchanged in design: the RUC cell of the outcome-based
  fitted object — **pooled establishment/trajectory SHAPE × measured RUC level** (the standing thin-RUC rule; decided
  RUC n≈41 `[report-only, 644d1254 census — re-cut on e1b4d8bf]` does not support an own curve), giving (i) the
  outcome-based ruck pick price and (ii) the ruck start-value level that replaces the capped prior. The cap dial then
  has nothing to cap against and retires with an obituary. Ruck-specific traps carried from the PVC spec: bimodal
  outcomes (Xerri-class late bloomers), late establishment must not read as bust inside short windows, and the
  **proven-ruck ordering requirement** this evidence adds: the derived object must separate demonstrated-elite from
  unproven at equal prior heat (the Gawn/Edwards axis) — i.e. the production leg must be allowed to breathe above the
  prior level for proven producers.
- **Acceptance criterion:** Gawn-vs-Edwards ordering restored (elite proven ruck prices above unproven same-V0_unc
  ruck by a margin the owner reads and signs); Emmett (`louis-emmett`) — on the honest board he is already **855**
  `[owner-seen, v2.5]` vs the owner's stated 650–800 band `[owner-seen, D13-era]` — the derived number lands inside
  the band **or the deviation goes to the owner as a named read** (his band may itself have been calibrated against
  the inflated board; OD-4 asks him to refresh it); A6 gate green; the ruck ladder re-printed three-column; Part-3
  sum-to-total guard PASS.
- **Owner decision surfaced:** OD-4 (pre-register derived-beats-dialled — now LIVE, because a rung (1.4) is actually
  in force; plus the Emmett-band refresh).

### OV-4 · M3 ABSENCE-AS-FRESHNESS — requirement FIRM, solution OPEN (owner rules)
**Tag: survives-fix** (the defect); the mechanism choice is deliberately NOT locked here. Basis: re-runnable `[v2.5]`
(Part B `partB/absence_freshness_v2.5.py`); coordinates confirmed on v2.5 (`_merged_recover.py:210–242`).

- **The confirmed defect (general, not anecdotal):** every zero-games established player receives a freshness bump via
  the M3 clock-pin: a zero-games season gives sit-fraction s=1 → maximum pinning → the age/tenure clock reads a full
  year younger → less age decay + level held at last-good seasons. `ev = w·click + (1−w)·pin`, `w = 1 − s·(1−M3_FE)`
  = 0.58 at s=1. Measured `[v2.5]`: Nicholas Martin (`nicholas-martin`) **+15.11%** (ev 3116 on click 2707) · Tom Green
  (`tom-green`) **+13.49%** · Jack Viney (`jack-viney`) **+26.74%** · Darcy Jones (`darcy-jones`) +19.70% · Josh Sinn
  (`josh-sinn`) +50.22% — and note Deven Robertson (`deven-robertson`, 4 games, s=0.64) **+46.22%**: the mechanism also
  inflates LOW-games established players, not only zero-games.
- **The FIRM requirement (for the owner to ratify as written law):** *an established player who did not play does not
  get fresher.* Absence must never increase an established player's price relative to the clock advancing normally.
  (The pin's legitimate job — prorating a genuinely in-progress season for players who ARE playing — is not the
  target.)
- **Solution OPTIONS (weighed; owner rules — none is locked by this spec):**
  - **(A) Establishment gate on the pin.** The clock-pin applies only below an establishment bar (e.g. `ns < N` or
    career games < G — bar to be derived, not invented); established players' clocks always advance fully; their
    in-progress-season *level* proration is untouched. — *Cheapest, most targeted; directly kills the Martin/Green/
    Viney class; risk: a cliff at the bar (must ride the G-NEW-4 continuity gate); leaves the Robertson partial-games
    class to the level machinery.*
  - **(B) Availability as data (cause-aware).** Per-(player, season) availability flag in the store (the F22 fix; LTI
    register becomes data, not gate annotations); injured/absent seasons advance the clock fully, and injury enters as
    its own priced channel (or haircut) derived from return-from-absence outcomes. — *The principled end-state; makes
    A3/A10-style gate bends unnecessary; cost: owner data work + a new derivation; slower.*
  - **(C) Bump cap (board patch).** Clamp `ev/click − 1 ≤ 0` for zero/low-games established players (or a small
    declared bound). — *One-line, immediate, reversible; crude: treats the symptom, leaves the clock lie in place;
    acceptable only as an interim patch if the owner wants the distortion off the board before the overhaul lands.*
  - **(D) Split the clocks.** Separate the biological/age clock (ALWAYS advances — a knee reconstruction does not make
    a player younger) from the evidence/level clock (may pin on missed play, holding the level read at last-good
    seasons without granting age credit). The pin becomes evidence-only. — *The cleanest mechanism story; widest blast
    radius (touches every M3 consumer: `_dev_advance`, peak_est, sit-out, staleness interactions); needs the fullest
    re-gate.*
  - **Recommendation:** rule the REQUIREMENT now (it is one sentence). Build **A** as the overhaul-candidate fix
    (bounded, targeted, testable), pre-commit **B** as the Chapter-3 end-state (it also fixes F22 and retires the
    LTI gate-bending pattern), hold **C** only if Luke wants Martin/Green/Viney corrected on the live board before the
    overhaul bakes, and treat **D** as the version A grows into if the split-clock proves necessary during build.
- **Acceptance criterion (mechanism-independent — binds whichever option is ruled):** re-run
  `absence_freshness_v2.5.py` on the candidate: for every zero-games established player, bump ≤ **0%** (the firm
  requirement, exact); the named set (Martin/Green/Viney/Jones/Sinn) printed three-column; genuinely in-progress
  playing players' proration unchanged (Robertson-class handled per the ruled option and printed); G-NEW-4 continuity
  green at the establishment boundary; B6 green.
- **Owner decision surfaced:** OD-1 — the headline ruling of this spec.

### OV-5 · THE PVC DERIVATION — carry the design core; correct the cohort start; re-stamp everything
**Tag: survives-fix** (design core) **+ confirm-with-a-number** (every quoted census/baseline number and code
coordinate — named below). Basis: the PVC spec itself `[report-only relative to v2.5 — designed against the v2.4-shape
world, store 644d1254]`; owner ruling on start-year `[owner-seen, ROADMAP v6]`.

- **Carried unchanged (the design core):** the estimand — one fitted object **F(v | log-pick, position × draft-age
  cell)** as smoothed quantile curves + establishment probability P_est, busts in-sample at 0; every downstream number
  (PVC price via WQ6, B5 floor via p5 generating rule, distribution-pricing tail, PICKEQ inversion) a functional of
  that ONE object; the two-part survivorship design; the pooling tree with pre-registered decision rule (eff-n≥35,
  ribbon test); the E-spot/E-disc/E-peak time-aggregation fork with the δ dial (D1); the validation design (A13/A14 as
  δ-calibration, out-of-sample cohort test vs the V1 model, named-anchor register D10); the leakage protections (harvest
  never reads `ev()`); the P0→P8 execution ladder with its abort criteria; the 11-entry decision register D1–D11.
- **CORRECTED — cohort start (owner ruling applied):** primary fit window = **2004–2018 drafts** (was 2006–2018 in
  spec v1). Rule: an entry is primary-fit-eligible **iff draft year ≥ 2004** — a 2004 draftee's rookie season is 2005,
  the first season the store's scoring rows cover, so his career is observable end-to-end; a 2003 draftee's 2004
  season is unobservable → **2003 = reference-only** (never in the fit; usable for era context). P1/P2 carry the
  owner's verification rider verbatim: *verify 2005-season-complete + no-other-reason* — i.e. assert scoring coverage
  is actually complete from 2005, and print any 2004–2005-draft entry whose early seasons are missing rather than
  silently including it.
- **FLAGGED — pending re-stamps on v2.5 (the confirm-with-a-number list for P1/P2):**
  1. **Store census re-cut on `e1b4d8bf`** — every count in PVC spec §2c.2/§5 was profiled on `644d1254`: 2,656
     records · 1,572 ND-with-pick · decided-cohort cell counts (MID ~270 … RUC ~41) · 175 missing `_by` · 391 pathway
     records · RD 693. The v2.5 bake scrubbed phantoms and fixed games — the counts WILL move; re-cut before fitting.
  2. **Code-coordinate re-check on `efea88e5`** — the spec's anchors are v2.4 line numbers; Part B measured
     `_merged_recover.py` +7 / `rl_model.py` −7 in the affected regions; re-grep every anchor (mechanical).
  3. **Phantom premise CORRECTED:** spec §1.7 assumed the 4 phantoms persist "keep-excluded". **v2.5 scrubbed them and
     sacrificed the calibration lift** (real McAndrew/Keane kept). P7's PICKEQ re-derivation re-pools IRE/MSD from real
     records only — the deliberate double-count is dead; the thin-pool consequence is printed for the owner rather
     than silently re-credited.
  4. **Ruck-cap premise updated:** spec §1.5 was written against the 1.73 rung; the rung in force at v2.5 is **1.4**
     `[owner-seen]`. D4's pre-registration is therefore live, not hypothetical (OD-4).
  5. **[AUDIT-EXPOSED] flags resolve:** the D13+D14 audit + the v2.5 bake happened; the spec's §5 exposure register is
     now a mechanical re-stamp, not an open dependency. The "bake lands before P-jobs" premise is satisfied.
  6. **At-draft position re-verify:** the 34 present-position reassignments edited PRESENT positions — P1 must assert
     the at-draft position field was not touched (conditioning integrity).
- **Acceptance criterion:** unchanged from PVC spec (per-job acceptances P0–P8 + the six abort criteria), with the
  re-stamps above prepended to P1/P2's acceptance and the 2004 window substituted throughout.
- **Owner decisions surfaced:** the carried D1–D11 register (headlined by D1 pick time-value = OD-2 here; D6 V0
  reconciliation = OD-3), plus OD-4.

### OV-6 · DPP FORWARD-ELIGIBILITY — close it
**Tag: superseded.** Basis: re-runnable `[v2.5]` (EVID3 `flags/dpp/` — store carries **0 `_fut` / 0 `_futpos` keys**;
population 94 → 0 by construction).
The v2.5 DPP strip removed the surface the finding lived on; the was-numbers (Σ dOPT +$5,953, Serong +$275) are
historical record. **Closure job:** CHANGELOG/ledger entry striking the flag; carry-forward note only — when the
transition model later populates the dormant `future_position` (Chapter 3), its spec must include (a) a deterministic
tie-break rule (the F21 lesson) and (b) a fresh eligibility-value measurement (the "~$0 median, real for ~20 swingmen"
DECISIONS v70 note is the starting read). No build work in this overhaul.

### OV-7 · ESTABLISHMENT-P — settled dead; strip, don't rebuild
**Tag: superseded** (as a modelling question). Basis: re-runnable `[v2.5]` (Part B: `P_HOOK=None` @ `rl_model.py:775`
is the last assignment; runtime `P_HOOK is None`, `PROD_GATE='off'` — genuinely inert, feeds no pricing).
Settled: do not rebuild. **Residual hygiene job (small):** per binding directive 7 (*retire a feature → delete, don't
disable*), strip the dead `P_estab`/`P_HOOK`/`PROD_GATE` machinery with an obituary + resurrection ref. Rides any
Wave-0/Wave-4 hygiene slot; zero board effect (asserted byte-identical before/after — that IS the acceptance).

---

## §2 — THE 26 COLD-REVIEW ENTRIES, TAGGED ON v2.5

Every F-number below was measured/stated at `[BAKED c47cb43d]` (pre-v2.5). Tags reflect the v2.5 world. Where the tag
is confirm-with-a-number, the NAMED measurement is in the disposition column and joins the Wave-0/2 measurement list
(§4). "Rides" = which overhaul work item absorbs it.

| F | finding (short) | tag | disposition on v2.5 · acceptance |
|---|---|---|---|
| **F1** | board export dropped 3 engine layers (`id()`-membership) | **superseded** | Fixed by the v2.5 F1 one-source rewire (`_REAL` keyed by `p['key']`, `_isreal(p)`); board verified faithful on all 5 panel anchors `[re-runnable v2.5, EVID2]`. Durable residual: **G-NEW-2 export↔engine identity gate** (Wave 0) so this class can never ship silently again. |
| **F2** | book built by a different engine (asc², deleted-cB) | **superseded** | Book rebuilt/sealed at v2.5 (`5799a9ce`); board/book/engine agree `[owner-seen + HANDOVER rev112]`. Durable residual: **G-NEW-1 book↔engine identity gate** (Wave 0). |
| **F3** | ONE price is structurally three prices | **superseded** | Corollary of F1/F2 — closed with them. The identity gates are the permanent fix; without them F3 is one namespace bug away from returning. |
| **F4** | no predictive-accuracy/calibration gate (C1/C2 PENDING) | **survives-fix** | THE gate-zero item. Rides PVC P0 (Wave 1): build the naive-baseline + V1-pick-model harnesses; gate Spearman/decile monotonicity. Frozen-gate rule stands: *if either fails, stop and re-scope before the PVC.* |
| **F5** | walk-forward book is walk-forward in data only (in-sample models) | **survives-fix** | Two-step: (1) immediate honest LABEL on the book ("as-of data, in-sample models"); (2) the C1/C2 harness + gate1's held-out protocol become the measured-skill surface. Full as-of retraining judged not worth the cost unless C1/C2 exposes material in-sample flattery — that number decides. |
| **F6** | future info leaks into book inputs (2026 positions, realized pick-equivalents) | **survives-fix** (narrowed) | The `_fut` channel is GONE (DPP strip). Still leaking: present-position-applied-backward and `_eff` realized-career pick-equivalents. Fix rides Chapter-3 transition model (position-as-of-Y history) + PVC P7 (PICKEQ re-derivation makes the pick-equivalent channel explicit). Book label (F5) covers it meanwhile. |
| **F7** | two sources of truth for career games (377 records ≠) | **confirm-with-a-number** | v2.5 fixed an off-by-one games class — whether the dual-source disagreement class is closed is UNMEASURED. **Measurement: recount `games` ≠ Σscoring on store `e1b4d8bf`** (one script, Wave 0). If >0 remain: derive top-level games at load (single source) + store-lint assert. |
| **F8** | pick-side scale = point-estimate stack (`_SCALE` 1.19×, tfade, synth-ISO) | **survives-fix** | The principled fix IS the PVC program: outcome-based pick prices (P3) + pole re-derivation from realized pick outcomes rather than synth-through-band, with jackknife stability per table. Rides P3/P7; the parked "1.19× revisit" closes here. |
| **F9** | owner dials live INSIDE measured tables (O1, KEY_FWD −1, cap rung) | **survives-fix** | Fix: a single labelled **OWNER_OVERRIDES layer** applied last, never in-table; board prints override-bound values (FLOOR-SAVES pattern extended). Rides P7 integration; OD-7 asks the owner to bless the relocation (his thumb becomes visible, not removed). |
| **F10** | frozen hand-coded tables, no re-derivation path | **survives-fix** | Fix: per-table derivation script + jackknife-by-cohort stability check, run at every bake. The overhaul re-derives the big ones (age curve OV-1, retention OV-2, ruck OV-3, PVC OV-5); the rule becomes bake process for the rest. |
| **F11** | train/inference feature skew (band queried on M1 features) | **confirm-with-a-number** | **Measurement: the skew report** — train-feature vs inference-feature distribution distance per cohort, plus band-output drift on the non-flat population `[v2.5]` (Wave 2). The number decides: retrain the band on M1 features at the re-bake, or accept with the report on file. |
| **F12** | era adjustment applied to some level surfaces, not others | **survives-fix** | Fix: ONE era policy, declared. The PVC ruler is already era-adjusted; the overhaul integration states the policy for level core + band training and documents the residual drift. Rides P2 (ruler) + P7. |
| **F13** | `id()`/exec-namespace duality as a systemic pattern | **survives-fix** (narrowed) | Sharpest instance (`_REAL`) fixed at v2.5. Remaining: exec-duality, `_PE_CACHE` id-keyed, unguarded double-load landmine. Fix: stable content keys + loud double-exec sentinel — rides G-NEW-5 (Wave 0). |
| **F14** | call-order-sensitive global clock mutation (`b6` side effects) | **survives-fix** | Fix direction: context-manager for clock state now; as-of-year as a parameter long-term. Schedule INSIDE the P7 integration window (the reconciliation work touches these paths anyway — cheapest moment). |
| **F15** | import-time build order load-bearing, unasserted | **survives-fix** | Fix: assert import-time table hashes (ISO/_POLE/_V0CURVE/R_SURF-as-applied) against committed seals — the engine-side analogue of B3. Rides G-NEW-5 (Wave 0). |
| **F16** | dead ISO line + two-sided "guard" sold as lift-only (RUC 0.821–1.367) | **survives-fix** | Delete the dead line; the lift-only-vs-two-sided question dissolves INTO the pole/ISO re-derivation (F8/OV-5) — the re-derived correction states its authority explicitly. Acceptance includes re-printing the iso factor table `[v2.5]`. |
| **F17** | engine's embedded falsifier is dead code (synth crashes on M3 path) | **survives-fix** | Fix: give `synth()` a games field; move the falsifier into ship_gates as a scripted gate. Wave 0 — cheap, and the overhaul NEEDS a live falsifier before re-fitting curves. |
| **F18** | season-progress dial exists ×5, one hard-coded (`SEASON_PROG=0.58`) | **survives-fix** | Fix: single source (env), derived everywhere; dial-coherence assertion at load. Rides G-NEW-5 (Wave 0). |
| **F19** | name-fragile seams + DOB-less recruits priced off the age-18 curve | **survives-fix** | Fix: key every seam by store `key` (shared lookup helper, F24); backfill `_by` or EXCLUDE DOB-less from age-resolved fits. Draft-age side rides PVC P1 (which re-counts missing `_by` on `e1b4d8bf` — the spec-v1 175 and review-side 302 were both `644d1254` counts); V0-curve side rides the OV-1/P7c re-fit. |
| **F20** | Kako patch lived only in the book harness | **superseded** | v2.5 folded Kako 2025 into the store (23@55.2) + the correction-sticks canary guards the class. Residual (tracked in DECISIONS, not this overhaul): close the owner-correction write-path loop. |
| **F21** | dual-position ties broke by sheet order | **superseded** | DPP stripped — every player one position, present==future. Forward note carried on OV-6: the transition-model spec must include a deterministic tie-break BEFORE `future_position` populates. |
| **F22** | injury/availability not a first-class dimension | **survives-fix** | The M3 finding (OV-4) upgraded this from design smell to measured mispricing. Fix: availability flag per (player, season) as STORE DATA (M3 option B's substrate); split R_SURF by cause where n allows; retire the LTI gate-bending pattern. Chapter-3 scale; OD-8 asks the owner to commit the data workstream. |
| **F23** | back/forward views ride broken semantics (2026-hardcoded `delisted()`) | **survives-fix** | Fix: Y-aware `delisted()`; label forward views as clock-rolls until the in-progress season is modelled at Y+1. Small; rides the P7 integration window. |
| **F24** | board-vs-gates matching conventions disagree (substring vs exact) | **survives-fix** | Fix: one shared lookup helper keyed by store `key`. Trivial; bundle with F19's seam work (Wave 0/4 hygiene). |
| **F25** | proration ignores per-club schedule (byes) | **confirm-with-a-number** | Never quantified. **Measurement: distribution of per-club rounds-played deltas at the 2026 cuts → implied shift in s/fE readings** (Wave 2, cheap). Build the per-club denominator only if the number is material; otherwise file the report and close. |
| **F26** | historical qualification cliffs: (5,5,5,5)→433 vs (6,6,5,5)→875, +102% | **confirm-with-a-number** | Mechanism confirmed present (staleness family untouched by v2.5; coordinates shifted +7 only). **Measurement: re-run `cliff_demo.py` on `efea88e5`** to re-stamp the magnitude `[was +102% @ c47cb43d]`. Fix: fractional season-qualification credit on the `ns` counter (the D10 f1 pattern, applied historically); guarded forever after by G-NEW-4. Rides Wave 3/4 as its own small candidate. |

**The five G-NEW gates from the cold review** (identity ×2, calibration, population continuity, dial/order coherence)
are adopted wholesale as the overhaul's instrumentation layer — they are invariant-shaped, cannot be re-fit to the
current state, and three of them (G-NEW-1/2/5) are cheap. G-NEW-3 IS the C1/C2 build (F4). Sequence: §4 Wave 0/1.

---

## §3 — FLAG-CLUSTER RESIDUALS (roadmap flags not yet confirmed on v2.5)

Per DECISIONS v70's own provenance note, these are report-only until re-confirmed on the honest board:

| flag | tag | the named measurement |
|---|---|---|
| **Elite KPF separation** | confirm-with-a-number | EVID2's transfer-elasticity harness cut on the KPF cell `[v2.5]`: value↔production elasticity + spread ratio for elite key forwards vs the MID reference. If the localised-compression read covers it (KPF inside the aging-elite locus), it merges into OV-2; if a distinct young/prime KPF signal appears, it becomes its own item. |
| **Pedigree-floor ordering** | confirm-with-a-number | Re-print the floor-saves list + B5 floor incidence by pick pedigree on `e1b4d8bf`; assert (or refute) the claimed ordering defect. Note: the B5 floor re-bases at P7c regardless — measure BEFORE that re-base so the defect (if real) informs the generating-rule re-run rather than being churned away unmeasured. |
| **M1 breakout under-crediting** (46 hits, 214.49 pts / $15,726 withheld `[re-runnable v2.5, EVID3]`) | confirm-with-a-number | The magnitude is stamped; what's missing is the DEFECT-vs-DESIGN verdict. **Measurement: out-of-sample follow-through test** — for historical M1-hit seasons, did SUSTAINED-classified breakouts realise their full (uncredited) level in Y+1/Y+2? If yes at high rate, S_M1=0.46 under-credits and re-derives (inside OV-1's growth work); if the withheld share tracks subsequent fade, the dial is right and the flag closes. Exemplars keyed: `sam-berry`·29·2021 ($932), `kysaiah-pickett`·12·2020 ($740). |

---

## §4 — THE RECOMMENDED SEQUENCE

**The ordering logic:** (1) instrument before you re-fit — the identity/continuity/coherence gates are cheap and every
later job leans on them; (2) the frozen gate text mandates C1/C2 before the PVC; (3) measurements and owner rulings
are the long poles — fire them early and in parallel; (4) everything that re-levels V0 (young slope, PVC/V0*, ruck)
must converge into ONE integration candidate so retention/floor re-derive once, not three times; (5) M3 is
mechanically independent — its RULING can land immediately even though its build rides the candidate.

### WAVE 0 — instrumentation + closures (cheap, parallelisable, no owner dependency)
- **G-NEW-1/2** book↔engine + export↔engine identity gates · **G-NEW-5** dial/order/table-hash coherence (absorbs
  F13/F15/F18) · **G-NEW-4** population continuity gate (±1-game perturbation sweep; the F26-class detector) ·
  **F17** falsifier revive (synth games field; falsifier into gates).
- Cheap measurements: **F7 recount** on `e1b4d8bf`.
- Paperwork closures: **OV-6** DPP strike · **OV-7** establishment-P strip (byte-identical assert) · F24 lookup helper.

### WAVE 1 — gate-zero
- **C1/C2 calibration baselines** (F4 = PVC P0). Abort rule live: either fails → stop, re-scope before the PVC.

### WAVE 2 — data, measurements, rulings (parallel)
- **PVC P1** hygiene with the **2004-window** rule + full census re-cut on `e1b4d8bf` + at-draft-position integrity
  check (post-34-reassignments) → **PVC P2** harvest + ruler reconciliation.
- Named measurements: **F11** skew report · **F25** per-club proration delta · **F26** cliff re-stamp · §3 flag-cluster
  trio (KPF, pedigree-floor — BEFORE any floor re-base — and the M1 follow-through test).
- **Owner ruling pack goes out** (§5): OD-1 (M3) and OD-2 (pick time-value δ) are the long poles — everything in
  Wave 4 that touches them waits on the rulings, so they ship to Luke NOW, with the Wave-2 numbers attached as they land.

### WAVE 3 — the derivations (two tracks + one small candidate)
- **Track A (growth):** OV-1 young-slope re-derivation (carrier attribution → re-fit → EVID1 harness re-run) and the
  OV-2 conditioned-decline fit (design + fit only; landing waits for P7c).
- **Track B (pick side):** PVC **P3** core fit → **P4** censoring extension (worst residual; fallback =
  decided-cohorts-only) → **P5** estimand aggregation + owner read (δ lands here) → **P6** ruck derivation (OV-3).
- **Small candidate:** F26 fractional-ns credit (independent of the curves; G-NEW-4 measures the improvement).

### WAVE 4 — ONE integration candidate line (the engine change)
- **P7a** new PVC object → draftval/rulers · **P7b** PICKEQ re-derivation (phantom-free pools) · **P7c** V0*
  reconciliation (per OD-3 ruling) + OV-1 young-slope landing + R_SURF re-derivation on the new denominator (OV-2
  lands here, conditioned decline + owner-override relocation per OD-7) + B5 generating-rule re-run + A5 re-base
  proposal · ruck cap retirement (with P6) · **M3 fix per the OD-1 ruling** · F14/F23 riders.
- Full gates three-column at every sub-stage; every mover attributed player-by-player; scoped cold audit follows.
- Sub-stages are independently gateable IN THIS ORDER — a short session never leaves the candidate un-gateable.

### WAVE 5 — closure + re-bake
- **P8** paperwork (obituaries: SCALE_PVC staging, ruck cap, PVC v3.4; A13/A14 PENDING→live; UNRESOLVED strikes;
  V-D6 symptom re-measure) → owner's written bake word → re-bake via the owner's codespace → THEN Phase 2 (the
  calibration gate becomes standing) and Phase 3 (weekly loop + cockpit start their history clean, per the owner's
  overhaul-before-loop ruling).

**What to attack FIRST (plain):** Wave 0 + Wave 1 immediately (no rulings needed, everything downstream leans on
them), and the OD-1/OD-2 ruling pack to Luke in the same breath — his two answers are the schedule's critical path,
not any build job.

**Dependency spine (one line):** gates → C1/C2 → census/harvest (2004 window) → {growth re-fit ∥ PVC fit ∥ M3 ruling}
→ one P7 candidate (curve → PICKEQ → V0*/retention/floor + M3 + compression) → audit → bake.

---

## §5 — DECISION REGISTER FOR THE OWNER (plain language; recommendation each)

| # | the question (plain) | recommendation | what would change it |
|---|---|---|---|
| **OD-1** | **Injured players are being priced as if sitting out made them fresher** — Nic Martin is +15% for missing the year, Viney +27%. The rule I ask you to sign: *a player who didn't play doesn't get fresher.* Then pick the fix: (A) stop the "freshness clock" applying to established players at all; (B) start recording WHY a player missed (injury vs not picked) and price it properly; (C) a quick cap so absence can never add value, as a stop-gap; (D) rebuild the clock so age always advances and only the form-evidence part can pause. | Sign the rule now. Build **A** in the overhaul; commit to **B** as the end-state (it also fixes the "we bend the gates for every injured star" pattern); take **C** only if you want Martin/Green/Viney corrected on the live board before the overhaul lands. | Your read of the named-player table after A is built — if A's establishment bar creates ugly edge cases, D is the deeper rebuild. Sub-question: do you want the quick patch (C) NOW, or one clean change at the bake? |
| **OD-2** | **When you trade for a pick, what are you buying** — what the kid is worth next year, what he might be worth at his peak, or something in between you choose with a dial? (PVC D1, unchanged.) | In between (**E-disc**): the δ dial, defaulted so pick 1 lands square between your Wardlaw and Ashcroft reads, then shown to you as named-player consequences for signature. | Your read of the named-anchor table at P5 — you move δ, not the curve. |
| **OD-3** | **When the measured outcomes disagree with today's rookie start values, do outcomes win on the board?** This is the single biggest board-value mover in the program — it re-levels rookies, then retention and the floor re-derive on top. (PVC D6, unchanged.) | Outcomes win, phased through the one integration candidate with full gates + audit + your movers-table read. | If outcome-priced start values break your named reads, the reconciliation becomes a blend — and that blend is YOUR dial, printed. |
| **OD-4** | **Rucks: pre-agree that the derived curve beats the dialled cap.** The 1.4× rung currently in force is a tourniquet; when the outcome-based ruck derivation lands it will disagree with the rung by construction. Also: Emmett is **855** on the honest board — your old 650–800 band was set against the inflated board; does the band stand? | Pre-agree derived-beats-dialled (prevents a future dial-vs-derivation standoff); refresh the Emmett band on the honest board before P6 runs, so the acceptance anchor is current. | You deciding the rung should be permanent owner-law instead — say so and the derivation ships as a comparison view only. |
| **OD-5** | **Should an aging star's price keep tracking what he's still producing?** Today the machine squashes aging elites together — Bont producing 129 and a 117-producer can hold wildly different fractions of their peaks, unrelated to output. The fix makes veteran decline follow demonstrated form, locally, without touching the rest of the scale. | Yes — condition veteran decline/retention on demonstrated level; the global scale stays put (measured: the scale is NOT globally compressed). | Your read of the before/after veteran table — if a named veteran moves against your football judgment, the conditioning strength is the dial. |
| **OD-6** | **Fixing the kids may bump into a law you signed.** Flattening the 19–22 over-optimism changes the cohort growth curve that gate B1 certifies. Pre-agree the process: B1 is *measured against*, never *tuned to*; if the honest curve breaks B1's written bounds, we bring you the evidence and B1 gets re-signed by you (like A7), not quietly bent. | Pre-agree the process now — it's the same frozen-gate discipline you already ruled for A7/Guard-5. | Nothing foreseeable — this is process, not a number. |
| **OD-7** | **Your thumb-on-the-scale dials should live in one labelled place.** Today your overrides (the KPP floor rule, the KEY_FWD bar tweak, the cap rung) sit INSIDE tables that read as measurements — a future re-derivation would silently fight them. The fix moves them to one visible OWNER_OVERRIDES layer applied last; nothing about their values changes without your word. | Yes — relocate at the P7 integration; the board prints which values are override-bound. | You preferring a specific dial to become permanent law instead (then it's documented as law, not an override). |
| **OD-8** | **Commit to recording availability?** One data workstream — a per-season flag for why a player missed (injury / not selected / retired) — unlocks the M3 end-state (OD-1 B), retires the gate-bending-for-injuries pattern, and gives the LTI work its substrate. It's owner data entry, so it's your time we're spending. | Yes, as the Chapter-3 workstream; start collecting at the 2026 season boundary so next year's fit has one clean season. | If the data cost is too high, option A's establishment gate remains the standing fix — workable, just cause-blind. |
| **OD-9** | **The carried PVC governance forks, batchable in one sitting** (unchanged from the PVC spec): D2 the ~16% flag referent · D3 keep t^1.5 as your law vs archive snapshots · D5 mature-age curve crossings (test, don't impose) · D7 retire the legacy top-band anchor · D8 who sets deep-pick risk appetite (the visible ladder) · D9 pick 1 stays 3000 · D10 name 3–6 pick-for-player trades BEFORE the numbers print · D11 the book channel split. | Batch-sign per the PVC spec's recommendations (all still stand on v2.5); D10 is time-sensitive — the earlier your named trades land, the cleaner they are as validation rather than calibration. | Per-fork, as written in the PVC register. |

**The two critical-path answers: OD-1 and OD-2.** Everything else can land while builds run; those two block Wave-4
work packages.

---

## §6 — TAG COUNTS + THE MEASUREMENT LIST

**Counts** (core items OV-1…OV-7 + 26 cold-review entries + 3 flag-cluster residuals = 36 tagged items):
- **survives-fix: 22** — OV-1, OV-2, OV-3, OV-4, OV-5(core) · F4, F5, F6, F8, F9, F10, F12, F13, F14, F15, F16, F17,
  F18, F19, F22, F23, F24.
- **confirm-with-a-number: 7** — F7, F11, F25, F26 · KPF separation · pedigree-floor ordering · M1 follow-through.
  (Plus the OV-5 re-stamp bundle: census on `e1b4d8bf`, coordinates on `efea88e5`, phantom premise, cap rung, audit
  flags, at-draft positions — six named re-stamps riding P1/P2.)
- **superseded: 7** — OV-6 (DPP), OV-7 (establishment-P) · F1, F2, F3, F20, F21.

**Every named measurement in one list** (the confirm-with-a-number ledger; all `[v2.5]`, all pre-build):
1. F7 — recount `games` ≠ Σscoring on `e1b4d8bf`.
2. F11 — band feature-skew report (train vs inference distribution, per cohort + output drift).
3. F25 — per-club rounds-played deltas at the 2026 cuts → implied s/fE shift.
4. F26 — `cliff_demo.py` re-run on `efea88e5` (was +102%).
5. KPF — elite-KPF transfer elasticity + spread (EVID2 harness, KPF cell).
6. Pedigree-floor — floor-saves + B5 incidence by pick pedigree (BEFORE the P7c floor re-base).
7. M1 — SUSTAINED-breakout follow-through test (does withheld level realise in Y+1/Y+2?).
8. OV-5 bundle — PVC census re-cut (2004 window) · coordinate re-grep · phantom-free pathway pools · cap-rung update ·
   [AUDIT-EXPOSED] re-stamp · at-draft-position integrity.

---

## §7 — WHAT THIS SPEC DOES NOT DO

No engine loads, no re-fits, no wiring, no canonical/store/engine/board touch, no implementation code, no locked
mechanism for any firm-requirement fix (M3 ships as options; the owner rules). The per-item build jobs come later,
each scoped from this spec, each on its own candidate branch, each gated the normal way. Numbers quoted here carry
their provenance labels; anything `[report-only c47cb43d]` re-stamps before it is built on.

---

**IN PLAIN TERMS (bottom line):** five real fixes — cool the kids down (~4–7% too hot, confirmed on the honest
board), let aging stars be separated by what they still produce, price rucks off what rucks actually become instead of
a blind cap, stop absence reading as freshness (your rule to sign, your fix to pick), and replace the old-world
draft-pick price list with a measured one starting from the 2004 draft. Around them: seven things v2.5 already killed
get their paperwork, seven need one number re-checked before anyone builds on them, and twenty-two are confirmed work.
The order: bolt the safety gates on first, prove the engine beats a dumb baseline, measure, then derive, then land
everything that re-levels rookie values in ONE audited candidate so the floor and retention re-derive once. Two
answers from you unblock the heavy work: the injured-players rule, and what a draft pick is actually buying.
