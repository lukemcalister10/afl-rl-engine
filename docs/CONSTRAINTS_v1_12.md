# CONSTRAINTS — the single-source registry of guards and acceptance anchors — v1.12 (AMENDED) · 2026-07-14 · supersedes v1.11
### CHANGELOG v1.12 (2026-07-14, owner-screened and owner-worded):
###  (1) **L-SYMMETRY IS FILED** — the owner's evidentiary-symmetry law becomes a named, citable law (PART 5).
###  (2) **L-SAGE-FADE IS FILED** — S_AGE must FADE to a measured residual, never VANISH at 30 (PART 5).
###  (3) **G-Y0: PENDING_OWNER → ADVISORY** by ruling. ⚠ **THE v1.12 G-Y0 BLOCK PUSHED AT `c48d390` WAS WRONG
###      AND IS REPLACED HERE** — the supervisor's 'cost of holding' argument MISREAD `V0` (it is the player's value
###      the day AFTER the draft, ONE DAY from the pick's; there is nothing to discount). **THE OWNER'S IDENTITY
###      STANDS. What is stale is the FIX DIRECTION — it was drafted for the OPPOSITE breach.**
###  (4) **A-FADE: basis APPROVED (multi-bake ARC) — and its PROVENANCE is marked UNVERIFIED.**
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


## PART 5 — LAWS (NEW at v1.12)

**L-SYMMETRY — THE EVIDENTIARY BAR IS SYMMETRIC. BINDING. Owner-ruled 2026-07-14.**
- **Owner's wording (VERBATIM):** *"Risers should have the same smoothing/ramping. And you should have to have
  the same drop for the engine to think you're declining as a rise for it to think you're rising."*
- **Rule:** the engine must require **THE SAME WEIGHT OF EVIDENCE** to believe a player has IMPROVED as to
  believe he has DECLINED, and must deliver **BOTH** through **CONTINUOUS RAMPS** — never a threshold on one
  side and a ramp on the other.
- **THE ASYMMETRY IT CORRECTS (measured, board `3dc19fbb`):**
  - A **RISE** requires **≥ 5.0 points** (`TOL_M1`) **AND** a **12-game season above the old level** (`_radq`).
    **Fail EITHER and the ENTIRE improvement is DELETED — not reduced. All 124 denied improvers ship at
    EXACTLY their old level (`core == Lo`).**
  - A **DECLINE** requires **3.0 points** (`DOWN_TOL`) and **NO games test at all**, and is then delivered by a
    **SMOOTH RAMP**.
  - **⇒ RISERS FACE CLIFFS. FALLERS GET A RAMP.** Josh Rachele improved **4.93** and received **nothing**;
    Connor MacDonald improved **5.04** and received **3.53 points of level**. **Eleven hundredths of a point.**
- **MEASURED COST: +28,820 SCAR DENIED TO IMPROVERS — 71.7% of ALL measured improvement** (`S_AGE` 14,637 ·
  `TOL_M1` 12,268 · `_radq` 1,915). **For scale, the flattery census found +19,168 of OVERvaluation. The
  DENIAL is 1.5× LARGER AND POINTS THE OTHER WAY.**
- **⚠ RELATIONSHIP TO R98.2 (THE SMOOTHNESS LAW): L-SYMMETRY IS STRICTER.** Smoothness forbids the CLIFF.
  **L-SYMMETRY ADDITIONALLY FORBIDS AN UNEQUAL BAR.** **Two smooth ramps with different thresholds SATISFY
  R98.2 AND VIOLATE THIS LAW.**
- **Status:** **BINDING. NOT YET WIRED.**

**L-SAGE-FADE — AGE DISCOUNTS IMPROVEMENT; IT DOES NOT ABOLISH IT. BINDING. Owner-ruled 2026-07-14.**
- **Rule:** the age-persistence discount on an improvement (`S_AGE`) must **FADE TO A MEASURED RESIDUAL**. It
  **MAY NOT REACH ZERO** on the assertion of a curve nobody has tested at that end.
- **Today:** `_S_AGE(a)` interpolates 0.915(20) → 0.490(25) → 0.151(28) → **0.000 FROM AGE 30, FOREVER.**
- **THE INDEFENSIBLE CASES:** **Callum Wilkie (+406) and Jack Sinclair (+143) CLEARED BOTH EVIDENCE GATES** —
  ≥5.0 points **AND** a 12-game season above their old level — **and received EXACTLY ZERO, because of their
  birthdays.** **The gates and `S_AGE` ask the same question twice ("is this improvement real?") and the AGE
  test OVERRIDES the EVIDENCE test completely. That is not scepticism; it is a rule that cannot be satisfied.**
- **PRECEDENT (the same disease, already measured):** the draft pedigree still carries a
  **significantly-positive ≈0.11 residual at n=4** (CI **[0.04, 0.17] — EXCLUDES ZERO**) — **and the engine
  zeroes it anyway** (`PROVEN_N`). **VANISH-WHERE-IT-SHOULD-FADE is a pattern in this codebase, not an
  accident.**
- **Remediation:** **MEASURE the 30+ residual. REPLACE the asserted zero with the measured fade.**
  **NOBODY HAS EVER TESTED WHETHER THE ZERO IS REAL.**
- **Status:** **BINDING. NOT YET WIRED. The measurement is the first job.**


## PART 6 — STATUS AMENDMENTS (v1.12)

