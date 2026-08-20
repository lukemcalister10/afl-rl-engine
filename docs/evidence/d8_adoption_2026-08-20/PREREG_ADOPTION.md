# PREREG — THE D8 ADOPTION. Written and committed BEFORE the engine is touched (law F6).

**Seat:** D8 adoption seat · **Date:** 2026-08-20 · **Base:** `main` @ `028eb4d`
**Register:** v797 records the owner's *intent*; **v798** is the entry this act earns.

## 0. THE WORD

The owner's adoption word was given today, **2026-08-20**, verbatim:

> **"Yes. I'm adopting."**

It was given in chat, post-compaction. Register **v797** (commit `028eb4d`) records the prior *intent*
("the owner intends to adopt D8 post-compaction"); the word is now real. This seat did not create the
approval and does not interpret it — it records one that exists and executes the lane the word names.
`docs/OPEN_ITEMS_REGISTER.md` is the supervisor's pen and is **not touched by this seat**.

## 1. WHAT IS BEING DONE, AND THROUGH WHICH LANE

`RL_O33_TAPEROFF` — ORDER D8's ceiling-only dial, priced 2026-08-20 at
`docs/evidence/d8_ceiling_2026-08-20/`, delivered **PRICED, NOT ADOPTED** — is flipped from
**default OFF** to **shipped default-ON**, behind a **DECLARED KILL-SWITCH**, through the *exact lane*
THE BAKE used (`f27482f`, register v780): the default literal in the engine changes, the kill-switch
name is stamped in the comment, and **`data/model_config.json` is not touched**.

One engine expression changes:

```python
_O33_TAPEROFF=os.environ.get('RL_O33_TAPEROFF','0')!='0'   # engine/rl_after/_merged_recover.py:1145
                                            ^^^  ->  '1'
```

plus the comment block above it (lines ~1118–1144), restamped to the bake idiom already used by its
declared family at `:473 :495 :529 :577 :595 :613 :632 :650 :709 :770`. **The block's technical content
is kept intact** — why it is not a manifest var, the `b6`/B-3 mechanics, why the B-1 ladder is
unreachable by construction. Only the stale half is rewritten (`default OFF; PRICED, NOT ADOPTED` /
`ADOPTION IS A LATER ACT, on the owner's word`).

No other engine file is touched. No parameter is added, fitted or targeted: `asc == 1` is ORDER B's own
boundary solution and the dial is a boolean. `q97m` stays FROZEN.

## 2. THE NUMERIC PREDICTIONS

Measured with the accepted disposable FV builder
(`session_2026-07-20/fv_provenance_remediation/test_fv_provenance._run_build`, `PYTHONHASHSEED=0`, BLAS
threads pinned to 1, staging into a throwaway dir, writing nothing under the repo), driven by the exact
recipe the D8 pricing seat used (`docs/evidence/d8_ceiling_2026-08-20/d8_build.py`, `run_price.sh`),
strictly sequential, under `tools/build_lock.sh`.

### 2.1 The two builds

| # | build | prediction |
|---|---|---|
| **P1** | **BARE** — no model-semantics `RL_*` set at all, `RL_O33_TAPEROFF` **unset** | board md5 **`5ea978f7b6a073abb2012f10cccbc3e3`**, total **693,753**, **804** rows, **byte-exact** against the priced candidate |
| **P2** | **KILL-SWITCH** — `RL_O33_TAPEROFF=0` | board md5 **`a05fe951f78482c70520480e184c80ec`**, total **664,949**, **804** rows, **byte-exact** against the live board of record |

P1 is the whole meaning of "shipped default": the bare build must reproduce, byte for byte, the board the
owner looked at and approved. P2 is the whole meaning of "declared kill-switch": the named var must
reproduce the retired board, byte for byte.

### 2.2 The identities

Pre-edit values read from `data/expected_boot.json` at `028eb4d` and re-hashed from the tree.

