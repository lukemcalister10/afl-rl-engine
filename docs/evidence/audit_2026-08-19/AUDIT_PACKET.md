# AUDIT PACKET — INDEPENDENT VERIFICATION OF THE CANDIDATE `fbf61d05`

**Seat:** INDEPENDENT AUDIT. Had no part in building the candidate. **Date:** 2026-08-19.
**Branch audited:** `land/order-29` at `4ae7246`, and the variant that landed mid-audit at `fba1a7f`.
**This seat fixed nothing, adopted nothing, and edited no engine file.** Everything below was
re-derived in a private worktree; the shared checkout was never touched.

**Scope of what was actually re-run here:** eight full engine builds, every one from the tracked
engine on this seat's own worktree with `bbASM.sh`'s staging copied verbatim — strictly sequential,
five-var thread pinning, `PYTHONHASHSEED=0`. Plus independent re-implementations of the class
instrument, the R3 rule, the tracker cross-check, the lever telescoping and the path test.

---

## THE HEADLINE

**The board is real.** The candidate reproduces byte-exact, twice, on an independent worktree. Every
dial-chain identity holds. The class mark is right. The tracker, the per-lever page, the year-1 page
and the no-arb page all reproduce at row level against the boards' own JSON.

**The documents are not.** `PACKET_ASSEMBLY.md` — the file the owner reads — still carries the
**superseded** board's lever table, and it scores two of its own pre-registered predictions as HELD
when the delivered candidate falsifies both. One of those predictions had an explicit falsifier
written into the prereg ("a total ABOVE R falsifies my understanding of the stack and I will say
so"). **It fired, and the packet does not say so.**

**And one mechanism does not do what the packet says it does.** The R3 production fade is documented
as leaving one-season-out rows untouched. It does not. The rows it reaches in that band are selected
by the engine's own long-term-injury register — which is also the register the two-channel injury
exemption does not consult.

---

# PART 1 — FINDINGS, RANKED BY SEVERITY

## F1 · HIGH · THE PACKET DESCRIBES THE SUPERSEDED BOARD, AND SCORES TWO FALSIFIED PREDICTIONS AS HELD

**The owner is about to spend time on this file. These numbers are wrong on the delivered candidate.**

`docs/evidence/assembly_2026-08-19/PACKET_ASSEMBLY.md`:

| line | what it says | what the delivered candidate is |
|---|---|---|
| 415 | lever table CANDIDATE row = `ca73176e`, **654,031** | `fbf61d05`, **665,180** |
| 416 | determinism row = "`ca73176e` both runs" | the repeat was run and is `fbf61d05` |
| 429 | R3 marginal **−12,232** on 124 rows | **−1,083** on **12** rows |
| 431 | whole arc R → CANDIDATE **−10,919** | **+230** |
| 750 | prediction **P3** scored **"HELD — 654,031"** | **P3 IS FALSIFIED** (below) |
| 756 | prediction **P9** scored **"HELD"** | **P9 IS FALSIFIED** (below) |
| 768 | acceptance determinism "PASS — `ca73176e` both runs" | true of `fbf61d05`, stated of the wrong board |
| 825 | deliverable 2 = board **`ca73176e`** | `fbf61d05` |
| 830 | year-1 page "**102 rows**, the 2025 draft" | the page has **105 rows** and is **cohort 2026** |

**P3 — the prereg's own falsifier fired and was not reported.** PREREG_ASSEMBLY.md §5 P3:
*"Predicted candidate total: 630,000 to 660,000. **A total ABOVE R falsifies my understanding of the
stack and I will say so.**"* The delivered candidate is **665,180**, which is outside the band **and
above R (664,950)**. The packet scores P3 "HELD" by quoting the superseded total.

**P9 — falsified on the delivered board.** P9 predicted R3 moves more than I1+I2+I3 combined. On
`fbf61d05` R3 is **−1,083** against **−3,722** for the other three. R3 is now the *smallest* absence
collector, not the largest. The packet scores it HELD by quoting −12,232.

**Not in scope of this finding, and worth saying:** the **per-lever HTML page and the tracker are
CORRECT and current** — I re-derived every cell of both. It is the packet's own markdown tables that
were not regenerated when the candidate changed.

Evidence: `AUD_DOCS_out.txt`, `AUD_BUILDS_out.txt`.

---

## F2 · HIGH · R3 CHARGES ONE-SEASON-OUT ROWS, AND THE LONG-TERM-INJURY REGISTER IS WHAT SELECTS THEM

**The declared behaviour.** PREREG_ASSEMBLY.md §4.4 and PACKET_ASSEMBLY.md line 196 both state:
*"Day-0 and one-season-out rows are untouched."*

**The built behaviour.** Three of the twelve rows R3 charges have missed **exactly one** season:
`−7`, `−15`, `−36` (58 board points). Every one of them has played every season up to 2025 and is
absent only in 2026.

**The mechanism, traced to the line.** In `engine/rl_after/_merged_recover.py`:

- `o41_absence_depth` (line 4761) returns `1.0 + _n`, where `_n` starts at `_o41_fe(Y,p)` — the
  in-progress season's fraction.
- `_fEy` (line 130) returns `SEASON_FE` = **0.58** normally, but **1.0** for a row `_fe_p_one(p)`
  marks as out — i.e. a row on `LTI_REGISTER.md`.
- `o41_r3_take` (line 4814) exempts only `if _cx < 2.0`.

So an ordinary row absent in 2026 has depth **1.58 → uncharged**. A row on the long-term-injury
register has depth **exactly 2.00 → charged** at F3's depth-2 cost (0.367 of delivered value).

**Verified decisively, not inferred.** Of the **41** rows whose only unplayed season is 2026:
**all 3 that are charged are on `LTI_REGISTER.md`, and not one non-LTI row is charged.**

**Being on the long-term-injury register is what makes a one-season absence chargeable at all.**
That is the opposite direction from the two-channel law's intent, and it is declared nowhere.

Evidence: `AUD_R3_out.txt` (test 2), and the LTI cross-tabulation reproduced in Part 3 below.

---

## F3 · HIGH · THERE ARE TWO INJURY REGISTERS AND THE EXEMPTION READS ONLY ONE

R3's two-channel exemption is keyed **solely** to `docs/owner_annotations/SITTER_2026_v1.csv`
`injured=Y` — 37 rows, md5-asserted (I re-read the file: md5 matches, 219 rows, 37 injured, and all
37 names match exactly one store row each — that part is clean).

The engine carries a **second** injury record of its own: `LTI_REGISTER.md`, 43 rows, tracked in the
repo, copied into the staging by `bbASM.sh` line 18, and the object that sets `out=True` → `fE=1.0`.
**It is never consulted by the exemption.**

| | count |
|---|---:|
| rows on `LTI_REGISTER.md` | 43 |
| of those, **not** `injured=Y` in the owner annotation → **not exempt from R3** | **21** |
| R3-charged rows that are on the LTI register | **4 of 12** |
| board points those 4 carry | **664 of 1,083 (61%)** — including the single largest charge |

So absence the engine itself classifies as long-term injury is priced by a collector whose own
docstring calls it *"MULTI-SEASON **UNEXPLAINED** absence"*.

**Stated fairly:** the owner has separately said he wants the largest of those rows stripped, so the
*outcome* on that row may well be what he wants. The point of the finding is that the *mechanism*
reaching it is not the one the packet describes, and 20 other long-term-injured rows sit in the same
unguarded position.

---

## F4 · MEDIUM · THE STANDING BOX CONTRADICTS ITSELF ON THE COMPRESSION ANCHOR — ON ALL THREE OWNER PAGES

The "what is in this board" box (`as_box.py`) leads with:

> **The compressed cap at the 20th percentile**

The board is built at **p15** (`RL_O40_CAPPCT=15`, ruled at v750). Four paragraphs later the *same
box* says the anchor *"was moved to the 15th percentile"*. The headline mechanism line is simply
wrong, and it is the line describing what the board does.

Present once each, both readings, on `ASSEMBLY_PLAYERS.html`, `ASSEMBLY_YEAR1.html` and
`ASSEMBLY_NOARB.html`.

---

## F5 · MEDIUM · FOUR LIVE OWNER-FACING ITEMS ARE NOT ON THE PAGES

The box does carry: modern 1-10, SSP, RUCK parked, the depth-4 rise and its consequence, the
option-shaped deep cell, SF left alone, the untested veteran board, the conviction speed. Good.

It does **not** carry:

1. **The tail's built number 0.8004.** The box says *"THE BUILT NUMBER FOR THIS BOARD IS PRINTED IN
   THE PACKET AND IT RULES"* — it defers rather than prints. The register carries 0.8004 as a
   standing red awaiting an owner word.
2. **The modern 1-20 breach** (+15.04, fails the path test on the candidate and on R alike). v751
   recommended extending the documented red to it; it is in the no-arb tables but not named in the box.
3. **The late-band sell-red deepening** (31-40 −11.04 / 41-64 −7.44 vs P −8.88/−5.03) — the
   deterioration v751 leads with, and the one where the supervisor's earlier claim was wrong in sign.
4. **The Brodie-shield open defect** — v753's own honestly-declared open defect, in the packet but
   not on any owner page.

---

## F6 · MEDIUM · PROCESS — ONLY THE FIRST OF FOUR ENGINE-EDITING PASSES WAS PREREGGED

There is exactly **one** prereg on the branch. Commit order:

| commit | time | engine edited? | prereg pushed first? |
|---|---|---|---|
| `c1dbd3e` PREREG | 07:34 | no | — |
| `7aa089d` the ORDER 41 wiring | 07:54 | **yes** | **YES** — c1dbd3e precedes it. **PASSES.** |
| `cefa05f` v750 finishing build | 09:04 | **yes** | **no** |
| `93f001f` the R3 rewrite | 09:51 | **yes** (+111 lines) | **no** |
| `fba1a7f` the fractional break rule | 10:12 | **yes** | **no** |

The R3 rewrite is the single largest mechanism change in the delivery — the repair of the defect the
owner himself caught — and it went in with no pre-registered spec. `93f001f` does not touch
`PACKET_ASSEMBLY.md` at all; the section describing it (§6c) arrives one commit later. The other two
edit the packet in the *same* commit as the engine, which is not "before".

The rulings themselves (v752 commissions the R3 fix in some detail) partly substitute for a prereg,
and the delivered work is candid about its own misses. But the discipline as written was not kept
after the first pass, and the packet's §12 row 1 claims it for the delivery as a whole.

---

## F7 · LOW · THE PREREG CONTRADICTS ITSELF ON WHETHER THE ANNOTATION IS READ FOR NEVER-DELIVERED ROWS

- §4.3 rule 3: *"Rookies / never-delivered rows: CAUSE-BLIND, UNCHANGED. **No annotation is read for
  a row with no delivered season**, whatever its `injured` flag says."*
- §4.4: *"INJURED-ANNOTATED ROWS ARE EXEMPT"* — no delivered qualifier.

The code follows §4.4: `o41_r3_take` line 4818 is a bare `if o41_injured(p): return 0.0` with no
delivered-season gate. (The *clock pause* in `o31_cu` **is** correctly gated — it sits inside the
`_yd is not None` branch. That half is right.) 16 of the 37 `injured=Y` rows have no season of 10+
games. **Materiality not quantified** — it would need another build line.

## F8 · LOW · THE R3 INJURED EXEMPTION IS NOT INDEPENDENT OF A SEPARATE DIAL

`o41_injured()` returns `False` whenever `RL_O41_INJ` is unset. So a build with `RL_O41_R3=1` and
`RL_O41_INJ` off silently loses R3's injured exemption entirely. Not reachable on the candidate
(both dials are on), but the two-channel law is stated as a property of R3 and is not one.

## F9 · LOW · THE PLAYER PAGE'S PROSE DESCRIBES A COLUMN THAT IS EMPTY

`ASSEMBLY_PLAYERS.html` says *"The mechanism legs show how each price is actually made: the production
leg is what he has shown…"*. The **production leg** and **absence take** columns are empty for all
804 rows. The packet declares this honestly (§11: *"present and empty rather than guessed"*). The
page the owner opens does not.

## F10 · INFO · THE CLASS ARTIFACT WAS NOT RE-RUN AFTER THE R3 FIX — BUT THE NUMBER IS RIGHT

`CLASS_ASM_out.txt` / `CLASS_S.json` were last written at `68106d6`, on the superseded board. Neither
`93f001f`, `e3e0ea8` nor `4ae7246` regenerated them, so v753's claim that the class is "unchanged"
rested on an artifact computed elsewhere.

**I re-derived it and it holds.** See A4 below — 1.0671 exactly, on the candidate's own post-fix
matrix, with an instrument validated against ORDER K's and ORDER P's published marks first. No
correction is needed; the check simply had not been re-earned.

---

# PART 2 — THE CLEAN PASSES, AND HOW EACH WAS EARNED

## A · THE BOARD

**A1 · THE CANDIDATE REPRODUCES BYTE-EXACT, TWICE.** Built on this seat's own worktree from the
tracked engine with the documented dial stack, `bbASM.sh` staging verbatim:

```
fbf61d052d6cd77e73f9338e17113eb6   run 1   day-0 89 of 89
fbf61d052d6cd77e73f9338e17113eb6   run 2   day-0 89 of 89     <- determinism, independently
fbf61d052d6cd77e73f9338e17113eb6   run 3   (after fba1a7f landed — the new dial does not disturb it)
```

**A2 · THE DIAL-OFF AND REFERENCE IDENTITIES HOLD.**

```
374d4e442665771801c5f1edd2a7e0e2   every assembly dial off   = ORDER P      OK
374d4e442665771801c5f1edd2a7e0e2   again, after fba1a7f                     OK
7f88f5096ff5b781da4614b7142d332c   A + B1 + p20 clip         = R / R20A     OK
```

**A3 · DAY-0.** The 89 frozen day-0 rows are **bit-identical across the whole chain** — ORDER P, R,
the pre-R3 board and the candidate all match ORDER K's `DAY0_K.json` on every one of the 89, and all
89 are gameless in the store. The walk-forward emit's replication guard is **fail-closed** (it
`raise SystemExit`s on any mismatch), is deliberately pointed at the frozen ORDER K reference rather
than re-based, and I re-read its result from its own output: *"89 of 89 wired entrants … reproduce
printed day-0 EXACTLY (tolerance 0, on the printed integer AND the unrounded derived_v0)"*.

