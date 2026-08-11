# The canonical-instrument read — reproduction first

The owner challenged a 1.74 peak reading. The last canonical no-arb tables read ~1.43-1.50 at peak,
and 1.74 would have meant peak appreciation grew from 50% to 75% over picks during work that was
supposed to conserve. This file records the reproduction-first check that settles it, in the order
the alignment-gate discipline requires: **reproduce the known answer before reading a new one.**

The seat's book-ratio spot-check that produced 1.74 was a naive approximation and is **not defended
here**. It pooled all 2,645 emitted rows — including 691 RD entrants whose small anchors inflate a
Σv/Σv0 ratio — with no basis or discount alignment and naive entry-year labelling. The canonical
script decides everything below.

---

## Step 1 — the instrument reproduces its own past output. **PASS**

`noarb_table_338.py` was run **completely unmodified** against the stage-5 matrix under the
**stage-5 pins**, and diffed against the published stage-5 table.

```
python noarb_table_338.py per_entrant_338_stage5.json   ->   diff vs noarb_table_stage5.txt
DIFF_EXIT=0          (text, ignoring only the trailing "json -> <path>" line)
JSON_DIFF_EXIT=0     (the groups block of the emitted json vs noarb_table_stage5.json)
```

Byte-identical. The instrument reproduces its own past output, so everything downstream of it is
trustworthy. The script's identity is `md5 0f8220351c64c56ccfa90c60edcdfa5f`, byte-identical to both
the `#338` evidence copy and the stage-5 copy — this act did not touch it and never will.

The published stage-5 reference, ALL picks 1-64:

| yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | yr6 | yr7 |
|---|---|---|---|---|---|---|---|
| 1.000 | 0.991 | 1.185 | 1.347 | **1.433** | 1.431 | 1.394 | 1.211 |

That is the ~1.43-1.50 family the owner was recalling. It is correct.

---

## The re-pin — and the proof it can still fire

The five variant matrices carry the **current** gate store, so the harness's pinned identity had to
be re-pointed. Run untouched under the stage-5 pins, the main matrix **halted**, which is the assert
doing its job and naming both values:

```
AssertionError: matrix store d9a24282 != committed identity 37ced3ce
```

Re-pointed in `harness_pvc_REPINNED_pass3.py`, documented in its header, asserts byte-identical:

| pin | stage-5 | this act | basis |
|---|---|---|---|
| `EXPECT_STORE` | `37ced3ce` | `d9a24282` | the current gate store |
| `EXPECT_V0SURF` | `3e8e50de5103` | `6ef67f07db98` | curve-keyed surface signature |
| `EXPECT_N` | 1197 | **1197** | RE-MEASURED on all five matrices, not assumed |

`EXPECT_N` is the important one: the ND teaching population is **1197 on every one of
main/FULL/V1/V2/V3 and on the stage-5 matrix**. The populations are identical, so the variant
comparison is apples-to-apples and the population is *not* a candidate explanation for any contrast
in the decision table.

**Only the harness pins moved. `noarb_table_338.py` itself is untouched.**

---

## Step 2 — the decisive read of `origin/main`. Reported as measured

Two outcomes were pre-registered. **Neither fits cleanly**, so the reading is reported as measured
rather than forced into a branch:

- **(a)** main in the ~1.4-1.5 family → no interim catastrophe, proceed
- **(b)** main at ~1.7+ → stop, hunt the divergence

**Measured: main peaks at 1.573.**

This is **not outcome (b)**. The 1.74 was construction noise, exactly as pre-registered — the
population difference is the whole story, and it is quantified: the canonical population is the
**1197** ND teaching rows, not the raw **2645** emitted rows, and the 1,448 excluded rows are
overwhelmingly small-anchor pool entrants (691 RD alone) that inflate a pooled Σv/Σv0.

But main is not squarely inside the 1.4-1.5 family either. Against the stage-5 reference:

| yrN | stage-5 | main | drift |
|---|---|---|---|
| yr1 | 0.991 | 1.124 | **+13.4%** |
| yr2 | 1.185 | 1.377 | +16.2% |
| yr3 | 1.347 | 1.510 | +12.1% |
| yr4 | 1.433 | 1.573 | **+9.8%** |
| yr5 | 1.431 | 1.567 | +9.5% |
| yr7 | 1.211 | 1.319 | +9.0% |

**This drift is not this act** — every item of the composition package is off in the main emit.

### The comparison is confounded, and that is stated rather than papered over

Two things moved between the stage-5 reference and `origin/main`, not one:

```
engine   98ed7070  (stage-5 BRANCH engine)  ->  c0a7e969  (origin/main)
store    37ced3ce                           ->  d9a24282
v0surf   3e8e50de5103                       ->  6ef67f07db98
```

The stage-5 table was emitted by a **branch** engine that was never main. So the drift **cannot be
attributed to any one commit from these numbers alone, and no attribution is offered.**

### Hunt plan — reported, not executed

Outside this act's scope and costing machine time the owner has not authorised for it:

1. **Separate store from engine.** Re-emit main's engine against store `37ced3ce`, and the stage-5
   engine against store `d9a24282`. Two emits, ~2.5 min each. Splits the drift into a store
   component and an engine component *before* any commit is blamed.
2. Only if the engine component is the large one, bisect across the candidate movers named in the
   order (R22 apply, DOB, G1, era-in-breach) — one emit + one table each.
3. Confirm whether the stage-5 engine was ever ancestral to main. If it was not, "drift" is the
   wrong word and the two tables were never on the same line of development.

### Why this does not block the act's decision

All five variants share one store, one surface, one engine head for the four act variants
(`4fc44090`, differing only by env dials) and one 1197-entrant population. The `main -> FULL`
difference is measured **inside that closed set**, so the drift shifts the whole table together and
cancels out of every within-table contrast.

---

## Step 3 — the five variants

`run_canonical.sh` runs the untouched script once per variant. Outputs: `table_<v>.txt/.json`, and
the combined read in `DECISION_TABLE.txt/.json`.

| variant | engine head | discount |
|---|---|---|
| main | `c0a7e969` | flat 14%/yr |
| FULL | `4fc44090` | flat 14%/yr (the package does not change the discount) |
| V1 | `4fc44090` | 13% ≤21, 15% ≥26, linear |
| V2 | `4fc44090` | 12% ≤19, 13% 20-21, 15% 25-27, 16% ≥28 |
| V3 | `4fc44090` | 10% ≤20, 11% 21-22, 12% 23-25, 13% 26-28, 14% ≥29 |

**Nothing ships.** PR #399 remains HELD.
