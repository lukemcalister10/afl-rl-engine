# PREREG — ACT B: THE BOOK RE-SEAL

**Owner word, VERBATIM:** *"And I'll re seal once that is done."* · **Date:** 2026-08-20
**Base:** `main` @ `5aaa654` (ACT A landed and gated) · **Committed BEFORE any seal is written.**

The owner's word sequences this act strictly after the back-rows repair, so the book is sealed on the
corrected tree. ACT A is landed: board **`68be10c7`**, balanced **`556ad70d`**, contract
**`cde9f70a49b6`**, gates GREEN.

---

## 1. THREE PREMISES IN THE BRIEF THAT THE TREE CORRECTS — STATED FIRST, NOT DISCOVERED LATER

The brief carries three facts from `RESEAL_HALT.md`, which was written **before THE BAKE**. Measured
against the tree now:

| brief says | the tree says |
|---|---|
| `data/book_stable_seal.json` is **STALE since 2026-07-17** | It was **RE-SEALED on 2026-08-20 at THE BAKE** (register v780, `docs/evidence/bake_2026-08-20/reseal_bake.py`). `sealed_date` reads `2026-08-20`. |
| the seal reads `n_players` **2649** | It reads **2650**. 2649 was the *pre-bake* count; the bake re-counted it and its own output records `2649 -> 2650`. |
| the seal reads `head_md5 40f43772` / `store_md5 968de0c7` | It reads **`5ac6780f` / `cb38ef11`** — the bake's line. |

**The lag is real, but it is one chapter old, not five weeks.** The seal names engine `5ac6780f` and
store `cb38ef11`; the tree carries engine `1867e953` and store `b745002e`. Both moved at the D8
adoption / injury-sheet re-cut / R23 advance, none of which re-sealed. That — and exactly that — is
what `release_manifest_check`'s two sealed-lag lines report, and it is what this act closes.

**A fourth correction, to the CAUTION.** `ship_gates_check.py`'s `RL_GAMMA=0.85` self-brick at line
~64 **is already repaired in tree** by M1a (the line now sets `RL_GAMMA='1.0'`, with the reasoning in
place). The blocker that remains in that file is different: `ship_gates_check.py:49` hardcodes
`RA = '/home/claude/rl_workspace/rl_after'`, a SHARED, OUT-OF-REPO workspace which this box carries at
engine `338a790b` / store `cc02567f` — **stale**, and not this branch's tree. Guard 5 will halt it.
That is a standing finding the bake already reported; **it is not edited in this act.**

## 2. THE PROCEDURE OF RECORD — AND WHICH INSTRUMENT IS ACTUALLY OF RECORD NOW

`RESEAL_HALT.md` §1 names `session_2026-07-17/legd_derivation/reseal_book.py`. That instrument was
superseded on 2026-08-20 by **`docs/evidence/bake_2026-08-20/reseal_bake.py`**, a *declared three-change
port* of it: (1) `ROOT`/`RA` re-pointed at the worktree instead of the stale shared workspace, (2) the
`RL_GAMMA=0.85` / `RL_PICK1` / `RL_RUCK_TAX` / `RL_RECENCY_DECAY` / `RL_PRIOR_TREES` / `PAR_RAMPS`
dial block **DROPPED**, (3) thread pinning made explicit. It is the instrument that last moved the seal
and it carries a `--check` mode that re-verifies a committed seal and writes nothing.

**Change (2) IS THE PRICE-LINE RULING, already implemented.** The settled ruling — certification runs
on the BARE SHIPPED LINE, no env dials — is what that instrument already does. This act therefore
carries it forward rather than re-deciding it, and re-points only the narrative fields at this act.

## 3. THE STEPS

1. **Re-verify the price-line identity on the POST-ACT-A board**: build the board under
   `RL_CONFIG_MODE=gate` on the bare line and assert it equals the live board `68be10c7`.
2. Regenerate the walk-forward matrix with `engine/rl_after/s4_matrix_M1v7.py` under
   `RL_CONFIG_MODE=gate`, bare line, exactly as `ship_gates` B3 does.
