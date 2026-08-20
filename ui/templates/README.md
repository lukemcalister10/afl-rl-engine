# `ui/templates/` — the frozen layouts for the five owner-facing pages

**M1a deliverable 5.** The fixed layouts, extracted from the canonical assembly-era pages of
2026-08-19, each with named data slots and a validator that refuses to render a page it cannot fill
honestly.

## The layout law

> **A seat injects data. A seat never injects layout.**

Five skeletons, one stylesheet, one slot contract:

| template | frozen from | row blocks | slots |
|---|---|---|---|
| `tracker.html` | `docs/evidence/assembly_2026-08-19/TRACKER_ASSEMBLY.html` + `TRACKER_ASSEMBLY.csv` headers | `rows` | 28 |
| `players.html` | `ASSEMBLY_PLAYERS.html` | `rows` | 26 |
| `year1.html`   | `ASSEMBLY_YEAR1.html` | `rows` | 24 |
| `noarb.html`   | `ASSEMBLY_NOARB.html` | `bands`, `arms` | 33 |
| `movers.html`  | the weekly movers report schema (`ui/data/movers.js` `reports[].players[]`) as rendered by `ui/app/movers.js` | `players` | 30 |

## Why `ui/templates/` and not `docs/templates/`

The order allowed either. `ui/` wins on three counts, and the third is the deciding one:

1. **These are the UI's pages.** `ui/` already holds `app/` (the renderers), `data/` (the bundles),
   `tools/` (the generators) and `tests/`. The layouts belong beside the code that will consume
   them, not beside the prose that describes them.
2. **`docs/` is where evidence goes to be preserved, not where live code goes to be imported.**
   `docs/evidence/` is an append-only record of what was true on a date. A template is neither — it
   is a live artifact that changes when the owner asks for a column to change. Putting an importable
   module under `docs/evidence/`-adjacent paths would blur the one distinction that tree is for.
3. **The generators that must eventually adopt these live in `ui/tools/`.** The migration this
   tranche sets up is `ui/tools/*` ceasing to emit markup and calling `slots.render()` instead. A
   relative import inside `ui/` is one line; a cross-tree import from `docs/` invites the
   path-resolution problems the audit already found in `ship_gates_check.py:49`.

## The one rule

> **A missing value is a loud failure. It is never a dash.**

`render()` refuses an absent slot, a `None`, an empty string, or any dash sentinel (`-`, `—`, `N/A`,
`null`, `nan`, `TBD`, …), naming the template, the slot and the row index. This is not fussiness.
`AUDIT_CI.md` §1.1 measured the cost:

> "9 × the `#326` per-division pool-entry non-vacuity family — every one reports `board v=-`, i.e.
> the probe cannot reach a live entrant's board price at all (`0 of 14`, `0 of 28`, `0 of 16`, …)."

Nine live guards had been reporting a dash for long enough that nobody knew when it started. A dash
renders, aligns and sorts, and says nothing.

Where "no value" is a genuine fact rather than a failure — a player with no draft pick, a movers
score for a player who did not play — the slot is declared `nullable` in `manifest.json` and the
caller passes the explicit `slots.ABSENT`. **Absence must be declared, once, in the manifest; it is
never inferred from a falsy variable.** Passing `ABSENT` to a slot that is not declared nullable is
itself a failure.

## Usage

```python
import sys; sys.path.insert(0, 'ui/templates')
import slots

html = slots.render('tracker', {
    'page_title': 'Assembly Tracker',
    'subtitle': '...', 'standing_note': '...',
    'board_md5': 'a05fe951', 'store_md5': 'cc02567f', 'engine_head': '5ac6780f',
    'config': 'eed19a75f775', 'as_of_round': 22, 'generated_at': '2026-08-20T04:00:00Z',
    'rows': [{'player': 'Toby Conway', 'pos': 'RUCK', ..., 'pick': slots.ABSENT}],
})
```

`slots.validate(name, data)` returns **every** problem at once rather than raising on the first, so a
seat wiring up a new page learns all of its missing slots in one run.

## The identity stamp is part of the layout

Every skeleton ends with a stamp carrying board / store / engine / config / as-of-round / build time,
and `movers.html` carries **both ends** of its comparison. This is not decoration: a page that does
not name the tree it was built from cannot be told apart from a page built off a different board, and
the audit traced the 63/66 `movers.test.js` failures to exactly that class of boundary ambiguity.
Because the stamp is in the template, a seat cannot forget it — the page will not render without it,
and it may not be filled with a dash.

## Self-test

```
$ python3 ui/templates/selftest.py
TEMPLATE SLOT SELF-TEST: 34 PASS / 0 FAIL
```

It asserts the manifest and the markup cannot drift apart **in both directions**, that every dash
sentinel and structural gap is refused, that declared absence works and undeclared absence does not,
and that injected markup is escaped. It found two real bugs in the validator on its first run — a
case-sensitivity bug that made the columns literally named `K`, `P` and `R` invisible to validation
(16 slots across three templates, shipping `{{K}}` verbatim into the page), and a nullability check
that accepted `ABSENT` on any slot at all. Both are fixed; both are now asserted.

## Scope, stated plainly

**This tranche ships the skeletons and the validator. It does not migrate any generator.** Nothing in
`ui/tools/` calls `slots.render()` yet, and no page in the tree is currently produced through these
templates. Full generator migration is a later tranche. The skeletons are frozen and the contract is
enforced, so that migration is a mechanical, one-generator-at-a-time job rather than a redesign.
