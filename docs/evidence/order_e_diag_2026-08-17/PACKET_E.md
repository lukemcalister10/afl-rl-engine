# PACKET E — WHERE THE AGE LENS INSIDE `Phat` ACTUALLY COSTS DEAN AND DUFF-TYTLER

**Seat:** ORDER E diagnostic, issue #334 comment 5316425330. **STRICTLY READ-ONLY.** Nothing in the
engine, the board, the store or the law was touched. Every experiment below is a change made to the
engine *in this seat's own memory*, for a few seconds, and then undone — and after every single
experiment the six measured players were re-priced and had to come back to exactly their original
price before the next one started. They always did.

**Pre-registered first:** `PREREG_E.md`, pushed before a single number was measured. It fixed the
list of 26 sites so none could be quietly dropped.

---

## 0 · THE ANSWER IN SIX LINES

1. **The site is found, and it is one site.** It is the **replacement bar inside the projection
   loop** — the number the engine subtracts from a player's expected output to turn it into value.
   For a 19-year-old key defender that number is **65.4** — what a *mature* key defender must beat.
2. **It costs harry-dean 843 board points and cooper-duff-tytler 448 board points.** Verified, with
   a byte-exact identity control on the re-implemented code and a leak check that came back clean.
3. **milan-murdock, 26 years old, moves by exactly 0.00 points.** So does every other mature row —
   not approximately, exactly. That is the law working: the correction is zero from age 24 up.
4. **But it does not stop there.** The same correction moves levi-ashcroft +638, connor-o-sullivan
   +495 and logan-morris +539. It is a *whole-cohort* lever, not a dean-shaped one.
5. **NO minimal set was found that gets BOTH men into the owner-expected neighbourhood without
   breaching the +14% early-band rule.** dean reaches ~2,600 at about 37% of the correction, and
   the early bands land right on the +14% line with essentially no margin. duff-tytler needs about
   70% of it, and at that dose the early bands go to roughly **+23%** and **+21%** — a clear
   double buy-side red.
6. **A second, larger reason exists and it is NOT inside `Phat`.** Even the full correction lifts
   dean's production leg by 1,431 points but only 843 of those reach his price, because the
   games-keyed production weight `rho31(17) = 0.589` throws away 41% of any improvement made there.
   For duff-tytler the weight is 0.547 — it throws away 45%.

---

## 1 · PLAIN LANGUAGE — WHAT THE ENGINE IS DOING TO THESE TWO

Some words, defined once:

- **Board points** — the currency the owner reads on the board. The engine computes in its own
  currency and the board divides by 1.0524. Every number in this packet is board points.
- **`Phat` (the production leg)** — the engine's estimate of what a player is worth *from his own
  playing*, as opposed to what he is worth from his draft pedigree.
- **The bar (replacement level)** — the engine does not value output; it values output *above a
  bar*. The bar is roughly what you could get for free at that position. Subtract the bar, and
  what's left is what the player is actually worth.
- **The pedigree leg** — what the player is worth because of where he was drafted. Dean's is
  **2,316** points, which is exactly the draft-day value the owner keeps citing. Duff-tytler's is
  **1,765**, which is exactly his.
- **The production weight (`rho31`)** — a number between 0 and 1 that says how much of the
  production leg counts. It rises with career games played. Dean has 17 games, so his is 0.589.

Here is the whole price, both men, laid out:

| | production leg `Phat` | × weight | pedigree leg | × its weight | + age credit | **= price** |
|---|---:|---:|---:|---:|---:|---:|
| harry-dean | 2,686 | 0.5895 → 1,583 | 2,316 | 0.3328 → 771 | 46 | **2,400** |
| cooper-duff-tytler | 1,622 | 0.5474 → 888 | 1,765 | 0.3546 → 626 | 58 | **1,572** |

Now the arithmetic that Order C pointed at, printed exactly:

| row | pos | age | shown output | the mature bar | his own age's bar | vs mature | vs his age |
|---|---|---:|---:|---:|---:|---:|---:|
| harry-dean | KPD | 19 | 59.7 | 65.4 | 44.8 | **−5.7** | **+14.9** |
| cooper-duff-tytler | KPF | 19 | 50.3 | 63.8 | 43.2 | **−13.5** | **+7.1** |
| milan-murdock | SF | 26 | 70.1 | 67.9 | 67.9 | +2.2 | +2.2 |
| levi-ashcroft | MID | 20 | 72.3 | 77.1 | 62.8 | −4.8 | +9.5 |
| connor-o-sullivan | KPD | 21 | 69.1 | 65.4 | 53.8 | +3.7 | +15.3 |
| logan-morris | KPF | 21 | 65.9 | 63.8 | 52.2 | +2.1 | +13.7 |

Read the two exhibit rows again. Dean averaged 59.7 in his first season. The engine's projection
subtracts 65.4 from that, gets a negative number, and prices the season as **below replacement** —
as if he were a mature key defender who could be replaced for nothing. Measured against what a
19-year-old key defender actually produces, he is 14.9 points a game *clear* of the bar. Duff-tytler
is 13.5 below the mature bar and 7.1 above his own. **That is the age lens inside `Phat`, and it is
a single subtraction in a single loop.**

For murdock, 26, the two bars are the same number. That is why he cannot move.

---

## 2 · THE SITE CLASSIFICATION TABLE

Every site found by walking the production leg end to end, with a file and line. Classification:
**(a)** age-aware by design · **(b)** age-blind but judging young output against a mature reference
· **(c)** age-irrelevant.

### 2.1 · Inside `Phat` — the production projection core

| # | site | file:line | class | verdict |
|---|---|---|---|---|
| **S1** | **the replacement bar in the projection loop** — `posval(base − REPL[pos])` at every horizon, and the same subtraction in the demonstrated-production floor. The number is `REPL[pos] − 3` (KPD 65.4 · KPF 63.8 · MID 77.1 · RUCK 75.5 · SD 75.3 · SF 67.9), set by `price6` lowering `MA.REPL` around the call | `_merged_recover.py:1074-1075` · `:1112-1114` · `rl_model.py:1089-1090` · `:1119-1121`; bar set at `_merged_recover.py:388` | **(b)** | **THE SITE. 843 / 448.** |
| S2 | the future discount — `age_disc` returns one flat rate for every age (`RL_AGE_DISC` off by default) | `rl_model.py:990-1000`, used `_merged_recover.py:1063,1071` | **(b\*)** — age-blind, but the reference is a carry rate, not an output bar | 157 (V5 ladder) / 470 (V3 ladder) |
| S3 | the v7 upside-tail taper. The taper itself is age-keyed and gives a 19-year-old the full tail. Its "keep some of your tail" relaxation is denied unless the player is 4 points clear of the **mature** bar | `_merged_recover.py:733-747` | **(a)** with a **(b)** sub-gate | **0.0** for both exhibits (the taper is already 1.0 at 19). +3.9 / +7.1 on the 21-year-old controls |
| S4 | the un-compress map's output axis — `ρ = Σ games·(season avg − REPL[pos]) / Σ games`, normalised by the **proven** median | `_merged_recover.py:534-549`, used `:562-573` | **(b)** | live but small, and it fights S1 — see §4 |
| S5 | the reliability shrink on the level fed to the band model | `conditional_prior.py:111-118`, feature `:120-123` | **(b, minor)** | 159 / 13 — but it also moves murdock (+41), so it is **not** an age correction |
| S6 | the upside-fade target bar `REPL[pos] − 3` inside `_inferM1` | `_merged_recover.py:730` | **(b)** | **0.0** — the gate `_eo` is zero for a first- or second-year player |
| S7 | the decliner shed `_agemult2(age, Lc − REPL[pos])` | `_merged_recover.py:695`, `:167` | **(b)** | **0.0** — needs a season-on-season fall; neither man has two seasons |
| S8 | the elite/runway premium `elite = clip((lp/PEAK[pos] − 0.97)/0.30,0,1)` | `_merged_recover.py:1091-1093` | **(c)** for elite (`lp` is itself a projected *peak*, so peak-vs-peak is like for like) / **(a)** for runway | not measured, and the reason is stated |
| S9 | the age curve `frac(a, peak_age, pos)` and the floor `lev = max(lev, current level)` | `rl_model.py:876-879`, `_merged_recover.py:1067-1069` | **(a)** | — |
| S10 | the conditional-prior band (the GBM that makes `b6`) — the player's age is one of its input features | `conditional_prior.py:196-199`, features `:120-123` | **(a)** | — |
| S11 | the frozen q97 ceiling — same age feature, frozen pickle | `_merged_recover.py:373`, load `:86-95` | **(a)** | — |
| S12 | the pedigree pole — `wage = clip(1 − (age−20)/6, 0, 1)`, par read at the player's own tenure | `_merged_recover.py:576-599` | **(a)** | — |
| S13 | `_dev_advance` / `level_now` | `rl_model.py:809-819` | **(a)**, and an exact identity on the present board | — |
| S14 | `level_demo` trust/confidence | `rl_model.py:757-807` | **(a)** | — |
| S15 | `_lvlcurr` per-group recency decay | `_merged_recover.py:305-309` | **(c)** for age | — |

