# THE STRIKES — A9 and B1, RULED BY THE OWNER, RECORDED IN THE INSTRUMENT

**Both reds the frozen suite raised on 2026-08-20 have been RULED. Both are RETIRED. Both are now
STRUCK, by the mechanism the suite already had.**

`docs/evidence/p1_safety_net_2026-08-20/1a_FINDING_frozen_suite_first_run.md` presented two reds and
said, correctly, that they were "model verdicts, not tooling" and "not P1's to rule". The owner has
now ruled on both. This act records those rulings where they belong — in the file that does the
asserting — and does nothing else to the estate.

**The rulings did not change the model. They recorded that the model had already been changed.**
Both legs had been retired BEFORE the run that raised them; see THE ZOMBIE MECHANISM below.

---

## THE OWNER'S RULINGS, VERBATIM (2026-08-20, in chat)

> **A9.** "Those player ordering assertions were retired and are outdated. Since they occurred, Ward
> has hit an excellent run of form."

> **B1.** "That cohort rail again was retired. Weeks ago."

---

## THE MECHANISM — FOUND, NOT INVENTED

The suite has carried a strike mechanism since **A15**, struck by the owner on **02/07/2026**. It is
three things, and A9 and B1 now use all three unchanged:

| | A15, since 02/07/2026 | how it works |
|---|---|---|
| in the code | `gate('A15', False, 'STRUCK', 'Luke 02/07/2026 — convexity dimension seeded as V_NEXT #1')` | a `gate()` call whose status literal is `STRUCK` |
| in the record | `SHIP_GATES.md` — "A15. STRUCK (Luke, 02/07/2026): …" with the owner's reason and the consequence logged | the written half; a strike with no reason is an erasure |
| in the arithmetic | `STRUCK` is not in `('FAIL', 'ERROR', 'HALT')`, so `_hard_fail` never sees it; it is counted in the board's `VERDICT:` tally under its own name | not counted against shipping, and never invisible |

`SHIP_GATES.md`'s verdict vocabulary already defined it: *"STRUCK — the gate was deliberately removed
by Luke (A15). Not counted."* That line now names three gates instead of one.

**A15's own line is byte-unchanged by this act** — asserted mechanically in `verify_strikes.py`. The
point of a mechanism is that it takes new cases without being rewritten for them.

---

## A9 — WHAT WAS DONE, AND WHY IT IS NOT NEW LAW

**Before:** `cmp_gate('A9', False, [('Ginnivan>Ward', 'Jack Ginnivan', 'Josh Ward')], …)` — the
generic greater-than helper, which renders `PASS` or `FAIL`.

**After:** a `STRUCK` gate that still resolves both players, still prints both values and their
ratio, and carries the owner's words, the register's prior pattern, and the zombie note in its
detail line.

### The register's prior pattern: SCORED, NEVER FLAGGED

This strike is **the pattern the register already recorded, finally made structural**. A9 was
converted to the scored-never-flagged disposition well before today, and is cited BY NAME in the
register as the precedent for handling pair 2 (item 265):

> "EXPECTED-FAIL-BY-LAW at v2.11 (**A9 Ginnivan/Ward precedent — the pair stays his law, the auditor
> scores it, never flags it; revisit on form/reads**) — supervisor-recommended"

Item 272's per-gate committed verdicts carry the same wiring by name ("the item-272
scored-never-flagged pair"). And `RULEBOOK.md` v2.1 PART 2 then retired the dated player reads
wholesale — **owner, 2026-07-22: "they've done their job"** — with the forward policy that "the board
is judged by the owner's eye at each release; new dated reads enter this file only on his word."

The revisit trigger the register named was **form**. Form is exactly what the owner cited today. The
instrument is doing what the register said it would; it simply never knew.

### What is preserved

The numbers. `A9 … STRUCK … SCORED (never flagged): Ginnivan=2198 vs Ward=2837 (retired assertion was
Ginnivan>Ward; ratio=0.775)`. If the owner's read moves back, the number is on every board run,
waiting. A strike removes the alarm, never the measurement.

