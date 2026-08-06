# #334 STORE-COMPLETION ACT — REHEARSAL on a working copy. Stage A executed and HALTED at step 7.
# Stage B NOT ENTERED: the box could not be classified, because the fit lane is barred on landed main.

Rehearsal seat, 2026-08-06, on landed main `da9aa70`, working copy
`scratchpad/rehearsal_326`. **Nothing committed, nothing pushed.** Two halts are recorded below and
neither was worked around.

The law read in full before anything moved: #334 body · the census comment (5199711591) ·
ADDENDUM 1 (5199768190, every closure binding) · the owner's answers (5199786512 — the Iles 2006
insert STANDS, 51 inserts, Paul Thomas confirmed) · the Drummond ruling (5199567533) · and the
#328 store-act pattern (`docs/evidence/store_328_jujn3g/ACT.md`, `RECLOSURE.md`).

---

## STEP 0 — THE CENSUS RE-PARSED INDEPENDENTLY BEFORE IT WAS APPLIED

`reparse_census_334.py` re-parses the owner's corrected sheet from its own xlsx bytes
(`docs/evidence/store_completion_2004_2005/owner_corrected_sheet_2026-08-06.xlsx` on
`claude/afl-rl-engine-seam-supervisor-gb9q0c`) and matches on **(cohort year, type, pick)** against
the store — never on name, because the two Will Hamills are exactly the trap that rule exists for.

```
inserts   mine  51   census  51   IDENTICAL: True
zero-confirmations  mine 177   census 177   MATCH: True
conflicts 0 · unmatched names 0 · pre-draft cells skipped 109
RE-PARSE REPRODUCES THE CENSUS
```

It also emits what `census.json` does not carry — the **(key, season) list** behind the count 177,
which is what makes ADDENDUM 1's no-change assert measurable rather than rhetorical.

## STEP 1 — THE 51 INSERTS

`apply_store_334.py`, dry-run first, whole-store diff audited before a byte was written.

