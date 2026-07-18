# RIDER (report-only) — engine-side R inputs: the free-intake pick-equivalents

Items 326/327; rider (iv) waits on this. **Report only — no engine value change, not a gate.** Emitted
from the migrated engine (`RL_PVC2=1`, default); artifact `out/rider_R_inputs.json`.

The "free-intake" (no national-slot) mechanisms enter the board at a **pick-equivalent** derived by
`_pick_equiv` inverting each mechanism's pooled realised value against the national realised-value curve
`_natcv34`. These are the R inputs.

| mechanism | name | pick-equiv (R) | cohort n | played n | cutoff |
|-----------|------|:---:|:---:|:---:|:---:|
| MSD | Mid-Season | **90** | 44 | 17 | 2021 |
| SSP | SSP / pre-season supp. | **92** | 31 | 16 | 2022 |
| IRE | Ireland | **92** | 48 | 13 | 2021 |
| UNR | Unregistered | **92** | 46 | 13 | 2021 |
| PDA | Post-draft Academy | **92** | 38 | 10 | 2021 |
| PDN | Post-draft Next-Gen | **92** | 24 | 4 | 2021 |
| PDS | Post-draft Scholarship | **92** | 21 | 4 | 2021 |

## Invariance note (relevant to the five-migration)
These pick-equivalents are **curve-independent**: measured byte-identical at `RL_PVC2=0` and `RL_PVC2=1`
(`_natcv34`/`_pick_equiv` read realised outcomes, not the PVC curve — see `JOB_natcv34_NULL_PROOF.md`).
So the migration does not disturb the R inputs; this report is stable across the kill-switch. MSD sits
one pick shallower (90) than the rest (92), reflecting its higher pooled realised value per the cohort.
