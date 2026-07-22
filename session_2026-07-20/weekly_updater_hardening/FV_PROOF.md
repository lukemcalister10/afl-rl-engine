# FORWARD-VALUATION PROVENANCE + CONFIG-POLICY PROOF (gate OFF, scratch only)

Writes nothing to the real store (gate OFF: real-store apply refused = `True`).

## RESULT: **ALL PASS**  (426.6s)

Generated at `2026-07-21T09:06:13Z` for proof run `local-0b64c61bc2f742e38d6dd2104aa7a087`

## RED — the audit's defect (stale `21d530bf` on the RL_FV default path)
| check | value |
|---|---|
| ambient `/home/claude/rl_workspace/forward_valuation` distribution_pricing md5 | `` |
| that IS the stale `21d530bf` | False |
| R1: provenance guard HALTS on the ambient module | True |
| R1: provenance guard HALTS on unset RL_FV | True |
| R2: full apply with FV mis-bound to ambient HALTS before generation | True |
| R2: live files byte-identical, no ledger entry, txn `ABORTED_PRECOMMIT` | True |
| R3: adversarial inherited RL_FV forced back to the staged module | True |
| R3: board built is the staged module, never the stale one | True |

**The stale `d7a95e8d` board is never generated, pinned or committed.**

## GREEN — staged strict build
| check | value |
|---|---|
| store `968de0c7` → `615bfe77`, board `0083c756` | applied |
| distribution_pricing used (staged `dd19a234`, inside the staged repo) | `dd19a234` / True |
| not the stale `21d530bf` | True |
| RL_CONFIG_MODE=gate loaded the release manifest (config `45b207c03a8c`) | True |
| Guard 5 GREEN on the staged set | True |

## CONFIG POLICY (item 2)
| check | value |
|---|---|
| inherited `RL_LEGE=0` HALTS before any staging | True |
| live files byte-identical | True |

> Scratch-only, gate OFF. No numerical-determinism verdict is claimed; the FV binding guarantees the board is built from the STAGED valuation module, not an ambient/stale one.
