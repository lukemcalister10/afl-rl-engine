# PREREG — THE H3 REPAIR. Re-pin the engine clock per row in `rl_export.py`'s value loop.

**Seat:** R23 unblock → build seat (H3 repair + R23 advance), register **v792**
**Date:** 2026-08-20 · **Base:** `origin/main` @ `702e25d`
**Measured base identities:** store `cc02567f`, board `a05fe951`, `rl_model` `6fe7c415`,
`rl_export.py` `5dca63ec`, `as_of_round=22`, sheet `b26798c3`.

**This document is written and committed BEFORE the edit.** Nothing below was measured after the fact.

---

## 1. The defect being repaired (adjudicated REAL, register v792)

`docs/evidence/r23_unblock_2026-08-20/H3_DIAGNOSIS.md` establishes, and the register ratifies:

`rl_export.py`'s value loop (`:189-221`) takes each player's **board value** from the **first** `ev()`
call of the iteration — `_ev(_p, 2026)` at `:191`. But the **previous** iteration's last call was
`_ev(_p, 2028)`. `_merged_recover.ev()` re-pins the engine clock only once it reaches `_b6_core` /
`price6` (`_merged_recover.py:371, 389`); **everything `ev()` evaluates before that point reads the
ambient `MA.BASE_REF`** left standing by the previous row.

* **Canonical posture** (`RL_LEGE=1`): `:197` sets `_LENS_FORM=2026`, so the forward calls leave
  `BASE_REF=2026`. The residue *is* the present. Masked, harmless, F1 passes 804/804.
* **Balanced/strict sibling** (`RL_LEGE=0`): `_LENS_FORM` is never set, so `ev(p,2028)` leaves
  `BASE_REF=2028`. Rows **1…803** are therefore priced on a 2028 form/tenure/peak basis. `players[0]`
  (`nick-daicos`) escapes because `rl_export.py:113` pins the clock immediately before the loop.

`AGE_REF` residue was measured inert. The whole effect is `MA.BASE_REF`.

## 2. The fix — stated exactly, in advance

**Scope: `engine/rl_after/rl_export.py` only. Two inserted statements, both inside the `:189-221`
value block. No expression, constant, or law is touched.**

**(a) the players loop** — insert at the top of each iteration, before the first value-forming
`ev()` call (`:191`):

```python
    for _p in players:
        g['BASE_REF']=g['AGE_REF']=2026; g['_pe_clear']()   # H3 REPAIR
        _r = _ev(_p, 2026); ...
```

**(b) the `back_extra` loop** (`:219-221`, inside the same value block) — the identical defect, but
reachable only on its **first** row (the residue the players loop's last `ev(p,2028)` leaves; from its
second row on, its own `ev(p,2026)` has already re-pinned). The same statement is inserted at the top
of its iteration. These rows are board-visible (`rl_export.py:359`, `back=[player_rec(p) …]`).

This is byte-for-byte the repair `H3_DIAGNOSIS.md` §6 names as option 1:
*"`g['BASE_REF']=g['AGE_REF']=2026; g['_pe_clear']()` at the top of each iteration."*

### What this prereg explicitly does NOT do

`H3_DIAGNOSIS.md` §6 question 2 offers a second, **strictly larger** repair: making
`_merged_recover.ev(p, Y)` pin its own clock before *any* evaluation, so it stops being
ambient-state-dependent at all. **That is the durable fix and it is NOT being done here.** It is a
structural change to the engine's single valuation source, it would need its own prereg and its own
byte-identity argument across every caller, and the register has referred it to the modernisation
programme. This seat does not smuggle it in. Likewise §6 question 3 — that the same latent
order-dependence sits under the canonical board, masked by `RL_LEGE=1` — is **noted, not cured**: the
per-row re-pin removes the *exposure* (the loop no longer carries residue between rows) but the
in-`ev()` structural sensitivity remains as a modernisation item.

## 3. FALSIFIERS — declared before the edit. Any one firing HALTS Part 1.

| id | falsifier | pass condition |
|---|---|---|
| **F1** | The canonical board of record must be **byte-identical**. The mask made it clean; the fix must be a **no-op** there. | canonical build (`balanced=False`, `config_mode='canonical'`) → board md5 **`a05fe951f78482c70520480e184c80ec`**, byte-exact. **If it moves, HALT.** |
| **F2** | The corrected balanced/sibling value vector must equal the board of record on **804/804** rows — the diagnosis proved this is the correct target. | 804/804 identical, **Σ = 664,949**. Any row differing ⇒ HALT. |
| **F3** | Determinism. | two independent builds in each posture ⇒ identical board md5 (canonical) and identical balanced md5 / Σv. |
| **F4** | The sibling parity gate. | `EXPORT<->ENGINE PARITY GATE FAILED for 96/804` ⇒ **`PARITY GATE PASS: all 804`**, build `rc=0`. **96 → 0.** |
| **F5** | `nick-daicos` — `players[0]`, the one row the residue could never reach — must be **unchanged** in both postures. | identical value pre- and post-fix. A move here means the fix did something other than remove residue. |

**Expected, disclosed in advance (not a falsifier — the priced consequence the owner accepted):** the
96 balanced rows rise by **+0.39 % … +9.65 %**, **+2,772** on a 662,177 board total; `balanced_board_md5`,
`release_contract.present_lens_baseline` + its seal, `reference_vector_<md5>.json`,
`forward_vector_<board>.json`, `test_forward_lens_<board>.py`, both board-view bundles and
`sibling_repin_state.json` all move. The `back_extra` first-row delta is measured and reported
separately, whatever it reads (including zero).

## 4. Sequencing

1. This prereg lands **first, in its own commit**, before the edit exists.
2. The `rl_export.py` edit lands in its own commit with F1–F5 measured and recorded.
3. The sibling/balanced artifacts are then moved **through the writers of record**
   (`sibling_repin reconcile` — build-and-compare, identity derived from the built artifact, never
   from a supplied constant), all dependent pins in **one act**, coherence manifest GREEN after.
   This discharges the v788 sibling fork (option A) and the v791 book-seal-lag note if the reseal
   rides this act. **If a genuine ambiguity arises about whether `reseal_book` is required, HALT
   that item and report.**
4. `python3 -m acceptance.runner` GREEN at each milestone before each push.

## 5. Sanctioned-edit discipline

This seat has **two** sanctioned engine-file edits for the whole sequence: this one, and the ORDER 42
sheet-pin constants of Part 2.1. Both are preregged. The owner's input bytes are never modified.
