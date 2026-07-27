# ITEM 411 · D1 — BASIC COLD REVIEW OF THE STAGED RESTRUCTURE BAKE

**Filed by the supervisor pen (seam) · 2026-07-27 · register v481**

## Provenance header

- **Reviewer:** the D1 cold review seat — a bare seat opened under v427 isolation (filed artifacts
  only, no project container), implementer ≠ reviewer ≠ supervisor, ordered by the owner at v459.
- **Subject:** `ci/item-411-d1-staging @ 2ca3df8bf109d6a5c7974c9024cf659761805502`, three
  build-seat commits atop the D1 pin `1a2b1933a663492c05c6a20b6be0f497655ddb48`.
- **Two sessions.** Session 1 ran in chat housing and discharged 4 of 8 mandate items, declaring
  the other 4 not-executable rather than simulating them; its verdict of record is register
  v475–v476. Session 2 resumed **the same reviewer identity** in a shell-capable bare environment
  per the v475 routing, with the nine owner-held package artifacts supplied by the owner as a
  sealed ZIP, and discharged the remaining 4.
- **How this text reached the record:** session 2's return was **owner-couriered verbatim into the
  seam channel on 2026-07-27** and is reproduced below as received. Session 1's verdict arrived as
  owner-couriered screenshots whose tail was truncated mid-Finding-2; its substance is recorded at
  register v475 and v476 and is **not** reproduced here as verbatim text. If the session-1 text is
  later supplied, it appends to this document rather than replacing anything.
- **Seam verification of this return** — which claims were independently re-checked by the pen,
  which two findings the pen recorded *against* the review, and the ruling on the unarchived
  transform — is at **register v481**. This document is the deliverable; the register carries the
  adjudication.

> One sentence from the owner corrects any part of this filing if misstated.

---

## SESSION 2 — VERBATIM AS RECEIVED

All four blocked items executed. Nothing fixed, nothing pushed, nothing re-pinned; tracked tree clean.

### Receipt — hash gate

All 9 attached artifacts re-hashed against my mandate pins before use. No mismatch, no STOP.

```
e6ba89cb…fadcd7  ITEM_411_current_store_extraction_1.xlsx     ✓ baseline
5301dc91…7e04e4  ITEM_411_PREPARATION_PACKAGE.zip             ✓ sealed (re-checked intact after extraction)
e86aded8…914a5   ITEM_411_STORE_PACKAGE_PREP.xlsx             ✓ workbook   (from inside the seal)
4f9ec6ea…540ccc  ITEM_411_CHANGE_MANIFEST.csv                 ✓ manifest   (from inside the seal)
85e791c6…d33092  ITEM_411_CHANGE_MANIFEST.json                ✓ manifest   (from inside the seal)
12ce2b30 / 0dfe82f0 / 1f04b816 / 608910a9                     ✓ supplement set
```

I verified against the mandate pins, not `CHECKSUMS.txt` (which itself says it is not evidence).
Scratch built from `git archive` only.

### Lineage established first, which reframes two items

| commit | store | board |
|---|---|---|
| `1a2b193` (base) | `f37d9716` / sha `4cbd01ce` | `6f07f7cb` |
| `8ecf8f8`→`2ca3df8` | `c120cfd5` / sha `eb02f754` | `fa172ac1` |

So `6f07f7cb` is the base board — item 3's instrument pair is base store → base board, and the
candidate store is a committed input, not something I could re-derive from the repo.

### Item 1 — NO-OP CONTROL: PASS, with a scope caveat you should weigh

The build seat's transform is not in the repo and not in the bundle. No
`draft_stream`/`stream_pick`/`stream_year` appears in any tracked `.py`; the branch adds zero new
scripts (`git diff --name-status 1a2b193 2ca3df8 | grep '\.py$'` → 5 modified, 0 added); the
bundled `…REPRODUCE.py` is a read-only impact supplement that writes no store. Commit `8ecf8f8`
describes the transform only as "manifest-driven".

Running their transform is therefore infeasible. Rather than stop, I wrote an independent
manifest-driven transform from the declared contract alone, and ran the control on it:

```
$ python3 transform.py store_base.json ITEM_411_CHANGE_MANIFEST.csv noop_out.json --rows 0
applied: 0 field edits, 0 removal(s); 2652 -> 2652 players; 1530130 bytes
4cbd01ce5bacd411e0f20d25956475bfe1d755150d5710695626eb5afe8a111c  store_base.json
4cbd01ce5bacd411e0f20d25956475bfe1d755150d5710695626eb5afe8a111c  noop_out.json
NO-OP CONTROL: BYTE-IDENTICAL TO BASELINE
```

`4cbd01ce` unchanged — exactly the value `8ecf8f8` claims. Stable across `PYTHONHASHSEED` 0/7/999.

