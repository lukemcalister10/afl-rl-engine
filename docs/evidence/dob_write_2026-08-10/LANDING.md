# THE LANDING — birthdates written, v0surf re-cut, board moved

Owner's two words on issue #334, both quoted verbatim:

- comment **5235574982**: *"Ruory Kirkby - 4/2/86. Tim Looby - 2/9/87. Write the birthdates."*
- comment **5235816134**: *"Authorise the refit."*

The first is the write. The second came after this seat HALTED on the v0surf frozen-signature guard and
reported the measured board impact; it authorises the surface re-cut that carries the birthdates onto
the board. `README.md` is the write and the halt; `board_impact_diagnostic.md` is the measurement that
the owner ruled on; this page is what landed.

---

## 1 · IDENTITIES — before and after

| artifact | before | after |
|---|---|---|
| store `engine/rl_after/rl_model_data.json` | `0dd6b4a01e16dabf8d3a388d8f8ac1f2` | **`d9a24282357cf3083b1640466e3ecd83`** |
| **v0surf** `data/v0surf.pkl` | `d594dc034e86935b370c49b240a18370` | **`5a03c9ea3e9a32e6cc6e1ffec5293685`** |
| v0surf shipped **config signature** | `af556bdc…` / `edb15f7a…` (the frozen pair) | **`6ef67f07db98258786189a6316ce24f9`** (+ `41af7326…` pre-swap) |
| board `data/rl_build/rl_app_data.json` | `6e724cca2bb2fb118ff7ad6ed1f8a4b6` | **`a672ed3a6a1426a262d932f844e8f87b`** |
| balanced board (sibling) | `b4cc0b2b7e4fb0552e9457f2d249cf52` | **`a970c19cd56ea184e9ca5eb02211d21b`** |
| release contract seal | `bf435d58aee2cd5a994a948bc3f3d4859fce1397ac21a80fb7ad0a3860188eaf` | **`9fb5e56c6442521635424c49a8be8e5a2f7548ca8bc4b30a4c9e657184040b7a`** |

**UNMOVED, and that is the point:** `engine_head` `8f0e3eb1`, `rl_model` `33f94073`, `fv` `d920557e`,
`config` `cef06fd6`, `register` `652d83e8`, `band` `34faa865`, `q97m` `cfdc7321`, `peak_model`,
`pvc_snapshot`, `bust_prior`, `release_version`, `as_of_round` 22. No model, no curve law, no dial, no
teaching, no config value. The only fitted artifact that moved is the one the owner authorised.

## 2 · THE BOARD MOVE — 6 of 804, every one ±1

| player | before | after |
|---|---|---|
| William McCabe | 624 | **625** |
| Mitchell Marsh | 505 | **506** |
| Maxwell King | 155 | **156** |
| Luke Urquhart | 142 | **143** |
| Isaac Cumming | 40 | **41** |
| Jevan Phillipou | 274 | **273** |

Board total **761,583 → 761,587** (+4, +0.0005%). Max absolute move **1**; median **1**. Backward board
**0 movers**. Sheezel **11,925 unmoved**. **PICK 1 numéraire 3000, unmoved.**

Every figure above was predicted by the pre-authorisation diagnostic and reproduced exactly by the
gated build. Nothing moved that was not forecast.

**Why the board moves at all:** `_v0surf_sig` (`_merged_recover.py:1324`) hashes every historical
national draftee's DRAFT AGE, which reads `_by`. With no birthdate the engine fell back to
`draft_year - 18`, i.e. draft age exactly 18. Fourteen of the 302 are mature-age draftees taken inside
picks 1-64 whose real draft ages are 19-22, so they cross the V0 fit's 18/19 split — out of the young
pick curve `c18`, into the mature surfaces `surfN`/`surfR`. Both change shape slightly; after the
numéraire re-base it lands as ±1 rounding on six current players. The 14 are named in `README.md` §4.

## 3 · GATES — all green

