# LEG E — PROJECTION LAW + POSTURES — EXIT PROOF

All lines produced by commands run THIS session on this container (py3.12.3/np2.4.4/scipy1.17.1/
sklearn1.8.0). Dev-shell board recipe (`RL_REPO` set, `PYTHONHASHSEED=0`, no `RL_CONFIG_MODE`).
Candidate engine: `rl_model.py` cc626d7d · `_merged_recover.py` 6ad07bb2 (base fdc54e24 / 40f43772).

## 1. THE k=0 BYTE-EXACT INVARIANT (the LENS-PROJECTION assertable invariant) — PASS
Gate `RL_LEGE` (default ON; a DECLARED kill-switch like `RL_PVC2`, NOT a manifest dial):
- **`RL_LEGE=0 RL_PVC2=1 ⇒ board 06d8af60`** BYTE-EXACT (== the base balanced board; k=0 lens reproduces it).
- **`RL_LEGE=0 RL_PVC2=0 ⇒ board 9829d01a`** BYTE-EXACT (the RL_PVC2 kill-switch baseline held).
- `RL_LEGE=1 RL_PVC2=1 ⇒ candidate 06d8af60→d85901af` (the projection-law + posture board).

## 2. THE BALANCED BOARD IS UNTOUCHED BY EVERY LENS/POSTURE RENDER (R104.4) — PASS
Candidate `d85901af` vs base `06d8af60`, keyed diff: **0 / 804 displayed-`v` movers, 0 pick movers.**
The balanced board — the ONLY board that gates, bakes, or seals — is byte-identical. The 446 movers are
all in the FORWARD-LENS columns (`vP1`/`vP2`), the display deliverable. The `LENS` config field gains the
sealed posture keys (that, plus the fixed forward columns, is the whole candidate delta).

## 3. THE PROJECTION LAW CREDITS EXPECTED PRODUCTION (R103.3) — PASS
Before (06d8af60, the ruled no-improvement floor) → after (d85901af, production credited):
| player (age)          | now  | +1 old→new | +2 old→new | reading |
|-----------------------|------|-----------|-----------|---------|
| Murphy Reid (20)      | 3855 | 3503→**3876** | 3076→**3544** | pre-peak accrual credited (rises) |
| Nick Daicos (23)      | 8017 | 6934→7056 | 5200→5256 | gentler (development offsets fade) |
| Max Gawn (35)         | 3416 | 2976→2976 | 2470→2470 | past peak: no development to credit (decline intact) |
| Marcus Bontempelli(31)| 3897 | 3556→**2949** | 3068→**2102** | projected decline (L-SYMMETRY: same bar as improvement) |

Mechanism: the forward lens sets the form anchor to true-now (`_LENS_FORM=2026`) so `AGE_REF>BASE_REF`
and `_dev_advance` credits development up the map's OWN growth curve — no lens-only term, no young
multiplier (the Reid constraint). LTI truncation honoured automatically (form/games held at 2026).
No thresholds introduced ⇒ continuous in age and evidence (L-SMOOTH); the only new branch is a
continuous anchor shift. Per-player now→+1→+2 is monotone — no horizon cliff.

## 4. COMPOSITION LAW — one discount per axis (memo §4) — PASS
`posture_2027_discounts = {balanced:0.10, contender:0.15, rebuilder:0.05}` (BINDING, exact). The unit
test `tests/test_composition_single_discount.py` asserts, for every pick n and posture,
`picks_2027[posture][n] == round(face[n]*(1-d))` — one and only one application (a `(1-d)^2` double-count
would fail). **RESULT: PASS — one discount per axis, exact, no double-count.**

## 5. FROZEN SUITE (S4) / SSI GUARDS — `one_source_selftest.py` (RL_LEGE=1 RL_PVC2=1; book built) — ALL PASS but one expected RED
- **F1 EXPORT PARITY** (board v == round(engine gated ev / 1.0524), key-for-key): **PASS, mismatches=0.**
- **F2 BOOK PARITY** (book built, s4_matrix a7cbe374): **PASS, mismatches=0.**
- GUARD 3 single-source + engine-opens: PASS. GUARD 1+2 derived read-only + stamped (board stamp ==
  source `968de0c7`): PASS.
- Data ground-truth, position model, Leg A (iso fade/monotone), Leg B (R105.4/.5/.6 recency+ρ), Collision
  Sentry (Max King): all PASS.
- LEG D ACT-2 curve instrument (§9): all PASS — R104.9 strict descent, numéraire 3000, entry closure,
  `_PVC0 == pvc_curve_v2.json`, stamp store_md5 `968de0c7`, G-Y0 pooled 1.100% ≤ 2% HARD.
- **GUARD 5 boot-store: FAIL (EXPECTED)** — `rl_model cc626d7d != pinned a5fd3d7d`; the pin re-stamps AT
  THE BAKE (Leg E is an rl_model-only display build; SPEC §4 candidate-line re-pin). Single flagged item,
  not a defect — identical in kind to the five-migration EXIT.

## 6. HARD-OUT HELD — PASS
`git diff a90052a` touches ZERO of: store `rl_model_data.json` (`968de0c7` unchanged) · curve
`pvc_curve_v2.json` · `data/` · `docs/` · SEASON_PROG. Changed: `rl_model.py`, `_merged_recover.py`,
`rl_export.py`, `forward_valuation/distribution_pricing.py`, `ui/app/board.js`, `session_2026-07-18/lege/`.

## 7. GATES SNAPSHOT — invariant under v-parity — PASS
The A/B/G acceptance gates are value-comparisons off the shipped board `v`. Board-wide v-parity (0/804
movers, §2) ⇒ every gate verdict is byte-identical to the pinned `data/gates_snapshots/gates_40f43772.json`
(`_merged_recover` engine_head untouched at the gate-relevant path; store `968de0c7` unchanged). No gate
moved; no new snapshot minted (it would be byte-identical).

## 8. FINDING FOR OWNER RATIFICATION (memo §6.2 — tuned from evidence, not a priori)
The forward lens correctly credits DEMONSTRATED development (established young producers rise, e.g.
Murphy Reid 37g@90) and projects decline for post-peak players (L-SYMMETRY). **Residual, flagged:**
THIN pre-establishment pedigree assets (low establishment-P, few games — Jagga Smith 12g, Taj Hotton 7g,
Nick Madden 6g) still ride the seasons-based pick-premium pedestal decay under the forward lens and fall
steeply at +1/+2 (−70–80%). This is the pedestal-decay × establishment-gate interaction the AGE_REF-seam
comment names ("young pedigree assets crater ... with nothing to replace it"). It is a **MAGNITUDE
question for the owner at THIS movers report** — how much expected development to credit an unproven
pick — not a build ruling. Nothing here is baked: the balanced board (§2) is byte-exact; the forward lens
is un-baked display awaiting §6.2 ratification. See `out/movers_report.txt` (the named LTI rows incl.
Rozee, per lens vs balanced, + posture pick discounts).

## VERDICT
Projection law (R103.3) implemented and PROVEN k=0 byte-exact; balanced board untouched; postures +
composition law (one discount) with a committed unit test; interim lens retired with an obituary; UI
toggle re-enabled. Frozen suite green but for the expected pre-bake rl_model pin. Store/curve/docs
HARD-OUT held. One evidence finding flagged for owner ratification at the movers report. Candidate ready
for review.
