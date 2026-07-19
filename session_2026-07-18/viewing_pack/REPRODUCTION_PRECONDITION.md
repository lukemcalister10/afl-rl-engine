# THE VIEWING PACK — REPRODUCTION PRECONDITION · HALT + REPORT · seat 13 · 2026-07-19
### (Tier 3) report-only · READ-ONLY · changes NOTHING, never bakes · single-thread OPENBLAS/OMP/MKL/NUMEXPR=1

## RESULT (item 366, MANDATORY) — read this first

**The reproduction precondition is NOT met on this container. The board render is HALTED.**

The balanced board built from the audited-head engine on this container is **`83a4b21d`** (Σv **750,159**),
byte-identical across two warm builds (deterministic). The **filed** balanced board is **`06d8af60`**
(Σv **752,427**). `83a4b21d ≠ 06d8af60`, so per item 366 this is a **weather instance** (item 374) and the
pack **renders only on a reproducing container**. No board, no movers re-render, no lens/rider/gate figure that
depends on a fresh board build is emitted from this container. The committed artifacts are mapped in `README.md`
for the owner; nothing is fabricated from the weather board.

This is not a new failure — it is the exact, already-owned outcome the directive anticipated ("if it does NOT
(a weather instance, item 374), HALT and report"). The legf5 leg recorded the same value on its own container.

## GIT ENTRY (read-only variant — item-338 law)

| ref | ls-remote SHA | check |
|---|---|---|
| `claude/legf5-entrant-layer-conservation-p4susl` | `15a9abd996f8f7426e98f173d83a0d600b966a3c` | **STRICT MATCH** — == the item-375 audit-clear head |
| `main` (branch parent, item 378) | `ecb146877ae6c66d35fab5e5288d3501cb86a080` | merge-base(main, 15a9abd) == main HEAD |

`git fetch origin main claude/legf5-entrant-layer-conservation-p4susl` succeeded; the audited head is present and
strict-matched. The pack is assembled at `15a9abd` as directed.

## LOAD-TIME PROVENANCE (built from the audited-head engine — `engine/rl_after/` @ `15a9abd`)

The render must build against the **audited-head** engine, not the boot workspace. The boot workspace
(`/home/claude/rl_workspace/rl_after`) is a *different, boot-pinned* engine (store `b1fd0bce`, rl_model
`f79fc740`); the audited head is store `968de0c7`, rl_model `cc626d7d`. All build inputs were taken from
`engine/rl_after/` and stamp-verified:

| input | measured | anchor | match |
|---|---|---|---|
| store `rl_model_data.json` | `968de0c7` | `968de0c7` | ✓ |
| curve `pvc_curve_v2.json` (file) | `56dd7a7b` | `56dd7a7b` | ✓ |
| curve payload self-stamp | `89c14729` | `89c14729` | ✓ |
| `rl_model.py` | `cc626d7d` | `cc626d7d` | ✓ (the **known guard-5 pre-bake red** — checkout head ≠ boot pin `f79fc740`; flagged, never self-pinned) |
| `_merged_recover.py` | `caf013e2` | `caf013e2` | ✓ |
| `rl_export.py` | `90aa3323` | `90aa3323` | ✓ |

## THE BUILD (dev-shell recipe — `session_2026-07-18/legf1/scripts/build_board.sh`)

Env: `PYTHONHASHSEED=0`, single-thread BLAS/OpenMP (`OPENBLAS/OMP/MKL/NUMEXPR_NUM_THREADS=1`), no
`RL_CONFIG_MODE` (dev-shell), `RL_LEGF=0` (balanced). Built in an isolated scratch copy of the audited-head
engine so **no build artifact is written into the repo tree** (READ-ONLY law). Board hash = `md5sum
rl_app_data.json | cut -c1-8`.

```
warm build 1  balanced md5 = 83a4b21d   Σv = 750159
warm build 2  balanced md5 = 83a4b21d   Σv = 750159   -> BYTE-IDENTICAL (deterministic container)
FILED anchor  balanced md5 = 06d8af60   Σv = 752427
ASSERT  83a4b21d == 06d8af60  ->  FALSE   (WEATHER INSTANCE, item 374)
```

Build integrity on this container was otherwise clean: **PARITY GATE PASS** (all 804 active board values ==
engine gated ev(), eps=0); `board stamped src=968de0c7`; `RL_LEGF=0 — entrant layer NOT emitted (Leg-E board
byte-exact)`.

## WEATHER CHARACTERIZATION (panel: this container vs filed EXPECT)

| player | built | filed | Δ |
|---|--:|--:|--:|
| Nick Daicos | 8014 | 8017 | −3 |
| Marcus Bontempelli | 3896 | 3897 | −1 |
| **Harry Sheezel** | **7869** | **7964** | **−95** ← the weather (one row) |
| Max Gawn | 3415 | 3416 | −1 |
| Harley Reid | 3347 | 3348 | −1 |
| Josh Ward | 2003 | 2003 | 0 |
| Darcy Moore | 257 | 257 | 0 |
| Taylor Goad | 914 | 914 | 0 |
| Josh Smillie | 1323 | 1324 | −1 |
| Will Green | 651 | 651 | 0 |

9/10 within ±3; the whole Σv delta (752,427 → 750,159 = −2,268) is the single Sheezel row plus sub-unit dust.
This is **identical** to the legf5 EXIT_PROOF characterization: the weather lives entirely in the *unedited* F4
base, present before any F5 edit. Item 347 forbids CORETYPE/microarch archaeology to chase it; item 374
downgrades it to **weather, not brittleness** (the "knife-edge" note the owner is asked to ratify in §6).

## WHAT THIS HALTS, AND WHY

The three *fresh compute* items of the pack all sit downstream of a reproducing board:

1. **§1 THE BOARD** (ranked board at `15a9abd`, per-row Δ-vs-v2.10 join) — HELD. Would render off the weather
   board; item 366 forbids it.
2. **§2 THE MOVERS**, incl. the **Rozee/Reid re-render at `15a9abd`** — HELD. The re-render is a fresh
   audited-head board read; on this container it would carry the Sheezel-class weather, so it cannot supersede
   the committed Leg-E figures. The committed (superseded) Leg-E figures remain available by reference.
3. **The reproduction-precondition board build** — DONE (this report); result = weather.

The container-independent, already-committed sections (§3 lens view, §4 riders where committed, §5 gate + audit
ledger, §6 ratification list) are **not fabricated here** but are mapped to their committed sources with
provenance tags in `README.md`, so the owner still sees the full evidentiary state — nothing hidden, nothing
invented. Rendering them *as a board/HTML* is the halted step; reporting *where the committed figures live* is
not.

## TO PRODUCE THE FULL PACK

Re-run this precondition on a container that byte-reproduces `06d8af60`. If/when the assert passes, the render
proceeds off that board (the UI board HTML via the existing `ui/app` pipeline + the companion markdown), using
the committed artifacts mapped in `README.md`. Until then: **HALT — findings, not verdicts; the owner rules.**
