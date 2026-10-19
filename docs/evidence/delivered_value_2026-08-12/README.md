# `docs/evidence/delivered_value_2026-08-12/` — ORDER 26B

**The act:** ORDER 26B, the delivered-value rederivation. Brief and thirteen owner rulings:
[#334 comment 5269952564](https://github.com/lukemcalister10/afl-rl-engine/issues/334#issuecomment-5269952564).

**Outcome: COMPLETE, steps 0–6.** The build stopped at step 1 when the identity gate, read literally
against the live board price, failed. The owner then ruled
([#334 comment 5270492281](https://github.com/lukemcalister10/afl-rl-engine/issues/334#issuecomment-5270492281),
"Core, resume") that the gate is **SATISFIED AT THE PRICING CORE** — the scorer is bit-exact against the
engine's own `price6` on 804/804 rows — and that the four adjustment legs are player-state machinery,
deferred whole to the consumption-rewire act. Steps 3–6 ran on that ruling.

**Start here:** `SHIPPING_PACKET_26B.md`.

| file | what |
|---|---|
| `PREREG_ORDER26B.md` | pre-registration, committed before any measurement of this order's quantities |
| `GATE_REPORT.md` | step 1 — the identity gate, its verdict and the zero-residual attribution |
| `o26b_gate.py` → `GATE.json`, `GATE_out.txt` | the gate instrument |
| `o26b_layer1.py` → `LAYER1_out.txt` | step 2 — the Layer-1 builder |
| `o26b_layer2.py` → `LAYER2.json`, `LAYER2_out.txt` | step 3 — the valuation layer, all knobs in one config block |
| `o26b_derive.py` → `DERIVE.json`, `DERIVE_out.txt` | step 4 — the all-in curve, positional relativities, pool ladders, MSD both ways |
| `INSTRUMENTS_PRESTATEMENT.md` | step 5 — both instruments' exact forms, dated and committed BEFORE the computation |
| `o26b_compare.py` → `COMPARE.json`, `COMPARE_out.txt` | step 5 — comparisons and both new mandatory instruments |
| `o26b_v5.py` → `V5_APPENDIX.json`, `V5_APPENDIX_out.txt` | the V5 age-ladder appendix (**RULED OFF 2026-08-13**, kept as measured context) |
| `PRESTATEMENT_26BV.md` | ORDER 26B-V's predictions, committed before the variants harness existed |
| `o26b_variants.py` → `VARIANTS.json`, `VARIANTS_out.txt` | the grace-years four-way menu + hits table (**NOT RULED**) |
| `per_entrant_O25R4.json` | the walk-forward matrix, copied for durability (md5 `3c6ffcdeaac9786473f3f017dba1d61e`) |
| `SHIPPING_PACKET_26B.md` | step 6 — the packet: the curve beside today's, the pathway tables, both instruments, the prereg scored, breaches owned |

**CORRECTION 1 (26B-C1), 2026-08-13 — READ `SHIPPING_PACKET_26B.md` §16 FIRST.** A standing owner
ruling missing from this order's brief (the force-majeure exclusion of `thomas-boyd` and
`paddy-mccartin`, implemented as the whole-draft slide of the 2013 and 2014 national drafts) was
applied by correction order, re-filed at
[#334 comment 5274640130](https://github.com/lukemcalister10/afl-rl-engine/issues/334#issuecomment-5274640130).
It ships as named config (`CFG.force_majeure`) with a **halting deriver assert**. Layer 1 is untouched
and Layer-2 per-career scores are byte-identical; only the ND cohort attribution moves. **Packet
sections 1–15 carry the pre-correction numbers and are left standing deliberately; §16 is the
operative version.**

**CORRECTION 2 (26B-C2), 2026-08-13 — `SHIPPING_PACKET_26B.md` §17 is the OPERATIVE version.** Owner
ruling [#334 comment 5275737926](https://github.com/lukemcalister10/afl-rl-engine/issues/334#issuecomment-5275737926):
the aggregator's weighted-mean step has one-sided **boundary bias** (pick 1 dragged down, pick 64
flattered up), and is replaced by a **local-linear fit** over log(pick) across the whole curve — the
shipped Gaussian kernel and bandwidth rule unchanged, the solver reusing the engine's own
`par_build.py::loclin` algebra (`o26b_loclin.py`). Engine bytes still 0.

**The headline numbers (C2, operative).** Pre-anchor scale at pick 1 = **2,463.1** board points;
anchoring factor **×1.2180** (pick-vs-player premium **21.8 %**, down from 31.3 %). Pool derived v0s
come in at **0.3906×** today's printed day-0 prices and **1.0056×** the owner's signed anchors — within
0.6 % of parity. Both new instruments **PASS**, every verdict unchanged by either correction. Nothing
is landed.

*For the record — head · factor · derived/printed · derived/anchor:*
*original 2,112.6 · ×1.4200 · 0.4554 · 1.1720 → C1 2,284.6 · ×1.3131 · 0.4211 · 1.0841 →*
***C2 2,463.1 · ×1.2180 · 0.3906 · 1.0056.***

**The dataset this act produced lives elsewhere, deliberately:**
`data/delivered_value/layer1_player_seasons.json` (md5 `ad1229ea6f443538479447132382b21c`) — a
first-class pinned dataset kept beyond this exercise, per Ruling 11.

**Pins.** Every instrument asserts these at entry and at exit and halts on a mismatch:

| object | md5 |
|---|---|
| `engine/rl_after/rl_model_data.json` | `d9a24282357cf3083b1640466e3ecd83` |
| `engine/rl_after/rl_app_data.json` | `88ce647f531030d8d2e094188b258191` |
| `engine/rl_after/_merged_recover.py` | `3f1468e5468462ab789e49aace264c90` |
| `engine/rl_after/rl_model.py` | `e5eb5e4405c09eebef45a9db89f014bc` |
| `engine/forward_valuation/dist_redesign.py` | `48ea1bfeccc6d1ea51add66b0cb93965` |

**Read-only.** No engine file was changed, no pin was moved, no board was rebuilt. **Nothing is landed.**

**Upstream:** ORDER 26A, `docs/evidence/reconciliation_2026-08-12/` (the target framing and the wedge).
**Conventions borrowed:** `docs/evidence/pool_dial_2026-08-12/o24_uharvest.py::stream` (pathway naming).
