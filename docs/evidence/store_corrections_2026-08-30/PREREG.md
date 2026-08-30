# PREREG — the two impossible-games rows, corrected · 2026-08-30

## What is wrong, and how long it has been wrong

`tools/store_sanity.py` (new, 2026-08-30) asserts what no other guard in this estate asserts: that a
season row says something possible. It found four rows. Every other guard here polices the store's
IDENTITY — Guard 5 asserts its md5, the manifest gate asserts every carrier names the same md5, the
lander re-measures it — and a wrong number hashes exactly as well as a right one.

| row | season | store says | correct |
| --- | --- | --- | --- |
| `jesse-joyce` | 2017 | 61 games, avg 11.0 | **11 games, avg 61.0** |
| `jesse-joyce` | 2018 | 60 games, avg 17.0 | **17 games, avg 60.0** |
| `jesse-joyce` | 2019 | 60 games, avg 19.0 | **19 games, avg 60.0** |
| `nathan-lovett-murray` | 2008 | 40 games, avg 77.8 | **20 games**, avg unchanged |

Joyce's three seasons are a straight games/avg transposition. Lovett-Murray's 2008 is not — 77.8 is a
plausible average — it is a doubled game count.

**The Joyce row has carried those values since the INITIAL SEED (`f4a4d34`, 2026-07-02) and has not
changed in a single commit since.** That was established by walking the store's own history, not by
recollection. The owner has corrected it more than once and every correction died before reaching
the store; there is no record of one anywhere in the register or the docs.

## The career-games field, and why it moves too

Both rows carry a top-level `games` field, and for BOTH of them it equals the sum of the *wrong*
season values exactly:

* `jesse-joyce`: 182 = 61 + 60 + 60 + 1
* `nathan-lovett-murray`: 116 = 18 + **40** + 13 + 12 + 13 + 17 + 3

Two exact three-digit agreements are not coincidence: the field was derived from the seasons for
these rows, from the wrong inputs. Correcting the seasons and leaving it would leave a provable
inconsistency behind. It moves to the corrected sums — 48 and 96.

THIS IS AN INFERENCE, NOT AN OWNER RULING, and it is flagged as such. The owner ruled the season
values; the career totals follow from them by the arithmetic above. Across the store as a whole the
field is NOT generally the season sum (502 of 2650 rows differ), so this is a claim about these two
rows on their own evidence, not a general rule. If the owner reads the dry-run and wants either
career total left alone, those two edits come out and the seasons land without them.

## The prediction

**Zero board movers.** Both players are `_retired: True` and therefore off the active board. The
store identity moves (it must — that is the act), the board identity is expected to move only if
some derived aggregate reads a retired row, and `edit.expected_movers` is declared `[]`: the real
prediction that NO board row moves, which the lander asserts rather than accepts.

If any row moves, this act ABORTS and the movement is explained before it flies again.

## What clears

`tools/store_sanity.py` goes from 4 impossible rows to PASS over 11,484 season rows — verified
against the post-edit text before this spec was written. The check sits in the step-0 preflight, so
the red is visible on every launch until this lands.
