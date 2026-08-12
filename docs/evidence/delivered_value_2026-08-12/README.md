# `docs/evidence/delivered_value_2026-08-12/` — ORDER 26B

**The act:** ORDER 26B, the delivered-value rederivation. Brief and thirteen owner rulings:
[#334 comment 5269952564](https://github.com/lukemcalister10/afl-rl-engine/issues/334#issuecomment-5269952564).

**Outcome: the build STOPPED at step 1.** The identity gate (Ruling 9) failed against the live board
price, and Ruling 9 makes a gate failure a stop. Steps 3–6 were not run.

**Start here:** `SHIPPING_PACKET_26B.md`.

| file | what |
|---|---|
| `PREREG_ORDER26B.md` | pre-registration, committed before any measurement of this order's quantities |
| `GATE_REPORT.md` | the identity gate in owner-readable form — the verdict, the attribution, the two readings |
| `SHIPPING_PACKET_26B.md` | the packet: what was and was not delivered, the prereg scored, breaches owned |
| `o26b_gate.py` → `GATE.json`, `GATE_out.txt` | the gate instrument |
| `o26b_layer1.py` → `LAYER1_out.txt` | the Layer-1 builder |

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
