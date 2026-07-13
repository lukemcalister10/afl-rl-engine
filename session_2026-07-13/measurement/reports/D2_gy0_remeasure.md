# DELIVERABLE 2 — THE G-Y0 RE-MEASURE (feeds a ratification)
**Board of record: the TAGGED BAKED board 81e48293 (store b0c39d78).** Re-quoted in the NUMÉRAIRE (F=1.0524).
The original "first measurement" (`session_2026-07-13/v2_9_continuation/`) was **PRE-BAKE and PRE-NUMÉRAIRE**
(comp-weighted V0 > derived PVC in every band, +19…+281). This re-runs it on the current baked board so the owner
ratifies on current numbers.

## CONSTRUCTION (same as the original)
Per pick band: the **comp-weighted position-conditioned V0** (mean `v0_start` over real ND players whose recorded
pick falls in the band — the mean naturally composition-weights by the band's position mix) vs the **derived PVC**
over the same picks. Both `v0_start` (board V0 curve, `_merged_recover.py:851`) and `PVC` are engine-internal raw
values (RL_PICK1 = 3000 pin); both are put on the **same numéraire divisor** (÷F). The y0→wk1→y1-trough→y2-recovery
chain is read walk-forward off the official matrix.

## THE SEAM TABLE (tagged baked board, numéraire)

| pick band | n | comp-wt V0 | derived PVC | deviation | dev % |
|---|---|---|---|---|---|
| 1–3 | 69 | 2555.1 | 2454.7 | **+100.4** | +4.09% |
| 4–7 | 91 | 2025.6 | 1832.8 | **+192.8** | +10.52% |
| 8–12 | 114 | 1464.9 | 1418.2 | **+46.7** | +3.29% |
| 13–20 | 182 | 1107.4 | 917.9 | **+189.4** | +20.63% |
| 21–27 | 160 | 883.3 | 597.1 | **+286.2** | +47.93% |
| 28–35 | 180 | 753.4 | 569.7 | **+183.7** | +32.24% |
| 36–48 | 297 | 625.4 | 468.8 | **+156.7** | +33.42% |
| 49–99 | 477 | 528.6 | 307.6 | **+221.0** | +71.83% |

**All 8 bands: V0 > PVC.** Deviations **+47 … +286 (numéraire)**, widest at the **21–27 band (+286)**. Net
deviation +1,377. (Deviations are quoted as reported — the numéraire is a uniform ÷F, so signs and ratios are
invariant to it; the magnitudes are the original raw figures ÷1.0524.)

## THE CHAIN (walk-forward, numéraire)
y0 (V0 at draft) = **902** → y1 (end of calendar year 1) = **631** → y2 = **977**. The **y1 trough** and the
**y2 recovery** shape **HOLDS** (y1 < y0; y2 > y1) — the y0→wk1→y1-trough→y2-recovery chain the G-Y0 law describes
is intact on the baked board.

## DOES THE ORIGINAL CONCLUSION SURVIVE THE RE-BASING?
**Yes.** On the tagged baked board, in the numéraire, comp-weighted position-conditioned V0 **exceeds** the derived
PVC in **every** band — the original conclusion (V0 > PVC in every band, +19…+281) survives, with deviations now
**+47…+286** and the widest band still in the 21–30 region. The y0→y1→y2 chain shape holds.

**One nuance to record.** At the single pick-1 point (not a band), the comp-weighted V0 across all pick-1 players
(2831 raw / 2690 numéraire) sits ~5.6% BELOW the pick-1 pin (PVC[1] = 3000 raw) — busts drag the pick-1 V0 mean
below the 3000 anchor, and the V0 and PVC curves cross right at the very top. But every BAND aggregate (including
1–3) is V0 > PVC, because PVC falls faster than V0 off pick 1. This is a point-vs-band distinction, not a reversal
of the conclusion.

**Bottom line for the ratification:** the G-Y0 first measurement's finding is confirmed on the current baked numbers.
Report-only; no proposal.
