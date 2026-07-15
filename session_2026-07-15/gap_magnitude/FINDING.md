# GAP-LENGTH MAGNITUDE — MEASUREMENT (feeds parked R100.11 assumption 1)

**Register item 122b · Tier 3 READ-ONLY · 2026-07-15 · Fable supervisor seat**
**Base pin:** analysis at candidate line head `62352729ec3523cec4bb117e713e1bec67a0d490`
(branch `claude/absence-penalty-evidence-fade-glcl8b`). Store md5 `340a7a32` == Guard-5 pin.

> ⚠ **THIS PARKS THE ASSUMPTION FOR THE OWNER'S RULING.** It measures only. No recommendation, no
> wired fix, no touch to the fade construction. The two readings are laid out; the call is the owner's.

## THE QUESTION
R100.11 declared, unruled: *multiple / longer absences are charged **once**, on the most-recent
return, and are **NOT scaled by gap length** — should a three-year absence cost more than a one-year?
Intuitively yes; currently it does not.* **Does the DATA show longer absences produce larger
post-return level shortfalls?**

## METHOD (declared)
- **Population:** every store row with a detectable most-recent mid-career absence, using the shipped
  `_abs_gap` detector copied **verbatim** from the head's `_merged_recover.py` (a `games==0` year after
  ≥1 prior played season, return year ≤ 2026; the **most-recent** gap, exactly as the engine charges it).
- **Gap length** `glen = ret − last − 1` (missed seasons). **Buckets, pooled per CORE rule 7:** `1`,
  `2`, `3+` (the 3+ pool is thin and declared so — see below).
- **Shortfall** = pre-absence level − realised post-return level, games-weighted season averages
  (**positive = a realised drop**). Pre = up to the 2 most-recent pre-gap seasons; post = all
  post-return seasons.
- **Age control = the SHIPPED absence age-curve**, `_ABS_AGE`/`_ABS_EFF` (`_merged_recover.py:370–371`),
  via `_abs_frac`'s point magnitude `max(0,−eff)` at `age_pre` (`:383–388`). `resid = shortfall − pred`.
  The curve is keyed on `age_pre` (age at the last pre-gap season) exactly as the engine keys it.
