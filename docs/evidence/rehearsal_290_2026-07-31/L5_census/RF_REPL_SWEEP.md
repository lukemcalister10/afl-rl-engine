# R-F — THE `MA.REPL` DERIVING-SCRIPT SWEEP. Verdict: **TRULY ABSENT**, with a reason.

**#290, 2026-07-31.** Seam ruling R-F ([#290 issuecomment-5144304085](https://github.com/lukemcalister10/afl-rl-engine/issues/290#issuecomment-5144304085)): *"absent from the repo" is NOT yet a fact — sweep EVERY ref, by name and by content, as the first act of L6.* The seam was right to refuse the claim: I had inherited it from lane A and repeated it in the L5 census without testing it.

## THE TARGET, NAMED BY THE CODE ITSELF

`engine/rl_after/rl_model.py:501`:

```python
REPL={'MID':80.1,'SD':78.3,'RUCK':78.5,'KPD':68.4,'SF':70.9,'KPF':66.8}
# v3.3 derived (rl_replacement_derive.py): Rule-1 pool, kfru 0.5, SD/MID 50/50 @4.16/5.20,
# KPD@2.0, SF@4.0, KPF@2.0, RUCK@1.64  [BAKE 2026-07-04: KPF REPL-1, 67.8->66.8, owner dial]
```

So the sweep has a **name** (`rl_replacement_derive.py`) and a **fingerprint** (`kfru`, the Rule-1 pool, the slot table).

## THE SWEEP — six passes, all negative

| # | pass | scope | result |
|---|---|---|---|
| 1 | by name | **every one of 43 remote ref tips** | **absent** |
| 2 | by name | **all history, every commit, `--diff-filter=A`** (so a since-deleted file would surface) | **never added** |
| 3 | by name pattern (`replacement`, `repl_`) | all history, all paths | **nothing** |
| 4 | by content — the script's own name | the four held branches + main | **mentions only**: `rl_model.py:501`'s comment · `docs/archive/HANDOVER_historical.md` · the consistency inventory · and two state diffs that merely carry `rl_model.py`'s line |
| 5 | by content — the **logic** (`kfru`) | every ref tip, `*.py` | the **only** python file on **any** branch that mentions it is `rl_model.py` — the comment, not a derivation |
| 6 | by content — the logic | **all history**, `*.py` | same single file |

## THE REASON — this is why it is absent, not merely that it is

| | |
|---|---|
| this repository's history begins | **2026-07-02** (`fddab37` *Initial commit*) |
| the v3.3 replacement reform that produced these bars is dated | **2026-06-17** |

**The derivation predates the repository by roughly two weeks.** It was never in this git history because it could not have been — it lived in the pre-repo working environment. `HANDOVER_historical.md` records the reform as *"reproducible via `rl_replacement_derive.py`, all 9 anchors pass"*, which is a true statement **about a machine that no longer exists**.

A negative sweep that ends at "not found" invites a successor to sweep again. This one ends at *why*, so it does not have to be repeated.

## THE SEAL — CARRIED-NOT-REGENERABLE

Per R-F: *truly absent → the gap seals as CARRIED-NOT-REGENERABLE, reconstruction dockets, and any step needing to re-derive from it HALTs.*

**SEALED.** The six bars `MID 80.1 · SD 78.3 · RUCK 78.5 · KPD 68.4 · SF 70.9 · KPF 66.8` are **carried forward as values, and are not regenerable from anything in this repository.** One of them (`KPF 67.8 → 66.8`) is additionally a hand dial applied at the 2026-07-04 bake, so even a recovered script would not reproduce the live table without that owner word replayed.

**THE HALT, ARMED:** any step that needs to **re-derive** `MA.REPL` HALTs and reports. It does not silently re-fit, and it does not treat the carried values as a derivation.

**Does anything in L6 fire it? Measured: no.** `MA.REPL` is **read** as a fixed bar table — `dist_redesign.py:46`, `_merged_recover.py:384`, `_p1_recency.py:33`, `_p2b_headtohead.py:26` all read it and temporarily apply `REPL_DROP` around a call, restoring it after. **Nothing re-fits it.** L6's convergence iterates the curve against the surface; the bars are a constant input to that loop. So the HALT is armed and does not fire at L6.

## A CORRECTION TO MY OWN L5 CENSUS

`l5_census.py` dispositioned **row 29 (`MA.REPL`) as RE-DERIVED**, on the reasoning that the bars *"move with the retrained band/peak substrate."* **The sweep falsifies that.** A table that cannot be regenerated cannot be re-derived; it can only be carried. The disposition is corrected to **CARRIED-NOT-REGENERABLE**, and `REPL_DROP_PTS` (row 38), which I had riding on row 29, is corrected with it — the **drop** is a live dial and stays RE-DERIVED, but it must not inherit a claim that the **bars** re-derive.

This is the third time this rehearsal that re-running beat re-reading, and the first where the thing being re-read was **mine**.

## THE RECONSTRUCTION DOCKET

To make the bars regenerable, a landing act would need all of:

1. **the pool rule** — Rule-1 pool membership, with the `h26`-filter bug excluded (`HANDOVER_historical.md` records that bug: it filtered on *"substantial 2026 sample"* and silently dropped injured/thin-2026 starters, biasing every bar **down**);
2. **the locked dials** — kfru 0.5 · GDEF/MID 50/50 · slots MID 5.20 / GEN_DEF 4.16 / KEY_DEF 2.0 / RUC 1.64 / GEN_FWD 4.0 / KEY_FWD 2.0;
3. **the 9 anchors** the original claimed to pass, so a rebuild is checkable rather than merely plausible;
4. **the 2026-07-04 KPF hand dial** (`67.8 → 66.8`), which is an **owner word** and is not derivable at all.

Item 4 means a faithful reconstruction is a **derivation plus a replayed owner word**. That is worth knowing before anyone estimates this as a scripting job.

## A CONNECTION R-G SHOULD BE MADE ON BEFORE IT IS DECIDED

R-G dockets `engine/rl_after/verify_anchors.py` to the landing set, **"re-default inside the identity set, or delete."**

Measured: that file is the **anchor verifier for exactly this reform** — its docstring reads *"UNIFORM REPL -3 … Anchors as of the 2026-06-28 REPL-uniformization refresh. If these drift, something changed — STOP and reconcile before building."*

**The deriver is gone; the verifier survived.** It is the only surviving instrument in the tree that can tell whether the `MA.REPL` bars still behave as they did when they were locked — precisely the check that a CARRIED-NOT-REGENERABLE table most needs.

**So the two branches of R-G are not equivalent, and the difference is not visible from R-G's own framing:** *delete* also destroys the last check on the sealed bars. **Re-default inside the identity set** keeps it. I am not taking the decision — it is a landing act and it is the seam's — but it should not be taken as a tidy-up without this fact in view. Its anchors are stale (pre-VOR, γ=0.85) and would need refreshing either way.
