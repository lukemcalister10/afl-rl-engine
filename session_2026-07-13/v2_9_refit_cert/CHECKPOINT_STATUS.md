# REFIT CHECKPOINT — status (v2.9 refit-certification seat) · 2026-07-13

**This is a committed checkpoint, not the finished refit** (directive: "Thin budget → committed checkpoint + say so";
here: a stop-point landed while the board regen + matrix are in flight). The engine wiring is COMPLETE and VERIFIED;
the panel/board re-pin + full gate-suite certification is the FOLLOW-UP commit. Candidate ONLY (no tag/main/bake).

## DONE + VERIFIED (this checkpoint)
- **All six levers wired on disk, each behind an env kill-switch (default ON):**
  - L1 `RL_PVCADOPT` — `_PVC0` swap + V0/RUC rebuild (`_merged_recover.py:992`, loads stamped `pvc_curve_L1b.json`).
  - L4 `RL_MSD_POOL_EXCL` — MSD training-pool exclusion (`:16`) + the membership-stability **edit tripwire** (halts on a
    silent re-admit of the named trio via debut>2021/type).
  - L2 `RL_DIAL14` — dial 14 (`rl_model.py:301`).
  - L3 `RL_AGE` — s(age) breakout-persistence (`_merged_recover.py:208/225`).
  - L5 `RL_L5_PICKLESS` — trio pickless completion (`rl_model.py:806`; Perez/McAndrew pick→None; the 92 pedestal UNTOUCHED — L6 STOP).
  - L7 numéraire — assert live in `rl_export.py (g)` (dormant on pre-L7 board by design; HALTs pick-1≠3000 in the numéraire world); `CONSTRAINTS_v1_8.md` constants re-quote authored.
- **Base byte-exact PROVEN:** all gates OFF ⇒ `n=804 sum=723075`, emmett 1178 / bont 3721 / gawn 2538 / butters 6060 — exact.
- **L1 validated to the dollar:** +L1 ⇒ sum 724371 (**+1296, +0.179%**), anchors byte-identical (knobel path rebuilds).
- **L4 validated to the dollar:** +L1+L4 ⇒ emmett **826** (−29.9% pool-isolation — the armed nonsense trigger), bont 3708, gawn 2556, butters 6059.
- **Boot pins moved (bootstrap Guard 5 PASS):** engine_head 7a07e369→**2030e5df**, rl_model 0c42d158→**952ddb3d**. Store/register/band/config UNCHANGED.

## PENDING (follow-up certification commit — board regen + matrix in flight)
- **Panel re-pin** (`run_panel.sh` + `PANEL_EXPECTED.txt`): the 10 named move to the all-lever board — regenerate, read, re-pin (claim-accurate). **Until then `run_panel.sh` reads the new board and does NOT match the stale hardcoded panel — this is EXPECTED, not a defect** (register v33/v35 hygiene: NOT claiming 10/10 while it reads otherwise).
- **Board md5 re-pin** (`data/expected_boot.json` board / panel note): needs the rl_app_data.json re-export (ship_gates B4).
- **G-ATTR cumulative tables** (base→+L1→+L1+L4→+L1+L4+L2→+L1+L4+L2+L3→FULL+L5): chain generating (3/6 done, all matching targets so far).
- **OFFICIAL cohort gate** on the wired board: matrix generating; expected to reproduce y4/y5/y6 = 126.8/125.2/116.1 ≤ 130.
- **Acceptance v1.7** (expected reds EXACTLY {A2,A3,A12}), B3 seal, B4 parity, five data guards.
- **L7 rebase** on the actual wired combined board (÷1.0524; adopted[1]=3000; ratios preserved).

## COMBINED TARGETS (to confirm on the full board)
bont 3664 · gawn 2518 · butters 5986 · darcy 4067 · emmett 851 (net −27.8%, L4-dominated) · briggs 2215 · holmes 6472.
