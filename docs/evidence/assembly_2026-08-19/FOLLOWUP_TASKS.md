# FOLLOW-UP TASKS RAISED BY THE ASSEMBLY BUILD SEAT

**Not for this seat to close inside a board pass, and not to be lost.** Logged here rather than in
`docs/OPEN_ITEMS_REGISTER.md` because that register is **maintained by the supervisor pen** and this
seat does not hold it. **These are offered up for that pen to carry across.**

---

## FT-1 · REPAIR `os_continuity.py` / `os_lib.assemble` — **INSTRUMENT, NOT BOARD** — OPEN

**Raised:** the audit fix pass, 2026-08-19. **Owner of the defect: this seat.**
**Explicitly deferred by the coordinator:** *"log its repair as a named follow-up task (instrument,
not board), do not fix it inside this pass."*

**WHAT IS WRONG.** `os_lib.assemble` reconstructs a row's price from the engine's recorded legs as the
ORDER 31 law — `rho·e + pi·ped + age_credit` — and **has no R3 term**, because it was written before
ORDER 41 existed. `os_continuity.py:168` builds its shifted-age price from that reconstruction and
compares it against `EV(p, 2026)`, the engine's real price, **which does carry R3**. The harness is
therefore comparing a price *with* the collector against a rebuilt price *without* it.

**WHAT IT PRODUCED.** Run on candidate `81cf787b` the age axis reported **9 birthday movers, 3 of them
at 50%+, +1,025 net** — which reads as a breach of the birthday acceptance law. It is not one:
**+1,025 is exactly R3's whole marginal and the 9 rows are exactly the 9 rows R3 charges.** Measured
directly against the engine (`as_r3age.py`), the true birthday step through R3 is **+0 board points on
every charged row**, with both self-checks exact (1,200 calls at 0.000e+00; 9 of 9 at tolerance 0).

**THE CONSEQUENCE THAT TRAVELS UNTIL IT IS FIXED.** `os_continuity.py`'s **age axis cannot be read on
any board carrying R3.** Every pass from here must measure the birthday law with `as_r3age.py`
instead, and must say so. **A future seat that runs the harness and believes its age output will
report a breach that is not there — or, worse, will "fix" a board that is not broken.**

**THE REPAIR.** Give `assemble` an `r3_take` leg recorded at the blend call site (the same place the
other legs are recorded), and subtract it in `os_continuity.py`'s `p1`. **It must be recorded at the
call site, not recomputed afterwards** — a row reaches the blend twice under the M3 blend and the two
calls carry different games, different production input `e`, and a different stashed `_O41_PRED8`
value. A probe that reads those objects after the run sees only the last call's state; that mistake
was made once already in this seat's first draft of `as_r3age.py` and its own self-check caught it at
2 of 9.

**WHY IT WAS NOT DONE IN THE SAME PASS,** beyond the instruction: **repairing an instrument in the
same pass as the board it is measuring is how a seat talks itself into a number.**

---

## FT-2 · `os_lib.load()`'s DIAL CLEAR-LIST IS INCOMPLETE — OPEN, LOW SEVERITY

**Raised:** the audit fix pass, 2026-08-19. **Owner of the defect: this seat.**

`os_lib.load()`'s docstring promises that **no unset ORDER S/41 dial can leak in from a previous run**,
and it clears a named list to keep that promise. **`RL_O41_CREDITFORM`, `RL_O41_RAMP`, `RL_O41_BREAK`
and `RL_O41_UNWIND` are not on that list**, so a stale value of any of them in the surrounding
environment would reach a harness run silently.

**NOTHING MEASURED SO FAR IS AFFECTED** — every run in these passes goes through a clean subprocess
environment via `bbASM.sh`. **The promise is still not kept**, and it is the kind of gap that only
shows up as an unreproducible number months later.

**THE REPAIR:** add the four names to the pop-list in `os_lib.load()`. It is a one-line change and it
is deliberately **not** bundled into a board pass.

---

## FT-3 · NO WALK-FORWARD MATRIX EXISTS FOR THE LIVE BOARD `88ce647f` — OPEN, OWNER-FACING

**Raised:** the audit fix pass, 2026-08-19, when the owner asked for the live board as the one
reference on the no-arb page.

The no-arb test reads a **walk-forward matrix** (`per_entrant_<LABEL>.json`), not a board. **No matrix
for the live board exists anywhere in this project's evidence.** Every matrix on disk stamps the
**engine commit** it came from; **none stamps a board id**, so not one of them can be *shown* to be the
live board's, and presenting the closest-looking one as "live" would be a guess dressed as a
reference.

**THE JOB:** build the **live engine commit** and emit its matrix under a label that stamps the board
id, so the live reference exists once and can be reused. **This is a real build, not a rerun.** Until
then `ASSEMBLY_NOARB.html` prints the absence and the reason in plain words rather than leaving a
blank column.

---

## FT-4 · `U0 = 5` IS AN OWNER CONSTANT AND MUST NEVER BE DESCRIBED AS MEASURED — STANDING

**Raised:** D5, register v755.

The unwind speed `U0 = 5` is **RULED BY THE OWNER, NOT MEASURED** — lawful, with precedent in this
engine (`G* = 2`, dose `0.40`, `eta 0.50`). The engine's dial note, the prereg and the packet all say
so. **The standing obligation is that no future document silently promotes it to a measured
constant**, which is the failure mode this project has already caught once elsewhere.

**What the measurement actually says** is on the record in `UNWIND_OOS_out.txt` and is reported
against the ruling rather than in place of it.
