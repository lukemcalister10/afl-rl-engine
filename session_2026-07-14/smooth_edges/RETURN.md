# RETURN — SMOOTH THE THREE HARD EDGES (attribution-first; Tier 3, read-only, candidate)

**branch** `claude/smooth-three-hard-edges-fxeza5` · **head** (see commit) · **PR** candidate (below) ·
**board measured** `3dc19fbb` (store `340a7a32`, engine `2030e5df`) = ITEM-20 successor to tagged
`81e48293` (bramble +1 the only v-delta; no measured player affected). Baseline rebuilt **twice,
byte-identical** (`3dc19fbb == committed`), panel PASS 10/10 — **ground is stable here.** Overlay all-off
= base byte-exact (`b5dbead0`). Nothing outside `session_2026-07-14/smooth_edges/` was written.

**THREE THINGS UP FRONT (no binding guard is *breached by the fix*):**
1. **Supervisor's Jamarra attribution is CORRECT on mechanism** — but Fix 2 is mis-located: the
   `FLAT_TOL_G` step it quotes is in **dead code** (`_lvl_eff_core`); the live step is `_coreM1`
   `TOL_M1=5.0`, and Blakey/English don't sit on it (see #3).
2. **The three fixes cannot fully smooth Jamarra** — a **fourth edge** (the ev(level) pricing convexity
   at the replacement bar) turns an 11% level move into a 54% value move. Reported, not redesigned.
3. **G-COHORT already breaches at BASE** (walk-fwd l3 gated: 136.5/137.3/141.2 vs 1.30) — pre-existing,
   reproduced by the official harness; the fix moves it ≤+2.5pt and does **not** create it.

**D1 — 1009→187, term by term:** `_nqual` 3→3 (nqual cliff never fires) · `_par_prior` 66.18→66.18
(unchanged) · **`_lvlcurr` 61.21→48.75** (−20%): the 3g@26.0 2026 cameo takes **35.4%** of the decay
weight (full 1.0 vs 2024's twice-decayed 0.16) — `_lvlcurr` has no small-sample damping · then the value
curve amplifies −20% level → **−81% value** at the KEY_FWD replacement knee.

**EACH FIX ALONE / COMBINED (ev/F, board `3dc19fbb`):** F1 278 movers +1171 · F2 57 movers +4675 ·
F3 86 movers −2612 · **ALL 335 movers +4171**.

**A1 Jamarra** (67→70g): BASE −81% (1009→187) → **F1 −54% (1006→466)** — F1 did it (F2/F3 don't touch
n=3). Still >20% (fourth edge). **A2 kids:** under ALL only bands 1/2 negative (−100/−3); band-1 24
movers 17↑7↓ — not the only negative, not nerfed (vs rejected build's −3593). **A3:** Fix 2 moves
**neither** Blakey (3330, +8.04 up-mover) **nor** English (3132→3251 via F1, −2.83 down-holder) — they
are NOT on the tolerance step; the premise fails. **A4 improvers:** F1 leaves all untouched; **F3 drags
Xerri −317 (−5%)** (its cost). **A5 guards on rebuilt board:** A-BONT PASS (3482,+12.9%, unchanged) ·
A-PAIRS p2 PASS (+3.0%) · p3 still-fails-but-improves (sanders 3960→3863) · A-DUUR hold (4339) · G-PEAK
PASS (0% drop) · G-FLOOR 13→12 (Jamarra saved) · G-CONVEX all bands clear · G-Y0 y2>y1 held · G-COHORT
see #3. **A6:** named worst-steps fall (Jamarra 81→58, Xerri 19→11, Wilmot 19→13); board-wide steppers
>20% 243→236 — residual dominated by the fourth (pricing) edge; **Jamarra still steps (58%).**

**IN PLAIN TERMS:** Fix 1 is the right fix and roughly halves Jamarra's cliff by making three bad games
count for less on a curve the data itself sets — and it does this without hurting the kids or the
improvers. Fix 2 as written moves nobody who matters, because the step it names is dead code and the
players it cites aren't standing on the live one. Fix 3 does what the owner asked but quietly pulls
proven improvers like Xerri back toward their draft pedigree. And the biggest jump that's left — in
Jamarra and across the board — isn't in any of the three edges: it's the pricing curve near the
replacement bar, a fourth hard edge that deserves its own ruling. **Candidate only — no bake, no tag,
no merge without the owner's word.**
