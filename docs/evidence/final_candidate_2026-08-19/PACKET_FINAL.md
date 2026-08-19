# PACKET — THE FINAL-CANDIDATE ASSEMBLY on `daa16812`

**Branch `land/order-29`, worked from `origin/land/order-29` at `51707fd`. Engine `53fff6de` —
UNCHANGED. No engine edit was made and none was needed.**

> ## THE BOARD IS **PRICED, NOT ADOPTED.**
> Nothing here is adopted, merged, tagged or promoted. Those are owner-only acts. Nothing is on `main`.

---

## 1 · BOARD IDENTITY — THE FIRST PRICING ACT, DISCHARGED

**`daa16812e50fb71241e627d89180412c` · TOTAL 660,578 · 804 ROWS — reproduced byte-exact on this
seat's own clean build before anything else was run.**

| board | dial line | expected | **got** | |
|---|---|---|---|---|
| **`FC_CAND`** | the full candidate line **+ `RL_O42=1`** | `daa16812` | **`daa16812`** · 660,578 · 804 | **PASS** |
| `FC_CAND2` | determinism repeat | `daa16812` | **`daa16812`** · 660,578 | **PASS** |
| `FC_BASE` | same, `RL_O42` UNSET | `ff936186` | **`ff936186`** · 659,222 | **PASS** |
| `FC_IDENT_P` | every ORDER-38*/39/40/41/42 dial OFF | `374d4e44` | **`374d4e44`** · 666,434 | **PASS** |
| `FC_IDENT_K` | ORDER K's ruled line | `f3101883` | **`f3101883`** · 673,097 | **PASS** |
| `FC_L0R` | R20A, the owner's reference | `7f88f509` | **`7f88f509`** · 664,950 | **PASS** |
| `FC_NOR3` | the R3-off companion (§5b) | — | `500811ba` · 667,847 | built |

Pinned inputs, printed on every run: engine `53fff6de` · store `cb38ef11` · v0surf **`5dd34ca8`**
(`RL_V0SURF_PKL` bound explicitly on every single run — see §2) · sheet `b26798c3…`.

**Day-0 89 of 89 on every board built, tolerance 0.**

The full dial line, as run:
`RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_BETASAT=0.105 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=15
RL_O40_RECW=0.47 RL_O40_PGMAT=1 RL_O41_SDOFF=2.98 RL_O41_CREDIT=1 RL_O41_RESET=1 RL_O41_INJ=1
RL_O41_R3=1 RL_O41_RAMP=1 RL_O41_BREAK=unwind RL_O41_UNWIND=7 RL_O42=1`

**U0 = 7 return games is carried throughout as OWNER-RULED, DATA-SUPPORTED.**

Raw: `BUILD_FC_out.txt`, `BUILD_FC_NOR3_out.txt`.

---

## 2 · GUARD 5 — RED, PRE-EXISTING, AND NOT CLAIMED GREEN

`bash run_panel.sh` exits 1 on this branch. Its own named remedy `bash bootstrap.sh` also exits 1.
The same five complaints the D6 seat recorded survive the remedy: `rl_model` `98f16794` vs pin
`14000af2`; the v0surf **load path**; the workspace engine vs `engine_head`; and `fv` CHECKOUT and
LOADED-PATH drift. **This is item C3 on register v767, it pre-dates this seat, and re-pinning is a
landing act outside it. Guard 5 IS NOT SCORED AS A PASS ANYWHERE IN THIS PACKET.**

**One thing worth the supervisor's eye.** Guard 5's v0surf complaint is that the load path resolves
to `/home/claude/v0surf.pkl` (`fbc5b393`), not the pin. That is `run_panel.sh` booting with
`RL_V0SURF_PKL` unset, where MAIN's surface silently wins precedence. **Every board, probe, census
and page in this packet binds `RL_V0SURF_PKL` explicitly to `<repo>/data/v0surf.pkl`, and every run
prints `5dd34ca8` — the pinned surface.** The complaint is real, and it does not touch a single
number here.

