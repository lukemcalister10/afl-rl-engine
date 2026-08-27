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
| board | `3167cba643a6b16e5ef5d904d8957fcd` | data/expected_boot.json | data/rl_build/rl_app_data.json | agrees |
| store | `fb640ca0baf92bbb122b1ad7e25c5a88` | data/expected_boot.json | engine/rl_after/rl_model_data.json | agrees |
| engine_head | `d84031cff312818a158855f2dd223cc1` | data/expected_boot.json | engine/rl_after/_merged_recover.py | agrees |
| rl_model | `6fe7c4155866d80e8045bed2d3bf2802` | data/expected_boot.json | engine/rl_after/rl_model.py | agrees |
| balanced_board_md5 | `b7149d5ff7b62ad0916f9a950351b03d` | data/expected_boot.json | (no in-tree artifact) | not in tree |
| config | `29fdfd1e1447a1d2fb33876fe659faa06b13ad19ad4d608a110c20d231f8b86e` | data/expected_boot.json | config_manifest.manifest_hash | agrees |

| release fact | value | carrier |
|---|---|---|
| contract seal | `de37f057eba1665b636f1202ae3319e8293fe141731bc2d49612ddb4194dabaf` | data/release_contract.json:contract_sha256 |
| config seal | `29fdfd1e1447a1d2fb33876fe659faa06b13ad19ad4d608a110c20d231f8b86e` | data/release_contract.json:config_sha256 |
| release version | v2.11-final-rc1-PROVISIONAL | data/release_contract.json:release_version |
| round (as_of_round) | 24 | data/release_contract.json:as_of_round |
| round (as_of_round) | 24 | data/expected_boot.json:as_of_round |
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

  > # OPEN ITEMS REGISTER · v873 2026-08-27 · **RUCK RELIEF IS RULED — the tall cells of the retention surface are THE ONE CARRIER; no second ruck lever enters the build.** Owner word, verbatim (2026-08-27): "Ruck relief yes" — given against this seat's stated recommendation ("confirm the tall cells ARE the ruck relief — one lever, no second ruck mechanism"). Effect: the fade redesign's ruck-relief it

- new-form entries under `docs/register/entries/`: 61
- frozen predecessor `docs/OPEN_ITEMS_REGISTER.md` — md5 `219021ace49ff2750a6576cb9ac8368c` (byte-sealed; `tools/seat/pen.py verify` is its gate)

## LINEAGE TIP

`data/release_lineage.json` — the append-only out-of-round transition register, 15 entries.

| field | value |
|---|---|
| column | order45-arm2-net-24-9 |
| after round | 24 |
| board moved | `82fcd8bb1e552b927299b5702122e321` → `3167cba643a6b16e5ef5d904d8957fcd` |
| identities moved | board |
| owner ruling id | ARM2_REBAKE_ADOPT_2026-08-25_yes_adopt_the_new_model, SAFETY_NET_SCALED_2026-08-25_scaled_on_the_safety_net, MATURE_AGERS_EXCLUDED_2026-08-25_exclude_mature_agers |

## GENERATION STAMP

| field | value |
|---|---|
| generated at commit | `23c6a41902e7b598324caf8e5578b0f3cda29522` |
| tool | `tools/landing/state.py` |
| written by | land lever (step `state`) · land round (step `state`) · python3 -m tools.landing.state write |
| freshness gate | `acceptance::state_file` — regenerates this file on the current tree and compares byte-for-byte |

The stamped commit is the tree HEAD the values above were READ FROM. In a landing that is the
commit before the landing commit: this file is written inside the transaction and committed
by it, so the commit carrying these bytes is the stamped commit's child. There is no
timestamp by design — a clock would make every regeneration differ from every other and
leave the freshness gate nothing to compare.

