# DIRECTIVE — LEG-B CONSERVED — TWO-POINT EXTENSION (s=0.10, 0.20) · 2026-07-16 · seat 10
### STATUS: fires on the owner's paste. PURPOSE: fill the two intermediate strengths the owner
### named (0.10, 0.20) so a baseline · 0.10 · 0.15 · 0.20 · 0.25 all-player sheet is ALL MEASURED,
### no interpolation. Read-only; ships nothing. Pure re-run of the PROVEN item-262 harness at two
### new RL_UNCOMP_S values — ZERO new engine code, toggle stays UNSET (conserved = shipped C).

## EFFORT: Low. Why not Medium: two points on a committed, md5-frozen harness; no new code,
## no new instrument, no design. MODE: auto — PLAN first (one line). TIME: 10–20 min. Confirm;
## flag >2×/<½×; report actual wall-clock.

## BASE PIN — full-URL ls-remote against https://github.com/lukemcalister10/afl-rl-engine.git
- **Engine base — STRICT:** branch `claude/legb-conserved-measurement-j9tcf7` at **`fef2b64`**
  (the proven conserved harness lives here; RL_UNCONSERVE stays UNSET). NEW branch; commits ONLY
  under `session_2026-07-16/legb_conserved_2pt/` (copy/import the harness; do not mutate it).
- **Docs base:** main AT OR AFTER the SHA in the owner's paste; diff docs/-only.

## FEED
session_2026-07-16/legb_conserved_measure/ (the harness of record: run_grid.sh, measure_gcohort.py,
analyze_conserved.py, aggregate.py + out/) · session_2026-07-16/uncompress/beta_measure.py (FROZEN
14c59139) · register items 258/259/262 (the band; the corrected verdicts) · this directive.

## THE JOB — CONSERVED map (RL_UNCONSERVE unset) at s ∈ {0.10, 0.20}
The item-262 battery, frozen instruments only (S4), unchanged:
β (CI/width/n) · G-COHORT y4/y5/y6 via the frozen July-8 construction, **judged against the FULL
BAND (floor 1.08 · cap 1.30 · ideal 1.15–1.25)** · E/B vs 1.75 with RAW numerator/denominator
printed · position-pool Δ totals · net board ΣΔ · the all-804 SINCERITY ledger CSV
(same schema as SINCERITY_all804_s0.25.csv: stable_player_id,player,pos,num_off,num_on,
delta_scar,delta_pct,rank_off,rank_on,delta_rank,rho_num,rho_ratio,w) · Bontempelli named ·
A-PAIRS pair 2 (Reid vs Bont) + pair 3 (Sanders vs Bont) scored at both s.
A/B: RL_UNCOMP=0 ⇒ board 8d90c9ac byte-exact (re-assert).

## FENCE
IN: env-var runs of the committed harness · the two new SINCERITY CSVs + two POINT files ·
session-dir artifacts under `legb_conserved_2pt/`. OUT (touch = HALT): engine · store · docs/ ·
config · acceptance · gate/guard code · the toggle file · any s other than 0.10 and 0.20 · any
selection or tuning. SILENCE IS A RED.

## RETURN
≤15 lines: branch · head · two one-liners (β/width · y-band verdict BOTH SIDES · E/B raw parts ·
Bontempelli SCAR+rank · pair 2/3) · confirm both SINCERITY_all804_s0.10.csv and _s0.20.csv
committed · actual time. The supervisor builds the owner's five-column sheet from the CSVs on
return.
