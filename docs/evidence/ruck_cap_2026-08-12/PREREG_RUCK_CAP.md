# PRE-REGISTRATION — THE 12-RUCK CAP TABLE (ORDER 20C)

> Committed **before any measurement was run**. Branch `build/ruck-cap-table`, cut from `origin/main`
> `591d082`. Measurement only: nothing is wired, no shipped default is changed, no board is promoted,
> `data/expected_boot.json` in the checkout is not restamped.

## THE OWNER'S QUESTION, VERBATIM

> "can you give me a list of the 12 players, what their rating was before this act, what it's going to
> be afterwards, and what it would be without the ruck cap?"

Three board values per player: **BEFORE** (HEAD engine, shipped defaults, the live board
`94f1fec5`), **AFTER** (the ORDER 20 par-separation fix), **NO-CAP** (the fix with
`RL_RUC_PRIOR_CAP` neutralised).

## PINS ASSERTED AT ENTRY (all three verified before this file was written)

| pin | expected | observed |
|---|---|---|
| board `engine/rl_after/rl_app_data.json` | `94f1fec59f99c59d5890d5975c79fa9b` | ✓ |
| store `engine/rl_after/rl_model_data.json` | `d9a24282357cf3083b1640466e3ecd83` | ✓ |
| instrument `docs/evidence/noarb_338_2026-08-06/noarb_table_338.py` | `0f8220351c64c56ccfa90c60edcdfa5f` | ✓ |

## §0 — WHAT I READ IN THE CODE BEFORE PREDICTING (declared, so the predictions are falsifiable)

1. `RUC_PRIOR_CAP=float(os.environ.get('RL_RUC_PRIOR_CAP','1.4'))` — `_merged_recover.py:1157`. It is
   a live env dial **and** a `data/model_config.json` manifest var (canonical `'1.4'`).
2. `_ruc_prior_cap(p,v)` (`:1219`) = `min(v, RUC_PRIOR_CAP·_cap_basis(p)·_ruc_head_v0(p))` for real
   RUCK rows. It is applied inside `_v0_raw` (`:1247`).
3. `v0_start(p)` (`:1756`): on the **board path** it returns `_V0CURVE[_v0key(p)]` — the frozen D14
   surface — and only falls back to `_v0_raw` when the row is **absent from `_V0CURVE`**. `_V0CURVE`
   is filled (`:1754`) over `real` = rows that are `_isreal` **and** `type=='ND'` **and** `pick is not
   None` **and** `not MA.is_pool(p)`. **Pool rucks are therefore not in `_V0CURVE`, and national ND
   rucks are.**
4. `RL_RUC_PRIOR_CAP` is a member of `_V0SURF_GATES` (`:1323`), so it enters `_v0surf_sig`. The frozen
   pickle has 2 signatures. A non-default cap therefore produces an unknown signature, and `:1719`
   **HALTs** rather than silently re-fitting.
5. `ev()` `:2237` is the only other consumer: `_cpv = _ruc_ceiling(p,Y)`, and `_ruc_ceiling` (`:1216`)
   falls back to `RUC_PRIOR_CAP·_cap_basis·_ruc_head_v0` **only when `bestlvl(p,Y) <= 0`** (no
   qualified production). With `bestlvl > 0` the ceiling is `RUC_CEIL_HEAD·interp(...)` and carries no
   `RUC_PRIOR_CAP` at all.

## PREDICTIONS

| # | prediction |
|---|---|
| **P1** | The HEAD board rebuilds to `94f1fec59f99c59d5890d5975c79fa9b` exactly. |
| **P2** | The FIX board (ORDER 20's two files staged as 20B did) rebuilds to `1dbd1480a34c7823f330273211cbb76a` exactly. |
| **P3** | Setting `RL_RUC_PRIOR_CAP=99` in **gate** mode HALTs on the frozen-signature check (§0.4). The dial is real; the halt is the proof it is read. |
| **P4** | Under the shipped `#306` lens the D14 surface is **cap-independent**: a declared refit (`RL_V0SURF_REFIT=1`) at cap 99 yields surfaces **value-identical** to the two frozen entries. |
| **P5** | A dev-shell build (no `RL_CONFIG_MODE`) with a v0surf pickle carrying the extra cap-99 keys, run at the **default** cap, still reproduces `1dbd1480…` — i.e. the no-cap lane's scaffolding is inert. |
| **P6** | **Of the 12 national binding rucks, at least 8 show a board-value delta of EXACTLY ZERO when the cap is lifted.** Their `_ruc_prior_cap` binding is latent: it cuts `_v0_raw`, and the board reads `_V0CURVE` instead (§0.3). |
| **P7** | The national rucks that DO move on cap lift are exactly those with `bestlvl(p,2026) <= 0` (no qualified production) whose `ev()` ceiling binds — §0.5. I predict **at most 4** such rows. |
| **P8** | **A majority of the 40 binding pool rucks DO move** on cap lift, because pool rows fall back to `_v0_raw` (§0.3). I predict **≥ 25 of 40**. |
| **P9** | Board totals: **NO-CAP ≥ FIX**, strictly. The cap only ever cuts. |
| **P10** | **Zero NON-ruck rows move** when the cap is lifted. (To be verified row-by-row over all 1002 rows, not assumed.) |
| **P11** | The ceiling `RUC_PRIOR_CAP·_cap_basis·_ruc_head_v0` moves on **0 of 71** ruck rows HEAD→FIX (ORDER 20B measured this; I re-take it). |
| **P12** | The six already-binding-under-HEAD national rucks are **not** the six ORDER 20B named. I will name them from the HEAD probe; no numeric prediction. |

## CLASSIFICATION RULE — FIXED IN ADVANCE

Each of the 12 is classified by a **measured** criterion, not a narrative one:

- **PRIOR-DOMINATED** — his NO-CAP board value **differs** from his AFTER board value. The cap is
  load-bearing on his price.
- **PRODUCTION-LED** — his NO-CAP board value is **identical** to his AFTER board value. The cap binds
  only on the latent V0 scaffold (`_v0_raw`), which the board does not read for him; his price is set
  by his production path.

The supporting reading (reported alongside, not used to classify) is `bestlvl(p,2026)`: `>0` = he has
qualified production the engine can price; `<=0` = he has none and the prior cap IS his ceiling.

**This is the thing the owner must see to read the table correctly**: a binding cap on the scaffold is
not the same as a cap that moves his price, and I expect most of the 12 to be the former.

## OWNED IN ADVANCE

If P6/P7/P8 break, the reading of §0.3 is wrong and the whole "latent vs live" framing in this packet
must be withdrawn, not patched. If P10 breaks, the cap has a channel outside the ruck rows and that is
a finding that outranks the table. Every breach is reported in the evidence with the number that broke
it.
