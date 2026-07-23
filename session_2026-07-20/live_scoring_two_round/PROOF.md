# Sequential two-round live-scoring proof — Round 15 → Round 16 (gate OFF, scratch only)

Writes **nothing** to the real store (gate ships OFF: `APPLY_DEFAULT=False` + env `INGEST_SCORE_APPLY` unset; real-store apply refused = `True`). Round 16 is applied in a **fresh process** after a full stop; the scratch `expected_boot.json` is stamped coherent with the scratch engine (release identities supplied to the fixture).

## RESULT: **ALL PASS**  (942.4s)

| # | proof | result |
|---|---|---|
| 1 | R15 preview validates identities + score meaning | ✅ |
| 2 | R15 apply updates the scratch store atomically | ✅ |
| 3 | R15 board generated from the updated store | ✅ |
| 4 | value+rank history records R14->R15 for every active player | ✅ |
| 5 | process fully stopped + restarted (fresh process reads committed state) | ✅ |
| 6 | R16 preview based on the R15 committed state | ✅ |
| 7 | R16 apply updates store+board atomically (fresh process) | ✅ |
| 8 | history records R14, R15, R16 without overwriting earlier | ✅ |
| 9 | re-sending R15 or R16 is blocked (dedup) | ✅ |
| 10 | stale R16 preview (pre-R15 change) is blocked | ✅ |
| 11 | altering preview after approval is blocked (content hash) | ✅ |
| 12 | player-universe mismatch / unresolved residue is blocked | ✅ |
| 13 | failure injection before/during replacement -> no partial state | ✅ |
| 14 | hard exit mid-commit detected; next run refuses until recovery | ✅ |
| 15 | recovery restores byte-identical files + keeps evidence | ✅ |
| 16A | UI extraction after committed R15 board -> coherent bundles | ✅ |
| 16B | UI extraction after committed R16 board -> coherent bundles | ✅ |
| 17 | no production / release-candidate files touched | ✅ |
| GATE | gate OFF: real-store apply refused (nothing written) | ✅ |

### Store / board / history hashes (the sequential chain)
```
R14 (fixture baseline) store 968de0c7  board 2ab73a6f
R15 apply              store 66cc4879  board 06c578d1   value/rank rounds [14, 15]
R16 apply              store 9c88c550  board c92fda2e   value/rank rounds [14, 15, 16]
```

> Single-env, scratch-only. No cross-run/cross-machine numerical-identity verdict is claimed — the board is validated for structure, source-stamp/pin coherence, Guard-5 pins, player universe and history integrity, under the accepted fail-closed forward-valuation path.
> The 7-point failure-injection + crash-recovery matrix is proven in `../weekly_updater_hardening/PROOF.md`; step 13/14/15 here re-prove no-partial-state and recovery in the two-round context.
