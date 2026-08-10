# THE DOB COURIER STORE WRITE — 2026-08-10 · **HALTED BEFORE PUSH**

The write that #290's runbook section 5 ("THE DOB COURIER ACT") specified and never fired.
Owner's word, 2026-08-10, issue #334 comment 5235574982: *"Ruory Kirkby - 4/2/86. Tim Looby - 2/9/87.
Write the birthdates."*

**The write itself is clean: 302 of 302 rows, zero join failures, exact bytes, census green.**

**It is not pushed and there is no PR.** The board could not be rebuilt from the written store. The
engine refuses to build: the birth data moves the frozen V0 pick-curve surface's config signature, and
a surface refit is outside this act's scope. Both of the brief's halt conditions fired, so the act
stops here for an owner word. Section 4 has the mechanism, named row by row.

**Measured, so the size of it is known:** under a declared refit the board moves by a hair — **6 of 804
players, every one by exactly ±1**, board total +4 in 761,583, pick 1 unmoved at 3000. The price
consequence is negligible; the obstacle is procedural, not economic. Section 5.

---

## 1 · WHAT WAS WRITTEN

| | |
|---|---|
| store | `engine/rl_after/rl_model_data.json` |
| md5 before | `0dd6b4a01e16dabf8d3a388d8f8ac1f2` |
| md5 after | `d9a24282357cf3083b1640466e3ecd83` |
| rows written | **302 of 302** |
| join failures | **0** |
| records changed | exactly 302 |
| fields changed | `_by` and `_bd`, and nothing else, on any record |

Join was on the store `key`, one-to-one, validated before a byte moved: every one of the 302 staged
keys exists in the store, no key is repeated on either side, no key hits two records, and all 302
staged player names match the store's own name for that key character-for-character. All 302 records
carried `_by: null` and no `_bd` field at all before this act.

`_bd` is inserted immediately after `_pickless`, which is where the store's own convention puts it —
781 of the 848 records that already carried a birth date are shaped exactly that way, and all 302
targets have `_pickless` followed by `future_position`.

The write is exact-byte by construction: the store round-trips through `json.dumps` byte-identically
(asserted by the script on entry), so every byte that moved, moved because the script moved it. A
post-write structural pass re-reads both versions and asserts that no record outside the 302 changed
at all, that no record moved position, and that nothing but `_by`/`_bd` changed inside the 302.

The script HALTs rather than writing a partial set: any missing key, duplicate key, name conflict,
wrong row count, or a row that would land a null year or null date stops the whole write.

Artifacts: `write_dob.py` (the script), `applied_302.csv` (every row, old and new value, source and
provenance), `md5_before_after.txt`.

## 2 · THE TWO OWNER OVERRIDES

The owner's word of 2026-08-10 supersedes the 2026-07-31 staging file for these two keys, and only
these two. Both keys existed in the store under exactly the keys named in the brief, so no name
resolution was needed.

| key | player | draft | staging file (2026-07-31) | **owner's word (2026-08-10)** |
|---|---|---|---|---|
| `ruory-kirkby` | Ruory Kirkby | 2004, RD, pick 4 | `_by` 1986, **`_bd` empty** | `_by` **1986**, `_bd` **1986-02-04** |
| `tim-looby` | Tim Looby | 2005, RD, pick 33 | `_by` 1987, **`_bd` empty** | `_by` **1987**, `_bd` **1987-09-02** |

