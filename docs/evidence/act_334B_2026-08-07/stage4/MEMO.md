# STAGE 4 — DESIGN MEMO: the pedigree-conditioned evidence bar

Branch `landing/334-stage-b`, baseline `c0ea507` (stage 3). Nothing merges to main; no PR; no tag.

## The owner's words, and what they ask for

> "I think it's good that the engine is reactive to players breaking out. This just seems extreme from a
> small sample, especially when there's no real 'pedigree' to make it feel more reliable. You'd be more
> inclined to buy into it based on a year 1 performance of a top 5 draft pick. But a 30s draft pick who
> didn't debut until year 2? I feel like that's more likely to be an outlier/purple patch/small sample?"

Three separable claims: (1) reactivity is GOOD and stays; (2) the EVIDENCE BAR for an upward re-rate
should scale with prior expectation; (3) a year-1 sit-out LOWERS the prior, it never preserves it.
Nothing here caps a breakout, narrows a band, or touches the 1.40 target.

## 1. THE INVESTIGATION — how a 4-game breakout actually re-rates

Traced on the stage-3 engine before anything was designed, using Noah Mraz as the calibration case
(KPD, ND pick 35 (2024), route debut year 2025, year-1 sit-out, one season: 2026, 4 games @ 84.25).

The candidate sites in the directive were each measured, and **four of the five turn out not to be the
site**:

| candidate | Mraz's value | does it carry the re-rate? |
|---|---|---|
| `_ev_qual(p,2026)` = E_q | **0.001720** | no. A 4-game season scores ~0 on the soft 10-game qualifying bar (logistic centre 11.0, width 1.1). |
| `_ev_rec(E_q)` (recency trust Lo→Lc) | **9.78e-06** | no — inert at this evidence level. |
| `_ev_pw(E_q)` (pedigree-PAR weight, residual r=0.11) | **9.77e-06** | no. The pedigree-par blend is gated to ~0 for the unqualified; it is not what is holding or releasing him. |
| L1c `_ycred_mult` (RL_YOUNG expected-re-rating credit) | **1.2754** | it lifts him, but it is a pedigree-CONDITIONED credit already, keyed on log-pick and the played/sat cell. It is not the pedigree-blind site. |
| `#336` resolution ramp `r(g*)` (stage-1 reference layer) | — | reads best-season games; not on the price path for a `ns==0` player. |
| **`sitout_ev` — the anchor/demonstrated blend** | **lam = 0.693727** | **YES. This is the site.** |

`ev()` routes every player with **no season at or above the prorated 6-game bar** into one line
(`_merged_recover.py`, the `ns==0` arm):

```
sitout_ev(p,Y,e_full) = (1-lam)*R*entry_anchor(p) + lam*e_full
lam = interp(min(games_this_season / fE, 6), [0..6], LAM_SIT)
```

For Mraz at a season 88% elapsed: 4 games = **4.55 at pace**, so **lam = 0.6937**. His price is
**69.4% the demonstrated-production path** (`e_full` = 5068.48) and 30.6% the decayed draft-day anchor
(`R × V0` = 0.45877 × 461.25 = 211.61). Blend = 3580.95, and after M3 the board carried him at **3358**.

**`lam` is THE site where demonstrated evidence overrides the pedigree anchor for a thin record, and it
was pedigree-BLIND.** Four games at pace bought the same 0.694 override at pick 1 and at pick 35, after a
straight debut and after a year-1 sit-out. That is exactly the asymmetry the owner describes, in one
number.

## 2. THE DESIGN

```
lam_eff = lam ** (1 + PED_BAR * (1 - q))
q       = ped(pick) * sit(depth)
ped(pk) = 1 - log(clip(pk,1,90)) / log(90)
sit(p)  = R(cls, pk, tau) / R(cls, pk, tau0)      tau0 = the SAME clock with the sit-out depth removed
```

**Conditioning an existing weight, not adding machinery.** `lam` is untouched as an object; it is raised
to a power. `ped` is the engine's own log-pick pedigree axis with the engine's own `[1,90]` clamp, taken
verbatim off the `_R_surf` call one line above — the same axis `R_SURF`, the L1c kernel and the V0
`star()` lookup all read pedigree on. `sit` is a ratio of the engine's own **already-computed** D13 ASK3
retention surface. **No new constant is introduced anywhere.** One dial, one four-line helper.

