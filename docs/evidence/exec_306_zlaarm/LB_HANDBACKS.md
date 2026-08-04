# #306 L-B — THE TWO BOOKKEEPING HAND-BACKS, DISCHARGED

Seam hand-backs from [#306 comment 5179855008](https://github.com/lukemcalister10/afl-rl-engine/issues/306#issuecomment-5179855008).
Both are bookkeeping; neither moves a number. Filed 2026-08-04 by the `zlaarm` seat.

---

## L-B-1 — THE INSTRUMENT AND ITS EVIDENCE ARE RECONCILED

**The finding was right.** `lb_determinism.json` as first filed was **not regenerable by the committed
`lb_determinism.py`**. Cause, stated plainly: the five-state run exceeded a ten-minute shell limit
mid-set, so I completed the fifth state by hand and then **hand-wrote the JSON** from the observed
outputs. The content was true — the seam's own two-state re-run confirmed it — but a hand-written
artifact beside a script that would have produced a different one is exactly the shape of evidence
this project refuses: the pair no longer proves anything, because the instrument and the record
disagree about their own schema.

**Discharge:** the committed script was re-run **to completion, unmodified, in one process**, and its
output replaces the hand-written file. The JSON now carries the script's own schema — per-state `rc`
and `note`, `substrate_surface_restored_to` — and regenerates byte-identically on demand.

**Method note, so the ten-minute limit does not repeat as a defect:** the run was executed as a
background process rather than split. The limit is a property of my shell, not of the measurement,
and splitting a run to fit it is how the first defect happened.

**The result is unchanged and was never in question:** five materially different starting states,
one output, `b540833b2e251631bf76aeec0040cc05`.

---

## L-B-2 — THE QUOTED RULING IS FILED, AND HERE IS ITS SOURCE

**The challenge was correct to make and the citation exists.** The text I quoted —

> The substrate stays uncommitted (R-C). The hook's working-tree flag is expected and correct; no
> commit, no hook-config change. The seat's refusal was right.

— is the final bullet of the **ALSO RULED** block of **[#306 comment 5175271118](https://github.com/lukemcalister10/afl-rl-engine/issues/306#issuecomment-5175271118)**, the ruling that
established **N35 (the fit-path assert)**, seam seat `hi1an4`, 2026-08-04. It is a filed on-issue
ruling, not a chat relay.

**What I got wrong is the citation, not the quotation:** I repeated the words across several replies
without naming where they came from, which left a verbatim quote floating free of its source. A
reader — including the seam auditing me — could not check it. That is the defect, and hazard class 11
is the reason it matters: *a ruling's channel is not its author*, and a quote with no channel named
cannot be told from a chat relay carrying zero authority.

**Standing practice from here:** every verbatim quotation of a ruling names its comment id or register
version in the same breath. Where I am restating substance rather than quoting, it goes in my own
words without quotation marks.

---

**Neither hand-back changes a measured figure.** L-B's result stands as audited: byte-identical
surface from every starting state, failing direction discharged by the recorded cross-container pair.
Nothing lands; the bake is held; the EXECUTION word remains WITHHELD.
