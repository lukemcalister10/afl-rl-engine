# #328 RESUMED — OPTION A. The ruled ladder installed, the closure CONFIRMED, steps 5–7 executed.

Owner's re-closure ruling of 2026-08-05, **OPTION A**, filed at [#328 comment 5192164003](https://github.com/lukemcalister10/afl-rl-engine/issues/328#issuecomment-5192164003).
The corrected-store derived ladder `df766dff` becomes the adopted ruled curve; the reversal condition
re-anchors to it, unchanged in terms. Read `ACT.md` first for steps 1–3 and `REVERSAL_CHECK.md` for the
halt that produced this ruling.

---

## THE BOX WAS RE-CLASSIFIED FIRST. The container had restarted.

`uptime` read **1 min** on this seat's first command after the ruling. N35 stales a classification on
any observed restart, and this resumption contains **two** fit acts, so nothing proceeded until the box
was classified again from scratch: env pins 5/5 · OpenBLAS sha256 byte-exact · `preboot_assert` ·
`bootstrap.sh` rc=0 with Guard 5 on the corrected store · tier-2 stamps · then the fit-path assert.

```
refit_v0surf.py --verify, on the step-3 substrate
  new md5  e4215093693d32929820834cbd8ecb27
  pin      e4215093693d32929820834cbd8ecb27
  VERIFY: refit REPRODUCES the committed pin.              97s
```

**FIT-CLASS, entry 2.** It reproduces the surface this seat itself baked in the previous container,
across a restart — a stronger check than entry 1, and the reason every figure below it is comparable.

---

## 1 · THE RULED LADDER INSTALLED — `df766dff`

Through `install_reclosure_328.py`, the `u8ir65` closure instrument **re-pointed, not rewritten**:
every discipline carried (C.2 field-level by JSON path, the sealed twin moved twice by path, N14/E6
factor coherence, N22/N32 full-md5 identity, the pin-length trap read-and-replaced whole, sealed
history byte-asserted). All-or-nothing, dry-run first.

| | from | to |
|---|---|---|
| curve payload | `01f27f02` | **`df766dff`** (full `df766dff94657940e2a892e91da5a6e2`) |
| pooled head (primitive, sealed twin) | 3060.621 | **3017.9232** — `s` derived 0.994061 at full precision |
| pool_value | 233.3 | **237.2** — this derivation's own pool-wide level |
| curve file md5 | `46525617` | `f1cf148e` (→ `b7389fe4` after step 7) |
| contract_sha256 | `588c463c` | **`ea560e55`** — recomputed by the contract's own writer |
| ladder sum · pick 64 | 53497 · 185 | **53536 · 185 — pick 64 UNCHANGED**, as the ruling records |

**One discipline changed direction here, deliberately.** Every prior pass held `curve_source_store_md5`
at `81d24704` on the stated ground that it records the store the ruled curve was *derived on*. This
ladder is derived on the corrected store, so that ground is gone and the field would be false at the
old value. It **moves to `f1e8c9fe`**, and the three places that carry it moved in the same act because
the FROZEN-RULER check binds them to each other: the ui contract (full 32), the curve's own
`stamp.store_md5` (8-char), and the selftest's `_curve_source_store` (full 32). The stamp's
`per_entrant_path` and `v0surf_sig_at_fit` moved with them, for the same reason.

## 2 · THE SURFACE RE-FIT ON THE NEW PAIR

Probe both sides, as standing. **Before:** signature `af556bdc` absent from the frozen set, engine
HALTs. And the moving leg is the mirror of the store act — **`pvc` moved `28e8449b` → `35b9b300`
while `roster` held at `31df8ae9`**, because this time the curve moved and not the roster. **After:**
present, engine builds.

```
BAKE WRITTEN: data/v0surf.pkl  e4215093 -> d594dc034e86935b370c49b240a18370
written signature set: af556bdca53d… <- shipped · edb15f7ab7c9…
--verify on the same box: REPRODUCES the committed pin.
```

## 3 · THE CONFIRMATION DERIVATION — **THE CLOSURE HOLDS**

One derivation, on the new pair, under the standing ±1 rule. The harness pin met the confirmation
matrix and **HALTED as designed** (`matrix v0surf af556bdca53d != expected aca37f9f0e24`), was re-pinned
with its in-file ledger, and all four loader asserts were re-proven able to fire on real bytes.

| | |
|---|---|
| installed ladder | `df766dff94657940e2a892e91da5a6e2` |
| confirmation ladder | `431e65d35e421cb5f35659e4c4b92d03` — **installed nowhere** |
| picks compared | 64 · **differing at all 15** · **max abs delta 1** |
| **picks moving more than 1** | **0** |
| ladder sum | 53536 → 53521 (`−15`) |

