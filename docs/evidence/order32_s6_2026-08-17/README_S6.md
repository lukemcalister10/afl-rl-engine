# ORDER 32 — SEAT S6 — the six-level scenario fan, and the owner's lottery dial

**Read-only seat.** Nothing in `engine/`, no law constant, no no-arb instrument and no board was
modified. `WQ6` stays sealed at `[0.18 ×5, 0.10]` normalised inside the engine. The λ dial on the page
is a **display-layer lens over an emit** — it renormalises weights in JavaScript and never re-enters the
pricing path.

---

## 1. What was emitted

The engine's production leg does not price a player at one projected level. `b6(p)` builds **six** of
them — five conditional-prior band quantile levels plus the frozen q97 ceiling as `b6[5]` — and

```
price6(p, bb) = SCALE_DIST × dot(WQ6, [v_at_peak(p, L, 'bal') for L in bb])
WQ6 = [0.18 ×5, 0.10], normalised                       engine/rl_after/_merged_recover.py :96, :374-391
```

The board prints only the average. This seat opens it. For **all 804 active rows** under the CANDIDATE
build, `s6_emit_fan.py` writes:

| field | what it is |
|---|---|
| `b6[6]` | the six band levels themselves (five conditional-prior quantiles + the frozen q97 ceiling) |
| `six_raw[6]` | the six per-scenario career values — literally `SCALE_DIST × v_at_peak(p, b6[i], 'bal')`, engine currency |
| `six_phat[6]` | the same fan expressed in P̂ units (see §3), so `dot(WQ6, six_phat) == P̂` |
| `price6`, `Phat`, `m_downstream`, `anchor_pts` | the reconciliation constants |
| `rho, v0, D, Phi, beta, pi, pedigree_pts, production_pts` | the law's own legs, carried from the committed movers ledger |
| `spread_ratio_6_1`, `spread_span_over_med`, `top_scenario_share_of_Phat`, `top_scenario_share_of_price`, `weighted_cv` | the spread metrics |
| `fan_carries_price`, `fan_flat`, `fan_nondecreasing`, `q97_below_band5` | fan-shape flags |

**Build identity, asserted before a number is emitted.** Candidate board
`fe6be9d6ac76ebc34d26ebc11d796505` (ORDER 31-F ladder tag `f2on`, total 666,913), engine
`rl_model.py 14000af2`, store `rl_model_data.json cb38ef11`, `pvc_curve_v2.json 78ad9842`, `RL_O31=1`,
`BASE_REF 2026`, `_PL_F 1.0524`. All three artefacts are byte-identical at this commit's HEAD, which is
why the engine can be loaded straight from the repo under the dial and read the candidate's own
arithmetic — the same route `docs/evidence/candidate_31f/o31f_ledger.py` takes. The prebuilt candidate
tree at `…/scratchpad/o31f/bb_f2on/` was reused after its md5 was checked against `fe6be9d6`.
Deterministic, five-var thread-pinned, `PYTHONHASHSEED=0`, strictly sequential — one engine process,
nothing concurrent.

---

## 2. Validation

| check | max deviation | over |
|---|---|---|
| `dot(WQ6, six_raw)` vs the engine's own `price6()` return | **0.000e+00 — exact** | 804 / 804 |
| **`dot(WQ6, six_phat)` vs the build's P̂ leg** | **1.819e-12 absolute · 4.043e-16 relative** | 708 rows with a production leg |
| `price(λ=0)` vs the printed board price | **0.000e+00 — exact** | 804 / 804 |
| `rho·P̂ + pedigree_pts` vs the printed board price | 4.547e-13 | 708 |

**The P̂ number asked for is 1.819e-12 absolute / 4.043e-16 relative — i.e. exact to float epsilon, ~2
ulp.** The epsilon is IEEE-754 rounding in the renormalising multiply, nothing else. The stronger of the
two statements is the first row: the six raw terms reproduce `price6()` **bit-exactly** on every row,
because the emitter re-uses the engine's own order-fixed `_det_dot` and reconstructs `price6`'s exact
context (the `REPL_DROP` shift, the `AGE_REF`/`BASE_REF` form-anchor pin, the `_pe_clear`).

The page re-asserts the λ=0 identity **in JavaScript on load** and prints the result in the header badge;
if it ever failed the badge would go red rather than the page quietly lying. The page was additionally
verified headlessly (DOM shim, node): λ=0 total reproduces 666,913 and **0 of 804 rows move rank**; every
one of the 20 column headers sorts; reset returns exactly to the board; the dial's direction invariant
holds on all rows.

---

## 3. The page's math

`docs/evidence/order32_s6_2026-08-17/S6_LOTTERY_DIAL.html` — one self-contained file, no external assets.

Per row the page carries six **scenario prices**

```
sp[i] = anchor_pts + rho × six_phat[i]                                          i = 0..5
anchor_pts = printed_price − rho × dot(WQ6, six_phat)
```

`sp[i]` reads as *"what this player is worth on the board if scenario i is the one that lands"*. Because
the weights sum to 1,

```
dot(WQ6, sp) == the printed board price      EXACTLY, on all 804 rows
```

— **the printed price is precisely the fixed-weight average of the six scenario prices.** The dial then is
just a reweighting of that average:

```
W_i(λ) ∝ WQ6_i × exp(λ·i),  renormalised to sum 1
price(λ) = dot(W(λ), sp)          ≡  rho × P̂(λ) + pedigree_pts
```

