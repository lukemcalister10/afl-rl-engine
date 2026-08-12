# SUMMARY — ORDER 26A, in plain language

Read-only forensic order. Nothing under `engine/` was written, no board was built, no pin was moved.
Everything here is measured on the landed matrix `per_entrant_O25R4.json`
(md5 `3c6ffcdeaac9786473f3f017dba1d61e`), store `d9a24282`, v0surf `6ef67f07db98`.

---

## 1. THE ANSWER IN FOUR SENTENCES

The two "yr4/yr0" figures were never in conflict. They share a numerator exactly — both read the
same board mark for the same player in the same season — and they differ almost entirely in **what
they divide by**. The derivation divides by what it costs a club to **sign** a rookie (the signed
level, ~305 for a MID); the all-arm instrument divides by what the board **marks him at** on day
one (~643 on average for a MID). The board prices a pool entrant at about **2.65× what signing him
costs**, and that single fact is **98.65 %** of the 2.7× disagreement.

---

## 2. THE BRIDGE — ZERO RESIDUAL

| step | what changed | reading | delta | share |
|---|---|---|---|---|
| 0 | all-arm as published | 0.508979 | — | — |
| **P** | population: cohort window 2005–2023 → all cohorts | 0.520725 | +0.011746 | **1.35 %** |
| **I** | year indexing: `N=4` → `cohort+3` | 0.520725 | +0.000000 | **0 %** |
| **S** | skip/zero branch semantics | 0.520725 | +0.000000 | **0 %** |
| **A** | aggregation `mean/mean` → `sum/sum` | 0.520725 | +0.000000 | **0 %** |
| **D** | entry price `v0` → signed anchor | **1.379793** | +0.859069 | **98.65 %** |
| = | derivation as published | 1.379793 | | |

**Residual: 0.000e+00.** Not "within tolerance" — exactly zero. Details and named players in
`RECONCILIATION.md`.

---

## 3. HYPOTHESES, EVERY ONE SCORED

### H1 (OWNER'S) — survivor bias through the skip branches → **FALSIFIED as the mechanism; the owner's NUMBER was right for a different reason**

The claim was that the 1.38 is survivors-over-their-own-entry because the `continue` branches drop
the dead out of the denominator. **It is not.** Measured on the derivation's own RD population:

- entry price **kept** in the denominator (not skipped): **96.54 %** — the skip branches drop almost
  nothing;
- the 24 rows they do drop are cohorts 2024–2026, whose year 4 has not happened yet;
- **406 of the 667 rows read score exactly 0.0 and stay in the denominator.** The pool's dead are
  zeroed, not skipped. The 1.38 is a genuine all-in figure.
- And decisively: the all-arm instrument carries **the same branches** (`reached` filter = `Y > W`
  skip; `'pre'` = `Y < yrs[0]` skip; `'ended'` = zeroed and kept). Bridge step S moved **0.000000**.

The owner's numeric check was: if H1 holds, surviving entry share ≈ 0.509/1.380 ≈ **36.9 %**.
**Measured: 38.01 %** of total RD entry (anchor basis), 37.68 % on the v0 basis, 39.37 % of the
entry actually kept in the denominator. **The owner's number lands within about one point.** But it
is not the share the skip branches remove — it is the share of RD entry belonging to players still
carrying a non-zero mark at year 4. The owner correctly sensed that ~37 % of the rookie book is
alive at year 4; he attributed it to the wrong branch. The intuition was sound, the mechanism was
not.

### H2 — the value object is not the board as-of mark → **FALSIFIED as bridge mass; confirmed as background**

**0 numerator mismatches** across the shared 623-row RD population. Both instruments read the same
`vpath[i]` at the same calendar year. `vpath` **is** the board's as-of mark series; it is not a
transformed series, and it contributes **nothing** to this gap.

The transformed object does exist, but it is elsewhere: `realised_full()` — a `pw`-weighted career
mean over `vpath` — is the CAREER PROFILE basis on which the signed levels were derived. It never
appears in either yr4 reading. It matters because it is *why* the signed anchor is what it is, which
is why H2's spirit is vindicated one level down: see the wedge.

