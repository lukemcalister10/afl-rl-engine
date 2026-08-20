# FINAL STATE — THE D8 ADOPTION, 2026-08-20

**Owner word, verbatim:** *"Yes. I'm adopting."* — 2026-08-20, given in chat post-compaction.
Register **v797** (`028eb4d`) recorded the intent; **v798** is the entry this act earns. The register is
the supervisor's pen and was **not touched** by this seat.

**Base:** `main` @ `028eb4d` · **Head:** `5dcfe71` · **UNPUSHED** (`origin/main` still at `028eb4d`).

> **THE LIVE BOARD IS NOW `5ea978f7b6a073abb2012f10cccbc3e3` — total 693,753 over 804 active rows.**
> The board of record `a05fe951f78482c70520480e184c80ec` / 664,949 is retired, and reproduces
> **byte-exact** under the declared kill-switch `RL_O33_TAPEROFF=0`.

---

## 1. THE COMMITS, IN ORDER

| # | sha | subject | paths |
|---|---|---|---|
| 1 | `16ec23bffea927de58476d23f582ab3740ead35e` | PREREG — THE D8 ADOPTION. Committed BEFORE the engine is touched (law F6). | `docs/evidence/d8_adoption_2026-08-20/PREREG_ADOPTION.md` |
| 2 | `d928bca554c2fdbb0419fc5818ec6b4460ae29a0` | THE D8 ADOPTION — THE ENGINE EDIT. RL_O33_TAPEROFF IS NOW THE SHIPPED DEFAULT. | `engine/rl_after/_merged_recover.py` |
| 3 | `5dcfe719fd971cdbc0045561af7da42bd850b265` | THE D8 ADOPTION — THE LANDING TRANSACTION. THE LIVE BOARD IS NOW 5ea978f7 / 693,753 / 804. | `data/expected_boot.json`, `data/release_contract.json`, `data/release_lineage.json`, `data/rl_build/rl_app_data.json`, `data/rl_build/rl_app_data.json.srcmd5`, `engine/rl_after/rl_app_data.json`, `engine/rl_after/rl_app_data.json.srcmd5`, `engine/rl_after/ingestion/{value,rank,pos_rank}_history.json`, `engine/rl_after/ingestion/sibling_repin_state.json`, `session_2026-07-20/fv_provenance_remediation/test_fv_provenance.py`, `.../fixtures/forward_vector_5ea978f7.json`, `.../fixtures/reference_vector_a49c155f.json`, `.../test_forward_lens_5ea978f7.py`, `ui/data/board_view_working.js`, `ui/data/board_view_public.js`, `ui/data/movers.js`, `ui/data/movers_transition.js` |
| 4 | `ae0f620…` | THE D8 ADOPTION — THE EVIDENCE AND THE FINAL ACCOUNT. | `docs/evidence/d8_adoption_2026-08-20/*` |
| 5 | *(this commit)* | THE D8 ADOPTION — FINAL_STATE names commit 4's sha. | `docs/evidence/d8_adoption_2026-08-20/FINAL_STATE.md` |

*(Commit 4's sha could not exist inside the file it commits, so it is filled in by commit 5 — the only
thing commit 5 does. `git log` is the authority on both; this table is a convenience, not a source.)*

Every commit used `git commit -- <explicit paths>`. No bare `git commit` after `git add`; no sweep.
Nothing pushed. `docs/OPEN_ITEMS_REGISTER.md` untouched.

## 2. EVERY IDENTITY, BEFORE → AFTER

