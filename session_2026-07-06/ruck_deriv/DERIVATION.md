# RUCK VALUES DERIVED OFF PRODUCTION — derivation (BATCH2, 2026-07-06)

**STATE:** CONTROL = BAKED v2.5 `efea88e5` · CURRENT = candidate `<engine head>` (this branch), store `e1b4d8bf` (UNCHANGED).

## The problem
The v2.5 ruck lever `RUC_PRIOR_CAP=1.4` capped a real ruck's value at `1.4 × draftval(p)`, where
`draftval = MA.PVC[effpk]` is the **draft-pick capital** of the player's slot — a flat multiple of a
*pick* unit standing in for a *production* value. That blends heterogeneous units under one dial.

## The swap (single lever)
The **production leg** of `ev()` for a real ruck (the prior-dominated regime) is now capped at a ceiling
**derived off ruck production** instead of off pick capital. Two hook points existed; the V0 draft-prior /
floor **scaffold (hook A) is left byte-identical** and only the **production leg (hook B)** is re-based —
see "Scope" below.

### Production statistic
`x = bestlvl(p)` — the games-qualified (`games ≥ 6·fE`), era-normalized **peak season level** (`_merged_recover.py:246`).
A pure production unit; it is the family the ruck price already responds to (rucks have `wage=0`, so
`raw_ev = price6(p, b6(p))` is a pure production price).

### Production → dollars
`y = ` the engine's **own** ruck pricing of a **standardized developing ruck** — `synth(refpk, avg, 'RUC')`
(2 seasons @ that avg, `:119`) priced through `raw_ev·iso_corr` at a **fixed representative slot**
`RUC_CEIL_REFPK`. This isolates production: no per-player pick, and no age/tenure/exposure noise.
`ceiling(p) = RUC_CEIL_HEAD · y(bestlvl(p))`, monotone non-decreasing in production.

- `RUC_CEIL_REFPK = 72` — the **ruck-median effpk** (the pick-neutral representative slot). Declared; env `RL_RUC_CEIL_REFPK`.
- `RUC_CEIL_HEAD = 0.80` — dimensionless **headroom** on the standardized production price for unproven
  exposure. A multiplier on a *production $*, never on pick capital. Calibrated so the owner's stated
  **Emmett anchor (650–800)** lands mid-range (**724**). The owner's eyeball dial; env `RL_RUC_CEIL_HEAD`.

## Thin-slice smoothing / pooling — DECLARED
The whole ruck slice is **POOLED onto one pick-neutral production→$ curve** (the standardized-ruck pricing),
rather than a noisy per-player empirical fit. An **empirical kernel over live `raw_ev` was tried and rejected**:
`raw_ev` of a live ruck embeds age-fade/tenure/exposure, so it is non-monotone in production (e.g. retired
Goldstein bestlvl 126 → $65; young Jackson 121 → $6803) — an isotonic fit collapsed the low end and crushed
thin prospects (Emmett → $322). The synth strips that noise, so no bandwidth-widening is needed; the "thin"
handling is the deliberate single-curve pooling. **No cross-position pooling** (rucks keep their own pole SCALE
1.13, `wage=0`, own V0 cells — pooling ruck $ with MID/FWD would re-introduce the unit blend).

**No-production fallback:** a ruck with `bestlvl==0` (no ≥6-game season) has nothing to derive from → the
pre-existing prior cap stands → every no-production ruck is **byte-exact**.

## Scope (why hook B only)
The ceiling governs the **production leg only**. The V0 draft-prior/floor scaffold (`_ruc_prior_cap → _v0_raw →
the pooled RUC V0 curve → floor → sit-out → delist scrap`) is byte-identical to v2.5. Reason: re-basing V0
refits the **pooled** RUC V0 curve and moves ~170 rucks — including bestlvl-0, no-game, pickless rucks whose
value must not change off *other* rucks' production. Keeping the scaffold fixed makes this the thin,
production-honest lever the directive asks for: **only rucks whose production is re-priced move**. Re-basing the
V0 prior off production is a larger, pooled-curve change = a later integration step, not this single lever.

## Result (before → after)
Single lever: **non-ruck moved = 0**; **rucks moved = 7 / 217**. Full table: `ruck_deriv_before_after.md`.

| ruck | pick | bestlvl | OLD $ | NEW $ | Δ | note |
|---|--:|--:|--:|--:|--:|---|
| Louis Emmett | 27 | 32.8 | 855 | **724** | −131 | anchor; lands in owner 650–800 |
| Nicholas Naitanui | 2 | 117.5 | 23 | **23** | 0 | anchor; retired → delist scrap, byte-exact |
| Sean Darcy | 38 | 120.2 | 826 | 948 | +122 | elite producer, PVC-suppression removed |
| Reilly O'Brien | 8 | 104.0 | 618 | 783 | +165 | elite producer un-capped |
| Rowan Marshall | 9 | 118.7 | 431 | 612 | +181 | elite producer un-capped |
| Samson Ryan | 42 | 55.4 | 569 | 581 | +12 | |
| Jarrod Witts | 81 | 112.3 | 375 | 384 | +9 | |
| Oliver Hayes-Brown | — | 49.6 | 319 | 335 | +16 | |
| Luke Jackson / Xerri / Grundy / English / Gawn … | | | | = | 0 | proven producers byte-exact |

The DOWN move (Emmett) is thin/weak production honestly priced; the UP moves are elite producers that the
pick-based cap under-valued (low pick → low PVC → low cap) now showing their production.

## Cross-position SANITY (FLAG only — NOT calibration)
Active players; each ruck's $ vs active **non-ruck** $ at matched `bestlvl ±12`. Flags (>1.5× q75 or <0.5× q25):
- **Rich:** Luke Jackson (1.99×), Tristan Xerri (1.76×), Mitchell Edwards (1.73×) — all **byte-exact** (this
  lever did not touch them); elite/young rucks priced above cross-position q75 is a pre-existing property.
- **Cheap:** Jarrod Witts (0.12×, moved +9 only), Darcy Fort, Rhys Stanley — aged rucks with low forward
  value vs prime-age same-peak non-rucks; structural (age), not a lever artifact.

No **absurd** value was introduced by the derivation. Cross-position relativities are **NOT locked** — final
calibration is an integration step (neighbour prices still moving in other jobs). Flags recorded for the owner's
eye; the `RUC_CEIL_HEAD` / `RUC_CEIL_REFPK` dials remain open.

## Reproduce
```
# before→after table + single-lever proof + sanity (needs a frozen OLD-engine base_old.json):
python3 session_2026-07-06/ruck_deriv/scripts/ruck_deriv_ladder.py <base_old.json> session_2026-07-06/ruck_deriv
# self-contained HTML board:
python3 session_2026-07-06/ruck_deriv/scripts/build_board_html.py data/rl_build/rl_app_data.json <base_old.json> session_2026-07-06/ruck_deriv/rl_ruck_board.html
```
