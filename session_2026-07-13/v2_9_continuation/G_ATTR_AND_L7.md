# G-ATTR (per-lever board attribution) + L7 on the combined refit board · 2026-07-13 (item 3 evidence)

Cumulative board passes (`scripts/run_levers.sh <levers> board`, pristine→patch→restore, md5-verified):
base → +L1 → +L1+L4 → +L1+L4+L2 → +L1+L4+L2+L3. Each lever's separable delta = diff of consecutive
boards (`scripts/attribute.py`; `out/gattr.json`). ALL-LEVERS-OFF == base is satisfied by construction
(the base board IS the RL_PVCADOPT=0 / RL_AGE=0 / LENS['bal']=0.15 / MSD-off run; panel reproduces
10/10 emmett 1178, bont 3721, gawn 2538).

## Per-lever separable contribution (board sum + character)
| lever | movers | board Δ | character |
|---|---|---|---|
| +L1 (_PVC0 swap + V0/RUC rebuild) | 24 | +1296 (+0.179%) | young prior-capped RUCs UP (knobel 402→505, barnett +101, conway +97); anchors byte-identical |
| +L4 (MSD pool exclusion) | 679 | +1428 | the refit — **emmett 1178→826 (−352)**; xerri/treacy +86; broad small ripple |
| +L2 (dial 14) | 713 | +5307 | young lift board-wide (duursma +106, uwland +75); the discount step |
| +L3 (s(age)) | 42 | +1619 | proven young risers UP (wilmot +455, callaghan +358, bowey +301, berry +216); old-name down |

## louis-emmett — the three-probe corner (directive's named case), clean + separable
| stage | emmett | Δ | probe |
|---|---|---|---|
| base | 1178 | — | |
| +L1 | 1178 | **0** | cap basis barely changes between frozen and derived curve (L1 does NOT clear his cap) |
| +L4 | **826** | **−352 (−29.9%)** | **pool-isolation** — the MSD slice was propping his ceiling; its removal is his own board-wide refit |
| +L2 | 851 | +25 | dial-14 lifts him (14% is above the ≤13% prior-cap artifact zone — the sweep's finding) |
| +L3 | 851 | 0 | he is not a proven-riser up-branch mover |

Net across the refit: **1178 → 851 (−327, −27.8%), L4-dominated.** This is exactly the synthesis's
three-probe attribution (cap via L1/L2 · pool-isolation via L4); L1 and L3 leave him untouched, so the
levers are cleanly separable at his corner. **The owner's football-nonsense review trigger is ARMED on
the L4 pool refit** (emmett −29.9%) — reproduces the inherited L4 figure exactly; returned for the word.

## Anchor carry (base · +L1 · +L4 · +L2 · +L3)
```
bontempelli 3721 3721 3708 3664 3664   gawn   2538 2538 2556 2518 2518   briggs 2222 2222 2223 2215 2215
darcy       4013 4013 4009 4067 4067   butters 6060 6060 6059 6049 5986   holmes 6270 6270 6269 6280 6472
```
L1 moves no anchor (byte-identical); L4 small (bont −13, gawn +18); L2 the dial (bont −44, gawn −38);
L3 hits butters (−63 = the age curve, ≈−1.04%) and holmes (+192, young riser). No anchor breaks its bar.

## L7 — numéraire re-base on the COMBINED refit board (the refit's FINAL step)
`l7_rebase.py` on the +L1+L4+L2+L3 board (÷1.0524): **adopted_curve[1]=3000 ✓ · display pick-1
3157→3000 ✓ · order preserved (no strict inversion) ✓ · ALL 10 anchor-pair ratios preserved ✓**
(e.g. bont/gawn 1.4551→1.4551, bont/emmett 4.3055→4.3041). Combined refit board → numéraire:
bont 3664→3482 · gawn 2518→2393 · briggs 2215→2105 · darcy 4067→3865 · emmett 851→809 · board sum
÷1.0524. Uniform scalar ⇒ every ratio/ordering preserved; only the unit changes. This demonstrates L7
on the ACTUAL combined refit board (the retiring seat built it on the pre-refit board) — ready to ride
the permanent refit as its last step. `out/l7_combined_rebased.json`.
