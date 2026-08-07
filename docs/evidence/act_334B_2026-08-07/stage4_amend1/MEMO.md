# STAGE 4 AMENDMENT 1 — DESIGN MEMO: the surprise-scaled evidence trust

Branch `landing/334-stage-b`, baseline `44950de` (stage 4, board `b490ae8b`). Nothing merges to main;
no PR; no tag. Adoption remains the owner's separate click.

## The owner's words, and what they ask for

Stage 4 conditioned the thin-record evidence weight on **pedigree**. The owner's verdict on the result —
Mraz still at **2,898**, rank 56, the #3 key defender on the board, off four games:

> "4 games of sample, especially when it's so far from the projection, shouldn't be trusted as much,
> surely."

And the binding constraint that came with it: **no broad hit to young players**. Players performing near
projection keep today's reactivity. No rebalance.

Two things are being said, and only the second is new. The first is *small sample* — stage 4 already reads
that, through `lam`'s games ramp. The second is **"so far from the projection"**, and stage 4 does not read
it at all. Stage 4 asks *whose* record this is. It never asks *what the record claims*. Mraz's four games
claim a **23.95×** re-rate against his own decayed draft-day anchor, and stage 4 charged that claim the
identical evidence bar it charges a claim of 1.05×.

**That is the missing axis, and this amendment adds exactly it: SURPRISE.**

## 1. WHY SURPRISE IS THE RIGHT AXIS — the selection argument

This is not a taste argument, and it is worth stating plainly because it is the whole justification for
shrinking a *measured* number toward a *prior*.

A fringe player's played games are **selection-biased upward**. He is not sampled at random from his own
distribution: he is picked when he is hot, kept in when he goes well, and dropped when he does not. The four
games on his record are, to a first approximation, **his best four**. The larger the surprise a thin record
claims, the more of that surprise is the selection rather than the player — a purple patch rather than a
revelation.

So the shrink should scale with **the size of the claim**, and it should **dissolve as real games
accumulate** and the selection washes out. That is the design, in one sentence.

Note what this argument does *not* say. It does not say a breakout is impossible, it does not cap anything,
and it does not touch a player performing near his projection — a small sample that claims little is
claiming little whether it was selected or not. The correction is proportional to the claim, and at zero
claim it is exactly zero.

## 2. THE STATISTIC, and the anchor choice (DISCLOSED, and forced)

```
s = | log( e_full / anchor_full ) |          anchor_full = R * entry_anchor(p)
```

`e_full` is the demonstrated-production price (the evidence). `anchor_full` is the **prior-implied full
price** — and it is **the same anchor leg that appears in the blend one line below**, not the undiscounted
`V0`.

**The choice is forced, not preferred, and this is the key design point.** The blend is

```
price = (1 - lam) * anchor_full  +  lam * e_full
```

so `s == 0` ⟺ `e_full == anchor_full` ⟺ **the blend is degenerate and `lam` cannot move the price at all**.
Measuring the surprise against the discounted anchor is therefore the only pairing for which

> "zero surprise" and "this change does nothing"

are **the same statement — identically, not approximately**. The directive's zero-surprise constraint holds
as an *identity* rather than as a measured near-miss. Against the undiscounted `V0`, `s` would be non-zero
at exactly the point where the change is inert, and zero at a point where it bites: the statistic would not
be measuring the re-rate the mechanism actually performs.

It also means the price move is doubly damped near projection: a small `s` gives both a small change in
`lam` **and** a small `(e_full − anchor_full)` for that change to act on. That is why the near-projection
proof passes with room to spare rather than by a whisker.

## 3. THE RESOLUTION FADE — reused, not invented

```
u = 1 - rho(gp) / rho(6)          rho(g) = g^2 / (g^2 + g + K)          K = _ABS_FADE_K = 5.8
```

`rho` is **the engine's own R100.11 evidence-resolution curve** (`_merged_recover.py:722`), at its own
pinned `K`, normalised at the **ruled 6-game establishment bar**. `u` is precisely the complement of the
`#336` amendment-3 resolution weight `r(g)` (`rl_model._resolve_w_336`) — i.e. **the unresolved share of
this record**. **No new constant and no new width is set anywhere in this amendment.**

