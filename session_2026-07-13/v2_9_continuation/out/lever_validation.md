# Single-lever source-patch validation vs the inherited audited sims · 2026-07-13

Each v2.9 lever is applied as a source patch (`scripts/levers.py`, single source of patch truth) to a
PRISTINE workspace copy, board-passed, then restored (md5-verified). The point: prove the source
patches reproduce the retiring seat's in-memory sims BEFORE trusting the combined matrix gate.

| lever | patch | board result | inherited sim | verdict |
|---|---|---|---|---|
| BASE | none | n=804 sum=723075 · emmett 1178 · bont 3721 · gawn 2538 · butters 6060 | panel/base | ✓ exact |
| L1 (_PVC0 swap + V0/RUC rebuild) | load-time inject after draftval rebind | sum 724371 (**+1296 = +0.179%**) · emmett 1178 (unmoved) · anchors byte-identical · knobel 402→505 | l1_adopt_sim pin3000: +0.179%, 25 movers (24 RUC+1 KEY_DEF), knobel 402→505 | ✓ mechanism exact (board sum + anchors byte-identical; the 25th mover = will-darcy 560→559, a −1 SCAR rounding flip) |
| L4 (MSD pool exclusion) | `or type=='MSD'` on pool filter | emmett **826** · bont **3708** · gawn **2556** | l4_pool_sim msdexcl: emmett 826, bont 3708, gawn 2556 | ✓ exact |
| L2 (dial 14) | LENS['bal'] 0.15→0.14 | bont **3676** · gawn **2501** · emmett 1227 | SWEEP_DISCOUNT 14% col: bont 3676, gawn 2501 | ✓ exact |
| L3 (s(age)) | flat S_M1→clip(s_age(age)) up-branch | (pending) butters ~5997 | L3_FINDINGS: butters 6060→5997 | (pending) |

**L1 is the load-bearing validation** (the only lever that was a post-exec in-memory recipe rather than
a one-line source patch): the source injection reproduces the sim's board sum (+1296) and every anchor
byte-for-byte, so the combined-matrix walk-forward will carry a faithful L1. L4 and L2 reproduce their
sims to the dollar. The combined candidate matrix (L1+L4+L2+L3) then feeds the reconciled B1 gate.
