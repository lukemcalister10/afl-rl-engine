# SITTER FADE PACKET 2 — ORDER 30A-2, THE RE-CUT. FOR THE OWNER'S RULING

**NOTHING WIRES UNTIL THE OWNER RULES.** No engine file, no board, no store, no curve moved in this
act. The old `los_decay` schedule is the **DECLARED FALLBACK** and stays operative. This packet is a
measurement and a recommendation; the build act (ORDER 30B) briefs separately, after the ruling.

**This packet SUPERSEDES `SITTER_FADE_PACKET.md` as the ruling basis.** It does not rewrite it.
ORDER 30A's artifacts stand untouched on their own basis, and ORDER 30A's headline row is reproduced
here from scratch, to `1.1e-16`, as a control (Q24) — so what follows sits *on top of* that act, not
in place of it.

Brief: the owner's four corrections,
[#334 comment 5290213551](https://github.com/lukemcalister10/afl-rl-engine/issues/334#issuecomment-5290213551).
Branch `land/order-29`. Pre-registration **`PREREG_30A2.md`, committed at `f29d623` BEFORE
`o30a2_recut.py` existed in runnable form** and before any cell of any of the four tasks was counted.
It has not been edited. All twenty-five predictions are scored by number in §8, breaches included.

**Read in this order:** this packet → `RECUT30A2_out.txt` (the full transcript, every cell, every n,
every dispersion) → `SITTER_DISCOUNT_TABLE_2.json` (machine-readable, including per-player rows) →
`o30a2_recut.py` (the instrument). Re-running the instrument twice produced byte-identical outputs
(`SITTER_DISCOUNT_TABLE_2.json` md5 `606b31e1`, `RECUT30A2_out.txt` md5 `0ff958d6`).

---

## 0. THE FOUR CORRECTIONS, AND WHERE EACH IS ANSWERED

| # | The owner's words | Answered in | One-line answer |
|---|---|---|---|
| 1 | *"what about a band / range of draft picks. There's nothing there at all?"* | §5 (T3) | Correct — there is nothing there. No band ordering survives in one direction across depths 2/3/4 under any guard. |
| 2 | *"it should transition to 1/2/3/4 etc in a curve, not be a hard cliff"* | §6 (T4) | The transition is now measured. It is **not** a cliff and it is **not** a smooth curve: the first game is worth +0.39 in D, and then the sequence goes *down* before it goes up. |
| 3 | *"Smillie is nearly at the end of year 2, not the start"* | §4 (T2) | Correct, and it is the single largest correction in this packet. On the continuous clock his depth is 2.92, not 2. |
| 4 | *"There is information on delistings … so you should have that data?"* | §3 (T1) | Yes — but it is a **policy reconstruction**, not an observation. It moves depth 3 from 0.214 to 0.360 and it cannot resolve depth 5 at all. |

---

## 1. THE HEADLINE, BOTH ROWS SIDE BY SIDE

`D(N)` = expected discounted delivery from the start of year N, for an entrant who has played **zero
games**, divided by the ORDER-29 landed positional entry law `nd_v0.posv` at his acquisition slot,
normalised on the depth-1 baseline `RAW(1) = 1.0286`. Fitted window: ND picks 1–64, entry years
2004–2021, n = 1,140 at depth 1.

| depth | **UNCONDITIONAL** (30A, delisting-blind = **harsh lower bound**) | n | **L-B LISTED-CONDITIONAL** (the candidate law) | n | **L-A** (own-data-extends = **generous bound**) | n | old `los_decay` (nonKPP / KPP) |
|---|---|---|---|---|---|---|---|
| 1 | 1.0000 | 1140 | 1.0000 | 1140 | 1.0000 | 1140 | 1.000 / 1.000 |
| 2 | 0.5684 | 462 | **0.5684** | 462 | 0.5684 | 462 | 0.852 / 1.000 |
| 3 | 0.2143 | 234 | **0.3600** | 100 | 0.3435 | 146 | 0.568 / 0.956 |
| 4 | 0.1052 | 154 | *0.3073* (bound only) | **11** | *0.4630* (bound only) | 35 | 0.307 / 0.716 |
| 5 | 0.0742 | 130 | **UNRESOLVED** (n=2) | 2 | *1.0723* — leak, see §3.4 | 9 | 0.136 / 0.428 |
| 6 | 0.0905 | 117 | **UNRESOLVED** (n=1) | 1 | *2.6472* — leak | 4 | 0.050 / 0.209 |

**Dispersion, never a bare mean.** Depth 3, L-B: median 0.0013, p25 0.0000, p75 0.1314, 33 of 100
rows at exactly zero, mean tail share 0.10. Depth 2 (all readings): median 0.0028, p25 0.0000,
p75 0.3042, 121 zeros of 462. The distribution is a **spike at zero plus a long right tail** at every
depth; the mean is the right statistic for a *price*, and the median is not — but the owner should
see that the median sitter delivers essentially nothing, at every depth, on every reading.

**Three facts the owner needs in the same breath as that table:**

1. **Depth 2 does not move — at all.** `D_listed(2) = D_uncond(2)` to `0.00e+00`. Every ND pick
   carries a #338 minimum tenure of at least 2 years, so the reconstruction lists *every* depth-2
   sitter and the depth-1 baseline alike. This is a statement about **the resolution of the source**,
   not evidence that delisting does not matter at depth 2. (Prereg Q1, held exactly.)
2. **Depth 3 is where the correction lives, and it is large.** 0.214 → **0.360**, +0.146. The two
   listing readings agree there to 0.017, so a single number is defensible.
3. **Depth 4 and deeper, the listed population essentially ceases to exist.** Eleven rows. Seven of
   them are still-active players, four are carried by the tenure band alone. L-A and L-B disagree by
   0.156 — over the prereg's own 0.15 threshold — so **§6 of the prereg fires and depth 4 is
   published as a BOUND [0.307, 0.463], not a law.** Depths 5 and 6 do not resolve at all.

---

## 2. THE SHORT VERSION OF THE RECOMMENDATION

The seat recommends, for the owner's ruling:

- **Wire the L-B listed-conditional row at depths 2 and 3 only** — 0.568 and 0.360 — **position-blind
  and band-blind**, on the **continuous season-fraction clock**.
- **Depth 4: rule a point value or rule the bound.** The measurement gives [0.307, 0.463] on n = 11.
  If the owner wants one number, take L-B 0.307 and accept that it rests on eleven rows.
- **Depth 5+: UNRESOLVED. The old `los_decay` stays the fallback there**, or the law is held flat at
  the depth-4 value — an owner ruling, not a measurement.
- **Do not wire any pick-band or position gradient.** §5.
- **Wire the games transition from the depth-2 cumulative points only**, and rule the 0→1 boundary
  as a design choice; the bucketed measurement does not produce a monotone curve. §6.
- **Nothing wires until that ruling.** The old `los_decay` schedule is the declared fallback.

Reasons, at length, in §7.

---

## 3. T1 — LISTED-CONDITIONING

### 3.1 The source, named on its face

The owner is right that the data exists. **It is not an observation table.** It is the
**#338 MINIMUM LISTING TENURE rule** — the owner's own word *"Fire 338"*, 2026-08-06 — implemented at
`engine/rl_after/s4_matrix_M1v7.py:53-70,81,113` (commit `30996f8`) and ported verbatim into the
no-arb lane's emitter at `docs/evidence/noarb_338_2026-08-06/emit_matrix_338.py:127-160`. The prereg
named it in §1 before it was used, and this act follows what it filed.

```
min_tenure(p)      = 4 if ND pick 1-20 ; 3 if ND pick 21-40 ; 2 otherwise
debut_year(p)      = entry_year + 1  (every route except MSD)
listed_through(p)  = _last_listed                                    if explicitly recorded
                   = None (STILL LISTED)                             if not retired
                   = max(debut + min_tenure - 1, last_scoring_year)  otherwise  ("own data extends")
```

**Explicit `_last_listed` is present on 2 of the 1,140 fitted ND rows.** That is the whole of the
player-specific delisting observation in this population. Everything else is either *"he is still on
a list today"* (observed) or *the tenure band* (a rule keyed on pick, carrying no player-specific
delisting information whatsoever). The packet states this per cell rather than presenting a band rule
as a listing measurement.

