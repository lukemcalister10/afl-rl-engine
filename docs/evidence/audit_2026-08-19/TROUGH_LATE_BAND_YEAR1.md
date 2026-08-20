# THE LATE-BAND YEAR-1 TROUGH — AN INVESTIGATION

**Seat:** INDEPENDENT AUDIT (read-only). **Date:** 2026-08-19. **Branch:** `land/order-29`.
**No engine edit. No dial. No board built. Nothing adopted. Parked item, blocking nothing.**

**The owner's diagnosis under test:** picks 31-64 dip in year 1 yet reach similar-or-higher peaks
than picks 1-20, so entries and peaks are consistent with each other and the year-1 mark is the
anomaly — *"something unique to that cohort causes them to appreciate the same by peak but display
less signal early for the model to identify the traits that become that peak."*

**Either verdict is a result.** The finding below is: **he is right about the early-signal deficit —
it is real, it is measured, and it is monotone in pick. He is wrong about it being the cause of the
trough.** The trough is a mix effect, and the year-1 mark is not blind to the late-band winners — it
marks them up harder than it marks up the early-band winners.

---

# THE ONE-PAGE ANSWER

**1. Both of his facts reproduce.** On the delivered table, picks 31-40 read −11.0% at year 1 and
41-64 read −7.4%, while 41-64 reach **1.493** at year 6 against picks 1-20's **1.438**. Confirmed.

**2. The early-signal deficit is real and monotone.** How well a year-1 observable separates the rows
that eventually become valuable from those that do not, measured as AUC (0.50 = says nothing):

| year-1 observable | picks 1-20 | picks 21-30 | picks 31-64 |
|---|---:|---:|---:|
| games in year 1 | 0.752 | 0.757 | **0.687** |
| average when played | 0.780 | 0.749 | **0.669** |
| total output (games × average) | 0.774 | 0.770 | **0.699** |

The late bands genuinely give the model less to work with. **That half of his diagnosis is supported.**

**3. But the year-1 mark is NOT missing the winners.** Within each band, comparing the year-1 mark of
the rows that eventually succeed against those that do not:

| band | success rate | yr-1 mark: eventual winners | yr-1 mark: eventual busts | ratio |
|---|---:|---:|---:|---:|
| picks 1-20 | 51% | 1.567 | 0.667 | 2.35 |
| picks 31-40 | 15% | 1.533 | 0.782 | 1.96 |
| picks 41-64 | 7% | **2.007** | 0.865 | **2.32** |

The late-band winners are marked up **harder** than the early-band winners, and the separation is as
wide. The mark finds them.

**4. The trough is a MIX effect, and the counterfactual proves it.** Hold each group's own year-1 mark
exactly where it is and give the late band the early band's success rate:

| band | actual year-1 mark | at the 1-20 success rate |
|---|---:|---:|
| picks 31-40 | 0.892 (**−10.8%**) | 1.169 (**+16.9%**) |
| picks 41-64 | 0.948 (**−5.2%**) | 1.452 (**+45.2%**) |

**The entire trough is the hit rate.** Nothing about the pricing of an individual late-band row is
wrong. There are simply far fewer winners among them, and the many busts are correctly marked down.

**5. "They appreciate the same by peak" is true of the MEAN, not of the typical row.** The late bands
are option-shaped:

| band | mean peak/entry | **median** | p90 | p99 | max |
|---|---:|---:|---:|---:|---:|
| picks 1-20 | 2.31 | **1.89** | 4.35 | 8.93 | 11.27 |
| picks 31-40 | 2.32 | **1.29** | 5.25 | 11.28 | 12.87 |
| picks 41-64 | 2.81 | **1.22** | 7.61 | 24.01 | 28.60 |

A typical late-band row peaks barely above its entry price. The band mean matches picks 1-20 because
a handful of rows multiply their entry twenty-odd times.

**6. Two candidate signals are NULLS and I state them as nulls.** Drafting club carries nothing
(spread inside reshuffling). Entry age carries nothing in any band. And **list retention — the
owner's own "still being listed is information" — turns out to be the termination mechanic, not an
early signal**: condition on surviving a few years and its discriminating power vanishes completely.