### 2.2 · The downstream layers and the level readers

| # | site | file:line | class | verdict |
|---|---|---|---|---|
| S16 | iso remnants — the pick tax, faded on evidence | `_merged_recover.py:629-635` | **(c)** for age | factor is exactly **1.000** for both exhibits |
| S17 | ITEM-H, the ruled cut list | `_merged_recover.py:2343-2355` | **(c)** — pool cells only | factor is exactly **1.000**; both men are national draftees |
| S18 | D8 graded staleness — `qv = season avg / REPL[pos]` | `_merged_recover.py:2536`, used `:2602-2606` | **(b)** | **0.0** — needs 4+ years of tenure; both have 1 |
| S19 | the decay gate — `pr = best level / bar` (ORDER C's site 2) | `_merged_recover.py:2579-2580`, used `:2607-2609` | **(b)** | **0.0** — needs 6+ years of tenure |
| S20 | ITEM C's evidence weight — `Q = clip(career avg / bar, 0, 2)` (ORDER C's site 1) | `_merged_recover.py:2437` | **(b)** | **0.0** — its only two consumers are the anchor blend (switched off on this lane) and the RUCK ceiling (wrong position) |
| S21 | KPF compression | `_merged_recover.py:2556-2571` | **(a)** — gated at age ≥ 24 | inert by construction |
| S22 | the L1c young credit — `1 + w·R·φ(g)`, `φ(g) = (1 − g/46)²`, keyed on **career games, never on age** | `_merged_recover.py:1169-1186`, applied `:1192-1195` | **(b)** | it currently pays dean **+127** and duff-tytler **+115**; keying it on age instead would pay a further **+193 / +109** |
| S23 | the M3 clock blend | `_merged_recover.py:2637-2652` | **(a)** | inert — both men are on pace (17 and 13 games; the lever needs under 11) |
| S24 | `_PL_F`, the board factor 1.0524 | `_merged_recover.py:1496` | **(c)** — uniform | — |
| S25 | the ORDER-31 production weight `rho31(g)` and its pedigree complement | `_merged_recover.py:3428-3437`, `:3543-3561`, blend `:3564-3566` | **(b)** — keyed on career games, so a 19-year-old with 17 games is judged "thin evidence" exactly like a 27-year-old with 17 career games | **NOT a `Phat` site and it is the ruled re-mix.** Measured only as a bound — see §4 |
| S26 | the recency readers `_lvl_wt` / `_lvl_eff` / `_exposure` and the `_est` hold-shed | `conditional_prior.py:100-118`, `_merged_recover.py:686-695` | **(c)** for age | already documented in `docs/evidence/order34_recency_2026-08-17/PACKET_RECENCY.md` |

---

## 3 · THE MATERIALITY TABLE

Every number is the change in **board points** when that one site — and nothing else — is corrected
in memory, then undone. Baseline is the repaired Candidate 32 with `RL_O32=1`: **dean 2,400 ·
duff-tytler 1,572 · murdock 170**, which reproduces PACKET_C §5's repaired column exactly (asserted
in the harness; it halts if it does not).

