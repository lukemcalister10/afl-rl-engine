# ORDER 21 — THE POOL SIT-OUT RETENTION, DERIVED ON POOL DATA

**Short answer for the owner. The pool sitter penalty has been re-derived from the pool's own
history, by the same method the national retention was derived by, with no pick axis. It replaces
the composed read entirely — `H_POOLSIT` and `H_UNION` are gone and the out-of-range national
surface is gone with them. On a staged board it is worth `+5,511` board points (`+0.74%` of the
board, `+4.5%` of the pool) across 81 named pool players, **eight of whom go DOWN** because this is a
redistribution and not a lift. Every pathway's entry-weighted mean prints `1.0000000000` exactly.
Zero national rows move — on the board, and on every year of the 24-year walk-forward. No player's
v0 moves by one float bit.**

**NOTHING IS LANDED.** `H_POOLSIT`/`H_UNION` keep their shipped defaults in the checkout; the surface
lives in a JSON artefact and a patch script, applied only inside scratchpad worktrees. The
pool-update lever lands after ORDER 22's packet. §REPRODUCE tells ORDER 22 exactly how to stand this
stage up again, byte for byte.

Pins asserted at the entry **and** the exit of every instrument, all three **UNMOVED**:

| pin | path | md5 |
|---|---|---|
| board | `data/rl_build/rl_app_data.json` | `1dbd1480a34c7823f330273211cbb76a` |
| store | `engine/rl_after/rl_model_data.json` | `d9a24282357cf3083b1640466e3ecd83` |
| instrument | `docs/evidence/composition_2026-08-10/noarb/noarb_table_338.py` | `0f8220351c64c56ccfa90c60edcdfa5f` |

Pre-registration `PREREG_ORDER21.md`, **committed at `a5732a0` before any measurement was run**.
Instruments in this directory, all re-runnable, all outputs committed:
`pool_retention_derive.py` → `POOL_RETENTION_SURFACE.json` ·
`retention_consequence.py` → `RETENTION_CONSEQUENCE.json` ·
`separation_check.py` → `SEPARATION_CHECK.json` ·
`noarb_margins.py` → `NOARB_MARGINS.json` ·
builders `build_board_o21.sh`, `emit_variant_o21.sh`, patcher `o21_patch.py`, runner `run_noarb_o21.sh`.

---

## 0. WHAT WAS REPLACED, AND BY WHAT

**Today** a pool sitter is priced `R × entry_anchor`, where `R = _R_surf(class, effpk=65, tau)` — the
**national** surface clamped at its deepest evaluated knot, because `MA.effpk` returns the constant
`POOL_PICK = 65` for every pool entrant while the surface's knots stop at pick 50 — and then
`H_POOLSIT = 0.804` and `H_UNION = 0.280` multiply the finished price on top.

**Staged**, one measured object stands in its place. Per class × depth, whole pool:

| class | today `R_natl@65` | × `H_POOLSIT` | × `H_UNION` too | **DERIVED** |
|---|---|---|---|---|
| nonKPP | 0.549 0.388 0.345 0.239 0.164 0.164 | 0.441 0.312 0.277 0.192 0.132 0.132 | 0.124 0.087 0.078 0.054 0.037 0.037 | **0.624 0.380 0.380 0.380 0.380 0.380** |
| KPP | 0.642 0.407 0.351 0.334 0.334 0.329 | 0.516 0.327 0.282 0.269 0.269 0.265 | 0.145 0.092 0.079 0.075 0.075 0.074 | **0.817 0.500 0.467 0.359 0.359 0.336** |
| RUCK | 0.781 0.594 0.594 0.594 0.541 0.470 | 0.628 0.478 0.478 0.478 0.435 0.378 | 0.176 0.134 0.134 0.134 0.122 0.106 | **1.000 0.522 0.522 0.488 0.354 0.344** |

Read the union column against the derived one: today a named-cell pool sitter at depth 1 keeps
**12.4%** of his entry price. The derived measurement says **62.4%**. That is the size of the object
being replaced.

---

## 1. THE POPULATION, DEFINED ONCE

**A cell is one (player, season) pair. A cell is a SIT-OUT iff the player has no season of `games ≥ 6`
at or before `Y`.** That is `nseas_pro(p,Y) == 0` evaluated on a completed season — **exactly the gate
`ev()` uses to send a row to `sitout_ev`**. It is **not** `_h_cut`'s test (`games this season ≤ 0`).

ORDER 19 measured that those two tests bite different populations and that the difference is
load-bearing — 26 live rows with 1–5 games in 2026 pay the R leg but not the H leg, and 6 established
rows pay H but never reach `sitout_ev`. **This act does not inherit that ambiguity: `_h_cut` retires,
so for pool rows the second population ceases to exist in the engine.** One test, one population, one
object.

**THE MID-SEASON BOUNDARY, RECONCILED RATHER THAN INHERITED.** The engine's depth clock is
`tau = max(0, Y − debutyr) + fE**1.5`. At a completed season (`fE = 1`) that is exactly `d`, so the
derivation's integer knots sit **on** the engine's own integer knots — no re-basing. Mid-season 2026
(`fE = SEASON_PROG = 0.58`) gives `tau = (d−1) + 0.4417` and the engine interpolates between the knots
either side, which is the existing D12 concave proration, untouched. `tau = 0 → R = 1.0` (no penalty
before a season starts) is preserved. **Historical cells are integer; the in-season boundary maps by
interpolation on the engine's own clock; no new convention is introduced.**

