# PRE-REGISTRATION — ORDER 7, THE ALL-ARM COHORT INSTRUMENT

**Filed BEFORE the first all-arm table was produced.** Population counts are fixed here, as the order
requires. Breaches are reported as breaches; the population is never tweaked to flatter a row.

## The owner's ruling, verbatim

> *"In previous conversations I had insisted that the no-arb sheets include not just ND 1-64 but all
> cohort players. I have made it clear that a cohort is all players drafted through mechanisms that are
> eligible to debut in the same year (for example, the most recent cohort is ND, RD, SSP in 2025 + MSD
> in 2026). So when I look at cohort progression, it's through that lens."*

## The instrument

`noarb_table_allarm.py` — a **sibling** reader. `noarb_table_338.py` is **NOT modified** (md5
`0f8220351c64c56ccfa90c60edcdfa5f` stays the canonical instrument's md5 and is re-asserted at every run).

**No new emits are needed and none are run.** The existing per-entrant matrices already carry **all
2645 rows**, every arm included — only the canonical *reader* filtered them down to ND picks 1-64. The
all-arm table is produced from the SAME matrices already emitted for main / FULL / V2 / V5 / XW / STACK,
so the two instruments are read off identical engine runs and any difference between them is the
population, never the engine.

**Cohort key** — the owner's rule, implemented literally:
`cohort(p) = draft year + 1`, except `MSD`, where `cohort(p) = draft year`.
This puts ND+RD+SSP of 2025 with MSD of 2026 in cohort **2026**, which is his worked example, and it is
the engine's own `debutyr` convention (`MSD` debuts in its entry year, every other route the year after).

**Year-0 anchor** = each entrant's own `v0`, the same field the canonical instrument uses. **This is
measured, not assumed, to be arm-appropriate**: `v0` moves for **1080 of 1201** pool rows between main
and FULL (median ratio 0.6632), so the pool arm's own year-zero repair is already inside the
denominator. Using it keeps the two instruments strictly parallel.

**Aggregation** — pooled Σprice/Σanchor over the same included set, exactly as the canonical reader:
`ratio = mean(value at cohort year N) / mean(v0)` over rows whose cohort year N has been reached.

## THE POPULATION, FIXED HERE BEFORE ANY RESULT

Excluded outright: **3** rows of 2645 (no draft year, or `v0 <= 0`) — stated, not hidden.

**PRIMARY WINDOW — cohorts 2005-2023** (the parallel of the canonical draft window 2004-2022):

| arm | n |
|---|---|
| ND | 1310 |
| RD | 621 |
| MSD | 55 |
| UNR | 49 |
| IRE | 47 |
| PDA | 43 |
| PDN | 33 |
| SSP | 31 |
| PDS | 21 |
| **TOTAL** | **2210** |

**MODERN WINDOW — cohorts 2019-2023** (the only span where *every* arm exists): **n = 540**
(ND 325, RD 66, MSD 55, SSP 31, PDN 25, UNR 13, PDA 13, IRE 12).

**ARM THINNESS, STATED WITH COUNTS RATHER THAN SILENTLY TRUNCATED.** The arms do not go back equally
far: first draft year is MSD **2019**, SSP **2018**, PDN **2016**, PDA **2009**, UNR **2007**, PDS
2007-2011 only, IRE/RD/ND **2003**. So the primary window is genuinely all-arm only from cohort 2019;
before that it is ND+RD with sporadic IRE/UNR/PDA/PDN. Both windows are therefore reported side by
side, and the per-cohort arm counts are printed in the table rather than described.

**CONSISTENCY SELF-CHECK, already computed:** the ND picks 1-64 subset of the primary window is
**exactly 1197** — the canonical population, to the row.

**DISCLOSED GAP — the MSD year-1 hole.** The emitter builds `yrs` from `draft year + 1` for every row,
but an MSD entrant debuts in his draft year. So an MSD row's **cohort year 1 is his debut season and is
not carried in the matrix**. Those 55 rows therefore enter from cohort year 2 and are EXCLUDED from
cohort year 1 rather than scored zero, because zero would be a false statement about a player who
played. The exclusion count is printed on the year-1 row.

## PREDICTIONS

**P7.1 — the canonical population reproduces inside the all-arm instrument.** Restricted to ND picks
1-64, cohorts 2005-2023, the all-arm reader must return the canonical table's ratios to 4 decimals
(FULL yr1 0.9974, yr4 1.5310). *Falsifier: any disagreement — which would mean the sibling reader's
value semantics differ from the canonical one, and nothing else on the table could be read.*

**P7.2 — all-arm FULL yr1 lands BELOW the picks-1-64 FULL yr1 of 0.9974.** The pool arm carries ITEM
H's flat 38.5% cut (ORDER 6) and it is absent from the canonical population entirely. Predicted all-arm
FULL yr1 in **0.90 – 0.99**. *Falsifier: at or above 0.9974.*

**P7.3 — the main→FULL year-1 drop is LARGER on the all-arm basis than on picks 1-64.** On main the
pool arm carries no ITEM H cut; under FULL it does. The canonical drop is −11.3%. Predicted all-arm
drop **worse than −11.3%**. *Falsifier: a smaller drop.*

**P7.4 — XW and V5 restore LESS on the all-arm basis than on picks 1-64.** Neither touches ITEM H,
which is where the pool arm's cut lives; both act on the par sample and the age discount, which are
national-draft-weighted machinery. Predicted: each row's yr1 gain over FULL is a **smaller fraction of
the main→FULL gap** on the all-arm instrument than on the canonical one.
*Falsifier: an equal or larger fraction.*

**P7.5 — the STACK stays ARB on the all-arm basis.** Its margin is measured against V5's own 12.00%.
Predicted still **negative**. *Falsifier: a positive margin — which would mean the arbitrage verdict is
an artefact of the canonical population.*

**No smoothing. No population tweak to flatter any row. Whatever it shows is what is reported.**