| site | what was changed | **Δ dean** | **Δ CDT** | murdock (26) | ashcroft (20) | o'sullivan (21) | morris (21) |
|---|---|---:|---:|---:|---:|---:|---:|
| **S1** | projection bar → age-referenced | **+843.5** | **+448.4** | **+0.0** | +638.0 | +494.7 | +538.9 |
| S25-η (bound) | re-mix pedigree de-rate off | +517.9 | +433.0 | +31.5 | +85.5 | +40.4 | +5.6 |
| S25-ρ (ceiling) | production weight → 1 | +674.6 | +389.2 | +66.5 | +378.8 | +451.7 | +375.6 |
| S2-V3 | discount → owner's V3 ladder | +469.5 | +268.9 | +1.2 | +559.8 | +346.1 | +388.2 |
| S22-full | young credit keyed on age | +193.0 | +108.5 | **+0.0** | +299.1 | +515.5 | +743.8 |
| S2-V5 | discount → owner's V5 ladder | +157.2 | +90.0 | −0.8 | +125.0 | +52.3 | +58.7 |
| S5 | reliability shrink removed | +158.9 | +13.0 | +40.7 | +93.5 | +6.0 | −211.7 |
| S22-off | young credit removed (sizes what is paid) | −127.3 | −115.1 | +0.0 | +0.0 | +0.0 | +0.0 |
| S4 | un-compress ρ → age-referenced | −44.4 | +30.7 | **+0.0** | −126.2 | −32.3 | +190.3 |
| S3 | v7 relax gate → age-referenced | **+0.0** | **+0.0** | +0.0 | +0.0 | +3.9 | +7.1 |
| S6 | upside-fade bar → age-referenced | **+0.0** | **+0.0** | +0.0 | +0.0 | +40.0 | +0.0 |
| S7 | decliner-shed bar → age-referenced | **+0.0** | **+0.0** | +0.0 | +0.0 | +0.0 | +0.0 |
| S18 | D8 staleness bar → age-referenced | **+0.0** | **+0.0** | +0.0 | +0.0 | +0.0 | +0.0 |
| S19 | decay-gate bar → age-referenced | **+0.0** | **+0.0** | +0.0 | +0.0 | +0.0 | +0.0 |
| S20 | ITEM-C bar → age-referenced | **+0.0** | **+0.0** | +0.0 | +0.0 | +0.0 | +0.0 |

**Joint counterfactuals** (the decomposition is not additive, and here is the proof):

| joint | Δ dean | Δ CDT | murdock | ashcroft | o'sullivan | morris |
|---|---:|---:|---:|---:|---:|---:|
| S1 + S22-full | +1139.2 | +611.7 | +0.0 | +1011.4 | +1131.4 | +1438.4 |
| every class-(b) site anywhere | +996.4 | +640.9 | **+0.0** | +771.3 | +1104.9 | +1719.8 |
| S1 + S2(V5) | +1007.7 | +542.3 | −0.8 | +767.8 | +548.0 | +598.5 |
| S1 + S4 + S2(V5) | +862.3 | +566.6 | −0.8 | +534.2 | +482.3 | +811.5 |
| **all class-(b) sites inside `Phat`** | **+716.2** | **+474.5** | **+0.0** | +422.9 | +473.4 | +757.2 |
| S1 + S4 | +716.2 | +474.5 | +0.0 | +422.9 | +432.5 | +749.8 |

### 3.1 · The controls, stated plainly

- **milan-murdock (26) held at exactly 0.00 board points for every age-correction** — S1, S3, S4,
  S6, S7, S18, S19, S20, and every joint of them. Not "within rounding"; exactly zero. That is the
  cap law: the correction is defined to be zero from age 24, so a mature row cannot be touched.
- **murdock DID move on three experiments — and none of them is an age correction.** S5 (+40.7)
  removes a reliability shrink that has nothing to do with age. S2 (−0.8) changes the discount rate
  for everybody. S25 (+31.5 / +66.5) changes the games-keyed re-mix. This distinction matters: it
  is the difference between "age-referencing the bar" and "loosening the engine".
- **The three young controls all move a lot** on S1: ashcroft +638, o'sullivan +495, morris +539.
  **This is the finding, not a side effect.** S1 is not a dean-and-duff-tytler fix. It re-prices
  every under-24 row on the board that produces anything at all.

### 3.2 · Where the counterfactual could NOT cleanly isolate a site — said, not hidden

- **S1 IS clean, and that was tested rather than assumed.** Under the full S1 correction the
  year-zero value, the day-0 pedigree leg, the entry anchor, the production weight `rho31`, the
  pedigree weight `pi` and the age credit all move by **0.0000000000**. S1 moves the production leg
  and nothing else. (`ISOLATE_E_out.txt`.)
