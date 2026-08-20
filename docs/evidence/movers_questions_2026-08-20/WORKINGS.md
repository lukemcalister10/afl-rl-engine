# R22 → R23 MOVERS — NUMERIC DECOMPOSITION OF FOUR OWNER QUESTIONS

Read-only investigation. No board build, no build lock taken. Every number below is either read
from a committed artifact or measured by loading the engine in-process against a **copy** of the
workspace in scratch (`ws_r22/`, `ws_r23/`) with a scratch repo root (`repo_r22/`, `repo_r23/`).
Nothing in `/home/user/afl-rl-engine` was written.

## 0 · THE TWO BOARDS AND THE EXACT INPUTS

| | R22 side | R23 side |
|---|---|---|
| board | `1d5c9f7a` "20/8 INJURY-SHEET RE-CUT" (`value_history` column `the-sheet-recut-20-8`) | `68be10c7` (live) |
| store | `cc02567f` (`git show b7ec627^:engine/rl_after/rl_model_data.json`) | `b745002e` |
| season state | as_of_round 22, calendar_progress **0.92**, exposure_pace 0.818 | as_of_round 23, calendar_progress **0.96**, exposure_pace 0.864 |
| engine | `_merged_recover.py` — **byte-identical** (`git diff --stat 2305743 b7ec627` shows no engine file) |

So the *entire* R22→R23 transition is: (a) 411 round-23 score rows merged into the store, and
(b) the season clock advancing 0.92 → 0.96 (+ the exposure pace 0.818 → 0.864). Nothing else.

Note on the two season-state values: `exposure_pace` is read **only** by
`engine/forward_valuation/conditional_prior.py`; `_merged_recover.py` and `rl_model.py` read only
`calendar_progress` (`grep -n "_season_val"`), and `_merged_recover.py` never imports
forward_valuation. So the season-state term in every split below **is** the calendar progress.

Board-level constants that moved (these are the pool renormalisation — the "global" term):
`SCALE 1.34483 → 1.34146` (−0.25 %), `SEASON_PROG 0.92 → 0.96`, and sub-0.2 % wobbles in
`POOL`, `BASEPK_REG`, `PJ`. `REPL`, `PEAK`, `ALPHA`, `GAMMA` unmoved.

Numeraire (engine currency → board currency) = **1.052329**, stable across both boards
(verified on Tom Green: 5932.323/1.052329 = 5637.0 = board; 5866.731/1.052329 = 5575.0 = board).

## 1 · THE 2×2 — GLOBAL vs PLAYER-SPECIFIC, MEASURED

Two full in-process loads (R22 store + R22 season state; R23 store + R23 season state). Inside
each load the target player's 2026 scoring row was swapped to the other side's row and re-priced,
then restored with a round-trip assert (all `rt=True`). Board currency:

| player | G22/S22 | G22/S23 | G23/S22 | G23/S23 | TOTAL | GLOBAL | SPECIFIC |
|---|---|---|---|---|---|---|---|
| Nicholas Martin | 4287.9 | 4061.1 | — | 4061.1 | **−226.8** | **−226.8** | **0.0** |
| Tom Green | 5637.3 | 5575.0 | — | 5575.0 | −62.3 | −62.3 | 0.0 |
| Darcy Jones | 1303.5 | 1280.2 | — | 1280.2 | −23.3 | −23.3 | 0.0 |
| Joshua Kelly | 779.5 | 759.3 | — | 759.3 | −20.2 | −20.2 | 0.0 |
| William McCabe | 228.8 | 229.8 | — | 229.8 | **+1.0** | **+1.0** | **0.0** |
| Sid Draper | 914.3 | 905.7 | — | 905.7 | −8.6 | −8.6 | 0.0 |
| Clay Hall | 415.2 | 384.2 | — | 384.2 | −31.0 | −31.0 | 0.0 |
| Max Kondogiannis | 356.7 | 371.5 | 344.1 | 358.9 | **+2.2** | **+14.8** | **−12.6** |
| Josh Dolan | 279.8 | 280.7 | 234.3 | 247.2 | **−32.6** | **+0.9** | **−33.5** |
| Lachie Jaques | 607.6 | 580.4 | 589.0 | 569.4 | −38.2 | −27.2 | −11.0 |
| Luke Trainor | 1007.6 | 982.9 | 960.1 | 932.5 | −75.1 | −24.7 | −50.4 |
| Lachlan Gulbin | 211.3 | 208.9 | 234.4 | 234.3 | +22.9 | −2.4 | +25.3 |

(G22/G23 = his 2026 scoring row; S22/S23 = the whole rest of the board, i.e. store + season state.
Where the store row is byte-identical there is no specific term at all, by construction.)

## 2 · NICHOLAS MARTIN — −227 (4288 → 4061, −5.29 %), rank 23 → 27, DNP

