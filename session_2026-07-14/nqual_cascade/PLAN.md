# PLAN — THE nqual CASCADE: trace the 10-game bar, the ramp and the cliff as one mechanism

**Seat 6 · 2026-07-14 · Tier 3, READ-ONLY.** Measure only. Propose no lever. Wire nothing.
File-disjoint from the q97m follow-up (STORE/ENGINE writer). Parallel, S3.

## Board of record (named beside every figure)
- tag `9f8ae7616555ce55c67ae2076247662960b731e5` (v2.9)
- board `81e48293e4a47309567c47f392eda1fc` (`rl_app_data.json`)
- store `b0c39d788119d541f360e9ee91851a55` (`rl_model_data.json`)
- engine `2030e5df7bdfcf2b9e801c3d2fe3b83b` (`_merged_recover.py`)
- Guard 5 PASS. Working checkout is `main@a9e5186` with the item-20 store `340a7a32`; the engine
  code (`_merged_recover.py`, `rl_model.py`) is **byte-identical** tag↔main, so the board of record is
  reproduced by pointing the engine at the tagged store `b0c39d78` in a scratch workspace.

## Method
1. Scratch workspace in `/tmp` (never committed): seed the bootstrapped `rl_after` engine, overwrite the
   store with the tagged `b0c39d78`. Run every measurement from there.
2. **Board reconstruction verified byte-exact:** the harness prices all 804 shipped players and matches
   `rl_app_data.json` field `v` with **maxdiff = 0** (804/804). Basis identity independently confirmed:
   the census counters reproduce exactly — `n∈{1,2,3}=545` and cliff `n=3(137)+n=4(116)=253` (item 88).
3. **T1** — every player's `n=_nqual(p,2026)`, regime, pedigree par `_par_prior`, `_lvlcurr`, shipped
   level `cp._lvl_eff`, shipped value `round(ev/1.0524)`. Counts per regime.
4. **T2** — split the "within one game of the bar" population into completed-season vs in-progress (2026)
   proximity; quantify the effective mid-season bar (`SEASON_FE=0.58`, R14/24).
5. **T3 cliff ledger** — **pure counter-tick** repricing: monkeypatch `_nqual → n+1` for one player in the
   scratch harness (holds every level input fixed; ticks only the counter) and read `ev`. This isolates
   the regime switch = the cliff height exactly, for *every* player regardless of games-distance, and so
   captures the proration-channel anchors (Tsatas / O'Driscoll / Cadman) that no literal 9→10 game bump
   would. Ranked by |ΔSCAR|. Boundaries 0→1 (switch ON) and 3→4 (VANISH) especially; anchors flagged.
6. **T4** — pedigree worth per blend player (n=1..3): counterfactually collapse the blend to pure current
   level (`_par_prior → _lvlcurr`) and reprice. Δ = who is held UP / held DOWN, in SCAR.
7. **T5** — walk-forward, leak-free: does the record (`_lvlcurr`, ≤Y) predict realised forward output
   (avg over Y+1..Y+3) better than the pedigree (`_par_prior`), as a function of evidence (nqual, games)?
   Optimal record weight `w*` per bin (cluster-bootstrap over players). Does the data support a 4-season
   cutoff?

Monkeypatching happens only inside the `/tmp` measurement harness against an exec'd copy of the engine —
the committed engine is never touched. All writes are confined to this directory.
