# PRE-REGISTRATION — ORDER 5 (the stacked row, and the per-player board comparison)

**Filed BEFORE the stacked emit ran.** Owner order, verbatim: *"How much effort would it be to look at
the different player values on the current board between XW, V5, and a stacked version (and also the
'menu' table including that stacked option)"*. Breaches are reported as breaches; nothing is retuned.

Instrument: `noarb_table_338.py` UNMODIFIED (md5 `0f8220351c64c56ccfa90c60edcdfa5f`), pooled
Σprice/Σanchor over the harness loader's own population (1197 ND entrants, picks 1-64, classes
2004-2022), EXPECT_N re-measured on the new matrix.

## The two components, as measured, and what a stack starts from

| row | yr1 | Δyr1 vs FULL | yr4 | Δyr4 | own disc @18 | margin |
|---|---|---|---|---|---|---|
| FULL | 0.9974 | — | 1.5310 | — | 14.00% | +14.26% |
| FULL+XW | 1.0884 | **+0.0910** | 1.5660 | +0.0350 | 14.00% | +5.16% |
| FULL+V5 | 1.0734 | **+0.0760** | 1.5665 | +0.0355 | 12.00% | +4.66% |
| naive sum of the two lifts | **1.1644** | +0.1670 | 1.6015 | +0.0705 | — | — |

## SHARED-CODE ASSERTION — checked before the emit, and one re-emit ordered because of it

The two dials are read at **disjoint sites**, verified by repo-wide search: `RL_336_XW` appears only in
`engine/forward_valuation/par_build.py`; `RL_AGE_DISC_MODE` only in `engine/rl_after/rl_model.py`.
Neither reads the other, and neither is in the other's call path.

**But the assertion is not free, and one row is re-emitted rather than assumed.** `git diff` from the
V5 emit commit (`de51561`) to the ORDER 5 tip shows **`par_build.py` changed** (the ORDER 4 wiring).
The V5 matrix was therefore emitted against a different `par_build.py` than the stack will be. The OFF
path is byte-exact by proof, so V5 *should* reproduce exactly — **so it is re-emitted as `V5B` and
compared byte-for-byte against the ORDER 3 matrix.** If `V5B.recs != V5.recs`, the off-path identity
claim is false and the whole stacked comparison is void.

`XW` needs no re-emit: `git diff a56f43f..c06824c -- ':!docs'` is **empty** — no engine or data file has
changed since the XW matrix was emitted.

## PREDICTIONS

**P5.1 — the stack lands ABOVE each component alone.** Both lift year 1 through different machinery.
Predicted yr1 **> 1.0884** (the larger of the two). *Falsifier: at or below 1.0884.*

**P5.2 — SUB-ADDITIVE overall: the stack lands BELOW the naive sum 1.1644.** Both act on the same young
rows, so the second lift has less left to lift. Predicted yr1 in **1.12 – 1.16**.
*Falsifier: yr1 ≥ 1.1644 (super-additive) or ≤ 1.0884.*

**P5.3 — THE SIGN OF THE INTERACTION IS NOT ASSUMED, AND IS CHECKED PER ROW.** There is a mechanical
route to SUPER-additivity: XW raises the par levels, and par feeds the peak estimate and ITEM C's
`Q = sa/par`, which is part of what V5's age-keyed discount is then applied to. So on some rows the
combined move may exceed the sum of the separate moves. **No prediction is made on the direction; the
per-row count of super-additive rows (|Δstack| > |ΔXW| + |ΔV5|, same sign) is MEASURED and printed.**

**P5.4 — THE STACK IS AT REAL RISK OF ARBITRAGE, and this is the decisive question of the row.**
Margin is computed against **V5's own young rate, 12.00% at draft age 18** — the tighter frame, because
the stack carries V5's discount schedule. A yr1 landing above **1.12** puts appreciation above the 12%
charged and the margin goes negative. Predicted margin **−4% to +1%, expected NEGATIVE (ARB)**.
**If it lands ARB, the finding is that two candidates each legal alone become illegal stacked** — which
is exactly the thing a menu table must show and a naive reader would not expect.
*Falsifier: a margin at or above +1%.*

**P5.5 — yr4 rises and the peak-estimate caveat still applies.** Predicted yr4 in **1.585 – 1.615**.
Both components already move yr4 (XW +2.29%, V5 +2.32%), and V5's own yr4 move runs through the peak
estimate, which is itself a forward-discounted object. *Falsifier: yr4 outside that band.*

**P5.6 — year-zero prices do not move beyond the one pre-existing row.** Predicted **≤ 2 v0 movers** of
1197 and sum(v0) within **0.05%**. *Falsifier: more.*

## THE BOARD COMPARISON — the law that governs it, carried on every artifact

> **These numbers attribute movers. They decide nothing.**

The cohort book on the canonical instrument is the deciding instrument for this act. The live board is
a **cross-section**, and this project has a standing finding that live-board cross-sections were the
wrong basis for the cohort and no-arb readings. The per-player board files exist because the owner
asked what happens to *individual players*, which a pooled ratio cannot show. **No candidate is
selected, ranked or recommended on a board number.**

Four boards, all built at the SAME final tip with the pinned environment
(`RL_CONFIG_MODE=gate`, `PYTHONHASHSEED=0`, all BLAS thread counts 1): FULL, FULL+XW, FULL+V5,
FULL+STACK. The shipped board (`data/rl_build/rl_app_data.json`, md5 `4b448a821f54180182637983f7a26a9d`)
is carried as the `main` column so the owner can see where each player stands today.

**P5.7 — the DISAGREEMENT set is non-empty.** XW acts on the par benchmark and V5 on the age discount.
They are different mechanisms, so some players should move in **opposite directions** under the two.
Predicted **> 0** such players. *Falsifier: 0 — which would mean the two are the same lever in disguise
and the stack is not a stack.*
