# Diff — the three `rl_model_data.json` lookalikes

Read-only diagnostic. Nothing in the engine or the data files was modified.
Location: `engine/rl_after/`. Repo commit at time of run: `389ac397712e623f927259de930ce266bec51afd`.

---

## WHAT I SAW

### 1. md5 + size

| file | md5 (full) | md5[:8] | size (bytes) |
|---|---|---|---|
| `rl_model_data.json`          | `644d1254db169dbc2824766ac3cf20f9` | **`644d1254`** | 1,201,231 |
| `rl_model_data.json.pre_stage0` | `644d1254db169dbc2824766ac3cf20f9` | **`644d1254`** | 1,201,231 |
| `rl_model_data.json.stage0`   | `91a3de6bbf07cef9a3ade4db2bb63d2c` | `91a3de6b`   | 1,225,496 |

- `644d1254` is **`rl_model_data.json` AND `.pre_stage0`** — they are **byte-identical** (`content-equal == True`).
- `.stage0` is the odd one out (different md5, +24,265 bytes).

### 2. Top-level structure

All three are the **same shape**: a JSON **list of player records** (dicts), **2,656 records** each. Not a dict keyed by slug.

Per-player field names (union across all records is identical, 23 keys, in all three files):

```
player, pick, year, type, pos, key, games, scoring,
_has26, _retired, _by, _cat, _draft, _club, _pickless, _fut, _bd,
_pos_now, _double_count, _force_active, _last_listed, _phantom, _pvc_exclude
```

The core scalar fields (`player, pick, year, type, pos, key, games, scoring, _has26, _retired, _by, _cat, _draft, _club, _pickless, _bd`) appear on every record. `scoring` is a **list of per-season objects** `{year, avg, games}` — the year-by-year scoring history lives inline in each player record.

### 3. Marcus Bontempelli (`marcus-bontempelli`)

Present in all three. Scoring history is present in every copy — a **13-season** list (2014→2026) of `{year, avg, games}`:

```
2014 avg 78.6  g16 | 2015 103.8 g21 | 2016 108.7 g26 | 2017 105.1 g22
2018 104.0 g19 | 2019 113.4 g23 | 2020 113.4 g18 | 2021 119.5 g26
2022 116.7 g22 | 2023 129.7 g23 | 2024 123.8 g24 | 2025 130.6 g18 | 2026 119.0 g14
```

`rl_model_data.json` and `.pre_stage0`: identical record. `_fut = [["MID",90.0],["GFWD",10.0]]`, no `_pos_now`.

`.stage0`: **same** identity/games/scoring, but two deltas:
- `_fut` → `[]` (emptied)
- `_pos_now: "MID"` added

Everything else (`games:271`, `_by:1995`, `_bd:"1995-11-24"`, `_club`, `pick:4`, the full 13-season `scoring`) is unchanged.

### 4. Three-way diff

`rl_model_data.json` vs `.pre_stage0`: **no diff** (byte-identical). So the diff is really two-way: `main == pre_stage0` vs `stage0`.

Same 2,656 keys on both sides — **no players added or removed**. Only two fields move, and only in two ways:

| field | absent→present in stage0 | value changed in stage0 |
|---|---|---|
| `_fut`     | 1,906 players (added as `[]`) | 715 players (existing value → `[]`) |
| `_pos_now` | 675 players (added) | 34 players (value reassigned) |

2,621 of 2,656 players carry at least one stage0 change.

**What "stage0" does — two operations:**

1. **Wipes `_fut` on essentially everyone.** After stage0, `_fut` is present on all 2,656 records and empty `[]` on **2,655** of them. The pre-stage0 future-position projections (non-empty `_fut` existed on 716 players) are cleared. The **sole exception is `ed-langdon`**, who keeps `_fut = [["GDEF",70.0],["MID",30.0]]` in stage0.