Raw: `GUARD5_FC_out.txt`.

---

## 3 · THE ACCEPTANCE SUITE — ELEVEN ITEMS, AND THE THREE THAT ARE NOT GREEN ARE NAMED FIRST

| item | required | measured on THIS build | verdict |
|---|---|---|---|
| board reproduces | `daa16812` / 660,578 / 804 | **`daa16812` / 660,578 / 804** | **PASS** |
| determinism ×2 | identical | **`daa16812` == `daa16812`** | **PASS** |
| day-0 | 89/89 | **89 of 89 on every board** | **PASS** |
| dial-off `RL_O42` | `ff936186` | **`ff936186`** | **PASS** |
| every ORDER-41+ dial off | `374d4e44` | **`374d4e44`** | **PASS** |
| K chain | `f3101883` | **`f3101883`** | **PASS** |
| R20A | `7f88f509` | **`7f88f509`** | **PASS** |
| **tail** | 0.8004 | **0.8004**, realized ratio **0.2979** | **PASS** |
| **burn** | 0 | **0 — every band, both populations** (R3-off line; §5a) | **PASS, with R3 unswept — §5a** |
| **birthday** | +0 | **+0 on the R3-off line.** On the candidate through the R3-aware probe: **the probe declines** | **NOT SCORABLE on the candidate — §5b** |
| **class mark** | the registered 1.0671 basis | **base reads `1.0671174504`. THE CANDIDATE CANNOT BE MEASURED** | **HALTED — §4** |
| **the 79/79 suite** | 79/79 | **56 checks, 55 PASS, 1 FAIL** | **§6** |
| **Guard 5** | PASS | **RED, PRE-EXISTING** | **NOT CLAIMED GREEN — §2** |

**Three items are not green: Guard 5 (red, pre-existing, not mine), the class mark and the no-arb
page (both HALTED on one shared cause, §4), and the candidate-line birthday (not scorable, §5b).
Not one of them is reported as a pass.**

---

## 4 · **THE HALT — THE CLASS MARK AND THE NO-ARB PAGE CANNOT BE PRODUCED FOR THIS BOARD**

**This is the finding of this pass and it is reported first among the failures, not buried.**

`run_emit_D6.sh` was committed unrun by the D6 seat precisely so this seat could produce the class
mark. **It was run. IT HALTS.**

```
ORDER 31-F HALT (replication): 86 of 89 wired entrants reproduce the board's printed day-0 at
tolerance 0. Mismatches: [('sam-allen', 450, 428, 791.8152857422534),
('ollie-murphy', 196, 200, 398.35828513161437), ('kobe-mcdonald', 40, 37, 87.02989219418069)].
```

No matrix is written. **Exit 1, `NO MATRIX`.**

### 4a · THE CONTROLLED TEST SAYS THE HALT IS `RL_O42`'s, AND THE GUARD IS RIGHT

The identical runner, identical engine, with **`RL_O42` unset and nothing else changed**:

> `ORDER 31-F REPLICATION: 89 of 89 wired entrants on board f3101883 reproduce printed day-0
> EXACTLY` · `emit exit=0` · `records=2648`

**86/89 with the dial on, 89/89 with the dial off.** The three rows are `sam-allen`,
`ollie-murphy` and `kobe-mcdonald` — **all three are D6's newly-annotated "gaining treatment" rows.**

**THE GUARD IS NOT MISFIRING; ITS PREMISE WAS WRONG.** `run_emit_D6.sh`'s own header states the
reason it does not re-base the day-0 reference: *"ORDER P changes NOTHING about entry prices or the
sitter fade: A(0) = 0 exactly, so a row with no games cannot move."* **Under `RL_O42=1` that is
false, and it is false measurably.** `fc_v0.py` re-reads `_landed_v0_board` — byte-carried from the
emitter — on the candidate's own engine state and confirms the entry prices really did move:

| row | v0 on the base | **v0 on the candidate** |
|---|---:|---:|
| `sam-allen` | 833.3 | **791.8152857423** |
| `ollie-murphy` | 419.2 | **398.3582851316** |
| `kobe-mcdonald` | 91.6 | **87.0298921942** |