**WITHIN TOLERANCE ON EVERY PICK. The closure HOLDS on the new pair.** Recorded, and the act proceeded
as the ruling directs. The movement also collapsed — 44 picks at ±1/±2 before, 15 at exactly −1 now —
which is what a basis settling looks like. Per-pick table in `confirmation_per_pick_table.json`.

---

## STEP 5 — RE-SEAL AND GATES IN ANGER

**The entrant structure re-sealed** by its own instrument from intake history. The counts moved, as the
act anticipated:

| | landed | re-sealed |
|---|---|---|
| seal | `ed5b7fcc` | **`c9e7491b`** |
| entrant PVC | 62726 (draft 55669 + mech 7057) | **62931** (draft 55753 + mech 7178) |
| expected slots/yr | 103.43 | 103.43 — **re-measured, not assumed** |

The seal's stamp is measured, never hardcoded, and it names this act's own inputs: store `f1e8c9fe`,
curve payload `df766dff`, curve file `f1cf148e`.

**THE SEAL FIRED IN ANGER BEFORE IT WAS RE-PINNED**, which is the whole point of the seal-first law.
With the new structure installed and the pins still stale, the render stopped dead:

```
LEG F5 HALT (§2.viii): sealed entrant structure seal drift — recomputed c9e7491b vs stored c9e7491b
vs pinned ed5b7fcc. Re-seal from intake history before rendering.
```

Recomputed and stored agreed; only the hardcoded pin was stale. Four source files name that seal —
found by search, not memory — and all four moved in one disclosed act (`repin_f5_seal.py`):
`rl_export.py` · `gate_f5.py` · `test_k0_dormancy_f5.py` · `ui/tests/extract_seam.test.py`.

**Both asserts re-proven able to fail, on real bytes:**

| tampered | result |
|---|---|
| one occupancy slot perturbed, stored seal left alone | `AssertionError: SEAL DRIFT a530a676/c9e7491b` |
| board's emitted entrant layer moved by 1 PVC | `AssertionError: F5 RECONCILIATION FAIL: board emitted 62932 != sealed total 62931` |
| the real pair | `MATCH True` |

**The gates, on the final pair:**

| gate | result |
|---|---|
| **G-Y0 national curve 1–64** | **0.033% ≤ 2.000% HARD** (n=1326 over 64 picks) — **no dated exception behind it** |
| one_source_selftest | **100 PASS / 0 FAIL** (the landing's was 97/0) — guards 1–3, board==engine F1, book==board F2, all six FROZEN-RULER checks on the new pins |
| Guard 4 correction-sticks canary | **PASSED** — a source correction sticks to board and book |
| F5 league conservation, both transitions | **PASS** (−2.7% and −0.2%, both in ±5%) |
| F4 roster-matched, both transitions | **PASS** (−1.4% and +1.2%, both in ±5%) |
| F5 reconciliation | board emitted 62931 == sealed 62931, **MATCH** |

**Pool divisions on the corrected store, for #326 queued behind this** (post-slide, from the emit's own
count; the run names its single boundary crosser, `Daniel Butler`):
RD 691 · ND 121 · MSD 106 · UNR 59 · IRE 57 · SSP 52 · PDA 51 · PDN 43 · PDS 21.

## STEP 6 — THE BOARD REBUILT, BOTH STAGES ATTRIBUTED, NO UNEXPLAINED MOVER

The board moves for **two** reasons in this act, so it is attributed in two runs, each holding every
other axis constant. Run against the store stage, the landing's committed instrument **HALTs by
design** — recorded rather than worked around, because that halt is the gate proving it is live:

```
store    base 81d24704  cand f1e8c9fe  DIFFERS -> UNNAMED CAUSE
HALT — ['store'] missing-or-moved between baseline and candidate.
```

| stage | boards | named pair | held constant | movers |
|---|---|---|---|---|
| **1 · store** | landed `46ebfb37` → `e7e53651` | store + surface | engine, band, **curve** `01f27f02` | **175 of 804** (21.8%) |
| **2 · re-closure** | `e7e53651` → `2b7c1a00` | curve + surface | engine, band, **store** `f1e8c9fe` | **649 of 804** (80.7%) |

Stage 1 (`attribute_movers_store_stage.py`, the committed instrument's channel logic carried verbatim,
only the cause set and held set differ): year_zero_lens 130 · ruled_curve 37 · pool_levels 8; sum
`+613` / `−45` / `+70`. Store and surface are one pair here for the same reason curve and surface are
one pair there — the engine refuses to build the corrected store on the old surface, so they cannot
move independently.

