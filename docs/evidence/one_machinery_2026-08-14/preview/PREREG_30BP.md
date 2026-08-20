# PREREG — ORDER 30B-P, THE STEP-3 PREVIEW BOARD

**FILED BEFORE ANY PREVIEW QUANTITY IS MEASURED.** Committed and pushed before the first preview build
runs. The preview lane's code was written first (it has to exist to be dialled), the DIAL-OFF control was
run first (it is a control on the committed state, not a preview reading), and then this file was filed.
No preview board, no preview price and no age-lens cell had been computed when these numbers were written.

**ORDER 30B-P preview seat · `land/order-29` · 2026-08-15 · brief: #334 comment `5299562714`.**

---

## 0 · THE LINE, RESTATED AT THE TOP

**NOTHING IS GREENLIT.** The Step-3 forbidden-set boundary word (STOP §5 Q1–Q4) is still **OPEN**. This
order wires the seat-recommended configuration **behind one new declared dial, `RL_O30B_PREVIEW`,
DEFAULT OFF**, so the owner can rule from a board instead of from prose. **THE PREVIEW IS PRE-NUMERAIRE** —
Step 6's re-pin has not run and every table this order emits says so on its face. Steps 4–7 are not
started. No pool value is derived. PR #510 stays HELD.

---

## 1 · WHAT THE PREVIEW WIRES (declared here so the expectations below are about a fixed object)

For a row that **has evidence** at `Y`:

```
price(p,Y) = (1 - sigma(g)) x production(p,Y)  +  sigma(g) x pedigree(p)
```