| | |
|---|---|
| rows inserted | **51** into **40** players (2005 · 14, 2006 · 37) — the owner's post-answer list |
| `avg` | the census 1-dp value **verbatim**, asserted field-by-field after the write |
| row shape | `{year, avg, games, pos}`, the existing field order, inserted in year order |
| `pos` | earliest existing scoring row's `pos`; `drafted_position` for the ten no-row players (10 rows) |
| sheet position HINT | **differs from the ruled `pos` on 16 of 51 rows and was discarded on all 51** — ADDENDUM 1 fault 6 |
| year collisions | 0 (the census's "0 conflicts" re-proven on live bytes) |

The ten no-row players the act found are exactly the ten ADDENDUM 1 names — derived from the bytes,
not copied from the list, and the instrument HALTS if a no-row player appears that is not among them.

## STEP 2 — THE CAREER-GAMES COUNTERS, AND THE DERIVE-RULE GATE

`record['games'] == sum(scoring row games)` is the #323 section-1 invariant, read live at
`rl_model.py:493`.

```
40 players, +287 games total (census sum 287)   MATCH: True
derive-rule gate on the bytes about to be written:
  2650 records · structural faults 0 · counter != sum 0 · GATE PASS
non-vacuity, 3 counters tampered: GATE FAILS, naming willem-duursma / zeke-uwland / harry-dean
```

## STEP 3 — NO ROWS FOR THE 177 ZERO-CONFIRMATIONS, ASSERTED AS A NUMBER

A walk-forward **training cell** is one (record, horizon-year) pair. The horizon rule is quoted from
the emitter (`emit_matrix_271.py`: `retired_now`, the `yend`/`yrs` construction) and evaluated on
store bytes alone, so it runs before any build.

```
store-wide cells          13684 -> 13691   (+7)
the 177 zero-confirmations span 132 distinct players, 119 of whom carry NO insert
THEIR cells                 494 ->   494   (+0)   players moved: 0
```

The other 13 zero-confirmation players are players whose *other* season is a ruled insert; they move
because of that insert, which is ordered. The 119 pure-zero players do not move by a single cell.

**A number in ADDENDUM 1 reconciled rather than repeated.** ADDENDUM 1 wrote "+18 training cells for
the ten no-row-today players". Measured: the ten carry **10 cells before and 18 after** — a delta of
+8. The 18 is the count they *carry*, not the delta; each held one degenerate `C+1` placeholder
before. Recorded here so the record is not carrying an arithmetic that does not reproduce.

## STEP 4 — DRUMMOND AND THE TWO ROOKIE SEQUENCES

Anchors checked against live bytes before the move (Drummond RD 2003 pick 35; Shaw 39, Clarke 40);
the instrument HALTs if the owner's named anchor is not there.

```
before: 2003 RD n=45 picks 1..45 contiguous · 2004 RD n=45 picks 1..45 contiguous
josh-drummond  year 2003->2004  pick 35->40  stream_year->2004  stream_pick->40
2004 RD picks >=40 slide DOWN one  ..  6 rows (ed-clarke, marcus-allan, andrew-hayes,
                                                will-hamill-2004, martin-pask, scott-harding)
2003 RD picks >35  slide UP  one  .. 10 rows (sam-pleming .. jeremy-stiller)
after:  2003 RD n=44 picks 1..44 contiguous   (want 44)  OK
        2004 RD n=46 picks 1..46 contiguous   (want 46)  OK   no collisions
stream_pick/stream_year track pick/year on every row of both groups: True   (ADDENDUM 1 fault 4)
Drummond sits between earl-shaw 39 and ed-clarke 41, as the owner's words require.
```

17 rows move in total, which is the number the pre-fire audit measured.

## STEP 5 — THE WHOLE-STORE EXPECTED-DELTA AUDIT

```
records the act declares it touches      55
records that actually differ             55
records differing but NOT declared        0
declared/actual field-set mismatches      0
every other record byte-identical      2595 of 2595   ASSERTED
```

Full table: `expected_delta_table.json` — per key, the exact field set that may move
(`scoring (+n rows)` · `games` · `pick` · `stream_pick` · `year` · `stream_year`), compared against
what actually moved. `marcus-allan` and `martin-pask` carry the four-field both-slid-and-inserted
entry ADDENDUM 1 fault 5 requires. Every comparison keys on `key`.

**An arithmetic in the directive corrected, not silently absorbed.** The brief says "ALL 57 touched
records (40 insert players, 16 slid, Drummond)". 40 + 16 + 1 = 57 is the sum of the three lists;
`marcus-allan` and `martin-pask` are in two of them, so the **union of distinct records touched is
55**. 57 is the right sum, 55 is the right count of records, and the table carries 55 rows.

**Store `f1e8c9fed35462536d00add604f69a3f` -> `f1e7f20c4adea9b17d19457a5217c735`**
(1,969,004 -> 1,971,802 bytes; 2,650 records both sides). The project's own SERIALIZER-DRIFT proof
(`json.dumps(json.loads(x)) == x`, `ui/tools/ownership_store_apply.py:215`) was run before the write
and the candidate bytes re-applied byte-identically after.

## STEP 6 — THE CARRIERS RE-PINNED, EACH THROUGH ITS OWN WRITER

`restamp_store_pins_334.py` — the #328 instrument re-pointed, not rewritten. Each act re-read and
asserted after its write; every file proven to round-trip byte-identically before being touched.

| # | artifact | writer | move |
|---|---|---|---|
| 1 | `data/expected_boot.json` `store` | plain pin | `f1e8c9fe` -> **`f1e7f20c`**, re-read and asserted |
| 2 | `data/release_contract.json` `identities.store` | `release_contract.contract_hash` | pin moved; `contract_sha256` `8cc7d897…` -> **`0c85a56b3dacd9ced83e9b795e5df111b80168caafc6a5dca7d6eb0ebea5bec4`**, re-verified |
| 3 | `data/season_state.json` | `season_state.derive` | **re-derived** from the new store bytes, never typed |
| 4 | tier-2 frozen stamps | `single_source.lock_tier2` | `peak_model_v4.pkl` `f305fe53` · `pvc_snapshot.json` `ade79790` — **unchanged**, re-measured not assumed |

**Guard 5 re-asserted on the corrected store:** `bootstrap.sh` rc=0, `store f1e7f20c == pinned
f1e7f20c`. This is the halt the brief warned about, and the re-pin cleared it.

**The CURVE-side stamps deliberately not moved**, per the #328 precedent: `pvc_curve_v2.json`
`stamp.store_md5`, `ui/release_pick_curve.json` `curve_source_store_md5`, and the selftest
FROZEN-RULER `_curve_source_store` all stay at `f1e8c9fe`, because they record the store the ruled
curve was **derived on** — still true, and it stays true unless and until Stage B runs. The selftest
proves all six FROZEN-RULER checks still pass at that value.

**Board-derived carriers not moved** (`data/rl_build/rl_app_data.json.srcmd5`,
`ui/data/board_view_working.js`): both still read `f1e8c9fe`. That is the #328 step-1 state and is
coherent only while no board is published. **If a board write is attempted from here,
`ui/tools/ownership_store_apply.py` P3 will report INCOHERENT BASE across the six store-identity
carriers, and it will be right to.** This act halts before publishing, so it leaves them.

---

## STEP 7 — **HALT. The act's own zero-movement expectation FAILS.**

The census comment says "Expected board movement: none from the season inserts and Drummond move
directly (all affected players retired) — asserted, halt on surprise". The brief turns that into
"assert ZERO value movement on every row of active and back lists". It was asserted. It failed.

**First, the surface did NOT move — which is the opposite of #328 and matters.**

```
v0surf signature af556bdca53dee20d4f73e0ae25a8127   in the frozen pickle: YES   engine builds
legs:  pvc 35b9b300 (unchanged) · gates 0a566c97 (unchanged) · roster 31df8ae9 (UNCHANGED)
roster rows 1448
```

At #328 the store swap moved the roster leg and forced a surface re-fit. Here it does not: the roster
leg carries `(position, age, pick)` over the 1,448 real ND non-pool rows, and this act touches no ND
row's position, age or pick — the 51 inserts are scoring rows, and Drummond and all 16 slid rows are
RD. **So this store rides the committed surface, and no re-fit is needed for the store stage.**
Store and surface are two axes here, not one, and only the store moved.

**The board was rebuilt on that pair, twice, and is deterministic.**

```
baseline (pristine da9aa70, store f1e8c9fe)   board 864b6726a4612b0d8afe57f230421514  <- the landed pin, reproduced byte-exact
candidate (same tree, store f1e7f20c)         board 827fb1fdfefe60c7c2c9026212d3992d  (twice, byte-identical)
```

**DIRECT movement is exactly zero, as the owner's reasoning predicted.** None of the 55 touched
records appears on `active` (804), `back` (198) or `cohort` (1974); all 55 are `_retired` and none
carries a 2025 or 2026 season. The retired-players argument is sound.

**INDIRECT movement is real, and it is the finding.**

```
STORE-STAGE COMPLETENESS GATE — held: engine 9f258a3b · band 34faa865 · curve df766dff · v0surf af556bdc
  -> ONLY the store differs; the cause set is COMPLETE.

active  804 rows · added 0 · dropped 0 · MOVERS 154 (19.2%) · unchanged 650
   year_zero_lens  106 movers  up 34/down 72  sum  -704  max|d| 85
   ruled_curve      44 movers  up 26/down 18  sum  -121  max|d| 44
   pool_levels       4 movers  up  2/down  2  sum    +6  max|d|  7
back    198 rows · 9 movers · 27 value-field moves
by career games:  thin <=30g 106 movers (sum -704) · 31-80g 36 (-108) · >80g 12 (-7)
by cohort age:    age 0-3 carry 110 of the 154 movers and -843 of the -819 net
largest: jack-whitlock -85 · hussien-el-achkar -60 · luke-trainor -48 · jed-walter -44
```

**The channel is named, not guessed.** `rl_model.py:335-358` builds `BPK` / `POOL` / `BASEPK_REG` at
load time from the historical population `hist`, using each player's `pkbest`. The completed store
changes that population — ten players who had no seasons now have careers, thirty more have earlier,
lower-scoring seasons — so the band baselines shift. The board's own emitted tables show it moving:

```
BASEPK_REG  RUCK|2  86.716 -> 86.313      MID|6  77.026 -> 76.862
POOL        band 2  84.236 -> 83.844      band 6  71.248 -> 71.212   band 7  72.892 -> 72.803
```

Slightly lower early-career baselines, so young players with thin own-form are marked down. That is
a coherent, explicable effect of adding real (mostly modest) early seasons — and it is exactly the
"value effects the re-derivation carries, not bookkeeping" that ADDENDUM 1 named. It is also the
mirror of #328's store stage, which moved 175 of 804.

**But it is a surprise against this act's stated assert, so the act halts here.** No board identity
carrier was re-pinned, no UI bundle written, no board published. Whether a 154-row / net -819
indirect move on the live board is acceptable is not this seat's call.

## STEP 7b — THE GATES THAT DID RUN, ON THE CORRECTED PAIR

| gate | result |
|---|---|
| `one_source_selftest.py` | **145 PASS / 0 FAIL** (the landed count is 145) |
| G-Y0 national curve 1-64 | **0.033% <= 2.000% HARD** (n=1326 over 64 picks) |
| board == engine (F1) parity | PASS — all 804 active values == gated `ev()`, eps=0 |
| book == board (F2) | PASS — book rebuilt (`s4_matrix.json` `a206b911`) |
| all six FROZEN-RULER checks | PASS at curve source store `f1e8c9fe` (correctly unmoved) |
| LEG F5 entrant layer / seal `c9e7491b` | PASS, reconciled 62931 |
| board determinism | two runs, byte-identical `827fb1fd` |

---

## STAGE B — **NOT ENTERED. The box could not be classified, because the fit lane is barred.**

N35 requires the box to reproduce recorded fit bytes before any surface fit. The recipe is
`refit_v0surf.py --verify` on the pre-fix substrate, expected to reproduce `d594dc03…`. Run on a
**pristine `da9aa70` worktree** (store `f1e8c9fe`, curve `df766dff`, surface pin `d594dc03`), with
env pins 5/5 exact (Python 3.12.3 · numpy 2.4.4 · scipy 1.17.1 · scikit-learn 1.8.0 · openpyxl
3.1.5), bundled OpenBLAS byte-exact, `preboot_assert` PASS, `bootstrap.sh` rc=0:

```
AssertionError at _merged_recover.py:1909
  #326 HALT: the year-zero surface was NOT loaded from the freeze
  (signature af556bdca53dee20d4f73e0ae25a8127, refit declared='1').
```

**This is not a divergence; the fit never ran.** #326 landed an *unconditional* module-scope assert:

```python
assert _V0CURVE_META.get('_v0surf_frozen') is True, ...
# _v0surf_frozen = (_frozen is not None and os.environ.get('RL_V0SURF_REFIT') != '1')
```

`RL_V0SURF_REFIT=1` is the only way to fit, and it forces `_v0surf_frozen` False, so the assert
always fires. #326 used precisely this as its own non-vacuity RED
(`docs/evidence/act_326_2026-08-06/gate7_nosilentrefit_RED.txt`, same line 1909, same message).
There is no env gate around it. **The one committed refit lane is unreachable on landed main, for
`--verify` and `--bake` alike.**

Consequences, stated plainly:

1. **The box cannot be classified by the recorded recipe on this substrate.** Not "is not
   fit-class" — cannot be tested. What this box *did* prove is determinism-class: it rebuilt the
   landed board `864b6726` byte-exact from a pristine checkout, and rebuilt the candidate board
   twice byte-identically.
2. **Stage A does not need the lane**, because the signature does not move (above). Stage A stands
   on its own halt, not on this one.
3. **Stage B cannot run at all until the lane is reopened.** The re-derivation installs a new ruled
   curve; the curve is the `pvc` leg of the signature; a moved signature means the engine HALTs on
   the frozen pickle and demands a re-fit — which is the barred lane. So steps 9, 10 (matrix
   re-emit, curve re-derivation, surface re-fit, per-pick ±1 table, G-Y0 on the new pair, board
   rebuild with movers attributed) were **not run**, and no number is reported for any of them.

Reopening it is a small, ordered job for someone with the word to do it: the assert needs to
distinguish "a silent refit rode along in an ordinary build" (which it should keep catching) from
"the declared bake lane is deliberately running" (which it must permit, or the surface can never be
re-baked again). That is a code change and is not this seat's to make.

---

---

## STEP 7c — **THE HALT RULED ON. The owner gave the landing word; the board is published.**

Owner: *"land and rederive"* — the indirect movement (154 active rows, net −819, all attributed to
the store alone) is **accepted**. The step-7 halt is lifted and the act completes through the #328
step-6b pattern. Nothing is committed or pushed; the working copy is left landable.

**The correction to this act's own step-6 reasoning, recorded as one.** Step 6 left the two
board-derived carriers at `f1e8c9fe` with a stated reason — coherent only while no board is
published. Publishing ends that, and `ui/tools/ownership_store_apply.py` P3 would have reported
INCOHERENT BASE. `publish_board_334.py` completes the set.

| # | artifact | writer | move |
|---|---|---|---|
| 1 | `data/rl_build/rl_app_data.json` + `.srcmd5` | the canonical build; sidecar by `single_source.stamp_derived` | `864b6726` -> **`827fb1fd`**, sidecar **mirrored whole**, never hand-written |
| 2 | `data/expected_boot.json` `board` | surgical, byte-preserving, line count asserted unchanged | `864b6726` -> **`827fb1fd`** |
| 3 | `data/release_contract.json` `identities.board` | `release_contract.contract_hash` | pin moved; `contract_sha256` `0c85a56b…` -> **`7033d200632651de158afd3fb7c61db9fa30b017b9c0f512107c49634b0cbc9b`**, re-verified after the write |
| 4 | `ui/data/board_view_working.js`, `board_view_public.js` | `ui/tools/extract_board_view.py` | regenerated; its **RING-FENCE asserts PASS** against the new pins (`md5 head == board id`, store verified) |

`balanced_board_md5` `4939d740` deliberately **not** moved — a separate artifact, none built here.
`data/release_lineage.json` untouched (sealed history). The other four `ui/data` bundles are written
by other tools and carry no store or board identity — verified, not assumed.

**Re-run end-to-end from the finalized tree**, nothing carried forward: `preboot_assert` PASS ·
`bootstrap.sh` rc=0 with Guard 5 on `f1e7f20c` · board rebuilt **`827fb1fd`** (third independent
reproduction) · book rebuilt · **`one_source_selftest.py` 145 PASS / 0 FAIL** · G-Y0 **0.033% ≤ 2%
HARD** · F1 parity eps=0 · F2 book==board · all six FROZEN-RULER checks PASS.

**Six-carrier coherence: TRUE on store, TRUE on board.** Full table in `carrier_table_334.txt`.

**One thing found and worth naming, not caused by this act.** `s4_matrix.json` (the book) is keyed by
Python `id()` values, so its md5 differs between two otherwise identical processes
(`a206b911` then `4d69aae4`). It is a workspace intermediate — not in `data/rl_build/`, not pinned in
`expected_boot` or the contract — so nothing asserts it and nothing is broken. But it means the book
file is **not byte-reproducible by construction**, which any future byte-determinism claim about it
would be wrong to make. Flagged for the seam.

## WHAT IS FILED

`reparse_census_334.py` + `reparse_334.json` · `apply_store_334.py` + `expected_delta_table.json` ·
`store_before_f1e8c9fe.json` / `store_candidate_334.json` · `derive_rule_gate_334.txt` ·
`training_cells_334.py` + `.json` + `.txt` · `restamp_store_pins_334.py` + dry-run/apply logs ·
`v0surf_sig_store334.json` · `board_baseline_864b6726.json` / `board_store334_stage.json` ·
`board_zero_movement_334.txt` · `attribute_movers_334.py` + `attribution_store_334.json`/`.txt` ·
`touched_rows_not_on_board.txt` · `selftest_334.txt` · `book_rebuild_334.txt` ·
`boxclass_attempt_334.txt` · `BOX_CLASS.md` · this file.

Landing additions: `publish_board_334.py` + `publish_dryrun.txt` / `publish_apply.txt` ·
`ui_bundles_regen.txt` · `final_bootstrap.txt` · `final_build.txt` · `final_book.txt` ·
`selftest_final_334.txt` · `carrier_table_334.txt` · `final_diffstat.txt`.

**Nothing committed. Nothing pushed.** The working copy carries **eight** modified files and nothing
else — no untracked files, no mode changes:

```
data/expected_boot.json                 02262ef16c58ea6e5ad49f6f2ecf63b4
data/release_contract.json              75190cfc8ac2ecf17b238708f0e06bbb
data/rl_build/rl_app_data.json          827fb1fdfefe60c7c2c9026212d3992d
data/rl_build/rl_app_data.json.srcmd5   9a8d73d24dbc424dcface1a44b89c793
data/season_state.json                  0d3c413e82e6eea014107a4e51da2a7d
engine/rl_after/rl_model_data.json      f1e7f20c4adea9b17d19457a5217c735
ui/data/board_view_public.js            b5af10da87bc156c294f4690979a4ca1
ui/data/board_view_working.js           444e9f622d81bba3700792aa3ee0cbe4
```

**Stage B remains unreachable** and is unaffected by the landing word: the surface re-fit lane is
barred by #326's unconditional assert (`BOX_CLASS.md`). "Rederive" cannot start until that is
reopened.