* `u(0) = 1` — a record of nothing is entirely unresolved.
* `u(6) = 0` **exactly** — at the establishment bar the surprise demand vanishes and stage 4 is reproduced.
* `gp` is the **same `min(games-at-pace, 6)` clamp the `lam` ramp itself interpolates on**, hoisted rather
  than re-derived, so `u >= 0` by construction with **no new clip**. On this path `gp < 6` strictly anyway
  (`ns==0` means no season reached the prorated bar); measured maximum across the board is **5.6818**.

Measured shape: `u` = 1.000 / 0.792 / 0.482 / 0.259 / 0.115 / 0.021 / 0.000 at `gp` = 0..6.

## 4. THE COMPOSITION — additive, and why (a judgement call, disclosed)

```
lam_eff = lam ** ( 1 + PED_BAR*(1-q)  +  SUR_W*s*u )
              \_______________/    \________/
               stage 4, untouched   amendment 1
```

The exponent is denominated in **"passes of the existing `lam` ramp this record must clear"**. Stage 4
demands extra passes for thin pedigree; this amendment demands extra passes for a large claim on a thin
sample. **Two independent demands on the same evidence SUM.**

The multiplicative form the directive offered — `lam_eff ** (1 + SUR_W*s*u)` — was built and measured too
(`COMPOSITION_CHECK.txt`). It reaches the same Mraz landing at a smaller dial, but it **scales the surprise
demand by the pedigree demand**, and that compounds the one channel the two terms genuinely share.

**IS IT DOUBLE-CHARGING? Measured, and the verdict is NO.** The two terms overlap in exactly one place: the
sit-out depth. It enters stage 4 through `sit` (a ratio of the retention surface) and enters `s` through `R`,
which discounts the anchor. Pedigree — the pick axis — is **not** shared. On Mraz:

| | |
|---|---|
| anchor undiscounted `entry_anchor` | 461.25 |
| retention `R` at his sit-out depth | 0.45877 |
| anchor discounted `R × entry_anchor` | 211.61 |
| `s` against the **discounted** anchor (**shipped**) | **3.176066** nats |
| `s` against the undiscounted anchor | 2.396779 nats |
| **the sit-out's contribution to `s`** | **0.779287 nats = 24.5% of `s`** |
| stage 4's separate charge for the same sit-out | `sit` = 0.656601 (inside `q` = 0.137813) |

The overlap is real, but it is not a double charge, for two reasons and the second is decisive:

**(a)** The two terms answer different questions about the same fact. `sit` asks *how much prior expectation
survives the year he did not play*; `R` inside `s` asks *what his prior price is TODAY*, which is what the
evidence is actually contradicting. A sit-out lowers both the expectation and the baseline the claim is
measured from, and **both are true**.

**(b)** The anchor choice is **forced** by §2. There is no version of this statistic that measures the
re-rate the mechanism performs and does not carry `R`.

So stage 4's pedigree/sit-out machinery is **composed with, not deleted**, and the sit-out prior effect is
retained in both terms. **Additive** keeps the shared channel charged once per term instead of once per term
*plus their product*.

The honest cost of that choice, stated: under the additive form a top-pick player with a big claim is
charged the **same** surprise demand as a deep-pick player with the same claim, and only stage 4's own term
separates them. The pedigree pair still separates — it separates by stage 4's margin, not a compounded one.

## 5. THE DIAL, THE LADDER, AND THE TENSION

**`RL_SUR_W = 5.0`.** One new dial. `RL_SUR_W=0` reproduces the stage-4 board **byte-exact** (proven: board
md5 `b490ae8b3bbd28b908ccb923ed8412c1`, the committed stage-4 pin, rebuilt through the full gate).

**The criterion, stated before the ladder was read:** Mraz lands in the low thousands — roughly 2–3× his
pick's value of 530, i.e. ~1,100–1,600 — **while players within ±25% of projection move by less than 1%**.

