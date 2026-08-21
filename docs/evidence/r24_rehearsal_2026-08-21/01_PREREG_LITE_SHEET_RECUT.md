# PREREG-LITE — THE SYNTHETIC R24 SHEET RE-CUT

**SYNTHETIC. SANDBOX ONLY. NO OWNER WORD EXISTS OR IS CLAIMED.** In a real R24 this document
carries Luke's verbatim ruling on the injury sheet; here it carries a fixture string, and the
re-cut was performed by the rehearsal seat on machine-generated inputs.

PLAN_v6 3a / R23 runbook ERRATUM E7: a sheet change is a DATA commit and still owes a
review-forcing step — predicted md5, predicted row and injured=Y counts, and the disclosed movers —
committed WITH the data change, in the same commit as the sheet and `data/sheet_pins.json`.

## WHY THE RE-CUT

The synthetic R24 score file lists two players the pinned sheet marks `injured=Y`:
`connor-rozee` and `tom-green`. `land round`'s H2 check caught it BEFORE anything was armed
(evidence: `03_RUN_B_H2_HALT.txt`) — ORDER 42 would otherwise have halted the board regen INSIDE
the staged transaction. This is the identical shape R23 met, where `harry-armstrong` and
`judson-clarke` flipped `Y -> N` for the same reason.

## PREDICTED (before measurement)

| fact | predicted |
|---|---|
| `sheet_md5` | `4656041e74f7cdf6e7f54af99e5a8381` |
| `sheet_rows` | 219 (unchanged — a re-cut that adds or drops a row is a different act) |
| `sheet_injured_y` | 33 (35 - 2) |

## DISCLOSED MOVERS

`Tom Green` and `Connor Rozee` only. Both flip `injured` `Y -> N`; both gain a dated note in the
`notes` cell. No other cell in any other row is touched. Every other injured=Y row stays injured=Y.

## THE FALSIFIER

`engine_head` must be UNMOVED across the sheet commit. A sheet re-cut that moves `engine_head` is a
red, not a chore: PACKAGE 3a's whole effect is that `engine_head` moves if and only if CODE changed.
