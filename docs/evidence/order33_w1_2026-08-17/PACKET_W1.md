# PACKET_W1 — ORDER 33 seat W1: the deep end of β, re-measured — and the honest answer about the S4 gap

**Read-only measurement seat · prereg = `PREREG_W1.md`, committed and pushed (96e6c1f) before any
result number existed; every estimator, the proposed-curve construction rule and all three
falsifiers were fixed there and none was changed after results.** Program brief: #334 comment
5312369107. Motivating evidence: Order 32 seat S4 (`docs/evidence/order32_s4_2026-08-17/`).

---

## 0 · HEADLINE — three sentences the build decision needs

1. **The deep end of β is now better measured**: pedigree persistence at ~40–70 career games is
   real and positive (identified with CIs clear of zero by two independent estimators), plausibly
   somewhat higher than the wired curve pays; past ~71 games it is genuinely indistinguishable from
   zero in every estimator tried — the added power did not manufacture identification, and the
   achieved bound is reported (§2).
2. **But wiring a deeper β does NOT close the S4 years-4–6 gap.** The preregistered counterfactual
   — the wired 53-knot raised 54% to its monotone cap, re-emitted through the full walk-forward and
   rescored by S4's own prereg-bound shootout — recovers a **median 0%** of the old law's years-4–6
   rank-skill edge. Every S4 verdict, in all 280 cells, is unchanged. **P3 is falsified.**
3. Therefore: **do not spend the ORDER A build's budget expecting "deeper β" to fix years 4–6.**
   The additive pedigree channel is saturated (§5); the defect lives elsewhere in the pedigree leg —
   the named candidates are the Φ deep zero-floor, the D/unplayed-clock channel, and the old law's
   production-side machinery (§5). This packet's proposed curve is published (§3) but on this
   evidence the seat recommends **holding it for ORDER A's joint re-derivation, not wiring it now**.

---

## 1 · Prereg discipline and the control (P1)

* `PREREG_W1.md` pushed before any measurement (estimators E1–E4, curve construction rule,
  falsifiers P1–P3, counterfactual controls — all pre-committed).
* **P1 PASS at deviation 0.0**: the 31-F β derivation (`o30bm_measure.py`, md5
  `e910fe64…`, run whole with the 31-F head-fix substitutions, outputs repointed) reproduces all
  five BETA_31F band coefficients, n and cluster counts **exactly** (`CONTROL_W1.json`,
  `w1_control.py`). Every measurement below stands on the estimator that produced the wired curve.

## 2 · The deep end, re-measured (estimators fixed in prereg §3)

**E1 — finer bands, harness `band_fit` verbatim, primary H=6 panel** (n=4,033 states / 767 careers;
"wired@mid" = the wired curve read at the band midpoint):

| band | mid g | n | clusters | β̂ | se | t | wired@mid |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0-5 | 2.5 | 382 | 332 | 0.2879 | 0.0786 | 3.66 | 0.2879 |
| 6-15 | 10.5 | 591 | 467 | 0.3561 | 0.0640 | 5.56 | 0.2879 |
| 16-35 | 25.5 | 834 | 571 | 0.2177 | 0.0531 | 4.10 | 0.2177 |
| 36-50 | 43.0 | 446 | 370 | **0.1671** | 0.0741 | **2.26** | 0.1601 |
| 51-70 | 60.5 | 441 | 355 | 0.1041 | 0.0785 | 1.33 | 0.0865 |
| 71-90 | 80.5 | 351 | 284 | 0.0152 | 0.0815 | 0.19 | 0.0298 |
| 91-120 | 105.5 | 357 | 231 | −0.0235 | 0.0659 | −0.36 | 0.0238 |
| 121+ | 164.8 | 631 | 172 | 0.0723 | 0.0637 | 1.14 | 0.0238 |

