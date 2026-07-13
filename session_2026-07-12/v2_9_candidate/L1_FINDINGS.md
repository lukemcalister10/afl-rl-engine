# L1 — PVC(b) + SMOOTHING FINISH · executed + verified · 2026-07-12

## What L1 is (corrected from the directive's framing)
"Adopt the derived levels" is **not** `RL_PVCFIT=1`. That existing lever swaps only `MA.PVC` (the
pick/trade **display** currency) and deliberately keeps `draftval` frozen on `_PVC0` to cut the
fit→board→fit circularity (`_merged_recover.py:986-992`) — so on its own it moves **zero players**
(verified: base vs `RL_PVCFIT=1` board = byte-identical, anchors + all 2652 rows). Full option (b)
— the owner's ruling D1(b) — additionally swaps the **ev-channel basis `_PVC0`** and rebuilds the V0
guard, V0 curve, and RUC ceiling grid; that is what re-prices the young prior-capped rucks. The
recipe is icbhpu `sim_option_b.py` STAGE 1.

## L1b — the declared smoothing pass (DONE)
- `scripts/pvc_smooth.py`: local-linear (LOESS deg-1) in log-pick, tricube weights, **h=0.20**;
  monotone (cummin) re-imposed; pick-1 pinned 3000. Chosen as the lightest touch that cuts the
  priced-range (picks≤50) max flat-run **9 → 2** while preserving the genuine −26% 5→6 concentration
  (26.5% → **25.8%**, owner-confirmed real, register v28 item 16 D1-ii) and G-MONO.
- Every deviation vs the raw isotonic is in **`out/pvc_smoothing_deviation.csv`** (max |dev| ≈ ±5%,
  all at the dissolved plateaus 6-9 / 15-18 / 32-40). Smoothed curve: `out/pvc_curve_smoothed.json`.
- Engine artifact rebuilt: `engine/rl_after/pvc_fit_candidate.json` (was the OLD discredited year-1
  W4 fit) → the smoothed derived curve, stamped non-bakeable (store b0c39d78).

## L1 verification vs the option-b oracle (`sim_option_b.json`) — read-only, `l1_adopt_sim.py`
The oracle ran the UNsmoothed curve at pin=3157; this build ran the SMOOTHED curve at both pins.

| metric | oracle (unsmoothed, 3157) | L1 pin=3000 (directive) | L1 pin=3157 |
|---|---|---|---|
| parity | 805/805 | **804** (= 805 − taylor-adams, removed in the b0c39d78 migration) | 804 |
| movers | 26 (RUC 24 / MID 1 / KEY_DEF 1) | **25 (RUC 24 / KEY_DEF 1)** | 25 |
| anchors byte-identical | yes | **yes** (bont 3721 · gawn 2538 · briggs 2222 · cam 1526 · darcy 4013 · butters 6060 · holmes 6270 · emmett 1178) | yes |
| board delta | +0.205% | **+0.179%** | +0.217% |
| knobel | 402→512 (+27.4%) | 402→505 (+25.6%) | 402→514 (+27.9%) |

**Verdict: PASS.** Anchors byte-identical (the load-bearing insulation proof — PVC never touches
player pricing). The 24 young-RUC mover set reproduces (knobel/barnett/conway/goad/green); the
1-row parity and 1 fewer MID mover are fully explained (adams removed; smoothing + pin). The
pin=3157 run matches the oracle within smoothing tolerance (knobel +27.9% vs +27.4%), confirming the
smoothed adoption is faithful.

## G-ATTR — L1's separable contribution
L1's per-row delta = base(b0c39d78) → +L1 = **exactly the 24 young prior-capped RUCs + 1 KEY_DEF**,
all UP (+13% to +26%); every anchor and every other row byte-identical. louis-emmett **UNMOVED** by
L1 (1178→1178) — his corner is L2/L4's, not L1's (three-probe attribution stays clean and separable).

## OPEN — for the ladder (not decided here)
1. **PIN CURRENCY: 3000 (ev-channel, directive "3000 stands") vs 3157 (display, ×1.0524
   re-denominated).** Materially sets the RUC mover magnitudes (board +0.179% vs +0.217%; knobel
   +25.6% vs +27.9%) and interacts with the v2.8 redenomination. Owner/supervisor word.
2. **The permanent lever is a real engine change** (un-freeze `_PVC0` + rebuild V0 scaffold/RUC grid),
   with the circularity the current design cuts. This session produced the EVIDENCE via the sanctioned
   read-only sim; wiring the permanent gated path (proposed `RL_PVCADOPT`) is staged, not shipped —
   it touches the V0 scaffold that feeds all player pricing and should land with the combined refit
   (L4) under the one-refit law, not as a lone edit.
3. PICKEQ pedestals: MSD 60→60 (no move), SSP 92→51 **HELD (L6)** — no pedestal ships in L1.
