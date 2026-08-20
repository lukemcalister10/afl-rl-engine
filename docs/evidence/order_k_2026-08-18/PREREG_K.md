# PREREG K — THE FLOOR FIX, ITS ACCEPTANCE TEST, AND EVERY GATE

**Seat:** ORDER K, the BUILD seat. **Authority:** issue #334 comment **5321546243** (owner, 2026-08-17
23:42 UTC) — *"let's take your recommendation and proceed. Park the other fixes for after we adopt."*
**Base:** the landing candidate **1f176444**. **Dial:** the existing `RL_O36` wire (Order I/J lineage),
reused. **Dial-off must reproduce 1f176444 byte-exact.**

**This file is pushed before the first engine edit of this order.** Nothing below may be edited after
the first built board of this order is read. Any change is an amendment, dated, with its reason, and
the original left standing.

---

## 0 · WHAT THIS SEAT WAS TOLD TO DO, AND WHAT IT WAS TOLD NOT TO DO

**Told to do.** Build the owner's CHOSEN setting. Fix ONE named defect — the fade floor. Run the
standing acceptance suite. Produce the three review documents.

**Told NOT to do.** Re-optimise the setting. "Improve" it. Re-open anything the owner parked (the
veteran board, the recency re-weighting, the entry re-anchors, the young-specific counterweight, the
band-targeted late fix, the bake items). Land anything on this seat's word.

**THE RULED SETTING, transcribed from the owner's comment and never varied:**

```
dose (S1 age-bar) = 0.40   kappa = 0.20   eta = 0.50
gamma_u = 8.0              gamma_d = 14.0  lambda_rel = 1.08
plus the owner-ruled tall/small sitter factor (R-TALLFACTOR, ADOPTED)
```

Its **predicted** frontier values as the owner published them (REGION_J shortlist, `law_fails = []`):

| quantity | predicted |
|---|---:|
| year-1 class cohort | **1.0519** |
| picks 1-10 | **+7.58%** |
| picks 11-20 | **+13.82%** |
| picks 21-30 | **+8.26%** |
| picks 31-40 | **−8.54%** |
| picks 41-64 | **−6.50%** |
| max single class mark | **1.1385** |
| calibration slope | **0.976** |
| hindsight weight W | **0.327** |

---

## 1 · THE INSTRUMENT QUESTION, ANSWERED BEFORE THE BUILD

The order asks this seat to determine whether the REGION_J frontier rows were scored on the **pooled**
(Order D) fade or the **tall** (Order H) fade, because the rows themselves do not record it.

**ANSWER: THE TALL FADE. Not read off a comment — PROVED by reproduction.**

`o37_sweep.py:322` sets `D = Dvec(lrel, 'tall')` inside the grid loop, so every one of the 408,240
swept points, and therefore every `ruled_feasible` and every `shortlist` row in `REGION_J.json`, is
scored on `Dfade` — the tall/small exponent — never on `Dfade_pool`. Only the two named controls carry
a `fade` key at all (`control_landing` = `pool`, `control_tall_only` = `tall`); the frontier rows do not.

`ok/bridge.py` re-reads Order J's own calibrator legs and re-scores the ruled point on each fade in
turn. It reproduces the published row **exactly** on the tall fade and **not** on the pooled one:

| fade the ruled point is scored on | class | 1-10 | 11-20 | 21-30 | 31-40 | 41-64 | max class |
|---|---:|---:|---:|---:|---:|---:|---:|
| POOLED (Order D) | 1.0520 | +7.38% | +12.72% | +7.43% | −10.09% | −5.58% | 1.1441 |
| **TALL wired (Order H+J)** | **1.0519** | **+7.58%** | **+13.82%** | **+8.26%** | **−8.54%** | **−6.50%** | **1.1385** |
| TALL floor-FIXED (this order) | 1.0515 | +7.47% | +13.62% | +8.30% | −8.47% | −6.41% | 1.1386 |

The middle row is bit-for-bit the owner's published prediction. The bridge's own control — that
`Dfade` is reproducible from `Dfade_pool` and the row's (effective pick, TALL/SMALL) — holds to
**1.1e-16** on all 1,986 rows.

