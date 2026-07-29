# R3-4 — would the next round apply false-flag against the landed store?

**Answer: no.** The next round apply will not false-flag. The asymmetry the seam found is real but
does not reach the equality guard; it surfaces as a *data-completeness* gap instead, which is the
re-derivation directive's to fix.

Run against the landed store `5d6e56d05f5e7d9eb8460bd1d07bca6e`.

---

## The two sites, and what they actually do

**The writer — `round_apply.py:180-187`.** This is what decides whether `pos` survives:

```python
entry = next((s for s in scoring if s.get('year') == a.year), None)
if entry is None:
    scoring.append(dict(a.merged_entry))        # NEW row: {year, avg, games} — no pos
else:
    entry['avg']   = a.merged_entry['avg']      # EXISTING row: mutated IN PLACE
    entry['games'] = a.merged_entry['games']    # every other key, including pos, SURVIVES
```

An existing season row is **updated in place, field by field** — it is never replaced by the 3-key
dict. So `pos` is preserved on every season row that already exists.

`score_ingestor.py:183` (`_before_entry`) does return a bare `{'year','avg','games'}`, exactly as the
seam reported — but it is **read-only**, used to compute the merge and report the "before" state. It
is not the writer, and the 3-key shape never reaches the store through it.

**The guard — `staged_apply.py:1327-1333.**` It compares live-store and staged-store season dicts
wholesale, then flags `changed_years - {season}`. Both sides are derived from the same store through
the same code path, so for any given season either both carry `pos` or neither does. The comparison
is symmetric, and a target-season difference is already excused by design.

## Measured exposure at the next apply (R21, season 2026)

| | |
|---|---|
| players with scoring history | 1,924 |
| …already holding a 2026 season row | **653** → in-place update, `pos` survives |
| …with no 2026 row yet | **1,271** → a new row would be appended **without** `pos` |
| 2026 rows currently carrying `pos` | **653 of 653** — full coverage |

Simulated in-place apply (Willem Duursma, the shape every one of the 653 takes):

```
changed_years                  = [2026]
guard flags changed_years-{2026} = EMPTY  ->  NO false flag
```

`dry_run_proof.py --year 2026` against the landed store: **PASS, exit 0**, previewed season entries
reproduce the store byte-for-byte.

## What the real exposure is

Not a false flag — a **hole in the eligibility data**. Any player who gains a *first* 2026 season row
at a future round (a debutant, or a listed player whose first game comes later in the year) gets a
season row with **no `pos` key**. Of the 1,271 players without a 2026 row today, every one who plays
before season end lands an eligibility-less row.

That is invisible to every guard, because nothing reads `pos` yet — which is exactly why it would go
unnoticed until the re-derivation starts consuming it. The durable fix (season-row writers stamp
eligibility at construction) is assigned to the re-derivation directive, not to this job.

**One thing worth flagging for that directive:** the fix has to reach `round_apply.py:182` *and*
`staged_apply.py`'s preview construction, which build `merged_entry` independently
(`staged_apply.py:178-185` and `score_ingestor.py:224-228`). That is the two-axis sibling shape —
two writers of the same row — and fixing one would leave the other producing bare rows.
