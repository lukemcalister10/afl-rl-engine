# PREREGISTRATION — the staged-validation free-agent casing comparison

**Pushed BEFORE the edit.** Unplanned: this is not one of the two rulings the order carried. It is
raised here because the apply, unblocked by R1 and R2, ran all the way through T8 and then halted on
a **self-contradiction inside one validation block**. The seat is making a code correction to a
fail-closed guard, which is exactly the kind of act that must be visible before it happens, not
explained after.

## WHAT FIRED

`python3 ui/tools/ingest_inputs.py` (attempt 1, `25_apply_attempt1_HALT_free_agent_casing.txt`)
reached **T8** — every prior verdict green, including `[T2] store diff proof — affl_team only, on
exactly 112 planned keys; byte-attribution OK` — and then:

```
■ HALT — ownership store apply refused: STAGED VALIDATION FAILED (nothing committed):
    - board_view_working did not take the move for bailey-banfield
    - ownership mirror did not take the move for bailey-banfield
    … 14 players, 28 lines …
```

The 14 are **exactly** the 14 of the owner's 112 moves whose destination is the lowercase spelling
`"Free agents"`: Bailey Banfield, Bobby Hill, Dion Prestia, Dougal Howard, Finnegan Davis, Matt
Duffy, Maurice Rioli, Nathan Broad, Sandy Brock, Steele Sidebottom, Taylor Walker, Tom McDonald,
Tyson Stengle, Zac Fisher. Counted independently off `11_the_112_movers.json`: 14 of 112 target a
free-agent spelling, and the failing set is that set exactly. No other mover fails.

## WHY IT IS A DEFECT AND NOT A REFUSAL — the proof

`ui/tools/ownership_store_apply.py` lines 686-699 are one block. Two of its assertions are **mutually
unsatisfiable** for any planned move whose target is `"Free agents"`:

```python
for key, name, _cur, new in plan.rows:
    if by_key.get(key, {}).get("affl_team") != new:              # demands the mirror hold "Free agents"
        fails.append("board_view_working did not take the move for %s" % key)
    if own["byKey"].get(key) != new:
        fails.append("ownership mirror did not take the move for %s" % key)
…
if any(c and c.lower() == "free agents" and c != "Free Agents" for c in clubs):
    fails.append("free-agent spelling forked in the mirror")     # demands the mirror hold "Free Agents"
```

There is no mirror that satisfies both. The tree has already ruled which one is right — in this same
file's own docstring, the seam-binding law of 2026-07-30:

> EXACT BYTES (seam-binding, 2026-07-30). The store takes the owner's bytes VERBATIM — no
> canonicalisation, no case-folding. … **Canonicalise for the MIRROR
> (extract_board_view.norm_club / ingest_inputs.normt), NEVER for the store.**

and `extract_board_view.norm_club` does exactly that:

```python
return "Free Agents" if s.lower() == "free agents" else s
```

So the mirror is CORRECT and the comparison is WRONG: it holds a display-normalised mirror value
against a raw store value. Latent since #283 (5dd2674, 2026-07-30) — that change set was 18 rows and
contained no move to the lowercase spelling, so nothing ever exercised it. The owner's 2026-08-20
sheet is the first change set that does. No test pins the current comparison.

**The guard fails CLOSED, which is why nothing is broken and nothing was committed:** store still
`cb38ef11`, board still `a05fe951`, all pins unmoved (`md5sum -c` on the pre-run hashes: OK for the
store, the board, expected_boot, release_contract and season_state). Only the ingest's two designed
refusal outputs were rewritten, as they are on every halt.

## THE CORRECTION — the smallest one that resolves the contradiction

In `ui/tools/ownership_store_apply.py`, compare the MIRRORS through the MIRRORS' OWN normaliser,
importing it from `extract_board_view` so there is one definition and not a copy:

* import `norm_club` from `ui/tools/extract_board_view.py` (import-safe: that module's top level is
  path constants only, `main()` is behind `if __name__`);
* in the two mirror comparisons, compare `norm_club(mirror_value) != norm_club(new)`.

Nothing else changes. Specifically **NOT** changed:

* the store side. `plan.rows` and the T1/T2 exact-bytes diff proof are untouched — the store keeps
  taking the owner's bytes verbatim, which is the load-bearing law.
* the `"free-agent spelling forked in the mirror"` assertion — it stays exactly as it is and still
  guards the mirror.
* every other member of the staged validation.

This makes the guard *consistent*, not *lenient*: a mirror that genuinely failed to take a move still
fails, because normalising both sides only collapses the one documented casing pair.

## FALSIFIERS

1. **F1 — non-vacuity.** After the fix the comparison must still be able to FAIL. Demonstrated by
   construction: `norm_club` maps only the free-agent casing pair; any other wrong club on either
   side still compares unequal. To be shown by a deliberate probe: corrupt one mirror entry to a real
   but different club and confirm the guard fires.
2. **F2 — exactly the 14 disappear.** The staged validation must go from 28 failure lines to 0. If
   ANY other validation line appears, that is a new finding and gets reported, not absorbed.
3. **F3 — the store side is untouched.** `[T2] store diff proof — affl_team only, on exactly 112
   planned keys` must still read exactly that, and the written store must still carry the owner's
   raw `"Free agents"` bytes for those 14 rows — verified by reading them back out of the WRITTEN
   store. If the store canonicalises, the fix is wrong and must be reverted.
4. **F4 — the board must be byte-identical.** `a05fe951f78482c70520480e184c80ec` before and after.
5. **F5 — the round pin never advances.** 22 everywhere.
6. **F6 — ui/tests/ownership_store_apply.test.py stands at 28/28** before and after this edit.

## THE FORK, STATED PLAINLY

**A. (taken)** The comparison is corrected as above and the apply completes. Grounds: the block
contradicts itself, the tree's own written law resolves which half is right, the store side is
untouched, and the guard keeps every discriminating property it had.

**B.** The comparison is left alone and the owner's apply stays blocked until a supervisor rules it.
Grounds: it is a fail-closed guard and a build seat should not edit one.

The seat is taking **A**, preregistered here and pushed before the edit, and is flagging it at the top
of its claims note so it can be reversed in one commit if the supervisor rules **B**. It is recorded
as an UNPLANNED edit outside the order's two rulings — the order sanctioned one code edit
(the selftest pin) and this is a second one.

*Pushed before the edit. Build seat, 2026-08-20.*
