# STOP — STEP 3. THE YEAR-0 BASIS THE RESOLVED CANDIDATE'S NO-ARB TABLE MUST USE IS NOT DETERMINED

**ORDER 30B-N.** Brief: #334 comment 5310246218. Filed against `PREREG_30BN.md` §2, which fixed the
basis *before* the run and is the reason this was caught rather than absorbed.

**The order's own rule is being followed: "Any wiring question the resolution arithmetic does not
determine: STOP and report."** The resolved law is wired, proven and built. What is not determined is
the **denominator** the owner's table divides by.

---

## 1. WHAT HAPPENED

The Step-3 re-emit halted, fail-closed, inside the ORDER 29C emitter:

```
ORDER 29C HALT (replication): 43 of 89 wired entrants reproduce the board's printed day-0 at
tolerance 0. ... The year-0 column is only the landed law if it reproduces the law's own published
output EXACTLY; a partial match is a DIFFERENT law and must not be emitted as this one.
```

**THE HALT IS NOT CAUSED BY THIS ORDER'S DIAL. That was tested, not assumed.** The identical emit was
re-run on the identical HEAD worktree with `RL_O30B_RESOLVED` unset:

| run | dial | result |
|---|---|---|
| `emit_variant_o30bn.sh O30BNRES` | `RL_O30B_RESOLVED=1` | HALT, 43 of 89, `exit=1` |
| `emit_ctl.sh` (same emitter, same worktree, same pins) | **unset** | **HALT, 43 of 89, `exit=1`, same mismatch list** |

The emitter's replication proof reads `_landed_v0_board()`, which resolves
`pvc_curve_v2.json::nd_v0.posv` and `MA.pool_v0_of` — **neither of which any 30B dial touches**. The
halt is a property of the branch, not of the resolved candidate.

## 2. THE CAUSE, NAMED

`DAY0_29B_FINAL.json` — the emitter's pinned replication reference — was published on board
`36d5dfc7` against the **then-current** `pvc_curve_v2.json`.

That artifact has since moved **exactly once**, at commit
**`860d370` — "ORDER 30B STEP 1: THE POSITIONAL v0 RE-FIT — A2 CURED, 107 ASCENTS → 0"**
(`git log -- engine/rl_after/pvc_curve_v2.json`; current md5 `06146b00`, unmoved since).

So **ORDER 30B's own Step 1 moved the year-0 object out from under the ORDER 29C emitter.** The
emitter is behaving exactly as designed: it refuses to emit a year-0 column that no longer reproduces
the law's published output.

## 3. THE SIZE OF THE MOVE — MEASURED, NOT ASSERTED

**The 89 wired entrants (the emitter's own proof population):**

| | |
|---|---|
| reproduce exactly | **43 of 89** |
| moved | **46** |
| move: min / median / max | **−10.98% / +0.34% / +455.82%** |
| mean absolute move | **17.94%** |

**The 2,648-record emit population (`per_entrant_O29CFINAL.json`, the 29C landed-law basis):**

| | |
|---|---|
| comparable rows | 2,643 (0 unmapped) |
| mean v0, 29C basis | 518.18 |
| mean v0, Step-1 re-fit | 519.00 |
| **pooled denominator move** | **+0.158%** |
| **rows whose v0 moved** | **1,441 of 2,643 — 54.5%** |
| per-row move, p05 / median / p95 | **−5.92% / +0.00% / +13.51%** |

**The pooled denominator barely moves; the per-row denominator moves a great deal.** Both cohort
instruments aggregate as `mean(value at year N) / mean(v0)` over the *same* set, so the pooled figure
is the one that scales the headline margin — but the 54.5% row churn and the ±6–14% tails are what
make the RESOLVED column non-comparable to the LIVE and SITALL columns **row for row**, which is
precisely what the owner asked to see side by side.

## 4. THE TWO OPTIONS, AND WHY THE SEAT WILL NOT PICK ONE

**OPTION A — keep year-0 on the frozen 29C landed entry law.**
Preserves the common denominator with LIVE (`88ce647f`) and the SITALL preview, so the three columns
stay comparable. **Cost:** the numerator's pedigree object (`day0_v0`, post-re-fit) would then be a
*different object* from the denominator — which reintroduces exactly the **MIXED-BASIS defect ORDER
29C was created to close** ("a landed-law numerator over a pre-landing denominator", `emit_matrix_29c.py`
header). It also requires freezing an artifact the engine no longer computes.

**OPTION B — move year-0 to the current re-fitted v0.**
Internally coherent: numerator and denominator on one object, which is arguably what "the landed entry
law" *means* under the current engine, and the brief does contemplate re-pointing identities that have
moved. **Cost:** the denominator moves for 54.5% of rows, so the RESOLVED column's margins are no
longer the same measurement as the LIVE and SITALL columns beside them. It also requires re-pointing
`RL_DAY0_FINAL` — **the very fail-closed guard that is currently refusing** — which this seat will not
do on its own authority, because doing so converts a refusal into a pass without an owner word.

**The resolution packet (T1–T4) determines the READING, the CLOCK, the CURVE and leaves the OBJECT
open. It says nothing about the year-0 basis of a no-arb table.** Neither option is derivable from it,
and the choice changes every margin the owner will read. **STOP.**

## 5. WHAT IS ALREADY DONE AND STANDS

Steps 1 and 2 are complete and are **not** blocked by this:

| control | result |
|---|---|
| P1 dial-off byte identity | **HELD** — `9298203135202a0c707bb0977ba38c31` |
| P2 preview lane undisturbed | **HELD** — `6a392bca7ad0dee04a6b4f037c758f65` |
| P4 determinism | **HELD** — `d3c65bc46cebb656914cacb34a693b77` twice |
| **the wiring proof** | **HELD EXACTLY** — see below |
| the resolved board total | 715,219.2 vs derived 715,228.6 (−0.0014%), the 715,229 class |

`o30bn_lawcheck.py`: `beta30bn == beta_at` exact over 4,009 points; `b_lift30bn == b_lift` exact over
48,108 points; the engine's own `_pv_resolved` == `o30br_resolved.py::book()`'s branch arithmetic to
**1.8e-12** over 14,592 synthetic points spanning every lane and both depth lanes.

## 6. WHAT THE OWNER IS BEING ASKED

**One word: A or B** (or a third basis the owner names). On that word, Step 3 is one emit and Step 4 is
one table pass — the machinery is built, controlled and committed.

If the answer is **B**, the seat additionally needs the owner to accept that the re-point of
`RL_DAY0_FINAL` is a **declared** basis change that will be logged in the emitter header and printed on
every table, not a silent one.

**A NOTE THE OWNER SHOULD SEE EITHER WAY.** The 30B Step-1 re-fit has silently invalidated the ORDER
29C emitter for **every** future act on this branch, not just this one. Any order that re-emits the
as-of matrix will hit the same halt until the basis question is settled.
