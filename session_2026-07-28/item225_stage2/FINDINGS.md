# ITEM 225 STAGE 2 — the ND 1–64 curve and the pool's level, derived from scratch

**Seat:** execution supervisor, cold, #225. Not the #217 seat.
**Store:** `e3aaba77` — the store as it stands, not `c120cfd5`. Named beside every figure below.
**Surface:** the **frozen** v0surf, signature `76498b5a`, `frozen=True`. Every figure in §1–§5 is
measured on it. §6 is the scratch-board run and names its own surfaces.
**Base:** `main` at `7cfde99`, taken in first, `git fetch --unshallow` done (1,262 commits, no
`.git/shallow`).
**Nothing here is adopted.** These are candidate values with their basis. Adoption is the owner's
and is a separate release with its own word.

---

## 0 · Does the requirement at the top of the directive hold? Limb by limb.

> *"It is essential to me that this new number we are deriving is ENTIRELY from scratch… ND pick 64
> can only be valued based on outcomes of players that were DRAFTED IN THE ND, and the outcomes are
> based on the NEW information we have."*

| limb | verdict | evidence |
|---|---|---|
| **No pool row teaches the national curve** | **met** | Direction 1 is the instrument inherited from `main` (Addendum 2 §2), not rebuilt. Re-run: all five sites clean — `build_pvc`, `build_pvc_v34`, `_natcv`, `_natcv34` and `v0_kernel`, the last on exactly **1,448** rows, the ND 1–64 count reached independently here. Direction 2 and the pooling term are §4. |
| **Positions as newly assigned** | **met** | `pos` is `MA.gfut(p)` read from the current store at emit time. Not a stored copy, not the assignments the old curve was fitted under. |
| **The current store** | **met** | `e3aaba77`, asserted by Guard 5 at bootstrap and stamped into every artifact this job wrote. |
| **Fitted, not adjusted** | **met** | The fit reads `per_entrant_split.json`, regenerated on `e3aaba77`. `pvc_curve_v2.json` is never opened by the derivation. It is opened once, in `scratch_board.py`, only to copy the artifact's *envelope* into a scratch file. |
| **Method held constant** | **met** | `pava_ni`, `build_points`, `fit_year0`, `monotone_strict` carried over from `derive_pvc2.py` function for function. `tau=0.12`, `nmin=35`, `PW_FLOOR=0.11`, `hmin/hmax=0.10/0.60`, `pin(1)=3000`, window 2004–2024 — all unchanged. The `×0.6` ceiling and `min(n_pos/200,1)` kept. The isotonic step kept. |

**The one domain change, and it is the ruling rather than a method choice:** the fit grid stops at
64 instead of 99. There is no price for pick 70.

---

## 1 · The curve: before and after the exclusion

All three curves on domain 1–64. `curve[1]` is the numéraire pin and is 3000 **by construction** in
all three — it cannot move, and reporting it as "unmoved" would be reporting the pin, not a result.

| pick | shipped | before exclusion | **AFTER (derived)** | vs shipped | vs before |
|---|---|---|---|---|---|
| 1 | 3000 | 3000 | **3000** | +0 | +0 |
| 10 | 1604 | 1566 | **1566** | −38 | +0 |
| 32 | 785 | 778 | **778** | −7 | +0 |
| 55 | 562 | 584 | **586** | +24 | +2 |
| 56 | 557 | 582 | **582** | +25 | +0 |
| 57 | 553 | 581 | **580** | +27 | −1 |
| 58 | 549 | 580 | **577** | +28 | −3 |
| 59 | 545 | 579 | **575** | +30 | −4 |
| 60 | 542 | 578 | **573** | +31 | −5 |
| 61 | 539 | 577 | **572** | +33 | −5 |
| 62 | 536 | 576 | **571** | +35 | −5 |
| 63 | 533 | 575 | **570** | +37 | −5 |
| 64 | 530 | 574 | **569** | +39 | −5 |

Ladder total 1–64: shipped 64,617 → derived 64,913 (**+0.46%**). Strict descent holds across all 63
steps, no plateaus.

**The last four picks move. The exclusion took.** But the integer ladder understates it, because the
strict-descent epsilon floors four of those steps at −1. On the **raw fit, before the monotone
step**, the effect is larger and it ramps monotonically into the boundary:

