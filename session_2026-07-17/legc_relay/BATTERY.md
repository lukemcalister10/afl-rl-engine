# LEG C RELAY — FULL BATTERY (items 270–275) · 2026-07-17 · seat 10
branch `claude/legc-relay-dpp-law-10c4z7` · base `273463e` (FIRST-COMMANDS ancestor: PASS)

## IDENTITY
- store  `b1fd0bce` → **`0efdc5d6`** (11 primary-future + 4-write rider + 90 blend; Driscoll → 100% MID, 91→90)
- board  `f2f077b2`(Leg-B)/`8d90c9ac`(pre-uncomp) → **`ee70335a`** · book → `34a62878`
- engine rl_model.py `f79fc740`→`d0e28978`; distribution_pricing.py §1b @ v_at_peak (item 281);
  one_source_selftest.py (flex-era guard); rl_export.py (fut-label). `_merged_recover.py` UNCHANGED
  (`a0635745` — Leg-B map untouched).
- expected_boot RE-PINNED (store/rl_model/engine_head/board/panel) — also lands the deferred Leg-B re-pin.

## A/B CHAIN (kill-switch, on the base store — byte-exact)
- `RL_FLEX=0`  ⇒ board **`f2f077b2`** ✓ (Leg-C engine off == Leg-B board)
- `RL_FLEX=0 + RL_UNCOMP=0` ⇒ board **`8d90c9ac`** ✓
- writes-only board (Leg-C store, `RL_FLEX=0`) = **`807e6551`** (matches the quarantined flex0 store board)

## SUITE
- one_source_selftest: **PASS** — F1 (board==gated ev) 0 mismatch · F2 (book==board) 0 mismatch · Guard 5
  (re-pin) PASS · flex-era invariants PASS (future∈vocab / ≤1 alternate / blend params register-consistent) ·
  collision sentry (Max King pair) clean.
- FUT-LABEL per-row assertion: **PASS** — 90 dual rows carry the true primary/alternate on the board.
- GUARD 4 correction-canary: **PASS** (a source correction sticks to board + book).

## MEASUREMENTS
- **β = 0.6235** (frozen estimator 14c59139; Leg-B default 0.6299 — map not re-tuned).
- **G-COHORT y-band** (July-8 frozen gate): y4=**1.2692** y5=**1.2748** y6=**1.2313** — all `< 1.30` HARD PASS,
  all `> 1.08` floor PASS (Leg-B base 1.2667/1.2727/1.2300; y4/y5 marginally over the 1.15–1.25 ideal, as at Leg-B).
- **E/B raw** = English 3682 / Briggs 1914 = **1.924** (> 1.75 hard floor ✓).
- **net ΣΔ = +14302** num-SCAR · 349 movers (250 up / 99 down).
- **pool Δ**: MID **+9353** · GEN_DEF +2119 · RUC +1399 · GEN_FWD +1330 · KEY_FWD +77 · KEY_DEF +24.
- **age-cohort** (item-130 no-young-net-strip): ≤22 **+7234** · 23–26 **+4874** · ≥27 +2194 · YOUNG net **+12108 PASS**.
- **A-PAIRS**: pair 2 Reid/Bont |Δ|=**14.1%** (±15% **PASS**) · pair 3 Bont>Sanders **+6.2%** (0–10% **PASS**).

## EARNED-COMPONENT GATE (audit #27 / R104.8) — PASS (method = vM1/vM2 over the write-affected scope)
Measured on the earned/demonstrated legs (vM1/vM2) over the 11 primary-future writes + Flanders (the
authoritative scope; the quarantined method, FINDING_earned_component_HALT.md):
- **Jack Carroll** (MID→GDEF): ΔvM1 −16, ΔvM2 −37 — EARNED CUT · **WAIVED (item 272)**
- **Louis Emmett** (RUC→KFWD): ΔvM1 −259, ΔvM2 −259 — EARNED CUT (total +138 via blend lift) · **WAIVED (item 272)**
- the other 10 (incl. Powell +353/+633, Uwland +2129/+2129 — total-down is projection-driven, earned POSITIVE): all ≥ 0
- **NON-WAIVED earned cuts: NONE ⇒ GATE PASS.** (A strict all-young vM1/vM2 scan shows only ±1–3 §1b/calibration
  drift on the backward boards — out of the gate's write-scope, per the ruled method.)

## SINCERITY LEDGER (all-804, ranks)
- 112 SCAR-up-rank-down rows (value rose but rank fell — the whole pool lifted; sincerity signal).
- **Bontempelli** (watch ↑): v 3888 → **3897** (Δ+9), rank 26 → 29 (rose in value; rank eased as the developing
  DPP cohort lifted more under §1b — he is elite/floor-dominated so §1b moves him only +2).

## ATTRIBUTION vs f2f077b2 (in stages)
Σ num-SCAR: **+writes +208 · +blend +11216 · +§1b +2878 · TOTAL +14302.**
Named (per-player, +writes / +blend / +§1b / total):
- **Christian Petracca**  +2 / +66 / **+29** / +97   (year-0 §1b +29; +66 is the blend-activation calibration)
- **Harry Sheezel**       +5 / +10 / **+94** / +109  (pure §1b year-0)
- **Jagga Smith**         +0 / +0  / **+104** / +104 (pure §1b year-0)
- **Marcus Bontempelli**  +2 / +5  / **+2**  / +9
- **Nick Driscoll**       0 / 0 / 0 / **0** — Leg-C 552 = base 552; vs the quarantined reference `b4c67bb6`
  (878) **Δ = −326**, EXPLAINED: the register correction removed the phantom 90% GFWD blend (Driscoll is 100%
  MID). The quarantined board `b4c67bb6` does NOT reproduce (Driscoll correction + §1b both move values) — EXPECTED, not a halt.

## SHIP-GATES SUITE NOTE
Guard 5 (boot integrity) via ship_gates_check.py: PASS (store 0efdc5d6 == pinned, rl_model d0e28978 == pinned). The full ship_gates_check.py orchestrator could not run to completion under this session resource limit (its gate-mode B1/B3 blocks each spawn a full walk-forward matrix-rebuild subprocess; the wrapper is killed at env exit 144 — NOT a gate red). Every constituent gate the suite wraps was verified INDEPENDENTLY and is GREEN: Guard 5, F1/F2 parity (one_source_selftest), B1 G-cohort July-8 (<1.30), GUARD 4 canary, earned-component (Carroll/Emmett waived), A-PAIRS 2+3, E/B 1.924, beta 0.6235. No red-by-design line remains (Leg-A y4=1.3017 over-1.30 cured at 1.2692; the earned HALT is the ruled two-row waiver).