**A4 · THE ACCEPTANCE SUITE, FROM RAW OUTPUTS.**

- **Class 1.0671 — RE-DERIVED, NOT TRUSTED.** I wrote the estimand from the register's words, then
  validated it: ORDER K **1.0513** (published 1.0513) and cohort clock **1.0324** (published 1.0324);
  ORDER P **1.0613** (published 1.0613). Only then, on the candidate's own post-fix matrix:
  **W2 = 1.0671**, cohort clock **1.0423**, 11 of 11 classes averaged, inside [1.03, 1.14). The three
  named breaches reproduce exactly: **2011 1.1671 · 2012 1.1581 · 2016 1.1737 (max)**.
- **Burn census 0** — every band, both populations (264 and 289 rows), zero burned, zero points.
- **Birthday census 0** — 0 gain-50+, **0 movers**, worst ratio 1.0000, all six bands.
- **No row above uncharged** — `S-S2` is a module-scope `raise SystemExit`; the build cannot complete
  with it failing.
- **Continuity** — clean on every axis including 23/24 and the season turn.
- **LAMBDA untouched** — `RL_O40_LAMBDA` never set, `O40_LAMBDA` falls back to
  `O37_LAMBDA = 0.1743833036575403`.
- **Declared honestly by the seat, and I confirm it is declared:** the burn and birthday censuses run
  on the **R3-off** line, and the packet says so in plain words with a "NOT COVERED, said plainly"
  paragraph. That is a disclosure, not a hidden gap.