**E2 — pooled-power H=4 panel** (adds state-years 2020–21; 4,969 states / 889 careers; robustness
only, disclosed horizon departure): same shape — 36-50 → 0.1346 (t 2.66), 51-70 → 0.0683 (t 1.28),
71-90 → 0.0252 (t 0.37), 91-120 → −0.0048, 121+ → 0.0463 (t 1.15). The pooled 31-F deep bands on
H=4: 36-70 → 0.1074 (t 2.41), **71+ → 0.0313 (t 1.04)** — still spanning zero even with ~35% more
states and 350 clusters.

**E3 — PRIMARY: joint monotone-constrained fit** (v0 × log-g hat basis at the wired knots, shared
controls + fine-band dummies, one regression on the whole H=6 panel; player-cluster bootstrap
B=400 seed 33):

| knot g | β̂ | CR0 se | boot 90% CI | CI excl. 0? | wired |
|---:|---:|---:|---|---|---:|
| 2.5 | 0.1843 | 0.0854 | [+0.037, +0.325] | YES | 0.2879 |
| 10.5 | 0.2541 | 0.0650 | [+0.156, +0.365] | YES | 0.2879 |
| 25.5 | 0.2940 | 0.0594 | [+0.202, +0.406] | YES | 0.2177 |
| **53.0** | **0.2439** | 0.0705 | **[+0.133, +0.356]** | **YES** | 0.1416 |
| **85.5** | **0.0152** | 0.0474 | **[−0.050, +0.111]** | **no** | 0.0238 |

**E4 — deep-local level + slope (g≥36)**: β(53) = 0.1753 (t 2.79) on H=6, 0.1436 (t 3.46) on H=4;
log-slope −0.19/−0.14 (t ≈ −2.8/−3.5) vs the wired 53→85.5 log-slope −0.246. Implied β(85.5)
≈ 0.078–0.085.

**What is and is not identified (P2 reading, honest):**
* The **53-knot is identified**: positive with CIs clear of zero in E3 ([+0.133, +0.356]) and E4
  (t 2.8–3.5). E3's point (0.2439) sits well above the wired 0.1416 — but its CI **contains** the
  wired value, and the local band fits (E1/E2: 0.10–0.17 in 36-70) sit **at or below** the wired
  curve. So "deep-mid pedigree is real" is proven; "the wired 53-knot is too low" is suggested by
  the joint estimator only, and is NOT proven at 90%.
* The **71+ region is unidentified everywhere**: E1 71-90 → t 0.19; 91-120 → t −0.36; 121+ →
  t 1.14; E2 pooled 71+ → t 1.04; E3 85.5-knot CI [−0.050, +0.111]. The achieved 90% CI width at
  85.5 is ~0.16 — the added power (finer bands, pooled eras via H=4, joint borrowing) shrank
  nothing decisively. **The bound stands: with this store (767–889 careers), β beyond ~71 games
  cannot be told from zero, nor from ~0.10.** No identification was manufactured (prereg P2
  falsifier honored in part: the 71+ prediction did NOT hold — E1 71-90 landed *below* its wired
  interpolation, not above).

## 3 · The proposed curve (prereg §4 construction rule, executed verbatim)