**THE CONSEQUENCE, REGISTERED HERE BEFORE ANY BOARD IS BUILT.** The owner's predicted frontier numbers
were computed **on the defective fade** — the same floor this order is commissioned to fix. The fix
therefore moves the prediction, and the third row above is what the SAME calibrator reads once the
floor is fixed. **Picks 1-10 and 11-20 come DOWN (−0.11 and −0.20 points) because part of what lifted
them was smalls at picks 6-18 being made LIGHTER by the defect.** Picks 31-40 and 41-64 come UP
slightly. The class mark is essentially unmoved (−0.0004).

**AND A SECOND, LARGER CAVEAT, registered now so it cannot be presented as a surprise later.** The
frontier is the **calibrator**. PREREG_J §3.3 registered that the calibrator is a NAVIGATION AID and
that the **standing extended-338 DECIDES**. The two instruments are known to disagree materially — on
the landing candidate the calibrator reads picks 11-20 at +11.52% where the standing extended-338
reads +9.20%. **The built numbers this order reports on the standing instrument will therefore differ
from the owner's predicted frontier values, and the difference is the instrument, not the build.**
Both are printed side by side, labelled, and the built-vs-predicted gap is stated at the top of the
packet — never quietly presented as if the built numbers were the predicted ones.

---

## 2 · THE DEFECT: THE FADE FLOOR

### 2.1 · The mechanism as wired

The sitter fade is `D_eff = D(c_u) ^ kappa`, where `D(c_u) < 1` is the ruled depth schedule and
`kappa` is the fade exponent at the row's effective pick. Because the base is **below 1**, a **higher
exponent is a HEAVIER fade** (a bigger discount) and a **lower exponent is a LIGHTER fade**.

```
Order D  (pooled) : kappa_P(p)  = clip( ( 0.1286221 + 0.4535959·ln p ) / 1.7472066 , 0.5 , 2.0 )
Order H  (tall)   : kappa_H(p,G)= clip( (−0.8778139 + 0.7100022·ln p + h·[G=TALL]) / s' , 0.5 , 2.0 )
                    h  = −0.6921227120657417        s' = 1.4284052406915069
TALL = the engine's own set, _O34_TALL = {KPD, KPF, RUCK}. Everything else is SMALL.
```

`s'` was re-solved by Order H so the redistribution identity holds: the mean of `D2^kappa` over Order
H's 408 fitted sitters equals the ruled depth-2 fade **0.5582775** exactly (residual −1.1e-16, verified
in this seat: `ok/floor_design.py`). **The identity pins the TOTAL fade the board charges. It does not
pin anything locally.**

### 2.2 · What actually goes wrong

The two fits have **different slopes** (0.4536 pooled vs 0.7100 tall/small), so the SMALL curve is not
the pooled curve shifted — **it crosses it.** Below pick 19 the small curve sits BELOW the pooled
curve, which means a LIGHTER fade, which means the tall factor **pays smalls at early picks instead of
charging them**. The floor at 0.5 does not cause this and does not cure it; it clips the small curve
part-way back up toward the pooled line and then stops, leaving the inversion in place:

| pick | pooled kappa | small kappa (wired) | small fade vs pooled |
|---:|---:|---:|---:|
| 5 | 0.5000 | 0.5000 (floor) | +0.00% |
| 6 | 0.5388 | 0.5000 (floor) | **+2.29% LIGHTER** |
| **7** | **0.5788** | **0.5000 (floor)** | **+4.70% LIGHTER** |
| 9 | 0.6440 | 0.5000 (floor) | **+8.76% LIGHTER** |
| 10 | 0.6714 | 0.5300 | **+8.59% LIGHTER** |
| 15 | 0.7767 | 0.7315 | **+2.67% LIGHTER** |
| 18 | 0.8240 | 0.8221 | **+0.11% LIGHTER** |
| 19 | 0.8380 | 0.8490 | −0.64% (heavier — intended) |
| 64 | 1.1533 | 1.4527 | −16.01% (heavier — intended) |

**The owner's named case.** `josh-smillie` — MID, pick 7, 0 games, and **not** in `_O34_TALL` — sat at
**772** on the landing candidate and reads **851** on the ruled tall board: **+79, all of it
`leg_tall`.** He is a small being paid by a talls-only relief, and he leaves the ~700s range the
owner's fade ruling put him in.

**The complete wired damage, measured on Order J's own built boards (`ORDER_J_MOVERS.json`), not
argued: SEVEN smalls are made LIGHTER, +126 board points in total.**

