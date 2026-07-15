# PLAN — THE EVIDENCE WEIGHT `w`: FOUR REGIMES → ONE CONTINUOUS OBJECT
## Tier-1 writer · register item 124 · auto mode (this PLAN is the first committed artifact)
## Branch `claude/intelligent-lovelace-6v863q` · base pin `62352729` (STRICT, verified) · merge line `#82 → #83 → #85 → this`

### 0. BASE PIN — VERIFIED BEFORE ANY WORK
- `git ls-remote origin refs/heads/claude/absence-penalty-evidence-fade-glcl8b` = `62352729ec3523cec4bb117e713e1bec67a0d490` ✓ (full-URL).
- `git rev-parse HEAD` == `62352729…` after `checkout -B claude/intelligent-lovelace-6v863q 62352729…`. Engine file md5 `113a4223`.
- Boot-store Guard 5 PASS on the re-bootstrapped workspace (store `340a7a32` == pinned). Panel 10/10. Baseline ship-gates run committed (`ship_gates_BASE.log`; snapshot `gates_113a4223.json`).

### 1. THE FOUR REGIMES (exact sites at engine head `113a4223`)
All four are functions of the DISCRETE evidence count `n = _nqual(p,Y)` (count of seasons with `games>=10`) and `PROVEN_N=4`.
1. **10-game bar** — `_nqual` (`:143`): `sum(1 for x in p['scoring'] if x['games']>=10 …)`. Hard 0/1 at 10 games (census: 551 within one game).
2. **nqual ramp** — `_coreM1` (`:297`) / dormant twin `_lvl_eff_core` (`:184`): `c=n/PROVEN_N; c*Lc+(1-c)*par`. 25% steps (census: 545 at n=1–3).
3. **PROVEN_N cliff** — `_coreM1` (`:292`) / `:176` / `eff_ten` (`:170`): the `n>=PROVEN_N` FORMULA SWITCH — thin blend `→` established asymmetric, **the pedigree par VANISHES** (census: 253 at n=3→4). Item-65's diagnosis: "we smoothed the staircase and left the cliff at the top of it."
4. **exposure regime** — `raw_ev` (`:240`): `expgate = 1.0 if n>=PROVEN_N else min(1, _exposure/(POLE_RAMP*playable))`, `POLE_RAMP=22`. Hard `n>=4 → 1.0` gate on the pole-recovery credit.

### 2. THE ONE CONTINUOUS OBJECT
The unifying insight (item 65, verbatim): *the flattery decay and the nqual cliff are THE SAME LINE OF CODE — the weight on the pedigree par.* Replace the discrete `n` with ONE continuous evidence quantity `E(p,Y)` and derive every regime from it.

