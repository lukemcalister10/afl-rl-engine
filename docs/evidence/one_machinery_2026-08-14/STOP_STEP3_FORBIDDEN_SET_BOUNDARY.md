# STOP AT STEP 3 — AN OWED OWNER WORD. Where the forbidden set ENDS is not ruled, and it re-prices the established book.

**ORDER 30B build seat · `land/order-29` · 2026-08-14 · Step 2 is WIRED AND PUSHED · Step 3's
CALIBRATION is DERIVED · Step 3's WIRING is not started · PR #510 stays HELD.**

The brief's rule: *"If a design question arises that the rulings do not cover, STOP and report it as an
owed owner word rather than choosing."* This is that question. **Measured, it is worth up to 19,273 board
points across 401 rows, and it flips the sign of two whole pathways** — so the seat will not choose it.

---

## 1. WHAT IS DONE, AND IS NOT IN QUESTION

**STEP 2 IS WIRED, MEASURED AND PUSHED** (`2ba3924`). The owner's ruling went in exactly as ruled, at full
precision, and reproduces his own disclosed numbers:

| | |
|---|---|
| fade | `D(2)=0.5502 · D(3)=0.2628 · D(4)=0.3460 · D(c≥4)=0.3460 FLAT`, log-linear, continuous clock |
| board | `84c9ea16` → **`9298203135202a0c707bb0977ba38c31`**, total 718,019 → **706,672** (−11,347) |
| movers | **46, every one `cg == 0` and ND in-curve.** Zero pool movers, zero rows with evidence |
| named rows | `smillie` **471** · `demattia` **301** · `knobel` **287** — the ruling said ~471 / ~301 / ~287 |
| printed-day-0 | **89 of 89, tolerance 0**, under the restated identity `printed == round(v0 × D(c))` |

**STEP 3's CALIBRATION IS DERIVED AND HOLDS ITS PREREG** (`BLEND30B.json`, `o30b_blend_fit.py`). This half
of Step 3 is fully determined by ruling 4 and is not in question:

```
w(g) = 1 - exp(-(g/tau)^beta)        tau = 11.650213   beta = 0.937162
```

| | |
|---|---|
| targets | the **R1 re-derived** cumulative backbone `≤0 0.5502 / ≤2 0.6485 / ≤5 0.6887 / ≤10 0.8223` |
| `w(0)` | **0 exactly, by construction** — so the `≤0` cell is matched identically and the price there is `v0 × D(2)` |
| RMS residual | **0.0197 in D units** — **P14 HELD** (bar 0.05) |
| entry crossover | **7.879 games** — **P15 HELD** (ruled window 6–10) |
| τ band | 11.65 ∈ [4, 12] — **P15 proxy HELD** |

The scale is an **inversion, not a fit**: the backbone is RAW(1)-normalised, so the production leg reads
1.0 and the faded-v0 leg reads `D(2)`, and `w = (B − D2)/(1 − D2)` gives three exact `w` points. Only the
two-parameter form — declared in `PREREG_30B` P13 before any of this ran — is fitted.

---

## 2. THE QUESTION

The blend needs a **production-projection**. The brief says it is the engine's production estimate with
*"THE FORBIDDEN SET DELETED (the 26A objects: pathway pedestals, par tables, prior poles — bars/aging/form
legitimately retained)"*.

**Three objects are named. Enumerated against the code, they are in three completely different states:**

| forbidden object | where it lives | reachable from a printed price? |
|---|---|---|
| **pathway pedestals** | `PICKEQ` / `_pick_equiv`, `rl_model.py:1803-1841` | **NO — ALREADY DELETED.** "THE SPLIT" (`rl_model.py:1831-1837`) retired it: *"Nothing assigns `_eff` from PICKEQ any more"*, and `rl_export.py:627` — *"'PICKEQ' is NO LONGER EXPORTED"*. Its only survivor is the `mech` display label. **Nothing to do.** |
| **prior poles** | `par_pole()` `_merged_recover.py:395-399`, consumed in `raw_ev:464,476` as `po` | **YES.** `raw_ev` → `_prod_path:2370` → `ev:2403`. This is an unambiguous forbidden object on a live price path. |
| **par tables** | `PR.par_at`, **FOUR live price sites** | **YES — and this is the question.** |

The four live `par_at` sites are not one thing:

| # | site | what it is | status |
|---|---|---|---|
| 1 | `:397` inside `par_pole` | the pole's own par read | **dies with the pole. Unambiguous.** |
| 2 | `:497` the **ISO table build** — `raw_ev(synth(pk, par_at(pos,pk,4)))` | the isotonic **pick-tax** on the production leg, built by probing the pick curve *at par* | **UNRULED** |
| 3 | `:2298` `_c_w` — `Q = clip(sa/par, 0, 2)` | the ITEM A / ITEM C **evidence weight**, feeding `_a_blend:2354` and the ruck ceiling `:2413` | **UNRULED** |
| 4 | `:2438` inside `ev` itself — `pr = bestlvl/par` | the gate on the **mediocre-for-years** decay branch | **UNRULED** |

