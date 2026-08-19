# PACKET — D6-CONSOLIDATION (register v760): THE INJURY CONSOLIDATION

**Branch `land/order-29`. Base `55f4dd3`. Prereg `bd365f9`, pushed BEFORE the engine edit. Engine edit
`307123c`.**

> ## THE BOARD IS **PRICED, NOT ADOPTED.**
> Nothing here is adopted, merged, tagged or promoted. Those are owner-only acts. Nothing is on `main`.

---

## 1 · THE HEADLINE, INCLUDING THE PARTS THAT GO AGAINST THIS SEAT

**THE PRICED BOARD IS `daa16812`, TOTAL 660,578 ON 804 ROWS.** Against the owner-ruled D5-final base
`ff936186` / 659,222 that is **+1,356 across 31 movers, and every mover is inside the affected set.**

**THREE THINGS FIRED OR HALTED AND ALL THREE ARE REPORTED FIRST, NOT BURIED:**

1. **Falsifier D6-F8 FIRED on the first candidate build — and the falsifier was WRONG, not the
   re-base.** The prereg claimed the 18-rebase "may only ever RAISE the haircut". That is
   arithmetically backwards. Full account in §6.
2. **Guard 5 is RED on this branch and this order does NOT claim it green.** It was red before this
   seat existed. §2.
3. **The RL_AVAIL=0 control board could not be built at all** — a frozen-v0surf HALT. That path was
   abandoned rather than worked around, and the combined take is measured a better way. §7.

**THE BRIEF'S "21 REGISTER-ONLY ROWS" IS 20 ON MEASUREMENT.** Reported as measured. §5.

**CONWAY IS INTACT. `460 → 460`, delta exactly 0.** §8.

---

## 2 · GUARD 5 — RED, PRE-EXISTING, AND NOT CLAIMED GREEN

The brief requires Guard 5 PASS before any pricing run. **It does not pass on `land/order-29`.**
`bash run_panel.sh` exits 1; its own named remedy `bash bootstrap.sh` also exits 1. Five complaints
survive the remedy:

| # | complaint | this seat's? |
|---|---|---|
| 1 | checkout `rl_model.py` `98f16794` != pinned `14000af2` | no |
| 2 | `v0surf` load-path resolves to `/home/claude/v0surf.pkl` `fbc5b393` != pinned `5dd34ca8` | no |
| 3 | workspace engine != pinned `engine_head` `a353a9d3` | no |
| 4 | `fv` CHECKOUT DRIFT — `engine/forward_valuation` identity != pin | no |
| 5 | `fv` LOADED-PATH DRIFT — same identity, same cause | no |

ORDER P disclosed the same condition at `bc63d5d`. **Per the brief's own instruction that path is
HALTED, not improvised around: Guard 5 is carried as RED / PRE-EXISTING and is never scored as a
pass.**

**What is true instead.** Every board here is built through `bbD6.sh`, which pins the engine, the
forward-valuation tree, the store, the five thread variables and `RL_V0SURF_PKL` explicitly and prints
their md5s on every run. Complaint 2 does not touch a build: the harness sets
`RL_V0SURF_PKL="$ROOT/data/v0surf.pkl"`, and that file **is** the pinned `5dd34ca8`. The base board
reproduced byte-exact under exactly this harness.

**If the supervisor's charter requires a green Guard 5, this order cannot satisfy it, and the re-pin
is a landing act outside this seat.**

Raw: `GUARD5_run_panel_out.txt`, `GUARD5_bootstrap_out.txt`.

---

## 3 · THE BOARDS

| board | md5 | total | vs base | what it is |
|---|---|---:|---:|---|
| `D6_IDENT_P` | `374d4e44` | — | — | every `RL_O38*/O39/O40/O41/O42` dial OFF = the ORDER P identity |
| `D6_IDENT_K` | `f3101883` | — | — | ORDER K's ruled line = the K chain |
| `D6_L0R` | `7f88f509` | — | — | R20A, the owner's reference |
| **`D6_BASE`** | **`ff936186`** | **659,222** | — | the D5-final stack, `RL_O42` UNSET — **THE BASE** |
| **`D6_CAND`** | **`daa16812`** | **660,578** | **+1,356** | **+ `RL_O42=1` — THE CONSOLIDATION** |
| `D6_CAND2` | `daa16812` | 660,578 | +1,356 | determinism repeat |
| `D6_OFF` | **NO BOARD** | — | — | `RL_AVAIL=0` control — **HALTED, see §7** |

