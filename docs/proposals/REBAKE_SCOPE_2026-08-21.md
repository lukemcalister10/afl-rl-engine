# END-OF-SEASON REBAKE — SCOPE FOR YOUR REVIEW

**Draft for Luke. Nothing here has been built or run against the live tree.**
This is a scope paper, not a plan you have approved. Your words on the schedule were:

> *"Yes, bounded fix now, end of season rebake next week once round 24 is done."*

The bounded fix is the one going through pricing tonight. **This paper is the other half — the
rebake — and it is the version that changes the machine underneath the prices rather than
correcting its output.** It needs decisions from you before anyone starts.

A note on vocabulary: everything below is written in plain words first, with the file or
measurement named in brackets so a seat can find it. Where something is genuinely unknown, it says
so rather than guessing.

---

## 1 · WHAT THE REBAKE IS

### The thing being refitted, in plain words

Every production price on the board starts the same way. The engine does not price a player's
scores directly. It looks up a **band of six numbers** — "what could this player's peak realistically
be, at the 10th, 30th, 50th, 70th, 90th and 97th percentile" — and then converts those six numbers
into money and takes a weighted average of them.

Those six numbers come out of six **trained forests**: five of them live in one pinned file
(`cm_400.pkl`, the top five quantiles) and the sixth, the ceiling, lives in another
(`data/q97m.pkl`). They were trained once, frozen, and are loaded — never refitted — by every build.
That freeze was your ruling of 2026-07-14 and it is the right design; it is why the board stopped
moving when it ran on a different computer.

A trained forest of this kind is a **staircase**. It sits flat over a range of inputs, then jumps at
a threshold. That is normal. What is *not* normal, and what the diagnosis found, is that **nothing
ever told these forests that more demonstrated level must mean more value** — so some of the stairs
go *down*.

### What the diagnosis established

Full workings: `docs/evidence/trough_diagnosis_2026-08-20/WORKINGS_TROUGH.md` (read-only; every
swept row restored and re-asserted against the shipped price).

- The forests carry between **253 and 632 distinct thresholds** on the level input alone, and the
  step direction is arbitrary. Kondogiannis's round-23 score of 71 walked his level input from
  47.2 to 49.3 across a run of *descending* steps. His price fell from 386.8 to 324.3. **A score of
  140 would have crossed back up to 428.7.** Nothing evaluated the 71 and decided it was bad. He
  fell off a stair.
- **44 of the 86 thin-evidence players (51.2%) would have been priced HIGHER by some round-23 score
  LOWER than the one they actually made.** 24 by more than 1%, 7 by more than 5%, 4 by more than 10%.
- The step positions were **predicted in advance** from the forest's own thresholds, with no free
  parameters, and then confirmed: 30 of 37 grid steps correct, all three named jumps and all three
  named flat stretches exact to the last digit. The seven misses are all under 0.04%.
- The class it bites is **level between roughly 42 and 70** — where the training data is thinnest.
  Games played is essentially irrelevant (correlation −0.08). Players at level 80+ are immune.

### What the rebake would do

**Refit all six forests with a constraint that says "more demonstrated level is never worth less",
on data current to the end of the 2026 season, and re-freeze them.**

That makes the defect impossible by construction rather than corrected after the fact. It is
also — and this is the whole reason it needs your word — a **change to a frozen artifact that every
price on the board is made of.**

---

## 2 · THE DECISIONS THAT ARE YOURS

Seven. The first is bigger than the others and was not visible until tonight.

### D1 — WHICH MACHINE. *(This one changed since the diagnosis was written.)*

The diagnosis proposed passing a monotonic constraint straight to the existing fit. **Checked
tonight against the pinned library version, and it is not available:** `GradientBoostingRegressor`
— the estimator all six forests use — **does not accept a `monotonic_cst` argument** in the installed
scikit-learn 1.8.0. Verified by inspecting the constructor signature. The diagnosis's "Fix 1, the
clean one" cannot be done as written.

Three real options:

| | what it is | what it costs |
|---|---|---|
| **D1-a** | Switch to the histogram-based estimator (`HistGradientBoostingRegressor`), which *does* support both quantile fitting and monotonic constraints — confirmed present in the same library version. | A **different machine**, not the same machine with a rule added. Every player's band is refitted from scratch on different internals. Rows the current forests price perfectly well will move too. |
| **D1-b** | Keep the current machine, fit exactly as today, then **project the fitted surface onto a monotone shape along the level axis and freeze that**. | Keeps the surface where it is already fine and straightens it only where it descends. Closest to "fix the defect, change nothing else". More custom code in the refit pipeline, which is the thing we are trying to make simple and reproducible. |
| **D1-c** | Don't refit. Keep the read-time bounded fix permanently. | Zero rebake risk. But the defect stays in the artifact, the fix is a permanent patch every future seat must know about, and the retirement accounting in §3 never happens. |

**Honest note:** D1-b is closer to your instinct on scope (one lever per move) and D1-a is closer to
"do it properly once". This is a genuine judgement call, not a technicality. Nobody should pick it
for you.

### D2 — WHICH OTHER INPUTS GET THE CONSTRAINT

The forests read eleven inputs: six position flags, the draft pick, games-exposure, tenure, level,
and age. The diagnosis only ever measured the **level** axis.

| input | case for constraining it | honest state |
|---|---|---|
| **level** | The measured defect. Your own engine already writes the principle down: *"more … at the same rate never worth less"*. | **Recommended. This is the act.** |
| **games / exposure** | The same defect exists here — measured at **+957 in one game** — and there is already a patch for it (§3.2). Constraining it would be what actually retires that patch. | **Plausible, unmeasured on the current forests.** Should be measured before you rule, not after. |
| **age** | Value should probably *fall* with age past a peak, so a constraint would have to be decreasing, and only past the peak. A forest constraint is monotone over the whole range — it cannot say "up then down". | **Recommend NO.** It would be wrong in the young half. |
| **draft pick** | Better pick should never be worth less. Plausible. But the pick axis already has its own isotonic instrument elsewhere in the engine. | **Recommend NO** for this act — two instruments on one axis is the thing that creates confusion. |
| **tenure, position** | No case made either way. | **No.** |

### D3 — THE TRAINING WINDOW *(there is an ambiguity here that needs your word)*

"On the full 2026 season's data" reads clearly but does not have one meaning here, because of how
these forests are trained. They learn from **resolved careers only** — players who debuted on or
before **2021** — one row per player per season, and the thing being predicted is *what that player's
best three seasons actually turned out to be*. **2026 players cannot be training rows: their answer
has not happened yet.**

So there are three different things "refit on the 2026 season" could mean:

- **D3-i — Same rule, current data.** Keep "debut ≤ 2021", but refit at season end so the training
  rows carry every game played through 2026. *Smallest change; the 2026 season enters as extra
  seasons of evidence for already-resolved players.*
- **D3-ii — Move the cutoff forward** (e.g. debut ≤ 2022 or 2023). More training rows, especially in
  the thin band where the stairs are roughest — which is exactly the fix's target. But the newer
  players have had fewer years to resolve, so their answers are noisier.
- **D3-iii — Something else you have in mind.**

**Recommendation: D3-i, and measure what D3-ii would add before deciding to take it.** But it is
your call, and D3-ii is the one that most directly attacks the thin-data root cause rather than just
its symptom.

### D4 — HYPERPARAMETERS: FINER STAIRS

Today: **400 trees, depth 4, learning rate 0.05, minimum 25 rows per leaf**, five quantiles
(10/30/50/70/90); the ceiling model is the same shape at **200 trees**.

More trees and shallower ones give finer stairs — more, smaller steps rather than fewer, larger
ones. With the monotonic constraint in place, finer stairs are strictly better: every step is
upward, so a fine staircase approaches a smooth ramp.

Options to rule on: leave as-is (400/depth 4) · finer (800–1200 trees, depth 2–3) · raise the
minimum-rows-per-leaf in the thin band. **Honest caveat: the current numbers were not chosen by any
recorded measurement I can find — they are what the freeze inherited.** So "leave as-is" is not a
safe default; it is just the status quo.

The fit is cheap enough that all of these can be tried and compared before you rule — see §6.

### D5 — THE FROZEN-MODEL LAW NEEDS YOUR WORD

