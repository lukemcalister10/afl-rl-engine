# DIRECTIVE — LEG B SEGMENT 3: THE v1.1 RE-WIRE · 2026-07-16 · seat 9 (Fable)
### FRESH Claude Code (Opus) chat. Self-contained — this document is your whole brief; supersedes
### docs/archive/DIRECTIVE_LEGB_segment3_diagnostic (its base pin and act (A) went stale — register
### items 224/225). SILENCE IS A RED. S1–S6 operative. Report context usage at every HALT/RETURN.
### REAP all background tasks before any HALT/RETURN.

## EFFORT: Extra
Why not one lower: this re-wires the central pricing surface; the design is measured and pinned
(memo v1.1), so the effort buys verification breadth, not exploration — and thinner validation is a
refused lever.

## MODE: auto — PLAN first, then STOP (checkpoint). The PLAN commit carries: the pre-view hash
## manifest (§FEED md5s below, verified against your own fetch) · the exact hook site (file:line) ·
## the ρ construction incl. the QUALIFYING-SEASON GAMES FLOOR you propose · the captain-off pass
## mechanics · the seg-2 posval-wiring removal list. HALT with the PLAN SHA (≤10 lines); the owner
## pastes PROCEED after supervisor prescreen. Then implement.

## TIME: ~20 min to the checkpoint · 2.5–4 h after PROCEED (confirm; flag >2×/<½×; report actual).

## FEED (fetch fresh from main; VERIFY the two md5s — mismatch ⇒ HALT, the seal)
1. `docs/MEMO_LEGB_functional_form_2026-07-16.md` — **header v1.1** — md5 MUST equal
   `c664062cf932ff1497e7b8fb19a2cd63`. THE DESIGN. Read in full; implement, never redesign.
2. `docs/acceptance_v1_18.json` — md5 MUST equal `caf8636cdc63c649d57cff72d94eca02`. Assert
   `leg_b.*` entries; the grid is {0.55, 0.60, 0.65, 0.70}.
3. `docs/DIRECTIVE_LEGB_uncompress_2026-07-16.md` — deliverables + fence, unchanged except where
   memo v1.1 ⟪v1.1⟫ blocks supersede (placement · ρ · captain · grid).
4. Register items 221/224 (the two measured diagnostics + the rulings, verbatim context).
5. On the branch: `session_2026-07-16/uncompress/PLAN.md` (amended) + `FINDING_s_dial_HALT.md` +
   the seg-3 diagnostic finding at the head — your predecessors' committed record.

## BASE PIN
- **Engine/store base — STRICT:** branch `claude/legb-output-price-decompress-3vo8y1` at
  **`c27d697`** exactly (`git ls-remote https://github.com/lukemcalister10/afl-rl-engine
  claude/legb-output-price-decompress-3vo8y1` must print
  `c27d69788f92b125a63a2b57ff39fc9e75cdfbd0`). Any other head ⇒ HALT-AND-ASK. CONTINUE this branch —
  never a sibling. All non-doc inputs are at-or-before this base; docs are FETCHED, never merged.
- **Docs base:** main AT OR AFTER **`62ab64d`**, and `git diff --name-only 62ab64d..main` must be
  `docs/`-ONLY (the #101 merge sits BEFORE this pin — earlier pins would false-halt on ui/).
- Store `b1fd0bce` untouched at your head (Guard 5).

## THE JOB (memo v1.1 exactly)
0. **CONFIRM (light, ~10 min, in the PLAN commit's evidence):** re-run β_c and λ_level_now on the
   frozen estimator (expect ≈ 0.622 / ≈ 0.124); one agreement line. Divergence ⇒ report it; your
   numbers govern.
1. **REMOVE the seg-2 six-site posval wiring** (delete-don't-disable; obituary — it implemented a
   superseded design; the diagnostics stay committed history).
2. **THE MAP, once per player, at the production-value hook** (pr = price6, pre-pole-recovery —
   the seg-3 diagnostic's exact construction): `v′ = pr₀^(1−w) · (V_ref_b · ρ)^w`, w = s·E (current
   evidence), where **pr₀ = the CAPTAIN-FREE pr** (via the RL_CAPT-off evaluation pass) and
   **δ = pr(capt on) − pr(capt off) is added back UNCHANGED** (δ byte-identity self-test).
3. **ρ (memo §2.1 ⟪v1.1⟫):** recent-2 QUALIFYING-season average points above REPL[pos] — a
   qualifying season has games ≥ the floor you declare in the PLAN (justify it against the frozen
   estimator's own o-construction); injury-wiped seasons SKIPPED, never averaged; zero qualifying
   seasons in window ⇒ w = 0. Denominator: the positional demonstrated-proven MEDIAN of the same
   measure. V_ref_b = the median demonstrated-proven pr per position.
4. **Onset ramp** (memo §2.2) at the bar in THIS measure's units, width declared in the PLAN.
5. **Conservation:** production-side per-position renorm across the whole population (the seg-2
   C[pos] machinery, re-pointed at the new map's site) — pedigree/iso nominal; the whole-system
   ledger carries the transfer.
6. **Kill-switch `RL_UNCOMP`** gates everything (map + renorm + reference build):
   **RL_UNCOMP=0 ⇒ board `8d90c9ac` BYTE-EXACT** — prove it. Config `c2d233ae` unmoved.
7. **The s dial:** frozen fit_beta, grid {0.55, 0.60, 0.65, 0.70}, **s = smallest clearing
   β ≥ 0.85**; empty grid ⇒ HALT with the table (do not extend).
8. **Then the FULL original deliverable set** (the item-206 directive, unchanged): frozen-suite
   β/≤22-slope/English-Briggs(captain-in)/G-COHORT y4-y5-y6 + the row-level fixture/census cells/
   L-SMOOTH · the whole-system SCAR ledger · the donor-side mover report (name · Δ · ρ · w ·
   earned/prior) · value-flow + R104.8 decomposition · the w-export (per-player w, ρ, earned/prior —
   Leg D consumes it) · kill-switch regeneration matrix (RL_UNCOMP × RL_ISOFADE) · gate snapshot ·
   panel/self-test.

## FENCE
IN: engine files at the hook + the removal list + kill-switch + deliverables + derived regeneration
(stamped). OUT (touch = HALT): the STORE (`b1fd0bce`) · docs/ · ui/ · acceptance JSON · gate/guard
code · config manifest · Leg A's τ · the pick curve. Scope growth = a NEW directive (S2).
RETURN ≤30 lines + plain-terms close: branch · head SHA · PR · actual time · context usage.