**The base reproduced byte-exact as the first pricing act, before the prereg was written** —
`ff936186` / 659,222 on 804 rows, day-0 89 of 89 (`BASE_REPRO_out.txt`).

Pinned inputs on every run: store `cb38ef11` (pin `cb38ef11`), v0surf `5dd34ca8` (pin `5dd34ca8`),
sheet `b26798c35adcd9bda5cef50ff2c884da` (pinned prefix `b26798c35adcd9bd` — **ASSERT PASSES**).

Raw: `BUILD_D6_out.txt`, `BUILD_D6_CAND_out.txt`, `BUILD_D6_FINAL_IDENT_out.txt`.

---

## 4 · PER-SITE DISPOSITION OF THE FOUR CONSUMPTION SITES

All four sites read **one** object, `_AVAIL_STATE`. Re-keying its source moves all four together, so
**not one of the four sites was edited.** Under `RL_O42=1`, `lti_register.build_state()` — the single
live read of `LTI_REGISTER.md` — **is not called at all.**

| # | site | verified lines | disposition | evidence it took effect |
|---|---|---|---|---|
| 1 | `_fe_p_one` / `_fEy` — the `fE=1.0` LTI override (behind audit F2's one-season-out leak) | 127-132 | **RE-KEYED** — `out` now comes from the sheet | 43 dispositions → 37, membership changed |
| 2 | KPF fork-v — the 2026-exclusion / nuked season | 1207-1208 | **RE-KEYED** — only annotated rows nuke 2026 | Ollie Murphy (§9) moves +4 through exactly this path |
| 3 | L1c clock advance `g += L*cp.SEASON` | 1414-1415 | **RE-KEYED** — sheet membership, re-based `L`; `cp.SEASON` at this site **untouched** | 9 rows' `L` moves (§6) |
| 4a | `_AVAIL_STATE` population | 5688-5752 | **RE-KEYED to the sheet** | section `A`×32 + `B`×11 → `S`×37 |
| 4b | the Part-2 return arm (`lti_return_table`) | 5705-5715, 1303 | **RETIRED** — no sheet analogue for section A/B | `return_arm` 32 → 0, `ret_hc>0` 6 → 0 |

Measured on the boards themselves:

| | `D6_BASE` | `D6_CAND` |
|---|---|---|
| rows carrying a disposition | **43** | **37** |
| sections | `A`×32, `B`×11 | **`S`×37** |
| designations | `2026`×23, `2026_preseason`×12, `2025`×6, `2025+2026`×2 | **`sheet_v1`×37** |
| `return_arm` true | 32 | **0** |
| rows with `ret_hc > 0` | 6 | **0** |

**D6-F6 — any register-only key still carrying a live disposition on the candidate: 0. Did not
fire.** The register has no live consumption on this lane.

### 4b · THE PART-2 RETIREMENT, PRICED SEPARATELY RATHER THAN ABSORBED

The return arm is gated on `section == 'A'`. **`section` is register-only information with no
analogue anywhere on the sheet.** Defaulting all 37 annotated rows to Section A would have INVENTED
section membership for the 14 rows the register never listed. **This seat does not invent an owner
input**, so the arm is retired and priced on its own line:

| | Part 1 | Part 2 | combined |
|---|---:|---:|---:|
| `D6_BASE` (43 rows) | −5,953 | **−28** | −5,981 |
| `D6_CAND` (37 rows) | −4,670 | **0** | −4,670 |

**Retiring the Part-2 return arm is worth 28 board points across 3 rows** (Esava Ratugolea −15, Jack
Payne −11, Brayden Fiorini −2). It is small, but it is a deletion of a priced component and the owner
should rule on it on its own merits rather than have it folded into a +1,356 total.

**Reconciliation, stated rather than glossed:** the attribution deltas above are computed at `ev()`
resolution; the board total moves +1,356 while the attribution difference is +1,311. The 45-point gap
is board rounding. **They are different objects and both are printed; neither is claimed to equal the
other.**

---

## 5 · MEMBERSHIP — AND A CORRECTION TO THE BRIEF

Membership is **the 37 annotated `injured=Y` rows ONLY**, resolved through the engine's own existing
name normaliser. All 37 resolve to exactly one store row each; zero misses, zero ambiguities. The
`max-king` collision resolves correctly and the two are distinct annotated rows — `Max King` →
`max-king-stk`, `Maxwell King` → `max-king-syd`.

| set | count |
|---|---:|
| annotated `injured=Y` | **37** |
| register unique keys (45 rows; `reef-mcinnes` has two windows) | **43** |
| register **AND** annotated — treatment continues, re-based | **23** |
| **register-only — LOSING treatment** | **20** |
| annotated, never on the register — **GAINING** treatment | **14** |

> **THE BRIEF SAYS 21 REGISTER-ONLY ROWS. THE MEASURED NUMBER IS 20.**
> 43 = 23 + 20, and all 43 register keys currently have `out=True`, so there is no untreated residue
> that could account for the difference. **Reported as measured, not as briefed.**

The **14 gaining** treatment are a real consequence of the ruling and are not suppressed — the sheet
is the only injury truth, so an annotated row the old register never listed becomes injured:

`Elliott Himmelberg −13 · Harry Armstrong −38 · Henry Smith −5 · Kobe McDonald −2 · Max King −40 ·
Mitchell Hinge −114 · Ollie Murphy +4 · Ricky Mentha 0 · Riley Garcia −11 · Rob Monahan 0 ·
Sam Allen −22 · Sam Powell-Pepper −80 · Sam Sturt 0 · Thomas Sims −61`

---

## 6 · THE 18-REBASE, THE `:5698` ASSERT, AND THE FALSIFIER THAT FIRED ON THIS SEAT

### 6a · WHAT HAPPENED TO THE ASSERT — THE ANTICIPATED DISCLOSURE, DISCHARGED

`_merged_recover.py:5698` asserts `LTIREG.G_FULL == cp.SEASON` (22 == 22). The brief anticipated that
an 18-rebase would break it by construction.

**IT DID NOT, BECAUSE THE 18 WAS NEVER PUT WHERE IT WOULD:**

- **`cp.SEASON` is NOT touched.** Still 22.
- **`lti_register.G_FULL` is NOT touched.** Still 22.
- **The assert at `:5698` is NOT touched, NOT weakened, NOT made conditional.** It is still
  unconditional and **it passed on every board in this order, dial on and dial off.** Measured on the
  candidate line: `LTIREG.G_FULL=22  cp.SEASON=22`.
- The 18 lives in its own separately named constant **`_O42_AVAIL_BASE = 18`** — the AVAILABILITY
  base, i.e. how much of a season a player is expected to be available for. **Nothing is asserted
  equal to it.** The engine still keeps exactly one season constant and it is still 22.
- A **new** dial-on guard rejects any later attempt to collapse the two:
  `_O42_AVAIL_BASE != 18 or _O42_AVAIL_BASE == cp.SEASON` ⇒ `ORDER 42 HALT`.

### 6b · **D6-F8 FIRED, AND THE HONEST READING IS THAT MY FALSIFIER WAS WRONG**

The first `RL_O42=1` build **HALTED on this order's own guard**:

```
ORDER 42 HALT: andy-moniz-wakefield — the re-base is not the stated form
(g=2 L22=0.909091 L18=0.888889). It may only ever RAISE the haircut, and
must clear to exactly zero at the availability base.
```

**THE DIAGNOSIS GOES AGAINST THIS SEAT.** The prereg (§8, D6-F8) asserted the re-base "may only ever
RAISE the haircut". **That is arithmetically backwards.** Against a SHORTER season the same games are
a LARGER fraction of it, so `g/18 > g/22` and therefore `L₁₈ ≤ L₂₂`.

**THE RE-BASE ITSELF IS EXACTLY WHAT WAS BRIEFED AND PREREGISTERED** — `L₁₈ = 1 − min(g/18, 1)` —
and **not one constant was moved to make the guard pass.** What was corrected is the guard's claim
about the direction of the form it guards. The corrected D6-F8 checks the invariant the form actually
has (range, direction, clears-at-base, `g=0 ⇒ L=1`) and **still HALTS on violation** — it was not
removed, weakened to a warning, or made conditional. It now reads **0 violations**.

`PREREG_D6.md §11` records the fire as an amendment rather than editing §8 silently.

### 6c · THE SUBSTANTIVE RESULT — AND IT IS THE OPPOSITE OF WHAT THE PREREG EXPECTED

> **RE-BASING TO THE OWNER'S 18-GAME AVAILABILITY SEASON MAKES AN INJURED ROW WHO PLAYED SOME GAMES
> IN 2026 *LESS* PENALISED, NOT MORE.**

A row with zero 2026 games is untouched (`L = 1` on both bases). **Only 9 of the 37 annotated rows
have `0 < g < 18` and therefore move at all**, and every one moves DOWNWARD in haircut:

| row | g₂₀₂₆ | L₂₂ | L₁₈ | Δ |
|---|---:|---:|---:|---:|
| Harry Armstrong | 3 | 0.8636 | 0.8333 | −0.0303 |
| Andy Moniz-Wakefield | 2 | 0.9091 | 0.8889 | −0.0202 |
| Brayden Fiorini | 2 | 0.9091 | 0.8889 | −0.0202 |
| Connor Rozee | 2 | 0.9091 | 0.8889 | −0.0202 |
| Harry Edwards | 2 | 0.9091 | 0.8889 | −0.0202 |
| Josh Gibcus | 1 | 0.9545 | 0.9444 | −0.0101 |
| Judson Clarke | 1 | 0.9545 | 0.9444 | −0.0101 |
| Mitchell Hinge | 1 | 0.9545 | 0.9444 | −0.0101 |
| Ollie Lord | 1 | 0.9545 | 0.9444 | −0.0101 |

The other 28 annotated rows have `g = 0` and sit at `L = 1` on both bases.

**`g` stays the STORE's 2026 games**, honouring the register's own rule that the store is the single
source of production (spec §3.3). **The sheet's `games_2026` column and the store agree on 37 of 37
annotated rows — zero disagreements**, and that agreement is asserted at build time (D6-F7 did not
fire).

---

## 7 · THE R1 COMBINED-TAKE GUARD

### 7a · A SECOND HALT, REPORTED RATHER THAN WORKED AROUND

The preregistered method was a layer-off control board (`RL_AVAIL=0`) with
`take = v(board) − v(control)`. **That board cannot be built:**

```
v0surf FROZEN-SIGNATURE HALT: this build's config signature 3ebc60f0 is NOT in
data/v0surf.pkl (frozen: 41af7326, 4405cba2). The engine will NOT silently re-fit
the V0 pick-curve surface.
```

`RL_AVAIL` is part of the frozen config signature and only `RL_AVAIL=1` signatures are frozen. A
refit is a **bake act, outside this seat**, and would make the control non-comparable anyway. **The
path was abandoned.**

**What replaced it is strictly better.** The engine ALREADY computes this attribution in-process at
the availability block: `_ev_off` (layer off) → `_ev_p1` (+ Part 1) → `_vfull` (+ Part 2), recorded
per row in `_AVAIL_MOVERS`. That is the whole take against the engine's own layer-off baseline, with
no second board and no frozen-surface problem. `d6_take.py` reads it out on each dial line.

### 7b · THE 37 ANNOTATED ROWS — take on the CANDIDATE

| player | g₂₆ | L₂₂ | L₁₈ | P1 | P2 | TAKE | v_base | v_cand | Δ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Tom Green | 0 | 1.0000 | 1.0000 | −1275 | 0 | **−1275** | 4339 | 4339 | +0 |
| Nicholas Martin | 0 | 1.0000 | 1.0000 | −1020 | 0 | **−1020** | 3199 | 3199 | +0 |
| Connor Rozee | 2 | 0.9091 | 0.8889 | −864 | 0 | **−864** | 2559 | 2559 | +0 |
| Joshua Kelly | 0 | 1.0000 | 1.0000 | −360 | 0 | **−360** | 427 | 427 | +0 |
| Jack Viney | 0 | 1.0000 | 1.0000 | −321 | 0 | **−321** | 254 | 254 | +0 |
| Brayden Fiorini | 2 | 0.9091 | 0.8889 | −175 | 0 | **−175** | 180 | 182 | +2 |
| Mitchell Hinge | 1 | 0.9545 | 0.9444 | −114 | 0 | **−114** | 303 | 194 | −109 |
| Darcy Jones | 0 | 1.0000 | 1.0000 | −106 | 0 | **−106** | 1095 | 1095 | +0 |
| Harry O'Farrell | 0 | 1.0000 | 1.0000 | −88 | 0 | **−88** | 537 | 537 | +0 |
| Sam Powell-Pepper | 0 | 1.0000 | 1.0000 | −80 | 0 | **−80** | 173 | 97 | −76 |
| Thomas Sims | 0 | 1.0000 | 1.0000 | −61 | 0 | **−61** | 737 | 670 | −67 |
| Max King | 0 | 1.0000 | 1.0000 | −40 | 0 | **−40** | 248 | 209 | −39 |
| Harry Armstrong | 3 | 0.8636 | 0.8333 | −38 | 0 | **−38** | 518 | 475 | −43 |
| Harley Barker | 0 | 1.0000 | 1.0000 | −23 | 0 | **−23** | 481 | 481 | +0 |
| Sam Allen | 0 | 1.0000 | 1.0000 | −22 | 0 | **−22** | 450 | 428 | −22 |
| Harry Edwards | 2 | 0.9091 | 0.8889 | −18 | 0 | **−18** | 89 | 89 | +0 |
| Elliott Himmelberg | 0 | 1.0000 | 1.0000 | −13 | 0 | **−13** | 43 | 31 | −12 |
| Riley Garcia | 0 | 1.0000 | 1.0000 | −11 | 0 | **−11** | 50 | 40 | −10 |
| Blake Thredgold | 0 | 1.0000 | 1.0000 | −9 | 0 | **−9** | 372 | 372 | +0 |
| Maxwell King | 0 | 1.0000 | 1.0000 | −8 | 0 | **−8** | 129 | 129 | +0 |
| Josh Gibcus | 1 | 0.9545 | 0.9444 | −6 | 0 | **−6** | 176 | 176 | +0 |
| Henry Smith | 0 | 1.0000 | 1.0000 | −5 | 0 | **−5** | 90 | 85 | −5 |
| Jesse Motlop | 0 | 1.0000 | 1.0000 | −3 | 0 | **−3** | 54 | 54 | +0 |
| Lewis Hayes | 0 | 1.0000 | 1.0000 | −3 | 0 | **−3** | 338 | 338 | +0 |
| Liam Hetherton | 0 | 1.0000 | 1.0000 | −3 | 0 | **−3** | 66 | 66 | +0 |
| Josh Sinn | 0 | 1.0000 | 1.0000 | −2 | 0 | **−2** | 159 | 159 | +0 |
| Kobe McDonald | 0 | 1.0000 | 1.0000 | −2 | 0 | **−2** | 40 | 37 | −3 |
| Noah Chamberlain | 0 | 1.0000 | 1.0000 | −2 | 0 | **−2** | 37 | 37 | +0 |
| Ollie Lord | 1 | 0.9545 | 0.9444 | −1 | 0 | **−1** | 74 | 74 | +0 |
| Reef McInnes | 0 | 1.0000 | 1.0000 | −1 | 0 | **−1** | 50 | 50 | +0 |
| Andy Moniz-Wakefield | 2 | 0.9091 | 0.8889 | 0 | 0 | **0** | 38 | 38 | +0 |
| Judson Clarke | 1 | 0.9545 | 0.9444 | 0 | 0 | **0** | 55 | 55 | +0 |
| Nathan Wardius | 0 | 1.0000 | 1.0000 | 0 | 0 | **0** | 37 | 37 | +0 |
| Ricky Mentha | 0 | 1.0000 | 1.0000 | 0 | 0 | **0** | 23 | 23 | +0 |
| Rob Monahan | 0 | 1.0000 | 1.0000 | 0 | 0 | **0** | 37 | 37 | +0 |
| Sam Sturt | 0 | 1.0000 | 1.0000 | 0 | 0 | **0** | 31 | 30 | −1 |
| **Ollie Murphy** | 0 | 1.0000 | 1.0000 | **+4** | 0 | **+4** | 196 | 200 | +4 |

**Combined take on these rows: BASE −4,290 → CANDIDATE −4,670 (change −380).**

### 7c · THE 20 REGISTER-ONLY ROWS — LOSING TREATMENT

Take shown **on the base** — what they *were* being charged. **On the candidate every one carries no
disposition and its take is EXACTLY ZERO.**

| player | g₂₆ | L₂₂ | P1 | P2 | TAKE (base) | v_base | v_cand | Δ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Sam Flanders | 12 | 0.4545 | −744 | 0 | **−744** | 1923 | 2631 | **+708** |
| Sam Darcy | 6 | 0.7273 | −592 | 0 | **−592** | 4450 | 5076 | **+626** |
| Esava Ratugolea | 8 | 0.6364 | −47 | −15 | **−62** | 67 | 127 | +60 |
| Jack Payne | 0 | 1.0000 | −50 | −11 | **−61** | 100 | 159 | +59 |
| Deven Robertson | 4 | 0.8182 | −49 | 0 | **−49** | 66 | 113 | +47 |
| Matt Carroll | 10 | 0.5455 | −44 | 0 | **−44** | 619 | 687 | +68 |
| Oscar Steene | 8 | 0.6364 | −44 | 0 | **−44** | 346 | 398 | +52 |
| Jonty Faull | 10 | 0.5455 | −26 | 0 | **−26** | 550 | 580 | +30 |
| Jai Culley | 7 | 0.6818 | −14 | 0 | **−14** | 157 | 175 | +18 |
| Joel Amartey | 15 | 0.3182 | −14 | 0 | **−14** | 37 | 50 | +13 |
| Jamie Elliott | 11 | 0.5000 | −12 | 0 | **−12** | 8 | 21 | +13 |
| Toby Pink | 5 | 0.7727 | −9 | 0 | **−9** | 39 | 48 | +9 |
| Brody Mihocek | 10 | 0.5455 | −8 | 0 | **−8** | 30 | 38 | +8 |
| Ewan Mackinlay | 14 | 0.3636 | −4 | 0 | **−4** | 109 | 115 | +6 |
| Archie May | 10 | 0.5455 | −3 | 0 | **−3** | 337 | 346 | +9 |
| Noah Long | 0 | 1.0000 | −3 | 0 | **−3** | 50 | 55 | +5 |
| Jacob Newton | 3 | 0.8636 | −1 | 0 | **−1** | 183 | 188 | +5 |
| Mani Liddy | 0 | 1.0000 | −1 | 0 | **−1** | 77 | 78 | +1 |
| Jackson Archer | 0 | 1.0000 | 0 | 0 | **0** | 12 | 12 | +0 |
| **Toby Conway** | 0 | 1.0000 | **0** | 0 | **0** | **460** | **460** | **+0** |

**Combined take on these rows: BASE −1,691 → CANDIDATE 0.**

Raw: `D6_TAKE_out.txt`, `D6_TAKE.json`.

---

## 8 · CONWAY — THE OWNER'S STANDING WORD, DISCHARGED

> **"The sheet wins; Conway is NOT injured and is EXPECTED TO KEEP his sitting charges."**

| | |
|---|---|
| sheet | `injured = N` · depth **4.08** · fade 0.346 · delivered never |
| on the old register | **YES** — so he loses LTI treatment under the consolidation |
| LTI take | base **+0** → candidate **+0** |
| **PRICE** | **base 460 → candidate 460 — delta exactly 0** |

**D6-F4 DID NOT FIRE. Conway's charges are intact.**

**Why it costs him nothing, stated as mechanism rather than luck:** the LTI layer was already taking
**zero** from Conway on the base. His `avail_hc` was 1.0, but the haircut multiplies a k=0 present leg
that is empty — 0 games in 2026, last played 2024 — so there was nothing for it to bite. His charge
comes from the **depth/fade machinery at depth 4.08**, which this order does not touch. Retiring his
register treatment therefore removes a haircut that was already worth nothing.

**Conway is a CHECK, not a target. No parameter in this order was chosen to produce any Conway
outcome.**

---

## 9 · MOVERS vs THE BASE `ff936186` — WITH NAMED-ROW COMMENTARY

**31 movers, +1,356 net, and 0 movers outside the 57-key union (37 annotated ∪ 20 register-only).
D6-F9 did not fire — there is no scope leak.**

The two directions are exactly what the ruling implies:

**RISING — register-only rows that stop being charged as injured (16 of 20 move):**

| row | base → cand | Δ | why |
|---|---|---:|---|
| **Sam Flanders** | 1923 → 2631 | **+708** | the largest single move on the board; he was carrying a −744 take on 12 games |
| **Sam Darcy** | 4450 → 5076 | **+626** | −592 take released; the owner did not annotate him injured |
| Matt Carroll | 619 → 687 | +68 | |
| Esava Ratugolea | 67 → 127 | +60 | includes the retired Part-2 arm (−15) |
| Jack Payne | 100 → 159 | +59 | includes the retired Part-2 arm (−11) |
| Oscar Steene | 346 → 398 | +52 | |
| Deven Robertson | 66 → 113 | +47 | |
| Jonty Faull | 550 → 580 | +30 | |
| Jai Culley +18 · Jamie Elliott +13 · Joel Amartey +13 · Archie May +9 · Toby Pink +9 · Brody Mihocek +8 · Ewan Mackinlay +6 · Jacob Newton +5 · Noah Long +5 · Mani Liddy +1 | | | |

**FALLING — annotated rows the register never listed, now injured (11 of 14 move):**

| row | base → cand | Δ |
|---|---|---:|
| **Mitchell Hinge** | 303 → 194 | **−109** |
| **Sam Powell-Pepper** | 173 → 97 | **−76** |
| Thomas Sims | 737 → 670 | −67 |
| Harry Armstrong | 518 → 475 | −43 |
| Max King (`max-king-stk`) | 248 → 209 | −39 |
| Sam Allen | 450 → 428 | −22 |
| Elliott Himmelberg −12 · Riley Garcia −10 · Henry Smith −5 · Kobe McDonald −3 · Sam Sturt −1 | | |

### THE ONE MOVER THAT GOES THE "WRONG" WAY, AND ITS MECHANISM

**Ollie Murphy is newly annotated-injured and his price RISES by +4** (196 → 200; his availability
take is **+4**, positive). This is not a defect and it is not noise: it is **site 2, the KPF fork-v**,
working as designed. Fork-v treats an injured current season as a NUKED season — excluded from the
top-2 demonstration window, with the window extended back year-for-year — so a KPF whose 2026 is weak
can be **helped** by being marked injured, because his demonstrated level then rests on his healthier
seasons. **The injury stream raising an injured row is a known property of this engine and was
reported by the assembly seat on the same mechanism (Max King +3).** Reported here rather than
smoothed over.

**Brayden Fiorini +2** is the only row in BOTH sets: he keeps treatment, and his `L` falls from
0.9091 to 0.8889 under the 18-rebase (§6c), so he rises slightly. That is the re-base, visible in
isolation on a single row.

---

## 10 · ACCEPTANCE SUITE

| item | required | measured | verdict |
|---|---|---|---|
| dial-off → `ff936186` byte-exact | `ff936186` | **`ff936186`** | **PASS** — D6-F1 did not fire |
| every-O41-dial-off → `374d4e44` | `374d4e44` | **`374d4e44`** | **PASS** — D6-F2 did not fire |
| chain to `f3101883` / `7f88f509` | both | **`f3101883` / `7f88f509`** | **PASS** |
| determinism ×2 | identical | **`daa16812` == `daa16812`** | **PASS** — D6-F3 did not fire |
| day-0 89/89 | 89 of 89 | **89 of 89 on every board built** | **PASS** |
| burn 0 | 0 | see §10b | see §10b |
| class 1.0671 (registered W2 basis) | 1.0671 | see §10b | see §10b |
| tail 0.8004 | 0.8004 | see §10b | see §10b |
| birthday probe +0 (R3-aware) | +0 | see §10b | see §10b |
| the 79/79 suite | 79/79 | see §10b | see §10b |
| **Guard 5** | PASS | **RED, PRE-EXISTING** | **NOT CLAIMED GREEN — §2** |

Additional checks this order added and ran:

| id | check | result |
|---|---|---|
| D6-F4 | Conway's sitting charges survive | **did not fire** — 460 → 460 |
| D6-F5 | membership resolves to exactly 37, one store row each | **did not fire** |
| D6-F6 | no register-only key retains a live disposition | **did not fire** — 0 |
| D6-F7 | sheet `games_2026` == store 2026 games on every annotated row | **did not fire** — 37/37 agree |
| D6-F8 | the re-base form | **FIRED as preregistered — the falsifier was wrong, §6b. 0 violations against the corrected invariant.** |
| D6-F9 | no mover outside the 57-key union | **did not fire** — 0 outside |
| D6-F10 | `cp.SEASON`=22, `G_FULL`==`cp.SEASON`, `:5698` assert unweakened | **did not fire** — 22 == 22 on every board |
| — | `RL_O42=1` with `RL_AVAIL=0` must HALT, not silently no-op | **HALTS correctly** (`ORDER 42 HALT`) |

---

## 11 · WHAT THIS ORDER DID **NOT** DO

Stated plainly so nothing is read as done that was not:

- **Guard 5 was not made to pass.** It is red, pre-existing, disclosed (§2).
- **The `RL_AVAIL=0` control board was not built.** Frozen-v0surf halt; path abandoned (§7a).
- **`LTI_REGISTER.md` was not deleted.** It stays in the tree and stays seeded by `bootstrap.sh`.
  What is retired is its LIVE CONSUMPTION on the `RL_O42=1` lane.
- **Nothing was adopted, merged, tagged or promoted, and nothing is on `main`.**

---

## 12 · FILES

| file | what |
|---|---|
| `PREREG_D6.md` | the prereg, pushed at `bd365f9` before the engine edit; §11 is the D6-F8 amendment |
| `PACKET_D6.md` | this packet |
| `bbD6.sh` | the board harness (assembly's `bbASM.sh` + `RL_O42`, `RL_AVAIL` pass-through) |
| `build_D6.sh` | identities, base, candidate, determinism repeat |
| `build_D6_cand.sh` | candidate rebuild after the D6-F8 fire, + controls + the guard exercise |
| `build_D6_final_ident.sh` | identities re-priced on the FINAL committed engine |
| `d6_take.py` | the R1 combined-take guard, from the engine's own attribution |
| `BASE_REPRO_out.txt` | the base reproducing `ff936186` before the prereg was written |
| `BUILD_D6_out.txt` | identities + base + the D6-F8 HALT, raw |
| `BUILD_D6_CAND_out.txt` | candidate, determinism, the frozen-v0surf halt, the ORDER 42 guard halt |
| `BUILD_D6_FINAL_IDENT_out.txt` | identities on the final engine |
| `D6_TAKE_out.txt` / `D6_TAKE.json` | the R1 per-row tables and falsifier scoring |
| `GUARD5_run_panel_out.txt` / `GUARD5_bootstrap_out.txt` | Guard 5 red, and red again after its own remedy |
