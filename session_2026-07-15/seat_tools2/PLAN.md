# PLAN — SEAT TOOLS 2: the pen script + standard verifications (item 148)

**Directive:** Fable supervisor seat · register item 148 · 2026-07-15. Tier-3 tooling: cut the
supervisor's per-turn tool+context burn. Parallel per S3; fence disjoint from the trio/captaincy
writers. Pattern = the P3 seat-tools build (item 119): raw evidence, loud exits, committed samples.

## Base
- Pin `90a17c789e744a07fd3b4ad344550ad11e5003a4` verified at-or-before live main
  `9be179a6` (merge-base --is-ancestor YES); `diff pin..main` is **docs/-only** (0 non-docs).
- Branch: `claude/seat-tools-pen-script-xyml9b` (already == live main head).

## Fence
- **IN:** `tools/seat/` · `session_2026-07-15/seat_tools2/`.
- **OUT (read-only-fence, Tier 3):** engine, store, `data/`, `docs/`, CI, `run_panel.sh`, boards,
  books. The scripts *read* these; they **write nothing** except pen.py's single intended commit.

## Deliverables
1. `tools/seat/pen.py` — the register pen, mechanised.
   - `append --item-file F --header-summary "…" -m MSG` → insert F's item text **before**
     `## FABLE'S QUEUE`; bump header `vN → vN+1` (date kept); rewrite ONLY the PEN summary's leading
     segment, keeping a trailing `· prior: <old first clause>` pointer (headers stay SHORT);
     **ASSERT every replacement count** (item-147 law); assert new_v == old_v+1; assert item numbers
     unique; `git add` the register only, commit MSG, push `HEAD:main` with `PEN_TOKEN` (env only,
     never echoed / never written); re-read pushed header first-200 + print new main SHA +
     `git diff --name-only` proving docs/-only. ≤12 output lines.
   - `--register PATH` (default docs/OPEN_ITEMS_REGISTER.md) + `--dry-run` (all asserts, NO
     write/commit/push) — for safe green-path + red-path samples against fixtures.
   - `verify` → header version + item-count sanity + duplicate-item scan. ≤6 lines.
2. `tools/seat/board_diff.py <revA> <revB> [--names n1,…]` — reads
   `data/rl_build/rl_app_data.json` at two revs (git show): mover count · ΣΔ num-SCAR (`active[].v`) ·
   age-bucket ΣΔ (≤22 / 23–26 / ≥27, head age) · top-3 cuts + top-3 lifts · `--names` rows before→after
   · PICK 1 both sides (`picks n=1`) · pair-2 / pair-3 ratios (pick2/pick1, pick3/pick1). ≤15 lines.
3. `tools/seat/gates_brief.py <gates_json> [acceptance_json] [--full]` — wraps gates_score: tally ·
   PICK 1 · B1 status · FAIL ids one-per-line (notes only with `--full`) · standing-fails cross-checked
   vs `acceptance.standing_fails` (STANDING-FAIL) → any UNLISTED FAIL flagged **NEW-DEFECT**. ≤10 lines.

## House laws (P3, carried forward)
Writes nothing (except pen.py's one commit) · every line raw evidence · loud non-zero exit +
propagation (SILENCE IS A RED) · python3 stdlib + git only · committed known-good samples.

## pen.py safety
- `PEN_TOKEN` checked EARLY (before any write) on the real push path; never echoed, never file-written;
  push URL built in-memory, errors sanitised of the token.
- Red-path proofs committed: (a) assert_replace matching 0 or 2 → HARD FAIL before any commit;
  (b) `PEN_TOKEN` unset → loud fail, nothing token-shaped printed, no write.

## Facts pinned during build
- board num-SCAR = `active[].v` (Josh Ward v=1649, Paul Curtis v=1518 vs gate A2 read 1735/1555 at the
  fef5719d snapshot head — same field, different head). PICK 1 = `picks[n=1].v` = 3000.
- `acceptance_v1_15.json` `standing_fails` = A2/A3/A12 STANDING-FAIL (A9 RESOLVED-IN-CANDIDATE).
- `gates_2030e5df.json` FAILs = A2/A3/A12 → clean known-good for gates_brief (all standing, 0 NEW-DEFECT).
