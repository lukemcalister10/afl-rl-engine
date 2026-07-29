# ITEM 262 — HAND-BACK

What landed, what did not, and the three items the owner asked to have carried back.

---

## WHAT LANDED

**Vocabulary replacement + per-season eligibility + the R2-4 note rewrite**, at the stage-1 baked
v0surf signature. Per owner ruling R3-1 the 62 position-field edits were **deferred** to the
re-derivation job.

| | before | after |
|---|---|---|
| store | `e3aaba77` | `5d6e56d0` |
| board | `750446d7` | `3d4e2e50` |
| `rl_model.py` | `eb1e065a` | `293e21d6` |
| `_merged_recover.py` (engine_head) | `444831d5` | `404e8113` |
| `bust_prior_table.json` | `ffb54267` | `5942aa6a` |
| fv source-set tree hash | `6a9a520f…` | `d10aa93e…` |
| `v0surf.pkl` | `5b02f33b` | `4cfc0b99` |
| `release_contract` `contract_sha256` | `826de287…` | `85b027f3…` |

### The proof, re-run at the final head

```
scalar cells compared : 103,146
differences           :       0
VALUE movers          :       0
RANK movers           :       0
per-numeric-field movers across all 804 active rows : NONE
```

The final board is **byte-identical to the stage-1 board** (`3d4e2e50`) even though the store now
carries 11,264 new eligibility keys — the sharpest available evidence that the per-season data moves
nothing. No v0surf halt on the final build, as the owner predicted: eligibility does not enter the
fingerprint.

### Acceptance 1, re-run on the final store

| check | result |
|---|---|
| store rows | 2,651 — **0 added, 0 lost** |
| scoring rows / player-seasons | 1,924 / **11,264** — both re-measured, not inherited |
| seasons carrying eligibility | **11,264 of 11,264 (100%)** |
| season vocabulary | MID 4,295 · SF 2,722 · SD 2,331 · KPF 1,461 · KPD 1,449 · RUCK 880 — **nothing outside the six codes** |
| key overlay demonstrable | Elliott Himmelberg (flagged, unnamed) → blanket, all 7 FWD seasons KPF |
| Himmelberg exception differs from blanket | Harrison: KPF ×6 (2016–21), **SD ×5 (2022–26)**. Blanket would have given KPD — it gives SD |
| bust-default rows | **0**, as ruled vacuous at Q9 |
| non-position store fields vs pre-262 | **NONE differ** |
| season `year`/`avg`/`games` moved | **0** |

### Acceptance 2, non-vacuously

Old-vocabulary sweep, identical command both sides: **0 hits on the branch store, 6,261 on main's
store.** (My token list includes `RUC`, which is why this is higher than the seam's 4,386 — same
conclusion.) Exempt and enumerated: prose notes describing history (7 fields across 4 files),
hash-named frozen snapshots (9 glob patterns — renaming them would falsify the filename hash,
hazard 1), archives and the register, and **the UI pair per R3-2**.

### Sibling re-pins, both axes

Stamped: `expected_boot.json` (`store`, `board`, `rl_model`, `engine_head`, `fv`, `bust_prior`,
`v0surf`) · `release_contract.json` (`identities` unchanged — they are the *released* side;
`held_candidates` board/engine_head/rl_model candidates re-stamped, **new `store` and `fv`
declarations** since both previously agreed with the release; `contract_sha256` re-stamped) ·
`season_state.json` `source_store_md5` (re-derived — every derived value unchanged) ·
`rl_app_data.json.srcmd5`.

`bust_prior` was named by neither the directive nor the seam audit. Guard 5 caught it. It is a
**sixth** pinned identity and future vocabulary work should expect it.

---

## THE THREE CARRIED ITEMS

### 1. The 16 sidecar trades (Q2 lane) — NOT APPLIED, and they collide with R3-2

The lane is: edit `docs/inputs/AFFL_Player_Locations.csv` → run `ui/tools/ingest_inputs.py` → it
rewrites `ui/data/ownership.js`. There is **no separate "edit command"**; the sidecar itself carries
`DO NOT hand-edit`.

The output lives in `ui/`. **R3-2 says touch none of the UI.** So the 16 trades cannot be applied in
this landing without breaching R3-2, and they are not applied.

Confirmed still carrying the old clubs in the CSV: Gulbin (Sydney, sheet says West Coast), Mannagh
(West Coast → Sydney), McCartin, Neale, Langdon and the rest of the 16.

**Recommendation:** they go as their own small change. They are presentation-only — ownership affects
no player's value — so they cost an edit and a reload, never an engine run. That is the whole point of
the #232 lane and there is no reason to bundle them with a board-moving landing.

