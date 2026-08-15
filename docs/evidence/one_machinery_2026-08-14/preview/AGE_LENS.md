# THE AGE-WITHIN-GAMES LENS — the owner's 36-early-vs-36-late question, answered off the committed table

**ORDER 30B-P · `land/order-29` · 2026-08-15 · READ-ONLY · NOTHING IS APPLIED.**
Source: the committed 30B-M state table `docs/evidence/pedigree_persistence_2026-08-14/PERSISTENCE_TABLE.json`
(`cells_all_states`, **1,378 cells over 4,033 states / 767 careers**). Harness: `o30bp_agelens.py`.
Raw output: `AGE_LENS_out.txt`. Machine-readable: `AGE_LENS.json`.

> **PRE-NUMERAIRE.** This lens is a re-cut of a measured table, not a price; it does not depend on the
> numéraire and it does not move one. **Nothing here is wired.**

---

## 1 · THE QUESTION, AND WHAT THE COMMITTED TABLE CAN ACTUALLY ANSWER

The owner's question: **does a 20-year-old at 36 games keep more pedigree than a 23-year-old at 36 games?**

**What the table cannot do, stated before any number.** `σ` in the packet is a **regression** quantity —
`β_v0 × mean_v0 / mean_R`, fitted on the 4,033-state panel with a 300-replicate player-cluster bootstrap.
**The panel is not in the committed artifact; only the aggregated cells are.** So σ itself **cannot be
re-fitted per age group from this file**, and this lens does not pretend otherwise.

**What the table can do.** The cells carry the packet's own **model-free** instrument: the **cell-matched
pick contrast** — high picks (bands A 1–6, B 7–12) minus low picks (D 21–40, E 41–64), matched inside
`position × output-quintile` strata so output and position are held. That is the instrument that produced
the packet's §2.1 band row (+159 / +849 / +273 / +127 / +201). This lens re-cuts **that** by age.

**The share-scaled column, and its declared assumption.**
`σ̂(band, age) = σ_published(band) × Δ_matched(band, age) / Δ_matched(band, all ages)`.
It assumes **σ is proportional to the matched pick gap within a band**. The assumption is declared, it is
the only bridge from cells to a share, and **the verdict below does not depend on it** — the verdict is
read off the raw matched contrasts.

**The age bins.** The committed table bins age-at-state as `≤19 / 20 / 21 / 22–23 / 24–26 / 27+`. **The
brief's example split (≤20 / 21–22 / 23+) cannot be cut exactly, because 22 and 23 are pooled in the
committed artifact.** The lens uses the table's own granularity, collapsed to **≤20 / 21 / 22–23 / 24+**.
Disclosed, not fudged.

---

## 2 · GAMES BAND 16–35 — published σ **0.3313** (90% CI 0.2079 … 0.4562; n 834 states, 571 clusters)

All ages pooled: matched pick contrast **+306.0 pts** over 26 strata (weight 190, SD 415, SE 112).

| age at state | cells | n | mean R6 | median R6 | IQR | zero % | strata | **matched Δ** | SE | σ̂ | ratio to all-ages |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **≤20** | 133 | 324 | 873.4 | 778.8 | 573.3 | 0.3% | 20 | **+362.7** | 119 | **0.393** | 1.19 |
| 21 | 83 | 203 | 505.3 | 415.8 | 406.9 | 5.4% | 17 | **−88.7** | 111 | −0.096 | −0.29 |
| 22–23 | 83 | 225 | 349.2 | 267.2 | 273.1 | 19.1% | 15 | **−261.6** | 228 | −0.283 | −0.86 |
| **24+** | 50 | 82 | 149.6 | 144.4 | 15.5 | 37.8% | 4 | **−170.2** | 175 | −0.184 | −0.56 |

## 3 · GAMES BAND 36–70 — published σ **0.1645** (90% CI 0.0590 … 0.2804; n 887 states, 436 clusters)

All ages pooled: matched pick contrast **+379.5 pts** over 27 strata (weight 226, SD 521, SE 135).