If `E()` cannot resolve either player, the leg still emits a `STRUCK` verdict naming the failure —
**SILENCE IS A RED applies to struck gates too**. A struck gate that went quiet would be the item-38
defect wearing a new hat.

---

## B1 — SUPERSESSION, NOT REPEAL

**What is struck** is the **JULY-8 CONSTRUCTION**: raw class-year sums of Vpath, averaged unweighted
across the classes observed at each career year, denominator `min(y1,y2)`, each of y4/y5/y6 tested
individually against a hard `≤ 1.30`, a breach HALTing the suite. That is the 2026-07-13 instrument
(register v52), and it is what the owner means by "that cohort rail".

**What survives** is the class-discipline law itself, in the owner-signed governing document:

> `docs/RULEBOOK.md` v2.1 + its twin `docs/acceptance_v2_0.json`:
> `{"id": "G-COHORT", "status": "BINDING", "check": "walk-forward book ratio", "max": 1.3,
> "note": "UNMEASURED at R19 until harness migration rebuilds the book"}`

RULEBOOK PART 3 reports it **UNMEASURED** — *"never assumed passing, never silently waived"*. The law
is binding and honestly unmeasured; the rail that used to stand in for it is retired. The register
carries the same direction of travel: **item 51** ("THE G-COHORT FEAR IS RETIRED, AND THE REASON
MATTERS"), **item 60** (a gate inherited from a superseded line is retired with an obituary or
re-derived on the current engine — *"do NOT rule it"*), **item 266** (the two-sided G-COHORT band).

### NOTHING IS SUPPRESSED — this is the B5 disposition, not a mute

`SHIP_GATES.md` already governs this: *"FEATURE does NOT mask a red: the signal is not suppressed, it
is relocated to a visible, printed list (mispricings stay VISIBLE …)"*. B1's strike follows it
exactly:

- the full July-8 computation **still runs**, on the candidate matrix **regenerated this run**;
- every figure still prints — `y1 … y7`, the denominator and its source, all three ratios and their
  guide-band positions;
- the years that **would have breached** the retired 1.30 bar are still **named in the verdict line**
  (`would have BREACHED at y[4, 5, 6] — SCORED, NOT FLAGGED (struck)`);
- the per-class table and the demoted indexed SHAPE row still print on every board run.

Only the alarm is gone.

### Every B1 path renders STRUCK, including the old HALTs

The skip path, the missing-matrix path and the exception path were all `HALT`. All three are now
`STRUCK`. **A retired gate that can still red the build on a bad input has not been retired — it has
been made unfalsifiable instead.** The exception path still NAMES its exception in the verdict line,
because item-38's real requirement was never "HALT", it was "never silent".

### The red-path seam is unweakened

`SGC_B1_MATRIX` (the injected-matrix proof seam) still stamps B1 `INJECTED`, never a bare verdict,
and an injected run still **exits non-zero regardless of any gate's status**. There is still no path
by which a caller-supplied matrix yields a green, zero-exit certification. The strike changed the
off-seam disposition only.

---

## THE ZOMBIE MECHANISM — the part worth generalising

**Both retirements PREDATE the reds that raised them.** The owner's own words say so: "were retired
and are outdated"; "was retired. **Weeks ago.**"

The suite could not record either one, because the suite could not run. `ship_gates_check.py` was
bricked — first on its own `RL_GAMMA` line, then on the `:49` hardcode into a shared out-of-repo
workspace — and it executed **no gate at all** through exactly the period in which both rulings
landed. When P1 1a unbricked it, its first full run compared its state against snapshots taken before
the rulings and reported:

> **TWO REDS THAT ARE NEW AT THE CURRENT HEAD** … Both are marked `<- MOVED` by the suite's own
> three-column comparison: they PASSED at CONTROL and at PREVIOUS, and do not pass at CURRENT.

**They were not new. They were unrecorded.** The suite was telling the truth about its own snapshots
and lying about the state of the law, and it could not tell the difference. The cost was two rulings
the owner had to give twice and a finding document written to ask for them.

