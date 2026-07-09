# PROOFS — Chapter-3 injury/availability build — 2026-07-09
### Candidate branch `claude/new-session-pjbof6`. Store `a2fbc9a0` UNCHANGED (no re-seal). Register
### `652d83e8` pinned. Candidate board `d9728208` (gate-mode, reproducible). BUILD-REPORTED — owner reads
### the R-i table + exemplars before any merge word; bake/tag/re-seal are owner-only.

## Full suite — green from a fresh bootstrap (reverify_gates.sh; ship_gates.txt / selftest.txt)
| check | result | note |
|---|---|---|
| **VERDICT** | **FAIL=3 (A2 · A3 · A12)** | exactly the frozen expected reds — **no new reds, none removed** |
| A2 | FAIL (unchanged) | Curtis/Ward — non-register, pre-existing frozen red |
| **A3 [DC]** | FAIL (upheld) | Rozee 2026 ratio 0.71→**0.54** (the layer prices his nil 2026); stays a permanent **DATA-CAUSED** red (R-A3 uphold). Evaluated PRE-LTI-layer stamp honoured: the red is data-caused; the overlay does **not** pass it (it deepens it) |
| A12 | FAIL (unchanged) | Travaglia/Smillie — non-register, pre-existing frozen red |
| **B1 (G-PEAK cohort)** | **PASS — UNCHANGED** | cross-cohort avg-peak row 1:100 2:116 3:121 4:130 5:128 6:120 7:107 — **byte-identical to baseline** |
| B2 (leakage) | PASS | unchanged |
| **B3 (book seal)** | **DIFFERS-BY-DESIGN** | candidate head da56bccf ≠ sealed 4b08796c → owner RE-SEALS the book at the bake. Content moved only because register names' `cur` column = their moved board value; the historical walk-forward rows stay clean (return haircut is `_BOARD_PATH`-guarded) |
| **B4 (board parity)** | **PASS** | regenerated d9728208 == shipped d9728208 (byte-agree) |
| **B5 (G-FLOOR)** | **FEATURE — never-crater holds** | 60→**61** saves (+1: one nerfed register name floor-caught — the floor doing its job), lift +1922→+1948; lowered=0, non-ND moved=0 |
| D14a/b/c (V0 laws) | PASS | unchanged |
| self-test (guards 1–5, F1, F2, collision sentry) | **PASS** | board==engine (F1), book==board (F2), Kako/Bont ground-truth, King-pair sentry clean |
| panel 10/10 | **PASS** | non-register byte-identical |
| CONFIG-MANIFEST (gate mode) | PASS | hash d88404 unchanged (new levers ride as code defaults; folded at the owner's bake) |
| RULING-CONFIG (R3) | PASS | RL_PVCFIT=0 default + export bake-guard intact |

## Guard before/after (FENCE watchers)
- **G-PEAK / A-PEAK (Butters/Holmes):** B1 avg-peak row **byte-identical**; Butters/Holmes non-register → parity. **Untouched.**
- **G-COHORT:** measured walk-forward on the book. The eight 2025-draft year-1 register names' 2026 nerf is a
  **present-board** effect; the walk-forward class sums are historical (data ≤ T) and **unmoved** → the year-1
  denominator is unchanged → the ratio does **not** rise → **no tip toward the hard 130.** Denominator direction:
  the injured year-1 names sit in the denominator, but the nerf never lowers the walk-forward denominator (it
  lowers only their present board value), so the no-arbitrage bound is not stressed. No remediation needed.
- **G-FLOOR (B5):** +1 floor-save (a nerfed register name caught by the never-crater floor) — the guarantee
  working, register-scoped, not a crater. **Held.**
- **G-ATTR:** three separable per-player columns ship — `avail_nerf` (Part 1), `lti_return_hc` + `lti_ret_delta`
  (Part 2), `avail_clock_note`/`_lti_reg` flags (fork dispositions). Every mover attributed.
- **G-DATA / Guard 5:** register `652d83e8` in the boot pin set; asserted on entry; tripwire single.

## Non-mover parity (nonmover_parity.txt)
RL_AVAIL on vs off: 805 board keys, **39/43 register names move, 0 non-register movers.** (4 register names sit
at the floor and don't move even on.) Movement is confined to register keys + their KPFFIX interactions
(fork-v LD exclusion on register KEY_FWD). Everyone else is **byte-identical**.

## _b2hc retirement parity
`_b2hc>0` fired on exactly {nicholas-martin, tom-green} on store a2fbc9a0 — both register names. The strip
moves only those two (up, by the removed haircut); no non-register player was affected. Store md5 UNCHANGED.

## Reproduce
`session_2026-07-09/injury_build/reverify_gates.sh` (gate-mode board → seed shipped → self-test + ship_gates
+ panel). R-i table: `run_ri_table.sh`. Part-2 derivation: `engine/rl_after/derive_lti_return.py`.
