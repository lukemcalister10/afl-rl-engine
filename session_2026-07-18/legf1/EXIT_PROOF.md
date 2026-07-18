# LEG F1 — PHANTOM INTAKE LAYER — EXIT PROOF
All lines produced this session · container py3.12.3/np2.4.4/scipy1.17.1/sklearn1.8.0 · OpenBLAS 0.3.31
DYNAMIC_ARCH · **dev-shell recipe, single-thread pinned** (`OPENBLAS_NUM_THREADS=1` … — determinism).
Candidate: `rl_export.py` (phantom block) + `ui/app/board.js`; engine (`rl_model.py` cc626d7d /
`_merged_recover.py` 6ad07bb2) **UNTOUCHED**.

## 1 — THE GATE KILL-SWITCH (RL_LEGF=0 ⇒ Leg-E byte-exact) — PASS, filed absolutes
| env (single-thread) | md5 | filed | verdict |
|---|---|---|---|
| RL_LEGE=1 RL_PVC2=1 **RL_LEGF=0** | `d85901af` | d85901af | **PASS byte-exact** (the Leg-E lens board) |
| RL_LEGE=0 RL_PVC2=1 RL_LEGF=0 | `06d8af60` | 06d8af60 | **PASS byte-exact** (the balanced board) |
| RL_LEGE=0 RL_PVC2=0 RL_LEGF=0 | `9829d01a` | 9829d01a | **PASS byte-exact** (RL_PVC2 kill baseline) |

## 2 — THE CHECKPOINT LAW: the balanced board CANNOT move — PASS (0 movers)
`RL_LEGF=1` (default) board = **`e613ca58`**. Keyed diff vs the `d85901af` board (`out/board_legf0_*` vs
`out/board_legf1_phantom.json`):
- keys ADDED by RL_LEGF=1: exactly `phantomLayer`, `phantomPicks`, `phantomTotals` (purely additive).
- shared top-level keys changed: **0**. Active rows: **k=0 `v` movers = 0**; any-lens value movers
  (v/vP1/vP2/vM1/vM2) = **0**; whole-active-row byte movers = **0**; `back` rows byte-identical.
The engine is untouched and the phantom keys are lens-scoped arrays ⇒ the balanced board is byte-untouched
**by construction**, not merely by proof. k=0 phantom content = NONE (the `phantomTotals.clubs[*]["0"]`
echo shows WITH == WITHOUT, Δ=0).

## 3 — THE PHANTOM LAYER (MEMO_LEGF §2; sealed strawman sha256 1d180424, hashed before render) — BUILT
- §2.i DRAFT CAPITAL: 60 rows (picks 1..30 × 2 lenses), PVC v2-curve GROSS, natural-order round-robin over
  the 18 clubs, every row `phantom=true`.
- §2.ii FREE INTAKE + §2.iii EXITS (list-size conservation): per club per +k lens, `vP_k<X(207)` exit
  (residual leaves the club total); freed slots refill draft-then-free at R=207; refill count == exit count.
- §2.v TOTALS (`out/phantom_totals_report.txt`): league +1 Σ 537768→618248 (**Δ +80480**, 366 exits) ·
  +2 Σ 393375→485937 (**Δ +92562**, 436 exits). Per club + league, per lens, WITH/WITHOUT; per-pick, no bins.
- The single structural strawman (draft picks CONSUME exit slots, memo §1 reading) is FLAGGED in the seal
  for owner ratification at the viewing.

## 4 — FROZEN SUITE (S4) / SSI GUARDS (`one_source_selftest.py`, RL_LEGF=1, single-thread) — GREEN but the expected RED
`out/selftest2.txt`: **F1 EXPORT PARITY (board v == round(engine gated ev/1.0524)): PASS, mismatches=0**
(the value regression tripwire — the phantom layer moved no value). GUARD 1/2/3 PASS (board stamp ==
source `968de0c7`; single-source; read-only). **GUARD 5 boot-store: FAIL (EXPECTED)** — `rl_model cc626d7d
!= pinned a5fd3d7d` (and `_merged 6ad07bb2 != 40f43772`): the **known pre-bake class**, identical in kind to
the Leg-E and five-migration EXITs; the pin re-stamps AT THE BAKE. Flagged, **never self-pinned**.
Book parity (F2 `s4_matrix`) NOT rebuilt this session — the engine/book valuation path is UNTOUCHED, so the
book is byte-identical to Leg-E's `a7cbe374`; the value tripwire (F1 parity) stands green.

## 5 — HARD-OUT HELD + STORE — PASS
Diff vs `cc58570` touches only `engine/rl_after/rl_export.py`, `ui/app/board.js`, `session_2026-07-18/legf1/`.
UNTOUCHED: store `rl_model_data.json` (**968de0c7** at entry and exit) · curve `pvc_curve_v2.json`
(**56dd7a7b**) · `_merged_recover.py:1121-1171` · `rl_model.py` · `distribution_pricing.py` · pins/acceptance ·
`docs/` · SEASON_PROG · F2's session dir. Derived fence NARROWER than "expected" (engine deliberately out).

## 6 — THE HEADLINE RECONCILIATION FINDING (supervisor item 347)
The filed board hashes reproduce **byte-exact only single-threaded**. Multi-threaded OpenBLAS (DYNAMIC_ARCH)
has non-fixed cross-thread reduction order → run-to-run last-ULP jitter in 6-dp float display fields → a
wandering whole-board md5. Discriminator (`out/discriminator.txt`): the filed 10-value panel reproduces
**10/10, max|Δv|=0, 0 rank moves** — the jitter never touches integer `v` (valuation/ranking). Reproducibility
annex committed. **Any bit-exact board gate in this repo must pin `OPENBLAS_NUM_THREADS=1`.**

## VERDICT
Phantom intake layer built and gated (RL_LEGF, default ON); RL_LEGF=0 reproduces the Leg-E boards
byte-exact (filed d85901af / 06d8af60 / 9829d01a); the balanced board is byte-untouched (0 k=0 v-movers,
engine untouched); totals WITH/WITHOUT reported per club+league; UI flags phantom rows and adds empty-state
-safe F2 tabs. Frozen suite green but the expected Guard-5 pre-bake red. Store/curve/docs HARD-OUT held.
Sealed strawman (R=207/X=207) ratifiable at the viewing; one structural choice flagged. Candidate ready.
