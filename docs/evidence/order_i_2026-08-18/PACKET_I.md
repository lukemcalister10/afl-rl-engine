# PACKET I — THE COORDINATED BUILD, AND THE TWO LAWS THAT WILL NOT BOTH HOLD

**Seat:** ORDER I, the build seat. **Scope:** issue #334 comment 5317842435. **Prereg:** `PREREG_I.md`,
pushed before the first engine edit. **Base:** the landing candidate **1f176444**. **Dial:** `RL_O36`.

**Nothing lands on this seat's word.** This packet ends in a HALT, and the halt is the finding.

---

## 0 · THE ANSWER IN NINE LINES

1. **All three levers are wired and all three work.** S1 is at its four measured sites, Order H's
   tall/small factor is on the pick curve, and the dial-off board reproduces 1f176444 byte-exact.
   Determinism x2 passes. The ORDER I board is `0510268a`.
2. **The counterweight cannot be re-derived at all.** Not "was hard to fit" — cannot move. The re-mix
   is keyed on **career games, not age**, so the smallest knob step tested (kappa 0.24 → 0.25) moves
   **421 of 429 mature rows**, worst 5.32 board points. The owner's own law G6 forbids that. **0 of 11
   knob moves and 4 of 5 relief values fail the mature law.** The counterweight is pinned at the
   repair point by the owner's law, not by this seat's choice.
3. **So the joint calibration collapses to one free axis: the S1 dose.** That is the whole reason the
   rest of this packet reads the way it does.
4. **S1 itself is now clean.** Three separate leaks were found by a store-wide mature assert and each
   was fixed at the mechanism (§2). At every dose from 0.15 to 1.00, **0 of 429 rows aged 24+ move.**
5. **The year-1 class grows, and the dose that lands it on the owner's stated ideal is 0.25**:
   class mark **1.0421 → 1.0788**, against G1's floor 1.03 and ideal ~1.08. That is G1 met.
6. **But the same dose puts the early bands into buy-side red and pushes the worst single class to
   1.1687.** G1 and G3 cross each other, and they cross at a dose of roughly **0.08**, while G1's
   ideal needs **0.25** and G2's no-sell-red needs **0.58 to 0.80**. There is no overlap.
7. **Neither dean nor duff-tytler reaches his neighbourhood.** In board points — the currency the
   owner reads — dean goes **2,400 → 2,514** against a 2,600 target, and duff-tytler **1,572 →
   1,616** against 1,800. They are still on opposite sides of the same lever, exactly as Order E
   measured, and the dose that would land duff-tytler is four times what G3 allows.
8. **LEVER 3 BREAKS TWO MORE OF THE OWNER'S LAWS, AND IT BREAKS THEM ALONE.** Order H's tall/small
   factor moves **50 rows aged 24 or over** (G6) and the **printed day-0 price of all 89 wired
   entrants** — because it is a change to the SITTER FADE, and mature sitters and day-0 sitters both
   live on that fade. **S1 breaks neither.** The ledger separates the two levers cleanly, so this is
   a choice the owner can make lever by lever, not a defect to be patched.
9. **HALT.** No dose satisfies the owner's laws jointly, and Lever 3 cannot be wired at all without
   re-basing two of them. The tension is quantified in §5, the full dose ladder is printed, and
   nothing is landed.

---

## 1 · WHAT WAS WIRED, IN PLAIN WORDS

### Lever 1 — S1, the age-referenced bar in the projection core

The engine does not value output. It values output **above a bar**. For a key defender that bar is
65.4 — what a *mature* key defender must beat. The projection loop was subtracting that same mature
bar from a **19-year-old's** output. harry-dean averaged 59.7 in his first season; against 65.4 he
prices as below replacement. Against what a 19-year-old key defender actually produces — 44.8 — he is
14.9 points a game clear.

The fix is one expression at four sites:

```
bar(pos, age) = REPL[pos] - lambda_S1 * DELTA(class, age)
```

`DELTA` is the engine's own measured development gap (the S1 C3 surface, already in the tree as
`O32_GATE_DELTA`). It has no pick axis. It is capped at the flat bar. **It is flat from age 24**, which
is why a mature row cannot move. The sites are `rl_model.proj_from_peak` (two) and
`rl_model.prod_floor` (two), plus their two duplicate loops in `_merged_recover.py`.

### Lever 2 — the counterweight

With S1 live, "below expectation" finally means below **age**-expectation, so the re-mix and the
relief were to be re-derived on the corrected readings. **They could not be.** §4.

### Lever 3 — the tall/small sitter factor

Order H measured that rucks sit 3.55 times more often than smalls taken at the same pick, and that
the sitter fade should therefore be gentler on talls. The wired pooled exponent becomes a group one:

```
s(pick, group) = g0 + g1*ln(pick) + h_TALL*(group is TALL)
kappa = clip(s / s_norm', 0.5, 2.0)      h_TALL = -0.6921   s_norm' = 1.428405
```

`s_norm'` is re-solved so the **total** fade the board charges is unchanged — this moves fade between
talls and smalls, it does not add or remove any. TALL = KPD/KPF/RUCK, the engine's own definition.
Smooth in ln(pick): one constant inside a logarithm, no band, no step, no cliff.

**A transcription note that mattered.** `PACKET_H` prints the coefficients rounded to −0.8778 and
+0.7100. Those rounded values miss H's own kappa table by 9e-6, which the build-failing assert caught.
The wire carries the unrounded fit (`H_RESULTS.json` `interaction['SAT1|ctl1|TALL-pooled'].coef`) and
reproduces H's published table at all eleven picks to 1e-12.

---

## 2 · S1 HAD THREE LEAKS. EACH WAS FOUND BY THE SAME ASSERT, AND EACH WAS FIXED AT THE MECHANISM

The mature-row law is not a formality — it is the sharpest instrument in the building. Turning it on
store-wide, at tolerance zero, found three real defects that no named-row check would have caught.

