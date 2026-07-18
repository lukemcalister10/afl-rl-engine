# FINDINGS — FORWARD-LENS CALIBRATION (item 351) · seat 13 · 2026-07-18 · READ-ONLY
**Findings, not verdicts. Nothing here gates, bakes, or fixes. Localizes by engine site (address, not fix).**
Probe: board `790136a3` (v2.10 head, store `b1fd0bce`) — same Leg-E/F lens family; see PLAN.md provenance note.
Cross-checked against F2 boards @ `cf94589` (−1 `771,152` / −2 `770,987` / now `752,427`).

---

## THE BACKTEST NUMBER FIRST (job 1 — decisive)
**The forward lens does NOT reproduce a flat recent past — it collapses it.**

- **(B) F2 actual −1 board projected forward one year through the lens → `526,851`** vs actual now
  **`752,427`** = **−225,576 (−30.0%) undershoot**. With an F1-scale phantom intake layer (~+80k)
  ≈ 607k — still **≈ −19%** short, and right on the directive's predicted "~620k smoking gun."
  −2 board → −1: reproduced `527,298` vs actual `771,152` = **−31.6%**.
- **(A) composition-controlled (identical 804 roster, zero membership change):**
  forward one year `Σv 725,590 → ΣvP1 532,870` = **−26.6%**, while the engine's OWN backward lens on
  the *same players* realized only `ΣvM1 797,633 → Σv 725,590` = **−9.0%**. A calibrated,
  L-SYMMETRIC lens would project ≈ `660,054` (−9%); it prints `532,870`. **Undershoot 127,184 (−17.5%).**
  Forward decline is **~3×** the backward decline on the identical roster — a pure shape asymmetry.

Independent corroboration: F2's realized −1→now survivor set ran ×1.106 (−9.6% for continuers), −2.4%
overall with real intake. The lens says −27%. **Backward flat, forward collapse ⇒ the lens
systematically under-projects. NOT calibrated.**

## JOB 2 — now→+1 DECOMPOSITION (owner's conservation model, tested) — THE DEFECT IS INVERTED
Σ(vP1 − v) by cohort:

| cohort | n | now Σv | +1 ΣvP1 | signed Δ | mean Δ | Δ% |
|---|--:|--:|--:|--:|--:|--:|
| **developing ≤23** | 375 | 340,003 | 226,830 | **−113,173** | −302 | **−33.3%** |
| mid 24–27 | 210 | 230,184 | 174,290 | −55,894 | −266 | −24.3% |
| **veteran ≥28** | 219 | 155,403 | 131,750 | −23,653 | −108 | **−15.2%** |
| exits (F1 filed) | 366 refilled | — | — | residual −32,338 | | |
| phantom intake (F1 filed net) | | | | +80,480 | | |

**The owner's conservation model FAILS exactly where he predicted it must hold.** Developing players
(who should HOLD OR RISE) fall **−33.3% — the STEEPEST cohort**, while veterans (who *should* decline
most) fall the LEAST (−15.2%). The lens has the age gradient backwards. The negative developing cohort
IS the defect (job-2(b), confirmed). Nick Daicos (age 23, pre-peak cornerstone): `8,049 → 6,880`
(−14.5%). No cohort is positive — the lens credits no net growth to anyone.

## JOB 3 — PEDIGREE-PREMIUM CARRY (the root) — CONFIRMED
Young, high-pick, low-games rows — the ones whose now-value is anchored on **pedigree (Leg-D V0)**, not
production — are **re-priced on thin production by the forward lens, stripping the premium:**

- young ≤23, pick ≤20, games ≤40 (n=119): now `110,738 → +1 69,158` = **−41,580 lost (−37.5%)**.
- this explains **36.7%** of the entire developing-cohort decline directly; broader young re-pricing the rest.

| player | age | pick | games | v (now) | vP1 (+1) | premium lost |
|---|--:|--:|--:|--:|--:|--:|
| Jagga Smith | 20 | 3 | 12 | 3,437 | 901 | −2,536 (−74%) |
| Willem Duursma | 19 | 1 | 12 | 4,328 | 3,093 | −1,235 |
| Sam Lalor | 20 | 1 | 18 | 3,299 | 2,071 | −1,228 |
| Taj Hotton | 20 | 12 | 7 | 1,642 | 511 | −1,131 (−69%) |
| Xavier Lindsay | 20 | 11 | 23 | 1,212 | 277 | −77% |

