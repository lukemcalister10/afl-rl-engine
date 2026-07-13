# JOB A2 — FAIL-CLOSE THE RED-PATH SEAM — RETURN

- **Branch:** `claude/b1-conform-silent-gate-pgm98w` (continues **PR #70**; no new PR).
- **Head SHA (pre-commit base):** 193250fb38ef6571e8b48ff65f3e62f869194c23 — this commit lands on top.
- **Effort:** Medium · **Time:** ~40 min (within the 30–60 band).

## Acceptance (all four PASS)
- **A1 — the door cannot green-light.** `prove_injection_cannot_certify.py` → **exit 0**. Clean, valid,
  non-breaching injected matrix: banner present (×5 in output), B1 CURRENT stamped **INJECTED** (never a
  bare PASS), suite **exits non-zero (1)**.
- **A2 — the bake door is bolted.** `prove_bake_door_bolted.py` → **exit 0**. `SGC_B1_MATRIX` set +
  `RL_CONFIG_MODE=gate` and `=bake`: config manifest **HALTs** on line one with the named reject
  `UNKNOWN gate-seam override SGC_B1_MATRIX=... must not be set in a real gate/bake run`.
- **A3 — existing proofs still pass.** `prove_breach_halts.py` → **exit 0** (control B1=INJECTED,
  breach B1=HALT+BREACH, non-zero); `prove_silence_halts.py` → **exit 0** (missing + unreadable both HALT,
  B1 named, non-zero). Fresh logs committed.
- **A4 — nothing else moved.** Normal run (seam UNSET): B1 **PASS** on the July-8 construction —
  y1=69,840.0 y2=79,298.2 … ratios **y4=1.2601 y5=1.2407 y6=1.1521**, den=min(y1,y2)=**y1=69,840.0**;
  reds exactly **{A2, A3, A12}**; **exit 1**; no banner; snapshot carries no injected flag (B1=PASS).

## Byte-unchanged
- Store **340a7a32** == pin · Board (rl_app_data.json) **3dc19fbb** == pin — both **BYTE-IDENTICAL** after
  the full normal run. Engine/config untouched (config hash 69ead79b944d).

## Changes (three, mechanical, all guarded)
1. `ship_gates_check.py`: `INJECT_RUN` (SGC_B1_MATRIX set) → top+bottom banner, B1 stamped INJECTED,
   snapshot flagged, `_hard_fail |= INJECT_RUN` (always non-zero). All gated → normal run byte-identical.
2. `config_manifest.py`: `enforce()` rejects ANY `SGC_*` when the **ambient** `RL_CONFIG_MODE∈{bake,gate}`
   (keyed on ambient, not the arg, so dev-shell proofs still drive the suite). Verified, not assumed.
3. `SHIP_GATES.md`: §RED-PATH TEST SEAM rewritten — proofs only, never a certification, cannot exit zero,
   gate/bake HALTs if set.

## Ladder / disposition
Tier-1-lite (owner-ruled). **Not merged, not tagged.** Ends on the PR #70 branch.

## In plain terms
The seam that lets a proof feed B1 a hand-made matrix can no longer be used to fake a green gate: any such
run screams "NOT A CERTIFICATION", stamps B1 INJECTED, and exits non-zero — and a real bake that even has
the seam set dies before the engine loads. A normal gate run is exactly as it was.
