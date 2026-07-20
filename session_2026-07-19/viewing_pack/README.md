# Viewing-pack render — 2026-07-19 · seat 14 · READ-ONLY / REPORT-ONLY / DO-NOT-MERGE

**Outcome: HALT.** The mandatory reproduction precondition (build the balanced board
`RL_LEGE=0 RL_LEGF=0` at the env-pin head `3055ea5` and assert `== 06d8af60` byte-exact) **did not
reproduce** on this fresh container — it produced `d7a95e8d`. This is the **container-#2 leg of the
item-392 reproduction gate**, and it is **RED**. Per the directive (halt-not-warn), the viewing pack
(sections 1–7) was **not rendered**; a divergent board must not be shown as truth.

## Artifact → provenance map
| artifact | what it is | provenance |
|----------|-----------|------------|
| `HALT_container2_gate.md` | the gate result + full diagnosis + findings | fresh compute (container #2, pinned env, F6 head `3055ea5`) |
| `evidence/board_balanced_repro.container2.json` | the balanced board built here (md5 `d7a95e8d`) | re-runnable; recipe = container-#1 `confirm_5of5.sh` verbatim |
| `evidence/exportlog_balanced.container2.txt` | export log (src=968de0c7, active=804, PARITY PASS, v0surf loaded) | re-runnable |
| `evidence/env_fingerprint.container2.txt` | numpy 2.4.4 (pinned wheel, assert PASS) + bundled OpenBLAS `05c9f9eb` | container-#2 fact |

## Gates run before HALT (all GREEN — this is not a setup failure)
- `bash bootstrap.sh` → ENV-PIN assert PASS · Guard 5 PASS.
- `git ls-remote … env-pin` = `3055ea5…` STRICT.
- Board built at head `3055ea5` (worktree; the working branch's later F7 engine has deleted `v0surf.pkl`).

See `HALT_container2_gate.md` for the recommendation (pin deeper: container/image or BLAS dispatch pin,
then re-run the two-container gate). Owner rules; nothing here bakes.
