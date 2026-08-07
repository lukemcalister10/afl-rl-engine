# Stage 3 step 2 — THE NUMERAIRE, resolved

Stage 2 left the numéraire openly broken: `new(p) = old(p) × f(p)` with no renormalisation put
`curve["1"]` at **3364**, and the engine halted at import.

## What the engine actually asserts, read out of the code

Three separate sites, all unconditional:

| site | assertion |
|---|---|
| `rl_model.py:1206` `_split_ladder` | `assert nd[1] == 3000` — fires at **import**, on every ladder the engine builds |
| `rl_export.py` (g) NUMÉRAIRE ASSERT | `PVC[1] != 3000` → `SystemExit`, "a shipped board with pick-1 ≠ 3000 HALTS, always" |
| `rl_model.py` `_load_numeraire` (E6) | `published_pin / pooled_head_pre_scale == s` to 1e-9 **and** `published_pin == RL_PICK1` |

Proven non-vacuous at this stage: the stage-2 ladder halted at
`AssertionError: RL_PVC2 v2 curve numeraire: curve(1)=3364 != 3000`.

And the two consumption paths the ladder feeds:

* **pick side / year-zero** — `_PVC0` is loaded verbatim from this artifact's `curve`. It feeds
  `draftval` (the RUCK prior-cap and V0-scaffold basis) and, through `_PVC2M`, `unpl_eq` and the
  pedigree pedestal — i.e. the **year-zero and young-player** values, and then the frozen year-zero
  surface fitted over them.
* **player side** — `BOARD_FACTOR = (RL_PICK1 / PVC_v34[1]) * _NUM['s']`, and `SCALE = SCALE ×
  BOARD_FACTOR`, so the artifact's `numeraire.s` scales `val()` and therefore every production-driven
  (established) engine value. `PVC_v34[1]` is the v3.4 **import-fit** head, not this ladder's head, so
  the two sides are anchored on different curves and `s` is the only shared term.

## The choice, and why it is FORCED rather than chosen

Write the taught curve as `T(p) = base_erafree(p) × f(p)` with `T(1) = 3000 × f(1)`.

* **(i)** forces the published ladder to pin at 3000.
* **(ii)** forces the published ladder to be `T` times a single scalar.

Those two together determine the ladder **uniquely**:

```
curve(p) = round( base_erafree(p) × f(p) / g ),      g = f(1) = 1.121405224905
```

so the only remaining free parameter in the whole problem is `s`. And `s` is what decides whether
**(iii)** holds, because the ratio the re-anchor exists to move is

```
R(p) = mean(year 4) / mean(year 0)  ~  (production, ∝ SCALE ∝ s) / (year-zero, ∝ ladder)
```

With the ladder fixed at `base × f / g` and `s` held put, the year-zero side would fall by `f(p)/g ≤ 1`
against an unmoved production side and `R` would rise — the re-anchor would run **backwards**. The
only value of `s` that delivers (iii) is `s / g`, which gives

```
R_new / R_old = (s_new/s_old) / (ladder_new/ladder_old) = (1/g) / (f(p)/g) = 1 / f(p)
```

— exactly the re-anchor, with `g` cancelling. **So (i)+(ii)+(iii) admit exactly one numéraire, and it
is the one the exporter's own halt text prescribes:** *"re-base the CURRENCY to the anchor (L7 ÷ the
scale drift), never the anchor to the drift."* Applying the same `g` to both sides is the E6 two-sided
law already implemented in `_load_numeraire` — *"one measured head, one factor, both sides."*

## The arithmetic

| field | before | after |
|---|---|---|
| `published_pin` | 3000.0 | **3000.0 — UNMOVED** |
| `pooled_head_pre_scale` | 3017.9232 | 3017.9232 × g = **3384.3148448406** |
| `s` | 0.9940610814748366 | 0.9940610814748366 / g = **0.8864423487588727** |

E6 coherence `published_pin / pooled_head_pre_scale − s` = **0.000e+00** (exact, by construction).
`s_new / s_old = 0.891738309927 = 1/g` to twelve places.

**ENGINE CHANGE: NO.** Not one line of `_merged_recover.py` or `rl_model.py` was touched. `engine_head`
and `rl_model` pins are unmoved. The whole numéraire resolution is data in the artifact the engine
already reads by design.

## (iv) — reported straight, because it does not hold literally

The brief asked for a numéraire under which *"established players' engine values [are] untouched by the
numeraire choice."* **It does not hold, and it cannot**, for the reason set out above: once (i), (ii)
and (iii) are required, `s` is forced to `s/g` and `SCALE` moves with it. Measured on the built board,
every player is cut by the uniform factor `1/g`:

```
Harry Sheezel  11963 -> 10668  -10.83%
Nick Daicos    10820 ->  9649  -10.82%
Zak Butters     7085 ->  6317  -10.84%
```

707 of 708 movers are cuts, and the per-player factor is `1/g = 0.891738` throughout. What IS preserved,
exactly:

* **every player-to-player relativity** — the cut is one uniform scalar, so no player is repriced
  against another by the numéraire choice;
* **the anchor** — pick 1 displays 3000, unmoved;
* **the intended pick-vs-player move** — the ladder falls by `f(p)/g` while players fall by `1/g`, so
  picks get dearer relative to players by exactly `f(p)`. That is the re-anchor itself, not a numéraire
  artifact.

The alternative — hold `s` and publish the tilted ladder — leaves established players' integers alone
and destroys the stage's entire purpose, driving the measured year-ratio away from 1.40 instead of
toward it. That trade was not takeable, so (iv) is reported as **not satisfiable alongside (i)–(iii)**
rather than quietly re-interpreted. The board-wide 10.83% re-denomination is the disclosed cost.

The `#328` reversal condition ("any future pass moving any pick by more than 1 board point re-opens
it") is **tripped by construction**. Adoption re-opens and remains the owner's separate click.
