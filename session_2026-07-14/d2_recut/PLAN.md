# D2 RE-CUT — PLAN

**Tier 3, READ-ONLY.** Board of record `9f8ae76` (v2.9 tag): store **`b0c39d78`**, board `81e48293`,
engine `2030e5df`. New files only under `session_2026-07-14/d2_recut/`. Simulate, do not wire.
Propose no lever. No bake, no tag, no merge.

## What carries forward (verified, do not redo)
D2's construction is sound and REPRODUCES on the board of record (store md5 `b0c39d78` asserted):
age-controlled diff-in-diff vs **14,698** continuous transitions; overall **−3.42 SC [−4.84, −1.95]**;
young 18–24 **−4.94**, prime 25–28 **−1.07 (CI spans 0)**, older 29+ −3.32; 109 absent-from-base
players; 0 explicit `games==0` rows (absence = year-gap). The measurement stands. Three things change
(R1/R2/R3) and two are added (R4/R5).

## R1 — additive vs multiplicative (form of the effect vs pre-absence level)
Per matched returner event I hold `(age_pre, pre_avg, effect)` where `effect = Δavg − age-expected Δavg`.
- **Additive test:** regress `effect` (points) on `pre_avg`. Additive ⟺ slope ≈ 0 (flat in points).
- **Multiplicative test:** regress `effect/pre_avg` (percent) on `pre_avg`. Multiplicative ⟺ slope ≈ 0.
- Report both slopes with bootstrap 95% CIs. **Also the age-partial slope** (`effect ~ age + pre_avg`)
  because age and level are correlated (young = low avg) — separate the form from the R2 age gradient.
- STATE WHICH FORM THE DATA SUPPORTS, and note the convexity consequence (a flat point haircut hits
  low-average players' *value* hardest because `ev(level)` is convex at the replacement bar).

## R2 — smooth curve in age (replaces the 3 bins; CORE rule 7)
Nadaraya–Watson / local-linear kernel smoother of `effect` on `age_pre`, evaluated at 18,19,…,34, with
a bootstrap confidence ribbon (resample events, refit). Bandwidth declared. Report the curve; test for a
U-shape (developmental loss young → ~0 prime → aging loss old). Where a slice is genuinely unsupported
(old tail), pool deliberately and declare it (rule 7). No wide bins as one number.

## R3 — what the recency decay ALREADY charges, vs the truth
The engine already docks absence: a year-gap ages the last good season an extra `k` years of decay
`ld^(Y−yr)` inside `_lvlcurr`. For every returner:
- Rebuild `_lvlcurr(p, Y)` **with** the gap (actual) and **without** the extra decay (pre-absence
  seasons' recency exponent reduced by the gap length `k`). Δlevel = the recency charge in points.
- Convert to SCAR by re-pricing via `ev()` with `_lvlcurr` patched to the no-gap form for that player.
- Compare the charge, player by player, against the **measured truth** from R1/R2 (the effect the data
  says the absence is worth at his age/level). Report **UNDER / OVER / RIGHT**, by how much, and
  **whether the error varies with age** (decay is group- not age-keyed; if the truth is age-shaped the
  engine over-charges prime and under-charges young — measure, don't assume).

## R4 — the four phantom boards (owner-proposed mechanism; TEST, do not wire)
Insert **one** phantom game-row in the missed season and re-price the whole affected board via `ev()`.
Four phantom averages:
1. `avg = 0`
2. `avg = replacement bar` (`MA.REPL[pos]`)
3. `avg = pre-absence level + effect` (signed effect < 0 ⇒ level − |penalty|; the **data-implied**
   candidate, R1/R2)
4. `avg = pre-absence level` (the null: absence costs nothing)

For each board: how many players move, by how much; **Jamarra** (2025 gap); the **A-anchors**
(Bontempelli/Gawn/Daicos/Sheezel/Reid — expected inert, they have no gap ⇒ confirms the phantom is
surgical); the **G-COHORT** (affected young cohort, board-side aggregate; the binding walk-forward gate
recompute is declared out of Tier-3 scope). Deep-copies only; the store is never written.

## R5 — historical vs future absences (REPORT, do not design)
Read `LTI_REGISTER.md` and trace its consumers in code: what the LTI register currently holds; what
reads it (the availability layer — **is it read into the LEVEL at all?** state plainly); and what a
cause-conditioned phantom average WOULD need from it. Scope only. Build nothing.

## Method / fences
- Reuse the prior harness (`harness.py` execs `_merged_recover.py` against `/tmp/bor_ws`, store
  `b0c39d78`). All perturbations on in-memory deep-copies / temporary function patches; restored after.
- Board md5 named beside every figure. No store/engine/board/gate/docs/pricing/λ/trust-basis writes.
- `boot_guard.py` / `bootstrap.sh` / `_merged_recover.py` NOT touched (the q97m writer lives there).
