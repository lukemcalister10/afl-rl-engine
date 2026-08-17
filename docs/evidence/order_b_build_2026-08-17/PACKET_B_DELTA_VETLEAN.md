# PACKET DELTA — ORDER B under the R-VETLEAN rulings (#334 c.5316404479)

Read this on top of PACKET_B_BUILD.md. Two owner rulings landed on the first build and both are now
wired. Prereg discipline held throughout: PREREG_B_A1 (the re-tune rule) and PREREG_B_A2 (the
measured-bracket step) were each pushed BEFORE the analysis they govern.

## 1. The flat terminal fade is DROPPED (as ruled)

Deleted, not disabled (obituary at the RL_O33 block in rl_model.py; resurrection ref 6a61029).
Stages re-map: 1 = ladder + s\* · 2 = +taper retirement (the candidate, default). **The star cut is
dead**: Bontempelli −208 → **+35**, Sinclair −208 → **+34**, Merrett −142 → **+5** (their only leg
is now the taper's ceiling credit). Non-tall veterans are untouched by construction — the fixed-level
MID sweep prints ratio 1.0000 at every age (ENGINE_CHECKS_B.json). The quality-conditional fade waits
for the exit-hazard order, as ruled.

## 2. R-VETLEAN — the softened ladder (lean over, not under)

The re-tune ran inside the fitted CI box (ρ0 ∈ [0, .08], g ∈ [.010, .045]) and needed the full
prereg'd machinery, honestly used: the offline replica transfer proved UNSTABLE across s\*
re-derivations (missed −0.07, then +0.07 — s\* lifts only the projection leg while veteran floors
bind, so the anchored instrument's anchor moves more than veteran marks), so B-A1's calibration
iteration produced a MEASURED BRACKET and B-A2 took its midpoint:

| point (ρ0, g) | s\* | tall survivor B at 27/28/29/30/31 | verdict |
|---|---|---|---|
| fit optimum (.030, .025) + flat fade (build 1) | 1.2988 | 1.01 / 0.93 / **0.83** / 1.00 / **0.83** | the ruled under-shoot |
| iter-1 (.050, .0125) | 1.3451 | 0.98 / **0.90** / **0.87** / 1.10 / **0.91** | calls dead, floor missed |
| iter-2 (.025, .010) | 1.1909 | 1.08 / 1.06 / 1.04 / 1.26 / 1.03 | floor cleared, **full-30 call RESURRECTED (1.335\*)** |
| **CHOSEN — B-A2 midpoint (.03625, .011125)** | **1.2678** | **1.035 / 0.983 / 0.949 / 1.170 / 0.955** | **every cell ≥ 0.945, NO call in either view** |

Chosen ladder (fraction of peak at ages 28–32): **0.964 / 0.918 / 0.864 / 0.804 / 0.739** (the
original fit: 0.970 / 0.917 / 0.843 / 0.755 / 0.657 — the head is nearly the fitted one, the slope
is softened inside the CI). Full-view cells at the chosen point: 1.01 / 0.99 / 0.96 / **1.235
(uncalled, CI-lo 0.936)** / 0.99 — the 30-cell leans over exactly as the preference ruling asks,
with ~0.08 of headroom below the measured call threshold. **The original 1.2–1.65 over-mark calls
are dead in both views.** Cells that could not reach 0.95: NONE under the chosen point (29 sits at
0.949, i.e. at the owner's "~0.95"); the bracket table above is the measured proof of the trade-off
space, and iter-1 remains the published alternative if the owner ever wants the 30-cell lower at the
price of 28/29/31 in the 0.87–0.91 band.

- s\* re-derived per point by the standing fixed-point discipline; chosen-point s\* = **1.2678**,
  anchor gate −0.09% (bound ±3%), log SSTAR_A3_out.txt.
- Star tier under the final build: 0.913\*/0.90/0.95/1.02/0.94 — the marginal star-27 under-mark
  call remains (it is the output-blind ladder on tall stars, present in every variant; the fade's
  removal returned the 29–31 star cells to 0.94–1.02).

## 3. Everything re-run on the final point

- **Identities**: default board bce0c65d, RL_O32=1 board 7802ee97, both byte-exact on the current
  tree; candidate **9d25c936**, deterministic ×2; ladder-leg board e2743190.
- **Day-0**: 89/89 byte-identical to the REPAIRED C32 prints. One infrastructure note, disclosed:
  Order D's landing (0e1187f) rewrote DAY0_32_FINAL.json with THEIR dial-on prints (deep sitters
  move by design under RL_O35), which fail-closed my emit 0/89 — this build's guard now points at a
  byte-carried copy of the repair board's own file (DAY0_32R_FOR_O33.json, extracted from 3e40344;
  md5 22a83e75). The assert's meaning is unchanged; nothing of Order D's is judged here.
- **Boards**: live 752,429 · C31 666,913 · C32-base 667,398 · **B-preview 688,047** (ladder leg
  −7,860 · fade 0 by deletion · taper +28,509).
- **Taper**: 407 ▼ inversions → 0; +5,290 ceiling-band level pts on 646 rows; lower bands untouched.
- **Standing suite** (O33M vs O32RFINAL control): no buy-red (max +7.7% vs the 14% line); the two
  inherited sell-reds improve (31-40 −12.9 → −12.2%, 41-64 −6.1 → −4.4%); V1 vantage spread 18.7 →
  23.6 pts (taper on late-band ceilings, reported).
- **Entry-year control**: yr0 0.00% everywhere; the same five yr1 cells breach ±1.5% (41-64 +1.9%,
  RD +2.9%, ALLPOOL +2.8%, SSP +4.3%, UNR +5.1%) and the stage-1 re-read attributes every one 100%
  to the ruled taper leg (ladder-only sits within ±0.7%).
- **Rank/continuity**: 27+ rank moves max 132 / mean 19.6; Spearman base→B 0.9933 (all 27+), 0.9901
  (tall 27+); KPF fixed-level sweeps smooth (max adjacent-age ratio step 0.15–0.19, the softened
  family's own compounding); MID sweeps identity.
- **Numeraire**: s unmoved; artifact byte-identical; the pre-anchor basis freeze stands.
- **Ledger/pages**: ORDER_B_MOVERS.json rebuilt (ladder + taper legs; fade column 0 by deletion);
  both pages refreshed (year-1: 86 of 120 rows unchanged; movers = taper leg + 17 year-1 tall rows
  on the disclosed W-A renorm reach).

## 4. Named rows — final vs build 1 vs base

| row | pos/age | base | build 1 | **final** | final legs (ladder/taper) |
|---|---|---|---|---|---|
| Wilkie | KPD 30 | 3,422 | 1,938 | **2,329** | −1,135 / +42 |
| McKay | KPF 29 | 1,636 | 1,005 | **1,157** | −514 / +35 |
| Andrews | KPD 30 | 1,521 | 919 | **1,119** | −416 / +14 |
| Battle | KPD 28 | 1,879 | 1,311 | **1,395** | −544 / +60 |
| Wright | KPF 30 | 1,531 | 950 | **1,151** | −392 / +12 |
| Curnow | KPF 29 | 1,297 | 810 | **936** | −396 / +35 |
| Bontempelli | MID 31 | 3,677 | 3,469 | **3,712** | 0 / +35 — star cut dead |
| Sinclair | SD 31 | 3,180 | 2,972 | **3,214** | 0 / +34 — star cut dead |
| Merrett | MID 31 | 2,542 | 2,400 | **2,547** | 0 / +5 — star cut dead |
| T.De Koning | RUCK 27 | 1,688 | 1,887 | **1,884** | 0 / +196 |
| Moyle / McAndrew / S.De Koning | | | | +129 / +113 / +54 | taper (+ small ladder legs for S.DK) |

B-A2 prediction scorecard: predicted cells 1.04/0.99/0.96/1.19(full 1.26)/0.98 vs built
1.035/0.983/0.949/1.170(full 1.235)/0.955 — every cell within 0.03, PASS with no iteration needed;
P-A1..P-A5 of B-A1: A1 ✓ (via the measured bracket), A2 ✗ (29 binds, not 28), A3 ✓ (30 highest,
uncalled), A4 ✓ (stars = taper legs), A5 ✓ (yr0 exact, same taper-attributed yr1 set).