| age at state | cells | n | mean R6 | median R6 | IQR | zero % | strata | **matched Δ** | SE | σ̂ | ratio to all-ages |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **≤20** | 51 | 84 | 1567.9 | 1564.4 | 617.7 | 0.0% | 10 | **+98.5** | 404 | 0.043 | 0.26 |
| 21 | 83 | 189 | 1320.8 | 1255.3 | 836.7 | 0.5% | 18 | **+235.8** | 229 | 0.102 | 0.62 |
| 22–23 | 111 | 387 | 737.8 | 658.2 | 518.8 | 3.6% | 23 | **+51.2** | 147 | 0.022 | 0.13 |
| **24+** | 103 | 227 | 410.8 | 354.4 | 319.5 | 17.6% | 12 | **−187.7** | 269 | −0.081 | −0.49 |

---

## 4 · THE DECIDING COMPARISONS

| band | ≤20 matched Δ | 24+ matched Δ | **difference** | 90% interval | z | separated from zero? |
|---|---:|---:|---:|---|---:|---|
| **16–35** | **+362.7** (SE 119, n 324) | **−170.2** (SE 175, n 82) | **+532.9** | **[+184.2, +881.7]** | **+2.51** | **YES** |
| 36–70 | +98.5 (SE 404, n 84) | −187.7 (SE 269, n 227) | +286.2 | [−512.7, +1085.0] | +0.59 | **NO** |

---

## 5 · THE VERDICT

**AT 16–35 GAMES, AGE-AT-STATE MOVES THE PICK GAP — AND IT MOVES IT A LONG WAY. AT 36–70 GAMES IT DOES
NOT SEPARATE.**

- At **16–35 games** the young cell's matched pick gap is **+362.7** and the 24+ cell's is **−170.2** — not
  merely smaller, **the sign flips**. Share-scaled, that is **σ̂ ≈ 0.39 for a ≤20-year-old against σ̂ ≈ −0.18
  for a 24+-year-old**, against a published all-ages band σ of 0.331. **The owner's intuition is supported
  at this depth: a 20-year-old at 25 games is carrying most of the band's pedigree, and an older player at
  the same games count is carrying none of it.**
- At **36–70 games** — the band kako's 36 games sits in — the difference is **+286.2 with a 90% interval
  that spans zero**. **On the owner's own example (36 early vs 36 late) the table does not separate them.**
  The monotone drop across the ages there (98.5 → 235.8 → 51.2 → −187.7) is not even ordered.

**THREE THINGS THAT MUST TRAVEL WITH THAT VERDICT.**

1. **This interval is NOT cluster-robust, and the packet's are.** The committed cells do not carry player
   identity, so the SE here is a strata-level weighted dispersion, not the packet's 300-replicate
   player-cluster bootstrap. **It is therefore too narrow.** Read the 16–35 separation as a **signal flag**,
   not as a measurement of the same standing as §2 of the packet.
2. **Age and games are confounded at fixed games, and the confound has a name.** A 24-year-old sitting at
   16–35 career games is, by construction, a player who has *not* made it — the same selection the fade's
   depth-4 kink was ruled on, running the other way. The 24+ cell in the 16–35 band is **n = 82 over only
   4 matched strata, with a 37.8% zero share and an IQR of 15.5**: it is a small, degenerate, almost
   uniformly-failed population. The sign flip may be that population, not an age law.
3. **Mean R6 falls hard with age at fixed games (873 → 505 → 349 → 150 in the 16–35 band).** That is
   *mostly the horizon effect the packet already named* (a remaining-value target declines with age for
   arithmetic reasons). The matched contrast holds age constant inside each row and is therefore the right
   instrument — but the levels in the table must not be read as an age law.

---

## 6 · THE WIRING IMPLICATION — STATED AS AN **OWED WORD**, NOT APPLIED

**Nothing in this order applies an age term.** The preview board `6a392bca` carries `σ(g)` as a function of
**games alone**, exactly as the 30B-M refit was fitted.

If the owner wants the signal pursued, the implication is precise and is stated so it can be ruled:

> **The share curve would become `σ(g, a)` — an age term inside the pedigree weight, biting in the 16–35
> games band and expiring by 36–70.** In price terms it would *raise* the pedigree leg of a young
> established player and *cut* the pedigree leg of an older player at the same games count.

**The seat does not recommend wiring it on this evidence**, and says why in one line: the deciding interval
is not cluster-robust, the separating cell is n = 82 over 4 strata, and the owner's own example band
(36–70) **does not separate**. What it *does* recommend, if the owner wants it settled: **its own order,
its own prereg, a re-fit of σ on the panel with age in the model and the packet's cluster bootstrap** —
the same discipline 30B-M held itself to. That is a measurement, not a wiring act, and it is the owner's
call whether it is worth one.
