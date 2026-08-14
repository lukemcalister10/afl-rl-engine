# SITTER FADE PACKET — ORDER 30A, FOR THE OWNER'S RULING

**NOTHING WIRES UNTIL THE OWNER RULES.** No engine file, no board, no store, no curve moved in this
act. The old `los_decay` schedule is the **DECLARED FALLBACK** and stays operative. This packet is a
measurement and a recommendation; the build act (ORDER 30B) briefs separately, after the ruling.

Brief: [#334 comment 5289933916](https://github.com/lukemcalister10/afl-rl-engine/issues/334#issuecomment-5289933916).
Branch `land/order-29`. Pre-registration `PREREG_30A.md`, committed at `06bd7be` **before**
`o30a_derive.py` existed in runnable form and before any cell was counted; it has not been edited.

**Read in this order:** this packet → `SITTER_DISCOUNT_TABLE.md` (every cell, every n, every
dispersion) → `DERIVE30A_out.txt` (the transcript) → `SITTER_DISCOUNT_TABLE.json` (machine-readable,
including per-player rows).

---

## 1. THE QUESTION

The owner, 2026-08-14, verbatim:

> *"we keep the old formula that was logical but not derived from evidence as a backup plan, and look
> to derive what a reasonable sitter discount would be for players in the ND. Considering all lenses
> — position, draft pick, and years in the system."*

The old formula is a **designed** schedule with no fit provenance (`rl_model.py:725-729`):

```
GRACE = {KPF 2.5, KPD 2.5, RUCK 2.5, MID 1.0, SD 1.0, SF 1.0}
los_decay = exp( -0.16 * max(0, years_since_entry - GRACE[pos])**1.82 )
```

It was never fitted to anything. This act fits it.

---

## 2. THE ANSWER — ONE ROW, AND IT IS NOT CLOSE

**The derived ND sitter discount**, all picks, all positions, on the fitted 2004–2021 population,
against the ORDER-29 landed positional entry law:

| years since entry | 1 | **2** | **3** | **4** | **5** | **6+** |
|---|---:|---:|---:|---:|---:|---:|
| **DERIVED (recommended)** | 1.000 | **0.568** | **0.214** | **0.105** | **0.074** | **0.074** |
| old `los_decay`, MID/SD/SF | 1.000 | 0.852 | 0.568 | 0.307 | 0.136 | 0.050 |
| old `los_decay`, KPF/KPD/RUCK | 1.000 | **1.000** | **0.956** | **0.716** | **0.428** | 0.209 |
| n in cell | 1,140 | 462 | 234 | 154 | 130 | 117 |

**Verdict per depth.**

| depth | verdict |
|---|---|
| **2** (sat one full season) | old is **TOO GENEROUS by 0.28** for smalls and **by 0.43** for KPP/RUCK. The evidence says a one-year sitter is worth **57 %** of a fresh same-pick entrant; the old schedule says 85 % (smalls) or **100 %** (bigs). |
| **3** | old is **TOO GENEROUS by 0.35** for smalls and **by 0.74** for KPP/RUCK. Evidence 21 %; the old schedule prices a KPP three-year sitter at **96 %** of a fresh entrant. |
| **4** | old is **TOO GENEROUS by 0.20 / 0.61**. Evidence 11 %; old 31 % / 72 %. |
| **5** | old is **TOO GENEROUS by 0.06 / 0.35**. Evidence 7 %; old 14 % / 43 %. |
| **6+** | the only place the old schedule is **too harsh**, and only for smalls: old 0.050 vs raw derived 0.091. At this depth the cell is dominated by never-played rows and the derived number is held flat at 0.074 by monotone enforcement. |

**One sentence:** *the designed schedule is too generous to a sitter at every depth the board actually
prices, and its 2.5-year grace for key-position players and rucks is the single largest error in it.*

**The shape.** Re-fitting the old functional form to the derived points gives
`exp(-0.657 · over^0.978)` with **grace 1.0 for every position** — i.e. a **plain exponential decay
at ≈ 0.66 per year of sitting**, not a gently-graced curve that steepens. The shipped `0.16 · over^1.82`
starts far too flat and only catches up after the players have already been mispriced for two years.
The re-fit is offered for continuity of form; the seat recommends the **table**, because the table is
the measurement and the re-fit misses it by up to 0.06 in the middle.

---

## 3. HOW IT WAS MEASURED, IN FIVE LINES

1. **Population.** ND entrants attributed to mechanism `ND 1-64` (force-majeure slide applied, the two
   excluded keys dropped), entry years **2004–2021** — 1,142 rows. **2022+ classes are excluded from
   every fitted number** and reported in their own panel: a recent class cannot show a deep-sit
   outcome, and its "delivered value" is 60–88 % engine projection of the very players in question.
2. **Depth.** `N = 2026 − entry_year` on the engine's own `los()` clock. Still sitting at N = zero
   games in every completed season `k = 1 … N−1`. Cells are nested.
3. **Numerator.** The delivered-value lane's **grace-A** career score, re-anchored to the start of
   year N through the engine's own `disc_factor`. A sitter has delivered nothing before depth N, so
   his whole career score *is* his from-depth-N score.
4. **Denominator.** The **landed entry law** — `pvc_curve_v2.json::nd_v0.posv[drafted position][pick]`.
   Same language as the price the discount will multiply.
5. **Statistic.** `D(N) = mean(V_N/v0 | sitting at N) ÷ mean(V_1/v0 | whole class)`. The
   depth-1 normalisation cancels every level offset between the two bases. **`RAW(1) = 1.0286` — the
   delivered-value scorer and the landed entry law already agree to within 2.9 %, which is itself a
   result worth having.**

**Robustness.** Six independent re-cuts, all published: day-0 anchoring, the flat-14 ladder, the
observed leg with no projected tail, the core window alone, an ever-played bound, and ORDER 21's
winsor-2.0. **Every one puts D(2) in 0.53–0.64, D(3) in 0.21–0.28, D(4) in 0.09–0.14.** The old
schedule sits outside all of those bands at every depth ≥ 2.

**And the pool's own machinery agrees.** Built the ψ way — same-depth norm, winsor 2.0, exactly
ORDER 21's construction, transplanted onto ND — the surface reads **0.590 / 0.288 / 0.148 / 0.093**.
That is within **0.075** of this act's headline at every depth. Two different normalisations, one
answer.

---

## 4. WHICH LENS CARRIES SIGNAL — the owner asked for all three

| lens | verdict | why |
|---|---|---|
| **YEARS IN THE SYSTEM** | **REAL. It carries essentially all the signal, and it is what the seat recommends wiring.** | n = 462 / 234 / 154 at depths 2–4. Monotone on the raw row through depth 5. Reproduced within ±0.06 by six alternative bases and within 0.075 by the pool's own construction. |
| **DRAFT PICK** | **NOT USABLE AS FILED. Do not wire it.** | Non-monotone at depth 2 (0.65 early / 0.44 middle / 0.63 late). The early-pick cells collapse to **n = 4, 3, 2** at depths 4, 5, 6 — borrowing 79 %, 83 %, 88 % from the all-pick row. And the late band is contaminated by Anomaly A2 below. Published in full with n and borrowing on every cell; not recommended. |
| **POSITION** | **SIX-WAY: NO SIGNAL. TWO-WAY: a real but second-order effect the sample supports at depth 2 only.** | RUCK — the cell the 2.5-year grace is really about — has n = 37 / 19 / 11 / 8 / 7 and sits on the artefact denominator; its raw column reads **1.20 at depth 5 and 1.56 at depth 6**, a six-year sitter apparently worth *more* than a fresh entrant. The KPP+RUCK vs nonKPP collapse does hold up in direction: **0.711 vs 0.484** at depth 2, 0.243 vs 0.194 at depth 3, 0.165 vs 0.063 at depth 4. But the gap is **not monotone** and is **4–8× smaller** than the 2.5-year grace implies. |

**On the 2.5-year grace specifically:** its **direction is right** — big bodies do hold value longer
when they sit. Its **size is wrong by a factor of 4 to 8**. Granting a KPP three-year sitter 96 % of a
fresh entrant's price is the largest single error in the shipped schedule.

---

## 5. THE NAMED TEST ROWS — player by player

The comparison the owner asked for: today's 29B flat-v0 print, that same print under the old
`los_decay`, and under the derived discount. **These are arithmetic on a packet. Nothing is wired.**

| player | pathway | pos | pick | entry | depth | career games | **29B flat v0 (today)** | old `los_decay` | **old price** | **derived D** | **DERIVED price** | pick-band variant |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **josh-smillie** | ND 1-64 | MID | 7 | 2024 | 2 | 0 | **1,617** | 0.852 | 1,378 | **0.568** | **919** | 1,058 |
| **harry-demattia** | ND 1-64 | MID | 25 | 2023 | 3 | 0 | **892** | 0.568 | 507 | **0.214** | **191** | 128 |
| **max-knobel** | ND 1-64 | RUCK | 42 | 2022 | 4 | 0 | **834** | **0.716** | 597 | **0.105** | **88** | 116 |
| harrison-ramm | **POOL** (MSD) | KPD | 3 | 2025 | 1 | 5 | live board 523 | 1.000 | – | — | — | — |
| mani-liddy | **POOL** (MSD) | MID | 15 | 2025 | 1 | 9 | live board 152 | 1.000 | – | — | — | — |
| vigo-visentini | **POOL** (RD) | RUCK | 5 | 2023 | 3 | 3 | live board 182 | 0.956 | – | — | — | — |

**Reading the ND rows.**

- **smillie** — the 29B keying reinflated him from 953 to 1,617. The derived discount puts him at
  **919**, which is within 4 % of where the board had him **before** 29B reinflated him. The evidence
  says the pre-29B number was closer to right than the current print, and that the old `los_decay`
  (1,378) is too soft by about 50 %.
- **demattia** — three years, no games, pick 25. Old schedule 507; evidence **191**.
- **knobel** — the clearest case in the packet. He is a RUCK, so the 2.5-year grace protects him: the
  old schedule prices a four-year gameless pick-42 ruck at **0.716 × 834 = 597**. The evidence says
  **0.105 × 834 = 88**. That single row is nearly a **seven-fold** difference and is exactly what
  "the grace is not derived from anything" costs.

**The three pool rows are carried for method-symmetry commentary only.** All three have played
(5, 9, 3 games), so on this act's own definition **none of them is a sitter at all** and no ND-derived
discount is applied to any of them. Under the one-machinery law they would be priced by the **pool's**
own depth object (ORDER 21's `whole_pool` retention, already landed), not by this surface — same
construction, pathway-specific values, which is the owner's law working exactly as written.

---

## 6. THE SEAT'S RECOMMENDATION

**R1 — REPLACE `los_decay` with the depth table, position-blind and pick-blind.**

```
D(years_since_entry) = { 1: 1.000, 2: 0.568, 3: 0.214, 4: 0.105, 5+: 0.074 }
```

*Reasons:* it is the only lens with the sample to support it; it is stable across six independent
re-cuts; the pool's own machinery reproduces it independently; and it removes a schedule that is too
generous at every depth the board prices.

**R2 — DO NOT wire the pick lens.** It is non-monotone at depth 2, its early-pick cells run to n = 4
/ 3 / 2, and its late band is contaminated by the entry law's own deep-tail artefact. Fitting it would
be fitting noise and an artefact at the same time.

**R3 — DO NOT wire the six-way position lens; and if the owner wants a position term at all, wire the
two-way collapse at depth 2 only** (`KPP+RUCK 0.711 / nonKPP 0.484`) and go position-blind beyond.
The seat's own preference is **fully position-blind**: the measured gap is real in direction but
non-monotone in depth, and a non-monotone term wired into a price is a future arbitrage.
**The 2.5-year grace should not survive in any form.**

**R4 — FIX THE DENOMINATOR BEFORE ANYTHING ELSE READS IT.** The landed positional entry law goes to
**zero** at RUCK picks 63–64 and to 84 / 31 at RUCK 60 / 62, 94 / 57 at MID 63 / 64, 18 at SF 64. The
ORDER-29 artifact declares this about itself. It is what makes the RUCK column read 1.56 at depth 6
here, and it will distort **any** act that prices per pick per position. It is handed forward as a
finding, not swept up inside this one.

**R5 — RULE ON THE LISTING LIMIT before wiring, because it sets the direction of the residual error.**
List membership is not observable in Layer 1 (`last_listed` is non-null on 3 of 1,448 ND rows), so a
player delisted after two gameless seasons is still counted in the depth-3+ cells at zero value. That
makes the recommended row a **harsh (lower) bound**. The generous bound — restricting to entrants who
eventually played — gives 0.69 / 0.40 at depths 2 / 3 but is explicit selection on the outcome and
goes uninterpretable past depth 3. **At depth 2, where few rows are delisted, the bound is tight and
the number is solid. At depths 4+ the truth is somewhere above the recommended figure**, and the owner
may reasonably want a floor there.

**R6 — TWO THINGS THIS ACT DOES NOT MEASURE, stated so they are not assumed.**
(a) **The first-game cliff.** A player who plays one game leaves the sitter population entirely; this
surface says nothing about the discontinuity at that boundary. ORDER 30B's "no first-game cliff"
requirement needs its own object.
(b) **Mid-season proration.** The derived table is on **integer** completed seasons. The board prices
mid-2026. ORDER 21 solved the same problem for the pool by interpolating on the engine's own
`tau` clock; the ND wiring should borrow that, not invent a second convention.

**R7 — WHAT THE OWNER SHOULD EXPECT IF HE RULES YES.** This is a **large** repricing of a small
population: 42 year-2+ 0-game rows are wired on today's day-0 print (22 ND 1-64, 20 pool), and the ND
ones move down hard — smillie −43 %, demattia −79 %, knobel −89 % against the current flat print.
Every one of those 42 rows sits in the 2022+ sensitivity tier, i.e. **the players this change would
price contributed nothing to the evidence that prices them** — which is correct discipline, and worth
saying out loud.

---

## 7. THE PREREG, SCORED — 12 HELD, 4 PARTIAL, 10 BREACHED

Nothing in `PREREG_30A.md` was edited. Breaches owned by number.

| # | prediction | verdict | measured |
|---|---|---|---|
| P1 | D(N) monotone decreasing, N = 1–4 | **HELD** | 1.000 / 0.568 / 0.214 / 0.105 |
| P2 | D(2) ∈ [0.70, 0.95]; old within ±0.15 | **BREACHED** | **0.568**; old is off by **0.28** |
| P3 | D(3) ∈ [0.35, 0.65]; old within ±0.20 | **BREACHED** | **0.214**; old is off by **0.35** |
| P4 | D(4+) < 0.30 and harsher than old 0.307 | **HELD** | 0.105 |
| P5 | old too harsh in the middle, too generous at the extremes | **BREACHED — and backwards** | old is too **generous** at every depth 2–5; too harsh only at depth 6, and only for smalls. I predicted the sign of the middle error wrongly. |
| P6 | n(2) ≥ 80 · n(3) ∈ [15,45] · n(4+) < 15 | **BREACHED** | 462 · **234** · **154**. I under-estimated the sitter population by an order of magnitude. |
| P7 | position lens: every six-way cell n < 10 at depth ≥ 3 | **PARTIAL** | only RUCK (19) is near it; KPD 35, KPF 40, MID 65, SD 41, SF 34. The *conclusion* (six-way unusable) survives on artefact grounds, not on n. |
| P8 | every three-way cell unusable at N ≥ 2; publish two two-ways only | **PARTIAL** | done as filed, but depth-2 three-way cells would have averaged ~26, not the handful I expected |
| P9 | at N ≥ 4 no pick band reaches n = 10 | **BREACHED** | 21–40 has 40 and 41–64 has 110 at depth 4; only 1–20 (n = 4) fails |
| P10 | years all the signal · pick second-order but real · position none | **PARTIAL** | years HELD; pick is **not** "real" — it is non-monotone and artefact-contaminated; position's two-way collapse **is** real, which I predicted away |
| P11 | pick 1–20 harsher than 41–64 at the same depth | **BREACHED** | direction **reverses** with depth: 0.675 vs 0.630 at N=2 (early *more* generous), 0.013 vs 0.143 at N=4 (early far harsher) |
| P12 | K-shrinkage borrows > 50 % at N ≥ 3 | **BREACHED** | at depth 3: 42.9 % / 18.3 % / 9.3 %. Only the thinnest cell approaches it. |
| P13 | the 2.5-year KPP/RUCK grace is not supported | **HELD, with a qualification I did not earn** | its **size** is unsupported (4–8× too large) but its **direction** is supported (KPP+RUCK 0.711 vs nonKPP 0.484 at depth 2). I predicted no effect at all. |
| P14 | RAW(1) ∈ [0.70, 1.40] | **HELD** | **1.0286** — the two bases agree to 2.9 % |
| P15 | p25 = 0 at every depth ≥ 2; median/mean < 0.60 | **HELD** | both, at every depth |
| P16 | median exactly 0 at N ≥ 3; recommend the mean | **HELD** | median 0.0000 at N = 3, 4, 5, 6; the mean is recommended |
| P17 | fitted tail share < 0.25 at N=2, < 0.10 at N ≥ 3; 2022+ panel > 0.90 | **BREACHED on the last clause** | fitted 0.081 / 0.044 / 0.023 / 0.008 — held. 2022+ panel **0.878 / 0.756 / 0.598**, all below 0.90. |
| P18 | at least one raw cell non-monotone in depth | **HELD** | the all-pick raw row itself (N=6 0.093 > N=5 0.076), plus the whole RUCK column |
| P19 | ND lands closer to the ORDER-21 pool shape than to `los_decay` at depths 2–3 | **HELD** | N=2: 0.056 from pool vs 0.284 from old. N=3: 0.166 vs 0.354. |
| P20 | pool-norm reading differs by > 0.10 at depth 3, and is more generous | **PARTIAL** | more generous — HELD (0.288 vs 0.214). By > 0.10 — **BREACHED** (0.074). |
| P21 | smillie derived ∈ [1,150, 1,500] | **BREACHED** | **919** |
| P22 | demattia derived ∈ [300, 550] | **BREACHED** | **191** |
| P23 | knobel derived < 400, materially harsher than old | **HELD** | **88** vs old 597 |
| P24 | ramm/liddy/visentini are pool and all carry ≥ 1 game | **HELD** | 5, 9, 3 games; none is a sitter on this act's definition |
| P25 | ≥ 30 of the reinflated year-2+ rows sit in the 2022+ tier | **HELD** (with **A3**) | **42 of 42**. But the total reconciles to **42**, not the brief's 43 — flagged as Anomaly A3, not smoothed over. |
| P26 | the seat will recommend depth-keyed, position-blind, pick-shrunk | **HELD** | R1–R3 |

**What the breaches have in common, owned plainly:** I went in expecting the designed schedule to be
roughly right and the samples to be too thin to say otherwise. **Both assumptions were wrong in the
same direction.** The sitter population is an order of magnitude larger than I predicted (462 / 234 /
154, not ~80 / ~30 / <15), and the evidence is far harsher than the design at every depth. Nine of
the ten clean breaches (P2, P3, P5, P6, P9, P11, P12, P21, P22) are that one mistake, in nine places.

---

## 8. ANOMALIES CARRIED FORWARD

| # | anomaly |
|---|---|
| **A1** | The right tail is **real**, not artefact: 192 of 1,140 depth-1 rows exceed a 2× ratio, headed by `jordan-dawson` (pk 55, 14.9×), `jarryd-lyons` (pk 61), `jase-burgoyne` (pk 60), `thomas-stewart` (pk 40), `errol-gulden` (pk 34), `harris-andrews` (pk 59). Winsorising it away (ORDER 21's guard) cuts `RAW(1)` by 40 % but moves the **normalised** D(N) by < 0.04 at every depth. Both the spike at zero and the tail belong in an expectation. |
| **A2** | **The landed positional entry law goes to ~0 in its own deep tail** (RUCK 63/64 = 0.0; RUCK 60/62 = 84/31; MID 63/64 = 94/57; SF 64 = 18). The ORDER-29 artifact declares this about itself. It distorts the RUCK column and the 41–64 pick band here, and it will distort any future act that reads `posv` per pick per position. **Handed forward, unresolved.** |
| **A3** | The 29B reinflated count reconciles to **42**, not 43 (22 ND 1-64 + 20 pool, on the stated clock). The one-row difference is flagged, not smoothed. |
| **A4** | **Store drift, disclosed not laundered.** The delivered-value scores were built on store `d9a24282`; this branch carries `cb38ef11`. Layer 1 is byte-identical, so the population and every sit fact are unaffected, and the depth-1 normalisation absorbs the level. No DV number was recomputed on the drifted store. |

---

## 9. WHAT THIS ACT DID NOT DO

It did not touch the store, the board, the curve, `rl_model.py`, or any pricing leg. It did not move a
pin. It did not post a GitHub comment. It did not wire a discount, and it did not remove the fallback.

**The old formula stands until the owner says otherwise.**

---

## FILES

| file | what |
|---|---|
| `PREREG_30A.md` | pre-registration — 26 numbered predictions, estimator and censoring rule, committed at `06bd7be` before any measurement |
| `o30a_derive.py` | the harness — reproducible, pin-asserted, read-only |
| `SITTER_DISCOUNT_TABLE.md` | all three lenses, n and dispersion on every cell, the unusable cells named |
| `SITTER_DISCOUNT_TABLE.json` | machine-readable twin, including the 1,142 per-player fitted rows |
| `DERIVE30A_out.txt` | the full transcript |
| `SITTER_FADE_PACKET.md` | this packet |
