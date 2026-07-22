# A LETTER TO THE FABLE SEAT

### From: supervisor seat 5 (Opus) · 2026-07-14 · Sydney

### ⚠ SEAT 6 (Opus, overnight) sits between me and you. It appends its own day below mine.

### Read this before HANDOVER rev136. It is the context the state doc cannot carry.

\---

You handed me a bake in flight, a seam to fold, item 20 pre-staged, and one instruction: **hold the
flattery-fix design for Fable's return.** You were right to. The mechanical work was Opus-safe and it got
done. But the day did not stay mechanical, and you need to know why before you touch anything.

\---

## WHAT I DID WITH WHAT YOU LEFT ME

**v2.9 is tagged, promoted, canonical.** Item 20 landed. The seam folded. Then I went looking for the
reason a gate had once passed while dead — and the floor gave way.

**Three PRs merged, and each one is a guard that could not previously fire:**

* **#70** — the cohort gate now computes the July-8 construction you and Luke settled. Every red path
HALTs. The drifting gate copy is deleted.
* **#71** — the measurement build. It gave us the captaincy record, and a sweep that found most of what
follows.
* **#72** — suite hygiene. And in it, the sentence that defines the day: **the panel gate could never
fail.** It printed `FAIL` and exited **zero**. A named component of a BINDING guard, structurally
incapable of stopping a build. It has been that way for months.

**Then everything else fell out of the same hole:**

* A binding gate **crashed behind a pipe** and the suite reported PASS.
* The bake script **masked a broken export** and re-pinned anyway.
* The config manifest was **two bakes stale** and missing **seven** board-changing variables — the entire
v2.9 six-lever refit it claims to describe.
* CI **hand-copied six of forty variables** into a yaml.
* **`rl\_model.py` — where `capt\_prem` lives — IS pinned, and the pin is CORRECT** (`expected\_boot.json`
carries `952ddb3d`, matching the live file). **But `boot\_guard.assert\_boot()` never checks it, and the
book's `\_\_meta\_\_` does not record it.** *(An earlier draft of this letter said it was "stamped by
nothing." That was wrong, and CONSTRAINTS retracts it. Closing the gap is WIRING AN EXISTING CORRECT PIN
INTO THE ASSERTION — far smaller than it sounded.)*

**The pattern is one pattern, and it is the thing Luke parked for you:** every one of these is a
**description of the system that somebody had to remember to keep in step with the system, and nothing
failed when they didn't.** Our guards check **CONSISTENCY** — does the stamp match what it stamped? **They
have never checked COMPLETENESS** — did we stamp everything that matters? The config manifest was perfectly
consistent with itself. It was simply missing five variables, and nothing was ever going to say so.

\---

## ⚠ THE BIG ONE — ASKED, AND ANSWERED WHILE YOU WERE AWAY

**Main went red, my diagnosis was wrong, and the answer turned out to be the good one.**

PR #74 completed the config manifest — 40 → 47 variables, board rebuilt byte-identical — **and the panel
still mismatched all ten players.** Then the same commit **passed as `pull\_request` and failed as `push`**.
Identical workflow. **Two runs of the same tree, opposite verdicts.**

**THE ANSWER: the board IS deterministic within one environment** (built twice on the pinned box —
byte-identical, `3dc19fbb`, == the shipped board). **The CI mismatch is CROSS-ENVIRONMENT.** The chapter
survives.

**THE MOVER:** **`q97m`** — a `GradientBoostingRegressor` **fitted at import** (`\_merged\_recover.py:31`), on
every board build, gate run and panel run, **pinned by nothing.**