Shallow knots wired (S4 shows the candidate winning years 1–3; not this seat's mandate), deep knots
from E3 capped by monotonicity at β(25.5), 0-floored:

| knot g | WIRED (31-F) | PROPOSED (W1) | status |
|---:|---:|---:|---|
| 2.5 | 0.2879 | 0.2879 | shallow — kept |
| 10.5 | 0.2879 | 0.2879 | shallow — kept |
| 25.5 | 0.2177 | 0.2177 | shallow — kept |
| 53.0 | 0.1416 | **0.2177** | E3 0.2439 capped at β(25.5); knot identified vs zero, not vs wired |
| 85.5 | 0.0238 | **0.0152** | E3 point; **unidentified** — prior-consistent only |

Interpolation rule unchanged (`_o31_loglin`, log-linear). Note the shape this rule produces — flat
0.2177 across 25.5→53, then the full fade to 85.5 — is the *monotone cap binding*, i.e. E3 actually
wanted the curve to **rise** into mid-career (0.294 at 25.5 → 0.244 at 53 measured pre-projection);
the brief's standing "π decays in g" ruling deletes that rise exactly as it deleted the 2.5→10.5
rise in 31-F, and the deletion is disclosed here the same way.

**Recommendation: do not wire on this evidence** — not because the deep-mid signal is fake (it
isn't; §2), but because the counterfactual (§4) shows the revision buys nothing where the owner
needs it, and the 85.5 leg would be wired on noise. If ORDER A wants a deeper β component, these
knots are the measured starting point, re-derived on its own tree (§7).

## 4 · The counterfactual — what the S4 years-4–6 cells do under the proposed curve

Pipeline (all prereg §5): the ORDER 31-F emitter run whole from a scratch worktree of THIS tree
(engine `71d9949a` — byte-identical to the O31FFINAL emit engine) with exactly one substitution,
the `O31_BETA` tuple → the proposed curve (site asserted unique, md5s printed, `EMIT_W1CF_out.txt`);
then S4's `s4_shootout.py` exec'd whole (B=2000, seed 32, same verdict rule) with `CAND_P` →
`per_entrant_W1CF.json` (`c5c7719a`).

**Controls — all PASS** (`RECOVERY_W1_out.txt`): day-0 replication guard 89/89 at tolerance 0;
day-0 `v0` identical 2648/2648; all 1,201 pool rows byte-identical; all 597 ND careers with ≤25
games byte-identical (the curve is unchanged on g≤25.5 by construction); `rho_old` unchanged in
every scored cell; pool-cell candidate skill unchanged. Movement that did happen: 4,516 of 9,566
non-pool vpath entries changed, mean +0.6, max |Δ| 198.7 board points.

**Primary ND cells (M1 Spearman; Δ>0 favours the candidate machine):**

| N | horizon | n | ρ old law | ρ cand (wired) | ρ cand (W1 curve) | S4 verdict | W1 verdict | recovery |
|---|---|---:|---:|---:|---:|---|---|---:|
| 1 | next | 1201 | 0.485 | 0.570 | 0.570 | CANDIDATE | CANDIDATE | −0% |
| 1 | rest | 1201 | 0.528 | 0.576 | 0.576 | CANDIDATE | CANDIDATE | −0% |
| 2 | next | 1137 | 0.626 | 0.668 | 0.668 | CANDIDATE | CANDIDATE | −0% |
| 2 | rest | 1137 | 0.643 | 0.677 | 0.677 | CANDIDATE | CANDIDATE | −0% |
| 3 | next | 955 | 0.665 | 0.677 | 0.677 | tie | tie | −3% |
| 3 | rest | 955 | 0.692 | 0.689 | 0.689 | tie | tie | +4% |
| 4 | next | 807 | 0.701 | 0.681 | 0.681 | OLD LAW | OLD LAW | −1% |
| 4 | rest | 807 | 0.751 | 0.729 | 0.728 | OLD LAW | OLD LAW | −0% |
| 5 | next | 680 | 0.718 | 0.704 | 0.703 | OLD LAW | OLD LAW | −3% |
| 5 | rest | 680 | 0.765 | 0.748 | 0.748 | OLD LAW | OLD LAW | −1% |
| 6 | next | 574 | 0.733 | 0.726 | 0.726 | OLD LAW | OLD LAW | +3% |
| 6 | rest | 574 | 0.801 | 0.791 | 0.791 | OLD LAW | OLD LAW | +0% |

**Median recovery over the six old-law-won primary M1 cells: 0%** (range −3% to +3% — noise).
Years 1–3 candidate wins all retained (the do-no-harm half of P3 holds). Verdict tallies over ALL
280 scored cells: S4 {candidate 72, tie 173, old law 35} → W1CF {**identical: 72 / 173 / 35**}.
**P3 (≥50% median recovery) is FALSIFIED**, per the prereg's own words: *the deep β is NOT the
mechanism behind the S4 years-4–6 result.*

## 5 · Why the additive channel cannot close the gap — and what can

* The counterfactual raised the pedigree top-up at g≈53 by **54%** (the monotone cap; more than any
  measured estimate would justify) and rank skill at years 4–6 moved by ≤0.003 Spearman. The
  channel is **saturated**: the top-up `Φ·β·ρ·v0` adds a v0-monotone shift *within* cohorts, and S4
  itself measured frozen-v0-alone at ρ ≈ 0.30–0.34 at years 4–6 while both machines sit at
  0.70–0.80 — pushing more weight onto v0 moves the candidate *toward* 0.33, not toward the old
  law's 0.75. No admissible β level fixes that; the S4 gap is not a β-magnitude defect.
* **Named candidates for closing it** (prereg §4.4, plus one observation from the wired law's own
  constants — no new measurements claimed):
  1. **The Φ deep zero-floor.** `O31_PHIST` is 0.0 at the 53 and 85.5 knots: a mid-career player
     with a current stall run of ≥2 seasons has his ENTIRE pedigree top-up deleted. The old law
     never deletes pedigree. If pedigree still predicts for mid-career stallers (S4 §4 says
     pedigree alone predicts everyone at ρ~0.3), this is exactly where the candidate would misrank
     at years 4–6 — and it is ORDER A's own territory (delivered-season reset, age-referenced
     stall bars all reshape `s`).
  2. **The D / unplayed-clock channel** — the pedigree leg's other multiplier `D(c_u)·(1−ρ)`,
     re-measured under ORDER A's sitter-fade changes.
  3. **The production leg / old-law carry**: the old law's years-4–6 edge may be production-side
     (its P̂-equivalent machinery), i.e. not in the pedigree leg at all. S4's identification (§1
     caveat there) already flagged that the Step-2 intermediate law was never scored; that
     comparison would localise it.

