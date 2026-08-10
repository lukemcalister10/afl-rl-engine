# THE COMPOSITION ACT — BUILD SEAT RECORD · 2026-08-10 · **HALTED AT THE ORDERED FIRST GATE**

Branch `landing/334-composition` from `origin/main` **`110afb3`**. Authority: the build brief
(#334 comment 5238883444) · `docs/directives/COMPOSITION_DIRECTIVE_2026-08-10.md` · the ruled
package (5238860310) · the D constraints (5238688172). **BRANCH-HELD: nothing merges, no
attribution column registers, before the owner's side-by-side adoption word.**

Plain English throughout, by the owner's standing rule.

---

## 0. THE HEADLINE, STATED FIRST

**The build did not reach the writes. It halted at ITEM I — the restatement — which the sitting
made the precondition for everything else, and it halted for a reason that is about the repo, not
about the seat's patience: the corrected ruler's probe scripts are not in the tree.**

The directive said this would happen. §6 discrepancy 10 lists what is "not re-runnable from the
repo … CF-B, the pool factors, the 1.378 contrast, the ruck measurements, F1/F2 figures, the H cut
sizes, the tilt ledger. The underlying probe scripts live in the act evidence records, not the
tree." ITEM I is the instruction to restate **every** F-based verdict on that ruler. A ruler that
cannot be loaded cannot be restated on; it has to be rebuilt first, and a rebuilt ruler that does
not reproduce the filed one is a **different** ruler wearing its name.

So the seat did the honest thing in the order the charter sets: state the expectation, run the
measurement, compare, and stop the step on a mismatch instead of improvising past it.

**What that halt did NOT stop.** Two of the sitting's own open questions were settled on the way,
both by exact reproduction of the directive's own figures, and both are reported below as findings
the owner can act on:

| result | status |
|---|---|
| **ITEM C's weight machinery** — `w = G·Q·gate` | **REPRODUCED EXACTLY** on all six worked rows, and on the cohort statistics and both landings |
| **C-Q3, the faller demonstration** | **SUCCEEDS** — the drafted z gate ships; the `sa` fallback does **not** install |
| **ITEM I, the restatement** | **HALTED** — ruler not reproducible from the tree (§3) |
| **ITEM B, the re-derived age gradient** | **HALTED** — conservation exact, but the 21+ factor moves −53% against the filed prior (§4) |
| ITEMS A · D · E1 · E2 · H, the side-by-side, the publication layer | **NOT STARTED** — they sit behind ITEM I and ITEM B by the ruled sequencing |

Nothing in this branch changes the engine. **No file under `engine/` is touched; the board, the
store and the surface pin are byte-identical to `110afb3`.** Everything here is read-only
measurement plus this record.

---

## 1. BASE IDENTITIES — VERIFIED BEFORE ANY WORK

| artifact | required | measured on disk |
|---|---|---|
| store `engine/rl_after/rl_model_data.json` | `d9a24282…` | `d9a24282357cf3083b1640466e3ecd83` ✓ |
| board `data/rl_build/rl_app_data.json` | `4b448a82…` | `4b448a821f54180182637983f7a26a9d` ✓ |
| engine mode | gate only, `RL_GAMMA=1.0` | `config_manifest.enforce('gate')`, manifest hash `cef06fd6250b` ✓ |
| year-1 cohort (ND in-curve, class 2025) | n = 58 | **58** ✓ (played 34 / sitters 24 — filed 34/24 ✓) |

The loader is `engine_load.py` (copied here from the session scratchpad): one exec-load per
process, gate mode, `RL_GAMMA=1.0` — the one configuration that reproduces the shipped board.

---

## 2. ITEM C — REPRODUCED EXACTLY, AND C-Q3 SETTLED

This is the part of the act that is now on solid ground, and it is worth stating precisely
**why** it counts: the directive published seven worked rows with every intermediate quantity, so
an independent re-derivation either lands on them or it does not. It landed on them.

### 2.1 The two reading conventions the directive left implicit

Reproducing the rows required pinning down two things the directive's prose did not spell out, and
both were recovered **from the rows themselves** (they are over-determined — six rows, two
unknowns):

1. **`par`'s tenure argument is the DRAFT-AGE bridge, not the live tenure clock.**
   `par = par_at(pos, min(effpk, KMAX), T)` with **`T = clip(draft_age − 18, 1, 6)`**. This is
   `eff_ten`'s own thin-career branch (`max(base, age−18)`) read at draft age, and it is what §2C
   means by "Q = clip(sa / par(pos, **draft-age**), 0, Q_max)" — quality judged against *who he
   is*. It resolves §6 discrepancy 2 (the engine's par object is pick-keyed) exactly as the
   directive said it had been resolved. Reading `T` off the live tenure clock instead moves Mraz
   from 57.55 to 60.35 and his **w** from 0.488 to 0.465 — so this choice is load-bearing and is
   now pinned by evidence rather than by taste.
2. **`g` and `sa` are CAREER quantities**: `g` = career games total, `sa` = career
   games-weighted average. Toby Conway settles it beyond argument — the directive's row says
   6 games at 74.00, and his store record is 2023 · 1 game @ 46.0 plus 2024 · 5 games @ 79.6:
   `(1×46 + 5×79.6) / 6 = 74.00` **exactly**, on 6 career games. This also explains the
   directive's own robustness note that career-average vs latest-season "moves only Conway".

### 2.2 The worked rows, reproduced

Transcript: `item_c_probe_out.txt`. Target = the directive's §2C table.

| row | player | g | sa | par | G | Q | gate | **w** (mine / filed) |
|---|---|---|---|---|---|---|---|---|
| 1 | Noah Mraz — KPD, pick 35 | 4 | 84.25 | 57.55 | 0.333 | 1.464 | 1.000 | **0.4880 / 0.488** ✓ |
| 2 | Archie Ludowyke — KPF, pick 50 | 2 | 40.00 | 49.03 | 0.200 | 0.816 | 1.000 | **0.1632 / 0.163** ✓ |
| 3a | Luke Beecken — MSD pool | 1 | 7.00 | 74.27¹ | 0.111 | 0.094 | 0.349 | **0.0037 / 0.0035** ≈ |
| 3b | Gerrick Weedon — ND SF pick 22 | 1 | 5.00 | 55.71 | 0.111 | 0.090 | 0.020 | **0.0002 / 0.0002** ✓ |
| 4 | Zeke Uwland — SD, pick 2 | 17 | 53.58 | 69.04 | 0.680 | 0.776 | 1.000 | **0.5277 / 0.528** ✓ |
| 5 | Toby Conway — ND RUCK pick 24 | 6 | 74.00 | 53.80 | 0.429 | 1.375 | 0.533 | **0.3144 / 0.314** ✓ |

¹ the single non-match: Beecken's draft-age bridge reads T=5 here against the directive's T=6, a
one-year draft-age difference on a mid-season-draft row. It moves his **w** from 0.0035 to 0.0037
— on the row the directive itself calls "w ≈ 0 … at most +0.14 points on 301". Immaterial, and
flagged rather than smoothed.

**Every anchor and every gate matches to the decimal published.** Both sanity anchors hold on the
live objects: the 1-game-at-7 row comes out w ≈ 0, and the spirit test still passes — 6 games at 70
beats 1 game at 120 by 2.65×.

### 2.3 C-Q2 — the H ladder (the ONE new dial)

Transcript: `item_c_q3_out.txt`. Landing = mean over the cohort of `ceiling/anchor`, i.e.
`mean(1 + w(H−1))`, on the taught year-1 level (C-Q1).

| H | played-only landing | all-rows landing |
|---|---|---|
| 1.0400 | 1.0155 | 1.0091 |
| 1.0945 | 1.0367 | 1.0215 |
| 1.1000 | 1.0388 | 1.0228 |
| **1.1300** | **1.0505** | **1.0296** |
| 1.1600 | 1.0621 | 1.0364 |
| 1.2000 | 1.0777 | 1.0455 |
| 1.2500 | 1.0971 | 1.0569 |
| 1.3000 | 1.1165 | 1.0683 |
| 1.3350 | ~1.1300 (band top) | ~1.0765 |

**Cross-check against the directive, which published two points of this ladder:**

| quantity | filed | measured here |
|---|---|---|
| cohort n / played / sitters | 58 / 34 / 24 | **58 / 34 / 24** ✓ |
| mean w, played-only | 0.3873 | **0.3884** |
| mean w, all rows | 0.2271 | **0.2277** |
| played-only landing at H=1.13 | 1.0504 | **1.0505** ✓ |
| all-rows landing at H=1.13 | 1.0295 | **1.0296** ✓ |

**The admissible H window** on the ruled played-only basis is **H ∈ [1.103, 1.335]** — below 1.103
the played-only landing does not reach the 1.04 floor; above ~1.335 it leaves the 1.13 ceiling.
**H = 1.13 is the recommendation** (played-only 1.0505, all-rows 1.0296): it is the value the
directive costed, it sits low-mid band with room for the ITEM H cuts underneath it (−0.002…−0.012),
and it is the only value on the ladder with a published figure to check it against.

*This is a recommendation, not a landing — H is only final once ITEMS I/B/A have moved the taught
year-1 level it multiplies.*

### 2.4 C-Q3 — THE FALLER DEMONSTRATION **SUCCEEDS**

The directive flagged this as unreproduced (§2C flag 3, §6 discrepancy 5): the z gate
`min(e/anchor, 1)` "does not fire on the named faller", because Zeke Uwland sits **above** entry.
That is confirmed here — and it is confirmed to be **the wrong test**, not a failed gate.

**Uwland is not a faller.** Measured: `ev/anchor = 1.178` → gate `1.000`. A player above his entry
expectation is by definition not a top-pick faller, so a gate that protects fallers is not supposed
to fire on him. The assembly tested the claim on the one named row that could not possibly satisfy
it.

**Run on the population the claim is about** — top-10 picks in the cohort book (ND in-curve,
classes 2019-26, live rows only, n = 67) — the gate fires hard and on exactly the right people:

| player | pick | pos | anchor | ev | **ev/anchor** | **gate** | w after gate |
|---|---|---|---|---|---|---|---|
| Liam Henry | 9 | SF | 1320.1 | 66 | **0.050** | 0.050 | 0.0379 |
| Josh Gibcus | 9 | KPD | 1103.1 | 143 | **0.130** | 0.130 | 0.0872 |
| Nikolas Cox | 8 | KPF | 1089.7 | 142 | **0.130** | 0.130 | 0.1145 |
| Jamarra Ugle-Hagan | 1 | KPF | 2225.0 | 291 | **0.131** | 0.131 | 0.1263 |
| Archie Perkins | 9 | SF | 1320.1 | 247 | **0.187** | 0.187 | 0.1679 |
| Dylan Stephens | 5 | MID | 2330.5 | 661 | **0.284** | 0.284 | 0.2495 |
| Braeden Campbell | 5 | SD | 1198.1 | 429 | **0.358** | 0.358 | 0.2685 |
| Sid Draper | 4 | MID | 2866.5 | 1220 | **0.426** | 0.426 | 0.0856 |
| Zane Duursma | 4 | SF | 1860.5 | 817 | **0.439** | 0.439 | 0.2022 |
| Logan McDonald | 4 | KPF | 1574.0 | 740 | **0.470** | 0.470 | 0.5032 |

**23 of the 67 top-10-pick rows carry gate < 1.0 and are protected.** The protection is material,
not cosmetic: Ugle-Hagan's weight is cut from 0.96 to 0.126 — the release reaches him at about an
eighth of the strength it reaches a player who is meeting his entry expectation.

**VERDICT: the demonstration succeeds. The drafted z gate `min(e/anchor, 1)` SHIPS. The designated
fallback (the scoring-average check as C's gate) does NOT install.**

And it should not, on the evidence. The fallback was measured beside it (same transcript). A
`sa`-based gate `clip(sa/par, 0, 1)` protects a similar *count* (25 of 67) but **protects the wrong
rows**: it lets Jamarra Ugle-Hagan (sa/par 1.076) and Logan McDonald (1.167) through at gate = 1.0
— two of the clearest fallers on the board, each priced at ~13% and ~47% of entry — while the z
gate cuts both hard. A player can hold a respectable per-game average and still have fallen a long
way, because falling is mostly *not playing*. The `sa` gate cannot see that; the z gate can.

**The double-counting assertion holds by construction on the shipped gate**: `w` reads `sa` exactly
once, through `Q = clip(sa/par, 0, 2)`. The z gate reads `ev` and `entry_anchor`, never `sa`. Had
the fallback installed, it would have been a second `sa` reader on the same leg and would have
needed the explicit assert; it does not install, so there is one reader.

---

## 3. ITEM I — THE HALT, AND WHY

### 3.1 What was expected, written before the run

The expectation was filed in the progress record before the measurement, per HALT-NO-SURPRISE:
reproduce the directive's four-instrument ledger — **A 1.6621 · B 1.5883 · C 1.6028 · D 1.5468**
(availability-in / rate-based × full-horizon / year-11-capped) — and audit 1's ND year-0
overall ≈ 0.99. **Stated halt condition: if the reconstruction does not land near those four
levels, the ruler is not reproduced and the step stops.**

### 3.2 What the reconstruction gives

Built from the engine's own integrand — `posval(level + capt_prem(level) − REPL[pos]) × G`
discounted at `LENS['bal'] = 0.14`/yr, which is `proj_from_peak`'s own summand (rl_model.py
581-598); availability-in uses games played, rate-based uses 21 regardless; the cap keeps career
years ≤ 11. Transcripts `ruler_probe_out.txt`, `ruler_probe2_out.txt`.

| instrument | filed | reconstructed (all rows) | reconstructed (ND only) |
|---|---|---|---|
| A — avail-in × full | 1.6621 | 1.5929 | 1.7029 |
| B — avail-in × yr-11 | 1.5883 | **1.7048** | **1.8289** |
| C — rate × full | 1.6028 | 1.5056 | 1.6152 |
| D — rate × yr-11 | 1.5468 | **1.6137** | **1.7370** |

The availability axis reproduces in **direction and roughly in size** (rate-based sits below
availability-in, by 5.5% here against the filed 4.4%). **The horizon axis comes out with the wrong
sign**, and the reason is diagnosable rather than mysterious: capping delivery at year 11 can only
*remove* delivered value, so price/realized must *rise* — yet the filed ledger has B below A. That
only works if the filed instrument **truncates the price as well as the delivery**. The ruler
report says exactly this in words: the engine carries 15.1% of the year-4 price beyond year 11
against 9.9% delivered. Applying that 15.1% haircut to the price side by hand brings the ND
readings to 1.553 (vs filed 1.588) and 1.475 (vs 1.547) — the right side of the line, still 2-5%
out, and now depending on a hand-applied constant rather than a re-derivation.

### 3.3 The structural finding — reported because it outlives this build

**The engine cannot price a historical player in his historical context.** `ev(p, Y)` takes an
evidence year, but the valuation is anchored on `BASE_REF`/`AGE_REF` = 2026 and reads the player's
**current** `_retired` / `delisted` flags. So "his year-4 price" for a player drafted in 2014 is a
2026-lens reading of a 2026-state player, not the price the board carried in his year 4. The
measurement shows how badly this bites: restricted to completed careers, the reconstructed level
collapses from ~1.6 to **0.04**, because `ev()` returns `0.02 × v0_start` for every delisted row —
the price the ratio needs is simply not recoverable from the live engine.

Any four-instrument ruler built on year-4 prices therefore rests on a same-kind approximation. That
is not a criticism of the filed ledger — it is a statement that **the ledger cannot be
re-derived from this tree, and the tree cannot currently be made to re-derive it.** Which is the
halt.

### 3.4 What this halt does and does not block

It blocks: the ITEM I restatement table (year-0 and year-1 verdicts per position/route on the
corrected basis); therefore the "clean restated v0" precondition; therefore **ITEM A**, which the
sitting ruled ships only on clean restated v0 verdicts; therefore the F8 player-unit re-measure of
every named cell of the act, which is a side-by-side deliverable.

It does not block: ITEM C (settled above, on the engine's own live objects, no ruler involved).

**OWNER DECISION REQUIRED.** One of:
1. **Supply the probe scripts** from the act evidence records (the directive says they exist
   there), so the ruler loads instead of being rebuilt — cleanest, and it makes ITEM I a re-run;
2. **Rule the reconstruction adequate** as the corrected ruler, with the level 2-5% off the filed
   figures and the horizon axis re-derived rather than reproduced, and let ITEM I restate on it;
3. **Re-scope ITEM I** to the verdicts the live engine *can* carry honestly — the year-0 verdicts,
   where the price is `entry_anchor(p)`, a draft-time function with no historical-context problem —
   and park the year-1 restatement with the ruler question.

The seat's recommendation is **(1) if the scripts can be found, otherwise (3)**. Option 2 renames a
rebuilt ruler as the corrected one, and the whole reason ITEM I exists is the owner's
no-cherry-picking word — restating verdicts on a ruler that is itself unverified would defeat it.

---

## 4. ITEM B — MEASURED, CONSERVATION EXACT, GRADIENT MISMATCHED (SECOND HALT)

ITEM B does **not** depend on the ruler's absolute level: the C5 reshape is level-preserving, so the
factors are a *relative* gradient inside the pool and the instrument's unknown global scale cancels.
It was therefore measured despite §3. Transcript: `item_b_probe_out.txt`.

**Method** — band factor = mean over the band of `delivered / entry_anchor`, normalised so the
anchor-weighted mean factor over the whole pool is exactly 1.0.

| band | players | Σ anchor | raw ratio | **re-derived factor** | filed prior | shift |
|---|---|---|---|---|---|---|
| ≤18 | 649 | 157,579.0 | 0.2182 | **0.7216** | 0.666 | +8.3% |
| 19-20 | 252 | 61,684.3 | 0.4605 | **1.5230** | 1.200 | +26.9% |
| 21+ | 301 | 73,902.7 | 0.3499 | **1.1572** | 2.474 | **−53.2%** |
| age-unknown | **0** | — | — | — | — | the cell is **empty** |

**Conservation: Σ anchor before 293,166.0 → after 293,166.0, delta 0.000000.** Pool Σv0 is held
**exactly**, by construction, as C5 requires.

**F8 at PLAYER UNIT** — effective n over players (weights = anchor), never player-seasons:

| band | players | eff-n | player-seasons | F8 (≥35) |
|---|---|---|---|---|
| ≤18 | 649 | 613.8 | 1,598 | **PASS** |
| 19-20 | 252 | 236.1 | 785 | **PASS** |
| 21+ | 301 | 280.1 | 853 | **PASS** |

Every band clears the bar comfortably at the player unit, so F8 is not what is in doubt here.

**Two findings, both flagged rather than smoothed:**

1. **The age-unknown cell is empty.** The directive requires age-unknown rows to "stay their own
   cell, never absorbed". On the DOB-written store (`d9a24282`, PR #390's 302 birthdates) **there
   are no pool rows without a birthdate at all**. The rule still needs to be *coded* — a future
   intake will arrive without a DOB — but it currently has no population, and audit 1's
   "priced as if he is 18" defect (175 records) is closed for the pool. Good news, and it should be
   on the record as such.
2. **HALT: the 21+ factor does not reproduce.** ≤18 (+8.3%) and 19-20 (+26.9%) are in the
   neighbourhood of the filed prior; **21+ lands at 1.157 against the filed 2.474, less than half.**
   The directive expects the re-derivation to move the numbers ("use the re-derived values"), but
   21+ is the band that *drives the whole repair* — it is audit 1's "under-priced by ~110 points
   each", the 2.07 return. Halving it halves ITEM B, and reshapes the package that sits on it.

   The seat is not confident enough in this number to re-teach on it, and says so plainly: it comes
   from **the same delivery instrument that failed the ITEM I level check in §3**. The most likely
   cause is on the horizon/discount axis — a 21+ pool entrant has a short career, so nearly all his
   delivery lands inside the year-11 cap and inside the low-discount years, while an ≤18 entrant's
   does not. A different horizon treatment would move the 21+ band far more than the other two.
   That is a hypothesis, not a finding, and it is exactly the sort of thing the missing probe
   scripts would settle in one run.

**OWNER DECISION REQUIRED:** ITEM B's factors are blocked behind the same ruler question as ITEM I.
The conservation machinery and the F8 reading are ready and proven; only the gradient's values are
in doubt.

---

## 4a. THE GATES — GREEN, AND THE BOARD REPRODUCES BYTE-EXACT

`gate_run.sh` in this directory, mirroring `docs/evidence/g1_never_rises_2026-08-10/gate_run.sh`
and pointed at the checkout (this branch changes no engine file, so the checkout **is** the engine
under test). Full transcripts alongside it.

| gate | result |
|---|---|
| `rl_export.py` (F1 export↔engine parity) | **exit 0** |
| **board rebuild md5** | **`4b448a821f54180182637983f7a26a9d`** — **byte-identical to the committed board** |
| `s4_matrix_M1v7.py` (F2 book↔board parity) | **exit 0** |
| `one_source_selftest.py` — the standing gated build | **exit 0 · 147 PASS / 0 FAIL / 0 STALE** (the expected baseline) |
| — D14a cross-draft dispersion | **PASS** 0.000000 over the 1,448 rows the surface prices |
| — D14b V0 pick inversions | **PASS** 0 |
| — D14c KPP retention floor O1 depth-monotone | **PASS** |
| — D14d never-rises on the surface | **PASS** 0 rising steps, picks 1-64 **and** the full 1-90 grid (8,010 pairs) |
| `guard_correction_canary.py` (Guard 4) | **exit 0** |
| `ship_gates_check.py` (the hand-run superset) | **exit 1 — pre-existing, not this branch (below)** |

**The board rebuild is the control that matters.** Rebuilt from this branch's bytes on this box, the
board comes back `4b448a82` — the committed board, unchanged. That is the direct proof of the claim
made in §0: this branch moves nothing.

**The one red row, and why it is not this branch's.** `ship_gates_check.py` halts before it runs a
single gate:

```
============ CONFIG MANIFEST (gate mode) REJECTED — BUILD HALTED ============
  - DIVERGENT model override RL_GAMMA='0.85' != manifest '1.0'
```

The cause is `ship_gates_check.py:64`, which hard-sets `RL_GAMMA='0.85'` — the START_HERE §2 value —
while the gate manifest pins `1.0`. **This is exactly the ENV-PIN CONFLICT the directive parked in
§4** ("two 'canonical' environments coexist in the tree — a documentation repair, its own small item,
not this act"). It is provably pre-existing rather than introduced here: this branch's entire diff
against main is `docs/evidence/composition_2026-08-10/`, and no engine, config or manifest file is
touched, so the halt reproduces identically on `110afb3`.

Worth stating for the record, because it is a live gap rather than a cosmetic one: **the hand-run
superset is currently unrunnable under the gate manifest.** The laws it carries are not lost — D14a-d
run inside `one_source_selftest.py` §(11) and are green above, which is precisely the wiring ruling
1.2 put in after the 2026-08-05 break went nineteen days unseen. But the checklist's own extra
coverage (three-column board, snapshots, the FLOOR-SAVES table) cannot be hand-run in gate mode by
anybody today. Flagged, not fixed — fixing it is the parked documentation item, not this act.

---

## 4b. THE MRAZ LINE — the BEFORE side, which is a flag on its own

The package did not land, so **there is no combined move to print**. What can be printed, and is —
`mraz_line_probe.py` — is where Mraz already stands against his standing surprise-scaled-trust
tolerance *before* anything moves. It is the baseline any future combined-move line is measured from,
and it does not wait on the rest of the act.

| quantity | value |
|---|---|
| identity (per the board) | Noah Mraz — Hawthorn KPD, pick 35, class 2024 |
| record | 2026: 4 games @ 84.25 |
| pick-35 curve value (frozen `_PVC0` ruler, ladder ccy) | **561.0** |
| entry anchor | 487.5 |
| **board price** | **3,555** |
| **board price ÷ pick-35 curve value** | **6.34× (raw) · 6.67× (ladder ccy)** |
| the charter's line | **3.5×** → 1,963.5 ladder / 1,865.7 board |

**Read straight: Mraz already sits at roughly 6.3-6.7× his pick's value on the shipped board —
close to double the 3.5× line — before any item of this package touches him.** His ruled band ran
2-3× at stage 4 and was slackened to 3.5-3.8× at stage 5; he is well beyond even the slackened top.

Two things follow, and neither is a resize:

1. **The breach is not something this act would create.** Any combined move ITEM A/C/D would add
   lands on an already-breached baseline. That materially changes what the Mraz check is *for*: as
   specified it asks "does the package push him through his tolerance?", and the answer is that he
   is through it already, on four games.
2. **It is a flag for the owner, per the charter** ("breach = FLAG, do not resize"). Recorded here,
   in the PR, and in the final report. Nothing was resized, and no component was tuned to move him.

---

## 5. WHAT WAS NOT STARTED, AND WHY — NOTHING IS SILENTLY DROPPED

| item | why not started |
|---|---|
| **ITEM A** (A1 full carry + conservation re-teach) | ruled to ship only on clean restated v0 verdicts — ITEM I halted (§3). **Also carries its own open design question**: §6 below. |
| **ITEM D** (three-class sit tilt) | the 1.378 [1.05, 1.80] contrast is on the not-re-runnable list (§6 disc. 10); its cautious-end sizing needs the contrast re-measured on the corrected ruler, i.e. behind ITEM I. The class machinery itself already exists in the engine (`_sitout_cls` already carries RUCK/KPP/nonKPP — the ruled three classes need no new structure). |
| **ITEM E1/E2** (ruck wage ramp / cap releasable) | E1's site is located and is a one-line change (`_merged_recover.py:461`, `wage = 0.0 if pos=='RUCK' else …`); its [+2.9%, +9.0%] band comes from ruck measurements on the not-re-runnable list. E2 rides C's `w`, which is ready. |
| **ITEM H** (the ruled cuts) | the cut sizes are on the not-re-runnable list; and H is C's funding, so it lands with C on one book. |
| **the side-by-side** | requires the items above plus the F8 re-measure of every named cell, which requires the ruler. |
| **the publication layer** (sibling repin, release-block, bundles, lineage) | the G1 lesson is followed by *not needing it*: **this branch does not move the board.** The ring-fence in `ui/tests/club_curve_provenance.test.py` compares the shipped bundle's board stamp against the release manifest, and both are unchanged at `4b448a82`, so it is green as it stands. The publication lane is required the moment ITEM A/B/C/D/E/H write — and it is documented in `docs/evidence/g1_never_rises_2026-08-10/README.md` §8 step by step, ready to walk. |

---

## 6. ONE DESIGN QUESTION ITEM A CANNOT ANSWER FROM THE DIRECTIVE — FOR THE OWNER

Recorded here because it will be the first thing the next build seat hits, and it is a shape
decision, not an implementation detail.

ITEM A says the year-1+ anchor leg borrows the fitted year-0 prior, "fading on the **EXISTING games
ramp** across ALL years (v2 borrows less than v1, more than v3)", and adds "no new machinery". The
engine has **four** existing games/evidence ramps that fit that sentence, and they fade at very
different rates:

| candidate | where | behaviour |
|---|---|---|
| `LAM_SIT` — the sit-out blend | `_merged_recover.py:1126`, used at `sitout_ev:1851` | within-season games at pace; **resets every year**, so it cannot make v2 borrow less than v1 |
| `tfade` — pole fade by developmental tenure | `raw_ev:462`, `[1.00, 0.76, 0.40, 0.16, 0.05, 0.05]` | exactly "v2 less than v1, more than v3", but it is the **pedigree** fade, which the sitting ruled STAYS pick/pedigree |
| `exp(−E_q/τ)`, τ=1.1 — the pedigree-fade family | `iso_eff:495`, `_ISOFADE_TAU` | cumulative, games-driven, already the engine's borrow-fade instrument; a true state function of the record |
| `_expgate` on `POLE_RAMP=22` | `raw_ev:463`, `_expgate:297` | cumulative exposure ramp, but saturates inside two seasons |

The seat's reading is the **third** — `exp(−E_q/τ)` is the engine's own existing prior-borrowing
fade, it is cumulative across all years, and it satisfies the recalculation law by construction
(a synthetic year-2 probe responds to year-2 games, because `E_q` is recomputed from the record and
never stored). But the choice materially changes ITEM A's per-position deltas and therefore the
size of the conservation re-teach that follows it, and the directive's own measured deltas
(KPD +16,546 … NET −69,172 engine / −65,728 board) were produced under *some* choice that is not
named. **The seat did not pick it unilaterally.** One owner sentence settles it.

Architectural note for whoever wires it: ITEM A must blend at the `ev()` level, **not** inside
`raw_ev`, or it becomes self-referential — `_v0_uncapped` calls `raw_ev` at `Y = debutyr − 1` to
build the very year-0 prior being borrowed. Blending at `ev()` (where `sitout_ev` already blends)
keeps V0 untouched by construction. Verified along the way: the V0 evaluation is pole-inert
(`_expgate` → 0 at zero evidence), so an ITEM E1 wage change also cannot leak into the frozen
surface — E1 is safe to wire without a re-bake.

---

## 7. FILES

| file | what it is |
|---|---|
| `README.md` | this record |
| `engine_load.py` | the read-only gate-mode loader every probe uses (`RL_GAMMA=1.0`, manifest `cef06fd6250b`) |
| `item_c_probe.py` · `_out.txt` | ITEM C: the six worked rows reproduced (§2.2) |
| `item_c_q3.py` · `_out.txt` | ITEM C: cohort stats, the H ladder (§2.3), the C-Q3 demonstration and the `sa` fallback comparison (§2.4) |
| `item_b_probe.py` · `_out.txt` | ITEM B: the re-derived pool age gradient, conservation proof, F8 at player unit (§4) |
| `ruler_probe.py` · `_out.txt` | ITEM I: the four-instrument reconstruction, first pass (§3.2) |
| `ruler_probe2.py` · `_out.txt` | ITEM I: the cohort/estimator variant sweep and the completed-career collapse that exposes the historical-context finding (§3.3) |
| `mraz_line_probe.py` | the Mraz standing-tolerance baseline (§4b) |
| `gate_run.sh` | the gate script, as run (§4a) |
| `gate_export.txt` · `gate_board_rebuild_md5.txt` · `gate_book.txt` · `gate_selftest.txt` · `gate_canary.txt` · `gate_ship.txt` | gate transcripts |

Every probe is read-only: it loads the engine, reads the store and the board, and writes nothing.

---

## 8. THE STANDING LAWS, OBSERVED

- **Recalculation law** — nothing here stores a per-player quantity; every figure is a state
  function re-derived from the record on each run.
- **F8 at player unit** — every effective-n in this record counts players. §4 prints the
  player-seasons beside it so the difference is visible rather than asserted.
- **No expectation site reads pick without position** — `par_at(pos, pick, T)` and
  `par_pole(pos, pk, T)` are both position-keyed; ITEM C's `Q` reads `par(pos, pick, draft-age)`.
- **Conservation shown, not asserted** — §4 prints Σ before and Σ after and their difference.
- **YEAR-4-IS-NOT-A-TARGET** — no component here is tuned to any year-4 number; the year-4 price
  appears only as the *denominator of the measuring instrument* in §3, which is what the law
  permits.
- **No blanket lifts** — nothing is lifted; nothing is written at all.
- **BRANCH-HELD** — no merge, no attribution column, no touch to main.
