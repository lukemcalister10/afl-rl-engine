# PREREG_S4 — ORDER 32 SEAT S4: THE OLD-LAW SHOOTOUT. FILED BEFORE ANY COMPARISON NUMBER EXISTS.

**ORDER 32 measurement seat S4 · `land/order-29` · program brief = #334 comment 5311991190 ·
read-only mandate: measure and report only.**

**The owner's direct challenge this seat answers:** *"How do we know that paying for pedigree via
poles and pars regardless of delivery wasn't a strong way compared to this? How do we know draft
pedigree isn't an effective predictor?"*

**WHAT EXISTED WHEN THIS FILE WAS WRITTEN.** Structural/identification facts only, disclosed in full
below (§1, §2): record counts, key/schema alignment between the two matrices, population counts by
type and entry year, the None-cell census of the vpaths, and the provenance headers of the two
emitters. **No predictor-vs-outcome quantity, no correlation, no error measure and no delivered-value
number had been computed when this file was committed.** Everything in §3–§6 binds. Nothing in this
file is edited after commit; any breach of it is reported as a breach in `PACKET_S4.md`.

---

## 1 · THE TWO MACHINES (and the pedigree baseline)

Both machines have emitted walk-forward per-entrant matrices on the SAME store (`cb38ef11`), the SAME
`v0surf` (`4405cba2b42f`), the SAME #338 minimum-tenure basis, the SAME emitter family
(`emit_matrix_29c.py`, one-column delta off the standing `emit_matrix_338.py`
`bffde2f786be85037483e9f5f1563068`), and byte-identical `yrs`/`seasons`/meta on all 2,648 records
(verified: 0 mismatches on `yrs`, 0 on `seasons`, 0 on type/cat/pick/year/pos; key sets identical).
The ONLY thing that differs is the valuation columns (`v0`, `vpath`) — i.e. the law.

| | CANDIDATE (one law) | OLD LAW (poles and pars) |
|---|---|---|
| matrix | `per_entrant_O31FFINAL.json` (scratchpad) | `per_entrant_O29CFINAL.json` (scratchpad) |
| engine identity | `engine_head 71d9949a`, `RL_O31=1` (ORDER 31-F one-law lane ON) | `engine_head a353a9d3` (ORDER 29C landed tree; pre-30B, pre-31) |
| law | `price = rho·Phat + [D·(1−rho) + Phi·beta·rho]·V0` — one formula, every row | the standing pre-31 machinery: pedigree POLE leg live, PAR tables live, pathway pedestals live, no sitter fade |
| n records | 2,648 | 2,648 |

**Identification of the old law (why O29CFINAL is the poles-and-pars machine).** (a) The engine at
HEAD deletes the pole leg and the par-built ISO pick-tax ONLY under the preview/O31 dials
(`_merged_recover.py:436-440`: `_O30B_NOPOLE`/`_O30B_NOISO` are true only when
`RL_O30B_PREVIEW`/`RL_O30B_RESOLVED`/`RL_O31` is set) — with every dial unset, poles and pars are
ACTIVE. (b) The O29C emit ran on the ORDER 29C landed tree (`engine=a353a9d3`, emit log in
`scratchpad/o29c/emit_O29CFINAL/emit.log`), which predates the ORDER 30B/31 lanes entirely: its
`emit.py` reads no `RL_O31`/`RL_O30B` variable at all (grep census reproduced in `PACKET_S4.md`).
(c) `PREREG_30B.md` names the set 30B deleted — "the 26A forbidden set (pathway pedestals, par
tables, prior poles)" — i.e. at 29C those objects are the standing law. **Caveat, stated now:** the
literal dial-off board at HEAD is the 30B Step-2 board (`92982031…`), which already carries the 30B
v0 re-fit and the sitter fade; O29C is one step further back — the machinery WITHOUT any
delivery-fade of pedigree, which is exactly the law the owner's challenge describes ("regardless of
delivery"). O29C is therefore the honest old-law comparator; no per-entrant matrix of the
intermediate Step-2 law exists and none is fabricated for this seat.

