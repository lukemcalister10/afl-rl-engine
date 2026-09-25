# ORDER 18 — DOES THE NATIONAL-DRAFT SITTER PENALTY REDISTRIBUTE?

**Answer: NO. It redistributes nothing. It is a 6.12% NET CHARGE on national draft picks 1–64, and
because the ND pick curve is already taught on sitter-inclusive returns, it is a DOUBLE CHARGE.**

Instrument: `nd_sitter.py` (this dir) · output `nd_sitter_out.txt` · data `ND_SITTER.json`
Pre-registration: `PREREG_ORDER18.md`, written and committed before the run.
Pins asserted at entry **and** exit, both UNMOVED:
board `94f1fec59f99c59d5890d5975c79fa9b` · store `d9a24282357cf3083b1640466e3ecd83` ·
instrument `noarb_table_338.py` `0f8220351c64c56ccfa90c60edcdfa5f`.
**Nothing was wired. No engine configuration changed. The shipped board was not touched.**

---

## THE OWNER'S QUESTION, AND THE DIRECT ANSWER

> "Does the ND sitter penalty redistribute? As if we are penalising 5x for some sitters, that would be
> a huge redistribution to those who don't."

The **5x is real and is exceeded** — the harshest cell on ND 1–64 is charged **6.10x** (`R = 0.1640`).
But the second half of the sentence does not follow, and that is the finding:

**The value taken off those sitters does not go to "those who don't". It leaves the cohort entirely.**

Measured, not assumed. The multiplier actually applied to an ND non-sitter cell, over all 5,277 of
them, takes exactly one distinct value: **`[1.0]`**. There is no uplift term anywhere on the national
arm. `_h_cut` is gated on `p['_pool']` so no ND row reaches it; `sitout_ev` multiplies only the
sitter's own anchor. Nobody is uplifted, in any band, in any class.

---

## 1. THE HEADLINE — ND PICKS 1–64

Population: the phase-1 cell construction, national arm, `stream == 'ND 1-64'`, complete-window
`Y <= 2021`. Weight `e = entry_anchor`. Sitter multiplier `R = _R_surf(cls, effpk, float(d))` at the
row's **own** pick — not clamped to the pool index.

| quantity | value |
|---|---|
| cells | 6,662 |
| sitter cells | 1,385 |
| sitter share (by count) | 0.2079 |
| **sitter share (entry-weighted)** | **0.1394** |
| **mean R among sitters** | **0.5613** (average sitter charged 1.78x) |
| **HEADLINE MEAN** | **0.938846** |
| **NET CHARGE** | **−0.061154 (−6.12%)** |
| **VERDICT** | **NET CHARGE — BREACH of the mean-preserving law** |
| **required uplift U** | **1.071060** |
| uplift actually carried by an ND non-sitter | **1.000000** — a 7.11% shortfall on every one |

Cross-check with `e = v0_start`: mean 0.938846, net −0.061154 — **identical to twelve places**, because
`entry_anchor(p)` returns `v0_start(p)` for any non-pool row (`_merged_recover.py:1852-1857`). The
denominator ambiguity phase 1 had to disclose for the pool does not arise on the national arm; the
script verifies `max |entry_anchor − v0_start| = 0` over all 6,662 cells rather than asserting it.

Unweighted per-cell mean multiplier: 0.904672 (reported so the weighting choice is visible).

---

## 2. THE BREAKDOWN

### By pick band (the engine's own board `RANGES`)

| band | cells | sitters | sit share (wtd) | mean R | mean | net charge | U needed |
|---|---|---|---|---|---|---|---|
| 1–10 | 1407 | 100 | 0.0577 | 0.5607 | 0.974632 | **−0.025368** | 1.026922 |
| 11–20 | 1273 | 181 | 0.1339 | 0.6128 | 0.948153 | **−0.051847** | 1.059863 |
| 21–30 | 1033 | 213 | 0.1987 | 0.5666 | 0.913882 | **−0.086118** | 1.107472 |
| 31–45 | 1502 | 419 | 0.2817 | 0.5448 | 0.871765 | **−0.128235** | 1.178530 |
| 46–64 | 1447 | 472 | 0.3239 | 0.5150 | 0.842898 | **−0.157102** | 1.232381 |

**Spread −0.0254 to −0.1571, range 0.1317 — a 6.2x span across the draft.** Monotone: every later
band is charged harder than the one before it. The charge is driven far more by the **sitter share**
(0.058 → 0.324, a 5.6x rise) than by `R` itself (0.561 → 0.515, roughly flat). Late first-rounders and
second-rounders carry the overwhelming bulk of a charge that pick 1–10 barely feels.

