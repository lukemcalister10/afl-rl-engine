# PLAN — Form-Conditioned Aging (Tier 3, READ-ONLY, MEASUREMENT ONLY)

Owner-fired 2026-07-15 (register items 161–162, "(i). Both in parallel."). Supervisor directive
`DIRECTIVE_form_conditioned_aging_T3`. **This PLAN is the first committed artifact** — the operational
definitions of "decline", the conditioning set, and the censoring treatment are fixed HERE, before any
estimate is computed (auto mode). Nothing wires; the owner rules on the return.

- **Base (STRICT):** commit `9be07b8e5939eeade71106ef1eaee112df183441` — chapter final head; the bake tags
  this same commit, so the data is identical either side of the bake.
- **Guard 5 (entry):** store `engine/rl_after/rl_model_data.json` md5 = `b1fd0bced30baa838325814c39d43233`
  → **PASS** (matches the pinned `store` in `data/expected_boot.json` at the base). engine_head `fc7045d6`,
  board `790136a3`. Computed on a read-only worktree at the base commit; artifacts commit to
  `claude/form-conditioned-aging-analysis-mjhiul`.
- **Time band:** 1.5–3 h confirmed. Effort High.
- **Fence:** read-only; writes only under `session_2026-07-15/form_conditioned_aging/`. No store/engine/
  config/board/gate/doc write, no wiring, no touching the bake or the prior-art branch.

---

## 0. THE QUESTION, in engine terms

The owner: veterans (Gawn 35, Bontempelli 31) "haven't shown any signs of dropping off yet — balance their
demonstrated lack of decline against their age meaning they probably might." Is the engine assuming fast
imminent decline for players who have not declined?

The engine's age path has two arms, both keyed on `age = year − _by`:

- **DOWN arm (already declining):** a player whose current level `Lc` sits `>DOWN_TOL(3.0)` below his banked
  level `Lo` is shed toward `Lc·_agemult2(age, lcr)`. `_agemult2 = _agemult(age)`
  (`30→0.73, 32→0.68, 34→0.62, 37→0.55`) `+ _fbump(age, lcr)`, an up-only form bump on level-above-
  replacement `lcr` (prior-art branch `…-5hi0xe`, already folded in). This arm is **already form-conditioned.**
- **UP arm (flat-or-rising) — the crux:** a player playing at/above his banked level carries the lift
  `(Lc−Lo)` forward at fraction `s = _S_AGE(age)`, where `_S_AGE = 28→0.151, 29→0.379, 30+ →0.0`. **At 30+
  the lift washes out entirely** (forward = `Lo`). Item 127 measured the UNCONDITIONAL 30+ residual and it
  is statistically zero (R102.2, the 30+ zero stands). The CONDITIONAL version — the persistence / decline
  hazard among 30+ players *who have not declined yet* — has never been measured. **That is this job.**

So "does decline arrive measurably slower for the no-decline-yet cohort" is, in engine terms: **conditional
on flat-or-rising form to date, is the age-30+ forward persistence still ~zero (decline hazard as high as the
whole cohort), or does the conditioning buy real runway the S_AGE 30+ zero and _agemult miss?**

---

## 1. DATA & PANEL

- **Source:** the 2652-record store list; each record carries `scoring = [{year, avg, games}, …]`, `_by`
  (birth year), `_retired`, `_has26` (has a 2026 row). 1909 records have a scoring history; season rows span
  2005–2026.
- **Demonstrated level** `L(t)` = the season `avg` for year `t`. Transparent, = "what he demonstrated that
  season." (The engine's `_lvlcurr` is a recency-weighted blend; we re-derive from the raw season series and
  cross-check the two named-anchor levels against the engine.)
- **Season age** `a(t) = t − _by`, floored per the engine's `_age_at` (`max(t−by, 18+(t−cycle))`). **Matches
  the engine's own age clock** (calendar age reached in the season year) so every comparison is apples-to-apples.
- **Qualifying season:** `games ≥ G_Q`. **Primary `G_Q = 8`** (a meaningful chunk of a season; avoids 1–3
  game cameo noise, consistent with the damping rationale). **Sensitivity: `G_Q ∈ {6, 10}`.**