- **Two views:** **ALL** detectable gaps (the directive's "every player", n=324); and **QUALIFIED**
  (both endpoints rest on a ≥6-game season, n=168) — the clean cut, because 156 rows have a sub-6-game
  cameo as one endpoint (e.g. Reilly O'Brien 2g@63 → full career; Mabior Chol 1g@10 → 63; a colliding
  1-game Harrison Jones row), which manufactures spurious ±40–50 pt "shortfalls" and clusters in the
  long-gap buckets. **The QUALIFIED view is the reliable one; ALL is shown for completeness.**

## (1) SHORTFALL BY GAP LENGTH — n, mean, 95% CI

| view | bucket | n | mean age_pre | raw shortfall (95% CI) | **age-adj resid (95% CI)** |
|------|:------:|--:|:---:|:---:|:---:|
| **QUALIFIED** | 1 | 144 | 23.8 | +0.47 [−1.80, +2.74] | **−3.88 [−6.09, −1.67]** |
| **QUALIFIED** | 2 | 16 | 22.6 | +5.81 [+0.68, +10.95] | **+1.02 [−3.77, +5.81]** |
| **QUALIFIED** | 3+ | 8 | 21.9 | −6.30 [−18.45, +5.84] | **−10.97 [−22.93, +0.99]** |
| ALL | 1 | 261 | 23.0 | −1.43 [−3.95, +1.10] | −5.29 [−7.75, −2.84] |
| ALL | 2 | 42 | 21.8 | +4.22 [−2.19, +10.64] | +0.62 [−5.57, +6.81] |
| ALL | 3+ | 21 | 21.7 | +0.65 [−7.88, +9.17] | −2.96 [−11.55, +5.64] |

Age composition barely moves across buckets (predicted penalty 4.35 / 4.79 / 4.67 pts in the qualified
view), so **the age control does almost nothing — the bucket differences are genuine gap-length
differences, not age artefacts.** Raw and age-adjusted orderings agree.

## (2) DO THE BUCKETS SEPARATE?  (verdict at stated confidence)

- **1 → 2 seasons: a real, marginal step UP.** Qualified 2-season absentees return **~+5.8 SC below**
  their pre-absence level vs **~0** for 1-season absentees; age-adjusted diff **+4.9 pts, one-sided
  p = 0.031** (ALL view: +5.9, one-sided p = 0.040). 13 of the 16 qualified 2-season players sit below
  their old level — a broad shift, not one outlier. **This is the only place the intuition finds
  support.**
- **1 → 3+ seasons: NO support, and it reverses.** 3+ does **not** exceed 1 at any conventional
  confidence — in the clean cut it trends the *other* way (3+ **below** 1; one-sided p for "3+ > 1"
  ≈ **0.88**; ALL view one-sided p ≈ 0.30, still nowhere near significance).
- **No monotone "longer = worse."** Spearman(glen, resid) = **+0.03, p = 0.72** (qualified);
  **+0.10, p = 0.08** (ALL). A monotone gap-length scaling is not supported by either view.

**The 3+ bucket is the crux and it is confounded.** n = 8 (qualified) / 21 (all), and it is dominated
by players whose pre-absence baseline was an immature-age season and who **matured during the gap**:
Menzel 61→69, Krakouer 50→69, McCartin 46→67, Wagner 57→69, Ryan Davis 50→65 — all `age_pre` 20–23,
all *improved*. The shipped age-curve (keyed on `age_pre`) does not remove this, because the confound is
the low starting baseline, not the return age. So the long-gap sample cannot distinguish a gap-length
effect from age-at-baseline and small-sample noise.

## (3) NAMED PLAYERS BY BUCKET
Full per-player table (all 324) in `gap_magnitude.json` → `records`; console dump in
`console_report.txt`. The load-bearing rows:

**Qualified bucket 2 (n=16, mean shortfall +5.8):** Nicholas Coffield 72→52 (+20) · Conor McKenna
76→58 (+18) · Sam Docherty 112→97 (+14) · Jaeger O'Meara 94→83 (+11) · Martin Clarke +11 · Nakia
Cockatoo +10 · Josh Thomas +10 · Samuel Reid +8 · Jonathon Marsh +7 · Caleb Marchbank +4 · Zac Dawson
+3 · Willie Rioli +2 · Lewis Stevenson −0.3 · Andy Otten −0.8 · Zachary Clarke −4 · Nicholas Holman
41→60 (−20, age 20, matured).

**Qualified bucket 3+ (n=8):** Lachlan Keeffe 62→50 (+13, g3) · Marty Hore 71→52 (+19, g4) — the only
two real shortfalls · then the maturers: Pfeiffer −8 · Menzel −8 · Wagner −12 · Ryan Davis −15 (g6) ·
Krakouer −19 · Paddy McCartin 46→67 (−21, g3).

**Bucket 1 headline movers (ALL):** biggest realised drops are washout/exit seasons — Dylan Roberton
85→26, Angus Monfries 65→7, Dom Tyson 77→23, Chris Knights 77→25, Michael Hurley 80→35, Jonathon Patton
79→35. The famous good-return case that motivated R100.11 — **Bailey Smith (2023→2025, g1): 88.8 → 118.7,
shortfall −29.9 (he returned well ABOVE his old level)** — sits in bucket 1's left tail, exactly as the
ruling anticipated.

## (4) FINDING — BOTH READINGS (the owner rules)

**READING A — "there is a magnitude, at short gaps."** Going from a 1-season to a 2-season absence
raises the realised post-return shortfall by ~5 SC, age-controlled, and this clears one-sided
significance (p ≈ 0.03–0.04) in both views on a broad (not outlier-driven) sample. A returner who
missed *two* seasons is, on average, genuinely below his pre-absence level where a one-season returner
is not. If the owner reads the question as "does *any* extra absence length cost more," the 1→2 step
says **yes, a little** — and a bounded, saturating length term (not a linear scale) would be the shape
the data suggests.

**READING B — "the data cannot support gap-length scaling, especially not 'a 3-year costs more than a
1-year.'"** The specific intuition in R100.11 — *three years worse than one* — is **not** in the data:
3+ absentees do not cost more than 1-season absentees (one-sided p ≈ 0.88 clean / 0.30 all), and no
monotone trend survives (Spearman p = 0.72 / 0.08). The 3+ evidence is thin (n = 8/21) and confounded
by maturation-during-gap (young baselines returning better). The one real signal (1→2) is marginal and
could equally be a single-season-vs-multi-season *threshold* rather than a *length scale*. On this
evidence the current build's "charge once, do not scale" is not refuted for long gaps, and any
length term would rest on the 1→2 step alone.

**What is NOT in dispute:** age composition does not explain the bucket differences (the age control is
near-inert here); and the largest realised shortfalls are concentrated in *exit/washout* returns
(bucket 1), which the evidence-fade already handles by construction — those are level facts, not
gap-length facts.

---
*Artifacts: `gap_magnitude.json` (full stats + all 324 records) · `console_report.txt` (readable dump) ·
`scripts/measure_gap_magnitude.py` (verbatim `_abs_gap` + shipped `_ABS_EFF` age control). No store,
engine, board or doc outside `session_2026-07-15/gap_magnitude/` was written or mutated.*
