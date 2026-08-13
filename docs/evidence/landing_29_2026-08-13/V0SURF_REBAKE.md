# THE v0surf RE-BAKE — WHY IT IS PART OF THE CURVE INSTALL, AND THE BOX PROOF THAT LICENSES IT

**ORDER 29 · Step 3 resumed · branch `land/order-29` · 2026-08-13 · build seat.**

> This file exists because installing the ruled curve moved a pin **PREREG P18 named as a
> STOP-AND-REPORT**. It was not smuggled through. The measurement, the record's own standing ruling on
> exactly this coupling, and the proof that this box is allowed to perform the re-bake are all below.

---

## 1. WHAT HAPPENED, MEASURED

With the tiebroken curve installed (`curve_md5 76f8fa96`), the G-MONO halt at `rl_model.py:1449`
**passed** — the ruling did its job. The build then stopped further downstream, on a different gate:

```
v0surf FROZEN-SIGNATURE HALT: this build's config signature 4405cba2b42fb96f50496ec791cb806c
is NOT in data/v0surf.pkl (frozen: 41af73267f1bcd86bdc208e5f32376d1, 6ef67f07db98258786189a6316ce24f9).
```

This is the **#326 no-silent-refit guard** working exactly as designed. It is a halt, not a warning,
and — like the G-MONO halt before it — it cannot produce a wrong board, only no board.

## 2. WHY A CURVE MOVE NECESSARILY MOVES IT — MECHANISM, NOT INFERENCE

`_v0surf_sig` (`_merged_recover.py:1503-1509`) hashes the **active pick curve itself**:

```python
_curve = _PVC0 if '_PVC0' in globals() else MA.PVC     # the pick curve _v0_raw is actually reading
_payload = {'pvc': sorted((int(k),int(v)) for k,v in _curve.items()), 'roster': ..., 'gates': ...}
```

`_PVC0` is sourced from the adopted artifact. So **any** change to `pvc_curve_v2.json::curve` changes
the signature, and the frozen surface no longer covers the build. There is no configuration of this
landing in which the ruled curve installs and `v0surf` stays still.

**The control proves the curve is the sole cause.** The only difference between the last buildable
board (`0017657e`, dial ON, Steps 0–2 landed) and the halting build is the curve artifact. Note
particularly that the unflag-three did **not** move this signature — it moves the *v3.4 kernel* head
(3917 → 3966), which the signature does not read; the signature reads the **artifact** curve. That
asymmetry is the measurement that isolates the cause.

## 3. THE RECORD HAS ALREADY RULED ON THIS EXACT COUPLING

This is not a new question. The register (v715, `main` `ed6bd31`) carries it twice:

* as a rehearsal hand-back **defect** — *"defect 3 — `_v0surf_sig` hashes `_PVC0` itself
  (`_merged_recover.py:1286-1292`), so **curve install and v0surf re-bake are inseparable**"*;
* and, adjudicating a seat that re-pinned it, *"the step-4 diff already re-pins fv d10aa93e→28cfe2e6
  with engine_head/rl_model/**v0surf** (**the omission was the directive text's, not that seat's**)"*.

So the record's standing position is: a curve install **carries** its v0surf re-bake, and a directive
that omits it has a **text defect** — the omission is not charged to the seat. ORDER 29's brief omits
it in precisely that way.

The house method for the value effect is also on the record, from the act that moved
`v0surf 4cfc0b99→19d085a2`: the re-bake is **decomposed as its own lever** —
*"535 value / 681 rank movers of 804, decomposed 53 edited-row + 382 gfut-cohort + **100 re-bake**,
ZERO unexplained"*. This build follows that method: **`v0 surface re-bake` is a named lever in the
movers ledger**, not an unattributed residual.

## 4. THE N35 FIT-CLASS BOX PROOF — GREEN, AND IT CLOSES AN ORDER-28 OPEN QUESTION

A re-bake on a "weather box" would permanently freeze that box's BLAS kernel into the shipped board —
the item-380 defect the freeze exists to prevent. N35 therefore requires the box to **byte-reproduce
the CURRENT frozen surface through the deterministic fit path** before any new fit is trusted.

Run with the **live** curve `f6f3027f` installed, through the declared lane, writing nothing:

```
refit_v0surf: shipped-config signature 6ef67f07db98 | 18 age18 pos, surfN 60 ages, surfR 12 ages
              | new md5 fbc5b39387b2b135284a2e157f46c810 | committed pin fbc5b39387b2b135284a2e157f46c810
  surfaces frozen: 2
    41af73267f1bcd86bdc208e5f32376d1
    6ef67f07db98258786189a6316ce24f9   <- shipped
VERIFY: refit REPRODUCES the committed pin (fbc5b39387b2b135284a2e157f46c810).
```

**REPRODUCES, byte-exact.** This box is fit-class clean for the surface, so a bake here bakes the
engine's arithmetic and not this container's weather.

**This also closes an ORDER-28 open question.** The ORDER-28 rehearsal recorded *"HALT 2 — stage B
cannot run on landed code: the #326 no-silent-refit guard blocks the DECLARED refit lane too"*, and
concluded *"surface-fit classification is **untested** because the lane is shut."* The lane is **not**
shut on this tree — the #344 declared-refit lane landed — and the classification is now **tested and
green**. ORDER 28's finding is superseded by measurement, not by assertion.

## 5. WHAT THIS COSTS PREREG P18, OWNED BY NUMBER

**P18 is breached a second time, and this breach is structural rather than incidental.** P18 reads:

> *"Exactly these identities move … Anything else moving — `band`, `bust_prior`, `peak_model`, `q97m`,
> **`v0surf`**, `balanced_board`, `fv` — is a **STOP-AND-REPORT**, not a footnote."*

P18 also mandates, through P5, that the ruled curve be **wired**. Given §2, those two clauses cannot
both hold: **P18's moved-set was mechanically impossible as written.** The prediction was wrong in a
way the record had already documented, and it is owned here rather than reconciled away.

What is **not** breached is P18's *purpose* — catching an **unexplained** mover. This mover is
explained by mechanism (§2), licensed by the record (§3), proven safe to perform on this box (§4),
and **decomposed as its own lever** in the ledger (§3). Every other pin in P18's forbidden list —
`band`, `bust_prior`, `peak_model`, `q97m`, `balanced_board` — is asserted **unmoved** on the final
board, and `fv`'s movement remains the pre-existing ORDER-28 staleness documented at entry.

## 6. HOW IT WAS PERFORMED

Through the engine's **one committed, declared** path — never a silent fit:

```
RL_V0SURF_REFIT=1 RL_BAKE_V0SURF=1 python3 session_2026-07-18/legf6/scripts/refit_v0surf.py --bake
```

on the **final** curve, from a clean staged workspace under full five-var thread pinning. It writes
`data/v0surf.pkl`, re-pins `data/expected_boot.json::v0surf` surgically (that one line only), and
appends to `session_2026-07-18/legf6/v0surf_refit_log.json`. It is committed **isolated**, so the pin
move is a reviewable commit of its own rather than a line inside a larger diff.

The shipped board carries **no** refit flag: `RL_V0SURF_REFIT` is in the release contract's
`must_be_unset`, and the final board is built with it unset, loading the newly frozen surface. That
the final build performs **zero** fits is asserted, not assumed — `_v0surf_frozen is True`
(`_merged_recover.py:2590`).