| row | pos | pick | games | landing | Order J ruled | leg_tall |
|---|---|---:|---:|---:|---:|---:|
| Josh Smillie | MID | 7 | 0 | 772 | 851 | **+79** |
| Will Brodie | MID | 9 | 55 | 791 | 812 | **+21** |
| Oskar Taylor | SD | 15 | 0 | 596 | 611 | **+15** |
| Campbell Chesser | MID | 14 | 39 | 332 | 338 | **+6** |
| James Leake | SD | 17 | 8 | 457 | 459 | **+2** |
| Tom Brown | SD | 17 | 58 | 507 | 509 | **+2** |
| Sam Sturt | SF | 17 | 31 | 77 | 78 | **+1** |

### 2.3 · The three candidate fixes, and why one is chosen

**Candidate A — re-solve the normalisation with the clip inside the constraint set. REJECTED, WITH
PROOF THAT IT IS A NO-OP.** Order H's solve already carries the clip inside the identity
(`oh_posfade.py:383` — `np.clip(s_t(p, tall) / sn, 0.5, 2.0)` is what `ident_t` averages). Re-solving
the wired form in this seat reproduces `s' = 1.4284052406915069` to the last bit. Candidate A cannot
move the small curve at all, because the small curve's problem is its SLOPE, not its LEVEL: raising the
level to make picks 6-18 heavier would make picks 19-64 heavier too, and the identity forbids that.

**Candidate B — apply the tall/small factor AFTER the clip.** This discards Order H's fitted small
slope entirely and replaces the ruled two-line object with a parallel translation of Order D's line.
**REJECTED because it re-opens a ruled object.** The owner ruled `h_TALL = −0.6921` on a fit whose
other coefficient is 0.7100; carrying `h` onto a curve with slope 0.4536 makes `h` mean something the
owner never ruled. It would also re-shape the tall relief profile materially (more relief at pick 64,
less at pick 24) — a re-optimisation this seat is explicitly forbidden to make.

**Candidate C — RE-SITE THE FLOOR, and re-solve the normalisation with the re-sited floor inside the
constraint set. CHOSEN.**

### 2.4 · The chosen fix, stated exactly

```
kappa_K(p, TALL)  = clip( s(p, TALL) / s_K , 0.5 , 2.0 )              # unchanged in form
kappa_K(p, SMALL) = min( 2.0 , max( kappa_P(p) , s(p, SMALL) / s_K ) ) # THE RE-SITED FLOOR
    where s(p,G) = −0.8778139 + 0.7100022·ln p + h·[G=TALL]   with h = −0.6921227120657417 UNCHANGED
    and   s_K    = 1.4340996145830727   (re-solved; identity residual −1.1e-16)
```

**In one sentence: a SMALL's floor stops being the abstract number 0.5 and becomes his own pre-factor
exponent** — the value the fade would have charged him if the tall factor did not exist. The talls keep
the [0.5, 2.0] clip they were ruled with.

**Why this is the right shape, and not a patch.** The 0.5 floor was never a measurement; PACKET_H says
so in its own words — *"a flat spot the clip, not the fit, is setting."* It is a guard rail. The defect
is that on the small side the guard rail was sited at a number that is **on the wrong side of the row's
own starting point**, so the guard rail itself pushed value the wrong way. Re-siting it at the row's
own pre-factor exponent makes the acceptance test **structural**: a small cannot be made lighter,
because his floor IS his pre-factor value. It is not a tolerance, not a special case for picks 6-18,
and not keyed to any named row.

**What it costs, all of it disclosed.** The redistribution identity is a real constraint: making smalls
at picks 6-18 heavier means the pinned total must be given back somewhere, and it is given back by
`s_K` rising from 1.4284052407 to 1.4340996146 (+0.40%). That makes every un-floored row very slightly
lighter — smalls at picks 19-64 and talls at picks 26-64. Talls therefore end up with **slightly MORE**
relief at late picks, not less (pick 64: +11.40% → +11.65%). Talls at picks 1-25 are on the 0.5 floor
in both wirings and do not move at all.

| | wired (Order J) | floor-fixed (Order K) |
|---|---|---|
| smalls made LIGHTER by the factor | picks **6-18** (7 real rows, +126 pts) | **NONE — no pick, no row** |
| tall relief, pick 16 | +18.65% | +18.65% |
| tall relief, pick 24 | +26.16% | +26.16% |
| tall relief, pick 64 | +11.40% | +11.65% |
| identity residual | −1.1e-16 | −1.1e-16 |
| 0.5 floor binds — TALL | picks 1-24 | picks 1-25 |
| floor binds — SMALL | picks 1-9 (at 0.5) | picks 1-18 (at his own pooled exponent; of those, picks 1-5 are also on 0.5 because the pooled curve is itself clipped there) |
| smoothness | continuous in ln(pick) | continuous in ln(pick) — the max of two continuous curves; measured max step over a 0.01-pick grid = **5.0e-4**, no cliff |