## B · THE MECHANISMS AS WIRED vs AS RULED

**B1 · R3 — three of four tests pass outright.** From the store, independently:

| test | result |
|---|---|
| no row that **played in 2026** may be charged (the defect v752 caught) | **0 violations — PASS** |
| no **injured-annotated** row may be charged | **0 violations — PASS** |
| **continuous-since-draft** rows must be uncharged | **0 of 409 — PASS** |
| every charged row must have a consecutive absent season | **3 exceptions — see F2** |

Named exhibits reproduce: a row with 16 games this season takes **0**; the genuinely-absent exhibits
take **−606** and **−252**; an 8-game returner takes **0**.

**B2 · THE CREDIT CURVE.** All **12** guarded knots match `FOLLOWUP_F1.json::iso` **exactly**
(bit-for-bit on the repr). Wired at **both** declared sites — `o31_played_units` (line 4022) and the
post-delivery credit loop in `o31_cu` (line 4057) — which is the deviation the prereg declared in
advance. The `raw` variant is a genuine running maximum over F1's own cells, with the one non-cell
number (the 1.0 cap at g=9) disclosed as structural.

**B3 · THE COMPRESSION.** p15 + slope 0.105. `LAMBDA·THETA_R == BETA_sat` and the TMAX recomputation
are asserted at module scope four times (R9, R10, S-F1, S-F2). **The F4 swap is ABSENT** — the
constants `0.21432976…` / `0.10522475…` do not appear anywhere in the file, and the wired 31-F row
**`3: 0.2747857941376827`, `4: 0.39727085107749216`** is intact at lines 3491-3495.

