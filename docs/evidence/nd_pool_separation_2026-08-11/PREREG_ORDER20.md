# PRE-REGISTRATION — ORDER 20, ND/POOL SEPARATION

**Written and committed BEFORE any measurement of this order was run.** Every prediction below is
falsifiable, numbered, and will be scored TRUE / BREACH in `SEPARATION_SUMMARY.md` with the measured
figure beside it. Orders 17/18/19 breached 4/6/7 predictions respectively and owned every one; that
is the standard this file is written to, not a failure state.

Pins asserted at entry of this order (all three verified before this file was written):

| pin | expected | verified at entry |
|---|---|---|
| board `data/rl_build/rl_app_data.json` | `94f1fec59f99c59d5890d5975c79fa9b` | ✓ |
| board `engine/rl_after/rl_app_data.json` | `94f1fec59f99c59d5890d5975c79fa9b` | ✓ |
| store `engine/rl_after/rl_model_data.json` | `d9a24282357cf3083b1640466e3ecd83` | ✓ |
| instrument `docs/evidence/composition_2026-08-10/noarb/noarb_table_338.py` | `0f8220351c64c56ccfa90c60edcdfa5f` | ✓ |

Branch `build/nd-pool-separation`, cut from `origin/main` = `d3d5f55`.

---

## THE LAW BEING TESTED

> "The ND and pool need to be entirely separated. Nothing here can impact ND pricing."

**SEPARATION LAW:** no change to any pool price, level, prior or surface may move any national-draft
price, the national pick curve, or `nd_profile`, **by any amount**. Zero tolerance, ASSERTED not hoped.

## THE TWO CLASSES THIS ORDER MUST DISTINGUISH — declared before measuring

This seat declares, before running anything, that the sweep will have to separate two different
things, because the order's candidate list mixes them and conflating them would let a real violation
hide behind an inert one:

- **CLASS A — LIVE PRICE-PATH CONTAMINATION.** A pool *price* or *level* is an input to a national
  price. This is the literal separation law. It is testable by perturbation and a non-zero residue
  is a **BLOCKER**.
- **CLASS B — POPULATION CONTAMINATION.** A national-arm quantity (a fit, norm, shrinkage target,
  stratum, band marginal, calibration target) is estimated over a row population that includes pool
  rows. Pool *outcomes* teach a national number. Perturbing pool *prices* may not move it at all, yet
  it still breaks the arm separation the owner asked for, and de-contaminating it moves national
  numbers **once**. That one-time delta is a REPORTABLE CONSEQUENCE, not a law breach.

Both are in scope for the sweep. Only Class A can be a blocker under the perturbation test.

---

## PREDICTIONS

### On the sweep (task 1)