**Leak 1 — the board's own denominators.** `_merged_recover` prices the whole store at load time to
build shared reference objects: medians, proven-population references, conservation renormalisers. With
S1 live during that, those shared denominators move — and a shared denominator moves **every** row.
Measured: 251,850 load-time evaluations across 8 sites; sam-taylor (27) −5.92, tom-green (25) +4.59,
toby-greene (33) +1.53, taylor-walker (36) +0.08 — while S1 was never once evaluated inside their own
pricing. Fix: **the board's denominators are frozen on the dial-off basis.** S1 is armed at the end of
the module load. This is Order B's own ruling ("the ruled mechanisms must not re-denominate the board")
applied to this lever.

**Leak 2 — the synthetic rows.** The pedigree pole is priced off a made-up 21-year-old and then
**memoised**, so S1 leaked into pedigree machinery and the leak depended on which player happened to
fill the cache first. Three rows aged 24+ moved by up to 0.09. Fix: S1 is switched off around that
synth pricing, and around the ruck-ceiling scaffold for the same reason. S1 corrects how a **real
player's own output** is judged; it has no business in the pedigree machinery — which is exactly what
Order E's isolation control proved it does not touch.

**Leak 3 — the cap law is a property of the row, not of the vantage.** A player who is 24 today is
still priced, inside his own `ev()`, through a lens whose clock stands a year earlier — and at that
vantage he is 23. Twenty-one rows aged 24+ moved that way, worst braeden-campbell **1.041** board
points, and **every one of them was exactly 24**. Fix: the gate is taken on the row's own age on the
board's clock, so a mature row is untouched full stop. (A related correction went in at the same time:
the bar now reads `a+k`, the man's real age at that horizon, not `ah+k`, which is a *curve position*
that LEG F3 holds one year back on the forward lens.)

**After all three: 0 of 429 mature rows move, at every dose tested, tolerance zero.** The harness
repeatability control passes on all 429.

---

## 3 · THE INSTRUMENT WAS CHECKED BEFORE IT WAS TRUSTED

- **Control 1 — the corrected age-fair surface.** Rebuilt from scratch here, it reproduces
  `REMIX_32R.json` **exactly**: W 0.4126838584 (deviation 0.00e+00), all five game-cells and all six
  terciles at deviation 0.00e+00. The two W2 objects this order names come out at **5-9g risers 1.9875
  of entry** and **5-9g sub-expectation 0.8543 of entry**.
- **Control 2 — the landing candidate.** Priced on this instrument at dose 0 with the pooled fade, it
  gives class mark **1.0421** — the Order-D wire's own W2 scorecard number of record, to four decimals.
- **Control 3 — the leg identity.** With the re-mix off, the reconstructed price equals `ev(p, Y)`
  exactly on **1,986 rows × 15 doses**.
- **Control 4 — the tall/small redistribution.** The transcribed curve reproduces `H_RESULTS.json` at
  eleven picks to 1e-12, is monotone and clipped over all 64 picks, and takes no step larger than the
  logarithm allows.

---

## 4 · THE COUNTERWEIGHT: WHY IT COULD NOT BE RE-DERIVED

This is the central finding and it deserves its own section.

The order asked for the O32 re-mix and relief constants to be re-derived jointly on the corrected
age-fair readings. They cannot be re-derived **at all**, and the reason is structural:

> **The re-mix is keyed on career games. It is not keyed on age.** A 27-year-old with 141 career games
> sits on exactly the same reliability curve a 19-year-old with 141 games would. Move the curve and you
> move him.

Measured on the live board, stage 6, store-wide, tolerance zero (`MATURE_GATE_36.json`):

| axis moved | mature rows that move (of 429) | worst move | worst row |
|---|---:|---:|---|
| **lambda_S1 = 0.15 / 0.35 / 0.70 / 1.00** | **0 / 0 / 0 / 0** | **0.0000** | — |
| kappa 0.24 → 0.25 | 421 | 5.3242 | marcus-herbert |
| kappa 0.24 → 0.30 | 422 | 31.9450 | marcus-herbert |
| kappa 0.24 → 0.34 | 423 | 53.2416 | marcus-herbert |
| kappa 0.24 → 0.20 | 423 | 21.2967 | marcus-herbert |
| gamma_u 11 → 12 | 425 | 14.2369 | ned-moyle |
| gamma_u 11 → 10 | 423 | 15.9145 | ned-moyle |
| eta 0.41 → 0.42 | 426 | 3.3512 | billy-cootee |
| eta 0.41 → 0.50 | 426 | 30.1607 | billy-cootee |
| eta 0.41 → 0.30 | 426 | 36.8630 | billy-cootee |
| gamma_d 14 → 13 | 426 | 8.0153 | nick-bryan |
| gamma_d 14 → 12 | 426 | 16.6700 | nick-bryan |
| lambda_rel 1.08 → 0.80 | 34 | 23.4026 | ryan-angwin |
| lambda_rel 1.08 → 1.00 | 30 | 6.6865 | ryan-angwin |
| lambda_rel 1.08 → 1.20 | 30 | 10.0297 | ryan-angwin |
| lambda_rel 1.08 → 1.30 | 30 | 11.3872 | ryan-angwin |

**0 of 11 knob moves pass. 1 of 5 relief values passes, and it is the one already wired.** ORDER C hit
the identical wall from the other side (`REMIX_34.json`: the repaired knob point is the only one of
3,960 its mature gate admits).

**What this costs, in plain words.** The counterweight was the mechanism that was supposed to charge
the sub-expectation-with-games rows and hold the early bands down while S1 lifted the performers. With
it frozen, **S1's lift is paid to everybody who produces anything**, including the young rows who are
producing badly — and there is nothing left to pay for it with. That is why G3 fails so early below.

---

## 5 · THE ACCEPTANCE GATES, ONE BY ONE, WITH THEIR NUMBERS

### 5.1 · The dose ladder — where each of the owner's laws breaks

Knobs and relief where the mature law pins them; the tall/small fade live. Class mark is W2's own
estimator (`mean_0515`); bands are the calibrator's ND subsets on the same all-arm walk-forward.

