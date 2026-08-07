# Stage 1 — the identity re-pin, every field old -> new

The branch `variant/336-bust-inclusive` @ `3bbc688` deliberately did **not** commit its pin
updates (the variant kept them as uncommitted build-harness edits in a scratch worktree). This
landing branch takes the four engine files *and* re-stamps the pins in the same commit, which is
the standing rule in `data/expected_boot.json`'s `_fv_note` — *"Re-stamp ONLY at a bake, in the
same commit that moves an engine/forward_valuation source, exactly as the store/engine pins move."*

Every value below was **recomputed from the checkout using the guard's own rule**, not copied from
the #336 evidence. All four independently reproduce the identities recorded in
`docs/evidence/act_336_variant_2026-08-06/amend3/RUN_RECIPE.md`.

## Fields changed (4)

| field | recompute rule (boot_guard.py) | old | new |
|---|---|---|---|
| `rl_model` | block (0f): `md5(engine/rl_after/rl_model.py)` | `33f940735281a07e3b6ca19f31bf2ea6` | `b35c5521b78dcdfb2423d54f5574330b` |
| `engine_head` | `_chk('ENGINE _merged_recover.py', …)`: `md5(engine/rl_after/_merged_recover.py)` | `8f0e3eb1b29fee6b2defa0a5cfd7ebec` | `e3527be4195732b2e271e9e10ed40ce4` |
| `fv` | `fv_provenance_fails` -> `fv_provenance.fv_identity(engine/forward_valuation)` — sha256 tree hash over sorted relpaths + per-file sha256 of all 8 `*.py` | `d920557ef21d0eec6434853b07869dd4c0b98f64e99e79ecbb8ee54c704ecf4a` | `0976195c84541204c0325831bb60a660d1eb5ffc2f8e8a4e8ba18f85f5f18a87` |
| `board` | block (0c): `md5(data/rl_build/rl_app_data.json)` | `113b36f898a32363c49c2a62fb809f4b` | `de5110bb57a04d9b24e9c761241e54c7` |

`fv` moves because **two** of the four files (`par_build.py`, `par_redesign.py`) live in
`engine/forward_valuation`; `engine_head` moves because `_merged_recover.py` is one of the four
(it was *not* touched by the earlier two-file cut of #336, where that pin held).

### On the `board` pin — disclosed

The checklist named `fv` / `engine_head` / `rl_model`. The `board` pin was stamped **as well**,
because step 7 lands the rebuilt board at `data/rl_build/rl_app_data.json` and Guard 5 block (0c)
asserts that exact file against this pin at full hash. The stale pin was proven to halt
non-vacuously before it was moved:

```
==================== STALE-BOOT GUARD (Guard 5) FAILED — BUILD HALTED ====================
  - checkout board de5110bb != pinned board 113b36f8 (data/expected_boot.json 'board', full-hash
    compare) — the board and its pin are out of sync (re-generate + re-pin, or the pin drifted)
=========================================================================================
```

Leaving it stale would have committed a branch that halts on line one. It is one field and is
trivially revertible if the seam wants the board landed unpinned instead.

## Fields deliberately NOT touched

| field | value | why it does not move |
|---|---|---|
| `store` | `37ced3ce…` | the store is read-only across the whole act — no store write |
| `v0surf` | `d594dc03…` | the year-zero surface is **HELD** at the shipped survivors-basis fit (the ruled basis; no `RL_V0SURF_REFIT`) |
| `balanced_board_md5` | `123deccb…` | a separate present-lens lineage field, not a Guard 5 identity |

`band`, `config`, `q97m`, `peak_model`, `pvc_snapshot`, `bust_prior`, `register` all re-asserted
unchanged by bootstrap — no fitted artifact and no manifest dial moved.

## Verification

`bootstrap.sh` Guard 5 **PASS on the first attempt**, no halt, nothing weakened:

```
boot-store guard (Guard 5) PASS  [bootstrap]  store 37ced3ce == pinned 37ced3ce
  |  rl_model b35c5521 == pinned b35c5521  |  fv 0976195c == pinned 0976195c (checkout+loaded-path)
```

A standalone `boot_guard.py` run after the board was landed and its pin stamped also returns
`PASS` / exit 0 — the committed branch is self-consistent.