The availability layer reaches the entry-price objects, so the candidate's year-0 law genuinely is
not ORDER K's published one. **The guard is doing exactly what it exists to do.**

### 4b · WHAT THIS SEAT DID NOT DO ABOUT IT

**The remedy is to re-publish the day-0 reference for this law** — which is what ORDER D and ORDER K
each did when they moved the fade. **That is a re-basing of a falsifier's own reference and it is
above this seat.** It was not done, not worked around, and not preregistered around.

**CONSEQUENCE, STATED WITHOUT SOFTENING — both the class mark and the no-arb tables read a
walk-forward matrix, not a board, so BOTH are unavailable for `daa16812`:**

- **THE CLASS MARK IS NOT MEASURED FOR THE CANDIDATE, AND IS NOT ASSUMED UNCHANGED.**
- **THE NO-ARB PAGE IS NOT BUILT FOR THE CANDIDATE** (Task 2 item 1 — see §6).

### 4c · WHAT *IS* KNOWN ABOUT THE CLASS MARK, AND A CORRECTION TO PACKET_D6

The instrument validates first: `fc_class.py` reproduces ORDER K's own published marks off ORDER K's
own matrix — **W2 1.0513 vs 1.0513, cohort 1.0324 vs 1.0324 → VALIDATED.**

| board | W2 mark (registered basis) | cohort clock |
|---|---:|---:|
| the assembly candidate `db1ccef5` | 1.0671174504 | 1.0423120554 |
| **`FC_BASE` `ff936186` — the candidate minus `RL_O42` only** | **1.0671174504** | **1.0423120554** |
| **`FC_CAND` `daa16812`** | **MATRIX MISSING** | **MATRIX MISSING** |

The base reads **exactly the registered 1.0671**, to ten decimal places, on the emit that carries
`RAMP`/`BREAK`/`UNWIND` — so those three dials do not move the mark, and the registered value stands
on the base. **It is NOT transferred to the candidate.** `fc_class.py` was changed in one respect
from the assembly copy: the assembly dropped absent labels silently, which would have made the
missing candidate vanish from the table without trace. It now **prints `FCCAND MATRIX MISSING`.**

> **A CORRECTION TO `PACKET_D6.md` §10b/§11, AND IT GOES AGAINST THE CAUTION RATHER THAN FOR IT.**
> D6 wrote that **"7 of the 31 movers sit inside that window"**. **The measured number is 2.** The
> registered W2 basis is DRAFT classes 2005-2015 = **cohort** years 2006-2016; five of D6's seven
> (Sam Powell-Pepper, Mitchell Hinge, Esava Ratugolea, Elliott Himmelberg, Toby Pink) are **draft
> 2016 = cohort 2017, outside the window.** Measured against the matrix's own cohort rule the two
> movers inside are **Jamie Elliott (draft 2011, cohort 2012)** and **Brayden Fiorini (draft 2015,
> cohort 2016)**. **This does not license assuming the mark is unmoved — two movers is not zero, and
> the mark is not measured.** Reported as measured, not as briefed.

Raw: `EMIT_FCCAND_run.txt` (the halt), `EMIT_FCBASE_run.txt` (the control), `V0_FC_out.txt`,
`CLASS_FC_out.txt`, `CLASS_FC.json`.

---

## 5 · BURN AND BIRTHDAY — THE R3-AWARE ROUTE, AND WHAT IT WOULD AND WOULD NOT GIVE

### 5a · BURN — **ZERO**, on the R3-off line, with the gap named

`os_census.py` **asserts on the candidate line**, on this seat's own build, exactly as D6 recorded:

```
board total (numeraire): 660578
AssertionError: identity broke on noah-mraz: 2135.777679 vs 1112.505054
```

Digit for digit the same two numbers D6 got. The census rebuilds price as
`[rho·e + age credit] + pi_base·(v·PL_F)·factor(v)` — **an identity with no absence-collector term** —
so it breaks on the first R3-faded row. **Noah Mraz is not a mover here: 1,057 on both boards.**