λ = 0 gives `W ≡ WQ6` and therefore the printed board price, exactly. λ > 0 tilts weight up the fan;
λ < 0 tilts it toward the floor bands. Ranks re-sort live. Range ±1.2; at λ = −1.2 the weights are
70/21/6/2/1/0 % and the board totals 458,634; at λ = +1.2 they are 0/1/3/9/31/56 % and it totals 947,934.

**The rank baseline is `pricesAt(0)`, not the printed integers.** 153 rows share a printed price, and
integer ties break differently from float ties — baselining on the integers would have reported phantom
rank moves at λ = 0. (This was caught by the headless check and fixed.)

### The disclosed downstream factor `m`

`price6` **is not** P̂. Between them sit the retained production-side layers — the iso multiplier, ITEM-H's
ruled cuts, the D8 graded staleness gate, the KPF compression, the LEG-B v1.1 un-compress map
(`RL_UNCOMP` is ON with `s = 0.1`), the young credit, the M3 in-progress-season clock blend — and the
BOARD→ENGINE numeraire `_PL_F`. Several are **not linear** in `price6`.

So the emit carries one disclosed scalar per row, `m = P̂ / price6`, and sets `six_phat = m × six_raw`.
Measured: min 0.298, p05 0.834, **median 0.971**, p95 1.244, max 3.486.

**What that means for the lens:** it holds each row's *realised* downstream factor fixed across
scenarios. It is a **first-order, proportional reading** of "what if the band were weighted differently",
not a re-run of the engine at a different weight vector. Stated on the page as well as here. All spread
metrics are computed on `six_raw` and are scale-invariant, so `m` does not touch them.

---

## 4. The honest caveat (printed prominently on the page)

**The fan covers the PRODUCTION leg only.** Under the one law

```
price = rho(g)·P̂ + [D(c_u)·(1−rho) + Φ·β·rho]·v0
```

the six scenarios live entirely inside `P̂`. **The v0 (pedigree) leg has its own variance and it is not in
this emit — seat S7 is designing it.**

Consequence: a low-games player shows a **misleadingly small spread**, because most of his price is
pedigree and pedigree's fan does not exist yet. A narrow bar on such a row means *"not measured"*, never
*"safe"*.

- **175 of 804 rows have `rho < 0.3`** — their spread cells are **greyed out** on the page for exactly
  this reason.
- **96 of those carry no production leg at all** (`rho = 0`, gameless). The dial cannot move them; their
  price is 100 % pedigree.

Two further caveats carried on the page:

- **80 rows have a perfectly flat fan** — all six scenarios price identically. Overwhelmingly established
  veterans: their remaining career prices the same at every band level, so the dial does nothing to them.
  A real property of the production model, not a display artefact.
- **341 rows have the q97 ceiling below band 5.** `b6[5]` is the frozen ceiling, but the v7 age-taper
  pulls it back toward the band median (`bb[5] = m + asc·(bb[5] − m)`), so on a taper-hit row the
  "ceiling" scenario prices *below* band 5. Marked ▼ in the S6 column. On those rows pushing λ positive is
  **not** the same as betting on the best case.

---

## 5. What the emit shows

Median S6/S1 across the 530 rows with `rho ≥ 0.3` is **2.63** — the typical measured player's ceiling
scenario is worth ~2.6× his floor scenario, and the board prints one number for that.

The spread is overwhelmingly a **young-player** phenomenon. The widest fans are all 16–27 game
prospects — Mitchell Edwards (RUCK, 16 g, 1,148 pts, S6/S1 = 6,780×), Samuel Grlj (MID, 19 g, 1,831 pts,
6,122×), Cooper Hynes, Hugh Boxshall, Jordan Croft, Zeke Uwland (SD, 17 g, **2,480 pts**, 2,110×) — and
the flattest are the veterans (Saad, Treloar, Aliir, Hill, Maynard: S6/S1 = 1.000 exactly, top-scenario
share pinned at the weight itself, 10.0 %).

That is the finding worth the owner's attention: **the board's most expensive young rows are also its
widest bets, and the printed price hides the whole distinction.** Zeke Uwland and Bradley Hill are priced
2,480 and 1,151 — but one of those numbers is an average over a 2,110× spread and the other is a point
estimate over no spread at all.

`(S6−S1)/S3` is reported but is **unstable when the median scenario is near zero** (Hugh Boxshall reads
656.5). Read it beside S6/S1, never instead of it. This is flagged in the page's definitions box.

---

## 6. Files

| path | what |
|---|---|
| `docs/evidence/order32_s6_2026-08-17/s6_emit_fan.py` | the emitter — standalone, imports the engine read-only, modifies nothing |
| `docs/evidence/order32_s6_2026-08-17/S6_FAN_EMIT.json` | the full emit, 804 rows (1.0 MB) |
| `docs/evidence/order32_s6_2026-08-17/S6_EMIT_out.txt` | the emitter's console record, including the validation block |
| `docs/evidence/order32_s6_2026-08-17/s6_build_page.py` | the page builder (no engine import) |
| `docs/evidence/order32_s6_2026-08-17/S6_LOTTERY_DIAL.html` | **the owner page** — self-contained, sortable, with the λ dial |

Reproduce:

```bash
export PATH="/root/rl_venv312/bin:$PATH"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
       NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
python3 docs/evidence/order32_s6_2026-08-17/s6_emit_fan.py     # ~75s (engine load dominates)
python3 docs/evidence/order32_s6_2026-08-17/s6_build_page.py   # instant
```

The emitter **halts** rather than emitting if any artefact md5 fails, if the reused candidate tree is not
board `fe6be9d6`, if `RL_O31` is not live, or if any of the four validations breaches its bound.
