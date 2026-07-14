# THE MOVEMENT-MACHINE ATTRIBUTION CENSUS
**supervisor seat 6 · 2026-07-14 · READ-ONLY, Tier 3 · candidate (no bake, no tag, no merge)**

Measured on the live pinned env — **engine `2030e5df`, store `340a7a32` → board `3dc19fbb`**, config `69ead79b944d`,
N = 804. Board `3dc19fbb` is byte-identical to the tagged board-of-record **`81e48293`** *except bramble (+1 SCAR)*
(item-20 store-identity job; `ev()`/config/band/rl_model unchanged). Every figure below carries **board md5 `3dc19fbb`**.
SCAR is reported in the **numéraire** (`ev ÷ F`, `F = 1.0524`, pick-1 = 3000) to match the shipped board.

**Method (G-ATTR, path-additive).** Each player's shipped *level* is decomposed leg-by-leg inside `_coreM1`/`_inferM1`:

```
Lo (pre-machine, _lvl_eff_orig)  →  + up-branch credit  →  − down-branch raw penalty
   →  − _agemult2 amplification  →  − _eo drag  →  shipped level  →  shipped value
```

Each leg is priced through the **convex price** by overriding `cp._lvl_eff` to the cumulative level at that step and
re-running `ev()` — everything downstream (bands, q97 tail, caps, floor) reflects the level. Legs are consecutive
value differences, so they **sum exactly to the machine's total effect** (verified: `max|Σlegs − total| = 0.0000`).
`residual` = the M3 in-progress-season value-blend (the one piece not expressible as a single level); it is 0 for all
completed-season / on-pace players and nonzero only for mid-season thin players. Pricing verified monotone and
state-clean (native reproduced at the shipped level for every non-M3 player).

---

## M1 — THE FIVE-LEG DECOMPOSITION. EVERY PLAYER. `_eo` IN ITS OWN COLUMN.

### Board-wide totals (numéraire SCAR) — the machine, mechanism by mechanism

| Leg | Board total | movers | what it is |
|---|---:|---|---|
| **up-branch credit** | **+11,371** | 39 up | proven risers, `S_AGE·(Lc−Lo)` after both gates |
| **down-branch raw penalty** | **−4,862** | 42 down | proven fallers, `sw·(Lc−Lo)` at agemult=1 |
| **`_agemult2` amplification** | **−3,668** | 39 down | the extra shave from the ≤0.98 multiplier |
| **`_eo` drag** | **−12,404** | 161 down | *the uncounted leg — the single largest mechanism on the board* |
| core (thin/cameo blend)* | +21,481 | 167 up | non-proven par-prior / pedigree blend (not part of the up/down fork) |
| residual (M3 blend) | −2,479 | — | in-progress value interpolation |
| **NET** | **+9,439** | | Σ\|total\| churn = 55,517 |

\* the thin/cameo core is shown for completeness; it is the `n<PROVEN_N` blend, not one of the four fork legs.

**Headline:** among the four fork legs, **`_eo` (−12,404) is larger than the down-penalty and the age multiplier
combined (−8,530)** — the leg nobody has ever counted is the biggest single drag on the board.

### Top 30 by |total|

