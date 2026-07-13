> **OBITUARY — ARCHIVED 2026-07-13 AT THE v2.9 SEAM (supervisor seat 5).**
> This file was authored by a BUILD (commit da5f7f3, the v2.9 refit-cert job). Builds never author
> docs (CORE). It is superseded in full by the supervisor-issued CONSTRAINTS v1.8.
> WHAT WAS RIGHT: its numéraire re-quote table — folded VERBATIM into v1.8.
> WHAT WAS WRONG: its "PROPOSED conform" of G-COHORT, which held that the frozen suite is
> authoritative. That is OVERRULED by the owner's ruling of 2026-07-13 (register v52): the July-8
> construction IS the gate, and the frozen code conforms to IT — not the other way round.
> Kept for the record only. Do not cite. Do not resurrect.

# CONSTRAINTS — v1.8 FOLD (the v2.9 seam) · 2026-07-13 · supersedes v1.7 on the two points below

**Scope of this file.** v1.8 is the seam fold of the v2.9 candidate. It records the TWO constraint-content changes the
v2.9 refit forces; **all other guards/anchors are UNCHANGED from v1.7** (this file references v1.7 by ID for them — the
full single-source merge is the supervisor pen's action at the seam, in the same commit that tags v2.9). Candidate ONLY
until the owner's bake word. Machine twin `acceptance_v1.x.json` regenerates from the folded registry at the seam.

### CHANGELOG v1.8 (v2.9 candidate)
1. **THE NUMÉRAIRE RE-QUOTE (L7, owner-ruled 2026-07-12 "Rebase, 3000 is it.").** PICK 1 = 3000 is the numéraire.
   The v1.7 ×1.0524 redenomination is **re-based ÷1.0524** to the 3000 anchor. Every absolute-SCAR constant re-quotes
   (uniform scalar ⇒ all ratios/orderings preserved; only the unit changes). **Ships** (owner-ruled).
2. **G-COHORT PROSE ↔ FROZEN D5 CODE — PROPOSED CONFORM (resolves item 19 margin-3).** The v1.7 canonical G-COHORT
   prose ("average the class-year SUMS") and the FROZEN shipped gate (`ship_gates_check.py:_b1_rows`, owner ruling D5:
   per-cohort yr1-indexed, unweighted cross-cohort mean) describe **different constructions**. The frozen suite is
   authoritative (v1.5+ legend). **PROPOSED** correction below — for the supervisor/owner, does not ship unruled.

---

## FOLD 1 — NUMÉRAIRE CONSTANTS RE-QUOTE (÷1.0524 · BINDING at bake, candidate now)
Factor = **1.0524** (`pick_redenomination.json`; MEASURED 4.68336/4.45 = 1.052440). These are the v1.7 absolute-SCAR
constants divided by the factor. Source table: `session_2026-07-12/v2_9_candidate/out/numeraire_requote_table.md`.

| constant | v1.7 (×1.0524 units) | → v1.8 (numéraire, pick-1=3000) | note |
|---|---|---|---|
| A-BONT baseline | 3246 | **3084** | back to the pre-redenomination 3084 class (3084 × 1.0524 = 3246) |
| G-CONVEX young-floor ≤21 | 189,579 | **180,140** | band-aggregate SCAR floor |
| G-CONVEX young-floor 22–24 | 187,563 | **178,224** | |
| G-CONVEX young-floor 25–26 | 113,420 | **107,773** | |
| SCALE anchor (7000/ref^γ) | 7000 | **6651** | absolute board magnitude; equivalently SCALE 4.68336 → **4.45017** (== baked v2.7 4.45) |

**Unchanged by L7** (already in the numéraire's parent unit, NOT board-SCAR): REPLACEMENT BARS (MID 80.1 · GEN_DEF 78.3 ·
GEN_FWD 70.9 · KEY_DEF 68.4 · KEY_FWD 66.8 · RUC 78.5) — live in level/par space. G-FLOOR historical dispensations are
closed one-offs (if ever re-applied to a numéraire board the SCAR deltas scale ÷1.0524: 5→4.75, 13→12.35).

**Standing law (mechanical, wired):** `rl_export.py (g)` numéraire guard + `BAKE_CHECKLIST §3` — a numéraire board with
pick-1 ≠ 3000 HALTS the write. Dormant-with-warning on the pre-L7 (×1.0524) board by design; unconditional once L7 is the
refit's final step. Future scale drift re-bases the CURRENCY to the anchor, never the anchor to the drift.

## FOLD 2 — G-COHORT: CONFORM THE PROSE TO THE FROZEN D5 GATE (**PROPOSED** — item 19 margin-3)
The **frozen, shipped** G-COHORT gate is authoritative. Its ruling (D5), pulled verbatim from `ship_gates_check.py`:

> **B1 REDEFINED 02/07/2026 (Luke, in writing, confirmed, D5):** the gate tests the CROSS-COHORT UNWEIGHTED AVERAGE of
> indexed cohort value at each year-depth (rise from yr1 to a peak in yrs 4-6; <5% pre-peak dips of the average tolerated).
> Per-cohort curves UNGATED by design but printed as a pipe table on every gates-board run. The old per-cohort rise
> backstop is RETIRED.

Construction (`_b1_rows`, the byte-for-byte gate): population = incurve (type ∈ {ND,RD}) ∧ draft cohort 2004..2020;
per cohort = class-year SUM of Vpath at each depth N; **index each cohort to its OWN yr1 (=100)**; the gated row =
the **UNWEIGHTED cross-cohort simple mean** at each depth. y4/y5/y6 EACH ≤ 130% (hard; guide 120–125%).

**The tension.** The v1.7 canonical prose reads "average the class-year SUMS across classes" (a raw-sum average — which
weights large cohorts more, and is the construction the refuted ad-hoc 137.8 read used). The frozen code indexes each
cohort to its own yr1 FIRST, then takes the unweighted mean (equal cohort weight). The reconciliation (register item 19)
reproduced the audited baseline **128.6/127.1/119.0** with the frozen construction; the raw-sum-average 137.8 is refuted.

**PROPOSED correction (does not ship unruled):** replace the v1.7 G-COHORT canonical wording with the D5 construction
above (per-cohort yr1-indexed, unweighted cross-cohort mean, ND+RD 2004–2020, denominator min(y1,y2)=y1). This is a
CONFORM (prose → the code that has always run), not a gate change — the gate is unmoved. Owner/supervisor word requested
at the seam. Until then: the frozen code governs (legend precedence), the prose is flagged non-authoritative.

---
_All other v1.7 constraint content stands unchanged and is not restated here (single-source discipline; full merge at the
seam). This v1.8 fold is the supervisor-pen input for that merge._