## 6 · Named rows — the proposed curve on the current board (`cand31.json`, 561 non-pool rows)

Repricing by the law's own algebra `Δ = ρ·Φ·(β_new−β_old)·v0`, β-field cross-checked to 1e-9 on
all rows, and validated against the counterfactual emit's own 2026 prices (direction and relative
size exact; a uniform ×1.053 board→engine currency factor, `_PL_F`, separates the rulers —
`RECOVERY_W1.json` / `xcheck`). 78 rows move up >0.5pt (Σ +781), 201 move down >0.5pt (Σ −1,631)
on a 552k board — a **net −0.15% board-level move**. The winners are the 40–60-game
pedigree-heavy mid-careers; the losers are every 85+-game veteran (β 0.0238 → 0.0152).

| up (top) | pos | pick | g | cand | Δ | | down (top) | pos | g | cand | Δ |
|---|---|---:|---:|---:|---:|---|---|---|---:|---:|---:|
| George Wardlaw | MID | 4 | 53 | 3088 | **+151 (+4.9%)** | | Sam Walsh | MID | 154 | 2926 | −28 (−1.0%) |
| Ryley Sanders | MID | 6 | 54 | 3395 | +82 (+2.4%) | | Matt Rowell | MID | 126 | 4471 | −27 (−0.6%) |
| Sam Darcy | KPF | 2 | 51 | 4428 | +64 (+1.4%) | | Jason Horne-Francis | MID | 100 | 5554 | −27 (−0.5%) |
| Harley Reid | MID | 1 | 60 | 3684 | +54 (+1.5%) | | Christian Petracca | MID | 231 | 1970 | −25 (−1.3%) |
| Colby McKercher | MID | 2 | 60 | 4018 | +48 (+1.2%) | | Joshua Kelly | MID | 230 | 421 | −25 (−5.9%) |
| Connor O'Sullivan | KPD | 11 | 47 | 2397 | +46 (+1.9%) | | Tim Taranto | MID | 192 | 2337 | −25 (−1.1%) |
| Murphy Reid | SF | 17 | 45 | 3139 | +29 (+0.9%) | | Andrew Brayshaw | MID | 191 | 2998 | −25 (−0.8%) |
| Zach Reid | KPD | 10 | 40 | 912 | +19 (+2.0%) | | Noah Anderson | MID | 149 | 4918 | −24 (−0.5%) |