This is what a **revived instrument resurrecting retired law** looks like, and nothing in the estate's
process laws covered it. The proposed cure is filed as **P11** in
`docs/proposals/rulebook/AMENDMENT_1b_2026-08-20.md`:

> When a ruling retires or supersedes a gate, the retirement is recorded in the instrument that
> carries the gate **in the same act** — an instrument that cannot run still gets its strike
> recorded, so a revived instrument can never resurrect retired law.

Its falsifier: **a repaired instrument's first run produces no verdict the owner has already ruled
on.** The 2026-08-20 first run fails that test twice, which is what makes it the born-from incident.

---

## BEFORE / AFTER — the suite's own board lines

Both runs are the FULL suite against head `1867e953`, store `b745002e`, config `eed19a75f775`.

**BEFORE** (`docs/evidence/p1_safety_net_2026-08-20/1a_ship_gates_FIRST_FULL_RUN.txt`):

```
A9        PASS    | PASS    | FAIL     Ginnivan>Ward: 2198 vs 2837  <- MOVED
B1        PASS    | PASS    | HALT     JULY-8 construction (…): y1=62073.9 … y7=79201.6;
                                       den=min(y1,y2)=y1=62073.9; ratios y4=1.4262 y5=1.4418 y6=1.3965;
                                       hard<=1.30 -> BREACH at y[4, 5, 6] (HALT)  <- MOVED
VERDICT: FAIL=4  FEATURE=1  HALT=1  PASS=16  PENDING=4  STRUCK=1  (862s)
```

**AFTER** (`2a_ship_gates_AFTER_STRIKE.txt`, this act; full report `2a_ship_gates_report_1867e953.md`):

```
A9        PASS    | PASS    | STRUCK   Luke 2026-08-20 — player-ordering assertion RETIRED, verbatim:
                                       "Those player ordering assertions were retired and are outdated.
                                       Since they occurred, Ward has hit an excellent run of form." …
                                       SCORED (never flagged): Ginnivan=2198 vs Ward=2837
                                       (retired assertion was Ginnivan>Ward; ratio=0.775)  <- MOVED
B1        PASS    | PASS    | STRUCK   [STRUCK — Luke 2026-08-20, verbatim: "That cohort rail again was
                                       retired. Weeks ago." … SUPERSEDED by G-COHORT …] JULY-8
                                       construction (…): y1=62073.9 y2=68070.9 y3=78013.9 y4=88527.6
                                       y5=89498.0 y6=86685.1 y7=79201.6; den=min(y1,y2)=y1=62073.9;
                                       ratios y4=1.4262 y5=1.4418 y6=1.3965; RETIRED hard<=1.30 bar ->
                                       would have BREACHED at y[4, 5, 6] — SCORED, NOT FLAGGED (struck)
VERDICT: FAIL=3  FEATURE=1  PASS=16  PENDING=4  STRUCK=3  (537s)
```

**Every B1 figure is byte-identical to the run before the strike** — `y1 … y7`, the denominator, all
three ratios. The strike changed the disposition and nothing else; that is the evidence that the
measurement survived the retirement.

---

## THE FALSIFIER FOR THIS ACT: NOTHING ELSE MOVED

Three claims, each checked mechanically rather than asserted.

### 1. No other gate's verdict changed — `BEFORE_AFTER.txt`

`before_after.py` parses the board rows out of both full runs and diffs all 27 gates. Its verdict:

```
changed: exactly A9 FAIL->STRUCK, B1 HALT->STRUCK — and nothing else
standing fails A2/A3/A12 still FAIL, exactly as recorded (not swept)
before_after: PASS
```

It fails if the gate SET moves in either direction, if the changed set is anything other than those
two, or if any of A2/A3/A12 stops failing. The three standing fails are checked BY NAME because a
strike act that quietly tidied one would be a worse version of the thing this act exists to fix.

