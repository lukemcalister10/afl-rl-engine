# PINS — round 22 landing, 2026-08-10

Every identity that moved, and every identity that deliberately did not. All in one transaction
(`txn_catchup_r22`, status COMMITTED, `failure: null`, 17 of 17 targets).

Baseline for the "before" column is `origin/main` at `1c34712`.

## The single source and the board

| artifact | before | after |
|---|---|---|
| `engine/rl_after/rl_model_data.json` (the store) | `37ced3ce45914e6feb00d27e26922e9a` | `0dd6b4a01e16dabf8d3a388d8f8ac1f2` |
| `data/rl_build/rl_app_data.json` (the board) | `113b36f898a32363c49c2a62fb809f4b` | `6e724cca2bb2fb118ff7ad6ed1f8a4b6` |
| `data/rl_build/rl_app_data.json.srcmd5` (the SSI stamp) | `6d80c58cd747b8369b1cf158b4ee7408` | `ded7e53725d69aa119c37f596aa26ecc` |

## Manifest / contract / state

| artifact | before | after |
|---|---|---|
| `data/expected_boot.json` | `dca47923b7bd2ff0bc5d3f63c89f93b4` | `2317e692f9baf6ed0927c53dcde1a845` |
| `data/release_contract.json` | `773416a6e6a20bb07d9b9736257c564a` | `887bed3f3130bfdb1dae76415194e260` |
| `data/season_state.json` | `57945b8903293fdecc34d80bc8ba87f3` | `f30ff89d42c4d77d0c9fbf8d21fffb18` |

Manifest contents after the landing:

```
store               0dd6b4a01e16dabf8d3a388d8f8ac1f2
board               6e724cca2bb2fb118ff7ad6ed1f8a4b6
balanced_board_md5  b4cc0b2b7e4fb0552e9457f2d249cf52
as_of_round         22
engine_head         8f0e3eb1b29fee6b2defa0a5cfd7ebec   (UNMOVED — no engine change in this act)
rl_model            33f940735281a07e3b6ca19f31bf2ea6   (UNMOVED)
fv                  d920557ef21d0eec6434853b07869dd4c0b98f64e99e79ecbb8ee54c704ecf4a  (UNMOVED)
config              cef06fd6250be86804f7d4432fdef8969070f9d9fc938f3e3473547c5b4b4739  (UNMOVED)
register            652d83e87780e415a01a2de6d8b3cc57   (UNMOVED)
q97m                cfdc73216c099e5e8f1fda3968f31c00   (UNMOVED — frozen)
v0surf              d594dc034e86935b370c49b240a18370   (UNMOVED — no refit in this act)
release_version     v2.11-final-rc1-PROVISIONAL        (UNMOVED)
```

The five model pins staying still is the point: this act adds data and nothing else. No dial, no
curve, no surface, no engine maths.

## Weekly histories and the ledger

| artifact | before | after |
|---|---|---|
| `engine/rl_after/ingestion/applied_rounds_ledger.json` | `59f2f0f22ad5cee9dcce5b228cea1f87` (2,677) | `4d6ec6d3e42d6338bbd8efaf2acc8bee` (3,086 = +409) |
| `engine/rl_after/ingestion/value_history.json` | `0cf68f282a201a4e1ea5ed1763b21a74` | `32ef519903474c43194de2feddea497c` |
| `engine/rl_after/ingestion/rank_history.json` | `1bcc0a0a6ad937dfe098a21eb5ca5d4a` | `a40abe2682198666229a6015710bbb88` |
| `engine/rl_after/ingestion/pos_rank_history.json` | `af817897978c6b679a537282b17a0bd2` | `11c278afe342d402b53c747dfd007404` |
| `engine/rl_after/ingestion/sibling_repin_state.json` | `3ba6bdc1c53bcadb8474f20aab246791` | `1e0d8022551604958b1eb52a6a25161a` |
| `engine/rl_after/ingestion/finalization_state.json` | `f42c32ad8104470306c54543d0dd1826` | `47f326576b3c6cae90d54cc38b9104dc` |

Histories now carry rounds `[14, 15, 16, 17, 18, 19, 20, 21, 22]`.

## UI bundles (derived, regenerated in the finalization step)

| artifact | before | after |
|---|---|---|
| `ui/data/board_view_public.js` | `79a11f14d0209b252f9541d5b3eea757` | `8e769f97a81790dbb52ca44c557cd847` |
| `ui/data/board_view_working.js` | `a7536adc53609d2ab875e7946614a982` | `15e4a33b06e6bcf0db89fffa3aa2d1b6` |
| `ui/data/club_valuation.js` | `eca8faee605d17349d9e157a91a55af0` | `a121a24c1ec5dbd5cfc1915b6ab81950` |
| `ui/data/movers.js` | `5e0e57090c2da9dab8e90374b6568f6f` | `b4b58846344698e8c616402b59db9777` |
| `ui/data/ownership.js` | `677078f7fd3ccf101f3d8b6cb62b67f1` | `494aeeef31fa2407ecd840068d660ae1` |

`ui/data/movers_transition.js` is **unchanged** — no out-of-round board was registered between round
21 and round 22, so the transition record has nothing new to carry. Round 22 compares straight back
to round 21, which is exactly the apples-for-apples basis the owner asked for.

## Inputs

| artifact | md5 |
|---|---|
| `scores/R22.csv` (new; the owner's couriered file, byte-unmodified) | `82b456d5675c18b137180416b82432fc` |
| `engine/rl_after/ingestion/catchup_identity_overrides.json` (owner's Bailey ruling recorded) | `0c872df734d82e282c9ef607104d619b` → `f213eed069abb4b338f7a6f7eeb3332d` |

## Sibling / balanced board

| | before | after |
|---|---|---|
| balanced board | `123deccb0838c7370ce614d7f4310b01` | `b4cc0b2b7e4fb0552e9457f2d249cf52` |
| reference vector fixture | `reference_vector_123deccb.json` | `reference_vector_b4cc0b2b.json` (new) |
| forward vector fixture | `forward_vector_113b36f8.json` | `forward_vector_6e724cca.json` (new) |
| forward-lens oracle | `test_forward_lens_113b36f8.py` | `test_forward_lens_6e724cca.py` (new) |
| active | 804 | 804 |
| board total (Σv) | 759,722 | 761,583 |
| Sheezel (pick-1-relative top of board) | 12,124 | 11,925 |
| PICK 1 numéraire | 3,000 | **3,000 (unmoved)** |

## Independent re-derivation

The board was rebuilt from the landed store in a clean private workspace, off the transaction, under
the canonical recipe (gate config mode, `PYTHONHASHSEED=0`, single-thread BLAS, pinned numpy 2.4.4 +
OpenBLAS `05c9f9eb`). It reproduced `6e724cca2bb2fb118ff7ad6ed1f8a4b6` **byte-exact**. See
`gate_board_rebuild_md5.txt` and `gate_export.txt`.
