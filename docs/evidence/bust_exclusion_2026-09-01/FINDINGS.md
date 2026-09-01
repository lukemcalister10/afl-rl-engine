# The bust exclusion: where it was, where it wasn't, and what applying it actually moves

**Date:** 2026-09-01 · maintainer note. Renders nowhere on a user surface.

## The owner's word

> "McCartin and Boyd should be excluded from everything. It's as if they weren't picked. So when
> looking at the value of pick 1 for the PVC, they didn't happen. For looking at KPF value for v0,
> they didn't happen. For your draft day analytics, they didn't happen."
> — 2026-09-01, on being shown both men in the draft-day record at pick 1, unslid.

This restates and widens ENGINE_PRIMER §4.5, which has carried the ruling for months:

> "Paddy McCartin and Tom Boyd (pick-1 KPF busts, force majeure) are excluded by owner ruling; every
> player in their drafts slides up one pick. If a KPF number looks bust-driven, check the exclusion
> applied before theorizing."

## THE FINDING, in three parts — and the first part is good news

### 1. The shipped pick curve ALREADY excludes them. "For the PVC, they didn't happen" is true today.

`pvc_curve_v2.json` is a FROZEN RULER by owner ruling (ITEM 408 / R1=C, asserted in
`one_source_selftest.py:514`): bound to source store `f1e8c9fe`, deliberately not tracking the weekly
store. It is the shipped pick currency — `rl_model.py:1541`: *"the pick side is overwritten downstream
by the adopted artifact pvc_curve_v2.json … The rescale on the next line never reaches the shipped
curve."*

Its own derivation basis, `docs/evidence/store_328_jujn3g/per_entrant_328_corrected_store.json`,
carries the ruling in its meta and applied it:

```
"force_majeure": ["paddy-mccartin", "thomas-boyd"],
"slide_years": [2013, 2014],
n_records 2645 · slid rows 135
paddy-mccartin  ABSENT from the basis
thomas-boyd     ABSENT from the basis
```

135 rows slid up — the identical count the draft-day board now slides. So the prices the estate pays
for picks were derived with both men struck out, exactly as ruled.

### 2. The live engine flag has never once been set.

`rl_model.py` has read a `_pvc_exclude` flag for months, with a same-draft slide (`_pvc_eff`) and a
registered-sample self-test that fails BY NAME if any one fit site drops the gate. Measured on the
pinned store `415929d3`: **zero rows of 2650 carry the flag.** Both men sit in the store at pick 1,
unslid.

The gate is therefore gating an empty set at every site, and the primer's instruction — *"check the
exclusion applied before theorizing"* — has had a false answer available for its whole life. It does
not corrupt the shipped curve (that curve is the frozen artifact, derived correctly offline), but it
means the LIVE fit and the ADOPTED curve were built on different populations, and only one of them
knows it.

What the live flag actually reaches today is `build_pvc_v34()`'s **head**:

```
BOARD_FACTOR = (RL_PICK1 / PVC[1]) * numeraire.s      # rl_model.py:1556
SCALE        = SCALE * BOARD_FACTOR                   # scales EVERY player
```

`PVC[1]` is the v3.4 pre-anchor head (4441 before this change). Striking out two pick-1 rows raises
that head, so `BOARD_FACTOR` falls and `SCALE` with it — a whole-board reprice arriving as a side
effect of a draft-record correction. Measured in RESULT.md: −2.08% across the board and 266 real
order crossings, so it is NOT the clean rescale the surrounding comments assume.

### 3. v0 DOES still learn from both of them. This is the real hole.

`_merged_recover.py:2237` builds the v0 pick surface's population:

```python
real = MA._curve_sample('v0_kernel', 0,
    [p for p in MA.data if _isreal(p) and p.get('type')=='ND' and p.get('pick') is not None
     and not MA.is_pool(p)])
```

The comment above it says *"Same gate as every other fit site"*. It is not: it applies the POOL gate
and not the exclusion gate. And `_isreal(p)` is `p['key'] in set(every store key)` — it does not mean
"currently playing", so retirement does not remove them either.

Both men are ND rows with picks, so both currently teach the v0 KPF pick surface. That is precisely
what the owner ruled out — *"for looking at KPF value for v0, they didn't happen"* — and it is not
true today. The fix is one filter. The cost is that `_v0surf_sig` hashes the roster, so the signature
moves, the frozen surface no longer matches its key, and `data/v0surf.pkl` must be re-baked
(`RL_BAKE_V0SURF=1 … refit_v0surf.py --bake`) on a clean instance and re-pinned.

## The slide was verified against the estate's own, not just against itself

The draft-day slide is not a second opinion about who moves up: it reproduces the curve derivation's
slide exactly. Cross-checked row by row against `per_entrant_328_corrected_store.json`, which records
`pick_stored` and `pick_slid` for every row the adopted curve slid:

```
engine slid rows                 135
agree with the draft-day slide   135
disagree                           0
not found in the draft record      0
```

Same men, same new ordinals, computed independently from the live store by a generator that loads no
engine. If the two had disagreed, one of them would be wrong about what pick 1 of 2013 means.

## What was landed, and what is owed

**LANDED — the draft-day half**, which needed no engine act and is what the owner asked for by name.
Both men are struck from `ui/data_aux/draft_outcomes.js` and the 135 selections behind them slide up
one, so no ordinal loses an observation (picks 1 and 2 still carry 23, one per class). The names are
declared once, in `docs/inputs/OWNER_BUST_EXCLUSION.json`, and read from there — never restated in
code. The exclusion list is folded into the bundle's input signature (`SIG_VERSION` bumped to
`draft-outcomes-inputs-2`), because the list is not a store field and a signature blind to it would
report "up to date" over a bundle built under a superseded ruling.

Measured on the shipped board, fully-run population, key forward:

| pick | VOR | clears bar | star | before |
|---|---|---|---|---|
| 1 | 17.3 | 71% | 38% | 15.9 · 68% · 36% |
| 3 | 18.1 | 74% | 43% | 16.8 · 72% · 40% |
| 6 | 16.9 | 70% | 43% | 15.9 · 69% · 41% |

Other columns move a little too, because the slide moves real men between ordinals — small forward at
pick 3 reads *worse* (12.1 against 13.2), which is what an honest slide looks like.

**OWED — two acts, each of which reprices, so each is put to the owner rather than taken:**

1. **The v0_kernel gate** (`_merged_recover.py:2237`) — one filter, plus a `v0surf.pkl` re-bake on a
   clean instance and a re-pin. **This is the one clause of the ruling that is not true today.**
2. **The live engine flag.** `BUST_EXCLUDE_KEYS` in `rl_model.py`, setting `_pvc_exclude` on the two
   `hist` rows. Correct in itself — the live fit should see the population the adopted curve was
   derived on — but **built and measured, and it is not the cosmetic rescale the code implied**:
   board `c8c2f2b6` → `b005096b`, 622 of 804 players down, none up, sum −2.08%, and **266 true order
   crossings** (pairs strictly distinct on both boards that swap). See RESULT.md. That reorders the
   board, so it is a repricing with trade consequences, not a restatement. Held for the owner's word.

Both were written, built and measured, then **reverted pending word**; the engine tree is byte-exact
to its pin and `restamp check` agrees on all five stamps. `ui/tests/draftday.test.js` pins BOTH holes
OPEN with assertions that fail the day either is fixed, so the fix cannot land without this record
being updated to match — the estate does not get to half-apply the same ruling twice.

**NOT owed:** a `derive_pvc2.py` re-derivation. The adopted curve already excludes them.
