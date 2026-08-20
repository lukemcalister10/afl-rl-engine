# THE BOOK RE-SEAL — HALTED, AND WHY

**Landing prep, order item 3. Nothing was guessed and no seal was written.**
`data/book_stable_seal.json` is **UNCHANGED** by this seat.

> The order: *"If the procedure is ambiguous or requires a decision not in the record, HALT that
> item and report rather than guessing."* That condition is met three times over. This file states
> each blocker, with the measurement that proves it rather than an inference.

---

## 1. THE PROCEDURE OF RECORD — FOUND, AND IT IS UNAMBIGUOUS AS A PROCEDURE

Recovered from the two committed re-seal instruments and from `ship_gates_check.py`'s B3 gate:

| source | what it is |
|---|---|
| `session_2026-07-17/legd_derivation/reseal_book.py` | the LEG D ACT-2 re-seal — the act that **last moved** `data/book_stable_seal.json`, at commit `2e49963` |
| `session_2026-07-15/captaincy/reseal_book.py` | the captaincy re-seal, same shape |
| `ship_gates_check.py` B3 (`:491-538`) | the gate that certifies the seal |

The steps, identical in both instruments:

1. Regenerate the walk-forward matrix with `engine/rl_after/s4_matrix_M1v7.py` **"EXACTLY as ship_gates
   B3 does"** — that is, under `RL_CONFIG_MODE=gate`.
2. Assert the matrix's embedded `__meta__` `engine_head_md5` / `store_md5` **== the candidate**.
3. Recompute `stable_sha256` over the stable-keyed content and **re-count `n_players`**
   (the historical language: *"book RE-SEALED for the new store (n re-counted)"*).
4. Rewrite `data/book_stable_seal.json` (`head_md5`, `store_md5`, `n_players`, `stable_sha256`, `config`).

**The mechanics are clear. What is missing is a decision about WHICH PRICE LINE step 1 runs on.**

Standing state, for context: the seal currently reads `head_md5 40f43772` / `store_md5 968de0c7` /
`config c2d233ae` / `n_players 2649`. The branch carries `5f434b95` / `cb38ef11` / `eed19a75`. The
book has not been re-sealed since **2026-07-17** — no order between Leg D and D7b moved it.

---

## 2. BLOCKER A — THE CANDIDATE'S DIAL LINE CANNOT ENTER GATE MODE  *(the decision not in the record)*

The candidate `a05fe951` is defined by an 18-dial environment line. **Every one of those dials is
`default '0'` in engine code** (verified: `_merged_recover.py:735 _O43=os.environ.get('RL_O43','0')!='0'`,
`:676` `RL_O42`, `:580` `RL_O41_R3`, `rl_model.py:1089` `RL_O37`) and **none is in
`data/model_config.json`**. Gate mode's reject scan (`config_manifest.py:93-100`) halts on any
`RL_*` var not in the manifest.

**Measured, not inferred** — `RESEAL_PROBE_out.txt`, ARM A:

```
============ CONFIG MANIFEST (gate mode) REJECTED — BUILD HALTED ============
  - UNKNOWN model override RL_O31='1' is not in the manifest (data/model_config.json)
  ... 28 lines, one per candidate dial ...
ARM A matrix produced: NO
```

**Why this is a decision and not a bug.** Every prior re-seal ran the manifest line legitimately,
because the levers of those chapters were **DECLARED KILL-SWITCHES wired default-ON into the engine
with the manifest deliberately unmoved** — `data/expected_boot.json` says so repeatedly in its own
notes: *"config c2d233ae UNMOVED (RL_EVW is a declared kill-switch, not a manifest dial)"*, and the
same sentence for `RL_CAPT`, `RL_ISOFADE`, `RL_PVC2`. Under gate mode those engines priced the
candidate line **by default**, so "the manifest line" and "the candidate line" were the same board.

**That identity does not hold here.** The O31–O43 dials are default-**OFF** and supplied by an env
line, so the two lines are different boards. The re-seal therefore forks, and neither fork is written
down anywhere in the record:

* **Fork 1 — seal the manifest line.** Mechanically legal, and it is what every prior re-seal did.
  But it seals a book for a board **that is not the candidate** (all O-dials off). Filing that as
  "the candidate's book" would be false.
* **Fork 2 — seal the candidate line.** Requires the 18 dials to enter `data/model_config.json`.
  That moves `config_sha256`, which moves the `config` pin in `expected_boot.json` — **the pin this
  very re-key just verified as already correct**, and the identity `a05fe951` was built under. It is
  a config bake: an owner-only act, explicitly out of this seat's scope, and it would invalidate the
  re-key it rides in.

**Choosing between these is a decision not in the record. This seat refuses to make it.**

---

## 3. BLOCKER B — THE BRANCH'S OWN FROZEN SURFACE CANNOT BE LOADED UNDER GATE MODE

`RL_V0SURF_PKL` is **not in `INFRA_ALLOW`** (`config_manifest.py:39-40`, which admits only
`RL_REPO`, `RL_APP_DATA`, `RL_FV`, `RL_ALLOW_PVCFIT_BOARD`, `RL_CONFIG_MODE`, `RL_VENV`) and not in
the manifest — so under gate mode it is rejected as an unknown override (measured, ARM B). Neither
committed `reseal_book.py` sets it.

With it unset, the engine's precedence resolves to `/home/claude/v0surf.pkl` (`fbc5b393`), **not**
the branch's `data/v0surf.pkl` (`5dd34ca8`) — the same footgun this order's item 2 probes. So the
re-seal **cannot legally load the surface the candidate was built on**. This is a second, independent
block, and it is the same out-of-repo cause.

---

## 4. BLOCKER C — THE STAGED ENGINE-SIDE BOARD PAIR IS INTERNALLY INCONSISTENT (PRE-EXISTING)

Measured, ARM B2 — the arm run **exactly as the committed instruments run it**:

```
SINGLE-SOURCE STARTUP GUARD FAILED (build HALTED):
  - GUARD 2 (source-hash assertion): rl_app_data.json stamped d9a24282... != current source md5 cb38ef11...
  - GUARD 1 (content-integrity): rl_app_data.json content md5 36d5dfc7... != stamped own_md5 88ce647f...
```

`engine/rl_after/rl_app_data.json.srcmd5` carries `own_md5 88ce647f` — **the LIVE board id** — while
the file beside it is `36d5dfc7`, and `source_md5 d9a24282` against a store of `cb38ef11`.

**This is pre-existing at `ba37032` and untouched by this seat** (`git status` shows this seat
modified only `data/expected_boot.json` and `data/rl_build/rl_app_data.json`). `bbD7.sh` sidesteps it
by deleting the staged board before every export; the re-seal instruments do not, so `s4_matrix`
halts at startup. Repairing that sidecar is a derived-artifact restamp nobody ordered, and doing it
silently to clear a path would be exactly the "reality bent to match" this order forbids.

---

## 5. WHAT THIS SEAT DID INSTEAD

* Ran the procedure on **both arms** and recorded the raw halts (`RESEAL_PROBE_out.txt`).
* Wrote **no seal**. `data/book_stable_seal.json` is byte-unchanged.
* Left the three blockers named, measured, and quoted.

## 6. WHAT THE SUPERVISOR MUST RULE, IN ONE SENTENCE EACH

1. **Which price line does the candidate's book seal on** — the pinned manifest line (mechanically
   legal, not the candidate) or the candidate's 18-dial line (requires a config bake that moves the
   `config` pin)?
2. **If the candidate line: is the config bake authorised**, and does it precede or follow the
   landing word, given it moves a pin this re-key just certified?
3. **Who repairs `engine/rl_after/rl_app_data.json.srcmd5`** (`own_md5 88ce647f` vs content
   `36d5dfc7`), which blocks `s4_matrix` at startup regardless of which fork is chosen?

A fourth question rides along and is not the book's: the `/home/claude/v0surf.pkl` shadow blocks
the re-seal as surely as it blocks the unbound build, and no in-repo procedure seeds or clears it.

---

**NOT ADOPTED. OWNER WORD PENDING. No tag, no main promote, the live board is untouched.**
