# LEG B SELECTION — s=0.10 CLEAN RE-MEASUREMENT (owner-set, register item 265) · 2026-07-16 · seat 10

**The owner locked the strength: register item 265, verbatim — "Let's lock in s=0.10 and move forward."**
This build WIRES that one constant (`UNCOMP_S_DEFAULT: None → 0.10`) on the STRICT engine base
`fef2b64` (the conserved-measurement line + the default-off `RL_UNCONSERVE` toggle) and re-measures the
frozen battery CLEAN on the properly-based line. The prior s=0.10 numbers were viewing-grade (item 264
base violation); these supersede them. Store `b1fd0bce` untouched throughout. **This build merges nothing
and bakes nothing** — the boot pin update + cold-audit ladder come at chapter end.

- Engine base **fef2b64** (`fef2b64 ancestor: yes`). Wire commit `ddb1328` — one line, owner-worded
  comment; `UNCOMP_DECAY` stays 0.25, `RL_UNCONSERVE` stays default-off, no other constant.
- Conserved path (memo §3 per-position renorm C[pos] APPLIED — the shipped path). Measured at the WIRED
  DEFAULT with **no env override** — the default path itself is the object under test.
- Frozen instruments: β `beta_measure.py` md5 `14c59139`; G-COHORT `ship_gates_check._b1_july8` (matrix
  `__meta__` engine/store hashes asserted == running engine); ledger `ledger_dump.py`.

## A/B — kill-switch identity + default-path proof
| run | board md5 | verdict |
|---|---|---|
| (1) `RL_UNCOMP=0` (kill-switch) | `8d90c9ac` | **PASS BYTE-EXACT** (shipped board reproduced) |
| (2) WIRED DEFAULT (no override) | **`f2f077b2`** | the new default board |
| (3) explicit `RL_UNCOMP_S=0.10` | `f2f077b2` | **== default** (default path == the 0.10 literal, proven) |

## SELF-TEST SUITE — substantive checks GREEN; GUARD 5 the expected candidate-vs-pin divergence
`one_source_selftest.py` — **every substantive guard PASSES**: SSI single-source (G3) · derived
read-only + stamped (G1/G2) · engine loads 804 · **F1 export parity** (0 mismatches) · **F2 book parity**
(0 mismatches) · data ground-truth (Kako/Bontempelli) · position model · Leg-A fade/monotone ·
**R105.5 L-RECENCY (7 checks)** · **R105.4 ρ-forbidden-list (3 checks)** · collision sentry (King pair, 30
checks). GUARD 4 correction-canary **GREEN** (separate full rebuild).

The **only RED is GUARD 5 (boot-store)**: it asserts the workspace engine md5 == the *shipped* pin
(`rl_model f79fc740`, `_merged_recover a83c9f6d` in `data/expected_boot.json`). The one-constant wire
legitimately moves them to `94b7016d` / `a0635745`, so GUARD 5 trips. **This is structural to any unbaked
candidate** — the boot pin is refreshed only at a bake (owner-only; `expected_boot.json` = gate data,
fenced OUT of this build). Not a wire defect; it is the item-264 lesson restated — the pin travels with
the shipped tree, and a candidate legitimately diverges until re-pinned at chapter end.

## G-COHORT y4/y5/y6 — judged both sides against the FULL band (floor 1.08 · cap 1.30 · ideal 1.15–1.25)
| | y4 | y5 | y6 | verdict |
|---|---|---|---|---|
| **OFF** (Leg-A head, board 8d90c9ac) | 1.3017 | 1.3160 | 1.2664 | **y4 & y5 BREACH cap 1.30** (the standing obligation) |
| **s=0.10 (wired default)** | **1.2667** | **1.2727** | **1.2300** | **PASS ×3** — all band-legal |

At the wired default the Leg-A y4/y5 breach (1.3017/1.3160) is pulled inside the band on both cohort
years; all three sit in [1.08, 1.30]. **y6=1.2300 lands inside the 1.15–1.25 ideal**; y4=1.2667 and
y5=1.2727 sit a hair above the ideal top (well under the 1.30 cap). The breach is resolved by genuine
seating (cohort curve intact), not by deflation.