| pick | raw before | raw after | delta | eff-n before | eff-n after |
|---|---|---|---|---|---|
| 50 | 604.7 | 606.8 | +2.2 | 285.6 | 261.2 |
| 55 | 583.9 | 585.6 | +1.7 | 453.2 | 264.6 |
| 58 | 579.8 | 577.1 | −2.7 | 641.9 | 244.2 |
| 61 | 579.2 | 572.2 | −7.0 | 826.2 | 204.2 |
| 64 | 579.5 | 569.8 | **−9.7 (−1.7%)** | **904.0** | **152.1** |

**At pick 64 the exclusion removes 83% of the effective sample** (904.0 → 152.1). Picks 1–45 are
byte-identical before and after — correct, and worth stating: all 761 contaminating rows sit at
**exactly pick 65** (the pool is collapsed to one index), so the Gaussian kernel over log-pick
reaches them only near the boundary.

**Why the value moves so little for so much sample:** the pool rows' `v0` sits close to the local
curve there, so removing 750 of 900 effective observations shifts the mean by under 2%. Large in
count, small in value. That is a finding, not a reassurance — the same contamination on a population
whose values differed would have moved the tail hard.

### The ND fit's rows, and what was excluded

| | rows |
|---|---|
| ND fit population (national draftees, picks 1–64, 2004–2024, with `v0`) | **1,326** |
| pre-split "in-curve" population, same store and window | 2,087 |
| **excluded, and the reason** | **761 — every one is a pool row under the ruling** |

Of the 761: rookie draft and ND 65+ only, because the pre-split "in-curve" set was `{ND, RD}` and
never admitted the pickless mechanisms in the first place. Whole-store census on `e3aaba77`: ND
1,569 (**1,448** at picks 1–64, 121 at 65+), RD 693, MSD 106, UNR 59, IRE 57, SSP 52, PDA 51,
PDN 43, PDS 21.

---

## 2 · The pool's level, one value per position

**Population: the ruled pool — 1,094 rows** in the 2004–2024 window (ND 65+, all rookie draft,
pre-season draft, every pickless mechanism). #217's pool population was 763 and admitted only ND 65+
and RD; it **dropped 331** of these. Both figures reproduced here exactly.

**Basis: realised outcomes, never-established entered as 0.0.** Two measures, both reported because
they answer different questions and must not be conflated:

- **SCAR** — the evidence-weighted mean of the walk-forward as-of values (`vpath`), i.e. the
  *evidence end* of the same R1 construction the curve uses, in curve currency.
- **production** — best-3 season average over seasons of ≥6 games, the bust-priors' own target, in
  score units.

A player who never established a ≥6-game season enters both at **0.0**. That zero is the
survivorship fix.

| pos | n | never-established | **level (SCAR)** | production | mean `v0` — **not the level** |
|---|---|---|---|---|---|
| MID | 253 | 148 (58%) | **332.6** | 29.27 | 489.17 |
| GEN_FWD | 227 | 125 (55%) | **212.1** | 26.55 | 376.20 |
| KEY_FWD | 118 | 72 (61%) | **266.9** | 23.77 | 590.01 |
| GEN_DEF | 249 | 135 (54%) | **296.2** | 31.52 | 577.62 |
| KEY_DEF | 116 | 54 (47%) | **324.5** | 32.96 | 662.80 |
| RUC | 131 | 90 (69%) | **308.6** | 24.38 | 644.26 |
| **whole pool** | **1,094** | **624 (57%)** | **288.5** | **28.43** | 533.72 |

Tracked separately, as ruled: **SSP** n=43, 19 never established, SCAR 321.2 · **MSD** n=72, 36 never
established, SCAR 321.0.

### The inversion, restated on this store and the frozen surface

| | mean `v0` |
|---|---|
| whole ruled pool (n=1,094) | 533.72 |
| played (n=470) | 515.78 |
| **never played (n=624)** | **547.23** |

**The inversion holds and still binds.** On #217's narrower 763-row population the frozen-surface
figures reproduce to rounding: mean `v0` **580.03** against their 580.04; on their ≥1-senior-game
definition, played 552.43 (theirs 553.12) and never-played 618.65 (theirs 618.31). No pedigree mean
may set the level.

On the outcome measure there is no inversion: played **671.4**, never-played **0.0** by construction.

### The comparison that is lawful, and the one that is not

The pool level is a **realised-outcome average**. The ND curve is an **entry-anchor ladder** — its
year-0 slice is dominated by `v0`. Putting 288.5 beside 569 compares two different footings, which
is the category error the seam committed with 575.9 against 544. So here is the national curve on
the **identical instrument**, no bridge and no pick-equivalent:

