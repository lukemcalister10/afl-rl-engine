# STORE-WRITE PROOF — weekly round-score APPLY (gate OFF, scratch only)

Writes **nothing** to the real store: the apply gate ships OFF (`APPLY_DEFAULT=False` + env `INGEST_SCORE_APPLY` unset); apply() on the real store refused (`gate_off_on_real_store=True`). Every write below is on a throwaway scratch repo.

## RESULT: **ALL PASS**  (666.4s)

## A — scratch round-15 apply (write + regen + re-stamp + Guard 5)
| field | value |
|---|---|
| store md5 | `968de0c7` → `15711cb3` (moved=True) |
| board md5 | `32b0944f` → `dbf36338` (moved=True) |
| players merged | 7 |
| all fed players moved on board | True |
| re-stamp coherent (store+board pins == written md5) | True |
| Guard 5 green on scratch (fresh boot) | True |
| dedup ledger entries after | 7 |

Board value moves (fed players, `v` before → after):
```json
{
  "darcy-moore": [
    257,
    279
  ],
  "harley-reid": [
    3348,
    3382
  ],
  "harry-sheezel": [
    7964,
    8060
  ],
  "josh-ward": [
    2003,
    2107
  ],
  "marcus-bontempelli": [
    3897,
    3943
  ],
  "max-gawn": [
    3416,
    3309
  ],
  "nick-daicos": [
    8017,
    7994
  ]
}
```

## B — dedup blocks the re-send
| field | value |
|---|---|
| re-sent round-15 refused | True |
| store unchanged by refused re-send | True |
| board unchanged | True |
| ledger unchanged | True |
| error | `round already applied (dedup ledger blocks re-send): 7 triple(s), e.g. ['afl-player-v1-25c` |

## C — season bound
| field | value |
|---|---|
| round 99 refused | True |
| bound | [1, 24] |
| store unchanged | True |

## D — 5× single-env board stability
| field | value |
|---|---|
| runs | 5 |
| byte-stable run-to-run | True |
| stable board md5 | `dbf36338` |
| matches proof-A board | True |

Per-run applied board md5s: `dbf36338, dbf36338, dbf36338, dbf36338, dbf36338`

> Single-env determinism only (this container, PYTHONHASHSEED=0 + single-thread BLAS).
> Cross-machine reproducibility is a separate item and is not attempted here.
