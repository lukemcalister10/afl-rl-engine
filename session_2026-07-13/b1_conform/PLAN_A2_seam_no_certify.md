# JOB A2 — FAIL-CLOSE THE RED-PATH SEAM (owner-ruled Option B) — PLAN

**Branch:** `claude/b1-conform-silent-gate-pgm98w` (continues PR #70) · **Effort:** Medium · **Mode:** auto
**Time band:** 30–60 min (confirmed).

## BASE VERIFICATION (done)
- Remote head `claude/b1-conform-silent-gate-pgm98w` = `193250fb38ef6571e8b48ff65f3e62f869194c23` (PR #70) — MATCHES.
- `main` diff since `c8631855` = `docs/OPEN_ITEMS_REGISTER.md` only — docs-only, PROCEED.
- Bootstrap Guard 5 PASS: store `340a7a32` == pinned. Board pin `3dc19fbb`.

## WHY
`SGC_B1_MATRIX` lets B1 read a caller-supplied matrix. `config_manifest.py`'s reject scan only polices
`RL_`/`PAR_`-prefixed vars, so `SGC_*` is neither cleared nor rejected in a bake/gate. A valid-meta doctored
matrix would ride into a BINDING gate and certify PASS. Owner ruled Option B: keep the seam (real red-path
proofs are worth having) but make it structurally incapable of producing a certification.

## THE THREE CHANGES

### 1. `ship_gates_check.py` — THE SEAM CANNOT CERTIFY (guarded by `INJECT_RUN = SGC_B1_MATRIX is set`)
- Loud banner at **top and bottom** of the printed board AND the report file:
  `INJECTED MATRIX — THIS RUN IS NOT A CERTIFICATION.`
- B1's verdict stamped **`INJECTED`** (never a bare `PASS`) in the board, report, and
  `data/gates_snapshots/` when the injected matrix is valid + non-breaching. (A breach/missing matrix still
  HALTs — HALT wins over INJECTED.)
- Suite **exits non-zero** whenever `INJECT_RUN`, regardless of gate results (`_hard_fail |= INJECT_RUN`).
- All new behaviour is gated on `INJECT_RUN`, so a **normal run (seam unset) is byte-identical** — same B1
  `PASS`, same report, same snapshot, exit 1.

### 2. `config_manifest.py` — THE BAKE DOOR IS BOLTED
- Add an `SGC_*` reject to `enforce()`. Fires when the **ambient** `RL_CONFIG_MODE ∈ {bake,gate}` (a real
  bake orchestrator / externally-driven gate). ANY set `SGC_*` var → named reject → HALT.
- Keyed on the **ambient** `RL_CONFIG_MODE`, NOT the `mode` argument: ship_gates_check calls
  `enforce('gate')` programmatically with no ambient `RL_CONFIG_MODE`, so dev-shell red-path proofs
  (breach/silence/A1) still run the suite (→ B1 INJECTED, non-zero) instead of dying at line one. A real
  bake sets `RL_CONFIG_MODE=bake` in the environment → dies on line one. **Verified, not assumed.**

### 3. `SHIP_GATES.md` — rewrite the RED-PATH TEST SEAM section
State plainly: the seam exists ONLY for red-path proofs; a run using it is NOT a certification and cannot
exit zero; gate/bake mode HALTs if it is set.

## PROOFS / ACCEPTANCE
- **A1** `prove_injection_cannot_certify.py` — clean valid non-breaching injected matrix → banner present,
  B1 `INJECTED`, suite exits non-zero. (Model on prove_breach_halts; skip B2/B3/B4 for speed.)
- **A2** `prove_bake_door_bolted.py` — `SGC_B1_MATRIX` set + `RL_CONFIG_MODE` gate & bake → config manifest
  HALTs with a named reject (stderr).
- **A3** re-run `prove_breach_halts.py` (update its CONTROL assertion `PASS`→`INJECTED`) + `prove_silence_halts.py`
  (unchanged — silence still HALTs). Both exit 0.
- **A4** normal run (seam unset): B1 PASS on July-8 (1.2601/1.2407/1.1521, den=y1=69,840.0), reds exactly
  {A2,A3,A12}, exit 1. Store `340a7a32` + board `3dc19fbb` byte-identical.

## LADDER
Tier-1-lite (owner-ruled). No merge, no tag. Ends on the PR #70 branch.
