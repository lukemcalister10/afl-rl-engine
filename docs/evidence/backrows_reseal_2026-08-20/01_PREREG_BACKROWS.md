# PREREG — ACT A: THE BACK-ROWS `AGE_REF` REPAIR

**Owner word, VERBATIM:** *"Let's fix it now please."* · **Date:** 2026-08-20
**Base:** `main` @ `78ebc08` · **Committed BEFORE any engine edit.**

The owner's second word this session — *"And I'll re seal once that is done"* — sequences ACT B (the
book re-seal) strictly AFTER this act, so that the book signs the CORRECTED board. That is why this
prereg lands first and why nothing in `data/book_stable_seal.json` is touched here.

---

## 1. THE DEFECT — ALREADY DIAGNOSED, ALREADY MEASURED, NOT RE-LITIGATED HERE

`engine/rl_after/rl_export.py`, the `back_extra` loop (currently `:251-253`):

```python
    for _p in g['back_extra']:
        _p['_v'] = _p['_vM2'] = _p['_vM1'] = _p['_vP1'] = _p['_vP2'] = _nb(_ev(_p, 2026))
        _p['_cvx'] = 1.0
```

Entering that loop the ambient engine clock is `BASE_REF=2026` **but `AGE_REF=2028`** — left standing
by the players loop's last forward call `ev(_p, 2028)` — and these rows do not traverse the
`_b6_core`/`price6` re-pin that would correct it. The H3 repair (register v792) inserted the per-row
re-pin in the **players** loop only; the identical insertion in this loop was prereged, applied,
MEASURED, found to move the canonical board of record, and REVERTED, with the reversion recorded in
the code's own comment block above the loop.

**WHERE THE RESIDUE LIVES — answered explicitly, because the brief asks.** It lives in the **export
path**, not in a cached input. `back_extra` row values are computed inline by that loop from
`_ev(_p, 2026)` on every build; nothing reads a baked back-row value from a sidecar, a store field or
a pickle. Grep evidence recorded in `02_where_the_residue_lives.txt`. The consequence is the point of
this act: **a one-statement change in the exporter makes the corrected pricing the shipped reality of
every bare build, forever** — as opposed to a hand-edit of 25 numbers on one board artifact, which is
explicitly NOT what is being done.

## 2. THE FIX — STATED EXACTLY, IN ADVANCE

**Scope: `engine/rl_after/rl_export.py` only. ONE inserted statement. No expression, constant, law,
threshold or parameter is touched, and no other file's behaviour changes.**

```python
    for _p in g['back_extra']:
        g['BASE_REF']=g['AGE_REF']=2026; g['_pe_clear']()   # THE BACK-ROWS REPAIR
        _p['_v'] = _p['_vM2'] = _p['_vM1'] = _p['_vP1'] = _p['_vP2'] = _nb(_ev(_p, 2026))
        _p['_cvx'] = 1.0
```

This is **byte-for-byte** `PREREG_H3_REPAIR.md` §2 variant **(b)**, the statement that was applied and
reverted at H3 time, and byte-for-byte what the probe rebuild `68be10c7` was built with. The comment
block above the loop is rewritten to record that the residue is now CURED and by whose word; comments
do not enter the board hash, so the rewrite cannot affect any prediction below.

### What this prereg explicitly does NOT do

The strictly larger, structural cure — making `_merged_recover.ev(p, Y)` pin its own clock before ANY
evaluation, so it stops being ambient-state-dependent at all (`H3_DIAGNOSIS.md` §6 q2/q3) — is **NOT
done here**. It changes the single valuation source, needs its own byte-identity argument across every
caller, and the register has referred it to the modernisation programme. Doing it here would also
falsify F1 below, because it would not reproduce the probe's rebuild. It stays referred.

## 3. PREDICTIONS — declared before the edit