**Population size.** 4,241 pool cells harvested (draft years 2003–2024, still-listed window);
**3,334 complete-window** (`Y ≤ 2021`) with a priceable entry anchor, of which **1,325 sit-outs**
(0.3974 by count). National rows encountered and excluded at the harvest gate: 1,390.
**Non-pool cells in the fitted population: 0, asserted.**

---

## 2. THE DERIVED SURFACE

### 2a. The norm — the ND method's denominator, re-harvested on the pool

`norm(cls,d) = E[winsor(O/entry_anchor, 2.0)]` over **all** pool cells at that class and depth
(developer-inclusive). It rises with depth exactly as the national one does — deep survivors are
increasingly the developers — and dividing by it is what strips the survivor-selection common mode.

| class | d1 (n) | d2 | d3 | d4 | d5 | d6 |
|---|---|---|---|---|---|---|
| nonKPP | 0.314 (657) | 0.678 (329) | 0.811 (283) | 0.956 (226) | 1.075 (183) | 1.062 (150) |
| KPP | 0.312 (206) | 0.622 (110) | 0.759 (94) | 0.871 (72) | 1.017 (53) | 1.202 (36) |
| RUCK | 0.240 (113) | 0.762 (44) | 1.005 (42) | 1.142 (34) | 1.288 (29) | 1.197 (22) |

### 2b. The whole-pool surface, raw and after the isotonic step

`R = clip(kernel r_sit / norm, 0.05, 1.0)`, kernel Gaussian on the **depth axis only**, bandwidth
grown through `[0.75, 1.1, 1.6, 2.5]` until eff-n ≥ 35.

| class | RAW d1..d6 | **ISOTONIC (wired)** | raw violations |
|---|---|---|---|
| nonKPP | 0.624 0.380 **0.494 0.525 0.529** 0.422 | **0.624 0.380 0.380 0.380 0.380 0.380** | 3 |
| KPP | 0.817 0.500 0.467 0.359 **0.362** 0.336 | **0.817 0.500 0.467 0.359 0.359 0.336** | 1 |
| RUCK | 1.000 0.522 **0.670** 0.488 0.354 0.344 | **1.000 0.522 0.522 0.488 0.354 0.344** | 1 |

**The owner's signed law was violated by the raw data in all three classes** — a nonKPP pool sitter's
raw realisation *rises* from d2 to d5 — and the isotonic projection is what enforces it.
**Violations after projection: 0, on the three whole-pool vectors and on all 27 wired
pathway × class vectors. Verified, not asserted.**

Exact-depth sit-out cell counts, before the depth kernel:

| class | d1 | d2 | d3 | d4 | d5 | d6 |
|---|---|---|---|---|---|---|
| nonKPP | 552 | 157 | 66 | 29 | 13 | 4 |
| KPP | 187 | 72 | 40 | 17 | 7 | 3 |
| RUCK | 107 | 29 | 22 | 7 | 4 | 1 |

Bandwidth actually used, and eff-n at each cell, is printed per class in
`pool_retention_derive_out.txt` §3. **No cell fell below eff-n 35 even at d6** (the widest bandwidth
used anywhere is RUCK d6, bw 2.50, eff-n 105); no cell is DECLARED THIN.

**RUCK d1 = 1.000 sits ON the clip ceiling.** The unclipped ratio exceeds 1: a depth-1 pool ruck who
has not yet qualified realises *more* forward output than the same-depth all-pool ruck average. That
is the survivor-selection norm at its most extreme (RUCK d1 norm 0.240) and the clip is the ND
method's own `clip[.05, 1.0]`, carried. **Flagged rather than smoothed away:** it means the derived
object charges a depth-1 pool ruck nothing at all, which is a measurement and not a design choice.

### 2c. The pathway layer, and every pooled cell disclosed

**13 of 162 cells** (9 pathways × 3 classes × 6 depths) reach `n ≥ 20` and fit on their own data:

| pathway | class | d | n | own = wired |
|---|---|---|---|---|
| RD | nonKPP | 1 / 2 / 3 | 372 / 95 / 43 | 0.6540 / 0.3998 / 0.5777 |
| RD | KPP | 1 / 2 / 3 | 117 / 38 / 22 | 0.7099 / 0.3888 / 0.3855 |
| RD | RUCK | 1 | 60 | 1.0000 |
| ND>64 | nonKPP | 1 / 2 | 69 / 28 | 0.4840 / 0.2976 |
| ND>64 | KPP | 1 | 25 | 0.8888 |
| IRE | nonKPP | 1 | 32 | 0.7744 |
| UNR | RUCK | 1 | 24 | 0.4076 |
| PDA | nonKPP | 1 | 23 | 0.1938 |