### H3 — the year-indexing off-by-one → **FALSIFIED, exactly as pre-registered**

Measured, not assumed, across all 2644 eligible rows: **0 rows** where the two year keys differ.
`N=4` resolves through `cohort + N − 1` to `cohort + 3`. Prediction was 0 rows; measured 0 rows.
There is no off-by-one.

### H4 (OWNER'S YARDSTICK) — ND survivors at yr4–5 read ≈ 2.2–3.1× their own entry → **FALSIFIED**

| measure | value | verdict |
|---|---|---|
| NATIONAL survivors' own entry, calendar yr4 | **1.7452** | below the 2.2–3.1 band |
| NATIONAL survivors' own entry, calendar yr5 | **1.8571** | below |
| NATIONAL survivors, career-age a=4 | **1.8310** | below |
| NATIONAL survivors, career-age a=5 | **1.9272** | below |

The band assumed a national surviving-entry share of 0.5–0.7. **Measured: 0.8909.** The national
arm's mortality is much lower than assumed, so the yardstick is lower — ~1.75–1.93×, not 2.2–3.1×.
This makes the pool look *better* after the entry fix, not worse.

**Pool vs ND survivor own-entry trajectories, both axes** (the comparison the brief demanded):

| | calendar yr4 | calendar yr5 | career-age a=4 | career-age a=5 |
|---|---|---|---|---|
| NATIONAL survivors | 1.7452 | 1.8571 | 1.8310 | 1.9272 |
| RD survivors @ signed anchor | 3.5047 | 3.9442 | 4.1627 | 4.3910 |
| RD survivors @ board v0 | 1.3328 | 1.5176 | 1.6053 | 1.7239 |
| **RD@anchor ÷ NATIONAL** | **2.008×** | **2.124×** | **2.274×** | **2.278×** |

**The timing offset the brief warned about is real but small.** Measured first-play offset from
cohort: national +0.502 seasons, RD +0.773 — a difference of 0.27 seasons, and 0.419 seasons once
entry-weighted at year 4. Reweighting the national yardstick onto the pool's own career-age mix
moves it from 1.7668 to 1.6923: **the timing leg is 1.0440×, i.e. 4.4 %.** It is separated and it
does not carry the finding.

### H5 (MINE) — the bridge closes on population + denominator alone → **CONFIRMED**

Steps I, S and A each moved exactly 0.000000. P moved 1.35 %, D moved 98.65 %. Nothing was absorbed
into a residual.

---

## 4. THE WEDGE, DECOMPOSED

On the derivation's own all-in convention at year 4:

**TOTAL 2.9857× = ENTRY-INFLATION 2.6498× (89.1 %) × TIMING 1.0440× (3.9 %) × MARK-RESIDUAL
1.0793× (7.0 %).** Exact; check residual 0.00e+00.

On the owner's survivors' convention: **TOTAL 1.3094× = ENTRY 2.6295× × TIMING 1.0440× ×
MARK-RESIDUAL 0.4770×** — a mark-residual **below 1**, meaning pool survivors marked **2.097× above**
the national survivor yardstick once entry is restated.

**So: (i) entry-inflation is 89 % of the wedge and (ii) mark-suppression is 7 % of it — and on the
survivors' convention (ii) is negative.** There is no suppression of living pool players to correct.

**Why the two conventions disagree — the mortality identity** (exact, since the dead score 0 and
keep their entry in the denominator):

```
ALL-IN = SURVIVORS' own-entry × SURVIVING ENTRY SHARE
NATIONAL   1.5547 = 1.7452 × 0.8909
RD@anchor  1.3798 = 3.5047 × 0.3937
```

Pool survivors are marked **2.008×** the national level per unit of signed entry, but only
**0.442×** as much pool entry survives. The two nearly cancel to 0.887 — exactly the 1.3798/1.5547
the derivation reads. **The pool board is barbell-shaped: more of it dies, and what lives is marked
much higher.** The signed levels already absorbed that trade, because `realised_full` is an all-in
career average carrying the deaths at 0.

