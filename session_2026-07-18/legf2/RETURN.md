# LEG F2 — RETROSPECTIVE BOARDS (−1/−2) · RETURN

- **Branch:** `claude/legf-retrospective-boards-cyqx00` (parent = MAIN `240c7378`) · **PR:** REPORT-ONLY / DO-NOT-MERGE.
- **Base (provenance-by-stamp, item-338):** store `968de0c7` ✓ · curve payload `89c14729` ✓ · engine cc58570 `6ad07bb2` · balanced board `06d8af60` reproduced BYTE-EXACT. Read READ-ONLY via out-of-tree worktree; fence held (writes = `session_2026-07-18/legf2/` only).
- **Effort band:** High, ~1–2 h — actual on band.
- **PLAN gap verdict: NO GAP** — the engine priced every on-board member (−1: 772/772, −2: 777/777). Membership as recorded (`_on_board`: `_last_listed`/debut/last-game); evidence = scoring truncated to ≤Y; nothing reconstructed by guess.
- **Artifacts (stamped DERIVED, for F1's UI tab):** `out/board_minus2_2024.json` `2c37e9d1` (777, Σ770,987) · `out/board_minus1_2025.json` `d223d8f6` (772, Σ771,152) · `out/board_now_2026.json` `ad0c6610` (804, Σ752,427). Bridge, PLAN, VERIFICATION, BOARDS_VIEW, ENTRY_PROOF alongside.
- **Bridge (actual vs band):** −2 771k → −1 771k → now 752k — within ~2.5%; the recent past looks like the past (value converts, does not vanish). Movers sane: young guns ascend −2→−1 (Thilthorpe +4073, Bailey Smith +3841, Ash +3278).

## The one most decision-relevant finding per board
- **−2 (2024):** the shipped board shows retired/left contributors at **scrap** on the years they were stars (`delisted()` is not Y-aware → back-row lens = `ev(p,2026)` ≈66). This build recovers them to real as-of value — 10 retired-now rows carry v>1000 (Jeremy McGovern 3078, Joe Daniher 2227, Steven May 1925). Biggest correction lands on −2.
- **−1 (2025):** the shipped *active* backward lens **leaks the future** — `raw_ev` (W4 context) reads `year>Y` rows, so 451/1608 non-retired members drift (max |Δ|=676 ≈10%). This build truncates → leak-free. The cumulative `games` field itself does not feed `ev`; the real §5.9 trap is future *rows*.

_Findings, not verdicts — these boards never gate and never re-litigate a sealed read._

IN PLAIN TERMS: I rebuilt what the board would have said at the end of 2024 and 2025 using only what was known then, and found the live −1/−2 lens quietly mis-states two things — retired stars vanish and current players' past values peek at the future — both fixed in these read-only boards.
