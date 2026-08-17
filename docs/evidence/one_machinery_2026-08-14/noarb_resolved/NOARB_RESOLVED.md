# NOARB_RESOLVED — THE RESOLVED CANDIDATE'S NO-ARB READING

**ORDER 30B-N.** Brief: #334 comment 5310246218. Prereg: `PREREG_30BN.md` (filed before any run).

> ### ⛔ THE RESOLVED COLUMN IS **HALTED**, AND THE HALT IS THE FINDING.
> The resolved law is **wired, proven exact and built** (board `d3c65bc4`). What could not be produced
> is its **as-of matrix**, because the ORDER 29C emitter refuses the year-0 column on this branch —
> **with this order's dial ON and equally with it OFF**. `ORDER 30B`'s own **Step-1 positional v0
> re-fit** (commit `860d370`) moved the year-0 object out from under the emitter's fail-closed
> replication proof: **43 of 89** wired entrants still reproduce it, **54.5%** of the 2,643-row emit
> population has a moved `v0`.
> **The year-0 basis is an owner word. Full statement and the two options: `STOP_STEP3_YEAR0_BASIS.md`.**
> No margin below has been tuned, and nothing has been re-pointed to make a refusal pass.

---

## CAVEATS — THESE TRAVEL WITH EVERY TABLE ON THIS PAGE

1. **PRE-NUMERAIRE.** Step 6's re-pin has **not** run. **Read the MOVEMENT, not the level.**
2. **POOL β IS PROVISIONAL.** Pool `v0` cells are Step 4's work, and the sitter fade is **forced to
   `D = 1.0` for every pool row** because the pool fade is **not derived**.
3. **THE RUCK-HEAD DEFECT IS OPEN.**
4. **T4 (THE OBJECT) IS OPEN.** These tables price the **v0 object**. The `entry_anchor` object is not
   wired and not read here.
5. **NOTHING IS GREENLIT.** Both dials are default-off; the committed board reproduces byte-exact with
   them unset.
6. **The bridge lane (11–15 games) is a DECLARED BRIDGE, not a measurement.**
7. **β(g) is NOT monotone** — it rises from 2.5 to 10.5 games before falling. That is what the band fit
   measured; it is carried, not patched.

---

## 1. THE OWNER'S TABLE — YEAR PATHS AS % OF ENTRY (yr0 = 100)

**Instrument:** all-arm deciding instrument, `noarb_table_allarm.py`.
**Population:** every entrant drafted through mechanisms eligible to debut in the same year (ND + RD +
SSP of year Y with MSD of Y+1).
**Basis:** year-0 = the landed entry law; numerator = `ev(p,Y)` under the stated variant.
**Charge:** 14% annual. **A NEGATIVE MARGIN IS AN ARBITRAGE.**

### 1a. PRIMARY — cohorts 2005–2023

| year | LIVE `88ce647f` | SITTER-LAW PREVIEW (SITALL, 2026-08-13) | **RESOLVED CANDIDATE** |
|---|---:|---:|---:|
| yr0 | 100.0 | 100.0 | **HALTED** |
| yr1 | 80.8 | 118.4 | **HALTED** |
| yr2 | 97.4 | 135.6 | **HALTED** |
| yr3 | 107.0 | 150.4 | **HALTED** |
| yr4 | 112.9 | 159.4 | **HALTED** |
| yr5 | 111.0 | 157.7 | **HALTED** |
| **apprec 0→1** | **−19.23%** | **+18.39%** | **HALTED** |
| **margin v14%** | **+33.23%** | **−4.39%** | **HALTED** |
| **verdict** | **no arb** | **ARB** | **HALTED** |

### 1b. MODERN — cohorts 2019–2023

| year | LIVE `88ce647f` | SITTER-LAW PREVIEW (SITALL) | **RESOLVED CANDIDATE** |
|---|---:|---:|---:|
| yr0 | 100.0 | 100.0 | **HALTED** |
| yr1 | 82.3 | 111.9 | **HALTED** |
| yr2 | 92.6 | 120.9 | **HALTED** |
| yr3 | 97.9 | 128.6 | **HALTED** |
| yr4 | 97.7 | 128.9 | **HALTED** |
| yr5 | 103.5 | 137.8 | **HALTED** |
| **apprec 0→1** | **−17.75%** | **+11.87%** | **HALTED** |
| **margin v14%** | **+31.75%** | **+2.13%** | **HALTED** |
| **verdict** | **no arb** | **no arb** | **HALTED** |

---

## 2. THE LEGACY RETAINED INSTRUMENT — `noarb_table_338.py`, UNMODIFIED

