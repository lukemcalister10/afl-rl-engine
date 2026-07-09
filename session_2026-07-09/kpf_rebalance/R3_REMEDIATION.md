# R3 REMEDIATION — PVC fit held out of the bake (2026-07-09)

**Bake-stamp / manifest for the R3-compliant candidate. Supervisor-directed (owner path 1).**

## The defect
The W4 PVC fit is owner-ruled **held out at bake** (ruling R3, acceptance v1.5, 2026-07-08:
"RL_PVCFIT=0 at bake; re-derivation queued 'with a view to fixing it'"). But the engine default was
`RL_PVCFIT='1'` (ON) and `rl_export.py` inherited the ambient env, so the shipped board **`bcd81363`**
was generated with the fit **active** — its pick currency (`PVC`/`picks`/`intake*`) was the fitted
candidate curve, not the frozen v3.4 curve. The pick side moved **18–42% on picks 3–60** (the largest
owner-facing move in the candidate). Guard 5 asserts file md5s, not runtime lever state, so it did not
catch this; ship-gates **B4 passed only because it regenerated the same PVCFIT-on board** and compared it
to itself. The KPF session PLAN itself listed `RL_PVCFIT (off)` — the leak was accidental, not intended.

## The fix (compliant-by-default + unbakeable-wrong)
| file | change |
|---|---|
| `engine/rl_after/_merged_recover.py` | `RL_PVCFIT` default `'1'` → `'0'`. Frozen v3.4 curve (`_PVC0`) ships; `RL_PVCFIT=1` is experiment-only. |
| `engine/rl_after/rl_export.py` | **R3 BAKE GUARD**: board export HALTS if the fit is active, unless `RL_ALLOW_PVCFIT_BOARD=1` marks a non-bakeable experiment. |
| `BAKE_CHECKLIST.md` | §4 assertion: `RL_PVCFIT=0` at bake; verify the board embeds the frozen v3.4 curve. |
| `data/rl_build/rl_app_data.json` | Regenerated at defaults → board **`799b2290`** (frozen v3.4). |
| `data/expected_boot.json` | Pin `engine_head` → `4b08796c`, `board` → `799b2290`, R3fix tag. |

## Identity (this candidate)
| artifact | value | vs pre-fix |
|---|---|---|
| store `rl_model_data.json` | `e1b4d8bf` | unchanged |
| band `cm_400.pkl` | `34faa865` | unchanged |
| rl_model.py | `121a45d0` | unchanged |
| engine `_merged_recover.py` | **`4b08796c`** | was `275aa2a5` (comment + default flip only) |
| board `rl_app_data.json` | **`799b2290`** | was `bcd81363` (pick side → frozen v3.4) |

## Verification (this session, engine 4b08796c, store e1b4d8bf entry+exit)
- **Board delta PROVEN**: player rows `active` (805) / `back` (197) / `cohort` (1977) **byte-identical**
  to `bcd81363`; only `PVC`/`picks`/`intakeFull`/`intakePickSum` changed. New `PVC` = frozen v3.4
  (pk 1/2/4/8/20/60 = 3000/2501/2085/1706/735/308). Zero player value moved.
- **R3 BAKE GUARD**: `RL_PVCFIT=1 rl_export.py` → HALTS (exit 1), board not written.
- **Panel**: PASS 10/10 (player values unchanged).
- **Ship gates** (frozen suite): expected reds **A2/A3/A12** only; **B4 byte-agree `799b2290`**;
  B1/B2/B3/B5/B6/D14a-c PASS; A13/A14 PENDING (advisory vs frozen stand-in curve).
- **G-COHORT** (conforming, on the regenerated book): y4/y5/y6 = **128.8 / 127.3 / 119.6** ≤130 PASS
  (den = y1 63,758.1) — unchanged (PVCFIT-independent via `Vpath`).
- **All-levers-off** board = **`7d1eeef8`** — byte-exact baked v2.5.

## Not done here (owner)
The PVC re-derivation remains queued (R3, "with a view to fixing it"). The owner tags the reported head.
The BAKED marker moves only on the owner's ack (BAKE_CHECKLIST §7).