Your own ruling, written into the boot pins (`data/expected_boot.json`, `_fitted_note`):

> *"It is now fitted ONCE at a bake, pickled to `data/q97m.pkl`, and **LOADED, never fitted**, by
> every consumer. Regenerate ONLY via `refit_q97m.py` at a bake (re-pins here + HALTs downstream)."*

The law already permits a refit "at a bake" through one gated entry point. So the rebake is not
against the law — but the law is a "never" with one exception, and the exception has **never been
exercised**: `data/q97m_refit_log.json` does not exist in the tree. This would be the first use.

**What is needed from you: one sentence in the prereg sanctioning this specific refit** — naming
both artifacts, naming that they move together, and naming that the board moves with them. Not an
amendment to the law; an authorised use of it. If you would rather amend the law's wording (e.g. to
say "at a bake, on a written owner sanction naming the artifacts"), say so and that rides the act.

*Related, and yours to decide:* the same file names three other frozen fitted artifacts
(`peak_model`, `pvc_snapshot`, `bust_prior`). **They are NOT in this scope.** Say if you want them
in — but the one-lever-per-move rule argues hard for keeping them out.

### D6 — ACCEPTANCE: WHAT "IT WORKED" MEANS

Proposed bar, for you to accept, tighten or loosen:

1. **Zero descending steps on the level axis**, checked across all 804 board rows over the model's
   full level range. This is the direct falsifier and it is cheap.
2. **The counterfactual count goes to zero.** Today 44 of 86 thin-evidence players would have been
   priced higher by a lower score. The rebake's bar is 0 of 86. The harness already exists in the
   diagnosis evidence tree.
3. **Every standing gate green** — the 17-check acceptance runner, the boot guard, the release
   contract seal, the year-0 closure standard (pooled gap ≤ 2.0%).
4. **The no-arbitrage pairs still hold** and the class/cohort table stays inside a band you name.
5. **Total pool movement inside a band you name.** See D7 — this is the one that needs a number
   from you, not a pass/fail.

### D7 — CONSERVATION: DOES THE POOL TOTAL MOVE?

The read-time bounded fix has a known property: it only ever raises prices, so it **mints value** —
measured at mean +0.61% across 801 rows. The diagnosis called this *"the single largest open question
on the fix and it is not a small one."*

A refit has the same question in a different shape. A constrained fit is not one-sided the way a
read-time projection is — it can move rows down as well as up — but there is **no guarantee the pool
total is preserved**, and no measurement of it yet.

Three answers are available: renormalise the pool back to its total · rule that the lift *is* the
correction and the old total was wrong · set a tolerance band and halt outside it. **This is a
valuation ruling, not an engineering one.**

---

## 3 · WHAT THE REBAKE RETIRES — THE ACCOUNTING

The plan requires every act to name what it retires, honestly, and to prove the retirement rather
than assert it. Here is that accounting, including the two items where the honest answer is
"unclear".

### 3.1 · The bounded staircase fix — **RETIRED, with a real proof available**

**What is actually shipping** (from the fix's own prereg, committed tonight before its engine edit):
one declared switch, **default off**, with five settings — *ratchet · ratchet+conserve · smooth ·
smooth+conserve · off* — applied at the **read** site where the band is assembled
(`_merged_recover.py:370-372`), over a declared level window of 40 to 120. It does **not** touch the
training code and does **not** refit or re-pin anything: the two frozen forests are read exactly as
they are. *That is what makes it bounded, and it is why it can land tonight without your rebake word.*

If the refit makes the surface monotone at the source, that read-time work — the switch, its five
settings, and the code at the read site — becomes pointless.

**The proof is checkable and should be stated as an acceptance condition:** with the new forests
loaded, **the read-time smoother finds nothing to fix on any of the 804 rows** — it becomes a
measured no-op before it is removed. That is the retirement proof.

Three honesty flags. First, this only holds if the refit constrains **the same axis, in the same
direction, over the same range** — the read-time fix declares a level window of 40 to 120, so the
refit's constraint has to cover at least that. D1 and D2 decide whether this retirement is available
at all. Second, **the retirement cannot hide behind a byte-identity check**: the refit itself moves
the board, so the removal happens inside a move. It has to be stated as a move and measured as one,
not slipped in under "nothing changed". Third, the fix has a **conservation** setting among its five
— if you adopt one of the conserving variants tonight, then whatever that setting does about pool
totals has to be re-decided for the refit (D7), because the refit will not inherit it.

### 3.2 · The games-axis patch — **PROBABLY NOT. Stated honestly as unresolved.**

`engine/rl_after/_merged_recover.py:2944-2962` — a three-point moving average on the games axis,
applied only to players in their first season of evidence. Its own docstring:

> *"the band prior is a stepwise (GBR) surface whose exposure-axis steps (measured +957 in one game
> on the B6 synth) **and the designed M3 pin-fade** otherwise leave the evidence ramp non-monotone
> (B6 law: more games at the same rate never worth less)"*

