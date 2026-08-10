# PHASE 2 — THE BUILD ON THE SUPPLIED RULER · 2026-08-10

Resume order: the five blockers of the phase-1 halt (`README.md`) are resolved and the ORIGINAL
ruler instruments are landed at `docs/evidence/ruler_act_2026-08-10/` (PR #400). Branch rebased
onto `origin/main` `b1dbbef`. This file records phase 2; `README.md` records the phase-1 halt and
still stands — nothing in it is withdrawn except the two halts it named, which are retired below.

**Precondition, run FIRST as ordered:** `r15_align.py` → **ALIGNMENT: PASS**, exact match to the
supervisor's own re-run — stage4a1 and stage5 both `n=414 F1=1.1363 · KPD 0.6680 · RUCK 1.6959`,
Hurley spot exact. Every number below sits on that gate.

---

## 0. WHAT THE ORIGINAL RULER CHANGED ABOUT MY PHASE-1 CONCLUSIONS

| phase-1 claim | status now |
|---|---|
| ITEM I could not be restated | **RETIRED** — restated in full (§1) |
| ITEM B's 21+ factor was −53% vs filed | **RETIRED and diagnosed** — on the honest instrument it is **+13.9%** (§2) |
| `ev()` cannot price a historical player | **stands as a fact, but is MOOT for ITEM I** — the original instrument prices from the frozen per-entrant matrices (`v0`/`vpath`), never from live `ev()` on retirees. That is exactly why the originals were needed and a rebuild could not substitute |

My reconstruction's error is now fully diagnosed, and it is worth recording because it is the
reason a rebuild was not good enough: it discounted at the engine's own `LENS['bal']=0.14` and
priced seasons on `gfut` REPL through live `ev()`, where the real instrument uses **DISC = 1.0939**
and **each season's OWN fit bar** off the frozen matrices. Two wrong constants and one wrong
object — enough to invert a band's sign.

---

## 1. ITEM I — THE RESTATEMENT (`item_i_restate.py`, `item_i_restate_out.txt`)

The original F definitions (`r15_align.py`'s own exponents: `d=4` at year 0, `d=3` at year 1,
`DISC=1.0939`), with the year-4 **PROXY replaced by r24's realized-delivery object**, on the
corrected ruler's own window (classes 2004-2015, `n=1418`, where career year 11 is observable).
All four instruments printed side by side so no reading is instrument-shopped; **D** (rate ×
year-11-capped — the owner's own economics and his own horizon) is the headline, as ruled.
**F8 applied at PLAYER UNIT on top**, as the sitting ruled and as these pre-ruling scripts did not:
Kish eff-n over players, weights = the ratio's own denominator, bar 35.

### The year-0 table (extract; full table in the transcript)

| cell | n | eff-n | F8 | F bent | F corr | verdict bent | verdict corr |
|---|---|---|---|---|---|---|---|
| ALL rows | 1414 | 665.4 | PASS | 0.9948 | 0.6431 | HONEST | OVER-priced |
| ND in-curve (1-64) | 741 | 416.4 | PASS | 1.0782 | 0.6808 | HONEST | OVER-priced |
| ND × MID | 218 | 143.1 | PASS | 1.0416 | 0.6923 | HONEST | OVER-priced |
| ND × SD | 161 | 107.5 | PASS | 0.9591 | 0.6209 | HONEST | OVER-priced |
| ND × SF | 138 | 84.5 | PASS | 1.2227 | 0.6209 | HONEST | OVER-priced |
| ND × KPF | 93 | 59.5 | PASS | 1.2203 | 0.6981 | HONEST | OVER-priced |
| ND × KPD | 85 | 60.6 | PASS | 1.0393 | 0.6396 | HONEST | OVER-priced |
| ND × RUCK | 46 | 27.3 | **fail** | 1.1095 | 0.8606 | HONEST | HONEST |
| pool ALL | 673 | 505.2 | PASS | 0.7298 | 0.5236 | OVER | OVER |
| pool age ≤18 | 363 | 310.5 | PASS | 0.5451 | 0.3477 | OVER | OVER |
| pool age 19-20 | 98 | 81.2 | PASS | 0.7648 | 0.7963 | HONEST | HONEST |
| pool age 21+ | 124 | 52.8 | PASS | 2.5471 | 1.6845 | UNDER | HONEST |

Year-1 headline: ALL rows `1.1725 → 0.7600`; ND in-curve `1.1783 → 0.7685`; ND × MID
`1.3323 → 0.9066`. (ND × SD/SF/KPF/KPD/RUCK all **fail** the player-unit bar at year 1 — n is
22-63 there. That is itself a result of moving F8 to player unit.)

### The precondition — and the reading it turns on

**Reading 1, absolute:** 9 ND year-0 cells flip HONEST → OVER-priced. **DIRTY.**

**Reading 2, relative:** **no ND year-0 cell changes its position relative to the population.
CLEAN.**

The two readings differ because every flip in reading 1 is *the same flip*: the level factors are
1.505 / 1.545 / 1.625 / 1.748 / 1.969 / 1.584 …, clustered on the overall **1.547**. That is not
nine findings. It is the ruler act's already-ruled headline — the year-4 price stands ~1.55×
above realized delivery — arriving at every cell at once.

The ruler act's own method draws exactly this line: `r25_2x2.py` defines *bend* as "the cell's
1/tilt divided by the OVERALL 1/tilt on the SAME instrument (level divides out)", and the sitting
acted **only on bends**. Applying the same rule to the restatement gives reading 2.

**Seat's reading: READING 2. ITEM A's precondition is MET; no year-0 cell is re-taught.** The
uniform level shift is the ROOT ACT's object — the directive stages it *after* composition
precisely because correcting the forward projection "re-derives year 0/1/2+ consistently" — and
re-teaching every ND year-0 cell down by 1.55× inside this act would BE the root act, unruled and
unfunded. **Flagged as an owner decision, not taken silently:** under reading 1 nothing ships.

### Two real cell-level findings (relative flips — both on the pool side, both ITEM B's object)

- **pool age 19-20**: below population → **ABOVE** (rel 0.769 → 1.238)
- **pool × RUCK**: below population → at population (rel 0.599 → 1.045)

On the ND side, SF (1.969×) and KPF (1.748×) shed the most level — SF is the named tilt cell that
item G already owns, and G is parked.

---

## 2. ITEM B — THE POOL YEAR-0 AGE GRADIENT (`item_b_derive.py`)

Same instrument as ITEM I, with `r36_dob.py`'s **basis split enforced**: every VALUE from the
act-branch artifact (store `37ced3ce`), **only the AGE FIELD** from the DOB store `d9a24282`. A
birth year is a fact about the world, not a valuation, so writing it cannot move a walk-forward
price computed without it. Without the split the teaching population still carries **88
age-unknown pool rows** and the C5 identity cannot close; with it, **age-unknown = 0**, matching
`r37_ageaxis.txt`.

| band | n | eff-n | F8 | **re-derived** | as filed | shift |
|---|---|---|---|---|---|---|
| ≤18 | 429 | 367.2 | PASS | **0.6859** | 0.666 | **+3.0%** |
| 19-20 | 111 | 90.9 | PASS | **1.4112** | 1.200 | **+17.6%** |
| 21+ | 133 | 60.5 | PASS | **2.8173** | 2.474 | **+13.9%** |

**Conservation (C5): pool Σv0 186,576.5 → 186,576.5, delta `0.000000`**, renormaliser
`K = 1.0000000000` — exact by construction, since the bands partition the pool and the factors are
ratio-normalised, so the gradient is preserved and only the level is pinned.

### The taper — the ruled shape is REFUSED, on evidence

"Smooth taper 21→26, no integer cliff", read as a mean-holding linear ramp, requires a **plateau
of 6.98 at age 26**. Refused, and the refusal is shown rather than asserted:

- every per-age cell inside 21+ is far below the F8 bar — **21:22.6 · 22:15.1 · 23:11.6 · 24:7.5 ·
  25:1.0 · 26:2.7**;
- the point estimates **fall** after 22, not rise — **3.11 · 4.70 · 3.59 · 0.75 · 0.00 · 0.01**;
- so a rising ramp hands the **largest** factor to the oldest, thinnest, measured-at-≈0 rows;
- and it breaks pool conservation by +3.5%.

The directive's own tilt reading already says *"mature-21+ unnameable → base factor, pooling
disclosed"*. The evidence agrees.

**What ships** removes the cliff where the ruling actually points — the band boundary — by keying
on **continuous** draft age (the engine's `_ageR` rounding is what would create an integer cliff):
flat 0.6859 to 18 · linear bridge to 1.4112 at 19 · flat to 20 · linear bridge to 2.8173 at 21 ·
**flat thereafter** (pooled, pooling disclosed). No integer cliff; each band mean held exactly; no
unmeasured within-band gradient invented.

---

## 3. ITEM D — THE SIT-CHARGE CONTRAST (`item_d_derive.py`)

The instrument was **verified before any sizing was taken from it**, and the first attempt
**halted**: the cohort reproduced exactly (`n=496`) but F came out 0.5824 against the recorded
0.984. The halt resolved on inspection, not guesswork — the sitter act used the **stage4a1**
matrix (its own step 3), not stage5, and its ratio is `r15`'s **F1 form** (year-4 proxy over the
**year-1** price), not the year-0 form. On that pairing the anchor reproduces at **0.9838 vs
0.984**. Only then was the contrast computed.

| class | n | eff-n | F bent | F corr | 95% CI (corr) | F8 |
|---|---|---|---|---|---|---|
| KPP | 83 | 60.4 | 1.3422 | 0.7290 | [0.394, 1.130] | PASS |
| SMALL | 186 | 98.9 | 1.0032 | 0.6603 | [0.383, 0.970] | PASS |
| RUCK | 30 | 22.5 | 1.2207 | 1.2945 | [0.391, 2.452] | **FAIL** |

**bent KPP/SMALL = 1.3380** (filed 1.378 — reproduces) → **corrected = 1.1041**, 95% CI
**[0.548, 2.157]**.

**FLAG 1 — the corrected CI includes 1.0.** The filed interval [1.05, 1.80] was clear of 1 and was
measured on the bent ruler. On the corrected ruler the contrast is no longer independently
significant, which weakens D's own stated premise ("only the contrast clears the bar → the input
is RELATIVE").

**FLAG 2 — a trap I nearly shipped.** Reading "cautious end" as the CI's lower edge gives
**0.5477 — below 1** — which **inverts the ruled direction**: it would deepen the KPP charge and
lighten SMALL, the exact opposite of the ruling, while still reporting "conserved" and "cautious".
A tilt whose interval covers 1 has a cautious end of **1.0**.

**What ships:** the **ruled cautious end 1.05, taken AS FILED** and marked as filed. Defensible on
this measurement rather than in spite of it — the corrected point estimate 1.1041 sits *above*
1.05, so 1.05 remains the cautious choice, and 1.05 lies inside the corrected CI.

| | factor | direction |
|---|---|---|
| `t_KPP` | 1.035292 | retention up → charge **LIGHTENED** |
| `t_SMALL` | 0.985992 | retention down → charge **DEEPENED** |
| `t_RUCK` | 1.000000 | **untouched**, as ruled (and its cell fails F8 anyway: eff-n 22.5) |

**Conservation within the sitter pool: 90,029.0 → 90,029.0, delta `0.000000000`.**

**Owner decision flagged:** the alternative honest reading is to ship **zero tilt**, since the
corrected contrast no longer clears the bar.

---

## 4. ITEM H — THE CUT LIST (`item_h_derive.py`)

Tested as what a cut factor should be if it is the cell's own delivery ratio. On the ruler they
were measured on, **none of the three reproduces**:

| cell | ruled | F bent | corrected F | CI (corr) | eff-n | F8 |
|---|---|---|---|---|---|---|
| named union sitters (23+ ∣ IRE ∣ MSD) | 0.280 | 0.1670 | 0.2301 | [0.010, 0.639] | 60.3 | PASS |
| all-pool-sitters | 0.804 | 0.3484 | 0.2974 | [0.185, 0.422] | 551.0 | PASS |
| mature nonRD | 0.615 | 0.7676 | 0.5162 | [0.115, 1.226] | 46.2 | PASS |

So my cell definitions are **not** the ones the cuts were sized from — the pool-grid qualification
(ruling 2.5) carries conditions I do not have, and its instrument belongs to a separate act whose
script is not in the landed set. Rather than size a cut on a cell I cannot verify, the factors are
**taken AS FILED (0.280 / 0.804 / 0.615) and marked as filed**, with the corrected-ruler bridge
printed beside them, per the order.

**Worth the sitting's eye:** on the corrected ruler two of the three cells deliver **less** than
their ruled cut factor, so the ruled cuts are if anything **generous** rather than harsh — the
all-pool-sitters cell especially, where the corrected reading (0.2974) is under half the ruled
0.804 and its CI **[0.185, 0.422] excludes 0.804 entirely**.

The #326 floor (0.45) is untouched. No blanket lifts anywhere.

---

## 5. WHAT IS STILL OUTSTANDING

The derivations above are complete and verified. **The engine wiring is not done**: no file under
`engine/` is touched, the board is still `4b448a82`, and ITEMS A/B/C/D/E1/E2/H are sized but not
installed. What remains, in the ruled order:

1. wire ITEM B's age curve into `entry_anchor`'s pool branch (build-time renormalisation, a state
   function, never a stored constant);
2. wire ITEM A at the `ev()` level (see `item_a_ablation.py` — and NOT inside `raw_ev`, which
   would be self-referential), then the conservation re-teach with sums printed;
3. wire C + D + E1 + E2 + H together on the shared book;
4. the side-by-side with per-item attribution columns summing exactly to each player's total move;
5. the gate lane + the publication layer (required the moment the board moves).
