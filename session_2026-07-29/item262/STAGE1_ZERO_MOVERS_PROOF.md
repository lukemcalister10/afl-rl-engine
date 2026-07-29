# STAGE 1 PROOF — the vocabulary replacement moves no value and no rank

Owner ruling Q1, 2026-07-29: *"Prove the landing in two stages: the rename alone must show zero value
and rank movers; then my edits applied, with every mover reported and attributed to the specific
edited rows."*

This is stage 1: **the rename alone.** No owner edits, no per-season eligibility data.

---

## The instrument, verified before any edit

A clean build off unmodified `main` reproduces the pinned board
`750446d74e7c5d6edeb132168db53259` **byte-exact**. Establishing that first is what makes every
later difference attributable to the migration rather than to the environment.

Build lane: `RL_VENV` 3.12 venv on the pinned numpy 2.4.4 / OpenBLAS `05c9f9eb`, `bootstrap.sh`,
then `RL_CONFIG_MODE=bake python3 rl_export.py`. Serialised — no parallel engine builds.

## The v0surf gate, and why the board could be rebuilt at all

The first stage-1 build **HALTed** at the v0surf frozen-signature gate. `_v0surf_sig`
(`_merged_recover.py:1286`) hashes a `roster` term built from `str(MA.gfut(p))` — the position
**label string** — so any vocabulary replacement moves the signature by construction while the
grouping it describes is unchanged.

Under owner ruling R2-3 the reverse-map diagnostic was run and reproduced the frozen signature
**exactly**:

| | |
|---|---|
| signature, new vocabulary | `8faa737b18f575d4cbf3dad750fa2188` |
| signature, labels reverse-mapped | `76498b5a7a7a80db17f5bb9748ff1492` — **in the frozen set** |
| roster identical after reverse-map | **True** (1,448 rows) |
| pvc term identical | **True** (65 entries) |
| gates term identical | **True** (37 gates) |

The gate env-var names (`RL_RUC_PRIOR_CAP` and friends) contain `RUC` only inside a longer
identifier, so the word-boundary rename never touched them — that is why the gates term is
untouched, and it was verified rather than assumed.

Then, as ruled, cell-by-cell equality against the frozen surfaces before anything was pinned:

| | |
|---|---|
| surface sets refit under the new vocabulary | 2 |
| both reverse-map into the frozen set | yes — `8faa737b`→`76498b5a`, `b08a5a7e`→`1cbaf33d` |
| scalar cells compared | **5,496** |
| differences | **0 — cell-for-cell identical** |

Only then was the bake taken through the declared `RL_V0SURF_REFIT` lane:
`data/v0surf.pkl` `5b02f33b` → `4cfc0b99`, both signatures frozen, provenance appended to
`session_2026-07-18/legf6/v0surf_refit_log.json`.

**One precondition could not be evaluated, and is reported rather than substituted.**
`refit_v0surf.py` requires a *clean instance* defined as "balanced board == `06d8af60` byte-exact".
The tree's `balanced_board_md5` is `4939d740`, and per `docs/CURRENT_STATE.md` v26 that precondition
"tests a pre-split, unreachable board and **cannot be evaluated** — say so rather than substitute."
So it was not evaluated. What stands in its place is the cell-by-cell equality above, which is a
stronger statement than the precondition was reaching for: the refit on *this* box reproduces the
frozen surface exactly, so this box is not a weather box for this artifact.

## The relabel-aware diff — method stated, as criterion 3 requires

The new board is normalised by mapping the six new codes back to their pre-262 spelling wherever a
position label can appear:

- dict **keys** that are a bare token — `REPL`, `PEAK`, `PEAK_AGE`, `BETA_POS`, `ICPT_POS`, `PJ`, `GRACE`
- dict **keys** with a token in any pipe-separated component — `3|GEN_DEF` in `pm_pos`, `GEN_DEF|0` in `BASEPK_REG`
- string **values** that are a bare token — each row's `grp`, `gf`, and the label inside `fut`

Nothing else is touched. The normalised board is then compared to the baseline structurally, every
scalar. A single differing number would be a finding.

*(The `BASEPK_REG` form — token BEFORE the pipe — was missed by the first normaliser and showed up as
one spurious key-set difference. The normaliser was fixed to map every pipe-separated component. The
board was never in question; the instrument was.)*