**Continuous everywhere (L-SMOOTH).** The exponent form fixes both endpoints — `0**e == 0` and
`1**e == 1` — so `lam(0)=0` and the graduation continuity `lam(prorated bar)=1` (Luke 2b: "no cliff, no
game-6 jackpot") survive **at every pedigree, by construction rather than by measurement**. Continuous
and monotone in games, in pick and in depth. No threshold, no counter, no branch, no band.

**Monotone in pedigree.** `q` rises with pedigree → the exponent falls → `lam_eff` rises. The same record
re-rates faster at pick 3 than at pick 35. Measured, §(c) of `PROBES.md`: the pure-pedigree ratio
(pick 3 / pick 35, straight debut, everything else held) widens **1.2247 → 1.3580**.

**A sit-out lowers the prior, and cannot preserve it.** `sit <= 1` is a **theorem** of the signed
isotonic-non-increasing-in-depth law ("a sitter never gains value"), not a clamp: `tau >= tau0` always,
so `R(tau) <= R(tau0)`. A straight debutant has `tau == tau0` and `sit == 1` **exactly** — he is judged
on pedigree alone. Mraz's sit-out costs him `sit = 0.6566`, which is the engine's own measured price of
the year he did not play, not a number chosen here.

**Established players are untouched by construction, not by tuning.** `sitout_ev` has exactly one caller:
the `ns==0` arm of `ev()`. A resolved player (`r=1`, a ≥6-game season) never reaches it. A thin-record
player with zero games this season has `lam == 0` and `0**e == 0`. Measured: of the 165 players on the
sit-out path, **109 have zero 2026 games and are byte-exact**; of 804 board rows, **51 move (6.34%)** and
**every one of them is on the sit-out path**.

**Symmetric, deliberately.** A thin record BELOW its anchor is the same small sample as one above it, so
a low-pedigree player whose few games went badly is likewise held nearer his anchor and moves UP. This is
the owner's own standing **L-SYMMETRY** law (register item 108: *"you should have to have the same drop
for the engine to think you're declining as a rise for it to think you're rising"*), and a one-sided
`max()` would be a BRANCH, refused under L-SMOOTH. **10 of the 51 movers move up**; all ten are named in
`MOVERS_FULL.txt` rather than hidden. This is the one place where the change does something the owner
did not literally ask for, and it is flagged here as such.

## 3. THE DIAL, and why 0.5

**`PED_BAR = 0.5`. One dial. `RL_PED_BAR=0` reproduces the stage-3 board byte-exact** (proven: 2650/2650
real rows identical, `qc_base` vs `qc_off`).

The exponent is "how many passes of the existing `lam` ramp this record must clear". The family's natural
unit is **1.0** — *with no prior expectation at all, the same record must clear the bar TWICE* — and that
is the only value with an independent motivation. It lands Mraz at −25.4%.

The owner's standing calibration word for adjacent machinery is **SLIGHT** (`RL_YCRED_KPF=0.92`, "slight
speculative-KPF trim"; the KPF rebalance T3). So the dial lands at **HALF the natural unit**: half a pass
more evidence at zero prior expectation, none at pick 1. What that buys, measured:

| PED_BAR | Mraz (engine ev) | worst mover | board total |
|---|---|---|---|
| 0.00 | 3534 (byte-exact base) | — | 0.0000% |
| 0.25 | 3235 (−8.5%) | −10.8% | −0.114% |
| **0.50 (SHIPPED)** | **3050 (−13.7%)** | **−17.4%** | **−0.181%** |
| 0.75 | 2834 (−19.8%) | −24.0% | −0.258% |
| 1.00 (the natural unit) | 2636 (−25.4%) | −29.4% | −0.326% |

At 0.5 the board moves **−0.18%** in total and the mean absolute move board-wide is **0.43%** — slight by
any reading — while the calibration case moves enough to be visible in a side-by-side. The side-by-side is
where the owner judges; the dial is one number and one edit away in either direction.

## 4. FIT COUPLING — the verdict is NO, and it is measured

See `FIT_COUPLING.md`. `sitout_ev` has one caller, `ev()`; `_build_v0_curve` fits `_v0_raw` (= `raw_ev ×
iso` at draft age) over the ND roster and never calls `ev()`. So `RL_PED_BAR` is **not** a `_V0SURF_GATES`
key and **no refit is owed**.

Proven by measurement rather than by reading, three-sided. A **declared refit** (`RL_V0SURF_REFIT=1`,
`refit_v0surf.py --verify`) was run at `PED_BAR` **0.0 / 0.5 / 2.0**. All three produced the identical
config signature `3e8e50de5103` and byte-identical fitted surfaces, md5
`9713ec6c83270ab916bb4a5e3ded6cb3` — **which is the CURRENT committed pin**. That single run does double
duty: it re-verifies the fit class against the current pickle on this box (the directive's precondition),
and it proves the dial cannot move the surface even at four times the shipped magnitude.

`v0surf` is therefore **UNMOVED** and the pickle was not rewritten.

## 5. What was NOT done

* No era anything. Nothing in this stage reads or writes an era table; the LAW holds.
* The 1.40 target untouched — no ladder, no curve, no numéraire, no `pvc_curve_v2.json`, no re-anchor.
* `rl_model.py`, `engine/forward_valuation/`, the store, the band, `q97m`, the entrant seal, the
  release-pick-curve contract: all UNTOUCHED. One engine file moves.
* The band check is REPORTED, never retuned. Stage 4 left the whole-cohort peak at **1.4322** (stage 3:
  1.4324) — inside `[1.35, 1.45]` and marginally closer to 1.40. Nothing was tuned to achieve that.
