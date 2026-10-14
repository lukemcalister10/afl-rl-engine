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
| board | `e40c37ccc543e7f2bcca16c996b53dbb` | data/expected_boot.json | data/rl_build/rl_app_data.json | agrees |
| store | `b0eeaf4b9f766e6618081dce8fc328e3` | data/expected_boot.json | engine/rl_after/rl_model_data.json | agrees |
| engine_head | `b6427045918d8e9a5eb208d8a077d78e` | data/expected_boot.json | engine/rl_after/_merged_recover.py | DRIFTED |
| rl_model | `ad48eb299b01639b62d397c4c0016dd4` | data/expected_boot.json | engine/rl_after/rl_model.py | agrees |
| balanced_board_md5 | `f4126b629ea4d4135b4c0ad0f1b29508` | data/expected_boot.json | (no in-tree artifact) | not in tree |
| register | `652d83e87780e415a01a2de6d8b3cc57` | data/expected_boot.json | (no in-tree artifact) | not in tree |
| config | `d4f3c3cf8707350dd4c48d7a78ed85c4207cd33d274daf74bb9b99760afadae4` | data/expected_boot.json | config_manifest.manifest_hash | agrees |

| release fact | value | carrier |
|---|---|---|
| contract seal | `a069562b941f9fc04c5d1a6f5d1e7ff427a5c8b7dc48922510ffafdff0b157d4` | data/release_contract.json:contract_sha256 |
| config seal | `d4f3c3cf8707350dd4c48d7a78ed85c4207cd33d274daf74bb9b99760afadae4` | data/release_contract.json:config_sha256 |
| release version | v2.11-final-rc1-PROVISIONAL | data/release_contract.json:release_version |
| round (as_of_round) | 24 | data/release_contract.json:as_of_round |
| round (as_of_round) | 24 | data/expected_boot.json:as_of_round |
| declared held checks | 0 | data/release_contract.json:held_checks |

BOOT vs CONTRACT, computed here rather than assumed: board agree · store agree · engine_head agree · balanced agree · round agree.

## THE LAWS

The single governing document, and its own lint's verdict — a pointer without a verdict is a
gate claimed by name (process law P5).

- **docs/RULEBOOK.md** — md5 `444f3f6c72d2aa5ff574fcb278643241`
- header: # THE RULEBOOK — v3 · 2026-08-20 · OWNER-SIGNED (in chat, 2026-07-22; amended 2026-07-28, 2026-08-20)
- `tools/rulebook_lint.py` verdict: **PASS** — rulebook_lint: 0 FAIL

## THE RECORD

- **docs/register/LATEST.md**, line 1, quoted:

  > # OPEN ITEMS REGISTER · v888 2026-08-30 · **FINALS WEEK 1 IS LANDED — AS A STORE EDIT, NOT A ROUND. The owner cut the design down and was right to.** Owner word: *"We're literally just updating player averages and game counts. Before round 14 we didn't add games one by one, we just priced based off averages and total season game counts. It really shouldn't be that hard."*

- new-form entries under `docs/register/entries/`: 76
- frozen predecessor `docs/OPEN_ITEMS_REGISTER.md` — md5 `219021ace49ff2750a6576cb9ac8368c` (byte-sealed; `tools/seat/pen.py verify` is its gate)

## LINEAGE TIP

`data/release_lineage.json` — the append-only out-of-round transition register, 30 entries.

| field | value |
|---|---|
| column | chain-hardwired-single-reader-14-10 |
| after round | 24 |
| board moved | `848874f1a79a230a453ddcecf4a7c843` → `e40c37ccc543e7f2bcca16c996b53dbb` |
| identities moved | board |
| owner ruling id | D3_ADOPTED_2026-10-13, PHASE1_HYGIENE_2026-10-14 |

## GENERATION STAMP

| field | value |
|---|---|
| generated at commit | `3911fdfc4771be15d4f831238d8020f6b8140e74` |
| tool | `tools/landing/state.py` |
| written by | land lever (step `state`) · land round (step `state`) · python3 -m tools.landing.state write |
| freshness gate | `acceptance::state_file` — regenerates this file on the current tree and compares byte-for-byte |

The stamped commit is the tree HEAD the values above were READ FROM. In a landing that is the
commit before the landing commit: this file is written inside the transaction and committed
by it, so the commit carrying these bytes is the stamped commit's child. There is no
timestamp by design — a clock would make every regeneration differ from every other and
leave the freshness gate nothing to compare.

