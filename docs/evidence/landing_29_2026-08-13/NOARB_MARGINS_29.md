# NO-ARBITRAGE TABLES — THE **FINAL LANDED BOARD** (ORDER 29, PR #510, board `86c8d5d9`)

Companion to `docs/evidence/pool_landing_v2_2026-08-12` / the ORDER 25 `NOARB_REVIEW`, in the same
layout so the owner can read landed against live side by side.
A NEGATIVE margin against the 14% annual charge is an arbitrage.

> ## READ THIS FIRST — THE LANDED READING NOW EXISTS, AND IT OPENS TWO ARBITRAGES
> The halt recorded below was resolved the precedented way: the supervisor seat authorized the
> five-literal re-point within the ruled ORDER 29 spec (#334 comments 5278653175 / 5279364952),
> applied to **ORDER 29's own instrument copies** under `noarb/` — the composition act's copies and
> the instrument of record are untouched, `noarb_table_338.py` byte-identical (md5 `0f822035…`,
> asserted at run). Both instruments then read the landed matrix cleanly (teaching population
> re-measured 1200 = 1197 + the unflag-three).
>
> **THE RESULT: 2 of 10 readings are ARBITRAGES on the landed board** — the legacy ND instrument's
> ALL picks 1–64 (margin **−7.73%**) and picks 1–20 (**−15.92%**). The all-arm deciding instrument
> stays no-arb in both windows (+28.71% / +26.66%). The pool yr0→yr1 cliffs did **not** close
> (§5). Nothing was tuned: the numbers are what the unmodified instrument computed.

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

**RESOLVED (2026-08-13, the supervisor seat, in-session):** the re-point was authorized within the
ruled ORDER 29 spec — the landing spec itself mandates both cohort instruments on the FINAL board,
and the pin move is exactly the basis change the landing lawfully made. Applied per this file's own
convention: ORDER 29's disclosed copies in `noarb/` (header log appended in the house style), five
literals moved (`EXPECT_STORE d9a24282→cb38ef11`, `EXPECT_V0SURF 6ef67f07db98→4405cba2b42f`,
`EXPECT_N 1197→1200` + the allarm inline pair), no tolerance, window, band or logic touched,
`noarb_table_338.py` byte-identical. Sections 1–3 below now carry the landed readings.

---

## 1. OVERALL — the all-arm deciding instrument (ND + every pool pathway, one cohort)

| window | n | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | yr6 | yr7 | apprec 0→1 | margin v14% | verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| PRIMARY 2005-2023 **(LIVE `88ce647f`)** | 2212 | 1.0000 | 0.8077 | 0.9737 | 1.0703 | 1.1291 | 1.1096 | 1.0560 | 0.9260 | -19.23% | **+33.23%** | no arb |
| PRIMARY 2005-2023 **(LANDED `86c8d5d9`)** | 2215 | 1.0000 | 0.8529 | 0.9607 | 1.0587 | 1.1188 | 1.0991 | 1.0446 | 0.9149 | -14.71% | **+28.71%** | no arb |
| MODERN  2019-2023 **(LIVE `88ce647f`)** | 540 | 1.0000 | 0.8225 | 0.9256 | 0.9794 | 0.9772 | 1.0345 | 0.9099 | 0.8009 | -17.75% | **+31.75%** | no arb |
| MODERN  2019-2023 **(LANDED `86c8d5d9`)** | 540 | 1.0000 | 0.8734 | 0.9204 | 0.9754 | 0.9732 | 1.0289 | 0.9017 | 0.7926 | -12.66% | **+26.66%** | no arb |

The landed n rises 2212 → 2215: the unflag-three join the ND arm. Margins narrow ~4.5 points in
both windows (day-0 falls less than year-1 marks under the landed engine at cohort grain) but stay
far from the line.

## 2. ND ONLY (picks 1–64) — the legacy retained instrument, `noarb_table_338.py` UNMODIFIED

| group | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | yr6 | yr7 | apprec 0→1 | margin v14% | verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ALL picks 1-64 **(LIVE)** | 1.0000 | 1.0730 | 1.3343 | 1.4952 | 1.5712 | 1.5529 | 1.4981 | 1.3005 | +7.30% | **+6.70%** | no arb |
| ALL picks 1-64 **(LANDED)** | 1.0000 | 1.2173 | 1.4051 | 1.5847 | 1.6700 | 1.6520 | 1.5935 | 1.3827 | +21.73% | **−7.73%** | **ARB** |
| picks 1-20 **(LIVE)** | 1.0000 | 1.1218 | 1.3642 | 1.4886 | 1.5981 | 1.5685 | 1.4750 | 1.2931 | +12.18% | **+1.82%** | no arb |
| picks 1-20 **(LANDED)** | 1.0000 | 1.2992 | 1.4402 | 1.5825 | 1.7036 | 1.6736 | 1.5741 | 1.3782 | +29.92% | **−15.92%** | **ARB** |
| picks 21-64 **(LIVE)** | 1.0000 | 0.9996 | 1.2894 | 1.5051 | 1.5307 | 1.5299 | 1.5322 | 1.3113 | -0.04% | **+14.04%** | no arb |
| picks 21-64 **(LANDED)** | 1.0000 | 1.0924 | 1.3516 | 1.5879 | 1.6188 | 1.6197 | 1.6225 | 1.3893 | +9.24% | **+4.76%** | no arb |

**THE TWO ARBITRAGES, stated plainly:** on the landed board, the historical ND cohort's year-0
price (the rederived curve at their picks) sits low enough relative to their year-1 marks (the
engine's as-of prices, still produced by the un-rewired four legs) that buying the ND cohort at
day 0 and holding one year returns +21.7% — above the 14% carry; +29.9% inside picks 1–20. The
teaching population is 1200 (the unflag-three included). Mechanism hypothesis, NOT asserted as
measured: the landing repriced the day-0 object (curve −, numeraire −) while year-1+ marks moved
only with the numeraire — the gap between the two IS the un-consumed rewire that P12 sized at
~47% of the entry anchor on fresh entrants. The decomposition is a follow-on measurement if the
owner wants it; this table asserts only the readings.

## 3. BY ARM — ND vs each pool pathway (all-arm construction, pooled ratio within the arm)

**PRIMARY 2005-2023 — live and landed side by side** (landed n for ND is 1313: the unflag-three).

| arm | n | yr1 LIVE | yr1 LANDED | Δ | yr4 LIVE | yr4 LANDED | Δ |
|---|---:|---:|---:|---:|---:|---:|---:|
| ND | 1313 | 1.0141 | 1.1323 | +0.1182 | 1.4803 | 1.5492 | +0.0689 |
| RD | 623 | 0.4379 | 0.4145 | −0.0234 | 0.5090 | 0.4559 | −0.0531 |
| MSD | 55 | n/a\* | n/a\* | — | 0.6083 | 0.5865 | −0.0218 |
| UNR | 49 | 0.2052 | 0.1977 | −0.0075 | 0.6090 | 0.5612 | −0.0478 |
| IRE | 47 | 0.2276 | 0.2263 | −0.0013 | 0.2181 | 0.2008 | −0.0173 |
| PDA | 43 | 0.3062 | 0.2933 | −0.0129 | 0.5344 | 0.4738 | −0.0606 |
| PDN | 33 | 0.1522 | 0.1444 | −0.0078 | 0.1897 | 0.1685 | −0.0212 |
| SSP | 31 | 0.9846 | 0.9444 | −0.0402 | 0.8108 | 0.7390 | −0.0718 |
| PDS | 21 | 0.1329 | 0.1241 | −0.0088 | 0.1305 | 0.1153 | −0.0152 |

**MODERN  2019-2023 — live and landed side by side.**

| arm | n | yr1 LIVE | yr1 LANDED | Δ | yr4 LIVE | yr4 LANDED | Δ |
|---|---:|---:|---:|---:|---:|---:|---:|
| ND | 325 | 0.9962 | 1.1088 | +0.1126 | 1.2431 | 1.3001 | +0.0570 |
| RD | 66 | 0.3398 | 0.3213 | −0.0185 | 0.3989 | 0.3570 | −0.0419 |
| MSD | 55 | n/a\* | n/a\* | — | 0.6083 | 0.5865 | −0.0218 |
| SSP | 31 | 0.9846 | 0.9444 | −0.0402 | 0.8108 | 0.7390 | −0.0718 |
| PDN | 25 | 0.1431 | 0.1346 | −0.0085 | 0.0982 | 0.0865 | −0.0117 |
| UNR | 13 | 0.2664 | 0.2560 | −0.0104 | 0.2777 | 0.2600 | −0.0177 |
| PDA | 13 | 0.1633 | 0.1537 | −0.0096 | 0.4705 | 0.4141 | −0.0564 |
| IRE | 12 | 0.1411 | 0.1395 | −0.0016 | 0.0260 | 0.0244 | −0.0016 |

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

**ANSWER (measured, §3): NO — every pool arm's cliff is unchanged-to-slightly-deeper** (PRIMARY
yr1: RD 0.4379→0.4145, UNR 0.2052→0.1977, PDN 0.1522→0.1444, PDS 0.1329→0.1241, IRE
0.2276→0.2263), while the ND arm moved the OTHER way (1.0141→1.1323). This is the un-consumed
rewire made visible at cohort grain: the landing built the day-0 objects (curve, v0s, numeraire)
but the PRINTED prices at every horizon still come through the four legs, which this act was
ruled NOT to touch. P12 measured the same object on fresh entrants (printed ≈ 0.53× of
v0 × numeraire). The cliffs the owner set out to close live in the legs, and the legs are the
next act — landing this board does not close them, and this table says so rather than implying
otherwise.

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
| `noarb/harness_pvc_REPINNED_pass3.py` · `noarb/noarb_table_allarm.py` | ORDER 29's disclosed re-pointed copies (five literals; header log appended) |
| `noarb/noarb_table_338.py` | byte-identical to the instrument of record, md5 `0f822035…` |
| `noarb/t338_O29FINAL.txt` · `noarb/allarm_O29FINAL.txt` · `noarb/*.json` | the landed readings, both instruments |
| `noarb/MARGINS_O29.{txt,json}` | the canonical margins reporter on live + landed: **2 of 10 ARB** |

---
---

# PART B — THE ORDER 29B COLUMN: THE ENTRY WIRING, BOARD `36d5dfc7`

**Appended 2026-08-13 by the ORDER 29B build seat. Nothing above this line is edited.** Every ORDER 29
reading in Part A stands exactly as it was published; this part adds a column beside it.

> ## READ THIS FIRST — THE ARBITRAGES DID NOT CLOSE. THEY WIDENED, AND A THIRD OPENED.
> `PREREG_29B` **P29B-26** predicted the direction: *"raising the day-0 denominator reduces measured
> yr0→1 appreciation … the ND legacy readings should move toward the carry line."* **That is BREACHED,
> and it is breached in the opposite direction.** The legacy ND instrument moves **−7.73% → −18.01%**
> (ALL picks 1–64) and **−15.92% → −20.93%** (picks 1–20), and **picks 21–64 crosses from no-arb
> (+4.76%) into ARB (−13.56%)**. **Arbitrages: 2 of 10 → 3 of 10.**
>
> **The mechanism is measured, not guessed** (`o29b_noarb_why.py`, §B3): **the cohort instruments'
> year-0 is not the printed day-0 price at all.** `emit_matrix_338.py:252` writes
> `v0 = round(v0_start(p), 1)` — the frozen year-zero *surface* value — while years 1…7 are `ev(p, Y)`.
> ORDER 29B wires `ev()`. So the denominator is **byte-identical across the two matrices (0 of 2648
> rows moved)** and the entire move sits in the numerator. P29B-26 assumed the instrument read the
> print as its yr0; it does not. **The prediction was wrong about the plumbing, and the reading is
> published as it came out. Nothing was tuned and no literal was re-pointed to make it look better.**
>
> **The all-arm deciding instrument stays no-arb in both windows** (+20.75% / +18.11%), and **reverse
> no-arb still passes 10 of 10**. What breaks is the **mark-path progression: 10/10 → 6/10** (§B5).

---

## B0. NO RE-POINT WAS NEEDED — P29B-24 HELD

ORDER 29's §12.3 halted on three literals and §13 re-pointed them. **ORDER 29B re-points nothing.**

| literal | ORDER 29's re-pointed value | ORDER 29B matrix carries | verdict |
|---|---|---|---|
| `EXPECT_STORE` | `cb38ef11` | `cb38ef11` | **holds — the store does not move** |
| `EXPECT_V0SURF` | `4405cba2b42f` | `4405cba2b42f` | **holds — no re-bake; the curve payload is untouched** |
| `EXPECT_N` | `1200` | `1200` | **holds — the teaching population does not change** |

`noarb_table_338.py` md5 **`0f8220351c64c56ccfa90c60edcdfa5f`**, computed at run, byte-identical.
The instruments used are ORDER 29's disclosed copies under `noarb/`, copied into a scratch run
directory and **not modified by this act in any way**.

**The live-basis control still reproduces `NOARB_MARGINS_V2` to the last digit** (PRIMARY +33.23%,
MODERN +31.75%, ND +6.70% / +1.82% / +14.04%, **0 arbitrages**) — run on the *pre*-re-point copies
under `composition_2026-08-10/noarb/`, because ORDER 29's copies are pinned to the landed store and
correctly **refuse** the live matrix. That refusal is printed in `NOARB_MARGINS_29B_out.txt` rather
than hidden. The pipeline, the runner and this seat are sound.

## B1. THE MATRIX

| | |
|---|---|
| `per_entrant_O29B.json` | **`ca24a49a`** · 24 as-of years · 1m 46s |
| basis | store **`cb38ef11`** (unmoved) · engine head **`a353a9d3`** · artifact **`911774bc`** · board **`36d5dfc7`** · v0surf **`4405cba2`** (unmoved) · `frozen=True` |
| population | **2648** records · ND 1–64 teaching **1447** · ruled pool **1201** — all identical to ORDER 29's emit |
| emitter | `emit_matrix_338.py` md5 `bffde2f7`, **copied, never modified** |

## B2. THE READINGS — LIVE vs ORDER 29 vs ORDER 29B

**All-arm deciding instrument** (`noarb_table_allarm.py`):

| window | LIVE `88ce647f` | ORDER 29 `86c8d5d9` | **ORDER 29B `36d5dfc7`** | verdict 29B |
|---|---:|---:|---:|---|
| PRIMARY 2005–2023 (n 2215) apprec 0→1 | −19.23% | −14.71% | **−6.75%** | |
| PRIMARY margin vs 14% | **+33.23%** | **+28.71%** | **+20.75%** | no arb |
| MODERN 2019–2023 (n 540) apprec 0→1 | −17.75% | −12.66% | **−4.11%** | |
| MODERN margin vs 14% | **+31.75%** | **+26.66%** | **+18.11%** | no arb |

**Legacy retained instrument** (`noarb_table_338.py`, UNMODIFIED):

| group | LIVE | ORDER 29 | **ORDER 29B** | verdict 29B |
|---|---:|---:|---:|---|
| ALL picks 1–64 · apprec 0→1 | +7.30% | +21.73% | **+32.01%** | |
| ALL picks 1–64 · margin | **+6.70%** | **−7.73%** ARB | **−18.01%** | **ARB** |
| picks 1–20 · apprec 0→1 | +12.18% | +29.92% | **+34.93%** | |
| picks 1–20 · margin | **+1.82%** | **−15.92%** ARB | **−20.93%** | **ARB** |
| picks 21–64 · apprec 0→1 | −0.04% | +9.24% | **+27.56%** | |
| picks 21–64 · margin | **+14.04%** | **+4.76%** | **−13.56%** | **ARB — NEW** |

**ARBITRAGES OPENED ON THE 29B BASIS: 3 of 10 readings** (ORDER 29: 2 of 10; live: 0 of 10).

## B3. WHY — THE MECHANISM, MEASURED ON THE TWO MATRICES

`o29b_noarb_why.py` · `NOARB_WHY_29B_out.txt` · `NOARB_WHY_29B.json`.

| | |
|---|---|
| rows whose `v0` (the yr0 **denominator**) moved | **0 of 2648 — BYTE-IDENTICAL** |
| in-curve ND Σ `v0` before → after | 1,707,328 → **1,707,328** |
| in-curve ND Σ year-1 mark (the **numerator**) before → after | 1,533,377 → **1,690,071**, **+10.22%** |
| in-curve ND year-1 marks that moved | **1,194 of 2,259 (52.9%)** |

Where the numerator moved, by cohort year:

| cohort year | cells | moved | % | Σ delta |
|---:|---:|---:|---:|---:|
| 1 | 2,630 | 1,434 | 54.5% | **+170,584** |
| 2 | 2,490 | 892 | 35.8% | +145,880 |
| 3 | 1,674 | 129 | 7.7% | +31,174 |
| 4 | 1,399 | 31 | 2.2% | +7,048 |
| 5 | 1,180 | 15 | 1.3% | +2,221 |
| 6 | 998 | 7 | 0.7% | +752 |
| 7 | 862 | 3 | 0.3% | +345 |
| ≥8 | 740 | 0 | 0.0% | 0 |

2,277 cells rose, 234 fell.

**In one sentence: the denominator is fixed and the numerator rose, so the appreciation had to rise.**
A day-0 print is a property of a player *at an as-of year*. On a national-draft cohort the printed
day-0 is overwhelmingly a **year-1** cell — a draftee who did not play his first season — never the
year-0 cell, which the instruments take from the frozen surface. So the act pushes years 1–2 up and
leaves year 0 exactly where it was.

**The honest reading of that: the day-0 gap P12 sized has been closed at day 0 and TRANSFERRED to the
yr0→yr1 step.** The year-1+ marks are still produced by the un-rewired legs. Closing the entry gap
without the year-1+ rewire does not remove the arbitrage; it moves it, and makes it bigger where it
now sits. That is a finding about the landed board's **interim** state, and it is a merge consideration.

## B4. AN OWED DECISION THIS SEAT WILL NOT TAKE ON ITS OWN

The wiring keys on **games as of Y**, which is why it reaches the historical matrix at all. The
alternative — keying on **career-total** games — is a one-line change and would leave every matrix cell
except the 89 current entrants untouched, so **all of §B2 and §B5 would read exactly as ORDER 29 did**.

**This seat did not switch to it after seeing the reading. That would be tuning, and PREREG_29B
forbids it by name.** The as-of predicate was declared in P29B-7 *before* any wiring was written, and
it was declared because the brief itself asked for the yr0 denominator to move "wherever the
instrument reads printed day-0". The measurement then found that the instruments **do not** read the
print at yr0 — so the premise that chose the predicate turned out to be false about the plumbing.
**The owner owes a word on which predicate the day-0 print should carry.** Both readings are on the
table above; neither was suppressed.

## B5. MARK-PATH PROGRESSION AND REVERSE NO-ARB, ON THE ENTRY-WIRED BOARD

`o29b_instruments.py` is `o29_instruments.py` (md5 `83e2fadb`) with **exactly one basis substitution** —
the matrix path — and nothing else (`INSTRUMENTS29B_REBASIS.diff`). **The denominator is NOT
substituted and must not be:** it is the derived day-0 (shipped ladder for ND, DERIVE28 cells ×
anchor_factor for pool), which is precisely the object ORDER 29B has now wired to the print. This act
does not move these instruments' denominator; it makes the engine agree with it.

| instrument | ORDER 29 | **ORDER 29B** |
|---|---|---|
| mark-path progression | **10 of 10 PASS** | **6 of 10 PASS — P29B-27 BREACHED** |
| reverse no-arb | 10 of 10 PASS · 0 fail | **10 of 10 PASS · 0 fail — HELD** |

**The four arms that flip, and why**, with their peak depth (the predicate is `peak at d ≥ 2` and
`some d ≥ 2 above base` — carried verbatim, not touched):

| arm | ORDER 29 peak (at d) | **ORDER 29B peak (at d)** | verdict |
|---|---|---|---|
| `RD` | 1.4660 @ **d3** | **1.6446 @ d1** | **FAIL** |
| `PDN` | 1.5228 @ **d5** | **1.7091 @ d1** | **FAIL [THIN]** |
| `PDS` | 1.3118 @ **d4** | **1.3856 @ d0** | **FAIL [THIN]** |
| `ND>64` | 1.5181 @ **d6** | **1.5493 @ d1** | **FAIL** |
| `ND 1-64` | 1.5653 @ d3 | 1.5706 @ d3 | PASS |
| `SSP` · `MSD` · `IRE` · `PDA` · `UNR` | — | peaks unchanged in depth | PASS |

**No arm's peak VALUE fell. Every one of the four rose.** They fail because the *shallow* marks rose
further — the same mechanism as §B3 — so the path peaks immediately instead of progressing. The
predicate is about SHAPE, and the entry wiring changed the shape by lifting d0/d1.

Reverse no-arb is unaffected because its predicate is a **level** test (`max m(d≥1) ≥ 1`), and every
arm clears it by a printed margin — the smallest `max m(d≥1)` is MSD **1.2379**, 24% above the line.

**A correction to Part A's §12.4.1, measured.** ORDER 29 reported the landed marks as *lower at
essentially every arm and depth* (shallow −0.0332, deep −0.0815) and concluded ORDER 28's read was
"optimistic, not conservative". On the entry-wired marks the shape **inverts**: shallow **+0.2134**,
deep **−0.0747**, and ORDER 28's original prediction — higher shallow, unchanged/lower deep — now
reads **CONFIRMED**. Both numbers are real; they are measurements of two different boards, and both
are recorded rather than one being quietly replaced.

## B6. PROVENANCE

| file | what |
|---|---|
| `run_noarb_o29b.sh` · `NOARB_MARGINS_29B_out.txt` | both cohort instruments: the 29B matrix, ORDER 29's, and the live control |
| `noarb29b/MARGINS_O29B.{txt,json}` | the canonical margins reporter, three variants: **3 of 10 ARB on 29B** |
| `noarb29b/t338_O29BFINAL.txt` · `noarb29b/allarm_O29BFINAL.{txt,json}` | the raw 29B readings, both instruments |
| `o29b_noarb_why.py` · `NOARB_WHY_29B.{json,_out.txt}` | the mechanism: the denominator does not move, the numerator does |
| `o29b_instruments.py` · `INSTRUMENTS29B.{json,_out.txt}` · `INSTRUMENTS29B_REBASIS.diff` | mark-path + reverse no-arb on the entry-wired board |
| `o29b_day0.py` · `DAY0_29B_{ENTRY,FINAL}.{json,_out.txt}` | the printed-day-0 identity, 0/89 → 89/89 |
