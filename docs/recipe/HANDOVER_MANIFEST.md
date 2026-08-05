# HANDOVER MANIFEST — the complete ingredient set for a fresh rebuild

2026-08-05 · A fresh repo receives the files below plus `RECIPE.md` and `FINDINGS.md` — and NOTHING else from this repository. The verification appendix, the engine code, the guards, the evidence trees and all governance pins stay behind.

## 1 · Data files (ship all of these)

| file | size | md5[:8] | what it is |
|---|---|---|---|
| `engine/rl_after/rl_model_data.json` | 1,960,480 B | `81d24704` | THE STORE — 2,651 player records: identity, entry route/pick, positions, birth year, season scoring rows |
| `data/season_state.json` | 864 B | `1f933e26` | season clock — year, rounds, current round, calendar progress, exposure pace |
| `engine/rl_after/params.json` | 1,638 B | `453c1a26` | per-position peak score, peak age, empirical age curves |
| `engine/rl_after/rl_passmark.json` | 4,701 B | `93239011` | expected-score curves per pick band / band+position, band definitions, bust-rate priors |
| `engine/rl_after/ycred_table.json` | 176,469 B | `123aa9dc` | young-player expected-improvement credit grid by pick |
| `engine/rl_after/bust_prior_table.json` | 5,398 B | `5942aa6a` | bust probability priors, position x pick 1-70 |
| `engine/rl_after/pvc_curve_v2.json` | 5,257 B | `cdc50a2f` | adopted pick-price curve, picks 1-64 + pool value (SUPERSEDED ladder - see note 1) |
| `engine/rl_after/pick_redenomination.json` | 2,847 B | `2765f83d` | the 1.0524 board-currency divisor |
| `LTI_REGISTER.md` | 8,064 B | `652d83e8` | owner-authored injury/availability register |
| `engine/rl_after/lti_return_table.json` | 1,156 B | `6a4800e8` | age-indexed return-season haircut surface |
| `data/owner_overrides.json` | 1,367 B | `f5f2967d` | owner display-only override list |
| `engine/rl_after/national_draft_last_pick.json` | 7,068 B | `35815ab1` | last national pick per draft year (display offset only; stale in 4 of 23 years - see note 2) |

**Note 1:** the pick curve shipped here is the superseded ladder; the redesigned ruled curve replaces it at the Track A landing — hand the rebuild the ruled artifact once it lands (or now, from the loop's evidence, clearly labelled unconverged).

**Note 2:** carried for completeness; its only live role is a display offset and it disagrees with the store in 4 of 23 years (recipe List 1 item 31).

## 2 · The frozen fitted models — OWNER DECISION PENDING

| file | size | md5[:8] | what it is |
|---|---|---|---|
| `data/v0surf.pkl` | 148,626 B | `b540833b` | frozen year-zero start-value surface (lens) |
| `data/cm_400.pkl` | 4,174,555 B | `34faa865` | frozen five-quantile forward-band tree ensemble |
| `data/q97m.pkl` | 387,567 B | `cfdc7321` | frozen 97th-percentile ceiling model |
| `engine/rl_after/peak_model_v4.pkl` | 1,341,030 B | `f305fe53` | frozen peak-projection model (currency-anchor role only) |

Two options: (a) ship them as sealed jars — the rebuild reproduces today's outputs but inherits four artifacts nobody can re-derive; (b) withhold them — the rebuild fits its own simple equivalents from the training rules stated in the recipe (List 2 steps 11-13, 32; List 3 steps 27-31, 35-36) and is judged on board-level closeness, not byte equality. **Recommendation: (b)** — it matches the goal of a simpler rebuild without this project's machinery, and the findings say exact reproduction is impossible anyway.

## 3 · Explicitly NOT handed over
Engine code, boot/governance pins, release contracts, boards and seals, CI, evidence trees, session archives, the verification appendix. The rebuild sees ingredients and recipe only.
