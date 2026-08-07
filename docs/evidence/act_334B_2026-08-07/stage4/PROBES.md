# STAGE 4 — THE PROBES (b) MRAZ · (c) THE PEDIGREE PAIR · (d) THE BOUNDARY DiD

Raw output: `probes_stage4.txt` / `probes_stage3.txt` (+ `.json`), `boundary_stage4.txt` /
`boundary_stage3.txt`. Instruments: `probes.py`, `boundary_did.py`.

**Method.** The counterfactual pattern is carried from
`docs/evidence/act_336_variant_2026-08-06/` (`seam_boundary.py`): hold ONE player fixed, vary ONE
property, price both, difference the differences. That file's two recorded traps are honoured — every
copy is HELD alive (`_PE_CACHE` keys on `id(p)`, and a freed copy's address gets reused) and
`MA._pe_clear()` runs before every price.

**Two disclosures that materially changed the answers, recorded rather than quietly fixed:**

1. `v0_start` reads the FROZEN `_V0CURVE`, prebuilt only for actual roster members. A counterfactual with
   a changed pick MISSES it and silently falls back to the unfrozen `_v0_raw` — a different ruler from the
   board's, on exactly the anchor these probes compare. Each counterfactual's curve entry is therefore
   INSTALLED from the engine's own frozen `star(pos, ageR, pick)`, the same function the board's own
   entries were written from.
2. **The first cut of the pedigree pair was INERT** and said pick 3 == pick 35 to the point.
   `MA.effpk(p)` reads the load-time cached `_eff` FIRST (`rl_model.py:214`) and only falls back to
   `pick`, so setting `pick` alone left the engine reading the ORIGINAL pedigree. `_eff`, `_pool`,
   `stream_pick`, `_eyr`, `stream_year`, `_by` and `_bd` are now all moved with the property being
   varied. A probe that returns "no effect" because it never varied anything is the most dangerous
   possible result, and it is named here so the next seat looks for it.

---

## (b) THE MRAZ PROBE

**Noah Mraz — KPD, ND pick 35 (2024), route debut year 2025, year-1 sit-out, one season: 2026, 4 games
@ 84.25.**

| | stage 3 | **stage 4** |
|---|---|---|
| **board price** | **3358** | **2898** (−460, **−13.70%**) |
| engine `ev()` | 3534 | **3050** |
| draft-day anchor `V0` | 461.25 | 461.25 (unmoved) |
| retention at depth `tau=1.826` | 0.45877 | 0.45877 (unmoved) |
| anchor leg `R × V0` | 211.61 | 211.61 (unmoved) |
| production path `e_full` | 5068.48 | 5068.48 (unmoved) |
| **`lam`** | **0.693727** | **0.592552** |

**The path, in two sentences.** At a season 88% elapsed the prorated establishment bar is 5.28 raw games,
so Mraz's four games leave him just short of it and `ev()` routes him into the thin-record blend
`(1-lam)·R·V0 + lam·e_full`, where four games at pace 4.55 bought `lam = 0.6937` — 69% of his price taken
straight from a four-game production estimate, at pick 35, after a year he did not play. Stage 4 leaves
every input untouched and conditions only that weight: `ped(35) = 0.2099` times the engine's own measured
cost of his sit-out `sit = 0.6566` gives a prior expectation `q = 0.1378`, hence an exponent of 1.4311
and `lam = 0.5926` — the anchor holds a larger share for longer, and his price falls 13.7% while the
breakout itself is still fully expressible.

---

## (c) THE PEDIGREE PAIR

One record — one season, 4 games @ 84.25, KPD, age/position matched to Mraz — priced under four entry
histories. The full 2×2 (`pick {3,35}` × `{straight year-1 debut, year-1 sit-out}`) is run rather than
just the requested three, so the pedigree effect and the sit-out effect are separately readable.

Two holds are reported, because there is no confound-free one: a player who sat a year IS a year older
now, and a player drafted a year later at the same current age WAS drafted a year older. **DRAFT-AGE HELD
is the primary**, because it makes the year-zero anchor `star(pos, draft-age, pick)` differ ONLY by pick,
which is the contrast the owner's question is about.

### PRIMARY — DRAFT-AGE HELD

| arm | stage 3 | **stage 4** | move |
|---|---|---|---|
| **(i) pick 3, straight year-1 debut** | 4801 | **4666** | −2.8% |
| **(ii) pick 35, year-1 sit-out** *(= Mraz-shaped)* | 3534 | **3050** | −13.7% |
| **(iii) pick 3, year-1 sit-out** | 4184 | **3947** | −5.7% |
| (iv) pick 35, straight year-1 debut | 3920 | **3436** | −12.3% |

| contrast | stage 3 | **stage 4** | |
|---|---|---|---|
| **GAP (i) − (ii)** | **+1267** | **+1616** | |
| **RATIO (i) / (ii)** | **1.3585** | **1.5298** | **← THE OWNER'S JUDGMENT NUMBER** |
| pure pedigree, straight debut (i)/(iv) | 1.2247 | **1.3580** | pedigree matters more |
| pure pedigree, after a sit-out (iii)/(ii) | 1.1839 | **1.2941** | pedigree matters more |
| pure sit-out at pick 3 (iii)/(i) | 0.8715 | **0.8459** | sitting costs more |
| pure sit-out at pick 35 (ii)/(iv) | 0.9015 | **0.8877** | sitting costs more |

### SECONDARY — AS-OF-AGE HELD (all four arms age 20 in 2026)

| arm | stage 3 | **stage 4** |
|---|---|---|
| (i) pick 3, straight year-1 debut | 4165 | **4058** |
| (ii) pick 35, year-1 sit-out | 3534 | **3050** |
| (iii) pick 3, year-1 sit-out | 4184 | **3947** |
| (iv) pick 35, straight year-1 debut | 3486 | **3062** |
| **GAP (i) − (ii)** | **+631** | **+1008** |
| **RATIO (i) / (ii)** | **1.1786** | **1.3305** |

**Reading.** Both holds say the same thing in the same direction: the identical record is now worth
materially more to a top-5 pick than to a pick-35 sit-out than it was, and the sit-out itself costs more
at both picks. The top-5 arm barely moves (−2.8%) — *"high-pedigree breakouts re-rate roughly as today"*
holds, because `ped(3) = 0.756` leaves an exponent of only 1.12. The change is one-directional in the
sense that matters: it does not make anybody's breakout believed FASTER than before, it makes the
low-pedigree breakout believed more slowly.

---

## (d) THE BOUNDARY DiD — no new cliff at the establishment bar

**The integer 5g → 6g step is not a cliff test and must not be read as one.** At `fE = 0.88` the prorated
bar sits at **5.28 raw games**, so 5 raw games (5.68 at pace) is BELOW the bar and 6 raw games (6.82 at
pace) is ABOVE it. That step straddles the bar and contains three things at once — the tail of the `lam`
ramp, the crossing itself, and the ordinary growth of `e_full` with an extra game. It does grow under the
change (Mraz +550 → +672), and that growth is the ramp being reshaped BELOW the bar, which is the
intended effect.

**The cliff test is the one-sided limit AT the bar**, `6−ε` vs `6+ε` at pace. `lam(6) = 1` and `1**e == 1`
for every exponent, so the conditioning is INERT exactly at the bar and the jump must be unchanged.
Measured at `ε = 1e-4` raw games:

| probe | pick | stage-3 jump at the bar | **stage-4 jump at the bar** | **SEAM RATIO** | price at the bar, s3 → s4 |
|---|---|---|---|---|---|
| Noah Mraz | 35 | +1 (+0.0189%) | **+1 (+0.0189%)** | **1.000** | 5291 → 5291 (identical) |
| Josh Smillie | 7 | +0 | **+0** | **1.000** | 2460 → 2460 (identical) |
| Charlie West | 50 | +0 | **+0** | **1.000** | 4387 → 4387 (identical) |
| Samuel Swadling | 37 | +0 | **+0** | **1.000** | 2326 → 2326 (identical) |

**SEAM RATIO ≈ 1 on all four, exactly.** The prices AT the bar are byte-identical across the change on
every probe — which is the proof stated as strongly as it can be stated: at the establishment bar this
change does literally nothing, so it cannot have put a cliff there. Mraz's `+1` is integer rounding of a
sub-point difference and is the SAME `+1` on both builds.

**The placebo, taken well away from the bar (3 games at pace), where the mechanism IS live** — a
cliff-free change must show ratio ≈ 1 at the seam and movement at the placebo, and it does:

| probe | stage-3 price at 3-at-pace | **stage-4** | move |
|---|---|---|---|
| Noah Mraz | 1347 | **1088** | −19.2% |
| Josh Smillie | 1471 | **1394** | −5.2% |
| Charlie West | 1043 | **814** | −22.0% |
| Samuel Swadling | 828 | **748** | −9.7% |

The effect is entirely in the ramp and exactly zero at the seam. The fine sweeps (raw games 3..8, in
`probes_*.txt`) show the crossing is monotone and smooth on both builds.