2. **Adds/normalizes `_pos_now` (current position).** Coverage goes 131 → 806 records. For the 675 newly added it equals the player's `pos`. For 34 it is a deliberate **reassignment** away from `pos`, almost all young draftees moved into `MID` (e.g. `samuel-grlj` GDEF→MID, `sam-lalor` GFWD→MID, `jagga-smith` GFWD→MID, `levi-ashcroft` GFWD→MID, `finn-o-sullivan` GDEF→MID; one the other way, `jack-ison` MID→GFWD).

The +24 KB size delta is exactly these added `_fut`/`_pos_now` keys.

### 5. What `rl_model.py` reads

Which of the three it opens — quoted:

- Line 4: `data=json.load(open('rl_model_data.json')); P=json.load(open('params.json')); PMD=json.load(open('rl_passmark.json'))`

It opens **`rl_model_data.json`** and nothing else of the three. It never references `.pre_stage0` or `.stage0` (grep for `rl_model_data` returns only line 4). Because `rl_model_data.json` is currently byte-identical to `.pre_stage0`, the engine is effectively running on the **pre_stage0** data (this matches the bootstrap banner: "rl_model_data.json = reconciled pre_stage0 (authoritative)").

Does it read any other file to build a player? Every player attribute — scoring history, birthdays (`_by`/`_bd`), pedigree (`type`/`pick`/`_draft`/`_cat`), club, position — is read out of the single in-memory `data` list. Confirmed in `rl_model.py` (`for _r in _p['scoring']`, `by(p)` from `_by`) and `pgrid.py` (which is handed `data` in memory via `pgrid.build(data, GRP, debut)` at line 733 and **opens no files of its own**). There is **no** separate scoring / birthday / pedigree / injury file.

Other files it opens (not for building a player — model/params/passmark artifacts):

- Line 4: `params.json`, `rl_passmark.json`
- Line 360 (lazy, inside `_v4_init`): `peak_model_v4.pkl` — `_pk.load(open('peak_model_v4.pkl','rb'))['model']`
- Line 361: `bust_prior_table.json`
- Line 362: `pvc_snapshot.json` — "snapshot of train-time PVC"

Imports `pgrid` (no file reads) and `unidecode` (vendored, offline).

**Definitive list of files `rl_model.py` reads:**

1. `rl_model_data.json` — all player data (the only data source for players)
2. `params.json`
3. `rl_passmark.json`
4. `peak_model_v4.pkl` — lazy, `_v4_init()`
5. `bust_prior_table.json` — lazy
6. `pvc_snapshot.json` — lazy

---

## CONCLUSIONS (separate from what I saw)

1. **`rl_model_data.json` and `.pre_stage0` are the same file** (md5 `644d1254`, byte-for-byte). `.pre_stage0` is a backup snapshot of the pre-stage0 state, and the live file was reconciled back to exactly it — consistent with the bootstrap declaring pre_stage0 authoritative.
2. **`.stage0` is a superset transform, not a different dataset.** Same 2,656 players, same identities, same `games`, same scoring histories. It differs only by (a) blanking `_fut` everywhere except `ed-langdon`, and (b) filling in `_pos_now` (current position), reassigning 34 young players — mostly forwards/defenders promoted to `MID`.
3. **stage0 is a position-normalization / future-projection-reset pass.** It strips the manual `_fut` future-position weightings and replaces per-player position handling with a normalized `_pos_now`. The one retained `_fut` (`ed-langdon`) looks like a deliberate carve-out.
4. **The engine is not running stage0.** `rl_model.py` reads `rl_model_data.json`, which currently equals `.pre_stage0`. So live output reflects the pre-stage0 world (with non-empty `_fut` projections intact and `_pos_now` sparse). Switching the engine to the stage0 data would remove `_fut` from the picture for all but `ed-langdon` and broaden `_pos_now` coverage.
5. **Scoring history is never a concern across these three** — Bontempelli (and by construction every player) carries an identical inline `scoring` list in all three files; stage0 touches only `_fut`/`_pos_now`.
6. **No hidden inputs.** A player is built entirely from `rl_model_data.json`; the other five files `rl_model.py` opens are model/params/passmark artifacts, not player sources.