### 2.1 His inputs did not move — at all
`cc02567f` vs `b745002e`, the row is byte-identical:
`2026: {avg 0.0, games 0}`; career 83 games; pick None (SSP, 2021); effpk 65, band 7.
Measured internals, R22 vs R23, identical to the last digit:
`_lvlcurr 98.8206`, `_par_prior 75.8036`, `bestlvl 105.0`, `E_q 3.98935`,
`ev_rec 0.98135`, `ev_est 0.57642`, `ev_pw 0.13118`, `nseas_pro 4`, `draftval 237`.
Only `v0_start` moved, 615.20 → 613.76 (−0.234 %), which is pool renormalisation.

**So 100 % of the −227 is the global term.** Confirmed twice: by the 2×2 above, and by the fact
that there is no other candidate.

### 2.1a THE GLOBAL TERM SPLIT — pool vs season clock (CLOSED, 3 loads)

Three loads, each a full engine load against a scratch copy; the store row is byte-identical for
every player in this table, so `A→B` is the **pure pool** term and `B→D` is the **pure season**
term, and they sum exactly to the total.

```
A = R22 store + R22 season      B = R23 store + R22 season      D = R23 store + R23 season
player               A        B        D  |    TOTAL     POOL    SEASON
Nicholas Martin   4287.9   4278.5   4061.1 |   -226.8     -9.3    -217.4   (season  96 %)
Tom Green         5637.3   5624.5   5575.0 |    -62.3    -12.8     -49.5   (season  79 %)
Joshua Kelly       779.5    777.6    759.3 |    -20.2     -2.0     -18.2   (season  90 %)
Darcy Jones       1303.5   1300.9   1280.2 |    -23.3     -2.6     -20.7   (season  89 %)
William McCabe     228.8    228.8    229.8 |     +1.0     +0.0      +1.0   (season 100 %)
```

**The season clock is 96 % of Martin's move; the pool renormalisation is 4 % (−9.3 board).**
McCabe's pool term is exactly 0.0 — his +1 is entirely the season clock.

### 2.1b WHERE THE SEASON TERM ACTUALLY ENTERS — a correction worth recording

`probe6_clock.py` patches `SEASON_FE`/`M3_FE` to 0.92 **after** the load and recomputes the
healthy counterpart, so it moves the *evaluation-time* clock only; surfaces built at load time
from fE (the V0 curve/guard, the precomputed parity floor) stay at 0.96. Subtracting:

```
player             SEASON tot   evaluation-time clock   surfaces baked at load from fE
Nicholas Martin       -217.4                   -30.5                          -186.9
Tom Green              -49.5                   -56.4                            +7.0
Joshua Kelly           -18.2                   -18.1                            -0.2
Darcy Jones            -20.7                   -20.7                            +0.0
```

For Kelly and Jones the season term is **entirely** the call-time clock — the depth read at
evaluation. **For Martin it is not**: only −30.5 of his −217.4 comes through the call-time read,
and −186.9 comes through surfaces the engine bakes from fE at load. So the §2.3 depth arithmetic
correctly describes *the quantity that moved* (his `c_u`, exactly reproduced to 7 decimals) and
the season clock is correctly identified as 96 % of the cause — but the **transmission** into his
price is mostly through load-time-baked fE surfaces, not through the depth read, and I have not
traced which surface. This is stated because an earlier pass of this file implied the depth read
itself carried the charge. It does for Kelly and Jones. It does not for Martin.

### 2.2 The board is NOT charging him for being unavailable — it is paying him the healthy price
Measured in-process (`_D7_ROWS`, the ORDER-D7/`RL_O43` parity guard from register v771):

```
nicholas-martin  v_injury = 3268.24   v_healthy = 4273.59   won = healthy   delta = +1005.35
                 treated_avail = True  treated_inj = True   floor_binds = True
```