**Everything else is partially pooled toward the whole-pool cell at `w = n/(n+10)`** — K = 10, the
layer-2 constant ruled at directive D4 (`K_336` `rl_model.py:396`, `K_338` `par_build.py:164`, the
engine's own within-group borrowing convention). **83 pooled cells carry `n > 0` and are printed
individually with their n, w, own estimate, donor and wired value** in
`pool_retention_derive_out.txt` §4. **66 cells carry `n = 0` and take the donor outright at `w = 0`**
— concentrated where you would expect: IRE/RUCK 5, PDS/RUCK 5, PDN/RUCK 5, SSP/KPP 5, all of MSD's
three classes 4 each.

The full wired 9 × 3 × 6 surface is in §4 of the derivation output and in
`POOL_RETENTION_SURFACE.json` under `pathway`.

**D4's renormalisation guard is discharged by construction** — see §3. Whatever the borrowed cells
deliver, the pathway's entry-weighted mean returns to exactly 1 in one multiplication.

### 2d. Reconciliation to ORDER 18, and it lands

ORDER 18 published pool-history depth-1 retention on **its** convention. Mine differs by three
declared departures — the denominator (D2: `entry_anchor`, what the engine actually multiplies, vs
`v0_start`), the norm population (pool-only) and era (D1). Running my pipeline on ORDER 18's
denominator as a sensitivity:

| class | ORDER 18 | **ORDER 21 d1 (wired, `entry_anchor`)** | ORDER 21 d1 on the `v0_start` denominator |
|---|---|---|---|
| nonKPP | 0.5725 | **0.6242** | **0.5731** |
| KPP | 0.7528 | **0.8173** | 0.6333 |
| RUCK | 0.8783 | **1.0000** | 0.9681 |

**nonKPP reconciles to ORDER 18 within 0.0006 once the denominator is matched.** That is the
strongest single control in this act: two independently written harvests, six weeks apart, agree on
the largest cell to four decimal places. KPP and RUCK do not reconcile as tightly, and the gap is the
norm population plus the pooling — declared, not argued.

**The whole of the D2 departure is visible in that table**: moving from `v0_start` to `entry_anchor`
raises depth-1 nonKPP retention from 0.573 to 0.624. `entry_anchor` is the correct denominator
because it is literally the multiplicand at both read sites; a surface derived against `v0_start` and
then multiplied onto `entry_anchor` would not be a retention of anything.

### 2e. Owner override O1 (the KPP retention floor) — printed both ways, NOT chosen

O1 is the owner's signed override on the **national** surface, board path only: KPP := pointwise
`max(KPP, nonKPP)`. Whether it extends to an object derived on pool data is an owner question and
this seat does not pre-empt it.

| | d1 | d2 | d3 | d4 | d5 | d6 |
|---|---|---|---|---|---|---|
| whole-pool KPP **as derived (wired)** | 0.8173 | 0.4996 | 0.4673 | **0.3594** | **0.3594** | **0.3363** |
| whole-pool KPP **under O1** | 0.8173 | 0.4996 | 0.4673 | **0.3799** | **0.3799** | **0.3799** |

O1 would bind at **3 of 6** depths. It is not applied in the staged configuration. This is a
DEPARTURE (D7) and it is the one open design question this act hands back.

---

## 3. THE MEAN-PRESERVING TABLE — THE OWNER'S LAW AS ARITHMETIC

`e = entry_anchor(p)` (ORDER 19's statistic, carried verbatim), over the pathway's complete-window
cells:

```
U = ( SUM_all e  −  SUM_sit e·R )  /  SUM_non e
mean = ( SUM_sit e·R + SUM_non e·U ) / SUM_all e   ==   1.0000000000   exactly
```

| pathway | cells | sitters | sit share (wtd) | **mean R (sitters)** | **uplift U (everyone else)** | **post-redistribution mean** |
|---|---|---|---|---|---|---|
| RD | 2352 | 832 | 0.3527 | 0.606216 | **1.214601** | **1.0000000000** |
| ND>64 | 441 | 193 | 0.4376 | 0.514156 | **1.378097** | **1.0000000000** |
| IRE | 137 | 70 | 0.5109 | 0.669220 | **1.345591** | **1.0000000000** |
| UNR | 126 | 65 | 0.5159 | 0.520699 | **1.510731** | **1.0000000000** |
| PDA | 106 | 53 | 0.5000 | 0.351682 | **1.648318** | **1.0000000000** |
| PDS | 62 | 36 | 0.5806 | 0.683981 | **1.437564** | **1.0000000000** |
| MSD | 40 | 34 | 0.8500 | 0.631439 | **3.088510** | **1.0000000000** |
| PDN | 36 | 29 | 0.8056 | 0.728500 | **2.124785** | **1.0000000000** |
| SSP | 34 | 13 | 0.3824 | 0.672054 | **1.203014** | **1.0000000000** |
| **ALL POOL** | **3334** | **1325** | **0.3845** | **0.591018** | **1.255520** | **1.0000000000** |

**Pathways whose post-redistribution mean is not exactly 1: 0. Asserted, and the instrument halts if
it fails.**

**THIS IS THE FULL UPDATE, NOT A SMALLER PENALTY.** Read the two middle columns together. An actual
pool sitter carries **0.5910** of his entry price — a **41% conditional markdown**, which is far
deeper than the pathway-blended figure a "one number for the pathway" treatment would produce. He
pays it because everyone else in the pathway is paid **+25.55%** to carry the risk he realised. In
MSD, where 85% of the entry weight sits out, the sitter markdown of 37% is financed by an uplift of
**3.09×** on the 15% who do not.

**Against what the engine charges today**, same cells, same weights:

| pathway | today's composed mean multiplier on sitters | derived R | delta |
|---|---|---|---|
| IRE | 0.114023 | 0.669220 | **+0.555** |
| MSD | 0.131887 | 0.631439 | **+0.500** |
| PDN | 0.407545 | 0.728500 | +0.321 |
| PDS | 0.386277 | 0.683981 | +0.298 |
| RD | 0.422175 | 0.606216 | +0.184 |
| SSP | 0.488708 | 0.672054 | +0.183 |
| ND>64 | 0.394106 | 0.514156 | +0.120 |
| UNR | 0.490032 | 0.520699 | +0.031 |
| **PDA** | **0.407689** | **0.351682** | **−0.056** |
| **ALL POOL** | 0.400936 | 0.591018 | +0.190 |

**PDA is charged MORE by the derived object than by the shipped one.** Its own depth-1 nonKPP cell
measures 0.1938 at n = 23 — the harshest fitted cell in the surface. That is the derivation
disagreeing with the shipped read in the opposite direction, and it is exactly the kind of thing a
uniform lift would have hidden.

---

## 4. THE STAGED BOARD

Five boards, all built on the **adopted** engine (main `c330169`, the par fix landed) by
`build_board_o21.sh`, all diffed against the live board `1dbd1480`.

**CONTROL 1: the HEAD-defaults build reproduces the live board BYTE-FOR-BYTE — md5
`1dbd1480a34c7823f330273211cbb76a`.** Believe nothing below until that line holds; it does.

Engine identity per build, the machine proof each patch was in the tree that built it:
BASE / VARA `a8071af4` (unpatched) · VARB `a20d7092` · DERIVEDSIT `cd2e37c0` · **DERIVED `54347ed4`**.

| | board total | change | change % | moved | up | down |
|---|---|---|---|---|---|---|
| **TODAY (shipped)** | 746,043 | — | — | — | — | — |
| VARIANT A — H lifted only | 748,355 | +2,312 | +0.310% | 48 | 48 | 0 |
| DERIVED, sit site only *(sensitivity)* | 749,028 | +2,985 | +0.400% | 66 | 58 | 8 |
| **★ STAGED — derived object, BOTH sites** | **751,554** | **+5,511** | **+0.739%** | **81** | **73** | **8** |
| VARIANT B — H lifted AND R := 1.0 | 754,501 | +8,458 | +1.134% | 73 | 73 | 0 |

The `back` board (198 delisted rows, 2,851 points) does not move under any variant —
`delisted(p)` returns before any sitter site is reached.

**Where the derived object lands between "H lifted only" and "everything lifted": at 0.521 of the
A→B interval.** It is not a compromise between them; it is a measurement that happens to sit near the
middle, and it is the only one of the three that moves rows *down*.

**ORDER 19's variants, rebuilt here on the adopted engine.** ORDER 19 published A `+2,306` / B
`+8,467` against the **superseded** board `94f1fec5`. Rebuilt on `1dbd1480`: **A `+2,312` / B
`+8,458`** — differences of `+6` (+0.26%) and `−9` (−0.11%). The par fix moved the base the sitter
legs act on by a few points; the legs themselves are unchanged code, and ORDER 19's sizing survives
the board change essentially intact.

### 4a. THE SEPARATION LAW — ASSERTED, TWICE, AT TWO DEPTHS

| check | result |
|---|---|
| ND 1-64 board rows moved, each of the four variants | **0** |
| **any** non-pool board row moved, each of the four variants | **0** |
| ND 1-64 board value | **620,877 in every variant** |
| non-pool records repriced on **any year** of the 24-year walk-forward (2,645 records) | **0** |
| records whose **v0** moved, SHIP vs STAGED | **0 — exactly zero, not merely small** |

1,054 records reprice on the walk-forward under the staged configuration and **every single one is a
pool record**. The instrument is plainly sensitive (40% of careers move) and `v0` still does not move
by one float bit — consistent with ORDER 19's three independent proofs that the sitter machinery is
applied inside `ev()` and never touches the v0 chain.

### 4b. THE MOVES, AND THE EIGHT THAT GO DOWN

| variant | n | min | p25 | median | p75 | max |
|---|---|---|---|---|---|---|
| VARIANT A | 48 | +14.89% | +16.95% | +23.92% | +26.61% | +344.23% |
| VARIANT B | 73 | +3.37% | +70.24% | +106.25% | +184.62% | +633.33% |
| **STAGED** | **81** | **−26.87%** | +10.14% | **+30.43%** | +76.67% | +533.75% |

**Eight rows move DOWN. This is the redistribution biting, and it is the thing neither ORDER 19
variant could produce:**

| player | pathway | g26 | d | TODAY | STAGED | move |
|---|---|---|---|---|---|---|
| Liam Reidy | RD | 4 | 4 | 291 | 267 | **−24** |
| Patrick Carr | UNR | 0 | 1 | 67 | 49 | **−18** |
| Oliver Francou | MSD | 4 | 1 | 375 | 358 | −17 |
| Balyn O'Brien | SSP | 4 | 1 | 300 | 285 | −15 |
| Vigo Visentini | RD | 1 | 3 | 168 | 153 | −15 |
| Jaxon Artemis | MSD | 4 | 1 | 340 | 326 | −14 |
| Jaime Uhr-Henry | UNR | 0 | 2 | 51 | 42 | −9 |
| Thomas Burton | SSP | 5 | 1 | 415 | 412 | −3 |

A row moves down when its derived retention is **below** what the composed shipped read gave it —
UNR nonKPP at depth 1 derives to 0.7010 where RD nonKPP derives to 0.6540, but Patrick Carr's shipped
composed read was 0.804 × his national-clamped R, and the derived object is harsher. **The FULL update
is not a uniform lift and the board shows it by name.**

### 4c. By pathway

| pathway | rows | moved | today | VAR A | VAR B | **STAGED** | A Δ | B Δ | **STAGED Δ** | **STAGED %** |
|---|---|---|---|---|---|---|---|---|---|---|
| RD | 66 | 18 | 45,874 | 46,148 | 47,687 | 46,300 | +274 | +1,813 | **+426** | +0.93% |
| SSP | 28 | 5 | 11,535 | 12,237 | 12,719 | 12,227 | +702 | +1,184 | **+692** | +6.00% |
| **MSD** | 63 | 26 | 36,089 | 36,962 | 39,118 | **39,327** | +873 | +3,029 | **+3,238** | **+8.97%** |
| IRE | 14 | 8 | 712 | 803 | 1,285 | 938 | +91 | +573 | **+226** | +31.74% |
| PDA | 15 | 2 | 8,103 | 8,159 | 8,444 | 8,239 | +56 | +341 | **+136** | +1.68% |
| PDN | 16 | 11 | 2,729 | 2,906 | 3,302 | **3,326** | +177 | +573 | **+597** | +21.88% |
| UNR | 13 | 7 | 1,296 | 1,376 | 1,676 | 1,372 | +80 | +380 | **+76** | +5.86% |
| ND>64 | 28 | 4 | 18,828 | 18,887 | 19,393 | 18,948 | +59 | +565 | **+120** | +0.64% |
| **ND 1-64** | **561** | **0** | **620,877** | **620,877** | **620,877** | **620,877** | **0** | **0** | **0** | **+0.000%** |

**MSD and PDN exceed variant B.** That is not an error: variant B lifts the sit-out arm to `R = 1.0`
but leaves the **year-1+** arm reading the clamped national surface. MSD and PDN carry the pool's
largest uplifts (`U` 3.09 and 2.12), and their established members sit on the year-1+ arm, so the
staged object pays them more than "no sitter charge at all" does. **PDS has zero rows on the live
board**; every PDS figure in this act is a historical-cell figure.

### 4d. The second read site, sized

| | delta |
|---|---|
| DERIVED at `sitout_ev` only | +2,985 |
| **DERIVED at both sites (staged)** | **+5,511** |
| **the `_a_blend` uplift leg alone** | **+2,526 — 45.8% of the whole staged move** |

**Nearly half of what the staged object does lives at the second read site**, on players who are not
sitters at all. ORDER 19 sized that site at +622 when it was lifted to 1.0; carrying the *uplift*
through it is worth four times as much. **20 of the 81 moved rows carry `q`** — they have a
qualifying season, take the year-1+ arm, and their move is `U`, not `R`. Mani Liddy (MSD, +655),
Robert Hansen (MSD, +427), James Blanck (MSD, +332), Flynn Young (MSD, +257) are the largest, and
**not one of them moves under either ORDER 19 variant.**

The full named ledger — every one of the 81 rows, with today / VAR A / VAR B / STAGED and its own
percentage — is in `retention_consequence_out.txt` §5 and in `RETENTION_CONSEQUENCE.json.named`.

---

## 5. BOTH COHORT INSTRUMENTS

`noarb_table_338.py` and `noarb_table_allarm.py` are the canonical files, **copied and never
modified**; `allarm` asserts `noarb_table_338.py`'s md5 `0f8220351c64c56ccfa90c60edcdfa5f` at run and
refuses to proceed otherwise. Matrices: `per_entrant_O21SHIP.json` (`a8071af4`) and
`per_entrant_O21DERIVED.json` (`54347ed4`), both on the adopted engine.
`margin vs 14% = 14% − (year-0 → year-1 appreciation)`; a negative margin is an arbitrage.

**A NOTE ON THE BASELINE, because it is the source of three of my pre-registration breaches.**
ORDER 19's readings (PRIMARY yr1 0.8850, legacy yr1 1.0884) were taken on the **superseded**
pre-par-fix engine. The par fix moved both baselines materially. Every figure below is SHIP vs STAGED
on the **same** adopted engine; ORDER 19's numbers are not comparable across that boundary.

### All-arm deciding instrument

| window | variant | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | apprec 0→1 | **margin vs 14%** | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| PRIMARY n=2212 | SHIP | 1.0000 | 0.7767 | 0.9581 | 1.0608 | 1.1231 | 1.1047 | −22.33% | **+36.33%** | no arb |
| PRIMARY | **STAGED** | 1.0000 | **0.7995** | 0.9660 | 1.0638 | 1.1275 | 1.1082 | −20.05% | **+34.05%** | **no arb** |
| MODERN n=540 | SHIP | 1.0000 | 0.8007 | 0.9084 | 0.9717 | 0.9734 | 1.0309 | −19.93% | **+33.93%** | no arb |
| MODERN | **STAGED** | 1.0000 | **0.8178** | 0.9148 | 0.9738 | 0.9783 | 1.0368 | −18.22% | **+32.22%** | **no arb** |

yr1 moves **+0.0228** (PRIMARY) and **+0.0171** (MODERN); the margin narrows by 2.28 and 1.71 points
and stays far from the bound.

**By arm, PRIMARY — year 1 is where the whole effect lives:**

| arm | n | yr1 SHIP | yr1 STAGED | move | yr4 SHIP | yr4 STAGED | move |
|---|---|---|---|---|---|---|---|
| ND | 1310 | 1.0042 | 1.0063 | +0.0021 | 1.4799 | 1.4808 | +0.0009 |
| RD | 623 | 0.3615 | 0.4247 | **+0.0632** | 0.4997 | 0.5055 | +0.0058 |
| MSD | 55 | nan | nan | — | 0.5816 | 0.6257 | +0.0441 |
| UNR | 49 | 0.2377 | 0.2561 | +0.0184 | 0.5489 | 0.5634 | +0.0145 |
| IRE | 47 | 0.1804 | 0.2585 | **+0.0781** | 0.1766 | 0.2216 | +0.0450 |
| PDA | 43 | 0.2754 | 0.2933 | +0.0179 | 0.5249 | 0.5311 | +0.0062 |
| PDN | 33 | 0.1059 | 0.1902 | **+0.0843** | 0.1814 | 0.2073 | +0.0259 |
| SSP | 31 | 0.8747 | 0.9381 | **+0.0634** | 0.8127 | 0.8203 | +0.0076 |
| PDS | 21 | 0.1644 | 0.2501 | **+0.0857** | 0.1308 | 0.1425 | +0.0117 |

The ND row's `+0.0021` is the shared strata and the one crosser, not national repricing — §4a proved
by execution that zero national records move.

### Legacy retained instrument — `noarb_table_338.py`, UNMODIFIED

Population `teaches_curve & pick 1..64 & 2004–2022`, n = 1,197. National by construction.

| group | variant | yr1 | apprec 0→1 | **margin vs 14%** | verdict |
|---|---|---|---|---|---|
| ALL picks 1-64 | SHIP / **STAGED** | 1.0730 / **1.0730** | +7.30% | **+6.70% / +6.70%** | no arb |
| picks 1-20 | SHIP / **STAGED** | 1.1218 / **1.1218** | +12.18% | **+1.82% / +1.82%** | no arb |
| picks 21-64 | SHIP / **STAGED** | 0.9994 / **0.9995** | −0.06% / −0.05% | **+14.06% / +14.05%** | no arb |

**The 1-64 aggregate is identical to the published precision on all six years.** The picks-21-64
slice moves by **+0.0001**, and `separation_check.py` names the single row responsible:
**`daniel-butler` — `pick_stored = 65`, slid to `pick = 64`, `is_pool_engine = True`.** He is a POOL
row admitted to a population selected by *stored pick number* — the crosser class ORDER 19
documented — **not a national reprice**. Every moved record carrying a 1-64 pick is that one row.

**ARBITRAGES OPENED BY THE STAGED CONFIGURATION: 0 of 5 readings.**

---

## 6. DEPARTURES FROM THE ND METHOD — DECLARED IN THE PRE-REGISTRATION, RE-STATED HERE

| # | ND method | ORDER 21 | why |
|---|---|---|---|
| **D1** | outcome era-normalised `avg × REF/era[y]` | **raw season averages** | era normalisation was RETIRED by owner ruling (`_merged_recover.py:52-57`, "*Do not reintroduce*"). Re-using it would contradict a standing ruling. |
| **D2** | denominator `V0 = v0_start(p)` | **`entry_anchor(p)`** | `entry_anchor` is literally what `R` multiplies at both pool read sites. Sensitivity printed; it moves depth-1 nonKPP 0.573 → 0.624 and is the whole gap to ORDER 18. |
| **D3** | kernel over `(log-pick, depth)`; R2 fired, so pick-conditioned | **depth axis only** | owner ruling — the pool is ONE population, rookie pick 1 and 30 are the same; and `MA.effpk` is the constant 65 for every pool row, so a pick axis is not identified in the pool at all. |
| **D4** | evaluation knots at picks 5/15/30/50 | **no pick knots; knots at depths 1..6** | consequence of D3. |
| **D5** | one surface for every draftee | **pathway layer at `n ≥ 20`, else K=10 shrinkage to the whole-pool cell** | directive D4 (ruled). 13 own-data cells, 83 pooled with `n > 0`, 66 at `n = 0`, all disclosed. |
| **D6** | no mean-preserving step | **`U` per pathway, exact to 1.0000000000** | the owner's D8 amendment; the ND surface predates it. **`U > 1` is a LIFT** — the engine's ITEM-H comment asserts "*every factor here is ≤ 1*", an invariant of ITEM H, which retires here. |
| **D7** | KPP retention floor `max(KPP, nonKPP)`, board path, owner override O1 | **not applied to the derived pool surface** | O1 is signed on the NATIONAL surface. Both readings printed (§2e); **the owner decides.** |

---

## 7. PRE-REGISTRATION: 26 PREDICTIONS, 21 HELD, 5 BREACHED

**Three of the five breaches share one root cause, and it is my error, not the data's: I anchored the
instrument bands to ORDER 19's readings, which were taken on the SUPERSEDED pre-par-fix engine — even
though the order told me in its second paragraph that the board pin had changed.** I predicted
against a baseline I had been explicitly warned was stale.

| # | quantity | predicted | measured | result |
|---|---|---|---|---|
| P1 | whole-pool R, nonKPP d1 | 0.40 – 0.75 | **0.6242** | ✓ |
| P2 | whole-pool R, KPP d1 | 0.40 – 0.85 | **0.8173** | ✓ |
| P3 | whole-pool R, RUCK d1 | 0.55 – 1.00 | **1.0000** | ✓ — *at the clip ceiling; disclosed in §2b* |
| P4 | class ordering at d1 | RUCK > KPP > nonKPP | 1.000 > 0.817 > 0.624 | ✓ |
| P5 | raw surface violates non-increasing in ≥1 cell | TRUE | nonKPP 3, KPP 1, RUCK 1 | ✓ |
| P6 | violations after isotonic, whole-pool AND pathway | ZERO | **0 of 30 vectors** | ✓ |
| P7 | d6 R below 0.45 for nonKPP and KPP | TRUE | 0.380 / 0.336 | ✓ |
| P8 | derived d1 above today's composed read, all classes | TRUE | 0.624>0.441, 0.817>0.516, 1.000>0.628 | ✓ |
| P9 | cells at `n ≥ 20` fewer than 25 of 162 | TRUE | **13** | ✓ |
| P10 | pathways with **no** cell at `n ≥ 20` | at least 5 of 9 | **4** (PDS, MSD, PDN, SSP) | **BREACH** — the pool's cells are thicker than I forecast; IRE, UNR and PDA each reach one |
| P11 | RD the only pathway with an `n ≥ 20` cell at depth ≥ 4 | TRUE | **no pathway has one** — the deepest own-data cell anywhere is d3 | **BREACH** — the prediction presupposed such a cell existed; it does not. Every depth-4+ pathway cell in the wired surface is borrowed |
| P12 | post-redistribution mean = 1.0000000000, all nine | TRUE | **1.0000000000 on all nine** | ✓ |
| P13 | MSD uplift `U` > 2.5 | TRUE | **3.088510** | ✓ |
| P14 | ALL-POOL `U` in 1.10 – 1.60 | TRUE | **1.255520** | ✓ |
| P15 | pooled sitter mean R below 0.80 | TRUE | **0.591018** | ✓ |
| P16 | ND rows moved on the staged board | EXACTLY 0 | **0** (and 0 non-pool records on the whole walk-forward) | ✓ |
| P17 | staged board change vs live | +2,000 – +12,000, positive | **+5,511** | ✓ |
| P18 | staged > variant A | TRUE | +5,511 > +2,312 | ✓ |
| P19 | staged < variant B | TRUE | +5,511 < +8,458 | ✓ |
| P20 | rows moved under staged | > 75 | **81** | ✓ |
| P21 | some pool row moves DOWN | TRUE | **8 rows, named** | ✓ |
| P22 | rebuilt variant A does NOT reproduce +2,306, within ±25% | NO / ±25% | **+2,312** (+0.26%) | ✓ *as stated, but the spirit was wrong: I expected the par fix to move it materially and it moved it by six points* |
| P23 | all-arm PRIMARY margin, staged | positive, +15% – +26% | **+34.05%**, positive | **BREACH** — outside the band. The band was anchored to ORDER 19's +25.50%, taken on the superseded engine; SHIP on the adopted engine already reads +36.33% |
| P24 | legacy 1-64 margin within 0.10 pts of +5.16% | TRUE | **+6.70%**, and SHIP is also +6.70% | **BREACH on the level** (same stale baseline) — **the intended content held exactly**: the staged configuration moves the legacy 1-64 margin by **0.00 points** |
| P25 | arbitrage opened on either instrument | NO | **0 of 5 readings** | ✓ |
| P26 | all-arm PRIMARY yr1 rises, into 0.89 – 0.97 | TRUE / band | rises **0.7767 → 0.7995**; band missed | **PARTIAL BREACH** — direction right, band wrong, same stale baseline |

---

## 8. WHAT IS UNRESOLVED, AND HANDED BACK

1. **Owner override O1 on a pool-derived object (D7).** Would bind at 3 of 6 KPP depths. Not applied.
   Both readings printed. **The owner decides.**
2. **RUCK depth-1 = 1.000 at the clip ceiling.** The unclipped ratio exceeds 1 — a depth-1 pool ruck
   who has not qualified realises *more* than the same-depth all-pool ruck average. The derived
   object therefore charges him nothing. Measurement, not design; flagged.
3. **The `_a_blend` uplift is 45.8% of the staged move** and lands on players who never sat. It
   follows from the owner's mean-preserving law applied at the site that reads the surface for
   non-sitters, and it is the largest single design consequence in this act. Stated explicitly, per
   the order, so it is a decision and not an accident.
4. **The uplift `U` is applied on entry prices the directive says are NOT yet calibrated** (D8: the
   mean-preserving principle "binds **after** the repricing in ITEM 1"). This act stages the full
   object because the order required the full update; **ORDER 22 should re-derive `U` against the
   repriced entry levels**, since `U` is a pure function of the pathway's sit share and mean `R` and
   will move when the levels move. The surface `R` itself is calibration-independent — it is a ratio.
5. **PDA is charged MORE by the derived object than by the shipped one** (−0.056). Its depth-1 nonKPP
   cell derives to 0.1938 at n = 23. Small and harsh; worth a second look before landing.

---

## 9. REPRODUCE — FOR ORDER 22, SO IT DERIVES ON THE IDENTICAL STAGE

    export PATH="/root/rl_venv312/bin:$PATH"
    SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
    cd <checkout of branch build/pool-retention>
    E=docs/evidence/pool_retention_2026-08-12

**1. The surface (~4 min).** Re-derives `POOL_RETENTION_SURFACE.json`; that file is committed, so
this is a control, not a prerequisite.

    OPENBLAS_NUM_THREADS=1 python $E/pool_retention_derive.py

Expected: `POOL_RETENTION_SURFACE.json` md5 `00ca5c3d1d4eca7e3b9a7d3ed3877d2e`.

**2. The boards (~1m20s each).**

    bash $E/build_board_o21.sh $SP/o21/board_BASE.json       nopatch
    bash $E/build_board_o21.sh $SP/o21/board_VARA.json       nopatch     RL_H_POOLSIT=1.0 RL_H_UNION=1.0
    bash $E/build_board_o21.sh $SP/o21/board_VARB.json       liftR       RL_H_POOLSIT=1.0 RL_H_UNION=1.0
    bash $E/build_board_o21.sh $SP/o21/board_DERIVEDSIT.json derived_sit RL_H_POOLSIT=1.0 RL_H_UNION=1.0
    bash $E/build_board_o21.sh $SP/o21/board_DERIVED.json    derived     RL_H_POOLSIT=1.0 RL_H_UNION=1.0

| board | md5 | engine_head |
|---|---|---|
| `board_BASE.json` | `1dbd1480a34c7823f330273211cbb76a` — **identical to the live board** | `a8071af4` |
| `board_VARA.json` | `452623adeb9aaed115d883dbe6b0239c` | `a8071af4` |
| `board_VARB.json` | `214e8f4c40280ba22e6c32652ed004d5` | `a20d7092` |
| `board_DERIVEDSIT.json` | `a4a7eef93a1cdc25de84496bc8d8afd9` | `cd2e37c0` |
| **`board_DERIVED.json`** | **`be89cbac9b0db6d70ecedc28696445ff`** | **`54347ed4`** |

**3. The two walk-forward matrices (~3m10s each).**

    bash $E/emit_variant_o21.sh SHIP    nopatch
    bash $E/emit_variant_o21.sh DERIVED derived RL_H_POOLSIT=1.0 RL_H_UNION=1.0

→ `$SP/per_entrant_O21SHIP.json` (`8d8b6894`, `engine_head a8071af4`) and
`$SP/per_entrant_O21DERIVED.json` (`bcfb737a`, **`engine_head 54347ed4`** — the machine proof the
surface was in the tree that emitted it).

**4. The instruments.**

    bash   $E/run_noarb_o21.sh
    python $E/retention_consequence.py
    python $E/separation_check.py
    python $E/noarb_margins.py

### THE STAGED CONFIGURATION, STATED EXACTLY

> **env**  `RL_H_POOLSIT=1.0  RL_H_UNION=1.0` (manifest dials, gate mode, config hash restamped,
> boot guards armed)
> **patch** `python $E/o21_patch.py <worktree> derived $E/POOL_RETENTION_SURFACE.json`

`o21_patch.py derived` does exactly three things to `engine/rl_after/_merged_recover.py` **in a
scratchpad worktree only**, applied **before** the identity restamp:

1. injects `_PR_PATH` / `_PR_WHOLE` / `_PR_U` / `_PR_U_ALL` and the two readers `_pr_R(p,tau)`,
   `_pr_U(p)` immediately after `_sitout_cls`;
2. `sitout_ev:1963` — inserts `if p.get('_pool'): R=_pr_R(p,tau)`;
3. `_a_blend:2177` — inserts `if p.get('_pool'): R=_pr_U(p)`.

Both anchors are asserted unique before insertion; the script aborts otherwise. **Modes `derived_sit`,
`liftR`, `liftRboth` and `nopatch` produce the other four builds.** The checkout's engine and
`data/rl_build/rl_app_data.json` are never written by any of it.