---

## 5. THE PLAIN-LANGUAGE ANSWER FOR ORDER 26B

**Does 26B's entry rederivation alone produce the ND-like curve? — On the convention the levels are
actually derived on: yes, essentially, and the marks owe nothing that can be told apart from noise.**

After the entry rederivation, RD reads 1.3798 against the national 1.5547 at year 4 — 11.3 % below,
and 7.9 % below once the 4.4 % timing offset is removed. That is inside the ±15 % band
pre-registered in §4 of the PREREG. The post-entry gap is stable and small across every year
measured: N=3 1.186×, N=4 1.127×, N=5 1.141×, N=6 1.160×, N=7 1.166×. **A level effect of order
10 %, not a 2–3× wedge.**

**The marks do NOT owe a 2× correction. They owe at most ~8 %, and arguably zero.**

**The hazard 26B must be warned about** is the convention switch, not suppression. A live squad
contains no dead players, so the natural thing to do after rederiving entry is to look at survivors
— and on that reading the pool will show **~3.5× entry at year 4 against the national ~1.75×**, and
every living pool player will look like a 2× bargain. He is not. That apparent alpha is the
mortality the all-in calibration already charged for, reappearing because the dead were dropped from
the denominator. **Do not derive a mark uplift from a survivors' reading.**

---

## 6. PREREG BREACHES, OWNED BY NAME

1. **THE PREREG WAS NOT BLIND — and I said so at the time, but it is still a weakness.**
   `PREREG_ORDER26A.md` §0A discloses that before writing it I had read both instruments in full and
   had already seen (a) that `N=4` resolves to `cohort+3`, and (b) that the two denominators are
   different objects and that the ORDER 25 output already printed their 2.574 ratio. H3 and H5 were
   therefore not predictions in any meaningful sense. Disclosing a pre-answer is better than hiding
   one, but it does not convert it into a blind test. **H3's and H5's confirmations should be read
   as verifications, not as successful predictions.** H1, H2 and H4 were genuinely open.

