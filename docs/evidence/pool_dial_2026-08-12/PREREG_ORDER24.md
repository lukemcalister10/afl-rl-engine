# PRE-REGISTRATION — ORDER 24, THE DIAL TABLE (cheap path)

Issue #334. Brief: comment [5265706155](https://github.com/lukemcalister10/afl-rl-engine/issues/334#issuecomment-5265706155).
Branch `build/pool-dial`, cut from `origin/land/pool-update` @ `29a3f87`.

**COMMITTED BEFORE ANY BOARD BUILD, ANY U DERIVATION AND ANY ENGINE EDIT.** Every prediction below is
scored in `SUMMARY.md`. A breach is owned by name and by number; nothing here is edited after the fact.

---

## 0. What I read before writing this, and what I deliberately did not

**Read (facts, not measurements of the fix):** the two engine read sites and their surrounding
machinery in `engine/rl_after/_merged_recover.py`; the landed retention block `_PR_PATH` / `_PR_U` /
`_pr_R` / `_pr_U`; `nseas_pro`, `_fEy`, `_a_share`, `_ev_qual`, `_h_cut`, `sitout_ev`, `_a_blend`,
`ev()`; the signed levels in `engine/rl_after/pvc_curve_v2.json`; the ORDER 21/22/23 harvest and
U-derivation scripts; the store rows of the three named players; and a **count of pool board rows by
current-season games**, which is a store fact used to size the affected population honestly rather
than guess it.

**Not read / not run:** no board has been built, no U′ has been computed, no dialled surface exists.
The numbers below are forward predictions from the code and the store, nothing else.

**Board identities in force (recorded now so they cannot drift):**

| board | md5 |
|---|---|
| `pre_act` — main @ `7f4d5d2`, the last board-touching main commit before PR #462 (whose base was `435fa929`, board identical) | `94f1fec59f99c59d5890d5975c79fa9b` |
| `live` — `origin/main` today | `1dbd1480a34c7823f330273211cbb76a` |
| `pr469` — committed on `land/pool-update` | `665311ca72576df6ff0bbf6dfd007739` |