## Result

```
scalar cells compared : 103,146
differences           :       0

active rows: baseline 804  new 804   same key set: True
VALUE movers (field v)                        : 0
RANK movers (order by v desc, key tiebreak)   : 0
per-numeric-field movers across all 804 rows  : NONE — every numeric field identical
```

The engine's own `PARITY GATE` also passed in the build: *all 804 active board values == engine gated
`ev()` (matched by key, eps=0)*.

## What moved, and what did not

| artifact | before | after |
|---|---|---|
| store `rl_model_data.json` | `e3aaba77` | `e4580f07` |
| board `rl_app_data.json` | `750446d7` | `3d4e2e50` |
| `rl_model.py` | `eb1e065a` | `293e21d6` |
| `_merged_recover.py` (engine_head) | `444831d5` | `404e8113` |
| `bust_prior_table.json` | `ffb54267` | `5942aa6a` |
| fv source-set tree hash | `6a9a520f…` | `d10aa93e…` |
| `v0surf.pkl` | `5b02f33b` | `4cfc0b99` |
| `season_state` derived values | — | **unchanged**, re-derived: `exposure_pace` 0.773, 305 durable players, median 17. Only `source_store_md5` moves. |

**Store field invariance**, verified against the pre-migration store record by record:

- 2,651 records in, 2,651 out · **0** records whose key set changed
- **0** non-position fields moved · **0** scoring arrays touched
- 6,365 position values remapped · **0** values outside the six new codes
- **0** old-vocabulary hits remain anywhere in the store (after R2-4)

## Sibling re-pins, both axes enumerated

**What STAMPS the moved identities:** `data/expected_boot.json` — `store`, `rl_model`, `engine_head`,
`fv`, `bust_prior`, `board`, `v0surf` · `data/release_contract.json` — `identities` + `held_candidates`
+ `contract_sha256` · `data/season_state.json` — `source_store_md5` ·
`data/rl_build/rl_app_data.json.srcmd5` — `own_md5` + `source_md5`.

**What READS the changed fields:** `rl_model.py` (`GRP`, `_ELIG_MAP`, `bnow`, `gfut`, `_collapse_elig`,
`y0dpp_bar`) · `pgrid.py` (`grp3`, the establishment surface) · `_merged_recover.py` (`GRPPOS`, every
`gfut` call, `synth`) · `rl_export.py` (`grp`/`gf`/`fut` labels, `alternate_position`) ·
`derive_lti_return.py` (three-way fallback) · `one_source_selftest.py` (schema guards, `_VOCAB`,
fixtures) · `collision_sentry.json` (pinned Max King expectations) · `ship_gates_check.py` (gate B) ·
the five position-keyed engine tables.

`bust_prior` was named by neither the directive nor the seam audit — Guard 5 caught it. It is a
**sixth** pinned identity beyond the five enumerated, and future vocabulary work should expect it.

Two new `held_candidates` declarations were added — `store` and `fv`. Both previously *agreed* with
the release, so neither was covered by an existing declaration and an undeclared mismatch would have
HALTed the gate. `board`, `engine_head` and `rl_model` had their candidate sides re-stamped;
`contract_sha256` re-stamped to cover all five.

## Two scope gaps found the hard way — recorded so they are not re-learned

1. **`pgrid.py` was invisible to the first live-input trace.** That trace listened only for `open`
   audit events, which never fire for a module reached through the import machinery. pgrid is
   imported by `rl_model`, and it holds the second half of a **duplicated** `grp3()` —
   `rl_model.py:954` and `pgrid.py:55` independently compute the same coarse GEN/KEY/RUC bucket, one
   READING the surface the other BUILDS. Migrating one side gave `KeyError: 'RUCK'`.

2. **Tests are not the build.** `collision_sentry.json` and `one_source_selftest.py` carry
   old-vocabulary *pinned expectations and fixtures*; no board-build trace can see them. They were
   found by running the self-test, not by reasoning about it.

Both were caught by the replaced-vocabulary ruling doing exactly what it was chosen to do: fail
visibly. A merged vocabulary would have bucketed every ruckman as GEN, silently.
