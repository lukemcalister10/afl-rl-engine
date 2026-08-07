# STAGE 5 — THE CONSISTENCY PASS, and what it revealed

Owner-authorized at **#334 comment 5217293177**: *one named solver correction, and the result is FINAL for
stage 5 whatever it lands.* This file is the record of that pass. **The STOP-report files (`README.md`,
`MEMO.md`, `FRONTIER.txt`, `teach_g5.py`, `g5_table.json`) are left in place; the frontier history stays.**

---

## 1 · THE HEADLINE, and it is not the one anyone expected

**The consistency pass made the landing WORSE, and it was still the right correction.**

| | frozen-lam pass (the STOP report) | **CONSISTENCY PASS (LANDED)** |
|---|---|---|
| whole-cohort yr1, teaching window | 0.9945 | **0.9908** |
| quiet starters 1-5 | 0.8925 | **0.8762** |
| board | `bad1961e` *(never landed)* | **`13f8c2e0`** |
| G table md5 | `1dc66750a51d04eb9b35b33685960feb` | **`1bd109cb0b428ed91c1988c0c72d4000`** |

The frozen-lam solve was not merely imprecise — **it OVERSHOT its own cell targets** (median +2.06%) and,
worse, **it breached the very aging law it declared**, pricing the deep-pick cells above their entry
anchors. The corrected solve removes both. The landing falls because the first landing was partly built
on those two errors.

**My own MEMO §4 diagnosis was WRONG, and this pass disproves it.** I wrote that the class landed at 93.5%
of its measured future because the solver undershot. It did not undershoot; it overshot at every node it
was free at. The 93.5% came from somewhere else entirely — §3.

---

## 2 · The solver, exactly

For a teaching row `i` under cell factor `g` — the engine's own price expression, nothing invented:

```
a_i(g)   = g · R_i · A_i                                the lifted anchor leg
s_i(g)   = |log(e_i / a_i(g))|                          the surprise, RE-READ at the lifted anchor
u_i      = 1 − rho(gp_i)/rho(6)                         the unresolved share (fixed)
x_i(g)   = xb_i + SUR_W · s_i(g) · u_i                  xb_i = 1 + PED_BAR·(1−q_i)
lam_i(g) = lam0_i ^ x_i(g)
P_i(g)   = (1 − lam_i(g))·a_i(g) + lam_i(g)·e_i         THE INSTALLED PRICE
```

and the cell solves `Σ w_i · P_i(g) = Σ w_i · F_i` by bisection. `F` — each cell's own measured discounted
future — **is unchanged**; so are the axes, knots, kernel, bandwidths, pooling rule, and the pins
`G(τ=0)≡1` and `τ=6 → 1`.

Three self-checks, all passed before any root was taken:

* **parameter recovery is exact** — `xb_i` is recovered from the published per-row measurement
  (`xb_i = log(lam_i)/log(lam0_i) − SUR_W·s_i(1)·u_i`) and must reproduce each row's own measured `lam`:
  **0 of 3517 rows fail**. The solve is measuring the same engine the board runs.
* **monotonicity** of `Σ w P_i(g)` is checked on a 13-point grid at every node before bisecting; a
  non-monotone node HALTS rather than returning a root. **None halted.**
* **no bracket exhaustion** — 0 of 300 nodes hit the `g ≤ 12` ceiling.

`CONSISTENCY_VERIFY.txt` proves the pass does what it claims, node by node: **nodes landing within 0.1% of
their own target go from 3/300 to 51/300**, and the median installed-to-target ratio goes from 1.0206 to
1.0000. **102 of 300 nodes move DOWN; none moves up** — the amplifying feedback means a *smaller* G
achieves the same price.

---

## 3 · WHAT THE PASS REVEALED: the binding constraint is a LAW, not the solver

With the solver honest, the cells that still miss their targets are exactly the ones a **law** is holding.
From `CONSISTENCY_VERIFY.txt`, at τ=1:

| node | installed / target |
|---|---|
| nonKPP pick 50, 2 games | **0.8517** |
| nonKPP pick 50, 5 games | **0.9147** |
| nonKPP pick 65, 2 games | **0.8306** |
| RUCK pick 65, 2 games | **0.7638** |

These are held at the **aging law** — *no cell taught an INSTALLED price above its own entry anchor*. They
sit below their measured futures because **for the deep-pick quiet starters the measured future EXCEEDS
the entry anchor**: `F/A` runs up to **1.17** there. Round 2 said exactly this — *"at picks 41–64 the gap
is dramatic (realized yr4 2.15 vs clock 0.58)"* — and the law refuses to follow it.

**A correction I owe:** `MEMO.md §3c` asserts that the measured `F/A` came back *"≤ 1 in EVERY resolved
cell"*, so the aging cap *"binds only where the estimate is noise"*. **That is false.** It was read off
coarse exploratory aggregates, not the kernel nodes. On the nodes, `F/A > 1` on the deep-pick τ=1 cells —
precisely the population the act exists for. The claim is struck here rather than edited out of the MEMO.

### What the law costs, measured

`RL_G5_NOCAP=1` rebuilds the identical surface with the aging cap lifted — **a DIAGNOSTIC, never shipped**
(`g5_table_NOCAP_DIAGNOSTIC.json`, md5 `217cd4b22807823e85a2d326644bd526`):

| | shipped (law held) | diagnostic (law lifted) |
|---|---|---|
| whole-cohort yr1 | **0.990805** | **1.000020** |
| quiet starters 1-5 | 0.8762 | 0.9166 |
| picks 21-64 | 0.9737 | 0.9948 |

**The aging-on-the-price law is the entire remaining distance to the 1.00 floor, to four decimal places.**

### Why the law was NOT lifted

1. The supervising seat's instruction names it among the laws to keep: *"same laws (aging on the price,
   taper, smoothness)"*.
2. Relaxing a law this seat itself introduced, at the exact moment it is the only thing between the act
   and its target, is the definition of tuning. The number is reported so the decision belongs to whoever
   owns it.

### The argument the owner may want to weigh

The aging cap is **this seat's construction (pass 2), not a governing-document law.** The directive and
Addendum 2 say only that `G·R` is *isotonic non-increasing in τ* — a statement about SHAPE, which is
enforced separately and independently. And the owner's own words allow value above entry:

> *"Even young players should lose value in line with age. It's career resources they're chewing up. **It's
> just the trend upward because often performance gives a greater positive signal than aging takes.**"*

A pick-50 quiet starter who played three games and whose measured future is 1.17× his entry anchor is
that sentence. **Whether the cap should stand is an owner question, and it is now a number: 0.9908 with
it, 1.0000 without it.**

---

## 4 · What the pass did NOT fix, stated plainly

Hitting every **cell** target is not hitting a **population** target. The teaching cells are dominated by
the pool routes (2,834 of 5,675 scanned rows); the ND 1-64 year-1 slice the no-arb landing is read on is a
minority inside those same cells. A cell can price its own aggregate at `F` while the ND subset within it
lands elsewhere. **That is a basis question, not a solver question, and this pass does not touch it.**

---

## 5 · The landing, on both presentation bases

Per the owner's ruling (**#334 comment 5217177098**) every cohort table leads with the **full cohort**.
`OWNER_BASIS.txt` carries it in full.

| population | n | baseline | **LANDED** | move |
|---|---|---|---|---|
| **FULL COHORT ND+pool, 2004-2025** | 2,517 | 0.908179 | **0.946050** | +0.037870 |
| ND 1-64, 2004-2025 | 1,383 | 0.949994 | **0.988526** | +0.038531 |
| pool routes, 2004-2025 | 1,134 | 0.752800 | **0.788214** | +0.035414 |
| class 2023 ND | 64 | 1.043485 | 1.077494 | +0.034010 |
| class 2024 ND | 64 | 0.875930 | 0.901970 | +0.026040 |
| class 2025 ND | 58 | 0.926992 | 0.947385 | +0.020393 |
| ND 1-64, 2004-2022 *(teaching window)* | 1,197 | 0.950431 | **0.990805** | +0.040374 |