2. **I changed the timing method after seeing a result. Unregistered.** The brief said to measure on
   both the calendar and the career-age axis, and `o26a_wedge.py` §E does exactly that. When I saw
   the axis switch move the residual by −0.5000×, I recognised it as a composition artefact (the
   career-age axis drops every never-played row, and RD loses 45.2 % of its rows that way against
   the national's 13.4 %) and **switched to a reweighting method** — holding the national yardstick
   and reweighting it onto the pool's career-age mix — which was not in the prereg. The reweighted
   timing leg is 1.0440× against the raw axis switch's implied ~1.60×. **I believe the reweighting
   is correct and the raw axis switch is contaminated, and I have published both so the reader can
   disagree.** But the method was chosen after seeing the number, and that is a breach.

3. **I added an unregistered analysis: the mortality identity (§G of `o26a_timing.py`).** It was
   written after the wedge output showed the mark-residual flipping sign between conventions. It is
   the single most load-bearing result in the act — it is what turns "the marks are suppressed" into
   "the pool has higher mortality and higher survivor marks" — and it was **not pre-registered**. It
   is an algebraic identity rather than a fitted quantity, which limits the damage, but it was
   introduced in response to a result and must be read as exploratory.

4. **I applied §4's decision rule against a band the measurement had just falsified.** The rule said
   pool must land "within the ND survivors' band (H4's 2.2–3.1×)". H4's band was falsified — the
   measured national yardstick is 1.75–1.93×. Rather than declare the rule inapplicable, I applied
   it against the **measured** yardstick. That is a defensible repair but it is a deviation from the
   literal rule, and it happens to favour the conclusion I reached.

5. **Declared deviations, registered in advance and therefore not breaches**, listed for
   completeness: the taxonomy split introducing **(c′) THE ENTRY-PRICE OBJECT** as distinct from the
   brief's numerator-side (c) — and the brief's (c) as literally worded scored **zero**; and the
   three-way wedge split keeping **(iii) TIMING** separate from **(ii) MARK-SUPPRESSION** rather than
   the brief's two-way split.

6. **The pre-registered bridge order was followed exactly**, with no reordering and no step added or
   dropped. No breach there.

---

## 7. ANOMALIES

1. **The derivation's published `n` is not the `n` it reads.** §6 of the ORDER 25 packet prints
   RD n=691, ALL POOL n=1200, NATIONAL n=1443 next to the YR4/YR0 column, but `yr4()`'s own
   `Y > W` branch skips rows whose year 4 has not happened. The figures are actually read over
   **667 / 1060 / 1257** rows respectively. The numbers are correct; the labels overstate the
   sample. A reader comparing n against the all-arm instrument's n is comparing two different
   things. **Recommend the packet print the read-n beside the population-n.**

2. **A name collision that will mislead someone.** The matrix record carries a field literally named
   `anchor`, and it is **not** the derivation's `anchor_of()` object — `r['anchor']` equals
   `r['cur']` equals `vpath[0]`, the board's current mark, while `anchor_of(r)` is the signed level
   × `_PL_F`. Two different quantities, one word. `fred-rodriguez`: `r['anchor']` = 212,
   `anchor_of(r)` = 305.2, `r['v0']` = 857.4.

3. **Three pool rows have a first playing season BEFORE their cohort** (SSP, offsets −6, −3, −2) —
   previously-listed players re-entering through the supplementary list. They land at zero or
   negative career ages and are visible in the N=4 age mix as the `-3 / -2 / -1 / 0` buckets. They
   are a small entry-weighted share (about 2.3 % of survivor entry on the national side, 4.9 % on
   RD) and do not change any conclusion, but the career-age axis is not strictly a career axis for
   them.

4. **The two instruments' "ND" are different arms.** The all-arm instrument's ND arm is every
   `type == 'ND'` row in cohorts 2005–2023 (n=1310); the derivation's NATIONAL is `raw_pick` 1–64
   and not pool-flagged (n=1443). The NATIONAL line therefore bridges on population alone
   (1.480344 → 1.554717) with the entry-price step being the identity — which is the cleanest
   available confirmation that the 2.7× is entirely a pool-side denominator effect.

5. **MSD yr1 is `nan`** in the all-arm by-arm table — the instrument's own disclosed MSD
   debut-year gap (the emitter builds `yrs` from draft year + 1, so an MSD entrant's debut season is
   not carried and the row is excluded from that year rather than scored zero). Pre-existing and
   documented in the instrument; noted here because it appears in the copied output.

6. **RUCK is the position where the board and the signed level nearly agree** (v0/anchor = 1.315)
   and **KPF is where they diverge most** (5.114). If 26B wants a sanity check on the entry
   rederivation, the positional spread of `v0/anchor` — 1.3 to 5.1 — is where to look; it is much
   wider than the pooled 2.65 suggests.

---

## 8. FILES

| file | what |
|---|---|
| `PREREG_ORDER26A.md` | pre-registration, committed first |
| `RECONCILIATION.md` | the bridge table and the row-level line-up |
| `WEDGE_DECOMPOSITION.md` | the wedge taken apart, both axes, and the 26B ruling |
| `SUMMARY.md` | this file |
| `o26a_bridge.py` → `BRIDGE.json`, `BRIDGE_out.txt` | the bridge, both instruments re-implemented and controlled |
| `o26a_wedge.py` → `WEDGE.json`, `WEDGE_out.txt` | trajectories on both axes, entry objects, first decomposition |
| `o26a_timing.py` → `TIMING.json`, `TIMING_out.txt` | composition control, true timing leg, mortality identity |
| `o26a_rows.py` → `ROWS.json`, `ROWS_out.txt` | which players each bridge step moves |
| `instruments/noarb_table_allarm.py` | the all-arm instrument, copied so the record is durable |
| `instruments/allarm_O25FINAL.{json,txt}` | its ORDER 25 output, copied for the same reason |
