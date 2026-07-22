# THE FIVE-MIGRATION — PLAN (Leg D consumers → pvc_curve_v2)

**Branch** `claude/five-migration-pvc-consumers-kxykfd` · **base** `e4177c2` (pinned engine head,
stacked PR #105 → #109) · **ruling** R107.5 (DECISIONS v123, on main) · **mode** auto.
**Authorisation (verified by fetch, ENTRY_PROOF.txt):** R107.5 "the five MA.PVC consumers migrate in
a SEPARATE pre-ladder build, per-consumer proofs, pvc_snapshot measured-first w/ post-bake fallback."
This is exactly the census's HALT-flagged fence-extension question — now owner-ruled. No fence
extension is a build's call; this one was already ruled, cited, and re-verified against main.

## The map (from SITE_CENSUS.md @ e4177c2 — the census wins on any disagreement)
`MA.PVC` (the v3.4 ruler, built in `rl_model.py` by `build_pvc_v34`) is **never swapped** by the ACT-2
ev-channel work; `_merged_recover.py` swaps only `_PVC0` (draftval/prior-cap). The five `rl_model.py`
consumers still read the v3.4 ruler. This build wires them to the offline-derived, stamped
`pvc_curve_v2.json` under the existing `RL_PVC2` kill-switch (default ON). `RL_PVC2=0` leaves every
v3.4 path byte-exact (board `9829d01a`, proven at entry and re-proven per commit).

**Design law (census §E verdict + PART 7 + R107.5):** OFFLINE + LOADED, no new import-time fit; the
`RL_PVCADOPT`/L1b template. Concretely: introduce one module-level indirection `_PVC2M` in
`rl_model.py` = the loaded v2 dict when `RL_PVC2` is on, else the v3.4 `PVC` object (same reference ⇒
byte-hold is automatic). Each consumer is repointed `PVC[...] → _PVC2M[...]` **one commit at a time**.

## Job → file map
| Job | Consumer | Site (rl_model.py) | Action |
|-----|----------|--------------------|--------|
| 1 | peak-model `pvc_snapshot`/`_V4PVC` | `:515`, `:530`, `:532` | **MEASURE FIRST** → HOLD frozen unless committed numbers show no retrain needed (memo-C rule). Retrain = POST-BAKE FALLBACK (R107.5). |
| 2 | pickless `unpl_eq` | `:798` | `PVC[min(ep,70)] → _PVC2M[min(ep,70)]` |
| 3 | pedestal | `:813` | `PVC[min(ep,70)] → _PVC2M[min(ep,70)]` |
| 4 | `_natcv34` inversion base (pickless `_eff`) | `:840-853`, `_pick_equiv :848` | pickless pick-equivalent inverted against the v2 currency (exact form fixed at execution from measured scale-consistency; proof attached) |
| 5 | `build_pvc_v34` import fit + `CURVE_H` + `BOARD_FACTOR` + `_deplateau` | `:714-737` (+ residual readers `:721`,`:1094-1096`,`:1103`) | global `PVC := _PVC2M` under flag — the import fit's output no longer feeds consumers; catches the residual value→pick-label reader `:1094-1096`. |

## Sequencing (the census dependency order, resolved for per-consumer isolation)
`build_pvc_v34` (job 5) **produces** the curve `unpl_eq`/`pedestal` **consume**. Swapping the producer
first would collapse three proofs into one (all `PVC` readers move at once). So the producer swap goes
**last**; the leaf consumers are wired first via `_PVC2M`, each showing its own isolated board delta,
and by the time job 5 unifies `PVC := _PVC2M` the leaves are already on v2 (no double-move) — job 5's
delta is only the residual (`:1094-1096` pick-label + `:1103` print). Order: **1 (measure) → 2 → 3 → 4 → 5.**
The `_PVC2M` conduit load is introduced in job 2's commit (first leaf); it is the mechanically-required
carrier of the loaded curve to the `MA.PVC` consumers (the census names the load template
`_merged_recover.py:1336-1342`; here the artifact is loaded in `rl_model.py` itself, as `rl_export.py:61`
already does — no `_merged_recover.py` change is mechanically required).

## FENCE — DERIVED MECHANICALLY FROM the job list (item-322 law)
Union of files the jobs above name:
- **`engine/rl_after/rl_model.py`** — the only engine file edited (all five consumer sites live here).
- **`session_2026-07-18/five_migration/`** — the session proof directory (plan, proofs, measurements, out/).
- Conduit a job MECHANICALLY requires to carry the loaded curve to `MA.PVC`: **none beyond `rl_model.py`** —
  `rl_model.py` loads `pvc_curve_v2.json` itself (READ-only), exactly as `rl_export.py:61` already does;
  `_merged_recover.py`'s load template is the *pattern*, not a required edit (it swaps `_PVC0`, a
  different instrument). If execution reveals a mechanically-required touch of `one_source_selftest.py`
  (EXIT guard wiring, census-IN) that will be added with its own justification; it is IN-fence per census.

**HARD-OUT (asserted, none touched by the plan):** the store `rl_model_data.json` (md5 `968de0c7`) ·
`pvc_curve_v2.json` as a WRITE (READ-only input here) · the V0/`_iso_dec` chain
(`_merged_recover.py:1121-1171`) · `s4_matrix_7147.py:62` anchor · SEASON_PROG (`rl_model.py:738`,
owner dial 0.58 — my edits are at `:515/:714-737/:798/:813/:840-853/:1094`, never `:738`) · `docs/`.
If any job mechanically requires a HARD-OUT file: HALT and return the conflict (never a build's call).

## PER-CONSUMER PROOF TEMPLATE (each of jobs 1–5 carries all)
(a) BEFORE/AFTER board md5 at `RL_PVC2=1` + the affected-row diff (`tools/seat/board_diff.py` on the
    committed board, or the in-session equivalent), **rows NAMED** (counts are not behaviours, item 293).
(b) byte-hold: `RL_PVC2=0` board == `9829d01a` after the commit (unchanged).
(c) one-line WHY per moved row class. A consumer that moves nothing proves the null (hash-equal, stated).
Proof harness (validated at entry): dev-shell build, `RL_REPO` set, `RL_PVC2` toggled; ~110 s/board.
Baseline for job 2 = `270a2c5f` (RL_PVC2=1, no rl_model consumer migrated). Each job's AFTER = next job's BEFORE.

## EXIT (job list step "EXIT")
Full FROZEN repo suite (S4) · SSI guards green · `RL_PVC2=0 ⇒ 9829d01a` byte-exact (third proof) ·
store md5 still `968de0c7` · gates snapshot (`tools/seat/gates_score.py`) committed · candidate PR raised.
Plus the report-only RIDER (items 326/327): engine-side R inputs (free-intake pick-equivalents) as a
committed report — no engine value change, not a gate.

## Time band: ~2–4 h wall (confirmed reasonable: 5 value-moving sites × ~3 board builds each @ ~110 s
+ the peak-model measurement + suite). Flag if actual falls >2× or <½× this band.
