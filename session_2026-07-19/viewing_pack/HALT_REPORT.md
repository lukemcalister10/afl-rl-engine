# VIEWING-PACK RENDER — HALT AT THE REPRODUCTION PRECONDITION
seat 14 · 2026-07-19 · READ-ONLY (Tier 3) · report-only · **changes nothing, never bakes**
directive: `docs/DIRECTIVE_VIEWING_PACK_2026-07-19.md`

## Bottom line
The mandatory reproduction precondition (item 366 + the LEGE=0 correction) **FAILED** on this
container, so — per the directive's own rule *"never render on a non-reproducing container"* — the
viewing pack was **NOT rendered**. This document and `out/repro_precondition.txt` are the entire
deliverable. No board, movers, lens, rider, gate, or ratification section was produced.

## What passed (git entry — STRICT)
| check | value | expect | verdict |
|---|---|---|---|
| F6 head `ls-remote` | `540b62f3c160…60b2b` | `540b62f…` | **PASS** |
| store `rl_model_data.json` | `968de0c7` | `968de0c7` | PASS |
| frozen `data/v0surf.pkl` | `3af2b725` | `3af2b725` | PASS |
| committed board `rl_app_data.json` | `270a2c5f` (RL_LEGF=1 full) | `270a2c5f` | PASS |

## What failed (the precondition)
Built the balanced board on a fresh copy of the F6-head `engine/rl_after` (materialised with
`git archive` into scratch — the repo working tree was never modified), single-thread, `PYTHONHASHSEED=0`,
v0surf **LOAD** mode, `RL_LEGE=0 RL_LEGF=0`:

```
balanced (RL_LEGE=0 RL_LEGF=0): md5 d7a95e8d | Sum v 750171 | Sheezel 7869   [5/5 consecutive, identical]
EXPECT                        : md5 06d8af60 | Sum v 752427 | Sheezel 7964
```

Sheezel **7869 = −95** is the documented *weather* signature — not the filed clean board.

## Why it is a genuine HALT, not a fixable slip
The directive lists two escape hatches — **bad/absent pickle** or **wrong env**. Both are ruled out:

- **Pickle correct + loaded.** `data/v0surf.pkl` md5 `3af2b725`; at runtime `_V0SURF` holds the one key
  `a610237ed541…`, the computed `_v0surf_sig` **matches** it, and `_v0surf_frozen = True` — the frozen
  surface is LOADED, not fitted.
- **Env correct.** `RL_LEGE=0 RL_LEGF=0`, `PYTHONHASHSEED=0`, all four BLAS/OMP thread caps = 1, dev-shell
  (no config-mode divergence), `RL_V0SURF_REFIT` unset.

Yet the board is stably weather-flipped. And it is not only the balanced lens — **all three other filed
configs flip too** on this box:

| config | this container | filed | verdict |
|---|---|---|---|
| default `RL_LEGE=1 RL_LEGF=1` | `c5ccd667` | `1f10220c` | MISMATCH |
| forward `RL_LEGE=1 RL_LEGF=0` | `527b25d0` | `d85901af` | MISMATCH |
| balanced `RL_LEGE=0 RL_LEGF=0` | `d7a95e8d` | `06d8af60` | MISMATCH |

**Diagnosis.** The v0surf freeze did its job (surface loaded, signature matched) — it de-weathered the V0
pick-curve surface. But a **residual weather-susceptible computation remains on the value path** (beyond
v0surf / q97m / peak), and it flips every lens on this container. The build is internally deterministic
(5/5 byte-identical) but does not reproduce any filed board. This is precisely the state the register
already records (`docs/OPEN_ITEMS_REGISTER.md`: *"internally deterministic, does NOT reproduce the filed
`06d8af60`, with a NAMED row −95"*), whose filed remedy is to **retry on fresh instances until one
reproduces `06d8af60` at the precondition** (retry is cheap).

## Recommended next step (for the owner / next seat)
Re-run this exact precondition on **fresh containers** until one reproduces `06d8af60` byte-exact, then
render the pack there. Nothing about the F6 head, the pins, or the directive is at fault — this box is a
weather box. Do **not** render the ladder viewing from the non-reproducing board on this container.

## Fence / posture
READ-ONLY. Wrote only into `session_2026-07-19/viewing_pack/`. No engine/store/curve/docs file touched;
nothing baked. The PR opened for this report is **REPORT-ONLY / DO-NOT-MERGE**.