| population | n | never-est. | realised SCAR | production |
|---|---|---|---|---|
| ND 1–10 | 209 | 6 | 2314.8 | 79.78 |
| ND 11–20 | 208 | 13 | 1345.1 | 67.99 |
| ND 21–40 | 420 | 104 | 819.6 | 51.84 |
| ND 41–54 | 294 | 105 | 511.2 | 42.07 |
| ND 55–64 | 195 | 88 | 350.4 | 34.26 |
| **the pool** | **1,094** | **624** | **288.5** | **28.43** |

**On one footing the pool sits below the last national band, where it should.** The pedigree measure
put it at 580.0 — *above* `curve[64]`=530, which the engine's own G-Y0 note flags as something no
pool entry level can coherently do. The outcome measure removes that incoherence without anyone
tuning anything.

---

## 3 · The priors, each fit pooling within its own population

Recipe unchanged (register v509): target = best-3 season average over ≥6-game seasons with
never-established at 0.0; estimator = `IsotonicRegression(increasing=False, out_of_bounds='clip')`
of that target on `effpk`, fitted twice — once pooled across positions, once per position — blended
`w·posfit + (1−w)·pool`, `w = min(n_pos/200, 1.0) × 0.6`. Debut cohorts 2006–2020.

**Per the owner's ruling of 2026-07-28, the pooled-across-positions fit is computed inside each
population.** The ND prior's pooled term sees only ND 1–64 rows; the pool prior's sees only pool rows.

**A consequence of the separation that the owner should see, because it changes what the low-sample
handling does:** splitting the population roughly halves each position's sample, so the `n/200` ramp
now binds where it previously did not.

| pos | ND n | w | ceiling binds? | pooled share (1−w) |
|---|---|---|---|---|
| MID | 284 | 0.600 | yes | 40% |
| GEN_FWD | 196 | 0.588 | no (n<200) | 41% |
| KEY_FWD | 108 | 0.324 | no (n<200) | **68%** |
| GEN_DEF | 208 | 0.600 | yes | 40% |
| KEY_DEF | 108 | 0.324 | no (n<200) | **68%** |
| RUC | 47 | 0.141 | no (n<200) | **86%** |

The directive records the `×0.6` ceiling binding for **five of six** positions pre-split (MID at 579
samples receiving what KEY_FWD received at 208). Under the separation it binds for **two of six** —
but the priors are *more* pooled overall, not less, because the ramp took over. In the pool fit no
position reaches n=200 at all, so the ceiling never binds there and pooled shares run 42–74%.

**Both known defects are REPORTED, not repaired** (Addendum 1 §A):

1. **The `×0.6` ceiling** — kept. Measured effect above.
2. **`increasing=False` on raw pick** — **this construction inherits it.** The pooled-across-positions
   prior resolves to **18 distinct levels over 64 picks**, plateau widths
   `[2,2,1,5,3,6,2,1,3,6,3,3,7,2,8,5,2,3]`, widest 8 picks. The step edges are wherever the sample
   happened to break. In the *curve* the effect is milder: the raw fit is strictly descending
   everywhere (no PAVA-induced plateau), but four steps — picks 60–63 — land on the strict-descent
   epsilon floor, so their ordering is supplied by the monotone step rather than by data.

---

## 4 · The check that decides whether this job succeeded

Direction 1 — *no pool row teaches the national curve* — is **inherited from `main`, not rebuilt**
(Addendum 2 §2). Re-run: all five sites clean.

**Direction 2 is this seat's, and it watches the pooling term as well as the sample.**

Each fit registers what it actually consumed, in two kinds:

- `sample` — the rows the fit consumed directly. A sampled-rows check sees this.
- `pooling` — the population the pooled-across-positions aggregate was computed over. **A
  sampled-rows check is blind to this.**

The second kind is the whole point. The priors blend `w·posfit + (1−w)·pool` with `w ≤ 0.6, so **at
least 40% of every prior is the pooled term**. Cross that term and every sampled row stays clean
while the other population is inside the fit. That is the same shape as the defect #217 shipped once
— a check watching its own copy of the rule rather than what the fit consumed — so this check reads
the recorded populations and never re-derives them.

**Non-vacuity, all 8 site × kind combinations, each crossed one at a time:**

| site | kind | failed? | failed **by name**? |
|---|---|---|---|
| nd_curve | sample | yes | yes |
| nd_curve | pooling | yes | yes |
| priors_ND_1_64 | sample | yes | yes |
| priors_ND_1_64 | pooling | yes | yes |
| pool_level | sample | yes | yes |
| pool_level | pooling | yes | yes |
| priors_POOL | sample | yes | yes |
| priors_POOL | pooling | yes | yes |

**The decisive case, and it is the one the owner asked for.** With `priors_ND_1_64`'s *pooling* term
crossed and its sample left alone:

```
PASS  site 'priors_ND_1_64' [sample] : no POOL row among the 951 keys it consumed
FAIL  site 'priors_ND_1_64' [pooling]: no POOL row among the 1769 keys it consumed
                                       <-- 818 found, e.g. ['aaron-bruce','aaron-hall',…]