### 3.2 Two readings, both published

- **L-A — the reconstruction as filed**, own-data-extends included. This is what the #338 lane emits.
- **L-B — the outcome-blind floor**: `listed at N iff (min_tenure >= N) or (not retired)`.

**Why both.** *Own data extends* infers listing **from delivery**: past the band floor, the only
retired rows L-A admits are rows that played. At depths where the floor has expired, L-A's
conditioning is therefore **selection on the outcome** — and it shows: `D_LA(5) = 1.072` and
`D_LA(6) = 2.647`, i.e. L-A prices a five-year gameless sitter *above a fresh entrant*. That is the
defect, visible in the number. L-B is free of that leak but confounds listing with pick band. The
truth sits between them, and this act publishes both rather than picking silently.

### 3.3 Listing-resolution coverage, per cell

How the listing status of the rows **inside** each L-B cell is actually known:

| depth | n (L-B) | observed listing (still active, or explicit `_last_listed`) | carried by the **tenure band alone** |
|---|---|---|---|
| 1 | 1140 | 341 (29.9 %) | 799 (70.1 %) |
| 2 | 462 | 88 (19.0 %) | 374 (81.0 %) |
| 3 | 100 | 23 (23.0 %) | 77 (77.0 %) |
| 4 | 11 | 7 (63.6 %) | 4 (36.4 %) |
| 5 | 2 | 2 (100 %) | 0 |
| 6 | 1 | 1 (100 %) | 0 |

