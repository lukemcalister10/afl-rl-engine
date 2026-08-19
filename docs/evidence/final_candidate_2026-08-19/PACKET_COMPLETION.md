# THE COMPLETION PASS ON THE PARITY BOARD `a05fe951` — DELIVERY PACKET

**Branch `land/order-29`, from `origin/land/order-29` at `9b93fba`, in this seat's own clean
worktree. Ordered by register v774 — the owner's word on the parity table: *"Completion pass
please."***

> ## THE BOARD IS **PRICED, NOT ADOPTED.**
> Nothing here is adopted, merged, tagged or promoted. **The tag and the `main` promote are
> OWNER-ONLY acts.** Nothing is on `main`. **NO ENGINE EDIT was made anywhere in this pass.**

---

## 0 · THE HEADLINE, INCLUDING THE PART THAT DID NOT WORK

**Four of the six ordered items are delivered. Three are HALTED, together, for one measured reason.**

| # | item | outcome |
|---|---|---|
| **1** | the amended day-0 disclosure, pushed **before** the reference was touched | **DELIVERED** — `355152c` |
| **2** | the day-0 reference regenerated on `a05fe951` | **DELIVERED — all nine assertions pass** |
| **3** | the walk-forward matrix on `a05fe951` | ### **HALTED** |
| **4** | the class mark on the candidate matrix | ### **HALTED** — blocked by item 3 |
| **5** | the full no-arb page for `a05fe951` | ### **HALTED** — blocked by item 3 |
| **6** | the regenerated document set on `a05fe951` | **DELIVERED** — tracker · levers · year-1 · players |
| **7** | the TRUE acceptance count | **DELIVERED — 42 run / 38 green / 2 named-red / 2 FAIL / 2 not run** |

**The halt is not a failure of the board.** `a05fe951` reproduces byte-exact, every dial-off identity
holds, determinism holds, and its own printed-day-0 identity reads 89 of 89 at tolerance 0. The halt
is an **instrument-versus-engine wiring gap**, found by a guard doing its job, and it needs a ruling
this seat is not authorised to make. Full diagnosis: **`HALT_EMIT_CP.md`**.

---

## 1 · THE BOARD

| | value |
|---|---|
| **THE PRICED BOARD** | **`a05fe951f78482c70520480e184c80ec`** |
| total | **664,949** · rows **804** |
| engine | `29376d5a73a3e8274fcebe5cd90ada0b` — **unchanged by this seat** |
| store / v0surf / sheet | `cb38ef11` / `5dd34ca8` / `b26798c35adcd9bda5cef50ff2c884da` |
| vs live `88ce647f` | **−87,480** · vs ORDER K `f3101883` **−8,148** · vs R `7f88f509` **−1** |

**FIRST PRICING ACT — reproduced byte-exact before anything was written.** `RL_V0SURF_PKL` was bound
explicitly to this branch tree's own `data/v0surf.pkl` on **every** run (register v767; Guard 5's own
output below independently confirms that footgun is live on this machine).

