# NOTE FOR SEAT 9 — Leg-D food for thought (circularity + survivorship)
### From seat 8, 2026-07-16. NOT a ruling and NOT a directive — items for CONSIDERATION when the
### Leg-D (PVC re-derivation) memo is written. These came out of an owner conversation AFTER seat 8
### closed; the owner asked they be passed on. Treat as hypotheses to test against the code, not
### settled design. Nothing here is owner-ruled; where it says "the owner thinks/notes", that is his
### read offered for consideration, not a waiver of anything. Verify everything fresh.

## WHERE THIS CAME FROM
The GPT audit (docs/AUDIT_gpt_spec_findings_2026-07-16.md) raised circularity and survivorship
against the PVC derivation (its Surface 7 / Surface 8 clusters). The owner pushed back on both and
sharpened them into something more useful than the audit's own wording. This note captures that — for
you to weigh when you build the Leg-D construction, not to pre-decide it.

## A CORRECTION SEAT 8 OWES THE RECORD (so you don't inherit the error)
Seat 8 twice wrote "day one" / "the day after the draft" when discussing the PVC derivation. The
owner corrected it: the derivation is understood to look at players at the **end of year 1** (a season
of evidence), NOT entry. Keep the two instruments distinct:
- **G-Y0 the IDENTITY** = the day-after-draft equivalence (pick N ≈ the player, one day apart). That
  is the population-level BINDING gate (R104.7), effective at Leg D.
- **The PVC DERIVATION** = what players are actually worth after real evidence. Different instrument.
Blurring them is what made the circularity argument sound worse than it is. Verify how the current
code actually defines the derivation window before designing — don't take either seat's word.

## ITEM 1 — CIRCULARITY (the owner thinks it's real but trivially cuttable)
The audit's "old curve feeds the new curve" is loose — the old PVC is retired, nothing old feeds
forward. The NARROW real seam: Leg D derives "what pick 5 is worth" from the values of players who
entered at pick 5, and a **zero-evidence** entrant is priced ≈ entirely by his (position-adjusted)
pick prior. For those players you'd be feeding the pick-5 prior back out as the pick-5 curve — a
potential tautology (proves nothing), not a wrong number.

The owner's move — worth considering — is to **cut the circle rather than test for it**: if a fresh
draftee is priced almost entirely by his pick, that pricing ALREADY IS the statement of what the pick
is worth, so read it directly instead of deriving it in a loop. Two shapes to weigh in the memo:
- **Pure:** the curve's entry point just IS the position-adjusted entry pricing — no derivation loop
  at that point; the circle is deleted, not broken.
- **Honest-calibration:** derive from EVIDENCE-BEARING seasons only (pick prior faded out) — a
  genuinely independent curve — and use it as the check on, or the source of, the entry pricing.
These are not in tension: they're the two ENDS of the same line. Anchor the entry end on the pick
pricing you already have (no circle); let the evidence end come from realised production (no prior);
the PVC is the line between them — both ends independently pinned. That structure appears to kill
circularity AND the tautology worry together. Offered as a candidate, not a decision.

## ITEM 2 — SURVIVORSHIP + CONVEXITY (the owner's real concern; bigger than the audit's)
The audit said "include busts or you overstate pick value." True but shallow. The owner's sharper
point: include busts AND preserve the convex survivor reward, or you UNDERSTATE the pick. His numbers,
for you to reproduce from the data (do not trust these as given — measure them):
- **Year 1:** ~100–120 players at value ≈ 100 ⇒ pool ≈ 10,000–12,000.
- **Year 4/5/6:** ~50–70 survivors at 125–133 (top of range ~1.78–2.66× a yr-1 player) ⇒ pool
  ≈ EQUAL OR GREATER than the year-1 pool — with ~HALF the bodies. Survivors more than double per head.
The consequence: a pick is a claim on the WHOLE life-path distribution, and because the surviving
pool holds as much total value as the entry pool, pricing a pick off a flat entry snapshot
systematically UNDERPAYS it — worst at the top, where the convex tail is fattest.

**The framing the owner and seat 8 landed on (offered as the useful lens):** this looks like the SAME
disease the chapter already exists to cure, in a third costume. English underpriced = output→price
flattened at the top (Leg B). Young underpriced = convex upside not credited (item 130). Picks
underpriced = survivor tail averaged flat (Leg D). One disease — convex reward collapsed into a
linear average — three costumes. If that framing holds, the pick curve must carry the SAME fix or it
re-imports the disease at the end of the chapter.

Design implication to WEIGH (not adopt blindly): a single cross-section (entry OR any one later year)
can't work — entry misses the tail, a later year misses the busts (survivor-selected). The candidate
worth testing is a curve built off the FULL REALISED LIFE-PATH of each entry cohort: every player a
pick produced — busts at their low value, survivors at their compounded value — summed across the
trajectory. Include wash-outs (don't overprice); let survivors compound (don't underprice); convexity
then falls out of the data rather than being modelled in or averaged away.

## THE ONE DISCIPLINE SEAT 8 WOULD URGE (and the owner agreed)
The owner THOUGHT busts were already included and survivors already compounding. Neither seat can see
it from here. Given this is plausibly the chapter's central disease and not a footnote: the FIRST
Leg-D act should be to MEASURE the current derivation's behaviour from the actual data — build the
life-path pool totals, see whether the existing curve reflects the convex tail or flattens it — and
design the fix from what the code DOES, not from memory. If it's already right, the audit points close
with evidence. If it's flattening, a real defect was caught before shipping. Measure, don't assume —
the discipline this project keeps proving it needs.

## HOW THIS RELATES TO THE AUDIT TRIAGE (item 199)
This note IS the substance of triage cluster (iii) for the two PVC findings, plus the owner's
correction of the audit's framing. The other audit clusters (i spec-fold, ii acceptance-hardening,
iv the flex misread) are unaffected and stand as filed. Fold what survives your own scrutiny into the
Leg-D section of the functional-form memo; discard what the code disproves.