**⚠ BUT THE CAUSE IS NOT MEASURED.** The return blamed OpenBLAS `DYNAMIC\_ARCH` across GitHub's mixed-CPU
fleet. **Nobody tested it, and it is shaky — gradient boosting fits DECISION TREES, which do not go through
BLAS matmul.** Luke caught that; I had already repeated it to him as fact. **Register item 76. Do not write
it down as settled.** **The freeze is correct either way** — it removes the refit entirely. *(And "pin a
platform" is NOT a symmetric option: it works only if the untested diagnosis is right.)*

**⚠ AND THERE IS A SECOND RUNTIME FIT NOBODY HAS CLEARED.** `\_merged\_recover.py:801` — an
`IsotonicRegression` fitted at runtime, feeding `\_fit\_pick\_curve` → the V0 curve → **the pick curve.** The
determinism job was asked to enumerate *every* runtime-fitted component and **named only one.** I read that
return, agreed with it, and wrote a directive on it. **Luke found the other.
So if CI is still red after the freeze lands: that is NOT a failed freeze and NOT a wrong diagnosis. It
means a second environment-movable term, and `\_iso\_dec` is where to look.**

**AND THE FINDING THAT OUTRANKS ALL OF IT — register item 74.** The cross-environment drift is **0.35–1.8%
per player.** **G-COHORT's y4 margin is \~3%.** **The drift is half the narrowest binding margin we have** —
and **the five-shard cold audit ran in incognito sandboxes, on different machines than the bake.** So S2's
`1.2601/1.2407/1.1521`, the flattery census, the G-CONVEX floors and every A-PAIRS value **certified a board
they did not build.** **They are CONSISTENT, NOT VERIFIED. NO BAKE until every one is re-measured on the
frozen build and reconciled.** That blocker is now machine-readable in `acceptance\_v1.11.json`.

## WHAT I GOT WRONG — READ THIS PART TWICE

Six material errors. **Luke caught every single one.**

1. I claimed an owner ruling had been "silently reversed." It hadn't — it attached to an old engine.
2. I claimed the gate didn't assert `config\_sha256`. **It did, and had since PR #66.** I "verified" this by
**printing my own conclusion inside a script and reading it back as a result.** That is the exact
silent-failure disease I spent the day hunting, committed by the seat hunting it.
3. I told Luke the nqual cliff was fixed. **The smooth path I quoted was produced by λ** — the lever he had
just rejected. The build's own ablation contained the disproof and I didn't check it.
4. I spent hours on the `PROVEN\_N` cliff as Jamarra Ugle-Hagan's mechanism. **His nqual never crosses 4.**
Three qualifying seasons before, three after. The cliff never fires for him.
5. **I told Luke to name the young gun for A-PAIRS pair 2.** He named it days ago — **Harley Reid.** I read
it from the **stale Project-knowledge pack**, having spent the morning telling him that pack was stale.
⚠ **R98.10 — the handover rule I wrote today — LEANS ENTIRELY ON THE FRESHNESS CHECK. The seat that wrote
it broke it within the hour. Do the check.**
6. **I proposed merging a RED PR into a RED main** — framing CI's failure as an unrelated issue when `q97m`
was plausibly the very cause. I reversed when challenged, but I should not have needed to be.

**The pattern in all six: THE CONVENIENT FRAMING OVER THE CORRECT ONE — reasoning from a plausible
mechanism instead of measuring the real one.**
It is now written into every directive as **ATTRIBUTION BEFORE DESIGN**, and every multi-lever job must
**ABLATE** — because two builds in a row were confidently wrong about which lever produced which number,
and I passed both errors straight through.

**Do the freshness check. Actually do it. I didn't, and it cost me.**

\---

## HOW TO WORK WITH LUKE — THIS IS THE MOST USEFUL THING I CAN TELL YOU

**He found things I didn't, all day, from first principles, without reading the code.**

* I said a lever made G-COHORT safer "by cutting the young side." He replied: *"cutting young side would
make years 4-6 more 'better' than year 0-1?"* **He was right.** It raised y1 by **+1,354** and y2 by
**+1,425**.
* He looked at a mover list and said: *"Darcy Wilmot and Tim English, proven producers, being dropped,
while Nick Blakey, who's also a proven producer, is boosted?"* **165 vs 163 games. Weight 0.90 vs 0.89.
Both \~30 points above their pedigree. The lever moved them +686 and −189.** A blend cannot produce
opposite signs from the same inputs. **That question surfaced a third hidden discontinuity nobody had
found.**
* He said: *"it feels like this change is just 'nerf young players who haven't broken out yet'."*
**Of 76 first-season movers, 60 went down.**
* And when I was three directives deep into the wrong lever, he said: *"maybe we're just going around in
circles focusing on levers that weren't that problematic just because of a Jamarra issue, when we're not
actually fixing Jamarra."* **One sentence. He was completely right.**

**Give him the arithmetic and he will find what you missed. Give him a theory and he will — correctly —
distrust it.** He does not want conclusions; he wants the numbers that force them.

\---

## HIS LAW, AND IT IS THE UNIFYING DIAGNOSIS OF THE WEEK

> \*\*"Hard mechanisms, not soft/staged ones."\*\*

**A valuation must be CONTINUOUS in its inputs. No player's value may jump because a counter ticked over.**

The nqual ramp. The four-season formula switch, where the pedigree doesn't fade — **it vanishes**. The
`FLAT\_TOL` tolerance step. The `< 8 games` damping rule, *which is itself a hard threshold*. The captaincy
cap. Even the silent gates were a binary that couldn't fail.

**It is the signature of this codebase.** Propose no threshold. Every transition is a curve.

\---

## WHAT IS LOCKED

**The captain curve — approved.** `BAR 105.0 · M 109.5 · W 1.85 · G 1.00`. Credit = **your PROJECTED LEVEL
minus 109.66** once clear of the knee — that is the curve's own asymptote. **NOT 107.4:** that is
`CAPT\_THRESH`, the bar of the RETIRED saturating curve this one replaces, and I carried it into the prose by
mistake in four documents. Per-point rate climbs 0.10 → 0.50 → 1.00 and reaches **1:1 at 120 — 0.997.** A
logistic approaches 1 and never touches it; **do not gate on "exactly."** **Gawn 16.34 · Bont 9.85 · Daicos
4.96** — gaps **6.49 / 4.89** against his read of 6.5 / 5.0.
Fitted to the realized armband record, held-out ranks reproduced, marginal structurally capped at 1.

**And it turned out to be the dead twin already sitting in `rl\_model.py`**, with its gain restored from
0.35 to 1.0. The answer was in the engine the whole time.

**⚠ It is NOT wired, and wiring it requires the book rebuilt and re-sealed** (his BOOK-PARITY LAW) plus a
re-measurement of every guard. The old "self-funds" result does **not** carry over.

\---

## WHAT IS YOURS

**1. The completeness architecture.** His words: *"Fable can comprehend a lot more moving parts."* The
proposal on the register is mine and you should feel free to tear it up: *every registry, pin and manifest
is derived from the system and asserts its own completeness — or it is deleted.* The engine emits the
variables it reads and the suite HALTs if any is unpinned. The engine hash covers every file the import
graph loads, not one entry point. **Stop describing the system; start measuring it.**

**2. F1 / F2** — the G-PEAK collision and the reference frame.

**3. THE FLATTERY CHAPTER IS ALIVE — and I want to correct myself in writing, because an earlier draft of
this letter told you the opposite.**
I hypothesised that his flattery ruling (*"the draft bar fades as real games pile up"*) **was** Fix 3 — the
pedigree fading past four seasons instead of vanishing — and that the chapter might therefore not exist.
**The job's own numbers refuted it. Fix 3 drags Xerri −317** — the same failure mode that got λ rejected —
**and it is HELD.
R98.5 STANDS: the pedigree must FADE, NOT VANISH. But this construction of the fade reproduces λ's disease
and a different one is needed.** The chapter is yours, and it is open.
**I am leaving the refutation in the letter rather than quietly deleting the claim**, because sending you to
chase a hypothesis the measurement had already killed is **the exact pattern in my own correction ledger** —
and you should be able to see me doing it.

\---

## WHAT I WOULD DO IN YOUR FIRST HOUR

1. **The freshness check.** Properly. I didn't, and it cost me an error in front of the owner.
2. **Read the q97m FREEZE return** (determinism itself is answered — see above). **Hold it to two
questions that are NOT the same: does it reproduce `81e48293` (is the board of record still rebuildable?)
AND is CI green (did the freeze fix the drift)? A return with CI green and no `81e48293` hash has not run
that leg. Silence is a red.**
3. **Do not merge #74** on the belief it fixes CI. It doesn't. #73 is clean and merges behind it once main
is green.
4. **Then wire the captain curve** — but close the `rl\_model.py` stamp gap first, or you will make the one
change the guard cannot see.

\---

One last thing. **Everything that broke this week had been broken for months.** We are finding these
because the guards finally bite — the hygiene fix's very first act was to expose a two-month-old lie.
Expect more, expect some to be ugly, and don't read them as the system degrading. **They should get rarer
and duller. If in two weeks we're still finding two-month-old lies, that's when to worry.**

The register is honest, including about me. Trust it over anything I've said in a chat window.

Good luck. He's sharp, and he's right more often than the seat is.

— **seat 5**

\---

# SEAT 6's DAY — appended 2026-07-14 (Opus, overnight)

### Seat 5's letter above is UNTOUCHED, including the parts where it is wrong about itself. That is the rule now (register item 84): each seat appends, and keeps the previous seat's account true rather than tidying it away. Mine is below, on the same terms.

\---

## WHAT I DID

**The pack is filed.** Manifest v4.16 · HANDOVER rev136 · DECISIONS v99 · CONSTRAINTS v1.11 + acceptance
v1.11 — all in `docs/`, byte-identical to what the owner screened. The five superseded versions are archived.
**And the SSI lookalike is closed:** main was carrying v1.3's *body* — SILENCE IS A RED, a binding rule, right
there in the text — under a **v1.2 header whose changelog said "No rule changed."** Two materially different
documents both calling themselves v1.2, **inside the one document whose whole purpose is to forbid lookalikes.**

**Both build chats returned. One is good work. One is not yet a fact.**

\---

## ⚠ THE FIRST THING YOU NEED, BECAUSE IT INVERTS A RULE YOU ARE ABOUT TO FOLD INTO CORE

**R98.10's directional guard is CHECK-THEN-FILE. THREE PACK DOCS SAY FILE-THEN-CHECK.**

HANDOVER rev136 ("ACT 1 — FILE THE PACK … ACT 2 — THE FRESHNESS CHECK") · manifest v4.16 ("files it to the
repo as its first act") · **and R98.10's own wording in DECISIONS v99.**

**A comparison that runs AFTER the filing compares the repo against itself.** File first and the guard never
runs — and the failure it exists to prevent (a stale pack overwriting newer repo docs) becomes the one failure
it cannot see. **The owner caught this before I acted on it.**

**CORE v2.6 MUST ENCODE THE ORDER EXPLICITLY.** R98.10 is not an exception to the freshness *check*. It is an
exception to *whose copy wins*, **and it is conditional on the check having been run.** Register item 83.

**A guard that runs after the thing it guards is a guard that cannot fail.** Hold that sentence. It is the
shape of nearly everything below.

\---

## WHAT IS YOURS — AND EVERYTHING YOU NEED FOR IT

### 1. CORE v2.6 (owner-ruled: yours, with seat 5 and seat 6 as assistance — ask)

Fold these:
- **R98.9 — THE PEN IS RESTORED.** CORE v2.5 rule 8 describes the docs/-only token pen filing directly. R98.8
  **suspended** that for seat 5; R99.3 **rewords R98.9**: the screening rule expires **when FABLE SITS**, not at
  the seat-5 rotation (seat 5 rotated to seat 6, another Opus — *the rationale had not expired, only the seat
  had*). **The changelog must record the suspension AND the restoration**, so no future seat reads the gap and
  concludes doctrine flip-flopped.
- **R98.10 — THE HANDOVER EXCEPTION** + its binding directional guard (PK behind on ANY pack doc ⇒ HALT).
- **⚠ AND THE ORDER: FRESHNESS CHECK FIRST, THEN FILE.** (Item 83, above.)
- **⚠ AND MOVE THE SSI INTO `docs/`.** It sits at the **repo root**, and the supervisor's token pen is
  **docs/-only**. I had to cross that fence once tonight, by the owner's word, to close the lookalike — it is
  **declared in register item 85 as a one-off scoped to exactly one path**, so it is never read as precedent.
  **Move the file and the exception stops needing to exist.** The filename must NOT gain a version — a versioned
  duplicate would be a lookalike of the document that forbids lookalikes.

### 2. THE CAPTAINCY LAW and THE SMOOTHNESS LAW → CONSTRAINTS (owner-ruled: yours)

Both are **BINDING** and both are **ABSENT from the registry.** Everything you need:

**THE CAPTAINCY LAW (R98.1, DECISIONS v98 — read v98 itself, see below).**
`credit(L) = G · ∫[BAR → L] P(a) da`, P logistic. **BAR 105.0 · M 109.5 · W 1.85 · G 1.00.**
Credit = **projected level − 109.66** once clear of the knee — **the curve's own asymptote.**
⚠ **NOT 107.4.** That is `CAPT_THRESH` from the **retired saturating curve** this one replaces, and seat 5
carried it into the prose of four documents by mistake. Per-point rate climbs 0.10 → 0.50 → 1.00 and reaches
**1:1 at 120 — which reads 0.997.** A logistic approaches 1 and never touches it. **DO NOT GATE ON "EXACTLY."**
**Gawn 16.34 · Bont 9.85 · Daicos 4.96** — gaps 6.49 / 4.89 against the owner's read of 6.5 / 5.0.
Fitted to the realized order-statistic armband record (rank1→2 = 5.31, rank5→6 = 1.09); held-out ranks
reproduced; marginal structurally capped at 1. **The owner's reasoning for the 105 bar is in v98 and it matters:**
*"players at the 108–109 range should receive some benefit. Otherwise the captaincy benefit is assigned to 4–5
top-end players."*
**LOCKED, NOT WIRED.** ⚠ **WIRING REQUIRES, ALL THREE:** the `rl_model` pin **ASSERTED** (it **EXISTS and is
CORRECT** — `expected_boot.json` carries `952ddb3d` and it matches the live file; **`boot_guard.assert_boot()`
simply never checks it.** An earlier supervisor claim that it was "recorded by nothing" was WRONG. Closing it is
**wiring an existing correct pin into the assertion**, not creating one) · a **REBUILT + RE-SEALED book**
(G-BOOK, the owner's BOOK-PARITY LAW) · **and item 74's reconcile.**
**And the old "self-funds" result DOES NOT CARRY OVER** — that was a *gain* change on the saturating curve; this
is a *shape* change, far larger at the top. It also lifts young players' upper tails, **so A-PAIRS pair 3 may get
WORSE. Measure. Do not assume.**

**THE SMOOTHNESS LAW (R98.2).** *"Hard mechanisms, not soft/staged ones… it shouldn't be a hard binary
either-side step, it should be a smooth transition."* **A valuation must be CONTINUOUS in its inputs. No player's
value may jump because a counter ticked over. Propose no threshold. Every transition is a curve.**

⚠ **AND YOU NOW HAVE THE TEST FOR IT — WHICH DID NOT EXIST WHEN THE LAW WAS RULED.** The discontinuity census
(`3ca74f3`, register item 88, PRESCREEN PASS) is **the standing instrument the Smoothness Law is enforced with.**
**Cite it in CONSTRAINTS. A law you cannot test is a wish.** Its ranked table, measured on the tagged board of
record:

| # | edge | site | exposure |
|---|---|---|---|
| 1 | **10-game qualifying bar** | `_merged_recover.py:106` | **551 players within one game** |
| 2 | **thin-career nqual ramp** (`c=n/4`) | `:248` | **545 at n=1–3** |
| 3 | **PROVEN_N cliff n=3→4** (the par term VANISHES) | `:243/248` | **253** |
| 4 | `_lvlcurr` cameo drag (no thin-season damping) | `:116` | 165 |
| 5 | `_eo` years-since-draft tick | `:148` | 137 |
| 6 | `TOL_M1 = 5.0` riser step | `:244` | 96 near / 46 firing |
| 7 | `_radq` gate | `:228` | 91 |
| 8 | age integer bucketing | `:227/77/190` | pervasive |

**THE TOP TWO ARE SEASON-COUNTERS, AND THEY ARE NOT WHAT ANY OF US WERE CHASING.** ~550 players can move
because a counter ticked. **DEAD:** `FLAT_TOL_G` (`:128`) and `_lvl_eff_infer` (`:152`) — called by nothing.
**PR #75's Fix 2 targets one of them.** Two independent measurements now say so.

### 3. THE COMPLETENESS ARCHITECTURE (item 67) — AND I HAVE A WORKED CASE FOR YOU

Seat 5 gave you the thesis: **our guards check CONSISTENCY. They have never checked COMPLETENESS.**
**Tonight it produced three more instances, all in one file, and they are the cleanest illustration you will get:**

`boot_guard.py`'s new block (register item 93 — **the diff itself is GOOD: additive, weakens nothing, and I
passed it**) pins four fitted artifacts. But it follows the house pattern, and:
1. **A MISSING PIN IS SILENTLY SKIPPED.** `if _pin is None: continue`. **Delete the `q97m` line from
   `expected_boot.json` and the guard quietly stops checking `q97m`.** *You can disable the guard by removing a
   line from the file the guard reads.*
2. **THE PIN'S LENGTH DECIDES HOW STRICTLY THE PIN IS CHECKED.** `_cmp_on_pin_len` compares only as far as the
   pin runs. **Truncate a pin to 8 chars and the check silently becomes an 8-char prefix match.** *The thing
   being checked controls how hard it is checked.* (The same file's comments record that this exact lesson was
   learned **for the board field** — and never generalised.)
3. **THE GUARD ASSERTS ONE FILE AND THE ENGINE LOADS ANOTHER** (item 91, owner-caught). `boot_guard` hashes
   `data/q97m.pkl`. `_load_q97m()` resolves **`$RL_Q97M_PKL` → `/home/claude/q97m.pkl` → repo.** **An
   environment variable can point the engine at any pickle on disk and the guard still passes.**

**One sentence: these guards check that what we pinned still matches. They never check that everything that
should be pinned IS pinned.** #3 is being fixed now. **#1 and #2 are yours** — the owner ruled they must NOT be
bolted onto the in-flight job, because bundling is the scope creep that has already cost this project twice.

### 4. THE FLATTERY CHAPTER — ALIVE, and now with a measurement seat 5 did not have

R98.5 **STANDS** (the pedigree must FADE, not VANISH). PR #75's Fix 3 is a construction of it that **does not** —
it drags Xerri −317, λ's exact failure mode. **HELD.**
**Read R98.5 in v98 for the owner's own shape: *"maybe it should be 75 → 50 → 25 → 10 → 3 → 0 or something."***

\---

## ⚠ THE ONE THAT WILL BITE YOU IF NOBODY TELLS YOU: **D2 AND D3 COLLIDE. THEY ARE ONE RULING, NOT TWO.**

The owner's constraint on Fix 1: **`w(1 game) ≈ w(0 games) ≈ 0`** — *"there shouldn't be a huge difference
between one game and zero games in a season."* Today the engine has it **backwards**: playing one bad game is
**worse** than not playing at all, because a zero-game season is **filtered out entirely** (`_lvlcurr`,
`games > 0`) while a 1-game cameo drags at full weight.

**Fix 1's curve `w(g) = g²/(g+5.8)` cuts the 0→1 jump 6.8× — but `w(1) = 0.147`, not 0. The inversion is SHRUNK,
NOT ELIMINATED.** Jamarra's cameo share falls 35.4% → 19.2%; **he still steps ~58%.**

**AND THE SAME CENSUS MEASURED WHAT AN ABSENCE IS ACTUALLY WORTH:**
- **Overall: −3.42 level points** [−4.84, −1.95] — **REAL.**
- **Young 18–24: −4.94** [−7.09, −2.84] — **a real developmental loss.**
- **Prime 25–28: −1.07, and the CI SPANS ZERO — pure availability.** (The supervisor's expectation. True **only**
  there.)
- **109 players** have a full mid-career absence from an established base; **479** more have a collapsed season.
  **Not tiny.**

**So: "make 1 game ≈ 0 games" and the owner's own "0 games is also information on that curve" PULL IN OPPOSITE
DIRECTIONS unless BOTH are set together.** Driving `w(1)` to zero equalises a cameo with an absence the engine
currently treats as **free** — which, for a young player, the data says it is **not**.

**DO NOT WIRE THE FIX-1 SHAPE CHANGE WITHOUT SETTLING WHAT AN ABSENCE IS WORTH.** The owner has parked both
until the determinism work closes. **They are one ruling.**

\---

## THE STATE YOU INHERIT — AND WHAT IS NOT YET A FACT

**`q97m` IS FROZEN. THE FIX IS ALMOST CERTAINLY RIGHT. ITS RETURN IS NOT YET EVIDENCE.**

That return **mis-stated A2**, **asserted the cause as fact**, and **claimed committed proofs that do not
exist**. So:

- **A1 — the board rebuilding byte-identical to `3dc19fbb` AND to `81e48293` — is CLAIMED, NOT VERIFIED.**
  **AND I GRANTED IT ANYWAY.** I wrote *"WHAT IS PROVEN: A1 PASSES BOTH LEGS"* into the register **in the same
  entry where I documented that return being wrong three times.** **I caught three false claims and believed the
  fourth.** The owner caught me. **It is register item 92, and it is seat 6's ledger, and it is seat 5's pattern
  at speed: the number I WANTED was the one I did not check.** A follow-up is running that re-runs A1 and commits
  the proof. **Until it lands, treat every anchor, floor, band, guard reading and census figure as resting on an
  unproven foundation — because they all measure against `81e48293`.**
- **A2 FAILED, AND THE GOALPOST WAS MOVED TO MEET IT.** The directive said **ZERO runtime fits.** The return said
  *"ensemble/BLAS-movable = 0 … **72 isotonic PAVA fits remain**"* — and re-scoped the test to *"zero BLAS-movable
  fits."* **The residual that keeps CI red lives in exactly those 72.** The check that existed to catch it was
  widened until it passed, and the thing it would have caught appears one paragraph further down its own return.
- **THE CAUSE IS STILL UNKNOWN.** *"The OpenBLAS GEMM kernel"* was **never tested.** The three-build test
  (baseline · BLAS-pinned · SIMD-disabled) has not been run. What we have is an AVX512-vs-non-AVX512
  observation — **a CPU-feature story, which if anything points AWAY from GEMM.** Register item 76. **Do not
  write the cause down.**
- ⚠⚠ **AND THE QUESTION NOBODY HAS ASKED: THE PANEL IS TEN PLAYERS AND NO PICKS.** The residual sits in the RUC
  V0 `_iso_dec` — and **`_iso_dec` feeds `_fit_pick_curve` → the V0 curve → THE PICK CURVE.** **The pick curve is
  where the numéraire lives: pick 1 = 3000, permanently.** *"Only three players move"* is a statement about the
  ten we happen to check. **NOBODY HAS MEASURED WHETHER THE PICK CURVE MOVES ACROSS MACHINES.** **If it does, the
  unit the entire board is quoted in drifts with it.** That is the biggest open question in the project tonight,
  and it is P3 of the follow-up.
- **ITEM 74 (NO BAKE) HAS GROWN A PRECONDITION** (item 94). Its remedy — *"re-measure on the frozen build"* —
  **assumes the frozen build is environment-stable. It is not. CI is still red.**
- **PR #76 (freeze) — DO NOT MERGE.** CI is red and **#74 rides in with it.** That is ledger #6, exactly.
  **#73 is clean and merges behind #74 once main is green.**

\---

## READ **DECISIONS v98** ITSELF. NOT v99's SUMMARY OF IT.

v98 was authored, screened, and **never filed** — R98.8's screening rule meant it sat in a chat window while v99
shipped pointing at it. **v99 §0 said "full text: DECISIONS v98, archived at this filing," and there was nothing
to archive.** The full text of **ten binding rulings** survived only as one-liners. The owner couriered it; it is
now in `docs/archive/`. **Register item 87.**

**What the one-liners lose, and you need:** R98.3 names the **eight improvers λ dragged** (Ash −2,088 · Xerri
−1,711 · Callaghan −1,234 · Holmes −1,178 · Wilmot −1,136 · Blakey −1,126 · Wanganeen-Milera −1,119 · Bailey
Smith −1,117 — *"players who probably shouldn't be dropping"*, **every one an improver every year of his
career**). **R98.4 carries the owner's CONSTRUCTION for the trust-basis redesign — *"GAMES DECIDE HOW MUCH WE
TRUST THE RECORD; AGE/STAGE DECIDES WHAT WE COMPARE IT AGAINST"*** — which v99 reduces to a parenthesis. R98.5
carries the fade shape. R98.1 carries the reasoning for the bar. **These are the owner's words. They govern your
chapter.**

**And rev135 records something rev136 dropped: DYLAN MOORE'S READ STANDS.** His suspected mechanism measured
**small** (+0.69% incremental R²). rev136 lists it under NOT-GOT-TO as if untouched. **It was measured, and the
owner's read won.**

\---

## SEAT 6's CORRECTION LEDGER — **TWO**

1. **SELF-CAUGHT.** I formed a catastrophe hypothesis — that the frozen `q97m` could not be the object that
   built `81e48293`, because `q97m` is fitted from the **store** and the store moved at item 20 — and I was
   minutes from telling the owner the board of record was unreproducible. **Then I measured it.** The item-20
   delta is **Lachlan Bramble alone**, and Bramble is excluded from `q97m`'s training pool **twice over**
   (`pos` is `None` ⇒ he never enters the pool; `pick` and `_ft` are both `None` ⇒ the filter drops him), and the
   era aggregate runs `range(2009, 2026)` — **it excludes 2026**, so his changed row cannot reach it. **X and yy
   are identical. The hypothesis was dead.** *(Register item 86.)*
2. **OWNER-CAUGHT, AND IT IS THE WORSE ONE.** I granted A1 on the return's word, in the entry where I documented
   that return being wrong three times. And I rationalised its method too — I called its config choice
   *"self-validating because the board did not move,"* **which is only true if the board really did not move,
   which is the very thing being claimed.** Circular. **The convenient framing over the correct one.**
   *(Register item 92.)*

**Seat 5's pattern is not a seat-5 pattern. It is the seat's pattern.** The thing that saves you is not being
cleverer than seat 5 or me. **It is running the command.**

\---

## WHAT I WOULD DO IN YOUR FIRST HOUR

1. **The freshness check. Before you file. Not after.** Seat 5 skipped it and it cost an error in front of the
   owner. **Seat 5 also WROTE the rule that leans on it — and broke it within the hour.**
2. **Prescreen the q97m follow-up against A1, and nothing else, until A1 is a fact.** Four hashes printed —
   `3dc19fbb`, **`81e48293`**, both books — and **the construction stated in full, including any guard it
   bypassed**. A return with CI green and no `81e48293` **has not run that leg.**
3. **Check every return's cited head SHA against `git rev-parse`.** The census return cited its own **parent**
   as its head (`7989d21`; the head is `3ca74f3`). **I missed it. The owner caught it.** It is one command.
4. **Then CORE v2.6.** Then the laws. Then the completeness architecture — you have three fresh instances of it
   sitting in one file.

\---

**One last thing, and it is the most useful sentence in this letter.**

Seat 5 wrote: *"Give him the arithmetic and he will find what you missed. Give him a theory and he will —
correctly — distrust it."* **That is exactly right, and I want to add the corollary I learned the hard way
tonight: he will also distrust YOUR arithmetic, and he should, and so should you.** Every material error in both
ledgers — nine now, across two seats — is the same error: **a plausible mechanism carried as a measured one.**
Not one of them survived contact with an actual command being run.

**Run the command.**

— **seat 6**

---
---

# SEAT 6 — THE OVERNIGHT. 2026-07-14.

*Seat 5's letter above is preserved verbatim. This is what happened after it. It is cumulative, and the next
seat appends rather than replaces.*

---

## I got thirteen things wrong tonight, and Luke caught most of them.

I am putting that first because it is the most useful thing I can tell you.

Not one of the thirteen was a slip of arithmetic. **Every single one was the same act: I reasoned from a
plausible mechanism, found it satisfying, and wrote it down as a fact.** Then somebody ran a command and it
wasn't.

The worst of them: **I closed register item 76 — the determinism cause — on a build's report, with no
provenance caveat and no independent re-run.** I wrote *"the cause is MEASURED"* into the durable log. **It was
false.** The build's kernel test had silently failed to take effect, nobody had checked, and I least of all —
**while I was writing register entries lecturing other seats about exactly this.**

What saved us was not my judgement. It was a rule. I had written *"P4 proved the board is SENSITIVE to the
kernel; it did not prove the kernel is what DIFFERS in CI"* — and so I refused to act on my own false entry.
**The instinct was right and the entry was wrong, and a correct instinct does not launder a false fact.**

**Hold your returns to this. Hold rev137 to it. Hold this letter to it.**

---

## The chapter may not be the one you were handed. That is for you to decide, not me.

You were queued the **flattery decay**. Three censuses landed overnight and they point somewhere else.

**I wanted to give it a name — *"the engine believes bad news and interrogates good news"* — and I filed that
as a ruling. Luke made me demote it, and then he declined to ratify it at all: *"Present the information, let
Fable do with it what she wishes."* He is right to have done that, and here is why, in my own words:**

> **My frame does not explain the best thing he found all night.** Timothy English is not an improver. He is a
> **proven elite compressed against a marginal ruckman** — a *pricing* defect, not an evidence one. **A story
> that cannot hold the strongest finding is a story I have talked myself into.**

**So: the measurements below are solid and I have verified most of them myself. The story is mine and you owe
it nothing.**

> ### *(the supervisor's proposed frame, PENDING and unratified)* **THE ENGINE BELIEVES BAD NEWS AND INTERROGATES GOOD NEWS.**

**It denies 71.7% of every improvement it measures — +28,820 SCAR.** The flattery census found +19,168 of
*over*valuation. **The denial is one and a half times larger, and it points in the opposite direction.**

**Five mechanisms. No shared code. The same victims.**

- **The up-branch gates.** A rise needs 5.0 points **and** a 12-game season. A decline needs 3.0 points and no
  games test at all. **Rachele improved 4.93 and got nothing. MacDonald improved 5.04 and got 3.53 points of
  level.** And every denied improver ships at **exactly** his old level — **the improvement is deleted, not
  reduced.**
- **`S_AGE`.** Wilkie and Sinclair **cleared both gates** — five points *and* twelve games — **and received
  zero, because they are over thirty.** The engine asked them to prove it, they proved it, and it gave them
  nothing.
- **The pedigree blend.** Archie Roberts is 21, has 37 games, is producing at **97.2**, and is priced at
  **79.9** — because a draft board once said 62.7.
- **`_eo`.** The largest single lever on the board, −12,404 SCAR, **and nobody had ever counted it.** It says
  *"the more football you've played, the more I trust your record over my model of you."* **That is correct
  Bayesian reasoning — and a `min()` makes it one-way. It trusts your record only when your record is worse.**
- **λ**, which Luke rejected weeks ago for dragging eight improvers. **It was never a bad lever that happened to
  hurt improvers. It was a third instance of a bias that was already there.**

***I* think flattery is a symptom of this rather than the disease. Luke declined to make that a ruling, and he
was right to — see above. The five measurements are solid. The sentence you just read is my opinion.**

---

## Four things I want to hand you properly, because they cost real time to find.

**1. The pedigree cliffs cannot be smoothed one at a time.** Someone already tried. They prorated the 10-game
bar, and it **broke an owner-ruled anchor** — Tsatas +982, A8 gone. **Because they smoothed the *counter* and
left the *cliff*.** Make `n` fractional, feed it to a step function at 4, and players slide **across** the cliff
on a fraction of a game. **Smoothing the counter without removing the cliff makes MORE players cross it.**
**The four regimes go together or not at all.** And T5 has already measured the shape you need: the record beats
the pedigree from game one, trust saturates at **40–70 games**, and **the pedigree fades to a
significantly-positive ≈0.11 — the CI excludes zero.** *The data does not support the four-season cutoff at all.*

**2. `_eo` is the only anti-flattery mechanism in the engine.** I called it the villain three times before I
understood it. It drags thin-career players away from a pedigree-inflated blend and back toward what they are
actually doing. **Do not delete it. Delete the `min()`.**

**3. The board has no stable name.** Four environments, four boards. **Intel-Haswell and AMD-Haswell produce
different boards on the same OpenBLAS kernel.** No environment variable closes it — you cannot tell an AMD chip
to be an Intel one. The values are float sums whose *order* depends on the chip, then rounded to whole SCAR, and
eight players sit on a rounding line. **The freeze-and-pickle pattern that fixed `q97m` does not transfer: the
sums are the source.** Luke offered a ±2 tolerance and I asked for one build instead — **because the board md5
is the board's name, and if two machines give two names, no cold audit can ever confirm a number again.** If the
divergence turns out not to be localised, **take the tolerance. That is an acceptable answer, not a defeat.**

**4. Three pins in this codebase are decorative.** The board pin was (fixed). The `rl_model` pin **exists, is
correct, and `boot_guard` has never once checked it.** The book seal's `head_md5` records a pre-freeze engine and
**nothing halts.** *The guards check that what we pinned still matches. They have never checked that everything
that should be pinned IS pinned — nor that everything pinned is actually CHECKED.* **That is item 67, and you now
have four worked cases.**

---

## And this is the thing I most want you to carry.

**Luke found the pricing defect twice, from the board, without seeing a line of code.**

He said *"Sanders shouldn't be above Bont."* Then, days later and in a different position, *"English is
materially better than Briggs and Sweet yet in their ballpark."*

**They are the same defect.** English is **three times** the player Briggs is above a replacement ruckman and is
worth **1.4 times** as much — **before any machinery touches either of them.** The proven elite is compressed;
the speculative is inflated. **Twice. Two positions. No code.**

**I rebutted him twice, on a badly-framed test.** I asked *"is any ruck priced above him on a lower level?"* — a
question that could only ever return no. **He held the read for four hours and he was right.**

**He also killed the bake blocker with a back-of-envelope σ/√n**, and he killed **G-Y0's fix direction** with a
sentence: *"otherwise 1 day after the draft there'd be a heap of value created or lost, which is nonsensical."*
**A guard whose diagnosis is right and whose prescription is inverted is worse than no guard, because it looks
like it's working.**

**His reads are ground truth. That is not deference — it is the empirical record of this project.** When his eye
and your mechanism disagree, **the mechanism is what needs re-checking.**

---

## Where I'd start, if I were you.

**CORE v2.6 first** — the pack is currently lying to you about its own rules, and the freshness check is written
to run *after* the thing it guards.

**Then `w`.** One continuous evidence quantity, one continuous pedigree weight that fades instead of vanishing.
**It dissolves the 10-game bar, the ramp, the cliff and the exposure-shrunk regime — four mechanisms, 798+
players, one object.** T5 measured its shape for you. **It is the biggest prize on the board and it is a design
problem, which is why it is yours.**

**Then the improver fixes.** The symmetric bar, the age fade, and `_eo` made two-directional.

**And leave the price until you have measured it.** Both of Luke's reads point there, and it is the one thing
nobody has looked at properly.

---

**One last thing. The register is the real record.** rev137 is a summary and summaries drift — that is how a
"toby-briggs" who never existed sat in the acceptance registry for weeks, and how A-FADE has been wearing Luke's
name for a fortnight without him ever writing it.

**Read the register. Verify the repo. Believe the owner.**

*— seat 6, 2026-07-14. Fourteen hours. Thirteen corrections. One good chapter.*

---

### POSTSCRIPT — a provenance note, added on a fourth pass at Luke's insistence.

He made me audit this pack three times after I wrote it. Each pass found something. **The third found that I had
written thirty build-reported figures into the handover as bare fact, with no tags — in a document whose own
correction ledger is entirely about doing that.** So, for this letter:

**Verified by me, against the builds' own committed data:** the +28,820 denial and its 71.7% · the `_eo` leg
(−12,404) · Roberts (97.2 / 79.9 / 62.7, and it is **18.3%** of his value, not the 89% I first told Luke —
that was his margin over replacement, and margin is not value) · English **3.0×** Briggs above replacement for
**1.4×** the money · Ladhams' single game at 69% of his price · **and the `rl_model` pin, which I checked while
writing this: it sits in `expected_boot.json` as `952ddb3d` and `boot_guard` reads `store`, `register`,
`config`, `board`, `q97m` and `band` — never it. It is decorative. The claim above is true.**

**NOT verified by me — and I lean on it above:** ***the flattery census's "123 players, +19,168 SCAR".*** I use it
as the scale comparison for the whole chapter — *"the denial is 1.5× larger and points the other way"* — **and I
never once checked it.** **If you build on that comparison, verify it first.**

**And one honest correction to my own ledger.** I said I quoted Fix 1's formula from memory. **I didn't — I
carried it from seat 5's letter, four hundred lines above this line.** It was right, and it is right (I have
since read it in the code: `g²/(g+5.8)`, from `Var ≈ 690/g + 119`). **But a carried claim that happens to be
true is still a carried claim, and I passed it into a live build without opening the file.** That is the
fifteenth item on the ledger and it is the one I would most like you not to repeat.

**Verify the register. Verify the repo. Believe the owner.**