The result that makes this more than a self-test — the same transform, all rows applied:

```
$ python3 transform.py store_base.json ITEM_411_CHANGE_MANIFEST.csv full_out.json
applied: 10444 field edits, 1 removal(s); 2652 -> 2651 players; 1808700 bytes
eb02f7546e7c848df839fdbe5842522cef470d61d7bb9bee3cacf6a8f51659a4  full_out.json
eb02f7546e7c848df839fdbe5842522cef470d61d7bb9bee3cacf6a8f51659a4  store_cand.json
FULL TRANSFORM: BYTE-IDENTICAL TO COMMITTED CANDIDATE STORE eb02f754
```

Stable across hashseeds 0/1/42/12345. Caveat, stated plainly: this proves my reconstruction is a
no-op on zero rows — it does not directly prove theirs is. But since the manifest alone regenerates
their store byte-for-byte from the baseline, whatever script they ran computed the same function on
this input. The residual risk is confined to behaviour on inputs not exercised here.

### Item 2 — Store-level attribution, BOTH directions: PASS

Scope matches v473 exactly: 10,445 player rows = 10,444 field edits + 1 removal; the 48
`year_reference` rows (`nd_total_picks`/`rd_total_picks`) carry no store field and are correctly out
of store scope.

```
FORWARD  field edits attributed : 10444 / 10444   (new_value in cand: 0 mismatch;
                                                   old_value in base: 0 mismatch)
         REMOVAL verified       : 'matt-maguire' present in base, absent from candidate
REVERSE  field-level deltas     : 10444
         ATTRIBUTED to manifest : 10444 / 10444
         UNATTRIBUTED           : 0
         rows added / removed unexplained : 0 / 0
         manifest rows with NO store delta : 0
```

An exact bijection: no unattributed movement, and no manifest row that claims a change it did not
make. The candidate adds exactly four fields (`draft_stream`, `stream_pick`, `stream_year`,
`pick_correction_note`) and removes none.

One correction to my own instrument: my first run reported 8,711 reverse failures because I
sentinelled an absent key differently from an explicit null, while the manifest declares both as an
empty `old_value`. Same state; comparator bug, not a data finding. Fixed and re-run — and the
byte-exact reconstruction in item 1 independently corroborates the result.

### Item 3 — Instrument validation: PASS

Pinned env via the repo's own gate: `setup_env` PASS (py numpy scipy sklearn openpyxl) = 3.12.3
2.4.4 1.17.1 1.8.0 3.1.5.

```
$ cd tree_base && bash bootstrap.sh
boot-store guard (Guard 5) PASS  store f37d9716 == pinned f37d9716

$ RL_CONFIG_MODE=bake python3 rl_export.py     # 1m26s
PARITY GATE PASS: all 804 active board values == engine gated ev() (eps=0)
board stamped src=f37d9716 (read-only)
6f07f7cbe042f8e56426a01226c967c9  rl_app_data.json

$ cmp board_base_rebuilt.json tree_base/data/rl_build/rl_app_data.json
BYTE-IDENTICAL to committed base board
```

Committed board `6f07f7cb` reproduced byte-exact from the committed store, before any candidate
build. Engine head is `7c452715` at both commits and no engine source changed on the branch — so
the validated instrument is literally the same instrument used for the candidate. That is what makes
item 4 load-bearing.

### Item 4 — Determinism: PASS on every pin

Two builds, each from a wiped `/home/claude` workspace and a fresh `bootstrap.sh`:

```
BUILD A   md5 fa172ac1c90ab84e5044d3e9907c5819   sha256 a24b080a…
BUILD B   md5 fa172ac1c90ab84e5044d3e9907c5819   sha256 a24b080a…
cmp A B → BUILD A == BUILD B BYTE-IDENTICAL

CAND A  active=804  sum(v)=764021
CAND B  active=804  sum(v)=764021        ← mandate Σv 764021 over 804 active ✓
BASE    active=804  sum(v)=760253        (delta +3768)
```

candidate store sha256 `eb02f754` / md5 `c120cfd5` ✓ (verified as committed input and reproduced in
item 1) · board md5 `fa172ac1` ✓ (twice) · Σv 764021 over 804 active ✓ (twice)

Independent corroboration: the reference-vector fixture the branch adds
(`reference_vector_5546f278.json`) matches my rebuilt board with 0 present-v movers, 0 added, 0
removed, sum 764021 — so the re-pinned present authority is honest, checked against a board I built
myself rather than the one they shipped.

Protected set genuinely untouched (my first path guess was wrong and returned the empty-file hash —
corrected): `engine/rl_after/pvc_curve_v2.json` `56dd7a7b`, `per_entrant.json` `40d7da7c`,
`ui/release_pick_curve.json` `676ad2b7`, all unmoved.