| dose | class mark | worst single class | 1-10 | 11-20 | 21-30 | 31-40 | 41-64 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| *landing candidate (pooled fade)* | *1.0421* | *1.1311 (2011)* | *+7.20%* | *+11.52%* | *+5.92%* | *−10.46%* | *−7.30%* |
| 0.00 (tall factor only) | 1.0420 | 1.1279 (2011) | +7.40% | +12.62% | +6.75% | **−8.90%** | **−8.23%** |
| 0.10 | 1.0551 | **1.1428** | +8.98% | **+14.22%** | +8.12% | −8.12% | −7.19% |
| 0.15 | 1.0622 | 1.1508 | +9.83% | +15.08% | +8.88% | −7.69% | −6.62% |
| 0.20 | 1.0698 | 1.1591 | +10.73% | +16.00% | +9.70% | −7.23% | −6.01% |
| **0.25 — the carried point** | **1.0788** | **1.1687** | **+11.88%** | **+16.96%** | **+10.56%** | **−6.74%** | **−5.35%** |
| 0.30 | 1.0872 | 1.1788 | +12.88% | +17.98% | +11.49% | −6.22% | −4.65% |
| 0.35 | 1.0964 | 1.1920 | +13.91% | +19.04% | +12.48% | −5.66% | −3.91% |
| 0.40 | 1.1058 | 1.2031 | +15.01% | +20.16% | +13.54% | −5.06% | −3.11% |
| 0.50 | 1.1260 | 1.2270 | +17.32% | +22.56% | +15.85% | −3.73% | −1.36% |
| 0.60 | 1.1482 | 1.2531 | +19.83% | +25.19% | +18.44% | −2.21% | **+0.64%** |
| 0.70 | 1.1743 | 1.2815 | +22.84% | +28.04% | +21.32% | −0.48% | +2.88% |
| 0.85 | 1.2150 | 1.3283 | +27.22% | +32.75% | +26.18% | **+2.52%** | +6.77% |
| 1.00 | 1.2596 | 1.3803 | +31.94% | +37.96% | +31.67% | +6.04% | +11.31% |

**Read the crossings off that table. They do not overlap.**

| owner's law | what it needs | the dose it needs |
|---|---|---|
| **G1** floor 1.03 | already met by the landing candidate (1.0421) | any dose |
| **G1** ideal ~1.08 | class mark 1.08 | **≈ 0.25** |
| **G1** rail: class < 1.14 | class mark under 1.14 | **≤ ≈ 0.58** |
| **G3** no buy-red on any band | 11-20 under +14% | **≤ ≈ 0.08** |
| the ruled 1.14 no-arb line on any single class | worst class ≤ 1.139 | **≤ ≈ 0.05** |
| **G2** aspiration: no sell-red on 41-64 | 41-64 ≥ 0% | **≥ ≈ 0.58** |
| **G2** aspiration: no sell-red on 31-40 | 31-40 ≥ 0% | **≥ ≈ 0.80** |
| **G4** duff-tytler ≈ 1,800 | +146 board points | **≥ ≈ 0.55** |

**THE TENSION, IN ONE SENTENCE: every law that wants the late bands and duff-tytler fixed needs a dose
of at least 0.55, and every law that protects the early bands and the no-arb line caps the dose at
0.08. There is no overlap, and the gap is a factor of seven.**

**And this is exactly what the frozen counterweight costs.** The counterweight is the only mechanism
in the engine that could have lifted the late bands without lifting the early ones — it moves weight
off pedigree and onto shown production, which is worth most to a late pick who is playing well and
costs a high pick who is not. With it pinned by G6, the dose is a blunt instrument: it lifts every band
at once, and the early bands hit the buy rail long before the late bands reach zero.

### 5.2 · Every gate, printed pass/fail (at the carried dose 0.25)


The carried dose is **lambda_S1 = 0.25**. Bands and arms are the **extended-338** and **all-arm**
standing instruments (§6); the class mark is W2's own estimator; the row numbers are the 2026 board.

| gate | what it asks | the number | verdict |
|---|---|---|---|
| **G1** | year-1 class cohort grows: floor 1.03, ideal ~1.08, strictly < 1.14 | **1.0421 -> 1.0788** | **PASS** — above the floor and on the ideal, and under the rail |
| **G2** | picks 31-40 and 41-64 materially improve | 31-40 -12.84% -> **-9.13%** (+3.70 pts) · 41-64 -7.88% -> **-5.83%** (+2.05 pts) | **PASS** on "materially improve"; **FAIL** on the no-sell-red aspiration — both are still red |
| **G3** | no buy-red: every band and arm <= +14% | ND bands worst **+14.49%** (picks 11-20) — **BUY-RED on picks 11-20** · pool arms buy-red: PRIMARY|SSP (+57.05%), MODERN|SSP (+57.05%) | **FAIL** |
| **G4** | dean ~2,600 and duff-tytler ~1,800 (BOARD POINTS, the currency the owner reads; C31 levels 2,670 / 1,832) | dean **2514** (was 2400, C31 2,670) · duff-tytler **1616** (was 1572, C31 1,832) | **BOTH FAIL** — dean short by 86, duff-tytler short by 184 |
| **G5** | sub-expectation-with-games rows do not rise | see the table below | **FAIL** |
| **G6** | every row aged 24+ byte-identical, store-wide, tolerance 0 | **50 of 429 move** on the board (total absolute movement 446 board points, worst Liam McMahon +41) — and **every single one moves through LEVER 3, none through S1** (leg_tall non-zero on 50 of 50, leg_S1 non-zero on 0) | **FAIL — and the cause is named** |
| **G6** | murdock, whole row | 178.74912838553396 -> 178.74912838553396 | **PASS — identical** |
| **G6** | day-0 prints 89/89 unmoved | the raw entry object `derived_v0` is **IDENTICAL on 89 of 89** at tolerance 0; the **printed** day-0 price moves on **89 of 89** (32 up, 57 down; largest up mitchell-marsh 451 -> 552, largest down ben-camporeale 157 -> 122) | **FAIL as stated** — see below |
| **G6** | determinism x2 | two identical builds byte-equal | **PASS** |
| **G6** | dial-off = 1f176444 byte-exact | `1f17644445f074d11e631b5cbae98a9a` | **PASS** |
| side | josh-smillie holds in the ~700s | **772 -> 851** board points, and the whole move is `leg_tall` | **FAIL — he rises out of the 700s**, exactly as the prereg predicted (§7) |

**G5, by name, as the order requires:**