**B4 · THE MATURE REFIT BLENDS BY SEASON-AGE.** `(_x['year'] - _by) >= O37_AGE_GATE` — the age the
season was *played at*, evaluated per season, at both the surplus and the decomposition sites. A
birthday reclassifies nothing. Confirmed empirically by the birthday census's 0 movers.

**B5 · SD OFFSET AND RECENCY.** The SD offset appears at exactly two sites (4509, 4631), each gated
`if _pos=='SD'` — **SF and RUCK are untouched**. Both sites are load-bearing and the code documents
why (a board built with only the first was byte-identical to no-dial; the seat reports it as a caught
defect). Recency `w**(Y - season year)` appears at the matching two sites and nowhere else.

**B6 · THE INJURY STREAM.** md5 `b26798c3…` re-read here and matching; 219 rows; 37 `injured=Y`; all
37 match — and **no annotation name matches more than one store row**, which I checked because 13
display names are shared in the store. The pause is the live year's fraction only and sits inside the
delivered-row branch. The lever moves **2 rows**, and `A-F16` fired on one downward — which the
packet reports and explains as the mechanical corollary of the owner's kept depth-4 rise.

## C · THE DOCUMENTS vs THE DATA

**C1 · THE TRACKER — CLEAN.** All **801** CSV rows checked against the boards' own JSON: **0**
mismatches across the five value columns **and 0 across all six delta columns**. The HTML carries all
six delta columns (`Δ live→K, Δ K→P, Δ P→R, Δ R→cand, Δ live→cand, Δ K→cand`) and 801 data rows. All
five board totals correct in the header. **The row filter is exactly right**: 801 = 804 minus the 3
rows identical on all five boards.

