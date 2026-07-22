# LEG F4 — EXIT PROOF · seat 13 · 2026-07-19 (single-thread OPENBLAS/OMP/MKL/NUMEXPR=1)
The L-SYMMETRY damper (MEMO_LEGF v1.3 §2.vii/§2.ix, owner ruling item 359). Base F3 exit `bccc231`. Store
`968de0c7` · curve `56dd7a7b` — ABSOLUTE, untouched. Touched set (⊆ the granted fence): `_merged_recover.py`
(the `:287-288` b6 band-read wrapper + the `:851` level_now consumption wrapper + the embedded sealed rate) ·
`rl_export.py` (§2.iii retirement, §2.ix) · `session_2026-07-18/legf4/`. HARD-OUT verified untouched:
`rl_model.py` (incl. `_dev_advance`) · `distribution_pricing.py` (`v_at_peak`/`price6`) · V0/`_iso_dec`
`:1121-1171` · q97m · store · curve · pins/acceptance · docs · ui · SEASON_PROG.

## THE GATE — ROSTER-MATCHED, ±5%, BOTH transitions (MEMO_LEGF v1.3 §2.x) — **PASS**
Project each committed historical roster forward under the damped board's r(age), vs the SAME players'
realized next-year values INCLUDING exiters' realized residuals (off-board = 0, busts full weight R107.3):

| transition | pred | realized (incl exiters) | error | ±5% | verdict |
|---|--:|--:|--:|---|---|
| **−2 → −1** | 677,809 | 697,105 | **−2.8%** | ±5% | **IN** |
| **−1 → now** | 681,034 | 680,109 | **+0.1%** | ±5% | **IN** |

Pre-F4 (undamped): the same projection landed −25.8% / −28.1% OUT. Survivor-only DIAGNOSTIC (not a gate,
ageing-quality isolation): −2→−1 −6.4%, −1→now −2.3%.

## THE SEALED RATE (measured ONCE, sealed pre-render, NEVER iterated against a backtest — v1.3 §2.ix)
`r_pop(age)` — value-weighted realized backward-transition rate per draft-year age on the committed −2/−1/now
boards, INCLUDING exiters' realized residuals (population basis, R107.3), rule-7 smoothed. **SEAL sha256_8
`c62b5ee8`.** `s(age)` — the geometric-blend coefficient bisected so the damped median(vP1/v) per age ==
r_pop(age) (deterministic solution of the sealed-rate constraint; Reid — content IS the measured rate).
**SEAL sha256_8 `efe97ee3`.** Both embedded in `_merged_recover.py` (ship in-source). The v1.2 survivor-basis
seal `ef1970db` is SUPERSEDED (owner item 359) — retained as a diagnostic only.

## BYTE-EXACT CHAIN (the untouchable invariants)
| config | edited vs reference | verdict |
|---|---|---|
| RL_LEGF=0 RL_LEGE=0 RL_PVC2=1 (balanced k=0) | edited == original engine | **PASS byte-exact** |
| RL_LEGF=0 RL_LEGE=1 RL_PVC2=1 (Leg-E lens)   | edited == original engine | **PASS byte-exact** |
| RL_LEGF=0 RL_LEGE=0 RL_PVC2=0 (PVC2 kill)    | edited == original engine | **PASS byte-exact** |
- **k=0 / backward DORMANCY: RL_LEGF=1 calibrated board v / vM1 / vM2 == undamped, diff 0 (804/804).** The
  damper is forward-only + RL_LEGF-gated ⇒ a no-op at k=0 / balanced / backward / RL_LEGF=0 BY CONSTRUCTION.
- **balanced k=0 `v` == committed board_now (`06d8af60` posture) byte-exact 804/804, Σv = 752,427** (the
  filed total). [The initial cold-start build read a transient — WARMED per F3's PLAN §0 lesson; all figures
  are the warm, deterministic state, two warm builds byte-identical.]
- **k=0 DORMANCY UNIT TESTS: F3 `test_k0_dormancy.py` PASS · F4 `test_k0_dormancy_f4.py` PASS** (clock/blend
  identity at every edited site — forward-only, RL_LEGF-gated, s≥1 & x_form==x_age ⇒ identity).
- store `968de0c7` untouched.

## THE CURE (composition-controlled, same 804 roster)
- **Forward −8.8% vs backward −9.0% — SYMMETRIC** (was forward −19.6% / −19.9% — the item-354 residual). The
  ~11pt board-wide asymmetry is closed to ~0.2pt.
- **Gradient un-inverted & monotone** (F3's cure is the floor, preserved): developing −3.8% (shallowest) ≥
  mid −9.5% ≥ veteran −18.3% (steepest — real aging).
- Per-lens totals (RL_LEGF=1): −2 875,732 · −1 827,140 · now 752,427 · +1 686,000 · +2 635,411.

## §2.iii RETIRED (v1.3 §2.ix; rl_export.py, obituary in the diff)
The F3 distributed-retirement haircut (`_LF_PRET`/`_pret`/`_hair`/`_residual`) is DELETED (not disabled) —
exit risk lives ENTIRELY in `r_pop` (one carrier, no double-count). Report-only; the balanced board `v` and
the k=0 chain are untouched by the retirement. Entrant/refill sizing deferred to §2.viii (F5).

## GUARD-5 / NUMERIC STACK ANNEX
Guard-5 rl_model pin = the KNOWN PRE-BAKE RED (checkout `cc626d7d` ≠ boot pin `a5fd3d7d`) — FLAGGED, never
self-pinned. Stack: py3.12.3 · numpy2.4.4 · scipy1.17.1 · sklearn1.8.0 · scipy-openblas DYNAMIC_ARCH ·
threads pinned 1.

## VERDICT
The L-SYMMETRY damper (r_pop, population basis) brings BOTH roster-matched transitions inside ±5%, cures the
forward-vs-backward asymmetry (−8.8% vs −9.0%), keeps the gradient un-inverted, is k=0/backward byte-exact
and RL_LEGF=0-inert, §2.iii retired without double-count. Store/curve/rl_model/v_at_peak untouched.
