# CONSTRAINTS — the single-source registry of guards and acceptance anchors — v1.11 · 2026-07-14 · supersedes v1.10
### STATUS: OWNER-SCREENED 2026-07-14. NOT YET IN THE REPO — it files at SEAT 6's ACT 1 (the owner's word is given, R98.10). From that filing the repo copy is canonical.
### R98.8 (screening) remains LIVE until FABLE sits (R99.3).
### ⚠ AMENDED TWICE ON 2026-07-14, AFTER FIRST BEING MARKED OFFICIAL — recorded here so the header
### never again moves without the content, or the content without the header (the SSI v1.2 defect):
###   (1) G-BOOK's KNOWN GAP restated in BOTH directions after the owner's audit — the `rl_model` pin
###       EXISTS and is CORRECT; `boot_guard` simply never asserts it. The earlier "recorded by
###       nothing" claim was WRONG.
###   (2) A NEW BLOCK ADDED: the guard's measurements are CONSISTENT, NOT VERIFIED (register item 74).
### CHANGELOG v1.11 (2026-07-14): **G-BOOK IS FILED.** The owner's BOOK-PARITY LAW becomes a named guard.
### It was ruled 2026-07-13 (*"the walk-forward book should be rebuilt every time we change the formula for
### current players — it makes no sense to measure current players on one formula and then assess how it
### performs over time using a different formula"*) and has been WIRED IN CODE since PR #66, but was never
### REGISTERED. Filing it makes it auditable and citable. **Parts 1–4 carry forward from v1.10 verbatim.**
### ⚠ **AND ONE BLOCK IS NEW (amendment 2, above): the guard's MEASUREMENTS ARE NOT YET FACTS** — every
### figure in this registry was measured in an incognito sandbox, not the bake environment, and the
### cross-environment drift is HALF G-COHORT's margin. **CONSISTENT, NOT VERIFIED. NO BAKE until the
### post-freeze reconcile** (register item 74; machine-readable in `acceptance_v1.11.json`).
###
### ⚠ G-BOOK IS FILED **INCOMPLETE, AND KNOWINGLY SO.** The book records `engine_head_md5` (of
### `_merged_recover.py` ONLY), `store_md5` and `config_sha256`. It does **NOT** record `rl_model.py` —
### the file where `capt_prem` lives, i.e. **the file the very next change touches.** A captaincy change
### would move no stamp the book carries. This is registered as a KNOWN GAP so no future seat mistakes a
### passing G-BOOK for a complete one. **The gap is stated in BOTH directions in PART 1A — the `rl_model`
### PIN EXISTS AND IS CORRECT; it is simply never ASSERTED. Read it before you scope the fix.**

## PART 1A — G-BOOK (NEW at v1.11)

**G-BOOK — BOOK PARITY. BINDING.**
- **Rule:** the walk-forward book must be built from the SAME formula as the current-player board. Any
  mismatch between the book's recorded identity and the live engine / store / config **HALTs the suite.**