- **Horizon / right-censoring at the boundary:** the last COMPLETE season is **2025** (668 rows). **2026 is a
  partial, in-progress season** (max 14 games, median 10 — mid-July 2026); it cannot judge a full-season
  change. So an observed transition `t → t+1` requires `t+1 ≤ 2025`. Conditioned seasons `t` therefore run
  through **2024**. The 2025→2026 step is right-censored (excluded from the primary hazard/Δ); 2026 partials
  appear ONLY as a "so-far" annotation in the worked examples, declared as partial.

## 2. OPERATIONAL DEFINITIONS (fixed here)

### 2a. "Decline" (the event)
A season-on-season demonstrated-level **drop beyond a declared noise band**:
> material decline at `t→t+1`  ⇔  `L(t+1) < L(t) − ε`, both `t` and `t+1` qualifying.

- **Noise band `ε = 3.0` avg points (primary)** — equals the engine's own down-side hold band `DOWN_TOL=3.0`,
  so "decline" here is exactly what the engine treats as a real drop rather than wobble. **Sensitivity:
  `ε = 2.0`, `ε = 5.0`, and a relative band `4%·L(t)`** (a 3-pt drop means more at 60 than at 110).
- "First material decline" = the first age `a∈[29,36]` at which a conditioned player-season declines.

### 2b. Conditioning set — "flat-or-rising form TO DATE" (declared)
A player-season `t` at age `a` enters the conditioned set iff:
1. **Established:** `≥ 3` prior qualifying seasons (a demonstrated record; ~ the engine's `PROVEN_N=4` spirit
   without over-trimming the elder tail).
