# ITEM 408 · D2 — COLD REVIEW COMPLETION PASS

**Filed by the supervisor pen (seam) · 2026-07-27 · register v487**

## Provenance header

- **Reviewer:** `d2-cold-review` — the same seat identity resuming per the v482 routing, in a
  shell-capable multi-core runner (`nproc=4`) without per-call process reaping.
- **Subject:** `ci/item-408-d2-staging @ dd117adfe0f0a0e77f05ab82ae0cd725e18bfaa0`, base pin
  `1a2b1933`. **Authority:** D2 §3, issue #157 as amended by Amendment 1.
- **Verdict:** **CLEAR-WITH-NOTES** on the completion mandate. Items 1, 4, 5, 6, 7 all verified by
  re-run and passing. Combined with items 2, 3, 8 from the partial pass, **the D2 §3 mandate is
  fully evidenced.** No merge-blocking finding. Three notes, none defects in this branch.
- **Companion document:** the partial pass is filed at `ITEM_408_D2_COLD_REVIEW_partial.md`
  (register v482). The two together are the complete D2 cold review; neither supersedes the other.
- **How this text reached the record:** owner-couriered verbatim into the seam channel on
  2026-07-27, reproduced below as received.
- **Seam verification and rulings** — including the pen's confirmation of all three notes and the
  **register correction Note 2 forces** — are at **register v487**.

> One sentence from the owner corrects any part of this filing if misstated.

---

## VERBATIM AS RECEIVED

**COLD REVIEW REPORT — ITEM 408 D2 (COMPLETION PASS)**

Reviewer: d2-cold-review · Subject: `ci/item-408-d2-staging @ dd117adfe0f0a0e77f05ab82ae0cd725e18bfaa0` · Base pin: `1a2b1933` · Authority: D2 §3, issue #157 as amended by Amendment 1 · Date: 2026-07-27

### VERDICT

**CLEAR-WITH-NOTES** on the completion mandate. Items 1, 4, 5, 6, 7 are all verified by re-run and all pass. Combined with items 2, 3, 8 from the prior pass, the mandate is now fully evidenced. No merge-blocking finding. Three notes, none of them defects in this branch.

### RESULTS

| # | Item | Result |
|---|---|---|
| 1 | both harnesses to full count | 33/33 PASS (exit 0, 24 min) · 73/73 PASS (exit 0, 93 min) — exactly the filed figures |
| 4 | negative controls on live key names | PASS — D5×4, D6×3, D7×2, D8×2 |
| 5 | atomicity, mid-transaction fault, zero targets moved | PASS — D3, D4, P3–P7 |
| 6 | P13/P15 scratch-relative, fail-on-corruption preserved | PASS |
| 7 | protected set 0-diff | PASS — all four members byte-identical |

### Item 7 — protected set, 0-diff on the directive's named list

All four members identical at `1a2b1933` and `dd117ad` (same blob SHA, same md5, same byte count), and both Amendment-1 pins reproduce exactly:

```
engine/rl_after/pvc_curve_v2.json                        2248 B  md5 56dd7a7b… == Amendment-1 pin
ui/release_pick_curve.json                                779 B  md5 676ad2b7… == Amendment-1 pin
session_2026-07-17/legd_derivation/out/per_entrant.json  1765993 B  md5 40d7da7c…
engine/rl_after/rl_model_data.json  (the store)          1530130 B  md5 f37d9716…
```

The VOID pin `26a034c2` matches nothing here. `git diff --stat 1a2b1933..dd117ad` is 6 `.py` files — no protected-set path appears in the diff at all. Neither hash is the empty-input sentinel `d41d8cd9…`, so real bytes were hashed.

### Item 5 — atomicity

Forward path (D3/D4) and staged path (P3–P7), fault injected inside the one transaction:

```
D3 before_validation        raised=SiblingFault  moved=[]  forward_files_left=[]  oracle_files_left=[]
D4 after_first_replacement  raised=SiblingFault  moved=[]  forward_files_left=[]  oracle_files_left=[]
D4 journal                  txn statuses=['ROLLED_BACK']
P3 generation failure   changed=[] newrv=[]      P5 fault after 1st canonical  still-changed=[]
P4 validation failure   changed=[] newrv=[]      P6 fault after sibling replace still-changed=[]
P7 crash recovery       incomplete=1 partial=True → next advance BLOCKED → still-changed=[]
```

D4 is the load-bearing one: `ROLLED_BACK` in the journal proves it genuinely passed the first replacement and unwound, rather than aborting pre-commit and passing trivially. `tree_state` walks four roots recursively (`data`, `ui/data`, `ingestion`, `fv_provenance_remediation`) — a broad sweep, not a whitelist that could miss a moved target. `bool(raised)` is part of every pass condition, so a case where nothing ran cannot score.

### Item 4 — negative controls fire on live key names

I mapped the resolver's actual read surface independently rather than trusting the harness labels: `continuity_fails`, `cohort_fails`, `oracle_fails` (`forward_lens.py`) and the sidecar checks at `sibling_repin.py:1271–1328`. Every tamper targets a key inside that surface, and each reads the live value before substituting — `assert new != s, "the control did not fire on a live key name"`, and D7's `assert sc.get("forward_vector_sha256") == old_seal`.

