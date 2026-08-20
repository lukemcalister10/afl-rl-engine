# HALT — THE WALK-FORWARD EMIT ON `a05fe951` CANNOT READ 89 OF 89 WITHOUT A WIRING CHANGE

**Branch `land/order-29`, from `origin/land/order-29` at `9b93fba`. Board
`a05fe951f78482c70520480e184c80ec`, engine `29376d5a`.**

> ## THE BOARD IS **PRICED, NOT ADOPTED.** Nothing here is adopted, merged, tagged or promoted.

**This halts completion-pass items 3 (the emit), 4 (the class mark) and 5 (the no-arb page).** They
are halted **together and for one reason**, because all three read a walk-forward matrix and no
matrix for `a05fe951` can be produced. **Nothing is worked around. No guard is bypassed, weakened or
re-pointed. No engine file and no emitter file is modified.** The order's instruction is followed
literally: *"if anything seems to require an engine change, HALT that item and report."*

---

## 1 · WHAT HAPPENED

The day-0 reference was regenerated first and cleanly — `DAY0_CP.json`, **all nine assertions pass**,
`83 of 89` byte-identical, the six named rows moving exactly as the D7 parity harness published
(`REBASE_DAY0_AMENDED_out.txt`, committed at `278774e`). The emit was then run against that
regenerated reference, with `RL_O43` added to the dial pass-through (`run_emit_CP.sh`, the disclosed
script change).

**It halted.** Raw, from `EMIT_CPCAND_out.txt`, unedited:

```
ORDER 31-F HALT (replication): 82 of 89 wired entrants reproduce the board's printed day-0 at
tolerance 0. Mismatches: [('harley-barker', 504, 481, 843.128494491119),
('blake-thredgold', 381, 372, 503.37499764375303), ('sam-allen', 450, 428, 791.8152857422534),
('max-king-syd', 138, 129, 278.369144349601), ('noah-chamberlain', 40, 37, 86.64903086038251),
('liam-hetherton', 70, 66, 117.30450712681677), ('kobe-mcdonald', 40, 37, 87.02989219418069)].
The year-0 column is only the landed law if it reproduces the law's own published output EXACTLY;
a partial match is a DIFFERENT law and must not be emitted as this one.
```

The tuple is `(key, the reference's printed, the printed integer the EMITTER forms, the raw entry
object)`. **The reference column is right in every row** — 504, 381, 450, 138, 40, 70, 40 are exactly
the board's own printed values and exactly what `DAY0_CP.json` carries. **The emitter forms something
else.**

---

## 2 · THE CAUSE, MEASURED — THE PARITY GUARD IS INVISIBLE TO THE ORDER 31-F GUARD