| identity | before (`028eb4d`) | after (`5dcfe71`) | |
|---|---|---|---|
| **board** | `a05fe951f78482c70520480e184c80ec` | **`5ea978f7b6a073abb2012f10cccbc3e3`** | **MOVED** |
| board total / rows | 664,949 / 804 | **693,753 / 804** (+28,804, +4.3318 %) | **MOVED** |
| **engine_head** (`_merged_recover.py`) | `338a790b773cfbbff0e1283794c72efe` | **`3cfc4325aa323b7f26594cb2a202a976`** | **MOVED** (recomputed) |
| **balanced_board_md5** | `72fe3a176953fce36239d7b81c3cd492` | **`a49c155fa20f7084bcaa0d3dceca6cb1`** | **MOVED** (BUILT) |
| **contract_sha256** | `88d298264cc5c75e108599c0a44ef3c97b0058428ed9fab2789b21e05c363989` | **`7dc087563cda3c17a7a273830729076a97f1edcd81e767bba8f0c6fac6d0599d`** | **MOVED** |
| present_lens_baseline.present_value_total | 664,949 | **693,753** | **MOVED** |
| **config_sha256** | `eed19a75f775aeafe4ee5ea4b3990667192d8f90389ad6b0e8318e91062d14c1` | *same* | **UNMOVED** |
| **store** | `cc02567f80bef39228f25854d121a766` | *same* | **UNMOVED** |
| rl_model | `6fe7c4155866d80e8045bed2d3bf2802` | *same* | UNMOVED |
| fv | `6e9a370e5970c5aefa859858070f4c3420f0177b4698d6fac90bd08bf1780346` | *same* | UNMOVED |
| band | `34faa8659cc8f19794f5cb9584fa19b2` | *same* | UNMOVED |
| register (LTI) | `652d83e87780e415a01a2de6d8b3cc57` | *same* | UNMOVED |
| q97m | `cfdc73216c099e5e8f1fda3968f31c00` | *same* | UNMOVED (FROZEN) |
| v0surf | `5dd34ca82735f5c8f021b1c7320df8f8` | *same* | UNMOVED |
| as_of_round | 22 | 22 | **HELD** |
| day-0 reference `DAY0_CP.json` | `210510fe5d09bbbd16909bb63f4a118d` | *same* | UNMOVED |
| `data/model_config.json` | — | — | **NOT TOUCHED** |

**Why `config_sha256` does not move, and why that is the point.** `RL_O33_TAPEROFF` is a **DECLARED
KILL-SWITCH**, not a manifest dial — the `RL_CAPT` / `RL_ISOFADE` / `RL_EVW` / `RL_UNCOMP` /
`RL_ONEMACH` family, and the same lane THE BAKE (`f27482f`, v780) used for all 18 campaign dials. It is
deliberately absent from `data/model_config.json`, so `config_manifest.enforce()` still **REJECTS** it
as an unknown model override in bake/gate/canonical mode: **no certifying build can carry the name — it
can only ship the baked-in default.** Moving the manifest would have *destroyed* that property.

### UI bundle identities

| carrier | after |
|---|---|
| `board_view_working.stamp.board_md5` / `.board` / `.srcmd5` | `5ea978f7b6a073abb2012f10cccbc3e3` |
| `board_view_working.stamp.balanced_board_md5` | `a49c155fa20f7084bcaa0d3dceca6cb1` |
| `board_view_working.stamp.engine` | `3cfc4325` |
| `board_view_working.stamp.release.board` / `.engine_head` | `5ea978f7…` / `3cfc4325aa323b7f26594cb2a202a976` |
| `board_view_working.stamp.release.balanced_board_md5` | `06d8af60b679a12db07c064c60c065f9` — **correctly unmoved**: `round_movers.release_identity` reads this field from `data/release_lineage.json`'s frozen top-level present-lens baseline, not from `expected_boot`. Pre-existing and by design (the landing tail's own `02a_inject_release_contract.txt` shows the same). |
| `ui/data/movers.js` | `f0dc28ad…` → `8b79493c049093f18a8a2c61e16dc559` |
| `ui/data/movers_transition.js` | 9 register entries mirrored, `--check` exit 0 |

## 3. THE PROOFS — F1 AND F2, NEITHER FIRED

