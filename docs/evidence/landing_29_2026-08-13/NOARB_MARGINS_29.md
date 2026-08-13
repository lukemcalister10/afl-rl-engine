# NO-ARBITRAGE TABLES — THE **FINAL LANDED BOARD** (ORDER 29, PR #510, board `86c8d5d9`)

Companion to `docs/evidence/pool_landing_v2_2026-08-12` / the ORDER 25 `NOARB_REVIEW`, in the same
layout so the owner can read landed against live side by side.
A NEGATIVE margin against the 14% annual charge is an arbitrage.

> ## READ THIS FIRST — THE DECIDING LANDED READING DID NOT RUN
> The as-of matrix **was** regenerated under the landed engine — that is the expensive half and it
> is done (`per_entrant_O29FINAL.json`, 2648 records, 3m14s). **Both cohort instruments then
> refused to read it**, on their own store / surface / population pins. Nothing was tuned to get a
> number: the halt is transcribed verbatim in `NOARB_LANDED_HALT.txt` and the five blocking
> literals are measured in `NOARB_BASIS_out.txt`.
> 
> **So sections 1–3 below carry the LIVE board's numbers with the landed column marked HALTED.**
> Section 4 carries the landed readings that *did* run — the pathway-grain instruments and the
> identity gate, neither of which pins the store.

---

## 0. WHAT BLOCKS THE LANDED READING, AND WHAT IT WOULD TAKE

| file | name | holds | landed matrix carries |
|---|---|---|---|
| `harness_pvc_REPINNED_pass3.py` | `EXPECT_STORE` | `d9a24282` | `cb38ef11` |
| `harness_pvc_REPINNED_pass3.py` | `EXPECT_V0SURF` | `6ef67f07db98` | `4405cba2b42f` |
| `harness_pvc_REPINNED_pass3.py` | `EXPECT_N` | `1197` | `1200` |
| `noarb_table_allarm.py` | `store_md5 inline` | `d9a24282` | `cb38ef11` |
| `noarb_table_allarm.py` | `v0surf_sig inline` | `6ef67f07db98` | `4405cba2b42f` |

`noarb_table_338.py` **itself carries no pin and needs no edit** — md5 `0f8220351c64c56ccfa90c60edcdfa5f`,
verified unmoved at run. It delegates to the harness; `noarb_table_allarm.py` asserts *its* md5.

`EXPECT_N` moves **1197 → 1200**, and the +3 are named: **`adam-treloar`, `dylan-shiel`,
`jeremy-cameron`** — the ORDER 29 unflag-three (lever 1), which stop being `_pvc_exclude` and
therefore start teaching the curve. Nothing else entered the teaching population and nothing left.