### 2.5 · How the fix is wired, and how it is priced

`RL_O36_FLOORFIX` — a **declared, default-ON** measurement dial, in the same discipline as
`RL_O36_TALL` and `RL_O31_NOPHI`. `RL_O36_FLOORFIX=0` restores Order J's wired form exactly
(`s' = 1.4284052406915069`, symmetric [0.5, 2.0] clip on both groups), so the fix's cost on **every row
and every band is a NUMBER on the movers ledger**, not a paragraph. `RL_O36` unset ⇒ not one byte of
this block executes ⇒ 1f176444 reproduces exactly.

### 2.6 · THE ACCEPTANCE TEST FOR THE FIX (the owner's words, made measurable)

> **K-FLOOR — the fix PASSES if and only if all five hold.**
>
> **(a) NO SMALL IS MADE LIGHTER, structurally.** For every pick `p` in 1..64:
> `kappa_K(p, SMALL) ≥ kappa_P(p) − 1e-12`. Build-failing assert in the engine.
>
> **(b) NO SMALL IS MADE LIGHTER, on the board.** Over all 804 active rows, every row whose position
> is not in `_O34_TALL` has `leg_tall ≤ 0`. **The FULL list of smalls whose fade changes is reported
> with its direction — every row, not a sample.**
>
> **(c) SMILLIE RETURNS.** `josh-smillie` reads inside the ~700s on the ORDER K board.
> Pre-registered arithmetic: at pick 7 the fix sets his exponent to exactly the pooled 0.5788, so his
> `leg_tall` becomes **0** and he returns to **772**; he has 0 games, so neither S1 nor the
> counterweight can reach him (`m_u(0) = m_d(0) = 0`). **Predicted ORDER K value: 772.**
>
> **(d) THE TALLS KEEP THEIR RELIEF.** `will-green`, `toby-conway`, `william-mccabe` and
> `alex-dodson` each keep a meaningful positive `leg_tall`. Pre-registered arithmetic — picks 16, 24
> and 19 are on the 0.5 floor in both wirings, so those three are **unchanged**; pick 53 gains a
> little: predicted **+141 / +86 / +70 / +16 or +17**.
>
> **(e) THE IDENTITY STILL HOLDS.** The redistribution residual against 0.5582775 is **< 1e-9**,
> printed as a number. Build-failing.
>
> Also reported, not gated: **where the floor still binds and for whom** — by pick range and by named
> row.

---

## 3 · THE OWNER'S LAWS — THE ACCEPTANCE SUITE

Every gate below is scored on a **built board** or on the **standing extended-338 / all-arm**
instruments, never on the calibrator. Halt-and-report on breach; **never trade one silently.**

| # | law | rail | instrument |
|---|---|---|---|
| **G1** | year-1 class cohort grows | ≥ **1.03** floor, **strictly < 1.14** buy rail. The owner's ~1.08 ideal is known unreachable — **report the number, do not chase it** | W2 estimator `mean_0515`, classes 2005-2015, class bootstrap seed 33 |
| **G2** | picks **31-40** and **41-64** materially improve vs the landing candidate; **both are expected to REMAIN negative** — a known limitation, not a failure of this build | improvement > 0 points on each | standing extended-338, committed md5 `d59ad550116ebbe3d90ed82becd2c4d5` |
| **G3** | no band or pool arm above **+14%** yr0→1 | +14% | extended-338 + all-arm, BOTH windows |
| **G3-SSP** | SSP's inherited **+50.52%** is preregistered and SEPARATE. It is REPORTED, never masked, and it may never stand in for a new breach | — | all-arm |
| **G4** | picks **1-10** stay near their current **+7.93%** — *this is why this setting was chosen* | report the number and the move | standing extended-338 |
| **G5** | sub-expectation-with-games rows do NOT rise: **xavier-taylor**, **daniel-annable**, **dylan-patterson**, by name with directions | do not rise | the 2026 board |
| **G6** | day-0 entry values **bit-identical, 89 of 89**; the sitter PRINT reference regenerates as the ruled fades require — **disclosed exactly as Order D did** | 89/89 on `derived_v0` | the emit's replication guard |
| **G7** | determinism ×2; dial-off = **1f176444** byte-exact; full dial chain identities | byte equality | board md5s |
| **G8** | continuity — no cliffs in age, games or pick; `rho32` monotone and < 1; the ruled at-bar continuity object | tolerance 1e-9 | engine asserts |
| **G9** | **J-TOL** (PREREG_J §2.2), reported on the counterweight legs so the veteran-side cost of the ruled setting is a number. The tall factor is EXEMPT (R-TALLFACTOR is adopted) and is DISCLOSED in full | per-row `min(25, max(1, 0.005·v))`; churn ≤ 1,001.87; net ≤ 667.91 | the 2026 board, mature rows 24+ |
| **G10** | reported, not gated: **dean** and **duff-tytler** against their Candidate-31 levels (2,670 / 1,832) | — | the 2026 board |