The discrimination pair is the part that makes this non-vacuous, and both halves are sound: `_doc` is written at `forward_lens.py:365` and read by nothing, and `vector_seal` covers only the lens vectors — so "stays green" is structural, not luck. `conservation.players` is read at `continuity_fails` and reds immediately.

```
D8 unread field (_doc)              rc=0  SIBLING CHECK: CURRENT
D8 read field (conservation)        rc=2  '+2 conservation players 636891 != sum(vector.values()) 636888 (G-Y0)'
D7 sum-preserving, triple-resealed  rc=0 on coherence gate → rc=2 on --full, EXACT-FORWARD-VECTOR MISMATCH
```

The scratch ran at board `32b0944f`/`790df69e`, sums 687465/636888, Sheezel 8133/8130 — no overlap with the live R19 frame (`6f07f7cb`, 705057/656811, 9542). The controls were provably operating on derived truth, not on literals that happen to match the live tree.

### Item 6 — P13/P15

Confirmed as briefed: the R19 literals at `:596` are the repair docstring, and the only other R19 strings in that file are the P1 drift sentinel (`:197–199`) and the known-open P8 block. The executable paths carry none. Executed:

```
P13  injected=True  ('active') == 804 → 803        ['FV oracle active != contract present_lens active']
P13  injected=True  ('sum_v') == 757081 → 757080   ['FV oracle sum_v != contract present_lens total']
P13  injected=True  ('sheezel') == 7964 → 7963     ['FV oracle sheezel != reference vector Sheezel']
P13  injected=True  (reference_vector_790df69e.json → …deadbeef.json)
P15  round=14 (from the scratch's OWN boot manifest)  baseline no-op: changed=False no_op=True
P15  view-only repair: changed=True no_op=False;  balanced pin before=790df69e after=790df69e
```

`sum_v=757081` and `sheezel=7964` are the scratch's values, not R19's 760253/9542 — the tokens were discovered by parsing, and the fail-on-corruption guard (`injected=True`) is part of every pass condition, so a `str.replace` that matched nothing would red rather than pass quietly. Item 6's property holds.

### NOTES

**Note 1 (new, not a defect) — neither harness is wired into CI.** `grep` across all `*.yml` and `*.sh` finds no invocation of `staged_sibling_integration_proof.py` or `forward_lens_integration_proof.py`. The four green suites on `dd117ad` (item 8) do not execute the 33 or the 73. The counts I report are sound — I ran them myself at the subject SHA from pristine state — but they are hand-run evidence, not continuously gated, and would not catch a regression on a future push. Raising it for routing, not as a merge blocker.

**Note 2 — P2 vacuity is narrower than the register's summary.** Only the check at `:233–234` is vacuous: `new_md5 != PRE_BALANCED` compares against `1373e824`, which this scratch never held (its pre-advance balanced board is `790df69e`), so it passes whether or not the sibling advanced. But the rest of the P2 group is frame-correct and does carry the single-transaction property — notably `:238–240` asserting `refvec["board_md5"] == new_md5`, plus the target accounting (manifest=17 collected=17 replaced=17 commit_verified=17) and `SIBLING_STAGED` precedes `COMMIT_BEGIN`. I record this as one dead check inside a live group rather than "P2 proves nothing"; the distinction matters if Track D scopes the repair.

**Note 3 — P8 confirmed open, as briefed.** Hardcoded `reference_vector_1373e824.json` at `:408` and the silent default `vec.get("harry-sheezel", 9542)` at `:433`. Both are live-tree R19 reads that will break or silently degrade at R20. Already routed to Track D; not mine to fix.

The hardening note from my previous pass (unconditional `config_manifest_loaded = True` at `sibling_repin.py:447`) stands unchanged; I understand it is already ruled and applies after this pass.

### TOOL LIMITS AND REVIEWER ERROR

**Reviewer error, recorded for integrity.** My first attempt seeded the scratch with `git archive`, which strips `.git`. `materialize_r14` reads exact historical git bytes and failed closed. I then found the deeper cause: this session's container clones the repository shallow (`is-shallow-repository: true`, 35 commits), so the R14 anchor `93bd01af` exists as a boundary object but is not an ancestor in the graph. Neither is a branch defect — the fixture failed closed and named the remedy verbatim ("In CI, check out with full history"). I resolved it by cloning and `git fetch --unshallow` from origin (1150 commits), verifying the checkout was clean and byte-identical to the pristine archive before running. **Anyone repeating this pass needs full history; `git archive` alone will not do.**

The compute limit from my last pass did not recur — this runner is `nproc=4` rather than 1, and the two harnesses ran concurrently to completion in 93 minutes wall-clock.

**Hygiene.** Both harnesses ran from a clean detached checkout at `dd117ad`; `git status --porcelain` is empty in both the session checkout and the scratch clone after the run. Result JSON went to `…/scratchpad/proofout_{D,P}/`, outside both checkouts. Board B was never a build input. No fix, no re-pin, no commit, no push.

Signed: **d2-cold-review**

Disposition: completion mandate discharged; items 1, 4, 5, 6, 7 all pass; no merge-blocking finding; three notes for routing. Nothing filed to the repository — the verdict routes to the owner and the supervisor pen files it.

---

*End of verbatim text. Seam verification, the confirmation of all three notes, and the register
correction Note 2 forces are at register v487.*
