# THE CHAPTER BAKE + PROMOTION (v2.10) — PLAN OF RECORD (first committed artifact) · 2026-07-15

Auto-mode. This PLAN is committed FIRST, before any pin/stamp change. It enumerates the fenced bake
steps and the acceptance each proves. Precedent: `session_2026-07-13/v2_9_bake/PLAN.md`.

## THE WORD (in-repo authorization)
Owner, verbatim (register item 162): **"(i). Both in parallel."** — the BAKE WORD, given after the
owner viewed board (`790136a3`) + book (sealed `99be9b36`) vs his sealed reads; the one raised read
(older guns) was resolved by measurement (items 161–162, no absolute-band miss named). **Authorizes:
bake · tag `v2.10` · promotion merge to main.** The parallel form-conditioned aging measurement is a
SEPARATE Tier-3 job — not this one.

## BASE VERIFY (done — Task 1)
- Full-URL `ls-remote`: candidate `claude/l-captain-curve-wire-r98a1` = `9be07b8e5939eeade71106ef1eaee112df183441` ✓ (== directive base, PR #94). main = `77683f5`.
- Fresh bootstrap from the candidate head. **Guard 5 GREEN**, every directive pin asserted with a printed verdict:
  store `b1fd0bce` · engine `fc7045d6` · rl_model `f79fc740` · q97m `cfdc7321` · cm_400 `34faa865` · config `c2d233ae` (manifest_hash) · board `790136a3` — all == `data/expected_boot.json`.
- main-guard: `git diff --name-only 1beec25..main` = docs-only (`OPEN_ITEMS_REGISTER.md`) ✓.
- Promotion merge de-risk: merge-base `7e2e1ed`; candidate touched **0 docs/**; the set of files changed on the
  main side (docs/ + seat-tooling) and the candidate side (engine/data) is **DISJOINT** (empty intersection) ⇒ the
  candidate→main merge commit is conflict-free. Store lineage is FORWARD: `340a7a32 → b1fd0bce` (trio, item 149)
  → captaincy `790136a3` (item 151); the promotion advances main, it does not regress it.

## MECHANISM MAP (verified by reading the code)
- **The captaincy head already re-pinned `expected_boot` (board `800d0399→790136a3`, rl_model `→f79fc740`) and
  committed `gates_fc7045d6.json`, but `repin.py` copied the board to `data/rl_build/` WITHOUT re-stamping the
  sidecar** — so `data/rl_build/rl_app_data.json.srcmd5` still carries `own_md5 800d0399` (the pre-captaincy board)
  while its `source_md5 b1fd0bce` is correct. This is item 158, the defect THIS job fixes.
- **Stamping path** = `engine/rl_after/single_source.stamp_derived('rl_app_data.json', tier=1)`: recomputes
  `own_md5` = md5(board content) and writes `source_md5` = md5(store). Run against the committed board (`790136a3`)
  + bootstrapped store (`b1fd0bce`) ⇒ `own_md5 790136a3`, `source_md5 b1fd0bce`. Board CONTENT is never touched
  (asserted byte-identical, `790136a3` both sides) — **zero movers**.
- **Gates** read engine `ev()` on the FROZEN q97m (`cfdc7321`, never refit) against the frozen board — deterministic.
  Regeneration reproduces the committed captaincy verdicts. Run ship-gates with **NO `SGC_*` env** (item 151: the
  `SGC_REPORT_DIR` leak 0-byte'd subprocess regens on both the trio and captaincy builds).

## THE BAKE STEPS (fenced; per-task commits; each proves itself)
1. **[done] Fresh bootstrap + Guard 5** — all pins asserted.
2. **Item-158 sidecar re-stamp** — `stamp_derived` on the committed board/store; write
   `data/rl_build/rl_app_data.json.srcmd5` with `own_md5 790136a3`, `source_md5 b1fd0bce`. ASSERT board md5
   `790136a3` before AND after (zero movers). Commit with both md5s printed.
3. **Panel re-pin + stale-prose refresh** — `PANEL_EXPECTED.txt`, `run_panel.sh` numéraire pins, and every stale
   prose annotation naming a superseded board hash (e.g. `800d0399`) in the bake-scope files. Panel must read **10/10**.
4. **Regenerate the ship-gates snapshot** on the frozen q97m ⇒ `data/gates_snapshots/gates_fc7045d6.json`. Expected:
   **B1 HALT at the frozen 1.30** with **y5 = 1.3057** (report BOTH bounds: the 1.30 verdict AND the 1.335 clearance,
   margin **0.0293**; waiver authority = item 159, not the suite). FAILs must be **exactly A2/A3/A12 (+ pair-3)**;
   ANY other FAIL ⇒ HALT, no bake. Commit.
5. **Tag `v2.10`** at the bake head. Owner pushes tags — attempt the push; if push rights require the owner, hand the
   exact command over.
6. **Promotion merge to main** — merge commit (candidate line reconciled onto the pen's docs line; never force). Verify
   CI GREEN on the AMD runner printing board md5 `790136a3` (R100.7). CI not green or a different md5 ⇒ report, no retry-loop.
7. **RETURN ≤30 lines.**

## FENCE
IN: exactly tasks 1–7; writes limited to the sidecar re-stamp, panel/prose pins, the gates snapshot, the tag, the
promotion merge, and this session dir. OUT: ANY store/engine/config/value change (zero movers — asserted at task 2) ·
ANY `docs/` authoring (the pen owns docs; the 1.30 waiver reversion is the supervisor's seam task) · gate edits · the
censuses · the form-conditioned aging measurement (separate parallel Tier-3 job). Scope growth ⇒ STOP and return.