Scored on the **R3-off line**, which is the basis the assembly seat used for the same reason:

| population | n | burned | points |
|---|---:|---:|---:|
| the supervisor's population (\|fK−fP\|≥0.02) | 264 | **0** | **0** |
| all young rows | 289 | **0** | **0** |

**Zero in every band — 1-10, 11-20, 21-30, 31-40, 41+, pool. Worst five: "(none — the census is
ZERO)".**

> **NOT COVERED, SAID PLAINLY: the burn sweep has NOT been run through the R3 term.** The
> interaction of entry price with the R3 collector is **unswept** on this board, exactly as it was
> unswept on the assembly board.

### 5b · BIRTHDAY — **+0 on the R3-off line; NOT SCORABLE on the candidate, and the probe says so itself**

On the R3-off line the birthday census is clean: **81 age-23 rows with a pedigree leg · 0 gaining
50%+ · NET +0 · GAINS ONLY +0 · worst ratio 1.0000 · 0 rows moving at all**, zero in every band.

**On the candidate, through `as_r3age.py` — the R3-aware probe the order names — the answer is that
the probe REFUSES TO GIVE ONE, and this seat reports the refusal rather than a number.**

Two things stack up:

1. **The one-dial-apart baseline the probe needs CANNOT BE BUILT. The engine refuses it:**
   `ORDER 41 HALT: RL_O41_BREAK=unwind but RL_O41_R3 is unset. The break rule shapes a collector
   that is not switched on.` So the only R3-off board is **three settings apart**, which puts **59
   rows** in the comparison instead of the assembly's 9.
2. **With 59 rows the probe's own SELF-CHECK 2 fails — 47 of 59 agree — and it prints:**
   *"A SELF-CHECK FAILED. This probe cannot reproduce the board and therefore says NOTHING about the
   birthday question."* **That verdict is carried here unaltered.**

SELF-CHECK 1 passed **EXACT** (1,200 calls, worst disagreement `0.000e+00`), so the re-formed
collector is right; it is the comparison that cannot be made cleanly.

**THE DIAGNOSIS, OFFERED AS A DIAGNOSTIC AND NOT AS A SCORE:** every one of the 12 disagreements is
**exactly ±1 board point**. The board delta is a difference of two independently rounded integers;
the re-formed take is continuous. Substituting the true numeraire from `pick_redenomination.json`
(1.0524) for the probe's single-row inferred one (1.0527496141) moves it only to 48 of 59 — so it is
**integer rounding, not a lever mis-attribution**. **The probe was NOT modified to make it pass, and
no birthday number is claimed for the candidate.** The instrument gap is open.

Raw: `CENSUS_FCCAND_out.txt`, `CENSUS_FCNOR3_out.txt`, `R3_AGE_FC_out.txt`, `R3_AGE_FC.json`.

---

## 6 · THE DOCUMENT SET — FOUR OF FIVE BUILT, ONE BLOCKED

| page | file | status |
|---|---|---|
| **no-arb — current candidate only** | — | **NOT BUILT — blocked by §4** |
| **tracker** | `TRACKER_FINAL.html` · `TRACKER_FINAL.csv` | **BUILT** — 801 moved rows |
| **per-lever breakdown** | `LEVERS_FINAL.html` | **BUILT** — 12 levers |
| **year-1 page** | `YEAR1_FINAL.html` | **BUILT** — 105 rows, cohort 2026 |
| **player list** | `PLAYERS_FINAL.html` | **BUILT** — all 804 rows |

### THE 79/79 SUITE: **56 checks, 55 PASS, 1 FAIL**

The one failure is `noarb / the page exists / MISSING`. The arithmetic is exact and worth stating so
the number cannot be misread: the assembly suite ran **79** checks of which **24** were the no-arb
page's. With the page absent, 23 of those 24 cannot run and the 24th fails. **79 − 23 = 56.**
**Every check that can run on this board passes.**