| id | prediction |
|---|---|
| **P1** | A CONTROL build of the unmodified tree reproduces the LIVE board `c97a4d9f9fa42597f85517c7850d3943` exactly, so every later diff is attributable to this one statement. |
| **P2** | **The post-repair bare build == the probe's fixed-clock rebuild `68be10c79d0ee096455754e084bcf757`, BYTE-EXACT.** |
| **P3** | dev-shell and canonical builds agree byte-for-byte on the new board. |
| **P4** | All **804** active rows byte-identical (`v/vM2/vM1/vP1/vP2`, and every other active field). |
| **P5** | **EXACTLY 25 of 198** back rows move, **all DOWN**; back-row `v` sum **772 → 700** (Δ −72). |
| **P6** | The 25 movers **by name and by delta** match `14_actc_ageref_probe.txt` exactly, including `charlie-dean 41→39` and `jacob-bauer 29→27`. |
| **P7** | `lensConservation` lens −1 `755307 → 755235` and lens −2 `782108 → 782036` (each −72), and NOTHING else in the board moves — no player price, club total, pick price, numéraire, F5 layer, seal id or lens-0 total. Lens 0 holds at **692,296**. |
| **P8** | `engine_head` (md5 `_merged_recover.py`) does **NOT** move — this act edits the exporter, not the engine. Likewise `config`, `rl_model`, `fv`, `store`, `register`, `v0surf`, `as_of_round` (held at 23). |
| **P9** | **The balanced/sibling board DOES move.** Under the balanced posture (`RL_LEGE=0`) `_LENS_FORM` is never set, so the residue entering the back loop is `BASE_REF=AGE_REF=2028` — a superset of the canonical exposure. `balanced_board_md5 3970156c…` is therefore expected to move, and the sibling reconcile is part of this act's landing. Its ACTIVE vector must be unmoved (P4's argument applies in both postures). |
| **P10** | Landing: `expected_boot.board` moves; `release_contract` restamps to a NEW `contract_sha256` (currently `c5149774b8ec`) with `as_of_round` HELD at 23; an out-of-round history column is written; a `release_lineage` register entry is appended citing the owner's word verbatim; BOTH UI writers run. |
| **P11** | Gates after the act: `acceptance.runner` GREEN, `release_manifest_check.py` PASS, `release_contract.py check` PASS. |

## 4. FALSIFIERS — any one firing HALTS the act and is reported, not absorbed

| id | falsifier | HALT condition |
|---|---|---|
| **F1** | **THE BYTE-EXACT REPRODUCTION.** If the fix is right, the bare build IS the probe's rebuild. | post-repair board md5 ≠ `68be10c79d0ee096455754e084bcf757` ⇒ **HALT**. |
| **F2** | The control build must reproduce the live board. | control ≠ `c97a4d9f…` ⇒ HALT (the tree is not what this act thinks it is). |
| **F3** | No active row may move. | any of the 804 active rows differing in ANY field ⇒ HALT. |
| **F4** | The mover set must be the probe's set. | count ≠ 25, or any mover up, or the name/delta list ≠ the probe list, or back sum ≠ 700 ⇒ HALT. |
| **F5** | Nothing outside back rows + `lensConservation` may move. | any other board field differing ⇒ HALT. |
| **F6** | Determinism. | dev ≠ canonical, or two builds disagreeing ⇒ HALT. |
| **F7** | The engine must not move. | `engine_head` ≠ `1867e953cf844d089ab1da68379b1742` ⇒ HALT. |
| **F8** | The store must not move and no round may be applied. | store ≠ `b745002eb0a0fbb1c34fa44f1ef708d6`, or `as_of_round` ≠ 23 ⇒ HALT. |
| **F9** | Gates. | any gate red after the act ⇒ HALT and report. |

## 5. THE 26-vs-25 DISCREPANCY — the standing instruction, restated

The H3 account reported **26** of 198 and named only three; the probe re-measured **25**. The record
does not attribute the one-row difference and this act **does not force it**. If — and only if — this
act's work EXPLAINS it (for example, a row that left the back section between eras), the explanation
is recorded with its measurement. Otherwise it stays recorded and unattributed, exactly as it is now.

## 6. SEQUENCING AND DISCIPLINE

1. This prereg lands first, in its own commit, before the edit exists.
2. The `rl_export.py` edit + the built board + its sidecars land in one commit with F1–F8 measured.
3. The landing transaction (pins + sidecars together, sibling reconcile, contract restamp + repin,
   column, lineage entry, BOTH UI writers) lands per the templated pattern.
4. Gates after the act.
5. **THEN, and only then, ACT B** — the book re-seal, on the owner's second word.

**No push. `docs/OPEN_ITEMS_REGISTER.md` is not touched. Explicit-path commits only.**
All builds under `tools/build_lock.sh`, `PYTHONHASHSEED=0`, BLAS pinned to 1, staging outside the repo.
The fv-provenance SUITE is never run on this box; only its accepted disposable builder `_run_build` is
imported, exactly as the D8, R23, H3 and F5 seats did.