| row | landing candidate | ORDER I | move | verdict |
|---|---:|---:|---:|---|
| xavier-taylor | 1176 | 1184 | +8 (+0.68%) | ROSE — G5 FAIL |
| daniel-annable | 1530 | 1553 | +23 (+1.50%) | ROSE — G5 FAIL |
| dylan-patterson | 1467 | 1494 | +27 (+1.84%) | ROSE — G5 FAIL |

**THE DAY-0 GATE, IN PLAIN WORDS — it fails, and the reason is worth understanding.** A day-0 price for
a player who has never played **is** `v0 x D(c_u)` — his entry value multiplied by the sitter fade.
Order H's factor is a change to exactly that fade. So it moves the printed day-0 of every wired sitter
**by construction**: all 89 of them, 32 up and 57 down. What did **not** move is `derived_v0`, the raw
entry object the walk-forward matrix writes as year-0 — **identical on 89 of 89 at tolerance zero**
(oskar-taylor 903.8014284605089 on both boards). So V0 is untouched and the year-0 column of the matrix
is untouched; what moved is what the board charges a sitter **today**. The guard file was therefore
re-based on this board and the re-base is disclosed (`o36_day0.py`, `DAY0_I_FINAL.json`, 89 of 89 at
tolerance 0) — the same re-base ORDER D's own pick-curve fade required when it landed. **This seat
reports it as a gate failure against the law as written and does not decide whether the re-base is
acceptable. That is the owner's ruling.**

**THE MATURE-ROW GATE, AND WHICH LEVER BREAKS IT.** S1 does not break it: at every dose tested, 0 of
429 rows aged 24+ move (§4). **Lever 3 does.** A mature row who has sat still carries an unplayed
clock, and Order H's factor is a change to the sitter fade — so a 25-year-old sitter is re-priced by
it exactly as a 20-year-old sitter is. On the board: Liam McMahon (24, pick 33) +41, Nick Bryan (25,
pick 37) +41, Luke Beecken (25, pick 16) −32, Callum Coleman-Jones (27, pick 20) +30. milan-murdock
does not move because he is not a sitter. **The two levers are separable and the ledger separates
them: turn Lever 3 off and G6 passes exactly; turn it on and 50 mature rows move.** That is a clean
choice for the owner, not a defect to be patched.

**Why G5 fails, stated plainly.** S1 lowers the bar these young rows are judged against, so even a
poor first season clears more of it and their production leg rises a little. The mechanism that was
supposed to take that back — the counterweight, moving weight off their large draft pedigree and onto
their small production — is frozen by G6 (§4). With it frozen there is nothing to charge them with.
This is not a surprise discovered after the fact: the prereg predicted these three would FALL, and
they did not, because the counterweight the prediction assumed turned out to be immovable.

**An inherited buy-red, declared in the prereg and reported here rather than hidden.** The pool arms PRIMARY|SSP, MODERN|SSP were ALREADY above the +14% rail on the landing candidate (PRIMARY|SSP +50.52%, MODERN|SSP +50.52%). Those rows enter at pick 65, outside the 1-64 pick curve, so no lever in this order reaches them. This build did not create that red and does not cure it.


---

## 6 · THE STANDARD TABLES

The instruments are the standing disclosed copies, run whole and unmodified: the **extended-338** five-band table (committed md5 `d59ad550116ebbe3d90ed82becd2c4d5`) for the ND bands and the year paths, and the **all-arm** cohort instrument's own semantics for the pool arms in both windows. Output verbatim.