**G-Y0 — PENDING_OWNER → ADVISORY (owner-ruled 2026-07-14). THE IDENTITY IS SOUND. **THE PRESCRIBED CURE IS
POINTED BACKWARDS.**
⚠⚠ **THIS BLOCK REPLACES A WRONG SUPERVISOR ANALYSIS PUSHED AT `c48d390` AND CORRECTED BY THE OWNER WITHIN THE
HOUR. THE ERROR AND ITS CORRECTION ARE BOTH RECORDED, BECAUSE THE WRONG VERSION WAS BRIEFLY BINDING.**
- **THE SUPERVISOR'S ERROR:** it argued that a pick *should* be worth LESS than the player, because the player
  peaks in 5–8 years — **"the gap is the cost of holding."** **IT MISREAD WHAT `V0` IS.**
- **THE OWNER'S CORRECTION (2026-07-14, VERBATIM):** *"if we're talking about picks and the players immediately
  post draft (i.e. pure v0 players), then they should be relatively even on average... Because otherwise 1 day
  after the draft there'd be a heap of value created or lost which is nonsensical."*
- **`V0` IS THE PLAYER'S VALUE THE DAY *AFTER* THE DRAFT. THE PVC IS THE PICK'S VALUE THE DAY *BEFORE*. THEY
  ARE ONE DAY APART. THERE IS NO HOLDING COST BETWEEN THEM AND NOTHING TO DISCOUNT.** **They must be equal, or
  the draft MANUFACTURES VALUE OUT OF NOTHING and no rational owner would ever sell a pick.**
  **THE NO-ARBITRAGE ARGUMENT IS EXACT. THE IDENTITY IS THE OWNER'S AND IT STANDS.**
- **THE HOLDING-COST QUESTION IS A DIFFERENT COMPARISON** — *pick vs the player's PEAK/CAREER value* — where the
  owner's other point **does** bite (*"how do you value the players? Peak career value? A range of samples
  across their peak? It's a bit arbitrary."*). **THAT COMPARISON IS NOT G-Y0. DO NOT WELD THEM TOGETHER AGAIN.**

**THE IDENTITY, AS THE OWNER STATES IT:**
- **CLAIM 1:** position conditioning **REDISTRIBUTES, never LEAKS.** A defender below the curve is paid for by a
  midfielder above it. **Deviations NET TO ZERO.**
- **CLAIM 2:** the composition-weighted mean `V0` **EQUALS the derived PVC.** **BOTH CLAIMS ARE THE OWNER'S.**
- ⚠ **AND THE OWNER'S POSITIONAL CAVEAT IS PART OF THE LAW, NOT AN EXCUSE FOR IT:** *"acknowledging that some
  drafts will be positionally weaker and as a result be below the PVC, while others may be positionally strong
  and therefore above it."*
  **⇒ THE IDENTITY HOLDS *ON AVERAGE ACROSS DRAFTS*, NOT DRAFT-BY-DRAFT. A SINGLE CLASS LANDING OFF THE CURVE IS
  NOT A BREACH — IT IS A WEAK OR A STRONG CLASS. G-Y0 MUST THEREFORE BE MEASURED ACROSS MULTIPLE DRAFTS.**

**⚠⚠ THE FIX DIRECTION IS STALE AND MUST NOT BE APPLIED.**
**MEASURED (2026-07-13, the v2.9 seam table): comp-weighted `V0` > derived PVC in EVERY band (+19…+281, widest
at picks 21–30). THE PLAYERS ARE WORTH MORE THAN THE PICKS. THE DRAFT CREATES VALUE.**
**G-Y0's recorded `fix_direction` is `raise_young_side_never_cut_survivors_never_bend_derived_curve`.**
**⇒ THE YOUNG SIDE IS ALREADY THE HIGH SIDE. RAISING IT WOULD *WIDEN* THE GAP.**
**WHY: the remedy was drafted on 2026-07-11 anticipating the OPPOSITE breach** — the supervisor's note that day
read *"the weighted average sits BELOW the curve broadly."* **The measurement came back the other way and NOBODY
UPDATED THE REMEDY.** **The PVC re-derivation must re-derive the CURE, not only the numbers.**
**ADVISORY, by owner ruling — scored and reported, not blocking, until the pricing-curve chapter.**

**A-FADE — BASIS APPROVED (owner 2026-07-14). ⚠ PROVENANCE UNVERIFIED.**
- **BASIS: APPROVED — the multi-bake ARC, not the single-bake tick.** *(Owner: "I'm happy to be loose on
  A-FADE... Arc makes sense.")* **A fading player can tick UP one bake on noise while declining across two
  years; demanding a tick-down every bake would fail the anchor on noise and teach us to ignore it.**
  **`basis_status` PENDING_OWNER is CLOSED.**
- ⚠ **PROVENANCE: UNVERIFIED. The owner (2026-07-14): *"I don't think I wrote that guard."*** What IS
  owner-worded is the **2026-07-08 clarification** (a player already at the scrap floor satisfies FLAT). **The
  FOUR NAMES predate it and THEIR AUTHOR CANNOT BE ESTABLISHED FROM THE HISTORY.** It has been carried as an
  owner read regardless. **PRECEDENT: A-GAWN's comparator had drifted to `toby-briggs` — a player who does not
  exist, origin unknown — and sat in this registry for weeks.** **CORE rule 4: provenance-tag every carried
  claim. This one is now tagged.**
