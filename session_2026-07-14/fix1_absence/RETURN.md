# RETURN — FIX 1 + THE ABSENCE TERM (Option C) · candidate

**TIER-1 CANDIDATE. NO BAKE. NO TAG. NO MERGE.** Main is RED (item 102); item 74 OPEN. The owner views the list.
Base = `addef03` (q97m freeze). File-disjoint from the CI job: `boot_guard.py` / `bootstrap.sh` UNTOUCHED.

- **branch**: `claude/damping-absence-penalty-us81yn`
- **head SHA**: `<FILLED AT PUSH>`
- **PR**: `<FILLED AT PUSH>`
- **board md5**: `e6a8e6efda796cbfb7620338c5b2c3ef` (was `3dc19fbb`)
- **book stable-sha256**: `2a2df435fad4784eee3bd1c36c5b8fd2bc24777bc8a86e1e9f147dc6d907a939` (was `d371a27c`; n=2649; REBUILT, not re-sealed — re-seal is an owner bake action)

## P0 — the three ablated boards (path-additive, order Fix1→Absence)
- **Fix 1 alone** (base→fix1): **+1171 num-SCAR** (278 movers: 166↑ 112↓) — reproduces R99.1's +1,171 exactly.
- **Absence alone** (base→abs): **−1836 num-SCAR** (17 movers). As a leg on top of Fix 1 (fix1→both): **−1977**.
- **Both** (base→both): **−806 num-SCAR** (285 movers).
- **path-additivity**: L1+L2 = −806 == total −806 → **max|Σlegs−total| = 0**.

## P1 — the complete affected-row list → `measurement/AFFECTED_ROWS.md` (committed), `board_deltas.csv`
**Jamarra Ugle-Hagan**: base **187** · (a) Fix 1 **466** · (b) Absence **187** · (c) Both **484**. Level 48.75→54.56(F1)→53.97(both).
The owner ruled 187 too low, ~1000 too high — **he lands at 484**, driven almost entirely by Fix 1 (the 3-game cold
cameo damped); the absence term nets his decay and adds essentially nothing (his decay already over-charges him).
- Fix 1 top movers: Wilmot −693, Rozee +531, C.MacDonald −518, R.O'Brien +348, **Ladhams −306** (M4, the 1-game-@97
  over-price comes out), Jamarra +279. M4 list in full in AFFECTED_ROWS.md.
- Absence term moves 19 players (down 17, up 2). Biggest: Bailey Smith −515, Tanner Bruhn −326, Logan McDonald −188.

## The double-charge split (per player: decay · new-term · total vs the measured curve)
- **NEW-TERM OVERSHOOTS: 0.** The new term never drives a player's total past the measured curve (it caps at the
  multiplicative truth via `min` and never lifts). Jamarra: decay −3.71 + new −0.60 = total −4.31 lvl == mult-truth
  −4.31 (NOT −3.71 + −4.31 = −8; the double-charge is avoided by construction).
- population mean: decay −0.79, new-term −1.72, total −2.51 lvl-pts (D2: decay −1.7, shortfall −3.2, truth −4.9).

## P2 — G-COHORT (B1, July-8 walk-forward, FROZEN suite) · hard 1.30 · **PASS x3, NO BREACH**
Candidate (engine fef5719d, store 340a7a32): y1=69840.0 y2=79466.3 y4=88352.1 y5=86910.6 y6=80533.1;
den=min(y1,y2)=y1=69840.0 → **y4=1.2651 · y5=1.2444 · y6=1.1531** (all ≤ hard 1.30). vs baseline
1.2601/1.2407/1.1521: moved +0.005/+0.004/+0.001 (toward, not through, the bound). **y1 denominator UNCHANGED
(69840) — the young were NOT cut**; the tiny rise is the year-4 numerator lifting (Fix 1). No breach → no STOP.

## P3 — guards + anchors
- **PICK 1 = 3000**: HELD (structural — PVC read from pinned `pvc_curve_L1b.json`; synths are gap-free & flat-games,
  so both levers are inert on the pick curve; rl_export numéraire guard PVC[1]==3000 passed).
- **A-BONT = 3482 ≥ 3392 (+10%): PASS** (Bontempelli unchanged by both levers).
- **A-PAIRS pair 2** (Reid/Bont) +3.0% → PASS (band ±10%). **pair 3** (Sanders/Bont) +10.9% → FAILS (standing
  failed read; Sanders above Bont — the PVC chapter). Note it IMPROVED from +13.7% (Fix 1 nudged Sanders −97).
- panel: 9/10 unchanged; only Reid moved (3594→3587, −7, 0.2% from Fix 1). run_panel RESULT FAIL is that one
  expected move (boot_guard PASSED — the candidate boots clean on the new pins).