The now board holds these up on the pedigree blend (pedmix/pedDecay, Leg-D V0); the forward lens prices
purely on the projected production trajectory `lp·frac(age,peak)`, where `lp` for a thin-evidence pick
sits at the production floor — so the premium is not carried, and the runway credit that could restore
it is gated on being *already* elite (see localization). **This is the mechanism of the under-projection.**

## JOB 4 — DISTRIBUTED-RETIREMENT ALTERNATIVE (owner's steer) — THE EXIT SIDE IS MIS-STATED
Empirical P(retire|age) from F2 exits (age≥26 eligible, youth floored), per-player haircut P·v, no named exits:

| construction | +1 | +2 |
|---|--:|--:|
| **distributed retirement liability** (P·v over 320 eligible) | **32,836** | 65,484 |
| F1 discrete rule (exit if vP1 < X=207), gross value removed | 65,067 (359 exits) | — |
| F1 filed residual (net, after phantom refill) | 32,338 | 34,746 |

The distributed liability (**32,836**) lands almost exactly on F1's filed *net* residual (**32,338**) —
so in AGGREGATE the exit magnitude is roughly right. **The mis-statement is WHO exits, and it compounds
job 3:** because the discrete bar reads the *under-projected* vP1, **155 of the 359 "exits" (43%) are
developing players age ≤23** — 20-year-old top-15 picks (Patrick Retschko pick 9 `826→126`; Matthew
Jefferson pick 15 `567→130`; Harry Rowston pick 16). The model *retires* the future of the list. A
probabilistic haircut spread over the age-eligible cohort touches NONE of them. The discrete rule
gross-removes ~2× the probabilistic liability and mislocates it onto the developing cohort.

---

## VERDICT — one-paragraph read
**The forward decline is NOT calibrated; it is systematic under-projection concentrated in the
developing cohort (job 2b / job 3), with the discrete exit rule compounding it (job 4).** Backward is
flat because it re-renders *recorded* production; forward collapses because the lens re-prices the
pedigree-anchored young cohort on thin projected production and credits no growth — so the identical
roster declines 3× faster forward than backward, the developing cohort falls hardest (−33%) instead of
holding, and the under-projected values then trip a discrete exit bar that retires 20-year-old top
picks. The owner's conservation model is correct and the lens violates it. The decline is a lens
artifact, not a real forecast.

## LOCALIZATION (address, not fix — NO fix in this build)
1. **Under-projection / no-growth engine site:** `rl_model.py :: proj_from_peak` — the level path
   `lev = lp·frac(ag,pa)` with the pre-peak floor `if ag<=pa: lev=max(lev,cl)` prices forward purely
   on `lp` (the `cohort_peak`/`track_delta` production estimate, near the floor for low-games players),
   and the only young credit — `runway = clamp((25-a)/6,0,1) · elite · PMAX` with
   `elite = clamp((lp/PEAK-0.97)/0.30,0,1)` — is GATED on `lp` already being elite, so it fails for
   exactly the thin-evidence high-pick cohort. R103.3's "no lens-only growth term" removes the offset
   that would carry the pedigree premium.
2. **Where the pedigree premium lives (and is dropped):** the now board's pedigree blend
   (`pedmix`/`pedDecay`, the Leg-D V0 anchor) is present at k=0 but the forward form-anchor set at
   `rl_export.py :96` (R103.3: "the FORWARD lens sets the form anchor to true-now") re-prices on the
   production map without re-supplying that anchor at +k.
3. **Exit-mis-statement site:** `rl_export.py` LEG-F1 block (~`:526`, `_LF_X = 207`) — the discrete
   exit reads the under-projected forward value, so the pedigree-strip in (1)/(2) feeds it developing
   players as false retirees.

*Findings only. Nothing ruled, nothing fixed, balanced board untouched.*