Read carefully, it names **two** causes, and a level-axis constraint addresses **neither**:

- The exposure-axis steps are the *same* defect one input over. A constraint on the games/exposure
  input (D2) would address them — but only if you rule that constraint in, and it has not been
  measured on the current forests.
- **The "designed M3 pin-fade" is not a forest artifact at all.** It is a deliberate fade elsewhere
  in the engine, and no refit of any kind removes it. If it alone can make the ramp non-monotone,
  the patch is still needed after a fully constrained refit.

**Honest verdict: a level-only refit does not retire this patch. A refit that also constrains the
games axis *might*, and the only way to know is to measure whether the pin-fade component alone
breaks monotonicity once the forest is constrained.** That measurement is small and should be
scoped into the rebake as a named question with a written answer either way — not left to be
discovered.

### 3.3 · The ceiling guard `max(ceiling, 90th percentile)` — **NO. It fixes a different problem.**

`_merged_recover.py:372` forces the ceiling estimate to be at least the 90th-percentile estimate.
This exists because **two independently trained models can disagree about ordering at the same
player** — the 0.97 model can come out below the 0.90 model. Monotonicity in level says nothing
about that; it constrains how each model behaves *as level changes*, not how two models rank against
each other *at one point*.

Worth knowing: **there is already a second guard of exactly the same kind and it is easy to miss.**
`engine/forward_valuation/conditional_prior.py:167` ends with `np.sort(...)` — the five quantiles are
sorted after prediction, which silently repairs any crossing among them. So the engine carries two
crossing repairs, and this act would retire neither.

Retiring them needs quantile **non-crossing enforced at the fit** (a joint or composed fit), which is
a materially bigger design change than adding a constraint. **Recommend explicitly out of scope, and
recommend the two guards be instrumented instead** — count how often each actually fires, so a future
act can retire them on evidence.

One more thing you should know before ruling on the ceiling: the earlier ceiling investigation
(register v723) found the ceiling model is **approximately calibrated** — 3.63% against a 3% target —
and that its real defect is **the age taper**, measured at +30,223 points across 566 rows with the
taper off. **That is a separate lever, and it is already queued for "next bake".** See §5.7.

### 3.4 · A retirement you may not have on your list — the pool contamination

Register v678 records, measured:

> *"cm_400 trained ~45.36% on pool careers, that shape baked inside every ND price today, **fixable
> only by a bake-time retrain**"*

and records your same-hour ruling: **keep the deferral, give it its own later exercise, its own bake,
its own attribution ledger.** *This is that exercise.* A refit is the only mechanism that closes it,
and the rebake is the only bake scheduled. **Flagging it so you can decide deliberately whether it
rides — not so it rides by accident.** If it does ride, the training pool composition becomes part of
D3 and the attribution ledger has to separate "the constraint moved this row" from "the pool split
moved this row", which is more work but is your own stated requirement.

### 3.5 · Missing provenance stamps — closed by construction

Register: *"cm_400/q97m pickles carry NO training-store stamp — stamps become mandatory."* Any refit
writes new pickles, so the stamp goes in then. Free, if it is written into the pipeline.

---

## 4 · THE SHAPE OF THE CAMPAIGN UNDER THE NEW MACHINERY

This is where the new tooling pays. The last campaign of this size was a checklist ordeal. This one
should be a pipeline.

