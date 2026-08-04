# PASS 1 — THE ENUMERATED INSTALL SET, prepared and verified. **Not executed.**

**#290 L6, 2026-07-31.** Prepared by this seat; handed to the next. The tree is clean at pass 0 —
`L6_pass0_state.diff` verified byte-current, **nothing half-installed**.

## WHY THIS IS A PREPARATION AND NOT AN EXECUTION

The install is L1(b)'s enumerated same-commit set: **six files with interlocking derived hashes**,
where three hashes depend on the bytes of files written earlier in the same act. The runbook's own
words for this class are *"the risk is atomicity, not time."* A half-written install set is worse
than none, because the interlocks make a partial state look self-consistent in places.

This seat reached the end of its usable working span at this boundary. Rather than begin a
six-file interlocked act it could not finish and verify, it has **fully specified and pre-verified**
the act so the next seat executes rather than re-derives. Same call as the T1 boundary.

## WHAT IS ALREADY PROVEN — no successor need re-derive these

**The payload recipe (E.5 finding 4) is proven, not assumed:**
`md5(json.dumps(curve, sort_keys=True))[:8]` — **string**-sorted keys, **default** separators,
**`int(round(v))`** values (E.5 finding 7: `float(v)` gives a different hash). Verified by
reproducing the installed `e69a3f38` from the installed curve.

**Curve 1, computed and cross-checked against the lane's own report:**

| | |
|---|---|
| payload | **`1a8db02b`** (recipe and lane agree) |
| head[1..5] | `3000, 2999, 2864, 2425, 1892` · pick 64 = **215** |
| Σ(1..64) | **54,350** · strict descent verified across all 63 steps |
| `s` | **0.998224** · `pooled_head_pre_scale` **3005.3384** · `published_pin` 3000 |
| POOL at this pass | **233.4**, ci95 [205.6, 261.3], n=1,005 |

**Worth noting:** this head and pick-64 are **identical to step 4's converged curve** (`fd9e8b63`:
`3000, 2999, 2864, 2425, 1892`, pick 64 = 215, ladder 54,354 — Addendum D.1's erratum table). The
re-derivation on the ruled substrate is landing on step 4's converged shape from a different
direction, with a 4-unit ladder difference. That is corroboration, not a coincidence to wave at.

**The derivation input is now committed** (the generalised freeze law): `pass0_matrix.json`,
md5 **`9c4bca53b738452739c353d94fe99928`**, `store 81d24704 · v0surf_sig 96d671c952c8 · 2,646 recs`.

## THE SET, WITH CURRENT VALUES AND THE ORDER THE HASHES FORCE

Three of these hashes are computed **from bytes written earlier in the same act**, so the order is
not stylistic:

**1. `engine/rl_after/pvc_curve_v2.json`**
   - `curve` → curve 1 · `curve_md5` `e69a3f38` → **`1a8db02b`**
   - `numeraire`: `pooled_head_pre_scale` 3068.4647 → **3005.3384**; `s` 0.9776876364261254 →
     **full-precision 0.998224…**; `published_pin` 3000.0 unchanged
     (N14: the **measured head is primitive**, `s` is DERIVED at full precision, 6dp is presentation only;
     E6 binds `published_pin / head == s` to 1e-9)
   - `pool_value` 234.3 → **233.4** (the L6 re-measurement; the stop-point value was never a target)
   - `stamp.per_entrant_md5` `77eba4d3` → **`9c4bca53`** (8-char, per the asymmetric convention)
   - `stamp.store_md5` `81d24704` — **unchanged**, the store did not move
   - `derived_from` and `_working_substrate_note` → the pass-0 matrix and L6 pass 1

**2. compute `md5(engine/rl_after/pvc_curve_v2.json)`** ← depends on step 1's bytes

**3. `ui/release_pick_curve.json`**
   - `pick_curve_curve_md5` → **`1a8db02b`** · `pick_curve_file_md5` `cdc50a2f…` → **step 2's value**
   - `pool_value` 234.3 → **233.4** · `per_entrant_md5` `77eba4d3` → **`9c4bca53`**
   - `curve_source_store_md5` stays the **full 32** `81d2470440a8…` — *not* the 8-char form
     (E.5 finding 5: the convention is asymmetric and `one_source_selftest.py:527` compares one-sided `[:8]`;
     writing the full md5 into the 8-char stamp FAILS the check)
   - `_doc` rewrite

**4. compute `md5(ui/release_pick_curve.json)`** ← depends on step 3's bytes

**5. `data/release_contract.json`**
   - `pvc_provenance.curve_payload_md5` → **`1a8db02b`**, `_note` → L6 pass 1
   - **`contract_sha256` recomputed** — `release_contract.py:69`: sha256 over the body **excluding
     `contract_sha256` and `_doc`**

**6. `engine/rl_after/one_source_selftest.py`**
   - `_contract_md5` (`:490`) `ca2f2e87…` → **step 4's value** (it pins `ui/release_pick_curve.json`)
   - `_per_entrant_md5` (`:500`) `77eba4d3` → **`9c4bca53`**
   - `_curve_source_store` (`:499`) — **unchanged**

**7. THEN the refit**, R-H.2: `RL_V0SURF_REFIT=1 RL_BAKE_V0SURF=1 refit_v0surf.py --bake`.
   The curve has moved, so **the signature key changes** and the surface must be committed as
   bytes + md5 + its new signature key **before the engine loads it**. The lane re-pins
   `expected_boot.v0surf` itself — **reset both together** if a run is repeated (this seat's slip).

**8. THEN** the chain for G-Y0 → re-emit the matrix (backup → emit → capture → restore, restore
   md5-proven) → derive curve 2 → compare payloads for the fixed point.

## THE STANDING TRAPS ON THIS SPECIFIC ACT

- **C.1 will fire** if any `engine/forward_valuation` file moves — it does not here, but
  `expected_boot.v0surf` moves at step 7 and must be re-pinned inside the identity set.
- **C.2 is field-level**: byte-surgical replacement, one occurrence asserted per file, line count and
  byte length checked. A wholesale JSON rewrite is the T1 seat's recorded violation.
- **Sealed history**: `release_lineage.json` and `finalization_state.json` are untouched at every step;
  the ten historical `45b207c0` occurrences must remain 4|4|4 and 6|6|6.
- **R-J**: the capture refreshes in the SAME evidence commit as the install.
- **R-I**: fixed point = derived payload md5 == installed payload md5; bound 4 passes; exhausted →
  HALT and report with the per-pass record, never declare.