**Known open defects that this order does NOT fix and MUST carry on every page, in plain words:**
picks 31-40 and 41-64 still negative · dean and duff-tytler still below their Candidate-31 levels ·
SSP +50% · development arms negative · **veteran key-position talls aged 28-30 over-priced by roughly
30% because the veteran board is parked** · the engine over-weights the current season (one-breakout
players likely rich — xerri, callaghan, ash, thilthorpe; one-bad-year veterans likely cheap —
coniglio, de-goey, langford) · the ceiling column on the dial page prints ~q87, not q97, for players 22+.

---

## 4 · NAMED-ROW PREDICTIONS (the scorecard — scored as stated, never rewritten)

Direction is the prediction. Where the arithmetic is already forced by the fix, the NUMBER is
predicted and named as forced.

| row | pos / pick / games | predicted on ORDER K | mechanism |
|---|---|---|---|
| **josh-smillie** | MID / p7 / 0g | **772 exactly** (forced) | the re-sited floor zeroes his `leg_tall`; 0 games ⇒ S1 and the counterweight cannot reach him |
| **will-brodie** | MID / p9 / 55g | **DOWN vs Order J**, `leg_tall` → 0 | same channel |
| **oskar-taylor** | SD / p15 / 0g | **596 exactly** (forced), `leg_tall` → 0 | same channel, 0 games |
| **campbell-chesser** | MID / p14 / 39g | `leg_tall` → 0 | same channel |
| **james-leake · tom-brown · sam-sturt** | SD/SD/SF / p17 | `leg_tall` → 0 | same channel |
| **will-green** | RUCK / p16 / 1g | **+141 retained** (forced — the 0.5 floor binds in both wirings) | ruled tall relief |
| **toby-conway** | RUCK / p24 / 6g | **+86 retained** (forced) | ruled tall relief |
| **william-mccabe** | KPF / p19 / 4g | **+70 retained** (forced) | ruled tall relief |
| **alex-dodson** | RUCK / p53 / 1g | **+16 or +17** — retained and very slightly LARGER | `s_K` rise gives late talls a touch more relief |
| **steely-green** | SF / p55 / 43g | DOWN, but slightly LESS down than Order J's −4 | late smalls still pay; `s_K` rise softens it a touch |
| **harry-dean** | KPD / p3 / 17g | **UP** vs landing 2,400; **still BELOW C31's 2,670** | S1 at dose 0.40: 14.9 a game clear of his own age bar |
| **cooper-duff-tytler** | KPF / p4 / 13g | **UP** vs landing 1,572; **still BELOW C31's 1,832** | S1, smaller margin |
| **xavier-taylor** | SD / p11 / 2g | **DOWN** | counterweight: weight off pedigree onto a poor production leg |
| **daniel-annable** | MID / p6 / 2g | **DOWN** | as xavier-taylor |
| **dylan-patterson** | SD / p5 / 5g | **DOWN** | as above, larger g so larger charge |
| **milan-murdock** | SF / 26 / 17g | moves, and small | age 26 with 17 games sits inside the re-mix's active zone |
| **isaac-kako** | SF / p13 / 36g | **UP** | S1 on a high-rho row |
| **alix-tauru** | KPD / p10 / 18g | **UP** | S1; tall age gaps are the largest |
| **jedd-busslinger** | KPD / p13 / 15g | **UP** | S1 + the ruled fade on an above-age-bar season |

