# LEG F BUILD 2 — RETROSPECTIVE BOARDS (−1/−2) · seat 13 · 2026-07-18

READ-ONLY (Tier 3) build. Construction of record: **MEMO_LEGF v1.0 §3**. Runs parallel to F1;
writes ONLY this directory. The boards are DERIVED artifacts for F1's `−1/−2` UI tab. They never
gate, never bake, never re-litigate a sealed read — findings, not verdicts.

## What these are
`−1` (2025) and `−2` (2024) are **history, not projection**: the balanced board **re-rendered at the
recorded evidence state** of each season's AFL lists. List membership is read as recorded
(`_last_listed` ground-truth + debut + last-game proxy — the engine's own `_on_board`); per-season
evidence is the scoring truncated to `year ≤ Y`, cumulative games rebuilt. **No backward phantom
layer — the past's intake actually happened.** Single-source `ev`; same engine as the balanced board.

## Provenance (asserted at load; HALT-on-mismatch) — item-338 provenance-by-stamp
| input | stamp | expect |
|---|---|---|
| store `rl_model_data.json` | `968de0c7` | `968de0c7` ✓ |
| curve `pvc_curve_v2.json` payload | `89c14729` | `89c14729` ✓ (file `56dd7a7b`) |
| engine `_merged_recover.py` | `6ad07bb2` | cc58570 Leg-E tip |
| rl_model.py | `cc626d7d` | cc58570 |
| balanced board reproduced | `06d8af60` | `06d8af60` ✓ (RL_LEGE=0 RL_PVC2=1, dev-shell) |

Commit branch parent = MAIN (`240c7378`); read base = the `e4177c2→a90052a→cc58570` line, imported
READ-ONLY via an out-of-tree git worktree. Zero engine/store/curve/docs edits (fence held).

## Artifact → stamp map
Every board JSON carries a `stamp` block (store md5 · curve payload · engine md5 · code SHA · asof year · numéraire F).

| artifact | md5 | asof | players | Σ value | for |
|---|---|---|--:|--:|---|
| `out/board_minus2_2024.json` | `2c37e9d1` | end 2024 | 777 | 770,987 | −2 UI tab |
| `out/board_minus1_2025.json` | `d223d8f6` | end 2025 | 772 | 771,152 | −1 UI tab |
| `out/board_now_2026.json` | `ad0c6610` | end 2026 | 804 | 752,427 | now (= balanced 06d8af60) |
| `out/bridge_totals.json` | `0905dd52` | — | — | — | bridge machine-read |

## Read files (pipe-tabled, Luke-facing)
- `PLAN.md` — recorded-history enumeration + **gap verdict = NO GAP** (engine priced every member 772/772, 777/777).
- `BOARDS_VIEW.md` — top-30 of each board.
- `BRIDGE_REPORT.md` — −2 → −1 → now totals + top-20 movers each step + churn (entries/exits).
- `VERIFICATION.md` — provenance, the §5.9 leak-free proof, now-board consistency (723/723 == balanced).
- `ENTRY_PROOF.txt` — the entry verdicts (SILENCE IS A RED).
- `scripts/build_retro_boards.py` — the whole build, byte-reproducible under the pinned base + env.

## Reproduce
```
git worktree add --detach <wt> cc58570 && (cd <wt> && bash bootstrap.sh)   # seeds /home/claude runtime
cd /home/claude/rl_workspace/rl_after
export PYTHONHASHSEED=0 RL_REPO=<wt> RL_LEGE=0 RL_PVC2=1 \
       PYTHONPATH=/home/claude/rl_workspace/rl_after:/home/claude/rl_vendor
python3 <repo>/session_2026-07-18/legf2/scripts/build_retro_boards.py
```

## The two decision-relevant findings (findings, not verdicts)
1. **Back-row scrap (the retrospective correction).** The shipped board sets every retired/delisted
   recalled row's backward lens to `ev(p,2026)` = scrap (`delisted()` is not Y-aware). So genuine
   contributors who have since left show ~66 on the year they were stars. This build recovers them:
   10 retired-now players carry v>1000 on −2 (Jeremy McGovern 3078, Joe Daniher 2227, Steven May
   1925, …). The `−2` board is where this matters most.
2. **The §5.9 future-row leak in the shipped backward lens.** The shipped active backward values use
   `ev()` on the *full* player object; `raw_ev` (the W4 context wrapper) reads scoring rows with
   `year>Y`, so 451/1608 non-retired members leak (max |Δ|=676 ≈10%). This build truncates
   (`_trunc_p` semantics) → leak-free. The top-level cumulative `games` field itself does NOT feed
   `ev` — the real trap is future *rows*, not the games field.

Sanity: the boards are within ~2.5% of each other (−2 771k, −1 771k, now 752k) — the recent past
looks like the past; value converts, it does not vanish.
