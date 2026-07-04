# FLAG (c) — RUCK DERIVATION — FINDINGS

**State:** `[BAKED c47cb43d]` · main `389ac39` · READ-ONLY on engine/data
**Script:** `ruck_derivation.py` → `ruck_derivation.txt`, `ruck_binding.json`
**Dial:** `RUC_PRIOR_CAP = 1.40 × PVC` (baked default 1.73→1.4, v2.4 bake 2026-07-04)
`draftval(p) = MA.PVC[effpk]` is the **legacy pick-value curve (PVC)**; the cap value is `1.4 × PVC`.

## Rucks are a THIN slice — declared pooling

218 real rucks span only **76 distinct effective-pick cells**. The sit-out retention
surface `R_SURF['RUC']` is its **own** 4-knot (pick 5/15/30/50) × 6-depth grid — a
**deliberately pooled** low-resolution surface (the KPP retention floor O1 explicitly
**excludes** RUC; ruck runs its own capped machinery). **Said so:** ruck retention and
V0 are pooled/smoothed coarsely because the per-pick cell counts are too thin to fit
finely — one hot prior would otherwise set an entire cell.

## Part 1 — cap-1.4 binding set

| Set | binds | idle |
|---|---|---|
| All 218 rucks | **187** | 31 |
| **Active** (not delisted, ev≥250): 50 | **46** | 4 |

The cap binds on **almost every active ruck** — via the V0-prior leg (`V0_uncapped >
1.4×PVC`, tagged `V0`) and/or the production leg (`cap < e_prod ≤ V0_uncapped`, tagged
`P`). Only 4 active rucks are idle (their prior sits below cap): luke-jackson
(V0/PVC 0.92), lachlan-mcandrew (1.26), liam-reidy (1.27), will-green (1.03). Full active
table in `ruck_derivation.txt`.

## Part 2 — thin-cell top-of-ruck plateau

Every hot-prior ruck (`V0_uncapped > 1.4×PVC`) is clamped to **exactly 1.4×PVC** at the
V0 leg, so the top of the ruck board **collapses onto the PVC ladder — a pick-ordered
plateau, not a talent-ordered one:**

| ID · pick · cohort | V0_unc | → clamped | 1.4×PVC |
|---|---|---|---|
| louis-emmett · 27 · 2026 | 1559 | 853 | 853 |
| timothy-english · 19 · 2017 | 1368 | 1112 | 1112 |
| brodie-grundy · 22 · 2013 | 1247 | 904 | 904 |
| max-gawn · 33 · 2010 | 1221 | 836 | 836 |
| **mitchell-edwards · 32 · 2024** | 1219 | **839** | 839 |
| toby-nankervis · 35 · 2014 | 1164 | 801 | 801 |

Elite max-gawn (pick 33) and unproven prospect mitchell-edwards (pick 32) land at
**836 vs 839** — same pick band, so the cap makes them near-identical *regardless of
demonstrated talent*. **V0/PVC ratios span 0.18–3.47 (median 1.55)**; the cap (1.4) sits
just above the class median, so it bites the whole upper half. **112 of the 168 non-active
rucks** collapse onto a single PVC-floor cell (PVC 308 / V0_unc 479 / cap 431) — the
talent-blind pile the thin slice degenerates to.

## Part 3 — sit-out / penalty decomposition (name-collision guard + SUM-TO-TOTAL)

The four names disambiguate by ID (surname search is unsafe — "darcy" also matches
**darcy-fort** and **darcy-cameron** by *first* name; only **sean-darcy** is meant):

| ID · pick · cohort | ns_pro | path | e_prod → click → M3 → ev | Δcap+stale | ΔM3 | **rides PVC?** |
|---|---|---|---|---|---|---|
| will-green · 16 · 2024 | 0 | pure sit-out | 936 → 541 → 541 → **541** | −395 | 0 | **no** (V0-curve) |
| samson-ryan · 42 · 2021 | 2 | thin proven | 506 → 506 → 565 → **565** | −0 | +59 | **no** (cap idle) |
| sean-darcy · 38 · 2017 | 10 | proven, cap | 923 → 760 → 823 → **823** | −163 | +63 | **YES** (1.4×PVC) |
| reilly-o-brien · 8 · 2015 | 7 | proven, cap | 688 → 431 → 613 → **613** | −257 | +182 | **YES** (1.4×PVC) |

Every row **sums to total** through the full pipeline
(`e_prod + Δcap+stale + ΔM3 + Δfloor = ev`, **GUARD PASS** all four); the sit-out sub-term
`(1−λ)·R·v0_start + λ·e_full == click` also reconciles for will-green (541.5 → 541).

### Does the sit-out penalty still ride the legacy PVC scale? — **SPLIT: yes for the cap, no for the sit-out floor**

- **will-green** (`ns=0`, pure `sitout_ev`): `click = (1−λ)·R·v0_start`, λ=0 (0 games), so
  `= R·v0_start = 0.599 × 904 = 541`. His `v0_start` is the **D14 V0-curve** (pick-anchored),
  **not** the cap (his V0 1037 < cap 1403). His sit-out floor **rides the V0-curve, not the
  legacy PVC cap** — though the V0-curve is itself pick-anchored, so PVC only enters
  indirectly. Sit-out penalty = e_prod − sit-out = **−$395**.
- **samson-ryan** (`ns=2`, thin proven): cap **idle** (e_prod 506 < cap 699); value is his
  production, M3 lifts +$59. Does **not** ride the cap.
- **sean-darcy / reilly-o-brien** (proven, still-scoring): the **production-leg 1.4×PVC cap
  BINDS** — their click is pinned to `1.4×PVC` (760, 431), i.e. **literally the legacy PVC
  ladder × 1.4 × retention, NOT their demonstrated output** (darcy scores ~98/game, o'brien
  ~94). **YES — rides legacy PVC.** M3 then partially rescues them (+$63, +$182) because they
  sat out most of 2026 and the clock-pin values a younger-clock season higher; for
  reilly-o-brien M3 (+$182) nearly cancels the cap cut.

## What the flag costs, in $ (BEFORE-numbers)

- The cap trims **sean-darcy −$163** and **reilly-o-brien −$257** off their production value
  and re-pins them to the legacy PVC ladder; M3 gives back part. A cap-basis overhaul (PVC →
  demonstrated output) would move proven, cap-bound rucks by ~$150–260 each **before** M3.
- **will-green** carries a **−$395** sit-out penalty riding the V0-curve.
- The **top-of-ruck plateau** compresses the entire hot-prior cohort onto pick-banded
  values (gawn≈edwards at ~838), so relative pricing among the top rucks is currently
  **talent-blind** — the largest structural cost of the flag, though it nets to little
  absolute $ because it is a *reshuffle within* the capped band.

## Method notes

- Identity = **ID(key)·pick·cohort(debutyr)** on every row; the darcy/green/o'brien
  collisions are resolved explicitly.
- Pipeline stages are the engine's own exposed fns (`_ev_click`, `ev_prefloor`, `ev`),
  cache cleared between — the decomposition is the real evaluation, not a re-derivation.
- "Active" = not delisted and ev ≥ 250 (excludes the retired-vet scrap tail); full 218-row
  binding data in `ruck_binding.json`.
