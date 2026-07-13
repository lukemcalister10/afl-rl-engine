# THE MEASUREMENT BUILD — PLAN (first committed artifact)
supervisor seat 5 · 2026-07-13 · **READ-ONLY. Four report-only deliverables.**

## BASE VERIFICATION (done, first act)
- `git ls-remote` → **v2.9 = 9f8ae7616555ce55c67ae2076247662960b731e5** exists ✓
- `b97d1bf7…` **IS ancestor** of `origin/main` (560982c) ✓; `git diff b97d1bf..origin/main` touches **docs/ only** ✓
- v2.9 IS ancestor of main ✓ · Guard 5 PASS at bootstrap (store 340a7a32 == pinned) ✓
- **Two boards, both confirmed by direct diff:** the ONLY ev-relevant difference between working-head store
  340a7a32 (board 3dc19fbb) and tagged store b0c39d78 (board 81e48293) is **Lachlan Bramble**'s 2026 line
  (±1 game, avg 62.3/62.4 — far below the captain line 107.4; not in any carrier/captain set).

## BOARD DISCIPLINE (every figure names its board)
- **D1, D2, D4 are measured on the TAGGED board 81e48293 (store b0c39d78).** I built a tagged-board
  workspace (`scratchpad/ws_tag`, store md5 **b0c39d78**) and validated it reproduces the shipped numéraire
  panel EXACTLY: Daicos 7667 · Bont 3482 · Gawn 2393 · Reid 3594 · Moore 197. All engine measurement runs
  chdir there. Numéraire divisor **F = 1.0524** (board value = round(ev/F)).
- Engine head = **2030e5df** (identical at tag and working head — item20 note: ev()/config/band/rl_model UNCHANGED).

## TIME
Band 90–150 min (confirmed; not flagged). Report actual in RETURN.

## FENCE
New files only under `session_2026-07-13/measurement/`. No writes to store/engine/board/gates/docs or any
existing file. All four deliverables REPORT-ONLY. If I want to correct a value: **write it down and stop.**

---

## DELIVERABLE 1 — SPEC_2/3 CALIBRATION LEGS (per carrier: mechanism from CODE · measurement · effect size · size of correction)
- **1a JUH — the 3-game cameo (−865) & the `nqual` cliff.** `_nqual(p,Y)` (`_merged_recover.py:106`) = count of
  seasons with games≥10 in the debut window ≤Y. It gates the career-thin blend `c=n/PROVEN_N` (PROVEN_N=4) in
  `_coreM1`/`_lvl_eff_core`, and the `expgate`/`eff_ten` paths in `raw_ev`. **Method:** identify JUH; decompose
  his −865 by toggling the level-core path; plot value vs matched production at nqual=1/2/3/4+ (synthetic matched
  producers + the real cohort) to show cliff-vs-slope and locate/steepen the discontinuity.
- **1b RYAN — the `_fbump`.** `_fbump(a,lcr)` (`_merged_recover.py:97`) is the UP-ONLY form-conditioned credit added
  to the age decline multiplier `_agemult2` — reached ONLY on the shed down-branch (n≥PROVEN_N, Lo−Lc>DOWN_TOL,
  lcr>0). **Method:** read exactly what it does & its conditions; census every row where `_agemult2 > _agemult`
  (i.e. `_fbump` fires); total SCAR moved (fbump-on vs a byte-exact fbump=0 run); place Ryan in that distribution.
- **1c DYLAN MOORE — missing body-of-work axis.** Verify the −694…−1009 dip penalty on the tagged board & decompose
  (shed branch `_coreM1` down-side + KPF paths). Then MEASURE the missing axis on the walk-forward record: does a
  player's **career body of work** predict next season **over and above his most recent season**? Fit at finest
  resolution the sample supports (smoothed, no wide bins — CORE rule 7); report effect size. Negative result stated
  plainly if that is what the data says.
- REPORT (1): one markdown per carrier. **No proposal.**