Built on the **edited tree** with the D8 pricing seat's own recipe: the accepted disposable FV builder
(`test_fv_provenance._run_build`), the byte-carried `d8_build.py` driver, `PYTHONHASHSEED=0`, BLAS
threads pinned to 1, staging into a throwaway dir, writing nothing under the repo, strictly sequential,
under `tools/build_lock.sh` (single writer).

| build | dial | md5 | total | rows | verdict |
|---|---|---|---|---|---|
| `BARE_DEV` | unset | `5ea978f7b6a073abb2012f10cccbc3e3` | 693,753 | 804 | **F1 PASS** |
| `BARE_CANON` | unset, `RL_CONFIG_MODE=canonical` | `5ea978f7b6a073abb2012f10cccbc3e3` | 693,753 | 804 | **F1 PASS** |
| `KILL_DEV` | `RL_O33_TAPEROFF=0` | `a05fe951f78482c70520480e184c80ec` | 664,949 | 804 | **F2 PASS** |

- **`BARE_DEV` and `BARE_CANON` are byte-identical** (1,223,960 bytes). Canonical mode *accepted* the
  shipped default — the manifest is unmoved and the build carries no `RL_` name.
- **`KILL_DEV` is byte-identical to the committed board file it replaced** — all 1,223,707 bytes.
- **`BARE_DEV` vs the priced candidate:** no board *artifact* for the priced candidate is preserved in
  `docs/evidence/d8_ceiling_2026-08-20/` (the pricing seat's driver copied it to a scratchpad since
  reaped; it committed the movers/bands/packet, not the board file). The byte-exact claim therefore
  rests on **md5 identity — which is a byte-exact claim** — against a value recorded **three times by
  two independent seats** (`ON_DEV_1`, `ON_DEV_2` in `BUILD_D8_out.txt`; `M_ON_DEV` in
  `REPRO_D8M_out.txt`), plus the row total 693,753 / n=804 recorded independently of the md5 in
  `MOVERS_D8_out.txt`. **Stated, not papered over: a diff that was not run is not claimed.**
- **F3** (identity re-proof after the repin) and **F4** (must-not-move list) and **F5** (gates): all
  enforced in-process by the landing scripts; none fired.

## 4. THE GATES

| gate | verdict |
|---|---|
| `python3 release_manifest_check.py` | **PASS** — 40 carrier fields, **38 coherent, 0 incoherent**, 2 sealed-lag |
| `python3 release_contract.py check` | **PASS** (contract `7dc087563cda`) |
| `python3 -m acceptance.runner` | **GREEN** — 7 checks, **PASS 7 / FAIL 0 / BLOCKED 0 / RULED-RED 0** |
| `sibling_repin.py verify` | **`ok: true`, 0 fails** (was **8**) |
| six-way store coherence | **PASS** — all six carriers `cc02567f` |

**No check was weakened, and no acceptance pin had to move.** The two **sealed-lag** stamps are the
pre-existing, reported-never-gating freeze-lag on `data/book_stable_seal.json`; the head side widened
`5ac6780f` → `3cfc4325` exactly as PREREG §3 F5 predicted. **The book is NOT re-sealed** — a re-seal is
a separate act and was not smuggled into this one (the `PACKET_D8` §2.1 precedent, verbatim).

## 5. THE LINEAGE ENTRY

`data/release_lineage.json` — **entry 9**, boundary `["22", "the-d8-adoption-20-8"]`, 35,150 → 42,622 bytes.

| | |
|---|---|
| kind | `movers_release_transition`, schema 2, `owner_approved: true` |
| ruling id | `THE_D8_ADOPTION_2026-08-20_yes_im_adopting` |
| owner_ruling | the word verbatim — *"Yes. I'm adopting."* — cited to register **v797** (intent) / **v798** (act) |
| source | board `a05fe951…`, store `cc02567f…`, engine_head `338a790b…`, balanced `72fe3a17…` |
| destination | board `5ea978f7…`, **store `cc02567f…` UNCHANGED**, engine_head `3cfc4325…`, balanced `a49c155f…` |
| `moved_by_transition` | `["balanced_board_md5", "board", "engine_head"]` |
| `unchanged_across_transition` | `["config", "fv", "register", "rl_model", "store", "v0surf"]` |