### 2. Is the store's `affl_team` legacy? — **Superseded as the source of truth, but not dead, and retiring it is an owner act**

Traced every live reader. `affl_team` appears **nowhere in the valuation path** — nothing in `ev()` or
any value computation reads it.

It is **not** unread by the engine, though, and the distinction matters:

- `engine/rl_after/ingestion/round_movers.py:279` —
  `affl_by_key = {r.get('key'): r.get('affl_team') for r in store_rows …}`. This copies the store's
  **current** `affl_team` into the movers bundle at bake time. `ui/app/movers.js:29-32` documents the
  consequence: the baked value has no round dimension, so it was never "his club as at that round".
- `engine/rl_after/rl_export.py:787` emits an `affl_team` column on the board (literal `None` for
  phantom pick rows).
- UI presentation reads it as the fallback: `ui/app/ownership.js`, `movers.js`, `format.js`,
  `board.js`, `config.js`.

The design, from `ui/app/ownership.js:9-11`: **the sidecar overrides, the store falls back.** A player
the sheet names takes the sidecar's club; a player it does not name keeps the store's `affl_team`. So
the sidecar is deliberately allowed to be partial, and the store field is still load-bearing for
everyone the sheet omits.

That same file states the disposition explicitly: *"nothing has to be deleted from the store —
**retiring that field is an owner act**."*

So: **legacy as an *authoring* surface** — never edit it to reflect a trade again — but still live as
a *fallback*, and still consumed by the movers bake. Dropping it needs the sidecar to cover all 804
**and** `round_movers.py:279` repointed at the sidecar, and that call is the owner's.

*(An earlier draft of this answer said no engine site reads it. That was wrong — `round_movers.py:279`
does. The valuation-path claim stands; the blanket one did not.)*

### 3. Q3 review lists

Full rows are in `OPEN_QUESTIONS_ROUND2.md` §R2-3 in this directory. Summary: **16 rows**, not the 13
first reported — the GFWD count was 7, not 4 (my earlier figure was the GFWD-drafted-*and*-GFWD-present
subset only). **None of the 16 appear in the Q5/Q6 ruling table, so zero were resolved by it.** All 16
took DEF → SD under the Q3 ruling.

- **9 key-flagged, KDEF-drafted:** Keough (0 seasons), Plowman (11), Johnson (3), Shaw (4), Stratton
  (11), Grimes (15), Silvagni (8), White (8), Delaney (6). Eight of the nine are `KDEF` drafted **and**
  present, yet their future leg already resolved to general defender through the engine's pre-existing
  alias — the rename only makes that visible. Grimes (15 seasons) and Stratton (11) are the largest
  careers affected.
- **7 GFWD-drafted:** Hotton (0), Winder (0), Hind (6), Spina (0), Crozier (12), Newman (2), Jetta
  (13). Four are `GFWD` present with a `DEF` future — a forward whose future leg is a defender.

---

## R3-4 — the ingestion check

**The next round apply will not false-flag.** Full working in `R3_4_INGESTION_CHECK.md`. In short: the
writer (`round_apply.py:184-186`) updates an existing season row **in place**, so `pos` survives; only
a brand-new row gets the bare 3-key dict. The guard compares live against staged, both from the same
store through the same path, so the shapes are symmetric. Simulated apply flags
`changed_years - {2026}` = empty. `dry_run_proof.py --year 2026` passes byte-for-byte on the landed
store.

The real exposure is a **data hole, not a false flag**: of the 1,924 players with scoring history, 653
already hold a 2026 row (all 653 carrying `pos`) and **1,271 do not** — each of those, on first
appearance, lands a season row with no eligibility. Nothing reads `pos` yet, so no guard would notice.
Assigned to the re-derivation directive, with the note that the fix must reach **both**
`round_apply.py:182` and the independent `merged_entry` construction in `staged_apply.py:178-185` /
`score_ingestor.py:224-228` — two writers of the same row.

---

## WHAT DID NOT LAND, DELIBERATELY

- **The 62 position-field edits** (58 sheet + 4 R2-1) — deferred to the re-derivation job per R3-1,
  which applies them as its first act with every mover attributed there. The stage-2
  write-then-revert is kept in branch history as the record.
- **The UI** — untouched per R3-2. The frozen bundles and the source that reads them stay whole under
  the #217 hold and migrate together in the adoption commit. `ui/data/board_view_working.js` is still
  stamped `board_md5 8a38cca4 / store_md5 e3aaba77`, the released identities, which is correct.
- **The 16 trades** — see above.
- **`club_curve_provenance`** — pre-existing red, out of scope, untouched.
