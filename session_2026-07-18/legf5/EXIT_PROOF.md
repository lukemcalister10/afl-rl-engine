# LEG F5 — EXIT PROOF · seat 13 · 2026-07-19 (single-thread OPENBLAS/OMP/MKL/NUMEXPR=1)
The ENTRANT LAYER + the CONSERVATION GATE (MEMO_LEGF v1.3 §2.viii/§2.x, owner ruling item 359). Base F4 exit
`a9570cb5` (F3/F4's cures are the floor, never re-opened). Store `968de0c7` · curve `56dd7a7b` (payload
`89c14729`) — ABSOLUTE, untouched. Touched set (⊆ the granted fence): `engine/rl_after/rl_export.py` (the
§2.viii phantom block only) · `ui/app/board.js` (the +1/+2 banner header — mechanically required: the F1
exits/R/X strawman fields it read are retired) · `session_2026-07-18/legf5/`. HARD-OUT verified untouched:
`rl_model.py` · `_merged_recover.py` (incl. the L-SYMMETRY damper + sealed rate) · `distribution_pricing.py`
· V0/`_iso_dec` · q97m · store · curve · pins/acceptance · docs · SEASON_PROG.

## THE TWO GATE TABLES (MEMO_LEGF v1.3 §2.x)

### (A) F5 CONSERVATION GATE — LEAGUE-LEVEL, ±5%, BOTH transitions — **PASS**
Project each committed historical roster forward under the population rate, ADD the §2.viii entrant layer at
PVC, vs the REALIZED league total (F2 bridge_totals 770,987 / 771,152 / 752,427, ~flat):

| transition | roster proj | + entrant layer | = pred | realized league | error | ±5% | verdict |
|---|--:|--:|--:|--:|--:|---|---|
| **−2 → −1** | 678,724 | +83,538 | 762,262 | 771,152 | **−1.2%** | ±5% | **IN** |
| **−1 → now** | 681,844 | +83,538 | 765,382 | 752,427 | **+1.7%** | ±5% | **IN** |

r_pop-direct variant (sealed rate, not the board median): −2→−1 **−0.6%**, −1→now **+2.3%** — both IN.

### (B) F4 ROSTER-MATCHED GATE — re-run, ±5%, BOTH transitions — **PASS (stays IN)**
Same players' realized next-year value INCLUDING exiters' residuals (off-board = 0, R107.3):

| transition | pred | realized (incl exiters) | error | ±5% | verdict |
|---|--:|--:|--:|---|---|
| **−2 → −1** | 678,724 | 697,105 | **−2.6%** | ±5% | **IN** |
| **−1 → now** | 681,844 | 680,109 | **+0.3%** | ±5% | **IN** |

(Filed at F4: −2.8% / +0.1%; the ≤0.2pt shift is this container's weather on the median vP1/v, well inside
±5%. The entrant layer is additive — it does not touch v/vP1, so r(age) is unchanged by F5.) Survivor-only
DIAGNOSTIC (not a gate, ageing-quality isolation): −2→−1 **−6.2%**, −1→now **−2.2%** (F4 filed −6.4 / −2.3).

## THE SEALED ENTRANT STRUCTURE (§2.viii; measured ONCE, sealed pre-render, NOT tuned against the gate)
`sealed_entrant_structure.json` — **seal sha256_8 `a17aafed`**. Measured from recorded store intake history,
window 2019–2025 (7 complete draft years; the partial 2026 mid-season cohort excluded), board-eligible (GRP)
entrants only. Priced at the engine's OWN effective pick `effpk`: ND = pick · RD/PSD = chained after the
national draft (`_NDC[year]+pick`) · pickless mechanisms = measured pick-equivalents (MSD **90**, all others
**92**, item 341). Smoothed = per-effective-pick mean per-year occupancy (no wide/decile bins, CORE rule 7).
**Expected 103.4 slots/yr · entrant PVC draft 69,266 + mech 14,272 = TOTAL 83,538.** The board emits exactly
this (cross-checked: board `entrant_layer_pvc` == sealed 83,538). The F1 §2.i/§2.ii pick-slot strawman
(picks 1..30 + flat R=207 + exit bar X=207, item-343 R-frame 207/220/471) is SUPERSEDED (obituary in-block).

## BYTE-EXACT CHAIN (the untouchable invariants — F1 discriminator doctrine, container-faithful)
This container instance is DETERMINISTIC (two warm RL_LEGF=0 builds byte-identical, stable balanced md5
`83a4b21d`, Σv 750,159) but does not byte-reproduce the filed `06d8af60` — a container-instance weather delta
living ENTIRELY in the UNEDITED F4 base (one panel row, Sheezel, −95; the other 9 within ±3; item 347 forbids
CORETYPE archaeology). The k=0 invariant is therefore proved as a byte-exact DIFF vs the F4 base IN THIS
container, not by reproducing filed bytes:

| config | edited vs F4-base original | verdict |
|---|---|---|
| **RL_LEGF=0** (balanced / Leg-E chain) | edited `rl_export.py` == original, board `83a4b21d` | **PASS byte-exact (cmp identical)** |
| **k=0 phantom = NONE** | RL_LEGF=1 balanced `v` == RL_LEGF=0 `v`, **0/804** diffs | **PASS** |

- The entire §2.viii edit is INSIDE the `RL_LEGF != '0'` branch (the executable diff carries no line before the
  guard; the two hunks are the phantom block only). So EVERY RL_LEGF=0 configuration (RL_LEGE, RL_PVC2) is
  byte-exact by construction — the block is unreachable at RL_LEGF=0.
- **k=0 DORMANCY UNIT TESTS: F5 `test_k0_dormancy_f5.py` PASS · F4 `test_k0_dormancy_f4.py` PASS**
  (`_merged_recover.py` untouched ⇒ the L-SYMMETRY damper suite is byte-unaffected).
- **PARITY GATE PASS**: all 804 active board values == engine gated ev() (eps=0) on the RL_LEGF=1 build.
- store `968de0c7` untouched.

## GUARD-5 / NUMERIC STACK ANNEX
Guard-5 rl_model pin = the KNOWN PRE-BAKE RED (checkout `cc626d7d` ≠ boot pin) — FLAGGED, never self-pinned
(unchanged from F3/F4; F5 touches no engine head). Stack: py3.12.3 · numpy2.4.4 · scipy1.17.1 · sklearn1.8.0 ·
scipy-openblas DYNAMIC_ARCH · threads pinned 1 (OPENBLAS/OMP/MKL/NUMEXPR).

## VERDICT
The §2.viii entrant layer carries the full sealed annual intake (83,538 PVC, 103.4 slots/yr, seal a17aafed,
sealed from history — not tuned). BOTH conservation gates PASS ±5%: the owner's LEAGUE-LEVEL law (−1.2% /
+1.7%) and the F4 ROSTER-MATCHED re-run (−2.6% / +0.3%, stays IN). k=0 / RL_LEGF=0 byte-exact, phantom=NONE
(0/804), both dormancy suites PASS, parity gate PASS, store/curve/engine untouched. The chapter's last build.