**The suite's own snapshot says the same thing independently.**
`data/gates_snapshots/gates_1867e953.json` is rewritten by every run under the D10 reporting rules;
diffed against its committed predecessor, exactly two of its 27 status fields changed — `A9` and
`B1` — and the gate set is equal. Two instruments, one written by the board printer and one by the
snapshot writer, agree.

### 2. The board of record is unmoved, proved by the suite itself

`B4 PASS — regenerated rl_app_data.json md5=68be10c7 vs shipped 68be10c7`. The suite rebuilt the
board from the checkout it was grading and got the shipped board byte-for-byte, on the run that
carries the strikes. `B3 PASS` likewise re-derived the book stable seal to the sealed baseline.

### 3. G1 — every value-bearing artifact byte-unmoved

`g1_BEFORE.txt` / `g1_AFTER.txt`. **All 20 value-bearing identity lines are byte-identical**: store,
board, engine head, rl_model, model config, the three fitted pickles, the LTI register, the RULEBOOK,
the twin, both UI bundles, all eight boot pins, the contract sha and the three book-seal fields.
`STRIKES_CLAIMS.json`, verified by `tools/claims.py`, is the same claim in checkable form.

This act touched no engine file, no store, no exporter, no data file and no dial.

> **ONE HONEST DIFFERENCE, NAMED RATHER THAN SMOOTHED.** The G1 script's first line is the HEAD
> commit, and it moved: `fb1dc3a → 813e5cd`. That is **not this act**. A CONCURRENT SEAT landed a
> docs-only evidence commit (`docs/evidence/movers_questions_2026-08-20/`, 8 new files, 0 changes to
> anything else) while this suite run was in flight. It is worth recording because it is the exact
> gap the build lock does not cover: the lock serialises ENGINE acts through the shared workspace,
> and a documentation commit neither takes it nor needs to. Every G1 line below the commit line is
> unchanged, which is what the falsifier is actually about.

**The suite still exits non-zero**, on A2/A3/A12. That is correct and is the point: striking two
retired legs did not turn the board green, and was never meant to.

---

## TWO TOOLING FACTS THIS RUN MEASURED, WORTH THE NEXT SEAT'S TIME

Neither is a defect in this act; both cost a run to discover and are recorded so they cost nobody
else one.

1. **`RL_BUILD_LOCK_HELD` trips the config manifest in gate mode.** The build lock's reentrancy
   marker is an `RL_*` name, and `config_manifest.enforce('gate')` rejects any unknown `RL_*` as a
   divergent model override — so running the frozen suite *through* `tools/build_lock.sh run` HALTs
   on the lock's own bookkeeping: `UNKNOWN model override RL_BUILD_LOCK_HELD=... is not in the
   manifest`. **This is the same defect class the `:49` repair already documented in this file**
   (its first draft used `RL_SGC_RA` and halted on its own repair, which is why the seam variables
   are `SGC_*`). Workaround used here, which weakens nothing: `env -u RL_BUILD_LOCK_HELD` on the
   child only — the flock is held by the parent shell's fd for the whole run; only reentrant
   re-acquisition inside the child is given up, and nothing inside the suite re-acquires.
2. **The suite needs `RL_REPO` set.** `data/v0surf.pkl` is resolved from `RL_REPO` /
   `CLAUDE_PROJECT_DIR` only, and `bootstrap.sh` does **not** seed v0surf into the workspace (it
   seeds `cm_400.pkl` and `q97m.pkl` only — the engine says so in its own HALT message). Without
   `RL_REPO` the run dies at the v0surf frozen-load HALT after passing Guard 5, which reads like a
   store problem and is not one.

**The invocation that works, recorded for the next seat:**

```
bash tools/build_lock.sh run <tag> -- \
  env -u RL_BUILD_LOCK_HELD RL_REPO=<repo> python3 ship_gates_check.py
```

(Guard 5 additionally requires the shared workspace to be seeded from the checkout —
`bash bootstrap.sh` under the same lock — or `SGC_RA` pointed at a workspace that already is.)
