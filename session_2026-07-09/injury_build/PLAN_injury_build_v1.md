# PLAN — CHAPTER-3 INJURY/AVAILABILITY BUILD — v1 · 2026-07-09 (auto-mode first artifact)

**Directive:** `DIRECTIVE_injury_build_v1` (tier 6, effort High, band 3–6h). **Mode:** auto (this PLAN is the
first committed artifact). **Base:** branch `claude/new-session-pjbof6` @ `b303795` (the #52 merge — store
`a2fbc9a0`, King/Murphy birth years FIXED). **Spec followed AS RULED:** `SPEC_injury_derivation_v1.md` @
pinned `d76e8dad` (PR #49), overridden by DECISIONS §33's eight rulings.

## 0. BASE VERIFICATION (done on entry)
- Fetched fresh. **Live remote `main` = `00d82dde`** = the stale v2.5 doc-refresh; it sits *behind* the #52
  merge (`b303795` is NOT its ancestor). My branch `claude/new-session-pjbof6` already carries `b303795`
  (post-#52, store `a2fbc9a0`, boot-guard PASS). **Base = `b303795`**, not remote main. REPORTED as drift.
- Store `a2fbc9a0` == pin. Panel 10/10. Baseline gates: **FAIL=3 (A2/A3/A12)** — the frozen expected reds;
  B4 PASS (regen fd90472c == shipped); B1 avg-peak row 1:100 2:116 3:121 4:130 5:128 6:120 7:107 (n=17).
- **43/43 register keys re-verified against the live store `a2fbc9a0`** (no drift; matches the spec table).
- **`_b2hc>0` set = exactly {nicholas-martin, tom-green}** — BOTH register names. So retiring `_b2hc` +
  register-driven availability moves ONLY register names → non-mover parity holds by construction.
- **Part-2 recount post-fix: 142 full-gap return cases** (spec found 184 on the old `e1b4d8bf` store; the
  King birth-year fix + leak-free recount lands 142 — a reported finding, not a discrepancy).

## 1. ARCHITECTURE (one coherent design; toggle-able; register-only movement)
The engine is a lever stack, each with an env kill-switch; "ALL OFF ⇒ byte-exact v2.5". Availability enters
the same way — as **new levers touching register keys only**, so B4/non-mover parity is by construction.

- **`RL_AVAIL`** (default `1`) — the Part-1 season-state + present-haircut layer (register-driven).
- **`RL_LTI_RETURN`** (default `1`) — the Part-2 return-season haircut arm (`lti_return_hc` column).
- **`RL_LTI_CLOCK`** (`pause`|`advance`, default `pause`) — fork-(i) L1c clock toggle for the R-i table.
- New levers ride as **code defaults**; they are NOT added to `data/model_config.json` at this candidate
  (the manifest doc: "change a value ONLY at a bake"). Config hash stays `d88404…` → Guard-5 config +
  config-manifest + ruling-config gates stay green. Fold-into-manifest is deferred to the owner's bake.
  New levers are NEVER exported in the gate-running shell (gate mode would reject an unknown ambient var).

## 2. TASK COMMITS (one PR)
1. **Register sidecar + pins (R-REG=R2).** `LTI_REGISTER.md` (spec schema, `key · player · section ·
   window_id · designation · status · returned_year · notes`; 43/43 store-verified). Pin its md5 in
   `data/expected_boot.json` (`register`), assert in `boot_guard.py`, seed in `bootstrap.sh`, row in
   `REQUIRED_INPUTS.md`, extend the lookalike tripwire to `LTI_REGISTER*`, stamp the register md5 into
   derived artifacts. Retire the un-keyed `LTI_REGISTER_2026-07-02.md` (SSI: one register file; its verbatim
   body + provenance fold into the keyed file). Build-time validator: HALT on unknown key; report-only on
   designation-vs-store anomalies (toby-conway last store yr 2024; oscar-steene no 2025 row — REPORTED).
2. **Retire `_b2hc` + obituary (R-B2HC).** Delete the inference (`rl_model.py:795-803`); the k=0 present
   haircut plumbing (`_proj_w4:431`, `_prod_floor_w4:456`, `rl_export`, `distribution_pricing`) is rewired
   to read `_avail_hc` (register-driven). `_b2hc` no store fields → **store md5 unchanged, no re-seal.**
   Obituary in `BOARD_LAYERS_OBITUARY.md`. Verify only {nic-martin, tom-green} move.
3. **Part 1 nerf (R-iv=season-state).** `RL_AVAIL`: register out-for-remainder names (all A + all B unless
   `status=returned`; R-iii binary default OUT) get a per-player effective season state at the proration
   seam — `_fEy(p,Y)=1.0` and the cp exposure/level clocks read "season complete" (kills the `/SEASON_PROG`
   gross-up; τ'/bars/λ re-price on final-games footing). The one new present factor = the lost-production
   term `_avail_hc = L_p = 1 − min(g₂₀₂₆/G_FULL,1)` (G_FULL≡cp.SEASON=22, asserted equal), feeding the k=0
   haircut that `_b2hc` used to feed. NO stacked multiplier; no τ'/M2 double-count. Section B = season state
   only, return arm structurally absent. `avail_nerf` attribution = ev(layer) − ev(layer-off), per player.
4. **Part 2 return pricing (R-v, R-ii).** Derive net-of-aging haircut from the 142 gap cases (E_aged = the
   store's non-gap same-age cohort; DECLARED confound: young nongap is development-selected). Kernel-smoothed
   over return-age, pooled RUC/KPP/nonKPP, local eff-n reported. **Young/speculative (age<24 or nqual<4) ⇒
   h=0, SHIPPED ZERO** (A-DARCY doctrine; raw young return ratio ≈1.0 = no ceiling dent; the growth-year cost
   is Part 1's, not double-charged). Established older = small net residual, capped, return-season only,
   decays to 0 next season. Applied AFTER KPFFIX as its own column `lti_return_hc` (G-ATTR). Fork-(v):
   exclude register-nuked seasons from the KPFFIX `LD` top-2 window, extend back cap +2, fallback-and-report.
   Fork-(ii): independent windows (McInnes/Hayes two rows) + report-only `repeat_lti` on-sight flag.
5. **R-i table (PROVISIONAL).** `RL_LTI_CLOCK` toggle: value every young register name (Darcy, Motlop,
   Flanders, Gibcus + any L1c-credited register name) under pause vs advance, delta, one driver line. Pause
   is a clean config default so an owner flip is config-only, not a rebuild. Owner confirms/flips before bake.
6. **Proofs.** Per-lever attribution (avail_nerf, lti_return_hc separable); non-mover parity (register-only);
   before/after exemplars (Rozee, Darcy, Nic Martin, Tom Green, McInnes, Hayes); G-COHORT/G-FLOOR/G-PEAK
   before/after (STOP-and-report if any moves materially, no self-remediation); A3 stays a DATA-CAUSED red;
   full suite green (verdict FAIL=A2/A3/A12 only) + panel 10/10 from a fresh bootstrap; CI green.

## 3. ACCEPTANCE TARGETS
- Suite verdict unchanged: **FAIL = {A2, A3, A12}** only; panel 10/10; B4 PASS (regen == shipped candidate
  board `data/rl_build/rl_app_data.json`, regenerated with the layer on and committed as a derived artifact —
  NOT a bake; the `board` pin stays the baked reference, candidate board md5 reported).
- Movement confined to register keys + their KPFFIX interactions; everyone else byte-identical.
- A-DARCY: triple-locus attribution (ceiling untouched · KPF-speculative untouched · availability real —
  avail_nerf on his 6 final 2026 games, lti_return_hc stated even if ≈0). A-FADE untouched.
- OUT OF SCOPE respected: no Law-2/PVC/frozen-gate-text edits; no second data copies; no force-push; no
  bake/tag/main. BUILD-REPORTED until supervisor prescreen; owner reads R-i + exemplars before any merge word.

## 4. RISKS / WATCHERS
- G-COHORT (§6.4): eight 2025-draft year-1 register names sit in the year-1 denominator; the nerf lowers
  their 2026 evidence → denominator down → ratio up toward the hard 130. Re-measure walk-forward with layer
  on; if it tips, STOP and report (remediation doctrine forbids blanket young lift / cutting survivors).
- Config gate: never export the new levers in the gate shell.
- B1/G-PEAK: register names in sampled cohorts could shift the avg-peak row; measure before/after, report.