Stage 2 (the committed instrument, **unmodified**): ruled_curve 362 movers, **every one up**, sum
`+7728`; year_zero_lens 257, sum `+2090`; pool_levels 30, all up, sum `+440`. A coherent upward move
of the whole board, which is exactly what a ladder 1–2 points higher at 44 of 64 picks predicts.

**Membership 0 added / 0 dropped on both stages. Every mover carries a channel. No unexplained
residual.**

**The board pin was deliberately NOT moved.** `expected_boot.board` stays `f2df6e0a` and no UI bundle
was written, per the standing rule the artifact states in its own words — *one column is written per
LANDED change, not per rebuild* — and because adoption remains the owner's separate click. The two
boards are committed here as evidence.

## STEP 7 — THE TEXT CLEANUP: ONE ITEM DONE AND PROVEN, TWO HALTED BY THE STEP'S OWN GUARD

#328 step 7 carries its own condition: *"Text only; any edit that would change a computed value is out
of scope and halts."* Measured against that, #323 Addendum 2 item 5's premise — *"One-line fixes each;
none touches a computed value"* — **does not hold for two of its three items.** Each was checked rather
than assumed:

| item | what it would move | outcome |
|---|---|---|
| **3 · the shipped curve artifact's SCAR-by-construction self-description** | `pvc_curve_v2.json` md5 → the ui pin → the selftest's `_contract_md5`. All three are identities **this act already owns and re-pins**; the engine reads only `curve` and `pool_value` from the artifact | **DONE** |
| **1 · the dead 0.85 fallback + its false "defaults are the engine's own" comment** | the `0.85` literal feeds the v0surf signature's **gates leg** (`53f6a32c` → `8216d137` if changed), which invalidates the surface just baked. And even the comment-only half moves `engine_head` — the md5 of `_merged_recover.py`, pinned at `15525b03`, asserted by Guard 5, by N44, and by **both attribution gates in step 6** | **HALTED** |
| **2 · ~10 stale 0.85 pins in auxiliary scripts** | `par_build.py` and `par_redesign.py` are inside the **`fv` pinned source set** (`d920557e`). The remaining sites (`verify_anchors.py:8`, `verify_restore.sh`, two 2026-07-10 session scripts) are **executable** `RL_GAMMA=0.85` exports — changing them changes what those tools compute. One further hit is a deliberately-preserved stale fixture named by its own md5 | **HALTED** |

**Item 3, delivered and proven text-only rather than asserted to be:** `cleanup_curve_note_328.py`
edits the `note` field by path, asserts `curve`, `pool_value`, `curve_md5` and `numeraire` are
byte-unmoved, walks the identity chain, and then **the board was rebuilt and came back
`2b7c1a00ee88c42e46d56ca1ccce44cd` — byte-identical.** That rebuild is the proof.

The correction states the truth: the SCAR denomination is **era provenance** from `build_pvc_v34`'s
step 5, not a live property — the engine executes γ = 1.0 VOR everywhere, and the note itself always
recorded that the artifact is identical in both columns. The stage-B era figures are kept and labelled
as era figures rather than silently refreshed.

**Items 1 and 2 are the finding, not a failure to deliver.** They are real fossils and they are worth
fixing; each needs an act that re-pins the identity it moves, and item 1 additionally needs a surface
re-bake because its literal is load-bearing in the signature. That is a small ordered job, and it is
not this one.

---

## THE TWO MAIN-BRANCH DEFECTS, FOLDED IN AS ORDERED (ruling item 4)

**The declared lens basis now lands.** `docs/evidence/exec_306_zlaarm/basis/` — both the artifact
(`25a72f85`) and its emitter (`bc6ff42f`) — byte-identical to the originals on
`claude/exec-seat-306-afl-rl-zlaarm`, verified against that branch. A fit now runs from a clean
checkout; every build in this act after the commit ran **without any `RL_LENS_BASIS` override**, which
is the practical proof.

**The three lens-path variables are classified.** They live inside `_build_v0_curve`'s **refit branch**
(`_merged_recover.py:1390 else:`) — verified by walking the enclosing blocks, not by reading the
comment — which a canonical build never enters: with the frozen surface present the build takes the
load branch and performs no fit. So they are bake-lane controls and are classified **class C/diag**
beside `RL_WS` and `RL_BAKE_REFIT`, which is both accurate and needs no `model_config.json` change.

```
CONFIG INVENTORY  reads=166 vars=84  A=59 B=20 C=5 unclassified=0
  RESULT: PASS  (zero unclassified live reads; every class-A semantic represented + stamped)
```