`cp_o31d_probe.py` (read-only, one engine load, the candidate's own dial line) reads both laws side by
side. Raw, from `O31D_PROBE_out.txt`:

```
  RL_O43 live in the engine namespace : _O43 = True
  _D7_DFADE entries (fade pairs)      : 23
  _D7_FLOOR entries (lifted rows)     : 23

  key                  derived_v0       o31_D       d0*o31_D    _e30b_price  EMITTER    BOARD
  harley-barker          843.1285    0.571012       481.4362       503.5089      481      504   <-- DIVERGES
  blake-thredgold        503.3750    0.739244       372.1171       381.2208      372      381   <-- DIVERGES
  max-king-syd           278.3691    0.464716       129.3627       137.5416      129      138   <-- DIVERGES
  liam-hetherton         117.3045    0.566367        66.4374        69.5288       66       70   <-- DIVERGES
  ollie-murphy           398.3583    0.503262       200.4784       200.4784      200      200
  noah-chamberlain        86.6490    0.426113        36.9223        39.5300       37       40   <-- DIVERGES
  sam-allen              791.8153    0.540664       428.1057       449.6938      428      450   <-- DIVERGES
  kobe-mcdonald           87.0299    0.426113        37.0846        39.7037       37       40   <-- DIVERGES
```

**The two arithmetics:**

| | forms the day-0 price as | wired by `RL_O43`? |
|---|---|---|
| **the engine / the board** | `_entry30b_price(q, BASE_REF)` | **YES** — the D7 second wiring site wraps it |
| **the emitter** (`emit_matrix_31f.py:143`) | `int(round(_landed_v0_board(q) × o31_D(q, BASE_REF)))` | **NO** — `o31_D` is **not** wrapped |

`ORDER D7` wired the parity guard into **`ev`** (the price) and into **`_entry30b_price`** (the
engine's own day-0 predicate). **It did not wire it into `o31_D`, the fade itself.** The engine is
internally consistent — its own boot-class identity reads **89 of 89 at tolerance 0** on this very
board, because that assert goes through `_entry30b_price`. But **any consumer that reaches for
`o31_D` directly still gets the unguarded live-depth fade**, and the ORDER 31-F emitter is exactly
such a consumer, by explicit design:

> `o31_D` is read out of the ENGINE NAMESPACE (`G['o31_D']`), not re-implemented here, **so the guard
> cannot drift from the law it is guarding.** — `emit_matrix_31f.py` header, §SITE 1

**That intent is correct and the emitter is faithful to it.** The drift is not the emitter's: the law
moved to a wrapper one level above the symbol the emitter was told to read.

**`ollie-murphy` does not diverge**, and that is the confirming detail: he is a **riser**, his
injury-regime value already exceeds his healthy counterpart, so `_D7_DFADE` applies no ratio to him
and the two arithmetics agree. **Exactly the seven rows where the healthy fade wins diverge** — the
six movers **less** murphy, **plus** `sam-allen` and `kobe-mcdonald`, whose printed integers the guard
restores to the frozen values but whose *fade* is now formed on the healthy side.

---

## 3 · WHY NOTHING WAS WORKED AROUND

Three ways exist to make the emit read 89 of 89. **This seat is authorised for none of them.**

| | the change | why it is refused here |
|---|---|---|
| **(a)** | wrap `o31_D` under `_O43` in `engine/rl_after/_merged_recover.py` | **AN ENGINE CHANGE.** The order forbids engine edits outright and instructs a halt-and-report instead. It also deserves its own prereg and its own falsifier set: `o31_D` is consumed in many places, and silently changing the fade everywhere is a far wider act than the per-row `max` the owner ruled. |
| **(b)** | re-point the guard at `_entry30b_price` in `emit_matrix_31f.py` | **A CHANGE TO THE BYTE-CARRIED EMITTER.** The emitter is carried byte-for-byte at every candidate's reading and its md5 is printed at run (`d5f4880662b7de3f2716e1c84112d11d`). Editing it would break the one property that makes every historical matrix comparable, and would do so inside the very guard that exists to catch this class of drift. |
| **(c)** | write the reference with the emitter's values (481 / 372 / 129 / 66 / 40 / 428 / 37) | **A FALSE REFERENCE.** Those are not the board's prices. It would contradict the board, the D7 parity table, the six-row disclosure the owner has already accepted, and the engine's own 89-of-89 assert — to make a guard pass. This is precisely the "regenerate the reference until the guard goes quiet" failure the guard was built to prevent. |

**The ORDER 31-F guard is behaving exactly as designed.** It fail-closed on a genuine divergence
between the board's law and the emitter's law. Reporting it is the correct outcome; silencing it is
not.

---

## 4 · WHAT THIS BLOCKS, AND WHAT IT DOES NOT

**BLOCKED — all three read a walk-forward matrix:**

| item | status |
|---|---|
| **(3) the walk-forward matrix on `a05fe951`** | **HALTED.** No matrix exists or can be lawfully produced. |
| **(4) the class mark on the candidate matrix** | **HALTED — NOT MEASURED, NOT ESTIMATED, NOT CARRIED FORWARD.** The class instrument reads `per_entrant_CPCAND.json`. The base `ff936186` reads **1.0671174504** and the instrument self-validates against ORDER K (1.0513 / 1.0324), but **the candidate's own number is unknown and is not guessed.** |
| **(5) the full no-arb page for `a05fe951`** | **HALTED.** The no-arb instruments read a matrix, not a board. **No owner page is written from a board that has no matrix**, and the base's no-arb status is **not** presented as the candidate's — the same rule `bb_noarbFC.sh` already states in its own header. |

**NOT BLOCKED — these do not read a matrix and are delivered:**

- the amended day-0 reference regeneration (item 1 + 2) — **DONE, all nine assertions pass**
- the document set (item 6) — the tracker, per-lever, year-1 and player pages read **boards**, not
  matrices (`fc_pages.py` borrows only the **dial-invariant** `year`/`type` columns from the base
  matrix, a borrowing that file already discloses and asserts)
- the acceptance chain (item 7) — determinism, the dial-off identities, the day-0 asserts, tail, burn
  and birthday

---

## 5 · THE HONEST HEADLINE

**This is not a failure of the parity board.** `a05fe951` reproduces byte-exact, its own printed-day-0
identity reads 89 of 89 at tolerance 0, every dial-off identity holds, and the day-0 reference
regenerated cleanly against it with all nine assertions passing.

**It is an incomplete wiring of the D7 guard with respect to instruments that read `o31_D` directly**,
found by a guard doing its job. It is filed here rather than smoothed, and it needs an owner or
supervisor ruling — most naturally as a **D7 follow-up order** that wraps `o31_D` under `_O43` with
its own prereg, its own falsifiers and its own dial-off byte-exactness proof, after which this
completion pass's items 3–5 can be run unchanged.

**Related, and already on the record:** `PACKET_D7.md` §4.1 filed a *different* instrument fragility
in the same neighbourhood (`rl_export.py:68`'s bare-substring sentinel). This is a second, independent
instrument-versus-engine gap in the same delivery. Both were caught by guards that must move or must
match, not by inspection.

---

## 6 · FILES

| file | what |
|---|---|
| `HALT_EMIT_CP.md` | this halt report |
| `EMIT_CPCAND_out.txt` / `EMIT_CPCAND_run.txt` | the raw emit halt, unedited |
| `cp_o31d_probe.py` / `O31D_PROBE_out.txt` | the read-only probe that locates the divergence |
| `run_emit_CP.sh` | the emitter runner with the `RL_O43` pass-through (the disclosed script change) |
| `DAY0_CP.json` / `REBASE_DAY0_AMENDED_out.txt` | the regenerated reference — **clean, nine of nine** |

**Priced, not adopted. Guard 5 remains RED (C3) and is not claimed green anywhere.**
