# PRE-REGISTRATION — ORDER 21, THE POOL SIT-OUT RETENTION, DERIVED ON POOL DATA

**Committed BEFORE any measurement was run.** Every prediction below is scored in
`POOL_RETENTION_SUMMARY.md` §BREACHES, whether it holds or not.

Pins asserted at the moment of writing (and re-asserted at the entry and exit of every instrument):

| pin | path | md5 |
|---|---|---|
| board | `data/rl_build/rl_app_data.json` | `1dbd1480a34c7823f330273211cbb76a` |
| store | `engine/rl_after/rl_model_data.json` | `d9a24282357cf3083b1640466e3ecd83` |
| instrument | `docs/evidence/composition_2026-08-10/noarb/noarb_table_338.py` | `0f8220351c64c56ccfa90c60edcdfa5f` |

Branch base: `origin/main` @ `c330169` (the par fix landed; the board pin CHANGED from the `94f1fec5`
that ORDER 19's evidence carries).

---

## §A — THE DERIVATION SPECIFICATION, FIXED IN ADVANCE

This is the method, written down before the data was looked at, so that no step is chosen after
seeing a number. It mirrors `session_2026-07-03/d13/scripts/d13_derive.py` +
`d13_norm_harvest.py` (the ND retention derivation) except where a DEPARTURE is declared.

**A1. THE SITTER POPULATION, DEFINED ONCE.**
A *cell* is one (player, season) pair. The population is:

- **pool rows only** — `p.get('_pool')` is true. **Zero national rows in any fitted cell** (asserted).
- draft years `dy = debutyr - 1` in `[2003, 2024]`;
- seasons `Y` in `[dy+1, min(listed_through(p), 2025)]` — the still-listed window, `listed_through`
  and `min_window` carried verbatim from the ND harvest;
- **complete-window** cells only for the derivation: `Y <= 2021` (so the 4-year forward outcome
  window is closed). Incomplete cells are harvested and reported but do not fit.
- **depth** `d = Y - dy`, an integer on completed seasons.
- **A cell is a SIT-OUT iff the player has no season of `games >= 6` at or before `Y`.**

This is the `nseas_pro == 0` test evaluated on completed seasons, i.e. **exactly the gate that admits
a row to `sitout_ev` in `ev()`**. It is NOT `_h_cut`'s test (`games this season <= 0`). ORDER 19
measured that those two bite different populations; this derivation adopts the `sitout_ev` population
and `_h_cut` retires entirely, so the second population ceases to exist in the engine for pool rows.

**THE MID-SEASON BOUNDARY.** The engine's depth clock is
`tau = max(0, Y - debutyr) + fE**1.5` (`sitout_ev:1962`, `_a_blend:2176`), which at a completed season
(`fE = 1`) equals `Y - debutyr + 1 = d`. The derivation's integer knots therefore sit exactly on the
engine's integer tau knots. Mid-season 2026 (`fE = SEASON_PROG = 0.58`) gives
`tau = (d-1) + 0.58**1.5 = (d-1) + 0.4417`, and the engine interpolates between the knot below and
above — the D12 concave proration, unchanged. `tau = 0 → R = 1.0` (no penalty before a season starts,
Luke 2a) is preserved. **The in-season boundary maps by interpolation on the engine's own clock; no
new convention is introduced and none is inherited ambiguously.**

**A2. THE MEASURE.**
`O(p,Y) = price6(p, [L]*6, Y)`, `L = max(x['avg'])` over seasons `Y < x['year'] <= Y+4` with
`x['games'] >= 6`; `O = 0` if none. `r = winsor(O / DENOM, 2.0)`.

**A3. THE NORM.** `norm(cls, d) = mean(r)` over **all** pool cells at that class and depth
(developer-inclusive, same depth) — the ND construction, which strips the survivor-selection
common-mode.

**A4. THE SMOOTHER.** `r_sit` at `(cls, d)` = Gaussian kernel local mean over the depth axis,
`bwd` grown through `[0.75, 1.1, 1.6, 2.5]` until `eff-n >= 35`; widest carried and declared thin
otherwise.

**A5. THE SURFACE.** `R_pool(cls, d) = clip(r_sit / norm, 0.05, 1.0)`, then **ISOTONIC
NON-INCREASING IN DEPTH** (downward-only running cap — the owner's signed law).

**A6. THE PATHWAY LAYER.** For cell `(pathway, cls, d)` with sitter count `n >= 20`, the cell fits on
its own data (own kernel estimate ÷ that pathway's own same-depth norm). Otherwise it is partially
pooled toward the whole-pool cell:
`v = w*own + (1-w)*R_pool(cls,d)`, `w = n/(n+10)` — **K = 10**, the layer-2 constant ruled at
directive D4 (`K_336`/`K_338`, the engine's own within-group borrowing convention). Every pooled cell
is disclosed with its `n` and its `w`. Isotonic is re-applied per `(pathway, cls)` after borrowing.
**No pick axis** (owner ruling: the pool is one population).

**A7. THE MEAN-PRESERVING STEP, PER PATHWAY.** With `e = entry_anchor(p)` as the entry weight
(ORDER 19's statistic, carried verbatim), over the pathway's complete-window cells:

```
U_pathway = ( SUM_all e  -  SUM_sit e * R(cell) )  /  SUM_non e
mean      = ( SUM_sit e*R + SUM_non e*U ) / SUM_all e   ==  1.0000000000  exactly
```

**This step discharges D4's renormalisation guard**: whatever the borrowed cells deliver, the
pathway's entry-weighted mean is returned to 1 exactly, by construction, in one multiplication.

**A8. BOTH READ SITES — the explicit statement the order demands.**
One derived object: the mean-preserving pair `(R, U)`.

| site | who reaches it | what replaces `R = _R_surf(cls, effpk=65, tau)` |
|---|---|---|
| `sitout_ev:1963` | `ns == 0` — **a sitter, by the derivation's own definition** | `R_pool_derived(pathway, cls, tau)` |
| `_a_blend:2177` | `ns >= 1` — **a NON-sitter, by the derivation's own definition** | `U_pathway` |

The two engine sites partition the pool population on precisely the variable the derivation splits on.
That is why one object covers both, and it is a design statement, not an accident.
`H_POOLSIT = H_UNION = 1.0`. Everything is `p.get('_pool')`-gated; **ND rows read the national surface
at both sites, untouched.**

**Declared consequence, stated up front:** `U > 1` is a **lift**, and the engine's ITEM-H comment
asserts "*NO BLANKET LIFTS EXIST ANYWHERE: every factor here is <= 1*". That invariant is a property
of ITEM H, which retires here. The owner's mean-preserving ruling requires a factor above 1 on the
non-sitters or the redistribution is a net charge. The uplift is therefore intentional and declared.

---

## §B — DEPARTURES FROM THE ND METHOD, DECLARED IN ADVANCE

| # | ND method | here | why |
|---|---|---|---|
| **D1** | outcome level era-normalised `avg * REF/era[y]` | **raw season averages** | era normalisation was RETIRED by owner ruling (`_merged_recover.py:52-57`, "*Do not reintroduce*"). Re-using it would contradict a standing ruling. |
| **D2** | denominator `V0 = v0_start(p)` | **`entry_anchor(p)`** | `entry_anchor` is literally what `R` multiplies at both pool read sites (`anch = R*entry_anchor(p)`). Deriving against a different denominator than the engine divides by would not be a retention. `v0_start` reported as a sensitivity. |
| **D3** | kernel over `(log-pick, depth)`, pick-conditioned (R2 fired) | **depth axis only** | owner ruling: the pool is ONE population, rookie pick 1 and 30 are the same; and `MA.effpk` returns the constant `POOL_PICK = 65` for every pool row, so a pick axis is not identified in the pool at all. |
| **D4** | evaluation knots at picks 5/15/30/50 | **no pick knots**; knots at depths 1..6 | consequence of D3. |
| **D5** | one surface for every draftee | **pathway layer at `n>=20`, else K=10 shrinkage to the whole-pool cell** | directive D4 (partial pooling, ruled); order requirement 3. |
| **D6** | no mean-preserving step | **U per pathway, exact to 1.0000000000** | owner's D8 amendment; the ND surface predates it. |
| **D7** | KPP retention floor `max(KPP, nonKPP)` applied on the board path (owner override O1) | **not applied to the derived pool surface** | O1 is a signed override on the NATIONAL surface, scoped to the board path. Whether it extends to a pool object derived on pool data is an owner question this seat does not pre-empt. **Reported both ways.** |

---

## §C — THE PREDICTIONS

Scored on the whole-pool surface unless a pathway is named. ORDER 18 measured pool-history depth-1
retention on its own convention as nonKPP **0.5725** / KPP **0.7528** / RUCK **0.8783**; my convention
differs on the denominator (D2), the norm population (pool-only, not all-draftee) and era (D1), so I
predict against my own construction and reconcile to ORDER 18's afterwards.

### The surface

| # | quantity | prediction |
|---|---|---|
| P1 | whole-pool derived R, nonKPP, depth 1 | **0.40 – 0.75** |
| P2 | whole-pool derived R, KPP, depth 1 | **0.40 – 0.85** |
| P3 | whole-pool derived R, RUCK, depth 1 | **0.55 – 1.00** |
| P4 | class ordering at depth 1 | **RUCK > KPP > nonKPP** (ORDER 18's pool-history ordering holds on my convention) |
| P5 | the RAW (pre-isotonic) whole-pool surface violates non-increasing-in-depth in **at least one** cell | **TRUE** |
| P6 | after the isotonic step, violations at every fitted cell (whole-pool AND pathway) | **ZERO** |
| P7 | whole-pool derived R at depth 6 | **below 0.45 for nonKPP and for KPP** |
| P8 | derived depth-1 R is **above** today's composed pool read (`0.549 x 0.804 = 0.441` nonKPP) | **TRUE for all three classes** |

### Cells and pooling

| # | quantity | prediction |
|---|---|---|
| P9 | pathway x class x depth sitter cells reaching `n >= 20` | **fewer than 25** of the 162 possible |
| P10 | pathways with **no** cell at `n >= 20` | **at least 5** of the 9 |
| P11 | RD is the only pathway with a cell at `n >= 20` at depth 4 or deeper | **TRUE** |

### The mean-preserving table

| # | quantity | prediction |
|---|---|---|
| P12 | post-redistribution entry-weighted mean, every pathway | **1.0000000000 on all nine** (by construction) |
| P13 | MSD uplift `U` (entry-weighted sit share 0.8500) | **> 2.5** |
| P14 | ALL-POOL pooled uplift `U` | **1.10 – 1.60** |
| P15 | pooled conditional mean `R` over actual sitters | **below 0.80** — the conditional markdown on sitters is LARGER than the pathway-blended average implies |

### The staged board

| # | quantity | prediction |
|---|---|---|
| P16 | ND rows moved on the staged board | **EXACTLY 0** (asserted, not reported) |
| P17 | staged board total change vs the live board `1dbd1480` | **+2,000 to +12,000**, sign POSITIVE |
| P18 | staged delta vs variant A (H lifted only, rebuilt on the adopted engine) | **staged > A** |
| P19 | staged delta vs variant B (H + R at `sitout_ev` lifted to 1.0) | **staged < B** — sitters take `R < 1`, not 1.0 |
| P20 | rows moved under the staged configuration | **> 75** — the `U` leg reaches non-sitters that neither A nor B touches |
| P21 | some pool row moves **DOWN** under the staged configuration | **TRUE** — the FULL update is a redistribution, so at least one deep sitter must lose against today's composed read |
| P22 | variant A rebuilt on the adopted engine reproduces ORDER 19's `+2,306` | **NO** — the board pin changed under the par fix; predicted within **±25%** of +2,306 |

### The instruments

| # | quantity | prediction |
|---|---|---|
| P23 | all-arm PRIMARY margin vs the 14% charge, staged | **positive, +15% to +26%** (today +25.50%) |
| P24 | legacy 1-64 (`noarb_table_338.py`) margin vs 14%, staged | **within 0.10 points of +5.16%** |
| P25 | arbitrage opened on either instrument | **NO** |
| P26 | all-arm PRIMARY yr1 ratio rises against today's 0.8850 | **TRUE**, into **0.89 – 0.97** |

---

## §D — WHAT THIS ACT DOES NOT DO

- It does not land. `H_POOLSIT`/`H_UNION` keep their shipped defaults in the checkout; the surface is
  staged in a scratchpad worktree only. The pool-update lever lands after ORDER 22's packet.
- It does not touch the national retention surface `R_SURF`, at either site, for any national row.
- It does not touch `v0`. ORDER 19 proved three ways that the sitter machinery never reaches the v0
  chain; nothing here changes which functions are called.
- It does not choose whether owner override O1 (the KPP retention floor) extends to a pool-derived
  object. Both readings are printed.