Full 561-row table: `NAMED_ROWS_W1.json` / `NAMED_ROWS_W1_out.txt` (all 111 rows with 40≤g≤90
printed).

## 7 · Interaction with the ORDER A build (owed statement)

ORDER A (Candidate 32: G\*=2 sitter credit, delivered-season reset, age-referenced stall bars,
deeper β) rebuilds the SAME pedigree leg this seat measured: Φ's stall run `s`, the bars that
define "delivered", and D's clock all multiply β inside `π = D(c_u)·(1−ρ) + Φ(g,s)·β(g)·ρ`.
Consequences, stated plainly:
1. The knot values proposed here are **conditional on the 31-F Φ and D**. Because Φ and β enter as
   a product, changing the stall definition re-identifies β — ORDER A must re-run this seat's
   instruments (they are all path-substitution reruns of committed harnesses; ~90 s each) on its
   own tree rather than transplant these numbers.
2. This seat's headline is direct input to ORDER A's scope: its "deeper β" component **should not
   be expected to move years-4–6 rank skill** (median recovery 0% here even at the monotone cap).
   If ORDER A's motivation for deeper β is the S4 gap, the evidence points at its OTHER components
   (the stall/Φ machinery, the sitter credit) as the live channels — and W2's acceptance bands
   (level/spread) are the right test for deeper β's actual effect, which is level-side
   (mid-career pedigree carry ≈ +0.1–5% on named rows), not rank-side.

## 8 · Honesty ledger

* **P1 PASS** (deviation 0.0). **P2 PARTIAL**: deep-mid (36–70) positive and identified, and E3's
  53-knot sits above wired — but its CI contains the wired value, and the 71+ predictions failed
  (71-90 measured 0.0152 vs wired-interpolated 0.0298; E3 85.5 = 0.0152 vs wired 0.0238 — both
  *below*, not above). **P3 FALSIFIED** — reported as the packet's headline, not buried.
* The E3-vs-local tension (joint knot 0.244 vs band fits 0.10–0.17 in 36-70) is a real
  estimator disagreement, shown in full; the joint fit borrows identification through shared
  controls and its hat basis is linear-in-value where the wired interpolation is log-log (disclosed
  second-order difference). The proposal took E3 per the prereg rule; the cap bound anyway.
* The 71+ bound is the result there: 90% CI width ~0.16 at 85.5 with all 889 careers pooled. Any
  deep-β wiring beyond ~71 games is a choice, not a measurement, on this store.
* One store, one league history; delivered value is the house v0-language ruler (√-games,
  Ruling-1 bars, flat-14); H=4 panel is a disclosed horizon departure used for power only; the
  named-rows board deltas ride `cand31.json`'s board snapshot and the ×1.053 currency factor to
  the emit ruler.
* Nothing in the engine, board, store, or any law file was touched; every artifact here is
  additive under `docs/evidence/order33_w1_2026-08-17/`.

**Files:** `PREREG_W1.md` · `w1_control.py` → `CONTROL_W1.json` · `w1_deep.py` → `DEEP_W1.json` /
`DEEP_W1_out.txt` · `w1_emit_cf.sh` → `EMIT_W1CF_out.txt` (+ `per_entrant_W1CF.json`, scratchpad,
md5 `c5c7719a`) · `w1_cf_score.py` → `RESULTS_W1CF.json` / `RECOVERY_W1.json` /
`RECOVERY_W1_out.txt` · `w1_named_rows.py` → `NAMED_ROWS_W1.json`.

*Seat W1. The prereg bound; the negative result is the result.*
