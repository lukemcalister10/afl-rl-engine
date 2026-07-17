# MEMO — LEG D: THE PVC RE-DERIVATION, THE CONSTRUCTION (owner-readable)

**Read this first, then rule.** ACT 1 is read-only measurement; nothing here is fitted, nothing is
wired. Every number is script-emitted into a committed artifact under `legd_derivation/out/`, re-run on
THIS base (store `968de0c7`) and reconciled against the groundwork (`9845180`, store `0efdc5d6`) —
**20/21 headline fields byte-identical; the base change moved nothing structural** (only three per-band
mean-peak values by ≤1 SCAR). So the groundwork's ground holds here. This memo asks you to rule three
things: **the construction**, **the G-Y0 tolerance number**, and **the fence question** (does the new
curve reach the `rl_model.py` consumers, or stay the clean ev-channel swap).

---

## 1. WHAT WE ARE RE-DERIVING, AND WHY (the measured problem)

The PVC is built from each drafted player's **end-of-calendar-year-1 as-of value** (the anchor,
`s4_matrix_7147.py:62`) — a season of evidence, your correction, confirmed by the code. Two cracks the
groundwork measured, both reproduced here:

- **The entry tautology (Job 2):** **1093 of 2083** in-curve entrants (52%) have played **zero** senior
  games by end-of-year-1, so their anchor IS the pick prior read straight back out (the pure V0 pole).
  It worsens with depth — 9.5% at picks 1–3 → 66.9% at picks 49–99.
- **The survivor tail is invisible (Job 3):** the anchor is a single year-1 snapshot; the good players
  roughly **double by peak** (peak/anchor **1.69 → 2.66**, U-shaped in ratio, largest in *dollars* at
  the top), and the year-1 photo credits none of it. The **MEDIAN** smoother flattens what little the
  anchor carries. So the curve **underpays picks**, most in dollars at the top, most in proportion in
  the middle.

Busts ARE already included (they get their low year-1 pole; nobody is dropped) — keep that true.

---

## 2. THE DERIVATION CONSTRUCTION — options weighed with THIS base's numbers

All three groundwork cuts, re-measured here (`out/job2_circularity.json`):

| option | rule | what it keeps / drops | the symmetric case |
|--------|------|----------------------|--------------------|
| **A — drop the poles** | exclude the 1093 zero-evidence anchors | drops 52% of the pool (worst in the tail, where the sample is largest) | **For:** kills the circle at entry, cleanest tautology removal. **Against:** the poles are floor-*informative* (they price the cheap tail); dropping them thins the tail sample brutally and is a **hard gate** (a threshold) — against L-SMOOTH / weight-don't-gate. |
| **B — honest end (yr4)** | re-anchor at end-of-yr4, keep only the **531** with ≥2 qualifying seasons | keeps survivors, drops 1552 washouts | **For:** prior fully faded → an independent curve. **Against:** **survivorship bias** — an all-survivor anchor OVER-prices picks (survivors peak 2.5–2.7×); it breaks "include busts" and is also a **hard gate**. This is the opposite failure to today's. |
| **C — two ends** | entry end = pick pricing for the 1093 poles (no loop); evidence end = the 531 survivors' production; **PVC = the line between** | drops nobody | **For:** the only option that keeps busts (their low poles pull the entry end down), removes the pure tautology (the evidence end is prior-faded and independent), AND preserves G-Y0 at entry (the entry end IS the day-after pricing). **Against:** needs a ruled blend weight between the two ends, and a definition for the evidence end. |

### RECOMMENDATION — **C (two-ends), built as a CONTINUOUS evidence-weighted blend, not a hard-cut**
A and B are both **gates** (they delete rows on a threshold). The binding **weight-don't-gate** (R105.4)
and **L-SMOOTH** ("every transition a curve, no threshold in the construction") laws point away from
deleting the 1093 or the 1552 and toward **weighting** every entrant continuously by its demonstrated
evidence:

- **Entry end** = the day-after pole pricing (dominant where evidence is thin — the 1093 poles carry
  full weight here, so the cheap tail stays anchored and busts stay in).
- **Evidence end** = realised production, up-weighted continuously by faded-prior share (the engine's own
  `pw = _ev_pw`, 1.0 at zero evidence fading to 0.11) — no season-count threshold; a player with one
  qualifying season contributes partially, not zero-or-all.
- **PVC(pick)** = the pick-resolved blend of the two ends, **at the finest resolution the sample
  supports** (per-pick, kernel-smoothed — picks 1–20 sit at ~21 samples each; the tail thins), with the
  standard bands carried **presentation-only** (CORE rule 7; `out/job4c_sample_counts.json`).