**Sites 2, 3 and 4 are par tables by construction and are on printed-price paths — so the letter of the
ruling deletes them. But none of them is a pedestal or a pole.** Site 2 is a pick-side correction, site 3
is an evidence weight, site 4 is a form/decay gate — and *"bars/aging/form legitimately retained"* is
exactly the clause that argues they stay. **The rulings name the objects; they do not draw the boundary.**

---

## 3. WHAT IT COSTS — MEASURED, NOT ARGUED

Two **declared, default-off** measurement dials were added (`RL_O30B_NOPOLE`, `RL_O30B_NOISO`;
default-off verified **byte-exact** — `9298203135202a0c707bb0977ba38c31` reproduced) and the boards built.
**These are the DELETION half only — no blend is wired — so they price the boundary, not the act.**

| ablation | board | total | Δ | movers |
|---|---|---:|---:|---:|
| — | Step 2 (nothing deleted) | 706,672 | — | — |
| **A** pole deleted | `554c49df` | **687,399** | **−19,273 (−2.73 %)** | **271 of 804** |
| **B** pole + par-built ISO deleted | `7b17962a` | **689,765** | **−16,907 (−2.39 %)** | **401 of 804** |

**THREE THINGS IN THAT TABLE THE OWNER SHOULD SEE.**

**(a) The deletion re-prices the ESTABLISHED book, not the sitters.** The movers are overwhelmingly
`cg 16+`: **183 rows / −15,965** under A, **293 rows / −15,045** under B. The sitter fade moved 46 rows and
−11,347; this moves 271–401 rows and −17k to −19k. It is not a bookkeeping tidy.

**(b) Adding a second deletion makes the board go UP.** B deletes strictly more than A yet lands 2,366
points *higher*, because the ISO pick-tax is a multiplier that was in places *below* 1. The boundary does
not move the board monotonically, so it cannot be reasoned about by "delete more, price less".

**(c) It flips the sign of whole pathways.** Per entry type:

| pathway | ablation A | ablation B | swing |
|---|---:|---:|---:|
| **MSD** | **−815** | **+1,273** | **2,088** |
| **SSP** | **−469** | **+90** | **559** |
| ND | −16,035 | −17,590 | 1,555 |
| RD | −896 | −341 | 555 |

MSD and SSP are precisely the pathways Step 4 is about. **Ruling the boundary one way makes the mid-season
book cheaper; the other way makes it dearer — from a question about which `par_at` call sites count as
"par tables".**

Largest single mover under both: `isaac-kako` (ND 2024, pick 13, 36 games) **1320 → 747 / 744**.

---

## 4. WHY THE SEAT WILL NOT PICK

Both readings are the owner's own words, and they point opposite ways:

- **"THE FORBIDDEN SET DELETED, not bypassed"** — `par_at` is named. Sites 2/3/4 are `par_at` on live price
  paths. Under this reading they go, and the production leg loses its pick correction, its evidence weight
  and its decay gate in one act.
- **"bars/aging/form legitimately retained"** — an isotonic pick guard, an evidence weight and a
  form-decay gate are not pedestals and not poles. Under this reading only site 1 goes with the pole, and
  the deletion is the −19,273 of ablation A alone.

And there is a third thing neither reading settles: **with the pole gone, `raw_ev` collapses to `price6`,
and the ISO table at site 2 is built by re-running `raw_ev` on par synths — so the ISO table is
re-derived by the pole's deletion whether or not it is itself deleted.** Ablation A already carries that
(its 271 movers include the re-derived ISO). Whether the correct object is "the ISO table as re-derived
without the pole" or "no ISO table at all" is a third option the seat has not priced, because it is not
one of the two the rulings suggest.

**The seat found the boundary while doing the work it was ordered to do, priced it before asking, and is
asking rather than choosing — exactly as the Step-2 stop did, and for the same reason: it decides prices
for hundreds of rows, most of them established players who are not what this act is about.**

---

## 5. THE WORD THE SEAT IS ASKING FOR

**Q1 — THE ISO PICK-TAX (`par_at` site 2).** Is the par-built isotonic pick correction on the production
leg a **forbidden par table** (deleted — one-machinery says pick information belongs in the `v0` term, not
as a multiplier on production), or **retained machinery** (it is a monotonicity guard, not a pedestal)?

**Q2 — THE EVIDENCE WEIGHT (`par_at` site 3).** `_c_w`'s `Q = clip(sa/par, 0, 2)` measures a player's
career average **against par**. It feeds ITEM A's anchor blend and the ruck ceiling. ITEM A's anchor blend
is **superseded by the ruled blend anyway** — but the ruck ceiling is not. Does `Q` keep its par
denominator, or does it re-reference to something in the v0 language?

