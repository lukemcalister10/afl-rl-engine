# STATE — GENERATED-ONLY · DO-NOT-HAND-EDIT

> **THIS FILE IS MACHINE-WRITTEN AND REGENERATED AT EVERY LANDING.** The landing library
> writes it as a late step of both sequences (`land lever` and `land round`, step `state`);
> `python3 -m tools.landing.state write` regenerates it on demand. Every value below is
> COMPUTED from the carrier named beside it — nothing here is typed, and nothing here is
> authored. **Do not hand-edit:** an edit is overwritten at the next landing, and
> `acceptance::state_file` reds the tree before then.
>
> **This file states no law and settles no dispute.** The laws are `docs/RULEBOOK.md`; the
> record is `docs/register/`; the identities of record are the carriers. Where this file and
> a carrier disagree, the carrier is right and this file is stale — which is a red, not a
> footnote (process law P6: a derived surface that cannot be generated does not exist).

## CURRENT IDENTITIES

Pinned value from the carrier, beside the artifact re-hashed in this tree. `agrees` is a
measurement made while this file was written, not a claim carried over from the last one.

| identity | pinned value | carrier | re-hashed from | verdict |
|---|---|---|---|---|
| board | `b3e8da99bc7f632e5d1eebc732f9cf01` | data/expected_boot.json | data/rl_build/rl_app_data.json | agrees |
| store | `b745002eb0a0fbb1c34fa44f1ef708d6` | data/expected_boot.json | engine/rl_after/rl_model_data.json | agrees |
| engine_head | `3af8c1f7d61275c198a5df70c34608c7` | data/expected_boot.json | engine/rl_after/_merged_recover.py | agrees |
| rl_model | `6fe7c4155866d80e8045bed2d3bf2802` | data/expected_boot.json | engine/rl_after/rl_model.py | agrees |
| balanced_board_md5 | `7c32a540578b799922daea41d8acdfa2` | data/expected_boot.json | (no in-tree artifact) | not in tree |
| config | `eed19a75f775aeafe4ee5ea4b3990667192d8f90389ad6b0e8318e91062d14c1` | data/expected_boot.json | config_manifest.manifest_hash | agrees |

| release fact | value | carrier |
|---|---|---|
| contract seal | `1b435ff6f988f52b5f395dc7b5b90152ee0679c97d63f6928f18cefd1f89eb3e` | data/release_contract.json:contract_sha256 |
| config seal | `eed19a75f775aeafe4ee5ea4b3990667192d8f90389ad6b0e8318e91062d14c1` | data/release_contract.json:config_sha256 |
| release version | v2.11-final-rc1-PROVISIONAL | data/release_contract.json:release_version |
| round (as_of_round) | 23 | data/release_contract.json:as_of_round |
| round (as_of_round) | 23 | data/expected_boot.json:as_of_round |
| declared held checks | 0 | data/release_contract.json:held_checks |

BOOT vs CONTRACT, computed here rather than assumed: board agree · store agree · engine_head agree · balanced agree · round agree.

## THE LAWS

The single governing document, and its own lint's verdict — a pointer without a verdict is a
gate claimed by name (process law P5).

- **docs/RULEBOOK.md** — md5 `e1780324f39c82a842579f22c09adb6b`
- header: # THE RULEBOOK — v3 · 2026-08-20 · OWNER-SIGNED (in chat, 2026-07-22; amended 2026-07-28, 2026-08-20)
- `tools/rulebook_lint.py` verdict: **PASS** — rulebook_lint: 0 FAIL

## THE RECORD

- **docs/register/LATEST.md**, line 1, quoted:

  > # OPEN ITEMS REGISTER · v824 2026-08-21 · **THE BLIND COMPARISON IS FILED (docs/proposals/REBAKE_COMPARISON_2026-08-21.md) — the owner's protocol executed to the letter: study B commissioned and completed blind (independence declaration in its header; one filename-level leak excluded and unopened), study A opened by the supervisor only after B filed.** ELEVEN INDEPENDENT AGREEMENTS = the confidenc

- new-form entries under `docs/register/entries/`: 12
- frozen predecessor `docs/OPEN_ITEMS_REGISTER.md` — md5 `219021ace49ff2750a6576cb9ac8368c` (byte-sealed; `tools/seat/pen.py verify` is its gate)

## LINEAGE TIP

`data/release_lineage.json` — the append-only out-of-round transition register, 13 entries.

| field | value |
|---|---|
| column | the-staircase-adoption-21-8 |
| after round | 23 |
| board moved | `68be10c79d0ee096455754e084bcf757` → `b3e8da99bc7f632e5d1eebc732f9cf01` |
| identities moved | board |
| owner ruling id | THE_STAIRCASE_FIX_ADOPTION_2026-08-21_A_raw_I_prefer_lock_that_in_unconserved |

## GENERATION STAMP

| field | value |
|---|---|
| generated at commit | `33b7fe7dd4efbe74c0cad7508c9cb8c8a6793da0` |
| tool | `tools/landing/state.py` |
| written by | land lever (step `state`) · land round (step `state`) · python3 -m tools.landing.state write |
| freshness gate | `acceptance::state_file` — regenerates this file on the current tree and compares byte-for-byte |

The stamped commit is the tree HEAD the values above were READ FROM. In a landing that is the
commit before the landing commit: this file is written inside the transaction and committed
by it, so the commit carrying these bytes is the stamped commit's child. There is no
timestamp by design — a clock would make every regeneration differ from every other and
leave the freshness gate nothing to compare.