Read that honestly: **at depth 3, 77 % of the "still listed" rows are listed because a band rule says
so.** The depth-3 number is a good number, but it is a number about a policy reconstruction.

**Floor expiry** (arithmetic on the rule, prestated): the band floor covers depth ≤ 4 for picks 1–20,
≤ 3 for 21–40, ≤ 2 for 41–64. At depth ≥ 5 **no** ND pick is carried by the floor, so an L-B listed
cell at depth 5+ can contain only still-active entrants — which is why it collapses to n = 2 and n = 1
and is reported **UNRESOLVED**, never approximated. (Prereg Q5, held.)

### 3.4 The sources cross-checked, disagreements reported not resolved

The rule was **re-derived here from Layer 1** (`ad1229ea`, byte-pinned) and checked key by key against
the #338 lane's own emitted `per_entrant_338_confirmation.json`:

- 1,137 of 1,140 fitted ND rows matched; **1,130 agree = 99.4 %** (prereg Q7 threshold 95 %, held).
- **All 7 disagreements have a single cause: the retired predicate.** The #338 lane's window uses its
  own `retired_now(p)` (*delisted, or drafted ≤2021 with last game ≤2024*); this act uses Layer 1's
  `retired`, which is the store's `_retired`. Those are **different predicates**, they disagree on
  `toby-conway`, `judson-clarke`, `finlay-macrae`, `max-king-stk`, `sam-sturt`, `paddy-dow`,
  `elliot-himmelberg` — seven players this act treats as still listed and that lane treats as
  finished in 2024. **The disagreement is reported, not resolved by preference.**
- Live store `cb38ef11` vs Layer 1 `ad1229ea`: `_retired` differs on **0** rows, `_last_listed` on
  **0** rows. The store move did not touch the listing facts.
- 4 rows sit in a different tenure band under the attribution pick than under `effective_pick`; the
  #338 rule bands on `effective_pick` and so does this act, as filed.

---

## 4. T2 — THE CONTINUOUS DEPTH CLOCK. **THE OWNER'S DECISION SURFACE.**

### 4.1 The clock, as prestated

`c = N + φ`, `N = 2026 − entry_year`, and `φ` is the fraction of the current season elapsed, taken
from **`data/season_state.json`** — the AUTHORITATIVE DYNAMIC SEASON STATE the engine itself reads:
`season_year 2026`, `as_of_round 22` of `24`, **`calendar_progress 0.92`**. Two home-and-away rounds
remain as of 2026-08-14. `exposure_pace` (0.818) is the empirical durable-sample pace and is
explicitly **not** the calendar clock; it is not used.

**Interpolation, prestated:** log-linear in D — `D(c) = D(N)^(1−φ) · D(N+1)^φ`. The discount is a
multiplicative survival-style object (the shipped `los_decay` is itself an exponential); log-linear is
positive everywhere, monotone whenever the table is, and reduces to the table exactly at φ = 0 and 1.
Linear-in-D is published beside it: the two differ by at most **0.021** in D on any named row, so the
convention is disclosed but **not decisive** (Q11, held).

**Where the next integer depth does not resolve, the law is HELD FLAT and the row is FLAGGED as
extrapolated** — never quoted silently.

### 4.2 The named rows at TRUE current depth

Every price below is `29B flat v0 × D`. **Nothing is wired; this is arithmetic on a packet.**

| player | pos | pick | entry | **true depth c** | 29B flat v0 | old `los_decay` (integer) | 30A integer D | **continuous UNCONDITIONAL** | **continuous L-B (candidate)** | continuous L-A (generous) |
|---|---|---|---|---|---|---|---|---|---|---|
| `josh-smillie` | MID | 7 | 2024 | **2.92** | 1617 | 0.852 → **1378** | 0.5684 → **919** | 0.2317 → **375** | **0.3734 → 604** | 0.3576 → 578 |
| `harry-demattia` | MID | 25 | 2023 | **3.92** | 892 | 0.568 → **507** | 0.2143 → **191** | 0.1114 → **99** | **0.3112 → 278** | 0.4521 → 403 |
| `max-knobel` | RUCK | 42 | 2022 | **4.92** | 834 | 0.716 → **597** | 0.1052 → **88** | 0.0763 → **64** | **0.3073 → 256 \*** | 1.0026 → 836 \*\* |

