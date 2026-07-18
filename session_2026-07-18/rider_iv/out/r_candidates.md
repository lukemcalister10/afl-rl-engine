# Rider (iv) — three R candidates + uncertainty on R  (REPORT-ONLY / DO-NOT-MERGE)

_stamps: pin=a90052ad curve_payload=89c14729 store_base=968de0c7 per_entrant=40d7da7c (five-migration head; read-only; asserted at load, HALT-on-mismatch)_

> **Axes note.** production bars and list-space R are orthogonal (R107.7); v2.11 bakes GROSS either way; making v-R the traded currency is the named post-v2.11 chapter, on the owner's word.

Symmetric: three candidates, **no verdict, no steer** — the reading is the owner's at the ladder.

Pick-equivalents (free-intake entry): {'IRE': 92, 'MSD': 90, 'PDA': 92, 'PDN': 92, 'PDS': 92, 'SSP': 92, 'UNR': 92}

## Headline (findings, not verdicts)

| candidate | value | what it is | grade |
|---|---:|---|---|
| **R_curve** | **470.8** | v2 list curve at the free-pool entry pick (90/92) | 39.79% uncertainty @pk90 (rider-iii; ~2.16x the 17.35% top) |
| **R_realized** | **207.5** | realised value the free pool actually delivers (evidence-weighted, busts full weight, no cutoff) | bootstrap rel-SD 10.9% (thin) |
| **R_owner** | **220** | owner's stated prior (item 332), reference line only | asserted, not measured |

The three span **220–470.8**: the v2 list curve prices the free-pool entry ~2.3x the realised outcomes; R_owner and R_realized sit close.

## (a) R_curve — circularity note, TESTED not assumed

- Directive expectation: the v2 deep tail was partly anchored on pickless pk90 outcomes -> R_curve self-referential.
- **Finding: REFUTED under this construction.** Mechanism rows in the curve's `load_pool`: **0** (all 389 mechanism entrants have `incurve=False`). The pk86-94 region is anchored by real-pick {'RD': 109, 'ND': 9}. R_curve at pk90/92 is **not** self-referential on pickless outcomes.

## (b) R_realized — per mechanism (thin; read as bands)

| mech | pick-eq | n | played | R_realized | boot median [16,84] | rel-SD |
|---|---:|---:|---:|---:|---|---:|
| MSD | 90 | 106 | 64 | 273.0 | 267.8 [208.0, 338.5] | 24.9% |
| SSP | 92 | 52 | 36 | 339.6 | 332.1 [251.2, 427.2] | 27.1% |
| IRE | 92 | 57 | 8 | 160.6 | 157.3 [122.5, 196.8] | 24.2% |
| UNR | 92 | 59 | 7 | 131.5 | 131.4 [102.4, 161.7] | 22.7% |
| PDA | 92 | 51 | 12 | 266.0 | 259.5 [202.4, 324.3] | 24.3% |
| PDN | 92 | 43 | 5 | 125.7 | 123.7 [97.1, 154.7] | 23.7% |
| PDS | 92 | 21 | 1 | 90.5 | 89.9 [60.4, 121.4] | 33.6% |
| **POOL** | 90-92 | 389 | — | **207.5** | 206.7 [184.4, 229.2] | 10.9% |

**Era-matching cross-read (national cohorts, same entry region/era):**
- ND realised @ pk88-94 (reading-B, what the equivalent pick delivers): **247.5** (n=7; curve says 474.0).
- ND realised @ pk88-94, same era 2003-2026: 247.5 (n=7).
- The free-pool R_realized (207.5) and the era-matched ND-at-entry realised (247.5) bracket the owner's 220, and all three sit far below the v2 list value (470.8).

## (c) R_owner

- **220**, item 332 — carried as a labelled reference line only; not fitted, not fed to any computation.

## Uncertainty grade per candidate (job 2)

- **R_curve**: rider-(iii) curve uncertainty at the entry pick = 39.79% (@pk90), 39.65% (@pk92) — ~2.16x the 17.35% top reference. The free-pool entry is in the curve's low-confidence deep tail.
- **R_realized**: cohort-bootstrap (seed 20260718, B=5000) pooled rel-SD **10.9%**; per-mechanism rel-SD [24.9, 27.1, 24.2, 22.7, 24.3, 23.7, 33.6]. Thin cohorts.
- **R_owner**: a prior — no sampling uncertainty; graded *asserted, not measured*.

> **Thin-sample declaration.** MSD 44/17 played, SSP 31/16 (engine cohort); IRE/UNR/PDA/PDN/PDS 5-12 played. Said on every artifact.