**The candidate was built THREE times** — `CP_CAND` (this seat's first pricing act), `D7_CAND` and
`D7_CAND2` (the determinism pair) — and all three are `a05fe951`, byte-for-byte.

---

## 2 · THE AMENDED DAY-0 REFERENCE REGENERATION — ITEMS 1 AND 2, DELIVERED

### 2.1 · The disclosure superseded the stale one ON THE RECORD, and went first

`REBASE_DAY0_AMENDED.md` was written and **pushed at `355152c` BEFORE the reference was touched.** It
supersedes `REBASE_DAY0.md` at `d5c37da` — the three-row disclosure written for the superseded board
`daa16812`, which was **never acted on** (the v771 owner ruling stopped it; `DAY0_FC.json` was never
written, and the absence of that file is the physical evidence the stop held). **`REBASE_DAY0.md` is
NOT deleted.** It stays as filed history, the way `DAY0_K.json` stays.

**Authority chain, all five links:** v763 bake item → v769 pull-forward → **v771 parity ruling (the
stop)** → v773 six-row finding (`D7-F8` **FIRED**) → **v774 the owner's completion word**.

### 2.2 · THE SIX ROWS — all annotated `injured=Y`, all UP

| key | pathway | depth (clock) | frozen | priced | move |
|---|---|---:|---:|---:|---:|
| `harley-barker` | ND pick 24, MID | 1.58 | 481 | **504** | **+23** |
| `blake-thredgold` | ND pick 26, KPD | 1.58 | 372 | **381** | **+9** |
| `max-king-syd` | ND pick 49, SF | 1.58 | 129 | **138** | **+9** |
| `liam-hetherton` | PDA pool, `PDA\|KPF` | 1.58 | 66 | **70** | **+4** |
| `ollie-murphy` | ND pick 41, KPD | 3.58 | 196 | **200** | **+4** |
| `noah-chamberlain` | PDA pool, `PDA\|SF` | 1.58 | 37 | **40** | **+3** |

`sam-allen` and `kobe-mcdonald` moved DOWN on the superseded board (450→428, 40→37) and **no longer
move at all** — the guard restores them exactly. So the amendment is **two downward movers removed
and five upward movers added**, not "three became six".

**These rows illustrate. They do not gate.** The gate is the assertion block.

### 2.3 · The nine assertions — ALL PASS

```
  A1  key set        : new 89 rows, old 89 rows, symmetric difference 0
  A2  derived_v0     : BIT-IDENTICAL on 89 of 89  — the matrix year-0 column does not move
  A3  printed movers : 6  — exactly the SIX rows the D7 parity harness named, no more and no fewer
  A4  each mover     : all six MATCH THE D7 TABLE (481->504 · 372->381 · 129->138 · 66->70 ·
                       196->200 · 37->40)
  A5  sheet          : every moved row annotated injured=Y; 5 of the 11 annotated wired entrants
                       did NOT move
  A6  non-movers     : 83 of 83 rows BYTE-IDENTICAL on EVERY field
                       (ty pos pick cell printed derived_v0 fade_D day0_price)
  A7  identity on the WRITTEN board a05fe951 : 89 of 89 at tolerance 0  (ND 46, pool 43)
  A8  direction      : 6 of 6 movers move strictly UP  (RL_O43 is a max — it can only RAISE)
  A9  parity-restored: sam-allen 450 and kobe-mcdonald 40 RESTORE EXACTLY
```

**83 of 89 BYTE-IDENTICAL — the headline the order names, asserted rather than asserted-away.**
`DAY0_CP.json` was written **only after** all nine passed. `DAY0_K.json` is **untouched**.

### 2.4 · Two instrument defects the first run exposed — DISCLOSED, NOT SMOOTHED

**The first run of `cprb_day0.py` HALTED with three assertion failures.** Both root causes were in
the **carried instrument**, not in the board. Full detail: `REBASE_DAY0_AMENDED.md` §8.

1. **The carried generator pre-dated the D7 second wiring site.** It formed the price on the **live**
   fade, so A7 read `82 of 89` on a board whose own assert reads `89 of 89`. Fixed by reading the
   engine's own `_D7_DFADE` ratio — **the assertion was not relaxed.**
2. **The membership join** re-normalised the sheet's `player` column and mis-mapped `Maxwell King` →
   `max-king-syd` — the artifact `PACKET_D7.md` §4.2 already named. **The row was never unannotated;
   the join was wrong.** Fixed by reading membership off the engine's own `_AVAIL_STATE` (37 → 37
   asserted) — **strictly stronger than the naive test.**
3. **A corrected count against this seat's own convenience:** **11** of the 89 wired entrants are
   annotated, not the 10 carried from the superseded file.

**None of the order's four halt conditions fired, on either run.** `A3`, `A4`, `A8` and `A9` passed
**before** both fixes — the six-row finding never depended on the defects.

---

## 3 · THE HALT — ITEMS 3, 4 AND 5

**Full report: `HALT_EMIT_CP.md`. Raw: `EMIT_CPCAND_out.txt`, `O31D_PROBE_out.txt`.**

The emit was run against the regenerated reference with `RL_O43` added to the dial pass-through
(`run_emit_CP.sh` — the disclosed script change). **It halted at 82 of 89.**