\* **EXTRAPOLATED** — held flat at the deepest resolved L-B depth (4), because depth 5 does not
resolve (Q10, held). \*\* L-A's depth-5 value is the outcome-selection leak of §3.2; it is printed to
show the leak, and the seat does **not** offer it as a price.

### 4.3 What this table says, plainly

- **The clock correction is bigger than the entire listing correction on `josh-smillie`.** Being
  0.92 of the way through year 2 puts him essentially at the year-3 discount. On the unconditional
  table alone it takes him from 919 to **375** (Q8, held).
- **The two corrections oppose each other, and the clock wins.** Listing-conditioning raises the
  price; the clock lowers it. Net, `smillie` lands at **604** — **below** ORDER 30A's integer print of
  919, and well below the old schedule's 1378 (Q9, held).
- **On the deeper rows, listing wins.** `demattia` 191 → 278 and `knobel` 88 → 256: the listed
  conditioning more than offsets the clock, because the unconditional deep cells were dominated by
  players who were almost certainly no longer on any list.
- The old schedule evaluated at the same continuous depth would give 0.592 / 0.325 / 0.450 — printed
  in the transcript for symmetry. It is not a recommendation; it is the fallback.

### 4.4 What the clock conflates — disclosed, not claimed away

`D(N)` is the price at the **start** of year N. Moving from N to N+1 carries **two things at once**:
a year of time-value, and the information gained by watching another full season pass gameless. The
measurement is on integer seasons and **cannot separate them at sub-season resolution.** Both push the
same way, so the interpolated value is defensible **as a price**. It is not a decomposition, and this
act does not claim it is one.

---

## 5. T3 — BANDS, A2-GUARDED. **VERDICT: NO WIREABLE GRADIENT.**

### 5.1 The guard

Anomaly A2: the landed positional entry law `nd_v0.posv` is floored at zero in the thinnest part of
its own deep tail — the ORDER-29 artifact declares this about itself
(`pvc_curve_v2.json::nd_v0.ruck_floor_63_64`). A near-zero denominator inflates any ratio taken
against it.

**GUARD G1 (primary, prestated):** exclude and count every row whose acquisition cell has
`posv[g][p] < 0.20 × curve[p]`. It selects exactly four cells — **RUCK 62, RUCK 63, RUCK 64, SF 64** —
and the absolute alternative the brief offered (`posv < 40` board points) selects the **identical
four**. The floor choice is therefore **not load-bearing**, and that was verified on the denominator
alone before the prereg was filed.

**G1 excludes 5 fitted rows** — `daniel-butler` (SF 64), `ben-crocker`, `rhys-o-keeffe` (SF 64),
`luke-lowden`, `chris-bryan` (RUCK 62) — on top of the two `v0 == 0` rows ORDER 30A had already
dropped. (Q12, held.)

**GUARD G2 (stricter sensitivity):** `pick ≥ 58 AND posv < 0.50 × curve[p]` — nine cells, 19 fitted
rows.

### 5.2 The bands, re-cut

Depth 2, 3-band, **G1**, unconditional (`D_shrunk`, K = 15):

| depth | band | n | mean | median | p25 | p75 | D_raw | D_shrunk | borrow |
|---|---|---|---|---|---|---|---|---|---|
| 2 | 1–20 | 61 | 0.6944 | 0.2306 | 0.0053 | 1.0198 | 0.6786 | **0.6535** | 19.7 % |
| 2 | 21–40 | 152 | 0.4368 | 0.0077 | 0.0000 | 0.3211 | 0.4268 | **0.4380** | 9.0 % |
| 2 | 41–64 | 246 | 0.6106 | 0.0001 | 0.0000 | 0.1054 | 0.5968 | **0.5942** | 5.7 % |
| 3 | 1–20 | 20 | 0.2411 | 0.0057 | 0.0001 | 0.1519 | 0.2356 | 0.2080 | 42.9 % |
| 3 | 21–40 | 67 | 0.1315 | 0.0000 | 0.0000 | 0.0329 | 0.1285 | 0.1363 | 18.3 % |
| 3 | 41–64 | 144 | 0.1863 | 0.0000 | 0.0000 | 0.0184 | 0.1820 | 0.1810 | 9.4 % |
| 4 | 1–20 | **4** | 0.0129 | 0.0028 | 0.0000 | 0.0157 | 0.0126 | 0.0795 | **78.9 %** |
| 4 | 21–40 | 40 | 0.0108 | 0.0000 | 0.0000 | 0.0000 | 0.0105 | 0.0342 | 27.3 % |
| 4 | 41–64 | 109 | 0.1354 | 0.0000 | 0.0000 | 0.0000 | 0.1323 | 0.1281 | 12.1 % |