**Instrument pin asserted at run, never hardcoded:** `noarb_table_338.py` md5
`0f8220351c64c56ccfa90c60edcdfa5f`. **Population:** national draftees only — this instrument has no
pool arm, which is why it and the all-arm instrument answer differently.

### 2a. ND ALL, picks 1–64 — YEAR PATHS AS % OF ENTRY

| year | LIVE `88ce647f` | SITALL | **RESOLVED** |
|---|---:|---:|---:|
| yr0 | 100.0 | 100.0 | **HALTED** |
| yr1 | 107.3 | 118.8 | **HALTED** |
| yr2 | — | 138.0 | **HALTED** |
| yr3 | — | 156.4 | **HALTED** |
| yr4 | — | 165.2 | **HALTED** |
| yr5 | — | 163.4 | **HALTED** |
| **margin v14%** | **+6.70% no arb** | **−4.76% ARB** | **HALTED** |

### 2b. ND picks 1–20

| year | LIVE | SITALL | **RESOLVED** |
|---|---:|---:|---:|
| yr1 | 112.2 | 125.3 | **HALTED** |
| yr4 | — | 165.4 | **HALTED** |
| **margin v14%** | **+1.82% no arb** | **−11.28% ARB** | **HALTED** |

### 2c. ND picks 21–64

| year | LIVE | SITALL | **RESOLVED** |
|---|---:|---:|---:|
| yr1 | 100.0 | 108.3 | **HALTED** |
| yr4 | — | 164.9 | **HALTED** |
| **margin v14%** | **+14.04% no arb** | **+5.67% no arb** | **HALTED** |

**ARBITRAGE COUNT — LIVE 0 of 5 · SITALL 3 of 5 · RESOLVED not readable.**

---

## 3. BY ARM — yr1 / yr4 (PRIMARY window)

Landed-law basis (`O29CFINAL`) carried as the reference the resolved column would have replaced.

| arm | n | yr1 | yr4 | mean v0 | **RESOLVED yr1 / yr4** |
|---|---:|---:|---:|---:|---:|
| ND | 1309 | 1.3068 | 1.6484 | 711.1 | **HALTED** |
| RD | 623 | 1.4461 | 1.4407 | 245.8 | **HALTED** |
| MSD | 55 | *nan* | 0.8567 | *nan* | **HALTED** |
| UNR | 49 | 1.0490 | 1.3492 | 115.9 | **HALTED** |
| IRE | 47 | 1.5547 | 1.3997 | 86.4 | **HALTED** |
| PDA | 43 | 1.2628 | 1.4523 | 207.8 | **HALTED** |
| PDN | 33 | 1.0361 | 1.1764 | 87.9 | **HALTED** |
| SSP | 31 | 2.4081 | 1.8783 | 209.0 | **HALTED** |
| PDS | 21 | 1.3689 | 0.9806 | 85.3 | **HALTED** |

**MSD `nan` is carried, not rediscovered:** the emitter builds `yrs` from draft year + 1 on every route
while `cohort()` for MSD is the draft year itself, so MSD's d=0 denominator is empty (ORDER 26A
anomaly 5).

---

## 4. WHAT *IS* READABLE: THE RESOLVED CANDIDATE ON THE CURRENT BOARD

The as-of matrix halted, but the **2026 board** under the resolved law is built and controlled. This is
a level reading, **pre-numeraire**, and it is **not** a no-arb reading.

| configuration | book total | vs preview |
|---|---:|---:|
| PREVIEW as built (weight, v0, no join) | 679,874 | — |
| weight reading, v0, JOINED | 667,260 | −1.86% |
| ADDITIVE reading, v0, no join | 755,464 | +11.12% |
| **RESOLVED: additive, v0, JOINED** | **715,229** | **+5.20%** |
| RESOLVED: additive, ANCHOR, JOINED | 715,377 | +5.22% |

**Wired board `d3c65bc4` reproduces the derived resolved board at 715,219.2 vs 715,228.6 — −0.0014%.**

**Lane populations:** sitter 89 (17,243) · thin 99 (35,470) · bridge 44 (29,578) · deep 572 (632,937).

**The mechanism the owner should see, because it is what the halted table would have measured.** At a
year-1 cell the fade clock sits at `c ≈ 2`, so `D = 0.5502` and the backbone is lane 2. A rookie with
**1–10 games falls in the THIN lane, where production does not enter at all**, and is priced at
`v0 × D × b_lift(g)` — **0.602 × v0 at one game rising to 0.797 × v0 at ten**. The un-rewired marks
that SITALL preserved sat near **1.37 × v0**. **The join is therefore a ~40% haircut on played
rookies**, and any green margin the resolved candidate eventually prints at yr1 will arrive *because
rookie marks collapse*, not because the law has been vindicated. That is a finding about the join, and
it is stated here in advance of the reading rather than after it.