2. **No drop-off yet — trailing trajectory non-declining:** `L(t) ≥ max(L_{prev1}, L_{prev2}) − ε`, i.e. the
   current season is at or above BOTH of the two most recent qualifying seasons (within the noise band). This
   captures "hasn't shown signs of dropping off," robust to a single wobble, and mirrors the engine's `Lc≥Lo`
   up-arm test rather than a career-peak test (an elite elder plateauing below his age-26 peak still counts as
   "not declining" — which is the owner's intent for Gawn).
- **Sensitivity on the conditioning rule:** (i) last-step-only `L(t) ≥ L_{prev1} − ε`; (ii) strict
  never-declined-from-running-peak `L(t) ≥ max(all prior L) − ε`; (iii) strictly-rising `L(t) ≥ L_{prev1} + ε`.
- **Rising vs flat split reported** (rising = `L(t) > L_{prev1}+ε`) so the owner can see whether "rising"
  buys more runway than "flat".

### 2c. Survivorship / censoring — the honest denominator (the heart of the job)
For each conditioned player-season at age `a`, the transition to `a+1` resolves to exactly one outcome:
- **CONTINUE** — plays a qualifying `t+1` with `L(t+1) ≥ L(t) − ε` (no material decline).
- **DECLINE** — plays a qualifying `t+1` with `L(t+1) < L(t) − ε`.
- **EXIT** — no qualifying `t+1`. Sub-classified:
  - **CENSORED (still-active):** the player is still active at the horizon (last qualifying season = 2025 and
    `_has26`, or has a 2026 row) → right-censored, at-risk but no observed event; kept out of the event
    numerator, reported separately.
  - **GENUINE EXIT:** left the competition after season `t` (no later qualifying season and not still-active).
    This is the survivorship trap: the worst decliners are cut BEFORE we see their decline season.

Because a genuine exit's intent (form-driven vs list-management/voluntary retirement of a still-good player)
is not observable, the hazard is **bracketed and both bounds reported at every age:**
- **H_lower (survivor-only):** genuine exits treated as censored →
  `hazard = DECLINE / (CONTINUE + DECLINE)`. Biased **low** (survivorship — the faders who exited are dropped).
- **H_upper (exit = decline):** genuine exits after a flat-or-rising season counted as decline events →
  `hazard = (DECLINE + GENUINE_EXIT) / (CONTINUE + DECLINE + GENUINE_EXIT)`. Biased **high** (some exits are
  voluntary/non-form).
- The truth sits between. A **list-management flag** is reported: of the genuine exits, how many left from a
  still-elite level (`L(t) ≥ REPL[pos]+15`, i.e. not a form collapse) — these are the ones most likely
  non-form, and they widen the gap between the bounds. Reported, not silently assigned.

`n` (CONTINUE / DECLINE / GENUINE_EXIT / CENSORED) is reported at **every integer age 29–36**.

## 3. ESTIMATION

For ages 29–36, on the conditioned set and (identically) on the unconditioned age cohort:

- **(a) Next-season Δ distribution:** `Δ(t) = L(t+1) − L(t)` over CONTINUE∪DECLINE. Report per-age
  mean, median, 10/25/75/90th pctiles, and P(Δ < −ε) (= H_lower). Bootstrap 95% CI on the mean/median.
- **(b) Hazard of first material decline:** H_lower and H_upper per age, with the CONTINUE/DECLINE/EXIT n.
- **Smoothing over age (CORE rule 7):** raw per-age point estimates (with n and bootstrap CI) PLUS a
  **local-linear / Nadaraya–Watson smooth over age** at the FINEST resolution the sample supports (Gaussian
  kernel; bandwidth declared; report the smoothed curve and the raw points together). **No wide bin reported
  as one number across a band.** Where an age slice is too thin (expected 35–36), it is pooled **deliberately
  and DECLARED** (e.g. "35–36 pooled, n=…") — never silently merged.
- **Persistence translation (engine-facing):** for the flat/rising-with-lift subset, the realized carry
  fraction `ŝ(a) = (L(t+1) − Lo) / (Lc − Lo)` (`Lo` = banked prior level, `Lc = L(t)`), smoothed over age, is
  laid directly against `_S_AGE(a)` (0 at 30+). The realized forward multiplier `L(t+1)/L(t)` is laid against
  `_agemult(a)`.

### Comparisons (both required by the directive)
- **(i) vs the age cohort UNCONDITIONED** — same ages, same outcome/censoring machinery, no flat-or-rising
  filter. Answers "does decline arrive measurably slower than for the cohort as a whole?"
- **(ii) vs the engine's current age path** — overlay `_agemult(a)`, `_agemult2`, and `_S_AGE(a)=0 @30+` on
  the measured curves; state where the engine over-/under-sheds the conditioned cohort.

## 4. WORKED EXAMPLES (owner-facing)
Gawn (35), Bontempelli (31), English, Heeney, Dale: each career `L(t)` trajectory plotted against the
conditional estimate for his age — "given his shown form, the data says his next season lands here ± spread."
2026 partials shown as annotation only.

## 5. PRIOR ART (read-only, report-only)
Branch `claude/form-conditioned-aging-decline-5hi0xe` read. **Report what it is and whether it is sound; do
NOT reuse its conclusions — re-derive everything from the committed data.** (First read: it is the origin of
the DOWN-arm `_agemult2`/`_fbump` decliner-shed already in the base engine — a different population and a
different question from the owner's UP-arm hazard. Full assessment in the FINDING.)

## 6. DELIVERABLES
Committed CSVs (per-age hazard both bounds + n; Δ distribution; conditioned vs unconditioned; worked-example
trajectories; sensitivity table), a FINDING, a one-page owner read, and a RETURN (≤30 lines: branch, head
SHA, PR number). **No recommendation to wire anything.**

## 7. THREATS TO VALIDITY (declared up front)
- Survivorship → the single largest threat; addressed by the H_lower/H_upper bracket, not a point estimate.
- Right-censoring of active elders (Gawn/Bont themselves) → excluded from the event numerator, reported.
- Conditioning-on-the-future: the conditioning uses only info through `t`; the outcome is `t+1`. No leakage.
- Small n at 34–36 → declared pooling + wide CIs, never a false-precise point.
- Position pooling → pooled (RUC/ruck thinnest, e.g. Gawn/English); a position split is reported where n allows.
- Level metric: raw season avg, not the engine `_lvlcurr`; the two named-anchor levels are cross-checked so the
  re-derivation is not silently off the engine's basis.
