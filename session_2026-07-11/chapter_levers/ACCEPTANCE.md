# ACCEPTANCE — chapter-lever candidate · 2026-07-11
### Levered candidate: board `9ecbe0fa` (was 8f3675f3) · book re-sealed `a19b3cb8` · store UNCHANGED
### `04f38dad` · engine head UNCHANGED `7a07e369` · config UNCHANGED `69ead79b` · expected_boot re-pinned.
### Full gate log: `out/gate_suite_levered.txt` · projection artifact: `out/projection_test.json`.

## 1. The owner's GDEF test — values + the transition expectation stated plainly
| player | candidate → levered | the genuine-chance arithmetic (measured) |
|---|---|---|
| zeke-uwland | 2230 → **2746** (+23.1%) | 0.83 chance of the pick-2 demonstrated prize (3191; ash/blakey-anchored) landing in ~4 yrs, PV'd at the board's own 15% lens, paid over the engine's own 4-yr view, fading at 10 career games (φ=0.61) |
| dylan-patterson | 920 → **992** (+7.8%) | 0.83 × prize 2099 (pick 5), PV ≈ 996 — now priced AT the transition expectation |
| tobie-travaglia | 786 → **792** (+0.8%) | 0.82 × prize 1718 (pick 8), PV ≈ 806 — he was ALREADY at it; the demonstrated pick-8–19 outcomes on this board are bimodal (blakey/wilmot/clark vs campbell/quaynor/jones) |
| lachlan-carmichael | 634 → **650** (+2.5%) | P 0.75 × prize 1446 over the engine's 931 — modest measured gap |

## 2. kysaiah-pickett + bailey-smith — the honest data verdict (L2)
NOT re-weighted: 3496 and 5605 unchanged. Realized outcomes for their exact stratum (sustained
2-season risers) fit s=0.334 [0.217, 0.451] vs the 0.46 they already receive — sustained risers
persist LESS than single-season risers (0.548), and even the age≤26 sustained stratum (0.478) is
within noise of 0.46. Full numbers: `L2_SUSTAINED_FORM_VERDICT.md`.

## 3. THE PROJECTION TEST — **PASS**
Levered board ridden 6 and 7 years forward through the engine's OWN aging lens (PEAK_AGE + DELTAS;
34+ = retired). Projected top-50 positional mix at +6: MID 28 · GEN_DEF **7** · KEY_FWD 5 · GEN_FWD 4 ·
KEY_DEF 4 · RUC 2 (top-20: 2 GDEF). Young-now GDEFs PRESENT at both horizons: archie-roberts
(proj 6123/6061 — top-5 overall) and zeke-uwland (proj 4296/4429, top-15) + maturing established
wilmot/bowey/b-uwland; ash/blakey age through but hold top-50. Young GDEFs do NOT vanish. (Method +
base-vs-levered comparison in the committed artifact; the mix is identical pre/post lever at top-50 —
the credit moved uwland UP INSIDE the top end; patterson projects to ~1600, top-100 not top-50.)

## 4. Gate suite (full log committed): VERDICT **FAIL=3 · FEATURE=1 · PASS=17 · PENDING=4 · STRUCK=1**
- Reds EXACTLY **{A2, A3, A12}** — A2/A3 the standing owner-ruled data-caused reds, unchanged.
- **A12 did NOT flip** (travaglia 792 vs moraes 1023, deficit −231): the directive expected the flip;
  the MEASURED transition says travaglia is already priced at his genuine chance (§1). Reported, not
  forced — the owner rules on the evidence.
- B1 cohort growth law PASS on the levered book: y4 = **129 vs hard 130 (margin ~1.0 pt, unchanged)**;
  row 100/115/120/129/127/119/106. B3 seal PASS (a19b3cb8 regen == sealed). B4 byte-parity PASS
  (9ecbe0fa). B6 ramp PASS, 0 dips. D14a/b/c PASS.
- **G-FLOOR (B5)**: 63 saves, **lowered=0, non-ND moved=0** — no new floor trips; the named-16 waiver
  set (remediation eyeball dips vs baked v2.7) is re-examined in the eyeball pack.
- Panel: 10/10 values byte-equal to the CANDIDATE base (levers moved none of the panel players);
  the uniform ~+5.2% offset vs the stale panel pins is the remediation's recorded currency shift
  (expected_boot 'panel' annotation carries it; panel re-pin is bake-time supervisor work).

## 5. G-ATTR — per-lever separability (boards committed)
| board | md5 | file |
|---|---|---|
| base (candidate) | 8f3675f3 | `data/rl_build/rl_app_data.json` @ c02499a3 |
| L1-only | 9ecbe0fa | `out/board_L1only.json` |
| L2-only | **== base byte-exact** (L2 ships NOTHING — measured not-supported) | n/a |
| both (SHIPPED) | 9ecbe0fa (**== L1-only byte-exact**) | `data/rl_build/rl_app_data.json` |

Δ(both) = Δ(L1) + Δ(L2) holds EXACTLY (Δ(L2)=0 per player by construction; both == L1-only byte-identical).
L1-only movers: 56, 0 negative, established top-end GDEFs byte-identical (named check in
`L1_TRANSITION_CREDIT.md`).

## 6. Threshold re-denomination factor (report-only; registry = supervisor's pen)
CONFIRMED unchanged: `pick_redenomination.json` factor **1.0524** (measured 1.052440; delta +0.00004
vs pin, unchanged to 4dp). × applies to A-BONT 3084→3246 and the G-CONVEX floors.

## 7. Three narrowest margins (levered candidate)
1. **G-COHORT/B1 y4: 129 vs hard 130 — ~1.0 pt** (unchanged by the lever; the credit lands mostly in
   the y1 denominator).
2. **A10 Curnow: ratio 0.55 vs floor 0.50 — +0.05** (data-caused knife-edge by design).
3. **A8 Berry/Tsatas: 2.14× vs 2.00× — +0.14×**.
(A12 is RED, deficit −231 SCAR — a standing red, not a margin.)