**1 · Prereg.** Predictions and falsifiers committed **before** any file is touched — that is now a
standing law (P9), and this act touches engine files. The prereg carries: your rulings on D1–D7
verbatim, the predicted direction and rough size of the board move, and the falsifiers. **Your
sanction for the frozen-artifact refit (D5) lives here.**

**2 · Refit — as committed code, versioned, reproducible.** The current state is honestly poor and
this is the act that fixes it:
- The five-quantile file lives at **`/home/claude/cm_400.pkl` — outside the repository**, seeded by
  `bootstrap.sh`, and its builder says plainly it is *"not byte-reproducible by a fresh fit"*.
- The ceiling model has a proper in-repo refit entry point (`refit_q97m.py`) that has **never been
  run** — there is no refit log in the tree.

**The rebake delivers one committed, versioned refit script that produces both artifacts, in-repo,
writing a provenance record (training store md5, row count, hyperparameters, old → new hashes) and
re-pinning the boot identity.** No more archaeology pickles. Reproducibility is then **measured**,
not claimed: fit twice on the same box, compare bytes, and record the answer honestly whichever way
it goes.

**3 · Candidate board.** Build the board on the new forests. It does not become the live board.

**4 · The full measurement battery**, all of it, against the current live board:
- **movers** — every row that moved, by size, with the biggest named individually;
- **no-arbitrage** — the paired-value checks still hold;
- **class/cohort** — the year-1 class mark and the cohort table stay inside band;
- **day-0** — explicitly off unless deliberately activated, with the row diff printed (automation
  never re-bases itself green);
- **book** — the matrix rebuilt and diffed, re-sealed if its size changed.
Plus the two acceptance conditions specific to this act: **zero descending steps** and
**zero counterfactual inversions among the 86**.

**5 · Probation.** The candidate sits, measured, before anything is asked of you.

**6 · Your word.** The packet arrives in the fixed template — what changes; **who moves and who
doesn't, by name**; cost; standing-table impacts; what would make this silly; recommendation;
falsifiers. Nothing lands without your word.

**7 · Land, in one command.** `tools/land lever` runs the whole transaction: takes the build lock,
builds and proves, moves the pins, appends the lineage, restamps and re-pins the release contract,
reconciles the sibling, writes both interface bundles, runs the manifest check and the 17-check
acceptance runner, times every step, and commits by explicit path. If any step fails it **aborts and
restores every carrier byte-exact** — proven 10 out of 10 in its self-test.

**8 · Re-pin and re-certify.** Both fitted-artifact pins move (`band`, `q97m`), the board pin moves,
the balanced-board pin moves, the release contract restamps. Until all of them are consistent the
boot guard stays red **by construction** — that red is the feature.

**9 · Book re-seal**, and the single lineage column that a landed change earns.

---

## 5 · WHAT COULD GO WRONG — HONESTLY

**5.1 · The blast radius is unbounded, by design, and that is the biggest difference from the bounded fix.**
Every production price starts at this band. Even the pedigree pole is priced through it. The bounded
fix left **466 of 801 rows completely unmoved**; a refit will move essentially **every row with any
production weight** — thin and mid rows hardest, but not only them. There is no version of this act
with a small blast radius. **The mitigation is measurement and your review, not containment.**

**5.2 · The level input is not the plain level, and it tangles with games.**
At build time the level input is rebound to a **par-centred** version
(`par_redesign.lvl_par`), which is `par + (weighted level − par) × min(1, exposure/ramp)`. So the
constraint "more level is never worth less" is being asserted in par-centred space, and the par-centred
level **contains the games-exposure term**. Two consequences: the constraint may behave differently
than the plain reading suggests, and constraining level and games together (D2) needs **one** reading
of the interaction, not two independent ones. *This is a real subtlety and it should be measured on a
mock fit before the real one.*

**5.3 · A constrained fit is a worse fit, by construction. How much worse is a measurement.**
Adding a constraint removes freedom, so the constrained forests will fit their training data less
well than the current ones. Whether that shows up anywhere that matters — whether the top quantiles
still sit where the earlier ceiling work measured them (3.63% against a 3% target), whether the
crossing repairs fire more often — **is unknown and must be measured, not assumed.**

