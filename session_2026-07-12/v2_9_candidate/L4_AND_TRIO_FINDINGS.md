# L4 (MSD pool exclusion) + L5 (trio) — read-only evidence + state reconciliation · 2026-07-12

## L4 — MSD pool exclusion reproduced on the CURRENT store (b0c39d78)
`scripts/l4_pool_sim.py` patches the training-pool filter in the engine source string
(`_merged_recover.py:17`, adds `or p.get('type')=='MSD'` to the `continue`), re-execs, re-evs —
read-only, mirrors #63 `msd_pool_ripple_pass.py`. Because #63 measured on a different base
(bc2929fe / store before the ID migration), this re-runs it on the shipped candidate store.

| metric | #63 oracle | this run (current store) |
|---|---|---|
| trained pool | ND 1255 / RD 640 / MSD 29 / PSD 7 | **ND 1255 / RD 640 / MSD 29 / PSD 7** (base) → MSD **29→0** (excl) |
| movers (any) | 668 | **671** |
| movers ≥5% | 47 | **48** |
| board sum | +0.18% | **+0.19%** |
| louis-emmett | 1177→826 (−29.82%) | **1178→826 (−29.88%)** |
| lachlan-mcandrew | +1.25% | +1.19% |
| bontempelli | −0.35% | −0.35% |
| max-gawn | +0.67% | +0.71% |
| jai-newcombe | −0.65% | −0.65% |

**Verdict: reproduces.** The +3-mover / +1 ≥5% drift vs #63 is the ID-migration store delta
(taylor-adams removed + 5 DOB corrections shifting a few marginal rows) — expected, not a defect.
The headline holds on the current store: **the MSD slice was propping louis-emmett's ceiling; its
removal drops him −29.9%** (his own board-wide refit; the owner's football-nonsense trigger is armed
here). Anchors are NOT byte-identical (it is a refit) — bont −0.35% etc., matching the oracle.

## The membership-stability facts-based rule (to author for the permanent lever)
Exclude a row from the calibration training pool iff **entry-type == MSD ∧ debut ≤ 2021** (the
existing pool window). **Load-bearing leg NAMED:** the re-entry trio's pool exclusion rides on the
**debut≤2021 window**, NOT on entry-type. `l4_base.json`/#63 `ssp_filter_note` confirm mcandrew
(SSP-typed, pick 12) and perez (SSP-typed, pick 35 + _ft) carry live pick capital and are kept out
of the pool **only by the debut window** (SSP → debut year+1 > 2021). **Edit tripwire:** any store
edit that would change a row's training-pool membership (a DOB/debut-window edit re-admitting the
trio, or a type relabel) must HALT for a ruling — that is exactly the silent-re-admit hole.

## L5 — the trio state, reconciled (not a from-scratch switch)
`PRESENT_ID_OVERRIDES` (`rl_model.py:806`) is **live**: perez/mcandrew/keane → SSP, `_eff`=92
(pedigree half of the switch applied), but `pick`=35/12 and `_pickless`=False (pick-capital half
NOT applied). Live evs: perez **14**, mcandrew **1176**, keane **1636**. So the board today already
prices them off the SSP pedigree — the register's "no engine override exists / deferred" describes
the STORE fields, not the loaded engine. What remains for the **full** switch = make them pickless
(drop pick 12/35, `_pickless`=True). Post-L4 that is **pool-neutral for mcandrew** (MSD out either
way; SSP debut window keeps him out either way); the residual cost ≈ **perez ~7 rows**.

**Reconciliation ruling needed (owner/supervisor):** (i) complete the switch (pickless) — matches
the stated intent, moves ~7 perez-side rows; or (ii) keep the half-state (SSP pedigree + retained
pick capital) as the membership-stability facts-based row and lock it with the edit tripwire. Either
way L4 must NAME the load-bearing leg so a data edit can't silently re-admit them.

## Status
L4 mechanism + figures VERIFIED (read-only) on the current store. The PERMANENT lever (make the
filter change durable + author the facts-based rule + the edit tripwire) is the **one refit** that
L1's permanent `_PVC0` path should ride under the one-refit law — staged, ladder-gated, not shipped
this session. L2 (dial) and L3 (age + the cohort gate) stack on top of that combined refit.
