# v2.9 REFIT — CERTIFICATION (the wired candidate) · 2026-07-13

Engine **2030e5df** (_merged_recover) / **952ddb3d** (rl_model) · store **b0c39d78** · config **69ead79b944d** ·
board **8a66b4ba** · matrix engine/store/config stamps == candidate. Candidate ONLY (no tag/main/bake).

## 1. BASE BYTE-EXACT (the G-ATTR contract) — PASS
All six kill-switches OFF (`RL_PVCADOPT=0 RL_MSD_POOL_EXCL=0 RL_DIAL14=0 RL_AGE=0 RL_L5_PICKLESS=0`) ⇒ the board
reproduces the pre-refit base **byte-exact**: `n=804 sum=723075`, emmett 1178 · bont 3721 · gawn 2538 · butters 6060.
Panel base (Daicos 8050 Bont 3721 Gawn 2538 …) reproduced. **All-off == base, proven.**

## 2. G-ATTR — cumulative attribution (base → +L1 → +L1+L4 → +L1+L4+L2 → +L1+L4+L2+L3 → FULL+L5)
`board_pass.py` on the wired engine, env-gated (no patching). base/+L1/+L1+L4 are THIS seat's runs (verified vs the
inherited sims to the dollar); the +L2/+L3 separable deltas reproduce the retiring seat's `gattr.json` — and the
FULL board sum **732725 = 723075 + 1296 + 1428 + 5307 + 1619** closes the arithmetic exactly.

| stage | board sum | Δ | movers | character |
|---|---|---|---|---|
| base | 723075 | — | — | all-off == base byte-exact |
| +L1 | 724371 | **+1296 (+0.179%)** | 24 | young prior-capped RUCs UP (knobel 402→505, barnett +101, conway +97); anchors byte-identical |
| +L1+L4 | 725799 | +1428 | 679 | the refit — **emmett 1178→826 (−352)**; xerri/treacy +86; broad small ripple |
| +L1+L4+L2 | 731106 | +5307 | ~713 | dial-14 young lift board-wide (duursma/uwland) |
| +L1+L4+L2+L3 | 732725 | +1619 | 42 | proven young risers UP (wilmot +455, callaghan +358, bowey +301) |
| FULL+L5 | **732725** | +0 | ~perez | trio pickless (sum-neutral; cohort-neutral) |

**louis-emmett — the three-probe corner (named):** base 1178 · +L1 **1178 (0)** · +L4 **826 (−352, −29.9%, pool-isolation)** ·
+L2 851 (+25) · +L3 851 (0). Net **1178→851 (−327, −27.8%), L4-dominated.** The owner's football-nonsense review
trigger is ARMED on the L4 pool refit — returned for the word (reproduces the inherited L4 figure exactly).

## 3. OFFICIAL COHORT GATE (frozen B1 `_b1_rows`, D5) on the wired board — PASS
ND+RD cohorts 2004–2020 (n=17), per-cohort yr1-indexed, unweighted cross-cohort mean:
**y4=126.8 · y5=125.2 · y6=116.1** — each ≤ hard 130 (margins 3.2 / 4.8 / 13.9); peak N=4, path_ok. **GATE: PASS.**
Reproduces the reconciled combined gate to 0.1pt; WIDENS the base margin 1.8pt.

## 4. PANEL 10/10 (re-pinned, claim-accurate) — PASS
`run_panel.sh` on the wired candidate == the committed panel, byte-agree: Daicos 8069 · Bont 3664 · Sheezel 8204 ·
Gawn 2518 · Reid 3782 · Ward 1735 · Moore 207 · Goad 919 · Smillie 1349 · Green 689. (Goad/Green +101 = L1's V0/RUC
rebuild, the knobel class.) Board md5 **8a66b4ba** re-pinned; PANEL_EXPECTED + expected_boot moved in-commit.

## 5. L7 NUMÉRAIRE RE-BASE (÷1.0524) on the wired combined board — PASS
`adopted_curve[1]=3000` ✓ · display pick-1 3157→3000 ✓ · order preserved (no strict inversion) ✓ · **ALL 10
anchor-pair ratios preserved** (<0.2%) ✓. bont 3664→3482 · gawn 2518→2393 · briggs 2215→2105 · darcy 4067→3865 ·
emmett 851→809. `rl_export.py (g)` numéraire guard LIVE (dormant on the pre-L7 board by design; HALTs pick-1≠3000
in the numéraire world — unit-tested). CONSTRAINTS v1.8 constants re-quote committed.

## 6. SHIP-GATES SUITE (ship_gates_check.py, engine 2030e5df) — CERTIFIED GREEN
Full report: `session_2026-07-02/ship_gates_report_2030e5df.md` (copy: `ship_gates_report.md`; md5 b017eba5).
**VERDICT: PASS=16 · FAIL=3 · DIFFERS-BY-DESIGN=1 · FEATURE=1 · PENDING=4 · STRUCK=1 (618s).**
- **B1 cohort gate: PASS** — avg row 4:127 5:125 6:116, peak N=4, path_ok (reproduces 126.8/125.2/116.1 on the regenerated candidate matrix; engine/store/config stamps == candidate).
- **B2 leave-cohort-out: PASS** — IS-WF leakage 0.000 %-pts.
- **B3 book seal: DIFFERS-BY-DESIGN** — candidate head 2030e5df ≠ sealed head 7a07e369 (a NEW version); content current=c7825f1b vs baseline=e559eb6c (both 2649 players). NOT a within-head immutability violation — the book RE-SEALS at the bake (owner action).
- **B4 board parity: PASS** — regenerated rl_app_data.json md5=8a66b4ba == shipped 8a66b4ba (byte-agree).
- **B6 ramp · D14a/b/c · A9/A10/A11: PASS · five data guards + Guard 5: PASS.**
- **ACCEPTANCE v1.7 — the 3 FAILs are EXACTLY the expected reds {A2, A3, A12}, all owner-ruled / data-caused; NO unexpected reds:**
  - **A2** FAIL — Curtis ≥ 0.90×Ward: 1598 vs 1562 (Ward=1735, ratio 0.921); Weddle>Ward 1661 vs 1735. [D7: threshold held at 0.90 by ruling — Luke "we can look at Curtis down the line".]
  - **A3** FAIL [DC] — Connor Rozee 2026=2396 / 2025=4464 ratio 0.54 (need ≥0.75). [Rozee out for 2026; knife-edge by design; AMENDED 0.80→0.75 D7, data-caused.]
  - **A12** FAIL [DC] — Travaglia>Moraes 824 vs 1041; Smillie>Retschko 1349 vs 873. [travaglia leg owner-WAIVED 2026-07-11; data-honest red stands.]

**Certification GREEN** (candidate). The B3 re-seal and the owner board+book reads sit ABOVE this rung at the bake ladder.