**5.4 · Circularity — and it is narrower than it first looks, but not zero.**
The season's data does include scores that were themselves priced through the staircase. Read
carefully:
- **The training targets are safe.** What the forests learn to predict is *what a player's best three
  seasons actually turned out to be* — real football outcomes from the store, not engine prices.
  The staircase does not contaminate them.
- **What is contaminated is the comparison.** The live board is itself a staircase board. It is the
  "before" in every movers table, every class mark, every no-arbitrage check. So the whole battery is
  measuring against a known-defective reference.
- **Handling, proposed:** (i) state plainly, in the packet, that the reference board carries the
  defect — a big move against it is not automatically a red flag; (ii) lean on the acceptance tests
  that **do not** reference the shipped board — the descending-step count and the counterfactual
  sweep are both absolute; (iii) **name and check** any place where an engine-produced price feeds
  back into a model input. My reading is that none does, but that is a reading, not a proof, and it
  should be a written check in the prereg rather than an assumption.

**5.5 · Two frozen artifacts moving in one act doubles the certification surface.**
The ceiling model's own refit script halts everything downstream until the board, the book and the
gates are re-pinned in the same commit. Doing both artifacts together means both halts are live at
once. **If either fit turns out not to reproduce on a second box, the entire certification is soft** —
and non-reproducibility is the *expected* state today, not a surprise: the library's numerical
kernels are CPU-selected, which is the whole reason these things are frozen. **The freeze buys
travel, not reproducibility.** So the rebake must state, measured, what its artifacts are and are not
reproducible against.

**5.6 · The season boundary.** The board is at round 23; round 24 lands first. If the refit is done
while the store and the training pool are in different states, the whole thing is void. **Sequencing
is: R24 lands and settles → the store is final for 2026 → then refit.** Your schedule already says
this; it is written here so a seat cannot get it wrong.

**5.7 · Scope creep, and there is a queue waiting.** Already sitting on the "next bake" list:
the ceiling model's age taper (+30,223 points over 566 rows measured with it off), the pool/national
training contamination (§3.4), a ~9% head-smoothing on one of the frozen surfaces, and an era
steepening. **Each is a separate lever.** Your own attribution rule is one lever per move. A rebake is
a rare, expensive opening and everything queued will try to ride it. **Recommendation: the constraint
rides alone, the pool contamination rides only if you say so, and everything else waits — with the
queue written into the packet so nothing gets lost.**

**5.8 · The one that is not on this list is the one that will happen.** The lander's own build found
four defects the moment it was actually run, including one where the first fix was wrong and its own
gate caught it. **Assume this act finds something too, and leave room in the schedule for it.**

---

## 6 · WHAT IT WILL COST — MEASURED, NOT GUESSED

### The numbers we actually have, from today

| what | measured | source |
|---|---|---|
| Full landing transaction, no-op rehearsal | **563.5 s = 9.4 min**, machine-timed per step | `docs/evidence/p2a_lander_2026-08-20/06_noop_CLAIMS.json` |
| — of which: build + proofs | 109.3 s | same |
| — of which: gates | 226.0 s | same |
| — of which: claims (re-runs every gate) | ~228 s | same |
| — of which: everything the landing *writes* | **under 1 second** | same |
| A board-*moving* act adds build legs + sibling reconcile | **≈ +2 min** | same, §5 |
| Board build | ~80 s | the standing cost measurement |
| Interface emit | ~3.5 min | same |
| Total builds before any acceptance stage | **~13 min** | same |
| Four passes, strictly serial | ≈ 51 min engine compute | register |

### The fits themselves — measured tonight

Benchmarked on this box against a synthetic dataset of the same shape as the real one
(13,221 rows × 11 inputs — the real row count is in the same range):

```
five quantile forests, 400 trees, depth 4 (as shipped)          65.3 s
the ceiling model,     200 trees, depth 4 (as shipped)           6.3 s
five constrained histogram forests (option D1-a)                 0.3 s
```

**The fit is not the cost.** Refitting everything takes about a minute. That is a genuinely useful
finding: it means **D4 can be settled by trying several hyperparameter settings and comparing them**,
rather than by argument.

### The estimate

