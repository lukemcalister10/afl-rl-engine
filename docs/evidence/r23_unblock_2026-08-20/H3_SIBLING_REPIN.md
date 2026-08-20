# THE SIBLING / BALANCED REPIN — one act, through the writers of record.

**Seat:** H3 repair + R23 advance (build seat), register **v792** · **Date:** 2026-08-20
**Rides on:** the H3 clock re-pin (`039024c`), whose falsifiers are in `H3_REPAIR_RESULT.md`.
**Store `cc02567f` and canonical board `a05fe951` are UNMOVED by this act.** Only the derived
balanced/strict sibling layer and the pins that name it move.

---

## 1. What was run, and why that command

```
python3 engine/rl_after/ingestion/sibling_repin.py reconcile --repo . --commit 039024c
```

`sibling_repin.reconcile` **is** the writer of record for this layer — the same code path
`staged_apply._stage_sibling` (`staged_apply.py:546-565`) invokes inside a round-advance transaction,
run here standalone because there is no round advance in this act. It **rebuilds** the sibling from the
live store via the accepted disposable FV builder, **derives the identity from the built artifact —
never from a supplied constant (build-and-compare)**, regenerates the complete FV reference vector from
that freshly built board, and stages the coherent movement of every dependent pin, then commits it
atomically with rollback. Run under `tools/build_lock.sh`, `PYTHONHASHSEED=0`, BLAS threads pinned to 1.

## 2. The identities that moved — all in the one transaction `txn_22_72fe3a17`

| pin / artifact | before | after |
|---|---|---|
| `expected_boot.balanced_board_md5` | `234c3414fa001bd9538deb6668e169f0` | **`72fe3a176953fce36239d7b81c3cd492`** |
| `release_contract.identities.balanced_board_md5` | `234c3414` | **`72fe3a17`** |
| `release_contract.present_lens_baseline.balanced_board_md5` | `234c3414` | **`72fe3a17`** |
| `release_contract.present_lens_baseline.present_value_total` | `761574` | **`664949`** |
| `release_contract.contract_sha256` (**the seal it feeds**) | `be37b3b4c584…` | **`8da998ce9764…`** |
| `sibling_repin_state.source_store_md5` | `d9a24282` (the DOB-courier landing) | **`cc02567f`** (live) |
| `sibling_repin_state.contract_sha256` | `ef25c259…` | **`8da998ce…`** |
| `sibling_repin_state.forward_board_md5` | `4b448a82` | **`a05fe951`** (the board of record) |
| `sibling_repin_state.harry_sheezel` | `11925` | **`10433`** |
| `sibling_repin_state.present_value_total` | `761574` | **`664949`** |
| `sibling_repin_state.fv_identity` | `d920557e…` | **`6e9a370e…`** |
| `sibling_repin_state.generated_at_commit` | `null` | **`039024c357736aa4d33ac81013c57d3485242c67`** |
| `test_fv_provenance.BOARD_MD5_GOOD` + oracle expectations | `234c3414` / 761574 / 11925 | **`72fe3a17` / 664949 / 10433** |
| `ui/data/board_view_working.js` `stamp.balanced_board_md5` | `234c3414` | **`72fe3a17`** |

**New generated artifacts** (`session_2026-07-20/fv_provenance_remediation/`):
`fixtures/reference_vector_72fe3a17.json` · `fixtures/forward_vector_a05fe951.json` ·
`test_forward_lens_a05fe951.py`. Prior-round oracles/vectors are retained, as at every previous
advance. `ui/data/board_view_public.js` was regenerated and came out **byte-identical** (it carries no
identity pins — verified).

The forward-lens totals in the sidecar (`forward_p1_total 598980`, `forward_p2_total 191217`) were
cross-checked against the live board of record's own Σ`vP1` / Σ`vP2`: **598,980 and 191,217, exact.**
They moved only because the sidecar had been pinned to the pre-ORDER-29 board `4b448a82`; nothing in
this act moved a forward value (F1: the canonical board is byte-identical).