Both were the crosscheck's DISCREPANT rows. The staging file carries them YEAR-ONLY under the
then-standing seam ruling (runbook Addendum A.2: "Kirkby and Looby are RULED YEAR-ONLY … `_bd`
deliberately absent"). The owner's fresh word replaces that ruling and supplies the days. The dates
above read his `4/2/86` and `2/9/87` as day/month/year per Australian convention, as the brief states.
The store value before this act was null in both fields for both rows, so nothing of his was
overwritten.

Machine-readable record: `owner_overrides.json`.

## 3 · CENSUS — GREEN

`census.py`, reading only, using the same classification as the L4 age-source census
(`build_peak_model_v4.age_source`). It does **not** run the peak-model refit.

| | before | after |
|---|---|---|
| ND records, classes 2003-2005, blank `_by` | 186 | **0** |
| all record types, classes 2003-2005, blank `_by` | 302 | **0** |
| of the 302 couriered rows, still blank | 302 | **0** |
| store-wide REAL_DATE | 848 | 1150 |
| store-wide REAL_YEAR | 1500 | 1500 |
| store-wide **FALLBACK** | **302** | **0** |

The fallback count fell by exactly 302, the number of rows written. That is the runbook's own
acceptance test for the courier (§5.4: "the FALLBACK count must fall by **exactly** the number of rows
written, or the leg HALTs"). It passes. Full output: `census_after.txt`.

## 4 · THE HALT — the board cannot be rebuilt, and why

### What happened

The board rebuild in a clean private workspace **failed on the written store**:

```
v0surf FROZEN-SIGNATURE HALT: this build's config signature 6ef67f07db98258786189a6316ce24f9
is NOT in data/v0surf.pkl (frozen: af556bdca53dee20d4f73e0ae25a8127, edb15f7ab7c9bded82119c99f4c5ee55).
  The engine will NOT silently re-fit the V0 pick-curve surface — that silent fallback was removed
  (owner word 2026-07-28) …
```

Every downstream gate fails behind it: the book build, the self-test (2 PASS / 2 FAIL, both "build it
first"), and the Guard 4 canary all fail for want of a board. Logs: `gate_run.log`, `gate_export.txt`,
`gate_book.txt`, `gate_selftest.txt`, `gate_canary.txt`.

**The instrument is sound.** The identical recipe on the *unwritten* store reproduced the shipped board
`6e724cca2bb2fb118ff7ad6ed1f8a4b6` byte-exact, with the self-test at 142 PASS / 0 FAIL and every gate
green (`control/`). So the failure is caused by this write and nothing else.

### Why — the mechanism, exactly

`_merged_recover.py:1324`, `_v0surf_sig()`, hashes a payload that includes:

```python
'roster': sorted([str(MA.gfut(p)), _ageR(p), int(p.get('pick'))] for p in real)
```

where `real` is every REAL national-draft player in the whole store history with a recorded, non-pool
pick — not just the 804 on today's board — and `_ageR(p)` is that player's **age at his draft**, which
reads `_by` straight through `MA.age()` (`rl_model.py:191-194`).

Draft age reduces to `max(draft_year - _by, 18)`. With `_by` missing the engine falls back to
`draft_year - 18` (`rl_model.py:191`), which makes the draft age **exactly 18** — so every one of the
302 has been sitting in the surface fit as an 18-year-old. Their real birthdates say otherwise for
some of them.

Measured on the written store: **54 of the 302 change draft age**, and **14 of those are national
draftees taken inside picks 1-64**, which is precisely the roster the V0 surface is fitted over:

| key | player | pick | draft age assumed | draft age real |
|---|---|---|---|---|
| `cameron-thurley` | Cameron Thurley | 22 | 18 | **22** |
| `chad-jones` | Chad Jones | 24 | 18 | **19** |
| `eddie-sansbury` | Eddie Sansbury | 39 | 18 | **20** |
| `brent-lecras` | Brent LeCras | 51 | 18 | **22** |
| `adrian-deluca` | Adrian Deluca | 57 | 18 | **21** |
| `nathan-ablett` | Nathan Ablett | 46 | 18 | **19** |
| `simon-taylor` | Simon Taylor | 50 | 18 | **22** |
| `matthew-egan` | Matthew Egan | 57 | 18 | **21** |
| `max-bailey` | Max Bailey | 18 | 18 | **19** |
| `ryan-brabazon` | Ryan Brabazon | 54 | 18 | **19** |
| `joshua-krueger` | Joshua Krueger | 31 | 18 | **20** |
| `stephen-kenna` | Stephen Kenna | 59 | 18 | **22** |
| `paul-thomas` | Paul Thomas | 56 | 18 | **22** |
| `ben-schwarze` | Ben Schwarze | 61 | 18 | **21** |

These are mature-age draftees. That matters because the V0 fit **splits on draft age at 18/19**
(`_merged_recover.py:1604-1607`): the young pick-curve `c18` is fitted only over players with draft
age ≤ 18, and the mature-entry surfaces `surfN`/`surfR` only over draft age ≥ 19. So all 14 currently
teach the **young** pick curve, and with their real birthdates they move **out of it and into the
mature-entry surfaces**. Both surfaces change shape. Those surfaces price today's board.

### The brief's expectation was wrong, and this is the seat saying so

The brief expected **zero board byte change**, on the reasoning that "birth data of 2003-05 draftees
should not enter current-player pricing." **It does.** Not through those players' own prices — they are
long retired and unpriced — but through the V0 pick-curve surface, which is fitted over the whole
national-draft history and is age-resolved. Fourteen mature-age draftees have been teaching the
18-year-old curve because the engine had no birthdate for them and assumed 18.

That is not a defect in this write. It is the write doing exactly what birth data is for, and the
freeze guard catching it — which is what the guard was installed for on 2026-07-28.

### Both halt conditions fired

1. *"If the board DOES change, HALT before pushing anything."* — It cannot even be built; the engine
   stops rather than produce one. That is stronger than a changed board, not weaker.
2. *"If the write mechanically triggers any refit or surface rebuild, HALT and report."* — It does.
   The only way to a board from this store is a **declared v0surf refit**
   (`RL_V0SURF_REFIT=1 RL_BAKE_V0SURF=1 refit_v0surf.py --bake`), which is a surface rebuild and a
   re-pin of `v0surf`, both explicitly outside this act's scope guard.

Nothing was pushed. No PR was opened. The v0surf freeze is untouched, `data/v0surf.pkl` is unmodified,
and no model, curve, surface, teaching or config value was changed.

## 5 · HOW BIG IS THE MOVE — measured

Full working: `board_impact_diagnostic.md`. Three builds in the private workspace, nothing written back
to the repo, `data/v0surf.pkl` untouched.

| run | store | v0surf | board |
|---|---|---|---|
| A | unwritten | frozen | `6e724cca` — the shipped board, byte-exact |
| B | unwritten | **declared refit** | `6e724cca` — **byte-exact again** |
| C | **written** | **declared refit** | `a672ed3a` |

B is the control that makes this clean: a fresh refit on unchanged data returns the frozen surface's
board bit for bit, so the freeze is faithful and there is no refit weather. Every difference between B
and C is the birthdates and nothing else.

**B vs C, on the present board:**

| | |
|---|---|
| movers | **6 of 804** |
| size of every move | **±1 SCAR** — max, median and mode are all 1 |
| board total | 761,583 → 761,587 (**+4**, +0.0005%) |
| backward board | **0 movers** |
| PICK 1 numéraire | **3000, PASS** |
| export↔engine parity | **PASS**, 804/804, eps 0 |

William McCabe +1 · Mitchell Marsh +1 · Maxwell King +1 · Luke Urquhart +1 · Isaac Cumming +1 ·
Jevan Phillipou −1. The lens columns move the same way: 15 rows at −1yr, 26 at −2yr, 7 at +1yr, 6 at
+2yr, every one of them ±1.

Reshaping the two surfaces by moving 14 players across the 18/19 draft-age split is a real change, but
after the numéraire re-base it lands as ±1 rounding on six current players. **A rounding ripple, not a
repricing.** Nobody's valuation changes in a way a human would notice.

What that does *not* dissolve: the board md5 still moves, and on main the engine still refuses to build
at all until the v0surf freeze is re-cut. Cheap in prices is not the same as free in process.

## 6 · WHAT IS RE-PINNED, AND WHAT IS NOT

Only one pin was moved, because the gates could not run to prove the rest:

- `data/expected_boot.json` → `store: d9a24282357cf3083b1640466e3ecd83` (moved so Guard 5 would let the
  gate workspace boot at all, which is how the halt was discovered).

The full carrier list was surveyed and is **not** re-pinned, because a store md5 re-pin is only honest
once the act it belongs to can land. For the record, the live carriers of the store md5 are:

| carrier | field |
|---|---|
| `data/expected_boot.json` | `store` |
| `data/release_contract.json` | `store` |
| `data/season_state.json` | `source_store_md5` |
| `data/rl_build/rl_app_data.json.srcmd5` | `source_md5` |
| `engine/rl_after/ingestion/sibling_repin_state.json` | `source_store_md5` |
| `engine/rl_after/ingestion/finalization_state.json` | release `store` |
| `ui/data/board_view_working.js` | `stamp.store_md5`, `stamp.store`, `release.store` |
| `ui/data/ownership.js` | `generatedFromStore` |
| `ui/data/movers.js` | `release.store` |
| `ui/data/club_valuation.js` | short-form `0dd6b4a0` |

Sealed history that must NOT be re-stamped, and was not: everything under
`docs/evidence/ingest_r22_2026-08-10/`, the `txn_catchup_r22` manifest and journal, and the R22
movers artifact — each records what was true at the round-22 act, not what is true now.

## 7 · THE WORD THIS NEEDS

The write is done and correct. What it needs is a ruling on the surface, which is the owner's, not the
seat's:

- **Land the birthdates with a v0surf refit and re-bake.** The honest reading: the surface has been
  fitted on 14 wrong ages and the data corrects it, for a measured cost of six players at ±1. Cost in
  process: a declared refit, a `v0surf` re-pin, board `6e724cca` → `a672ed3a`, and the re-bake train
  behind a moved board — balanced board, UI bundles, book re-seal, fixtures. This is the runbook's own
  picture; §5.4 always said the store md5 moves and L4's final bake runs on the couriered store.
- **Land the birthdates year-only for those 14**, keeping their draft age at 18 and the surface still.
  Preserves a zero-move board and needs no refit, at the cost of knowingly holding wrong ages for 14
  players so the surface does not have to be re-cut. Year-only is already a first-class store state
  (Addendum A.2), so the machinery exists — but it would be keeping a known-wrong age on purpose.
- **Hold.** Nothing lands; the store stays as it is and the 302 stay on the draft-year-minus-18
  fallback.

The seat does not recommend between them. It notes only that the measured price cost of the first
option is six players at one point each, which is the smallest board move in the recent record.

## 8 · FILES

| file | what |
|---|---|
| `write_dob.py` | the write, fail-closed |
| `applied_302.csv` | all 302 rows: old value, new value, source, provenance |
| `owner_overrides.json` | the two owner rows, staging value vs owner value |
| `md5_before_after.txt` | store md5 before and after |
| `census.py` · `census_after.txt` | the census and its output |
| `board_impact_diagnostic.md` · `ab_driver.sh` | the measured size of the board move, and its driver |
| `gate_run.sh` · `gate_run.log` | the gate driver and its log (the halt) |
| `gate_export.txt` | the v0surf HALT in full |
| `gate_book.txt` · `gate_selftest.txt` · `gate_canary.txt` | the gates that failed behind it |
| `control/` | the same gates on the UNWRITTEN store: board `6e724cca` byte-exact, self-test 142/0 |
| `workspace_bootstrap.sh` | the clean-workspace recipe used for every build here |
