# P3 — THE NON-AVX512 DELTA: board, pick curve, book, guards (the core of the job)

**Measured on the FROZEN engine `2334f570` (q97m LOADED). Native = Haswell/AVX2 (this box, the bake-box
analog). "non-AVX512" = an SSE BLAS kernel (`OPENBLAS_CORETYPE=Prescott`) + numpy AVX512 disabled — the
class of environment the CI red reproduces on.** Board builds saved as `boardA_native.json` / `boardB_sse.json`.

## 0. Is the board even movable after the freeze? — YES (this is the headline)
| board | md5 | moved? |
|---|---|---|
| native Haswell/AVX2 | `3dc19fbbf920958affe7c6a2be9697d2` (== pin) | — |
| SkylakeX (AVX512 BLAS) | `3dc19fbbf920958affe7c6a2be9697d2` | **no** |
| numpy-AVX512-off only (BLAS native Haswell) | `3dc19fbbf920958affe7c6a2be9697d2` | **no** |
| **SSE (Prescott)** | **`935c2c297288dd699584d5857305f32d`** | **YES** |

**The freeze did NOT make the board environment-invariant** — but the movement is narrow and attributable:
- **AVX2 (Haswell) == AVX512 (SkylakeX)** boards are byte-identical. Disabling numpy's AVX512 SIMD (BLAS
  unchanged) is ALSO byte-identical. **The board moves ONLY when the BLAS kernel drops to SSE (Prescott).**
- So, exactly as at the q97m-fit level (P4): **the mover is the OpenBLAS kernel *generation* (SSE vs AVX2/
  AVX512), NOT numpy SIMD, NOT the AVX2↔AVX512 boundary.** The 72 isotonic fits are fed by `np.dot`
  NW-smoother sums that route through OpenBLAS; on an SSE kernel those sums shift, the V0 curve shifts, the
  board shifts (`3dc19fbb`→`935c2c29`).
- **Severity read:** GitHub's modern fleet is AVX2+; across AVX2/AVX512 the board is STABLE here. The residual
  bites a runner only if OpenBLAS DYNAMIC_ARCH maps its CPU to an SSE-class kernel. That is the residual to
  chase — real, but narrower than "any two machines differ."

## 1. THE FULL BOARD — how many of the 804 move (not ten)
```
active players 804/804 common-keyed=804
SUM native=696248  SSE=696264  delta=+16  (+0.0023% of the board total)
MOVERS (v differs): 8 of 804
  delta range: min=+1 max=+4 sum=+16      |delta| histogram: {1:4, 2:1, 3:2, 4:1}
  largest movers by |delta|:
    brodie-grundy    3718 -> 3722  (+4)     max-gawn        2393 -> 2395  (+2)
    timothy-english  3132 -> 3135  (+3)     tom-de-koning   1626 -> 1627  (+1)
    will-green        655 ->  658  (+3)     taylor-goad      873 ->  874  (+1)
    mitchell-edwards 1550 -> 1551  (+1)     harry-barnett    634 ->  635  (+1)
```
**8 of 804 move, all by +1..+4 (max +0.458% rel; board sum +0.0023%). The movers are ALL rucks/tall**
(Grundy, English, Gawn, de Koning, Goad, Green, Barnett) — the cohort whose value runs through the RUC
ceiling + RUC V0 curve, i.e. the most iso-fit-sensitive path. The other 796 players (incl. the numéraire
anchors Daicos/Bont/Sheezel/Reid/Ward/Moore/Smillie) are byte-identical. This is the residual, and it is
real but small.

## 2. THE PICK CURVE — does it move? does pick 1 still price 3000?
- **pick 1 = 3000 on BOTH environments (`pick1_pvc=3000`).** ✅ The numéraire is the LOADED `_PVC0`
  (`pvc_curve_L1b.json`, RL_PICK1=3000) — env-invariant by construction; it is not fitted at runtime, so no
  BLAS kernel can move it. **The unit the board is quoted in does NOT drift.**