3. Assert the matrix `__meta__` `engine_head_md5` / `store_md5` == the current tree, and its
   `config_sha256` == `data/model_config.json`'s.
4. Recompute `stable_sha256` over the STABLE-KEYED content and **re-count** `n_players` honestly.
5. Rewrite `data/book_stable_seal.json` (`head_md5`, `store_md5`, `n_players`, `stable_sha256`,
   `config`, and the narrative fields).
6. **Certify**: re-run the same instrument `--check` (the B3 steps run directly, which is what the
   brief authorises if `ship_gates_check.py` bricks). Attempt `ship_gates_check.py` B3 as well and
   record whatever it does, without editing it.
7. `release_manifest_check.py`: the sealed-lag count must DROP.
8. Gates.

## 4. PREDICTIONS

| id | prediction |
|---|---|
| **B1** | A bare **gate-mode** board build reproduces the live board `68be10c79d0ee096455754e084bcf757` byte-exact — the bake's design identity (bare build == live board), re-verified on the post-Act-A board. |
| **B2** | The gate-mode matrix carries `__meta__` `engine_head_md5` starting `1867e953`, `store_md5` starting `b745002e`, `config_sha256` == `eed19a75f775…`. |
| **B3** | `stable_sha256` MOVES off `86a82e6e…`. The engine moved `5ac6780f -> 1867e953` and the store moved `cb38ef11 -> b745002e` since the seal; the book is engine-`ev()`-derived, so it must move. **A seal that did not move would be the surprise.** |
| **B4** | `n_players` may move from **2650**. It is a RE-COUNT, not a carry. Whatever it reads is recorded with its reason; no number is predicted. |
| **B5** | The `--check` re-verify PASSES on every field after the write. |
| **B6** | `release_manifest_check`'s **sealed-lag count drops 2 -> 0**, and its verdict stays PASS. |
| **B7** | The board, store, `expected_boot`, `release_contract`, `release_lineage` and every UI bundle are **BYTE-UNMOVED** by this act. A book re-seal writes ONE file. |
| **B8** | Gates after the act: `acceptance.runner` GREEN, `release_manifest_check` PASS, `release_contract check` PASS. |

**Stated in advance so it is not claimed as a discovery afterwards:** the walk-forward book is built by
`s4_matrix_M1v7.py` from `_merged_recover.ev()`; **it does not import `rl_export.py`**. So ACT A does
not change the book's CONTENT. The board enters the re-seal only as a GUARD — `single_source.assert_startup`
consumes `rl_app_data.json` and asserts its stamp against the live store, which is why the seal could
not have been taken over an incoherent board. Sealing after ACT A rather than before is therefore
correct-and-cheap rather than content-changing, and the honest statement is: **the book is sealed on
the tree whose board is the corrected one**, not "the corrected board changed the book".

## 5. FALSIFIERS — any one firing HALTS and is reported

| id | falsifier | HALT condition |
|---|---|---|
| **FB1** | The price-line identity. | gate-mode board ≠ `68be10c7` ⇒ **HALT**: the line being certified is not the live board's line, which is the whole premise of the ruling. |
| **FB2** | The matrix must be this tree's. | `__meta__` engine/store/config ≠ the tree ⇒ HALT (the instrument asserts this itself). |
| **FB3** | Certification. | `--check` not PASS on every field after the write ⇒ HALT. |
| **FB4** | The lag must drop. | sealed-lag not lower than 2 ⇒ HALT and disclose the named remainder rather than declaring success. |
| **FB5** | One file. | any file other than `data/book_stable_seal.json` (and this act's evidence) modified ⇒ HALT. |
| **FB6** | Gates. | any gate red ⇒ HALT and report. |

## 6. DISCIPLINE

No push. `docs/OPEN_ITEMS_REGISTER.md` untouched. Explicit-path commits. Build lock held for every
build. **The fv-provenance SUITE is never run on this box.** `ship_gates_check.py` is NOT edited in
this act whatever it does; if it bricks, the brick is recorded as the known P1 item and certification
is carried by the B3 steps run directly, which is the brief's own instruction.
