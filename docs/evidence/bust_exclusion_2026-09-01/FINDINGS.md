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

## THE FINDING, in three parts — and only the middle one is a defect

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

### 3. v0 does NOT learn from either of them either. (CORRECTED 2026-09-01 — I had this wrong.)

**What I reported first, and why it was wrong.** I read `_merged_recover.py:2237`, saw the v0 kernel's
population built with the pool gate and not the exclusion gate, and reported that both men still teach
the v0 KPF surface. The owner pushed back: *"Given the pick curve doesn't, and v0 across positions is
mean to = pick curve pvc, then surely the KPF v0 doesn't learn from those two?"* He was right.

**The `real` list I quoted does not teach the shipped surface.** `RL_V0_LENS` defaults to `'1'` and is
not overridden in `data/model_config.json`, so the lane that ships is the #306 LENS. It does not fit
over the roster at all — it fits over a DECLARED EXTERNAL BASIS, and refuses to fall back:

```python
_lensf = .../docs/evidence/exec_306_zlaarm/basis/structural_basis_279.json
if not os.path.exists(_lensf):
    raise SystemExit("v0 LENS BASIS MISSING: ... There is deliberately no fallback: fitting
                      the lens from the surface's own prior is the barred, self-referential lineage.")
```

`real` is used for two things, neither of which is teaching: the freeze signature `_v0surf_sig`, and
the **pre-#306 free fit retained behind `RL_V0_LENS=0` as the declared A/B control**. That control lane
is the code I read and reported as if it shipped.

**And the basis carries the exclusion by construction.** `emit_structural_basis.py` imports
`harness_pvc.load_matrix` + `structural_values` unmodified and lists what it inherits wholesale —
*"McCartin/Boyd exclusions and one-pick slides as the committed matrix carries them"*. Verified
directly against the artifact's 1,197 rows:

```
paddy-mccartin      ABSENT
thomas-boyd         ABSENT
joshua-kelly        store pick 2  ->  basis pick 1
christian-petracca  store pick 2  ->  basis pick 1
jack-billings       store pick 3  ->  basis pick 2
marcus-bontempelli  store pick 4  ->  basis pick 3
```

The same two men struck out and the same one-pick slide the draft-day board now applies. The chain is
matrix → `structural_values` → `structural_basis_279.json` → the v0 lens → `v0surf.pkl` → the board's
v0. Both men are out of every link of it.

**So all three of the owner's clauses are true.** No v0surf re-bake is owed.

## §2 RE-MEASURED — the head is 3784, not 4441, and this is a mis-scaling not a side effect

The owner asked the right question: *"Pick 1 = 3000 is the scaler … so knowing the true worth of pick 1
is important. However, you're telling me that the scaling is based on the OLD curve? … I assume 4441 is
a relic of the old system?"*

Both halves are right, and one number I gave was wrong.

### 4441 was quoted from a stale comment. Measured, it is 3784.

`rl_model.py:1540` says *"measured 4441"*. It is not 4441 today. Measured live
(`measure_anchor_head.py`, output beside it):

```
BOARD_FACTOR                  0.7453156150     (from the module itself)
numeraire s                   0.9400914291     ( = 3000 / 3191.178972 )
=> head the anchor used       3000 * s / BOARD_FACTOR  =  3784.0000
re-measured directly                              3784        (agrees exactly)
```

Re-calling `build_pvc_v34()` after import does NOT give this number — it gives 2821 — because step 5
anchors to `build_pvc(ALPHA)`, which reads `SCALE`, and the module MUTATES `SCALE` at the anchor line.
2821 = 3784 x BOARD_FACTOR: the same head, restated in the currency the anchor just created. Restoring
the pre-anchor `SCALE` reproduces 3784 exactly. Worth writing down, because the naive re-call is the
obvious way to measure this and it is off by 25%.

### The two heads are different numbers from different fits

```
the ADOPTED curve's own measured head    3191.18   published at 3000, s = 0.940091
the v3.4 kernel's pre-anchor head        3784      a superseded fit
```