| `SUR_W` | Mraz (board) | × pick-35 value | moved | up | worst mover | board total Δ | band moved | band max abs rel (cont / board) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 2,898 | 5.47× | 0 | 0 | — | 0.000% | 0 | 0.000% / 0.000% |
| 2.0 | 2,267 | 4.28× | 41 | 6 | 43.18% | −0.184% | 2 | 0.310% / 0.518% |
| 4.0 | 1,784 | 3.37× | 44 | 7 | 50.76% | −0.314% | 2 | 0.555% / 1.036% |
| **5.0 (SHIPPED)** | **1,585** | **2.99×** | **45** | **7** | **51.52%** | **−0.365%** | **2** | **0.657% / 1.036%** |
| 6.0 | 1,413 | 2.67× | 45 | 7 | 52.27% | −0.408% | 2 | 0.748% / 1.554% |
| 7.0 | 1,262 | 2.38× | 45 | 7 | 56.45% | −0.447% | 2 | 0.845% / 1.554% |
| 8.0 | 1,129 | 2.13× | 44 | 7 | 61.04% | −0.479% | 2 | 0.955% / 1.554% |

**Why 5.0:** it is the **smallest rung at which Mraz lands inside the stated range**. The owner's *binding*
constraint is the near-projection one — "no broad hit to young players" — so the dial takes the least value
consistent with his calibration target, and the collateral on the near-projection band is the minimum the
target admits. 5.0 also carries the smallest integer-board disturbance of any qualifying rung (2 board points
on the single affected row, against 3 at every rung above).

### ⚠ THE TENSION — reported, not forced

**On the criterion as literally written, NO rung achieves both conditions.** That is stated plainly because
it is true, and the directive's instruction was to report it rather than force it.

The entire gap is **one row**. `Jaxon Artemis` (SD, MSD pool, board value **193**, three games, claiming
1.152× his projection) moves **193 → 191, two board points**. His **continuous** move — the engine's own
real-valued price, before the board rounds it to an integer — is **−0.6166%**, i.e. **1.19 board points**,
comfortably under the 1% bar. But his board value is 193, so **one board point is already 0.518%**, and a
"<1%" criterion on that row means *"moves by less than 1.93 board points"*. The integer grid cannot express
the move the engine actually made.

Measured both ways, across the whole band (n=6):

| ruler | max abs rel in band | verdict |
|---|---|---|
| **continuous engine price** | **0.6574%** | **PASS** |
| integer board value | 1.0363% | **FAIL** (one row, by 0.04 percentage points, on a 2-point move) |

This is a **measurement-granularity result, not a re-rate**. It is filed as a criterion failure anyway,
because it is one, and the owner should rule on it rather than have it smoothed away here. If the integer
reading is binding, `SUR_W = 2.0` satisfies it (band max 0.518% = one board point) at Mraz 2,267 — outside
the Mraz target. **There is no rung that satisfies both on the integer ruler.** Both numbers are one edit
apart in either direction.

## 6. WHAT THE CHANGE DOES, AND TO WHOM

**45 of 804 board rows move (5.60%)** — 38 cuts, 7 lifts. **Every mover is on the thin-record path.** Board
total 654,570 → 652,183 (**−0.365%**).

The population is ordered by **surprise**, not by pedigree, position or value. Sorted into quartiles of `s`,
the mean absolute continuous move over the 56 thin-record players with live evidence:

| quartile of `s` | range | n | mean abs move |
|---|---|---|---|
| 1 | 0.009 – 0.351 | 14 | **1.90%** |
| 2 | 0.364 – 0.689 | 14 | 4.02% |
| 3 | 0.715 – 1.190 | 14 | 16.86% |
| 4 | 1.191 – 3.536 | 14 | **25.77%** |

That monotone ladder **is** the mechanism, read off the built board.

**Established players are untouched by construction, not by tuning.** `sitout_ev` has exactly one caller: the
`ns==0` arm of `ev()`. Of the 165 players on that path, **109 have zero 2026 games** — `lam == 0`, `0**e == 0`
— and **all 109 are byte-exact**. A resolved player never enters the function at all.

**SYMMETRIC, deliberately.** `s` is an **absolute** log-ratio, so a four-game *collapse* from a high prior is
shrunk toward that prior by exactly the same amount as a four-game breakout of the same log size — and the
collapsed player's price therefore **rises**. This is the owner's own standing **L-SYMMETRY** law (register
item 108), and a one-sided `max()` would be a **branch**, refused under L-SMOOTH. **7 players move up**; all
seven are named in `MOVERS_FULL.txt` rather than hidden. As at stage 4, this is the one place the change does
something the owner did not literally ask for, and it is flagged here as such.

