# PREREG — the bust exclusion, applied to the live engine and to the draft-day record

**Date:** 2026-09-01 · written BEFORE the candidate board was inspected.

## The word

> "McCartin and Boyd should be excluded from everything. It's as if they weren't picked. So when
> looking at the value of pick 1 for the PVC, they didn't happen. For looking at KPF value for v0,
> they didn't happen. For your draft day analytics, they didn't happen."
> — owner, 2026-09-01

Standing authority: ENGINE_PRIMER §4.5 (the force-majeure exclusion, and the same-draft slide-up).

## What is being changed

1. `engine/rl_after/rl_model.py` — `BUST_EXCLUDE_KEYS = ('paddy-mccartin','thomas-boyd')` is declared
   and the existing `_pvc_exclude` flag is set on those two `hist` rows, so the machinery that has
   read that flag for months finally has something to read. A HALT fires if the cohort does not carry
   exactly the declared names, so a rename can never silently restore the old behaviour.
2. `ui/tools/gen_draft_outcomes.py` — reads that list out of `rl_model.py` (never restates it), drops
   both selections and slides the rest of their own draft up one pick.
3. `ui/app/draftday.js` — declares the exclusion on the page.

## The prediction, stated before the candidate board was looked at

**The shipped pick curve does NOT move.** `pvc_curve_v2.json` is a frozen ruler and its derivation
basis already excludes both men (`force_majeure`, `slide_years [2013,2014]`, 135 slid rows). Nothing
in this change re-derives it.

**The board DOES move, by a global rescale, and by nothing else.** `build_pvc_v34()` no longer ships
as the curve but its head still sets `BOARD_FACTOR = (RL_PICK1 / PVC[1]) * s`, which multiplies
`SCALE`. So the predicted signature of this act is:

- every active player's value moves;
- they move **coherently, in one direction, by one ratio** — relativities preserved;
- no reordering of the board;
- club ratings move by the same ratio;
- pick values (from the artifact) do not move at all.

If the observed board instead shows players moving in BOTH directions, or any rank change, the
prediction is wrong and this act does not land — it would mean the flag reaches the value path
somewhere other than the scalar, which is not what the code says.

**v0 does not move**, because `v0surf.pkl` is frozen and its signature covers `_PVC0` (the adopted
artifact) and the roster, neither of which this change touches.

> **Written here at the time, and WRONG:** *"That is also the finding that makes the owner's v0 clause
> NOT yet satisfied — see FINDINGS.md §3."* The v0 clause was already satisfied. The shipped v0 lens
> fits from a declared basis that excludes both men and applies the slide; the roster list I was
> reading feeds the freeze signature and the `RL_V0_LENS=0` A/B control, not the shipped fit. The
> sentence is left standing rather than edited out, because a prereg that gets quietly corrected after
> the fact is not a prereg. See FINDINGS.md §3 as corrected.

## Board identities

- before: `c8c2f2b6f99445484fadaa8c44afe609` (the pinned board, `data/rl_build/rl_app_data.json`)
- after: recorded in RESULT.md alongside the measured movers.