- **`E(p,Y)` — continuous evidence (games scale, per T5).** Smooth, cumulative, opportunity-aware. Built from the season game record with the STRICT small-sample form (D3): a 1-game cameo counts ≈0 (`ρ(g)=max(0,g−1)/((g−1)+k)`), so E replaces the `games>=10` bar without a threshold. Calibrated so E saturates over the **T5-measured 40–70 games** window.
- **Trust `θ(E)`** — production weight, `0 → 1`, saturating at 40–70 games (T5 shape).
- **Pedigree weight `pw(E) = r + (1−r)·(1−θ(E))`**, `r = 0.11` (T5's measured residual at n=4, CI [0.04,0.17], EXCLUDES ZERO — R98.5 the pedigree FADES, NEVER VANISHES). `pw(0) → 1` (pedigree carries the row); `pw(sat) → 0.11` (production rules, pedigree residual). Monotone, smooth, no branch (L-SMOOTH).
- The **established asymmetric machinery (M1 up-credit `S_AGE`/`TOL_M1`/`_radq`, decliner shed `_agemult2`) is UNCHANGED internally** (SCOPE EXCLUDES: S_AGE / L-SYMMETRY / `_eo`). Only its HARD GATE (`n>=PROVEN_N`) becomes a smooth maturity ramp `m(E)` on the same `E`, so the thin→established transition is continuous.
- **Level core** (replacing regimes 1–3): `core = (1−pw)·prod(E) + pw·par`, where `prod(E)` smoothly interpolates the thin production reference and the established M1/shed result via `m(E)`.
- **Pole gate** (regime 4): `expgate → eg(E)`, a smooth `0→1` ramp on the same `E` replacing the `n>=4` gate + `POLE_RAMP` bar; the D10 `_playable` proration is preserved.

### 3. THE A8 TRAP (Berry/Tsatas) — the recorded failure this design must clear
- Base A8 (raw ev): **Berry=2836 / Tsatas=1243 = 2.28×** (need ≥2.00×). Tight — Tsatas may rise only ~+150 num before breach.
- Tsatas (n=0, 4 list-years, 22 games): base `core=Lo=66.7`, `par=78.5`. The recorded failure (register `:285`): injecting the n=1 par asymptote lifted him +940 → A8 break. **The design must give Tsatas' 22 games of taken-and-not-converted opportunity ENOUGH evidence weight that pedigree stays near zero for him** — his failure to hold a spot IS evidence (production carries him), exactly as the current multi-year-n=0 path intends. `E` is therefore opportunity-aware, not raw-cameo-credulous.
- The symmetric risk (measured in attribution): a 0.11 residual on PROVEN ELITES pulls them toward par (Bont −3.85 level; Gawn/Daicos similar). This is the "leans-against-flattery" effect (item 66) but it can push **A-BONT** below its +10% floor and move **A-PAIRS**. This is where the directive's *"where Fix 1's directional-not-strict note bites, derive the strict form and show the delta"* and the model-split HALT valve live.

### 4. SCOPE — TOUCH vs KEEP
- **TOUCH (the four regimes):** `_nqual` (regime 1, at the level-core/pole sites), `_coreM1` regimes 2+3, `_lvl_eff_core` (dormant twin, kept in lock-step), `raw_ev` `expgate` (regime 4), `eff_ten`'s `n>=PROVEN_N` pole-side switch (same PROVEN_N cliff family, feeds the pole with regime 4).
- **KEEP (declared out-of-four, protective/eligibility gates, NOT flagged by the census; touching them risks the excluded scopes):** the `_nqual`-gated KPF partial-proven (`:571`), the speculative exemption (`:1200`), `_v7` form retention (`:316`). These are eligibility gates for specialised protections (A-DARCY ceiling etc.), not level-price regimes. If measurement shows one of them re-introduces a flagged discontinuity, that is a HALT-and-report (scope growth = new directive, S2).
- **EXCLUDED (other owners):** S_AGE + its 30+ zero · `_eo`/L-SYMMETRY · the absence term (#85) · anything PVC/pick-curve.

### 5. KILL-SWITCH & CONFIG
- `RL_EVW` — declared kill-switch (the #85 pattern), default ON in-code (`os.environ.get('RL_EVW','1')!='0'`). **NOT added to `data/model_config.json`** (exactly as `RL_DAMP`/`RL_ABSENCE`), so `config_sha256` = `c2d233ae…` stays UNMOVED. `RL_EVW=0 ⇒ w=n-regimes ⇒ byte-exact base board` (proven dev-shell, outside gate mode where the reject-scan lives). NO new env dials (item 114): every constant in-code.
- If the construction genuinely needs a config change → **HALT and report** (never move config silently).

### 6. ACCEPTANCE (assert `acceptance_v1_13.json`, never prose)
- Full ship-gates run: LOG + gates SNAPSHOT `data/gates_snapshots/gates_<newhead>.json` COMMITTED (item 121's lesson — the snapshot is a deliverable).
- G-COHORT (B1 July-8): regenerate; report y4/y5/y6 + margins to 1.30 (base y4=1.2660/y5=1.2477/y6=1.1588).
- A8 (Berry/Tsatas) BY NAME with values; must hold ≥2.00×.
- A-PAIRS measured + SCORED (pair 3 failure EXPECTED until the PVC cure — score, never skip). PICK 1 = 3000.
- `RL_EVW=0` reproduces base board md5 `24159c49` byte-exact (state both md5s).
- Committed AFFECTED_ROWS: every mover base→new, with evidence fields (games/nqual/proven_n/exposure) + separability line.
- Boot-store Guard 5 + five SSI guards green from fresh bootstrap; book re-sealed; expected_boot re-pinned (board + engine_head only; store UNCHANGED).

### 7. HALT CONDITIONS (do not ship a subset)
- If the four cannot be replaced in one motion (a subset smooths a counter but leaves a cliff, à la Variant A / the A8 break) → HALT + report.
- If the T5 residual on proven players cannot be reconciled with the binding anchors (A8, A-BONT, A-PAIRS direction, G-COHORT, A4) by in-code calibration of the curve shape → derive the strict form, show the delta, and HALT back to the supervisor (Fable) seat per the owner's model split.
- If a config change proves genuinely required → HALT.

### 8. STEPS
1. ✅ Base pin + toolchain + baseline gates + attribution (done; this PLAN commits them).
2. Implement `E`, `θ`, `pw`, `m`, `eg` behind `RL_EVW`; delete the four regimes (delete-don't-disable); obituary lines in the return.
3. Dev-shell ablation: `RL_EVW=0` byte-exact base (md5) ; `RL_EVW=1` new board dump.
4. Measure A8, A-PAIRS, A-BONT, A4, B1, A-FADE + full board movers; iterate the in-code constants to T5's shape while holding the binding anchors — or HALT per §7.
5. Full ship-gates (snapshot committed); AFFECTED_ROWS; book reseal; expected_boot re-pin; SSI guards; RETURN.

### FENCE
`engine/rl_after/_merged_recover.py` · data re-pins (`expected_boot.json`, board + `.srcmd5`, `book_stable_seal.json`) · `session_2026-07-15/evidence_weight/`. Store UNTOUCHED. Docs UNTOUCHED.