| # | prediction | basis |
|---|---|---|
| **P1** | The sweep will find **at least 6** distinct sites (file:line) where a national-arm quantity is fitted/normed/shrunk/stratified over a population containing pool rows. | ORDER 19 named 2; the order's own candidate list names 5 more areas. |
| **P2** | `engine/rl_after/rl_model.py:283` `hist` (the `#336` layer's population) **includes pool rows** — every `RD`/`PSD` row and every ND row at pick ≥ 65 carry `_pool=True` and sit in `hist`. → **Class B violation.** | Read of `rl_model.py:267-283`. Structural, pre-measurement. |
| **P3** | `engine/forward_valuation/par_build.py:261-263` `gather()`'s `pool` list has **no `is_pool` filter**, so `build_pest`'s all-position band marginal (`bnum[b]/bden[b]`, `:211`, consumed at `:226-228` with `K_338`) is a **mixed-arm** shrinkage target. → **Class B violation.** | Read of `par_build.py:205-263`. Structural. |
| **P4** | The pick-curve **builders** (`build_pvc` / `_natcv34`) will be found **clean** — `_teaches_curve` (`rl_model.py:313`) already gates them on `not is_pool`. The contamination is in the layers around the curve, not the curve builders. | `rl_model.py:296-313` THE SPLIT ADDENDUM 1. |
| **P5** | `R_SURF` (`_merged_recover.py:1123`) is a **frozen literal table**, not re-derived at runtime, so it is a **historical** Class B contamination (its producer had no `_pool` filter) with **zero live perturbation channel**. | Read of `_merged_recover.py:1110-1132`. |
| **P6** | At least one site will be found that this seat has **not** anticipated in P2/P3/P5 — i.e. the sweep is not merely a confirmation of ORDER 19's two. | Priors from orders 17-19: every sweep found more than the order named. |

### On the fixes (task 2)

| # | prediction | basis |
|---|---|---|
| **P7** | De-contaminating the `#336`/`BASEPK` layer (restricting `hist`'s *fit* population to non-pool rows) **WILL move national board prices** by more than 0.01% on at least one row. | The pool is ~35% of `hist` by row count and sits entirely in the last band. |
| **P8** | The magnitude of the whole-board national total move from all Class B fixes combined will be **between 0.1% and 5.0%**. | Order-of-magnitude guess. Deliberately wide; a miss outside it is a real miss. |
| **P9** | De-contaminating `structural_values`' completion strata will move `nd_profile` by a **non-zero** amount, and by **less than 1.0%** in absolute terms. | ORDER 19 measured a −0.1939% drift from a *pool price perturbation*; the population fix is a different and probably larger lever, but same order. |
| **P10** | **No fix in this order will require changing a shipped default dial.** Every fix is a population filter, not a parameter change. | Design intent. |

### On `daniel-butler` (task 3)

| # | prediction | basis |
|---|---|---|
| **P11** | The record **WILL settle** `daniel-butler` — i.e. the store will carry an unambiguous `type` and `pick` that place him on exactly one side, and the disagreement will prove to be an **instrument** artefact (the matrix's slid pick), not a genuine ambiguity in the source data. | The engine already classifies him `_pool True, effpk 65`; the engine's classification is the authority under `rl_model.py:267`. |
| **P12** | He is a **pool** row: a national selection at pick ≥ 65, which `rl_model.py:267` sends to `POOL_PICK` explicitly. | Same. |

### On the separation test (task 4)

| # | prediction | basis |
|---|---|---|
| **P13** | Under the **shipped** engine (before any fix in this order), a large pool-price/level perturbation will move **at least one** national-draft board price or `nd_profile` by a non-zero amount — i.e. the test will FAIL on HEAD. Specifically `nd_profile` will move. | ORDER 19's −0.1939%. |
| **P14** | After this order's fixes, the perturbation test will pass at **EXACTLY ZERO** (bitwise-equal national prices, `nd_profile` delta 0.0 exactly, not "< 1e-12") for **every** perturbation tried. | This is the order's success condition. |
| **P15** | The `daniel-butler` row will be the **only** national-teaching-population row that a pool perturbation can reach, and removing him will close that channel entirely. | ORDER 19 named him as the sole crosser. |
| **P16** | At least **4** distinct perturbations will be tried, including at least one ≥ 50% in magnitude, and the test will be committed as a re-runnable script with its output. | Commitment, not a guess. Scored on whether it was done. |

### On the board (constraint)

| # | prediction | basis |
|---|---|---|
| **P17** | The live board `94f1fec5…` **WILL move** under the Class B fixes, so nothing will be shipped and this order will stop at the PR with the delta reported. | Follows from P7. |

---

## WHAT WOULD MAKE THIS ORDER A BLOCKER RATHER THAN A DELIVERY

Declared in advance so it cannot be rationalised after the fact:

1. A **non-zero residue** in the perturbation test after the fixes — reported with size and mechanism,
   not worked around.
2. `daniel-butler`'s side **not** settleable from the record — STOP, do not pick a side.
3. A fix that would require a **shipped default dial** to change — out of scope for this order.

---

*Committed before measurement. `git log` is the timestamp.*
