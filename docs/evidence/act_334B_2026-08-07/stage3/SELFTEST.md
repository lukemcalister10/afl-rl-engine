# Stage 3 step 7 — the self-test, and the owed 144 → 146 count

```
$ python3 one_source_selftest.py
SELF-TEST PASSED: single source; guards 1-3; board==engine (F1); book==board (F2);
  Kako+Bontempelli ground-truth; DPP blend stripped; Leg B L-RECENCY + rho forbidden-list
  (R105.5/R105.4); collision sentry (King pair) clean.
EXIT = 0
```

**FINAL COUNTS: 143 PASS assertions · 0 FAIL · 0 STALE · 0 HELD · exit 0.**
(= 145 by a plain `grep -c PASS`; see the count section below for why the two differ.)

Full transcript: `selftest_full_output.txt`.

## The re-point enumeration — THREE pins

Each one moved because the artifact it pins was legitimately re-derived by this stage.

| # | test | old | new | why, one line |
|---|---|---|---|---|
| 1 | `_contract_md5` — "FROZEN-RULER contract byte-untouched" | `eae593f220460d880be20da38e3de39d` | `160f9fe77fd3f99707c48916f3d59e50` | `ui/release_pick_curve.json` was re-derived for the stage-3 ladder, which moves its own bytes. |
| 2 | `_curve_source_store` — "FROZEN-RULER contract source store" | `f1e8c9fed35462536d00add604f69a3f` | `37ced3ce45914e6feb00d27e26922e9a` | the ladder is now taught on the current gate store, not the #323 corrected store. |
| 3 | `_per_entrant_md5` — "FROZEN-RULER curve stamp per_entrant" | `999d24c8` | `b7ed144e` | the ladder is now taught on the stage-3 era-free matrix, not `per_entrant_328_corrected_store.json`. |

Nothing else in `one_source_selftest.py` was touched. Before the re-point the two file-identity checks
FAILED loudly (`FROZEN-RULER curve bytes == contract file md5 aee19206` / `curve payload md5=18203822 ==
contract`) — the guard is non-vacuous and caught the moved artifact exactly as designed. The
`_held_check('FROZEN-RULER')` declaration is absent from `release_contract.json`, so these checks are
live FAILs, not HELDs — confirmed by the two FAIL lines in the pre-repin run.

## ONE assertion is no longer emitted — data, not a re-point

`143` vs stage 1 / stage ER's `144`. The missing line is:

```
  PASS #326 currency end-to-end (ND65+): Nathan Broad ships at 83 == floor_frac(15)=0.05 x signed level 185
```

**This is a data-conditional emission, not a removed check.** In `one_source_selftest.py` the `#326`
per-division block names, for each signed level, the CHEAPEST live entrant that re-prices when that
level is probed, and then emits the extra end-to-end currency line only if that named entrant's route
is `floor`:

```python
if _named and _route(_named[0]) == 'floor':
    check(abs(board_v - round(floor_frac(yrs) * level)) <= 1, "#326 currency end-to-end (%s): ...")
```

The ND65+ level is a LAW, not a number: `min(the signed K15 measurement 185, the ruled curve's pick 64)`.
The re-anchor moved pick 64 from 185 to **182**, so the ND65+ level followed to 182 and the cheapest
re-pricing ND65+ entrant moved from **Nathan Broad (floor route)** to **Lincoln McCarthy (ruck-cap
route)**. Ruck-cap entrants get no currency line, so the count drops by one. The PDN division's named
entrant likewise moved (Andy Moniz-Wakefield → Changkuoth Jiath), both on the ruck-cap route, so its
count is unchanged. The `#326 level ND65+ reaches a real entrant's BOARD price` assertion itself still
PASSES, on the new named entrant.

## THE OWED REGISTER ITEM: why 144 → 146 with a byte-identical test file

**The assertion count never moved. `144` and `146` are the same run counted two different ways.**

* stage 1 (`stage1/build_log_tails.txt`) reported `PASS lines : 144`, counting the indented assertion
  lines the `check()` function prints (`^\s+PASS `).
* stage ER (`stageER/SELFTEST_REPOINTS.md`) reported `PASS assertions: 146`, which is `grep -c PASS`.

`grep -c PASS` sweeps in **two lines that are not assertions at all**, and the stage-ER transcript
committed in this repo proves it directly — `grep -vE '^\s+PASS '` over its own PASS-matching lines
returns exactly these two, and no others:

1. **line 2** — the boot banner printed by `boot_guard` at import:
   `boot-store guard (Guard 5) PASS  [one_source_selftest]  store 37ced3ce == pinned 37ced3ce | …`
2. **line 227** — the closing summary `SELF-TEST PASSED: single source; guards 1-3; …`, where `PASS` is
   a substring of `PASSED`.

Measured on the committed artifacts:

| transcript | `^\s+PASS ` (assertions) | `grep -c PASS` | difference |
|---|---|---|---|
| `stageER/selftest_full_output.txt` | **144** | 146 | +2 |
| `act_334_2026-08-06/selftest_final_334.txt` | 145 | 147 | +2 |
| this stage (`selftest_full_output.txt`) | **143** | 145 | +2 |

The `+2` is a constant. So stage 1's 144 and stage ER's 146 are **the same 144 assertions**; the test
file was byte-identical because nothing about it changed, and nothing about the run changed either.
The register item is closed as a **counting-method artifact**, not a behavioural move.

### And, for completeness, the check family that CAN move the count with data

Two families emit a variable number of PASS lines:

1. **the owner-anchor loop** `KAKO_ANCHORS` — one line per anchor, and it prints `STALE` (a FAIL)
   instead of `PASS` once the store's `as_of_round` outruns an anchor's `thru` round. This is the
   family behind the *real* 145 → 144 move between act #334 stage A and this branch: the 2026 Kako
   anchor was RETIRED by owner word 2026-08-06 at R21, so the list lost an entry. That is a genuine,
   earlier, source-level move and is **not** the 144 → 146 the register flagged.
2. **the `#326` per-division currency block** described above — the family that moved this stage.

Recording both is the point: the register asked which checks print PASS conditionally on data, and
these two are the answer, even though neither of them caused the number the register was asking about.