**C2 · THE PER-LEVER PAGE — TELESCOPES EXACTLY.**

```
R (7f88f509)        664,950
sum of 9 marginals     +230
                    -------
                    665,180  ==  candidate fbf61d05   EXACT
```

Every cell of the page — total, marginal, rows moved, up, down — matches my re-derivation on all ten
rows. Named movers for two levers re-derived straight from the lever boards' JSON and reproduce.

**C3 · THE YEAR-1 PAGE — THE COHORT DEFECT IS GENUINELY FIXED.** Re-run independently on the
engine's own clock: **105 rows, 0 whose cohort is not 2026**, and **0 cohort-2026 board rows missing
from the page** — both directions. All **18** MSD rows are draft-year 2026. `v0` populated on every
row; **no dead columns**.

**C4 · THE NO-ARB PAGE — VERDICTS RECOMPUTED.** All **11** published path-test verdicts recomputed
from the year paths and the carry rail: **0 mismatches** on `limb_a`, `limb_b`, `both` and the
beat-years list. The rail is a genuine compounding 14% (`1.14^k` reproduces the wired table). Five
boards, both windows, all nine arm types present on the page, **0 breaching cells unscored**, MSD
exclusion note present.

**C5 · THE PLAYER LIST — 804 rows.** Mechanism legs present or honestly empty (see F9 for the prose).

**C6 · THE 77-CHECK LIST — RE-RUN INDEPENDENTLY: 77/77.** The three non-mechanical items are real
caveats, not hand-waves — prose accuracy, no named-player targets, depths quoted as depths are
genuinely not machine-checkable. **But the first of them is exactly the check that would have caught
F1 and F4.** It was correctly named and evidently not performed.

## D · THE FRACTIONAL RUN-BREAK VARIANT (`fba1a7f`, landed mid-audit)

**Every number in that commit reproduces on my own rebuilds.** This is the most honest artefact in
the delivery.