- **S1 and S4 are coupled, and the coupling runs the wrong way.** Alone, S1 gives dean +843.5 and
  S4 gives him −44.4. Together they give **+716.2**, not +799. The reason is mechanical: once the
  bar is age-referenced, dean's realised output margin flips from −8.7 to positive, which switches
  the un-compress map ON — and that map pulls a high production number DOWN (the same behaviour the
  engine's own register items 221/224 recorded). So S4's cost against dean is **−127 points when S1
  is live** versus −44 on its own. Reported as a range, not a point.
- **S19's isolation carries a caveat.** The decay-gate bar is an inline expression that cannot be
  rebound, so it was measured by the algebraically identical route of scaling `bestlvl`. `bestlvl`
  has one other consumer, the RUCK ceiling. No row measured here is a ruck, so the isolation holds
  for these numbers and would **not** hold for a ruck.
- **S25 is not a `Phat` site and its numbers are bounds, not proposals.** "η = 0" deletes a term of
  the ruled re-mix that the owner's own mature-row identity gate has already pinned. "ρ → 1" gives
  the production leg full weight while leaving the pedigree leg in place, which double-counts by
  construction. Both are reported as ceilings so their size is a number rather than a paragraph.

---

## 4 · THE STRUCTURAL FINDING THE TABLE ALONE HIDES

The full S1 correction lifts dean's **production leg** from 2,686 to **4,117** — a rise of **1,431
board points**. Only **843** of that reaches his price. The other 588 points are discarded by the
production weight `rho31(17) = 0.589`, which is keyed on career games and knows nothing about age.
For duff-tytler: production leg 1,622 → 2,441, a rise of **819**, of which **448** survives; 371
points are discarded by `rho31(13) = 0.547`.

Stated plainly: **the engine has two age-blind layers stacked on top of each other.** The first
(S1) judges a 19-year-old's output against a 26-year-old's bar. The second (S25) then discounts
whatever is left because he has not played many games — as though a 19-year-old with 17 games and a
27-year-old with 17 career games were the same kind of evidence. Fixing the first is worth roughly
half of what it looks like, because the second takes the rest.

That second layer is the ruled re-mix. It is **out of this seat's scope** and it is named here, not
touched.

---

## 5 · THE VERDICT TABLE

Sites ranked by |Δ dean| + |Δ duff-tytler|, board points.

| rank | site | Δ dean | Δ CDT | sum | is it a `Phat` site? |
|---:|---|---:|---:|---:|---|
| 1 | **S1 — the projection replacement bar** | +843.5 | +448.4 | **1291.9** | **yes** |
| 2 | S25 — the re-mix (bound only) | +517.9 | +433.0 | 950.9 | no — the ruled re-mix |
| 3 | S2-V3 — the discount ladder | +469.5 | +268.9 | 738.4 | yes |
| 4 | S22 — the young credit, age-keyed | +193.0 | +108.5 | 301.5 | applied at the leg's output |
| 5 | S2-V5 — the milder discount ladder | +157.2 | +90.0 | 247.2 | yes |
| 6 | S22 — the young credit, sized by removal | −127.3 | −115.1 | 242.4 | applied at the leg's output |
| 7 | S5 — the reliability shrink | +158.9 | +13.0 | 172.0 | yes, but not an age correction |
| 8 | S4 — the un-compress ρ axis | −44.4 | +30.7 | 75.1 | yes |
| =9 | S3 · S6 · S7 · S18 · S19 · S20 | 0.0 | 0.0 | 0.0 | six sites, all structurally inert |

### 5.1 · Does any minimal set reach dean ≈ 2,600 and CDT ≈ 1,800?

The target is their Candidate-31 levels: dean 2,670 and duff-tytler 1,832; the owner's stated
neighbourhood is 2,600+ and 1,800+.

The S1 correction was run at doses. λ is the fraction of the engine's own measured development gap
applied to the bar. λ = 0 is today's board; λ = 1 is the full age-referenced bar.

| λ | dean | **CDT** | murdock | ashcroft | o'sullivan | morris | reaches? |
|---:|---:|---:|---:|---:|---:|---:|---|
| 0.00 | 2400 | 1572 | 170 | 3173 | 2376 | 2682 | baseline |
| 0.20 | 2486 | 1605 | 170 | 3280 | 2468 | 2787 | neither |
| 0.30 | 2547 | 1628 | 170 | 3338 | 2516 | 2841 | neither |
| **0.37** | **~2600** | ~1650 | 170 | ~3380 | ~2550 | ~2880 | **dean only** |
| 0.40 | 2621 | 1657 | 170 | 3399 | 2565 | 2895 | dean only |
| 0.50 | 2708 | 1694 | 170 | 3463 | 2615 | 2949 | dean only |
| **0.70** | ~2900 | **~1800** | 170 | ~3590 | ~2715 | ~3055 | **both** |
| 1.00 | 3244 | 2020 | 170 | 3811 | 2871 | 3221 | both, badly overshot |

Other single sites, whole:

| set | dean | CDT | reaches? |
|---|---:|---:|---|
| S2 · owner's V5 discount ladder | 2558 | 1662 | neither |
| S2 · owner's V3 discount ladder | 2870 | 1841 | **both** |
| S22 · young credit keyed on age | 2594 | 1680 | neither |
| S1 λ=0.20 + S2 V5 | 2644 | 1696 | dean only |
| S1 λ=0.30 + S2 V5 | 2705 | 1719 | dean only |
| S1 λ=0.20 + S2 V3 | 2958 | 1876 | **both** |
| S1 full (λ=1.00) | 3244 | 2020 | **both** |

Three sets reach both. **All three breach the +14% rule — see §6.** The narrowest one that reaches
dean alone (S1 at λ≈0.37) sits right on the line with no margin.

**duff-tytler is the harder of the two, by a lot.** Dean needs his production leg lifted 12.6% to
gain the 200 points he wants. Duff-tytler needs his lifted 26% to gain his 228, because his
production leg is smaller relative to his pedigree leg and his production weight is lower (0.547
against 0.589). Any lever that lands dean will leave duff-tytler short; any lever that lands
duff-tytler will send dean past 2,900.

---

## 6 · WHAT THESE COUNTERFACTUALS DO TO THE CLASS AND TO THE FIVE BANDS

### 6.1 · The year-1 class

The brief says "the ~105-row year-1 class". On this store no reading of the draft-2025 intake
reaches 105, and the packet says so rather than quietly picking one:

- national-draft, picked, active, non-pool, drafted 2025: **58 rows**
- every active row drafted 2025 including all pool pathways: **102 rows**

The 58-row national-draft class is the one used below, and the row count is printed with every
number.

### 6.2 · The five-band year-1 economics — WHAT THIS TABLE IS, AND WHAT IT IS NOT

**The standing five-band instrument was NOT re-run.** It reads a walk-forward per-entrant matrix
over the 2004-2022 draft classes, which is a multi-thousand-row re-price outside this seat's budget.
`PREREG_E.md` §5 registered that substitution **before** any measurement, and here is what was run
instead:

For each draft class C in 2021-2025, each player's record is truncated to seasons ≤ C+1, the
engine's clocks are pinned to C+1, and his year-1 value is read as `ev(p, C+1)`. His year-0 value is
`v0_start(p)` — the same year-zero object the committed instrument reads. **n = 272 cells** (49 / 42
/ 59 / 64 / 58 by class).

Two departures from the standing table, both disclosed:

1. **Different population and window.** The standing table is a walk-forward over 2004-2022; this is
   a single-store as-of read over 2021-2025.
2. **This read is survivor-only.** A row already delisted or retired is excluded, whereas the
   standing instrument keeps busts in the denominator at zero. That biases these levels **up**.

**Therefore the levels below are NOT the standing instrument's numbers and are never quoted as such.
Read the MOVEMENT between baseline and counterfactual, measured on the identical population.**

| scenario | yr1 class mean | picks 1-10 | 11-20 | 21-30 | 31-40 | 41-64 |
|---|---:|---:|---:|---:|---:|---:|
| baseline (repaired C32), this read | 801.7 | +13.51% | −0.30% | −10.50% | −7.99% | +0.52% |
| S1 λ=0.20 | 824.7 | +17.40% | +2.56% | −9.08% | −6.49% | +3.17% |
| S1 λ=0.30 | 838.2 | +19.61% | +4.29% | −8.19% | −5.49% | +4.78% |
| S1 λ=0.40 | 853.2 | +22.01% | +6.25% | −7.14% | −4.26% | +6.60% |
| S1 λ=0.72 | 912.8 | +31.00% | +13.99% | −2.35% | +1.84% | +14.19% |
| S1 λ=1.00 | 979.5 | +40.31% | +22.63% | +3.82% | +10.34% | +23.42% |
| S2 V5 ladder | 833.3 | +18.81% | +3.41% | −7.86% | −5.06% | +3.26% |
| S2 V3 ladder | 895.2 | +29.12% | +10.66% | −2.71% | +0.73% | +8.85% |
| S22 age-keyed | 836.4 | +19.29% | +3.93% | −7.79% | −4.69% | +3.50% |
| S1 λ=0.20 + S2 V5 | 856.5 | +22.74% | +6.30% | −6.42% | −3.53% | +5.95% |

**The movement, in percentage points of appreciation — this is the transferable number:**

| scenario | 1-10 | 11-20 | 21-30 | 31-40 | 41-64 |
|---|---:|---:|---:|---:|---:|
| S1 λ=0.20 | +3.90 | +2.85 | +1.42 | +1.50 | +2.66 |
| S1 λ=0.30 | +6.11 | +4.59 | +2.31 | +2.50 | +4.27 |
| S1 λ=0.40 | +8.51 | +6.55 | +3.36 | +3.73 | +6.09 |
| S1 λ=0.72 | +17.49 | +14.29 | +8.15 | +9.83 | +13.68 |
| S1 λ=1.00 | +26.80 | +22.93 | +14.32 | +18.33 | +22.91 |
| S2 V5 | +5.30 | +3.71 | +2.64 | +2.93 | +2.75 |
| S2 V3 | +15.61 | +10.96 | +7.80 | +8.72 | +8.34 |
| S22 age-keyed | +5.78 | +4.23 | +2.71 | +3.31 | +2.98 |

### 6.3 · The two-sided call, made carefully

The standing committed table for the repaired Candidate 32 (PACKET_C §6) reads **+6.10%** on picks
1-10 and **+7.40%** on picks 11-20. Adding the measured movement above to those committed levels
gives an **estimate** — labelled as an estimate, because it assumes the movement transfers across
the two populations:

| dose | what it delivers | est. picks 1-10 | est. picks 11-20 | halt (+14%)? |
|---|---|---:|---:|---|
| λ ≈ 0.37 | dean ≈ 2,600, CDT ≈ 1,650 | ≈ **+13.9%** | ≈ **+13.4%** | **on the line, no margin** |
| λ = 0.40 | dean 2,621, CDT 1,657 | ≈ +14.6% | ≈ +13.9% | **1-10 BREACHES** |
| λ ≈ 0.70 | dean ≈ 2,900, **CDT ≈ 1,800** | ≈ **+23.0%** | ≈ **+21.2%** | **BOTH BREACH badly** |
| λ = 1.00 | dean 3,244, CDT 2,020 | ≈ +32.9% | ≈ +30.3% | **BOTH BREACH badly** |
| S2 V3 alone | dean 2,870, **CDT 1,841** | ≈ **+21.7%** | ≈ **+18.4%** | **BOTH BREACH** |

**The conclusion, stated without softening: every counterfactual that lands duff-tytler at 1,800
also pushes the early bands into buy-side red past +14%, on both this seat's read and on the
transferred committed levels.** The late bands do move the right way — picks 31-40 goes from −7.99%
to −4.26% at λ=0.40 and to +1.84% at λ=0.72, which is real relief on the standing sell-side reds —
but it is bought at the early bands' expense.

The year-1 class mean rises from 801.7 to 853.2 (+6.4%) at λ=0.40 and to 912.8 (+13.9%) at λ=0.72.

---

## 7 · REPRODUCTION RECIPES

Lane, on every run: `PATH=/root/rl_venv312/bin:$PATH`, `RL_O32=1`, `PYTHONHASHSEED=0`,
`OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
VECLIB_MAXIMUM_THREADS=1`, `RL_GAMMA=1.0 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72
RL_PRIOR_TREES=400 PAR_RAMPS=22`, `RL_V0SURF_PKL=<repo>/data/v0surf.pkl`. Strictly sequential; the
engine is loaded once, read-only, in-process.

The age bar used by every age-correction is the engine's own object:
`bar(pos, age) = flat_bar(pos) − O32_GATE_DELTA[TALL|SMALL][clamp(int(age),18,23)]`, zero from age
24. TALL = KPD/KPF/RUCK. The table is at `_merged_recover.py:3332-3335`.

| site | the exact perturbation |
|---|---|
| S1 | `MA.proj_from_peak` and `MA.prod_floor` are replaced by line-for-line copies of `_proj_w4` / `_prod_floor_w4` / `rl_model.proj_from_peak` / `rl_model.prod_floor` in which the single expression `MA.REPL[x]` becomes `MA.REPL[x] − λ·Δ(x, age_at_that_horizon)`. **Identity control: with Δ ≡ 0 the copies reproduce every measured price to 0.0000000000 board points** (`MEASURE_E_out.txt`, first block). |
| S2 | `MA.AGE_DISC = True; MA.AGE_DISC_MODE = '5'` (or `'3'`) — the engine's own declared, already-built dial |
| S3 | `_v7`'s `_lcr` test reads `MA.REPL[pos] − Δ(pos, age)` instead of `MA.REPL[pos]` |
| S4 | `rho_out`'s per-season margin becomes `avg_s − (MA.REPL[pos] − Δ(pos, age in that season))`; `RHO_DEN` untouched |
| S5 | `cp._lvl_eff` returns `cp._lvl_wt` (the shrink removed) |
| S6 | `_inferM1`'s `bar` becomes `MA.REPL[pos] − 3.0 − Δ(pos, age)` |
| S7 | `_est`'s shed argument becomes `Lc − (MA.REPL[pos] − Δ(pos, age))` |
| S18 | `_staleness_grade`'s `qv` denominator becomes `MA.REPL[pos] − Δ(pos, age)` |
| S19 | `bestlvl` scaled by `flat/aged` (algebraically identical to lowering the gate's par; the one-consumer property is asserted at `_merged_recover.py:2576-2578`) |
| S20 | `_c_w`'s `par` becomes `_O30BP_BARS[pos] − Δ(pos, age)` |
| S22-off | `_ycred_mult` returns 1.0 |
| S22-full | `φ = 1` for rows under 24, otherwise unchanged |
| S25-η | `O32_ETA = 0.0` |
| S25-ρ | `rho31(g) = 1.0` for `g > 0` |

Every experiment is followed by the uninstaller and a re-price of all six rows; the harness asserts
they return to the baseline exactly. That assert passed on every run recorded here.

**Files** (all in `docs/evidence/order_e_diag_2026-08-17/`):
`PREREG_E.md` (pushed first) · `loadeng.py` (engine loader) · `cf.py` (the counterfactual
installers) · `measure.py` + `MATERIALITY_E.json` + `MEASURE_E_out.txt` (the site sweep and the
joints) · `dose.py` + `DOSE_E.json` + `DOSE_E_out.txt` (the S1 dose-response and the live-board
class read) · `verdict.py` + `VERDICT_E.json` + `VERDICT_E_out.txt` (the minimal-set search) ·
`bands.py` + `BANDS_E.json` + `BANDS_E_out.txt` (the as-of five-band economics) · `isolate.py` +
`ISOLATE_E.json` + `ISOLATE_E_out.txt` (the leak check and the leg decomposition).

---

## 8 · WHAT THIS SEAT DOES **NOT** SAY

This is a diagnostic. It does not recommend wiring anything.

- It does not say S1 should be corrected. It says S1 costs dean 843 points and duff-tytler 448,
  verified, and that correcting it enough to reach duff-tytler breaks the +14% rule.
- It does not say the re-mix should be loosened. It says the re-mix discards 41% of any `Phat`
  correction for dean and 45% for duff-tytler, and that this is where the rest of the money is.
- It does not claim the five-band numbers are the standing instrument's. They are a labelled
  as-of proxy, and the transfer to the committed levels is labelled an estimate.
- It does not claim any of the zero-valued sites are unimportant. It claims they are **inert on
  these two rows on this lane**, names the gate that makes each one inert, and leaves them on the
  list.

*— ORDER E diagnostic seat. Read-only. Nothing landed, nothing proposed, the owner's word decides.*