## 3. THE T7 GAP — hit, named, and closed with the second writer

`sibling_repin._regen_board_view` runs **`extract_board_view` only**. `stamp.release` — the full
release identity the browser validates lineage against — is written by a **different** writer,
`round_movers.inject_release_contract`, which only `round_finalize` calls. So the repin's bundle
regeneration **dropped `stamp.release` entirely**, and `release_manifest_check` went **FAIL**:

```
40 carrier fields across 8 identities and 7 files: 31 coherent, 8 incoherent, 1 sealed-lag
  ui_bundle.stamp.release:{store,board,engine_head,rl_model,fv,config,register,as_of_round}
      board_view_working.stamp.release.* = (empty)
  RELEASE MANIFEST COHERENCE: FAIL
```

**Closed by running the second step of record**, `round_movers.inject_release_contract(working, repo,
22)` — not by hand-editing the bundle. Measured before and after: the pre-repin bundle carried a
`stamp.release` block with exactly these fields, so this **restores** it rather than inventing it.
Note `stamp.release.balanced_board_md5` reads `06d8af60` both before and after: that field is the
**immutable v2.11 present-lens lineage anchor** from `data/release_lineage.json`, constant across
rounds by owner/supervisor ruling 2026-07-20 and explicitly *"NEVER synthesized"*. It is correct that
it did not move with the balanced board.

## 4. Verdicts after the act

| check | verdict |
|---|---|
| `sibling_repin verify` | **`ok: true`, `fails: []`** — was `ok:false` with **7** stale-sidecar fails |
| `release_manifest_check` | **PASS** — 40 carriers, **39 coherent, 0 incoherent**, 1 sealed-lag |
| `python3 -m acceptance.runner` | **GREEN — 7 PASS / 0 FAIL / 0 BLOCKED**, contract seal `8da998ce9764` |
| FV board oracle (`test_fv_provenance.board_oracle`) | **PASS** — `rc=0 md5=72fe3a17 active=804 sumv=664949 sheezel=10433 vector_movers=0` |
| `ui/tests/movers.test.js` | **66 / 66 PASS** |

### The v788 sibling fork — DISCHARGED (option A)

The seven `verify` fails were one fact: the sidecar named the pre-ORDER-29 state (`d9a24282` /
`4b448a82` / `234c3414` / `ef25c259`). They are gone because the advance-repin **rebuilt and re-derived**
the layer, which is exactly the non-no-op case the module exists to serve — not because anything was
hand-edited to match.

### The v791 book-seal-lag — NOT RESEALED, and not required. Reported.

`reseal_book` is **not required by any gate this act trips.** `release_manifest_check` classifies
`book_stable_seal.store_md5` (sealed against `cb38ef11`, tree `cc02567f`) as **SEALED-LAG —
*"legitimate between seals; reported, never gating"***, and the lag **pre-existed this act** (the base
acceptance run at `702e25d` reported the same 39/40 + 1 sealed-lag). Nothing here moved the store or
the canonical board, so nothing here changed the seal's relationship to the tree.

Independently, `docs/evidence/landing_prep_2026-08-20/RESEAL_HALT.md` records **three unresolved
blockers** (the candidate's 18-dial line cannot enter gate mode; `RL_V0SURF_PKL` is not in
`INFRA_ALLOW` so the branch's own frozen surface cannot be loaded under gate mode; the staged
`rl_app_data.json.srcmd5` pair is internally inconsistent) and **owner word is pending on all three**.
Per the seat order — *"if a genuine ambiguity arises, HALT that item"* — **the re-seal was not
attempted and `data/book_stable_seal.json` is byte-unchanged.**

## 5. Not committed

`engine/rl_after/ingestion/.sibling_txn/txn_22_72fe3a17/` — the transaction's staged bytes and
originals (1.6 MB). It has never been tracked in this repo's history and is not a release artifact;
git now holds the revert.