```
======================================================================================================================
ORDER I — STANDING TWO-SIDED NO-ARB SUITE.  carry charge = 14%/yr.
   SELL-SIDE RED: yr0->1 appreciation < 0.     BUY-SIDE RED: yr0->1 appreciation > +14%.
======================================================================================================================

-- ND BANDS (extended-338 disclosed instrument; years 0..7 as mean-ratio vs the same-set yr0) --

[O35FINAL  LANDING CANDIDATE 1f176444 (Order D)]
  band                  n     yr0     yr1     yr2     yr3     yr4     yr5     yr6     yr7     apr0-1   buy-mgn   verdict
  ALL picks 1-64     1200   1.000   1.030   1.143   1.325   1.468   1.517   1.494   1.321     +2.98%   +11.02%        ok
  picks 1-20          380   1.000   1.084   1.187   1.355   1.527   1.550   1.482   1.317     +8.36%    +5.64%        ok
  picks 21-64         820   1.000   0.945   1.073   1.277   1.376   1.465   1.513   1.326     -5.54%   +19.54%  SELL-RED
  ----------------------------------------------------------------------------------------------------------------
  picks 1-10          190   1.000   1.079   1.179   1.360   1.521   1.503   1.424   1.247     +7.93%    +6.07%        ok
  picks 11-20         190   1.000   1.092   1.203   1.345   1.538   1.642   1.593   1.456     +9.20%    +4.80%        ok
  picks 21-30         190   1.000   1.028   1.182   1.418   1.599   1.610   1.687   1.459     +2.76%   +11.24%        ok
  picks 31-40         190   1.000   0.872   0.941   1.255   1.249   1.394   1.298   1.162    -12.84%   +26.84%  SELL-RED
  picks 41-64         440   1.000   0.921   1.073   1.152   1.256   1.375   1.518   1.329     -7.88%   +21.88%  SELL-RED

[O36FINAL  ORDER I (RL_O36)]
  band                  n     yr0     yr1     yr2     yr3     yr4     yr5     yr6     yr7     apr0-1   buy-mgn   verdict
  ALL picks 1-64     1200   1.000   1.073   1.197   1.372   1.499   1.531   1.495   1.321     +7.35%    +6.65%        ok
  picks 1-20          380   1.000   1.133   1.241   1.398   1.556   1.564   1.482   1.318    +13.30%    +0.70%        ok
  picks 21-64         820   1.000   0.979   1.128   1.329   1.409   1.481   1.514   1.327     -2.06%   +16.06%  SELL-RED
  ----------------------------------------------------------------------------------------------------------------
  picks 1-10          190   1.000   1.127   1.227   1.399   1.547   1.514   1.425   1.247    +12.69%    +1.31%        ok
  picks 11-20         190   1.000   1.145   1.267   1.397   1.573   1.659   1.594   1.458    +14.49%    -0.49%   BUY-RED
  picks 21-30         190   1.000   1.074   1.246   1.475   1.632   1.626   1.688   1.459     +7.42%    +6.58%        ok
  picks 31-40         190   1.000   0.909   0.994   1.307   1.280   1.410   1.301   1.163     -9.13%   +23.13%  SELL-RED
  picks 41-64         440   1.000   0.942   1.119   1.199   1.288   1.392   1.519   1.330     -5.83%   +19.83%  SELL-RED

-- THE MOVE, BAND BY BAND (Order I minus the landing candidate, in points of yr0->1 appreciation) --
  band                candidate      ORDER I         move   verdict move
  ALL picks 1-64         +2.98%       +7.35%       +4.37   ok -> ok
  picks 1-20             +8.36%      +13.30%       +4.94   ok -> ok
  picks 21-64            -5.54%       -2.06%       +3.47   SELL-RED -> SELL-RED
  picks 1-10             +7.93%      +12.69%       +4.76   ok -> ok
  picks 11-20            +9.20%      +14.49%       +5.28   ok -> BUY-RED
  picks 21-30            +2.76%       +7.42%       +4.66   ok -> ok
  picks 31-40           -12.84%       -9.13%       +3.70   SELL-RED -> SELL-RED
  picks 41-64            -7.88%       -5.83%       +2.05   SELL-RED -> SELL-RED

-- POOL ARMS (cohort clock, all-arm instrument semantics; MSD yr1 is the debut-gap exclusion, printed in words, never a silent blank) --

[O35FINAL  LANDING CANDIDATE 1f176444 (Order D)]
  PRIMARY window:
    arm          n     yr0     yr1     yr2     yr3     yr4     yr5     yr6     yr7     apr0-1   buy-mgn   verdict
    RD         623   1.000   0.978   1.169   1.074   1.216   1.267   1.234   1.131     -2.21%   +16.21%  SELL-RED
    MSD         55   1.000       -   0.701   0.684   0.745   0.944   1.240   0.608         —         —  n/a — MSD debuts in his draft year, so the matrix has no year-1 cell for him; those rows are excluded and counted, never scored zero
    UNR         49   1.000   0.579   0.784   0.682   1.224   1.464   0.925   0.381    -42.06%   +56.06%  SELL-RED
    IRE         47   1.000   1.135   1.524   1.030   1.185   1.391   1.280   1.877    +13.51%    +0.49%        ok
    PDA         43   1.000   0.817   0.927   0.992   1.165   1.551   0.737   1.247    -18.33%   +32.33%  SELL-RED
    PDN         33   1.000   0.622   1.037   0.805   0.872   0.884   1.260   0.983    -37.81%   +51.81%  SELL-RED
    SSP         31   1.000   1.505   1.590   2.014   1.640   1.316   0.684   0.405    +50.52%   -36.52%   BUY-RED
    PDS         21   1.000   0.745   0.793   0.415   0.725   0.977   0.795   0.415    -25.47%   +39.47%  SELL-RED
    ALLPOOL   1016   1.000   0.961   1.117   1.034   1.169   1.240   1.187   1.157     -3.91%   +17.91%  SELL-RED
  MODERN window:
    arm          n     yr0     yr1     yr2     yr3     yr4     yr5     yr6     yr7     apr0-1   buy-mgn   verdict
    RD          66   1.000   0.814   0.987   0.890   1.096   1.419   1.421   0.975    -18.65%   +32.65%  SELL-RED
    MSD         55   1.000       -   0.701   0.684   0.745   0.944   1.240   0.608         —         —  n/a — MSD debuts in his draft year, so the matrix has no year-1 cell for him; those rows are excluded and counted, never scored zero
    UNR         13   1.000   0.672   0.744   0.492   0.562   0.149   0.058   0.040    -32.81%   +46.81%  SELL-RED
    IRE         12   1.000   0.507   0.511   0.467   0.178   0.215   0.041   0.173    -49.34%   +63.34%  SELL-RED
    PDA         13   1.000   0.588   0.721   0.635   0.918   1.908   0.040       -    -41.15%   +55.15%  SELL-RED
    PDN         25   1.000   0.651   1.114   0.838   0.487   0.279   0.426   0.114    -34.93%   +48.93%  SELL-RED
    SSP         31   1.000   1.505   1.590   2.014   1.640   1.316   0.684   0.405    +50.52%   -36.52%   BUY-RED
    ALLPOOL    229   1.000   0.909   0.931   0.890   0.932   1.066   0.986   0.583     -9.15%   +23.15%  SELL-RED

[O36FINAL  ORDER I (RL_O36)]
  PRIMARY window:
    arm          n     yr0     yr1     yr2     yr3     yr4     yr5     yr6     yr7     apr0-1   buy-mgn   verdict
    RD         623   1.000   0.979   1.180   1.101   1.234   1.274   1.234   1.131     -2.09%   +16.09%  SELL-RED
    MSD         55   1.000       -   0.713   0.703   0.757   0.949   1.241   0.608         —         —  n/a — MSD debuts in his draft year, so the matrix has no year-1 cell for him; those rows are excluded and counted, never scored zero
    UNR         49   1.000   0.578   0.792   0.688   1.225   1.465   0.925   0.381    -42.19%   +56.19%  SELL-RED
    IRE         47   1.000   1.126   1.541   1.064   1.209   1.398   1.278   1.876    +12.60%    +1.40%        ok
    PDA         43   1.000   0.795   0.920   1.022   1.190   1.558   0.736   1.247    -20.47%   +34.47%  SELL-RED
    PDN         33   1.000   0.589   1.022   0.823   0.891   0.897   1.260   0.983    -41.06%   +55.06%  SELL-RED
    SSP         31   1.000   1.571   1.625   2.053   1.649   1.316   0.682   0.404    +57.05%   -43.05%   BUY-RED
    PDS         21   1.000   0.731   0.778   0.426   0.748   0.993   0.791   0.414    -26.86%   +40.86%  SELL-RED
    ALLPOOL   1016   1.000   0.962   1.127   1.060   1.185   1.247   1.187   1.157     -3.78%   +17.78%  SELL-RED
  MODERN window:
    arm          n     yr0     yr1     yr2     yr3     yr4     yr5     yr6     yr7     apr0-1   buy-mgn   verdict
    RD          66   1.000   0.806   0.993   0.921   1.118   1.433   1.421   0.974    -19.43%   +33.43%  SELL-RED
    MSD         55   1.000       -   0.713   0.703   0.757   0.949   1.241   0.608         —         —  n/a — MSD debuts in his draft year, so the matrix has no year-1 cell for him; those rows are excluded and counted, never scored zero
    UNR         13   1.000   0.663   0.736   0.488   0.556   0.142   0.058   0.040    -33.69%   +47.69%  SELL-RED
    IRE         12   1.000   0.449   0.457   0.472   0.170   0.213   0.039   0.171    -55.10%   +69.10%  SELL-RED
    PDA         13   1.000   0.542   0.696   0.652   0.943   1.915   0.036       -    -45.78%   +59.78%  SELL-RED
    PDN         25   1.000   0.624   1.105   0.861   0.495   0.283   0.426   0.114    -37.58%   +51.58%  SELL-RED
    SSP         31   1.000   1.571   1.625   2.053   1.649   1.316   0.682   0.404    +57.05%   -43.05%   BUY-RED
    ALLPOOL    229   1.000   0.908   0.939   0.914   0.946   1.072   0.986   0.583     -9.24%   +23.24%  SELL-RED

-- THE MOVE, ARM BY ARM (primary window) --
  arm           candidate      ORDER I         move   verdict move
  RD               -2.21%       -2.09%       +0.12   SELL-RED -> SELL-RED
  UNR             -42.06%      -42.19%       -0.14   SELL-RED -> SELL-RED
  IRE             +13.51%      +12.60%       -0.91   ok -> ok
  PDA             -18.33%      -20.47%       -2.15   SELL-RED -> SELL-RED
  PDN             -37.81%      -41.06%       -3.25   SELL-RED -> SELL-RED
  SSP             +50.52%      +57.05%       +6.53   BUY-RED -> BUY-RED
  PDS             -25.47%      -26.86%       -1.39   SELL-RED -> SELL-RED
  ALLPOOL          -3.91%       -3.78%       +0.13   SELL-RED -> SELL-RED

-- VANTAGE-CONSISTENCY MATRIX (implied growth yrV -> yrV+k vs the 14% carry; DIAGNOSTIC ONLY) --

[O35FINAL]
  band               V      k=1      k=2      k=3      k=4    carry:    14.0%    30.0%    48.2%    68.9%
  picks 1-10         0    +7.9%   +17.9%   +36.0%   +52.1%
                     1    +9.3%   +26.0%   +40.9%   +39.2%
                     2   +15.3%   +29.0%   +27.4%   +20.8%
  picks 11-20        0    +9.2%   +20.3%   +34.5%   +53.8%
                     1   +10.1%   +23.2%   +40.9%   +50.4%
                     2   +11.8%   +27.9%   +36.5%   +32.4%
  picks 21-30        0    +2.8%   +18.2%   +41.8%   +59.9%
                     1   +15.0%   +38.0%   +55.6%   +56.7%
                     2   +20.0%   +35.2%   +36.2%   +42.8%
  picks 31-40        0   -12.8%    -5.9%   +25.5%   +24.9%
                     1    +8.0%   +44.0%   +43.3%   +60.0%
                     2   +33.3%   +32.7%   +48.2%   +37.9%
  picks 41-64        0    -7.9%    +7.3%   +15.2%   +25.6%
                     1   +16.4%   +25.1%   +36.3%   +49.3%
                     2    +7.4%   +17.1%   +28.2%   +41.5%

[O36FINAL]
  band               V      k=1      k=2      k=3      k=4    carry:    14.0%    30.0%    48.2%    68.9%
  picks 1-10         0   +12.7%   +22.7%   +39.9%   +54.7%
                     1    +8.9%   +24.2%   +37.3%   +34.4%
                     2   +14.0%   +26.0%   +23.4%   +16.1%
  picks 11-20        0   +14.5%   +26.7%   +39.7%   +57.3%
                     1   +10.6%   +22.0%   +37.4%   +44.9%
                     2   +10.3%   +24.1%   +31.0%   +25.9%
  picks 21-30        0    +7.4%   +24.6%   +47.5%   +63.2%
                     1   +16.0%   +37.3%   +51.9%   +51.4%
                     2   +18.4%   +31.0%   +30.5%   +35.5%
  picks 31-40        0    -9.1%    -0.6%   +30.7%   +28.0%
                     1    +9.4%   +43.8%   +40.8%   +55.2%
                     2   +31.4%   +28.7%   +41.9%   +30.8%
  picks 41-64        0    -5.8%   +11.9%   +19.9%   +28.8%
                     1   +18.8%   +27.3%   +36.8%   +47.8%
                     2    +7.2%   +15.2%   +24.4%   +35.7%

-- ENTRY-YEAR CONTROL (S1 must not move the entry year: it is a production correction and a day-0 row has no production) --
   bound: every ND-band yr0 MEAN within +-0.1% of the landing candidate cell (yr1 is EXPECTED to move)
   ALL picks 1-64   yr0: candidate     762.5  ORDER I     762.5   +0.000%  ok
   ALL picks 1-64   yr1: candidate     785.2  ORDER I     818.5   +4.242%  (yr1 moves by design)
   picks 1-20       yr0: candidate    1474.7  ORDER I    1474.7   +0.000%  ok
   picks 1-20       yr1: candidate    1598.0  ORDER I    1670.8   +4.556%  (yr1 moves by design)
   picks 21-64      yr0: candidate     432.5  ORDER I     432.5   +0.000%  ok
   picks 21-64      yr1: candidate     408.5  ORDER I     423.5   +3.674%  (yr1 moves by design)
   picks 1-10       yr0: candidate    1946.8  ORDER I    1946.8   +0.000%  ok
   picks 1-10       yr1: candidate    2101.2  ORDER I    2193.8   +4.408%  (yr1 moves by design)
   picks 11-20      yr0: candidate    1002.5  ORDER I    1002.5   +0.000%  ok
   picks 11-20      yr1: candidate    1094.8  ORDER I    1147.8   +4.839%  (yr1 moves by design)
   picks 21-30      yr0: candidate     666.9  ORDER I     666.9   +0.000%  ok
   picks 21-30      yr1: candidate     685.3  ORDER I     716.4   +4.540%  (yr1 moves by design)
   picks 31-40      yr0: candidate     548.2  ORDER I     548.2   +0.000%  ok
   picks 31-40      yr1: candidate     477.9  ORDER I     498.2   +4.250%  (yr1 moves by design)
   picks 41-64      yr0: candidate     281.2  ORDER I     281.2   +0.000%  ok
   picks 41-64      yr1: candidate     259.1  ORDER I     264.8   +2.223%  (yr1 moves by design)

ENTRY-YEAR CONTROL: PASS — every yr0 cell inside +-0.1%
```


