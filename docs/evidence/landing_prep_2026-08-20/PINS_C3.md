# C3 — THE SIX-PIN RE-KEY, DISCLOSED PIN BY PIN

**land/order-29 @ `ba37032` · candidate board `a05fe951` / 664,949 / 804 · engine `5f434b95`**

**NOT ADOPTED. NOTHING TAGGED. NOTHING PROMOTED TO MAIN. THE LIVE BOARD (`88ce647f`) IS UNTOUCHED.**
Tag push and main promote are **owner-only** and the owner has not given the landing word.

> The law this act was run under: **the re-key changes PINS TO MATCH REALITY, never reality to match
> pins.** Every value below was **computed from the branch tree** by `rekey_c3.py`, in-process, using
> the same routines the guard uses — `md5()` for files, `config_manifest.manifest_hash()` for config,
> `fv_provenance.fv_identity()` for the forward-valuation source set. **Nothing was typed in from the
> order or the register.** Each of the six was traced against the tree before being touched, and a pin
> that already matched was left alone and reported as already-correct rather than re-stamped.

## THE SIX PINS

| # | pin | source of truth (branch tree) | old | new | verdict |
|---|---|---|---|---|---|
| 1 | `engine_head` | `engine/rl_after/_merged_recover.py` | `a353a9d361937a78014eef521cb65d68` | `5f434b9592ad8adb7dcd534da49df3c7` | **RE-STAMPED** |
| 2 | `rl_model` | `engine/rl_after/rl_model.py` | `14000af2a46f7a3c4cdfde303f5a1aff` | `98f16794ba4ce7ca4747320d4ebc510c` | **RE-STAMPED** |
| 3 | `board` | `data/rl_build/rl_app_data.json` | `36d5dfc73e2b508ece530bc7dfae2090` | `a05fe951f78482c70520480e184c80ec` | **RE-STAMPED** (+ artifact synced, §2) |
| 4 | `config` | `data/model_config.json` via `config_manifest.manifest_hash` | `eed19a75…62d14c1` | *(unchanged)* | **ALREADY CORRECT — traced, not re-stamped** |
| 5 | `v0surf` | `data/v0surf.pkl` | `5dd34ca82735f5c8f021b1c7320df8f8` | *(unchanged)* | **ALREADY CORRECT — traced, not re-stamped** |
| 6 | `fv` | `engine/forward_valuation` source-set tree hash | `2621b56a…60f7dc6` | `6e9a370e5970c5aefa859858070f4c3420f0177b4698d6fac90bd08bf1780346` | **RE-STAMPED** |

**Four moved, two were already right.** Raw run: `REKEY_C3_out.txt`.

### On pins 4 and 5 — the ones that did not move

The order flagged `v0surf` with the v767 correction already attached: *"the branch pin matches the
branch file; what you are fixing is whatever the pinned value actually mismatches."* Traced: the pin
`5dd34ca8…` **equals** `data/v0surf.pkl` exactly. There was no stale pin to fix. The v0surf failure
Guard 5 was firing is a **LOAD-PATH** failure, not a pin failure — `/home/claude/v0surf.pkl`
(`fbc5b393`) shadowing the branch file — and **a pin re-key cannot fix it.** See `RESEAL_HALT.md` §3
and the landing table's closing note. `config` likewise matched on measurement. Re-stamping either
to a value it already held would have been theatre; both were left byte-identical.

### On pin 6 — the sixth pin

`fv` is the pin *"never re-stamped after the Order 28 grace-A wiring"*. ORDER 29B said so in its own
commit message at `0260787`: *"fv IS LEFT RED, DELIBERATELY. It is ORDER 28's drift, carried through
ORDER 29 unrestamped."* It is the drift Guard 5 fires **CHECKOUT** and **LOADED-PATH** on — two
legs, one pin. Both now pass; the guard's own PASS line prints
`fv 6e9a370e == pinned 6e9a370e (checkout+loaded-path)`.

## SURGICAL DISCIPLINE — WHAT ELSE CHANGED IN THE FILE

**Nothing.** `rekey_c3.py` edits the file as **raw text**, replacing one exact value at a time, and
**asserts each old value occurs exactly once in the whole file** before touching it. `json.dump` is
never used to rewrite it, so key order, whitespace and every note field survive byte-for-byte. The
script then re-reads the result and asserts:

```
  JSON valid                                  : yes
  keys whose value moved                      : ['board', 'engine_head', 'fv', 'rl_model']
  keys declared to move                       : ['board', 'engine_head', 'fv', 'rl_model']
  note fields (_*) moved                      : NONE (byte-for-byte preserved)
  key count before / after                    : 37 / 37
  bytes before / after                        : 20888 / 20888
  byte-diff == exactly the declared values    : yes
```

`git diff data/expected_boot.json` is **four changed value lines and nothing else.**

## 2. THE ONE COMPANION ACT, DISCLOSED RATHER THAN SLIPPED IN

**`data/rl_build/rl_app_data.json` `36d5dfc7` → `a05fe951`.**

`boot_guard` (0c) asserts the **checked-out** `data/rl_build/rl_app_data.json` == the `board` pin. So
the board pin cannot move on its own — pin and artifact move together or Guard 5 goes red on the
board leg. This is the same pairing **ORDER 29B performed at `0260787`**, in its own words:
*"data/rl_build/rl_app_data.json synced to the new board — Guard 5 asserts THAT copy, not the engine
one, and it fired in anger when it was stale"*; and ORDER 25 / ORDER 23 before it (*"THE BOARD REBUILT
DETERMINISTICALLY, AND THE PINS RESTAMPED"*).

The board written is **not authored**: it is the byte-exact output of the candidate dial line
(`docs/evidence/parity_2026-08-19/build_D7B.sh`, `ONLY=cand`), reproduced in this seat as the **first
act** and md5-verified `a05fe951f78482c70520480e184c80ec` **before and after** the copy
(`sync_board.sh`).

**Left untouched, deliberately, both per `0260787`'s own disclosure:**

* `engine/rl_after/rl_app_data.json` — the engine-side copy Guard 5 does **not** assert; `bbD7.sh`
  deletes it from staging before every export, so it is never a build input.
* `data/rl_build/rl_app_data.json.srcmd5` — `source_md5` is the **store** (`cb38ef11`), and the store
  does not move in this act. It was already unequal to the committed board md5 before this act
  (pre-existing, disclosed, not created here).

## 3. WHAT THE RE-KEY BOUGHT — GUARD 5, BEFORE AND AFTER

Same command, same tree, the boot form (`run_panel.sh:17` / `bootstrap.sh:85`):

| | before | after |
|---|---|---|
| checkout `rl_model` | **RED** `98f16794 != 14000af2` | PASS |
| checkout `fv` | **RED** `6e9a370e != 2621b56a` | PASS |
| loaded-path `fv` | **RED** | PASS |
| `engine_head` read-path | **RED** `29376d5a != a353a9d3` | *expected now names `5f434b95` — the pin took* |
| loaded-path `v0surf` | **RED** `fbc5b393 != 5dd34ca8` | **RED, unchanged — out-of-repo cause, cannot be re-keyed** |

**Five failures became one**, and the one that remains has no pin to fix. Raw: `GUARD5_out.txt`.

---

**NOT ADOPTED. OWNER WORD PENDING.**