**Pedigree baseline (the embedded question).** Draft pedigree standalone is scored two ways, both
fixed here: (P-a) **raw pick**, sign-flipped (predictor = −pick), ND arm only — pedigree with no
machine at all; (P-b) each machine's own **day-0 entry price `v0`** held frozen and used as the
predictor at EVERY vantage year — "what if you never updated on delivery." (P-b) is reported for
both machines' v0 columns.

## 2 · GROUND TRUTH — REALIZED DELIVERED VALUE (the house construction, reused not reinvented)

Realized subsequent delivered value is computed from the matrix records' own `seasons` arrays
(store scoring history: year/games/avg/pos/bar — byte-identical between the two matrices), priced in
the v0-language by the house scorer (ORDER 26B Layer-2 / pedigree-persistence lineage,
`docs/evidence/grace_adoption_2026-08-13/inputs/o26b_layer2.py` and
`docs/evidence/pedigree_persistence_2026-08-14/PEDIGREE_PERSISTENCE_PACKET.md`):

- **season value** `SV(t) = w_sqrt(games_t) × season_raw(avg_t, bar_t)` where
  - `season_raw(X, g) = posval(X + capt_prem(X) − BARS[g]) × 21.0` (Ruling-3 pinned callable,
    certified bit-exact against `price6` on 804/804 in the 26B gate);
  - `posval(x) = 3.0·ln(1+exp(min(x/3.0, 40)))` (`rl_model.py:830`, `S_SH=3.0`);
  - `capt_prem = _capt_ruled` with the in-code pinned constants `LCAPT_BAR=105.0, LCAPT_M=109.5,
    LCAPT_W=1.85, LCAPT_G=1.00` (`rl_model.py:703-709`);
  - `BARS` = the Ruling-1 position bars **KPD 65.4 · KPF 63.8 · MID 77.1 · RUCK 75.5 · SD 75.3 ·
    SF 67.9** (the engine's own `MA.REPL − rd.REPL_DROP`, asserted to these values at 5e-2 in the
    Layer-2 harness);
  - `w_sqrt(g) = min(1, sqrt(g/10))` (the house games weight);
  - the season's bar group is the record's own `bar` field (the emitter already applied the engine's
    season-bar rule `_fit_bar`: dual positions collapse to the LOWEST-REPL member).
- **Horizon 1 — next season:** `DV1(p, Y) = SV(Y+1)`, undiscounted; **0 if no season row at Y+1**
  (busts and sit-outs stay in the denominator at 0).
- **Horizon 2 — rest of career:** `DVrest(p, Y) = Σ_{t=Y+1..2025} 1.14^−(t−Y) · SV(t)` — flat-14
  discount from the vantage year (the pedigree-persistence convention), missing years contribute 0,
  **every future season realized or zero, no projections of any kind** (engine projections are
  deliberately kept out — scoring a machine on its own projections would be circular).
- **Right censoring:** 2026 is in progress and contributes NOTHING (no target season, and no vantage
  whose future would need it). **Left censoring:** store season rows begin 2005, so entry years
  2003–04 are excluded (the house rule).

## 3 · POPULATIONS, VANTAGES, CELLS — ALL FIXED HERE

- **Force majeure:** `paddy-mccartin`, `thomas-boyd` excluded everywhere (owner rule, carried by
  both emitters).
- **ND arm (primary):** `teaches_curve` & type ND & pick 1–64 (1,447 records before censoring).
- **Pool arms:** `is_pool` records, sliced by arm: **RD** (676), **MSD** (106), and **OTHER-POOL**
  (ND>64 + UNR + IRE + SSP + PDA + PDN + PDS pooled — each is too thin to cell alone). A **POOL-ALL**
  slice (all 1,201) is also reported.