```
2eac9bc79b27c5c184151b9aa0d9bdfc   fractional, run 1
2eac9bc79b27c5c184151b9aa0d9bdfc   fractional, run 2   (determinism)
fbf61d052d6cd77e73f9338e17113eb6   break dial unset    (the candidate is undisturbed)
374d4e442665771801c5f1edd2a7e0e2   all dials off
```

| claim | published | mine |
|---|---:|---:|
| fractional total | 649,412 | **649,412** |
| R3 marginal, fractional | −16,851 on 121 rows | **−16,851 on 121** |
| fractional vs binary | −15,768 on 110 rows, all down | **−15,768 on 110, all down** |
| shield population | 63 rows | **63** |
| shield take, binary / fractional | 356 / 3,813 | **356 / 3,813** |
| **share landing OUTSIDE the shield** | **78%** | **78%** |

Day-0 holds (89/89, 0 gameless rows move). The named-row comparison holds. **The self-criticism in
that commit message is accurate**: the rule does close the shield, and 78% of what it does lands
outside the population it was built for. One claim I initially flagged as not reproducing turned out
to be my own error — the packet's "Visentini" is a different player from the one I looked up, and the
packet is right.

---

# PART 3 — THE LTI CROSS-TABULATION (evidence for F2 and F3)

The twelve rows R3 charges on the candidate, against both injury records:

| take | on `LTI_REGISTER.md` | `injured=Y` in the owner annotation |
|---:|---|---|
| −606 | **YES (A)** | no |
| −252 | no | no |
| −57 | no | no |
| −36 | **YES (A)** | no |
| −33 | no | no |
| −26 | no | no |
| −24 | no | no |
| −15 | **YES (A)** | no |
| −14 | no | no |
| −10 | no | no |
| −7 | **YES (B)** | no |
| −3 | no | no |
| **−1,083** | **4 rows, −664 (61%)** | **0** |

Of the 41 rows whose only unplayed season is 2026: 3 charged, **all 3 on the LTI register**; 38
uncharged, of which 11 are on the LTI register **and** `injured=Y` (so exempt).

---

# PART 4 — WHAT I COULD NOT VERIFY, AND WHY

1. **The materiality of F7** (annotation read for never-delivered rows). Establishing what those rows
   would otherwise pay needs a further build line this seat did not run.
2. **The burn sweep through the R3 term.** Structurally uncoverable by the existing instrument — the
   burn identity has no absence-collector term. **The packet declares this itself**; I confirm the
   declaration is accurate rather than closing the gap.
3. **Whether the owner intends the LTI-registered rows to be charged.** F2/F3 are findings about the
   mechanism and its documentation. Whether the resulting prices are the wanted ones is an owner
   question, and at least one of those rows he has said he wants stripped.
4. **The three MANUAL items on the 77-check list** are by construction not machine-checkable. I
   checked two of them by hand against the pages and they hold (no player is used as a target; depths
   are quoted as depths). The third — prose accurate and current — **fails**, which is F1 and F4.

---

# PART 5 — THE FILES IN THIS PACKET

| file | what it is |
|---|---|
| `aud_build.sh` / `aud_build2.sh` | the eight rebuilds — staging copied from `bbASM.sh`, strictly sequential, thread-pinned |
| `AUD_BUILDS_out.txt` / `AUD_BUILDS2_out.txt` | their raw output, every md5 and every day-0 assert |
| `aud_docs.py` / `AUD_DOCS_out.txt` | C1 and C2 — tracker rows and deltas, lever telescoping, named movers |
| `aud_r3.py` / `AUD_R3_out.txt` | B1 — the R3 rule re-derived from the store, six tests |
| `aud_class.py` / `AUD_CLASS_out.txt` | A4 — the class mark re-derived, instrument validated first |
| `aud_noarb.py` / `AUD_NOARB_out.txt` | C4 — path-test verdicts recomputed from the paths and the rail |

**Conventions kept:** plain speech · no named-player targets (rows are cited as consequences, by
store key or by take, never as things to hit) · nulls as nulls · thread pins printed per run · every
number here re-derived rather than copied from a document under audit.

**NOTHING WAS FIXED, ADOPTED OR MERGED BY THIS SEAT. NO ENGINE FILE WAS EDITED. THE LIVE BOARD
`88ce647f` WAS NOT TOUCHED.**
