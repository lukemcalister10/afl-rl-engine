# #306's DECIDING MEASUREMENTS — re-runnable, from committed inputs only

Filed 2026-08-04 by the #290 `d7bnaa` seat under **#306 pre-fire condition 1** (charter D2): the
directive's §2 and §3 tables were prose in an issue; they are now scripts plus outputs whose inputs
are committed and asserted by md5.

| script | answers | output |
|---|---|---|
| `hysteresis_magnitude.py` | how BIG is the refit's path memory? | `hysteresis_magnitude.json` |
| `tail_gap_by_band.py` | WHERE does the year-zero gap sit? | `tail_gap_by_band.json` |

Both are read-only — no engine act, no bake, nothing written outside this directory — and both HALT
rather than report a number if any pinned input has moved.

## What they establish

**`hysteresis_magnitude.py`.** Passes 2 and 4 installed a byte-identical curve (`ca662051`) onto a
byte-identical frozen fitted stack by different routes, so every difference between their matrices
is path memory alone. **60 of 2,646 v0 values move, by at most 0.1 absolute / 1.845e-4 relative.**
A different-curve control (passes 1 vs 3) runs beside it, because a small number needs something to
be small *relative to*. The cycle those differences were proposed to explain swings the band gaps by
**~2 percentage points** — three orders of magnitude more. **Determinism is necessary, not
sufficient**; that is #306 §2, and it is why the directive does not let an acceptance line rest on
the mechanism clause R-K originally carried.

**`tail_gap_by_band.py`.** The year-zero gap on the halt substrate is a **tail** phenomenon: picks
46–64 sit **~+64%** above the installed curve while picks 1–10 sit **~−5%** below it. The cycle moves
every band by ~2pp and the tail most (+3.09pp). The same-curve repeat control is flat to ~0.001pp, so
none of the band structure is hysteresis. That is #306 §3, and it is the measurement behind N16's
first spec word — *tail constrained by construction* — and behind the owner's steer that year-zero
values **anchor** to the measured pick outcomes while position and age **modulate within bounds**.

## The population caveat, stated once here and again inside the script

`tail_gap_by_band.py` runs on the **FIT population** — the matrix's own `teaches_curve` rows at picks
1–64. That is **NOT** the G-Y0 gate's population; the gate runs inside `one_source_selftest.py` over
its own ~1,326-row set and prints its own figure every run. The overall numbers here land near the
gated ones and **are not them**. The band SHAPE is what these tables are for. A figure from this
directory must never be quoted as a gated G-Y0.

## Inputs

The committed pass matrices (`pass1..pass4_matrix.json`) and the committed derived-curve artifacts
(`pass0..pass3_derived_curve*.json`), each pinned by md5 inside the scripts. The pass-N matrix is
paired with the curve installed **at pass N** — the pairing is explicit in the source, because
comparing a matrix against the wrong pass's curve yields a plausible, wrong table.