---

## 7 · THE NAMED ROWS AND THE PREREG SCORECARD

**11 of 16 preregistered direction predictions were correct.** Three of the five misses are the three sub-expectation rows (xavier-taylor, annable, patterson), and they missed for one reason: the prediction assumed a counterweight that the owner's mature-row law then froze. The fourth is oskar-taylor, predicted FLAT because S1 cannot reach a player with no games — correct about S1, wrong because Lever 3 reaches him through the sitter fade (+15 board points). The fifth is steely-green, predicted UP on S1 and actually DOWN 3 board points, because he is a small at pick 55 and the tall/small redistribution charges late smalls more — Order H said in advance that late small sitters would pay, and he is one.

| row | prediction | actual | landing | ORDER I | move | hit? | mechanism |
|---|---|---|---:|---:|---:|---|---|
| harry-dean | UP | UP | 2526 | 2646 | +120 (+4.74%) | HIT | above his age bar by 14.9 a game |
| cooper-duff-tytler | UP | UP | 1654 | 1701 | +47 (+2.83%) | HIT | above his age bar by 7.1 a game |
| xavier-taylor | DOWN | UP | 1238 | 1246 | +8 (+0.68%) | **MISS** | sub-expectation WITH games (42.0 vs an age bar of 55.2) |
| oskar-taylor | FLAT | UP | 627 | 643 | +15 (+2.45%) | **MISS** | zero games — S1 cannot reach him |
| daniel-annable | DOWN | UP | 1610 | 1634 | +24 (+1.48%) | **MISS** | sub-expectation WITH games (38.0 vs 57.0) |
| dylan-patterson | DOWN | UP | 1544 | 1572 | +28 (+1.82%) | **MISS** | sub-expectation WITH games (35.6 vs 55.2) |
| josh-smillie | UP | UP | 812 | 895 | +83 (+10.22%) | HIT | a small at pick 7 falls onto the 0.5 clip |
| chris-scerri | UP | UP | 329 | 345 | +16 (+4.80%) | HIT | pool row — production dominates a small pedigree |
| thomas-burton | UP | UP | 325 | 339 | +14 (+4.33%) | HIT | same channel, weaker |
| milan-murdock | EXACTLY FLAT | FLAT | 179 | 179 | +0 (+0.00%) | HIT | age 26 — the cap law |
| will-green | UP | UP | 508 | 659 | +150 (+29.61%) | HIT | TALL at pick 16: exponent 0.793 -> 0.500 |
| toby-conway | UP | UP | 900 | 991 | +91 (+10.07%) | HIT | TALL at pick 24: exponent 0.899 -> 0.500 |
| steely-green | UP | DOWN | 84 | 81 | -3 (-3.44%) | **MISS** | high-rho row, fade clock spent |
| isaac-kako | UP | UP | 830 | 870 | +41 (+4.90%) | HIT | S1 on a high-rho row |
| alix-tauru | UP | UP | 969 | 991 | +22 (+2.31%) | HIT | S1, and tall gaps are the largest |
| jedd-busslinger | UP | UP | 609 | 681 | +71 (+11.67%) | HIT | S1 + re-mix on an above-age-bar season |