### By position class

| class | cells | sitters | sit share (wtd) | mean R | mean | net charge | U needed |
|---|---|---|---|---|---|---|---|
| nonKPP | 4656 | 864 | 0.1204 | 0.5454 | 0.945255 | **−0.054745** | 1.062241 |
| KPP | 1558 | 379 | 0.1840 | 0.5473 | 0.916687 | **−0.083313** | 1.102102 |
| RUCK | 448 | 142 | 0.2204 | 0.6795 | 0.929379 | **−0.070621** | 1.090583 |

**Spread −0.0547 to −0.0833, range 0.0286** — far tighter than the pick-band spread. Note the
inversion worth naming: RUCK has by far the **mildest per-sitter** treatment (`mean R` 0.6795 vs
~0.545 for the other two) yet lands a **harsher net charge than nonKPP**, because its sitter share is
nearly double. The class differential is a sitter-frequency effect, not a surface-severity effect.

### By depth of sit-out

| depth | sitters | mean R | min R | harshest |
|---|---|---|---|---|
| d1 | 757 | 0.6321 | 0.5470 | 1.83x |
| d2 | 373 | 0.4422 | 0.3880 | 2.58x |
| d3 | 154 | 0.4273 | 0.3450 | 2.90x |
| d4 | 58 | 0.4017 | 0.2390 | 4.18x |
| d5 | 26 | 0.4229 | 0.1640 | 6.10x |
| d6 | 10 | 0.3244 | 0.1640 | 6.10x |

---

## 3. THE CALIBRATION QUESTION — THE CRUX, SETTLED FROM THE CODE

**Never-established players are INSIDE the curve-teaching population, at value 0.0. Stated without
hedging, because the code is unambiguous.**

The chain, each link readable:

- `realised_full(r)` (`harness_pvc_REPINNED_pass3.py:313`) → `if never_established(r): return 0.0`
- `sofar(r, t)` (`:318`) → `return 0.0 if never_established(r) else realised_at(r, t)`
- `structural_values(ND)` (`:339`) iterates **all** of `ND`. A concluded never-established row is
  appended with `value = realised_full(r) = 0.0`, `how = 'concluded_realised'`. An unconcluded one
  with written depth takes `sofar(r,T) * ratio = 0.0`. **Neither path drops the row.**
- `load_matrix` (`:325`) filters on `teaches_curve`, which is a **membership** flag —
  `rl_model.py:313`: `_teaches_curve(p) = _in_pvc(p) and not is_pool(p)`. It selects national,
  in-window, non-pool rows. **It is not a survivorship filter.**
- `kernel_raw` (`:396`) then takes a weighted **mean** over `max(r['value'], 0.0)` across all rows —
  so each zero sits in the numerator as zero **and in the denominator as one**.

Measured on the committed store-`37ced3ce` pair (see caveat below):

| quantity | value |
|---|---|
| ND teaching population | 1,197 |
| never-established rows (no season of `QUAL_GAMES = 6` games) | **262 (21.89%)** |
| of those, inside the teaching population | **262 — all of them** |
| of those, teaching **exactly 0.0** | **262 — all of them** |
| of those, teaching non-zero via prior fallback | **0** |
| their contribution to the summed teaching value | **0.0** of 1,039,851.5 |
| provenance of the whole population | `concluded_realised` 825, `completed` 301, `prior_fallback_thin` 71 |

The harness says it in its own header, so this is not a reading imposed from outside:

> "**THE ZERO IS UNTOUCHED.** … a career with no season of >= QUAL_GAMES (6) games still teaches 0.0,
> and stays in the denominator. On the #338 matrix 262 of the 1197 teaching rows are never-established
> and every one of them still teaches 0."

**And the original derivation instrument names the rule outright.** `derive_271.py:143-147` — the #271
derivation the harness carries — introduces the same zero and calls it, in its own docstring, exactly
what it is:

> `realised_scar(r)`: "The realised outcome in curve currency: the evidence-weighted mean of the
> walk-forward as-of values, **never-established entered at 0.0 (the survivorship rule)**."
> …followed by `if never_established(r): return 0.0`

So the project itself already identifies this zero as **the survivorship correction**. That closes the
question the order posed. The curve is not calibrated on survivors and then corrected by `R`; the
survivorship correction is *already inside the curve*, under that name, and `R` is a second one.

### THE VERDICT

**The ND pick curve is already calibrated on returns that include the sitters and the busts at zero.
The entry price a pick-N draftee is charged ALREADY has sit-out risk priced into it. Applying `R` on
top is a second charge for the same thing.**