**7. Verdict (T4): there is no measured object that would price the trough away, and I would not want
one.** The residual early-signal deficit is a deficit in *discrimination*, not in *level*. Pricing it
would mean marking the whole late band up at year 1 — but the band mean is low because most of that
population really is worth less by year 1, and marking the band up would spoil the very separation
that makes the winners' mark high. **The trough is a property of the population, not a defect in the
price.** The genuine open question it exposes is about the *instrument*, not the engine: the no-arb
test compares band **means** against a compounding carry rail, which implicitly treats a band as one
holdable asset. For an option-shaped population that is the wrong summary.

---

# T1 — WHO CARRIES THE RECOVERY

**Balanced panel:** a row counts only if year 1 and year 6 are both observed, so censoring cannot
manufacture the result. Censored rows are counted and reported in the raw output.

**The recovery is concentrated, and monotonically more concentrated as the pick gets later.**

| band | n | rows that GAIN yr1→yr6 | top 5% share of the band's net gain | top 10% | top 20% |
|---|---:|---:|---:|---:|---:|
| picks 1-10 | 170 | 49% | 57% | 98% | 150% |
| picks 11-20 | 170 | 44% | 68% | 118% | 163% |
| picks 21-30 | 170 | 34% | 69% | 117% | 163% |
| picks 31-40 | 170 | 33% | 84% | 141% | 199% |
| picks 41-64 | 398 | **23%** | **121%** | 170% | 201% |

A share above 100% means the rest of the band is net *negative*, so the top slice has to cover the
losses as well as produce the gain. At picks 41-64 the top 5% of rows carry more than the whole band's
net appreciation.

**Historical exemplars — illustration only, never a gate and never a target.** The ten largest
year-1→year-6 gains in picks 41-64 are all rows whose year-1 mark was modest or low and whose year-6
value is many multiples of entry (e.g. entry 651 → year 1 319 → year 6 7,566; entry 179 → year 1 82 →
year 6 3,958). The pattern is a lottery with a very fat right tail, not a broad cohort recovery.

---

# T2 — THE EARLY-SIGNAL AUDIT

**Estimand.** Within a band group, take every row observed at least 6 years. Call it a SUCCESS if its
realized peak value clears an **absolute, band-independent** bar — the top quartile of realized peaks
across the whole ND teaching population. The bar is absolute on purpose: a within-band bar would
define the answer into existence. Separation is AUC with a 2,000-draw bootstrap; one row is one
player, so the row is the cluster.

| band group | n | successes | thin? |
|---|---:|---:|---|
| picks 1-20 | 340 | 175 (51%) | ok |
| picks 21-30 | 170 | 41 (24%) | ok |
| picks 31-64 | 568 | 54 (10%) | ok |
| — of which 31-40 | 170 | 25 (15%) | **THIN** |
| — of which 41-64 | 398 | 29 (7%) | **THIN** |

| signal | picks 1-20 | picks 31-64 | already read by the engine? |
|---|---|---|---|
| games in year 1 | 0.752 [0.709, 0.796] | 0.687 [0.627, 0.755] | **YES** — `rho31`, `A(g)`, the F1 credit curve, every games bar |
| average when played | 0.780 [0.735, 0.825] | 0.669 [0.576, 0.745] | **YES** — the level, the gate bar, the surplus |
| total output (g × avg) | 0.774 [0.734, 0.817] | 0.699 [0.637, 0.767] | **YES** — both factors |
| entry age | 0.509 [0.479, 0.538] **null** | 0.461 **null** | YES (age-referenced bar, mature-entry discount) — and it separates nothing anyway |
| retained into year 2 | 0.515 | 0.612 — **but see below** | partially; and the increment is a mechanic |
| drafting club | — | **NULL** | **NO** — genuinely unread, and worth nothing |

### The retention result, and why it is a null

Retention looks like the story: its power *rises* as the pick gets later (0.515 → 0.554 → 0.612),
which is exactly where the production signal is weakest, and it matches the owner's own prior ruling
lineage. It also survives stratification by year-1 games. **It is still a null, and here is why.**

Being cut **terminates the value path**, and the standing instrument scores an ended path as zero. So
"retained predicts value" is guaranteed in part by construction. The honest test is whether year-1
retention still separates among rows that all survived further:

| conditioning (picks 31-64) | n | % kept | AUC of retention |
|---|---:|---:|---:|
| no conditioning | 568 | 80% | 0.612 |
| survived to year 3 | 408 | **100%** | **0.500** |
| survived to year 4 | 370 | 100% | 0.500 |
| survived to year 5 | 319 | 100% | 0.500 |

There is no contrast left. **The separation in the headline number is the termination mechanic, not an
independent early signal.** Reported as a null rather than banked.

### Drafting club — a clean null

Club is the one candidate the engine genuinely does not read: a grep for `afl_club` / `_draft_club`
across `_merged_recover.py`, `rl_model.py` and `forward_valuation/*.py` returns **nothing** in
valuation code. Measured on picks 31-64 (n=568, base success rate 10%), **every club cell is THIN**,
and the spread of club success rates (sd 0.0609) sits **inside** what random reassignment produces
(90th percentile 0.0678). **No club signal. Null.**

---

# T3 — IS THE DEFICIT UNIQUE TO THE LATE BANDS?

**Yes for the production signals — the gradient is monotone and it is his hypothesis, confirmed.**

| signal | 1-20 | 21-30 | 31-64 | direction |
|---|---:|---:|---:|---|
| games in year 1 | 0.752 | 0.757 | 0.687 | weaker late |
| average when played | 0.780 | 0.749 | 0.669 | weaker late |
| total output | 0.774 | 0.770 | 0.699 | weaker late |
| entry age | 0.509 | 0.496 | 0.461 | null everywhere |
| retention | 0.515 | 0.554 | 0.612 | *rises* late — but a mechanic (T2) |

The deficit is **not uniform across bands**. A late-pick row's year-1 output tells you materially less
about what he becomes than an early-pick row's does. The owner's framing of *"less signal early"* is
measured and correct.

**What it does not explain is the trough** — see T4.

---

# T4 — THE VERDICT

### Is there a measured, non-invented object that would price the missing early signal?

**No, and the reason matters.**

The deficit T3 measures is a deficit in **discrimination**: at year 1 a future late-band star and a
future late-band bust look more alike than their early-band counterparts do. But the year-1 *mark* is
a price, and the band figure the no-arb test reads is a **mean over the whole band**. Those are
different objects:

- To fix a *discrimination* deficit you would need a signal that separates winners from busts inside
  the late band. **T2 found no unread one.** Production is already fully consumed; age and club are
  nulls; retention is a mechanic.
- To move the *band mean* you would have to mark the whole late band up at year 1 — including the
  ~90% who really are worth less by then. That would not price the missing signal; it would blunt the
  separation the mark already achieves (win/bust ratio 2.32 at picks 41-64, as wide as picks 1-20's
  2.35).

**So the trough is irreducible with what the store holds — stated plainly as a null.** Not because
the data was not looked at, but because the residual is genuine population risk, not unread
information.

### The one thing that IS worth carrying forward — and it is an instrument question

The late bands are option-shaped (median peak/entry 1.22-1.29 against means of 2.32-2.81). The
no-arb test scores a band by comparing its **mean** path against a compounding 14%/yr carry rail —
which implicitly treats a band as one asset a holder could own. For a population where the median row
never appreciates and the top percentile multiplies twenty-fold, the mean is the wrong summary of
what a holder experiences.

**This is already half-acknowledged on the board.** The standing box carries: *"THE DEEP CELL IS
OPTION-SHAPED, AND THE MEAN HIDES THAT — about half deliver almost nothing and a few deliver a lot.
The board prices the average, which is the right thing for a price."* That sentence is about the
charge's deep cell; **the same statement is true of the late pick bands and is not made about them.**
The cheapest honest improvement here is documentary, not mechanical: say on the no-arb page that the
31-64 rows are an option-shaped population whose median row does not appreciate, so the band mean and
the band median tell different stories.

### The reconciliation the brief asked for

The brief asked: *if T2 finds list-retention is the live signal, reconcile with the existing
sitter/selection machinery so any future wiring would collect once.*

**T2 does not find that** — retention is a mechanic (above). But the reconciliation is worth stating
anyway, because the temptation will recur:

The engine **already collects survival-as-evidence, twice over**. The sitter/depth machinery
(`o31_cu`, the `D(c)` fade) prices absence, and the owner's own v750 ruling kept the depth-4 rise on
exactly this reasoning — *clubs cut the sitters who are not up to it, so a player still contracted at
depth 4 has survived a cut, and that survival is itself a signal.* A new year-1 retention term would
read **the same fact** as the depth schedule already reads. Under the owner's R1 combined-take law
that is a second collector on one fact, and it would need to be sized as a residual against the
existing take, not added on top. **My recommendation is that it should not be wired at all**, since
the measurement above says the signal is not there once the termination mechanic is removed.

---

# PROVENANCE — A PROBLEM I HIT, REPORTED RATHER THAN WORKED AROUND

The delivered `BANDS_ASM.json` records that it was built on matrix `per_entrant_ASMCAND.json` with
md5 **`56f2033c`**. **That file no longer exists.** The shared scratch path was overwritten at 11:07
by a newer emit under the same label (md5 `48ffd892`) while the builder works on the next candidate.

Consequences, measured rather than assumed:

- **Year 0 and year 1 reproduce EXACTLY** on the current matrix for every band (1.133 / 1.128 / 1.061
  / 0.890 / 0.926, matching the published table digit for digit). **The trough under investigation is
  unaffected**, which is why this report stands.
- Years 2-7 drift by about 0.5% (e.g. picks 1-10 year 6: 1.396 here vs 1.376 published), because the
  newer board changed some 2026 values.
- **But the delivered no-arb and band tables can no longer be reproduced from the scratch**, because
  the matrix they name is gone. That is a provenance hazard worth a line in the register: emits that
  back a delivered table should be written under a label that a later run cannot overwrite.

**A correction I made to my own work, on the record:** my first pass used the cohort window's upper
bound as the inclusion cutoff. The standing instrument uses the matrix's own observed window end
(2026) and applies the cohort window to the *population* only. My first-pass year-6 figures were
wrong because of it; I found it by refusing to publish before reproducing the delivered table, and
every number above is on the corrected basis.

---

# THIN CELLS, CENSORING AND LIMITS

- **Thin:** the success counts inside picks 31-40 (25) and 41-64 (29) are below the 30-row threshold.
  Every table that splits those bands is marked THIN. The 31-64 group (54 successes) is not thin, and
  the headline conclusions are drawn there.
- **Censoring:** all T1-T4 work uses a balanced panel (year 1 and year 6 both observed). Censored rows
  are counted in the raw outputs, never silently dropped.
- **The MODERN window is heavily censored** (cohorts 2019-2023) and its year-4+ cells rest on very few
  rows. The 41-64 MODERN reading of −27.7% at year 1 is real but its later path should not be read as
  a peak.
- **One artifact I caught and discarded:** entry age read AUC 0.295 (strongly inverse) in picks 31-40
  on the first pass and 0.576 in picks 41-64 — adjacent bands pointing opposite ways on thin cells.
  On the corrected basis both collapse toward 0.50. **Noise, not a signal**, and it is not reported as
  one.
- **Not attempted:** any multivariate model of eventual value. The brief asked which observables carry
  information and whether the engine reads them; a fitted predictor would be a different order and
  would need its own out-of-sample discipline.

---

# FILES

| file | what it is |
|---|---|
| `tr_lib.py` | shared loader; population and `value_at` copied from the standing instrument so the reading cannot drift |
| `tr0_reproduce.py` / `TROUGH_REPRODUCE_out.txt` | step 0 — the trough reproduced before anything is explained |
| `tr1_carriers.py` / `TROUGH_T1_out.txt` | T1 — concentration of the recovery, with exemplars |
| `tr2_signals.py` / `TROUGH_T2T3_out.txt` | T2 + T3 — the signal audit and the across-band comparison |
| `tr2b_incremental.py` / `TROUGH_T2B_out.txt` | T2b — retention base rates, stratified increment, and the club null |
| `tr2c_tautology.py` / `TROUGH_T2C_out.txt` | T2c — the honesty test that turns retention into a null |
| `tr4_verdict.py` / `TROUGH_T4_out.txt` | T4 — the mix decomposition, the counterfactual and the option shape |

**Conventions:** plain speech · no named-player targets (the exemplars illustrate a distribution and
gate nothing) · nulls as nulls · thin cells marked · censoring stated · every figure re-derived from
the walk-forward matrix, none copied from a document under investigation.

**NOTHING WAS EDITED, ADOPTED OR BUILT. READ-ONLY THROUGHOUT.**