| identity | before | prediction |
|---|---|---|
| `board` | `a05fe951f78482c70520480e184c80ec` | **MOVES** → `5ea978f7b6a073abb2012f10cccbc3e3` |
| `engine_head` (md5 `_merged_recover.py`) | `338a790b773cfbbff0e1283794c72efe` | **MOVES** — value unknown until the edit exists; it will be **RECOMPUTED** from the edited source by the tree's own definition (`boot_guard.py:310`, md5 of the file), never typed |
| `config` / `config_sha256` | `eed19a75f775aeafe4ee5ea4b3990667192d8f90389ad6b0e8318e91062d14c1` | **DOES NOT MOVE.** The dial is deliberately absent from `data/model_config.json` — it is a declared kill-switch, not a manifest dial, exactly as `RL_CAPT` / `RL_ISOFADE` / `RL_EVW` / `RL_UNCOMP` / the 18 bake dials. `config_manifest.enforce()` must keep REJECTING `RL_O33_TAPEROFF` as an unknown model override in bake/gate/canonical mode. **Asserted, not assumed.** |
| `rl_model` | `6fe7c4155866d80e8045bed2d3bf2802` | **DOES NOT MOVE** (file untouched) |
| `fv` | `6e9a370e5970c5aefa859858070f4c3420f0177b4698d6fac90bd08bf1780346` | **DOES NOT MOVE** (`engine/forward_valuation` untouched) |
| `store` | `cc02567f80bef39228f25854d121a766` | **DOES NOT MOVE.** This is a lever change; nothing writes the store. |
| `band` | `34faa8659cc8f19794f5cb9584fa19b2` | **DOES NOT MOVE** |
| `register` (LTI) | `652d83e87780e415a01a2de6d8b3cc57` | **DOES NOT MOVE** |
| `q97m` | `cfdc73216c099e5e8f1fda3968f31c00` | **DOES NOT MOVE** — FROZEN, no bake-time refit here (R-W6) |
| `v0surf` | `5dd34ca82735f5c8f021b1c7320df8f8` | **DOES NOT MOVE** |
| `as_of_round` | `22` | **HELD at 22** — no round is applied |
| day-0 reference `docs/evidence/final_candidate_2026-08-19/DAY0_CP.json` | `210510fe5d09bbbd16909bb63f4a118d` | **DOES NOT MOVE** — not re-based by this act |
| `balanced_board_md5` | `72fe3a176953fce36239d7b81c3cd492` | **MOVES** — value unknown until built. The dial sits in `b6`, which the balanced/strict sibling posture (`RL_PVC2=1 RL_LEGE=0 RL_LEGF=0`) also reaches, so the sibling is predicted to move. It will be **BUILT** by `sibling_repin.py reconcile` (build-and-compare) and the derived value recorded — never typed in. If it comes back UNMOVED that is a finding to be reported honestly, not smoothed. |
| `contract_sha256` | `88d298264cc5c75e108599c0a44ef3c97b0058428ed9fab2789b21e05c363989` | **MOVES** (it seals the moved identities) |

### 2.3 The board move, as the owner saw it priced

| | |
|---|---|
| from | `a05fe951f78482c70520480e184c80ec` — total **664,949** / 804 rows |
| to | `5ea978f7b6a073abb2012f10cccbc3e3` — total **693,753** / 804 rows (**+28,804**, **+4.3318 %**) |
| movers | 559 of 804 — 551 up, 8 down, 245 unmoved |
| ceiling v-inversions | **407 → 0** |

