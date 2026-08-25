# SEAM FIX · BOUNDED SEARCH FINDINGS · 2026-08-25 (successor window)
Mandate: v848 — fix the error; fresh-eyes bounded search before the floor; floor stands as backup.
Method files in this dir: DECLARATION.md (construction + predictions, written first) ·
census51.json / census51_live_verified.json (51 rows re-verified in-process: 0 mismatches) ·
scope_census.json (the vocabulary-blind-spot census) · variants.json · ramp_honest_scope.json ·
ROOTFIX_SCOPING.md.

## FINDING 1 — THE SMOOTH SHAPE THAT SURVIVES IS A RAMP, NOT A MIXTURE
A logistic mixture centered at the threshold FAILS the settled requirement (leake at lambda=0.575
lands at 314 < his never-played 421). Lambda must equal 1 at and above the threshold. The surviving
object: v = v_ev + lambda(c) * max(0, v_cf - v_ev), lambda = 0 below 40, smoothstep 40->45, 1 at 45+.
ZERO fitted constants — the knots are exactly the two thresholds already on the owner's desk, and the
taper spans precisely the zone the outcome data cannot resolve (the bands measured are <45 / 45-65).
Position enters via the anchor (v_cf is the row's own pick/position counterfactual) while the gate is
position-blind — both halves exactly as v841 settled them.

## FINDING 2 — THE HONEST SCOPE IS "NO BANKED LEVEL", NOT "1-8 GAMES"
The vocabulary blind spot is a row with NO >=6-game season (level reads "none"), any game count.
Census: 69 such active rows with >=1 game; 58 at tenure 1-4. The 51-row census missed real victims
(rows with >8 games spread across sub-6-game seasons) and included 9 rows that DO carry a banked
level (the machinery already sees them — out of the lever's scope).

## FINDING 3 — RAMP MOVERS AT THE HONEST SCOPE (t1-4): 12 rows, +979
leake +252 · will-green +210 · goad +184 (graded, dissolves the 40-vs-45 word) · charlie-edwards
+115 · jepson +84 · visentini +38 (NEW — census missed him, c=67.2) · lachlan-smith +36 ·
zakostelsky +28 · henderson +16 · oscar-ryan +8 · podhajski +5 · anastasopoulos +3.
Weak-late rows (barnett-class): EXACTLY zero movement. Created cameo-axis inversions within
(position, tenure, pick+-10): ZERO (checked on true board positions).

## FINDING 4 — THE T5+ BLIND SPOT (report-only; outside the validated seam range)
9 no-banked-level rows at tenure 5+ price below their never-played selves, three with strong cameos:
toby-conway (c=74.0, 460 vs 673) · liam-reidy (c=53.3, 76 vs 211) · hustwaite (c=43.3, 60 vs 213).
The t1-4 scope is where the ordering science is settled (t1/t2 correctly ordered, t3/t4 inversion
measured); the t5+ counterfactuals ride fade depths beyond the calibrated bracket (0.20-0.53 bracket
measured at depth 4). OWNER WORD: extend the lever's scope to t5+ or file for the off-season.

## FINDING 5 — THE ROOT FIX IS OFF-SEASON SCALE AND STILL WOULDN'T GUARANTEE THE ORDERING
See ROOTFIX_SCOPING.md: 67 read sites; the >=6g rule defines the band's training corpus, the outcome
currency (T_bp), ruled definitions (QUAL_336, T1 interplay), and the gates; its damping constant
would be fitted on exactly the thin cells v843 proved binding; and a damped level still would not
force any row to its never-played self (dBoard/dLevel 1.03-48.79). Complementary off-season work,
not this week's fix.

## FINDING 6 — CONSERVATIVE BY CONSTRUCTION (the honest limit)
The ramp lifts strong cameos to PARITY with their never-played selves, not to the outcome-implied
premium (outcome data says cameo cohorts BEAT sitter cohorts; the premium's size is the thing three
constructions could not resolve). This is the constraint posture: fix the proven inequality, impose
nothing the data cannot support.

## RECOMMENDATION FOR THE PACKET
THE RAMP at scope (no banked level, >=1 game, tenure 1-4). It strictly dominates both hard floors:
identical on the six settled rows, graded where the data is unresolved (goad), exactly zero on weak
rows, no law-3 cliff at any threshold, zero fitted constants, same read-site cost (one extra
scoring-stripped ev() per in-scope row). The hard floor at 45 remains the validated backup and is a
special case of the ramp (lambda as indicator). Implementation site: a final ev() wrap in
_merged_recover.py alongside the 30B-P floor wrap (ORDER-numbered, env-gated, kill-switch), stripped
rows cannot re-enter scope (0 games), day-0 byte-exact by construction; P12 reading rides the prereg.