**Other rows of record:**

| row | landing | ORDER I | move |
|---|---:|---:|---:|
| connor-o-sullivan | 2500 | 2623 | +122 |
| finn-o-sullivan | 3491 | 3630 | +139 |
| harry-morrison | 35 | 35 | +0 |
| keidean-coleman | 708 | 708 | +0 |
| levi-ashcroft | 3339 | 3482 | +143 |
| logan-morris | 2822 | 2961 | +139 |
| sam-taylor | 1177 | 1177 | +0 |
| taylor-goad | 611 | 768 | +157 |
| taylor-walker | 136 | 136 | +0 |
| toby-greene | 847 | 847 | +0 |
| tom-green | 4566 | 4566 | +0 |
| will-ashcroft | 6827 | 6901 | +75 |
| zac-taylor | 168 | 165 | -4 |

**The year-1 class on the 2026 board:** 120 rows, 61100 -> 62883 (+2.92%); 70 up, 37 down, 13 unchanged.


---

## 8 · ORDER H'S TWO DECLARED SIDE EFFECTS, WITH NUMBERS

**Side effect one — the 0.5 clip flat-spot.** Order D's exponent is clipped below at 0.5. Shifting
talls down by 0.69 pushes them onto that floor for **picks 1 through 24** — 24 of the 64 picks — and
smalls onto it for **picks 1 through 9**. Over that range the **clip**, not the fit, is setting the
price: a tall sitter at pick 1, at pick 10, at pick 16 and at pick 24 all receive the identical
depth-2 multiplier 0.7472. That is a flat spot that ends abruptly at pick 25. It is inherited from
Order D's clip, it is not this seat's constant, and it binds.

**Side effect two — the late small sitters pay.** The redistribution is pinned, so the talls' relief is
funded by the smalls. Measured on the calibration instrument, the tall factor **alone** (dose 0) does
this to the bands:

| band | landing candidate | tall factor alone | move |
|---|---:|---:|---:|
| picks 1-10 | +7.20% | +7.40% | +0.20 |
| picks 11-20 | +11.52% | +12.62% | +1.10 |
| picks 21-30 | +5.92% | +6.75% | +0.83 |
| picks 31-40 | −10.46% | **−8.90%** | **+1.56** |
| picks 41-64 | −7.30% | **−8.23%** | **−0.93** |