| gate | result |
|---|---|
| `rl_export.py` — F1 export↔engine parity | **PASS**, exit 0, board `a672ed3a` |
| PARITY GATE | **PASS** — all 804 active board values == engine gated `ev()`, matched by key, eps 0 |
| NUMÉRAIRE GUARD | **PASS** — shipped pick-1 = 3000 |
| `s4_matrix_M1v7.py` — F2 book↔board parity | **PASS**, exit 0 |
| `one_source_selftest.py` | **PASS**, exit 0 — **142 PASS / 0 FAIL / 0 STALE** |
| `guard_correction_canary.py` (Guard 4) | **PASS**, exit 0 |
| Guards 1/2/3/5 (in the self-test) | **PASS** |
| `config_manifest.py check` · `release_contract.py check` · `ruling_config_check.py` | **PASS** |
| `release_state_failclosed_test.py` · `invariant_proof.py` | **PASS** |
| `sibling_repin.py check` | **PASS** |
| `generate_movers_transition.py --check` (drift guard) | **PASS** |
| UI: extract_seam · release_seam · counting_rule · club_curve_provenance · club_valuation_current · club_totals_parity | **PASS** |
| UI: ownership_single_source · ownership_store_apply · ownership_sidecar · movers · adoption_gate | **PASS** |
| ingestion: `test_catchup_preflight.py` · `test_movers_transition.py` | **PASS** |

**One pre-existing failure, not caused by this act and not fixed by it:**
`engine/rl_after/ingestion/test_weekly_updater.py` fails with
`R14 fixture verification FAILED — expected_boot config pin != scratch model_config vars hash (config
drift)`. **Verified pre-existing:** it fails identically on an unmodified checkout of `main` at
`c133a63`, with this act's changes nowhere in the tree. It concerns the *config* pin, which this act
does not touch. Reported, deliberately not repaired — repairing a config-pin drift is a config act and
is outside this act's scope guard.

## 4 · THE BOARD MOVED OUTSIDE A ROUND — column + transition

The standing owner rule (`out_of_round_column.py`, owner word 2026-07-28): *"whenever the board moves
OUTSIDE a round, write a column at that point."* This act moves the board at round 22 with no round
applied, so:

- **History column `dob-courier-10-8`** ("10/8 DOB courier + v0surf re-cut", `after_round` 22, board
  `a672ed3a`) written into all three histories — `value_history.json`, `rank_history.json`,
  `pos_rank_history.json` — 804 players each, 0 already present, no conflict. Script:
  `register_column.py`. It reads a finished board and writes JSON; it computes no value.
- **Transition record appended** to `data/release_lineage.json`'s append-only
  `release_transition_register` (entry 5). Script: `append_transition.py`, which asserts the file
  round-trips at `indent=1` and that no prior entry changed before writing.

**On that record, plainly:** it RECORDS an approval that already exists in the owner's own words — both
are quoted verbatim in the entry and cited to their comments — it does not create one. This is the
shape the register's own law prescribes ("an APPENDED entry is the shape the validator's own law
prescribes for a future out-of-round board move"), and it is what lets the Movers dropdown name the
boundary. A label never blocks a comparison. **The seam should verify the quoted words against the
owner's actual comments.**

## 5 · A REGRESSION CAUGHT ON THE WAY

`sibling_repin.py reconcile` regenerates `ui/data/board_view_working.js` through
`extract_board_view.py`, which does **not** emit the stamp's `release` block. In a weekly round it is
`round_finalize` that re-adds it (`round_movers.inject_release_contract`) right after the refresh. This
act is not a round, so nothing re-added it and the regenerated bundle came out **without
`stamp.release`** — which silently un-anchors the UI's movers lineage (`curApp.balanced_board_md5`
falls through to the board-artifact hash instead of the immutable present-lens anchor `06d8af60`, the
exact three-way confusion #271 A17 closed).

Caught by `ui/tests/movers.test.js`, then repaired by calling the same injector the round lane calls.
The block is back, carrying the immutable anchor `06d8af60` with the new board and store. Recorded here
because the next out-of-round landing will hit it too: **`sibling_repin` outside a round needs
`inject_release_contract` run after it.**

## 6 · TWO TEST EXPECTATIONS BUMPED — both to match a real, intended change

Neither weakens an assertion; both are counts/states that the file's own comments predicted would move.

1. `ui/tests/movers.test.js` — lineage state `"ok"` → `"bridged"`. `ok` is the DIRECT-lineage branch,
   which needs the latest **round report's** terminal board to equal the loaded board. The board moved
   outside a round, so R22's report keeps its frozen terminal board `6e724cca` (a later act never
   rewrites an earlier report's identity, #271 A15/A16) while the app serves `a672ed3a`. The file's own
   note calls `bridged` "the honest state, not a defect". The out-of-round column carries the live
   board, so THE ONE ASSERT still passes — which is why it is `bridged` and not `mismatch`. **Both
   non-vacuity assertions around it are untouched and still pass:** a foreign board still fails closed
   as `mismatch`, and the same bundle loaded at its own terminal identity still reads `ok`.