**The survivor tail (Job 3):** the evidence end should read the **life-path**, not the single year-1
cross-section, so the convex tail is credited. Because you have flagged that "peak? a window across the
peak? it's arbitrary," I propose a **bounded window** (mean over a fixed post-peak-onset window), NOT raw
peak — and the smoother must NOT be the current MEDIAN kernel, which flattens exactly this tail; a
mean/kernel blend that preserves convexity is the fix. This is a design knob for your pen.

*(If you prefer a simpler ruling: C with a hard 531/1093 split is implementable, but it re-introduces a
threshold and I'd advise against it on your own smoothness doctrine.)*

---

## 3. DESIGN CONSTRAINTS (binding — restated and honoured by the plan)

- **Finest resolution, smoothed; wide bins presentation-only** (CORE rule 7). Per-pick derivation, kernel
  smoother; bands for display only.
- **NO THRESHOLD in the construction** (L-SMOOTH) — hence the weighted blend, not a cut.
- **Weight-don't-gate** (R105.4) — evidence up-weights, never gates out.
- **Offline-derived, STAMPED, LOADED — no new import-time fit.** The new curve is computed by an offline
  script into a stamped artifact (md5 of store+code+config), then **loaded** — exactly as the shipped
  `pvc_curve_L1b.json` is loaded at `_merged_recover.py:1336-1339`, never refit at import. **The
  `_iso_dec`/`_fit_pick_curve` import-time chain (`:1121-1170`) is the V0-curve (G-Y0 gate) instrument,
  a DIFFERENT object; the new PVC path does not add to it and does not touch it.** (Details: `SITE_CENSUS.md`.)
- **Include busts** — the entry end carries the low poles; the current anchor already includes them, and
  the weighted-C construction keeps that true.

---

## 4. THE G-Y0 TOLERANCE PROPOSAL (the number is YOURS; here is the measured distribution)

The identity: **comp-weighted (position-mix) mean V0 per band == derived PVC per band**, population-level,
across drafts — *a single class off-curve is a weak/strong class, NOT a breach.* V0 is the value the day
AFTER the draft; the PVC is the pick's value the day before — one day apart, nothing to discount. The
retired "raise-young-side" remedy is history and is NOT wired.

**Measured signed residuals (mean V0 − shipped PVC) by pick decile** (`out/gy0_residuals.json`, base
`968de0c7`, pool 2082):

| decile | picks | n | mean V0 | mean PVC | signed resid | rel % | sd |
|--------|-------|---|---------|----------|--------------|-------|----|
| 1 | 1–10 | 208 | 2196 | 2247 | −50 | −1.6% | 883 |
| 2 | 11–21 | 208 | 1242 | 1320 | −78 | −6.2% | 301 |
| 3 | 21–31 | 208 | 894 | 920 | −26 | −2.8% | 174 |
| 4 | 31–41 | 208 | 742 | 752 | −11 | −1.6% | 132 |
| 5 | 41–51 | 209 | 623 | 581 | +42 | +8.5% | 137 |
| 6 | 51–61 | 208 | 553 | 390 | +162 | +42% | 127 |
| 7 | 61–72 | 208 | 531 | 345 | +187 | +54% | 147 |
| 8 | 72–85 | 208 | 503 | 342 | +161 | +47% | 169 |
| 9 | 85–99 | 208 | 470 | 335 | +134 | +40% | 246 |
| 10 | 99 | 209 | 455 | 334 | +121 | +36% | 199 |

**FINDING — the residual is sign-changing, not one-directional.** Against the *shipped L1b* curve the top
(picks 1–41) sits **slightly below** V0 (−1.6% to −6.2%) and the **deep tail (picks 51+) sits far below**
V0 (+36% to +54%), because the shipped curve floors flat at 334–343 while comp-weighted tail V0 is
455–553. **This is NOT the "V0 > PVC in every band" of the 2026-07-13 record** — two reasons: (a) that
record measured against the *derived PVC of the day*, before L1b adoption; (b) it used the **comp-weighted**
(position-mix) mean, mine is a raw entrant mean. **The ruled gate must use the comp-weighted mean against
the NEW curve; these residuals are the shape evidence, not the gate value.** The re-derivation (lifting
the tail, tracking V0) will collapse the +40–54% tail residuals — that is most of the current gap.

**Proposed tolerance — shape (yours to set the number):**
1. **Relative, per-decile, population-averaged across drafts.** Absolute SCAR residuals scale with pick
   value (top sd 883 vs tail 130), so a relative band is the honest unit.
2. **A single per-decile band** (e.g. **|mean signed residual| ≤ 8–10% per decile**, **~5% pooled**),
   measured on the comp-weighted mean after re-derivation — a *starting* number motivated by the residual
   spread above, **explicitly for you to rule up or down.**
3. **Wider allowance only where the sample earns it:** decile 1 (picks 1–10) carries sd 883 on small
   per-position n — its position mix swings honestly, so a slightly looser top band avoids penalising a
   legitimately strong/weak draft class (the positional caveat is part of the law).
4. Assertable by the job-5 harness **unchanged** — the harness already computes signed residuals by
   decile; only the numeric bound is injected at your ruling.

---

## 5. THE PICK-BAND WIRING PLAN

- **Held pick** = the LIVE re-derived curve evaluated over its ladder band **[low, high]**, taken as the
  **mean** across the band (you can supply band weights later; absent them, equal-weight mean).
- **2027 picks** = `live_curve(band) × (1 − discount)`, discounts **per-posture, EXACT**:
  **balanced 0.10 · contender 0.15 · rebuilder 0.05** — asserted byte-exact in every generated artifact
  (R104.5 / §6.3; `leg_d_placeholders.posture_2027_discounts`).
- No threshold in the band mapping; the curve is continuous, the band mean is a presentation aggregate.

---

## 6. PLANNED TESTS (enumerated, not yet run — ACT 2)

- **Multi-start** (audit #34/#35): re-derive from several kernel bandwidths / init seeds; **divergence
  between starts is a reported FINDING with numbers, not a silent pick.**
- **Prior-removed** (audit #44): re-derive with the 1093 pole entrants down-weighted to zero on the
  evidence end, to confirm the evidence-end shape does **not** depend on the circular poles (the entry
  end still uses them for the floor — that is by design, not circularity).
- Both committed with results in ACT 2.

---

## 7. A-PAIRS NOTE (never result-conditioned — L-AXIS)

Pair 3 (**Sanders / Bontempelli**) maps to this chapter. The acceptance diagnosis (guards A-PAIRS) places
pair 3's gap in the **base pick-band price × young-side growth** — i.e. exactly the PVC re-derivation —
and rules **NO HAND EDIT**: the derivation is NEVER conditioned on the pair result. It is scored at the
ladder against the v1.21 bands (pair 3: bont above sanders by 0–10%). **Expected direction only:** lifting
the young/tail pricing should move pair 3 *toward* the band; magnitude is measured at the ladder, not
targeted. Pair 3 is `OWNER_ON_SIGHT` — a pair-3 miss is not itself a bake blocker.

---

## 8. THE FENCE QUESTION (item-281 — I do NOT extend the fence myself; your call at the checkpoint)

The clean, in-fence design wires a new kill-switch **`RL_PVC2`** as an exact parallel of `RL_PVCADOPT`:
load the new stamped curve into `_PVC0` + rebuild the V0 guard/curve/RUC ceiling — all inside
`_merged_recover.py` + the artifact + the selftest. `RL_PVC2=0` reproduces the shipped board `9829d01a`
byte-exact. **But the census names live PVC consumers in `rl_model.py` (FENCE-OUT):** the pickless
`unpl_eq` (`:798`), the pedestal (`:813`), the `build_pvc_v34` import fit (`:714`), the `_natcv34`
pickless-inversion (`:834-853`), and the frozen peak-model feature `pvc_snapshot.json` (`:515`). These
read `MA.PVC` (the v3.4 ruler), which the L1b precedent leaves unswapped. **Recommendation:** the
fence-clean `_PVC0`-only swap (the held-pick ladder and G-Y0 gate both read the ev-channel basis).
**Ruling needed:** should the new curve also reach the `rl_model.py` `MA.PVC` consumers? If yes, that is a
fence extension and needs your word before ACT 2 touches `rl_model.py`.

---

## WHAT I NEED FROM YOU (the go for ACT 2)
1. **Construction:** C weighted-two-ends (my rec) · or A · or B · or C hard-split.
2. **G-Y0 tolerance number** (the per-decile relative band; I proposed ~8–10% per decile / ~5% pooled).
3. **Fence:** ev-channel-only swap (my rec) · or extend to the `rl_model.py` `MA.PVC` consumers.
4. **Version note (FYI):** the engine base carries `acceptance_v1_20.json`, not `v1_21`; the operative
   entries are all present and substance-identical (v1_20 overrides the stale G-Y0 fix_direction with
   `STALE_DO_NOT_APPLY` + the 2026-07-14 correction; v1_21's `RE_DERIVE_AT_LEG_D` formalises that). I
   assert against v1_20 and pre-view-hash it.