```

Every sampled row clean; 818 pool rows teaching the ND prior through the ≥40% pooled term alone.
**A sampled-rows check reads green on that.** Same asymmetry proven in the other direction for
`pool_level` and `priors_POOL`.

Evidence: `out/check_nonvacuity.log`.

### Magnitude of that contamination, measured

Because the magnitude matters as much as the mechanism, and honesty here cuts against the finding:

With identical sampled rows (951 ND) and only the pooled term crossed, the blended ND prior moves at
**picks 62–64 only**, by at most **+0.52** prior points. It is zero everywhere from pick 1 to 61.
The pooled-across-positions fit itself moves only at pick 64 (28.72 → 29.33).

**Why so small, and why the check still matters.** All 818 pool rows sit at pick 65, outside the
1–64 grid, so the isotonic pooled fit only feels them at the boundary. The damage scales with
`(1−w)` — worst for the thinnest position, RUC at +0.518 against MID at +0.241, i.e. it lands
hardest on exactly the positions the low-sample handling exists to protect. **The confinement is a
property of today's data, not of the construction:** SSP and MSD are ruled to become their own pools
later, and the moment the pool carries more than one index the pooled term spreads across the grid
and the confinement is gone. The check is cheap and it is the only thing standing between that
change and a silently contaminated prior.

---

## 5 · A structural finding the owner needs before adoption

The directive asks for **one value per position** in the pool, applied by the position layer
`iso_corr`. The artifact and the engine currently carry **one position-blind scalar** —
`_V2CURVE[POOL_PICK] = int(_V2J['pool_value'])`, and `_split_ladder` documents it as "ONE entry at
POOL_PICK carrying the pool's single position-blind level".

So the per-position differentiation has to come entirely from `iso_corr`. It cannot:

| pos | `iso_corr(pos,65)` | 288.5 × iso_corr | derived realised level | ratio |
|---|---|---|---|---|
| MID | 0.9591 | 276.7 | 332.6 | **1.20** |
| GEN_FWD | 0.9539 | 275.2 | 212.1 | **0.77** |
| KEY_FWD | 0.9488 | 273.7 | 266.9 | 0.98 |
| GEN_DEF | 0.9858 | 284.4 | 296.2 | 1.04 |
| KEY_DEF | 0.9709 | 280.1 | 324.5 | **1.16** |
| RUC | 0.9593 | 276.7 | 308.6 | 1.12 |

`iso_corr` spans **3.9%** across positions at the pool index; the realised evidence spans **57%**.
A scalar `pool_value` times the existing position layer would overprice GEN_FWD by ~30% and
underprice MID by ~20%.

**This is reported, not resolved.** Whether the pool carries per-position levels, and how, is a
structural decision — ITEM 412 and the owner's, explicitly outside this job's fence.

---

## 6 · The scratch board, and the halt

**Nothing adopted, baked, re-pinned to `main`, or released.** The derived curve went into a *copy*
of the workspace and the regenerated surface into a scratch pickle addressed by `RL_V0SURF_PKL`. The
checkout's engine, `data/v0surf.pkl`, `data/expected_boot.json` and the UI bundles were never
written. Evidence: `out/scratch_board.json`.

### The halt fired, and it is the design

Exactly as Addendum 2 §1 said it would. Changing the curve moved the config signature, and the
engine stopped rather than quietly refitting:

```
v0surf FROZEN-SIGNATURE HALT: this build's config signature ef4ba845… is NOT in data/v0surf.pkl
  (frozen: 1cbaf33d…, 76498b5a…).
