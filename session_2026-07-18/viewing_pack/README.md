# THE VIEWING PACK — seat 13 · 2026-07-19 · README (artifact → provenance map)
### Tier 3 · **REPORT-ONLY / DO-NOT-MERGE** · READ-ONLY · changes NOTHING, never bakes · THREADS=1

## STATUS: RENDER HALTED (reproduction precondition, item 366)

The mandatory reproduction precondition (build the balanced board, assert == filed `06d8af60` byte-exact) was
run first and **failed**: this container builds `83a4b21d` (Σv 750,159), a deterministic **weather instance**
(item 374). Per item 366 the pack renders **only on a reproducing container**, so the board (§1) and the fresh
Rozee/Reid re-render (§2) are **HELD** and no UI board HTML is emitted. Full evidence:
**`REPRODUCTION_PRECONDITION.md`** and **`out/`**. This README maps every pack section to its committed source
and provenance so the owner still sees the full evidentiary state.

Provenance tags: **owner-seen** (already before the owner) · **re-runnable** (rebuildable on a reproducing
container) · **report-only** (a view, never gates/bakes).

## PACK SECTIONS → committed sources @ `15a9abd`

| # | section | committed source(s) | provenance | render state |
|---|---|---|---|---|
| 1 | **THE BOARD** (ranked board, balanced `06d8af60` line, per-row Δ-vs-v2.10) | built from `engine/rl_after/` @ 15a9abd; UI = `ui/app/board.js` | re-runnable | **HELD (weather; item 366)** |
| 2 | **THE MOVERS** + **Rozee/Reid re-render** + raw-pick benefit-of-doubt (item 344) | `session_2026-07-18/lege/out/movers_report.txt`, `lege/scripts/movers_report.py` (Leg-E era — to be **superseded** at head) | owner-seen (Leg-E) / re-runnable (head) | **HELD re-render; Leg-E figures available by ref** |
| 3 | **THE LENS VIEW** (bal/+1/+2 with & without phantom; −1/−2 retro; the bridge) | `legf5/out/lens_totals.txt`; bridge `legf3/f2_boards/bridge_totals.json` (−2 **770,987** → −1 **771,152** → now **752,427**); retro boards `legf3/f2_boards/board_minus{1,2}_*.json` | report-only | committed (by ref) |
| 4 | **THE RIDERS (i)–(iv)** + the three R candidates (R_realized **207** [184–229] · R_owner **220** · R_curve **471**; item 343) + gross/net p1/p60, p1/p90 | R-frame `legf1/PLAN.md`, `legf1/sealed_strawman.json`; rider probes `legf3/out/probe_rows*.json` | report-only | committed (by ref) |
| 5 | **THE GATE + AUDIT LEDGER** (gate values vs thresholds; five-shard audit, item 375, all green; two lineage-split findings; the known guard-5 pre-bake red) | gate `legf5/out/gate.txt`; audit verdict `docs/OPEN_ITEMS_REGISTER.md` (item 375, **HARD-OUT — reference only**); guard-5 red = rl_model `cc626d7d` ≠ boot pin `f79fc740` | report-only | committed (by ref) |
| 6 | **THE RATIFICATION LIST** (owner's calls + seals) | entrant structure seal **`a17aafed`** (`legf5/sealed_entrant_structure.json`); φ pedigree `fd92b6fc`; r_pop **`c62b5ee8`** + s(age) `efe97ee3` (`legf4/sealed_rate_pop.json`); posture presets `c2e17c49`; knife-edge = item 374 (weather, downgraded) | owner-seen | laid out below |
| 7 | **RENDER** (UI board HTML + companion markdown) | existing `ui/app` pipeline (read-only) | — | **HELD (depends on §1)** |

## §6 — THE RATIFICATION LIST (laid out; the owner rules at the viewing)

Each item: what it is · measured value/seal · what ratifying vs re-ruling changes · recommendation (findings, not
verdicts — the owner decides). Full gate/audit numbers live in the §5 sources above.

- **Tail read — STAND / RETIRE.** The L-SYMMETRY fallers tail (e.g. Jagga Smith 3512→924, Gulden 5857→3964 on
  +1). Ratify STAND ⇒ the forward-lens decline bar holds as shipped; RETIRE ⇒ re-open the damper.
  *Recommendation: STAND* — both conservation gates PASS ±5% with the tail in place. Changes if the owner
  rejects symmetric decline.
- **R = 207 free-intake basis** (R_realized 207 [184–229] vs R_owner 220 vs R_curve 471, item 343). Ratify 207
  ⇒ the entrant/free-intake layer is priced at the realized rate. *Recommendation: 207* (measured basis).
  Changes if the owner prefers the curve-implied 471 or the round 220.
- **Entrant structure `a17aafed`** — sealed intake 83,538 PVC (draft 69,266 + mech 14,272), 103.4 slots/yr,
  measured from 2019–2025 history, sealed pre-render (not tuned against the gate). *Recommendation: ratify.*
- **φ pedigree `fd92b6fc`** · **r_pop `c62b5ee8`** (+ s(age) `efe97ee3`) · **posture presets `c2e17c49`** —
  sealed inputs, unmoved across F3/F4/F5. *Recommendation: ratify (seals verified present + unmoved).*
- **Raw-pick benefit-of-doubt** (item 344) — the raw-pick rows surfaced for the owner's ruling (source: §2
  movers, currently HELD at head). *Recommendation: defer to the owner; no engine effect either way.*
- **Knife-edge note (item 374)** — **downgraded: weather, not brittleness.** This viewing's own precondition
  reproduced the weather exactly (Sheezel −95, 9/10 within ±3, deterministic). *Recommendation: ratify the
  downgrade* — the delta is container weather in the unedited base (item 347), not model brittleness.

## FILES IN THIS PACK

```
session_2026-07-18/viewing_pack/
  README.md                        this map + §6 ratification list
  REPRODUCTION_PRECONDITION.md     the item-366 HALT report (precondition result first)
  out/
    reproduction_precondition.txt  git entry + provenance stamps + build md5s + weather panel
    exportlog_balanced.txt         the RL_LEGF=0 build log (parity gate PASS, src=968de0c7)
    md5_ledger.txt                 board md5 ledger
```

## FENCE / LAW

IN = `session_2026-07-18/viewing_pack/` ONLY. No engine/store/curve/docs file was edited (HARD-OUT). The board
was built in an isolated scratch copy; the repo tree carries no build artifact. Report-only, do-not-merge:
this pack informs the viewing, it never pre-empts the owner's ruling.