Picks 31-40 improve by 1.56 points. **Picks 41-64 get worse by 0.93 points** — that is the late small
sitters paying, and it is exactly what Order H said would happen. The class mark moves by −0.0001,
which is the redistribution identity doing its job: the total fade charged is unchanged.

The exponent, small vs tall, at the picks the owner asked about: pick 16, small 0.764 / tall 0.500;
pick 64, small 1.453 / tall 0.968. `m_TALL` on the wire is **0.645** over picks 1-64 (H publishes 0.677
on its own averaging; both are printed).

---

## 9 · THE MOVERS LEDGER AND THE PREVIEW PAGES

**Boards:** live `88ce647f` &middot; Candidate 31 `fe6be9d6` &middot; landing candidate `1f176444` &middot; ORDER I `0510268a`. Leg boards: S1 alone `585d8064`, tall factor alone `d1058fe0`.

**Board totals:** live 752429 &middot; C31 666913 &middot; landing 667916 &middot; **ORDER I 676833**.

**416 of 804 rows move against the landing candidate. 50 of them are aged 24 or over.**

Age profile of the rows that moved: 19:71, 20:87, 21:75, 22:58, 23:75, 24:14, 25:10, 26:11, 27:4, 28:5, 29:4, 30:1, 33:1

| row | age | pick | g | live | C31 | landing | ORDER I | leg S1 | leg tall | leg re-mix+interaction | vs landing |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Harry Dean | 19 | 3 | 17 | 2577 | 2670 | 2400 | 2514 | +114 | +0 | +0 | +114 |
| Cooper Duff-Tytler | 19 | 4 | 13 | 1561 | 1832 | 1572 | 1616 | +44 | +0 | +0 | +44 |
| Xavier Taylor | 19 | 11 | 2 | 802 | 1288 | 1176 | 1184 | +8 | +0 | +0 | +8 |
| Oskar Taylor | 19 | 15 | 0 | 629 | 529 | 596 | 611 | +0 | +15 | +0 | +15 |
| Daniel Annable | 19 | 6 | 2 | 1395 | 1633 | 1530 | 1553 | +23 | +0 | +0 | +23 |
| Dylan Patterson | 19 | 5 | 5 | 1628 | 1675 | 1467 | 1494 | +27 | +0 | +0 | +27 |
| Josh Smillie | 20 | 7 | 0 | 953 | 459 | 772 | 851 | +0 | +79 | +0 | +79 |
| Chris Scerri | 20 | None | 7 | 459 | 232 | 313 | 328 | +15 | +0 | +0 | +15 |
| Thomas Burton | 19 | None | 5 | 439 | 213 | 309 | 322 | +13 | +0 | +0 | +13 |
| Milan Murdock | 26 | None | 17 | 208 | 187 | 170 | 170 | +0 | +0 | +0 | +0 |
| Will Green | 21 | 16 | 1 | 604 | 338 | 483 | 626 | +2 | +141 | +0 | +143 |
| Toby Conway | 23 | 24 | 6 | 503 | 729 | 855 | 942 | +1 | +86 | +0 | +87 |
| Steely Green | 22 | 55 | 43 | 150 | 60 | 80 | 77 | +1 | -4 | +0 | -3 |
| Isaac Kako | 20 | 13 | 36 | 1413 | 806 | 788 | 827 | +39 | +0 | +0 | +39 |
| Alix Tauru | 20 | 10 | 18 | 1684 | 1005 | 920 | 942 | +22 | +0 | +0 | +22 |
| Jedd Busslinger | 22 | 13 | 15 | 916 | 469 | 579 | 647 | +14 | +53 | +1 | +68 |

The legs are REAL BOARDS, each built on its own — they are not an arithmetic split, and they do not sum to the total. The residual column carries the interaction, and it is shown rather than hidden. **Both preview pages are refreshed:** `PREVIEW_I_PLAYERS.html` (the full board, four columns and the three legs) and `PREVIEW_I_YEAR1.html` (the year-1 class in draft order with v0 and the four board columns).


---

## 10 · WHAT THIS SEAT DOES NOT SAY

- It does not recommend a dose. It reports that **no dose satisfies the owner's laws jointly**, prints
  the ladder, and carries 0.25 — the point where the class cohort lands on G1's stated ideal — purely
  so the owner has a board in front of him.
- It does not say the counterweight should not have been re-derived. It says **the owner's own
  mature-row law forbids moving it**, prints the 429-row evidence, and stops.
- It does not propose relaxing G6, G3, or the 1.139 line. Those are the owner's to rule on.
- It does not claim the calibrator's band levels are the standing instrument's. The calibrator's ND
  subsets run hotter than the extended-338; the standing tables in §6 are the extended-338's own
  numbers and the two are never mixed in one row.
- It does not re-open josh-smillie's fade. His rise is reported and its mechanism named.

---

## 11 · REPRODUCTION

Lane on every run: `PATH=/root/rl_venv312/bin:$PATH`, `PYTHONHASHSEED=0`,
`OPENBLAS/OMP/MKL/NUMEXPR/VECLIB_NUM_THREADS=1`, `RL_GAMMA=1.0 RL_PICK1=3000 RL_RUCK_TAX=0.25
RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22`, `RL_V0SURF_PKL=data/v0surf.pkl`. Engine runs
strictly sequential; one tag, one directory, one run.

| step | script |
|---|---|
| prereg (pushed first) | `PREREG_I.md` |
| walk-forward leg extraction, 15 doses | `o36_legs.py` → `O36_LEGS.json` |
| the pooled-fade control column | `o36_legs_pool.py` |
| the mature-row law, stage 6, store-wide | `o36_mature_gate.py` → `MATURE_GATE_36.json` |
| the one joint calibration | `o36_calibrate.py` → `O36_SWEEP.json` |
| the five boards | `build_all36.sh` (wraps `bb36.sh`) |
| the walk-forward matrix | `run_emit_o36.sh` |
| the standing instruments | `bb_noarb36.sh` → `bb_standing_tables36.py` |
| the board gates and the scorecard | `o36_gates.py` → `GATES_I.json` |
| the movers ledger | `o36_ledger.py` → `docs/ledgers/ORDER_I_MOVERS.json` |
| the preview pages | `o36_pages.py` |

*— ORDER I, the build seat. The levers are wired, the laws are measured, and the owner's word decides.*