**THE ND SITTER TREATMENT IS A DOUBLE CHARGE, NOT A SURVIVOR-BIAS CORRECTION.**

This is the branch the pre-registered decision rule selected in advance, before the counts were run.
Because the entry price *is* sitter-inclusive, the mean-preserving law **bites on the national arm
exactly as it does on the pool**, and the −6.12% is a breach rather than a defensible correction.

**Disclosure on the store.** The composition-act harness copy pins store `d9a24282` (the current gate
store), but the matrices it pins are not committed to the repo — only the tables derived from them
are. The count therefore runs on the committed self-consistent pair in
`docs/evidence/noarb_338_2026-08-06/` (harness pinned to `37ced3ce` + its own matrix). The script
**verifies rather than assumes** that the deciding functions are identical: `md5` of each harness copy
from `def never_established` to EOF is `cf5cafb62b70db645b1e40679dfaa981` for the noarb-338 copy, the
composition copy, **and the instrument of record** (`session_2026-07-30/item279_step4/scripts/
harness_pvc_REPINNED.py`) — all three identical, and the script refuses to substitute if they are not.
`never_established` is a career property, and the #334 harness header records `EXPECT_N = 1197`
re-measured on every `d9a24282` matrix, so the teaching population is identically sized and keyed.
**The 262 count itself has not been re-run at store `d9a24282`** — see "could not determine" below.

---

## 4. THE POOL COMPARISON

**Control first.** Before reporting anything about the national arm, the script reproduces phase 1's
published pool net-charge column. Max |delta| across all nine pathways = **0.000048 → REPRODUCED**.
The harness is believable.

| arm | net charge | vs ND 1–64 | verdict |
|---|---|---|---|
| **ND 1–64** | **−0.0612** | — | **BREACH** |
| pool RD | −0.0807 | 1.32x | BREACH |
| pool SSP | −0.0920 | 1.50x | BREACH |
| pool MSD | −0.6586 | 10.77x | BREACH |
| pool IRE | −0.3959 | 6.47x | BREACH |
| pool PDA | −0.1198 | 1.96x | BREACH |
| pool PDN | −0.1740 | 2.85x | BREACH |
| pool PDS | −0.1138 | 1.86x | BREACH |
| pool UNR | −0.2022 | 3.31x | BREACH |
| pool ND>64 | −0.0976 | 1.60x | BREACH |

**Plainly: the ND arm breaches the mean-preserving law in the SAME DIRECTION as all nine pool
pathways** — mean below 1.0, net charge, no uplift to anyone. Its magnitude is **the smallest of the
ten**: 0.76x the mildest pool pathway (RD), and 1/10.8th of the harshest (MSD). Every pathway in the
engine, pool and national alike, now measures as a net charge. **There is no arm that complies.**

### A FINDING SURFACED BY THE CONTROL, REPORTED BECAUSE IT WAS MEASURED

Phase 1's published pool net charges are the **H leg alone** — `H_POOLSIT`/`H_UNION`, the objects its
ruling retired. But a pool sitter **also** takes `R` inside `sitout_ev` at the pool index. The composed
`R × H` charge is much larger than the figure the phase-1 ruling was made on:

| pathway | phase-1 published (H only) | R leg only | **composed R × H** |
|---|---|---|---|
| RD | −0.0807 | −0.1675 | **−0.2102** |
| SSP | −0.0920 | −0.1499 | **−0.2064** |
| MSD | −0.6586 | −0.3520 | **−0.7379** |
| IRE | −0.3959 | −0.2522 | **−0.4527** |
| PDA | −0.1198 | −0.2465 | **−0.3062** |
| PDN | −0.1740 | −0.3972 | **−0.4861** |
| PDS | −0.1138 | −0.3017 | **−0.3564** |
| UNR | −0.2022 | −0.2015 | **−0.3291** |
| ND>64 | −0.0976 | −0.2231 | **−0.2726** |

This is a statement about the **completeness of phase 1's figure**, not about its correctness — phase 1
measured the object its ruling was about. It is flagged here because retiring the H leg alone would
leave every pool pathway still in breach on the R leg. This was not asked for; it is reported because
the control measured it. **It is for the supervising seat and the owner, not for this seat to act on.**

---

## 5. PRE-REGISTRATION BREACHES — OWNED, NOT HIDDEN

Six of twelve pre-registered items missed. **Every quantitative miss is in the same direction: I
over-predicted the severity of the ND charge.** Named in full:

| # | quantity | predicted | measured | result |
|---|---|---|---|---|
| P1 | headline mean | 0.87–0.93 | **0.938846** | **BREACH** — above band |
| P2 | net charge | −7% to −13% | **−6.12%** | **BREACH** — milder than predicted |
| P3 | entry-weighted sitter share | 0.15–0.25 | **0.1394** | **BREACH** — below band |
| P4 | mean R among sitters | 0.45–0.60 | 0.5613 | ✓ within band |
| P5 | required uplift U | 1.10–1.18 | **1.0711** | **BREACH** — below band |
| P6 | same direction as pool | net charge | net charge | ✓ confirmed |
| P7 | ND vs RD's −8.07% | **ND larger** | **ND SMALLER (−6.12% vs −8.07%)** | **BREACH — predicted the wrong side** |
| P8 | class ordering | RUCK mildest, KPP harshest | KPP harshest ✓, but **nonKPP mildest, not RUCK** | **PARTIAL BREACH** |
| P9 | later picks charged harder | monotone rise | monotone, −0.025 → −0.157 | ✓ confirmed |
| P10 | who is uplifted | nobody; exactly 1.0 | `[1.0]`, 5,277 cells | ✓ confirmed |
| P11 | never-established share | 18–25% | 21.89% | ✓ within band |
| P12 | NE rows teaching 0.0 | all but prior fallbacks | **262/262, zero fallbacks** | ✓ confirmed, stronger |

**Why P7 went the wrong way — the mechanism, since the miss is instructive.** I reasoned that `R`
(0.15–0.68) is far harsher per sitter than `H_POOLSIT` (0.804), so ND must carry the larger charge. It
does not, because the **entry weighting** dominates: ND 1–64's entry-weighted sitter share is 0.1394
against RD's 0.3527. High picks carry most of the entry value and almost never sit (pick 1–10 sitter
share 0.058), so the harsh multiplier lands on cheap rows. **Severity per sitter and severity per
cohort point in opposite directions here, and I predicted from the first.** The pick-band table is the
same lesson: the 6.2x band spread is a sitter-frequency effect, not a surface-severity effect.

**None of these breaches touches the headline verdict.** P6 and P10 — the two items the owner's
question actually turns on — are confirmed. The charge is milder than predicted and it is still a
charge, and nobody is still nobody.

---

## 6. WHAT THIS SEAT COULD NOT DETERMINE

1. **The 262 never-established count has not been re-run at store `d9a24282`.** The composition-act
   matrices are not committed. The code reading that decides the calibration verdict is
   store-independent and the deciding functions are proven byte-identical across all three harness
   copies, so the verdict does not rest on the count — but the count itself is from `37ced3ce`.
2. **The last link from the teaching population to the shipped entry price was traced but not
   closed.** What *was* established: `v0_start(p)` on the board path reads `_V0CURVE`
   (`_merged_recover.py:1756-1760`); `_V0CURVE` is the frozen year-zero surface loaded from
   `data/v0surf.pkl` (`:1298-1318`), which `refit_v0surf.py` produces by freezing the engine's own
   `_build_v0_curve` fits over `_PVC0` — the adopted PVC pick curve. And the PVC curve is what
   `structural_values()` teaches, on the population measured above. What was **not** established: that
   the shipped `pvc_curve_L1b.json` is that fit's direct output rather than a later re-fit or an
   owner-adjusted ladder (the #328 notes refer to an "adopted curve `df766dff`" installed by ruling).
   If the shipped ladder were fitted on a different, survivor-only population the double-charge verdict
   would need re-testing against it. Nothing seen suggests that, and `derive_271`'s explicit
   "survivorship rule" points the other way — but the end-to-end identity was not verified.
3. **The correct remedy.** Whether the fix is to retire `R` on the ND arm, to rescale it to be
   mean-preserving with an explicit non-sitter uplift `U = 1.0711`, or to re-derive it against a
   sitter-excluded curve, is a design ruling and is **not** measured here.
4. **Whether the composed `R × H` pool finding changes phase 1's conclusion.** Phase 1 is an open PR
   this act must not touch. The composed figures are reported for the supervising seat; their
   consequences for the phase-1 ruling were not assessed.
5. **The in-season `tau` proration.** `sitout_ev` computes `tau = max(0, Y − debutyr) + fe**1.5`, a
   concave within-season accrual. This measurement uses `tau = float(d)` — the integer depth — which is
   exactly the mapping phase 1 used to read the same surface, and is what makes the two directly
   comparable. On a genuine full-season sitter the two coincide at the season boundary, but the effect
   of the fractional term on mid-season cells was not separately quantified.
