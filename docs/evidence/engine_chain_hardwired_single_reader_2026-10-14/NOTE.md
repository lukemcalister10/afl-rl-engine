# The adopted chain hard-wired (D3), one season-state reader, +2 panel per class — engine act, 2026-10-14

Owner word (verbatim, in chat 2026-10-13): "Yes, d3 was adopted. And should be reflected". The single
season-state reader and the panel fix are Phase 1 hygiene items from the owner-accepted plan (2026-10-13).

## What changed
1. **The ORDER 30B–43 chain is hard-wired** (`engine/rl_after/_merged_recover.py`, `rl_model.py`). 51 RL_* kill-switch
   reads become their shipped literals and the branches that could no longer run are deleted, including the two
   off-switch halts that raised NameError (`o41_injured`, `_O46`). `_merged_recover.py` 6,771 -> 6,386 lines; net
   −666 lines ignoring the de-indent of the 2,343-line preview lane. Every "NOT ADOPTED / OWNER WORD PENDING" label on
   the chain now reads adopted. Finding recorded on the way: `config_manifest.enforce()` and
   `staged_apply._assert_config_policy()` already refused every one of these flags in bake/gate/canonical builds, so
   each was a constant in every landed board; only a dev shell could ever set one. Left alone: the five infra flags
   (INFRA_ALLOW), the three `must_be_unset` override hooks in the release contract (RL_UNCOMP_S, RL_LSYM_TAB,
   RL_V0SURF_REFIT), and the three reads inside the declared v0-surface refit lane (RL_LENS_BASIS, RL_LANE_EXPECT,
   RL_V0_LENS). The frozen v0-surface signature table is untouched (RL_DAMP_K is one of its inputs).
2. **One season-state reader** (`engine/rl_after/season_read.py`). The three private `_season_val` copies (with a
   dev-mode fallback to the Round-14 literals 0.58 / 0.545) are gone; the one reader halts in every mode. CI's
   fenced test is restated to it (61/61).
3. **The +2 reconciliation panel** (`rl_export.py` draftAssetTotals) counts the two classes it shows: lens totals are
   per-class × classes, with a `per_class` block. CI's invariant proof reads it that way (restated 0cee65a8).

## Proof (build on the act tree, store b0eeaf4b)
Board e40c37cc vs the live board 848874f1: every top-level key byte-identical as JSON **except `draftAssetTotals`**
(+2: nClasses 2, visible 94,396, residual 18,920, total 113,316). No player value, rank or lens value moved.
Identities moving: board (the panel bytes), engine_head, rl_model, fv (conditional_prior.py). Store, config, register,
as_of_round unmoved. No blind review: the act is value-neutral by construction and the build is the review.