| stage | estimate (machine time) |
|---|---|
| Refit both artifacts + provenance + reproducibility check | 3–8 min |
| Candidate board + book + interface emit | ~15 min |
| Full measurement battery (movers, no-arb, class, day-0, book, + the two act-specific tests) | 30–60 min |
| The landing itself, board-moving | ~11.5 min |
| One clean re-certification pass | ~10 min |
| **Total machine time** | **roughly 1.0–1.5 hours** |

**Honest range: 0.5 to 3 hours.** That is the ±2× the schedule should carry, and here is exactly why
it is that wide:

1. **No board-moving landing has been run through the new command yet.** The 563.5 s is a no-op
   rehearsal that reproduced the live board and moved nothing. The first real one will find things —
   the rehearsal itself found four.
2. **The measurement battery has never been run end-to-end as one battery.** Its parts exist as
   separate scripts from previous campaigns. Assembling them is work that is not in the machine-time
   column.
3. **The gates are paid for twice** — the claims step re-runs every gate and never reads a verdict
   back, about 3.8 of the 9.4 minutes. That is referred to you as a ruling in its own right; if you
   rule it out, every number above drops.

### Against the last campaign — the honest comparison

The last board-moving campaign ran across many seats over several days, and the record puts the
order-A era at roughly **1.9 million tokens across 13 seats**. Machine time was a small fraction of
that. The cost was people-time: prereg, reading measurements, adjudicating, and the landing tail.

**What the new machinery actually changed:** the landing tail. It was a hand checklist with a
history of ordeals; it is now one command with machine-recorded timings and a byte-exact abort path
proven ten times out of ten.

**What it did not change:** the prereg, the measurement battery, and your review. Those are the bulk
of the cost and they stay. **So the honest claim is not "the rebake is cheap" — it is "the rebake's
riskiest and most error-prone hour is now a command instead of a checklist."**

---

## 7 · WHAT IS BEING ASKED OF YOU

1. **D1** — which machine: switch estimator (a), straighten the current one (b), or don't refit (c).
2. **D2** — level only, or level + games.
3. **D3** — the training window: same rule with current data, or move the cutoff forward.
4. **D4** — hyperparameters, or a word to go and measure the options first.
5. **D5** — the sentence in the prereg sanctioning this refit of the frozen artifacts.
6. **D6** — accept, tighten or loosen the acceptance bar.
7. **D7** — conservation: renormalise, rule the lift is the correction, or set a tolerance band.

Plus two scope calls: **does the pool-contamination retrain ride** (§3.4), and **does anything else
from the bake queue ride** (§5.7). The recommendation on both is no, and the reason is your own rule
about one lever per move.

**Nothing in this paper has been started. It waits for your word.**

---

## 8 · PROVENANCE OF THIS PAPER

Read-only throughout. Nothing was written to the repository, no build was run, and the build lock
was never taken — the pricing seat held it.

Base at the start: `main` @ `efbe1b6`. **The base moved while this was being written**: the pricing
seat committed its prereg (`5f94a44`) and has an in-flight edit to `engine/rl_after/_merged_recover.py`
in the working tree. Recorded rather than smoothed over. Nothing this paper measures changed across
it — `docs/OPEN_ITEMS_REGISTER.md` is byte-identical between the two commits, and §3.1 was rewritten
against the prereg's actual text rather than a guess at it.

Sources read: `docs/evidence/trough_diagnosis_2026-08-20/WORKINGS_TROUGH.md` and `PREDICTION.md` ·
`engine/forward_valuation/conditional_prior.py` · `engine/forward_valuation/par_redesign.py` ·
`engine/rl_after/wire_redesign.py` · `engine/rl_after/_merged_recover.py` (the band read site and the
games-axis patch) · `refit_q97m.py` · `data/expected_boot.json` · the round-24 lander evidence at
`docs/evidence/p2a_lander_2026-08-20/` · the ceiling and pool-contamination entries in the register
(v678, v723) · `git show 5f94a44`.

Measurements taken tonight, on this box, in memory only: the library check that the current estimator
does not accept a monotonic constraint (§2 D1), and the fit-cost benchmark on a synthetic dataset of
the same shape (§6). Both are reproducible in a few seconds and neither touches the engine.

