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
