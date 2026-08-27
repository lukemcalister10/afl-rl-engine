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
| board | `530a4053622c29092274fab0aa1fee7f` | data/expected_boot.json | data/rl_build/rl_app_data.json | agrees |
| store | `fb640ca0baf92bbb122b1ad7e25c5a88` | data/expected_boot.json | engine/rl_after/rl_model_data.json | agrees |
| engine_head | `a5550b678f05e5c8b80cd3952d1b4ce5` | data/expected_boot.json | engine/rl_after/_merged_recover.py | agrees |
| rl_model | `6fe7c4155866d80e8045bed2d3bf2802` | data/expected_boot.json | engine/rl_after/rl_model.py | agrees |
| balanced_board_md5 | `c06ff1e897f850bbecf3330e9050c365` | data/expected_boot.json | (no in-tree artifact) | not in tree |
| config | `f233d1604975cdbda18bde0d31e253c8254bddc97fb7f1be6ac0412f57e06979` | data/expected_boot.json | config_manifest.manifest_hash | agrees |

| release fact | value | carrier |
|---|---|---|
| contract seal | `7cd796dee6ceb7716d70619b085e87cfe1c365cc8ef1279e1c9f197859972451` | data/release_contract.json:contract_sha256 |
| config seal | `f233d1604975cdbda18bde0d31e253c8254bddc97fb7f1be6ac0412f57e06979` | data/release_contract.json:config_sha256 |
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

  > # OPEN ITEMS REGISTER · v880 2026-08-27 · **THE COMBINED BUILD IS LANDED (main d7a7726, take 11 of the transaction): the board of record moved ONCE, 3167cba6 → 530a4053, and every step's postcondition held.** Owner authority: the banked mechanism words (v873/v874/v875) + the no-arb approval (v877) + the standing land-if-possible directive, executed while the owner sleeps per his word; the final ra

- new-form entries under `docs/register/entries/`: 68
- frozen predecessor `docs/OPEN_ITEMS_REGISTER.md` — md5 `219021ace49ff2750a6576cb9ac8368c` (byte-sealed; `tools/seat/pen.py verify` is its gate)

## LINEAGE TIP

`data/release_lineage.json` — the append-only out-of-round transition register, 16 entries.

| field | value |
|---|---|
| column | combined-build-46-47-48-sll5g |
| after round | 24 |
| board moved | `3167cba643a6b16e5ef5d904d8957fcd` → `530a4053622c29092274fab0aa1fee7f` |
| identities moved | board |
| owner ruling id | MECHANISM_AGREED_2026-08-27_agree_on_your_mechanism, SLL5G_LOCKED_2026-08-27_lock_in_ll5g_then, DEPTH3_CAP_A_2026-08-27_a_for_depth_3_cap, SAT_SEASON_LT2_2026-08-27_lt2_is_fine_for_sat_season, EASING… |

## GENERATION STAMP

| field | value |
|---|---|
| generated at commit | `c559d6b4c3464849f97e0f94b98242cb2078ab38` |
| tool | `tools/landing/state.py` |
| written by | land lever (step `state`) · land round (step `state`) · python3 -m tools.landing.state write |
| freshness gate | `acceptance::state_file` — regenerates this file on the current tree and compares byte-for-byte |

The stamped commit is the tree HEAD the values above were READ FROM. In a landing that is the
commit before the landing commit: this file is written inside the transaction and committed
by it, so the commit carrying these bytes is the stamped commit's child. There is no
timestamp by design — a clock would make every regeneration differ from every other and
leave the freshness gate nothing to compare.

