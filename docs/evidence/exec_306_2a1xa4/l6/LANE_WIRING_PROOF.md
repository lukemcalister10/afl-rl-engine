# #306 L6 — THE LANE-WIRING PROOF (fire-order step 1) · **PASS**

Seam ruling 3 ([#306 comment 5186041140](https://github.com/lukemcalister10/afl-rl-engine/issues/306#issuecomment-5186041140)):
mandatory before new bytes; non-reproduction is HALT-and-file with both hashes.

## WHY IT IS NEEDED
`pooled_numeraire.py` resolves its harness by bare module name (`import harness_pvc as H`), and so do the
four fitters. Which copy loads is therefore a **routing fact**, not a visible argument — and a wrong
routing yields a plausible curve and a plausible convergence verdict, neither checkable. That is exactly
the risk the outgoing seat refused to take. So the lane is not asserted correct; it **reproduces a recorded
result** before it is allowed near new bytes.

## THE RECONSTRUCTION
- Lane dir holds `harness_pvc.py` = the re-pinned harness, **byte-identical to the tracked substrate file**
  `session_2026-07-30/item279_step4/scripts/harness_pvc_REPINNED.py` (verified by `cmp`).
- `PANEL` = the #279 panel from `…-4ql38z` (RETENTION-PROTECTED); its frozen `harness_pvc.py` verified at
  **`e0130cc22cdf9b43cb9d79f315a33a69`** and never on `sys.path`.
- Pin set to the record's own state at #290 L6 pass 0: `EXPECT_V0SURF = '96d671c952c8'`.
- Input: the **committed** `pass0_matrix.json`, md5 `9c4bca53b738452739c353d94fe99928`, store `81d24704`,
  sig `96d671c952c8`, 2,646 recs; ND-after-class-cut **re-counted here = 1,197**.

## THE RESULT — all four mandated targets, exact

| target | record | reproduced | |
|---|---|---|---|
| payload | `1a8db02b` | `1a8db02b` | **MATCH** |
| ladder total | 54,350 | 54,350 | **MATCH** |
| factor `s` | 0.998224 | 0.998224 | **MATCH** |
| pooled head pre-scale | 3005.3384 | 3005.3384 | **MATCH** |

**Ladder compared element by element: 64 of 64 identical, 0 differing picks, max abs diff 0.**
Payload independently recomputed from the reproduced ladder by the committed recipe:
`1a8db02b41326ed413d9ea4488f084c7` → `[:8]` = **`1a8db02b`**.

## VERDICT
**PASS.** The lane is proven by the record rather than by a seat's reading of it, and is lawful for new
bytes. Output kept beside this file as `lane_wiring_proof_output.json`.

## THE RE-PIN'S NON-VACUITY (fire-order step 2), proven on committed matrices

| pin | matrix (sig) | outcome | required |
|---|---|---|---|
| `8291668eff41` (old) | `pass0_matrix` (`96d671c952c8`) | `AssertionError`, names both values | FAIL — yes |
| `8291668eff41` (old) | `pass4_matrix` (`8291668eff41`) | LOADS, ND=1197 | LOAD — yes |
| `96d671c952c8` (new) | `pass4_matrix` (`8291668eff41`) | `AssertionError`, names both values | FAIL — yes |
| `96d671c952c8` (new) | `pass0_matrix` (`96d671c952c8`) | LOADS, ND=1197 | LOAD — yes |

**Both directions, before and after the move: PROVEN.** The asserts themselves were never touched; the
code diff between the re-pinned harness and the frozen `e0130cc2` is **three constants and the header —
no logic differs**.