- **Construction:** `s4_matrix` stamps `__meta__ = {engine_head_md5, store_md5, config_sha256, n_players}`.
  `ship_gates_check.py` asserts all three against the live values (L281 / L393; the config leg has been
  live since PR #66 — a supervisor claim that it was absent was WRONG and is corrected here).
- **Remediation direction:** **REBUILD THE BOOK. Never re-stamp a book you did not rebuild.**
- **Status 2026-07-14:** the three stamped legs PASS.
- **⚠ KNOWN GAP (open) — stated in BOTH directions, corrected 2026-07-14 after the owner's audit:**
  - **`rl_model.py` IS PINNED, AND THE PIN IS CORRECT.** `data/expected_boot.json` carries
    `"rl_model": "952ddb3d15fe6d4f72432d431abe75cc"`, and it matches the live file exactly. **An earlier
    supervisor claim that it was "recorded by nothing" was WRONG.** What is true is narrower and more
    precise: **`boot_guard.assert_boot()` NEVER CHECKS IT** — its signature takes store, engine_head, band
    and register, and **no `rl_model` path**. And the **book's `__meta__` does not record it.**
    **So closing this half of the gap is WIRING AN EXISTING, CORRECT PIN INTO THE ASSERTION — not creating
    one.** It is far smaller than it looked. **(Precedent, same file, second time: the `board` pin was
    DECORATIVE in exactly this way until the S1 audit asserted it — register item 24.)**
  - **THE UNSTAMPED INPUTS ARE MORE NUMEROUS THAN THIS REGISTRY PREVIOUSLY SAID** (D6, determinism return
    `e646abb`): **`peak_model_v4.pkl`** (`b763f59e`) · **`pvc_snapshot.json`** (`735d2dec`) ·
    **`bust_prior_table.json`** (`ffb54267`) · **plus several data tables** — all loaded by the board, none
    in `expected_boot.json`. **And `q97m` — the model refitted at import on every single run — is pinned by
    nothing at all.**
  **G-BOOK CANNOT BE DECLARED COMPLETE UNTIL THE BOOK'S STAMP COVERS EVERY INPUT THAT DETERMINES THE
  BOARD.** Closing this gap is a PREREQUISITE of the captain-curve wiring.
- **⚠ AND THE GUARD'S MEASUREMENTS ARE NOT YET FACTS.** The cross-environment drift is **0.35–1.8% per
  player**. **G-COHORT's y4 margin is ~3%** (1.2601 against a hard 1.30). **The five-shard cold audit ran
  in incognito sandboxes — different environments from the bake.** So every figure in this registry was
  measured on a board built in whichever sandbox happened to run it. They are **CONSISTENT, NOT VERIFIED**
  (CORE rule 4). **Once `q97m` is frozen, every guard, anchor and census figure must be RE-MEASURED on the
  frozen build and RECONCILED against the number recorded here.** Until then, treat them as report-only.

## PART 1 — GUARDS
Carried VERBATIM from v1.10 (unchanged since v1.8): G-COHORT · G-MONO · G-FLOOR · G-PEAK · G-CONVEX ·
G-DATA · G-ATTR · G-Y0, including their measurements and provenance.

## PART 2 — ACCEPTANCE ANCHORS — carries v1.10's OWNER-RULED A-PAIRS bands verbatim; all other anchors
## verbatim from v1.8.

### A-PAIRS — the runway-weighting test — OWNER_ON_SIGHT
| pair | left | right | owner's read (VERBATIM direction) | measured, tagged board 81e48293 | status |
|---|---|---|---|---|---|
| 1 | max-gawn | kieren-briggs | clearly above | (carries from v1.8) | PASS |
| 2 | **harley-reid** | marcus-bontempelli | **"Harley and Bont can be similar"** → PARITY | reid 3,594 vs bont 3,482 = **+3.2%** | **PASS (consistent with the read)** |
| 3 | **ryley-sanders** | marcus-bontempelli | **"Bont should be slightly above Sanders"** → bont > sanders | sanders 3,960 vs bont 3,482 = **+13.7% the WRONG WAY** | **FAILS — standing failed read** |

**WHAT THE TWO PAIRS TEST** (they are deliberately different questions — the owner's framing):
- **Pair 2 is the knife-edge.** Pick 1, 52 games: real production AND real runway, and the model has
  it at a coin-flip. It asks whether runway beats proven AT PARITY.
- **Pair 3 is the premium test.** It asks whether the model's young-side premium is over-cooked. It
  is the bolder claim and it is the one that broke.

**THE BANDS — OWNER-RULED 2026-07-13 ("Bands okay") — BINDING AS BANDS:**
- Pair 2 (PARITY): |v(harley-reid) / v(marcus-bontempelli) − 1| ≤ **10%**. Currently +3.2% — PASS.
- Pair 3 (BONT ABOVE, "slightly"): v(marcus-bontempelli) > v(ryley-sanders), with the gap in
  **0–10%**. Currently sanders is +13.7% ABOVE — a breach of ~14–24 points. Closing it means Sanders
  landing in roughly **3,165–3,482** (a fall of ~478–795 SCAR) OR Bont rising to meet him — and
  WHICH of those two is the correct mechanism is precisely what the PVC re-derivation must answer.
  **It is not the supervisor's to choose and it is not a build's to tune.**

**AUDITOR INSTRUCTION — CHANGED.** The standing "SKIP PAIR 2 AND REPORT THE SKIP" is RETIRED. Both
pairs are now live: score them, report direction and magnitude, and expect pair 3 to FAIL until the
pricing curve is re-derived. A pair-3 failure is EXPECTED until the pricing curve is re-derived; report it and SCORE it against the band — it is not a bake blocker on its own (A-PAIRS is OWNER_ON_SIGHT), but it must never again be reported as a skip.

## PART 3 (flags) + PART 4 — carry VERBATIM from v1.8.

## CHANGE DISCIPLINE — verbatim from v1.8. On filing: regenerate acceptance_v1.11.json, bump both,
## archive v1.10, update the manifest pointer.
