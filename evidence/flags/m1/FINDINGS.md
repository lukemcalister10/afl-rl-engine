# FLAG (a) — M1 BREAKOUT-CREDITING — FINDINGS

**State:** `[BAKED c47cb43d]` · main `389ac39` · READ-ONLY on engine/data
**Script:** `m1_breakout_credit.py` → `m1_breakout_credit.txt`, `m1_hits.json`
**Engine constants (verbatim):** `PROVEN_N=4  TOL_M1=5.0  S_M1=0.46  G_ADQ=12  WIN=2`

## What the M1 flag does

The engine `_coreM1` up-branch fires for a **proven** player (`n=_nqual>=4`) when:

```
Lc >= Lo   AND   (Lc - Lo) >= TOL_M1(5.0)   AND   _radq
```

`Lo` = `_lvl_eff_orig` (career, recency-weighted level); `Lc` = `_lvlcurr`
(steeper-recency current level); `_radq` = a season within `WIN=2` yrs with
`>=G_ADQ(12)` games and avg above `Lo`. When it fires the credited level is:

```
credited level = Lo + 0.46*(Lc - Lo)          # only 46% of the gap is banked
```

So of every point of recent-over-career gap, **0.46 is credited and 0.54 is
withheld**. That 0.54 is the flag's cost.

## Headline numbers  `[BAKED c47cb43d]`

| Metric | Value |
|---|---|
| M1 up-branch **hits** (Y=2026, real store) | **46** |
| — SUSTAINED (rise held ≥2 consecutive adequate seasons > career) | **34** |
| — SPIKE (only most-recent adequate season > career) | 12 |
| Total **withheld level** (Σ 0.54·gap) | 214.7 pts |
| Total **$ to restore full credit** (Σ ev@1.0 − ev@0.46) | **$15,484** |
| **SUSTAINED-and-under-credited** | **34 players, $10,604** |

The sustained cohort — the players whose rise is *not* a one-year noise spike —
carries **$10,604** of the $15,484 total withheld. That is the concrete
BEFORE-number: the overhaul that lifts breakout crediting is worth on the order
of **~$10.6k** to genuinely-improving proven players, before any spike is
re-credited.

## Explicit consecutive-year (spike vs sustained) test

On adequate (`>=12`-game) real career seasons, sorted by year:
- `nyr_above` = count of **consecutive most-recent** adequate seasons with `avg > Lo`.
- `asc_run` = length of the terminal strictly-increasing run of adequate avgs.
- **SUSTAINED** iff `nyr_above >= 2` (the rise clears career level for ≥2 straight
  years — not a single up-tick). Otherwise **SPIKE**.

Both counters are printed per player so the call is auditable, not asserted.

## Sum-to-total guard — PASS

Per player `credited + withheld == gap` to machine precision: **46 checked, 0
mismatches → PASS**. The dollar leg also reconciles per player:
`(base−zero) + (full−base) == (full−zero)`.

## Pickett exemplar — name-collision guard is load-bearing

The store holds **four Picketts**; two share pick 12 *and* position GEN_FWD —
only cohort disambiguates:

| ID (key) | pick | cohort | pos | age |
|---|---|---|---|---|
| jarrod-pickett | 5 | 2015 | MID | 30 |
| marlion-pickett | 11 | 2019 | GEN_FWD | 35 |
| **kysaiah-pickett** | **12** | **2020** | GEN_FWD | 25 |
| latrelle-pickett | 12 | 2026 | GEN_FWD | 21 |

Surname alone (or even surname+pick+position) would confuse Kysaiah with
Latrelle. Identity is keyed **ID·pick·cohort** throughout.

### kysaiah-pickett · pick 12 · cohort 2020 · GEN_FWD · age 25 — SUSTAINED (nyr 2 / asc 5)

Adequate season path: 2022 **63.0** → 2023 **69.2** → 2024 **73.4** →
2025 **91.5** → 2026 **100.6** (the task's "73→91.5→100.6" is the tail of a
5-season ascending run).

**Level decomposition** `[BAKED c47cb43d]`:
```
Lo (career)                 = 80.87
Lc (steep-recency current)  = 93.28
gap                         = 12.40
credited = 0.46*gap         =  5.71   -> M1 level 86.58
withheld = 0.54*gap         =  6.70
GUARD credited+withheld     = 12.40 == gap  -> PASS
```

**Dollar decomposition** (actual re-priced `ev`; nonlinear via band/asc/floor):
```
ev @ S_M1=0.00 (=Lo)        = $2849
ev @ S_M1=0.46 (BAKED)      = $3007
ev @ S_M1=1.00 (=Lc)        = $3718
M1 currently adds over Lo   = $158    (base - zero)
WITHHELD from full credit   = $711    (full - base)
GUARD add+withheld $869 == (full-zero) $869 -> PASS
```

Kysaiah alone carries **$711** of withheld value on a demonstrably sustained
(5-year ascending) breakout while M1 banks only **$158** of it.

## Method notes / deliberate scope

- Dollar figures are **actual re-priced `ev`** at `S_M1 ∈ {0.0, 0.46, 1.0}`
  (cache cleared each pass), not a level-scaled proxy — so they carry the true
  band/asc-tail/floor nonlinearity. The *level* decomposition is exact/linear;
  the *dollar* decomposition is reported as measured.
- `S_M1=1.0` (full credit → price at `Lc`) is an **upper bound** on the
  under-credit, not a proposed dial. It answers "how much is withheld", which is
  the BEFORE-number the overhaul needs.
- A few hits are floored/near-scrap (e.g. jaxon-prior, toby-bedford) so their $
  deltas are small despite real level gaps — visible in the table, not hidden.