**The control that makes this diagnostic:** the same invocation, same instrument copies, on the
live matrix reproduced `NOARB_MARGINS_V2` **to the last digit**. The pipeline is sound; the pin is
the blocker. The harness is named `harness_pvc_REPINNED_pass3.py` and its header is a log of
prior declared re-points — so the fix is precedented and small, but it re-points the instrument
that *defines the basis of the no-arb reading*, and this seat was authorised exactly one re-point
(the identity gate's). It is the owner's call, and it is now a two-minute call.

---

## 1. OVERALL — the all-arm deciding instrument (ND + every pool pathway, one cohort)

| window | n | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | yr6 | yr7 | apprec 0→1 | margin v14% | verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| PRIMARY 2005-2023 **(LIVE `88ce647f`)** | 2212 | 1.0000 | 0.8077 | 0.9737 | 1.0703 | 1.1291 | 1.1096 | 1.0560 | 0.9260 | -19.23% | **+33.23%** | no arb |
| PRIMARY 2005-2023 **(LANDED `86c8d5d9`)** | — | — | — | — | — | — | — | — | — | — | **HALTED** | pin |
| MODERN  2019-2023 **(LIVE `88ce647f`)** | 540 | 1.0000 | 0.8225 | 0.9256 | 0.9794 | 0.9772 | 1.0345 | 0.9099 | 0.8009 | -17.75% | **+31.75%** | no arb |
| MODERN  2019-2023 **(LANDED `86c8d5d9`)** | — | — | — | — | — | — | — | — | — | — | **HALTED** | pin |

## 2. ND ONLY (picks 1–64) — the legacy retained instrument, `noarb_table_338.py` UNMODIFIED

| group | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | yr6 | yr7 | apprec 0→1 | margin v14% | verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ALL picks 1-64 **(LIVE)** | 1.0000 | 1.0730 | 1.3343 | 1.4952 | 1.5712 | 1.5529 | 1.4981 | 1.3005 | +7.30% | **+6.70%** | no arb |
| ALL picks 1-64 **(LANDED)** | — | — | — | — | — | — | — | — | — | **HALTED** | pin |
| picks 1-20 **(LIVE)** | 1.0000 | 1.1218 | 1.3642 | 1.4886 | 1.5981 | 1.5685 | 1.4750 | 1.2931 | +12.18% | **+1.82%** | no arb |
| picks 1-20 **(LANDED)** | — | — | — | — | — | — | — | — | — | **HALTED** | pin |
| picks 21-64 **(LIVE)** | 1.0000 | 0.9996 | 1.2894 | 1.5051 | 1.5307 | 1.5299 | 1.5322 | 1.3113 | -0.04% | **+14.04%** | no arb |
| picks 21-64 **(LANDED)** | — | — | — | — | — | — | — | — | — | **HALTED** | pin |

## 3. BY ARM — ND vs each pool pathway (all-arm construction, pooled ratio within the arm)

**PRIMARY 2005-2023 — LIVE `88ce647f`.  LANDED: HALTED on the same pins.**

| arm | n | yr1 | yr4 |
|---|---:|---:|---:|
| ND | 1310 | 1.0141 | 1.4803 |
| RD | 623 | 0.4379 | 0.5090 |
| MSD | 55 | n/a\* | 0.6083 |
| UNR | 49 | 0.2052 | 0.6090 |
| IRE | 47 | 0.2276 | 0.2181 |
| PDA | 43 | 0.3062 | 0.5344 |
| PDN | 33 | 0.1522 | 0.1897 |
| SSP | 31 | 0.9846 | 0.8108 |
| PDS | 21 | 0.1329 | 0.1305 |

**MODERN  2019-2023 — LIVE `88ce647f`.  LANDED: HALTED on the same pins.**

| arm | n | yr1 | yr4 |
|---|---:|---:|---:|
| ND | 325 | 0.9962 | 1.2431 |
| RD | 66 | 0.3398 | 0.3989 |
| MSD | 55 | n/a\* | 0.6083 |
| SSP | 31 | 0.9846 | 0.8108 |
| PDN | 25 | 0.1431 | 0.0982 |
| UNR | 13 | 0.2664 | 0.2777 |
| PDA | 13 | 0.1633 | 0.4705 |
| IRE | 12 | 0.1411 | 0.0260 |

\* the disclosed MSD debut-year gap: the mid-season draft begins 2019 and its cohort year 1
precedes the emitted window for part of the population; those rows are EXCLUDED from that year,
never scored zero.

---

## 4. WHAT **DID** RUN ON THE LANDED BOARD

These instruments carry no store pin, so the landing did not lock them out. Both are committed
pre-statements, re-read on the landed basis with no predicate touched.

### 4.1 By arm, on the landed board — the mark-path construction (`INSTRUMENTS29`)

**This is NOT section 3's number and must not be read as a landed version of it.** Section 3's
`yr1`/`yr4` are *as-of price in cohort year N ÷ mean year-0 price* over the arm. The table below is
`m_allin(d)` = *sum of marks at depth d ÷ sum of derived day-0*, the pre-stated mark-path
progression. Different denominator, different question — but it is a genuine **landed** pathway
reading, and it is the only by-arm number in this document that is one.

| arm | n | d0 | d1 | d4 | peak | at d | verdict | reverse no-arb |
|---|---:|---:|---:|---:|---:|---:|---|---|
| IRE | 57 | 1.4949 | 1.6364 | 1.6487 | 2.0281 | d6 | PASS | PASS |
| MSD | 106 | n/a\* | 0.9206 | 0.9096 | 1.2379 | d5 | PASS | PASS |
| ND 1-64 | 1447 | 1.1258 | 1.3042 | 1.5352 | 1.5653 | d3 | PASS | PASS |
| ND>64 | 121 | 1.0889 | 1.2891 | 1.2530 | 1.5181 | d6 | PASS | PASS |
| PDA | 51 | 0.9242 | 1.0886 | 1.6901 | 1.6901 | d4 | PASS | PASS |
| PDN | 43 | 1.1126 | 1.3876 | 1.0011 | 1.5228 | d5 | PASS | PASS |
| PDS | 21 | 0.9993 | 0.7585 | 1.3118 | 1.3118 | d4 | PASS | PASS |
| RD | 691 | 1.2782 | 1.3460 | 1.4241 | 1.4660 | d3 | PASS | PASS |
| SSP | 52 | 1.8403 | 1.7713 | 1.2709 | 2.0527 | d2 | PASS | PASS |
| UNR | 59 | 0.4926 | 0.6801 | 1.7261 | 1.7261 | d4 | PASS | PASS |

**Mark-path progression: 10 of 10 arms PASS. Reverse no-arb: 10 of 10 arms PASS, 0 pathways fail.**
Smallest `max m(d≥1)` across arms is **1.2379** (MSD) — 24% above the failure line.

### 4.2 The identity gate (P16), on the landed board

| reading | result |
|---|---|
| price-function identity, panel | **12 of 12 PASS**, max &#124;mine/price6 − 1&#124; = **0.000e+00** |
| price-function identity, board-wide | **800 of 800 within 1e−6 (100.0%)**, max **0.000e+00**, over 804 active rows |
| pins re-asserted at exit | store `cb38ef11` · board `86c8d5d9` — **unmoved** |

---

## 5. THE DELTA — WHAT MOVED vs THE LIVE BOARD'S TABLES

The pool day-0 re-derivation was the point of this landing, so the question the owner will ask is
**did the pool yr0→yr1 cliffs close** — the live RD 0.4379, UNR 0.2052, PDN 0.1522, PDS 0.1329,
IRE 0.2276 of section 3.

**That question cannot be answered from this document, and the reason is section 0, not the board.**
The instrument that measures those cliffs is the one that refused the landed matrix. Section 4.1's
landed by-arm numbers are a *different construction* and do not answer it — quoting them as though
they did would be the exact substitution this packet has refused everywhere else.

What **is** measured, landed against live, on identical constructions:

| reading | live | landed | source |
|---|---|---|---|
| mark-path progression | 10 of 10 PASS (ORDER 28 *candidate* basis, off-dial marks) | **10 of 10 PASS** (landed board, landed marks) | `INSTRUMENTS29` vs `INSTRUMENTS28` |
| reverse no-arb | 10 of 10 PASS (same caveat) | **10 of 10 PASS**, 0 pathways fail | `INSTRUMENTS29` |
| price-function identity, board-wide | 800 of 800, 0.000e+00 | **800 of 800, 0.000e+00** | `GATE29` vs `GATE28` |
| marks, landed − live (same denominator) | — | shallow **-0.0332**, deep **-0.0815** | `INSTRUMENTS29` §3 |

**One delta is a correction to a delivered packet.** ORDER 28 could not measure the dial's effect
on the marks, so it predicted the direction — *higher at shallow depths, unchanged deeper* — and
used it to argue its own progressions were **conservative**. Re-emitted under the landed engine,
the marks are **lower at essentially every arm and every depth, and they fall further deep than
shallow** (-0.0332 vs -0.0815) — the opposite shape, consistent with a board that fell 6.17% under the
numéraire re-pin. ORDER 28's read was **optimistic, not conservative**. Neither verdict in section
4.1 depends on that assumption — both instruments are run on the landed marks directly — but
ORDER 28's reported margin was defended by a claim that has now been measured and did not hold.

---

### Provenance

| file | what |
|---|---|
| `emit_variant_o29.sh` | the as-of matrix, re-emitted on the landed tree (the expensive half, done) |
| `run_noarb_o29.sh` · `NOARB_MARGINS_29_out.txt` | both cohort instruments, live basis + the landed attempt |
| `NOARB_LANDED_HALT.txt` | the two refusals, verbatim, with instrument md5s computed at run |
| `o29_noarb_basis.py` · `NOARB_BASIS_out.txt` | the five blocking literals, measured |
| `o29_instruments.py` · `INSTRUMENTS29.{json,txt}` | mark-path + reverse no-arb, ON the landed board |
| `o29_gate.py` · `GATE29.{json,txt}` · `GATE29_REPOINT.diff` | the identity gate, re-pointed and run |