- **The pick-currency (pvc) is env-invariant** (loaded). **The V0 curve (fitted) MOVES at fine precision but
  NOT at display precision:** `v0_c18_sha` (hash of all 6 positions × 90 pts at 6-dp) native `30435406b1208fd7`
  vs SSE `85071d090e4b90ca` — **they differ.** But the sampled MID V0 picks (3-dp) are byte-identical, so the
  movement is concentrated in the RUC/tall positions — exactly the path that produces the 8 ruck board movers.

| pick | pvc native | pvc SSE | V0 native (MID) | V0 SSE (MID) |
|---|---|---|---|---|
| 1 | **3000** | **3000** | 3841.885 | 3841.885 |
| 2 | 3000 | 3000 | 3746.393 | 3746.393 |
| 3 | 2817 | 2817 | 3380.526 | 3380.526 |
| 5 | 2365 | 2365 | 3006.797 | 3006.797 |
| 10 | 1657 | 1657 | 2167.264 | 2167.264 |
| 20 | 1126 | 1126 | 1266.973 | 1266.973 |
| 30 | 822 | 822 | 982.453 | 982.453 |
| 50 | 473 | 473 | 693.046 | 693.046 |
| 70 | 343 | 343 | 602.543 | 602.543 |

**pick 1 prices 3000 on BOTH environments — the numéraire does NOT drift.** pvc and MID V0 are display-stable;
the residual lives in the RUC V0 sub-curve (`v0_c18_sha` differs). RUC ceiling grid (native): lo=957.06
hi=12549.22 mid=2859.20.

## 3. THE BOOK — does the walk-forward book move?
| book | B3 stable_sha256 | n |
|---|---|---|
| native (== sealed baseline) | `d371a27c787a34c93de18c1bcc824c63c63aadcaa68f8a0a4d9c7291871bc44f` | 2649 |
| **SSE (Prescott)** | **`98fc2a4f333f6417b14a6b461ed27370ffdf5398fbdde102a28791b94f3ff953`** | 2649 |

**YES — the walk-forward book MOVES across environments** (`d371a27c` → `98fc2a4f`). Same n (2649), same
mechanism as the board: `s4_matrix_M1v7.py` runs the same engine with the 72 iso fits, so on an SSE kernel the
ruck-affected rows shift and the stable seal changes. So B3 would read **FAIL (IMMUTABILITY VIOLATION)** if a
gate ran on an SSE box against the AVX-sealed baseline. (At fixed AVX2/AVX512 environment the book is stable —
this is the SAME SSE-only residual as the board.)

## 4. THE GUARDS — could any G-COHORT verdict flip?
The y4 margin is **1.2601 vs a hard 1.30 (~3.07% headroom)**; item-74 drift is 0.35–1.8%/player. Bound from
the measured board delta (`guard_probe.py`, native vs SSE):
```
BOARD SUM native=696248 SSE=696264 delta=+16 (+0.0023%)
movers=8  max_abs_delta=4  max_rel=0.458% (will-green)  mean_rel=0.1429%
named anchors: Daicos/Bont/Sheezel/Reid/Ward/Moore/Smillie UNCHANGED; Gawn +2, Goad +1, Green +3
```
**Verdict: no G-COHORT verdict is expected to flip.** The residual (frozen engine, SSE) is 8 movers, max
+0.458%/player, board sum +0.0023% — roughly an order of magnitude below the ~3.07% y4 margin, and well
below item-74's 0.35–1.8%/player (that figure was the *unfrozen* q97m drift; the freeze shrank the residual).
The movers ARE rucks, so the RUC cohort carries most of the shift — but +2..+4 on ruck values of 600–3700 is
≤0.5%, diluted across the cohort average, and cannot cross 1.2601→1.30. **Definitive test = re-run G-COHORT
on the SSE board** (a ~10-min ship_gates pass; not run — out of this fence's compute scope; flagged). Per
item-74, every guard was measured on sandbox-built boards (consistent, not verified) and must be re-measured
on a frozen build regardless.

## Bottom line
The board of record rebuilds byte-identically at fixed environment (A1 ✅), but it is NOT
environment-invariant: the residual 72 isotonic fits move it across BLAS-kernel generations. The freeze
closed the q97m mover; it did not close the residual. This is the next job — and it is OUT of this fence.