Recovery of `pre_act` is **not ambiguous**: `git log origin/main -- data/rl_build/rl_app_data.json`
gives `6242e08` (→ `1dbd1480`, the ORDER 20C board that PR #462 landed) immediately above `7f4d5d2`
(→ `94f1fec5`). PR #462's own base commit `435fa929` carries `94f1fec5` byte-identically, and the
PR body itself records `94f1fec5` as its control. Both routes agree.

---

## (a) THE PROPOSED WIRING — exact, and pool-gated only

### The defect, restated in code terms

`ev()` dispatches on `ns = nseas_pro(p,Y)`, a **career** counter (`:1085-1086`): the number of seasons
ever played at or above the 6-game bar (prorated for the in-progress season). `ns==0` → `sitout_ev`;
`ns>=1` → `_a_blend`. ORDER 21/23 bound the pool retention `R` to the first and the pool uplift `U`
to the second (`:2009`, `:2237`), on the reading that the two sites partition the pool population on
"sitter vs non-sitter".

They do not. They partition it on **career** state. The **anchor share** those multipliers are
delivered against is a **current-season** quantity:

```
_a_share(p,Y) = (1 - lam) * exp(-E_q/_A_TAU),   lam = interp(min(gy/fe,6), [0..6], LAM_SIT)
```

`gy` is games **this season**. `LAM_SIT[6]==1.0`, so a pool player at or above the prorated bar this
season carries an anchor share of **exactly zero** and never feels `U` at all; a pool player with a
career but **zero** games this season carries `lam=0` and an anchor share of `exp(-E_q/1.1)`, which
for a thin record is near 1. The premium therefore lands **inversely to current participation**.
`mani-liddy` (MSD 2025 pick 15; 9 games @ 51.1 in 2025, 0 games in 2026) has `E_q = 0.1396`, so
`s = exp(-0.1269) = 0.8808` — the brief's ~0.88 — multiplied against `U(MSD)=3.0959`. 128 → 1025.

### The fix

**Current participation, on the engine's own mid-season convention.** The engine judges the
in-progress season against a **prorated** 6-game bar in three places already:
`nseas_pro` (`games >= 6.0*_fEy(Y,p)`), `bestlvl` (same bar), and `sitout_ev`'s
`gp = min(gy/fe, 6.0)` — games at pace against that same bar. `_fEy(Y,p)` returns `SEASON_PROG`
(0.92 on this board) for the in-progress season, and `1.0` for a completed season **and** for an
availability-register name whose season is priced as complete (mani-liddy and nicholas-martin are
both such names, so their 2026 is judged on a full 6-game bar, not a prorated one — the engine's own
convention, inherited free).

The delivery weight is therefore the **continuous form of the engine's own current-season
qualification**, and is `gp/6` exactly:

```python
def _pr_phi(p,Y):
    fe=_fEy(Y,p); gy=sum(x['games'] for x in p['scoring'] if x['year']==Y)
    return float(min(max(gy/(6.0*fe),0.0),1.0)) if fe>0.0 else 0.0
```

`phi=0` at zero games; `phi=1` at or above the prorated bar; linear between. No new constant, no new
threshold, no new dial, and it reduces to the engine's existing binary current-season judgement at
both ends.

**On D12.** The engine's D12 concave clock (`tau = max(0,Y-debutyr) + fe**1.5`, `:2007`) is the
**depth** convention for the in-progress season — how far down the retention curve a player has
travelled — and it is a *penalty-path* object by its own comment. It is **not** touched and **not**
reused as the participation weight: depth and participation are different quantities, and D12 already
carries `tau` into `_pr_R` at both sites. Using `fe**1.5` as a participation share would say a player
who has played no games is 88% participating, which is the defect inverted. The correct mid-season
convention for *participation* is the prorated bar, which is what `_pr_phi` uses. **This is a design
choice and it is declared here rather than buried.**

**The one delivered multiplier:**

```python
def _pr_mult(p,Y,tau):
    phi=_pr_phi(p,Y)
    return (1.0-phi)*_pr_R(p,tau)+phi*_pr_U(p)
```

**The two sites, both already `p.get('_pool')`-gated, both change to the same object:**

| site | line (pre-edit) | from | to |
|---|---|---|---|
| `sitout_ev` | `:2009` | `if p.get('_pool'): R=_pr_R(p,tau)` | `if p.get('_pool'): R=_pr_mult(p,Y,tau)` |
| `_a_blend` | `:2237` | `if p.get('_pool'): R=_pr_U(p)` | `if p.get('_pool'): R=_pr_mult(p,Y,tau)` |

`Y` and `tau` are both already in scope at both sites. **The career-state partition ceases to select
who gets what; current state does** — the two sites now compute the *same function*, and which one
runs is irrelevant to the multiplier.

**Nothing else moves.** No national code path is touched: both edits are inside the existing
`_pool` guards, `_R_surf` is untouched, `LAM_SIT`, `_a_share`, `_ev_qual`, `_surprise`, `_c_w`,
`C_H`, `_h_cut` and the D12 clock are all untouched. Downstream, `anch = R*entry_anchor(p)` feeds the
surprise damper and the C release automatically and correctly — the anchor is the anchor.

### The dial and the U′ re-derivation

`R′ = 1 + α(R−1)` applied elementwise to the wired retention surface (`_PR_PATH` 9×3×6 and
`_PR_WHOLE` 3×6), α ∈ {0.25, 0.5, 1.0}. `α=1.0` leaves the surface identical and is therefore the
**pure delivery fix**.

`U′` is re-derived per pathway per α so that mean preservation holds **under the new delivery
weights**, on the ORDER 21 historical harvest population, entry-weighted exactly as ORDER 21/22/23
weighted it:

```
mean = SUM_all e * [ (1-phi)*R' + phi*U' ] / SUM_all e  ==  1.0000000000
=>  U'  =  ( SUM_all e  -  SUM_all e*(1-phi)*R' )  /  SUM_all e*phi
        =  1 + [ SUM_all e*(1-phi)*(1-R') ] / [ SUM_all e*phi ]
```

which collapses to the ORDER 22/23 formula exactly when `phi ∈ {0,1}` and `phi==0` coincides with the
career-state sitter flag. The harvest is re-run (`o24_uharvest.py`, adapted from `o22_uharvest.py`)
solely to record each cell's **current-season games** so `phi_c = min(g_Y/(6*fe_Y), 1)` can be formed;
for the historical cells `fe=1.0`, so `phi_c = min(g_Y/6, 1)`. Population gates, depth convention and
entry weights are carried verbatim.

**Levels: FROZEN.** `engine/rl_after/pvc_curve_v2.json` is read from the file as committed on this
branch (the ND65+ cap-removal law as landed) and is **not modified**, and no value from any brief is
hardcoded. No level iteration.

---

## (b) THE PREDICTIONS

Population facts established before predicting (store + branch board, 243 pool rows):

| cell | n |
|---|---:|
| current sitters, `gy26 == 0` | 55 |
| — of which career-qualified (**the Liddy cell**) | 10 |
| partial participants, `0 < gy26 < 6*fe` | 42 |
| full participants, `gy26 >= 6*fe` → anchor share **exactly 0** | 146 |
| **rows the pool multiplier can reach at all** | **97** |

### Structural predictions

**P1 — CONTROL.** Rebuilding the board on the unmodified branch reproduces
`665311ca72576df6ff0bbf6dfd007739` byte-identically.

**P2 — SEPARATION.** ND movers (rows with `ty=='ND'` and `ep<=64`) between `live` `1dbd1480` and each
of the three α boards: **exactly 0**, all three.

**P3 — MEAN PRESERVATION.** All nine pathways and ALL POOL print `1.0000000000` to 1e-9 at every α.

**P4 — U′ IS EXACTLY LINEAR IN α.** Because the numerator carries `(1−R′) = α(1−R)` and the
denominator `Σ e·φ` is α-free, `U′(α) − 1 = α·(U′(1.0) − 1)` to floating precision for every pathway,
including ALL POOL. Consequently `U′(0.25) < U′(0.5) < U′(1.0)` for every pathway.

**P5 — FULL PARTICIPANTS DO NOT MOVE, AT ALL, AT ANY α.** A pool row with `gy >= 6*fe` has
`lam == LAM_SIT[6] == 1.0`, hence anchor share exactly 0, hence no exposure to the pool multiplier.
All **146** such rows are byte-identical to `pr469` in all three α columns.

**P6 — AT α=1.0, NEVER-QUALIFIED CURRENT SITTERS ARE BYTE-IDENTICAL TO `pr469`.** `φ=0` and `R′=R`
give `(1−0)*R + 0*U = R` exactly. All **45** such rows unchanged. Therefore pool rows moving between
`pr469` and `a100` number **at most 52** (10 Liddy-cell + 42 partials) and I predict **≥ 38**.

### U′ direction per pathway (vs the landed `_PR_U`)

The new sitter mass gains every career-qualified row sitting this season, at **deep** τ where
`R ≈ 0.35–0.50` so `(1−R)` is large; the new participating mass gains the partially-playing
never-qualified rows, which leave the numerator. Which wins depends on each pathway's sitter share.
Writing `x = Σ_A e / Σ_B e` (old sitter mass over old non-sitter mass), the numerator scales by
roughly `(1 − φ̄_A)` while the denominator gains `x·φ̄_A`. For large `x` the denominator gain
dominates; for small `x` the numerator's new B-sitters dominate.

**P7.** Pathways with a **high** landed U fall; pathways with a **low** landed U rise; the crossover
sits between U ≈ 1.4 and U ≈ 1.8. Specifically at α=1.0:

| pathway | landed U | prediction |
|---|---:|---|
| MSD | 3.0959 | **falls**, into [2.0, 2.9] |
| PDN | 2.0956 | **falls** |
| PDA | 1.6144 | falls or ~flat |
| UNR | 1.5041 | either side of flat (nearest the crossover) |
| PDS | 1.4160 | either side of flat |
| ND>64 | 1.3687 | **rises** |
| IRE | 1.3380 | **rises** |
| RD | 1.2063 | **rises**, into [1.20, 1.33] |
| SSP | 1.2001 | **rises** |
| ALL POOL | 1.2522 | rises |

Scored as: (i) the MSD and PDN falls, (ii) the RD/SSP/ND>64/IRE rises, (iii) the crossover lying in
[1.4, 1.8]. Each scored separately.

### The named rows

Selection criteria for the two rows I choose, stated before I look at any result:

- **Healthy currently-playing pool rookie — `marcus-herbert`** (MSD 2026 pick 13, 8 games in 2026,
  live = pr469 = 906). Criteria: (1) a pool pathway; (2) his first professional season is the current
  one; (3) current-season games comfortably above the prorated bar (8 vs 5.52) so `φ = 1.0` exactly;
  (4) unmoved by PR #469, so his α columns isolate this order's lever alone. He is the row that shows
  the fix does **not** reach a healthy playing rookie.
- **Established multi-season MSD star — `jai-newcombe`** (MSD 2021 pick 2, 121 career games, 6
  qualifying seasons, 21 games in 2026, live = pr469 = 4883). Criteria: the **highest live-board
  value** among MSD rows, with ≥5 qualifying seasons and currently playing. He is the row that shows
  the fix does not reach an established playing pool star.

**P8 — `marcus-herbert`: Δ = 0 exactly vs `pr469` at all three α.** (φ=1 ⇒ anchor share 0.)

**P9 — `jai-newcombe`: Δ = 0 exactly vs `pr469` at all three α.** (Same mechanism.)

**P10 — `mani-liddy` falls hard at every α, monotonically in α.** His multiplier goes from
`U(MSD)=3.0959` to `R′(MSD, nonKPP, τ≈1.88)`: predicted `R(τ)=0.4294` at α=1.0, `0.7147` at α=0.5,
`0.8577` at α=0.25 — a **7.2× reduction** in the anchor leg at α=1.0, against an anchor share of
0.8808. Price predictions (rough magnitude, per the order):

| | pr469 | a025 | a050 | a100 |
|---|---:|---:|---:|---:|
| `mani-liddy` | 1025 | **[200, 500]** | **[160, 420]** | **[90, 300]** |

with `a100 < a050 < a025 < 1025` strictly, and `a100` within a factor of ~2.5 of the live 128.

**P11 — `robert-hansen` falls hard at every α, monotonically in α.** MSD, SF ⇒ nonKPP, debut 2023,
`fe=0.92`, so `τ = 3 + 0.92**1.5 = 3.88` and predicted `R(τ) = 0.5095` at α=1.0 (0.7548 at 0.5,
0.8774 at 0.25). `E_q = 0.7235`, anchor share `0.518`.

| | pr469 | a025 | a050 | a100 |
|---|---:|---:|---:|---:|
| `robert-hansen` | 650 | **[170, 340]** | **[140, 300]** | **[70, 220]** |

**P12 — `nicholas-martin` moves DOWN but is NOT material.** He is the third of the three named
because he is the *counter-example inside the same cell*: an established SSP career (83 games, 4
qualifying seasons) sitting out 2026, so he is in the Liddy cell by mechanism — but his evidence fade
has almost extinguished the anchor leg (`E_q = 3.989`, `s = exp(-3.626) = 0.0266`). His multiplier
falls from `U(SSP)=1.2001` to `R′(SSP,nonKPP,τ=5)=0.4782` at α=1.0, but only 2.7% of his price leans
on it. **Predicted |Δ| ≤ 25 points at every α, direction DOWN, and he fails the ≥20-point / ≥10%
materiality test at α=0.25 and α=0.5.** (At α=1.0 he may just reach 20 points; scored either way.)

### Counts and totals

**P13 — MATERIAL-MOVER COUNT.** Rows in `MOVERS_TABLE.md` — pool rows where **any** of `pre_act`,
`pr469`, `a025`, `a050`, `a100` differs from `live` by ≥20 points **or** ≥10%: predicted **[110, 210]**.
Restricted to the α columns alone (any α column vs live, material): predicted **[45, 100]**.

**P14 — POOL TOTAL.** Live pool total is 125,166 (746,043 − 620,877); pr469's is 132,960. The
delivery fix withdraws the premium from current sitters and re-lands only part of it on partial
participants, so every α total sits **below pr469 and above live**, ordered
`live < a100 < a050 < a025 < pr469`. Predicted `a100` pool total ∈ **[126,500, 132,000]**.

---

## (c) Instruments that halt

- **Control mismatch** (P1 fails) → BLOCKER, stop, report, build nothing.
- **Any mean-preservation cell ≠ 1.0 within 1e-9, at any α, any pathway** → HALT, report.
- **Any ND mover on any α board** → HARD FAILURE, stop, report.
- **Non-deterministic board build** → BLOCKER.

## (d) The absolute-price caveat, carried verbatim into every artifact

> levels frozen at #469 values; absolute prices ±few points, MSD up to ~5%; re-trued at landing

## (e) Scope fence

Nothing lands. `engine/rl_after/pvc_curve_v2.json` is not modified. `main` is not touched. PR #469 is
not touched. The PR opened by this order is based on `land/pool-update`. **MERGE NOTHING.**