```
player                 branch         n age   eo | baseSC |    up   down    age     EO  other resid |  total | native
Sean Darcy             falling-shed   7  28 1.00 |  1930 |    +0   -738   -255     +0     +0    -1 |   -994 |   985
Archie Roberts         thin           2  21 0.25 |  5372 |    +0     +0     +0     +0   -985     0 |   -985 |  4616
Lachlan Ash            rising         7  25 1.00 |  4075 |  +967     +0     +0     +0     +0     0 |   +967 |  5307
Finn Callaghan         rising         4  23 0.75 |  4629 |  +917     +0     +0     +0     +0     0 |   +917 |  5837
Mark Keane             thin           2  26 0.50 |  2381 |    +0     +0     +0     +0   -758   -62 |   -820 |  1643
Murphy Reid            thin           2  20 0.00 |  4514 |    +0     +0     +0     +0   -720     0 |   -720 |  3993
Darcy Wilmot           rising         4  23 0.75 |  3551 |  +686     +0     +0     +0     +0     0 |   +686 |  4459
Jake Bowey             rising         4  24 1.00 |  2554 |  +578     +0     +0     +0     +0    87 |   +665 |  3388
Lloyd Meek             falling-shed   4  28 0.80 |  1538 |    +0   -362   -281     +0     +0     0 |   -643 |   942
Sam Darcy              thin           2  23 0.68 |  4504 |    +0     +0     +0     +0   -639     0 |   -639 |  4067
Max Holmes             rising         6  24 1.00 |  5512 |  +638     +0     +0     +0     +0     0 |   +638 |  6472
Josh Lindsay           thin           1  19 0.00 |  2390 |    +0     +0     +0     +0   -637     0 |   -637 |  1845
Bailey Smith           rising         7  26 1.00 |  4626 |  +618     +0     +0     +0     +0     0 |   +618 |  5518
Tom McCarthy           thin           2  26 0.00 |  2146 |    +0     +0     +0     +0   -611     0 |   -611 |  1615
Max Hall               thin           2  24 0.25 |  2462 |    +0     +0     +0     +0   -607     0 |   -607 |  1952
Timothy English        falling-hold   7  29 1.00 |  3723 |    +0     +0     +0   -591     +0     0 |   -591 |  3296
Rowan Marshall         falling-shed   9  31 1.00 |  1188 |    +0   -411   -171     +0     +0     0 |   -582 |   637
Aaron Cadman           thin           3  22 0.50 |  2428 |    +0     +0     +0     +0   +615   -37 |   +578 |  3163
Sam Berry              rising         5  24 1.00 |  2175 |  +556     +0     +0     +0     +0     0 |   +556 |  2874
Kieren Briggs          falling-shed   4  27 0.82 |  2659 |    +0   -355   -162    -36     +0     0 |   -554 |  2215
Luke Jackson           rising         6  25 1.00 |  6907 |  +553     +0     +0     +0     +0     0 |   +553 |  7851
Nathan O'Driscoll      thin           3  24 0.63 |   398 |    +0     +0     +0    -41   +593     1 |   +553 |  1001
Brayden Cook           thin           2  24 0.61 |   231 |    +0     +0     +0   -173   +697     0 |   +524 |   794
Connor MacDonald       rising         5  23 0.75 |  1967 |  +517     +0     +0     +0     +0     0 |   +517 |  2614
Josh Dunkley           falling-shed  10  29 1.00 |  1394 |    +0   -411    -90     +0     +0     0 |   -502 |   939
Ryley Sanders          thin           3  21 0.25 |  3472 |    +0     +0     +0     +0   +488     0 |   +488 |  4168
James Rowbottom        falling-shed   8  26 1.00 |   942 |    +0    -93   -383     +0     +0     0 |   -476 |   490
Jordan Ridley          falling-shed   5  28 0.85 |  1515 |    +0   -338   -165     +0     +0    29 |   -475 |  1094
Marcus Windhager       rising         5  23 0.75 |  1246 |  +473     +0     +0     +0     +0     0 |   +473 |  1809
Daniel Turner          thin           3  24 0.70 |  1174 |    +0     +0     +0     +0   +442     0 |   +442 |  1700
```

Full per-player CSV of all 804 is `census_data.json`. Note the fork's asymmetry made concrete: every `falling-shed`
player carries **two** negative legs (down **and** age), while the age column never lifts anyone; the biggest
`_eo`-only mover is **Timothy English (−591, 100% `_eo`)** with all fork legs at zero.

---

## M2 — THE DENIED-CREDIT LEDGER (the counterweight to the flattery census)

**175 proven risers** generated **+40,191 SCAR** of improvement value (level `Lo→Lc`, priced at 100%).
They were **credited +11,371**. **They were DENIED +28,820 SCAR — 71.7% of everything they improved.**

The denial splits **cleanly and exhaustively** across the three gates (they sum to the total exactly):

| Gate | players | SCAR denied | share |
|---|---:|---:|---:|
| **`S_AGE` age discount** (on the 46 who *passed* both gates) | 46 | **14,637** | 50.8% |
| **`TOL_M1` cliff** (0 < improvement < 5.0 → zero) | 124 | **12,268** | 42.6% |
| **`_radq` cliff** (improved ≥5.0, no 12-game season above `Lo`) | 5 | **1,915** | 6.6% |
| **TOTAL DENIED** | | **28,820** | 100% |

### Denied by `TOL_M1` — the 4.0–4.9 list (a rounding error from credit)
124 risers improved but by < 5.0 and got **nothing**. Had the cliff been a ramp, their (still `S_AGE`-discounted)
credit would have been **+5,739 SCAR**. The 20 who sit at **4.0–4.9 — one tenth of a point from credit**:

```
Josh Rachele    4.93 (would +416)   Tom Green       4.83 (would +329)   Nick Murray     4.61 (would +104)
Bailey Williams 4.93 (would   +0)   Jack Gunston    4.71 (would   +0)   Max Gawn        4.54 (would   +0)
Izak Rankine    4.92 (would +117)   Brent Daniels   4.63 (would  +74)   Josh Worrell    4.52 (would  +73)
Mac Andrew      4.86 (would +372)   Oliver Florent  4.41 (would  +15)   Josh Daicos     4.39 (would  +11)
George Hewett   4.86 (would   +0)   Jarman Impey    4.38 (would   +0)   Lachlan Schultz 4.33 (would   +0)
Jordan Clark    4.27 (would +131)   Rhyan Mansell   4.23 (would  +43)   Sam Wicks       4.22 (would   +0)
Shai Bolton     4.16 (would   +1)   Peter Wright    4.02 (would   +0)
```
(A `would = 0` means the age discount **or** `_radq` would have zeroed the credit even if `TOL` had passed —
i.e. these players are blocked twice over. Gawn improved 4.54 *and* is a 30+/RUC zero either way.)

### Denied by `_radq` — the 10-and-11-game list (one game from their whole improvement counting)
5 risers cleared 5.0 but have no 12-game season above `Lo` in the last two years. **Three are one game short:**

```
Errol Gulden   MID  imp 6.24  best recent season = 10 games   (would +72)
Tim Taranto    MID  imp 5.24  best recent season = 11 games   (would  +1)
Francis Evans  GEN_FWD imp 7.12 best recent season = 11 games (would +41)
— also blocked (further from the bar):
Bailey J. Williams RUC imp 11.95 best 9 games (would +196)    Will Day MID imp 9.31 best 6 games (would +230)
```

### Denied by `S_AGE` — the age discount, and the 30+ zeroes
The 46 risers who passed *both* gates still lost **+14,637 SCAR** to the age curve (`S_AGE`: 0.92@20 → 0.49@25 →
0.15@28 → **0.00 from 30**). The heaviest shaves are on prime-age improvers, not just elders:

```
Nick Blakey     26  imp 8.04  full +1008  granted +197  SHAVE +811
Luke Jackson    25  imp14.86  full +1310  granted +553  SHAVE +757
Sam Berry       24  imp15.44  full +1291  granted +556  SHAVE +735
Kysaiah Pickett 25  imp12.40  full  +920  granted +218  SHAVE +702
Jake Bowey      24  imp 9.27  full +1212  granted +578  SHAVE +635
Jack Ross       26  imp13.38  full  +586  granted  +61  SHAVE +525
Ed Richards     27  imp11.45  full  +661  granted +153  SHAVE +508
Justin McInerney 26 imp 8.81  full  +628  granted +143  SHAVE +486
Lachlan Ash     25  imp11.26  full +1410  granted +967  SHAVE +443
Max Holmes      24  imp12.99  full +1043  granted +638  SHAVE +406
```

**Every player aged 30+ who improved and received EXACTLY ZERO** (passed both gates, `S_AGE=0`):

```
Callum Wilkie  KEY_DEF  age 30  improved 6.18  → shaved (=full) +406
Jack Sinclair  GEN_DEF  age 31  improved 6.14  → shaved (=full) +143
Isaac Heeney   MID      age 30  improved 13.34 → shaved (=full)  +72
Brodie Grundy  RUC      age 32  improved 10.02 → shaved (=full)  +21
```

---

## M3 — THE ENGLISH TEST (`_eo`)

### 1. Every player's `eo`, and how many sit at/near 1.0
`eo` distribution over 804: **at 1.0 → 250**; ≥0.99 → 251; ≥0.90 → 278; strictly in (0, 0.9) → 296; **==0 → 230**;
mean **0.504**. `eo` weight is strongly predicted by durability: **corr(career games, `eo`) = +0.854** board-wide
(+0.507 among proven). *So the supervisor is right that `_eo` keys on availability — at the weight level.*

### 2. Does `_inferM1` override `_coreM1`? (shipped level vs `_coreM1` output)
At `eo = 1.0`, `_inferM1 = min(coreM1, max(_upS, _lvlcurr))` — the `(1−eo)·L0` term **does vanish** and `coreM1`
enters **only** through the `min()`. Whether that overrides `coreM1` depends on which side of the `min()` binds:

Among the **251** players at `eo ≥ 0.99`:
- **79 OVERWRITTEN** — `coreM1 > demonstrated floor`, so `min()` returns the floor and `coreM1`'s value is moot
  (mean level drop 1.46; Σ drag **−2,572 SCAR**). *These are the fallers and hold-band players.*
- **172 PRESERVED** — `coreM1 ≤ demonstrated floor`, so `min()` returns `coreM1` itself. *These are the risers /
  at-production players — the up-branch survives untouched.*

So the down-side is bypassed; the up-side is preserved. `_eo` at full strength **overwrites the down-branch
machinery and leaves the up-branch intact.**

### 3. Is the DOWN_TOL hold band real, or is it undone by `_eo`?
**It is a guard that does not guard.** Of **94** `falling-hold` players (drop ≤ 3.0, `coreM1 = Lo` — "forgiven"),
**`_eo` drags 92 of them (98%) down anyway**, for **−2,706 SCAR**. The hold band holds for exactly two players.
Biggest hold-band victims:

```
Timothy English  RUC   drop 2.83  eo 1.00  eo_SCAR −591  (career 163g)  ← the worked case
Sam Taylor       KEY_DEF drop2.78 eo 1.00  eo_SCAR −262  (career 133g)
Darcy Cameron    RUC   drop 1.85  eo 1.00  eo_SCAR −176  (career 132g)
Chad Warner      MID   drop 2.84  eo 1.00  eo_SCAR −174  (career 122g)
Clayton Oliver   MID   drop 2.01  eo 1.00  eo_SCAR −116  (career 218g)
```
**English confirmed exactly:** `Lo = 106.89`, drop **2.83** (inside the 3.0 band), `coreM1 = Lo = 106.89`
(the fork forgave him), then `eo = 1.0` pulled shipped to `Lc = 104.06` (his demonstrated floor). His whole loss is
`_eo`, fork legs zero. **Measured total −591 SCAR** on board `3dc19fbb` (the directive's "−189" is a stale figure;
the mechanism — hold-band-forgiven then `_eo`-dragged — is exactly as described, the magnitude is larger here).

### 4. Does durability predict the size of the drag?
**No — and this is where the supervisor's hypothesis breaks.** State plainly:
- The `_eo` **weight** rises with durability (corr with career games **+0.85**). ✔ availability is punished *at the weight*.
- The `_eo` **drag (SCAR)** does **not**: among the 251 dragged, corr(career games, |drag|) = **−0.197**, and
  corr(`eo`, |drag|) = −0.037 (≈0). The drag size tracks the **depth of the dip** (`coreM1` − demonstrated floor),
  not games played.
- In fact the **most durable players are disproportionately PRESERVED**: mean career games of the *preserved*
  `eo≈1.0` group is **169**, versus **91** for the *dragged*. Durable stars tend to sit at/above their demonstrated
  floor (risers → preserved). English looks like the rule (durable **and** dipped) but is the exception: across the
  board, "the more durable, the harder the drag" is **not** what the numbers say.

---

## M4 — FLATTERY'S TWIN: WHO IS LIFTED BY A THIN HOT SAMPLE?

Jamarra's 3 games at 26.0 *cost* him because the cameo was **unlucky**, not because it was **small**. The upside twin:
players whose level is materially **raised** by a thin, high-average recent season. Scan: any season with < 8 games,
avg > `Lo`, in the last 3 years; counterfactual removes those seasons and re-prices the level lift.

**85 candidates; 37 material (> 10 SCAR); Σ lift handed by thin samples = +5,645 SCAR.** Top 20:

```
player             pos      n  branch  liftSCAR native  thin-hot season(s) (yr,games,avg)
Nathan O'Driscoll  MID      3  thin      +552    951   2026: 6g @ 78.8
Kane McAuliffe     MID      0  cameo     +438   1243   2025: 5g @ 81.6 ; 2026: 6g @ 77.7
Rhett Bazzo        KEY_DEF  1  thin      +410    567   2025: 7g @ 53.1 ; 2026: 5g @ 66.0
Will Day           MID      4  rising    +349   2950   2025: 6g @ 99.0 ; 2026: 2g @ 102.5
Jake Bowey         GEN_DEF  4  rising    +337   3219   2026: 6g @ 99.2
Jack Lukosius      KEY_FWD  6  falling   +326   1437   2026: 4g @ 80.3
Peter Ladhams      RUC      4  falling   +316    458   2026: 1g @ 97.0
Ned Moyle          RUC      0  cameo     +309   1630   2026: 6g @ 82.7
Elijah Tsatas      MID      0  cameo     +271   1181   2026: 6g @ 82.5
Caiden Cleary      GEN_FWD  1  thin      +248    740   2026: 5g @ 60.8
Deven Robertson    MID      2  thin      +244    294   2026: 4g @ 84.5
Xavier Lindsay     GEN_DEF  1  thin      +240   1445   2026: 5g @ 70.6
Campbell Chesser   MID      2  thin      +235    552   2025: 4g @ 63.2 ; 2026: 3g @ 62.7
Harry Rowston      MID      1  thin      +210    906   2026: 4g @ 58.3
Sam Lalor          MID      1  thin      +185   3483   2026: 7g @ 81.3
Jedd Busslinger    KEY_DEF  0  cameo     +158    735   2026: 4g @ 74.5
Cooper Lord        MID      1  thin      +124    392   2024: 2g @ 78.5 ; 2026: 3g @ 76.7
Sam Marshall       MID      1  thin       +79   1125   2026: 2g @ 63.5
Errol Gulden       MID      5  rising     +76   5743   2026: 2g @ 112.5
Hayden McLean      KEY_FWD  4  falling    +74    631   2026: 4g @ 66.2
```

The cameo cuts both ways: **Peter Ladhams' single game at 97.0** and **Ned Moyle's 6 games at 82.7** are handed
+316 / +309 SCAR by samples too thin to trust — the exact mirror of Jamarra's thin sample deleting his. Note the
cross-links: **Gulden and Will Day** appear in *both* the `_radq` denied-credit list (thin qualifying seasons block
their up-credit) *and* here (the same thin seasons lift their level through `_lvlcurr`) — the machine punishes their
thinness on the up-branch gate and rewards it on the level channel in the same breath.

---

## IN PLAIN TERMS

The owner asked what the down branch costs. It is only half the machine, and the half nobody had counted —
**`_eo` — is the biggest single lever on the board (−12,404 SCAR, larger than the down-penalty and the age
multiplier put together).**

1. **Risers face cliffs.** The board's improvers earned +40,191 SCAR of improvement and were allowed to keep
   +11,371 — **71.7% denied.** Half of that (14,637) is the age discount, which zeroes anyone 30+; the other
   half is two step-function gates — a 5.0-point cliff (20 players sit at 4.0–4.9) and a 12-game cliff (three
   players are on 10 or 11). One tenth of a point or one game deletes the whole credit.

2. **Fallers get a ramp — and then `_eo` ignores it.** The 3.0 hold band is supposed to forgive a small dip.
   It forgives 94 players in the fork and then **`_eo` drags 92 of them down anyway (−2,706 SCAR).** The guard
   guards two players. English is the worked case: forgiven by the fork, sunk −591 by `_eo`.

3. **The supervisor's `eo = 1.0` hypothesis is TRUE — with one correction.** At full strength the `(1−eo)·L0`
   term vanishes and `coreM1` survives only through a `min()`; for the 77–79 established players sitting above
   their demonstrated floor (the fallers and the hold-band), the hold band, the down-ramp **and** the age
   multiplier are **all bypassed** — `coreM1` is overwritten by the floor. The correction: it is the **down-side**
   machinery that is bypassed. Established **risers** (172 of 251 at `eo≈1.0`) keep `coreM1` intact, because the
   `min()` returns it. So "the careful machinery survives only for the un-established" is not quite right — the
   up-branch survives for everyone; the **down-branch** is what `_eo` erases for the established.

4. **`_eo` punishes availability at the weight, but the pain is not durability's.** `eo`-weight tracks games played
   (+0.85). But the **cost** does not (−0.20): the drag is set by how far you dipped, not how durable you are, and
   the most durable players are the ones most often spared. **The supervisor is right about the trigger and wrong
   about the target.**

5. **The thin-sample lottery runs both ways.** 37 players are handed +5,645 SCAR by seasons too thin to trust
   (a single game at 97, six games at 82) — the exact mirror of Jamarra losing ~820 to three unlucky games.
   The cameo is priced for luck, not size, in both directions.

The owner has already ruled the direction (symmetric smoothing; the same drop to be "declining" as the rise to be
"rising"). **This census measures what the current asymmetry costs; it proposes no lever and wires nothing.**

*Tier 3, read-only. Candidate — no bake, no tag, no merge. Board md5 `3dc19fbb` (== `81e48293` except bramble +1).*