2. `ui/tests/movers.test.js` — declared out-of-round boundaries `3` → `4`. Exactly the growth the
   adjacent comment predicted ("it grows correctly with the register instead of pinning a number"). The
   durable property — *every* boundary anchored to an owner-approved record — is a separate assertion,
   untouched, and it covers the new entry.

## 7 · CARRIERS RE-PINNED

Store `0dd6b4a0` → `d9a24282`, board `6e724cca` → `a672ed3a`.

| carrier | what moved | by what |
|---|---|---|
| `data/expected_boot.json` | `store`, `board`, `v0surf`, `balanced_board_md5` | this act + refit lane + sibling repin |
| `data/release_contract.json` | `identities.store`, `identities.board`, `balanced_board_md5`, present-lens baseline, re-seal | `release_contract.restamp_dynamic` + sibling repin |
| `data/season_state.json` | `source_store_md5` | this act |
| `data/rl_build/rl_app_data.json` (+ `.srcmd5`) | the board of record and its SSI stamp | gated build |
| `data/v0surf.pkl` | the re-cut frozen surface | `refit_v0surf.py --bake` |
| `data/release_lineage.json` | transition register entry 5 appended | `append_transition.py` |
| `engine/rl_after/ingestion/sibling_repin_state.json` | `source_store_md5` + sibling identity | sibling repin |
| `engine/rl_after/ingestion/{value,rank,pos_rank}_history.json` | out-of-round column | `register_column.py` |
| `ui/data/board_view_working.js` · `board_view_public.js` | stamp identities (+ `stamp.release` re-injected) | sibling repin + injector |
| `ui/data/ownership.js` · `club_valuation.js` | stamp identities, regenerated from the store | `ingest_inputs.py` |
| `ui/data/movers.js` | derived blocks: points, values, model_changes | `rebuild_movers_derived.py` |
| `ui/data/movers_transition.js` | register mirror (5 entries) | `generate_movers_transition.py` |
| fixtures: `reference_vector_a970c19c.json`, `forward_vector_a672ed3a.json`, `test_forward_lens_a672ed3a.py`, `test_fv_provenance.py` | regenerated for the new identities | sibling repin |
| `session_2026-07-18/legf6/v0surf_refit_log.json` | refit provenance appended | refit lane |

**Sealed history, deliberately NOT re-stamped:** `docs/evidence/ingest_r22_2026-08-10/`, the
`txn_catchup_r22` manifest and journal, `movers/movers_R22.json`, `finalization_journal.jsonl`, and
`finalization_state.json`'s round-22 entry. Each records what was true at the round-22 act. A later act
never rewrites an earlier report's identity.

## 8 · ON THE CLEAN-INSTANCE PRECONDITION

`refit_v0surf.py` records `precondition_balanced_board_06d8af60: NOT EVALUATED — unreachable since the
pricing split`, and asks the running job to supply substitute evidence. This job's substitute evidence
is strong and is in `board_impact_diagnostic.md`: a declared refit on this same box against the
**unwritten** store reproduced the shipped board `6e724cca` **byte-exact**. A weather box cannot do
that. The freeze is faithful and this box is not a weather box for this surface.

## 9 · ONE-WRITER NOTE

An earlier attempt at this landing was blocked because a second seat (the G1 repair agent) was building
in the shared `/home/claude` scratch and had placed a non-pinned surface at the shared
`/home/claude/v0surf.pkl` slot, which sits ahead of the checkout's copy in the engine's load
precedence. That seat is now held. Before seeding the slot from this checkout — the canonical pattern
(`session_2026-07-19/envpin/scripts/build_board.sh:20`) — its file was preserved at
`/home/claude/g1_v0surf_experimental_c309168f.pkl.bak`; nothing of theirs was lost. Every shared pinned
input was md5-checked before and after each build and none moved under this job.

## 10 · FILES

Added by the landing: `LANDING.md` (this page), `bake_v0surf.sh`, `register_column.py`,
`append_transition.py`, `landing_attempt/` (the blocked run's logs). The write, the halt, the two owner
overrides, the census and the measurement are in `README.md`, `applied_302.csv`,
`owner_overrides.json`, `census_after.txt` and `board_impact_diagnostic.md`.
