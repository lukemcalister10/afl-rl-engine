# HALT — VIEWING-PACK RENDER · reproduction precondition FAILED · seat 14 · 2026-07-20

**Status: HALT (halt-not-warn). The viewing pack was NOT rendered.**
The directive gates every board on a precondition: *"before rendering any board, build the
balanced board with `RL_LEGE=0 RL_LEGF=0` and assert it == `06d8af60` byte-exact … If it does
NOT reproduce, HALT and report — the pin is insufficient on this container → we pin deeper
(item 392 gate). This render reproducing `06d8af60` IS the container-#2 leg of the gate."*

The precondition **did not reproduce**. This report IS the container-#2 gate result.

## Gate result — RED
| leg | container | recipe | balanced board md5 | verdict |
|-----|-----------|--------|--------------------|---------|
| #1  | env-pin build (commit 3055ea5, item 392) | `RL_LEGE=0 RL_LEGF=0 build_board.sh` ×5 | `06d8af60` ×5 | PASS (recorded) |
| #2  | **this fresh container, pinned env** | **identical recipe** | **`d7a95e8d`** | **FAIL** |

`d7a95e8d != 06d8af60` → the two-container reproduction gate (item 392) is **RED**. Per the
directive and the env-pin EXIT_PROOF's own "THE ONE GATE" clause, this means **the wheel pin is
insufficient on this container → pin deeper**.

## Pre-gate checks — all GREEN (this is not a setup failure)
- `bash bootstrap.sh` — **ENV-PIN assert PASS**; Guard 5 PASS (store `b1fd0bce`, q97m `cfdc7321`,
  register `652d83e8`, rl_model `f79fc740` all == pinned).
- `git ls-remote origin claude/env-pin-2026-07-19-4y4w0p` = `3055ea5ffdc390f81d5e17476a60fbb841f24cff`
  — STRICT match, base verified.
- Board built at the **F6/env-pin head `3055ea5`** (via a detached git worktree — the working branch
  carries the later F7/one-source engine `fc7045d6` which has **deleted `data/v0surf.pkl`**; building
  there would be wrong). The worktree has `v0surf.pkl` (24967 B) and it **LOADED** (no error).

## The recipe was faithful — the divergence is real, not operator error
Invocation is **byte-for-byte** the container-#1 canonical confirm recipe
(`session_2026-07-19/envpin/scripts/confirm_5of5.sh` → `build_board.sh`): `RL_LEGE=0 RL_LEGF=0`,
`PYTHONHASHSEED=0`, single-thread BLAS/OMP, `RL_REPO` set, **no `RL_CONFIG_MODE`** (dev-shell), fresh
engine copy into a private workspace, `python3 rl_export.py`, `md5sum rl_app_data.json | cut -c1-8`.
The 3055ea5 engine confirmed reads both gates (`_merged_recover.py:198` `RL_LEGF`, `:1252` `RL_LEGE`).

Container-#2 export log agrees with container #1 on every structural stamp:
- `board stamped src=968de0c7 (read-only)` — matches the directive provenance stamp.
- `exported active=804`; `PARITY GATE PASS: all 804 active board values == engine gated ev() (eps=0)`.
- `LEG F5 ENTRANT LAYER: RL_LEGF=0 — layer NOT emitted (Leg-E board byte-exact)`.

Only the **value path** moved:

| metric | container #1 (`06d8af60`) | container #2 (`d7a95e8d`) |
|--------|---------------------------|---------------------------|
| n (active) | 804 | 804 |
| Σv | 752,427 (EXIT_PROOF confirm line) | **750,171** |
| Sheezel v | 7964 | **7869** |
| top-6 lead | (default panel: Daicos) | Luke Jackson 8611 > N.Daicos 8014 > Sheezel 7869 > Xerri 7633 > Holmes 6929 > Treacy 6713 |

The spread (Σv −2,256 across 804 rows; ~95 on Sheezel) is consistent with the item-391 `np.interp`
**amplifier** riding the load-time calibration refit — the exact rank-unsafe mechanism the pin was
meant to remove.

## Why the pin didn't hold — the environment is byte-identical yet the board diverges
This is the dispositive point. The pinned numpy binary + BLAS are **identical** to container #1, and
it still diverged:
- numpy **2.4.4**, the pinned wheel (bootstrap's fail-closed hash assert PASSED against the lock
  `numpy==2.4.4 --hash=sha256:81f4a14b…`).
- bundled OpenBLAS `numpy.libs/libscipy_openblas64_-32a4b2a6.so` sha256 **`05c9f9eb`** — **byte-for-byte
  the same `.so`** the EXIT_PROOF names for container #1.
- numpy build config: scipy-openblas **0.3.31.188.0**, `DYNAMIC_ARCH … Haswell`, gcc 14.2.1.

The env-pin EXIT_PROOF's sufficiency argument was **inferential**, and it said so:
> **HONEST LIMIT:** every REAL alternate build available on this container … held `06d8af60` — I could
> not reproduce a REAL diverging build … Container #2 = the follow-on viewing render on the pinned env.
> If it diverges → HALT + pin deeper.

Container #2 has now produced the real divergence container #1 could not. Because the numpy wheel **and**
its bundled BLAS are byte-identical here, the residual amplifier is **not fully captured by the numpy
wheel**. The remaining candidate is runtime CPU-microarchitecture dispatch (OpenBLAS `DYNAMIC_ARCH`
kernel selection and/or FMA/AVX dispatch differing on this host's CPU) reaching the value path through a
non-numpy-wheel route — i.e. the pin must go **deeper than the wheel**: a full container/image pin (or a
kernel/`OPENBLAS_CORETYPE` dispatch pin), then a fresh two-container re-run.

## Consequence for the v2.11 bake
The directive states this render "renders the EXACT board that bakes" and is container #2 of the
reproduction gate. With the gate RED, the board of record `06d8af60` is **not reproducible on this
container**, so the viewing must not be rendered as truth and the bake precondition is **not met**.
No player value is disputed by this finding — it is a **determinism/reproducibility** failure, not a
valuation change. Engine / store / curve / q97m / v0surf were **read-only throughout**; nothing was
edited, nothing bakes.

## Findings (owner rules; no verdict pre-empted)
1. **item-392 two-container gate: RED.** Balanced board `d7a95e8d` (container #2) ≠ `06d8af60`
   (container #1), same recipe, same head, byte-identical pinned numpy wheel + bundled BLAS.
2. **The wheel pin is necessary but not sufficient.** The amplifier survives a byte-identical numpy
   binary → the divergence source is outside the pinned wheel (most likely OpenBLAS `DYNAMIC_ARCH`
   runtime kernel dispatch / CPU microarch).
3. **Recommended next step (the directive's own contingency): pin deeper** — container/image pin or an
   explicit BLAS core-type/dispatch pin — then re-run the two-container gate before any viewing render
   or v2.11 bake. What would change this: a deeper pin that holds `06d8af60` byte-exact on ≥2 genuinely
   different containers.

## Evidence (this folder)
- `evidence/board_balanced_repro.container2.json` — the container-#2 balanced board (md5 `d7a95e8d`).
- `evidence/exportlog_balanced.container2.txt` — its export log (src=968de0c7, active=804, parity PASS).
- `evidence/env_fingerprint.container2.txt` — numpy/scipy/sklearn versions + bundled OpenBLAS `05c9f9eb`.

READ-ONLY (Tier 3) · report-only · DO-NOT-MERGE · changes nothing, never bakes. Silence is a red;
this HALT is the report.
