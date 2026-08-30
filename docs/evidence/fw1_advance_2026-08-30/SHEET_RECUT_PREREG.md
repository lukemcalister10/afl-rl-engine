# PREREG-LITE — the FW1 injury-sheet re-cut · 2026-08-30

**Owner word, verbatim:** *"Yes, Viney has returned. Nobody else."*

## Why the re-cut exists

FW1 aborted at `catchup_preflight` with ORDER 42:

> 1 player(s) marked injured=Y on the pinned owner sheet appear in the score file: `['jack-viney']`.
> The advance increments games_2026 for every listed player, so the sheet and the store would
> disagree and the board regen halts INSIDE the staged transaction. The remedy is the owner-worded
> re-cut — not a weakened guard.

Jack Viney played in Finals Week 1 for Melbourne (SC 55). The pinned sheet carried him
`injured=Y`, `games_2026=0`, and the LTI register carries `out_until_2027`. He is demonstrably not.
The guard is right, and it stopped at the door rather than inside the transaction.

## The change — exactly one field on exactly one row

    docs/owner_annotations/SITTER_2026_v1.csv, line 86
    Jack Viney,Melbourne,MID,32,ND,2012,0,237,2025,0.58,1,"yes, 2025",229,Y,
                                                                       ^ injured
                                                                       Y -> N

| | before | after |
| --- | --- | --- |
| md5 | `21361291f26d35108b88f92f885c5063` | `61ef3e61a685909784c1d6eb23859788` |
| rows | 219 | **219** |
| injured=Y | 35 | **34** |

The row carries a QUOTED field containing a comma (`"yes, 2025"`), so it was parsed with the csv
reader to confirm which column `injured` actually is before anything was written — a naive split
lands on `229` and would have edited the wrong field. The replacement is surgical on that one line,
and the result was re-parsed and asserted field-by-field: every column except `injured` is identical,
and exactly one row differs across the whole file.

## What is NOT changed here, and why it is being raised rather than done quietly

`LTI_REGISTER.md` still carries `| jack-viney | Jack Viney | A | 1 | 2026_preseason |
out_until_2027 |`. That is now a stale statement about the world.

It is deliberately NOT in this act. The register is a SEPARATE pinned input (`register` in
expected_boot, currently `652d83e8`), so editing it moves an identity this act declares UNMOVED, and
it would turn a one-field sheet re-cut into a two-identity act. **It has no pricing effect today:**
the register's availability layer prices an "out for the remainder" player's 2026 as COMPLETE
(`fE=1.0`), and with the calendar round held at 24 the season fraction is already 1.0 for everyone —
so the row changes nothing while the home-and-away season is complete. It should be corrected in its
own small act, and it is recorded here so it is not forgotten rather than folded in silently.