| element | the exact object |
|---|---|
| the dial | `RL_O30B_PREVIEW`, default `0`. It **implies** `_O30B_NOPOLE` and `_O30B_NOISO` through the `or` at `_merged_recover.py:409-411`, so the pole and the par-built ISO pick-tax are deleted **through the two existing ablation lines** (`:487` `:517`) and no third deletion path exists. |
| `production` | the finished production leg at the blend site in `ev()`: pole deleted, ISO deleted, and the **retained** bars/aging/form machinery applied — ITEM H's ruled cuts, the ruck ceiling (ITEM E2), the KPF compression, D8 graded staleness and the decay gate. |
| `pedigree` | the **STEP-1 positional v0**, `day0_v0(p)`, converted BOARD → ENGINE by `_PL_F = 1.0524`. ND in-curve: `nd_v0.posv[gfut][pick]`. Pool: the signed `pool_v0` cell through `MA.pool_v0_of`, which halts on an unsigned cell. **The numéraire `s` is already inside both**, so `x _PL_F` is the only conversion — the identical conversion ORDER 29B's own day-0 branch performs. |
| `sigma(g)` | `exp(-(g/23.0)^0.80)` — the 30B-M packet §6 **refit of ruling 4's own functional form** to the five measured band midpoints (2.5 → 70.1% · 10.5 → 66.4% · 25.5 → 33.1% · 53.0 → 16.5% · 85.5 → 2.2%). **This is the declared interpolation between the band midpoints.** The raw log-linear midpoint interpolation is published alongside as `sigma30bp_raw` and is **not** wired. |
| `g` | career games as of `Y`, never future. **Ruling 5:** an MSD row's entry-season games are credited at `cp.SEASON/12` per game; every other season on every route is 1:1. |
| the two re-referenced denominators | `_c_w`'s `Q = clip(sa/par,0,2)` and `ev`'s decay gate `pr = bestlvl/par` **keep their form, their clip and their constants**; only the denominator object moves, from `PR.par_at(pos, effpk, T)` (a par table read at the player's own pick) to `_O30BP_BARS[pos] = MA.REPL[pos] - rd.REPL_DROP[pos]` — the **effective positional bar**, position-level and pick-blind, the same object 30B-M read live off the engine and asserted against Ruling 1 (KPD 65.4 · KPF 63.8 · MID 77.1 · RUCK 75.5 · SD 75.3 · SF 67.9). |
| replace-not-wrap (STOP §5 Q4) | `_a_blend` (ITEM A's anchor carry), `sitout_ev`'s `ns==0` arm and the year-zero floor `floor_frac x entry_anchor` are **REPLACED** in the preview lane, not wrapped. `_c_w`, `C_H`, the ruck ceiling, ITEM H, D8 and the KPF compression **survive** — they are an evidence weight, a ceiling and form machinery, not anchor blends. |
| no stacking | zero-evidence rows are intercepted by `_entry30b_price` **above** the preview lane and keep the Step-2 fade `v0 x D(c)` untouched. A played row carries an **unfaded** pedigree leg at weight `sigma(g)`. The two branches are mutually exclusive by predicate, so `(1-w)` and `D` can never multiply. |

---

## 2 · THE PRE-MEASUREMENTS, RECORDED SEPARATELY AND LABELLED AS SUCH

Three quantities were read off the **committed Step-2 engine** while the preview lane was being written —
before the preview existed. They are recorded here so they cannot later be mistaken for predictions.

| # | measured on the Step-2 engine, pre-wiring | value |
|---|---|---|
| M1 | rows priced at `Y=2026` that are **not** day-0 | **715** (89 day-0; 804 total) |
| M2 | rows carrying evidence with **no** `day0_v0` pedigree object | **0 of 715** — the blend can be formed for every row |
| M3 | `par_at(site 3)/bar` over the 715 rows | min 0.626 · p25 0.765 · **med 0.805** · p75 0.890 · max 1.083 |
| M4 | `par_at(site 4)/bar` over the 715 rows | min 0.626 · p25 0.909 · **med 0.994** · p75 1.052 · max 1.270 |
| M5 | `Q` under the two denominators | par: mean 1.0809 med 1.0637 → **bar: mean 0.8834 med 0.8847** |
| M6 | rows the decay gate reaches (`el>=onset+2`, `pr<0.55`, `ns>=1`) | par denominator **2** (`campbell-chesser`, `finlay-macrae`) → bar denominator **0** |

And the standing baselines this order is scored against, all from committed evidence:

| board | md5 | total |
|---|---|---:|
| live (main) | `88ce647f` | — |
| Step-2 provisional | `9298203135202a0c707bb0977ba38c31` | **706,672** |
| ablation A — pole deleted, no blend | `554c49df` | 687,399 |
| ablation B — pole + ISO deleted, no blend | `7b17962a` | 689,765 |

---

## 3 · THE NUMBERED EXPECTATIONS

**P1 — DIAL-OFF BYTE IDENTITY.** With `RL_O30B_PREVIEW` unset and both ablation dials unset, the build
reproduces **`9298203135202a0c707bb0977ba38c31`** byte-exact, total 706,672. *(Run before this file was
filed; recorded here as the control it is, and scored as filed.)*

**P2 — PRINTED DAY-0, 89 OF 89, TOLERANCE 0, UNDER THE PREVIEW.** Zero-evidence rows never enter the
preview lane, so all 89 day-0 prices are **byte-identical** to Step-2 and the restated identity
`printed == round(v0 x D(c))` holds at tolerance 0. Predicted: **89/89**, and all 89 rows show `Δ = 0`
against Step-2 in the movers table.

**P3 — DETERMINISM.** Two independent preview builds, each from a freshly staged tree under the pinned
five-var environment, produce **the same board md5**.

**P4 — POPULATION.** Exactly **715** rows carry the blend, **89** keep the Step-2 fade, **804** rows on
the board. **Zero** population changes (no row added, no row dropped) versus `92982031`.

**P5 — BOARD TOTAL BAND.** The preview total lands in **[640,000 , 730,000]** and the **direction is
DOWN** versus Step-2's 706,672. Reasoning filed blind: the pole+ISO deletion alone measured −16,907
(ablation B) before any blend, and the blend then replaces two anchor-LIFTING objects (ITEM A's carry and
the year-zero floor) with a single pedigree leg whose weight is under 4% past 71 games — where most of
the board's value sits.

**P6 — MOVER COUNT.** **≥ 700 of 804** rows move against `92982031` (every one of the 715 evidence rows
except a handful whose blend rounds to the same integer). **Zero** of the 89 day-0 rows move.

**P7 — THE KAKO BAND, AS THE BRIEF STATES IT: 900–1000.** `isaac-kako` (ND 2024, pick 13, SF, 36 games,
Step-2 price 1320) prints in **[900, 1000]**.
*Seat note, filed blind and before any component was computed:* this expectation is dominated entirely by
the size of kako's pole-free, ISO-free **production** leg, which has never been measured on its own.
`sigma(36) = 0.2391` and his pedigree leg is the Step-1 positional v0 for SF pick 13, **759.77 board
points** — so the pedigree contribution is ≈ **182 board points** and the band requires a production leg
of roughly **945–1075**. Ablation B printed him at **744**, and that number *included* ITEM A's anchor
lift, so it is an **upper bound** on the production leg alone. **The seat therefore expects this band to
BREACH LOW, and files the band as the brief states it rather than substituting its own.** If it breaches,
the seat owns the breach and does **not** move the wiring to reach the band.

**P8 — THE MOVER CLASS.** The movers are overwhelmingly the **established** book, as ablation B already
showed (293 rows / −15,045 in `cg 16+`). Predicted: the `cg 16+` class carries **≥ 60%** of the movers
and **the majority of the summed delta**. Direction predicted: `cg 16+` **DOWN** (the pedigree leg is
worth under 4% of a long career's price and it displaces production), `cg 6–70` **UP relative to ablation
B** (the blend restores a pedigree leg the ablation had removed).

**P9 — THE AT-BAR / TREMBATH CLASS RE-REFERENCES, IT DOES NOT FADE.** Rows sitting at or near their
positional bar with mid-career games show a **smaller `|Δ%|`** than the star class (`cg 100+`, top-decile
price). Predicted as a class statement, checked as one.

**P10 — THE RE-REFERENCED DENOMINATORS, BOARD CONSEQUENCE.** Given M5 and M6 above, predicted:
`campbell-chesser` and `finlay-macrae` — the only two rows the decay gate reached under the par
denominator — print **HIGHER** under the preview than the same configuration would print with the par
denominator retained; and no row **enters** the gate.

**P11 — THE FIRST-GAME STEP. THE SEAT PREDICTS RULING 6's CONTINUITY CURVE FAILS AT 0 → 1 GAME UNDER
THE PREVIEW AS SPECIFIED, AND WILL REPORT IT RATHER THAN FIX IT.** The no-stacking constraint sends a
gameless row to `v0 x D(c)` and a one-game row to `sigma(1) x v0 + (1-sigma(1)) x production` with
`sigma(1) = 0.9218`. For a depth-2 sitter `D(2) = 0.5502`, so the first game is predicted to be worth a
step of **≥ +40%** of the row's price. This is a property of the **constraint as ruled**, not of this
implementation; the seat measures the step, reports it as an **owed owner word**, and does **not** choose
a smoothing.

**P12 — THE AGE LENS (filed blind, against the owner's 36-early-vs-36-late question).** Within the 16–35
and 36–70 games bands, split by age-at-state (≤20 / 21–22 / 23+): the seat predicts **age does NOT move
the share at fixed games with the power available** — specifically that the ≤20 and 23+ cells' σ 90% CIs
**OVERLAP in both bands**. If they do not overlap, the wiring implication (an age term in the share
curve) is stated as an **OWED WORD** and is **NOT applied**.

**P13 — THE SELECTABILITY COUNTERFACTUAL.** For every named row, `preview price > sat-counterfactual`
(`v0 x D(c)`, the pure sitter at the same clock). Predicted **strictly, for all six** named rows
(`isaac-kako`, `willem-duursma`, `dyson-sharp`, `jacob-farrow`, and the two additional named rows the
brief lists once they are resolved in the store). The claim under test is that the new law **pays for
playing**.

**P14 — NOTHING OUTSIDE THE LANE MOVES.** `rl_model.py`, `rl_model_data.json` (the store),
`data/v0surf.pkl`, `engine/rl_after/pvc_curve_v2.json` and every committed board file are **unmoved**;
no numéraire re-pin runs; Steps 4–7 are not started; PR #510 stays HELD.

**P15 — POOL ROWS ARE PRICED, AND LABELLED PROVISIONAL.** Pool rows are priced under the **same** formula
with their **own** pool `v0` cells and the same σ curve, and **every** pool row in every table this order
emits carries the label *"provisional — pool values pending Step 4"*.

---

## 4 · SCORING RULE, FIXED IN ADVANCE

Each expectation is scored **HELD** or **BREACHED** on its **first** reading. A breach is owned in the
packet with its number and its measured value, and **nothing is re-tuned to reach a filed band** — if a
number lands outside a band, the band was wrong or the configuration is wrong, and both of those are the
owner's to rule, not the seat's to close. Every board is built **once** per configuration from a freshly
staged tree, sequentially, under the pinned five-var environment.

---

*Filed at `land/order-29`. The preview lane's dial-off byte-identity control had been run; no preview
board, no preview price and no age-lens cell existed when this file was written.*
