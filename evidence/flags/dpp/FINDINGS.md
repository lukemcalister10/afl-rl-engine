# FLAG (b) — DPP FORWARD-ELIGIBILITY — FINDINGS

**State:** baked subject `[BAKED c47cb43d]`; old-engine reconciliation `[OLD rl_model pre-merge]` · main `389ac39` · READ-ONLY
**Scripts:** `dpp_baked.py` → `dpp_baked.json`; `dpp_old.py` → `dpp_old.json`; `dpp_report.py` → `dpp_forward_eligibility.txt`, `dpp_merged.json`
**Population:** dual-position players = `len(_fut)>1` in the real store (94 total); **YOUNG = age ≤ 24 (49 players, 30 forward-eligible)**.

## What the flag is

A DPP carries `_fut = [[pos,weight],…]` (eligible future positions). The baked engine's
**only** reader of `_fut` is `gfut` = the **max-weight position**; it has no `futblend`
and no dual-premium (both lived in the pre-merge `rl_model.py` and were dropped —
`dist_redesign.py:30`: *"the DPP strip removes the forward-eligibility basis"*). So the
baked engine prices every DPP on its **primary (max-weight) position only**. This
diagnostic asks: what does a forward-eligibility-aware valuation add, per player?

## The headline is a divergence, not a single gap

Three measures, kept in their own engine's scale (**never subtracted across engines**):

| Measure | What it is | Serong | Young-DPP aggregate |
|---|---|---|---|
| **dOPT** `[BAKED c47cb43d]` | optionality: best-eligible-position ev − max-weight ev | **+$10** | Σ **+$5,953** (49) |
| **prem_fut** `[OLD rl_model]` | value(_fut) − value(bare listed pos) — reads dual/future role | **+$275** | +$1,210 over 5 lifted |
| **prem_2nd** `[OLD rl_model]` | value(_fut) − value([[max-wt,100]]) — 2nd-position blend, gfut held | **+$0** | net +$573 |

**The task's ~+$320 Serong anchor is the OLD engine's `prem_fut` (+$275; his stored
`_vpt`=377 == value(dual)).** It is the value of the engine reading his dual/forward
role (GDEF/MID, worth $377) instead of his bare listed tag (KEY_DEF, $102) — **not** a
second-position blend (`prem_2nd`≈$0, because his two eligible positions value alike).

## The baked engine has DROPPED — and partly INVERTED — that credit

In the baked engine the same eligibility is worth almost nothing, and for Serong it is
**mis-signed**:

```
jai-serong  pick 53 · cohort 2022 · listed KEY_DEF · _fut GDEF/MID
  BAKED  ev with _fut  (gfut GEN_DEF)  = $ 88
  BAKED  ev strip _fut (gfut KEY_DEF)  = $168     <- strip RAISES him +$80
  BAKED  optionality best (as MID)     = $ 98     -> dOPT +$10
  OLD    value(dual) $377 vs bare KEY_DEF $102     -> prem_fut +$275  (== ~$320 anchor)
```

Stripping `_fut` in the **baked** engine *increases* Serong's price (+$80) because his
listed KEY_DEF carries a lower replacement bar (REPL 68.4) than his projected GEN_DEF
(78.3) — the exact **opposite sign** to the old engine's +$275 lift. The $88-vs-$377
cross-engine gap is dominated by the baked sit-out/staleness machinery (he is `ns=0`,
thin career — see flag (c)) and scale, **not** by position value.

**Conclusion:** forward/dual-eligibility is effectively **unpriced (and occasionally
inverted) in the baked engine.** The overhaul's BEFORE-number is that the old engine
credited genuine cases like Serong **~$275–320**; the bake credits ~$10 optionality and
can even move the wrong way.

## Top young-DPP optionality gaps (baked engine, dOPT)

The largest per-player forward-eligibility-aware gaps the baked engine *can* express
(deploy at best-eligible line vs max-weight default):

| ID · pick · cohort | FWD-elig | current $ | best-eligible $ | dOPT |
|---|---|---|---|---|
| xavier-lindsay · 11 · 2025 | – | 1249 | 2207 | **+958** |
| jason-horne-francis · 1 · 2022 | FWD | 4166 | 4897 | **+731** |
| oliver-hollands · 11 · 2023 | – | 1401 | 2100 | +699 |
| jake-soligo · 36 · 2022 | FWD | 2503 | 3198 | +695 |
| tobie-travaglia · 8 · 2025 | – | 706 | 1396 | +690 |
| koltyn-tholstrup · 13 · 2024 | FWD | 1512 | 1890 | +378 |
| hudson-o-keeffe · FT · 2023 | FWD | 298 | 647 | +349 |
| bo-allan · 16 · 2025 | – | 1027 | 1371 | +344 |
| toby-murray · 7 · 2024 | FWD | 167 | 471 | +304 |

Full 49-row table in `dpp_forward_eligibility.txt`. Note dOPT is bidirectional: some
DPPs (dante-visentini −$416, sullivan-robey −$253) are priced on a max-weight position
worth *more* than their alternatives, so optionality would not lift them.

## Method notes / deliberate scope

- **Identity = ID(key)·pick·cohort(debutyr)** on every row; the two Serongs are
  disambiguated — only **jai-serong** is a young DPP; **caleb-serong** is `_fut` single
  (MID 100%), not a DPP, and is excluded by construction (stated, not silently dropped).
- The old-engine passes reproduce the stored board (jai `value(dual)`=377 == `_vpt`),
  so they are faithful to the pre-merge engine, not an ad-hoc recompute.
- `prem_2nd` isolates the second-position blend by collapsing `_fut→[[max-wt,100]]`,
  holding `gfut` fixed for all 94 (verified), so it is a clean blend-only measure.
- No sum-to-total guard is claimed for (b): the task asks for per-player gaps, and the
  measures live on two engines/scales that must not be summed together.