The full 2-band, 3-band × G0/G1/G2 × unconditional/L-B grid — 8 lenses, every cell with n, mean,
median, p25, p75, D_raw, D_shrunk and borrow % — is in `RECUT30A2_out.txt` §T3 and in the JSON under
`T3.cells`.

### 5.3 The verdict, mechanically evaluated

Direction of the band ordering at depths 2 / 3 / 4, on `D_shrunk`:

| lens | guard | listing | depth 2 | depth 3 | depth 4 | one direction throughout? |
|---|---|---|---|---|---|---|
| 3-band | G0 | uncond | non-monotone | non-monotone | non-monotone | NO |
| 3-band | G1 | uncond | non-monotone | non-monotone | non-monotone | NO |
| 3-band | G2 | uncond | non-monotone | non-monotone | non-monotone | NO |
| 3-band | G1 | L-B | non-monotone | non-monotone | increasing | NO |
| 2-band | G0 | uncond | decreasing | decreasing | increasing | NO |
| 2-band | G1 | uncond | decreasing | decreasing | increasing | NO |
| 2-band | G2 | uncond | decreasing | decreasing | increasing | NO |
| 2-band | G1 | L-B | decreasing | increasing | increasing | NO |

> **VERDICT: NO WIREABLE BAND GRADIENT.** No band ordering holds in the same direction at all three
> depths under any guard, under either band cut, under either listing reading.

**And the guard is not what is stopping it.** The A2 tail sits only in the 41–64 band's denominator.
The actual source of the non-monotonicity is the **21–40 dip** — the middle band is the *lowest* of
the three at depth 2 (0.438 vs 0.654 and 0.594), and no denominator guard can touch that (Q13, held).
The 2-band contrast at depth 2 is 0.121 — smaller than 0.20 — and the 1–20 cell borrows 19.7 % of its
value from the all-pick row through K-shrinkage (Q14, held). By depth 4 the 1–20 cell is **four rows
borrowing 79 %**. There is no signal to wire.

**So the answer to the owner's question is: no, there is nothing there at all — and it is not the
broken tail's fault.**

### 5.4 The owner's proposed pick-64 floor — referenced, NOT applied

The owner has proposed (**not yet firmly ruled**) a floor of **100** on positional v0 at pick 64, to
be confirmed with the fade ruling. **Nothing in this act applies it.** G1 and G2 are the prestated
guards and are what every number above uses. For reference only: at pick 64 the cells currently below
100 are **MID 64, RUCK 64, SF 64**. A floor of 100 there would be a *strictly larger* intervention
than G1 (which reaches MID 64 not at all), so if the owner rules the floor, the band cells at depth
2–4 will need one re-read — the seat expects it to change nothing about the verdict, because the
verdict is driven by the 21–40 dip and not by the tail.

**Sensitivity disclosure, a prereg breach owned:** G2 moves the depth-4 41–64 cell by **0.079** vs G1,
over the 0.05 the prereg predicted (Q16, breached). The guard choice *is* mildly load-bearing in the
deepest, thinnest band cell — which is one more reason the seat recommends wiring no band at all.

---

## 6. T4 — THE GAMES TRANSITION. **NEITHER A CLIFF NOR A CURVE.**

### 6.1 How a partial career is decomposed

ORDER 30A needed no decomposition: a sitter delivered nothing before depth N, so his whole career
score *is* his from-depth-N score. A player with 1–10 games has not, so the pre-depth-N seasons must
come out. The DV lane's own config grants the licence — `LAYER2.json::cfg.gamma_note`: *"GAMMA==1.0
makes val(r)=SCALE*r LINEAR, so delivered value is ADDITIVE across seasons … a career is a straight
sum."*

```
V_from_N(i) = ( grace_a[i].obs × s_N(i)  +  grace_a[i].tail ) × DF_i(N−1)
s_N(i)      = Σ_{k ≥ N} pts_k(i)  ÷  Σ_all pts_k(i)
```

**Only the SHARE comes from the live-store recompute; the LEVEL stays the pinned DV number.** Two
controls, both prestated and both held:

- **Q17 — the share reconstruction validates.** Live-store recomputed `obs` ÷ pinned DV
  `grace_a.obs`: median **0.9340**, IQR width **0.0000**, and the **full spread across all 1,019 rows
  is 1.1e-15**. The ratio is a *constant*. Every season leg moved by the same factor, so the store
  move `d9a24282 → cb38ef11` is a pure `MA.SCALE` rescale with the bars and the scorer unchanged — and
  a share is exactly invariant to it. This is the cleanest possible justification for taking the share.
- **Q18 — the 0-game reduction is exact.** On every 0-game row `s_N = 1.0` to `1e-12` (0 exceptions
  across all five depths), and the T4 machinery reproduces ORDER 30A's `D(N)` to **1.1e-16**. Asserted
  in the harness, not assumed.