---

## 5. PREREG SCORE (`PREREG_30BN.md`, filed before any run)

| # | prediction | verdict | note |
|---|---|---|---|
| **P1** | dial-off byte identity | **HELD** | `9298203135202a0c707bb0977ba38c31` |
| **P2** | preview lane undisturbed | **HELD** | `6a392bca7ad0dee04a6b4f037c758f65` |
| **P3a** | sitter/thin rows exact (< 0.05) | **BREACHED** | sitter max **0.049**, thin max **0.510**. **The band was wrong, not the wiring.** Two rounding sources were omitted from it: the derived board stores `round(pr,1)` (±0.05) and the preview lane's blend site has always ended in `round()` in *engine* currency (±0.5/`_PL_F` = 0.4751 board). Sitter = exactly the first; thin = exactly the sum. |
| **P3b** | max \|Δ\| ≤ 1.2 | **BREACHED** | 2.05 |
| **P3c** | no row > 1.5 | **BREACHED** | 12 rows |
| **P3d** | total within ±150 | **HELD** | −10.1 |
| **P3e** | 715,229 class | **HELD** | 715,219.2 |
| **P3f** | *added at run:* the law within the blend-site round | see below | superseded by the exact wiring proof |
| — | **THE WIRING PROOF** (`o30bn_lawcheck.py`) | **HELD EXACTLY** | `beta30bn`≡`beta_at` over 4,009 pts; `b_lift30bn`≡`b_lift` over 48,108 pts; `_pv_resolved`≡`book()` to **1.8e-12** over 14,592 pts. Reference self-checked against `RESOLVED_ALLROWS.json` at **0.0** first. |
| **P4** | determinism | **HELD** | `d3c65bc4` twice |
| **P5** | instrument pins hold | **PARTIAL** | `noarb_table_338.py` and the standing emitter both verified at run. But the **emitter's own year-0 pin REFUSED** — and per the prereg, *"if a pin refuses, THE HALT IS THE FINDING"*. It is reported verbatim. |
| **P6–P13** | the directional core (yr1 falls; margins greener; 0 of 5 arb; ordering preserved; all-arm improves less than ND; path steepens; by-arm) | **NOT SCORABLE** | the matrix halted. **None of these has been edited.** They stand as filed, blind, for whoever runs Step 3 after the owner's word. |
| **P14** | mark-path / reverse no-arb | **NOT SCORABLE** | same halt — both instruments read the as-of matrix |

**Scored: 5 HELD · 3 BREACHED (all three the same mis-specified P3 band) · 1 PARTIAL · 9 NOT SCORABLE.**
The three P3 breaches are a **control-design error by this seat**, disclosed as such rather than
quietly re-banded; the question P3 exists to answer was then answered exactly and independently.

---

## 6. PROVENANCE

| object | identity |
|---|---|
| store `rl_model_data.json` | `cb38ef1171dcf20aae66ebf12682be0d` (UNMOVED) |
| artifact `pvc_curve_v2.json` | `06146b00daf2043487f58a8b9f842a1e` (**moved at `860d370` — the cause of the halt**) |
| `rl_model.py` | `14000af2a46f7a3c4cdfde303f5a1aff` |
| `data/v0surf.pkl` | `5dd34ca82735f5c8f021b1c7320df8f8` |
| dial-off board (P1) | `9298203135202a0c707bb0977ba38c31` |
| preview board (P2) | `6a392bca7ad0dee04a6b4f037c758f65` |
| **resolved board (P4, twice)** | **`d3c65bc46cebb656914cacb34a693b77`** |
| LIVE matrix | `per_entrant_O25R4.json` `3c6ffcde` |
| historical-print matrix | `per_entrant_O29B.json` `ca24a49a` |
| landed-law matrix | `per_entrant_O29CFINAL.json` `6db06e40` |
| `noarb_table_338.py` | `0f8220351c64c56ccfa90c60edcdfa5f` (byte-unmodified) |
| `emit_matrix_29c.py` | `0c3efa545832dd1131bd2b403588af29` (byte-unmodified; **it is the file that refused**) |
| standing emitter | `bffde2f786be85037483e9f5f1563068` (asserted in-copy at run) |

**No instrument was modified. No literal was re-pointed. No margin was tuned. The refusal was
reproduced with the dial off before it was reported.**