## DELIVERABLE 2 — G-Y0 RE-MEASURE (feeds a ratification)
Re-run the G-Y0 seam table on the TAGGED BAKED board (81e48293): weighted-mean position-conditioned V0 vs derived
PVC per pick band; deviations net zero; the y0→wk1→y1 trough→y2 recovery chain, walk-forward. Report the table +
per-band deviations **in the numéraire**, and whether the chain shape holds. State plainly whether the original
`v2_9_continuation` conclusion (comp-weighted V0 > derived PVC in every band, +19…+281, PRE-BAKE/PRE-NUMÉRAIRE) survives the re-basing.

## DELIVERABLE 3 — SILENT-FAILURE SWEEP (delegated, in progress)
Sweep the live harness tree for checks whose exit code is discarded (pipe w/o pipefail through tail/head/grep;
swallowed subprocess returncodes; except:pass around a gate; `|| true`). Exclude historical session logs. Per site:
file · line · invokes · what-happens-today-if-it-raises · HARMLESS vs DANGEROUS. Count DANGEROUS + worst 3. REPORT ONLY.

## DELIVERABLE 4 — CAPTAINCY PREMIUM (owner-raised; possibly the biggest)
Live term `capt_prem(lev)` (`rl_model.py:180`): `cb=0.35·over^1.25`, `prem=cb·18/(18+cb)` — hard 18-pt asymptote.
Applied at every credited forward year inside `_proj_w4`/`_prod_floor_w4` (`_merged_recover.py:495,520`) + rl_model
:339/:353/:543. Dead twin `capt_bonus(level)` (`rl_model.py:294`) defined, never called, non-saturating/asymptotically linear.
1. **Premium today:** reproduce curve, cap, the 19 players over the line (ln>107.4), total board SCAR moved (capt-on
   vs capt-off), and Bont/Gawn/Daicos attribution.
2. **Realized value, off the record:** captaincy is a **slot good** (one captain/week) → an **order statistic**.
   On the walk-forward record, measure the top scorer's realized captain worth over the 2nd/5th/10th-best option per
   season; test whether the gap is **convex** in how far the top sits above the field.
3. **Sensitivity ladder:** vary CAPT_GAIN/CAPT_CAP/CAPT_EXP across a stated ladder (monkeypatch MA.CAPT_* after import
   — validated safe: pole/V0/PVC synths sit at par < line so capt=0 there; the 19 elite re-price live). Per rung:
   Bont · Gawn · Daicos · top-19 total · **A-PAIRS pair 3 (does Bont pass Sanders, at what rung?)**.
4. **Guard exposure:** per rung recompute **G-COHORT y4/y5/y6 on the July-8 binding construction** (class-SUM of
   walk-forward values, mean across incurve classes 2004–2020, ratio to min(y1,y2); baseline must reproduce the
   ratified **1.2601/1.2407/1.1521**). G-COHORT headroom = 0.0399 at y4 (1.2601 vs hard 1.30). Direction on
   G-PEAK/G-CONVEX/A-BONT/A-GAWN. **If a rung breaches a BINDING guard, say so in the RETURN's first three lines.**
   REPORT-ONLY — no rung chosen, none wired. No magnitude tuned to catch one player.

## METHOD / SPEED
- One shared harness (`scripts/harness.py`) loads the tagged engine once; exposes ev, players, capt on/off, ladder
  monkeypatch, walk-forward accessors (`p['scoring']`, `cp.debutyr`, `cp.fwd_best3_from`, `value_asof`).
- G-COHORT baseline matrix generated via the OFFICIAL pricer `s4_matrix_M1v7.py` (gate mode) on the tagged store;
  hash-cached; the class-sum reading validated == 1.2601 before any ladder rung.
- Long computes backgrounded with completion markers; sparse polling.

## RETURN
≤30 lines, committed to this dir. Branch · head SHA · PR# (if opened) · board per figure · D1/D2/D3/D4 figures ·
confirmation nothing outside this dir was written · plain-terms close. A return without its SHA is incomplete.