### 6.2 The transition at depth 2 (games in the debut season), L-B listed-conditioned

| games by depth 2 | n | n=0 | mean | median | p25 | p75 | **D(k, 2)** | tail share |
|---|---|---|---|---|---|---|---|---|
| **0** | 462 | 121 | 0.5846 | 0.0028 | 0.0000 | 0.3042 | **0.5684** | 0.081 |
| **1–2** | 133 | 11 | 0.9877 | 0.1208 | 0.0013 | 1.0230 | **0.9602** | 0.116 |
| **3–5** | 145 | 5 | 0.8722 | 0.2827 | 0.0069 | 1.0671 | **0.8479** | 0.119 |
| **6–10** | 161 | 5 | 1.4619 | 0.6035 | 0.0258 | 2.0245 | **1.4213** | 0.112 |
| 11+ | 239 | 0 | 1.6707 | 1.0206 | 0.1729 | 2.5720 | 1.6242 | 0.108 |

*(At depth 2 the listed-conditional and unconditional rows are identical — §3.1, Q1.)*

**The steps:** 0 → 1-2 **+0.392** · 1-2 → 3-5 **−0.112** · 3-5 → 6-10 **+0.573** · 6-10 → 11+ +0.203.

### 6.3 What that measurement actually says — and what it does not

1. **The first game is worth a great deal.** +0.392 in D, a 69 % jump, and 46 % of the whole 0 → 6-10
   range in one step. The owner's instinct that zero games is being penalised hard is **confirmed** —
   but the measurement says the penalty *is* real, not that it is an artefact.
2. **The sequence is NOT monotone.** 3–5 games prices *below* 1–2 games. (Q20, breached — I predicted
   monotone.) With n = 133 and 145 those cells are not thin; the dip is what the data says.
3. **The 0 → 1 step is not the largest step.** 3–5 → 6–10 is bigger (+0.573). (Q21, breached — I
   predicted the first game would dominate.) But the *conclusion* the prereg drew from Q21 survives on
   different evidence: **the measurement does not produce a smooth curve.** It produces a big step, a
   dip, and a bigger step.
4. **D crosses 1.0.** A debut-season player with 6–10 games prices at **1.42** — *above* a fresh
   entrant on this normalisation. Any games schedule wired from these points must therefore be a
   multiplier that is **allowed to exceed 1**, or the fade must be applied only in the ≤5-games region.
   This is a real design constraint on 30B and the seat flags it now.
5. **Dispersion is not the 30A shape.** p25 is 0.0000 only in the 0-games cell; it is 0.0013 at 1–2
   and 0.0069 at 3–5 (Q23, breached). median/mean stays far below 0.60 in every cell (0.005 / 0.122 /
   0.324), so the spike-plus-tail shape holds — but the zero spike thins out the moment a player has
   played at all.

### 6.4 The cumulative reading — **this one is well-behaved, and it is what the seat would wire**

The brief phrased the estimand as *"≤ k games by depth N"*. Published beside the prereg's buckets:

| depth | ≤ games | n | mean | **D** |
|---|---|---|---|---|
| 2 | ≤ 0 | 462 | 0.5846 | **0.5684** |
| 2 | ≤ 2 | 595 | 0.6747 | **0.6560** |
| 2 | ≤ 5 | 740 | 0.7134 | **0.6936** |
| 2 | ≤ 10 | 901 | 0.8472 | **0.8236** |
| 3 | ≤ 0 | 100 | 0.3703 | **0.3600** |
| 3 | ≤ 2 | 164 | 0.6103 | **0.5933** |
| 3 | ≤ 5 | 234 | 0.7002 | **0.6807** |
| 3 | ≤ 10 | 331 | 0.7128 | **0.6930** |

**The cumulative reading is monotone increasing at both depths.** It is the same evidence, pooled so
the bucket noise cancels, and it is the object the owner's "no hard cliff" ruling can actually be
built on.

### 6.5 Depth 3 and 4