The gate was right and the table was incomplete — that is why the repair is three rows in the table
and nothing in the gate.

---

## ACCEPTANCE SET

| # | item | state |
|---|---|---|
| 1 | store at `f1e8c9fe`, every pin re-stamped and asserted | **met** (steps 1–3, `ACT.md`) |
| 2 | new surface reproduces under its own verify on the same box | **met** — `d594dc03`, and `e4215093` before it |
| 3 | reversal check ran, verdict filed with the per-pick table | **met twice** — the halt, and the confirmation that HOLDS |
| 4 | every re-sealed gate demonstrated able to fail, both directions | **met** — derive rule, four harness asserts, seal drift, F5 reconciliation, the bake's env gate, the signature probe, and the attribution completeness gate |
| 5 | store-stage attribution complete, no unexplained mover | **met** — both stages, 0 added / 0 dropped |
| 6 | all four CI workflows green on the branch head | reported on the PR as it lands; the two that were red **on the base** are the subject of the folded-in repairs |

---

## STEP 6b — THE BOARD PUBLISHED, because the six-carrier guard said so

**A correction to this act's own step-1 reasoning, recorded as one.** Step 1 left two store-identity
carriers alone with a stated reason — `data/rl_build/*.srcmd5` and the `ui/data` bundles "are
board-derived and move at a board rebuild, which this act never reached". Step 6 reached it. The
project's own guard (`ui/tools/ownership_store_apply.py`, P3) refused the result, and was right to:

```
INCOHERENT BASE — the six store-identity carriers disagree BEFORE any write
  store file / expected_boot.store / release_contract.identities.store /
  season_state.source_store_md5 ........ f1e8c9fe
  rl_app_data.json.srcmd5.source_md5 .... 81d24704
  board_view_working.stamp.store_md5 .... 81d24704
```

*"If the tree already disagrees with itself about which store it is on, moving the pin would paper over
the disagreement instead of surfacing it."* Completed by `repin_board_identity.py` plus the canonical
writers: board artifact `f2df6e0a` → **`2b7c1a00`** with its sidecar stamped by
`single_source.stamp_derived`, `ui/data` bundles regenerated by `extract_board_view.py` (whose
RING-FENCE assert refuses until the board pin moves), the board pin moved in `expected_boot` and the
contract, contract re-sealed `ea560e55` → **`9d155e8e`**. `balanced_board_md5` deliberately not moved.

Clean-room rebuild-equality: **6/9 → 9/9, `overall_ok=True`**, rebuilt board byte-identical to the
committed artifact.

## THE CI ACCOUNTING — caused vs inherited, each reproduced on the base

Every line below was checked by running the same suite in a clean worktree at `dab9657`.

| suite | base `dab9657` | this branch | |
|---|---|---|---|
| `config_inventory` | FAIL (3 unclassified) | **PASS** | repaired |
| `extract_seam` | 40/42 | **42/42** | repaired |
| clean-room rebuild-equality | FAIL `46ebfb37 vs f2df6e0a` | **9/9 PASS** | repaired |
| `ownership_store_apply` | 28/28 | **28/28** | caused by this act, fixed |
| `club_curve_provenance` | 25/35 | 25/35 | **inherited, not repaired** |
| Live Scoring `test_weekly_updater` | FAIL (R14 config drift) | FAIL | **inherited, not repaired** |

Three of the four Final Integration failures were already on the base and **masked** — the
config-inventory gate failed first and hid the stack behind it.

**Two era-bound asserts corrected** in `ownership_store_apply.test.py`: both tied a SEALED historical
lineage entry (#283) to the live head, true only while #283 remained the latest store transition. This
act is the first legitimate store and board write since. Both now assert the entry's own recorded
constants and still fail if it is falsified; `data/release_lineage.json` is untouched. **Open for the
seam:** whether the `release_transition_register` owes an appended entry for this act.

**The two not repaired, with reasons.** `club_curve_provenance` CASE1 halts on `PVC is not monotone
non-increasing` because the pool level exceeds `curve[64] = 185` and the ingest's check spans the pool
index — a condition `one_source_selftest.py` already documents and rules owner-reserved (#207 stage 2 /
ITEM 412, "not tuned here, and not to be tuned from this figure"). Live Scoring fails on a drift
between the R14 anchor's `model_config` and the current pin inside a disposable scratch; this branch
never touches `model_config.json`, and `config_manifest check` and `release_contract check` both PASS.

**Acceptance item 6 is NOT met and cannot be by this act.** Items 1–5 stand.
