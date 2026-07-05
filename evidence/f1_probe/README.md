# F1/F2 Pipeline-Divergence Investigation — Evidence Record (READ-ONLY)

**Directive:** F1/F2 PIPELINE-DIVERGENCE INVESTIGATION, 2026-07-05. Confirm/refute a cold review
(out_sweep.json, branch `claude/engine-cold-design-review-c62k2c` @ 283cd9b) claiming the shipped
board and walk-forward book diverge from the gated engine.

## Ground truth
- git HEAD: `389ac397712e623f927259de930ce266bec51afd` (tag `baked-v2.4-2026-07-04`)
- engine md5 (`_merged_recover.py`): `c47cb43d` — matches directive.
- Files (all git-tracked, present): `rl_export.py` 16494 B; `data/rl_build/rl_app_data.json` md5 eb5d6716;
  `rl_model_data.json` == `.pre_stage0` (md5 644d1254, authoritative reconciled store); `.stage0` md5 91a3de6b.
- Run env (canonical, from `run_panel.sh`): PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25
  RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22; PYTHONPATH includes vendored unidecode.
  Run from `/home/claude/rl_workspace/rl_after` (byte-identical mirror of `engine/rl_after` @ 389ac39).

## How to reproduce
```
cd /home/claude/rl_workspace/rl_after
export PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
export PYTHONPATH=/home/claude/rl_workspace/rl_after:/home/claude/rl_vendor
python3 <repo>/evidence/f1_probe/probe.py        # fingerprints + id-membership test
python3 <repo>/evidence/f1_probe/sweep_only.py   # full gated-vs-shipped board sweep
python3 <repo>/evidence/f1_probe/part2.py         # Petracca position, population/retirement, pick-60
python3 <repo>/evidence/f1_probe/f2_probe.py      # F2 double-v7 book recomputation
```
Each script re-execs `_merged_recover.py` (the gated engine) and diffs against the committed
`data/rl_build/rl_app_data.json`. No engine files are modified.

## F1 — CONFIRMED (CRITICAL)
The board export drops all three `_REAL`-gated engine layers (v2.4 RUC prior cap 1.4x, v7 age tail-fade,
B5 pricing floor). Mechanism: `rl_export.py:6` execs `rl_model.py` into a dict namespace; `rl_export.py:25`
execs `_merged_recover.py` into a **separate** namespace whose `import rl_model as MA` (`_merged_recover.py:6`)
creates a **second module instance** with its own player objects. `_REAL=set(id(p) for p in MA.data)`
(`_merged_recover.py:194`) therefore contains none of the board's player ids, so every gate
`if id(p) in _REAL` (`:317` RUC cap, `:198` v7, `:552` floor) evaluates False.

**Direct measurement:** of the 805 board player objects, **0** have `id(p) in _REAL`.
- Louis Emmett (id `louis-emmett`, RUC, pick27/2025): gated **853** (cap = 1.4 × PVC 609) vs shipped **1361**
  (cap stripped). Shipped matches the export-path recomputation exactly (1361). +59.6%.
- Full board sweep: **531 / 805 (66.0%)** of shipped values differ from gated; median divergence **+11.9%**
  (501 shipped-higher, 30 shipped-lower). Top over-values are all young rucks/KPPs.

## F2 — CONFIRMED (CRITICAL)
The walk-forward book generator `s4_matrix_M1v7.py` re-injects a **prototype** v7 on top of the already-v7-baked
engine. `s4_matrix_M1v7.py:47-58`: defines `_v7` with `cB=0.47*...` compression (line 48) **and** `asc` fade,
then `_b6fix` (line 52) wraps `b6_orig` — which is the engine's already-v7-wrapped `b6` (`_merged_recover.py:196-201`,
asc-only) — and rebinds `g['b6']=_b6fix`. Result: `asc` applied to the band tail **twice**, and the
owner-DELETED `cB` compression (`_merged_recover.py:155-156`: "v7-cB DELETED 02/07/2026") **resurrected**.
The sealed book generator (`data/book_stable_seal.json`: generator=`s4_matrix_M1v7.py`, head_md5=`c47cb43d`)
is this buggy file — so B1/B3 certify a book the shipping engine did not produce.

**Direct measurement:** engine ev(2026) vs book-path ev(2026): Josh Ward 1640 → **1233 (−24.8%)**;
Daicos 7013 → 6769 (−3.5%); Sheezel 7150 → 7076; Reid 3537 → 3433 (−2.9%). Petracca/Bontempelli unchanged.

## Reconciliation with review (out_sweep.json @ 283cd9b)
Review: 537/805 (66.7%), median +12.5%. Independent reproduction: **531/805 (66.0%), median +11.9%.**
Agreement within 6 players / 0.6pp — the review's sweep is **corroborated, not suspect**. F2 numbers
(Ward −24.8%, Daicos −3.5%) reproduce exactly.

## Three fingerprints (gated vs shipped)
| fingerprint | gated | shipped | verdict |
|---|---|---|---|
| Louis Emmett (RUC pk27/2025) value | 853 | 1361 | DIVERGENT — RUC cap stripped (F1) |
| Christian Petracca (MID pk2/2014) value | 3033 | 3033 | MATCH (no gated layer binds on a MID) |
| Petracca position | gf=MID, grp(bnow)=GEN_FWD, fut=[MID .7, GEN_FWD .3] | identical | MATCH — de-DPP in gf; bnow retains fwd by engine design; NOT stale |
| Pick-60 draftval | PVC[60]=308 | PVC['60']=308 | MATCH — picks table renders 1..30 only, but PVC carries 60 correctly |

## Population / retirement
- Engine active players **805** == shipped active rows **805** (the "794 vs 805" concern is REFUTED).
- Engine `_retired`=0 and `delisted()`=0 among the 805 active (retired players live in `back`, 197 rows) —
  so no retired player carries value in `active`. 0 shipped active rows are delisted-in-engine with v>50.
- Injured players correctly NOT retired (keyed by id): Toby Conway `toby-conway` (pk24/2021, v=468);
  Max King `max-king-stk` (pk4/2018, v=651) vs Maxwell King `max-king-syd` (pk49/2025, v=347) — distinct;
  Ben King `ben-king` (pk6/2018, v=538). No injured player mislabeled retired.

## Three-price corollary (F3)
Josh Ward (id `josh-ward`, MID pk7/2021) is priced three ways at the baked head:
**engine/gates 1640 · board 1772 (+8.0%, F1 cap-off) · book 1233 (−24.8%, F2 double-v7).**

## Verdict
F1 CONFIRMED, F2 CONFIRMED. Both are real, both tie to shipped/sealed artifacts. They are TWO
independent bugs in the export/book harnesses, not in the canonical engine (`_merged_recover.py` is correct).
The board over-prices ~2/3 of players (young rucks worst); the book under-prices the tail. Canonical
gated engine, PANEL 10/10, and ship-gates are unaffected.