**Band predictions on the STANDING extended-338**, stated before the build so the instrument gap is
scored and not explained afterwards. The calibrator says the fix costs picks 1-10 about 0.11 points
and picks 11-20 about 0.20 points relative to the owner's published frontier. The standing instrument
runs COOLER than the calibrator on the young bands. This seat therefore predicts, on the standing
extended-338, ORDER K vs the landing candidate's +7.93 / +9.20 / +2.76 / −12.84 / −7.88:

- **picks 1-10: UP a little, and staying near +7.93%** — predicted **+8.0% to +8.6%**;
- **picks 11-20: UP** — predicted **+10.5% to +12.0%**, and **under the +14% rail**;
- **picks 21-30: UP** — predicted **+4% to +6%**;
- **picks 31-40: UP (improved) and STILL NEGATIVE** — predicted **−11.5% to −9.0%**;
- **picks 41-64: essentially flat to slightly UP, and STILL NEGATIVE** — predicted **−9.0% to −7.0%**;
- **year-1 class: 1.03 ≤ mark < 1.14, and the ~1.08 ideal NOT reached.**

---

## 5 · FALSIFIERS — any one firing is reported in the packet, in these words

- **K1** — a SMALL's sitting fade becomes lighter as a result of the tall factor, at any pick or on any
  row. **BUILD-FAILING** (structural assert) and, if it ever reached a board, **HALT AND REPORT**.
- **K2** — `josh-smillie` does not return to the ~700s. **HALT AND REPORT.**
- **K3** — any of will-green / toby-conway / william-mccabe / alex-dodson loses meaningful relief.
  **HALT AND REPORT** with the numbers.
- **K4** — the redistribution identity misses 0.5582775 by more than 1e-9. **BUILD-FAILING.**
- **K5** — `RL_O36` unset does not reproduce **1f176444** byte-exact. **BUILD-FAILING.**
- **K6** — `derived_v0` is not bit-identical on 89 of 89. **BUILD-FAILING.** (The *printed* day-0 of
  sitters moving is the ruled fade's disclosed effect, not a failure — Order D's disclosure verbatim.)
- **K7** — determinism ×2 differs. **BUILD-FAILING.**
- **K8** — `rho32` non-monotone, or any continuity assert in age / games / pick fires. **BUILD-FAILING.**
- **K9** — the year-1 class mark falls below 1.03 or reaches 1.14. **HALT AND REPORT.**
- **K10** — any band or reachable pool arm exceeds +14%. **HALT AND REPORT.** (SSP's inherited +50.52%
  is preregistered, separate, and reported — it may never mask a new breach.)
- **K11** — picks 1-10 fall materially below the landing candidate's +7.93%. **HALT AND REPORT** — this
  is the owner's stated reason for choosing this setting.
- **K12** — picks 31-40 or 41-64 fail to improve. **HALT AND REPORT.** (Remaining negative is NOT K12;
  it is the known limitation, reported as such.)
- **K13** — any of xavier-taylor / daniel-annable / dylan-patterson RISES. Reported by name with its
  number.
- **K14** — the built values differ materially from the owner's predicted frontier values. **REPORTED
  PROMINENTLY at the top of the packet and of every document**, with the instrument gap and the floor
  fix separated. This falsifier is expected to fire; it is registered so that it is reported and not
  discovered.

---

## 6 · THE ORDER OF OPERATIONS, FIXED

1. **This file, pushed — before the first engine edit.**
2. The engine edit: the re-sited floor, `s_K`, `RL_O36_FLOORFIX`, and the build-failing asserts
   (K-FLOOR (a) and (e), clip, monotone, smoothness, the Order H transcription kept live so the ruled
   fit constants are proved unchanged). Pushed.
3. The board suite, **strictly sequential, PID-unique staging, five-var thread pinning**:
   `cand` (dial off ⇒ 1f176444) · `tallJ` (the wired floor alone — the fix's own before-picture) ·
   `tallK` (the floor-fixed factor alone) · `s1` (S1 alone at dose 0.40) · `K` (the full ruled
   setting) · `K2` (the determinism repeat).
4. The walk-forward emit on the ORDER K board; the standing extended-338 and all-arm instruments,
   disclosed copies, unmodified.
5. The gates, scored and printed with their numbers.
6. The movers ledger over the four board columns plus the legs.
7. The three documents, PACKET_K.md, the prereg scorecard.

**Nothing lands on this seat's word.**

*— ORDER K. Pushed before the first engine edit of this order.*