**Append-only discipline held and was proven, not asserted:** the 8 prior entries are byte-verbatim,
the file round-trips at `json indent=1` **before and after**, the top-level present-lens baseline
(`06d8af60`, `v2.11-present-lens-baseline`) is asserted **UNMOVED**, the store chain is continuous
(register tail `destination.store` == this entry's `source.store`), and no existing record declares
`destination.board 5ea978f7` — so this entry *creates* the boundary rather than superseding anyone's
ruling id. Both sides were **re-hashed** — `source` from a checkout of `16ec23b` (**proven
identity-identical to main `028eb4d`**), `destination` from the live tree — and each checked against
that commit's own `expected_boot.json`. Nothing was typed in.

**The Movers dropdown names the boundary:** out-of-round history column `the-d8-adoption-20-8`
(*"20/8 D8 ADOPTION — ceiling-only dial shipped default-on"*), 804 points written into each of the
three histories via the writer of record `out_of_round_column.add_column`, then
`generate_movers_transition.py` (9 entries mirrored) and `rebuild_movers_derived.py`, both `--check`
exit 0.

## 6. DEVIATIONS FROM THE BRIEF, AND WHY

1. **The `docs/evidence/d8_ceiling_2026-08-20/` board artifact does not exist**, so the brief's "diff the
   bare-build board against the priced candidate board file **if one is preserved**" resolved to its own
   escape clause. Recorded in §3 rather than claimed. The kill-switch board *was* byte-diffed, against
   the live board file, and is identical.
2. **`engine/rl_after/rl_app_data.json` + `.srcmd5` were moved too**, beyond the brief's named
   `data/rl_build` pair. Reason: it is the *generator's* output that `data/rl_build` is published from
   (`round_apply.py:141`), and **THE BAKE `48ec96f` moved the two in lockstep**. Leaving it would have
   left a tracked board file naming a retired board. Its sidecar's `source_md5` also advanced
   `cb38ef11` → `cc02567f`, correcting a lag left by the bake — disclosed in `03_landing_a_pins.txt`,
   not silent. The gate-read sidecar (`data/rl_build`) was already correct.
3. **`release_contract.json` lost one trailing newline.** The committed file carried one, added by the
   pricing seat's `d8_restamp.py:87`; the **writer of record** `restamp_dynamic:402` emits none. The body
   round-trips byte-exact; only that newline differs, and it is the writer's own format reasserting
   itself. Named in `04_landing_c_contract.txt` rather than absorbed.
4. **Two of this seat's own assertions were wrong and were corrected against the tree, never the
   reverse.** (a) `stamp.release.balanced_board_md5` was asserted against `expected_boot`; it is
   correctly sourced from the lineage baseline. (b) The `columns` list in the three histories was
   asserted prefix-append; the writer of record **sorts** it by `(after_round, id)`. Both re-checked
   against their real sources and both pass. Recorded because a seat that silently fixes its own failed
   assertion is indistinguishable from one that bends a result.
5. **A side effect worth naming, in the tree's favour:** the sibling rebuild this adoption required
   **discharged the 8-fail `sibling_repin` backlog** the landing tail had booked as a named future order.
   `verify` is now `ok: true`.
6. **`engine/rl_after/ingestion/.sibling_txn/txn_22_a49c155f/`** is left **untracked**. It is the sibling
   transaction's journal + originals backup; no prior reconcile ever committed one. It is scratch, and
   deleting a completed transaction journal by hand is worse than leaving it.

## 7. THE TREE

Committed and clean but for the untracked scratch named above. **Three commits ahead of `origin/main`,
UNPUSHED.** No tag. No promote. `docs/OPEN_ITEMS_REGISTER.md` is the supervisor's to pen.