The engine will NOT silently re-fit the V0 pick-curve surface — that silent fallback was removed…
If the config CHANGED deliberately (a split, an exclusion, a curve move), regenerate and re-pin: …
```

**No fallback restored, no accepted-signature set widened, nothing routed around.** Regeneration was
done under the one declared entry point, `RL_V0SURF_REFIT=1`.

### Which surface every figure sits on

| | signature | frozen? |
|---|---|---|
| baseline board | `76498b5a` | **yes** |
| scratch board | `ef4ba845` | **no — refit** |

The scratch figures below ride a **refit** surface, because freezing one requires `--bake`, which
writes `data/v0surf.pkl` and re-pins `data/expected_boot.json`. Addendum 2 §5 would permit that
locally; I took the more conservative route of a scratch pickle instead, and the cost is that these
figures are not frozen-reproducible. Stated rather than glossed.

### Cleanliness evidence, and what could not be evaluated

`refit_v0surf.py:17` states the precondition verbatim: *"run ONLY on a CLEAN instance — one whose
balanced board == 06d8af60 byte-exact."* **`06d8af60` is pre-split and unreachable, so the literal
precondition could not be evaluated.** I did not manufacture a substitute and do not claim it
satisfied. What I do have:

- **Intra-box determinism: IDENTICAL** across repeated refits — same signature, byte-identical ev-map.
- The baseline arm loaded the **frozen** pinned surface and reproduced `curve[1]`=3000 / `curve[64]`=530.

### The board effect

| | |
|---|---|
| players compared | 2,651 |
| movers (\|Δ\| > 1e-6) | **114 (4.3%)** |
| mean Δ | −27.69 |
| median Δ | −7.00 |
| range | +4.00 … −281.00 |

**Composition: 107 of the 114 movers are pool rows; 7 are ND 1–64, and those move by +4 to −1** —
rounding-scale, which is what a ±5 curve change at the tail should produce. **The substantive board
movement is entirely the pool level**, 528 → 288, and it is a repricing downward of pool entrants:
`caleb-may`, `max-mapley`, `patrick-carr` 617 → 336 (−281); `aiden-riddle`, `joe-pike` 473 → 258.

That is the expected shape. The 528 placeholder was the pre-split artifact's value at index 65, and
the register records it handing deep pool entrants a ~14% uplift before any age adjustment. The
derived level removes that. **Whether it is the right level is the owner's call, not this job's.**

---

## 7 · What was chosen rather than derived

Stated plainly, because the directive asks for it and because these are the places a reader should
push back.

1. **The pool level's SCAR measure is the *evidence end* of the R1 construction — the ND curve uses
   both ends.** Dropping the entry end is **directed** by Addendum 1 §C (V0 is not the instrument for
   the pool's level), not chosen. But *which* realised statistic carries the level was not specified,
   and there is no old method to replicate for a quantity that did not previously exist. I report
   both the SCAR and the production measure so the choice is visible rather than buried.
2. **The pool's window is 2004–2024**, matching the curve's, and the priors' is 2006–2020, matching
   the priors'. Each fit keeps its own construction's window. Nothing in the directive settles this
   and I did not want one number sitting on two windows.
3. **`pool_value` for the scratch board is the position-blind 288.5**, because the artifact cannot
   carry per-position levels (§5). That is a measurement convenience for the board run, not a
   recommendation of a scalar.
4. **`realised_scar` carries no time-kernel.** `exp(−t/τ)` exists in the curve fit to centre the 2-D
   surface on the year-0 slice; the pool has no year-0 slice and no ordering, so every evidence year
   carries its own evidence share and nothing else.

## 8 · Environment and process notes

- **The `bootstrap_env.sh` fault is live and cost this seat time before Addendum 2 §4 resolved it:**
  bare `python3` is **3.11.15**, the lock pins **cp312**, system pip is PEP 668-blocked. The
  Addendum 2 route works — `python3.12 -m venv`, `--require-hashes --only-binary=:all:`, then
  `RL_VENV=… bash bootstrap.sh`. `bootstrap.sh` not patched, pin not weakened. **#231 is repairing
  this; flagged, not resolved here.**
- **A stale remediation message, reported not fixed.** The `v0surf FROZEN-LOAD HALT` says *"Re-run
  bootstrap.sh to seed the workspace copy"*. `bootstrap.sh` does not copy `v0surf.pkl` anywhere —
  the load resolves it through `RL_REPO`/`CLAUDE_PROJECT_DIR`. A seat following the halt's own advice
  gets the same halt again. One-line fix, not taken here (not this job's, and it cannot stop the
  project working).
- **Coordination:** this job touched neither `data/expected_boot.json` nor `bootstrap_env.sh`. No
  conflict with #231.
- **Selftest state on `main`:** 5 pre-existing failures, none caused by this job — 4 are missing
  build artifacts (`rl_app_data.json`, `s4_matrix.json`, and the two board/book files that depend on
  them, none of which this job generates), and one is a Kako 2026 games/score expectation. Working
  tree carried no engine or data edits at any point.
