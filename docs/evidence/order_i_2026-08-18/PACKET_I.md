# PACKET I — THE COORDINATED BUILD, AND THE TWO LAWS THAT WILL NOT BOTH HOLD

**Seat:** ORDER I, the build seat. **Scope:** issue #334 comment 5317842435. **Prereg:** `PREREG_I.md`,
pushed before the first engine edit. **Base:** the landing candidate **1f176444**. **Dial:** `RL_O36`.

**Nothing lands on this seat's word.** This packet ends in a HALT, and the halt is the finding.

---

## 0 · THE ANSWER IN NINE LINES

1. **All three levers are wired and all three work.** S1 is at its four measured sites, Order H's
   tall/small factor is on the pick curve, and the dial-off board reproduces 1f176444 byte-exact.
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
6. **But the same dose puts picks 11-20 into buy-side red and pushes the worst single class to
   1.1687.** G1 and G3 cross each other, and they cross **between dose 0.05 and dose 0.10**.
7. **And the late bands need a far larger dose.** Picks 41-64 only stops depreciating at dose ≈ 0.60;
   picks 31-40 at dose ≈ 0.80. Both are three times the dose G3 allows.
8. **duff-tytler cannot reach 1,800 at any dose that G3 permits.** dean can reach his neighbourhood.
   The two men are still on opposite sides of the same lever, exactly as Order E measured.
9. **HALT.** No dose satisfies the owner's laws jointly. The tension is quantified in §5 and the full
   dose ladder is printed so the owner can see exactly where each of his laws breaks.

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

<!--GATES-->

---

## 6 · THE STANDARD TABLES

<!--TABLES-->

---

## 7 · THE NAMED ROWS AND THE PREREG SCORECARD

<!--NAMED-->

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

<!--LEDGER-->

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
