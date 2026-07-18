# LEG F1 — PHANTOM INTAKE — ENTRY PROOF (captured this session)
container: py3.12.3 numpy2.4.4 scipy1.17.1 sklearn1.8.0 · OpenBLAS 0.3.31 DYNAMIC_ARCH (Haswell) · dev-shell recipe

## GIT ANCHOR (the item-334 STRICT law) — PASS
- `git ls-remote origin claude/lege-projection-law-postures-63u283` → `cc58570a65616a643a5dcfc955a79f5a44dd5adc` == directive. **PASS (STRICT).**
- checked out `cc58570`; working branch `claude/legf-phantom-intake-build-dvbipz` (harness-assigned; the
  directive's `claude/legf1-phantom-intake-<suffix>` maps to this — same lineage base, docs stay on MAIN).

## HARD-OUT INTEGRITY ANCHORS (file md5 — NOT floating-point; must byte-match) — PASS
- store `rl_model_data.json` md5 = **968de0c7** == directive `968de0c7`. **PASS.**
- curve `pvc_curve_v2.json` file md5 = **56dd7a7b**; stamp.store_md5 = 968de0c7; payload stamp = 89c14729
  (per Leg E ENTRY_PROOF). **PASS.**
- engine `rl_model.py`=cc626d7d · `_merged_recover.py`=6ad07bb2 · `rl_export.py`=9d58cc27 ·
  `distribution_pricing.py`=d0c8c69f (all == cc58570; byte-identical 7f77973→cc58570 for engine files).

## BOARD-HASH ENTRY ASSERTIONS — MISMATCH (environmental, uniform; NOT a code/data defect)
The FP-computed board md5 does not reproduce the filed absolute hashes on this container:

| env config (dev-shell) | THIS container | filed (directive) |
|---|---|---|
| RL_LEGE=0 RL_PVC2=1 (balanced k=0) | `30d96f1f` | `06d8af60` |
| RL_LEGE=1 RL_PVC2=1 (default / Leg-E lens) | `83a4b21d` | `d85901af` |
| RL_LEGE=0 RL_PVC2=0 (RL_PVC2 kill-switch) | `86444a70` | `9829d01a` |

### Root cause (proven, not conjectured)
- **Store + curve + engine files are byte-identical** to the directive (above) — the inputs are correct.
- Built at the five-migration EXIT `a90052a` (engine fdc54e24, the commit whose own ENTRY_PROOF filed
  `06d8af60`): this container yields **`30d96f1f`** — i.e. the *documented balanced board itself* does not
  reproduce here, independent of any Leg-E/Leg-F change.
- The **kill-switch equivalence reproduces exactly**: a90052a base board ≡ cc58570 `RL_LEGE=0` board, both
  **`30d96f1f`**. Every relative invariant the ledgers assert holds; only the *absolute* md5 is shifted.
- Mechanism: `numpy.show_config()` → `OpenBLAS 0.3.31 … DYNAMIC_ARCH` (runtime SIMD-kernel dispatch by CPU
  microarch). The filed hashes were minted on a different runner; last-ULP BLAS differences round a handful
  of `ev()` values to different integers → a different whole-board md5. The repo already names this hazard
  (`boot_guard.py`: "DYNAMIC_ARCH, not bit-stable").

### Consequence for this build
The Leg-F safety invariants are **relative** and fully provable on-container:
1. `RL_LEGF=0` reproduces this container's Leg-E state byte-exact (baseline `83a4b21d` default / `30d96f1f`
   balanced).
2. `RL_LEGF=1` adds only +k lens-scoped content with **0 k=0 `v`-movers** (the balanced board cannot move).

These are proven against the container baselines above. The absolute-hash gap is an environment/BLAS
reproducibility finding for supervisor reconciliation at the canonical runner — it does not touch code,
store, curve, or the balanced-board invariant. **Flagged, not silently absorbed (SILENCE IS A RED).**