- **ship_gates (candidate column): PASS=16 · B5/G-FLOOR FEATURE (60 floor-saves +2230 — IMPROVED, per R99.1) ·
  B6/G-MONO PASS (ramp monotone, no dips) · B2 leakage 0.000 PASS · B4 parity PASS (e6a8e6ef==e6a8e6ef) ·
  D14a/b/c PASS · B3/G-BOOK DIFFERS-BY-DESIGN (candidate head != sealed 2030e5df; re-seal is a bake action).**
- **The only FAILs are A2/A3/A12 — ALL PRE-EXISTING** (FAIL in the CONTROL/PREVIOUS columns too; the players
  Curtis/Ward/Rozee-ratio/Smillie/Travaglia are UNMOVED by both levers). My change introduces NO new gate break.
- A-PEAK: Butters 5688→5688, Holmes 6150→6150 (0% drop, «2%) PASS. A-GAWN: Gawn 2393 > Briggs 2105 PASS.
  A-FADE: Coniglio/Adams/Blicavs/Guthrie unmoved (flat at floor) PASS. A-DARCY 3865→3873 (+8, up) PASS.
- **THREE NARROWEST MARGINS (all PASS)**: A-BONT +2.6% (3482 vs 3392) · G-COHORT y4 2.7% (1.2651 vs 1.30) ·
  G-COHORT y5 4.3% (1.2444 vs 1.30).

## P4 — board + book REBUILT; re-pinned
- board rebuilt via `rl_export.py` (both levers ON): 3dc19fbb → **e6a8e6ef**; parity gate PASS (804 board == ev()).
- book rebuilt via `s4_matrix_M1v7.py`: stable-sha d371a27c → **2a2df435** (n=2649). NOT re-sealed (owner bake action).
- **re-pinned in `data/expected_boot.json`**: `engine_head` 2334f570 → **fef5719d**; `board` 3dc19fbb → **e6a8e6ef**.
  All other pins UNCHANGED (store/band/config/q97m/peak_model/pvc_snapshot/bust_prior/register/rl_model).
- ⚠ `expected_boot.json` is shared surface with the CI job (per the directive). No live conflict on this branch
  (built from addef03); flag a possible merge-time conflict on the two re-pinned fields.

## w(g) — the damping curve, and the owner constraint
| g | 0 | 1 | 2 | 3 | 5 | 8 | 12 | 22 |
|---|---|---|---|---|---|---|---|---|
| w(g)=g²/(g+5.8) | 0 | 0.147 | 0.513 | 1.02 | 2.32 | 4.64 | 8.09 | 17.41 |
**Does w(1)≈w(0)≈0 HOLD? Approximately, NOT exactly.** w(0)=0, w(1)=0.147: the 0→1 jump is cut **6.8×** (from
1.0 to 0.147) but is not zero. Playing one game is now worth 0.15 of a game's evidence, not a full game — the
inversion is shrunk, not eliminated (census item 88 agrees).

## Assumptions (law 5, NOT measured — DECLARED, flagged for the owner)
- **Multiple absences**: charged on the MOST-RECENT return only, ONE penalty (age-indexed, NOT scaled by gap
  length). A player who missed two separate times does NOT pay twice.
- **Fade**: the penalty is FULL in the return season and fades to 0 over **2** subsequent ≥10-game seasons
  (`RL_ABS_FADE_N=2`), so a re-established player is not penalised forever. R98.2 (smoothness) requires a fade of
  ≥2 seasons (a 1-season fade is a hard step). **Flagged case: Bailey Smith** — out 2024, back 2025@116 & 2026@122
  (career-best), age_pre 23. At fade 0.5 he still takes −515 SCAR. He is demonstrably re-established; the owner may
  rule the fade should be faster (or demonstration-conditioned). This is the sharpest law-5 judgment call.
- **Population (law 4)**: applied to NON-established players too (≥1 prior played season). The curve is CLAMPED to 0
  below age ~20 (D2's data-free extrapolation) — so a very young absentee is charged ~nothing; the trough is 22–24.
  323 gap players detected; 267 don't move (re-established, or curve≈0, or decay already ≥ curve).

## In plain terms
Fix 1 says: a season counts for how much football it actually is. One game barely counts, so a hot or cold cameo
can no longer whip a player's value around — Ladhams comes off a 1-game over-price, Jamarra climbs off a 3-game
crash to 484. The absence term says: missing a season should cost a returning player something, sized by his age
(worst in the developmental early-20s, easing in the prime, biting again past 30) — but only the SHORTFALL the
engine wasn't already charging through its recency decay, and only until he's played his way back. It never lifts
anyone and it never charges past the measured curve. The one honest tension is Bailey Smith, who missed a year and
came back better than ever; the model still docks him half a penalty, and that is the owner's to rule.
