# DIRECTIVE — LEG B SEGMENT 4: THE v1.2 LAW + THE GRID · 2026-07-16 · seat 9 (Fable)
### FRESH Claude Code (Opus) chat — this document is the whole brief. Segments 1-3 are retired; the
### scaffolding is DONE and prescreened (item 237). This segment: replace the stub with the OWNER'S
### LAW, pass the λ pre-gate, run the grid, deliver the full Leg-B RETURN. SILENCE IS A RED. S1-S6.
### Report the APP context counter (self-estimates are floors) at HALT/RETURN; reap tasks.

## EFFORT: Extra (the chapter's crux ships here; thinner validation is a refused lever — why not
## lower). Why not higher: the design is owner-ruled and measured; the machinery is prescreened.
## MODE: auto — a SHORT PLAN commit first (the weight-function diff · the λ pre-gate evidence · the
## re-recorded seals), then STOP for PROCEED. TIME: ~25 min to the checkpoint · 2.5-4 h after.

## FEED (fetch fresh; VERIFY the seals — mismatch ⇒ HALT)
1. docs/MEMO_LEGB_functional_form_2026-07-16.md — header **v1.2** — md5 == `1ff0702af5146a6a5fe68adaf974a346`. THE LAW
   (§2.1 ⟪v1.2⟫). Implement, never redesign.
2. docs/acceptance_v1_19.json — md5 == `7a97717b8302c53f3937c238abf16794`. Assert leg_b.* (rho_construction · lambda_pre_gate
   · the grid {0.55,0.60,0.65,0.70} · every carried entry).
3. docs/DIRECTIVE_LEGB_uncompress_2026-07-16.md — the FULL deliverable set + fence (unchanged where
   not superseded by memo ⟪v1.1⟫/⟪v1.2⟫ blocks).
4. Register items 230/237/239/240 (the rulings + the scaffolding prescreen, verbatim context).
5. On the branch: session_2026-07-16/segment3_rewire/ (PLAN · SCAFFOLDING_PROOF) — your predecessor's
   committed record; and session_2026-07-16/qualifying_diag/ on `2b76d37` (the diagnostic's findings
   + the PINNED harness copy) — read-only reference.

## BASE PIN — STRICT
Branch `claude/legb-segment3-v1-rewire-5jy7f3` at **`243106b`** exactly (full-URL ls-remote; any
other head ⇒ HALT). CONTINUE this branch. Docs: main at-or-after **`649d107`** (docs/-only diff —
tools/ from #102 sits BEFORE this pin). Store `b1fd0bce` + config `c2d233ae` untouched throughout.

## THE JOB
0. **THE λ PRE-GATE:** implement the ρ construction (below), then measure λ_ρ of THIS construction
   (the pinned frozen fit_beta harness, same sample law). **λ ≥ 0.95 ⇒ proceed; below ⇒ HALT with
   the number and NOTHING else built.** Commit the measurement either way.
1. **REPLACE the stub pair with the LAW:** delete `_qualifying` (a never-shipped stub — replace,
   note in the commit) and rewrite `rho_out(p,pos)` per memo §2.1 ⟪v1.2⟫ verbatim: over ALL
   games>0 seasons, u_s = games_s · 0.5^(Ynow − year_s); ρ_num = Σ u·(avg−REPL[pos]) / Σ u;
   RHO_DEN[pos] = the demonstrated-proven positional MEDIAN of the same measure; V_ref_b unchanged;
   zero played seasons ⇒ w = 0. **FORBIDDEN (acceptance-enforced): any season exclusion, games
   floor, or career-phase test.** The decay 0.5 is a declared constant next to Δ=6.0.
2. **A/B re-prove at your head:** RL_UNCOMP=0 AND default-inert ⇒ board `8d90c9ac` BYTE-EXACT.
3. **THE s-GRID:** frozen fit_beta per point over {0.55, 0.60, 0.65, 0.70}; s = the SMALLEST
   clearing β ≥ 0.85; EMPTY ⇒ HALT with the table (never extend). Selected s ⇒ UNCOMP_S_DEFAULT.
4. **THE FULL RETURN** (the item-206 deliverable set, unchanged): frozen-suite β_c+β(s) (est·CI·n) ·
   ≤22 slope (≥0.15, CI clear) · English/Briggs captain-IN ≥ 1.75 · G-COHORT y4∧y5∧y6 vs 1.30 via
   ship_gates_check._b1_july8 + the committed row-level fixture · L-SMOOTH census · census-v2 gauge
   + cells · the whole-system SCAR ledger · the donor-side mover report (name·Δ·ρ·w·earned/prior) ·
   value-flow + R104.8 decomposition · **the w-export (per-player: id,player,pos,E,rho,w,ramp,
   earned,prior — Leg D consumes it)** · the killswitch regeneration matrix · gate snapshot by
   engine hash · panel/self-tests (δ captain byte-identity · monotone ramp · zero-evidence identity).

## FENCE
IN: `rho_out`/the stub replacement + the declared constants + deliverables + derived regeneration
(stamped). OUT (touch = HALT): the STORE · docs/ · ui/ · acceptance · gates/guards code · config ·
the hook/captain/removal scaffolding beyond the stub (it is DONE and prescreened) · the pick curve.
Scope growth = a NEW directive. RETURN ≤30 lines + plain-terms close: branch · head SHA · PR ·
G-COHORT y4/y5/y6 · the chosen s · actual time · APP context counter.