`BOARD_FACTOR = (3000 / 3784) x 0.940091 = 0.745316`. The `s` term is the adopted curve's. The
`3000 / 3784` term is the OLD curve's head. So the PLAYER side's absolute level is set by a superseded
fit's opinion of pick 1, and that opinion is measured on a pick-1 population that STILL CONTAINS
McCartin and Boyd.

`_load_numeraire`'s own docstring says E6 existed to stop the player side *"silently falling back to the
v3.4 pre-anchor head"*; the formula still divides by it, and `rl_model.py:1548` defends that as the
player side's *"own natural scale"*. Whichever reading is right, the population that head is measured on
should be the ruled one.

### What the exclusion does to it

```
v3.4 pre-anchor head   3784 -> 3877     (+2.458%)   two pick-1 busts removed, 197 cohort rows slid
BOARD_FACTOR       0.745316 -> 0.727437  (-2.399%)
```

That is the whole of the board's -2.08% move, and it reframes it. **This is not a cosmetic side effect
to be avoided. It says players are currently priced about 2.4% expensive relative to picks, because the
exchange rate between them was measured on a pick-1 sample containing two men the owner ruled out.**

### One thing still unexplained

A single scalar should move every value by one ratio, and it does not: 266 true order crossings, and the
1000-3000 band spans ratios 0.9757-0.9930. The likely mechanism is the ISO correction table
(`_merged_recover.py:1092-1098`), which is rebuilt from `raw_ev(synth(...))` and is therefore
SCALE-dependent, so a change in SCALE reshapes the per-position multipliers rather than passing through.
**That is a hypothesis, not a measurement** — it has not been traced, and it should be before the act
lands.


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

**OWED — ONE act, and it reprices, so it is put to the owner rather than taken:**

**The live engine flag.** `BUST_EXCLUDE_KEYS` in `rl_model.py`, setting `_pvc_exclude` on the two
`hist` rows. It is now the ONLY place on the estate where the ruling is not applied: the adopted pick
curve excludes them, the v0 lens basis excludes them, the draft-day board excludes them, and the live
v3.4 import fit is the last hold-out.

**Re-framed after the anchor head was measured (§2 RE-MEASURED, below).** This is not a cosmetic
rescale to be avoided. The v3.4 head is the exchange rate between players and picks, it is measured on
a pick-1 sample that still contains both men, and correcting it moves that head 3784 → 3877. So the
board's −2.08% is the size of a live mis-scaling: **players are currently about 2.4% expensive relative
to picks.** That is an argument FOR the act, not against it.

The cost is still real and still unexplained in one respect: 622 of 804 players down, none up, and
**266 true order crossings** (pairs strictly distinct on both boards that swap), where a single scalar
should produce none. The likely cause is the SCALE-dependent ISO table, but that is a hypothesis and
has not been traced. No pick price moves either way — the pick curve is the frozen artifact and is
already correct.

It was written, built, measured and then **reverted pending word**. The engine tree is byte-exact to
its pin and `restamp check` agrees on all five stamps. `ui/tests/draftday.test.js` pins the hole open
with an assertion that fails the day it is fixed, so the next attempt starts from a failing test
rather than a rediscovery.

**NOT owed:** a `derive_pvc2.py` re-derivation, or a `v0surf.pkl` re-bake. Both already exclude them.

## The correction, recorded

The first version of this note claimed v0 still learned from both men and that a v0surf re-bake was
owed. That was wrong, and it was wrong in a specific way worth naming: I read the code lane that is
retained as a declared A/B control (`RL_V0_LENS=0`, the pre-#306 free fit over the roster) and reported
it as the lane that ships. The shipped lane fits from a declared external basis that inherits the
exclusion by construction. The owner caught it by reasoning from the model rather than the code —
if the pick curve excludes them, and v0 is denominated in the pick curve, then v0 excludes them — which
is the check I should have run before filing.