**THE CAUSE, MEASURED.** `ORDER D7` wired the parity guard into `ev` and into `_entry30b_price` — the
engine's day-0 predicate. **It did not wire it into `o31_D`, the fade itself.** The ORDER 31-F emitter
forms the day-0 price as `round(_landed_v0_board(q) × o31_D(q, BASE_REF))`, reading `o31_D` straight
out of the engine namespace **by design**, so that *"the guard cannot drift from the law it is
guarding."* The board is written through the **guarded** path; the emitter reads the **unguarded**
fade.

```
  key                  derived_v0       o31_D       d0*o31_D    _e30b_price  EMITTER    BOARD
  harley-barker          843.1285    0.571012       481.4362       503.5089      481      504   <-- DIVERGES
  blake-thredgold        503.3750    0.739244       372.1171       381.2208      372      381   <-- DIVERGES
  max-king-syd           278.3691    0.464716       129.3627       137.5416      129      138   <-- DIVERGES
  liam-hetherton         117.3045    0.566367        66.4374        69.5288       66       70   <-- DIVERGES
  ollie-murphy           398.3583    0.503262       200.4784       200.4784      200      200
  noah-chamberlain        86.6490    0.426113        36.9223        39.5300       37       40   <-- DIVERGES
  sam-allen              791.8153    0.540664       428.1057       449.6938      428      450   <-- DIVERGES
  kobe-mcdonald           87.0299    0.426113        37.0846        39.7037       37       40   <-- DIVERGES
```

**`ollie-murphy` does not diverge, and that is the confirming detail** — he is a riser, so no ratio
applies and the two arithmetics agree. Exactly the seven rows where the healthy fade wins diverge.

**THE GUARD IS BEHAVING CORRECTLY.** It fail-closed on a real divergence. **Nothing was worked
around:** no engine edit, no edit to the byte-carried emitter, and **no false reference written to
make a guard go quiet.**

### What is NOT claimed as a consequence

- **The class mark on the candidate is NOT MEASURED, NOT ESTIMATED, AND NOT CARRIED FORWARD.** The
  instrument reads `per_entrant_CPCAND.json`. The base `ff936186` reads **1.0671174504** on the
  registered W2 basis (drafts 2005-2015) and the instrument self-validates against ORDER K
  (1.0513 / 1.0324) — but **the candidate's own number is unknown, and this packet does not guess
  it.**
- **No owner no-arb page is written from a board that has no matrix**, and the base's no-arb status
  is **not** presented as the candidate's — the rule `bb_noarbFC.sh` already states in its own header.

**This needs an owner or supervisor ruling**, most naturally a **D7 follow-up order** wrapping
`o31_D` under `_O43` with its own prereg, its own falsifiers and its own dial-off byte-exactness
proof — after which items 3-5 run unchanged.

---

## 4 · THE ACCEPTANCE TABLE — EVERY ITEM GREEN OR NAMED

**44 items enumerated · 42 RUN · 38 GREEN · 2 NAMED-RED · 2 FAIL · 2 NOT RUN (blocked).**
**No headline is back-filled. The two fails and the two named-reds are named below.**

### 4.1 · Identity and determinism — 8 of 8 GREEN

| item | expected | got | |
|---|---|---|---|
| first pricing act `CP_CAND` | `a05fe951` / 664,949 / 804 | `a05fe951` / 664,949 / 804 | **GREEN** |
| `D7_CAND` | `a05fe951` | `a05fe951` | **GREEN** |
| **determinism ×2** `D7_CAND2` | equal | `a05fe951` — A-F4 did not fire | **GREEN** |
| **D7-off** `D7_BASE` | `daa16812` | `daa16812` | **GREEN** |
| **O42-off chain** `D7_NOO42` | `ff936186` | `ff936186` | **GREEN** |
| **all-O41+-off** `D7_IDENT_P` | `374d4e44` | `374d4e44` | **GREEN** |
| **ORDER K** `D7_IDENT_K` | `f3101883` | `f3101883` | **GREEN** |
| **R20A** `D7_L0R` | `7f88f509` | `7f88f509` | **GREEN** |

### 4.2 · Board totals — 4 of 4 GREEN

`live` 752,429 · `IDENT_K` 673,097 · `IDENT_P` 666,434 · `L0_R` 664,950 — all as expected.

### 4.3 · Printed-day-0 identity on every written board — 5 of 5 GREEN

`CP_CAND` · `D7_CAND` · `D7_CAND2` · `D7_BASE` · `CP_NOR3` — each **89 of 89 at tolerance 0**.