## β (frozen) — flat, as the conserved grid predicted
- OFF β_c = **0.6219** (CI [0.4836, 0.7899], width 0.3063, n=116). Default s=0.10 β = **0.6299**
  (CI [0.4914, 0.7960], width **0.3046 ≤ 0.35 OK**, **n=116 < 120**, CI contains 1.0, point < 0.85).
- s=0.10 buys β essentially nothing over the OFF anchor (+0.008) — matches the conserved synthesis:
  the health-band-legal landing zone does not trade cohort health for a passing β.

## E/B vs 1.75 — PASSES; the denominator-collapse flag, mild at s=0.10
- OFF: 3655 / 2070 = **1.766×**. ON (s=0.10): **3679 / 1913 = 1.923× → PASS ≥ 1.75**.
- Raw parts: **English +24 (+0.7%)**, **Briggs −157 (−7.6%)**. Per the item-260 lesson the lift is more
  denominator (Briggs down) than numerator (English up), but at s=0.10 the cut is mild (−7.6% vs −45% at
  s=0.70). Note: **English is itself a marginal sincerity-fail row** (SCAR +24, rank 34→36, +2) — recorded,
  consistent with the conserved measurement.

## NET ΣΔ / POOL RE-RATE — conserved residual, generational shape
- Net board **ΣΔ = +1231 num-SCAR** (0.17% of the 734,044 active-804 baseline sum). 206 movers
  (128 lift / 78 cut), Σ|Δ| = 15,527.
- Pools: **MID absorbs the lift (+1155)**, funded out of **GEN_FWD (−404)** + KEY_FWD (−45); GEN_DEF +148,
  KEY_DEF +105, RUC +272 on the board total (individual ruck denominators cut: Briggs −157, De Koning −146).
- **Generational axis** (same as items 260/conserved): veterans proven up — Liberatore +182, Neale +175,
  Gunston +136, Steele +110, Pendlebury +74, Kelly +67, Viney +49, Witts +52; young-pedigree forwards down —
  Sanders −374, Watson −345, MacDonald −186, Rachele −149, Ginnivan −114.

## SINCERITY LEDGER (item 256, all 804 rows) — `SINCERITY_all804_s0.10.csv`
- **Bontempelli PASSES the owner's named test** (SCAR up AND rank up): SCAR 3625→3888 (**+263, +7.3%**),
  rank 35→**26** (**−9**). Clean.
- **SCAR-up-rank-down failures: 10, all MARGINAL** (ΔSCAR +6…+31 on near-flat rows nudged by faster
  risers; no large-SCAR row loses rank): Maynard +6 (240→243), English +24 (34→36), Ridley +10 (206→208),
  Drew +12 (256→258), Madden +20 (164→165), Sweet +18 (72→73), Daniels +21 (168→169), Waterman +31
  (125→126), McKay +28 (124→125), Lester +27 (244→245). No genuine insincerity.
- Top-20 rank gainers: proven MID/RUC/veteran GEN_FWD. Top-20 losers: young GEN_FWD + ruck denominators.
  (Full named rosters in `out/POINT_s0.10.md`.)

## A-PAIRS pair 2 + pair 3 (scored on the wired-default board `f2f077b2`)
- **pair_2 reid/bont**: reid 3343 vs bont 3888 = **−14.0%** — **FAIL on the historic ±10% PARITY band**
  (as the directive expected; scored, NOT flagged as a defect). PASS on the owner ±15% re-band (register
  item 266). Disposition rests with the owner word (item 266 re-bands to ±15%).
- **pair_3 sanders/bont**: sanders 3579 vs bont 3888 = **−7.9%** — **PASS** (sits 0–10% below bont).

## PLAIN CLOSE
On the properly-based line, the owner-locked s=0.10 does the one thing the chapter owed: it pulls the
Leg-A y4/y5 breach (1.3017/1.3160) inside the band (1.2667/1.2727) with y6=1.2300 landing in the ideal
zone, at a conserved net residual of +1231 num-SCAR that recycles generationally (veterans up, young
forwards down). β is flat (0.6299), E/B passes (1.923×) with a mild denominator flag, Bontempelli's
sincerity test passes emphatically, and the ten sincerity slips are all marginal. pair_2 reads −14.0%
(FAIL ±10% / PASS ±15% item 266). The substantive self-test suite is green; the lone GUARD 5 RED is the
expected candidate-vs-shipped-pin divergence, resolved by the boot re-pin at chapter-end bake.