## 7. CONTINUITY, MONOTONICITY, AND THE SEAM

* **Continuous everywhere (L-SMOOTH).** `s` is an absolute log of a ratio of positive quantities; `u` is a
  ratio of polynomials in `g` composed with the existing `min(·,6)` clamp. No threshold, no counter, no
  branch, no band, no era. The one conditional in the new code is a **domain guard** on `log`, in the same
  idiom `_ped_prior` already uses for `r0>0`; it is taken **0 times out of 165** on the board, measured.
* **Endpoints fixed.** `0**e == 0` and `1**e == 1`, so `lam(0)=0` and the graduation continuity
  `lam(prorated bar)=1` survive at every surprise, **by construction**.
* **The seam is inert twice over.** At the bar, `lam(6)=1` and `1**e==1` (stage 4's argument, still holding),
  **and** `u(6)=0` exactly (this amendment's own normalisation). Measured: **prices AT the establishment bar
  are byte-identical across the change on all four probes; SEAM RATIO = 1.0000** on every one.
* **"More games → less shrink"** is the `u(g)` row, and `u` is **strictly decreasing in `g` on every probe,
  always**, by construction (`rho` is strictly increasing).

**One honest wrinkle, measured and disclosed.** In a synthetic sweep that replaces a player's record with a
single season of `g` games at a fixed average, the *level ratio* amendment/stage-4 is **not** monotone in `g`
— on Mraz it runs 0.744 (g=1) → 0.233 (g=2) → 0.223 (g=3) → 0.547 → 0.981 → 1.000. The deepest shrink is at
two or three games, not at one. **That is correct, and it is the mechanism working:** in that sweep `e_full`
— and therefore `s` — *grows with `g` too*. At one game the player is barely claiming anything above his
anchor, so there is little to shrink; by two or three games he is claiming a large re-rate while still almost
wholly unresolved, which is precisely the population the owner pointed at. The design constraint is *more
games → less shrink **at a fixed claim***, and that is `u(g)`, which is strictly monotone. The law that must
not break is the **B6** monotonicity of the **price** — more games at the same rate is never worth less — and
it **holds on every probe**, with **no new non-monotonicity introduced anywhere in `g = 1..10`**.

## 8. FIT COUPLING — the verdict is NO, and it is measured

The change stays **strictly inside `sitout_ev`**, whose only caller is the `ns==0` arm of `ev()`;
`_build_v0_curve` fits `_v0_raw` (`raw_ev × iso` at draft age) over the ND roster and **never calls `ev()`**.
So `RL_SUR_W` is **not** a `_V0SURF_GATES` key and **no refit is owed** — the same static argument stage 4
made, on a change that did not escape the same function.

Re-verified by the same **three-signature declared-refit check**, at `SUR_W` **0.0 / 5.0 / 20.0** — four times
the shipped magnitude. All three produced the identical config signature `3e8e50de5103` and byte-identical
fitted surfaces, md5 `9713ec6c83270ab916bb4a5e3ded6cb3`, **which is the current committed pin**.
**`v0surf` is UNMOVED and the pickle was not rewritten.** See `FIT_COUPLING.md`.

## 9. What was NOT done

* **No era anything.** Nothing here reads or writes an era table; the LAW holds.
* **The 1.40 target untouched.** No ladder, no curve, no numéraire, no `pvc_curve_v2.json`, no re-anchor.
  The settled ladder is byte-identical to stage 4 at all 64 picks (asserted in the workbook build).
* **No new hard bands, no thresholds, no counters, no branches.**
* **Stage 4 is not deleted.** `PED_BAR` and `_ped_prior` are untouched; `RL_PED_BAR` still reproduces stage 3
  on its own leg.
* `rl_model.py`, `engine/forward_valuation/`, the store, the band, `q97m`, the entrant seal, the
  release-pick-curve contract: all **UNTOUCHED**. **One engine file moves.**
* **The band check is REPORTED, never retuned.** The whole-cohort peak went **1.432196 → 1.432092** — inside
  `[1.35, 1.45]`, and a rounding-scale move that happens to sit marginally closer to 1.40. Nothing was tuned
  to achieve that, and nothing would have been changed if it had gone the other way.