### 4.4 · The day-0 reference regeneration — 9 of 9 GREEN

`A1`–`A9` as printed in §2.3, raw at `REBASE_DAY0_AMENDED_out.txt`.

### 4.5 · The documents — 8 of 8 GREEN

| item | reading |
|---|---|
| tracker rows | **801** — the 801-row format |
| tracker header | **FIELD-FOR-FIELD IDENTICAL** to `TRACKER_ASSEMBLY.csv`, all delta columns present, candidate column = `a05fe951` |
| per-lever page | **13 levers** — the D7 parity guard has **its own line**; the unwind and the D6 consolidation keep theirs |
| year-1 cohort | **2026, 105 rows** (18 MSD) |
| year-1 membership assertion | **PRINTED AND PASSING** — 105 checked / **0 violations** / **0 missing**; 2025-drafted MSDs correctly excluded |
| year-1 v0 | **every v0 populated — 0 blank cells** |
| year-1 board id | **`a05fe951` printed on the page** |
| full player list | **804 rows**, live vs candidate, absolute and relative, ranks |

### 4.6 · The supporting instruments — 4 GREEN, 1 NAMED-RED

| item | reading | |
|---|---|---|
| v0 self-check | the 8 named rows reproduce the **frozen reference's** `derived_v0` at tolerance 0 | **GREEN** |
| v0 coverage | **804 of 804** rows carry a v0 object; **0** without | **GREEN** |
| mechanism legs | 2,650 rows | **GREEN** |
| movers ledger | 801 rows | **GREEN** |
| **tail calibration** | **0.8004** on the candidate's own charge form | **NAMED-RED — the ruled documented-red "tail 0.80". Reported at what it reads; no dial was touched to chase it.** |

### 4.7 · THE TWO FAILS AND THE SECOND NAMED-RED

| item | outcome |
|---|---|
| **the ORDER 31-F replication guard (the emit)** | ### **FAIL — 82 of 89.** §3 and `HALT_EMIT_CP.md`. Blocks the class mark and the no-arb page. |
| **the R3-aware burn/birthday probe** | ### **FAIL — self-check 47 of 67.** It therefore says **NOTHING** about the birthday question, and is reported as a failure rather than worked around. **THE FAILURE IS PRE-EXISTING** — the FC seat's own run of this probe **also failed, 47 of 59**, on the superseded board, and its **12 disagreeing rows are byte-for-byte the same 12 here**. D7 adds **8** more, and **all 8 are D7-treated riser/tie rows** for which the probe predicts **exactly 0.0000** while the board moves — the probe models the direct R3 take and is **not `RL_O43`-aware**, the same class of instrument-versus-engine gap as the emit halt. |
| **Guard 5** | ### **NAMED-RED — C3.** Pre-existing six-pin `rl_model` staleness on this branch. Raw at `GUARD5_CP_out.txt`. **NOT claimed green anywhere. NOT re-pinned.** Its `v0surf` line independently confirms the register v767 footgun (`/home/claude/v0surf.pkl`, md5 `fbc5b393`, shadowing the pinned `5dd34ca8`) — which is exactly why every run in this pass bound `RL_V0SURF_PKL` explicitly. |

### 4.8 · NOT RUN — 2, both blocked, neither guessed

| item | why |
|---|---|
| the class mark on the candidate matrix | no matrix exists (§3). **Not measured, not estimated.** |
| the full no-arb page for `a05fe951` | no matrix exists (§3). **No owner page written.** |

---

## 5 · THE RED LEDGER — WHAT COULD AND COULD NOT BE MEASURED ON THIS BOARD

| ruled documented-red | measured on `a05fe951`? |
|---|---|
| **tail 0.80 ruled** | **YES — 0.8004**, on the candidate's own charge form (`TAIL_CP_out.txt`) |
| modern 1-10 and 1-20 buy-side reds — **ruled accepted** | **NO — not measurable.** The no-arb instruments read a matrix. Carried forward as ruled, **not re-measured and not re-asserted on this board.** |
| late-band sell-reds — **population-risk ruled** | **NO — not measurable**, same reason |
| **SSP inherited / parked** | **NO — not measurable**, same reason |

**Three of the four red-ledger cells could NOT be measured on this board**, and this packet does not
carry the base's readings forward as though they were the candidate's.