The ND figure moves only **−0.0023** between the owner window and the teaching window — the landing story
is the same on either, as the ruling anticipated. Stage 5 **did** reach the pool quiet starters
(0.7528 → 0.7882); the remaining full-cohort drag is the pool leg's deep sub-par level, whose own honesty
is a separate fired measurement and is **not this act's to claim**.

---

## 6 · Gates on the landed board `13f8c2e0`

| gate | result |
|---|---|
| **landing floor** yr1 > 1.00 | **0.990805 — still below.** Reported, not re-taught. The owner ruled the result final either way. |
| below-own-pick falls | **PASS** — matrix 939 → **888**, board 374 → **371**; mean shortfall falls on both |
| **Mraz tiered** | **PASS — `1585 → 1645` = `3.1038×` his pick, tier "3.0-3.5×, pass disclosed".** Taught G at his cell **1.141258** (was 1.157941 under the frozen-lam solve — the fixed point moved him DOWN) |
| Nairn | `471 → 605` (+28.45%), G **1.305547** |
| band [1.35,1.45] at each own peak | **PASS** whole **1.432651** (yr4), 1-20 **1.429314** (yr4); 21-64 **1.471250** (yr6) outside but **byte-identical to baseline** |
| entry-year rides | **PASS, no machine STOP** — largest excess over draft day **+3.68pp/yr** (whole), +3.24 (1-20), +1.96 (21-64); line is +5.00 |
| FRONT-LOADED guide | **PASS** — yr1→2 exceeds yr3→4 |
| within-class | **PASS** — realised max `|ΔlnG|/Δτ` **0.446382** vs the fitted taper's own max slope **0.535608**. no-taper −30.8% → landed **−25.1%** vs baseline −25.4%: the taper recovers **105.4%** of the deepening |
| non-uniformity + convergence | **PASS** — gap **0.052317 → 0.027884** (46.7% closed); ordering 1-20 < 41-64 < 21-40, consistent with round 2 |
| ladder seam | **PASS — 1.8868% of ±2.00%** |
| boundary probes | **PASS** — bar byte-identical on all 5 probes (seam 1.0000); rollover step in G **9.9e-06**; zero new cliffs g=1..10 |
| recalculation law | **PASS** — G spread **1.0202 .. 1.2511** over a frozen year-1 record |
| **dial-0** | **PASS — `b56bbdde` byte-exact through the full gate** |
| fit coupling | **NONE** — v0surf `9713ec6c` reproduced at `RL_G5_W` 0 / 1.0 / 2.0 |
| machinery | PARITY **804/804 eps=0** · numéraire **3000** · book↔board **PASS** · Guard 5 **PASS** · manifest **62 vars** · selftest **143/0, 0 re-points** |
| movers | **66 of 804, ALL UP, zero cuts**; board total **+0.3658%** |
| **near-projection** | **FAILS, disclosed** — unchanged in character from the STOP report; it is a lift, and the band population is the target population |

---

## 7 · Artifacts

| file | md5 | status |
|---|---|---|
| `g5_table_LANDED.json` → `engine/rl_after/g5_table.json` | `1bd109cb0b428ed91c1988c0c72d4000` | **SHIPPED** |
| `g5_table.json` (frozen-lam, first pass) | `1dc66750a51d04eb9b35b33685960feb` | STOP record, kept |
| `g5_table_NOCAP_DIAGNOSTIC.json` | `217cd4b22807823e85a2d326644bd526` | **diagnostic only, never installed** |
| `teach_g5_consistency.py` · `consistency_log.txt` · `CONSISTENCY_VERIFY.txt` | — | the pass |
| `teach_g5.py` · `teach_g5_PASS1_superseded.py` | — | the earlier passes, kept |