His *injury-regime* price is 3268 engine (= 3106 board). The board carries 4273.59 engine
(= 4061 board) — the **healthy counterpart**, +955 board points higher. The owner's own parity
ruling ("being marked as injured shouldn't enrol you in a mechanism that doesn't affect your
peers") is doing exactly what it says. **The standing law holds: forward availability is not
being priced.** The `avail_nerf` column (−1045 → −1005) is the attribution of a charge that the
guard then discards.

### 2.3 What actually moved: the UNPLAYED-TIME DEPTH CLOCK
`o31_cu` — "the fade clock MINUS the time he actually played". For Martin the healthy-counterpart
clock is, exactly:

```
c_pre                = fade30b_clock(p,2025) − o31_played_units(p,2025) = 5.0 − 4.0 = 1.0
r  = o41_reversal(16 delivered games)                                    = 0.5959292984
carry              = (1 − r)·c_pre                                       = 0.4040707016
in-progress accrual = _o41_fe(2026) = fE^1.5      (RL_O41_RAMP: concave, not linear)
        R22:  0.92^1.5 = 0.8824330
        R23:  0.96^1.5 = 0.9406041
c_u = carry + accrual
        R22:  0.4040707 + 0.8824330 = 1.2865037   (measured in-process: 1.2865)
        R23:  0.4040707 + 0.9406041 = 1.3446748   (measured in-process: 1.3446748)   Δ = +0.05817
ruled fade at that depth  fade30b_D(c) = 0.5501936^(c−1)
        R22:  0.842668     R23:  0.813884    (measured `fade_at_cu` = 0.813883510087804)  → −3.42 %
```

That is the only quantity in his valuation that moved between the two boards. The season went
from 92 % to 96 % elapsed; the fraction of the season he has not played entered his sitting depth
as `fE^1.5`; his depth moved +0.0581 and his price moved −5.29 %.

### 2.4 Comparable, same mechanism, different person
Every zero-game player carries the same clock; the size of the charge scales with where his depth
sits on the fade and with his pick-signal exponent `o35_kappa`/`o36_kappa`:

| player | age | 2026 g | c_u R22 → R23 | κ (o36) | move |
|---|---|---|---|---|---|
| Tom Green | 25 | 0 | 1.5347 → 1.5929 | 0.6714 | −1.11 % |
| Joshua Kelly | 31 | 0 | 1.2865 → 1.3447 | 0.5 | −2.59 % |
| **Nicholas Martin** | 25 | 0 | **1.2865 → 1.3447** | **1.4469** | **−5.29 %** |
| Darcy Jones | 22 | 0 | 1.6906 → 1.7487 | — | −1.77 % |

Martin and Joshua Kelly have the *identical* depth clock (both last delivered 2025, both carry
0.40407) and take different-sized hits: −5.29 % vs −2.59 %. The ordering across the four tracks
the pick-signal exponent (Kelly pick 2, κ=0.5; Green pick 10, κ=0.671; Martin pickless SSP,
effective pick 65, κ=1.447) — i.e. **the sitting charge is steeper the weaker the draft pedigree**,
which is the design intent (a low-pedigree row has no pedigree anchor to fall back on) and is why
Martin is the only DNP name in the top-20 fallers.
CAVEAT, stated because precision is the law here: `o31_D` reads **1.0 for Martin on both boards**
(the ORDER-A stage-5 selection buy-back caps the fade at 1 for a row with a recent selected
season), so the depth `c_u` is *not* reaching his price through `o31_D` itself. `c_u` is the only
input of his that moved, and the size ordering matches κ, but I have not isolated the downstream
site that carries it. Treat "κ explains the size" as an ordering observation, not a measured
attribution.

### 2.5 Board-wide confirmation of the mechanism (all 393 DNP rows, no engine needed)
The M3/absence machinery is keyed on games played this season. Median % move by 2026 games:

```
2026 games:   0     1     2     3     4     5     6     7     8     9    10    11   12+
median %:  -2.22 -2.21 -2.04 -1.64 -0.46 -1.83 -1.45 -1.82 -0.77 -0.64  0.00  0.00 -0.15
n:          139    13    30    22    14    19    17    14    15    12    13    12    73
```

Monotone: a DNP row that has played a full season's worth of games moved 0.00 %; a row that has
played none moved −2.22 %. Martin's −5.29 % is 2.4× the zero-game median, and §2.4 shows why.

### 2.6 FORWARD NOTE (flagged)
At round 24 `fE` → 1.00, so `c_u` → 0.4040707 + 1.0 = 1.4040707, another **+0.0594** of depth
(this round's step was +0.0582) and `fade30b_D` → 0.785507 (this round: 0.842668 → 0.813884).
A further charge of the same order is due at round 24 **by construction**, for Martin and for
every zero-game row. This is not a surprise the owner should meet cold.

## 3 · MAX KONDOGIANNIS — +2 (357 → 359, +0.56 %) off a 71

### 3.1 What actually changed
`2026: 9 games @ 36.60 → 10 games @ 40.04`. Check: (9×36.6 + 71)/10 = 40.04 ✓.
**A 71 in one game moves his season average by +3.44, not by +34.** That is the first half of the
answer and it is just arithmetic: the engine prices his *level*, and one game is one tenth of it.

Measured internals R22 → R23:

```
_lvlcurr    36.60   →  40.04    (+3.44, +9.4 %)
bestlvl     36.60   →  40.04
_par_prior  55.858  →  55.858   (unchanged — the par for his position × pick)
E_q         0.1397  →  0.2872   (+106 %)   ← the 10th game of evidence
ev_rec(E_q) 0.0606  →  0.2142   (×3.5)     ← weight on his own recent form
ev_pw(E_q)  0.0541  →  0.1704
v0_start   445.21   → 445.21    (his baseline anchor — unmoved)
o31_cu       1.1032 →   1.1077   o31_D = 1.0 both (no sitting fade — he is playing)
```

### 3.2 The two halves cancel — and his own half is NEGATIVE
2×2 split: **GLOBAL +14.8, SPECIFIC −12.6, net +2.2.**
His own change (the 10th game plus the 71) was worth **−12.6**; everything else on the board
moving was worth **+14.8**. The +2 the owner is looking at is the residue of two larger,
opposite terms.

**Why negative, when his level went UP 9.4 %? The sweep in §3.4 is the answer, and it is not the
story I first reached for.** Playing a 10th game *at all* is worth roughly **+13** to him (a
score of 0 prices at 384.8 against the 9-game counterfactual's 371.5). The 71 is what costs him:
it carries his season average to 40.04, which lands in a **trough** of a price curve that is
non-monotone in that average. It is not "the 10th game sheds his pedigree" — that framing is
contradicted by the sweep, because at a score of 30 or 40 the same 10th game *gains* him 25–28.
The evidence-weight and pedigree numbers below are real and moved as stated, but they do **not**
explain the sign or the size of his move. The curve shape does.

### 3.3 What caps a first-year defender — measured, not asserted
He has **one** season of evidence, so `_ev_est(E_q) = 0.0005` — the "established" weight is
effectively zero, and `pedDecay = 1.0` (full pedigree weight). His price is his **baseline anchor**
(`v0_start` 445.2 engine ≈ 423 board) adjusted, not his production. His board value 359 sits
*below* that anchor. Until he accumulates evidence (E_q rises through ~3.6 before `_ev_est`
reaches a half), single scores cannot move him much: the level channel is throttled by the
evidence weight and the pedigree channel is anchored by a fixed v0.

### 3.4 What a 71 WOULD have to be — measured by sweeping his round-23 score
Same engine, same board, only his round-23 score changed (10 games, average recomputed), board
currency. `no R23 game` = the 9-game counterfactual priced under the R23 board = 371.5.

```
R23 score:    0     20     30     40     48     55     60    71     80     90    100    110    120    140
board v:  384.8  389.1  396.1  399.0  386.8  362.0  365.7 358.9  335.9  324.3  330.8  358.6  380.4  428.7
```

To beat the 9-game counterfactual (371.5) he needed roughly **a score under ~50 or over ~115**.
His 71 landed in a trough. See §5 — this is a finding, not a description of intended behaviour.

### 3.5 Peer cross-check
Among the 15 thin-evidence players (5–13 games in 2026) whose round-23 score beat their prior
season average by +20 to +40, the median move was **+8.49 %**. Kondogiannis (+34.4 surprise) got
**+0.56 %** — second-lowest in the group. `wil-dawson` (58 vs prior 33.5, 9 games, pick 22)
got +1.36 %; `eric-hipwood` (80 vs 47.2) +6.52 %; `jay-polkinghorne` (71 vs 44.5) +29.6 %.
**The owner's instinct that the 71 under-registered is supported by his peers.**

## 4 · WILLIAM McCABE — he is not an R23 mover; the drop was 20 August

### 4.1 Round 23 did nothing to him
Store row byte-identical (`2026: 4 games @ 31.75`, career 4 games). Board 229 → 230 (**+1**,
+0.44 %). His rank fell 468 → 472 purely because ~400 players who played moved past him.
Every measured internal is identical R22 → R23: `_lvlcurr 31.75`, `_par_prior 60.411`,
`E_q 0.00172`, `nseas_pro 0`, `v0_start 653.82`, `ln/lns/pn/ps/ep/band/pedDecay/losd` all unmoved.

### 4.2 Where he actually fell — the registered value history
```
column                      value   rank
R22 (weekly)                  624    310
g1-never-rises-10-8           623    311
the-landing-20-8              229    439    ← the campaign board adopted, 20 Aug: −394 (−63 %)
the-d8-adoption-20-8          229    468
the-sheet-recut-20-8          229    468
R23                           230    472
```
None of his own inputs moved on 20 August either. The **pricing function** changed.

### 4.3 What the campaign board did, measured across the 804 rows
`36d5dfc7` → `a05fe951` (the D5-final dial line + the parity guard), median % move by career games:
```
career games <10 :  n=188   median −41.0 %
career games 10-29: n=128   median −26.9 %
career games 30-79: n=158   median −10.5 %
career games 80+  : n=330   median  +0.8 %
by pick band  0: +0.3 %  1: −1.4 %  2: −4.8 %  3: −6.0 %  4: −9.2 %  5: −5.1 %  6: −8.9 %  7: −17.5 %
```
It re-priced thin-evidence rows as a class. McCabe (4 career games, band 3) took −57 % on the
board file; the registered column shows −63 %. Attributed across the certified dial stages
(the D7B stage boards, still on disk):
```
D7B_IDENT_P 359 | D7B_IDENT_K 474 | D7B_L0R 410 | D7B_NOO42 229 | D7B_BASE 229 | D7B_CAND 229
```
The step to 229 is the **D5-final dial stack** (O37/O38A/O38B1/O39/O40/**O41**), not O42 and not
the parity guard O43.

### 4.4 Why he sits at rank 472 — the unplayed-time depth fade
Measured on the live board:
```
fade30b_clock      3.96      (2026 − 2023 draft year + fE)
o31_played_units   0.2288    (4 career games ≈ 0.23 of one season's credit)
o31_cu             3.7312    ← his unplayed-time depth, of a maximum 4 (the fade is FLAT from 4)
fade30b_D(c_u)     0.3213    the raw ruled fade
o31_D              0.5998    after the pick-signal exponent (κ = 0.5)
E_q                0.00172   effectively zero production evidence
nseas_pro          0         no qualifying season, ever
```
He is a pick-19 (2023) key defender with **4 career games in three seasons**. He is priced almost
purely as a prospect off his baseline anchor (`v0_start` 653.8) with a ~40 % discount for time not
played. That is the "depths-as-depths" law reaching its deep end, and it is exactly what it is
meant to charge.

### 4.5 Comparable
Clay Hall (pick 38, 2023, 0 games in 2026, c_u 2.27 → 2.33, `o31_D` 0.829 → 0.789) moved
415 → 384, **−7.47 %** in round 23 — the same depth clock, one year shallower and still running.
McCabe's clock has already reached the flat end, which is why round 23 could not move him.

## 5 · JOSH DOLAN — −33 (280 → 247, −11.79 %) off a 48

The owner said 15 %; the measured figure is **−11.8 %** (−33 board points). The 15 % is almost
certainly the row immediately above his in the movers table: `Ben Keays | Fwd | Adelaide | 57 |
221 | 188 | −33 | **−14.9 %**` sits directly above `Josh Dolan | Fwd | Western Bulldogs | 48 |
280 | 247 | −33 | −11.8 %` — same −33, adjacent rows. Worth saying out loud so the owner's own
figure is reconciled rather than silently corrected.

### 5.1 What changed
`2026: 9 games @ 50.09 → 10 games @ 49.88`. Check: (9×50.09 + 48)/10 = 49.88 ✓.
A 48 is *below* his running 50.09, so his season average fell by **0.21 points**. His blended
current level actually went **UP**:
```
_lvlcurr    42.935  →  43.477   (+0.54)   ← the 10th game re-weights 2026 against 2025 (11 g @ 27.4)
bestlvl     50.09   →  49.88    (−0.21)
_par_prior  58.065  →  58.065   (unchanged)
E_q         0.6397  →  0.7872   (+23.1 %)
ev_rec      0.5749  →  0.6720
v0_start   457.44   → 457.44    (unmoved)
o31_cu      1.1032  →  1.1077   o31_D = 1.0 both
```

### 5.2 The split
2×2: **GLOBAL +0.9, SPECIFIC −33.5.** Essentially all of it is his own row — the rest of the
board moving was worth less than one point to him.

And within his own row it is **not** the 48 dragging his average down by 0.21, and it is **not**
"the 10th game sheds his pedigree". The sweep in §5.4 falsifies both: playing a 10th game and
scoring **0** would have priced him at **297.0**, i.e. **+16.3** against the 9-game counterfactual
of 280.7; a **30** at 297.6 (+16.9). The extra game is a *gain* at those scores. His 48 carries
his season average to 49.88, which lands in a **trough**. The controlling variable is where his
new season average sits on a price curve that is non-monotone between roughly 48.5 and 53.
(Validation that the sweep is the real machinery and not an artefact: the sweep's score-48 point
reproduces the shipped board value 247.2 exactly, and its 9-game point reproduces the
independently-measured 280.7 exactly.)

The evidence/pedigree numbers below are real and did move as stated — they are just not what
carried the sign or the size here.

### 5.3 A pedigree-vs-production cross-check — same 9→10 step, opposite sign
`lachlan-gulbin`: 2024 entry, **pickless** (PDA, `draftval` 237 against Dolan's 589), same
9 → 10 games, scored 53, level 45.0 → 45.8, par 61.7 (a **larger** production-below-par deficit
than Dolan's). He moved **+22.9 (+10.9 %)**, 2×2 split GLOBAL −2.4 / SPECIFIC **+25.3**.

So the identical structural step — a tenth game in a first/second-year row — is worth **+25 to
one player and −33 to another**, at almost the same production level. Two more, same 9 → 10 step,
2024 draft: `luke-trainor` (pick 21) −7.45 %, `lachie-jaques` (pick 29) −6.41 %; both scored
*worse* than Dolan (33 and 32 against his 48) and both fell less. Whatever separates these four,
it is not the size of the round-23 score. (The natural hypothesis is pedigree-minus-production —
Gulbin has no draft anchor above his output to shed — and it is consistent with all four signs,
but I have not isolated the site, and §5.4/§6 shows the same rows also sit on a jagged curve,
so I am recording the ordering as an observation, not an attribution.)

### 5.4 The 48 was cheaper than a 30 — measured
Sweeping only his round-23 score (10 games, average recomputed), board currency, R23 board.
9-game counterfactual = 280.7.
```
R23 score:    0     20     30     40     48     55     60     71     80     90    100    110    120    140
board v:  297.0  294.8  297.6  261.2  247.2  247.4  250.8  254.9  286.3  328.5  374.0  404.4  406.1  391.9
```
**A duck egg would have been worth 297; his 48 was worth 247.** Every score from roughly 38 to 78
prices *below* a score of zero. See §6.

### 5.5 Peer cross-check
Among the 21 thin-evidence players whose round-23 score fell 0–20 points short of their prior
average, the median move was **−0.64 %**. Dolan's −11.79 % is the 4th-worst of the 21.
`harvey-harrison` (46 vs prior 46.8, 10 games, pick 52) took −5.48 %; `bailey-macdonald`
(45 vs 54.5, 11 games, pick 51) −1.85 %. The owner is right that this is heavy for the input.

## 6 · FINDING FOR THE RECORD — the price is not monotone in the round's score

Both sweeps in §3.4 and §5.4 are non-monotone over a wide interior band, holding everything else
fixed and changing only the round-23 score:

* **Josh Dolan** — 0 → 297.0, 30 → 297.6, **48 → 247.2**, 71 → 254.9, 90 → 328.5, 120 → 406.1.
  A ~50-point (−17 %) penalty for scoring 48 rather than 30.
* **Max Kondogiannis** — 0 → 384.8, 40 → 399.0, **71 → 358.9**, 90 → 324.3 (the trough),
  140 → 428.7. A 90 would have priced 60 points *below* a 0.

This is **local to thin-evidence rows**, not a board-wide inversion — the population is monotone:
across the 86 players with 5–13 games in 2026, median move by score-minus-prior-average is
−9.9 % (surprise −40..−21), −0.6 % (−20..−1), +3.5 % (0..+19), +8.5 % (+20..+39), +13.5 %
(+40..+59). Only 2 of 86 beat their prior average and still fell more than 5 %.

### 6a · THE DIP LOCALISED — it is a STEP STRUCTURE on a smooth input (`probe5_kink.py`)

Dolan only, season average swept 46.00 → 53.40 in steps of **0.2**, games fixed at 10, everything
else untouched. The sweep's restore point reproduces the shipped board value exactly (247.2 = 247).

```
avg    score   v       lvlcurr   radq  delivered
49.00   39.2  278.9    42.847    False  False
49.20   41.2  254.7    42.990    False  False   <== -24.2  (-8.7 %)
49.40   43.2  235.2    43.133    False  False   <== -19.5  (-7.7 %)
49.60   45.2  235.2    43.277    False  False       exact plateau
49.80   47.2  235.2    43.420    False  False       exact plateau
50.00   49.2  247.2    43.563    False  False   <== +12.0  (+5.1 %)
...
52.40   73.2  257.7    45.279    False  False
52.60   75.2  288.3    45.422    False  False   <== +30.5 (+11.8 %)
```

Three things are established here that "non-monotone" alone does not say:

1. **The level input is perfectly smooth.** `_lvlcurr` advances exactly +0.143 per grid step,
   linear in the average, across the whole band. `bestlvl` = the average exactly. The jaggedness
   is not in the level estimate.
2. **The price contains a genuinely discrete component.** Consecutive *distinct* inputs return
   **bit-identical** prices — `294.8031519805` over three grid points (avg 46.6/46.8/47.0),
   `235.2416369028` over two (49.6/49.8), `297.5779368357` over two (48.0/48.2). A steep smooth
   curve cannot do that. Something in the chain is a piecewise-constant lookup.
3. **It is not the two threshold predicates I could test.** `_radq` (the recent-form-adequacy
   switch) and `o32_delivered` (the delivered-season depth reset) are **False at every point** in
   the band, so neither is flipping. The site remains unidentified — but two plausible candidates
   are now ruled out, which narrows it.

**Where Dolan actually landed:** his 48 puts his average at 49.88, i.e. just past a two-step cliff
that costs **−43.7 board points (−16 %) between averages of 49.0 and 49.4** — a four-tenths-of-a-
point swing, which is the difference between one 48 and one 44 in a ten-game season. He sits at
247.2, immediately above the 235.2 floor of that structure and immediately below the +12 recovery.

I am **not** calling this a defect. What is measured is: for these rows, holding all else fixed,
the shipped price is a step function of a smoothly-moving level, with individual risers worth
8–12 % of the row. That is worth a ruling rather than a silent carry, because it means "he scored
well and went down" is a reproducible outcome of the pricing lookup, not a rounding artefact, and
both of the players the owner asked about sit inside the band.

## 6b · PEER TABLES (the two buckets quoted in §3.5 and §5.5, in full)

Population: PLAYED in round 23, 5–13 games in 2026. Surprise = round-23 score − prior 2026 average.

Surprise −20 .. 0 (n=21), median **−0.64 %**:
```
 -17.86% callum-ah-chee   43 vs 58.4 g7  pk8      -0.64% sam-lalor       59 vs 73.7 g12 pk1
 -17.24% billy-cootee     29 vs 47.7 g8  pk42     -0.57% harry-rowston   52 vs 61.5 g11 pk16
 -12.75% harry-kyle       29 vs 47.6 g8  pk14     -0.48% jack-williams   44 vs 52.4 g11 pk57
 -11.79% JOSH DOLAN       48 vs 50.1 g10 pk31     -0.06% hayden-young    77 vs 82.0 g12 pk7
  -7.14% jaxon-artemis    44 vs 54.2 g5  pk1      +0.45% nick-madden     63 vs 78.4 g8  pkNone
  -5.48% harvey-harrison  46 vs 46.8 g10 pk52     +1.43% louis-emmett    11 vs 29.7 g7  pk27
  -3.53% alix-tauru       35 vs 41.9 g9  pk10     +1.50% jake-rogers     35 vs 47.3 g8  pk14
  -2.26% joel-fitzgerald  69 vs 69.4 g9  pk16     +4.58% kye-annand      52 vs 59.8 g10 pk2
  -2.08% cooper-lord      68 vs 79.4 g8  pk9      +5.37% wade-derksen    55 vs 59.2 g12 pk5
  -1.85% bailey-macdonald 45 vs 54.5 g11 pk51     +5.68% braeden-campbell 62 vs 75.2 g5 pk5
                                                 +10.21% hugo-hall-kahan 61 vs 73.0 g10 pk10
```

Surprise +20 .. +40 (n=15), median **+8.49 %**:
```
  -3.15% sam-taylor       90 vs 62.5 g11 pk28    +8.49% will-setterfield 111 vs 80.8 g10 pk5
  +0.56% MAX KONDOGIANNIS 71 vs 36.6 g10 pk36    +8.75% errol-gulden     151 vs 112.6 g10 pk34
  +1.36% wil-dawson       58 vs 33.5 g9  pk22   +12.50% balyn-o-brien     50 vs 26.8 g5 pkNone
  +2.26% nick-bryan       92 vs 66.1 g12 pk37   +12.50% hugo-ralphsmith   82 vs 58.0 g12 pk45
  +6.52% eric-hipwood     80 vs 47.2 g9  pk14   +12.50% joel-hamling      78 vs 51.7 g8  pk41
  +7.32% dayne-zorko     128 vs 102.9 g12 pk38  +12.70% harry-morrison    97 vs 66.3 g12 pk73
  +8.27% xavier-bamert    65 vs 42.8 g9  pk5    +21.00% jack-graham      108 vs 76.6 g12 pk53
                                                +29.55% jay-polkinghorne  71 vs 44.5 g5  pk44
```

## 6c · THE AVAILABILITY REGISTER ON THE LIVE BOARD (context for §2)

32 rows carry an availability haircut; 28 of them have a negative `avail_nerf` (the layer would
have charged them) totalling −4,711 board points. Martin is by a wide margin the largest, at
−1,005 — and the parity guard hands all 1,005 back. The next-worst R23 movers in that group are
`reef-mcinnes` −6.19 % (v=91) and `riley-garcia` −4.76 % (v=80): tiny rows where a point or two
is a large percentage. Martin is the only high-value name in the group with a large move.

## 6d · WHAT THE OWNER IS ACTUALLY LOOKING AT (MOVERS_R23.html, verbatim cells)

```
Nicholas Martin | Fwd     | Essendon         | no  | ·  | 4288 | 4061 | -227 |  -5.3% | 23  -> 27  | pos 5  -> 6
Max Kondogiannis| Def     | Essendon         | yes | 71 |  357 |  359 |   +2 |  +0.6% | 386 -> 385 | pos 94 -> 94
William McCabe  | Key Def | Hawthorn         | no  | ·  |  229 |  230 |   +1 |  +0.4% | 468 -> 472 | pos 42 -> 41
Josh Dolan      | Fwd     | Western Bulldogs | yes | 48 |  280 |  247 |  -33 | -11.8% | 423 -> 454 | pos 97 -> 103
```
Martin is #5 in the TOP 20 VALUE FALLERS and the only DNP row in that list — which is why he was
noticed. McCabe's row shows a **+1**; the "ranked so low" the owner is reacting to is the 472,
which is a level, not a round-23 move.

## 6e · WHAT I DID **NOT** MEASURE (stated so nothing here is over-read)

1. ~~The calendar-vs-pool sub-split of the "global" term.~~ **CLOSED — see §2.1a.** Reached by the
   cheaper route (R23 store + R22 season state, `ws_r23` + `repo_r22`, which loads in 57 s because
   that pairing hits the cached v0 surface) rather than the run that stalled. Season 96 %, pool 4 %
   for Martin; the three terms sum exactly.
2. **Which load-time surface carries the season clock into Martin's price.** REFINED, not closed —
   see §2.1b. `o31_D` reads 1.0 for him on both boards (the stage-5 selection buy-back caps it), so
   the fade is not the channel; and only −30.5 of his −217.4 season term comes through the
   evaluation-time read at all. The remaining −186.9 is in surfaces baked from fE at load. I have
   not identified which one. His `v0_start` moves −0.234 % across the two boards, which is the
   right *kind* of quantity but is not on its own large enough to be the whole −186.9, so there is
   at least one more fE-baked surface involved.
3. **The exact site that produces the interior dip.** PARTIALLY CLOSED — see §6a. The trimmed
   probe (`probe5_kink.py`, Dolan, 0.2-average grid) ran on the idle box and established that the
   dip is a **step structure on a smooth level input**, with bit-identical prices across distinct
   inputs (so: a discrete lookup in the chain), and ruled out `_radq` and `o32_delivered` as the
   switching predicates. The **specific engine site** is still not named. Kondogiannis was not
   re-swept at fine grain; his 14-point grid stands.
   (`probe4_fine.py` — 4 players × 71 points × 8 internals — was the version that never finished;
   it is superseded by `probe5_kink.py` and kept only for the record.)
4. **Whether the §6 non-monotonicity generalises.** Two players swept. The population check in §6
   says the board as a whole is monotone in score-surprise, so this is a local, thin-evidence
   phenomenon — but I have not counted how many rows sit inside such a band.

## 7 · PROVENANCE OF EVERY MEASUREMENT

* store R22 `cc02567f` — `git show b7ec627^:engine/rl_after/rl_model_data.json`
* season state R22 — `git show b7ec627^:data/season_state.json`
* boards `36d5dfc7 / a05fe951 / 5ea978f7 / 1d5c9f7a / 68be10c7` — `git show <commit>:data/rl_build/rl_app_data.json`
* D7B stage boards — `scratchpad/d7bbb/bb_D7B_*/rl_after/rl_app_data.json` (from `docs/evidence/parity_2026-08-19/build_D7B.sh`)
* engine loads — `ws_r22/`, `ws_r23/` (copies), `repo_r22/`, `repo_r23/` (scratch roots)
* probes — `probe_r23.py` (2×2 + internals; run three times, once per load A/B/D), `probe3.py`
  (depth clock + coarse score sweep), `probe5_kink.py` (0.2-average grid across the Dolan trough),
  `probe6_clock.py` (evaluation-time clock isolation via post-load SEASON_FE patch).
  Outputs: `probe_r22_out.json` (load A), `probe_B_r23store_r22season.json` (load B),
  `probe_r23_out.json` (load D), `probe3_r22.json`, `probe3_r23.json`, `probe5_kink.json`,
  `probe6_clock.json`.
  (`probe4_fine.py` never completed under CPU contention and is superseded by `probe5_kink.py`.)

**Two decompositions appear in this file and they are different cuts of the same square — not a
contradiction.** §1's 2×2 holds a player's own scoring row fixed and moves store+season together
("global"); §2.1a moves the whole store first with the season held, then the season. For a player
whose row is byte-identical the two agree exactly. For a player whose row changed they differ,
because §1's "specific" term swaps only *his* row inside one load while §2.1a's `A→B` moves
*everybody's* row at once. Lead with §2.1a for the pool-vs-season question; lead with §1 for the
his-row-vs-everything-else question. Kondogiannis: §1 says global +14.8 / specific −12.6; §2.1a
says row+pool +2.1 / season +0.1. Both are correct answers to different questions.
* every mutation restored and round-trip asserted (`rt=True`, `restored_ok=True`) before the next probe.
* board values reproduced exactly from engine currency ÷ 1.052329 for all 12 probed players.
