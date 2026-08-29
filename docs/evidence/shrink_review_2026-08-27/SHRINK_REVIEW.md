# THE MACHINERY SHRINK REVIEW — 2026-08-27

Owner word: "Please go" (2026-08-27, following the over-engineering critique of the same night).
Method: three independent evidence sweeps — (1) the full instrument inventory from code,
(2) a catch ledger mined from register entries v813–v880 + the incident index, (3) a cost
ledger of the combined-build landing night. Every claim below carries a register citation or
a measured timing. NOTHING on this list is implemented without the owner's word per item.

## DISPOSITION AS AT 2026-08-29 (added after the fact — the slots below were never filled in)

The per-item `**Your word: ____**` slots were left blank when the rulings came, so this document
still reads as twelve open questions when ten of them are settled and shipped. What follows is the
true state, each line carried by a citation in the code or the register — not by memory.

| Item | State | Evidence |
| --- | --- | --- |
| S1 — derive the moving-identity pins | **LIVE** | register v881 ("S1/S4/S11/S12 live") |
| S2 — retire the curve-mirror byte pins | **LIVE** | `engine/rl_after/one_source_selftest.py:520` ("shrink S2, owner word 2026-08-28") |
| S3 — book seal at bake acts only | **LIVE, via S10** | the seal is B3's baseline, and B3 is bake-scoped (`ship_gates_check.py:551`), so no landing asserts it |
| S4 — PREFLIGHT.json out of the pre-step-0 tree | **LIVE** | register v881 |
| S5 — delete struck gates' scoring code | **LIVE** | `ship_gates_check.py:331, 405` ("shrink S5, 2026-08-28") |
| S7 — selftest once per (spec, lander hash) | **LIVE** | `tools/landing/cli.py:119` ("SHRINK S13/S7, owner word 2026-08-28") |
| S9 — bare-build proof: verify-installed on retries | **LIVE, via S13 slice 1** | `tools/landing/steps.py:650` — the stash re-hashes the installed board against the prereg prediction instead of rebuilding |
| S10 — B3 freeze-stamp at bake acts only | **LIVE** | `ship_gates_check.py:367, 551` |
| S11 — three checks added to the step-0 battery | **LIVE** | register v881 |
| S12 — one-command pen | **LIVE** | register v881; every entry since v881 is filed through it |

**STILL AWAITING YOUR WORD — two items, and neither should be built without it.**

**S6 — collapse the identity-pin triplication.** Unruled and untouched: no `shrink S6` marker
exists anywhere in the code. It is the largest remaining item and the one that would have prevented
the five restamps the ORDER 49 flip needed (register v882), but it rewrites how release identity is
carried, which is the thing that guards everything else. The RL_-prefix namespace fix in
`carriers.py`'s header rides with it if you rule it.

**S8 — the sibling rebuild, identity-keyed ("S13 slice 2").** The mechanism already exists and is
proven: `tools/landing/proofstash.py` is generic in its `kind`, and the build proof (slice 1) has
been through a landing. Extending it to the sibling is a small change with a large saving — the
sibling reconcile is 54% of a landing's wall-clock (2,171s), and this build rebuilt it four times to
the same identity with three of the four deleted byte-exact by aborts. WHY IT IS NOT DONE ANYWAY:
slice 1 stashes a pure derivation (build a board, hash it, compare to the prereg prediction), while
the sibling step WRITES AND COMMITS to the repository. That is a genuinely different risk shape and
it carries its own decision slot, so it waits for you rather than riding in on S13's word.

## THE VERDICT

The estate carries **242 distinct verification instruments**. The recorded catch weight is
concentrated in about a dozen instrument families; a long tail has **zero recorded catches
ever** — every recorded firing was the instrument tripping over its own staleness (stale pin,
count bump, restamp, record-dirt). The sharpest finding: most of the cut list is not a
weakening of the rulebook — it is the rulebook's own **process law P4** ("assert the
relationship, never this month's number") finally enforced against the instruments that
violate it.

The cost exhibit: the combined-build landing took **11 takes / ~7.3 machine-hours**, of which
the productive take was 66 minutes. One retry was a real catch (take 5: a wrong engine
default headed for the live board — the bare-build proof earned its keep for the year).
Seven retries were machinery policing its own paperwork; three of those (takes 8/9/10) each
burned a ~55-minute build+sibling to reach a check that costs seconds and failed on a stale
pin, a hard-coded count, and an undeclared carrier.

## THE CUT LIST — one decision slot per item

### CUT / DERIVE (zero recorded catches; every firing was self-inflicted)