**Q3 — THE DECAY GATE (`par_at` site 4).** `ev:2438`'s `pr = bestlvl/par` gates the mediocre-for-years
decay. Deleted, or retained as form machinery?

**Q4 — THE SUPERSESSION LIST, stated so it is on the record rather than assumed.** The seat reads the one
formula as **replacing**, not wrapping: `sitout_ev` (the `ns==0` arm), `_a_blend` (ITEM A's anchor carry)
and the year-zero floor `floor_frac × entry_anchor` are all anchor↔production blends or anchor lower
bounds, and the ruled blend is the one that survives. **Wrapping instead of replacing would double-count
pedigree**, because ITEM A already carries an anchor leg. Confirm that reading — and say explicitly
whether the **ITEM H ruled cuts**, the **D8 graded staleness**, the **ruck ceiling** and the **KPF
compression** are inside the retained form machinery or outside it. The seat can carry all four either
way; it will not decide which.

---

## 6. STATE AT THE STOP

| | |
|---|---|
| branch / tip | `land/order-29` — see the push accompanying this note |
| board | **`9298203135202a0c707bb0977ba38c31`** (Steps 0–2), total **706,672** |
| Step 0 | **COMPLETE** — entry control PASS vs `36d5dfc7` |
| Step 1 | **COMPLETE** — positional v0 re-fit, 107 ascents → 0, A2 cured, λ = 0.995505141235 |
| Step 2 | **COMPLETE AND WIRED** — the ruled fade; 46 movers; printed-day-0 89/89 |
| Step 3 | **CALIBRATION DERIVED** (`τ`, `β`, P13/P14/P15 all HELD). **WIRING NOT STARTED.** |
| Steps 4–7 | **NOT STARTED** — every one of them consumes the wired blend |
| store / `v0surf` / `rl_model.py` | **UNMOVED** |
| PR #510 | **HELD — `[HELD — DO NOT MERGE]`** |

### CONTROLS CLOSED AT THIS STOP

| control | result |
|---|---|
| **P28 KILL-SWITCH, in its complete form** | `RL_ONEMACH=0` **+ the ENTRY artifact `911774bc`** reproduces the entry board **`36d5dfc7` BYTE-EXACT**. **HELD.** The 30B code block is provably the only *code* that moves the board; the artifact is the separately-declared mover (P29). |
| **P28, code-only reading** | `RL_ONEMACH=0` with the Step-1 artifact reproduces **`84c9ea16` byte-exact** — the 29B flat hold restored exactly. |
| **measurement dials default-off** | byte-exact: `9298203135202a0c707bb0977ba38c31` reproduced with both dials present and unset. |

### PREREG SCORED SO FAR (by number, breaches owned)

| # | verdict | reading |
|---|---|---|
| P1–P7 | **HELD** (P5 partially breached, owned at Step 1) | as filed in `860d370` |
| **P8** | **BREACHED** | `D_LB(3)` moved 0.0972, outside the declared ±0.06; and the direction was predicted UP, measured DOWN at every depth. Owned in the Step-2 stop. |
| **P9** | **BREACHED** | the re-derived row is NOT monotone (0.5502 > 0.2628 < 0.3460). **The owner ruled the non-monotone row IS the law.** |
| P10 | **HELD** | `RAW(1)` 1.028605 → 1.020106, −0.83 % (bar 3 %) |
| P11 | **HELD** | the harness flagged its own control as DRIFT, expected-by-construction |
| **P12** | **HELD, with one amendment on the record** | the three named clocks reproduce packet 2 exactly (`smillie` 2.92 · `demattia` 3.92 · `knobel` 4.92). **The "deep end EXTRAPOLATED" clause of P12 is superseded by the owner's amendment — the deep end holds FLAT.** |
| P13 | **HELD** | form as declared, `w(0)=0` exact, strictly increasing |
| P14 | **HELD** | RMS 0.0197 D units (bar 0.05) |
| P15 | **HELD** | crossover 7.879 games, in the ruled 6–10; τ = 11.65 ∈ [4,12] |
| **P18** | **HELD** | the sitter book **21,192 → 10,337**, inside the declared 9,500–11,500 band and on the ~10,185 the preview predicted |
| P28 | **HELD** | both readings, above |
| P33 | **HELD** | nothing merged |
| P16/P17/P19–P27/P29–P32 | **NOT YET REACHABLE** | they consume the wired blend, the pool step, the position gate, the numéraire re-pin or the final board |

---

*Nothing was tuned after seeing any reading. The ablations were run once each, from a byte-exact-verified
default-off baseline, and this note was written from their first output.*