(Source: `docs/evidence/d8_ceiling_2026-08-20/MOVERS_D8.md`, `PACKET_D8.md` §4. Nothing is re-derived
here; these are the numbers the owner's word was given against.)

## 3. THE FALSIFIERS — EXPLICIT, AND WHAT EACH ONE DOES ON FIRING

> A fired falsifier is a HALT. It is not improvised around, not re-run until green, and not narrowed.

**F1 — THE BARE BUILD.**
After the flip, a build with `RL_O33_TAPEROFF` **unset** (and no model-semantics `RL_*` set) produces a
board whose md5 is **not** `5ea978f7b6a073abb2012f10cccbc3e3`, **or** whose active-row `v` total is
**not** `693,753`, **or** whose active row count is not **804**.
→ **HALT. Revert the engine edit. Report.** The default did not become what the owner approved, and
nothing downstream of it may be pinned.

**F2 — THE KILL-SWITCH.**
After the flip, a build with `RL_O33_TAPEROFF=0` produces a board whose md5 is **not**
`a05fe951f78482c70520480e184c80ec`, **or** whose total is **not** `664,949`.
→ **HALT. Revert the engine edit. Report.** A kill-switch that does not reproduce the retired board
byte-exact is not a kill-switch, and the comment stamping it as one would be false.

**F3 — IDENTITY RE-PROOF AFTER THE REPIN.**
Any identity re-proof mismatch after the pins move — the six-way store coherence, Guard 5 / boot_guard,
`release_manifest_check.py` carrier coherence, `release_contract.py check`, the contract self-seal, the
`sibling_repin` overlay validation, or a pin whose written value does not read back equal to the value
measured from the tree.
→ **HALT. Report.**

**F4 (auxiliary, non-negotiable) — THE THINGS THAT MUST NOT MOVE.**
`config_sha256`, `rl_model`, `fv`, `store`, `band`, `register`, `q97m`, `v0surf`, `as_of_round`, the
day-0 reference `DAY0_CP.json`, or `data/model_config.json` itself.
→ Any of these moving is a **HALT**, reported, not re-stamped into agreement.

**F5 (auxiliary) — THE GATES.**
`python3 release_manifest_check.py` not GREEN, or `python3 -m acceptance.runner` not GREEN (7 checks),
for any reason other than a pin that this adoption *legitimately* moves and that is moved in the same
commit as the pins.
→ **No check is ever weakened to get green.** A genuinely red check is a **HALT + report**.

Baseline, measured on `028eb4d` before any edit (so a post-flip red is attributable):

```
release_manifest_check.py      RELEASE MANIFEST COHERENCE: PASS   (38/40 coherent, 2 sealed-lag)
release_contract.py check      PASS (contract 88d298264cc5)
python3 -m acceptance.runner   7 checks | PASS 7 FAIL 0 BLOCKED 0 RULED-RED 0 | VERDICT GREEN
```

The two **sealed-lag** stamps (`book_stable_seal.store_md5`, `book_stable_seal.head_md5`) are a
pre-existing, reported-never-gating freeze-lag from THE LANDING. This act moves `engine_head`, so the
head-side lag **widens** — that is expected and is **not** re-sealed here: a book re-seal is a separate
act and this seat will not smuggle one in (the `PACKET_D8.md` §2.1 precedent, verbatim).

## 4. THE ACTS, AND THE COMMIT DISCIPLINE

1. **This file** — its own commit, before the engine is touched. *(F6)*
2. **The engine edit** — `engine/rl_after/_merged_recover.py` alone, its own commit.
3. **The proofs** — bare build + kill-switch build, both captured to this directory. F1/F2 adjudicated.
4. **The landing transaction** — pins (`data/expected_boot.json` board + engine_head, the board artifact
   `data/rl_build/rl_app_data.json` and its `.srcmd5` sidecar moved TOGETHER, C3 pattern), lineage
   (append-only, `register_landing_column`), release contract (`restamp_dynamic` then the bake-lane
   identities), sibling repin, **both** UI bundles (`extract_board_view` **and**
   `round_movers.inject_release_contract(22)` — the thrice-proven trap), gates.
5. **`FINAL_STATE.md`** — every identity before → after, every commit sha with its paths, every verdict.

Every commit is `git commit -- <explicit paths>`. Never a bare `git commit` after `git add`; never a
sweep. **Nothing is pushed.** `docs/OPEN_ITEMS_REGISTER.md` is not touched.

## 5. WHAT THIS ACT IS NOT

It does not re-seal the book. It does not apply R23 or any round. It does not touch the store, the
frozen pick curve, the curve contract, `q97m`, or the day-0 reference. It does not add a manifest var.
It does not re-price anything: every number above was measured by the D8 pricing seat and is reproduced,
not re-derived.