**S1 — Moving-identity pins in the movers test suites → derive from the lineage.**
Record: 0 catches; 4+ aborts/procedures (v823 all-five-weekly-pins trap, v837 "the eleventh
bump", v858 attempt 8, v880 take 9 — a pin that was structurally impossible to pass).
The P4 cure (boundary count derived from the register) is already proven in production; this
extends it to every remaining pin that tracks a MOVING identity (board/store/rounds/counts).
Pins on frozen history (the r19 store sentinel) stay. Saves: one abort class per landing +
the pre-bump procedure per advance. Risk: none identified — a derived check is strictly
harder to fool than a stale pin. **Your word: ____**

**S2 — File-md5 pins on the curve mirror (one_source_selftest `_contract_md5` + the
ui/release_pick_curve.json md5 fields) → assert the relationships instead.**
Record: 0 catches; take 8 burned 67 minutes on a stale mirror pin; a restamp chain with its
own filed precedent for restamping itself. The payload checks (curve == contract == engine
domain, pin1=3000, strict descent) all STAY — only the byte-md5-of-the-mirror-file pins go.
Risk: hand-edits to the mirror file's prose would no longer halt; the payload checks still
catch any value change. **Your word: ____**

**S3 — The book stable seal → re-seal at bake acts only, not asserted at every landing.**
Record: 0 recorded catches ever; chronic lag (v794, v818, v859, ~33-minute re-seals at v863
and again this build); one proven blind spot (v828: its sealed object silently drops rows —
the fire drill found that, not the seal). B3 can compare the committed book directly.
Risk: a book edit between bakes would surface at the next bake instead of the next landing.
**Your word: ____**

**S4 — PREFLIGHT.json out of the pre-step-0 tree.**
Record: takes 3+4 died on the record dirtying the tree it polices; the lock-holder line still
forces a per-launch commit ritual. Cure: file the record into evidence at the landing commit
(step 10), keep verdicts on stdout at launch. Zero verification lost. **Your word: ____**

**S5 — Delete the scoring code of STRUCK gates (B1, A9, A15); shelve PENDING gates
(A13/A14/C1/C2) off the board until built.**
Record: struck by your word already (B1 "that cohort rail again was retired"); they are still
scored and printed every run. P11 keeps the retirement note where each gate lived. B3's
timeout history alone cost carry-weeks (v849→v863). **Your word: ____**

**S6 — Collapse the identity-pin triplication (expected_boot / release_contract / mirror
stamps) to ONE stamped carrier + derived agreement.**
Record: the only "catch" in this family was the contract catching its own stale pins (v858
attempt 6); self-inflicted: take 1, the v828 tag whose own verifier rejects the tag's bytes,
the flip-completion restamp trio that exists only because three copies of one fact live in
three files. The manifest gate already COMPUTES truth from artifacts and checks carriers
agree — that stays as the enforcement. Risk: none identified beyond transition care.
**Your word: ____**

### SCOPE-DOWN (real value, wrong frequency)

**S7 — The 43-leg lander selftest: full run once per spec + lander-hash; skip on retries
where the lander and spec are byte-unchanged.**
Record: it proved the identical abort ladder ~10 times in one night (~1.7h); its one real
firing (take 2) was about its own sandbox base. The precedent is yours: v819/v820 "Skip it"
scoped build_twice out of transactions. Saves ~11 min per retry. **Your word: ____**

**S8 — The sibling rebuild: identity-keyed — rebuild once per (board, store, config)
candidate, verify-not-rebuild on retries.**
Record: 54% of every landing's wall-clock (2,171s); rebuilt 4× to the same identity this
build, 3 of 4 results deleted byte-exact by aborts. Its one recorded catch class (ambient
clock, v792/v794) was closed at the source. Saves ~36 min per retry. **Your word: ____**

**S9 — The bare-build proof: full proof on the FIRST flight of a candidate identity,
verify-installed-md5 on retries.**
Record: the night's one real catch (take 5) — this instrument is untouchable on first
flights. But takes 8–11 re-proved the same md5 four times (77 minutes). Any input identity
moves → full proof again. Saves ~19 min per retry. **Your word: ____**

**S10 — B3 freeze-stamp comparison → bake-time acts only.** (Pairs with S3.)
**Your word: ____**

### REORDER (extends an existing instrument; no new machinery)

**S11 — Extend the step-0 preflight battery with the three checks whose absence cost takes
8/9/10:** carrier-scope closure (every write the spec predicts is in the declared set —
take 10's class), ui-pin coherence read-only (take 8's class), and the two-world-safe gate
dry-run (take 9's class). The battery's own record (v863) says its ten sub-second checks
"would have prevented six of ORDER 45's nine failed attempts" — these three finish the job.
With S7–S9, a retry after an abort costs ~3 minutes instead of ~66. **Your word: ____**

### PROCEDURE MERGE

**S12 — One-command pen:** `pen.py append` runs index + incident-index + STATE + the
explicit-path commit in one flow (today: four commands and a push per entry, a procedure
born of its own misses — v822). Consolidation of existing steps into the existing tool.
**Your word: ____**

## WHAT STAYS, UNTOUCHED (the earned list)

Every instrument with a recorded real catch: the board verifier / named-row / residual
probes / preregistered censuses (five real catches in one week — the highest density in the
estate) · the blind review (ship-blocking catches both in-window uses) · Guard 5 + the
config manifest enforcement (four catches) · the bare-build and F1 two-world proofs (on
first flights) · the independent rebuild and the soak ("it has caught something real after
every single act") · the lander's atomic commit, abort-restore and explicit-path scope
(zero corruption across 21 takes) · B2/B4 · the dress-rehearsal and fire-drill pattern
(best catch-per-run ratio recorded) · the UI reader-side pin guards · every derived,
fail-closed assertion. The 12 laws and 13 process laws of the rulebook themselves: untouched
— the cut list is P4 enforcement, not law removal.

## PROJECTED EFFECT

- Retry of an aborted landing (same identity): **~66 min → ~3 min** (S7+S8+S9+S11).
- Last night, re-run with this list in force: ~7.3h → **~2.5h** with every real catch kept.
- Abort classes removed at the source: stale pin, count bump, record dirt, undeclared
  carrier (already fixed), restamp drift.
- Instruments retired or derived: ~45 of 242. Instruments with recorded catches touched: 0.

## NOT IN SCOPE OF THIS REVIEW

The already-filed speed items S1/S2 (bake-class preflight; walk-forward parallelization,
which would cut the FIRST flight from ~66 to ~40 min) remain filed separately. The
RL_-prefix namespace own-goal (four burns) has its named fix standing in carriers.py's
header — it rides with S6 if you rule it.
