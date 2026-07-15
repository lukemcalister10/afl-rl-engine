# PLAN — SEAT TOOLS (P3): orientation + prescreen readers

**Directive:** Fable supervisor seat · 2026-07-15 · owner-ruled P3. Tier-3 READ-ONLY tooling.
Runs in parallel with the R100.11 rework (S3); fences DISJOINT.

## Fence
- **IN:** `tools/seat/` · `session_2026-07-15/seat_tools/`.
- **OUT (touch nothing):** engine, store, `data/`, `docs/`, CI, `run_panel.sh`, `expected_boot.json`,
  boards, books, and the rework's session dir. The scripts *read* these paths but write none.

## Base
- `git ls-remote` main = `5738f2b2dfbcb7fd746c3c349a09c518d6b541a0` (== the base pin), tag v2.9 =
  `9f8ae761…`. Pin is a floor ("at or after"), not strict equality. `diff pin..main` is empty →
  trivially `docs/`-only. Branch from `5738f2b2`; push to the harness branch
  `claude/seat-tools-orient-prescreen-a7z23x`; open own PR.

## Deliverables
1. `tools/seat/orient.sh` — freshness check (ls-remote + register header + docs listing + pack-doc
   HEADER VERSION table).
2. `tools/seat/prescreen.sh <branch> <base_sha>` — head rev-parse · ancestry verdict · name-status
   diff · board md5 recompute vs pin · expected_boot changed fields · book seal/`__meta__` · run_panel
   pin diff · NEW-ENV-READ CHECK (item 114). ≤35 lines.
3. `tools/seat/gates_score.py <gates_json> [acceptance_json]` — status tally · PICK 1 · B1/G-COHORT
   ratios vs bound · every FAIL with note · named anchors · acceptance scoring by id.
4. `tools/seat/README.md` — cites each house law where it bites.
5. `tools/seat/samples/*.out.txt` — the three PROVE-IT runs, committed.

## House laws wired in
Write nothing (temp `/tmp` only) · every line carries raw evidence · non-zero exit + propagation on
any failure/missing input (SILENCE IS A RED) · canonical URL only · POSIX bash + python3 stdlib only.

## Findings pinned during the build (raw evidence)
- Board md5 = plain `md5sum` of `data/rl_build/rl_app_data.json` (per `boot_guard._md5`); current
  board `3dc19fbb…` == expected_boot pin.
- `gates_fef5719d.json` is NOT at main's base — `fef5719d` is the engine head that was the
  expected_boot base of `claude/board-hardware-independent-az0iz5`; the byte-identical snapshot
  (md5 `20f43e32`) lives in that branch's history and was scored via `git show` into `/tmp`.
- Gates snapshots truncate `detail` at 200 chars → the cohort ratios are not recoverable from the
  file; the scorer reports B1's PASS status and says so. (The one convention that could not be encoded.)

## Verification
- `orient.sh` → exit 0, live SHAs printed.
- `prescreen.sh claude/board-hardware-independent-az0iz5 e7d980eb…` → ancestry YES, board `800bf461`
  MATCH, 27 lines (≤35).
- `gates_score.py gates_fef5719d.json` → B1 PASS, PICK 1 = 3000, FAILs A2/A3/A12.
- Failure paths (missing input, bad branch, wrong argc) all exit 1.
