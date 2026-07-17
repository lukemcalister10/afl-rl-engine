# LEG D ACT-2 — PER-GATE VERDICTS (halt-not-warn; silence is a RED)

Base ACT-1 checkpoint `12a0761` · store `968de0c7` (UNCHANGED, read-only whole leg) · engine
`bea8fea8 -> 40f43772` · board `9829d01a -> 270a2c5f` · book seal `ef2fbf9c -> 745e3462` ·
curve `pvc_curve_v2.json` curve_md5 `89c14729` (R1 composed pathway; tau=0.12, nmin=35).

## THE RULED CONSTRUCTION — R1 (composed pathway), memo-C measured & rejected
- **R1** (year-0 point of the 2-D pick×career-year evidence-weighted NON-median fit; busts full
  weight, no threshold): **G-Y0 pooled 0.257% offline / 1.10% real-engine** — PASS.
- **memo-C** (two-ends blend, the named fallback): built far enough to COMMIT the comparison —
  **G-Y0 pooled 9.486%** → C FAILS the 2% gate (its evidence-end pulls the tail back to the old
  ~330 floor). **FALLBACK TRIGGER = null → R1 stands** (`out/job5_r1_vs_c.json`).

## THE GATES
| gate | rule | verdict |
|------|------|---------|
| **RL_PVC2=0 kill-switch** | board == `9829d01a` byte-exact | **PASS** (proven, dev-shell) |
| **G-Y0 pooled (R2, HARD)** | \|comp-weighted mean day-after V0 − curve\| ≤ 2% | **PASS 1.10%** (real engine, post-swap v0) |
| **R104.9 strict descent (BINDING)** | curve(p+1) ≤ curve(p)−1, p=1..79; all 15 shipped plateaus clear | **PASS** (0 violations on `_PVC0`) |
| **numéraire** | curve(1) == 3000 | **PASS** |
| **R104.5 posture discounts (BINDING)** | {balanced 0.10 · contender 0.15 · rebuilder 0.05} EXACT in every artifact | **PASS** (board `posture_2027_discounts`) |
| **ENTRY CLOSURE** | zero-evidence entrant's draftval == `_PVC0` == curve; content from outcomes | **PASS** (Jagga Smith pk3: 2675 == `_PVC0[3]`) |
| **stamp-assert-not-stale** | curve carries the store md5 it was derived on | **PASS** (`968de0c7`) |
| **pre-view-hash LAW** | MEMO/census/acceptance unmutated | **PASS** (`abe387d9`/`04b9350e`/`6b83e336`) |
| **one_source_selftest §(9)** | promoted job-5 harness — all above, halt-not-warn | **PASS** (in-pipeline) |
| **G-COHORT (SOLE hard halt)** | class-year sum ratio ≤ 1.30, y4/y5/y6 | _see ship_gates battery_ |

## THE G-Y0 DIAGNOSTIC (owner-viewing, REPORT-ONLY — NOT gated; CORE rule 7)
`out/gy0_residual_curve_v2.json` — the residual PER EXACT PICK, kernel-smoothed across picks.
Smoothed relative residual runs −4.5% (pick 1: curve pinned to 3000 above meanV0) to +3.2%
(deep tail). **No decile/band table is a gated or headline number.** The single POOLED number
(1.10%) is the HARD gate.

## THE TESTS (audits #34/#35/#44 — divergence is a reported FINDING with numbers)
- **Multi-start** (kernel bandwidth nmin ∈ {25,35,50}; pathway tau ∈ {0.08,0.12,0.25}): divergence
  vs shipped ≤ **2.24%** — the curve is STABLE across starts (a stability finding, not a divergence).
- **Prior-removed** (audit #44): zeroing the 1093 zero-evidence poles on the EVIDENCE end only
  (entry-end floor kept by design) moves the curve by **max 1 SCAR (0.21%)** — the evidence-end
  shape does NOT depend on the circular poles. **Non-circularity confirmed.**

## HEADLINE FINDING — the gate binds the pathway (honest, reported)
Under the owner's tight 2% gate, the composed-pathway construction's YEAR-0 point is necessarily
≈ the day-after V0: any MATERIAL trajectory pull (tau ≥ 0.5) breaches the pooled gate (measured:
tau=0.5 → 2.55%, tau=0.8 → 3.73%). So the pathway's development signal cannot move the entry price
by more than the gate allows — which VALIDATES the owner's "entry closure made safe, nothing leaks."
The SUBSTANTIVE re-derivation is the non-median / evidence-weighted / busts-full-weight method that
lifts the deep tail from L1b's flat **~334 → ~463** (tracking the day-after V0), clearing all 15
plateau violations. The pathway (full 2-D trajectory surface) is the object of the tests and the
diagnostic; its year-0 contribution is a bounded (~1%) refinement.

## THE FENCE — ev-channel ONLY (R3, owner-reconfirmed)
IN: `_merged_recover.py` RL_PVC2 block (`_PVC0` swap + V0 guard/curve/RUC-ceiling rebuild) ·
`pvc_curve_v2.json` · `rl_export.py` held-pick ladder + posture · `one_source_selftest.py` §(9) ·
board/book/`expected_boot` re-pin. **OUT (untouched):** the five `rl_model.py` `MA.PVC` consumers
(pickless :798 · pedestal :813 · `build_pvc_v34` :714 · `_natcv34` :834 · `pvc_snapshot` :515) —
they migrate in a separate pre-ladder build; the ACT-1 census is their map. Store · `docs/` ·
Leg-B dials · SEASON_PROG (0.58) · lens code — all untouched.

## BOARD MOVERS & NAMED ROWS (`9829d01a -> 270a2c5f`; `out/ledgers.json`)
22 active movers, all young/low-value LIFTING on the tail lift (Flynn Riley/Caleb May 412→620).
Established / litmus rows HOLD (ev-channel only): Daicos 8017 · Sheezel 7964 · Bontempelli 3897 ·
Sanders 3668 · Gawn 3416 · Reid 3348 · Petracca 2955 — all +0. **item-256 ledgers:** movement (22);
value-up/rank-down subset (1), POSITIONAL-rank tie-break. **A-PAIRS (L-AXIS, never conditioned):**
pair-3 Bontempelli 3897 vs Sanders 3668 = **+6.2%**, inside the v1.21 band (bont above sanders
0–10%); SCORED at the ladder, not targeted. Top-10 pick currency old→new breaks the L1b plateaus
(pick 2 3000→2779).