**The suite is NOT reported as 79/79 and the missing 23 are not counted as passes.**

### The tracker — the header check the order asks for, done

The past defect was a missing delta column. The HTML header row and the CSV header row were compared
**field for field against `TRACKER_ASSEMBLY`**: `player · pos · club · cat · age · live · K ·
Δ live→K · P · Δ K→P · R · Δ P→R · CANDIDATE · Δ R→cand · Δ live→cand · Δ K→cand` —
**IDENTICAL, both files. All three of ΔR→cand, Δlive→cand and ΔK→cand are present.**

### The per-lever page — the two new levers are their own lines

`V755_CAND` → **`+ the unwind U0 = 7 return games` → `ff936186`** → **`+ D6 the injury
consolidation (RL_O42=1)` → `daa16812`**. Ten levers became **twelve**; neither new lever is folded
into another's marginal.

### The year-1 page — both past defects specifically closed

- **v0 POPULATED on all 105 rows — 0 empty.** It is **not** borrowed from the base: v0 is *not*
  dial-invariant (§4a), so it is read off the candidate's own engine state by `fc_v0.py`, which
  self-checks against the day-0 guard's own three numbers at tolerance 0 before writing anything.
  The cohort clock (`year`, `type`) *is* taken from the base matrix, and that is a **checked**
  equality, not an assumption: 2,648 of 2,648 rows carry identical `year` and `type` across two
  matrices built on different dial lines.
- **The two-way membership assertion is PRINTED on the page**: every included row is cohort 2026;
  no cohort-2026 board row is missing (**PASS, 0 missing**); **18 MSD rows** correctly included and
  2025-drafted MSDs correctly excluded. The build asserts and would fail closed.
- **BOARD ID `daa16812` printed on the page**, with total 660,578 on 804 rows.

---

## 7 · THE DOCUMENTED-RED LEDGER, CONFIRMED ON THIS BOARD

Every entry below was **re-measured on this seat's own build**, not carried over.

| ledger entry | status on this board |
|---|---|
| **modern picks 1-10 buy-red** | **CONFIRMED** — yr0→1 **+21.52%**, buy-margin **−7.52%**, BUY-RED |
| **modern picks 1-20 buy-red** | **CONFIRMED** — yr0→1 **+15.04%**, buy-margin **−1.04%**, BUY-RED |
| **late-band sell-reds, population-risk ruled** | **CONFIRMED** — primary picks 31-40 **−11.04%**, picks 41-64 **−7.44%**, both SELL-RED; modern 21-30 −15.88%, 31-40 −13.32%, 41-64 −27.68% |
| **tail 0.80 ruled** | **CONFIRMED — 0.8004** on the candidate's own charge form, realized ratio 0.2979 |
| **SSP inherited / parked** | **CARRIED, NOT RE-MEASURED** — it lives on the no-arb arm tables, which §4 blocks. Named on every page. |
| **Brodie reprieve self-limiting** | **CONFIRMED** — Will Brodie **147** on both base and candidate. The unwind strips him; the consolidation does not touch him. |
| **Conway keeps his sitting charges** | **CONFIRMED — 460 → 460, delta exactly 0.** |

**The band numbers above are measured on `FCBASE`, NOT on the candidate**, for the reason in §4 — the
candidate has no matrix. They are the nearest evidence that exists and they are labelled as the
base's every place they appear. `bb_noarbFC.sh` carries that warning in its own header, and **no
owner page was written from them.** All four instrument pins matched at run
(`0f822035…`, `d59ad550…`, `02dcf28c…`).

Raw: `NOARB_FCBASE_out.txt`, `BANDS_FC_out.txt`, `BANDS_FC.json`, `TAIL_FC_out.txt`.

---

## 8 · NEW THIS PASS — TWO DEFECTS FOUND IN THE INHERITED TOOLING

Neither is an engine fault and neither was worked around silently.