- **Vantage years:** cohort year `N ∈ {1..6}`; as-of year `Y = entry_year + N`. Machine predictor at
  `N` = `vpath[N−1]` (= `ev(p, entry_year+N)`, the engine's own walk-forward as-of price). A record
  enters the vantage-N cohort iff (i) `len(vpath) ≥ N` and `vpath[N−1]` is not None — the player is
  still priced (listed) at Y; players whose #338 window closed before Y have no live price on either
  machine and are excluded, counts disclosed; and (ii) `entry_year + N + 1 ≤ 2025` — at least one
  realized future season-year is observable. Entry-year floor 2005 (left censor).
- **Supplementary vantage N=0:** predictor = each machine's `v0` column (entry-law day-0 price);
  pedigree = −pick; future = entry_year+1 … 2025. Reported after the primary block, same metrics.
- **Slices:** (S1) cohort year N (the primary axis); (S2) ND pick band 1–10 / 11–20 / 21–30 /
  31–40 / 41–64; (S3) pathway arm (ND, RD, MSD, OTHER-POOL, POOL-ALL); (S4) era by entry year
  2005–2014 vs 2015+. Slice tables are per-N where cell n permits, else N-pooled as labelled.
- **Minimum cell:** a cell is scored only if `n ≥ 20` and the target has ≥ 5 distinct values;
  otherwise it is printed as `n<20 unscored` — never silently dropped.

## 4 · METRICS — FIXED, NO SHOPPING

- **M1 (rank skill):** Spearman rank correlation ρ(predictor, target) within cell. Average ranks on
  ties (scipy default). Higher is better.
- **M2 (relative-value error):** within cell, normalize predictor and target each to mean 1
  (divide by the cell mean; cell unscored for M2 if either mean ≤ 0);
  `NMAE = mean_i |pred̂_i − tarĝ_i|`. Lower is better. This is the calibration measure: how far the
  machine's relative price ladder sits from the realized relative delivery ladder.
- Every headline number carries dispersion: the bootstrap CI defined in §5.

## 5 · WIN / LOSS / TIE — THE RULE

Per cell, per horizon, per metric: **paired player bootstrap**, B = 2,000 resamples with
replacement of the cell's players, fixed seed 32, both machines evaluated on the identical resample.
Statistic Δ = skill(candidate) − skill(old law), where skill = ρ for M1 and skill = −NMAE for M2
(so Δ > 0 always favours the candidate). Percentile 90% CI on Δ (5th–95th).

- **candidate wins** iff point Δ > 0 AND the 90% CI excludes 0;
- **old law wins** iff point Δ < 0 AND the 90% CI excludes 0;
- **statistical tie** otherwise.

**The verdict table counts cells won by candidate / old law / tie, every cell printed, the cells the
candidate loses included and given first-class treatment — if the old law wins anywhere, that is the
headline of the packet.** The PRIMARY verdict block is the ND arm, N = 1..6 × 2 horizons × 2 metrics
(24 cells). Slices are scored by the same rule and all reported.

**Pedigree's own verdict:** for each primary cell, pedigree standalone (P-a raw pick; P-b frozen v0)
gets the same Spearman + bootstrap CI. "Pedigree is an effective predictor at N" is declared iff the
90% CI on its own ρ excludes 0. The packet reports, side by side: pedigree alone, old law, candidate
— so the owner sees the real pedigree signal and what each machine adds to or subtracts from it.

## 6 · MECHANICS

Scorer: one read-only script in this directory (`s4_shootout.py`), pure numpy/scipy on the two JSON
matrices; no engine import, no board build, no store write. Environment: pinned venv
`/root/rl_venv312`, five-var thread pinning, `PYTHONHASHSEED=0`. Outputs: `RESULTS_S4.json` (every
cell, every CI), `PACKET_S4.md` (owner-readable verdicts). Push-per-step to `land/order-29`.

*Filed by seat S4 before any comparison number existed. The prereg binds.*
