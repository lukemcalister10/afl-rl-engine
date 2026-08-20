# STEP 2 — RL_GRACE ON AS THE CODE DEFAULT (PREREG P4)

**ORDER 29 · branch `land/order-29` · 2026-08-13.**

> ## P4 — HELD.
> With `RL_GRACE` defaulted **ON** in `engine/rl_after/rl_model.py` and added to the pinned manifest,
> **`RL_GRACE=0` still reproduces the dial-off board byte-for-byte** on an otherwise-unchanged tree.
> The dial stays a real dial; only its default inverts. The grace-A law is unchanged from ORDER 28.

## THE TWO EDITS

**1. `engine/rl_after/rl_model.py`** — one operative character, `'0'` → `'1'`:

```python
RL_GRACE=os.environ.get('RL_GRACE','1')!='0'      # was ...get('RL_GRACE','0')
```

`grace_years()`, `GRACE_G = 1`, `GRACE_MAX_ENTRY_AGE = 19`, `disc_factor`'s grace branch and all seven
call sites are **untouched**. The ORDER 28 law stands verbatim: entry age ≤ 19 ⇒ seasons 1 and 2 full,
the third season first diminished; entry 20+ ⇒ nothing; `grace_years(p)` keys on `p['year'] − by(p)`.
`engine/rl_after/rl_model.py` `5d1e7b7a8172c58cb2c8c49a0aaad77a` → `cb78e0efe129fdcd9c02be5364db4aab`.

**2. `data/model_config.json`** — `RL_GRACE: "1"` added to `vars`, and `config_sha256` re-stamped
through `config_manifest.canonical_hash` (the sorted `NAME=VALUE` digest), a **two-line diff**:

`config_sha256 bf0121056ee4437f407c9af42fbb760c1f4fd2a1fa7bfb9e13cdd94450615672`
→ `eed19a75f775aeafe4ee5ea4b3990667192d8f90389ad6b0e8318e91062d14c1`

This half is not optional and was named in advance. ORDER 28 §9.8: `config_manifest.enforce()` in
bake/gate mode **clears the ambient model environment and rejects unknown `RL_*` overrides**, so a
canonical landing build would have refused the dial while `RL_GRACE` was absent from the manifest.
Closed here, in the same commit that flips the default.

## THE CONTROL, AND WHY IT NEEDED A THIRD BUILD

The naive control — "flip the default, set `RL_GRACE=0`, check it matches the live board" — is not
available at this point in the build, because **the store has already moved** (Step 1). Comparing
against `88ce647f` would have measured the unflag-three, not the default flip, and would have
"failed" for a reason that has nothing to do with P4.

So the reference was **built, not assumed**: the same unflagged tree, with the *pre-flip*
`rl_model.py`, at its dial-off default. Both builds are on store `cb38ef11`.

| build | `rl_model.py` | its default | env | `rl_app_data.json` md5 |
|---|---|---|---|---|
| **B_U** — the dial-off reference | `5d1e7b7a` (pre-flip) | `'0'` OFF | `RL_GRACE` **unset** | **`71cbb13b3414d031135771dd7e564b3c`** |
| **B_G0** — the P4 control | `cb78e0ef` (flipped) | `'1'` ON | `RL_GRACE=0` | **`71cbb13b3414d031135771dd7e564b3c`** |
| **B_G** — the dial reachable | `cb78e0ef` (flipped) | `'1'` ON | `RL_GRACE` **unset** | `0017657e0469addda9260964938bad78` |

**B_U == B_G0, byte for byte — P4 HELD.** And **B_G differs**, which is what stops the control being
vacuous: a dial that was inert when on would have printed `71cbb13b` three times and proved nothing.

An attempt to run this control by staging a *foreign* `rl_model.py` into the scratch workspace was
**refused by the engine's own provenance guard** (*"the engine LOADED rl_model from … which is NOT
byte-identical to the trusted checkout … refusing to generate a board"*). That guard is working as
designed, and it is recorded here because it forced the control to be done the honest way — by
reverting the checkout, building, and restoring — rather than by shimming a file past it.

## WHAT MOVES BETWEEN B_U AND B_G

Nothing about the curve, the pool or the numéraire — those are Steps 3–6 and are not wired yet. The
only change between those two boards is the grace dial, on the already-unflagged store. Its
contribution is carried as its own lever in `docs/ledgers/LANDING_29_MOVERS_2026-08-13.md`, where
every stage delta is measured against the stage before it, so the levers sum to the total by
construction rather than by reconciliation.