1. **`as_legs.py` carries `RL_O40_CAPPCT=20`. Every candidate since v750 is p15.** The assembly
   seat's own `LEGS_CAND.json` — the mechanism-legs column on its player page — was therefore
   computed on a cap anchor its board was not built on. `fc_legs.py` corrects it to `15` and adds
   the four dials the file never had (`RAMP`/`BREAK`/`UNWIND`/`RL_O42`). Effect is small and
   visible: the S-S5 limb-2 worst excess reads **1.4126%** here against the assembly's 1.4117%.
2. **`fc_class.py` silently dropped absent boards.** A missing matrix vanished from the table
   rather than being reported. Now printed as `MATRIX MISSING`.

Also carried forward from D6 and confirmed here: **`os_census.py` is unscorable on any R3 board**
(§5a), and **the continuity harness is blind to R3** — to which this pass adds that **`as_r3age.py`,
the replacement instrument, cannot be run one-dial-apart on any board carrying `BREAK=unwind`**
(§5b). Both are open instrument defects.

---

## 9 · WHAT THIS ORDER DID **NOT** DO

- **No engine edit.** `_merged_recover.py` is `53fff6de` before and after.
- **Guard 5 was not made to pass.** Red, pre-existing, disclosed (§2).
- **The day-0 replication reference was NOT re-based**, so the class mark and the no-arb page are
  missing rather than manufactured (§4b).
- **`as_r3age.py` was not modified to make its self-check pass**, so no candidate birthday number is
  claimed (§5b).
- **The base's no-arb bands were not presented as the candidate's**, and no owner page was built
  from them (§7).
- **Nothing was adopted, merged, tagged or promoted. Nothing is on `main`.**

---

## 10 · FILES

| file | what |
|---|---|
| `PACKET_FINAL.md` | this packet |
| `bbFC.sh` | the board harness — byte copy of `bbD6.sh`, scratch re-pointed |
| `build_FC.sh` · `BUILD_FC_out.txt` | the six boards, candidate first |
| `build_FC_nor3.sh` · `BUILD_FC_NOR3_out.txt` | the R3-off companion; `..._HALT_out.txt` is the engine refusing R3-off-alone |
| `run_emit_FC.sh` · `EMIT_FCCAND_run.txt` | **the emit HALT** |
| `EMIT_FCBASE_run.txt` | **the control emit — 89/89, matrix written** |
| `fc_v0.py` · `V0_FC.json` · `V0_FC_out.txt` | the candidate's own v0, self-checked against the guard |
| `fc_class.py` · `CLASS_FC_out.txt` · `CLASS_FC.json` | the class mark; instrument validated; candidate MISSING |
| `run_census_FC.sh` · `CENSUS_FCCAND_out.txt` · `CENSUS_FCNOR3_out.txt` | burn + birthday, both lines |
| `fc_r3age.py` · `R3_AGE_FC_out.txt` · `R3_AGE_FC.json` | the R3-aware probe, and its refusal |
| `fc_tail.py` · `TAIL_FC_out.txt` · `TAIL_FC.json` | the tail, 0.8004 |
| `fc_boards.py` · `BOARDS_FC_out.txt` · `MOVERS_LEDGER.json` | lever stack, determinism, the ledger |
| `fc_tracker.py` · `TRACKER_FINAL.html` · `.csv` · `LEVERS_FINAL.html` | the tracker and the per-lever page |
| `fc_pages.py` · `fc_box.py` · `YEAR1_FINAL.html` · `PLAYERS_FINAL.html` | the year-1 and player pages |
| `fc_legs.py` · `LEGS_FC.json` | the mechanism legs, on the corrected dial line |
| `fc_bands.py` · `BANDS_FC_out.txt` · `bb_noarbFC.sh` · `NOARB_FCBASE_out.txt` | the band tables, **on the base** |
| `fc_verify.py` · `DELIVERY_VERIFICATION_FC_out.txt` | the suite — 56 checks, 55 PASS, 1 FAIL |
| `GUARD5_FC_out.txt` | Guard 5 red, and red again after its own remedy |
| `os_lib.py` · `os_census.py` | byte-identical carries of the assembly's shared machinery |