Depth 3, L-B: `0` 0.3600 (n=100) · `1-2` 0.9578 (n=64) · `3-5` 0.8857 (n=70) · `6-10` 0.7226 (n=97).
Depth 4, L-B: `0` 0.3073 (n=11) · `1-2` 0.8404 (n=12) · `3-5` 2.4981 (n=17, outlier-driven) ·
`6-10` 0.8931 (n=41, mean tail share **0.375** — approaching 30A's CENSOR-3 unusability flag).

**No depth-3 games cell fell below n = 10** — the samples are much richer than the prereg expected
(Q22, breached in the generous direction). The depth-4 cells are thin and one of them (3–5) is driven
by a right-tail outlier; the seat does **not** recommend wiring anything from depth 4.

---

## 7. THE SEAT'S RECOMMENDATION, WITH REASONS

### 7.1 What to wire (after the ruling — **nothing wires now**)

| element | recommendation | reason |
|---|---|---|
| **The row** | **L-B listed-conditional** at depths 2–3: **0.5684 / 0.3600** | It is the only reading that conditions on listing *without* inferring listing from delivery. L-A's leak is visible in its own numbers (D=1.07 at depth 5). The unconditional row is a genuine harsh bound and stays published. |
| **Depth 4** | **A BOUND [0.307, 0.463]**, not a law. If a point is forced: 0.307. | The prereg's own falsification clause (§6) fired: L-A and L-B disagree by 0.156, over the 0.15 threshold. n = 11. |
| **Depth 5+** | **UNRESOLVED.** Old `los_decay` fallback, or held flat at depth 4 — an owner ruling. | The tenure floor carries no ND pick past depth 4, so the listed cell is 2 rows and 1 row. Approximating it would be inventing evidence. |
| **The clock** | **Continuous, log-linear, `φ = calendar_progress`** off `data/season_state.json` | The owner's correction 3 is right and it is the largest single effect in this packet. The convention is disclosed and costs ≤0.021 in D against linear-in-D, so it is not load-bearing. |
| **Bands** | **Wire none.** Position-blind and band-blind. | §5.3: no ordering survives across depths under any guard. The 21–40 dip, not the A2 tail, is what breaks it. |
| **Position** | **Wire none.** | ORDER 30A already showed the position lens carries the A2 artefact at depth (RUCK D_raw 1.20 at depth 5). Nothing in this re-cut rehabilitates it. |
| **Games** | **The depth-2 CUMULATIVE points** 0.568 / 0.656 / 0.694 / 0.824, with the 0→1 boundary an **owner-ruled shape**. | The bucketed transition is not monotone (§6.3); the cumulative one is. The measurement cannot adjudicate the shape of the very first step, and the seat will not pretend it can. |

### 7.2 The three things the seat wants on the record

1. **The listing correction is real but small in reach.** It moves exactly one depth that matters
   (3: 0.214 → 0.360). It cannot move depth 2 at all, and it destroys the sample at depth 4+. The
   owner asked whether we had the delisting data; the honest answer is *we have a policy rule that
   stands in for it, and it resolves two of the five depths we care about.*
2. **The clock correction is the one that changes the board.** `smillie` 919 → 604 even *after*
   listing-conditioning raises him. If only one of the four corrections is ruled in, it should be
   this one.
3. **The owner's "curve not cliff" is a DESIGN CHOICE imposed on the measurement, not a shape the
   measurement produces.** The seat said in the prereg it would say this in those words if the
   measurement showed a step, and it does — a +0.39 step at the first game, followed by a *dip*. The
   prediction that the first step would be the *largest* was wrong (Q21, breached) and the seat owns
   that; the conclusion it was drawn to support stands on the non-monotonicity instead. Ruling a
   smooth blend is defensible as **policy**. It is not what the evidence says.

### 7.3 What is NOT being claimed

- No claim that D_listed is the "true" delisting-conditional price. It is conditional on a **band
  rule** for 77 % of its depth-3 rows.
- No claim that the continuous clock decomposes time-value from information (§4.4).
- No claim about pool routes. This act is ND 1–64 only.
- No claim that anything here is wired. **Nothing wires until the owner rules. The old `los_decay`
  schedule is the DECLARED FALLBACK and remains operative.**

---

## 8. THE PREREG, SCORED — 17 HELD, 7 BREACHED, 1 SELF-REFERENTIAL

Every prediction is owned by its number. None was dropped, none was edited.

| # | verdict | what happened |
|---|---|---|
| Q1 | **HELD** | `D_listed(2) = D_uncond(2)` to `0.00e+00` under both readings. |
| Q2 | **HELD** | `D_LB(3) − D_unc(3) = +0.1456` ≥ 0.05. |
| Q3 | **HELD** | L-B stays monotone decreasing: 0.5684 / 0.3600 / 0.3073. |
| Q4 | **HELD** | `D_LA(4) − D_LB(4) = +0.1557` > 0.10 — the outcome-selection leak, in the predicted direction. |
| Q5 | **HELD** | L-B depth 5 n = 2, depth 6 n = 1; both reported UNRESOLVED. (Predicted n = 0; 2 and 1 still-active rows exist.) |
| Q6 | **BREACHED** | `n_LB(3) = 100` ✔ in [90,180]; **`n_LB(4) = 11`, far below the predicted [20,70]**. I underestimated how completely the tenure floor expires at depth 4. |
| Q7 | **HELD** | 99.4 % agreement with the #338 lane's own `max(yrs)`; all 7 disagreements attributable to the differing retired predicate, not a port error. |
| Q8 | **HELD** | `smillie` continuous unconditional = **375** < 500. |
| Q9 | **HELD** | `smillie` continuous L-B = **604** < 919; the clock beats the listing correction on that row. |
| Q10 | **HELD** | `knobel` at c = 4.92 is flagged EXTRAPOLATED (deepest resolved L-B depth = 4). |
| Q11 | **HELD** | max \|log-linear − linear\| = 0.0209 < 0.06. |
| Q12 | **HELD** | G1 excludes 5 fitted rows, inside [5,25]. |
| Q13 | **HELD** | Depth-2 3-band after G1 still non-monotone, 21–40 still lowest (0.6535 / 0.4380 / 0.5942). |
| Q14 | **HELD** | 2-band contrast 0.1209 < 0.20; 1–20 borrow 19.7 % > 15 %. |
| Q15 | **HELD** | **NO WIREABLE BAND GRADIENT** — no direction survives all three depths under any lens. |
| Q16 | **BREACHED** | G2 moves the depth-4 41–64 3-band cell by **0.0793** > 0.05. The guard choice is mildly load-bearing in the deepest, thinnest band cell. Disclosed in §5.4. |
| Q17 | **HELD** | median 0.9340 ∈ [0.90,0.97]; IQR width 0.0000 — in fact a **constant** to 1.1e-15. |
| Q18 | **HELD** | 0-game reduction exact: 0 rows with `s_N ≠ 1`; max \|T4 − 30A\| = 1.1e-16. |
| Q19 | **BREACHED** | `D(1-2,2) = 0.9602`, above the predicted [0.60,0.95] band. The direction claim (> 0.568) held; the ceiling did not. |
| Q20 | **BREACHED** | Not monotone: 0.5684 < 0.9602 **> 0.8479** < 1.4213. |
| Q21 | **BREACHED** | The 0 → 1-2 step (+0.392) is **not** the largest; 3-5 → 6-10 (+0.573) is. The prereg's conclusion — *the measurement will not support a smooth curve* — survives via the non-monotonicity instead, and §7.2(3) says so in the words the prereg promised. |
| Q22 | **BREACHED** | Breached in the generous direction: `n(6-10, depth 3) = 97` (predicted < 30) and **no** depth-3 games cell fell below n = 10, so nothing needed collapsing. |
| Q23 | **BREACHED** | p25 = 0 only in the 0-games cell; it is 0.0013 at 1–2 and 0.0069 at 3–5. median/mean < 0.60 held everywhere (0.005 / 0.122 / 0.324). |
| Q24 | **HELD** | ORDER 30A reproduced from scratch: RAW(1) 1.028605 vs 1.0286; D 0.5684 / 0.2143 / 0.1052 / 0.0742 / 0.0905. |
| Q25 | **HELD, WITH ONE AMENDMENT** | The seat does recommend the L-B listed row on a continuous log-linear clock, band-blind and position-blind, with L-A as the generous bound and the unconditional row as the harsh bound, and the games transition from depth 2 only with an owner-ruled 0→1 shape — **but** the prereg did not anticipate that depth 4 would fail its own §6 threshold and have to be published as a bound rather than a law, nor that the *cumulative* games reading would be the well-behaved one. Both amendments are stated in §7.1. |

**Breach summary in one line:** the seat was right about listing, the clock and the bands, and wrong
about the shape and the sample sizes of the games transition — it predicted a monotone curve with a
dominant first step and thin deep cells, and got a non-monotone sequence with a large-but-not-largest
first step and cells three times richer than expected.

---

## 9. WHAT WOULD CHANGE THIS RULING

- **A real delisting table.** Two explicit `_last_listed` rows in 1,140 is what this act has. Any
  actual list-membership history would replace §3's reconstruction outright and would be the single
  biggest improvement available.
- **A ruling on the pick-64 v0 floor of 100** (§5.4) — referenced here, not applied. The seat expects
  it not to change the band verdict, and will re-read the band cells once if it is ruled.
- **The retired predicate.** Seven rows turn on whether *"drafted ≤2021, last game ≤2024"* means
  retired. If the owner rules that predicate one way, both this act and the #338 lane should use it.
- **Deeper depths.** Depth 5+ will not resolve on this source no matter how the estimator is cut. It
  needs either the delisting table or an owner ruling that the law is held flat.

---

*ORDER 30A-2, the measurement seat. `land/order-29`. READ-ONLY: no engine file, no board, no store,
no curve was touched. **NOTHING WIRES UNTIL THE OWNER RULES — the old `los_decay` schedule is the
DECLARED FALLBACK and remains operative.***
