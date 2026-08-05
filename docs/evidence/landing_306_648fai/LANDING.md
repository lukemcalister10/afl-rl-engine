# #306 — THE LANDING · seat `648fai` · 2026-08-05

Authority: the owner's EXECUTION word, *"Execute"* (2026-08-05), scoped to **the landing only**
(#306 comment 5189811177) · the artifact locations (5189920301) · the pool-structure ruling
(5190059333) · the hand-back's own checklist, `HANDBACK.md` §4 on branch
`claude/exec-306-pass-2-u8ir65` at `9451fae`, no re-spec.

**This lands as a branch. There is no merge here — the owner clicks.** Adoption stays the owner's
separate act; until then the shipped board and the owner-facing bundles are untouched.

The landing pair, fixed once and referenced throughout:

```
adopted curve   payload 01f27f0231929b285de83aaa6713048d   [:8] 01f27f02   pick 64 = 185 · pool_value 233.3
converged surf  ebc3d3303a1956a8ec94b4e2c1497bdf                [:8] ebc3d330
store 81d24704 (UNMOVED — see the HALT) · engine 15525b03 · band 34faa865 · sealed history untouched
```

## 0 · WHAT HAPPENED, IN ONE PARAGRAPH

The rehearsed landing set is installed and every gate that stands behind it was re-run in anger on
this box and passed. **One ordered item did not land: the #323 store batch.** The corrected store
moves the year-zero surface's config signature, so the engine refuses to build anything at all on it
while the converged surface is frozen — a measured, both-directions HALT, filed at
`HALT_323_STORE.md`, with the store install reverted in full. Separately, this box is **NOT
FIT-CLASS** under N35; the landing contains no fit act, so that does not block it, and it is recorded
at `BOX_CLASS.md` together with the cross-machine result it accidentally produced.

## 1 · THE CHECKLIST, ITEM BY ITEM

| # | item | state | evidence |
|---|---|---|---|
| 1 | adopted ruled curve `01f27f02` in `pvc_curve_v2.json`, contract re-stamped | **LANDED** | payload md5 recomputed here = `01f27f02`, 64 picks, pick 64 = 185; `release_contract.pvc_provenance.curve_payload_md5` agrees |
| 2 | converged surface bytes `ebc3d330` as `data/v0surf.pkl`; `expected_boot.v0surf` re-stamped | **LANDED** | `data/v0surf.pkl` md5 = `ebc3d330…`; boot pin agrees |
| 3 | N43 signed pool levels | **NOT IN THIS LANDING, by the seam's ruling** (5190059333) — the landing prices the pool at the single rehearsed level `pool_value` 233.3, which the candidate board already carries; the per-division set is the named follow-up | ruling 5190059333 |
| 4 | #323 store batch (Addenda 1–4), fixture `f1e8c9fe…`, and the text cleanup | **HALTED — did not land** | `HALT_323_STORE.md`, with the instrument, the probe and both probe outputs |
| 5 | the deliberate harness-pin halt, held as-is | **HELD, deliberately** | `harness_pvc_REPINNED.py` still carries `EXPECT_V0SURF = '1cbbd9b00ff4'`; no matrix was emitted at this landing, so nothing re-pinned it and nothing should have |
| 6 | G-Y0 dated exception retired; the 2.000% hard bar untouched | **LANDED** | `release_contract.held_checks` = `[]`, `_retired_checks` records G-Y0 with its measurement; the bar itself is unchanged |
| 7 | candidate board regenerated, byte-deterministic `46ebfb37`; the per-stage before/after assembled | **LANDED** | built twice on this box, `46ebfb37` both times; `before_after.md`/`.csv`/`.json` |

## 2 · THE GATES, RE-RUN IN ANGER ON THIS BOX

Not carried over from the rehearsal — re-measured here, on a different architecture, and each one
reproduced the rehearsal figure exactly.

| gate | result here | able to fail |
|---|---|---|
| Guard 5 boot-store | PASS, store `81d24704` == pinned | fired in anger during this seat: it PASSed on the corrected store `f1e8c9fe` only after the pin moved with it |
| `one_source_selftest.py` | **97 PASS / 0 FAIL**, rc=0 | one FROZEN-RULER check caught the pass-1 pin defect on its first run (rehearsal record) |
| G-Y0 national curve 1–64 | **0.033% ≤ 2.000% HARD** (n=1326), GREEN with no held record | fired RED at 3.035% pre-#279 |
| F5 entrant reconciliation | sealed `ed5b7fcc` 62726 == board emitted 62726, **MATCH** | a stale seal reprices to a different total and the render HALTs (L7 made this a hard assert) |
| F5 league gate · F4 roster gate | both **PASS** (±5%) | conservation law |
| board determinism | `46ebfb37` → `46ebfb37`, two builds | — |
| L8 completeness gate | **PASS** on the same-engine baseline | **HALTs** on the released board (store + engine named as unnamed causes) — both directions shown here |
| v0surf frozen-signature guard | **HALTED** the corrected store | passes on the rehearsal store — both directions shown at `HALT_323_STORE.md` |

The G-Y0 **pool leg** reports UNMEASURED as before (+110.953% vs the carried-over level 233, n=763).
Reported, not gated, and not a reason to move the level — the pool level is #207 stage 2 and the
owner's.

## 3 · THE BEFORE/AFTER — owner order 1 (#306 comment 5186108632)

Full table at `before_after.csv` (every player, one row), machine copy at `before_after.json`, built
by `before_after.py` with the **fixed** completeness rule: every common row's stages must sum to its
total, or the run HALTs. It ran clean — **804 players, 0 appeared, 0 vanished, 0 unexplained
residuals.**

```
stage 1  store lag + engine        801 movers   up   72 / down 729   sum  -52528   mean  -65.6   max|d| 1802
stage 2  curve+surface pair        601 movers   up  447 / down 154   sum    +954   mean   +1.6   max|d|   31
TOTAL    shipped -> landed         802 movers   up   76 / down 726   sum  -51574   mean  -64.3   max|d| 1833

stage 2, by dominant pricing channel
  ruled_curve       322 movers   up 287 / down  35   sum +1339   mean +4.2   max|d| 31
  year_zero_lens    255 movers   up 136 / down 119   sum  -466   mean -1.8   max|d| 22
  pool_levels        24 movers   up  24 / down   0   sum   +81   mean +3.4   max|d| 22
```

**Read the two stages apart, because they are not the same size.** Nearly all of what an owner would
see between the shipped board and this one is **stage 1** — the gap that was already open before this
job started, between the released board (`f2df6e0a`, store `6b9d00a7`, the retired engine `404e8113`)
and the engine and store the rehearsal actually ran on. **Stage 2 is the landing's own change**, and
it is small and two-sided: 601 movers, net `+954` across the league, largest single move 31 board
points — consistent with the L6 closure residual of at most one ladder point per pick carried through
the value path. Stage 2 reproduces the L8 attribution figure for figure.

**Stage 1 is two axes and is NOT split, by name.** Splitting store lag from engine needs a board built
on store `81d24704` under the retired engine `404e8113`. No such board is committed and this substrate
cannot build one. Reporting a split would be a figure not read from a committed artifact, so it is
reported as one stage and said so.

**The #323 store-correction stage is absent because it has no board.** See the HALT.

## 4 · WHAT THIS COMMIT CONTAINS

The rehearsal substrate `2b5e99eb` exactly — the state the hand-back describes, uncommitted under R-C
until now, verified byte-identical against its capture before and after every act of this seat — plus
this evidence directory. Nothing else. In particular:

- **`data/release_lineage.json` (sealed history) is untouched**, and no board pin moved:
  `expected_boot.board` and `release_contract.identities.board` both still read `f2df6e0a`. Moving them
  is the adoption act, not this one.
- **The owner-facing UI bundles are untouched.** Until adoption the shipped board is what the league
  sees.
- **The curve's own `curve_source_store_md5` provenance stays `81d24704`** — it records the store the
  ruled curve was derived on, which the selftest's FROZEN-RULER section states in as many words. It is
  not a live store pin and was not treated as one.
- **`tools/preboot_assert.sh` and the #279 panel machinery DO ride this commit** — 39 files, ~3.5 MB,
  all additions, nothing on `main` overwritten. They live on `claude/exec-seat-306-afl-rl-zlaarm` at
  `472c39d` and are absent from `main`, which is a real gap: every standing discipline in this era
  says *run `tools/preboot_assert.sh` before every workspace seeding*, and the file is not there to
  run. They are also load-bearing for the substrate itself — capture `2b5e99eb` is defined against
  `472c39d`'s non-docs tree, and **checklist item 5's deliberate stale pin lives in
  `session_2026-07-30/item279_step4/scripts/harness_pvc_REPINNED.py`** (`EXPECT_V0SURF =
  '1cbbd9b00ff4'`, verified present). Landing the set without them would leave item 5 with no file to
  hold the state and the capture with no base to verify against. Named here so the widened diff is a
  stated choice, not a slip.
- The `#306` rehearsal record (`docs/evidence/exec_306_u8ir65/`, `exec_306_2a1xa4/`, ~31 MB) is **not**
  duplicated here; it stands on its own branch at `9451fae`. The two files this seat's deliverable
  actually consumes — the L8 baseline board and the fixed attribution instrument — are copied in so
  this directory reproduces on its own.

## 5 · WHAT REMAINS OUTSTANDING AFTER THIS COMMIT

1. **The owner's merge click.** The seam audits the branch first.
2. **The owner's ADOPTION act**, separate and still withheld: the board pin, the UI bundles, the
   lineage entry.
3. **The #323 store batch as its own job** — refit, L6 re-entry, gates, captures. `HALT_323_STORE.md`
   states what it needs and why.
4. **The N43 per-division pool implementation**, ordered as a bounded follow-up by 5190059333; the
   owner chooses its slot relative to his adoption click.
5. **The text cleanup**, undefined on the record and therefore not landed.
6. **L-C's assert wired into the lane.** This seat measured the cross-machine result by accident of
   being handed a different architecture (`BOX_CLASS.md`); an assert that lives in the lane is still
   owed.
