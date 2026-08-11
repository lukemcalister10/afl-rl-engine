# `daniel-butler` — THE RECORD SETTLES IT. HE IS A **POOL** ROW.

**This is not a blocker and no owner ruling is requested.** The record is unambiguous on every field that
matters, and the disagreement turns out to be a self-contradiction inside one instrument, not an ambiguity
in the data.

## 1. THE STORE, verbatim

`engine/rl_after/rl_model_data.json` (md5 `d9a24282357cf3083b1640466e3ecd83`), key `daniel-butler`:

| field | value |
|---|---|
| `player` | Daniel Butler |
| `type` | **`ND`** |
| `year` | 2014 |
| `pick` | **65** |
| `_pickless` | `False` |
| `draft_stream` | `ND` |
| `stream_pick` | **65** |
| `stream_year` | 2014 |
| `_draft` | National |
| `_draft_club` | Richmond |

There is no missing field, no null, no conflicting duplicate row, and no correction note. He was selected
at **national pick 65**.

## 2. THE RULING, in the engine's own words

`engine/rl_after/rl_model.py:264-268` (THE SPLIT, RULEBOOK v2.1 law 4):

> the national curve covers picks 1-64. A national selection at 65 or deeper is NOT on the curve — it
> enters the pool with every other pool entrant.

So the engine classifies him, and this is what it actually does at build time:

    _eff = 65 (POOL_PICK)   _pool = True   is_pool(p) = True   _teaches_curve(p) = False
    pool_division(p) = 'ND65+'

Verified live in the emitted matrix (`meta.store_md5` `d9a24282`, `meta.engine_head` `a8071af4`):

    is_pool_engine = True        teaches_curve_engine = False
    epk = 65                     band = '49-99'                raw_pick = 65

## 3. WHERE THE DISAGREEMENT COMES FROM — and it is one instrument contradicting itself

The matrix ALSO publishes `is_pool = False` and `teaches_curve = True` for him. That is the
Quinton-Boyd **force-majeure slide**: `paddy-mccartin` is the excluded 2014 pick-1 row, so every 2014 ND
pick above 1 slides up one slot for curve-attribution purposes. Butler's 65 becomes `pick_slid = 64`, and
`slid_membership()` (`emit_matrix_338.py:101-110`) then **re-derives arm membership from the slid pick**,
which `teaches_curve` (`:243`) consumes.

The emitter's own header already forbids exactly this, at `emit_matrix_338.py:49-52`:

> `_min_tenure` bands on `MA.effpk(p)` — the ENGINE'S OWN pick … That is deliberate and it is the
> conservative reading: … **the Q-B slide is a fit-population device for the curve, not an assertion that
> anyone was drafted a slot earlier.**

It applies that principle to the tenure band and then breaks it for arm membership one screen later. A
device that may not assert a different draft position also may not move a player across the wall — under
the ruling, the draft position **is** the arm.

The emitter has been printing the consequence on every single run, and it is one row:

    boundary crossers (pool -> ND fit via the slide): ['Daniel Butler']

(observed on all three ORDER 20 emits: BASE, P_x3.0, P_flat100.)

## 4. WHAT HE ACTUALLY DOES TO THE CALIBRATION TARGET — measured, not asserted

His `vpath` **does** move when pool prices move (base → `flat100`: `88 → 47`, `68 → 37`, tail `10 → 7/5`),
because he is priced as a pool entrant. Under the published `teaches_curve` he is inside the ND 1-64
numerator, so that movement leaks into `nd_profile`.

Under the ORDER 20 arm-split strata he happens to land in `prior_fallback_thin` and takes his own
`v0 = 349.4`, which is price-invariant — so the published-population `nd_profile` came out at exactly zero
drift **incidentally**. That is stated plainly here because it is a coincidence of this measurement and
not a structural guarantee:

| construction | his structural value, BASE | his structural value, flat100 | how |
|---|---|---|---|
| contaminated `S[(pos,t)]` | 222.0343676864 | 214.7006938368 | `completed` |
| arm-split `S[(arm,pos,t)]` | 349.4 | 349.4 | `prior_fallback_thin` |

The strata split alone therefore does NOT close this channel on principle — only on today's numbers. The
membership fix is what closes it structurally, which is why both are delivered.

## 5. THE FIX

`fix_matrix_membership.py` in this directory. `is_pool` / `teaches_curve` are quoted from the engine
(the `is_pool_engine` / `teaches_curve_engine` fields the emitter **already records** at `:240`); the slid
reading is kept and published as `is_pool_slid` / `teaches_curve_slid`, disclosed and never consumed.
`pick_slid` keeps its real job — curve attribution inside 1..64 — untouched.

It is applied to a **staged copy**. `docs/evidence/noarb_338_2026-08-06/emit_matrix_338.py` is filed
evidence of a landed act and this order does not write filed evidence. Landing the change in the
canonical emitter is a one-line edit for whoever owns that file.

**Effect: the national teaching population goes from n = 1,444 to n = 1,443. The one row is Daniel Butler,
and he goes where the store already says he is.**
