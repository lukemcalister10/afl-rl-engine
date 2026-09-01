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
| board | `b005096b5e78014425922cae3f28f6c9` | data/expected_boot.json | data/rl_build/rl_app_data.json | agrees |
| store | `415929d3c9d561cc58bef00ae63432b2` | data/expected_boot.json | engine/rl_after/rl_model_data.json | agrees |
| engine_head | `17243c16277842e0a30470cfbdb5b196` | data/expected_boot.json | engine/rl_after/_merged_recover.py | agrees |
| rl_model | `aa1541d8ebb93868907b24daab5dbed1` | data/expected_boot.json | engine/rl_after/rl_model.py | agrees |
| balanced_board_md5 | `c0afa5d869ce0ac490dde4105f6008c9` | data/expected_boot.json | (no in-tree artifact) | not in tree |
| config | `d4f3c3cf8707350dd4c48d7a78ed85c4207cd33d274daf74bb9b99760afadae4` | data/expected_boot.json | config_manifest.manifest_hash | agrees |

| release fact | value | carrier |
|---|---|---|
| contract seal | `3e334b3d5e60705de80d9357520419112882eb4dc8e7c861e20e93bd488f28cd` | data/release_contract.json:contract_sha256 |
| config seal | `d4f3c3cf8707350dd4c48d7a78ed85c4207cd33d274daf74bb9b99760afadae4` | data/release_contract.json:config_sha256 |
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

  > # OPEN ITEMS REGISTER · v888 2026-08-30 · **FINALS WEEK 1 IS LANDED — AS A STORE EDIT, NOT A ROUND. The owner cut the design down and was right to.** Owner word: *"We're literally just updating player averages and game counts. Before round 14 we didn't add games one by one, we just priced based off averages and total season game counts. It really shouldn't be that hard."*

- new-form entries under `docs/register/entries/`: 76
- frozen predecessor `docs/OPEN_ITEMS_REGISTER.md` — md5 `219021ace49ff2750a6576cb9ac8368c` (byte-sealed; `tools/seat/pen.py verify` is its gate)

## LINEAGE TIP

`data/release_lineage.json` — the append-only out-of-round transition register, 21 entries.

| field | value |
|---|---|
| column | bust-exclusion-live-fit-1-9 |
| after round | 24 |
| board moved | `c8c2f2b6f99445484fadaa8c44afe609` → `b005096b5e78014425922cae3f28f6c9` |
| identities moved | board |
| owner ruling id | BUST_EXCLUSION_LIVE_FIT_2026-09-01_if_it_works_it_works |

## GENERATION STAMP

| field | value |
|---|---|
| generated at commit | `b313971d9ad27fbeb6a9ce3f98223bed10f0ce95` |
| tool | `tools/landing/state.py` |
| written by | land lever (step `state`) · land round (step `state`) · python3 -m tools.landing.state write |
| freshness gate | `acceptance::state_file` — regenerates this file on the current tree and compares byte-for-byte |

The stamped commit is the tree HEAD the values above were READ FROM. In a landing that is the
commit before the landing commit: this file is written inside the transaction and committed
by it, so the commit carrying these bytes is the stamped commit's child. There is no
timestamp by design — a clock would make every regeneration differ from every other and
leave the freshness gate nothing to compare.