---

## 6 · THE LEVER STACK, WITH D7 AS ITS OWN STEP

```
  board          total     marginal    moved       up     down  worst row  the lever added
  V755_CAND    665,249       -1,025        9        0        9       -606  + absence I4  the R3 production fade
  FC_BASE      659,222       -6,027       50        0       50       -972  + the unwind U0=7 return games  — OWNER-RULED, DATA-SUPPORTED
  FC_CAND      660,578       +1,356       31       20       11       +708  + D6 the injury consolidation (RL_O42=1)
  CP_CAND      664,949       +4,371       23       23        0     +1,212  + D7 THE PARITY GUARD (RL_O43=1)  = THE CANDIDATE

  THE WHOLE ARC R -> CANDIDATE: -1  (sum of the marginals: -1)
```

**The D7 marginal reproduces the parity table exactly: +4,371 over 23 rows, 23 up, ZERO down, worst
row +1,212 (Tom Green).** The arc reconciles to the point: the candidate sits **1 point** below the
owner's R reference on a 664,950-point board.

---

## 7 · MOVERS VERSUS LIVE

| | rows | net |
|---|---:|---:|
| **candidate vs live `88ce647f`** | **144 up · 651 down · 6 unchanged** (801 tracked) | **−87,480** |
| **candidate vs R `7f88f509`** | **229 up · 252 down · 320 unchanged** | **−1** |

Biggest up vs live: Tom Green +832 · Nicholas Martin +655 · Connor Rozee +655.
Biggest down vs live: Harry Sheezel −1,331 · Archie Roberts −1,155 · Mitchell Edwards −1,113.

**Named to illustrate the shape of the move. They do not gate anything.**

---

## 8 · WHAT THIS PASS DOES NOT CLAIM

- **The candidate is not adopted.** **Priced, not adopted.** The tag and the `main` promote are
  OWNER-ONLY.
- **Guard 5 is not green.** It is RED, C3, pre-existing, recorded raw, not re-pinned.
- **The class mark and the no-arb numbers are not known for this board** and are not guessed.
- **The birthday question is not answered.** The probe failed its own self-check and therefore says
  nothing.
- **Three of four red-ledger cells are not measured on this board** and are not carried across.
- **`D7-F8` FIRED** and stays reported as having fired.
- **U0 = 7 return games — OWNER-RULED, DATA-SUPPORTED**, both halves, wherever quoted.
- **Depths are quoted as depths (clock values)**, never as "Nth year" prose.

---

## 9 · FILES

```
docs/evidence/final_candidate_2026-08-19/
  PACKET_COMPLETION.md              this file
  REBASE_DAY0_AMENDED.md            the disclosure — PUSHED FIRST at 355152c; §8 appended after the run
  REBASE_DAY0_AMENDED_out.txt       the raw regeneration, all nine assertions printed
  cprb_day0.py                      the regenerator (fcrb_day0.py carried, re-keyed to six rows + A8/A9)
  DAY0_CP.json                      THE REGENERATED REFERENCE, board a05fe951
  HALT_EMIT_CP.md                   the halt report for items 3/4/5
  EMIT_CPCAND_out.txt / _run.txt    the raw emit halt, unedited
  cp_o31d_probe.py / O31D_PROBE_out.txt   the read-only probe locating the divergence
  run_emit_CP.sh                    the emitter runner with the RL_O43 pass-through (disclosed)
  TRACKER_COMPLETION.csv / .html    801 rows, header identical to TRACKER_ASSEMBLY.csv
  LEVERS_COMPLETION.html            13 levers, D7 on its own line
  YEAR1_COMPLETION.html             cohort 2026, assertion printed, every v0 populated
  PLAYERS_COMPLETION.html           804 rows
  BOARDS_CP.json / _out.txt         the identity chain and the lever decomposition
  V0_CP.json / _out.txt             804 of 804 v0 objects
  LEGS_CP.json · TAIL_CP · R3_AGE_CP · MOVERS_LEDGER.json
  GUARD5_CP_out.txt                 Guard 5 RED, recorded raw
  cp_tracker.py cp_pages.py cp_v0.py cp_legs.py cp_boards.py cp_r3age.py cp_tail.py
```

**Priced, not adopted.**