### Item 8 — Suite map on `2ca3df8`, read from the Actions API

38 workflows exist in the repo; 4 are push-triggered and ran on this head.

| workflow | run | result | detail |
|---|---|---|---|
| Final Integration | `30199533155` | success | 21/21 steps |
| FV Provenance | `30199533165` | success | red/green suite |
| Live Scoring Updater | `30199533153` | success | 22 steps, 80 min |
| CI Guards | `30199533117` | failure | step 11 |

CI Guards steps 1–10 all green (incl. Guard 5, guards 1/2/3/5 + F1/F2 parity, Guard 4 canary). It
builds the board in-run to `fa172ac1` — matching mine — then fails at step 11 "Panel 10/10" with all
ten players mismatched (Nick Daicos 8765 vs 8683, etc.), RESULT: FAIL.

The cause is confirmed and benign as declared: `PANEL_EXPECTED.txt` is byte-identical between
`1a2b193` and `2ca3df8` and still pins "board `6f07f7cb`, store `f37d9716`" at a head where both
moved by design. Re-pinning it is owner authorship, correctly refused by hands.

> **Pen note, register v481 Finding A:** the conclusion is right and the cited artifact is not.
> `PANEL_EXPECTED.txt` has **zero executable readers** and the live step-11 pins are inline at
> `run_panel.sh:43`. See v481 — the landing act targets `run_panel.sh:43`, the `expected_boot.json`
> panel block and the panel narrative together, never the inert txt.

One thing the commit message does not disclose. The step-11 failure short-circuits the job, so steps
12 and 13 — RULING-CONFIG (R3) and CONFIG-MANIFEST integrity — are skipped, i.e. never asserted at
this head. "CI Guards red for that reason and that reason alone" is true about the cause but
understates the consequence: two gates went unrun. I closed that myself rather than leave it open:

```
=== STEP 12: ruling_config_check.py (R3) ===
RULING-CONFIG PASSED: RL_PVCFIT=0 (engine + env) + R3 export bake-guard active;
RL_LTI_CLOCK=advance (engine default + env + manifest pin).           EXIT=0

=== STEP 13: config_manifest.py check ===
CONFIG-MANIFEST CHECK: PASS (hash 45b207c03a8c; 59 vars; pin+stored consistent)  EXIT=0
```

Both pass at `2ca3df8`. The gap is in CI coverage, not in the artifact.

Minor observability point: Final Integration's step names still narrate
`reference_vector_1373e824`, while the actual assertion in `invariant_proof.py` uses
`5546f278`/`764021`. The assertion is correct (I verified the fixture independently); the label is
stale — the "step-names-are-narration" norm from register v478.

### COMBINED VERDICT — both sessions

Session 1 (chat housing): 4 of 8 items executed; 4 blocked as not-executable, verdict of record at
register v475.
Session 2 (this one): all 4 blocked items executed. **8 of 8 now discharged.**

The store transition is sound. Its central claim — every store movement is attributable to the filed
manifest, and nothing else moved — holds at the strongest available standard: not merely a
bidirectional row-match, but byte-exact regeneration of the candidate store from the hash-verified
baseline plus the manifest alone. The board is a deterministic function of that store, on an
instrument I validated against the committed base pair before trusting any candidate build, with
engine source untouched across the transition. Every pin in my mandate reproduced: `eb02f754`,
`c120cfd5`, `fa172ac1`, Σv 764021/804.

Three things I record against the branch, none of them disqualifying:

1. **The transform is unarchived.** The artifact that produced the store is not in the repo or the
   bundle. It reproduced here only because I could rebuild it from the manifest. If the manifest is
   ever the output of the transform rather than its input, that circularity would matter — on this
   evidence it does not, but the transform should be committed before landing, not reconstructed by
   a reviewer.
2. **Two gates unasserted in CI** (R3, CONFIG-MANIFEST), masked by the panel short-circuit. Both
   pass locally; the reporting is what misleads.
3. **`PANEL_EXPECTED.txt` is internally inconsistent at this head** — correctly so, pending owner
   authorship. Until it is re-pinned, this branch cannot show a green CI Guards, and any reader
   taking the red at face value will misread it.

Honest-infeasible declared where it applies: item 1 as literally worded — "the transform" — was not
executable, and I have not claimed otherwise. What I ran is a faithful reconstruction whose
equivalence on this input is proven byte-exact; that is stronger than the original ask in reach and
weaker in provenance, and you should read it as exactly that.

Standing recommendation unchanged: this is staging evidence, and the landing decision remains
owner-worded. I fixed nothing, pushed nothing, re-pinned nothing.

---

*End of session-2 verbatim text. Adjudication, seam verification and the unarchived-transform
ruling are at register v481.*
